<!-- lesson-kind: standard -->
<!-- lesson-id: histogram-rectangles -->
## Find The Largest Rectangle

<!-- stage: context -->
### A Banner That Fits Under The Bars

A layout tool draws a bar chart with one bar per day, and every bar has a height in pixels. A designer wants to place the largest rectangular banner that fits completely inside the filled area of the bars. The banner sits on the baseline, and it can span several neighboring bars. Its height cannot pass the shortest bar that it covers.

For the heights 6, 2, 5, 4, 5, 1, 6, the best banner covers the three bars 5, 4, 5 at height 4, which gives an area of 12. The lesson answers one question. How can one left-to-right pass find that area for a chart with 100000 bars?

<!-- stage: naive -->
### Try Every Pair Of End Bars

The direct approach picks a first bar `l` and a last bar `r`. The banner over those bars has a height equal to the shortest bar between them, so the method keeps a running minimum while `r` moves right.

```java
static long largestByPairs(int[] heights) {
    long best = 0;
    for (int l = 0; l < heights.length; l++) {
        int lowest = Integer.MAX_VALUE;
        for (int r = l; r < heights.length; r++) {
            lowest = Math.min(lowest, heights[r]);
            best = Math.max(best, (long) lowest * (r - l + 1));
        }
    }
    return best;
}
```

The method is correct. Each pair gives the tallest banner that spans exactly those bars. On the heights 6, 2, 5, 4, 5, 1, 6, the pair from index 2 to index 4 gives 4 x 3 = 12.

<!-- stage: bottleneck -->
### Most Pairs Cannot Win

```predict
A chart has 100000 bars. How many pairs of end bars does the method try?

About 5 x 10^9. A chart of n bars has n x (n + 1) / 2 pairs, and 100000 x 100001 / 2 is about 5 x 10^9.
```

The method takes O(n^2) time for `n` bars, and a chart with a hundred thousand bars takes seconds and grows fourfold when the chart doubles. Almost all of those pairs are wasted. In the heights 6, 2, 5, 4, 5, 1, 6, the pair from index 2 to index 3 has height 4. The pair from index 2 to index 4 has the same height 4 and a larger width, so the first pair can never be the best.

For each height, only the widest banner can matter. The widest banner at the height of bar `i` stretches until the first shorter bar on each side. The previous lessons found nearest smaller values on both sides, so the width is ready to compute.

<!-- stage: insight -->
### Find Widths When A Shorter Bar Arrives

A stack of bars that never decrease in height holds exactly the bars whose right side is still open. The first shorter bar closes them.

<!-- names: popped bar, sentinel bar, flush -->

#### The Popped Bar Has Both Boundaries

A **popped bar** is a bar that leaves the stack because the current bar is shorter. The current index is the first shorter bar on its right, so it is the right boundary. The stack never decreases in height, so the new top below the popped bar is not taller than the popped bar. For a stack that holds one index per bar, the new top is the left boundary. The banner at the popped bar's height then spans every bar strictly between the two boundaries. Its width is `i - top - 1`, or `i` when the stack is empty after the pop.

Equal heights need no special rule here. The question asks for a maximum, not a count. A bar that pops with a too-small width, because an equal bar sits below it, is followed by that equal bar, which pops next and computes the full width.

#### A Zero-Height Bar Flushes The Rest

After the last real bar, some bars are still on the stack, because no shorter bar followed them. A **sentinel bar** is an extra bar of height 0 placed after the end. It is shorter than every bar of positive height, so it pops all of them. The act of emptying the stack this way is a **flush**. Bars of height 0 stay on the stack, and they have area 0, so they cannot change the answer.

Skipping the flush is a common mistake. A chart with rising heights such as 1, 2, 3 never meets a shorter bar, so nothing pops, and the loop reports an area of 0.

#### Why One Pass Is Enough

Every bar is pushed once and popped at most once, and the width computation at the pop takes constant time. The maximum of all computed areas is the answer, because every bar's widest banner is computed exactly when the bar pops.

