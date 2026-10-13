<!-- solutions-for: 05-randomized-sets -->
### Solutions For Picking A Random Value

#### Solution: [Build] Swap-With-Last Removal (Author exercise)
<!-- id: ds-swap-last-removal -->

**Approach.**

The array `values` holds exactly the current values, and the map `slotOf` stores the exact slot of each one. Insert checks the map, appends the value and records its slot. Remove reads the slot from the map and takes the last value out of the array tail. It writes that value into the freed slot, because shifting every later element would cost O(n).

Two entries then need repair. The moved value now sits in the freed slot, so its map entry changes first. The removed value has left the set, so its map entry is deleted last. The invariant is that `slotOf.get(values.get(i))` equals `i` for every slot, and the map has no other key. The random-script check below replays thousands of operations against a plain list and compares the arrays after each one.

**Complexity.**

- **Time** is O(1) expected per operation, because each call makes a constant number of hash and array-end accesses.
- **Space** is O(n) for the array and the map together, because each current value appears once in each.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public final class SwapLastRemoval {
    /** Set of ints with array storage and a value-to-slot map. */
    static final class IntPool {
        private final ArrayList<Integer> values = new ArrayList<>();
        private final HashMap<Integer, Integer> slotOf = new HashMap<>();

        /**
         * Stores val when absent.
         * Time: O(1) expected, one lookup and one append. Space: O(1) extra per stored value.
         * Invariant: slotOf.get(values.get(i)) equals i for every slot i.
         */
        boolean insert(int val) {
            // A present value changes nothing, so the false result is the whole effect.
            if (slotOf.containsKey(val)) return false;
            // The new value takes the next free slot, which is the current size.
            slotOf.put(val, values.size());
            // Append in O(1) amortized time.
            values.add(val);
            return true;
        }

        /**
         * Removes val by copying the last value into its slot.
         * Time: O(1) expected, a fixed number of map and array-end accesses. Space: O(1).
         * Invariant: afterward every slot and every map entry agree again.
         */
        boolean remove(int val) {
            // Look up the slot of the value to delete.
            Integer slot = slotOf.get(val);
            // An absent value means there is nothing to repair.
            if (slot == null) return false;
            // The last value fills the freed slot.
            int last = values.get(values.size() - 1);
            // Overwrite the removed value with the last value.
            values.set(slot, last);
            // Repair the moved value's entry before deleting anything.
            slotOf.put(last, slot);
            // The int argument selects remove(int), which deletes the last position in O(1).
            values.remove(values.size() - 1);
            // Delete the removed value's entry last, so it stays deleted even when it was the last value.
            slotOf.remove(val);
            return true;
        }

        boolean contains(int val) { return slotOf.containsKey(val); }

        List<Integer> snapshot() { return new ArrayList<>(values); }

        /** Checks the invariant: each slot is named by its value's entry and no other key exists. */
        void check() {
            // Every slot must be found through the map.
            for (int i = 0; i < values.size(); i++) {
                if (slotOf.get(values.get(i)) != i) throw new AssertionError("slot mismatch at " + i);
            }
            // The map has exactly one entry per slot.
            if (slotOf.size() != values.size()) throw new AssertionError("map size differs from array size");
        }
    }

    public static void main(String[] args) {
        // Example 1: removing 8 from [5, 8, 2, 9] moves 9 into slot 1.
        IntPool pool = new IntPool();
        for (int v : new int[] {5, 8, 2, 9}) pool.insert(v);
        if (!pool.remove(8)) throw new AssertionError("remove of a present value");
        if (!pool.snapshot().equals(List.of(5, 9, 2))) throw new AssertionError("example 1 array");
        pool.check();
        if (pool.contains(8)) throw new AssertionError("8 is gone");
        // Example 2: removing an absent value changes nothing.
        IntPool other = new IntPool();
        for (int v : new int[] {5, 8, 2, 9}) other.insert(v);
        if (other.remove(4)) throw new AssertionError("absent value");
        if (!other.snapshot().equals(List.of(5, 8, 2, 9))) throw new AssertionError("example 2 unchanged");
        // Random scripts: replay against a plain list that also swaps with the last element.
        Random rnd = new Random(33_051);
        for (int round = 0; round < 300; round++) {
            IntPool p = new IntPool();
            ArrayList<Integer> model = new ArrayList<>();
            for (int step = 0; step < 60; step++) {
                int v = rnd.nextInt(12) - 3;
                if (rnd.nextBoolean()) {
                    // Insert expectation: true exactly when the model lacks v.
                    boolean expect = !model.contains(v);
                    if (p.insert(v) != expect) throw new AssertionError("insert result");
                    if (expect) model.add(v);
                } else {
                    // indexOf(Object) scans the model in O(n), which is fine for an oracle.
                    int at = model.indexOf(v);
                    if (p.remove(v) != (at >= 0)) throw new AssertionError("remove result");
                    if (at >= 0) {
                        model.set(at, model.get(model.size() - 1));
                        model.remove(model.size() - 1);
                    }
                }
                // After every operation the arrays match and the invariant holds.
                if (!p.snapshot().equals(model)) throw new AssertionError("array differs from model");
                p.check();
            }
        }
    }
}
```

#### Solution: [Vary] Insert Delete GetRandom O(1) (LeetCode 380)
<!-- id: ds-random-pick-injected -->

**Approach.**

The structure is the array plus value-to-slot map from the previous exercise. The contract changes in two places. First, `getRandom` receives the random source as an argument instead of owning one. Second, `insert` and `remove` return only booleans, with no moved-value report and no `getAt`.

The pick calls `rng.nextInt(size)` once. The bound equals the current size, so the draw is uniform over the slots. Every slot holds a distinct current value, so the pick is uniform over the values. The empty case checks the size first, because `nextInt(0)` throws `IllegalArgumentException` and the contract promises `IllegalStateException`.

Two checks prove the uniform claim. An exact check uses a scripted `Random` that returns each index in turn. It asserts the bound passed and the value returned for every slot. A statistical check draws from seeded generators and computes a chi-square statistic against the expected count. The seed fixes the draws, so the check never flakes.

**Complexity.**

- **Time** is O(1) expected for all three operations, because each does a constant number of map and array accesses.
- **Space** is O(n) for the array and the map, and the pick allocates nothing.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public final class InjectedRandomSet {
    /** Set with a caller-supplied random source for the pick. */
    static final class RandomizedSet {
        private final ArrayList<Integer> values = new ArrayList<>();
        private final HashMap<Integer, Integer> slotOf = new HashMap<>();

        /**
         * Adds val when absent.
         * Time: O(1) expected. Space: O(1) extra per stored value.
         * Invariant: values holds exactly the current values and slotOf names each slot.
         */
        boolean insert(int val) {
            // Present values leave the state unchanged.
            if (slotOf.containsKey(val)) return false;
            // The new value goes to the next free slot.
            slotOf.put(val, values.size());
            values.add(val);
            return true;
        }

        /**
         * Removes val by moving the last value into its slot.
         * Time: O(1) expected. Space: O(1).
         * Invariant: slotOf and values agree again on return.
         */
        boolean remove(int val) {
            Integer slot = slotOf.get(val);
            // Absent values change nothing.
            if (slot == null) return false;
            int last = values.get(values.size() - 1);
            // Move the last value into the hole, then repair its entry.
            values.set(slot, last);
            slotOf.put(last, slot);
            // Drop the tail by position, then delete the removed value's entry last.
            values.remove(values.size() - 1);
            slotOf.remove(val);
            return true;
        }

        /**
         * Returns one current value, each with probability 1/size.
         * Time: O(1), one draw and one array read. Space: O(1).
         * The uniform index implies a uniform value, because slots hold distinct values.
         */
        int getRandom(Random rng) {
            // nextInt(0) would throw IllegalArgumentException, so the empty case gets its own error.
            if (values.isEmpty()) throw new IllegalStateException("empty set");
            return values.get(rng.nextInt(values.size()));
        }

        List<Integer> snapshot() { return new ArrayList<>(values); }
    }

    /** Random source that replays scripted answers and records the bound it was asked for. */
    static final class ScriptedRandom extends Random {
        private final int[] script;
        private int next = 0;
        int lastBound = -1;
        ScriptedRandom(int... script) { this.script = script; }

        @Override
        public int nextInt(int bound) {
            // Record the bound so the test can check it equals the size.
            lastBound = bound;
            return script[next++];
        }
    }

    /** Returns sum over cells of (observed - expected)^2 / expected for equal expected counts. */
    static double chiSquare(int[] counts, int draws) {
        double expected = (double) draws / counts.length;
        double stat = 0;
        for (int c : counts) stat += (c - expected) * (c - expected) / expected;
        return stat;
    }

    public static void main(String[] args) {
        // Example 1: the insert results are true, false, true, true.
        RandomizedSet set = new RandomizedSet();
        boolean[] got = {set.insert(4), set.insert(4), set.insert(7), set.insert(9)};
        if (!(got[0] && !got[1] && got[2] && got[3])) throw new AssertionError("insert results");
        // A script returning 1 selects slot 1, which holds 7, and the bound is the size 3.
        ScriptedRandom one = new ScriptedRandom(1);
        if (set.getRandom(one) != 7) throw new AssertionError("scripted pick");
        if (one.lastBound != 3) throw new AssertionError("bound must equal size");
        // Exact enumeration: every index maps to the value stored in that slot.
        List<Integer> snap = set.snapshot();
        for (int k = 0; k < snap.size(); k++) {
            ScriptedRandom r = new ScriptedRandom(k);
            if (set.getRandom(r) != snap.get(k)) throw new AssertionError("slot " + k);
        }
        // The empty set throws IllegalStateException, and the raw JDK call with bound 0 throws IllegalArgumentException.
        try { new RandomizedSet().getRandom(new Random(1)); throw new AssertionError("no exception"); }
        catch (IllegalStateException expected) { }
        try { new Random(1).nextInt(0); throw new AssertionError("no exception"); }
        catch (IllegalArgumentException expected) { }
        // Example 2: values 1 to 5 and 10,000 seeded picks stay under the 0.1% critical value 18.47.
        RandomizedSet five = new RandomizedSet();
        for (int v = 1; v <= 5; v++) five.insert(v);
        Random seeded = new Random(42);
        int[] counts = new int[5];
        for (int i = 0; i < 10_000; i++) counts[five.getRandom(seeded) - 1]++;
        if (chiSquare(counts, 10_000) >= 18.47) throw new AssertionError("chi-square, five values");
        // After churn the pick stays uniform: eight inserts and two removes leave six values (critical value 20.52 for 5 degrees).
        RandomizedSet churn = new RandomizedSet();
        for (int v = 1; v <= 8; v++) churn.insert(v);
        churn.remove(2);
        churn.remove(8);
        int[] counts2 = new int[6];
        List<Integer> left = churn.snapshot();
        Random seeded2 = new Random(7);
        for (int i = 0; i < 12_000; i++) counts2[left.indexOf(churn.getRandom(seeded2))]++;
        if (chiSquare(counts2, 12_000) >= 20.52) throw new AssertionError("chi-square after churn");
        // Random scripts against a plain list: same array order and the same pick for the same seed.
        Random rnd = new Random(380);
        for (int round = 0; round < 200; round++) {
            RandomizedSet s = new RandomizedSet();
            ArrayList<Integer> model = new ArrayList<>();
            for (int step = 0; step < 50; step++) {
                int v = rnd.nextInt(10);
                int op = rnd.nextInt(3);
                if (op == 0) {
                    boolean expect = !model.contains(v);
                    if (s.insert(v) != expect) throw new AssertionError("insert");
                    if (expect) model.add(v);
                } else if (op == 1) {
                    int at = model.indexOf(v);
                    if (s.remove(v) != (at >= 0)) throw new AssertionError("remove");
                    if (at >= 0) {
                        model.set(at, model.get(model.size() - 1));
                        model.remove(model.size() - 1);
                    }
                } else if (!model.isEmpty()) {
                    long seed = rnd.nextLong();
                    int expect = model.get(new Random(seed).nextInt(model.size()));
                    if (s.getRandom(new Random(seed)) != expect) throw new AssertionError("pick");
                }
                if (!s.snapshot().equals(model)) throw new AssertionError("array order");
            }
        }
    }
}
```

