<!-- lesson-kind: standard -->
<!-- lesson-id: sort-order -->
## Choose How To Sort Intervals

<!-- stage: context -->
### A Merge That Misses A Booking

A booking tool receives three reservations in arrival order: hours `[1,4]`, `[7,9]` and `[2,5]`. The tool must merge reservations that share any hour. A short loop compares each new reservation with the last merged one only. It keeps `[1,4]`, sees that `[7,9]` shares no hour with it, and appends `[7,9]`. It then compares `[2,5]` with `[7,9]`, finds no overlap, and appends `[2,5]` too. The output is `[1,4]`, `[7,9]`, `[2,5]`, although `[1,4]` and `[2,5]` plainly share the hours 2 to 4.

The loop is cheap, but it looks at the wrong neighbour. The reservation `[2,5]` belongs next to `[1,4]`, and the arrival order put `[7,9]` between them. The lesson turns on a single question. Which order makes the last merged interval the only one that the next interval can overlap?

<!-- stage: naive -->
### Compare Every Pair Until Nothing Changes

The simple repair is to stop trusting the order. Keep a list of intervals. Test every pair, and when two pairs overlap, replace them with their union. Repeat the whole pass until a pass changes nothing.

An interval here is a pair `[start, end]` with `start <= end`, and two intervals overlap when each starts no later than the other ends.

```java
static List<int[]> mergeByRepeatedPasses(int[][] intervals) {
    List<int[]> list = new ArrayList<>();
    for (int[] iv : intervals) list.add(new int[] {iv[0], iv[1]});
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int i = 0; i < list.size() && !changed; i++) {
            for (int j = i + 1; j < list.size() && !changed; j++) {
                int[] a = list.get(i), b = list.get(j);
                if (a[0] <= b[1] && b[0] <= a[1]) {
                    list.set(i, new int[] {Math.min(a[0], b[0]), Math.max(a[1], b[1])});
                    list.remove(j);
                    changed = true;
                }
            }
        }
    }
    return list;
}
```

On `[1,4]`, `[7,9]`, `[2,5]` the method returns `[1,5]` and `[7,9]`, which is correct. It never depends on the arrival order, so it fixes the failure from the opening.

<!-- stage: bottleneck -->
### Counting Pair Tests

```predict
Suppose the intervals are processed in increasing order of their start values. After merging some of them, which earlier interval can the next one overlap?

Only the last merged interval can overlap it. Every earlier merged interval ends before the last one begins, and the next start is at least as large as the last start. One comparison per interval is therefore enough, and the order costs only the O(n log n) of a sort.
```

One pass tests every pair, which is `n * (n - 1) / 2` tests and so O(n^2). Each successful merge restarts the scan, and a chain of `n` intervals where each overlaps only its neighbour needs `n - 1` merges. The worst case is therefore O(n^3). For `n = 2,000` that is about 8 billion pair tests, far too slow for an interactive tool.

The pair tests are mostly wasted. Interval `[1,4]` never needs a comparison with `[100,120]`. The method makes it anyway, because the order does not say which intervals are close. The waste comes from comparing intervals in an arbitrary order, so the fix has to be an order that tells the method where to look.

<!-- stage: insight -->
### Sort By Start To Compare One Interval

An order is useful when it turns a question about all earlier intervals into a question about one earlier interval. Sorting by start does this. Write the intervals so that each start is at least as large as the start before it. Every unprocessed interval then begins at or after every processed start. An unprocessed interval can reach a processed one only through the largest end among the processed intervals, and the merged scan keeps exactly that end.

#### The Comparator Defines The Order

In Java, a **comparator** is a function of two items. It returns a negative number when the first item goes first and zero when the two are equivalent. It returns a positive number when the second item goes first. `Arrays.sort(int[][], comparator)` calls it to place the rows.

<!-- names: comparator, tie rule, overflow -->

#### The Tie Rule Settles Equal Starts

Two intervals can share a start, such as `[1,2]` and `[1,9]`. The **tie rule** is the second key that orders them. Sorting by end after start gives a fixed order, so repeated runs and different input orders produce the same output. For merging, either order of equal starts works, but a fixed rule keeps results reproducible and prepares the end-based orders of later lessons.

#### Overflow Makes Subtraction Unsafe

A comparator like `a[0] - b[0]` is short, but the subtraction can **overflow**. Overflow means the true result does not fit in 32 bits, so the stored value wraps to the opposite sign. For starts `-2,000,000,000` and `2,000,000,000` the true difference is `-4,000,000,000`, and the wrapped result is positive, so the comparator puts the smaller start last. `Integer.compare(a[0], b[0])` compares without subtracting, so it never overflows.

<!-- stage: variables -->
### What An Ordered Scan Reads

The ordering needs four pieces of state, and each one has a fixed meaning.

