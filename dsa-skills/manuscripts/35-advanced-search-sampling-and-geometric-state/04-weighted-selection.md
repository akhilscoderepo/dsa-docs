<!-- lesson-kind: standard -->
<!-- lesson-id: weighted-selection -->
## Weighted Selection

<!-- stage: context -->
### Servers With Unequal Capacity

A load balancer sends each incoming request to one of three servers. Server 0 has weight 1, server 1 has weight 3 and server 2 has weight 6, so over many requests server 2 should receive 60 percent of the traffic. A test with these weights passes. In production the weights are capacities measured in requests per hour, and a single weight reaches a billion. The balancer builds a table with one row per unit of weight, and the process runs out of memory while it fills the table.

The task is to choose index `i` with probability proportional to `w[i]`, using memory that grows with the number of servers and not with the sum of their weights. Each pick must also be fast, because the balancer chooses for every request. The question of this lesson is how a single random number can be mapped to the right server without a table of billions of rows.

<!-- stage: naive -->
### One Table Row Per Unit Of Weight

The direct design writes each index into a list `w[i]` times and picks a random position in the list. A server with weight 6 appears six times, so it is six times as likely as a server with weight 1. The source of randomness is a `LongUnaryOperator` named `pick`, where `pick.applyAsLong(b)` returns an integer from 0 to `b - 1`.

```java
final class ExpandedPicker {
    private final int[] table;
    private final java.util.function.LongUnaryOperator pick;

    ExpandedPicker(int[] w, java.util.function.LongUnaryOperator pick) {
        int total = 0;
        for (int x : w) total += x;
        table = new int[total];
        int at = 0;
        for (int i = 0; i < w.length; i++)
            for (int c = 0; c < w[i]; c++) table[at++] = i;   // index i appears w[i] times
        this.pick = pick;
    }

    int pickIndex() { return table[(int) pick.applyAsLong(table.length)]; }
}
```

The class is exact and a pick costs O(1). Its memory is the sum of all weights. A different attempt scans the weights for each pick, which saves memory and spends time.

```predict
The weights are 2, 5 and 3, so the table has 10 rows numbered 1 to 10 from left to right, with index 0 in rows 1 and 2. Which index does row 7 hold, and which index does row 8 hold? Then suppose there are 10^5 servers and each weight is 10^9. How many rows does the table need?

Rows 1 and 2 hold index 0, rows 3 to 7 hold index 1, and rows 8 to 10 hold index 2. So row 7 holds index 1 and row 8 holds index 2. The boundary falls between rows 7 and 8. With 10^5 weights of 10^9 the table needs 10^14 rows, far more than any machine can store.
```

<!-- stage: bottleneck -->
### Memory Follows The Weights

The table costs O(W) space for total weight `W`, and it costs O(W) time to build. The weights are numbers, and a number such as 10^9 needs a few bytes. The table stores it as a billion separate rows. The cost depends on how big the weights are, not on how many servers there are.

The table is also redundant. The rows for one server are consecutive and identical. All the table says about server 1 in the predict example is that its rows start at row 3 and end at row 7. Two numbers per server carry the same information. A pick only needs to know which of these row ranges holds the random row number.

A scan over the weights avoids the table. It adds weights one at a time until the running sum reaches the random number, and the index where it reaches is the answer. That costs O(1) space but O(n) time per pick, and the balancer picks for every request. A faster design keeps the running sums once and finds the right range without re-adding. The structure has to be small, built once, and searchable.

<!-- stage: insight -->
### Cumulative Sums Mark The Ranges

<!-- names: prefix total, ticket, owner -->

#### Each Index Owns A Range Of Tickets

Number the rows of the imaginary table from 1 to `W`, and call each number a **ticket**. Index `i` holds the tickets from `P[i-1] + 1` to `P[i]`, where `P[i]` is the **prefix total** `w[0] + w[1] + ... + w[i]` and `P[-1]` is 0. The range of index `i` has exactly `w[i]` tickets. The ranges do not overlap, and together they cover every ticket from 1 to `W`. The index that holds a ticket is its **owner**.

