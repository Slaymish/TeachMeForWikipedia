import { openLessonPanel } from "./panel/App";

const BUTTON_ID = "teachme-wikipedia-button";

export function injectTeachMeButton(): void {
  if (document.getElementById(BUTTON_ID)) {
    return;
  }

  const firstHeading = document.getElementById("firstHeading");
  if (!firstHeading) {
    return;
  }

  const button = document.createElement("button");
  button.id = BUTTON_ID;
  button.textContent = "Teach me";
  button.style.marginLeft = "1rem";
  button.className = "vector-button";
  button.addEventListener("click", openLessonPanel);

  firstHeading.appendChild(button);
}
