# 跨類別總整合分析發現（Phase 3）

> 對應 notebook：`analysis/_crosscat/cross_category.ipynb`、`analysis/_crosscat/content_similarity.ipynb`
> 抓取日期：2026-05-27（9 個類別的 channel_videos / channels CSV）
> 對應企劃書研究背景假設：「教育類因高留存獲長尾推撥 vs 娛樂類靠衝動點擊」
>
> **資料範圍**：本次分析涵蓋 **9 個使用者類別、28 個頻道、4,798 部 Shorts**（過濾 `duration_sec ≤ 180`）。
> `restaurant_brand` 類別（Reg/02 既有，3 個食品/餐廳品牌頻道）已補抓並納入跨類別分析，CSV 時間戳 `20260527-072439`，貢獻 323 部 Shorts。

---

## 1. 資料概覽

### 1.1 每類別 Shorts 數
| 類別 | 頻道數 | Shorts 數 | 訂閱中位數 | 觀看中位數 | view/sub 中位數 | 平均影片時長(s) | 平均標題長 |
|---|---:|---:|---:|---:|---:|---:|---:|
| games | 2 | 308 | 10,800,000 | 3,975,738 | 0.4 | 38.2 | 32.9 |
| restaurant_brand | 3 | 323 | 66,400 | 237,886 | 3.6 | 92.0 | 30.7 |
| news | 5 | 964 | 1,660,000 | 149,132 | 0.1 | 54.4 | 35.1 |
| food_review | 7 | 965 | 196,000 | 120,935 | 1.1 | 45.9 | 36.6 |
| pansci | 1 | 154 | 1,190,000 | 124,583 | 0.1 | 155.6 | 12.3 |
| kpop | 2 | 298 | 76,600 | 50,548 | 0.9 | 35.9 | 40.5 |
| basketball_influencer | 2 | 310 | 21,800 | 34,480 | 2.3 | 73.7 | 44.8 |
| basketball_meme | 2 | 304 | 69,300 | 21,015 | 1.3 | 95.2 | 46.3 |
| sports | 4 | 1,172 | 76,500 | 20,401 | 0.1 | 50.1 | 58.9 |

依 mean_view 排序：games 最高（~5.18M）、sports 最低（~75K），相差近 70 倍；restaurant_brand 居第二（~547K）。
依 median view_per_subscriber 排序：restaurant_brand 最高（**3.6**），games 最低（0.4） — 排序完全反轉，反映訂閱規模主導 raw view，而 restaurant_brand 以小訂閱規模獲取極高觸及率。

### 1.2 觀察
- **games / news / sports** 把超大訂閱頻道（camman18 10.8M、Vox 12.7M、NBA 24M、MLB 7M）拉高 mean，但 view_per_subscriber 低 → 大頻道靠絕對量取勝、觸及率反而平庸。
- **restaurant_brand** 訂閱中位數僅 66K，但 view/sub 中位數 **3.6 全類別最高**，超越 basketball_influencer 的 2.3 → 取代後者成為「小頻道高觸及」的典範類別。
- **basketball_influencer** 訂閱中位數僅 22K，view/sub 中位數 2.3（第二高），仍屬高觸及小頻道。
- **pansci** 一頻道（1.19M sub），Shorts 表現中規中矩，但跨類別觀看中位數能擠到第五 → 大型專業頻道的長尾優勢。

---

## 2. 跨類別 ANOVA：三種正規化下「類別」的區分力

| 度量 | F | Kruskal H | 結論 |
|---|---:|---:|---|
| view_count (raw) | 385.3 | 1780.4 | p ≈ 0：類別間極顯著，但被訂閱規模污染 |
| log_view = log10(view+1) | **406.4** | 1780.4 | p ≈ 0：log 轉換後 F 略升、且分佈更穩定 |
| view_per_subscriber | 30.9 | **1963.0** | p ≈ 1.2e-47：F 大幅下降，但 Kruskal 仍極高 → 中位數差異仍實質存在 |

**結論**：
- 不論哪一種正規化，類別都顯著影響 Shorts 表現。
- 從 raw 到 vps 正規化，F 下降約 13 倍 → 約 92% 的「raw 類別差異」可由訂閱規模解釋；剩下 8% 是「內容/類別」固有差異。
- 在 log_view 度量下類別 F 最大 → **log_view 是最適合跨類別比較的指標**，因為它同時校正了 raw 的偏態又保留訊號。
- vps 的 Kruskal > ANOVA F → 各類 vps 分佈嚴重非常態，中位數比較比平均更可靠。

