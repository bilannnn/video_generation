import datetime
import tempfile

from fastapi import APIRouter, UploadFile, File, Depends
from dependency_injector.wiring import Provide, inject
from app.domain.interfaces import GenerateShortsVideoUseCase
from fastapi.responses import StreamingResponse
router = APIRouter(
    prefix="/video",
)

@router.post(
    "/generate/shorts",
)
@inject
def generate_shorts_video(
        images: list[UploadFile] = File(...),
        full_video_duration: int = 55,
        use_case: GenerateShortsVideoUseCase = Depends(Provide["generate_shorts_video_use_case"],),
):
    video_clip = use_case(images, full_video_duration)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_filename = temp_file.name
        video_clip.write_videofile(temp_filename, fps=60, codec='libx264', audio_codec='aac')

    def file_stream():
        with open(temp_filename, "rb") as f:
            yield from f


    return StreamingResponse(file_stream(), media_type="video/mp4", headers={"Content-Disposition": f"attachment; filename=video_{datetime.datetime.now()}.mp4"},)