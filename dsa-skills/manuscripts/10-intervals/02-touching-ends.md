<!-- lesson-kind: standard -->
<!-- lesson-id: touching-ends -->
## Decide When Touching Intervals Overlap

<!-- stage: context -->
### One Pair Of Bookings, Two Answers

A hotel system stores guest A in room 12 from day 1 to day 3. It stores guest B in the same room from day 3 to day 5. The front desk says the booking is fine. Guest A checks out on the morning of day 3, and guest B checks in that afternoon. The booking code reports a double booking and rejects guest B. Both sides read the same numbers, `[1,3]` and `[3,5]`, and they disagree about one shared value.

The data does not decide the answer. A rule about the ends decides it, and the code and the front desk follow different rules. The lesson works toward one answer. How does a rule about the ends turn into the exact comparison that tests two intervals for overlap?

<!-- stage: naive -->
### Use The Same Comparison Every Time

The usual habit is to remember one test and apply it everywhere. Two intervals overlap when each one starts no later than the other one ends, so the test uses `<=` on both sides.

```java
static boolean overlaps(int[] a, int[] b) {
    return a[0] <= b[1] && b[0] <= a[1];
}
```

For the hotel, `overlaps({1,3}, {3,5})` returns true, so the system rejects guest B. For two meetings `[9,10]` and `[10,11]` it also returns true, although the meeting room is free at 10:00 for the second meeting. The test answers correctly only when the rule says that touching ends count as shared.

<!-- stage: bottleneck -->
### Counting The Pairs That Flip

```predict
Take the ten intervals `[0,1]`, `[1,2]`, `[2,3]` up to `[9,10]`, each one starting where the previous one ends. How many neighbouring pairs does the `<=` test report as overlapping, and how many does a test that treats the end as excluded report?

The `<=` test reports 9 overlapping pairs and the strict test reports 0. Every touching neighbour changes its answer when the rule about ends changes, so the cost of a wrong rule grows with n.
```

A chain of `n` intervals that each start at the previous end has `n - 1` touching neighbours. All `n - 1` pairs change from overlap to no overlap when the rule changes. A wrong rule therefore changes O(n) results in one scan. A merge scan collapses the whole chain into one interval under one rule and leaves `n` separate intervals under the other. The output size itself changes from 1 to `n`.

The fault is hard to find because the method never crashes. It runs fast on every input and gives a wrong answer only where two ends meet. The test needs to come from the rule that the problem states, not from habit.

<!-- stage: insight -->
### Derive The Test From The End Rule

A rule for ends says which coordinates belong to an interval. Write the interval as a set of coordinates first, and derive the comparison from the set.

#### Closed Intervals Include Both Ends

A **closed** interval `[a, b]` holds every coordinate `x` with `a <= x <= b`, so it includes both ends. The interval `[x, x]` holds exactly one coordinate. This is the model of the opening `<=` test.

<!-- names: closed, half-open, point -->

#### Half-Open Intervals Exclude The End

A **half-open** interval `[a, b)` holds every coordinate `x` with `a <= x < b`, so it includes its start and excludes its end. The interval `[x, x)` holds no coordinate. Java uses this model in `String.substring(begin, end)`, `List.subList(from, to)` and `Arrays.copyOfRange(a, from, to)`. The second argument is excluded, and the length is `end - begin`.

#### One Test For Both Models

Two intervals share a **point** when some coordinate lies in both. Let `lo` be the larger of the two starts and `hi` be the smaller of the two ends. The shared coordinates form the range from `lo` to `hi`. For closed intervals that range is non-empty when `lo <= hi`. For half-open intervals it is non-empty when `lo < hi`. The two models differ in one character of the comparison. Whether the end is included decides that character.

<!-- stage: variables -->
### What The Overlap Test Reads

The test needs four pieces of state.

- **lo** is the larger start of the two intervals, `Math.max(a[0], b[0])`.
- **hi** is the smaller end of the two intervals, `Math.min(a[1], b[1])`.
- **model** is the stated rule for ends, either closed or half-open, and it picks `<=` or `<`.
- **shared range** is the set of coordinates from `lo` to `hi` that the model keeps.

<!-- stage: trace -->
### Walking The Coordinates Of Two Models

#### Both Ends Included

Take `A = [1,3]` and `B = [3,5]` as closed intervals. The trace uses the coordinates 0 to 6 as its cells, and the pointer `x` marks the coordinate under test. At each coordinate the trace records whether `A` holds it and whether `B` holds it.