<!-- stage: variables -->
### What The Pass Tracks

The pass tracks six pieces of state.

- **heights** is the input array of non-negative bar heights.
- **stack** holds bar indices, and the heights at these indices never decrease from bottom to top.
- **i** is the index of the current bar, and it equals `n` for the sentinel bar of height 0.
- **top** is the index of the popped bar, and `heights[top]` is the banner height.
- **width** equals `i - stack.peek() - 1` after the pop, or `i` when the stack is empty.
- **best** is the largest area computed so far.

The loop runs from `0` through `n`, so the sentinel is a virtual position that reads height 0.

<!-- stage: trace -->
### Following Pops And The Flush

#### A Chart That Pops In The Middle

The first trace reads 6, 2, 5, 4, 5, 1, 6. Each pop shows the banner height, the width and the area. The 2 pops the 6, whose width is 1. The 4 pops the first 5, and the second 5 then sits above the 4. The 1 pops the 5, the 4 and the 2. The 4 pops with the width 3, from index 2 to index 4, and this gives the area 12.

```trace
{"cells":[6,2,5,4,5,1,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[0]","best":0},"note":"Index 0 goes on the stack."},{"at":{"i":1},"vars":{"stack":"[]","height":6,"width":1,"area":6,"best":6},"note":"Height 2 is shorter than bar 0 of height 6. The width is 1, so the area is 6."},{"at":{"i":1},"vars":{"stack":"[1]","best":6},"note":"Index 1 goes on the stack."},{"at":{"i":2},"vars":{"stack":"[1, 2]","best":6},"note":"Index 2 goes on the stack."},{"at":{"i":3},"vars":{"stack":"[1]","height":5,"width":1,"area":5,"best":6},"note":"Height 4 is shorter than bar 2 of height 5. The width is 1, so the area is 5."},{"at":{"i":3},"vars":{"stack":"[1, 3]","best":6},"note":"Index 3 goes on the stack."},{"at":{"i":4},"vars":{"stack":"[1, 3, 4]","best":6},"note":"Index 4 goes on the stack."},{"at":{"i":5},"vars":{"stack":"[1, 3]","height":5,"width":1,"area":5,"best":6},"note":"Height 1 is shorter than bar 4 of height 5. The width is 1, so the area is 5."},{"at":{"i":5},"vars":{"stack":"[1]","height":4,"width":3,"area":12,"best":12},"note":"Height 1 is shorter than bar 3 of height 4. The width is 3, so the area is 12."},{"at":{"i":5},"vars":{"stack":"[]","height":2,"width":5,"area":10,"best":12},"note":"Height 1 is shorter than bar 1 of height 2. The width is 5, so the area is 10."},{"at":{"i":5},"vars":{"stack":"[5]","best":12},"note":"Index 5 goes on the stack."},{"at":{"i":6},"vars":{"stack":"[5, 6]","best":12},"note":"Index 6 goes on the stack."},{"at":{"i":7},"vars":{"stack":"[5]","height":6,"width":1,"area":6,"best":12},"note":"The sentinel of height 0 is shorter than bar 6 of height 6. The width is 1, so the area is 6."},{"at":{"i":7},"vars":{"stack":"[]","height":1,"width":7,"area":7,"best":12},"note":"The sentinel of height 0 is shorter than bar 5 of height 1. The width is 7, so the area is 7."},{"at":{"i":7},"vars":{"stack":"[7]","best":12},"note":"The scan ends with the sentinel on the stack."}]}
```

#### A Chart That Only Flushes

The second trace reads 2, 3, 5, 6. No bar is shorter than the one before it, so nothing pops until the sentinel arrives at index 4. The sentinel pops the 6, the 5, the 3 and the 2 in order. The widths grow from 1 to 4 as the stack empties, and the best area comes from the 5 and the 6 at height 5.

