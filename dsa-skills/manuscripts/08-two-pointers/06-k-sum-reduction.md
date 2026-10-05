<!-- lesson-kind: standard -->
<!-- lesson-id: k-sum-reduction -->
## Fix Values Then Scan A Pair

<!-- stage: context -->
### Three Payments That Settle One Invoice

An accounting tool reconciles an invoice against a list of 3,000 payments. It looks for three payments that add up to the invoice total. The first version tries every triple. That is 4.5 billion triples, and the reconciliation job runs for minutes on one invoice. The same tool must also handle four payments for large invoices, and the number of combinations grows again.

Each triple has one free value after the other two are fixed. The question is how the pair scan from earlier lessons can take over the last two choices, so that only the first choices need a loop.

<!-- stage: naive -->
### One Nested Loop For Each Payment

The direct method uses one loop for each value in the combination. For three values it checks every triple of indexes `i < j < k`.

```java
static long countTriplesSlow(int[] nums, long target) {
    long count = 0;
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            for (int k = j + 1; k < nums.length; k++) {
                if ((long) nums[i] + nums[j] + nums[k] == target) count++;
            }
        }
    }
    return count;
}
```

For `[-4, -1, -1, 0, 1, 2]` and target 0, the method returns 3. The method needs no sorted order, and it is correct for every input. A fourth value would need a fourth loop, and each extra value multiplies the cost by `n`.

```predict
The list holds 3,000 payments. How many index triples does `countTriplesSlow` examine, and how many would a version for four payments examine?

It examines 3,000 * 2,999 * 2,998 / 6, about 4.5 billion triples. A version for four payments examines about 3,000^4 / 24, which is about 3.4 trillion quadruples. The cost is O(n^3) for triples and O(n^4) for quadruples.
```

<!-- stage: bottleneck -->
### The Innermost Loop Searches For One Value

After `i` and `j` are fixed, the innermost loop looks for a value equal to a known number. It tries every later index in turn. That search repeats for each pair `(i, j)`, so the method pays O(n) for work that a sorted array can answer by elimination. The total is O(n^3).

The innermost loop is a two-sum question in disguise. The earlier lesson already solved the question of finding a pair with a given sum in one pass over a sorted array. The method reuses none of that.

<!-- stage: insight -->
### Fix Values, Then Hand Over A Pair

#### One Reduction Per Fixed Value

A **reduction** turns a problem with `k` values into a smaller problem. Fixing `nums[i]` as the first value turns a `k`-value search with target `t` into a `(k - 1)`-value search with the **remaining target** `t - nums[i]`, over the indexes after `i`. Starting the search just after `i` never reuses an earlier index, and the sorted order of the array lets the pair scan work on that suffix.

#### The Base Case Is The Pair Scan

The **base case** is `k = 2`. A search for two values with a given target runs the opposite-end scan on the sorted suffix in O(n) time. The scan moves `left` when the sum is too small and `right` when it is too large. This is the elimination argument of the first lesson, applied to the indexes after the last fixed value.

<!-- names: reduction, remaining target, base case -->

#### The Cost Of The Reduction

Three values need one loop and one pair scan, so the cost is O(n^2). Four values need two loops and one pair scan, so the cost is O(n^3). In general `k` values cost O(n^(k-1)), because the base case saves one factor of `n`. Counting index combinations adds one more idea. When the scan finds a match, the number of index pairs behind it comes from the lengths of the two runs of equal values, so a counting scan never needs to look at each copy.

<!-- stage: variables -->
### What Each Level Of The Reduction Holds

A reduction with `k` levels keeps the following state.

- **start** is the first index that the current level may use, and each deeper level starts one index after the fixed value.
- **k** is the number of values still missing from the combination.
- **target** is the sum that the missing values must reach, and it equals the original target minus the fixed values.
- **left** and **right** are the pair scan indexes at the base case, and both stay at or after `start`.

The sum of the fixed values and the final pair equals the original target. Each level reads only its own `start`, `k` and `target`.

<!-- stage: trace -->
### Two Reductions On Sorted Arrays

#### Counting Index Triples

The input is `[-4, -1, -1, 0, 1, 2]` and the target is 0. The loop fixes `nums[i]`, and the pair scan then looks for the remaining target in the indexes after `i`. When two runs match, the scan adds the product of their lengths to the count. The fixed index moves right after each pair scan ends, and the remaining target changes with it.

