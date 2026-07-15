"""
AI Company — FastAPI Backend
=============================
REST API to trigger the AI company pipeline and retrieve results.

Endpoints:
  POST /api/run          → Start a new company run
  GET  /api/status/{id}  → Check run status
  GET  /api/results/{id} → Get run results
  GET  /api/history      → List all past runs
"""

import os
import uuid
import time
import threading
import logging
from collections import deque
from datetime import datetime
from typing import Optional

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Depends,
    Header,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field, field_validator

from crew import run_company
from config import API_KEY, validate_config
from db import (
    init_db,
    create_job,
    get_job,
    list_jobs,
    update_job,
    serialize_results,
    deserialize_results,
)

# Path to the frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

# ── Logging ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("ai_company")

# ── App Setup ────────────────────────────────────────────
app = FastAPI(
    title="🏢 AI Company API",
    description="Multi-agent AI startup engine powered by CrewAI & Gemini",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 10
rate_limits: dict[str, deque[float]] = {}
rate_limit_lock = threading.Lock()


def get_client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if API_KEY:
        if x_api_key != API_KEY:
            logger.warning("Invalid API key attempt")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )


def rate_limit(request: Request):
    ip = get_client_ip(request)
    now = time.time()
    with rate_limit_lock:
        queue = rate_limits.setdefault(ip, deque())
        while queue and queue[0] <= now - RATE_LIMIT_WINDOW_SECONDS:
            queue.popleft()
        if len(queue) >= RATE_LIMIT_MAX_REQUESTS:
            logger.warning("Rate limit exceeded for %s", ip)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )
        queue.append(now)

# ── App Setup ────────────────────────────────────────────
app = FastAPI(
    title="🏢 AI Company API",
    description="Multi-agent AI startup engine powered by CrewAI & Gemini",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models ───────────────────────────────────────────────
class RunRequest(BaseModel):
    startup_idea: str = Field(..., min_length=5, max_length=500)
    model: Optional[str] = None

    @field_validator("startup_idea")
    def strip_startup_idea(cls, value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("startup_idea must not be empty")
        return text


class RunResponse(BaseModel):
    job_id: str
    status: str
    message: str


class JobStatus(BaseModel):
    job_id: str
    status: str
    startup_idea: str
    started_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None


# ── Background Runner ────────────────────────────────────
def _run_in_background(job_id: str, startup_idea: str, model: str = None):
    logger.info("Job %s: starting background execution", job_id)
    update_job(job_id, status="running")
    try:
        results = run_company(startup_idea, model)
        output_dir = results.get("_metadata", {}).get("output_dir", "")
        update_job(
            job_id,
            status="completed",
            completed_at=datetime.utcnow(),
            results_json=serialize_results({k: v for k, v in results.items() if k != "_metadata"}),
            output_dir=output_dir,
        )
        logger.info("Job %s: completed successfully", job_id)
    except Exception as exc:
        logger.exception("Job %s failed", job_id)
        update_job(
            job_id,
            status="failed",
            completed_at=datetime.utcnow(),
            error=str(exc),
        )


@app.on_event("startup")
async def startup_event():
    init_db()
    validate_config()
    logger.info("AI Company API started")


@app.post(
    "/api/run",
    response_model=RunResponse,
    dependencies=[Depends(verify_api_key), Depends(rate_limit)],
)
async def start_run(request: RunRequest):
    job_id = str(uuid.uuid4())[:8]
    create_job(job_id, request.startup_idea)
    logger.info("Job %s created", job_id)

    thread = threading.Thread(
        target=_run_in_background,
        args=(job_id, request.startup_idea, request.model),
        daemon=True,
    )
    thread.start()

    return RunResponse(
        job_id=job_id,
        status="queued",
        message=f"AI Company is now working on: '{request.startup_idea}'",
    )


@app.get(
    "/api/status/{job_id}",
    response_model=JobStatus,
    dependencies=[Depends(verify_api_key)],
)
async def get_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobStatus(
        job_id=job.job_id,
        status=job.status,
        startup_idea=job.startup_idea,
        started_at=job.started_at.isoformat(),
        completed_at=job.completed_at.isoformat() if job.completed_at else None,
        error=job.error,
    )


@app.get(
    "/api/results/{job_id}",
    dependencies=[Depends(verify_api_key), Depends(rate_limit)],
)
async def get_results(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.status != "completed":
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "job_id": job.job_id,
                "status": job.status,
                "message": "Job has not completed yet." if job.status != "failed"
                else f"Job failed: {job.error}",
            },
        )
    return {
        "job_id": job.job_id,
        "status": "completed",
        "startup_idea": job.startup_idea,
        "results": deserialize_results(job.results_json) or {},
        "output_dir": job.output_dir,
    }


@app.get(
    "/api/history",
    dependencies=[Depends(verify_api_key), Depends(rate_limit)],
)
async def get_history():
    history = [
        {
            "job_id": job.job_id,
            "status": job.status,
            "startup_idea": job.startup_idea,
            "started_at": job.started_at.isoformat(),
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        }
        for job in list_jobs()
    ]
    return {"runs": history}


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "api_key_protected": bool(API_KEY),
    }


@app.get("/health")
async def simple_health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# Mount static files LAST (so API routes take priority)
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")
