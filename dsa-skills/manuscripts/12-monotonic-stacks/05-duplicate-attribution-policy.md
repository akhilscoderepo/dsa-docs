<!-- lesson-kind: standard -->
<!-- lesson-id: duplicate-attribution-policy -->
## Break Ties Between Equal Values

<!-- stage: context -->
### Two Equal Readings Claim The Same Window

A monitoring report credits each reading with the windows in which it is the lowest. A window is a run of consecutive readings, such as readings 3 through 5. The report adds one credit per window, so a log of 2 readings must produce 3 credits, one for each of the windows `[0]`, `[1]` and `[0, 1]`.

Take the readings 2 and 2. Each reading is lowest in its own one-reading window. In the window of both readings, the two readings tie for lowest, so both claim it. The report shows 4 credits for 3 windows. The lesson answers one question. How can the code give every window to exactly one reading when values are equal?

<!-- stage: naive -->
### Credit One Reading Per Window By Enumeration

The direct approach lists every window by its first index `l` and last index `r`. It keeps a running minimum while `r` grows, and it records which index holds that minimum. On a tie it keeps the later index. After each extension, it adds one credit to the recorded index.

```java
static int[] creditsByEnumeration(int[] nums) {
    int n = nums.length;
    int[] credits = new int[n];
    for (int l = 0; l < n; l++) {
        int best = l;
        for (int r = l; r < n; r++) {
            if (nums[r] <= nums[best]) best = r;
            credits[best]++;
        }
    }
    return credits;
}
```

The method is correct, and every window receives exactly one credit. On the readings 2 and 2, it returns 1 for the first reading and 2 for the second. The later reading takes the window of both.

<!-- stage: bottleneck -->
### The Windows Outnumber The Readings

```predict
A log holds 100000 readings. How many windows does the enumeration visit?

About 5 x 10^9. A log of n readings has n x (n + 1) / 2 windows, and 100000 x 100001 / 2 is about 5 x 10^9.
```

The enumeration visits n(n + 1) / 2 windows, so it takes O(n^2) time for `n` readings. Counting must avoid looking at windows one by one. A reading with `a` possible starts and `b` possible ends owns `a * b` windows, and one multiplication would replace `a * b` visits.

The earlier lessons computed the boundaries that give `a` and `b`. The open question is what the boundary comparison does with equal values. The wrong choice either counts a window twice or leaves it with no credit.

<!-- stage: insight -->
### Make The Two Sides Disagree On Equality

Counting by multiplication works only if every window has exactly one reading that claims it. The tie decision must happen once per window, and the two boundary scans must agree on it.

<!-- names: owner, tie rule, rightmost minimum -->

#### Every Window Gets One Owner

The **owner** of a window is the single index that receives the window's credit. The **tie rule** picks the owner among equal minimum values. One rule that always works is to choose the **rightmost minimum**: the largest index in the window that holds the window's minimum value. A window has at least one minimum, so it has exactly one rightmost minimum. No window is unowned, and no window has two owners.

#### What Index i Needs To Own A Window

Index `i` owns the window from `l` to `r` exactly when two conditions hold. Every value in `l` through `i - 1` is at least `nums[i]`, because equal values to the left do not stop `i` from being the rightmost minimum. Every value in `i + 1` through `r` is strictly greater than `nums[i]`, because an equal value to the right would take the title.

So the left boundary of `i` is the nearest strictly smaller value. The right boundary is the nearest value that is smaller or equal. The two sides use opposite comparisons on purpose. The count of owned windows is `(i - left) * (right - i)`, where `left` is `-1` or an index, and `right` is `n` or an index.

#### One Pass Produces Both Sides

A stack with strictly increasing values does both jobs. A new value removes every top whose value is at least as large. Each removed top gets the new index as its right boundary, which is the first value that is smaller or equal. The surviving top becomes the left boundary of the new index, which is the nearest strictly smaller value. Equal values pop each other, so the later one takes the right boundary of the earlier one. The choice of the rightmost minimum is a convention, and choosing the leftmost minimum would swap the two comparisons.

