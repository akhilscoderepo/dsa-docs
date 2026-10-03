<!-- lesson-kind: standard -->
<!-- lesson-id: histogram-rectangles -->
## Histogram Rectangles

<!-- stage: context -->
### A Banner Against The Fence Posts

A carpenter has a row of fence posts, side by side, all one hand wide and cut to different heights. A sign painter wants to hang one rectangular banner that stands on the ground and leans against a run of neighbouring posts. The banner may be as wide as the run, but it can be no taller than the shortest post in the run, because a taller banner would stick out above that post. The painter is paid by the area of the banner, so the carpenter wants to know which run of posts allows the largest one.

There are many runs to consider, since any stretch of neighbouring posts will do. For a short post the run can be very wide but the banner is low, and for a tall post the banner could be high but the run is narrow. The carpenter would like to look at each post once and still be sure that the best banner has been found.

<!-- stage: naive -->
### Try Every Run Of Posts

The direct method tries every run, fixing the left end and growing the right end while tracking the shortest post seen so far, since that post limits the banner.

```java
static long largestBannerByRuns(int[] posts) {
    long best = 0;
    for (int start = 0; start < posts.length; start++) {
        int shortest = Integer.MAX_VALUE;
        for (int end = start; end < posts.length; end++) {
            shortest = Math.min(shortest, posts[end]);
            best = Math.max(best, (long) shortest * (end - start + 1));
        }
    }
    return best;
}
```

For `[2, 4, 3]` it returns 6, which is the banner of height 2 across all three posts, since the narrower options 4 by 1, 3 by 1 and 3 by 2 are smaller.

<!-- stage: bottleneck -->
### Every Run Is A Separate Candidate

The two loops look at `n * (n + 1) / 2` runs, so with 100,000 posts the method makes about five billion steps, and it is O(n^2). Nearly all of them are wasted. For a run to give the best banner it has to be as wide as possible for its limiting post, otherwise a wider run with the same limit would do better. So the only runs worth a look are those that stretch from one limiting post out to the nearest shorter post on each side, and there is one such run per post, `n` in all, and the method looks at all `n * (n + 1) / 2`.

The information about the nearest shorter post on both sides is what the boundary scans of the earlier lessons provide. A single pass has an extra advantage. At the moment a post is found to have a shorter successor, the successor is its right wall, and the post below it on the stack is its left wall, so its width is known the moment it is removed.

<!-- stage: insight -->
### Price Each Post On Shorter Arrival

Each post is the **limiting height** of exactly one widest run: the run that extends to the nearest strictly shorter post on each side. Its area is `height * (right - left - 1)`, where `left` and `right` are the indices of those shorter posts, or the edge positions -1 and `n`. The best banner is the maximum of these `n` areas, and no other run needs to be considered, since a run limited by a post but narrower than its widest run is dominated by it.

The scan keeps a stack of indices whose heights never decrease from bottom to top. A new post `j` removes every top that is strictly taller than it. This is the **pop-time width**: when index `t` is removed by `j`, its right wall is `j`, and its left wall is the index now on top of the stack, or -1 when the stack is empty, so the width is `j - left - 1` and the area `h[t] * (j - left - 1)` is known immediately. Equal heights stay on the stack. A later post of the same height as an earlier one is removed first, with a narrower width, and then the earlier post is removed with the full width that covers both, so the maximum is not changed.

The posts remaining when the row ends have no shorter post to their right. A **closing zero**, a conceptual post of height 0 at index `n`, removes every one of them, with right wall `n`. Without it, the tall increasing runs at the end would never be priced.

<!-- names: limiting height, pop-time width, closing zero -->

Each index is pushed once and removed once, so the whole scan is O(n) time with O(n) extra space for the stack.

<!-- stage: variables -->
### Index, Height And Width At Removal

When index `t` is removed, `h[t]` is the limiting height, the new top is the left wall, the current index `j` is the right wall, and `width = j - left - 1` is the number of posts strictly between the walls. With an empty stack the left wall is -1, so the width is `j`, which is the whole prefix. The best area is kept in a `long`, because 100,000 posts that are each up to 10,000 high give an area of a billion, and larger limits would wrap an `int`. The scan runs for `j` from 0 to `n`, where `j = n` stands for the closing zero and has height 0, which is below every real height. A post of height 0 inside the row removes every taller post below it and is itself pushed, and since its height is 0 it can only ever contribute an area of 0.

<!-- stage: trace -->
### Pricing Posts As Shorter Ones Arrive

