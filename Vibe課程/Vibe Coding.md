# Vibe Coding 2026：從零到全球產品的技術棧大綱

## 學習目標
建立對 2026 獨立開發全流程的「直覺理解」。不求精通每一行代碼，但求在 AI Agent (Claude Code/Cursor) 執行任務時，你能聽懂它在做什麼，並在出錯時知道如何調整「Vibe」。

**2026-07 改版說明**：本版大幅加深「第三階段：The Brain」，参考兩本開源 AI Agent 技術書籍的章節架構重新設計 —— 《AI Agent 实战：从原理到落地》(bojieli/ai-agent-book) 與《AI Agents From Zero》(didilili/ai-agents-from-zero)。這兩本書把 Claude Code、Cursor 這類工具背後「Agent = LLM + 上下文 + 工具」的設計原理講得很透徹，過去的大綱只停留在「工具比較」層級，現在補上上下文工程、記憶系統、工具設計、MCP、RAG、Agent 評估、多 Agent 協作等實際運作邏輯，讓你不只會用，還能看懂「為什麼 AI 這樣設計」。

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

### 第三階段：The Brain (AI Agent 架構與協作) 🆕 全面加深
*不只是「比較工具」，而是拆開 Agent 的引擎蓋，看懂 Claude Code/Cursor 背後真正在做什麼。*
10. **AI Agents 對比**：Claude Code vs Cline vs Cursor 的擅長領域。
11. **Agent 核心公式**：Agent = LLM + 上下文 + 工具，三層拆解 Harness 的運作方式。
12. **上下文工程 (Context Engineering)**：系統指令、工具說明、對話歷史如何組成 AI 的「視野」。
13. **記憶系統與知識庫**：AI 如何記住你的專案偏好，以及個人記憶 vs 共享知識庫的差異。
14. **工具設計與 Function Calling**：AI 是怎麼「決定」要呼叫哪個工具、傳什麼參數的。
15. **MCP 協議深度解析**：讓 AI 擁有「手」去操作 GitHub、瀏覽器與本地工具的標準協議。
16. **Coding Agent 與檔案系統架構**：為什麼「會寫代碼的 Agent + 檔案系統」是目前最強的通用 Agent 範式。
17. **RAG 檢索增強生成基礎**：AI 如何從你的文件堆裡「找到」相關內容再回答。
18. **向量資料庫與 Embedding 實戰**：語意搜索的底層原理與 pgvector 實作。
19. **Agent 的評估與除錯**：當 Vibe 破裂時，如何系統性判斷是模型、上下文還是工具出了問題。
20. **多 Agent 協作**：一個 Agent 不夠用時，如何讓多個 AI 分工合作完成大型任務。
21. **自動化流程**：n8n 與 GitHub Actions 的結合，實現開發自動化。

### 第四階段：The Soul (數據、存儲與 API)
*處理數據的存儲、流轉邏輯。*
22. **BaaS 核心 (Supabase)**：PostgreSQL 資料庫與數據表的設計思維。
23. **緩存與存儲**：Redis 快取邏輯與 Cloudflare R2 對象存儲。
24. **API 通訊**：Next.js API Routes 與第三方 API (Resend, Stripe) 的調用流。

### 第五階段：The Money (身份認證與商業變現)
*將專案轉化為可盈利的產品。*
25. **身份驗證 (Auth)**：Better Auth 與 Clerk 的安全邏輯。
26. **支付系統**：Stripe 與 Lemon Squeezy 的訂閱與結帳流程。
27. **郵件與通訊**：Resend 郵件發送與通知觸發邏輯。

### 第六階段：The Shield (運維、監控與分析)
*確保產品穩定運行，並根據數據持續優化。*
28. **容器化 (Docker)**：為什麼「在 AI 那裡會動」但在部署時不動？
29. **部署地圖**：Vercel vs Cloudflare Pages vs Railway。
30. **監控與分析**：Sentry (抓 Bug)、PostHog (看用戶行為)、Bruno (調試 API)。
31. **市場洞察與決策**：Appark 與 Sensor Tower 的數據驅動決策。

---

## 課程細化大綱

本大綱將上述 31 堂課，依照「核心概念、AI 調用邏輯、實戰任務」三維度進行細化。

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

### 第三階段：The Brain (AI Agent 架構與協作)

