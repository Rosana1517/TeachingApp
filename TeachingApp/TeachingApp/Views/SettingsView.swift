import SwiftUI

struct SettingsView: View {
    @ObservedObject var courseViewModel: CourseViewModel
    @StateObject private var viewModel = NotificationViewModel()
    @State private var showAlert = false
    @State private var alertMessage = ""
    @State private var reminderHour = 9
    @State private var reminderMinute = 0
    @State private var isRefreshing = false

    var body: some View {
        ZStack {
            NeumorphicColors.background.ignoresSafeArea()

            NavigationStack {
                ScrollView {
                    VStack(spacing: 20) {
                        sectionNotification
                        sectionTiming
                        sectionActions
                    }
                    .padding()
                }
                .navigationTitle("設定")
                .alert("提示", isPresented: $showAlert) {
                    Button("確定") {}
                } message: {
                    Text(alertMessage)
                }
                .onAppear {
                    loadSettings()
                }
            }
        }
    }

    private var sectionNotification: some View {
        NeumorphicCard {
            VStack(alignment: .leading, spacing: 16) {
                Text("通知提醒")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(NeumorphicColors.primary)

                NeumorphicToggle(title: "啟用每日提醒", isOn: $viewModel.settings.isEnabled)
                    .onChange(of: viewModel.settings.isEnabled) { newValue in
                        viewModel.saveSettings(
                            hour: viewModel.settings.reminderHour,
                            minute: viewModel.settings.reminderMinute,
                            isEnabled: newValue
                        )
                    }

                VStack(alignment: .leading, spacing: 8) {
                    Text("提醒時間")
                        .font(.subheadline)
                        .foregroundColor(NeumorphicColors.secondary)

                    HStack(spacing: 16) {
                        Picker("時", selection: $reminderHour) {
                            ForEach(0..<24) { hour in
                                Text(String(format: "%02d", hour)).tag(hour)
                            }
                        }
                        .pickerStyle(.wheel)
                        .frame(width: 80)
                        .labelsHidden()

                        Text(":")
                            .font(.title3)
                            .fontWeight(.bold)
                            .foregroundColor(NeumorphicColors.primary)

                        Picker("分", selection: $reminderMinute) {
                            ForEach(Array(stride(from: 0, to: 60, by: 5)), id: \.self) { minute in
                                Text(String(format: "%02d", minute)).tag(minute)
                            }
                        }
                        .pickerStyle(.wheel)
                        .frame(width: 80)
                        .labelsHidden()
                    }
                }
            }
        }
    }

    private var sectionTiming: some View {
        NeumorphicCard {
            VStack(alignment: .leading, spacing: 16) {
                Text("權限")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(NeumorphicColors.primary)

                HStack {
                    Image(systemName: "bell")
                        .font(.title2)
                        .foregroundColor(NeumorphicColors.accent)

                    VStack(alignment: .leading, spacing: 4) {
                        Text("通知權限")
                            .font(.subheadline)
                            .foregroundColor(NeumorphicColors.secondary)

                        HStack(spacing: 6) {
                            Circle()
                                .fill(viewModel.isPermissionGranted ? NeumorphicColors.success : NeumorphicColors.warning)
                                .frame(width: 8, height: 8)

                            Text(viewModel.isPermissionGranted ? "已授權" : "尚未授權")
                                .font(.body)
                                .fontWeight(.medium)
                                .foregroundColor(viewModel.isPermissionGranted ? NeumorphicColors.success : NeumorphicColors.warning)
                        }
                    }
                }

                if !viewModel.isPermissionGranted {
                    Button(action: { viewModel.requestPermission() }) {
                        HStack {
                            Image(systemName: "bell.badge")
                            Text("要求授權")
                        }
                        .font(.system(size: 15, weight: .semibold))
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 10)
                        .background(
                            LinearGradient(
                                colors: [NeumorphicColors.accent, NeumorphicColors.accentLight],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                        .shadow(color: NeumorphicColors.accent.opacity(0.3), radius: 4, x: 0, y: 2)
                    }
                }
            }
        }
    }

    private var sectionActions: some View {
        NeumorphicCard {
            VStack(alignment: .leading, spacing: 16) {
                Text("操作")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(NeumorphicColors.primary)

                Button(action: { refreshLessons() }) {
                    HStack {
                        if isRefreshing {
                            ProgressView()
                                .scaleEffect(0.8)
                        } else {
                            Image(systemName: "arrow.clockwise")
                        }
                        Text(isRefreshing ? "正在重新整理..." : "重新整理課程")
                            .fontWeight(.medium)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption)
                            .foregroundColor(NeumorphicColors.secondary)
                    }
                    .foregroundColor(NeumorphicColors.primary)
                    .padding()
                    .background(NeumorphicColors.background)
                    .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                    .modifier(NeumorphicShadow(size: 8, isPressed: true))
                }
                .buttonStyle(.plain)
                .disabled(isRefreshing)

                Divider()
                    .background(NeumorphicColors.secondary.opacity(0.3))

                Button(action: {
                    ProgressService.shared.resetAll()
                    alertMessage = "本機設定已清除"
                    showAlert = true
                }) {
                    HStack {
                        Image(systemName: "trash")
                        Text("清除本機資料")
                            .fontWeight(.medium)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption)
                            .foregroundColor(NeumorphicColors.error)
                    }
                    .foregroundColor(NeumorphicColors.error)
                    .padding()
                    .background(NeumorphicColors.background)
                    .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                    .modifier(NeumorphicShadow(size: 8, isPressed: true))
                }
                .buttonStyle(.plain)
            }
        }
    }

    private func refreshLessons() {
        isRefreshing = true
        Task {
            await courseViewModel.refresh()
            isRefreshing = false
            if let error = courseViewModel.errorMessage {
                alertMessage = error
            } else {
                alertMessage = courseViewModel.hasNewCourses ? "已找到新課程！" : "目前沒有新課程。"
            }
            showAlert = true
        }
    }

    private func loadSettings() {
        reminderHour = viewModel.settings.reminderHour
        reminderMinute = viewModel.settings.reminderMinute
    }
}
