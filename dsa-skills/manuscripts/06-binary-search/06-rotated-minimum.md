<!-- lesson-kind: standard -->
<!-- lesson-id: rotated-minimum -->
## Find The Minimum After Rotation

<!-- stage: context -->
### Finding The Oldest Ring Buffer Entry

A device logs its last seven timestamps in a ring buffer. The writer overwrites the oldest slot, then moves to the next slot, and wraps around at the end. After a few wraps the array reads `[6, 7, 9, 1, 2, 3, 4]` when read from slot 0. The timestamps are still ascending, but the sequence starts in the middle. A report needs the slot of the oldest entry, because the report must list the entries from oldest to newest.

The array is not sorted, so exact search and bounds do not apply directly. This lesson answers one question. How can a program find the start of such a wrapped sorted sequence without reading every slot?

<!-- stage: naive -->
### Reading Every Slot

The direct method reads each slot and keeps the index of the smallest value.

```java
static int indexOfSmallest(int[] nums) {
    int best = 0;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] < nums[best]) best = i;
    }
    return best;
}
```

For `[6, 7, 9, 1, 2, 3, 4]` the method returns index 3. A slightly faster version stops at the first slot where a value is smaller than its predecessor. The full scan is correct for any order. The faster version is correct only because the array is a rotated sorted array.

```predict
The buffer holds 1,000,000 slots, and the oldest entry sits in slot 999,990. How many slots does the loop read, and which fact about the data does the loop ignore?

It reads all 1,000,000 slots, which is O(n). It ignores that each part of the array is ascending, so a comparison with one end shows which part a middle slot belongs to.
```

<!-- stage: bottleneck -->
### Two Ascending Runs Hide In One Array

The scan costs `n` reads, which is O(n). The array is not random. It consists of two ascending runs, a high run first and a low run second, and every value of the low run is smaller than every value of the high run. The oldest entry is the first value of the low run.

A middle value belongs to one of the two runs. If the middle value is larger than the last value of the array, it is in the high run, because every value of the low run is smaller than the last value. Then the start of the low run lies to its right. The scan never asks which run a value belongs to.

<!-- stage: insight -->
### Compare The Middle With The Right End

A **rotation** by `k` moves the last `k` values of a sorted array to its front. The array `[1, 2, 3, 4, 6, 7, 9]` rotated by 3 becomes `[6, 7, 9, 1, 2, 3, 4]`. The **pivot** is the index of the smallest value, the place where the sorted order restarts. A rotation by 0 is the original array, and its pivot is index 0.

<!-- names: rotation, pivot, right endpoint -->

#### The Search Rule

Compare `nums[mid]` with the **right endpoint** `nums[hi]`. If `nums[mid] > nums[hi]`, then `mid` is in the high run and the pivot lies strictly after it, so `lo = mid + 1`. Otherwise `nums[mid] < nums[hi]` holds for distinct values, `mid` is in the low run or the array is not rotated, and the pivot is at `mid` or to its left, so `hi = mid`. The loop ends when `lo == hi`.

#### Why The Right Endpoint

The right endpoint is a stable reference. In the low run, every value is at most `nums[hi]`. In the high run, every value is larger. This holds for every interval that still contains the pivot. The left endpoint fails. The test `nums[mid] > nums[lo]` is true in a high run with the pivot to its right. It is also true in an interval that is already sorted, where the minimum is `nums[lo]` itself. Telling these cases apart needs an extra check.

#### The Interval

The search uses the closed interval `[lo, hi]` with `hi = nums.length - 1` and the test `lo < hi`, as in the peak lesson. The step `hi = mid` keeps the pivot candidate. The step `lo = mid + 1` drops `mid`, which cannot be the pivot, because a larger value sits to its right.

<!-- stage: variables -->
### What The Endpoints Mean

The search has three names, and the right endpoint is the reference.

- **lo** is the smallest index that can still hold the pivot.
- **hi** is an index that can hold the pivot, and `nums[hi]` is the reference value for the comparison.
- **mid** is `lo + (hi - lo) / 2`, which satisfies `lo <= mid < hi` while `lo < hi`.