#### L10: AI Agents 對比
- **核心**: Claude Code vs Cursor 的場景選擇。
- **邏輯**: 什麼時候該用終端機 Agent，什麼時候該用 IDE Agent？
- **任務**: 在同一任務下對比兩個 Agent 的執行效率。

#### L11: Agent 核心公式：LLM + 上下文 + 工具
- **核心**: 拆解 Agent 的三個組成部分——大腦（模型）、視野（上下文）、手腳（工具）。
- **邏輯**: 為什麼同一顆模型，換了 Harness（工具骨架）表現天差地遠？Claude Code 與普通聊天視窗的差異在哪。
- **任務**: 畫出你正在用的 Agent 的「LLM + 上下文 + 工具」拆解圖。

#### L12: 上下文工程 (Context Engineering)
- **核心**: 系統指令、工具描述、對話歷史如何組成 AI 每次決策時「看到」的全部資訊。
- **邏輯**: 為什麼專案的 CLAUDE.md / .cursorrules 檔案會直接影響 AI 的表現？上下文太長為什麼會讓 AI 變笨。
- **任務**: 幫自己的專案寫一份精簡的專案規則檔，觀察 AI 回答品質的變化。

#### L13: 記憶系統與知識庫
- **核心**: 個人記憶（針對單一使用者）vs 共享知識庫（面向所有使用者的集體知識）。
- **邏輯**: AI 工具的「記住我的偏好」功能是怎麼做到跨對話持久化的。
- **任務**: 讓 AI 記住一項你的專案偏好，並在新對話中驗證它是否還記得。

#### L14: 工具設計與 Function Calling
- **核心**: 工具是連接語言模型與真實世界的手腳。
- **邏輯**: AI 如何從一堆工具中「選對」該用哪一個、決定要傳什麼參數。
- **任務**: 觀察一次 AI 呼叫工具的完整過程，寫下它選擇該工具的原因。

#### L15: MCP 協議深度解析
- **核心**: Model Context Protocol，讓 AI 用標準化方式操作外部系統。
- **邏輯**: 為什麼 MCP 出現前，每個 AI 工具都要重新對接一次 GitHub/瀏覽器；MCP 之後大家共用同一套「插頭規格」。
- **任務**: 啟動一個 MCP Server（例如 GitHub 或 Browser），讓 AI 完成一項真實操作。

#### L16: Coding Agent 與檔案系統架構
- **核心**: 一個能自主寫代碼、讀寫檔案的 Agent，是目前業界驗證過最強的通用 Agent 範式。
- **邏輯**: 為什麼 Claude Code、Cursor 都選擇「代碼執行 + 檔案讀寫 + 搜尋」這三種通用工具作為核心，而不是無限堆疊專用工具。
- **任務**: 觀察 AI 在完成一項任務時如何運用檔案系統當作「暫存記憶體」。

#### L17: RAG 檢索增強生成基礎
- **核心**: 讓 AI 在回答前先「查資料」，而不是只靠訓練時記住的知識。
- **邏輯**: AI Agent 是如何從你專案裡成千上百個檔案中，準確找出相關內容再回答的。
- **任務**: 問 AI 一個關於你專案內部文件的問題，觀察它如何先搜尋再回答。

#### L18: 向量資料庫與 Embedding 實戰
- **核心**: 把文字轉成向量，讓「語意相近」的內容在數學空間裡也相近。
- **邏輯**: pgvector 如何讓 Supabase 同時具備關聯式資料庫與語意搜索的能力。
- **任務**: 在 Supabase 開啟 pgvector，寫入幾筆資料並做一次語意搜索查詢。

#### L19: Agent 的評估與除錯
- **核心**: 面對「模型選什麼、上下文怎麼設計、工具好不好用」這些沒有標準答案的選擇，如何用數據驗證。
- **邏輯**: Vibe 破裂時，如何分層排查：是模型能力不夠、上下文餵錯資訊，還是工具本身設計有缺陷？
- **任務**: 針對一次失敗的 AI 回應，依「模型/上下文/工具」三層列出可能原因並逐一排除。

#### L20: 多 Agent 協作
- **核心**: 群體智能——當任務超出單一 Agent 的能力邊界或上下文窗口時的解法。
- **邏輯**: 拆解任務給多個專責 Agent（例如一個負責寫代碼、一個負責審查）分工合作的架構模式。
- **任務**: 設計一個雙 Agent 分工流程（例如「產出 + 審查」），並實際跑一次。

