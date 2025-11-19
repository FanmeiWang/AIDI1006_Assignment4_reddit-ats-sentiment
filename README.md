# AIDI1006_Assignment4_reddit-ats-sentiment

**Reddit Sentiment on AI Recruiting & ATS (Last 30 Days)**  
Sentiment analysis of ATS / AI interview posts from **r/AskHR** and **r/recruitinghell**.  
Stack: Python (PRAW, TextBlob).  
Privacy-first: aggregated results only.

---

## Research question

**What is the overall sentiment and the most common concerns expressed in r/AskHR and r/recruitinghell posts about ATS/resumé screening and AI interviews over the past 30 days?**

---

## Overview

This repo implements a small end-to-end data product — **collect -> ingest -> process -> visualize** — to analyze recent Reddit discussions about AI hiring (ATS screening, AI interviews/assessments).  
It is minimal, reproducible, and privacy-preserving.

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

## Architecture

**Collect -> Ingest -> Process -> Visualize**

- **Collect (Python + PRAW)**  
  - Search recent posts in `r/AskHR` and `r/recruitinghell` with keyword filters.  
  - Save results to `data/raw/reddit_posts.csv`.

- **Ingest**  
  - Option A (local): work directly from local CSV files.    

- **Process**  
  - Clean text (lowercase, remove URLs, strip noise).  
  - Filter to English (e.g., `langdetect`).  
  - Run sentiment analysis:  
    - **Baseline:** TextBlob polarity (−1..+1) & subjectivity (0..1).  

- **Visualize**  
  - Spyder (`notebooks/01_eda.ipynb`) for quick EDA + charts.  

---

## Repository structure
    .
    ├─ scripts/
    │  ├─ scrape_reddit.py          
    │  ├─ clean_text.py             # dedupe, lowercase, language filter
    │  ├─ sentiment_textblob.py     # baseline sentiment (polarity, subjectivity)
    │  └─ visualize_basic.py        # optional: Azure Text Analytics sentiment
    ├─ data/
    │  ├─ raw/
    │  │  └─ reddit_posts.csv       
    │  └─ processed/
    │     ├─ reddit_clean.csv
    │     └─ reddit_scored.csv
    ├─ .gitignore
    ├─ .env                 
    ├─ requirements.txt
    └─ README.md


