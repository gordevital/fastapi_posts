from fastapi import APIRouter, Depends

from app.security import authorize

router = APIRouter()

@router.get("/users/me")
def read_current_user(credentials=Depends(authorize)):
    print(credentials)
    return credentials