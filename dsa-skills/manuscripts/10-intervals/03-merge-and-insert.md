<!-- lesson-kind: standard -->
<!-- lesson-id: merge-and-insert -->
## Merge And Insert

<!-- stage: context -->
### Highway Repair Reports

A highway authority tracks repair work along a single long road. Crews phone in reports, each saying "we have resurfaced from kilometer 12 to kilometer 19", with both ends included. Reports come in at random: they overlap, they repeat, and sometimes one crew's stretch begins exactly where another's ended. The foreman keeps a board listing the stretches that are known to be repaired, and his rule is that the board must show unbroken stretches, so two reports that overlap or touch must be shown as one longer stretch.

Each time a report arrives, the foreman redraws the whole board from scratch: he lays out every report received so far, sorts them by starting kilometer, and joins neighbors. As the day goes on and the pile of reports grows, redrawing takes longer and longer, even though most of the board has not changed.

<!-- stage: naive -->
### Redraw The Board After Every Report

The direct approach is to keep all the reports, add the new one, sort everything, and merge neighbors again.

```java
static int[][] redraw(List<int[]> reports) {
    int[][] sorted = reports.toArray(new int[reports.size()][]);
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> board = new ArrayList<>();
    for (int[] r : sorted) {
        if (!board.isEmpty() && r[0] <= board.get(board.size() - 1)[1]) {
            int[] last = board.get(board.size() - 1);
            last[1] = Math.max(last[1], r[1]);
        } else {
            board.add(new int[] {r[0], r[1]});
        }
    }
    return board.toArray(new int[board.size()][]);
}
```

The board it produces is correct after every report, because it recomputes the whole answer from the full list each time.

<!-- stage: bottleneck -->
### The Board Is Rebuilt For Nothing

Sorting costs O(n log n) per redraw, so n reports that each trigger a redraw cost O(n^2 log n) in total. For a hundred thousand reports that is on the order of a hundred trillion steps. A new report touches only the stretches near it. Stretches far to the left end before it starts, and stretches far to the right begin after it ends, so neither changes.

Two separate savings are available. First, a single batch of reports needs sorting only once, followed by a single pass that grows one stretch while the next report overlaps it, which costs O(n log n) in all. Second, when the board is already sorted and disjoint, one new report can be placed by a single pass, in O(n), or O(log n) plus the work of the affected stretches, because the board needs no sorting at all. Both savings come from the same idea: only one stretch is ever still growing.

<!-- stage: insight -->
### One Open Stretch, Everything Else Final

While merging sorted reports, the output holds a list of stretches that can never change again, plus at most one **active interval** that the next report may still extend. The state is the invariant of the whole method: the finalized stretches are disjoint, they lie before the active one, and the active one begins no later than any unread report. A report either overlaps the active interval, in which case the active end becomes the larger of the two ends, or it starts after the active end, in which case the active interval is finalized and the report becomes the new active one. A report that starts exactly at the active end overlaps it under the closed contract, so it extends it.

Insertion into a board that is already sorted and disjoint needs no sorting because the board's order is the order the method would have produced. The new interval splits the board into **before-overlap-after** regions. Stretches that end before the new one starts go to the output unchanged. Stretches that overlap the new one are absorbed: the new interval's start becomes the smaller start, and its end the larger end, and it keeps growing as long as the next stretch overlaps it. Once the next stretch begins after the grown interval ends, the grown interval is written, and everything after it is copied unchanged.

<!-- names: active interval, before-overlap-after, finalized stretches -->

Two promises make the shortcut legal: the input is sorted by start, and its stretches are disjoint, with no two overlapping. If the promise is dropped, the scan must sort first. The shortcut also avoids a second trap, re-sorting an input that is already in order, which costs time and changes nothing. What matters for correctness is that the code states which promise it relies on.

<!-- stage: variables -->
### Output List, Active End, Cursor

`out` is the list of **finalized stretches** plus, at its tail, the active interval being grown. For merging an unsorted batch, the sort comes first, and for each report `r` the test compares `r[0]` with the end of the last element of `out`. For insertion, `i` is the cursor into the sorted board, `lo` and `hi` are the start and end of the new interval as it grows, and three loops move `i` forward through the three regions. At the end the list is converted to the required array with `toArray(new int[out.size()][])`.

<!-- stage: trace -->
### Growing One Stretch Across A Board

