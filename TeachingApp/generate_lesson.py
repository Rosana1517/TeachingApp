#!/usr/bin/env python3
"""
自動生成每日 HTML 教學課程腳本
這個腳本會根據課程資料庫生成新的 HTML 教學檔案
"""

import os
from datetime import datetime

# 課程資料庫 - 你可以擴展這個列表
COURSES = [
    {
        "id": 1,
        "title": "Swift 基礎語法",
        "category": "程式設計",
        "content": """
# Swift 基礎語法

Swift 是蘋果公司開發的現代化程式語言，用於開發 iOS、macOS、watchOS 和 tvOS 應用程式。

## 變數與常數

在 Swift 中，我們使用 `var` 聲明變數，使用 `let` 聲明常數。

[code]
// 聲明變數
var userName = "小明"
var age = 25

// 聲明常數
let appName = "學習 App"
let version = "1.0.0"
[/code]

[note]提示：建議優先使用 const 而不是 var，除非你真的需要改變它的值。[/note]

## 資料類型

Swift 是類型安全的語言，它會在編譯時檢查類型。

[code]
// 整數
let integerNumber: Int = 42

// 浮點數
let floatingPointNumber: Double = 3.14

// 布林值
let isLearning: Bool = true

// 字串
let greeting: String = "你好世界"
[/code]

## 字串插值

你可以使用字串插值來在字串中嵌入變數和常數。

[code]
let name = "小明"
let age = 25
let message = "我叫\(name)，今年\(age)歲"
print(message)
[/code]

[note]字串插值讓你可以輕鬆地將變數值嵌入字串中。[/note]

## 小測驗

[quiz]Swift 中使用哪個關鍵字聲明常數？|var|let|const|fixed|B|常數使用 let 聲明，變數使用 var 聲明。|B[/quiz]
""",
        "tags": ["swift", "基礎", "語法"]
    },
    {
        "id": 2,
        "title": "SwiftUI 元件基礎",
        "category": "程式設計",
        "content": """
# SwiftUI 元件基礎

SwiftUI 是蘋果公司推出的聲明式 UI 框架，讓建立使用者介面變得更加簡單。

## 基本元件

SwiftUI 提供了許多基本元件來構建使用者介面。

[code]
struct ContentView: View {
    var body: some View {
        VStack {
            Text("Hello, World!")
                .font(.largeTitle)
            
            Button("點擊我") {
                print("按鈕被點擊了")
            }
            
            Image(systemName: "star.fill")
        }
    }
}
[/code]

## 佈局容器

SwiftUI 提供了三種主要的佈局容器。

[code]
// 垂直堆疊
VStack {
    Text("第一行")
    Text("第二行")
}

// 水平堆疊
HStack {
    Image(systemName: "heart.fill")
    Text("喜歡")
}

// 網格佈局
LazyVGrid(columns: [GridItem()]) {
    Text("項目 1")
    Text("項目 2")
}
[/code]

[note]VStack 和 HStack 是 SwiftUI 中最常用的佈局容器。[/note]

## 修飾符

修飾符用來改變元件的外觀和行為。

[code]
Text("美化文字")
    .font(.title)
    .foregroundColor(.blue)
    .padding()
    .background(Color.yellow)
    .cornerRadius(10)
    .shadow(radius: 5)
[/code]

## 小測驗

[quiz]SwiftUI 中用於垂直排列元件的容器是？|HStack|VStack|ZStack|Stack|B|VStack 用於垂直排列元件，HStack 用於水平排列。|B[/quiz]
""",
        "tags": ["swiftui", "UI", "元件"]
    },
    {
        "id": 3,
        "title": "iOS 應用程式架構",
        "category": "程式設計",
        "content": """
# iOS 應用程式架構

良好的架構設計對於維護大型應用程式至關重要。

## MVC 架構

MVC（Model-View-Controller）是 iOS 開發中最常見的架構模式。

[code]
// Model - 資料層
class User {
    var name: String
    var age: Int
    
    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }
}

// View - 視覺層
struct UserView: View {
    let user: User
    
    var body: some View {
        VStack {
            Text(user.name)
            Text("\(user.age) 歲")
        }
    }
}

// Controller - 控制層
class UserController {
    var user: User
    
    func updateUser(name: String) {
        user.name = name
    }
}
[/code]

## MVVM 架構

MVVM（Model-View-ViewModel）是現代 iOS 開發推薦的架構。

[code]
// ViewModel
class UserViewModel: ObservableObject {
    @Published var userName: String = "小明"
    @Published var userAge: Int = 25
    
    func updateName(_ newName: String) {
        userName = newName
    }
}
[/code]

[note]MVVM 將業務邏輯放在 ViewModel 中，使 View 更加純粹和易於測試。[/note]

## 選擇合適的架構

- 小型專案：MVC 就足夠了
- 中型專案：考慮使用 MVVM
- 大型專案：MVVM + Clean Architecture

## 小測驗

[quiz]MVVM 中的 VM 代表什麼？|View Manager|ViewModel|Value Model|View Model|D|ViewModel 負責處理 View 的業務邏輯和資料轉換。|D[/quiz]
""",
        "tags": ["架構", "MVC", "MVVM"]
    }
]

def get_next_course_id():
    """獲取下一個課程 ID"""
    existing_files = [f for f in os.listdir('.') if f.startswith('lesson-') and f.endswith('.html')]
    if not existing_files:
        return 1
    
    max_id = 0
    for file in existing_files:
        try:
            course_id = int(file.split('-')[1].split('.')[0])
            max_id = max(max_id, course_id)
        except:
            pass
    
    return max_id + 1

def generate_html_template(course, generated_date):
    """生成 HTML 模板"""
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{course['title']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #007AFF;
            border-bottom: 2px solid #007AFF;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #5856D6;
            margin-top: 30px;
        }}
        code {{
            background-color: #f0f0f0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: "Menlo", monospace;
            color: #FF3B30;
        }}
        pre {{
            background-color: #f0f0f0;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            color: #1C1C1E;
        }}
        .note {{
            background-color: #FFF3CD;
            border-left: 4px solid #FFC107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .quiz {{
            background-color: #E7F5FF;
            border-left: 4px solid #007AFF;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{course['title']}</h1>
        
        <div class="meta">
            <span>分類：{course['category']}</span> | 
            <span>生成日期：{generated_date}</span>
        </div>
        
        {course['content']}
        
        <hr style="margin: 30px 0;">
        
        <p style="color: #999; font-size: 12px;">
            此課程由 TeachingApp 自動生成，生成時間：{generated_date}
        </p>
    </div>
</body>
</html>"""
    
    return html

def main():
    """主函式"""
    print("📚 開始生成每日教學課程...")
    
    # 獲取下一個課程 ID
    next_id = get_next_course_id()
    
    # 選擇一個課程來生成（可以擴展為生成多個）
    course = COURSES[(next_id - 1) % len(COURSES)]
    
    # 添加生成日期
    generated_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    course_with_date = {
        **course,
        'id': next_id,
        'generated_date': generated_date
    }
    
    # 生成 HTML
    html_content = generate_html_template(course_with_date, generated_date)
    
    # 生成檔案名稱
    filename = f"lesson-{next_id:02d}.html"
    
    # 寫入檔案
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 已成功生成課程: {filename}")
    print(f"   標題: {course['title']}")
    print(f"   分類: {course['category']}")
    print(f"   生成時間: {generated_date}")

if __name__ == "__main__":
    main()
