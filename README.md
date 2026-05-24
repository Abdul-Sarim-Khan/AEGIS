# 🛡️ LLM-Powered SAST Auditor

An automated, serverless **Static Application Security Testing** tool that uses
a **Retrieval-Augmented Generation (RAG)** pipeline and a Large Language Model
to find vulnerabilities in source code, grounded in the **OWASP Top 10**.

This project is structured to satisfy two courses:

| Course | What it demonstrates |
|---|---|
| **Cloud Computing & Virtualization** | Decoupled cloud-native stack: GitHub as source of truth, PaaS hosting (Streamlit Community Cloud) with auto-built containers, an **ephemeral in-RAM vector DB** (FAISS) that exists only while the container is warm, and inference offloaded to a serverless third-party API. |
| **Parallel & Distributed Computing** | A **parallel map-reduce analysis layer**: code is split into chunks analysed by *concurrent* workers (map), whose findings are merged (reduce). Supported by FAISS's multi-threaded (OpenMP) similarity search and parallel batch embedding. |

> **Honest note on the PNDC angle:** a single FAISS index in one container is
> *local* in-memory search, not a distributed system. The parallelism that
> actually carries the PNDC requirement is the **concurrent map-reduce
> analysis** and parallel embedding — benchmark sequential vs parallel and put
> the speedup chart in your results section.

## Project structure

```
sast-rag/
├── app.py                 # Streamlit UI (Phase 1) + retrieval display (Phase 2)
├── rag_engine.py          # RAG engine: load → chunk → embed → FAISS → search
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example
├── knowledge_base/        # OWASP Top 10 rules (Markdown, with code indicators)
│   ├── a01_broken_access_control.md
│   ├── ... (a02 … a10)
└── sample_code/
    └── vulnerable_login.py  # deliberately insecure file for testing
```

## How it works

1. **Ingestion** — on startup, every `.md` rule file is loaded, split into
   overlapping chunks (LangChain `RecursiveCharacterTextSplitter`), embedded
   with `all-MiniLM-L6-v2`, and added to a FAISS `IndexFlatIP` (cosine).
2. **Retrieval** — uploaded code is embedded and used to query FAISS for the
   most relevant rule chunks.
3. **Augmentation + Generation (Phase 3)** — code + retrieved rules + a system
   prompt are sent to Gemini, which returns a formatted security report.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Or test the engine without the UI:

```bash
python rag_engine.py        # prints index stats + a sample retrieval
```

## Deploy (Phase 4)

1. Push this folder to a **public GitHub repo**.
2. On **Streamlit Community Cloud**, create an app pointing at `app.py`.
3. In **Secrets**, add `GEMINI_API_KEY = "..."` (needed once Phase 3 is wired).
   Never commit the real key — `.streamlit/secrets.toml` is git-ignored.

## Known limitations (for the report)

- **Context-window limits** — single scripts, not huge multi-file repos. *(The
  parallel map-reduce layer is the mitigation: it lets you exceed a single
  window by analysing chunks concurrently.)*
- **Hallucination risk** — RAG grounds the model but cannot fully eliminate
  incorrect mitigations; human review is required.
- **Cold-start latency** — the ephemeral container spins down when idle, so the
  first request after inactivity rebuilds the FAISS index in RAM (~1–2 min).

## Status

- ✅ Phase 1 — environment, knowledge base, Streamlit UI
- ✅ Phase 2 — RAG engine (load, chunk, embed, FAISS, retrieval verified)
- ⬜ Phase 3 — Gemini integration + parallel map-reduce report generation
- ⬜ Phase 4 — deployment to Streamlit Community Cloud
