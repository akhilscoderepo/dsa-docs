<!-- lesson-kind: standard -->
<!-- lesson-id: boundary-discovery -->
## Boundary Discovery

<!-- stage: context -->
### How Far Can A Plank Stretch

A fence is built from planks of different heights standing side by side, and a painter wants to roll a long strip of tape along the fence at the height of a chosen plank. The tape can only run across planks that are at least as tall as the chosen one, because a shorter plank would leave a gap beneath the tape. So she walks left from the chosen plank until she meets a plank that is shorter, and then right until she meets a shorter one. Those two meetings mark where the strip must end.

She wants these two stopping places for every plank on the fence, and she wants to know how wide each strip is. Some planks are so low that nothing on one side is shorter, and for them the strip reaches the end of the fence. She has a notebook with a column for the left stop and a column for the right stop, and she intends to fill it quickly.

<!-- stage: naive -->
### Walk Both Ways From Each Plank

The direct method takes each plank and walks outward in both directions until it finds a shorter plank or leaves the fence.

```java
static int[][] wallsByWalking(int[] h) {
    int n = h.length;
    int[][] walls = new int[n][2];
    for (int i = 0; i < n; i++) {
        int l = i - 1;
        while (l >= 0 && h[l] >= h[i]) l--;
        int r = i + 1;
        while (r < n && h[r] >= h[i]) r++;
        walls[i][0] = l;
        walls[i][1] = r;
    }
    return walls;
}
```

It is correct. For `[3, 5, 4]` it returns, for the 5, the pair `(0, 2)`, because the 3 on the left and the 4 on the right are both shorter, and for the 3 it returns `(-1, 3)`, because nothing shorter exists on either side.

<!-- stage: bottleneck -->
### Level Fences Make Every Walk Long

When all planks have the same height, or the heights only rise, every walk runs a long way before it stops. For a fence of `n` equal planks, each of the `n` planks walks across all the others on both sides, which is about `n * n` steps in total, and the method is O(n^2). A fence of 100,000 planks asks for about ten billion steps just to learn that no plank has a shorter neighbour.

The repeated work shows in the walks that start at neighbouring planks. If plank 4 is at least as tall as plank 3, then everything that plank 3's left walk saw is also seen by plank 4's left walk, and plank 4 could have started from the stopping place of plank 3 rather than from its own side. The planks passed over by a walk are exactly those that are no shorter than the walker, and these are the ones that the next walk does not need to look at again. Two long scans are being done as many small ones.

<!-- stage: insight -->
### One Pass Finds Walls For All

Keep a stack of indices whose heights strictly increase from bottom to top, and scan from left to right. For the plank at index `j`, remove every top whose height is at least `h[j]`, because the new plank is closer and no taller, so the removed plank can never again be the nearest shorter plank for any later plank. After the removal, the top of the stack, if there is one, is the **left wall** of `j`: the nearest earlier plank that is strictly shorter. If the stack is empty, the left wall is the **sentinel edge** -1, a position just before the fence. Then `j` is pushed. This finds the left wall of every plank in one pass, and the left wall is read from the surviving top, after the removals.

The right wall is found by the same idea in the opposite direction, or by resolving on a pop. Scan left to right again and pop a top when a strictly shorter plank arrives. The arriving index is that top's **right wall**. Planks that are never popped have no shorter plank to their right, and their right wall is the sentinel edge `n`, a position just past the fence. The popping condition uses a strict comparison here, so a plank of equal height never ends a strip. With strict comparisons on both sides, a strip may include any number of equal planks.

<!-- names: left wall, right wall, sentinel edge -->

The strip of plank `i` then contains every plank strictly between its two walls, so its width is `right - left - 1`, and with the sentinels this formula needs no special case at either end. Each of the two scans costs O(n), since each index is pushed once and popped at most once.

<!-- stage: variables -->
### Two Columns Of The Notebook

The `left` array holds, for each index, the index of the nearest strictly shorter plank to its left, or -1. The `right` array holds the nearest strictly shorter plank to its right, or `n`. These two sentinel values are not accidents: -1 and `n` are the positions just outside the array, so a plank with no wall on one side gets a strip that reaches the edge, and `right - left - 1` counts exactly the planks inside. The stack holds indices and never values, since the walls are positions. In the left scan the stack is rebuilt by removing with `>=`, so its heights strictly increase. In the right scan the stack is allowed to hold equal heights, because only a strictly shorter plank pops. The array `right` is filled with `n` before the scan begins, and each entry is overwritten exactly once, when its index is popped.

<!-- stage: trace -->
### Walls On A Small Fence

