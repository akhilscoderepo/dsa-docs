<!-- lesson-kind: standard -->
<!-- lesson-id: query-planning -->
## Query Planning

<!-- stage: context -->
### Why Every Query Rescans The Array

A log analysis service loads one million request records into an array, where each entry is an error code. The dashboard then asks questions such as how often code 503 appears between request 40,000 and request 90,000. The first version answers each question with a loop over that range. It passes every test on a small sample. On launch day, the dashboard sends 100,000 questions against the same array, and each one scans up to a million entries. The service burns minutes of processor time on data that never changed between questions.

Nothing is wrong with a single answer, because each loop is correct. The waste comes from repeating the same reading of the array for every question. This lesson asks what the constructor can store once so that each later question needs only a few steps. It also asks how the promises in the API change that choice, such as whether all questions arrive at the start or one at a time.

<!-- stage: naive -->
### Scanning The Range For Each Question

The direct design keeps the array and answers each question with a loop over the requested range. The loop compares every entry with the wanted value and counts the matches.

```java
final class ScanFrequency {
    private final int[] arr;

    ScanFrequency(int[] arr) { this.arr = arr; }

    int query(int left, int right, int value) {
        int count = 0;
        for (int i = left; i <= right; i++) {   // visits every slot in the closed range
            if (arr[i] == value) count++;
        }
        return count;
    }
}
```

The constructor does no work, and each question costs time proportional to the width of its range. For a small array this is the best choice, because nothing can beat a loop that is already short.

<!-- stage: bottleneck -->
### Total Cost Grows With Questions Times Length

```predict
An array holds 100,000 entries and the service receives 100,000 questions that each span the whole array. About how many entries does the loop read in total?

About ten billion reads, because each of the 100,000 questions reads all 100,000 entries. The array never changes, so almost all of that reading repeats work already done.
```

With `n` entries and `q` questions, each question reads up to `n` entries, so the total is O(n * q). At `n = q = 10^5` that is `10^10` reads. The constructor ran in zero time, yet the service pays for that saving with every question. When questions outnumber constructor calls by a large factor, the total cost sits almost entirely in the question path.

The array also does not change between questions, so every read after the first pass over a region repeats earlier work. A faster loop does not fix this. The fix is to decide, before the first question, which summary of the array answers every possible question. The right summary depends on what the API promises about the questions, and that promise is the next point.

<!-- stage: insight -->
### Store Positions And Read The Contract

#### Keep Sorted Positions Per Value

A **position index** maps each value to the ascending list of array positions where it occurs. The constructor builds it in one pass. The constructor appends positions in index order, so each list stays sorted. A question about value `v` in the closed range `[left, right]` now needs only the list of `v`. The answer is the number of list entries inside the range, and two binary searches find that number. The first search returns how many entries are below `left`. The second returns how many entries are below `right + 1`. Their difference is the count, and the half-open end `right + 1` keeps both searches identical.

#### Let The Call Contract Pick The Plan

The summary is only half of the plan. The other half is a fact about the API, namely whether the questions are known in advance. **Offline** questions all arrive before any answer is due, so the code may reorder them. A union-find is a structure that merges vertices into groups and tells whether two vertices share a group. Consider the question whether a path joins two vertices using only edges below a given limit. Take edges of weight 2, 4 and 9 and offline questions with limits 5 and 10. The code sorts the questions by limit, merges every edge below the limit into the groups, and then answers each question with one group check. **Online** questions arrive one at a time, and each answer is due before the next question is visible. Reordering is then impossible, so the structure must answer any question from stored state alone. The update/query ratio matters as well. This lesson has no updates, so any work moved into the constructor pays back across all questions.

<!-- names: position index, offline, online -->

#### Verify What A Summary Only Suggests

Some summaries produce a suspect and not an answer. The Boyer-Moore majority vote is the clearest case. It scans the values once and holds one candidate with a counter. A value equal to the candidate raises the counter, a different value lowers it, and a counter at zero adopts the current value as the new candidate. The candidate left after the scan is the survivor. It equals the true majority value when one exists, and otherwise it is an arbitrary element. In that case the position index serves a second purpose: it counts the suspect exactly, and the answer is the suspect only when that count meets the requirement.

<!-- stage: variables -->
### Name The Facts That Choose The Plan

Four facts decide the plan before the first line of code.

- **Updates** counts the calls that change the data after construction; here it is zero.
- **Queries** is the number of questions, written `q`, and it sets how much constructor work pays back.
- **Arrival** says whether every question is known at the start or each is visible only when asked.
- **Endpoints** states whether a range is closed, `[left, right]`, or half-open, `[left, right + 1)`, and the code states which one before any comparison.

