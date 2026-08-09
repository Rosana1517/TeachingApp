import { buildPushPayload } from "@block65/webcrypto-web-push";

const REMINDER_TITLE = "TeachingApp 學習提醒";
const REMINDER_BODY = "今天還有課程沒學完，點開看看吧！";
const WINDOW_MINUTES = 15;

function corsHeaders(env) {
  return {
    "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN,
    "Access-Control-Allow-Methods": "POST, DELETE, OPTIONS, GET",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function jsonResponse(body, status, env) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders(env) },
  });
}

async function subscriptionId(endpoint) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(endpoint));
  return btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

async function handleSubscribe(request, env) {
  const body = await request.json();
  const { subscription, reminderHour, reminderMinute, timezone } = body || {};
  if (!subscription?.endpoint || !subscription?.keys?.p256dh || !subscription?.keys?.auth) {
    return jsonResponse({ error: "invalid subscription" }, 400, env);
  }
  if (
    typeof reminderHour !== "number" || reminderHour < 0 || reminderHour > 23 ||
    typeof reminderMinute !== "number" || reminderMinute < 0 || reminderMinute > 59 ||
    typeof timezone !== "string" || !timezone
  ) {
    return jsonResponse({ error: "invalid reminder settings" }, 400, env);
  }

  const id = await subscriptionId(subscription.endpoint);
  const existing = await env.SUBSCRIPTIONS.get(id, "json");
  await env.SUBSCRIPTIONS.put(
    id,
    JSON.stringify({
      subscription,
      reminderHour,
      reminderMinute,
      timezone,
      lastSentDate: existing?.lastSentDate ?? null,
    })
  );
  return jsonResponse({ ok: true }, 200, env);
}

async function handleUnsubscribe(request, env) {
  const { endpoint } = (await request.json()) || {};
  if (!endpoint) return jsonResponse({ error: "missing endpoint" }, 400, env);
  const id = await subscriptionId(endpoint);
  await env.SUBSCRIPTIONS.delete(id);
  return jsonResponse({ ok: true }, 200, env);
}

async function sendPush(record, env) {
  const vapid = {
    subject: env.VAPID_SUBJECT,
    publicKey: env.VAPID_PUBLIC_KEY,
    privateKey: env.VAPID_PRIVATE_KEY,
  };
  const message = {
    data: JSON.stringify({ title: REMINDER_TITLE, body: REMINDER_BODY }),
    options: { ttl: 3600 },
  };
  const payload = await buildPushPayload(message, record.subscription, vapid);
  return fetch(record.subscription.endpoint, payload);
}

function localTimeParts(timezone, date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: timezone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const map = Object.fromEntries(parts.map((p) => [p.type, p.value]));
  return {
    dateStr: `${map.year}-${map.month}-${map.day}`,
    minutesOfDay: Number(map.hour) * 60 + Number(map.minute),
  };
}

async function runReminders(env) {
  const now = new Date();
  let cursor;
  do {
    const page = await env.SUBSCRIPTIONS.list({ cursor });
    for (const key of page.keys) {
      const record = await env.SUBSCRIPTIONS.get(key.name, "json");
      if (!record) continue;

      let local;
      try {
        local = localTimeParts(record.timezone, now);
      } catch {
        continue; // invalid timezone string, skip
      }

      const target = record.reminderHour * 60 + record.reminderMinute;
      const inWindow = local.minutesOfDay >= target && local.minutesOfDay < target + WINDOW_MINUTES;
      if (!inWindow || record.lastSentDate === local.dateStr) continue;

      try {
        const res = await sendPush(record, env);
        if (res.status === 404 || res.status === 410) {
          await env.SUBSCRIPTIONS.delete(key.name);
        } else if (res.ok) {
          await env.SUBSCRIPTIONS.put(key.name, JSON.stringify({ ...record, lastSentDate: local.dateStr }));
        }
      } catch (err) {
        console.error("push failed for", key.name, err);
      }
    }
    cursor = page.cursor;
  } while (cursor);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(env) });
    }

    if (url.pathname === "/vapid-public-key" && request.method === "GET") {
      return jsonResponse({ publicKey: env.VAPID_PUBLIC_KEY }, 200, env);
    }

    if (url.pathname === "/subscribe" && request.method === "POST") {
      return handleSubscribe(request, env);
    }

    if (url.pathname === "/unsubscribe" && request.method === "POST") {
      return handleUnsubscribe(request, env);
    }

    // Manual trigger for verifying delivery end-to-end without waiting for
    // the cron window; requires the admin token as a query param.
    if (url.pathname === "/send-test" && request.method === "POST") {
      if (url.searchParams.get("token") !== env.ADMIN_TOKEN) {
        return jsonResponse({ error: "unauthorized" }, 401, env);
      }
      const { endpoint } = await request.json();
      const id = await subscriptionId(endpoint);
      const record = await env.SUBSCRIPTIONS.get(id, "json");
      if (!record) return jsonResponse({ error: "not found" }, 404, env);
      const res = await sendPush(record, env);
      return jsonResponse({ status: res.status }, 200, env);
    }

    return jsonResponse({ error: "not found" }, 404, env);
  },

  async scheduled(event, env, ctx) {
    ctx.waitUntil(runReminders(env));
  },
};
