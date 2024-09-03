import io
import random
from tempfile import SpooledTemporaryFile

import numpy as np
from moviepy.editor import *
from PIL import Image
import string
from app.domain.interfaces import VideoBuilder


class VideoBuilderImpl(VideoBuilder):
    def __init__(self, static_dir: str) -> None:
        self.static_dir = static_dir

    def generate_zoom_video(self, image: SpooledTemporaryFile,
                 duration: int,
                 zoom_factor: float,
                 fps: int) -> VideoClip:
        image.seek(0)
        image_bytes = image.read()
        image_stream = io.BytesIO(image_bytes)

        img = Image.open(image_stream)
        width, height = img.size

        def make_frame(t):
            scale = 1 + (zoom_factor - 1) * (t / duration)
            new_width = int(width * scale)
            new_height = int(height * scale)

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            x = (new_width - width) // 2
            y = (new_height - height) // 2
            cropped_img = resized_img.crop((x, y, x + width, y + height))

            return np.array(cropped_img)

        video = VideoClip(make_frame, duration=duration)

        return video

    def generate_movement_video(self, image: SpooledTemporaryFile,
                 duration: int,
                 zoom_factor: float,
                 fps: int) -> VideoClip:

        image.seek(0)
        image_bytes = image.read()
        image_stream = io.BytesIO(image_bytes)

        img = Image.open(image_stream)
        img_width, img_height = img.size

        new_width = int(img_width * zoom_factor)
        new_height = int(img_height * zoom_factor)

        img = img.resize((new_width, new_height), Image.LANCZOS)

        frames = []

        direction = random.choice(['left', 'right'])

        frames_per_second = fps

        for i in range(int(duration * frames_per_second)):
            if direction == 'left':
                offset_x = int((new_width - img_width) * (i % 150) / 150)
            else:
                offset_x = int((new_width - img_width) * (1 - (i % 150) / 150))

            offset_x = min(max(offset_x, 0), new_width - img_width)

            frame = img.crop((offset_x, 0, offset_x + img_width, img_height))

            frame_array = np.array(frame)
            frames.append(ImageClip(frame_array).set_duration(1 / fps))

            if (i + 1) % 150 == 0:
                direction = 'left' if direction == 'right' else 'right'

        video = concatenate_videoclips(frames, method="compose")

        return video

    def combine_videos(self, video_clips: list[VideoClip]) -> str:
        return concatenate_videoclips(video_clips, method="compose")

    @property
    def random_int_string(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))