<!-- lesson-kind: standard -->
<!-- lesson-id: next-greater-or-smaller -->
## Find The Next Greater Value

<!-- stage: context -->
### Every Reading Needs A Later Answer

A monitoring service stores one temperature reading per hour in an array. The alert page must show, for every reading, the first later reading that is higher. Hour 0 reads 6, hour 1 reads 2 and hour 2 reads 4, so the answer for hour 1 is 4. The service runs this report on logs with 100000 readings, and the first version needs minutes to finish.

The lesson answers one question. How can a single left-to-right pass find the first higher later value for every position?

<!-- stage: naive -->
### Scan Right From Every Position

The direct approach starts at each index `i` and walks to the right until it meets a value strictly greater than `nums[i]`. It stores that value, or `-1` when the walk reaches the end of the array.

```java
static int[] nextGreaterScan(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    for (int i = 0; i < n; i++) {
        ans[i] = -1;
        for (int j = i + 1; j < n; j++) {
            if (nums[j] > nums[i]) {
                ans[i] = nums[j];
                break;
            }
        }
    }
    return ans;
}
```

The method is correct. On the readings 6, 2, 4, 3, 9, the walk from the 2 stops at the 4 after one step. The walk from the 6 passes the 2, the 4 and the 3 before it stops at the 9.

<!-- stage: bottleneck -->
### Every Walk Rereads The Same Values

```predict
The array holds 100000 values in strictly decreasing order, such as 100000, 99999 and so on down to 1. About how many comparisons does the scan make in total?

About 5 x 10^9. No value has a greater value after it, so the walk from index i reads all of the 100000 - i - 1 later values. The sum over all indices is 100000 x 99999 / 2.
```

The worst case is O(n^2) comparisons for an array of length `n`. A decreasing array triggers it, because no walk ever stops early. Doubling the log quadruples the time.

Most of that work repeats. In the readings 6, 2, 4, 3, 9, the walk from index 0 reads the 2, the 4 and the 3. The walk from index 1 reads the 4 again. The walk from index 2 reads the 3 again. Each walk learns something about the values it passes, and then the next walk throws that knowledge away.

<!-- stage: insight -->
### Keep The Waiting Positions In A Stack

One pass can answer every position if it remembers which positions still wait for a greater value. It must also drop a position the moment its answer arrives.

<!-- names: unresolved index, resolving value, monotonic stack -->

#### Positions Wait Until A Greater Value Arrives

An **unresolved index** is an index the scan has already read whose next greater value has not appeared yet. When the scan reaches index `j`, the value `nums[j]` is the **resolving value** for every unresolved index whose value is smaller than `nums[j]`. Each of those indices gets the answer `nums[j]` right away. Index `j` is the first position after them that exceeds their value, because an earlier position would have resolved them already.

#### The Waiting Values Never Increase

Take two unresolved indices `a < b`. Their values satisfy `nums[a] >= nums[b]`. If `nums[b]` were larger, the scan would have resolved `a` when it reached `b`, so `a` would no longer wait. Equal values can wait side by side, because equality does not resolve anything.

Store the unresolved indices in a stack, with the newest index on top. The values then never increase from the bottom to the top. A stack with this ordering is a **monotonic stack**. The ordering is what makes the work small. The indices that `nums[j]` resolves form the top run of the stack. The scan checks the top, resolves it when `nums[top] < nums[j]`, and stops at the first top that is not smaller. Every index below it holds a value at least as large, so none of them can be smaller either.

#### Each Index Enters And Leaves Once

After the pops, index `j` becomes unresolved and goes on top. This keeps the ordering, because the top that stopped the pops is at least as large as `nums[j]`. The scan pushes each index once and pops it at most once. A single step can pop many indices, but the total number of pops over the whole scan never exceeds `n`.

<!-- stage: variables -->
### What The Scan Keeps

The scan tracks five pieces of state.

