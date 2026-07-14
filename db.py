import os
import json
from datetime import datetime
from threading import Lock
from typing import Optional

from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(os.path.dirname(__file__), 'ai_company.db')}"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
_db_lock = Lock()


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String(36), primary_key=True, index=True)
    status = Column(String(32), nullable=False, default="queued")
    startup_idea = Column(Text, nullable=False)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=True)
    output_dir = Column(Text, nullable=True)
    results_json = Column(Text, nullable=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def create_job(job_id: str, startup_idea: str) -> Job:
    job = Job(
        job_id=job_id,
        status="queued",
        startup_idea=startup_idea,
        started_at=datetime.utcnow(),
        completed_at=None,
        error=None,
        output_dir="",
        results_json=None,
    )
    with _db_lock:
        with SessionLocal() as session:
            session.add(job)
            session.commit()
            session.refresh(job)
    return job


def update_job(job_id: str, **fields) -> Optional[Job]:
    with _db_lock:
        with SessionLocal() as session:
            job = session.get(Job, job_id)
            if not job:
                return None
            for key, value in fields.items():
                setattr(job, key, value)
            session.add(job)
            session.commit()
            session.refresh(job)
            return job


def get_job(job_id: str) -> Optional[Job]:
    with SessionLocal() as session:
        return session.get(Job, job_id)


def list_jobs() -> list[Job]:
    with SessionLocal() as session:
        return session.query(Job).order_by(Job.started_at.desc()).all()


def serialize_results(results: Optional[dict]) -> Optional[str]:
    if results is None:
        return None
    return json.dumps(results, ensure_ascii=False)


def deserialize_results(results_json: Optional[str]) -> Optional[dict]:
    if not results_json:
        return None
    try:
        return json.loads(results_json)
    except json.JSONDecodeError:
        return None
