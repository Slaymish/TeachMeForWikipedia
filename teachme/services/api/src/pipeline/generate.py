from ..models.schemas import Archetype, LessonResponse, Level


def make_lesson(context: list[str], archetype: Archetype, level: Level, rubric_version: str) -> LessonResponse:
    # Placeholder generator that echoes the context
    lesson_markdown = "\n".join(context[:1])
    return LessonResponse(
        meta={
            "title": "Unknown Article",
            "lang": "en",
            "revision_id": 0,
            "archetype": archetype,
            "level": level,
            "section": None,
            "rubric_version": rubric_version,
        },
        claims=[],
        lesson_markdown=lesson_markdown,
        diagram_brief=None,
        worked_example_markdown=None,
        checks=[],
        disclaimer="Derived from Wikipedia, CC BY-SA 4.0.",
    )
