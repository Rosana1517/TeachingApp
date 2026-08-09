// Web Push subscription management. Talks to the teachingapp-push Cloudflare
// Worker (separate origin from the Pages site) which stores subscriptions in
// KV and fires reminders via a cron trigger, so notifications can arrive even
// when this app isn't open — unlike the old in-app-only reminder check.
const PUSH_SERVER_URL = "https://teachingapp-push.teachingapp-push-worker.workers.dev";

function isIOS() {
  return /iphone|ipad|ipod/i.test(navigator.userAgent);
}

function isStandalone() {
  return window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
}

function pushSupported() {
  return "serviceWorker" in navigator && "PushManager" in window && "Notification" in window;
}

// iOS only allows Notification permission requests / push subscriptions from
// an installed (Add to Home Screen) standalone PWA, not from a Safari tab.
function pushBlockedReason() {
  if (!pushSupported()) return "此瀏覽器不支援推播通知。";
  if (isIOS() && !isStandalone()) return "請先「加入主畫面」，從主畫面開啟的 App 才能使用推播通知。";
  return null;
}

function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
  const rawData = atob(base64);
  return Uint8Array.from([...rawData].map((c) => c.charCodeAt(0)));
}

async function getCurrentSubscription() {
  if (!pushSupported()) return null;
  const registration = await navigator.serviceWorker.ready;
  return registration.pushManager.getSubscription();
}

async function subscribeToPush(reminderHour, reminderMinute) {
  const blocked = pushBlockedReason();
  if (blocked) throw new Error(blocked);

  const permission = await Notification.requestPermission();
  if (permission !== "granted") throw new Error("通知權限被拒絕。");

  const registration = await navigator.serviceWorker.ready;
  let subscription = await registration.pushManager.getSubscription();

  if (!subscription) {
    const keyRes = await fetch(`${PUSH_SERVER_URL}/vapid-public-key`);
    const { publicKey } = await keyRes.json();
    subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(publicKey),
    });
  }

  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const res = await fetch(`${PUSH_SERVER_URL}/subscribe`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ subscription: subscription.toJSON(), reminderHour, reminderMinute, timezone }),
  });
  if (!res.ok) throw new Error("伺服器儲存訂閱失敗。");
  return subscription;
}

async function unsubscribeFromPush() {
  const subscription = await getCurrentSubscription();
  if (!subscription) return;
  try {
    await fetch(`${PUSH_SERVER_URL}/unsubscribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ endpoint: subscription.endpoint }),
    });
  } finally {
    await subscription.unsubscribe();
  }
}

window.Push = { subscribeToPush, unsubscribeFromPush, getCurrentSubscription, pushBlockedReason, pushSupported };
