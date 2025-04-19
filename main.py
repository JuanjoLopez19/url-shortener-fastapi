import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.app.api.index import router

app = FastAPI()

static_dir = os.path.join(
    os.path.dirname(__file__),
    "src",
    "static",
)

app.include_router(router)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


def main():
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
