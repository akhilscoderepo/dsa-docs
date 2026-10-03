<!-- lesson-kind: standard -->
<!-- lesson-id: touching-boundary-semantics -->
## Touching-Boundary Semantics

<!-- stage: context -->
### A Campsite Calendar

A campsite has a single pitch near the lake, and the warden keeps a calendar of requests. One camper writes "from day 1 to day 3", another writes "from day 3 to day 5". The warden has to decide whether the two requests clash. The answer depends on what the words mean. If the first camper keeps the pitch through the whole of day 3, as a pass stamped with dates would, then the second cannot arrive that day. If the first camper leaves on the morning of day 3, as a booking with a checkout would, the second can pitch a tent that same afternoon.

The warden has run into this at every campsite she has worked at. A calendar of ranges does not say by itself whether its end days are included, and two calendars that look identical on paper can produce different answers for every pair of requests that meet at a single day.

<!-- stage: naive -->
### Mark Every Day On A Grid

The direct approach is to mark each day of each request on a grid, one cell per day, and to report a clash when a day gets marked twice.

```java
static boolean clashByMarking(int[] first, int[] second, boolean endIncluded) {
    boolean[] marked = new boolean[1000];
    for (int day = first[0]; day < first[1] + (endIncluded ? 1 : 0); day++) {
        marked[day] = true;
    }
    for (int day = second[0]; day < second[1] + (endIncluded ? 1 : 0); day++) {
        if (marked[day]) return true;
    }
    return false;
}
```

It answers correctly for both meanings, because it decides which days belong to a request before it compares anything.

<!-- stage: bottleneck -->
### Cost Grows With Range Length

Marking costs O(L) for ranges of length L, and the grid needs space for every possible day, so ranges counted in seconds or millions of days make the method unusable. A range from 1 to 1000000000 needs a billion cells, and every pair of requests repeats that work. What the grid computes is a single yes or no that depends only on four numbers, the two starts and the two ends.

The comparison can be done on the endpoints alone, in O(1), if the meaning of the endpoints is fixed first. Two ranges clash when the later start comes before the earlier end, and the only question is what happens when the two are equal. That one equality is the entire difference between the two meanings, so the code has to settle it by the contract and not by habit.

<!-- stage: insight -->
### Fix The Meaning, Then Compare Four Numbers

A **closed interval** `[a, b]` contains both endpoints and every value between them. A **half-open interval** `[a, b)` contains its start and every value up to but not including its end. The meaning is chosen by the problem and written next to the data. Two intervals overlap when some value belongs to both, and for ranges on a line, this reduces to comparing the larger start with the smaller end. Let `s` be the larger of the two starts and `e` the smaller of the two ends. The intervals share a value exactly when there is a value at least `s` and still inside both, which is the **overlap predicate**.

For closed intervals the predicate is `s <= e`: if the larger start equals the smaller end, that single value is in both. For half-open intervals it is `s < e`: when the larger start equals the smaller end, that value is excluded from the interval that ends there, so nothing is shared. The two predicates differ in exactly one symbol, and applying the wrong one gives answers that look plausible and fail only at touching endpoints. The invariant for every comparison is that the code uses the predicate matching the declared contract, and nothing else.

<!-- names: closed interval, half-open interval, overlap predicate -->

Degenerate cases follow from the same definitions. A closed interval with equal endpoints, `[x, x]`, is a single point, and it overlaps any closed interval that contains `x`. A half-open interval `[x, x)` is empty, so it overlaps nothing, and the predicate `s < e` already gives that answer without a special branch. Merging intervals uses the same predicate to decide whether two ranges join: under the closed contract, touching ranges merge, and under the half-open contract, ranges that merely touch remain separate.

<!-- stage: variables -->
### Four Endpoints And One Symbol

`aStart`, `aEnd`, `bStart` and `bEnd` are the four endpoints, with the meaning of the ends fixed by the contract. `s` is `Math.max(aStart, bStart)` and `e` is `Math.min(aEnd, bEnd)`. The verdict is `s <= e` for closed ranges and `s < e` for half-open ranges. A merge scan keeps `reach`, the end of the block being grown, and compares each new start with it by the same predicate: a start that is at most `reach` joins a closed block, and a start that is strictly below `reach` joins a half-open block.

