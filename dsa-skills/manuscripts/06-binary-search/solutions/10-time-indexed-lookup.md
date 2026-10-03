<!-- solutions-for: 06-time-indexed-lookup -->
### Time Indexed Lookup

#### Solution: [Build] One Key History (Author exercise)
<!-- id: bs-one-key-history -->

**Approach.** The times are strictly increasing, so the changes at or before the query are a prefix of the list. The upper bound is the first position with a time greater than the query, found with `hi` starting at the length, `times[mid] <= query` sending `lo` to `mid + 1`, and anything else sending `hi` to `mid`. The latest change not after the query is one position before the upper bound, and it does not exist when the upper bound is zero, so minus one is returned. The oracle scans for the last time that is at most the query.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;

public final class OneKeyHistory {
    static int latestNotAfter(int[] times, int query) {
        int lo = 0, hi = times.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (times[mid] <= query) lo = mid + 1;
            else hi = mid;
        }
        return lo - 1;
    }
    static int oracle(int[] times, int query) {
        int best = -1;
        for (int i = 0; i < times.length; i++) if (times[i] <= query) best = i;
        return best;
    }

    public static void main(String[] args) {
        int[] ex = {2, 5, 9, 14};
        if (latestNotAfter(ex, 10) != 2) throw new AssertionError("example 1");
        if (latestNotAfter(ex, 14) != 3) throw new AssertionError("example 2");
        if (latestNotAfter(ex, 1) != -1) throw new AssertionError("early query");
        if (latestNotAfter(new int[0], 5) != -1) throw new AssertionError("empty history");
        Random rnd = new Random(701);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(10);
            int[] times = new int[n];
            int cur = rnd.nextInt(5);
            for (int i = 0; i < n; i++) { times[i] = cur; cur += 1 + rnd.nextInt(4); }
            int q = rnd.nextInt(50) - 5;
            if (latestNotAfter(times, q) != oracle(times, q)) throw new AssertionError("differs for q=" + q);
        }
    }
}
```

#### Solution: [Vary] Time Based Key-Value Store (LeetCode 981)
<!-- id: bs-time-map -->

**Approach.** A hash map from key to a list of times and a second map from key to the list of values keep the entries of each key apart. Because `set` calls for one key come with increasing timestamps, appending keeps both lists sorted without any work. A `get` finds the list for the key, counts the entries whose time is at most the query with the upper-bound search, and returns the value at the position before that count, or an empty string if the count is zero or the key is unknown. The oracle stores every call in one flat list and scans it for the best entry of the key.

**Complexity.** O(1) amortized for `set`, and O(log m) for `get` over the m entries of one key, plus O(1) expected for the map lookup. Space is O(total entries).

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class TimeBasedStore {
    static final class TimeMap {
        private final Map<String, List<Integer>> times = new HashMap<>();
        private final Map<String, List<String>> values = new HashMap<>();

        void set(String key, String value, int time) {
            times.computeIfAbsent(key, k -> new ArrayList<>()).add(time);
            values.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
        }
        String get(String key, int time) {
            List<Integer> t = times.get(key);
            if (t == null) return "";
            int lo = 0, hi = t.size();
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                if (t.get(mid) <= time) lo = mid + 1;
                else hi = mid;
            }
            return lo == 0 ? "" : values.get(key).get(lo - 1);
        }
    }
    static final class Flat {
        final List<String[]> rows = new ArrayList<>();
        void set(String key, String value, int time) { rows.add(new String[] {key, value, String.valueOf(time)}); }
        String get(String key, int time) {
            String best = "";
            int bestTime = -1;
            for (String[] r : rows) {
                int tt = Integer.parseInt(r[2]);
                if (r[0].equals(key) && tt <= time && tt > bestTime) { best = r[1]; bestTime = tt; }
            }
            return best;
        }
    }

    public static void main(String[] args) {
        TimeMap m = new TimeMap();
        m.set("foo", "bar", 1);
        if (!m.get("foo", 1).equals("bar")) throw new AssertionError("example 1a");
        if (!m.get("foo", 3).equals("bar")) throw new AssertionError("example 1");
        m.set("foo", "bar2", 4);
        if (!m.get("foo", 4).equals("bar2")) throw new AssertionError("example 2");
        if (!m.get("foo", 5).equals("bar2")) throw new AssertionError("later query");
        Random rnd = new Random(702);
        for (int t = 0; t < 400; t++) {
            TimeMap a = new TimeMap();
            Flat b = new Flat();
            int[] clock = new int[3];
            for (int step = 0; step < 40; step++) {
                String key = "k" + rnd.nextInt(3);
                int id = key.charAt(1) - '0';
                if (rnd.nextBoolean()) {
                    clock[id] += 1 + rnd.nextInt(5);
                    String v = "v" + rnd.nextInt(1000);
                    a.set(key, v, clock[id]);
                    b.set(key, v, clock[id]);
                } else {
                    int q = rnd.nextInt(60);
                    if (!a.get(key, q).equals(b.get(key, q))) throw new AssertionError("differs for " + key + " at " + q);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Time Based Key-Value Store Early Query (LeetCode 981)
<!-- id: bs-time-map-early -->

**Approach.** The edge cases are the key that was never set, a query smaller than every stored time, a query equal to the first time, and a query after the last. The search handles the third and fourth correctly, since a time that is not after the query counts, and a query after the last time gives an upper bound equal to the length. The first two need explicit handling: a missing key is checked before searching, and an upper bound of zero returns the empty string before any read. The program shows that the unguarded version, which reads position `count - 1` directly, throws for an early query, and that the guarded version matches an oracle on queries ranging below the first time.

**Complexity.** O(log m) time per lookup and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class EarlyQuery {
    static int countNotAfter(List<Integer> times, int when) {
        int lo = 0, hi = times.size();
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (times.get(mid) <= when) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
    static String unguarded(Map<String, List<Integer>> times, Map<String, List<String>> values, String key, int when) {
        List<Integer> t = times.get(key);
        return values.get(key).get(countNotAfter(t, when) - 1);
    }
    static String guarded(Map<String, List<Integer>> times, Map<String, List<String>> values, String key, int when) {
        List<Integer> t = times.get(key);
        if (t == null) return "";
        int n = countNotAfter(t, when);
        if (n == 0) return "";
        return values.get(key).get(n - 1);
    }
    static String oracle(Map<String, List<Integer>> times, Map<String, List<String>> values, String key, int when) {
        List<Integer> t = times.get(key);
        String answer = "";
        if (t == null) return answer;
        for (int i = 0; i < t.size(); i++) if (t.get(i) <= when) answer = values.get(key).get(i);
        return answer;
    }

    public static void main(String[] args) {
        Map<String, List<Integer>> times = new HashMap<>();
        Map<String, List<String>> values = new HashMap<>();
        times.put("a", new ArrayList<>(List.of(5)));
        values.put("a", new ArrayList<>(List.of("x")));
        if (!guarded(times, values, "a", 4).isEmpty()) throw new AssertionError("example 1");
        if (!guarded(times, values, "a", 5).equals("x")) throw new AssertionError("equal to first");
        if (!guarded(times, values, "a", 500).equals("x")) throw new AssertionError("after last");
        if (!guarded(times, values, "b", 100).isEmpty()) throw new AssertionError("example 2");
        boolean threw = false;
        try { unguarded(times, values, "a", 4); } catch (IndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("the unguarded read should fail for an early query");
        Random rnd = new Random(703);
        for (int t = 0; t < 3000; t++) {
            List<Integer> ts = new ArrayList<>();
            List<String> vs = new ArrayList<>();
            int cur = 5 + rnd.nextInt(5);
            int n = 1 + rnd.nextInt(8);
            for (int i = 0; i < n; i++) { ts.add(cur); vs.add("v" + i); cur += 1 + rnd.nextInt(4); }
            times.put("k", ts);
            values.put("k", vs);
            int q = rnd.nextInt(50);
            if (!guarded(times, values, "k", q).equals(oracle(times, values, "k", q))) throw new AssertionError("differs for q=" + q);
        }
    }
}
```

