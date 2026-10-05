<!-- lesson-kind: standard -->
<!-- lesson-id: rotated-target -->
## Find A Target After Rotation

<!-- stage: context -->
### Finding A Timestamp In A Wrapped Log

The ring buffer from the previous lesson now holds `[6, 7, 9, 1, 2, 3, 4]`. A support engineer asks whether the timestamp 2 is in the buffer and in which slot. With seven slots a scan is fine. With 50 million slots, a scan takes seconds for every query, and the service answers thousands of queries a minute.

The array has two ascending runs, and a plain binary search can move in the wrong direction on it. The question for this lesson is how a search decides, at each middle slot, on which side the target can lie.

<!-- stage: naive -->
### Scanning The Wrapped Array

The direct method compares each slot with the target and returns the first matching index.

```java
static int firstMatchByScan(int[] nums, int target) {
    int i = 0;
    while (i < nums.length && nums[i] != target) i++;
    return i < nums.length ? i : -1;
}
```

For `[6, 7, 9, 1, 2, 3, 4]` and target 2, the method returns 4 after five comparisons. A missing target costs all seven.

```predict
Treat the wrapped array like a sorted one and run the plain search from the first lesson for target 7. What index does it return, and why?

It returns -1. The first middle value is 1, which is smaller than 7, so the search moves right and never looks at index 1 where the 7 sits. The array is sorted only in two runs, so a middle value says nothing about the whole left side.
```

<!-- stage: bottleneck -->
### A Middle Value Alone Proves Nothing

The scan costs up to `n` comparisons, which is O(n). The plain binary search fails for a different reason. Its move depends on one comparison of the target with `nums[mid]`. That comparison means something only when the array is sorted around `mid`.

Some structure survives. The array has a single place where the order restarts, so any interval that is cut at `mid` has the restart point in at most one of its two halves. The half without the restart point is a plain ascending run. The search can read the end values of that half, decide whether the target lies between them, and keep or discard the whole half. The plain search lacks this step.

<!-- stage: insight -->
### Find The Sorted Half First

Every cut at `mid` produces a left half `[lo, mid]` and a right half `[mid, hi]`. At least one of them is a **sorted half**, a half without the restart point, which is ascending from its first to its last index. The search identifies it first and only then asks about the target.

<!-- names: sorted half, range test, one-pass search -->

#### Identifying The Sorted Half

Compare `nums[lo]` with `nums[mid]`. If `nums[lo] <= nums[mid]`, the left half is a sorted half, because a restart point inside `[lo, mid]` would make `nums[mid]` smaller than `nums[lo]` for distinct values. The comparison uses `<=` because `mid` equals `lo` when two indexes remain. If the comparison fails, the restart point lies in the left half, and the right half `[mid, hi]` is the sorted half.

#### The Range Test

Once the sorted half is known, a **range test** asks whether the target lies between its end values. For a sorted left half, the test is `nums[lo] <= target && target < nums[mid]`. A pass means the target can only be in that half, so `hi = mid - 1`. A fail discards the half, so `lo = mid + 1`. For a sorted right half, the test is `nums[mid] < target && target <= nums[hi]`. A pass sets `lo = mid + 1`, and a fail sets `hi = mid - 1`. Equality at `mid` returns the index before any of this.

#### Why This Is A One-Pass Search

This **one-pass search** reads the array only through the loop and halves the interval every step. It does not locate the restart point separately. The cost is O(log n), with a constant number of reads per step. A second approach finds the restart point with the previous lesson and then searches one run. Both are logarithmic, and the exercises compare them.

<!-- stage: variables -->
### The State Of The Loop

The loop keeps three indexes and makes two decisions per step.

- **lo** and **hi** are the closed ends of the interval that may hold the target.
- **mid** is `lo + (hi - lo) / 2`, and `nums[mid]` is compared with the target first.
- **sorted half** is the left half when `nums[lo] <= nums[mid]`, and the right half otherwise.

The first decision names the sorted half. The second is the range test on that half. The loop test is `lo <= hi`, because `mid` is dropped on every update, as in the first lesson.

<!-- stage: trace -->
### Two Searches In A Wrapped Array

