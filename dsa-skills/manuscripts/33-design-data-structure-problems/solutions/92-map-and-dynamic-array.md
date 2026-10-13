<!-- solutions-for: 92-map-and-dynamic-array -->
### Solutions For Slots In An Array

#### Solution: [Build] Remove By Swap (Author exercise)
<!-- id: ds-remove-by-swap -->

**Approach.** The list `items` stays dense, so a removal must not leave a hole. The method reads the removed value's index from `slotOf`, copies the last element into that index and deletes the last list position. That copy changes the index of exactly one value, the moved one, so the method rewrites its map entry. The method then deletes the removed key. Agreement holds before the call and after it, which is why a check method can run after every operation. The method calls `list.remove(list.size() - 1)` with an `int` argument, so Java deletes by index. A call with an `Integer` argument would search by value instead, and the assertions in `main` cover the index overload.

**Complexity.**

- **Time** is O(1) expected per call, because one map lookup, one list write, one map write and one map delete each cost constant time.
- **Space** is O(1) extra per call, because the method stores two integers and the structure itself holds O(n).

```java run
import java.util.*;

public final class RemoveBySwap {
    static final class Pool {
        final ArrayList<Integer> items = new ArrayList<>();
        final HashMap<Integer, Integer> slotOf = new HashMap<>();

        /**
         * Appends value when absent. Time: O(1) amortized. Space: O(1).
         * Invariant: slotOf.get(items.get(i)) == i for every i.
         */
        boolean insert(int value) {
            // A present value is rejected in O(1) by the map.
            if (slotOf.containsKey(value)) return false;
            // The new value takes index size, which the map records.
            slotOf.put(value, items.size());
            items.add(value);
            return true;
        }

        /**
         * Removes value by moving the last element into its index.
         * Time: O(1) expected. Space: O(1). Invariant: agreement holds on exit.
         */
        boolean remove(int value) {
            // One map lookup finds the index of the removed value.
            Integer slot = slotOf.get(value);
            // An absent value leaves both structures untouched.
            if (slot == null) return false;
            // The last element is the one that fills the hole.
            int lastIndex = items.size() - 1;
            int moved = items.get(lastIndex);
            // Overwrite the hole; for the last index this writes the value onto itself.
            items.set(slot, moved);
            // The moved value now lives at the vacated index.
            slotOf.put(moved, slot);
            // The removed key must go last, so a self-move still ends deleted.
            slotOf.remove(value);
            // int argument: removes by index and shifts nothing, since it is the final position.
            items.remove(lastIndex);
            return true;
        }

        /** Checks agreement: each index maps back to itself and sizes match. */
        boolean agrees() {
            // The map holds exactly one entry per list element.
            if (slotOf.size() != items.size()) return false;
            // Every element's recorded slot equals its real index.
            for (int i = 0; i < items.size(); i++) {
                Integer s = slotOf.get(items.get(i));
                if (s == null || s != i) return false;
            }
            return true;
        }
    }

    static void check(boolean ok, String msg) { if (!ok) throw new AssertionError(msg); }

    public static void main(String[] args) {
        // Example 1: insert 5, 8, 2, 9, then remove 8.
        Pool p = new Pool();
        for (int v : new int[]{5, 8, 2, 9}) check(p.insert(v) && p.agrees(), "insert");
        check(p.remove(8) && p.agrees(), "remove 8");
        check(p.items.equals(List.of(5, 9, 2)), "items after remove 8");
        check(p.slotOf.get(5) == 0 && p.slotOf.get(9) == 1 && p.slotOf.get(2) == 2, "slots");
        // Example 2: a missing value changes nothing, then remove 5.
        check(!p.remove(7) && p.items.equals(List.of(5, 9, 2)) && p.agrees(), "remove absent");
        check(p.remove(5) && p.items.equals(List.of(2, 9)) && p.agrees(), "remove 5");
        // The int overload removes by index even when the value equals an index.
        Pool q = new Pool();
        q.insert(0); q.insert(1); q.insert(2);
        check(q.remove(0) && q.items.equals(List.of(2, 1)) && q.agrees(), "index overload");
        // Random scripts against a plain list model, with agreement checked after every call.
        Random rnd = new Random(33);
        for (int round = 0; round < 300; round++) {
            Pool pool = new Pool();
            ArrayList<Integer> model = new ArrayList<>();
            for (int step = 0; step < 80; step++) {
                int v = rnd.nextInt(12);
                if (rnd.nextBoolean()) {
                    boolean expect = !model.contains(v);
                    if (expect) model.add(v);
                    check(pool.insert(v) == expect, "insert result");
                } else {
                    boolean expect = model.remove(Integer.valueOf(v));
                    check(pool.remove(v) == expect, "remove result");
                }
                check(pool.agrees(), "agreement");
                ArrayList<Integer> a = new ArrayList<>(pool.items), b = new ArrayList<>(model);
                Collections.sort(a); Collections.sort(b);
                check(a.equals(b), "same members");
            }
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Insert Delete GetRandom O(1) With A Different Pick (LeetCode 380)
<!-- id: ds-random-excluding -->

**Approach.** Let `s` be the excluded value's index when the value is present. The qualifying values then occupy every index except `s`, which is `size - 1` indices. The method draws one integer `r` uniformly from `0..size-2`. When `r` differs from `s` it returns `items[r]`. When `r` equals `s` it returns `items[size-1]`, the one index that the range `0..size-2` can never reach when `s` is smaller than `size - 1`. Each qualifying index is then returned by exactly one draw value, so the pick is uniform. When `s` equals `size - 1` the draw never equals `s`, and the pick is also uniform. When the value is absent the method draws from `0..size-1`. A size of 0, or a size of 1 holding the excluded value, returns `-1`. The method draws once and has no loop, so the worst case is constant.

**Complexity.**

- **Time** is O(1) expected, from one map lookup, one random draw and one array read, with no redraw loop.
- **Space** is O(1) extra, because the method stores the index and the drawn integer.

```java run
import java.util.*;

