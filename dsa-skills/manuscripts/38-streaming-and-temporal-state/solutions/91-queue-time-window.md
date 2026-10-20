<!-- solutions-for: 91-queue-time-window -->
### Solutions For Queue Time Window

#### Solution: [Build] Smoothed Reading With Two Limits (LeetCode 346)
<!-- id: st38c-count-and-age-cap -->

**Approach.**
The window is the intersection of two bounds, so the queue needs two eviction conditions and the running sum needs one update rule. Each call first checks that the time did not move backward, then appends the new reading and adds its value to the `long` sum. The new reading has `time > time - span`, so the age test never removes it, and `maxCount >= 1` means the size test never removes it either. A loop then removes from the front while the queue holds more than `maxCount` readings or the oldest reading is at or before `time - span`, and each removal subtracts its value from the sum. The average is the sum divided by the queue size.

Invariant: the queue lists the readings among the latest `maxCount` with time above `time - span`, and the sum equals their values. Both bounds remove from the front only, because readings arrive in time order, so the oldest reading is always the first candidate for either rule. The oracle recomputes the window from the full history on each call and compares the result exactly, since the sum and the count are the same integers.

**Complexity.**
- **Time** is O(1) amortized per call, because each reading enters the queue once and leaves it once.
- **Space** is O(min(maxCount, readings inside the span)), the size of the queue at its peak.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class CappedAverageBuild {
    static final class CappedAverage {
        private final int maxCount;
        private final long span;
        private final ArrayDeque<long[]> window = new ArrayDeque<>(); // entries {time, value}, oldest first
        private long sum;                                             // long: 10^5 values of 10^9 overflow int
        private long last = Long.MIN_VALUE;                           // latest time seen

        CappedAverage(int maxCount, long span) {
            this.maxCount = maxCount;
            this.span = span;
        }

        /**
         * Records a reading and returns the average over the bounded window.
         * Time: O(1) amortized. Space: O(window size).
         * Invariant: window holds the latest maxCount readings with time greater than time - span.
         */
        double next(long time, int value) {
            // Time may repeat but may not decrease, or the front would not be the oldest reading.
            if (time < last) throw new IllegalArgumentException("time moved backward");
            last = time;
            // Append the new reading and add it to the sum in one step.
            window.addLast(new long[] {time, value});
            sum += value;
            long cutoff = time - span; // a reading with time <= cutoff is too old
            // Remove from the front while either bound is broken; the new reading is never removed.
            while (window.size() > maxCount || window.peekFirst()[0] <= cutoff) {
                // Each removal subtracts the reading's value from the sum.
                sum -= window.pollFirst()[1];
            }
            // Exact integer sum over a positive count.
            return (double) sum / window.size();
        }
    }

    /** Brute force: rescans the full history for the latest maxCount readings inside the span. */
    static double oracle(List<long[]> history, int maxCount, long span) {
        long time = history.get(history.size() - 1)[0];
        long sum = 0;
        int count = 0;
        // Only the latest maxCount history entries can qualify.
        for (int i = Math.max(0, history.size() - maxCount); i < history.size(); i++) {
            // The age rule keeps time greater than time - span.
            if (history.get(i)[0] > time - span) {
                sum += history.get(i)[1];
                count++;
            }
        }
        return (double) sum / count;
    }

    public static void main(String[] args) {
        // Example 1: both bounds act, the count bound at 5 and the age bound at 20 and 21.
        CappedAverage a = new CappedAverage(3, 10);
        long[][] r1 = {{1, 4}, {3, 8}, {5, 6}, {6, 10}, {20, 2}, {21, 7}};
        double[] e1 = {4.0, 6.0, 6.0, 8.0, 2.0, 4.5};
        for (int i = 0; i < r1.length; i++) {
            if (a.next(r1[i][0], (int) r1[i][1]) != e1[i]) throw new AssertionError("example 1 step " + i);
        }
        // Example 2: equal times, values near the int limit, and a sum above Integer.MAX_VALUE.
        CappedAverage b = new CappedAverage(2, 5);
        long[][] r2 = {{4, 1_000_000_000}, {4, 1_000_000_000}, {4, 7}, {9, 3}, {9, 5}};
        double[] e2 = {1_000_000_000.0, 1_000_000_000.0, 500_000_003.5, 3.0, 4.0};
        for (int i = 0; i < r2.length; i++) {
            if (b.next(r2[i][0], (int) r2[i][1]) != e2[i]) throw new AssertionError("example 2 step " + i);
        }
        // A backward time is rejected and the structure is unchanged.
        boolean threw = false;
        try { b.next(8, 1); } catch (IllegalArgumentException e) { threw = true; }
        if (!threw || b.next(9, 5) != 5.0) throw new AssertionError("backward time must leave the window unchanged");
        // Random streams against the oracle.
        Random rnd = new Random(38);
        for (int trial = 0; trial < 3000; trial++) {
            int maxCount = 1 + rnd.nextInt(6);
            long span = 1 + rnd.nextInt(12);
            CappedAverage c = new CappedAverage(maxCount, span);
            List<long[]> history = new ArrayList<>();
            long time = rnd.nextInt(5);
            for (int step = 0; step < 40; step++) {
                time += rnd.nextInt(4); // zero gaps give equal times
                int value = rnd.nextInt(3) == 0 ? 1_000_000_000 - rnd.nextInt(3) : rnd.nextInt(41) - 20; // some values near the int limit
                history.add(new long[] {time, value});
                if (c.next(time, value) != oracle(history, maxCount, span)) throw new AssertionError("trial " + trial);
            }
        }
    }
}
```

#### Solution: [Vary] Counts Over Several Window Lengths (LeetCode 933)
<!-- id: st38c-many-spans-one-queue -->

**Approach.**
The stored list is bounded by the largest span a caller may ask for, `maxSpan`, so eviction uses that fixed bound and never a query's span. Every call first moves the clock to `time` and advances a head index past the entries with `entry <= time - maxSpan`. These entries cannot belong to any permitted query again, because later calls have a time that is at least as large. The list between the head and the end is sorted, so a `count` call finds the first entry greater than `time - span` by binary search and returns the number of entries from that position to the end. Equal times occupy separate entries, and the search for "first greater" places the boundary after all of them when they sit exactly on the cutoff.

The invariant is that every entry at or after the head is inside the widest window, and the entries are in non-decreasing order, so the entries inside any narrower window form a suffix of the live part. Removing entries by moving a head index avoids shifting the list. The program compacts the list when the head passes half its length, which keeps memory proportional to the live entries.

**Complexity.**
- **Time** is O(log w) per `count` call for `w` live entries, and O(1) amortized for `record` and for eviction.
- **Space** is O(w), because compaction runs whenever dead entries outnumber live ones.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class MultiSpanCounterVary {
    static final class MultiSpanCounter {
        private final long maxSpan;
        private final ArrayList<Long> times = new ArrayList<>(); // non-decreasing event times
        private int head;                                         // first entry that can still be counted
        private long last = Long.MIN_VALUE;                       // latest time seen by any call

        MultiSpanCounter(long maxSpan) { this.maxSpan = maxSpan; }

        /**
         * Moves the clock to time and drops entries outside the widest window.
         * Time: O(1) amortized. Space: O(live entries) after compaction.
         * Invariant: every entry at or after head has a time greater than time - maxSpan.
         */
        private void advance(long time) {
            // A smaller time would break the sorted order that binary search relies on.
            if (time < last) throw new IllegalArgumentException("time moved backward");
            last = time;
            // Skip entries at or before the widest cutoff; no later query can count them.
            while (head < times.size() && times.get(head) <= time - maxSpan) head++;
            // Compact when dead entries are at least half the list, so memory tracks live entries.
            if (head * 2 > times.size()) {
                times.subList(0, head).clear();
                head = 0;
            }
        }

        /**
         * Records one event at the given time.
         * Time: O(1) amortized. Space: O(1) per event.
         * Invariant: the new entry is the largest, so the list stays sorted.
         */
        void record(long time) {
            advance(time);
            times.add(time);
        }

        /**
         * Counts events with a time greater than time - span.
         * Time: O(log w). Space: O(1).
         * Invariant: the counted events are exactly the suffix after the cutoff.
         */
        int count(long time, long span) {
            // A span above maxSpan would need entries that were already dropped.
            if (span < 1 || span > maxSpan) throw new IllegalArgumentException("span out of range");
            advance(time);
            long cutoff = time - span;
            int lo = head, hi = times.size(); // search the live part for the first entry > cutoff
            // Binary search: the loop keeps all entries before lo at or below the cutoff.
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (times.get(mid) <= cutoff) lo = mid + 1; else hi = mid;
            }
            // Everything from lo to the end lies inside the window.
            return times.size() - lo;
        }
    }

    /** Brute force: keeps every event and filters on each query. */
    static int oracle(List<Long> all, long time, long span) {
        int n = 0;
        // The window is half-open: a time equal to time - span is outside.
        for (long t : all) if (t > time - span) n++;
        return n;
    }

    public static void main(String[] args) {
        // Example 1: one stream, three different query spans, an event exactly on a cutoff.
        MultiSpanCounter a = new MultiSpanCounter(10);
        a.record(1); a.record(2); a.record(5); a.record(5);
        int[] got = new int[5];
        got[0] = a.count(6, 3);   // 5, 5 are inside (3, 6]
        got[1] = a.count(6, 10);  // 1, 2, 5, 5 are inside (-4, 6]
        a.record(9);
        got[2] = a.count(12, 4);  // only 9 is inside (8, 12]
        got[3] = a.count(12, 10); // 5, 5, 9 are inside (2, 12]; the event at 2 is on the cutoff
        got[4] = a.count(20, 10); // everything is at or before 10
        int[] e1 = {2, 4, 1, 3, 0};
        for (int i = 0; i < 5; i++) if (got[i] != e1[i]) throw new AssertionError("example 1 query " + i);
        // Example 2: an empty counter, then equal times, then a span of 1.
        MultiSpanCounter b = new MultiSpanCounter(4);
        if (b.count(3, 4) != 0) throw new AssertionError("empty");
        b.record(3); b.record(3);
        if (b.count(3, 1) != 2 || b.count(7, 4) != 0 || b.count(7, 1) != 0) throw new AssertionError("example 2");
        // Out-of-range span and backward time are rejected.
        boolean s = false, t = false;
        try { b.count(8, 5); } catch (IllegalArgumentException e) { s = true; }
        try { b.record(2); } catch (IllegalArgumentException e) { t = true; }
        if (!s || !t) throw new AssertionError("argument checks");
        // Random operation mixes against the oracle.
        Random rnd = new Random(933);
        for (int trial = 0; trial < 3000; trial++) {
            long maxSpan = 1 + rnd.nextInt(15);
            MultiSpanCounter c = new MultiSpanCounter(maxSpan);
            List<Long> all = new ArrayList<>();
            long time = rnd.nextInt(4);
            for (int step = 0; step < 60; step++) {
                time += rnd.nextInt(4); // zero gaps give equal times
                if (rnd.nextBoolean()) {
                    c.record(time);
                    all.add(time);
                } else {
                    long span = 1 + rnd.nextInt((int) maxSpan);
                    if (c.count(time, span) != oracle(all, time, span)) throw new AssertionError("trial " + trial);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Correct The Newest Reading (LeetCode 362)
<!-- id: st38c-amend-latest-entry -->

**Approach.**
The stream is correctable at its newest entry only, so the queue of entries stays in time order and the correction touches the last element. The meter keeps a queue of `{time, bytes}` entries, a `long` total, and `seen`, the latest time given to `add` or `total`. Every call that carries a time first checks that it does not go backward, sets `seen` and removes from the front the entries with `time <= seen - span`, which is the half-open rule: an entry exactly `span` old is outside. An `add` then appends and increases the total.

The method `amend` needs no time argument. The newest entry is the last element of the queue, and front eviction removes it only after every older entry. If the queue is empty, the newest entry has expired, or nothing was added, and `amend` throws `IllegalStateException`. Otherwise the method replaces the stored bytes and changes the total by the difference between new and old. The invariant is that the total equals the bytes of the queue, and the queue equals the entries inside the window at `seen`. Because `amend` does not move the clock, an entry that `total` has already evicted cannot come back.

**Complexity.**
- **Time** is O(1) amortized for `add`, `total` and `amend`, since each entry is added and removed once and a correction touches one element.
- **Space** is O(entries inside the window).

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class AmendableMeterBoundary {
    static final class AmendableMeter {
        private final long span;
        private final ArrayDeque<long[]> queue = new ArrayDeque<>(); // entries {time, bytes}, oldest first
        private long sum;                                            // bytes inside the window, as long
        private long seen = Long.MIN_VALUE;                          // latest time given to add or total

        AmendableMeter(long span) { this.span = span; }

        /**
         * Moves the clock and evicts entries at or before seen - span.
         * Time: O(1) amortized. Space: O(window).
         * Invariant: the queue holds exactly the entries inside (seen - span, seen].
         */
        private void advance(long time) {
            // Time repeats are fine; a decrease would make the front stop being the oldest entry.
            if (time < seen) throw new IllegalArgumentException("time moved backward");
            seen = time;
            // Half-open window: an entry exactly span old is outside.
            while (!queue.isEmpty() && queue.peekFirst()[0] <= time - span) sum -= queue.pollFirst()[1];
        }

        /**
         * Adds an entry at the given time.
         * Time: O(1) amortized. Space: O(1) per entry.
         * Invariant: the new entry is the newest and sits at the back.
         */
        void add(long time, long bytes) {
            advance(time);
            queue.addLast(new long[] {time, bytes});
            sum += bytes;
        }

        /**
         * Returns the bytes inside the window that ends at the given time.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: the returned value equals the sum over the queue.
         */
        long total(long time) {
            advance(time);
            return sum;
        }

        /**
         * Replaces the bytes of the newest entry.
         * Time: O(1). Space: O(1).
         * Invariant: sum changes by exactly the difference, and the clock does not move.
         */
        void amend(long bytes) {
            // An empty queue means no entry was added, or the newest one already left the window.
            if (queue.isEmpty()) throw new IllegalStateException("newest entry is not live");
            long[] newest = queue.peekLast(); // the newest entry is always the last one
            sum += bytes - newest[1];
            newest[1] = bytes;
        }
    }

    /** Brute force: keeps every entry and the latest seen time, and filters on demand. */
    static final class Oracle {
        final long span;
        final List<long[]> all = new ArrayList<>();
        long seen = Long.MIN_VALUE;
        Oracle(long span) { this.span = span; }
        void add(long t, long b) { seen = t; all.add(new long[] {t, b}); }
        long total(long t) {
            seen = t;
            long s = 0;
            for (long[] e : all) if (e[0] > t - span) s += e[1];
            return s;
        }
        boolean amend(long b) {
            // Live means the newest entry is inside the window at the latest seen time.
            if (all.isEmpty() || all.get(all.size() - 1)[0] <= seen - span) return false;
            all.get(all.size() - 1)[1] = b;
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1: a correction while live, one after the entry expired through total.
        AmendableMeter m = new AmendableMeter(5);
        boolean first = false;
        try { m.amend(1); } catch (IllegalStateException e) { first = true; }
        m.add(3, 10);
        if (!first || m.total(7) != 10) throw new AssertionError("example 1 start");
        m.amend(4);
        if (m.total(8) != 0) throw new AssertionError("exactly span old is outside");
        boolean second = false;
        try { m.amend(9); } catch (IllegalStateException e) { second = true; }
        if (!second) throw new AssertionError("expired entry must not be amendable");
        m.add(8, 2); m.add(8, 0); m.amend(5);
        if (m.total(8) != 7) throw new AssertionError("equal times, newest only");
        // Example 2: corrections move the total, and the final amend sees an evicted entry.
        AmendableMeter n = new AmendableMeter(10);
        n.add(2, 50); n.add(6, 30);
        if (n.total(8) != 80) throw new AssertionError("before amend");
        n.amend(45);
        if (n.total(8) != 95 || n.total(12) != 45) throw new AssertionError("after amend and eviction");
        n.amend(99);
        if (n.total(16) != 0) throw new AssertionError("window empties");
        boolean third = false;
        try { n.amend(1); } catch (IllegalStateException e) { third = true; }
        if (!third) throw new AssertionError("third");
        // Large values stay exact in long.
        AmendableMeter big = new AmendableMeter(100);
        for (int i = 0; i < 5; i++) big.add(i, 1_000_000_000_000L);
        if (big.total(4) != 5_000_000_000_000L) throw new AssertionError("long total");
        // Random operation mixes against the oracle.
        Random rnd = new Random(362);
        for (int trial = 0; trial < 3000; trial++) {
            long span = 1 + rnd.nextInt(8);
            AmendableMeter a = new AmendableMeter(span);
            Oracle o = new Oracle(span);
            long time = rnd.nextInt(3);
            for (int step = 0; step < 50; step++) {
                int op = rnd.nextInt(3);
                time += rnd.nextInt(3);
                if (op == 0) {
                    long b = rnd.nextInt(1000);
                    a.add(time, b);
                    o.add(time, b);
                } else if (op == 1) {
                    if (a.total(time) != o.total(time)) throw new AssertionError("total, trial " + trial);
                } else {
                    long b = rnd.nextInt(1000);
                    boolean ok = true;
                    try { a.amend(b); } catch (IllegalStateException e) { ok = false; }
                    if (ok != o.amend(b)) throw new AssertionError("amend, trial " + trial);
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Sessions With Idle And Hard Expiry (LeetCode 1797)
<!-- id: st38c-idle-and-hard-expiry -->

**Approach.**
The two expiry rules sort the sessions differently, so one queue cannot serve both. The idle rule depends on the last touch, and the hard rule depends on the start. The store therefore keeps two insertion-ordered maps over the same keys. The map `byTouch` holds each key's last touch and moves a key to the back on every renewal by removing and putting it again. The map `byStart` holds each key's start and never reorders. Both maps are sorted ascending by their value, because time never decreases.

Every call first sweeps. It removes keys from the front of `byTouch` while `time - touch >= idle`, and from the front of `byStart` while `time - start >= maxLife`. Each removal deletes the key from both maps, so a key that fails either rule disappears entirely. After the sweep, every remaining session satisfies both rules, because the front of each map holds its minimum value. `renew` then succeeds exactly when the key is present. `open` removes any old entry for the key and inserts a fresh session. The live count is the map size.

The invariant is that after a sweep, the two maps hold the same key set, which is exactly the set of live sessions, and each map is sorted by its own value.

**Complexity.**
- **Time** is O(1) amortized per call, because each session is inserted once per `open` and removed once, and a renewal is one removal and one insertion in a hash-based linked map.
- **Space** is O(live sessions) for each of the two maps.

```java run
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Random;

