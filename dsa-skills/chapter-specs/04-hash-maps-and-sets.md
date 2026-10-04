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

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0003 | Frequency counting | Contains Duplicate | Direct concept | Introduces membership tracking with a set. |
| P0004 | Frequency counting | Valid Anagram | Immediate application | Same frequency idea, now comparing two inputs. |
| P0005 | Hash lookup | Two Sum | Small extension | Turns repeated search into constant-time lookup. |
| P0006 | Hash lookup | Isomorphic Strings | Small extension | Extends one-way lookup into a consistent mapping. |
| Bundle 1-1 | Lookup | Two Sum | Learn | — |
| Bundle 1-2 | Lookup | Contains Duplicate | Extend | — |
| Bundle 1-3 | Lookup | Group Anagrams | Twist | — |
| Bundle 2-11 | String DP | Word Break | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Seen-before state | Need only membership | Only existence matters; no ordering/frequency required | https://leetcode.com/problems/contains-duplicate/ | Core |
| Increment/decrement counts | Need counts | Count is the minimal state needed for frequency requirements | https://leetcode.com/problems/group-anagrams/ | Core |
| Normalize then hash | Need group equivalent objects | Equal canonical forms imply same equivalence class | https://leetcode.com/problems/group-anagrams/ | Core |
| Store first occurrence only | Need longest span where state repeats | Earliest occurrence gives maximum span | https://leetcode.com/problems/contiguous-array/ | Intermediate |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Strings + Hash Maps | LC 387 First Unique Character in a String | LC 242 Valid Anagram | LC 205 Isomorphic Strings | LC 290 Word Pattern |
| Matrices + Hash Sets | Author drill: detect a duplicate in one Sudoku row | Author drill: enforce row and column membership | Author drill: include 3×3 box membership | LC 36 Valid Sudoku |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

Each structure earns its place by storing exactly the information the next decision needs. The point is not to reach automatically for a `HashMap`; it is to say what a key means, what its value means, and why order is irrelevant.

### Check Membership With A Set

**Recognition cue.** The question asks whether something has appeared, exists, or is forbidden; its count and order do not matter. **State.** `seen` contains exactly the relevant values processed so far. **False friend.** A map is needless when membership alone answers the question.

- **Build - LC 217 Contains Duplicate.** Given `nums`, return whether any value appears at least twice. `[1,2,3,1] -> true`; `[1,2,3,4] -> false`. Hint: what fact must be remembered after each value?
- **Vary - LC 349 Intersection of Two Arrays.** Return the distinct values present in both arrays. `[1,2,2,1], [2,2] -> [2]`; `[], [1] -> []`.
- **Boundary - LC 202 Happy Number.** Detect the repeated numeric state rather than allowing an infinite loop. `19 -> true`; `2 -> false`.
- **Recognize - LC 128 Longest Consecutive Sequence.** Start only at values whose predecessor is absent; this prevents repeatedly expanding the same run.

### Count Values With A Map

**Recognition cue.** The decision depends on multiplicity, not just existence. **State.** `count.get(key)` means the exact processed frequency, including the convention for absent keys. **False friend.** A set silently loses the count needed for an anagram or top-frequency decision.

- **Build - LC 387 First Unique Character in a String.** Return the first index with frequency one. `"leetcode" -> 0`; `"aabb" -> -1`.
- **Vary - LC 242 Valid Anagram.** Compare two frequency ledgers. `"anagram", "nagaram" -> true`; `"rat", "car" -> false`.
- **Boundary - Author exercise: Remove Zero Counts.** Process additions and removals; delete a key precisely when its count returns to zero. This prevents an empty count from being mistaken for membership.
- **Recognize - LC 1207 Unique Number of Occurrences.** Count each value with a map, then use a set to verify that no two values have the same frequency.

### Remember Where A Value Appeared

**Recognition cue.** A current value needs one earlier location or complement immediately. **State.** The map records the index meaning stated by the contract: usually the earliest usable index, or the most recent one. **False friend.** Sorting changes original-index requirements and is not a substitute for remembered lookup.

