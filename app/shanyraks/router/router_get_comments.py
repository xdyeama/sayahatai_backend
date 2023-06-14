from fastapi import Depends
from typing import Any
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CommentItem(AppModel):
    id: str
    content: str
    created_at: str
    author_id: str


class GetCommentsResponse(AppModel):
    comments: Any


@router.get("/{id}/comments", status_code=200, response_model=GetCommentsResponse)
def get_comments(id: str, svc: Service = Depends(get_service)):
    comments = svc.repository.get_comments(id)

    return {"comments": comments}
