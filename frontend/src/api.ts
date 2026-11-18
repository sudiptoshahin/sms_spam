import type { Prediction } from "./types";
// const API_URL: string = import.meta.env.API_BASE_URL ?? "";
const API_URL: string = import.meta.env.VITE_API_BASE_URL ?? "";


export async function predict(message: string): Promise<Prediction> {
  console.log('____API_URL____', API_URL);
  const res = await fetch(`${API_URL}/detect`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) throw new Error(`Request failed with status ${res.status}`);
  const data = await res.json();
  return {
    label: String(data.label).toLowerCase() === "spam" ? "spam" : "ham",
    confidence: Number(data.percentage),
    words: Array.isArray(data.message) ? data.message : [],
  };
}


export async function fetchReport(): Promise<ReportList> {

  try {
    const res = await fetch(`${API_URL}/reports`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) throw new Error('Something went wrong!');
    const data = await res.json();
    return data.reports;
  } catch (err) {
    console.error('Something went wrong!\n', err);
  }

  return [] as ReportList
}

