# YouTube Data API v3 爬蟲管線

統計學期末專案。用 YouTube Data API v3 爬公開資料（頻道、影片、留言、熱門榜），輸出 CSV 給後續回歸分析使用。

四個研究目標各對應一個指令：

| Goal | 指令 | 用途 | 配額成本 |
|---|---|---|---|
| 熱門榜快照 | `trending` | 各地區/分類的 mostPopular 影片 | 便宜（~5 units/region）|
| 頻道比較 | `channel-compare` | 多個頻道的所有上傳影片 + 統計 | 中等（~50–200 units）|
| 關鍵字搜尋 | `search-top` | 由關鍵字找熱門影片 | 貴（每次 search 100 units）|
| 留言分析 | `comments` | 指定影片的留言串 | 中等（~5 units/影片）|

---

## 一次性環境設定

### 1. 虛擬環境

```bash
cd "/Users/waynliu/Documents/NTU/台大/大二下/統計一下/final project"
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安裝套件

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 取得 YouTube Data API v3 金鑰

1. 進 [Google Cloud Console](https://console.cloud.google.com/)，建立新 project（例如 `yt-stats-final`）
2. **APIs & Services → Library** → 搜尋 **YouTube Data API v3** → Enable
3. **APIs & Services → Credentials → Create credentials → API key** → 複製金鑰
4. 建議：點該金鑰 → **API restrictions** → 限制只能用 YouTube Data API v3

### 4. 設定 `.env`

```bash
cp .env.example .env
```

打開 `.env`，把 API key 貼進去：

```
YOUTUBE_API_KEY=AIza...你的金鑰
```

`.env` 已被 `.gitignore` 排除，不會被版控追蹤。

### 5. 之後每次新開 terminal

```bash
cd "/Users/waynliu/Documents/NTU/台大/大二下/統計一下/final project"
source .venv/bin/activate
```

離開虛擬環境輸入 `deactivate`。

---

## 目錄結構

```
final project/
├── .env                      # 你的 API key（gitignored）
├── .env.example              # 範本
├── config.yaml               # 全域設定（配額預算）
├── main.py                   # CLI 入口
├── requirements.txt
├── presets/                  # 研究情境設定檔
│   ├── default.yaml
│   ├── tech_education.yaml
│   ├── trending_panel.yaml
│   └── music_tw.yaml
├── src/                      # 抓取邏輯（不用改）
├── data/
│   ├── raw/                  # （目前未使用，預留 JSON dump）
│   └── processed/            # 抓出來的 CSV 都在這
└── notebooks/                # 統計分析（你自己寫）
```

---

## 使用方式

### 指令格式

```bash
python main.py <goal> [--preset <name>] [--dry-run] [--budget <n>]
```

- `<goal>`：`trending` / `channel-compare` / `search-top` / `comments` 四選一
- `--preset`：用 `presets/<name>.yaml`，預設 `default`
- `--dry-run`：不打 API，只顯示讀到的設定 + 配額估算
- `--budget`：覆蓋當次配額預算（預設 8000）

### 列出可用 preset

```bash
python main.py --list-presets
```

會列出每個 preset 包含哪些 goal section。

### 常用指令

```bash
# 跑預設 trending（最便宜，~12 units）
python main.py trending

# 換 preset
python main.py channel-compare --preset tech_education
python main.py search-top --preset music_tw

# 先 dry-run 看設定有沒有讀對
python main.py trending --preset trending_panel --dry-run

