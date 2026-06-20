import SwiftUI

struct Category: Identifiable {
    let id: String
    var title: String
    var icon: String
    var iconColor: Color
    var description: String
    var courses: [Course]

    init(
        id: String = UUID().uuidString,
        title: String,
        icon: String,
        iconColor: Color,
        description: String,
        courses: [Course] = []
    ) {
        self.id = id
        self.title = title
        self.icon = icon
        self.iconColor = iconColor
        self.description = description
        self.courses = courses
    }
}

struct Categories {
    /// Categories are populated dynamically from scanned lesson files
    /// (see `CourseViewModel.checkForNewCourses`) — no seed/placeholder data.
    static var all: [Category] = []
}
