from app.telemetry.events import EventRecorder
from app.telemetry.logger import StructuredLogger
from app.telemetry.metrics import MetricsCollector

import time


logger = StructuredLogger()
event_recorder = EventRecorder()
metric_point = MetricsCollector()

def trigger_memory_leak(request_id: str | None = None, size_mb: int = 100, hold_seconds: int = 5) -> None:
    """Intentionally triggering a memory leak"""
    leaked_data = []
    try:
        leaked_data = allocate_in_chunks(size_mb)
        logger.error(service="Memory", message=f"Memory failure injected: memory leak", request_id=request_id)
        event_recorder.failure_injected(service= "Memory", message="FAILURE_INJECTED", request_id=request_id)
        metric_point.record_memory_usage(service="Memory", value=size_mb)
        time.sleep(hold_seconds)
    finally:
        leaked_data.clear()

def allocate_in_chunks(total_mb: int, chunk_mb: int = 10) -> list:
    chunks = []
    num_chunks = int(total_mb/chunk_mb)
    for _ in range(num_chunks):
        chunk = bytearray(chunk_mb * 1024 * 1024)
        chunks.append(chunk)
    return chunks