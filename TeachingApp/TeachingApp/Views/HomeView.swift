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
                            ProgressView("載入中...")
                                .frame(maxWidth: .infinity, minHeight: 240)
                        } else if let course = viewModel.unlearnedCourses.first ?? viewModel.filteredCourses.first {
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
            .navigationTitle("首頁")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    NavigationLink(destination: SettingsView(courseViewModel: viewModel)) {
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
                Text("今日課程")
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

            Text("尚無課程")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(NeumorphicColors.primary)

            Text("到「設定」頁面點選重新整理，即可同步最新課程。")
                .font(.body)
                .foregroundColor(NeumorphicColors.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 40)
        }
        .frame(maxWidth: .infinity, minHeight: 260)
    }

    private var unreadSection: some View {
        HStack {
            Text("未學習")
                .font(.title3)
                .fontWeight(.bold)
                .foregroundColor(NeumorphicColors.primary)

            Spacer()

            Text("\(viewModel.unlearnedCourses.count)")
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
                        count: category == "全部" ? viewModel.courses.count : viewModel.courses.filter { $0.category == category }.count,
                        isSelected: viewModel.selectedCategory == category
                    ) {
                        viewModel.selectedCategory = category
                    }
                }
            }
            .padding(.vertical, 4)
        }
    }

    @State private var showLearned = false

    private var courseList: some View {
        LazyVStack(spacing: 16) {
            ForEach(viewModel.unlearnedCourses) { course in
                NeumorphicCourseCard(
                    course: course,
                    onTap: { navigateToCourse = course },
                    onToggleLearned: { viewModel.toggleLearned(course: course) },
                    onDelete: { viewModel.deleteCourse(course) }
                )
            }

            if !viewModel.learnedCourses.isEmpty {
                learnedSection
            }
        }
    }

    private var learnedSection: some View {
        VStack(spacing: 12) {
            Button {
                withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                    showLearned.toggle()
                }
            } label: {
                HStack {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(NeumorphicColors.success)
                    Text("已學習")
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(NeumorphicColors.primary)
                    Spacer()
                    Text("\(viewModel.learnedCourses.count)")
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(NeumorphicColors.success)
                    Image(systemName: showLearned ? "chevron.up" : "chevron.down")
                        .font(.caption)
                        .foregroundColor(NeumorphicColors.secondary)
                }
                .padding(.horizontal, 4)
            }
            .buttonStyle(.plain)

            if showLearned {
                ForEach(viewModel.learnedCourses) { course in
                    NeumorphicCourseCard(
                        course: course,
                        onTap: { navigateToCourse = course },
                        onToggleLearned: { viewModel.toggleLearned(course: course) },
                        onDelete: { viewModel.deleteCourse(course) }
                    )
                }
            }
        }
    }
}
