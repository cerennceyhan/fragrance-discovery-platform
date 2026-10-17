# 🌸 Fragrance Discovery Platform

**[English](#english) | [Türkçe](#türkçe)**

## English

AI-powered perfume recommendation system. Describe the scent you like in natural language; the app extracts perfume notes with an LLM (Groq) and ranks the perfumes in a local database by how many of those notes they contain.

**Example:** "I love dry vetiver with warm, creamy sandalwood" → notes: `vetiver`, `sandalwood` → matching perfumes with the matched notes highlighted.

### Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then put your Groq API key in .env
python run.py               # http://127.0.0.1:5000
```

Get a free API key from the [Groq Console](https://console.groq.com).

### Configuration (`.env` or environment variables)

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | – | Groq API key (required for analysis) |
| `GROQ_MODEL` | `openai/gpt-oss-120b` | model used for note extraction |
| `SECRET_KEY` | dev value | set a real value in production |
| `FLASK_DEBUG` | `true` | set `false` in production |
| `PERFUME_DATABASE_PATH` | `data/perfumes.json` | alternative perfume database |

### Project layout

```
perfume_finder/
├── __init__.py     # create_app()
├── config.py       # settings from environment
├── routes.py       # / and /analyze_comment
├── llm.py          # Groq note extraction
├── matching.py     # database loading + similarity
├── rendering.py    # (escaped) HTML fragments for the UI
├── templates/      # index.html
└── static/
data/               # perfumes.json, sample_reviews.txt
analysis/           # model accuracy comparison (xlsx -> reports in results/)
scripts/            # batch_analyze.py – run the sample reviews against a running server
tests/              # pytest suite
run.py              # development server
```

### Scripts

```bash
python run.py                          # start the web app
python scripts/batch_analyze.py        # send data/sample_reviews.txt to the running app
python analysis/accuracy_analysis.py   # recompute model accuracy reports
pip install -r requirements-dev.txt && pytest
```

### Tech

Flask · Groq API · vanilla HTML/CSS/JS · JSON database

### Team

[@cerennceyhan](https://github.com/cerennceyhan) · [@ilaydabalal](https://github.com/ilaydabalal)

---

## Türkçe

Yapay zeka destekli parfüm öneri sistemi. Sevdiğiniz kokuyu doğal dille anlatırsınız; uygulama Groq üzerinden bir LLM ile nota çıkarır ve yerel veritabanındaki parfümleri bu notalarla eşleşme oranına göre sıralar.

### Hızlı başlangıç

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # .env içine Groq API anahtarınızı yazın
python run.py               # http://127.0.0.1:5000
```

API anahtarını [Groq Console](https://console.groq.com) üzerinden ücretsiz alabilirsiniz. Ayarların tablosu yukarıdadır; testler için `pip install -r requirements-dev.txt && pytest`.
