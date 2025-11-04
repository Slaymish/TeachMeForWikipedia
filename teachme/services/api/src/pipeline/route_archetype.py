from ..models.schemas import Archetype


def classify_archetype(html: str, categories: list[str], infobox_name: str | None) -> Archetype:
    categories_lower = [cat.lower() for cat in categories]

    if infobox_name and "born" in infobox_name.lower():
        return "person"

    if any("births" in cat or "people" in cat or "scientists" in cat for cat in categories_lower):
        return "person"

    if any("countries" in cat or "states" in cat or "settlements" in cat for cat in categories_lower):
        return "country"

    if any("philosophy" in cat or "philosophers" in cat for cat in categories_lower):
        return "philosophy"

    if "infobox settlement" in html.lower():
        return "country"

    return "concept"
