# 運動類 Shorts 分析發現

> 資料：data/processed/channel_videos_20260527-064706.csv（4 頻道 × 400 部 = 1,600 部影片）
> 範圍：Shorts 過濾條件 duration_sec ≤ 180，共 1,172 部 Shorts。

## 樣本概況
- 4 個頻道：@NBA、@MLB、@挖掘肌讲健身、@老赵闹健身
- Shorts 樣本：1,172 部（占抓取資料 73.2%）
- 各頻道 Shorts 篇數（皆 ≥ 30，無需排除）：
  - 老赵闹健身：393
  - 挖掘肌讲健身：369
  - NBA：274
  - MLB：136

## 關鍵統計
| 指標 | mean | median | std |
|---|---:|---:|---:|
| view_count | 74,532 | 20,401 | 169,025 |
| like_count | 1,098 | 319 | 2,308 |
| comment_count | 36.8 | 9.0 | 75.9 |
| duration_sec | 50.1 | 32.0 | 45.1 |
| title_length | 58.9 | 50.0 | 28.1 |
| tag_count | 8.3 | 6.0 | 8.6 |

頻道級摘要：
| 頻道 | n_shorts | mean_view | median_view | mean_like | mean_comment |
|---|---:|---:|---:|---:|---:|
| MLB | 136 | 72,095 | 32,384 | 1,189.7 | 34.0 |
| NBA | 274 | 94,176 | 53,029 | 1,699.2 | 80.9 |
| 挖掘肌讲健身 | 369 | 15,223 | 5,927 | 265.3 | 6.3 |
| 老赵闹健身 | 393 | 117,367 | 22,517 | 1,427.9 | 35.5 |

## 頻道間 ANOVA
- view_count: F=26.4153, p=1.56e-16 → 極顯著
- 排序：老赵闹健身 > NBA > MLB > 挖掘肌讲健身

## 標題長度分組 ANOVA（qcut 三等分位）
- 短:n=396 mean=34,291；中:n=398 mean=73,460；長:n=378 mean=117,818
- F=24.58, p=3.50e-11 → 顯著；長標題平均觀看是短標題的 3.4 倍

## 標籤數量分組 ANOVA
- 無標籤:n=153 mean=88,941；4+:n=1019 mean=72,368（此類別無 1-3 組）
- F=1.28, p=0.258 → 不顯著

## 內容貼標發現
### Layer 1 — YouTube topic 主導
- NBA: Sport 97% / Basketball 96%
- MLB: Baseball 96% / Sport 94%
- 挖掘肌讲健身: Physical_fitness 91% / Lifestyle 89% / Health 65%
- 老赵闹健身: Physical_fitness 86% / Lifestyle 90% / Health 68%

### Layer 2 — 規則字典命中率 Top 3
| 頻道 | has_運動 | has_搞笑迷因 | has_問句 |
|---|---:|---:|---:|
| MLB | 99.3% | 0% | 4.4% |
| NBA | 47.1% | 0% | 0.7% |
| 挖掘肌讲健身 | 100% | 0.3% | 2.7% |
| 老赵闹健身 | 100% | 9.2% | 0.3% |

### Layer 3 — TF-IDF Top 5
- MLB: the, mlb, to, highlights, in
- NBA: the, in, to, game, wemby
- 挖掘肌讲健身: 训练, 健身, 水平, 力量, 肌肉
- 老赵闹健身: man, 健身, 猛男, 教练, 美女

### 內容標籤與高觀看（卡方）
- has_運動 χ²=32.71, p=1.07e-8 *** （注意：實為頻道差異代理，因 100% vs 47% 的分布幾乎二元）
- Logistic 因奇異矩陣（多 has_* 全為 0/1）跳過

## 迴歸結果
| 模型 | R² | Adj R² |
|---|---:|---:|
| M1（duration + title_length + tag_count） | 0.055 | 0.053 |
| M2（+ C(channel_title)） | 0.065 | 0.060 |

- 顯著預測子（M1）：title_length (+, β=+30K)、duration_sec (−, β=−16K)
- VIF：duration_sec=1.10, title_length=1.08, tag_count=1.02 → 無共線性
- 殘差偏態嚴重（Skew=6.03）→ 標準誤可能低估

## 對應企劃書研究問題
- RQ1 標題長度：顯著（F=24.58）
- RQ3 標籤數量：不顯著
- RQ6 影片長度：r=−0.152, p<0.001 → 越短觀看略多
- RQ7 訂閱數：MLB (7.2M) 平均觀看反低於老赵闹健身 (76.5K)，訂閱規模非主導因子

## 限制與註記
- 字元數計算偏誤：英文以單詞分隔，中文密集；NBA/MLB title_length=50 約 8–10 英文詞，中國頻道 50 約 25–30 漢字
- 觀看數極偏（std/mean ≈ 2.3），建議補做 Kruskal-Wallis
- 同類別內部異質：英文體育官方 vs 中文教學/迷因混雜
- 無樣本不足頻道
