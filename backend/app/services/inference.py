import onnxruntime
import numpy as np
import asyncio
from functools import lru_cache
import os
from app.utils.text_preprocessing import text_preprocessing
from app.utils.text_preparation import (
    convert_to_numerical_sentence, padded_numerical_sentences
)


# backend/app/artifacts/TextSpamDetect_v2.1.onnx
BACKEND_ARTIFACTS_DIR = os.path.join(os.getcwd(), 'app', 'artifacts')
MODEL_PATH = os.path.join(BACKEND_ARTIFACTS_DIR, 'TextSpamDetect_v2.1.onnx')


@lru_cache(maxsize=1)
def get_onnx_session() -> onnxruntime.InferenceSession:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"ONNX model not found at: {MODEL_PATH}")

    # providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
    providers = ['CPUExecutionProvider']
    return onnxruntime.InferenceSession(str(MODEL_PATH), providers=providers)


def _run_onnx_inference(text, max_len=73):
    # 1. Preprocessing
    cleaned_texts = ' '.join(text_preprocessing(text))

    # 2. Convert words into numerical values
    numeric_sentence = convert_to_numerical_sentence(cleaned_texts)
    # 3. Truncate sequence
    numeric_sentence = numeric_sentence[:max_len]
    # 4. Padding
    padded_numeric_sentence, current_seq_length = padded_numerical_sentences(
        numeric_sentence
    )
    # 5. Convert to NumPy arrays
    input_seq = np.array(
        [padded_numeric_sentence],
        dtype=np.int64
    )

    seq_length = np.array(
        [current_seq_length],
        dtype=np.int64
    )

    # 6. ONNX Runtime inference
    session = get_onnx_session()
    outputs = session.run(
        None, {
            'input_seq': input_seq,
            'seq_length': seq_length
        }
    )

    # 7. Get logits
    logits = outputs[0]

    # 8. Calculate probabilities
    ham_probability = 1 / (1 + np.exp(-logits)).item()
    spam_probability = 1 - ham_probability

    # 9. Classification
    prediction = "ham" if ham_probability >= 0.5 else "spam"
    
    ham_prob = float(ham_probability * 100)
    spam_prob = float(spam_probability * 100)
    
    return {
        "text": text,
        "ham_probability": f"{ham_prob:.1f}",
        "spam_probability": f"{spam_prob:.1f}",
        "prediction": prediction
    }


async def predict_sentiment_onnx(text: str, max_len=73):
    return await asyncio.to_thread(_run_onnx_inference, text, max_len)
