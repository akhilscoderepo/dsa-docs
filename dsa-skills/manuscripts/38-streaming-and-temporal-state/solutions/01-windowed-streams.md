<!-- solutions-for: 01-windowed-streams -->
### Solutions For Windowed Streams

#### Solution: [Build] Rolling Average Of Readings (LeetCode 346)
<!-- id: st38-moving-average -->

**Approach.**
The class keeps a queue of at most `size` values and a `long` total of the values in the queue. A new value enters at the back and adds to the total. When the queue then holds more than `size` values, exactly one value leaves from the front and the total drops by it. The invariant is that the total equals the sum of the queued values and the queue length is at most `size`. The result divides the total by the queue length, which is at least 1 after an insertion.

The program compares each answer with a direct re-sum of the last `size` values on random streams, including a size of 1 and negative values.

**Complexity.**
- **Time** is O(1) per call, because one insertion and at most one removal change the total.
- **Space** is O(size), because the queue never holds more than `size` values.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class MovingAverageBuild {
    static final class MovingAverage {
        private final int size;
        private final ArrayDeque<Integer> window = new ArrayDeque<>();
        private long total;

        MovingAverage(int size) {
            // The bound is stored once; it never changes.
            this.size = size;
        }

        /**
         * Appends a value and returns the mean of the last size values.
         * Time: O(1). Space: O(size) for the whole object.
         * Invariant: total equals the sum of window, and window.size() <= size.
         */
        double next(int val) {
            // The value enters at the back of the queue.
            window.addLast(val);
            // The total changes by this one value.
            total += val;
            // At most one value is over the bound, and it is the oldest.
            if (window.size() > size) total -= window.pollFirst();
            // The queue holds at least one value, so the division is defined.
            return (double) total / window.size();
        }
    }

    public static void main(String[] args) {
        // Example 1: the window of 3 drops the first value at the fourth call.
        MovingAverage a = new MovingAverage(3);
        double[] want1 = {5.0, 6.5, 5.0, 7.0};
        int[] in1 = {5, 8, 2, 11};
        for (int i = 0; i < in1.length; i++)
            if (a.next(in1[i]) != want1[i]) throw new AssertionError("example 1 at " + i);
        // Example 2: a size of 1 returns each value itself.
        MovingAverage b = new MovingAverage(1);
        if (b.next(4) != 4.0 || b.next(-2) != -2.0 || b.next(0) != 0.0) throw new AssertionError("example 2");
        // Large values must not overflow the total: 10^4 values of 10^5 fit a long.
        MovingAverage big = new MovingAverage(10000);
        double last = 0;
        for (int i = 0; i < 10000; i++) last = big.next(100000);
        if (last != 100000.0) throw new AssertionError("large sum");
        // Random streams compare with a direct re-sum of the tail.
        Random rnd = new Random(3801L);
        for (int t = 0; t < 2000; t++) {
            int size = 1 + rnd.nextInt(6);
            MovingAverage real = new MovingAverage(size);
            List<Integer> all = new ArrayList<>();
            for (int step = rnd.nextInt(20); step > 0; step--) {
                int v = rnd.nextInt(2001) - 1000;
                all.add(v);
                long sum = 0;
                int from = Math.max(0, all.size() - size);
                for (int i = from; i < all.size(); i++) sum += all.get(i);
                double expected = (double) sum / (all.size() - from);
                if (real.next(v) != expected) throw new AssertionError("random stream");
            }
        }
    }
}
```

#### Solution: [Vary] Recent Pings Within A Span (LeetCode 933)
<!-- id: st38-recent-calls -->

**Approach.**
The counter stores the timestamps that can still count in a queue, oldest first. A ping appends its time. The inclusive range `t - span <= u <= t` means that a timestamp is expired exactly when `u < t - span`, so a loop removes front entries while that holds. The loop stops at the first live entry, because timestamps never decrease and every later entry is at least as new. The queue size is the answer. Equal timestamps are separate entries, so two pings at time 2 return 1 and then 2.

The invariant is that after each call the queue holds exactly the pings inside the range ending at the latest time. The program compares with a scan of the full history on random non-decreasing times, including a span of 0.

**Complexity.**
- **Time** averages O(1) per call over the stream, since each timestamp is appended once and removed at most once.
- **Space** is O(m), where `m` is the largest number of pings that fit in one range, because older pings are removed.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RecentCounterVary {
    static final class RecentCounter {
        private final int span;
        private final ArrayDeque<Integer> window = new ArrayDeque<>();

        RecentCounter(int span) {
            // The span is part of the contract, so it is a constructor argument.
            this.span = span;
        }

        /**
         * Records a ping and counts the pings in [t - span, t].
         * Time: O(1) amortized. Space: O(m) for the live pings.
         * Invariant: the queue holds exactly the pings with t - span <= u <= t.
         */
        int ping(int t) {
            // The new ping is the newest entry.
            window.addLast(t);
            // An entry is expired when it is strictly older than the lower end; the loop stops at the first live one.
            while (window.peekFirst() < t - span) window.pollFirst();
            // The size of the queue is the number of live pings.
            return window.size();
        }
    }

    public static void main(String[] args) {
        // Example 1: span 4 with a repeated time at 5.
        RecentCounter a = new RecentCounter(4);
        int[] in1 = {1, 3, 5, 5, 9, 10};
        int[] want1 = {1, 2, 3, 4, 3, 2};
        for (int i = 0; i < in1.length; i++)
            if (a.ping(in1[i]) != want1[i]) throw new AssertionError("example 1 at " + i);
        // Example 2: span 0 counts only pings at the same time.
        RecentCounter b = new RecentCounter(0);
        if (b.ping(2) != 1 || b.ping(2) != 2 || b.ping(3) != 1) throw new AssertionError("example 2");
        // The lowest end is inclusive: a ping exactly span old still counts.
        RecentCounter c = new RecentCounter(3);
        if (c.ping(0) != 1 || c.ping(3) != 2 || c.ping(4) != 2) throw new AssertionError("inclusive end");
        // Random non-decreasing times compare with a scan of the whole history.
        Random rnd = new Random(3802L);
        for (int t = 0; t < 3000; t++) {
            int span = rnd.nextInt(8);
            RecentCounter real = new RecentCounter(span);
            List<Integer> all = new ArrayList<>();
            int now = rnd.nextInt(3);
            for (int step = rnd.nextInt(25); step > 0; step--) {
                now += rnd.nextInt(4);
                all.add(now);
                int expected = 0;
                for (int u : all) if (now - span <= u && u <= now) expected++;
                if (real.ping(now) != expected) throw new AssertionError("random times");
            }
        }
    }
}
```

