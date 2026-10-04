# Chapter 00: Problem contracts, complexity, and sequence language

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| constraints as algorithm signals | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| mutation/space contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| subarray versus subsequence | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| input guarantees | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| complexity tradeoffs | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| amortized analysis (accounting/potential intuition) | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| adversarial dry-runs | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Java API/code-quality habits | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.

### Pattern References

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.


### Released Combination Ladders

No combination is released by this chapter's current prerequisite boundary. The visible deferred entries below remain ownership notes, not premature exercises.


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

This chapter teaches the language used to reason about every later problem. Its exercises are deliberately small: the learner should practice reading a contract, predicting a cost, and constructing a hostile test before a named algorithm competes for attention.

### Analyzing Input Limits And Operation Budgets

**Recognition cue.** The input limits rule out entire classes of solutions before code is written. **State.** Record the largest possible input size, value range, and required operation count. **Invariant.** A proposed approach must remain within its time and memory budget at the maximum legal input. **False friend.** Difficulty labels and familiar nouns such as “array” do not select an algorithm; the contract does.

- **Build - Author exercise: Budget Check.** Given `1 <= n <= 100_000`, classify a single scan, an `O(n log n)` sort, and an all-pairs `O(n^2)` comparison as plausible or implausible for an ordinary interview time limit. Hint: estimate growth at the maximum `n`, not at the sample input.
- **Vary - Author exercise: Small Domain.** Given `1 <= n <= 100_000` and `0 <= nums[i] <= 100`, explain why an auxiliary array of 101 counters may be reasonable even though an array indexed by arbitrary integer values would not be.
- **Boundary - Author exercise: Hidden Overflow.** Given `n = 100_000` and `|nums[i]| <= 1_000_000_000`, decide whether the total sum fits in Java `int`. The hostile case is one hundred thousand maximum positive values.
- **Recognize - Author exercise: Query Pressure.** Compare one range-sum query with one hundred thousand range-sum queries over unchanged data. State why the number of operations, rather than the word “array,” changes the acceptable design. The later Prefix Sum chapter owns the implementation.

### Specifying Preconditions, Postconditions And Mutation

**Recognition cue.** The prompt states whether the input may change and whether extra storage counts against the target. **State.** Separate the physical container from the logical result. **Invariant.** Every write preserves data still needed by a later read. **False friend.** “In place” does not mean “the Java array becomes shorter,” and output storage required by the return value is not always counted as auxiliary space.

- **Build - Author exercise: Meaningful Prefix.** Given `nums = [3,2,2,3]`, suppose a method returns `k = 2` after filtering `3`. State precisely what is guaranteed about `nums[0..k-1]` and what is unspecified about the suffix.
- **Vary - Author exercise: Preserve Input.** Given a contract that forbids mutation, choose between overwriting `nums` and allocating `result`. Explain why a correct value with a modified input still violates the API.
- **Boundary - Author exercise: Aliased Input.** Two variables refer to the same array. Trace why mutating through one reference is observable through the other. The exercise changes no algorithm; it changes the caller-visible contract.
- **Recognize - Author exercise: Output Space.** A method must return an array of length `n`. Distinguish the `O(n)` returned output from additional working memory, then state both conventions explicitly instead of hiding one.

### Defining Subarrays, Subsequences And Subsets

**Recognition cue.** The prompt uses terms such as subarray, substring, subsequence, subset, prefix, or suffix. **State.** Write down which index relationships must be preserved. **Invariant.** A subarray/substring occupies consecutive positions; a subsequence preserves relative order but may skip positions; a subset need not preserve either adjacency or order. **False friend.** These words are not interchangeable even when a sample answer happens to satisfy several definitions.

- **Build - Author exercise: Classify `[2,4]`.** For `nums = [1,2,3,4]`, decide whether `[2,4]` is a subarray, subsequence, and subset. Explain each answer from index positions.
- **Vary - Author exercise: Order Matters.** For the same input, classify `[4,2]`. The changed decision is whether original relative order must be preserved.
- **Boundary - Author exercise: Empty Choice.** State whether an empty subarray or subsequence is legal only after reading the problem’s non-empty/empty contract; do not assume one universal convention.
- **Recognize - Author exercise: Contiguous Maximum.** Explain why “maximum sum subarray” cannot freely skip a negative middle value, while a maximum-sum subsequence may. Kadane’s algorithm remains deferred to Chapter 01.

### Input Preconditions And Defensive Assumptions

**Recognition cue.** Correct initialization and guards depend on facts promised by the caller: non-empty input, sorted order, legal indices, rectangular shape, or bounded values. **State.** List guarantees separately from assumptions introduced by the solution. **Invariant.** Code may rely on a documented guarantee but must not invent one. **False friend.** Defensive branches added from habit can obscure the actual algorithm and may define behavior the problem never requested.

- **Build - Author exercise: Non-Empty Maximum.** Given a non-empty array contract, initialize a maximum from `nums[0]`. Explain why initializing from zero fails for `[-8,-3]` and why an empty-array guard is unnecessary under this exact contract.
- **Vary - Author exercise: Possibly Empty.** Change the contract to allow an empty array. Choose and document one response: sentinel, exception, or optional result. The method signature must agree with that choice.
- **Boundary - Author exercise: Rectangular Or Ragged.** For `int[][] grid`, distinguish a rectangular guarantee from a ragged array. Explain why `grid[0].length` is unsafe as the bound for every row when ragged input is legal.
- **Recognize - Author exercise: Sorted Promise.** Show which conclusion becomes valid when an array is guaranteed sorted: equal values form adjacent runs. Do not yet introduce binary search or two pointers.