Take the posts `3, 6, 2, 5, 4, 5, 1`. The 3 and the 6 are pushed. The 2 arrives, and it is shorter than both. The 6 is removed first, with left wall index 0 and right wall 2, so the width is 1 and the area is 6. The 3 is removed next, with an empty stack below it, so the left wall is -1, the width is 2 and the area is 6. Then the 5 and the 4 arrive; the 4 removes the 5, which is priced at 5. After the second 5, the 1 arrives and removes the 5, the 4 and the 2. The 4 sits above the 2, so its left wall is index 2 and its right wall is 6, the width is 3, and the area is 12, the best so far. The 2 then has width 6 and area 12 as well. The closing zero removes the 1, with width 7 and area 7. The step to study is the arrival of the 1, which resolves three posts at once and finds the best banner in the middle one.

Now take `5, 5, 2, 5`. The second 5 does not remove the first, since it is not taller. The 2 removes the second 5, which is priced with width 1, since the earlier 5 is its left wall, and then the first 5, with width 2 and area 10. The last 5 is removed by the closing zero, with left wall 2 and width 1, and then the 2 gets width 4. The best is 10.

```trace
{"cells":[3,6,2,5,4,5,1],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","best":0},"note":"The height 3 arrives. Nothing is removed. The best area is 0."},{"at":{"j":1},"vars":{"stack":"[0,1]","best":0},"note":"The height 6 arrives. Nothing is removed. The best area is 0."},{"at":{"j":2},"vars":{"stack":"[2]","best":6},"note":"The height 2 arrives. Index 1 (height 6) is removed with left wall 0 and right wall 2, so the width is 1 and the area is 6. Index 0 (height 3) is removed with left wall -1 and right wall 2, so the width is 2 and the area is 6. The best area is 6."},{"at":{"j":3},"vars":{"stack":"[2,3]","best":6},"note":"The height 5 arrives. Nothing is removed. The best area is 6."},{"at":{"j":4},"vars":{"stack":"[2,4]","best":6},"note":"The height 4 arrives. Index 3 (height 5) is removed with left wall 2 and right wall 4, so the width is 1 and the area is 5. The best area is 6."},{"at":{"j":5},"vars":{"stack":"[2,4,5]","best":6},"note":"The height 5 arrives. Nothing is removed. The best area is 6."},{"at":{"j":6},"vars":{"stack":"[6]","best":12},"note":"The height 1 arrives. Index 5 (height 5) is removed with left wall 4 and right wall 6, so the width is 1 and the area is 5. Index 4 (height 4) is removed with left wall 2 and right wall 6, so the width is 3 and the area is 12. Index 2 (height 2) is removed with left wall -1 and right wall 6, so the width is 6 and the area is 12. The best area is 12."},{"at":{"j":7},"vars":{"stack":"[]","best":12},"note":"The closing zero arrives. Index 6 (height 1) is removed with left wall -1 and right wall 7, so the width is 7 and the area is 7. The best area is 12."}]}
```

```trace
{"cells":[5,5,2,5],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","best":0},"note":"The height 5 arrives. Nothing is removed. The best area is 0."},{"at":{"j":1},"vars":{"stack":"[0,1]","best":0},"note":"The height 5 arrives. Nothing is removed. The best area is 0."},{"at":{"j":2},"vars":{"stack":"[2]","best":10},"note":"The height 2 arrives. Index 1 (height 5) is removed with left wall 0 and right wall 2, so the width is 1 and the area is 5. Index 0 (height 5) is removed with left wall -1 and right wall 2, so the width is 2 and the area is 10. The best area is 10."},{"at":{"j":3},"vars":{"stack":"[2,3]","best":10},"note":"The height 5 arrives. Nothing is removed. The best area is 10."},{"at":{"j":4},"vars":{"stack":"[]","best":10},"note":"The closing zero arrives. Index 3 (height 5) is removed with left wall 2 and right wall 4, so the width is 1 and the area is 5. Index 2 (height 2) is removed with left wall -1 and right wall 4, so the width is 4 and the area is 8. The best area is 10."}]}
```

<!-- stage: code -->
### Largest Rectangle With A Closing Zero

```java
static long largestRectangle(int[] h) {
    int n = h.length;
    long best = 0;
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j <= n; j++) {
        int current = (j == n) ? 0 : h[j];                 // the closing zero at j == n
        while (!stack.isEmpty() && h[stack.peekLast()] > current) {
            int t = stack.removeLast();
            int left = stack.isEmpty() ? -1 : stack.peekLast();
            long width = j - left - 1;                      // posts strictly between the walls
            best = Math.max(best, (long) h[t] * width);
        }
        if (j < n) stack.addLast(j);
    }
    return best;
}
```

Every index enters and leaves the stack once, so a single linear pass suffices and the stack holds at most `n` indices. The comparison is strict, so equal heights stay on the stack and the earlier of two equal posts is priced with the full width. The `long` widening is applied to the width before the multiplication, and the closing zero makes the loop run to `j = n` so that no post is left unpriced.

<!-- stage: applicability -->
### When A Limit Sets The Rectangle

