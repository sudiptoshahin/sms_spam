"""Example Flask backend for the Spam/Ham UI.

Install:  pip install flask flask-cors joblib scikit-learn
Run:      python server/app.py

Assumes you saved a scikit-learn Pipeline (vectorizer + classifier) with
joblib.dump(pipeline, "model.pkl"). If you use another framework, only the
two lines marked CHANGE ME need to be replaced.
"""
import joblib
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load("model.pkl")  # CHANGE ME: load your model


@app.post("/predict")
def predict():
    text = (request.get_json(silent=True) or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400

    probs = model.predict_proba([text])[0]  # CHANGE ME: your prediction call
    best = int(probs.argmax())
    name = str(model.classes_[best]).lower()
    is_spam = name in ("spam", "1", "true")

    return jsonify({
        "label": "spam" if is_spam else "ham",
        "confidence": float(probs[best]),
        "words": [],  # optional: words that influenced the prediction
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
