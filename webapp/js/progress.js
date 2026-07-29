// Mirrors ProgressService.swift key-for-key so behaviour matches the native app.
const Progress = {
  UNREAD_KEY: "UnreadCoursesKey",
  PROGRESS_PREFIX: "CourseProgress_",

  _unreadIds() {
    try {
      return JSON.parse(localStorage.getItem(this.UNREAD_KEY) || "[]");
    } catch {
      return [];
    }
  },

  _saveUnreadIds(ids) {
    localStorage.setItem(this.UNREAD_KEY, JSON.stringify(ids));
  },

  isUnread(courseId) {
    return this._unreadIds().includes(courseId);
  },

  isLearned(courseId) {
    return !this.isUnread(courseId) && localStorage.getItem(this.PROGRESS_PREFIX + courseId + "_touched") === "1";
  },

  markAsRead(courseId) {
    const ids = this._unreadIds().filter((id) => id !== courseId);
    this._saveUnreadIds(ids);
    localStorage.setItem(this.PROGRESS_PREFIX + courseId + "_read", "1");
    localStorage.setItem(this.PROGRESS_PREFIX + courseId + "_touched", "1");
  },

  markAsUnread(courseId) {
    const ids = this._unreadIds();
    if (!ids.includes(courseId)) ids.push(courseId);
    this._saveUnreadIds(ids);
    localStorage.setItem(this.PROGRESS_PREFIX + courseId + "_read", "0");
    localStorage.setItem(this.PROGRESS_PREFIX + courseId + "_touched", "1");
  },

  toggleLearned(courseId) {
    if (this.isReadState(courseId)) {
      this.markAsUnread(courseId);
    } else {
      this.markAsRead(courseId);
    }
  },

  isReadState(courseId) {
    return localStorage.getItem(this.PROGRESS_PREFIX + courseId + "_read") === "1";
  },

  // Courses start "unread" by default the first time they're seen, matching
  // the native app's default of showing every synced course as unlearned.
  ensureKnown(courseId) {
    const touched = localStorage.getItem(this.PROGRESS_PREFIX + courseId + "_touched") === "1";
    if (touched) return;
    const ids = this._unreadIds();
    if (!ids.includes(courseId)) ids.push(courseId);
    this._saveUnreadIds(ids);
  },

  removeProgress(courseId) {
    this._saveUnreadIds(this._unreadIds().filter((id) => id !== courseId));
    localStorage.removeItem(this.PROGRESS_PREFIX + courseId + "_read");
    localStorage.removeItem(this.PROGRESS_PREFIX + courseId + "_touched");
  },

  resetAll() {
    localStorage.removeItem(this.UNREAD_KEY);
  },
};
