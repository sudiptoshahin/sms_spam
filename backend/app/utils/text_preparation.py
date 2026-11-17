from pathlib import Path
import json
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
VOCAB_PATH = os.path.join(BASE_DIR, 'app', 'utils', "vocabulary.json")

with open(VOCAB_PATH, "r", encoding="utf-8") as f:
    VOCABULARY = json.load(f)
PAD_TOKEN = "<pad>"
UNK_TOKEN = "<unk>"

PAD_IDX = 0
UNK_IDX = 1

TRAIN_SEQ_MAX_LEN = 73


# when using dataframes `tokens` columns
def text_to_indices(sentence, vocab):
    numerical_sentences = []
    for token in sentence:
        token_id = vocab.get(token, UNK_IDX)
        numerical_sentences.append(token_id)
    return numerical_sentences


def convert_to_numerical_sentence(texts: list | str):
    X_train_numerical_sentences = []

    if isinstance(texts, str):
        texts_indices = text_to_indices(texts, VOCABULARY)
        return texts_indices
    else:
        for sentence in texts:
            texts_indices = text_to_indices(sentence, VOCABULARY)
            X_train_numerical_sentences.append(texts_indices)
        return X_train_numerical_sentences


def padded_numerical_sentences(numeric_sentences):

    if len(numeric_sentences) == 0:
        return [], []

    # Detect a single numerical sentence
    if isinstance(numeric_sentences[0], int):
        sequences = [numeric_sentences]
        is_single = True

    else:
        sequences = numeric_sentences
        is_single = False

    padded_sequences = []
    actual_lengths = []

    for seq in sequences:

        if not isinstance(seq, (list, tuple)):
            raise TypeError(
                f"Expected a list of token indices, got {type(seq)}: {seq}"
            )

        # Truncate
        seq = list(seq)[:TRAIN_SEQ_MAX_LEN]

        # Handle empty sequence
        if len(seq) == 0:
            seq = [UNK_IDX]

        # Calculate actual length
        actual_length = len(seq)

        # Padding
        pad_seq = seq + (
            [PAD_IDX] * (TRAIN_SEQ_MAX_LEN - actual_length)
        )

        padded_sequences.append(pad_seq)
        actual_lengths.append(actual_length)

    if is_single:
        return padded_sequences[0], actual_lengths[0]

    return padded_sequences, actual_lengths
