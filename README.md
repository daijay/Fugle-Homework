# Fugle Homework 專案說明

## 1. 使用 uv 設置 Python 環境

本專案建議使用 `Python 3.10`

請依下列步驟使用 `uv` 建立虛擬環境並安裝：

```bash
# 建立虛擬環境，指定 Python 版本
uv venv .venv --python=python3.10

# 啟動虛擬環境
source .venv/bin/activate

# 安裝相關套件
uv pip install -r requirements.txt
```

---

## 2. 啟動專案步驟

請在專案根目錄下執行以下指令：

```bash
# 1. 執行資料庫遷移
python manage.py migrate

# 2. 啟動開發伺服器（預設 8000 port）
python manage.py runserver
```

如需指定其他 port，例如 8001：

```bash
python manage.py runserver 8001
```

---

## 3. 預設資料說明

執行 `python manage.py migrate` 時，會自動寫入以下預設資料：

- 建立一個帳號：
  - 帳號：`demo`
  - 密碼：`demo`
- 建立一筆帳戶申請資料，屬於 demo 使用者：
  - 帳戶名稱：預設帳戶
  - 電話：0912345678
  - 地址：台北市
  - 狀態：PENDING

---

## 4. 創建 Superuser（管理員帳號）

請在瀏覽器開啟下列網址，依照畫面指示建立管理員帳號：

```
http://127.0.0.1:8000/superuser-register/
```

建立後可用 `/admin/` 進入 Django 後台管理介面。

---

## 5. 其他注意事項

- 預設管理員後台網址為：http://127.0.0.1:8000/admin/
- 一般使用者註冊、登入、申請等功能請依照前端頁面指示操作。
- 若有任何問題，請先確認虛擬環境已啟動並安裝所有套件。

---

