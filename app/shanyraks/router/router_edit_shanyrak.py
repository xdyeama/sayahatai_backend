from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class EditShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{id}", status_code=200)
def edit_shanyrak(
    id: str,
    input: EditShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> str:
    svc.repository.edit_shanyrak_by_id(id=id,
                                       user_id=jwt_data.user_id,
                                       input=input.dict())
    return Response(status_code=200)

@router.delete("/{id}", status_code=200)
def delete_shanyrak(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.delete_shanyraq_by_id(id=id, user_id=jwt_data.user_id)

    return Response(status_code=200)
