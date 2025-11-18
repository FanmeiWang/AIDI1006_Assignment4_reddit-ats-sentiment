import os
import pandas as pd
from textblob import TextBlob

INPUT_PATH = "data/processed/reddit_clean.csv"
OUT_PATH = "data/processed/reddit_scored.csv"

POS_THRESH = 0.05
NEG_THRESH = -0.05


def label_from_polarity(p: float) -> str:
    if p >= POS_THRESH:
        return "positive"
    elif p <= NEG_THRESH:
        return "negative"
    else:
        return "neutral"


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"[ERROR] Cleaned file not found: {INPUT_PATH}")
        return

    print(f"[1/3] Reading {INPUT_PATH} ...")
    df = pd.read_csv(INPUT_PATH, encoding="utf-8")

    if "text" not in df.columns:
        print("[ERROR] 'text' column missing; run clean_text.py first.")
        return

    print("[2/3] Scoring sentiment with TextBlob ...")
    polarities = []
    subjectivities = []
    labels = []

    for t in df["text"].astype(str):
        blob = TextBlob(t)
        pol = float(blob.sentiment.polarity)
        sub = float(blob.sentiment.subjectivity)
        polarities.append(pol)
        subjectivities.append(sub)
        labels.append(label_from_polarity(pol))

    df["polarity"] = polarities
    df["subjectivity"] = subjectivities
    df["sentiment_label"] = labels

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"[3/3] Saved {len(df)} scored rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
