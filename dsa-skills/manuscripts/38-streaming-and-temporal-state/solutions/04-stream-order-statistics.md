<!-- solutions-for: 04-stream-order-statistics -->
### Solutions For Stream Order Statistics

#### Solution: [Build] Running Median (LeetCode 295)
<!-- id: st38-running-median -->

**Approach.**
The class keeps a max-heap `lower` and a min-heap `upper`. Every added integer enters `lower` when it is at most the lower root and enters `upper` otherwise, so each value in `lower` stays at most each value in `upper`. A single move of a root repairs the size relation, which allows `lower` to hold the same number of values as `upper` or one more. For an odd count the median is the lower root. For an even count it is the average of the two roots, and the sum is formed as a `long` before the division by 2.0.

The invariant is that the two heaps hold every added value once, the order between them holds and the size relation holds. The program compares the class with a sorted copy of the list on random streams, including duplicates, negative values and a single element.

**Complexity.**
- **Time** is O(log n) per `addNum`, because an insertion and at most one root move touch two heaps, and O(1) per `findMedian`, which reads one or two roots.
- **Space** is O(n), because every added value stays in one of the two heaps.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class RunningMedianBuild {
    static final class MedianFinder {
        private final PriorityQueue<Integer> lower = new PriorityQueue<>(Comparator.reverseOrder());
        private final PriorityQueue<Integer> upper = new PriorityQueue<>();

        /**
         * Appends one value to the stream.
         * Time: O(log n). Space: O(1) extra.
         * Invariant: the halves stay ordered and lower holds the same count as upper or one more.
         */
        void addNum(int num) {
            // Values at most the lower root go left, so no lower value exceeds an upper value.
            if (lower.isEmpty() || num <= lower.peek()) lower.add(num);
            else upper.add(num);
            // One extra move restores the size relation after a single insertion.
            if (lower.size() > upper.size() + 1) upper.add(lower.poll());
            else if (upper.size() > lower.size()) lower.add(upper.poll());
        }

        /**
         * Returns the median of the values added so far.
         * Time: O(1). Space: O(1).
         * Invariant: the roots are the values next to the dividing line.
         */
        double findMedian() {
            // An odd count leaves the extra value in lower, so its root is the median.
            if (lower.size() > upper.size()) return lower.peek();
            // An even count averages the two roots, and long arithmetic avoids overflow.
            return ((long) lower.peek() + upper.peek()) / 2.0;
        }
    }

    public static void main(String[] args) {
        // Example 1: the medians 7.0 and 4.0.
        MedianFinder a = new MedianFinder();
        a.addNum(4); a.addNum(10);
        if (a.findMedian() != 7.0) throw new AssertionError("example 1 first");
        a.addNum(2);
        if (a.findMedian() != 4.0) throw new AssertionError("example 1 second");
        // Example 2: duplicates and an even count with a fractional median.
        MedianFinder b = new MedianFinder();
        b.addNum(-3);
        if (b.findMedian() != -3.0) throw new AssertionError("example 2 single");
        b.addNum(-3); b.addNum(8);
        if (b.findMedian() != -3.0) throw new AssertionError("example 2 duplicate");
        b.addNum(9);
        if (b.findMedian() != 2.5) throw new AssertionError("example 2 even");
        // Extreme values must not overflow when two middle values are added.
        MedianFinder c = new MedianFinder();
        c.addNum(Integer.MAX_VALUE); c.addNum(Integer.MAX_VALUE);
        if (c.findMedian() != (double) Integer.MAX_VALUE) throw new AssertionError("overflow");
        // Random streams compare every median with a sorted copy.
        Random rnd = new Random(3801L);
        for (int t = 0; t < 2000; t++) {
            MedianFinder real = new MedianFinder();
            List<Integer> model = new ArrayList<>();
            int n = 1 + rnd.nextInt(30);
            for (int i = 0; i < n; i++) {
                int v = rnd.nextInt(21) - 10;
                real.addNum(v);
                model.add(v);
                List<Integer> sorted = new ArrayList<>(model);
                Collections.sort(sorted);
                int sz = sorted.size();
                double want = sz % 2 == 1 ? sorted.get(sz / 2) : ((long) sorted.get(sz / 2 - 1) + sorted.get(sz / 2)) / 2.0;
                if (real.findMedian() != want) throw new AssertionError("median at " + sz);
            }
        }
    }
}
```

#### Solution: [Vary] Stock Price Corrections (LeetCode 2034)
<!-- id: st38-stock-price-corrections -->

**Approach.**
The class keeps three pieces of state. The map `price` stores the current price for each timestamp. The integer `latest` is the largest timestamp recorded. The `TreeMap` named `counts` is an ordered multiset: it maps each price that currently counts to the number of timestamps that hold it. An update to a new timestamp inserts one occurrence of the price. An update to a known timestamp removes one occurrence of the old price, deleting the key when its count reaches zero, and then inserts one occurrence of the new price.

The count is necessary because two timestamps can hold the same price. Removing the key outright would drop the other timestamp's price from the maximum and the minimum. The invariant is that the counts add up to the number of recorded timestamps and every key of `counts` is a price that some timestamp holds. The program compares the class with a scan over the plain map on random operation sequences with many repeated timestamps and prices.

**Complexity.**
- **Time** is O(log n) per `update`, because the ordered map performs one removal and one insertion. Calls to `maximum` and `minimum` cost O(log n) as well, because they read the last and first key.
- **Space** is O(n) for n distinct timestamps, because the two maps hold at most one entry per timestamp.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class StockPriceVary {
    static final class StockPrice {
        private final Map<Integer, Integer> price = new HashMap<>();
        private final TreeMap<Integer, Integer> counts = new TreeMap<>();
        private int latest;

        /**
         * Records or corrects the price at a timestamp.
         * Time: O(log n). Space: O(1) extra.
         * Invariant: counts holds exactly one occurrence per recorded timestamp.
         */
        void update(int timestamp, int newPrice) {
            // The previous price of this timestamp, or null for a first record.
            Integer old = price.put(timestamp, newPrice);
            if (old != null) {
                // A correction removes one occurrence, so a shared price stays for the other timestamps.
                int left = counts.get(old) - 1;
                if (left == 0) counts.remove(old);
                else counts.put(old, left);
            }
            // The new price gains one occurrence.
            counts.merge(newPrice, 1, Integer::sum);
            // The latest timestamp can only grow, and a correction never lowers it.
            if (timestamp > latest) latest = timestamp;
        }

        /** Price at the largest timestamp. Time: O(1). Space: O(1). */
        int current() {
            // A hash lookup of the latest timestamp.
            return price.get(latest);
        }

        /** Largest current price. Time: O(log n). Space: O(1). */
        int maximum() {
            // The last key of the ordered multiset.
            return counts.lastKey();
        }

        /** Smallest current price. Time: O(log n). Space: O(1). */
        int minimum() {
            // The first key of the ordered multiset.
            return counts.firstKey();
        }
    }

    public static void main(String[] args) {
        // Example 1: a correction lowers the minimum while the latest price stays.
        StockPrice a = new StockPrice();
        a.update(3, 20); a.update(5, 8);
        if (a.current() != 8 || a.minimum() != 8) throw new AssertionError("example 1 first");
        a.update(3, 2);
        if (a.maximum() != 8 || a.minimum() != 2 || a.current() != 8) throw new AssertionError("example 1 second");
        // Example 2: a repeated update and a shared price.
        StockPrice b = new StockPrice();
        b.update(10, 6); b.update(10, 6);
        if (b.maximum() != 6) throw new AssertionError("example 2 repeat");
        b.update(4, 9);
        if (b.maximum() != 9 || b.current() != 6) throw new AssertionError("example 2 second");
        b.update(4, 1);
        if (b.maximum() != 6 || b.minimum() != 1) throw new AssertionError("example 2 third");
        // A price held by two timestamps survives the correction of one of them.
        StockPrice c = new StockPrice();
        c.update(1, 7); c.update(2, 7); c.update(1, 3);
        if (c.maximum() != 7) throw new AssertionError("shared price");
        // Random sequences compare with a scan over the plain map.
        Random rnd = new Random(3802L);
        for (int t = 0; t < 3000; t++) {
            StockPrice real = new StockPrice();
            Map<Integer, Integer> model = new HashMap<>();
            for (int step = 1 + rnd.nextInt(25); step > 0; step--) {
                int ts = 1 + rnd.nextInt(6), p = 1 + rnd.nextInt(5);
                real.update(ts, p);
                model.put(ts, p);
                int hi = Integer.MIN_VALUE, lo = Integer.MAX_VALUE, last = 0;
                for (Map.Entry<Integer, Integer> e : model.entrySet()) {
                    hi = Math.max(hi, e.getValue());
                    lo = Math.min(lo, e.getValue());
                    last = Math.max(last, e.getKey());
                }
                if (real.maximum() != hi || real.minimum() != lo || real.current() != model.get(last))
                    throw new AssertionError("mismatch");
            }
        }
    }
}
```

