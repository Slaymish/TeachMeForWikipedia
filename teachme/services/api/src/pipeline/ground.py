from __future__ import annotations

from collections.abc import Sequence
from typing import Iterable

from bs4 import BeautifulSoup, Tag

MAX_PARAGRAPHS = 5


def _heading_level(tag: Tag | None) -> int:
    if tag and tag.name and tag.name.startswith("h") and tag.name[1:].isdigit():
        return int(tag.name[1:])
    return 7


def _collect_paragraphs(nodes: Iterable[Tag]) -> list[str]:
    paragraphs: list[str] = []
    for node in nodes:
        if node.name != "p":
            continue
        if not node.get_text(strip=True):
            continue
        paragraphs.append(str(node))
        if len(paragraphs) >= MAX_PARAGRAPHS:
            break
    return paragraphs


def build_context(revision_html: str, section: str | None) -> Sequence[str]:
    soup = BeautifulSoup(revision_html, "html.parser")
    target_paragraphs: list[str] = []

    if section:
        anchor = section.lstrip("#")
        heading = soup.find(id=anchor)
        if isinstance(heading, Tag):
            level = _heading_level(heading)
            siblings: list[Tag] = []
            for sibling in heading.next_siblings:
                if not isinstance(sibling, Tag):
                    continue
                if sibling.name and sibling.name.startswith("h") and _heading_level(sibling) <= level:
                    break
                siblings.append(sibling)
            target_paragraphs = _collect_paragraphs(siblings)

    if not target_paragraphs:
        parser_output = soup.select("div.mw-parser-output > p")
        target_paragraphs = _collect_paragraphs(parser_output)

    if not target_paragraphs and revision_html:
        return [revision_html]

    return target_paragraphs
