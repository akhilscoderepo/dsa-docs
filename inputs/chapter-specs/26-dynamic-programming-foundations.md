# Chapter 26: Dynamic programming: foundations

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| state definition | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| memoization/tabulation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| linear recurrence | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| take/skip state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| rolling-state compression | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| feasibility/count/minimize objectives | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| grid DP | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| transition discipline | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0121 | DP foundations | Fibonacci Number | Direct concept | Shows overlapping subproblems and state compression. |
| P0122 | DP foundations | Climbing Stairs | Immediate application | Same recurrence with a combinatorial interpretation. |
| P0123 | 1D take/skip | House Robber | New subtopic | Introduces take/skip state. |
| P0124 | 1D take/skip | House Robber II | Immediate application | Breaks a circular dependency into two linear cases. |
| P0125 | 1D optimization | Min Cost Climbing Stairs | Small extension | Changes the objective while preserving the 1D state structure. |
| P0126 | Unbounded choices | Coin Change | New subtopic | Builds each amount from smaller amounts with reusable choices. |
| P0129 | Grid DP | Unique Paths | New subtopic | Introduces 2D state from neighboring cells. |
| P0130 | Grid DP | Minimum Path Sum | Immediate application | Changes counting paths into minimizing accumulated cost. |
| P0133 | String DP | Word Break | New variation | Builds valid prefixes using dictionary membership. |
| P0135 | Tree / graph DP | House Robber III | Combination | Applies take/skip state to a tree. |
| Bundle 1-1 | 1D | Climbing Stairs | Learn | — |
| Bundle 1-2 | 1D | Min Cost Climbing Stairs | Extend | — |
| Bundle 1-3 | 1D Decision | House Robber | Twist | — |
| Bundle 1-1 | Grid | Unique Paths | Learn | — |
| Bundle 1-2 | Grid | Minimum Path Sum | Extend | — |
| Bundle 1-3 | Grid | Maximal Square | Twist | — |
| Bundle 1-1 | State Machine | Best Time to Buy and Sell Stock with Cooldown | Learn | — |
| Bundle 1-2 | State Machine | Best Time to Buy and Sell Stock with Transaction Fee | Extend | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| State + transition | Best/count up to index | Overlapping subproblems are reused | https://leetcode.com/problems/house-robber/ | Core |
| Take/skip + reverse capacity | Choose/skip items with one-use constraint | Reverse order prevents using same item multiple times | https://leetcode.com/problems/partition-equal-subset-sum/ | Core |
| Forward capacity | Items reusable unlimited times | Forward order allows reuse | https://leetcode.com/problems/coin-change/ | Core |
| Add predecessor ways | Need count ways | Each valid construction contributes exactly once | https://leetcode.com/problems/coin-change-ii/ | Core |
| dp[i][j] | Compare prefixes of two sequences | Every pair of prefixes is a reusable subproblem | https://leetcode.com/problems/longest-common-subsequence/ | Core |
| Predecessor aggregation | Grid path count/cost | Every path enters through known predecessor states | https://leetcode.com/problems/minimum-path-sum/ | Core |
| Explicit action states | Action changes future options | Future possibilities depend on a compact state, not full history | https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/ | Intermediate |
| Best ending at i | Subsequence order matters | Every increasing subsequence ending at i has one compatible predecessor | https://leetcode.com/problems/longest-increasing-subsequence/ | Core |
| Smallest tail frontier | LIS state can be compressed/optimized | Smaller tail dominates larger tail for the same length | https://leetcode.com/problems/longest-increasing-subsequence/ | Advanced |
| Split over k | Optimal interval result depends on split point | Any optimal interval solution has a final decomposition point | https://leetcode.com/problems/burst-balloons/ | Advanced |
| Insert/delete/replace transition | String transformation operations | Every transformation reduces to smaller prefixes | https://leetcode.com/problems/edit-distance/ | Core |
| Inner-range dependency | Need palindrome/range relation | Palindrome status depends on inner range plus boundary equality | https://leetcode.com/problems/palindromic-substrings/ | Intermediate |
| Return multiple states | Tree choices depend on child choices | Parent only needs summarized child state | https://leetcode.com/problems/house-robber-iii/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Recursion + Memoization | LC 70 Climbing Stairs | LC 198 House Robber | LC 62 Unique Paths | LC 64 Minimum Path Sum |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### State Definition

**Recognition cue.** Recursive subproblems repeat and their future answer depends on a small set of arguments. **Invariant.** `dp[state]` has one complete sentence defining exactly what it returns.

- **Build - Author exercise: Name The Subproblem.** Define `dp[i]` before writing a recurrence.
- **Vary - Author exercise: Add One Necessary Dimension.** Show why two calls with different remaining state cannot share a cache entry.
- **Boundary - Author exercise: Base-State Contract.** Make every transition terminate at a defined state.
- **Recognize - LC 70 Climbing Stairs.** Define ways to reach or leave index `i` consistently.

