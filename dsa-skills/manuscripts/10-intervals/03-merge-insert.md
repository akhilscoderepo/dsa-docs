<!-- lesson-kind: standard -->
<!-- lesson-id: merge-insert -->
## Merge Intervals And Insert A New One

<!-- stage: context -->
### Outage Windows That Must Become Bars

A monitoring page lists every outage as a window of minutes, such as `[8,10]`, `[1,3]`, `[2,6]` and `[15,18]`. The page draws one bar for each stretch of time with an outage. The windows `[1,3]` and `[2,6]` must therefore become one bar from minute 1 to minute 6. The previous lesson settled when two windows overlap. Counting the bars does not help here, because the page needs the start and end of every bar. A second feature adds one new window to a list that is already sorted and has no overlaps. The page must redraw only what changed.

Both features ask for the same result, a list of non-overlapping windows that covers exactly the same minutes as the input. The lesson has two goals, each stated as a question. What must a single scan remember to build that list, and what does the scan skip when the list is already in order?

<!-- stage: naive -->
### Add Each Window To The Result

The simple method builds the result one window at a time. For each new window, it scans the whole result so far. Every result entry that overlaps the new window is removed, and the new window grows to cover it. After the scan, the grown window joins the result. Overlap uses the closed model, so touching windows overlap.

```java
static int[][] mergeByInsertion(int[][] windows) {
    List<int[]> result = new ArrayList<>();
    for (int[] w : windows) {
        int start = w[0], end = w[1];
        List<int[]> kept = new ArrayList<>();
        for (int[] r : result) {
            if (r[0] <= end && start <= r[1]) {
                start = Math.min(start, r[0]);
                end = Math.max(end, r[1]);
            } else {
                kept.add(r);
            }
        }
        kept.add(new int[] {start, end});
        result = kept;
    }
    result.sort((a, b) -> Integer.compare(a[0], b[0]));
    return result.toArray(new int[result.size()][]);
}
```

On the four outage windows the method returns `[1,6]`, `[8,10]` and `[15,18]`, which is correct. It does not depend on the input order. Each new window absorbs every overlap at once, so two entries of the result never need merging with each other.

<!-- stage: bottleneck -->
### Counting The Scans Of The Result

```predict
A list of non-overlapping intervals is sorted by start, and one new interval arrives. Which intervals of the list can overlap the new one, and where do they sit in the list?

They form one unbroken block. Every interval before the block ends before the new start, and every interval after the block starts after the new end. One left-to-right pass finds the block, so the insert costs O(n) and not a pass for each pair.
```

Each of the `n` windows scans a result that can hold up to `n` entries. The method therefore makes about `n * n / 2` overlap tests, which is O(n^2). For `n = 100,000` that is 5 billion tests. The final sort adds O(n log n) and does not change the order of growth.

The scan repeats work in two ways. First, it tests entries far to the left of the new window. Once the windows are ordered, none of them can overlap it. Second, it rebuilds the whole result list each time, even when the new window touches nothing. The two sources of waste both come from ignoring order, and the next stage shows how an order removes both.

<!-- stage: insight -->
### Keep One Open Interval At The End

An order lets the scan look in one place only. Sort the windows by start, as the first lesson showed. Then keep one **active interval**, the last entry of the result. It is the only entry that can still grow, because every later window starts at or after its start. A window that starts at or before the active end joins it. A window that starts after the active end cannot join it, and no later window can either, because later starts are not smaller.

#### Finalized Intervals Never Change

When a window starts after the active end, it becomes the new active interval. The old active interval turns into a **finalized interval**: no later window overlaps it, so its start and end stay fixed. The result is therefore a list of finalized intervals followed by one active interval.

<!-- names: active interval, finalized interval, overlapping block -->

#### Growing The Active End Takes The Larger End

A joining window can end before the active end, as `[2,3]` does after `[1,10]`. The active end must become the larger of the two ends, never simply the end of the newest window. A smaller end would shrink the interval and lose coverage.

#### An Insert Needs No Sort

Insert has more structure, because the list is already sorted by start and has no overlaps. The intervals that overlap the new one form an **overlapping block**, an unbroken run of neighbours. Intervals before the block end before the new start, and intervals after the block start after the new end. One pass handles the three parts in order. It copies the intervals that end before the new start, absorbs the block into the new interval, and copies the rest. The pass costs O(n), and a sort would add a factor of log n for no gain.

<!-- stage: variables -->
### What Merge And Insert Each Keep

The two scans use five pieces of state between them.

- **sorted** holds the windows in start order in the merge scan, a copy that leaves the input untouched.
- **result** is a `List<int[]>` of finalized intervals plus the active interval at its end.
- **active** is the last entry of `result`, and the next window is tested against its end.
- **start** and **end** are the bounds of the new interval during an insert, and they grow as the block is absorbed.
- **i** is the index of the next unprocessed list entry in the insert scan, and the merge scan needs no index.

