import os
import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "data/processed/reddit_scored.csv"
CHART_DIR = "charts"


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"[ERROR] Scored file not found: {INPUT_PATH}")
        return

    os.makedirs(CHART_DIR, exist_ok=True)

    print(f"[1/3] Reading {INPUT_PATH} ...")
    df = pd.read_csv(INPUT_PATH, encoding="utf-8")

    if "sentiment_label" not in df.columns:
        print("[ERROR] 'sentiment_label' column missing; run sentiment_textblob.py first.")
        return

    # Ensure labels have a consistent order
    label_order = ["negative", "neutral", "positive"]

    # ----- Chart 1: overall sentiment distribution -----
    print("[2/3] Creating overall sentiment bar chart ...")
    counts = df["sentiment_label"].value_counts()
    counts = counts.reindex(label_order).fillna(0)

    plt.figure(figsize=(6, 4))
    counts.plot(kind="bar")
    plt.title("Overall sentiment distribution")
    plt.xlabel("Sentiment label")
    plt.ylabel("Number of posts")
    plt.tight_layout()
    out1 = os.path.join(CHART_DIR, "sentiment_overall.png")
    plt.savefig(out1)
    plt.close()
    print(f"Saved {out1}")

    # ----- Chart 2: sentiment by subreddit -----
    if "subreddit" in df.columns:
        print("[3/3] Creating sentiment-by-subreddit bar chart ...")
        crosstab = (
            df.pivot_table(
                index="subreddit",
                columns="sentiment_label",
                values="id",
                aggfunc="count",
                fill_value=0,
            )
            .reindex(columns=label_order, fill_value=0)
        )

        plt.figure(figsize=(8, 5))
        crosstab.plot(kind="bar", ax=plt.gca())
        plt.title("Sentiment distribution by subreddit")
        plt.xlabel("Subreddit")
        plt.ylabel("Number of posts")
        plt.legend(title="Sentiment")
        plt.tight_layout()
        out2 = os.path.join(CHART_DIR, "sentiment_by_subreddit.png")
        plt.savefig(out2)
        plt.close()
        print(f"Saved {out2}")
    else:
        print("No 'subreddit' column found; skipping sentiment-by-subreddit chart.")

    print("Done.")


if __name__ == "__main__":
    main()
