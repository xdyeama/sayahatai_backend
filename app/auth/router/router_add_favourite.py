from fastapi import Depends, Response


from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from app.shanyraks.service import Service as Service1
from app.shanyraks.service import get_service as get_service1


@router.post("/users/favourites/shanyraks/{id}", status_code=200)
def add_favourite(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    auth_svc: Service = Depends(get_service),
    shanyrak_svc: Service1 = Depends(get_service1),
) -> str:
    shanyrak = shanyrak_svc.repository.get_shanyrak_by_id(id=id)
    auth_svc.repository.add_to_favourites(user_id=jwt_data.user_id, shanyrak=shanyrak)

    return Response(status_code=200)
