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
    search_dirs = ['.', os.path.join('..', 'TeachingApp')]
    existing_files = []
    for d in search_dirs:
        if os.path.isdir(d):
            existing_files.extend(f for f in os.listdir(d) if f.startswith('vibe-lesson-') and f.endswith('.html'))
    if not existing_files:
        return 1

    max_id = 0
    for file in existing_files:
        try:
            lesson_id = int(file.split('-')[1].split('.')[0])
            max_id = max(max_id, lesson_id)
        except:
            pass

    return max(max_id + 1, 2)


def get_previous_topics():
    """掃描已經存在的課程 HTML，抓出每堂課的標題，避免新課程主題重複。"""
    topics = [lesson["title"] for lesson in LESSONS]
    search_dirs = ['.', os.path.join('..', 'TeachingApp')]
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


def generate_lesson_via_llm(next_id, previous_topics):
    """呼叫第三方 OpenAI 相容 API 生成下一堂課的內容（JSON），失敗時回傳 None。"""
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

    # 寫入檔案到 TeachingApp/ 目錄（與 french-lesson 同級）
    output_dir = os.path.join('..', 'TeachingApp')
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
