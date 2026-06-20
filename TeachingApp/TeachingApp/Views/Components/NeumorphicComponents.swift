import SwiftUI
import UIKit

// MARK: - Neumorphism Color System
struct NeumorphicColors {
    // Light mode colors
    static let background = Color(UIColor { traitCollection in
        switch traitCollection.userInterfaceStyle {
        case .dark:
            return UIColor(red: 0.24, green: 0.25, blue: 0.27, alpha: 1.0)
        case .light, .unspecified:
            return UIColor(red: 0.93, green: 0.94, blue: 0.96, alpha: 1.0)
        @unknown default:
            return UIColor(red: 0.93, green: 0.94, blue: 0.96, alpha: 1.0)
        }
    })
    
    static let primary = Color(UIColor { traitCollection in
        switch traitCollection.userInterfaceStyle {
        case .dark:
            return .white
        case .light, .unspecified:
            return UIColor(red: 0.10, green: 0.10, blue: 0.18, alpha: 1.0)
        @unknown default:
            return UIColor(red: 0.10, green: 0.10, blue: 0.18, alpha: 1.0)
        }
    })
    
    static let secondary = Color(UIColor { traitCollection in
        switch traitCollection.userInterfaceStyle {
        case .dark:
            return UIColor(red: 0.70, green: 0.72, blue: 0.75, alpha: 1.0)
        case .light, .unspecified:
            return UIColor(red: 0.45, green: 0.47, blue: 0.50, alpha: 1.0)
        @unknown default:
            return UIColor(red: 0.45, green: 0.47, blue: 0.50, alpha: 1.0)
        }
    })
    
    static let accent = Color(UIColor { traitCollection in
        switch traitCollection.userInterfaceStyle {
        case .dark:
            return UIColor(red: 0.55, green: 0.63, blue: 0.98, alpha: 1.0)
        default:
            return UIColor(red: 0.40, green: 0.49, blue: 0.95, alpha: 1.0)
        }
    })
    static let accentLight = Color(UIColor { traitCollection in
        switch traitCollection.userInterfaceStyle {
        case .dark:
            return UIColor(red: 0.68, green: 0.74, blue: 0.99, alpha: 1.0)
        default:
            return UIColor(red: 0.55, green: 0.63, blue: 0.97, alpha: 1.0)
        }
    })
    static let success = Color(UIColor { traitCollection in
        switch traitCollection.userInterfaceStyle {
        case .dark:
            return UIColor(red: 0.36, green: 0.82, blue: 0.56, alpha: 1.0)
        default:
            return UIColor(red: 0.22, green: 0.71, blue: 0.44, alpha: 1.0)
        }
    })
    static let warning = Color(UIColor { traitCollection in
        switch traitCollection.userInterfaceStyle {
        case .dark:
            return UIColor(red: 0.98, green: 0.75, blue: 0.30, alpha: 1.0)
        default:
            return UIColor(red: 0.95, green: 0.66, blue: 0.13, alpha: 1.0)
        }
    })
    static let error = Color(UIColor { traitCollection in
        switch traitCollection.userInterfaceStyle {
        case .dark:
            return UIColor(red: 0.95, green: 0.40, blue: 0.42, alpha: 1.0)
        default:
            return UIColor(red: 0.85, green: 0.20, blue: 0.25, alpha: 1.0)
        }
    })
}

// MARK: - Neumorphic Radius Tokens
struct NeumorphicRadius {
    static let small: CGFloat = 10
    static let medium: CGFloat = 12
    static let large: CGFloat = 20
}

// MARK: - Neumorphic Shadow
struct NeumorphicShadow: ViewModifier {
    let size: CGFloat
    let isPressed: Bool
    
    init(size: CGFloat = 15, isPressed: Bool = false) {
        self.size = size
        self.isPressed = isPressed
    }
    
