from collections.abc import Sequence


def build_context(revision_html: str, section: str | None) -> Sequence[str]:
    # Placeholder chunking logic
    if section:
        return [f"Section {section}", revision_html]
    return [revision_html]
