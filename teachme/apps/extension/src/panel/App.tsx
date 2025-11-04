import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { LessonResponse } from "@teachme/shared/types";
import { fetchLesson } from "../api";

type PanelState = "idle" | "loading" | "loaded" | "error";

const PANEL_ID = "teachme-lesson-panel";

const App: React.FC = () => {
  const [state, setState] = useState<PanelState>("idle");
  const [lesson, setLesson] = useState<LessonResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleLoad = async () => {
    setState("loading");
    setError(null);

    try {
      const response = await fetchLesson();
      setLesson(response);
      setState("loaded");
    } catch (err) {
      setState("error");
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  };

  return (
    <div className="teachme-panel">
      <h2>TeachMe Lesson</h2>
      {state === "idle" && <button onClick={handleLoad}>Load lesson</button>}
      {state === "loading" && <p>Preparing lesson…</p>}
      {state === "error" && <p role="alert">{error}</p>}
      {state === "loaded" && lesson && (
        <article>
          <header>
            <h3>{lesson.meta.title}</h3>
            <small>{`Level ${lesson.meta.level} · ${lesson.meta.archetype}`}</small>
          </header>
          <section dangerouslySetInnerHTML={{ __html: lesson.lesson_markdown }} />
        </article>
      )}
    </div>
  );
};

export function openLessonPanel(): void {
  let host = document.getElementById(PANEL_ID);
  if (!host) {
    host = document.createElement("div");
    host.id = PANEL_ID;
    document.body.appendChild(host);
  }

  const root = createRoot(host);
  root.render(<App />);
}

export default App;
