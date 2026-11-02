import re

from searchengine.normalize import fold_diacritics
from searchengine.stopwords import STOPWORDS


def normalize_document(text: str) -> list[str]:
    text = text.upper()
    text = fold_diacritics(text)
    text = text.lower()
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return [t for t in tokens if t and t not in STOPWORDS]


text = "ß"
toks = normalize_document(text)
print(toks == normalize_document(" ".join(toks)))
