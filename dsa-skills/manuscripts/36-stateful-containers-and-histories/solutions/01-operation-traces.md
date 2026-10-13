<!-- solutions-for: 01-operation-traces -->
### Solutions For Method Call Sequences

#### Solution: [Build] Bounded Counter API (Author exercise)
<!-- id: sc-operation-traces-bounded-counter -->

**Approach.**
The class keeps two fields, the fixed `limit` and the mutable `count`. The invariant is `0 <= count <= limit`. The constructor sets `count` to 0, which satisfies the invariant for every non-negative limit. The method `increment` compares `count` with `limit` before it writes anything. When they are equal, the method returns `false` and the state stays identical. Otherwise it adds 1, which keeps `count` at most `limit`, and returns `true`. The method `reset` writes 0, which is legal for every limit, and `value` only reads.

Because every method keeps the invariant when it starts from a legal state, induction over the trace length shows that every sequence of calls ends in a legal state. The program below checks the claim from two sides. It compares every return value with a model that stores the accepted increments in a list, and it checks the invariant after every call of every random trace.

**Complexity.**
- **Time** is O(1) per call, because each method performs one comparison and at most one assignment.
- **Space** is O(1) per object, because the class stores two ints regardless of the number of calls.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class BoundedCounterBuild {
    /** Counter that refuses increments at the limit and keeps 0 <= count <= limit. */
    static final class BoundedCounter {
        private final int limit;
        private int count;

        /**
         * Creates a counter with the given limit.
         * Time: O(1). Space: O(1).
         * Invariant: the constructor establishes count = 0, a legal state for every limit >= 0.
         */
        BoundedCounter(int limit) {
            // The limit never changes after construction.
            this.limit = limit;
            // The count starts at the smallest legal value.
            this.count = 0;
        }

        /**
         * Adds 1 when the count is below the limit and reports whether it did.
         * Time: O(1). Space: O(1).
         * Invariant: a refused call writes no field, so the state before and after are equal.
         */
        boolean increment() {
            // The precondition test runs before any write, so a refusal changes nothing.
            if (count == limit) return false;
            // Accepted path: count < limit, so count + 1 <= limit still holds.
            count++;
            // The caller learns that the increment happened.
            return true;
        }

        /**
         * Sets the count back to 0.
         * Time: O(1). Space: O(1).
         * Invariant: 0 is legal for every limit, so the state stays legal.
         */
        void reset() {
            // One assignment restores the smallest legal value.
            count = 0;
        }

        /**
         * Returns the current count.
         * Time: O(1). Space: O(1).
         * Invariant: the method only reads, so no field changes.
         */
        int value() {
            // The count is already within 0..limit by the invariant.
            return count;
        }
    }

    /** The naive class from the lesson: it counts first and reports afterward. */
    static final class NaiveCounter {
        private final int limit;
        private int count;
        NaiveCounter(int limit) { this.limit = limit; }
        boolean increment() { count++; return count <= limit; }
        int value() { return count; }
    }

    /** Model that remembers every accepted increment as a list entry. Time per call: O(limit). Space: O(limit). */
    static final class Model {
        private final int limit;
        private final List<Integer> accepted = new ArrayList<>();
        Model(int limit) { this.limit = limit; }
        boolean increment() {
            // A new entry fits only while the list is shorter than the limit.
            if (accepted.size() >= limit) return false;
            accepted.add(accepted.size());
            return true;
        }
        void reset() { accepted.clear(); }
        int value() { return accepted.size(); }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise: the third increment is refused and value stays 2.
        BoundedCounter c = new BoundedCounter(2);
        if (!c.increment() || !c.increment() || c.increment() || c.value() != 2) throw new AssertionError("example 1");
        // Example 2: reset makes room again for a limit of 1.
        BoundedCounter d = new BoundedCounter(1);
        if (!d.increment()) throw new AssertionError("example 2 first");
        d.reset();
        if (!d.increment() || d.increment() || d.value() != 1) throw new AssertionError("example 2");
        // A limit of 0 refuses every increment and keeps value at 0.
        BoundedCounter z = new BoundedCounter(0);
        if (z.increment() || z.value() != 0) throw new AssertionError("limit 0");
        // The naive class returns false on the third increment but its count passes the limit.
        NaiveCounter bad = new NaiveCounter(2);
        bad.increment();
        bad.increment();
        if (bad.increment() || bad.value() != 3) throw new AssertionError("naive drift");
        // Random traces compare every return value with the model and check the invariant after every call.
        Random rnd = new Random(3601L);
        for (int t = 0; t < 4000; t++) {
            int limit = rnd.nextInt(6);
            BoundedCounter real = new BoundedCounter(limit);
            Model model = new Model(limit);
            for (int step = rnd.nextInt(31); step > 0; step--) {
                int op = rnd.nextInt(3);
                if (op == 0 && real.increment() != model.increment()) throw new AssertionError("increment");
                if (op == 1) { real.reset(); model.reset(); }
                if (real.value() != model.value()) throw new AssertionError("value");
                if (real.value() < 0 || real.value() > limit) throw new AssertionError("invariant");
            }
        }
    }
}
```

#### Solution: [Vary] Design Parking System (LeetCode 1603)
<!-- id: sc-operation-traces-parking-system -->

**Approach.**
The class keeps one array `free` with an entry for each car type. Entry `t - 1` holds the number of free spaces of type `t`. The invariant is that each entry stays between 0 and the capacity given for that type. The call `addCar(t)` looks only at the entry of its own type. When the entry is 0, the call returns `false` and writes nothing. Otherwise it decreases that one entry and returns `true`.

The independence of the three types is the new decision compared with the single counter. A refusal for one type must not touch the other two entries, and the oracle checks this by comparing the full list of parked cars per type after each call.

**Complexity.**
- **Time** is O(1) per call, because one array read and at most one array write run.
- **Space** is O(1) per object, because the array always has exactly three entries.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ParkingSystemVary {
    /** Parking lot with an independent number of free spaces for each of three car types. */
    static final class ParkingSystem {
        private final int[] free;

        /**
         * Stores the free spaces of each type in the order big, medium, small.
         * Time: O(1). Space: O(1).
         * Invariant: every entry is between 0 and its starting capacity.
         */
        ParkingSystem(int big, int medium, int small) {
            // Three entries, indexed by carType - 1.
            free = new int[] {big, medium, small};
        }

        /**
         * Parks one car of the given type when a space is free.
         * Time: O(1). Space: O(1).
         * Invariant: a refused call writes nothing; an accepted call lowers exactly one entry.
         */
        boolean addCar(int carType) {
            // Only the entry of this type takes part in the decision.
            if (free[carType - 1] == 0) return false;
            // Accepted: one space of this type is used, so the entry stays at least 0.
            free[carType - 1]--;
            return true;
        }
    }

    /** Oracle that stores every parked car in a list for its type. Time per call: O(1). Space: O(cars). */
    static final class Model {
        private final int[] cap;
        private final List<List<Integer>> parked = new ArrayList<>();
        private int nextId;
        Model(int big, int medium, int small) {
            cap = new int[] {big, medium, small};
            for (int i = 0; i < 3; i++) parked.add(new ArrayList<>());
        }
        boolean addCar(int type) {
            List<Integer> lot = parked.get(type - 1);
            // The lot accepts a car only while it holds fewer cars than its capacity.
            if (lot.size() >= cap[type - 1]) return false;
            lot.add(nextId++);
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1: the small lot has no space, and the big lot runs out after one car.
        ParkingSystem a = new ParkingSystem(1, 1, 0);
        if (!a.addCar(1) || !a.addCar(2) || a.addCar(3) || a.addCar(1)) throw new AssertionError("example 1");
        // Example 2: a refusal for medium cars does not use or free a space of another type.
        ParkingSystem b = new ParkingSystem(2, 0, 1);
        boolean[] want = {true, false, false, true, true, false};
        int[] types = {3, 3, 2, 1, 1, 1};
        for (int i = 0; i < types.length; i++) if (b.addCar(types[i]) != want[i]) throw new AssertionError("example 2 at " + i);
        // Random traces compare every answer with the oracle, including lots of size 0.
        Random rnd = new Random(3602L);
        for (int t = 0; t < 4000; t++) {
            int big = rnd.nextInt(4), medium = rnd.nextInt(4), small = rnd.nextInt(4);
            ParkingSystem real = new ParkingSystem(big, medium, small);
            Model model = new Model(big, medium, small);
            for (int step = rnd.nextInt(16); step > 0; step--) {
                int type = 1 + rnd.nextInt(3);
                if (real.addCar(type) != model.addCar(type)) throw new AssertionError("mismatch");
            }
        }
    }
}
```

