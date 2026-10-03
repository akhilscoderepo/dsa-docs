<!-- lesson-kind: standard -->
<!-- lesson-id: exact-search -->
## Exact Search

<!-- stage: context -->
### A Guide Looking For House Number 4271

A tour guide stands at one end of a very long street. The houses are numbered in increasing order along it, and she has been asked to point out house number 4271, or to say that there is no such house. She can walk to any house she likes and read its number, but each walk costs time, so she wants to read as few numbers as possible.

Her first thought is to start at the first house and read every number in turn. Then she realizes that the numbering gives her more than a list. If she walks to a house in the middle and reads 3000, she knows without walking any further that every house before that one has a smaller number, and that 4271, if it exists at all, lies in the second half. One reading has taught her about thousands of houses she never visited.

<!-- stage: naive -->
### Read Every House From The Start

The plain method reads each number in turn and stops when it finds the target.

```java
static int findByWalking(int[] houses, int target) {
    for (int i = 0; i < houses.length; i++) {
        if (houses[i] == target) return i;
    }
    return -1;
}
```

It returns the position of the target when there is one, and minus one otherwise. It does not use the fact that the numbers are sorted, so it would give the same answers on a street where the numbers were shuffled.

<!-- stage: bottleneck -->
### Each Reading Rules Out One House

When the target is absent or sits near the end, the walk reads all n numbers, which is O(n) readings. A street with a billion houses would need a billion readings in the worst case. Each reading in this method answers only the question about the house it was taken at, so it eliminates a single position.

On a sorted street a reading eliminates far more. If the number read at position `mid` is smaller than the target, then every position up to `mid` is too small, and if it is larger, every position from `mid` onward is too large. The method above throws that information away. A method that keeps it would remove half of the remaining houses with each reading, and would need only about thirty readings for a billion houses, which is O(log n).

<!-- stage: insight -->
### Keep Only Where The Target Could Be

Binary search keeps a **search interval**, the stretch of positions that could still hold the target. It starts as the whole array. At each step the algorithm reads the **middle** position and compares it with the target. If they are equal, the search is finished. If the middle value is too small, the target can only be to its right, so the left edge of the interval moves to one past the middle. If the middle value is too large, the right edge moves to one before the middle. Either way the middle position itself is removed, because it has been checked, so the interval shrinks after every comparison and the loop must end.

The convention for this lesson is a closed interval: both `lo` and `hi` are positions that might hold the target, the loop runs while `lo <= hi`, and an empty interval, `lo > hi`, means the target is absent. The invariant is one sentence: if the target is in the array, it is inside the interval. The **discard rule** is what keeps that sentence true, because a position is dropped only when the comparison proves that it cannot hold the target.

<!-- names: search interval, discard rule, safe midpoint -->

The position to read is computed as `lo + (hi - lo) / 2`, the **safe midpoint**. The shorter form `(lo + hi) / 2` adds two positions before dividing, and for arrays with more than a billion elements the sum can exceed the largest `int` and become negative. The safe form never produces a value outside the interval, since `hi - lo` is never negative inside the loop.

The same loop works on a descending array if the two moves are exchanged: a middle value that is too large now means the target is to the right. The comparison decides which side to keep, and the contract about the order decides what each outcome means. A matrix whose rows are sorted and whose rows follow each other in order is one long sorted array in disguise. Position `p` of the long array is row `p / cols`, column `p % cols`, so the same loop searches it without copying anything.

<!-- stage: variables -->
### Low, High, Middle And The Verdict

`lo` is the first position that could still hold the target and `hi` is the last. `mid` is recomputed at every turn and is not remembered between turns. The verdict is a comparison with three outcomes: equal, too small, too large. After the loop, `lo` is greater than `hi`, and the method returns minus one. For a matrix, the same three variables range over virtual positions from zero to rows times columns minus one, and the row and column are computed from `mid` only when a value must be read.

<!-- stage: trace -->
### A Hit And A Miss

The first trace looks for 23 among ten sorted numbers. The first reading at position 4 finds 16, which is too small, so the left edge jumps to 5. The second reading at position 7 finds 56, which is too large, so the right edge drops to 6. The third reading at position 5 finds 23 and the search ends. The step to study is the second one, where a single reading removes three positions on the right at once.

```trace
{"cells":[2,5,8,12,16,23,38,56,72,91],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":9,"mid":4},"vars":{"value":16,"target":23},"note":"Read position 4: 16 is too small, so positions 0 to 4 are ruled out and lo becomes 5."},{"at":{"lo":5,"hi":9,"mid":7},"vars":{"value":56,"target":23},"note":"Read position 7: 56 is too large, so positions 7 to 9 are ruled out and hi becomes 6."},{"at":{"lo":5,"hi":6,"mid":5},"vars":{"value":23,"target":23},"note":"Read position 5: 23 equals 23. The search ends and returns 5."}]}
```

The second trace looks for 40 in the same array, which is absent. The interval shrinks reading by reading until its two edges cross. The step to study is the last one, where the left edge is 7 and the right edge is 6: the interval is empty, so the loop stops and the method reports that the number is absent.

```trace
{"cells":[2,5,8,12,16,23,38,56,72,91],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":9,"mid":4},"vars":{"value":16,"target":40},"note":"Read position 4: 16 is too small, so positions 0 to 4 are ruled out and lo becomes 5."},{"at":{"lo":5,"hi":9,"mid":7},"vars":{"value":56,"target":40},"note":"Read position 7: 56 is too large, so positions 7 to 9 are ruled out and hi becomes 6."},{"at":{"lo":5,"hi":6,"mid":5},"vars":{"value":23,"target":40},"note":"Read position 5: 23 is too small, so positions 5 to 5 are ruled out and lo becomes 6."},{"at":{"lo":6,"hi":6,"mid":6},"vars":{"value":38,"target":40},"note":"Read position 6: 38 is too small, so positions 6 to 6 are ruled out and lo becomes 7."},{"at":{"lo":7,"hi":6,"mid":-1},"vars":{"target":40,"verdict":"absent"},"note":"The left edge 7 has passed the right edge 6, so the interval is empty and the target 40 is absent."}]}
```

