<!-- lesson-kind: standard -->
<!-- lesson-id: two-list-intersection -->
## Two-List Intersection

<!-- stage: context -->
### Two Shift Rotas

A lighthouse has two keepers who each write a rota of the hours they are awake and on duty, as a list of closed time ranges such as "from hour 5 to hour 10". Each rota is sorted by time, and no two ranges within one rota overlap. The harbour office wants one list: every stretch of time when both keepers are awake, so that a joint safety drill can be planned at a moment when nobody has to be woken.

The two rotas are long, because they cover a whole season, and the office clerk has to produce the joint list every morning from the latest versions. Two keepers might be awake together for a single hour, for a whole shift, or only for the instant one finishes and the other starts. The clerk wants a joint list that is complete and that lists each shared stretch once.

<!-- stage: naive -->
### Compare Every Pair Of Ranges

The direct approach is to take each range from the first rota and compare it with each range from the second rota, keeping every nonempty overlap.

```java
static List<int[]> bothAwakeAllPairs(int[][] first, int[][] second) {
    List<int[]> joint = new ArrayList<>();
    for (int[] a : first) {
        for (int[] b : second) {
            int lo = Math.max(a[0], b[0]);
            int hi = Math.min(a[1], b[1]);
            if (lo <= hi) joint.add(new int[] {lo, hi});
        }
    }
    return joint;
}
```

It is correct because every possible pair is examined, so no shared hour can be missed, and the pairs come out in order because both rotas are sorted.

<!-- stage: bottleneck -->
### Most Pairs Can Never Meet

If the first rota has a ranges and the second has b ranges, the double loop makes a times b comparisons, which is O(a b) work. For two season rotas of a hundred thousand ranges each, that is ten billion comparisons, and almost every one of them compares ranges that are months apart. Both rotas are sorted and disjoint, so a range from early in the season can only meet ranges from early in the season, and the comparison with a range from the end of the season is wasted before it starts.

The wasted work comes from forgetting the order. Once a range from one rota has been compared with a range from the other, and one of them ends earlier, the one that ends earlier cannot meet anything that starts later in the other rota, so it can be dropped for good. That lets a single pass finish in O(a + b) comparisons.

<!-- stage: insight -->
### One Pair Decides Who Leaves

Keep one cursor in each rota. The **current pair** is the range each cursor points at. Their overlap, if any, is the larger of the two starts up to the smaller of the two ends, and it exists exactly when the larger start does not pass the smaller end. After handling the pair, the question is which cursor to move, and the answer is the one with the **smaller end**. A range that ends earlier cannot meet any later range of the other rota, because those later ranges start after the other current range has ended, which is after the earlier end. The range with the larger end may still meet the next range of the other rota, so it stays.

The invariant is that the current pair is the only unresolved cross-rota pair involving both current ranges, and every pair of earlier ranges has already been settled. Moving the cursor with the smaller end preserves it, since the pair that is dropped is fully handled and the new pair is the first one not yet examined. When the ends are equal, either cursor may move, because the one that stays will meet nothing, and it will be skipped by the next comparison.

Whether the overlap exists depends on the **joint slot** rule of the endpoint contract. Under closed ranges, a shared single instant is a nonempty slot, and the test is `lo <= hi`. Under half-open ranges, the same instant is empty, and the test is `lo < hi`. The advance rule stays the same.

<!-- names: current pair, smaller end, joint slot -->

The merge of the two rotas into one list is a different problem. A union keeps every awake hour of either keeper, while the joint list keeps only hours both are awake, so a routine that merges the lists answers the wrong question.

<!-- stage: variables -->
### Two Cursors, One Output List

`i` indexes the first rota and `j` indexes the second rota. For the current pair, `lo` is the larger start and `hi` is the smaller end, and `joint` collects the overlaps in the order they are found. Because both rotas are sorted and disjoint, the overlaps come out sorted and disjoint too. When one fixed range is compared against a sorted list, only the cursor `j` moves, and the loop stops as soon as a list range starts after the fixed range ends.

<!-- stage: trace -->
### Walking Two Rotas Together

The first trace intersects the rota 0 to 2, 5 to 10, 13 to 23, 24 to 25 with the rota 1 to 5, 8 to 12, 15 to 24, 25 to 26 under closed ranges. The cells hold the first rota followed by the second, with `i` pointing into the first and `j` into the second. Look at the first step: the pair 0 to 2 and 1 to 5 shares the stretch 1 to 2, and the first range leaves because its end is smaller.

