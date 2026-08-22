from app.telemetry.events import EventRecorder
from app.telemetry.logger import StructuredLogger
from app.telemetry.metrics import MetricsCollector


logger = StructuredLogger()
event_recorder = EventRecorder()
metrics_collector = MetricsCollector()

def trigger_bad_deployment(request_id: str | None = None, version: str = "v-bad") -> None:
    """Intentionally simulate a bad deployment"""

    event_recorder.deployment(
        service="Application",
        message=f"Deployed version {version}",
        request_id=request_id,
    )
    metrics_collector.record_error_rate(service="Application", value=100)
    logger.error(
        service="Application",
        message=f"Bad deployment injected: version {version} is causing errors",
        request_id=request_id,
    )
    event_recorder.failure_injected(
        service="Application",
        message=f"Bad deployment injected: {version}",
        request_id=request_id,
    )
