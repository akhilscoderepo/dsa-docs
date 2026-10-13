<!-- lesson-kind: standard -->
<!-- lesson-id: stream-order-statistics -->
## Stream Order Statistics

<!-- stage: context -->
### Why A Median Query Stalls

#### Two Failures In Production

A metrics agent records the latency of every request and shows the median on a dashboard. The first version keeps all samples in a list and sorts a copy whenever the dashboard refreshes. After a week the list holds fifty million samples. One refresh takes several seconds, the next refresh starts before the first finishes, and the agent stops answering. The median moved by a few microseconds between two refreshes, yet each refresh sorted everything again.

A trading screen shows a second failure. It displays the highest price seen in a day. A data vendor then sends a correction for a trade from ten minutes ago, and the old price must stop counting. The screen still shows the old price as the maximum, because the code only knows how to add values.

#### The Question This Lesson Answers

Both programs answer a question about the order of values, such as the middle value, the largest value or an average of the values between two ranks. Both receive a stream, so values arrive one at a time and the answer is needed after every arrival. This lesson asks which small amount of ordering a program must keep so that arrivals, corrections and expirations each cost far less than sorting everything again.

Three kinds of stream appear below, and each one fixes the data structure before any code is written. An append-only stream only adds values. A correctable stream also replaces the value stored for a key, such as a timestamp. An expiring stream drops the oldest values when a window moves. The median question is append-only, the price question is correctable, and the last exercise is expiring.

<!-- stage: naive -->
### Sorting On Every Query

The direct design stores every value in an `ArrayList` and sorts a copy when the caller asks for the middle value. The class below returns the lower middle value of the readings so far, which is the value at sorted position `(n - 1) / 2` counted from 0.

```java
final class NaiveMedian {
    private final java.util.ArrayList<Long> readings = new java.util.ArrayList<>();

    void add(long reading) { readings.add(reading); }

    long lowerMedian() {
        java.util.ArrayList<Long> copy = new java.util.ArrayList<>(readings);   // the original order stays intact
        java.util.Collections.sort(copy);                                       // full sort on every query
        return copy.get((copy.size() - 1) / 2);
    }
}
```

After the readings 12, 4 and 9 the call `lowerMedian()` returns 9, and after 20 it still returns 9. The answers are correct and the class looks finished.

```predict
A program adds 100000 readings and calls lowerMedian() after each addition. Roughly how many comparisons does the sorting alone perform, and does the work per call stay the same as the list grows?

The call after the n-th reading sorts n values, which takes about n log n comparisons. The sum over all 100000 calls is on the order of 100000 * 100000 * 17 / 2, about 8.5 * 10^10 comparisons. The work per call grows with the list, so the last calls cost about 100000 times more than the first calls, although each call changed the data by one value.
```

<!-- stage: bottleneck -->
### Repeated Sorting Of Unchanged Data

#### The Cost Of One Query

The call after the n-th reading sorts n values, so one query costs O(n log n) time and O(n) extra memory for the copy. A stream of q readings with a query after each one costs O(q^2 log q) in total. Sorting the stored list once and inserting each new value into its place does not fix the cost, because shifting list entries costs O(n) per insertion.

#### Why Most Of The Work Repeats

Almost all of that work repeats. Before the new reading arrives, the list is already ordered. The new reading changes the position of at most one value, and the query needs one value, the one in the middle. The program orders the values far below the middle and far above it, and no query ever looks at their order.

#### What Corrections Add

Corrections make the waste worse. A sorted array cannot drop one value from the middle without shifting the values after it. A `PriorityQueue` offers `remove(Object)`, which scans the queue and costs O(n) per call. A correct design therefore needs three properties. It must find the middle value in O(1) or O(log n) time. It must absorb a new value in O(log n) time. It must make a corrected value stop counting without an O(n) scan.

<!-- stage: insight -->
### Two Halves Meet At The Middle

#### Keeping Only The Middle Ordered

<!-- names: lower half, upper half, size relation, stale entry -->

The middle value needs only a dividing line between the smaller values and the larger values. Inside each side, the program needs only that side's boundary value. The **lower half** is a max-heap that holds the smaller values, so its root is the largest of them. The **upper half** is a min-heap that holds the larger values, so its root is the smallest of them. The two roots are the two values next to the dividing line.

