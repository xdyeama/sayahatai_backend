from typing import Any

from fastapi import Depends, status
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from .dependencies import parse_jwt_user_data
from . import router


class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateShanyrakResponse,
)
def create_shanyrak(
    input: CreateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    response = svc.repository.create_shanyrak(
        user_id=jwt_data.user_id,
        shanyrak_data=input.dict(),
    )

    return CreateShanyrakResponse(id=response)

