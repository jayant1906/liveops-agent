from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import deployments, telemetry
from app.config.settings import get_settings
from app.database.connection import check_database_connection, create_database_tables
from app.services import order_service, payment_service, user_service


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Day 1 LiveOps backend with service and database connectivity.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    create_database_tables()


@app.get("/")
def root() -> dict[str, str]:
    return {"name": settings.app_name, "environment": settings.app_env}


@app.get("/health")
def health_check() -> dict[str, object]:
    return {
        "status": "ok",
        "database": check_database_connection(),
    }


app.include_router(user_service.router, prefix=settings.api_prefix)
app.include_router(order_service.router, prefix=settings.api_prefix)
app.include_router(payment_service.router, prefix=settings.api_prefix)
app.include_router(deployments.router, prefix=settings.api_prefix)
app.include_router(telemetry.router, prefix=settings.api_prefix)