#### Solution: [Boundary] Rejected Calls (Author exercise)
<!-- id: sc-operation-traces-rejected-calls -->

**Approach.**
The class keeps `capacity` and `used`, with the invariant `0 <= used <= capacity`. Both methods that can refuse decide first and write second. The call `reserve(n)` accepts when `n <= capacity - used`. The subtraction form is deliberate. Because `used <= capacity` holds, the difference is a non-negative `int`, so no overflow occurs. The form `used + n <= capacity` would overflow when both values are near `2^31 - 1`, and the wrapped negative sum would wrongly accept the call. The call `cancel(n)` accepts when `n <= used`, which keeps `used` at least 0.

The refusing path contains only a `return false`, so no field is written. The program proves this claim for every random trace. It reads every non-static field through reflection before each call and compares the values after each call that returns `false`. A field added to the class later is covered by the same comparison without any change to the checks.

**Complexity.**
- **Time** is O(1) per call, because each method runs one comparison and at most one assignment.
- **Space** is O(1) per object, because the class stores two ints.

```java run
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RejectedCallsQuota {
    /** Quota that reserves and cancels whole amounts and refuses a call that would break 0 <= used <= capacity. */
    static final class Quota {
        private final int capacity;
        private int used;

        /**
         * Creates an empty quota.
         * Time: O(1). Space: O(1).
         * Invariant: used = 0 is legal for every capacity >= 0.
         */
        Quota(int capacity) {
            // The capacity stays fixed for the life of the object.
            this.capacity = capacity;
            // Nothing is reserved yet.
            this.used = 0;
        }

        /**
         * Reserves n units, all or nothing.
         * Time: O(1). Space: O(1).
         * Invariant: the test uses capacity - used, which cannot overflow because used <= capacity.
         */
        boolean reserve(int n) {
            // Refuse before any write; the subtraction form avoids int overflow.
            if (n > capacity - used) return false;
            // Accepted: n <= capacity - used, so used + n <= capacity.
            used += n;
            return true;
        }

        /**
         * Gives back n previously reserved units, all or nothing.
         * Time: O(1). Space: O(1).
         * Invariant: a refused call leaves used unchanged; an accepted call keeps used >= 0.
         */
        boolean cancel(int n) {
            // Refuse before any write when fewer than n units are reserved.
            if (n > used) return false;
            // Accepted: n <= used, so used - n >= 0.
            used -= n;
            return true;
        }

        /**
         * Returns the reserved amount.
         * Time: O(1). Space: O(1).
         * Invariant: the method reads only.
         */
        int used() {
            // The value is within 0..capacity by the invariant.
            return used;
        }
    }

    /**
     * Reads every non-static field of the quota, so main can compare states before and after a call.
     * Time: O(number of fields). Space: O(number of fields).
     */
    static List<Object> snapshot(Quota q) throws IllegalAccessException {
        List<Object> values = new ArrayList<>();
        // Every declared instance field takes part, including fields added later.
        for (Field f : Quota.class.getDeclaredFields()) {
            if (Modifier.isStatic(f.getModifiers())) continue;
            f.setAccessible(true);
            values.add(f.get(q));
        }
        return values;
    }

    public static void main(String[] args) throws Exception {
        // Example 1 from the exercise.
        Quota q = new Quota(5);
        if (!q.reserve(3) || q.reserve(3) || q.cancel(4) || !q.cancel(2) || q.used() != 1) throw new AssertionError("example 1");
        // Example 2: capacity 0 refuses every reservation and every cancellation.
        Quota z = new Quota(0);
        if (z.reserve(1) || z.cancel(1) || z.used() != 0) throw new AssertionError("example 2");
        // The addition form overflows in Java, so the class must not use it.
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("expected wraparound");
        Quota big = new Quota(Integer.MAX_VALUE);
        if (!big.reserve(Integer.MAX_VALUE) || big.reserve(1) || big.used() != Integer.MAX_VALUE) throw new AssertionError("overflow");
        // Random traces: results match a long-based model, and every refused call leaves all fields equal.
        Random rnd = new Random(3603L);
        for (int t = 0; t < 4000; t++) {
            int cap = rnd.nextInt(4) == 0 ? Integer.MAX_VALUE - rnd.nextInt(3) : rnd.nextInt(8);
            Quota real = new Quota(cap);
            long modelUsed = 0;
            for (int step = rnd.nextInt(21); step > 0; step--) {
                int n = rnd.nextInt(4) == 0 ? Integer.MAX_VALUE - rnd.nextInt(3) : 1 + rnd.nextInt(6);
                boolean reserve = rnd.nextBoolean();
                List<Object> before = snapshot(real);
                boolean got = reserve ? real.reserve(n) : real.cancel(n);
                // The model uses long arithmetic, so it cannot overflow.
                boolean want = reserve ? modelUsed + n <= cap : n <= modelUsed;
                if (want) modelUsed += reserve ? n : -n;
                if (got != want) throw new AssertionError("result");
                if (real.used() != modelUsed) throw new AssertionError("used");
                // A refused call must leave every field exactly as it was.
                if (!got && !before.equals(snapshot(real))) throw new AssertionError("fields changed on refusal");
            }
        }
    }
}
```

