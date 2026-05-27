# 籃球網紅 Shorts 分析發現

## 樣本概況
- 兩個頻道：@ehoozeng（曾舔舔🕊️）、@肖他11（肖他）
- 抓取原始：312 部；分析樣本：Shorts 310 部（duration_sec ≤ 180）
- 曾舔舔🕊️ n = 199；肖他 n = 111（兩頻道樣本均 ≥ 30，可進行檢定）

## 關鍵統計（Shorts 整體）
| 指標 | mean | median | std |
|---|---|---|---|
| view_count | 105,868 | 34,480 | 189,365 |
| like_count | 2,010 | 830 | 3,568 |
| comment_count | 15.6 | 7 | 24.7 |
| duration_sec | 73.7 | 61 | 44.8 |
| title_length | 44.8 | 43.5 | 17.7 |
| tag_count | 0.0 | 0 | 0.0 |

每頻道摘要：
| channel | n | mean_view | median_view | mean_like | mean_comment |
|---|---|---|---|---|---|
| 曾舔舔🕊️ | 199 | 139,535 | 57,774 | 2,387 | 19.1 |
| 肖他 | 111 | 45,510 | 19,510 | 1,335 | 9.3 |

## 兩頻道差異（Mann-Whitney U，曾舔舔🕊️ vs 肖他）
- view_count: p = 2.01e-15 ***  → **曾舔舔🕊️ 顯著高**
- like_count: p = 1.55e-05 ***  → 曾舔舔🕊️ 顯著高
- comment_count: p = 8.97e-09 ***  → 曾舔舔🕊️ 顯著高
- title_length: p = 4.39e-19 ***  → 曾舔舔🕊️ 標題顯著長（51.2 vs 33.4）
- tag_count: p = 1.0 ns  → 兩頻道幾乎都無 tag（CSV `tags` 欄全 NaN）

曾舔舔🕊️ 訂閱（21,800）約為肖他（9,770）的 2.2 倍，但中位 view 差 3 倍 → 高觀看不只靠訂閱規模，內容差異也是因子。

## 內容貼標發現（§4.5 / §7.5）

### Layer 1 — YouTube topic（前 4 大）
| topic | 曾舔舔🕊️ | 肖他 |
|---|---|---|
| Basketball | 73.9% | 84.7% |
| Sport | 66.8% | 96.4% |
| Lifestyle | 27.6% | 3.6% |
| Humour | 14.1% | 0.0% |
| Entertainment | 4.5% | 0.0% |

→ 肖他被歸「純粹體育/籃球」，曾舔舔🕊️同時帶入 Lifestyle/Humour/Entertainment，定位較娛樂化。

### Layer 2 — 規則字典命中率（前 3 高 buckets）
- 曾舔舔🕊️：`has_運動` 78.9%、`has_教學教育` 28.6%、`has_問句` 19.1%
- 肖他：`has_運動` 57.7%、`has_問句` 21.6%、`has_情緒詞` 9.9%

### Layer 3 — TF-IDF Top 5 keywords
- 曾舔舔🕊️：如何、分析、籃球、阿猿、教練
- 肖他：学校、球员、球风、厉害、这么

→ 兩頻道在地理 / 用字差異明顯：曾舔舔🕊️ 用繁體＋台灣 KOL 體系（教練、王師傅、新生），肖他用簡體＋校園篇章（学校、球员、校园）。

### §7.5 卡方檢定（top_quartile 門檻 view_count ≥ 102,853）
- `has_運動` chi² = 11.84, **p = 5.8e-04 ***（顯著預測高觀看）
- 其餘 ns
- Logistic 跳過（singular matrix）

## 迴歸結果
- Model 1（duration + title_length + tag_count）：R² = 0.037, Adj R² = 0.030
  - duration_sec: p = 0.43 ns
  - title_length: +35.7k ** (p=0.001)
  - tag_count: 共線（全 0），自動 drop
- Model 2（加 channel dummy）：R² = 0.063, Adj R² = 0.054
  - C(channel)[肖他]: -76.4k ** (p=0.003)
  - title_length 在加 dummy 後變不顯著
- VIF：N/A（tag_count 全 0 → 條件數 inf）

**整體 R² 低**（< 7%）顯示連續變數對 view_count 的解釋力很弱，view 主要由「個別影片是否爆 + 頻道粉絲基礎」驅動。

## 對應企劃書研究問題
- RQ1（標題長度）：單變量正相關（p=0.001）但加頻道控制後消失 → 同籃球幹片，**頻道風格驅動**
- RQ3（標籤數量）：**無法檢定**（兩頻道 CSV `tags` 欄全 NaN，可能為抓取時 API 對 hashtag-only 影片不回 tags）
- RQ6（影片長度）：duration_sec 在 Shorts 內不顯著（兩頻道平均 < 90s，變異有限）
- RQ7（訂閱數）：訂閱差 2 倍但觀看差 3 倍，內容差異可能也有影響

## 限制與註記
- `tags` 欄全為 NaN — 這兩頻道用 hashtag 寫在 title 而非 metadata tag（典型短影音作者），導致 tag_count 完全為 0、相關性檢定 NaN
- 曾舔舔🕊️ 是與「俊鸿TV」（即上 basketball_meme 的高觀看頻道）有合拍系列（TF-IDF 命中「俊鸿TV」），實質為 KOL 聯盟，不純粹「兩頻道對照」
- 「肖他」用簡體 + 中國校園情境，曾舔舔🕊️ 用繁體 + 台灣街頭，文化脈絡差異未控制
- view_count 嚴重右偏（kurtosis 31），OLS 模型擬合很差，後續宜改 log 或 rank-based 分析
