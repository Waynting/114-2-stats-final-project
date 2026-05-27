# Notebook 模板使用說明

本資料夾提供 3 份分析模板與一個共用內容貼標模組，覆蓋計畫書定義的「single / two / multi 頻道」三種類別規模。

## 三個模板對應表

| 模板 | 適用頻道數 | 對應類別 | 核心統計檢定 |
|---|---|---|---|
| `template_single.ipynb` | 1 | 科普（PanSci） | 時間分段 ANOVA + Shorts vs 長片 Mann-Whitney（取代頻道 ANOVA） |
| `template_two.ipynb` | 2 | 遊戲 / 籃球幹片 / 籃球網紅 / Kpop | Mann-Whitney U + OLS 含 0/1 channel dummy |
| `template_multi.ipynb` | 3+ | 運動 / 時事 / 介紹食物 / 餐廳推廣 | ANOVA + OLS 含 C(channel_title) dummy；title_length 用 `pd.qcut` 動態分位 |

每份模板都已內建：
- §4.5 **內容貼標**（呼叫 `content_labeling.py` 的 Layer 1-3：YouTube topic、規則式關鍵字、jieba+TF-IDF）
- §7.5 **內容標籤與觀看數的關係**（卡方檢定每個 `has_<bucket>` vs top-quartile，logistic regression）

## 改用流程：複製到類別資料夾後只改 3 個常數

每個模板第一個 code cell（`## 0. 參數`）長這樣：

```python
CSV_TIMESTAMP = "20260526-030644"   # 改這裡切換不同類別的資料
TARGET_CHANNELS = None               # None = 全部；或填 list 過濾特定頻道
CATEGORY_NAME = "範例類別"            # 用於圖表標題
```

工作流程：
1. 跑完 `python main.py channel-compare --preset <cat>`，記下新生成 CSV 的時間戳
2. 將時間戳填入該類別資料夾的 `DATA_REF.md`
3. 複製對應模板：`cp _templates/template_<size>.ipynb <cat>/analysis.ipynb`
4. 開 notebook，把 `CSV_TIMESTAMP` / `CATEGORY_NAME` 改成該類別的值
5. （可選）若 preset CSV 含其他類別，用 `TARGET_CHANNELS = ['@xxx', '@yyy']` 過濾
6. 從上到下執行所有 cell

## 路徑慣例

模板假設放置位置為 `analysis/<category>/analysis.ipynb`，因此路徑回退兩層：
```python
pd.read_csv(f'../../data/processed/channel_videos_{CSV_TIMESTAMP}.csv')
```
且把 `analysis/_templates/` 動態加入 `sys.path` 才能 `import content_labeling`。

## 內容貼標模組

- `content_keywords.yaml`：Layer 2 規則式關鍵字字典 v1.0（10 個 bucket，可改）
- `content_labeling.py`：提供 `explode_topic_categories()` / `apply_keyword_labels()` / `tokenize_zh()` / `tfidf_top_keywords_by_channel()` / `channel_content_profile()`

要關閉 §4.5 / §7.5 兩個 cell，直接刪除即可（其餘 cell 不依賴 `df_lab`）。
