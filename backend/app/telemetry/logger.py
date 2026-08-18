"""
Structured application logging skeleton.

Expected log levels:
- INFO
- WARNING
- ERROR

Expected log fields:
- timestamp
- service
- message
- request_id
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class LogLevel:
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class StructuredLogEntry:
    timestamp: datetime
    service: str
    message: str
    request_id: Optional[str]
    level: str


class StructuredLogger:
    def info(self, service: str, message: str, request_id: Optional[str] = None):
        return StructuredLogEntry(
            timestamp=datetime.utcnow(),
            service=service,
            message=message,
            request_id=request_id,
            level=LogLevel.INFO,
        )

    def warning(self, service: str, message: str, request_id: Optional[str] = None):
        return StructuredLogEntry(
            timestamp=datetime.utcnow(),
            service=service,
            message=message,
            request_id=request_id,
            level=LogLevel.WARNING,
        )

    def error(self, service: str, message: str, request_id: Optional[str] = None):
        return StructuredLogEntry(
            timestamp=datetime.utcnow(),
            service=service,
            message=message,
            request_id=request_id,
            level=LogLevel.ERROR,
        )
