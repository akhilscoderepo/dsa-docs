<!-- solutions-for: 92-ordered-stream-state -->
### Solutions For Ordered Stream State

#### Solution: [Build] Kth Largest With Changing Rank (LeetCode 703)
<!-- id: st38o-kth-moving-k -->

**Approach.**
The stream is append-only, but the rank can grow, so no value can be thrown away. The tracker keeps two ordered regions: a min-heap `top` that holds the k largest values, and a max-heap `rest` that holds every other value. The root of `top` is the boundary and the answer. A new value that beats the boundary enters `top`, and the old boundary drops into `rest`. A value that ties or loses goes to `rest` directly.

A change of rank moves values across the boundary. A smaller rank pushes roots of `top` into `rest`, and a larger rank pulls roots of `rest` into `top`. The invariant is that `top` holds the min(k, count) largest values, and every value in `top` is at least every value in `rest`. Each move preserves this order because only the extreme value of a region crosses. A tie that goes to `rest` is safe, since equal values are interchangeable for a rank.

**Complexity.**
- **Time** is O(log n) per addition and O(d log n) for a rank change of d, because each moved value costs one heap operation.
- **Space** is O(n), because the structure must keep every value to serve a rank that grows later. A fixed rank would allow O(k).

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class KthWithMovingK {
    /** Min-heap that holds the current top region: the k largest values seen. */
    private final PriorityQueue<Integer> top = new PriorityQueue<>();
    /** Max-heap that holds every other value, so a larger k can pull values back. */
    private final PriorityQueue<Integer> rest = new PriorityQueue<>(Comparator.reverseOrder());
    private int k;

    /**
     * Creates the tracker with a starting rank.
     * Time: O(1). Space: O(1).
     * Invariant: top holds the min(k, count) largest values, and every value in top is at least every value in rest.
     */
    KthWithMovingK(int k) {
        // A rank below one has no meaning, so the constructor rejects it.
        if (k < 1) throw new IllegalArgumentException("k must be at least 1");
        this.k = k;
    }

    /**
     * Appends one value to the stream.
     * Time: O(log n). Space: O(1) extra, and the value stays stored.
     */
    void add(int v) {
        if (top.size() < k) {
            // Fewer than k values exist, so rest is empty and the value joins the top region.
            top.add(v);
        } else if (v > top.peek()) {
            // The value beats the boundary: it enters top and the old boundary drops into rest.
            top.add(v);
            rest.add(top.poll());
        } else {
            // The value ties or loses against the boundary, so it belongs to rest.
            rest.add(v);
        }
    }

    /**
     * Changes the rank, moving |newK - oldK| values between the two heaps at most.
     * Time: O(d log n) for a change of d. Space: O(1).
     */
    void setRank(int newK) {
        if (newK < 1) throw new IllegalArgumentException("k must be at least 1");
        k = newK;
        // A smaller k pushes the smallest values of top down into rest.
        while (top.size() > k) rest.add(top.poll());
        // A larger k pulls the largest values of rest up into top.
        while (top.size() < k && !rest.isEmpty()) top.add(rest.poll());
    }

    /**
     * Returns the k-th largest value, or null when fewer than k values exist.
     * Time: O(1). Space: O(1).
     */
    Integer kth() {
        // The root of top is the smallest of the k largest, which is the k-th largest overall.
        return top.size() == k ? top.peek() : null;
    }

    private static Integer oracle(List<Integer> all, int k) {
        // The reference sorts a copy in descending order and indexes it.
        List<Integer> copy = new ArrayList<>(all);
        copy.sort(Collections.reverseOrder());
        return copy.size() >= k ? copy.get(k - 1) : null;
    }

    public static void main(String[] args) {
        // Example 1: the rank grows to 4 with three values, which gives no answer, and then shrinks to 1.
        KthWithMovingK t = new KthWithMovingK(2);
        t.add(6); t.add(11);
        if (t.kth() != 6) throw new AssertionError("example 1 first");
        t.add(8);
        if (t.kth() != 8) throw new AssertionError("example 1 second");
        t.setRank(4);
        if (t.kth() != null) throw new AssertionError("example 1 short");
        t.add(3);
        if (t.kth() != 3) throw new AssertionError("example 1 fourth");
        t.setRank(1);
        if (t.kth() != 11) throw new AssertionError("example 1 max");
        // Example 2: negative duplicates, then a rank beyond the count.
        KthWithMovingK u = new KthWithMovingK(3);
        if (u.kth() != null) throw new AssertionError("empty");
        u.add(-5); u.add(-5);
        if (u.kth() != null) throw new AssertionError("two of three");
        u.add(-9);
        if (u.kth() != -9) throw new AssertionError("third");
        u.setRank(2);
        if (u.kth() != -5) throw new AssertionError("second");
        u.setRank(5);
        if (u.kth() != null) throw new AssertionError("five");
        u.add(0); u.add(7);
        if (u.kth() != -9) throw new AssertionError("fifth");
        // A rank below one is rejected.
        try { new KthWithMovingK(0); throw new AssertionError("accepted zero"); } catch (IllegalArgumentException ok) { }
        // Random operation sequences are compared with the sorting reference after every step.
        Random rnd = new Random(3801L);
        for (int trial = 0; trial < 20000; trial++) {
            int k = 1 + rnd.nextInt(5);
            KthWithMovingK fast = new KthWithMovingK(k);
            List<Integer> all = new ArrayList<>();
            for (int step = 0; step < 25; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) { int v = rnd.nextInt(7) - 3; fast.add(v); all.add(v); }
                else if (op == 1) { k = 1 + rnd.nextInt(6); fast.setRank(k); }
                // Compare after every operation, including answers that are null.
                Integer got = fast.kth();
                Integer want = oracle(all, k);
                if (want == null ? got != null : !want.equals(got)) throw new AssertionError("trial " + trial + " step " + step);
            }
        }
    }
}
```

#### Solution: [Vary] Median Of The Last W Values (LeetCode 295)
<!-- id: st38o-window-median -->

**Approach.**
The stream expires, so the median covers only the newest `w` values. The structure keeps the two halves of the median finder: a max-heap `low` and a min-heap `high`, plus a queue of items in arrival order. When the window is full, the item at the front of the queue expires. Its heap entry is not searched for. The code marks the item dead and lowers the live count of its half. The dead entry waits in its heap until it reaches the root.

Every read of a root first discards dead roots. The invariant has two parts. The live values of `low` are at most the live values of `high`, and the live count of `low` exceeds that of `high` by zero or one. The routine repairs the halves after an expiry and before the new value is routed. Otherwise a half with no live value would misroute it. Dead items buried below live roots do not disturb the answer. They would grow the memory, so a rebuild from the live items runs when the heaps hold more than twice the window plus a constant. The query returns the root of `low`, which is the lower median.

**Complexity.**
- **Time** is O(log w) amortized per addition and per query. Each event moves a bounded number of items between heaps, and each item leaves a heap at most once. A rebuild costs O(w) and follows at least w additions.
- **Space** is O(w), since the rebuild keeps the stored items, live and dead together, within about twice the window.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class WindowMedian {
    /** One stream value. It sits in exactly one heap and is marked dead when it expires. */
    private static final class Item {
        final int value;
        boolean dead;
        boolean inLow;
        Item(int value) { this.value = value; }
    }

    private final int w;
    private final ArrayDeque<Item> window = new ArrayDeque<>();
    private final PriorityQueue<Item> low = new PriorityQueue<>((a, b) -> Integer.compare(b.value, a.value));
    private final PriorityQueue<Item> high = new PriorityQueue<>((a, b) -> Integer.compare(a.value, b.value));
    private int lowLive, highLive;

    /**
     * Creates a tracker for the last w values.
     * Time: O(1). Space: O(w) live items plus a bounded number of dead items.
     * Invariant: every live value in low is at most every live value in high, and lowLive - highLive is 0 or 1.
     */
    WindowMedian(int w) {
        if (w < 1) throw new IllegalArgumentException("window must hold at least one value");
        this.w = w;
    }

    /**
     * Appends a value and expires the oldest value when the window is full.
     * Time: O(log w) amortized. Space: O(1) extra.
     */
    void add(int x) {
        // The oldest value expires first, and the halves are repaired before the new value is routed.
        if (window.size() == w) { expire(window.pollFirst()); rebalance(); }
        Item item = new Item(x);
        window.addLast(item);
        // Route by the largest live value of the lower half.
        clean(low);
        if (low.isEmpty() || x <= low.peek().value) { item.inLow = true; low.add(item); lowLive++; }
        else { high.add(item); highLive++; }
        rebalance();
        compact();
    }

    /**
     * Returns the lower median of the live values: the smaller of the two middle values for an even count.
     * Time: O(log w) amortized. Space: O(1).
     */
    int median() {
        if (window.isEmpty()) throw new IllegalStateException("no values");
        // Dead roots are discarded first; after that the root of low is the lower median.
        clean(low);
        return low.peek().value;
    }

    private void expire(Item old) {
        // The item stays inside its heap; it only changes the live count of its side.
        old.dead = true;
        if (old.inLow) lowLive--; else highLive--;
    }

    private void clean(PriorityQueue<Item> heap) {
        // A dead root is stale and leaves the heap; each item leaves at most once.
        while (!heap.isEmpty() && heap.peek().dead) heap.poll();
    }

    private void rebalance() {
        // The lower half is too large: its live root moves up.
        while (lowLive > highLive + 1) {
            clean(low);
            Item m = low.poll();
            m.inLow = false; high.add(m);
            lowLive--; highLive++;
        }
        // The upper half is larger: its live root moves down.
        while (highLive > lowLive) {
            clean(high);
            Item m = high.poll();
            m.inLow = true; low.add(m);
            highLive--; lowLive++;
        }
    }

    private void compact() {
        // Dead items buried below live ones are removed when they outnumber the live items.
        if (low.size() + high.size() <= 2 * window.size() + 16) return;
        List<Item> keepLow = new ArrayList<>(), keepHigh = new ArrayList<>();
        for (Item i : low) if (!i.dead) keepLow.add(i);
        for (Item i : high) if (!i.dead) keepHigh.add(i);
        low.clear(); high.clear();
        low.addAll(keepLow); high.addAll(keepHigh);
    }

    int stored() { return low.size() + high.size(); }

    private static int oracle(List<Integer> win) {
        // Reference: sort the window and take the lower middle element.
        List<Integer> s = new ArrayList<>(win);
        Collections.sort(s);
        return s.get((s.size() - 1) / 2);
    }

    public static void main(String[] args) {
        // Example 1: window of 3; the median follows the last three values only.
        WindowMedian a = new WindowMedian(3);
        int[] in1 = {8, 1, 5, 9, 2, 2};
        int[] out1 = {8, 1, 5, 5, 5, 2};
        for (int i = 0; i < in1.length; i++) {
            a.add(in1[i]);
            if (a.median() != out1[i]) throw new AssertionError("example 1 at " + i);
        }
        // Example 2: window of 2 returns the smaller of two middle values; negative numbers work.
        WindowMedian b = new WindowMedian(2);
        int[] in2 = {-4, -4, 7, -1, -1, 0};
        int[] out2 = {-4, -4, -4, -1, -1, -1};
        for (int i = 0; i < in2.length; i++) {
            b.add(in2[i]);
            if (b.median() != out2[i]) throw new AssertionError("example 2 at " + i);
        }
        // An empty tracker and a zero window are rejected.
        try { new WindowMedian(3).median(); throw new AssertionError("empty"); } catch (IllegalStateException ok) { }
        try { new WindowMedian(0); throw new AssertionError("zero"); } catch (IllegalArgumentException ok) { }
        // A window of one always returns the newest value.
        WindowMedian one = new WindowMedian(1);
        for (int v : new int[] {3, -2, 9}) { one.add(v); if (one.median() != v) throw new AssertionError("window one"); }
        // Random streams are compared with the sorting reference after every add.
        Random rnd = new Random(3802L);
        for (int trial = 0; trial < 20000; trial++) {
            int w = 1 + rnd.nextInt(6);
            WindowMedian fast = new WindowMedian(w);
            List<Integer> win = new ArrayList<>();
            for (int step = 0; step < 30; step++) {
                int v = rnd.nextInt(7) - 3;
                fast.add(v);
                win.add(v);
                if (win.size() > w) win.remove(0);
                if (fast.median() != oracle(win)) throw new AssertionError("trial " + trial + " step " + step);
            }
        }
        // Memory stays proportional to the window even for a long increasing stream.
        WindowMedian longRun = new WindowMedian(4);
        for (int i = 0; i < 200000; i++) longRun.add(i);
        if (longRun.stored() > 2 * 4 + 16 + 2) throw new AssertionError("stored " + longRun.stored());
    }
}
```

