import Foundation

struct NotificationSettings: Codable, Identifiable {
    let id: UUID
    var isEnabled: Bool
    var reminderHour: Int
    var reminderMinute: Int
    var enabledDays: [Int]
    var quietHoursStart: Int
    var quietHoursEnd: Int
    
    init(
        id: UUID = UUID(),
        isEnabled: Bool = true,
        reminderHour: Int = 9,
        reminderMinute: Int = 0,
        enabledDays: [Int] = [1, 2, 3, 4, 5, 6, 0],
        quietHoursStart: Int = 23,
        quietHoursEnd: Int = 7
    ) {
        self.id = id
        self.isEnabled = isEnabled
        self.reminderHour = reminderHour
        self.reminderMinute = reminderMinute
        self.enabledDays = enabledDays
        self.quietHoursStart = quietHoursStart
        self.quietHoursEnd = quietHoursEnd
    }
}