#### Solution: [Boundary] Duplicate And Stale Heap Roots (Author exercise)
<!-- id: st38-duplicate-and-stale-heap-roots -->

**Approach.**
The board keeps a map `scores` from id to the current score and a heap of entries ordered by score and then by id. The map is the only source of truth. The method `set` stores the score in the map and pushes an entry, unless the item already has exactly that score, because the heap then already holds a matching entry. The method `remove` deletes the id from the map and touches no heap entry.

An entry is valid exactly when the map holds its id with its exact score. The method `lowestId` removes invalid roots until the root is valid, then returns the id of the root without removing it. A removed item, a replaced score and a duplicate entry all fail or pass this one test correctly. An old entry that becomes valid again after the same pair is set once more is a harmless duplicate, because both entries name the same truth. The invariant is that every current pair has at least one entry in the heap, so the first valid root is the minimum.

The program compares the board with a scan over the map and asserts that the heap never holds more entries than the number of `set` calls.

**Complexity.**
- **Time** is O(log n) amortized per call, because every entry is pushed once and removed at most once, and each push or removal costs O(log n).
- **Space** is O(n) for n `set` calls, because stale entries stay until a query reaches them.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Random;

public final class ScoreBoardBoundary {
    static final class ScoreBoard {
        private record Entry(int score, int id) {}

