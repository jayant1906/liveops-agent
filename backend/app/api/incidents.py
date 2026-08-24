from enum import Enum
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Incident as IncidentRecord
from app.detection.detector import detect_incidents


router = APIRouter(prefix="/incidents", tags=["incidents"])


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class IncidentResponse(BaseModel):
    id: int
    service: str
    type: str
    severity: Severity
    message: str
    status: IncidentStatus
    metric_value: float
    threshold: float
    detected_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


def build_incident_response(incident: IncidentRecord) -> IncidentResponse:
    return IncidentResponse(
        id=incident.id,
        service=incident.service,
        type=incident.incident_type,
        severity=incident.severity,
        message=incident.message,
        status=incident.status,
        metric_value=incident.metric_value,
        threshold=incident.threshold,
        detected_at=incident.timestamp,
    )


@router.get("")
def list_incidents(db: Session = Depends(get_db)):
    incidents = db.query(IncidentRecord).order_by(IncidentRecord.timestamp.desc()).all()
    return {
        "incidents": [
            build_incident_response(incident)
            for incident in incidents
        ]
    }


@router.post("/detect")
def run_incident_detection(db: Session = Depends(get_db)):
    incidents = detect_incidents(db)
    return {
        "incidents": [
            build_incident_response(incident)
            for incident in incidents
        ]
    }
