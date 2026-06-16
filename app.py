from os import getenv

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "AI Career Mentor Backend Running"}


def main() -> None:  # pragma: no cover
    import uvicorn

    uvicorn.run(
        "app:app",
        host=getenv("APP_HOST", "127.0.0.1"),
        port=int(getenv("APP_PORT", "8000")),
        reload=False,
    )