Use this scan when each element limits a rectangle, a window or a stretch that extends to the nearest element that breaks the limit on both sides, and the answer is a maximum over those stretches of limit times width. The invariant is that the stack holds heights that never decrease from bottom to top, each waiting for its right wall, and that when an index is removed, its left wall is the new top and its right wall is the current index. End the scan with a closing step that removes everything.

The false friend is the next-smaller distance on one side alone. Knowing how far a post can stretch to the right says nothing about the left, and for `[3, 6, 2, 5, 4, 5, 1]` the best banner is the 4 with width 3, which reaches left over the 5 and right over the 5. A second false friend is the largest height times the count of posts, or the average, which ignore the fact that the shortest post in a run is what limits it. Another is the two-pointer idea that moves the shorter end inward; it is correct for a different question, the container with most water, where the limit is the shorter of two ends and not of every post in between.

Do not apply the stack when the question is about a fixed width window, where a sliding window with a deque in a later chapter is the right structure. In Java also remember that `int` arithmetic on a height times a width can overflow, so widen first.

<!-- stage: exercises -->
### Exercises

#### [Build] Rectangle From Supplied Boundaries (Author exercise)
<!-- id: ms-rectangle-supplied-boundaries -->

**Prerequisites.** The boundary and contribution lessons of this chapter.

**Problem.** Given an array `h` of non-negative bar heights, and arrays `left` and `right` that hold for every index the nearest strictly shorter bar to its left, or -1, and to its right, or `n`, return the largest value of `h[i] * (right[i] - left[i] - 1)`.

**Constraints.** 1 <= h.length <= 10^5 and 0 <= h[i] <= 10^4. The answer can reach 10^9, so use `long`.

**Example 1.** Input `h = [4, 1, 3, 5, 2, 2]`, `left = [-1, -1, 1, 2, 1, 1]`, `right = [1, 6, 4, 4, 6, 6]`, output 8.

**Example 2.** Input `h = [7]`, `left = [-1]`, `right = [1]`, output 7.

**Hint.** What does `right - left - 1` count? Why is the strictly shorter bar, and not an equal one, the right limit of a rectangle?

**Changed decision.** First rung: the area formula, with the two walls given as input, so the only new thing is the width.

#### [Vary] Resolve On A Shorter Bar (Author exercise)
<!-- id: ms-resolve-on-shorter-bar -->

**Prerequisites.** The Rectangle From Supplied Boundaries exercise above.

**Problem.** Given an array `h` of bar heights whose last element is 0, return the area of the largest rectangle that fits under the bars, computed in one left-to-right scan that prices each bar at the moment a strictly shorter bar arrives.

**Constraints.** 2 <= h.length <= 10^5, 0 <= h[i] <= 10^4, and the final element is 0. Do not store arrays of walls.

**Example 1.** Input `h = [3, 6, 2, 5, 4, 5, 1, 0]`, output 12.

**Example 2.** Input `h = [5, 5, 5, 0]`, output 15, so equal bars are priced correctly through the earlier bar.

**Hint.** When a bar is removed from the stack, which index is the left wall and which is the right wall? What is the width, and which bar of an equal pair receives the full width?

**Changed decision.** The walls are not precomputed. The width is derived from the stack at removal time, and the final zero removes everything.

#### [Boundary] Flush Increasing Heights (Author exercise)
<!-- id: ms-flush-increasing-heights -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `h` of bar heights that does not end with 0, and which may rise all the way to its last element, return the largest rectangle area. Add the closing zero conceptually and do not copy the array.

**Constraints.** 1 <= h.length <= 10^5 and 0 <= h[i] <= 10^4. Use `j == n` in the loop for the closing zero.

**Example 1.** Input `h = [2, 4, 6]`, output 8.

**Example 2.** Input `h = [5]`, output 5, because the only bar waits for the closing zero.

**Hint.** What would your scan return for a strictly increasing array if the loop stopped at `j = n - 1`? Which bars would never be priced?

**Changed decision.** The row can end while bars are still waiting, so a closing step is needed to resolve every remaining index.

#### [Recognize] Largest Rectangle in Histogram (LeetCode 84)
<!-- id: ms-largest-rectangle-histogram -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `heights` of non-negative integers, where each bar has width 1, return the area of the largest rectangle in the histogram.

**Constraints.** 1 <= heights.length <= 10^5 and 0 <= heights[i] <= 10^4.

**Example 1.** Input `heights = [6, 2, 5, 4, 5, 1, 6]`, output 12.

**Example 2.** Input `heights = [3, 3, 1, 3]`, output 6, so the two equal bars at the front beat the lone 3 at the end.

**Hint.** Combine the pop-time width with the closing zero. Which bar's removal produces the best rectangle in the first example?

**Changed decision.** The row is general, so the scan needs both the resolve-on-a-shorter-bar rule and the closing step, with the width taken from the new top of the stack.
