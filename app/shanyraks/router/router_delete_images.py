from fastapi import Depends, Response, UploadFile
from typing import List
from app.utils import AppModel


from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data

import re


class DeleteImagesResponse(AppModel):
    media: List[str]


@router.delete("/{id}/media", status_code=200)
def delete_images(
    input: DeleteImagesResponse,
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    pattern = re.compile("/*.png")
    for image in input:
        svc.s3_service.delete_file(image)
        svc.repository.delete_images(
            id=id, user_id=jwt_data.user_id, media=input.dict()
        )
    return Response(status_code=200)
