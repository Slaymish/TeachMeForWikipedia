from ..models.schemas import Archetype


def classify_archetype(html: str, categories: list[str], infobox_name: str | None) -> Archetype:
    if infobox_name in {"Infobox person", "Infobox scientist"}:
        return "person"
    if infobox_name in {"Infobox country", "Infobox settlement"}:
        return "country"
    if any(cat.startswith("Category:Philosophical") for cat in categories):
        return "philosophy"
    return "concept"
