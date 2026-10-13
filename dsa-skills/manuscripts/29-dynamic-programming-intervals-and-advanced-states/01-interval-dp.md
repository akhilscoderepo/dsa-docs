<!-- lesson-kind: standard -->
<!-- lesson-id: interval-dp -->
## Interval DP

<!-- stage: context -->
### Joining Chunks That Must Stay In Order

A build tool receives four chunk files of 9, 7, 8 and 8 megabytes. It must join them into one file, and the chunks must stay in their given order. Each join of two neighbouring pieces copies every byte of both, so a join of 9 and 7 megabytes costs 16 megabytes of copying. The tool wants the plan with the least total copying.

A developer adds a simple rule: always join the two neighbours with the smallest combined size. On these chunks the rule copies 70 megabytes. Another plan copies only 64 megabytes, and the rule never finds it.

Formally, the input is an array `a` of non-negative sizes. A **merge** replaces two neighbouring pieces with one piece whose size is their sum, and it costs that sum. Repeat merges until one piece remains. Return the smallest total cost. An array with zero or one piece costs 0, and the input array does not change.

This lesson asks how to choose merges when each choice changes which pieces stay neighbours.

<!-- stage: naive -->
### Joining The Cheapest Neighbours First

The simple rule looks at every neighbouring pair, merges the pair with the smallest sum, and repeats. The list shrinks by one piece per round.

```java
static int cheapestFirst(int[] a) {
    List<Integer> pieces = new ArrayList<>();
    for (int x : a) pieces.add(x);
    int total = 0;
    while (pieces.size() > 1) {
        int at = 0;
        for (int i = 1; i + 1 < pieces.size(); i++) {
            if (pieces.get(i) + pieces.get(i + 1) < pieces.get(at) + pieces.get(at + 1)) at = i;
        }
        int sum = pieces.get(at) + pieces.get(at + 1);
        total += sum;
        pieces.set(at, sum);
        pieces.remove(at + 1);
    }
    return total;
}
```

Each round scans the list once and removes one piece, so the rule runs in O(n^2) time with O(n) memory. It is fast, but each merge is final. A cheap early merge can create a large piece that every later merge must copy again.

```predict
Run cheapestFirst on a = [9, 7, 8, 8]. What does it return, and what is the true minimum?

It returns 70. It merges 7 and 8 for 15, then 15 and 8 for 23, then 9 and 23 for 32, and 15 + 23 + 32 is 70. The piece of 15 is copied again in two later merges. Merging 9 with 7 and 8 with 8 costs 16 + 16 + 32, which is 64.
```

<!-- stage: bottleneck -->
### Every Merge Plan Shares Smaller Plans

The correct method looks at the last merge of the whole array. That merge joins a left part and a right part, and each part is a run of neighbouring pieces. The search tries every cut position, solves both parts, and keeps the cheapest total. It stores nothing, so it solves a run again each time a cut produces it.

```predict
The search described above runs on 10 pieces. How many calls does it make, and how many different groups of neighbouring pieces exist among those calls?

It makes 3^9 = 19683 calls. Only 55 different groups of neighbouring pieces exist, because a group is fixed by its first and last piece. The search solves each of the 55 groups about 358 times on average.
```

For n pieces the call count T(n) satisfies T(n) = 1 + 2 * (T(1) + ... + T(n - 1)), which gives T(n) = 3^(n - 1). This is O(3^n) time. For n = 30 it exceeds 10^13 calls.

The cost comes from repetition. A run of pieces from index `l` to index `r` appears inside many different cuts, and every appearance re-solves it from nothing. The answer for that run does not depend on how the pieces outside it were merged. Only n * (n + 1) / 2 different runs exist. If each run is solved once and stored, the work drops to O(n^3), because each of the O(n^2) runs tries at most n cuts. The next section shows what to store and in which order to fill it.

<!-- stage: insight -->
### Solve Every Run By Length

Treat each run of neighbouring pieces as its own small problem, and solve the short runs before the long ones. A run of length 2 needs only runs of length 1, a run of length 3 needs runs of length 1 and 2, and so on.

<!-- names: interval table, split point, base interval -->

#### One Entry For Each Interval

An **interval** `[l, r]` is the pieces `a[l]` through `a[r]`, inclusive. The **interval table** holds `dp[l][r]`, the least cost to merge exactly that interval into one piece. The answer is `dp[0][n - 1]`.

#### The Last Merge Fixes A Split Point

Every plan for `[l, r]` ends with one merge of a left piece and a right piece. The left piece is the merged result of `[l, k]` and the right piece is the merged result of `[k + 1, r]` for some **split point** `k` with `l <= k < r`. The final merge always costs the interval sum, `a[l] + ... + a[r]`, whatever `k` is. The two parts are independent, so the best plan for each part can be chosen separately. Therefore `dp[l][r]` is the minimum over `k` of `dp[l][k] + dp[k + 1][r]`, plus the interval sum.

