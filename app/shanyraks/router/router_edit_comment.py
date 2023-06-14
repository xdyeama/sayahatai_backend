from fastapi import Depends, Response
from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class EditCommentRequest(AppModel):
    content: str


@router.patch("/{id}/comments/{comment_id}", status_code=200)
def edit_comment(
    input: EditCommentRequest,
    id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.edit_comment(
        id=id, comment_id=comment_id, user_id=jwt_data.user_id, comment=input.dict()
    )
    return Response(status_code=200)
