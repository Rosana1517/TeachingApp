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

> 2026-07 改版：完整大綱與每課細化內容見 [Vibe Coding.md](./Vibe%20Coding.md)。第三階段「The Brain」參考 [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book/tree/main/book) 與 [didilili/ai-agents-from-zero](https://github.com/didilili/ai-agents-from-zero/tree/main) 兩份開源教材的章節深度重新設計，從「工具比較」擴充為完整的 Agent 架構理解（上下文工程、記憶系統、工具設計、MCP、RAG、向量資料庫、Agent 評估、多 Agent 協作）。

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

### 第三階段：The Brain（AI Agent 架構與協作）🆕 全面加深
10. **AI Agents 對比**：Claude Code vs Cline vs Cursor
11. **Agent 核心公式**：LLM + 上下文 + 工具，拆解 Harness 的運作方式
12. **上下文工程（Context Engineering）**：AI 每次決策時「看到」的全部資訊
13. **記憶系統與知識庫**：個人記憶 vs 共享知識庫
14. **工具設計與 Function Calling**：AI 如何決定呼叫哪個工具
15. **MCP 協議深度解析**：讓 AI 調用 GitHub、瀏覽器與本地工具的標準協議
16. **Coding Agent 與檔案系統架構**：目前業界驗證最強的通用 Agent 範式
17. **RAG 檢索增強生成基礎**：AI 如何先查資料再回答
18. **向量資料庫與 Embedding 實戰**：語意搜索與 pgvector
19. **Agent 的評估與除錯**：Vibe 破裂時的分層排查邏輯
20. **多 Agent 協作**：任務超出單一 Agent 能力邊界時的分工架構
21. **自動化流程**：n8n 與 GitHub Actions

### 第四階段：The Soul（數據、存儲與 API）
22. **BaaS 核心（Supabase）**：PostgreSQL 資料庫與數據表設計
23. **緩存與存儲**：Redis 快取與 Cloudflare R2
24. **API 通訊**：Next.js API Routes 與第三方 API 調用流

### 第五階段：The Money（身份認證與商業變現）
25. **身份驗證（Auth）**：Better Auth 與 Clerk 的安全邏輯
26. **支付系統**：Stripe 與 Lemon Squeezy
27. **郵件與通訊**：Resend 郵件發送與通知觸發

### 第六階段：The Shield（運維、監控與分析）
28. **容器化（Docker）**：環境隔離與部署包
29. **部署地圖**：Vercel vs Cloudflare Pages vs Railway
30. **監控與分析**：Sentry、PostHog、Bruno
31. **市場洞察**：Appark 與 Sensor Tower

---

## 教學偏好

- 繁體中文教學
- 一課只教一件事，節奏緊湊
- HTML 課頁面乾淨好看、留白充足、適合截圖
- 每節課結尾帶一個小測驗或手動任務
- 生成課程後提供一條能夠在瀏覽器打開課的命令
