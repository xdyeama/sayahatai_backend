from typing import Any

from fastapi import Depends, status
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from .dependencies import parse_jwt_user_data
from . import router


class CreateTripRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateTripResponse(AppModel):
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
    coordinates = svc.here_service.get_location(input.dict()["address"])[
        "items"
    ][0]["position"]
    new_shanyrak_id = svc.repository.create_shanyrak(
        user_id=jwt_data.user_id, shanyrak=input.dict(), coordinates=coordinates
    )
    return CreateShanyrakResponse(id=str(new_shanyrak_id))