public final class RandomExcluding {
    static final class Pool {
        int[] items = new int[2];
        int size = 0;
        final HashMap<Integer, Integer> slotOf = new HashMap<>();
        final Random rng;

        Pool(long seed) { rng = new Random(seed); }

        boolean insert(int v) {
            if (slotOf.containsKey(v)) return false;
            if (size == items.length) items = Arrays.copyOf(items, size * 2);
            items[size] = v;
            slotOf.put(v, size++);
            return true;
        }

        boolean remove(int v) {
            Integer s = slotOf.get(v);
            if (s == null) return false;
            int last = items[--size];
            items[s] = last;
            slotOf.put(last, s);
            slotOf.remove(v);
            return true;
        }

        /** Number of draw values for the excluded value; each draw value maps to one result. */
        int drawRange(int value) {
            // A present value removes one qualifying index; an absent value removes none.
            return slotOf.containsKey(value) ? size - 1 : size;
        }

        /** Maps a draw r in [0, drawRange) to a value; this is the whole pick, split out for exact checks. */
        int valueForDraw(int value, int r) {
            Integer s = slotOf.get(value);
            // Absent value: every index qualifies, so the draw is the index.
            if (s == null) return items[r];
            // The draw hit the excluded index: redirect to the last index, which the range never reaches.
            return r == s ? items[size - 1] : items[r];
        }

        /**
         * Uniform value different from value, or -1 when none exists.
         * Time: O(1) expected, from the map lookup. Space: O(1). Reads state only.
         */
        int getRandomExcluding(int value) {
            int range = drawRange(value);
            // No qualifying value: empty pool, or the only value is the excluded one.
            if (range == 0) return -1;
            // Exactly one draw, so there is no loop and the cost stays constant after the lookup.
            return valueForDraw(value, rng.nextInt(range));
        }
    }

    static void check(boolean ok, String msg) { if (!ok) throw new AssertionError(msg); }

