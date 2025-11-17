# AIDI1006_Assignment4_reddit-ats-sentiment

**Reddit Sentiment on AI Recruiting & ATS (Last 30 Days)**  
Sentiment analysis of ATS / AI interview posts from **r/AskHR** and **r/recruitinghell**.  
Stack: Python (PRAW, TextBlob), optional Azure Text Analytics, Power BI/Tableau.  
Privacy-first: aggregated results only, **no usernames/IDs**.

---

## One-sentence research question

**What is the overall sentiment and the most common concerns expressed in r/AskHR and r/recruitinghell posts about ATS/resumé screening and AI interviews over the past 30 days?**

---

## Overview

This repo implements a small end-to-end data product — **collect → ingest → process → visualize** — to analyze recent Reddit discussions about AI hiring (ATS screening, AI interviews/assessments).  
It is minimal, reproducible, and privacy-preserving.

---

## MVP outputs

- `data/raw/reddit_posts.csv` — topic-matched posts (last 30 days)  
- `data/processed/reddit_clean.csv` — cleaned & filtered text  
- `data/processed/sentiment.csv` — TextBlob polarity/subjectivity; (optional) Azure TA scores  
- Simple visuals — sentiment distribution, subreddit comparison, top n-grams  
- `docs/architecture.png` — one-page architecture diagram  
- **5–10 min screen recording** demo (silent is fine; on-screen captions are enough)

---

## Scope

- **Subreddits:** `r/AskHR`, `r/recruitinghell`  
- **Time window:** last 30 days  
- **Keywords:** `ATS`, `resume screening`, `AI interview`, `assessment`  
- **Unit of analysis:** post titles + bodies (optionally top comments)  
- **Language:** English only (basic language detection filter)

---

## Ethics & Privacy

- Use only public Reddit content via official API or compliant tools.  
- Do **not** store usernames, profile links, or IDs in any released data.  
- Keep only: text, subreddit, timestamps, simple metadata for analysis.  
- Share only **aggregated** statistics and anonymized short snippets.  
- Respect Reddit’s API terms and rate limits.  
- Be prepared to delete raw data if a takedown is requested.

---

## Architecture (1-page sketch)

**Collect → Ingest → Process → Visualize**

- **Collect (Python + PRAW)**  
  - Search recent posts in `r/AskHR` and `r/recruitinghell` with keyword filters.  
  - Save results to `data/raw/reddit_posts.csv`.

- **Ingest**  
  - Option A (local): work directly from local CSV files.  
  - Option B (Azure): upload CSV to Azure Blob; optionally use Azure Data Factory to move into Azure SQL.

- **Process**  
  - Clean text (lowercase, remove URLs, strip noise).  
  - Filter to English (e.g., `langdetect`).  
  - Run sentiment analysis:  
    - **Baseline:** TextBlob polarity (−1..+1) & subjectivity (0..1).  
    - **Optional:** Azure Text Analytics sentiment scores.

- **Visualize**  
  - Jupyter notebook (`notebooks/01_eda.ipynb`) for quick EDA + charts.  
  - Or a Power BI / Tableau dashboard on top of `data/processed/sentiment.csv`.

> The actual architecture image can be exported as `docs/architecture.png` and referenced in the report/PPT.

---

## Repository structure

    .
    ├─ scripts/
    │  ├─ scrape_reddit.py          # collect posts into CSV
    │  ├─ clean_text.py             # dedupe, lowercase, language filter
    │  ├─ sentiment_textblob.py     # baseline sentiment (polarity, subjectivity)
    │  └─ sentiment_azure.py        # optional: Azure Text Analytics sentiment
    ├─ notebooks/
    │  └─ 01_eda.ipynb              # EDA, charts, top terms
    ├─ dashboards/
    │  └─ reddit_ats_sentiment.pbix # or Tableau workbook
    ├─ data/
    │  ├─ raw/
    │  │  └─ reddit_posts.csv       # collected raw posts (not committed)
    │  └─ processed/
    │     ├─ reddit_clean.csv
    │     └─ sentiment.csv
    ├─ docs/
    │  └─ architecture.png
    ├─ .env.example                 # environment variable template
    ├─ requirements.txt
    └─ README.md

---

## Quickstart

