from fastapi import Depends
from ..service import Service, get_service
from . import router
from pydantic import Field
from typing import Any, List, Dict
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


class GetTripByIdResponse(AppModel):
    id: Any = Field(alias="_id")
    user_id: str
    trip: List[Dict]


@router.get("/{id}", status_code=200, response_model=GetTripByIdResponse)
def get_trip_by_id(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    response = svc.repository.get_trip_by_id(user_id=jwt_data.user_id, trip_id=id)
    return GetTripByIdResponse(
        id=response["_id"], user_id=str(response["user_id"]), trip=response["trip"]
    )
