<!-- lesson-kind: standard -->
<!-- lesson-id: shortest-subarray-deque-state -->
## Shortest-Subarray Deque State

<!-- stage: context -->
### The Bakery That Wants A Quick Target

A bakery records its net profit for every day, and some days are losses, because the oven broke or a delivery was refunded. The owner has a target figure and asks a short question: what is the fewest consecutive days that together reach the target? A run that earns the target in three days is better news than one that needs ten, since the sooner the target is met, the sooner the loan is paid off.

The ledger has years of entries. The bookkeeper's first idea is to add days one after another until the target is met, and then drop days from the beginning to make the run shorter. That idea collapses at the first loss. When a loss arrives, the total falls, and she cannot tell whether dropping an old day, or keeping it, will help later. She needs a way to ask about any two cut points in the ledger and to forget cut points that can never be the best one.

<!-- stage: naive -->
### Try Every Start And Every End

The direct method fixes each start day, adds days one at a time, and records the length when the total reaches the target.

```java
static int shortestByScan(int[] profit, long target) {
    int best = -1;
    for (int start = 0; start < profit.length; start++) {
        long sum = 0;
        for (int end = start; end < profit.length; end++) {
            sum += profit[end];
            if (sum >= target) {
                int len = end - start + 1;
                if (best == -1 || len < best) best = len;
                break;
            }
        }
    }
    return best;
}
```

It is correct, and for the profits `[3, -2, 4, -1, 5]` with a target of 6 it returns 3, since the last three days sum to 8. The `break` is valid here, because a longer run from the same start is never shorter.

<!-- stage: bottleneck -->
### Quadratic Work And A Broken Shortcut

The scan examines about half of all start and end pairs when the target is never met, so it takes O(n^2) time. A ledger of a hundred thousand days means five billion additions in the worst case. The obvious speed-up, a two-pointer window that grows from the right and shrinks from the left, depends on one fact: adding a day never lowers the total, and removing one never raises it. With losses in the ledger both halves of that fact are false. A window may need to grow past a loss to recover, and shrinking from the left may remove a loss and make the total larger.

What stays true is a statement about cut points. A run from cut point `a` to cut point `b` has the sum of cumulative profit at `b` minus the cumulative profit at `a`, and the task is to find the closest pair of cut points whose difference reaches the target. A cut point that comes earlier and has a cumulative profit no lower than a later one is never the better start, because the later one is both closer and gives a larger difference. Only the remaining cut points need to be kept, and a cut point that has just been used cannot give a shorter run for any later end.

<!-- stage: insight -->
### Cut Points In A Deque

The solution works on **running balance** values: let `P[0] = 0` and let `P[j]` be the sum of the first `j` entries, held as `long`, so the sum of entries `a` to `b - 1` is `P[b] - P[a]`. A deque stores cut points in increasing order of position, and the invariant is that their balance values also increase strictly from front to back. For every new cut point `b`, there are two jobs, done in this order. The first is the **profitable start** job: while the front cut point satisfies `P[b] - P[front] >= target`, remove it from the front and record `b - front` as a candidate, since that start cannot give a shorter run with any later end. The second is the **dominated start** job: while the back cut point has a balance at least as large as `P[b]`, remove it from the back, since `b` is a start that is later and at least as good. Then `b` is appended.

<!-- names: running balance, profitable start, dominated start -->

The front is removed on success because the first end that works for a start is the shortest for that start, and the next end can only be longer. The back is removed on domination because the balance order is what lets the front be the only start worth testing. Without the strict order, a start behind the front might satisfy the target while the front does not, and the front test would miss it.

Every cut point enters once and leaves once, so the time is O(n) with O(n) memory for the balance values.

<!-- stage: variables -->
### Balance Array, Deque And Best Length

The array `P` has length `n + 1` and holds `long` values, because a hundred thousand entries of a billion each reach a hundred trillion, far beyond `int`. The index `b` runs from 0 to `n`. The deque holds cut points, which are indices into `P`, and a cut point `a` stands for a run that starts at day `a`. The value `best` starts at a sentinel that is larger than any possible length, and it is replaced by `b - front` only when that is smaller. At the end the sentinel means that the target was never reached, and the answer is -1.

<!-- stage: trace -->
### A Loss Does Not Break The Order

Take the profits `3, -2, 4, -1, 5` with a target of 6, so the cut-point balances are `0, 3, 1, 5, 4, 9`. Cut point 0 is stored. Cut point 1 has balance 3, the front fails with difference 3, and it is appended behind. Cut point 2 has balance 1, which is lower than the 3 at the back, so the back is removed and cut point 2 is appended, leaving `[0, 2]`. This is the loss: the balance fell, and the cut point that held 3 became useless as a start. Cut point 3 has balance 5 and joins the deque. Cut point 4 has balance 4 and removes cut point 3 from the back. At cut point 5 the balance is 9, and the front passes with difference 9, giving length 5. The next front, cut point 2, passes with difference 8, giving length 3. Cut point 4 fails with difference 5, so the loop stops.

