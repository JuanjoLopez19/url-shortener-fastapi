import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.app import settings
from src.app.api.index import router
from src.app.database.mongo import mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb.initialize()
    yield
    await mongodb.close()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

static_dir = os.path.join(
    os.path.dirname(__file__),
    "src",
    "static",
)

app.include_router(router)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


def main():
    import uvicorn

    if settings.development:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