```trace
{"cells":[-4,-1,-1,0,1,2],"pointers":["i","left","right"],"steps":[{"at":{"i":0,"left":1,"right":5},"vars":{"remaining":"4","sum":"1","count":"0"},"note":"The pair sum 1 is below the remaining target 4, so left moves right."},{"at":{"i":0,"left":2,"right":5},"vars":{"remaining":"4","sum":"1","count":"0"},"note":"The pair sum 1 is below the remaining target 4, so left moves right."},{"at":{"i":0,"left":3,"right":5},"vars":{"remaining":"4","sum":"2","count":"0"},"note":"The pair sum 2 is below the remaining target 4, so left moves right."},{"at":{"i":0,"left":4,"right":5},"vars":{"remaining":"4","sum":"3","count":"0"},"note":"The pair sum 3 is below the remaining target 4, so left moves right."},{"at":{"i":1,"left":2,"right":5},"vars":{"remaining":"1","sum":"1","count":"1"},"note":"The pair sum matches. The run of -1 has length 1 and the run of 2 has length 1, so the count grows by 1."},{"at":{"i":1,"left":3,"right":4},"vars":{"remaining":"1","sum":"1","count":"2"},"note":"The pair sum matches. The run of 0 has length 1 and the run of 1 has length 1, so the count grows by 1."},{"at":{"i":2,"left":3,"right":5},"vars":{"remaining":"1","sum":"2","count":"2"},"note":"The pair sum 2 is above the remaining target 1, so right moves left."},{"at":{"i":2,"left":3,"right":4},"vars":{"remaining":"1","sum":"1","count":"3"},"note":"The pair sum matches. The run of 0 has length 1 and the run of 1 has length 1, so the count grows by 1."},{"at":{"i":3,"left":4,"right":5},"vars":{"remaining":"0","sum":"3","count":"3"},"note":"The pair sum 3 is above the remaining target 0, so right moves left."}]}
```

#### Keeping The Closest Total

The input is `[-4, -1, 1, 2]` and the target is 1. The scan has no exact match, so it keeps the total with the smallest distance to the target. The pair scan still moves by comparing the total with the target. The best total changes only when a new total is closer to the target, and it ends at 2.

```trace
{"cells":[-4,-1,1,2],"pointers":["i","left","right"],"steps":[{"at":{"i":0,"left":1,"right":3},"vars":{"sum":"-3","best":"-3"},"note":"The total -3 is below 1, so left moves right. The best total is -3."},{"at":{"i":0,"left":2,"right":3},"vars":{"sum":"-1","best":"-1"},"note":"The total -1 is below 1, so left moves right. The best total is -1."},{"at":{"i":1,"left":2,"right":3},"vars":{"sum":"2","best":"2"},"note":"The total 2 is above 1, so right moves left. The best total is 2."}]}
```

<!-- stage: code -->
### The Reduction In Java

```java
static long countKSum(int[] a, int start, int k, long target) {
    if (k == 2) return countPairs(a, start, target);
    long total = 0;
    for (int i = start; i + k <= a.length; i++) {
        total += countKSum(a, i + 1, k - 1, target - a[i]);
    }
    return total;
}

static long countPairs(int[] a, int start, long target) {
    int left = start, right = a.length - 1;
    long count = 0;
    while (left < right) {
        long sum = (long) a[left] + a[right];
        if (sum < target) left++;
        else if (sum > target) right--;
        else if (a[left] == a[right]) {
            long m = right - left + 1;
            return count + m * (m - 1) / 2;
        } else {
            int x = a[left], y = a[right];
            long runX = 0, runY = 0;
            while (left <= right && a[left] == x) { left++; runX++; }
            while (right >= left && a[right] == y) { right--; runY++; }
            count += runX * runY;
        }
    }
    return count;
}
```

The array must be sorted before the first call. The target and the sums are `long`, because several values near `10^9` can exceed the `int` range. When the two ends hold equal values, every value between them is equal too, so the pairs inside that block number `m * (m - 1) / 2`. The loop bound `i + k <= a.length` leaves enough later indexes for the remaining `k - 1` values.

<!-- stage: applicability -->
### When Reduction Fits

#### The Invariant

The invariant is that the count at each level equals the number of index combinations that start at `start` and sum to `target`. Fixing one value splits those combinations by their first index, and each part equals a smaller count with a smaller target. The base case is exact, so the sum of the parts is exact.

#### The False Friend

