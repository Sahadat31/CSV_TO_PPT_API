# 📊 CSV to PPT API (FastAPI)

This backend transforms **unstructured CSVs** into **AI-generated PowerPoint presentations** with insights, summary, and charts using LLMs and data visualization tools.

---

## 🚀 Features

- Upload unstructured CSVs (even messy ones)
- Gemini-powered AI data cleaning & insight generation
- Auto-generated charts using matplotlib/seaborn
- AI-curated PowerPoint presentations with summaries, insights, and visuals
- Supports direct PPT download from API

---

## 🛠️ Stack

- **FastAPI** (REST API)
- **Pandas** (data cleaning)
- **Google Gemini / OpenAI GPT-4** (LLM)
- **Matplotlib & Seaborn** (visualization)
- **python-pptx** (PPT generation)

---

## ⚙️ Setup

```bash
git clone https://github.com/your-org/CSV_TO_PPT_API.git
cd CSV_TO_PPT_API
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