public final class SessionStoreRecognize {
    static final class SessionStore {
        private final long idle;
        private final long maxLife;
        private final LinkedHashMap<String, Long> byTouch = new LinkedHashMap<>(); // key to last touch, oldest touch first
        private final LinkedHashMap<String, Long> byStart = new LinkedHashMap<>(); // key to start, oldest start first
        private long last = Long.MIN_VALUE;                                         // latest time seen

        SessionStore(long idle, long maxLife) {
            this.idle = idle;
            this.maxLife = maxLife;
        }

        /**
         * Removes every session that fails the idle rule or the hard rule at the given time.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: afterward both maps hold the same keys, all of them live.
         */
        private void sweep(long time) {
            // Time never decreases, which keeps both maps sorted by their own value.
            if (time < last) throw new IllegalArgumentException("time moved backward");
            last = time;
            // Idle rule: the front of byTouch has the oldest touch, so stop at the first live one.
            for (Iterator<Map.Entry<String, Long>> it = byTouch.entrySet().iterator();
                 it.hasNext(); ) {
                Map.Entry<String, Long> e = it.next();
                if (time - e.getValue() < idle) break; // this and every later session passes the idle rule
                it.remove();                           // expired by idleness
                byStart.remove(e.getKey());            // keep the two maps on one key set
            }
            // Hard rule: the front of byStart has the oldest start.
            for (Iterator<Map.Entry<String, Long>> it = byStart.entrySet().iterator();
                 it.hasNext(); ) {
                Map.Entry<String, Long> e = it.next();
                if (time - e.getValue() < maxLife) break; // this and every later session passes the hard rule
                it.remove();                              // expired by age
                byTouch.remove(e.getKey());               // keep the two maps on one key set
            }
        }

