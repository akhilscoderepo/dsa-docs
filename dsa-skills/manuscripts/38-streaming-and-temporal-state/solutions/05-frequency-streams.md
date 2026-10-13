<!-- solutions-for: 05-frequency-streams -->
### Solutions For Frequency Streams

#### Solution: [Build] Pair Sum Lookup (LeetCode 170)
<!-- id: st38-pair-sum-lookup -->

**Approach.**
The store keeps a hash map from each value to the number of times it was added. A query walks the distinct values. For each value `x` it computes the partner `target - x` in `long` arithmetic, so the subtraction cannot overflow `int`. If the partner differs from `x`, the query needs the partner to be in the map. If the partner equals `x`, the query needs a count of at least 2, because one stored element cannot pair with itself. The invariant is that `counts` equals the multiset of added values, and `add` is the only writer.

The program compares the store with a double loop over a list of all added values. Random streams use small values, so equal partners occur often. Separate checks cover targets that need `long` arithmetic.

**Complexity.**
- **Time** is O(1) expected for `add` and O(d) for `find`, where `d` is the number of distinct values, because `find` visits each key once with a constant-time lookup.
- **Space** is O(d), because the map stores one entry per distinct value.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public final class PairSumStoreBuild {
    static final class PairSumStore {
        private final HashMap<Long, Integer> counts = new HashMap<>();

        /**
         * Appends one value to the multiset.
         * Time: O(1) expected. Space: O(1) extra.
         * Invariant: counts holds the multiplicity of every added value.
         */
        void add(int x) {
            // merge raises the stored multiplicity by one in a single hash operation.
            counts.merge((long) x, 1, Integer::sum);
        }

        /**
         * Tells whether two different stored positions sum to target.
         * Time: O(d) expected for d distinct values. Space: O(1).
         * Invariant: a value pairs with itself only when its count is at least 2.
         */
        boolean find(long target) {
            // Each distinct value is tried once as the first element of a pair.
            for (java.util.Map.Entry<Long, Integer> e : counts.entrySet()) {
                // long arithmetic keeps target - x exact for every int x.
                long partner = target - e.getKey();
                if (partner == e.getKey()) {
                    // A value pairs with itself only through two separate copies.
                    if (e.getValue() >= 2) return true;
                } else if (counts.containsKey(partner)) {
                    // A different partner needs only one stored copy.
                    return true;
                }
            }
            // No distinct value found a partner.
            return false;
        }
    }

    public static void main(String[] args) {
        // Example 1: equal values pair through two copies, and a single 7 cannot pair with itself.
        PairSumStore s = new PairSumStore();
        s.add(3); s.add(7); s.add(3);
        if (!s.find(6) || !s.find(10) || s.find(14) || s.find(9)) throw new AssertionError("example 1");
        // Example 2: a long target works, and a single value needs a second copy.
        PairSumStore t = new PairSumStore();
        t.add(-5);
        if (t.find(-10)) throw new AssertionError("one copy cannot pair with itself");
        t.add(-5);
        if (!t.find(-10)) throw new AssertionError("two copies pair");
        t.add(1000000000);
        if (!t.find(999999995L)) throw new AssertionError("example 2");
        // An empty store has no pair, and a target beyond int range stays exact.
        if (new PairSumStore().find(0)) throw new AssertionError("empty store");
        PairSumStore big = new PairSumStore();
        big.add(1000000000); big.add(1000000000); big.add(-1000000000);
        if (!big.find(2000000000L) || big.find(4000000000L) || !big.find(0)) throw new AssertionError("long targets");
        // Random streams compare every answer with a double loop over positions.
        Random rnd = new Random(3805L);
        for (int trial = 0; trial < 3000; trial++) {
            PairSumStore real = new PairSumStore();
            List<Integer> all = new ArrayList<>();
            for (int step = rnd.nextInt(25); step > 0; step--) {
                if (rnd.nextBoolean()) {
                    int v = rnd.nextInt(9) - 4;
                    real.add(v); all.add(v);
                } else {
                    long target = rnd.nextInt(21) - 10;
                    boolean expect = false;
                    for (int i = 0; i < all.size(); i++)
                        for (int j = i + 1; j < all.size(); j++)
                            if ((long) all.get(i) + all.get(j) == target) expect = true;
                    if (real.find(target) != expect) throw new AssertionError("find " + target + " in " + all);
                }
            }
        }
    }
}
```

#### Solution: [Vary] First Unique Reader (LeetCode 1429)
<!-- id: st38-first-unique-reader -->

**Approach.**
The reader keeps a count map and a queue `order` of values in the order their count first reached 1. It also keeps the integer `unique`, the number of values with count exactly 1. An append raises the count of its value. When the new count is 1, the value joins the queue and `unique` grows. When the new count is 2, the value leaves the unique set, so `unique` shrinks, and the queue entry becomes stale. When the count is above 2, nothing else changes. The method `first` pops from the front while the front's count differs from 1, then reads the front.

The invariant is that every value with count 1 is in the queue in arrival order. Any other entry in the queue is stale and is removed before the queue is read. A value is pushed once because its count passes through 1 once, so each entry is popped at most once. The program compares all three methods with a recount over the full stream.

**Complexity.**
- **Time** is O(1) per `append` and `uniqueCount`, and O(1) amortized for `first`, because the total number of pops never exceeds the number of pushes.
- **Space** is O(d) for `d` distinct values, since the map and the queue each hold at most one entry per value.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public final class UniqueReaderVary {
    static final class UniqueReader {
        private final HashMap<Integer, Integer> counts = new HashMap<>();
        private final ArrayDeque<Integer> order = new ArrayDeque<>();
        private int unique;

        UniqueReader(int[] initial) {
            // Initial values go through the same path as later appends.
            for (int v : initial) append(v);
        }

        /**
         * Adds one value to the end of the stream.
         * Time: O(1) expected. Space: O(1) extra.
         * Invariant: counts is exact, and order holds every value of count 1.
         */
        void append(int v) {
            // The authoritative count rises by one.
            int c = counts.merge(v, 1, Integer::sum);
            if (c == 1) {
                // First arrival: the value becomes a candidate and a unique value.
                order.addLast(v);
                unique++;
            } else if (c == 2) {
                // Second arrival: the value stops being unique, its queue entry is now stale.
                unique--;
            }
        }

        /**
         * Returns the earliest value that occurs once, or -1.
         * Time: O(1) amortized. Space: O(1).
         * Invariant: a stale front is removed before the front is read.
         */
        int first() {
            // Each stale entry is popped once, and its push paid for the pop.
            while (!order.isEmpty() && counts.get(order.peekFirst()) != 1) order.pollFirst();
            // After the loop the front, if any, has count exactly 1.
            return order.isEmpty() ? -1 : order.peekFirst();
        }

        /**
         * Counts the values that occur exactly once.
         * Time: O(1). Space: O(1).
         */
        int uniqueCount() {
            // The counter was maintained by append, so no scan is needed.
            return unique;
        }
    }

    public static void main(String[] args) {
        // Example 1: a 4 arrives twice, then a 9 arrives twice.
        UniqueReader a = new UniqueReader(new int[]{7, 7, 4});
        if (a.first() != 4) throw new AssertionError("e1 a");
        a.append(4);
        if (a.first() != -1) throw new AssertionError("e1 b");
        a.append(9);
        if (a.first() != 9 || a.uniqueCount() != 1) throw new AssertionError("e1 c");
        a.append(9);
        if (a.first() != -1) throw new AssertionError("e1 d");
        // Example 2: an empty reader grows one value and loses uniqueness.
        UniqueReader b = new UniqueReader(new int[0]);
        if (b.first() != -1) throw new AssertionError("e2 a");
        b.append(6);
        if (b.uniqueCount() != 1) throw new AssertionError("e2 b");
        b.append(6);
        if (b.uniqueCount() != 0 || b.first() != -1) throw new AssertionError("e2 c");
        // Random streams compare each answer with a full recount of the history.
        Random rnd = new Random(3806L);
        for (int trial = 0; trial < 3000; trial++) {
            int n0 = rnd.nextInt(6);
            int[] init = new int[n0];
            List<Integer> all = new ArrayList<>();
            for (int i = 0; i < n0; i++) { init[i] = rnd.nextInt(5); all.add(init[i]); }
            UniqueReader real = new UniqueReader(init);
            for (int step = rnd.nextInt(25); step > 0; step--) {
                int op = rnd.nextInt(3);
                if (op == 0) { int v = rnd.nextInt(5); real.append(v); all.add(v); }
                else {
                    int expectFirst = -1, expectCount = 0;
                    for (int v : all) {
                        int occurrences = 0;
                        for (int w : all) if (w == v) occurrences++;
                        if (occurrences == 1) { if (expectFirst == -1) expectFirst = v; expectCount++; }
                    }
                    if (op == 1 && real.first() != expectFirst) throw new AssertionError("first of " + all);
                    if (op == 2 && real.uniqueCount() != expectCount) throw new AssertionError("uniqueCount of " + all);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Count Of Counts (LeetCode 2671)
<!-- id: st38-count-of-counts -->

**Approach.**
The tracker keeps `counts`, the number of copies of each value, and `tally`, the number of values that have each count. All changes pass through one private method, `shift`, which receives a value with its old and new count. It lowers `tally[old]` when the old count is positive and raises `tally[new]` when the new count is positive. It then writes the value into `counts`, or removes it when the new count is 0. Because every count of 0 is skipped on the tally side and removed on the map side, absent values leave no trace in either map.

The invariant is that `tally[c]` equals the number of values with count `c` for every `c >= 1`, and neither map contains a zero entry. `removeOne` on an absent value reads count 0 and does nothing. `removeAll` calls `shift` once with the full old count and a new count of 0, so the tally entry for the old count drops by exactly 1. The program compares the tracker with a recount of a plain map after every operation and checks that the tally map never holds an entry that is zero or negative.

**Complexity.**
- **Time** is O(1) expected per call, since `shift` performs a fixed number of hash operations and `hasFrequency` performs one lookup.
- **Space** is O(d) for `d` distinct stored values, because the tally never has more entries than the map has values.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class FrequencyTrackerBoundary {
    static final class FrequencyTracker {
        private final HashMap<Integer, Integer> counts = new HashMap<>();
        private final HashMap<Integer, Integer> tally = new HashMap<>();

        /**
         * Moves one value from count "from" to count "to" in both maps.
         * Time: O(1) expected. Space: O(1).
         * Invariant: afterwards tally agrees with counts, and neither holds zero.
         */
        private void shift(int v, int from, int to) {
            // The old bucket loses the value, and an emptied bucket is removed.
            if (from > 0 && tally.merge(from, -1, Integer::sum) == 0) tally.remove(from);
            // The new bucket gains the value, except for count 0 which means absent.
            if (to > 0) tally.merge(to, 1, Integer::sum);
            // The authoritative map drops the key at zero and stores the count otherwise.
            if (to == 0) counts.remove(v); else counts.put(v, to);
        }

        /** Stores one more copy of x. Time: O(1) expected. Space: O(1). */
        void add(int x) {
            // Read the old count, defaulting to 0 for a new value.
            int c = counts.getOrDefault(x, 0);
            // The value moves up by one.
            shift(x, c, c + 1);
        }

        /** Removes one copy of x if present. Time: O(1) expected. Space: O(1). */
        void removeOne(int x) {
            // An absent value has count 0 and changes nothing.
            int c = counts.getOrDefault(x, 0);
            if (c > 0) shift(x, c, c - 1);
        }

        /** Removes every copy of x. Time: O(1) expected. Space: O(1). */
        void removeAll(int x) {
            // One shift moves the value from its full count straight to absent.
            int c = counts.getOrDefault(x, 0);
            if (c > 0) shift(x, c, 0);
        }

        /** Tells whether some value occurs exactly f times. Time: O(1) expected. Space: O(1). */
        boolean hasFrequency(int f) {
            // A single lookup in the tally answers the question.
            return tally.getOrDefault(f, 0) > 0;
        }

        /** Test hook: confirms the tally equals a recount of the counts. */
        boolean consistent() {
            // Recount the buckets from the authoritative map.
            HashMap<Integer, Integer> rec = new HashMap<>();
            for (int c : counts.values()) {
                if (c <= 0) return false;
                rec.merge(c, 1, Integer::sum);
            }
            // Equal maps imply no zero or negative tally entries either.
            return rec.equals(tally);
        }
    }

    public static void main(String[] args) {
        // Example 1: removing one copy of 5 turns frequency 2 into frequency 1.
        FrequencyTracker a = new FrequencyTracker();
        a.add(5); a.add(5); a.add(8);
        if (!a.hasFrequency(2)) throw new AssertionError("e1 a");
        a.removeOne(5);
        if (a.hasFrequency(2) || !a.hasFrequency(1)) throw new AssertionError("e1 b");
        a.removeAll(8);
        if (!a.hasFrequency(1) || a.hasFrequency(2)) throw new AssertionError("e1 c");
        // Example 2: removing an absent value, then removing all copies, leaves no frequency.
        FrequencyTracker b = new FrequencyTracker();
        b.removeOne(4);
        if (b.hasFrequency(1) || !b.consistent()) throw new AssertionError("e2 a");
        b.add(4); b.add(4); b.add(4);
        b.removeAll(4);
        if (b.hasFrequency(3) || b.hasFrequency(1) || !b.consistent()) throw new AssertionError("e2 b");
        // Random operations compare with a recount, and the maps stay consistent after each call.
        Random rnd = new Random(3807L);
        for (int trial = 0; trial < 3000; trial++) {
            FrequencyTracker real = new FrequencyTracker();
            Map<Integer, Integer> model = new HashMap<>();
            for (int step = rnd.nextInt(30); step > 0; step--) {
                int op = rnd.nextInt(4);
                int v = rnd.nextInt(4);
                if (op == 0) { real.add(v); model.merge(v, 1, Integer::sum); }
                else if (op == 1) { real.removeOne(v); if (model.merge(v, -1, Integer::sum) <= 0) model.remove(v); }
                else if (op == 2) { real.removeAll(v); model.remove(v); }
                else {
                    int f = 1 + rnd.nextInt(4);
                    if (real.hasFrequency(f) != model.containsValue(f)) throw new AssertionError("hasFrequency " + f + " in " + model);
                }
                if (!real.consistent()) throw new AssertionError("tally disagrees with counts");
            }
        }
    }
}
```

