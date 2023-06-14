from fastapi import Depends, Response
from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.delete("/{id}/comments/{comment_id}", status_code=200)
def delete_comment(
    id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.delete_comment(
        id=id, comment_id=comment_id, user_id=jwt_data.user_id
    )
    return Response(status_code=200)
