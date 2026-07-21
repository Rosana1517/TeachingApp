# Vibe Coding 2026：從零到全球產品的技術棧大綱

## 學習目標
建立對 2026 獨立開發全流程的「直覺理解」。不求精通每一行代碼，但求在 AI Agent (Claude Code/Cursor) 執行任務時，你能聽懂它在做什麼，並在出錯時知道如何調整「Vibe」。

---

## 課程邏輯架構

### 第一階段：The Core (基礎設施與底層邏輯)
*這是你的開發環境，是所有代碼運行的舞台。*
1. **Node.js 的角色**：JavaScript 脫離瀏覽器的「引擎」。
2. **Localhost 與 Port (連接埠)**：電腦公寓理論，解決 EADDRINUSE (打架) 衝突。
3. **Git/GitHub 協作**：代碼的時光機，理解 AI 是如何處理分支與提交的。
4. **GitHub 寶庫挖掘**：如何精準搜索開源項目，並讓 AI 提取有價值的代碼塊（Snippet）整合進專案。
5. **Package Management (NPM/Bun)**：理解 `node_modules` 與依賴地圖。

### 第二階段：The Shell (前端與 AI 原型)
*如何利用 AI 快速把想法具現化為用戶能看到的介面。*
6. **AI 原型工具**：v0, Bolt, Step1 的快速生成邏輯。
7. **Next.js 全家桶**：App Router, SSR vs CSR 的直覺理解。
8. **UI 組件與設計**：shadcn/ui, Magic UI 的組裝邏輯與 Figma 轉代碼。
9. **資源自動化**：Lucide (圖標)、Unsplash (圖片) 的 API 式調用。

### 第三階段：The Brain (AI 協作與 MCP)
*深度發揮 AI Agent 的能力，讓 AI 擁有更強的工具調用權。*
10. **AI Agents 對比**：Claude Code vs Cline vs Cursor 的擅長領域。
11. **MCP 協議 (Model Context Protocol)**：如何讓 AI 調用 GitHub、瀏覽器與本地工具。
12. **自動化流程**：n8n 與 GitHub Actions 的結合，實現開發自動化。

### 第四階段：The Soul (數據、存儲與 API)
*處理數據的存儲、流轉與 AI 檢索邏輯。*
13. **BaaS 核心 (Supabase)**：PostgreSQL 資料庫與數據表的設計思維。
14. **向量資料庫 (pgvector)**：AI 檢索與 RAG 的基礎原理。
15. **緩存與存儲**：Redis 快取邏輯與 Cloudflare R2 對象存儲。
16. **API 通訊**：Next.js API Routes 與第三方 API (Resend, Stripe) 的調用流。

### 第五階段：The Money (身份認證與商業變現)
*將專案轉化為可盈利的產品。*
17. **身份驗證 (Auth)**：Better Auth 與 Clerk 的安全邏輯。
18. **支付系統**：Stripe 與 Lemon Squeezy 的訂閱與結帳流程。
19. **郵件與通訊**：Resend 郵件發送與通知觸發邏輯。

### 第六階段：The Shield (運維、監控與分析)
*確保產品穩定運行，並根據數據持續優化。*
20. **容器化 (Docker)**：為什麼「在 AI 那裡會動」但在部署時不動？
21. **部署地圖**：Vercel vs Cloudflare Pages vs Railway。
22. **監控與分析**：Sentry (抓 Bug)、PostHog (看用戶行為)、Bruno (調試 API)。
23. **市場洞察**：Appark 與 Sensor Tower 的數據驅動決策。

---

## 課程細化大綱

本大綱將上述 23 堂課，依照「核心概念、AI 調用邏輯、實戰任務」三維度進行細化。

### 第一階段：The Core (基礎設施)

#### L01: Node.js 的角色
- **核心**: JS 的脫離瀏覽器執行環境。
- **邏輯**: 為什麼 AI 需要 Node 才能執行 `npm install`？
- **任務**: 檢查電腦的 Node 版本與環境路徑。

#### L02: Localhost 與 Port (連接埠)
- **核心**: 本地伺服器公寓理論。
- **邏輯**: EADDRINUSE (打架) 發生時，AI 是如何幫你「換房」的。
- **任務**: 啟動一個服務並手動指定不同 Port。

#### L03: Git/GitHub 協作
- **核心**: 版本控制與雲端同步。
- **邏輯**: 理解 AI 的 `git commit` 邏輯與 `push` 到雲端的流程。
- **任務**: 建立一個 Repo 並完成第一次 Push。

#### L04: GitHub 寶庫挖掘
- **核心**: 精準搜索與 Snippet 提取。
- **邏輯**: 如何將 GitHub 上的開源功能「餵」給 AI Agent 並整合進你的專案。
- **任務**: 找一個開源組件並讓 AI 遷移到你的專案中。

#### L05: Package Management (NPM/Bun)
- **核心**: 依賴地圖與 `package.json`。
- **邏輯**: 當依賴衝突時，AI 是如何修改 `package-lock.json` 修復問題的。
- **任務**: 練習安裝與卸載依賴，觀察檔案變化。

---

### 第二階段：The Shell (前端與 AI 原型)

