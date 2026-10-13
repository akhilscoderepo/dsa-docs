<!-- solutions-for: 04-version-histories -->
### Solutions For Version Histories

#### Solution: [Build] Versioned Integer (Author exercise)
<!-- id: it37-version-histories-versioned-integer -->

**Approach.**
The class stores the changes in two parallel `long`/`int` arrays, `versions` and `values`, in the order of the `set` calls. The invariant is that `versions` is strictly increasing, which the contract guarantees for every call. The method `get` runs a binary search for the first index whose version is greater than the query. The slot before that index holds the latest change that is not after the query. When the search returns index 0, every stored version is above the query, so the method returns -1 and never reads index minus one.

The harness checks the claim against a brute-force scan that walks the whole list of pairs and keeps the last pair whose version is at most the query. The random queries include versions before the first change, equal to a stored version, between two versions and after the last one.

**Complexity.**
- **Time** is O(1) amortized per `set` because the arrays double, and O(log k) per `get` because each probe halves the window of `k` changes.
- **Space** is O(k) for `k` stored changes, with no copy of the past.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class VersionedIntBuild {
    /** Stores changes in version order and answers a floor query on the versions. */
    static final class VersionedInt {
        private long[] versions = new long[2];
        private int[] values = new int[2];
        private int size;

        /**
         * Appends one change.
         * Time: O(1) amortized. Space: O(1) amortized.
         * Invariant: versions stays strictly increasing because the caller sends increasing versions.
         */
        void set(long version, int value) {
            // Doubling the arrays keeps the amortized cost of an append constant.
            if (size == versions.length) {
                versions = java.util.Arrays.copyOf(versions, size * 2);
                values = java.util.Arrays.copyOf(values, size * 2);
            }
            // The new pair goes after every older pair, which preserves the sorted order.
            versions[size] = version;
            values[size] = value;
            size++;
        }

        /**
         * Returns the value of the latest change at or before the query version, or -1.
         * Time: O(log size). Space: O(1).
         * Invariant: every index below lo holds a version at most the query, and every index from hi holds a larger one.
         */
        int get(long version) {
            // The window starts as the whole history.
            int lo = 0, hi = size;
            // Each iteration halves the window, so the loop runs O(log size) times.
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                // A version at most the query moves the left edge past mid.
                if (versions[mid] <= version) lo = mid + 1;
                // A larger version becomes the new right edge.
                else hi = mid;
            }
            // lo is the first index with a larger version, so lo - 1 is the floor slot; 0 means none.
            return lo == 0 ? -1 : values[lo - 1];
        }
    }

    /** Reference: scans every pair and keeps the last one not after the query. Time: O(k) per query. */
    static int oracle(List<long[]> pairs, long version) {
        int best = -1;
        // A scan in insertion order sees the pairs from the smallest version to the largest.
        for (long[] p : pairs) if (p[0] <= version) best = (int) p[1];
        return best;
    }

    public static void main(String[] args) {
        // Example 1 from the exercise, including the query before the first change and after the last.
        VersionedInt a = new VersionedInt();
        a.set(3, 10);
        a.set(8, 20);
        if (a.get(2) != -1 || a.get(3) != 10 || a.get(7) != 10 || a.get(8) != 20 || a.get(100) != 20) throw new AssertionError("example 1");
        // Example 2: version 0 is before the only change.
        VersionedInt b = new VersionedInt();
        b.set(1, 7);
        if (b.get(0) != -1 || b.get(1) != 7) throw new AssertionError("example 2");
        // An empty history and a version near 10^15 both behave, and long arithmetic is not truncated.
        VersionedInt c = new VersionedInt();
        if (c.get(0) != -1) throw new AssertionError("empty");
        c.set(1_000_000_000_000_000L, 5);
        if (c.get(999_999_999_999_999L) != -1 || c.get(1_000_000_000_000_000L) != 5) throw new AssertionError("large version");
        // Random histories are compared with the scan for every query version in range.
        Random rnd = new Random(3704L);
        for (int t = 0; t < 3000; t++) {
            VersionedInt real = new VersionedInt();
            List<long[]> pairs = new ArrayList<>();
            long v = rnd.nextInt(3);
            int n = rnd.nextInt(12);
            for (int i = 0; i < n; i++) {
                int val = rnd.nextInt(100);
                real.set(v, val);
                pairs.add(new long[] {v, val});
                v += 1 + rnd.nextInt(4);
            }
            for (long q = -1; q <= v + 2; q++) {
                if (q < 0) continue;
                if (real.get(q) != oracle(pairs, q)) throw new AssertionError("query " + q);
            }
        }
    }
}
```

#### Solution: [Vary] Snapshot Array (LeetCode 1146)
<!-- id: it37-version-histories-snapshot-array -->

**Approach.**
Each cell owns a history of pairs (snapshot id, value). A call to `set` does not touch any history. It writes into a pending table keyed by index, so repeated writes to one cell inside one snapshot interval collapse into one entry. A call to `snap` moves every pending entry into the history of its cell, tagged with the new snapshot id. It then clears the table and increments the counter. A cell that never changes has no history object at all, which keeps memory proportional to the number of distinct changes.

The method `get` first answers -1 for a snapshot that does not exist yet. For an existing id it runs a floor search in the cell's history and returns the starting value when no stored id is at most the query. The invariant is that every history holds strictly increasing ids, because `snap` adds at most one pair per cell and ids only grow. The harness compares the class with a full-copy model on random operation sequences, including reads of snapshots that do not exist.

**Complexity.**
- **Time** is O(1) per `set`, O(w) per `snap` for `w` distinct cells written since the last snapshot, and O(log k) per `get` for `k` pairs.
- **Space** is O(c) for `c` distinct cell changes, plus O(w) for the pending table.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class SnapshotArrayVary {
    /** Snapshot array that stores only the cells changed in each snapshot interval. */
    static final class SnapshotArray {
        private final long start;
        private final int[][] ids;       // ids[i] is the sorted snapshot ids at which cell i changed
        private final long[][] vals;     // vals[i][k] is the value that cell i took at ids[i][k]
        private final int[] counts;
        private final Map<Integer, Long> pending = new HashMap<>();
        private int snaps;

        SnapshotArray(int length, long start) {
            // Every cell starts with an empty history and the shared starting value.
            this.start = start;
            this.ids = new int[length][];
            this.vals = new long[length][];
            this.counts = new int[length];
        }

        /**
         * Records a write inside the current interval.
         * Time: O(1). Space: O(1) per distinct cell.
         * Invariant: a second write to a cell replaces the first, so the table has one entry per cell.
         */
        void set(int index, long value) {
            // put replaces an older entry for the same index.
            pending.put(index, value);
        }

        /**
         * Saves the pending writes under a new snapshot id.
         * Time: O(w) for w pending cells. Space: O(w) new pairs.
         * Invariant: each history gains at most one pair, with an id larger than all earlier ids.
         */
        int snap() {
            // Only cells written in this interval are visited, so unchanged cells cost nothing.
            for (Map.Entry<Integer, Long> e : pending.entrySet()) {
                int i = e.getKey();
                if (ids[i] == null) {
                    ids[i] = new int[2];
                    vals[i] = new long[2];
                } else if (counts[i] == ids[i].length) {
                    // Doubling keeps appends amortized constant.
                    ids[i] = java.util.Arrays.copyOf(ids[i], counts[i] * 2);
                    vals[i] = java.util.Arrays.copyOf(vals[i], counts[i] * 2);
                }
                ids[i][counts[i]] = snaps;
                vals[i][counts[i]] = e.getValue();
                counts[i]++;
            }
            // The next interval starts with no pending writes.
            pending.clear();
            return snaps++;
        }

        /**
         * Returns the cell value at a snapshot, or -1 when the snapshot does not exist.
         * Time: O(log k). Space: O(1).
         * Invariant: the floor slot holds the latest pair with id at most snapId.
         */
        long get(int index, int snapId) {
            // A snapshot id at or beyond the counter has not been taken.
            if (snapId >= snaps) return -1;
            // A cell that never changed keeps the starting value.
            if (ids[index] == null) return start;
            int lo = 0, hi = counts[index];
            // Binary search for the first id above snapId; each step halves the window.
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (ids[index][mid] <= snapId) lo = mid + 1; else hi = mid;
            }
            // lo == 0 means every change happened after the snapshot.
            return lo == 0 ? start : vals[index][lo - 1];
        }
    }

    /** Reference: copies the whole array at every snapshot. Time: O(n) per snapshot. Space: O(n * s). */
    static final class CopyModel {
        private final long[] cur;
        private final List<long[]> copies = new ArrayList<>();
        CopyModel(int length, long start) { cur = new long[length]; java.util.Arrays.fill(cur, start); }
        void set(int i, long v) { cur[i] = v; }
        int snap() { copies.add(cur.clone()); return copies.size() - 1; }
        long get(int i, int s) { return s >= copies.size() ? -1 : copies.get(s)[i]; }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise with start value 7.
        SnapshotArray a = new SnapshotArray(3, 7);
        long[] out = new long[10];
        int k = 0;
        a.set(0, 5);
        out[k++] = a.snap();
        a.set(0, 6);
        a.set(0, 9);
        out[k++] = a.get(0, 0);
        out[k++] = a.snap();
        a.set(1, 4);
        out[k++] = a.get(1, 0);
        out[k++] = a.get(1, 1);
        out[k++] = a.get(0, 1);
        out[k++] = a.get(2, 1);
        out[k++] = a.get(0, 2);
        out[k++] = a.snap();
        out[k++] = a.get(1, 2);
        long[] want = {0, 5, 1, 7, 7, 9, 7, -1, 2, 4};
        if (!java.util.Arrays.equals(out, want)) throw new AssertionError("example 1 " + java.util.Arrays.toString(out));
        // Example 2: a read before the first snapshot returns -1, then 0 after it.
        SnapshotArray b = new SnapshotArray(1, 0);
        if (b.get(0, 0) != -1 || b.snap() != 0 || b.get(0, 0) != 0) throw new AssertionError("example 2");
        // Values near 10^12 do not overflow because the cells are long.
        SnapshotArray c = new SnapshotArray(1, 1_000_000_000_000L);
        c.set(0, 999_999_999_999L);
        c.snap();
        c.set(0, 1_000_000_000_000L);
        c.snap();
        if (c.get(0, 0) != 999_999_999_999L || c.get(0, 1) != 1_000_000_000_000L) throw new AssertionError("long values");
        // Random operation sequences are compared with the full-copy model, including unknown snapshot ids.
        Random rnd = new Random(3714L);
        for (int t = 0; t < 2500; t++) {
            int n = 1 + rnd.nextInt(5);
            long start = rnd.nextInt(4);
            SnapshotArray real = new SnapshotArray(n, start);
            CopyModel model = new CopyModel(n, start);
            for (int step = rnd.nextInt(40); step > 0; step--) {
                int op = rnd.nextInt(3);
                if (op == 0) {
                    int i = rnd.nextInt(n);
                    long v = rnd.nextInt(6);
                    real.set(i, v);
                    model.set(i, v);
                } else if (op == 1) {
                    if (real.snap() != model.snap()) throw new AssertionError("snap id");
                } else {
                    int i = rnd.nextInt(n);
                    int s = rnd.nextInt(8);
                    if (real.get(i, s) != model.get(i, s)) throw new AssertionError("get");
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Equal Versions Replace (Author exercise)
<!-- id: it37-version-histories-repeated-writes -->

**Approach.**
The class keeps the same two parallel arrays as the build exercise, and the decision lives in `set`. The method compares the new version with the last stored version. A smaller version makes the method return `false` before it writes any field. An equal version overwrites the last value and leaves the size alone. A larger version appends. The invariant is that the stored versions are strictly increasing, because equal versions never create a second pair and smaller versions never enter.

The method `get` is the same floor search as before and returns -1 when the first greater version sits at index 0. The harness uses a model that stores every accepted write in a list and answers a query by scanning from the end. It also issues many writes with repeated and decreasing versions to check that a rejected call changes neither `size` nor any answer.

**Complexity.**
- **Time** is O(1) amortized per `set` and O(log k) per `get`, where `k` is the number of stored pairs.
- **Space** is O(k), and repeated writes at one version add no space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class CoalescedIntBoundary {
    /** Version history in which a write at the last version replaces the last pair. */
    static final class CoalescedInt {
        private long[] versions = new long[2];
        private int[] values = new int[2];
        private int size;

        /**
         * Applies one write by comparing its version with the last stored version.
         * Time: O(1) amortized. Space: O(1) amortized.
         * Invariant: stored versions stay strictly increasing; a rejected call changes no field.
         */
        boolean set(long version, int value) {
            // A version below the last one is rejected before any field is written.
            if (size > 0 && version < versions[size - 1]) return false;
            // The same version replaces the last value, so the pair count does not change.
            if (size > 0 && version == versions[size - 1]) {
                values[size - 1] = value;
                return true;
            }
            // A new largest version needs room, so double the arrays when they are full.
            if (size == versions.length) {
                versions = java.util.Arrays.copyOf(versions, size * 2);
                values = java.util.Arrays.copyOf(values, size * 2);
            }
            // The append keeps the order strictly increasing.
            versions[size] = version;
            values[size] = value;
            size++;
            return true;
        }

        /**
         * Returns the value of the latest pair at or before the version, or -1.
         * Time: O(log size). Space: O(1).
         * Invariant: indices below lo hold versions at most the query.
         */
        int get(long version) {
            int lo = 0, hi = size;
            // The window halves each iteration, so the loop is logarithmic.
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (versions[mid] <= version) lo = mid + 1; else hi = mid;
            }
            // lo == 0 means the query lies before the first stored version.
            return lo == 0 ? -1 : values[lo - 1];
        }

        /** Returns the number of stored pairs. Time: O(1). Space: O(1). */
        int size() { return size; }
    }

    /** Reference: keeps the accepted writes in a list and scans from the end. Time: O(k) per query. */
    static final class Model {
        final List<long[]> pairs = new ArrayList<>();
        boolean set(long v, int x) {
            // Only a version at least the last one is accepted.
            if (!pairs.isEmpty() && v < pairs.get(pairs.size() - 1)[0]) return false;
            if (!pairs.isEmpty() && v == pairs.get(pairs.size() - 1)[0]) pairs.set(pairs.size() - 1, new long[] {v, x});
            else pairs.add(new long[] {v, x});
            return true;
        }
        int get(long v) {
            // The last pair with a version at most v wins.
            for (int i = pairs.size() - 1; i >= 0; i--) if (pairs.get(i)[0] <= v) return (int) pairs.get(i)[1];
            return -1;
        }
    }

    public static void main(String[] args) {
        // Example 1: the equal version replaces, and the write at version 5 is rejected because 6 is already stored.
        CoalescedInt a = new CoalescedInt();
        boolean[] ok = {a.set(4, 1), a.set(4, 2), a.set(6, 3), a.set(5, 9)};
        if (!ok[0] || !ok[1] || !ok[2] || ok[3]) throw new AssertionError("example 1 flags");
        if (a.size() != 2 || a.get(4) != 2 || a.get(5) != 2 || a.get(3) != -1) throw new AssertionError("example 1");
        // Example 2: two writes at version 0 leave one pair holding 6.
        CoalescedInt b = new CoalescedInt();
        b.set(0, 5);
        b.set(0, 6);
        if (b.get(0) != 6 || b.size() != 1) throw new AssertionError("example 2");
        // A rejected call must not change size or answers.
        int before = a.size();
        a.set(0, 99);
        if (a.size() != before || a.get(6) != 3) throw new AssertionError("rejected call");
        // Random write streams with repeated and decreasing versions match the model on every query.
        Random rnd = new Random(3724L);
        for (int t = 0; t < 4000; t++) {
            CoalescedInt real = new CoalescedInt();
            Model model = new Model();
            for (int step = rnd.nextInt(25); step > 0; step--) {
                long v = rnd.nextInt(8);
                int x = rnd.nextInt(50);
                if (real.set(v, x) != model.set(v, x)) throw new AssertionError("flag");
                if (real.size() != model.pairs.size()) throw new AssertionError("size");
            }
            for (long q = 0; q <= 9; q++) if (real.get(q) != model.get(q)) throw new AssertionError("get " + q);
        }
    }
}
```

