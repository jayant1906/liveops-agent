from app.telemetry.events import EventRecorder
from app.telemetry.logger import StructuredLogger
from app.telemetry.metrics import MetricsCollector


logger = StructuredLogger()
event_recorder = EventRecorder()
metrics_collector = MetricsCollector()

def trigger_dependency_failure(request_id: str | None = None, dependency_name: str = "payment-provider") -> None:
    """Intentionally simulate a dependency outage."""
    try:
        raise ConnectionError(f"{dependency_name} unavailable")
    except ConnectionError as error:
        metrics_collector.record_error_rate(service="payment-service", value=100)
        logger.error(service="payment-service", message=f"Dependency failure injected: {error}",request_id=request_id)
        event_recorder.failure_injected(service="payment-service", message=f"Dependency failure injected: {dependency_name}", request_id=request_id)
