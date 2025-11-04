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
        <p>
          Cache key: <code>{lesson.cache_key}</code>
        </p>
      </header>
      <section dangerouslySetInnerHTML={{ __html: lesson.lesson_markdown }} />
      {lesson.claims.length > 0 && (
        <section>
          <h3>Key claims</h3>
          <ol>
            {lesson.claims.map((claim) => (
              <li key={claim.text}>
                <p>{claim.text}</p>
                {claim.refs.length > 0 && <small>{claim.refs.join(", ")}</small>}
              </li>
            ))}
          </ol>
        </section>
      )}
      {lesson.checks.length > 0 && (
        <section>
          <h3>Quick checks</h3>
          <ul>
            {lesson.checks.map((check) => (
              <li key={check.q}>
                <strong>{check.q}</strong>
                <p>{check.a}</p>
              </li>
            ))}
          </ul>
        </section>
      )}
      <footer>
        <p>{lesson.disclaimer}</p>
      </footer>
    </article>
  );
}
