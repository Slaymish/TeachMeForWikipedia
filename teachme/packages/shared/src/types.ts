export type Archetype = "concept" | "person" | "country" | "philosophy";
export type Level = "l0" | "l1" | "l2" | "l3";

export interface LessonMeta {
  title: string;
  lang: string;
  revision_id: number;
  archetype: Archetype;
  level: Level;
  section: string | null;
  rubric_version: string;
}

export interface Claim {
  text: string;
  refs: string[];
}

export interface Check {
  q: string;
  a: string;
}

export interface LessonResponse {
  meta: LessonMeta;
  claims: Claim[];
  lesson_markdown: string;
  diagram_brief: string | null;
  worked_example_markdown: string | null;
  checks: Check[];
  disclaimer: string;
}

export interface LessonRequestPayload {
  title: string;
  lang: string;
  revision_id?: number;
  section?: string;
  level: Level;
}

export interface FeedbackPayload {
  lesson_cache_key: string;
  rating: "up" | "down";
  comment?: string;
}
