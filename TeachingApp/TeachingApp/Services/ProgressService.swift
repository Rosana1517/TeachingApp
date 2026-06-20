import Foundation

final class ProgressService {
    static let shared = ProgressService()

    private let unreadKey = "UnreadCoursesKey"
    private let progressPrefix = "CourseProgress_"

    private init() {}

    func markAsRead(courseId: String) {
        var unreadCourses = unreadCourseIDs()
        unreadCourses.removeAll { $0 == courseId }
        saveUnreadCourseIDs(unreadCourses)
    }

    func markAsUnread(courseId: String) {
        var unreadCourses = unreadCourseIDs()
        guard !unreadCourses.contains(courseId) else { return }
        unreadCourses.append(courseId)
        saveUnreadCourseIDs(unreadCourses)
    }

    func isUnread(courseId: String) -> Bool {
        unreadCourseIDs().contains(courseId)
    }

    func unreadCount() -> Int {
        unreadCourseIDs().count
    }

    func saveProgress(_ course: Course) {
        UserDefaults.standard.set(course.progress, forKey: progressKey(for: course.id))
        UserDefaults.standard.set(course.isRead, forKey: readKey(for: course.id))
    }

    func loadProgress(for courseId: String) -> Double {
        UserDefaults.standard.double(forKey: progressKey(for: courseId))
    }

    func loadReadState(for courseId: String) -> Bool {
        UserDefaults.standard.object(forKey: readKey(for: courseId)) as? Bool ?? false
    }

    func resetAll() {
        UserDefaults.standard.removeObject(forKey: unreadKey)
    }

    private func unreadCourseIDs() -> [String] {
        UserDefaults.standard.array(forKey: unreadKey) as? [String] ?? []
    }

    private func saveUnreadCourseIDs(_ ids: [String]) {
        UserDefaults.standard.set(ids, forKey: unreadKey)
    }

    private func progressKey(for courseId: String) -> String {
        progressPrefix + courseId
    }

    private func readKey(for courseId: String) -> String {
        progressPrefix + courseId + "_read"
    }
}
