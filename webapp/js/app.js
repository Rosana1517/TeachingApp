const state = {
  courses: [],
  category: "全部",
  showLearned: false,
};

const CATEGORY_LABELS = { all: "全部" };

async function loadCourses() {
  const res = await fetch("courses.json", { cache: "no-store" });
  const courses = await res.json();
  courses.forEach((c) => Progress.ensureKnown(c.id));
  state.courses = courses;
  render();
}

function categories() {
  const set = new Set(state.courses.map((c) => c.category));
  return ["全部", ...Array.from(set)];
}

function filtered() {
  if (state.category === "全部") return state.courses;
  return state.courses.filter((c) => c.category === state.category);
}

function unlearned() {
  return filtered().filter((c) => !Progress.isReadState(c.id));
}

function learned() {
  return filtered().filter((c) => Progress.isReadState(c.id));
}

function render() {
  renderToday();
  renderUnreadCount();
  renderCategories();
  renderCourseList();
}

function renderToday() {
  const el = document.getElementById("today-section");
  const course = unlearned()[0] || filtered()[0];
  if (!course) {
    el.innerHTML = `
      <div class="empty-state">
        <div class="icon">📚</div>
        <div style="font-weight:700;font-size:1.1rem;margin-bottom:8px;">尚無課程</div>
        <div>目前沒有可顯示的課程內容。</div>
      </div>`;
    return;
  }
  el.innerHTML = `
    <h2>今日課程</h2>
    <div class="today-course">
      <div>
        <p class="title">${escapeHtml(course.title)}</p>
        <span class="badge">${escapeHtml(course.category)}</span>
      </div>
      <button class="go-btn" aria-label="開始學習" onclick="location.href='course.html?id=${encodeURIComponent(course.id)}'">→</button>
    </div>`;
}

function renderUnreadCount() {
  document.getElementById("unread-count").textContent = unlearned().length;
}

function renderCategories() {
  const el = document.getElementById("category-scroll");
  el.innerHTML = categories()
    .map((cat) => {
      const count = cat === "全部" ? state.courses.length : state.courses.filter((c) => c.category === cat).length;
      const active = cat === state.category ? "active" : "";
      return `<button class="category-chip ${active}" onclick="setCategory('${escapeAttr(cat)}')">${escapeHtml(cat)} (${count})</button>`;
    })
    .join("");
}

function setCategory(cat) {
  state.category = cat;
  render();
}

function renderCourseList() {
  const el = document.getElementById("course-list");
  const unlearnedCourses = unlearned();
  const learnedCourses = learned();

  let html = unlearnedCourses.map(courseCardHtml).join("");

  if (learnedCourses.length > 0) {
    html += `
      <button class="learned-toggle" onclick="toggleLearnedSection()">
        <span>✅ 已學習</span>
        <span class="spacer"></span>
        <span class="count-pill">${learnedCourses.length}</span>
        <span>${state.showLearned ? "▲" : "▼"}</span>
      </button>`;
    if (state.showLearned) {
      html += learnedCourses.map(courseCardHtml).join("");
    }
  }

  if (unlearnedCourses.length === 0 && learnedCourses.length === 0) {
    html = "";
  }

  el.innerHTML = html;
}

function toggleLearnedSection() {
  state.showLearned = !state.showLearned;
  renderCourseList();
}

function formatCourseDate(dateStr) {
  if (!dateStr) return "";
  const [, m, d] = dateStr.split("-");
  return `${m}/${d}`;
}

function courseCardHtml(course) {
  const isLearned = Progress.isReadState(course.id);
  const dateLabel = formatCourseDate(course.generatedDate);
  const meta = dateLabel
    ? `${escapeHtml(course.category)} · ${dateLabel}`
    : escapeHtml(course.category);
  return `
    <div class="course-card ${isLearned ? "learned" : ""}" onclick="location.href='course.html?id=${encodeURIComponent(course.id)}'">
      <div class="info">
        <p class="title">${escapeHtml(course.title)}</p>
        <p class="meta">${meta}</p>
      </div>
      <button class="check" aria-label="標記完成" onclick="event.stopPropagation(); toggleLearned('${escapeAttr(course.id)}')">${isLearned ? "✓" : ""}</button>
    </div>`;
}

function toggleLearned(courseId) {
  Progress.toggleLearned(courseId);
  render();
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function escapeAttr(str) {
  return escapeHtml(str).replace(/'/g, "&#39;");
}

document.addEventListener("DOMContentLoaded", () => {
  loadCourses();
  setupInstallBanner();
  checkDailyReminder();
});

// iOS/Android back-navigation (system back gesture or button) can restore this
// page from the browser's bfcache instead of reloading it, which replays the
// exact DOM from before the user left — including a course that was since
// marked as learned on course.html still showing as unlearned here, because
// no script re-runs on a bfcache restore. Re-render from localStorage
// (already up to date) whenever that happens.
window.addEventListener("pageshow", (event) => {
  if (event.persisted) render();
});

function setupInstallBanner() {
  const isStandalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
  if (isStandalone) return;
  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  if (!isIOS) return;
  const dismissed = localStorage.getItem("installBannerDismissed") === "1";
  if (dismissed) return;
  const banner = document.getElementById("install-banner");
  banner.classList.add("show");
}

function dismissInstallBanner() {
  localStorage.setItem("installBannerDismissed", "1");
  document.getElementById("install-banner").classList.remove("show");
}

// Fallback for browsers/situations without an active Web Push subscription
// (e.g. push unsupported, or the user hasn't granted it yet): if today's
// reminder time has passed and there's still an unlearned course, show a
// one-time notification while the app happens to be open. Skipped entirely
// when a real push subscription exists, since the push server already
// covers this — showing both would double-notify.
async function checkDailyReminder() {
  const settings = JSON.parse(localStorage.getItem("NotificationSettingsKey") || "null");
  if (!settings || !settings.isEnabled) return;
  if (!("Notification" in window) || Notification.permission !== "granted") return;
  if (window.Push && (await Push.getCurrentSubscription())) return;

  const today = new Date().toISOString().slice(0, 10);
  const lastShown = localStorage.getItem("lastReminderShownDate");
  if (lastShown === today) return;

  const now = new Date();
  const target = new Date();
  target.setHours(settings.reminderHour, settings.reminderMinute, 0, 0);
  if (now < target) return;

  if (unlearned().length === 0) return;

  localStorage.setItem("lastReminderShownDate", today);
  const title = "TeachingApp 學習提醒";
  const body = `該複習了：${unlearned()[0].title}`;

  // iOS Safari (including installed standalone PWAs) does not implement the
  // `new Notification()` constructor at all — it silently throws. Notifications
  // there must go through the active service worker's registration instead.
  if ("serviceWorker" in navigator) {
    const reg = await navigator.serviceWorker.getRegistration();
    if (reg) {
      reg.showNotification(title, { body });
      return;
    }
  }
  new Notification(title, { body });
}
