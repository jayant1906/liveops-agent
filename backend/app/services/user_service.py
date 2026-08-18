from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def list_users() -> dict[str, list[dict[str, str]]]:
    return {
        "users": [
            {"id": "user_001", "name": "Asha Sharma", "status": "active"},
            {"id": "user_002", "name": "Rohan Mehta", "status": "active"},
        ]
    }


@router.get("/{user_id}")
def get_user(user_id: str) -> dict[str, str]:
    return {"id": user_id, "name": "Demo User", "status": "active"}
