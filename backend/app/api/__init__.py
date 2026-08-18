"""
API package for LiveOps backend routes.

Planned route modules:
- incidents
- telemetry
- remediation
- deployments
"""

from app.api import deployments, incidents, remediation, telemetry


class ApiRouterRegistry:
    incidents = incidents
    telemetry = telemetry
    remediation = remediation
    deployments = deployments

    telemetry_router = telemetry.router


__all__ = [
    "ApiRouterRegistry",
    "deployments",
    "incidents",
    "remediation",
    "telemetry",
]
