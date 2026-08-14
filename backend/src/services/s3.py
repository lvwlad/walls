from minio import Minio
import os, dotenv
import uuid
from io import BytesIO
from fastapi import UploadFile
import magic
from PIL import Image
import filetype

class InvalidMimeType(Exception):
    pass


dotenv.load_dotenv()
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
    "image/avif",
    "image/heic",
    "image/bmp",
    "image/tiff"
}

class S3Service():
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            access_key=os.getenv("MINIO_ROOT_USER"),
            secret_key=os.getenv('MINIO_ROOT_PASSWORD'),
            secure=False
        )
        self.bucket_name = "images"
        self.valid_types =  ALLOWED_IMAGE_TYPES

    async def convert_webp(self, content: bytes):
        file_obj = BytesIO(content)
        file_obj = Image.open(file_obj)
        file_webp = BytesIO()
        file_obj.save(file_webp, 'WEBP')
        kind = filetype.guess(file_webp)
        file_webp.seek(0)
        return file_webp, kind
        


    async def upload_image(self, file: UploadFile):
        header_bytes = await file.read(2048)
    
        await file.seek(0)
    
        # Определяем реальный MIME-тип по сигнатуре байтов
        detected_mime = magic.from_buffer(header_bytes, mime=True)
    
        if detected_mime not in self.valid_types:
            raise InvalidMimeType
        else:
            content = await file.read()
            
            file_webp, kind =  await self.convert_webp(content)
            unique_name = f"{uuid.uuid4()}.{kind.extension}"

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=unique_name,
                data=file_webp,
                length=len(file_webp.getbuffer()),
                content_type=kind.mime
            )
            
            # Возвращаем URL-строку
            return f"http://localhost:9000/{self.bucket_name}/{unique_name}"
            #return unique_name
        
s3 = S3Service()



