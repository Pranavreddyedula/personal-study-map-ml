import pandas as pd
from dateutil import parser

def load_social_json(data):
    items = data.get("activities", [])
    df = pd.DataFrame(items)

    if "timestamp" in df.columns:
        df["timestamp"] = df["timestamp"].apply(lambda x: parser.parse(x))

    return df

def extract_topics(df):
    def get_tags(text):
        if not isinstance(text, str):
            return []
        return [w[1:].lower() for w in text.split() if w.startswith("#")]

    df["topics"] = df["text"].apply(get_tags)
    return df