The structure keeps three facts true after every operation, and together they form the invariant. Every value that counts belongs to exactly one half. Every value in the lower half is at most every value in the upper half. The **size relation** holds: the lower half has the same number of values as the upper half, or exactly one more. With that relation, the lower root is the lower middle value, and for an even count the average of the two roots is the usual median.

#### Inserting With One Move

A new value `x` goes into the lower half when `x` is at most the lower root, and into the upper half otherwise. That choice keeps the order between the halves. The insertion may break the size relation by one value. A single move repairs it: the root of the bigger half leaves that heap and enters the other heap. The order between the halves survives the move, because the moved root was the boundary of its side. One insertion costs a constant number of heap operations, so it costs O(log n).

#### Correcting Without Searching

A correction replaces the value stored under a key, such as a timestamp. A heap cannot find an arbitrary entry quickly. The program leaves the old entry in the heap and records the truth in a map from key to current value. An entry whose value no longer matches the map is a **stale entry**. The program checks the root against the map only when it reads the root. If the root is a stale entry, the program removes it and looks at the next root. Each entry enters a heap once and leaves it once, so the removals cost O(log n) amortized per operation.

Entries with equal values are different entries when they belong to different keys. A check by value alone cannot tell them apart, so each entry also carries its key, or a version number that the map increases with each correction. When the stream also expires its oldest values, the same idea fits into three ordered regions, and the last exercise builds them.

<!-- stage: variables -->
### State In Both Classes

The lesson uses two small classes, and the trace follows the first fields of each.

- **lower** is the max-heap of the smaller values, and its root is the lower middle value.
- **upper** is the min-heap of the larger values, and its size is never larger than the size of `lower`.
- **version** maps a sensor name to the number of readings recorded for it, and the newest reading carries that number.
- **heap** holds one entry for every reading ever recorded, each with its value, sensor name and version.

The size relation is `lower.size() == upper.size()` or `lower.size() == upper.size() + 1`. Every value in `lower` is at most every value in `upper`. An entry in `heap` counts only when its version equals `version.get(sensor)`.

<!-- stage: trace -->
### Tracing Both Structures

#### The Two Halves Over Six Readings

The first trace adds the readings 12, 4, 9, 20, 1 and 7 and shows both halves after each reading. The pointer `i` marks the reading just added. The reading 12 enters the empty lower half. The reading 4 is at most the lower root 12, so it also enters the lower half. The lower half then has two values and the upper half none, so the root 12 moves to the upper half. The reading 9 is above the lower root 4, so it enters the upper half. The upper half is now larger, so its root 9 moves to the lower half. The reading 20 enters the upper half and the sizes are equal. The reading 1 enters the lower half, which now holds one value more, and the size relation allows that. The reading 7 is at most the lower root 9, so it enters the lower half. That half is too large, so its root 9 moves to the upper half. The variable `median` holds the lower middle value after each reading.

```trace
{"cells":["12","4","9","20","1","7"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"lower":"[]","upper":"[]","median":"none"},"note":"Start: both halves are empty."},{"at":{"i":0},"vars":{"lower":"[12]","upper":"[]","median":12},"note":"12 enters the lower half. The lower middle value is 12."},{"at":{"i":1},"vars":{"lower":"[4]","upper":"[12]","median":4},"note":"4 enters the lower half. The lower half is too large, so its root 12 moves to the upper half. The lower middle value is 4."},{"at":{"i":2},"vars":{"lower":"[9,4]","upper":"[12]","median":9},"note":"9 enters the upper half. The upper half is larger, so its root 9 moves to the lower half. The lower middle value is 9."},{"at":{"i":3},"vars":{"lower":"[9,4]","upper":"[12,20]","median":9},"note":"20 enters the upper half. The lower middle value is 9."},{"at":{"i":4},"vars":{"lower":"[9,4,1]","upper":"[12,20]","median":9},"note":"1 enters the lower half. The lower middle value is 9."},{"at":{"i":5},"vars":{"lower":"[7,4,1]","upper":"[9,12,20]","median":7},"note":"7 enters the lower half. The lower half is too large, so its root 9 moves to the upper half. The lower middle value is 7."}]}
```

