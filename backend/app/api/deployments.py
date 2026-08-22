from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.failures import bad_deployment, database_failure, dependency_failure, memory_leak, slow_database


router = APIRouter(prefix="/failures", tags=["failures"])


class FailureRequest(BaseModel):
    request_id: Optional[str] = None


class SlowDatabaseFailureRequest(FailureRequest):
    delay_seconds: float = Field(default=5, gt=0)


class MemoryFailureRequest(FailureRequest):
    size_mb: int = Field(default=100, gt=0)
    hold_seconds: int = Field(default=5, ge=0)


class DependencyFailureRequest(FailureRequest):
    dependency_name: str = Field(default="payment-provider", min_length=1)


class BadDeploymentFailureRequest(FailureRequest):
    version: str = Field(default="v-bad", min_length=1)


@router.post("/database")
def trigger_database_failure(failure_request: FailureRequest):
    database_failure.trigger_database_failure(request_id=failure_request.request_id)
    return {"status": "failure_injected", "failure": "database"}


@router.post("/slow-db")
def trigger_slow_database_failure(failure_request: SlowDatabaseFailureRequest):
    slow_database.trigger_slow_database(
        request_id=failure_request.request_id,
        delay_seconds=failure_request.delay_seconds,
    )
    return {"status": "failure_injected", "failure": "slow_database"}


@router.post("/memory")
def trigger_memory_failure(failure_request: MemoryFailureRequest):
    memory_leak.trigger_memory_leak(
        request_id=failure_request.request_id,
        size_mb=failure_request.size_mb,
        hold_seconds=failure_request.hold_seconds,
    )
    return {"status": "failure_injected", "failure": "memory"}


@router.post("/dependency")
def trigger_dependency_failure(failure_request: DependencyFailureRequest):
    dependency_failure.trigger_dependency_failure(
        request_id=failure_request.request_id,
        dependency_name=failure_request.dependency_name,
    )
    return {"status": "failure_injected", "failure": "dependency"}


@router.post("/deployment")
def trigger_bad_deployment_failure(failure_request: BadDeploymentFailureRequest):
    bad_deployment.trigger_bad_deployment(
        request_id=failure_request.request_id,
        version=failure_request.version,
    )
    return {"status": "failure_injected", "failure": "bad_deployment"}
