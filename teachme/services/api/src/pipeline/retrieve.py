from ..clients.mediawiki import RevisionData, fetch_revision_html
from ..models.schemas import LessonRequest


async def retrieve_revision(request: LessonRequest) -> RevisionData:
    return await fetch_revision_html(request.title, request.revision_id, request.lang)
