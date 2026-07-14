# AI Company - Project Architecture & Execution Flow

This document outlines the complete data and control flow for the AI Company project, detailing how a user's startup idea travels from the main page to a fully generated business output.

## 1. Entry Points & Frontend

The system offers two ways to interact with it:
- **`app.py` (Streamlit Dashboard):** A direct, interactive frontend where the user inputs their startup idea. It acts as a visual interface that can run the pipeline directly or interface with the API.
- **`api.py` (FastAPI Server):** A RESTful backend that provides endpoints (like `/api/run`, `/api/status/{id}`, and `/api/results/{id}`) to queue and process startup ideas asynchronously. It also serves a static HTML frontend (`frontend/index.html`).

## 2. API & Database Layer (`api.py` & `db.py`)

When an idea is submitted via the API:
1. **Endpoint Trigger:** A `POST` request is sent to `/api/run` containing the `startup_idea`.
2. **Database Record:** `db.py` creates a new `Job` record in `ai_company.db` (SQLite) with a status of `"queued"`.
3. **Background Execution:** `api.py` spawns a background thread (`_run_in_background`) so the main server doesn't block. The job status updates to `"running"`.

## 3. Orchestration Engine (`crew.py`)

The background thread calls `run_company(startup_idea)` located in `crew.py`. This is the core orchestration file.
1. **Pipeline Initialization:** It sets up a sequential pipeline of five departments:
   - CEO (Strategy)
   - Research (Market Analysis)
   - Developer (Code & MVP)
   - Marketing (Campaigns)
   - Customer Support (FAQ & Help)
2. **Agent Execution:** It iterates through each department one by one.
3. **Rate Limit Handling:** To respect the Groq API rate limits, it applies an `AGENT_DELAY_SECONDS` wait between each agent's execution and implements a 3-retry mechanism.

## 4. Agents & Configuration (`agents.py` & `config.py`)

Before an agent starts working, its configuration is loaded:
1. **`config.py`:** Loads the `GROQ_API_KEY` from `.env`, specifies the AI model (e.g., `llama-3.1-70b-versatile`), and sets generation limits like `MAX_OUTPUT_TOKENS` and delay timers.
2. **`agents.py`:** Initializes the specific CrewAI `Agent` objects. Each agent is given a specific persona (e.g., "10x Full-Stack Developer" or "Visionary CEO") and attached to the configured Groq LLM instance.

## 5. Tasks Execution (`tasks.py`)

Once an agent is loaded, `crew.py` assigns it a specific task from `tasks.py`:
- Each task combines the `startup_idea` with explicit instructions (e.g., "Build a 6-month product roadmap" or "Write engaging LinkedIn posts").
- The CrewAI framework triggers the LLM (Groq) to execute the task. The output is captured as a string.

## 6. Output Storage & Completion

After all five agents have completed their tasks:
1. **File Generation:** `crew.py` collects the outputs and creates a timestamped folder inside the `outputs/` directory (e.g., `outputs/run_20260707_140000/`).
2. **Markdown Files:** It writes a distinct markdown file for each department (e.g., `ceo_strategy.md`, `market_research.md`) alongside a compiled `metadata.json` file.
3. **Database Update:** The results are sent back to `api.py`, which serializes the output into the SQLite database and marks the job status as `"completed"`.
4. **User Retrieval:** The user's frontend polls `/api/status` or reads directly to display the final comprehensive startup strategy.
