from sqlalchemy.orm import Session

from app.database.models import Incident, MetricRecord
from app.detection.thresholds import (
    DB_CONNECTIONS_THRESHOLD,
    ERROR_RATE_THRESHOLD,
    LATENCY_P95_THRESHOLD_MS,
)
from app.telemetry.metrics import MetricName


def detect_incidents(db: Session) -> list[Incident]:
    latest_metrics = {}
    for metric_name in (
        MetricName.ERROR_RATE,
        MetricName.LATENCY,
        MetricName.DB_CONNECTIONS,
    ):
        latest_metric = (
            db.query(MetricRecord)
            .filter(MetricRecord.name == metric_name)
            .order_by(MetricRecord.timestamp.desc())
            .first()
        )
        if latest_metric:
            latest_metrics[metric_name] = latest_metric
    list_incidents = []

    error_rate_metric = latest_metrics.get(MetricName.ERROR_RATE)
    if error_rate_metric and error_rate_metric.value > ERROR_RATE_THRESHOLD:
        list_incidents.append(
            Incident(
                timestamp=error_rate_metric.timestamp,
                service=error_rate_metric.service,
                incident_type=error_rate_metric.name,
                severity="high",
                message="Error rate exceeded threshold",
                status="open",
                metric_value=error_rate_metric.value,
                threshold=ERROR_RATE_THRESHOLD,
            )
        )

    latency_metric = latest_metrics.get(MetricName.LATENCY)
    if latency_metric and latency_metric.value > LATENCY_P95_THRESHOLD_MS:
        list_incidents.append(
            Incident(
                timestamp=latency_metric.timestamp,
                service=latency_metric.service,
                incident_type=latency_metric.name,
                severity="high",
                message="Latency p95 exceeded threshold",
                status="open",
                metric_value=latency_metric.value,
                threshold=LATENCY_P95_THRESHOLD_MS,
            )
        )

    db_connections_metric = latest_metrics.get(MetricName.DB_CONNECTIONS)
    if (
        db_connections_metric
        and db_connections_metric.value > DB_CONNECTIONS_THRESHOLD
    ):
        list_incidents.append(
            Incident(
                timestamp=db_connections_metric.timestamp,
                service=db_connections_metric.service,
                incident_type=db_connections_metric.name,
                severity="critical",
                message="Database connections exceeded threshold",
                status="open",
                metric_value=db_connections_metric.value,
                threshold=DB_CONNECTIONS_THRESHOLD,
            )
        )

    if list_incidents:
        db.add_all(list_incidents)
        db.commit()
        for incident in list_incidents:
            db.refresh(incident)

    return list_incidents