        private final Map<Integer, Integer> scores = new HashMap<>();
        private final PriorityQueue<Entry> heap = new PriorityQueue<>((x, y) ->
            x.score() != y.score() ? Integer.compare(x.score(), y.score()) : Integer.compare(x.id(), y.id()));
        int setCalls;

        /**
         * Gives an item a score, replacing an earlier score.
         * Time: O(log n). Space: O(1) extra.
         * Invariant: every current pair has an entry in the heap.
         */
        void set(int id, int score) {
            setCalls++;
            // The map is the truth, so the replaced score needs no heap search.
            Integer old = scores.put(id, score);
            // An identical pair already has its entry, so pushing again would only add a duplicate.
            if (old == null || old != score) heap.add(new Entry(score, id));
        }

        /**
         * Deletes an item if it exists.
         * Time: O(1). Space: O(1).
         * Invariant: heap entries of the item become invalid because the map no longer holds the id.
         */
        void remove(int id) {
            // Only the map changes, and the heap entries are discarded when they reach the root.
            scores.remove(id);
        }

        /**
         * Returns the id with the smallest score, ties to the smaller id, or -1 when empty.
         * Time: O(log n) amortized. Space: O(1).
         * Invariant: after the loop the root is valid, so it is the minimum.
         */
        int lowestId() {
            // A root is stale when the map lacks its id or holds another score.
            while (!heap.isEmpty()) {
                Entry top = heap.peek();
                Integer now = scores.get(top.id());
                if (now != null && now == top.score()) break;
                // Each stale entry leaves the heap once, which pays for the check.
                heap.poll();
            }
            // An empty heap means no item exists.
            return heap.isEmpty() ? -1 : heap.peek().id();
        }

        int heapSize() { return heap.size(); }
    }

