from fastapi import APIRouter

from ..models.schemas import LessonRequest, LessonResponse
from ..pipeline.retrieve import retrieve_revision
from ..pipeline.route_archetype import classify_archetype
from ..pipeline.place import determine_level
from ..pipeline.ground import build_context
from ..pipeline.generate import make_lesson
from ..pipeline.validate import validate_lesson
from ..cache.redis_cache import cache_lesson, get_cached_lesson

router = APIRouter()


@router.post("/", response_model=LessonResponse)
async def create_lesson(request: LessonRequest) -> LessonResponse:
    cache_hit = await get_cached_lesson(request)
    if cache_hit:
        return cache_hit

    revision = await retrieve_revision(request)
    archetype = classify_archetype(revision.html, revision.categories, revision.infobox)
    level = determine_level(request.level_hint)
    context = build_context(revision.html, request.section)
    lesson = make_lesson(context, archetype, level, request.rubric_version)
    validate_lesson(lesson)
    await cache_lesson(lesson)
    return lesson
