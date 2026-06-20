# iPhone 教學 App 開發計畫

## Summary

設計並開發一款 iOS App，讓用戶可以在 iPhone 上閱讀每日自動生成的教學 HTML 檔案，具備分類瀏覽、學習提醒功能，並提供流暢的行動端閱讀體驗。

---

## Current State Analysis

### 現狀
- **位置**: `c:\Users\Tong\Desktop\Project 2\教學\`
- **內容**: 教學 HTML 檔案（範例：`lesson-01.html` — 法語課 01）
- **檔案格式**: 單一完整 HTML 檔案，包含 CSS + JavaScript，獨立可讀
- **課程結構**: 每課包含標題、課程介紹、核心知識區塊、跟練區、測驗區、任務區
- **語言**: 繁體中文
- **現有課程種**: 法語入門（至少一個分類）
- **自動化**: HTML 每日自動生成（生成機制在專案外）

### 現有 HTML 結構特徵
- 使用 `lang="zh-Hant"`
- `<title>` 格式：`法語課 01 — 法語元音字母與基本發音`
- 標題格式：`LEÇON 01`（在 `.lesson-number` 元素中）
- 章節：`<h1>` 為課程標題，`.section-title` 為各節標題
- 包含互動元素：測驗按鈕 (`checkAnswer`)、答案顯示 (`revealAnswer`)

---

## Requirements

### 核心功能
1. **HTML 教學瀏覽**: 在 App 內渲染並顯示 HTML 教學檔案內容
2. **分類管理**: 依照教學種類（如：法語、日語、程式設計等）分類瀏覽
3. **每日提醒**: 自動推送通知提醒用戶學習
4. **每日更新**: 自動讀取最新生成的 HTML 檔案
5. **進度追蹤**: 記錄已讀/未讀課程

### 使用者體驗
- 支援 Dark Mode
- 適合手機閱讀的字型大小與排版
- 流暢的頁面切換與載入速度
- 離線可用（下載後可離線閱讀）

---

## Technical Architecture

### 開發技術選擇

| 層級 | 技術 | 理由 |
|------|------|------|
| 框架 | **SwiftUI** | Apple 官方現代 UI 框架，適合 iOS 15+ |
| 語言 | **Swift 5.9+** | 穩定、效能好、支援 Swift Concurrency |
| 儲存 | **SwiftData** | iOS 17+ 內建資料框架，替代 CoreData |
| 通知 | **UserNotifications** | Apple 官方推送通知 API |
| HTML 渲染 | **WKWebView** | 完整支援 JS + CSS，完美還原 HTML 內容 |
| 本地儲存 | **File System** | 讀取本機資料夾的 HTML 檔案 |
| 最低版本 | **iOS 17.0** | SwiftData + 現代 API 支援 |

### 資料架構

```
教學 App Data Model
├── Course (課程)
│   ├── id: UUID
│   ├── title: String          // 例：法語課 01
│   ├── category: String       // 例：法語
│   ├── fileName: String       // 例：lesson-01.html
│   ├── filePath: String       // 本機路徑
│   ├── generatedDate: Date    // 生成日期
│   ├── isRead: Bool           // 是否已讀
│   ├── readDate: Date?        // 最後閱讀時間
│   └── progress: Double       // 閱讀進度 (0.0 - 1.0)
├── Category (分類)
│   ├── id: UUID
│   ├── name: String           // 例：法語
│   ├── icon: String           // SF Symbol 名稱
│   └── sortOrder: Int         // 排序順序
└── NotificationSettings
    ├── isEnabled: Bool
    ├── reminderTime: Date     // 每日提醒時間
    └── daysOfWeek: [Int]      // 提醒的星期幾
```

---

## Project Structure

```
TeachingApp/
├── TeachingApp.xcodeproj
├── TeachingApp/
│   ├── TeachingApp.swift              // App 入口
│   ├── Models/
│   │   ├── Course.swift               // 課程資料模型
│   │   ├── Category.swift             // 分類資料模型
│   │   └── NotificationSettings.swift // 通知設定
│   ├── Services/
│   │   ├── HTMLScannerService.swift   // 掃描本機 HTML 檔案
│   │   ├── NotificationService.swift  // 管理推送通知
│   │   └── ProgressService.swift      // 進度追蹤
│   ├── Views/
│   │   ├── MainTabView.swift          // 主標籤頁導航
│   │   ├── HomeView.swift             // 首頁（今日課程）
│   │   ├── CategoryView.swift         // 分類瀏覽頁
│   │   ├── CourseListView.swift       // 課程列表
│   │   ├── CourseDetailView.swift     // 課程詳情（WKWebView）
│   │   ├── SettingsView.swift         // 設定頁
│   │   └── Components/
│   │       ├── CourseCard.swift       // 課程卡片
│   │       └── CategoryBadge.swift    // 分類標籤
│   ├── ViewModels/
│   │   ├── CourseViewModel.swift      // 課程資料管理
│   │   └── NotificationViewModel.swift // 通知管理
│   └── Assets.xcassets/
│       ├── AccentColor.colorset
│       └── AppIcon.appiconset
└── TeachingAppTests/
```

---

## Implementation Steps

### Step 1: 建立 Xcode 專案
- 建立新的 SwiftUI 專案
- 設定最低版本為 iOS 17.0
- 啟用 SwiftData
- 設定 App ID 與名稱（建議：教學、Learning Log 等）

### Step 2: 建立資料模型 (SwiftData)
- 建立 `Course` Model，包含所有必要欄位
- 建立 `Category` Model，支援自訂分類
- 建立 `NotificationSettings` Model
- 設定 SwiftData 內容容器 (ModelContainer)

### Step 3: 開發 HTML 掃描服務
- 讀取指定資料夾中的所有 `.html` 檔案
- 解析 HTML 檔案標題（從 `<title>` 或 `<h1>` 標籤）
- 從檔名或路徑自動提取課程編號與分類
- 更新課程狀態（已讀/未讀）

```swift
func scanHTMLFiles(in folderURL: URL) -> [Course] {
    // 1. 取得所有 .html 檔案
    // 2. 使用 String 處理解析標題（輕量方式）
    // 3. 自動偵測分類（從資料夾名稱或檔名前綴）
    // 4. 回傳 Course 陣列
}
```

### Step 4: 開發 HTML 渲染器
- 使用 `WKWebView` 載入本地 HTML 檔案
- 調整 viewport 設定，確保手機閱讀體驗良好
- 支援 JavaScript 互動功能（測驗、答案顯示）
- 追蹤閱讀進度（透過 WebView message handler）
- 啟用 Dark Mode 支援

```swift
class CourseWebView: UIViewRepresentable {
    let htmlURL: URL
    
