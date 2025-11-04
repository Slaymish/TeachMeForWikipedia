import { LessonRequestPayload, LessonResponse, Level } from "@teachme/shared/types";

declare const mw: undefined | { config: { get(key: string): unknown } };

const DEFAULT_LEVEL: Level = "l1";
const DEFAULT_RUBRIC_VERSION = "v0";
const globalConfig = globalThis as typeof globalThis & Record<string, unknown>;
const API_BASE: string =
  (globalConfig.TEACHME_API_BASE_URL as string | undefined) ?? "http://localhost:8000";

function getMwValue<T>(key: string): T | undefined {
  if (typeof mw === "object" && typeof mw?.config?.get === "function") {
    return mw.config.get(key) as T | undefined;
  }
  return undefined;
}

function normaliseTitle(rawTitle: string | undefined): string {
  if (!rawTitle) return "";
  return rawTitle.replace(/_/g, " ").trim();
}

function resolveSectionAnchor(): string | undefined {
  const hash = window.location.hash;
  if (!hash) return undefined;
  try {
    const decoded = decodeURIComponent(hash);
    return decoded.startsWith("#") ? decoded : `#${decoded}`;
  } catch (error) {
    console.warn("TeachMe: unable to decode section anchor", error);
    return hash;
  }
}

function buildLessonRequest(): LessonRequestPayload {
  const title = normaliseTitle(
    getMwValue<string>("wgTitle") ?? document.getElementById("firstHeading")?.textContent ?? "",
  );
  const revisionId = getMwValue<number>("wgCurRevisionId");
  const lang =
    getMwValue<string>("wgContentLanguage") ?? document.documentElement.lang?.trim() ?? "en";

  const payload: LessonRequestPayload = {
    title,
    lang,
    revision_id: typeof revisionId === "number" && revisionId > 0 ? revisionId : undefined,
    section: resolveSectionAnchor(),
    level: DEFAULT_LEVEL,
    rubric_version: DEFAULT_RUBRIC_VERSION,
  };

  return payload;
}

export async function fetchLesson(): Promise<LessonResponse> {
  const payload = buildLessonRequest();
  const url = new URL("/lesson", API_BASE).toString();
  const response = await fetch(url, {
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
