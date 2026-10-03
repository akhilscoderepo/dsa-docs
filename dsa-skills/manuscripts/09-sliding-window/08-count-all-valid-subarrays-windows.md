<!-- lesson-kind: standard -->
<!-- lesson-id: count-all-valid-subarrays-windows -->
## Count-All-Valid-Subarrays Windows

<!-- stage: context -->
### Quiet Weeks At The Food Bank

A food bank writes down, every day, how many crates were delivered to its door, and the number is never zero. The director wants a figure for the annual report: in how many runs of consecutive days did the deliveries add up to fewer than twenty crates? A single quiet day counts as a run, and so does a stretch of five slow days, and two runs that start on different days are counted separately even if they end on the same day.

The log covers several years, so the number of runs is huge. The director does not want a list of them, only how many there are. The staff notice that when a run of days is quiet, any shorter run inside it, cut from either end, is quiet too, because it holds fewer crates. That observation looks useful, but nobody has turned it into a plan yet.

<!-- stage: naive -->
### Try Every Run Of Days

The plain approach tries every first day, then extends the run one day at a time while adding up the crates. Each time the total is still under the limit, one more run is counted. Once it reaches the limit, longer runs from that first day can only be bigger, so the inner loop stops.

```java
static int countByStarting(int[] crates, int cap) {
    int runs = 0;
    for (int first = 0; first < crates.length; first++) {
        int sum = 0;
        for (int last = first; last < crates.length; last++) {
            sum += crates[last];
            if (sum >= cap) break;
            runs++;
        }
    }
    return runs;
}
```

It gives the right count on a short log. It keeps the sum in an `int` and the count in an `int`, which is fine for a few thousand days with small deliveries.

<!-- stage: bottleneck -->
### Counting One Run At A Time

When the quiet runs are numerous, this loop visits every one of them to add a single unit, and a log with n days of tiny deliveries has about n squared over two quiet runs. The work is O(n^2) and the answer itself can be that large, so counting by visiting cannot be fast. The staff observation says that visiting is unnecessary: for a fixed last day, the first days that work are not scattered, they form an unbroken tail ending at the last day.

Two facts hide inside that. The earliest first day that still gives a quiet run ending today never moves backward as today moves forward, because adding days only adds crates. And the number of quiet runs ending today is simply the length of that tail, a subtraction and not a loop. Both facts together suggest keeping one marker for the earliest workable first day and adding a whole group of runs to the count at each step, in one operation. The loop that remains has to move the marker, and to keep the daily total up to date as it moves.

<!-- stage: insight -->
### Each Endpoint Adds A Whole Tail

Fix a last day and call the first days that give a quiet run ending there its **valid starts**. Because deliveries are positive, removing days from the front of a run only lowers its total, so the valid starts are a contiguous block that reaches up to the last day itself, unless the last day alone is already too big. Call the front edge of that block the **restored boundary**: the position the left marker returns to after the new day pushes the total over the limit and the marker moves forward to repair it. The block has `last - boundary + 1` members, and that number is what the day adds to the count.

The rule that justifies the shortcut is **monotone validity**: if a run is valid, every run obtained by cutting days from its front, or from its back, is valid too. For counting, only the front cut is used, so the argument is one line long. Cutting the front of a valid run ending at the last day gives another valid run ending at the same day, so no valid start can lie before an invalid one inside the block. Together with the marker's one-way travel, each day is added once and removed at most once.

<!-- names: valid starts, restored boundary, monotone validity -->

The invariant after the repair is that the window from the boundary to the last day is valid, or empty, and that the day before the boundary, as a start for this last day, is not valid. Adding `last - boundary + 1` to the count therefore counts exactly the runs ending at this day, and no run is counted twice, because runs with different last days are different runs.

A caution follows from the same argument. The shortcut quietly assumes that cutting days never breaks validity. With deliveries that can be negative, a run can become quiet after its front day is removed, and the tail is no longer unbroken, so the formula counts wrongly. The same happens when the condition is something like having an exact total, and not an upper bound.

<!-- stage: variables -->
### Marker, Running Total And Tally

`left` is the restored boundary, the earliest first day whose run ending at `right` is still quiet. `right` is the last day, advanced once per iteration. `sum` is the total of the days from `left` to `right`, kept in a `long`, because the individual deliveries are `int` but their total can exceed that range. `runs` is the tally of all quiet runs found so far, also a `long`, since n days can have close to n squared over two runs. When the window shrinks past the last day, `left` equals `right + 1`, the window is empty, and the day contributes `right - left + 1`, which is zero, to the tally.

<!-- stage: trace -->
### Whole Tails Added At Each Step