A uniform random ticket from 1 to `W` is owned by index `i` with probability `w[i] / W`. This is the required probability, and no table is built. The program stores only the `n` prefix totals.

#### Finding The Owner By Binary Search

The prefix totals are non-decreasing, because weights are not negative. The owner of ticket `x` is the first index `i` with `P[i] >= x`. That index satisfies `P[i-1] < x <= P[i]`, so `x` lies in the range of `i`. A binary search for the first prefix total that is at least `x` finds it in O(log n) steps. At the exact boundary `x = P[i]`, the ticket belongs to index `i` and not to `i + 1`, because the comparison is "at least".

An index with weight 0 has `P[i] = P[i-1]`. The search stops at the first index with the value, so it stops before the zero-weight index and that index owns no ticket.

#### The Cost

Building the prefix totals costs O(n) time and O(n) space. Each pick draws one ticket and searches in O(log n) time. The invariant is that the prefix totals are non-decreasing, the last one is `W`, and every ticket from 1 to `W` has exactly one owner.

<!-- stage: variables -->
### Totals, Tickets And Search Range

The picker keeps four names.

- **prefix** is a `long` array where `prefix[i]` is the sum of weights `0` to `i`. It is built once.
- **total** is `prefix[n - 1]`, the number of tickets. It is a `long`, because a sum of 10^5 weights of 10^9 reaches 10^14.
- **ticket** is the random number from 1 to `total` drawn for one pick. It equals `pick.applyAsLong(total) + 1`.
- **lo** and **hi** bound the binary search. The answer always lies in `[lo, hi]`, and the search ends when `lo == hi`.

The draw returns 0 to `total - 1`, so adding 1 makes the ticket start at 1. A ticket of 0 would belong to no range.

<!-- stage: trace -->
### Tracing Two Picks

#### A Ticket Inside A Range

The first trace uses weights `3 1 4 2`, so the prefix totals are `3 4 8 10` and the number of tickets is 10. The ticket is 5. Three pointers track the search: `lo` and `hi` mark its ends and `mid` marks the probe. The search starts with `lo` at 0 and `hi` at 3. The middle prefix total, 4 at index 1, is below 5, so `lo` moves to 2. The next middle value, 8 at index 2, is at least 5, so `hi` moves to 2. The search ends at index 2. Index 2 owns tickets 5 to 8, so ticket 5 is the first ticket of its range.

```trace
{"cells":[3,4,8,10],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"mid":-1,"hi":3},"vars":{"ticket":5},"note":"Start: ticket 5, search the whole range of indexes 0 to 3."},{"at":{"lo":2,"mid":1,"hi":3},"vars":{"ticket":5,"value":4},"note":"The prefix total 4 at index 1 is below 5, so lo moves to 2."},{"at":{"lo":2,"mid":2,"hi":2},"vars":{"ticket":5,"value":8},"note":"The prefix total 8 at index 2 is at least 5, so hi moves to 2."},{"at":{"lo":2,"mid":2,"hi":2},"vars":{"ticket":5,"owner":2},"note":"The search ends with lo equal to hi at index 2, so index 2 owns ticket 5."}]}
```

#### A Ticket On The Boundary

The second trace uses the same prefix totals with ticket 4. This ticket equals `P[1]`, the last ticket of index 1. The first middle value is 4, which is at least 4, so `hi` moves to 1. The next middle value is 3 at index 0, which is below 4, so `lo` moves to 1. The search ends at index 1. The comparison "at least" gives the boundary ticket to the earlier index.

