# 遊戲 — 內容指紋

> Source: `data/processed/channel_videos_20260527-064831.csv`（Shorts 308 部）
> 字典版本：v1.0（`analysis/_templates/content_keywords.yaml`）

---

## 卡片 1：camman18（@camman18）

- **n_shorts**：198  
- **訂閱數**：10.8M  
- **頻道總觀看**：18.0B  

### YouTube topics（Layer 1，Top 5）
| topic | 比例 |
|---|---|
| Video_game_culture | 100.0% |
| Role-playing_video_game | 93.4% |
| Action-adventure_game | 84.3% |
| Action_game | 54.0% |
| Strategy_video_game | 2.5% |

### 規則字典命中率（Layer 2，Top 5）
| bucket | rate |
|---|---|
| has_教學教育 | 100.0% |
| has_挑戰對決 | 100.0% |
| has_問句 | 14.6% |
| has_搞笑迷因 | 2.0% |
| has_開箱評測 | 0.5% |

注：教學/挑戰 100% 為「tag 重複」偽命中（每片都有 minecraft + how to 類 tag），非內容真的全為教學。

### TF-IDF Top 15 keywords（Layer 3）
minecraft / the / to / in / how / is / new / you / and / use / this / of / what / it / have

### 標題長度（mean）
- CJK：0 字元 / EN：6.98 詞 / 總長：42.8

### 標籤類型粗分（每片平均 29.0 個 tag）
- 主題標籤：minecraft, minecraft shorts, gaming, minecraft mods, minecraft 1.21, minecraft pe
- 系列／作者標籤：camman18, camman18 minecraft（自家 brand）
- 版本／平台：minecraft bedrock, minecraft survival
- 規模標籤：minecraft tips, minecraft tutorial（教學語料）
- 高度重複：tag list 在大多數片完全一致，更像 SEO 模板

---

## 卡片 2：GothamChess（@gothamchess）

- **n_shorts**：110  
- **訂閱數**：7.58M  
- **頻道總觀看**：5.18B  

### YouTube topics（Layer 1，Top 5）
| topic | 比例 |
|---|---|
| Video_game_culture | 57.3% |
| Entertainment | 20.9% |
| Hobby | 17.3% |
| Lifestyle | 16.4% |
| Strategy_video_game | 6.4% |

### 規則字典命中率（Layer 2，Top 5）
| bucket | rate |
|---|---|
| has_挑戰對決 | 7.3% |
| has_問句 | 3.6% |
| has_教學教育 | 0.0% |
| has_搞笑迷因 | 0.0% |
| has_情緒詞 | 0.9% |

### TF-IDF Top 15 keywords（Layer 3）
jynxzi / he / gotham / magnus / chess / vs / is / no / the / boom / levy / sindarov / do / why / this

### 標題長度（mean）
- CJK：0 字元 / EN：2.57 詞 / 總長：14.9

### 標籤類型粗分（每片平均 5.0 個 tag）
- 主題標籤：chess, gotham, levy, gothamchess
- 名人標籤：magnus (Carlsen)、sindarov、jynxzi（KOL 連動）
- 競技標籤：chess.com, blitz, bullet（賽制）
- 少量、精準：每片 tag 數中位數 ~5，遠少於 camman18

---

## 解讀：兩頻道內容差異最大的點

1. **遊戲類型完全不同**：camman18 = Minecraft（沙盒/RPG），GothamChess = 西洋棋（策略）。YouTube topics 重疊度幾乎為零。
2. **標題策略差 3 倍**：camman18 平均 6.98 個英文 word，GothamChess 2.57 個。camman18 寫「敘述句 + meme」（如 "there was never powdered snow"），GothamChess 寫「人名 + vs」這種對戰式短句。
3. **tag 數量差 6 倍**：camman18 平均 29 個 tag（重複度高、SEO 模板），GothamChess 平均 5 個 tag（精準連動）— 反映兩種完全不同的觸及策略。
4. **TF-IDF 完全不重疊**：camman18 = "minecraft" + 通用英文連接詞主導；GothamChess = 人名 (jynxzi, magnus, levy, sindarov) 主導 — 後者高度依賴跨 KOL 流量。
5. **平均觀看差 2.7 倍**（camman18 中位 5.4M vs GothamChess 中位 1.8M），即使 GothamChess 也是 7.58M 訂閱的超頂級頻道，但 Shorts 演算法在 Minecraft 領域有更強推送。
