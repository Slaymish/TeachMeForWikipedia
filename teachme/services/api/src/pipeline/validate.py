from ..models.schemas import LessonResponse


def validate_lesson(lesson: LessonResponse) -> None:
    if not lesson.cache_key:
        raise ValueError("Lesson cache key is missing")
    if not lesson.meta.title:
        raise ValueError("Lesson metadata is incomplete")
    if not lesson.lesson_markdown.strip():
        raise ValueError("Lesson content is empty")
