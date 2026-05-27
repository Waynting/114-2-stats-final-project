# 科普（PanScitw）Shorts 分析發現

> 對應 CSV：`data/processed/channel_videos_20260527-064747.csv`（抓取日期 2026-05-27）
> 模板：`analysis/_templates/template_single.ipynb`（已於 analysis.ipynb 新增 §6.2 多面向 ANOVA）

## 樣本概況
- 單頻道：@PanScitw（PanSci 泛科學）
- 影片總數：**200**（Shorts ≤180s = **154**，長片 >180s = **46**）
- 發布時段：154 部 Shorts 中 9 成集中在 UTC 11:00（=台灣 19:00），組間極度不平衡
- 期間跨度：依 published_at 排序後切 3 等分位，每段約 51–52 部

## 關鍵統計（Shorts，n=154）
| 指標 | mean | median | std |
|---|---:|---:|---:|
| view_count | 184,527 | 124,584 | 193,290 |
| like_count | 5,961 | 4,131 | 5,325 |
| comment_count | 219 | 165 | 189 |
| duration_sec | 155.6 | 161.0 | 29.6 |
| title_length | 12.3 | 11.0 | 6.4 |
| tag_count | 0.7 | 1.0 | 0.5 |

長片（n=46）：mean view = 134,678；mean like = 3,821；mean comment = 287。

## Shorts vs 長片 兩樣本檢定（取代頻道 ANOVA）
Mann-Whitney U（雙尾）：

| 指標 | Shorts mean | Long mean | p-value | 結論 |
|---|---:|---:|---:|---|
| view_count | 184,527 | 134,678 | 0.0977 | ns（Shorts 平均較高，邊界） |
| like_count | 5,961 | 3,821 | **0.0132** | * Shorts 顯著 > 長片 |
| comment_count | 219 | 287 | 0.169 | ns（長片留言略多） |

**結論**：PanSci 的 Shorts 在按讚數上顯著優於長片，觀看數雖然平均較高但統計上未達顯著；長片在留言互動上略勝（不顯著）→ 支持 Shorts 在「快速正向反饋（讚）」面向有觸及優勢。

## 時間分段 ANOVA（按 published_at 三等分位）
- **F = 4.5054，p = 0.0126 ***（顯著）
- 早期 mean view = 171,105 / 中期 = 246,299 / 近期 = 136,440
- **結論**：中期 Shorts 表現最佳，近期表現最差；發布時間段顯著影響觀看數。可能反映該頻道內容主題或演算法環境變化。

## 發布時段 ANOVA（早 6-11 / 中 12-13 / 下 14-17 / 晚 18-22 / 深夜 23-5）
- F = 0.0571，p = 0.811 ns
- 樣本極度集中：早(139)、中(14)、深夜(1)、下/晚(0)
- **結論**：PanSci 採固定發布時間策略（幾乎全部 UTC 11:00 = 台灣 19:00），此分析無法檢出有意義差異；於單頻道情境下「發布時段」並非可操作變數。

## 星期 ANOVA
- F = 0.3189，p = 0.926 ns
- 平日（週二/四/三）發片最多（26–27 部），週一最少（13 部）
- **結論**：星期並未顯著影響 PanSci Shorts 觀看數。

## 標題長度分組 ANOVA（qcut 三等分位）
- 分位邊界：短 ≤10 / 中 10–12 / 長 12–67 字
- F = 0.2692，p = 0.764 ns
- **結論**：標題長度並非 PanSci Shorts 觀看數的顯著預測子。

## 標籤數量分組 ANOVA
- 0 tags（n=52）vs 1 tag（n=102）；無 ≥2 tag 案例
- F = 0.6964，p = 0.405 ns
- **結論**：PanSci 的 tag 策略過於單一（要嘛沒 tag、要嘛 1 個），無法檢出顯著差異。

## 內容貼標發現（§4.5 / §7.5）

### Layer 1：YouTube topic 分佈（200 部全體）
| Topic | 命中 | 比例 |
|---|---:|---:|
| Health | 45 | 22.5% |
| Society | 39 | 19.5% |
| Lifestyle_(sociology) | 19 | 9.5% |
| Entertainment | 14 | 7.0% |
| Knowledge | 11 | 5.5% |
| Technology | 3 | 1.5% |
| Religion | 2 | 1.0% |
| Film / Politics | 2 / 2 | 1.0% |
| Food | 1 | 0.5% |

**驗證手動分類**：YouTube 系統將 PanSci 主要標為 **Health / Society / Knowledge / Lifestyle**，「Knowledge」直接對應使用者手動歸類的「科普」，但比例僅 5.5% — 顯示 YouTube 演算法更傾向以**主題領域**（健康、社會議題）而非「知識性／科普」這個 meta-label 來分類 PanSci。手動歸類「科普」與系統視角部分一致（Knowledge / Health / Society 確實均為知識性公共議題範疇），但 YouTube 並未把 PanSci 視為「教育類」（Education topic 0 命中）。

### Layer 2：規則字典命中率（Shorts，由高到低）
| Bucket | 命中率 |
|---|---:|
| has_問句 | **35.7%** |
| has_食物 | 3.9% |
| has_情緒詞 | 2.6% |
| has_教學教育 | 1.3% |
| has_挑戰對決 | 1.3% |
| has_開箱評測 | 0.65% |
| has_品牌推廣 | 0.65% |
| has_運動 | 0.65% |
| has_搞笑迷因 / has_互動誘導 | 0% |