#### One Piece Needs No Merge

An interval with one piece, `l == r`, is the **base interval**. It is already a single piece, so `dp[l][l] = 0`. The interval sum comes from prefix sums in constant time. The invariant is that `dp[l][r]` describes exactly the interval `[l, r]`, and the recurrence reads only `dp[l][k]` and `dp[k + 1][r]`, which are strictly shorter intervals. Filling the table by increasing length makes every read final.

<!-- stage: variables -->
### Working Values For The Table

The input array stays unchanged, and these working values describe the computation.

- **prefix** is an `int[n + 1]`; `prefix[i]` is the sum of the first `i` sizes, so the interval sum is `prefix[r + 1] - prefix[l]`.
- **dp** is an `int[n][n]`; entry `dp[l][r]` is the least merge cost of the interval from `l` to `r`, and only entries with `l <= r` are used.
- **len** is the number of pieces in the interval, from 2 to n.
- **l** and **r** are the first and last index of the interval, with `r = l + len - 1`.
- **k** is the split point; the left part ends at `k` and the right part starts at `k + 1`.

Java fills a new `int` array with zeros, so every base interval already holds 0. The loop over `len` must be the outer loop. If `l` were the outer loop, `dp[k + 1][r]` would be read before it is final.

<!-- stage: trace -->
### Two Runs Of The Interval Table

#### Beating The Cheapest First Rule

The first run uses the chunks from the opening, `a = [9, 7, 8, 8]`. The table has 4 rows and 4 columns, and the cells below list them row by row, so cell `l * 4 + r` is the entry for the interval from `l` to `r`. The pointer `cell` shows which interval the loop is solving. The variable `sum` is the interval sum, `k` is the cheapest split point and `dp` is the value written.

