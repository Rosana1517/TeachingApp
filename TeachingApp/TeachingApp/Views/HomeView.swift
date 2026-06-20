import SwiftUI

struct HomeView: View {
    @ObservedObject var viewModel: CourseViewModel
    @State private var navigateToCourse: Course?

    var body: some View {
        NavigationStack {
            ZStack {
                NeumorphicColors.background.ignoresSafeArea()

                ScrollView {
                    VStack(spacing: 20) {
                        if viewModel.isLoading {
                            ProgressView("Loading...")
                                .frame(maxWidth: .infinity, minHeight: 240)
                        } else if let course = viewModel.courses.first {
                            todaySection(course: course)
                        } else {
                            emptyState
                        }

                        unreadSection
                        categoryFilter
                        courseList
                    }
                    .padding()
                }
            }
            .navigationTitle("Home")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    NavigationLink(destination: SettingsView()) {
                        Image(systemName: "gearshape")
                            .font(.title3)
                            .foregroundColor(NeumorphicColors.primary)
                    }
                }
            }
            .sheet(item: $navigateToCourse) { course in
                CourseDetailView(course: course)
            }
        }
    }

    private func todaySection(course: Course) -> some View {
        NeumorphicCard {
            VStack(alignment: .leading, spacing: 16) {
                Text("Today")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(NeumorphicColors.primary)

                HStack {
                    VStack(alignment: .leading, spacing: 8) {
                        Text(course.title)
                            .font(.title3)
                            .fontWeight(.semibold)
                            .foregroundColor(NeumorphicColors.primary)

                        Text(course.category)
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundColor(.white)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 4)
                            .background(
                                Capsule(style: .continuous)
                                    .fill(
                                        LinearGradient(
                                            colors: [NeumorphicColors.accent, NeumorphicColors.accentLight],
                                            startPoint: .leading,
                                            endPoint: .trailing
                                        )
                                    )
                            )
                    }

                    Spacer()

                    Button {
                        navigateToCourse = course
                    } label: {
                        Image(systemName: "arrow.right")
                            .font(.title3)
                            .foregroundColor(NeumorphicColors.accent)
                            .frame(width: 44, height: 44)
                            .background(NeumorphicColors.background)
                            .clipShape(Circle())
                            .modifier(NeumorphicShadow(size: 8))
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding()
        }
    }

    private var emptyState: some View {
        VStack(spacing: 20) {
            Image(systemName: "book.closed")
                .font(.system(size: 60))
                .foregroundColor(NeumorphicColors.accent)
                .frame(width: 120, height: 120)
                .background(NeumorphicColors.background)
                .clipShape(Circle())
                .modifier(NeumorphicShadow(size: 20))

            Text("No lessons found")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(NeumorphicColors.primary)

            Text("Select a folder in Settings and add HTML lesson files.")
                .font(.body)
                .foregroundColor(NeumorphicColors.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 40)
        }
        .frame(maxWidth: .infinity, minHeight: 260)
    }

    private var unreadSection: some View {
        let unreadCount = viewModel.courses.filter { !$0.isRead }.count

        HStack {
            Text("Unread")
                .font(.title3)
                .fontWeight(.bold)
                .foregroundColor(NeumorphicColors.primary)

            Spacer()

            Text("\(unreadCount)")
                .font(.title3)
                .fontWeight(.bold)
                .foregroundColor(NeumorphicColors.accent)
        }
        .padding(.horizontal, 4)
    }

    private var categoryFilter: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                ForEach(viewModel.allCategories.indices, id: \.self) { index in
                    let category = viewModel.allCategories[index]
                    CategoryBadge(
                        name: category,
                        count: category == "All" ? viewModel.courses.count : viewModel.courses.filter { $0.category == category }.count,
                        isSelected: viewModel.selectedCategory == category
                    ) {
                        viewModel.selectedCategory = category
                    }
                }
            }
            .padding(.vertical, 4)
        }
    }

    private var courseList: some View {
        LazyVStack(spacing: 16) {
            ForEach(viewModel.filteredCourses) { course in
                NeumorphicCourseCard(course: course) {
                    navigateToCourse = course
                }
            }
        }
    }
}
