# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Opposite Ends  ->  01-opposite-ends.md
02. Read And Write  ->  02-read-and-write.md
03. Two-Way Partition  ->  03-two-way-partition.md
04. Three-Way Partition  ->  04-three-way-partition.md
05. Duplicate Skipping  ->  05-duplicate-skipping.md
06. K-Sum Reduction  ->  06-k-sum-reduction.md
07. Array Cycle State  ->  07-array-cycle-state.md

# Chapter 08: Two pointers

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| opposite-end sorted-pair scans | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| same-direction read/write scans | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| partitioning | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Dutch-national-flag three-way partition | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| duplicate skipping | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| 3Sum/k-sum foundations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| index-as-storage plus Floyd fast/slow cycle detection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Sorting And Two Pointers

Sorting creates the monotone sum relation; pointer movement exploits it. Sorting alone still scans too many pairs, while pointers on unsorted data have no safe movement proof.

- **Build - LC 167 Two Sum II.** Sorted pair elimination.
- **Vary - LC 15 3Sum.** Fix one value and reuse pair search.
- **Boundary - LC 16 3Sum Closest.** Preserve a best candidate when no exact target exists.
- **Recognize - LC 18 4Sum.** Add another fixed dimension with `long` sums and duplicate control.

### Strings And Two Pointers

String normalization/indexing supplies comparable characters; pointers supply symmetric or same-direction movement.

- **Build - LC 125 Valid Palindrome.** Skip non-alphanumeric characters and compare normalized endpoints.
- **Vary - LC 344 Reverse String.** Swap endpoints in a mutable `char[]`.
- **Boundary - LC 680 Valid Palindrome II.** At the first mismatch, test exactly one skipped endpoint.
- **Recognize - LC 392 Is Subsequence.** Both pointers now move left-to-right at different rates; this is not palindrome movement.

### Index State And Floyd

The array’s bounded values create next links; Floyd’s algorithm supplies cycle entry detection. Neither prerequisite alone explains LC 287.

- **Build - Author exercise: Value-As-Next-Index.** Validate the representation and trace one path.
- **Vary - LC 287 Find the Duplicate Number.** Run meeting and entry phases.
- **Boundary - Author exercise: Duplicate Near Start.** Trace a short tail and cycle without mutating the array.
- **Recognize - Author exercise: Compare Alternatives.** Explain when cyclic placement or sign marking would violate the no-mutation contract.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Document whether input mutation through sorting or partitioning is allowed.
- Explain duplicate-skipping order before moving either pointer.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Sorting + Two Pointers | Ordered sum search and duplicate policy; staircase: pair sum → 3Sum → 3Sum Closest |
| Teach now | Strings + Two Pointers | Opposite-end validation; representative: LC 125 Valid Palindrome |
| Teach now | Index-as-Storage + Fast/Slow Pointers | LC 287 after the array-value-as-next-index contract is restated |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Array-valued Floyd cycle detection:** add the released composition `index-as-storage + fast/slow pointers` for LC 287. Teach the required value domain first: each value names the next index. Phase one proves entry into a cycle; phase two resets one pointer to the start and advances both one step to find the entry/duplicate.
- **Do not mix with linked-list cycle mechanics:** the pointer motion is shared, but array-value-to-index representation and its bounds contract are Chapter 01 prerequisites.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** sliding window, greedy, linked-list pointer techniques.

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