        /**
         * Starts a session for key, replacing any earlier one.
         * Time: O(1) amortized. Space: O(1) per session.
         * Invariant: the new session sits at the back of both maps.
         */
        void open(String key, long time) {
            sweep(time);
            // Remove first, so a re-inserted key moves to the back instead of keeping its old place.
            byTouch.remove(key);
            byStart.remove(key);
            byTouch.put(key, time);
            byStart.put(key, time);
        }

        /**
         * Renews the session if it is live; returns whether it was.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: a renewal changes the touch order only, never the start order.
         */
        boolean renew(String key, long time) {
            sweep(time);
            // After the sweep, presence in byTouch means the session is live.
            if (!byTouch.containsKey(key)) return false;
            byTouch.remove(key);       // leave the old position
            byTouch.put(key, time);    // re-enter at the back with the new touch
            return true;
        }

        /**
         * Counts live sessions at the given time.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: the size equals the number of live sessions after the sweep.
         */
        int liveCount(long time) {
            sweep(time);
            return byTouch.size();
        }
    }

    /** Brute force: keeps every session and tests the two rules directly. */
    static final class Oracle {
        final long idle, maxLife;
        final Map<String, long[]> sessions = new HashMap<>(); // key to {start, touch}
        Oracle(long idle, long maxLife) { this.idle = idle; this.maxLife = maxLife; }
        boolean live(long[] s, long t) { return t - s[1] < idle && t - s[0] < maxLife; }
        void open(String k, long t) { sessions.put(k, new long[] {t, t}); }
        boolean renew(String k, long t) {
            long[] s = sessions.get(k);
            if (s == null || !live(s, t)) return false;
            s[1] = t;
            return true;
        }
        int count(long t) {
            int n = 0;
            for (long[] s : sessions.values()) if (live(s, t)) n++;
            return n;
        }
    }