#### The Heap With Stale Entries

The second trace records sensor readings A=7, B=9, A=12, B=4 and A=3 and asks for the peak after each one. The pointer `i` marks the reading just recorded. The heap keeps every reading, and the map `version` says which entry is current for each sensor. The peak query removes stale roots until the root is current. The variable `heap` counts entries, stale ones included, and `popped` counts the stale roots that the latest query removed. The first four queries find a current root, so the heap only grows. The fifth recording makes A the sensor with reading 3, and the entries 12, 9 and 7 are now stale, because sensor B and sensor A both have newer versions. The query removes those three roots one after another and stops at the entry 4, which is current. The entries that remain are the two current readings.

```trace
{"cells":["A=7","B=9","A=12","B=4","A=3"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"peak":"none","heap":0,"popped":0},"note":"Start: the heap and the version map are empty."},{"at":{"i":0},"vars":{"peak":7,"heap":1,"popped":0},"note":"A records 7 as version 1. The root is current, so nothing is removed. The peak is 7."},{"at":{"i":1},"vars":{"peak":9,"heap":2,"popped":0},"note":"B records 9 as version 1. The root is current, so nothing is removed. The peak is 9."},{"at":{"i":2},"vars":{"peak":12,"heap":3,"popped":0},"note":"A records 12 as version 2. The root is current, so nothing is removed. The peak is 12."},{"at":{"i":3},"vars":{"peak":12,"heap":4,"popped":0},"note":"B records 4 as version 2. The root is current, so nothing is removed. The peak is 12."},{"at":{"i":4},"vars":{"peak":4,"heap":2,"popped":3},"note":"A records 3 as version 3. The query removed 3 stale roots. The peak is 4."}]}
```

<!-- stage: code -->
### Two Classes That Avoid Resorting

#### Lower Middle Of A Reading Stream

The class keeps two heaps and repairs the size relation after every insertion. Readings are `long` values, so a latency in nanoseconds does not overflow.

```java
final class LatencyMedian {
    private final java.util.PriorityQueue<Long> lower =
        new java.util.PriorityQueue<>(java.util.Comparator.reverseOrder());   // root is the largest of the smaller values
    private final java.util.PriorityQueue<Long> upper = new java.util.PriorityQueue<>();   // root is the smallest of the larger values

    void add(long reading) {
        if (lower.isEmpty() || reading <= lower.peek()) lower.add(reading);   // keeps every lower value at most every upper value
        else upper.add(reading);
        if (lower.size() > upper.size() + 1) upper.add(lower.poll());         // lower half too large, move its root across
        else if (upper.size() > lower.size()) lower.add(upper.poll());        // upper half too large, move its root across
    }

    long lowerMedian() {
        if (lower.isEmpty()) throw new java.util.NoSuchElementException();    // no reading yet
        return lower.peek();                                                  // the lower root is the lower middle value
    }
}
```

#### Largest Current Reading Per Sensor

The class replaces the reading of a sensor without searching the heap. Each entry stores the version of its sensor at the time it was recorded, and `peak` discards entries whose version is no longer current.

```java
final class PeakTracker {
    private record Entry(long reading, String sensor, int version) {}

    private final java.util.Map<String, Integer> version = new java.util.HashMap<>();
    private final java.util.PriorityQueue<Entry> heap =
        new java.util.PriorityQueue<>((a, b) -> Long.compare(b.reading(), a.reading()));   // largest reading at the root

    void record(String sensor, long reading) {
        int v = version.merge(sensor, 1, Integer::sum);   // each recording makes the previous entry of this sensor stale
        heap.add(new Entry(reading, sensor, v));          // the heap is never searched, so this costs O(log n)
    }

    long peak() {
        while (!heap.isEmpty() && version.get(heap.peek().sensor()) != heap.peek().version())
            heap.poll();                                  // a stale root leaves the heap for good
        if (heap.isEmpty()) throw new java.util.NoSuchElementException();
        return heap.peek().reading();                     // the root is current, so it is the maximum of the current readings
    }
}
```

#### Cost

- **LatencyMedian** costs O(log n) time per `add` and O(1) time per `lowerMedian`, with O(n) space for the stored readings.
- **PeakTracker** costs O(log n) time per call, amortized, because every entry is polled at most once, with O(n + s) space for n recordings and s sensors.

