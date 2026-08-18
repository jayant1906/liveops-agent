from fastapi import APIRouter


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
def list_orders() -> dict[str, list[dict[str, str]]]:
    return {
        "orders": [
            {"id": "order_001", "user_id": "user_001", "status": "created"},
            {"id": "order_002", "user_id": "user_002", "status": "paid"},
        ]
    }


@router.get("/{order_id}")
def get_order(order_id: str) -> dict[str, str]:
    return {"id": order_id, "status": "processing"}
