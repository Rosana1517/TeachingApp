import SwiftUI
import UIKit

struct CourseCard: View {
    let course: Course
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Text(course.category)
                        .font(.caption)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 4)
                        .background(Color.blue)
                        .clipShape(RoundedRectangle(cornerRadius: 6))
                    
                    Spacer()
                    
                    if !course.isRead {
                        Circle()
                            .fill(Color.red)
                            .frame(width: 8, height: 8)
                    }
                }
                
                Text(course.title)
                    .font(.headline)
                    .fontWeight(.semibold)
                    .lineLimit(2)
                
                HStack {
                    Label(formatDate(course.generatedDate), systemImage: "calendar")
                    if course.progress > 0 && course.progress < 1 {
                        ProgressView(value: course.progress)
                            .scaleEffect(x: 1.2, y: 1.2, anchor: .leading)
                    }
                }
                .font(.caption)
                .foregroundColor(.secondary)
            }
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
        }
        .buttonStyle(.plain)
    }
    
    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
}
