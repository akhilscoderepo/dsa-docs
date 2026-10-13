<!-- lesson-kind: combination -->
<!-- lesson-id: ordered-stream-state -->
## Ordered Stream State

<!-- stage: context -->
### Why The Daily High Never Went Down

A market dashboard shows the highest price of each instrument for the current day. The service keeps every price in a max-heap, and the root is the answer. At 10:02 a feed sends a tick with price 9100 for an instrument that trades near 910. At 10:05 the exchange sends a correction for that timestamp with price 910. The service writes the new price into its table of timestamps and prices, but the old tick still sits inside the heap. The dashboard shows 9100 as the daily high until the service restarts.

Nothing crashed, and the heap did exactly what a heap does. The bug lies in the contract. The stream is correctable, and the structure fits only a stream that grows. The question of this lesson is how to keep an ordered answer correct. The answer can be a maximum, a k-th largest value or a median, and values arrive, change, disappear and expire.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

The heap lessons supplied the bounded heap. A min-heap of size k keeps the k largest values, and its root is the k-th largest. The lessons on ordered sets supplied the count map, where a `TreeMap` from value to count gives the smallest and the largest value in O(log n). The design chapter supplied the habit of keeping one table that holds the truth about every key, so that a second structure is only an index over it. The first lessons of this chapter supplied the window queue, where the oldest value expires from the front. They also supplied the rule that an API states its time and its inclusive edges.

This lesson joins them. The new work is a way to decide which structure fits each kind of stream. An append-only stream needs a bounded heap. A correctable stream needs an index that can be wrong in a controlled way. An expiring stream needs both a queue of arrival order and an ordered split of the live values. The Java rule that goes with all three is simple: `PriorityQueue.remove(Object)` scans the whole heap, so a hot path never calls it.

<!-- stage: naive -->
### Keep Everything And Sort On Demand

The direct design stores every value in a list and sorts a copy whenever a question arrives. A correction overwrites the stored value, so the list is always the truth. The class below answers the k-th largest value and the maximum.

```java
final class SortingBoard {
    private final java.util.ArrayList<Long> values = new java.util.ArrayList<>();

    // Appends a value to the stream.
    void add(long v) { values.add(v); }

    // Replaces the value at a position after a correction.
    void correct(int index, long v) { values.set(index, v); }

    // Returns the k-th largest value, or null when fewer than k values exist.
    Long kth(int k) {
    if (values.size() < k) return null;
    java.util.ArrayList<Long> copy = new java.util.ArrayList<>(values);
    copy.sort(java.util.Collections.reverseOrder());
    return copy.get(k - 1);
    }
}
```

Every answer is right, including the answers after corrections, and a test with ten values passes at once. The list also serves as a trusted reference for faster designs later in this lesson.

```predict
A feed adds 100000 values, and a user asks for the 3rd largest after each addition. About how many comparisons does the sorting design perform in total?

Each question sorts a copy of m values, which costs about m log m comparisons. The sum over m from 1 to 100000 is about n squared over 2 times log n, which is roughly 8 times 10^10 comparisons. The service falls behind within seconds, and almost all of the work repeats an order that did not change since the previous question.
```

<!-- stage: bottleneck -->
### Re-Sorting Values That Did Not Move

Each question pays O(n log n) to rebuild an order of which almost every pair was already known. After one new value arrives, the order of the old values stays the same, and only the place of the new value is open. A stream of n values with a question after each value costs O(n^2 log n) in total, and the copy of the list adds O(n) memory traffic per question.

A faster design has to answer from a structure that changes a little per event. Three kinds of event change the structure in different ways.

An append adds one value. A correction replaces one value, so an old value must stop counting somewhere inside the structure. An expiry removes the oldest value, and the oldest value can sit anywhere in the order. A binary heap supports the first event in O(log n) and has no fast way to find a value inside it. A call to `PriorityQueue.remove(Object)` takes O(n) time, so n corrections cost O(n^2). A design is therefore good only if it meets two conditions. First, every answer comes from the roots of a few heaps or from the ends of an ordered map. Second, a correction or an expiry costs O(log n) amortized and never searches the inside of a heap.

<!-- stage: insight -->
### Split The Values And Check The Roots

#### Say Which Kind Of Stream It Is

<!-- names: region, boundary, stale entry -->