- **nums** is the input array, and the scan never changes it.
- **ans** holds one answer per index, and every entry starts at `-1`.
- **stack** holds the unresolved indices, and the values behind them never increase from bottom to top.
- **i** is the index of the value that the scan reads now, which is the resolving value for the pops that follow.
- **top** is the index on top of the stack, and the comparison `nums[top] < nums[i]` decides whether it resolves.

An index that stays on the stack at the end keeps `-1`, because no greater value follows it.

<!-- stage: trace -->
### Following The Stack Through An Array

#### An Array With Distinct Values

The first trace reads 6, 2, 4, 3, 9, 5, 7. The pointer `i` marks the value being read. Each step shows the stack as a list of indices and the answers so far, where `.` means no answer yet.

The 2 and the 4 show the basic move. The 4 is greater than the 2 at the top, so index 1 gets the answer 4 and leaves the stack. The 4 is smaller than the 6 below it, so the pops stop. Later, the 9 resolves three indices in a row, because the values 3, 4 and 6 all lie below it. The last two indices never meet a greater value and keep `-1`.

```trace
{"cells":[6,2,4,3,9,5,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[0]","ans":"[., ., ., ., ., ., .]"},"note":"Index 0 with value 6 goes on top of the stack."},{"at":{"i":1},"vars":{"stack":"[0, 1]","ans":"[., ., ., ., ., ., .]"},"note":"Index 1 with value 2 goes on top of the stack."},{"at":{"i":2},"vars":{"stack":"[0]","ans":"[., 4, ., ., ., ., .]"},"note":"4 is greater than nums[1] = 2, so ans[1] becomes 4 and index 1 leaves the stack."},{"at":{"i":2},"vars":{"stack":"[0, 2]","ans":"[., 4, ., ., ., ., .]"},"note":"Index 2 with value 4 goes on top of the stack."},{"at":{"i":3},"vars":{"stack":"[0, 2, 3]","ans":"[., 4, ., ., ., ., .]"},"note":"Index 3 with value 3 goes on top of the stack."},{"at":{"i":4},"vars":{"stack":"[0, 2]","ans":"[., 4, ., 9, ., ., .]"},"note":"9 is greater than nums[3] = 3, so ans[3] becomes 9 and index 3 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[0]","ans":"[., 4, 9, 9, ., ., .]"},"note":"9 is greater than nums[2] = 4, so ans[2] becomes 9 and index 2 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[]","ans":"[9, 4, 9, 9, ., ., .]"},"note":"9 is greater than nums[0] = 6, so ans[0] becomes 9 and index 0 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[4]","ans":"[9, 4, 9, 9, ., ., .]"},"note":"Index 4 with value 9 goes on top of the stack."},{"at":{"i":5},"vars":{"stack":"[4, 5]","ans":"[9, 4, 9, 9, ., ., .]"},"note":"Index 5 with value 5 goes on top of the stack."},{"at":{"i":6},"vars":{"stack":"[4]","ans":"[9, 4, 9, 9, ., 7, .]"},"note":"7 is greater than nums[5] = 5, so ans[5] becomes 7 and index 5 leaves the stack."},{"at":{"i":6},"vars":{"stack":"[4, 6]","ans":"[9, 4, 9, 9, ., 7, .]"},"note":"Index 6 with value 7 goes on top of the stack."},{"at":{"i":6},"vars":{"stack":"[4, 6]","ans":"[9, 4, 9, 9, ., 7, .]"},"note":"The scan has read the last value. Indices [4, 6] stay on the stack and keep -1."}]}
```

#### An Array With Equal Values

The second trace reads 4, 4, 2, 4, 5 and shows what equality does. The second 4 does not resolve the first, because 4 is not greater than 4. Both indices wait. The third 4 resolves only the 2 on top. The final 5 resolves all three indices that hold a 4.

