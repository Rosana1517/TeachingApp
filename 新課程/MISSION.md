# 學習目標：Vibe Coding 2026 全流程技術棧

## 為什麼要學這個？（Mission）

我已經能使用 Claude Code、Cursor、Codex 等 AI Agent 成功開發出專案項目，但對底層資工程式代碼原理不清楚。專案中調用了哪些功能、為什麼要這樣設定、出了錯該怎麼修——這些都搞不懂。

當 AI 幫你寫代碼時，我不只是「照著做」，而是想真正理解它在做什麼。這樣當 Vibe 破裂（報錯、部署失敗、依賴衝突）時，我能自己判斷問題在哪裡，而不是完全依賴 AI。

**最終目標：** 建立對 2026 獨立開發全流程的直覺理解，達到「日常 Vibe Coding 用到時會用且理解」的程度。不需要精通每一項技術，但要能看懂、能調用、能除錯。

---

## 學習者背景

- 已能使用 AI Agent（Claude Code、Cursor）開發專案
- 對 Node.js、Next.js、Docker、Git 等技術棧缺乏系統性知識
- 不了解 localhost、Port、Event Loop、npm 依賴等底層概念
- 不知道如何從 GitHub 開源項目中取用有價值的代碼整合進自己的專案

## 課程大綱

### 第一階段：The Core（基礎設施與底層邏輯）
1. **Node.js 的角色**：JavaScript 脫離瀏覽器的「引擎」
2. **Localhost 與 Port**：電腦公寓理論，解決 EADDRINUSE 衝突
3. **Git/GitHub 協作**：代碼的時光機
4. **GitHub 寶庫挖掘**：搜索開源項目並讓 AI 提取 Snippet 整合進專案
5. **Package Management（NPM/Bun）**：node_modules 與依賴地圖

### 第二階段：The Shell（前端與 AI 原型）
6. **AI 原型工具**：v0、Bolt、Step1 的快速生成邏輯
7. **Next.js 全家桶**：App Router、SSR vs CSR
8. **UI 組件與設計**：shadcn/ui、Magic UI 的組裝邏輯
9. **資源自動化**：Lucide、Unsplash 的 API 式調用

### 第三階段：The Brain（AI 協作與 MCP）
10. **AI Agents 對比**：Claude Code vs Cline vs Cursor
11. **MCP 協議**：讓 AI 調用 GitHub、瀏覽器與本地工具
12. **自動化流程**：n8n 與 GitHub Actions

### 第四階段：The Soul（數據、存儲與 API）
13. **BaaS 核心（Supabase）**：PostgreSQL 資料庫與數據表設計
14. **向量資料庫（pgvector）**：AI 檢索與 RAG 基礎
15. **緩存與存儲**：Redis 快取與 Cloudflare R2
16. **API 通訊**：Next.js API Routes 與第三方 API 調用流

### 第五階段：The Money（身份認證與商業變現）
17. **身份驗證（Auth）**：Better Auth 與 Clerk 的安全邏輯
18. **支付系統**：Stripe 與 Lemon Squeezy
19. **郵件與通訊**：Resend 郵件發送與通知觸發

### 第六階段：The Shield（運維、監控與分析）
20. **容器化（Docker）**：環境隔離與部署包
21. **部署地圖**：Vercel vs Cloudflare Pages vs Railway
22. **監控與分析**：Sentry、PostHog、Bruno
23. **市場洞察**：Appark 與 Sensor Tower

---

## 教學偏好

- 繁體中文教學
- 一課只教一件事，節奏緊湊
- HTML 課頁面乾淨好看、留白充足、適合截圖
- 每節課結尾帶一個小測驗或手動任務
- 生成課程後提供一條能夠在瀏覽器打開課的命令