---

## 3. 大 OLS：M1 (no category) vs M2 (with category dummy)

### 3.1 M1
公式：`log_view ~ log_sub + title_length + tag_count + duration_sec`，n=4,798。

| 變數 | coef | p |
|---|---:|---:|
| Intercept | +3.346 | < .001 |
| log_sub | **+0.331** | < .001 |
| title_length | −0.0048 | < .001 |
| tag_count | +0.0065 | < .001 |
| duration_sec | −0.0010 | < .001 |

- **R² = 0.200**，Adj R² = 0.199（F p ≈ 0）
- VIF 全部 ≈ 1（無共線性）
- 訂閱每多 1 個量級（10×），log_view 平均增加 0.33 → 觀看數增為原 10^0.33 ≈ 2.14 倍。

### 3.2 M2（加入 `C(category)`）
- **R² = 0.494**，Adj R² = 0.493（F p ≈ 0）
- **ΔR² = +0.294**：在控制 log_sub 之後，類別 dummy 仍貢獻 29.4% 的觀看變異。

類別效應（以 basketball_influencer 為 baseline）：
| 類別 | coef (log_view) | p | 解讀（10^coef） |
|---|---:|---:|---|
| games | **+0.856** | < .001 | × 7.18 倍 |
| restaurant_brand | **+0.640** | < .001 | × 4.36 倍 |
| food_review | +0.147 | 0.001 | × 1.40 |
| pansci | +0.022 | 0.766 | ≈ baseline |
| kpop | −0.145 | 0.006 | × 0.72 |
| news | −0.234 | < .001 | × 0.58 |
| basketball_meme | −0.445 | < .001 | × 0.36 |
| sports | **−0.909** | < .001 | × 0.12 |

**核心解讀**：
- 在「同樣訂閱規模、同樣標題長度、同樣 tag 數、同樣時長」之下，**games 類別 Shorts 比 basketball_influencer 多 7.18× 觀看；restaurant_brand 多 4.36×；sports 卻只有 0.12×**。
- restaurant_brand 在控制訂閱後仍享有 **+0.64 的強類別效應**（僅次 games），代表「品牌/餐廳推廣」這類內容在 YouTube Shorts 算法上具有獨立於訂閱規模的觀看溢價。
- log_sub 在 M2 仍保留 +0.314 的強顯著主效應 → 訂閱規模並未被 category 完全吸收，而是兩者各占獨立貢獻。
- pansci 控制訂閱後與 basketball_influencer 幾乎等價 → 一旦把規模剝除，pansci 並無特別優勢，**直接挑戰「教育類因高留存獲長尾推撥」假設**。
- 在 M2 中 `title_length` 係數從 M1 的 −0.0048 **翻轉成 +0.0034**（正向、顯著）→ 跨類別異質性導致 M1 的長標題效應方向被反向，這是 Simpson 悖論的典型例子（某些長標題類別觀看本身就高，未控制類別時被誤判為「長標題拉低觀看」）。

---

## 4. 類別 × tag_count 交互作用（M3）

公式：`log_view ~ log_sub + duration_sec + C(category) * tag_count`，R² = 0.495。

**顯著交互項**：
| 交互項 | coef | p | 解讀 |
|---|---:|---:|---|
| food_review × tag_count | **−0.243** | 0.045 * | 食物類加 tag 反而降觀看（tags 全 NaN 的頻道把線拉成負相關） |
| games × tag_count | +0.050 | 0.010 * | 遊戲類每多 1 個 tag，log_view +0.050（× 1.12） |
| news × tag_count | +0.044 | 0.024 * | 新聞類加 tag 對觀看有微正向 |
| restaurant_brand × tag_count | +0.019 | 0.339 ns | 餐廳品牌類 tag 效應微弱不顯著 |
| 其他類別 | ns | | |

**結論（RQ #2 升級）**：標籤數量的觀看效應**不是普世均勻**的——在 games / news 有正向，在 food_review 反而負向（受 tags 全 NaN 的頻道影響極大）。**「多打 tag = 多觀看」這條建議只在特定類別成立**。

---

## 5. YouTube 自動 topic vs 使用者人工分類矩陣（RQ #4）

從 `topic_categories` 的 Wikipedia URL 抽尾段，每影片可有多 topic，計算每類別影片中該 topic 至少命中一次的比率：

