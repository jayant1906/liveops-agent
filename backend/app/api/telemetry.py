"""
Telemetry API skeleton.

Planned routes:
- logs
- metrics
- events
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repository import TelemetryRepository
from app.telemetry.events import EventRecorder, EventType
from app.telemetry.logger import LogLevel, StructuredLogger
from app.telemetry.metrics import MetricName, MetricsCollector


router = APIRouter(prefix="/telemetry", tags=["telemetry"])
logger = StructuredLogger()
metrics_collector = MetricsCollector()
event_recorder = EventRecorder()
repository = TelemetryRepository()


class CreateLogRequest(BaseModel):
    level: str
    service: str
    message: str
    request_id: Optional[str] = None


class CreateMetricRequest(BaseModel):
    name: str
    service: str
    value: float


class CreateEventRequest(BaseModel):
    event_type: str
    service: str
    message: str
    request_id: Optional[str] = None


@router.get("/logs")
def list_logs(db: Session = Depends(get_db)):
    return {"logs": repository.list_logs(db)}


@router.post("/logs")
def create_log(log_request: CreateLogRequest, db: Session = Depends(get_db)):
    if log_request.level == LogLevel.INFO:
        log_entry = logger.info(
            service=log_request.service,
            message=log_request.message,
            request_id=log_request.request_id,
        )
    elif log_request.level == LogLevel.WARNING:
        log_entry = logger.warning(
            service=log_request.service,
            message=log_request.message,
            request_id=log_request.request_id,
        )
    elif log_request.level == LogLevel.ERROR:
        log_entry = logger.error(
            service=log_request.service,
            message=log_request.message,
            request_id=log_request.request_id,
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid log level")

    return repository.save_log(db, log_entry)


@router.get("/metrics")
def list_metrics(db: Session = Depends(get_db)):
    return {"metrics": repository.list_metrics(db)}


@router.post("/metrics")
def create_metric(metric_request: CreateMetricRequest, db: Session = Depends(get_db)):
    if metric_request.name == MetricName.CPU_USAGE:
        metric_point = metrics_collector.record_cpu_usage(
            service=metric_request.service,
            value=metric_request.value,
        )
    elif metric_request.name == MetricName.MEMORY_USAGE:
        metric_point = metrics_collector.record_memory_usage(
            service=metric_request.service,
            value=metric_request.value,
        )
    elif metric_request.name == MetricName.LATENCY:
        metric_point = metrics_collector.record_latency(
            service=metric_request.service,
            value=metric_request.value,
        )
    elif metric_request.name == MetricName.ERROR_RATE:
        metric_point = metrics_collector.record_error_rate(
            service=metric_request.service,
            value=metric_request.value,
        )
    elif metric_request.name == MetricName.DB_CONNECTIONS:
        metric_point = metrics_collector.record_db_connections(
            service=metric_request.service,
            value=metric_request.value,
        )
    elif metric_request.name == MetricName.REQUEST_COUNT:
        metric_point = metrics_collector.record_request_count(
            service=metric_request.service,
            value=metric_request.value,
        )
    elif metric_request.name == MetricName.THROUGHPUT:
        metric_point = metrics_collector.record_throughput(
            service=metric_request.service,
            value=metric_request.value,
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid metric name")

    return repository.save_metric(db, metric_point)


@router.get("/events")
def list_events(db: Session = Depends(get_db)):
    return {"events": repository.list_events(db)}


@router.post("/events")
def create_event(event_request: CreateEventRequest, db: Session = Depends(get_db)):
    if event_request.event_type == EventType.DEPLOYMENT:
        event = event_recorder.deployment(
            service=event_request.service,
            message=event_request.message,
            request_id=event_request.request_id,
        )
    elif event_request.event_type == EventType.SERVICE_RESTART:
        event = event_recorder.service_restart(
            service=event_request.service,
            message=event_request.message,
            request_id=event_request.request_id,
        )
    elif event_request.event_type == EventType.FAILURE_INJECTED:
        event = event_recorder.failure_injected(
            service=event_request.service,
            message=event_request.message,
            request_id=event_request.request_id,
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid event type")

    return repository.save_event(db, event)