The values in `nums` are distinct. When the loop ends, `lo == hi` is the pivot, and `nums[lo]` is the minimum. For an unrotated array, the pivot is index 0.

<!-- stage: trace -->
### One Rotated And One Unrotated Array

#### A Rotated Array

The array is `[3, 4, 5, 1, 2]`. The first midpoint is index 2 with value 5, larger than the right endpoint 2, so the pivot lies right of it and `lo` becomes 3. The midpoint at index 3 has value 1, smaller than the right endpoint 2, so `hi` becomes 3. One index remains, and the minimum is 1 at index 3.

```trace
{"cells":[3,4,5,1,2],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":4,"mid":-1},"vars":{},"note":"Start with the whole array, indexes 0 to 4. The pivot lies inside it."},{"at":{"lo":0,"hi":4,"mid":2},"vars":{"nums[mid]":"5","nums[hi]":"2"},"note":"The value 5 is larger than the right endpoint 2, so mid is in the high run. The pivot lies right of mid, and lo becomes 3."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"nums[mid]":"1","nums[hi]":"2"},"note":"The value 1 is not larger than the right endpoint 2, so the pivot is at mid or left of it. hi becomes 3."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"minimum":"1"},"note":"One index remains. The pivot is index 3, and the minimum is 1."}]}
```

#### An Array That Was Not Rotated

The array is `[2, 4, 6, 8, 10]`, with rotation 0. The midpoint at index 2 has value 6, smaller than the right endpoint 10, so `hi` becomes 2. The midpoint at index 1 has value 4, smaller than 6, so `hi` becomes 1. The midpoint at index 0 has value 2, smaller than 4, so `hi` becomes 0. The pivot is index 0, and no special case was needed.

```trace
{"cells":[2,4,6,8,10],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":4,"mid":-1},"vars":{},"note":"Start with the whole array, indexes 0 to 4. The pivot lies inside it."},{"at":{"lo":0,"hi":4,"mid":2},"vars":{"nums[mid]":"6","nums[hi]":"10"},"note":"The value 6 is not larger than the right endpoint 10, so the pivot is at mid or left of it. hi becomes 2."},{"at":{"lo":0,"hi":2,"mid":1},"vars":{"nums[mid]":"4","nums[hi]":"6"},"note":"The value 4 is not larger than the right endpoint 6, so the pivot is at mid or left of it. hi becomes 1."},{"at":{"lo":0,"hi":1,"mid":0},"vars":{"nums[mid]":"2","nums[hi]":"4"},"note":"The value 2 is not larger than the right endpoint 4, so the pivot is at mid or left of it. hi becomes 0."},{"at":{"lo":0,"hi":0,"mid":-1},"vars":{"minimum":"2"},"note":"One index remains. The pivot is index 0, and the minimum is 2."}]}
```

<!-- stage: code -->
### The Pivot Search In Java

```java
static int pivotIndex(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static int minimum(int[] nums) {
    return nums[pivotIndex(nums)];
}
```

The method reads one pair of values per step and makes at most `floor(log2(n)) + 1` steps. The method assumes a non-empty array of distinct values. A one-element array skips the loop and returns index 0. An array rotated by `k` has its pivot at index `k`.

<!-- stage: applicability -->
### When The Right End Decides

#### The Invariant

This is the invariant: the pivot lies inside `[lo, hi]`. A larger middle value than the right endpoint proves that the sorted order restarts after `mid`, so dropping `mid` and everything before it is safe. A smaller middle value proves that `mid` to `hi` is ascending, so the minimum of that part is `nums[mid]`, and the pivot is at `mid` or before it.

#### The False Friend

A rotated array with repeated values is the false friend. In `[2, 2, 2, 0, 2]` and in `[2, 0, 2, 2, 2]`, the first midpoint sees `nums[mid] == nums[hi]`. The equality does not say which side holds the pivot. The safe move is `hi--`. A copy of the same value remains at `mid`, so the minimum value stays inside the interval. An array of equal values then costs O(n) steps.

