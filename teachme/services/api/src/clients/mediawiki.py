from dataclasses import dataclass

import httpx


@dataclass
class RevisionData:
    html: str
    categories: list[str]
    infobox: str | None


async def fetch_revision_html(title: str, revision_id: int | None = None, lang: str = "en") -> RevisionData:
    base_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/html/{title}"
    params = {"redirect": "false"}
    if revision_id:
        params["oldid"] = revision_id

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        response.raise_for_status()
        html = response.text

    # Placeholder parsing
    return RevisionData(html=html, categories=[], infobox=None)
