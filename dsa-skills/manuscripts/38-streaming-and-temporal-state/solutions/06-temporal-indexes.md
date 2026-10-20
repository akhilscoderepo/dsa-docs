<!-- solutions-for: 06-temporal-indexes -->
### Solutions For Temporal Indexes

#### Solution: [Build] Log Storage System (LeetCode 635)
<!-- id: st38-log-storage-system -->

**Approach.**
The store keeps a `TreeMap` from the full timestamp text to the ids stored at that text. Because every field has a fixed width, the text order of two timestamps equals their time order, and `String.compareTo` compares the characters left to right. A retrieval first cuts the start and the end to the prefix length of the unit. It then pads each cut text back to full width. The start is padded with the lowest filler `0000:00:00:00:00:00` and the end with the highest filler `9999:99:99:99:99:99`. Every stored timestamp whose prefix equals the cut start is at least the padded start, and every one whose prefix equals the cut end is at most the padded end. A single `subMap` call with both ends included therefore returns exactly the logs whose cut texts lie between the cut query ends. The ids are collected and sorted.

The invariant is that the map holds each timestamp once, in text order, and that a padded end is never smaller than any real timestamp with the same prefix. The program compares the class with a direct scan that cuts every stored text on random data. It also asserts the claim behind the log viewer failure, that a date without a time sorts before a full timestamp of that date.

