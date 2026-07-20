# 教學偏好設定

## 語言設定
- 使用繁體中文進行教學

## 教學節奏
- 一課只教一件事，節奏緊湊

## HTML 課頁面規範
- 生成的 HTML 課頁面要乾淨好看、留白充足、適合截圖
- 使用 assets/styles.css 作為共用樣式表
- 使用 assets/quiz-widget.js 作為共用測驗元件
- 每堂課包含：Header、Section、Deep Dive（可展開）、小測驗、任務、推薦延伸閱讀、Follow-up 提醒、導航連結

## 課程結構
- 每一節課結尾帶一個小測驗或手動任務
- 每堂課使用 lessons/0001-<dash-case-name>.html 命名格式
- 參考文件放在 reference/ 目錄
- 學習記錄放在 learning-records/ 目錄

## 自動生成模式
- 參考 TeachingApp/generate_french_lesson.py 的模式
- 使用 LLM API 生成下一堂課內容（JSON Schema）
- GitHub Actions 每日觸發生成新課
- 生成的課程檔名格式：vibe-lesson-{id:02d}.html

## 使用方式
- 生成課程後，提供一條能夠在瀏覽器打開課頁面的命令
