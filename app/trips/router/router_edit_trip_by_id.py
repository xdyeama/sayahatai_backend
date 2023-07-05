from fastapi import Depends, status, Response

from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

import json


class EditTripRequest(AppModel):
    num_day: int
    prev_city: str
    new_city: str
    travel_style: str


@router.put(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    # response_model=EditTripResponse,
)
def edit_trip_by_id(
    id: str,
    input: EditTripRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    trip = svc.repository.get_trip_by_id(user_id=jwt_data.user_id, trip_id=id)
    response = svc.openai_service.edit_plan(
        tour_plan=json.dumps(
            {"_id": str(trip["_id"]), "user_id": str("user_id"), "trip": trip["trip"]}
        ),
        num_day=input.dict()["num_day"],
        prev_city=input.dict()["prev_city"],
        new_city=input.dict()["new_city"],
        travel_style=input.dict()["travel_style"],
    )
    trip_json = json.loads(response[: len(response) // 2])
    svc.repository.edit_trip(
        user_id=jwt_data.user_id, trip_id=id, input=trip_json
    )
    return Response(status_code=200)