A second run uses `4, -5, 6, -1, 7` with a target of 12, where a loss early on clears every earlier start from the deque and the answer needs the whole run after it.

```trace
{"cells":[0,3,1,5,4,9],"pointers":["b"],"steps":[{"at":{"b":0},"vars":{"balances":"[0]","deque":"[0]","best":-1},"note":"Cut point 0 has balance 0. The front does not reach the target. Cut point 0 is appended."},{"at":{"b":1},"vars":{"balances":"[0,3]","deque":"[0,1]","best":-1},"note":"Cut point 1 has balance 3. The front does not reach the target. Cut point 1 is appended."},{"at":{"b":2},"vars":{"balances":"[0,3,1]","deque":"[0,2]","best":-1},"note":"Cut point 2 has balance 1. The front does not reach the target. The back removes cut point 1 because 1 is not larger. Cut point 2 is appended."},{"at":{"b":3},"vars":{"balances":"[0,3,1,5]","deque":"[0,2,3]","best":-1},"note":"Cut point 3 has balance 5. The front does not reach the target. Cut point 3 is appended."},{"at":{"b":4},"vars":{"balances":"[0,3,1,5,4]","deque":"[0,2,4]","best":-1},"note":"Cut point 4 has balance 4. The front does not reach the target. The back removes cut point 3 because 4 is not larger. Cut point 4 is appended."},{"at":{"b":5},"vars":{"balances":"[0,3,1,5,4,9]","deque":"[4,5]","best":3},"note":"Cut point 5 has balance 9. The front passes the target test and is removed for starts 0, 2, giving the best length 3. Cut point 5 is appended."}]}
```

```trace
{"cells":[0,4,-1,5,4,11],"pointers":["b"],"steps":[{"at":{"b":0},"vars":{"balances":"[0]","deque":"[0]","best":-1},"note":"Cut point 0 has balance 0. The front does not reach the target. Cut point 0 is appended."},{"at":{"b":1},"vars":{"balances":"[0,4]","deque":"[0,1]","best":-1},"note":"Cut point 1 has balance 4. The front does not reach the target. Cut point 1 is appended."},{"at":{"b":2},"vars":{"balances":"[0,4,-1]","deque":"[2]","best":-1},"note":"Cut point 2 has balance -1. The front does not reach the target. The back removes cut points 1, 0 because -1 is not larger. Cut point 2 is appended."},{"at":{"b":3},"vars":{"balances":"[0,4,-1,5]","deque":"[2,3]","best":-1},"note":"Cut point 3 has balance 5. The front does not reach the target. Cut point 3 is appended."},{"at":{"b":4},"vars":{"balances":"[0,4,-1,5,4]","deque":"[2,4]","best":-1},"note":"Cut point 4 has balance 4. The front does not reach the target. The back removes cut point 3 because 4 is not larger. Cut point 4 is appended."},{"at":{"b":5},"vars":{"balances":"[0,4,-1,5,4,11]","deque":"[4,5]","best":3},"note":"Cut point 5 has balance 11. The front passes the target test and is removed for start 2, giving the best length 3. Cut point 5 is appended."}]}
```

<!-- stage: code -->
### Prefix Array And The Two Jobs

```java
static long[] prefixBalances(int[] profit) {
    long[] balance = new long[profit.length + 1];
    for (int i = 0; i < profit.length; i++) balance[i + 1] = balance[i] + profit[i];
    return balance;
}

static int shortestAtLeast(int[] profit, long target) {
    long[] balance = prefixBalances(profit);
    java.util.ArrayDeque<Integer> deque = new java.util.ArrayDeque<>();
    int best = Integer.MAX_VALUE;
    for (int b = 0; b < balance.length; b++) {
        while (!deque.isEmpty() && balance[b] - balance[deque.peekFirst()] >= target) {
            best = Math.min(best, b - deque.removeFirst());
        }
        while (!deque.isEmpty() && balance[deque.peekLast()] >= balance[b]) deque.removeLast();
        deque.addLast(b);
    }
    return best == Integer.MAX_VALUE ? -1 : best;
}
```

The balance array is built once in O(n). Every index is added to the deque once and removed once, from at most one end, so the loop is O(n) in total. The subtraction is between two `long` values, so it cannot wrap.

<!-- stage: applicability -->
### When Negative Values Block A Window

Use this state when the task asks for the shortest or the longest stretch whose sum meets a threshold, when entries may be negative, and when the cumulative sums let any stretch be written as a difference of two of them. The invariant is that the stored cut points are in position order and their cumulative values strictly increase, so the front is the earliest start that might still pay off, and a start that succeeds at some end is removed because no later end can shorten it.

