# src/mindmap_generator.py
import re
import os
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

# Ensure punkt tokenizer exists (first run will download)
try:
    nltk.data.find("tokenizers/punkt")
except Exception:
    nltk.download("punkt")

from nltk.tokenize import sent_tokenize

def _clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_top_terms(text, top_n=12):
    text = _clean_text(text)
    if not text:
        return []
    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.8, min_df=1, ngram_range=(1,2))
    tfidf = vectorizer.fit_transform([text])
    scores = tfidf.toarray().flatten()
    indices = scores.argsort()[::-1]
    feature_names = vectorizer.get_feature_names_out()
    top_terms = []
    for idx in indices:
        term = feature_names[idx]
        if any(c.isalpha() for c in term):
            top_terms.append(term)
        if len(top_terms) >= top_n:
            break
    return top_terms

def build_cooccurrence_graph(text, top_terms):
    sentences = sent_tokenize(text)
    terms_lower = [t.lower() for t in top_terms]
    G = nx.Graph()
    for t in top_terms:
        G.add_node(t)

    for s in sentences:
        s_low = s.lower()
        present = [top_terms[i] for i,t in enumerate(terms_lower) if t in s_low]
        for i in range(len(present)):
            for j in range(i+1, len(present)):
                a, b = present[i], present[j]
                if G.has_edge(a, b):
                    G[a][b]['weight'] += 1
                else:
                    G.add_edge(a, b, weight=1)

    if G.number_of_edges() == 0 and len(top_terms) > 1:
        center = top_terms[0]
        for t in top_terms[1:]:
            G.add_edge(center, t, weight=1)
    return G

def draw_mindmap(G, out_path, figsize=(10,10)):
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G, k=0.6, iterations=80, seed=42)

    degrees = dict(G.degree(weight='weight'))
    node_sizes = [300 + (degrees.get(n,0) * 400) for n in G.nodes()]

    edge_weights = [G[u][v].get('weight',1) for u,v in G.edges()]
    max_w = max(edge_weights) if edge_weights else 1
    edge_widths = [1 + (w / max_w) * 4 for w in edge_weights]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes)
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

def generate_mindmap_from_text(text, out_dir="output", basename="mindmap", top_n=12):
    os.makedirs(out_dir, exist_ok=True)
    text = _clean_text(text)
    top_terms = extract_top_terms(text, top_n=top_n)
    if not top_terms:
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        freq = defaultdict(int)
        for w in words:
            freq[w] += 1
        top_terms = sorted(freq, key=freq.get, reverse=True)[:top_n]

    G = build_cooccurrence_graph(text, top_terms)
    out_path = os.path.join(out_dir, f"{basename}.png")
    draw_mindmap(G, out_path)
    return out_path, top_terms