#### A Second Problem That Looks Alike

Searching a rotated array for a target value needs the same rotation fact but a different decision. Finding the minimum does not finish that task, because the target may sit in either run. The next lesson builds on this one.

<!-- stage: exercises -->
### Exercises

#### [Build] Find Minimum In Rotated Sorted Array (LeetCode 153)
<!-- id: bs-rotated-min-153 -->

**Prerequisites.** The right endpoint rule and the closed interval of this lesson.

**Problem.** An array `nums` of distinct integers was sorted in ascending order and then rotated by some number of positions between 0 and `nums.length - 1`, as defined in this lesson. Return the minimum value of `nums`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 5000`.
- **Values** are distinct `int` values.
- **Shape** is an ascending array rotated by `0` to `nums.length - 1` positions.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [6,8,9,2,4,5]`, output 2.

**Example 2.** Input `nums = [4,7,9]`, output 4.

**Hint.** Compare `nums[mid]` with `nums[hi]`. Which side holds the smaller values when `nums[mid]` is larger?

**Changed decision.** Basic case: the comparison is against the right endpoint and never against a target.

#### [Vary] Rotation Count (Author exercise)
<!-- id: bs-rotation-count -->

**Prerequisites.** The first exercise above.

**Problem.** An array `nums` of distinct integers was sorted in ascending order and then rotated by `k` positions, with `0 <= k < nums.length`. A rotation by `k` moves the last `k` values to the front. Return `k`, which equals the index of the minimum value.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 5000`.
- **Values** are distinct `int` values.
- **Answer** satisfies `0 <= k < nums.length`.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [6,8,9,2,4,5]`, output 3.

**Example 2.** Input `nums = [1,5,8]`, output 0.

**Hint.** Return the index at which the loop ends and not the value stored there.

**Changed decision.** The output switches from the minimum value to its index, and the unrotated array answers 0.

#### [Boundary] Two Values (Author exercise)
<!-- id: bs-two-values -->

**Prerequisites.** Both exercises above.

**Problem.** Given a rotated array `nums` of distinct integers with `1 <= nums.length <= 2`, return the pair `[index, steps]`. The value `index` is the index of the minimum. The value `steps` is the number of times the loop body of the search runs.

**Constraints.** The limits are:
- **Length** is `1` or `2`.
- **Values** are distinct `int` values.
- **Shape** may be `[a]`, `[a,b]` with `a < b`, or `[a,b]` with `a > b`.
- **Answer** is `[index, steps]` with `steps <= 1`.

**Example 1.** Input `nums = [2,1]`, output `[1,1]`.

**Example 2.** Input `nums = [1,2]`, output `[0,1]`.

**Hint.** With two values, `mid` equals `lo`. Trace both arrays and check which bound moves when `nums[mid] > nums[hi]`.

**Changed decision.** The interval holds exactly two indexes, so the midpoint equals `lo` and the update must still shrink it.

#### [Recognize] Find Minimum With Duplicates (LeetCode 154)
<!-- id: bs-rotated-min-154 -->

**Prerequisites.** All exercises above.

**Problem.** An array `nums` of integers, possibly with repeated values, was sorted in non-decreasing order and then rotated by some number of positions. Return the minimum value of `nums`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 5000`.
- **Values** are `int` values, and duplicates are allowed.
- **Shape** is a non-decreasing array rotated by `0` to `nums.length - 1` positions.
- **Complexity** may degrade to O(n) when many values are equal.

**Example 1.** Input `nums = [2,2,2,0,1]`, output 0.

**Example 2.** Input `nums = [3,3,1,3]`, output 1.

**Hint.** What does `nums[mid] == nums[hi]` prove about the minimum? Which single index can be dropped safely?

**Changed decision.** Equality of the middle and the right endpoint decides nothing, so the search shrinks by one index and the worst case becomes linear.
