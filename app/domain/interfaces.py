from abc import ABC, abstractmethod
from tempfile import SpooledTemporaryFile
from typing import Any, Protocol

from moviepy.video import VideoClip


class VideoBuilder(ABC):
    @abstractmethod
    def generate_zoom_video(self, image: SpooledTemporaryFile,
                            duration: int,
                            zoom_factor: float,
                            fps: int) -> VideoClip:
        """
        Build a video with zoom effect.
        Arguments:
            image: bytes of the image
            duration: video duration
            zoom_factor: zoom factor for the video
            fps: frames per second
        Return:
            VideoClip object
        """

    @abstractmethod
    def generate_movement_video(self, image: SpooledTemporaryFile,
                 duration: int,
                 zoom_factor: float,
                 fps: int) -> VideoClip:
        """
        Build a video with movement effect.
        Arguments:
            image: bytes of the image
            duration: video duration
            zoom_factor: zoom factor for the video
            fps: frames per second
        Return:
            VideoClip object
        """

    @abstractmethod
    def combine_videos(self, video_paths: list[str]) -> VideoClip:
        """
        Combine multiple videos into one.
        Arguments:
            video_paths: list of paths to the videos

        Return:
            VideoClip object
        """


class GenerateShortsVideoUseCase(Protocol):

    def __call__(self, images: list, full_video_duration: int) -> VideoClip:
        """
        Generate video based on images
        Arguments:
            images: list of images
            full_video_duration: duration of the full video
        Returns:
            VideoClip object
        """