Take the fence `3, 5, 4, 6, 2, 7` and scan for left walls. The 3 finds an empty stack and gets the sentinel -1. The 5 sees the 3 on top, which is shorter, so the 5 keeps it as its left wall. The 4 removes the 5, which is not shorter, and meets the 3, so its left wall is index 0. The 6 meets the 4 and gets index 2. The 2 removes the 6, the 4 and the 3, so the stack is empty and the wall is the sentinel -1. The 7 meets the 2 and gets index 4. The step to study is the 2, where a single plank removes three entries and ends with no wall at all.

Next take `2, 5, 5, 3, 1` and scan for right walls by resolving on a pop. The first 5 and the second 5 are equal, so the second does not pop the first, and both wait. The 3 pops the two 5s, so both get right wall 3. The 1 pops the 3 and the 2, so the walls are index 4 for the 3 and index 4 for the 2. The 1 itself is never popped, so its right wall stays at the sentinel 5.

```trace
{"cells":[3,5,4,6,2,7],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"left":-1,"stack":"[0]"},"note":"Nothing is removed. The stack is empty, so the left wall is the sentinel -1."},{"at":{"j":1},"vars":{"left":0,"stack":"[0,1]"},"note":"Nothing is removed. The surviving top is index 0, which is shorter, so it is the left wall."},{"at":{"j":2},"vars":{"left":0,"stack":"[0,2]"},"note":"The height 4 removes index 1 because those planks are not shorter. The surviving top is index 0, which is shorter, so it is the left wall."},{"at":{"j":3},"vars":{"left":2,"stack":"[0,2,3]"},"note":"Nothing is removed. The surviving top is index 2, which is shorter, so it is the left wall."},{"at":{"j":4},"vars":{"left":-1,"stack":"[4]"},"note":"The height 2 removes index 3, 2, 0 because those planks are not shorter. The stack is empty, so the left wall is the sentinel -1."},{"at":{"j":5},"vars":{"left":4,"stack":"[4,5]"},"note":"Nothing is removed. The surviving top is index 4, which is shorter, so it is the left wall."}]}
```

```trace
{"cells":[2,5,5,3,1],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"right":"[5,5,5,5,5]","stack":"[0]"},"note":"The height 2 is not shorter than the top, or the stack is empty, so nothing is resolved and index 0 is pushed."},{"at":{"j":1},"vars":{"right":"[5,5,5,5,5]","stack":"[0,1]"},"note":"The height 5 is not shorter than the top, or the stack is empty, so nothing is resolved and index 1 is pushed."},{"at":{"j":2},"vars":{"right":"[5,5,5,5,5]","stack":"[0,1,2]"},"note":"The height 5 is not shorter than the top, or the stack is empty, so nothing is resolved and index 2 is pushed."},{"at":{"j":3},"vars":{"right":"[5,3,3,5,5]","stack":"[0,3]"},"note":"The height 3 is strictly shorter than the waiting plank(s) at index 2, 1, so their right wall is 3. Index 3 is pushed."},{"at":{"j":4},"vars":{"right":"[4,3,3,4,5]","stack":"[4]"},"note":"The height 1 is strictly shorter than the waiting plank(s) at index 3, 0, so their right wall is 4. Index 4 is pushed."}]}
```

<!-- stage: code -->
### Left And Right Walls

```java
static int[] leftWalls(int[] h) {
    int n = h.length;
    int[] left = new int[n];
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j < n; j++) {
        while (!stack.isEmpty() && h[stack.peekLast()] >= h[j]) stack.removeLast();
        left[j] = stack.isEmpty() ? -1 : stack.peekLast();   // read after the removals
        stack.addLast(j);
    }
    return left;
}

static int[] rightWalls(int[] h) {
    int n = h.length;
    int[] right = new int[n];
    java.util.Arrays.fill(right, n);                          // n means no shorter plank to the right
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j < n; j++) {
        while (!stack.isEmpty() && h[j] < h[stack.peekLast()]) right[stack.removeLast()] = j;
        stack.addLast(j);
    }
    return right;
}
```

Each method scans once, and every index is on the stack for one stretch of the scan, so both run in O(n) time with O(n) extra space. The width of the strip at `i` is `right[i] - left[i] - 1`. In `leftWalls` the answer is read after the removals and the comparison removes equals, so the stack holds strictly increasing heights. In `rightWalls` the answer is written when a pop happens, and equals are kept on the stack. Both comparisons ask the same question, which is whether a plank is strictly shorter.

<!-- stage: applicability -->
### When The Neighbours Set The Limits