The first trace merges the reports 8 to 10, 1 to 3, 15 to 18 and 2 to 6. The cells are the reports in the order received, but the scan visits them in order of start, and each step names the active stretch. Pay attention to the second visited report, 2 to 6: it starts inside the active stretch 1 to 3, so the stretch grows to 1 to 6 and nothing is added to the output.

```trace
{"cells":["8-10","1-3","15-18","2-6"],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"activeStart":1,"activeEnd":3,"stretches":1},"note":"The report 1 to 3 starts past the active end, so it opens a new active stretch. The output now has 1 stretches."},{"at":{"i":3},"vars":{"activeStart":1,"activeEnd":6,"stretches":1},"note":"The report 2 to 6 starts inside the active stretch, so its end becomes 6 and nothing is added to the output."},{"at":{"i":0},"vars":{"activeStart":8,"activeEnd":10,"stretches":2},"note":"The report 8 to 10 starts past the active end, so it opens a new active stretch. The output now has 2 stretches."},{"at":{"i":2},"vars":{"activeStart":15,"activeEnd":18,"stretches":3},"note":"The report 15 to 18 starts past the active end, so it opens a new active stretch. The output now has 3 stretches."}]}
```

The second trace inserts the report 4 to 8 into the board 1 to 2, 3 to 5, 6 to 7, 8 to 10, 12 to 16. The cells are the board stretches, and each step classifies one of them. Look at the fourth stretch, 8 to 10: it begins exactly where the new report ends, so it is absorbed and the new report grows to 3 to 10.

```trace
{"cells":["1-2","3-5","6-7","8-10","12-16"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"newStart":4,"newEnd":8,"written":1},"note":"The stretch 1 to 2 ends before the new report starts at 4, so it is copied unchanged."},{"at":{"i":1},"vars":{"newStart":3,"newEnd":8,"written":1},"note":"The stretch 3 to 5 reaches the new report, so it is absorbed and the new report becomes 3 to 8."},{"at":{"i":2},"vars":{"newStart":3,"newEnd":8,"written":1},"note":"The stretch 6 to 7 reaches the new report, so it is absorbed and the new report becomes 3 to 8."},{"at":{"i":3},"vars":{"newStart":3,"newEnd":10,"written":1},"note":"The stretch 8 to 10 reaches the new report, so it is absorbed and the new report becomes 3 to 10."},{"at":{"i":4},"vars":{"newStart":3,"newEnd":10,"written":3},"note":"The stretch 12 to 16 starts after the new report ends, so the grown report 3 to 10 is written first and this stretch is copied."}]}
```

<!-- stage: code -->
### Extend The End Or Split Regions

```java
static int[][] merge(int[][] intervals) {
    int[][] sorted = intervals.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> out = new ArrayList<>();
    for (int[] cur : sorted) {
        if (out.isEmpty() || cur[0] > out.get(out.size() - 1)[1]) {
            out.add(new int[] {cur[0], cur[1]});
        } else {
            int[] last = out.get(out.size() - 1);
            last[1] = Math.max(last[1], cur[1]);
        }
    }
    return out.toArray(new int[out.size()][]);
}

static int[][] mergeSorted(int[][] sortedByStart) {
    List<int[]> out = new ArrayList<>();
    for (int[] cur : sortedByStart) {
        if (out.isEmpty() || cur[0] > out.get(out.size() - 1)[1]) {
            out.add(new int[] {cur[0], cur[1]});
        } else {
            int[] last = out.get(out.size() - 1);
            last[1] = Math.max(last[1], cur[1]);
        }
    }
    return out.toArray(new int[out.size()][]);
}

static int[][] insert(int[][] board, int[] add) {
    List<int[]> out = new ArrayList<>();
    int i = 0, n = board.length;
    while (i < n && board[i][1] < add[0]) out.add(board[i++]);
    int lo = add[0], hi = add[1];
    while (i < n && board[i][0] <= hi) {
        lo = Math.min(lo, board[i][0]);
        hi = Math.max(hi, board[i][1]);
        i++;
    }
    out.add(new int[] {lo, hi});
    while (i < n) out.add(board[i++]);
    return out.toArray(new int[out.size()][]);
}
```

The first function costs O(n log n) for the sort and O(n) for the scan. The second drops the sort under its stated promise and costs O(n), and the third is a single O(n) pass, with O(n) space for the output.

<!-- stage: applicability -->
### When Ranges Should Become One

