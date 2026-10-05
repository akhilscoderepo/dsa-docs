<!-- lesson-kind: standard -->
<!-- lesson-id: exact-search -->
## Find A Value In Sorted Data

<!-- stage: context -->
### A Lookup That Slows As Data Grows

A support tool stores order numbers in ascending order. An agent types one number and the tool answers with the position of that order or reports that it does not exist. With 5,000 orders nobody notices a delay. After a year the list holds 20 million orders, and each lookup takes visible seconds, because the tool reads the list from the front.

The list is already sorted, and the tool ignores that fact. This lesson answers one question. How does a sorted array let a program rule out a large part of the data with a single comparison?

<!-- stage: naive -->
### Reading The Array From The Front

The direct method compares the target with each value in turn and returns the index of the first match. It returns `-1` after the last value.

```java
static int scanFor(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] == target) return i;
    }
    return -1;
}
```

The method is correct and it works on unsorted arrays too. On `[-1, 0, 3, 5, 9, 12]` with target 9, it makes five comparisons and returns 4.

```predict
The array holds 1,000,000 ascending values, and the target is larger than every value. How many comparisons does `scanFor` make before it returns `-1`?

It makes 1,000,000 comparisons, one per value. A missing target forces the loop to reach the end, and doubling the array doubles the work, so the cost is O(n).
```

<!-- stage: bottleneck -->
### One Comparison Rules Out One Value

Each comparison in `scanFor` rules out exactly one position. After `nums[0] == target` fails, the other `n - 1` positions are still possible. The loop pays a full comparison for every position it removes, so the worst case costs `n` comparisons, which is O(n).

The loop never uses the fact that the array is sorted. In sorted data, one comparison against a middle value says more. If the middle value is smaller than the target, every value to its left is smaller too, and none of them can match. A single comparison can therefore remove half of the remaining positions, and the scan throws that information away.

<!-- stage: insight -->
### Keep A Range And Halve It

Binary search keeps a **search interval**, which is a range of indexes `lo` to `hi` that may still contain the target. The method compares the target with the value at the middle of that range and discards the half that cannot contain it.

#### The Interval And Its Middle

This chapter writes the interval as closed, so both `nums[lo]` and `nums[hi]` are still candidates. The interval starts as `lo = 0` and `hi = nums.length - 1`. The **midpoint** is `mid = lo + (hi - lo) / 2`. It lies between `lo` and `hi` and splits the interval in two. The form `(lo + hi) / 2` fails for very large arrays. The sum `lo + hi` can exceed `Integer.MAX_VALUE` and wrap to a negative number. The subtraction form never leaves the range of an `int`.

<!-- names: search interval, midpoint, halving -->

#### The Discard Rule

Compare `nums[mid]` with the target. On equality, return `mid`. If `nums[mid] < target`, the sort order puts every index up to `mid` below the target, so the rule sets `lo = mid + 1`. If `nums[mid] > target`, every index from `mid` up is too large, so the rule sets `hi = mid - 1`. The search also drops `mid`, because the comparison has already examined its value.

#### Why Halving Gives O(log n)

Halving works because each step removes `mid` and at least half of the rest. The interval size drops from `s` to at most `s / 2`. After `k` steps the size is at most `n / 2^k`. The size reaches zero after about `log2(n) + 1` steps. For 20 million orders that is at most 25 comparisons. When `lo > hi`, the interval is empty and the target is absent.

<!-- stage: variables -->
### Four Names And Their Roles

The method tracks four values, and three of them change.

- **target** is the value to find and never changes.
- **lo** is the first index still possible, and it only moves right.
- **hi** is the last index still possible, and it only moves left.
- **mid** is recomputed from `lo` and `hi` at the start of every step.

The loop condition is `lo <= hi`. It says that at least one candidate remains. The loop ends either with a return from inside, or with an empty interval, where `lo` equals `hi + 1`.

<!-- stage: trace -->
### Two Searches Step By Step

#### Finding 9 In A Six Value Array

The array is `[-1, 0, 3, 5, 9, 12]` and the target is 9. The pointers `lo`, `hi` and `mid` mark the interval and its middle. The first midpoint is index 2 with value 3. That value is smaller than 9, so the search keeps only indexes 3 to 5. The second midpoint is index 4 with value 9, and the search returns 4 after two comparisons.

```trace
{"cells":[-1,0,3,5,9,12],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"target":"9"},"note":"Start with the whole array as the search interval, indexes 0 to 5."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"nums[mid]":"3","target":"9"},"note":"The value 3 is smaller than 9. Indexes 0 to 2 are discarded, so lo becomes 3."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"nums[mid]":"9","target":"9"},"note":"The value 9 equals the target, so the search returns index 4."}]}
```

#### Missing 2 In A Two Value Array

The array is `[1, 3]` and the target is 2, which lies between the two values. The first midpoint is index 0 with value 1, so the interval shrinks to index 1. The second midpoint is index 1 with value 3, which is larger than 2, so the interval shrinks to nothing. The pointer `lo` ends one past `hi`, and the method returns `-1`.

```trace
{"cells":[1,3],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":1,"mid":-1},"vars":{"target":"2"},"note":"Start with the whole array as the search interval, indexes 0 to 1."},{"at":{"lo":0,"hi":1,"mid":0},"vars":{"nums[mid]":"1","target":"2"},"note":"The value 1 is smaller than 2. Indexes 0 to 0 are discarded, so lo becomes 1."},{"at":{"lo":1,"hi":1,"mid":1},"vars":{"nums[mid]":"3","target":"2"},"note":"The value 3 is larger than 2. Indexes 1 to 1 are discarded, so hi becomes 0."},{"at":{"lo":1,"hi":0,"mid":-1},"vars":{"target":"2"},"note":"lo is 1 and hi is 0, so the interval is empty. The target is absent and the method returns -1."}]}
```

