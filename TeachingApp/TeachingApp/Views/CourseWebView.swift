import SwiftUI
import UIKit

struct CourseWebView: View {
    let course: Course

    @State private var isLoading = true
    @State private var errorMessage: String?
    @State private var lessons: [LessonContent] = []

    var body: some View {
        ZStack {
            if isLoading {
                ProgressView("Loading...")
                    .padding()
            } else if let errorMessage {
                VStack(spacing: 16) {
                    Image(systemName: "exclamationmark.triangle")
                        .font(.system(size: 40))
                        .foregroundColor(.orange)

                    Text("Unable to load content")
                        .font(.headline)

                    Text(errorMessage)
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)

                    Button("Retry") {
                        loadCourseContent()
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
            } else {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        ForEach(lessons) { lesson in
                            LessonView(lesson: lesson)
                        }
                    }
                    .padding()
                }
            }
        }
        .task {
            loadCourseContent()
        }
    }

    private func loadCourseContent() {
        isLoading = true
        errorMessage = nil
        lessons = []

        if !course.content.isEmpty {
            lessons = HTMLParserService.parseHTMLContent(htmlString: course.content)
        } else {
            lessons = [LessonContent(type: .text, value: "No lesson content available.")]
        }

        isLoading = false
    }
}

fileprivate struct LessonView: View {
    let lesson: LessonContent

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            switch lesson.type {
            case .title:
                Text(lesson.value)
                    .font(.largeTitle)
                    .fontWeight(.bold)
            case .heading:
                Text(lesson.value)
                    .font(.title2)
                    .fontWeight(.semibold)
            case .text:
                Text(lesson.value)
                    .font(.body)
                    .lineSpacing(4)
            case .code:
                CodeBlockView(code: lesson.value)
            case .note:
                NoteView(text: lesson.value)
            case .quiz:
                QuizView(quizData: lesson.value)
            }
        }
        .padding(.vertical, 4)
    }
}

struct CodeBlockView: View {
    let code: String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Code")
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(.secondary)

            Text(code)
                .font(.system(.body, design: .monospaced))
                .lineSpacing(2)
                .textSelection(.enabled)
        }
        .padding()
        .background(Color(.systemGray5))
        .cornerRadius(8)
    }
}

struct NoteView: View {
    let text: String

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: "info.circle.fill")
                .foregroundColor(.blue)
                .font(.title2)

            Text(text)
                .font(.caption)
                .foregroundColor(.secondary)
                .lineSpacing(2)
        }
        .padding()
        .background(Color.blue.opacity(0.1))
        .cornerRadius(8)
    }
}

struct QuizView: View {
    let quizData: String

    private var components: [String] {
        quizData.components(separatedBy: "|")
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "questionmark.circle.fill")
                    .foregroundColor(.purple)
                Text("Quiz")
                    .font(.headline)
            }

            if components.count >= 7 {
                Text(components[0])
                    .font(.body)

                VStack(alignment: .leading, spacing: 8) {
                    ForEach(1..<5, id: \.self) { index in
                        Button(action: {}) {
                            HStack {
                                Text("\(index).")
                                    .fontWeight(.semibold)
                                Text(components[index])
                            }
                        }
                        .buttonStyle(.plain)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                    }
                }

                Text(components[6])
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(Color.purple.opacity(0.1))
        .cornerRadius(8)
    }
}

fileprivate struct HTMLParserService {
    static func parseHTMLContent(htmlString: String) -> [LessonContent] {
        var lessons: [LessonContent] = []
        var currentText = ""
        var inCodeBlock = false
        var codeContent = ""

        for rawLine in htmlString.components(separatedBy: .newlines) {
            let line = rawLine.trimmingCharacters(in: .whitespacesAndNewlines)
            guard !line.isEmpty else { continue }

            if line.hasPrefix("[code]") || line.hasPrefix("<pre>") || line.hasPrefix("<code>") {
                if !currentText.isEmpty {
                    lessons.append(LessonContent(type: .text, value: currentText))
                    currentText = ""
                }
                inCodeBlock = true
                codeContent = line
                    .replacingOccurrences(of: "[code]", with: "")
                    .replacingOccurrences(of: "<pre>", with: "")
                    .replacingOccurrences(of: "<code>", with: "")
                continue
            }

            if line.hasPrefix("[/code]") || line.hasPrefix("</pre>") || line.hasPrefix("</code>") {
                inCodeBlock = false
                if !codeContent.isEmpty {
                    lessons.append(LessonContent(type: .code, value: codeContent))
                    codeContent = ""
                }
                continue
            }

            if inCodeBlock {
                codeContent += (codeContent.isEmpty ? "" : "\n") + line
                continue
            }

            if line.hasPrefix("# ") {
                if !currentText.isEmpty {
                    lessons.append(LessonContent(type: .text, value: currentText))
                    currentText = ""
                }
                lessons.append(LessonContent(type: .heading, value: String(line.dropFirst(2))))
                continue
            }

            if line.hasPrefix("[note]") {
                if !currentText.isEmpty {
                    lessons.append(LessonContent(type: .text, value: currentText))
                    currentText = ""
                }
                let noteContent = line
                    .replacingOccurrences(of: "[note]", with: "")
                    .replacingOccurrences(of: "[/note]", with: "")
                    .trimmingCharacters(in: .whitespaces)
                lessons.append(LessonContent(type: .note, value: noteContent))
                continue
            }

            if line.hasPrefix("[quiz]") {
                if !currentText.isEmpty {
                    lessons.append(LessonContent(type: .text, value: currentText))
                    currentText = ""
                }
                let quizContent = line
                    .replacingOccurrences(of: "[quiz]", with: "")
                    .trimmingCharacters(in: .whitespaces)
                lessons.append(LessonContent(type: .quiz, value: quizContent))
                continue
            }

            currentText += (currentText.isEmpty ? "" : " ") + line
        }

        if !currentText.isEmpty {
            lessons.append(LessonContent(type: .text, value: currentText))
        }

        return lessons.isEmpty ? [LessonContent(type: .text, value: htmlString)] : lessons
    }
}

fileprivate struct LessonContent: Identifiable {
    let id = UUID()
    let type: LessonType
    let value: String
}

fileprivate enum LessonType {
    case title
    case heading
    case text
    case code
    case note
    case quiz
}
