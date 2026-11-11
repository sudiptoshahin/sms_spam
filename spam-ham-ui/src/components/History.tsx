import type { HistoryItem } from "../types";

export default function History({ items }: { items: HistoryItem[] }) {
  if (items.length === 0) return null;
  return (
    <section className="panel hist">
      <h2>Recent checks</h2>
      <ul>
        {items.map((h) => (
          <li key={h.id}>
            <span className={`tag ${h.label}`}>{h.label === "spam" ? "Spam" : "Ham"}</span>
            <span className="m">{h.text}</span>
            <em>{h.pct}%</em>
          </li>
        ))}
      </ul>
    </section>
  );
}