#### L21: 自動化流程 (n8n)
- **核心**: 流程自動化。
- **邏輯**: 串接 GitHub Actions，實現「代碼提交 -> 自動測試 -> 自動部署」。
- **任務**: 搭建一個簡單的自動化觸發流。

---

### 第四階段：The Soul (數據與 API)

#### L22: BaaS 核心 (Supabase)
- **核心**: 雲端資料庫與表結構。
- **邏輯**: 理解 AI 如何撰寫 SQL 並在 Supabase 中執行。
- **任務**: 建立一個 User Profile 表並實現 CRUD。

#### L23: 緩存與存儲 (Redis/R2)
- **核心**: 效能優化與對象存儲。
- **邏輯**: 為什麼圖片要放 R2 而不是放資料庫？
- **任務**: 上傳一張圖片到 Cloudflare R2 並獲得訪問連結。

#### L24: API 通訊與第三方整合
- **核心**: API Routes 與 Webhooks。
- **邏輯**: 理解 API 調用時的 Request 與 Response 結構。
- **任務**: 整合一個天氣 API 並在頁面顯示。

---

### 第五階段：The Money (商業變現)

#### L25: 身份驗證 (Better Auth)
- **核心**: 安全認證流程。
- **邏輯**: 理解 OAuth (Google/GitHub 登入) 的跳轉與權限邏輯。
- **任務**: 實現一個完整的登入/登出功能。

#### L26: 支付系統 (Stripe)
- **核心**: 訂閱制與結帳。
- **邏輯**: 理解 Stripe Checkout 與 Webhook 的非同步通知。
- **任務**: 在測試模式下完成一筆虛擬訂單。

#### L27: 郵件通訊 (Resend)
- **核心**: 交易性郵件發送。
- **邏輯**: 為什麼 AI 需要 Resend API 而不是 SMTP？
- **任務**: 發送一封包含動態內容的歡迎郵件。

---

### 第六階段：The Shield (運維與分析)

#### L28: 容器化 (Docker)
- **核心**: 環境隔離與部署包。
- **邏輯**: 理解 `Dockerfile` 如何定義「代碼的生存環境」。
- **任務**: 將一個簡單的專案打包成 Docker Image。

#### L29: 部署地圖 (Vercel/CF)
- **核心**: 全球部署。
- **邏輯**: 理解 CDN 與 Edge Functions 的執行位置。
- **任務**: 將專案部署到 Vercel 並設定自定義域名。

#### L30: 監控與分析 (PostHog)
- **核心**: 錯誤監控與用戶行為。
- **邏輯**: 如何在 Vibe Coding 過程中利用數據發現「Vibe 破裂」的地方。
- **任務**: 埋入一個按鈕點擊事件並在後台查看。

#### L31: 市場洞察與決策
- **核心**: 數據驅動開發。
- **邏輯**: 獨立開發者如何利用數據判斷下一個 Feature 該做什麼。
- **任務**: 撰寫一份簡單的產品數據分析報告。

---

## 參考資料來源

第三階段「The Brain」的深度與章節架構，主要參考以下兩份開源教材的主題編排（內容以繁體中文重新撰寫、結合 Vibe Coding 場景改寫，非逐字翻譯）：

- [AI Agent 实战：从原理到落地](https://github.com/bojieli/ai-agent-book/tree/main/book)（bojieli/ai-agent-book）— 「Agent = LLM + 上下文 + 工具」的核心框架、上下文工程、記憶與知識庫、工具設計、Coding Agent、Agent 評估、多 Agent 協作等章節。
- [AI Agents From Zero](https://github.com/didilili/ai-agents-from-zero/tree/main)（didilili/ai-agents-from-zero）— MCP 協議、RAG 檢索增強生成、向量資料庫與 Embedding 的實作章節。

## 教學偏好與規範
- **語言**：繁體中文。
- **節奏**：一課一事，專注於「調用邏輯」而非「語法細節」。
- **頁面**：HTML 乾淨美觀、留白充足、適合截圖。
- **互動**：每課結尾必帶一個實戰任務或小測驗。
- **交付**：提供直接在瀏覽器開啟的 `start` 命令。
