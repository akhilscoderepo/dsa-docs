<!-- lesson-kind: standard -->
<!-- lesson-id: bitmask-assignment -->
## Bitmask Assignment

<!-- stage: context -->
### Giving Each Worker One Job

A batch system has three workers and three jobs. Each worker takes one job, and each job goes to one worker. The table `cost[w][j]` gives the minutes that worker `w` needs for job `j`. For `[[3,3,9],[2,8,9],[7,6,5]]`, the cheapest plan costs 10. Worker 0 takes job 1, worker 1 takes job 0 and worker 2 takes job 2.

A developer writes a quick rule. It handles the workers in order, and each worker takes the cheapest job that is still free, using the lowest job number on a tie. Worker 0 takes job 0 for 3 minutes. Worker 1 then has only jobs 1 and 2 left and pays 8. Worker 2 pays 5 for job 2. The rule reports 16, which is 6 minutes worse than the best plan.

Formally, the input is a square matrix `cost` with `n` rows and `n` columns. Row `w` is a worker and column `j` is a job. An **assignment** gives every worker a different job. Its cost is the sum of the chosen entries. The goal is to return the smallest cost over all assignments.

This lesson asks how to search the assignments quickly when one early pick changes which jobs stay free.

<!-- stage: naive -->
### Trying Every Order Of Jobs

The safe idea is to try every assignment. The method gives worker 0 each job, then gives worker 1 each job that is still free, and so on. A `boolean[]` named `taken` records which jobs are in use.

```java
static int tryAll(int[][] cost, int worker, boolean[] taken) {
    int n = cost.length;
    if (worker == n) {
        return 0;
    }
    int best = Integer.MAX_VALUE;
    for (int j = 0; j < n; j++) {
        if (!taken[j]) {
            taken[j] = true;
            int rest = tryAll(cost, worker + 1, taken);
            taken[j] = false;
            best = Math.min(best, cost[worker][j] + rest);
        }
    }
    return best;
}
```

The first call passes `worker = 0` and an all-false array. The method finds the true minimum, because it looks at every assignment. Worker 0 has n choices, worker 1 has n - 1 choices, and so on, so the recursion visits n! complete assignments. The time is O(n!), and the recursion depth gives O(n) memory.

<!-- stage: bottleneck -->
### Repeated Work Across Different Orders

```predict
A search tries every assignment for 15 workers. How many complete assignments is that? And how many different sets of jobs can the first few workers hold, counting every size from 0 to 15?

There are 15! = 1,307,674,368,000 complete assignments. There are only 2^15 = 32,768 different sets of jobs, because each job is either in the set or out of it.
```

The search is correct but its cost explodes. For n = 12 it visits 479,001,600 assignments, and each one costs O(n) to add up unless the sum is kept along the path. For n = 15 the count passes 10^12. No input of that size finishes.

The cause is repeated work. Take workers 0 and 1 and jobs 3 and 5. Worker 0 on job 3 with worker 1 on job 5 leaves the same problem as worker 0 on job 5 with worker 1 on job 3. Both leave workers 2 onward facing the same free jobs. The search solves that remaining problem once for each order of the two picks.

Only the set of used jobs matters for the future, not the order that produced it. A set drawn from n jobs has 2^n possibilities, which is far below n!. If each set is solved once and stored, the work drops to O(n * 2^n). The next section shows how to store a set in one integer and how one answer follows from smaller ones.

<!-- stage: insight -->
### Store The Used Jobs In One Integer

An integer has 32 bits, and each bit can say yes or no for one job. That makes a whole set of jobs a single number, which can index an array.

<!-- names: job mask, popcount, full mask -->

#### Bits Hold A Set Of Jobs

A **job mask** is an `int` whose bit `j` is 1 exactly when job `j` is in the set. Bit 0 is the lowest bit. The set `{0, 2}` is the number `101` in binary, which is 5.

Five operations cover everything the lesson needs. `1 << j` is an integer with only bit `j` set. `mask | (1 << j)` adds job `j`. `mask & ~(1 << j)` removes it. `(mask >> j) & 1` tests it and gives 0 or 1. `mask ^ (1 << j)` flips it, which removes a job that is known to be present.

#### Counting Bits Gives The Worker

The **popcount** of a mask is the number of 1 bits, and Java computes it with `Integer.bitCount(mask)`. Suppose workers receive jobs in order, worker 0 first. After the first `k` workers finish, the job mask holds exactly `k` jobs. The popcount therefore names the next worker without an extra index.

