from __future__ import annotations

import re
from typing import Iterable

from bs4 import BeautifulSoup

from ..clients.mediawiki import RevisionData
from ..models.schemas import Archetype, Check, Claim, LessonMeta, LessonResponse, Level


def _paragraph_text(html_fragment: str) -> str:
    return BeautifulSoup(html_fragment, "html.parser").get_text(" ", strip=True)


def _collect_sentences(paragraphs: Iterable[str], limit: int = 3) -> list[str]:
    sentences: list[str] = []
    for html_fragment in paragraphs:
        text = _paragraph_text(html_fragment)
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            cleaned = sentence.strip()
            if cleaned:
                sentences.append(cleaned)
            if len(sentences) >= limit:
                return sentences
    return sentences


def make_lesson(
    context: list[str],
    revision: RevisionData,
    archetype: Archetype,
    level: Level,
    rubric_version: str,
    section: str | None,
    cache_key: str,
) -> LessonResponse:
    lesson_body = "".join(context) if context else "<p>No relevant content was found for this section.</p>"
    intro = (
        "<p>These highlights are extracted from the selected Wikipedia revision to keep the lesson grounded. "
        "Use the source link below to inspect the original context.</p>"
    )
    lesson_markdown = f"<div class=\"teachme-lesson\">{intro}<section>{lesson_body}</section></div>"

    claim_texts = _collect_sentences(context)
    claims = [Claim(text=text, refs=[f"rev:{revision.revision_id}"]) for text in claim_texts]

    checks: list[Check] = []
    if claims:
        checks.append(
            Check(
                q=f"Summarise one key idea about {revision.title}.",
                a=claims[0].text,
            )
        )
    checks.append(
        Check(
            q="Where did the information in this lesson come from?",
            a=f"Wikipedia article '{revision.title}' (revision {revision.revision_id}).",
        )
    )

    disclaimer = (
        "Derived from the Wikipedia article "
        f"<a href=\"https://{revision.lang}.wikipedia.org/w/index.php?oldid={revision.revision_id}\">{revision.title}</a> "
        "under CC BY-SA 4.0."
    )

    meta = LessonMeta(
        title=revision.title,
        lang=revision.lang,
        revision_id=revision.revision_id,
        archetype=archetype,
        level=level,
        section=section,
        rubric_version=rubric_version,
    )

    return LessonResponse(
        cache_key=cache_key,
        meta=meta,
        claims=claims,
        lesson_markdown=lesson_markdown,
        diagram_brief=None,
        worked_example_markdown=None,
        checks=checks,
        disclaimer=disclaimer,
    )
