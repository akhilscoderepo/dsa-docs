<!-- lesson-kind: standard -->
<!-- lesson-id: peak-search -->
## Peak Search

<!-- stage: context -->
### A Hiker On A Dark Ridge

A hiker is on a long ridge trail at night, with a marker post every hundred meters and an altimeter that reads the height of whichever post she stands beside. The trail climbs, reaches a summit, and then descends. She wants to reach the summit, and her only tools are the altimeter and her legs. Each reading means walking to a post, so she would like to read as few as possible.

She notices that she does not need to know what the summit is to know which way to go. Standing at a post, she can read the height there and the height at the next post. If the next post is higher, the trail is still climbing, and the summit must lie ahead. If the next post is lower, the trail is already falling, and the summit is here or behind her. No target number is involved at all, only the direction in which the trail is tilting.

<!-- stage: naive -->
### Read Every Post And Keep The Highest

The plain plan is to visit every post and remember the highest reading.

```java
static int summitByWalking(int[] heights) {
    int best = 0;
    for (int i = 1; i < heights.length; i++) {
        if (heights[i] > heights[best]) best = i;
    }
    return best;
}
```

It returns the position of the highest post for any trail, and it works for a trail with several summits by returning the tallest one.

<!-- stage: bottleneck -->
### Every Post Gets Visited

The loop reads all n posts, so it is O(n), and that holds even for a trail that rises smoothly for thousands of posts before falling. A long ridge of a million posts means a million readings of a costly instrument. The loop also finds the tallest summit, which is more than the task asked for in the version where any summit will do.

The comparison between a post and its neighbor carries more information than the loop uses. If post `mid` is lower than post `mid + 1`, then everything from `mid + 1` onward is a place where a summit could still be, and there is no need to look behind. If post `mid` is higher than its neighbor, a summit exists at `mid` or before it. One reading of two adjacent posts therefore removes half of the trail, which leads to O(log n) readings.

<!-- stage: insight -->
### The Tilt Tells You Where To Go

The decision at each step depends on the **local slope** at the middle, which is the comparison of `nums[mid]` with `nums[mid + 1]`. This is a different question from the target searches of earlier lessons. Equality has no meaning here, and what counts is whether the sequence is going up or down at that point. The **uphill rule** is: when the next element is larger, a peak lies strictly to the right of `mid`, and when the next element is smaller, a peak lies at `mid` or to its left.

The interval is closed, `[lo, hi]`, and the loop runs while `lo < hi`, so `mid + 1` is always a valid index, because `mid < hi`. The invariant is that the interval contains at least one peak. When the next element is larger, set `lo = mid + 1`, and when it is smaller, set `hi = mid`. The loop ends with `lo == hi`, and that position is a peak. For a **mountain array**, which rises strictly to one summit and then falls strictly, the peak is unique and the invariant says that the interval holds that summit.

<!-- names: local slope, uphill rule, mountain array -->

The same loop proves something stronger for arrays that are not mountains. If neighbors are always different, and the elements just outside both ends are imagined to be smaller than everything, then a climbing step guarantees a peak ahead, because the sequence must eventually come down, at the latest at the imagined edge. A falling step guarantees a peak behind, because going backwards the sequence climbs, and it cannot climb forever. This is why endpoints can be peaks: a strictly increasing array has its peak at the last position, and a strictly decreasing array has it at the first.

Some problems combine peak search with the earlier kinds. To find a value in a mountain array, first locate the summit, then search the rising part with ordinary exact search, and if that fails, search the falling part with the reversed comparison. If reading an element costs something, the three searches each add their own logarithmic number of readings, and the total can be counted exactly.

<!-- stage: variables -->
### Edges, Middle And The Next Element

`lo` and `hi` are the first and last positions of the interval that must contain a peak. `mid` is always strictly less than `hi` inside the loop, so the next element exists and the comparison is legal. The comparison result has two outcomes, rising or falling, and equality does not occur for the arrays in this lesson because neighbors differ. After the loop, `lo` is the peak position. In the mountain-array lookup, the summit position is kept as a fixed boundary that splits the array into an ascending part and a descending part.

