from pydantic_settings import BaseSettings as _BaseSettings
import os

class Settings(_BaseSettings):
    shorts_video_limit: int = 59

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir: str = os.path.join(os.path.dirname(base_dir), 'static')

    base_api_path: str = "/api"
    title: str = "Video Generation Service"