#### Solution: [Boundary] Price Timeline With Deletions (LeetCode 2034)
<!-- id: st38o-timeline-deletions -->

**Approach.**
The stream is correctable. An ordered map from timestamp to price is the truth, and it also answers `current` through its last key, even after the latest record is removed. Two lazy heaps hold entries of price and timestamp, a max-heap and a min-heap. An update changes the truth and pushes one entry into each heap. A removal changes only the truth, because the entries of the removed record stay behind as stale entries.

A query for the maximum or the minimum discards roots whose timestamp is missing from the truth or holds a different price, and then returns the first root that agrees. An entry that repeats the same price is still valid, and a duplicate valid entry is harmless. The invariant is that every live record has at least one valid entry in each heap. The rebuild from the map runs when the heap holds more than twice the live count plus a constant, and it keeps memory proportional to the live records. The test also checks the queries on an empty timeline, which throw.

**Complexity.**
- **Time** is O(log n) amortized per operation, because each entry is polled at most once and a rebuild of O(n) follows at least n pushes or removals.
- **Space** is O(n) for the live records, plus a bounded number of stale entries because of the rebuild.

```java run
import java.util.PriorityQueue;
import java.util.Random;
import java.util.TreeMap;

public final class StockTimeline {
    /** Truth: the live price of each timestamp, ordered by timestamp. */
    private final TreeMap<Long, Long> prices = new TreeMap<>();
    /** Lazy max-heap of entries {price, timestamp}; an entry is live only when it equals the truth. */
    private final PriorityQueue<long[]> maxHeap = new PriorityQueue<>((a, b) -> Long.compare(b[0], a[0]));
    /** Lazy min-heap of entries {price, timestamp} with the same liveness rule. */
    private final PriorityQueue<long[]> minHeap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));

    /**
     * Sets the price at a timestamp, replacing any earlier price there.
     * Time: O(log n) amortized. Space: O(1) amortized, because rebuilds cap the heap size.
     * Invariant: every live price has at least one entry in each heap.
     */
    void update(long timestamp, long price) {
        prices.put(timestamp, price);
        // The old entries stay in the heaps; they now disagree with the truth and will be discarded later.
        maxHeap.add(new long[] {price, timestamp});
        minHeap.add(new long[] {price, timestamp});
        compact();
    }

    /**
     * Deletes the record at a timestamp. Returns true when a record existed.
     * Time: O(log n) amortized. Space: O(1).
     */
    boolean remove(long timestamp) {
        // Only the truth changes; the heaps keep entries that are now stale.
        boolean existed = prices.remove(timestamp) != null;
        compact();
        return existed;
    }

    /** Returns the price at the largest timestamp. Time: O(log n). Space: O(1). */
    long current() {
        if (prices.isEmpty()) throw new IllegalStateException("no records");
        // The ordered map gives the latest timestamp directly, even after the latest record was removed.
        return prices.lastEntry().getValue();
    }

    /** Returns the highest live price. Time: O(log n) amortized. Space: O(1). */
    long maximum() { return live(maxHeap); }

    /** Returns the lowest live price. Time: O(log n) amortized. Space: O(1). */
    long minimum() { return live(minHeap); }

    private long live(PriorityQueue<long[]> heap) {
        if (prices.isEmpty()) throw new IllegalStateException("no records");
        while (true) {
            long[] top = heap.peek();
            Long truth = prices.get(top[1]);
            // The root is live when the truth for its timestamp still holds the same price.
            if (truth != null && truth == top[0]) return top[0];
            // Otherwise the root is stale and leaves the heap; each entry leaves at most once.
            heap.poll();
        }
    }

    private void compact() {
        // When stale entries outnumber live ones, both heaps are rebuilt from the truth in O(n).
        if (maxHeap.size() > 2 * prices.size() + 16) {
            maxHeap.clear();
            minHeap.clear();
            for (var e : prices.entrySet()) {
                maxHeap.add(new long[] {e.getValue(), e.getKey()});
                minHeap.add(new long[] {e.getValue(), e.getKey()});
            }
        }
    }

    int heapSize() { return maxHeap.size(); }

    private static void same(StockTimeline fast, TreeMap<Long, Long> ref, String where) {
        // Compare every query with a direct scan of the reference map.
        if (ref.isEmpty()) {
            try { fast.maximum(); throw new AssertionError("empty max " + where); } catch (IllegalStateException ok) { }
            try { fast.current(); throw new AssertionError("empty current " + where); } catch (IllegalStateException ok) { }
            return;
        }
        long max = Long.MIN_VALUE, min = Long.MAX_VALUE;
        for (long p : ref.values()) { max = Math.max(max, p); min = Math.min(min, p); }
        if (fast.maximum() != max || fast.minimum() != min || fast.current() != ref.lastEntry().getValue()) {
            throw new AssertionError("mismatch " + where);
        }
    }

    public static void main(String[] args) {
        // Example 1: removing the latest record moves current back to the previous timestamp.
        StockTimeline s = new StockTimeline();
        s.update(10, 40); s.update(20, 25); s.update(15, 60);
        if (s.maximum() != 60 || s.minimum() != 25 || s.current() != 25) throw new AssertionError("example 1 a");
        if (!s.remove(20) || s.current() != 60) throw new AssertionError("example 1 b");
        if (s.remove(20)) throw new AssertionError("second removal");
        s.update(15, 5);
        if (s.maximum() != 40 || s.minimum() != 5) throw new AssertionError("example 1 c");
        if (!s.remove(15) || !s.remove(10)) throw new AssertionError("example 1 d");
        try { s.maximum(); throw new AssertionError("empty after removals"); } catch (IllegalStateException ok) { }
        // Example 2: duplicate prices, a repeated update, and a remove-then-reinsert at the same timestamp.
        StockTimeline t = new StockTimeline();
        try { t.current(); throw new AssertionError("empty"); } catch (IllegalStateException ok) { }
        t.update(7, 30); t.update(7, 30); t.update(3, 30);
        if (!t.remove(7) || t.current() != 30 || t.maximum() != 30) throw new AssertionError("example 2 a");
        if (!t.remove(3)) throw new AssertionError("example 2 b");
        try { t.minimum(); throw new AssertionError("empty min"); } catch (IllegalStateException ok) { }
        // Random operations are compared with a plain map after every step.
        Random rnd = new Random(3803L);
        for (int trial = 0; trial < 3000; trial++) {
            StockTimeline fast = new StockTimeline();
            TreeMap<Long, Long> ref = new TreeMap<>();
            for (int step = 0; step < 60; step++) {
                long ts = rnd.nextInt(8);
                int op = rnd.nextInt(3);
                if (op == 0) {
                    long p = rnd.nextInt(6);
                    fast.update(ts, p); ref.put(ts, p);
                } else if (op == 1) {
                    if (fast.remove(ts) != (ref.remove(ts) != null)) throw new AssertionError("remove result");
                }
                same(fast, ref, "trial " + trial + " step " + step);
            }
        }
        // The heap size stays proportional to the live count plus a constant, even after many corrections.
        StockTimeline many = new StockTimeline();
        for (int i = 0; i < 100000; i++) many.update(i % 5, i);
        many.maximum();
        if (many.heapSize() > 2 * 5 + 16 + 1) throw new AssertionError("heap grew to " + many.heapSize());
    }
}
```