<!-- stage: trace -->
### Following The Tilt To A Summit

The first trace finds the summit of the mountain 1, 3, 6, 9, 12, 10, 7, 4, 2. The first reading compares position 4, which holds 12, with the next element 10. It is falling, so the summit is at 4 or earlier and the right edge moves to 4. The third step compares 9 with 12, finds the trail still rising, and moves the left edge to 4, where the edges meet.

```trace
{"cells":[1,3,6,9,12,10,7,4,2],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":8,"mid":4},"vars":{"here":12,"next":10,"slope":"falling"},"note":"Position 4 holds 12 and the next holds 10. The trail is falling, so a peak is here or earlier and hi becomes 4."},{"at":{"lo":0,"hi":4,"mid":2},"vars":{"here":6,"next":9,"slope":"rising"},"note":"Position 2 holds 6 and the next holds 9. The trail is rising, so a peak lies to the right and lo becomes 3."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"here":9,"next":12,"slope":"rising"},"note":"Position 3 holds 9 and the next holds 12. The trail is rising, so a peak lies to the right and lo becomes 4."},{"at":{"lo":4,"hi":4,"mid":-1},"vars":{"peak":4,"height":12},"note":"The edges meet at position 4, holding 12, which is a peak."}]}
```

The second trace uses an array that is not a mountain, 1, 5, 2, 6, 3, 4, which has three peaks. The search does not try to find the tallest. It compares 2 with 6, sees a rise, and moves right. Then it compares 3 with 4, sees another rise, and moves right again, ending at the last position. The peak it returns is the final element, which is a peak because the position beyond the end counts as lower than anything.

```trace
{"cells":[1,5,2,6,3,4],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":2},"vars":{"here":2,"next":6,"slope":"rising"},"note":"Position 2 holds 2 and the next holds 6. The trail is rising, so a peak lies to the right and lo becomes 3."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"here":3,"next":4,"slope":"rising"},"note":"Position 4 holds 3 and the next holds 4. The trail is rising, so a peak lies to the right and lo becomes 5."},{"at":{"lo":5,"hi":5,"mid":-1},"vars":{"peak":5,"height":4},"note":"The edges meet at position 5, holding 4, which is a peak."}]}
```

<!-- stage: code -->
### Summit Search And Mountain Lookup

```java
final class PeakTools {
    interface MountainArray { int get(int index); int length(); }

    static int findPeak(int[] a) {
        int lo = 0, hi = a.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] < a[mid + 1]) lo = mid + 1;     // still climbing
            else hi = mid;                             // falling: a peak is here or before
        }
        return lo;
    }

    static int findInMountain(MountainArray m, int target) {
        int n = m.length(), lo = 0, hi = n - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (m.get(mid) < m.get(mid + 1)) lo = mid + 1;
            else hi = mid;
        }
        int peak = lo;
        lo = 0; hi = peak;
        while (lo <= hi) {                             // rising part
            int mid = lo + (hi - lo) / 2, v = m.get(mid);
            if (v == target) return mid;
            if (v < target) lo = mid + 1; else hi = mid - 1;
        }
        lo = peak + 1; hi = n - 1;
        while (lo <= hi) {                             // falling part
            int mid = lo + (hi - lo) / 2, v = m.get(mid);
            if (v == target) return mid;
            if (v > target) lo = mid + 1; else hi = mid - 1;
        }
        return -1;
    }
}
```

The peak loop makes O(log n) comparisons and uses O(1) space. The mountain lookup runs three halving loops, so it makes O(log n) calls to `get` overall, with a constant of about four times the number of halvings, since the peak loop reads two elements per step. Searching the rising part first returns the smaller index when the target occurs on both sides.

<!-- stage: applicability -->
### When The Direction Is The Clue

Use peak search when the question asks for a local maximum or minimum and each comparison of neighbors tells which side must contain one. The invariant is the sentence about the interval: it contains at least one peak. Check the contract about the ends, and about whether neighbors can be equal, because the proof of each move depends on both.