#### Solution: [Recognize] Snapshot Array (LeetCode 1146)
<!-- id: bs-snapshot-array -->

**Approach.** Copying the array at every snapshot costs the length each time, so each index keeps only its own list of changes, each tagged with the snapshot number that was current when the value was set. The list is in increasing order of tag, because the snapshot counter only grows. If an index is set again before a snapshot, the last entry already has the current tag, so it is overwritten and the list never holds two entries with one tag. A `get` searches the list of the index for the upper bound of the requested snapshot number and returns the value one position before it, or zero if there is none. The oracle copies the whole array at each snapshot.

**Complexity.** O(1) for `set` and `snap`, and O(log c) for `get` over the c changes of one index. Space is O(number of sets plus length).

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SnapshotArrayDemo {
    static final class SnapshotArray {
        private final List<List<int[]>> changes = new ArrayList<>();
        private int nextId = 0;

        SnapshotArray(int length) {
            for (int i = 0; i < length; i++) changes.add(new ArrayList<>());
        }
        void set(int index, int value) {
            List<int[]> c = changes.get(index);
            if (!c.isEmpty() && c.get(c.size() - 1)[0] == nextId) c.get(c.size() - 1)[1] = value;
            else c.add(new int[] {nextId, value});
        }
        int snap() { return nextId++; }
        int get(int index, int snapId) {
            List<int[]> c = changes.get(index);
            int lo = 0, hi = c.size();
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                if (c.get(mid)[0] <= snapId) lo = mid + 1;
                else hi = mid;
            }
            return lo == 0 ? 0 : c.get(lo - 1)[1];
        }
    }
    static final class Copying {
        private int[] now;
        private final List<int[]> taken = new ArrayList<>();
        Copying(int length) { now = new int[length]; }
        void set(int index, int value) { now[index] = value; }
        int snap() { taken.add(now.clone()); return taken.size() - 1; }
        int get(int index, int snapId) { return taken.get(snapId)[index]; }
    }

    public static void main(String[] args) {
        SnapshotArray s = new SnapshotArray(3);
        s.set(0, 5);
        if (s.snap() != 0) throw new AssertionError("first snapshot id");
        s.set(0, 6);
        if (s.get(0, 0) != 5) throw new AssertionError("example 1");
        if (s.snap() != 1) throw new AssertionError("second snapshot id");
        if (s.get(2, 1) != 0) throw new AssertionError("example 2");
        if (s.get(0, 1) != 6) throw new AssertionError("value after second snapshot");
        Random rnd = new Random(704);
        for (int t = 0; t < 400; t++) {
            int len = 1 + rnd.nextInt(4);
            SnapshotArray a = new SnapshotArray(len);
            Copying b = new Copying(len);
            for (int step = 0; step < 60; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) { int i = rnd.nextInt(len), v = rnd.nextInt(10); a.set(i, v); b.set(i, v); }
                else if (op == 1) { if (a.snap() != b.snap()) throw new AssertionError("snapshot ids differ"); }
                else if (b.taken.size() > 0) {
                    int i = rnd.nextInt(len), id = rnd.nextInt(b.taken.size());
                    if (a.get(i, id) != b.get(i, id)) throw new AssertionError("differs at index " + i + " id " + id);
                }
            }
        }
    }
}
```

#### Solution: [Extend] Online Election (LeetCode 911)
<!-- id: bs-online-election -->

**Approach.** For each vote, keep the count of every person and the current leader, and record the leader after that vote. A new vote makes its person the leader when their count is at least the leader's count, since a tie goes to the most recent vote. The leaders then form a list aligned with the sorted times. A query asks for the latest vote at or before time `t`, found with the upper-bound search, and returns the leader recorded at the position before it. The oracle recounts all votes up to `t` on every query, giving ties to the person with the latest vote.

**Complexity.** O(n) time to build, O(log n) per query, and O(n) space.

```java run
import java.util.Random;