    public static void main(String[] args) {
        // Example 1: a tie, a replaced score, a removal and an empty board.
        ScoreBoard a = new ScoreBoard();
        a.set(7, 4); a.set(3, 4);
        if (a.lowestId() != 3) throw new AssertionError("tie");
        a.set(3, 9);
        if (a.lowestId() != 7) throw new AssertionError("replaced");
        a.set(3, 4); a.remove(7);
        if (a.lowestId() != 3) throw new AssertionError("after remove");
        a.remove(3);
        if (a.lowestId() != -1) throw new AssertionError("empty");
        // Example 2: empty start, repeated pair, remove then set the same pair again.
        ScoreBoard b = new ScoreBoard();
        if (b.lowestId() != -1) throw new AssertionError("empty start");
        b.set(2, 5); b.set(2, 5); b.remove(2); b.set(2, 5);
        if (b.lowestId() != 2) throw new AssertionError("example 2 first");
        b.set(9, 5);
        if (b.lowestId() != 2) throw new AssertionError("example 2 tie");
        b.set(2, 8);
        if (b.lowestId() != 9) throw new AssertionError("example 2 last");
        // Removing an absent id changes nothing.
        b.remove(12345);
        if (b.lowestId() != 9) throw new AssertionError("absent remove");
        // Random sequences compare with a scan and check the heap bound.
        Random rnd = new Random(3803L);
        for (int t = 0; t < 4000; t++) {
            ScoreBoard real = new ScoreBoard();
            Map<Integer, Integer> model = new HashMap<>();
            for (int step = rnd.nextInt(30); step > 0; step--) {
                int op = rnd.nextInt(3), id = rnd.nextInt(5), sc = rnd.nextInt(4) - 1;
                if (op == 0) { real.set(id, sc); model.put(id, sc); }
                else if (op == 1) { real.remove(id); model.remove(id); }
                int want = -1, best = Integer.MAX_VALUE;
                for (Map.Entry<Integer, Integer> e : model.entrySet()) {
                    if (e.getValue() < best || (e.getValue() == best && e.getKey() < want)) { best = e.getValue(); want = e.getKey(); }
                }
                if (real.lowestId() != want) throw new AssertionError("lowestId");
                if (real.heapSize() > real.setCalls) throw new AssertionError("heap bound");
            }
        }
    }
}
```

#### Solution: [Recognize] Trimmed Mean Of Recent Values (LeetCode 1825)
<!-- id: st38-trimmed-mean-recent-values -->

**Approach.**
The class holds the last `m` values in a queue and also in three ordered multisets named `low`, `mid` and `high`. Each multiset is a `TreeMap` from value to count with a size and a sum. Every stored value belongs to exactly one region. Every value in `low` is at most every value in `mid`, and every value in `mid` is at most every value in `high`. When the window holds `m` values, `low` and `high` hold `k` values each and `mid` holds the remaining `m - 2k` values.

An addition places the new value by comparing it with the top of `low` and the bottom of `high`. When the queue then exceeds `m` values, the oldest value leaves whichever region holds a copy of it. Equal values in different regions are interchangeable, so removing any copy keeps the order between regions. A repair step then moves boundary values: it first shrinks a region that holds more than `k` values, and then refills `low` and `high` from the nearest end of `mid`. The answer is the sum of `mid`, held as a `long`, divided by `m - 2k` with integer division, which rounds down because all values are non-negative.

The invariant after each addition is the order between regions and the sizes `k`, `m - 2k`, `k` once `m` values exist. Each addition causes a constant number of tree operations. The program compares the class with sorting the last `m` values on random streams with many duplicates.

**Complexity.**
- **Time** is O(log m) per `addElement`, because it performs a constant number of insertions, removals and boundary moves in ordered maps. Each `calculateMKAverage` costs O(1), because it divides two stored numbers.
- **Space** is O(m), because the queue and the three regions together hold the last `m` values.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.TreeMap;

public final class TrimmedMeanRecognize {
    /** Ordered multiset of ints that tracks its size and its sum. */
    static final class Region {
        final TreeMap<Integer, Integer> map = new TreeMap<>();
        int size;
        long sum;

        void add(int v) { map.merge(v, 1, Integer::sum); size++; sum += v; }

        boolean remove(int v) {
            // Absent values report false so the caller can try another region.
            Integer c = map.get(v);
            if (c == null) return false;
            if (c == 1) map.remove(v); else map.put(v, c - 1);
            size--; sum -= v;
            return true;
        }

        int min() { return map.firstKey(); }
        int max() { return map.lastKey(); }
    }

    static final class MKAverage {
        private final int m, k;
        private final ArrayDeque<Integer> window = new ArrayDeque<>();
        private final Region low = new Region(), mid = new Region(), high = new Region();

        MKAverage(int m, int k) { this.m = m; this.k = k; }

        /**
         * Appends a value and expires the oldest one when more than m values exist.
         * Time: O(log m). Space: O(1) extra.
         * Invariant: regions are ordered, and sizes are k, m - 2k, k once the window is full.
         */
        void addElement(int num) {
            window.addLast(num);
            // Place the value by the region boundaries, which keeps the order between regions.
            if (low.size > 0 && num <= low.max()) low.add(num);
            else if (high.size > 0 && num >= high.min()) high.add(num);
            else mid.add(num);
            if (window.size() > m) {
                // The oldest value leaves one region that holds a copy of it.
                int old = window.pollFirst();
                if (!low.remove(old) && !mid.remove(old)) high.remove(old);
            }
            // Shrink oversized outer regions first, so mid never lacks a value to lend.
            while (low.size > k) { int v = low.max(); low.remove(v); mid.add(v); }
            while (high.size > k) { int v = high.min(); high.remove(v); mid.add(v); }
            // Refill the outer regions from the nearest end of mid.
            while (low.size < k && mid.size > 0) { int v = mid.min(); mid.remove(v); low.add(v); }
            while (high.size < k && mid.size > 0) { int v = mid.max(); mid.remove(v); high.add(v); }
        }

        /**
         * Returns the rounded-down mean of the middle region, or -1 before m values exist.
         * Time: O(1). Space: O(1).
         * Invariant: mid.sum is the sum of the m - 2k values between the trimmed ends.
         */
        int calculateMKAverage() {
            // Fewer than m values means the window is not full.
            if (window.size() < m) return -1;
            // A long sum divided by the middle size, rounded down for non-negative values.
            return (int) (mid.sum / (m - 2 * k));
        }
    }

    public static void main(String[] args) {
        // Example 1: m = 5, k = 1.
        MKAverage a = new MKAverage(5, 1);
        int[] in1 = {6, 6, 1, 6};
        for (int v : in1) a.addElement(v);
        if (a.calculateMKAverage() != -1) throw new AssertionError("example 1 before full");
        a.addElement(6);
        if (a.calculateMKAverage() != 6) throw new AssertionError("example 1 first");
        a.addElement(50);
        if (a.calculateMKAverage() != 6) throw new AssertionError("example 1 second");
        a.addElement(0);
        if (a.calculateMKAverage() != 4) throw new AssertionError("example 1 third");
        a.addElement(6);
        if (a.calculateMKAverage() != 6) throw new AssertionError("example 1 fourth");
        // Example 2: m = 3, k = 1, zeros and duplicates.
        MKAverage b = new MKAverage(3, 1);
        b.addElement(10); b.addElement(0); b.addElement(10);
        if (b.calculateMKAverage() != 10) throw new AssertionError("example 2 first");
        b.addElement(0);
        if (b.calculateMKAverage() != 0) throw new AssertionError("example 2 second");
        // A full window of 10^5 values of 10^5 sums to 10^10, which exceeds the int range.
        MKAverage big = new MKAverage(100000, 1);
        for (int i = 0; i < 100000; i++) big.addElement(100000);
        if (big.calculateMKAverage() != 100000) throw new AssertionError("wide window");
        // Random streams compare with sorting the last m values.
        Random rnd = new Random(3804L);
        for (int t = 0; t < 1500; t++) {
            int m = 3 + rnd.nextInt(8);
            int k = 1 + rnd.nextInt((m - 1) / 2);
            MKAverage real = new MKAverage(m, k);
            List<Integer> all = new ArrayList<>();
            for (int step = 1 + rnd.nextInt(40); step > 0; step--) {
                int v = rnd.nextInt(7);
                real.addElement(v);
                all.add(v);
                int want = -1;
                if (all.size() >= m) {
                    List<Integer> w = new ArrayList<>(all.subList(all.size() - m, all.size()));
                    java.util.Collections.sort(w);
                    long s = 0;
                    for (int i = k; i < m - k; i++) s += w.get(i);
                    want = (int) (s / (m - 2 * k));
                }
                if (real.calculateMKAverage() != want) throw new AssertionError("mk average");
            }
        }
    }
}
```
