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

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Push unresolved state | Nested/reversible operations | Nested structures resolve in reverse order | https://leetcode.com/problems/valid-parentheses/ | Core |
| Preserve arrival order | Work must be processed first-in, first-out | Enqueue at the back and remove from the front | https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/ | Core |
| Transfer only when output is empty | Implement FIFO with two LIFO containers | Each element enters and leaves each stack at most once | https://leetcode.com/problems/implement-queue-using-stacks/ | Core |
| Save one frame per nesting level | Decode or evaluate nested syntax | A closing token resolves the most recent unfinished parent state | https://leetcode.com/problems/decode-string/ | Intermediate |
| Capture current queue size | Process one BFS level at a time | Newly enqueued states belong to the next level | https://leetcode.com/problems/binary-tree-level-order-traversal/ | Core; application deferred to Chapter 16 |
| Pop operands in right-then-left order | Evaluate postfix expressions | Every operator consumes already completed operand values | https://leetcode.com/problems/evaluate-reverse-polish-notation/ | Core |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Stack + Parsing State | LC 150 Evaluate Reverse Polish Notation | LC 394 Decode String | LC 71 Simplify Path | LC 224 Basic Calculator |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Use ArrayDeque For Stack And Queue

**Recognition cue.** The algorithm needs LIFO or FIFO access with no indexed search. **Invariant.** One chosen end has one meaning throughout the implementation. Use `addLast/removeLast/peekLast` for a stack or `addLast/removeFirst/peekFirst` for a queue. **False friend.** Java's legacy `Stack` works but is not the preferred ordinary stack. **Java hazard.** `ArrayDeque` rejects `null`, so `null` cannot be a level delimiter.

- **Build - Author exercise: Deque As Stack.** Push three integers and return them in reverse insertion order.
- **Vary - Author exercise: Deque As Queue.** Enqueue the same values and return them in insertion order.
- **Boundary - Author exercise: Empty Access Contract.** Compare exception-throwing `remove`/`get` operations with null-returning `poll`/`peek`, without storing null elements.
- **Recognize - Author exercise: Choose The Ends.** Label the exact deque operations for a LIFO undo log and a FIFO request buffer.

### Process Items In Arrival Order

**Recognition cue.** Items must be handled in arrival order while later arrivals wait behind earlier ones. **Invariant.** The front is the next item to process and every enqueued item appears behind all items already present. **False friend.** A stack reverses arrival order.

- **Build - Author exercise: Printer Queue.** Process job IDs in the order received.
- **Vary - Author exercise: Round-Robin One Step.** Remove the front task, decrement its remaining work, and re-enqueue it only when unfinished.
- **Boundary - Author exercise: Queue Becomes Empty.** Guard or prove every removal and handle a task completed on its first turn.
- **Recognize - LC 1700 Number of Students Unable to Eat Lunch.** Simulate only while progress is possible and detect a full unsuccessful rotation.

### Build A Queue From Two Stacks

**Recognition cue.** Only LIFO containers are available, but the public API must be FIFO. **Invariant.** New values enter `in`; the oldest available values are on top of `out`. Transfer all values only when `out` is empty. **False friend.** Moving everything on every operation is correct but costs linear time per call.

- **Build - Author exercise: Enqueue And One Dequeue.** Transfer `in` to `out` and observe the reversal.
- **Vary - Author exercise: Interleaved Queue Calls.** Enqueue while `out` remains nonempty and preserve older values ahead of new ones.
- **Boundary - Author exercise: Empty Queue API.** Make `peek` and `pop` follow the stated nonempty-call contract or document the chosen failure behavior.
- **Recognize - LC 232 Implement Queue using Stacks.** Implement the full API and explain why each element moves between stacks at most once.

### Find Shortest Steps With A Queue

**Recognition cue.** States are explored in nondecreasing number of transitions from a start. **Invariant.** The queue contains discovered but unprocessed states; each state is marked when enqueued so it is not scheduled twice. **False friend.** A stack explores deeply and does not preserve shortest unweighted transition count. Full graph modeling arrives in Chapter 21.

- **Build - Author exercise: Process A Supplied Frontier.** Remove states from a queue and append their already-supplied unseen successors.
- **Vary - Author exercise: Minimum Add-One Or Double Steps.** Search integer states within a stated bound and return the first distance to a target.
- **Boundary - Author exercise: Start Is Target.** Return distance zero before generating successors and mark states at enqueue time.
- **Recognize - Author exercise: Shortest Word Transform From Supplied Neighbors.** Use the queue invariant without requiring graph construction techniques not yet taught.

### Check That Brackets Match In Order

**Recognition cue.** Every closing symbol must match the most recent unresolved compatible opening symbol. **Invariant.** The stack stores exactly the openings not yet matched, in nesting order. **False friend.** Equal counts do not prove correct order.

