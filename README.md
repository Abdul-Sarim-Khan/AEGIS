# 🛡️ AEGIS: Distributed LLM-Powered SAST Auditor

An automated, serverless **Static Application Security Testing** tool that uses
a **Retrieval-Augmented Generation (RAG)** pipeline and a Large Language Model
to find vulnerabilities in source code, grounded in the **OWASP Top 10**.

This project was architected by Abdul Sarim Khan to satisfy the advanced requirements for two courses:

| Course | What it demonstrates |
|---|---|
| **Cloud Computing & Virtualization** | Decoupled cloud-native stack: GitOps continuous deployment, PaaS hosting (Streamlit Community Cloud), ephemeral containers, environment variable orchestration (`HF_TOKEN` / `HF_HUB_OFFLINE`), and inference offloaded to a serverless API. |
| **Parallel & Distributed Computing** | A **dynamic map-reduce analysis layer**: Code is mathematically partitioned (N/2) by a Dynamic Load Balancer to spread work across concurrent threads while respecting strict cloud API rate limits. Includes a live dashboard proving Amdahl's Law, Empirical Speedup, and Core Efficiency. |

## Project structure

```text
AEGIS - CCP/
├── app.py                 # Core application, Streamlit UI, and Map-Reduce coordinator
├── rag_engine.py          # RAG engine: load → chunk → embed → FAISS → search
├── ui_components.py       # Custom Cyberpunk UI styling and PNDC Math Dashboard
├── requirements.txt       # Dependencies (google-genai, faiss-cpu, pandas, etc.)
├── README.md
├── .gitignore
├── knowledge_base/        # OWASP Top 10 rules (Markdown, with code indicators)
│   ├── a01_broken_access_control.md
│   └── ... (a02 … a10)
└── sample_code/
    ├── vulnerable_login.py          # Basic insecure file for testing
    └── massive_vulnerable_app.py    # 5,000+ line generator for heavy load testing
```

## Architecture & Pipeline

1. **Ingestion (Vector DB)** — On startup, every `.md` OWASP rule file is loaded, split into overlapping chunks (LangChain `RecursiveCharacterTextSplitter`), embedded using `all-MiniLM-L6-v2`, and cached in a FAISS `IndexFlatIP` ephemeral vector database.
2. **Dynamic Task Decomposition** — Uploaded source code is passed into a dynamic load balancer that calculates the optimal chunk size to distribute the workload evenly while ensuring the total number of chunks never exceeds the Gemini Free-Tier API burst limits.
3. **Map Phase (Concurrency)** — Worker threads retrieve the most relevant OWASP rules for their specific code chunk via the RAG engine, then concurrently query the LLM to identify localized vulnerabilities.
4. **Reduce Phase (Fault-Tolerant Synthesis)** — The system catches the concurrent outputs and synthesizes them into a single, deduplicated markdown report. Features exponential backoff and a raw-fallback degradation if the reducer node is overloaded.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

*Tip: To suppress Hugging Face terminal warnings during local runs, `app.py` automatically injects `HF_HUB_OFFLINE=1` and `TRANSFORMERS_VERBOSITY=error` at runtime.*

## Deploy (GitOps)

1. Push this folder to a **public GitHub repository**.
2. On **Streamlit Community Cloud**, create a new app pointing to `app.py`.
3. In **Advanced Settings > Secrets**, configure the following environment variables:
   ```toml
   GEMINI_API_KEY = "your_google_ai_studio_key"
   HF_TOKEN = "your_huggingface_read_token"
   ```
4. Deploy. The cloud container will automatically download the `all-MiniLM` model on its first cold start using the provided Hugging Face token.

## Status & Milestones

- ✅ **Phase 1** — Environment setup, OWASP knowledge base parsing, Streamlit UI.
- ✅ **Phase 2** — RAG engine (LangChain splitters, Sentence-Transformers embedding, FAISS retrieval).
- ✅ **Phase 3** — New `google-genai` SDK integration, multithreaded Map-Reduce pipeline, fault tolerance.
- ✅ **Phase 4** — Dynamic Load Balancing to bypass Free-Tier API Rate Limiting (HTTP 429).
- ✅ **Phase 5** — Interactive PNDC Mathematics Dashboard (Amdahl's Law, Empirical Speedup).
- ✅ **Phase 6** — GitOps Continuous Deployment to Streamlit Community Cloud.