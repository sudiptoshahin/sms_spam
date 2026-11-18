export type Label = "spam" | "ham";

export interface Prediction {
  label: Label;
  confidence: number;
  words: string[];
}

export interface HistoryItem {
  id: number;
  text: string;
  label: Label;
  pct: number;
}

export interface ReportItem {
  id: string;
  label: string;
  message: string;
  percentage: number;
  created_at: string;
}

export interface ReportList {
  reports: Array<ReportItem>
  total: number;
}

