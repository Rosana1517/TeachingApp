import SwiftUI

struct MainTabView: View {
    @StateObject private var courseViewModel = CourseViewModel()
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView(viewModel: courseViewModel)
                .tabItem {
                    Label("首頁", systemImage: "house")
                }
                .tag(0)
            
            CategoryView(viewModel: courseViewModel)
                .tabItem {
                    Label("分類", systemImage: "folder")
                }
                .tag(1)
            
            SettingsView(courseViewModel: courseViewModel)
                .tabItem {
                    Label("設定", systemImage: "gearshape")
                }
                .tag(2)
        }
        .onAppear {
            courseViewModel.loadCourses()
        }
    }
}
