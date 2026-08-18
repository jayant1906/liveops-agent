from fastapi import APIRouter


router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/")
def list_payments() -> dict[str, list[dict[str, str]]]:
    return {
        "payments": [
            {"id": "payment_001", "order_id": "order_002", "status": "authorized"},
            {"id": "payment_002", "order_id": "order_003", "status": "pending"},
        ]
    }


@router.get("/{payment_id}")
def get_payment(payment_id: str) -> dict[str, str]:
    return {"id": payment_id, "status": "pending"}