- **Build - LC 1 Two Sum.** Given `nums` and `target`, return indices of two values summing to `target`. `[2,7,11,15], 9 -> [0,1]`; `[3,3], 6 -> [0,1]`.
- **Vary - LC 219 Contains Duplicate II.** Store the last seen index and compare the gap to `k`.
- **Boundary - Author exercise: First Index Wins.** Given repeated values, preserve the first index when the output requires the widest valid pair; name why overwriting would change the answer.
- **Recognize - Author exercise: Widest Equal-Value Pair.** Store the first index of each value and return the largest distance between two equal values.

### Group Values In A Map

**Recognition cue.** Several inputs belong to the same output bucket under a stated equivalence relation. **State.** `groups.get(key)` owns the full list for one equivalence class. **False friend.** A frequency map tells how many; it does not preserve the members required by grouped output.

- **Build - Author exercise: Group by Remainder.** Given `nums` and `m`, return groups keyed by `Math.floorMod(value, m)`. `[1,4,2,5], 3 -> [[1,4],[2,5]]`.
- **Vary - LC 1282 Group the People Given the Group Size They Belong To.** A key owns an in-progress bucket that is emitted only when full.
- **Boundary - Author exercise: Empty Buckets.** Do not return keys that received no values; map creation must be demand-driven.
- **Recognize - LC 49 Group Anagrams.** Use a fixed-alphabet count signature as the grouping key; the map owns the buckets for equal signatures.

### Extend Runs With A Set

**Recognition cue.** A numeric sequence can be extended by local predecessor/successor membership tests. **State.** The set describes the complete input; iteration begins only from a sequence start. **False friend.** Sorting can also expose runs, but it mutates or costs `O(n log n)` when a set gives expected `O(n)` time.

- **Build - LC 128 Longest Consecutive Sequence.** Begin at `x` only when `x - 1` is absent.
- **Vary - LC 349 Intersection of Two Arrays.** Use membership across two collections while emitting each shared value once.
- **Boundary - Author exercise: Duplicate Starts.** Insert duplicates into the set first, then prove they cannot create duplicate runs.
- **Recognize - LC 202 Happy Number.** Store previously seen states in a set and stop when the numeric sequence reaches `1` or repeats.

### Use Records As Keys

**Recognition cue.** The key is a compound value such as a coordinate, pair, or application object. **State.** Equal logical keys must have equal hashes, and their equality fields must not mutate while stored. **Java hazard.** Use an immutable record or a correctly implemented `equals`/`hashCode`; reference equality is not logical equality.

- **Build - Author exercise: Count Coordinates.** Given `Point(row, col)` observations, count logically equal coordinates using `record Point(int row, int col) {}`.
- **Vary - Author exercise: Undirected Edge Key.** Normalize `(a,b)` and `(b,a)` to the same immutable key before insertion.
- **Boundary - Author exercise: Mutable-Key Failure.** Explain why mutating a field that participates in `hashCode` after insertion makes a stored entry effectively unreachable.
- **Recognize - Author exercise: Count Directed Transitions.** Use an immutable `Pair(from, to)` record as a frequency-map key while keeping `(a, b)` distinct from `(b, a)`.

### Choose An Array Or A Map

**Recognition cue.** A compact, known domain makes an array a more direct representation than a map. **State.** `count[value - min]` maps the declared range to slots; a `HashMap` remains the general representation for sparse or open-ended keys. **False friend.** Do not claim `int[26]` works for arbitrary Unicode text.

- **Build - Author exercise: Lowercase Character Counts.** Count `a` through `z` with `int[26]` under an explicit lowercase-English contract.
- **Vary - LC 242 Valid Anagram.** Replace a map with a frequency array only after the alphabet contract is stated.
- **Boundary - Author exercise: Sparse IDs.** Explain why values `{2, 1_000_000_000}` reject direct addressing even though both are integers.
- **Recognize - LC 706 Design HashMap.** The prompt removes the compact-domain guarantee; a general hash representation is now justified.

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

