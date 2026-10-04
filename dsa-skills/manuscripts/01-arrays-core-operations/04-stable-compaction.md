<!-- lesson-kind: standard -->
<!-- lesson-id: stable-compaction -->
## Stable Compaction

<!-- stage: context -->
### Why Deleting From An Array Is Costly

A service receives a shared `int[]` of 100,000 session ids from its caller. The service must drop every id that equals an expired value. The caller keeps using the same array afterward, so the service cannot allocate a replacement array and hand it back. The remaining ids must keep their original order, because the caller reads them by position.

A Java array has a fixed length. No operation deletes the middle of one. Every "removal" is really a rewrite of positions. The question is how to rewrite the positions so that the surviving values stay in order. A second question is how to touch each position only a constant number of times.

<!-- stage: naive -->
### Shifting The Tail After Each Removal

The direct approach finds an unwanted value and closes the gap at once. It copies every later element one position to the left. Then it records that the array holds one fewer live value.

```java
static int removeByShifting(int[] nums, int val) {
    int length = nums.length;
    int i = 0;
    while (i < length) {
        if (nums[i] == val) {
            for (int j = i + 1; j < length; j++) nums[j - 1] = nums[j];
            length--;
        } else {
            i++;
        }
    }
    return length;
}
```

This code is correct. It keeps the surviving values in order and it works inside the given array. After a shift, the loop does not advance `i`, because the value that moved into position `i` has not been checked yet.

<!-- stage: bottleneck -->
### Counting The Shifted Elements

```predict
An array holds 100,000 copies of the value to remove. About how many element copies does `removeByShifting` perform?

About five billion. The first removal shifts 99,999 elements, the next shifts 99,998, and so on, so the copies add up to n * (n - 1) / 2.
```

Count the inner copy statement. Each removal copies every element that sits after the removed position. When all `n` elements match, removal `r` copies `n - r` elements. The total is `(n - 1) + (n - 2) + ... + 1`, which is `n * (n - 1) / 2`. That is O(n^2) time. For `n = 100,000` the count is about 5 * 10^9 copies, which takes seconds.

The work repeats itself. A surviving value near the end of the array moves once for every removal in front of it. Yet its final position is already known from the start. It lands at the number of surviving values that precede it. If the code writes each survivor directly to that position, no element needs more than one write. The next stage shows how to track that position.

<!-- stage: insight -->
### Writing Each Survivor To Its Final Position

#### Two Indexes Over One Array

The **read index** visits every position from left to right exactly once. The **write index** marks the next position that receives a kept value. The write index never passes the read index, because it advances only when the read index has accepted a value. So a write never overwrites a value that the scan has not read yet.

<!-- names: read index, write index, stable order -->

#### The Invariant And The Safe Move

After each step, `nums[0..write-1]` holds exactly the accepted values read so far, in the order the scan read them. The safe move has two cases. If `nums[read]` is accepted, copy it to `nums[write]` and advance `write`. If it is rejected, do nothing and let the read index move on. Both cases keep the invariant true. The copy touches one position, so each value is written at most once.

#### Stable Order And The Return Value

An algorithm has **stable order** when accepted values keep their relative order from the input. Compaction has it automatically, because the read index only moves forward and each accepted value goes to the next free write position. The method returns `write`, the count of accepted values. Only `nums[0..write-1]` has a defined meaning afterward. The array length does not change, and the positions from `write` onward still hold old values, so a correct caller reads only the first `write` positions.

<!-- stage: variables -->
### Track Two Indexes And One Count

Three quantities describe the state at every step.

- **`read`** is the index of the value under examination, from `0` to `nums.length - 1`.
- **`write`** is the index of the next free position in the accepted prefix, with `0 <= write <= read` before each decision.
- **Accepted prefix** is the range `nums[0..write-1]`, and `write` is also its length and the final return value.

The acceptance test is the only part that changes between problems. Everything else stays fixed.

<!-- stage: trace -->
### Follow The Indexes Through Two Arrays

The first array is `[2, 7, 2, 5, 9, 2, 8]` and the rule rejects the value 2. At `read = 0` the value 2 is rejected, so `write` stays 0. At `read = 1` the value 7 is accepted and copies to position 0. The array now begins `[7, 7, ...]`, and `write` becomes 1. The old 7 at position 1 is not a problem, because position 1 lies outside the accepted prefix until `write` reaches it. The scan continues the same way and ends with the prefix `[7, 5, 9, 8]` and the return value 4.

