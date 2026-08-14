from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import Response

from services.s3 import InvalidMimeType, s3
from services.users import get_current_user_id

router = APIRouter(prefix="/api", tags=["uploads"])


@router.post("/uploads/images")
async def upload_image(
    response: Response,
    file: UploadFile,
    _: int = Depends(get_current_user_id),
):
    try:
        url = await s3.upload_image(file)
    except InvalidMimeType:
        response.status_code = 415
        return {"message": "Неверный формат файла"}
    return url
