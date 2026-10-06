<!-- lesson-kind: standard -->
<!-- lesson-id: circular-next-greater -->
## Find The Next Greater In A Circle

<!-- stage: context -->
### The Ring Buffer Has No End

A service keeps its last five latency samples in a ring buffer. A new sample overwrites the oldest slot, so after the last slot the next slot to read is slot 0. An alert rule asks, for every slot, which slot holds the first strictly larger sample when the reader moves forward and wraps past the end. The array version of this question stops at the last slot. The ring version must keep going.

The lesson answers one question. How does the stack scan from the previous lesson handle a walk that wraps around, without building a second copy of the data?

<!-- stage: naive -->
### Walk Forward With A Wrapping Index

The direct approach starts at slot `i` and moves forward one slot at a time. The index `(i + k) % n` wraps from the last slot to slot 0. The walk takes at most `n - 1` steps, so it never returns to slot `i` itself.

```java
static int[] circularNextGreaterWalk(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    for (int i = 0; i < n; i++) {
        ans[i] = -1;
        for (int k = 1; k < n; k++) {
            int j = (i + k) % n;
            if (nums[j] > nums[i]) {
                ans[i] = nums[j];
                break;
            }
        }
    }
    return ans;
}
```

For the samples 3, 8, 4, 1, 2, the walk from the 4 reads the 1, the 2 and the 3, and stops at the 8. The 8 sits before the 4 in the array and after it in the ring.

<!-- stage: bottleneck -->
### Each Slot Walks The Full Circle

```predict
Every one of 100000 slots holds the same value. About how many comparisons does the walk make in total?

About 10^10. No slot holds a strictly larger value, so every walk takes all 99999 steps. The total is 100000 x 99999.
```

The worst case is O(n^2) for `n` slots. An array without a larger value anywhere makes every walk run to the end. The walks also repeat each other's reads. The walk from slot 3 and the walk from slot 4 both pass slot 0 and slot 1, and each one compares the same values again.

The previous lesson removed that repeated work for a line of values. The new difficulty is only the wrap. A stack that waits for a larger value must be allowed to find it on the other side of the end.

<!-- stage: insight -->
### Read The Array Twice Without Copying It

An index waits for a larger value that may come after the wrap, so the scan must pass over the array a second time. It can do that without storing a second array.

<!-- names: virtual second pass, wrap-around index -->

#### A Second Pass Reaches Every Wrapped Answer

The answer for index `i` lies at one of the positions `i + 1` through `i + n - 1` in circular order. Number those positions as if the array repeated itself, so position `p` holds `nums[p % n]`. Every answer then lies below position `2n - 1`. A scan over positions `0` through `2n - 1` is therefore a **virtual second pass**. It reads the array twice and allocates nothing, because each position computes its value on demand.

The **wrap-around index** `i = p % n` turns a virtual position into a real array index. The value `nums[i]` is the resolving value for the stack tops that it beats. The pop loop is the one from the previous lesson, and it still stops when a top is not smaller.

#### Only The First Pass Pushes

Every real index must wait on the stack once, so the push happens only while `p < n`. During the second pass, the scan reads values and pops, but it never pushes. A pushed copy in the second pass would stand for an index that either has its answer already or has none at all. An index that is still on the stack at position `i + n` has been compared with every other slot, so no larger value exists for it. Skipping the push keeps the stack at most `n` entries and keeps each index on the stack at most once.

#### Equal Values Still Do Not Resolve

An index never answers itself, because the comparison is strict and position `i + n` holds the same value as position `i`. A circular array whose values are all equal leaves every answer at `-1`. No pop ever happens.

<!-- stage: variables -->
### What The Two Passes Track

The scan tracks five pieces of state.

- **p** is the virtual position from `0` up to `2n - 1`, and it names one read of the array.
- **i** is the wrap-around index `p % n`, which names the real slot that position `p` reads.
- **stack** holds unresolved indices, and the values behind them never increase from bottom to top.
- **ans** holds one answer per real index, and every entry starts at `-1`.
- **n** is the array length, and it decides when the pushes stop.

The second pass changes `p` and `i` but never adds to `stack`.

<!-- stage: trace -->
### Following Two Passes Over One Array

#### Answers Found After The Wrap

