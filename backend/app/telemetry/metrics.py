"""
Application metrics skeleton.

Expected metric categories:
- cpu_usage
- memory_usage
- latency
- error_rate
- throughput
- db_connections
- request_count

Expected metric fields:
- timestamp
- service
- name
- value
- unit
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MetricPoint:
    timestamp: datetime
    service: str
    name: str
    value: float
    unit: Optional[str]


class MetricName:
    LATENCY = "latency"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DB_CONNECTIONS = "db_connections"
    REQUEST_COUNT = "request_count"


class MetricsCollector:
    def record_latency(self, service: str, value: float) -> MetricPoint:
        return MetricPoint(
            timestamp=datetime.utcnow(),
            service=service,
            name=MetricName.LATENCY,
            value=value,
            unit="ms",
        )

    def record_error_rate(self, service: str, value: float) -> MetricPoint:
        return MetricPoint(
            timestamp=datetime.utcnow(),
            service=service,
            name=MetricName.ERROR_RATE,
            value=value,
            unit="percent",
        )

    def record_throughput(self, service: str, value: float) -> MetricPoint:
        return MetricPoint(
            timestamp=datetime.utcnow(),
            service=service,
            name=MetricName.THROUGHPUT,
            value=value,
            unit="requests_per_second",
        )

    def record_cpu_usage(self, service: str, value: float) -> MetricPoint:
        return MetricPoint(
            timestamp=datetime.utcnow(),
            service=service,
            name=MetricName.CPU_USAGE,
            value=value,
            unit="percent",
        )

    def record_memory_usage(self, service: str, value: float) -> MetricPoint:
        return MetricPoint(
            timestamp=datetime.utcnow(),
            service=service,
            name=MetricName.MEMORY_USAGE,
            value=value,
            unit="mb",
        )

    def record_db_connections(self, service: str, value: float) -> MetricPoint:
        return MetricPoint(
            timestamp=datetime.utcnow(),
            service=service,
            name=MetricName.DB_CONNECTIONS,
            value=value,
            unit="connections",
        )

    def record_request_count(self, service: str, value: float) -> MetricPoint:
        return MetricPoint(
            timestamp=datetime.utcnow(),
            service=service,
            name=MetricName.REQUEST_COUNT,
            value=value,
            unit="requests",
        )