<!-- stage: variables -->
### What Counting Needs

The pass tracks five pieces of state.

- **left** is the index of the nearest strictly smaller value before `i`, or `-1`.
- **right** is the index of the nearest smaller or equal value after `i`, or `n`.
- **stack** holds indices whose values strictly increase from bottom to top.
- **owned** is `(i - left) * (right - i)`, the number of windows owned by index `i`.
- **total** is the sum of all `owned` entries, and it must equal `n * (n + 1) / 2`.

A popped index finishes its `right` value at the pop. Its `left` value was fixed when it was pushed.

<!-- stage: trace -->
### Following The Ownership Rule

#### One Pass With Equal Values

The first trace reads 3, 2, 2, 4, 2, 5 and uses the single pass. The stack lists indices. Each pop fixes the right boundary of the popped index, and the push fixes the left boundary of the new index. The second 2 pops the first 2, so the first 2 gets right boundary 2. No 2 has a strictly smaller value before it, so every 2 has left boundary -1. The last 2 pops the 4 and the second 2, and it owns 5 x 2 = 10 windows.

```trace
{"cells":[3,2,2,4,2,5],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[0]","left":"[-1, ., ., ., ., .]","right":"[., ., ., ., ., .]"},"note":"The surviving top gives left[0] = -1, and index 0 goes on the stack."},{"at":{"i":1},"vars":{"stack":"[]","left":"[-1, ., ., ., ., .]","right":"[1, ., ., ., ., .]"},"note":"nums[0] = 3 is at least 2, so right[0] = 1 and index 0 leaves the stack."},{"at":{"i":1},"vars":{"stack":"[1]","left":"[-1, -1, ., ., ., .]","right":"[1, ., ., ., ., .]"},"note":"The surviving top gives left[1] = -1, and index 1 goes on the stack."},{"at":{"i":2},"vars":{"stack":"[]","left":"[-1, -1, ., ., ., .]","right":"[1, 2, ., ., ., .]"},"note":"nums[1] = 2 is at least 2, so right[1] = 2 and index 1 leaves the stack."},{"at":{"i":2},"vars":{"stack":"[2]","left":"[-1, -1, -1, ., ., .]","right":"[1, 2, ., ., ., .]"},"note":"The surviving top gives left[2] = -1, and index 2 goes on the stack."},{"at":{"i":3},"vars":{"stack":"[2, 3]","left":"[-1, -1, -1, 2, ., .]","right":"[1, 2, ., ., ., .]"},"note":"The surviving top gives left[3] = 2, and index 3 goes on the stack."},{"at":{"i":4},"vars":{"stack":"[2]","left":"[-1, -1, -1, 2, ., .]","right":"[1, 2, ., 4, ., .]"},"note":"nums[3] = 4 is at least 2, so right[3] = 4 and index 3 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[]","left":"[-1, -1, -1, 2, ., .]","right":"[1, 2, 4, 4, ., .]"},"note":"nums[2] = 2 is at least 2, so right[2] = 4 and index 2 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[4]","left":"[-1, -1, -1, 2, -1, .]","right":"[1, 2, 4, 4, ., .]"},"note":"The surviving top gives left[4] = -1, and index 4 goes on the stack."},{"at":{"i":5},"vars":{"stack":"[4, 5]","left":"[-1, -1, -1, 2, -1, 4]","right":"[1, 2, 4, 4, ., .]"},"note":"The surviving top gives left[5] = 4, and index 5 goes on the stack."},{"at":{"i":6},"vars":{"stack":"[4, 5]","left":"[-1, -1, -1, 2, -1, 4]","right":"[1, 2, 4, 4, 6, 6]","owned":"[1, 2, 6, 1, 10, 1]"},"note":"The scan ends. The remaining indices get right = 6, and owned[i] = (i - left) * (right - i) gives [1, 2, 6, 1, 10, 1]."}]}
```

