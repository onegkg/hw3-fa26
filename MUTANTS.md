# Task 8: Surviving Mutants

See Task 8 in [ARTIFACT.md](ARTIFACT.md).

## Without your Hypothesis tests (`make mutmut`)

**How many mutants survived?**

2

Fill in one section for each surviving mutant, up to two.

### Mutant 1

**Name:** searchengine.normalize.x_normalize_document__mutmut_2

**What it changes:** <!-- paste the changed line from `mutmut show <name>`, or describe it in a sentence -->
```python
-    text = text.lower()
+    text = text.upper()
     text = fold_diacritics(text)
     text = text.lower()
     text = text.replace("-", " ")
```

**Real gap or no observable difference?** Real gap

**Why it survived:** <!-- 2-4 sentences. For a real gap: what input would show the difference, and why none of your tests tried it. For no observable difference: why no input could tell this mutant from the original code. -->
I didn't realize that there are unicode characters for whom the lower->upper->lower conversion changes the output. For example "ß" becomes "SS" on uppercasing which becomes "ss" on lowercasing. A test checking this would have killed the mutant

**Killed?** <!-- If you killed it, name the test. If not, say why not. --> `test_non_round_trippable_consistency`

### Mutant 2

**Name:** searchengine.normalize.x_normalize_query__mutmut_2

**What it changes:**

It makes the same changes as mutation one, but in normalize_query instead of in normalize_document

```python
-    text = text.lower()
+    text = text.upper()
     text = fold_diacritics(text)
     text = text.lower()
     text = text.replace("-", " ")
```

**Real gap or no observable difference?** Real gap

**Why it survived:** Same reason as Mutant 1. `normalize_query` has the same upper-then-lower step, and my tests never passed it a character like "ß".

**Killed?** Killed by `test_non_round_trippable_consistency`

## With all your tests (`make mutmut-all`)

**How many mutants survived?** 0

**Which of your Hypothesis tests killed the mutants above, and why could it when your other tests couldn't?** <!-- One paragraph. -->

The mutants were both killed by `test_query_document_consistency_any_text`. While my example based tests did check for consistency between the two normalizers, it only tested it on ASCII and basic unicode rather than arbitrary unicode, so the lower->upper->lower round trip issue was not found. Since Hypothesis tests arbitrary unicode, it was able to kill the mutants where my example tests couldn't.