<!-- stage: trace -->
### Tracing A Merge And An Insert

#### Merging Five Windows

Take the windows `[8,10]`, `[1,3]`, `[2,6]`, `[6,7]`, `[15,18]`. After sorting by start they read `[1,3]`, `[2,6]`, `[6,7]`, `[8,10]`, `[15,18]`. The trace lists the sorted starts as cells, and the pointer `i` marks the window under test.

The window `[2,6]` starts at 2, which is at most the active end 3, so it joins and the end becomes 6. The window `[6,7]` starts at 6, which equals the active end, so it joins under the closed model and the end becomes 7. The window `[8,10]` starts after 7, so it opens a new active interval.

```trace
{"cells":[1,2,6,8,15],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"result":"none"},"note":"The windows are sorted by start. The result is empty."},{"at":{"i":0},"vars":{"window":"[1,3]","result":"[1,3]"},"note":"The result is empty, so [1,3] becomes the active interval."},{"at":{"i":1},"vars":{"window":"[2,6]","result":"[1,6]"},"note":"The start 2 is at most the active end 3, so the window joins and the active end becomes 6."},{"at":{"i":2},"vars":{"window":"[6,7]","result":"[1,7]"},"note":"The start 6 is at most the active end 6, so the window joins and the active end becomes 7."},{"at":{"i":3},"vars":{"window":"[8,10]","result":"[1,7] [8,10]"},"note":"The start 8 is after the active end, or the result is empty, so [8,10] opens a new active interval."},{"at":{"i":4},"vars":{"window":"[15,18]","result":"[1,7] [8,10] [15,18]"},"note":"The start 15 is after the active end, or the result is empty, so [15,18] opens a new active interval."}]}
```

#### Inserting One Interval

Now take the sorted list `[1,2]`, `[3,5]`, `[6,7]`, `[8,10]`, `[12,16]` and the new interval `[4,9]`. The cells are the starts of the list. The pointer `i` marks the list entry under test, and the vars record the part of the pass and the growing interval.

The entry `[1,2]` ends before 4, so it is copied. The next three entries start at or before 9, so each is absorbed. The entry `[12,16]` starts after 9, which ends the block, so the grown interval is written and the entry is copied.

```trace
{"cells":[1,3,6,8,12],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"new":"[4,9]","part":"start"},"note":"The list is sorted and has no overlaps. The new interval is [4,9]."},{"at":{"i":0},"vars":{"part":"copy before","output":"[1,2]"},"note":"The entry [1,2] ends before 4, so it is copied."},{"at":{"i":1},"vars":{"part":"absorb","merged":"[3,9]"},"note":"The entry [3,5] starts at or before the merged end, so the merged interval becomes [3,9]."},{"at":{"i":2},"vars":{"part":"absorb","merged":"[3,9]"},"note":"The entry [6,7] starts at or before the merged end, so the merged interval becomes [3,9]."},{"at":{"i":3},"vars":{"part":"absorb","merged":"[3,10]"},"note":"The entry [8,10] starts at or before the merged end, so the merged interval becomes [3,10]."},{"at":{"i":4},"vars":{"part":"write merged","output":"[1,2] [3,10]"},"note":"The entry [12,16] starts after the merged end 10, so the block ends. The merged interval [3,10] is written."},{"at":{"i":5},"vars":{"part":"copy after","output":"[1,2] [3,10] [12,16]"},"note":"The remaining entries are copied unchanged. The pass is complete."}]}
```

<!-- stage: code -->
### Merging And Inserting In Java

#### Merge With One Scan

The method copies each row before it extends one, so the caller's rows never change. The last line converts the list to the array type that the caller needs.

```java
static int[][] merge(int[][] windows) {
    int[][] sorted = windows.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> result = new ArrayList<>();
    for (int[] w : sorted) {
        if (result.isEmpty() || result.get(result.size() - 1)[1] < w[0]) {
            result.add(new int[] {w[0], w[1]});
        } else {
            int[] active = result.get(result.size() - 1);
            active[1] = Math.max(active[1], w[1]);
        }
    }
    return result.toArray(new int[result.size()][]);
}
```

#### Insert Into A Sorted List

The three loops share one index, so each list entry is visited exactly once.

```java
static int[][] insert(int[][] list, int[] add) {
    List<int[]> result = new ArrayList<>();
    int i = 0, n = list.length;
    int start = add[0], end = add[1];
    while (i < n && list[i][1] < start) result.add(list[i++]);
    while (i < n && list[i][0] <= end) {
        start = Math.min(start, list[i][0]);
        end = Math.max(end, list[i][1]);
        i++;
    }
    result.add(new int[] {start, end});
    while (i < n) result.add(list[i++]);
    return result.toArray(new int[result.size()][]);
}
```