The false friend is the ordinary two-pointer window. It passes on all-positive input and fails quietly on negative input, because shrinking from the left can raise the total. A second false friend is a deque that is checked only at its front but whose back is never trimmed, so a hidden start behind the front is never reached. A third is `int` balances, which overflow on long ledgers.

Do not use it for an at-most threshold with positive entries, where the plain window suffices, nor for a stretch whose sum must equal a target exactly, where a hash map of balances is the tool. In Java, remember that `Integer.MAX_VALUE` is a sentinel only while real lengths stay below it, and that mixing `int` and `long` in the subtraction needs the left operand widened before the arithmetic.

<!-- stage: exercises -->
### Exercises

#### [Build] Prefix-Pair Difference (Author exercise)
<!-- id: dq-prefix-pair-difference -->

**Prerequisites.** The prefix sums chapter, and the index expiry lesson of this chapter.

**Problem.** Given an integer array `nums` and a list of queries `[l, r]` with `0 <= l <= r < nums.length`, return the sum of `nums[l]` through `nums[r]` for every query, by building an array of cumulative sums once and subtracting two of its entries.

**Constraints.** 1 <= nums.length <= 10^5, -10^9 <= nums[i] <= 10^9 and up to 10^5 queries. The answers may exceed the range of `int`, so return `long` values.

**Example 1.** Input `nums = [2, -1, 3, -4, 5]`, queries `[[0, 2], [1, 3], [3, 4]]`, output `[4, -2, 1]`.

**Example 2.** Input `nums = [7]`, queries `[[0, 0]]`, output `[7]`.

**Hint.** The cumulative array has one more entry than `nums`. Which two entries give the sum of positions `l` through `r`?

**Changed decision.** First rung: the cumulative array starts with a zero entry, so the run from `l` to `r` is the difference between the entries at `r + 1` and `l`.

#### [Vary] Remove Dominated Prefixes (Author exercise)
<!-- id: dq-remove-dominated-prefixes -->

**Prerequisites.** The Prefix-Pair Difference exercise above.

**Problem.** Given an array `p` of cumulative values, process its indices from left to right, and before appending an index remove from the back every stored index whose value is at least as large as the new one. Return the indices that remain after the last step.

**Constraints.** 1 <= p.length <= 10^5 and -10^15 <= p[i] <= 10^15. Linear time.

**Example 1.** Input `p = [0, 2, 1, 4, 4, 3]`, output `[0, 2, 5]`.

**Example 2.** Input `p = [0, -1, -2]`, output `[2]`.

**Hint.** Why is a stored index with a value at least as large as a newer one never the better start for any later end?

**Changed decision.** The back is trimmed with a non-strict comparison, so values stored from front to back increase strictly, and equal values keep only the newest index.

#### [Boundary] Negative Values And Long Sums (Author exercise)
<!-- id: dq-negative-long-sums -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums` and a `long` target `k`, return `[length, start]` for the shortest non-empty contiguous run whose sum is at least `k`, taking the leftmost start when several runs share the shortest length. If no run qualifies, return `[-1, -1]`.

**Constraints.** 1 <= nums.length <= 10^5, -10^9 <= nums[i] <= 10^9 and 1 <= k <= 10^14. Linear time.

**Example 1.** Input `nums = [4, -5, 6, -1, 7]`, `k = 12`, output `[3, 2]`.

**Example 2.** Input `nums = [1000000000, 1000000000, 1000000000]`, `k = 3000000000`, output `[3, 0]`.

**Hint.** When a start is removed from the front, which end produced the candidate, and how is the start's position recovered? When two candidates tie in length, which one is found first?

**Changed decision.** Cumulative sums and the target are `long`, and a candidate replaces the best only when it is strictly shorter, so the earliest end, and with it the leftmost start, wins ties.

#### [Recognize] Shortest Subarray with Sum at Least K (LeetCode 862)
<!-- id: dq-shortest-subarray-sum-k -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `nums` and an integer `k`, return the length of the shortest non-empty contiguous subarray whose sum is at least `k`. If there is none, return -1.

**Constraints.** 1 <= nums.length <= 10^5, -10^4 <= nums[i] <= 10^4 and 1 <= k <= 10^9. Linear time.

**Example 1.** Input `nums = [3, -2, 4, -1, 5]`, `k = 6`, output 3.

**Example 2.** Input `nums = [1, 2]`, `k = 4`, output -1.

**Hint.** Why does a window that shrinks from the left fail when `nums` has negative entries? What do the stored cut points need to satisfy so that the front is the only one worth testing?

**Changed decision.** The scan runs over cut points of the cumulative array instead of over array entries, and the deque is trimmed at both ends, successful starts from the front and dominated starts from the back.
