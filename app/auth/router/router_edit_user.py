from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class EditUserRequest(AppModel):
    phone: str
    name: str
    city: str


@router.patch("/users/me", status_code=200)
def edit_user(
    input: EditUserRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> str:
    svc.repository.edit_user_by_id(jwt_data.user_id, input.dict())

    return Response(status_code=200)
