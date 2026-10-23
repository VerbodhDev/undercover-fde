import { useEffect, useState } from "react";
import { getInstructions } from "./api";

export function Instructions() {
  const [text, setText] = useState<string | null>(null);

  useEffect(() => {
    void getInstructions().then((loaded) => {
      setText(loaded.text);
    });
  }, []);

  return (
    <section className="stack">
      <h1>The agent's instructions</h1>
      <p className="muted">
        Read only. These are the instructions the agent works from.
      </p>
      <pre className="panel instructions">{text ?? "Loading"}</pre>
    </section>
  );
}