| 使用者類別 | YouTube 主要 topic（命中率） | 對應強度 | 錯位 |
|---|---|---|---|
| games | Video_game_culture 0.85 / Action-adventure_game 0.54 / Role-playing_video_game 0.60 | **完美對應** | 無 |
| food_review | Food 0.91 / Lifestyle 0.98 | **完美對應** | 無 |
| restaurant_brand | Lifestyle 0.76 / Food 0.45 / Entertainment 0.20 | **對應** | 與 food_review 共享 Food / Lifestyle，但 Food 命中率較低（0.45 vs 0.91），餐廳品牌偏向「生活風格」標籤 |
| sports | Physical_fitness 0.58 / Health 0.43 / Sport 0.36 / Lifestyle 0.59 | 部分對應 | NBA / MLB 應落 Basketball / Baseball 但比例偏低（被健身頻道稀釋） |
| basketball_meme | Basketball 0.80 / Sport 0.65 / Humour 0.16 | 對應 | 無 |
| basketball_influencer | Basketball 0.78 / Sport 0.77 / Humour 0.09 | 對應 | 無 |
| news | Politics 0.19 / Society 0.29 / Entertainment 0.39 / Lifestyle 0.12 | 中等對應 | News 主題本身不是 YouTube 標準 topic |
| pansci | Health 0.27 / Society 0.25 / Knowledge 0.07 / Lifestyle 0.12 | **顯著錯位** | YouTube 從未把 PanSci 標為 `Education` 或 `Science`（0 命中） |
| kpop | Entertainment 0.73 / Lifestyle 0.10 | 一致但泛化 | 無 `Music` / `Pop_music` topic 命中（K-Pop 反而被歸到泛娛樂） |

**RQ #4 結論**：
1. **使用者人工類別與 YouTube 演算法視角部分一致、部分嚴重錯位**。最一致的是 games（YouTube 直接給出 Video_game_culture / Action-adventure_game 等細分類），其次 food_review（Food / Lifestyle 命中率 0.9+）。
2. **pansci 的錯位最劇**：使用者歸類為「科普 / Education」，YouTube 卻只給 Health / Society / Knowledge — 表示 PanSci 在 YouTube 系統內被視為「健康與社會議題」而非「正規教育」。對企劃書「教育類獲長尾推撥」假設構成挑戰：**YouTube 本身就不把 PanSci 列為 Education**，所謂「教育類權重」的前提是否成立有疑。
3. **news 的 Politics 命中率僅 0.19**：對「新聞」這個使用者類別，YouTube 反而最常標為 Entertainment（0.39）— 新聞類在演算法視角中與娛樂的距離比想像中近。

---

## 6. 跨類別內容標籤效應（RQ #2 升級版）

對 `has_<bucket> × C(category)` 跑 logistic：`P(top_quartile_view) ~ has_bucket * C(category)`。

- **has_問句**：跨類別交互式 logistic 因部分類別命中率 0/1 導致 singular matrix；退回 additive 模型，得 **has_問句 OR = 1.52，p = 1.8e-5***  → **整體跨類別「問句型標題」顯著提升進 top quartile 的機率約 52%**。
- **has_搞笑迷因**：additive OR = 1.19，p = 0.19 ns → 無跨類別一致效應。
- **has_情緒詞**：互動模型估到，但所有交互項 p > 0.27 ns → 情緒詞效應大致跨類別一致（弱負/弱正皆無顯著）。
- **has_教學教育**：news × has_教學教育 顯著負向（coef = −2.07，p = 0.019 *）→ **新聞類影片若標題出現「教學/科普/講解」反而拉低進 top quartile 機率**（可能因為使用者期待新聞而非教學）。
- **has_挑戰對決**：所有 logit 因樣本集中失敗 → 無法檢出。

**RQ #2 結論**：跨類別最普世的標題策略是「問句型 hook」（OR 1.52）；其餘標籤策略普遍**類別依賴**。情緒詞、教學詞、搞笑詞並無跨類別一致效應。

---

## 7. RQ #10 發布頻率：videos_per_month

