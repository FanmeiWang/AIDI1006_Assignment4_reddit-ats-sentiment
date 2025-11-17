# AIDI1006_Assignment4_reddit-ats-sentiment
**Reddit Sentiment on AI Recruiting & ATS (Last 30 Days)**  
Sentiment analysis of ATS / AI interview posts from **r/AskHR** and **r/recruitinghell** (last 30 days). Pipeline uses Python (PRAW + TextBlob), optional **Azure Text Analytics**, and visualization in **Power BI/Tableau**. Outputs are **aggregated**; **no usernames/IDs** are stored.

---

## One‑sentence research question
**What is the overall sentiment and the most common concerns expressed in r/AskHR and r/recruitinghell posts about ATS/resume screening and AI interviews over the past 30 days?**

## Overview
This project analyzes recent Reddit discussions about AI hiring—especially ATS (Applicant Tracking Systems), resume screening, and AI interviews/assessments—to quantify sentiment and surface concern themes.  
It is a small, end‑to‑end data product: **collect → ingest → process → visualize**, with a minimal, reproducible setup.

---

## Scope
- **Subreddits:** `r/AskHR`, `r/recruitinghell`  
- **Time window:** last **30 days**  
- **Keywords:** `ATS`, `resume screening`, `AI interview`, `assessment`  
- **Unit of analysis:** post titles + bodies (optionally top comments)  
- **Language:** English-only filter (simple language detection)

---

## Ethics & Privacy
- Use only public Reddit text via the official API or compliant tools.  
- Do **not** store usernames, profile links, or IDs in outputs; keep only text and timestamps for analysis.  
- Limit outputs to aggregated statistics and anonymized snippets.  
- Respect platform terms, rate-limit requests, and document data deletion on request (if applicable).

---

## Architecture (1‑page)
```mermaid
flowchart TD
  A[Reddit API (PRAW)\nkeywords + date filter] --> B[data/raw/reddit_posts.csv]
  B --> C[Clean & dedupe\n+ language filter]
  C --> D[data/processed/reddit_clean.csv]
  D --> E[Sentiment: TextBlob\npolarity, subjectivity]
  D -. optional .-> F[Azure Text Analytics\nsentiment confidence]
  E --> G[data/processed/reddit_scored.csv]
  F --> G
  G --> H[notebooks/01_eda.ipynb\ncharts & n-grams]
  G --> I[dashboards/\nPower BI or Tableau]