```trace
{"cells":[2,3,5,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[0]","best":0},"note":"Index 0 goes on the stack."},{"at":{"i":1},"vars":{"stack":"[0, 1]","best":0},"note":"Index 1 goes on the stack."},{"at":{"i":2},"vars":{"stack":"[0, 1, 2]","best":0},"note":"Index 2 goes on the stack."},{"at":{"i":3},"vars":{"stack":"[0, 1, 2, 3]","best":0},"note":"Index 3 goes on the stack."},{"at":{"i":4},"vars":{"stack":"[0, 1, 2]","height":6,"width":1,"area":6,"best":6},"note":"The sentinel of height 0 is shorter than bar 3 of height 6. The width is 1, so the area is 6."},{"at":{"i":4},"vars":{"stack":"[0, 1]","height":5,"width":2,"area":10,"best":10},"note":"The sentinel of height 0 is shorter than bar 2 of height 5. The width is 2, so the area is 10."},{"at":{"i":4},"vars":{"stack":"[0]","height":3,"width":3,"area":9,"best":10},"note":"The sentinel of height 0 is shorter than bar 1 of height 3. The width is 3, so the area is 9."},{"at":{"i":4},"vars":{"stack":"[]","height":2,"width":4,"area":8,"best":10},"note":"The sentinel of height 0 is shorter than bar 0 of height 2. The width is 4, so the area is 8."},{"at":{"i":4},"vars":{"stack":"[4]","best":10},"note":"The scan ends with the sentinel on the stack."}]}
```

<!-- stage: code -->
### The Stack Loop With A Sentinel

#### The Loop To N Inclusive

The loop runs `i` through `n` and reads height 0 at position `n`. This avoids copying the array. The area is computed in `long`, because a height near 10^9 times a width near 10^5 passes the range of `int`.

```java
static long largestRectangle(int[] heights) {
    int n = heights.length;
    long best = 0;
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i <= n; i++) {
        int current = i == n ? 0 : heights[i];
        while (!stack.isEmpty() && heights[stack.peek()] > current) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            best = Math.max(best, (long) height * width);
        }
        stack.push(i);
    }
    return best;
}
```

The final `push(i)` also pushes the sentinel index `n`. The method never reads `heights[n]`, because the stack is not read again after the loop ends, and `current` replaces the missing bar.

#### A Copy With A Real Sentinel

An alternative copies the heights into an array of length `n + 1` whose last entry is 0, and loops over that array. The loop body stays the same without the `current` check. The copy costs O(n) extra space, and the version above costs no more than the stack itself.

Both versions run in O(n) time, because each index enters the stack once and leaves at most once. They use O(n) extra space for the stack.

<!-- stage: applicability -->
### When Both Boundaries Are Needed

#### The Cue For A Rectangle

The cue is a region whose size is limited by the shortest element inside it, and the answer needs the widest region for each limiting element. The invariant is that the stack holds bars whose right boundary is still open, with heights that never decrease from bottom to top. A pop supplies the right boundary, and the bar below supplies the left boundary.

#### Two False Friends

Using only one side is the first false friend. The distance to the next shorter bar gives how far a banner reaches to the right, and it says nothing about how far it reaches to the left. On the heights 6, 2, 5, 4, 5, 1, 6, the best banner of height 4 needs the 5 on its left, and the right side alone reports a width of 2.

Skipping the flush is the second false friend. The loop without the sentinel passes every chart whose last bar is the shortest. It fails on rising charts, where the best banner is still waiting on the stack when the input ends.

#### When It Does Not Apply

A rectangle in a two-dimensional grid of cells needs one histogram per row, and that problem is built from this lesson. A banner that may have a gap, or may skip bars, is a different problem, because the shortest bar no longer limits the width.

<!-- stage: exercises -->
### Exercises

#### [Build] Rectangle From Supplied Boundaries (Author exercise)
<!-- id: ms-rectangle-from-boundaries -->

**Prerequisites.** The popped bar's two boundaries in this lesson.

**Problem.** A bar chart has heights `heights` of length `n`. Arrays `left` and `right` are given. For each index `i`, `left[i]` is the nearest index before `i` with a strictly smaller height, or `-1`, and `right[i]` is the nearest index after `i` with a strictly smaller height, or `n`. Return the maximum of `heights[i] * (right[i] - left[i] - 1)` over all indices.