A count that can exceed the `int` range or a sum of lengths uses `long`. The counts in this lesson stay below the array length, so `int` is enough.

<!-- stage: trace -->
### Count Entries Between Two Binary Searches

#### Two Searches Over One List

Take the array `3, 1, 3, 2, 3, 1, 3` and the question for value 3 in the closed range `[1, 5]`. The index lists value 3 at positions 0, 2, 4 and 6. The two searches below look for the first stored position that is at least 1 and then the first that is at least 6, which is `right + 1`.

The first search ends at 1, because only position 0 is below 1. The second ends at 3, because positions 0, 2 and 4 are below 6. The count is 3 - 1 = 2, which matches positions 2 and 4. The step to watch is the second search, where the target is 6 and not 5. A search for 5 would give the wrong count whenever position 5 is stored, because that position belongs in the range. The first trace shows both searches step by step. In every trace row, `lo` and `hi` show the window after the move, while `mid` still marks the probe that caused the move.

```trace
{"cells":["0","2","4","6"],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"hi":4,"mid":-1},"vars":{"target":1,"search":"lower end"},"note":"lower end: find the first stored position that is at least 1. The window from lo up to but not including hi starts as the whole list."},{"at":{"lo":0,"hi":2,"mid":2},"vars":{"target":1,"search":"lower end"},"note":"mid = 2 holds 4. 4 is at least 1, so hi moves to 2."},{"at":{"lo":0,"hi":1,"mid":1},"vars":{"target":1,"search":"lower end"},"note":"mid = 1 holds 2. 2 is at least 1, so hi moves to 1."},{"at":{"lo":1,"hi":1,"mid":0},"vars":{"target":1,"search":"lower end"},"note":"mid = 0 holds 0. 0 is below 1, so lo moves to 1."},{"at":{"lo":1,"hi":1,"mid":-1},"vars":{"target":1,"search":"lower end","first":1},"note":"lo equals hi at 1, so first = 1, the list index of the first stored position that is at least 1."},{"at":{"lo":0,"hi":4,"mid":-1},"vars":{"target":6,"search":"upper end"},"note":"upper end: find the first stored position that is at least 6. The window from lo up to but not including hi starts as the whole list."},{"at":{"lo":3,"hi":4,"mid":2},"vars":{"target":6,"search":"upper end"},"note":"mid = 2 holds 4. 4 is below 6, so lo moves to 3."},{"at":{"lo":3,"hi":3,"mid":3},"vars":{"target":6,"search":"upper end"},"note":"mid = 3 holds 6. 6 is at least 6, so hi moves to 3."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"target":6,"search":"upper end","first":3,"count":2},"note":"lo equals hi at 3, so first = 3, the list index of the first stored position that is at least 6. The count is 3 - 1 = 2."}]}
```

#### Second Example With Boundary Hits

The second trace uses value positions 1, 4, 5, 8 and 9 and the closed range `[5, 8]`. A stored position that equals `left` must count, so the first search stops at index 2 and does not skip past position 5. A stored position that equals `right` must count too. The second search targets 9 and stops at index 4, which leaves position 8 inside the count. The result is 4 - 2 = 2.

```trace
{"cells":["1","4","5","8","9"],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"target":5,"search":"lower end"},"note":"lower end: find the first stored position that is at least 5. The window from lo up to but not including hi starts as the whole list."},{"at":{"lo":0,"hi":2,"mid":2},"vars":{"target":5,"search":"lower end"},"note":"mid = 2 holds 5. 5 is at least 5, so hi moves to 2."},{"at":{"lo":2,"hi":2,"mid":1},"vars":{"target":5,"search":"lower end"},"note":"mid = 1 holds 4. 4 is below 5, so lo moves to 2."},{"at":{"lo":2,"hi":2,"mid":-1},"vars":{"target":5,"search":"lower end","first":2},"note":"lo equals hi at 2, so first = 2, the list index of the first stored position that is at least 5."},{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"target":9,"search":"upper end"},"note":"upper end: find the first stored position that is at least 9. The window from lo up to but not including hi starts as the whole list."},{"at":{"lo":3,"hi":5,"mid":2},"vars":{"target":9,"search":"upper end"},"note":"mid = 2 holds 5. 5 is below 9, so lo moves to 3."},{"at":{"lo":3,"hi":4,"mid":4},"vars":{"target":9,"search":"upper end"},"note":"mid = 4 holds 9. 9 is at least 9, so hi moves to 4."},{"at":{"lo":4,"hi":4,"mid":3},"vars":{"target":9,"search":"upper end"},"note":"mid = 3 holds 8. 8 is below 9, so lo moves to 4."},{"at":{"lo":4,"hi":4,"mid":-1},"vars":{"target":9,"search":"upper end","first":4,"count":2},"note":"lo equals hi at 4, so first = 4, the list index of the first stored position that is at least 9. The count is 4 - 2 = 2."}]}
```

