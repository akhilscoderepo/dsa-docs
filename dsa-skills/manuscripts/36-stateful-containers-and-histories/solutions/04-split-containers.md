<!-- solutions-for: 04-split-containers -->
### Solutions For Split Containers

#### Solution: [Build] Balanced Two-Deque Sequence (Author exercise)
<!-- id: sc-split-balanced-sequence -->

**Approach.**
The sequence is the left deque followed by the right deque. Each push touches one end of one deque: `pushFront` adds to the front of the left deque, and `pushBack` adds to the back of the right deque. That single insertion leaves the sizes off by one element in one direction only. A private method `rebalance` then repairs it. If the left deque is longer, its last element becomes the first element of the right deque. If the right deque is two elements longer, its first element becomes the last element of the left deque. A move across the boundary keeps the order of the whole sequence, because the moved element stays adjacent to the same neighbours.

The invariant is that `right.size() - left.size()` is 0 or 1 whenever a public method returns. Equivalently, the left deque holds exactly `size / 2` elements. Only `rebalance` moves elements between the deques, so the repair lives in one place and the push methods cannot disagree about it.

**Complexity.**
- **Time** is O(1) per push, because each call makes one deque insertion and at most one move.
- **Space** is O(n) for the n stored elements, with O(1) extra per call; `toArray` allocates O(n) only when it is called.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class BalancedSequenceBuild {
    /** Sequence stored as the left deque followed by the right deque. */
    static final class BalancedSequence {
        // Left deque holds the first size() / 2 elements, in sequence order.
        private final Deque<Integer> left = new ArrayDeque<>();
        // Right deque holds the remaining elements, so it is never smaller than left.
        private final Deque<Integer> right = new ArrayDeque<>();

        /**
         * Restores the invariant right.size() - left.size() in {0, 1} after one insertion.
         * Time: O(1), because at most one element moves between the deques.
         * Space: O(1), because no new container is created.
         * Invariant: the sequence order left + right is unchanged by the move.
         */
        private void rebalance() {
            // The left deque is too long by one: its last element becomes the first of the right deque.
            if (left.size() > right.size()) right.offerFirst(left.pollLast());
            // The right deque is too long by two: its first element becomes the last of the left deque.
            else if (right.size() > left.size() + 1) left.offerLast(right.pollFirst());
        }

        /** Inserts v before every element. Time: O(1). Space: O(1). Invariant: rebalance runs before returning. */
        void pushFront(int v) {
            // The new element becomes the first element of the left deque.
            left.offerFirst(v);
            // Insertion can leave left one element too long.
            rebalance();
        }

        /** Inserts v after every element. Time: O(1). Space: O(1). Invariant: rebalance runs before returning. */
        void pushBack(int v) {
            // The new element becomes the last element of the right deque.
            right.offerLast(v);
            // Insertion can leave right two elements longer than left.
            rebalance();
        }

        /** Returns {left size, right size}. Time: O(1). Space: O(1). */
        int[] sizes() {
            // Deque.size() is constant time for ArrayDeque.
            return new int[] {left.size(), right.size()};
        }

        /** Returns the whole sequence in order. Time: O(n). Space: O(n). */
        int[] toArray() {
            // Copy left first, then right, which is the sequence order.
            List<Integer> all = new ArrayList<>(left);
            all.addAll(right);
            int[] res = new int[all.size()];
            // One pass unboxes each element.
            for (int i = 0; i < res.length; i++) res[i] = all.get(i);
            return res;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise: four calls leave two elements in each deque.
        BalancedSequence s = new BalancedSequence();
        s.pushBack(1); s.pushBack(2); s.pushFront(0); s.pushBack(3);
        if (!Arrays.equals(s.toArray(), new int[] {0, 1, 2, 3}) || !Arrays.equals(s.sizes(), new int[] {2, 2})) throw new AssertionError("example 1");
        // Example 2: odd total size puts the extra element in the right deque.
        s = new BalancedSequence();
        s.pushFront(7); s.pushFront(6); s.pushBack(8); s.pushBack(9); s.pushBack(10);
        if (!Arrays.equals(s.toArray(), new int[] {6, 7, 8, 9, 10}) || !Arrays.equals(s.sizes(), new int[] {2, 3})) throw new AssertionError("example 2");
        // An empty sequence has two empty deques.
        if (!Arrays.equals(new BalancedSequence().sizes(), new int[] {0, 0})) throw new AssertionError("empty");
        // Random comparison with a plain list; the invariant is checked after every call.
        Random rnd = new Random(3601L);
        for (int t = 0; t < 2000; t++) {
            BalancedSequence b = new BalancedSequence();
            List<Integer> oracle = new ArrayList<>();
            for (int i = rnd.nextInt(30); i > 0; i--) {
                int v = rnd.nextInt(100);
                // The oracle inserts at index 0 or at the end, which is the definition of the two calls.
                if (rnd.nextBoolean()) { b.pushFront(v); oracle.add(0, v); } else { b.pushBack(v); oracle.add(v); }
                int[] sz = b.sizes();
                if (sz[1] - sz[0] != 0 && sz[1] - sz[0] != 1) throw new AssertionError("unbalanced");
                if (sz[0] != oracle.size() / 2) throw new AssertionError("boundary position");
            }
            int[] got = b.toArray();
            for (int i = 0; i < got.length; i++) if (got[i] != oracle.get(i)) throw new AssertionError("order");
            if (got.length != oracle.size()) throw new AssertionError("length");
        }
    }
}
```

#### Solution: [Vary] Design Front Middle Back Queue (LeetCode 1670)
<!-- id: sc-split-front-middle-back -->

**Approach.**
The same two deques now serve six calls. A middle push inserts at index `size / 2`, which equals the length of the left deque, so the value goes to the back of the left deque. A middle pop removes index `(size - 1) / 2`. When the sizes are equal, the size is even and that index is the last element of the left deque, which is the frontmost of the two middle elements. When the right deque is longer, the size is odd and the middle is the first element of the right deque. Front and back pops take the first element of the left deque (or of the right deque when the left deque is empty) and the last element of the right deque.

The invariant is that the left deque holds `size / 2` elements after each call. The test for an empty queue reads the right deque only, because that deque is empty exactly when the whole queue is empty.

**Complexity.**
- **Time** is O(1) per call, because each call does one deque operation and at most one move in `rebalance`.
- **Space** is O(n) for n stored elements, with no extra memory per call.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class FrontMiddleBackQueue {
    // Left deque holds the first size() / 2 elements; right deque holds the rest.
    private final Deque<Integer> left = new ArrayDeque<>();
    private final Deque<Integer> right = new ArrayDeque<>();

    /**
     * Restores right.size() - left.size() in {0, 1}; the single owner of cross-deque moves.
     * Time: O(1), because at most one element moves. Space: O(1).
     * Invariant: the order left + right never changes.
     */
    private void rebalance() {
        // Left too long: its last element joins the front of right.
        if (left.size() > right.size()) right.offerFirst(left.pollLast());
        // Right too long: its first element joins the back of left.
        else if (right.size() > left.size() + 1) left.offerLast(right.pollFirst());
    }

    /** Inserts at index 0. Time: O(1). Space: O(1). */
    void pushFront(int v) { left.offerFirst(v); rebalance(); }

    /** Inserts at index size() / 2, which is the end of the left deque. Time: O(1). Space: O(1). */
    void pushMiddle(int v) { left.offerLast(v); rebalance(); }

    /** Appends at the end. Time: O(1). Space: O(1). */
    void pushBack(int v) { right.offerLast(v); rebalance(); }

    /** Removes index 0, or returns -1 when empty. Time: O(1). Space: O(1). */
    int popFront() {
        // Empty check first: the polls below would return null and unboxing would throw.
        if (left.isEmpty() && right.isEmpty()) return -1;
        // A single element lives in the right deque, so the left deque can be empty.
        int v = left.isEmpty() ? right.pollFirst() : left.pollFirst();
        rebalance();
        return v;
    }

    /**
     * Removes index (size - 1) / 2, the first of the two middle elements when size is even; -1 when empty.
     * Time: O(1). Space: O(1).
     */
    int popMiddle() {
        if (left.isEmpty() && right.isEmpty()) return -1;
        // Equal sizes: the frontmost middle is the last of left. Odd size: the middle is the first of right.
        int v = left.size() == right.size() ? left.pollLast() : right.pollFirst();
        rebalance();
        return v;
    }

    /** Removes the last element, or returns -1 when empty. Time: O(1). Space: O(1). */
    int popBack() {
        // The right deque holds the extra element, so it is empty only when the whole queue is empty.
        if (right.isEmpty()) return -1;
        int v = right.pollLast();
        rebalance();
        return v;
    }

    /** Reference queue: one list, with the middle indexes written out by their definitions. Time: O(n) per call. */
    static final class Oracle {
        final List<Integer> a = new ArrayList<>();
        void pushFront(int v) { a.add(0, v); }
        void pushMiddle(int v) { a.add(a.size() / 2, v); }
        void pushBack(int v) { a.add(v); }
        int popFront() { return a.isEmpty() ? -1 : a.remove(0); }
        int popMiddle() { return a.isEmpty() ? -1 : a.remove((a.size() - 1) / 2); }
        int popBack() { return a.isEmpty() ? -1 : a.remove(a.size() - 1); }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        FrontMiddleBackQueue q = new FrontMiddleBackQueue();
        q.pushFront(1); q.pushBack(2); q.pushBack(3); q.pushMiddle(4); q.pushMiddle(5);
        int[] got = {q.popMiddle(), q.popMiddle(), q.popFront(), q.popBack(), q.popMiddle(), q.popMiddle()};
        int[] want = {5, 4, 1, 3, 2, -1};
        for (int i = 0; i < want.length; i++) if (got[i] != want[i]) throw new AssertionError("example 1 at " + i);
        // Example 2: with two middle elements, popMiddle removes the frontmost one.
        q = new FrontMiddleBackQueue();
        q.pushFront(1); q.pushBack(2); q.pushMiddle(3); q.pushMiddle(4);
        if (q.popMiddle() != 4 || q.popBack() != 2 || q.popFront() != 1 || q.popMiddle() != 3) throw new AssertionError("example 2");
        // Java claim behind the empty guard: ArrayDeque.pollFirst returns null when empty.
        if (new ArrayDeque<Integer>().pollFirst() != null) throw new AssertionError("poll on empty");
        // Java claim behind the guard in the pop methods: removeFirst on an empty deque throws NoSuchElementException.
        try { new ArrayDeque<Integer>().removeFirst(); throw new AssertionError("no exception"); } catch (java.util.NoSuchElementException expected) { }
        // Random sequences of all six calls, checked against the oracle after every call.
        Random rnd = new Random(3602L);
        for (int t = 0; t < 3000; t++) {
            FrontMiddleBackQueue f = new FrontMiddleBackQueue();
            Oracle o = new Oracle();
            for (int i = rnd.nextInt(40); i > 0; i--) {
                int op = rnd.nextInt(6), v = 1 + rnd.nextInt(1000);
                switch (op) {
                    case 0 -> { f.pushFront(v); o.pushFront(v); }
                    case 1 -> { f.pushMiddle(v); o.pushMiddle(v); }
                    case 2 -> { f.pushBack(v); o.pushBack(v); }
                    case 3 -> { if (f.popFront() != o.popFront()) throw new AssertionError("popFront"); }
                    case 4 -> { if (f.popMiddle() != o.popMiddle()) throw new AssertionError("popMiddle"); }
                    default -> { if (f.popBack() != o.popBack()) throw new AssertionError("popBack"); }
                }
                // Boundary check: the left deque always holds exactly size / 2 elements.
                if (f.left.size() != o.a.size() / 2 || f.right.size() != o.a.size() - o.a.size() / 2) throw new AssertionError("balance");
            }
        }
    }
}
```

#### Solution: [Boundary] Oscillating Empty Halves (Author exercise)
<!-- id: sc-split-oscillating -->

**Approach.**
The risky states are size 0 and size 1. At size 1 the left deque is empty and the only element is the first of the right deque, so a middle removal must read the right deque and leave both deques empty. At size 0 the removal reports -1 and leaves the state alone. When the sizes are equal and non-zero, the middle is the last element of the left deque. After each operation the size changes by at most one, so one call to `rebalance` is always enough, including the first insertion into two empty deques: the new element goes to the left deque and crosses to the right deque at once.

The invariant is that the left deque holds `size / 2` elements after every operation. The random test in `main` removes more often than it inserts, so the sequence visits the empty state many times, and it checks the balance after each run and compares the removed values with a single-list oracle.

**Complexity.**
- **Time** is O(q) for q operations, because each operation does constant work and at most one move.
- **Space** is O(n) for the live elements plus O(r) for the r returned values.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class OscillatingHalves {
    // Left deque holds the first size / 2 elements, right deque the rest.
    static final Deque<Integer> left = new ArrayDeque<>();
    static final Deque<Integer> right = new ArrayDeque<>();

    /**
     * Moves at most one element so that right.size() - left.size() is 0 or 1.
     * Time: O(1). Space: O(1).
     * Invariant: the order left + right is unchanged.
     */
    static void rebalance() {
        // Left holds one element too many.
        if (left.size() > right.size()) right.offerFirst(left.pollLast());
        // Right holds two elements more than left.
        else if (right.size() > left.size() + 1) left.offerLast(right.pollFirst());
    }

    /**
     * Applies the operations: a positive value inserts at index size / 2, zero removes index (size - 1) / 2.
     * Returns the removed values in order, with -1 for a removal from an empty sequence.
     * Time: O(q) for q operations, because each operation does O(1) work and moves at most one element.
     * Space: O(n) for the sequence and O(r) for the r removed values.
     * Invariant: after every operation, left.size() equals size / 2.
     */
    static int[] run(int[] ops) {
        left.clear();
        right.clear();
        List<Integer> removed = new ArrayList<>();
        // One pass over the operations; each costs O(1).
        for (int op : ops) {
            if (op > 0) {
                // Insertion at index size / 2 is the end of the left deque.
                left.offerLast(op);
            } else if (left.isEmpty() && right.isEmpty()) {
                // Both deques empty: nothing to remove, report -1.
                removed.add(-1);
            } else if (left.size() == right.size()) {
                // Even size: the frontmost middle is the last element of left.
                removed.add(left.pollLast());
            } else {
                // Odd size: the middle is the first element of right, and left may be empty (size 1).
                removed.add(right.pollFirst());
            }
            // Every operation changes the size by one, so one move restores the invariant.
            rebalance();
        }
        int[] res = new int[removed.size()];
        for (int i = 0; i < res.length; i++) res[i] = removed.get(i);
        return res;
    }

    /** Reference: one list with the indexes from the definition. Time: O(q * n). Space: O(n). */
    static int[] oracle(int[] ops) {
        List<Integer> a = new ArrayList<>(), removed = new ArrayList<>();
        for (int op : ops) {
            if (op > 0) a.add(a.size() / 2, op);
            else removed.add(a.isEmpty() ? -1 : a.remove((a.size() - 1) / 2));
        }
        return removed.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Example 1: the sequence empties twice and refills.
        if (!Arrays.equals(run(new int[] {1, 2, 0, 0, 0, 3, 0}), new int[] {2, 1, -1, 3})) throw new AssertionError("example 1");
        // Example 2: removals from a four-element sequence drain it to empty and past it.
        if (!Arrays.equals(run(new int[] {1, 2, 3, 4, 0, 0, 0, 0, 0}), new int[] {4, 3, 2, 1, -1})) throw new AssertionError("example 2");
        // After a drain both deques are empty, which is the state the next insertion must start from.
        if (!left.isEmpty() || !right.isEmpty()) throw new AssertionError("not empty after drain");
        // Random runs with many removals so the sequence hovers around empty.
        Random rnd = new Random(3603L);
        for (int t = 0; t < 5000; t++) {
            int[] ops = new int[rnd.nextInt(40)];
            for (int i = 0; i < ops.length; i++) ops[i] = rnd.nextInt(5) < 2 ? 1 + rnd.nextInt(50) : 0;
            if (!Arrays.equals(run(ops), oracle(ops))) throw new AssertionError("mismatch " + Arrays.toString(ops));
            // The final state must satisfy the balance invariant too.
            if (right.size() - left.size() < 0 || right.size() - left.size() > 1) throw new AssertionError("final balance");
        }
    }
}
```

#### Solution: [Recognize] Dinner Plate Stacks (LeetCode 1172)
<!-- id: sc-split-dinner-plates -->

**Approach.**
Two queries need two orders. A push needs the smallest index among stacks with room, so the structure keeps a `TreeSet` of those indexes, ordered ascending. A pop needs the largest index among non-empty stacks, which is the last stack in the list once empty stacks at the end are trimmed. The stale-entry policy is that the set is exact: an index is in the set if and only if its stack exists and is not full. A push removes the index when the stack becomes full, a pop at a stack adds the index back, and trimming a stack from the end also removes its index from the set. With no stale entries, `first()` is always a valid target and no lazy skipping is needed.

The invariant ties the list and the set together after every call. Trimming is safe because an empty trailing stack behaves the same as a missing one: a later push would create it again at the same index.

**Complexity.**
- **Time** is O(log s) per call for s stacks, because the set operations are logarithmic and each stack is trimmed at most once after it is created.
- **Space** is O(n + s) for n stored values and the set of at most s indexes.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class DinnerPlates {
    // Stack i is stacks.get(i); a stack is bounded by capacity.
    private final int capacity;
    private final List<Deque<Integer>> stacks = new ArrayList<>();
    // Ordering: ascending stack index. Policy: holds exactly the indexes of existing stacks that are not full, with no stale entries.
    private final TreeSet<Integer> writable = new TreeSet<>();

    DinnerPlates(int capacity) { this.capacity = capacity; }

    /**
     * Pushes onto the leftmost stack that is not full.
     * Time: O(log s) for s stacks, because TreeSet.first and remove are logarithmic. Space: O(1) extra.
     * Invariant: writable holds every non-full stack index and nothing else.
     */
    void push(int val) {
        // No writable stack: create the next stack and register it as writable.
        if (writable.isEmpty()) {
            stacks.add(new ArrayDeque<>());
            writable.add(stacks.size() - 1);
        }
        // The smallest writable index is the leftmost stack with room.
        int i = writable.first();
        stacks.get(i).push(val);
        // A stack that just became full leaves the set, which keeps the set exact.
        if (stacks.get(i).size() == capacity) writable.remove(i);
    }

    /**
     * Pops from the rightmost non-empty stack, or returns -1.
     * Time: amortized O(log s), because each stack is trimmed once after it was created. Space: O(1).
     */
    int pop() {
        // Trim trailing empty stacks, and drop them from the set so no entry refers to a removed stack.
        while (!stacks.isEmpty() && stacks.get(stacks.size() - 1).isEmpty()) {
            writable.remove(stacks.size() - 1);
            stacks.remove(stacks.size() - 1);
        }
        if (stacks.isEmpty()) return -1;
        return popAtStack(stacks.size() - 1);
    }

    /**
     * Pops from stack index, or returns -1 when the index is out of range or the stack is empty.
     * Time: O(log s). Space: O(1).
     * Invariant: after the pop the stack is not full, so its index is in writable.
     */
    int popAtStack(int index) {
        // Index beyond the list means the stack was never created or was trimmed, so it is empty.
        if (index >= stacks.size() || stacks.get(index).isEmpty()) return -1;
        int v = stacks.get(index).pop();
        // Add is idempotent for a TreeSet, so a stack that was already writable stays listed once.
        writable.add(index);
        return v;
    }

    /** Reference: unbounded list of lists scanned linearly. Time: O(s) per call. Space: O(total elements). */
    static final class Oracle {
        final int cap;
        final List<List<Integer>> st = new ArrayList<>();
        Oracle(int cap) { this.cap = cap; }
        void push(int v) {
            for (List<Integer> s : st) if (s.size() < cap) { s.add(v); return; }
            List<Integer> s = new ArrayList<>();
            s.add(v);
            st.add(s);
        }
        int pop() {
            for (int i = st.size() - 1; i >= 0; i--) if (!st.get(i).isEmpty()) return st.get(i).remove(st.get(i).size() - 1);
            return -1;
        }
        int popAtStack(int i) {
            if (i >= st.size() || st.get(i).isEmpty()) return -1;
            return st.get(i).remove(st.get(i).size() - 1);
        }
    }

    public static void main(String[] args) {
        // Example 1: capacity 2; a hole at stack 0 is refilled before a new stack is opened.
        DinnerPlates d;
        d = new DinnerPlates(2);
        for (int v = 1; v <= 5; v++) d.push(v);
        if (d.popAtStack(0) != 2) throw new AssertionError("ex1 a");
        d.push(20); d.push(21);
        int[] want = {21, 4, 5, 3, 20, 1};
        int[] seq = {d.pop(), d.popAtStack(1), d.pop(), d.pop(), d.pop(), d.pop()};
        for (int i = 0; i < want.length; i++) if (seq[i] != want[i]) throw new AssertionError("ex1 at " + i);
        // Example 2: capacity 1; an out-of-range index and an emptied structure both return -1.
        d = new DinnerPlates(1);
        d.push(7); d.push(8);
        if (d.popAtStack(0) != 7) throw new AssertionError("ex2 a");
        d.push(9);
        if (d.popAtStack(5) != -1 || d.pop() != 8 || d.pop() != 9 || d.pop() != -1) throw new AssertionError("ex2 b");
        // Random sequences against the oracle, with small capacities so stacks fill and empty often.
        Random rnd = new Random(3604L);
        for (int t = 0; t < 3000; t++) {
            int cap = 1 + rnd.nextInt(3);
            DinnerPlates f = new DinnerPlates(cap);
            Oracle o = new Oracle(cap);
            for (int i = rnd.nextInt(60); i > 0; i--) {
                int op = rnd.nextInt(5), v = 1 + rnd.nextInt(100);
                if (op <= 1) { f.push(v); o.push(v); }
                else if (op == 2) { if (f.pop() != o.pop()) throw new AssertionError("pop"); }
                else { int idx = rnd.nextInt(5); if (f.popAtStack(idx) != o.popAtStack(idx)) throw new AssertionError("popAtStack"); }
                // The set must equal the non-full indexes exactly: no stale and no missing entries.
                TreeSet<Integer> expect = new TreeSet<>();
                for (int k = 0; k < f.stacks.size(); k++) if (f.stacks.get(k).size() < cap) expect.add(k);
                if (!expect.equals(f.writable)) throw new AssertionError("stale or missing entry");
            }
        }
    }
}
```