The nearest wrong idea is to hash the first values instead of fixing them. A hash set finds one missing value in O(1), but it gives no pointer movement and needs care with repeated values. A second false friend is a pair scan after fixing both ends of a window in an unsorted array. The scan needs the sorted order of the suffix, and a sort that changes indexes loses the original positions.

#### Conditions That Break The Fit

The method needs a sorted array and a sum that grows when a value grows. For a product, the order flips around negative values, and the elimination argument fails. The cost O(n^(k-1)) also grows fast with `k`, so values of `k` above four need another method, such as a meet in the middle search.

<!-- stage: exercises -->
### Exercises

#### [Build] 3Sum (LeetCode 15)
<!-- id: tp-three-sum-count -->

**Prerequisites.** The reduction of this lesson and the pair scan of the first lesson.

**Problem.** Take an integer array `nums` and a `long` target. Return the number of index triples `i < j < k` with `nums[i] + nums[j] + nums[k] = target`. Equal values at different indexes count as different triples. This version counts index triples, while the original problem lists distinct value triplets.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 3000`; the empty array is valid.
- **Values** are `int` values with `|nums[i]| <= 10^9`, in any order.
- **Target** is a `long`.
- **Return type** is `long`, because the count can exceed the `int` range.

**Example 1.** Input `nums = [-1,0,1,2,-1,-4]` and `target = 0`, output 3.

**Example 2.** Input `nums = [0,0,0,0]` and `target = 0`, output 4.

**Hint.** Sort a copy first. When the two scan ends hold different values, how many index pairs does one match stand for?

**Changed decision.** The scan counts index combinations, so it counts whole runs by their lengths and does not list one representative.

#### [Vary] 3Sum Closest (LeetCode 16)
<!-- id: tp-three-sum-closest -->

**Prerequisites.** The first exercise above.

**Problem.** Take an integer array `nums` with at least three values and an integer `target`. Return the sum of three values at different indexes that is closest to `target`. A tie in distance goes to the smaller sum.

**Constraints.** The limits are:
- **Length** is `3 <= nums.length <= 1000`.
- **Values** are `int` values with `|nums[i]| <= 10^6`, in any order.
- **Target** is an `int` with `|target| <= 10^7`.
- **Mutation** of the input does not occur.

**Example 1.** Input `nums = [-4,-1,1,2]` and `target = 1`, output 2.

**Example 2.** Input `nums = [1,3,5,7]` and `target = 10`, output 9, because the sums 9 and 11 are equally close.

**Hint.** Which total do you keep, and which pointer moves when the total equals the target?

**Changed decision.** No exact match is guaranteed, so the scan keeps the best candidate while it follows the same pointer rule.

#### [Boundary] Overflowing Sum (Author exercise)
<!-- id: tp-overflowing-sum -->

**Prerequisites.** The Java remark in the code stage of this lesson.

**Problem.** Take a sorted integer array `nums` and a `long` target. Return `true` when three values at different indexes sum to `target`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 3000`; the empty array is valid.
- **Values** are `int` values over the full `int` range, sorted in nondecreasing order.
- **Target** is a `long`.
- **Arithmetic** must not wrap: three values near `2^31` need a `long` sum.

**Example 1.** Input `nums = [2,2147483647,2147483647]` and `target = 0`, output `false`.

**Example 2.** Input `nums = [2147483647,2147483647,2147483647]` and `target = 6442450941`, output `true`.

**Hint.** What is `2147483647 + 2147483647 + 2` in `int` arithmetic?

**Changed decision.** The sum can leave the `int` range, so every addition widens to `long` first.

#### [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-count -->

**Prerequisites.** All exercises above.

**Problem.** Count the index quadruples `i < j < k < l` of an integer array `nums` with `nums[i] + nums[j] + nums[k] + nums[l] = target`, where `target` is a `long`. Equal values at different indexes count as different quadruples.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 200`.
- **Values** are `int` values with `|nums[i]| <= 10^9`, in any order.
- **Target** is a `long` with `|target| <= 4 * 10^9`.
- **Return type** is `long`.

**Example 1.** Input `nums = [1,0,-1,0,-2,2]` and `target = 0`, output 3.

**Example 2.** Input `nums = [2,2,2,2,2]` and `target = 8`, output 5.

**Hint.** Fix two values with two loops, and reuse the pair scan at the end. What does the recursion pass to the next level?

**Changed decision.** A second fixed value adds one level to the reduction, and the pair scan stays the same.
