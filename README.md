# AIDI1006_Assignment4_reddit-ats-sentiment
**Reddit Sentiment on AI Recruiting & ATS (Last 30 Days)**  
Sentiment analysis of ATS / AI interview posts from **r/AskHR** and **r/recruitinghell**.  
Stack: Python (PRAW, TextBlob), optional Azure Text Analytics, Power BI/Tableau.  
Privacy-first: aggregated results only, **no usernames/IDs**.

---

## One‑sentence research question
**What is the overall sentiment and the most common concerns expressed in r/AskHR and r/recruitinghell posts about ATS/resumé screening and AI interviews over the past 30 days?**

---

## Overview
This repo implements a small end‑to‑end data product—**collect → ingest → process → visualize**—to analyze recent Reddit discussions about AI hiring (ATS screening, AI interviews/assessments). It’s minimal, reproducible, and privacy‑preserving.

---

## MVP outputs
- `data/raw/reddit_posts.csv` — topic‑matched posts (last 30 days)  
- `data/processed/sentiment.csv` — TextBlob polarity/subjectivity; (optional) Azure TA scores  
- Simple visuals — sentiment distribution, subreddit comparison, top n‑grams  
- `docs/architecture.png` — one‑page diagram  
- **5–10 min screen recording** demo (silent is fine; use on‑screen captions)

---

## Scope
- **Subreddits:** `r/AskHR`, `r/recruitinghell`  
- **Time window:** last **30 days**  
- **Keywords:** `ATS`, `resume screening`, `AI interview`, `assessment`  
- **Unit:** post titles + bodies (optionally top comments)  
- **Language:** filter to English where possible

---

## Ethics & Privacy
- Use only **public** Reddit content via the official API or compliant tools.
- Store **text + timestamps** only; **no usernames, profile links, or IDs** in outputs.
- Respect platform ToS and rate limits; document removal on request (if applicable).
- Report only **aggregated** statistics and anonymized short snippets.

---

## Architecture (1‑page sketch)
**Collect → Ingest → Process → Visualize**

- **Collect**: Reddit API (PRAW), keyword + date filters  
- **Ingest**: write CSV to `data/raw/` (local) or Azure Blob (optional)  
- **Process**: clean/dedupe/language filter → TextBlob (baseline), Azure TA (optional)  
- **Visualize**: notebook charts or Power BI/Tableau

_Save the diagram as `docs/architecture.png` and reference it here._

---

## Repository structure
```text
.
├─ src/
│  ├─ collect.py              # query Reddit → CSV
│  ├─ clean.py                # dedupe, lowercase, language filter
│  ├─ analyze.py              # TextBlob polarity/subjectivity + labels
│  └─ visualize.py            # simple charts saved to charts/*.png
├─ notebooks/
│  └─ 01_eda.ipynb            # EDA, n-grams, subreddit comparison
├─ dashboards/
│  └─ reddit_ats_sentiment.pbix   # or Tableau workbook
├─ data/
│  ├─ raw/
│  └─ processed/
├─ docs/
│  └─ architecture.png
├─ .env.example               # environment variables template
├─ requirements.txt
└─ README.md
