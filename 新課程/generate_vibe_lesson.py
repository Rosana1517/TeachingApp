#!/usr/bin/env python3
"""
自動生成 Vibe Coding 教學課程腳本
參考 generate_french_lesson.py 的模式，生成精美的 HTML 課程頁面。
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

# 硬編碼課程資料庫（前幾課使用預設內容）
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

# 課程 JSON Schema 指令（供 LLM 生成下一課使用）
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
    """獲取下一個課程 ID"""
    existing_files = [f for f in os.listdir('.') if f.startswith('vibe-lesson-') and f.endswith('.html')]
    if not existing_files:
        return 1

    max_id = 0
    for file in existing_files:
        try:
            lesson_id = int(file.split('-')[1].split('.')[0])
            max_id = max(max_id, lesson_id)
        except:
            pass

    return max_id + 1


def get_previous_topics():
    """掃描已經存在的課程 HTML，抓出每堂課的標題，避免新課程主題重複。"""
    topics = [lesson["title"] for lesson in LESSONS]
    existing_files = sorted(f for f in os.listdir(".") if f.startswith("vibe-lesson-") and f.endswith(".html"))
    for filename in existing_files:
        try:
            with open(filename, encoding="utf-8") as f:
                html = f.read()
        except OSError:
            continue
        match = re.search(r'<h1 class="lesson-title">([^<]+)</h1>', html)
        if match:
            topics.append(match.group(1).strip())
    # 去重但保留順序
    seen = set()
    deduped = []
    for topic in topics:
        if topic not in seen:
            seen.add(topic)
            deduped.append(topic)
    return deduped


def generate_lesson_via_llm(next_id, previous_topics):
    """呼叫第三方 OpenAI 相容 API 生成下一堂課的內容（JSON），失敗時回傳 None。

    透過環境變數設定第三方服務：
      LLM_API_URL   — 完整的 chat completions 端點
      LLM_API_KEY   — 該服務的 API key
      LLM_MODEL     — 要使用的 model 名稱
    """
    api_url = os.environ.get("LLM_API_URL")
    api_key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL")

    if not api_url or not api_key or not model:
        print("缺少 LLM_API_URL / LLM_API_KEY / LLM_MODEL，無法呼叫 LLM 生成課程")
        return None

    topics_list = "、".join(previous_topics) if previous_topics else "（尚無）"
    prompt = (
        f"你是一位資深的 Vibe Coding 技術導師，正在為一套給繁體中文使用者的獨立開發技術棧課程撰寫第 {next_id} 課的教材。\n"
        f"已經教過的主題依序是：{topics_list}。\n"
        "請挑選一個循序漸進、難度適中地往下延伸的新主題，絕對不要跟已經教過的主題重複或高度相似。\n\n"
        "課程重點應該放在：\n"
        "- 這個技術在 Vibe Coding 中的角色是什麼？\n"
        "- AI Agent 是如何調用這個技術的？\n"
        "- 當 Vibe 破裂（報錯）時，如何診斷和修復？\n\n"
        + LESSON_SCHEMA_INSTRUCTIONS
    )

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

    # 防止模型還是包了 ```json ... ``` 之類的 code block
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
    return lesson


def generate_html(lesson):
    """生成精美的 HTML 課程頁面"""
    lesson_num = f"{lesson['id']:02d}"
    phase = lesson.get("phase", "Phase 1: The Core")

    html_parts = []

    # HTML head
    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html lang="zh-Hant">')
    html_parts.append('<head>')
    html_parts.append('<meta charset="UTF-8">')
    html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_parts.append(f'<title>L{lesson_num} — {lesson["title"]}</title>')
    html_parts.append('<link rel="stylesheet" href="../assets/styles.css">')
    html_parts.append('<style>')
    html_parts.append(get_lesson_css())
    html_parts.append('</style>')
    html_parts.append('</head>')
    html_parts.append('<body>')
    html_parts.append('<div class="container">')

    # Header
    html_parts.append('')
    html_parts.append('  <!-- Header -->')
    html_parts.append('  <div class="lesson-header">')
    html_parts.append(f'    <span class="lesson-phase">{phase}</span>')
    html_parts.append(f'    <span class="lesson-number">LESSON {lesson_num} / 23</span>')
    html_parts.append(f'    <h1 class="lesson-title">{lesson["title"]}</h1>')
    html_parts.append(f'    <p class="lesson-subtitle">{lesson["subtitle"]}</p>')
    html_parts.append('  </div>')

    # Generate sections
    for section in lesson['sections']:
        html_parts.append('')
        html_parts.append(f'  <!-- Section: {section["title"]} -->')
        html_parts.append('  <div class="section">')
        html_parts.append(f'    <div class="section-title"><span class="icon">{section["icon"]}</span> {section["title"]}</div>')

        # Content paragraph
        if 'content' in section:
            html_parts.append(f'    <p>{section["content"]}</p>')

        # Terminal block
        if 'terminal_block' in section:
            html_parts.append('    <div class="terminal-block">')
            html_parts.append(section['terminal_block'])
            html_parts.append('    </div>')

        # Comparison grid
        if 'comparison' in section:
            html_parts.append('    <div class="diagram-grid">')
            for item in section['comparison']:
                tag_class = 'tag-blue' if item.get('side', '') == 'left' else 'tag-green'
                html_parts.append(f'      <div class="diagram-card" style="text-align:left;">')
                html_parts.append(f'        <span class="tag {tag_class}">{item["label"]}</span>')
                html_parts.append(f'        <div class="terminal-block" style="margin-top:0.5rem;">{item["code"]}</div>')
                html_parts.append('      </div>')
            html_parts.append('    </div>')

        # Quiz
        if 'quiz' in section:
            html_parts.append('    <div class="quiz-box">')
            html_parts.append('      <h4>✏️ 小測驗</h4>')
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

        # Tasks
        if 'tasks' in section:
            html_parts.append('    <div class="task-box">')
            html_parts.append(f'      <h4>🚀 今日任務</h4>')
            html_parts.append('      <ol>')
            for task in section['tasks']:
                html_parts.append(f'        <li>{task}</li>')
            html_parts.append('      </ol>')
            html_parts.append('    </div>')

        html_parts.append('  </div>')

    # Primary Source
    html_parts.append('')
    html_parts.append('  <!-- Primary Source -->')
    html_parts.append('  <div class="primary-source">')
    html_parts.append('    <h4>📖 推薦延伸閱讀</h4>')
    html_parts.append(f'    <p>參考文件：<a href="../reference/lesson-{lesson_num}-cheatsheet.html">Lesson {lesson_num} Cheatsheet</a></p>')
    html_parts.append('  </div>')

    # Followup Reminder
    html_parts.append('')
    html_parts.append('  <!-- Followup Reminder -->')
    html_parts.append('  <div class="followup">')
    html_parts.append('    💡 有任何不清楚的地方嗎？隨時問我！這些都可以繼續深入探討。')
    html_parts.append('  </div>')

    # Navigation
    html_parts.append('')
    html_parts.append('  <!-- Navigation -->')
    html_parts.append('  <div class="nav-links">')
    prev_link = f"./000{lesson['id']-1:02d}-previous.html" if lesson['id'] > 1 else "#"
    next_link = f"./000{lesson['id']+1:02d}-next.html" if lesson['id'] < 23 else "#"
    html_parts.append(f'    <a href="{prev_link}">← 上一課</a>')
    html_parts.append(f'    <a href="{next_link}">下一課 →</a>')
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

    # JavaScript
    html_parts.append('')
    html_parts.append('<script src="../assets/quiz-widget.js"></script>')
    html_parts.append('</body>')
    html_parts.append('</html>')

    return '\n'.join(html_parts)


def get_lesson_css():
    """返回課程專屬 CSS"""
    return """
    .deep-dive {
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 1rem;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
    }
    .deep-dive summary {
      cursor: pointer;
      font-weight: 700;
      color: #334155;
      font-size: 1.05rem;
    }
    .deep-dive[open] summary {
      margin-bottom: 1rem;
      color: #1e40af;
    }
    .primary-source {
      background: linear-gradient(135deg, #fefce8, #fef9c3);
      border-left: 4px solid #eab308;
      border-radius: 0.75rem;
      padding: 1.25rem;
      margin-top: 2rem;
    }
    .primary-source h4 {
      color: #854d0e;
      font-size: 0.95rem;
      margin-bottom: 0.5rem;
    }
    .primary-source a {
      color: #a16207;
      text-decoration: none;
      font-weight: 600;
    }
    .primary-source p {
      color: #713f12;
      font-size: 0.9rem;
    }
    .followup {
      background: #f0fdf4;
      border: 1px dashed #86efac;
      border-radius: 0.75rem;
      padding: 1rem 1.25rem;
      margin-top: 1.5rem;
      color: #166534;
      font-size: 0.9rem;
    }
    .nav-links {
      display: flex;
      justify-content: space-between;
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid #e2e8f0;
      font-size: 0.85rem;
    }
    .nav-links a {
      color: #667eea;
      text-decoration: none;
      font-weight: 600;
    }
    .nav-links a:hover { text-decoration: underline; }
    """


def main():
    """主函式"""
    print("開始生成 Vibe Coding 教學課程...")

    # 獲取下一個課程 ID
    next_id = get_next_lesson_id()
    print(f"將生成第 {next_id:02d} 課")

    # 選擇對應的課程
    if next_id <= len(LESSONS):
        lesson = LESSONS[next_id - 1]
    else:
        lesson = generate_lesson_via_llm(next_id, get_previous_topics())
        if lesson is None:
            print("LLM 生成失敗，改用最後一個預設課程內容")
            lesson = dict(LESSONS[-1])
            lesson["id"] = next_id
        else:
            print(f"已透過 LLM API 生成第 {next_id:02d} 課內容")

    # 生成 HTML
    html_content = generate_html(lesson)

    # 生成檔案名稱
    filename = f"vibe-lesson-{lesson['id']:02d}.html"

    # 寫入檔案
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"已成功生成課程: {filename}")
    print(f"   標題: {lesson['title']}")
    print(f"   副標題: {lesson['subtitle']}")
    print(f"   檔案大小: {len(html_content)} bytes")
    print(f"   生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
