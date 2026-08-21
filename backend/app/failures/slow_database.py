from sqlalchemy import text

from app.database.connection import SessionLocal
from app.telemetry.events import EventRecorder
from app.telemetry.logger import StructuredLogger
from app.telemetry.metrics import MetricsCollector

import time


logger = StructuredLogger()
event_recorder = EventRecorder()
metric_point = MetricsCollector()

def trigger_slow_database(request_id: str | None = None, delay_seconds: int = 5) -> None:
    """Intentionally triggering a very slow DB request"""
    db = SessionLocal()
    start_time = time.perf_counter()
    try:
        db.execute(text("SELECT pg_sleep(:delay)"), {"delay": delay_seconds})
        metric_point.record_latency(service="Database", value=(time.perf_counter() - start_time) * 1000)
        logger.error(service="Database", message=f"Database failure injected: high latency", request_id=request_id)
        event_recorder.failure_injected(service= "Database", message="FAILURE_INJECTED", request_id=request_id)
    finally:
        db.close()