Coordinates 1 and 2 belong to `A` only, and coordinates 4 and 5 belong to `B` only. Coordinate 3 belongs to both, so the intervals share one coordinate. The comparison agrees: `lo = 3`, `hi = 3`, and `3 <= 3` holds.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["x"],"steps":[{"at":{"x":0},"vars":{"in A":"false","in B":"false"},"note":"Coordinate 0 is in neither interval."},{"at":{"x":1},"vars":{"in A":"true","in B":"false"},"note":"Coordinate 1 is in A only."},{"at":{"x":2},"vars":{"in A":"true","in B":"false"},"note":"Coordinate 2 is in A only."},{"at":{"x":3},"vars":{"in A":"true","in B":"true"},"note":"Coordinate 3 is in both intervals."},{"at":{"x":4},"vars":{"in A":"false","in B":"true"},"note":"Coordinate 4 is in B only."},{"at":{"x":5},"vars":{"in A":"false","in B":"true"},"note":"Coordinate 5 is in B only."},{"at":{"x":6},"vars":{"in A":"false","in B":"false"},"note":"Coordinate 6 is in neither interval."},{"at":{"x":7},"vars":{"lo":3,"hi":3,"overlap":"true"},"note":"The walk ends. With lo = 3 and hi = 3, the test gives true, which matches the shared coordinates."}]}
```

#### End Excluded

Now take the same numbers as half-open intervals, `A = [1,3)` and `B = [3,5)`. Coordinate 3 no longer belongs to `A`, so no coordinate lies in both. The comparison agrees again: `lo = 3`, `hi = 3`, and `3 < 3` fails.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["x"],"steps":[{"at":{"x":0},"vars":{"in A":"false","in B":"false"},"note":"Coordinate 0 is in neither interval."},{"at":{"x":1},"vars":{"in A":"true","in B":"false"},"note":"Coordinate 1 is in A only."},{"at":{"x":2},"vars":{"in A":"true","in B":"false"},"note":"Coordinate 2 is in A only."},{"at":{"x":3},"vars":{"in A":"false","in B":"true"},"note":"Coordinate 3 is in B only."},{"at":{"x":4},"vars":{"in A":"false","in B":"true"},"note":"Coordinate 4 is in B only."},{"at":{"x":5},"vars":{"in A":"false","in B":"false"},"note":"Coordinate 5 is in neither interval."},{"at":{"x":6},"vars":{"in A":"false","in B":"false"},"note":"Coordinate 6 is in neither interval."},{"at":{"x":7},"vars":{"lo":3,"hi":3,"overlap":"false"},"note":"The walk ends. With lo = 3 and hi = 3, the test gives false, which matches the shared coordinates."}]}
```

<!-- stage: code -->
### Writing The Test For Each Model

#### Two Overlap Methods

Both methods read `lo` and `hi` and differ only in the comparison.

```java
static boolean overlapsClosed(int[] a, int[] b) {
    int lo = Math.max(a[0], b[0]);
    int hi = Math.min(a[1], b[1]);
    return lo <= hi;
}

static boolean overlapsHalfOpen(int[] a, int[] b) {
    int lo = Math.max(a[0], b[0]);
    int hi = Math.min(a[1], b[1]);
    return lo < hi;
}
```

#### Counting Coordinates Of One Interval

The number of coordinates also depends on the model. The cast to `long` matters, because `end - start` for far-apart `int` values does not fit in an `int`.

```java
static long countClosed(int[] iv) {
    return (long) iv[1] - iv[0] + 1;
}

static long countHalfOpen(int[] iv) {
    return (long) iv[1] - iv[0];
}
```

All four methods run in O(1) time and O(1) space. A scan over `n` intervals takes the model as a boolean and calls one of the two overlap methods. The scan itself stays unchanged.

<!-- stage: applicability -->
### Reading The Rule Before Writing The Test

#### Find The Model In The Statement

The invariant of this lesson is that the overlap test follows the stated model for ends. Look for words such as "inclusive", "exclusive", "from day to day" and "up to but not including". Resource problems such as room bookings often use half-open time slots. A slot that ends at 3 frees the resource for a slot that starts at 3. A problem that asks for "any shared coordinate" on whole numbers is usually closed.

#### Memorized Comparisons Mislead

Remembering "use `<=`" or "use `<`" without the model is a false friend. Each rule is right for one model and wrong for the other, and neither one is wrong in itself. When a problem does not state the model, write the assumption in a comment. Then check a sample with touching ends, because that sample reveals the model.

#### Zero-Length Intervals

