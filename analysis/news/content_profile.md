# 時事類 — 內容指紋

> 資料：data/processed/channel_videos_20260527-065044.csv（5 頻道，964 部 Shorts）
> 字典版本：v1.0

---

## Johnny Harris (@johnnyharris)
- YouTube topics 前 3：Society 57% / Politics 37% / Knowledge 15%
- 規則字典 Top 3：has_問句 19.8% / has_教學教育 0.9% / has_挑戰對決 0.9%
- TF-IDF Top 10：the, why, is, how, are, to, in, us, this, israel
- 解讀：英文國際時事「why / how」提問型；高權重詞為地緣熱點（israel, russia, china, war）。

## Vox (@Vox)
- YouTube topics 前 3：Society 57% / Politics 48% / Lifestyle 17%
- 規則字典 Top 3：has_問句 26.1% / has_教學教育 3.3% / has_挑戰對決 0.9%
- TF-IDF Top 10：the, is, to, why, how, in, are, trump, of, for
- 解讀：與 Johnny Harris 同類型但更政治導向（trump, iran 入榜）；has_問句 較高。

## 志祺七七 (@shasha77)
- YouTube topics 前 3：Entertainment 79% / Lifestyle 18% / Pet 3.2%
- 規則字典 Top 3：has_問句 55.9% / has_食物 3.6% / has_情緒詞 2.4%
- TF-IDF Top 10：志祺, 七七, shorts, 日本, 台灣, 中國, ai, 美國, 男子, 怎麼
- 解讀：時事評論「shorts」化最徹底（頻道名/品牌字佔據 TF-IDF Top 3）；has_問句 55.9% 全類別最高。

## 喵耳電波 (@SubsOverflow)
- YouTube topics 前 3：Entertainment 52% / Video_game_culture 23% / Society 15%
- 規則字典 Top 3：has_搞笑迷因 100% / has_問句 29.7% / has_挑戰對決 5.2%
- TF-IDF Top 10：直接, asmongold, asmon, 結果, vs, 女生, 男人, 美國, 赤血, 只是
- 解讀：實為「實況翻譯 / 電玩政治」混血；has_搞笑迷因 100% 是字典觸發（頻道含「迷因」字），需注意該命中率非實質內容指紋。

## Real Fake (@RealFake)
- YouTube topics 前 3：全為空（topic_categories 缺失）
- 規則字典 Top 3：has_* 全為 0%
- TF-IDF Top 5：tedua, per, intro, izi, charles
- 解讀：n=8 樣本過少；TF-IDF 顯示為義大利語音樂/嘻哈內容，與「時事」主題不符 — preset 內混入了異類頻道，建議下次抓取時剔除或重新分類。

---

## 跨頻道觀察
1. 5 頻道分屬「英文長片頻道做 Shorts」(Johnny Harris, Vox)、「中文時事評論」(志祺七七)、「實況/電玩政論」(喵耳電波)、「義大利音樂」(Real Fake) — preset 異質性最高。
2. Johnny Harris 平均觀看 173 萬 vs Real Fake 961 = 1,800 倍差距，是 channel dummy R² 暴增至 0.283 的主因。
3. has_問句 與「中文時事評論」強相關（志祺七七 55.9%）；Logistic 顯示在 top quartile 中 has_問句 反為負（被英文頻道稀釋）。