**Complexity.**
- **Time** for `store` is O(log n) for the map insert. A retrieval costs O(log n + r log r) for `r` returned ids, because one search finds the range view and a sort orders the ids.
- **Space** is O(n) for the map, plus O(r) for one answer.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class LogStorageBuild {
    static final class LogStore {
        private static final String LOW = "0000:00:00:00:00:00";    // lowest text of full width
        private static final String HIGH = "9999:99:99:99:99:99";   // highest text of full width
        private final TreeMap<String, List<Integer>> byTime = new TreeMap<>();

        /**
         * Maps a unit name to the length of its prefix.
         * Time: O(1). Space: O(1).
         * Invariant: the lengths 4, 7, 10, 13, 16 and 19 end right before a separator or at the end.
         */
        static int digits(String unit) {
            // Each case returns the number of characters that name the unit and everything above it.
            switch (unit) {
                case "Year": return 4;
                case "Month": return 7;
                case "Day": return 10;
                case "Hour": return 13;
                case "Minute": return 16;
                default: return 19;
            }
        }

        /**
         * Saves one log.
         * Time: O(log n). Space: O(1) extra.
         * Invariant: the map stays ordered by timestamp text.
         */
        void store(int id, String timestamp) {
            // One map insert places the id under its timestamp, and equal timestamps share a list.
            byTime.computeIfAbsent(timestamp, k -> new ArrayList<>()).add(id);
        }

        /**
         * Returns the ids whose timestamp, cut to the unit, lies between the cut ends, both included.
         * Time: O(log n + r log r). Space: O(r).
         * Invariant: the padded start is the lowest text with the cut start prefix, the padded end the highest.
         */
        List<Integer> retrieve(String start, String end, String unit) {
            int d = digits(unit);
            // Cut each end to the unit and pad it to full width, so both are valid map keys.
            String lo = start.substring(0, d) + LOW.substring(d);
            String hi = end.substring(0, d) + HIGH.substring(d);
            List<Integer> out = new ArrayList<>();
            // The range view visits only the stored timestamps between the two padded ends.
            for (Map.Entry<String, List<Integer>> e : byTime.subMap(lo, true, hi, true).entrySet()) out.addAll(e.getValue());
            // Ascending ids give a deterministic answer.
            Collections.sort(out);
            return out;
        }
    }

    static final String[] UNITS = {"Year", "Month", "Day", "Hour", "Minute", "Second"};

    static String stamp(Random rnd) {
        // Small field ranges force many equal prefixes and boundary cases.
        return String.format("%04d:%02d:%02d:%02d:%02d:%02d", 2019 + rnd.nextInt(2), 1 + rnd.nextInt(2),
                1 + rnd.nextInt(2), rnd.nextInt(2), rnd.nextInt(2), rnd.nextInt(3));
    }

    public static void main(String[] args) {
        // The failure from the lesson: a date alone sorts before a timestamp of that date.
        if ("2021:05:07:12:00:00".compareTo("2021:05:07") <= 0) throw new AssertionError("text order");
        // Example 1: day and hour units.
        LogStore a = new LogStore();
        a.store(1, "2021:05:07:09:30:15");
        a.store(2, "2021:05:07:23:59:59");
        a.store(3, "2021:05:08:00:00:00");
        a.store(4, "2021:06:01:12:00:00");
        if (!a.retrieve("2021:05:07:12:00:00", "2021:05:08:00:00:00", "Day").equals(List.of(1, 2, 3))) throw new AssertionError("example 1 day");
        if (!a.retrieve("2021:05:07:12:00:00", "2021:05:08:00:00:00", "Hour").equals(List.of(2, 3))) throw new AssertionError("example 1 hour");
        // Example 2: year unit and an exact second.
        LogStore b = new LogStore();
        b.store(7, "2019:12:31:23:59:59");
        b.store(8, "2020:01:01:00:00:00");
        b.store(9, "2020:01:01:00:00:01");
        if (!b.retrieve("2019:01:01:00:00:00", "2020:01:01:00:00:00", "Year").equals(List.of(7, 8, 9))) throw new AssertionError("example 2 year");
        if (!b.retrieve("2020:01:01:00:00:00", "2020:01:01:00:00:00", "Second").equals(List.of(8))) throw new AssertionError("example 2 second");
        // Random data is compared with a scan that cuts every stored text.
        Random rnd = new Random(3806L);
        for (int t = 0; t < 2000; t++) {
            LogStore real = new LogStore();
            List<String> stamps = new ArrayList<>();
            int n = rnd.nextInt(12);
            for (int i = 0; i < n; i++) { String s = stamp(rnd); stamps.add(s); real.store(i + 1, s); }
            for (int q = 0; q < 6; q++) {
                String x = stamp(rnd), y = stamp(rnd);
                String s = x.compareTo(y) <= 0 ? x : y, e = x.compareTo(y) <= 0 ? y : x;
                String unit = UNITS[rnd.nextInt(UNITS.length)];
                int d = LogStore.digits(unit);
                List<Integer> expect = new ArrayList<>();
                for (int i = 0; i < n; i++) {
                    String cut = stamps.get(i).substring(0, d);
                    if (cut.compareTo(s.substring(0, d)) >= 0 && cut.compareTo(e.substring(0, d)) <= 0) expect.add(i + 1);
                }
                if (!real.retrieve(s, e, unit).equals(expect)) throw new AssertionError("random " + unit);
            }
        }
    }
}
```

#### Solution: [Vary] Tweet Counts Per Frequency (LeetCode 1348)
<!-- id: st38-count-per-interval -->

**Approach.**
Each sensor owns a `TreeMap` from time to the number of readings at that time. Readings may arrive in any order, so a tree map keeps the order that an array cannot keep with O(1) appends. A query computes the number of buckets as `(to - from) / width + 1` and allocates one `int` slot per bucket. The constraint on the range bounds that number. The query then reads only the entries of the sensor between `from` and `to`, both included, and adds each count to the slot `(time - from) / width`. The last bucket is shorter automatically, because no entry beyond `to` is read.

The invariant is that every reading inside the range is added to exactly one slot, and no reading outside the range is read. The program compares the class with a list of all readings that is scanned for each query, using random times with many duplicates.

**Complexity.**
- **Time** for `record` is O(log n). A query costs O(log n + m + B) for `m` readings in the range and `B` buckets, because the answer list has `B` entries.
- **Space** is O(n) for the stored readings and O(B) for one answer.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class CountPerIntervalVary {
    static final class ReadingCounter {
        private final Map<String, TreeMap<Long, Integer>> bySensor = new HashMap<>();

        /**
         * Returns the bucket width of a unit name in seconds.
         * Time: O(1). Space: O(1).
         * Invariant: the widths are 60, 3600 and 86400.
         */
        static long width(String unit) {
            // The three allowed units map to fixed widths.
            return unit.equals("minute") ? 60L : unit.equals("hour") ? 3600L : 86400L;
        }

        /**
         * Stores one reading.
         * Time: O(log n). Space: O(1) extra.
         * Invariant: the map holds the number of readings at each distinct time.
         */
        void record(String sensor, long time) {
            // merge adds 1 to the count at this time, or creates the entry with 1.
            bySensor.computeIfAbsent(sensor, k -> new TreeMap<>()).merge(time, 1, Integer::sum);
        }

        /**
         * Counts readings per bucket over the inclusive range [from, to].
         * Time: O(log n + m + B). Space: O(B).
         * Invariant: each reading adds to the slot (time - from) / width exactly once.
         */
        List<Integer> counts(String sensor, String unit, long from, long to) {
            long w = width(unit);
            // The range constraint keeps the number of buckets small enough for an int.
            int buckets = (int) ((to - from) / w + 1);
            int[] slots = new int[buckets];
            TreeMap<Long, Integer> m = bySensor.get(sensor);
            // An unknown sensor skips the loop and returns zeros.
            if (m != null)
                // The range view visits only readings with from <= time <= to.
                for (Map.Entry<Long, Integer> e : m.subMap(from, true, to, true).entrySet())
                    slots[(int) ((e.getKey() - from) / w)] += e.getValue();
            List<Integer> out = new ArrayList<>(buckets);
            // Copy the slots into the answer list.
            for (int c : slots) out.add(c);
            return out;
        }
    }

    public static void main(String[] args) {
        // Example 1: minute buckets with a short last bucket, then hour buckets.
        ReadingCounter a = new ReadingCounter();
        for (long t : new long[]{10, 70, 75, 130, 3700, 3700}) a.record("a", t);
        if (!a.counts("a", "minute", 10, 200).equals(List.of(1, 2, 1, 0))) throw new AssertionError("example 1 minute");
        if (!a.counts("a", "hour", 0, 7200).equals(List.of(4, 2, 0))) throw new AssertionError("example 1 hour");
        // Example 2: duplicates, an inclusive end that opens a new bucket, and an unknown sensor.
        ReadingCounter b = new ReadingCounter();
        b.record("b", 5); b.record("b", 5); b.record("b", 120);
        if (!b.counts("b", "minute", 0, 119).equals(List.of(2, 0))) throw new AssertionError("example 2 a");
        if (!b.counts("b", "minute", 0, 120).equals(List.of(2, 0, 1))) throw new AssertionError("example 2 b");
        if (!b.counts("c", "day", 0, 0).equals(List.of(0))) throw new AssertionError("example 2 c");
        // Random readings are compared with a scan of all readings for every query.
        Random rnd = new Random(3807L);
        String[] units = {"minute", "hour", "day"};
        String[] names = {"p", "q"};
        for (int t = 0; t < 3000; t++) {
            ReadingCounter real = new ReadingCounter();
            List<long[]> all = new ArrayList<>();
            List<String> who = new ArrayList<>();
            for (int i = rnd.nextInt(15); i > 0; i--) {
                long time = rnd.nextInt(400);
                String s = names[rnd.nextInt(2)];
                real.record(s, time); all.add(new long[]{time}); who.add(s);
            }
            for (int q = 0; q < 5; q++) {
                long from = rnd.nextInt(300), to = from + rnd.nextInt(300);
                String unit = rnd.nextInt(2) == 0 ? "minute" : units[rnd.nextInt(3)];
                String s = names[rnd.nextInt(2)];
                long w = ReadingCounter.width(unit);
                int[] expect = new int[(int) ((to - from) / w + 1)];
                for (int i = 0; i < all.size(); i++) {
                    long time = all.get(i)[0];
                    if (who.get(i).equals(s) && time >= from && time <= to) expect[(int) ((time - from) / w)]++;
                }
                List<Integer> got = real.counts(s, unit, from, to);
                if (got.size() != expect.length) throw new AssertionError("size");
                for (int i = 0; i < expect.length; i++) if (got.get(i) != expect[i]) throw new AssertionError("count");
            }
        }
    }
}
```

