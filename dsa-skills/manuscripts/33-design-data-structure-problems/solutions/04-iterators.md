<!-- solutions-for: 04-iterators -->
### Solutions For Peeking And Flattening

#### Solution: [Build] Array Peeking Iterator (Author exercise)
<!-- id: ds-array-peeking-iterator -->

**Approach.**

The class keeps a cursor `pos` into `data`, one cached element `slot` and a boolean `hasSlot`. The invariant is that either `hasSlot` is false and `data[pos..]` holds every untaken element, or `hasSlot` is true, `slot` is the next element and `data[pos..]` holds the elements after it.

Operation `peek()` reads `data[pos]` only when `hasSlot` is false, and it checks the length before any assignment, so a failed call changes nothing. Operation `next()` calls `peek()` and then clears the flag, so one taken element costs exactly one read. Operation `hasNext()` answers from the flag and the cursor without reading.

**Complexity.**

- **Time** is O(1) per operation, because each call does a constant number of comparisons and at most one array read.
- **Space** is O(1) extra, because the class stores one cursor, one value and one flag and never copies `data`.

```java run
import java.util.NoSuchElementException;
import java.util.Random;

public final class ArrayPeekingIterator {
    private final int[] data;
    private int pos;
    private int slot;
    private boolean hasSlot;

    ArrayPeekingIterator(int[] data) { this.data = data; }

    /**
     * Reports whether an element is left to take.
     * Time: O(1), two reads. Space: O(1). Invariant: no field changes.
     */
    boolean hasNext() {
        // Either the slot holds the next element or the array still has unread positions.
        return hasSlot || pos < data.length;
    }

    /**
     * Returns the next element without taking it.
     * Time: O(1), at most one array read. Space: O(1).
     * Invariant: afterwards hasSlot is true and slot holds the next untaken element.
     */
    int peek() {
        // Read from the array only when the slot is empty, so repeated peeks cost one read.
        if (!hasSlot) {
            // Check before assigning, so a failed call leaves every field as it was.
            if (pos >= data.length) throw new NoSuchElementException("no element left");
            slot = data[pos++];
            hasSlot = true;
        }
        return slot;
    }

    /**
     * Takes the next element.
     * Time: O(1). Space: O(1). Invariant: afterwards the slot is empty.
     */
    int next() {
        // peek() fills the slot once, then the flag clears so the element is taken exactly once.
        int value = peek();
        hasSlot = false;
        return value;
    }

    /** Number of reads from the array so far; equals taken elements plus one when the slot is full. */
    int advances() { return pos; }

    static boolean throwsOnPeek(ArrayPeekingIterator it) {
        try { it.peek(); return false; } catch (NoSuchElementException e) { return true; }
    }

    public static void main(String[] args) {
        // Example 1: peek twice, then take two elements.
        ArrayPeekingIterator a = new ArrayPeekingIterator(new int[] {4, 7, 9});
        if (a.peek() != 4 || a.peek() != 4) throw new AssertionError("repeated peek");
        if (a.next() != 4 || a.next() != 7) throw new AssertionError("next after peek");
        if (a.advances() != 2) throw new AssertionError("advances after four calls");
        // Example 2: a single element, then the failing peek leaves state alone.
        ArrayPeekingIterator b = new ArrayPeekingIterator(new int[] {5});
        if (b.peek() != 5 || b.next() != 5 || b.hasNext()) throw new AssertionError("single element");
        if (!throwsOnPeek(b) || b.advances() != 1) throw new AssertionError("failed peek changes nothing");
        // Empty input throws on both read operations.
        ArrayPeekingIterator empty = new ArrayPeekingIterator(new int[0]);
        if (empty.hasNext() || !throwsOnPeek(empty)) throw new AssertionError("empty");
        boolean threw = false;
        try { empty.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("next on empty");
        // Random scripts compare the class with an index-based model of the sequence.
        Random rnd = new Random(33);
        for (int trial = 0; trial < 400; trial++) {
            int n = rnd.nextInt(9);
            int[] data = new int[n];
            for (int i = 0; i < n; i++) data[i] = rnd.nextInt(11) - 5;
            ArrayPeekingIterator it = new ArrayPeekingIterator(data);
            int taken = 0;
            boolean peeked = false;
            for (int step = 0; step < 30; step++) {
                int op = rnd.nextInt(3);
                boolean left = taken < n;
                if (op == 0) {
                    if (it.hasNext() != left) throw new AssertionError("hasNext");
                } else if (op == 1) {
                    if (left) {
                        if (it.peek() != data[taken]) throw new AssertionError("peek value");
                        peeked = true;
                    } else if (!throwsOnPeek(it)) throw new AssertionError("peek should throw");
                } else {
                    if (left) {
                        if (it.next() != data[taken]) throw new AssertionError("next value");
                        taken++;
                        peeked = false;
                    } else {
                        boolean t = false;
                        try { it.next(); } catch (NoSuchElementException e) { t = true; }
                        if (!t) throw new AssertionError("next should throw");
                    }
                }
                // The read count never exceeds taken elements plus the cached one.
                if (it.advances() != taken + (peeked ? 1 : 0)) throw new AssertionError("advances");
            }
        }
    }
}
```