**Constraints.** The limits are:
- **Length** is `1 <= n <= 10^5`.
- **Heights** are integers with `0 <= heights[i] <= 10^9`.
- **Boundaries** are correct for `heights`, with the sentinels `-1` and `n`.
- **Return** is a `long`.

**Example 1.** Input `heights = [3,1,3,2,2]`, `left = [-1,-1,1,1,1]`, `right = [1,5,3,5,5]`, output `6`.

**Example 2.** Input `heights = [2,5,6,3,0,4,4]`, `left = [-1,0,1,0,-1,4,4]`, `right = [4,3,3,4,7,7,7]`, output `10`.

**Hint.** The distance between the two boundaries, minus one, is the number of bars in the widest banner at that height.

**Changed decision.** The boundaries are given, so the only work is the width formula and a maximum.

#### [Vary] Resolve On A Shorter Bar (Author exercise)
<!-- id: ms-resolve-on-shorter-bar -->

**Prerequisites.** The exercise above and the pop rule in this lesson.

**Problem.** A bar chart `heights` has non-negative heights, and its last entry is `0`. Scan from left to right with a stack of indices. When the current bar is shorter than the top, pop the top, compute the banner height times the width between its two boundaries, and keep the maximum. Return the largest area.

**Constraints.** The limits are:
- **Length** is `1 <= heights.length <= 10^5`.
- **Heights** are integers with `0 <= heights[i] <= 10^9`, and the last entry is always `0`.
- **Flush** is not needed in the code, because the final `0` pops every positive bar.
- **Return** is a `long`.

**Example 1.** Input `[3,1,3,2,2,0]`, output `6`.

**Example 2.** Input `[2,5,6,3,0]`, output `10`.

**Hint.** Compute the width from the new top after each pop. What does an empty stack mean for the left side?

**Changed decision.** The boundaries are not supplied. Each pop produces them, so the scan resolves on a shorter bar.

#### [Boundary] Flush Increasing Heights (Author exercise)
<!-- id: ms-flush-increasing-heights -->

**Prerequisites.** The two exercises above.

**Problem.** A bar chart `heights` has non-negative heights and no trailing zero. Return the area of the largest rectangle under the bars. The chart can be non-decreasing, so the input can end before any bar is popped.

**Constraints.** The limits are:
- **Length** is `1 <= heights.length <= 10^5`.
- **Heights** are integers with `0 <= heights[i] <= 10^9`, and the last entry can be any value.
- **Flush** must remove every bar left on the stack at the end of the input.
- **Return** is a `long`.

**Example 1.** Input `[1,2,3,4,5]`, output `9`.

**Example 2.** Input `[2,2,2]`, output `6`.

**Hint.** Which bars are still on the stack when the input ends? Which position plays the role of the shorter bar for them?

**Changed decision.** The input has no trailing zero, so the loop reads a virtual height of 0 after the last bar.

#### [Recognize] Largest Rectangle in Histogram (LeetCode 84)
<!-- id: ms-largest-rectangle-histogram -->

**Prerequisites.** The three exercises above.

**Problem.** Given an array of integers `heights` that represents the heights of bars in a histogram, where each bar has width 1, return the area of the largest rectangle in the histogram.

**Constraints.** The limits are:
- **Length** is `1 <= heights.length <= 10^5`.
- **Heights** are integers with `0 <= heights[i] <= 10^4`.
- **Width** of every bar is 1.
- **Return** is an `int`, because the area is at most `10^9`.

**Example 1.** Input `[6,2,5,4,5,1,6]`, output `12`.

**Example 2.** Input `[3,3,1,3,3,3]`, output `9`.

**Hint.** The best rectangle has the height of one of the bars. Which bars decide its left and right edges?

**Changed decision.** The chart can start or end with its tallest bar, so both the empty stack and the flush occur.
