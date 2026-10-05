<!-- lesson-kind: combination -->
<!-- lesson-id: sort-then-scan -->
## Sort Intervals Then Scan Once

<!-- stage: context -->
### One List, Four Different Reports

A maintenance team keeps one list of closed work windows, such as `[5,7]`, `[1,4]`, `[3,6]` and `[9,9]`. Management asks four questions about it. How many hours does at least one window cover? What does the list look like after one more window is added? How many windows can run without any two sharing an hour? How few inspection visits reach every window? A developer sorts the list by start for the first question and gets it right. The same sort for the third question can keep one long window and reject several short windows that would have fit.

The list is the same in all four questions, and the sort order that works changes with the question. The task here is to answer one question. How do you pick the order, and the one value to carry through the scan, for each of the four questions?

<!-- stage: contributions -->
### What Sorting And Interval Rules Each Add

Two earlier ideas combine in this lesson, and each supplies a different part. Sorting supplies an order in which every processed interval comes before every unresolved one. After that order exists, one value can describe everything that has been processed. Sorting alone cannot say which value that is, or whether a new interval joins, replaces or skips an old one.

The interval rule supplies the test for two intervals: whether touching ends overlap, as the lesson on touching ends showed. The same scan gives different answers under the closed model and the half-open model. The pairing therefore needs an order from sorting and a test from the interval rule. The question dictates the carried value.

<!-- stage: naive -->
### Check Every Earlier Interval For Each Question

Without an order, each question rechecks the whole list. To find the hours covered by at least one window, the method marks every hour of every window in a boolean array. The array spans the whole coordinate range. The method then counts the marked hours.

```java
static long coveredHoursByMarking(int[][] windows, int low, int high) {
    boolean[] marked = new boolean[high - low + 1];
    for (int[] w : windows) {
        for (int h = w[0]; h <= w[1]; h++) marked[h - low] = true;
    }
    long total = 0;
    for (boolean m : marked) if (m) total++;
    return total;
}
```

On the four maintenance windows with `low = 1` and `high = 9`, the method returns 8, which is correct. Each of the other three questions needs its own search over all earlier windows in the same way.

<!-- stage: bottleneck -->
### Counting The Marks

```predict
After the intervals are sorted by start, one number summarises every interval processed so far for the union question. Which number is it? After sorting by end for a selection question, which number summarises the kept intervals?

For the union question it is the largest end among the processed intervals. For selection it is the end of the last kept interval. One number lets each new interval be decided with one comparison.
```

The marking method visits every hour of every window. It costs O(n * R) for `n` windows whose spans are at most `R` hours, and it needs a boolean array of the full range `R`. When the coordinates are times in milliseconds, `R` reaches billions and the array does not fit in memory. The cost depends on the size of the coordinates and not only on the number of windows.

The method also cannot answer the third and fourth questions. Marking says nothing about which windows to drop or where to place a visit. An order and a single carried value remove both difficulties, and the cost then depends only on `n`.

<!-- stage: insight -->
### Pick The Sort Key From The Question

The scan keeps one **local state**, a single value that stands for all processed intervals. The question decides which value it is, and the value decides the **sort key**, the field by which the list is ordered.

#### Union Questions Sort By Start

For a union, such as covered length or merged intervals, the sort key is the start. The local state is the active end, the largest end of the interval that is still growing. A new interval joins it when it overlaps the active interval under the stated model. Otherwise the old interval is finished and added to the answer. The first lesson explained why only the active interval can still grow.

<!-- names: local state, sort key, safe move -->

#### Selection And Shared Points Sort By End

For selection, the sort key is the end. The local state is the end of the last kept interval. A new interval that does not overlap the last kept interval is kept, and any other is skipped. The same key with a different local state answers the shared-point question. The local state is the position of the current arrow. An interval that starts past the arrow needs a new arrow at its own end, and every other interval is burst by the current arrow.

#### The Safe Move In Each Scan

The **safe move** is the step that never loses an optimal answer. For the union it is to extend the active end to the larger end. For selection and for arrows it is to commit to the smallest end among the unresolved intervals. In both cases the committed value is final, because every later interval starts at or after the order's current position.

#### Sorted Input Removes The Sort

When the input is already ordered and disjoint, as for an insert, the sort key is supplied by the contract. The scan splits the list into the intervals before the new one, the ones it absorbs, and the ones after it, and it never sorts.

<!-- stage: variables -->
### What Each Scan Carries

All four scans share one shape, and only the carried value differs.

- **sorted** is the clone ordered by the sort key, so the input stays as given.
- **activeEnd** is the largest end of the growing interval in a union scan.
- **lastKept** is the end of the last kept interval in a selection scan.
- **arrow** is the coordinate of the current arrow in a shared-point scan.
- **answer** is the running total, count or output list.

<!-- stage: trace -->
### Tracing A Union And An Arrow Scan

