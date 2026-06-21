# 教學 App 專案總結

## 📱 專案概覽

這是一個為 iPhone 設計的教學 App，使用 **SwiftUI** 開發，採用 **Neumorphism（新擬態）** 設計風格。

## ✨ 核心功能

1. **HTML 教學瀏覽** - 在 App 內完整顯示教學內容
2. **分類管理** - 自動依照教學種類分類
3. **每日提醒** - 推送通知提醒你學習
4. **進度追蹤** - 記錄學習進度
5. **Neumorphism 風格** - 柔和立體的全新視覺體驗

## 🎨 設計特色

- **柔和陰影** - 創造立體感而不刺眼
- **溫暖觸感** - 圓角 + 柔和色彩
- **流暢動畫** - 平滑的過渡效果
- **Dark Mode** - 完整的深色模式支援

## 📂 專案結構

```
TeachingApp/
├── TeachingApp/              # Swift 原始碼
│   ├── Models/               # 資料模型
│   ├── Services/             # 服務層
│   ├── ViewModels/           # 視圖模型
│   └── Views/                # 介面層
├── TeachingApp.xcodeproj/    # Xcode 專案文件
├── README.md                 # 專案說明
├── NEUMORPHISM-DESIGN-SYSTEM.md  # 設計規範
├── COMPONENT-GUIDE.md        # 組件展示
└── DESIGN-SUMMARY.md         # 設計總結
```

## 🚀 使用方式

1. 將整個 `TeachingApp` 資料夾複製到 Mac
2. 在 Xcode 中開啟 `TeachingApp.xcodeproj`
3. 選擇你的 iPhone 裝置
4. 按 Run 鍵編譯並執行

## 📖 相關文件

- [README.md](README.md) - 完整安裝和使用說明
- [NEUMORPHISM-DESIGN-SYSTEM.md](NEUMORPHISM-DESIGN-SYSTEM.md) - 設計系統規範
- [COMPONENT-GUIDE.md](COMPONENT-GUIDE.md) - UI 組件展示
- [DESIGN-SUMMARY.md](DESIGN-SUMMARY.md) - 設計完成總結

## 🎯 技術棧

- **框架**: SwiftUI
- **語言**: Swift 5.9+
- **資料儲存**: SwiftData
- **HTML 渲染**: WKWebView
- **通知**: UserNotifications
- **最低版本**: iOS 17.0

## 🎨 設計系統

本專案使用 Neumorphism（新擬態）設計風格，特色：

- 背景色：柔和的淺灰色 (#EDEFF4)
- 強調色：藍紫色漸層 (#667eea → #764ba2)
- 陰影效果：柔和的凸起和凹陷效果
- 圓角：8px - 24px 根據元素類型
- 間距：8pt 網格系統

## 📅 版本資訊

- **版本**: 2.0
- **設計風格**: Neumorphism
- **建立日期**: 2026-06-18
- **狀態**: ✅ 完成並可使用

---

**開發者**: AI Assistant  
**授權**: 個人學習使用