#### Solution: [Vary] Peeking Iterator (LeetCode 284)
<!-- id: ds-peeking-iterator-contract -->

**Approach.**

The class wraps the source with a one-element cache `slot` and a flag `has`, and it adds a counter `remaining` that starts at `size`. The counter changes only in `next()`, so `remaining` is always `size` minus the number of taken elements, and a `peek()` cannot disturb it.

The changed failure contract lives in `peek()`. When the cache is empty, the method asks `source.hasNext()` first and throws before it assigns `slot` or `has`. That order makes the failed call a pure observation, so the same call can be repeated with the same result. Operation `next()` reuses `peek()`, which means it also throws before it decrements `remaining`.

**Complexity.**

- **Time** is O(1) per operation, because each call does a fixed number of field reads and at most one `source.next()`.
- **Space** is O(1) extra, because the wrapper stores one value, one flag and one counter beside the source.

```java run
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class PeekingCountdown {
    private final Iterator<Integer> source;
    private int remaining;
    private int slot;
    private boolean has;

    PeekingCountdown(Iterator<Integer> source, int size) {
        this.source = source;
        this.remaining = size;
    }

    /**
     * True when an element can still be taken.
     * Time: O(1). Space: O(1). Invariant: no field changes.
     */
    boolean hasNext() { return has || source.hasNext(); }

    /**
     * Shows the next element; on an exhausted wrapper it throws and changes nothing.
     * Time: O(1). Space: O(1).
     * Invariant: the cached slot, when full, holds the element after the last taken one.
     */
    int peek() {
        // Pull only when the cache is empty, so a repeated peek reuses the stored element.
        if (!has) {
            // Throw before any assignment so a failed call leaves slot, has and remaining unchanged.
            if (!source.hasNext()) throw new NoSuchElementException("exhausted");
            slot = source.next();
            has = true;
        }
        return slot;
    }

    /**
     * Takes the next element and counts it.
     * Time: O(1). Space: O(1). Invariant: remaining equals size minus taken.
     */
    int next() {
        // peek() throws first on an exhausted wrapper, so remaining never goes below zero.
        int value = peek();
        has = false;
        remaining--;
        return value;
    }

    /** Elements not yet taken; a peek never changes it. */
    int remaining() { return remaining; }

    static boolean peekThrows(PeekingCountdown p) {
        try { p.peek(); return false; } catch (NoSuchElementException e) { return true; }
    }

    public static void main(String[] args) {
        // Example 1: remaining is unchanged by the peek and drops by one per taken element.
        PeekingCountdown a = new PeekingCountdown(List.of(3, 8, 1).iterator(), 3);
        int[] seen = {a.peek(), a.remaining(), a.next(), a.remaining(), a.next(), a.next(), a.remaining()};
        int[] expected = {3, 3, 3, 2, 8, 1, 0};
        for (int i = 0; i < expected.length; i++) {
            if (seen[i] != expected[i]) throw new AssertionError("example 1 at " + i);
        }
        // Example 2: an empty source throws twice in a row with remaining still zero.
        PeekingCountdown e = new PeekingCountdown(new ArrayList<Integer>().iterator(), 0);
        if (e.hasNext() || e.remaining() != 0) throw new AssertionError("empty start");
        if (!peekThrows(e) || !peekThrows(e) || e.remaining() != 0) throw new AssertionError("repeated failing peek");
        // Random operation scripts replayed against a list model.
        Random rnd = new Random(284);
        for (int trial = 0; trial < 400; trial++) {
            int n = rnd.nextInt(8);
            List<Integer> model = new ArrayList<>();
            for (int i = 0; i < n; i++) model.add(rnd.nextInt(100));
            PeekingCountdown p = new PeekingCountdown(new ArrayList<>(model).iterator(), n);
            for (int step = 0; step < 25; step++) {
                int op = rnd.nextInt(4);
                if (op == 0) {
                    if (p.hasNext() != !model.isEmpty()) throw new AssertionError("hasNext");
                } else if (op == 1) {
                    if (model.isEmpty()) {
                        if (!peekThrows(p)) throw new AssertionError("peek should throw");
                    } else if (p.peek() != model.get(0)) throw new AssertionError("peek value");
                } else if (op == 2) {
                    if (model.isEmpty()) {
                        boolean t = false;
                        try { p.next(); } catch (NoSuchElementException ex) { t = true; }
                        if (!t) throw new AssertionError("next should throw");
                    } else if (p.next() != model.remove(0)) throw new AssertionError("next value");
                }
                // Every step, including failed ones, keeps the counter equal to the model size.
                if (p.remaining() != model.size()) throw new AssertionError("remaining");
            }
        }
    }
}
```