### Comparing Time And Space Complexity Trade-Offs

**Recognition cue.** Two correct solutions consume different combinations of time, memory, preprocessing, or mutation. **State.** Name `n`, any secondary dimension, and the exact operation being counted. **Invariant.** The stated bound must describe the dominant work on the worst legal input. **False friend.** Two loops written next to each other are additive; two loops nested over the same growing input are usually multiplicative.

- **Build - Author exercise: Consecutive Loops.** Determine the time cost of scanning an `n`-element array twice. Explain why `O(n) + O(n)` simplifies to `O(n)`.
- **Vary - Author exercise: Triangular Work.** Count iterations of `for (i = 0; i < n; i++) for (j = i + 1; j < n; j++)`. Derive `n(n-1)/2` and classify it as `O(n^2)`.
- **Boundary - Author exercise: Two Dimensions.** A grid has `rows` and `cols`. State traversal time as `O(rows * cols)` rather than silently calling both dimensions `n`.
- **Recognize - Author exercise: Sort Then Scan.** Compare `O(n^2)` all-pairs work with `O(n log n)` sorting followed by `O(n)` scanning. State the tradeoff: changed order, possible mutation/copying, and lower asymptotic time.

### Amortized Analysis Of Operation Sequences

**Recognition cue.** An operation is usually cheap but occasionally performs a large repair or resize whose cost is spread across many earlier/later operations. **State.** Track stored “credit” or a potential such as unused capacity. **Invariant.** Across a sequence of operations, the total charged cost pays for every actual operation. **False friend.** Amortized `O(1)` is not worst-case `O(1)` for each individual call.

- **Build - Author exercise: Doubling Array.** Start with capacity 1 and append eight values, doubling whenever full. List capacities `1,2,4,8` and count all element copies. Observe that the total copies remain proportional to the number of appends.
- **Vary - Author exercise: Grow By One.** Repeat the experiment when capacity increases by exactly one. Sum `1 + 2 + ... + (n-1)` and explain why append becomes `O(n)` amortized rather than `O(1)`.
- **Boundary - Author exercise: One Expensive Append.** Identify the append that triggers an `O(n)` copy and reconcile it with an `O(1)` amortized bound over the whole sequence.
- **Recognize - Author exercise: Potential Intuition.** Treat unused slots after doubling as prepaid capacity. Explain, without formal algebra, how this stored potential funds future cheap appends and the next resize.

### Designing Adversarial Test Inputs

**Recognition cue.** A plausible implementation depends on an unstated happy-path assumption. **State.** Select the smallest input that attacks initialization, equality, boundaries, overflow, or mutation order. **Invariant.** A dry run must track variable meanings after every state change, not merely reproduce the sample output. **False friend.** Large random tests are poor substitutes for a tiny case designed around one failure mode.

- **Build - Author exercise: Singleton.** Dry-run a loop over `[7]`. Verify initialization, the number of iterations, and the returned value.
- **Vary - Author exercise: All Equal.** Use `[4,4,4]` to test strict versus non-strict comparisons and duplicate handling.
- **Boundary - Author exercise: Numeric Extremes.** Use `[Integer.MAX_VALUE, Integer.MAX_VALUE]` against code that accumulates into `int`; predict the overflow before running it.
- **Recognize - Author exercise: Mutation Order.** For right-shifting `[1,2,3]` to insert at index 0, trace a left-to-right copy and show exactly where data is overwritten. Then justify right-to-left copying.

### Java Library Call Time And Space Costs

**Recognition cue.** A Java library call appears inside a loop or silently changes representation. **State.** Include the API operation’s actual cost and semantics in the algorithm analysis. **Invariant.** Convenience syntax must not invalidate the target complexity or output contract. **False friend.** Familiar-looking APIs are not automatically constant time, primitive-friendly, or value-based.

- **Build - Author exercise: Front Removal.** Explain why repeatedly calling `ArrayList.remove(0)` over `n` elements performs quadratic shifting. Contrast it with maintaining a read index.
- **Vary - Author exercise: String Construction.** Compare `result = result + ch` in a loop with `StringBuilder.append(ch)`. Explain where repeated copying occurs.
- **Boundary - Author exercise: Primitive Arrays.** Evaluate `Arrays.asList(new int[]{1,2,3})`. State why the result is a one-element `List<int[]>`, not `List<Integer>`.
- **Recognize - Author exercise: Value Equality.** Compare two distinct `String` objects containing the same characters. Explain why `.equals` expresses value equality while `==` tests reference identity.

## Foundation Exit Check

Before Chapter 01, the learner should be able to read a prompt and state: the meaningful input guarantees; whether mutation is allowed; what output portion is valid; the sequence relationship being requested; the plausible time/space budget; one adversarial test; and any Java API operation that changes the claimed complexity. No new algorithm is unlocked here, but every later lesson assumes this language.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- State the input and mutation contract before writing guards.
- Name asymptotic costs of the Java operation actually used.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| No teach-now combination | Foundations only | Specific structures and algorithms |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** specific data structures and algorithms.

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

