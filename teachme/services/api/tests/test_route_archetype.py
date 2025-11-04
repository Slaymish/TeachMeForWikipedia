import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[4])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from teachme.services.api.src.pipeline.route_archetype import classify_archetype


def test_classify_archetype_prefers_hint():
    result = classify_archetype("", [], None, archetype_hint="philosophy")

    assert result == "philosophy"


def test_classify_archetype_retains_existing_logic_when_no_hint():
    html = "<table class=\"infobox\">Born in 1900</table>"
    result = classify_archetype(html, [], "born")

    assert result == "person"