#### Solution: [Boundary] Sparse Empty Buckets (Author exercise)
<!-- id: st38-sparse-empty-buckets -->

**Approach.**
Events arrive in non-decreasing order, so a growable `long` array is a sorted index. Two helper searches return the first position whose time is at least a target. The method `nonEmpty` searches for `from` once, then walks the events up to `to`. For each event it computes the bucket number `(time - from) / size`. It advances over all events with the same number and emits the bucket start with their count. Empty buckets never appear, so the cost depends on the events in the range and not on the number of buckets. The method `countAt` first computes the number of buckets `(to - from) / size + 1`, which reaches 10^15 and so needs a `long`. It returns -1 for an index outside that count. Otherwise it takes the bucket start `from + index * size` and the bucket end `min(start + size - 1, to)`. The count is the difference of two searches.

The invariant is that a pair covers one run of events with one bucket number. The product `index * size` never exceeds `to - from`, so it fits in a `long`. The program also checks the Java facts that the lesson relies on. The cast of 10^12 + 1 to `int` is negative, and the allocation with that size throws `NegativeArraySizeException`. Random small ranges are checked against a dense array that counts every bucket.

**Complexity.**
- **Time** for `record` is O(1) amortized. The method `nonEmpty` costs O(log n + m) for `m` events in the range, and `countAt` costs O(log n).
- **Space** is O(n) for the events and O(k) for the `k` pairs of one answer, and no space depends on the number of buckets.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class SparseEmptyBucketsBoundary {
    static final class SparseSeries {
        private long[] times = new long[16];
        private int n;

        /**
         * Appends one event.
         * Time: O(1) amortized. Space: O(1) extra.
         * Invariant: the array stays in non-decreasing order.
         */
        void record(long time) {
            // A smaller time would break the order, so it is rejected.
            if (n > 0 && time < times[n - 1]) throw new IllegalArgumentException("time went backward");
            // Doubling the array keeps the append cost O(1) amortized.
            if (n == times.length) times = Arrays.copyOf(times, n * 2);
            times[n++] = time;
        }

        /**
         * Finds the first position whose time is at least the target.
         * Time: O(log n). Space: O(1).
         * Invariant: every position below lo is smaller than target, every position from hi on is not.
         */
        private int lowerBound(long target) {
            int lo = 0, hi = n;
            // Each pass halves the window, so there are O(log n) passes.
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                // A time below the target lies left of the answer.
                if (times[mid] < target) lo = mid + 1;
                else hi = mid;
            }
            return lo;
        }

        /**
         * Lists the nonempty buckets of [from, to] in ascending order.
         * Time: O(log n + m). Space: O(k).
         * Invariant: each pair covers one maximal run of events with equal bucket number.
         */
        List<long[]> nonEmpty(long from, long to, long size) {
            List<long[]> out = new ArrayList<>();
            // One search finds the first event of the range.
            int i = lowerBound(from);
            // The walk stops at the first event after the range.
            while (i < n && times[i] <= to) {
                long b = (times[i] - from) / size;
                int start = i;
                // Advance over every event with the same bucket number.
                while (i < n && times[i] <= to && (times[i] - from) / size == b) i++;
                // The pair holds the bucket start and the event count.
                out.add(new long[]{from + b * size, i - start});
            }
            return out;
        }

        /**
         * Returns the count of one bucket, 0 if empty, -1 if the index is outside the range.
         * Time: O(log n). Space: O(1).
         * Invariant: index * size stays at most to - from, so no overflow occurs.
         */
        long countAt(long from, long to, long size, long index) {
            long buckets = (to - from) / size + 1;
            // An index outside the bucket count is not a bucket.
            if (index < 0 || index >= buckets) return -1;
            long start = from + index * size;
            // The last bucket ends at the inclusive end of the range.
            long end = Math.min(start + size - 1, to);
            // Two searches count the events with start <= time <= end.
            return lowerBound(end + 1) - lowerBound(start);
        }
    }

    public static void main(String[] args) {
        // The lesson claim: casting 10^12 + 1 to int gives a negative size, and allocation fails.
        if ((int) (1_000_000_000_000L + 1) >= 0) throw new AssertionError("cast should be negative");
        boolean threw = false;
        try { int[] x = new int[(int) (1_000_000_000_000L + 1)]; } catch (NegativeArraySizeException e) { threw = true; }
        if (!threw) throw new AssertionError("negative size must throw");
        // Example 1: three nonempty buckets among six.
        SparseSeries a = new SparseSeries();
        for (long t : new long[]{2, 2, 9, 31, 33, 58}) a.record(t);
        List<long[]> got = a.nonEmpty(0, 59, 10);
        long[][] want = {{0, 3}, {30, 2}, {50, 1}};
        if (got.size() != 3) throw new AssertionError("example 1 size");
        for (int i = 0; i < 3; i++) if (!Arrays.equals(got.get(i), want[i])) throw new AssertionError("example 1 pair");
        if (a.countAt(0, 59, 10, 1) != 0 || a.countAt(0, 59, 10, 5) != 1 || a.countAt(0, 59, 10, 6) != -1) throw new AssertionError("example 1 countAt");
        // Example 2: two events 10^15 apart, memory does not depend on the bucket count.
        SparseSeries b = new SparseSeries();
        b.record(0); b.record(1_000_000_000_000_000L);
        List<long[]> far = b.nonEmpty(0, 1_000_000_000_000_000L, 7);
        if (far.size() != 2 || far.get(0)[0] != 0 || far.get(0)[1] != 1 || far.get(1)[0] != 999_999_999_999_994L || far.get(1)[1] != 1) throw new AssertionError("example 2 pairs");
        if (b.countAt(0, 1_000_000_000_000_000L, 7, 142_857_142_857_142L) != 1 || b.countAt(0, 1_000_000_000_000_000L, 7, 142_857_142_857_143L) != -1) throw new AssertionError("example 2 countAt");
        // Random small ranges are compared with a dense array of every bucket.
        Random rnd = new Random(3808L);
        for (int t = 0; t < 3000; t++) {
            SparseSeries real = new SparseSeries();
            List<Long> ev = new ArrayList<>();
            long cur = rnd.nextInt(5);
            for (int i = rnd.nextInt(12); i > 0; i--) { cur += rnd.nextInt(9); ev.add(cur); real.record(cur); }
            long from = rnd.nextInt(10), to = from + rnd.nextInt(80), size = 1 + rnd.nextInt(12);
            int nb = (int) ((to - from) / size + 1);
            long[] dense = new long[nb];
            for (long x : ev) if (x >= from && x <= to) dense[(int) ((x - from) / size)]++;
            List<long[]> pairs = real.nonEmpty(from, to, size);
            int p = 0;
            for (int k = 0; k < nb; k++) {
                if (dense[k] > 0) {
                    long[] pr = pairs.get(p++);
                    if (pr[0] != from + (long) k * size || pr[1] != dense[k]) throw new AssertionError("pair");
                }
                if (real.countAt(from, to, size, k) != dense[k]) throw new AssertionError("countAt");
            }
            if (p != pairs.size() || real.countAt(from, to, size, nb) != -1) throw new AssertionError("extra pairs");
        }
    }
}
```

#### Solution: [Recognize] Design Exam Scores Tracker (LeetCode 3709)
<!-- id: st38-exam-scores-tracker -->

**Approach.**
The ledger keeps two parallel `long` arrays. The array `times` holds the result times, which strictly increase, so it is a sorted index. The array `prefix` is one slot longer than `times`, and entry `prefix[i]` holds the total of the first `i` scores. A range `[from, to]` becomes the half-open range `[from, to + 1)` once, at the entry of `total`. Two binary searches give the position `l` of the first result at or after `from` and the position `r` of the first result at or after `to + 1`. The answer is `prefix[r] - prefix[l]`, which is the sum of the scores at the positions `l` through `r - 1`. A reversed range gives 0 by an explicit test.

The invariant is that `prefix[i + 1] = prefix[i] + score_i` at all times, so any contiguous run sums by one subtraction. The sums use `long`, because three scores of 10^9 already exceed `Integer.MAX_VALUE`. The program asserts that fact and compares the class with a loop over all results on random data.

**Complexity.**
- **Time** for `add` is O(1) amortized, and `total` costs O(log n) for two searches.
- **Space** is O(n) for the two arrays, and a query uses O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ExamScoresTrackerRecognize {
    static final class ScoreLedger {
        private long[] times = new long[16];
        private long[] prefix = new long[17];
        private int n;

        /**
         * Stores one result.
         * Time: O(1) amortized. Space: O(1) extra.
         * Invariant: prefix[i + 1] equals prefix[i] plus the score at position i.
         */
        void add(long time, int score) {
            // Times must strictly increase, which keeps the array sorted without duplicates.
            if (n > 0 && time <= times[n - 1]) throw new IllegalArgumentException("times must increase");
            // Both arrays double together, so one growth test is enough.
            if (n == times.length) { times = Arrays.copyOf(times, n * 2); prefix = Arrays.copyOf(prefix, n * 2 + 1); }
            times[n] = time;
            // The running total adds the score as a long, so large sums do not wrap.
            prefix[n + 1] = prefix[n] + score;
            n++;
        }

        /**
         * Finds the first position whose time is at least the target.
         * Time: O(log n). Space: O(1).
         * Invariant: every position below lo is smaller than target, every position from hi on is not.
         */
        private int lowerBound(long target) {
            int lo = 0, hi = n;
            // The window halves on every pass.
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                // A time below the target lies left of the answer.
                if (times[mid] < target) lo = mid + 1;
                else hi = mid;
            }
            return lo;
        }

        /**
         * Sums the scores with from <= time <= to.
         * Time: O(log n). Space: O(1).
         * Invariant: the half-open range [from, to + 1) selects positions l through r - 1.
         */
        long total(long from, long to) {
            // A reversed range holds no result.
            if (from > to) return 0;
            int l = lowerBound(from);
            int r = lowerBound(to + 1);
            // One subtraction of running totals sums the contiguous run.
            return prefix[r] - prefix[l];
        }
    }

    public static void main(String[] args) {
        // The lesson claim: three scores of 10^9 exceed the int range.
        if (3L * 1_000_000_000 <= Integer.MAX_VALUE) throw new AssertionError("int overflow claim");
        // Example 1: a sum above the int range, an inner range, and an empty range.
        ScoreLedger a = new ScoreLedger();
        a.add(5, 900_000_000); a.add(8, 800_000_000); a.add(20, 700_000_000);
        if (a.total(5, 20) != 2_400_000_000L || a.total(6, 19) != 800_000_000L || a.total(9, 10) != 0) throw new AssertionError("example 1");
        // Example 2: a reversed range, the full span, and a single point.
        ScoreLedger b = new ScoreLedger();
        b.add(3, 10); b.add(4, 20);
        if (b.total(4, 3) != 0 || b.total(1, 1_000_000_000) != 30 || b.total(3, 3) != 10) throw new AssertionError("example 2");
        // Random ledgers are compared with a loop over every result.
        Random rnd = new Random(3809L);
        for (int t = 0; t < 3000; t++) {
            ScoreLedger real = new ScoreLedger();
            int n = rnd.nextInt(40);
            long[] ts = new long[n];
            long[] sc = new long[n];
            long cur = 0;
            for (int i = 0; i < n; i++) {
                cur += 1 + rnd.nextInt(5);
                ts[i] = cur;
                sc[i] = 1 + rnd.nextInt(1_000_000_000);
                real.add(ts[i], (int) sc[i]);
            }
            for (int q = 0; q < 8; q++) {
                long from = rnd.nextInt(80) - 3, to = rnd.nextInt(80) - 3;
                long expect = 0;
                for (int i = 0; i < n; i++) if (ts[i] >= from && ts[i] <= to) expect += sc[i];
                if (real.total(from, to) != expect) throw new AssertionError("total");
            }
        }
    }
}
```