    public static void main(String[] args) {
        // Example 1: the hard limit ends a session that keeps renewing within the idle limit.
        SessionStore a = new SessionStore(5, 12);
        a.open("a", 0); a.open("b", 2);
        boolean r1 = a.renew("a", 4);
        int c1 = a.liveCount(4);
        boolean r2 = a.renew("a", 8), r3 = a.renew("b", 8);
        int c2 = a.liveCount(8);
        boolean r4 = a.renew("a", 12);
        int c3 = a.liveCount(12);
        boolean r5 = a.renew("a", 12);
        if (!r1 || c1 != 2 || !r2 || r3 || c2 != 1 || r4 || c3 != 0 || r5) throw new AssertionError("example 1");
        // Example 2: both limits equal, and a replaced session starts a new life.
        SessionStore b = new SessionStore(3, 3);
        b.open("x", 1);
        boolean q1 = b.renew("x", 3);
        int d1 = b.liveCount(3);
        boolean q2 = b.renew("x", 4);
        b.open("x", 4);
        int d2 = b.liveCount(6), d3 = b.liveCount(7);
        if (!q1 || d1 != 1 || q2 || d2 != 1 || d3 != 0) throw new AssertionError("example 2");
        // Random operation mixes against the oracle, with few keys so renewals and replacements collide.
        Random rnd = new Random(1797);
        String[] keys = {"a", "b", "c", "d", "e"};
        for (int trial = 0; trial < 4000; trial++) {
            long idle = 1 + rnd.nextInt(6), maxLife = 1 + rnd.nextInt(12);
            SessionStore s = new SessionStore(idle, maxLife);
            Oracle o = new Oracle(idle, maxLife);
            long time = rnd.nextInt(3);
            for (int step = 0; step < 60; step++) {
                time += rnd.nextInt(3); // zero gaps give equal times
                String k = keys[rnd.nextInt(keys.length)];
                int op = rnd.nextInt(3);
                if (op == 0) {
                    s.open(k, time);
                    o.open(k, time);
                } else if (op == 1) {
                    if (s.renew(k, time) != o.renew(k, time)) throw new AssertionError("renew, trial " + trial);
                } else {
                    if (s.liveCount(time) != o.count(time)) throw new AssertionError("count, trial " + trial);
                }
            }
        }
    }
}
```