```trace
{"cells":[4,4,2,4,5],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[0]","ans":"[., ., ., ., .]"},"note":"Index 0 with value 4 goes on top of the stack."},{"at":{"i":1},"vars":{"stack":"[0, 1]","ans":"[., ., ., ., .]"},"note":"Index 1 with value 4 goes on top of the stack."},{"at":{"i":2},"vars":{"stack":"[0, 1, 2]","ans":"[., ., ., ., .]"},"note":"Index 2 with value 2 goes on top of the stack."},{"at":{"i":3},"vars":{"stack":"[0, 1]","ans":"[., ., 4, ., .]"},"note":"4 is greater than nums[2] = 2, so ans[2] becomes 4 and index 2 leaves the stack."},{"at":{"i":3},"vars":{"stack":"[0, 1, 3]","ans":"[., ., 4, ., .]"},"note":"Index 3 with value 4 goes on top of the stack."},{"at":{"i":4},"vars":{"stack":"[0, 1]","ans":"[., ., 4, 5, .]"},"note":"5 is greater than nums[3] = 4, so ans[3] becomes 5 and index 3 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[0]","ans":"[., 5, 4, 5, .]"},"note":"5 is greater than nums[1] = 4, so ans[1] becomes 5 and index 1 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[]","ans":"[5, 5, 4, 5, .]"},"note":"5 is greater than nums[0] = 4, so ans[0] becomes 5 and index 0 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[4]","ans":"[5, 5, 4, 5, .]"},"note":"Index 4 with value 5 goes on top of the stack."},{"at":{"i":5},"vars":{"stack":"[4]","ans":"[5, 5, 4, 5, .]"},"note":"The scan ends. Indices [4] stay on the stack and keep -1."}]}
```

<!-- stage: code -->
### The Stack Loop In Java

#### Answers As Values

The first method returns the next greater value for every index. It declares the stack as a `Deque<Integer>` and uses `push`, `peek` and `pop`, which all work on the same end.

```java
static int[] nextGreaterValues(int[] nums) {
    int[] ans = new int[nums.length];
    Arrays.fill(ans, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < nums.length; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
            ans[stack.pop()] = nums[i];
        }
        stack.push(i);
    }
    return ans;
}
```

#### Answers As Distances

The second method needs the distance to the resolving position, so the stack must hold indices and not values. A value alone cannot give a distance. A value can also appear at several positions, so it cannot name one position.

```java
static int[] daysUntilGreater(int[] temps) {
    int[] wait = new int[temps.length];
    Deque<Integer> stack = new ArrayDeque<>();
    for (int day = 0; day < temps.length; day++) {
        while (!stack.isEmpty() && temps[stack.peek()] < temps[day]) {
            int earlier = stack.pop();
            wait[earlier] = day - earlier;
        }
        stack.push(day);
    }
    return wait;
}
```

Both methods run in O(n) time, because the scan pushes each index once and pops it at most once. They use O(n) extra space for the stack in the worst case, which a decreasing array reaches. In `daysUntilGreater`, an index that never pops keeps the default `0`.

<!-- stage: applicability -->
### When A Waiting Stack Applies

#### The Question That Fits

The method applies when every position needs the first later position whose value crosses a threshold relative to its own value. Greater and smaller are the two common forms. The invariant is that the stack holds exactly the indices that have no answer yet, and their values never increase from bottom to top. A smaller-value question flips the comparison, and the stack then never decreases.

#### Two False Friends

The largest value to the right is a false friend. For the readings 6, 2, 4, 3, 9, the largest value to the right of the 2 is 9, but the next greater value is 4. A running maximum answers a different question.

A sorted structure such as `TreeSet` is the second false friend. It can find the smallest value above `x` among the values seen so far. That value need not come after position `i`, and it need not be the first greater one in position order. The question here is about order of position, and a sorted set forgets that order.

#### When It Does Not Apply

A question about the k-th greater value, or about the next value within a fixed distance, needs different state. Each of those asks for more than the first crossing, so one stack of waiting indices does not hold enough information.

<!-- stage: exercises -->
### Exercises

#### [Build] Next Greater Value (Author exercise)
<!-- id: ms-next-greater-value -->

**Prerequisites.** The stack loop in this lesson.