**最大特色**：`has_問句` 命中 35.7%（長片更達 65.2%）— PanSci 的核心 hook 策略是「以問句製造好奇」（「為什麼…？」「什麼決定了…？」「真的…嗎？」）。注意 `has_教學教育` 僅 1.3%，因為字典只命中「教學/tutorial/怎麼」等明確教學動詞，未涵蓋 PanSci 慣用的問句式教學 → 印證計劃書 §C2 的「字典帶主觀偏誤」風險。

### Layer 3：TF-IDF Top 15 keywords（Shorts，n=154）
`什麼` / `科學家` / `突破` / `大腦` / `秘密` / `ai` / `泛科學` / `竟然` / `一直` / `決定` / `量子` / `容易` / `自己` / `直播` / `這個`

**詞群解讀**：「什麼／決定／秘密」為問句 hook；「科學家／量子／大腦／AI／泛科學」為科學主題詞；「突破／竟然」為情緒/驚奇詞。整體呈現「**好奇驅動 + 前沿研究 + 適度誇張**」三層次內容指紋。

### Shorts vs 長片 內容指紋對比
| 維度 | Shorts | Long |
|---|---|---|
| 標題長度（CJK 字）mean | 10.6 | **25.4**（2.4 倍） |
| 標題英數 mean | 0.11 | **1.50**（13 倍） |
| has_問句 命中率 | 35.7% | **65.2%** |
| TF-IDF top 詞 | 什麼、科學家、突破、秘密 | news、泛科學、什麼、ai、ft（合作）、新聞 |
| topic 缺值率 | 26.6% | **84.8%** |

**洞察**：
1. Shorts 標題顯著比長片短一倍以上（10.6 vs 25.4 CJK 字），符合 Shorts 平台特性
2. 長片更頻繁使用「ft（feat 合作）／news／半小時泛／新聞」等系列節目/品牌標籤，Shorts 則更純粹以**單一好奇點**為標題
3. 長片的 topic_categories 缺值率高達 85% — YouTube 對 PanSci 長片幾乎不主動貼 topic 標
4. Shorts 用「什麼」開頭的問句頻率非常高，是 PanSci Shorts 的招牌句型

### §7.5 內容標籤與觀看數的關係（卡方 / Logistic）
top_quartile 門檻 view_count ≥ 228,596。多數 has_* 標籤樣本太集中（命中 0 或全 1）導致檢定無效；可檢驗者：
- `has_食物`：chi2 = 0.00，p = 0.985 ns
- `has_問句`：chi2 = 0.05，p = 0.825 ns

Logistic 因設計矩陣 singular（多 has_* 全 0）而跳過。**結論**：在單頻道 154 個 Shorts 樣本上，無法用內容標籤顯著區分高/低觀看；標題詞彙策略對「能否進 top quartile」沒有可測量影響 — PanSci 內部變異主要由話題本身（而非標題包裝）決定。

## 迴歸結果（OLS model1，無 channel dummy）

公式：`view_count ~ duration_sec + title_length + tag_count`（features 已 z-score）

| 參數 | coef | p |
|---|---:|---:|
| Intercept | 184,500 | < 0.001 |
| duration_sec | +7,334 | 0.666 |
| title_length | −2,091 | 0.903 |
| tag_count | −12,490 | 0.430 |

- **R² = 0.006，Adj R² = −0.013**
- F-statistic p = 0.808（整體模型不顯著）
- VIF 均 < 1.2（無共線性）

**結論**：在 PanSci Shorts 上，duration / title_length / tag_count 三個結構性變數**完全不能預測**觀看數。`view_count` 的變異主要由其他未觀測因素（影片題目本身、演算法推送、首頁熱度、外部曝光）解釋。

## 對應企劃書研究問題

| RQ | 結論 |
|---|---|
| **RQ1（標題長度）** | 與 view r = −0.033 ns；ANOVA p = 0.764 ns。**否定**：標題長度對 PanSci Shorts 觀看無影響。 |
| **RQ3（標籤數量）** | 與 view r = −0.068 ns；ANOVA 0 vs 1 tag p = 0.405 ns。**否定**。 |
| **RQ6（影片長度）** | duration 與 view r = +0.045 ns；Shorts vs 長片 view p = 0.098（邊界 ns）／like p = 0.013 *。**部分支持**：Shorts 平均按讚顯著高於長片。 |
| **RQ9（發布時間）** | 發布時段 p = 0.811 ns；星期 p = 0.926 ns。**否定**。但時間分段（早/中/近）ANOVA p = 0.013 * → **支持**：PanSci 觀看在不同時期確有變化（演算法或內容週期效應）。 |
| RQ2/4/5（標題詞、標籤類型、一致性） | 由內容貼標回答：問句型 hook 是 PanSci 主軸（35.7% 命中），但問句出現與否未顯著影響觀看 → 一致性策略已成形，內部變異由話題決定。 |

## 單頻道分析的限制
1. **無法做頻道間比較**：無 channel dummy；無法分離「品牌效應」與「內容效應」
2. **發布時間策略單一**：PanSci 幾乎全部排在固定時段發片，使「發布時段」變數失去檢定價值
3. **長片 n=46 偏少**：Shorts vs 長片檢定有效但 statistical power 受限
4. **樣本時期效應未控制**：CSV 為 2026-05 抓取的近 200 部上傳，季節/節日/議題熱度未控
5. **跨類別比較留給 Phase 3**：PanSci 與「介紹食物」「Kpop」等娛樂類的觀看分佈差異將在 `analysis/_crosscat/` 處理
