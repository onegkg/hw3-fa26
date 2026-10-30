"""Property-based tests for the normalization module.

Task 3: Implement check_property in checker.py so these tests can run.
Task 4: Define at least one new prop_ function in this file.
        Add at least one new test class that exercises it (or a provided property)
        with a generator of your choice.
Task 5: Replace the placeholder generators with better ones.
        Add tests that use them and see which ones find failures.
Task 6: When check_property finds a failure, manually minimize the counterexample,
        then add regression test(s) here with the required docstring format.
"""

from __future__ import annotations

import unicodedata

from searchengine.normalize import normalize_document

from .checker import check_property
from .generators import (
    diacritic_word,
    hyphenated_phrase,
    random_printable,
    random_sentence,
    random_word,
)
from .properties import (
    prop_idempotent_document,
    prop_no_empty_tokens_document,
    prop_query_document_consistent,
)

# Generators for Tasks 4-5 (import them when you implement them):
# from .generators import diacritic_word, hyphenated_phrase

# ---------------------------------------------------------------------------
# TODO (Task 4): Add at least one new test class below.
# Use check_property with one of the provided properties from .properties
# and a generator of your choice. Which generator is most likely to find
# a failure for each property?
# ---------------------------------------------------------------------------


def prop_no_diacritics_document(input: str) -> bool:
    """
    Tests whether there are any diacritics in the string
    """

    toks = normalize_document(input)
    norm_toks = [unicodedata.normalize("NFD", tok) for tok in toks]
    # if any character is a combining mark (`Mn`), return false
    return not any(unicodedata.category(char) == "Mn" for char in "".join(norm_toks))


class TestNoDiacritics:
    def test_no_diacritics_document_random_sentences(self) -> None:
        """Even on random sentences"""
        passed, counterexample = check_property(
            prop_no_diacritics_document,
            diacritic_word,
            trials=200,
            seed=42,
        )
        assert passed, f"Diacritics found in normalized text for: {counterexample!r}"


# ---------------------------------------------------------------------------
# Tests using check_property
# ---------------------------------------------------------------------------


class TestIdempotence:
    def test_idempotent_random_sentences(self) -> None:
        """Idempotence holds for random sentences (naive generator)."""
        passed, counterexample = check_property(
            prop_idempotent_document,
            random_sentence,
            trials=200,
            seed=42,
        )
        assert passed, f"Idempotence violated for: {counterexample!r}"


class TestNoEmptyTokens:
    def test_no_empty_tokens_printable(self) -> None:
        """No empty tokens from random printable strings."""
        passed, counterexample = check_property(
            prop_no_empty_tokens_document,
            random_printable,
            trials=200,
            seed=1,
        )
        assert passed, f"Empty token found for input: {counterexample!r}"


class TestQueryDocumentConsistency:
    def test_consistency_random_words(self) -> None:
        """Query and document normalization agree on random plain words.

        With the naive generator (lowercase words only), this property likely
        passes, because the naive generator never produces diacritics or hyphens.
        """
        passed, counterexample = check_property(
            prop_query_document_consistent,
            random_word,
            trials=200,
            seed=10,
        )
        assert passed, f"Normalization mismatch for: {counterexample!r}"

    # TODO (Task 5): Add a test using diacritic_word as the generator, and one
    # using hyphenated_phrase. Each should find a failure on the starter code.

    def test_consistency_diacritic_words(self) -> None:
        """
        Query and document normalization agree on random words containing diacritics
        """
        passed, counterexample = check_property(
            prop_query_document_consistent,
            diacritic_word,
            trials=200,
            seed=120,
        )
        assert passed, f"Normalization mismatch for: {counterexample!r}"

    # TODO (Task 5): After implementing hyphenated_phrase, add a test here
    # that uses it. Does it find a failure the printable generator missed?
    def test_consistency_hyphenated_phrase(self) -> None:
        """No empty tokens from random hyphenated phrases"""
        passed, counterexample = check_property(
            prop_query_document_consistent,
            hyphenated_phrase,
            trials=200,
            seed=45,
        )
        assert passed, f"Normaliation mismatch found with input: {counterexample!r}"


# ---------------------------------------------------------------------------
# Regression tests (Task 6)
# ---------------------------------------------------------------------------
#
# After finding a failure with check_property, add a regression test here.
# A regression test is a plain example-based test for a specific failing input.
#
# Structure:
#
#   def test_regression_<descriptive_name>() -> None:
#       """Regression: <describe what failed and how you found it>."""
#       failing_input = "..."   # the exact counterexample
#       assert prop_<name>(failing_input), f"Regression: {failing_input!r}"
#
# A regression test should be:
# - Named clearly so future readers understand what bug it guards against
# - Accompanied by a docstring explaining how the failure was discovered
# - Standalone (does not call check_property; uses the specific failing input)


def test_regression_diacritics_consistency() -> None:
    """
    Regression: Diacritics produce inconsistent results when passed to normalize query vs normalize document

    Original Failure: `iopqijt̗a jnskhgd̪m kskuifr͒z ihjdnzyeirt̂h razrygqwz̆u w͐v hbi̡f vňj hypnmri̸q xvocmabwx̅y`
    Minimized Failure: `z̆`

    Reason: Presence of any diacritic is enough to fail

    Original failure found by diacritic word with seed=120 and trials=200
    """
    minimized_input = "î"
    assert prop_query_document_consistent(minimized_input), f"Regression: {minimized_input}"

    failing_input = (
        "iopqijt̗a jnskhgd̪m kskuifr͒z ihjdnzyeirt̂h razrygqwz̆u w͐v hbi̡f vňj hypnmri̸q xvocmabwx̅y"
    )
    assert prop_query_document_consistent(failing_input), f"Regression: {failing_input}"


def test_regression_hyphenation_consistency() -> None:
    """
    Regression: Hyphenated works produce inconsistent results when passed to normalize query vs normalize document

    Original Failure: `picjkac-adjzdjxu-t-ei`
    Minimized Failure: `i-i`

    Reason: Presence of any hyphen is enough to fail

    Original failure found by hyphenated word with seed=45 trials=200
    """
    minimized_input = "i-i"
    assert prop_query_document_consistent(minimized_input), f"Regression: {minimized_input}"

    failing_input = "picjkac-adjzdjxu-t-ei"
    assert prop_query_document_consistent(failing_input), f"Regression: {failing_input}"
