<!-- lesson-kind: standard -->
<!-- lesson-id: direct-scans -->
## Direct Scans

<!-- stage: context -->
### Finding The Overdue Slip

A library keeps returned-book slips in a drawer in the order they arrive, each marked with a member number. A clerk needs the earliest slip belonging to member 7, because that member's account needs checking first. The drawer is unsorted, nobody promised any pattern, and the clerk has one hand free. She starts at the front and flips slips one at a time, and the moment she sees a 7 she stops.

Her procedure is so natural that it hardly feels like an algorithm. Yet it contains every decision this lesson is about: where to start, what to remember, when she is allowed to stop, and what she can conclude if she reaches the back of the drawer without a match. Many array questions are exactly this one wearing different clothes.

<!-- stage: naive -->
### Tidy The Drawer First

A tempting thought is to sort the slips so that member 7's slips sit together, which feels like it makes the search easier. In code, that means copying the array, sorting it and looking for the target in the sorted copy.

```java
static int firstIndexViaSort(int[] nums, int target) {
    int[] sorted = nums.clone();
    Arrays.sort(sorted);
    for (int i = 0; i < sorted.length; i++) {
        if (sorted[i] == target) return i;
    }
    return -1;
}
```

On `[7, 4, 7]` with target 7 the method returns 1, because the sorted copy is `[4, 7, 7]`. The slip that arrived first was at position 0.

<!-- stage: bottleneck -->
### Wrong Answer, Extra Work

The sorted copy answers a different question. Sorting rearranged the positions, so the index it reports is a position in the rearranged array, and the original arrival order is gone. The result is wrong whenever the caller needs the original index, which is what "first index" means here.

The cost is also higher than the problem deserves. Sorting is O(n log n) time and the clone is O(n) extra space, while the clerk's flip-through touches each slip at most once. For `n = 100,000` that is roughly 1.7 million steps for sorting against at most 100,000 for the plain pass, and the extra memory buys nothing. Even if you only needed to know whether a 7 exists, the sort adds work and leaves you with no direct way to answer the position question.

<!-- stage: insight -->
### Ruling Out Positions One By One

The clerk's method has a precise form. Keep one position that marks the next unexamined slip, check that slip, and move on. As long as you have not found the target, you know something definite about everything behind you.

A **direct scan** is a single pass in which a loop index marks the next unexamined position and each step inspects exactly one element. The invariant is that before examining `nums[i]`, you know the target does not occur in `nums[0..i-1]`. That one sentence explains both exits. A match at `i` proves the answer, since everything before it was already ruled out. Reaching the end proves absence, because the invariant then covers the entire array.

<!-- names: direct scan, early exit, result contract -->

Whether you may stop at the first match is the **early exit**, and the result you owe the caller is the **result contract**. For the first index, the early exit is allowed, since the earliest match is the first one you meet. For the last index, the early exit is wrong, because a later match may still exist, so the scan must either continue to the end or walk from the back. A contract also says what to return when nothing matches. Because an index can never be negative, `-1` is a safe signal for absence here, and it cannot be confused with a real answer.

Notice what the scan does not need. It never asks for sorted data, never builds a second structure, and never copies the array. Those would answer other questions. The scan simply trades one look per element for a definite answer.

<!-- stage: variables -->
### One Index And One Promise

The loop index `i` is the only moving part. It starts at 0, so nothing has been ruled out yet, and each iteration that finds no match extends the ruled-out region by one. The target is fixed. The answer is produced the moment the contract is satisfied, by returning inside the loop, and the fallback after the loop reports absence. If a problem wants the last match, the same variables work with the index running from `nums.length - 1` downward, or with an explicit `answer` variable overwritten on every match.

<!-- stage: trace -->
### Two Runs Of The Drawer

Take `[4, 1, 7, 7]` with target 7 and ask for the first index. At position 0 the value 4 is not a 7, so position 0 joins the ruled-out region. Position 1 holds a 1 and joins it too. At position 2 the value is a 7, so the scan returns 2 immediately. Position 3 holds another 7, and the scan never visits it, which is correct because the contract asks for the earliest.

Now take `[3, 2, 2, 3]` with target 5. Positions 0, 1, 2 and 3 are each examined and each fails to match. Only after the fourth failure does the loop end, and only then can the method return `-1`. The hardest step to appreciate is that last one. The scan cannot return `-1` after seeing one or two non-matches, because the invariant has not yet covered the whole array, and reaching the end is itself the proof.

```trace
{"cells":[4,1,7,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"target":7,"ruledOut":0},"note":"Position 0 holds 4, not a 7. Positions 0..-1 are already ruled out; this one joins them next."},{"at":{"i":1},"vars":{"target":7,"ruledOut":1},"note":"Position 1 holds 1, not a 7. The ruled-out region grows to 2 positions."},{"at":{"i":2},"vars":{"target":7,"ruledOut":2},"note":"Position 2 holds 7, a match. Return 2 at once. Positions after it are never visited."}]}
```

```trace
{"cells":[3,2,2,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"target":5,"ruledOut":0},"note":"Position 0 holds 3, not a 5. The ruled-out region grows to 1 position."},{"at":{"i":1},"vars":{"target":5,"ruledOut":1},"note":"Position 1 holds 2, not a 5. The ruled-out region grows to 2 positions."},{"at":{"i":2},"vars":{"target":5,"ruledOut":2},"note":"Position 2 holds 2, not a 5. The ruled-out region grows to 3 positions."},{"at":{"i":3},"vars":{"target":5,"ruledOut":3},"note":"Position 3 holds 3, not a 5. The ruled-out region grows to 4 positions."},{"at":{"i":4},"vars":{"target":5,"ruledOut":4},"note":"The loop ends with all four positions ruled out, which proves absence. Return -1."}]}
```

