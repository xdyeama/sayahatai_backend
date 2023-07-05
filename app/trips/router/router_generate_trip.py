import logging
from fastapi import Depends, status

from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

import json

logger = logging.getLogger(__name__)


class GenerateTripRequest(AppModel):
    cities: str
    num_days: int
    travel_style: str


class GenerateTripResponse(AppModel):
    trip_id: str


@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
    response_model=GenerateTripResponse,
)
def generate_trip(
    input: GenerateTripRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    cities = input.dict()["cities"]
    num_days = str(input.dict()["num_days"])
    travel_style = input.dict()["travel_style"]

    response = svc.openai_service.generate_initial_plan(
        cities=cities, num_days=num_days, travel_style=travel_style
    )
    # logger.info("Generated initial plan")
    # logger.info(response)
    # logger.info("Ended initial plan")
    resp_json = json.loads(response[: len(response) // 2])
    trip_id = svc.repository.create_trip(
        user_id=jwt_data.user_id, input=resp_json["trip"]
    )

    return GenerateTripResponse(trip_id=str(trip_id))