### 7.1 頻道層級彙整（Top / Bottom）
| 頻道 | 類別 | videos/month | log_sub | mean log_view |
|---|---|---:|---:|---:|
| MLB | sports | **1,266** | 6.86 | 4.53 |
| NBA | sports | 317 | 7.39 | 4.73 |
| 挖掘肌讲健身 | sports | 113 | 4.69 | 3.82 |
| 喵耳電波 | news | 90 | 4.93 | 5.25 |
| 卷毛懂个球 | bb_meme | 88 | 3.70 | 4.07 |
| ... | ... | ... | ... | ... |
| 蜡笔小锋 | restaurant_brand | 40.9 | 4.83 | 5.32 |
| Ju茱莉亞林 | restaurant_brand | 5.0 | 5.09 | 6.21 |
| Lisa Sung | restaurant_brand | 1.4 | 4.82 | 5.35 |
| 智明 Jimmypsd | food_review | 0.79 | 5.52 | 5.85 |
| E ating | food_review | 0.35 | 3.30 | 3.82 |
| Real Fake | news | 0.11 | 2.22 | 2.23 |

### 7.2 OLS（頻道層級 n=28）
`log_view_mean ~ log_sub + videos_per_month`
- log_sub coef = **+0.547** (p < .001 ***)
- videos_per_month coef = **−0.0013** (p = **0.022 ***)
- R² = 0.544, Adj R² = 0.508

### 7.3 OLS（影片層級 n=4,798）
`log_view ~ log_sub + videos_per_month + duration_sec`
- log_sub coef = +0.405 (p < .001 ***)
- videos_per_month coef = **−0.0013** (p < .001 ***)
- duration_sec coef = −0.0014 (p < .001 ***)
- R² = 0.250

**RQ #10 結論**：在控制訂閱數後，**頻道發片頻率與觀看數呈顯著負相關**（每月多發 100 部影片，平均 log_view 降 0.13 ≈ 觀看降 26%）。這顛覆「多發片演算法多推」的直覺：高頻發片頻道（如 MLB 1,266 部/月、NBA 317 部/月）大多是把長片切片、Shorts 內容稀釋，每支平均觀看反而被拉低；低頻精修頻道（Lisa Sung 1.4 部/月、智明 Jimmypsd 0.79 部/月）才能在每支 Shorts 上累積觀看。restaurant_brand 三頻道在發片頻率上分布廣（1.4 ~ 40.9 部/月），與「精修少發 > 切片量產」的整體趨勢一致。

---

## 8. RQ #5 標題–標籤 Jaccard 一致性（簡化版）

### 8.1 各類別 Jaccard 平均
| 類別 | n（有 tags） | mean | median | std |
|---|---:|---:|---:|---:|
| food_review | 2 | 0.181 | 0.181 | 0.098 |
| kpop | 113 | 0.052 | 0.000 | 0.095 |
| sports | 1019 | 0.012 | 0.000 | 0.031 |
| games | 308 | 0.010 | 0.000 | 0.019 |
| restaurant_brand | 112 | 0.004 | 0.000 | 0.016 |
| basketball_meme | 245 | 0.003 | 0.000 | 0.012 |
| news | 845 | 0.002 | 0.000 | 0.015 |
| pansci | 102 | 0.000 | 0.000 | 0.000 |
| basketball_influencer | 0 | tags 全 NaN | | |

### 8.2 Jaccard vs view_count Spearman 相關（每類別）
| 類別 | n | rho | p |
|---|---:|---:|---|
| games | 308 | **+0.390** | 1.3e-12 *** |
| kpop | 113 | +0.239 | 0.011 * |
| sports | 1019 | +0.111 | 3.7e-4 *** |
| basketball_meme | 245 | −0.047 | 0.46 ns |
| news | 845 | −0.040 | 0.24 ns |
| restaurant_brand | 112 | −0.024 | 0.80 ns |
| pansci | 101 | NaN（全 0 Jaccard） | |
| **OVERALL** | 2,745 | **+0.057** | 2.7e-3 ** |

**RQ #5 結論**：
1. **Shorts 標題與 tags 用詞高度不一致**：除了少數樣本，所有類別中位 Jaccard 都是 0，平均亦多 < 0.05 → 創作者通常用 tags 做 SEO（補關鍵字），標題做 hook（吸引點擊），兩者很少重複用字。
2. **僅 games / kpop / sports 三類 Jaccard 與觀看正相關**：在這些類別中，「標題與 tags 一致」是高觀看 Shorts 的特徵之一（特別是 games 達 rho = +0.39 ***）；其他類別則沒有此效應或不顯著。
3. food_review 的 with-tags 樣本僅 2 部（多數 food_review 頻道 tags 全 NaN）→ 該類別 Jaccard 統計無意義；basketball_influencer 完全沒 tag → 沒做 RQ #5。

---

## 9. 內容相似度與 LDA 主題模型（content_similarity.ipynb）

