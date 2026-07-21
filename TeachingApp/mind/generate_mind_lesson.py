#!/usr/bin/env python3
"""
自動生成心靈成長課程腳本

沿用 french / vibe 兩套的架構：前幾課用寫死的種子內容，之後交給 LLM 依照
既定學習路徑往下長。輸出為自帶 CSS 的單一 HTML，供 TeachingApp 的 WebView 直接顯示。

檔名慣例 mind-lesson-NN.html 由 HTMLScannerService 自動辨識分類，不需改 App 程式碼。
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

# ---------------------------------------------------------------------------
# 學習路徑：LLM 生成新課時必須依照這條路徑，不可自由發散
# ---------------------------------------------------------------------------

CURRICULUM = """\
階段一 · 止血（打斷自動反應）
  緩衝句 → 說不的三個層次 → 迴避地圖 → 身體訊號辨識
階段二 · 建立判斷（不被片面資訊帶走）
  事實與評論分離 → 認知扭曲辨識 → 資訊來源可信度 → 他人評價的歸屬
階段三 · 表達與爭取
  PREP 結構化表達 → DEAR MAN 請求腳本 → 應對推回 → 情緒勒索的辨識與回應
階段四 · 整合
  價值澄清 → 小型暴露計畫 → 復發處理 → 長期維持
"""

SAFETY_RULES = """\
安全準則（絕對不可違反）：
1. 這是心理教育與技能訓練，不是心理治療。不得提供診斷、不得暗示使用者有任何疾患。
2. 練習必須低風險、可在日常生活中執行，不得要求使用者進行high-stakes對抗
   （例如當場質問主管、切斷關係、公開衝突）。
