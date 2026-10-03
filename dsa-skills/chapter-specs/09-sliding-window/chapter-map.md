# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Fixed-Size Aggregate Windows  ->  01-fixed-size-aggregate-windows.md
02. Fixed Frequency Windows  ->  02-fixed-frequency-windows.md
03. Longest-Valid Windows  ->  03-longest-valid-windows.md
04. Minimum-Cover And Deficit Windows  ->  04-minimum-cover-and-deficit-windows.md
05. At-Most-K Distinct Windows  ->  05-at-most-k-distinct-windows.md
06. Exactly-K By Subtraction  ->  06-exactly-k-by-subtraction.md
07. Replacement-Budget Windows  ->  07-replacement-budget-windows.md
08. Count-All-Valid-Subarrays Windows  ->  08-count-all-valid-subarrays-windows.md
09. Repeated-Shrink Versus Non-Shrinking Policy  ->  09-repeated-shrink-versus-non-shrinking-policy.md

# Chapter 09: Sliding window

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| fixed-size aggregate windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| fixed-size frequency/permutation windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| longest-valid windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| minimum-cover/deficit windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| at-most-K distinct windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| exactly-K-by-subtraction windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| replacement-budget windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| count-all-valid-subarrays windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| repeated-shrink versus non-shrinking policy | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Window Frequency State

Window boundaries identify the active contiguous range; frequency state records the multiset, deficits, or violations inside it. Neither component is sufficient by itself. The combined invariant must say both which indices are active and what every stored count means.

- **Build - LC 567 Permutation in String.** Maintain exact counts in a fixed-length window.
- **Vary - LC 3 Longest Substring Without Repeating Characters.** Let the length vary and shrink until all counts are at most one.
- **Boundary - LC 424 Longest Repeating Character Replacement.** Convert frequencies into a replacement budget and justify the maximum-frequency policy.
- **Recognize - LC 76 Minimum Window Substring.** Track required multiplicities, expand to validity, and shrink to a minimal cover.

### Deferred: Sliding Window And Deque

A deque can retain the best candidate for each moving window, but its ordered-candidate and index-expiry invariants have not been taught. Chapter 13 owns Sliding Window Maximum and related exercises; this chapter only names the future composition.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Avoid creating substrings in the moving-window loop; retain boundaries and construct output once.
- Use primitive count arrays only when the character-domain contract permits them.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Sliding Window + Frequency State | Moving boundaries plus counts/deficits; staircase: LC 567 → LC 3 → LC 76 |
| Deferred | Sliding Window + Deque | Chapter 13 supplies the monotone-deque and index-expiry invariant |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Shrink-policy classification:** distinguish a repeatedly shrinking window, which restores validity before continuing, from a non-shrinking maximum-length formulation, which advances `left` at most once per `right` under a separately proved monotonic condition. Do not present the one-removal form as a universal longest-window rule.
- **Practice split:** give the two policies separate recognition cues and staircases; minimum-cover and replacement-budget windows should not share one vague shrink explanation.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** prefix-sum alternatives, heap/window combinations.

For every released combination, create a dedicated lesson that states each prerequisite's contribution, the combined state/invariant, a false friend, implementation, and its own Build → Vary → Boundary → Recognize staircase. Deferred combinations receive an explanation and a future owner only—never premature exercises.

## Publication Gate

- Crosswalk every required micro-pattern to a named lesson and practice ladder.
- Run the composition audit and record released/deferred outcomes.
- Run the Java integrity focus against every code example.
- Verify exact problem wording, examples, complexity, and prerequisite ownership.
- Render and inspect the PDF; then perform text extraction checks.

## Research Baseline

- [LeetCode Study Plans](https://leetcode.com/studyplan/) for problem discovery and current interview-style prompts.
- [NeetCode Roadmap](https://neetcode.io/roadmap) for a cross-check of prerequisite order and representative pattern families.
- [Tech Interview Handbook study cheatsheets](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) for topic-specific corner cases, complexity review, and interview habits.
- [Oracle Java Collections documentation](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) for Java collection semantics. Prefer the installed JDK documentation for version-specific details when a chapter relies on a newer API.
- Supplied reference books: *Cracking the Coding Interview*, *Grokking Algorithms*, and *Elements of Programming Interviews in Java*. They guide explanation quality and problem selection; they are not copied verbatim.