- **intervals** is the array of pairs, where `iv[0]` is the start and `iv[1]` is the end.
- **comparator** decides which of two pairs goes first, using the start and then the end.
- **sorted** is a copy of `intervals` in comparator order, so the caller's array keeps its order.
- **i** is the position in `sorted` that the scan has reached; positions before `i` are already processed.

<!-- stage: trace -->
### Checking Two Orders Step By Step

#### Equal Starts Use The Tie Rule

Take the intervals `[5,8]`, `[1,4]`, `[1,2]`, `[3,6]`. The sorted order by start and then end is `[1,2]`, `[1,4]`, `[3,6]`, `[5,8]`. In the trace below, the cells hold the sorted starts, and the pointer `i` marks the pair under test, namely `sorted[i - 1]` and `sorted[i]`.

At `i = 1` the starts tie at 1, so the comparator reads the ends 2 and 4 and keeps `[1,2]` first. At `i = 2` and `i = 3` the starts differ, so the start alone decides.

```trace
{"cells":[1,1,3,5],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"sorted":"[1,2] [1,4] [3,6] [5,8]"},"note":"The sorted order by start and then end is ready. The pointer is before the first pair."},{"at":{"i":1},"vars":{"prev":"[1,2]","cur":"[1,4]","deciding key":"end"},"note":"The starts tie at 1, so the ends 2 and 4 decide. The interval with end 2 goes first."},{"at":{"i":2},"vars":{"prev":"[1,4]","cur":"[3,6]","deciding key":"start"},"note":"The starts differ, 1 before 3, so the start alone decides."},{"at":{"i":3},"vars":{"prev":"[3,6]","cur":"[5,8]","deciding key":"start"},"note":"The starts differ, 3 before 5, so the start alone decides."}]}
```

#### Subtraction Wraps Around

Now take two intervals whose starts lie at the extremes of the `int` range. The cell values are the two starts, -2,000,000,000 and 2,000,000,000, and the pointer `i` marks the second one. The subtraction comparator computes `a[0] - b[0]` for `a = sorted[1]` and `b = sorted[0]`. The true difference is 4,000,000,000, which does not fit in an `int`. The wrapped value is negative, so the comparator claims the larger start belongs first.

```trace
{"cells":[-2000000000,2000000000],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"sorted[0].start":"-2000000000"},"note":"The first start is -2,000,000,000, the smaller of the two."},{"at":{"i":1},"vars":{"true difference":"4000000000","wrapped difference":"-294967296"},"note":"The true difference a minus b is 4,000,000,000, which exceeds the int maximum of 2,147,483,647, so the stored result wraps to -294,967,296."},{"at":{"i":1},"vars":{"subtraction says":"a first","Integer.compare says":"b first"},"note":"The negative wrapped value tells the sort that the larger start goes first. Integer.compare returns 1 for the same pair and keeps the smaller start first."}]}
```

<!-- stage: code -->
### Sorting In Java Without Subtraction

#### Sort By Start Then End

The method copies the rows first, so the input array keeps its order, and then sorts the copy.

```java
static int[][] sortByStart(int[][] intervals) {
    int[][] sorted = intervals.clone();
    Arrays.sort(sorted, (a, b) -> a[0] != b[0]
            ? Integer.compare(a[0], b[0])
            : Integer.compare(a[1], b[1]));
    return sorted;
}
```

#### Sort By End Then Start

The second order keeps the same shape and swaps the key positions. Later lessons use it for selection problems.

```java
static int[][] sortByEnd(int[][] intervals) {
    int[][] sorted = intervals.clone();
    Arrays.sort(sorted, (a, b) -> a[1] != b[1]
            ? Integer.compare(a[1], b[1])
            : Integer.compare(a[0], b[0]));
    return sorted;
}
```

Both methods cost O(n log n) time for the sort and O(n) space for the cloned array of row references. The rows themselves are shared with the input, so changing a row changes both arrays. A sort by objects with a comparator runs a stable merge sort variant, so equal items keep their input order.

<!-- stage: applicability -->
### When The Sort Key Fits

#### State The Order In Terms Of The Question

The invariant of this lesson is that every processed interval comes before every unprocessed interval under the chosen comparator. Pick the key from the decision the scan makes. A scan that grows a union needs start order, because the next start can touch only the current union. A scan that keeps the earliest finishing interval needs end order, because the first interval in that order leaves the most room.

#### Sorting By End Does Not Merge

Sorting by end is a false friend for merging. Take `[1,10]`, `[2,3]`, `[4,5]`. In end order the intervals are `[2,3]`, `[4,5]`, `[1,10]`. The scan keeps `[2,3]`, appends `[4,5]` as a separate interval, and then compares `[1,10]` only with `[4,5]`. It outputs `[2,3]` and `[1,10]`, which overlap. Start order puts `[1,10]` first, and both later intervals fall inside it.