```trace
{"cells":[2,7,2,5,9,2,8],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"array":"[2, 7, 2, 5, 9, 2, 8]","kept":0},"note":"Read 2 at index 0. The rule rejects it, so nothing is written and the write index stays 0."},{"at":{"read":1,"write":1},"vars":{"array":"[7, 7, 2, 5, 9, 2, 8]","kept":1},"note":"Read 7 at index 1. The rule keep everything except 2 accepts it, so it copies to index 0. The accepted prefix is now [7]."},{"at":{"read":2,"write":1},"vars":{"array":"[7, 7, 2, 5, 9, 2, 8]","kept":1},"note":"Read 2 at index 2. The rule rejects it, so nothing is written and the write index stays 1."},{"at":{"read":3,"write":2},"vars":{"array":"[7, 5, 2, 5, 9, 2, 8]","kept":2},"note":"Read 5 at index 3. The rule keep everything except 2 accepts it, so it copies to index 1. The accepted prefix is now [7, 5]."},{"at":{"read":4,"write":3},"vars":{"array":"[7, 5, 9, 5, 9, 2, 8]","kept":3},"note":"Read 9 at index 4. The rule keep everything except 2 accepts it, so it copies to index 2. The accepted prefix is now [7, 5, 9]."},{"at":{"read":5,"write":3},"vars":{"array":"[7, 5, 9, 5, 9, 2, 8]","kept":3},"note":"Read 2 at index 5. The rule rejects it, so nothing is written and the write index stays 3."},{"at":{"read":6,"write":4},"vars":{"array":"[7, 5, 9, 8, 9, 2, 8]","kept":4},"note":"Read 8 at index 6. The rule keep everything except 2 accepts it, so it copies to index 3. The accepted prefix is now [7, 5, 9, 8]."},{"at":{"read":7,"write":4},"vars":{"array":"[7, 5, 9, 8, 9, 2, 8]","kept":4},"note":"The scan ends. The return value is 4, and only the first 4 positions are meaningful."}]}
```

The second array is `[5, 8, 0, 3, 0, 1]` and the rule rejects zero. Here the first two values are accepted while `read` and `write` are equal, so each value copies onto itself. The first zero opens a gap, and from then on `write` is smaller than `read`. The hardest step is the last accepted value, a 1 at position 5 that moves to position 3. The accepted prefix is `[5, 8, 3, 1]` and the return value is 4. The two trailing positions still hold old values.

```trace
{"cells":[5,8,0,3,0,1],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":1},"vars":{"array":"[5, 8, 0, 3, 0, 1]","kept":1},"note":"Read 5 at index 0. The rule keep every non-zero value accepts it, so it copies to index 0. The accepted prefix is now [5]."},{"at":{"read":1,"write":2},"vars":{"array":"[5, 8, 0, 3, 0, 1]","kept":2},"note":"Read 8 at index 1. The rule keep every non-zero value accepts it, so it copies to index 1. The accepted prefix is now [5, 8]."},{"at":{"read":2,"write":2},"vars":{"array":"[5, 8, 0, 3, 0, 1]","kept":2},"note":"Read 0 at index 2. The rule rejects it, so nothing is written and the write index stays 2."},{"at":{"read":3,"write":3},"vars":{"array":"[5, 8, 3, 3, 0, 1]","kept":3},"note":"Read 3 at index 3. The rule keep every non-zero value accepts it, so it copies to index 2. The accepted prefix is now [5, 8, 3]."},{"at":{"read":4,"write":3},"vars":{"array":"[5, 8, 3, 3, 0, 1]","kept":3},"note":"Read 0 at index 4. The rule rejects it, so nothing is written and the write index stays 3."},{"at":{"read":5,"write":4},"vars":{"array":"[5, 8, 3, 1, 0, 1]","kept":4},"note":"Read 1 at index 5. The rule keep every non-zero value accepts it, so it copies to index 3. The accepted prefix is now [5, 8, 3, 1]."},{"at":{"read":6,"write":4},"vars":{"array":"[5, 8, 3, 1, 0, 1]","kept":4},"note":"The scan ends. The return value is 4, and only the first 4 positions are meaningful."}]}
```

<!-- stage: code -->
### Write The Compaction Loop

```java
static int compactKeeping(int[] nums, java.util.function.IntPredicate keep) {
    int write = 0;
    for (int read = 0; read < nums.length; read++) {
        if (keep.test(nums[read])) {
            nums[write] = nums[read];
            write++;
        }
    }
    return write;
}

static int removeValue(int[] nums, int val) {
    return compactKeeping(nums, v -> v != val);
}
```

The loop reads each position once, so it takes O(n) time. Two integer variables are the only extra storage, so extra space is constant. Only the predicate changes between problems: `v != val` removes a value, while another predicate keeps a different set. The method returns `write` and never shrinks the array. When the caller needs the surviving values, it reads `nums[0..write-1]` only. Printing the whole array shows leftover values from before the compaction.

<!-- stage: applicability -->
### Recognize Compaction And Its Limits

#### Recognize The Pattern

