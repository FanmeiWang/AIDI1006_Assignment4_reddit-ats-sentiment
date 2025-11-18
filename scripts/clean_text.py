import os
import re
import pandas as pd
from langdetect import detect, LangDetectException

RAW_PATH = "data/raw/reddit_posts.csv"
OUT_PATH = "data/processed/reddit_clean.csv"
MIN_LEN = 40  # drop very short texts


def clean_text(s: str) -> str:
    """Remove URLs and squeeze whitespace."""
    if not isinstance(s, str):
        return ""
    # remove http/https and www URLs
    s = re.sub(r"(https?://\S+|www\.\S+)", " ", s, flags=re.IGNORECASE)
    # normalize whitespace
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def is_english(s: str) -> bool:
    """Return True if text is detected as English."""
    s = (s or "").strip()
    if not s:
        return False
    try:
        return detect(s[:500]) == "en"
    except LangDetectException:
        return False


def main():
    if not os.path.exists(RAW_PATH):
        print(f"[ERROR] Raw file not found: {RAW_PATH}")
        return

    print(f"[1/4] Reading {RAW_PATH} ...")
    df = pd.read_csv(RAW_PATH, encoding="utf-8")

    # ensure title/selftext exist
    df["title"] = df.get("title", "").fillna("")
    df["selftext"] = df.get("selftext", "").fillna("")

    print("[2/4] Merging and cleaning text ...")
    df["text"] = (df["title"].astype(str) + " " + df["selftext"].astype(str))
    df["text"] = df["text"].apply(clean_text)

    # drop too-short texts
    df = df[df["text"].str.len() >= MIN_LEN].copy()

    print("[3/4] Keeping English-only posts ...")
    df["is_en"] = df["text"].apply(is_english)
    df = df[df["is_en"]].copy()

    # drop exact duplicate texts
    before = len(df)
    df = df.drop_duplicates(subset=["text"])
    print(f"Removed {before - len(df)} duplicate rows.")

    # choose columns to keep
    keep_cols = [
        c for c in [
            "subreddit", "id", "created_utc", "score", "num_comments",
            "title", "selftext", "text", "url", "permalink"
        ] if c in df.columns
    ]
    df = df[keep_cols]

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"[4/4] Saved {len(df)} cleaned rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