#### Windows Of Equal Values

The second trace lists every window of the readings 2, 2, 2. The pointers `l` and `r` mark the first and last index of a window. Every window goes to its last index, because all values tie and the rightmost minimum is the last position of the window. The index counts 1, 2 and 3 add up to 6 windows, which is `3 * 4 / 2`.

```trace
{"cells":[2,2,2],"pointers":["l","r"],"steps":[{"at":{"l":0,"r":0},"vars":{"owner":0,"credits":"[1, 0, 0]"},"note":"The window from 0 to 0 holds only 2s, so its rightmost minimum is index 0, and index 0 gets one credit."},{"at":{"l":0,"r":1},"vars":{"owner":1,"credits":"[1, 1, 0]"},"note":"The window from 0 to 1 holds only 2s, so its rightmost minimum is index 1, and index 1 gets one credit."},{"at":{"l":0,"r":2},"vars":{"owner":2,"credits":"[1, 1, 1]"},"note":"The window from 0 to 2 holds only 2s, so its rightmost minimum is index 2, and index 2 gets one credit."},{"at":{"l":1,"r":1},"vars":{"owner":1,"credits":"[1, 2, 1]"},"note":"The window from 1 to 1 holds only 2s, so its rightmost minimum is index 1, and index 1 gets one credit."},{"at":{"l":1,"r":2},"vars":{"owner":2,"credits":"[1, 2, 2]"},"note":"The window from 1 to 2 holds only 2s, so its rightmost minimum is index 2, and index 2 gets one credit."},{"at":{"l":2,"r":2},"vars":{"owner":2,"credits":"[1, 2, 3]"},"note":"The window from 2 to 2 holds only 2s, so its rightmost minimum is index 2, and index 2 gets one credit."}]}
```

<!-- stage: code -->
### One Pass That Counts Windows

#### The Stack With Both Boundaries

The method pops with `>=`. A pop writes the right boundary of the popped index, and the push of the new index reads its left boundary from the surviving top. Counts use `long`, because `(i - left) * (right - i)` can exceed what `int` holds when `n` is large.

```java
static long[] ownedWindows(int[] nums) {
    int n = nums.length;
    int[] left = new int[n];
    int[] right = new int[n];
    Arrays.fill(right, n);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) {
            right[stack.pop()] = i;
        }
        left[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(i);
    }
    long[] owned = new long[n];
    for (int i = 0; i < n; i++) {
        owned[i] = (long) (i - left[i]) * (right[i] - i);
    }
    return owned;
}
```

The cast `(long)` applies to the first factor before the multiplication, so the product is computed in `long`. The pass costs O(n) time because each index enters the stack once and leaves it at most once. The arrays and the stack use O(n) extra space.

#### Checking The Partition

The sum of `owned` must equal `n * (n + 1) / 2` for every input. A test that compares the sum with that value catches both double counting and gaps.

<!-- stage: applicability -->
### When The Tie Rule Matters

#### The Cue For A Tie Rule

The cue is a count or a sum over all windows that credits each window to its minimum, or to its maximum, when equal values can occur. The invariant is that every window has exactly one owner, so the counts form a partition of the windows. The two sides must use opposite comparisons on equality, and either choice of which side is strict works when it is applied consistently.

#### Two False Friends

Strict comparisons on both sides are the first false friend. On the readings 2 and 2, both boundaries stop only at smaller values, so each reading owns every window that contains it. The counts are 2 and 2, which total 4 for 3 windows.

Non-strict comparisons on both sides are the second false friend. Each reading then stops at its equal neighbor, so the window of both readings has no owner. The counts are 1 and 1, which total 2.

#### When It Does Not Apply

The rule is unnecessary when all values are distinct, because no ties occur. It is also unnecessary when the question asks only for the widest region around each value, as in the previous lesson, because that question allows equal values inside the region and credits nothing.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Equal Minima Ownership (Author exercise)
<!-- id: ms-two-equal-minima -->

