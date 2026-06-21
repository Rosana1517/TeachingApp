# TeachingApp

自動生成法文教學課程的 GitHub Action 工作流程

## 功能

- 每天自動生成精美的法文教學 HTML 課程
- 自動上傳至 GitHub Release
- 支援互動式小測驗和跟練功能
- 繁體中文介面

## 課程內容

目前包含以下課程：

1. **法語課 01** - 法語元音字母與基本發音
2. **法語課 02** - 法語鼻化元音（an, in, on, un）

## 如何新增課程

編輯 `TeachingApp/generate_french_lesson.py` 檔案，在 `LESSONS` 列表中添加新的課程資料。

每個課程包含：
- `id`: 課程編號
- `title`: 課程標題
- `subtitle`: 課程副標題
- `next_topic`: 下一課預告
- `sections`: 課程內容區塊

## GitHub Actions

### 排程設定

預設每天 UTC 時間 01:00 執行（台北時間 09:00）

修改排程：編輯 `.github/workflows/generate-lessons.yml` 中的 `cron` 設定

### 手動觸發

可以在 GitHub Actions 頁面手動觸發工作流程

## 檔案結構

```
.
├── .github/
│   └── workflows/
│       └── generate-lessons.yml  # GitHub Actions workflow
├── TeachingApp/
│   ├── generate_french_lesson.py  # 法文課程生成腳本
│   └── generate_lesson.py  # 原有課程生成腳本（保留）
└── ...
```

## 本地測試

```bash
cd TeachingApp
python generate_french_lesson.py
```

生成的 HTML 檔案會在 `TeachingApp/` 目錄中，可以直接在瀏覽器打開查看。

## 教學偏好

- 使用繁體中文教學
- 一課只教一件事，節奏緊湊
- HTML 課頁面乾淨好看、留白充足、適合截圖
- 每節課結尾帶小測驗或手動任務

## 授權

MIT License
