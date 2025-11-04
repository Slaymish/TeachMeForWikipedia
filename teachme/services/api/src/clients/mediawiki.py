from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
from bs4 import BeautifulSoup


USER_AGENT = "TeachMeBot/0.1 (https://example.com; contact@example.com)"


@dataclass
class RevisionData:
    html: str
    categories: list[str]
    infobox: str | None
    title: str
    revision_id: int
    lang: str


async def fetch_revision_html(title: str, revision_id: int | None = None, lang: str = "en") -> RevisionData:
    api_url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "prop": "text|categories",
        "format": "json",
        "formatversion": "2",
        "redirects": "1",
    }
    if revision_id:
        params["oldid"] = revision_id

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(api_url, params=params, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        data: dict[str, Any] = response.json()

    parse = data.get("parse")
    if not parse:
        raise RuntimeError("MediaWiki response missing parse data")

    html: str = parse.get("text", "")
    if not html:
        raise RuntimeError("MediaWiki returned empty HTML for revision")

    categories = [entry.get("category", "") for entry in parse.get("categories", []) if entry.get("category")]
    resolved_revision_id = int(parse.get("revid") or revision_id or 0)
    resolved_title = parse.get("title", title)

    soup = BeautifulSoup(html, "html.parser")
    infobox_name: str | None = None
    infobox = soup.select_one("table.infobox")
    if infobox is not None:
        caption = infobox.find("caption")
        if caption and caption.get_text(strip=True):
            infobox_name = caption.get_text(strip=True)
        else:
            infobox_name = "infobox"

    return RevisionData(
        html=html,
        categories=categories,
        infobox=infobox_name,
        title=resolved_title,
        revision_id=resolved_revision_id,
        lang=lang,
    )
