import SwiftUI

struct CategoryView: View {
    @ObservedObject var viewModel: CourseViewModel
    @State private var navigateToCourse: Course?

    var body: some View {
        NavigationStack {
            ZStack {
                NeumorphicColors.background.ignoresSafeArea()

                if Categories.all.isEmpty {
                    emptyState
                } else {
                    categoryListView
                }
            }
            .navigationTitle("分類")
            .sheet(item: $navigateToCourse) { course in
                CourseDetailView(course: course)
            }
        }
    }

    private var categoryListView: some View {
        ScrollView {
            LazyVStack(spacing: 16) {
                ForEach(Categories.all) { category in
                    NavigationLink(destination: categoryCourseList(category.title)) {
                        NeumorphicCard {
                            HStack(spacing: 16) {
                                Image(systemName: category.icon)
                                    .font(.title2)
                                    .foregroundColor(.white)
                                    .frame(width: 44, height: 44)
                                    .background(category.iconColor)
                                    .clipShape(Circle())

                                VStack(alignment: .leading, spacing: 2) {
                                    Text(category.title)
                                        .font(.headline)
                                        .foregroundColor(NeumorphicColors.primary)

                                    Text(category.description)
                                        .font(.caption)
                                        .foregroundColor(NeumorphicColors.secondary)
                                        .lineLimit(1)
                                }

                                Spacer()

                                Text("\(viewModel.courses.filter { $0.category == category.title }.count)")
                                    .font(.subheadline)
                                    .fontWeight(.bold)
                                    .foregroundColor(NeumorphicColors.accent)

                                Image(systemName: "chevron.right")
                                    .font(.caption)
                                    .foregroundColor(NeumorphicColors.secondary)
                            }
                        }
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding()
        }
    }

    private func categoryCourseList(_ category: String) -> some View {
        CourseListView(
            courses: viewModel.courses.filter { $0.category == category },
            onTap: { navigateToCourse = $0 },
            onDelete: { viewModel.deleteCourse($0) }
        )
        .navigationTitle(category)
    }

    private var emptyState: some View {
        VStack(spacing: 20) {
            Image(systemName: "tray")
                .font(.system(size: 60))
                .foregroundColor(NeumorphicColors.accent)
                .frame(width: 120, height: 120)
                .background(NeumorphicColors.background)
                .clipShape(Circle())
                .modifier(NeumorphicShadow(size: 20))

            Text("尚無分類")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(NeumorphicColors.primary)

            Text("到「設定」重新整理，課程會依檔名自動分類顯示。")
                .font(.body)
                .foregroundColor(NeumorphicColors.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 40)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

struct CourseListView: View {
    let courses: [Course]
    let onTap: (Course) -> Void
    var onDelete: ((Course) -> Void)? = nil

    var body: some View {
        ZStack {
            NeumorphicColors.background.ignoresSafeArea()

            ScrollView {
                LazyVStack(spacing: 16) {
                    ForEach(courses) { course in
                        NeumorphicCourseCard(
                            course: course,
                            onTap: { onTap(course) },
                            onDelete: onDelete.map { delete in { delete(course) } }
                        )
                    }
                }
                .padding()
            }
        }
    }
}
