import unicodedata
from searchengine.normalize import normalize_document

s = '𝑨'
for c in s:
    print(repr(c), unicodedata.name(c, "(no name)"))

first = normalize_document(s)
print(first)
print(normalize_document(" ".join(first)))
