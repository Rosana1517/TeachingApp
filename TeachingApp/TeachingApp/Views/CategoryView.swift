import SwiftUI

struct CategoryView: View {
    @ObservedObject var viewModel: CourseViewModel
    @State private var navigateToCourse: Course?

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.allCategories.count > 1 {
                    courseListView
                } else {
                    emptyState
                }
            }
            .navigationTitle("Categories")
            .sheet(item: $navigateToCourse) { course in
                CourseDetailView(course: course)
            }
        }
    }

    private var courseListView: some View {
        List(Array(viewModel.allCategories.dropFirst()), id: \.self) { category in
            NavigationLink(destination: categoryCourseList(category)) {
                HStack {
                    Image(systemName: "book")
                        .foregroundColor(.blue)

                    Text(category)
                        .font(.headline)

                    Spacer()

                    Text("\(viewModel.courses.filter { $0.category == category }.count)")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
        }
    }

    private func categoryCourseList(_ category: String) -> some View {
        CourseListView(courses: viewModel.courses.filter { $0.category == category }) { course in
            navigateToCourse = course
        }
        .navigationTitle(category)
    }

    private var emptyState: some View {
        VStack(spacing: 16) {
            Image(systemName: "tray")
                .font(.system(size: 50))
                .foregroundColor(.gray)

            Text("No categories yet")
                .font(.headline)

            Text("Add lessons to see them grouped by category.")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

struct CourseListView: View {
    let courses: [Course]
    let onTap: (Course) -> Void

    var body: some View {
        List(courses) { course in
            CourseCard(course: course) {
                onTap(course)
            }
            .listRowInsets(EdgeInsets(top: 4, leading: 16, bottom: 4, trailing: 16))
        }
        .listStyle(.plain)
    }
}
