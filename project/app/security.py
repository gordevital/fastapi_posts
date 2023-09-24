from typing import Annotated

from app.config import username, password
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def authorize(security: Annotated[HTTPBasicCredentials, Depends(security)]):
    if security.username == username and security.password == password:
        return {
            "username": security.username,
            "auth": True
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "username": security.username,
                "auth": False
            },
            headers={"WWW-Authenticate": "Basic"},
        )
