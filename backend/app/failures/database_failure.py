from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import SessionLocal
from app.telemetry.events import EventRecorder
from app.telemetry.logger import StructuredLogger


logger = StructuredLogger()
event_recorder = EventRecorder()


def trigger_database_failure(request_id: str | None = None) -> None:
    """Intentionally triggering a database failure."""
    db = SessionLocal()
    try:
        db.execute(text("SELECT * FROM table_does_not_exist"))
    
    except SQLAlchemyError as error:
        logger.error(service="Database", message=f"Database failure injected: {error}", request_id=request_id)
        event_recorder.failure_injected(service= "Database", message="FAILURE_INJECTED", request_id=request_id)
    finally:
        db.close()