The **full mask** is `(1 << n) - 1`, which has bits 0 to n - 1 all set. It is the largest mask for n jobs. The array that stores one answer per mask has `1 << n` entries, indexes 0 to the full mask.

#### Each Entry Removes One Job

Let `dp[mask]` be the smallest cost of giving the first `popcount(mask)` workers different jobs, using exactly the jobs in `mask`. For a nonempty mask, the last of those workers is worker `w = popcount(mask) - 1`. That worker holds one job `j` from the mask. The other workers hold the jobs of `mask ^ (1 << j)`.

The entry is the smallest value of `dp[mask ^ (1 << j)] + cost[w][j]` over every `j` in the mask. The base entry is `dp[0] = 0`, because no worker needs a job. The answer is `dp[full mask]`. The invariant is that `mask ^ (1 << j)` is a smaller number than `mask`, so a loop that counts up from 1 finishes every entry before another entry reads it.

<!-- stage: variables -->
### The Array And Its Bit Operations

One matrix comes in, and these working values describe the computation.

- **cost** is the `int[n][n]` input; `cost[w][j]` is the price of giving job `j` to worker `w`.
- **dp** is an `int[1 << n]`; entry `dp[mask]` is the cheapest way to cover the jobs in `mask` with the first `popcount(mask)` workers.
- **mask** runs from 1 to `(1 << n) - 1`, one value per set of jobs.
- **w** is `Integer.bitCount(mask) - 1`, the worker who takes the last job of the set.
- **j** is a job whose bit is 1 in `mask`; the loop tries each one.

Java fills a new `int` array with zeros, so `dp[0]` is already the base value 0. The loop sets `best` to `Integer.MAX_VALUE` before it compares. Each cost stays small enough that adding it to a stored answer never overflows an `int`.

<!-- stage: trace -->
### Two Runs Over The Masks

#### Beating The Cheapest Free Job Rule

The first run uses the matrix from the opening, `[[3,3,9],[2,8,9],[7,6,5]]`. The array has 8 cells, one per mask from 0 to 7, and the pointer `mask` marks the entry in progress. The variable `mask` prints the bits with job 0 on the right, `worker` is the index of the worker who takes the last job, and `dp` is the value written.

The three masks with one job cost the first row of the matrix, which is 3, 3 and 9. Mask `011` holds jobs 0 and 1. Worker 1 takes one of them, and the cheaper option leaves job 1 to worker 0 and gives job 0 to worker 1, for 5. The final mask `111` has three options. Worker 2 on job 2 adds 5 to the 5 stored for `011`, which gives 10. The other two options give 19 and 17. The answer is 10, as the opening claimed.

```trace
{"cells":[0,1,2,3,4,5,6,7],"pointers":["mask"],"steps":[{"at":{"mask":-1},"vars":{"mask":"000","worker":-1,"dp":0},"note":"Only mask 0 is known. The empty set of jobs costs 0, and the other entries wait."},{"at":{"mask":1},"vars":{"mask":"001","worker":0,"dp":3},"note":"Mask 001 holds 1 job, so worker 0 takes the last one. Options: job 0 leaves mask 000 at 0 plus 3, which is 3. The entry keeps the smallest, 3."},{"at":{"mask":2},"vars":{"mask":"010","worker":0,"dp":3},"note":"Mask 010 holds 1 job, so worker 0 takes the last one. Options: job 1 leaves mask 000 at 0 plus 3, which is 3. The entry keeps the smallest, 3."},{"at":{"mask":3},"vars":{"mask":"011","worker":1,"dp":5},"note":"Mask 011 holds 2 jobs, so worker 1 takes the last one. Options: job 0 leaves mask 010 at 3 plus 2, which is 5; job 1 leaves mask 001 at 3 plus 8, which is 11. The entry keeps the smallest, 5."},{"at":{"mask":4},"vars":{"mask":"100","worker":0,"dp":9},"note":"Mask 100 holds 1 job, so worker 0 takes the last one. Options: job 2 leaves mask 000 at 0 plus 9, which is 9. The entry keeps the smallest, 9."},{"at":{"mask":5},"vars":{"mask":"101","worker":1,"dp":11},"note":"Mask 101 holds 2 jobs, so worker 1 takes the last one. Options: job 0 leaves mask 100 at 9 plus 2, which is 11; job 2 leaves mask 001 at 3 plus 9, which is 12. The entry keeps the smallest, 11."},{"at":{"mask":6},"vars":{"mask":"110","worker":1,"dp":12},"note":"Mask 110 holds 2 jobs, so worker 1 takes the last one. Options: job 1 leaves mask 100 at 9 plus 8, which is 17; job 2 leaves mask 010 at 3 plus 9, which is 12. The entry keeps the smallest, 12."},{"at":{"mask":7},"vars":{"mask":"111","worker":2,"dp":10},"note":"Mask 111 holds 3 jobs, so worker 2 takes the last one. Options: job 0 leaves mask 110 at 12 plus 7, which is 19; job 1 leaves mask 101 at 11 plus 6, which is 17; job 2 leaves mask 011 at 5 plus 5, which is 10. The entry keeps the smallest, 10."}]}
```