```trace
{"cells":[3,4,8,10],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"mid":-1,"hi":3},"vars":{"ticket":4},"note":"Start: ticket 4, search the whole range of indexes 0 to 3."},{"at":{"lo":0,"mid":1,"hi":1},"vars":{"ticket":4,"value":4},"note":"The prefix total 4 at index 1 is at least 4, so hi moves to 1."},{"at":{"lo":1,"mid":0,"hi":1},"vars":{"ticket":4,"value":3},"note":"The prefix total 3 at index 0 is below 4, so lo moves to 1."},{"at":{"lo":1,"mid":1,"hi":1},"vars":{"ticket":4,"owner":1},"note":"The search ends with lo equal to hi at index 1, so index 1 owns ticket 4."}]}
```

<!-- stage: code -->
### Picker With Prefix Totals

#### The Class

The constructor builds the prefix totals as a `long` array. Each pick draws a ticket and runs a lower-bound search.

```java
final class WeightedPicker {
    private final long[] prefix;
    private final java.util.function.LongUnaryOperator pick;

    WeightedPicker(int[] w, java.util.function.LongUnaryOperator pick) {
        prefix = new long[w.length];
        long run = 0;
        for (int i = 0; i < w.length; i++) { run += w[i]; prefix[i] = run; }   // long arithmetic
        this.pick = pick;
    }

    int pickIndex() {
        long total = prefix[prefix.length - 1];
        long ticket = pick.applyAsLong(total) + 1;           // 1 to total
        int lo = 0, hi = prefix.length - 1;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (prefix[mid] >= ticket) hi = mid; else lo = mid + 1;   // first prefix total >= ticket
        }
        return lo;
    }
}
```

#### Cost

- **Constructor** costs O(n) time and O(n) space.
- **pickIndex** costs O(log n) time and O(1) extra space.
- **Weights** may be as large as the `int` range, because every sum is in a `long`.

<!-- stage: applicability -->
### When Cumulative Ranges Apply

#### Recognizing The Pattern

Use this method when each item has a non-negative weight, the chance of an item is its weight divided by the total, and the weights are fixed between picks. Before coding, decide the width of the sums and the policy for zero weights and for a total of zero. The invariant to keep is that the prefix totals are non-decreasing and every ticket has exactly one owner.

#### False Friends

Reservoir sampling looks related, since both pick at random, but it chooses among items that arrive one at a time with equal chance. A random pick from a sorted array by value is a second false friend: it uses binary search too, but the array holds values, not cumulative weights. A pick by rejection, which draws an index and a number below the maximum weight and keeps the pair when the number is below the weight, is exact but its speed depends on how uneven the weights are.

#### When The Method Does Not Apply

If weights change between picks, rebuilding the prefix totals costs O(n) per update, and a Fenwick tree is the right structure. If the weights are floating-point numbers, a ticket of exact integer width is not available and the boundaries need a tolerance. If every weight is 0, no item has a chance, and the caller must handle that case.

<!-- stage: exercises -->
### Exercises

#### [Build] Prefix Weight Intervals (Author exercise)
<!-- id: ws35-prefix-intervals -->

**Prerequisites.** Prefix totals and tickets from this lesson.

**Problem.** Write `int ownerOf(int[] w, long ticket)`. The array `w` holds positive weights. Index `i` owns the tickets `P[i-1] + 1` to `P[i]`, where `P[i]` is the sum of `w[0]` to `w[i]` and `P[-1]` is 0. Return the index that owns `ticket`.

**Constraints.** The limits are:
- **Length** of `w` is from 1 to 10^5.
- **Weights** are `int` values from 1 to 10^9.
- **Ticket** is a `long` from 1 to the sum of the weights.
- **Method** may scan the array once, because speed is not the goal here.

**Example 1.** Input `w = [2, 5, 3]`, `ticket = 7`, output `1`.

**Example 2.** Input `w = [2, 5, 3]`, `ticket = 8`, output `2`.

**Hint.** Which comparison between the running sum and the ticket marks the first index whose range reaches the ticket?

**Changed decision.** Basic case: the ranges come from a running sum, and the lookup is a scan.

#### [Vary] Random Pick With Weight (LeetCode 528)
<!-- id: ws35-random-pick-weight -->

