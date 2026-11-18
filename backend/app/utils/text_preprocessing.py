
import re
import string
import nltk
import os
from pathlib import Path
from app.utils.chatwords import chat_words_dict
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.corpus import words, stopwords

# NLTK_DIR = os.path.abspath("../../env/nltk_data")

BACKEND_DIR = Path(__file__).resolve().parents[2]
NLTK_DIR = Path(
    os.getenv('NLTK_DATA', BACKEND_DIR / "env" / "nltk_data")
)
print(f'_________NLTK_DIR_______{NLTK_DIR}')
NLTK_DIR.mkdir(parents=True, exist_ok=True)
nltk.data.path[:] = [str(NLTK_DIR)]

RESOURCES = [
    ("tokenizers/punkt", "punkt"),
    ("tokenizers/punkt_tab", "punkt_tab"),
    ("corpora/words", "words"),
    ("corpora/stopwords", "stopwords"),
    ("corpora/wordnet", "wordnet")
]

def ensure_nltk_data() -> None:
    missing = []
    for path, package in RESOURCES:
        try:
            nltk.data.find(path)
        except LookupError:
            ok = nltk.download(package, download_dir=str(NLTK_DIR), quiet=False)
            if not ok:
                missing.append(package)
    if missing:
        raise RuntimeError(
            f"NLTK data missing: {missing}. Could not download them "
            f"(no network?). Copy the 'nltk_data' folder from a working "
            f"machine into: {NLTK_DIR}"
        )


ensure_nltk_data()

STOP_WORDS = set(stopwords.words('english'))


def remove_number_middle_of_text(text):
    pattern = re.compile(r'[a-zA-Z]+')
    text = pattern.sub(r"", text)
    return " ".join(text)


def remove_htmltags(text):
    pattern = re.compile(r"<.*?>")
    return pattern.sub(r"", text)


def remove_urls(text):
    pattern = re.compile(r"https?:\/\/\S+|www\.\S+")
    return pattern.sub(r"", text)


def remove_punctuations(text):
    excluded_punctuations = string.punctuation
    return text.translate(str.maketrans(" ", " ", excluded_punctuations))


def eloborate_chat_conversion(texts):
    new_text = []
    token_words = texts.split()

    for word in token_words:
        key = word.upper()
        if key in chat_words_dict:
            new_text.append(chat_words_dict[key])
        else:
            new_text.append(word)
    return " ".join(new_text)


def corrected_spelling(texts):
    results = []
    correct_words = [w.lower() for w in words.words()]
    correct_set = set(correct_words)
    text_tokens = texts.split()

    for word in text_tokens:
        lower_word = word.lower()
        # keep the correctly spelled words
        if lower_word in correct_set or not lower_word.isalpha() or len(lower_word) < 2:
            results.append(lower_word)
            continue

        incorrect_bigrams = set(ngrams(lower_word, 2))
        best_score, best_match = 1.0, word

        for w in correct_words:
            if w[0] == lower_word[0]:
                correct_bigrams = set(ngrams(w, 2))
                score = jaccard_distance(incorrect_bigrams, correct_bigrams)
                if score < best_score:
                    best_score, best_match = score, w
        results.append(best_match)
    return " ".join(results)


def remove_stopwords(texts):
    cleaned = []
    text_tokens = texts.split()
    for word in text_tokens:
        # word is already lowered
        if word and word not in STOP_WORDS:
            cleaned.append(word)
    return " ".join(cleaned)


def remove_emoji(texts):
    text_tokens = texts.split()
    text = " ".join(text_tokens)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002700-\U000027BF"  # dingbats
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    texts = emoji_pattern.sub(r'', text)
    return texts


def stemming_words(text_tokens):
    ps = PorterStemmer()
    stemmed_words = []
    return [stemmed_words.append(ps.stem(word)) for word in text_tokens]


def lemmatize_words(text_tokens):
    lemmatized_words = []
    wordnet_lemmatizer = WordNetLemmatizer()
    for word in text_tokens:
        lemmatized_words.append(wordnet_lemmatizer.lemmatize(word, pos='v'))
    return lemmatized_words


def text_preprocessing(text):
    # lowercasing
    text = text.lower()

    # remove html tags
    text = remove_htmltags(text)

    # remove urls from text
    text = remove_urls(text)

    text = remove_punctuations(text)

    text = eloborate_chat_conversion(text)

    text = corrected_spelling(text)

    text = remove_stopwords(text)

    text = remove_emoji(text)

    tokenized_text = word_tokenize(text)

    # tokenized_text = stemming_words(tokenized_text)

    tokenized_text = lemmatize_words(tokenized_text)

    return tokenized_text

