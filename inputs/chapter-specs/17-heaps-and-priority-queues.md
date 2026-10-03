# Chapter 17: Heaps and priority queues

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| Java `PriorityQueue` | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| min/max heap orientation and comparators | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| top-k | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| k-way merge | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| scheduling | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| lazy deletion/stale entries | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| running median and dual-heap balancing | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0061 | Heap fundamentals | Last Stone Weight | Direct concept | Repeatedly extract the largest elements. |
| P0062 | Heap fundamentals | Kth Largest Element in a Stream | Immediate application | Maintains a fixed-size heap over a changing stream. |
| P0063 | Top K | Kth Largest Element in an Array | Immediate application | Generalizes fixed-size heap maintenance. |
| P0064 | Top K | Top K Frequent Elements | Small extension | Combines frequency counting with a heap. |
| P0065 | Two heaps | Find Median from Data Stream | New subtopic | Maintains lower and upper halves with opposite heaps. |
| P0066 | Two heaps | Sliding Window Median | Immediate application | Extends the two-heap partition to a moving window. |
| P0067 | K-way merge | Merge k Sorted Lists | New subtopic | Heap contains the current head from each sorted source. |
| P0068 | K-way merge | Kth Smallest Element in a Sorted Matrix | Immediate application | Treats rows/columns as sorted streams. |
| P0069 | K-way merge | Find K Pairs with Smallest Sums | Small extension | Generates the next candidate from multiple ordered streams. |
| P0070 | Scheduling simulation | Single-Threaded CPU | New subtopic | Sort by availability, then select the best currently available task. |
| P0071 | Scheduling simulation | Process Tasks Using Servers | Immediate application | Maintains available and busy resources with heaps. |
| P0072 | Heap + greedy | Furthest Building You Can Reach | New combination | Use a heap to defer the most expensive choices. |
| P0073 | Heap + greedy | Minimum Number of Refueling Stops | Combination | Greedy decisions are supported by a max-heap of prior options. |
| Bundle 1-1 | Priority Selection | Kth Largest Element in an Array | Learn | — |
| Bundle 1-2 | Top K | Top K Frequent Elements | Extend | — |
| Bundle 1-3 | Heap + Simulation | Single-Threaded CPU | Twist | — |
| Bundle 2-4 | Simulation | Single-Threaded CPU | Mixed | — |
| Bundle 2-13 | Scheduling | Task Scheduler | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Dynamic extreme | Repeatedly need current min/max | Heap keeps best currently available item efficiently | https://leetcode.com/problems/kth-largest-element-in-an-array/ | Core |
| Keep exactly K useful candidates | Need Top K only | Only K boundary candidates can affect final result | https://leetcode.com/problems/top-k-frequent-elements/ | Core |
| Balance lower/upper halves | Need median of stream | Both heaps bracket the median | https://leetcode.com/problems/find-median-from-data-stream/ | Intermediate |
| Advance time -> add eligible -> poll priority | Tasks have release/start time and priority | Heap contains exactly the currently executable tasks | https://leetcode.com/problems/single-threaded-cpu/ | Core |
| Track earliest finishing active job | Intervals require minimum simultaneous resources | Earliest finish is the first resource that becomes free | https://leetcode.com/problems/meeting-rooms-ii/ | Core |
| Choose ordering with proof | Need order tasks under deadlines | Exchange argument makes the chosen ordering safe | https://leetcode.com/problems/course-schedule-iii/ | Advanced |
| Time + eligibility + priority | Jobs have release/start time + processing time + priority | Separates chronological availability from selection among available jobs | https://leetcode.com/problems/single-threaded-cpu/ | Core |
| Take jobs by deadline; eject longest when infeasible | Jobs have deadlines and durations | Removing the longest job frees the most time while retaining maximum count | https://leetcode.com/problems/course-schedule-iii/ | Advanced |
| Track currently active jobs | Repeated events compete for resources | Only active jobs consume resources | https://leetcode.com/problems/meeting-rooms-ii/ | Core |
| Heap contains one head from each stream | Need merge many sorted streams | Only each stream's current head can be the next global minimum | https://leetcode.com/problems/merge-k-sorted-lists/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Heap + Intervals | LC 252 Meeting Rooms | LC 253 Meeting Rooms II | LC 2406 Divide Intervals Into Minimum Number of Groups | LC 1851 Minimum Interval to Include Each Query |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### PriorityQueue Mechanics

**Recognition cue.** The algorithm repeatedly needs the smallest or largest currently eligible item while the candidate set changes. **Invariant.** `peek()` is the extreme under the queue's comparator; the rest of the heap is only partially ordered. **False friend.** Iterating a `PriorityQueue` does not produce sorted order.

- **Build - Author exercise: Repeated Minimum.** Insert values, then poll them in nondecreasing order.
- **Vary - LC 1046 Last Stone Weight.** Repeatedly remove the two largest values and reinsert a remainder.
- **Boundary - Author exercise: Empty And Singleton Heap.** State when `peek` or `poll` is legal and what one remaining item means.
- **Recognize - LC 703 Kth Largest Element in a Stream.** Maintain a heap whose root is the kth-largest boundary.

### Heap Orientation

**Recognition cue.** Correctness depends on which candidate must be exposed first and how ties are resolved. **Invariant.** The comparator orders the exact priority tuple used by the algorithm. **False friend.** Negating integers to imitate a max-heap can overflow at `Integer.MIN_VALUE`. **Java hazard.** Use `Integer.compare` or `Comparator.comparingInt` rather than subtraction.