Use boundary discovery when the region where an element keeps its role, such as being the minimum, is limited on each side by the nearest element that breaks the role. The invariant is that, after the left scan has handled `j`, the stack holds exactly the indices that can still be the nearest strictly shorter plank for some later index, and the surviving top is the left wall of `j`. Choose the comparison for each side from the definition of the region, and write down the two sentinels before coding.

The false friend is the boundary value alone. Knowing that the nearest shorter plank on the right has height 4 says nothing about how many planks lie between, and widths, counts and areas all depend on positions. A second false friend is a pair of values taken from a prefix minimum and a suffix minimum, which tells you the lowest plank on each side and not the nearest shorter one. For `[2, 1, 5, 6, 2, 3]` the nearest shorter plank to the left of the final 3 is the 2 at index 4, while the prefix minimum is the 1.

Do not use two independent strict scans when equal heights must be shared out between planks, as when counting subarrays by their minimum, because a strict wall on both sides lets equal planks all claim the same region. That problem needs an asymmetric rule, which the next lesson derives. Remember also that the widths are measured in positions, so with unequal spacing between planks the arithmetic would have to use coordinates, not indices.

<!-- stage: exercises -->
### Exercises

#### [Build] Previous Smaller Index (Author exercise)
<!-- id: ms-previous-smaller-index -->

**Prerequisites.** The first three lessons of this chapter.

**Problem.** Given an integer array `a`, return an array `p` where `p[i]` is the largest index `k < i` with `a[k] < a[i]`, or -1 if no such index exists. A value equal to `a[i]` is not smaller.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. One left-to-right pass.

**Example 1.** Input `a = [3, 5, 4, 6, 2, 7]`, output `[-1, 0, 0, 2, -1, 4]`.

**Example 2.** Input `a = [2, 2, 2]`, output `[-1, -1, -1]`, since equal values are not smaller.

**Hint.** What does the surviving top mean after the removals? Which comparison removes equal values, and why must it?

**Changed decision.** First rung: the stack keeps strictly increasing values, and the answer is read from the survivor.

#### [Vary] Next Smaller Index (Author exercise)
<!-- id: ms-next-smaller-index -->

**Prerequisites.** The Previous Smaller Index exercise above.

**Problem.** Given an integer array `a`, return an array `q` where `q[i]` is the smallest index `j > i` with `a[j] < a[i]`, or `n` if no such index exists, where `n` is the array length.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. One left-to-right pass that resolves indices when they are popped.

**Example 1.** Input `a = [4, 6, 5, 2, 7, 1]`, output `[3, 2, 3, 5, 5, 6]`.

**Example 2.** Input `a = [1, 2, 3]`, output `[3, 3, 3]`, because nothing smaller ever arrives.

**Hint.** The first lesson resolved indices at a pop. Which comparison pops here, and what value should an index that is never popped keep?

**Changed decision.** The answer is written at a pop and the default is `n`, not -1, so that a missing wall points just past the array.

#### [Boundary] No Boundary (Author exercise)
<!-- id: ms-no-boundary -->

**Prerequisites.** The two exercises above.

**Problem.** For each index `i` of an integer array `a`, return the pair `[left, right]` where `left` is the nearest earlier index with a strictly smaller value and `right` is the nearest later index with a strictly smaller value. Use -1 for a missing left wall and `n` for a missing right wall.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [1, 2, 3]`, output `[[-1, 3], [0, 3], [1, 3]]`.

**Example 2.** Input `a = [3, 2, 1]`, output `[[-1, 1], [-1, 2], [-1, 3]]`.

**Hint.** Why are -1 and `n` the right sentinels for the formula `right - left - 1`? What would a sentinel of 0 do to the width of the first element?

**Changed decision.** Both sentinels are fixed and used on both sides, so a missing wall never needs a special case in later arithmetic.

#### [Recognize] Widest Region Where Each Value Is Minimum (Author exercise)
<!-- id: ms-widest-minimum-region -->

**Prerequisites.** All three exercises above.

**Problem.** For each index `i` of an integer array `a`, return the number of elements in the longest contiguous subarray that contains `i` and in which `a[i]` is less than or equal to every element. Equal values are allowed inside the region.

**Constraints.** 1 <= a.length <= 10^5 and 1 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [2, 1, 5, 6, 2, 3]`, output `[1, 6, 2, 1, 4, 1]`.

**Example 2.** Input `a = [4, 4, 4]`, output `[3, 3, 3]`, since equal values do not end a region.

**Hint.** Which two arrays from this lesson give the ends, and which formula turns them into a width? Why do strict walls on both sides suit this particular question?

**Changed decision.** Both walls are used at once, and the answer is a distance, so the boundary value alone is not enough.