#### A Larger Matrix With Sixteen Masks

The second run uses the 4 by 4 matrix `[[9,2,7,8],[6,4,3,7],[5,8,1,8],[7,6,9,4]]`, so the array has 16 cells. The single-job masks again copy the first row. Each two-job mask compares two options and keeps the smaller. Each three-job mask compares three, and the final mask compares four. The sequence shows that every entry is written once, in increasing order, and that each option reads an entry with fewer bits that is already final. The answer at mask `1111` is 13.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],"pointers":["mask"],"steps":[{"at":{"mask":-1},"vars":{"mask":"0000","worker":-1,"dp":0},"note":"Only mask 0 is known. The empty set of jobs costs 0, and the other entries wait."},{"at":{"mask":1},"vars":{"mask":"0001","worker":0,"dp":9},"note":"Mask 0001 holds 1 job, so worker 0 takes the last one. Options: job 0 leaves mask 0000 at 0 plus 9, which is 9. The entry keeps the smallest, 9."},{"at":{"mask":2},"vars":{"mask":"0010","worker":0,"dp":2},"note":"Mask 0010 holds 1 job, so worker 0 takes the last one. Options: job 1 leaves mask 0000 at 0 plus 2, which is 2. The entry keeps the smallest, 2."},{"at":{"mask":3},"vars":{"mask":"0011","worker":1,"dp":8},"note":"Mask 0011 holds 2 jobs, so worker 1 takes the last one. Options: job 0 leaves mask 0010 at 2 plus 6, which is 8; job 1 leaves mask 0001 at 9 plus 4, which is 13. The entry keeps the smallest, 8."},{"at":{"mask":4},"vars":{"mask":"0100","worker":0,"dp":7},"note":"Mask 0100 holds 1 job, so worker 0 takes the last one. Options: job 2 leaves mask 0000 at 0 plus 7, which is 7. The entry keeps the smallest, 7."},{"at":{"mask":5},"vars":{"mask":"0101","worker":1,"dp":12},"note":"Mask 0101 holds 2 jobs, so worker 1 takes the last one. Options: job 0 leaves mask 0100 at 7 plus 6, which is 13; job 2 leaves mask 0001 at 9 plus 3, which is 12. The entry keeps the smallest, 12."},{"at":{"mask":6},"vars":{"mask":"0110","worker":1,"dp":5},"note":"Mask 0110 holds 2 jobs, so worker 1 takes the last one. Options: job 1 leaves mask 0100 at 7 plus 4, which is 11; job 2 leaves mask 0010 at 2 plus 3, which is 5. The entry keeps the smallest, 5."},{"at":{"mask":7},"vars":{"mask":"0111","worker":2,"dp":9},"note":"Mask 0111 holds 3 jobs, so worker 2 takes the last one. Options: job 0 leaves mask 0110 at 5 plus 5, which is 10; job 1 leaves mask 0101 at 12 plus 8, which is 20; job 2 leaves mask 0011 at 8 plus 1, which is 9. The entry keeps the smallest, 9."},{"at":{"mask":8},"vars":{"mask":"1000","worker":0,"dp":8},"note":"Mask 1000 holds 1 job, so worker 0 takes the last one. Options: job 3 leaves mask 0000 at 0 plus 8, which is 8. The entry keeps the smallest, 8."},{"at":{"mask":9},"vars":{"mask":"1001","worker":1,"dp":14},"note":"Mask 1001 holds 2 jobs, so worker 1 takes the last one. Options: job 0 leaves mask 1000 at 8 plus 6, which is 14; job 3 leaves mask 0001 at 9 plus 7, which is 16. The entry keeps the smallest, 14."},{"at":{"mask":10},"vars":{"mask":"1010","worker":1,"dp":9},"note":"Mask 1010 holds 2 jobs, so worker 1 takes the last one. Options: job 1 leaves mask 1000 at 8 plus 4, which is 12; job 3 leaves mask 0010 at 2 plus 7, which is 9. The entry keeps the smallest, 9."},{"at":{"mask":11},"vars":{"mask":"1011","worker":2,"dp":14},"note":"Mask 1011 holds 3 jobs, so worker 2 takes the last one. Options: job 0 leaves mask 1010 at 9 plus 5, which is 14; job 1 leaves mask 1001 at 14 plus 8, which is 22; job 3 leaves mask 0011 at 8 plus 8, which is 16. The entry keeps the smallest, 14."},{"at":{"mask":12},"vars":{"mask":"1100","worker":1,"dp":11},"note":"Mask 1100 holds 2 jobs, so worker 1 takes the last one. Options: job 2 leaves mask 1000 at 8 plus 3, which is 11; job 3 leaves mask 0100 at 7 plus 7, which is 14. The entry keeps the smallest, 11."},{"at":{"mask":13},"vars":{"mask":"1101","worker":2,"dp":15},"note":"Mask 1101 holds 3 jobs, so worker 2 takes the last one. Options: job 0 leaves mask 1100 at 11 plus 5, which is 16; job 2 leaves mask 1001 at 14 plus 1, which is 15; job 3 leaves mask 0101 at 12 plus 8, which is 20. The entry keeps the smallest, 15."},{"at":{"mask":14},"vars":{"mask":"1110","worker":2,"dp":10},"note":"Mask 1110 holds 3 jobs, so worker 2 takes the last one. Options: job 1 leaves mask 1100 at 11 plus 8, which is 19; job 2 leaves mask 1010 at 9 plus 1, which is 10; job 3 leaves mask 0110 at 5 plus 8, which is 13. The entry keeps the smallest, 10."},{"at":{"mask":15},"vars":{"mask":"1111","worker":3,"dp":13},"note":"Mask 1111 holds 4 jobs, so worker 3 takes the last one. Options: job 0 leaves mask 1110 at 10 plus 7, which is 17; job 1 leaves mask 1101 at 15 plus 6, which is 21; job 2 leaves mask 1011 at 14 plus 9, which is 23; job 3 leaves mask 0111 at 9 plus 4, which is 13. The entry keeps the smallest, 13."}]}
```

<!-- stage: code -->
### Filling The Array By Mask

The method returns the smallest total cost of a complete assignment. It visits masks in increasing order and reads only smaller masks.

```java
static int minAssignment(int[][] cost) {
    int n = cost.length;
    int full = (1 << n) - 1;
    int[] dp = new int[1 << n];
    for (int mask = 1; mask <= full; mask++) {
        int w = Integer.bitCount(mask) - 1;
        int best = Integer.MAX_VALUE;
        for (int j = 0; j < n; j++) {
            if ((mask >> j & 1) == 1) {
                best = Math.min(best, dp[mask ^ (1 << j)] + cost[w][j]);
            }
        }
        dp[mask] = best;
    }
    return dp[full];
}
```

Time is O(n * 2^n), because there are 2^n masks and each tries up to n jobs. Memory is O(2^n). For n = 0 the loop runs zero times and the method returns `dp[0]`, which is 0. For n = 20 the array holds about a million entries, and for n = 30 it would hold over a billion, which is too large. The exercises below build the bit operations first.

<!-- stage: applicability -->
### Recognizing Small Sets In The State

#### Reading The Cue

Use this method when each item can be used once and the future depends on which items are left. Phrases such as "each exactly once", "different columns" and "split into groups" point here, together with a limit near 20 on the item count. The state is a set of used items, and a count often tells the next position.

#### Checking The Invariant

The invariant says that bit `j` of the mask records whether item `j` is used, and that each entry is final before a larger mask reads it. Test a one-by-one matrix, which must return its single entry. Test a matrix where every entry is equal, which must return `n` times that value. Test a matrix whose cheapest picks collide on one column, because that case defeats the quick rule from the opening.

#### Avoiding The False Friend

The first false friend is the cheapest-free-job rule, which passes whenever the cheapest picks happen not to collide. The second is a set stored as a sorted list or a string key in a hash map, which has the same states but pays far more per lookup. The third is indexing the worker by the mask value and not by `Integer.bitCount(mask) - 1`. The mask value can be far larger than `n`, and it does not count the jobs already placed. The method does not apply when n reaches 30 or more, because 2^n entries no longer fit in memory, or when item order matters and not just the set, because a mask forgets order.

<!-- stage: exercises -->
### Exercises

#### [Build] Set Test And Clear Bits (Author exercise)
<!-- id: dp29-set-test-clear -->

**Prerequisites.** The bit operations from this lesson.

**Problem.** An integer `n` and two arrays `add` and `remove` are given. Start with an empty set stored in an `int` where bit `i` stands for item `i`. First add every item of `add`, in order. Then remove every item of `remove`, in order. Return the final integer.

**Constraints.** The limits are:
- **Item count** satisfies `0 <= n <= 30`.
- **Items** satisfy `0 <= item < n` in both arrays.
- **Length** of each array is at most 100, and either array may be empty.
- **Repeats** are allowed, and removing an absent item changes nothing.

**Example 1.** Input `n = 5`, `add = [0, 2, 4]`, `remove = [2]`, output `17`.

**Example 2.** Input `n = 4`, `add = [1, 1, 3]`, `remove = [0]`, output `10`.

**Hint.** Which operator sets a bit without touching the others, and which one clears a bit that may already be 0?

**Changed decision.** The method stores the whole set in one `int` instead of a `boolean[]`, so each update is a single bit operation.

#### [Vary] Minimum Assignment Cost (Author exercise)
<!-- id: dp29-min-assignment-cost -->

**Prerequisites.** The exercise above and the table from this lesson.

**Problem.** A matrix `cost` with `n` rows and `m` columns is given, where `n <= m`. Give every row a different column. Return the smallest sum of the chosen entries. Some columns stay unused.

**Constraints.** The limits are:
- **Rows** satisfy `1 <= n <= 12`.
- **Columns** satisfy `n <= m <= 14`.
- **Entries** satisfy `0 <= cost[r][c] <= 1000`.
- **Result** is an `int`.

**Example 1.** Input `cost = [[4, 2, 8], [4, 3, 7]]`, output `6`.

**Example 2.** Input `cost = [[5, 9, 1, 6]]`, output `1`.

**Hint.** The mask now ranges over columns, so which masks can be a final answer, and which popcount do they share?

**Changed decision.** The mask has `m` bits and only `n` workers, so the answer is the smallest entry among masks with exactly `n` bits set, not the entry for the full mask.

#### [Boundary] Full Mask And State Count (Author exercise)
<!-- id: dp29-full-mask-count -->

**Prerequisites.** The two exercises above.

**Problem.** An integer `n` is given. Return a `long[]` of three values. The first is the full mask `(1 << n) - 1`. The second is the number of masks from 0 to the full mask. The third is the memory in bytes of an `int[]` that holds one entry for each of those masks, counting 4 bytes per entry and ignoring the array header.

**Constraints.** The limits are:
- **Item count** satisfies `0 <= n <= 30`.
- **Result** is a `long[]` of length 3, because the byte count exceeds the `int` range for large `n`.
- **Mutation** is not applicable, because the method has no array input.

**Example 1.** Input `n = 3`, output `[7, 8, 32]`.

**Example 2.** Input `n = 0`, output `[0, 1, 4]`.

**Hint.** Which type must hold `1L << n` and the byte count, and what is the largest byte count when `n = 30`?

**Changed decision.** The method returns counts and runs no loop over masks. The count is held in a `long`, so n = 0 gives a single state and n = 30 gives 1,073,741,824 states and 4,294,967,296 bytes, which exceeds the `int` range.

#### [Recognize] Partition To K Equal Sum Subsets (LeetCode 698)
<!-- id: dp29-partition-k-subsets -->

**Prerequisites.** All three exercises above.

**Problem.** The inputs are the array `nums` of integers and the integer `k`. Return `true` if the numbers can be split into `k` nonempty groups with the same sum, using every number exactly once. Return `false` otherwise.

**Constraints.** The limits are:
- **Length** satisfies `1 <= k <= nums.length <= 16`.
- **Values** satisfy `1 <= nums[i] <= 10000`.
- **Result** is a `boolean`.
- **Mutation** of `nums` is allowed, because the caller does not reuse the array.

**Example 1.** Input `nums = [2, 2, 2, 3, 3]`, `k = 2`, output `true`.

**Example 2.** Input `nums = [5, 5, 5, 5, 2, 2]`, `k = 3`, output `false`.

**Hint.** If the target sum is `t`, how full is the current group after the numbers in a mask are placed, and can that be stored as one number per mask?

**Changed decision.** The state has two parts, the set of placed numbers and the fill of the group in progress, and the fill is stored as the remainder of the mask's sum divided by `t`.
