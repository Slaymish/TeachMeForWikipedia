import sys
import textwrap
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[4])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from teachme.services.api.src.pipeline.ground import build_context


def test_build_context_selects_section_paragraphs_when_anchor_is_nested_span():
    html = textwrap.dedent(
        """
        <div class="mw-parser-output">
          <p>Lead paragraph.</p>
          <h2><span class="mw-headline" id="History">History</span></h2>
          <p>First history paragraph.</p>
          <p>Second history paragraph.</p>
          <h2><span class="mw-headline" id="Legacy">Legacy</span></h2>
          <p>Legacy paragraph.</p>
        </div>
        """
    )

    context = build_context(html, "#History")

    assert context == ["<p>First history paragraph.</p>", "<p>Second history paragraph.</p>"]


def test_build_context_falls_back_to_whole_html_when_no_paragraphs_available():
    html = "<div><table id=\"History\"></table></div>"

    context = build_context(html, "#History")

    assert context == [html]
