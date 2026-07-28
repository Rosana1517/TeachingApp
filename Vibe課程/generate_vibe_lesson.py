#!/usr/bin/env python3
"""
自動生成 Vibe Coding 教學課程腳本
參考 generate_french_lesson.py 的模式，生成精美的 HTML 課程頁面。
所有 CSS 和 JavaScript 都內嵌在單一 HTML 檔案中（自包含），與 TeachingApp/ 下的 french-lesson 保持一致風格。
"""

import os
import re
import json
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
                "content": "JavaScript 原本是一種「瀏覽器內嵌語言」——它只能在 Chrome、Safari 裡跑。直到 2009 年，Ryan Dahl 把 Google Chrome 的 <strong>V8 JavaScript 引擎</strong> 抽出來，包了一層 C++ 外殼，讓 JavaScript 能直接在作業系統上執行。這就是 <strong>Node.js</strong>。"
            },
            {
                "title": "AI Agent 調用 Node.js 的完整流程",
                "icon": "2",
                "content": "當你對 Claude Code 說：「幫我建立一個 Next.js 專案，加入登入功能」，它實際上經歷了以下步驟："
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
                        "answer": "正確答案：B。Node.js 是 Ryan Dahl 在 2009 年把 Chrome 的 V8 引擎抽出來，讓 JS 能在作業系統上直接執行。"
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "🚀",
                "tasks": [
                    "打開終端機，依序執行 node -v、npm -v、npx -v",
                    "確認三個命令都有輸出版本號",
                    "進階挑戰：執行 node -e \"console.log('Hello from Node.js'); setTimeout(() => console.log('2秒後'), 2000);\"，體驗 Event Loop"
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
                "content": "<strong>Localhost</strong> 其實就是你的電腦自己（IP 是 127.0.0.1）。你的電腦就像一棟公寓，裡面有 65,535 個「房間」（這就是 <strong>Port / 連接埠</strong>）。"
            },
            {
                "title": "為什麼多個任務會打架？",
                "icon": "⚡",
                "content": "當你同時開兩個 Vibe 專案，它們都想擠進 <code>3000</code> 號房，就會噴出 <code>EADDRINUSE</code> 錯誤。"
            },
            {
                "title": "如何避免 Port 衝突？",
                "icon": "3",
                "content": "學會「換房」技巧：<code>npm run dev -- -p 3008</code>，讓不同專案住在不同的房間，就能同時完美運行！"
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
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "🚀",
                "tasks": [
                    "啟動一個 Next.js 專案到 port 3000",
                    "再啟動另一個專案到 port 3008",
                    "確認兩個專案可以同時運行而不打架"
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

LESSON_SCHEMA_INSTRUCTIONS = """請只回傳一個合法的 JSON 物件（不要加任何說明文字、不要用 markdown code block），結構必須完全符合：

{
  "title": "課程主標題（繁體中文）",
  "subtitle": "一句話副標題",
  "phase": "所屬階段名稱（例如 Phase 1: The Core）",
  "next_topic": "下一課預告的主題名稱",
  "sections": [
    {
      "title": "小節標題",
      "icon": "數字或 emoji",
      "content": "說明文字，可用 <strong> 和 <code> 標籤強調重點"
    },
    {
      "title": "深入解析",
      "icon": "🔬",
      "content": "說明文字",
      "terminal_block": "一段程式碼或命令列輸出範例"
    },
    {
      "title": "小測驗",
      "icon": "✏️",
      "quiz": [
        {
          "question": "題目",
          "options": [
            {"text": "A. 選項", "correct": false},
            {"text": "B. 選項", "correct": true},
            {"text": "C. 選項", "correct": false}
          ],
          "answer": "正確答案說明"
        }
      ]
    },
    {
      "title": "今日任務",
      "icon": "🚀",
      "tasks": ["任務一", "任務二"]
    }
  ]
}

每個 section 只需要包含它需要的欄位。"sections" 至少要有 4 個小節，建議包含「小測驗」與「今日任務」。
內容要聚焦於「AI Agent 是如何調用這個技術的」以及「當 Vibe 破裂時該如何診斷」。
"""


def get_next_lesson_id():
    """獲取下一個課程 ID；L01 已由手動優化的版本，自動跳過"""
    search_dirs = [os.path.join('..', 'TeachingApp', 'vibe')]
    existing_files = []
    for d in search_dirs:
        if os.path.isdir(d):
            existing_files.extend(f for f in os.listdir(d) if f.startswith('vibe-lesson-') and f.endswith('.html'))
    if not existing_files:
        return 1

    max_id = 0
    for file in existing_files:
        try:
            lesson_id = int(file.split('-')[2].split('.')[0])
            max_id = max(max_id, lesson_id)
        except:
            pass

    return max(max_id + 1, 2)


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
    return {
        "id": next_id,
        "title": outline_item["title"],
        "subtitle": outline_item["core"],
        "phase": outline_item["phase"],
        "next_topic": next_item["title"] if next_item else "",
        "sections": [
            {
                "title": outline_item["title"],
                "icon": "1",
                "content": f"{outline_item['core']}。{outline_item['logic']}"
            },
            {
                "title": "今日任務",
                "icon": "🚀",
                "tasks": [outline_item["task"]]
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
        + LESSON_SCHEMA_INSTRUCTIONS
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
        + LESSON_SCHEMA_INSTRUCTIONS
    )


def generate_lesson_via_llm(next_id, previous_topics, outline_item=None):
    """呼叫第三方 OpenAI 相容 API 生成下一堂課的內容（JSON），失敗時回傳 None。"""
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

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        print("LLM 回應裡找不到 JSON 物件")
        return None

    try:
        lesson = json.loads(match.group(0))
    except json.JSONDecodeError as error:
        print(f"無法解析 LLM 回應的 JSON：{error}")
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
    html_parts.append(f'<title>Vibe Coding 課 {lesson_num} — {lesson["title"]}</title>')
    html_parts.append(get_full_css())
    html_parts.append('</head>')
    html_parts.append('<body>')
    html_parts.append('<div class="container">')

    # Header
    html_parts.append('')
    html_parts.append('  <!-- Header -->')
    html_parts.append('  <div class="lesson-header">')
    html_parts.append(f'    <span class="lesson-number">{phase}</span>')
    html_parts.append(f'    <h1 class="lesson-title">{lesson["title"]}</h1>')
    html_parts.append(f'    <p class="lesson-subtitle">{lesson["subtitle"]}</p>')
    html_parts.append('  </div>')

    # Generate sections
    for section in lesson['sections']:
        html_parts.append('')
        html_parts.append(f'  <!-- Section: {section["title"]} -->')
        html_parts.append('  <div class="section">')
        html_parts.append(f'    <div class="section-title"><span class="icon">{section["icon"]}</span> {section["title"]}</div>')

        if 'content' in section:
            html_parts.append(f'    <p>{section["content"]}</p>')

        if 'terminal_block' in section:
            html_parts.append('    <div class="terminal-block">')
            html_parts.append(section['terminal_block'])
            html_parts.append('    </div>')

        if 'comparison' in section:
            html_parts.append('    <div class="diagram-grid">')
            for item in section['comparison']:
                tag_class = 'tag-blue' if item.get('side', '') == 'left' else 'tag-green'
                html_parts.append(f'      <div class="diagram-card" style="text-align:left;">')
                html_parts.append(f'        <span class="tag {tag_class}">{item["label"]}</span>')
                html_parts.append(f'        <div class="terminal-block" style="margin-top:0.5rem;">{item["code"]}</div>')
                html_parts.append('      </div>')
            html_parts.append('    </div>')

        if 'quiz' in section:
            html_parts.append('    <div class="quiz-box">')
            html_parts.append('      <h4>請先回答，再點擊「查看答案」</h4>')
            for idx, quiz_item in enumerate(section['quiz'], 1):
                html_parts.append('')
                html_parts.append('      <div class="quiz-item">')
                html_parts.append(f'        <div class="quiz-question">{idx}. {quiz_item["question"]}</div>')
                html_parts.append('        <ul class="quiz-options">')
                for opt in quiz_item['options']:
                    correct_attr = 'true' if opt['correct'] else 'false'
                    html_parts.append(f'          <li onclick="checkAnswer(this, {correct_attr})">{opt["text"]}</li>')
                html_parts.append('        </ul>')
                html_parts.append('        <button class="reveal-btn" onclick="revealAnswer(this)">查看答案</button>')
                html_parts.append(f'        <div class="answer">✅ {quiz_item["answer"]}</div>')
                html_parts.append('      </div>')
            html_parts.append('    </div>')

        if 'tasks' in section:
            html_parts.append('    <div class="follow-box">')
            html_parts.append(f'      <h4>請依序完成以下練習</h4>')
            html_parts.append('      <ol style="padding-left: 1.5rem;">')
            for task in section['tasks']:
                html_parts.append(f'        <li style="padding: 0.5rem 0;">{task}</li>')
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
    html_parts.append(f'    <p>Vibe Coding Masterclass · Lesson {lesson_num} · {lesson["title"]}</p>')
    html_parts.append(f'    <p style="margin-top: 0.3rem;">下一課預告：{lesson.get("next_topic", "")}</p>')
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
    if next_id <= len(LESSONS):
        lesson = LESSONS[next_id - 1]
    else:
        lesson = generate_lesson_via_llm(next_id, get_previous_topics(), outline_item=outline_item)
        if lesson is None:
            print("LLM 生成失敗，改用備用課程內容")
            lesson = build_fallback_lesson(next_id, outline_item)
        else:
            print(f"已透過 LLM API 生成第 {next_id:02d} 課內容")

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
    print(f"   標題: {lesson['title']}")
    print(f"   副標題: {lesson['subtitle']}")
    print(f"   檔案大小: {len(html_content)} bytes")
    print(f"   生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
