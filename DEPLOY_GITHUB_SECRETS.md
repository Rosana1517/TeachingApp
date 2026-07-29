# GitHub Secrets 設定(Cloudflare 自動部署)

如果要啟用 GitHub Actions 自動部署到 Cloudflare Pages(`.github/workflows/deploy-pages.yml`),需要在 GitHub repo 中新增以下 Secrets。

## 步驟

1. 登入 GitHub,進入 [TeachingApp repo](https://github.com/Rosana1517/TeachingApp)
2. 點 **Settings** → **Secrets and variables** → **Actions**
3. 點 **New repository secret**,逐個新增以下內容:

## 需要的 Secrets

### 1. CLOUDFLARE_API_TOKEN

**用途**:授權 GitHub Actions 部署到 Cloudflare Pages

**如何獲取**:
1. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 左側底部點帳號頭像 → **My Profile**
3. 選擇 **API Tokens** 頁籤
4. 點 **Create Token**
5. 選擇 **Edit Cloudflare Workers** 範本(或自訂):
   - 需要的權限:
     - **Account** > **Cloudflare Pages** > **Write**
     - **Zone** > **Zone** > **Read**(所有區域)
6. 點 **Continue to summary** → **Create Token**
7. 複製生成的 token,貼到 GitHub Secrets 中
8. **Secret name**: `CLOUDFLARE_API_TOKEN`

### 2. CLOUDFLARE_ACCOUNT_ID

**用途**:告訴 Wrangler 要部署到哪個 Cloudflare 帳號

**如何獲取**:
1. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 任選一個 domain 或直接進 Workers & Pages
3. 右下角會看到 **Account ID**,複製該 32 位字母數字
4. **Secret name**: `CLOUDFLARE_ACCOUNT_ID`

### 3. CLOUDFLARE_PROJECT_NAME(選用,美化用)

**用途**:在 GitHub Actions workflow 頁面顯示部署的網址

**填入**:你的 Cloudflare Pages 專案名稱(通常是 `teachingapp`)
- **Secret name**: `CLOUDFLARE_PROJECT_NAME`
- **Value**: `teachingapp`(或你自訂的名稱)

## 驗證設定

設定完成後,新增的 Secrets 應該會列在頁面上(值不會顯示)。

嘗試手動觸發 workflow:
1. 進入 repo 的 **Actions** 頁籤
2. 左側選擇 **Deploy to Cloudflare Pages**
3. 點 **Run workflow** → **Run workflow**
4. 等待執行完成(應該會在 2-3 分鐘內部署成功)

若出現錯誤,可在 workflow run 頁面查看 logs 診斷問題。

## 自動觸發

設定完成後,以下情況會自動觸發部署:
- 每次 `update-webapp.yml` 成功執行後(課程更新)
- 每次推送到 main 分支且修改了 `webapp/` 或 deploy workflow 本身
- 手動點 **Run workflow** 觸發

## 移除 Secrets

若日後需要撤銷授權,回到 GitHub Secrets 頁面刪除相應項目,然後:
1. 登入 [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
2. 找到對應的 token 點 **Roll** 撤銷(或 **Delete**)

這樣 GitHub 就無法再存取 Cloudflare 了。