    func makeUIView(context: Context) -> WKWebView
    func updateUIView(_ uiView: WKWebView, context: Context)
}
```

### Step 5: 開發首頁（今日課程）
- 顯示今日最新生成的課程
- 顯示未讀課程數量
- 快速進入按鈕
- 每日自動更新（App 啟動時重新掃描）

```swift
struct HomeView: View {
    @Environment(\.modelContext) private var context
    
    var body: some View {
        NavigationStack {
            ScrollView {
                // 今日課程卡片
                // 未讀課程提醒
                // 快速分類入口
            }
        }
    }
}
```

### Step 6: 開發分類瀏覽
- 左側分類側邊欄 / 右側課程列表
- 支援篩選與排序
- 每個分類顯示課程數量
- 支援自訂分類名稱與圖示

### Step 7: 開發課程詳情頁
- `CourseDetailView` 包含 `CourseWebView`
- 顯示課程基本資訊（標題、日期、分類）
- 顯示閱讀進度條
- 標記為已讀按鈕
- 分享功能（分享 HTML 檔案）

### Step 8: 開發通知系統
- 請求通知權限
- 設定每日提醒時間
- 使用 `UNTimeIntervalNotificationTrigger` 進行每日觸發
- 顯示自訂通知內容（課程標題、鼓勵訊息）
- 支援靜音時段設定

```swift
class NotificationService {
    static func scheduleDailyReminder(at time: Date) {
        // 1. 建立 notification request
        // 2. 設定每日 trigger
        // 3. 加入 notification center
    }
    
    static func sendTodayCourseNotification(courseTitle: String) {
        // 建立內容並發送
    }
}
```

### Step 9: 開發設定頁
- 每日提醒時間設定
- 通知開關
- 提醒日期選擇
- 顯示本機 HTML 檔案路徑
- 手動重新掃描按鈕
- 主題設定（淺色/深色/自動）

### Step 10: 優化與測試
- 測試不同 HTML 檔案的渲染
- 測試通知功能
- 測試離線模式
- 效能優化（大量檔案時的載入速度）
- 新增支援（手動添加課程）

---

## File Path Configuration

- **預設 HTML 資料夾路徑**: 使用 Documents 資料夾
- 使用者可在設定中自訂路徑
- 首次啟動時顯示路徑設定畫面
- 支援同步到 iCloud Drive（可選）

---

## Assumptions & Decisions

| 決策 | 選擇 | 理由 |
|------|------|------|
| 開發框架 | SwiftUI | 原生 iOS、開發效率高 |
| iOS 版本 | iOS 17+ | SwiftData 需求 |
| HTML 解析 | String 處理 | 不需要重量級 HTML 解析器 |
| 資料同步 | 僅本機 | 簡化架構，如需雲端可後續新增 |
| 分類方式 | 自動偵測 + 手動修正 | 平衡便利與彈性 |
| 通知機制 | 本地推送 | 不需要後端伺服器 |

---

## Verification Steps

1. **HTML 渲染測試**
   - 開啟 `lesson-01.html`，確認所有內容正確顯示
   - 確認 JavaScript 互動功能運作（測驗、查看答案）
   - 確認 Dark Mode 下文字可讀

2. **分類功能測試**
   - 新增不同分類的 HTML 檔案
   - 確認分類正確顯示
   - 確認篩選功能正常

3. **通知功能測試**
   - 設定提醒時間
   - 確認通知按時推送
   - 確認點擊通知可跳轉到課程

4. **進度追蹤測試**
   - 開啟課程後確認進度更新
   - 確認已讀/未讀狀態正確

5. **效能測試**
   - 載入 50+ 課程時的反應速度
   - 記憶體使用情況

---

## 預計開發時間（參考）

- 基礎架構與資料模型：1-2 天
- HTML 掃描與渲染：1-2 天
- 主要 UI（首頁、分類、詳情）：2-3 天
- 通知系統：1 天
- 設定與優化：1 天
- **總計：6-9 個工作天**

---

## Next Steps

1. 確認此計畫符合需求
2. 開始建立 Xcode 專案
3. 依序實作各模組
