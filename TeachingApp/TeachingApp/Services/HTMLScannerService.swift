import Foundation
import Combine

final class HTMLScannerService: ObservableObject {
    @Published var isScanning = false
    @Published var lastScanTime: Date?
    @Published var scannedCourses: [RemoteCourse] = []
    @Published var errorMessage: String?

    private let owner = "Rosana1517"
    private let repo = "TeachingApp"
    private let accessToken = ""

    struct RemoteCourse: Codable, Identifiable {
        let id: String
        let title: String
        let category: String
        let fileName: String
        let generatedDate: Date
        let description: String
    }

    init() {
        if let timestamp = UserDefaults.standard.object(forKey: "last_scan_timestamp") as? TimeInterval {
            lastScanTime = Date(timeIntervalSince1970: timestamp)
        }
    }

    func scanForNewLessons() async -> [RemoteCourse] {
        await MainActor.run {
            isScanning = true
            errorMessage = nil
        }

        do {
            let courses = try await fetchRemoteCourses()
            let newCourses = filterNewCourses(courses)

            await MainActor.run {
                lastScanTime = Date()
                UserDefaults.standard.set(lastScanTime?.timeIntervalSince1970, forKey: "last_scan_timestamp")
                isScanning = false
                scannedCourses = newCourses
            }

            return newCourses
        } catch {
            await MainActor.run {
                errorMessage = "Scan failed: \(error.localizedDescription)"
                isScanning = false
            }
            return []
        }
    }

    private func fetchRemoteCourses() async throws -> [RemoteCourse] {
        let urlString = "https://api.github.com/repos/\(owner)/\(repo)/releases"
        guard let url = URL(string: urlString) else {
            throw ScannerError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/vnd.github.v3+json", forHTTPHeaderField: "Accept")
        if !accessToken.isEmpty {
            request.setValue("token \(accessToken)", forHTTPHeaderField: "Authorization")
        }

        let (data, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw ScannerError.networkError
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        decoder.dateDecodingStrategy = .iso8601

        let releases = try decoder.decode([Release].self, from: data)

        return releases.flatMap { release in
            release.assets.filter { $0.name.hasSuffix(".html") }.map { asset in
                let baseName = asset.name.replacingOccurrences(of: ".html", with: "")
                return RemoteCourse(
                    id: "\(release.id)-\(asset.name)",
                    title: baseName.replacingOccurrences(of: "lesson-", with: "").capitalized,
                    category: "General",
                    fileName: asset.name,
                    generatedDate: release.publishedAt ?? Date(),
                    description: release.body ?? ""
                )
            }
        }
    }

    private func filterNewCourses(_ allCourses: [RemoteCourse]) -> [RemoteCourse] {
        let existingIDs = Set(Categories.all.flatMap { $0.courses.map { $0.id } })
        return allCourses.filter { !existingIDs.contains($0.id) }
    }

    func downloadHTML(fileName: String) async throws -> String {
        let urlString = "https://api.github.com/repos/\(owner)/\(repo)/releases/latest"
        guard let url = URL(string: urlString) else {
            throw ScannerError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/vnd.github.v3+json", forHTTPHeaderField: "Accept")
        if !accessToken.isEmpty {
            request.setValue("token \(accessToken)", forHTTPHeaderField: "Authorization")
        }

        let (data, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw ScannerError.networkError
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        let release = try decoder.decode(Release.self, from: data)

        guard let asset = release.assets.first(where: { $0.name == fileName }) else {
            throw ScannerError.fileNotFound
        }

        guard let downloadURL = URL(string: asset.downloadUrl) else {
            throw ScannerError.invalidURL
        }

        let (downloadData, downloadResponse) = try await URLSession.shared.data(from: downloadURL)
        guard let downloadHttpResponse = downloadResponse as? HTTPURLResponse, downloadHttpResponse.statusCode == 200 else {
            throw ScannerError.fileDownloadFailed
        }

        guard let htmlContent = String(data: downloadData, encoding: .utf8) else {
            throw ScannerError.fileDownloadFailed
        }

        return htmlContent
    }

    func checkForUpdates() async -> Bool {
        do {
            let courses = try await fetchRemoteCourses()
            return !filterNewCourses(courses).isEmpty
        } catch {
            return false
        }
    }
}

extension HTMLScannerService {
    struct Release: Codable, Identifiable {
        let id: Int
        let tagName: String
        let name: String
        let body: String?
        let publishedAt: Date?
        let assets: [Asset]

        enum CodingKeys: String, CodingKey {
            case id
            case tagName = "tag_name"
            case name
            case body
            case publishedAt = "published_at"
            case assets
        }
    }

    struct Asset: Codable, Identifiable {
        let name: String
        let downloadUrl: String
        let downloadCount: Int

        var id: String { name }

        enum CodingKeys: String, CodingKey {
            case name
            case downloadUrl = "browser_download_url"
            case downloadCount = "download_count"
        }
    }
}

enum ScannerError: Error, LocalizedError {
    case invalidURL
    case networkError
    case fileDownloadFailed
    case fileNotFound

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .networkError:
            return "Network error"
        case .fileDownloadFailed:
            return "File download failed"
        case .fileNotFound:
            return "File not found"
        }
    }
}
