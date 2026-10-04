<!-- lesson-kind: standard -->
<!-- lesson-id: top-k -->
## Top K

<!-- stage: context -->
### The Season's Fastest Five

A trail-running club posts the five fastest ascents of its hill each season on a board by the clubhouse door. Runners finish at all hours, and each one hands in a score, the climb speed in metres per minute, to a volunteer who updates the board. The record has grown to several million entries over the years, and only the five best of them are ever displayed.

The volunteer used to copy the whole record into a spreadsheet, sort it, and read off the top of the column. That worked for a few hundred scores. Now a tablet at the finish line sends every score as it happens, the board is supposed to update within a second of each finish, and the spreadsheet no longer even opens. She wants to carry a handful of numbers in her pocket and update them as each score arrives.

<!-- stage: naive -->
### Sort Everything And Slice

The direct method copies all scores, sorts the copy, and returns the last `k` entries.

```java
static int[] bestKBySorting(int[] scores, int k) {
    int[] copy = scores.clone();
    java.util.Arrays.sort(copy);
    int[] best = new int[k];
    for (int i = 0; i < k; i++) best[i] = copy[copy.length - 1 - i];
    return best;
}
```

It is correct. For the scores `[4, 9, 1, 7, 3, 8]` and `k = 3` it returns `[9, 8, 7]`, with the best score first.

<!-- stage: bottleneck -->
### Ordering Millions To Show Five

Sorting costs O(n log n) time and needs a copy of all `n` scores, and it has to be repeated from scratch whenever a new score arrives. For ten million scores that is hundreds of millions of steps per update, to show five numbers. The sort also discovers the exact order of the ten million minus five scores that will never be displayed, which is work whose result is thrown away.

What the board needs is much smaller. A new score matters only if it beats the weakest of the five currently displayed, and nothing else about the record matters at that moment. So the information that has to be kept is the five best scores and a quick way to find the weakest of them and replace it. A fully sorted record keeps millions of facts when five facts, plus the ability to find the smallest of them, would give the same board.

<!-- stage: insight -->
### Keep Only The Contenders

Keep the `k` best scores seen so far in a **bounded heap**: a min-heap, ordered with the weakest at the root, that never holds more than `k` items. The root is the **retention boundary**, the weakest score that is still good enough to be displayed. A score that does not beat the boundary can be discarded forever, because at least `k` better scores already exist and more can only be added.

Each arriving score is handled by the **replace-root rule**. If the heap holds fewer than `k` items, offer the score. Otherwise compare it with the root: if it is strictly larger, poll the root and offer the score, and if it is not, ignore it. The heap then again holds the `k` best scores seen, and its root is the new boundary.

<!-- names: bounded heap, retention boundary, replace-root rule -->

The heap must be a min-heap even though the goal is the largest scores, because the item that must be found fast is the weakest of the contenders, and a min-heap exposes the smallest item at the root. Each score costs at most one offer and one poll on a heap of size `k`, so the whole pass is O(n log k) time, and the memory is O(k) beyond the input. When `k` is small, log k is nearly constant, and the pass is close to linear. Reading the answer takes one more step, since the heap's contents are not sorted: poll them out for ascending order, or sort the `k` items.

<!-- stage: variables -->
### Heap, Limit And Boundary

The heap `best` holds at most `k` scores, and its size grows only while the stream is still filling it. The limit `k` never changes during a pass. The boundary is `best.peek()`, and it can only grow: it changes when a replacement removes the old root, and the new root is at least as large as the old one, since the old root was the minimum and the newcomer exceeded it. The current score `v` is compared with the boundary with a strict inequality, so an equal score does not replace anything, and the multiset of retained values is the same either way. When `k` is 0 there is nothing to retain, and the loop must not call `peek` on an empty heap.

<!-- stage: trace -->
### Replacing The Weakest Contender

Take the scores `5, 1, 9, 3, 7, 8, 2, 6` with `k = 3`. The first three scores fill the heap, and the boundary after them is 1. The 3 beats the boundary and replaces the 1, and the boundary rises to 3. The 7 replaces the 3, and the boundary becomes 5. The 8 replaces the 5, so the heap now holds 7, 8 and 9 with the boundary 7. The 2 and the 6 are both below the boundary and are ignored, so the final contenders are 7, 8 and 9.

