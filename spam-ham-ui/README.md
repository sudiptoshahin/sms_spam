# Spam or Ham UI

React + TypeScript + Vite interface for a spam/ham text classifier.

## Run the UI

    npm install
    npm run dev

Open http://localhost:5173. It starts in demo mode (simple keyword rules).

## Connect your model

1. Start the example backend (edit `server/app.py` to load your model):

       pip install flask flask-cors joblib scikit-learn
       python server/app.py

2. Set `VITE_API_URL=/predict` in `.env` and restart `npm run dev`.

The UI sends `POST /predict` with `{"text": "..."}` and expects:

    { "label": "spam" | "ham", "confidence": 0.97, "words": ["free"] }

`words` is optional; when present, those words are highlighted in the message.

## Build for production

    npm run build

The static site is written to `dist/`.

## Structure

    src/App.tsx                 page state and layout
    src/api.ts                  model call and demo fallback
    src/components/             MessageInput, Verdict, History
    server/app.py               example Flask backend
