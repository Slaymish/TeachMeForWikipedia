from ..models.schemas import FeedbackRequest


async def store_feedback(feedback: FeedbackRequest) -> None:
    # Placeholder persistence
    _ = feedback.dict()