#### Solution: [Recognize] Fresh Time Based Store (LeetCode 981)
<!-- id: it37-version-histories-fresh-store -->

**Approach.**
A hash map sends each key to its own history, two parallel arrays of times and values in increasing time order. The method `set` appends to the history of its key. The method `get` finds the key's history, runs the floor search for the largest time at most the query, and then applies the freshness test. The pair is fresh when `ts - t <= ttl`. Both operands are `long`, and `ts >= t` holds for the found pair, so the subtraction cannot go negative or overflow for times up to 10^15.

The invariant is that every history is strictly increasing in time, which the contract guarantees. An unknown key, a query before the first time, and a stale pair all return the empty string. The harness compares the store with a model that scans every record ever written and keeps the one with the largest qualifying time.

**Complexity.**
- **Time** is O(1) expected per `set` and O(log k) per `get` for a key with `k` pairs, plus O(1) expected for the map lookup.
- **Space** is O(n) for `n` stored pairs across all keys.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class FreshStoreRecognize {
    /** Per-key time histories with a freshness limit on the answer. */
    static final class FreshStore {
        /** Parallel growable arrays holding one key's history. */
        private static final class Track {
            long[] times = new long[2];
            String[] values = new String[2];
            int size;
        }

        private final long ttl;
        private final Map<String, Track> tracks = new HashMap<>();

        FreshStore(long ttl) { this.ttl = ttl; }

        /**
         * Appends a pair to the history of the key.
         * Time: O(1) expected, amortized. Space: O(1) amortized.
         * Invariant: times of one key are strictly increasing because the caller sends them in order.
         */
        void set(String key, String value, long ts) {
            // computeIfAbsent creates the history on the first write of a key.
            Track t = tracks.computeIfAbsent(key, k -> new Track());
            // Doubling keeps appends amortized constant.
            if (t.size == t.times.length) {
                t.times = java.util.Arrays.copyOf(t.times, t.size * 2);
                t.values = java.util.Arrays.copyOf(t.values, t.size * 2);
            }
            t.times[t.size] = ts;
            t.values[t.size] = value;
            t.size++;
        }

        /**
         * Returns the value at the largest time at most ts when it is within ttl, or the empty string.
         * Time: O(log k). Space: O(1).
         * Invariant: slot lo - 1 holds the latest pair not after ts.
         */
        String get(String key, long ts) {
            Track t = tracks.get(key);
            // An unknown key has no history at all.
            if (t == null) return "";
            int lo = 0, hi = t.size;
            // Floor search: find the first time above ts.
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (t.times[mid] <= ts) lo = mid + 1; else hi = mid;
            }
            // lo == 0 means every pair is newer than the query.
            if (lo == 0) return "";
            // The subtraction uses long, and ts >= times[lo - 1], so the difference is not negative.
            return ts - t.times[lo - 1] <= ttl ? t.values[lo - 1] : "";
        }
    }

    /** Reference: scans all records for the largest qualifying time. Time: O(n) per query. */
    static String oracle(List<Object[]> records, long ttl, String key, long ts) {
        String best = "";
        long bestTime = -1;
        // Every record of the key is examined, so no ordering assumption is used.
        for (Object[] r : records) {
            long t = (Long) r[2];
            if (r[0].equals(key) && t <= ts && t > bestTime) { bestTime = t; best = (String) r[1]; }
        }
        // The freshness test applies to the single best record.
        return bestTime >= 0 && ts - bestTime <= ttl ? best : "";
    }

    public static void main(String[] args) {
        // Example 1 with ttl 5.
        FreshStore a = new FreshStore(5);
        a.set("a", "x", 3);
        a.set("a", "y", 10);
        String[] got = {a.get("a", 2), a.get("a", 3), a.get("a", 8), a.get("a", 9), a.get("a", 10), a.get("a", 15), a.get("a", 16), a.get("b", 1)};
        String[] want = {"", "x", "x", "", "y", "y", "", ""};
        if (!java.util.Arrays.equals(got, want)) throw new AssertionError("example 1 " + java.util.Arrays.toString(got));
        // Example 2: ttl 0 accepts only an exact time.
        FreshStore b = new FreshStore(0);
        b.set("k", "v", 4);
        if (!b.get("k", 4).equals("v") || !b.get("k", 5).isEmpty()) throw new AssertionError("example 2");
        // Times near 10^15 with a ttl of 10^15 do not overflow.
        FreshStore c = new FreshStore(1_000_000_000_000_000L);
        c.set("z", "w", 1);
        if (!c.get("z", 1_000_000_000_000_000L).equals("w")) throw new AssertionError("large times");
        // Random streams are compared with the scan on every key and many query times.
        Random rnd = new Random(3734L);
        String[] keys = {"a", "b", "c"};
        for (int t = 0; t < 2500; t++) {
            long ttl = rnd.nextInt(6);
            FreshStore real = new FreshStore(ttl);
            List<Object[]> records = new ArrayList<>();
            long[] clock = new long[3];
            for (int step = rnd.nextInt(20); step > 0; step--) {
                int ki = rnd.nextInt(3);
                // Each key's times grow strictly, as the constraints promise.
                clock[ki] += 1 + rnd.nextInt(5);
                String val = "v" + rnd.nextInt(9);
                real.set(keys[ki], val, clock[ki]);
                records.add(new Object[] {keys[ki], val, clock[ki]});
            }
            for (String key : keys) {
                for (long q = 1; q <= 40; q++) {
                    if (!real.get(key, q).equals(oracle(records, ttl, key, q))) throw new AssertionError("get " + key + " " + q);
                }
            }
        }
    }
}
```