<!-- stage: code -->
### Closed Interval, Both Directions And A Matrix

```java
static int search(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

static int searchDescending(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[mid] > target) lo = mid + 1;     // too large: the target is further right
        else hi = mid - 1;
    }
    return -1;
}

static boolean searchMatrix(int[][] m, int target) {
    int rows = m.length;
    if (rows == 0) return false;
    int cols = m[0].length;
    long lo = 0, hi = (long) rows * cols - 1;
    while (lo <= hi) {
        long mid = lo + (hi - lo) / 2;
        int v = m[(int) (mid / cols)][(int) (mid % cols)];
        if (v == target) return true;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}
```

Each loop halves the interval, so the number of readings is at most about log base two of n plus one, which is O(log n), and the extra space is O(1). The matrix version works over n equal to rows times columns, so it costs O(log(rows times cols)). The virtual index is kept in a `long` so that the product cannot overflow when a matrix is very large.

<!-- stage: applicability -->
### When The Order Lets You Skip Half

Use exact search when the data is sorted under a stated order and the question is whether one value occurs, or where. The invariant to write in a comment before coding is the sentence about the interval: if the target is present, it lies between `lo` and `hi`. Write the interval convention next to it, closed or half-open, because the loop condition and both updates depend on it.

A false friend is any array whose order was not promised. Without an order, a reading says nothing about the other positions, so no half is safe to throw away, and a plain scan is the only correct method. Another false friend is an array that is sorted by one key while the target is described by another. The comparison must use the same key that defines the order.

In Java, never compute the middle as `(lo + hi) / 2` for arrays that might be huge. Use `lo + (hi - lo) / 2`. When the answer must be an index, return it inside the loop on equality, and return minus one only after the loop. For descending data, reverse the comparison, and do not sort the data just to reuse the ascending code.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Search (LeetCode 704)
<!-- id: bs-binary-search -->

**Prerequisites.** Chapter 01 array indexing; the loop invariants of Chapter 00.

**Problem.** Given an array of distinct integers sorted in increasing order and a target, return the index of the target, or minus one if it is absent. State the interval convention in a comment, and run in O(log n).

**Constraints.** 1 <= nums.length <= 10000 and every value lies between -100000 and 100000. The values are strictly increasing.

**Example 1.** Input `nums = [4, 8, 15, 16, 23, 42], target = 16`, output 3.

**Example 2.** Input `nums = [7], target = 3`, output -1.

**Hint.** After comparing the middle value with the target, which positions can you prove are not the answer? What does it mean when the left edge passes the right edge?

**Changed decision.** First rung: every comparison removes the position it read and everything on the wrong side of it.

#### [Vary] Descending Search (Author exercise)
<!-- id: bs-descending-search -->

**Prerequisites.** The binary-search exercise above.

**Problem.** Given an array sorted in decreasing order and a target, return the index of the target or minus one. Do not reverse or copy the array, and explain which comparison moves which edge.

**Constraints.** 0 <= nums.length <= 10000, strictly decreasing values within the `int` range, and any `int` target.

**Example 1.** Input `nums = [90, 70, 50, 30, 10], target = 30`, output 3.

**Example 2.** Input `nums = [9, 4, 1], target = 5`, output -1.

**Hint.** If the middle value is larger than the target, on which side of the middle must the target be? What if the array is empty?

**Changed decision.** The order is reversed, so the mapping from comparison to movement is reversed with it, while the shape of the loop stays.

#### [Boundary] Two Elements (Author exercise)
<!-- id: bs-two-elements -->

**Prerequisites.** The two exercises above.

**Problem.** Trace the search on the array `[1, 3]` for the targets 1, 3 and 2. For each, count the readings, and verify in code that the interval holds strictly fewer positions after every comparison, so the loop cannot run forever.

**Constraints.** The array is exactly `[1, 3]`. Instrument the loop to record the interval size before each reading.

**Example 1.** Input `target = 1`, output index 0 after one reading, since the first middle is position 0.

**Example 2.** Input `target = 2`, output -1 after two readings, with interval sizes 2 and then 1.

**Hint.** Which position is the first middle for two elements, and what happens to the interval when the target is larger than it? Why does moving an edge past the middle guarantee progress?

**Changed decision.** The smallest nontrivial array forces you to check that the middle is removed whichever side is kept.

#### [Recognize] Search a 2D Matrix (LeetCode 74)
<!-- id: bs-search-matrix-virtual -->

**Prerequisites.** All three exercises above, and the matrix indexing of Chapter 02.

**Problem.** A matrix has rows sorted from left to right, and the first value of each row is larger than the last value of the row before it. Return whether a target occurs. Treat the matrix as one sorted array and map a virtual position to a row and a column.

**Constraints.** 1 <= rows, cols <= 100 and values within the `int` range. Do not copy the matrix into a new array.

**Example 1.** Input `m = [[2, 4, 6], [8, 10, 12]], target = 10`, output true.

**Example 2.** Input `m = [[2, 4, 6], [8, 10, 12]], target = 7`, output false.

**Hint.** Which row and column does virtual position `p` correspond to? What are the first and last virtual positions?

**Changed decision.** The array is virtual, so the search runs over positions and converts each middle position to coordinates on demand.