```trace
{"cells":["0-2","5-10","13-23","24-25","1-5","8-12","15-24","25-26"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":4},"vars":{"lo":1,"hi":2,"found":1},"note":"The pair 0 to 2 and 1 to 5 shares the stretch 1 to 2, and the first range leaves because its end is smaller."},{"at":{"i":1,"j":4},"vars":{"lo":5,"hi":5,"found":2},"note":"The pair 5 to 10 and 1 to 5 shares the stretch 5 to 5, and the second range leaves because its end is smaller."},{"at":{"i":1,"j":5},"vars":{"lo":8,"hi":10,"found":3},"note":"The pair 5 to 10 and 8 to 12 shares the stretch 8 to 10, and the first range leaves because its end is smaller."},{"at":{"i":2,"j":5},"vars":{"lo":13,"hi":12,"found":3},"note":"The pair 13 to 23 and 8 to 12 shares nothing, and the second range leaves because its end is smaller."},{"at":{"i":2,"j":6},"vars":{"lo":15,"hi":23,"found":4},"note":"The pair 13 to 23 and 15 to 24 shares the stretch 15 to 23, and the first range leaves because its end is smaller."},{"at":{"i":3,"j":6},"vars":{"lo":24,"hi":24,"found":5},"note":"The pair 24 to 25 and 15 to 24 shares the stretch 24 to 24, and the second range leaves because its end is smaller."},{"at":{"i":3,"j":7},"vars":{"lo":25,"hi":25,"found":6},"note":"The pair 24 to 25 and 25 to 26 shares the stretch 25 to 25, and the first range leaves because its end is smaller."}]}
```

The second trace uses the same input and watches only the touching moments. Closed ranges report a single instant where one range ends exactly at the start of the other, so the shared hour 5 and the shared hour 24 appear as one-point stretches. The stretch 5 to 5 is found when the pair 5 to 10 meets 1 to 5, and the closed test accepts it because the larger start 5 does not pass the smaller end 5.

```trace
{"cells":["0-2","5-10","13-23","24-25","1-5","8-12","15-24","25-26"],"pointers":["i","j"],"steps":[{"at":{"i":1,"j":4},"vars":{"lo":5,"hi":5,"found":2},"note":"The pair 5 to 10 and 1 to 5 meets at the single value 5, and the closed test accepts it because the larger start does not pass the smaller end."},{"at":{"i":3,"j":6},"vars":{"lo":24,"hi":24,"found":5},"note":"The pair 24 to 25 and 15 to 24 meets at the single value 24, and the closed test accepts it because the larger start does not pass the smaller end."},{"at":{"i":3,"j":7},"vars":{"lo":25,"hi":25,"found":6},"note":"The pair 24 to 25 and 25 to 26 meets at the single value 25, and the closed test accepts it because the larger start does not pass the smaller end."}]}
```

<!-- stage: code -->
### Intersect, Fix One, Walk Two

```java
static int[] intersectPair(int[] a, int[] b, boolean closed) {
    int lo = Math.max(a[0], b[0]);
    int hi = Math.min(a[1], b[1]);
    boolean nonEmpty = closed ? lo <= hi : lo < hi;
    return nonEmpty ? new int[] {lo, hi} : null;
}

static List<int[]> againstList(int[] fixed, int[][] sortedList, boolean closed) {
    List<int[]> joint = new ArrayList<>();
    int j = 0;
    while (j < sortedList.length && sortedList[j][1] < fixed[0]) j++;
    while (j < sortedList.length && sortedList[j][0] <= fixed[1]) {
        int[] piece = intersectPair(fixed, sortedList[j], closed);
        if (piece != null) joint.add(piece);
        j++;
    }
    return joint;
}

static int[][] intersectLists(int[][] first, int[][] second, boolean closed) {
    List<int[]> joint = new ArrayList<>();
    int i = 0, j = 0;
    while (i < first.length && j < second.length) {
        int[] piece = intersectPair(first[i], second[j], closed);
        if (piece != null) joint.add(piece);
        if (first[i][1] < second[j][1]) i++;
        else j++;
    }
    return joint.toArray(new int[joint.size()][]);
}
```

The pair function is O(1). The fixed-range search costs O(b) for a sorted list of b ranges, and the two-list walk advances one cursor per step, so it costs O(a + b) time with O(a + b) space at most for the output.

<!-- stage: applicability -->
### When Sorted Lists Share Time

Use this when two lists are each sorted and disjoint and the answer needs every place where a range from one meets a range from the other. The invariant is that the current pair is the only unresolved pair involving both current ranges, and the range that ends first is finished.

