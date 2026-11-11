export type Label = "spam" | "ham";

export interface Prediction {
  label: Label;
  /** Confidence in the predicted label, 0 to 1. */
  confidence: number;
  /** Optional words that influenced the prediction. */
  words: string[];
}

export interface HistoryItem {
  id: number;
  text: string;
  label: Label;
  pct: number;
}
