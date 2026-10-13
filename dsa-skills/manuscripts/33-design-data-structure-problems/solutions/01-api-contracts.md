<!-- solutions-for: 01-api-contracts -->
### Solutions For Writing Operation Contracts

#### Solution: [Build] Specify A Counter API (Author exercise)
<!-- id: ds-specify-counter-api -->

**Approach.**

The contract comes first. `add(key)` returns the new count, increments one key and `total`, and never fails except for a null key. `remove(key)` returns nothing, decrements one key, deletes the key at zero, and throws `NoSuchElementException` before it writes anything when the key is absent. `count(key)` returns 0 for an absent key, so absence is an ordinary answer. `snapshot()` returns a new map, which costs O(k) and keeps the caller away from the field.

The invariant is that every stored count is at least 1 and `total` equals the sum of the stored counts. Deleting the key at zero keeps `distinct()` equal to the map size. The failure check runs before any write, so a failed `remove` cannot break the invariant. A class that returns its own map breaks the invariant from outside, and the demonstration below shows the damage next to the safe copy.

**Complexity.**

- **Time** is O(1) expected per `add`, `remove`, `count`, `distinct` and `total`, because each does one hash-map lookup or update. `snapshot` takes O(k) for k distinct keys.
- **Space** is O(k) for the stored counts, and each `snapshot` allocates another O(k).