#### L06: AI 原型工具 (v0/Bolt)
- **核心**: 從 Prompt 到 UI 的瞬間轉化。
- **邏輯**: 理解 v0 生成代碼的組件化思維。
- **任務**: 生成一個 Landing Page 並導出到本地。

#### L07: Next.js 全家桶
- **核心**: App Router 與渲染機制。
- **邏輯**: `use client` vs `server component` 在 Vibe Coding 中的標記邏輯。
- **任務**: 建立一個包含 API Routes 的 Next.js 基本架構。

#### L08: UI 組件與設計 (shadcn/ui)
- **核心**: 組件組裝與 Tailwind CSS。
- **邏輯**: 為什麼 AI 喜歡 shadcn？理解「複製代碼而非安裝插件」的優勢。
- **任務**: 使用 shadcn 快速搭建一個註冊頁面。

#### L09: 資源自動化 (Icons/Images)
- **核心**: Lucide 與 Unsplash API。
- **邏輯**: 如何讓 AI 根據主題自動挑選正確的 Icon 與占位圖。
- **任務**: 建立一個動態 Icon 列表頁面。

---

### 第三階段：The Brain (AI 協作與 MCP)

#### L10: AI Agents 對比
- **核心**: Claude Code vs Cursor 的場景選擇。
- **邏輯**: 什麼時候該用終端機 Agent，什麼時候該用 IDE Agent？
- **任務**: 在同一任務下對比兩個 Agent 的執行效率。

#### L11: MCP 協議深度解析
- **核心**: Model Context Protocol。
- **邏輯**: 如何讓 AI 獲得「手」來操作你的瀏覽器或 GitHub。
- **任務**: 啟動一個 Browser MCP 讓 AI 幫你爬取資料。

#### L12: 自動化流程 (n8n)
- **核心**: 流程自動化。
- **邏輯**: 串接 GitHub Actions，實現「代碼提交 -> 自動測試 -> 自動部署」。
- **任務**: 搭建一個簡單的自動化觸發流。

---

### 第四階段：The Soul (數據與 API)

#### L13: BaaS 核心 (Supabase)
- **核心**: 雲端資料庫與表結構。
- **邏輯**: 理解 AI 如何撰寫 SQL 並在 Supabase 中執行。
- **任務**: 建立一個 User Profile 表並實現 CRUD。

#### L14: 向量資料庫 (pgvector)
- **核心**: 向量檢索與 RAG 基礎。
- **邏輯**: AI 是如何從幾千個檔案中「搜尋」出相關內容的。
- **任務**: 在 Supabase 中開啟 pgvector 並進行簡單的語義搜索。

#### L15: 緩存與存儲 (Redis/R2)
- **核心**: 效能優化與對象存儲。
- **邏輯**: 為什麼圖片要放 R2 而不是放資料庫？
- **任務**: 上傳一張圖片到 Cloudflare R2 並獲得訪問連結。

#### L16: API 通訊與第三方整合
- **核心**: API Routes 與 Webhooks。
- **邏輯**: 理解 API 調用時的 Request 與 Response 結構。
- **任務**: 整合一個天氣 API 並在頁面顯示。

---

### 第五階段：The Money (商業變現)

#### L17: 身份驗證 (Better Auth)
- **核心**: 安全認證流程。
- **邏輯**: 理解 OAuth (Google/GitHub 登入) 的跳轉與權限邏輯。
- **任務**: 實現一個完整的登入/登出功能。

#### L18: 支付系統 (Stripe)
- **核心**: 訂閱制與結帳。
- **邏輯**: 理解 Stripe Checkout 與 Webhook 的非同步通知。
- **任務**: 在測試模式下完成一筆虛擬訂單。

#### L19: 郵件通訊 (Resend)
- **核心**: 交易性郵件發送。
- **邏輯**: 為什麼 AI 需要 Resend API 而不是 SMTP？
- **任務**: 發送一封包含動態內容的歡迎郵件。

---

### 第六階段：The Shield (運維與分析)

#### L20: 容器化 (Docker)
- **核心**: 環境隔離與部署包。
- **邏輯**: 理解 `Dockerfile` 如何定義「代碼的生存環境」。
- **任務**: 將一個簡單的專案打包成 Docker Image。

#### L21: 部署地圖 (Vercel/CF)
- **核心**: 全球部署。
- **邏輯**: 理解 CDN 與 Edge Functions 的執行位置。
- **任務**: 將專案部署到 Vercel 並設定自定義域名。

#### L22: 監控與分析 (PostHog)
- **核心**: 錯誤監控與用戶行為。
- **邏輯**: 如何在 Vibe Coding 過程中利用數據發現「Vibe 破裂」的地方。
- **任務**: 埋入一個按鈕點擊事件並在後台查看。

#### L23: 市場洞察與決策
- **核心**: 數據驅動開發。
- **邏輯**: 獨立開發者如何利用數據判斷下一個 Feature 該做什麼。
- **任務**: 撰寫一份簡單的產品數據分析報告。

---

## 教學偏好與規範
- **語言**：繁體中文。
- **節奏**：一課一事，專注於「調用邏輯」而非「語法細節」。
- **頁面**：HTML 乾淨美觀、留白充足、適合截圖。
- **互動**：每課結尾必帶一個實戰任務或小測驗。
- **交付**：提供直接在瀏覽器開啟的 `start` 命令。
