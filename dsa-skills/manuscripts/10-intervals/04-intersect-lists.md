<!-- lesson-kind: standard -->
<!-- lesson-id: intersect-lists -->
## Intersect Two Lists Of Intervals

<!-- stage: context -->
### When Two People Are Both Online

A scheduling service stores the online sessions of two users as lists of closed time windows. Each list is sorted by start, and no two windows in one list overlap. The service must report every window in which both users are online. For user A the sessions are `[1,4]`, `[6,9]`, `[12,15]` and `[18,20]`. For user B they are `[3,7]`, `[8,13]` and `[14,19]`. Reading the lists side by side, the shared windows are `[3,4]`, `[6,7]` and four more.

A developer might first merge the two lists into one and report the merged windows. The merged list shows when at least one user is online, which answers a different question. The service needs the time when both are online. This lesson answers one question: how does a single left-to-right pass pair each window of A with exactly the windows of B that it meets?

<!-- stage: naive -->
### Test Every Pair Of Windows

The direct method compares each window of the first list with each window of the second list. For a pair, it takes the later start and the earlier end. It keeps the pair when the later start does not exceed the earlier end.

```java
static int[][] sharedWindowsAllPairs(int[][] a, int[][] b) {
    List<int[]> out = new ArrayList<>();
    for (int[] x : a) {
        for (int[] y : b) {
            int lo = Math.max(x[0], y[0]);
            int hi = Math.min(x[1], y[1]);
            if (lo <= hi) out.add(new int[] {lo, hi});
        }
    }
    return out.toArray(new int[out.size()][]);
}
```

For the two lists above, the method returns six windows in the order of the first list, and each window is correct. It does not use the order of either list, and it needs no special case for gaps.

<!-- stage: bottleneck -->
### Counting The Pairs

```predict
Two indexes, one in each list, point at one window each, and the method has just recorded their shared window. Which of the two windows can the method discard, and why is it safe?

The one that ends first. Every later window in the other list starts after that other window ends, so it starts after the first window ends too. The discarded window can meet nothing else.
```

The method tests every pair, so it makes `n * m` tests for lists of `n` and `m` windows. That is O(n * m). For two lists of 100,000 windows the method makes 10 billion tests. At most `n + m - 1` pairs actually overlap, because the lists are sorted and disjoint, so almost all tests find nothing.

The waste comes from ignoring the order. A window of A that ends at minute 4 gets tested against a window of B that starts at minute 14. The lists are sorted and disjoint. The windows of B near minute 14 come after every window of B near minute 3, so a pass can move forward through both lists.

<!-- stage: insight -->
### Move The Cursor That Ends First

The shared part of one pair is the **intersection**, the range from the larger start to the smaller end. The rule for ends from the second lesson decides whether it is empty. The scan keeps one **cursor** in each list. A cursor is an index that names the first window of its list that the scan has not yet finished.

#### Compare The Pair Under The Cursors

At each step the scan takes the windows `A[i]` and `B[j]`. It records their intersection when the intersection is non-empty. It then has to move one cursor, and the choice decides correctness.

<!-- names: intersection, cursor, smaller end -->

#### Move The One With The Smaller End

Suppose `A[i]` has the **smaller end** of the two. The window `B[j + 1]` starts after `B[j]` ends, because the list is disjoint, and `B[j]` ends at or after `A[i]`'s end. So `B[j + 1]` and every later window of B start after `A[i]` ends. Earlier windows of B were already tested. Window `A[i]` therefore meets nothing more, and the scan advances `i`. The symmetric argument moves `j` when `B[j]` has the smaller end. Moving the cursor with the smaller start would be wrong, because that window may still meet the next window of the other list.

#### Each Step Ends One Window

Every step moves one cursor forward, so the scan runs at most `n + m - 1` steps. It also records at most one window per step, which bounds the output at `n + m - 1` windows.

<!-- stage: variables -->
### What The Two Cursors Track

The pass keeps four values.

- **i** is the cursor in the first list, and all windows before `i` are finished.
- **j** is the cursor in the second list, and all windows before `j` are finished.
- **lo** is the larger start of `A[i]` and `B[j]`.
- **hi** is the smaller end of `A[i]` and `B[j]`, and `lo <= hi` means the pair shares a window under the closed model.

<!-- stage: trace -->
### Tracing Two Passes Over The Lists

#### Six Shared Windows

Take `A = [1,4], [6,9], [12,15], [18,20]` and `B = [3,7], [8,13], [14,19]`. The cells of the trace are the positions 0 to 3. The pointer `i` is the cursor in `A`, and the pointer `j` is the cursor in `B`.

At the first step the pair `[1,4]` and `[3,7]` shares `[3,4]`, and `A[i]` ends first, so `i` advances. The second step pairs `[6,9]` with `[3,7]` and shares `[6,7]`, and now `B[j]` ends first, so `j` advances. The cursors alternate in this way until `B` is exhausted.

