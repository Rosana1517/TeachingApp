#!/usr/bin/env python3
"""
自動生成 Vibe Coding 教學課程腳本
參考 generate_french_lesson.py 的模式，生成精美的 HTML 課程頁面。
所有 CSS 和 JavaScript 都內嵌在單一 HTML 檔案中（自包含），與 TeachingApp/ 下的 french-lesson 保持一致風格。
"""

import os
import re
import sys
import json
import difflib
import html as html_module
import urllib.request
import urllib.error
from datetime import datetime

LESSONS = [
    {
        "id": 1,
        "title": "Node.js 的角色",
        "subtitle": "JavaScript 脫離瀏覽器後的完整運作原理，以及 AI Agent 是如何調用它來執行你的專案。",
        "phase": "Phase 1: The Core",
        "next_topic": "Localhost 與 Port（連接埠）",
        "sections": [
            {
                "title": "JavaScript 的兩條世界線",
                "icon": "1",
                "content": "JavaScript 原本是一種「瀏覽器內嵌語言」——它只能活在 Chrome、Safari 這種瀏覽器裡，負責讓網頁動起來（點按鈕、跳出提示框、修改畫面）。直到 2009 年，工程師 Ryan Dahl 做了一件事：把 Google Chrome 裡負責執行 JavaScript 的 <strong>V8 引擎</strong> 整顆抽出來，外面包一層 C++ 外殼，讓它可以脫離瀏覽器、直接在作業系統上執行。這個「脫離瀏覽器的 JavaScript 執行環境」就是 <strong>Node.js</strong>。從那一刻起，JavaScript 不再只是「網頁裝飾語言」，而是能讀寫檔案、開伺服器、跑資料庫指令的正式後端語言。"
            },
            {
                "title": "瀏覽器 JS vs Node.js：能力大不同",
                "icon": "2",
                "content": "同樣是 JavaScript 語法，能做的事情卻完全不同，關鍵在於「宿主環境」給了它什麼權限：",
                "comparison": [
                    {
                        "side": "left",
                        "label": "瀏覽器裡的 JavaScript",
                        "code": "document.querySelector('#btn')\n  .addEventListener('click', () => {\n    alert('哈囉！')\n  })\n\n// 出於安全考量，不能直接讀寫\n// 使用者電腦的檔案系統"
                    },
                    {
                        "side": "right",
                        "label": "Node.js 裡的 JavaScript",
                        "code": "const fs = require('fs')\nfs.readFileSync('./data.json')\n\nconst http = require('http')\nhttp.createServer((req, res) => {\n  res.end('Hello from server')\n}).listen(3000)"
                    }
                ]
            },
            {
                "title": "AI Agent 調用 Node.js 的完整流程",
                "icon": "3",
                "content": "當你對 Claude Code 說：「幫我建立一個 Next.js 專案，加入登入功能」，它背後其實是在你的終端機裡，一步步執行 Node.js 相關指令，而不是憑空生出一個網站：",
                "terminal_block": "$ npx create-next-app@latest my-app\n> ✔ Would you like to use TypeScript? … Yes\n> ✔ Would you like to use Tailwind CSS? … Yes\n> Creating a new Next.js app in /Users/you/my-app...\n\n# AI 接著會安裝登入功能需要的套件\n$ npm install better-auth\n\n# 最後啟動開發伺服器——這一步才是「跑起來給你看」的關鍵\n$ npm run dev\n> ▲ Next.js 14.2.3\n> - Local:  http://localhost:3000\n> ✓ Ready in 1.2s"
            },
            {
                "title": "常見報錯與除錯",
                "icon": "⚠️",
                "content": "當 AI 執行指令卻回報「command not found: node」，代表這台電腦根本沒裝 Node.js，或是安裝了但沒有加進系統的 <code>PATH</code>。這時候可以請 AI 帶你安裝，或改用版本管理工具 <code>nvm</code>（Node Version Manager）——它能讓你在同一台電腦上，針對不同專案切換不同的 Node 版本，避免「這個專案要 Node 18，那個專案要 Node 20」互相打架。",
                "terminal_block": "$ node -v\n! command not found: node\n\n# 用 nvm 安裝並切換到指定版本\n$ nvm install 20\n$ nvm use 20\n> Now using node v20.11.0"
            },
            {
                "title": "深入解析：Event Loop 到底在忙什麼",
                "icon": "🔬",
                "deep_dive": {
                    "summary": "為什麼 Node.js 只用一個執行緒，卻能同時處理成千上萬個請求？",
                    "content": "Node.js 的 JavaScript 主執行緒其實只有一條，但它從不「傻等」。當程式呼叫像讀檔案、查資料庫、發送網路請求這類「慢動作」時，Node.js 會把這個任務丟給背後的 C++ 層（libuv）去非同步處理，自己立刻回頭繼續執行下一行程式碼。等到那個慢動作真的完成了，結果會被放進一個「回呼佇列（Callback Queue）」，由 <strong>Event Loop（事件循環）</strong> 在主執行緒閒下來的時候，一個一個把它們取出來執行。這就是為什麼你在終端機打 <code>setTimeout(() => console.log('2秒後'), 2000)</code>，程式不會被卡住 2 秒，而是會先往下跑，2 秒後才回頭印出結果——這種「非阻塞（non-blocking）」設計，正是 Node.js 能同時服務大量使用者、卻不需要開一大堆執行緒的秘密。"
                }
            },
            {
                "title": "小測驗",
                "icon": "✏️",
                "quiz": [
                    {
                        "question": "Node.js 的本質是什麼？",
                        "options": [
                            {"text": "A. 一種新的程式語言", "correct": False},
                            {"text": "B. 把 V8 引擎帶出瀏覽器的執行環境", "correct": True},
                            {"text": "C. 瀏覽器內建的 JavaScript 引擎", "correct": False}
                        ],
                        "answer": "正確答案：B。Node.js 是 Ryan Dahl 在 2009 年把 Chrome 的 V8 引擎抽出來，讓 JS 能在作業系統上直接執行，因此能讀寫檔案、開伺服器。"
                    },
                    {
                        "question": "為什麼瀏覽器裡的 JavaScript 不能直接讀寫使用者電腦的檔案？",
                        "options": [
                            {"text": "A. 因為瀏覽器沒有安裝 Node.js", "correct": False},
                            {"text": "B. 因為瀏覽器基於安全考量限制了這項權限", "correct": True},
                            {"text": "C. 因為 JavaScript 語法不支援檔案操作", "correct": False}
                        ],
                        "answer": "正確答案：B。瀏覽器是一個「沙盒」環境，出於安全考量刻意限制網頁程式碼存取本機檔案系統，Node.js 則是在受信任的伺服器/開發環境執行，所以擁有完整權限。"
                    },
                    {
                        "question": "Node.js 的 Event Loop 讓程式具備什麼特性？",
                        "options": [
                            {"text": "A. 阻塞式（Blocking），一次只能做一件事並等待完成", "correct": False},
                            {"text": "B. 非阻塞式（Non-blocking），慢任務丟出去後可以繼續做別的事", "correct": True},
                            {"text": "C. 多執行緒（Multi-threading），每個請求開一個新執行緒", "correct": False}
                        ],
                        "answer": "正確答案：B。Node.js 用單一主執行緒搭配 Event Loop，把耗時任務交給背後處理，自己不被卡住，因此能非阻塞地同時應付大量請求。"
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "🚀",
                "tasks": [
                    "打開終端機，依序執行 node -v、npm -v、npx -v，確認三個命令都有輸出版本號",
                    "執行 node -e \"console.log('Hello from Node.js'); setTimeout(() => console.log('2秒後'), 2000);\"，觀察兩行文字出現的時間差，體驗 Event Loop",
                    "請 AI Agent（Claude Code/Cursor）幫你建立一個最小的 Next.js 專案，觀察它在終端機依序執行了哪些指令",
                    "刻意輸入一個錯誤指令（例如 nod -v），截圖記錄下錯誤訊息，並嘗試看懂它在說什麼",
                    "進階挑戰：查詢並安裝 nvm，練習切換兩個不同的 Node.js 版本"
                ]
            }
        ]
    },
    {
        "id": 2,
        "title": "Localhost 與 Port（連接埠）",
        "subtitle": "電腦公寓理論，解決 EADDRINUSE 打架衝突",
        "phase": "Phase 1: The Core",
        "next_topic": "Git/GitHub 協作",
        "sections": [
            {
                "title": "什麼是 Localhost？",
                "icon": "1",
                "content": "<strong>Localhost</strong> 其實就是你自己這台電腦，它有一個固定的網路位址 <code>127.0.0.1</code>，意思是「回頭指向自己」。當你在瀏覽器打開 <code>http://localhost:3000</code>，你並沒有連到遠方的伺服器，而是連到自己電腦裡正在跑的那個開發伺服器。你可以把整台電腦想像成一棟公寓大樓，裡面有 65,536 個「房間」，這就是 <strong>Port（連接埠）</strong>——每個正在執行的網路服務，都必須先「登記」一個房號，外界才能敲對門找到它。"
            },
            {
                "title": "常見服務的預設房號",
                "icon": "2",
                "content": "不同的開發工具，出廠時都有各自習慣使用的預設 Port，先認識這些數字，之後看到報錯訊息就不會慌：",
                "comparison": [
                    {
                        "side": "left",
                        "label": "前端開發常見 Port",
                        "code": "3000  → React / Next.js\n5173  → Vite (Vue/React)\n8080  → Vue CLI / 通用 Web Server\n4200  → Angular"
                    },
                    {
                        "side": "right",
                        "label": "後端／資料庫常見 Port",
                        "code": "5432  → PostgreSQL\n3306  → MySQL\n6379  → Redis\n27017 → MongoDB"
                    }
                ]
            },
            {
                "title": "為什麼多個任務會打架？",
                "icon": "⚡",
                "content": "作業系統有個規則：同一個 Port，同一時間只能被一個程式「獨佔」。當你已經開著一個 Vibe 專案佔用 <code>3000</code> 號房，這時又啟動第二個專案、AI Agent 也試著把它塞進同一間房，系統就會直接拒絕，並丟出以下錯誤：",
                "terminal_block": "$ npm run dev\n! Error: listen EADDRINUSE: address already in use :::3000\n# EADDRINUSE = Error Address Already In Use（地址已被使用）"
            },
            {
                "title": "深入解析：作業系統怎麼決定誰能用哪個 Port",
                "icon": "🔬",
                "deep_dive": {
                    "summary": "為什麼 Port 不能像資料夾一樣被兩個程式同時打開？",
                    "content": "每個網路服務啟動時，都要向作業系統執行一個叫做 <code>bind()</code> 的動作，向系統登記「我要用這個 IP + Port 組合來接收資料」。作業系統的網路層會維護一張表，記錄目前每個 Port 被哪個程式（Process ID）佔用；一旦有第二個程式想 bind 同一組 IP + Port，系統為了避免「兩個程式收到同一筆資料卻不知道該給誰」的混亂，會直接回傳錯誤拒絕這次請求，而不是讓兩個程式共享。這也是為什麼「換一個 Port」永遠是最快的解法——因為每個房間本來就只租給一位房客。"
                }
            },
            {
                "title": "如何避免與排除 Port 衝突？",
                "icon": "3",
                "content": "最直覺的解法是「換房」：手動指定一個沒人用的 Port 啟動服務。如果你想知道是誰佔用了那個房間，也可以直接查出佔用的程式並關掉它：",
                "terminal_block": "# 方法一：換一個 Port 啟動，兩個專案就不會打架\n$ npm run dev -- -p 3008\n\n# 方法二（macOS / Linux）：查出誰佔用了 3000，再結束它\n$ lsof -i :3000\n> COMMAND   PID   USER   ...\n> node    12345  you    ...\n$ kill -9 12345\n\n# 方法二（Windows）：一樣先查 PID 再強制結束\n$ netstat -ano | findstr :3000\n$ taskkill /PID 12345 /F"
            },
            {
                "title": "小測驗",
                "icon": "✏️",
                "quiz": [
                    {
                        "question": "EADDRINUSE 錯誤代表什麼意思？",
                        "options": [
                            {"text": "A. 網路斷線", "correct": False},
                            {"text": "B. Port 已被其他程式佔用", "correct": True},
                            {"text": "C. Node.js 版本太舊", "correct": False}
                        ],
                        "answer": "正確答案：B。EADDRINUSE = Address already in use，代表你要使用的連接埠已經被另一個程式佔用了。"
                    },
                    {
                        "question": "http://localhost:3000 這個網址，實際上連到的是哪裡？",
                        "options": [
                            {"text": "A. 遠端的雲端伺服器", "correct": False},
                            {"text": "B. 你自己這台電腦（127.0.0.1）", "correct": True},
                            {"text": "C. 你的路由器", "correct": False}
                        ],
                        "answer": "正確答案：B。localhost 對應的 IP 是 127.0.0.1，意思是「回頭指向自己」，所以連到的是本機正在執行的服務。"
                    },
                    {
                        "question": "在 macOS/Linux 上，要查出誰佔用了 3000 這個 Port，該用哪個指令？",
                        "options": [
                            {"text": "A. lsof -i :3000", "correct": True},
                            {"text": "B. npm install port", "correct": False},
                            {"text": "C. git status", "correct": False}
                        ],
                        "answer": "正確答案：A。lsof -i :3000 會列出目前佔用該 Port 的程式與 PID，方便你進一步用 kill 結束它。"
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "🚀",
                "tasks": [
                    "啟動一個 Next.js 專案到預設的 port 3000",
                    "在不關閉第一個專案的情況下，再啟動另一個專案，刻意觸發一次 EADDRINUSE 錯誤並截圖",
                    "改用 npm run dev -- -p 3008 啟動第二個專案，確認兩者能同時運行而不打架",
                    "練習用 lsof -i（或 Windows 的 netstat -ano）查出目前佔用 3000 的程式 PID",
                    "進階挑戰：手動 kill 掉其中一個服務的行程，觀察瀏覽器再次整理頁面時發生什麼事"
                ]
            }
        ]
    }
]


# 完整課程大綱（對應 Vibe Coding.md）。id 1~2 由上面的 LESSONS 手動撰寫；
# id 3~31 由 LLM 依此大綱逐課生成；超過 31 課後才交由 LLM 自由延伸進階主題。
# 第三階段（The Brain, id 10~21）的深度參考自兩份開源書籍的章節架構：
#   - bojieli/ai-agent-book（Agent = LLM + 上下文 + 工具、Context Engineering、記憶、工具設計、
#     Coding Agent、Agent 評估、多 Agent 協作）
#   - didilili/ai-agents-from-zero（MCP、RAG、向量資料庫與 Embedding）
# 內容一律用繁體中文原創改寫，不逐字翻譯來源書籍。
OUTLINE = [
    {"id": 1, "phase": "Phase 1: The Core", "title": "Node.js 的角色",
     "core": "JS 的脫離瀏覽器執行環境", "logic": "為什麼 AI 需要 Node 才能執行 npm install？",
     "task": "檢查電腦的 Node 版本與環境路徑"},
    {"id": 2, "phase": "Phase 1: The Core", "title": "Localhost 與 Port（連接埠）",
     "core": "本地伺服器公寓理論", "logic": "EADDRINUSE（打架）發生時，AI 是如何幫你換房的",
     "task": "啟動一個服務並手動指定不同 Port"},
    {"id": 3, "phase": "Phase 1: The Core", "title": "Git/GitHub 協作",
     "core": "版本控制與雲端同步", "logic": "理解 AI 的 git commit 邏輯與 push 到雲端的流程",
     "task": "建立一個 Repo 並完成第一次 Push"},
    {"id": 4, "phase": "Phase 1: The Core", "title": "GitHub 寶庫挖掘",
     "core": "精準搜索與 Snippet 提取", "logic": "如何將 GitHub 上的開源功能餵給 AI Agent 並整合進專案",
     "task": "找一個開源組件並讓 AI 遷移到你的專案中"},
    {"id": 5, "phase": "Phase 1: The Core", "title": "Package Management（NPM/Bun）",
     "core": "依賴地圖與 package.json", "logic": "當依賴衝突時，AI 是如何修改 package-lock.json 修復問題的",
     "task": "練習安裝與卸載依賴，觀察檔案變化"},
    {"id": 6, "phase": "Phase 2: The Shell", "title": "AI 原型工具（v0/Bolt）",
     "core": "從 Prompt 到 UI 的瞬間轉化", "logic": "理解 v0 生成代碼的組件化思維",
     "task": "生成一個 Landing Page 並導出到本地"},
    {"id": 7, "phase": "Phase 2: The Shell", "title": "Next.js 全家桶",
     "core": "App Router 與渲染機制", "logic": "use client 與 server component 在 Vibe Coding 中的標記邏輯",
     "task": "建立一個包含 API Routes 的 Next.js 基本架構"},
    {"id": 8, "phase": "Phase 2: The Shell", "title": "UI 組件與設計（shadcn/ui）",
     "core": "組件組裝與 Tailwind CSS", "logic": "為什麼 AI 喜歡 shadcn？複製代碼而非安裝插件的優勢",
     "task": "使用 shadcn 快速搭建一個註冊頁面"},
    {"id": 9, "phase": "Phase 2: The Shell", "title": "資源自動化（Icons/Images）",
     "core": "Lucide 與 Unsplash API", "logic": "AI 如何根據主題自動挑選正確的 Icon 與占位圖",
     "task": "建立一個動態 Icon 列表頁面"},
    {"id": 10, "phase": "Phase 3: The Brain", "title": "AI Agents 對比",
     "core": "Claude Code vs Cursor 的場景選擇", "logic": "什麼時候該用終端機 Agent，什麼時候該用 IDE Agent",
     "task": "在同一任務下對比兩個 Agent 的執行效率"},
    {"id": 11, "phase": "Phase 3: The Brain", "title": "Agent 核心公式：LLM + 上下文 + 工具",
     "core": "拆解 Agent 的三個組成部分——大腦（模型）、視野（上下文）、手腳（工具）",
     "logic": "為什麼同一顆模型換了 Harness（工具骨架）表現天差地遠，Claude Code 與普通聊天視窗的差異",
     "task": "畫出你正在用的 Agent 的 LLM + 上下文 + 工具拆解圖"},
    {"id": 12, "phase": "Phase 3: The Brain", "title": "上下文工程（Context Engineering）",
     "core": "系統指令、工具描述、對話歷史如何組成 AI 每次決策時看到的全部資訊",
     "logic": "為什麼 CLAUDE.md／.cursorrules 會直接影響 AI 表現，上下文太長為什麼會讓 AI 變笨",
     "task": "幫自己的專案寫一份精簡的專案規則檔，觀察 AI 回答品質的變化"},
    {"id": 13, "phase": "Phase 3: The Brain", "title": "記憶系統與知識庫",
     "core": "個人記憶（針對單一使用者）vs 共享知識庫（面向所有使用者的集體知識）",
     "logic": "AI 工具的記住我的偏好功能是怎麼做到跨對話持久化的",
     "task": "讓 AI 記住一項你的專案偏好，並在新對話中驗證它是否還記得"},
    {"id": 14, "phase": "Phase 3: The Brain", "title": "工具設計與 Function Calling",
     "core": "工具是連接語言模型與真實世界的手腳",
     "logic": "AI 如何從一堆工具中選對該用哪一個、決定要傳什麼參數",
     "task": "觀察一次 AI 呼叫工具的完整過程，寫下它選擇該工具的原因"},
    {"id": 15, "phase": "Phase 3: The Brain", "title": "MCP 協議深度解析",
     "core": "Model Context Protocol，讓 AI 用標準化方式操作外部系統",
     "logic": "MCP 出現前每個 AI 工具都要重新對接一次 GitHub/瀏覽器，MCP 之後大家共用同一套插頭規格",
     "task": "啟動一個 MCP Server（例如 GitHub 或 Browser），讓 AI 完成一項真實操作"},
    {"id": 16, "phase": "Phase 3: The Brain", "title": "Coding Agent 與檔案系統架構",
     "core": "會寫代碼的 Agent + 檔案系統，是業界驗證過最強的通用 Agent 範式",
     "logic": "為什麼 Claude Code、Cursor 都選擇代碼執行、檔案讀寫、搜尋這三種通用工具作為核心",
     "task": "觀察 AI 在完成一項任務時如何運用檔案系統當作暫存記憶體"},
    {"id": 17, "phase": "Phase 3: The Brain", "title": "RAG 檢索增強生成基礎",
     "core": "讓 AI 在回答前先查資料，而不是只靠訓練時記住的知識",
     "logic": "AI Agent 是如何從專案裡成千上百個檔案中準確找出相關內容再回答的",
     "task": "問 AI 一個關於你專案內部文件的問題，觀察它如何先搜尋再回答"},
    {"id": 18, "phase": "Phase 3: The Brain", "title": "向量資料庫與 Embedding 實戰",
     "core": "把文字轉成向量，讓語意相近的內容在數學空間裡也相近",
     "logic": "pgvector 如何讓 Supabase 同時具備關聯式資料庫與語意搜索的能力",
     "task": "在 Supabase 開啟 pgvector，寫入幾筆資料並做一次語意搜索查詢"},
    {"id": 19, "phase": "Phase 3: The Brain", "title": "Agent 的評估與除錯",
     "core": "面對模型選什麼、上下文怎麼設計、工具好不好用這些沒有標準答案的選擇，如何用數據驗證",
     "logic": "Vibe 破裂時如何分層排查：是模型能力不夠、上下文餵錯資訊，還是工具本身設計有缺陷",
     "task": "針對一次失敗的 AI 回應，依模型/上下文/工具三層列出可能原因並逐一排除"},
    {"id": 20, "phase": "Phase 3: The Brain", "title": "多 Agent 協作",
     "core": "群體智能——當任務超出單一 Agent 的能力邊界或上下文窗口時的解法",
     "logic": "拆解任務給多個專責 Agent（例如一個負責寫代碼、一個負責審查）分工合作的架構模式",
     "task": "設計一個雙 Agent 分工流程（例如產出 + 審查），並實際跑一次"},
    {"id": 21, "phase": "Phase 3: The Brain", "title": "自動化流程（n8n）",
     "core": "流程自動化", "logic": "串接 GitHub Actions，實現代碼提交到自動測試到自動部署",
     "task": "搭建一個簡單的自動化觸發流"},
    {"id": 22, "phase": "Phase 4: The Soul", "title": "BaaS 核心（Supabase）",
     "core": "雲端資料庫與表結構", "logic": "理解 AI 如何撰寫 SQL 並在 Supabase 中執行",
     "task": "建立一個 User Profile 表並實現 CRUD"},
    {"id": 23, "phase": "Phase 4: The Soul", "title": "緩存與存儲（Redis/R2）",
     "core": "效能優化與對象存儲", "logic": "為什麼圖片要放 R2 而不是放資料庫",
     "task": "上傳一張圖片到 Cloudflare R2 並獲得訪問連結"},
    {"id": 24, "phase": "Phase 4: The Soul", "title": "API 通訊與第三方整合",
     "core": "API Routes 與 Webhooks", "logic": "理解 API 調用時的 Request 與 Response 結構",
     "task": "整合一個天氣 API 並在頁面顯示"},
    {"id": 25, "phase": "Phase 5: The Money", "title": "身份驗證（Better Auth）",
     "core": "安全認證流程", "logic": "理解 OAuth（Google/GitHub 登入）的跳轉與權限邏輯",
     "task": "實現一個完整的登入/登出功能"},
    {"id": 26, "phase": "Phase 5: The Money", "title": "支付系統（Stripe）",
     "core": "訂閱制與結帳", "logic": "理解 Stripe Checkout 與 Webhook 的非同步通知",
     "task": "在測試模式下完成一筆虛擬訂單"},
    {"id": 27, "phase": "Phase 5: The Money", "title": "郵件通訊（Resend）",
     "core": "交易性郵件發送", "logic": "為什麼 AI 需要 Resend API 而不是 SMTP",
     "task": "發送一封包含動態內容的歡迎郵件"},
    {"id": 28, "phase": "Phase 6: The Shield", "title": "容器化（Docker）",
     "core": "環境隔離與部署包", "logic": "理解 Dockerfile 如何定義代碼的生存環境",
     "task": "將一個簡單的專案打包成 Docker Image"},
    {"id": 29, "phase": "Phase 6: The Shield", "title": "部署地圖（Vercel/CF）",
     "core": "全球部署", "logic": "理解 CDN 與 Edge Functions 的執行位置",
     "task": "將專案部署到 Vercel 並設定自定義域名"},
    {"id": 30, "phase": "Phase 6: The Shield", "title": "監控與分析（PostHog）",
     "core": "錯誤監控與用戶行為", "logic": "如何在 Vibe Coding 過程中利用數據發現 Vibe 破裂的地方",
     "task": "埋入一個按鈕點擊事件並在後台查看"},
    {"id": 31, "phase": "Phase 6: The Shield", "title": "市場洞察與決策",
     "core": "數據驅動開發", "logic": "獨立開發者如何利用數據判斷下一個 Feature 該做什麼",
     "task": "撰寫一份簡單的產品數據分析報告"},
]

REFERENCE_BOOKS_NOTE = (
    "第三階段（The Brain）內容在深度與觀念上請參考兩份開源教材的章節架構："
    "bojieli/ai-agent-book《AI Agent 实战：从原理到落地》"
    "（https://github.com/bojieli/ai-agent-book/tree/main/book，核心公式 Agent = LLM + 上下文 + 工具、"
    "Context Engineering、記憶與知識庫、工具設計、Coding Agent、Agent 評估、多 Agent 協作）"
    "與 didilili/ai-agents-from-zero《AI Agents From Zero》"
    "（https://github.com/didilili/ai-agents-from-zero/tree/main，MCP、RAG、向量資料庫與 Embedding）。"
    "務必只借用觀念與結構作為靈感，用你自己的話以繁體中文原創撰寫，不得逐字翻譯或大段抄錄原書（原書為簡體中文）。"
)

# === 課程內容輸出格式 ===
# 先前版本要求 LLM 直接輸出 JSON，但豐富後的課程內容大量包含 HTML/JSX 程式碼片段
# （雙引號屬性）、程式碼註解、多行終端機輸出，LLM 在該用 \" 轉義的地方漏轉義的機率
# 非常高，導致 JSON 解析持續失敗、只能落到內容單薄的 fallback。既然真正會壞掉的
# 是「JSON 字串跳脫規則」，最徹底的修法不是繼續在 prompt 裡疊加轉義規則、
# 再用一堆正規表示式事後修補（那是治標，前面已經證明會不斷冒出新的邊角案例），
# 而是換一種完全不需要跳脫字元的純文字格式：以固定的 KEY: value 標記逐行分隔內容，
# 內容本身（包含任何雙引號、HTML 標籤、程式碼）原封不動照抄，不需要任何跳脫。
LESSON_TEXT_FORMAT_INSTRUCTIONS = """請「只」用下面這種純文字標記格式回覆，不要加任何開場白、結語，也不要用 markdown code block 包住整個回覆：

TITLE: 課程主標題（繁體中文）
SUBTITLE: 一句話副標題
PHASE: 所屬階段名稱（例如 Phase 1: The Core）
NEXT_TOPIC: 下一課預告的主題名稱
===SECTION===
SECTION_TITLE: 小節標題
SECTION_ICON: 數字或 emoji
CONTENT:
完整、有實質內容的說明文字（120 字以上），可以直接寫 <strong>、<code> 等 HTML 標籤，
也可以直接寫雙引號、單引號、任何符號，不需要跳脫，這裡的每一行都會被原文保留。
===SECTION===
SECTION_TITLE: 對照小節（可選，視主題需要使用）
SECTION_ICON: 2
CONTENT:
一句引導文字
COMPARISON_LEFT_LABEL: 情境 A 的標籤
COMPARISON_LEFT_CODE:
純文字或程式碼，可以多行，一樣不需要跳脫任何符號
COMPARISON_RIGHT_LABEL: 情境 B 的標籤
COMPARISON_RIGHT_CODE:
純文字或程式碼，可以多行
===SECTION===
SECTION_TITLE: 帶指令範例的小節
SECTION_ICON: 3
CONTENT:
說明文字
TERMINAL_BLOCK:
終端機指令與輸出範例，每一行用開頭前綴標示類型，系統會自動幫你上色，不要自己寫 HTML/span：
$ 開頭 = 指令本身（例如 "$ npm install"）
> 開頭 = 正常輸出
! 開頭 = 錯誤訊息
# 開頭 = 註解
沒有前綴的行就當作一般文字。這裡可以直接寫雙引號、任何符號，不需要跳脫。
===SECTION===
SECTION_TITLE: 深入解析
SECTION_ICON: 🔬
DEEP_DIVE_SUMMARY: 一句吸引人往下讀的提問式標題
DEEP_DIVE_CONTENT:
至少 150 字的深入原理說明，解釋「為什麼」而不只是「是什麼」
===SECTION===
SECTION_TITLE: 小測驗
SECTION_ICON: ✏️
QUIZ_QUESTION: 第一題題目
QUIZ_OPTION_A: 選項 A 的內容
QUIZ_OPTION_B: 選項 B 的內容
QUIZ_OPTION_C: 選項 C 的內容
QUIZ_CORRECT: B
QUIZ_ANSWER: 解釋為什麼 B 對、其他選項為什麼錯
QUIZ_QUESTION: 第二題題目（同一個小節內可以有多個 QUIZ_QUESTION 區塊）
QUIZ_OPTION_A: ...
QUIZ_OPTION_B: ...
QUIZ_OPTION_C: ...
QUIZ_CORRECT: A
QUIZ_ANSWER: ...
===SECTION===
SECTION_TITLE: 今日任務
SECTION_ICON: 🚀
TASK: 任務一
TASK: 任務二
TASK: 任務三
TASK: 任務四
===END===

格式規則：
- 每個標記都是「大寫英文_底線: 值」放在單獨一行；CONTENT/TERMINAL_BLOCK/DEEP_DIVE_CONTENT/COMPARISON_*_CODE 這幾個標記，值從下一行開始一路到下一個標記或 ===SECTION===/===END=== 為止，可以是多行。
- 一定要用 ===SECTION=== 分隔每個小節，並在最後一個小節後面加上 ===END===。
- 絕對不要把整段回覆包在 ```、「」或任何額外符號裡；也不要輸出這份格式說明本身。

內容硬性要求（不符合就視為不合格）：
1. 至少要有 6 個 ===SECTION===，且必須包含至少一個 TERMINAL_BLOCK（實際指令／輸出範例）與至少一個 DEEP_DIVE_SUMMARY/DEEP_DIVE_CONTENT（原理深挖），COMPARISON 視主題需要選用。
2. 一般 CONTENT 每則至少 120 字、DEEP_DIVE_CONTENT 至少 150 字，禁止寫成一句話就結束的空洞段落，更禁止「以下步驟：」「如下：」這類話講到一半沒有接下文。
3. 小測驗至少要有 2 題（2 個 QUIZ_QUESTION 區塊），每題 3 個選項，QUIZ_ANSWER 要解釋原因，不能只寫「正確答案：B」。
4. 今日任務（TASK）至少要有 4 項，其中至少 1 項要請學習者實際操作 AI Agent（Claude Code/Cursor 等）並觀察它的行為，而不是只有手動操作。
5. 內容要聚焦於「這個概念在 Vibe Coding 中的角色」「AI Agent 是如何調用/運用它的」「當 Vibe 破裂時該如何診斷」，並提供具體、可執行的指令或程式碼範例，不要只有抽象描述。
6. 【禁止編造】所有指令、套件名稱、錯誤訊息、API 端點、GitHub repo 名稱都必須是真實存在、你有把握的資訊，不可以為了讓範例看起來具體而虛構不存在的錯誤代碼、虛構的 CLI 工具名稱，或猜測、編造 GitHub repo 的擁有者帳號、commit hash、版本號。如果不確定某個指令的確切輸出格式，就用比較通用、你確定正確的範例（例如常見的 npm/git/docker 基本指令），或用文字描述其「大致行為」，而不要生出一段編造的假終端機輸出。除非是 facebook/react、vercel/next.js、vuejs/vue 這類極度知名、你非常確定的 repo，否則請用「（你要示範的套件）官方 GitHub repo」這種泛稱描述，不要生造一個看起來具體但可能是錯的路徑。寧可簡單但真實，也不要花俏但虛構。
7. 【禁止空洞裝飾】不要用「vibe stable ✅ / vibe broken ⚠️」這類裝飾性但沒有實質資訊的標籤來包裝內容；每一段範例、每一句話都必須包含具體、可查證的技術事實，而不是聽起來專業但其實沒有講清楚任何事情的空話。
"""

FEW_SHOT_EXAMPLE_NOTE = (
    "以下是已通過審核、品質達標的範例片段，示範什麼叫做具體、真實、有實質內容"
    "（而不是抽象空話或編造的假輸出），請以同等真實度與資訊密度撰寫：\n\n"
    "TERMINAL_BLOCK:\n"
    "$ npm run dev\n"
    "! Error: listen EADDRINUSE: address already in use :::3000\n"
    "# EADDRINUSE = Error Address Already In Use（地址已被使用），這是 Node.js 內建的真實錯誤代碼\n\n"
    "DEEP_DIVE_SUMMARY: 為什麼 Port 不能像資料夾一樣被兩個程式同時打開？\n"
    "DEEP_DIVE_CONTENT:\n"
    "每個網路服務啟動時，都要向作業系統執行一個叫做 bind() 的動作，向系統登記「我要用這個 IP + Port 組合來接收資料」。"
    "作業系統的網路層會維護一張表，記錄目前每個 Port 被哪個程式（Process ID）佔用；一旦有第二個程式想 bind 同一組 IP + Port，"
    "系統為了避免兩個程式收到同一筆資料卻不知道該給誰的混亂，會直接回傳錯誤拒絕這次請求。\n\n"
    "注意範例中的 EADDRINUSE、bind() 都是真實存在的技術名詞，DEEP_DIVE_CONTENT 解釋的是「為什麼」而非重複「是什麼」，"
    "TERMINAL_BLOCK 只用 $/>/!/# 這幾個前綴標示每一行的類型，絕對不要自己寫 <span> 之類的 HTML 標籤——"
    "系統會自動把這些前綴轉換成正確上色的畫面，你只要專心寫真實、正確的指令與輸出內容就好。"
)


# === 純文字標記格式解析器 ===
# 用「找下一個已知標記」取代 JSON 逐字元跳脫，天生就不怕內容裡出現任何引號、
# HTML 屬性、程式碼片段，從根本上避開了先前反覆出現的 JSON escaping 失敗模式。

_SECTION_DELIM_RE = re.compile(r'^={2,}\s*SECTION\s*={2,}$', re.IGNORECASE)
_END_DELIM_RE = re.compile(r'^={2,}\s*END\s*={2,}$', re.IGNORECASE)
_MARKER_LINE_RE = re.compile(r'^([A-Z][A-Z_]*):[ \t]?(.*)$')

_TOP_LEVEL_KEYS = {'TITLE', 'SUBTITLE', 'PHASE', 'NEXT_TOPIC'}
_SECTION_TEXT_KEYS = {
    'SECTION_TITLE', 'SECTION_ICON', 'CONTENT', 'TERMINAL_BLOCK',
    'COMPARISON_LEFT_LABEL', 'COMPARISON_LEFT_CODE',
    'COMPARISON_RIGHT_LABEL', 'COMPARISON_RIGHT_CODE',
    'DEEP_DIVE_SUMMARY', 'DEEP_DIVE_CONTENT',
}
_QUIZ_KEYS = {'QUIZ_QUESTION', 'QUIZ_OPTION_A', 'QUIZ_OPTION_B', 'QUIZ_OPTION_C', 'QUIZ_CORRECT', 'QUIZ_ANSWER'}
_KNOWN_KEYS = _TOP_LEVEL_KEYS | _SECTION_TEXT_KEYS | _QUIZ_KEYS | {'TASK'}

# LLM 偶爾會把標記名稱打成看似合理的同義詞（例如 SUBLINE 而非 SUBTITLE）；
# 這裡做一層寬容的別名對應，減少不必要的重試，但真正的正確性保障仍然是
# generate_lesson_via_llm 裡「缺欄位就拒絕接受」的驗證，別名只是錦上添花。
_KEY_ALIASES = {
    'SUB_TITLE': 'SUBTITLE', 'SUBLINE': 'SUBTITLE', 'SUBHEADING': 'SUBTITLE',
    'NEXT_LESSON': 'NEXT_TOPIC', 'NEXT': 'NEXT_TOPIC',
    'ICON': 'SECTION_ICON', 'TITLE_SECTION': 'SECTION_TITLE',
    'TERMINAL': 'TERMINAL_BLOCK', 'CODE': 'TERMINAL_BLOCK',
    'DEEP_DIVE_TITLE': 'DEEP_DIVE_SUMMARY',
    'LEFT_LABEL': 'COMPARISON_LEFT_LABEL', 'LEFT_CODE': 'COMPARISON_LEFT_CODE',
    'RIGHT_LABEL': 'COMPARISON_RIGHT_LABEL', 'RIGHT_CODE': 'COMPARISON_RIGHT_CODE',
    'COMPARISON_A_LABEL': 'COMPARISON_LEFT_LABEL', 'COMPARISON_A_CODE': 'COMPARISON_LEFT_CODE',
    'COMPARISON_B_LABEL': 'COMPARISON_RIGHT_LABEL', 'COMPARISON_B_CODE': 'COMPARISON_RIGHT_CODE',
}


def _strip_code_fence(text):
    """去除 LLM 偶爾會加上的 ```...``` 包裹。"""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r'^```[a-zA-Z]*\n?', '', text)
        text = re.sub(r'```\s*$', '', text)
    return text.strip()


def _tokenize_lesson_text(text):
    """把純文字格式切成 (KEY, value) 事件序列，SECTION 分隔符用 ('__SECTION__', None) 表示。"""
    events = []
    cur_key = None
    buf = []

    def flush():
        if cur_key is not None:
            events.append((cur_key, '\n'.join(buf).strip()))

    for raw_line in text.replace('\r\n', '\n').split('\n'):
        stripped = raw_line.strip()
        if _END_DELIM_RE.match(stripped):
            flush()
            return events
        if _SECTION_DELIM_RE.match(stripped):
            flush()
            cur_key, buf = None, []
            events.append(('__SECTION__', None))
            continue
        m = _MARKER_LINE_RE.match(raw_line)
        matched_key = _KEY_ALIASES.get(m.group(1), m.group(1)) if m else None
        if m and matched_key in _KNOWN_KEYS:
            flush()
            cur_key, buf = matched_key, [m.group(2)]
        elif cur_key is not None:
            buf.append(raw_line)
        # 標記出現前的雜訊行（例如 LLM 誤加的開場白）直接忽略
    flush()
    return events


def _structure_lesson_events(events):
    """把 (KEY, value) 事件序列組成 generate_html() 期望的 lesson dict 結構。"""
    lesson = {"sections": []}
    raw_sections = []
    cur = None

    for key, value in events:
        if key == '__SECTION__':
            cur = {}
            raw_sections.append(cur)
            continue
        if cur is None:
            if key in _TOP_LEVEL_KEYS:
                lesson[key.lower()] = value
            continue
        if key == 'QUIZ_QUESTION':
            cur.setdefault('_quiz', []).append({'question': value, 'options': [], 'correct': '', 'answer': ''})
        elif key in ('QUIZ_OPTION_A', 'QUIZ_OPTION_B', 'QUIZ_OPTION_C'):
            quiz_list = cur.get('_quiz') or []
            if quiz_list:
                quiz_list[-1]['options'].append((key[-1], value))
        elif key == 'QUIZ_CORRECT':
            quiz_list = cur.get('_quiz') or []
            if quiz_list:
                quiz_list[-1]['correct'] = value.strip().upper()[:1]
        elif key == 'QUIZ_ANSWER':
            quiz_list = cur.get('_quiz') or []
            if quiz_list:
                quiz_list[-1]['answer'] = value
        elif key == 'TASK':
            cur.setdefault('_tasks', []).append(value)
        elif key == 'SECTION_TITLE':
            cur['title'] = value
        elif key == 'SECTION_ICON':
            cur['icon'] = value
        elif key == 'CONTENT':
            cur['content'] = value
        elif key == 'TERMINAL_BLOCK':
            cur['terminal_block'] = value
        elif key in ('COMPARISON_LEFT_LABEL', 'COMPARISON_RIGHT_LABEL', 'COMPARISON_LEFT_CODE', 'COMPARISON_RIGHT_CODE'):
            comp = cur.setdefault('_comparison', {'left': {}, 'right': {}})
            side = 'left' if key.startswith('COMPARISON_LEFT') else 'right'
            field = 'label' if key.endswith('LABEL') else 'code'
            comp[side][field] = value
        elif key in ('DEEP_DIVE_SUMMARY', 'DEEP_DIVE_CONTENT'):
            dd = cur.setdefault('_deep_dive', {})
            dd['summary' if key.endswith('SUMMARY') else 'content'] = value

    for raw in raw_sections:
        if not raw.get('title'):
            continue
        section = {"title": raw['title'], "icon": raw.get('icon') or '•'}
        if raw.get('content'):
            section['content'] = raw['content']
        if raw.get('terminal_block'):
            section['terminal_block'] = raw['terminal_block']
        comp = raw.get('_comparison')
        if comp:
            items = []
            for side in ('left', 'right'):
                if comp[side].get('label') or comp[side].get('code'):
                    items.append({"side": side, "label": comp[side].get('label', ''), "code": comp[side].get('code', '')})
            if items:
                section['comparison'] = items
        dd = raw.get('_deep_dive')
        if dd and (dd.get('summary') or dd.get('content')):
            section['deep_dive'] = {"summary": dd.get('summary', ''), "content": dd.get('content', '')}
        quiz_raw = raw.get('_quiz') or []
        quiz_list = []
        for q in quiz_raw:
            if not q['question'] or len(q['options']) < 2:
                continue
            options = [{"text": opt_text, "correct": letter == q['correct']} for letter, opt_text in q['options']]
            if not any(o['correct'] for o in options):
                options[0]['correct'] = True  # 保底：避免 QUIZ_CORRECT 缺漏導致沒有任何正確答案
            quiz_list.append({"question": q['question'], "options": options, "answer": q['answer']})
        if quiz_list:
            section['quiz'] = quiz_list
        tasks = [t for t in raw.get('_tasks', []) if t]
        if tasks:
            section['tasks'] = tasks
        lesson['sections'].append(section)

    return lesson


def parse_lesson_text(raw_text):
    """把 LLM 回傳的純文字標記格式解析成 lesson dict；格式明顯不對時回傳 None。"""
    text = _strip_code_fence(raw_text)
    if 'TITLE:' not in text or '===SECTION===' not in text:
        return None
    events = _tokenize_lesson_text(text)
    return _structure_lesson_events(events)


def get_next_lesson_id():
    """獲取下一個要生成的課程 ID：找出目前缺少的最小編號（會自動補上被刪除以便重新生成的課次），
    而不是單純永遠往最大值 +1，這樣才能個別刪除品質不佳的課程並重新生成。"""
    search_dirs = [os.path.join('..', 'TeachingApp', 'vibe')]
    existing_ids = set()
    for d in search_dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.startswith('vibe-lesson-') and f.endswith('.html'):
                    try:
                        existing_ids.add(int(f.split('-')[2].split('.')[0]))
                    except (IndexError, ValueError):
                        pass

    next_id = 1
    while next_id in existing_ids:
        next_id += 1
    return next_id


def get_previous_topics():
    """掃描已經存在的課程 HTML，抓出每堂課的標題，避免新課程主題重複。"""
    topics = [lesson["title"] for lesson in LESSONS]
    search_dirs = [os.path.join('..', 'TeachingApp', 'vibe')]
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        existing_files = sorted(f for f in os.listdir(d) if f.startswith("vibe-lesson-") and f.endswith(".html"))
        for filename in existing_files:
            try:
                with open(os.path.join(d, filename), encoding="utf-8") as f:
                    html = f.read()
            except OSError:
                continue
            match = re.search(r'<h1 class="lesson-title">([^<]+)</h1>', html)
            if match:
                topics.append(match.group(1).strip())
    seen = set()
    deduped = []
    for topic in topics:
        if topic not in seen:
            seen.add(topic)
            deduped.append(topic)
    return deduped


def normalize_topic(title):
    """去掉「第N課：」這類編號前綴，只留下主題本身，方便比對是否重複。"""
    t = re.sub(r'^第\s*\d+\s*課[:：]\s*', '', title or '')
    return t.strip()


def find_duplicate_topic(new_title, previous_topics, threshold=0.82):
    """檢查新課程主題是否與過去教過的主題重複或高度相似。
    有相似項就回傳該舊主題，否則回傳 None。"""
    new_norm = normalize_topic(new_title)
    if not new_norm:
        return None
    for old_title in previous_topics:
        old_norm = normalize_topic(old_title)
        if not old_norm:
            continue
        if new_norm == old_norm:
            return old_title
        if difflib.SequenceMatcher(None, new_norm, old_norm).ratio() >= threshold:
            return old_title
    return None


def get_outline_item(lesson_id):
    """依課程 ID 找出對應的固定大綱項目；超出大綱範圍則回傳 None。"""
    for item in OUTLINE:
        if item["id"] == lesson_id:
            return item
    return None


def build_fallback_lesson(next_id, outline_item):
    """LLM 呼叫失敗時的備用課程內容：若在大綱範圍內，至少保留正確的標題與方向。"""
    if outline_item is None:
        lesson = dict(LESSONS[-1])
        lesson["id"] = next_id
        return lesson

    next_item = get_outline_item(next_id + 1)
    title = outline_item["title"]
    core = outline_item["core"]
    logic = outline_item["logic"]
    task = outline_item["task"]

    return {
        "id": next_id,
        "title": title,
        "subtitle": core,
        "phase": outline_item["phase"],
        "next_topic": next_item["title"] if next_item else "",
        "sections": [
            {
                "title": f"什麼是{title}？",
                "icon": "1",
                "content": core
            },
            {
                "title": "為什麼 Vibe Coding 開發者需要懂這個",
                "icon": "2",
                "content": logic
            },
            {
                "title": "核心概念",
                "icon": "3",
                "content": (
                    f"在 Vibe Coding 的工作流程中，{title}是不可或缺的一環。"
                    f"理解「{core}」，能讓你在 AI 協作開發時更有效率地溝通需求與除錯。"
                )
            },
            {
                "title": "常見問題",
                "icon": "⚠️",
                "content": (
                    f"初學者在接觸{title}時，常常忽略「{logic}」這個核心邏輯。"
                    "建議在實作今日任務時，特別留意這個面向，並請 AI 逐步解釋每個步驟的原因。"
                )
            },
            {
                "title": "小測驗",
                "icon": "✏️",
                "quiz": [
                    {
                        "question": f"關於「{title}」，下列哪項描述最接近其核心用途？",
                        "options": [
                            {"text": f"A. {core}", "correct": True},
                            {"text": "B. 這是前端框架才需要的專有知識", "correct": False},
                            {"text": "C. 只有後端工程師需要了解", "correct": False}
                        ],
                        "answer": f"正確答案：A。{title}的核心在於{core}。"
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "🚀",
                "tasks": [
                    task,
                    f"閱讀 AI 對「{title}」的完整解釋，記下對你最有用的 3 個知識點",
                    "請 AI 舉一個在真實 Vibe Coding 專案中應用這個概念的實際範例"
                ]
            }
        ]
    }


def build_outline_prompt(next_id, outline_item, previous_topics):
    """依固定大綱產生指定主題的課程 prompt。"""
    topics_list = "、".join(previous_topics) if previous_topics else "（尚無）"
    reference_note = REFERENCE_BOOKS_NOTE if outline_item["phase"] == "Phase 3: The Brain" else ""
    return (
        f"你是一位資深的 Vibe Coding 技術導師，正在為一套給繁體中文使用者的獨立開發技術棧課程撰寫第 {next_id} 課的教材。\n"
        f"這一課在整體大綱中屬於「{outline_item['phase']}」，主題已經固定為：「{outline_item['title']}」。\n"
        f"核心概念：{outline_item['core']}\n"
        f"AI 調用邏輯重點：{outline_item['logic']}\n"
        f"建議的實戰任務方向（可依此發揮，不必逐字照用）：{outline_item['task']}\n"
        f"已經教過的主題依序是：{topics_list}，撰寫時避免與這些內容重複。\n"
        f"{reference_note}\n\n"
        "課程重點應該放在：\n"
        "- 這個技術/概念在 Vibe Coding 中的角色是什麼？\n"
        "- AI Agent 是如何調用或運用這個概念的？\n"
        "- 當 Vibe 破裂（報錯或行為異常）時，如何診斷和修復？\n\n"
        + LESSON_TEXT_FORMAT_INSTRUCTIONS
        + "\n" + FEW_SHOT_EXAMPLE_NOTE
    )


def build_freeform_prompt(next_id, previous_topics):
    """大綱（31 課）跑完後，交由 LLM 自由延伸進階主題的 prompt。"""
    topics_list = "、".join(previous_topics) if previous_topics else "（尚無）"
    return (
        f"你是一位資深的 Vibe Coding 技術導師，正在為一套給繁體中文使用者的獨立開發技術棧課程撰寫第 {next_id} 課的教材。\n"
        f"這套課程原本規劃的 31 課大綱已經教完，現在要延伸進階主題。\n"
        f"已經教過的主題依序是：{topics_list}。\n"
        "請挑選一個循序漸進、難度適中地往下延伸的新主題，絕對不要跟已經教過的主題重複或高度相似，"
        "可以考慮更進階的 AI Agent 工程主題（例如 Prompt 快取、Agent 沙盒安全、長任務中斷恢復、成本控管等）。\n\n"
        "課程重點應該放在：\n"
        "- 這個技術在 Vibe Coding 中的角色是什麼？\n"
        "- AI Agent 是如何調用這個技術的？\n"
        "- 當 Vibe 破裂（報錯）時，如何診斷和修復？\n\n"
        + LESSON_TEXT_FORMAT_INSTRUCTIONS
        + "\n" + FEW_SHOT_EXAMPLE_NOTE
    )


def generate_lesson_via_llm(next_id, previous_topics, outline_item=None):
    """呼叫第三方 OpenAI 相容 API 生成下一堂課的內容（純文字標記格式），失敗時回傳 None。"""
    api_url = os.environ.get("LLM_API_URL")
    api_key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL")

    if not api_url or not api_key or not model:
        print("缺少 LLM_API_URL / LLM_API_KEY / LLM_MODEL，無法呼叫 LLM 生成課程")
        return None

    if outline_item is not None:
        prompt = build_outline_prompt(next_id, outline_item, previous_topics)
    else:
        prompt = build_freeform_prompt(next_id, previous_topics)

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        # 加深後的課程 schema（6+ 小節、多題小測驗、任務）常需要遠超過 4096 tokens 的
        # 繁體中文輸出；太低的上限會讓 JSON 在結構中間被截斷、解析失敗，進而落到空洞的
        # fallback 內容，這正是先前「內容空泛」的根本原因之一。
        "max_tokens": 8192,
    }).encode("utf-8")

    request = urllib.request.Request(
        api_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        print(f"呼叫 LLM API 失敗：HTTP {error.code} {error.read().decode('utf-8', 'ignore')}")
        return None
    except Exception as error:
        print(f"呼叫 LLM API 失敗：{error}")
        return None

    try:
        text = result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as error:
        print(f"無法從回應中取出內容：{error}；原始回應：{result}")
        return None

    print(f"LLM 回應長度：{len(text)} 字元；前 300 字：{text[:300]}", flush=True)

    lesson = parse_lesson_text(text)
    if lesson is None:
        print("LLM 回應不是預期的純文字標記格式（缺少 TITLE: 或 ===SECTION===）", flush=True)
        print(f"原始回應（前 500 字）：{text[:500]!r}", flush=True)
        return None

    # 品質驗證：標題/副標題缺漏（例如 LLM 把標記名稱打錯，像是用 SUBLINE 而非
    # SUBTITLE）或 sections 太少，代表這次輸出不完整，一律拒絕接受並重試，
    # 而不是帶著缺欄位的 lesson 繼續往下跑到 generate_html 才爆炸。
    sections = lesson.get("sections", [])
    has_quiz = any("quiz" in s for s in sections)
    has_tasks = any("tasks" in s for s in sections)
    if not lesson.get("title") or not lesson.get("subtitle") or len(sections) < 4 or not has_quiz or not has_tasks:
        print(
            f"LLM 回傳的課程內容不完整（title={bool(lesson.get('title'))}, "
            f"subtitle={bool(lesson.get('subtitle'))}, sections={len(sections)}, "
            f"quiz={has_quiz}, tasks={has_tasks}），拒絕接受",
            flush=True,
        )
        print(f"Section keys: {[list(s.keys()) for s in sections]}", flush=True)
        print(f"完整原始回應（用來診斷是否為輸出截斷）：\n{text}", flush=True)
        return None

    lesson["id"] = next_id
    if outline_item is not None:
        # 大綱範圍內的課程：標題與階段強制對齊大綱，避免 LLM 偏題
        lesson["title"] = outline_item["title"]
        lesson["phase"] = outline_item["phase"]
        next_item = get_outline_item(next_id + 1)
        if next_item is not None:
            lesson["next_topic"] = next_item["title"]
    return lesson


# === 輸出時的 HTML 逃逸處理 ===
# LLM 生成的教學內容常常會示範真正的 JSX/HTML 程式碼（例如 <button>、<div
# className="...">）。這些內容如果原封不動塞進頁面，瀏覽器會把它們當成
# 真正的 DOM 標籤解析、渲染出實體按鈕/容器，而不是顯示成看得見的程式碼文字
# （L07 的教材裡就出現過 <button>...</button> 被瀏覽器直接吃掉、畫面上只剩
# 裸露文字的狀況）。因此一般文字欄位一律逃逸，只保留固定幾個我們自己認可
# 的行內標籤；終端機區塊則完全不接受 LLM 寫的 HTML，改用簡單的前綴語法
# 由程式自己組出安全的 <span> 標記，從根本避免這個類別的渲染錯誤。

_ALLOWED_INLINE_TAGS = ("strong", "code", "em", "b", "i")


def _sanitize_inline_html(text):
    """逃逸所有 HTML，只保留少數幾個白名單的行內標籤（不含屬性）。"""
    if text is None:
        return ""
    escaped = html_module.escape(str(text), quote=False)
    for tag in _ALLOWED_INLINE_TAGS:
        escaped = re.sub(rf'&lt;{tag}&gt;', f'<{tag}>', escaped, flags=re.IGNORECASE)
        escaped = re.sub(rf'&lt;/{tag}&gt;', f'</{tag}>', escaped, flags=re.IGNORECASE)
    return escaped


def _render_terminal_block(raw_text):
    """把純文字終端機腳本（每行用 $/>/!/# 前綴標示類型）轉成安全的著色 HTML。
    不接受、也不信任 LLM 直接寫入的 <span> 或其他標籤——每一行都會先逃逸，
    再依前綴包上我們自己產生的 <span> class，杜絕任意 HTML 注入。"""
    if not raw_text:
        return ""
    rendered = []
    for line in raw_text.split('\n'):
        if line.startswith('$ ') or line == '$':
            rest = html_module.escape(line[2:] if len(line) > 1 else '')
            rendered.append(f'<span class="prompt">$</span> <span class="cmd">{rest}</span>')
        elif line.startswith('> '):
            rendered.append(f'<span class="output">{html_module.escape(line[2:])}</span>')
        elif line.startswith('! '):
            rendered.append(f'<span class="error">{html_module.escape(line[2:])}</span>')
        elif line.startswith('# '):
            rendered.append(f'<span class="comment">{html_module.escape(line)}</span>')
        else:
            rendered.append(html_module.escape(line))
    return '\n'.join(rendered)


def generate_html(lesson):
    """生成精美的 HTML 課程頁面（自包含，無外部 CSS/JS 依賴）"""
    lesson_num = f"{lesson['id']:02d}"
    phase = lesson.get("phase", "Phase 1: The Core")

    html_parts = []

    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html lang="zh-Hant">')
    html_parts.append('<head>')
    html_parts.append('<meta charset="UTF-8">')
    html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_parts.append(f'<title>Vibe Coding 課 {lesson_num} — {_sanitize_inline_html(lesson.get("title", ""))}</title>')
    html_parts.append(get_full_css())
    html_parts.append('</head>')
    html_parts.append('<body>')
    html_parts.append('<div class="container">')

    # Header
    html_parts.append('')
    html_parts.append('  <!-- Header -->')
    html_parts.append('  <div class="lesson-header">')
    html_parts.append(f'    <span class="lesson-number">{_sanitize_inline_html(phase)}</span>')
    html_parts.append(f'    <h1 class="lesson-title">{_sanitize_inline_html(lesson.get("title", ""))}</h1>')
    html_parts.append(f'    <p class="lesson-subtitle">{_sanitize_inline_html(lesson.get("subtitle", ""))}</p>')
    html_parts.append('  </div>')

    # Generate sections
    for section in lesson['sections']:
        section_title = _sanitize_inline_html(section["title"])
        comment_safe_title = re.sub(r'[^\w\s（）()：:、,.-]', '', section["title"])
        html_parts.append('')
        html_parts.append(f'  <!-- Section: {comment_safe_title} -->')
        html_parts.append('  <div class="section">')
        html_parts.append(f'    <div class="section-title"><span class="icon">{_sanitize_inline_html(section["icon"])}</span> {section_title}</div>')

        if 'content' in section:
            html_parts.append(f'    <p>{_sanitize_inline_html(section["content"])}</p>')

        if 'terminal_block' in section:
            html_parts.append('    <div class="terminal-block">')
            html_parts.append(_render_terminal_block(section['terminal_block']))
            html_parts.append('    </div>')

        if 'comparison' in section:
            html_parts.append('    <div class="diagram-grid">')
            for item in section['comparison']:
                tag_class = 'tag-blue' if item.get('side', '') == 'left' else 'tag-green'
                html_parts.append(f'      <div class="diagram-card" style="text-align:left;">')
                html_parts.append(f'        <span class="tag {tag_class}">{_sanitize_inline_html(item["label"])}</span>')
                html_parts.append(f'        <div class="terminal-block" style="margin-top:0.5rem;">{html_module.escape(item["code"])}</div>')
                html_parts.append('      </div>')
            html_parts.append('    </div>')

        if 'deep_dive' in section:
            dd = section['deep_dive']
            html_parts.append('    <details class="deep-dive">')
            html_parts.append(f'      <summary>{_sanitize_inline_html(dd.get("summary", "深入解析"))}</summary>')
            html_parts.append('      <div class="deep-dive-content">')
            html_parts.append(f'        <p>{_sanitize_inline_html(dd.get("content", ""))}</p>')
            html_parts.append('      </div>')
            html_parts.append('    </details>')

        if 'quiz' in section:
            html_parts.append('    <div class="quiz-box">')
            html_parts.append('      <h4>請先回答，再點擊「查看答案」</h4>')
            for idx, quiz_item in enumerate(section['quiz'], 1):
                html_parts.append('')
                html_parts.append('      <div class="quiz-item">')
                html_parts.append(f'        <div class="quiz-question">{idx}. {_sanitize_inline_html(quiz_item["question"])}</div>')
                html_parts.append('        <ul class="quiz-options">')
                for opt in quiz_item['options']:
                    correct_attr = 'true' if opt['correct'] else 'false'
                    html_parts.append(f'          <li onclick="checkAnswer(this, {correct_attr})">{_sanitize_inline_html(opt["text"])}</li>')
                html_parts.append('        </ul>')
                html_parts.append('        <button class="reveal-btn" onclick="revealAnswer(this)">查看答案</button>')
                html_parts.append(f'        <div class="answer">✅ {_sanitize_inline_html(quiz_item["answer"])}</div>')
                html_parts.append('      </div>')
            html_parts.append('    </div>')

        if 'tasks' in section:
            html_parts.append('    <div class="follow-box">')
            html_parts.append(f'      <h4>請依序完成以下練習</h4>')
            html_parts.append('      <ol style="padding-left: 1.5rem;">')
            for task in section['tasks']:
                html_parts.append(f'        <li style="padding: 0.5rem 0;">{_sanitize_inline_html(task)}</li>')
            html_parts.append('      </ol>')
            html_parts.append('    </div>')

        html_parts.append('  </div>')

    # Followup Reminder
    html_parts.append('')
    html_parts.append('  <!-- Followup Reminder -->')
    html_parts.append('  <div class="followup">')
    html_parts.append('    💡 有任何不清楚的地方嗎？隨時問我！這些都可以繼續深入探討。')
    html_parts.append('  </div>')

    # Footer
    html_parts.append('')
    html_parts.append('  <!-- Footer -->')
    html_parts.append('  <div class="lesson-footer">')
    html_parts.append(f'    <p>Vibe Coding Masterclass · Lesson {lesson_num} · {_sanitize_inline_html(lesson.get("title", ""))}</p>')
    html_parts.append(f'    <p style="margin-top: 0.3rem;">下一課預告：{_sanitize_inline_html(lesson.get("next_topic", ""))}</p>')
    html_parts.append('  </div>')
    html_parts.append('')
    html_parts.append('</div>')

    # Inline JavaScript (self-contained, no external dependency)
    html_parts.append('')
    html_parts.append('<script>')
    html_parts.append(INLINE_JS)
    html_parts.append('</script>')
    html_parts.append('</body>')
    html_parts.append('</html>')

    return '\n'.join(html_parts)


INLINE_JS = """
function checkAnswer(el, isCorrect) {
  const siblings = el.parentElement.querySelectorAll('li');
  siblings.forEach(s => {
    s.style.pointerEvents = 'none';
  });
  if (isCorrect) {
    el.classList.add('correct');
  } else {
    el.classList.add('wrong');
    siblings.forEach(s => {
      if (s.onclick && s.onclick.toString().includes('true')) {
        s.classList.add('correct');
      }
    });
  }
}

function revealAnswer(btn) {
  const answer = btn.nextElementSibling;
  if (answer.style.display === 'block') {
    answer.style.display = 'none';
    btn.textContent = '查看答案';
  } else {
    answer.style.display = 'block';
    btn.textContent = '隱藏答案';
  }
}
"""


def get_full_css():
    """返回完整的自包含 CSS（與 TeachingApp/french-lesson 風格一致）"""
    return '''<style>

  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "Noto Sans TC", "Microsoft JhengHei", sans-serif;
    background: #fafbfc;
    color: #1a1a2e;
    line-height: 1.9;
    padding: 3rem 2rem;
  }
  .container { max-width: 720px; margin: 0 auto; }

  /* Header */
  .lesson-header {
    text-align: center;
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 2px solid #e8ecf1;
  }
  .lesson-number {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.35rem 1.2rem;
    border-radius: 999px;
    margin-bottom: 1rem;
  }
  .lesson-title {
    font-size: 1.85rem;
    font-weight: 800;
    color: #1a1a2e;
    margin-bottom: 0.5rem;
  }
  .lesson-subtitle {
    font-size: 1rem;
    color: #6b7280;
  }

  /* Section */
  .section {
    margin-bottom: 2.5rem;
  }
  .section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .section-title .icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px; height: 28px;
    border-radius: 8px;
    background: #667eea22;
    color: #667eea;
    font-size: 0.85rem;
    font-weight: 800;
  }

  /* Terminal block */
  .terminal-block {
    background: #1e1e2e;
    color: #cdd6f4;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
    font-size: 0.85rem;
    line-height: 1.8;
    overflow-x: auto;
    white-space: pre-wrap;
    margin-bottom: 1rem;
  }
  .terminal-block .prompt { color: #a6e3a1; }
  .terminal-block .cmd { color: #89b4fa; }
  .terminal-block .output { color: #cdd6f4; opacity: 0.85; }
  .terminal-block .error { color: #f38ba8; }
  .terminal-block .comment { color: #6c7086; font-style: italic; }

  /* Diagram grid */
  .diagram-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  .diagram-card {
    background: #fff;
    border: 1px solid #e8ecf1;
    border-radius: 12px;
    padding: 1.2rem 1rem;
    transition: box-shadow 0.2s;
  }
  .diagram-card:hover { box-shadow: 0 4px 16px #667eea22; }
  .tag {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    margin-bottom: 0.6rem;
  }
  .tag-blue { background: #eff6ff; color: #2563eb; }
  .tag-green { background: #f0fdf4; color: #16a34a; }

  /* Follow-box */
  .follow-box {
    background: linear-gradient(135deg, #f0f4ff, #faf5ff);
    border: 1px solid #d4d9f2;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .follow-box h4 {
    font-size: 1rem;
    margin-bottom: 0.8rem;
    color: #4338ca;
  }

  /* Deep dive */
  .deep-dive {
    background: #fff;
    border: 1px solid #e8ecf1;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .deep-dive summary {
    cursor: pointer;
    font-weight: 700;
    color: #1a1a2e;
    font-size: 1.05rem;
    outline: none;
  }
  .deep-dive summary::-webkit-details-marker { display: none; }
  .deep-dive summary::before {
    content: "▶";
    display: inline-block;
    margin-right: 0.5rem;
    font-size: 0.7rem;
    color: #667eea;
    transition: transform 0.2s;
  }
  .deep-dive[open] summary::before {
    transform: rotate(90deg);
  }
  .deep-dive[open] summary {
    color: #667eea;
    margin-bottom: 1rem;
  }
  .deep-dive-content {
    padding-top: 0.5rem;
    color: #555;
    font-size: 0.95rem;
  }
  .deep-dive-content p {
    margin-bottom: 0.8rem;
  }
  .deep-dive-content code {
    background: #f3f4f6;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
    font-size: 0.85rem;
  }

  /* Quiz */
  .quiz-box {
    background: #fff;
    border: 2px solid #667eea33;
    border-radius: 12px;
    padding: 1.5rem;
  }
  .quiz-box h4 {
    font-size: 1.05rem;
    margin-bottom: 1rem;
    color: #1a1a2e;
  }
  .quiz-item {
    margin-bottom: 1.2rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #f0f0f0;
  }
  .quiz-item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
  .quiz-question {
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #333;
  }
  .quiz-options { list-style: none; padding: 0; }
  .quiz-options li {
    padding: 0.5rem 0.8rem;
    margin-bottom: 0.3rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
    font-size: 0.95rem;
  }
  .quiz-options li:hover { background: #f5f3ff; }
  .quiz-options li.correct {
    background: #d1fae5;
    font-weight: 600;
  }
  .quiz-options li.wrong {
    background: #fee2e2;
  }

  .reveal-btn {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.5rem 1.4rem;
    background: #667eea;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }
  .reveal-btn:hover { background: #5568d3; }
  .answer { display: none; margin-top: 0.5rem; color: #059669; font-weight: 600; }

  /* Followup */
  .followup {
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    border: 1px dashed #86efac;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-top: 2rem;
    color: #166534;
    font-size: 0.95rem;
  }

  /* Footer */
  .lesson-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 2px solid #e8ecf1;
    color: #999;
    font-size: 0.85rem;
  }

</style>'''


def main():
    """主函式"""
    print("開始生成 Vibe Coding 教學課程...")

    # 獲取下一個課程 ID
    next_id = get_next_lesson_id()
    print(f"將生成第 {next_id:02d} 課")

    # 選擇對應的課程
    outline_item = get_outline_item(next_id)
    previous_topics = get_previous_topics()
    if next_id <= len(LESSONS):
        lesson = LESSONS[next_id - 1]
    else:
        lesson = None
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                lesson = generate_lesson_via_llm(next_id, previous_topics, outline_item=outline_item)
            except Exception as error:
                # 任何未預期的例外（解析器邊角案例、網路問題等）都不該讓整個
                # GitHub Action 直接失敗；當成這次嘗試失敗，讓迴圈重試或最終落到
                # fallback 內容，維持「今天一定要生出一堂課」的可用性。
                print(f"第 {attempt} 次生成時發生未預期例外：{error!r}", flush=True)
                lesson = None
            if lesson is not None:
                duplicate = find_duplicate_topic(lesson.get("title", ""), previous_topics)
                if duplicate:
                    print(f"第 {attempt} 次生成的主題「{lesson.get('title', '')}」與已存在課程「{duplicate}」重複，捨棄重試。")
                    lesson = None
                else:
                    print(f"已透過 LLM API 生成第 {next_id:02d} 課內容（第 {attempt} 次嘗試）")
                    break
            print(f"第 {attempt} 次 LLM 生成失敗，{'重試中...' if attempt < max_attempts else '改用備用課程內容'}")
        if lesson is None:
            lesson = build_fallback_lesson(next_id, outline_item)

    duplicate = find_duplicate_topic(lesson.get("title", ""), previous_topics)
    if duplicate:
        print(f"偵測到主題重複：新課程「{lesson.get('title', '')}」與已存在課程「{duplicate}」高度相似，停止生成本課。")
        sys.exit(1)

    # 生成 HTML
    html_content = generate_html(lesson)

    # 生成檔案名稱
    filename = f"vibe-lesson-{lesson['id']:02d}.html"

    # 寫入檔案到 TeachingApp/vibe/ 目錄
    output_dir = os.path.join('..', 'TeachingApp', 'vibe')
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"已成功生成課程: {filepath}")
    print(f"   標題: {lesson.get('title', '')}")
    print(f"   副標題: {lesson.get('subtitle', '')}")
    print(f"   檔案大小: {len(html_content)} bytes")
    print(f"   生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
