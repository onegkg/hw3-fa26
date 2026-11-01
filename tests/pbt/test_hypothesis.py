"""Property-based tests with Hypothesis (Task 7).

Hypothesis is a property-based testing library. It plays the role of your
check_property and your generators: you describe what kind of input you want
(a "strategy", such as st.text() for any string), and Hypothesis generates the
inputs, runs your test on each one, and reports the smallest failing input it
can find.

The test below is a complete example. It reuses a property from properties.py,
the same function your check_property tests call.
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from searchengine.normalize import normalize_document, normalize_query

from .properties import prop_no_empty_tokens_document


@given(st.text())
def test_no_empty_tokens_any_text(text: str) -> None:
    """No empty tokens, for any string Hypothesis generates."""
    assert prop_no_empty_tokens_document(text)


# TODO (Task 7): Add a Hypothesis test for each of these properties from
# properties.py, using st.text() as the strategy:
#   - prop_idempotent_document
#   - prop_query_document_consistent
# Then follow the rest of Task 7 in ARTIFACT.md.
@settings(max_examples=2000)
@given(st.text())
def test_indempotent_document_any_text(text: str) -> None:
    """Document normalization is indempotent for any input text"""
    toks = normalize_document(text)
    assert toks == normalize_document(" ".join(toks))


@settings(max_examples=2000)
@given(st.text())
def test_query_document_consistency_any_text(text: str) -> None:
    """Document and query normalization should be consistent for any input text"""
    assert normalize_document(text) == normalize_query(text)


def test_regression_lack_of_indempotence_related_to_stopword_elimination() -> None:
    """
    Regression: document normalization is not indempotent when a normalization results in a stopword.

    Found by : Hypothesis, test_indempotent_document_any_text (st.text(), 2000 examples)
    Hypothesis gave : '𝑨' (MATHEMATICAL BOLD ITALIC CAPITAL A)

    The first normalization pass changed it to a normal 'A' which was removed in the second pass since it is a stopword.
    """
