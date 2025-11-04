import React from "react";
import { GetServerSideProps } from "next";
import { renderLesson } from "../lib/renderLesson";
import { LessonResponse } from "@teachme/shared/types";

type LessonPageProps = {
  cacheKey: string;
  lesson: LessonResponse | null;
};

const LessonPage: React.FC<LessonPageProps> = ({ cacheKey, lesson }) => (
  <main>
    <h1>Lesson {cacheKey}</h1>
    {!lesson && <p>No cached lesson found.</p>}
    {lesson && renderLesson(lesson)}
  </main>
);

export const getServerSideProps: GetServerSideProps<LessonPageProps> = async ({ params }) => {
  const cacheKeyParam = params?.key;
  const cacheKey = typeof cacheKeyParam === "string" ? cacheKeyParam : Array.isArray(cacheKeyParam) ? cacheKeyParam[0] : "";
  let lesson: LessonResponse | null = null;

  if (cacheKey) {
    const baseUrl = process.env.TEACHME_API_BASE_URL ?? "http://localhost:8000";
    const url = `${baseUrl.replace(/\/$/, "")}/lesson/${encodeURIComponent(cacheKey)}`;
    try {
      const response = await fetch(url);
      if (response.ok) {
        lesson = (await response.json()) as LessonResponse;
      }
    } catch (error) {
      console.error("Failed to fetch lesson", error);
    }
  }

  return {
    props: {
      cacheKey,
      lesson,
    },
  };
};

export default LessonPage;
