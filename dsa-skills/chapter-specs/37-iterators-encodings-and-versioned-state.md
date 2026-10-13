# Chapter 37: Iterators, encodings, and versioned state

**Status:** Authored curriculum specification; PDF generation remains pending.

## Purpose

Teach APIs that expose a large or structured value incrementally, encode it for later reconstruction, or answer queries against a historical version.

## Entry Contract

Stacks, queues, trees, tries, prefix sums, binary lifting, and ordinary iterator state are prerequisites. The chapter distinguishes materialized output from resumable state.

## Mastery Scope

The required LeetCode anchors are LC 900, LC 1286, LC 1146, and LC 2080. LC 449 and LC 1993 are transfer problems. Other numbered problems in this specification are taxonomy examples or prerequisite reviews; they are not assigned work and do not receive complete solutions in the PDF.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| iterator protocol state | Separate observation, availability, consumption, and exhaustion. |
| nested and multi-source iteration | Preserve unfinished traversal state without flattening the entire input. |
| structural codecs | Make encoding unambiguous and decoding consume exactly one representation. |
| versioned snapshots | Separate logical versions from physical copies through change histories. |
| preprocessed query objects | Spend constructor work to make repeated queries cheaper. |
| incremental tree APIs | Maintain traversal or hierarchy state as the represented tree changes. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

### Supplied Progression

The crosswalk assigns 18 Design-tag problems here, in addition to iterator, serialization, and snapshot foundations already introduced in Chapters 16 and 33.

### Pattern References

| Micro-pattern | Recognition cue | Representative progression |
| --- | --- | --- |
| Iterator protocol | `hasNext`, `next`, or `peek` across calls | LC 284, LC 604, LC 900 |
| Nested iteration | Several sequences form one logical stream | LC 251, LC 281, LC 341, LC 1286 |
| Codec | Reconstruct exact structure from a sequence | LC 271, LC 297, LC 431, LC 449 |
| Snapshot history | Query state at an earlier version | LC 1146, LC 981 |
| Preprocessed query | Constructor precedes many related queries | LC 244, LC 1570, LC 2080 |
| Incremental tree API | Tree traversal/state survives public calls | LC 919, LC 1586, LC 1600, LC 1993 |

### Released Combination Ladders

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Iterator + Traversal State | LC 284 | LC 900 | LC 341 | LC 1586 |
| Codec + Structural Traversal | Author string codec | LC 297 | LC 431 | LC 449 |
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Iterator Protocols

**Recognition cue.** A class reveals one logical sequence over multiple calls. **Invariant.** Observation does not consume, consumption advances once, and exhaustion behavior is explicit.

- **Build - Author exercise: Array Iterator.** Define `hasNext` and `next` around one cursor.
- **Vary - LC 284 Peeking Iterator.** Cache one element for nonconsuming observation.
- **Boundary - LC 604 Design Compressed String Iterator.** Skip exhausted runs and handle multi-digit counts.
- **Recognize - LC 900 RLE Iterator.** Consume a requested number of logical elements without expanding runs.

### Nested Iteration

**Recognition cue.** Several arrays, iterators, or nested values must appear as one lazy sequence. **Invariant.** The state identifies exactly the next nonempty source and its local cursor.

- **Build - LC 251 Flatten 2D Vector.** Skip empty rows lazily.
- **Vary - LC 281 Zigzag Iterator.** Rotate only among sources that still contain values.
- **Boundary - LC 341 Flatten Nested List Iterator.** Descend through arbitrarily empty nested lists.
- **Recognize - LC 1286 Iterator for Combination.** Generate the next lexicographic combination from index state.

### Structural Codecs

**Recognition cue.** A structured value must cross a flat string or tree boundary and be reconstructed exactly. **Invariant.** Every encoded unit has an unambiguous boundary and every decoder step consumes one complete unit.

- **Build - LC 271 Encode and Decode Strings.** Use length framing instead of a fragile delimiter.
- **Vary - LC 297 Serialize and Deserialize Binary Tree.** Preserve shape with null markers.
- **Boundary - LC 431 Encode N-ary Tree to Binary Tree.** Preserve child order and empty child lists.
- **Recognize - LC 449 Serialize and Deserialize BST.** Use the BST ordering contract to reduce structural metadata.

