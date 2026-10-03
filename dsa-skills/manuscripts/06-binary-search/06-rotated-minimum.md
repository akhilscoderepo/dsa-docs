<!-- lesson-kind: standard -->
<!-- lesson-id: rotated-minimum -->
## Rotated Minimum

<!-- stage: context -->
### Gates On A Circular Race Track

A circular race track has gates numbered 1 through 40 clockwise. A steward walked the track and wrote down the gate numbers in the order he met them, but he began at a random gate, so his list climbs to 40, jumps back to 1, and climbs again until it reaches the gate just before his starting point. For example, a list that starts at gate 23 reads 23, 24, and so on up to 40, then 1, 2, and so on up to 22.

The race director now wants to know where gate 1 sits in the steward's list, because that tells her how far the steward's start was from the official start. The list is long, and each entry she checks means reading a line of tiny handwriting. She suspects that the shape of the list should help her: it is two sorted stretches joined end to end, with exactly one place where the numbers drop.

<!-- stage: naive -->
### Read The Whole List

The simplest method reads every entry and remembers the smallest.

```java
static int smallestByReading(int[] list) {
    int best = list[0];
    for (int i = 1; i < list.length; i++) {
        if (list[i] < best) best = list[i];
    }
    return best;
}
```

It gives the right number for any list, rotated or not, and it uses no property of the list at all.

<!-- stage: bottleneck -->
### Ignoring The Two Sorted Stretches

Reading every entry is O(n), and the cost does not change however regular the list is. The list is two ascending stretches, and the smallest number is the start of the second one, at the single drop. A method that exploits this should be able to compare an entry with something and decide which of the two stretches that entry lies in, and then discard the other stretch's far side.

Comparing the middle entry with the first entry, the obvious choice, does not work cleanly. If the middle is larger than the first, the middle is in the first stretch and the drop is to its right, but if the middle is smaller than the first, the drop is to its left, and when the list is not rotated at all, the middle is larger than the first even though there is no drop to find. The two cases give opposite advice for the same comparison. A comparison that gives unambiguous advice would make the search O(log n).

<!-- stage: insight -->
### Compare The Middle With The Right End

The comparison that works is between the middle element and the **right endpoint** of the interval, the element at `hi`. All the elements in the first stretch are larger than all the elements in the second stretch, and the last element belongs to the second stretch, or is in the only stretch when the array is not rotated. If `nums[mid] > nums[hi]`, the middle must be in the first stretch, so the drop is strictly to its right, and `lo = mid + 1`. If `nums[mid] < nums[hi]`, the middle and everything between it and `hi` are in one ascending stretch, so the minimum is at `mid` or to its left, and `hi = mid`.

This is the **right-end test**, and it needs the elements to be distinct, so equality never occurs between `mid` and `hi` while `mid < hi`. The interval `[lo, hi]` contains the **rotation point**, the position of the smallest value, which is also the number of positions the array was rotated by. The loop runs while `lo < hi`, and when the edges meet the position is the rotation point. For a list that was never rotated, the right-end test always finds `nums[mid] < nums[hi]`, so `hi` moves toward 0, which is correct.

<!-- names: right endpoint, right-end test, rotation point -->

Duplicates break the test. If `nums[mid] == nums[hi]`, the middle could be in either stretch: the arrays 2, 2, 2, 0, 2 and 2, 0, 2, 2, 2 have the same three comparison values at some step and different answers. What can be done safely is to drop the right endpoint with `hi = hi - 1`, because the value at `hi` is still present at `mid`, so the minimum value remains in the interval. This **duplicate shrink** keeps the invariant but removes only one element, so an array that is mostly equal values can force O(n) steps. No comparison-based method can do better in the worst case, since a single different element could be hiding anywhere in a run of equal values.

<!-- stage: variables -->
### Edges, Middle And The Right End

