from typing import List, Dict
from fastapi import Depends

from app.utils import AppModel


from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetFavouritesResponse(AppModel):
    shanyraks: List[Dict]


@router.get(
    "/users/favourites/shanyraks/",
    status_code=200,
    response_model=GetFavouritesResponse,
)
def get_favourites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> GetFavouritesResponse:
    favourites = svc.repository.get_favourites(user_id=jwt_data.user_id)

    return {"shanyraks": favourites}