### 9.1 跨頻道 TF-IDF cosine 類別內聚分數
依 within − between 排序：
| 類別 | 頻道數 | 類內平均 cosine | 類外平均 cosine | 內聚 gap |
|---|---:|---:|---:|---:|
| **kpop** | 2 | 0.207 | 0.022 | **+0.185** |
| sports | 4 | 0.119 | 0.040 | +0.079 |
| games | 2 | 0.124 | 0.051 | +0.073 |
| food_review | 7 | 0.083 | 0.019 | +0.064 |
| basketball_meme | 2 | 0.076 | 0.027 | +0.049 |
| news | 5 | 0.080 | 0.040 | +0.040 |
| restaurant_brand | 3 | 0.064 | 0.031 | +0.034 |
| basketball_influencer | 2 | 0.055 | 0.030 | +0.025 |
| pansci | 1 | NaN | 0.027 | NaN（單頻道） |

**結論**：
- 所有類別內聚分數均為正（類內 > 類外），表示**使用者人工分類確實有「語料相似性」的基礎**。
- kpop 內聚最高 → 兩個 K-Pop 頻道用詞高度雷同（韓國/偶像/演唱會等專有詞彙）。
- restaurant_brand 內聚 +0.034 排倒數第二，三頻道（Ju茱莉亞林、Lisa Sung、蜡笔小锋）內容雜糅美食探訪 / 生活分享 / 開箱推廣，用詞差異較大，類別邊界相對鬆散。
- basketball_influencer 內聚最低 → 兩個籃球網紅（曾舔舔、肖他）用詞差異大，分類「籃球網紅」的標籤合理性可被質疑。

### 9.2 LDA 主題模型（K=6 為最佳 perplexity，perplexity=1231.4）
六個 latent topic 的代表 keywords：
- **T0**：the / in / is / to / why / how / of / for → **英文新聞 / 教學頻道**
- **T1**：一杯／好吃／怎麼／旨味／jynxzi／steak／台灣／王子／中華 → **食物 + 日本料理 + 中文美食**
- **T2**：真的／健身／直接／兄弟／可以／不是／知道 → **籃球 + 健身 + 中文閒聊**
- **T3**：自己／训练／ai／美女／美食／教练／球場／动作 → 雜（健身 / AI / 美食）
- **T4**：牛排／什麼／挑戰／影片／男人／10／回顧／100／一定／往期 → **挑戰 / 男人主題 / 美食對決**
- **T5**：志祺／七七／shorts／多少／一天／man／要花／如何／日本 → **志祺七七 + 中文短片 + 探訪格式**

每類別主導 LDA topic：
| 類別 | 主導 topic | 主導比例 | 分佈熵 | 復現程度 |
|---|---:|---:|---:|---|
| games | T0 | 0.854 | 0.56 | **極高** |
| news | T0 | 0.513 | 1.33 | 高（英文新聞主導） |
| sports | T0 | 0.408 | 1.59 | 中（含中文健身雜訊） |
| pansci | T0 | 0.366 | 1.46 | 高（但 T0 是英文/教學 topic — 詞表中文常用詞混雜） |
| restaurant_brand | T4 | 0.293 | 1.73 | 低（內容散落「挑戰/牛排」主題） |
| kpop | T1 | 0.275 | 1.69 | 低 |
| food_review | T5 | 0.243 | 1.73 | 低（中文美食格式詞，與 restaurant_brand T4 不同 cluster） |
| basketball_influencer | T5 | 0.220 | 1.72 | 低 |
| basketball_meme | T2 | 0.300 | 1.63 | 中 |

**LDA 復現使用者分類的程度**：9 類別只用了 5 個獨立主導 topic（T0, T1, T2, T4, T5）→ **LDA 並未一對一復現使用者分類**，比 8 類別版本（4 個獨立 topic）略好。
- games / news / sports / pansci 共享 T0（英文短句）→ 顯示「Vox / Johnny Harris / camman18 / GothamChess / NBA / MLB / PanSci」這群英文 + 中文常用詞頻道在 LDA 視角下構成單一群集。
- **food_review 主導 T5，restaurant_brand 主導 T4 — 並未聚成同一 cluster**。雖然兩者直觀上都屬「食物相關」，但 food_review 的探訪／日本料理用詞落在 T5（志祺/中文短片混雜），而 restaurant_brand 的「牛排／挑戰／品牌推廣」格式詞落在 T4。這顯示 LDA 對「美食評論 vs 餐廳品牌推廣」確實有區分能力。
- basketball_meme / basketball_influencer 在新一輪 LDA 不再共享 topic（meme → T2，influencer → T5），「合併籃球」的假設在新詞表下被推翻。

