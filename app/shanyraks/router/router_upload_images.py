from fastapi import Depends, Response, UploadFile
from typing import List

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.post("/{id}/media", status_code=200)
def upload_images(
    input: List[UploadFile],
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    for image in input:
        svc.s3_service.upload_file(image.file, image.filename)
        svc.repository.upload_images(
            id=id, user_id=jwt_data.user_id, image_filename=image.filename
        )
    return Response(status_code=200)