Keep the zero-length case in mind. `[x, x]` is a closed interval with one coordinate, so it overlaps any closed interval that contains `x`. `[x, x)` is empty under the half-open model, so it overlaps nothing, and a scan may skip it. A test that never asks whether an interval is empty can report an overlap with a range that holds no coordinate.

<!-- stage: exercises -->
### Exercises

#### [Build] Closed Interval Overlap (Author exercise)
<!-- id: iv-closed-overlap -->

**Prerequisites.** The closed model and the `lo`, `hi` test in this lesson.

**Problem.** A closed interval `[start, end]` contains every integer `x` with `start <= x <= end`. Given two closed intervals `a` and `b`, return true if some integer lies in both, and false otherwise.

**Constraints.** The limits are:
- **Values** are `int` values with `start <= end` in each interval.
- **Return** is a `boolean`.
- **Mutation** is not allowed; neither interval changes.
- **Ties** include equal starts, equal ends and one shared end coordinate.

**Example 1.** Input `a = [1,3]` and `b = [3,5]`, output true, because 3 lies in both.

**Example 2.** Input `a = [1,2]` and `b = [4,5]`, output false.

**Hint.** Compute the larger start and the smaller end. When is the range between them non-empty if both ends are included?

**Changed decision.** Basic case: the test is `lo <= hi`, and the touching pair counts as overlap.

#### [Vary] Half-Open Reservations (Author exercise)
<!-- id: iv-half-open-reservations -->

**Prerequisites.** The exercise above.

**Problem.** A reservation `[start, end)` uses a single resource at every integer time `t` with `start <= t < end`. Given two reservations, return true if they use the resource at a common time, so the two conflict.

**Constraints.** The limits are:
- **Values** are `int` values with `start < end` in each reservation.
- **Return** is a `boolean`.
- **Mutation** is not allowed; neither reservation changes.
- **Ties** include equal starts and an end equal to the other start.

**Example 1.** Input `[1,3)` and `[3,5)`, output false, because the first reservation ends before time 3.

**Example 2.** Input `[1,4)` and `[3,5)`, output true, because time 3 belongs to both.

**Hint.** Reuse the two quantities from the previous exercise. Which comparison changes when the end is excluded?

**Changed decision.** The model excludes the end, so `<=` becomes `<`.

#### [Boundary] Zero-Length Range (Author exercise)
<!-- id: iv-zero-length-range -->

**Prerequisites.** The two exercises above.

**Problem.** Given an interval `[start, end]` and a flag `closed`, return how many integers the interval contains. When `closed` is true the interval contains every integer `x` with `start <= x <= end`. When `closed` is false it contains every integer `x` with `start <= x < end`.

**Constraints.** The limits are:
- **Values** are any `int` values with `start <= end`, including both extremes of `int`.
- **Return** is a `long`, because the count can exceed the `int` range.
- **Equal ends** `start == end` are legal and must give the right count for both models.
- **Mutation** is not allowed; the input does not change.

**Example 1.** Input `[4,4]` with `closed` true, output 1; with `closed` false, output 0.

**Example 2.** Input `[-2147483648, 2147483647]` with `closed` true, output 4294967296.

**Hint.** Write the count as `end - start` plus a correction that depends on the flag. Which type holds the difference of two extreme values?

**Changed decision.** The empty half-open interval is legal, and the arithmetic must widen to `long`.

#### [Recognize] Merge Under A Supplied Contract (Author exercise)
<!-- id: iv-group-starts-contract -->

**Prerequisites.** All three exercises above, and the group scan from the previous lesson.

**Problem.** Intervals are given already ordered by start, then by end. Two intervals belong to the same group when a chain of overlapping intervals links them. A flag `closed` selects the model: when true each interval is `[start, end]`, and when false each interval is `[start, end)`. Merge each group into one interval and return only the start of each merged interval, in input order. Write one scan and change only the overlap comparison between the two models.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start < end` in each interval.
- **Order** is non-decreasing by start; the code must not sort.
- **Return** is an `int[]`, empty for an empty input.

**Example 1.** Input `[[1,3],[3,5],[6,8]]` with `closed` true, output `[1,6]`; with `closed` false, output `[1,3,6]`.

**Example 2.** Input `[[1,4],[2,3],[4,6]]` with `closed` true, output `[1]`; with `closed` false, output `[1,4]`.

**Hint.** Keep the largest end of the current group. The new start compares with that end through the model's comparison.

**Changed decision.** One scan serves both models, and only `<=` against `<` changes.