The first trace reads 3, 8, 4, 1, 2. The pointer `i` marks the real slot, and the variable `p` counts virtual positions from 0 to 9. In the first pass, the 8 resolves the 3, and the 2 resolves the 1. The stack then holds the indices 1, 2 and 4, and the three of them still wait.

In the second pass, position 5 reads the 3 again. It is greater than the 2 at index 4, so index 4 gets the answer 3. It is not greater than the 4 at index 2, so the pops stop. Position 6 reads the 8 and resolves the 4 at index 2. The 8 at index 1 stays, because no value exceeds it.

```trace
{"cells":[3,8,4,1,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"p":0,"stack":"[0]","ans":"[., ., ., ., .]"},"note":"Position 0 pushes index 0 with value 3."},{"at":{"i":1},"vars":{"p":1,"stack":"[]","ans":"[8, ., ., ., .]"},"note":"Position 1 reads 8, which is greater than nums[0] = 3. Index 0 gets the answer 8 and leaves the stack."},{"at":{"i":1},"vars":{"p":1,"stack":"[1]","ans":"[8, ., ., ., .]"},"note":"Position 1 pushes index 1 with value 8."},{"at":{"i":2},"vars":{"p":2,"stack":"[1, 2]","ans":"[8, ., ., ., .]"},"note":"Position 2 pushes index 2 with value 4."},{"at":{"i":3},"vars":{"p":3,"stack":"[1, 2, 3]","ans":"[8, ., ., ., .]"},"note":"Position 3 pushes index 3 with value 1."},{"at":{"i":4},"vars":{"p":4,"stack":"[1, 2]","ans":"[8, ., ., 2, .]"},"note":"Position 4 reads 2, which is greater than nums[3] = 1. Index 3 gets the answer 2 and leaves the stack."},{"at":{"i":4},"vars":{"p":4,"stack":"[1, 2, 4]","ans":"[8, ., ., 2, .]"},"note":"Position 4 pushes index 4 with value 2."},{"at":{"i":0},"vars":{"p":5,"stack":"[1, 2]","ans":"[8, ., ., 2, 3]"},"note":"Position 5 reads 3, which is greater than nums[4] = 2. Index 4 gets the answer 3 and leaves the stack."},{"at":{"i":0},"vars":{"p":5,"stack":"[1, 2]","ans":"[8, ., ., 2, 3]"},"note":"Position 5 reads 3 and pushes nothing."},{"at":{"i":1},"vars":{"p":6,"stack":"[1]","ans":"[8, ., 8, 2, 3]"},"note":"Position 6 reads 8, which is greater than nums[2] = 4. Index 2 gets the answer 8 and leaves the stack."},{"at":{"i":1},"vars":{"p":6,"stack":"[1]","ans":"[8, ., 8, 2, 3]"},"note":"Position 6 reads 8 and pushes nothing."},{"at":{"i":2},"vars":{"p":7,"stack":"[1]","ans":"[8, ., 8, 2, 3]"},"note":"Position 7 reads 4 and pushes nothing."},{"at":{"i":3},"vars":{"p":8,"stack":"[1]","ans":"[8, ., 8, 2, 3]"},"note":"Position 8 reads 1 and pushes nothing."},{"at":{"i":4},"vars":{"p":9,"stack":"[1]","ans":"[8, ., 8, 2, 3]"},"note":"Position 9 reads 2 and pushes nothing."},{"at":{"i":5},"vars":{"p":10,"stack":"[1]","ans":"[8, ., 8, 2, 3]"},"note":"Both passes end. Indices [1] keep -1."}]}
```

#### A Second Pass That Resolves Several Indices

The second trace reads 1, 2, 3, 2, 1. The first pass leaves the indices 2, 3 and 4 on the stack. The second pass resolves index 4 at position 6 and index 3 at position 7. Index 2 holds the maximum 3, so it keeps `-1` through position 9.