#### Solution: [Boundary] Removing The Last Value (Author exercise)
<!-- id: ds-remove-last-value -->

**Approach.**

When the value to remove sits in the last slot, the freed slot and the last slot are the same. The copy step writes the value onto itself. The repair step then writes `slotOf.put(last, slot)`, and `last` equals the removed value, so that step re-creates its entry. The entry deleted last is the only one that stays deleted.

The correct order has four updates. Overwrite the freed slot with the last value. Write the moved value's map entry. Remove the last array position. Delete the removed value's map entry. The wrong order deletes the entry first and then writes the repair, which puts the removed value back in the map. After that, `contains` reports a value that the array no longer holds, and a later pick or insert acts on a broken invariant. When the set holds only one value, the array and the map both end empty.

The second hazard is `ArrayList<Integer>.remove`. A call with an `int` argument removes by position, and a call with an `Integer` argument removes by value. The tail removal needs the position form.

**Complexity.**

- **Time** is O(1) expected, because the four updates are a fixed number of map and array-end accesses.
- **Space** is O(1) extra, because the operation allocates only a few locals.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public final class LastValueRemoval {
    /** Array plus slot map, with the correct and the broken removal order side by side. */
    static final class Pool {
        final ArrayList<Integer> values = new ArrayList<>();
        final HashMap<Integer, Integer> slotOf = new HashMap<>();

        void insert(int val) {
            // Append and record the slot; callers in this test never insert a present value.
            slotOf.put(val, values.size());
            values.add(val);
        }

        /**
         * Correct order: overwrite, repair, drop the tail, delete the removed entry.
         * Time: O(1) expected. Space: O(1).
         * Invariant: when val is the last value, the final delete leaves no entry for it.
         */
        boolean remove(int val) {
            Integer slot = slotOf.get(val);
            if (slot == null) return false;
            int last = values.get(values.size() - 1);
            // Copy the last value over the freed slot.
            values.set(slot, last);
            // Repair the moved value's entry; this recreates the entry for val when val is last.
            slotOf.put(last, slot);
            // Remove the tail by position.
            values.remove(values.size() - 1);
            // The delete runs last, so it also removes the entry the repair just wrote.
            slotOf.remove(val);
            return true;
        }

        /** Broken order: deletes the entry before the repair, which resurrects it for the last value. */
        void removeBroken(int val) {
            int slot = slotOf.get(val);
            int last = values.get(values.size() - 1);
            values.set(slot, last);
            // Deleting first lets the repair write the entry again.
            slotOf.remove(val);
            slotOf.put(last, slot);
            values.remove(values.size() - 1);
        }

        List<Integer> snapshot() { return new ArrayList<>(values); }

        void check() {
            // Every slot is named by its map entry, and the map has no extra keys.
            for (int i = 0; i < values.size(); i++) {
                if (slotOf.get(values.get(i)) != i) throw new AssertionError("slot mismatch");
            }
            if (slotOf.size() != values.size()) throw new AssertionError("stale map entry");
        }
    }

    public static void main(String[] args) {
        // Example 1: remove the only value, check membership, then insert it again.
        Pool one = new Pool();
        one.insert(6);
        if (!one.remove(6)) throw new AssertionError("remove only");
        if (one.slotOf.containsKey(6)) throw new AssertionError("entry must stay deleted");
        if (!one.values.isEmpty() || !one.slotOf.isEmpty()) throw new AssertionError("empty after removal");
        one.insert(6);
        if (!one.snapshot().equals(List.of(6))) throw new AssertionError("reinsertion");
        // Example 2: [3, 6] minus 6 is [3]; [3, 6] minus 3 is [6] mapped to slot 0.
        Pool a = new Pool();
        a.insert(3);
        a.insert(6);
        a.remove(6);
        if (!a.snapshot().equals(List.of(3)) || a.slotOf.get(3) != 0 || a.slotOf.size() != 1) throw new AssertionError("example 2a");
        Pool b = new Pool();
        b.insert(3);
        b.insert(6);
        b.remove(3);
        if (!b.snapshot().equals(List.of(6)) || b.slotOf.get(6) != 0) throw new AssertionError("example 2b");
        // The broken order resurrects the entry for the only value.
        Pool bad = new Pool();
        bad.insert(6);
        bad.removeBroken(6);
        if (!bad.values.isEmpty()) throw new AssertionError("array is empty");
        if (!bad.slotOf.containsKey(6)) throw new AssertionError("the broken order resurrects the entry");
        // remove(int) removes by position and remove(Object) removes by value.
        ArrayList<Integer> list = new ArrayList<>(List.of(10, 20, 30, 1));
        list.remove(1);
        if (!list.equals(List.of(10, 30, 1))) throw new AssertionError("remove(int) is by position");
        list.remove(Integer.valueOf(1));
        if (!list.equals(List.of(10, 30))) throw new AssertionError("remove(Object) is by value");
        // Random scripts over a tiny value range, so removing the last value happens often.
        Random rnd = new Random(33_053);
        for (int round = 0; round < 400; round++) {
            Pool p = new Pool();
            ArrayList<Integer> model = new ArrayList<>();
            for (int step = 0; step < 40; step++) {
                int v = rnd.nextInt(4);
                if (rnd.nextBoolean()) {
                    // Insert only absent values, as the contract of this helper requires.
                    if (!model.contains(v)) { p.insert(v); model.add(v); }
                } else {
                    int at = model.indexOf(v);
                    if (p.remove(v) != (at >= 0)) throw new AssertionError("remove result");
                    if (at >= 0) {
                        model.set(at, model.get(model.size() - 1));
                        model.remove(model.size() - 1);
                    }
                }
                if (!p.snapshot().equals(model)) throw new AssertionError("array differs");
                p.check();
            }
        }
    }
}
```

#### Solution: [Recognize] Duplicates Allowed (LeetCode 381)
<!-- id: ds-random-duplicates -->

**Approach.**

The array now holds every occurrence, so a value can fill several slots. The map from value to index set replaces the map from value to one index. The invariant is that, for every slot `i`, the index set of `values.get(i)` contains `i`, and the sets together hold exactly the slots `0..size-1`.

`remove(val)` takes the greatest index `p` in the set of `val`. The rule has a useful effect: the last slot holds `val` exactly when `p` equals the last slot. In that case the operation only deletes the last slot and its index. Otherwise the last slot holds a different value `moved`. The operation writes `moved` into slot `p`, then removes the old last slot from the set of `moved` and adds `p`. The set of `moved` is a different object from the set of `val`, so the two edits cannot collide. The remaining count is the size of the set of `val` after the removal, and an empty set is deleted from the map.

A `TreeSet` finds the greatest index in O(log k). A `HashSet` finds none, because its iteration follows hash buckets and not insertion order, so `iterator().next()` returns an arbitrary index and the greatest-index rule needs an O(k) scan. The pick is as before: a random slot over all occurrences, so a value with more occurrences is more likely.

**Complexity.**

- **Time** is O(log k) for `insert` and `remove`, where k is the number of occurrences of the value involved, and O(1) for `getRandom`.
- **Space** is O(n), because each occurrence takes one array slot and one index in a set.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class DuplicatesAllowed {
    /** Multiset with array storage and a sorted index set per value. */
    static final class RandomizedCollection {
        private final ArrayList<Integer> values = new ArrayList<>();
        private final HashMap<Integer, TreeSet<Integer>> indexes = new HashMap<>();

        /**
         * Stores one more occurrence of val.
         * Time: O(log k) for the sorted set insert, k occurrences of val. Space: O(1) extra per occurrence.
         * Returns true when val had no occurrence before.
         */
        boolean insert(int val) {
            // Create the index set on the first occurrence.
            TreeSet<Integer> set = indexes.computeIfAbsent(val, key -> new TreeSet<>());
            boolean fresh = set.isEmpty();
            // The new occurrence takes the next free slot.
            set.add(values.size());
            values.add(val);
            return fresh;
        }

        /**
         * Removes the occurrence of val with the greatest index; returns the count that remains, or -1 when absent.
         * Time: O(log k) for the sorted set edits. Space: O(1).
         * Invariant: every slot appears in exactly the index set of its value.
         */
        int remove(int val) {
            TreeSet<Integer> set = indexes.get(val);
            // An absent value has no occurrence to remove.
            if (set == null) return -1;
            // The greatest index leaves the set of val first.
            int slot = set.pollLast();
            int lastSlot = values.size() - 1;
            // A different last value must move into the freed slot; slot == lastSlot means val was last.
            if (slot != lastSlot) {
                int moved = values.get(lastSlot);
                values.set(slot, moved);
                // The set of moved is a different object from set, so these two edits cannot collide.
                TreeSet<Integer> movedSet = indexes.get(moved);
                movedSet.remove(lastSlot);
                movedSet.add(slot);
            }
            // The int argument removes the tail by position.
            values.remove(lastSlot);
            // The remaining count is the set size; an empty set leaves the map.
            int remaining = set.size();
            if (remaining == 0) indexes.remove(val);
            return remaining;
        }

        /** Returns the value in a random slot; Time: O(1). Space: O(1). */
        int getRandom(Random rng) {
            if (values.isEmpty()) throw new IllegalStateException("empty collection");
            return values.get(rng.nextInt(values.size()));
        }

        List<Integer> snapshot() { return new ArrayList<>(values); }

        /** Checks the invariant: sets name exactly the slots of their value, and the sets cover every slot once. */
        void check() {
            int total = 0;
            for (var e : indexes.entrySet()) {
                if (e.getValue().isEmpty()) throw new AssertionError("empty set kept in map");
                for (int i : e.getValue()) {
                    if (values.get(i) != e.getKey().intValue()) throw new AssertionError("wrong value at slot " + i);
                }
                total += e.getValue().size();
            }
            if (total != values.size()) throw new AssertionError("sets do not cover the array");
        }
    }

    public static void main(String[] args) {
        // Example 1: inserts report true only for the first occurrence.
        RandomizedCollection c = new RandomizedCollection();
        boolean[] ins = {c.insert(4), c.insert(4), c.insert(6), c.insert(4)};
        if (!(ins[0] && !ins[1] && ins[2] && !ins[3])) throw new AssertionError("insert results");
        // The greatest index of 4 is 3, which is the last slot, so no value moves.
        if (c.remove(4) != 2) throw new AssertionError("remaining count");
        if (!c.snapshot().equals(List.of(4, 4, 6))) throw new AssertionError("example 1 array");
        c.check();
        // Example 2: the next removal takes index 1, so the last value 6 moves into slot 1.
        if (c.remove(4) != 1) throw new AssertionError("remaining 1");
        if (!c.snapshot().equals(List.of(4, 6))) throw new AssertionError("example 2 array");
        if (c.remove(9) != -1) throw new AssertionError("absent value");
        c.check();
        // A HashSet iterates by bucket, not by insertion order: 9 goes in first and 2 comes out first.
        HashSet<Integer> hs = new HashSet<>();
        hs.add(9);
        hs.add(2);
        if (hs.iterator().next() != 2) throw new AssertionError("HashSet order follows buckets");
        // A TreeSet returns the greatest element directly.
        TreeSet<Integer> ts = new TreeSet<>(List.of(9, 2, 5));
        if (ts.last() != 9) throw new AssertionError("greatest element");
        // The pick is proportional to the count: value 4 fills 3 of 4 slots.
        RandomizedCollection w = new RandomizedCollection();
        w.insert(4); w.insert(4); w.insert(4); w.insert(6);
        Random seeded = new Random(381);
        int fours = 0;
        for (int i = 0; i < 8_000; i++) if (w.getRandom(seeded) == 4) fours++;
        double z = (fours - 6_000.0) / Math.sqrt(8_000 * 0.75 * 0.25);
        if (Math.abs(z) > 3.3) throw new AssertionError("pick is proportional to the count");
        // Random scripts against a plain list that removes lastIndexOf and swaps with the last element.
        Random rnd = new Random(33_054);
        for (int round = 0; round < 300; round++) {
            RandomizedCollection s = new RandomizedCollection();
            ArrayList<Integer> model = new ArrayList<>();
            for (int step = 0; step < 60; step++) {
                int v = rnd.nextInt(5);
                int op = rnd.nextInt(3);
                if (op == 0) {
                    boolean expect = !model.contains(v);
                    if (s.insert(v) != expect) throw new AssertionError("insert");
                    model.add(v);
                } else if (op == 1) {
                    // lastIndexOf(Object) finds the greatest index in O(n), fine for an oracle.
                    int at = model.lastIndexOf(v);
                    int expectRemaining = -1;
                    if (at >= 0) {
                        model.set(at, model.get(model.size() - 1));
                        model.remove(model.size() - 1);
                        expectRemaining = Collections.frequency(model, v);
                    }
                    if (s.remove(v) != expectRemaining) throw new AssertionError("remaining count");
                } else if (!model.isEmpty()) {
                    long seed = rnd.nextLong();
                    int expect = model.get(new Random(seed).nextInt(model.size()));
                    if (s.getRandom(new Random(seed)) != expect) throw new AssertionError("pick");
                }
                if (!s.snapshot().equals(model)) throw new AssertionError("array order");
                s.check();
            }
        }
    }
}
```