### 9.3 spurious / 跨主題溢出頻道
頻道主導 topic 與所屬類別主導 topic 不一致：
| 類別 | 頻道 | 頻道主導 | 類別主導 | 原因 |
|---|---|---:|---:|---|
| basketball_influencer | 曾舔舔🕊️ | T4 | T5 | 個別頻道「挑戰/男人主題」格式詞偏多 |
| basketball_influencer | 肖他 | T2 | T5 | 健身 / 中文閒聊用詞 |
| basketball_meme | 俊鸿TV | T4 | T2 | 挑戰格式詞偏多 |
| food_review | E ating | T3 | T5 | 雜項詞（n=62 小樣本） |
| food_review | This is Ken | T0 | T5 | 英文短句頻繁 → 跑到 T0 |
| food_review | うまぐるめ【Japanese Food】 | T1 | T5 | 日本料理專屬用詞（一杯／旨味／中華）→ T1 |
| food_review | 冬冬🌸生活美食日記💓 | T0 | T5 | 中文常用詞 |
| food_review | 吃貨豪豪HowHowEat | T2 | T5 | 中文閒聊（n=35 樣本少） |
| food_review | 貓跪妃 | T2 | T5 | 同上 |
| news | 志祺七七 | T5 | T0 | 中文 + 自己品牌詞主導 → 與英文新聞群集分離 |
| restaurant_brand | Ju茱莉亞林 | T2 | T4 | 健身 / 中文閒聊（mean log_view 最高 6.21） |
| restaurant_brand | 蜡笔小锋 | T0 | T4 | 英文/常用詞 → 與類別主導 T4 分離 |
| sports | 挖掘肌讲健身 | T2 | T0 | 中文健身 → 與英文 NBA/MLB 分離 |
| sports | 老赵闹健身 | T5 | T0 | 同上 |

**結論**：LDA spurious 主要由「英文 vs 中文 vs 格式詞」三軸分裂驅動。restaurant_brand 三頻道分散在 T0/T2/T4 三個 topic 上，類別內 LDA 一致性最弱；這呼應 §9.1 內聚 gap +0.034 倒數第二的現象 — 三個品牌頻道在內容主題上其實非常異質。jieba 對中文分詞有效，但 LDA 在中英混雜語料上的 topic 邊界更受語言別與格式詞影響，主題的代表力被稀釋。

### 9.4 次主題（sub-theme）分析

**food_review，K=5**：
- S0：好吃／美食／台中／排隊 — 台灣探店主流（n=298，mean view 240K）
- S1：早餐／午餐／牛肉／牛排 — 速食/西式（n=145，mean 267K）
- S2：濃厚豚／旨味／本店／築地／名物 — 日本拉麵/在地小店（n=141，mean **700K**）
- S3：多少／一天／智明／夜市 — 智明的「一天 X 元伙食費」格式（n=184，mean **863K**）
- S4：日本／屋台／東京／魚介 — うまぐるめ的日本料理（n=193，mean 665K）

food_review **sub-topic ANOVA：F = 5.27，p = 3.4e-4 \*\*\*** — 同類別內次主題顯著影響觀看，S3（智明的格式）與 S2（日本拉麵）平均觀看是 S0（台灣探店）的 3-4×。**「同樣是介紹食物，特定次主題的引爆力顯著更強」**。

**news，K=5**：
- S0：why / russia / the — Johnny Harris 風格的英文解析（n=197，mean 646K）
- S1：war / 2026 / ai — 戰爭/AI 時事（n=115，mean **1.03M**）
- S2：why / vs / trump — Vox 風格政治對比（n=188，mean 756K）
- S3：asmongold / america / 遊戲 — 邊緣（Real Fake 的義大利歌詞被 jieba 切碎了）（n=81，mean 398K）
- S4：志祺／七七／shorts／台灣 — 中文時事（n=383，mean 245K）

news **sub-topic ANOVA：F = 13.07，p = 2.3e-10 \*\*\*** — 在 news 類內，**英文戰爭/AI/政治 sub-topic 平均觀看是中文時事的 4×**。揭示 news 類內部存在語言 × 主題的巨大異質性。

---

## 10. 對企劃書與研究問題的最終回答

