
from fastapi import FastAPI
from app.views.routers.video import router as video_router


def make_fastapi_app(
    title: str,
    base_api_path: str,
) -> FastAPI:
    app = FastAPI(
        title=title,
        openapi_url=f"{base_api_path}/docs/json/",
        docs_url=f"{base_api_path}/docs/swagger/",
        redoc_url=f"{base_api_path}/docs/redoc/",
    )

    app.include_router(video_router)

    return app