- **Build - Author exercise: Safe Max-Heap.** Create a reverse comparator without numeric negation.
- **Vary - Author exercise: Pair Priority.** Order tasks by duration, then original index.
- **Boundary - Author exercise: Equal Priorities And Extreme Integers.** Verify deterministic ties and overflow-safe comparison.
- **Recognize - LC 1834 Single-Threaded CPU.** Select by processing time and index among currently available tasks.

### Top K

**Recognition cue.** Only the best `k` elements matter, so the weakest retained candidate should be cheap to replace. **Invariant.** A size-`k` heap contains the best `k` items seen; its root is the retention boundary. **False friend.** A max-heap holding every item works for extraction but wastes space when `k` is small.

- **Build - Author exercise: K Largest Values.** Keep a size-`k` min-heap and replace its root when a larger value arrives.
- **Vary - LC 215 Kth Largest Element in an Array.** Return the root after scanning all values.
- **Boundary - Author exercise: K Equals One Or N.** Preserve the same invariant at both extremes.
- **Recognize - LC 347 Top K Frequent Elements.** Count with a map, then heap-select by frequency.

### K-Way Merge

**Recognition cue.** Several sources are individually sorted and the next global value must be chosen repeatedly. **Invariant.** The heap contains at most one current head from each nonexhausted source. **False friend.** Inserting every value loses the `O(k)` frontier-space advantage.

- **Build - Author exercise: Merge Three Sorted Arrays.** Store value, source index, and position for each current head.
- **Vary - LC 23 Merge k Sorted Lists.** Poll one list node and offer its successor.
- **Boundary - Author exercise: Empty Sources And Equal Heads.** Skip exhausted sources and use a safe tie policy.
- **Recognize - LC 378 Kth Smallest Element in a Sorted Matrix.** Treat each row as a sorted stream and stop after `k` polls.

### Heap Scheduling

**Recognition cue.** Items become eligible over time, and the best eligible item must be selected by a second priority. **Invariant.** After advancing time and adding all released tasks, the heap contains exactly the executable tasks. **False friend.** One global sort cannot generally express both release time and dynamic selection priority.

- **Build - Author exercise: Released Shortest Job.** Sort by release time and heap-select the shortest available job.
- **Vary - LC 1834 Single-Threaded CPU.** Add index tie-breaking and jump time when no task is available.
- **Boundary - Author exercise: Idle Gap And Simultaneous Releases.** Advance directly to the next release and enqueue every tie before selecting.
- **Recognize - LC 1882 Process Tasks Using Servers.** Coordinate available-resource and busy-resource heaps.

### Lazy Deletion

**Recognition cue.** Priorities change or items expire, but arbitrary heap removal would be linear. **Invariant.** Before using the root, discard entries whose stored version, count, or eligibility no longer matches companion state. **False friend.** `PriorityQueue.remove(Object)` and `contains` are linear, not logarithmic.

- **Build - Author exercise: Versioned Priorities.** Insert a new record after an update and ignore old versions when polled.
- **Vary - Author exercise: Delayed Removal Counts.** Record logical deletions in a map and clean matching roots on demand.
- **Boundary - Author exercise: Several Stale Roots.** Clean in a loop and handle equal values with multiple outstanding copies.
- **Recognize - LC 480 Sliding Window Median.** Combine delayed deletion with two balanced heaps.

### Running Median

**Recognition cue.** Values arrive online and each prefix needs its median. **Invariant.** A max-heap owns the lower half, a min-heap owns the upper half, their sizes differ by at most one, and every lower value is no greater than every upper value. **False friend.** One heap exposes only one extreme, not the center.

- **Build - Author exercise: Rebalance Two Halves.** Insert one value and move roots until the size invariant holds.
- **Vary - LC 295 Find Median from Data Stream.** Return one root for odd size or the average of two roots for even size.
- **Boundary - Author exercise: Overflow-Safe Even Median.** Convert to `long` or `double` before adding extreme integers.
- **Recognize - LC 480 Sliding Window Median.** Add expiry through lazy deletion while preserving logical heap sizes.

## Released Combination Lessons

### Heap And Intervals

Interval sorting reveals start times; the heap exposes the active interval that finishes first. Together they decide whether a resource can be reused or a new resource is required.

- **Build - LC 252 Meeting Rooms.** Establish the overlap contract after sorting by start.
- **Vary - LC 253 Meeting Rooms II.** Reuse the room with the earliest finishing active meeting.
- **Boundary - LC 2406 Divide Intervals Into Minimum Number of Groups.** Apply the closed-interval tie rule where touching endpoints still overlap.
- **Recognize - LC 1851 Minimum Interval to Include Each Query.** Add eligible intervals by start, expire by end, and select minimum size.

### Deferred: Graph And Heap

Dijkstra-style search also uses the smallest heap entry, but correctness depends on graph relaxation and stale-distance state. Chapter 24 owns that composition.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- `PriorityQueue` is a min-heap by default; write the comparator direction explicitly.
- Do not treat `contains` or `remove(Object)` as logarithmic; use lazy deletion or companion state when needed.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Heap + Intervals | Earliest release time controls room reuse; representative: LC 253 |
| Deferred | Graph + Heap | Chapter 24 supplies distance and stale-entry invariants |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** graph shortest paths.

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

