from fastapi import APIRouter

from ..models.schemas import FeedbackRequest, FeedbackResponse
from ..store.postgres import store_feedback

router = APIRouter()


@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest) -> FeedbackResponse:
    await store_feedback(request)
    return FeedbackResponse(status="received")
