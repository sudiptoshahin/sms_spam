import type { Prediction } from "../types";

interface Props {
  result: Prediction | null;
  text: string;
  error: string | null;
}

function Highlighted({ text, words }: { text: string; words: string[] }) {
  const escaped = words.map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const re = new RegExp(`(${escaped.join("|")})`, "gi");
  return (
    <p>
      {text.split(re).map((part, i) => (i % 2 === 1 ? <mark key={i}>{part}</mark> : part))}
    </p>
  );
}

export default function Verdict({ result, text, error }: Props) {
  return (
    <section className="panel verdict" aria-live="polite">
      {error && <p className="empty">{error}</p>}
      {!error && !result && (
        <p className="empty">Your verdict will appear here after you check a message.</p>
      )}
      {!error && result && (() => {
        const isSpam = result.label === "spam";
        const pct = Math.round(result.confidence * 100);
        const spamPct = isSpam ? pct : 100 - pct;
        return (
          <>
            {/* key restarts the stamp animation on every new result */}
            <div key={`${result.label}-${pct}-${text.length}`} className={`stamp ${result.label} drop`} role="img" aria-label={isSpam ? "Spam" : "Ham"}>
              <b>{isSpam ? "SPAM" : "HAM"}</b>
            </div>
            <p className="say">{isSpam ? "This looks like spam" : "This looks like a normal message"}</p>
            <p className="sub">{pct}% confident</p>
            <div className="meter">
              <div className="top"><span>Ham {100 - spamPct}%</span><span>Spam {spamPct}%</span></div>
              <div className="bar" aria-hidden="true">
                <i className="h" style={{ width: `${100 - spamPct}%` }} />
                <i className="s" style={{ width: `${spamPct}%` }} />
              </div>
            </div>
            {result.words.length > 0 && (
              <div className="flag">
                <h2>Suspicious words found</h2>
                <Highlighted text={text} words={result.words} />
              </div>
            )}
          </>
        );
      })()}
    </section>
  );
}