#### Target 2 Is Present

The array is `[6, 7, 9, 1, 2, 3, 4]`. The first midpoint is index 3 with value 1. The left value 6 is larger than 1, so the right half is the sorted half. The range test `1 < 2 <= 4` passes, so `lo` becomes 4. The midpoint at index 5 has value 3, and the left value 2 is not larger than 3, so the left half is sorted. The range test `2 <= 2 < 3` passes, so `hi` becomes 4. The midpoint at index 4 equals the target, and the search returns 4.

```trace
{"cells":[6,7,9,1,2,3,4],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":-1},"vars":{"target":"2"},"note":"Start with the whole array, indexes 0 to 6."},{"at":{"lo":0,"hi":6,"mid":3},"vars":{"nums[mid]":"1","sorted half":"right"},"note":"The right half is sorted, from 1 to 4. The target 2 lies inside it, so lo becomes 4."},{"at":{"lo":4,"hi":6,"mid":5},"vars":{"nums[mid]":"3","sorted half":"left"},"note":"The left half is sorted, from 2 to 3. The target 2 lies inside it, so hi becomes 4."},{"at":{"lo":4,"hi":4,"mid":4},"vars":{"nums[mid]":"2","target":"2"},"note":"The value 2 equals the target, so the search returns index 4."}]}
```

#### Target 3 Is Absent

The array is `[4, 5, 6, 7, 0, 1, 2]` and the target is 3, which falls in the gap between the values 2 and 4. The first midpoint is index 3 with value 7, and the left half `[4, 7]` is sorted. The range test `4 <= 3` fails, so `lo` becomes 4. The midpoint at index 5 has value 1, and the left half `[0, 1]` is sorted, but 3 is not in it, so `lo` becomes 6. The midpoint at index 6 has value 2, and 3 is not in its single-value half, so `lo` becomes 7. The interval is empty.

```trace
{"cells":[4,5,6,7,0,1,2],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":-1},"vars":{"target":"3"},"note":"Start with the whole array, indexes 0 to 6."},{"at":{"lo":0,"hi":6,"mid":3},"vars":{"nums[mid]":"7","sorted half":"left"},"note":"The left half is sorted, from 4 to 7. The target 3 is outside it, so lo becomes 4."},{"at":{"lo":4,"hi":6,"mid":5},"vars":{"nums[mid]":"1","sorted half":"left"},"note":"The left half is sorted, from 0 to 1. The target 3 is outside it, so lo becomes 6."},{"at":{"lo":6,"hi":6,"mid":6},"vars":{"nums[mid]":"2","sorted half":"left"},"note":"The left half is sorted, from 2 to 2. The target 3 is outside it, so lo becomes 7."},{"at":{"lo":7,"hi":6,"mid":-1},"vars":{"target":"3"},"note":"The interval is empty, so the target is absent and the search returns -1."}]}
```

<!-- stage: code -->
### The One-Pass Search In Java

```java
static int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}
```

Each branch drops `mid`, so the interval shrinks and the loop ends. The first branch handles an unrotated array, where the left half is always sorted. The method assumes distinct values. An empty array returns `-1` without entering the loop.

<!-- stage: applicability -->
### When A Half Can Be Discarded

#### The Invariant

The invariant is that the target, if present, lies inside `[lo, hi]`. The search drops the sorted half when the target lies outside its end values. It drops the other half when the target lies inside them. Each case uses only the order of a sorted half, which is the single fact the search can trust.

#### The False Friend

Finding the minimum alone is the false friend. It returns the restart point and says nothing about a target. The restart point splits the array into two ascending runs, and the target may lie in either one. A complete method must then choose a run by comparing the target with `nums[0]` and search that run. The one-pass search merges both steps.

#### Where Duplicates Break The Rule

With repeated values, `nums[lo] <= nums[mid]` no longer proves that the left half is sorted. In `[1, 0, 1, 1, 1]` the three values `nums[lo]`, `nums[mid]` and `nums[hi]` are equal at the first step, and the restart point could lie on either side. The safe move is to shrink both ends by one, which can cost O(n) on arrays of equal values. Exercise three treats this case.

