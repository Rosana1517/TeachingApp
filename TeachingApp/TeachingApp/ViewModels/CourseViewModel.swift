import Foundation
import Combine

@MainActor
final class CourseViewModel: ObservableObject {
    @Published var courses: [Course] = []
    @Published var filteredCourses: [Course] = []
    @Published var selectedCategory: String = "All"
    @Published var searchText: String = ""
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var hasNewCourses = false

    private var cancellables = Set<AnyCancellable>()
    private let htmlScanner = HTMLScannerService()

    init() {
        fetchCourses()

        $searchText
            .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
            .sink { [weak self] _ in
                self?.filterCourses()
            }
            .store(in: &cancellables)

        $selectedCategory
            .debounce(for: .milliseconds(100), scheduler: RunLoop.main)
            .sink { [weak self] _ in
                self?.filterCourses()
            }
            .store(in: &cancellables)

        Task {
            await checkForNewCourses()
        }
    }

    func loadCourses() {
        fetchCourses()
    }

    func refresh() async {
        await checkForNewCourses()
    }

    func fetchCourses() {
        courses = Categories.all.flatMap { $0.courses }
        filterCourses()
    }

    private func checkForNewCourses() async {
        isLoading = true

        defer {
            isLoading = false
        }

        do {
            let newCourses = try await htmlScanner.scanForNewLessons()
            guard !newCourses.isEmpty else { return }

            hasNewCourses = true

            for remoteCourse in newCourses {
                let course = Course(
                    id: remoteCourse.id,
                    title: remoteCourse.title,
                    category: remoteCourse.category,
                    content: remoteCourse.description,
                    fileName: remoteCourse.fileName,
                    filePath: remoteCourse.downloadUrl,
                    isRead: false,
                    readDate: nil,
                    progress: 0.0,
                    generatedDate: remoteCourse.generatedDate
                )

                if let index = Categories.all.firstIndex(where: { $0.title == remoteCourse.category }) {
                    var category = Categories.all[index]
                    category.courses.append(course)
                    Categories.all[index] = category
                } else {
                    Categories.all.append(
                        Category(
                            title: remoteCourse.category,
                            icon: "book.fill",
                            iconColor: .blue,
                            description: "Imported lessons",
                            courses: [course]
                        )
                    )
                }

                courses.append(course)
            }

            filterCourses()
        } catch {
            errorMessage = "Failed to scan lessons: \(error.localizedDescription)"
        }
    }

    func markAsRead(course: Course) {
        guard let index = courses.firstIndex(where: { $0.id == course.id }) else { return }
        courses[index].isRead = true
        filterCourses()
    }

    func updateProgress(course: Course, progress: Double) {
        guard let index = courses.firstIndex(where: { $0.id == course.id }) else { return }

        courses[index].progress = progress
        if progress >= 1.0 {
            courses[index].isRead = true
        }

        ProgressService.shared.saveProgress(courses[index])
        filterCourses()
    }

    func filterCourses() {
        filteredCourses = courses.filter { course in
            let matchesCategory = selectedCategory == "All" || course.category == selectedCategory
            let matchesSearch = searchText.isEmpty
                || course.title.localizedCaseInsensitiveContains(searchText)
                || course.category.localizedCaseInsensitiveContains(searchText)
            return matchesCategory && matchesSearch
        }
    }

    var allCategories: [String] {
        ["All"] + Categories.all.map { $0.title }
    }

    func getCategoryStats() -> [(name: String, count: Int)] {
        Categories.all.map { ($0.title, $0.courses.count) }
    }
}
