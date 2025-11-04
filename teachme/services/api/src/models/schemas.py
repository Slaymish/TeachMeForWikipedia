from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

Archetype = Literal["concept", "person", "country", "philosophy"]
Level = Literal["l0", "l1", "l2", "l3"]


class LessonMeta(BaseModel):
    title: str
    lang: str
    revision_id: int
    archetype: Archetype
    level: Level
    section: Optional[str]
    rubric_version: str


class Claim(BaseModel):
    text: str
    refs: list[str]


class Check(BaseModel):
    q: str
    a: str


class LessonResponse(BaseModel):
    meta: LessonMeta
    claims: list[Claim]
    lesson_markdown: str
    diagram_brief: Optional[str]
    worked_example_markdown: Optional[str]
    checks: list[Check]
    disclaimer: str


class LessonRequest(BaseModel):
    title: str
    lang: str
    revision_id: Optional[int]
    section: Optional[str]
    level: Level = Field(default="l1")
    level_hint: Optional[Level] = None
    archetype_hint: Optional[Archetype] = None
    rubric_version: str = "v0"


class FeedbackRequest(BaseModel):
    lesson_cache_key: str
    rating: Literal["up", "down"]
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    status: str