#### Solution: [Boundary] Repeated hasNext And Peek (Author exercise)
<!-- id: ds-repeated-has-next-peek -->

**Approach.**

The wrapper reads from the source only inside `peek()`, and only when the cache is empty. Operation `hasNext()` returns `has || source.hasNext()`, which asks the source for availability and never advances it. Both operations are therefore idempotent: the first call may fill the cache, and every repeat finds the state already in place.

A counting source wraps the real iterator and increments a counter after each successful `next()`. The invariant is that the counter equals the number of taken elements plus one when the cache is full. The hazards are checked in the harness. The class never overrides `remove()`, so the interface default throws. A list iterator detects a change on its next pull, so a cached element hides the change for one call. A boolean flag keeps a `null` element distinct from an empty cache, while unboxing that `null` into an `int` throws.

**Complexity.**

- **Time** is O(1) per operation, because each call performs at most one source call and constant field work.
- **Space** is O(1) extra, because the wrapper holds one element reference and one flag.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class RepeatedLookahead {
    /** Counts successful source.next() calls; hasNext() does not count. */
    static final class CountingSource<T> implements Iterator<T> {
        private final Iterator<T> inner;
        int calls;
        CountingSource(Iterator<T> inner) { this.inner = inner; }
        @Override public boolean hasNext() { return inner.hasNext(); }
        @Override public T next() {
            // Count only after the inner call succeeds, so a failed pull is not an advance.
            T value = inner.next();
            calls++;
            return value;
        }
    }

    /**
     * Wrapper with idempotent hasNext() and peek().
     * Time: O(1) per operation. Space: O(1).
     * Invariant: slot plus the source hold exactly the untaken elements, at most one in the slot.
     */
    static final class Lookahead<T> implements Iterator<T> {
        private final Iterator<T> source;
        private T slot;
        private boolean cached;

        Lookahead(Iterator<T> source) { this.source = source; }

        // Asks the source for availability only, so any number of calls consume nothing.
        @Override public boolean hasNext() { return cached || source.hasNext(); }

        T peek() {
            // The only place that pulls; the flag, not the value, says whether the slot is full.
            if (!cached) {
                slot = source.next();
                cached = true;
            }
            return slot;
        }

        @Override public T next() {
            // peek() throws on an exhausted source before this method changes any field.
            T value = peek();
            cached = false;
            slot = null;
            return value;
        }
    }

    public static void main(String[] args) {
        // Example 1: repeated hasNext and peek cost one advance in total.
        CountingSource<Integer> src = new CountingSource<>(List.of(6, 2, 9).iterator());
        Lookahead<Integer> la = new Lookahead<>(src);
        for (int i = 0; i < 3; i++) if (!la.hasNext()) throw new AssertionError("hasNext");
        for (int i = 0; i < 3; i++) if (la.peek() != 6) throw new AssertionError("peek");
        if (src.calls != 1) throw new AssertionError("one advance for six read-only calls");
        if (la.next() != 6 || !la.hasNext() || la.peek() != 2 || src.calls != 2) throw new AssertionError("second element");
        // Example 2: a failed peek on an exhausted wrapper is not an advance.
        CountingSource<Integer> one = new CountingSource<>(List.of(5).iterator());
        Lookahead<Integer> single = new Lookahead<>(one);
        if (single.peek() != 5 || single.next() != 5 || single.hasNext()) throw new AssertionError("single");
        boolean threw = false;
        try { single.peek(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw || one.calls != 1) throw new AssertionError("failed peek");
        // Java hazard 1: remove() is not overridden, so the Iterator default throws.
        threw = false;
        try { new Lookahead<>(new ArrayList<>(List.of(1)).iterator()).remove(); }
        catch (UnsupportedOperationException e) { threw = true; }
        if (!threw) throw new AssertionError("default remove");
        // Java hazard 2: ArrayList checks modCount in next(), so the cached element hides the change one call.
        List<Integer> list = new ArrayList<>(List.of(1, 2, 3));
        Lookahead<Integer> late = new Lookahead<>(list.iterator());
        if (late.peek() != 1) throw new AssertionError("first peek");
        list.add(4);
        if (late.next() != 1) throw new AssertionError("cached element still returned");
        threw = false;
        try { late.peek(); } catch (ConcurrentModificationException e) { threw = true; }
        if (!threw) throw new AssertionError("late ConcurrentModificationException");
        // Java hazard 3: a null element is a real element, and unboxing it throws.
        Lookahead<Integer> nulls = new Lookahead<>(Arrays.asList(1, null, 3).iterator());
        if (nulls.next() != 1) throw new AssertionError("before null");
        Integer boxed = nulls.peek();
        if (boxed != null || !nulls.hasNext()) throw new AssertionError("null stays an element");
        threw = false;
        try { int bad = boxed; if (bad == 0) bad++; } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("unboxing null");
        if (nulls.next() != null || nulls.next() != 3 || nulls.hasNext()) throw new AssertionError("after null");
        // Random scripts against a list model, checking the advance count on every step.
        Random rnd = new Random(341);
        for (int trial = 0; trial < 400; trial++) {
            int n = rnd.nextInt(8);
            List<Integer> data = new ArrayList<>();
            for (int i = 0; i < n; i++) data.add(rnd.nextInt(50));
            CountingSource<Integer> cs = new CountingSource<>(data.iterator());
            Lookahead<Integer> w = new Lookahead<>(cs);
            int taken = 0;
            boolean peeked = false;
            for (int step = 0; step < 30; step++) {
                int op = rnd.nextInt(3);
                boolean left = taken < n;
                if (op == 0) {
                    if (w.hasNext() != left) throw new AssertionError("hasNext");
                } else if (op == 1) {
                    try {
                        int v = w.peek();
                        if (!left || v != data.get(taken)) throw new AssertionError("peek value");
                        peeked = true;
                    } catch (NoSuchElementException e) {
                        if (left) throw new AssertionError("unexpected throw");
                    }
                } else {
                    try {
                        int v = w.next();
                        if (!left || v != data.get(taken)) throw new AssertionError("next value");
                        taken++;
                        peeked = false;
                    } catch (NoSuchElementException e) {
                        if (left) throw new AssertionError("unexpected throw");
                    }
                }
                if (cs.calls != taken + (peeked ? 1 : 0)) throw new AssertionError("advance count");
            }
        }
    }
}
```

#### Solution: [Recognize] Flatten Nested List Iterator (LeetCode 341)
<!-- id: ds-nested-item-flatten -->

**Approach.**

The lookahead idea from the earlier exercises carries over, but the next integer is no longer one step away. The class keeps a stack of iterators, one per list that is entered and not yet finished, and a cache `pending` for the next integer it has found. The invariant is that the stack iterators, from top to bottom, hold exactly the unvisited items in order, and `pending` holds at most one integer that precedes all of them.

Operation `hasNext()` scans only while the cache is empty. It looks at the top iterator. If that iterator has no item, it pops the frame. If the item is an integer, the scan stores it and stops. If the item is a list, the scan pushes an iterator over its children and continues, so an empty list is entered and popped without producing a value. Repeated `hasNext()` calls stop at the first test, which makes them idempotent. Operation `next()` calls `hasNext()`, clears the cache and returns the integer.

**Complexity.**

- **Time** is O(1) amortized per call, because each item is pushed or visited once and each frame is popped once, so total work over all calls is proportional to the item count.
- **Space** is O(d), where d is the maximum list nesting depth, because the stack holds at most one iterator per open level.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class NestedFlattener {
    interface NestedItem {
        boolean isInt();
        int value();
        List<NestedItem> children();
    }

    record IntItem(int value) implements NestedItem {
        public boolean isInt() { return true; }
        public List<NestedItem> children() { throw new UnsupportedOperationException("an integer has no children"); }
    }

    record ListItem(List<NestedItem> children) implements NestedItem {
        public boolean isInt() { return false; }
        public int value() { throw new UnsupportedOperationException("a list has no value"); }
    }

    private final Deque<Iterator<NestedItem>> stack = new ArrayDeque<>();
    private int pending;
    private boolean hasPending;

    NestedFlattener(List<NestedItem> top) { stack.push(top.iterator()); }

    /**
     * Finds the next integer without consuming it; repeated calls do nothing after the first.
     * Time: O(1) amortized, each item and frame is handled once overall. Space: O(d) for the stack.
     * Invariant: the stack iterators hold exactly the unvisited items, and pending precedes them.
     */
    boolean hasNext() {
        // Scan only while no integer is cached, so a second hasNext() returns immediately.
        while (!hasPending && !stack.isEmpty()) {
            Iterator<NestedItem> top = stack.peek();
            if (!top.hasNext()) {
                // The innermost list is finished, so its frame leaves the stack.
                stack.pop();
            } else {
                NestedItem item = top.next();
                if (item.isInt()) {
                    // An integer ends the scan and waits in the cache.
                    pending = item.value();
                    hasPending = true;
                } else {
                    // A list opens a frame; an empty list is popped on the next pass.
                    stack.push(item.children().iterator());
                }
            }
        }
        return hasPending;
    }

    /** Returns the next integer. Time: O(1) amortized. Space: O(d). */
    int next() {
        // hasNext() fills the cache, or this call fails before changing any state.
        if (!hasNext()) throw new NoSuchElementException("no integer left");
        hasPending = false;
        return pending;
    }

    /** Number of iterators currently on the stack, including the top-level list. */
    int liveFrames() { return stack.size(); }

    static NestedItem i(int v) { return new IntItem(v); }
    static NestedItem l(NestedItem... items) { return new ListItem(List.of(items)); }

    static List<NestedItem> gen(Random rnd, int depth) {
        List<NestedItem> out = new ArrayList<>();
        int size = rnd.nextInt(5);
        for (int k = 0; k < size; k++) {
            if (depth < 5 && rnd.nextInt(3) == 0) out.add(new ListItem(gen(rnd, depth + 1)));
            else out.add(new IntItem(rnd.nextInt(21) - 10));
        }
        return out;
    }

    // Oracle: plain recursion that appends every integer in order.
    static void flatten(List<NestedItem> items, List<Integer> sink) {
        for (NestedItem it : items) {
            if (it.isInt()) sink.add(it.value());
            else flatten(it.children(), sink);
        }
    }

    static int depthOf(List<NestedItem> items) {
        int best = 0;
        for (NestedItem it : items) if (!it.isInt()) best = Math.max(best, depthOf(it.children()));
        return best + 1;
    }

    public static void main(String[] args) {
        // Example 1: [[1,[2]],[],3] yields 1, 2, 3 with live frames 2, 3, 1 after each next().
        NestedFlattener f = new NestedFlattener(List.of(l(i(1), l(i(2))), l(), i(3)));
        if (f.liveFrames() != 1) throw new AssertionError("only the top-level frame before any call");
        int[] values = new int[3];
        int[] frames = new int[3];
        for (int k = 0; k < 3; k++) {
            values[k] = f.next();
            frames[k] = f.liveFrames();
        }
        if (values[0] != 1 || values[1] != 2 || values[2] != 3) throw new AssertionError("example 1 values");
        if (frames[0] != 2 || frames[1] != 3 || frames[2] != 1) throw new AssertionError("example 1 frames");
        if (f.hasNext() || f.liveFrames() != 0) throw new AssertionError("finished stack is empty");
        // Example 2: only empty lists, so hasNext() is false and every frame is popped.
        NestedFlattener e = new NestedFlattener(List.of(l(l()), l(l())));
        if (e.liveFrames() != 1 || e.hasNext() || e.liveFrames() != 0) throw new AssertionError("example 2");
        boolean threw = false;
        try { e.next(); } catch (NoSuchElementException ex) { threw = true; }
        if (!threw) throw new AssertionError("next on finished");
        // Random nested inputs against recursive flattening.
        Random rnd = new Random(2026);
        for (int trial = 0; trial < 500; trial++) {
            List<NestedItem> top = gen(rnd, 1);
            List<Integer> expected = new ArrayList<>();
            flatten(top, expected);
            int maxFrames = depthOf(top);
            NestedFlattener it = new NestedFlattener(top);
            List<Integer> got = new ArrayList<>();
            while (true) {
                // Repeated hasNext() calls must agree and must not change the frame count.
                boolean first = it.hasNext();
                int framesAfter = it.liveFrames();
                for (int r = rnd.nextInt(3); r > 0; r--) {
                    if (it.hasNext() != first || it.liveFrames() != framesAfter) throw new AssertionError("hasNext not idempotent");
                }
                if (framesAfter > maxFrames) throw new AssertionError("more frames than nesting levels");
                if (!first) {
                    if (framesAfter != 0) throw new AssertionError("frames left after the end");
                    break;
                }
                if (framesAfter < 1) throw new AssertionError("an integer needs a live frame");
                got.add(it.next());
            }
            if (!got.equals(expected)) throw new AssertionError("flattened order " + got + " vs " + expected);
        }
    }
}
```