<!-- stage: code -->
### Build The Index And Answer By Counting

```java
final class PositionIndex {
    private final java.util.HashMap<Integer, int[]> where = new java.util.HashMap<>();

    PositionIndex(int[] arr) {
        java.util.HashMap<Integer, Integer> size = new java.util.HashMap<>();
        for (int x : arr) size.merge(x, 1, Integer::sum);          // count occurrences per value
        java.util.HashMap<Integer, Integer> used = new java.util.HashMap<>();
        for (java.util.Map.Entry<Integer, Integer> e : size.entrySet())
            where.put(e.getKey(), new int[e.getValue()]);           // exact-size list per value
        for (int i = 0; i < arr.length; i++)
            where.get(arr[i])[used.merge(arr[i], 1, Integer::sum) - 1] = i; // ascending by construction
    }

    // First list index whose stored position is at least x; equals p.length when none is.
    private static int firstAtLeast(int[] p, int x) {
        int lo = 0, hi = p.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (p[mid] < x) lo = mid + 1; else hi = mid;
        }
        return lo;
    }

    int count(int left, int right, int value) {
        int[] p = where.get(value);
        if (p == null) return 0;                                    // value never occurs
        return firstAtLeast(p, right + 1) - firstAtLeast(p, left); // closed [left, right]
    }
}
```

The constructor takes O(n) time and stores `n` positions in total. Each question costs O(log n) and allocates nothing. The result stays an `int` because a count never exceeds the array length. The midpoint formula `lo + (hi - lo) / 2` avoids overflow when `lo + hi` would pass the `int` range.

<!-- stage: applicability -->
### Choose A Plan From The Call Contract

#### Read The Contract Before Choosing

Move work into the constructor when many questions follow it on data that stays fixed. Compare the one-time cost against the saving per question times the number of questions. State the arrival rule too. If every question is known before the first answer, sorting the questions is a legal plan. If an answer is due immediately, the plan must keep a structure that answers any question alone.

#### The Invariant Of A Summary

The invariant of a summary is that it contains enough information for every allowed question without returning to the original input. The position index keeps that invariant for frequency questions, because the count of a value in any range is the difference of two ranks. A summary that fails the invariant needs a second step, such as verification of a suspect.

#### Where The Shortcut Misleads

A false friend of this design is the assumption that a cheap candidate is also a correct answer. A majority vote over a range always returns a survivor, even when no value reaches the required count. Skipping the verification step returns a plausible but wrong value. A second false friend is offline sorting under an online contract. Sorted questions give a fast algorithm only when the API reveals all questions in advance.

<!-- stage: exercises -->
### Exercises

#### [Build] Range Frequency Queries (LeetCode 2080)
<!-- id: dq39-range-frequency -->

**Prerequisites.** Binary search on a sorted array and the lower-bound idea from this lesson.

**Problem.** Design a class `RangeFreqQuery`. Its constructor receives an integer array `arr`. The method `query(left, right, value)` returns how many indices `i` with `left <= i <= right` satisfy `arr[i] == value`. Both endpoints are inclusive, so the range is closed. The array never changes after construction, so there are zero updates and many queries. The queries arrive one at a time and are not known in advance, so the design must answer each from stored state.

**Constraints.** The limits are:
- **`n`** is `arr.length` with `1 <= n <= 10^5`.
- **Values** satisfy `1 <= arr[i] <= 10^4`, and `value` has the same range.
- **Indices** satisfy `0 <= left <= right < n`.
- **Calls** are one constructor call and up to `10^5` queries, with no updates.
- **Return value** is an `int` count, and the array is not modified.

**Example 1.** Input `arr = [3,1,3,2,3,1,3]` and `query(1, 5, 3)`, output 2, because value 3 sits at indices 2 and 4 in that range.

**Example 2.** Input the same array and `query(0, 6, 9)`, output 0, because 9 never occurs.

**Hint.** If the positions of each value form a sorted list, how many list entries lie between `left` and `right`?

**Changed decision.** The constructor now stores a summary of the whole array, so each query stops reading the array.

#### [Vary] Majority Element In Subarray (LeetCode 1157)
<!-- id: dq39-subarray-majority -->

**Prerequisites.** The range frequency exercise above and a segment tree built over array leaves.