```trace
{"cells":[1,2,3,2,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"p":0,"stack":"[0]","ans":"[., ., ., ., .]"},"note":"Position 0 pushes index 0 with value 1."},{"at":{"i":1},"vars":{"p":1,"stack":"[]","ans":"[2, ., ., ., .]"},"note":"Position 1 reads 2, which is greater than nums[0] = 1. Index 0 gets the answer 2 and leaves the stack."},{"at":{"i":1},"vars":{"p":1,"stack":"[1]","ans":"[2, ., ., ., .]"},"note":"Position 1 pushes index 1 with value 2."},{"at":{"i":2},"vars":{"p":2,"stack":"[]","ans":"[2, 3, ., ., .]"},"note":"Position 2 reads 3, which is greater than nums[1] = 2. Index 1 gets the answer 3 and leaves the stack."},{"at":{"i":2},"vars":{"p":2,"stack":"[2]","ans":"[2, 3, ., ., .]"},"note":"Position 2 pushes index 2 with value 3."},{"at":{"i":3},"vars":{"p":3,"stack":"[2, 3]","ans":"[2, 3, ., ., .]"},"note":"Position 3 pushes index 3 with value 2."},{"at":{"i":4},"vars":{"p":4,"stack":"[2, 3, 4]","ans":"[2, 3, ., ., .]"},"note":"Position 4 pushes index 4 with value 1."},{"at":{"i":0},"vars":{"p":5,"stack":"[2, 3, 4]","ans":"[2, 3, ., ., .]"},"note":"Position 5 reads 1 and pushes nothing."},{"at":{"i":1},"vars":{"p":6,"stack":"[2, 3]","ans":"[2, 3, ., ., 2]"},"note":"Position 6 reads 2, which is greater than nums[4] = 1. Index 4 gets the answer 2 and leaves the stack."},{"at":{"i":1},"vars":{"p":6,"stack":"[2, 3]","ans":"[2, 3, ., ., 2]"},"note":"Position 6 reads 2 and pushes nothing."},{"at":{"i":2},"vars":{"p":7,"stack":"[2]","ans":"[2, 3, ., 3, 2]"},"note":"Position 7 reads 3, which is greater than nums[3] = 2. Index 3 gets the answer 3 and leaves the stack."},{"at":{"i":2},"vars":{"p":7,"stack":"[2]","ans":"[2, 3, ., 3, 2]"},"note":"Position 7 reads 3 and pushes nothing."},{"at":{"i":3},"vars":{"p":8,"stack":"[2]","ans":"[2, 3, ., 3, 2]"},"note":"Position 8 reads 2 and pushes nothing."},{"at":{"i":4},"vars":{"p":9,"stack":"[2]","ans":"[2, 3, ., 3, 2]"},"note":"Position 9 reads 1 and pushes nothing."},{"at":{"i":5},"vars":{"p":10,"stack":"[2]","ans":"[2, 3, ., 3, 2]"},"note":"Both passes end. Indices [2] keep -1."}]}
```

<!-- stage: code -->
### Two Passes In One Loop

#### The Virtual Pass

The loop runs `p` from 0 to `2 * n - 1`. It computes `i` with `%`, and it pushes only when `p < n`.

```java
static int[] nextGreaterRing(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    Arrays.fill(ans, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int p = 0; p < 2 * n; p++) {
        int i = p % n;
        while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
            ans[stack.pop()] = nums[i];
        }
        if (p < n) stack.push(i);
    }
    return ans;
}
```

An empty array makes `2 * n` equal to 0, so the loop body never runs and `p % n` never divides by zero.

#### The Copy That Is Not Needed

An alternative builds an array of length `2n` that holds the input twice and runs the previous lesson's method on it. The method then needs `n` more integers of memory and a second copy of every answer, and its stack can hold up to `2n` indices. Both versions run in O(n) time. The virtual pass uses O(n) extra space with a small constant, and the copy version has a larger constant.

<!-- stage: applicability -->
### When The Wrap Changes The Scan

#### The Cue For A Circle

The cue is a successor that continues from the last slot back to the first. Ring buffers, round-robin schedules and clock-face positions all behave this way. The invariant is that the stack holds exactly the real indices without an answer, with values that never increase from bottom to top. The second pass only gives those indices more positions to find a larger value.

#### Two False Friends

Running the line version once is the first false friend. It leaves every index whose answer lies before it in the array at `-1`, which is wrong for a ring. In the samples 3, 8, 4, 1, 2, a single pass gives the 4 no answer, while the ring gives it the 8.

Pushing in both passes is the second false friend. The answers stay correct, but the stack holds duplicate entries for the same slot, and the extra work has no use.

