from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/token")
def get_token():
    raise NotImplementedError()
