# 介紹食物類 Shorts 分析發現

> 資料：data/processed/channel_videos_20260527-065126.csv（7 頻道，1,227 部影片）
> 範圍：Shorts 過濾條件 duration_sec ≤ 180，共 965 部 Shorts。

## 樣本概況
- 7 個頻道：@CatQTV (貓跪妃)、@HowHowEat (吃貨豪豪)、@jimmmypsd (智明)、@eating3922 (E ating)、@thisiskenyoung (This is Ken)、@hua_foodie (冬冬)、@umaguru-tokyo (うまぐるめ)
- Shorts 樣本：965 部
- 各頻道 Shorts 篇數：
  - 冬冬🌸生活美食日記💓：200
  - うまぐるめ【Japanese Food】：200
  - This is Ken：194
  - 智明 Jimmypsd：165
  - 貓跪妃：109
  - E ating：62
  - 吃貨豪豪HowHowEat：35

## 關鍵統計
| 指標 | mean | median | std |
|---|---:|---:|---:|
| view_count | 514,373 | 120,935 | 1,739,091 |
| like_count | 12,557 | 2,000 | 36,596 |
| comment_count | 116.9 | 30 | 243.9 |
| duration_sec | 45.9 | 48 | 20.4 |
| title_length | 36.6 | 34 | 21.2 |
| tag_count | 0.0 | 0 | 0.2 |

→ **食物類 Shorts 幾乎不打 tags**（mean=0.0, std=0.2）— 與運動類 mean=8.3 形成鮮明對比。

頻道級摘要：
| 頻道 | n_shorts | mean_view | median_view | mean_like | mean_comment |
|---|---:|---:|---:|---:|---:|
| E ating | 62 | 40,465 | 5,198 | 349 | 13.3 |
| This is Ken | 194 | 512,916 | 172,559 | 14,452 | 125 |
| うまぐるめ【Japanese Food】 | 200 | 978,641 | 254,142 | 20,884 | 119 |
| 冬冬🌸生活美食日記💓 | 200 | 71,188 | 22,163 | 569.7 | 17.1 |
| 吃貨豪豪HowHowEat | 35 | 356,637 | 289,561 | 7,952 | 260 |
| 智明 Jimmypsd | 165 | 1,007,727 | 877,319 | 28,501 | 296 |
| 貓跪妃 | 109 | 51,670 | 23,884 | 475.6 | 22.6 |

## 頻道間 ANOVA
- view_count: F=9.31, p=6.07e-10 → 顯著（但 F 值是三類別中最低）
- 觀看排序：智明 Jimmypsd > うまぐるめ > This is Ken > 吃貨豪豪 > 冬冬 > 貓跪妃 > E ating

## 標題長度分組 ANOVA
- 短:n=328 mean=222,942；中:n=320 mean=683,970；長:n=317 mean=644,713
- F=7.11, p=8.64e-4 → 顯著；中等長度最佳

## 標籤數量分組 ANOVA
- 無標籤:n=962 mean=515,889；1-3:n=3 mean=28,143
- F=0.24, p=0.628 → 不顯著（樣本極度失衡，幾乎所有 Shorts 都無 tag）

## 內容貼標發現
### Layer 1 — YouTube topic 主導
- 全 7 頻道皆以 Lifestyle (sociology) > 90% 與 Food (15–100%) 為主導；差異在 Tourism / Pet / Hobby 上：
  - This is Ken: Food 77% / Lifestyle 97% / Tourism 33% （日本/海外旅遊類）
  - 智明 Jimmypsd: Food 95% / Lifestyle 99% / Tourism 15%
  - 貓跪妃: Food 97% / Lifestyle 98% / Pet 3.7%
  - 其他頻道 Tourism < 3%

### Layer 2 — 規則字典命中率 Top 3
| 頻道 | has_食物 | has_問句 | has_情緒詞 |
|---|---:|---:|---:|
| E ating | 95.2% | 4.8% | 3.2% |
| This is Ken | 53.6% | 21.1% | 3.6% |
| うまぐるめ | 1.5% | 0% | 4.5% |
| 冬冬 | 20.5% | 9.0% | 4.0% |
| 吃貨豪豪 | 82.9% | 45.7% | 0% |
| 智明 Jimmypsd | 87.3% | **93.9%** | 0.6% |
| 貓跪妃 | 98.2% | 6.4% | 0.9% |

→ **智明 Jimmypsd has_問句 93.9%** 對應其平均觀看 100 萬（類別最高）— 「（地名）一天要花多少」標題公式。

### Layer 3 — TF-IDF Top 5
- E ating: 台中, 潤餅, 豆花, 飲料, 豆腐 （台中在地小吃）
- This is Ken: 東京, 日本, 好吃, in, 就是 （日本旅遊美食）
- うまぐるめ: 一杯, 旨味, 中華, 王子, 屋台 （東京拉麵屋台）
- 冬冬: 完售, 不到, 草莓, 臭豆腐, 可以 （限時限量在地）
- 吃貨豪豪: 免費, 大胃, 好吃, 漢堡, 麥當勞 （連鎖速食/挑戰）
- 智明 Jimmypsd: 要花, 多少, 一天, 智明, 彰化 （費用挑戰格式）
- 貓跪妃: 隱藏, 知道, 這間, 人才, 只要 （隱藏美食推薦）

### 內容標籤與高觀看（卡方 + Logistic）
- has_問句 χ²=176.44, p=2.91e-40 *** ← **三類別中最強的內容標籤效應**
- has_食物 χ²=23.12, p=1.52e-6 ***
- Logistic 顯著項：has_問句 β=+2.12, p<0.001 → has_問句=1 的 Shorts 進入 top quartile 的勝算是無問句的 8.3 倍

## 迴歸結果
| 模型 | R² | Adj R² |
|---|---:|---:|
| M1（duration + title_length + tag_count） | 0.030 | 0.027 |
| M2（+ C(channel_title)） | 0.066 | 0.057 |

- ΔR² = +0.036（中等強度頻道效應）
- 顯著預測子（M1）：duration_sec (+, β=+239K, p<0.001)、title_length (+, β=+172K, p=0.002)
- 顯著預測子（M2）：title_length (+, β=+255K, p=0.002)、多個頻道 dummy 顯著
- VIF：duration_sec=1.006, title_length=1.004, tag_count=1.005 → 完全無共線性

## 對應企劃書研究問題
- RQ1 標題長度：顯著（中等最佳）
- RQ3 標籤數量：不顯著（樣本失衡，幾乎全為 0）
- RQ6 影片長度：r=+0.141, p<0.001 → 較長 Shorts 觀看略多（與運動類相反）
- RQ7 訂閱數：未直接比較（需 channels.csv 對照）

## 限制與註記
- 樣本不足頻道：吃貨豪豪 HowHowEat (n=35) 接近門檻；E ating (n=62) 因影片更新慢但仍可用
- 字元數計算偏誤：中日英混雜（うまぐるめ 為日文）對 title_length 不公；建議補 cjk-only 比較
- has_食物 字典覆蓋不足：うまぐるめ 全日文標題 has_食物 僅 1.5%（漢字「食」未在日文標題出現），需擴充日文字典
- tag_count 幾乎全為 0 → 此類別 RQ3 無實際分析價值
- 觀看分配極偏（std/mean=3.4），ANOVA 結論需以非參數法復驗
