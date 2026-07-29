# Cloudflare Pages 私有部署指南

TeachingApp PWA 已準備好部署到 Cloudflare Pages,支援私有存取(用 email 白名單)。

## 準備工作

- [ ] Cloudflare 帳號(免費方案即可)
- [ ] GitHub 帳號(repo 已有)
- [ ] 你自己的 email 作為 Access 白名單

## 部署步驟

### 1. 連接 GitHub 到 Cloudflare Pages

1. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 左側選擇 **Workers & Pages**
3. 點選 **Pages** → **Connect to Git**
4. 選擇 **GitHub** 並授權連接
5. 在 repo 清單中找到並選擇 `TeachingApp`
6. 點 **Begin setup**

### 2. 設定部署設定

在「Set up builds and deployments」頁面填入:

| 欄位 | 值 |
|---|---|
| **Production branch** | `main` |
| **Framework preset** | `None` (不需要 build) |
| **Build command** | 留空 |
| **Build output directory** | `webapp` |
| **Environment variables** | 無(可留空) |

然後點 **Save and Deploy** 等待第一次部署完成(通常 1-2 分鐘)。

✅ 部署完成後會得到網址,格式類似 `https://teachingapp.pages.dev`

### 3. 設定 Cloudflare Access(私有白名單)

1. 在 Cloudflare 後台左側選擇 **Access** → **Applications**
2. 點 **Add an application** → 選 **Self-hosted**
3. 設定應用名稱:填 `TeachingApp`
4. **Subdomain**:填 `teachingapp`(會自動變成 `teachingapp.<your-domain>.pages.dev`,但 Pages 自動產生的域名本身不需要這步——改用下面的方法)

**簡化版(推薦)**:
直接在 Cloudflare Pages 設定中:
1. 回到 Pages 專案的 **Settings**
2. 找 **Access policy**(或 **Authentication**)
3. 啟用 **Cloudflare for Teams** 保護(需升級帳號或使用免費試用)

### 4. 替代方案:用 Wrangler CLI 快速部署

如果上述步驟太複雜,可以用 Wrangler CLI:

```bash
# 安裝 Wrangler
npm install -g wrangler

# 登入 Cloudflare
wrangler login

# 部署
cd webapp
wrangler pages deploy .
```

這會直接上傳 `webapp/` 的所有檔案到 Cloudflare Pages。

### 5. 設定 Access 白名單(使用 Wrangler 部署時)

1. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 左側選擇 **Access** → **Applications**
3. 如果沒看到自動建立的應用,點 **Add an application** → **Self-hosted**
4. **Application name**: `TeachingApp`
5. **Subdomain**: `teachingapp`
6. 點 **Next**
7. **Application domain** 會自動生成(或選擇自訂網域)
8. 進入 **Access Policies**
9. 新增 Policy:
   - **Policy name**: `Email whitelist`
   - **Action**: `Allow`
   - **Rules** 選擇 **Emails** → 輸入你的 email(`rosana870107@gmail.com`)
   - 點 **Save application**

✅ 設定完成後,訪問應用時會跳出 Cloudflare Access 登入頁面,輸入郵箱後會收到驗證碼,驗證後才能進入。

## 驗證部署

1. **Web 瀏覽器**:用 Chrome/Safari 開啟部署後的網址
2. **手機 Safari**(iOS):
   - 開啟該網址
   - 點下方「分享」按鈕 → **加入主畫面**
   - 打開新增的 App → 應該看到首頁課程清單
3. **離線測試**:開啟後斷開網路,頁面應該仍可瀏覽已快取的課程

## 自動化(選用)

若要每次課程更新後自動重新部署 PWA,可在 `.github/workflows/update-webapp.yml` 末尾加入:

```yaml
      - name: Deploy to Cloudflare Pages
        run: |
          npm install -g wrangler
          wrangler pages deploy webapp
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

然後在 GitHub repo 的 **Settings** → **Secrets and variables** 中新增:
- `CLOUDFLARE_API_TOKEN`:從 [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens) 建立(需要 Pages 部署權限)
- `CLOUDFLARE_ACCOUNT_ID`:可從 Cloudflare 後台右下角「帳號 ID」複製

## 常見問題

**Q: 部署後頁面顯示空白?**
- 檢查 Cloudflare Pages 的 **Builds** 頁籤,看部署是否成功
- 若失敗,檢查 **Build output directory** 是否填 `webapp`

**Q: Access 白名單登不進去?**
- 確認 email 拼寫正確且添加到白名單
- 清除瀏覽器 cookie 後重試
- 檢查 Cloudflare Access 政策中 email 規則是否啟用

**Q: 課程內容沒有更新?**
- 手動到 Cloudflare Pages 的 **Deployments** 點 **Retry build**
- 或等待自動化 workflow 觸發(課程更新 > 自動執行 `update-webapp.yml` > 自動 push > 自動觸發 Pages 部署)

## 下一步

部署完成後,可以:
1. 在實機上「加入主畫面」測試獨立 App 模式
2. 驗證離線閱讀功能
3. 測試進度同步(跨裝置存取)
4. (後續)評估是否要開啟 Web Push 推播通知
