import { LessonRequestPayload, LessonResponse } from "@teachme/shared/types";

function buildLessonRequest(): LessonRequestPayload {
  const title = document.getElementById("firstHeading")?.textContent?.trim() ?? "";
  const revisionMeta = (window as any).wgCurRevisionId;
  const lang = document.documentElement.lang || "en";

  return {
    title,
    lang,
    revision_id: Number(revisionMeta) || undefined,
    section: window.location.hash || undefined,
    level: 1,
  };
}

export async function fetchLesson(): Promise<LessonResponse> {
  const payload = buildLessonRequest();
  const response = await fetch("https://api.teachme.local/lesson", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response.json();
}