    func body(content: Content) -> some View {
        if isPressed {
            content
                .shadow(color: .black.opacity(0.15), radius: size/3, x: 2, y: 2)
                .shadow(color: .white.opacity(0.7), radius: size/3, x: -2, y: -2)
        } else {
            content
                .shadow(color: .black.opacity(0.12), radius: size, x: size/3, y: size/3)
                .shadow(color: .white.opacity(0.75), radius: size, x: -size/3, y: -size/3)
        }
    }
}

// MARK: - Neumorphic Card
struct NeumorphicCard<Content: View>: View {
    let corners: UIRectCorner
    let isPressed: Bool
    let content: Content
    
    init(
        corners: UIRectCorner = [.allCorners],
        isPressed: Bool = false,
        @ViewBuilder content: () -> Content
    ) {
        self.corners = corners
        self.isPressed = isPressed
        self.content = content()
    }
    
    var body: some View {
        content
            .padding()
            .background(
                NeumorphicBackground(corners: corners, isPressed: isPressed)
            )
            .modifier(NeumorphicShadow(size: 15, isPressed: isPressed))
    }
}

// MARK: - Neumorphic Background
struct NeumorphicBackground: View {
    let corners: UIRectCorner
    let isPressed: Bool
    
    var body: some View {
        RoundedRectangle(cornerRadius: 20, style: .continuous)
            .fill(NeumorphicColors.background)
            .clipShape(CustomRoundedRectangle(corners: corners, cornerRadius: 20))
    }
}

// MARK: - Custom Rounded Rectangle
struct CustomRoundedRectangle: Shape {
    let corners: UIRectCorner
    let cornerRadius: CGFloat
    
    func path(in rect: CGRect) -> Path {
        let path = UIBezierPath(
            roundedRect: rect,
            byRoundingCorners: corners,
            cornerRadii: CGSize(width: cornerRadius, height: cornerRadius)
        )
        return Path(path.cgPath)
    }
}

// MARK: - Neumorphic Button
struct NeumorphicButton: View {
    let title: String
    let icon: String
    let action: () -> Void
    let variant: ButtonVariant
    
    enum ButtonVariant {
        case primary, secondary, pill, circle
    }
    
    var body: some View {
        Button(action: action) {
            switch variant {
            case .primary:
                primaryButton
            case .secondary:
                secondaryButton
            case .pill:
                pillButton
            case .circle:
                circleButton
            }
        }
        .buttonStyle(.plain)
    }
    
