import Foundation
import UserNotifications

final class NotificationService {
    static let shared = NotificationService()

    private let settingsKey = "NotificationSettingsKey"

    private init() {}

    func loadSettings() -> NotificationSettings {
        if let data = UserDefaults.standard.data(forKey: settingsKey),
           let settings = try? JSONDecoder().decode(NotificationSettings.self, from: data) {
            return settings
        }
        return NotificationSettings()
    }

    func saveSettings(_ settings: NotificationSettings) {
        if let data = try? JSONEncoder().encode(settings) {
            UserDefaults.standard.set(data, forKey: settingsKey)
        }
    }

    func requestPermission(completion: @escaping (Bool) -> Void) {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
            if let error {
                print("Notification permission error: \(error.localizedDescription)")
            }
            completion(granted)
        }
    }

    func scheduleDailyReminder(settings: NotificationSettings, courseTitle: String) {
        UNUserNotificationCenter.current().removePendingNotificationRequests(withIdentifiers: ["dailyReminder"])

        guard settings.isEnabled else { return }

        let content = UNMutableNotificationContent()
        content.title = "TeachingApp reminder"
        content.body = "Time to review: \(courseTitle)"
        content.sound = .default

        var components = DateComponents()
        components.hour = settings.reminderHour
        components.minute = settings.reminderMinute

        let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: true)
        let request = UNNotificationRequest(identifier: "dailyReminder", content: content, trigger: trigger)

        UNUserNotificationCenter.current().add(request) { error in
            if let error {
                print("Notification scheduling error: \(error.localizedDescription)")
            }
        }
    }

    func cancelAllReminders() {
        UNUserNotificationCenter.current().removeAllPendingNotificationRequests()
    }
}
