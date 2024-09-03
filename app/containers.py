
from dependency_injector.providers import (
    Configuration,
    Factory,
    Self,
)
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from fastapi import FastAPI

from app.application import make_fastapi_app
from app.domain.interfaces import VideoBuilder, GenerateShortsVideoUseCase
from app.domain.services import VideoBuilderImpl
from app.domain.use_cases import GenerateShortsVideoUseCaseImpl
from app.settings import Settings

WIRING_MODULES = [
 "app.views.routers.video",
]
class MainContainer(DeclarativeContainer):
    __self__ = Self()
    wiring_config = WiringConfiguration(modules=WIRING_MODULES)

    config: Configuration = Configuration()

    fastapi_app: Factory[FastAPI] = Factory(
        make_fastapi_app,
        title=config.title,
        base_api_path=config.base_api_path,
    )

    video_builder_service: Factory[VideoBuilder] = Factory(
        VideoBuilderImpl,
        static_dir=config.static_dir,
    )

    generate_shorts_video_use_case: Factory[GenerateShortsVideoUseCase] = Factory(
        GenerateShortsVideoUseCaseImpl,
        video_builder_service=video_builder_service,
    )




def bootstrap(init_resources: bool = False) -> MainContainer:
    container = MainContainer()
    settings = Settings()

    container.config.from_dict(settings.model_dump())

    if init_resources:
        container.init_resources()

    return container