<!-- stage: code -->
### The Search Loop In Java

```java
static int binarySearch(int[] nums, int target) {
    int lo = 0;
    int hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

Every branch either returns or moves a bound past `mid`, so the interval loses at least one index per step. The loop cannot run forever. An empty array gives `hi = -1`, the loop body never runs, and the method returns `-1`.

The library method `Arrays.binarySearch(int[], int)` follows the same loop. It returns `-(position where the target would be inserted) - 1` for a missing target and not `-1`. With duplicate values it may return any matching index.

<!-- stage: applicability -->
### When Halving Is Safe

#### The Invariant

The invariant is that if the target occurs in the array, its index lies inside `[lo, hi]`. It holds at the start, because the interval covers the whole array. Each discard removes only indexes that the sort order proves unable to hold the target. The invariant therefore holds after every step, and an empty interval proves absence.

#### The False Friend

Unsorted input is the false friend. The code compiles and runs on any `int[]`, but a middle value then says nothing about the left or right half. Take `[9, 1, 5]` and target 9. The search compares 1 with 9 and discards indexes 0 and 1. It then compares 5 with 9 and reports a miss. The target sat at index 0. Sorting costs O(n log n), so a single lookup on unsorted data is cheaper by scanning.

#### Other Conditions That Break The Rule

A linked list also fails, because reaching the middle takes O(n) steps and removes the benefit. Duplicate values do not break the loop, but the returned index is then unspecified. The next lesson fixes that case. An interval that is not sorted in the direction the code assumes breaks the rule in the same way as unsorted input.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Search (LeetCode 704)
<!-- id: bs-exact-704 -->

**Prerequisites.** The search interval, midpoint and discard rule of this lesson.

**Problem.** Given an array `nums` sorted in strictly ascending order and an integer `target`, return the index `i` with `nums[i] == target`. Return `-1` when no such index exists.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`; the empty array is valid.
- **Values** are distinct `int` values in ascending order.
- **Target** is any `int`, including a value outside the range of `nums`.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [-1,0,3,5,9,12]` and `target = 9`, output 4.

**Example 2.** Input `nums = [5]` and `target = 2`, output -1.

**Hint.** After comparing with `nums[mid]`, which indexes can no longer hold the target? Move a bound past `mid`.

**Changed decision.** Basic case: a comparison decides which half to discard, and equality ends the search.

#### [Vary] Descending Search (Author exercise)
<!-- id: bs-descending -->

**Prerequisites.** The first exercise above.

**Problem.** Given an array `nums` sorted in strictly descending order and an integer `target`, return the index of `target` or `-1` when it is absent. The order of the array is the only change from the previous exercise.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are distinct `int` values in descending order.
- **Target** is any `int`.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [12,9,5,3,0,-1]` and `target = 5`, output 2.

**Example 2.** Input `nums = [12,9,5]` and `target = 6`, output -1.

**Hint.** If `nums[mid]` is smaller than the target in a descending array, on which side do the larger values sit?

**Changed decision.** The comparison result keeps its meaning, but it now maps to the opposite bound update.

#### [Boundary] Two Elements (Author exercise)
<!-- id: bs-two-elements -->

**Prerequisites.** The first exercise and the second trace of this lesson.

**Problem.** Given a sorted array `nums` of distinct values and a `target`, return the midpoint indexes that the search of this lesson compares, in order. The loop stops when it finds the target or when the interval is empty. Use the midpoint `lo + (hi - lo) / 2`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 100`.
- **Values** are distinct `int` values in ascending order.
- **Target** is any `int`.
- **Answer** has at most `floor(log2(nums.length)) + 1` entries.

**Example 1.** Input `nums = [1,3]` and `target = 2`, output `[0,1]`.

**Example 2.** Input `nums = [1,3]` and `target = 3`, output `[0,1]`.

**Hint.** With `lo = 0` and `hi = 1`, the first midpoint is 0. What is the interval after `nums[0] < target`?

**Changed decision.** The output is the sequence of probes, so the answer shows the shrinking interval and not only its result.

#### [Recognize] Matrix As One Sorted Array (LeetCode 74)
<!-- id: bs-matrix-probe-budget -->

**Prerequisites.** All exercises above. Integer division and remainder.

**Problem.** An `m` by `n` matrix has ascending rows. The first value of each row is larger than the last value of the previous row. Given the matrix and an integer `target`, return the number of comparisons that a binary search makes before it decides. Treat the matrix as one array of length `m * n`, where index `k` is row `k / n` and column `k % n`. Return the count of comparisons and whether the target exists, as a two entry array `[count, found]` with `found` equal to 1 or 0.

**Constraints.** The limits are:
- **Shape** is `1 <= m, n <= 100`.
- **Values** are distinct `int` values in row-major ascending order.
- **Target** is any `int`.
- **Answer** is `[count, found]` with `count <= floor(log2(m * n)) + 1`.

**Example 1.** Input `matrix = [[1,3,5],[7,9,11]]` and `target = 9`, output `[2,1]`.

**Example 2.** Input `matrix = [[1,3,5],[7,9,11]]` and `target = 4`, output `[3,0]`.

**Hint.** Run the loop of this lesson on indexes `0` to `m * n - 1`, and read each value as `matrix[mid / n][mid % n]`.

**Changed decision.** The array is virtual, and the counted probes show that the budget depends on `m * n` and not on the matrix shape.