3. 不得教授操控、話術取勝、情緒勒索等傷害他人的技巧。目標是能表達，不是壓過別人。
4. 不得承諾療效，不得使用「保證」「一定會」「徹底解決」這類措辭。
5. 每課都必須保留頁尾的專業協助提醒，不可刪除或淡化。
"""

# ---------------------------------------------------------------------------
# 種子課程
# ---------------------------------------------------------------------------

LESSONS = [
    {
        "id": 1,
        "title": "緩衝句",
        "subtitle": "在反射性答應之前，先為自己拿回三秒鐘",
        "next_topic": "說不的三個層次",
        "sections": [
            {
                "title": "為什麼答應得那麼快",
                "icon": "1",
                "content": "被要求的當下，你身體裡先出現的是不舒服 —— 緊、悶、心跳快。而「答應」能讓這股不舒服<strong>立刻</strong>消失。問題就在這個「立刻」：短期的解脫感會回頭強化剛才那個行為，心理學稱為<strong>負增強</strong>，它讓反射下次來得更快、更自動。你不是不夠堅強，你是被訓練過的。"
            },
            {
                "title": "迴避會自己長大",
                "icon": "2",
                "content": "研究指出，迴避雖然帶來暫時緩解，長期卻會<strong>放大</strong>痛苦、鞏固「這件事很危險」的信念，並讓行為變得僵化。換句話說，你越常秒答應，下次開口拒絕就越難。要斷掉它不必一步跳到拒絕 —— 只要讓解脫感<strong>延後抵達</strong>就夠了。"
            },
            {
                "title": "技能：緩衝句",
                "icon": "3",
                "content": "緩衝句是一句<strong>事先準備好、不需要當場想</strong>的話，作用是把「回應」和「決定」拆開。公式：<strong>我需要確認的事 ＋ 明確的回覆時間</strong>。兩個零件缺一不可 —— 少了時間聽起來像敷衍，少了理由聽起來像抗拒。",
                "script_list": [
                    {"situation": "同事臨時塞工作", "line": "我看一下手上的進度，一小時後回你。"},
                    {"situation": "朋友約你參加活動", "line": "我查一下那天的安排，今晚給你答覆。"},
                    {"situation": "主管加派任務", "line": "我確認一下現有排程，下午跟你回報。"},
                    {"situation": "推銷或募款", "line": "我不當場決定，需要的話我再聯絡你。"}
                ],
                "tip": "注意這四句都沒有拒絕任何事。這是刻意的 —— 這一課的目標不是拒絕，是讓你重新拿到決定權。"
            },
            {
                "title": "三個必須避開的寫法",
                "icon": "4",
                "content": "以下三種是初學者最常見的失敗，它們看起來像緩衝，其實已經把主動權交出去了：",
                "comparison": [
                    {"bad": "應該可以吧？", "why": "已經答應了，只是加了問號"},
                    {"bad": "我再看看喔", "why": "沒有時間點，對方會持續追你"},
                    {"bad": "不好意思我這個人比較…", "why": "開始解釋自己，主動權就交出去了"}
                ]
            },
            {
                "title": "會發生什麼",
                "icon": "5",
                "content": "你講完那句話的當下，那股不舒服<strong>不會消失</strong>，甚至會更明顯一點。這不是失敗 —— 這正是原本被「秒答應」偷走的東西。它通常在幾分鐘內就會退掉。"
            },
            {
                "title": "小測驗",
                "icon": "✏️",
                "quiz": [
                    {
                        "question": "你反射性答應之後，短時間內的焦慮通常會怎麼變化？",
                        "options": [
                            {"text": "A. 短期焦慮下降", "correct": True},
                            {"text": "B. 短期焦慮上升", "correct": False}
                        ],
                        "answer": "A。答應會讓不適立刻解除，這份解脫感回頭強化了反射。麻煩的正是它短期有效 —— 有效才會被學起來。"
                    },
                    {
                        "question": "下面哪一句是合格的緩衝句？",
                        "options": [
                            {"text": "A. 我看一下行程，一小時後回覆你", "correct": True},
                            {"text": "B. 應該沒問題，我再盡量安排看看", "correct": False}
                        ],
                        "answer": "A。它同時具備「要確認的事」和「明確時間」。B 已經實質答應了，只是把壓力延後 —— 那是討好，不是緩衝。"
                    },
                    {
                        "question": "緩衝句的主要目的是什麼？",
                        "options": [
                            {"text": "A. 爭取決定的時間", "correct": True},
                            {"text": "B. 委婉地表達拒絕", "correct": False}
                        ],
                        "answer": "A。緩衝句刻意不含任何拒絕。它處理的是「反射」，不是「答案」。把兩者混在一起是初學時最常見的失敗。"
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "📝",
                "tasks": [
                    "挑一句上面的緩衝句，改成你自己會講的語氣，寫下來",
                    "對著空氣唸五次，唸到不用想就能出口為止",
                    "找一個「低風險」場合用掉它 —— 家人問晚餐吃什麼、同事問要不要訂飲料都可以。第一次刻意挑不重要的場合",
                    "用完記一行：當時身體什麼感覺？對方的反應是什麼？"
                ]
            }
        ]
    },
    {
        "id": 2,
        "title": "說不的三個層次",
        "subtitle": "拒絕不是一個開關，是一道有階梯的斜坡",
        "next_topic": "迴避地圖：找出自己在哪些地方用逃避換短期舒服",
        "sections": [
            {
                "title": "為什麼「直接拒絕」對你太難",
                "icon": "1",
                "content": "多數教人拒絕的內容，一開口就要你說「不行」。對已經習慣討好的人來說，這個跨度太大 —— 失敗一次，反而<strong>強化</strong>了「開口會有壞結果」的既有信念，比不練還糟。拒絕應該當成一道<strong>階梯</strong>：從最低階開始，站穩了再往上。"
            },
            {
                "title": "三個層次",
                "icon": "2",
                "content": "由低到高，每一階都是完整可用的拒絕。你不需要一路爬到第三階才算成功。",
                "principle_grid": [
                    {"term": "第一階：延遲", "desc": "不給答案，只給時間。上一課的緩衝句就在這裡。"},
                    {"term": "第二階：條件", "desc": "答應一部分，說清楚代價。「可以，但 A 要往後延。」"},
                    {"term": "第三階：直接", "desc": "明確說不，不附加解釋。「這個我沒辦法。」"}
                ]
            },
            {
                "title": "第二階最實用",
                "icon": "3",
                "content": "「條件式拒絕」對你現階段最值得練。它不需要對抗，卻能把<strong>取捨的責任交還給對方</strong> —— 對方要嘛接受代價，要嘛自己收回要求。兩種結果你都不吃虧。",
                "script_list": [
                    {"situation": "主管加派任務", "line": "可以接，但這週的 A 案就要往後一週，你看哪個優先？"},
                    {"situation": "同事請你幫忙", "line": "我最快明天下午才有空，來得及的話沒問題。"},
                    {"situation": "朋友臨時揪約", "line": "我只能待一小時，這樣可以的話我就來。"}
                ],
                "tip": "句型是：可以 ＋ 具體代價 ＋ 把選擇丟回去。不要在後面補「不好意思」。"
            },
            {
                "title": "不要解釋、不要道歉",
                "icon": "4",
                "content": "這是討好型最難戒的兩個動作。理由講得越多，聽起來越像在徵求許可 —— 對方只要駁倒你的理由，你就沒有退路了。",
                "comparison": [
                    {"bad": "真的很抱歉，因為我最近家裡有事，然後手上又…", "why": "理由是攻擊面，越多越好被駁倒"},
                    {"bad": "如果你真的很需要的話，那我…", "why": "把決定權交還對方，等於沒拒絕"},
                    {"bad": "我可能沒辦法耶，可是…", "why": "「可是」之後通常就投降了"}
                ]
            },
            {
                "title": "小測驗",
                "icon": "✏️",
                "quiz": [
                    {
                        "question": "條件式拒絕的核心作用是什麼？",
                        "options": [
                            {"text": "A. 把取捨交還對方", "correct": True},
                            {"text": "B. 讓對方覺得虧欠", "correct": False}
                        ],
                        "answer": "A。你不否決要求，只是把它的真實代價攤開，讓對方自己決定要不要付。這不是操控，是資訊透明。"
                    },
                    {
                        "question": "拒絕時補上大量理由，通常會怎樣？",
                        "options": [
                            {"text": "A. 讓對方更能接受", "correct": False},
                            {"text": "B. 增加被駁倒風險", "correct": True}
                        ],
                        "answer": "B。每個理由都是一個攻擊面。對方只要解決掉你的理由，你就失去立場了。少即是多。"
                    },
                    {
                        "question": "現階段最該優先練習哪一階？",
                        "options": [
                            {"text": "A. 第二階的條件式", "correct": True},
                            {"text": "B. 第三階的直接式", "correct": False}
                        ],
                        "answer": "A。第三階需要的心理強度還沒長出來，貿然練失敗率高，而失敗會強化原本的信念。先在第二階累積成功經驗。"
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "📝",
                "tasks": [
                    "回想這週被要求的一件事，把它改寫成一句「條件式拒絕」，寫下來",
                    "檢查你寫的句子有沒有出現「不好意思」「抱歉」，有的話刪掉再唸一次",
                    "本週找一次機會實際使用第二階。挑中低風險的對象，不要一開始就挑主管",
                    "記下對方的反應。多數時候它會比你預想的平淡很多 —— 這個落差就是你要蒐集的證據"
                ]
            }
        ]
    }
]


def get_next_lesson_id():
    """掃描既有檔案，取得下一個課程編號。"""
    existing = [f for f in os.listdir('.') if f.startswith('mind-lesson-') and f.endswith('.html')]
    if not existing:
        return 1

    max_id = 0
    for filename in existing:
        try:
            lesson_id = int(filename.split('-')[2].split('.')[0])
            max_id = max(max_id, lesson_id)
        except (IndexError, ValueError):
            pass

    return max_id + 1


def get_previous_topics():
    """掃描已生成的課程標題，避免新課主題重複。"""
    topics = [lesson["title"] for lesson in LESSONS]
    existing = sorted(f for f in os.listdir(".") if f.startswith("mind-lesson-") and f.endswith(".html"))
    for filename in existing:
        try:
            with open(filename, encoding="utf-8") as f:
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


LESSON_SCHEMA_INSTRUCTIONS = """\
請只回傳一個合法的 JSON 物件（不要加任何說明文字、不要用 markdown code block），結構必須完全符合：