- **Build - Author exercise: One Bracket Type.** Validate parentheses by pushing openings and resolving closings.
- **Vary - LC 20 Valid Parentheses.** Match three delimiter types against the stack top.
- **Boundary - Author exercise: Premature Close And Leftover Open.** Reject both an empty-stack close and a nonempty stack after the scan.
- **Recognize - LC 1021 Remove Outermost Parentheses.** Use nesting depth to omit the first opening and final closing of each primitive group.

### Save State For Each Nesting Level

**Recognition cue.** Inner structures must finish before their enclosing structures can be finalized. **Invariant.** Each stack frame contains the unresolved state of one nesting level. **False friend.** A single global accumulator loses the parent state when nesting begins.

- **Build - Author exercise: Maximum Parenthesis Depth.** Track opened but unresolved levels.
- **Vary - Author exercise: Sum Values By Nested Group.** Save a parent accumulator when entering a group and restore it when leaving.
- **Boundary - Author exercise: Deep Single Chain.** Trace nested empty groups and reject unbalanced input under the stated contract.
- **Recognize - LC 856 Score of Parentheses.** Resolve each completed nested group into the value expected by its parent.

### Min Stack

**Recognition cue.** Ordinary stack operations must additionally return the current minimum in constant time. **Invariant.** Each depth stores enough information to recover the minimum for exactly that prefix of the stack. **False friend.** Scanning for the minimum on demand violates the operation contract.

- **Build - Author exercise: Value-Min Pairs.** Push each value with `min(value, previousMin)`.
- **Vary - Author exercise: Two-Stack Minimum.** Store a value on the minimum stack when it is no greater than the current minimum.
- **Boundary - Author exercise: Duplicate Minima.** Push the same minimum twice and ensure one pop does not lose it.
- **Recognize - LC 155 Min Stack.** Implement `push`, `pop`, `top`, and `getMin` with constant-time worst-case operations.

### Queue-Based Level Processing

**Recognition cue.** Work must be grouped by its distance or batch level, and all items currently in the queue belong to the present level. **Invariant.** Capture `levelSize = queue.size()` before the inner loop; exactly those items form the current level. **Java hazard.** Do not use a null sentinel with `ArrayDeque`. Tree level order is applied in Chapter 16.

- **Build - Author exercise: Process Queue In Batches.** Given items that append next-batch items, return the IDs processed at each level.
- **Vary - Author exercise: Count Levels To First Target.** Increment distance after processing one captured batch.
- **Boundary - Author exercise: Expanding Queue.** Prove newly enqueued items are excluded from the current batch despite increasing `queue.size()`.
- **Recognize - Author exercise: Alternate Level Output.** Reverse only the reported order for every other level while preserving FIFO discovery.

### Nested Decoding

**Recognition cue.** A repetition count applies to a bracketed substring that may itself contain encoded groups. **Invariant.** On `[`, save the parent string state and repeat count; on `]`, resolve the current group into its parent. **False friend.** Repeating immediately at each digit fails for multi-digit counts and nesting.

- **Build - Author exercise: Decode One Flat Group.** Decode a single form such as `3[ab]`.
- **Vary - Author exercise: Multi-Digit Repeat Count.** Accumulate `count = count * 10 + digit`.
- **Boundary - Author exercise: Adjacent And Nested Groups.** Decode an input such as `2[a]3[b2[c]]` without mixing frames.
- **Recognize - LC 394 Decode String.** Implement the complete nested grammar using saved counts and parent builders.

### Calculator And String Parsing

**Recognition cue.** Characters form multi-digit numbers and operators whose effect may be delayed by precedence or parentheses. **Invariant.** At each token boundary, the parser has a precise meaning for the accumulated number, pending sign/operator, and saved parent context. **False friend.** Splitting on spaces fails when spaces are optional or parentheses are present.

- **Build - Author exercise: Signed Sum.** Parse multi-digit integers joined by `+` and `-`.
- **Vary - LC 227 Basic Calculator II.** Resolve multiplication and division before committing lower-precedence terms.
- **Boundary - Author exercise: Spaces And Unary Sign.** Distinguish a binary operator from a leading or post-parenthesis unary sign under the chosen grammar.
- **Recognize - LC 224 Basic Calculator.** Save the outer result and sign at `(`, then fold the completed inner expression at `)`.

### Infix And Postfix Evaluation

**Recognition cue.** Operators must be applied either from explicit postfix order or after infix precedence has been made explicit. **Invariant.** In postfix evaluation, the value stack contains completed operands; for a binary operator, pop right before left. **False friend.** Reversing operand order is invisible for addition but breaks subtraction and division.

- **Build - Author exercise: Evaluate One Postfix Operator.** Compute tokens `a b op` with correct operand order.
- **Vary - LC 150 Evaluate Reverse Polish Notation.** Process arbitrary valid postfix tokens with one value stack.
- **Boundary - Author exercise: Non-Commutative Trace.** Test `8 3 -` and integer division with negative values under Java semantics.
- **Recognize - Author exercise: Convert Simple Infix To Postfix.** Use an operator stack for `+`, `-`, `*`, and `/`, then evaluate with the already learned postfix engine.

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

