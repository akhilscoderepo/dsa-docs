# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Use ArrayDeque For Stack And Queue  ->  01-arraydeque-contracts.md
02. Process Items In Arrival Order  ->  02-fifo-simulation.md
03. Build A Queue From Two Stacks  ->  03-two-stack-queue.md
04. Find Shortest Steps With A Queue  ->  04-bfs-queue-state.md
05. Check That Brackets Match In Order  ->  05-matching-delimiters.md
06. Save State For Each Nesting Level  ->  06-nested-structure.md
07. Track The Minimum In A Stack  ->  07-min-stack.md
08. Group Queue Items By Level  ->  08-queue-based-level-processing.md
09. Nested Decoding  ->  09-nested-decoding.md
10. Calculator And String Parsing  ->  10-calculator-and-string-parsing.md
11. Infix And Postfix Evaluation  ->  11-infix-and-postfix-evaluation.md

# Chapter 11: Stacks and queues

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| Java APIs and `ArrayDeque` null contract | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| FIFO simulation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| queue via two stacks/amortized transfer | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| BFS queue state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| matching delimiters | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| nested structure | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| min stack | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| queue-based level processing | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| nested decoding | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| calculator/string parsing | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| infix/postfix evaluation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Stack And Parsing State

The parser determines token meaning and grammar position; the stack preserves operands, pending operators, or parent contexts that cannot yet be resolved. A stack alone does not define the grammar, and parsing without saved unresolved state fails on precedence or nesting.

- **Build - LC 150 Evaluate Reverse Polish Notation.** Resolve operators whose operands already appear in evaluation order.
- **Vary - LC 394 Decode String.** Save count and parent-string frames across nested groups.
- **Boundary - LC 71 Simplify Path.** Treat path components as tokens and prevent `..` from moving above the root.
- **Recognize - LC 224 Basic Calculator.** Combine tokenization, signs, and a stack of parent expression states.

### Deferred: Monotonic Stack

Ordinary stacks preserve unresolved order; they do not yet justify removing dominated values. Chapter 12 introduces the ordered-stack invariant and owns next-greater, histogram, and contribution-counting exercises.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `ArrayDeque` for ordinary stack and queue operations rather than legacy `Stack`.
- State whether polling an empty queue is impossible by invariant or handled by contract.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Stack + Parsing State | Nested unresolved tokens; representative: LC 394 and LC 224 |
| Deferred | Monotonic Stack | Chapter 12 supplies ordered stack invariant |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Queue using two stacks:** add the amortized transfer invariant: move items from the input stack to the output stack only when the output stack is empty. This is ordinary FIFO emulation, not a monotonic queue.
- **ArrayDeque null contract:** it rejects `null`. Teach BFS level-size loops or an explicit marker object rather than null sentinels.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** monotonic structures, histogram/contribution counting.

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
