import SwiftUI
import UIKit

struct CourseDetailView: View {
    let course: Course
    @State private var isRead: Bool
    @State private var showingShareSheet = false
    @Environment(\.dismiss) private var dismiss

    init(course: Course) {
        self.course = course
        self._isRead = State(initialValue: course.isRead)
    }

    var body: some View {
        ZStack {
            NeumorphicColors.background.ignoresSafeArea()

            VStack(spacing: 0) {
                courseHeader

                Divider()
                    .background(NeumorphicColors.secondary.opacity(0.3))

                CourseWebView(course: course)
            }
        }
        .navigationTitle(course.title)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarLeading) {
                Button(action: { dismiss() }) {
                    Image(systemName: "chevron.left")
                        .font(.title3)
                        .foregroundColor(NeumorphicColors.primary)
                }
            }

            ToolbarItem(placement: .navigationBarTrailing) {
                Menu {
                    Button {
                        showingShareSheet = true
                    } label: {
                        Label("分享", systemImage: "square.and.arrow.up")
                    }
                } label: {
                    Image(systemName: "ellipsis.circle")
                        .font(.title3)
                        .foregroundColor(NeumorphicColors.primary)
                }
            }
        }
        .overlay(alignment: .bottomTrailing) {
            Button {
                isRead.toggle()
                if isRead {
                    ProgressService.shared.markAsRead(courseId: course.id)
                } else {
                    ProgressService.shared.markAsUnread(courseId: course.id)
                }
            } label: {
                Image(systemName: isRead ? "checkmark.circle.fill" : "circle")
                    .font(.title2)
                    .foregroundColor(isRead ? NeumorphicColors.success : NeumorphicColors.secondary)
                    .frame(width: 56, height: 56)
                    .background(NeumorphicColors.background)
                    .clipShape(Circle())
                    .modifier(NeumorphicShadow(size: 12))
            }
            .padding()
        }
        .sheet(isPresented: $showingShareSheet) {
            ShareSheet(items: [course.title])
        }
    }

    private var courseHeader: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(course.category)
                    .font(.caption)
                    .fontWeight(.semibold)
                    .foregroundColor(.white)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 5)
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

                Spacer()

                Text(formatDate(course.generatedDate))
                    .font(.caption)
                    .foregroundColor(NeumorphicColors.secondary)
            }

            if let readDate = course.readDate {
                HStack(spacing: 8) {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(NeumorphicColors.success)
                        .font(.caption)

                    Text("已於 \(formatDate(readDate)) 讀過")
                        .font(.caption)
                        .foregroundColor(NeumorphicColors.secondary)
                }
            }
        }
        .padding()
        .background(NeumorphicColors.background)
        .modifier(NeumorphicShadow(size: 10))
        .padding()
    }

    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        formatter.locale = Locale(identifier: "zh_Hant_TW")
        return formatter.string(from: date)
    }
}

struct ShareSheet: UIViewControllerRepresentable {
    let items: [Any]

    func makeUIViewController(context: Context) -> UIActivityViewController {
        UIActivityViewController(activityItems: items, applicationActivities: nil)
    }

    func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {}
}
