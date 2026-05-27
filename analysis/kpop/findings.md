# Kpop Shorts 分析發現

## 樣本概況
- 兩個頻道：@kukuo1019（kukuo 쿠쿠）、@k-chaoliu（K-潮流）
- 抓取原始：308 部；分析樣本：Shorts 298 部（duration_sec ≤ 180）
- K-潮流 n = 200；kukuo 쿠쿠 n = 98（兩頻道樣本均 ≥ 30，可進行檢定）
- 注：企劃書原列「Lablodol」因無 @handle，本次未含入；待後續手動補 channel_id

## 關鍵統計（Shorts 整體）
| 指標 | mean | median | std |
|---|---|---|---|
| view_count | 145,826 | 50,548 | 316,431 |
| like_count | 3,268 | 1,234 | 5,888 |
| comment_count | 22.3 | 10 | 34.3 |
| duration_sec | 35.9 | 31 | 20.0 |
| title_length | 40.5 | 39 | 21.9 |
| tag_count | 1.6 | 0 | 2.3 |

每頻道摘要：
| channel | n | mean_view | median_view | mean_like | mean_comment |
|---|---|---|---|---|---|
| K-潮流 | 200 | 102,862 | 54,838 | 2,569 | 19.5 |
| kukuo 쿠쿠 | 98 | 233,508 | 17,199 | 4,695 | 28.0 |

注意：kukuo mean 高但 median 低 → 有少數爆款拉高均值。

## 兩頻道差異（Mann-Whitney U，K-潮流 vs kukuo 쿠쿠）
- view_count: p = 0.044 *  → **kukuo 顯著高（憑爆款分佈）**
- like_count: p = 0.041 *  → kukuo 顯著高
- comment_count: p = 0.0036 **  → kukuo 顯著高
- title_length: p = 6.89e-37 ***  → K-潮流 顯著長（51.2 vs 18.7）
- tag_count: p = 5.07e-48 ***  → kukuo 顯著多 tag（3.9 vs 0.4）

kukuo 訂閱（5,290）vs K-潮流 訂閱（76,600）= 1:14，但 kukuo 觀看更高 → **訂閱數與 Shorts 觀看脫鉤**，是 Kpop 類別最反直覺發現。

## 內容貼標發現（§4.5 / §7.5）

### Layer 1 — YouTube topic（前 4 大）
| topic | K-潮流 | kukuo 쿠쿠 |
|---|---|---|
| Entertainment | 69.0% | 81.6% |
| Lifestyle | 13.5% | 3.1% |
| Humour | 6.0% | 0.0% |
| Music | 3.5% | 4.1% |
| Music_of_Asia | 3.5% | 4.1% |

→ kukuo 純粹 Entertainment（K-pop 偶像 reaction），K-潮流帶 Lifestyle/Humour（八卦+娛樂評論混合）。

### Layer 2 — 規則字典命中率（前 3 高 buckets）
- K-潮流：`has_教學教育` 7.0%、`has_搞笑迷因` 4.0%、`has_互動誘導` 3.0%
- kukuo 쿠쿠：`has_問句` 9.2%、`has_食物` 5.1%、`has_情緒詞` 5.1%

→ Kpop 字典命中率整體很低（< 10%），現有 v1.0 字典對 K-pop 偶像文本覆蓋不足，建議 Phase 2 增 `偶像/應援/直拍/MV` bucket。

### Layer 3 — TF-IDF Top 5 keywords
- K-潮流：xd、karina、潮流、真的、自己
- kukuo 쿠쿠：haewon、bae、yuna、真的、lily

→ 兩頻道都圍繞偶像名（karina, haewon, yuna, lily, bae）；K-潮流多評論詞（潮流、自己、忍不住、立刻），kukuo 多人物名 + 動作（捉弄、表情、撒嬌）。

### §7.5 卡方檢定（top_quartile 門檻 view_count ≥ 125,806）
- 所有 bucket p > 0.05 → **內容字典標籤對 Kpop 高觀看無預測力**
- 多 bucket 樣本太集中（has_挑戰對決 / has_開箱評測 / has_品牌推廣 / has_運動）跳過
- Logistic 跳過（singular matrix）

## 迴歸結果
- Model 1（duration + title_length + tag_count）：R² = 0.029, Adj R² = 0.019 — **解釋力極弱**
  - 所有連續變數 ns
- Model 2（加 channel dummy）：R² = 0.043, Adj R² = 0.030
  - C(channel)[kukuo 쿠쿠]: +136.5k * (p=0.035) — kukuo 平均觀看顯著較高
  - duration_sec / title_length / tag_count 仍 ns
- VIF：duration 1.25、title_length 1.53、tag_count 1.78（OK）

整體 R² < 5% → Kpop Shorts 的觀看主要由「該影片拍到哪個偶像/事件」決定，與標題或長度幾乎無關。

## 對應企劃書研究問題
- RQ1（標題長度）：Pearson r = −0.15 **（負相關），但 OLS 控制後不顯著 → 標題短反而稍微高觀看（kukuo 的標題短而觀看高）
- RQ3（標籤數量）：相關性 ns；兩頻道 tag 策略差很多但對結果影響小
- RQ6（影片長度）：與 view_count 幾乎無相關（r = −0.05）— Kpop Shorts 普遍 < 60s，變異有限
- RQ7（訂閱數）：**反向**——kukuo 訂閱僅 K-潮流的 7% 但平均觀看是 2.3 倍。Kpop Shorts 推送高度仰賴演算法外推，訂閱不是主因子

## 限制與註記
- kukuo 樣本 98 部低於 K-潮流（200 部），mean 易被少數爆款（>1M）拉高 → Mann-Whitney 用 rank 較穩健，仍顯示 kukuo 顯著
- kukuo 標題大量為「人名+動作描述」（如「Yeji 一句話馬上引起抗議」），title_length 短是該頻道風格
- v1.0 字典對 Kpop 內容命中率低（< 10%），下一版宜增「偶像/演唱會/應援/MV/直拍/造型」buckets
- 兩頻道都把偶像名寫在 title（描述區的 hashtag 也常用），故 TF-IDF 結果反映粉絲關注的 idol
- Lablodol 缺值：企劃書原列三頻道，只有兩頻道 @handle 抓得到，已於樣本檔記錄
