import React from "react";
import Link from "next/link";

const HomePage: React.FC = () => (
  <main>
    <h1>TeachMe Lesson Viewer</h1>
    <p>Enter a cache key to load a previously generated lesson.</p>
    <form action="/[key]">
      <label htmlFor="cache-key">Cache key</label>
      <input id="cache-key" name="key" placeholder="sha256(...)" />
      <button type="submit">Open lesson</button>
    </form>
    <p>
      or browse a sample: <Link href="/sample">Sample lesson</Link>
    </p>
  </main>
);

export default HomePage;
