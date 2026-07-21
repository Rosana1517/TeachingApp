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
        let downloadUrl: String
        let generatedDate: Date
        let description: String
    }

    init() {
        if let timestamp = UserDefaults.standard.object(forKey: "last_scan_timestamp") as? TimeInterval {
            lastScanTime = Date(timeIntervalSince1970: timestamp)
        }
    }

    func scanForNewLessons() async throws -> [RemoteCourse] {
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
            throw error
        }
    }

    private func fetchAllReleases() async throws -> [Release] {
        // Release/Asset already declare explicit snake_case CodingKeys, so
        // .convertFromSnakeCase must NOT be set here — combining both makes
        // JSONDecoder look for the already-camelCased key name and silently
        // throw keyNotFound for every required field, which the catch below
        // swallowed into an empty result instead of surfacing a real error.
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601

        var allReleases: [Release] = []
        var page = 1

        // Without explicit pagination, the API defaults to the 30 most recent
        // releases — as IPA builds pile up, that silently pushes the oldest
        // lesson releases out of view. Page through everything instead, up to
        // a generous cap so this can never loop forever.
        while page <= 20 {
            let urlString = "https://api.github.com/repos/\(owner)/\(repo)/releases?per_page=100&page=\(page)"
            guard let url = URL(string: urlString) else {
                throw ScannerError.invalidURL
            }

            var request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData)
            request.httpMethod = "GET"
            request.setValue("application/vnd.github.v3+json", forHTTPHeaderField: "Accept")
            if !accessToken.isEmpty {
                request.setValue("token \(accessToken)", forHTTPHeaderField: "Authorization")
            }

            let (data, response) = try await URLSession.shared.data(for: request)
            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                throw ScannerError.networkError
            }

            let pageReleases = try decoder.decode([Release].self, from: data)
            allReleases.append(contentsOf: pageReleases)

            if pageReleases.count < 100 {
                break
            }
            page += 1
        }

        return allReleases
    }

    private func fetchRemoteCourses() async throws -> [RemoteCourse] {
        async let releaseCoursesTask = fetchReleaseCourses()
        async let repoCoursesTask = fetchRepositoryCourses()

        let releaseCourses = try await releaseCoursesTask
        let repoCourses = try await repoCoursesTask

        // Prefer release assets when present because they carry publish metadata,
        // but fall back to repo HTML files so freshly committed lessons are still
        // readable before the release-upload workflow catches up.
        var mergedCoursesByFileName = Dictionary(
            uniqueKeysWithValues: releaseCourses.map { ($0.fileName, $0) }
        )

        for repoCourse in repoCourses where mergedCoursesByFileName[repoCourse.fileName] == nil {
            mergedCoursesByFileName[repoCourse.fileName] = repoCourse
        }

        return mergedCoursesByFileName.values.sorted { lhs, rhs in
            if lhs.generatedDate != rhs.generatedDate {
                return lhs.generatedDate > rhs.generatedDate
            }
            return Self.lessonOrder(for: lhs.fileName) > Self.lessonOrder(for: rhs.fileName)
        }
    }

    private func fetchReleaseCourses() async throws -> [RemoteCourse] {
        let releases = try await fetchAllReleases()

        return releases.flatMap { release in
            release.assets
                .filter { Self.isLessonHTMLFile($0.name) }
                .map { asset in
                    let metadata = Self.parseCourseMetadata(fileName: asset.name)
                    return RemoteCourse(
                        id: "\(release.id)-\(asset.name)",
                        title: metadata.title,
                        category: metadata.category,
                        fileName: asset.name,
                        downloadUrl: asset.downloadUrl,
                        generatedDate: release.publishedAt ?? Date(),
                        description: release.body ?? ""
                    )
                }
        }
    }

    private func fetchRepositoryCourses() async throws -> [RemoteCourse] {
        let topLevel = try await fetchContents(at: "TeachingApp")

        // Legacy: HTML files directly in TeachingApp/ (kept for backwards compat)
        var allCourses = topLevel
            .filter { $0.type == "file" && Self.isLessonHTMLFile($0.name) }
            .map { mapContentToCourse($0) }

        // Scan category subdirectories (e.g. french/, vibe/)
        let subdirs = topLevel.filter { $0.type == "dir" }
        for subdir in subdirs {
            let subItems = try await fetchContents(at: subdir.path)
            let lessonCourses = subItems
                .filter { $0.type == "file" && Self.isLessonHTMLFile($0.name) }
                .map { mapContentToCourse($0) }
            allCourses.append(contentsOf: lessonCourses)
        }

        return allCourses
    }

    private func fetchContents(at path: String) async throws -> [RepositoryContent] {
        guard let url = URL(string: "https://api.github.com/repos/\(owner)/\(repo)/contents/\(path)?ref=main") else {
            throw ScannerError.invalidURL
        }
        var request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData)
        request.httpMethod = "GET"
        request.setValue("application/vnd.github.v3+json", forHTTPHeaderField: "Accept")
        if !accessToken.isEmpty {
            request.setValue("token \(accessToken)", forHTTPHeaderField: "Authorization")
        }
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw ScannerError.networkError
        }
        return try JSONDecoder().decode([RepositoryContent].self, from: data)
    }

    private func mapContentToCourse(_ item: RepositoryContent) -> RemoteCourse {
        let metadata = Self.parseCourseMetadata(fileName: item.name)
        return RemoteCourse(
            id: "repo-\(item.path)",
            title: metadata.title,
            category: metadata.category,
            fileName: item.name,
            downloadUrl: item.downloadUrl ?? "https://raw.githubusercontent.com/\(owner)/\(repo)/main/\(item.path)",
            generatedDate: Date(),
            description: "Loaded from repository contents"
        )
    }

    /// Lesson HTML assets follow the naming convention `{category}-lesson-{number}.html`
    /// (e.g. `french-lesson-01.html`) so new subjects can be introduced just by choosing
    /// a filename when publishing a release — no app code changes needed. Files without
    /// the `-lesson-` marker (legacy naming) fall back to a single "General" category.
    static func parseCourseMetadata(fileName: String) -> (category: String, title: String) {
        let baseName = fileName.replacingOccurrences(of: ".html", with: "")

        guard let range = baseName.range(of: "-lesson-") else {
            let title = baseName.replacingOccurrences(of: "lesson-", with: "").capitalized
            return (category: "General", title: title)
        }

        let categoryRaw = String(baseName[..<range.lowerBound])
        let numberPart = String(baseName[range.upperBound...])
        let category = categoryRaw.replacingOccurrences(of: "-", with: " ").capitalized
        let title = "\(category) Lesson \(numberPart)"
        return (category: category, title: title)
    }

    private static func isLessonHTMLFile(_ fileName: String) -> Bool {
        fileName.hasSuffix(".html") && fileName.contains("-lesson-")
    }

    private static func lessonOrder(for fileName: String) -> Int {
        let pattern = #"-lesson-(\d+)\.html$"#
        guard
            let regex = try? NSRegularExpression(pattern: pattern),
            let match = regex.firstMatch(
                in: fileName,
                range: NSRange(location: 0, length: fileName.utf16.count)
            ),
            let range = Range(match.range(at: 1), in: fileName)
        else {
            return 0
        }

        return Int(fileName[range]) ?? 0
    }

    private func filterNewCourses(_ allCourses: [RemoteCourse]) -> [RemoteCourse] {
        let existingIDs = Set(Categories.all.flatMap { $0.courses.map { $0.id } })
        return allCourses.filter { !existingIDs.contains($0.id) }
    }

    func downloadHTML(from downloadUrl: String) async throws -> String {
        guard let downloadURL = URL(string: downloadUrl) else {
            throw ScannerError.invalidURL
        }

        let downloadRequest = URLRequest(url: downloadURL, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData)
        let (downloadData, downloadResponse) = try await URLSession.shared.data(for: downloadRequest)
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

    struct RepositoryContent: Codable, Identifiable {
        let name: String
        let path: String
        let downloadUrl: String?
        let type: String

        var id: String { path }

        enum CodingKeys: String, CodingKey {
            case name
            case path
            case downloadUrl = "download_url"
            case type
        }
    }
}

enum ScannerError: Error, LocalizedError {
    case invalidURL
    case networkError
    case fileDownloadFailed

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .networkError:
            return "Network error"
        case .fileDownloadFailed:
            return "File download failed"
        }
    }
}