# 限縮預算（避免一次燒太多）
python main.py search-top --preset music_tw --budget 500
```

---

## Preset 設定檔（`presets/*.yaml`）說明

一個 preset 檔可以同時包含多個 goal section。你跑哪個 goal 就只讀對應的 section，其他會被忽略。

### `trending` 區塊

```yaml
trending:
  regions: ["TW", "US", "JP"]      # 地區代碼（ISO 3166-1 alpha-2）
  category_ids: null               # null = 所有分類；範例 [10] = 只要音樂
  max_per_region: 200              # 每個地區最多抓幾部（會被四捨到 50 的倍數）
```

常用 category_id（用 `videoCategories.list` 可查全表）：
- `1` 電影動畫 / `10` 音樂 / `15` 寵物動物 / `17` 運動 / `20` 遊戲
- `22` 部落格 / `23` 喜劇 / `24` 娛樂 / `25` 新聞政治 / `26` How-to
- `27` 教育 / `28` 科技 / `29` 非營利

### `channel_compare` 區塊

```yaml
channel_compare:
  channel_ids:
    - "@veritasium"                # 可以用 @handle
    - "UCsXVk37bltHxD1rDPwtNM8Q"   # 也可以用 channel ID（UC 開頭）
  max_videos_per_channel: 200      # 每個頻道最多抓多少部影片
```

> 想做回歸分析的話，這是最重要的資料來源。建議選 5–20 個**同類型**頻道（例如都是科普頻道、都是台灣 vlogger），這樣比較才有統計意義。

### `search_top` 區塊

```yaml
search_top:
  keywords:                        # 關鍵字列表，會逐一搜尋
    - "linear regression tutorial"
    - "p value explained"
  region_code: "TW"                # null 不限地區
  order: "viewCount"               # viewCount / relevance / date / rating
  max_pages_per_keyword: 2         # 每個關鍵字翻幾頁（每頁 50 部）
  published_after: null            # ISO 8601，例如 "2026-01-01T00:00:00Z"
```

> ⚠️ `search.list` 一次 100 units，這是最貴的呼叫。3 個關鍵字 × 2 頁 = 600 units。

### `comments` 區塊

```yaml
comments:
  video_ids: []                    # 可以直接列影片 ID
  video_ids_from: "trending"       # 或從現成 CSV 讀：trending / top_by_keyword / channel_videos
  limit: 20                        # 最多處理幾部影片
  max_pages_per_video: 5           # 每部影片留言翻幾頁（每頁 100 則）
  order: "relevance"               # relevance / time
  fetch_replies: false             # true 會用 comments.list 抓完整回覆樹（可能爆量）
```

> `video_ids_from: "trending"` 會自動找 `data/processed/` 底下最新的 `trending_*.csv`，取前 N 部影片。所以工作流程通常是：先跑 `trending` → 再跑 `comments`。

---

## 新增你自己的 preset

1. 複製一份範本：

   ```bash
   cp presets/default.yaml presets/my_research.yaml
   ```

2. 編輯 `presets/my_research.yaml`，把 channel_ids、keywords 等改成你要的。不需要的 goal section 可以整段刪掉。

3. 用：

   ```bash
   python main.py channel-compare --preset my_research
   ```

主程式不用改。

---

## 輸出檔案

所有 CSV 都寫到 `data/processed/`，檔名帶 UTC 時間戳：

```
data/processed/
├── trending_20260510-061234.csv          # 來自 trending
├── channels_20260510-062100.csv          # channel-compare 的頻道層級
├── channel_videos_20260510-062150.csv    # channel-compare 的影片層級
├── top_by_keyword_20260510-063000.csv    # search-top
├── comments_top_20260510-063500.csv      # comments 的頂層留言
├── comments_replies_20260510-063500.csv  # comments 的回覆（如有）
└── comments_skipped_20260510-063500.csv  # 關閉留言或刪除的影片
```

**主要欄位**（`videos.csv` 形 — `trending` / `channel_videos` / `top_by_keyword` 都長這樣）：

`video_id, title, description, channel_id, channel_title, published_at, category_id, tags, default_language, duration_iso, duration_sec, definition, caption, view_count, like_count, comment_count, favorite_count, topic_categories, fetched_at`

`channels.csv`：`channel_id, title, country, published_at, view_count, subscriber_count, video_count, uploads_playlist_id`

`comments_top.csv`：`video_id, comment_id, author_display_name, text, like_count, published_at, total_reply_count`

---

## 配額策略

YouTube Data API v3 每天免費額度 **10,000 units**（太平洋時間午夜重置 ≈ 台灣時間下午 3 點）。

| 端點 | 成本 |
|---|---|
| `search.list` | **100** |
| `videos.list` | 1 |
| `channels.list` | 1 |
| `playlistItems.list` | 1 |
| `commentThreads.list` | 1 |
| `comments.list` | 1 |

`config.yaml` 的 `quota.per_run_budget` 設了 8000 上限作為單次預算護欄（留 2000 緩衝）。任何時候只要要超過預算就會主動停下並儲存已抓的結果。

**省配額的小技巧**：
- 跑前先 `--dry-run` 看一下估算
- `videos.list` 已經內建批次（一次 50 個 ID）
- 寧可多次小跑、累積資料，也不要一次衝大量

---

## 常見錯誤

| 錯誤訊息 | 意思 | 解法 |
|---|---|---|
| `YOUTUBE_API_KEY not set` | 沒設 `.env` | 建 `.env` 並填金鑰 |
| `400 API key not valid` | 金鑰錯/沒啟用 Data API v3 | Cloud Console 確認 |
| `403 quotaExceeded` | 當天額度用完 | 等台灣下午 3 點重置 |
| `403 commentsDisabled` | 影片關閉留言 | 自動 skip 到 `comments_skipped_*.csv` |
| `KeyError: ... section` | 你選的 preset 沒定義那個 goal | 換 preset 或加 section |
| `FileNotFoundError: No CSV found for source` | comments 找不到來源 CSV | 先跑對應的 goal |

---

## 工作流程建議

第一次：

1. `python main.py trending --dry-run` — 確認 preset 讀得到
2. `python main.py trending` — 跑最便宜的 goal 驗證整條管線（~12 units）
3. 開 `data/processed/trending_*.csv` 檢查欄位
4. 編輯 `presets/<your>.yaml` 設定你的研究目標
5. `python main.py channel-compare --preset <your> --dry-run` 再 `--dry-run` 過一次
6. 真的跑

之後分析就在 `notebooks/` 裡用 pandas 讀 CSV 做 EDA / 回歸。