### 1) Environment

    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate

    pip install -r requirements.txt

### Minimal `requirements.txt`

    praw
    pandas
    python-dotenv
    textblob
    langdetect
    matplotlib
    scikit-learn
    # optional:
    azure-ai-textanalytics

### Initialize TextBlob resources (first run)

    python -m textblob.download_corpora

---

### 2) Configure credentials

Copy `.env.example` → `.env` and fill in:

    # Reddit
    REDDIT_CLIENT_ID=xxxx
    REDDIT_CLIENT_SECRET=xxxx
    REDDIT_USER_AGENT=aidi1006-ats-sentiment/0.1 (by u/your_username)

    # Azure (optional)
    AZURE_TEXT_KEY=xxxx
    AZURE_TEXT_ENDPOINT=https://<your-cog-services>.cognitiveservices.azure.com/

---

### 3) Collect (last 30 days)

    python scripts/scrape_reddit.py \
      --subreddits r/AskHR r/recruitinghell \
      --query "ATS OR resume screening OR \"AI interview\" OR assessment" \
      --days 30 \
      --limit 1000 \
      --out data/raw/reddit_posts.csv

Script tasks:

- Call Reddit API for each subreddit with the query.  
- Filter by `created_utc` within the last N days.  
- Save fields like title, selftext, subreddit, score, created_utc, permalink (for local use only).

---

### 4) Clean

    python scripts/clean_text.py \
      --input data/raw/reddit_posts.csv \
      --output data/processed/reddit_clean.csv

Cleaning steps:

- Drop duplicates.  
- Remove posts with empty or ultra-short text.  
- Lowercase text; strip URLs; strip extra whitespace.  
- Use `langdetect` (or similar) to keep only English posts.

---

### 5) Sentiment (baseline: TextBlob)

    python scripts/sentiment_textblob.py \
      --input data/processed/reddit_clean.csv \
      --output data/processed/sentiment.csv

Each row gains:

- `polarity` (−1.0 … +1.0)  
- `subjectivity` (0.0 … 1.0)  
- `sentiment_label` (negative / neutral / positive), using:

- `polarity >= 0.05` → **Positive**  
- `-0.05 < polarity < 0.05` → **Neutral**  
- `polarity <= -0.05` → **Negative**

Optional Azure Text Analytics:

    python scripts/sentiment_azure.py \
      --input data/processed/reddit_clean.csv \
      --output data/processed/sentiment_azure.csv

Adds Azure sentiment scores such as `positive`, `neutral`, `negative`.

---

### 6) Visualize

Option A — Notebook:

- Open `notebooks/01_eda.ipynb`.  
- Build:
  - Sentiment distribution (pos/neu/neg).  
  - Comparison by subreddit (`AskHR` vs `recruitinghell`).  
  - Top bigrams/trigrams in negative posts.  
  - Simple timeline over the last 30 days.

Option B — Power BI / Tableau:

- Load `data/processed/sentiment.csv`.  
- Build visuals:
  - Bar chart: sentiment count by subreddit.  
  - Bar/column: top concern phrases (n-grams).  
  - Line chart: posts per day by sentiment.

---

## Methodology (summary)

- **Retrieval:** keyword search in selected subreddits for the last 30 days, limited by API rate.  
- **Cleaning:** deduplicate, remove URLs/noise, filter to English.  
- **Sentiment:** TextBlob as baseline; optional Azure TA for comparison.  
- **Labeling:** threshold-based mapping from polarity to pos/neu/neg.  
- **Themes (optional):** TF-IDF + simple clustering to surface main concern groups.  
- **Visualization:** distribution charts, subreddit comparison, top terms, timeline.

---

## Deliverables checklist (MVP)

- `data/raw/reddit_posts.csv` (sample)  
- `data/processed/sentiment.csv` (final)  
- `docs/architecture.png` (1-page diagram)  
- Charts in `notebooks/` and/or `dashboards/reddit_ats_sentiment.pbix`  
- **5–10 min** screen recording demo (on-screen captions; voice optional)

---

## Limitations

- Time-bounded to 30 days → recency bias.  
- Reddit population bias; sarcasm and nuanced tone can confuse sentiment models.  
- Keyword search may miss relevant posts without those exact terms.

---

