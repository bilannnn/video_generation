from fastapi import UploadFile, File
from pydantic import BaseModel


class ShortVideoRequestSchema(BaseModel):
    images: list[UploadFile] = File(...)
    full_video_duration: int
