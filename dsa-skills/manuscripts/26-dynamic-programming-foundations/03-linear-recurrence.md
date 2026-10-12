<!-- lesson-kind: standard -->
<!-- lesson-id: linear-recurrence -->
## Linear Recurrence

<!-- stage: context -->
### Counting Request Sequences For An Upload

An upload client cuts a file into n equal blocks. Each network request carries either one block or two consecutive blocks. A test engineer wants to know how many different request sequences can deliver the file. For n = 4 blocks the engineer lists five sequences by hand: 1+1+1+1, 1+1+2, 1+2+1, 2+1+1 and 2+2. For n = 40 blocks the list is far too long to write, and a loop that builds every sequence takes minutes.

A **sequence** here is an ordered list of request sizes, each 1 or 2, that adds up to n. The task is to return how many sequences exist for a given n, where n is between 0 and 45. The empty sequence counts as one sequence for n = 0. The method reads only the integer n and changes nothing.

This lesson asks how the answer for 40 blocks can come from the answers for smaller block counts, with no enumeration at all.

<!-- stage: naive -->
### Counting By Calling Itself Twice

The direct idea is to reason about the last request of a sequence. A sequence for n blocks ends with a request of size 1 or size 2. Removing that request leaves a sequence for n - 1 or n - 2 blocks. So `count(n)` calls `count(n - 1)` and `count(n - 2)` and adds the two results.

```java
static int count(int n) {
    if (n <= 1) return 1;
    return count(n - 1) + count(n - 2);
}
```

The method returns correct answers, and it matches the hand count of five for n = 4. Each call that is not a base call starts two more calls, and a call with n of 0 or 1 returns 1 at once.

```predict
For n = 5, how many calls to count happen in total, including the first call, and how many of them compute a value that an earlier call already computed?

The total is 15 calls, which return the answer 8. Only 6 calls have a new argument, namely n = 5, 4, 3, 2, 1 and 0. The other 9 calls repeat an argument that an earlier call already solved. For example, count(3) runs twice and count(2) runs three times.
```

<!-- stage: bottleneck -->
### The Same Argument Is Solved Again

Each call to `count` with n of 2 or more starts two calls, so the number of calls grows by a factor of about 1.6 with every extra block. The call count for n = 5 is 15, and for n = 40 it is more than 300 million. The growth is exponential, and the bound O(2^n) holds as a loose upper limit. The answer for n = 45 would take several seconds on a laptop.

The waste is visible in the call tree. The calls fall on only n + 1 different arguments, from 0 to n, yet the tree has far more than n + 1 nodes. Every node with an argument that appeared earlier recomputes a value that is already known.

A usable method must compute the value for each argument exactly once and in an order where every needed value already exists. The needed values here are always the two arguments directly below the current one. That regular shape means a plain loop from small n to large n can do the job in O(n) time. The next section turns that observation into a table.

<!-- stage: insight -->
### Fill A Table From The Smallest Case

The answer for n depends only on the answers for n - 1 and n - 2. So a loop can compute the answers in increasing order of n and keep each one in an array.

<!-- names: recurrence, base case, window -->

#### One Entry Means One Question

Let `ways[i]` be the number of sequences that add up to exactly `i` blocks. This sentence is the whole definition of the table. Every entry answers the same question for a different size, and the final answer is `ways[n]`.

#### The Recurrence Reads Two Earlier Entries

A **recurrence** is a rule that computes one entry from entries with smaller indexes. Here the rule is `ways[i] = ways[i - 1] + ways[i - 2]`. A sequence for `i` blocks ends with a request of size 1, which leaves one of the `ways[i - 1]` shorter sequences, or ends with a request of size 2, which leaves one of the `ways[i - 2]` shorter sequences. No sequence is counted twice, because the last request differs between the two groups.

#### Base Cases Start The Table

The rule cannot compute `ways[0]` or `ways[1]`, because it would read negative indexes. A **base case** is an entry that is set directly from the problem statement. `ways[0]` is 1, because the empty sequence adds up to 0 blocks. `ways[1]` is 1, because only the request 1 fits. Every later entry is then well defined.

#### The Window Has Fixed Width

The **window** of a recurrence is the set of earlier entries that one entry reads. This window always holds the last two entries, so its width is 2. A fixed window gives the invariant of the method. Before the loop computes `ways[i]`, the entries `ways[i - 1]` and `ways[i - 2]` are already final. The same loop shape works for any recurrence with a fixed window, and only the number of base cases and the combining operation change.

<!-- stage: variables -->
### The Table, The Index, And The Window

The method reads one integer `n`, with `0 <= n <= 45`, and changes nothing. It keeps two working values.

- **ways** is an `int[]` of length `n + 2`; entry `i` holds the count of sequences that add up to `i` blocks.
- **i** is the loop index from 2 to `n`; every entry below `i` is final when the loop reaches `i`.

The array has two extra slots, so the base cases `ways[0]` and `ways[1]` exist even when `n` is 0. The count for n = 45 is 1836311903, which fits in an `int`. The count for n = 46 is 2971215073, which exceeds `Integer.MAX_VALUE` and wraps to a negative number, so the limit of 45 protects the type.