**Problem.** Let `nums` be an array of non-negative integers. For each index `i`, find the smallest index `j` with `j > i` and `nums[j] > nums[i]`. Return an array `ans` where `ans[i]` equals `nums[j]` for that index, or `-1` when no such index exists.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values with `0 <= nums[i] <= 10^9`, so `-1` is never a real value.
- **Ties** do not count, because the condition is strictly greater.
- **Return** is a new `int[]` of the same length, and `nums` stays unchanged.

**Example 1.** Input `[6,2,4,3,9,5,7]`, output `[9,4,9,9,-1,7,-1]`.

**Example 2.** Input `[5,4,3,2,1]`, output `[-1,-1,-1,-1,-1]`.

**Hint.** Push each index after the pops. Which comparison decides whether the top index gets its answer from the current value?

**Changed decision.** The loop writes each answer at the pop, not at the push.

#### [Vary] Daily Temperatures (LeetCode 739)
<!-- id: ms-daily-temperatures -->

**Prerequisites.** The exercise above and the distance method in this lesson.

**Problem.** Let `temperatures` be an array of daily readings. For each day `i`, return the number of days from day `i` to the first later day with a strictly higher reading. Return `0` for day `i` when no such day exists.

**Constraints.** The limits are:
- **Length** is `1 <= temperatures.length <= 10^5`.
- **Values** are integers with `30 <= temperatures[i] <= 100`.
- **Ties** do not count, because the later reading must be strictly higher.
- **Return** is an `int[]` of the same length, with `0` as the no-answer marker.

**Example 1.** Input `[71,70,75,70,69,72,80,68]`, output `[2,1,4,2,1,1,0,0]`.

**Example 2.** Input `[60,60,61,59,62]`, output `[2,1,2,1,0]`.

**Hint.** The answer is a difference of two positions. What must the stack hold so that the difference is available at the pop?

**Changed decision.** The stack holds indices, and the output records a distance instead of a value.

#### [Boundary] Equal Values Stay Unresolved (Author exercise)
<!-- id: ms-equal-values-stay-unresolved -->

**Prerequisites.** The two exercises above.

**Problem.** Let `nums` be an array of integers. An index `i` is open when no index `j > i` has `nums[j] > nums[i]`. Return the number of open indices. Equal values never make an index closed.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`, and an empty array returns `0`.
- **Values** are `int` values, and repeated values occur.
- **Ties** keep an index open, because only a strictly greater value closes it.
- **Return** is an `int`.

**Example 1.** Input `[2,2,3,3,1]`, output `3`.

**Example 2.** Input `[5,5,5,5]`, output `4`.

**Hint.** Run the stack loop and look at the stack after the last value. What does each remaining index mean?

**Changed decision.** The output is the size of the final stack, and the comparison must treat equality as not resolving.

#### [Recognize] Next Greater Element I (LeetCode 496)
<!-- id: ms-next-greater-element-one -->

**Prerequisites.** The three exercises above.

**Problem.** Array `nums1` is a subset of array `nums2`, and each array has distinct values. For each `x` in `nums1`, find its position in `nums2`. Return the first value to the right of that position in `nums2` that is greater than `x`, or `-1` when none exists.

**Constraints.** The limits are:
- **Lengths** satisfy `1 <= nums1.length <= nums2.length <= 1000`.
- **Values** are integers with `0 <= value <= 10^4`, and no value repeats within one array.
- **Subset** means every value of `nums1` also appears in `nums2`.
- **Return** is an `int[]` with one entry per element of `nums1`, in the same order.

**Example 1.** Input `nums1 = [3,5]`, `nums2 = [5,2,3,8,4]`, output `[8,8]`.

**Example 2.** Input `nums1 = [9,1]`, `nums2 = [1,9,4,7]`, output `[-1,9]`.

**Hint.** Answer every position of `nums2` once. How can a lookup by value then serve each element of `nums1`?

**Changed decision.** The scan covers the reference array, and the queries only read stored answers.