State the stream kind before choosing a structure. An append-only stream never changes a value. A correctable stream replaces or deletes a value by key. An expiring stream drops the oldest value when the window moves. The kind decides how much of the data a structure must keep. A heap of size k is enough only for append-only streams with a fixed k, because every discarded value can never matter again.

#### Give Every Value Exactly One Home

A **region** is a group of live values that one structure holds, and the regions together cover every live value exactly once. The lower half of a median finder is a region, and so is the set of the k largest values. The regions are ordered: every value of one region is at most every value of the next. The order between regions is what makes the answer readable from the roots. The median is the largest value of the lower region, and the k-th largest is the smallest value of the top region.

#### Compare Against The Edge Between Regions

The **boundary** is the pair of values where two regions meet, such as the largest value of the lower region and the smallest value of the upper region. The code routes a new value by comparing it with the boundary. A value above the boundary joins the upper region. If a region then holds too many values, its extreme value crosses the boundary into the next region. One move repairs the sizes, because only the extreme value can cross without breaking the order.

#### Let Wrong Entries Wait Inside The Heap

A **stale entry** is a heap item that no longer matches the truth. The item can hold a deleted key, an old price or a timestamp that left the window. The design never searches for a stale entry. It keeps a table of truth, and it discards a heap root when the table disagrees with it. The design creates each entry once and discards it at most once, so n events cost O(n log n) in total. An entry buried below a good root costs nothing until it reaches the root, and a rebuild from the table clears buried entries when they outnumber the live ones.

The three ideas combine into one invariant. Every live value belongs to exactly one region. The regions are ordered across the boundary. The code checks every root against the truth before it reads the root.

<!-- stage: variables -->
### State In The Ordered Structures

The structures below are small, and each piece of state has one owner and one rule for when it changes.

- **truth** is the map from key to live value, and every correction and deletion changes it first.
- **top** is the min-heap of the k largest values. Its root is the boundary and the k-th largest value.
- **rest** is the max-heap of the other values, used when k may grow later.
- **heap** is the lazy max-heap of entries, and an entry stays in it after the truth moves on.
- **k** is the rank. In the first example it never changes. The exercises let it change.
- **now** is the current time, and it is a parameter of every call that depends on time. A test passes any value of `now` it wants, and no method reads the system clock.

Sums and timestamps use `long`. A sum of 10^5 values near 10^9 reaches 10^14, which an `int` cannot hold. The state changes in one order: first update the truth, then push at most one new entry, then repair the sizes, and only then read a root.

<!-- stage: trace -->
### Admitting Values And Discarding Stale Roots

#### Keeping The Three Largest Of An Append-Only Stream

The stream is append-only, and the question is always the third largest value. The pointer `i` marks the value that just arrived. The heap `top` holds at most three values, and its root is the boundary. The first three values fill the heap without any comparison. The value 20 then beats the boundary 4, so it replaces the root. The value 1 loses to the boundary and leaves the heap unchanged. The value 7 loses against the new boundary 9, and 15 beats it. The answer after the last value is the root 12.

```trace
{"cells":["12","4","9","20","1","7","15"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"top":"[]","boundary":"none"},"note":"Start: the heap is empty and no boundary exists."},{"at":{"i":0},"vars":{"top":"[12]","boundary":"none"},"note":"The heap holds fewer than 3 values, so 12 is admitted."},{"at":{"i":1},"vars":{"top":"[4,12]","boundary":"none"},"note":"The heap holds fewer than 3 values, so 4 is admitted."},{"at":{"i":2},"vars":{"top":"[4,9,12]","boundary":"4"},"note":"The heap holds fewer than 3 values, so 9 is admitted."},{"at":{"i":3},"vars":{"top":"[9,12,20]","boundary":"9"},"note":"The value 20 beats the boundary 4, so it replaces the root 4."},{"at":{"i":4},"vars":{"top":"[9,12,20]","boundary":"9"},"note":"The value 1 does not beat the boundary 9, so the heap stays unchanged."},{"at":{"i":5},"vars":{"top":"[9,12,20]","boundary":"9"},"note":"The value 7 does not beat the boundary 9, so the heap stays unchanged."},{"at":{"i":6},"vars":{"top":"[12,15,20]","boundary":"12"},"note":"The value 15 beats the boundary 9, so it replaces the root 9."}]}
```

#### Correcting And Deleting With A Lazy Heap

