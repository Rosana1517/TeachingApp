import SwiftUI

struct CategoryBadge: View {
    let name: String
    let count: Int
    let isSelected: Bool
    let onTap: () -> Void

    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 6) {
                Text(name)
                    .font(.subheadline)
                    .fontWeight(isSelected ? .semibold : .medium)

                if count > 0 {
                    Text("\(count)")
                        .font(.caption2)
                        .fontWeight(.bold)
                        .foregroundColor(isSelected ? NeumorphicColors.accent : .white)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(isSelected ? Color.white.opacity(0.9) : NeumorphicColors.secondary.opacity(0.5))
                        .clipShape(Capsule())
                }
            }
            .foregroundColor(isSelected ? .white : NeumorphicColors.primary)
            .padding(.horizontal, 14)
            .padding(.vertical, 8)
            .background(
                Group {
                    if isSelected {
                        Capsule(style: .continuous)
                            .fill(
                                LinearGradient(
                                    colors: [NeumorphicColors.accent, NeumorphicColors.accentLight],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .modifier(NeumorphicShadow(size: 8))
                    } else {
                        Capsule(style: .continuous)
                            .fill(NeumorphicColors.background)
                            .modifier(NeumorphicShadow(size: 8, isPressed: true))
                    }
                }
            )
        }
        .buttonStyle(.plain)
    }
}