#### When Not To Sort

Do not sort when the input contract already promises order. Sorting costs O(n log n), and a later lesson shows an input sorted by start and disjoint that needs only one pass. Also remember that `Arrays.sort` on the caller's array changes the caller's data, so copy first unless the contract allows mutation.

<!-- stage: exercises -->
### Exercises

#### [Build] Order By Start Then End (Author exercise)
<!-- id: iv-order-start-end -->

**Prerequisites.** The comparator and the tie rule in this lesson.

**Problem.** An interval is an array `[start, end]` of two integers with `start <= end`. Given an array of intervals, return a new array that holds the same intervals ordered by `start` ascending. When two intervals have equal `start`, the interval with the smaller `end` comes first. Intervals that are equal in both values keep any relative order.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start <= end`.
- **Return** is a new array; an empty input gives an empty array.
- **Mutation** is not allowed; the order of `intervals` stays as given.

**Example 1.** Input `[[5,8],[1,4],[1,2],[3,6]]`, output `[[1,2],[1,4],[3,6],[5,8]]`.

**Example 2.** Input `[[2,2],[2,2],[1,3]]`, output `[[1,3],[2,2],[2,2]]`.

**Hint.** Write the comparator for two rows `a` and `b`. Which key decides first, and which key decides when the first one ties?

**Changed decision.** Basic case: a comparator with two keys replaces an arrival order.

#### [Vary] Order By End Then Start (Author exercise)
<!-- id: iv-order-end-start -->

**Prerequisites.** The exercise above.

**Problem.** Each interval is a pair `[start, end]`, and its end is never below its start. Given an array of intervals, return a new array ordered by `end` ascending, and by `start` ascending when two ends are equal. Then state which decision the first interval of that order makes possible. The goal is to choose as many intervals as possible with no shared point.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start <= end`.
- **Return** is a new array; an empty input gives an empty array.
- **Mutation** is not allowed; `intervals` keeps its order.

**Example 1.** Input `[[1,10],[2,3],[4,5]]`, output `[[2,3],[4,5],[1,10]]`.

**Example 2.** Input `[[3,6],[1,6],[2,4]]`, output `[[2,4],[1,6],[3,6]]`.

**Hint.** Swap the roles of the two keys. Which interval finishes first, and how much room does it leave to the right?

**Changed decision.** The first key moves from the start to the end, which changes the scan from growing a union to keeping the earliest finish.

#### [Boundary] Equal And Extreme Endpoints (Author exercise)
<!-- id: iv-extreme-endpoints -->

**Prerequisites.** The two exercises above.

**Problem.** Take intervals written as `[start, end]` with the start no larger than the end. Return the intervals ordered by `start` ascending and then `end` ascending. The values can be as small as `Integer.MIN_VALUE` and as large as `Integer.MAX_VALUE`, so the order must be correct for every pair of `int` values.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are any `int` values, including both extremes, with `start <= end`.
- **Ties** in both keys keep any relative order.
- **Mutation** is not allowed; the input array keeps its order.

**Example 1.** Input `[[2147483647,2147483647],[-2147483648,0],[0,5],[0,3]]`, output `[[-2147483648,0],[0,3],[0,5],[2147483647,2147483647]]`.

**Example 2.** Input `[[-2000000000,1],[2000000000,2000000000]]`, output `[[-2000000000,1],[2000000000,2000000000]]`.

**Hint.** What does `a[0] - b[0]` return for the two starts of Example 2? Compare the values without subtracting them.

**Changed decision.** The comparator drops subtraction, because the difference of two `int` values can leave the `int` range.

#### [Recognize] Count Groups After Merging (LeetCode 56)
<!-- id: iv-count-merged-groups -->

**Prerequisites.** All three exercises above.

**Problem.** This exercise uses the setting of LeetCode 56 but changes the output. Given an array of closed intervals `[start, end]`, two intervals belong to the same group when a chain of overlapping intervals links them. Two closed intervals overlap when they share at least one point, so `[1,3]` and `[3,5]` overlap. Return the number of groups. Choose the sort key before writing the scan, and explain why only the last group can accept the next interval.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start <= end`.
- **Return** is a single `int`, which is 0 for an empty input.
- **Mutation** is not allowed; the input array keeps its order.

**Example 1.** Input `[[1,4],[7,9],[2,5]]`, output 2, because `[1,4]` and `[2,5]` form one group.

**Example 2.** Input `[[1,3],[3,5],[6,8],[10,12],[11,13]]`, output 3.

**Hint.** After sorting by start, compare each start with the largest end of the current group. When does the count increase?

**Changed decision.** The scan counts group boundaries and builds no merged list, but the sort key stays the start.
