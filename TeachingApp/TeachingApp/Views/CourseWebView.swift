import SwiftUI
import WebKit

struct CourseWebView: View {
    let course: Course

    @State private var htmlContent: String?
    @State private var isLoading = true
    @State private var errorMessage: String?
    private let scanner = HTMLScannerService()

    var body: some View {
        ZStack {
            if isLoading {
                ProgressView("Loading...")
                    .padding()
            } else if let errorMessage {
                VStack(spacing: 16) {
                    Image(systemName: "exclamationmark.triangle")
                        .font(.system(size: 40))
                        .foregroundColor(NeumorphicColors.warning)

                    Text("Unable to load content")
                        .font(.headline)

                    Text(errorMessage)
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)

                    Button("Retry") {
                        Task { await loadContent() }
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
            } else if let htmlContent {
                WebView(htmlString: htmlContent)
            }
        }
        .task {
            await loadContent()
        }
    }

    private func loadContent() async {
        isLoading = true
        errorMessage = nil

        if !course.fileName.isEmpty {
            do {
                htmlContent = try await scanner.downloadHTML(fileName: course.fileName)
            } catch {
                errorMessage = "Failed to download lesson: \(error.localizedDescription)"
            }
        } else if !course.content.isEmpty {
            htmlContent = Self.wrapPlainText(course.content)
        } else {
            htmlContent = Self.wrapPlainText("No lesson content available.")
        }

        isLoading = false
    }

    private static func wrapPlainText(_ text: String) -> String {
        """
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
          body { font-family: -apple-system, sans-serif; padding: 24px; line-height: 1.7; color: #1a1a2e; }
        </style>
        </head>
        <body><p>\(text)</p></body>
        </html>
        """
    }
}

private struct WebView: UIViewRepresentable {
    let htmlString: String

    func makeUIView(context: Context) -> WKWebView {
        WKWebView()
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        webView.loadHTMLString(htmlString, baseURL: nil)
    }
}