The three intervals of length 2 each have only one split, and they write 16, 15 and 16. The interval from 0 to 2 compares 15 and 16 and takes the split after 0. The interval from 1 to 3 takes the split after 2. The whole array then compares 38, 32 and 39. The split after 1 wins with 32, so the answer is 32 plus 32, which is 64. The cheapest first rule never makes that split, because it merges 7 and 8 first.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"l":0,"r":0,"sum":0,"k":0,"dp":0},"note":"Every interval with one piece starts at 0, because a single piece needs no merge. The cells for these intervals stay 0 throughout."},{"at":{"cell":1},"vars":{"l":0,"r":1,"sum":16,"k":0,"dp":16},"note":"Interval 0 to 1 has sum 16 and one split, after 0, which gives 0. The entry is 0 plus 16, which is 16."},{"at":{"cell":6},"vars":{"l":1,"r":2,"sum":15,"k":1,"dp":15},"note":"Interval 1 to 2 has sum 15 and one split, after 1, which gives 0. The entry is 0 plus 15, which is 15."},{"at":{"cell":11},"vars":{"l":2,"r":3,"sum":16,"k":2,"dp":16},"note":"Interval 2 to 3 has sum 16 and one split, after 2, which gives 0. The entry is 0 plus 16, which is 16."},{"at":{"cell":2},"vars":{"l":0,"r":2,"sum":24,"k":0,"dp":39},"note":"Interval 0 to 2 has sum 24. The candidates are: split after 0 gives 15; split after 1 gives 16. The cheapest is the split after 0 with 15, so the entry is 15 plus 24, which is 39."},{"at":{"cell":7},"vars":{"l":1,"r":3,"sum":23,"k":2,"dp":38},"note":"Interval 1 to 3 has sum 23. The candidates are: split after 1 gives 16; split after 2 gives 15. The cheapest is the split after 2 with 15, so the entry is 15 plus 23, which is 38."},{"at":{"cell":3},"vars":{"l":0,"r":3,"sum":32,"k":1,"dp":64},"note":"Interval 0 to 3 has sum 32. The candidates are: split after 0 gives 38; split after 1 gives 32; split after 2 gives 39. The cheapest is the split after 1 with 32, so the entry is 32 plus 32, which is 64."}]}
```

#### A Plan That Splits In The Middle

The second run uses `a = [1, 3, 4, 2, 5]`. The table has 25 cells, and the cell for the interval from `l` to `r` is `l * 5 + r`. Intervals of length 2 write 4, 7, 6 and 7. The intervals of length 3 write 12, 15 and 17, and the intervals of length 4 write 20 and 28. The whole array has four candidate splits. The split after 2 gives 19, the smallest, so the answer is 19 plus the sum 15, which is 34. The cheapest first rule returns 35 on this input.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"l":0,"r":0,"sum":0,"k":0,"dp":0},"note":"Every interval with one piece starts at 0, because a single piece needs no merge. The cells for these intervals stay 0 throughout."},{"at":{"cell":1},"vars":{"l":0,"r":1,"sum":4,"k":0,"dp":4},"note":"Interval 0 to 1 has sum 4 and one split, after 0, which gives 0. The entry is 0 plus 4, which is 4."},{"at":{"cell":7},"vars":{"l":1,"r":2,"sum":7,"k":1,"dp":7},"note":"Interval 1 to 2 has sum 7 and one split, after 1, which gives 0. The entry is 0 plus 7, which is 7."},{"at":{"cell":13},"vars":{"l":2,"r":3,"sum":6,"k":2,"dp":6},"note":"Interval 2 to 3 has sum 6 and one split, after 2, which gives 0. The entry is 0 plus 6, which is 6."},{"at":{"cell":19},"vars":{"l":3,"r":4,"sum":7,"k":3,"dp":7},"note":"Interval 3 to 4 has sum 7 and one split, after 3, which gives 0. The entry is 0 plus 7, which is 7."},{"at":{"cell":2},"vars":{"l":0,"r":2,"sum":8,"k":1,"dp":12},"note":"Interval 0 to 2 has sum 8. The candidates are: split after 0 gives 7; split after 1 gives 4. The cheapest is the split after 1 with 4, so the entry is 4 plus 8, which is 12."},{"at":{"cell":8},"vars":{"l":1,"r":3,"sum":9,"k":1,"dp":15},"note":"Interval 1 to 3 has sum 9. The candidates are: split after 1 gives 6; split after 2 gives 7. The cheapest is the split after 1 with 6, so the entry is 6 plus 9, which is 15."},{"at":{"cell":14},"vars":{"l":2,"r":4,"sum":11,"k":3,"dp":17},"note":"Interval 2 to 4 has sum 11. The candidates are: split after 2 gives 7; split after 3 gives 6. The cheapest is the split after 3 with 6, so the entry is 6 plus 11, which is 17."},{"at":{"cell":3},"vars":{"l":0,"r":3,"sum":10,"k":1,"dp":20},"note":"Interval 0 to 3 has sum 10. The candidates are: split after 0 gives 15; split after 1 gives 10; split after 2 gives 12. The cheapest is the split after 1 with 10, so the entry is 10 plus 10, which is 20."},{"at":{"cell":9},"vars":{"l":1,"r":4,"sum":14,"k":2,"dp":28},"note":"Interval 1 to 4 has sum 14. The candidates are: split after 1 gives 17; split after 2 gives 14; split after 3 gives 15. The cheapest is the split after 2 with 14, so the entry is 14 plus 14, which is 28."},{"at":{"cell":4},"vars":{"l":0,"r":4,"sum":15,"k":2,"dp":34},"note":"Interval 0 to 4 has sum 15. The candidates are: split after 0 gives 28; split after 1 gives 21; split after 2 gives 19; split after 3 gives 20. The cheapest is the split after 2 with 19, so the entry is 19 plus 15, which is 34."}]}
```

<!-- stage: code -->
### Filling The Table By Length

The method returns the least total cost. It builds prefix sums first and then fills the table with the shortest intervals first.

```java
static int mergeCost(int[] a) {
    int n = a.length;
    if (n < 2) return 0;
    int[] prefix = new int[n + 1];
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + a[i];
    int[][] dp = new int[n][n];
    for (int len = 2; len <= n; len++) {
        for (int l = 0; l + len <= n; l++) {
            int r = l + len - 1;
            int best = Integer.MAX_VALUE;
            for (int k = l; k < r; k++) {
                best = Math.min(best, dp[l][k] + dp[k + 1][r]);
            }
            dp[l][r] = best + prefix[r + 1] - prefix[l];
        }
    }
    return dp[0][n - 1];
}
```

Time grows as O(n^3), because there are O(n^2) intervals and each tries up to n split points. The table needs O(n^2) memory. An empty array and a single piece return 0 before any table exists. The exercises below change the cost of one merge, the shape of the table and the meaning of the split.

<!-- stage: applicability -->
### Recognizing Problems Built On Intervals

#### Reading The Cue

Use this method when the pieces form a line, the final operation joins two contiguous parts, and the cost of the final operation depends only on the interval. Phrases such as "adjacent", "in order" and "the last one removed or merged" point here. The state is a pair of indexes, and each entry reads shorter intervals of the same line.

#### Checking The Invariant

The invariant says that `dp[l][r]` describes exactly the interval from `l` to `r` and reads only completed shorter intervals. Test a single piece, which must return 0. Test two pieces, which must return their sum. Test sizes that are all 0, which must return 0. Test a case where the cheapest first rule fails, such as the opening chunks, which must return 64.

#### Avoiding The False Friend