**Prerequisites.** The Prefix Weight Intervals exercise above. This exercise stores the prefix totals once and replaces the scan with binary search.

**Problem.** Design the class `Picker` with a constructor that receives `int[] w` and a `LongUnaryOperator pick`. The method `pickIndex()` draws the ticket `pick.applyAsLong(total) + 1`, where `total` is the sum of the weights, and returns the owner of that ticket by binary search over stored prefix totals.

**Constraints.** The limits are:
- **Length** of `w` is from 1 to 10^4.
- **Weights** are `int` values from 1 to 10^5.
- **Calls** number at most 10^4 per object.
- **Cost** per call is O(log n), and the constructor does not copy the weights more than once.

**Example 1.** Input `w = [1, 3]` with scripted draws `0, 1, 3`, outputs `0, 1, 1`.

**Example 2.** Input `w = [2, 5, 3]` with scripted draw `6`, output `1`.

**Hint.** Which search finds the first prefix total that is at least the ticket?

**Changed decision.** The scan becomes a binary search over prefix totals that are built once.

#### [Boundary] Large Total And Zero Weight Policy (Author exercise)
<!-- id: ws35-large-total-zero-weight -->

**Prerequisites.** The Random Pick With Weight exercise above. This exercise changes the weight range and the legality of zero.

**Problem.** Design the class `SafePicker` with a constructor that receives `int[] w` and a `LongUnaryOperator pick`. A weight may be 0, and an index with weight 0 is never returned. The constructor throws `IllegalArgumentException` when the array is empty, when a weight is negative, or when the total is 0. The method `pickIndex()` returns an index with chance proportional to its weight, using `long` totals.

**Constraints.** The limits are:
- **Length** of `w` is from 0 to 10^5.
- **Weights** are `int` values from -10^9 to 10^9, and only the values from 0 up are legal.
- **Total** is at most 10^14 and fits in a `long`.
- **Draw** bound is the total, and the ticket is the draw plus 1.

**Example 1.** Input `w = [0, 4, 0, 1]` with scripted draws `0, 3, 4`, outputs `1, 1, 3`.

**Example 2.** Input `w = [1000000000, 1000000000, 1000000000]` with scripted draw `2999999999`, output `2`, and `w = [0, 0]` throws `IllegalArgumentException`.

**Hint.** What would an `int` sum of the prefix totals do for three weights of 10^9?

**Changed decision.** Totals move to `long`, zero weights are legal and never chosen, and the constructor rejects inputs that have no valid ticket.

#### [Recognize] Mutable Weight Discussion (Author exercise)
<!-- id: ws35-mutable-weights -->

**Prerequisites.** The Large Total And Zero Weight Policy exercise above and the Fenwick tree from the range-query chapter.

**Problem.** Design the class `LivePicker` with a constructor that receives `int[] w` and a `LongUnaryOperator pick`. The method `update(int i, int newWeight)` sets `w[i]` to `newWeight`. The method `pickIndex()` returns an index with chance proportional to the current weights, using the ticket rule of the previous exercises. Both methods must run in O(log n) time. Static prefix totals cost O(n) per update, so the design keeps a Fenwick tree and finds the owner by descending the tree.

**Constraints.** The limits are:
- **Length** of `w` is from 1 to 10^5.
- **Weights** are `int` values from 0 to 10^9, and the total is positive before every pick.
- **Calls** number at most 10^5 per object.
- **Update** index `i` is valid, and the total after an update may be 0 until the next update.

**Example 1.** Input `w = [3, 1, 2]` with scripted draw `3`, output `1`. After `update(1, 5)` and the scripted draw `3`, output `1`, and with the scripted draw `8`, output `2`.

**Example 2.** Input `w = [4]` with scripted draw `3`, output `0`. After `update(0, 0)` a pick throws `IllegalStateException`.

**Hint.** Which update would a prefix array pay for, and what does a Fenwick tree touch instead?

**Changed decision.** The weights change between picks, so the state becomes a Fenwick tree and the search becomes a descent on it.
