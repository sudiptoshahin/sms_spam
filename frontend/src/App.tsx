import { useState } from "react";
import { predict, isDemoMode } from "./api";
import type { HistoryItem, Prediction } from "./types";
import MessageInput from "./components/MessageInput";
import Verdict from "./components/Verdict";
import History from "./components/History";

export default function App() {
  const [text, setText] = useState("");
  const [checked, setChecked] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Prediction | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  async function check(override?: string) {
    const message = (override ?? text).trim();
    if (!message) return;
    setLoading(true);
    setError(null);
    try {
      const r = await predict(message);
      setResult(r);
      setChecked(message);
      setHistory((h) =>
        [{ id: Date.now(), text: message, label: r.label, pct: Math.round(r.confidence * 100) }, ...h].slice(0, 5)
      );
    } catch {
      setResult(null);
      setError("The model could not be reached. Check that your API is running, then try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>Spam or ham?</h1>
      <p className="lede">Paste any message and the model will sort it. Ham is a normal message you actually want.</p>
      <div className="grid">
        <MessageInput value={text} loading={loading} onChange={setText} onSubmit={check} />
        <Verdict result={result} text={checked} error={error} />
      </div>
      <History items={history} />
      {isDemoMode && (
        <p className="note">Demo mode: results come from a simple keyword rule, not your trained model yet.</p>
      )}
    </main>
  );
}
