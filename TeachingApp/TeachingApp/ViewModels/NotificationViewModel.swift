import Foundation
import Combine
import UserNotifications

@MainActor
final class NotificationViewModel: ObservableObject {
    @Published var settings: NotificationSettings
    @Published var isPermissionGranted = false

    init() {
        settings = NotificationService.shared.loadSettings()
        checkPermissionStatus()
    }

    func checkPermissionStatus() {
        UNUserNotificationCenter.current().getNotificationSettings { [weak self] settings in
            DispatchQueue.main.async {
                self?.isPermissionGranted = settings.authorizationStatus == .authorized
            }
        }
    }

    func requestPermission() {
        NotificationService.shared.requestPermission { [weak self] granted in
            DispatchQueue.main.async {
                self?.isPermissionGranted = granted
                if granted {
                    self?.scheduleReminder()
                }
            }
        }
    }

    func saveSettings(hour: Int, minute: Int, isEnabled: Bool) {
        settings.reminderHour = hour
        settings.reminderMinute = minute
        settings.isEnabled = isEnabled
        NotificationService.shared.saveSettings(settings)
        scheduleReminder()
    }

    private func scheduleReminder() {
        NotificationService.shared.scheduleDailyReminder(
            settings: settings,
            courseTitle: "Today's lesson"
        )
    }
}