#### Solution: [Recognize] Trimmed Mean With A Correction (LeetCode 1825)
<!-- id: st38o-amended-trimmed-mean -->

**Approach.**
The stream expires and is correctable at its newest value. The window keeps three ordered regions: `low` holds the `lo` smallest values, `high` holds the `hi` largest values, and `mid` holds the rest with a running sum. Each region is a count map with a size and a sum. A queue of the window values finds the value that expires and the newest value to correct.

Insertion routes a value by the two boundaries, the largest value of `low` and the smallest value of `high`. Removal takes a copy of the value from the first region that holds it, which is safe because equal copies are interchangeable. Both paths end in one repair that sets the targets to min(lo, n) and min(hi, n - low). The repair moves surplus extremes into `mid` first, and then refills a short side from `mid`. The invariant is that every value of `low` is at most every value of `mid`, and every value of `mid` is at most every value of `high`. The mean is the sum of `mid` divided by its size, and it is read only when `m` values exist.

**Complexity.**
- **Time** is O(log m) per addition, correction and query step, because each repair moves a constant number of values and each move is a map operation.
- **Space** is O(m) for the queue and the three count maps.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.TreeMap;

public final class TrimmedWindow {
    /** A multiset of ints with a running size and sum. */
    private static final class Region {
        final TreeMap<Integer, Integer> counts = new TreeMap<>();
        int size;
        long sum;
        void add(int v) { counts.merge(v, 1, Integer::sum); size++; sum += v; }
        void remove(int v) { counts.computeIfPresent(v, (key, c) -> c == 1 ? null : c - 1); size--; sum -= v; }
        boolean has(int v) { return counts.containsKey(v); }
        int min() { return counts.firstKey(); }
        int max() { return counts.lastKey(); }
    }

