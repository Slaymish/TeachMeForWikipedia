TeachMe for Wikipedia

A browser button that turns any Wikipedia article or section into a tailored mini-lesson, anchored to the exact revision, with levels that adapt to the reader.

⸻

1. Goals
	•	Teach concepts, not just list facts.
	•	Adapt to reader level in under 30 seconds.
	•	Ground every sentence in a specific Wikipedia revision.
	•	Cache by revision and level for fast reuse.
	•	Respect licences and attributions by default.

⸻

2. Scope (MVP)
	•	Platforms: Chrome and Edge extension, simple web viewer.
	•	Languages: English Wikipedia to start.
	•	Page coverage: four archetypes
	•	Concept or method
	•	Person
	•	Country or place
	•	Philosophy or theory

⸻

3. User Flow (MVP)
	1.	User opens a Wikipedia page and clicks Teach me.
	2.	Extension reads article title, language, section anchor, and revision ID.
	3.	User answers a 3–5 item placement quiz, then picks “focus” if needed.
	4.	Backend fetches that revision content, runs a levelled lesson template, returns a mini-lesson with inline citations and a worked micro-example.
	5.	User can reveal deeper rungs, upvote or downvote, and compare with the source.

⸻

4. Archetype Routing

Detect via infobox name, categories, and lead paragraph cues.
	•	Concept or method: DFT, transformers, normalising flows, PCR.
Headings: Big picture, Minimal formalism, Worked micro-example, Failure modes, Next steps.
	•	Person: Ada Lovelace, Galois.
Headings: Why they matter, Signature works, Timeline anchors, Influence map, Read them yourself.
	•	Country or place: New Zealand, Catalonia.
Headings: Where and who, How it is governed, How it makes a living, What is changing now, Compare nearby.
	•	Philosophy or theory: The Absurd, virtue ethics.
Headings: Question at stake, Core claim, Canonical passage, Arguments, Misreadings.

Fallback to the closest archetype if signals are weak.

⸻

5. Levels and Placement

Four levels: 0 lay reader, 1 first-year, 2 advanced undergrad, 3 specialist.
	•	Short quiz per archetype. Example for concepts:
“Can you explain complex rotation”, “Comfort with dot products”, “Seen sine and cosine in signals”.
	•	Level policies:
	•	L0: forbid symbols, require one picture or analogy.
	•	L1: at most one equation, one tiny example.
	•	L2: careful definitions, two equations, algorithm steps.
	•	L3: formal statement with assumptions, edge cases, and brief proof sketch.

⸻

6. Output Contract

{
  "meta": {
    "title": "Discrete Fourier transform",
    "lang": "en",
    "revision_id": 123456789,
    "archetype": "concept",
    "level": 2,
    "section": "#Definition"
  },
  "claims": [
    {"text": "DFT expresses a vector as coordinates in a sinusoid basis.", "refs": ["rev:123456789#L110-L142"]}
  ],
  "lesson_markdown": "...",
  "diagram_brief": "Plot eight complex phasors and show projection.",
  "worked_example_markdown": "...",
  "checks": [{"q": "What is orthogonality here", "a": "..."}, {"q": "Transfer question", "a": "..."}],
  "disclaimer": "Derived from Wikipedia, CC BY-SA 4.0."
}


⸻

7. Grounding and Guardrails
	•	Retrieval: use MediaWiki REST or Action API to fetch the exact revision HTML or wikitext.
	•	Chunking: section-first, keep citation markers and anchors.
	•	Generation: RAG with strict grounding to retrieved chunks. No external facts except general definitions.
	•	Guardrails: require a “facts used” list with refs, and refuse if the section is too sparse.
	•	For living people and companies, stick to claims present in that revision.

⸻

8. Caching

Key:

sha256(project, language, title, section, revision_id, archetype, level, rubric_version)

Invalidate on revision change or rubric update. Store 24 h minimum, or until a new revision exists.

⸻

9. Feedback and Learning
	•	Upvote or downvote all lessons.
	•	For 10 percent of requests, serve A or B prompt variants.
	•	Train a light preference model over features: archetype, level, section mix, prompt rubric, diagram type.
	•	Use a bandit to pick the best variant without drifting off-source.

⸻

10. Legal and Attribution
	•	Wikipedia text is CC BY-SA 4.0. Output is a derivative work.
	•	Show attribution: article title, exact revision link, and CC BY-SA 4.0 in footer.
	•	Images follow their own licences. Do not transform images unless the licence permits.
	•	Prefer API usage to scraping.

⸻

11. Architecture

Extension
	•	Manifest V3, adds a floating button on *.wikipedia.org.
	•	Sends {title, lang, section_anchor, revision_id, url} to backend.
	•	Receives lesson JSON, renders panel with level toggles and citations.

Backend
	•	REST API with FastAPI or Express.
	•	Retrieval: MediaWiki API client.
	•	Orchestration: RAG pipeline with policy checks and rubric prompts.
	•	Cache: Redis for hot entries, Postgres for persisted lessons and feedback.
	•	Optional queue: simple worker for cache warm and precompute popular pages.

