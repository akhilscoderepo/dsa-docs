<!-- lesson-kind: standard -->
<!-- lesson-id: sorted-deduplication -->
## Sorted Deduplication

<!-- stage: context -->
### Why Repeated Ids Break A Report

A billing job reads a sorted `int[]` of customer ids, one entry per invoice line. A customer with five lines appears five times in a row. The job must produce the list of distinct customers, and it must reuse the same array, because the array is large and the caller owns it. The distinct ids must stay in ascending order.

The input has a promise that general arrays lack. Because the array is sorted, all copies of one id sit side by side. No copy of an id can hide far away from its siblings. The question is how much of that promise the algorithm can use, and what breaks when the promise is missing.

<!-- stage: naive -->
### Searching Backward For Each Value

The cautious approach does not trust the order. For each position, it scans every earlier kept position to look for the same value. If it finds none, it keeps the value. This works on any array, sorted or not.

```java
static int dedupeBySearch(int[] nums) {
    int kept = 0;
    for (int i = 0; i < nums.length; i++) {
        boolean seen = false;
        for (int j = 0; j < kept; j++) {
            if (nums[j] == nums[i]) { seen = true; break; }
        }
        if (!seen) nums[kept++] = nums[i];
    }
    return kept;
}
```

The method is correct, and it needs no sorted input. It does not use the one fact that the problem guarantees.

<!-- stage: bottleneck -->
### Counting Comparisons On Distinct Values

```predict
A sorted array holds 100,000 distinct ids. About how many comparisons does `dedupeBySearch` make, and which comparisons carry new information?

About five billion comparisons, because each value is compared with every earlier kept value. Only one comparison per value carries new information, the one with its immediate predecessor, because a sorted array puts any copy next to it.
```

Count the inner comparison. When every value is distinct, position `i` compares against all `i` earlier kept values, so the total is `0 + 1 + ... + (n - 1)`, which is `n * (n - 1) / 2`. That is O(n^2) time, or about 5 * 10^9 comparisons at `n = 100,000`.

Most of that work is wasted. In a sorted array, the largest kept value is the last one written. Every other kept value is smaller or equal to it. A new value can equal an earlier kept value only if it also equals the last kept value. One comparison therefore answers the question that the whole inner loop answers. The next stage turns that observation into a rule.

<!-- stage: insight -->
### Compare Against The Last Kept Value

#### Runs Of Equal Values

A sorted array splits into maximal blocks in which every element is equal. Call each block a **value run**. Two different runs never share a value, and the runs appear in ascending order of their value. The distinct values of the array are exactly one value per run.

<!-- names: value run, representative, last written value -->

#### One Representative Per Run

The algorithm keeps one **representative** for each run. The first element of a run is its representative. A read index visits all positions, and a write index marks the next free position of the output prefix. The first element of the array is always a representative, so the write index starts at 1 when the array is not empty.

#### The Admission Check

A new element at `nums[read]` starts a new run exactly when it differs from the **last written value**, which is `nums[write - 1]`. If it differs, copy it to `nums[write]` and advance `write`. If it is equal, skip it. The invariant is that `nums[0..write-1]` holds one representative of every run that the scan has started, in ascending order. The comparison reads `nums[write - 1]`, which always holds the last accepted value, so the same form extends to a limit of more than one copy.

<!-- stage: variables -->
### Track The Read Index And Write Index

Three quantities describe the state.

- **`read`** is the index under examination, from 1 to `nums.length - 1`.
- **`write`** is the length of the output prefix and the index of the next free position, with `1 <= write <= read` once the array is not empty.
- **Last written value** is `nums[write - 1]`, the only value the admission check reads.

An empty array has no first element, so the method returns 0 before any index is read.

<!-- stage: trace -->
### Follow Runs Through A Sorted Array

Take the sorted array `[1, 1, 2, 2, 2, 4, 7, 7]`. The first element, 1, is already the representative of its run, so `write` starts at 1. At `read = 1` the value 1 equals the last written value, so it is skipped. At `read = 2` the value 2 differs from 1, so it copies to position 1 and `write` becomes 2. The two further copies of 2 equal the last written value and are skipped. The method continues through 4 and 7 in the same way, and the final prefix is `[1, 2, 4, 7]` with return value 4.

