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
  const cacheKey = params?.key as string;
  // Placeholder: fetch from API cache endpoint
  const lesson: LessonResponse | null = null;

  return {
    props: {
      cacheKey,
      lesson,
    },
  };
};

export default LessonPage;