A second run takes the scores `9, 8, 7, 3, 2, 1` with `k = 3`. The heap is full after the third score, with the boundary 7, and every later score is below it, so nothing is replaced. The step to study in the first run is the arrival of the 6 at the end, where a score that is higher than several earlier ones is still discarded, since it is not larger than the boundary.

```trace
{"cells":[5,1,9,3,7,8,2,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"kept":"[5]","boundary":5},"note":"Score 5 arrives and the heap holds fewer than 3 items, so it is offered. The boundary is now 5."},{"at":{"i":1},"vars":{"kept":"[1,5]","boundary":1},"note":"Score 1 arrives and the heap holds fewer than 3 items, so it is offered. The boundary is now 1."},{"at":{"i":2},"vars":{"kept":"[1,5,9]","boundary":1},"note":"Score 9 arrives and the heap holds fewer than 3 items, so it is offered. The boundary is now 1."},{"at":{"i":3},"vars":{"kept":"[3,5,9]","boundary":3},"note":"Score 3 beats the boundary 1, so the root is polled and 3 is offered. The boundary is now 3."},{"at":{"i":4},"vars":{"kept":"[5,7,9]","boundary":5},"note":"Score 7 beats the boundary 3, so the root is polled and 7 is offered. The boundary is now 5."},{"at":{"i":5},"vars":{"kept":"[7,8,9]","boundary":7},"note":"Score 8 beats the boundary 5, so the root is polled and 8 is offered. The boundary is now 7."},{"at":{"i":6},"vars":{"kept":"[7,8,9]","boundary":7},"note":"Score 2 does not beat the boundary 7, so it is ignored. The boundary is now 7."},{"at":{"i":7},"vars":{"kept":"[7,8,9]","boundary":7},"note":"Score 6 does not beat the boundary 7, so it is ignored. The boundary is now 7."}]}
```

```trace
{"cells":[9,8,7,3,2,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"kept":"[9]","boundary":9},"note":"Score 9 arrives and the heap holds fewer than 3 items, so it is offered. The boundary is now 9."},{"at":{"i":1},"vars":{"kept":"[8,9]","boundary":8},"note":"Score 8 arrives and the heap holds fewer than 3 items, so it is offered. The boundary is now 8."},{"at":{"i":2},"vars":{"kept":"[7,8,9]","boundary":7},"note":"Score 7 arrives and the heap holds fewer than 3 items, so it is offered. The boundary is now 7."},{"at":{"i":3},"vars":{"kept":"[7,8,9]","boundary":7},"note":"Score 3 does not beat the boundary 7, so it is ignored. The boundary is now 7."},{"at":{"i":4},"vars":{"kept":"[7,8,9]","boundary":7},"note":"Score 2 does not beat the boundary 7, so it is ignored. The boundary is now 7."},{"at":{"i":5},"vars":{"kept":"[7,8,9]","boundary":7},"note":"Score 1 does not beat the boundary 7, so it is ignored. The boundary is now 7."}]}
```

<!-- stage: code -->
### K Largest With A Bounded Heap

```java
static int[] kLargest(int[] values, int k) {
    java.util.PriorityQueue<Integer> best = new java.util.PriorityQueue<>();
    for (int v : values) {
        if (best.size() < k) best.offer(v);
        else if (k > 0 && v > best.peek()) {      // beats the boundary
            best.poll();
            best.offer(v);
        }
    }
    int[] out = new int[best.size()];
    for (int i = out.length - 1; i >= 0; i--) out[i] = best.poll();   // weakest leaves first
    return out;
}
```

The loop does at most two heap operations per value on a heap of size at most `k`, which gives O(n log k) time, and the heap is the only extra memory, which is O(k). The comparison `v > best.peek()` unboxes the root, and it is safe because the branch is reached only when `k > 0` and the heap is full, so the root exists. The output is filled from the back because the polls arrive weakest first, which leaves the result in descending order. If `k` exceeds the array length, the heap simply never fills and all values are returned.

<!-- stage: applicability -->
### When Only The Best Few Matter

Use a bounded heap when a question asks for the `k` best items, or the k-th best, under some order, and `k` is much smaller than `n`, or the data arrives as a stream that cannot be stored. The invariant is that after each item the heap holds exactly the `k` best items seen so far, and its root is the weakest of them. For the `k` smallest items, mirror the construction with a max-first heap, so that the root is again the item that is next to be dropped.

