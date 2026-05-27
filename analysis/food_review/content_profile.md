# 介紹食物類 — 內容指紋

> 資料：data/processed/channel_videos_20260527-065126.csv（7 頻道,965 部 Shorts）
> 字典版本：v1.0

---

## E ating (@eating3922)
- 平均 view: 40,465 / 標題長度: 中等
- YouTube topics 前 3：Food 96.8% / Lifestyle 96.8% / Tourism 1.6%
- 規則字典 Top 3：has_食物 95.2% / has_問句 4.8% / has_情緒詞 3.2%
- TF-IDF Top 10：台中, 潤餅, 豆花, 飲料, 豆腐, 早餐, 草莓, 冰沙, 魚燒, 一碗
- 解讀：台中在地小吃巡禮；極窄地域聚焦。

## This is Ken (@thisiskenyoung)
- 平均 view: 512,916
- YouTube topics 前 3：Lifestyle 97.4% / Food 77.3% / Tourism 33.0%
- 規則字典 Top 3：has_食物 53.6% / has_問句 21.1% / has_情緒詞 3.6%
- TF-IDF Top 10：東京, 日本, 好吃, in, 就是, 京都, 台灣, 機場, 真的, 美食
- 解讀：日本旅遊美食 vlog；中英混雜、地名為主。

## うまぐるめ【Japanese Food】(@umaguru-tokyo)
- 平均 view: 978,641（類別第二高）
- YouTube topics 前 3：Food 100% / Lifestyle 100% / Pet 0.5%
- 規則字典 Top 3：has_情緒詞 4.5% / has_食物 1.5% / has_問句 0%
- TF-IDF Top 10：一杯, 旨味, 中華, 王子, 屋台, 本店, 濃厚, 自家, 魚介, 出汁
- 解讀：純日文標題；字典中文設計導致 has_食物 偽低；TF-IDF 揭示為東京拉麵/屋台類 — 「旨味 / 出汁 / 濃厚豚」拉麵術語密集。

## 冬冬🌸生活美食日記💓 (@hua_foodie)
- 平均 view: 71,188
- YouTube topics 前 3：Lifestyle 98% / Food 89.5% / Tourism 2%
- 規則字典 Top 3：has_食物 20.5% / has_問句 9.0% / has_情緒詞 4.0%
- TF-IDF Top 10：完售, 不到, 草莓, 臭豆腐, 可以, 好吃, 必買, 直接, 自己, 地人
- 解讀：限時/限量在地（「完售 / 必買 / 不到」緊迫感詞彙）；emoji 在頻道名上 → 視覺品牌化。

## 吃貨豪豪HowHowEat (@HowHowEat)
- 平均 view: 356,637 / n=35（接近樣本門檻）
- YouTube topics 前 3：Lifestyle 94.3% / Food 85.7% / Hobby 2.9%
- 規則字典 Top 3：has_食物 82.9% / has_問句 45.7% / has_挑戰對決 8.6%
- TF-IDF Top 10：免費, 大胃, 好吃, 漢堡, 麥當勞, 中國大陸, 挑戰, 餐點, 推出, 壽司
- 解讀：連鎖速食/大胃挑戰；has_挑戰對決 8.6% 是類別內最高 — 與「挑戰 / 大胃」TF-IDF 高度一致。

## 智明 Jimmypsd (@jimmmypsd)
- 平均 view: 1,007,727（類別第一）
- YouTube topics 前 3：Lifestyle 98.8% / Food 94.5% / Tourism 14.5%
- 規則字典 Top 3：has_問句 **93.9%** / has_食物 87.3% / has_挑戰對決 1.2%
- TF-IDF Top 10：要花, 多少, 一天, 智明, 彰化, 夜市, 台南, 美食, 去一趟, 苗栗
- 解讀：標題公式高度規範化 —「（地名）一天要花多少」格式；has_問句 93.9% 全類別最高，對應其類別第一的平均觀看 — **問句格式 × 高觀看的最佳示例**。

## 貓跪妃 (@CatQTV)
- 平均 view: 51,670
- YouTube topics 前 3：Lifestyle 98.2% / Food 97.2% / Pet 3.7%
- 規則字典 Top 3：has_食物 98.2% / has_問句 6.4% / has_搞笑迷因 0.9%
- TF-IDF Top 10：隱藏, 知道, 這間, 人才, 只要, 深夜, 這家, 美食, 美味, 排隊
- 解讀：隱藏版美食推薦（「隱藏 / 知道 / 這家」探秘語感）；雖 has_食物 命中最高但平均觀看僅 5 萬 — 字典命中不代表流量。

---

## 跨頻道觀察
1. **同主題、不同敘事 → 觀看差距 25 倍**：智明 Jimmypsd (100 萬) vs E ating (4 萬)，兩者 Food + Lifestyle 命中皆 > 95% — 差異不在主題，而在 has_問句 (93.9% vs 4.8%) 與標題公式化程度。
2. **has_問句 在此類別最具預測力**：χ²=176.44, p=2.91e-40，Logistic β=+2.12 → 問句格式 Shorts 進入 top quartile 機率是其他的 8.3 倍。
3. **字典侷限**：うまぐるめ 全日文，has_食物 僅 1.5% 但 100% Layer-1 Food — Layer 1（YouTube 官方標籤）對非中文內容更可靠，建議報告中以 Layer 1 為主、Layer 2 為輔。
4. **tag_count 在本類別失去信號**：962/965 Shorts tag 為 0，RQ3 在 food_review 等同於 nullified。