### Memo And Table

**Recognition cue.** The recurrence is clear but repeated calls cause exponential work. **Invariant.** Memoization caches completed states; tabulation evaluates dependencies before consumers.

- **Build - Author exercise: Memoized Fibonacci.** Cache each index once.
- **Vary - Author exercise: Bottom-Up Fibonacci.** Evaluate the same recurrence in dependency order.
- **Boundary - Author exercise: Zero And One.** Align array size and base cases.
- **Recognize - LC 70 Climbing Stairs.** Implement both forms and compare stack versus table space.

### Linear Recurrence

**Recognition cue.** Each one-dimensional state depends on a fixed number of earlier states. **Invariant.** Before computing `dp[i]`, all referenced earlier states are final.

- **Build - LC 70 Climbing Stairs.** Sum the two predecessor counts.
- **Vary - LC 746 Min Cost Climbing Stairs.** Minimize cost instead of counting ways.
- **Boundary - Author exercise: Short Arrays.** Derive answers from the problem's legal starting positions.
- **Recognize - LC 1137 N-th Tribonacci Number.** Extend the recurrence window from two states to three.

### Take Or Skip

**Recognition cue.** At each position, choosing it forbids a nearby choice. **Invariant.** `dp[i]` is the best answer for a stated prefix; transition compares skipping with taking plus the last compatible state.

- **Build - Author exercise: Nonadjacent Sum.** Write `max(skip, take)` explicitly.
- **Vary - LC 198 House Robber.** Apply the recurrence to money values.
- **Boundary - Author exercise: All Zero And Singleton.** Preserve the empty-choice contract.
- **Recognize - LC 213 House Robber II.** Split the cycle into two legal linear cases.

### Rolling State

**Recognition cue.** A transition reads only a fixed recent window of DP values. **Invariant.** Each scalar retains the exact prior state named by the recurrence before update.

- **Build - Author exercise: Two-State Fibonacci.** Keep previous-two and previous-one.
- **Vary - LC 198 House Robber.** Roll skip/take prefix values.
- **Boundary - Author exercise: Update Order.** Save old values before overwriting a needed dependency.
- **Recognize - LC 746 Min Cost Climbing Stairs.** Compress the table to constant auxiliary space.

### Objective Types

**Recognition cue.** The same state graph may ask whether, how many, or what minimum/maximum. **Invariant.** Initialization and combination operator match feasibility, counting, or optimization semantics.

- **Build - Author exercise: Reachable Boolean States.** Combine predecessors with OR.
- **Vary - Author exercise: Count The Same Paths.** Replace OR with addition.
- **Boundary - Author exercise: Impossible Minimum.** Use a sentinel that cannot overflow when adding cost.
- **Recognize - LC 64 Minimum Path Sum.** Minimize predecessor cost instead of counting paths.

### Grid DP

**Recognition cue.** Movement restrictions make each cell depend on already processed neighbors. **Invariant.** `dp[r][c]` describes paths or cost to exactly that cell.

- **Build - LC 62 Unique Paths.** Count from top and left.
- **Vary - LC 64 Minimum Path Sum.** Minimize accumulated cost.
- **Boundary - Author exercise: First Row And Column.** Initialize their single available predecessor direction.
- **Recognize - LC 63 Unique Paths II.** Make obstacle cells contribute zero ways.

### Transition Discipline

**Recognition cue.** A recurrence is known, but in-place loop order can accidentally reuse current-iteration state. **Invariant.** Every read comes from the intended logical layer.

- **Build - Author exercise: Separate Previous Row.** Compute a new layer from an immutable old layer.
- **Vary - Author exercise: Safe In-Place Grid Row.** Explain which neighbor is current-row and which is prior-row.
- **Boundary - Author exercise: Aliased Arrays.** Show why assigning `next = current` destroys layer separation.
- **Recognize - LC 931 Minimum Falling Path Sum.** Use explicit prior-row ownership or safe update storage.

## Released Combination Lessons

### Recursion And Memoization

Recursive call arguments identify subproblems; memoization turns repeated subproblem evaluation into one computation per state.

- **Build - LC 70 Climbing Stairs.** Cache a one-index recurrence.
- **Vary - LC 198 House Robber.** Cache take/skip value by index.
- **Boundary - LC 62 Unique Paths.** Use two-dimensional coordinates as the cache key.
- **Recognize - LC 64 Minimum Path Sum.** Change the objective while preserving grid state ownership.

### Deferred: Capacity DP

Capacity state and loop direction determine item reuse. Chapter 27 owns that distinction.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Define each DP state in one sentence before transitions.
- Use a copy or reverse iteration when an in-place update would accidentally reuse the current item.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Recursion + Memoization | Call arguments become cache keys; staircase: stairs → house robber → grid paths |
| Deferred | DP + Capacity | Chapter 27 supplies reuse and capacity-state rules |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** knapsack, state machines, interval/subsequence DP.

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

