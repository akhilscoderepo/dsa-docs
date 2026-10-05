<!-- solutions-for: 06-binary-search -->
### Solutions For Looking Up Values By Time

#### Solution: [Build] One Key History (Author exercise)
<!-- id: bs-time-one-key -->

**Approach.**
The method finds `p`, the first position whose time is greater than `q`, with the half-open interval `[lo, hi)`. A time at most `q` moves `lo` past `mid`, and a larger time moves `hi` to `mid`. All positions below `p` have times at most `q`, and `p - 1` is the last of them. The method returns `times[p - 1]`, or `-1` when `p` is 0. The invariant is that every position below `lo` has a time at most `q` and every position at or above `hi` has a larger time.

**Complexity.**
- **Time** is O(log n), because each comparison halves the interval `[lo, hi)`.
- **Space** is O(1), because the search keeps only two indexes.

```java run
import java.util.Random;

public final class OneKeyHistory {
    /**
     * Returns the largest element of times that is at most q, or -1.
     * Time: O(log n). Space: O(1).
     * Invariant: times[i] <= q for i < lo, and times[i] > q for i >= hi.
     */
    static int latest(int[] times, int q) {
        int lo = 0, hi = times.length;
        // The interval [lo, hi) holds positions that may be the first one above q.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // A time at most q cannot be the first one above q, so lo passes it.
            if (times[mid] <= q) lo = mid + 1;
            // A time above q may be the first one above q, so hi keeps it out of the interval.
            else hi = mid;
        }
        // lo is the first position above q, so lo - 1 holds the answer when lo > 0.
        return lo == 0 ? -1 : times[lo - 1];
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] t = {2, 5, 9, 14, 20};
        if (latest(t, 12) != 9) throw new AssertionError("example 1");
        if (latest(t, 1) != -1) throw new AssertionError("example 2");
        // A query equal to the last element and one far beyond it.
        if (latest(t, 20) != 20 || latest(t, 1_000_000_000) != 20) throw new AssertionError("after last");
        // Random sorted arrays against a scan.
        Random rnd = new Random(101);
        for (int k = 0; k < 4000; k++) {
            int n = 1 + rnd.nextInt(12), v = rnd.nextInt(3);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = v += 1 + rnd.nextInt(4);
            int q = rnd.nextInt(v + 5), expect = -1;
            for (int x : a) if (x <= q) expect = x;
            if (latest(a, q) != expect) throw new AssertionError("random " + java.util.Arrays.toString(a) + " " + q);
        }
    }
}
```

#### Solution: [Vary] Time Based Key-Value Store (LeetCode 981)
<!-- id: bs-time-key-value-store -->

**Approach.**
A `HashMap` from key to history list selects the entries of one key, so no query reads the entries of another key. Each `set` appends to the list of its key. Times increase for each key, so each list stays sorted without extra work. Each `get` fetches the list and runs the floor search of the previous exercise. An unknown key has no list, and the method returns the empty string. A search that ends with `p = 0` also returns the empty string. The invariant is that each list is sorted by time and holds exactly the changes of its key.