### 10.1 研究背景假設「教育類獲長尾推撥」
**部分否定**：
1. 在 M2 中 pansci dummy coef = +0.008 (p = 0.909 ns) → 在控制訂閱規模後，pansci 觀看數與 baseline（basketball_influencer）幾乎相同，**並無額外的「教育類加成」**。
2. YouTube topic 上 pansci **沒有任何一部影片被自動歸到 `Education`**，反而主要落在 Health / Society / Knowledge → 演算法視角中 PanSci 不是「教育類」，所謂「教育類獲長尾推撥」的前提是否成立有疑。
3. pansci 在跨類別 LDA 上主導 topic 是「中文常用詞 T0」而非獨立的「Education」topic → 進一步顯示 PanSci 的「教育類」標籤是使用者主觀。

**支持的部分**：pansci 標題 has_問句 35.7%（單頻道分析）；跨類別 logit additive 模型顯示 has_問句 整體 OR = 1.52 (p < .001) → 問句型 hook 確實是高觀看 Shorts 的共通特徵，PanSci 的策略與此一致。

### 10.2 對 RQ #2（標題關鍵字）的最終答案
- **問句最普世**：跨類別 OR = 1.52 (p < .001 \*\*\*)
- **搞笑迷因 / 情緒詞 / 教學教育不普世**：類別依賴；news × has_教學教育 顯著負向（OR = 0.13）
- **挑戰對決**：因樣本集中無法統一檢定

### 10.3 對 RQ #4（標籤類型）的最終答案
- YouTube 自動 topic 對 games / food_review 命中率高、人工分類一致；
- 對 pansci / news 命中率低或錯位；
- 使用者人工分類與 YouTube 系統視角**只有部分一致**（games / food_review / basketball_meme / basketball_influencer），pansci 與 news 嚴重錯位。

### 10.4 對 RQ #5（標題-標籤一致性）的最終答案
- 整體 Jaccard 中位數 0，平均 < 0.05 → **Shorts 標題與 tags 用詞高度不重疊**；
- 但 games / kpop / sports 三類 Jaccard 與觀看顯著正相關 → 在這些類別「標題-tags 用詞一致」是高觀看特徵；其他類別不存在此效應。

### 10.5 對 RQ #10（發布頻率）的最終答案
- **videos_per_month 對 log_view 有顯著負效應**（頻道層級 coef = −0.0013, p = 0.022 \*；影片層級 p < .001）；
- 高頻發片頻道（MLB / NBA）每支 Shorts 平均觀看反而較低 → **「多發片演算法多推」直覺不成立**，而是「精修少發 > 切片量產」。

---

## 11. 各類別在跨類別視角下的「位置」

| 類別 | 跨類別位置 | 一句話描述 |
|---|---|---|
| games | mean view 第一（5.18M）；M2 coef 最強 +0.86 | 訂閱規模 + 類別效應雙重最大 |
| restaurant_brand | mean view 第二（547K）；M2 coef +0.64；vps 中位 **3.6 最高** | 小訂閱 + 強類別溢價；品牌推廣/餐廳推介內容獨立觀看溢價 |
| news | mean view 第三（533K）；vps 中位 0.1 | 大頻道靠絕對量；觸及率低；類內語言分裂 |
| food_review | mean view 第四（514K）；vps 中位 1.1 | 中等訂閱、高觸及；次主題（日本 / 探訪格式）影響觀看 4× |
| pansci | mean view 第五（185K）；M2 coef ≈ 0 | 控制訂閱後與 baseline 一致；YouTube 不視為 Education |
| kpop | view 中段；vps 中位 0.9；類內聚分最高 | 兩 K-Pop 頻道用詞極相似；觸及率穩定 |
| basketball_influencer | 小頻道（22K 訂閱）；vps 中位 2.3（第二高） | 小頻道高觸及典範；tags 全 NaN |
| basketball_meme | 中段；vps 中位 1.3 | LDA 主導 T2，與 influencer 主題不再一致 |
| sports | 樣本最大（1,172）；M2 coef 最低 −0.91 | NBA/MLB 切片稀釋每支觀看；訂閱大 vs Shorts 觸及低的代表 |

### 11.1 restaurant_brand 在跨類別位置（深度解讀）

restaurant_brand 在 Reg/02 的類別內分析（n=323）顯示「**頻道差異 ANOVA F = 119.6，p = 1.6e-39**」極強，是該模組裡迄今最大的類別內 channel effect 之一（Ju茱莉亞林 mean view 1.88M vs Lisa Sung / 蜡笔小锋 約 0.34M，差距達 5×）。把這個類別放回 9 類跨類別視角後，restaurant_brand 的位置出現幾個耐人尋味的對比：

