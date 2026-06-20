import Foundation

struct Course: Identifiable, Codable {
    let id: String
    var title: String
    var category: String
    var content: String
    var fileName: String
    var filePath: String
    var isRead: Bool
    var readDate: Date?
    var progress: Double
    var generatedDate: Date
    
    init(
        id: String = UUID().uuidString,
        title: String,
        category: String,
        content: String = "",
        fileName: String = "",
        filePath: String = "",
        isRead: Bool = false,
        readDate: Date? = nil,
        progress: Double = 0.0,
        generatedDate: Date = Date()
    ) {
        self.id = id
        self.title = title
        self.category = category
        self.content = content
        self.fileName = fileName
        self.filePath = filePath
        self.isRead = isRead
        self.readDate = readDate
        self.progress = progress
        self.generatedDate = generatedDate
    }
}