<!-- stage: code -->
### The Scan In Java

```java
static int firstIndex(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] == target) return i;      // everything before i was already ruled out
    }
    return -1;                                // the loop ended, so the whole array was ruled out
}

static int lastIndex(int[] nums, int target) {
    for (int i = nums.length - 1; i >= 0; i--) {
        if (nums[i] == target) return i;
    }
    return -1;
}
```

Both methods cost O(n) time and constant extra space, and they only differ in direction. Each returns from inside the loop on a match, so no result variable is needed. An empty array makes the loop body run zero times and both methods return `-1`, which agrees with the contract without a special case. The method that sorts first loses the original positions and costs more, so it is not a refinement of this one but a different question.

<!-- stage: applicability -->
### When A Plain Pass Is The Answer

Use a direct scan when the data is unsorted, any element may matter, and the answer is fixed by inspecting one element at a time. The invariant to say out loud is that before looking at `nums[i]`, the answer is not found in `nums[0..i-1]`. The loop bounds and the early-exit rule follow from the result contract, so read the contract first.

The false friend is the urge to sort or to build a lookup structure before looking. Sorting changes index meaning and costs more than one scan, so it is wrong when the question is about original positions. A lookup structure from a later chapter pays off only when many queries hit the same data, and for a single query the one pass is cheaper to write and to run.

Java adds small cautions. `Arrays.binarySearch` requires sorted input and gives an undefined result on unsorted data, so it is not a shortcut here. An `int` index return with `-1` for absence is a convention, and callers must check for it before using the value as an index. Chapter 00's guarantee habit applies, because a scan over a possibly `null` array throws, and the statement decides whether that case exists.

<!-- stage: exercises -->
### Exercises

#### [Build] First Match (Author exercise)
<!-- id: ar-first-match -->

**Prerequisites.** Chapter 00 contract reading; the direct scan in this lesson.

**Problem.** Given an integer array `nums` and an integer `target`, return the first index at which `target` occurs, or `-1` when it does not occur. Do not modify `nums`, and stop scanning as soon as the answer is known.

**Constraints.** 0 <= nums.length <= 10^5 and -10^9 <= nums[i], target <= 10^9. Aim for one scan and no extra array.

**Example 1.** Input `nums = [7, 4, 7]`, `target = 7`, output 0.

**Example 2.** Input `nums = []`, `target = 3`, output -1, because an empty array contains nothing.

**Hint.** What does reaching the end of the loop without a match prove about the whole array?

**Changed decision.** First rung of the ladder: introduces the loop invariant and the early exit.

#### [Vary] Last Match (Author exercise)
<!-- id: ar-last-match -->

**Prerequisites.** The first-match exercise above.

**Problem.** Keep scanning after a match and return the last index at which `target` occurs, or `-1` if it never does. Explain why returning at the first match would be wrong here.

**Constraints.** 0 <= nums.length <= 10^5 and -10^9 <= nums[i], target <= 10^9. Stop at the first match; no auxiliary storage.

**Example 1.** Input `nums = [7, 4, 7]`, `target = 7`, output 2.

**Example 2.** Input `nums = [1]`, `target = 9`, output -1.

**Hint.** A later match may exist after the first one. Can you scan from the other end so that the first match you meet is the answer?

**Changed decision.** The contract changes from earliest to latest, so the early-exit rule changes with it.

#### [Boundary] Target Absent (Author exercise)
<!-- id: ar-target-absent -->

**Prerequisites.** The two exercises above.

**Problem.** Given an unsorted array and a target that may not occur, return `-1` only after a complete scan. Explain why returning `-1` earlier would be unsafe and why an empty array needs no extra branch.

**Constraints.** 0 <= nums.length <= 10^5. Values may repeat. The scan must not rely on any ordering.

**Example 1.** Input `nums = [3, 2, 2, 3]`, `target = 5`, output -1.

**Example 2.** Input `nums = []`, `target = 3`, output -1, with the loop body never running.

**Hint.** After how many examined elements does the invariant cover the entire array? What does a loop over zero elements return?

**Changed decision.** The question moves from finding to proving absence, so the end of the loop becomes the evidence.

#### [Recognize] Build Array From Permutation (LeetCode 1920)
<!-- id: ar-build-permutation -->

**Prerequisites.** The three exercises above.

**Problem.** The array `nums` is a permutation of `0..n-1`, meaning each of those integers appears exactly once. Build and return a new array `ans` where `ans[i] = nums[nums[i]]` for every `i`. The task is a direct indexed read, not a search.

**Constraints.** 1 <= n <= 1000 and `nums` is a permutation of `0..n-1`. Target O(n) time, with the returned array as the only allocation.

**Example 1.** Input `nums = [2, 0, 1]`, output `[1, 2, 0]`.

**Example 2.** Input `nums = [0]`, output `[0]`, since a one-element permutation maps zero to itself.

**Hint.** Every value in `nums` is itself a legal index. Do you need to look for anything, or can you just read?

**Changed decision.** The scan visits each position once and reads another position directly, so no search is involved.