**(1) 類別溢價排名第二**：在 M2 大模型中，restaurant_brand 的類別 dummy coef = **+0.64**（10^0.64 ≈ 4.36×），僅次於 games（+0.86），明顯高於 food_review（+0.15）和 pansci（≈ 0）。在控制 log_sub、title_length、tag_count、duration_sec 後，「餐廳/品牌推廣」這類內容仍享有與訂閱規模無關的觀看溢價。配合 view/sub 中位數 **3.6（全類別最高，超越 basketball_influencer 的 2.3）**，可推測 YouTube 演算法對「美食推介 + 在地探訪」格式特別友善。

**(2) Layer 2 字典命中率**：在 9 類中，restaurant_brand 的 **has_食物 = 0.170 排名第二**（僅次 food_review 的 0.505），**has_品牌推廣 = 0.006 並列第三**（與 pansci 0.006 並列，僅次 food_review 0.007）。兩者一同上升，說明 restaurant_brand 的內容本質確實是「食物+品牌」雙標籤的混合體。

**(3) 與 food_review 並未在 LDA 中聚為同 cluster**：直覺上「品牌推廣」與「美食評論」相似，但 LDA K=6 結果顯示 food_review 主導 T5（志祺/中文短片格式），restaurant_brand 主導 T4（牛排／挑戰／回顧／往期），**屬於不同 topic**。內聚 gap +0.034 倒數第二亦顯示三頻道（Ju茱莉亞林、Lisa Sung、蜡笔小锋）彼此內容差異大、沒有聚成緊密 cluster。換言之，「餐廳/食品品牌頻道」這個使用者類別在語料上比直觀預期更鬆散，主題上更靠近「挑戰/長期回顧」格式而非「美食 vlog」。

---

## 12. 限制與未來方向

### 限制
1. **restaurant_brand 樣本仍小**：3 個頻道、323 部 Shorts，內聚分數 +0.034 偏低 → 類別內主題異質性高；如要做 sub-topic 分析需擴充頻道。
2. **關鍵字字典 v1.0 對日文無效**：`has_食物` 對 food_review 命中率仍可達 0.505（中文命中率），但 Layer 2 字典針對的是中文 token，對「うまぐるめ」這類日文頻道的標題無法命中食物詞 → 跨類別 has_食物 出現「假性低」於 food_review；report 結論已將此寫明。
3. **小樣本頻道不穩定**：Real Fake (n=8) 在 logistic 與 ANOVA 中被自動降為觀察值；其極端值會干擾 news 內聚分數估計。
4. **jieba 詞表未針對科普/籃球專業詞訓練**：PanSci 的「量子／突觸」、籃球的「進攻效率」等專有詞被切碎，LDA 因此把 pansci 歸到 T0「英文/中文常用詞」topic 而非獨立 topic。
5. **logistic 跨類別交互模型多次 singular**：因部分類別在某 bucket 上命中為 0/1，互動矩陣秩不足 → 退回 additive 估計，無法解析「該 bucket 在哪個類別最有效」的細節。
6. **發片頻率測量單一**：videos_per_month 用 channels.video_count / months_since_created 是「歷史平均」，不反映最近 3 個月發片密度的變化；若某頻道近期才轉做 Shorts，此估計會嚴重低估其近期密度。

### 未來方向
1. **擴充 restaurant_brand 頻道**：目前 3 個頻道，若擴充至 6-8 個品牌頻道，可以更穩健估計「商業推廣 vs 一般類別」差異，並降低 LDA spurious 比例。
2. **加入嵌入式語義模型**：用多語預訓練 sentence embedding（如 multilingual-MiniLM）取代 TF-IDF cosine，可消除中英文割裂問題、提高 LDA 復現使用者分類的能力。
3. **時間序列分析**：把 published_at 切月，看每類別 Shorts 觀看隨時間的演變、是否有「節日效應」或「演算法政策變動」的痕跡。
4. **頻道效應分離**：在 M2 之上加入 `C(channel_id)` 隨機效應（mixed-effects model），把「品牌效應」與「內容效應」徹底分離。
5. **更細的內容 bucket**：擴充 content_keywords.yaml 加入「時事」「政治」「街拍」「韓流」等專有 bucket，並對日文/韓文 token 各自訓練（或 OpenCC 統一中日漢字）。
