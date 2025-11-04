import React from "react";
import { LessonResponse } from "@teachme/shared/types";

export function renderLesson(lesson: LessonResponse): React.ReactElement {
  return (
    <article>
      <header>
        <h2>{lesson.meta.title}</h2>
        <p>
          Level {lesson.meta.level} · {lesson.meta.archetype}
        </p>
        <p>
          Revision <a href={`https://en.wikipedia.org/w/index.php?oldid=${lesson.meta.revision_id}`}>{lesson.meta.revision_id}</a>
        </p>
      </header>
      <section dangerouslySetInnerHTML={{ __html: lesson.lesson_markdown }} />
    </article>
  );
}
