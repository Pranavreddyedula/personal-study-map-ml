# personal-study-map-ml
ML-powered Personal Study Map Generator using Social Media Activity · Flask · PDF Export · ICS Calendar · Render-ready deployment
# Personal Study Map from Social Media Activity

This project analyzes a user's public social media activity (hashtags, keywords, timestamps) and automatically generates:

- A **Personal Study Map PDF**
- An **ICS Calendar file** (daily study tasks)
- A simple **Flask web interface**

Fully deployable on **Render** using the included `Procfile` and `render.yaml`.

## 🚀 Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python app.py
Upload: data/sample_social_activity.json

📦 Features

Topic extraction from text

Hashtag frequency scoring

PDF study plan export (ReportLab)

ICS event generation

Flask UI

Render-ready deployment files

🛠 Tech Stack

Python, Flask

Pandas, NLTK, Scikit-Learn

ReportLab (PDF)

ICS (Calendar Export)

Gunicorn (Production Server)
📄 License

MIT License.


---

# **📄 LICENSE**
```text
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy...
