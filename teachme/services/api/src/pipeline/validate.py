from ..models.schemas import LessonResponse


def validate_lesson(lesson: LessonResponse) -> None:
    if not lesson.lesson_markdown:
        raise ValueError("Lesson content is empty")
