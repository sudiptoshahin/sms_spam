import type { Prediction } from "./types";

const API_URL: string = import.meta.env.VITE_API_URL ?? "";

const SPAM_WORDS = [
  "free", "winner", "won", "prize", "claim", "urgent", "limited", "offer",
  "click", "cash", "call now", "congratulations", "password", "verify",
  "suspended", "£", "$", "guaranteed", "bonus", "selected", "http",
];

/** Simple keyword rules so the UI works before your model is connected. */
function demoPredict(text: string): Prediction {
  const lower = text.toLowerCase();
  const hits = SPAM_WORDS.filter((w) => lower.includes(w));
  const caps = (text.match(/[A-Z]{4,}/g) ?? []).length;
  const bangs = Math.min((text.match(/!/g) ?? []).length, 3);
  const digits = (text.match(/\d{4,}/g) ?? []).length;
  const score = hits.length * 1.1 + caps * 0.8 + bangs * 0.5 + digits * 0.8 - 1.6;
  const pSpam = 1 / (1 + Math.exp(-score));
  const isSpam = pSpam >= 0.5;
  return {
    label: isSpam ? "spam" : "ham",
    confidence: isSpam ? pSpam : 1 - pSpam,
    words: hits,
  };
}

/**
 * Calls your model. Expected response from POST {API_URL}:
 *   { "label": "spam" | "ham", "confidence": 0.97, "words": ["free"] }
 * "words" is optional.
 */
export async function predict(text: string): Promise<Prediction> {
  if (!API_URL) return demoPredict(text);

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error(`Request failed with status ${res.status}`);
  const data = await res.json();
  return {
    label: String(data.label).toLowerCase() === "spam" ? "spam" : "ham",
    confidence: Number(data.confidence),
    words: Array.isArray(data.words) ? data.words : [],
  };
}

export const isDemoMode = !API_URL;