`lo` and `hi` are the edges of the closed interval that must contain the rotation point. `mid` is always strictly less than `hi` in the loop, so comparing it with `nums[hi]` never compares an element with itself. The comparison has two outcomes for distinct values, and a third, equality, when duplicates are allowed. The loop ends when the edges meet, and that position holds the minimum. The rotation count and the index of the minimum are the same number.

<!-- stage: trace -->
### Dropping Toward The Drop

The first trace looks for the smallest value in 4, 5, 6, 7, 0, 1, 2. The first comparison is 7 against the right end 2, so the middle is in the first stretch and the left edge moves to 4. The step to study is the third: position 4 holds 0, which is smaller than 1, so the right edge moves to 4 and the edges meet at the minimum.

```trace
{"cells":[4,5,6,7,0,1,2],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":3},"vars":{"middle":7,"rightEnd":2},"note":"Position 3 holds 7, larger than the right end 2. The middle is in the first stretch, so the drop is to its right and lo becomes 4."},{"at":{"lo":4,"hi":6,"mid":5},"vars":{"middle":1,"rightEnd":2},"note":"Position 5 holds 1, smaller than the right end 2. The minimum is at 5 or earlier, so hi becomes 5."},{"at":{"lo":4,"hi":5,"mid":4},"vars":{"middle":0,"rightEnd":1},"note":"Position 4 holds 0, smaller than the right end 1. The minimum is at 4 or earlier, so hi becomes 4."},{"at":{"lo":4,"hi":4,"mid":-1},"vars":{"minimum":0},"note":"The edges meet at position 4, which holds the minimum 0."}]}
```

The second trace allows duplicates and uses 2, 2, 2, 0, 1, 2. The first comparison finds the middle equal to the right end, 2 against 2, which gives no advice, so the right edge is dropped by one. The next comparisons behave normally. The step to study is the first one, since it removes a single element, which is the price of ambiguity.

```trace
{"cells":[2,2,2,0,1,2],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":2},"vars":{"middle":2,"rightEnd":2},"note":"Position 2 holds 2, equal to the right end 2. The middle gives no advice, so drop one copy of the right end and hi becomes 4."},{"at":{"lo":0,"hi":4,"mid":2},"vars":{"middle":2,"rightEnd":1},"note":"Position 2 holds 2, larger than the right end 1. The middle is in the first stretch, so the drop is to its right and lo becomes 3."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"middle":0,"rightEnd":1},"note":"Position 3 holds 0, smaller than the right end 1. The minimum is at 3 or earlier, so hi becomes 3."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"minimum":0},"note":"The edges meet at position 3, which holds the minimum 0."}]}
```

<!-- stage: code -->
### Right-End Test With And Without Repeats

```java
static int findMinIndex(int[] a) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;      // the drop is to the right of mid
        else hi = mid;                         // mid is in the last stretch
    }
    return lo;
}

static int findMin(int[] a) {
    return a[findMinIndex(a)];
}

static int findMinWithRepeats(int[] a) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;
        else if (a[mid] < a[hi]) hi = mid;
        else hi--;                             // equal: drop one copy of the right end
    }
    return a[lo];
}
```

The distinct version halves the interval each turn, so it is O(log n) time and O(1) space, and the index it returns is also the rotation count. The repeat-tolerant version is O(log n) when the equality case is rare, and O(n) in the worst case, such as an array of equal values with one smaller value hidden among them.

<!-- stage: applicability -->
### When Sorted Order Was Spliced

Use the rotated-minimum search when a sorted array has been rotated, so that it consists of two ascending stretches, and the question is where the stretches join. The invariant is that the interval contains the rotation point. Compare with the right endpoint, because that comparison gives one clear answer for distinct values.

A false friend is the comparison with the left endpoint. It looks symmetric, but it fails for arrays that were not rotated, or rotated by a full turn, and the standard fix needs an extra special case. Another false friend is a rotated array with duplicates treated as if it were distinct: the same code would sometimes discard the half that holds the minimum. A third is searching for a target value by finding the minimum first and assuming that finishes the job. It only gives the join point, and the target lookup needs one more search, which the next lesson treats.

