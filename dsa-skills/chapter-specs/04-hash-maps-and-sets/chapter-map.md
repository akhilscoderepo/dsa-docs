# Chapter map (generated; do not edit, edit the source spec)

Each structure earns its place by storing exactly the information the next decision needs. The point is not to reach automatically for a `HashMap`; it is to say what a key means, what its value means, and why order is irrelevant.

## Lesson order

01. Membership Sets  ->  01-membership-sets.md
02. Frequency Maps  ->  02-frequency-maps.md
03. Key-to-Index Maps  ->  03-key-to-index-maps.md
04. Grouping Maps  ->  04-grouping-maps.md
05. Set Sequences  ->  05-set-sequences.md
06. Key Equality  ->  06-key-equality.md
07. Direct Addressing  ->  07-direct-addressing.md

# Chapter 04: Hash maps and sets

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| membership | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| counts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| key-to-index lookup | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| grouping | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| set-based sequence reasoning | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| custom-key equality/hash contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| bounded-domain direct-address versus hash representation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Strings And Maps

**What each part contributes.** String traversal supplies characters in a defined order. The map or frequency array supplies remembered counts or a character-to-character correspondence. **Recognition cue.** The question compares, classifies, or constrains characters across one or more strings. **False friend.** A plain scan cannot remember a non-adjacent earlier character; sorting is a later canonicalization tool, not required for every string relation.

- **Build - LC 387 First Unique Character in a String.** Count first, then scan in original order; the map answers frequency while the string supplies the required first occurrence.
- **Vary - LC 242 Valid Anagram.** Replace "first unique" with a two-ledger equality contract.
- **Boundary - LC 205 Isomorphic Strings.** Maintain both directions of the mapping; one-way consistency lets two source characters map to one target character.
- **Recognize - LC 290 Word Pattern.** Tokenize the words, then apply the same bijection invariant between pattern characters and tokens.

### Matrices And Sets

**What each part contributes.** Matrix traversal supplies coordinates. Sets remember which values have already appeared in a row, column, or box. **Recognition cue.** Validity depends on uniqueness within several overlapping scopes. **False friend.** One global set rejects a legal digit appearing in different rows.

- **Build - Author exercise: Row Duplicates.** Given one Sudoku row, ignore `'.'` and reject its first repeated digit.
- **Vary - Author exercise: Row And Column Scope.** Traverse a board and maintain one set per row plus one set per column.
- **Boundary - Author exercise: Box Identity.** Derive a box key from `(row / 3, col / 3)`; test equal digits in different boxes and the same box.
- **Recognize - LC 36 Valid Sudoku.** The complete solution maintains all three scopes without confusing their keys.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `entrySet()` when both map key and value are needed.
- Make map value semantics explicit: count, index, group, or membership.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Strings + Hash Maps | Character counts, bijections, and grouping state; staircase: LC 387 → LC 242 → LC 290 |
| Teach now | Matrices + Hash Sets | Row/column/box membership; staircase: row duplicate → column duplicate → box duplicate → LC 36 |
| Deferred | Strings + Maps + Sorting | Chapter 05 supplies canonical sorted signatures |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Custom-key identity:** add a lesson note that `HashMap`/`HashSet` use logical equality. Records are safe value keys because Java supplies component-based `equals` and `hashCode`; a custom class used as a key must keep those methods consistent, and fields participating in equality must not be mutated while the key is stored.
- **Direct address versus hashing:** contrast `int[26]` with `HashMap<Character, Integer>`. A frequency array is preferable only under a stated compact alphabet/range contract; a map remains the correct general representation for open-ended characters, words, or objects.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** heap top-k, sort-based grouping, two-pointer combinations.

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