    private var primaryButton: some View {
        Text(title)
            .font(.system(size: 16, weight: .semibold))
            .foregroundColor(.white)
            .padding(.horizontal, 24)
            .padding(.vertical, 12)
            .background(
                LinearGradient(
                    colors: [NeumorphicColors.accent, NeumorphicColors.accentLight],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
            .shadow(color: NeumorphicColors.accent.opacity(0.4), radius: 8, x: 0, y: 4)
    }
    
    private var secondaryButton: some View {
        HStack(spacing: 8) {
            Image(systemName: icon)
            Text(title)
        }
        .font(.system(size: 15, weight: .medium))
        .foregroundColor(NeumorphicColors.primary)
        .padding(.horizontal, 20)
        .padding(.vertical, 10)
        .background(NeumorphicColors.background)
        .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
        .modifier(NeumorphicShadow(size: 12))
    }
    
    private var pillButton: some View {
        HStack(spacing: 8) {
            Image(systemName: icon)
            Text(title)
        }
        .font(.system(size: 14, weight: .semibold))
        .foregroundColor(.white)
        .padding(.horizontal, 24)
        .padding(.vertical, 10)
        .background(
            Capsule(style: .continuous)
                .fill(LinearGradient(colors: [NeumorphicColors.accent, NeumorphicColors.accentLight], startPoint: .leading, endPoint: .trailing))
        )
        .shadow(color: NeumorphicColors.accent.opacity(0.3), radius: 6, x: 0, y: 3)
    }
    
    private var circleButton: some View {
        Image(systemName: icon)
            .font(.system(size: 20, weight: .semibold))
            .foregroundColor(NeumorphicColors.primary)
            .frame(width: 44, height: 44)
            .background(NeumorphicColors.background)
            .clipShape(Circle())
            .modifier(NeumorphicShadow(size: 10))
    }
}

// MARK: - Neumorphic Toggle
struct NeumorphicToggle: View {
    let title: String
    @Binding var isOn: Bool
    
    var body: some View {
        HStack(spacing: 12) {
            Text(title)
                .font(.system(size: 16, weight: .medium))
                .foregroundColor(NeumorphicColors.primary)
            
            Spacer()
            
            ZStack(alignment: .leading) {
                RoundedRectangle(cornerRadius: 20, style: .continuous)
                    .fill(NeumorphicColors.background)
                    .frame(width: 52, height: 32)
                    .modifier(NeumorphicShadow(size: 8))
                
                if isOn {
                    Circle()
                        .fill(
                            LinearGradient(
                                colors: [NeumorphicColors.accent, NeumorphicColors.accentLight],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .frame(width: 26, height: 26)
                        .offset(x: 20)
                        .transition(.move(edge: .leading))
                } else {
                    Circle()
                        .fill(NeumorphicColors.secondary)
                        .frame(width: 26, height: 26)
                        .offset(x: -20)
                        .transition(.move(edge: .trailing))
                }
            }
            .animation(.spring(response: 0.3, dampingFraction: 0.6), value: isOn)
        }
    }
}

// MARK: - Neumorphic Slider
struct NeumorphicSlider: View {
    let value: Binding<Double>
    let range: ClosedRange<Double>
    let label: String?
    
    init(_ value: Binding<Double>, in range: ClosedRange<Double> = 0...1, label: String? = nil) {
        self.value = value
        self.range = range
        self.label = label
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            if let label = label {
                Text(label)
                    .font(.caption)
                    .foregroundColor(NeumorphicColors.secondary)
            }
            
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(NeumorphicColors.background)
                        .frame(height: 8)
                        .modifier(NeumorphicShadow(size: 4, isPressed: true))
                    
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(
                            LinearGradient(
                                colors: [NeumorphicColors.accent, NeumorphicColors.accentLight],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .frame(width: sliderWidth(in: geometry))
                    
                    Circle()
                        .fill(.white)
                        .frame(width: 24, height: 24)
                        .shadow(color: .black.opacity(0.15), radius: 4, x: 0, y: 2)
                        .offset(x: thumbOffset(in: geometry))
                        .gesture(
                            DragGesture()
                                .onChanged { gesture in
                                    let newValue = gesture.location.x / geometry.size.width
                                    value.wrappedValue = max(range.lowerBound, min(range.upperBound, range.lowerBound + newValue * (range.upperBound - range.lowerBound)))
                                }
                        )
                }
            }
            .frame(height: 24)
        }
    }
    
    private func sliderWidth(in geometry: GeometryProxy) -> CGFloat {
        let normalizedValue = (value.wrappedValue - range.lowerBound) / (range.upperBound - range.lowerBound)
        return geometry.size.width * CGFloat(normalizedValue)
    }
    
    private func thumbOffset(in geometry: GeometryProxy) -> CGFloat {
        let normalizedValue = (value.wrappedValue - range.lowerBound) / (range.upperBound - range.lowerBound)
        return -12 + geometry.size.width * CGFloat(normalizedValue)
    }
}

// MARK: - Neumorphic Progress Circle
struct NeumorphicProgressCircle: View {
    let progress: Double
    let size: CGFloat
    let strokeWidth: CGFloat
    
    init(_ progress: Double, size: CGFloat = 80, strokeWidth: CGFloat = 8) {
        self.progress = min(1.0, max(0.0, progress))
        self.size = size
        self.strokeWidth = strokeWidth
    }
    
    var body: some View {
        ZStack {
            Circle()
                .stroke(
                    NeumorphicColors.background,
                    lineWidth: strokeWidth
                )
                .modifier(NeumorphicShadow(size: 6, isPressed: true))
                .frame(width: size, height: size)
            
            Circle()
                .trim(from: 0, to: progress)
                .stroke(
                    LinearGradient(
                        colors: [NeumorphicColors.accent, NeumorphicColors.accentLight],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    style: StrokeStyle(lineWidth: strokeWidth, lineCap: .round)
                )
                .rotationEffect(.degrees(-90))
                .frame(width: size, height: size)
                .animation(.easeInOut(duration: 0.5), value: progress)
            
            Text("\(Int(progress * 100))%")
                .font(.system(size: size * 0.25, weight: .bold))
                .foregroundColor(NeumorphicColors.primary)
        }
    }
}

// MARK: - Neumorphic Input Field
struct NeumorphicInputField: View {
    let placeholder: String
    @Binding var text: String
    let isSecure: Bool
    
    init(_ placeholder: String = "", text: Binding<String>, isSecure: Bool = false) {
        self.placeholder = placeholder
        self._text = text
        self.isSecure = isSecure
    }
    
    var body: some View {
        Group {
            if isSecure {
                SecureField(placeholder, text: $text)
            } else {
                TextField(placeholder, text: $text)
            }
        }
        .font(.system(size: 16))
        .foregroundColor(NeumorphicColors.primary)
        .padding()
        .background(NeumorphicColors.background)
        .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
        .modifier(NeumorphicShadow(size: 10, isPressed: true))
        .overlay(
            RoundedRectangle(cornerRadius: 12, style: .continuous)
                .stroke(NeumorphicColors.accent.opacity(text.isEmpty ? 0 : 1), lineWidth: text.isEmpty ? 0 : 2)
                .padding(-1)
        )
    }
}

// MARK: - Neumorphic Tab Bar
struct NeumorphicTabBar: View {
    @Binding var selectedTab: Int
    let tabs: [TabItem]
    
    struct TabItem {
        let icon: String
        let title: String
    }
    
    var body: some View {
        HStack(spacing: 0) {
            ForEach(Array(tabs.enumerated()), id: \.offset) { index, tab in
                Button(action: { selectedTab = index }) {
                    VStack(spacing: 4) {
                        Image(systemName: tab.icon)
                            .font(.system(size: 22))
                        Text(tab.title)
                            .font(.caption2)
                    }
                    .foregroundColor(selectedTab == index ? NeumorphicColors.accent : NeumorphicColors.secondary)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 8)
                    .background(NeumorphicColors.background)
                    if selectedTab == index {
                        Capsule()
                            .fill(NeumorphicColors.accent)
                            .frame(height: 3)
                    }
                }
                .buttonStyle(.plain)
            }
        }
        .background(NeumorphicColors.background)
        .modifier(NeumorphicShadow(size: 15))
        .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))
    }
}

// MARK: - Neumorphic Course Card
struct NeumorphicCourseCard: View {
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
                        .padding(.horizontal, 12)
                        .padding(.vertical, 5)
                        .background(
                            Capsule(style: .continuous)
                                .fill(LinearGradient(colors: [NeumorphicColors.accent, NeumorphicColors.accentLight], startPoint: .leading, endPoint: .trailing))
                        )
                    
                    Spacer()
                    
                    if !course.isRead {
                        Circle()
                            .fill(NeumorphicColors.error)
                            .frame(width: 10, height: 10)
                            .shadow(color: NeumorphicColors.error.opacity(0.4), radius: 4)
                    }
                }
                
                Text(course.title)
                    .font(.headline)
                    .fontWeight(.semibold)
                    .foregroundColor(NeumorphicColors.primary)
                    .lineLimit(2)
                
                HStack(spacing: 12) {
                    Label(formatDate(course.generatedDate), systemImage: "calendar")
                        .font(.caption)
                        .foregroundColor(NeumorphicColors.secondary)
                    
                    if course.progress > 0 && course.progress < 1 {
                        Spacer()
                        NeumorphicProgressCircle(course.progress, size: 32, strokeWidth: 3)
                    }
                }
            }
            .padding()
            .background(NeumorphicColors.background)
            .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))
            .modifier(NeumorphicShadow(size: 15))
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
