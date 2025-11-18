import os
from datetime import datetime, timedelta, timezone

import pandas as pd
import praw
from dotenv import load_dotenv


def load_config():
    """Load config from .env with reasonable defaults."""
    load_dotenv()

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "aidi1006-ats-sentiment/0.1")

    if not client_id or not client_secret:
        raise RuntimeError(
            "Missing Reddit credentials. Please set REDDIT_CLIENT_ID and "
            "REDDIT_CLIENT_SECRET in your .env file."
        )

    days_back = int(os.getenv("DAYS_BACK", "30"))
    subreddits = os.getenv("SUBREDDITS", "AskHR,recruitinghell").split(",")
    keywords = os.getenv(
        "KEYWORDS", "ATS,resume screening,AI interview,assessment"
    ).split(",")

    subreddits = [s.strip() for s in subreddits if s.strip()]
    keywords = [k.strip() for k in keywords if k.strip()]

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "user_agent": user_agent,
        "days_back": days_back,
        "subreddits": subreddits,
        "keywords": keywords,
    }


def create_reddit_client(cfg):
    """Create a PRAW Reddit client from config dict."""
    reddit = praw.Reddit(
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        user_agent=cfg["user_agent"],
    )
    return reddit


def search_posts(reddit, cfg):
    """Search posts in target subreddits and time window."""
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=cfg["days_back"])

    all_rows = []

    # Build a basic OR query string for search
    query = " OR ".join([f'"{kw}"' if " " in kw else kw for kw in cfg["keywords"]])

    print(f"Searching subreddits: {cfg['subreddits']}")
    print(f"Keywords: {cfg['keywords']}")
    print(f"Time window: {start_time.date()} ~ {end_time.date()}")
    print(f"Search query: {query}")
    print("-" * 60)

    for sub in cfg["subreddits"]:
        sub = sub.strip()
        if not sub:
            continue

        subreddit = reddit.subreddit(sub)
        print(f"Fetching from r/{sub} ...")

        for submission in subreddit.search(
            query=query,
            sort="new",
            time_filter="month",
            limit=1000,  
        ):
            created_dt = datetime.fromtimestamp(
                submission.created_utc, tz=timezone.utc
            )

            if not (start_time <= created_dt <= end_time):
                continue

            title = submission.title or ""
            selftext = submission.selftext or ""

            full_text = (title + "\n\n" + selftext).strip()
            if len(full_text) < 20:
                continue

            all_rows.append(
                {
                    "subreddit": submission.subreddit.display_name,
                    "id": submission.id,
                    "created_utc": created_dt.isoformat(),
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "title": title,
                    "selftext": selftext,
                    "url": submission.url,
                    "permalink": f"https://reddit.com{submission.permalink}",
                }
            )

        print(f"Done r/{sub}")

    return all_rows


def save_to_csv(rows, output_path="data/raw/reddit_posts.csv"):
    """Save collected rows into a CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not rows:
        print("No posts collected. CSV will not be created.")
        return

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Saved {len(df)} rows to {output_path}")


def main():
    try:
        cfg = load_config()
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        print("Please create a .env file based on .env.example and fill in your keys.")
        return

    reddit = create_reddit_client(cfg)
    rows = search_posts(reddit, cfg)
    save_to_csv(rows)


if __name__ == "__main__":
    main()