The stream is correctable. The pointer `op` marks the operation that was just applied. The table `truth` is always right, and the heap `heap` may contain stale entries. The correction of key b to 20 leaves the entry 50 in the heap. The next maximum query meets that entry at the root, finds that the truth for b is 20, and discards it. The root is then 30, which matches the truth for key a, so the answer is 30. The deletion of a leaves its entry stale in the same way. The final query discards it and returns 20. After a new value arrives for key a, the new entry becomes the root.

```trace
{"cells":["set a 30","set b 50","set b 20","max","erase a","max","set a 25","max"],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"truth":"{}","heap":"[]"},"note":"Start: no key has a value and the heap is empty."},{"at":{"op":0},"vars":{"truth":"{a=30}","heap":"[30a]"},"note":"The truth for a becomes 30, and one new entry is pushed. Any older entry for a is now stale."},{"at":{"op":1},"vars":{"truth":"{a=30,b=50}","heap":"[50b,30a]"},"note":"The truth for b becomes 50, and one new entry is pushed. Any older entry for b is now stale."},{"at":{"op":2},"vars":{"truth":"{a=30,b=20}","heap":"[50b,30a,20b]"},"note":"The truth for b becomes 20, and one new entry is pushed. Any older entry for b is now stale."},{"at":{"op":3},"vars":{"truth":"{a=30,b=20}","heap":"[30a,20b]","answer":"30"},"note":"The query discards the stale root 50b and finds the live root 30, which agrees with the truth."},{"at":{"op":4},"vars":{"truth":"{b=20}","heap":"[30a,20b]"},"note":"The key a leaves the truth. Its entries stay in the heap and are now stale."},{"at":{"op":5},"vars":{"truth":"{b=20}","heap":"[20b]","answer":"20"},"note":"The query discards the stale root 30a and finds the live root 20, which agrees with the truth."},{"at":{"op":6},"vars":{"truth":"{a=25,b=20}","heap":"[25a,20b]"},"note":"The truth for a becomes 25, and one new entry is pushed. Any older entry for a is now stale."},{"at":{"op":7},"vars":{"truth":"{a=25,b=20}","heap":"[25a,20b]","answer":"25"},"note":"The root 25 agrees with the truth, so nothing is discarded."}]}
```

<!-- stage: code -->
### A Bounded Heap And A Lazy Heap

#### Keeping The Largest K Values

The class `TopKHeap` handles the append-only stream with a fixed rank. The heap never holds more than k values, so memory is O(k). Each addition costs O(log k), and the query costs O(1).

```java
final class TopKHeap {
    private final int k;
    private final java.util.PriorityQueue<Integer> top = new java.util.PriorityQueue<>();

    TopKHeap(int k) {
        if (k < 1) throw new IllegalArgumentException("k must be at least 1");
        this.k = k;
    }

    void add(int v) {
        if (top.size() < k) top.add(v);                    // the heap is not full, so every value is admitted
        else if (v > top.peek()) { top.poll(); top.add(v); } // the value beats the boundary and replaces the root
    }

    Integer kth() {
        return top.size() == k ? top.peek() : null;        // the root is the k-th largest once k values exist
    }
}
```

#### Checking Roots Against The Truth

The class `LazyMaxHeap` handles a correctable stream. The map `truth` holds each live value. A heap entry records the key and the value at the time of the push. The method `max` discards roots that the truth contradicts, so a correction or a deletion costs one map operation.

```java
final class LazyMaxHeap {
    private record Entry(String key, long value) {}

    private final java.util.HashMap<String, Long> truth = new java.util.HashMap<>();
    private final java.util.PriorityQueue<Entry> heap =
        new java.util.PriorityQueue<>((a, b) -> Long.compare(b.value(), a.value()));

    void set(String key, long value) {
        truth.put(key, value);                             // the truth changes first
        heap.add(new Entry(key, value));                   // one new entry; older entries for the key become stale
    }

    void erase(String key) {
        truth.remove(key);                                 // no heap search; the old entries become stale
    }

    java.util.OptionalLong max() {
        while (!heap.isEmpty()) {
            Entry top = heap.peek();
            Long live = truth.get(top.key());
            if (live != null && live == top.value()) return java.util.OptionalLong.of(top.value()); // the root agrees with the truth
            heap.poll();                                   // the root is stale; each entry leaves at most once
        }
        return java.util.OptionalLong.empty();             // nothing live remains
    }
}
```

#### Cost And Java Details

