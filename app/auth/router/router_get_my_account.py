from typing import Any

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetMyAccountResponse(AppModel):
    id: Any = Field(alias="_id")
    email: str = ""
    phone: str = ""
    name: str = ""
    city: str = ""
    avatar_url: str = ""


@router.get("/users/me", response_model=GetMyAccountResponse)
def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user = svc.repository.get_user_by_id(jwt_data.user_id)
    response = {
        "_id": user["_id"],
        "email": user["email"],
        "name": user["name"],
        "avatar_url": user["avatar_url"],
    }
    return response
