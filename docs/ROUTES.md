# ROUTES API Design Document (路由設計文件)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 | GET | `/` | `templates/index.html` | 系統入口與介紹 |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 提交註冊 | POST | `/auth/register` | — | 寫入 DB 並重導向至登入頁 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 提交登入 | POST | `/auth/login` | — | 驗證帳號密碼，設定 Session |
| 登出 | GET | `/auth/logout` | — | 清除 Session 並重導向首頁 |
| 抽籤/擲筊 | GET, POST | `/fortune/draw` | `templates/fortune/draw.html` | GET 顯示頁面，POST 回傳隨機結果 |
| 籤詩詳情 | GET | `/fortune/<int:fortune_id>` | `templates/fortune/detail.html` | 顯示特定籤詩內容與解析 |
| 儲存紀錄 | POST | `/fortune/<int:fortune_id>/save` | — | 將算命紀錄寫入 `fortune_results` |
| 個人主頁 | GET | `/profile` | `templates/profile/index.html` | 顯示使用者儲存的籤詩與捐獻歷史 |
| 捐獻頁面 | GET | `/donate` | `templates/profile/donate.html` | 顯示香油錢捐獻表單 |
| 提交捐獻 | POST | `/donate/checkout` | — | 寫入捐獻紀錄至 `donations` |

## 2. 每個路由的詳細說明

### Auth 模組 (`app/routes/auth.py`)
- **`/auth/register` (GET/POST)**
  - 輸入：POST 時接收表單欄位 `username`, `email`, `password_hash` (密碼需在後端使用 werkzeug 雜湊)
  - 邏輯：檢查信箱與帳號是否重複，若無則呼叫 `User.create()`。
  - 輸出：GET 渲染 `auth/register.html`；POST 成功則重導向 `/auth/login`。
  - 錯誤：資料不全或重複時，flash 錯誤訊息並重新渲染表單。

- **`/auth/login` (GET/POST)**
  - 輸入：POST 時接收 `username` 與 `password`。
  - 邏輯：透過 `User.get_by_username()` 查詢，使用 `check_password_hash` 驗證密碼。正確則建立登入 Session。
  - 輸出：GET 渲染 `auth/login.html`；POST 成功重導向 `/` 或 `/profile`。
  - 錯誤：帳號或密碼錯誤時 flash 錯誤並重新渲染。

- **`/auth/logout` (GET)**
  - 邏輯：從 Session 中清除 `user_id`。
  - 輸出：完成後重導向至首頁 `/`。

### Main 模組 (`app/routes/main.py`)
- **`/` (GET)**
  - 處理邏輯：首頁載入。
  - 輸出：渲染 `index.html`。

- **`/fortune/draw` (GET/POST)**
  - 輸入：無或 AJAX 傳來的 POST 擲筊訊號。
  - 邏輯：前端模擬擲筊時，若為 POST 且出現聖筊，後端使用 `Fortune.get_all()` 與 `random.choice()` 隨機選出一首籤詩。
  - 輸出：GET 渲染 `fortune/draw.html`，若是 POST 則可回傳 JSON 以供前端動態顯示結果與跳轉。

- **`/fortune/<int:fortune_id>` (GET)**
  - 輸入：URL 參數 `fortune_id`。
  - 邏輯：呼叫 `Fortune.get_by_id(fortune_id)` 取得指定籤詩的內容。
  - 輸出：渲染 `fortune/detail.html`。
  - 錯誤：若 ID 不存在，返回 404 Not Found。

- **`/fortune/<int:fortune_id>/save` (POST)**
  - 輸入：URL 參數 `fortune_id`。
  - 邏輯：此路由必須確認 `session.get('user_id')` 存在。然後呼叫 `FortuneResult.create(user_id, fortune_id)`。
  - 輸出：成功後重導向 `/profile` 或原本籤詩頁，並附帶已儲存的 flash 提示。
  - 錯誤：若未登入則重導向 `/auth/login`。

### Profile 模組 (`app/routes/profile.py`)
- **`/profile` (GET)**
  - 邏輯：需確保已登入。透過 User 關聯或 `FortuneResult.get_by_user_id(user_id)` 取得過往抽籤紀錄；透過 `Donation.get_by_user_id(user_id)` 取得捐款紀錄。
  - 輸出：渲染 `profile/index.html`。
  - 錯誤：未登入重導向 `/auth/login`。

- **`/donate` (GET)**
  - 邏輯：需確保已登入。
  - 輸出：渲染 `profile/donate.html`。

- **`/donate/checkout` (POST)**
  - 輸入：接收表單 `amount` 金額。
  - 邏輯：確保已登入，並呼叫 `Donation.create(user_id, amount, status='completed')` 模擬完款金流。
  - 輸出：完成後重導向至 `/profile` 並 flash 感謝捐贈的訊息。

## 3. Jinja2 模板清單
以下是本專案需要建立的 HTML 模板檔案規劃，所有子模板都繼承自 `base.html`。

- `templates/base.html`：包含 `<head>`、Navbar、Footer 以及共通 CSS / JS。
- `templates/index.html`：首頁。
- `templates/auth/register.html`：註冊頁面 (繼承 base)。
- `templates/auth/login.html`：登入頁面 (繼承 base)。
- `templates/fortune/draw.html`：抽籤擲筊互動介面 (繼承 base)。
- `templates/fortune/detail.html`：單支籤詩結果與解析呈現 (繼承 base)。
- `templates/profile/index.html`：個人主頁，列出歷史算命紀錄與捐獻明細 (繼承 base)。
- `templates/profile/donate.html`：香油錢捐獻頁面與選擇介面 (繼承 base)。

## 4. 路由骨架程式碼
對應的 `.py` 檔案已儲存於專案 `app/routes/` 目錄中，分別為：
- `__init__.py`
- `auth.py`
- `main.py`
- `profile.py`
