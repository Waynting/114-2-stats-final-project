# Kpop — 內容指紋

> Source: `data/processed/channel_videos_20260527-065002.csv`（Shorts 298 部）
> 字典版本：v1.0（`analysis/_templates/content_keywords.yaml`）
> 註：企劃書原列 Lablodol，因無 @handle 本次未抓到；待後續手動補 channel_id

---

## 卡片 1：K-潮流（@k-chaoliu）

- **n_shorts**：200  
- **訂閱數**：76,600  
- **頻道總觀看**：459M  

### YouTube topics（Layer 1，Top 5）
| topic | 比例 |
|---|---|
| Entertainment | 69.0% |
| Lifestyle | 13.5% |
| Humour | 6.0% |
| Music | 3.5% |
| Music_of_Asia | 3.5% |

### 規則字典命中率（Layer 2，Top 5）
| bucket | rate |
|---|---|
| has_教學教育 | 7.0% |
| has_搞笑迷因 | 4.0% |
| has_互動誘導 | 3.0% |
| has_情緒詞 | 2.0% |
| has_食物 | 2.0% |

### TF-IDF Top 15 keywords（Layer 3）
xd / karina / 潮流 / 真的 / 自己 / ahyeon / rora / 看到 / 怎麼 / chiquita / 員瑛 / 忍不住 / aespa / 立刻 / 姐姐

### 標題長度（mean）
- CJK：16.5 字元 / EN：4.9 詞 / 總長：51.2

### 標籤類型粗分（每片平均 0.4 個 tag）
- 主題標籤：少（多寫在描述非 metadata tag）
- 偶像/團體標籤：karina, aespa, 員瑛, ahyeon, rora, chiquita（混入英文+繁中藝名）
- 評論／情緒詞：忍不住、立刻、姐姐（評論者角度）
- emoji：偶爾在標題

---

## 卡片 2：kukuo 쿠쿠（@kukuo1019）

- **n_shorts**：98  
- **訂閱數**：5,290  
- **頻道總觀看**：22.6M  

### YouTube topics（Layer 1，Top 5）
| topic | 比例 |
|---|---|
| Entertainment | 81.6% |
| Music_of_Asia | 4.1% |
| Music | 4.1% |
| Television_program | 4.1% |
| Lifestyle | 3.1% |

### 規則字典命中率（Layer 2，Top 5）
| bucket | rate |
|---|---|
| has_問句 | 9.2% |
| has_食物 | 5.1% |
| has_情緒詞 | 5.1% |
| has_搞笑迷因 | 2.0% |
| has_挑戰對決 | 1.0% |

### TF-IDF Top 15 keywords（Layer 3）
haewon / bae / yuna / 真的 / lily / 表情 / 彩領 / nmixx / 真心 / jiwoo / karina / kyujin / 捉弄 / love / 完全

### 標題長度（mean）
- CJK：9.7 字元 / EN：1.37 詞 / 總長：18.7

### 標籤類型粗分（每片平均 3.9 個 tag）
- 偶像/團體標籤（主導）：Itzy, illit, NMIXX, Aespa, Babymonster；個人 haewon, yuna, lily, 彩領, jiwoo（中英混合）
- 主題標籤：少（純偶像名稱為主）
- 品牌標籤：無
- emoji：少

---

## 解讀：兩頻道內容差異最大的點

1. **標題長度差 2.7 倍**：K-潮流 51.2 字 vs kukuo 18.7 字。K-潮流寫「評論句 + 偶像名」（如「Karina 真的忍不住要笑」），kukuo 純「人名+一句動作」（如「Yeji 一句話馬上引起抗議」）。
2. **訂閱反向關係**：K-潮流訂閱多 14 倍，但 Shorts 平均觀看 kukuo 是 K-潮流的 2.3 倍 — Shorts 演算法不吃訂閱基礎，純看內容黏著度。
3. **tag 策略相反**：kukuo 每片寫 3.9 個 tag（純偶像名），K-潮流 0.4 個 tag。kukuo 用 metadata tag 補強搜尋觸及。
4. **詞庫關注的偶像不同**：K-潮流的高權重偶像是 karina, aespa, 員瑛, ahyeon, rora；kukuo 是 haewon, yuna, lily, 彩領, jiwoo — 雖然兩頻道都做「偶像 reaction」但選材／粉絲取向不同。
5. **規則字典覆蓋不足**：兩頻道命中率 Top bucket 也不超過 10%，下一版字典需增 Kpop 專屬 buckets（偶像/直拍/演唱會/應援/MV）。
