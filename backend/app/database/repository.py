"""
Database repository skeleton for telemetry storage.

Planned responsibilities:
- save logs
- list logs
- save metrics
- list metrics
- save events
- list events
"""

from sqlalchemy.orm import Session

from app.database.models import EventRecord, LogRecord, MetricRecord
from app.telemetry.events import OperationalEvent
from app.telemetry.logger import StructuredLogEntry
from app.telemetry.metrics import MetricPoint


class TelemetryRepository:
    def save_log(self, db: Session, log_entry: StructuredLogEntry) -> LogRecord:
        log_record = LogRecord(
            timestamp=log_entry.timestamp,
            service=log_entry.service,
            message=log_entry.message,
            request_id=log_entry.request_id,
            level=log_entry.level,
        )
        db.add(log_record)
        db.commit()
        db.refresh(log_record)
        return log_record

    def list_logs(self, db: Session) -> list[LogRecord]:
        return db.query(LogRecord).order_by(LogRecord.timestamp.desc()).all()

    def save_metric(self, db: Session, metric_point: MetricPoint) -> MetricRecord:
        metric_record = MetricRecord(
            timestamp=metric_point.timestamp,
            service=metric_point.service,
            name=metric_point.name,
            value=metric_point.value,
            unit=metric_point.unit,
        )
        db.add(metric_record)
        db.commit()
        db.refresh(metric_record)
        return metric_record

    def list_metrics(self, db: Session) -> list[MetricRecord]:
        return db.query(MetricRecord).order_by(MetricRecord.timestamp.desc()).all()

    def save_event(self, db: Session, event: OperationalEvent) -> EventRecord:
        event_record = EventRecord(
            timestamp=event.timestamp,
            service=event.service,
            event_type=event.event_type,
            message=event.message,
            request_id=event.request_id,
        )
        db.add(event_record)
        db.commit()
        db.refresh(event_record)
        return event_record

    def list_events(self, db: Session) -> list[EventRecord]:
        return db.query(EventRecord).order_by(EventRecord.timestamp.desc()).all()
