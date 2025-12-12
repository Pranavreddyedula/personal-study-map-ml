import pandas as pd
from dateutil import parser
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict
from .utils import logger

HASHTAG_RE = re.compile(r"#([A-Za-z0-9_]+)")

def load_social_json(data):
    """
    Accepts either a dict (already parsed) or path to a json file.
    Returns a pandas DataFrame with at least 'text' and optionally 'timestamp'.
    """
    if isinstance(data, dict):
        items = data.get("activities", [])
    else:
        import json
        with open(data, "r", encoding="utf-8") as f:
            items = json.load(f).get("activities", [])
    df = pd.DataFrame(items)
    if df.empty:
        logger.warning("No activities found in provided data.")
        return df
    # Normalize columns
    if "text" not in df.columns:
        df["text"] = df.get("content", "")
    # parse timestamps where possible
    if "timestamp" in df.columns:
        def _parse_ts(x):
            try:
                return parser.parse(x)
            except Exception:
                return pd.NaT
        df["timestamp"] = df["timestamp"].apply(_parse_ts)
    return df

def extract_hashtags(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    return [m.group(1).lower() for m in HASHTAG_RE.finditer(text)]

def extract_topics_by_hashtag(df: pd.DataFrame) -> Dict[str,int]:
    """Return dict of hashtag -> count"""
    topics = {}
    for t in df.get("text", "").fillna("").tolist():
        for tag in extract_hashtags(t):
            topics[tag] = topics.get(tag, 0) + 1
    return topics

def extract_top_terms_tfidf(df: pd.DataFrame, top_n=15) -> List[str]:
    """
    Use TF-IDF over the concatenated texts to find candidate topics (multiword allowed).
    Returns top_n terms.
    """
    texts = df.get("text", "").fillna("").astype(str).tolist()
    if not any(texts):
        return []
    corpus = ["\n".join(texts)]
    vect = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_df=0.9)
    try:
        X = vect.fit_transform(corpus)
        scores = X.toarray().flatten()
        names = vect.get_feature_names_out()
        idx = scores.argsort()[::-1][:top_n]
        terms = [names[i] for i in idx if scores[i] > 0]
        return terms
    except Exception as e:
        logger.warning("TF-IDF extraction failed: %s", e)
        return []

# convenience wrapper used by generator
def extract_topics(df, prefer_hashtags=True, top_n=12):
    """
    Returns list of {'topic': str, 'weight': int} sorted descending by weight.
    If prefer_hashtags is True and hashtags exist, uses them; otherwise TF-IDF.
    """
    ht_counts = extract_topics_by_hashtag(df)
    if prefer_hashtags and ht_counts:
        items = sorted(ht_counts.items(), key=lambda x: -x[1])
        return [{"topic":k, "weight":v} for k,v in items]
    # fallback to tf-idf terms
    terms = extract_top_terms_tfidf(df, top_n=top_n)
    return [{"topic":t, "weight": (top_n - i)} for i,t in enumerate(terms)]