**Prerequisites.** The rightmost-minimum rule in this lesson.

**Problem.** Take an integer array `nums`. A window is a range of consecutive indices from `l` to `r` with `l <= r`. The owner of a window is the largest index in the window that holds the window's minimum value. Return an array whose entry `i` is the number of windows that index `i` owns. List the windows directly.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 2000`.
- **Values** are `int` values, and equal values are allowed.
- **Partition** means every window has exactly one owner.
- **Return** is an `int[]` of the same length.

**Example 1.** Input `[2,2,2]`, output `[1,2,3]`.

**Example 2.** Input `[2,7,2,7,2]`, output `[2,1,6,1,5]`.

**Hint.** Extend the end of the window one index at a time and keep the owner so far. When the new value is equal to the current minimum, who owns the window?

**Changed decision.** A tie moves the title to the later index, so equality updates the owner.

#### [Vary] Strict Left, Non-Strict Right (Author exercise)
<!-- id: ms-strict-left-non-strict-right -->

**Prerequisites.** The exercise above and the single pass in this lesson.

**Problem.** For each index `i`, let `left` be the largest index before `i` with a strictly smaller value, or `-1`. Let `right` be the smallest index after `i` with a value smaller than or equal to `nums[i]`, or `n`. Return an array whose entry `i` equals `(i - left) * (right - i)`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values, and equal values are allowed.
- **Counts** can exceed the range of `int`, so each entry is a `long`.
- **Return** is a `long[]` of the same length.

**Example 1.** Input `[3,2,2,4,2,5]`, output `[1,2,6,1,10,1]`.

**Example 2.** Input `[4,4,1,4,4]`, output `[1,2,9,1,2]`.

**Hint.** Equal values pop each other. Which index gets the boundary when a pop happens, and which index reads the surviving top?

**Changed decision.** The tie decision moves from a window list into two boundary comparisons, so the cost drops to one pass.

#### [Boundary] All Equal Array (Author exercise)
<!-- id: ms-all-equal-array -->

**Prerequisites.** The two exercises above.

**Problem.** Use the ownership counts of the previous exercise. Return the counts of all indices, followed by one extra entry that holds their sum. For every input, the sum equals the number of windows `n * (n + 1) / 2`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values, and every value can be equal.
- **Sum** must equal `n * (n + 1) / 2`, with no window dropped and none counted twice.
- **Return** is a `long[]` of length `n + 1`.

**Example 1.** Input `[2,2,2]`, output `[1,2,3,6]`.

**Example 2.** Input `[5,1,5,1,5]`, output `[1,4,1,8,1,15]`.

**Hint.** An all-equal array is the extreme tie case. Which side of each index stops at its neighbor, and which side runs to the array end?

**Changed decision.** The output adds a checked total, so a wrong tie rule shows up as a wrong sum.

#### [Recognize] Sum of Subarray Minimums (LeetCode 907)
<!-- id: ms-sum-of-subarray-minimums-exact -->

**Prerequisites.** The three exercises above.

**Problem.** Let `arr` be an array of positive integers. Return the sum of `min(subarray)` over every contiguous non-empty subarray of `arr`. This version asks for the exact sum, with no remainder operation.

**Constraints.** The limits are:
- **Length** is `1 <= arr.length <= 3 * 10^4`.
- **Values** are integers with `1 <= arr[i] <= 10^4`, and equal values are allowed.
- **Sum** fits in a `long`, and no modulus is applied.
- **Return** is a `long`.

**Example 1.** Input `[2,7,2,7,2]`, output `40`.

**Example 2.** Input `[6,3,6,3,6]`, output `54`.

**Hint.** State which side of an index stops at an equal value before you multiply. Then credit each value with the product of its two distances.

**Changed decision.** The original problem asks for a remainder, and this version asks for the exact sum, so the arithmetic stays in `long` throughout.