<!-- stage: applicability -->
### When To Keep Two Halves

#### Recognizing The Pattern

Use the method when a stream must answer the middle value, a rank or an aggregate between two ranks after every change, and the rank depends on the current count. The cue is a question about order whose answer moves slowly while the data changes. Before coding, name the kind of stream. Append-only streams need only the two heaps. Correctable streams add a map of current values and validation of every root. Expiring streams need a structure that removes the oldest value by value, such as an ordered multiset, because a heap cannot remove it quickly. The invariant to keep is that every counted value sits in exactly one region, and the regions respect their order and size relation.

#### A False Friend

A bounded heap that keeps the k largest values is a false friend. It answers the k-th largest value for a fixed k and discards the rest. The median has a rank that grows with the count, and a bounded heap cannot hold the values on the other side of the dividing line. A second false friend is `PriorityQueue.remove(Object)` for corrections. It gives right answers and costs O(n) per call, so the speed advantage of the heap disappears.

#### When The Method Does Not Apply

If the caller asks for arbitrary ranks, such as the 10th and the 90th percentile together, two halves with one dividing line are not enough. A Fenwick tree over compressed values, or a balanced tree with subtree sizes, answers any rank in O(log n). If every value is a small integer, a counting array answers any rank with a scan of the array. This lesson also assumes one caller, so it does not cover concurrent updates.

<!-- stage: exercises -->
### Exercises

#### [Build] Running Median (LeetCode 295)
<!-- id: st38-running-median -->

**Prerequisites.** The two halves, the size relation and the one-move repair from this lesson. The stream is append-only.

**Problem.** Design the class `MedianFinder`. The method `addNum(num)` appends the integer `num` to the stream. The method `findMedian()` returns the median of all integers added so far as a `double`. For an odd count the median is the middle value in sorted order. For an even count it is the average of the two middle values.

**Constraints.** The limits are:
- **Values** are `int` values from -10^5 to 10^5, and duplicates occur.
- **Calls** number at most 5 * 10^4 per object.
- **Queries** happen only after at least one `addNum` call.
- **Return** type is `double`, and the sum of the two middle values must not overflow.

**Example 1.** Input calls `["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]` with arguments `[[],[4],[10],[],[2],[]]`, output `[null,null,null,7.0,null,4.0]`.

**Example 2.** Input calls `["MedianFinder","addNum","findMedian","addNum","addNum","findMedian","addNum","findMedian"]` with arguments `[[],[-3],[],[-3],[8],[],[9],[]]`, output `[null,null,-3.0,null,null,-3.0,null,2.5]`.

**Hint.** After each insertion, which heap is allowed to be larger, and which root moves when the sizes differ by two?

**Changed decision.** Basic case: the stream only grows, so two heaps with the size relation are enough and no value ever leaves.

#### [Vary] Stock Price Corrections (LeetCode 2034)
<!-- id: st38-stock-price-corrections -->

**Prerequisites.** The Running Median exercise above. This exercise changes the stream from append-only to correctable, and it keeps the extreme values queryable.

**Problem.** Design the class `StockPrice`. The method `update(timestamp, price)` records the price at the timestamp. When the timestamp already has a price, the new price replaces the old price. The method `current()` returns the price at the largest timestamp recorded. The methods `maximum()` and `minimum()` return the largest and smallest of the prices that currently count, one price for each recorded timestamp.

**Constraints.** The limits are:
- **Timestamps** are `int` values from 1 to 10^9, and updates arrive in any order.
- **Prices** are `int` values from 1 to 10^9.
- **Calls** number at most 10^5 per object.
- **Queries** happen only after at least one `update` call.

**Example 1.** Input calls `["StockPrice","update","update","current","minimum","update","maximum","minimum","current"]` with arguments `[[],[3,20],[5,8],[],[],[3,2],[],[],[]]`, output `[null,null,null,8,8,null,8,2,8]`.

**Example 2.** Input calls `["StockPrice","update","update","maximum","update","maximum","current","update","maximum","minimum"]` with arguments `[[],[10,6],[10,6],[],[4,9],[],[],[4,1],[],[]]`, output `[null,null,null,6,null,9,6,null,6,1]`.

