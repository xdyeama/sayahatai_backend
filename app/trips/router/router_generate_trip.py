from fastapi import Depends, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GenerateTripRequest(AppModel):
    cities: str
    num_days: int
    travel_style: str


class GenerateTripResponse(AppModel):
    trip: str


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=GenerateTripResponse
)
def generateTrip(
    input: GenerateTripRequest,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    cities = input.dict()["cities"]
    num_days = str(input.dict()["num_days"])
    travel_style = input.dict()["travel_style"]

    response = svc.openai_service.generate_initial_plan(
        cities=cities, num_days=num_days, travel_style=travel_style
    )
    print(response)

    return {"trip": response}
