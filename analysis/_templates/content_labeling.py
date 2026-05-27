"""Layer 1-3 內容貼標共用模組

Layer 1: parse YouTube topic_categories
Layer 2: rule-based keyword dictionary
Layer 3: TF-IDF top keywords per channel
"""
from pathlib import Path
import re
import yaml
import pandas as pd
from collections import Counter

try:
    import jieba
    _HAS_JIEBA = True
except ImportError:
    _HAS_JIEBA = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    _HAS_SKLEARN = True
except ImportError:
    _HAS_SKLEARN = False


_KEYWORDS_YAML = Path(__file__).parent / "content_keywords.yaml"


def load_keyword_dict(path=None):
    p = Path(path) if path else _KEYWORDS_YAML
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["buckets"]


def parse_topic_categories(s):
    """從 'https://en.wikipedia.org/wiki/Food|https://en.wikipedia.org/wiki/Entertainment'
    抽出 ['Food', 'Entertainment']"""
    if pd.isna(s) or not s:
        return []
    return [url.rsplit("/", 1)[-1] for url in str(s).split("|") if url]


def explode_topic_categories(df, col="topic_categories"):
    """回傳 (df with topics_list 欄, topic 計數 series)"""
    df = df.copy()
    df["topics_list"] = df[col].apply(parse_topic_categories)
    all_topics = [t for ts in df["topics_list"] for t in ts]
    return df, pd.Series(Counter(all_topics)).sort_values(ascending=False)


def topic_distribution_by_channel(df):
    """每個 channel 的 topic 命中比例（DataFrame: rows=channel, cols=topic）"""
    out = {}
    for ch, g in df.groupby("channel_title"):
        topics = [t for ts in g["topics_list"] for t in ts]
        c = Counter(topics)
        total = len(g)
        out[ch] = {t: c[t] / total for t in c}
    return pd.DataFrame(out).T.fillna(0)


def apply_keyword_labels(df, text_cols=("title",), buckets=None):
    """為每個 bucket 加一個 has_<bucket> 0/1 欄位"""
    if buckets is None:
        buckets = load_keyword_dict()
    df = df.copy()
    combined = df[list(text_cols)].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
    for name, kws in buckets.items():
        pattern = "|".join(re.escape(kw.lower()) for kw in kws)
        df[f"has_{name}"] = combined.str.contains(pattern, regex=True).astype(int)
    return df


_STOPWORDS = set("""
的 了 是 在 我 你 他 她 它 們 嗎 啊 也 都 就 不 沒 有 一 個 這 那 和 與 及 或 但 而 為
""".split())


def tokenize_zh(text):
    if pd.isna(text) or not text:
        return []
    text = re.sub(r"#\S+", "", str(text))
    text = re.sub(r"[^\w\s一-鿿]", " ", text)
    if _HAS_JIEBA:
        words = jieba.lcut(text)
    else:
        words = re.findall(r"[一-鿿]+|[A-Za-z]+", text)
    return [w for w in words if w.strip() and w not in _STOPWORDS and len(w) > 1]


def tfidf_top_keywords_by_channel(df, n=15, text_col="title"):
    if not _HAS_SKLEARN:
        raise RuntimeError("sklearn not installed")
    groups = df.groupby("channel_title")[text_col].apply(
        lambda s: " ".join(" ".join(tokenize_zh(t)) for t in s.dropna())
    )
    # 過濾掉空字串文檔
    groups = groups[groups.str.strip() != ""]
    if len(groups) == 0:
        return {}
    vec = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", max_features=2000)
    mat = vec.fit_transform(groups.values)
    feat = vec.get_feature_names_out()
    out = {}
    for i, ch in enumerate(groups.index):
        row = mat[i].toarray().ravel()
        top_idx = row.argsort()[::-1][:n]
        out[ch] = [(feat[j], float(row[j])) for j in top_idx if row[j] > 0]
    return out


def channel_content_profile(df):
    """回傳每個頻道的綜合 content profile dict"""
    df_with_topics, _ = explode_topic_categories(df)
    df_labeled = apply_keyword_labels(df_with_topics, text_cols=("title", "tags"))
    topic_dist = topic_distribution_by_channel(df_with_topics)
    try:
        tfidf_top = tfidf_top_keywords_by_channel(df_labeled, n=15)
    except RuntimeError:
        tfidf_top = {}
    buckets = load_keyword_dict()
    label_cols = [f"has_{b}" for b in buckets]
    label_rates = df_labeled.groupby("channel_title")[label_cols].mean()
    return {
        "topic_dist": topic_dist,
        "label_rates": label_rates,
        "tfidf_top": tfidf_top,
    }