```trace
{"cells":[1,1,2,2,2,4,7,7],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":1},"vars":{"array":"[1, 1, 2, 2, 2, 4, 7, 7]","kept":1},"note":"Read 1 at index 0. The first element always starts the first run, so 1 is admitted without a comparison. The prefix is [1]."},{"at":{"read":1,"write":1},"vars":{"array":"[1, 1, 2, 2, 2, 4, 7, 7]","kept":1},"note":"Read 1 at index 1. The value at index 0 of the prefix is 1, which equals 1, so 1 is skipped. The prefix is [1]."},{"at":{"read":2,"write":2},"vars":{"array":"[1, 2, 2, 2, 2, 4, 7, 7]","kept":2},"note":"Read 2 at index 2. The value at index 0 of the prefix is 1, which differs from 2, so 2 is admitted. The prefix is [1, 2]."},{"at":{"read":3,"write":2},"vars":{"array":"[1, 2, 2, 2, 2, 4, 7, 7]","kept":2},"note":"Read 2 at index 3. The value at index 1 of the prefix is 2, which equals 2, so 2 is skipped. The prefix is [1, 2]."},{"at":{"read":4,"write":2},"vars":{"array":"[1, 2, 2, 2, 2, 4, 7, 7]","kept":2},"note":"Read 2 at index 4. The value at index 1 of the prefix is 2, which equals 2, so 2 is skipped. The prefix is [1, 2]."},{"at":{"read":5,"write":3},"vars":{"array":"[1, 2, 4, 2, 2, 4, 7, 7]","kept":3},"note":"Read 4 at index 5. The value at index 1 of the prefix is 2, which differs from 4, so 4 is admitted. The prefix is [1, 2, 4]."},{"at":{"read":6,"write":4},"vars":{"array":"[1, 2, 4, 7, 2, 4, 7, 7]","kept":4},"note":"Read 7 at index 6. The value at index 2 of the prefix is 4, which differs from 7, so 7 is admitted. The prefix is [1, 2, 4, 7]."},{"at":{"read":7,"write":4},"vars":{"array":"[1, 2, 4, 7, 2, 4, 7, 7]","kept":4},"note":"Read 7 at index 7. The value at index 3 of the prefix is 7, which equals 7, so 7 is skipped. The prefix is [1, 2, 4, 7]."}]}
```

The second array allows two copies of each value, which is the variation of this lesson. Take `[1, 1, 1, 2, 2, 3]`. The admission check now reads `nums[write - 2]`, the second last written value. A value enters the prefix when it differs from that value. The third 1 equals `nums[write - 2]`, so it is skipped. The hardest step is the second 2 at `read = 4`, which looks like a repeat but still enters, because the value two positions back in the prefix is 1. The final prefix is `[1, 1, 2, 2, 3]` and the return value is 5.

```trace
{"cells":[1,1,1,2,2,3],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":1},"vars":{"array":"[1, 1, 1, 2, 2, 3]","kept":1},"note":"Read 1 at index 0. Fewer than 2 values are written, so 1 is admitted without a comparison. The prefix is [1]."},{"at":{"read":1,"write":2},"vars":{"array":"[1, 1, 1, 2, 2, 3]","kept":2},"note":"Read 1 at index 1. Fewer than 2 values are written, so 1 is admitted without a comparison. The prefix is [1, 1]."},{"at":{"read":2,"write":2},"vars":{"array":"[1, 1, 1, 2, 2, 3]","kept":2},"note":"Read 1 at index 2. The value at index 0 of the prefix is 1, which equals 1, so 1 is skipped. The prefix is [1, 1]."},{"at":{"read":3,"write":3},"vars":{"array":"[1, 1, 2, 2, 2, 3]","kept":3},"note":"Read 2 at index 3. The value at index 0 of the prefix is 1, which differs from 2, so 2 is admitted. The prefix is [1, 1, 2]."},{"at":{"read":4,"write":4},"vars":{"array":"[1, 1, 2, 2, 2, 3]","kept":4},"note":"Read 2 at index 4. The value at index 1 of the prefix is 1, which differs from 2, so 2 is admitted. The prefix is [1, 1, 2, 2]."},{"at":{"read":5,"write":5},"vars":{"array":"[1, 1, 2, 2, 3, 3]","kept":5},"note":"Read 3 at index 5. The value at index 2 of the prefix is 2, which differs from 3, so 3 is admitted. The prefix is [1, 1, 2, 2, 3]."}]}
```

<!-- stage: code -->
### Write The Admission Loop

```java
static int uniquePrefix(int[] nums) {
    if (nums.length == 0) return 0;
    int write = 1;
    for (int read = 1; read < nums.length; read++) {
        if (nums[read] != nums[write - 1]) {
            nums[write++] = nums[read];
        }
    }
    return write;
}

static int limitedPrefix(int[] nums, int copies) {
    int write = 0;
    for (int read = 0; read < nums.length; read++) {
        if (write < copies || nums[read] != nums[write - copies]) {
            nums[write++] = nums[read];
        }
    }
    return write;
}
```

The first method handles one copy per value. The second method generalizes the same check to any positive limit `copies`. The guard `write < copies` admits the first values without reading a negative index. Both loops make one pass, so each takes O(n) time. Neither allocates, so each takes O(1) extra space. After the call, only the first `write` positions have a defined meaning.

<!-- stage: applicability -->
### Recognize Sorted Runs And Their Limits

#### Recognize The Pattern

Use this pattern when the input is sorted, equal values are adjacent, and the task keeps a bounded number of copies of each value in place. The invariant states that the prefix holds one representative for each run started so far. Each correct solution keeps that statement true after every read. Run-length encoding of a character array fits the same shape, because each finished run owns one write decision.

#### Check The False Friend