#### Covered Length By Start Order

Take the closed windows `[5,7]`, `[1,4]`, `[3,6]` and `[9,9]`. Sorted by start they read `[1,4]`, `[3,6]`, `[5,7]`, `[9,9]`. The cells hold the sorted starts, and the pointer `i` marks the window under test.

The window `[3,6]` starts inside the active interval, so the active end grows from 4 to 6. The window `[5,7]` also starts inside it, and the end grows to 7. The window `[9,9]` starts after 7. The active interval `[1,7]` is finished and adds 7 hours, and `[9,9]` becomes the active interval with 1 hour.

```trace
{"cells":[1,3,5,9],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"active":"none","covered":0},"note":"The windows are sorted by start. Nothing has been read yet."},{"at":{"i":0},"vars":{"active":"[1,4]","covered":0},"note":"The first window [1,4] becomes the active interval."},{"at":{"i":1},"vars":{"active":"[1,6]","covered":0},"note":"The start 3 is at most the active end, so the window joins and the active end becomes 6."},{"at":{"i":2},"vars":{"active":"[1,7]","covered":0},"note":"The start 5 is at most the active end, so the window joins and the active end becomes 7."},{"at":{"i":3},"vars":{"active":"[9,9]","covered":7},"note":"The start 9 is after the active end 7, so [1,7] is finished and adds 7 hours. The window [9,9] becomes active."},{"at":{"i":4},"vars":{"active":"none","covered":8},"note":"The last active interval adds 1 hour. The total is 8 hours."}]}
```

#### Arrows By End Order

Now take the balloons `[10,16]`, `[2,8]`, `[1,6]` and `[7,12]`. Sorted by end they read `[1,6]`, `[2,8]`, `[7,12]`, `[10,16]`, and the cells hold those ends. The first arrow goes to 6, the smallest end. It bursts `[2,8]` as well, since 2 is at most 6. The balloon `[7,12]` starts after 6, so it needs a second arrow at 12, and that arrow also bursts `[10,16]`.

```trace
{"cells":[6,8,12,16],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"arrows":"none"},"note":"The balloons are sorted by end."},{"at":{"i":0},"vars":{"arrows":"[6]"},"note":"The first arrow goes to the smallest end, 6."},{"at":{"i":1},"vars":{"arrows":"[6]"},"note":"The start 2 is at most the arrow at 6, so the arrow bursts [2,8]."},{"at":{"i":2},"vars":{"arrows":"[6, 12]"},"note":"The start 7 is after the arrow at 6, so the arrow misses [7,12]. A new arrow goes to 12."},{"at":{"i":3},"vars":{"arrows":"[6, 12]"},"note":"The start 10 is at most the arrow at 12, so the arrow bursts [10,16]."}]}
```

<!-- stage: code -->
### Writing The Scans In Java

#### Hours Covered By A Union

The method sorts a clone by start, keeps the growing interval in two locals, and adds each finished interval's length. The length uses `long` arithmetic, because one interval can span the whole `int` range.

```java
static long coveredHours(int[][] windows) {
    if (windows.length == 0) return 0;
    int[][] s = windows.clone();
    Arrays.sort(s, (a, b) -> Integer.compare(a[0], b[0]));
    long total = 0;
    long from = s[0][0], to = s[0][1];
    for (int i = 1; i < s.length; i++) {
        if (s[i][0] <= to) {
            to = Math.max(to, s[i][1]);
        } else {
            total += to - from + 1;
            from = s[i][0];
            to = s[i][1];
        }
    }
    return total + (to - from + 1);
}
```

#### Positions Of Arrows

The scan sorts by end and records the position of each new arrow in an `int` array.

```java
static int[] arrowPositions(int[][] balloons) {
    if (balloons.length == 0) return new int[0];
    int[][] s = balloons.clone();
    Arrays.sort(s, (a, b) -> Integer.compare(a[1], b[1]));
    int[] out = new int[s.length];
    int k = 0;
    int arrow = s[0][1];
    out[k++] = arrow;
    for (int i = 1; i < s.length; i++) {
        if (s[i][0] > arrow) {
            arrow = s[i][1];
            out[k++] = arrow;
        }
    }
    return Arrays.copyOf(out, k);
}
```

In both scans the sort sets the cost at O(n log n) time, and the clone takes O(n) space. The loop itself adds O(n) time and O(1) extra space, apart from the output array of the second method.

<!-- stage: applicability -->
### Choosing The Order For A New Question

#### Read The Decision And The Test

The invariant of every scan in this lesson is that the carried value summarises all processed intervals under the sort key. Read the question and name its decision: union, replace, keep or place. Then name the test that the interval rule gives. A union and a count of kept intervals can both be answered from the same list, and the two questions use different keys.

#### Wrong Key Pairings Fail