**Problem.** Design a class `MajorityChecker`. Its constructor receives an integer array `arr`. The method `query(left, right, threshold)` returns a value that occurs at least `threshold` times among indices `left` through `right` inclusive, or `-1` when no such value exists. The contract guarantees `2 * threshold > right - left + 1`, so at most one value can qualify. The array never changes. The queries arrive one at a time and are not known in advance.

**Constraints.** The limits are:
- **`n`** is `arr.length` with `1 <= n <= 2 * 10^4`.
- **Values** satisfy `1 <= arr[i] <= 2 * 10^4`.
- **Indices** satisfy `0 <= left <= right < n`.
- **Threshold** satisfies `2 * threshold > right - left + 1` and `threshold <= right - left + 1`.
- **Calls** are one constructor call and up to `10^4` queries, with no updates.

**Example 1.** Input `arr = [1,1,2,2,1,1]` and `query(0, 5, 4)`, output 1, because value 1 occurs four times.

**Example 2.** Input the same array and `query(0, 3, 3)`, output -1, because values 1 and 2 each occur twice.

**Hint.** A range can merge two survivors from a majority vote in constant time. What must you check before you trust the survivor?

**Changed decision.** Counting by position lists alone is not enough, because the value to count is unknown. A merge-friendly survivor supplies the one value to verify.

#### [Boundary] No Majority Exists (Author exercise)
<!-- id: dq39-no-majority -->

**Prerequisites.** The subarray majority exercise above.

**Problem.** Design a class `StrictMajority`. Its constructor receives an integer array `arr`. The method `query(left, right)` returns the value that occurs strictly more than half the times in indices `left` through `right` inclusive. Formally, the count satisfies `2 * count > right - left + 1`. When no value meets that rule, including an exact tie, it returns `-1`. The array never changes, and queries arrive one at a time. A cheap summary may suggest a value that does not qualify, so the method must reject it.

**Constraints.** The limits are:
- **`n`** is `arr.length` with `1 <= n <= 10^5`.
- **Values** satisfy `0 <= arr[i] < 2^15`, so `-1` never collides with a stored value.
- **Indices** satisfy `0 <= left <= right < n`.
- **Calls** are one constructor call and up to `10^5` queries, with no updates.
- **Return value** is an `int`, and the array is not modified.

**Example 1.** Input `arr = [1,2,3]` and `query(0, 2)`, output -1. The counter scan leaves the survivor 3, but 3 occurs once.

**Example 2.** Input `arr = [5,5,6,6]` and `query(0, 3)`, output -1 because the tie is not more than half. Input `query(0, 2)` on the same array gives output 5.

**Hint.** Which value does the Boyer-Moore counter leave as the survivor of the range? How do you count that survivor exactly with its position list?

**Changed decision.** The contract no longer promises a majority, so verification becomes the decisive step and not a formality.

#### [Recognize] Edge Length Limited Paths II (LeetCode 1724)
<!-- id: dq39-limited-paths-online -->

**Prerequisites.** Union-find, Kruskal's minimum spanning tree and binary lifting.

**Problem.** Design a class `LimitedPaths`. Its constructor receives `n` vertices numbered `0` to `n - 1` and an undirected edge list, where each edge is `{u, v, weight}`. The method `query(p, q, limit)` returns `true` when some path from `p` to `q` uses only edges with weight strictly less than `limit`, and `false` otherwise. Parallel edges and self-loops may appear. The graph never changes. Queries arrive one at a time and are not known in advance, so sorting the queries by `limit` is not available. Contrast this with the offline task, where all queries are known and a union-find processes them in sorted order.

**Constraints.** The limits are:
- **`n`** satisfies `2 <= n <= 10^4`, and the edge count satisfies `0 <= E <= 10^5`.
- **Weights and limits** are `int` values with `1 <= weight, limit <= 10^9`.
- **Vertices** satisfy `0 <= p, q < n`, and `p` may equal `q`.
- **Calls** are one constructor call and up to `10^4` queries, with no updates.
- **Return value** is a `boolean`, and no path sum is computed.

**Example 1.** Input four vertices, edges `{0,1,2}`, `{1,2,4}`, `{0,2,9}` and `query(0, 2, 5)`, output true through the two light edges.

**Example 2.** Input the same graph and `query(0, 2, 4)`, output false because the edge of weight 4 is not strictly less than 4. Input `query(0, 3, 100)` gives output false because vertex 3 has no edges.

**Hint.** What is the smallest possible heaviest edge over all paths between two vertices, and which tree stores it?

**Changed decision.** The summary changes from a sorted order of queries to a minimum spanning forest, because the API hides future queries.