The same loop on an unsorted array is a false friend. The array `[3, 1, 3]` gives the prefix `[3, 1, 3]`, because the last written value never equals the third element, so the duplicate 3 survives. General duplicate removal needs a set or a sort first. Sorting is covered in a later chapter, and general hash sets in chapter 04.

#### Check The Java Hazards

The expression `nums[write - 1]` throws `ArrayIndexOutOfBoundsException` when `write` is 0. An empty array reaches that case, so the method guards it. The generalized check uses `write < copies` first and relies on short-circuit evaluation, which skips the right operand when the left one is true.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Duplicates From Sorted Array (LeetCode 26)
<!-- id: ar-remove-sorted-duplicates -->

**Prerequisites.** The read index, write index and value run from this lesson.

**Problem.** Given an integer array `nums` sorted in non-decreasing order, overwrite its start with the distinct values in ascending order. Return `k`, the number of distinct values. The first `k` positions must hold the distinct values. Positions `k` and later may hold any values.

**Constraints.** The limits are:
- **`nums`** is a sorted `int[]` with `0 <= nums.length <= 10^5`.
- **Values** are any `int` values, and repeats are adjacent.
- **Extra space** is `O(1)`.
- **Return value** is `k`, which is 0 for an empty array.

**Example 1.** Input `[3, 3, 3, 8, 9, 9]`. Output `k = 3`, and the prefix is `[3, 8, 9]`.

**Example 2.** Input `[]`. Output `k = 0`. The input `[-5]` returns `k = 1` and keeps `[-5]`.

**Hint.** Which single earlier value tells you that the current value begins a new run?

**Changed decision.** Baseline case: one representative per run, admitted by comparison with the last written value.

#### [Vary] Remove Duplicates, Keep Two (LeetCode 80)
<!-- id: ar-keep-two-copies -->

**Prerequisites.** The remove-duplicates exercise above.

**Problem.** Given an integer array `nums` sorted in non-decreasing order, overwrite its start so that each distinct value appears at most twice. The kept values stay in ascending order. Return `k`, the length of the result prefix. Positions `k` and later may hold any values.

**Constraints.** The limits are:
- **`nums`** is a sorted `int[]` with `0 <= nums.length <= 10^5`.
- **Values** are any `int` values.
- **Copy limit** is exactly two per distinct value.
- **Extra space** is `O(1)`.

**Example 1.** Input `[4, 4, 4, 4, 6, 7, 7, 7]`. Output `k = 5`, and the prefix is `[4, 4, 6, 7, 7]`.

**Example 2.** Input `[2, 2]`. Output `k = 2`, because two copies are allowed. The input `[9]` returns `k = 1`.

**Hint.** Which earlier written position must differ from the current value for a third copy to be impossible?

**Changed decision.** The admission check now reads the second last written value, `nums[write - 2]`.

#### [Boundary] Keep One Per Run (Author exercise)
<!-- id: ar-keep-one-per-run -->

**Prerequisites.** The two exercises above.

**Problem.** Given a sorted integer array `nums`, overwrite its start with one value per run of equal values. Return `k`, the number of runs. Check two extremes: an array whose values are all equal and an array whose values are already distinct. A correct method keeps the whole array in the second case and one value in the first.

**Constraints.** The limits are:
- **`nums`** is a sorted `int[]` with `0 <= nums.length <= 10^5`.
- **Values** include `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Comparison** uses `!=` on the values and no subtraction.
- **Extra space** is `O(1)`.

**Example 1.** Input `[5, 5, 5]`. Output `k = 1`, and the prefix is `[5]`.

**Example 2.** Input `[1, 2, 3]`. Output `k = 3`, and the array is unchanged. The input `[Integer.MIN_VALUE, Integer.MAX_VALUE]` returns `k = 2`.

**Hint.** What happens to the write index when no value is skipped, and what happens when every value after the first is skipped?

**Changed decision.** The method meets the two extreme run structures, and the comparison must avoid subtraction, which overflows on extreme values.

#### [Recognize] String Compression (LeetCode 443)
<!-- id: ar-string-compression -->

**Prerequisites.** All three exercises above.

**Problem.** Given a `char[]` named `chars`, compress it in place. Each maximal run of one repeated character becomes that character, followed by the decimal digits of the run length when the length exceeds 1. Write the result at the start of `chars` and return its length `k`. Positions `k` and later may hold any values.

**Constraints.** The limits are:
- **`chars`** is a `char[]` with `1 <= chars.length <= 2000`.
- **Characters** are lowercase English letters.
- **Run length** may have several digits, and each digit takes one position.
- **Extra space** is `O(1)`, so no `String` or second array of the input size is allowed.

**Example 1.** Input `x, y, y, y, y, y, y, y, y, y, y, y, y, z`, which is `x`, then twelve `y`, then `z`. Output `k = 5`, and the prefix is `x, y, 1, 2, z`.

**Example 2.** Input a single run of 100 copies of `q`. Output `k = 4`, and the prefix is `q, 1, 0, 0`. The input `a` returns `k = 1`.

**Hint.** When one run ends, which positions does its output use, and can that output ever overtake the read index?

**Changed decision.** The array holds characters, and each finished run owns one write decision that may take several positions.
