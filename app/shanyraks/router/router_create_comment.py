from fastapi import Depends, Response, status
from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class CreateCommentRequest(AppModel):
    content: str


@router.post("/{id}/comments", status_code=status.HTTP_201_CREATED)
def create_comment(
    id: str,
    input: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.create_comment_by_id(
        id=id, user_id=jwt_data.user_id, content=input.dict()
    )

    return Response(status_code=201)
