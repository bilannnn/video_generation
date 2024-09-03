from typing import Any
import random

from moviepy.video import VideoClip

from app.domain.interfaces import GenerateShortsVideoUseCase, VideoBuilder


class GenerateShortsVideoUseCaseImpl(GenerateShortsVideoUseCase):
    def __init__(self, video_builder_service: VideoBuilder):
        self.video_builder_service = video_builder_service


    def __call__(self, images: list, full_video_duration: int) -> VideoClip:
        raw_video_storage = []
        one_video_duration = full_video_duration / len(images)
        for image in images:
            image_path = image.file
            movement, kwargs = self._get_random_movement()
            raw_video_storage.append( movement(image_path, one_video_duration, **kwargs))

        return self.video_builder_service.combine_videos(raw_video_storage)


    def _get_random_movement(self) -> tuple[Any, dict[str, Any]]:
        mapping = {
            "movement": [self.video_builder_service.generate_movement_video, {"zoom_factor": 1.03, "fps": 60}],
            "zoom": [self.video_builder_service.generate_zoom_video, {"zoom_factor": 1.25, "fps": 60}]
        }
        return mapping[random.choice(list(mapping.keys()))]