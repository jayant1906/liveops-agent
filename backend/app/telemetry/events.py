"""
Operational events for LiveOps timelines.

Expected event types:
- DEPLOYMENT
- SERVICE_RESTART
- FAILURE_INJECTED

Expected event fields:
- timestamp
- service
- event_type
- message
- request_id
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class EventType:
    DEPLOYMENT = "DEPLOYMENT"
    SERVICE_RESTART = "SERVICE_RESTART"
    FAILURE_INJECTED = "FAILURE_INJECTED"


@dataclass
class OperationalEvent:
    timestamp: datetime
    service: str
    event_type: str
    message: str
    request_id: Optional[str]


class EventRecorder:
    def deployment(self, service: str, message: str, request_id: Optional[str] = None):
        return OperationalEvent(
            timestamp=datetime.utcnow(),
            service=service,
            event_type=EventType.DEPLOYMENT,
            message=message,
            request_id=request_id,
        )

    def service_restart(self, service: str, message: str, request_id: Optional[str] = None):
        return OperationalEvent(
            timestamp=datetime.utcnow(),
            service=service,
            event_type=EventType.SERVICE_RESTART,
            message=message,
            request_id=request_id,
        )

    def failure_injected(self, service: str, message: str, request_id: Optional[str] = None):
        return OperationalEvent(
            timestamp=datetime.utcnow(),
            service=service,
            event_type=EventType.FAILURE_INJECTED,
            message=message,
            request_id=request_id,
        )