<!-- stage: trace -->
### Two Tables Built Left To Right

#### Counting Sequences Up To Eight Blocks

The first table sets `ways[0]` and `ways[1]` to 1 and then fills the entries up to 8. Each cell is one entry of the table, and the pointer `i` marks the entry that the loop has just completed. The variable `left` holds `ways[i - 2]`, and `right` holds `ways[i - 1]`, which are the two entries read by the step.

The values grow as 1, 1, 2, 3, 5, 8, 13, 21, 34. Each value equals the sum of the two before it, so the final answer for 8 blocks is 34 sequences.

```trace
{"cells":["ways[0]","ways[1]","ways[2]","ways[3]","ways[4]","ways[5]","ways[6]","ways[7]","ways[8]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"left":0,"right":0},"note":"The base case ways[0] is 1, because the empty sequence adds up to 0 blocks."},{"at":{"i":1},"vars":{"left":0,"right":1},"note":"The base case ways[1] is 1, because only the request of size 1 fits."},{"at":{"i":2},"vars":{"left":1,"right":1},"note":"The entry ways[2] is 1 + 1, which equals 2."},{"at":{"i":3},"vars":{"left":1,"right":2},"note":"The entry ways[3] is 1 + 2, which equals 3."},{"at":{"i":4},"vars":{"left":2,"right":3},"note":"The entry ways[4] is 2 + 3, which equals 5."},{"at":{"i":5},"vars":{"left":3,"right":5},"note":"The entry ways[5] is 3 + 5, which equals 8."},{"at":{"i":6},"vars":{"left":5,"right":8},"note":"The entry ways[6] is 5 + 8, which equals 13."},{"at":{"i":7},"vars":{"left":8,"right":13},"note":"The entry ways[7] is 8 + 13, which equals 21."},{"at":{"i":8},"vars":{"left":13,"right":21},"note":"The entry ways[8] is 13 + 21, which equals 34."}]}
```

#### Lowest Cost Of Climbing Seven Steps

The second table changes the question and keeps the window. A staircase has seven steps with leaving costs `[10, 15, 20, 5, 10, 25, 5]`. The climber starts on step 0 or step 1 at no cost, pays the cost of a step to leave it, and moves up by one or two steps. The goal is to stand above the last step. Here `dp[i]` is the lowest total cost to stand on position `i`, and position 7 is the top.

Each entry is the smaller of two sums, one from each window entry. The variable `viaOne` is `dp[i - 1] + cost[i - 1]`, and `viaTwo` is `dp[i - 2] + cost[i - 2]`. The answer is `dp[7]`, which equals 35 for these prices.

```trace
{"cells":["dp[0]","dp[1]","dp[2]","dp[3]","dp[4]","dp[5]","dp[6]","dp[7]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"viaOne":0,"viaTwo":0},"note":"Position 0 is a free start, so dp[0] is 0."},{"at":{"i":1},"vars":{"viaOne":0,"viaTwo":0},"note":"Position 1 is also a free start, so dp[1] is 0."},{"at":{"i":2},"vars":{"viaOne":15,"viaTwo":10},"note":"The two sums are 15 and 10, so dp[2] is 10."},{"at":{"i":3},"vars":{"viaOne":30,"viaTwo":15},"note":"The two sums are 30 and 15, so dp[3] is 15."},{"at":{"i":4},"vars":{"viaOne":20,"viaTwo":30},"note":"The two sums are 20 and 30, so dp[4] is 20."},{"at":{"i":5},"vars":{"viaOne":30,"viaTwo":20},"note":"The two sums are 30 and 20, so dp[5] is 20."},{"at":{"i":6},"vars":{"viaOne":45,"viaTwo":30},"note":"The two sums are 45 and 30, so dp[6] is 30."},{"at":{"i":7},"vars":{"viaOne":35,"viaTwo":45},"note":"The two sums are 35 and 45, so dp[7] is 35."}]}
```

<!-- stage: code -->
### Two Methods With One Loop Shape

The first method counts sequences, and the second method finds the lowest climbing cost. Both fill a table from the base cases up to the target index.

```java
static int countSequences(int n) {
    int[] ways = new int[n + 2];
    ways[0] = 1;
    ways[1] = 1;
    for (int i = 2; i <= n; i++) {
        ways[i] = ways[i - 1] + ways[i - 2];
    }
    return ways[n];
}

static int lowestClimbCost(int[] cost) {
    int n = cost.length;
    int[] dp = new int[n + 1];
    for (int i = 2; i <= n; i++) {
        dp[i] = Math.min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]);
    }
    return dp[n];
}
```

The table in `lowestClimbCost` has `n + 1` entries, and its base cases `dp[0]` and `dp[1]` stay 0 because Java zero-fills a new array. Both loops run in O(n) time and use O(n) memory. For `countSequences`, the extra slot makes `ways[1]` legal when n is 0.

<!-- stage: applicability -->
### Recognizing A Fixed Window

#### Reading The Cue

Use this method when a statement defines a result for position `i` through a fixed number of earlier positions. Typical wording says that a move covers one or two steps, or that each term is the sum of the previous three. The answer can be a count, a minimum, or a maximum, and the loop shape stays the same.