The merge spends O(n log n) time sorting and holds O(n) entries in its result. The insert needs O(n) time and O(n) space. The conversion `toArray(new int[size][])` is an output step and not a speed-up, because it copies `size` row references once.

<!-- stage: applicability -->
### When Merge And Insert Apply

#### State What Stays True

The invariant of both scans is that every entry before the active interval is finalized and disjoint from everything after it. Use the merge scan when the goal is a union of ranges. Busy bars, covered address blocks and minutes with an outage are examples. Use the insert scan when the input is already sorted by start and has no overlaps. The two conditions are a contract of the input, and the scans rely on both without checking them.

#### Appending Then Merging Is A False Friend

Appending the new interval to the list and running the merge scan gives the same answer for an insert. It is a false friend, because it costs O(n log n) for a sort that the sorted input already makes unnecessary. It also copies work that the three-part pass avoids. Use it only when the list is not guaranteed to be sorted.

#### Mutation And The Touching Rule

Extending `active[1]` in place changes a row of the result. The result rows must be copies, as the merge method does, or the caller's input changes too. The comparisons also depend on the model. The closed model uses `<` to start a new interval and `<=` to join one, as above, and the half-open model swaps the two.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Intervals (LeetCode 56)
<!-- id: iv-merge-intervals -->

**Prerequisites.** The sort order from the first lesson and the closed overlap test from the second.

**Problem.** Given an array of closed intervals `[start, end]`, return an array of closed intervals that covers exactly the same integers. No two returned intervals overlap. Intervals that share an end coordinate overlap and must merge. Return the result ordered by start.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start <= end`.
- **Order** of the input is arbitrary and may contain equal intervals.
- **Mutation** is not allowed; the input array and its rows keep their values.

**Example 1.** Input `[[8,10],[1,3],[2,6],[6,7],[15,18]]`, output `[[1,7],[8,10],[15,18]]`.

**Example 2.** Input `[[3,4],[1,3],[7,7]]`, output `[[1,4],[7,7]]`.

**Hint.** Sort by start first. Compare each start with the end of the last interval in the result.

**Changed decision.** Basic case: the active end grows to the larger of two ends.

#### [Vary] Merge Already-Sorted Intervals (Author exercise)
<!-- id: iv-merge-sorted -->

**Prerequisites.** The exercise above.

**Problem.** Given closed intervals `[start, end]` that are already ordered by start, return the merged intervals in the same form as the previous exercise. The input contract promises the order, so the method must not sort.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start <= end`.
- **Order** is non-decreasing by start, with ends in any order.
- **Time** must be O(n), and the input stays unchanged.

**Example 1.** Input `[[1,2],[2,2],[5,9],[6,7]]`, output `[[1,2],[5,9]]`.

**Example 2.** Input `[[0,0],[1,1],[2,3]]`, output `[[0,0],[1,1],[2,3]]`.

**Hint.** The sort was only there to give the order that the contract now supplies.

**Changed decision.** The sort disappears, and the cost drops from O(n log n) to O(n).

#### [Boundary] One Interval Covers Many (Author exercise)
<!-- id: iv-one-covers-many -->

**Prerequisites.** The two exercises above.

**Problem.** Given closed intervals `[start, end]` ordered by start, merge them as before. Return an `int[]` that holds, for each merged interval in order, how many input intervals it absorbed.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start <= end`, and ends are not ordered.
- **Order** of the input is non-decreasing by start.
- **Return** is an `int[]` whose sum equals the input length; it is empty for an empty input.

**Example 1.** Input `[[1,10],[2,3],[4,5]]`, output `[3]`, because the first interval covers both later ones.

**Example 2.** Input `[[0,20],[1,2],[3,4],[20,25],[26,27]]`, output `[4,1]`.

**Hint.** What does the active end become when a window ends before it? Try the first example with each choice.

**Changed decision.** The active end keeps the larger end, never the end of the newest window.

#### [Recognize] Insert Interval (LeetCode 57)
<!-- id: iv-insert-interval -->

**Prerequisites.** All three exercises above.

**Problem.** Given closed intervals ordered by start with no two overlapping, and one new closed interval, return the closed intervals that cover the integers of the list and the new interval together. No two returned intervals overlap, and they are ordered by start. The method must make one pass and must not sort.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start <= end` for every interval, including the new one.
- **Order** of the list is by start, and its intervals do not overlap.
- **Mutation** is not allowed; the input list and the new interval keep their values.

**Example 1.** Input `[[2,4],[6,7],[9,12]]` and new interval `[5,10]`, output `[[2,4],[5,12]]`.

**Example 2.** Input `[[1,2],[3,5]]` and new interval `[2,3]`, output `[[1,5]]`, because both neighbours touch it.

**Hint.** Which intervals end before the new start? Which start after the new end? What happens to the ones in between?

**Changed decision.** The three parts of the list replace the sort, because the list is already in order.
