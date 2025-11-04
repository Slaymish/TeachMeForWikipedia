from ..models.schemas import Level


LEVEL_ORDER: list[Level] = ["l0", "l1", "l2", "l3"]


def determine_level(level_hint: Level | None) -> Level:
    return level_hint or "l1"