The first false friend is the cheapest first rule, which passes any test where the locally cheap merge is also globally cheap. The second is a table filled with `l` as the outer loop, which reads entries that are not final yet. The third is a table that adds the interval sum only at the top level, which undercounts the copies of inner pieces. The method does not apply when any two pieces may merge, not only neighbours, because an interval no longer captures the remaining problem. It also does not fit n above a few thousand, since O(n^3) time becomes too slow.

<!-- stage: exercises -->
### Exercises

#### [Build] Best Split Of A Short Interval (Author exercise)
<!-- id: dp29-short-interval-split -->

**Prerequisites.** The interval table from this lesson.

**Problem.** An array `a` of non-negative sizes and two indexes `l` and `r` are given. Return the least total cost to merge the pieces `a[l]` through `a[r]` into one piece. A merge of two neighbouring pieces costs their sum.

**Constraints.** The limits are:
- **Length** satisfies `1 <= a.length <= 200`.
- **Sizes** satisfy `0 <= a[i] <= 1000`.
- **Indexes** satisfy `0 <= l <= r < a.length`.
- **Mutation** is not allowed, and the result is an `int`.

**Example 1.** Input `a = [9, 7, 8, 8]`, `l = 1`, `r = 3`, output `38`.

**Example 2.** Input `a = [4, 1, 3, 5]`, `l = 0`, `r = 2`, output `12`.

**Hint.** For a given split point, which two shorter intervals does the entry read, and what is added on top?

**Changed decision.** The table covers only the interval from `l` to `r`. The pieces outside it never enter any sum.

#### [Vary] Matrix Chain Cost (Author exercise)
<!-- id: dp29-matrix-chain-cost -->

**Prerequisites.** The exercise above.

**Problem.** An array `dims` of length `n + 1` is given. Matrix `i` has `dims[i]` rows and `dims[i + 1]` columns, for `0 <= i < n`. Multiplying a matrix of shape `p x q` by one of shape `q x s` costs `p * q * s` scalar multiplications. Return the least total cost to multiply all `n` matrices in order. Only the grouping may change.

**Constraints.** The limits are:
- **Length** satisfies `2 <= dims.length <= 150`, so `n` is between 1 and 149.
- **Dimensions** satisfy `1 <= dims[i] <= 100`.
- **Result** fits in an `int`, and `n = 1` returns 0.
- **Mutation** is not allowed.

**Example 1.** Input `dims = [10, 30, 5, 60]`, output `4500`.

**Example 2.** Input `dims = [3, 8, 2, 9, 4]`, output `144`.

**Hint.** When the matrices from `l` to `r` split after `k`, what shape does each side have, and what does the last multiplication cost?

**Changed decision.** The cost of the last merge is `dims[l] * dims[k + 1] * dims[r + 1]` and depends on the split point, so it moves inside the minimum.

#### [Boundary] Empty And Singleton Intervals (Author exercise)
<!-- id: dp29-empty-singleton -->

**Prerequisites.** The two exercises above.

**Problem.** An array `a` of non-negative sizes is given, and it may be empty. Return the least total cost to merge all pieces into one piece, where a merge of two neighbouring pieces costs their sum. An array of zero or one piece needs no merge and costs 0.

**Constraints.** The limits are:
- **Length** satisfies `0 <= a.length <= 300`.
- **Sizes** satisfy `0 <= a[i] <= 100`.
- **Result** is an `int`.
- **Mutation** is not allowed.

**Example 1.** Input `a = []`, output `0`.

**Example 2.** Input `a = [3, 1, 2]`, output `9`.

**Hint.** Which intervals hold 0 before any split is tried, and what would `dp[0][n - 1]` mean for an empty array?

**Changed decision.** The answer must exist for length 0 and length 1, where the table has no interval to fill. The method returns the neutral value 0 directly.

#### [Recognize] Burst Balloons (LeetCode 312)
<!-- id: dp29-burst-balloons -->

**Prerequisites.** All three exercises above.

**Problem.** An array `nums` of `n` balloon values is given. Bursting balloon `i` earns `left * nums[i] * right`, where `left` and `right` are the values of its nearest unburst neighbours. A missing neighbour counts as 1. Return the largest total coins from bursting all balloons in the best order.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 300`.
- **Values** satisfy `0 <= nums[i] <= 100`.
- **Result** fits in an `int`.
- **Mutation** is not allowed.

**Example 1.** Input `nums = [2, 4, 3]`, output `33`.

**Example 2.** Input `nums = [5, 1, 6, 2]`, output `105`.

**Hint.** Choose the balloon that bursts last inside an interval. Which neighbours does it see at that moment?

**Changed decision.** The split is the last balloon removed from an open interval, not the last merge. Its neighbours are the fixed boundary values, so the two sides stay independent.