A false friend is target search. Peak search compares an element with its neighbor, not with a goal, and equality is not an event. Another false friend is an array with plateaus, where equal neighbors make a comparison uninformative: the middle could sit on a flat stretch with a peak on either side or neither. Peak search needs the guarantee that adjacent elements differ, or it needs a policy for ties that is separately argued.

In Java, compare `nums[mid]` with `nums[mid + 1]` only when `mid < hi`, which the loop condition guarantees. Do not compare with `nums[mid - 1]` at position 0. When elements are fetched through an interface that charges per call, keep the number of calls in a variable of the test harness, and reuse values you have already fetched instead of calling twice.

<!-- stage: exercises -->
### Exercises

#### [Build] Peak Index in a Mountain Array (LeetCode 852)
<!-- id: bs-mountain-peak -->

**Prerequisites.** The first-true lesson, and comparison of neighboring elements.

**Problem.** An array rises strictly to a single summit and then falls strictly. Return the index of the summit, using the comparison of each middle element with the one after it.

**Constraints.** 3 <= arr.length <= 100000, the array is a mountain, and values lie between 0 and 1000000. Run in O(log n).

**Example 1.** Input `arr = [3, 6, 11, 8]`, output 2.

**Example 2.** Input `arr = [1, 2, 3, 4, 2, 1]`, output 3.

**Hint.** What does a rising step at `mid` say about the positions to its left? Why is `mid + 1` always a valid index in the loop?

**Changed decision.** First rung: the search compares neighbors, not a target, and the loop moves toward the rising side.

#### [Vary] Find Peak Element (LeetCode 162)
<!-- id: bs-find-peak-element -->

**Prerequisites.** The mountain exercise above.

**Problem.** An array has no two equal neighbors, and the positions outside both ends count as lower than every element. Return the index of any element that is larger than both of its neighbors. The array need not be a single mountain.

**Constraints.** 1 <= nums.length <= 1000 and any `int` values with `nums[i] != nums[i + 1]`. Any valid peak index is accepted. Run in O(log n).

**Example 1.** Input `nums = [1, 5, 2, 6, 3, 4]`, output 1, 3 or 5, since each is a peak.

**Example 2.** Input `nums = [9, 1]`, output 0.

**Hint.** If the trail is still climbing at `mid`, what must happen eventually to the right? What if it is falling?

**Changed decision.** The invariant weakens from "the summit" to "some peak", which is enough because only one is asked for.

#### [Boundary] Endpoint Peak (Author exercise)
<!-- id: bs-endpoint-peak -->

**Prerequisites.** The two exercises above.

**Problem.** Trace the peak search on a strictly increasing array and on a strictly decreasing array, and show that the peaks are the last and first positions. Test arrays of length 1 and 2.

**Constraints.** 1 <= nums.length <= 1000 and strictly monotone arrays, in both directions. Never read past either end of the array.

**Example 1.** Input `nums = [1, 2, 3, 4, 5]`, output 4.

**Example 2.** Input `nums = [5, 4, 3, 2, 1]`, output 0.

**Hint.** What does the outside of the array count as? Which comparison is made when the interval has two elements?

**Changed decision.** The data has no interior summit, so the answer sits at an end, and the imagined elements beyond the array justify it.

#### [Recognize] Find in Mountain Array (LeetCode 1095)
<!-- id: bs-find-in-mountain -->

**Prerequisites.** All three exercises above, and exact search from the first lesson.

**Problem.** Elements of a mountain array can only be read through a `get(index)` call, and the number of calls is limited. Return the smallest index holding the target, or minus one. Locate the summit first, then search the rising part, and then the falling part if needed.

**Constraints.** 3 <= length <= 10000, the array is a mountain of non-negative values, and at most 100 calls to `get` are allowed. The target occurs at most once on each side of the summit.

**Example 1.** Input `mountain = [1, 3, 6, 9, 12, 10, 7, 4, 2], target = 6`, output 2.

**Example 2.** Input `mountain = [1, 3, 6, 9, 12, 10, 7, 4, 2], target = 5`, output -1.

**Hint.** Which side do you search first so the smaller index wins? What changes in the comparison when you search the falling part?

**Changed decision.** The cost of a read is part of the contract, so the three searches are counted and the budget is checked.
