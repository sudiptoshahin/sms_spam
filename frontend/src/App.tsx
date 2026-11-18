import { useEffect, useState } from "react";
import { predict, fetchReport } from "./api";
import type { HistoryItem, Prediction, ReportItem } from "./types";
import MessageInput from "./components/MessageInput";
import Verdict from "./components/Verdict";
import History from "./components/History";

export default function App() {
  const [text, setText] = useState("");
  const [checked, setChecked] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Prediction | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<ReportItem[]>([]);
  const isDemoMode = true;

  async function check(override?: string) {
    const message = (override ?? text).trim();
    if (!message) return;
    setLoading(true);
    setError(null);
    try {
      const r = await predict(message);
      setResult(r);
      setChecked(message);
    } catch {
      setResult(null);
      setError("The model could not be reached. Check that your API is running, then try again.");
    } finally {
      setLoading(false);
    }
  }

  async function getReports() {
    setLoading(true);
    setError(null);
    try {
      const data: ReportList = await fetchReport();
      setHistory(data.reports);
    } catch {
      setResult(null);
      setError("The model could not be reached. Check that your API is running, then try again.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    getReports();
  }, [result]);

  return (
    <main>
      <h1>Spam or ham?</h1>
      <p className="lede">Paste any message and the model will sort it. Ham is a normal message you actually want.</p>
      <div className="grid">
        <MessageInput value={text} loading={loading} onChange={setText} onSubmit={check} />
        <Verdict result={result} text={checked} error={error} />
      </div>
      <History items={history} />
      <p className="note">Results come from a trained LSTM model with the API.</p>
    </main>
  );
}
