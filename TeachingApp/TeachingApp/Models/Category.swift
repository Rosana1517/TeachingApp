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
    static var all: [Category] = [
        Category(
            id: "1",
            title: "Programming",
            icon: "code",
            iconColor: .blue,
            description: "Swift, SwiftUI, and iOS fundamentals",
            courses: [
                Course(
                    id: "1",
                    title: "Swift Basics",
                    category: "Programming",
                    content: "Intro content",
                    isRead: false,
                    progress: 0.0,
                    generatedDate: Date()
                ),
                Course(
                    id: "2",
                    title: "SwiftUI Basics",
                    category: "Programming",
                    content: "Intro content",
                    isRead: false,
                    progress: 0.0,
                    generatedDate: Date()
                ),
                Course(
                    id: "3",
                    title: "iOS App Basics",
                    category: "Programming",
                    content: "Intro content",
                    isRead: false,
                    progress: 0.0,
                    generatedDate: Date()
                )
            ]
        ),
        Category(
            id: "2",
            title: "Data",
            icon: "tree",
            iconColor: .green,
            description: "Data structures and algorithms"
        ),
        Category(
            id: "3",
            title: "Database",
            icon: "database",
            iconColor: .purple,
            description: "Database concepts"
        ),
        Category(
            id: "4",
            title: "Network",
            icon: "wifi",
            iconColor: .orange,
            description: "Networking and APIs"
        ),
        Category(
            id: "5",
            title: "Security",
            icon: "lock.shield",
            iconColor: .red,
            description: "Security basics"
        ),
        Category(
            id: "6",
            title: "Cloud",
            icon: "cloud",
            iconColor: .cyan,
            description: "Cloud concepts"
        ),
        Category(
            id: "7",
            title: "AI",
            icon: "cpu",
            iconColor: .indigo,
            description: "AI and automation"
        ),
        Category(
            id: "8",
            title: "Mobile",
            icon: "iphone",
            iconColor: .pink,
            description: "iOS and Android"
        ),
        Category(
            id: "9",
            title: "Web",
            icon: "globe",
            iconColor: .teal,
            description: "Web development"
        ),
        Category(
            id: "10",
            title: "Other",
            icon: "ellipsis.circle",
            iconColor: .gray,
            description: "Miscellaneous topics"
        )
    ]
}