#### Solution: [Recognize] Design an Ordered Stream (LeetCode 1656)
<!-- id: sc-operation-traces-ordered-stream -->

**Approach.**
The class keeps an array `slots` indexed by key and a pointer `ptr`. The invariant is that `ptr` is the smallest key whose value has not been returned, and every key below `ptr` has been stored and returned exactly once. An insertion writes the value into its slot. If the slot at `ptr` is still empty, nothing new becomes contiguous and the list is empty. Otherwise a loop collects the values at `ptr`, `ptr + 1` and onward while slots are filled, and `ptr` stops at the first empty slot or at `n + 1`. The loop ends because each pass moves `ptr` forward and the array is finite.

The state is no longer one count. It is a stored array plus a pointer, and the returned list is exactly the contiguous run that the insertion completed. The oracle recomputes the whole contiguous prefix of stored keys from scratch after each insertion and returns the part that is new.

**Complexity.**
- **Time** is O(n) in total over all insertions, because `ptr` only moves forward and each slot is read into a list at most once; one call costs O(1) plus its list length.
- **Space** is O(n), because the array holds one string reference per key.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class OrderedStreamRecognize {
    /** Stream that releases values in key order as soon as they form a contiguous run. */
    static final class OrderedStream {
        private final String[] slots;
        private int ptr;

        /**
         * Creates a stream for keys 1 to n.
         * Time: O(n). Space: O(n).
         * Invariant: ptr = 1 and no value has been returned yet.
         */
        OrderedStream(int n) {
            // Index 0 stays unused, so key k lives at slots[k].
            slots = new String[n + 2];
            // Key 1 is the first value to release.
            ptr = 1;
        }

        /**
         * Stores one value and returns the newly contiguous values in key order.
         * Time: O(1) plus the length of the returned list. Space: O(1) beyond the returned list.
         * Invariant: ptr is the smallest key not yet returned; all smaller keys were returned once.
         */
        List<String> insert(int idKey, String value) {
            // Store the value; no other field changes yet.
            slots[idKey] = value;
            List<String> out = new ArrayList<>();
            // Release values while the slot at ptr is filled; the sentinel slot n + 1 stays null and stops the loop.
            while (slots[ptr] != null) {
                // Each returned value is read once, so the total work over all calls is O(n).
                out.add(slots[ptr]);
                // Move to the next key to release.
                ptr++;
            }
            return out;
        }
    }

    /** Oracle that recomputes the contiguous prefix of stored keys from scratch. Time per call: O(n). Space: O(n). */
    static final class Model {
        private final String[] stored;
        private int released;
        Model(int n) { stored = new String[n + 2]; }
        List<String> insert(int key, String value) {
            stored[key] = value;
            // k is the largest key such that keys 1..k are all stored.
            int k = 0;
            while (stored[k + 1] != null) k++;
            List<String> out = new ArrayList<>();
            // Return the keys between the old prefix and the new prefix.
            for (int i = released + 1; i <= k; i++) out.add(stored[i]);
            released = Math.max(released, k);
            return out;
        }
    }

    public static void main(String[] args) {
        // Example 1: keys 2 and 1 release together, then keys 3 and 4 release together.
        OrderedStream a = new OrderedStream(4);
        if (!a.insert(2, "b").equals(List.of())) throw new AssertionError("e1 step 1");
        if (!a.insert(1, "a").equals(List.of("a", "b"))) throw new AssertionError("e1 step 2");
        if (!a.insert(4, "d").equals(List.of())) throw new AssertionError("e1 step 3");
        if (!a.insert(3, "c").equals(List.of("c", "d"))) throw new AssertionError("e1 step 4");
        // Example 2: the last insertion completes a run that began at key 2.
        OrderedStream b = new OrderedStream(3);
        if (!b.insert(1, "x").equals(List.of("x"))) throw new AssertionError("e2 step 1");
        if (!b.insert(3, "z").equals(List.of())) throw new AssertionError("e2 step 2");
        if (!b.insert(2, "y").equals(List.of("y", "z"))) throw new AssertionError("e2 step 3");
        // Random permutations of the keys compare every returned list with the oracle.
        Random rnd = new Random(3604L);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            List<Integer> keys = new ArrayList<>();
            for (int k = 1; k <= n; k++) keys.add(k);
            java.util.Collections.shuffle(keys, rnd);
            OrderedStream real = new OrderedStream(n);
            Model model = new Model(n);
            int returned = 0;
            for (int key : keys) {
                String v = "v" + key;
                List<String> got = real.insert(key, v);
                if (!got.equals(model.insert(key, v))) throw new AssertionError("mismatch at key " + key);
                returned += got.size();
            }
            // After all n insertions every value has been returned exactly once.
            if (returned != n) throw new AssertionError("returned " + returned + " of " + n);
        }
    }
}
```