```java run
import java.util.*;

public final class SpecifyCounterApi {
    /** A counter whose operations state output, mutation, failure and cost. */
    static final class EventCounter {
        private final Map<String, Integer> counts = new HashMap<>();
        private int total;

        /**
         * Adds one occurrence of key and returns its new count.
         * Time: O(1) expected. Space: O(1) amortized for a new key.
         * Invariant: every stored count is at least 1 and total is their sum.
         */
        int add(String key) {
            // A null key is a caller bug, so fail before any write.
            Objects.requireNonNull(key, "key");
            // total and the key's count both grow by one, which keeps total equal to the sum.
            total++;
            return counts.merge(key, 1, Integer::sum);
        }

        /**
         * Removes one occurrence of key; throws NoSuchElementException when none exists.
         * Time: O(1) expected. Space: O(1).
         * Invariant: the check precedes every write, so a failed call changes nothing.
         */
        void remove(String key) {
            Objects.requireNonNull(key, "key");
            // Read the current count; null means the key is absent.
            Integer c = counts.get(key);
            if (c == null) throw new NoSuchElementException("no occurrence of " + key);
            // Delete the key at 1 so no stored count ever reaches 0.
            if (c == 1) counts.remove(key); else counts.put(key, c - 1);
            total--;
        }

        /** Returns the count of key, 0 when absent. Time: O(1) expected. Space: O(1). */
        int count(String key) {
            Objects.requireNonNull(key, "key");
            // getOrDefault turns absence into a legal answer, so the caller never sees null.
            return counts.getOrDefault(key, 0);
        }

        /** Returns the number of keys with a positive count. Time: O(1). Space: O(1). */
        int distinct() { return counts.size(); }

        /** Returns the sum of all counts. Time: O(1). Space: O(1). */
        int total() { return total; }

        /** Returns an independent copy of the counts. Time: O(k). Space: O(k). */
        Map<String, Integer> snapshot() { return new HashMap<>(counts); }
    }

    /** The hazard: a counter whose getter hands out its real map. */
    static final class LeakyCounter {
        private final Map<String, Integer> counts = new HashMap<>();
        void add(String key) { counts.merge(key, 1, Integer::sum); }
        Map<String, Integer> all() { return counts; }
    }

    public static void main(String[] args) {
        // The sample sequence from the problem.
        EventCounter c = new EventCounter();
        if (c.add("a") != 1 || c.add("b") != 1 || c.add("a") != 2) throw new AssertionError("add results");
        c.remove("a");
        if (c.count("a") != 1 || c.distinct() != 2 || c.total() != 2) throw new AssertionError("example 1");

        // Clearing a snapshot never reaches the counter, and an absent key is not a failure.
        c.snapshot().clear();
        if (c.count("a") != 1 || c.total() != 2) throw new AssertionError("snapshot is a copy");
        if (c.count("zzz") != 0) throw new AssertionError("absent key counts 0");
        boolean threw = false;
        try { c.remove("zzz"); } catch (NoSuchElementException e) { threw = true; }
        if (!threw || c.total() != 2 || c.distinct() != 2) throw new AssertionError("failed remove keeps state");
        threw = false;
        try { c.add(null); } catch (NullPointerException e) { threw = true; }
        if (!threw || c.total() != 2) throw new AssertionError("null key");

        // The leaky version loses its data when a caller clears the returned map.
        LeakyCounter leaky = new LeakyCounter();
        leaky.add("bob");
        leaky.all().clear();
        if (!leaky.all().isEmpty()) throw new AssertionError("leak lets the caller erase state");

        // Boxed counts above 127 are separate objects, so == compares references and equals compares values.
        EventCounter big1 = new EventCounter(), big2 = new EventCounter();
        for (int i = 0; i < 1000; i++) { big1.add("x"); big2.add("x"); }
        Integer p = big1.snapshot().get("x"), q = big2.snapshot().get("x");
        if (p == q) throw new AssertionError("1000 is outside the Integer cache");
        if (!p.equals(q) || p != 1000) throw new AssertionError("equals compares values");

        // Random operation scripts replayed against a naive list model.
        Random rnd = new Random(3301);
        String[] keys = {"a", "b", "c", "d"};
        for (int round = 0; round < 300; round++) {
            EventCounter real = new EventCounter();
            List<String> model = new ArrayList<>();
            for (int step = 0; step < 60; step++) {
                String k = keys[rnd.nextInt(keys.length)];
                if (rnd.nextBoolean()) {
                    // The model counts occurrences by scanning the list.
                    real.add(k); model.add(k);
                } else {
                    boolean present = model.contains(k);
                    boolean failed = false;
                    try { real.remove(k); } catch (NoSuchElementException e) { failed = true; }
                    if (failed == present) throw new AssertionError("failure matches absence");
                    if (present) model.remove(k);
                }
                if (real.total() != model.size()) throw new AssertionError("total");
                if (real.distinct() != new HashSet<>(model).size()) throw new AssertionError("distinct");
                for (String key : keys) {
                    if (real.count(key) != Collections.frequency(model, key)) throw new AssertionError("count " + key);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Empty Removal Policy (Author exercise)
<!-- id: ds-empty-removal-policy -->

**Approach.**

All three versions share one array-backed stack and differ only in the empty case, which is applied to `pop` and `top` alike. The throwing version checks `size == 0` first and throws `NoSuchElementException`, so a failed call changes nothing. The sentinel version checks the same condition and returns `-1`. That answer is only unambiguous when no stored value is `-1`, so `push` rejects negative values. The precondition version has no check at all, so its cost on the legal path is the lowest, and a violation is the caller's bug.

The demonstration pins down the difference. The first two versions are tested on the empty stack and on a state check afterward. The third is tested only on legal calls, plus one deliberate violation. In this implementation `pop` decrements `size` before it reads, so the violation throws `ArrayIndexOutOfBoundsException` and leaves `size` at -1. The contract does not promise that outcome, which is exactly why callers must check `isEmpty()`.

**Complexity.**

- **Time** is O(1) per operation in all three versions, and `push` is O(1) amortized because the array doubles when it fills.
- **Space** is O(n) for n stored values, with at most 2n slots allocated after doubling.

```java run
import java.util.*;

public final class EmptyRemovalPolicy {
    interface IntStack {
        void push(int v);
        int pop();
        int top();
        boolean isEmpty();
        int size();
    }

    /** Shared storage; subclasses choose only the empty-stack rule. */
    static abstract class ArrayStack implements IntStack {
        protected int[] data = new int[2];
        protected int size;
        /** Appends v. Time: O(1) amortized. Space: O(1) amortized. Invariant: data[0..size-1] holds the stack. */
        public void push(int v) {
            // Double the array when full so n pushes cost O(n) in total.
            if (size == data.length) data = Arrays.copyOf(data, size * 2);
            data[size++] = v;
        }
        public boolean isEmpty() { return size == 0; }
        public int size() { return size; }
    }

    /** Policy A: an empty stack throws and the state stays unchanged. */
    static final class ThrowingStack extends ArrayStack {
        public int pop() {
            // The check precedes the decrement, so a failed call writes nothing.
            if (size == 0) throw new NoSuchElementException("empty");
            return data[--size];
        }
        public int top() {
            if (size == 0) throw new NoSuchElementException("empty");
            return data[size - 1];
        }
    }