#### When It Does Not Apply

A walk that wraps more than once, such as one that takes a fixed number of steps `k` around the ring, needs more than two passes or a different state. The two-pass bound relies on the fact that the answer always lies within one full turn.

<!-- stage: exercises -->
### Exercises

#### [Build] Circular Successor Indices (Author exercise)
<!-- id: ms-circular-successor-index -->

**Prerequisites.** The wrap-around index in this lesson.

**Problem.** Let `nums` be an array of `n` integers read as a ring, where slot `n - 1` is followed by slot `0`. For a given start slot `s`, visit the slots `(s + 1) % n`, `(s + 2) % n` and so on, for at most `n - 1` slots. Return the index of the first visited slot whose value is strictly greater than `nums[s]`, or `-1` when no visited slot qualifies.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Start** satisfies `0 <= s < nums.length`.
- **Walk** never visits slot `s` again.
- **Return** is an `int` index, or `-1`.

**Example 1.** Input `nums = [3,8,4,1,2]`, `s = 2`, output `1`.

**Example 2.** Input `nums = [7,7,7,7]`, `s = 0`, output `-1`.

**Hint.** Write the index of the k-th visited slot as one expression in `s`, `k` and `n`. Which values of `k` are allowed?

**Changed decision.** The array is read as a ring, so the walk continues past the last slot instead of stopping there.

#### [Vary] Virtual Double Scan (Author exercise)
<!-- id: ms-virtual-double-scan -->

**Prerequisites.** The exercise above and the virtual pass in this lesson.

**Problem.** Let `nums` be an array read as a ring. For each index `i`, return the number of forward steps in circular order from slot `i` to the first slot with a strictly greater value. Return `0` for an index that has no such slot. Read the array through `nums[p % n]` for positions `p` from `0` to `2n - 1`, and allocate no second array.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values, and equal values are allowed.
- **Steps** range from `1` to `n - 1` when they exist.
- **Return** is an `int[]` of the same length, with `0` as the no-answer marker.

**Example 1.** Input `[3,8,4,1,2]`, output `[1,0,4,1,1]`.

**Example 2.** Input `[1,2,3,2,1]`, output `[1,1,0,4,2]`.

**Hint.** The steps equal a difference of virtual positions. Which position does a popped index record, and which does it keep on the stack?

**Changed decision.** The stack holds real indices, and the distance comes from the virtual position `p` of the resolving read.

#### [Boundary] All Equal Circular Array (Author exercise)
<!-- id: ms-all-equal-circular -->

**Prerequisites.** The two exercises above.

**Problem.** Let `nums` be a ring of non-negative integers. For each index, return the value of the first strictly greater slot in circular order, or `-1`. The array can have length 1, and it can hold the same value everywhere. In those cases an index never answers itself, and every answer stays `-1`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values with `0 <= nums[i] <= 10^9`.
- **Ties** never resolve an index.
- **Return** is an `int[]` of the same length.

**Example 1.** Input `[7,7,7,7]`, output `[-1,-1,-1,-1]`.

**Example 2.** Input `[2,2,5,2]`, output `[5,5,-1,5]`.

**Hint.** What does position `i + n` read, and does that read resolve index `i`?

**Changed decision.** The scan covers `2n` positions, and a strict comparison keeps equal values from resolving each other.

#### [Recognize] Next Greater Element II (LeetCode 503)
<!-- id: ms-next-greater-element-two -->

**Prerequisites.** The three exercises above.

**Problem.** Let `nums` be a circular integer array, where the next element of `nums[n - 1]` is `nums[0]`. For each element, return the first greater number that comes next in circular traversal order, or `-1` when it does not exist.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^4`.
- **Values** are integers with `-10^9 <= nums[i] <= 10^9`.
- **Traversal** visits at most `n - 1` further elements per index.
- **Return** is an `int[]` of the same length.

**Example 1.** Input `[6,2,9,4,4]`, output `[9,9,-1,6,6]`.

**Example 2.** Input `[5,-3,0,5,-3]`, output `[-1,0,5,-1,5]`.

**Hint.** Which indices can still wait after the first pass, and what must the second pass do with them?

**Changed decision.** The answer may lie before the index in the array, so one pass is not enough.