```trace
{"cells":[0,1,2,3],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":0},"vars":{"found":"none"},"note":"Both cursors start at position 0."},{"at":{"i":0,"j":0},"vars":{"lo":3,"hi":4,"found":"[3,4]"},"note":"The pair [1,4] and [3,7] shares [3,4], which is recorded. The window of A ends first, so cursor i advances."},{"at":{"i":1,"j":0},"vars":{"lo":6,"hi":7,"found":"[3,4] [6,7]"},"note":"The pair [6,9] and [3,7] shares [6,7], which is recorded. The window of B ends first, so cursor j advances."},{"at":{"i":1,"j":1},"vars":{"lo":8,"hi":9,"found":"[3,4] [6,7] [8,9]"},"note":"The pair [6,9] and [8,13] shares [8,9], which is recorded. The window of A ends first, so cursor i advances."},{"at":{"i":2,"j":1},"vars":{"lo":12,"hi":13,"found":"[3,4] [6,7] [8,9] [12,13]"},"note":"The pair [12,15] and [8,13] shares [12,13], which is recorded. The window of B ends first, so cursor j advances."},{"at":{"i":2,"j":2},"vars":{"lo":14,"hi":15,"found":"[3,4] [6,7] [8,9] [12,13] [14,15]"},"note":"The pair [12,15] and [14,19] shares [14,15], which is recorded. The window of A ends first, so cursor i advances."},{"at":{"i":3,"j":2},"vars":{"lo":18,"hi":19,"found":"[3,4] [6,7] [8,9] [12,13] [14,15] [18,19]"},"note":"The pair [18,20] and [14,19] shares [18,19], which is recorded. The window of B ends first, so cursor j advances."},{"at":{"i":3,"j":3},"vars":{"found":"[3,4] [6,7] [8,9] [12,13] [14,15] [18,19]"},"note":"A cursor has left its list, so the pass ends."}]}
```

#### Windows That Only Touch

Now take `A = [1,3], [5,7]` and `B = [3,5], [7,9]` under the closed model. Every shared window is a single coordinate, because each pair meets only at an end. The same rule applies: record the intersection, then advance the cursor with the smaller end.

```trace
{"cells":[0,1],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":0},"vars":{"found":"none"},"note":"Both cursors start at position 0."},{"at":{"i":0,"j":0},"vars":{"lo":3,"hi":3,"found":"[3,3]"},"note":"The pair [1,3] and [3,5] shares [3,3], which is recorded. The window of A ends first, so cursor i advances."},{"at":{"i":1,"j":0},"vars":{"lo":5,"hi":5,"found":"[3,3] [5,5]"},"note":"The pair [5,7] and [3,5] shares [5,5], which is recorded. The window of B ends first, so cursor j advances."},{"at":{"i":1,"j":1},"vars":{"lo":7,"hi":7,"found":"[3,3] [5,5] [7,7]"},"note":"The pair [5,7] and [7,9] shares [7,7], which is recorded. The window of A ends first, so cursor i advances."},{"at":{"i":2,"j":1},"vars":{"found":"[3,3] [5,5] [7,7]"},"note":"A cursor has left its list, so the pass ends."}]}
```

<!-- stage: code -->
### Writing The Pass In Java

#### One Pair And Two Lists

The pair method returns the intersection, or `null` when there is none. The `null` result keeps the caller's loop short and shows that "no shared window" is a legal answer. In the list method, the loop runs while both cursors are inside their lists. When the ends tie, advancing either cursor is correct.

```java
static int[] intersectPair(int[] x, int[] y) {
    int lo = Math.max(x[0], y[0]);
    int hi = Math.min(x[1], y[1]);
    return lo <= hi ? new int[] {lo, hi} : null;
}

static int[][] intersectLists(int[][] a, int[][] b) {
    List<int[]> out = new ArrayList<>();
    int i = 0, j = 0;
    while (i < a.length && j < b.length) {
        int[] hit = intersectPair(a[i], b[j]);
        if (hit != null) out.add(hit);
        if (a[i][1] < b[j][1]) i++;
        else j++;
    }
    return out.toArray(new int[out.size()][]);
}
```

#### Cost Of The Pass

The pass costs O(n + m) time, because each iteration advances a cursor. It uses O(n + m) space for the output in the worst case, and the pair method allocates only when a pair intersects.

<!-- stage: applicability -->
### When To Use Two Cursors

#### State The Contract Of Both Lists

The invariant of the pass is that no finished window of either list can meet an unfinished window of the other. That statement holds only when each list is sorted by start and has no overlaps. Check the contract before you write the pass. When a list is not disjoint, merge it first with the method of the previous lesson. When it is not sorted, sort it first.

#### Merging Is A False Friend

Merging the two lists, as the opening developer first tried, is a false friend. A merge computes the union, the time when at least one user is online. The intersection needs the larger start and the smaller end, and it can only shrink windows. The two operations also differ in cost. The union needs a sort or a merge, and the intersection is a single pass with no sort.

