# HW3 Written Reflection

Answer the following questions thoughtfully. There are no "right" answers. The goal is honest reflection on your experience and on the ideas from class.

This written component is designed to reward **honest engagement and theory-building**, even if your artifact is incomplete. A test suite that passes without understanding and a partial test suite with deep understanding are *not* the same thing, but both can be discussed thoughtfully here.

---

## Part 0: Self-Assessment

Complete this section **before** writing your reflection. Be honest. This is not penalized, and it helps us calibrate grading. Accurate self-assessment demonstrates the kind of self-awareness we value.

### Artifact Completion

For each task, mark your status: **Done**, **Partial**, or **Not Done**. Add brief notes if helpful.

| Task | Status | Notes (optional) |
|------|--------|------------------|
| 1. Read the code and tried `search explain` before writing tests | Done | |
| 2. At least 6 new example-based tests | Done | |
| 3. `check_property` implemented | Done | |
| 4. A new property, with a test class that uses it | Done | |
| 5. `diacritic_word` and `hyphenated_phrase` implemented | Done | |
| 6. Regression tests with minimized counterexamples; both bugs fixed | Done | |
| 7. Hypothesis tests, a regression test, and the third bug fixed | Done | |
| 8. Surviving mutants analyzed, one killed by a named test, and compared with Hypothesis | Done | |
| All tests pass (`make test`) | Done | |
| Lint passes (`make lint`) | Done | |
| Grading checks pass (`make grade`) | Done | |

### Understanding Self-Check

Answer briefly (1–3 sentences each):

1. **What do you feel you genuinely understand** about this assignment? (Not just "made it work," but could explain to someone else or extend on your own.)
    - property based testing
    - mutation testing

2. **What did you make work without fully understanding?** (Be honest. This is useful self-knowledge.)
    - Minimization
    - Coming up with edgecases
    - Unicode quirks

3. **Where did you get stuck?** What did you try before moving on or seeking help?
    - I had initially said that my mutants were unkillable, but then my Hypothesis tests killed them, which greatly confused me. I turned to Claude, Google, and the Unicode spec for help

---

## Part 1: Short Response (1–2 paragraphs each)

### A: Shrinking by Hand and by Hypothesis

In Task 6 you took a failing input from `check_property` and shrank it yourself. In Task 7, Hypothesis handed you a failing input it had already shrunk. Compare the two minimizations, giving the original and minimized input from Task 6 and the input Hypothesis reported in Task 7, and explain what each one told you about the bug behind it. Was the smallest input always the easiest one to understand?
    - Hypothesis gave me `𝑨` (MATHEMATICAL BOLD ITALIC CAPITAL A). The task six original input was `iopqijt̗a jnskhgd̪m kskuifr͒z ihjdnzyeirt̂h razrygqwz̆u w͐v hbi̡f vňj hypnmri̸q xvocmabwx̅y` and the minimized input was `î`. The task of minimization was actually quite useful in determining the bug in this case, since not all of the characters with diacritics caused the tests to fail. Both bugs were caused by Unicode quirks that I hadn't anticipated. The smallest input was in this case the easiest to understand since it cuts the failure down to the smallest possible failure, removing any unnecessary variables that may have sent me on wild goose chases while debugging.

### B: Generic and Domain-Aware Inputs

Your Task 5 generators were built from what you knew about this domain (diacritics and hyphens), and they found the two Task 6 bugs. Hypothesis's `st.text()` knows nothing about search engines, and in Task 7 it found a third bug that your generators never produced an input for. Using these results, explain where knowing the domain helped you choose test inputs and where it limited you.
    - While knowing the domain helped me choose good test inputs, I think that domain aware generators fall victim to a similar problem as example based testing. In order to write good generators and good tests, you need to be able to think of the thing to test and write the generator or example based test. For this project, where most of the bugs were caused by quirks of the Unicode specification, I feel that our domain aware generators were not aware enough, and that Hypothesis' arbitrary Unicode generator would have been a better fit while still covering the same areas as our custom generators. Arbitrary Unicode does have `-`s and diacritics in it.

### C: Mutation Testing as Test Evaluation

*Software Engineering at Google* (ch. 11) says that tests have no tests of their own, so they need a person to review them, and it warns that code coverage only shows that a line ran, not that anything checked the result.

What did mutation testing reveal about your test suite that you could not have known from simply running the tests, and what does it mean to "strengthen" a test suite?
    - Mutation testing was enormously helpful at discovering weaknesses in both my test suite, and often the code itself. It is a more powerful tool for measuring test coverage, since it actually checks whether a given line of code not just runs, but is checked in the test suite. Mutation testing taught me that my test suite was reliant on Hypothesis for certain types of Unicode quirks, which is not necessarily a problem, but would be something to keep in mind if I were to keep working in this code-base. Strengthening a test suite is the action of adding to the test suite to either A. add code coverage or B. bring the test suite more in line with a formal or informal specification of the desired functionality of the program.

### D: What Counts as Correct?

The normalizer makes choices about what users can find. A few cases:

- Before Task 6's fix, a search for "co-op" became "coop" and would match a page about chicken coops. After the fix, it becomes "co" and "op", and a search for "coop" no longer finds the co-op programs document.
- A search for "The Who" drops "the" as a stopword and becomes a search for "who", which matches any document with that word in it.
- A post written in styled letters like 𝐁𝐫𝐞𝐚𝐤𝐢𝐧𝐠 𝐍𝐞𝐰𝐬 (common on social media) is indexed differently from plain text, at least until Task 7's fix.
- A spam post written in l33tsp34k, like "fr33 g1v34w4y", is indexed as the words "fr33" and "g1v34w4y", so a search for "free giveaway" never finds it. Spammers spell words this way on purpose, to get past filters that look for "free".