{
  "title": "課程主標題（繁體中文，簡短有力，不超過 12 字）",
  "subtitle": "一句話副標題",
  "next_topic": "下一課預告的主題名稱",
  "sections": [
    {
      "title": "小節標題",
      "icon": "1",
      "content": "說明文字，可用 <strong> 標籤強調重點"
    },
    {
      "title": "概念拆解",
      "icon": "2",
      "content": "說明文字",
      "principle_grid": [
        {"term": "概念名稱", "desc": "一到兩句說明"}
      ]
    },
    {
      "title": "可以直接用的句型",
      "icon": "3",
      "content": "說明文字",
      "tip": "一句使用提醒",
      "script_list": [
        {"situation": "情境描述", "line": "可以照唸的句子"}
      ]
    },
    {
      "title": "要避開的說法",
      "icon": "4",
      "content": "說明文字",
      "comparison": [
        {"bad": "錯誤的說法", "why": "為什麼這樣不行"}
      ]
    },
    {
      "title": "小測驗",
      "icon": "✏️",
      "quiz": [
        {
          "question": "題目",
          "options": [
            {"text": "A. 選項", "correct": true},
            {"text": "B. 選項", "correct": false}
          ],
          "answer": "解說，說明為什麼是這個答案"
        }
      ]
    },
    {
      "title": "今日任務",
      "icon": "📝",
      "tasks": ["可在日常生活中執行的低風險任務"]
    }
  ]
}

