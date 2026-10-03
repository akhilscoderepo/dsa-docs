# Chapter 34: Advanced strings

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| rolling hash | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| KMP/Z algorithm | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| palindrome radii | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| suffix arrays/automata | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Aho-Corasick multi-pattern matching | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.

### Pattern References

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Prefix Automata + Stream State | LC 28 Find the Index of the First Occurrence in a String | LC 459 Repeated Substring Pattern | LC 1392 Longest Happy Prefix | LC 1032 Stream of Characters |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Rolling Hash

**Recognition cue.** Many equal-length substrings need fast equality checks or repeated-pattern detection. **Invariant.** The maintained hash represents exactly the current substring under fixed base/modulus rules. **False friend.** Hash equality is not proof unless collisions are verified or bounded by policy.

- **Build - Author exercise: Fixed-Window Hash.** Remove the outgoing character and append the incoming one.
- **Vary - LC 187 Repeated DNA Sequences.** Record repeated fixed-length encodings.
- **Boundary - Author exercise: Negative Modular Difference.** Normalize after removing the outgoing contribution.
- **Recognize - LC 1044 Longest Duplicate Substring.** Combine rolling hash with binary search and collision verification.

### Prefix Matching

**Recognition cue.** Pattern matching must reuse knowledge after a mismatch instead of restarting. **Invariant.** KMP's prefix function stores the longest proper prefix that is also a suffix; fallback preserves already matched structure.

- **Build - Author exercise: Prefix Function.** Compute fallback lengths for one pattern.
- **Vary - LC 28 Find the Index of the First Occurrence in a String.** Match text with KMP state.
- **Boundary - Author exercise: Repeated Prefixes.** Trace a pattern such as `ababaca` through multiple fallbacks.
- **Recognize - LC 1392 Longest Happy Prefix.** Read the final prefix-function value as the answer.
- **Extend - Author exercise: Z Array.** Compute, for every position, the length matching the string prefix and compare its reuse window with KMP fallback state.

### Palindrome Radii

**Recognition cue.** Palindromes centered at every position must be found in linear time. **Invariant.** Manacher's algorithm maintains the rightmost known palindrome and mirrors a radius within it, then expands only beyond known coverage.

- **Build - Author exercise: Expand Odd Centers.** Compute radii by direct expansion.
- **Vary - Author exercise: Unified Separators.** Transform the string so odd and even palindromes share one representation.
- **Boundary - Author exercise: Mirror Beyond Boundary.** Clamp the copied radius to the current right edge.
- **Recognize - LC 5 Longest Palindromic Substring.** Use radii to recover the longest substring boundaries.

### Suffix Structures

**Recognition cue.** Queries concern repeated substrings, suffix order, or distinct substrings across one text. **Invariant.** A suffix array orders all suffixes lexicographically; an automaton state represents end-position-equivalent substrings.

- **Build - Author exercise: Sort Small Suffixes.** List suffixes and their lexical order.
- **Vary - Author exercise: Longest Common Prefix Of Adjacent Suffixes.** Find repeated substring candidates.
- **Boundary - Author exercise: Repeated Character String.** Preserve distinct suffix starts despite equal prefixes.
- **Recognize - LC 1044 Longest Duplicate Substring.** Compare suffix-array and rolling-hash approaches.

### Aho Corasick

**Recognition cue.** Many patterns must be matched simultaneously against one text or stream. **Invariant.** Trie transitions consume characters; failure links move to the longest suffix that is also a stored prefix, and output links report terminal matches.

- **Build - Author exercise: Trie Failure Links.** Build fallback state level by level.
- **Vary - Author exercise: Multi-Pattern Scan.** Follow transitions and report all terminal outputs.
- **Boundary - Author exercise: Suffix Pattern Matches.** Preserve outputs inherited through failure links.
- **Recognize - LC 1032 Stream of Characters.** Maintain automaton state across successive query calls.

## Released Combination Lessons

### Prefix Automata State

Trie nodes encode prefixes; failure transitions make that prefix state reusable after mismatches and across a stream.

- **Build - LC 28 Find the Index of the First Occurrence in a String.** Establish reusable prefix fallback with KMP.
- **Vary - LC 459 Repeated Substring Pattern.** Interpret prefix structure as repeated period length.
- **Boundary - LC 1392 Longest Happy Prefix.** Require a proper prefix and suffix rather than the whole string.
- **Recognize - LC 1032 Stream of Characters.** Preserve multi-pattern automaton state between API calls.

### Deferred: Specialized String DP

Problem-specific string/DP compositions remain with their owning recurrence rather than being duplicated here.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use a collision policy for rolling hash and make alphabet/encoding assumptions explicit.
- Avoid substring allocation in repeated pattern checks when indexes suffice.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Prefix Automata + Stream State | KMP/Z prefix state and trie failure links summarize active matches; representative: LC 1032 |
| Deferred | Strings + DP/Trie compositions | Release only with the owning DP or trie invariant |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** trie/DP/string compositions.

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