    /** Policy B: an empty stack returns -1, so stored values must be at least 0. */
    static final class SentinelStack extends ArrayStack {
        static final int EMPTY = -1;
        @Override public void push(int v) {
            // The sentinel is only unambiguous if no real value equals it.
            if (v < 0) throw new IllegalArgumentException("negative value");
            super.push(v);
        }
        public int pop() { return size == 0 ? EMPTY : data[--size]; }
        public int top() { return size == 0 ? EMPTY : data[size - 1]; }
    }

    /** Policy C: the caller must check isEmpty() first; an empty call is outside the contract. */
    static final class PreconditionStack extends ArrayStack {
        public int pop() { return data[--size]; }
        public int top() { return data[size - 1]; }
    }

    public static void main(String[] args) {
        // Policy A on the sample: 5, then an exception, then an unchanged empty stack.
        ThrowingStack a = new ThrowingStack();
        a.push(5);
        if (a.pop() != 5) throw new AssertionError("A pop");
        boolean threw = false;
        try { a.pop(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw || a.size() != 0) throw new AssertionError("A empty pop keeps state");
        threw = false;
        try { a.top(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("A applies the same rule to top");

        // Policy B on the sample: 5, then -1 for both pop and top.
        SentinelStack b = new SentinelStack();
        b.push(5);
        if (b.pop() != 5 || b.pop() != -1 || b.top() != -1 || b.size() != 0) throw new AssertionError("B sample");
        threw = false;
        try { b.push(-1); } catch (IllegalArgumentException e) { threw = true; }
        if (!threw || b.size() != 0) throw new AssertionError("B rejects the sentinel value");

        // Policy C: a legal sequence works, and a violation corrupts this implementation's size.
        PreconditionStack c = new PreconditionStack();
        c.push(8);
        if (c.top() != 8 || c.pop() != 8 || !c.isEmpty()) throw new AssertionError("C legal calls");
        threw = false;
        try { c.pop(); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw || c.size() != -1) throw new AssertionError("C violation leaves undefined state");

        // Random scripts against a list model; C is only called when the model is non-empty.
        Random rnd = new Random(3302);
        for (int round = 0; round < 300; round++) {
            ThrowingStack ra = new ThrowingStack();
            SentinelStack rb = new SentinelStack();
            PreconditionStack rc = new PreconditionStack();
            List<Integer> model = new ArrayList<>();
            for (int step = 0; step < 80; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) {
                    int v = rnd.nextInt(1000);
                    ra.push(v); rb.push(v); rc.push(v); model.add(v);
                } else if (model.isEmpty()) {
                    // Empty model: A throws, B returns -1, C is not called.
                    boolean t = false;
                    try { if (op == 1) ra.pop(); else ra.top(); } catch (NoSuchElementException e) { t = true; }
                    if (!t) throw new AssertionError("A throws on empty");
                    int got = op == 1 ? rb.pop() : rb.top();
                    if (got != -1) throw new AssertionError("B sentinel");
                } else {
                    int want = model.get(model.size() - 1);
                    if (op == 1) {
                        model.remove(model.size() - 1);
                        if (ra.pop() != want || rb.pop() != want || rc.pop() != want) throw new AssertionError("pop");
                    } else if (ra.top() != want || rb.top() != want || rc.top() != want) throw new AssertionError("top");
                }
                if (ra.size() != model.size() || rb.size() != model.size() || rc.size() != model.size()) throw new AssertionError("size");
            }
        }
    }
}
```

#### Solution: [Boundary] Repeated Calls (Author exercise)
<!-- id: ds-repeated-calls -->

**Approach.**

The simulation applies the counter contract call by call and records `distinct/total` after each one. An `add` always succeeds and increments the key's count and the total. A `remove` first looks up the key. When the count is positive, the remove lowers it, deletes the key at zero and lowers the total. When the key is absent, the remove reports `err` and writes nothing, so the reported numbers equal the previous report.

The boundary lies in duplicates. After two `add x` calls, one `remove x` leaves `distinct` unchanged, because the key survives with count 1. Only the removal that brings the count to 0 lowers `distinct`. An implementation that decrements `distinct` on every removal, or that keeps zero-count entries, fails on exactly these sequences. The invariant that every stored count is at least 1 prevents both mistakes.

**Complexity.**

- **Time** is O(m) for m calls, because each call does one hash-map lookup and update in O(1) expected time.
- **Space** is O(k) for k distinct keys plus O(m) for the report list.

```java run
import java.util.*;

public final class RepeatedCalls {
    /**
     * Replays calls such as "add x" and "remove x" and reports the state after each.
     * Time: O(m) expected for m calls. Space: O(k + m) for k keys and m reports.
     * Invariant: every stored count is at least 1, and total is the sum of the counts.
     */
    static List<String> replay(List<String> calls) {
        Map<Character, Integer> counts = new HashMap<>();
        int total = 0;
        List<String> out = new ArrayList<>();
        for (String call : calls) {
            // Split the call into its operation word and its one-letter key.
            boolean isAdd = call.startsWith("add");
            char key = call.charAt(call.length() - 1);
            boolean ok = true;
            if (isAdd) {
                // compute stores 1 for a new key and count + 1 otherwise.
                counts.compute(key, (k, v) -> v == null ? 1 : v + 1);
                total++;
            } else if (counts.containsKey(key)) {
                // computeIfPresent returning null deletes the key, so a stored count is never 0.
                counts.computeIfPresent(key, (k, v) -> v == 1 ? null : v - 1);
                total--;
            } else {
                // A failed removal writes nothing; the report repeats the old numbers.
                ok = false;
            }
            out.add((ok ? "ok " : "err ") + counts.size() + "/" + total);
        }
        return out;
    }

    /** Naive model: a list of occurrences. Distinct is the set size, total is the list size. */
    static List<String> oracle(List<String> calls) {
        List<Character> model = new ArrayList<>();
        List<String> out = new ArrayList<>();
        for (String call : calls) {
            char key = call.charAt(call.length() - 1);
            boolean ok = true;
            if (call.startsWith("add")) model.add(key);
            else if (model.contains(key)) model.remove(Character.valueOf(key));
            else ok = false;
            out.add((ok ? "ok " : "err ") + new HashSet<>(model).size() + "/" + model.size());
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: a duplicate keeps the key alive after one removal.
        List<String> r1 = replay(List.of("add a", "add a", "remove a"));
        if (!r1.equals(List.of("ok 1/1", "ok 1/2", "ok 1/1"))) throw new AssertionError("example 1 " + r1);

        // Example 2: the third removal fails and the next add restores a second key.
        List<String> r2 = replay(List.of("add x", "add x", "add y", "remove x", "remove x", "remove x", "add x"));
        if (!r2.equals(List.of("ok 1/1", "ok 1/2", "ok 2/3", "ok 2/2", "ok 1/1", "err 1/1", "ok 2/2")))
            throw new AssertionError("example 2 " + r2);

        // Random scripts compared with the list model.
        Random rnd = new Random(3303);
        for (int round = 0; round < 500; round++) {
            List<String> calls = new ArrayList<>();
            int n = 1 + rnd.nextInt(40);
            for (int i = 0; i < n; i++) {
                calls.add((rnd.nextBoolean() ? "add " : "remove ") + (char) ('a' + rnd.nextInt(3)));
            }
            if (!replay(calls).equals(oracle(calls))) throw new AssertionError("mismatch " + calls);
        }
    }
}
```

#### Solution: [Recognize] Min Stack (LeetCode 155)
<!-- id: ds-min-stack-contract -->

**Approach.**

The contracts come first. `push(v)` returns nothing, appends `v`, and costs O(1) amortized because the arrays double. `pop()` returns the removed value, removes the newest value, and throws `NoSuchElementException` on an empty stack before it changes anything. `top()` returns the newest value, changes nothing, and throws on empty. `getMin()` returns the smallest stored value, changes nothing, costs O(1), and throws on empty, because an empty stack has no minimum and any placeholder would collide with a legal `int`.

To make `getMin` constant time, the stack keeps a second array `mins`, where `mins[i]` is the minimum of `values[0..i]`. The invariant is that `mins[size-1]` equals the minimum of everything stored. A push computes `mins[size]` from the previous entry in O(1). A pop only decrements `size`, and the entry below already holds the correct minimum for the remaining values, so no recomputation happens.

**Complexity.**

- **Time** is O(1) for `pop`, `top` and `getMin`, and O(1) amortized for `push` because doubling copies are spread over earlier pushes.
- **Space** is O(n) for n stored values, since two int arrays each hold at most 2n slots.

```java run
import java.util.*;

public final class MinStackContract {
    /** A stack with constant-time minimum and a stated failure contract. */
    static final class MinStack {
        private int[] values = new int[2];
        private int[] mins = new int[2];
        private int size;

        /**
         * Appends v. Time: O(1) amortized. Space: O(1) amortized.
         * Invariant: mins[i] is the minimum of values[0..i].
         */
        void push(int v) {
            // Grow both arrays together so they always have equal length.
            if (size == values.length) {
                values = Arrays.copyOf(values, size * 2);
                mins = Arrays.copyOf(mins, size * 2);
            }
            values[size] = v;
            // The running minimum depends only on v and the entry below it.
            mins[size] = size == 0 ? v : Math.min(v, mins[size - 1]);
            size++;
        }

        /** Removes and returns the newest value; throws on empty with no change. Time: O(1). Space: O(1). */
        int pop() {
            // Check first so a failed call changes nothing.
            if (size == 0) throw new NoSuchElementException("empty stack");
            return values[--size];
        }

        /** Returns the newest value; throws on empty. Time: O(1). Space: O(1). */
        int top() {
            if (size == 0) throw new NoSuchElementException("empty stack");
            return values[size - 1];
        }

        /** Returns the smallest stored value; throws on empty. Time: O(1). Space: O(1). */
        int getMin() {
            if (size == 0) throw new NoSuchElementException("empty stack");
            // The top running minimum covers every stored value.
            return mins[size - 1];
        }
    }

    static boolean throwsEmpty(Runnable r) {
        try { r.run(); return false; } catch (NoSuchElementException e) { return true; }
    }

    public static void main(String[] args) {
        // Example 1: results of the six value-returning calls.
        MinStack s = new MinStack();
        s.push(6); s.push(2); s.push(9); s.push(2);
        int[] got = new int[6];
        got[0] = s.getMin(); got[1] = s.pop(); got[2] = s.getMin();
        got[3] = s.pop(); got[4] = s.pop(); got[5] = s.getMin();
        if (!Arrays.equals(got, new int[] {2, 2, 2, 9, 2, 6})) throw new AssertionError("example 1 " + Arrays.toString(got));

        // Example 2: a failed pop leaves the stack usable.
        MinStack e = new MinStack();
        if (!throwsEmpty(e::pop) || !throwsEmpty(e::top) || !throwsEmpty(e::getMin)) throw new AssertionError("empty failures");
        e.push(3);
        if (e.getMin() != 3) throw new AssertionError("example 2");

        // Extreme values must not be confused with a placeholder.
        MinStack x = new MinStack();
        x.push(Integer.MAX_VALUE); x.push(Integer.MIN_VALUE); x.push(Integer.MAX_VALUE);
        if (x.getMin() != Integer.MIN_VALUE) throw new AssertionError("extremes");

        // Random scripts against a list model that scans for the minimum.
        Random rnd = new Random(3304);
        for (int round = 0; round < 300; round++) {
            MinStack real = new MinStack();
            List<Integer> model = new ArrayList<>();
            for (int step = 0; step < 80; step++) {
                int op = rnd.nextInt(4);
                if (op == 0) {
                    int v = rnd.nextInt(10) == 0 ? Integer.MIN_VALUE : rnd.nextInt(21) - 10;
                    real.push(v); model.add(v);
                } else if (model.isEmpty()) {
                    // Every query fails on empty, and the next push still works.
                    Runnable r = op == 1 ? real::pop : op == 2 ? real::top : real::getMin;
                    if (!throwsEmpty(r)) throw new AssertionError("must throw on empty");
                } else if (op == 1) {
                    if (real.pop() != model.remove(model.size() - 1)) throw new AssertionError("pop");
                } else if (op == 2) {
                    if (real.top() != model.get(model.size() - 1)) throw new AssertionError("top");
                } else if (real.getMin() != Collections.min(model)) throw new AssertionError("getMin");
            }
        }
    }
}
```