    private final int m, lo, hi;
    private final ArrayDeque<Integer> window = new ArrayDeque<>();
    private final Region low = new Region(), mid = new Region(), high = new Region();

    /**
     * Creates a window of m values that trims the lo smallest and hi largest values.
     * Time: O(1). Space: O(m).
     * Invariant: every value in low is at most every value in mid, every value in mid is at most every value in high,
     * low holds min(lo, n) values, and high holds min(hi, n - low) values for n stored values.
     */
    TrimmedWindow(int m, int lo, int hi) {
        // The middle region must stay non-empty once the window is full.
        if (lo < 0 || hi < 0 || m <= lo + hi) throw new IllegalArgumentException("need m > lo + hi");
        this.m = m; this.lo = lo; this.hi = hi;
    }

    /**
     * Appends a value and expires the oldest one when the window is already full.
     * Time: O(log m). Space: O(1) extra.
     */
    void add(int x) {
        // The oldest value leaves the regions before the new one enters.
        if (window.size() == m) erase(window.pollFirst());
        window.addLast(x);
        insert(x);
    }

    /**
     * Replaces the newest value by a corrected one without moving the window.
     * Time: O(log m). Space: O(1).
     */
    void amendLast(int x) {
        if (window.isEmpty()) throw new IllegalStateException("no value to amend");
        // The wrong value is removed from its region and the corrected value is routed again.
        erase(window.pollLast());
        window.addLast(x);
        insert(x);
    }

