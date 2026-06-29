#!/usr/bin/env python3
"""
自動生成法文教學課程腳本
根據 teach skill 的流程，生成精美的 HTML 法文課程
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

# 課程資料庫 - 法文教學內容
LESSONS = [
    {
        "id": 1,
        "title": "法語元音字母與基本發音",
        "subtitle": "認識 26 個法文字母，掌握 6 個核心元音音",
        "next_topic": "法語鼻化元音（an, in, on, un）",
        "sections": [
            {
                "title": "法語字母簡介",
                "icon": "1",
                "content": "法語使用與英文相同的 <strong>26 個拉丁字母</strong>，但發音規則大不相同。法語是<strong>拼讀相對規律</strong>的語言，只要掌握基本規則，看到單字就能大致讀出來。第一課我們先認識最重要的 <strong>6 個元音音</strong>，它們是法語發音的基石。"
            },
            {
                "title": "6 個核心元音音",
                "icon": "2",
                "content": "以下 6 個元音音是初學階段最重要的基礎。每個音都配有法語單字範例，請大聲跟讀。",
                "pronunciation_grid": [
                    {"letter": "/a/", "desc": "嘴巴張大，像說「啊」", "example": "patte", "meaning": "貓爪"},
                    {"letter": "/e/", "desc": "嘴角向兩側拉，像微笑", "example": "cle", "meaning": "鑰匙"},
                    {"letter": "/ɛ/", "desc": "嘴巴微張，像說「哎」", "example": "mer", "meaning": "大海"},
                    {"letter": "/i/", "desc": "嘴角用力拉開，像說「一」", "example": "oui", "meaning": "是"},
                    {"letter": "/u/", "desc": "嘴唇圓圓突出，像「烏」但更緊", "example": "tu", "meaning": "你"},
                    {"letter": "/y/", "desc": "嘴巴像說 /u/，但舌頭位置像說 /i/", "example": "tu", "meaning": "你"}
                ]
            },
            {
                "title": "跟練時間",
                "icon": "🎙",
                "content": "請對著鏡子，大聲朗讀以下每個單字至少 3 次",
                "tip": "法語的元音要發得「清晰、乾淨、不滑動」。不要像英文那樣有雙元音的滑動感。",
                "follow_list": [
                    {"word": "patte", "ipa": "/pat/", "meaning": "貓的爪子"},
                    {"word": "cle", "ipa": "/kle/", "meaning": "鑰匙"},
                    {"word": "mer", "ipa": "/mɛʁ/", "meaning": "大海"},
                    {"word": "oui", "ipa": "/wi/", "meaning": "是"},
                    {"word": "tu", "ipa": "/ty/", "meaning": "你"},
                    {"word": "rue", "ipa": "/ʁy/", "meaning": "街道"},
                    {"word": "barbe", "ipa": "/baʁb/", "meaning": "鬍鬚"},
                    {"word": "frere", "ipa": "/fʁɛʁ/", "meaning": "兄弟"}
                ]
            },
            {
                "title": "重點對照：/e/ 與 /ɛ/ 的差別",
                "icon": "⚡",
                "content": "這兩個音是初學者最容易混淆的。關鍵差別在於<strong>嘴巴張開的大小</strong>：",
                "comparison": [
                    {"letter": "/e/", "desc": "嘴巴閉合較小，嘴角拉開", "example": "cle /kle/", "note": "嘴巴幾乎不張開"},
                    {"letter": "/ɛ/", "desc": "嘴巴張開較大", "example": "mer /mɛʁ/", "note": "嘴巴明顯張開"}
                ]
            },
            {
                "title": "小測驗",
                "icon": "✏️",
                "quiz": [
                    {
                        "question": "下列哪個單字的元音發 /i/ 音？",
                        "options": [
                            {"text": "A. mer", "correct": False},
                            {"text": "B. oui", "correct": True},
                            {"text": "C. patte", "correct": False}
                        ],
                        "answer": "正確答案：B. oui（發 /wi/ 音，包含 /i/）"
                    },
                    {
                        "question": "/y/ 音發音時，嘴唇是什麼形狀？",
                        "options": [
                            {"text": "A. 圓圓突出", "correct": True},
                            {"text": "B. 向兩側拉開像微笑", "correct": False},
                            {"text": "C. 自然張開", "correct": False}
                        ],
                        "answer": "正確答案：A. 圓圓突出（/y/ 是圓唇音）"
                    },
                    {
                        "question": "「rue」的發音中包含哪個元音？",
                        "options": [
                            {"text": "A. /i/", "correct": False},
                            {"text": "B. /u/", "correct": False},
                            {"text": "C. /y/", "correct": True}
                        ],
                        "answer": "正確答案：C. /y/（rue 發 /ʁy/）"
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "📝",
                "tasks": [
                    "拿起手機錄音功能，錄下自己朗讀「跟練時間」中的 8 個單字",
                    "聽自己的錄音，檢查每個元音是否發得清晰、不滑動",
                    "在紙上寫下 patte、cle、mer、oui、tu、rue 各 5 遍，同時大聲朗讀"
                ]
            }
        ]
    },
    {
        "id": 2,
        "title": "法語鼻化元音（an, in, on, un）",
        "subtitle": "掌握四個法語特有的鼻化音，讓你的法語更道地",
        "next_topic": "法語輔音發音（h 發音、小舌音 r）",
        "sections": [
            {
                "title": "什麼是鼻化音？",
                "icon": "1",
                "content": "法語有 <strong>三個鼻化元音</strong>，是法語最獨特的發音特色之一。發鼻化音時，<strong>空氣同時從口腔和鼻腔流出</strong>，手指摸著鼻子會感覺到震動。今天我們要學習最常见的四個拼法：<strong>an, in, on, un</strong>。"
            },
            {
                "title": "四個鼻化音發音",
                "icon": "2",
                "content": "每個鼻化音都有特定的發音方法和範例單字，請仔細聽並跟著練習。",
                "pronunciation_grid": [
                    {"letter": "/ɑ̃/", "desc": "拼法：an, am, aim", "example": "vent", "meaning": "風"},
                    {"letter": "/ɛ̃/", "desc": "拼法：in, im, ain, aing", "example": "fin", "meaning": "好的"},
                    {"letter": "/ɔ̃/", "desc": "拼法：on, om", "example": "bon", "meaning": "好的"},
                    {"letter": "/œ̃/", "desc": "拼法：un, um", "example": "une", "meaning": "一"}
                ]
            },
            {
                "title": "跟練時間",
                "icon": "🎙",
                "content": "請對著鏡子，大聲朗讀以下每個單字至少 3 次",
                "tip": "發鼻化音時，試著把手指放在鼻子上，應該能感覺到微微的震動。",
                "follow_list": [
                    {"word": "vent", "ipa": "/vɑ̃/", "meaning": "風"},
                    {"word": "pain", "ipa": "/pɛ̃/", "meaning": "麵包"},
                    {"word": "bon", "ipa": "/bɔ̃/", "meaning": "好的"},
                    {"word": "une", "ipa": "/yn/", "meaning": "一（陰性）"},
                    {"word": "champ", "ipa": "/ʃɑ̃/", "meaning": "田野"},
                    {"word": "main", "ipa": "/mɛ̃/", "meaning": "手"},
                    {"word": "monde", "ipa": "/mɔ̃d/", "meaning": "世界"},
                    {"word": "lune", "ipa": "/lyn/", "meaning": "月亮"}
                ]
            },
            {
                "title": "鼻化音拼法規則",
                "icon": "⚡",
                "content": "同樣的鼻化音可能有不同的拼法，以下是常見規則：",
                "spelling_rules": [
                    {
                        "sound": "/ɑ̃/ 的拼法",
                        "items": [
                            {"spell": "an", "example": "enfant", "meaning": "孩子"},
                            {"spell": "am", "example": "ample", "meaning": "大量的"},
                            {"spell": "aim", "example": "faim", "meaning": "餓"}
                        ]
                    },
                    {
                        "sound": "/ɛ̃/ 的拼法",
                        "items": [
                            {"spell": "in", "example": "fin", "meaning": "精細的"},
                            {"spell": "ain", "example": "pain", "meaning": "麵包"},
                            {"spell": "aing", "example": "parking", "meaning": "停車"}
                        ]
                    }
                ]
            },
            {
                "title": "小測驗",
                "icon": "✏️",
                "quiz": [
                    {
                        "question": "「pain」（麵包）中的鼻化音發什麼音？",
                        "options": [
                            {"text": "A. /ɑ̃/", "correct": False},
                            {"text": "B. /ɛ̃/", "correct": True},
                            {"text": "C. /ɔ̃/", "correct": False}
                        ],
                        "answer": "正確答案：B. /ɛ̃/（ain 發 /ɛ̃/ 音）"
                    },
                    {
                        "question": "下列哪個單字發 /ɔ̃/ 音？",
                        "options": [
                            {"text": "A. vent", "correct": False},
                            {"text": "B. fin", "correct": False},
                            {"text": "C. bon", "correct": True}
                        ],
                        "answer": "正確答案：C. bon（on 發 /ɔ̃/ 音）"
                    },
                    {
                        "question": "「lune」（月亮）的鼻化音屬於哪一種？",
                        "options": [
                            {"text": "A. /yn/ (un)", "correct": True},
                            {"text": "B. /ɑ̃/ (an)", "correct": False},
                            {"text": "C. /ɛ̃/ (in)", "correct": False}
                        ],
                        "answer": "正確答案：A. /yn/（un 發 /yn/ 或 /œ̃/ 音）"
                    }
                ]
            },
            {
                "title": "今日任務",
                "icon": "📝",
                "tasks": [
                    "拿起手機錄音功能，錄下自己朗讀「跟練時間」中的 8 個鼻化音單字",
                    "對比每個鼻化音，確認鼻子有震動感",
                    "找 3 個含有鼻化音的法語歌曲，試著跟唱並辨識鼻化音的位置"
                ]
            }
        ]
    }
]

def get_next_lesson_id():
    """獲取下一個課程 ID"""
    existing_files = [f for f in os.listdir('.') if f.startswith('french-lesson-') and f.endswith('.html')]
    if not existing_files:
        return 1
    
    max_id = 0
    for file in existing_files:
        try:
            lesson_id = int(file.split('-')[2].split('.')[0])
            max_id = max(max_id, lesson_id)
        except:
            pass
    
    return max_id + 1

def speak_button(text):
    """產生一個會用瀏覽器內建 Web Speech API 朗讀法語單字的按鈕。
    不需要產生/上傳任何音檔，iOS 的 WKWebView 也支援 speechSynthesis。"""
    clean_text = text.split('/')[0].strip()  # 去掉像 "cle /kle/" 裡的 IPA 部分
    # 法語單字常見如 l'eau、c'est 這類含單引號的字，json.dumps 不會跳脫單引號，
    # 因此另外把它轉成 HTML 實體，避免提早結束用單引號包住的 onclick 屬性。
    js_literal = json.dumps(clean_text).replace("'", "&#39;")
    return f"<button class=\"speak-btn\" onclick='speakFrench({js_literal})' aria-label=\"播放發音\">🔊</button>"


def generate_html(lesson):
    """生成精美的 HTML 課程頁面"""
    lesson_num = f"{lesson['id']:02d}"
    
    # Start HTML
    html_parts = []
    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html lang="zh-Hant">')
    html_parts.append('<head>')
    html_parts.append('<meta charset="UTF-8">')
    html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_parts.append(f'<title>法語課 {lesson_num} — {lesson["title"]}</title>')
    html_parts.append('<style>')
    html_parts.append(get_css())
    html_parts.append('</style>')
    html_parts.append('</head>')
    html_parts.append('<body>')
    html_parts.append('<div class="container">')
    
    # Header
    html_parts.append('')
    html_parts.append('  <!-- Header -->')
    html_parts.append('  <div class="lesson-header">')
    html_parts.append(f'    <span class="lesson-number">LEÇON {lesson_num}</span>')
    html_parts.append(f'    <h1 class="lesson-title">{lesson["title"]}</h1>')
    html_parts.append(f'    <p class="lesson-subtitle">{lesson["subtitle"]}</p>')
    html_parts.append('  </div>')
    
    # Generate sections
    for section in lesson['sections']:
        html_parts.append('')
        html_parts.append(f'  <!-- Section {section["icon"]}: {section["title"]} -->')
        html_parts.append('  <div class="section">')
        html_parts.append(f'    <div class="section-title"><span class="icon">{section["icon"]}</span> {section["title"]}</div>')
        
        # Content paragraph
        if 'content' in section:
            html_parts.append(f'    <p>{section["content"]}</p>')
        
        # Pronunciation grid
        if 'pronunciation_grid' in section:
            html_parts.append('    <div class="pron-grid">')
            for item in section['pronunciation_grid']:
                html_parts.append('      <div class="pron-card">')
                html_parts.append(f'        <div class="pron-letter">{item["letter"]}</div>')
                html_parts.append(f'        <div class="pron-ipa">{item["desc"]}</div>')
                html_parts.append(f'        <div class="pron-example"><em>{item["example"]}</em>（{item["meaning"]}）{speak_button(item["example"])}</div>')
                html_parts.append('      </div>')
            html_parts.append('    </div>')

        # Follow-along list
        if 'follow_list' in section:
            html_parts.append('    <div class="follow-box">')
            html_parts.append(f'      <h4>{section["content"]}</h4>')
            html_parts.append('      <ul class="follow-list">')
            for item in section['follow_list']:
                html_parts.append('        <li>')
                html_parts.append(f'          <span class="word">{item["word"]}</span>')
                html_parts.append(f'          <span class="ipa">{item["ipa"]}</span>')
                html_parts.append(f'          <span class="meaning">—— {item["meaning"]}</span>')
                html_parts.append(f'          {speak_button(item["word"])}')
                html_parts.append('        </li>')
            html_parts.append('      </ul>')
            html_parts.append('    </div>')
            tip_text = section.get("tip", "")
            if tip_text:
                html_parts.append(f'    <p style="color: #888; font-size: 0.9rem; margin-bottom: 1rem;">💡 小技巧：{tip_text}</p>')

        # Comparison grid
        if 'comparison' in section:
            html_parts.append('    <div class="pron-grid">')
            for item in section['comparison']:
                html_parts.append('      <div class="pron-card">')
                html_parts.append(f'        <div class="pron-letter">{item["letter"]}</div>')
                html_parts.append(f'        <div class="pron-ipa">{item["desc"]}</div>')
                html_parts.append(f'        <div class="pron-example">{item["example"]}{speak_button(item["example"])}<br>{item["note"]}</div>')
                html_parts.append('      </div>')
            html_parts.append('    </div>')

        # Spelling rules
        if 'spelling_rules' in section:
            for rule_group in section['spelling_rules']:
                html_parts.append(f'      <h4 style="margin-top: 1rem;">{rule_group["sound"]}</h4>')
                html_parts.append('      <ul class="follow-list">')
                for item in rule_group['items']:
                    html_parts.append(f'        <li><span class="word">{item["spell"]}</span> <span class="ipa">{item["example"]}</span> <span class="meaning">{item["meaning"]}</span> {speak_button(item["spell"])}</li>')
                html_parts.append('      </ul>')
        
        # Quiz
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
        
        # Tasks
        if 'tasks' in section:
            html_parts.append('    <div class="follow-box">')
            html_parts.append('      <h4>請完成以下練習</h4>')
            html_parts.append('      <ol style="padding-left: 1.5rem;">')
            for task in section['tasks']:
                html_parts.append(f'        <li style="padding: 0.5rem 0;">{task}</li>')
            html_parts.append('      </ol>')
            html_parts.append('    </div>')
        
        html_parts.append('  </div>')
    
    # Footer
    html_parts.append('')
    html_parts.append('  <!-- Footer -->')
    html_parts.append('  <div class="lesson-footer">')
    html_parts.append(f'    <p>法語課 {lesson_num} · {lesson["title"]} · {datetime.now().year}</p>')
    html_parts.append(f'    <p style="margin-top: 0.3rem;">下一課預告：{lesson["next_topic"]}</p>')
    html_parts.append('  </div>')
    html_parts.append('')
    html_parts.append('</div>')
    
    # JavaScript
    html_parts.append('')
    html_parts.append('<script>')
    html_parts.append('function checkAnswer(el, isCorrect) {')
    html_parts.append('  const siblings = el.parentElement.querySelectorAll(\'li\');')
    html_parts.append('  siblings.forEach(s => {')
    html_parts.append('    s.style.pointerEvents = \'none\';')
    html_parts.append('  });')
    html_parts.append('  if (isCorrect) {')
    html_parts.append('    el.classList.add(\'correct\');')
    html_parts.append('  } else {')
    html_parts.append('    el.classList.add(\'wrong\');')
    html_parts.append('    siblings.forEach(s => {')
    html_parts.append('      if (s.onclick && s.onclick.toString().includes(\'true\')) {')
    html_parts.append('        s.classList.add(\'correct\');')
    html_parts.append('      }')
    html_parts.append('    });')
    html_parts.append('  }')
    html_parts.append('}')
    html_parts.append('')
    html_parts.append('function revealAnswer(btn) {')
    html_parts.append('  const answer = btn.nextElementSibling;')
    html_parts.append('  if (answer.style.display === \'block\') {')
    html_parts.append('    answer.style.display = \'none\';')
    html_parts.append('    btn.textContent = \'查看答案\';')
    html_parts.append('  } else {')
    html_parts.append('    answer.style.display = \'block\';')
    html_parts.append('    btn.textContent = \'隱藏答案\';')
    html_parts.append('  }')
    html_parts.append('}')
    html_parts.append('')
    html_parts.append('function speakFrench(text) {')
    html_parts.append('  if (!(\'speechSynthesis\' in window)) return;')
    html_parts.append('  window.speechSynthesis.cancel();')
    html_parts.append('  const utterance = new SpeechSynthesisUtterance(text);')
    html_parts.append('  utterance.lang = \'fr-FR\';')
    html_parts.append('  utterance.rate = 0.85;')
    html_parts.append('  window.speechSynthesis.speak(utterance);')
    html_parts.append('}')
    html_parts.append('</script>')
    html_parts.append('</body>')
    html_parts.append('</html>')
    
    return '\n'.join(html_parts)

def get_css():
    """返回 CSS 樣式"""
    return """
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

  /* Pronunciation cards */
  .pron-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  .pron-card {
    background: #fff;
    border: 1px solid #e8ecf1;
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: box-shadow 0.2s;
  }
  .pron-card:hover { box-shadow: 0 4px 16px #667eea22; }
  .pron-letter {
    font-size: 2rem;
    font-weight: 800;
    color: #667eea;
    margin-bottom: 0.3rem;
  }
  .pron-ipa {
    font-size: 0.9rem;
    color: #888;
    margin-bottom: 0.4rem;
    font-family: "Lucida Sans Unicode", sans-serif;
  }
  .pron-example {
    font-size: 0.85rem;
    color: #555;
  }
  .pron-example em {
    color: #667eea;
    font-style: normal;
    font-weight: 600;
  }

  /* Follow-along box */
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
  .follow-list {
    list-style: none;
    padding: 0;
  }
  .follow-list li {
    padding: 0.6rem 0;
    border-bottom: 1px dashed #e0e4ef;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-size: 1rem;
  }
  .follow-list li:last-child { border-bottom: none; }
  .follow-list .word {
    font-weight: 700;
    color: #4338ca;
    min-width: 80px;
  }
  .follow-list .ipa {
    color: #888;
    font-size: 0.85rem;
    min-width: 80px;
  }
  .follow-list .meaning { color: #555; }

  /* Speak button (Web Speech API) */
  .speak-btn {
    border: none;
    background: #eef2ff;
    color: #4338ca;
    border-radius: 999px;
    width: 1.8rem;
    height: 1.8rem;
    font-size: 0.95rem;
    line-height: 1;
    cursor: pointer;
    margin-left: 0.4rem;
    flex-shrink: 0;
  }
  .speak-btn:active { background: #c7d2fe; }

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

  /* Reveal button */
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

  /* Footer */
  .lesson-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 2px solid #e8ecf1;
    color: #999;
    font-size: 0.85rem;
  }
"""

LESSON_SCHEMA_INSTRUCTIONS = """\
請只回傳一個合法的 JSON 物件（不要加任何說明文字、不要用 markdown code block），結構必須完全符合：

{
  "title": "課程主標題（繁體中文，可包含法語術語）",
  "subtitle": "一句話副標題",
  "next_topic": "下一課預告的主題名稱",
  "sections": [
    {
      "title": "小節標題",
      "icon": "1",
      "content": "說明文字，可用 <strong> 標籤強調重點"
    },
    {
      "title": "發音對照表",
      "icon": "2",
      "content": "說明文字",
      "pronunciation_grid": [
        {"letter": "音標或拼法", "desc": "怎麼發這個音", "example": "法語單字", "meaning": "中文意思"}
      ]
    },
    {
      "title": "跟練時間",
      "icon": "🎙",
      "content": "說明文字（會當作跟練清單的標題）",
      "tip": "一句發音小技巧",
      "follow_list": [
        {"word": "法語單字", "ipa": "/IPA/", "meaning": "中文意思"}
      ]
    },
    {
      "title": "重點對照",
      "icon": "⚡",
      "content": "說明文字",
      "comparison": [
        {"letter": "音標", "desc": "說明", "example": "範例單字", "note": "提示"}
      ]
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
      "icon": "📝",
      "tasks": ["練習任務一", "練習任務二"]
    }
  ]
}

每個 section 只需要包含它需要的欄位（例如純說明的 section 只要 title/icon/content，不用加 pronunciation_grid）。
"sections" 至少要有 4 個小節，建議包含「跟練時間」與「小測驗」兩種。
"""


def generate_lesson_via_llm(next_id, previous_topics):
    """呼叫第三方 OpenAI 相容 API 生成下一堂法文課的內容（JSON），失敗時回傳 None。

    透過環境變數設定第三方服務（例如 agnes）：
      LLM_API_URL   — 完整的 chat completions 端點，例如
                       https://your-agnes-endpoint.example.com/v1/chat/completions
      LLM_API_KEY   — 該服務的 API key（會帶在 Authorization: Bearer 裡）
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
        f"你是一位法語教師，正在為一套給繁體中文使用者的自學法語課程撰寫第 {next_id} 課的教材。\n"
        f"已經教過的主題依序是：{topics_list}。\n"
        "請挑選一個循序漸進、難度適中地往下延伸的新主題（例如：先學過母音、鼻化音之後，"
        "可以接輔音發音、聯誦規則、基本問候語、數字、現在時動詞變化等），"
        "絕對不要跟已經教過的主題重複或高度相似。\n\n"
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
        print(f"無法解析 Claude 回應的 JSON：{error}")
        return None

    lesson["id"] = next_id
    return lesson


def get_previous_topics():
    """掃描已經存在的課程 HTML，抓出每堂課的標題，避免新課程主題重複。"""
    topics = [lesson["title"] for lesson in LESSONS]
    existing_files = sorted(f for f in os.listdir(".") if f.startswith("french-lesson-") and f.endswith(".html"))
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


def main():
    """主函式"""
    print("開始生成法文教學課程...")

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
    filename = f"french-lesson-{lesson['id']:02d}.html"
    
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