The first trace counts runs with a total below 7 in the log 3, 1, 2, 6, 1, 1, 4. The first three days all fit, so each adds a growing tail. The step to study is the fourth, where the 6 arrives: the total jumps past the limit, the marker leaps over three days at once, and the tail that remains has length 1.

```trace
{"cells":[3,1,2,6,1,1,4],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"total":3,"added":1,"count":1},"note":"Read position 0. Adding 3 keeps the total under 7, so left stays at 0. Starts 0 to 0 each give a valid stretch ending here, so 1 is added and the count is 1."},{"at":{"left":0,"right":1},"vars":{"total":4,"added":2,"count":3},"note":"Read position 1. Adding 1 keeps the total under 7, so left stays at 0. Starts 0 to 1 each give a valid stretch ending here, so 2 is added and the count is 3."},{"at":{"left":0,"right":2},"vars":{"total":6,"added":3,"count":6},"note":"Read position 2. Adding 2 keeps the total under 7, so left stays at 0. Starts 0 to 2 each give a valid stretch ending here, so 3 is added and the count is 6."},{"at":{"left":3,"right":3},"vars":{"total":6,"added":1,"count":7},"note":"Read position 3. Adding 6 makes the total too large, so drop 3, 1, 2 from the left; left becomes 3. Starts 3 to 3 each give a valid stretch ending here, so 1 is added and the count is 7."},{"at":{"left":4,"right":4},"vars":{"total":1,"added":1,"count":8},"note":"Read position 4. Adding 1 makes the total too large, so drop 6 from the left; left becomes 4. Starts 4 to 4 each give a valid stretch ending here, so 1 is added and the count is 8."},{"at":{"left":4,"right":5},"vars":{"total":2,"added":2,"count":10},"note":"Read position 5. Adding 1 keeps the total under 7, so left stays at 4. Starts 4 to 5 each give a valid stretch ending here, so 2 is added and the count is 10."},{"at":{"left":4,"right":6},"vars":{"total":6,"added":3,"count":13},"note":"Read position 6. Adding 4 keeps the total under 7, so left stays at 4. Starts 4 to 6 each give a valid stretch ending here, so 3 is added and the count is 13."}]}
```

The second trace multiplies instead of adding, with a product limit of 20 on the log 3, 25, 2, 4, 1, 6. The step to study is the second one, where 25 alone reaches the limit: the marker passes it, the window is empty, and the day adds zero. After that the window starts over from the next day.

```trace
{"cells":[3,25,2,4,1,6],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"product":3,"added":1,"count":1},"note":"Read position 0. Multiplying by 3 keeps the product under 20, so left stays at 0. 1 valid stretches end here, and the count is 1."},{"at":{"left":2,"right":1},"vars":{"product":1,"added":0,"count":1},"note":"Read position 1. The value 25 alone reaches 20, so every start is dropped, left becomes 2 and the window is empty. 0 valid stretches end here, and the count is 1."},{"at":{"left":2,"right":2},"vars":{"product":2,"added":1,"count":2},"note":"Read position 2. Multiplying by 2 keeps the product under 20, so left stays at 2. 1 valid stretches end here, and the count is 2."},{"at":{"left":2,"right":3},"vars":{"product":8,"added":2,"count":4},"note":"Read position 3. Multiplying by 4 keeps the product under 20, so left stays at 2. 2 valid stretches end here, and the count is 4."},{"at":{"left":2,"right":4},"vars":{"product":8,"added":3,"count":7},"note":"Read position 4. Multiplying by 1 keeps the product under 20, so left stays at 2. 3 valid stretches end here, and the count is 7."},{"at":{"left":4,"right":5},"vars":{"product":6,"added":2,"count":9},"note":"Read position 5. Multiplying by 6 makes the product too large, so divide out 2, 4; left becomes 4. 2 valid stretches end here, and the count is 9."}]}
```

<!-- stage: code -->
### Three Windows That Count Tails

```java
static long countQuietRuns(int[] crates, int cap) {
    long runs = 0, sum = 0;
    int left = 0;
    for (int right = 0; right < crates.length; right++) {
        sum += crates[right];
        while (left <= right && sum >= cap) sum -= crates[left++];
        runs += right - left + 1;
    }
    return runs;
}

static long countProductBelow(int[] values, long limit) {
    if (limit <= 1) return 0;
    long product = 1, runs = 0;
    int left = 0;
    for (int right = 0; right < values.length; right++) {
        product *= values[right];
        while (product >= limit) product /= values[left++];
        runs += right - left + 1;
    }
    return runs;
}

static long countAtMostOneZero(int[] values) {
    long runs = 0;
    int zeros = 0, left = 0;
    for (int right = 0; right < values.length; right++) {
        if (values[right] == 0) zeros++;
        while (zeros > 1) if (values[left++] == 0) zeros--;
        runs += right - left + 1;
    }
    return runs;
}
```

