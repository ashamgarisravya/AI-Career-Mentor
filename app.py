from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "AI Career Mentor Backend Running"}


def main() -> None:  # pragma: no cover
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
