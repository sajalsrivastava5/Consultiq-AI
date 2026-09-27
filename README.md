# 🧠 ConsultIQ AI - Enterprise Knowledge Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-FF4B4B)
![FAISS](https://img.shields.io/badge/Vector%20Store-FAISS-6E56CF)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Portfolio%20POC-orange)

> **Educational / portfolio project.** Built to demonstrate GenAI engineering,
> RAG system design, and enterprise software architecture. Uses only
> synthetic, publicly-shaped sample data - no proprietary or confidential
> data from any organization is used or referenced. Not deployed inside, or
> claiming affiliation with, any real consulting firm.

ConsultIQ AI is a Retrieval-Augmented Generation (RAG) knowledge assistant
that simulates an internal accelerator a consulting firm could use to make
its own proposals, SOWs, case studies, and reports instantly searchable -
replacing slow keyword search with semantic search, a cited-source chat
assistant, and an RFP-to-past-proposal recommendation engine.

**[📸 Screenshots](#screenshots)** · **[🏗️ Architecture](docs/ARCHITECTURE.md)** · **[🚀 Quick Start](#quick-start)** · **[📊 Business Value](#business-value-illustrative)**

---

## Features

| Area | What it does |
|---|---|
| 🔐 **Auth** | Role-based login (Admin / Consultant / Viewer), session management |
| 📤 **Upload** | PDF / DOCX / PPTX / XLSX / TXT, multi-file, progress bar, duplicate detection |
| 🏷️ **Auto-tagging** | Detects industry, technology, country, service line, skills, tools, deliverables |
| ✂️ **Chunking** | Overlap-aware chunking, header/footer stripping, table preservation |
| 🧬 **Embeddings** | Sentence-Transformers (configurable model) with automatic offline fallback |
| 🔍 **Semantic Search** | Natural-language search, similarity scoring, keyword highlighting |
| 💬 **RAG Chat** | Cited, no-hallucination chat assistant; provider-agnostic (OpenAI / Azure / Ollama / offline demo) |
| 📋 **Recommender** | Upload an RFP → get similar past proposals + suggested skills/tech/timeline |
| 📊 **Analytics** | Interactive Plotly dashboard; Power BI-ready CSV export |
| ⚙️ **Admin Console** | Users, documents, logs, system health, DB stats |
| 📝 **Logging** | Application, error, audit, and search logs (rotating files) |

## Screenshots

_Run the app locally (`streamlit run app.py`) and drop screenshots here before
sharing — e.g. `assets/screenshot-chat.png`, `assets/screenshot-dashboard.png`._

## Quick Start

```bash
git clone <this-repo>
cd consultiq-ai
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env        # defaults work out of the box — no keys required
python sample_data/generate_samples.py   # optional: generate demo documents

streamlit run app.py
```

Open `http://localhost:8501` and sign in with a demo account:

```
admin       / Admin@123      (full access incl. Admin Console)
consultant  / Consult@123    (upload, chat, search, recommend)
viewer      / Viewer@123     (search + chat only)
```

The app runs with **zero API keys** out of the box: `LLM_PROVIDER=demo` in
`.env.example` answers chat queries by extracting and citing the most
relevant retrieved passages instead of calling an LLM. Set `LLM_PROVIDER` to
`openai`, `azure_openai`, or `ollama` (plus the matching credentials) in
`.env` to enable generative synthesis — no code changes needed.

### Docker

```bash
docker compose up --build
```

## Architecture

```
Document Loader → Metadata Extraction → Text Chunking → Embedding Generation
     → FAISS Vector Store → Retriever → LLM (or offline extractive fallback)
     → Response Generator → Streamlit UI
```

Full system architecture, sequence diagrams, ER diagram, and component
diagram: **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

## Project Structure

```
consultiq-ai/
├── app.py                    # Streamlit entry point + auth/session/navigation
├── config.py                 # Central, env-driven configuration
├── ingestion/                 # Document loaders, metadata extraction, pipeline orchestration
├── embeddings/                 # Embedding engine (Sentence-Transformers + offline fallback)
├── rag/                        # Vector store, retriever, RAG pipeline
├── recommendation/             # Proposal/RFP similarity recommender
├── analytics/                  # Dashboard figures + Power BI export
├── auth/                       # Role-based auth
├── database/                   # SQLite schema + data access
├── utils/                      # Text processing, logging
├── ui/pages/                   # Streamlit pages (Upload, Chat, Search, Dashboard, Recommend, Admin)
├── sample_data/                 # Synthetic sample consulting documents + generator
├── tests/                       # pytest suite
├── docs/                        # Architecture, user guide, FAQ/troubleshooting
├── Dockerfile, docker-compose.yml
└── requirements.txt
```

## Configuration

Every tunable is an environment variable — see **[.env.example](.env.example)**
for the full list (LLM provider, embedding model, chunk size/overlap,
similarity threshold, upload limits, session timeout).

## Testing

```bash
pytest tests/ -v
```

Covers text chunking, document loaders, metadata extraction, auth, the
end-to-end RAG pipeline (ingestion → retrieval → citation), and the
proposal recommender.

## Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) — diagrams, data flow, design decisions
- [User & Developer Guide](docs/USER_GUIDE.md) — installation, usage, API reference, deployment
- [FAQ & Troubleshooting](docs/FAQ_TROUBLESHOOTING.md)
- [Resume Points & Interview Prep](docs/RESUME_AND_INTERVIEW_PREP.md)
- [PPO Pitch Deck](ConsultIQ_AI_PPO_Pitch.pptx)

## Business Value (Illustrative)

These are **illustrative estimates based on comparable industry deployments**,
not measured figures from a real organizational rollout:

- Document search time: hours → seconds via semantic search
- Higher proposal/case-study reuse across consulting teams
- Faster new-consultant onboarding to firm knowledge
- Estimated productivity gain shown live on the Analytics Dashboard, with methodology disclosed

## Roadmap / Future Scope

- Scale sample corpus from ~15 to ~100 documents across all 10 spec'd industries
- Swap SQLite → PostgreSQL for multi-user production concurrency
- Add SSO/OAuth (Azure AD) in place of the demo auth module
- Expand automated test coverage (integration tests for each LLM provider path)
- Add a full diagram suite (sequence, ER, deployment, data-flow) as rendered images

## License

MIT — see [LICENSE](LICENSE). Sample data is synthetic and freely reusable.

## Contributing

This is a personal portfolio project built for a KPMG Business Analytics
Programme capstone / PPO evaluation. Suggestions and issues are welcome via
the repository's issue tracker.