<!-- stage: exercises -->
### Exercises

#### [Build] Search In Rotated Sorted Array (LeetCode 33)
<!-- id: bs-rotated-search-33 -->

**Prerequisites.** The sorted half and the range test of this lesson, and the previous lesson.

**Problem.** An array `nums` of distinct integers was sorted in ascending order and then rotated by an unknown number of positions. Given `nums` and an integer `target`, return the index of `target`, or `-1` when it does not occur.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 5000`.
- **Values** are distinct `int` values.
- **Shape** is an ascending array rotated by `0` to `nums.length - 1` positions.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [9,11,14,2,4,6]` and `target = 4`, output 4.

**Example 2.** Input `nums = [9,11,14,2,4,6]` and `target = 5`, output -1.

**Hint.** At `mid`, which half is sorted? If the target lies between that half's end values, keep it. Otherwise discard it.

**Changed decision.** Basic case: the search must identify a sorted half before it can compare the target.

#### [Vary] Pivot Then Search (Author exercise)
<!-- id: bs-pivot-then-search -->

**Prerequisites.** The first exercise above and the previous lesson.

**Problem.** Solve the previous problem in two phases. First find the index `p` of the minimum value. Then run an exact binary search on the ascending run that can hold the target, and return the index in `nums`, or `-1` when the target does not occur.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 5000`.
- **Values** are distinct `int` values in a rotated ascending array.
- **Phases** run one after the other, and each costs O(log n).
- **Answer** is an index of `nums` or `-1`.

**Example 1.** Input `nums = [9,11,14,2,4,6]` and `target = 11`, output 1.

**Example 2.** Input `nums = [9,11,14,2,4,6]` and `target = 2`, output 3.

**Hint.** If `p` is 0, search the whole array. Otherwise, the run `[0, p - 1]` holds the target when `target >= nums[0]`, and the run `[p, n - 1]` holds it otherwise.

**Changed decision.** The task splits into two logarithmic searches instead of one search with two kinds of step.

#### [Boundary] Search With Duplicates (LeetCode 81)
<!-- id: bs-rotated-search-81 -->

**Prerequisites.** Both exercises above.

**Problem.** An array `nums` of integers, possibly with repeated values, was sorted in non-decreasing order and then rotated by an unknown number of positions. Given `nums` and an integer `target`, return `true` when `target` occurs in `nums` and `false` otherwise.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 5000`.
- **Values** are `int` values, and duplicates are allowed.
- **Answer** is a boolean, not an index.
- **Complexity** may degrade to O(n) when many values are equal.

**Example 1.** Input `nums = [1,0,1,1,1]` and `target = 0`, output `true`.

**Example 2.** Input `nums = [2,2,2,3,2,2]` and `target = 4`, output `false`.

**Hint.** If `nums[lo]`, `nums[mid]` and `nums[hi]` are all equal, no half is proved sorted. Which ends can you drop without losing the target?

**Changed decision.** A three-way tie proves nothing, so the search drops one index from each end.

#### [Recognize] Explain Both Strategies (Author exercise)
<!-- id: bs-compare-strategies -->

**Prerequisites.** All exercises above.

**Problem.** Given a rotated array `nums` of distinct integers and a `target`, return the pair `[onePass, twoPhase]`. The value `onePass` is the number of loop iterations of the one-pass search of this lesson. The value `twoPhase` is the number of loop iterations of the minimum search plus the number of iterations of the exact search on the chosen run, as in the previous exercise. Both strategies are O(log n), and the pair makes the constant factors visible.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 5000`.
- **Values** are distinct `int` values in a rotated ascending array.
- **Target** is any `int`.
- **Answer** is a pair of non-negative `int` values.

**Example 1.** Input `nums = [9,11,14,2,4,6]` and `target = 4`, output `[2,4]`.

**Example 2.** Input `nums = [9,11,14,2,4,6]` and `target = 5`, output `[3,5]`.

**Hint.** The two-phase method pays for the minimum search even when the target is found at once. State what each strategy must prove before it discards a half.

**Changed decision.** The output compares two correct methods, so the choice rests on proof obligations and constants and not on the answer.
