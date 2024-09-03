from fastapi import FastAPI

from app.containers import bootstrap


def build_app() -> FastAPI:
    container = bootstrap(
        init_resources=True,
    )

    return container.fastapi_app()