格式要求：
- 每個 section 只需包含它用得到的欄位。
- sections 至少 5 個，且必須包含「小測驗」與「今日任務」。
- 測驗每題只給兩個選項，且兩個選項的<strong>字數必須相同</strong>，不可從長短看出答案。
- 一課只教一件事。不要在同一課塞入兩個以上的核心概念。
- 任務必須具體到「今天就能做」，不可以是「多多練習」這種空話。
"""


def generate_lesson_via_llm(next_id, previous_topics):
    """呼叫 OpenAI 相容 API 生成下一課內容（JSON），失敗回傳 None。

    環境變數：
      LLM_API_URL — 完整 chat completions 端點
      LLM_API_KEY — API key（帶在 Authorization: Bearer）
      LLM_MODEL   — model 名稱
    """
    api_url = os.environ.get("LLM_API_URL")
    api_key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL")

    if not api_url or not api_key or not model:
        print("缺少 LLM_API_URL / LLM_API_KEY / LLM_MODEL，無法呼叫 LLM 生成課程")
        return None

    topics_list = "、".join(previous_topics) if previous_topics else "（尚無）"
    prompt = (
        f"你是一位受過認知行為治療（CBT）與接納承諾治療（ACT）訓練的心理教育工作者，"
        f"正在為一位繁體中文使用者撰寫心靈成長自學課程的第 {next_id} 課。\n\n"
        "學習者的處境：容易焦慮；遇事第一反應是逃避；有討好型傾向，不敢爭取自己的權益；"
        "容易被片面資訊與他人評論影響而缺乏自主判斷；口語表達的邏輯組織較弱。\n\n"
        f"既定學習路徑（必須依序推進，不可跳階或自由發散）：\n{CURRICULUM}\n"
        f"已經教過的主題依序是：{topics_list}。\n"
        "請沿著上面的路徑挑選下一個主題，絕對不要與已教過的主題重複或高度相似。\n\n"
        f"{SAFETY_RULES}\n"
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

    if not lesson.get("title") or not lesson.get("sections"):
        print("LLM 回傳的 JSON 缺少必要欄位")
        return None

    lesson["id"] = next_id
    return lesson


def generate_html(lesson):
    """生成自帶 CSS 的單一 HTML 課程頁（供 App 的 WebView 直接顯示）。"""
    lesson_num = f"{lesson['id']:02d}"

    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="zh-Hant">')
    parts.append('<head>')
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    parts.append(f'<title>心靈成長 {lesson_num} — {lesson["title"]}</title>')
    parts.append('<style>')
    parts.append(get_css())
    parts.append('</style>')
    parts.append('</head>')
    parts.append('<body>')
    parts.append('<div class="container">')

    parts.append('  <div class="lesson-header">')
    parts.append(f'    <span class="lesson-number">第 {lesson_num} 課</span>')
    parts.append(f'    <h1 class="lesson-title">{lesson["title"]}</h1>')
    parts.append(f'    <p class="lesson-subtitle">{lesson["subtitle"]}</p>')
    parts.append('  </div>')

    for section in lesson['sections']:
        parts.append('')
        parts.append('  <div class="section">')
        parts.append(
            f'    <div class="section-title"><span class="icon">{section["icon"]}</span> {section["title"]}</div>'
        )

        if 'content' in section:
            parts.append(f'    <p>{section["content"]}</p>')

        if 'principle_grid' in section:
            parts.append('    <div class="principle-grid">')
            for item in section['principle_grid']:
                parts.append('      <div class="principle-card">')
                parts.append(f'        <div class="principle-term">{item["term"]}</div>')
                parts.append(f'        <div class="principle-desc">{item["desc"]}</div>')
                parts.append('      </div>')
            parts.append('    </div>')

        if 'script_list' in section:
            parts.append('    <div class="script-box">')
            parts.append('      <h4>可以直接照唸</h4>')
            parts.append('      <ul class="script-list">')
            for item in section['script_list']:
                parts.append('        <li>')
                parts.append(f'          <span class="situation">{item["situation"]}</span>')
                parts.append(f'          <span class="line">{item["line"]}</span>')
                parts.append('        </li>')
            parts.append('      </ul>')
            parts.append('    </div>')
            tip = section.get("tip", "")
            if tip:
                parts.append(f'    <p class="tip">💡 {tip}</p>')

        if 'comparison' in section:
            parts.append('    <table class="compare">')
            parts.append('      <thead><tr><th>不要說</th><th>為什麼</th></tr></thead>')
            parts.append('      <tbody>')
            for item in section['comparison']:
                parts.append(
                    f'        <tr><td class="bad">{item["bad"]}</td><td>{item["why"]}</td></tr>'
                )
            parts.append('      </tbody>')
            parts.append('    </table>')

        if 'quiz' in section:
            parts.append('    <div class="quiz-box">')
            parts.append('      <h4>請先自己作答，再看解說</h4>')
            for idx, item in enumerate(section['quiz'], 1):
                parts.append('      <div class="quiz-item">')
                parts.append(f'        <div class="quiz-question">{idx}. {item["question"]}</div>')
                parts.append('        <ul class="quiz-options">')
                for opt in item['options']:
                    correct_attr = 'true' if opt['correct'] else 'false'
                    parts.append(f'          <li onclick="checkAnswer(this, {correct_attr})">{opt["text"]}</li>')
                parts.append('        </ul>')
                parts.append('        <button class="reveal-btn" onclick="revealAnswer(this)">查看解說</button>')
                parts.append(f'        <div class="answer">{item["answer"]}</div>')
                parts.append('      </div>')
            parts.append('    </div>')

        if 'tasks' in section:
            parts.append('    <div class="task-box">')
            parts.append('      <h4>完成後才算學會</h4>')
            parts.append('      <ol>')
            for task in section['tasks']:
                parts.append(f'        <li>{task}</li>')
            parts.append('      </ol>')
            parts.append('    </div>')

        parts.append('  </div>')

    parts.append('')
    parts.append('  <div class="disclaimer">')
    parts.append('    本課程為心理教育與技能訓練，不是心理治療，也不提供診斷。')
    parts.append('    若焦慮已明顯影響睡眠、工作或身體健康，請優先尋求專業協助，本課程作為輔助。')
    parts.append('  </div>')

    parts.append('  <div class="lesson-footer">')
    parts.append(f'    <p>心靈成長 · 第 {lesson_num} 課 · {datetime.now().strftime("%Y-%m-%d")}</p>')
    parts.append(f'    <p class="next">下一課：{lesson["next_topic"]}</p>')
    parts.append('  </div>')
    parts.append('</div>')

    parts.append('')
    parts.append('<script>')
    parts.append('function checkAnswer(el, isCorrect) {')
    parts.append('  const siblings = el.parentElement.querySelectorAll("li");')
    parts.append('  siblings.forEach(s => { s.style.pointerEvents = "none"; });')
    parts.append('  if (isCorrect) {')
    parts.append('    el.classList.add("correct");')
    parts.append('  } else {')
    parts.append('    el.classList.add("wrong");')
    parts.append('    siblings.forEach(s => {')
    parts.append('      if (s.onclick && s.onclick.toString().includes("true")) {')
    parts.append('        s.classList.add("correct");')
    parts.append('      }')
    parts.append('    });')
    parts.append('  }')
    parts.append('}')
    parts.append('')
    parts.append('function revealAnswer(btn) {')
    parts.append('  const answer = btn.nextElementSibling;')
    parts.append('  const open = answer.style.display === "block";')
    parts.append('  answer.style.display = open ? "none" : "block";')
    parts.append('  btn.textContent = open ? "查看解說" : "隱藏解說";')
    parts.append('}')
    parts.append('</script>')
    parts.append('</body>')
    parts.append('</html>')

    return '\n'.join(parts)


def get_css():
    return """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    background: #fbfaf7;
    color: #24211d;
    line-height: 1.9;
    padding: 3rem 1.5rem;
    -webkit-font-smoothing: antialiased;
  }
  .container { max-width: 680px; margin: 0 auto; }

  .lesson-header {
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #e5e0d6;
  }
  .lesson-number {
    display: inline-block;
    background: #2f6f5e;
    color: #fff;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 0.3rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.1rem;
  }
  .lesson-title {
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    margin-bottom: 0.5rem;
  }
  .lesson-subtitle { font-size: 1rem; color: #6f6a62; }

  .section { margin-bottom: 2.8rem; }
  .section-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }
  .section-title .icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px; height: 28px;
    border-radius: 8px;
    background: #2f6f5e1f;
    color: #2f6f5e;
    font-size: 0.85rem;
    font-weight: 800;
    flex-shrink: 0;
  }
  .section p { margin-bottom: 1rem; }
  .tip { color: #7d776d; font-size: 0.9rem; }

  .principle-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.9rem;
    margin: 1.2rem 0;
  }
  .principle-card {
    background: #fff;
    border: 1px solid #e5e0d6;
    border-radius: 12px;
    padding: 1.1rem;
  }
  .principle-term {
    font-weight: 700;
    color: #2f6f5e;
    margin-bottom: 0.35rem;
  }
  .principle-desc { font-size: 0.9rem; color: #5b564e; line-height: 1.7; }

  .script-box {
    background: #f2f7f4;
    border: 1px solid #cfe2d8;
    border-radius: 12px;
    padding: 1.4rem;
    margin: 1.2rem 0 0.8rem;
  }
  .script-box h4 { font-size: 0.95rem; color: #2f6f5e; margin-bottom: 0.8rem; }
  .script-list { list-style: none; }
  .script-list li {
    padding: 0.7rem 0;
    border-bottom: 1px dashed #d8e5dd;
  }
  .script-list li:last-child { border-bottom: none; }
  .script-list .situation {
    display: block;
    font-size: 0.8rem;
    color: #7d8f86;
    margin-bottom: 0.15rem;
  }
  .script-list .line { font-weight: 600; color: #1f4a3e; }

  table.compare {
    width: 100%;
    border-collapse: collapse;
    margin: 1.2rem 0;
    font-size: 0.92rem;
  }
  table.compare th {
    text-align: left;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    color: #8a857b;
    font-weight: 600;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e5e0d6;
  }
  table.compare td {
    padding: 0.7rem 0.8rem 0.7rem 0;
    border-bottom: 1px solid #f0ece3;
    vertical-align: top;
  }
  table.compare td.bad { color: #9d3e26; font-weight: 600; }

  .quiz-box {
    background: #fff;
    border: 2px solid #2f6f5e33;
    border-radius: 12px;
    padding: 1.4rem;
  }
  .quiz-box h4 { font-size: 1rem; margin-bottom: 1rem; }
  .quiz-item {
    margin-bottom: 1.3rem;
    padding-bottom: 1.3rem;
    border-bottom: 1px solid #f2efe8;
  }
  .quiz-item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
  .quiz-question { font-weight: 600; margin-bottom: 0.6rem; }
  .quiz-options { list-style: none; }
  .quiz-options li {
    padding: 0.55rem 0.9rem;
    margin-bottom: 0.35rem;
    border: 1px solid #e5e0d6;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.93rem;
    transition: background 0.15s;
  }
  .quiz-options li:hover { background: #f5f8f6; }
  .quiz-options li.correct { background: #dff0e6; border-color: #7cb79b; font-weight: 600; }
  .quiz-options li.wrong { background: #fbe6e0; border-color: #d9a08d; }

  .reveal-btn {
    margin-top: 0.8rem;
    padding: 0.45rem 1.2rem;
    background: #2f6f5e;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
  }
  .answer {
    display: none;
    margin-top: 0.7rem;
    padding-left: 0.9rem;
    border-left: 2px solid #cfe2d8;
    color: #4a5f56;
    font-size: 0.9rem;
  }

  .task-box {
    background: #fdf8ee;
    border: 1px solid #ecdfc4;
    border-radius: 12px;
    padding: 1.4rem;
  }
  .task-box h4 { font-size: 0.95rem; color: #8a6d2f; margin-bottom: 0.7rem; }
  .task-box ol { padding-left: 1.3rem; }
  .task-box li { padding: 0.4rem 0; }

  .disclaimer {
    margin-top: 3rem;
    padding: 1rem 1.2rem;
    background: #f4f2ee;
    border-radius: 8px;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #6f6a62;
  }

  .lesson-footer {
    text-align: center;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e5e0d6;
    color: #9b958b;
    font-size: 0.82rem;
  }
  .lesson-footer .next { margin-top: 0.3rem; }
"""


def main():
    print("開始生成心靈成長課程...")

    next_id = get_next_lesson_id()
    print(f"將生成第 {next_id:02d} 課")

    if next_id <= len(LESSONS):
        lesson = LESSONS[next_id - 1]
    else:
        lesson = generate_lesson_via_llm(next_id, get_previous_topics())
        if lesson is None:
            print("LLM 生成失敗，本次不產生新課程（避免重複舊內容佔用課號）")
            return
        print(f"已透過 LLM API 生成第 {next_id:02d} 課內容")

    html_content = generate_html(lesson)
    filename = f"mind-lesson-{lesson['id']:02d}.html"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"已成功生成課程: {filename}")
    print(f"   標題: {lesson['title']}")
    print(f"   副標題: {lesson['subtitle']}")
    print(f"   檔案大小: {len(html_content)} bytes")
    print(f"   生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