Each index enters the window once and leaves at most once, so the work is O(n) time with O(1) extra space, even though the answer may be of order n squared. The product version requires positive values, so dividing by the departing value is exact, and the early return for a limit of at most one is what keeps the loop from running past the end.

<!-- stage: applicability -->
### Telling When Counting Can Be Batched

Ask for a count of ranges, and ask whether a valid range stays valid when its first element is cut away. If both answers are yes, the number of valid ranges ending at each position is the window length after repair, and the whole count is a sum of those lengths. State the invariant before coding: after repair, every start in the window works and the start just before it does not.

A false friend is the same problem with a condition that cutting can break. An exact target sum with negative numbers is the usual offender, since removing a front element can move the total either way, and the marker no longer travels in one direction. Another is a question for the longest or shortest range, where you keep a maximum or a minimum and never need the tail. A third is the count of ranges with exactly k of something, which is usually computed as the count for at most k minus the count for at most k minus one.

In Java, declare the tally as `long` from the start, because int overflow in a counter is silent and wraps to a negative number. Write the repair loop with a guard against the marker passing the right edge, and test with a limit so small that every range is invalid, where the answer is zero and the window is empty after every step.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Subarrays With At Most One Zero (Author exercise)
<!-- id: sw-one-zero -->

**Prerequisites.** The idea of a window whose left marker only moves forward.

**Problem.** Given an array of integers, return how many contiguous subarrays contain at most one zero. Two subarrays with different start or end positions are different, even when their contents are equal. At each right end add the number of starts that still work.

**Constraints.** 0 <= nums.length <= 100000 and any `int` values. The answer can exceed the `int` range, so return a `long`.

**Example 1.** Input `nums = [1, 0, 2, 0, 3]`, output 11.

**Example 2.** Input `nums = [0, 0, 0]`, output 3.

**Hint.** If a run ending at `right` is fine, which runs ending at `right` are also fine? What event forces the left marker to move?

**Changed decision.** First rung: the condition is a count of zeros and not a total, and the tail length is added at every right end.

#### [Vary] Count Subarrays With Sum Below K For Positive Values (Author exercise)
<!-- id: sw-sum-below-k -->

**Prerequisites.** The at-most-one-zero exercise above.

**Problem.** Given an array of positive integers and an integer `k`, return the number of contiguous subarrays whose sum is strictly less than `k`. The array may not be changed. Positivity is what lets you say that dropping a front element cannot raise the sum.

**Constraints.** 0 <= nums.length <= 100000, 1 <= nums[i] <= 2000000000, and 0 <= k <= 2147483647. Totals and the count can exceed `int`, so use `long`.

**Example 1.** Input `nums = [2, 1, 3, 1], k = 5`, output 7.

**Example 2.** Input `nums = [5, 5], k = 6`, output 2.

**Hint.** Where does the left marker stop after the repair? Why would the same method fail if some elements were negative?

**Changed decision.** The check is a running total that must stay below a limit, so monotone validity now rests on positivity.

#### [Boundary] K At The Minimum (Author exercise)
<!-- id: sw-k-at-minimum -->

**Prerequisites.** The sum-below-k exercise above.

**Problem.** For an array of positive integers and a limit `k`, return a pair: the number of subarrays with sum strictly below `k`, and the number of right ends at which the repaired window is empty. The limit may be as small as 0 or 1, in which case no subarray is valid at all.

**Constraints.** 0 <= nums.length <= 100000, 1 <= nums[i] <= 1000000, and 0 <= k <= 1000000000. The left marker must never run past `right + 1`.

**Example 1.** Input `nums = [4, 1, 7], k = 2`, output `[1, 2]`.

**Example 2.** Input `nums = [3, 3], k = 1`, output `[0, 2]`.

**Hint.** What condition stops the repair loop when the window has become empty? What does an empty window add to the count?

**Changed decision.** The window is allowed to shrink all the way to empty, and the contribution of such a step is exactly zero.

#### [Recognize] Subarray Product Less Than K (LeetCode 713)
<!-- id: sw-product-less-than-k -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array of positive integers and an integer `k`, return the number of contiguous subarrays whose product is strictly less than `k`. Use a window with a running product and add the number of valid starts for each right end.

**Constraints.** 0 <= nums.length <= 30000, 1 <= nums[i] <= 100000, and 0 <= k <= 1000000000. The running product can exceed `int` before it is repaired.

**Example 1.** Input `nums = [4, 2, 3, 1, 6], k = 25`, output 13.

**Example 2.** Input `nums = [7, 9], k = 1`, output 0.

**Hint.** What do you do with the product when the left element leaves? When is the limit so small that the answer is known without looping?

**Changed decision.** The running quantity is multiplied and divided and not added and subtracted, and a limit of one or less is an early exit.