**Complexity.**
- **Time** is O(1) amortized per `set` and O(log h) per `get` for a history of `h` entries, plus the expected O(1) map lookup.
- **Space** is O(n) for `n` stored changes, because each change appears once in a list.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public final class TimeKeyValueStore {
    /** Store with one sorted history list per key. */
    static final class Store {
        private final HashMap<String, ArrayList<Integer>> times = new HashMap<>();
        private final HashMap<String, ArrayList<String>> values = new HashMap<>();

        /** Appends a change; Time O(1) amortized, Space O(1). Times increase per key. */
        void set(String key, String value, int time) {
            times.computeIfAbsent(key, k -> new ArrayList<>()).add(time);
            values.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
        }

        /** Returns the value at the last time at most the query; Time O(log h), Space O(1). */
        String get(String key, int time) {
            ArrayList<Integer> ts = times.get(key);
            // An unknown key has no list, so the empty answer applies.
            if (ts == null) return "";
            int lo = 0, hi = ts.size();
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                // A time at most the query moves lo past mid.
                if (ts.get(mid) <= time) lo = mid + 1; else hi = mid;
            }
            // lo == 0 means every change is later than the query.
            return lo == 0 ? "" : values.get(key).get(lo - 1);
        }
    }

    public static void main(String[] args) {
        // The statement example.
        Store s = new Store();
        s.set("a", "x", 3); s.set("a", "y", 8); s.set("b", "z", 5);
        String[] got = {s.get("a", 2), s.get("a", 3), s.get("a", 7), s.get("a", 9), s.get("b", 5), s.get("c", 5)};
        String[] want = {"", "x", "x", "y", "z", ""};
        if (!java.util.Arrays.equals(got, want)) throw new AssertionError("example 1 " + java.util.Arrays.toString(got));
        Store one = new Store();
        one.set("k", "v", 1);
        if (!one.get("k", 1000).equals("v")) throw new AssertionError("example 2");
        // Random operations against a scan over all stored changes.
        Random rnd = new Random(102);
        for (int t = 0; t < 1500; t++) {
            Store st = new Store();
            HashMap<String, ArrayList<int[]>> oracle = new HashMap<>();
            ArrayList<String> vals = new ArrayList<>();
            int[] clock = new int[3];
            for (int op = 0; op < 40; op++) {
                String key = "k" + rnd.nextInt(3);
                int ki = key.charAt(1) - '0';
                if (rnd.nextBoolean()) {
                    clock[ki] += 1 + rnd.nextInt(3);
                    String v = "v" + vals.size();
                    vals.add(v);
                    st.set(key, v, clock[ki]);
                    oracle.computeIfAbsent(key, z -> new ArrayList<>()).add(new int[]{clock[ki], vals.size() - 1});
                } else {
                    int q = rnd.nextInt(clock[ki] + 4);
                    String expect = "";
                    for (int[] e : oracle.getOrDefault(key, new ArrayList<>())) if (e[0] <= q) expect = vals.get(e[1]);
                    if (!st.get(key, q).equals(expect)) throw new AssertionError("random " + key + " " + q);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Early Query (Author exercise)
<!-- id: bs-time-early-query -->

**Approach.**
The method finds `p`, the first position with a time above `q`, and returns `p - 1`. If `q` is below every element, then `p` is 0 and the result is -1, so the method reads no element at an invalid position. If `q` equals an element, then that element does not pass `q`, so `p` lies after it and the result is its own position. If `q` is above every element, then `p` equals the length and the result is the last position. The invariant of the half-open interval `[lo, hi)` is the same as in the first exercise.

**Complexity.**
- **Time** is O(log n), because each comparison halves the interval.
- **Space** is O(1), because the method keeps two indexes.

```java run
import java.util.Random;

public final class EarlyQuery {
    /**
     * Returns the position of the largest element at most q, or -1.
     * Time: O(log n). Space: O(1).
     * Invariant: times[i] <= q for i < lo, and times[i] > q for i >= hi.
     */
    static int floorIndex(int[] times, int q) {
        int lo = 0, hi = times.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // An element at most q moves lo past it, including an element equal to q.
            if (times[mid] <= q) lo = mid + 1; else hi = mid;
        }
        // lo - 1 is -1 exactly when q is smaller than every element.
        return lo - 1;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] t = {4, 7, 10};
        if (floorIndex(t, 3) != -1) throw new AssertionError("example 1");
        if (floorIndex(t, 10) != 2) throw new AssertionError("example 2");
        // Equal to the first element, between two, and after the last.
        if (floorIndex(t, 4) != 0 || floorIndex(t, 5) != 0 || floorIndex(t, 99) != 2) throw new AssertionError("edges");
        // A single element before and on the query.
        if (floorIndex(new int[]{6}, 5) != -1 || floorIndex(new int[]{6}, 6) != 0) throw new AssertionError("single");
        // Random arrays against a scan.
        Random rnd = new Random(103);
        for (int k = 0; k < 4000; k++) {
            int n = 1 + rnd.nextInt(10), v = rnd.nextInt(3);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = v += 1 + rnd.nextInt(4);
            int q = rnd.nextInt(v + 5), expect = -1;
            for (int i = 0; i < n; i++) if (a[i] <= q) expect = i;
            if (floorIndex(a, q) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Snapshot Array (LeetCode 1146)
<!-- id: bs-time-snapshot-array -->

**Approach.**
Each index owns a history list of snapshot identifiers and values, and the structure stores one entry per `set` and not one copy of the array per snapshot. A `set` during snapshot `s` replaces the last entry of its index when that entry carries identifier `s`, and otherwise appends a new entry. A `snap` only increments the identifier. A `get(index, id)` runs a floor search for the last entry with an identifier at most `id`, and it returns 0 when none exists. The invariant is that identifiers in each list increase strictly, so the floor search is valid.

**Complexity.**
- **Time** is O(1) amortized for `set`, O(1) for `snap` and O(log h) for `get`, for `h` entries at one index.
- **Space** is O(m) for `m` calls of `set`, because each call adds at most one entry.

```java run
import java.util.ArrayList;
import java.util.Random;

public final class SnapshotArrayLookup {
    /** Array with one history list per index. */
    static final class Snap {
        private final ArrayList<Integer>[] ids;
        private final ArrayList<Integer>[] vals;
        private int current = 0;

        @SuppressWarnings("unchecked")
        Snap(int length) {
            ids = new ArrayList[length];
            vals = new ArrayList[length];
            for (int i = 0; i < length; i++) { ids[i] = new ArrayList<>(); vals[i] = new ArrayList<>(); }
        }

        /** Writes a value in the current snapshot; Time O(1) amortized, Space O(1). */
        void set(int index, int val) {
            ArrayList<Integer> a = ids[index];
            // A second write in the same snapshot replaces the last entry.
            if (!a.isEmpty() && a.get(a.size() - 1) == current) vals[index].set(a.size() - 1, val);
            else { a.add(current); vals[index].add(val); }
        }

        /** Saves the state and returns its identifier; Time O(1), Space O(1). */
        int snap() { return current++; }

        /** Returns the value at snapshot id; Time O(log h), Space O(1). */
        int get(int index, int id) {
            ArrayList<Integer> a = ids[index];
            int lo = 0, hi = a.size();
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                // An entry saved at or before the identifier moves lo past it.
                if (a.get(mid) <= id) lo = mid + 1; else hi = mid;
            }
            // No entry at or before the identifier means the element still had its initial value 0.
            return lo == 0 ? 0 : vals[index].get(lo - 1);
        }
    }

    public static void main(String[] args) {
        // The statement examples.
        Snap s = new Snap(3);
        s.set(0, 5);
        int[] got = new int[6];
        got[0] = s.snap();
        s.set(0, 6);
        got[1] = s.get(0, 0);
        got[2] = s.snap();
        s.set(1, 4);
        got[3] = s.get(1, 0); got[4] = s.get(1, 1); got[5] = s.get(0, 1);
        if (!java.util.Arrays.equals(got, new int[]{0, 5, 1, 0, 0, 6})) throw new AssertionError("example 1 " + java.util.Arrays.toString(got));
        Snap one = new Snap(1);
        if (one.snap() != 0 || one.get(0, 0) != 0) throw new AssertionError("example 2");
        // Random operations against full copies of the array at every snapshot.
        Random rnd = new Random(104);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(4);
            Snap sn = new Snap(n);
            int[] cur = new int[n];
            ArrayList<int[]> copies = new ArrayList<>();
            for (int op = 0; op < 40; op++) {
                int c = rnd.nextInt(3);
                if (c == 0) { int i = rnd.nextInt(n), v = rnd.nextInt(100); sn.set(i, v); cur[i] = v; }
                else if (c == 1) { if (sn.snap() != copies.size()) throw new AssertionError("id"); copies.add(cur.clone()); }
                else if (!copies.isEmpty()) {
                    int id = rnd.nextInt(copies.size()), i = rnd.nextInt(n);
                    if (sn.get(i, id) != copies.get(id)[i]) throw new AssertionError("random get");
                }
            }
        }
    }
}
```
