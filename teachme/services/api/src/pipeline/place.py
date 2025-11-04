from typing import cast

from ..models.schemas import Level


LEVEL_ORDER: list[Level] = ["l0", "l1", "l2", "l3"]


def determine_level(selected: Level | None, level_hint: Level | None) -> Level:
    if selected in LEVEL_ORDER:
        return cast(Level, selected)
    if level_hint in LEVEL_ORDER:
        return cast(Level, level_hint)
    return "l1"
