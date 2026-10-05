<!-- lesson-kind: standard -->
<!-- lesson-id: peak-search -->
## Find A Peak By Slope

<!-- stage: context -->
### Finding The Best Thread Count

A load test measures throughput for each thread count from 1 to 10,000. Throughput grows as threads are added, reaches a maximum, and then falls because the threads fight over locks. Each measurement takes a minute. Measuring every thread count takes almost a week. The engineer needs the thread count with the highest throughput.

The measurements are not sorted, and no target value is known in advance. This lesson answers one question. When values rise and then fall, how can two neighboring measurements show which side of a position holds the maximum?

<!-- stage: naive -->
### Measuring Every Count

The direct method reads every value, remembers the largest one, and returns its index.

```java
static int indexOfMaximum(int[] nums) {
    int best = 0;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] > nums[best]) best = i;
    }
    return best;
}
```

For `[1, 3, 6, 9, 7, 4, 2]` the method returns index 3. It works on any array, sorted or not, and it needs no assumption about the shape of the values.

```predict
The array has 10,000 values that rise and then fall. How many values does `indexOfMaximum` read, and what does the shape of the data let a smarter method skip?

It reads all 10,000 values, which is O(n). The shape says that a rise continues toward the maximum, so one comparison of two neighbors rules out a whole side.
```

<!-- stage: bottleneck -->
### Every Read Looks At One Value Alone

The loop costs `n` reads, which is O(n), because it compares each value with the best one so far and nothing else. It learns nothing about positions that it has not read.

Two neighboring values carry more information. Suppose the value at index 4 is smaller than the value at index 5. The data is rising there. Moving right keeps climbing until the climb stops, and the climb must stop at or before the end of the array. A maximum therefore exists to the right. If the value at index 4 is larger than the value at index 5, the data is falling there. The stop of the climb then lies at index 4 or to its left. One comparison of neighbors picks the side.

<!-- stage: insight -->
### Follow The Slope Uphill

The **slope** at index `mid` is the comparison of `nums[mid]` with `nums[mid + 1]`. A **peak** is an index whose value is greater than the values of its neighbors. An end index needs to beat only the one neighbor that it has. The search moves in the direction in which the slope rises.

<!-- names: slope, peak, mountain array -->

#### The Search Rule

A **mountain array** strictly rises to one top and then strictly falls. The same rule also finds a peak in an array with several peaks, if neighboring values always differ. At `mid`, compare `nums[mid]` with `nums[mid + 1]`. If the first is smaller, the data rises and a peak lies in `mid + 1` to `hi`. The rule then sets `lo = mid + 1`. If the first is larger, a peak lies in `lo` to `mid`, and the rule sets `hi = mid`.

#### Why The Rule Keeps A Peak

Take the rising case. Walk right from `mid + 1` while values keep rising. The walk ends at an index that is larger than its right neighbor, or at the last index. Either way that index is a peak, and it lies inside `[mid + 1, hi]`. The falling case is the mirror image: `mid` is larger than its right neighbor, and walking left from `mid` ends at a peak inside `[lo, mid]`.

#### The Interval And Its Exit

This search uses the closed interval `[lo, hi]` with `hi = nums.length - 1` and the loop test `lo < hi`. Unlike the closed search of the first lesson, this loop stops when one index remains, so `hi = mid` is safe. Because `mid < hi`, the index `mid + 1` is always inside the array. Equality never occurs for neighbors that differ, so the rule needs no tie case.

<!-- stage: variables -->
### One Interval And One Comparison

The state has three names, and a single comparison drives the loop.

- **lo** is the first index that can still hold a peak.
- **hi** is the last index that can still hold a peak.
- **mid** is `lo + (hi - lo) / 2`, and it is always smaller than `hi` while `lo < hi`.

The comparison `nums[mid] < nums[mid + 1]` is the only read of the data. When the loop ends, `lo == hi` names a peak. A single-value array skips the loop and returns index 0.

<!-- stage: trace -->
### Two Searches That Follow The Slope

#### A Mountain With One Top

The array is `[1, 3, 6, 9, 7, 4, 2]`. The first midpoint is index 3, and its value 9 is larger than the next value 7, so the data falls and `hi` becomes 3. The midpoint at index 1 has value 3, smaller than 6, so `lo` becomes 2. The midpoint at index 2 has value 6, smaller than 9, so `lo` becomes 3. The interval holds only index 3, and the peak value is 9.

```trace
{"cells":[1,3,6,9,7,4,2],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":-1},"vars":{},"note":"Start with the whole array, indexes 0 to 6. A peak exists inside it."},{"at":{"lo":0,"hi":6,"mid":3},"vars":{"nums[mid]":"9","nums[mid+1]":"7"},"note":"The value 9 is larger than 7, so the data falls. A peak lies at mid or left of it, and hi becomes 3."},{"at":{"lo":0,"hi":3,"mid":1},"vars":{"nums[mid]":"3","nums[mid+1]":"6"},"note":"The value 3 is smaller than 6, so the data rises. A peak lies right of mid, and lo becomes 2."},{"at":{"lo":2,"hi":3,"mid":2},"vars":{"nums[mid]":"6","nums[mid+1]":"9"},"note":"The value 6 is smaller than 9, so the data rises. A peak lies right of mid, and lo becomes 3."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"peak value":"9"},"note":"One index remains. Index 3 is a peak with value 9."}]}
```

#### An Array With Two Peaks

The array is `[1, 5, 2, 4, 6, 3, 0]`, with peaks at index 1 and index 4. The first midpoint is index 3 with value 4, smaller than 6, so `lo` becomes 4. The midpoint at index 5 has value 3, larger than 0, so `hi` becomes 5. The midpoint at index 4 has value 6, larger than 3, so `hi` becomes 4. The search ends at index 4. It never visits the other peak, which the contract allows.

```trace
{"cells":[1,5,2,4,6,3,0],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":-1},"vars":{},"note":"Start with the whole array, indexes 0 to 6. A peak exists inside it."},{"at":{"lo":0,"hi":6,"mid":3},"vars":{"nums[mid]":"4","nums[mid+1]":"6"},"note":"The value 4 is smaller than 6, so the data rises. A peak lies right of mid, and lo becomes 4."},{"at":{"lo":4,"hi":6,"mid":5},"vars":{"nums[mid]":"3","nums[mid+1]":"0"},"note":"The value 3 is larger than 0, so the data falls. A peak lies at mid or left of it, and hi becomes 5."},{"at":{"lo":4,"hi":5,"mid":4},"vars":{"nums[mid]":"6","nums[mid+1]":"3"},"note":"The value 6 is larger than 3, so the data falls. A peak lies at mid or left of it, and hi becomes 4."},{"at":{"lo":4,"hi":4,"mid":-1},"vars":{"peak value":"6"},"note":"One index remains. Index 4 is a peak with value 6."}]}
```

<!-- stage: code -->
### The Slope Loop In Java

```java
static int findPeak(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < nums[mid + 1]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

Each step either moves `lo` past `mid` or sets `hi = mid` with `mid < hi`, so the interval shrinks and the loop ends. The method reads two values per step, so a search over `n` values reads at most `2 * (floor(log2(n)) + 1)` values. A single value returns index 0, and the array must not be empty.

<!-- stage: applicability -->
### When The Slope Decides

#### The Invariant

The invariant is that a peak exists inside `[lo, hi]`. It holds at the start, because the whole array contains a peak, and an array without ties always has one. A rising step keeps the right side, and a falling step keeps the left side, and the argument above shows each side contains a peak. The last remaining index is therefore a peak.

#### The False Friend

Searching for a target value is the false friend. Target search compares a middle value with a number given in advance, and equality means success. Here equality has no role, and the comparison looks at a neighbor. A peak search also does not return the unique maximum unless the shape is a single mountain. In the array with two peaks, the search may return the smaller peak.

#### What Breaks The Rule

Equal neighbors break it. The array `[1, 2, 2, 2, 1]` has no strict peak, so the invariant is false from the start. The search returns index 1, whose right neighbor is equal. The contract must therefore say that adjacent values differ. A flat region also needs a different approach, which the rotation lessons discuss for a similar tie.

<!-- stage: exercises -->
### Exercises

#### [Build] Peak Index In A Mountain Array (LeetCode 852)
<!-- id: bs-mountain-852 -->

**Prerequisites.** The slope rule and the interval `[lo, hi]` of this lesson.

**Problem.** An array `arr` is a mountain array when it has at least three values, strictly increases up to one index, and then strictly decreases. Given a mountain array, return the index of its largest value.

**Constraints.** The limits are:
- **Length** is `3 <= arr.length <= 10^5`.
- **Shape** is strictly increasing and then strictly decreasing, with the top neither first nor last.
- **Values** are `int` values.
- **Mutation** does not occur; `arr` does not change.

**Example 1.** Input `arr = [1,3,6,9,7,4,2]`, output 3.

**Example 2.** Input `arr = [2,10,30,40,5]`, output 3.

**Hint.** If `arr[mid] < arr[mid + 1]`, can the top lie at or before `mid`?

**Changed decision.** Basic case: the neighbor comparison replaces a target comparison.

#### [Vary] Find Peak Element (LeetCode 162)
<!-- id: bs-peak-162 -->

**Prerequisites.** The first exercise above.

**Problem.** Given an array `nums` in which adjacent values always differ, return the index of any peak. An index is a peak when its value is strictly larger than each neighbor that exists. The first index has only a right neighbor, and the last index has only a left neighbor.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 1000`.
- **Values** are `int` values, and `nums[i] != nums[i + 1]` for every valid `i`.
- **Answer** is the index of any one peak.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [1,5,2,4,6,3,0]`, output 1 or 4.

**Example 2.** Input `nums = [7]`, output 0.

**Hint.** The argument that a peak exists on the rising side does not need a single top. What does it need at the array ends?

**Changed decision.** The shape guarantee shrinks from one mountain to "neighbors differ", and any peak is accepted.

#### [Boundary] Endpoint Peak (Author exercise)
<!-- id: bs-endpoint-peak -->

**Prerequisites.** Both exercises above.

**Problem.** Given an array `nums` in which adjacent values differ, return the index of a peak under the end rule of the previous exercise. A strictly increasing array has its only peak at the last index. A strictly decreasing array has its only peak at index 0.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 1000`.
- **Values** are `int` values with `nums[i] != nums[i + 1]`.
- **Shape** may be strictly increasing, strictly decreasing, or any other pattern.
- **Answer** is the index of one peak.

**Example 1.** Input `nums = [1,2,3,4]`, output 3.

**Example 2.** Input `nums = [4,3,2,1]`, output 0.

**Hint.** Trace `[1,2,3,4]` and write down which bound moves at every step. Where does `lo` stop?

**Changed decision.** The peak sits at an end, so the search must reach an end index without reading outside the array.

#### [Recognize] Find In Mountain Array (LeetCode 1095)
<!-- id: bs-find-in-mountain -->

**Prerequisites.** All exercises above and the descending search of the first lesson.

**Problem.** A mountain array `m` is hidden behind two calls: `m.length()` returns its length and `m.get(i)` returns the value at index `i`. A mountain array strictly increases and then strictly decreases. Given `m` and an integer `target`, return the smallest index with value `target`, or `-1` when it does not occur. The search may call `get` at most 100 times.

**Constraints.** The limits are:
- **Length** is `3 <= m.length() <= 10^4`.
- **Values** are distinct on each side of the top, but one value may occur on both sides.
- **Target** is any `int`.
- **Calls** to `get` number at most 100, and each call has a cost.

**Example 1.** Input values `[1,5,9,12,10,7,2]` and `target = 7`, output 5.

**Example 2.** Input values `[1,5,9,12,10,7,2]` and `target = 4`, output -1.

**Hint.** Find the top first. Which search runs on the rising part, which on the falling part, and which side is checked first for the smallest index?

**Changed decision.** The call budget is part of the contract, so peak search and two ordered searches must each stay logarithmic.
