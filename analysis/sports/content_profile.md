# 運動類 — 內容指紋

> 資料：`data/processed/channel_videos_20260527-064706.csv`（4 頻道，1,172 部 Shorts）
> 字典版本：v1.0（`analysis/_templates/content_keywords.yaml`）

---

## NBA（@NBA）

- **平均標題長度**：見 §findings.md（英文標題，分詞口徑差異需注意）
- **YouTube topics 前 3**：Sport (97.1%) / Basketball (95.6%) / Entertainment (1.8%)
- **規則字典命中率 Top 3**：has_運動 47.1% / has_挑戰對決 1.5% / has_教學教育 0.7%
- **TF-IDF Top 10 keywords**：the, in, to, game, wemby, nba, for, knicks, of, with
- **解讀**：NBA 官方頻道 — 英文 highlights 為主，多為球員姓名 + 比賽事件，幾乎無教學/挑戰類字典命中。has_運動 偏低（47%）非實質差異，而是中文字典未涵蓋英文體育詞。

---

## MLB（@MLB）

- **YouTube topics 前 3**：Baseball (95.6%) / Sport (94.1%) / Entertainment (2.2%)
- **規則字典命中率 Top 3**：has_運動 99.3% / has_挑戰對決 4.4% / has_問句 4.4%
- **TF-IDF Top 10 keywords**：the, mlb, to, highlights, in, his, homer, of, home, run
- **解讀**：MLB highlights 樣板化 — 「Shohei homers off」「Aaron Judge」這類人名+動作。內容單一度高，TF-IDF 也以英文虛詞為主導（the 0.61 → 文本標準化空間極窄）。

---

## 挖掘肌讲健身（@挖掘肌讲健身）

- **YouTube topics 前 3**：Physical_fitness (91.3%) / Lifestyle (88.9%) / Health (65.0%)
- **規則字典命中率 Top 3**：has_運動 100% / has_情緒詞 3.0% / has_問句 2.7%
- **TF-IDF Top 10 keywords**：训练, 健身, 水平, 力量, 肌肉, 什么, 身材, 健美, 动作, 轮子
- **解讀**：技術導向健身教學 — 「训练 / 力量 / 动作」是核心，反差元素少（搞笑迷因 0.3%）。「阿纳托利」「罗尼」（科尔曼 Ronnie Coleman）等 IP/名人入境 — 屬「健身知識 + 名人事件」型內容。

---

## 老赵闹健身（@老赵闹健身）

- **YouTube topics 前 3**：Lifestyle (90.3%) / Physical_fitness (85.8%) / Health (67.9%)
- **規則字典命中率 Top 3**：has_運動 100% / has_搞笑迷因 9.2% / has_情緒詞 3.8%
- **TF-IDF Top 10 keywords**：man, 健身, 猛男, 教练, 美女, 挑战, 网红, 训练, 肌肉, 顶级
- **解讀**：健身 + 整活混血路線 —「猛男 / 美女 / 网红」TF-IDF 高權重明顯偏娛樂；has_搞笑迷因 9.2% 是四頻道中唯一達兩位數。這也對應其 mean_view (117K) 顯著高於「挖掘肌讲健身」(15K)，雖訂閱數差異不大 (76.5K vs 49.5K)。

---

## 跨頻道觀察

1. **訂閱規模 ≠ 觀看表現**：MLB (7.2M) Shorts 觀看 mean 72K，與老赵闹健身 (76.5K subs, mean 117K) 反差 → 體育 highlights 在 Shorts 平台未獲爆發優勢。
2. **語言/內容類型撕裂**：NBA/MLB 英文 + 體育 highlights，中國健身頻道中文 + 教學/迷因 — 「sports」這個 preset 內部其實是兩個次類別。
3. **內容字典命中率與觀看的關聯**：本類別內，只有 has_運動 達顯著（χ² = 32.71），但這是頻道間 100% vs 47% 的二元分布偽相關，**非實質的內容效應**。