#### Solution: [Recognize] Suffix Run Counter (LeetCode 2526)
<!-- id: st38-suffix-run-counter -->

**Approach.**
The answer to every call depends on one number, the length of the run of `target` values at the end of the stream. A pushed value equal to `target` extends the run by 1, and any other value ends it, so the run becomes 0. The method `push` returns whether the run is at least `k`. Because a run of at least `k` includes at least `k` pushed values, the case "fewer than `k` values pushed" needs no separate test. The run uses `long`, since `k` can reach 10^12.

The invariant is that `run` equals the number of consecutive `target` values ending at the last pushed value. Nothing stored depends on `k`, so memory is constant. The program compares the class with a check of the last `k` entries of the full history, and it uses a large `k` with a direct assertion.

**Complexity.**
- **Time** is O(1) per call, because each call performs one comparison and one assignment.
- **Space** is O(1), as the object stores `target`, `k` and `run` and no history.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SuffixRunRecognize {
    static final class SuffixRun {
        private final int target;
        private final long k;
        private long run;

        SuffixRun(int target, long k) {
            // Only two constants and one counter are stored.
            this.target = target;
            this.k = k;
        }

        /**
         * Appends x and tells whether the last k values all equal target.
         * Time: O(1). Space: O(1).
         * Invariant: run is the length of the target suffix of the stream.
         */
        boolean push(int x) {
            // A match extends the suffix, and anything else ends it.
            run = (x == target) ? run + 1 : 0;
            // A suffix of length k or more contains k pushed values, all equal to target.
            return run >= k;
        }

        /** Returns the current suffix length. Time: O(1). Space: O(1). */
        long currentRun() {
            // The counter is the answer itself.
            return run;
        }
    }

    public static void main(String[] args) {
        // Example 1: the run of 6 breaks at 2 and then reaches 3 at the sixth push.
        SuffixRun a = new SuffixRun(6, 3);
        int[] in = {6, 6, 2, 6, 6, 6, 6};
        boolean[] want = {false, false, false, false, false, true, true};
        for (int i = 0; i < in.length; i++)
            if (a.push(in[i]) != want[i]) throw new AssertionError("e1 at " + i);
        // Example 2: with k equal to 1, every target value answers true at once.
        SuffixRun b = new SuffixRun(0, 1);
        if (!b.push(0) || b.push(5) || !b.push(0) || b.currentRun() != 1) throw new AssertionError("e2");
        // A huge k needs no memory and stays false, and the run counter does not overflow int arithmetic.
        SuffixRun big = new SuffixRun(1, 1_000_000_000_000L);
        for (int i = 0; i < 1000; i++) if (big.push(1)) throw new AssertionError("big k");
        if (big.currentRun() != 1000) throw new AssertionError("big run");
        // Random streams compare each answer with a direct check of the last k stored values.
        Random rnd = new Random(3808L);
        for (int trial = 0; trial < 3000; trial++) {
            int target = rnd.nextInt(3);
            int k = 1 + rnd.nextInt(5);
            SuffixRun real = new SuffixRun(target, k);
            List<Integer> all = new ArrayList<>();
            for (int step = rnd.nextInt(25); step > 0; step--) {
                int x = rnd.nextInt(3);
                all.add(x);
                boolean expect = all.size() >= k;
                for (int i = all.size() - k; expect && i < all.size(); i++) if (all.get(i) != target) expect = false;
                if (real.push(x) != expect) throw new AssertionError("push on " + all);
                int suffix = 0;
                for (int i = all.size() - 1; i >= 0 && all.get(i) == target; i--) suffix++;
                if (real.currentRun() != suffix) throw new AssertionError("currentRun on " + all);
            }
        }
    }
}
```