public final class OnlineElection {
    static final class TopVoted {
        private final int[] times;
        private final int[] leaders;

        TopVoted(int[] persons, int[] times) {
            this.times = times;
            leaders = new int[persons.length];
            int[] count = new int[persons.length + 1];
            int lead = -1;
            for (int i = 0; i < persons.length; i++) {
                count[persons[i]]++;
                if (lead == -1 || count[persons[i]] >= count[lead]) lead = persons[i];
                leaders[i] = lead;
            }
        }
        int q(int t) {
            int lo = 0, hi = times.length;
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                if (times[mid] <= t) lo = mid + 1;
                else hi = mid;
            }
            return leaders[lo - 1];
        }
    }
    static int oracle(int[] persons, int[] times, int t) {
        int[] count = new int[persons.length + 1];
        int lead = -1;
        for (int i = 0; i < persons.length && times[i] <= t; i++) {
            count[persons[i]]++;
            if (lead == -1 || count[persons[i]] >= count[lead]) lead = persons[i];
        }
        return lead;
    }

    public static void main(String[] args) {
        int[] persons = {0, 1, 1, 0, 0, 1, 0};
        int[] times = {0, 5, 10, 15, 20, 25, 30};
        TopVoted e = new TopVoted(persons, times);
        if (e.q(3) != 0) throw new AssertionError("q(3)");
        if (e.q(12) != 1) throw new AssertionError("example 1");
        if (e.q(25) != 1) throw new AssertionError("example 2");
        if (e.q(24) != 0) throw new AssertionError("q(24)");
        Random rnd = new Random(705);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] p = new int[n], ts = new int[n];
            int cur = rnd.nextInt(3);
            for (int i = 0; i < n; i++) { p[i] = rnd.nextInt(Math.min(3, n)); ts[i] = cur; cur += 1 + rnd.nextInt(3); }
            TopVoted tv = new TopVoted(p, ts);
            for (int q = ts[0]; q <= cur + 2; q++)
                if (tv.q(q) != oracle(p, ts, q)) throw new AssertionError("differs at query " + q);
        }
    }
}
```
