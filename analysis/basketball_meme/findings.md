# 籃球幹片 Shorts 分析發現

## 樣本概況
- 兩個頻道：@juanmaodonggeqiu（卷毛懂个球）、@junhongtv（俊鸿TV）
- 抓取原始：400 部；分析樣本：Shorts 304 部（duration_sec ≤ 180）
- 俊鸿TV n = 164；卷毛懂个球 n = 140（兩頻道樣本均 ≥ 30，可進行檢定）

## 關鍵統計（Shorts 整體）
| 指標 | mean | median | std |
|---|---|---|---|
| view_count | 76,862 | 21,015 | 128,964 |
| like_count | 1,777 | 542 | 2,989 |
| comment_count | 9.5 | 4 | 19.5 |
| duration_sec | 95.2 | 94.5 | 45.9 |
| title_length | 46.3 | 43.5 | 21.2 |
| tag_count | 21.6 | 20 | 11.6 |

每頻道摘要：
| channel | n | mean_view | median_view | mean_like | mean_comment |
|---|---|---|---|---|---|
| 俊鸿TV | 164 | 120,376 | 42,412 | 2,815 | 14.0 |
| 卷毛懂个球 | 140 | 25,889 | 10,578 | 560 | 4.2 |

## 兩頻道差異（Mann-Whitney U，俊鸿TV vs 卷毛懂个球）
- view_count: p = 2.12e-19 ***  → **俊鸿TV 顯著高**
- like_count: p = 1.17e-20 ***  → 俊鸿TV 顯著高
- comment_count: p = 3.13e-11 ***  → 俊鸿TV 顯著高
- title_length: p = 2.16e-46 ***  → 俊鸿TV 標題顯著長（62.3 vs 27.6）
- tag_count: p = 7.02e-46 ***  → 俊鸿TV 標籤顯著多（28.5 vs 13.4）

俊鸿TV 訂閱（69,300）約為卷毛懂个球（5,030）的 14 倍，view_count 中位數差 4 倍 → 訂閱數可解釋大部分但非全部差距。

## 內容貼標發現（§4.5 / §7.5）

### Layer 1 — YouTube topic（前 4 大）
| topic | 俊鸿TV | 卷毛懂个球 |
|---|---|---|
| Basketball | 90.2% | 67.9% |
| Sport | 86.6% | 40.7% |
| Lifestyle | 7.9% | 25.7% |
| Entertainment | 4.9% | 27.9% |
| Humour | 4.3% | 30.0% |

→ 俊鸿TV 被 YouTube 認定為「硬核籃球」；卷毛懂个球 同時掛 Lifestyle/Entertainment/Humour，定位為「娛樂為主的籃球段子」。

### Layer 2 — 規則字典命中率（前 3 高 buckets）
- 俊鸿TV：`has_運動` 96.3%、`has_搞笑迷因` 65.2%、`has_教學教育` 12.2%
- 卷毛懂个球：`has_搞笑迷因` 67.9%、`has_問句` 13.6%、`has_運動` 5.0%

→ 卷毛懂个球 標題幾乎不含「籃球/運動」字眼，但「搞笑迷因」命中率與俊鸿TV 接近，凸顯定位差異。

### Layer 3 — TF-IDF Top 5 keywords
- 俊鸿TV：回顧、往期、野球、球場、籃球
- 卷毛懂个球：兄弟、打球、就是、遇到、还是

### §7.5 卡方檢定（top_quartile 門檻 view_count ≥ 82,352）
- `has_運動` chi² = 21.04, **p = 4.5e-06 ***（顯著預測高觀看）
- `has_挑戰對決` p = 0.039 *
- `has_搞笑迷因` p = 0.050 *
- 其餘 ns
- Logistic 跳過（singular matrix，部分 bucket 全 0）

## 迴歸結果
- Model 1（duration + title_length + tag_count）：R² = 0.2205, Adj R² = 0.2127
  - duration_sec: +24.4k ***
  - title_length: +58.3k ***
  - tag_count: -27.6k ** — 反直覺，多標籤不增加觀看
- Model 2（加 channel dummy）：R² = 0.2861, Adj R² = 0.2765
  - C(channel)[卷毛懂个球]: -128.3k ***（頻道效應強烈）
  - 加 dummy 後 title_length 變不顯著（p=0.21）→ 標題長度其實是頻道風格的代理
- VIF 均 < 2，無共線性問題

## 對應企劃書研究問題
- RQ1（標題長度）：單變量正相關但加頻道控制後消失，**頻道風格是主要驅動因子**
- RQ3（標籤數量）：負相關（控制其他變數後），與一般「多標籤導觀看」直覺相反
- RQ6（影片長度）：在 Shorts 內 duration_sec 仍正向（接近 180s 端的觀看略高）
- RQ7（訂閱數）：俊鸿TV 訂閱 14 倍於卷毛 → 兩頻道訂閱差距大；channel dummy 顯著反映了這個跨頻道差異

## 限制與註記
- 樣本均為 channels.list 預設的 200 部上傳，可能含半年內舊片，非「即時 Shorts feed」
- tag_count 由 `|` 分隔欄計算；俊鸿TV 重複度高（共用 30+ 標籤），對 t_value 影響需保留
- title_length 用混合字元數（CJK 1 char + EN 1 char）；本類別兩頻道皆中文為主，CJK 為主驅動（俊鸿 35.1 vs 卷毛 21.5 CJK chars）
- view_count 嚴重右偏（kurtosis 13）；OLS 殘差非常態，後續可改 log-OLS 或 Spearman
