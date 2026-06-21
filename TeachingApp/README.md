# TeachingApp - iOS 教學應用程式

這是一個使用 SwiftUI 開發的 iOS 教學應用程式，具有自動生成和更新教學內容的功能。

## 功能特點

- 📚 自動生成每日教學課程
- 🔔 每日學習提醒通知
- 📊 學習進度追蹤
- 🔍 課程搜索和分類
- 📱 支援 iOS 16.0+
- 🔄 自動從 GitHub 同步最新課程

## 專案結構

```
TeachingApp/
├── .github/
│   └── workflows/
│       ├── build-ios.yml              # iOS 應用程式打包
│       └── generate-lessons.yml       # 每日生成 HTML 教學
├── Support/
│   └── ExportOptions.plist            # IPA 匯出設定
├── TeachingApp/
│   ├── TeachingApp.swift              # App 入口
│   ├── Models/
│   │   ├── Course.swift               # 課程資料模型
│   │   └── Category.swift             # 分類資料模型
│   ├── ViewModels/
│   │   ├── CourseViewModel.swift      # 課程邏輯處理
│   │   └── NotificationViewModel.swift # 通知邏輯處理
│   ├── Views/
│   │   ├── MainTabView.swift          # 主頁面導航
│   │   ├── HomeView.swift             # 首頁
│   │   ├── CategoryView.swift         # 分類頁面
│   │   ├── CourseDetailView.swift     # 課程詳情頁面
│   │   ├── CourseWebView.swift        # HTML 教學內容渲染
│   │   ├── SettingsView.swift         # 設定頁面
│   │   └── Components/                # 自定義 UI 組件
│   └── Services/
│       ├── HTMLScannerService.swift   # HTML 掃描和遠端課程下載
│       ├── ProgressService.swift      # 學習進度持久化
│       └── NotificationService.swift  # 通知管理
├── generate_lesson.py                 # HTML 教學生成腳本
└── lesson-01.html                     # 示例教學檔案
```

## 快速開始

### 1. 在本地開發

1. 使用 Xcode 打開 `TeachingApp.xcodeproj`
2. 選擇你的開發者帳號（免費或付費）
3. 選擇你的 iPhone 作為目標裝置
4. 點擊 Run 按鈕開始開發

### 2. 設定 GitHub Actions

1. 將專案推送到 GitHub 倉庫
2. GitHub Actions 會自動：
   - 編譯 iOS 應用程式
   - 生成 `.ipa` 檔案
   - 上傳到 GitHub Releases
3. 從 GitHub Releases 下載 `.ipa` 檔案
4. 使用 SideStore 或 Diawi 安裝到 iPhone

### 3. 自動生成教學內容

GitHub Actions 會每天自動生成新的 HTML 教學課程：
- 訪問 [generate_lesson.py](generate_lesson.py) 來自定義課程內容
- 修改 `COURSES` 列表來添加更多課程
- Actions 會自動生成新的 HTML 檔案並上傳到 Releases

## 設定說明

### 修改 GitHub 倉庫資訊

在 `HTMLScannerService.swift` 中修改以下設定：

```swift
// GitHub 仓库配置
private let owner = "YOUR_GITHUB_USERNAME"  // 替換成你的 GitHub 用戶名
private let repo = "TeachingApp"           // 你的仓库名
private let accessToken = ""               // 可選：如果有私人仓库需要 token
```

### 自定義課程內容

編輯 `generate_lesson.py` 中的 `COURSES` 列表：

```python
COURSES = [
    {
        "id": 1,
        "title": "課程標題",
        "category": "分類",
        "content": """
# 課程內容
使用 Markdown 格式編寫課程內容
[code]...[/code] 表示程式碼區塊
[note]...[/note] 表示提示
[quiz]問題|選項1|選項2|選項3|選項4|正確答案|解答|D|解釋
""",
        "tags": ["標籤1", "標籤2"]
    },
    # 添加更多課程...
]
```

### 修改通知設定

在 `SettingsView.swift` 中可以調整：
- 通知時間
- 通知天數
- 免打擾時段

## 技術棧

- **SwiftUI** - 使用者介面框架
- **Combine** - 響應式程式設計
- **WebKit** - HTML 渲染
- **GitHub Actions** - 自動化構建和部署
- **Python + Jinja2** - HTML 內容生成

## 依賴項目

- Xcode 15.0+
- iOS 16.0+
- Python 3.11+（用於生成教學內容）
- Jinja2（Python 模板引擎）

## 許可證

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 聯絡方式

如有問題請創建 Issue 或聯絡作者。
