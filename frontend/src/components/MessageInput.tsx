const SAMPLES = [
  { name: "Prize message", text: "WINNER!! You have been selected for a free £1000 prize. Claim now by calling 0900 123 4567 – limited time offer, urgent!" },
  { name: "Lunch plan", text: "Hey, are we still on for lunch tomorrow? I can book the place near the office if you like." },
  { name: "Account alert", text: "Your account is suspended. Verify your password at http://secure-login.example now to avoid cancellation." },
];

interface Props {
  value: string;
  loading: boolean;
  onChange: (v: string) => void;
  onSubmit: (text?: string) => void;
}

export default function MessageInput({ value, loading, onChange, onSubmit }: Props) {
  const count = value.trim() ? value.trim().split(/\s+/).length : 0;

  return (
    <section className="panel" aria-label="Message input">
      <label className="t" htmlFor="msg">Message to check</label>
      <textarea
        id="msg"
        value={value}
        placeholder="Paste an email or SMS here…"
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => {
          if ((e.ctrlKey || e.metaKey) && e.key === "Enter") onSubmit();
        }}
      />
      <div className="row">
        <span className="count">{count} {count === 1 ? "word" : "words"}</span>
        <div>
          <button type="button" onClick={() => onChange("")}>Clear</button>{" "}
          <button type="button" className="go" disabled={count === 0 || loading} onClick={() => onSubmit()}>
            {loading ? "Checking…" : "Check message"}
          </button>
        </div>
      </div>
      <div className="samples">
        <span>Try an example:</span>
        {SAMPLES.map((s) => (
          <button key={s.name} type="button" onClick={() => { onChange(s.text); onSubmit(s.text); }}>
            {s.name}
          </button>
        ))}
      </div>
    </section>
  );
}
