import json
from typing import Any

from ..models.schemas import LessonRequest, LessonResponse


async def get_cached_lesson(request: LessonRequest) -> LessonResponse | None:
    # Placeholder cache lookup
    return None


async def cache_lesson(lesson: LessonResponse) -> None:
    # Placeholder cache write
    _ = json.dumps(lesson.model_dump())