Pairing a decision with the wrong key is a false friend, and it fails on small inputs. Sorting by end for a union loses the extension of a long interval. Sorting by start for selection keeps the first long interval and rejects short ones that fit. Merging before selecting is also wrong, because a merge destroys the original intervals that the selection must count.

#### When The Pairing Stops Working

The pairing needs one carried value. A question that needs several active intervals at once cannot be summarised by one end. The number of rooms in use is an example, and Chapter 17 adds a heap for that case. A question that attaches weights to intervals needs dynamic programming, because a greedy commitment can lose weight. State the interval rule before writing any comparison, because the closed and half-open models give different counts on touching input.

<!-- stage: exercises -->
### Exercises

#### [Build] Covered Length After Merging (LeetCode 56)
<!-- id: iv-comb-covered-length -->

**Prerequisites.** The sort order of the first lesson and the merge scan of the third lesson.

**Problem.** This exercise uses the closed intervals of LeetCode 56 and changes the output. Given closed intervals `[start, end]`, return the number of integers that lie in at least one interval. An integer belongs to an interval when `start <= x <= end`.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are any `int` values with `start <= end`, including both extremes.
- **Return** is a `long`, because the count can exceed the `int` range.
- **Mutation** is not allowed; the input keeps its order and values.

**Example 1.** Input `[[5,7],[1,4],[3,6],[9,9]]`, output 8.

**Example 2.** Input `[[-2147483648,2147483647]]`, output 4294967296.

**Hint.** Sort by start and keep the growing interval. When is an interval finished, and what does it add?

**Changed decision.** The scan adds lengths to a running total, and it builds no merged list.

#### [Vary] Insert Interval Under A Half-Open Rule (LeetCode 57)
<!-- id: iv-comb-insert-half-open -->

**Prerequisites.** The exercise above and the half-open model from the second lesson.

**Problem.** This exercise uses the setting of LeetCode 57 and changes the model. Given half-open intervals `[start, end)` sorted by start, and one new half-open interval, return the list with every group of overlapping intervals merged into one. Intervals that only touch, such as `[1,3)` and `[3,5)`, do not overlap and stay separate. The method must not sort.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start < end`, including the new interval.
- **Order** of the list is by start, and the list intervals do not overlap each other.
- **Return** is an `int[][]` ordered by start, and the input is not modified.

**Example 1.** Input `[[1,3],[3,5],[7,9]]` and new interval `[4,8]`, output `[[1,3],[3,9]]`.

**Example 2.** Input `[[1,3],[5,6]]` and new interval `[3,5]`, output `[[1,3],[3,5],[5,6]]`.

**Hint.** Which comparison separates the intervals before the new one from the ones it absorbs? Does a touching end belong to the block?

**Changed decision.** The three-part pass uses `<` and `>` where the closed rule used `<=`.

#### [Boundary] Closed Schedule Size (LeetCode 435)
<!-- id: iv-comb-closed-schedule -->

**Prerequisites.** The two exercises above and the selection scan of the fifth lesson.

**Problem.** This exercise uses the setting of LeetCode 435 and changes the model and the output. Given closed intervals `[start, end]`, two intervals conflict when they share an integer, so touching intervals conflict. Return the largest number of intervals that can be kept so that no two kept intervals conflict.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are any `int` values with `start <= end`, including both extremes.
- **Return** is a single `int`, and the input is not modified.
- **Ties** include equal intervals and intervals that share one end coordinate.

**Example 1.** Input `[[1,3],[3,5],[6,8]]`, output 2.

**Example 2.** Input `[[1,10],[2,3],[4,5],[6,7],[3,4]]`, output 3.

**Hint.** Sort by end. After a kept interval ends at `e`, which start values are still allowed under the closed rule?

**Changed decision.** A touching start now conflicts, so the keep test moves from `>=` to `>`.

#### [Recognize] List The Arrow Positions (LeetCode 452)
<!-- id: iv-comb-arrow-positions -->

**Prerequisites.** All three exercises above.

**Problem.** This exercise uses the setting of LeetCode 452 and asks for positions instead of a count. Each balloon spans the closed range `[start, end]`. A balloon is burst by an arrow at `x` when `start <= x <= end`. Return the coordinates of any smallest set of arrows that bursts every balloon, in increasing order.

**Constraints.** The limits are:
- **Length** is `0 <= balloons.length <= 10^5`.
- **Values** are any `int` values with `start <= end`, including both extremes.
- **Return** is an `int[]` in increasing order. Any smallest valid set is accepted.
- **Mutation** is not allowed; the input is not modified.

**Example 1.** Input `[[10,16],[2,8],[1,6],[7,12]]`, output `[6,12]`, one valid answer.

**Example 2.** Input `[[1,2],[2,3],[3,4]]`, output `[2,4]`, one valid answer.

**Hint.** Sort by end and shoot at the first unburst balloon's end. Which balloons does that arrow burst?

**Changed decision.** The scan records the arrow coordinates and not only how many there are.