A false friend is merging the two lists and scanning for overlaps, which computes a union and reports overlaps inside one list that do not exist, or hides overlaps between lists. A second false friend is running the pairwise double loop on sorted input, which is correct but ignores the order and costs O(a b). A third is advancing both cursors after every pair, which skips the range with the larger end that still has a partner waiting.

In Java, compute the overlap as `Math.max` of starts and `Math.min` of ends, and choose `<=` or `<` from the stated contract before writing any loop. Compare which end is smaller with `<`, never by subtracting ends, and convert the output list with `toArray(new int[joint.size()][])`. Ties on the ends may advance either cursor, but not both.

<!-- stage: exercises -->
### Exercises

#### [Build] Intersect One Pair (Author exercise)
<!-- id: iv-intersect-one-pair -->

**Prerequisites.** The endpoint ordering and touching-boundary lessons.

**Problem.** Given two closed intervals, return their intersection as `[start, end]`, or an empty array when they share no value. The start is the larger of the two starts and the end is the smaller of the two ends, and the result counts only when the start does not pass the end.

**Constraints.** -1000000000 <= start <= end <= 1000000000 for both intervals.

**Example 1.** Input `a = [1, 5], b = [3, 8]`, output `[3, 5]`.

**Example 2.** Input `a = [1, 2], b = [4, 6]`, output `[]`.

**Hint.** Which expression gives the earliest value that both intervals contain? When is there no such value?

**Changed decision.** First rung: the answer is an interval or nothing, so the code returns a computed pair and tests it against the contract.

#### [Vary] One Interval Against A Sorted List (Author exercise)
<!-- id: iv-one-against-list -->

**Prerequisites.** The Intersect One Pair exercise above.

**Problem.** Given one closed interval and a sorted list of disjoint closed intervals, return the intersection of the interval with every list interval that meets it, in order. Skip the list intervals that end before the fixed interval begins, then stop at the first one that starts after it ends.

**Constraints.** 0 <= list.length <= 100000, the list is sorted and disjoint, and 0 <= start <= end <= 1000000000.

**Example 1.** Input `fixed = [4, 9], list = [[1, 2], [3, 5], [6, 7], [8, 12]]`, output `[[4, 5], [6, 7], [8, 9]]`.

**Example 2.** Input `fixed = [3, 4], list = [[5, 6], [7, 8]]`, output `[]`.

**Hint.** What condition lets a list interval be skipped for good? What condition lets the loop stop early?

**Changed decision.** One side is a single fixed interval, so only one cursor moves, and both ends of the loop come from the fixed interval's endpoints.

#### [Boundary] Touching Intersections (Author exercise)
<!-- id: iv-touching-intersections -->

**Prerequisites.** The two exercises above and the touching-boundary lesson.

**Problem.** Given two sorted lists of disjoint intervals and a flag saying whether the intervals are closed or half-open, return all nonempty intersections. A closed pair that meets at one value gives a one-point interval, and a half-open pair that meets at one value gives nothing.

**Constraints.** 0 <= a.length, b.length <= 100000, each list is sorted and disjoint under its contract, and 0 <= start <= end <= 1000000000.

**Example 1.** Input `a = [[1, 3]], b = [[3, 5]], closed = true`, output `[[3, 3]]`.

**Example 2.** Input `a = [[1, 3]], b = [[3, 5]], closed = false`, output `[]`.

**Hint.** Which comparison decides that a pair has an overlap? Does the rule for advancing a cursor change with the contract?

**Changed decision.** The nonempty test changes between `<=` and `<`, while the rule for advancing the cursor with the smaller end stays the same.

#### [Recognize] Interval List Intersections (LeetCode 986)
<!-- id: iv-interval-list-intersections -->

**Prerequisites.** All three exercises above.

**Problem.** Given two lists of closed intervals, each sorted and pairwise disjoint, return the intersection of the two lists, sorted. Emit the overlap of the current pair when it exists, then advance the interval with the smaller end.

**Constraints.** 0 <= firstList.length, secondList.length <= 1000 and 0 <= start <= end <= 1000000000.

**Example 1.** Input `firstList = [[0, 2], [5, 10], [13, 23], [24, 25]], secondList = [[1, 5], [8, 12], [15, 24], [25, 26]]`, output `[[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]`.

**Example 2.** Input `firstList = [[1, 3], [5, 9]], secondList = []`, output `[]`.

**Hint.** After the overlap of a pair is written, which of the two intervals can still meet a later interval from the other list?

**Changed decision.** Both inputs are ordered, so one cursor moves per step and the total work is the sum of the two lengths, not their product.