Web viewer
	•	Minimal page to view a lesson by URL and revision for sharing.

⸻

12. Model Strategy
	•	Start with high-quality LLM in grounded RAG mode.
	•	Use structured prompt rubrics per archetype and level.
	•	Only fine-tune after you have several hundred curated pairs.
	•	No diffusion or flow matching required. This is controlled editing and curriculum design.

⸻

13. API Sketch

POST /v1/lesson
Body:
{
  "title": "Discrete Fourier transform",
  "lang": "en",
  "section": "#Definition",
  "revision_id": 123456789,
  "archetype_hint": "concept",   // optional
  "answers": {"q1": true, "q2": false, "q3": true} // placement
}

Response: Output Contract above

GET /v1/lesson/cache-key?...
GET /v1/lesson/:key
POST /v1/feedback { key, vote: "up" | "down", variant_id }


⸻

14. Prompt Rubric Snippets
	•	Concept L0: “Explain without symbols, one everyday analogy, 120–180 words, highlight one misuse to avoid, cite claims inline with [n] that map to refs.”
	•	Concept L2: “Introduce definition and two equations, one 8-point worked example, failure mode, cite inline [n].”
	•	Person L1: “Why they matter in 3 sentences, two works with year and one-line impact, four-event timeline.”
	•	Philosophy L3: “State the core argument in premise-conclusion form, list two rival readings, one canonical passage with citation anchor.”

⸻

15. Code Structure (monorepo)

teachme/
  apps/
    extension/
      src/
        content.ts
        injectButton.ts
        panel/App.tsx
        api.ts
      manifest.json
    web/
      pages/
        index.tsx
        [key].tsx
      lib/renderLesson.tsx
  services/
    api/
      src/
        main.py                  # FastAPI
        routes/lesson.py
        routes/feedback.py
        clients/mediawiki.py
        pipeline/retrieve.py
        pipeline/route_archetype.py
        pipeline/place.py
        pipeline/ground.py
        pipeline/generate.py
        pipeline/validate.py
        cache/redis_cache.py
        store/postgres.py
        models/schemas.py        # Pydantic models for Output Contract
      pyproject.toml
    worker/
      src/worker.py              # cache warm, A/B scheduling
  packages/
    shared/
      src/types.ts               # TS types that mirror schemas.py
      src/archetypes.ts
      src/levels.ts
  infra/
    docker-compose.yml           # api, redis, postgres
    migrations/
  README.md


⸻

16. Key Functions (pseudocode)

# route_archetype.py
def classify_archetype(html, categories, infobox_name) -> Archetype:
    if infobox_name in {"Infobox person", "Infobox scientist"}: return "person"
    if infobox_name in {"Infobox country", "Infobox settlement"}: return "country"
    if "Category:Philosophical concepts" in categories: return "philosophy"
    return ml_backoff_or("concept")

# ground.py
def build_context(revision_html, section):
    chunks = chunk_by_section(revision_html, section)
    return ensure_citations(chunks)

# generate.py
def make_lesson(ctx, archetype, level, rubric_version):
    prompt = load_rubric(archetype, level, rubric_version)
    raw = llm.generate(prompt, context=ctx)
    return validate_and_attach_refs(raw, ctx)

# cache key
def cache_key(meta):
    s = f"{meta.lang}|{meta.title}|{meta.section}|{meta.revision_id}|{meta.archetype}|{meta.level}|{meta.rubric}"
    return sha256(s)


⸻

17. Testing
	•	Golden set of 20 pages across archetypes with fixed revision IDs.
	•	Assert every claim has a valid ref that points into the revision.
	•	Unit tests for archetype routing and level policies.
	•	Snapshot tests for lesson JSON.
	•	Manual checks for two living biographies to verify cautious behaviour.

⸻

18. Risks and Mitigations
	•	Hallucination: strict context injection and ref validation that fails closed.
	•	Messy pages: “best route to learn this” fallback with links to subsections.
	•	Licence drift: standardised footer with attribution and links.
	•	Out-of-date stats: always show year and the article’s cited source.

⸻

19. Build Order
	1.	Retrieval and revision anchoring.
	2.	Archetype routing and level placement.
	3.	Concept template end to end.
	4.	Person and philosophy templates.
	5.	Cache by revision and level.
	6.	Feedback and A or B serving.
	7.	Country template, then add 10 curated pages to shake out edge cases.

⸻

20. Tooling
	•	Extension: TypeScript, Vite, React.
	•	Backend: FastAPI, Pydantic, httpx.
	•	Storage: Postgres, Redis.
	•	Model: high-quality LLM via API, later fine-tuning optional.
	•	Tests: Pytest, Playwright for extension panel.
	•	Telemetry: OpenTelemetry?.

⸻

21. Definition of Done (MVP)
	•	Button appears on Wikipedia, returns a levelled lesson for four archetypes.
	•	Every claim in the lesson has a visible citation badge that maps to the exact revision.
	•	Cache hits on repeated requests for the same revision and level.
	•	Users can upvote or downvote.
	•	Footer shows full attribution and licence.