Choose one of these cases (or another you found) and argue what the search engine should do, and who should get to decide.
    - I will be discussing "The Who". I would argue that users should at least have a way to search for "The Who" and not "who". While this may seem like a mostly benign case, decisions like this in real search engines can make or break the success of a band, company, product. There are whole classes about how to name things in a way to maximize its reach on search engines. Also, you could imagine a world in which a search engine company (say Google) could subtly modify the normalization rules to disadvantage their competitors (To be clear it doesn't seem that Google is actually doing this, but they definitely could if they wanted to). This leads into the discussion of who gets to make those decisions, which is a complicated and subjective issue. The owner of the tool obviously has the final say (unless they get sued I guess), but I would argue that, in cases like these, they have a responsibility to design their systems to minimize these sorts of inequities, but I don't really know how to encourage/enforce that ideal.

---

## Part 2: Essay on the Limits and Value of Testing (500–700 words)

*This is the biggest question, in terms of both size and importance. Take your time with it.*

Write an essay that engages with **both** readings, Dijkstra's "The Humble Programmer" and *Software Engineering at Google* (ch. 11), using your own experience in this assignment as evidence. Your essay should take a position, not just describe both arguments neutrally.

**Possible directions** (choose 2–3 to develop; you do not need to touch all of them):

- **What your suite shows and what it doesn't**: what your finished tests leave unchecked, and whether that matters for a search engine like this one.
- **A bug nobody planted**: what the Task 7 bug says about tests written by people who already know where the bugs are, and whether Dijkstra's structural approach would have caught it.
- **Who tests the tests**: mutation testing checks your tests, but something has to check the mutation tests. What this regress says about how much any amount of testing can establish.
- **Confidence to change**: what automated tests did for the GWS team in ch. 11, and whether that is the right goal for testing, judged by how you felt changing `normalize.py` with and without your tests in place.

A thoughtful argument that testing matters less than either reading suggests is **entirely acceptable** if it is well reasoned and grounded in your experience.

Dijkstra's **The Humble Programmer** and Chapter 11 of **Software Engineering at Google** both address the inevitable complexity of software systems, but they go in somewhat different directions in their approaches to addressing that complexity. They both recognize the fundamental limitations of software testing, with Dijkstra saying "program testing can be a very effective way to show the presence of bugs, but is hopelessly inadequate for showing their absence". Dijkstra recommends supplementing or even replacing program testing with formal verification of system behavior. SWE@Google also recognizes the limits of software testing, but they argue that, if done well, it is still valuable for lending confidence that larger refactors and new features have not introduced any regressions, allowing faster cleanup of technical debt and feature development.

I feel that giving developers confidence in their changes is arguably the most important role of a test suite. A test suite which is regularly updated with regression tests can give developers a sense of security when making large changes which they might otherwise not have had the confidence to make. I argue that this is the most important role of a test suite because it is the only role that a test suite can completely fill. Even the most extensive test suite can never guarantee software quality, there will always be edge cases that are missed. But a good test suite can give enough assurances against regressions that it enables developers to iterate with ease.

Since a test suite can never guarantee software quality, it can be tempting to lean (pun unintended) on formal verification to guarantee software quality. And while formal verification definitely has a place in guaranteeing software quality, it provides competing incentives with automated testing that developers need to be aware of. The resource intensive nature of formal verification, combined with the fact that it is implementation dependent, encourages developers not to touch code that has been formally verified, since any changes to the code would mean that it would need to be re-verified, costing significant time and money. Combined with the fact that formally verifiable systems must be written in a restricted manner in order to allow for verification, this fact restricts formal verification's usefulness to security or safety critical code that is unlikely to ever change, which is a niche most software developers outside of kernel development or military contracts are likely to happen upon. Automated tests on the other hand, are (relatively) cheap to write, usually do not care about the implementation of the program they're testing, and can actually test arbitrary programs in a Turing complete language (which is not true of formal verification, due to The Halting Problem). This combination of traits means automated testing ends up being a good solution for many codebases, for both the reasons listed in the paragraph above, and because a good test suite can be a good enough signal of software quality for these less security sensitive applications.

A personal note: I hate writing tests. While I recognize that it is super important for all the reasons listed above, among many others, I find it tedious and boring. I especially have this gripe with example based testing, especially unit testing, but it applies less strongly to other testing methods as well. I recognize that this is a personal weakness, so I am constantly looking for ways to make testing less painful for myself. As I've found more palatable (snapshot tests are wonderful in the right contexts), I've found that when I actually implement the tests, and have faith in their completeness (i.e. I didn't just pass it off to AI), I feel much more confident making changes, since I can be reasonably sure that if the tests pass, I haven't introduced any regressions. This aligns with the point that SWE@Google makes about tests lending developers confidence in their changes. This unit has been extremely helpful to me, as it has reinforced the need for me to improve my testing discipline and introduced me to new, more pleasant, and more comprehensive ways of testing software.

---

## Submission

The written reflection is submitted separately from your artifact:

1. Write your responses in this document (or a copy of it, in any editor you like).
2. Upload the completed `WRITTEN.md` to the **HW3 Written** assignment on Gradescope.

### Formatting Guidelines

- **For all parts:** Aim for and prioritize clarity and honest engagement.
- **Part 1**: ~1–2 paragraphs each
- **Part 2**: **~500–700 words** (roughly one single-spaced page). It's fine to go slightly over.