The false friend is the max-heap that holds every item. It looks natural, since the largest item is at the root, and it does answer the question: poll `k` times. But it stores all `n` items and spends O(n) to build and O(k log n) to extract, and it cannot run on a stream. Another false friend is a sort, which is simpler and fine when `k` is close to `n`, because the heap then keeps almost everything and has no advantage.

Do not use it when the retained items must be removed or changed from outside, because the heap cannot find an arbitrary item cheaply. Do not use it for a single k-th value of a stored array when its order may be disturbed, since a partition-based selection can do that in expected linear time. In Java, keep the comparator explicit for object items, and make sure that the heap size is checked before `peek`.

<!-- stage: exercises -->
### Exercises

#### [Build] K Largest Values (Author exercise)
<!-- id: hp-k-largest-values -->

**Prerequisites.** The bounded heap and replace-root rule of this lesson.

**Problem.** Given an integer array `values` and an integer `k` with 0 <= k <= values.length, return the `k` largest values in descending order, counting duplicates separately. Hold at most `k` items in the queue at any moment.

**Constraints.** 0 <= values.length <= 10^5 and -10^9 <= values[i] <= 10^9.

**Example 1.** Input `values = [4, 9, 1, 7, 3, 8]`, `k = 3`, output `[9, 8, 7]`.

**Example 2.** Input `values = [5, 5, 2]`, `k = 2`, output `[5, 5]`.

**Hint.** Which end of the queue must be the one that you can read and discard? What comparison decides whether the newcomer enters?

**Changed decision.** First rung: the retention boundary and the replace-root rule on their own, with a size limit that is never exceeded.

#### [Vary] Kth Largest Element in an Array (LeetCode 215)
<!-- id: hp-kth-largest-element -->

**Prerequisites.** K Largest Values above.

**Problem.** Given an integer array `nums` and an integer `k`, return the k-th largest element in sorted order, counting duplicates, so that the second largest of `[9, 9, 2]` is 9.

**Constraints.** 1 <= k <= nums.length <= 10^5 and -10^4 <= nums[i] <= 10^4.

**Example 1.** Input `nums = [8, 2, 9, 4, 9, 1]`, `k = 2`, output 9.

**Example 2.** Input `nums = [-1, -4, -2]`, `k = 3`, output -4.

**Hint.** After the whole scan, which item of the bounded heap is the answer? Why is it not necessary to sort the contents?

**Changed decision.** Only the boundary is returned, so the contents of the heap are never read out, and the root after the scan is the answer.

#### [Boundary] K Equals One Or N (Author exercise)
<!-- id: hp-k-one-or-n -->

**Prerequisites.** The two exercises above.

**Problem.** Given `values` and `1 <= k <= values.length`, run the bounded heap over the array. Return `[root, replacements]`, where `root` is the heap's root after the scan and `replacements` counts the times a full heap polled its root to admit a strictly larger newcomer.

**Constraints.** 1 <= values.length <= 10^5 and -10^9 <= values[i] <= 10^9.

**Example 1.** Input `values = [3, 1, 4, 1, 5, 9, 2, 6]`, `k = 1`, output `[9, 3]`.

**Example 2.** Input `values = [2, 7, 1]`, `k = 3`, output `[1, 0]`.

**Hint.** For `k = 1` the heap is full after the first item, so which items replace the root? For `k = n` the heap never has to discard anything, so what is its root at the end?

**Changed decision.** The two extreme limits keep the same invariant but make the heap either permanently full from the start or never full to the end, and the replacement count exposes which one happened.

#### [Recognize] Top K Frequent Elements (LeetCode 347)
<!-- id: hp-top-k-frequent -->

**Prerequisites.** All three exercises above, and the counting map from the hash-map chapter.

**Problem.** Given an integer array `nums` and an integer `k`, return the `k` values that occur most often, sorted in ascending order of value. It is guaranteed that the set of `k` most frequent values is unique.

**Constraints.** 1 <= nums.length <= 10^5, values between -10^4 and 10^4, and 1 <= k <= the number of distinct values.

**Example 1.** Input `nums = [7, 7, 7, 3, 3, 9, 9, 9, 9, 1]`, `k = 2`, output `[7, 9]`.

**Example 2.** Input `nums = [5]`, `k = 1`, output `[5]`.

**Hint.** What is the thing being ranked now, and what is the key? What must a heap entry carry besides the count?

**Changed decision.** The queue ranks distinct values by their counts, not raw numbers, so a map comes first and the heap holds pairs.
