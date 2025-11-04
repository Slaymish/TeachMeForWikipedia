from fastapi import APIRouter, HTTPException

from ..cache.redis_cache import cache_lesson, get_cached_lesson, make_cache_key
from ..models.schemas import LessonRequest, LessonResponse
from ..pipeline.generate import make_lesson
from ..pipeline.ground import build_context
from ..pipeline.place import determine_level
from ..pipeline.retrieve import retrieve_revision
from ..pipeline.route_archetype import classify_archetype
from ..pipeline.validate import validate_lesson

router = APIRouter()


@router.post("/", response_model=LessonResponse)
async def create_lesson(request: LessonRequest) -> LessonResponse:
    revision = await retrieve_revision(request)
    archetype = classify_archetype(
        revision.html,
        revision.categories,
        revision.infobox,
        archetype_hint=request.archetype_hint,
    )
    level = determine_level(request.level, request.level_hint)

    cache_key = make_cache_key(
        lang=request.lang,
        title=revision.title,
        section=request.section,
        revision_id=revision.revision_id,
        archetype=archetype,
        level=level,
        rubric_version=request.rubric_version,
    )

    cache_hit = await get_cached_lesson(cache_key)
    if cache_hit:
        return cache_hit

    context = build_context(revision.html, request.section)
    lesson = make_lesson(
        context=context,
        revision=revision,
        archetype=archetype,
        level=level,
        rubric_version=request.rubric_version,
        section=request.section,
        cache_key=cache_key,
    )
    validate_lesson(lesson)
    await cache_lesson(cache_key, lesson)
    return lesson


@router.get("/{cache_key}", response_model=LessonResponse)
async def read_lesson(cache_key: str) -> LessonResponse:
    lesson = await get_cached_lesson(cache_key)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson
