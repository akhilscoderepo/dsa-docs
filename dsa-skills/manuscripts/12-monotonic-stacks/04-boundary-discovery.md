<!-- lesson-kind: standard -->
<!-- lesson-id: boundary-discovery -->
## Find Both Boundaries Of A Value

<!-- stage: context -->
### How Far Each Hour Stays Lowest

A traffic dashboard stores the request count of every hour in a day. For each hour, an analyst wants the longest stretch of consecutive hours that contains it and in which no hour has fewer requests. If the counts are 4, 2, 5, 5, 3, 6, the first 5 sits inside a stretch from hour 2 to hour 3. The 3 at hour 4 reaches from hour 2 to hour 5, because neither 5 nor the 6 has fewer requests than it.

Such a stretch ends on the left and on the right at the nearest hour with a smaller count. The lesson answers one question. How does one stack find that nearest smaller hour on both sides for every hour?

<!-- stage: naive -->
### Expand Outward From Every Hour

The direct approach starts at hour `i` and moves left until it meets a count smaller than `counts[i]`. It then moves right in the same way. The stretch length is the number of hours strictly between the two stopping hours.

```java
static int[] stretchByExpanding(int[] counts) {
    int n = counts.length;
    int[] stretch = new int[n];
    for (int i = 0; i < n; i++) {
        int left = i - 1;
        while (left >= 0 && counts[left] >= counts[i]) left--;
        int right = i + 1;
        while (right < n && counts[right] >= counts[i]) right++;
        stretch[i] = right - left - 1;
    }
    return stretch;
}
```

The method is correct. For the counts 4, 2, 5, 5, 3, 6, the 3 expands left over the 5 and the 5, stops at the 2, and expands right over the 6 to the end.

<!-- stage: bottleneck -->
### Every Expansion Starts From Zero

```predict
The counts rise every hour, as in 1, 2, 3 and so on up to 100000. About how many hours do the right-hand expansions read in total?

About 5 x 10^9. The expansion from hour i meets no smaller count, so it reads all the hours after i. The sum over all hours is about 100000 x 99999 / 2.
```

The worst case is O(n^2) for `n` hours. A rising array makes every right expansion run to the end, and a falling array does the same on the left. The expansions repeat each other. The expansion from hour 3 crosses hours that the expansion from hour 2 already crossed, and it checks the same counts again.

The previous lessons let a stack skip the repeated reads on one side. Each hour here needs both sides, so the program must decide which stack step produces which side.

<!-- stage: insight -->
### One Pass Gives One Side Per Step

A stack of hours with increasing counts exposes the nearest smaller hour at exactly the moment an hour enters or leaves.

<!-- names: previous smaller index, next smaller index, boundary sentinel -->

#### The Left Side Is The Surviving Top

The **previous smaller index** of `i` is the largest `j < i` with `nums[j] < nums[i]`. Scan from left to right and keep a stack whose values strictly increase from bottom to top. A new value pops every top that is greater than or equal to it. No popped top can be the boundary of any later value, because the new index is nearer and its value is at most the popped value. The pops stop at a top with a smaller value, and that top is the previous smaller index.

Equal values must pop. An earlier equal value is not smaller, so it cannot be a boundary, and leaving it on the stack would return it as one.

#### The Right Side Appears At A Pop

The **next smaller index** of `i` is the smallest `j > i` with `nums[j] < nums[i]`. Scan from left to right and keep a stack whose values never decrease from bottom to top. A new value pops every top that is strictly greater than it. For each popped top, the new index is the first smaller value after it, so it is that top's next smaller index.

Here equal values must stay. An equal later value is not smaller, so it does not resolve the top. This lesson uses a strictly smaller boundary on both sides. The next lesson changes the rule on one side.

#### A Missing Side Needs A Sentinel

Some values have no smaller neighbor. A **boundary sentinel** marks that case with an index outside the array. The previous smaller index uses `-1`, and the next smaller index uses `n`. With these two values, the stretch around index `i` is the open interval from `left[i]` to `right[i]`, and its width is `right[i] - left[i] - 1`. The formula needs no special case, because a sentinel sits exactly one slot beyond each end of the array.

<!-- stage: variables -->
### What Each Scan Keeps

The two scans track six pieces of state.

- **nums** is the input array, and neither scan changes it.
- **left** holds the previous smaller index of every position, and the sentinel `-1` marks none.
- **right** holds the next smaller index of every position, and the sentinel `n` marks none.
- **stack** holds indices, and its values increase from bottom to top as described for each side.
- **i** is the index that the scan reads, and its value decides the pops.
- **width** is `right[i] - left[i] - 1`, the count of positions strictly between the two boundaries.

The left scan reads `left[i]` from the surviving top. The right scan writes `right[top]` at each pop and writes `n` for the indices that remain.

<!-- stage: trace -->
### Following Both Scans

#### The Left Scan

The first trace reads 4, 2, 5, 5, 3, 6 and fills `left`. The stack lists indices. The second 5 meets an equal 5 on top and pops it. The 3 pops the 5 and stops at the 2, so its previous smaller index is 1. The 6 stops immediately at the 3.

```trace
{"cells":[4,2,5,5,3,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[0]","left":"[-1, ., ., ., ., .]"},"note":"The surviving top gives left[0] = -1, and index 0 goes on the stack."},{"at":{"i":1},"vars":{"stack":"[]","left":"[-1, ., ., ., ., .]"},"note":"nums[0] = 4 is at least 2, so index 0 leaves the stack."},{"at":{"i":1},"vars":{"stack":"[1]","left":"[-1, -1, ., ., ., .]"},"note":"The surviving top gives left[1] = -1, and index 1 goes on the stack."},{"at":{"i":2},"vars":{"stack":"[1, 2]","left":"[-1, -1, 1, ., ., .]"},"note":"The surviving top gives left[2] = 1, and index 2 goes on the stack."},{"at":{"i":3},"vars":{"stack":"[1]","left":"[-1, -1, 1, ., ., .]"},"note":"nums[2] = 5 is at least 5, so index 2 leaves the stack."},{"at":{"i":3},"vars":{"stack":"[1, 3]","left":"[-1, -1, 1, 1, ., .]"},"note":"The surviving top gives left[3] = 1, and index 3 goes on the stack."},{"at":{"i":4},"vars":{"stack":"[1]","left":"[-1, -1, 1, 1, ., .]"},"note":"nums[3] = 5 is at least 3, so index 3 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[1, 4]","left":"[-1, -1, 1, 1, 1, .]"},"note":"The surviving top gives left[4] = 1, and index 4 goes on the stack."},{"at":{"i":5},"vars":{"stack":"[1, 4, 5]","left":"[-1, -1, 1, 1, 1, 4]"},"note":"The surviving top gives left[5] = 4, and index 5 goes on the stack."}]}
```

#### The Right Scan

The second trace reads the same array and fills `right`. The stack lists indices, and `.` means no answer yet. The 2 resolves the 4 at index 0. The second 5 leaves the first 5 on the stack, because equality does not resolve it. The 3 then pops both 5 days. The indices 1, 4 and 5 remain at the end, and each receives the sentinel 6.

```trace
{"cells":[4,2,5,5,3,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[0]","right":"[., ., ., ., ., .]"},"note":"Index 0 with value 4 goes on the stack."},{"at":{"i":1},"vars":{"stack":"[]","right":"[1, ., ., ., ., .]"},"note":"2 is smaller than nums[0] = 4, so right[0] = 1 and index 0 leaves the stack."},{"at":{"i":1},"vars":{"stack":"[1]","right":"[1, ., ., ., ., .]"},"note":"Index 1 with value 2 goes on the stack."},{"at":{"i":2},"vars":{"stack":"[1, 2]","right":"[1, ., ., ., ., .]"},"note":"Index 2 with value 5 goes on the stack."},{"at":{"i":3},"vars":{"stack":"[1, 2, 3]","right":"[1, ., ., ., ., .]"},"note":"Index 3 with value 5 goes on the stack."},{"at":{"i":4},"vars":{"stack":"[1, 2]","right":"[1, ., ., 4, ., .]"},"note":"3 is smaller than nums[3] = 5, so right[3] = 4 and index 3 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[1]","right":"[1, ., 4, 4, ., .]"},"note":"3 is smaller than nums[2] = 5, so right[2] = 4 and index 2 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[1, 4]","right":"[1, ., 4, 4, ., .]"},"note":"Index 4 with value 3 goes on the stack."},{"at":{"i":5},"vars":{"stack":"[1, 4, 5]","right":"[1, ., 4, 4, ., .]"},"note":"Index 5 with value 6 goes on the stack."},{"at":{"i":6},"vars":{"stack":"[1, 4, 5]","right":"[1, 6, 4, 4, 6, 6]"},"note":"The scan ends, and the indices [1, 4, 5] receive the sentinel 6."}]}
```

<!-- stage: code -->
### Two Scans And A Width

#### The Left Boundary From The Surviving Top

The method pops with `>=`, then reads the top. An empty stack yields the sentinel `-1`.

```java
static int[] previousSmaller(int[] nums) {
    int[] left = new int[nums.length];
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < nums.length; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) stack.pop();
        left[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(i);
    }
    return left;
}
```

#### The Right Boundary At The Pop

The method pops with `>` and writes the answer for the popped index. It fills every entry with the sentinel `n` first, so the indices left on the stack need no extra loop.

```java
static int[] nextSmaller(int[] nums) {
    int n = nums.length;
    int[] right = new int[n];
    Arrays.fill(right, n);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] > nums[i]) right[stack.pop()] = i;
        stack.push(i);
    }
    return right;
}
```

The two comparisons look different, `>=` and `>`, but both exclude equal values from the boundary. Each scan runs in O(n) time, because it pushes each index once and pops it at most once. The width `right[i] - left[i] - 1` costs O(1) per index. The arrays and stack use O(n) extra space.

<!-- stage: applicability -->
### When A Value Needs Both Sides

#### The Cue For Two Boundaries

The cue is a question about the region around each element, such as the widest stretch where it stays the minimum. The invariant is that every stack entry still waits for a smaller value on one side, and the values on the stack are ordered so the nearest smaller one is always at the top. One scan supplies one side per pop or per push, and two scans supply both.

#### Two False Friends

Storing only the boundary values is the first false friend. For the counts 4, 2, 5, 5, 3, 6, the boundary value of the 3 is 2 on the left. The width needs the position of that 2, and equal values make the value ambiguous.

The next greater scan is the second false friend. It answers the same shape of question for larger values. Reusing its `<` comparison for smaller boundaries pops the wrong tops, because the order on the stack is reversed.

#### When It Does Not Apply

A boundary defined by a condition other than a comparison with the element itself, such as the first value that differs by more than `k`, needs different state. The stack order that exposes the nearest smaller value says nothing about such a condition.

<!-- stage: exercises -->
### Exercises

#### [Build] Previous Smaller Index (Author exercise)
<!-- id: ms-previous-smaller-index -->

**Prerequisites.** The left scan in this lesson.

**Problem.** Consider an integer array `nums`. For each index `i`, return the largest index `j < i` with `nums[j] < nums[i]`, or `-1` when no such index exists.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values, and equal values are allowed.
- **Ties** are not smaller, so an equal earlier value is never returned.
- **Return** is an `int[]` of the same length.

**Example 1.** Input `[5,2,6,3,4,1]`, output `[-1,-1,1,1,3,-1]`.

**Example 2.** Input `[4,4,4]`, output `[-1,-1,-1]`.

**Hint.** Keep the stack values strictly increasing. Which tops must leave when the new value is equal to the top?

**Changed decision.** The answer is the surviving top after the pops, and nothing is written at a pop.

#### [Vary] Next Smaller Index (Author exercise)
<!-- id: ms-next-smaller-index -->

**Prerequisites.** The exercise above and the right scan in this lesson.

**Problem.** Take an integer array `nums`. For each index `i`, return the smallest index `j > i` with `nums[j] < nums[i]`, or `-1` when no such index exists.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values, and equal values are allowed.
- **Ties** are not smaller, so an equal later value never resolves an index.
- **Return** is an `int[]` of the same length, with `-1` as the no-answer marker.

**Example 1.** Input `[5,2,6,3,4,1]`, output `[1,5,3,5,5,-1]`.

**Example 2.** Input `[3,3,1,3]`, output `[2,2,-1,-1]`.

**Hint.** Write the answer when an index leaves the stack. Which comparison keeps equal values waiting?

**Changed decision.** The answer is written at the pop, and the comparison flips from the previous exercise.

#### [Boundary] No Boundary (Author exercise)
<!-- id: ms-no-boundary -->

**Prerequisites.** The two exercises above.

**Problem.** An integer array `nums` has length `n`. For each index `i`, return the pair `{left, right}`, where `left` is the previous smaller index or `-1`, and `right` is the next smaller index or `n`. Use the sentinels even when both sides are missing.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values, and equal values are allowed.
- **Sentinels** are `-1` on the left and `n` on the right, never `-1` on both sides.
- **Return** is an `int[][]` with one pair per index.

**Example 1.** Input `[1,2,3]`, output `[[-1,3],[0,3],[1,3]]`.

**Example 2.** Input `[3,3]`, output `[[-1,2],[-1,2]]`.

**Hint.** Fill the right array with `n` before the scan. Why does the left scan need no fill step?

**Changed decision.** A missing boundary becomes an index one step outside the array, so later formulas need no special case.

#### [Recognize] Widest Region Where Each Value Is Minimum (Author exercise)
<!-- id: ms-widest-minimum-region -->

**Prerequisites.** The three exercises above.

**Problem.** An integer array `nums` holds the values to scan. For each index `i`, let the region of `i` be the longest range of consecutive indices that contains `i` and in which every value is at least `nums[i]`. Return the length of the region of every index.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values, and equal values belong inside each other's regions.
- **Region** length is at least 1, because the range can hold only `i`.
- **Return** is an `int[]` of the same length.

**Example 1.** Input `[4,2,5,5,3,6]`, output `[1,6,2,2,4,1]`.

**Example 2.** Input `[3,1,2,2,5]`, output `[1,5,3,3,1]`.

**Hint.** The region ends at the nearest strictly smaller value on each side. How do the two boundary indices turn into a length?

**Changed decision.** The answer combines two boundary scans into one width per index.