#### Solution: [Boundary] Large Sum Window (Author exercise)
<!-- id: st38-large-sum-window -->

**Approach.**
The class stores each recorded event as a pair of a time and a value in two parallel `long` queues, and keeps a `long` total of the values in the queue. A recorded event enters at the back and adds to the total. A query first computes the cutoff `now - span`. Both arguments are at least 0 and at most 4 * 10^18, so the difference lies between -4 * 10^18 and 4 * 10^18 and cannot overflow. The sum `time + span` could reach 8 * 10^18 in the worst case, which is why the code never forms it. The query removes front events with `time < cutoff` and subtracts their values, then returns the total.

The invariant is that after a query at `now` the queue holds exactly the events with `now - span <= time <= now`. A query also expires events, which is correct because no later call has a smaller time. The program checks both examples and compares with a scan on random streams, including a huge span.

**Complexity.**
- **Time** averages O(1) per call over the stream, since each event enters once and leaves at most once.
- **Space** is O(m), where `m` is the largest number of events inside one range, because expired events are removed.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class LargeSumWindowBoundary {
    static final class TimedSum {
        private final long span;
        private final ArrayDeque<Long> times = new ArrayDeque<>();
        private final ArrayDeque<Long> values = new ArrayDeque<>();
        private long total;

        TimedSum(long span) {
            // The span is a long, because it can exceed the int range.
            this.span = span;
        }

        /**
         * Stores an event.
         * Time: O(1). Space: O(1) per live event.
         * Invariant: total equals the sum of values in the queue.
         */
        void record(long time, long value) {
            // The event enters at the newest end.
            times.addLast(time);
            values.addLast(value);
            // The total changes by this value only.
            total += value;
        }

        /**
         * Returns the sum of values with now - span <= time <= now.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: afterwards the queue holds exactly the events in the range.
         */
        long total(long now) {
            // Subtraction of two non-negative longs below 4e18 cannot overflow, unlike time + span.
            long cutoff = now - span;
            // Events strictly older than the cutoff expire; the loop stops at the first live event.
            while (!times.isEmpty() && times.peekFirst() < cutoff) {
                times.pollFirst();
                total -= values.pollFirst();
            }
            // The remaining total belongs to the live events.
            return total;
        }
    }

    public static void main(String[] args) {
        // Example 1: both ends count, so time 5 is still live at now 15 and gone at now 16.
        TimedSum a = new TimedSum(10);
        a.record(5, 100);
        a.record(15, -30);
        if (a.total(15) != 70 || a.total(16) != -30) throw new AssertionError("example 1");
        // Example 2: timestamps near the long limit with a span of 4e18.
        long big = 4_000_000_000_000_000_000L;
        TimedSum b = new TimedSum(big);
        b.record(0, 5_000_000_000_000L);
        b.record(big, 5_000_000_000_000L);
        if (b.total(big) != 10_000_000_000_000L || b.total(big + 1) != 5_000_000_000_000L)
            throw new AssertionError("example 2");
        // A sum of 10^5 events of 10^12 is 10^17, which fits a long but not an int.
        TimedSum c = new TimedSum(big);
        for (int i = 0; i < 100000; i++) c.record(i, 1_000_000_000_000L);
        if (c.total(99999) != 100_000_000_000_000_000L) throw new AssertionError("long sum");
        // A query alone expires events, and a zero value is an ordinary event.
        TimedSum d = new TimedSum(2);
        d.record(1, 0);
        d.record(1, 7);
        if (d.total(3) != 7 || d.total(4) != 0) throw new AssertionError("query expiry");
        // Random streams compare with a scan of the whole history.
        Random rnd = new Random(3803L);
        for (int t = 0; t < 3000; t++) {
            long span = rnd.nextInt(8);
            TimedSum real = new TimedSum(span);
            List<long[]> all = new ArrayList<>();
            long now = rnd.nextInt(3);
            for (int step = rnd.nextInt(25); step > 0; step--) {
                now += rnd.nextInt(4);
                if (rnd.nextBoolean()) {
                    long v = rnd.nextInt(21) - 10;
                    all.add(new long[]{now, v});
                    real.record(now, v);
                } else {
                    long expected = 0;
                    for (long[] e : all) if (now - span <= e[0] && e[0] <= now) expected += e[1];
                    if (real.total(now) != expected) throw new AssertionError("random stream");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Hit Counter With Two Designs (LeetCode 362)
<!-- id: st38-hit-counter -->

**Approach.**
The queue design stores pairs of a second and a count of hits in that second, oldest first. A hit at the same second as the newest pair adds 1 to its count, and a hit at a later second appends a pair. The counter also keeps a `long` total of all counts in the queue. A query at `t` removes front pairs with `second <= t - span`, subtracts their counts and returns the total. Merging hits per second keeps the queue length at most `span`, even when 10^5 hits share one second.

The slot design keeps two arrays of length `span`. A hit at second `t` uses slot `t % span`. If the slot's stored second differs from `t`, the slot holds hits from an older second, so the code overwrites the tag with `t` and resets the count to 1. Otherwise it adds 1. A query at `t` sums the counts of slots whose tag satisfies `t - span < tag <= t`. The tag check is the invariant that makes stale slots harmless, because a slot is never cleared by a timer.

The queue costs memory in proportion to the distinct live seconds, and its query is O(1) amortized. The slots cost fixed memory in proportion to `span`, and each query reads all `span` slots. The program runs both designs against a scan of the full history on random streams, and requires equal answers from all three.

**Complexity.**
- **Time** is O(1) amortized per call for the queue design, and O(1) per hit and O(span) per count for the slot design.
- **Space** is O(min(span, live seconds)) for the queue design and O(span) for the slot design.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class HitCounterRecognize {
    /** Queue design: one pair per distinct second. */
    static final class QueueCounter {
        private final int span;
        private final ArrayDeque<int[]> window = new ArrayDeque<>();
        private long total;

        QueueCounter(int span) { this.span = span; }

        /**
         * Records one hit.
         * Time: O(1). Space: O(1) amortized.
         * Invariant: total equals the sum of counts in the queue.
         */
        void hit(int t) {
            // Hits in the newest second merge into one pair.
            if (!window.isEmpty() && window.peekLast()[0] == t) window.peekLast()[1]++;
            // A later second starts a new pair with count 1.
            else window.addLast(new int[]{t, 1});
            // The total counts the new hit.
            total++;
        }

        /**
         * Counts hits with t - span < u <= t.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: afterwards the queue holds only seconds above t - span.
         */
        int count(int t) {
            // A second at or below the cutoff has expired; the loop stops at the first live pair.
            while (!window.isEmpty() && window.peekFirst()[0] <= t - span) total -= window.pollFirst()[1];
            // The total now belongs to the live pairs.
            return (int) total;
        }
    }

    /** Slot design: a fixed array indexed by the second modulo span. */
    static final class SlotCounter {
        private final int span;
        private final int[] tag;
        private final int[] hits;

        SlotCounter(int span) {
            this.span = span;
            // Each slot starts with tag 0, which no hit can use because times start at 1.
            this.tag = new int[span];
            this.hits = new int[span];
        }

        /**
         * Records one hit.
         * Time: O(1). Space: O(span) for the object.
         * Invariant: a slot's count belongs to the second in its tag.
         */
        void hit(int t) {
            int i = t % span;
            // A different tag means the slot holds an older second, so the old count is discarded.
            if (tag[i] != t) { tag[i] = t; hits[i] = 0; }
            // The hit adds to the slot of its own second.
            hits[i]++;
        }

        /**
         * Counts hits with t - span < u <= t.
         * Time: O(span). Space: O(1).
         * Invariant: only slots whose tag lies in the range contribute.
         */
        int count(int t) {
            int sum = 0;
            // Every slot is checked, because slots hold no clock of their own.
            for (int i = 0; i < span; i++)
                if (t - span < tag[i] && tag[i] <= t) sum += hits[i];
            return sum;
        }
    }

    public static void main(String[] args) {
        // Example 1: span 5, and the hits at second 2 expire at second 7.
        int[] ops1 = {0, 0, 0, 1, 0, 1, 1, 1};
        int[] arg1 = {1, 2, 2, 4, 7, 7, 11, 12};
        int[] want1 = {-1, -1, -1, 3, -1, 1, 1, 0};
        // Example 2: span 3, and the hit at second 4 expires at second 7.
        int[] ops2 = {0, 1, 1, 1, 0, 0, 1, 1};
        int[] arg2 = {4, 4, 6, 7, 7, 7, 9, 10};
        int[] want2 = {-1, 1, 1, 0, -1, -1, 2, 0};
        run(5, ops1, arg1, want1);
        run(3, ops2, arg2, want2);
        // Many hits in one second merge into one pair and still count exactly.
        QueueCounter q = new QueueCounter(2);
        SlotCounter s = new SlotCounter(2);
        for (int i = 0; i < 100000; i++) { q.hit(9); s.hit(9); }
        if (q.count(9) != 100000 || s.count(9) != 100000 || q.count(10) != 100000 || q.count(11) != 0 || s.count(11) != 0)
            throw new AssertionError("many hits in one second");
        // Random non-decreasing streams compare both designs with a scan.
        Random rnd = new Random(3804L);
        for (int t = 0; t < 3000; t++) {
            int span = 1 + rnd.nextInt(6);
            QueueCounter rq = new QueueCounter(span);
            SlotCounter rs = new SlotCounter(span);
            List<Integer> all = new ArrayList<>();
            int now = 1 + rnd.nextInt(3);
            for (int step = rnd.nextInt(30); step > 0; step--) {
                now += rnd.nextInt(4);
                if (rnd.nextBoolean()) {
                    all.add(now); rq.hit(now); rs.hit(now);
                } else {
                    int expected = 0;
                    for (int u : all) if (now - span < u && u <= now) expected++;
                    if (rq.count(now) != expected || rs.count(now) != expected) throw new AssertionError("random stream");
                }
            }
        }
    }

    /** Replays one call list on both designs; op 0 is hit, op 1 is count, and want -1 marks a hit. */
    static void run(int span, int[] ops, int[] args, int[] want) {
        QueueCounter q = new QueueCounter(span);
        SlotCounter s = new SlotCounter(span);
        for (int i = 0; i < ops.length; i++) {
            if (ops[i] == 0) { q.hit(args[i]); s.hit(args[i]); }
            else if (q.count(args[i]) != want[i] || s.count(args[i]) != want[i]) throw new AssertionError("example call " + i);
        }
    }
}
```
