# 餐廳/食品推廣類 — 內容指紋（補充輸出範例）

> 此為 Phase 0.5 prototype 驗證輸出之示範格式。實際餐廳類資料對應 `data/processed/channel_videos_20260526-030644.csv`（如重抓需更新）。
> 驗證原型實際以 `data/processed/channel_videos_20260510-143336.csv`（PanSci 200 部）跑通 Layer 1–3，輸出僅為示範性質。
>
> 字典版本：v1.0（`analysis/_templates/content_keywords.yaml`）

---

## Layer 1：YouTube `topic_categories` 解析

- 缺值率：在 PanSci 樣本上為 **45.0%**（含長片）→ 表示約半數影片 YouTube 沒回標籤。
- 預期：娛樂/食物類頻道命中率高於科普；長片頻道命中率高於 Shorts 為主之頻道（因 YouTube 給 Shorts 標的密度較低）。
- 輸出格式：每頻道一張「topic 比例表」，欄為 Wikipedia 末段（Food / Entertainment / Lifestyle / Knowledge / Health / Society / Sport / Music / ...）。

## Layer 2：規則式關鍵字字典（v1.0）

10 個 bucket，每部影片得到 10 個 0/1 欄位：
`has_教學教育 / has_挑戰對決 / has_搞笑迷因 / has_開箱評測 / has_互動誘導 / has_情緒詞 / has_品牌推廣 / has_食物 / has_運動 / has_問句`

文字來源：`title + tags`（concatenated, lowercased）。

## Layer 3：TF-IDF Top 15 keywords per channel

- Tokenizer：jieba（已安裝 v0.42.1）；去除 `#hashtag` 與標點。
- TfidfVectorizer：每頻道一份文件，跨頻道計算 IDF，每頻道取 Top 15。
- 輸出：每頻道一張 keyword × tfidf 表，供 `findings.md` 引用。

## Layer 4：LDA（選做）

仅在「跨類別 ≥ 500 部」場景跑，类别内样本 < 300 跳過（C5 风险）。

---

## 範例：PanSci 內容指紋（200 部上傳 / 含長片）

```
YouTube topics 前 3：Health (42)、Society (32)、Lifestyle (18)
規則命中率 Top 3：has_問句 42.5% / has_食物 4.0% / has_教學教育 2.0%
TF-IDF Top 5：泛科學, news, 什麼, ai, 科學家
```

> 解讀：PanSci 標題多以「為什麼／怎麼」結構提問（has_問句 命中高）；科普本性導致 has_教學教育 命中卻只有 2%（字典未涵蓋「為什麼」這類問句型教學）→ Phase 2 起可考慮替每個類別微調字典 v1.1。