- **TopKHeap** costs O(log k) per addition and O(k) space.
- **LazyMaxHeap** costs O(log n) amortized per event, because each entry enters the heap once and leaves it at most once.
- **Memory** of `LazyMaxHeap` grows with the number of events unless a rebuild from `truth` runs when the heap holds more than twice the live count.

The comparison `live == top.value()` unboxes the `Long` before it compares, so the value 1000 does not fail the way two boxed `Long` objects can under `==`. The comparator uses `Long.compare`, since the difference of two large `long` values can overflow.

<!-- stage: applicability -->
### When Ordered Regions Fit

#### Recognizing The Pattern

Look for a question about an extreme or a rank over data that changes. Examples are the largest value so far and the middle value of the last hundred. Then ask which kind of event the stream contains. The invariant to state has three parts. Every live value has one home, the regions are ordered, and the code trusts a heap root only after the truth confirms it. Equal values are the usual trap, so the routing rule must say which side a tie takes and the test must contain ties.

#### The Nearest False Friend

A bounded heap that keeps the k largest values is a false friend for the median and for any rank that grows with the count. It answers a fixed rank and discards the values on the other side of the boundary. A `TreeSet` is a second false friend, because it merges equal values into one item, so the count of a rank drifts after the first duplicate. A `TreeMap` from value to count fixes the duplicates.

#### When Not To Use It

If the questions ask for arbitrary ranks, such as the 10th and the 90th percentile together, two regions with one boundary are not enough. A Fenwick tree over compressed values answers any rank in O(log n). If the values are small integers, a counting array does the same without a heap. If corrections are rare and the stream is short, the sorted list of the first design is the clearest code. A lazy heap then adds complexity without a gain.

<!-- stage: exercises -->
### Exercises

#### [Build] Kth Largest With Changing Rank (LeetCode 703)
<!-- id: st38o-kth-moving-k -->

**Prerequisites.** The bounded heap from the code stage. The stream is append-only, but the rank can change. This exercise changes the contract of LeetCode 703: a bounded heap of fixed size loses the values that a larger rank needs.

**Problem.** Design the class `RankTracker`. The constructor takes the initial rank `k`. The method `add(v)` appends the integer `v` to the stream. The method `setRank(newK)` replaces the rank. The method `kth()` returns the k-th largest value among all added values, where equal values count separately, or `null` when fewer than k values exist.

**Constraints.** The limits are:
- **Rank** is an integer from 1 to 10^5 at every moment.
- **Values** are `int` values from -10^9 to 10^9, and duplicates occur.
- **Calls** number at most 10^5 per object.
- **Cost** of `setRank` is proportional to the change in rank times a logarithm.

**Example 1.** Input calls `["RankTracker","add","add","kth","add","kth","setRank","kth","add","kth","setRank","kth"]` with arguments `[[2],[6],[11],[],[8],[],[4],[],[3],[],[1],[]]`, output `[null,null,null,6,null,8,null,null,null,3,null,11]`.

**Example 2.** Input calls `["RankTracker","kth","add","add","kth","add","kth","setRank","kth","setRank","kth","add","add","kth"]` with arguments `[[3],[],[-5],[-5],[],[-9],[],[2],[],[5],[],[0],[7],[]]`, output `[null,null,null,null,null,null,-9,null,-5,null,null,null,null,-9]`.

**Hint.** When the rank grows, which values must the structure still hold, and from which heap does the next value come?

**Changed decision.** A single bounded heap is no longer enough. The structure keeps two ordered regions, the top k values and all others, and a change of rank moves values across the boundary.

#### [Vary] Median Of The Last W Values (LeetCode 295)
<!-- id: st38o-window-median -->

**Prerequisites.** The first exercise above and the stale-entry idea from the insight stage. This exercise changes the contract of LeetCode 295: the stream expires, so the median covers only the newest values.

**Problem.** Design the class `WindowMedian`. The constructor takes the window size `w`. The method `add(x)` appends the integer `x`; when more than `w` values exist, the oldest one leaves the window. The method `median()` returns the lower median of the values in the window. For `c` values in the window, this is the value at zero-based position `(c - 1) / 2` in sorted order. It throws `IllegalStateException` when the window is empty.

**Constraints.** The limits are:
- **Window** size `w` is an integer from 1 to 10^5.
- **Values** are `int` values from -10^9 to 10^9, and duplicates occur.
- **Calls** number at most 2 * 10^5 per object.
- **Memory** stays O(w) however long the stream runs.