    /**
     * Returns the floor of the mean of the middle values, or -1 while fewer than m values exist.
     * Time: O(1). Space: O(1).
     */
    long average() {
        if (window.size() < m) return -1;
        // The sum is a long, and Java division of non-negative values is the floor.
        return mid.sum / mid.size;
    }

    private void insert(int x) {
        // Route by the nearest boundary: the largest of low, then the smallest of high, else the middle.
        if (low.size > 0 && x <= low.max()) low.add(x);
        else if (high.size > 0 && x >= high.min()) high.add(x);
        else mid.add(x);
        rebalance();
    }

    private void erase(int v) {
        // Equal copies are interchangeable, so the first region that holds the value gives it up.
        if (low.has(v)) low.remove(v);
        else if (mid.has(v)) mid.remove(v);
        else high.remove(v);
        rebalance();
    }

    private void move(Region from, Region to, boolean takeMax) {
        // One extreme value crosses a region border, so the ordering between regions stays intact.
        int v = takeMax ? from.max() : from.min();
        from.remove(v);
        to.add(v);
    }

    private void rebalance() {
        int n = window.size();
        int wantLow = Math.min(lo, n);
        int wantHigh = Math.min(hi, n - wantLow);
        // Overflow first: surplus values of low and high move into the middle.
        while (low.size > wantLow) move(low, mid, true);
        while (high.size > wantHigh) move(high, mid, false);
        // Then underflow: the middle gives its extremes to the sides that are short.
        while (low.size < wantLow) move(mid, low, false);
        while (high.size < wantHigh) move(mid, high, true);
    }

