# 籃球幹片 — 內容指紋

> Source: `data/processed/channel_videos_20260527-064904.csv`（Shorts 304 部）
> 字典版本：v1.0（`analysis/_templates/content_keywords.yaml`）

---

## 卡片 1：俊鸿TV（@junhongtv）

- **n_shorts**：164  
- **訂閱數**：69,300  
- **頻道總觀看**：177M  

### YouTube topics（Layer 1，Top 5）
| topic | 比例 |
|---|---|
| Basketball | 90.2% |
| Sport | 86.6% |
| Lifestyle | 7.9% |
| Entertainment | 4.9% |
| Humour | 4.3% |

### 規則字典命中率（Layer 2，Top 5）
| bucket | rate |
|---|---|
| has_運動 | 96.3% |
| has_搞笑迷因 | 65.2% |
| has_教學教育 | 12.2% |
| has_問句 | 10.4% |
| has_挑戰對決 | 4.9% |

### TF-IDF Top 15 keywords（Layer 3）
回顧 / 往期 / 野球 / 球場 / 籃球 / 一個 / 隊友 / 打球 / 真正 / 兄弟 / 自己 / 時刻 / 高手 / 有料 / 教學

### 標題長度（mean）
- CJK：35.1 字元 / EN：1.07 詞 / 總長：62.3

### 標籤類型粗分（每片平均 28.5 個 tag）
- 主題標籤：籃球、野球、籃球場段子、剧情演绎（出現於 90%+ 影片）
- 品牌標籤：曾舔舔、俊鸿TV、曾教練（自家系列名稱）
- 系列標籤：王師傅、阿猿、新生杯（影片系列）
- emoji：少（主要在標題不在 tag）

---

## 卡片 2：卷毛懂个球（@juanmaodonggeqiu）

- **n_shorts**：140  
- **訂閱數**：5,030  
- **頻道總觀看**：7.5M  

### YouTube topics（Layer 1，Top 5）
| topic | 比例 |
|---|---|
| Basketball | 67.9% |
| Sport | 40.7% |
| Humour | 30.0% |
| Entertainment | 27.9% |
| Lifestyle | 25.7% |

### 規則字典命中率（Layer 2，Top 5）
| bucket | rate |
|---|---|
| has_搞笑迷因 | 67.9% |
| has_問句 | 13.6% |
| has_運動 | 5.0% |
| has_情緒詞 | 1.4% |
| has_教學教育 | 0.7% |

### TF-IDF Top 15 keywords（Layer 3）
兄弟 / 打球 / 就是 / 遇到 / 还是 / 身边 / 打篮球 / 你们 / 小时候 / 特别 / 我要 / 时候 / 这种 / 一个 / 篮球

### 標題長度（mean）
- CJK：21.5 字元 / EN：0.22 詞 / 總長：27.6

### 標籤類型粗分（每片平均 13.4 個 tag）
- 主題標籤：篮球、内容真实、剧情演绎、球场搞笑
- 品牌標籤：卷毛懂个球、卷毛、Mao Mao Basketball
- 情境標籤：真实篮球、篮球段子（更接近「人類觀察 vlog」而非「教學」）
- emoji：標題開頭有 🏀（描述區） 但 tag 中無

---

## 解讀：兩頻道內容差異最大的點

1. **YouTube 對頻道的歸類完全不同**：俊鸿TV 被歸 Basketball+Sport（90%/87%），卷毛懂个球被歸 Humour+Entertainment（30%/28%）。
2. **標題長度差 2 倍**：俊鸿TV 平均 62.3 字、卷毛 27.6 字 — 俊鸿TV 偏「描述型長標」（如「『高球商玩弄 06』高球商反制卑鄙對手 #籃球 #有料教學」），卷毛偏「短迷因句」。
3. **TF-IDF 區分清楚**：俊鸿TV 的 keyword 圍繞「教學/系列名/球場術語」（回顧、往期、野球、高手、教學）；卷毛則是「對話風口語」（兄弟、就是、遇到、还是、身边）。
4. **tag 數量差 2 倍**（28.5 vs 13.4），但內容貼標 `has_運動` 命中率差 19 倍（96% vs 5%）—— 俊鸿TV 寫實打標、卷毛標題故意不放關鍵字，依靠演算法推送風格詞。