**Example 1.** Input `w = 3`. Add `8, 1, 5, 9, 2, 2` one at a time and query after each. The output is `8, 1, 5, 5, 5, 2`.

**Example 2.** Input `w = 2`. Add `-4, -4, 7, -1, -1, 0` and query after each. The output is `-4, -4, -4, -1, -1, -1`.

**Hint.** The oldest value may sit deep inside either heap. How can the live counts stay correct while its entry stays where it is?

**Changed decision.** The oldest value expires and the two halves must stay balanced by live count. Expiry marks a value dead, and the code discards a dead root when it reaches the top.

#### [Boundary] Price Timeline With Deletions (LeetCode 2034)
<!-- id: st38o-timeline-deletions -->

**Prerequisites.** The lazy heap from the code stage and the second exercise above. This exercise changes the contract of LeetCode 2034: records can be deleted, and the heaps must stay small.

**Problem.** Design the class `PriceTimeline`. The method `update(t, p)` sets the price at timestamp `t` to `p` and replaces an earlier price at `t`. The method `remove(t)` deletes the record at `t` and returns `true` when a record existed. The methods `current()`, `maximum()` and `minimum()` return the price at the largest live timestamp, the highest live price and the lowest live price. Each throws `IllegalStateException` when no record is live.

**Constraints.** The limits are:
- **Timestamps** are `long` values from 1 to 10^12, and arrive in any order.
- **Prices** are `long` values from 0 to 10^12.
- **Calls** number at most 2 * 10^5 per object.
- **Memory** of the heaps stays within a constant factor of the live record count plus a fixed number of entries.

**Example 1.** Input calls `update(10,40)`, `update(20,25)`, `update(15,60)`, then `maximum()`, `minimum()`, `current()`, `remove(20)`, `current()`, `remove(20)`, `update(15,5)`, `maximum()`, `minimum()`, output `60`, `25`, `25`, `true`, `60`, `false`, `40`, `5`.

**Example 2.** Input calls `update(7,30)`, `update(7,30)`, `update(3,30)`, `remove(7)`, `current()`, `maximum()`, `remove(3)`, then `minimum()`, output `true`, `30`, `30`, `true`, and an `IllegalStateException`.

**Hint.** Which structure gives the largest live timestamp after the latest record disappears, and when does a heap entry still count?

**Changed decision.** Deletion makes an entry stale without replacing it, so validity means the timestamp is live with the same price. A rebuild from the table keeps memory proportional to the live records.

#### [Recognize] Trimmed Mean With A Correction (LeetCode 1825)
<!-- id: st38o-amended-trimmed-mean -->

**Prerequisites.** The second exercise above and the idea that each live value has one home among ordered regions. This exercise is a transfer prompt. The interview question asks how three regions behave when the two cuts differ and the newest value can change. It changes the contract of LeetCode 1825.

**Problem.** Design the class `TrimmedWindow`. The constructor takes `m`, `lo` and `hi` with `m > lo + hi`. The method `add(x)` appends the non-negative integer `x`, and the oldest value leaves when more than `m` values exist. The method `amendLast(x)` replaces the newest value by the non-negative integer `x`, and it throws `IllegalStateException` when no value exists. The method `average()` returns -1 while fewer than `m` values exist. Otherwise it removes the `lo` smallest and the `hi` largest values of the window and returns the floor of the mean of the remaining `m - lo - hi` values.

**Constraints.** The limits are:
- **Window** size `m` is an integer from 1 to 10^5, with `lo` and `hi` from 0 up to `m - 1`.
- **Values** are `int` values from 0 to 10^9, and duplicates occur.
- **Calls** number at most 10^5 per object.
- **Sums** need `long` arithmetic.

**Example 1.** Input `m = 4`, `lo = 1`, `hi = 0`. Add `9, 2, 6, 4, 20` in order and call `average()` after the third, fourth and fifth value. Then call `amendLast(1)` and `average()`. The output is `-1`, `6`, `10`, `4`.

**Example 2.** Input `m = 5`, `lo = 2`, `hi = 1`. Add `0, 0, 7, 7, 3`, then call `average()`, `amendLast(100)`, `average()`, `add(1)`, `average()`, `add(20)` and `average()`. The output is `5`, `7`, `7`, `13`.

**Hint.** When a value leaves, which region might hold it, and which neighbor refills the region that lost a value?

**Changed decision.** The cut sizes differ on the two sides, and the newest value can change after the code routed it. Removal and insertion both go through the same repair that restores the region sizes.
