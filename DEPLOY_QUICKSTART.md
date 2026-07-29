# 5 分鐘快速部署到 Cloudflare Pages

## 最快路徑:手動部署(不需要 GitHub Secrets)

### 1. 安裝 Wrangler CLI

```bash
npm install -g wrangler
```

### 2. 登入 Cloudflare

```bash
wrangler login
```

瀏覽器會跳出登入頁面,用你的 Cloudflare 帳號登入並授權。

### 3. 部署

```bash
cd "C:\Users\Tong\Desktop\Project 2\教學"
cd webapp
wrangler pages deploy .
```

等待上傳完成(通常 30 秒內),會印出部署網址:
```
✨ Deployment successful! Deployed to https://teachingapp.pages.dev
```

✅ **完成!** 打開該網址即可存取 PWA。

---

## 設定 Access(email 白名單)

1. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 左側 **Access** → **Applications**
3. 若沒自動建立,手動:
   - **Add an application** → **Self-hosted**
   - **Application name**: `TeachingApp`
   - **Subdomain**: `teachingapp`
4. 進入 **Access Policies**
5. **Add a policy**:
   - **Policy name**: `Email whitelist`
   - **Action**: `Allow`
   - **Rules**: 選 **Emails** → 輸入你的 email(`rosana870107@gmail.com`)
   - **Save application**

訪問時會先要求用 email 驗證,驗證後即可進入。

---

## 測試(手機上)

1. 用 iPhone Safari 打開部署的網址
2. 點下方「分享」→ **加入主畫面**
3. 命名後點「加入」
4. 打開新增的 App,應該看到課程清單
5. 關閉網路,頁面仍可運作(離線快取)

---

## 自動化部署(選用)

若想每次課程更新後自動部署:

1. 參考 [DEPLOY_GITHUB_SECRETS.md](DEPLOY_GITHUB_SECRETS.md),在 GitHub 新增:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`
   - `CLOUDFLARE_PROJECT_NAME`(選用)

2. 就這樣!`.github/workflows/deploy-pages.yml` 已經會自動運作。

---

## 完整文檔

- [DEPLOY_CLOUDFLARE.md](DEPLOY_CLOUDFLARE.md) — 詳細部署步驟
- [DEPLOY_GITHUB_SECRETS.md](DEPLOY_GITHUB_SECRETS.md) — Secrets 獲取與設定
