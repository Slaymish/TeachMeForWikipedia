from __future__ import annotations

from hashlib import sha256

from ..models.schemas import LessonResponse

_CACHE: dict[str, LessonResponse] = {}
_PROJECT = "teachme"


def make_cache_key(
    *,
    lang: str,
    title: str,
    section: str | None,
    revision_id: int,
    archetype: str,
    level: str,
    rubric_version: str,
) -> str:
    components = [
        _PROJECT,
        lang.lower().strip(),
        title.lower().strip(),
        (section or "").lower().strip(),
        str(revision_id),
        archetype.lower().strip(),
        level.lower().strip(),
        rubric_version.lower().strip(),
    ]
    joined = "||".join(components)
    return sha256(joined.encode("utf-8")).hexdigest()


async def get_cached_lesson(cache_key: str) -> LessonResponse | None:
    return _CACHE.get(cache_key)


async def cache_lesson(cache_key: str, lesson: LessonResponse) -> None:
    _CACHE[cache_key] = lesson