<!-- stage: trace -->
### The Same Pairs Under Two Meanings

The first trace evaluates four pairs of ranges under both meanings, and each step shows the larger start, the smaller end and both verdicts. Look at the first pair, 1 to 3 against 3 to 5: the larger start 3 equals the smaller end 3, so the closed verdict is yes and the half-open verdict is no.

```trace
{"cells":["1-3 vs 3-5","1-3 vs 4-5","1-4 vs 3-6","3-3 vs 1-5"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"largerStart":3,"smallerEnd":3,"closed":"yes","halfOpen":"no"},"note":"The pair 1 to 3 and 3 to 5 has larger start 3 and smaller end 3, so closed says yes and half-open says no."},{"at":{"i":1},"vars":{"largerStart":4,"smallerEnd":3,"closed":"no","halfOpen":"no"},"note":"The pair 1 to 3 and 4 to 5 has larger start 4 and smaller end 3, so closed says no and half-open says no."},{"at":{"i":2},"vars":{"largerStart":3,"smallerEnd":4,"closed":"yes","halfOpen":"yes"},"note":"The pair 1 to 4 and 3 to 6 has larger start 3 and smaller end 4, so closed says yes and half-open says yes."},{"at":{"i":3},"vars":{"largerStart":3,"smallerEnd":3,"closed":"yes","halfOpen":"no"},"note":"The pair 3 to 3 and 1 to 5 has larger start 3 and smaller end 3, so closed says yes and half-open says no."}]}
```

The second trace merges the ranges 1 to 3, 3 to 5 and 7 to 8 under the half-open meaning, in order of start. Notice the second step: the start 3 equals the reach 3, which would join the block under the closed meaning, but the half-open predicate needs a start strictly below the reach, so the block stays separate.

```trace
{"cells":["1-3","3-5","7-8"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"reach":3,"blocks":1},"note":"The first range 1 to 3 opens a block, so the reach is 3 and there is 1 block."},{"at":{"i":1},"vars":{"reach":5,"blocks":2},"note":"The start 3 equals the reach 3. Half-open needs a start strictly below the reach, so a new block opens and the count is 2."},{"at":{"i":2},"vars":{"reach":8,"blocks":3},"note":"The start 7 is past the reach 5, so another block opens and the count is 3."}]}
```

<!-- stage: code -->
### One Scan, One Symbol Apart

```java
static boolean overlapsClosed(int[] a, int[] b) {
    return Math.max(a[0], b[0]) <= Math.min(a[1], b[1]);
}

static boolean overlapsHalfOpen(int[] a, int[] b) {
    return Math.max(a[0], b[0]) < Math.min(a[1], b[1]);
}

static int[][] mergeUnder(int[][] intervals, boolean closed) {
    int[][] sorted = intervals.clone();
    Arrays.sort(sorted, (x, y) -> Integer.compare(x[0], y[0]));
    List<int[]> out = new ArrayList<>();
    for (int[] cur : sorted) {
        if (!out.isEmpty()) {
            int[] last = out.get(out.size() - 1);
            boolean joins = closed ? cur[0] <= last[1] : cur[0] < last[1];
            if (joins) {
                last[1] = Math.max(last[1], cur[1]);
                continue;
            }
        }
        out.add(new int[] {cur[0], cur[1]});
    }
    return out.toArray(new int[out.size()][]);
}
```

Each predicate is O(1), and the merge costs O(n log n) for the sort plus one pass. The scan is the same in both modes except for one comparison symbol, and the result list is converted to an array at the end with `toArray(new int[out.size()][])`.

<!-- stage: applicability -->
### When The Ends Might Count

Reach for the endpoint predicate whenever two ranges meet at a boundary value, or whenever the data comes from a source that does not say how ends are counted. The invariant is that every comparison uses the one predicate that corresponds to the declared meaning, so a boundary case is decided by the contract and never by memory.

A false friend is the pair of symbols `<=` and `<` memorized as the rule for overlap: it is correct under one meaning and wrong under the other, and nothing in the code shows which. Another false friend is converting a half-open range to a closed one by subtracting one from the end without checking the empty case, which turns an empty range into a range with one value. A third is treating a zero-length range as invalid when the contract allows it.

