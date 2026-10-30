"""Unit tests for the normalization module.

Some tests are provided as working examples.
Your job in Task 2 is to add more, including tests that expose
the normalization bugs lurking in this codebase.
"""

from __future__ import annotations

from searchengine.normalize import fold_diacritics, normalize_document, normalize_query

# ---------------------------------------------------------------------------
# fold_diacritics: provided tests
# ---------------------------------------------------------------------------


class TestFoldDiacritics:
    def test_resume(self) -> None:
        assert fold_diacritics("résumé") == "resume"

    def test_naïve(self) -> None:
        assert fold_diacritics("naïve") == "naive"

    def test_plain_ascii_unchanged(self) -> None:
        assert fold_diacritics("hello") == "hello"

    def test_empty_string(self) -> None:
        assert fold_diacritics("") == ""

    def test_idempotent(self) -> None:
        text = "café naïve résumé"
        assert fold_diacritics(fold_diacritics(text)) == fold_diacritics(text)


# ---------------------------------------------------------------------------
# normalize_document: provided tests
# ---------------------------------------------------------------------------


class TestNormalizeDocument:
    def test_lowercases(self) -> None:
        assert normalize_document("Hello World") == ["hello", "world"]

    def test_strips_punctuation(self) -> None:
        result = normalize_document("hello, world!")
        assert result == ["hello", "world"]

    def test_removes_stopwords(self) -> None:
        result = normalize_document("a quick brown fox")
        assert "a" not in result

    def test_empty_input(self) -> None:
        assert normalize_document("") == []

    def test_all_stopwords(self) -> None:
        assert normalize_document("the a an") == []

    def test_no_empty_tokens(self) -> None:
        result = normalize_document("hello   world")
        assert "" not in result

    def test_diacritics(self) -> None:
        result = normalize_document("naïve")
        assert result == ["naive"]

    def test_hyphenation(self) -> None:
        result = normalize_document("co-op")
        assert result == ["co", "op"]

    def test_cpp(self) -> None:
        result = normalize_document("C++")
        assert result == ["c++"]

    def test_node_js(self) -> None:
        result = normalize_document("node.js")
        assert result == ["nodejs"]


# ---------------------------------------------------------------------------
# normalize_query: provided tests
# ---------------------------------------------------------------------------


class TestNormalizeQuery:
    def test_lowercases(self) -> None:
        assert normalize_query("Hello") == ["hello"]

    def test_removes_stopwords(self) -> None:
        result = normalize_query("a search query")
        assert "a" not in result

    def test_empty_input(self) -> None:
        assert normalize_query("") == []

    def test_no_empty_tokens(self) -> None:
        result = normalize_query("hello   world")
        assert "" not in result

    def test_diacritics(self) -> None:
        result = normalize_query("naïve")
        assert result == ["naive"]

    def test_hyphenation(self) -> None:
        result = normalize_query("co-op")
        assert result == ["co", "op"]


# ---------------------------------------------------------------------------
# Consistency tests: provided (some of these FAIL because they expose the bugs)
# ---------------------------------------------------------------------------


class TestNormalizationConsistency:
    """Query and document normalization should agree.

    If they disagree, a user who searches for a term will not find
    documents that contain that term. The search fails silently.

    Two of these tests fail on the starter code.
    """

    def test_plain_ascii_consistent(self) -> None:
        """Basic ASCII text normalizes the same way for docs and queries."""
        assert normalize_query("hello world") == normalize_document("hello world")

    def test_diacritic_consistency(self) -> None:
        """'naïve' should normalize the same way whether in a doc or a query.

        This test FAILS on the starter code.
        """
        assert normalize_query("naïve") == normalize_document("naïve")

    def test_hyphen_consistency(self) -> None:
        """'co-op' should normalize the same way whether in a doc or a query.

        This test FAILS on the starter code.
        """
        assert normalize_query("co-op") == normalize_document("co-op")

    # TODO (Task 2): Add at least two more consistency tests with inputs
    # that are likely to surface disagreements between the two normalizers.

    def test_cpp_consistency(self) -> None:
        """
        C++ should normalize the same way in both places
        """
        assert normalize_query("C++") == normalize_document("C++")

    def test_node_js_consistency(self) -> None:
        """
        node.js should normalize the same way in both places
        """
        assert normalize_query("node.js") == normalize_document("node.js")