**Hint.** When a correction removes the old price of a timestamp, how does the ordered collection know that other timestamps may hold the same price?

**Changed decision.** A correction now removes one occurrence of the old price from an ordered multiset of counts, so a shared price stays until both timestamps change.

#### [Boundary] Duplicate And Stale Heap Roots (Author exercise)
<!-- id: st38-duplicate-and-stale-heap-roots -->

**Prerequisites.** The Stock Price Corrections exercise above and the stale entry definition from this lesson. This exercise replaces the ordered multiset with a plain heap, so every read of a root needs a check.

**Problem.** Design the class `ScoreBoard`. The method `set(id, score)` gives the item `id` the score `score`, and it replaces an earlier score of that item. The method `remove(id)` deletes the item and does nothing when the item is absent. The method `lowestId()` returns the id of the item with the smallest score, and the smaller id wins a tie. It returns -1 when no item exists. The class stores items in one binary heap and a map from id to current score, and it never calls `PriorityQueue.remove(Object)`.

**Constraints.** The limits are:
- **Ids** are `int` values from 0 to 10^9.
- **Scores** are `int` values from -10^9 to 10^9.
- **Calls** number at most 2 * 10^5 per object, and `set` may repeat the same pair.
- **Heap size** never exceeds the number of `set` calls.

**Example 1.** Input calls `["ScoreBoard","set","set","lowestId","set","lowestId","set","remove","lowestId","remove","lowestId"]` with arguments `[[],[7,4],[3,4],[],[3,9],[],[3,4],[7],[],[3],[]]`, output `[null,null,null,3,null,7,null,null,3,null,-1]`.

**Example 2.** Input calls `["ScoreBoard","lowestId","set","set","remove","set","lowestId","set","lowestId","set","lowestId"]` with arguments `[[],[],[2,5],[2,5],[2],[2,5],[],[9,5],[],[2,8],[]]`, output `[null,-1,null,null,null,null,2,null,2,null,9]`.

**Hint.** If an item is removed and later set to the same score, is the old entry in the heap wrong, harmless or harmful?

**Changed decision.** The check for a root is now "the map holds this id with this exact score", so one test covers removed items, replaced scores and duplicates.

#### [Recognize] Trimmed Mean Of Recent Values (LeetCode 1825)
<!-- id: st38-trimmed-mean-recent-values -->

**Prerequisites.** The Stock Price Corrections exercise above. This exercise adds expiry: the stream is expiring, because only the last `m` values count.

**Problem.** Design the class `MKAverage` with a constructor that receives integers `m` and `k`. The method `addElement(num)` appends `num` to the stream. The method `calculateMKAverage()` looks at the last `m` values. When fewer than `m` values exist, it returns -1. Otherwise it removes the `k` smallest and the `k` largest of those `m` values, with duplicates counted separately, and returns the average of the remaining values rounded down.

**Constraints.** The limits are:
- **Parameters** satisfy 3 <= m <= 10^5 and 1 <= k and 2k < m.
- **Values** are `int` values from 0 to 10^5.
- **Calls** number at most 10^5 per object.
- **Sums** reach 10^10, so the sum needs `long`.

**Example 1.** Input calls `["MKAverage","addElement","addElement","addElement","addElement","calculateMKAverage","addElement","calculateMKAverage","addElement","calculateMKAverage","addElement","calculateMKAverage","addElement","calculateMKAverage"]` with arguments `[[5,1],[6],[6],[1],[6],[],[6],[],[50],[],[0],[],[6],[]]`, output `[null,null,null,null,null,-1,null,6,null,6,null,4,null,6]`.

**Example 2.** Input calls `["MKAverage","addElement","addElement","addElement","calculateMKAverage","addElement","calculateMKAverage","addElement","calculateMKAverage","addElement","calculateMKAverage"]` with arguments `[[3,1],[10],[0],[10],[],[0],[],[0],[],[0],[]]`, output `[null,null,null,null,10,null,0,null,0,null,0]`.

**Hint.** When the oldest value leaves the window, which of the three regions contains it, and which region boundary must be repaired afterward?

**Changed decision.** Three regions, a queue and a running sum of the middle region replace the two heaps. The oldest value leaves a region by value, and the region sizes return to k, m - 2k and k.
