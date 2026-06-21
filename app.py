from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import careers, interview, profile, resume, roadmap

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(profile.router)
app.include_router(careers.router)
app.include_router(resume.router)
app.include_router(roadmap.router)
app.include_router(interview.router)


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