Use this when overlapping or touching ranges must be replaced by their union, or when a new range joins a collection that is already sorted and disjoint. The invariant is that everything finalized lies strictly before the active interval, and only the active interval can still change.

A false friend is the full re-sort after each insertion, which treats a sorted board as unordered and pays for it every time. Another false friend is the scan that keeps the first end instead of the larger end, which loses a long report that swallows the ones after it. A third is merging in place on the caller's rows: the output intervals are mutated when joined, so copy a report before extending it.

In Java, extend with `Math.max(last[1], cur[1])`, not by assigning `cur[1]`, and compare `cur[0] > last[1]` to decide that a gap exists under the closed contract. Build results in a `List<int[]>` and convert with `toArray(new int[out.size()][])`. Copy each row you append, since the same array object may be extended later, and never rely on a sorted input unless the contract states it.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Intervals (LeetCode 56)
<!-- id: iv-merge-intervals -->

**Prerequisites.** The endpoint ordering lesson and the touching-boundary lesson, with closed intervals.

**Problem.** Given closed intervals in any order, return the intervals obtained by merging all those that overlap or touch, sorted by start. Sort by start, keep one active interval, and extend its end with the larger of the two ends.

**Constraints.** 1 <= intervals.length <= 10000 and 0 <= start <= end <= 10000.

**Example 1.** Input `intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]`, output `[[1, 6], [8, 10], [15, 18]]`.

**Example 2.** Input `intervals = [[1, 4], [4, 5]]`, output `[[1, 5]]`.

**Hint.** When does a new interval start a block of its own? What must the active end become when the new one overlaps it?

**Changed decision.** First rung: the sorted scan produces intervals, not a count, and an interval is extended by the larger end.

#### [Vary] Merge Already-Sorted Intervals (Author exercise)
<!-- id: iv-merge-already-sorted -->

**Prerequisites.** The Merge Intervals exercise above.

**Problem.** The intervals arrive sorted by start. Return the merged list without sorting, and state the promise the code depends on. Show what happens to the result when the promise is broken by an input that is not sorted.

**Constraints.** 0 <= intervals.length <= 100000, intervals sorted by start, and 0 <= start <= end <= 1000000000.

**Example 1.** Input `intervals = [[1, 2], [2, 3], [5, 6]]`, output `[[1, 3], [5, 6]]`.

**Example 2.** Input `intervals = []`, output `[]`.

**Hint.** What does the first step of the scan need to handle? Which operation from the previous exercise can be removed?

**Changed decision.** The ordered-input contract replaces the sort, so the cost drops to one pass and correctness depends on the promise.

#### [Boundary] One Interval Covers Many (Author exercise)
<!-- id: iv-one-covers-many -->

**Prerequisites.** The two exercises above.

**Problem.** Let one long interval absorb several later ones, including one that touches its end, and make sure the active end never shrinks when a short interval lies inside it. Return the merged list and explain which expression protects the end.

**Constraints.** 1 <= intervals.length <= 100000 and 0 <= start <= end <= 1000000000.

**Example 1.** Input `intervals = [[1, 10], [2, 3], [4, 5], [10, 12], [13, 14]]`, output `[[1, 12], [13, 14]]`.

**Example 2.** Input `intervals = [[0, 5], [1, 2], [3, 4]]`, output `[[0, 5]]`.

**Hint.** What happens to the end if the code assigns the end of each overlapping interval instead of taking the larger? Which input shows it?

**Changed decision.** A single interval may contain many others, so the active end must be the maximum of all ends seen in the block.

#### [Recognize] Insert Interval (LeetCode 57)
<!-- id: iv-insert-interval -->

**Prerequisites.** All three exercises above.

**Problem.** Given a list of disjoint closed intervals sorted by start, and one new interval, return the sorted disjoint list after inserting it and merging any intervals it overlaps or touches. Copy the intervals before the new one, grow the new one across its overlaps, then copy the rest.

**Constraints.** 0 <= intervals.length <= 10000, the intervals are sorted and disjoint, and 0 <= start <= end <= 100000.

**Example 1.** Input `intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], newInterval = [4, 8]`, output `[[1, 2], [3, 10], [12, 16]]`.

**Example 2.** Input `intervals = [[1, 3], [6, 9]], newInterval = [2, 5]`, output `[[1, 5], [6, 9]]`.

**Hint.** Which intervals end before the new one starts? Which start no later than the new interval's current end?

**Changed decision.** The input is already ordered and disjoint, so a single pass in three regions replaces the sort.