Use compaction when a problem says to keep some values, preserve their order, and reuse the input array. The words "in place" and "return the new length" signal the same thing. The invariant is that `nums[0..write-1]` holds exactly the accepted values read so far. Every correct solution in this family preserves that statement after each step.

#### Check The False Friend

Swapping each rejected value with the last element looks like the same idea but is a false friend. It also works in place in O(n) time. It breaks stable order, because the last value jumps to the front of the unread region. Use the swap version only when the problem permits any order.

#### Check The Java Hazards

Java gives no way to cut an array shorter. The method reports the new length, and the caller must respect it. A solution that claims the suffix was deleted misstates the contract. When a problem asks for a specific suffix, such as zeros, the code must write that suffix itself in a second pass.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Element (LeetCode 27)
<!-- id: ar-remove-element -->

**Prerequisites.** The read index and write index from this lesson.

**Problem.** Given an integer array `nums` and an integer `val`, overwrite the start of `nums` with every value that is not equal to `val`. The kept values appear in their original relative order. Return `k`, the number of kept values. The first `k` positions of `nums` must hold the kept values. Positions `k` and later may hold any values.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `0 <= nums.length <= 10^5`.
- **Values** and `val` are any `int` values.
- **Extra space** is `O(1)`, so no second array is allowed.
- **Return value** is `k`, with `0 <= k <= nums.length`.

**Example 1.** Input `nums = [4, 7, 4, 9, 4, 2]`, `val = 4`. Output `k = 3`, and the first three positions hold `[7, 9, 2]`.

**Example 2.** Input `nums = [6, 6, 6]`, `val = 6`. Output `k = 0`, because every value is removed. An empty input also returns 0.

**Hint.** When `nums[read]` differs from `val`, where must it go so that all earlier kept values stay in front of it?

**Changed decision.** Baseline case: one acceptance test, and the return value is the only measure of the result.

#### [Vary] Move Zeroes (LeetCode 283)
<!-- id: ar-move-zeroes -->

**Prerequisites.** The remove-element exercise above.

**Problem.** Given an integer array `nums`, rearrange it in place so that all non-zero values come first, in their original relative order, and all zeros come last. The method returns nothing. After the call, `nums` has the same length and the same multiset of values as before.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 10^5`.
- **Values** are any `int` values, and zero is the only rejected value.
- **Extra space** is `O(1)`.
- **Output** is the mutated input array, and every position has a defined value.

**Example 1.** Input `[0, 0, 5, 0, -2, 7]`. Output `[5, -2, 7, 0, 0, 0]`.

**Example 2.** Input `[0, 0, 0]`. Output `[0, 0, 0]`. An array with no zero, such as `[3, 1]`, stays as it is.

**Hint.** After the compaction pass, the count of kept values is known. Which positions still hold stale values, and what must they contain?

**Changed decision.** The suffix after `write` now has a required value, so the method needs a second step that fills it.

#### [Boundary] Keep Evens (Author exercise)
<!-- id: ar-keep-evens -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums`, overwrite the start of `nums` with its even values in their original relative order and return `k`, the number of even values. An integer is even when its remainder on division by 2 is zero. The caller ignores positions `k` and later.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `0 <= nums.length <= 10^5`.
- **Values** are any `int` values, including negative values and zero.
- **Evenness** follows the mathematical definition, so `-4` is even and `-3` is odd.
- **Extra space** is `O(1)`.

**Example 1.** Input `[-2, 3, 4]`. Output `k = 2`, and the prefix is `[-2, 4]`.

**Example 2.** Input `[-3, 1, 5]`. Output `k = 0`, because Java computes `-3 % 2` as `-1`. A test of the form `nums[i] % 2 == 1` misses negative odd values, so the safe test compares the remainder with 0.

**Hint.** What does Java return for `-3 % 2`? Which comparison against zero gives the right answer for both signs?

**Changed decision.** The acceptance test now meets a Java hazard: the remainder of a negative number is negative.

#### [Recognize] Filter Positives (Author exercise)
<!-- id: ar-filter-positives -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `nums`, overwrite the start of `nums` with its strictly positive values in their original relative order. Return `k`, the number of positive values. Zero is not positive. Nothing is promised about positions `k` and later.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `0 <= nums.length <= 10^5`.
- **Values** are any `int` values, including `Integer.MIN_VALUE`.
- **Extra space** is `O(1)`.
- **Return value** is `k`.

**Example 1.** Input `[3, -1, 0, 5, -7, 2]`. Output `k = 3`, and the prefix is `[3, 5, 2]`.

**Example 2.** Input `[0, -4, Integer.MIN_VALUE]`. Output `k = 0`.

**Hint.** Which part of the compaction loop changes when the keep rule changes, and which part stays fixed?

**Changed decision.** The acceptance test changes, but the read index, the write index and the invariant stay identical.