    public static void main(String[] args) {
        // Example 1: the pool 3, 6, 9 excluding 6 offers 3 and 9 once each across all draws.
        Pool p = new Pool(1);
        p.insert(3); p.insert(6); p.insert(9);
        check(p.drawRange(6) == 2, "range");
        TreeSet<Integer> seen = new TreeSet<>();
        for (int r = 0; r < p.drawRange(6); r++) check(seen.add(p.valueForDraw(6, r)), "duplicate result");
        check(seen.equals(new TreeSet<>(List.of(3, 9))), "example 1");
        // Example 2: a one-element pool excluding its only value returns -1.
        Pool one = new Pool(2);
        one.insert(4);
        check(one.getRandomExcluding(4) == -1, "example 2");
        check(one.getRandomExcluding(5) == 4, "absent value in one-element pool");
        check(new Pool(3).getRandomExcluding(1) == -1, "empty pool");
        // Random scripts: the exact set of results over all draws equals the model's qualifying values.
        Random rnd = new Random(380);
        for (int round = 0; round < 300; round++) {
            Pool pool = new Pool(round);
            ArrayList<Integer> model = new ArrayList<>();
            for (int step = 0; step < 60; step++) {
                int v = rnd.nextInt(10);
                if (rnd.nextInt(3) > 0) { if (pool.insert(v)) model.add(v); }
                else { if (pool.remove(v)) model.remove(Integer.valueOf(v)); }
                int ex = rnd.nextInt(11);
                ArrayList<Integer> want = new ArrayList<>();
                for (int m : model) if (m != ex) want.add(m);
                Collections.sort(want);
                ArrayList<Integer> got = new ArrayList<>();
                // Enumerating every draw value proves each qualifying value appears exactly once.
                for (int r = 0; r < pool.drawRange(ex); r++) got.add(pool.valueForDraw(ex, r));
                Collections.sort(got);
                check(got.equals(want), "uniform support");
                int pick = pool.getRandomExcluding(ex);
                check(want.isEmpty() ? pick == -1 : want.contains(pick), "pick membership");
            }
        }
        // Sampled frequencies stay near uniform for a fixed seed.
        Pool f = new Pool(99);
        for (int v : new int[]{10, 20, 30, 40}) f.insert(v);
        int[] counts = new int[4];
        for (int i = 0; i < 30000; i++) {
            int x = f.getRandomExcluding(20);
            check(x != 20 && x != -1, "excluded value returned");
            counts[x / 10 - 1]++;
        }
        check(counts[1] == 0, "excluded count");
        for (int idx : new int[]{0, 2, 3}) check(Math.abs(counts[idx] - 10000) < 500, "frequency " + counts[idx]);
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Last-Slot Removal (Author exercise)
<!-- id: ds-last-slot-removal -->

**Approach.** When the removed value sits at index `size - 1`, the moved value is the removed value. The repair `slotOf.put(moved, slot)` then targets the key about to be deleted. If the key deletion runs first and the repair second, the repair inserts the deleted key again, and the map holds one entry more than the array holds elements. The correct order repairs first and deletes second, so the final state has no entry for the removed key. A one-element pool is the same case with `size - 1` equal to 0. The method then ends with `size = 0` and an empty map. The solution also includes the faulty order, and the assertions show that the agreement check catches it.

**Complexity.**

- **Time** is O(1) expected, because the order of two map updates adds no extra work.
- **Space** is O(1) extra, because no temporary collection is created.

```java run
import java.util.*;

public final class LastSlotRemoval {
    static final class Pool {
        int[] items = new int[4];
        int size = 0;
        final HashMap<Integer, Integer> slotOf = new HashMap<>();

        void insert(int v) {
            if (slotOf.containsKey(v)) return;
            if (size == items.length) items = Arrays.copyOf(items, size * 2);
            items[size] = v;
            slotOf.put(v, size++);
        }

        /**
         * Correct order: repair the moved value, then delete the removed key.
         * Time: O(1) expected. Space: O(1). Invariant: agreement holds on exit.
         */
        boolean remove(int v) {
            Integer s = slotOf.get(v);
            if (s == null) return false;
            // When s == size - 1 this reads v itself: moved and removed values are identical.
            int moved = items[size - 1];
            items[s] = moved;
            // Repair first; for a self-move this writes a key that the next line deletes.
            slotOf.put(moved, s);
            slotOf.remove(v);
            size--;
            return true;
        }

        /** Faulty order kept for contrast: the repair resurrects a deleted key on a self-move. */
        boolean removeWrongOrder(int v) {
            Integer s = slotOf.get(v);
            if (s == null) return false;
            int moved = items[size - 1];
            items[s] = moved;
            slotOf.remove(v);
            slotOf.put(moved, s);
            size--;
            return true;
        }

        boolean agrees() {
            if (slotOf.size() != size) return false;
            for (int i = 0; i < size; i++) {
                Integer s = slotOf.get(items[i]);
                if (s == null || s != i) return false;
            }
            return true;
        }

        List<Integer> view() {
            ArrayList<Integer> out = new ArrayList<>();
            for (int i = 0; i < size; i++) out.add(items[i]);
            return out;
        }
    }

    static void check(boolean ok, String msg) { if (!ok) throw new AssertionError(msg); }

    public static void main(String[] args) {
        // Example 1: remove the last of 4, 7, 1.
        Pool p = new Pool();
        for (int v : new int[]{4, 7, 1}) p.insert(v);
        check(p.remove(1) && p.view().equals(List.of(4, 7)) && p.agrees(), "example 1");
        check(p.slotOf.keySet().equals(Set.of(4, 7)), "map keys");
        // Example 2: remove the only element.
        Pool one = new Pool();
        one.insert(6);
        check(one.remove(6) && one.size == 0 && one.slotOf.isEmpty() && one.agrees(), "example 2");
        // The faulty order leaves a ghost key, and the agreement check detects it.
        Pool bad = new Pool();
        for (int v : new int[]{4, 7, 1}) bad.insert(v);
        bad.removeWrongOrder(1);
        check(bad.slotOf.containsKey(1) && !bad.agrees(), "faulty order must be caught");
        // Random scripts that favor last-slot removals, against a list model.
        Random rnd = new Random(92);
        for (int round = 0; round < 400; round++) {
            Pool pool = new Pool();
            ArrayList<Integer> model = new ArrayList<>();
            for (int step = 0; step < 60; step++) {
                if (rnd.nextInt(3) > 0 || model.isEmpty()) {
                    int v = rnd.nextInt(15);
                    if (!model.contains(v)) model.add(v);
                    pool.insert(v);
                } else {
                    // Half the removals target the newest element, which sits at the last index.
                    int v = rnd.nextBoolean() ? pool.items[pool.size - 1] : model.get(rnd.nextInt(model.size()));
                    model.remove(Integer.valueOf(v));
                    check(pool.remove(v), "remove present");
                }
                check(pool.agrees(), "agreement");
                ArrayList<Integer> a = new ArrayList<>(pool.view()), b = new ArrayList<>(model);
                Collections.sort(a); Collections.sort(b);
                check(a.equals(b), "members");
            }
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Duplicate Values Pool (LeetCode 381)
<!-- id: ds-duplicate-values -->

**Approach.** The array `items` holds one entry per occurrence, so a uniform index draw already picks each value with probability equal to its multiplicity divided by `size`. Each value owns a record with a growing `int[]` of the array indices where it occurs. The array `posInList` stores, for each array index, the position of that index inside its value's list. Removal detaches the last entry of the value's list, which names the array index `s`, and costs O(1). The last array index `m` then fills `s`. The moved value's list entry at `posInList[m]` is rewritten to `s`, and `posInList[s]` takes that position. When the moved value equals the removed value, its entry sits inside the same list, below the shrunken count, so the same two writes stay correct. An empty list deletes the map key, and `insert` returns `true` only when the key was absent.

**Complexity.**

- **Time** is O(1) expected per operation, with array doubling amortized, because every step is a map lookup or an indexed write.
- **Space** is O(n) for the array, the position array and the lists, since every occurrence owns one entry in each.

```java run
import java.util.*;

public final class DuplicateValuesPool {
    static final class Slots {
        int[] idx = new int[2];
        int n = 0;
        void add(int i) {
            // Doubling keeps appends amortized O(1).
            if (n == idx.length) idx = Arrays.copyOf(idx, n * 2);
            idx[n++] = i;
        }
    }

    static final class Pool {
        int[] items = new int[2];
        int[] posInList = new int[2];
        int size = 0;
        final HashMap<Integer, Slots> map = new HashMap<>();
        final Random rng;

        Pool(long seed) { rng = new Random(seed); }

        /**
         * Adds one occurrence; true when the value was absent. Time O(1) amortized. Space O(1) extra.
         * Invariant: items[map.get(v).idx[p]] == v and posInList[idx[p]] == p.
         */
        boolean insert(int v) {
            if (size == items.length) {
                items = Arrays.copyOf(items, size * 2);
                posInList = Arrays.copyOf(posInList, size * 2);
            }
            Slots list = map.get(v);
            boolean fresh = list == null;
            if (fresh) { list = new Slots(); map.put(v, list); }
            // The new occurrence takes array index size and the next list position.
            items[size] = v;
            posInList[size] = list.n;
            list.add(size);
            size++;
            return fresh;
        }

        /** Removes one occurrence. Time O(1) expected. Space O(1). */
        boolean remove(int v) {
            Slots list = map.get(v);
            if (list == null) return false;
            // The last list entry names the array index to vacate, so detaching it is O(1).
            int s = list.idx[--list.n];
            int m = size - 1;
            if (s != m) {
                // The last array element moves into s; its list entry must now name s.
                Slots other = map.get(items[m]);
                int p = posInList[m];
                other.idx[p] = s;
                posInList[s] = p;
                items[s] = items[m];
            }
            size--;
            // An exhausted list removes the key, so countOf reports 0.
            if (list.n == 0) map.remove(v);
            return true;
        }

        int countOf(int v) { Slots l = map.get(v); return l == null ? 0 : l.n; }

        /** Value drawn with probability count/size. Time O(1). Throws IllegalStateException when empty. */
        int getRandom() {
            if (size == 0) throw new IllegalStateException("empty pool");   // an empty pool has nothing to draw
            return items[rng.nextInt(size)];
        }

        boolean agrees() {
            int total = 0;
            for (Map.Entry<Integer, Slots> e : map.entrySet()) {
                Slots l = e.getValue();
                if (l.n == 0) return false;
                total += l.n;
                for (int p = 0; p < l.n; p++) {
                    int i = l.idx[p];
                    if (i < 0 || i >= size || items[i] != e.getKey() || posInList[i] != p) return false;
                }
            }
            return total == size;
        }
    }

    static void check(boolean ok, String msg) { if (!ok) throw new AssertionError(msg); }

    public static void main(String[] args) {
        // Example 1: insert 3, 3, 8.
        Pool p = new Pool(5);
        // An empty pool throws IllegalStateException on getRandom.
        try { p.getRandom(); throw new AssertionError("empty getRandom must throw"); }
        catch (IllegalStateException expected) { }
        check(p.insert(3) && !p.insert(3) && p.insert(8), "inserts");
        check(p.countOf(3) == 2 && p.countOf(8) == 1 && p.agrees(), "counts");
        int threes = 0, draws = 30000;
        for (int i = 0; i < draws; i++) if (p.getRandom() == 3) threes++;
        check(Math.abs(threes - draws * 2 / 3) < 600, "proportional draw " + threes);
        // Example 2: remove one 3, then a missing 5.
        check(p.remove(3) && p.countOf(3) == 1 && p.agrees(), "remove 3");
        check(!p.remove(5) && p.agrees(), "remove 5");
        // Random scripts against a list model, checking counts and structure after each call.
        Random rnd = new Random(381);
        for (int round = 0; round < 400; round++) {
            Pool pool = new Pool(round);
            ArrayList<Integer> model = new ArrayList<>();
            for (int step = 0; step < 80; step++) {
                int v = rnd.nextInt(6);
                if (rnd.nextInt(5) < 3) {
                    boolean fresh = !model.contains(v);
                    model.add(v);
                    check(pool.insert(v) == fresh, "insert result");
                } else {
                    boolean had = model.remove(Integer.valueOf(v));
                    check(pool.remove(v) == had, "remove result");
                }
                check(pool.agrees(), "structure");
                check(pool.size == model.size(), "size");
                for (int x = 0; x < 6; x++) check(pool.countOf(x) == Collections.frequency(model, x), "count " + x);
            }
        }
        System.out.println("ok");
    }
}
```