In Java, check the one-element array, since the loop condition `lo < hi` makes it return at once. Use `a[mid] > a[hi]` with `mid < hi` so that `mid` is never compared with itself. For duplicates, say in a comment that the shrink step keeps the invariant but gives up logarithmic time in the worst case.

<!-- stage: exercises -->
### Exercises

#### [Build] Find Minimum in Rotated Sorted Array (LeetCode 153)
<!-- id: bs-rotated-minimum -->

**Prerequisites.** The peak-search lesson, and comparison of an element with an endpoint.

**Problem.** A strictly increasing array was rotated an unknown number of times, which may be zero. Return its smallest element. Compare the middle with the right endpoint and run in O(log n).

**Constraints.** 1 <= nums.length <= 5000, distinct values within the `int` range, and the array is a rotation of a sorted array.

**Example 1.** Input `nums = [9, 11, 15, 2, 4, 6]`, output 2.

**Example 2.** Input `nums = [3, 5, 8]`, output 3, since the array was not changed.

**Hint.** If the middle is larger than the right end, in which stretch is it? What does the middle being smaller than the right end say?

**Changed decision.** First rung: the comparison is with the right endpoint, because that one comparison gives unambiguous advice.

#### [Vary] Rotation Count (Author exercise)
<!-- id: bs-rotation-count -->

**Prerequisites.** The rotated-minimum exercise above.

**Problem.** Return how many positions a sorted array was rotated to the right, which equals the index of the smallest element in the rotated array. A sorted array that was not rotated has a count of zero.

**Constraints.** 1 <= nums.length <= 5000 and distinct values. The method must return the index, not the value.

**Example 1.** Input `nums = [9, 11, 15, 2, 4, 6]`, output 3.

**Example 2.** Input `nums = [3, 5, 8]`, output 0.

**Hint.** Is the index of the minimum the same as the number of elements before it? How many elements were moved from the end to the front?

**Changed decision.** The method returns a position instead of a value, so the loop's final `lo` is the answer without any array read.

#### [Boundary] Two Values (Author exercise)
<!-- id: bs-two-values -->

**Prerequisites.** The two exercises above.

**Problem.** Trace the search on `[2, 1]` and on `[1, 2]`, and on a one-element array. State which element `mid` is in each case, which comparison is made, and why the edges meet after one step.

**Constraints.** The arrays are exactly `[2, 1]`, `[1, 2]` and any one-element array. Verify the traces in code by recording each `lo`, `hi` and `mid`.

**Example 1.** Input `nums = [2, 1]`, output index 1, after one comparison of 2 with 1.

**Example 2.** Input `nums = [1, 2]`, output index 0, after one comparison of 1 with 2.

**Hint.** What is `mid` when the interval has two elements? Which edge moves in each case, and why can neither case loop forever?

**Changed decision.** The shortest rotated arrays force you to verify that the middle equals the left edge and that the update still shrinks the interval.

#### [Recognize] Find Minimum in Rotated Sorted Array II (LeetCode 154)
<!-- id: bs-rotated-minimum-repeats -->

**Prerequisites.** All three exercises above.

**Problem.** The rotated array may now contain repeated values. Return its smallest element, and explain in a comment what happens when the middle equals the right endpoint and how that affects the worst-case cost.

**Constraints.** 1 <= nums.length <= 5000 and values within the `int` range, nondecreasing before the rotation. Count the steps taken on an array of equal values with one smaller value hidden.

**Example 1.** Input `nums = [2, 2, 2, 0, 1, 2]`, output 0.

**Example 2.** Input `nums = [1, 1, 1]`, output 1.

**Hint.** Is it safe to drop the right endpoint when it equals the middle? How many elements can the equality case remove in the worst case?

**Changed decision.** Equality now occurs, so the search keeps its invariant by shrinking one element at a time and may lose logarithmic time.