### Version Histories

**Recognition cue.** Updates create versions and later queries name an earlier version or time. **Invariant.** Each index/key stores a monotone history; a query selects the latest change not after the requested version.

- **Build - Author exercise: Versioned Integer.** Append `(version,value)` changes.
- **Vary - LC 1146 Snapshot Array.** Store only changed indices per snapshot.
- **Boundary - Author exercise: Repeated Writes Before Snap.** Coalesce writes with the same version.
- **Recognize - LC 981 Time Based Key-Value Store.** Binary-search per-key timestamp histories.

### Query Objects

**Recognition cue.** A constructor receives stable data and many queries follow. **Invariant.** Preprocessing preserves exactly the information needed by the query while avoiding repeated full scans.

- **Build - LC 244 Shortest Word Distance II.** Store sorted positions per word.
- **Vary - LC 1570 Dot Product of Two Sparse Vectors.** Iterate only represented nonzero entries.
- **Boundary - LC 288 Unique Word Abbreviation.** Distinguish one owning word from collisions among different words.
- **Recognize - LC 2080 Range Frequency Queries.** Binary-search first and last relevant positions.

### Incremental Trees

**Recognition cue.** Public methods modify or navigate a tree while retaining auxiliary state. **Invariant.** The stored frontier, parent relation, or traversal history remains consistent with the current tree.

- **Build - LC 919 Complete Binary Tree Inserter.** Keep the queue of nodes missing children.
- **Vary - LC 1586 Binary Search Tree Iterator II.** Add backward navigation without rebuilding traversal state.
- **Boundary - LC 1261 Find Elements in a Contaminated Binary Tree.** Recover membership without relying on corrupted values.
- **Recognize - LC 1993 Operations on Tree.** Maintain lock rules involving ancestors and descendants.

## Released Combination Lessons

### Iterator Traversal State

- **Build - LC 284 Peeking Iterator.** Separate cached observation from source advancement.
- **Vary - LC 900 RLE Iterator.** Advance by a logical count.
- **Boundary - LC 341 Flatten Nested List Iterator.** Skip empty nested containers.
- **Recognize - LC 1586 Binary Search Tree Iterator II.** Preserve reversible traversal history.

### Codec Structural Traversal

- **Build - Author exercise: Length-Prefixed String Codec.** Make token boundaries explicit.
- **Vary - LC 297 Serialize and Deserialize Binary Tree.** Preserve null structure.
- **Boundary - LC 431 Encode N-ary Tree to Binary Tree.** Preserve ordered child ownership.
- **Recognize - LC 449 Serialize and Deserialize BST.** Exploit ordering without losing reconstructability.

## Practice Contract

Each independent protocol retains a Build-to-Recognize staircase, but the early roles may be cursor traces, encoding drills, or invariant checks rather than full LeetCode solutions. Fully expand the four required anchors; present the two transfer problems as interview prompts with hints and review notes rather than complete code.

## Java Integrity Focus

- State whether exhausted `next()` is forbidden or throws.
- Avoid recursive eager flattening when the contract requires lazy iteration.
- Use `long` for version/timestamp arithmetic when constraints require it.

## Unlocked Combinations Preview

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Iterator + Traversal State | Stack/cursor state must survive arbitrary call sequences. |
| Teach now | Codec + Structural Traversal | Encoding and decoding share one grammar and shape contract. |
| Already covered | Binary lifting | Chapter 29/30 foundations support LC 1483 as advanced review. |

## Composition Audit

The chapter releases iterator/tree, string/codec, and binary-search/history combinations because all participating techniques are already taught.

## Publication Gate

- Trace repeated `hasNext`, `peek`, exhaustion, and malformed-boundary cases.
- Verify every codec is injective over the stated input domain.
- Check historical queries at versions before the first and after the last update.
- Render and validate the final PDF.

## Research Baseline

- [LeetCode Design problem list](https://leetcode.com/problem-list/design/).
- [Design-tag crosswalk](../design-tag-crosswalk.md).
- Oracle Iterator and Collections documentation.

