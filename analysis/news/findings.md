# 時事類 Shorts 分析發現

> 資料：data/processed/channel_videos_20260527-065044.csv（5 頻道，1,214 部影片）
> 範圍：Shorts 過濾條件 duration_sec ≤ 180，共 964 部 Shorts。

## 樣本概況
- 5 個頻道：@Johnny Harris、@Vox、@志祺七七、@喵耳電波、@Real Fake
- Shorts 樣本：964 部
- 各頻道 Shorts 篇數：
  - 喵耳電波：286
  - 志祺七七：247
  - Johnny Harris：212
  - Vox：211
  - Real Fake：8  ← 樣本不足，描述統計保留但檢定建議排除

## 關鍵統計
| 指標 | mean | median | std |
|---|---:|---:|---:|
| view_count | 533,436 | 149,132 | 1,216,269 |
| like_count | 21,561 | 3,360 | 59,321 |
| comment_count | 685.4 | 153 | 2,144 |
| duration_sec | 54.4 | 48 | 27.8 |
| title_length | 35.1 | 35 | 17.5 |
| tag_count | 18.7 | 3 | 25.6 |

頻道級摘要：
| 頻道 | n_shorts | mean_view | median_view | mean_like | mean_comment |
|---|---:|---:|---:|---:|---:|
| Johnny Harris | 212 | 1,730,981 | 920,258 | 83,529 | 2,432 |
| Real Fake | 8 | 961 | 211 | 17.3 | 5.3 |
| Vox | 211 | 41,726 | 29,698 | 885 | 49.5 |
| 喵耳電波 | 286 | 291,926 | 186,478 | 5,884.5 | 299 |
| 志祺七七 | 247 | 222,515 | 156,419 | 5,137 | 199 |

## 頻道間 ANOVA
- view_count: F=92.91, p=8.42e-67 → 極顯著（5 類別中觀看差異最劇烈）
- Johnny Harris 平均觀看為 Real Fake 的 1,800 倍

## 標題長度分組 ANOVA
- 短:n=325 mean=489,807；中:n=324 mean=716,823；長:n=315 mean=389,822
- F=6.15, p=2.21e-3 → 顯著；中等長度最佳（非單調）

## 標籤數量分組 ANOVA
- 無標籤:n=119 mean=1,708,987；1-3:n=457 mean=139,430；4+:n=388 mean=636,966
- F=97.13, p=3.80e-39 → 極顯著；無 tag 的反而觀看最高 → 多為 Johnny Harris 等英文長片頻道短片化（不打 tag）

## 內容貼標發現
### Layer 1 — YouTube topic 主導
- Johnny Harris: Society 57% / Politics 37% / Knowledge 15% / Military 13%
- Vox: Society 57% / Politics 48% / Lifestyle 17% / Entertainment 9.5%
- 志祺七七: Entertainment 79% / Lifestyle 18% / Pet 3.2%
- 喵耳電波: Entertainment 52% / Video_game_culture 23% / Society 15%
- Real Fake: 全空（topic_categories 缺失）

### Layer 2 — 規則字典命中率 Top 3
| 頻道 | has_問句 | has_搞笑迷因 | has_挑戰對決 |
|---|---:|---:|---:|
| Johnny Harris | 19.8% | 0% | 0.9% |
| Vox | 26.1% | 0% | 0.9% |
| 志祺七七 | 55.9% | 0% | 1.6% |
| 喵耳電波 | 29.7% | 100% | 5.2% |
| Real Fake | 0% | 0% | 0% |

→ 喵耳電波 has_搞笑迷因=100% 是因「迷因」一詞在頻道名/標籤中常出現（字典觸發）

### Layer 3 — TF-IDF Top 5
- Johnny Harris: the, why, is, how, are
- Vox: the, is, to, why, how
- 志祺七七: 志祺, 七七, shorts, 日本, 台灣
- 喵耳電波: 直接, asmongold, asmon, 結果, vs
- Real Fake: tedua, per, intro, izi, charles（義大利語）

### 內容標籤與高觀看（卡方 + Logistic）
- has_問句 χ²=17.52, p=2.84e-5 ***
- has_搞笑迷因 χ²=3.21, p=0.073（接近顯著）
- Logistic 顯著項：has_搞笑迷因 (β=−0.37, p=0.036)、has_問句 (β=−0.72, p<0.001)
  → 在 news 類別，has_問句 = 1 的影片**較少**進入 top quartile（因 top quartile 由 Johnny Harris 英文長片碎片化主導，其 has_問句 = 19.8%）

## 迴歸結果
| 模型 | R² | Adj R² |
|---|---:|---:|
| M1（duration + title_length + tag_count） | 0.053 | 0.050 |
| M2（+ C(channel_title)） | 0.283 | 0.278 |

- M2 的 ΔR² = +0.230，三類別中最大 → 頻道效應極強
- 顯著預測子（M2）：title_length (−, β=−115K, p=0.038)；C(channel_title) 多項 p<0.001
- VIF：title_length=2.07, tag_count=1.93, duration_sec=1.15 → 接近邊界但仍可接受

## 對應企劃書研究問題
- RQ1 標題長度：顯著（非單調，中等長度最佳）
- RQ3 標籤數量：顯著但反向 — 無 tag > 4+ tag > 1-3 tag
- RQ6 影片長度：r=−0.017, p=0.59 → 不顯著
- RQ7 訂閱數：Johnny Harris (高訂閱) 反差大，主要因「英文長片頻道做 Shorts」的稀缺性紅利

## 限制與註記
- Real Fake n=8 嚴重不足，建議檢定排除（描述統計保留）
- 觀看數極偏（std/mean=2.28），Johnny Harris 一個頻道把 mean 拉高
- 字元數計算偏誤：英文（Johnny Harris, Vox）vs 中文（志祺七七, 喵耳電波）混雜
- has_搞笑迷因 對喵耳電波 100% 命中是字典 spurious — 頻道描述含「迷因」字
