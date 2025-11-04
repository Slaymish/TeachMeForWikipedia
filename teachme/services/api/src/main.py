from fastapi import FastAPI

from .routes import lesson, feedback

app = FastAPI(title="TeachMe API")

app.include_router(lesson.router, prefix="/lesson", tags=["lesson"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
