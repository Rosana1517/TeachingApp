import SwiftUI
import UIKit
import UniformTypeIdentifiers

struct SettingsView: View {
    @StateObject private var viewModel = NotificationViewModel()
    @State private var htmlFolderPath: String = ""
    @State private var showFolderPicker = false
    @State private var showAlert = false
    @State private var alertMessage = ""
    @State private var reminderHour = 9
    @State private var reminderMinute = 0

    var body: some View {
        ZStack {
            NeumorphicColors.background.ignoresSafeArea()

            NavigationStack {
                ScrollView {
                    VStack(spacing: 20) {
                        sectionFolder
                        sectionNotification
                        sectionTiming
                        sectionActions
                    }
                    .padding()
                }
                .navigationTitle("Settings")
                .toolbar {
                    ToolbarItem(placement: .navigationBarLeading) {
                        Button(action: {}) {
                            Image(systemName: "chevron.left")
                                .font(.title3)
                                .foregroundColor(NeumorphicColors.primary)
                        }
                    }
                }
                .sheet(isPresented: $showFolderPicker) {
                    FolderPickerView(selectedPath: $htmlFolderPath)
                }
                .alert("Notice", isPresented: $showAlert) {
                    Button("OK") {}
                } message: {
                    Text(alertMessage)
                }
                .onAppear {
                    loadSettings()
                }
            }
        }
    }

    private var sectionFolder: some View {
        NeumorphicCard {
            VStack(alignment: .leading, spacing: 16) {
                Text("HTML Folder")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(NeumorphicColors.primary)

                HStack {
                    Image(systemName: "folder")
                        .font(.title2)
                        .foregroundColor(NeumorphicColors.accent)

                    VStack(alignment: .leading, spacing: 4) {
                        Text(htmlFolderPath.isEmpty ? "No folder selected" : htmlFolderPath)
                            .font(.body)
                            .foregroundColor(htmlFolderPath.isEmpty ? NeumorphicColors.secondary : NeumorphicColors.primary)

                        Text("Pick a folder containing lesson HTML files.")
                            .font(.caption)
                            .foregroundColor(NeumorphicColors.secondary)
                    }
                }

                Button(action: { showFolderPicker = true }) {
                    HStack {
                        Image(systemName: "plus.circle.fill")
                        Text("Choose Folder")
                    }
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 12)
                    .background(
                        LinearGradient(
                            colors: [NeumorphicColors.accent, NeumorphicColors.accentLight],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                    .shadow(color: NeumorphicColors.accent.opacity(0.3), radius: 6, x: 0, y: 3)
                }
            }
        }
    }

    private var sectionNotification: some View {
        NeumorphicCard {
            VStack(alignment: .leading, spacing: 16) {
                Text("Notifications")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(NeumorphicColors.primary)

                NeumorphicToggle(title: "Enable reminders", isOn: $viewModel.settings.isEnabled)
                    .onChange(of: viewModel.settings.isEnabled) { newValue in
                        viewModel.saveSettings(
                            hour: viewModel.settings.reminderHour,
                            minute: viewModel.settings.reminderMinute,
                            isEnabled: newValue
                        )
                    }

                VStack(alignment: .leading, spacing: 8) {
                    Text("Reminder time")
                        .font(.subheadline)
                        .foregroundColor(NeumorphicColors.secondary)

                    HStack(spacing: 16) {
                        Picker("Hour", selection: $reminderHour) {
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

                        Picker("Minute", selection: $reminderMinute) {
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
                Text("Permission")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(NeumorphicColors.primary)

                HStack {
                    Image(systemName: "bell")
                        .font(.title2)
                        .foregroundColor(NeumorphicColors.accent)

                    VStack(alignment: .leading, spacing: 4) {
                        Text("Notification access")
                            .font(.subheadline)
                            .foregroundColor(NeumorphicColors.secondary)

                        HStack(spacing: 6) {
                            Circle()
                                .fill(viewModel.isPermissionGranted ? NeumorphicColors.success : NeumorphicColors.warning)
                                .frame(width: 8, height: 8)

                            Text(viewModel.isPermissionGranted ? "Granted" : "Not granted")
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
                            Text("Request Permission")
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
                Text("Actions")
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(NeumorphicColors.primary)

                Button(action: {
                    alertMessage = "Refresh lesson list"
                    showAlert = true
                }) {
                    HStack {
                        Image(systemName: "arrow.clockwise")
                        Text("Refresh")
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

                Divider()
                    .background(NeumorphicColors.secondary.opacity(0.3))

                Button(action: {
                    ProgressService.shared.resetAll()
                    alertMessage = "Local settings cleared"
                    showAlert = true
                }) {
                    HStack {
                        Image(systemName: "trash")
                        Text("Clear Local Data")
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

    private func loadSettings() {
        htmlFolderPath = ""
        reminderHour = viewModel.settings.reminderHour
        reminderMinute = viewModel.settings.reminderMinute
    }
}

struct FolderPickerView: UIViewControllerRepresentable {
    @Binding var selectedPath: String
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [.folder])
        picker.allowsMultipleSelection = false
        picker.delegate = context.coordinator
        return picker
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}

    final class Coordinator: NSObject, UIDocumentPickerDelegate {
        let parent: FolderPickerView

        init(_ parent: FolderPickerView) {
            self.parent = parent
        }

        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            guard let url = urls.first else { return }
            parent.selectedPath = url.path
            parent.dismiss()
        }
    }
}
