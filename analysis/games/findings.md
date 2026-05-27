# 遊戲 Shorts 分析發現

## 樣本概況
- 兩個頻道：@camman18、@gothamchess
- 抓取原始：400 部；分析樣本：Shorts 308 部（duration_sec ≤ 180）
- camman18 n = 198；GothamChess n = 110（兩頻道樣本均 ≥ 30，可進行檢定）

## 關鍵統計（Shorts 整體）
| 指標 | mean | median | std |
|---|---|---|---|
| view_count | 5,179,427 | 3,975,738 | 4,531,712 |
| like_count | 203,026 | 178,150 | 168,860 |
| comment_count | 2,143 | 1,506 | 2,689 |
| duration_sec | 38.2 | 33 | 23.8 |
| title_length | 32.9 | 27.5 | 22.7 |
| tag_count | 20.4 | 29 | 11.5 |

每頻道摘要：
| channel | n | mean_view | median_view | mean_like | mean_comment |
|---|---|---|---|---|---|
| camman18 | 198 | 6,673,253 | 5,360,629 | 280,874 | 2,997 |
| GothamChess | 110 | 2,490,539 | 1,844,345 | 62,900 | 606 |

⚠ 兩頻道都是全英文國際大型頻道（10M+ 訂閱），平均觀看遠高於其他類別。

## 兩頻道差異（Mann-Whitney U，GothamChess vs camman18）
- view_count: p = 5.51e-29 ***  → **camman18 顯著高**
- like_count: p = 2.33e-42 ***  → camman18 顯著高
- comment_count: p = 1.45e-41 ***  → camman18 顯著高
- title_length: p = 5.13e-40 ***  → camman18 顯著長（42.8 vs 14.9）
- tag_count: p = 9.97e-69 ***  → camman18 顯著多 tag（29.0 vs 5.0）

camman18 訂閱（10.8M）vs GothamChess（7.58M）= 1.4 倍，但中位觀看 2.9 倍 → 內容差異也是主因。

## 內容貼標發現（§4.5 / §7.5）

### Layer 1 — YouTube topic（前 4 大）
| topic | camman18 | GothamChess |
|---|---|---|
| Video_game_culture | 100.0% | 57.3% |
| Role-playing_video_game | 93.4% | 0.0% |
| Action-adventure_game | 84.3% | 0.0% |
| Action_game | 54.0% | 0.0% |
| Strategy_video_game | 2.5% | 6.4% |
| Entertainment | 0.0% | 20.9% |
| Hobby | 0.0% | 17.3% |
| Lifestyle | 0.0% | 16.4% |

→ 兩頻道內容差異極大：camman18 = Minecraft 沙盒，YouTube 一律歸 RPG/Action-adventure；GothamChess = 西洋棋，被歸 Strategy + Entertainment/Hobby/Lifestyle 混合。

### Layer 2 — 規則字典命中率
- camman18：`has_教學教育` 100.0%、`has_挑戰對決` 100.0%、`has_問句` 14.6%
- GothamChess：`has_挑戰對決` 7.3%、`has_問句` 3.6%、其餘 ≤ 1%

→ camman18 的 `has_教學教育 / has_挑戰對決` 100% 命中是因為 `tags` 欄含 "minecraft", "how to" 等通用詞，**這是 tag 重複導致的偽命中**（不是內容真的全是教學）。

### Layer 3 — TF-IDF Top 5 keywords
- camman18：minecraft, the, to, in, how
- GothamChess：jynxzi, he, gotham, magnus, chess

→ camman18 = Minecraft 完全主題化；GothamChess = 與名人 KOL（jynxzi, magnus carlsen）連動的內容。

### §7.5 卡方檢定（top_quartile 門檻 view_count ≥ 6,530,391）
- `has_教學教育` chi² = 39.9, **p = 2.68e-10 ***
- `has_挑戰對決` chi² = 37.8, **p = 7.69e-10 ***
- 其餘 ns 或樣本太集中
- Logistic 跳過（singular matrix）

注：這兩個顯著 bucket 完全來自 camman18（100% 命中）而 GothamChess（< 8%），等於是「頻道效應」被誤判為「內容標籤效應」 — 卡方在這裡實質上是 channel 的代理。

## 迴歸結果
- Model 1（duration + title_length + tag_count）：R² = 0.208, Adj R² = 0.201
  - duration_sec: ns
  - title_length: +511k *（p=0.075，邊緣）
  - tag_count: **+1.65M ***（p<0.001）— 多 tag 強烈正相關
- Model 2（加 channel dummy）：R² = 0.208, Adj R² = 0.201（相同）
  - **C(channel)[camman18]: +2.51M ***（p<0.001）**
  - tag_count 在加 dummy 後變不顯著（邊緣 p=0.08）
  - 設計矩陣 condition number = 5.7e15 → **嚴重共線性**：channel 與 tag_count 幾乎完全共線（camman18 平均 29 tag、Gotham 5 tag）
- VIF：duration 1.05、title_length 1.53、tag_count 1.57（單獨看 OK，但加 channel dummy 後 channel-tag 共線無法分離）

## 對應企劃書研究問題
- RQ1（標題長度）：邊緣正相關，但同樣是頻道風格代理（camman18 標題長、tag 多、觀看高）
- RQ3（標籤數量）：**Model 1 中極顯著正相關**，但無法分離 channel 效應 — 這是兩頻道間最大行為差異
- RQ6（影片長度）：duration_sec ns — Shorts 內幾乎所有片都 < 60s，變異有限
- RQ7（訂閱數）：camman18 訂閱多 42%，但平均觀看多 168% → 不只訂閱基礎，內容/演算法分發也有差

## 限制與註記
- 兩頻道規模都極大（10M+ 訂閱），mean_view 量級接近 5M，與其他類別（10K~100K 量級）差 50-500 倍 — **跨類別比較時 view_count 必須 normalize**
- camman18 tag 高度重複（每片有相同 30+ tag），tag_count 變異主要來自「有 vs 沒有」非「多 vs 少」
- title_length 在 camman18 平均 6.98 個英文 word（純英文），GothamChess 平均 2.57 word — 對英文頻道 EN word count 是主要驅動，CJK 全 0
- channel × tag_count 共線嚴重，獨立估計 RQ3 在這個類別上不可信賴
- view_count 嚴重右偏（kurtosis 13.5），OLS 殘差非常態，宜改 log-OLS