    private static long oracle(List<Integer> w, int m, int lo, int hi) {
        // Reference: sort the window, cut both ends and average the rest.
        if (w.size() < m) return -1;
        List<Integer> s = new ArrayList<>(w);
        Collections.sort(s);
        long sum = 0;
        for (int i = lo; i < m - hi; i++) sum += s.get(i);
        return sum / (m - lo - hi);
    }

    public static void main(String[] args) {
        // Example 1: trim only the smallest value; a correction changes the newest value.
        TrimmedWindow a = new TrimmedWindow(4, 1, 0);
        a.add(9); a.add(2); a.add(6);
        if (a.average() != -1) throw new AssertionError("example 1 short");
        a.add(4);
        if (a.average() != 6) throw new AssertionError("example 1 first");
        a.add(20);
        if (a.average() != 10) throw new AssertionError("example 1 second");
        a.amendLast(1);
        if (a.average() != 4) throw new AssertionError("example 1 amended");
        // Example 2: duplicates at both cuts, then a correction with a large value.
        TrimmedWindow b = new TrimmedWindow(5, 2, 1);
        b.add(0); b.add(0); b.add(7); b.add(7); b.add(3);
        if (b.average() != 5) throw new AssertionError("example 2 first");
        b.amendLast(100);
        if (b.average() != 7) throw new AssertionError("example 2 second");
        b.add(1);
        if (b.average() != 7) throw new AssertionError("example 2 third");
        b.add(20);
        if (b.average() != 13) throw new AssertionError("example 2 fourth");
        // The constructor rejects a window that leaves no middle value, and amend needs a value.
        try { new TrimmedWindow(3, 1, 2); throw new AssertionError("accepted"); } catch (IllegalArgumentException ok) { }
        try { new TrimmedWindow(3, 1, 1).amendLast(1); throw new AssertionError("amend empty"); } catch (IllegalStateException ok) { }
        // Large values keep the sum exact in long arithmetic.
        TrimmedWindow c = new TrimmedWindow(3, 0, 0);
        c.add(1_000_000_000); c.add(1_000_000_000); c.add(1_000_000_000);
        if (c.average() != 1_000_000_000L) throw new AssertionError("long sum");
        // Random operation sequences, including corrections, are compared with the sorting reference.
        Random rnd = new Random(3804L);
        for (int trial = 0; trial < 20000; trial++) {
            int m = 1 + rnd.nextInt(6);
            int lo = rnd.nextInt(m);
            int hi = rnd.nextInt(m - lo);
            TrimmedWindow fast = new TrimmedWindow(m, lo, hi);
            List<Integer> w = new ArrayList<>();
            for (int step = 0; step < 30; step++) {
                int v = rnd.nextInt(6);
                if (rnd.nextInt(4) == 0 && !w.isEmpty()) { fast.amendLast(v); w.set(w.size() - 1, v); }
                else { fast.add(v); w.add(v); if (w.size() > m) w.remove(0); }
                if (fast.average() != oracle(w, m, lo, hi)) throw new AssertionError("trial " + trial + " step " + step);
            }
        }
    }
}
```