#### Checking The Invariant

An **invariant** is a statement that holds before and after every loop step. Here, before the loop computes `dp[i]`, every entry the recurrence reads is final and describes a complete subproblem. Test the smallest inputs first. For n = 0 and n = 1, no loop iteration runs, and the base cases must already hold the right answers. Test the largest allowed n to check that the type does not overflow.

#### Avoiding The False Friend

A **false friend** is a method that looks correct yet returns wrong answers or runs too long on some inputs. The plain recursive call from the naive section is one, because it is correct and exponentially slow. A closed formula for the Fibonacci numbers with `Math.pow` and `double` is another. It rounds wrongly for large n, and it does not extend to costs or minima. A third is a greedy choice, such as always taking the cheaper next step. That choice ignores that a cheap step can lead to an expensive one two positions later.

<!-- stage: exercises -->
### Exercises

#### [Build] Climbing Stairs (LeetCode 70)
<!-- id: dp-linrec-climb-stairs -->

**Prerequisites.** The table and the recurrence of this lesson.

**Problem.** A staircase has `n` steps. A climber moves up by exactly 1 or exactly 2 steps per move and must land exactly on step `n`. A way is an ordered list of moves that reaches step `n` from step 0. Return the number of distinct ways as an `int`.

**Constraints.** The limits are:
- **Steps** satisfy `1 <= n <= 45`.
- **Result** fits in an `int` for every allowed `n`.
- **Mutation** does not apply, because the only input is an integer.

**Example 1.** Input `n = 4`, output `5`.

**Example 2.** Input `n = 7`, output `21`.

**Hint.** The last move lands on step `n` from step `n - 1` or from step `n - 2`. What does each case count?

**Changed decision.** The method defines `ways[i]` as the number of move lists that reach step `i`. It sets `ways[0]` to 1 for the empty list and builds the table upward.

#### [Vary] Min Cost Climbing Stairs (LeetCode 746)
<!-- id: dp-linrec-min-cost-climb -->

**Prerequisites.** The exercise above.

**Problem.** An array `cost` holds the price of leaving each step. The climber may start on step 0 or step 1 and pays `cost[i]` each time it leaves step `i`. A move goes up by 1 or 2 steps. The top is the position `cost.length`, one past the last step. Return the smallest sum of prices paid on any route that ends at the top.

**Constraints.** The limits are:
- **Length** satisfies `2 <= cost.length <= 1000`.
- **Price** satisfies `0 <= cost[i] <= 999`.
- **Mutation** is not allowed, because the input array stays unchanged.
- **Result** is an `int`.

**Example 1.** Input `cost = [4,2,9,1,7]`, output `3`.

**Example 2.** Input `cost = [5,5]`, output `5`.

**Hint.** In the second example, which two starting steps reach the top, and what does each start pay?

**Changed decision.** The method replaces the sum of two counts with the minimum of two sums, each made from a window entry and a price. The base cases `dp[0]` and `dp[1]` are both 0 because either start is free.

#### [Boundary] Short Arrays (Author exercise)
<!-- id: dp-linrec-short-arrays -->

**Prerequisites.** The two exercises above.

**Problem.** An array `gain` holds a value for each cell. A path starts at cell 0 or cell 1, moves forward by 1 or 2 cells per move, and ends exactly on the last cell. The score of a path is the sum of `gain` over all cells that the path visits, including the first and last. Return the highest score. A cell that does not exist is not a legal start, and an empty array returns 0.

**Constraints.** The limits are:
- **Length** satisfies `0 <= gain.length <= 1000`.
- **Value** satisfies `-1000 <= gain[i] <= 1000`.
- **Start** is cell 0 or cell 1, and only existing cells qualify.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `gain = [-3,8]`, output `8`.

**Example 2.** Input `gain = [2,-7,4,-1,5]`, output `11`.

**Hint.** For one cell, which start is legal? For two cells, can the path begin on cell 1, and what does that skip?

**Changed decision.** The method does not copy the stairs base cases. Cell 1 can be a start, so its entry adds `max(0, dp[0])`, where 0 stands for a path that begins there. The method returns 0 before it reads any cell of an empty array.

#### [Recognize] N-th Tribonacci Number (LeetCode 1137)
<!-- id: dp-linrec-tribonacci -->

**Prerequisites.** All three exercises above.

**Problem.** Define `T(0) = 0`, `T(1) = 1`, `T(2) = 1`, and `T(n) = T(n - 1) + T(n - 2) + T(n - 3)` for `n >= 3`. Given `n`, return `T(n)` as an `int`.

**Constraints.** The limits are:
- **Index** satisfies `0 <= n <= 37`.
- **Result** fits in an `int` for every allowed `n`.
- **Mutation** does not apply, because the only input is an integer.

**Example 1.** Input `n = 5`, output `7`.

**Example 2.** Input `n = 0`, output `0`.

**Hint.** How many base cases does a window of width three need, and which index first reads all three of them?

**Changed decision.** The window grows from two entries to three, so the table has three base cases and the loop starts at index 3. Small `n` must return before the loop reads a missing base case.