In Java, name the contract in the method, as in `overlapsClosed` and `overlapsHalfOpen`, and use `Math.max` and `Math.min` so the predicate reads as a comparison of two numbers. Compare with `<=` or `<`, never with subtraction, since a difference of `int` endpoints can overflow. Write the test cases at touching endpoints first, because those are the only inputs on which the two predicates disagree.

<!-- stage: exercises -->
### Exercises

#### [Build] Closed Interval Overlap (Author exercise)
<!-- id: iv-closed-overlap -->

**Prerequisites.** The endpoint ordering lesson, and comparisons of `int` values.

**Problem.** Given two closed intervals, each with both endpoints included, return whether they share at least one value. Decide whether `[1, 3]` and `[3, 5]` overlap, and compute the answer from the larger start and the smaller end.

**Constraints.** Each interval is `[start, end]` with -1000000000 <= start <= end <= 1000000000.

**Example 1.** Input `a = [1, 3], b = [3, 5]`, output true.

**Example 2.** Input `a = [1, 2], b = [4, 5]`, output false.

**Hint.** If the larger start equals the smaller end, is that value in both intervals? Which comparison symbol follows?

**Changed decision.** First rung: the meaning of the endpoints is fixed as closed, so a shared endpoint counts as a shared value.

#### [Vary] Half-Open Reservations (Author exercise)
<!-- id: iv-half-open-reservations -->

**Prerequisites.** The Closed Interval Overlap exercise above.

**Problem.** Reservations are half-open: a reservation `[start, end)` holds a resource from `start` up to but not including `end`. Given two reservations, return whether they need the same resource at the same moment. Decide whether `[1, 3)` and `[3, 5)` clash.

**Constraints.** Each reservation is `[start, end)` with -1000000000 <= start <= end <= 1000000000, and an empty reservation with equal ends is allowed.

**Example 1.** Input `a = [1, 3), b = [3, 5)`, output false.

**Example 2.** Input `a = [1, 4), b = [3, 6)`, output true.

**Hint.** If the larger start equals the smaller end, does the interval that ends there contain that value?

**Changed decision.** The end is now excluded, so the predicate loses its equality and requires a strict comparison.

#### [Boundary] Zero-Length Range (Author exercise)
<!-- id: iv-zero-length-range -->

**Prerequisites.** The two exercises above.

**Problem.** Handle intervals whose start equals their end. State whether a closed `[x, x]` is a single point and whether a half-open `[x, x)` is empty, and show that the same predicates from the earlier exercises give the right answers without a special case. Test a zero-length range against a longer one and against another zero-length range.

**Constraints.** -1000000000 <= start <= end <= 1000000000, with start equal to end allowed.

**Example 1.** Input closed `a = [3, 3], b = [1, 5]`, output true.

**Example 2.** Input half-open `a = [3, 3), b = [1, 5)`, output false.

**Hint.** Which values does `[3, 3)` contain? What does the half-open predicate compute for `s = 3` and `e = 3`?

**Changed decision.** The shortest legal range is a single point under one contract and empty under the other, and the predicate must handle both.

#### [Recognize] Merge Under A Supplied Contract (Author exercise)
<!-- id: iv-merge-under-contract -->

**Prerequisites.** All three exercises above, and the merge scan from the previous lesson.

**Problem.** Write one merge function that takes the intervals and a flag saying whether they are closed or half-open, and merges only intervals that share a value. Under the closed contract touching intervals merge, and under the half-open contract they stay separate. The two modes may differ only in the comparison used to decide whether the next interval joins the current block.

**Constraints.** 1 <= intervals.length <= 10000, 0 <= start <= end <= 10000, and every half-open interval has start < end.

**Example 1.** Input closed `intervals = [[1, 3], [3, 5], [7, 8]]`, output `[[1, 5], [7, 8]]`.

**Example 2.** Input half-open `intervals = [[1, 3], [3, 5], [7, 8]]`, output `[[1, 3], [3, 5], [7, 8]]`.

**Hint.** What is the single comparison that changes? Which sort order does the scan still need?

**Changed decision.** The overlap predicate becomes a parameter, and nothing else in the scan changes.