#### Cursor Choice And The Model For Ends

Advance the cursor with the smaller end, never the smaller start. Under the half-open model the same rule applies, and only the emptiness test changes from `lo <= hi` to `lo < hi`. When a problem gives one interval and one list, the same idea applies with one cursor. It skips windows that end before the interval starts and stops at the first window that starts after the interval ends.

<!-- stage: exercises -->
### Exercises

#### [Build] Intersect One Pair (Author exercise)
<!-- id: iv-intersect-pair -->

**Prerequisites.** The closed overlap test from the second lesson.

**Problem.** Given two closed intervals `x` and `y`, return their intersection, the closed interval that holds exactly the integers lying in both. When no integer lies in both, return an empty array.

**Constraints.** The limits are:
- **Values** are `int` values with `start <= end` in each interval.
- **Return** is an `int[]` of length 2, or an empty `int[]` when there is no intersection.
- **Touching** intervals that share one end coordinate intersect in a single coordinate.
- **Mutation** is not allowed; neither input changes.

**Example 1.** Input `[2,6]` and `[4,9]`, output `[4,6]`.

**Example 2.** Input `[1,3]` and `[4,5]`, output `[]`.

**Hint.** Compute the larger start and the smaller end first. When is the range between them empty?

**Changed decision.** Basic case: the intersection takes the larger start and the smaller end, and the test decides whether it exists.

#### [Vary] One Interval Against A Sorted List (Author exercise)
<!-- id: iv-interval-vs-list -->

**Prerequisites.** The exercise above.

**Problem.** Given one closed interval `q` and a list of closed intervals, return the intersection of `q` with each list interval that meets it, in list order. The list is sorted by start and has no overlaps. Skip every list interval that ends before `q` starts, and stop at the first list interval that starts after `q` ends.

**Constraints.** The limits are:
- **Length** is `0 <= list.length <= 10^5`.
- **Values** are `int` values with `start <= end` in every interval.
- **Order** of the list is by start, and its intervals do not overlap.
- **Return** is an `int[][]` in list order, empty when nothing meets `q`.

**Example 1.** Input `q = [4,12]` and list `[[1,3],[5,6],[8,10],[11,15],[20,22]]`, output `[[5,6],[8,10],[11,12]]`.

**Example 2.** Input `q = [3,3]` and list `[[1,2],[3,5]]`, output `[[3,3]]`.

**Hint.** The list is in order, so the windows that meet `q` form one unbroken block. Where does it begin and end?

**Changed decision.** One interval is fixed, so only one cursor moves and the stop rule replaces the second list.

#### [Boundary] Touching Intersections (Author exercise)
<!-- id: iv-touching-intersections -->

**Prerequisites.** The two exercises above and the half-open model from the second lesson.

**Problem.** Given two lists of intervals and a flag `closed`, return how many non-empty intersections the two lists produce. Inside each list the intervals are sorted by start and do not overlap. When `closed` is true each interval is `[start, end]`. When `closed` is false each interval is `[start, end)`, and an interval with `start == end` is empty and meets nothing.

**Constraints.** The limits are:
- **Length** of each list is `0 <= length <= 10^5`.
- **Values** are `int` values with `start <= end` in every interval.
- **Disjoint** means no overlap under the chosen model within one list.
- **Return** is a single `int`.

**Example 1.** Input `A = [[1,3],[5,7]]` and `B = [[3,5],[7,9]]`, output 3 when `closed` is true and 0 when it is false.

**Example 2.** Input `A = [[1,5]]` and `B = [[2,2]]`, output 1 when `closed` is true and 0 when it is false.

**Hint.** Which test decides whether a pair counts? Does the choice of cursor change between the two models?

**Changed decision.** The emptiness test flips from `lo <= hi` to `lo < hi`, and the cursor rule stays the same.

#### [Recognize] Interval List Intersections (LeetCode 986)
<!-- id: iv-interval-list-intersections -->

**Prerequisites.** All three exercises above.

**Problem.** Given two lists of closed intervals, return every non-empty intersection of an interval from the first list with an interval from the second, ordered by start. Each list is sorted by start and has no overlaps inside it. The method must run in a single pass.

**Constraints.** The limits are:
- **Length** of each list is `0 <= length <= 10^5`.
- **Values** are `int` values with `start <= end` in every interval.
- **Order** within each list is by start, and its intervals do not overlap.
- **Return** is an `int[][]`, empty when no interval pair meets.

**Example 1.** Input `A = [[0,3],[7,9]]` and `B = [[2,8]]`, output `[[2,3],[7,8]]`.

**Example 2.** Input `A = [[4,4],[6,8]]` and `B = [[1,4],[8,9]]`, output `[[4,4],[8,8]]`.

**Hint.** After you record a pair, which of the two intervals can no longer meet any unfinished interval?

**Changed decision.** The cursor with the smaller end advances, because the other list is disjoint.
