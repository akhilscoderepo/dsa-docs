<!-- solutions-for: 92-multiple-collections-ownership -->
### Solutions For Multiple Collections Ownership

#### Solution: [Build] Reusable-ID Pool (Author exercise)
<!-- id: mco-reusable-id-pool -->

**Approach.**
The pool stores three facts. The integer `frontier` says that every id at or above it is never issued. The `PriorityQueue` named `returnedHeap` gives the smallest returned id. The `HashSet` named `returnedSet` answers whether an id waits for reuse. Allocation prefers the heap, because every returned id lies below the frontier and is therefore smaller than the next fresh id. Release first derives the state of the id and rejects anything that is not allocated, so a repeated or never-issued id cannot enter the stores.

The invariant is that the heap and the set hold the same ids, each id once, all below the frontier. Two private helpers are the only code that touches the stores, so a public method cannot update one store and forget the other. The stale-entry policy is eager: no store ever holds an id that the other has dropped. The main method checks this equality after every random call.

**Complexity.**
- **Time** is O(log k) per allocate and release, where k is the number of returned ids, because the heap dominates and the set costs expected O(1).
- **Space** is O(k) for the two stores plus O(1) for the frontier, and k never exceeds the frontier.

```java run
import java.util.*;

public final class ReusableIdPool {
    static final class IdPool {
        static final int NEVER_ISSUED = 0, ALLOCATED = 1, RETURNED = 2;
        private final int capacity;
        private int frontier = 0;
        private final PriorityQueue<Integer> returnedHeap = new PriorityQueue<>();
        private final Set<Integer> returnedSet = new HashSet<>();

        IdPool(int capacity) { this.capacity = capacity; }

        /** Adds an id to both stores. Time: O(log k). Space: O(1). Invariant: heap and set stay equal. */
        private void putReturned(int id) { returnedHeap.add(id); returnedSet.add(id); }

        /** Removes the smallest returned id from both stores. Time: O(log k). Space: O(1). Invariant: heap and set stay equal. */
        private int takeReturned() {
            // The heap yields the smallest returned id.
            int id = returnedHeap.poll();
            // The set drops the same id so that the two stores agree.
            returnedSet.remove(id);
            return id;
        }

        /** Derives the state of an id. Time: expected O(1). Space: O(1). Invariant: states partition the valid ids. */
        int state(int id) {
            // Ids outside the valid range have no state.
            if (id < 0 || id >= capacity) throw new IllegalArgumentException("id out of range: " + id);
            // Every id at or above the frontier was never issued.
            if (id >= frontier) return NEVER_ISSUED;
            // Below the frontier, the set separates returned ids from allocated ones.
            return returnedSet.contains(id) ? RETURNED : ALLOCATED;
        }

        /** Returns the smallest available id or -1. Time: O(log k). Space: O(1). Invariant: returned ids are below the frontier. */
        int allocate() {
            // A returned id is smaller than any never-issued id.
            if (!returnedHeap.isEmpty()) return takeReturned();
            // Otherwise issue the frontier id and advance the frontier.
            if (frontier < capacity) return frontier++;
            // No id is available.
            return -1;
        }

        /** Returns an allocated id to the pool. Time: O(log k). Space: O(1). Invariant: a throwing call changes nothing. */
        void release(int id) {
            // Validation happens before any store changes.
            if (state(id) != ALLOCATED) throw new IllegalStateException("id is not allocated: " + id);
            putReturned(id);
        }

        /** Checks that both stores agree. Time: O(k log k). Space: O(k). Invariant: same ids, each below the frontier. */
        boolean consistent() {
            // Equal sizes and equal contents mean no duplicate in the heap.
            if (returnedHeap.size() != returnedSet.size()) return false;
            for (int id : returnedHeap) if (!returnedSet.contains(id) || id >= frontier) return false;
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1: capacity 3 exhausts after three ids.
        IdPool a = new IdPool(3);
        int[] first = {a.allocate(), a.allocate(), a.allocate(), a.allocate()};
        if (!Arrays.equals(first, new int[] {0, 1, 2, -1})) throw new AssertionError("example 1");
        // Example 2: reuse in numeric order, then a rejected repeat release.
        IdPool b = new IdPool(5);
        b.allocate(); b.allocate(); b.allocate();
        b.release(1); b.release(0);
        try { b.release(1); throw new AssertionError("repeat release accepted"); } catch (IllegalStateException expected) { }
        int[] next = {b.allocate(), b.allocate(), b.allocate()};
        if (!Arrays.equals(next, new int[] {0, 1, 3})) throw new AssertionError("example 2");
        // Never-issued and out-of-range ids are rejected with the documented exceptions.
        try { b.release(4); throw new AssertionError("never-issued accepted"); } catch (IllegalStateException expected) { }
        try { b.release(5); throw new AssertionError("range accepted"); } catch (IllegalArgumentException expected) { }
        // Random comparison with a boolean-array oracle.
        Random rnd = new Random(3692L);
        for (int t = 0; t < 3000; t++) {
            int cap = 1 + rnd.nextInt(6);
            IdPool pool = new IdPool(cap);
            boolean[] used = new boolean[cap];
            boolean[] ever = new boolean[cap];
            for (int step = 0; step < 40; step++) {
                if (rnd.nextBoolean()) {
                    // Oracle: scan for the smallest unused id.
                    int want = -1;
                    for (int i = 0; i < cap; i++) if (!used[i]) { want = i; break; }
                    int got = pool.allocate();
                    if (got != want) throw new AssertionError("allocate " + got + " vs " + want);
                    if (want >= 0) { used[want] = true; ever[want] = true; }
                } else {
                    int id = rnd.nextInt(cap + 2) - 1;
                    boolean valid = id >= 0 && id < cap;
                    if (valid && used[id]) { pool.release(id); used[id] = false; }
                    else {
                        // Every other release must throw the documented exception and change nothing.
                        try { pool.release(id); throw new AssertionError("accepted " + id); }
                        catch (IllegalArgumentException e) { if (valid) throw new AssertionError("wrong exception"); }
                        catch (IllegalStateException e) { if (!valid) throw new AssertionError("wrong exception"); }
                    }
                }
                // The state of every id agrees with the oracle and both stores agree.
                for (int i = 0; i < cap; i++) {
                    int want = !ever[i] ? 0 : used[i] ? 1 : 2;
                    if (pool.state(i) != want) throw new AssertionError("state of " + i);
                }
                if (!pool.consistent()) throw new AssertionError("stores disagree");
            }
        }
    }
}
```

#### Solution: [Vary] Smallest Number In Infinite Set (LeetCode 2336)
<!-- id: mco-infinite-set-treeset -->

**Approach.**
The set has two regions. Every integer at or above `frontier` has never been popped, and the `TreeSet` named `addedBack` holds exactly the values below the frontier that were popped and then restored. Popping takes the first element of the `TreeSet` when it is not empty, because every such value is smaller than the frontier, and otherwise takes the frontier itself. The method `addBack` ignores values at or above the frontier, since they were never removed. For a value below the frontier, the result of `TreeSet.add` is true exactly when the value was removed, so the same call both ignores a duplicate and decides whether the removed count drops.

The invariant is `removed == frontier - 1 - addedBack.size()`, which counts the popped values minus the restored ones. The main method checks that equation after every operation, and it compares every pop with a boolean-array oracle.

**Complexity.**
- **Time** is O(log k) per call for k restored values, because `pollFirst` and `add` on a `TreeSet` are logarithmic.
- **Space** is O(k) for the restored values, and the infinite range costs one integer.

```java run
import java.util.*;

public final class InfiniteSetTree {
    static final class InfiniteSet {
        private int frontier = 1;
        private final TreeSet<Integer> addedBack = new TreeSet<>();
        private int removed = 0;

        /** Removes and returns the smallest value. Time: O(log k). Space: O(1). Invariant: removed == frontier - 1 - addedBack.size(). */
        int popSmallest() {
            int v;
            // Restored values are all below the frontier, so they come first.
            if (!addedBack.isEmpty()) v = addedBack.pollFirst();
            // Otherwise the frontier is the smallest present value.
            else v = frontier++;
            removed++;
            return v;
        }

        /** Restores a removed value. Time: O(log k). Space: O(1). Invariant: values at or above the frontier are never stored. */
        void addBack(int num) {
            // A value at or above the frontier was never removed.
            if (num >= frontier) return;
            // add returns true only when the value was absent, meaning it was removed.
            if (addedBack.add(num)) removed--;
        }

        /** Counts removed values. Time: O(1). Space: O(1). Invariant: equals popped values minus restored values. */
        int removedCount() { return removed; }

        boolean consistent() { return removed == frontier - 1 - addedBack.size(); }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        InfiniteSet s = new InfiniteSet();
        int[] p = {s.popSmallest(), s.popSmallest(), s.popSmallest()};
        if (!Arrays.equals(p, new int[] {1, 2, 3})) throw new AssertionError("pops");
        s.addBack(2); s.addBack(2); s.addBack(7);
        if (s.popSmallest() != 2 || s.popSmallest() != 4 || s.removedCount() != 4) throw new AssertionError("example 1");
        // Example 2: restoring the only popped value empties the removed count.
        InfiniteSet u = new InfiniteSet();
        if (u.popSmallest() != 1) throw new AssertionError("e2 pop");
        u.addBack(1);
        if (u.removedCount() != 0 || u.popSmallest() != 1 || u.removedCount() != 1) throw new AssertionError("example 2");
        // Random comparison with a boolean-array oracle over values 1..60.
        Random rnd = new Random(3693L);
        for (int t = 0; t < 3000; t++) {
            InfiniteSet set = new InfiniteSet();
            boolean[] gone = new boolean[100];
            for (int step = 0; step < 50; step++) {
                if (rnd.nextInt(3) > 0) {
                    // Oracle: scan for the smallest value not removed.
                    int want = 1;
                    while (gone[want]) want++;
                    if (set.popSmallest() != want) throw new AssertionError("pop");
                    gone[want] = true;
                } else {
                    int n = 1 + rnd.nextInt(60);
                    set.addBack(n);
                    gone[n] = false;
                }
                // The oracle count of removed values must equal the stored count.
                int c = 0;
                for (boolean g : gone) if (g) c++;
                if (set.removedCount() != c || !set.consistent()) throw new AssertionError("count");
            }
        }
    }
}
```

#### Solution: [Boundary] Design Phone Directory (LeetCode 379)
<!-- id: mco-phone-directory-free-list -->

**Approach.**
One array `next` stores two things. For a free number `n`, `next[n]` is the following free number, or `END` for the last one, and a field `head` names the first free number. For an allocated number, `next[n]` holds the reserved value `USED`. A number is therefore in exactly one place: in the free chain, or marked used. Both `get` and `release` work at the head, so each is a constant number of array writes.

Release is idempotent because the test `next[n] == USED` is both the permission to free and the record of the change. A number out of range or already free fails the test and returns false without touching the list. The invariant is that following `head` visits every free number once and ends at `END`, and the used count plus the chain length equals `maxNumbers`. The main method walks the chain after every call.

**Complexity.**
- **Time** is O(1) per call, because each call reads and writes a constant number of array cells.
- **Space** is O(n) for the single `int[]` of length `maxNumbers`, and no other collection exists.

```java run
import java.util.*;

public final class PhoneDirectoryFreeList {
    static final class PhoneDirectory {
        private static final int END = -1, USED = -2;
        private final int[] next;
        private int head = 0;

        PhoneDirectory(int maxNumbers) {
            // Every number starts free, linked to the next larger number.
            next = new int[maxNumbers];
            for (int i = 0; i < maxNumbers; i++) next[i] = i + 1 < maxNumbers ? i + 1 : END;
        }

        /** Hands out a free number. Time: O(1). Space: O(1). Invariant: the chain from head holds exactly the free numbers. */
        int get() {
            // An empty chain means every number is used.
            if (head == END) return -1;
            int n = head;
            // Unlink the head and mark the number as used.
            head = next[n];
            next[n] = USED;
            return n;
        }

        /** Tells whether a number is free. Time: O(1). Space: O(1). Invariant: free means not marked USED. */
        boolean check(int n) { return n >= 0 && n < next.length && next[n] != USED; }

        /** Frees a used number and reports whether it changed. Time: O(1). Space: O(1). Invariant: a false result changes nothing. */
        boolean release(int n) {
            // Out of range or already free means there is nothing to undo.
            if (n < 0 || n >= next.length || next[n] != USED) return false;
            // Push the number onto the front of the chain.
            next[n] = head;
            head = n;
            return true;
        }

        /** Counts the chain length, failing on a cycle. Time: O(n). Space: O(1). Invariant: chain visits each free number once. */
        int freeCount() {
            int c = 0;
            for (int v = head; v != END; v = next[v]) {
                if (next[v] == USED || ++c > next.length) throw new AssertionError("broken chain");
            }
            return c;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        PhoneDirectory d = new PhoneDirectory(3);
        if (d.get() != 0 || d.get() != 1) throw new AssertionError("gets");
        if (!d.release(0) || d.release(0)) throw new AssertionError("release");
        if (d.get() != 0 || d.get() != 2 || d.get() != -1) throw new AssertionError("example 1");
        // Example 2: a number that was never taken is already free.
        PhoneDirectory e = new PhoneDirectory(2);
        if (e.release(1) || !e.check(1) || e.release(5)) throw new AssertionError("example 2 a");
        if (e.get() != 0 || e.check(0)) throw new AssertionError("example 2 b");
        // Random comparison with a boolean-array oracle; get may return any free number.
        Random rnd = new Random(3694L);
        for (int t = 0; t < 4000; t++) {
            int max = 1 + rnd.nextInt(6);
            PhoneDirectory dir = new PhoneDirectory(max);
            boolean[] used = new boolean[max];
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) {
                    int free = 0;
                    for (boolean b : used) if (!b) free++;
                    int got = dir.get();
                    // -1 exactly when nothing is free, otherwise a number that the oracle holds free.
                    if ((got == -1) != (free == 0)) throw new AssertionError("get -1");
                    if (got != -1) { if (used[got]) throw new AssertionError("duplicate " + got); used[got] = true; }
                } else if (op == 1) {
                    int n = rnd.nextInt(max + 4) - 2;
                    boolean want = n >= 0 && n < max && used[n];
                    if (dir.release(n) != want) throw new AssertionError("release " + n);
                    if (want) used[n] = false;
                } else {
                    int n = rnd.nextInt(max + 4) - 2;
                    boolean want = n >= 0 && n < max && !used[n];
                    if (dir.check(n) != want) throw new AssertionError("check " + n);
                }
                // The chain length must equal the oracle's free count.
                int free = 0;
                for (boolean b : used) if (!b) free++;
                if (dir.freeCount() != free) throw new AssertionError("chain length");
            }
        }
    }
}
```

#### Solution: [Recognize] Dinner Plate Stacks (LeetCode 1172)
<!-- id: mco-dinner-plates-writable -->

**Approach.**
The class keeps an `ArrayList` of stacks and a `TreeSet<Integer>` named `writable` of stack indexes. The policy for stale entries is lazy. The set may contain an index whose stack is full or whose index is at or above the list size, but it must contain every index of a non-full stack. Push reads the smallest index, discards it when the stack is full or missing, and repeats. When the set runs out, it opens a new stack at the end of the list. Pop removes empty stacks from the end of the list before it reads the last stack, and both pop methods add the touched index to the set, where a second add changes nothing.

Each push or pop adds at most one entry, and each cleanup removes one, so cleanup is paid for by earlier additions. The invariant is that every non-full stack below the list size appears in `writable`, which the main method checks after each call.

**Complexity.**
- **Time** is amortized O(log n) per call for n stacks, because cleanup removes only entries that earlier calls added.
- **Space** is O(n + v) for n stacks and v stored values, plus at most one set entry per call.

```java run
import java.util.*;

public final class DinnerPlatesWritable {
    static final class DinnerPlates {
        private final int cap;
        private final List<ArrayDeque<Integer>> stacks = new ArrayList<>();
        private final TreeSet<Integer> writable = new TreeSet<>();

        DinnerPlates(int capacity) { cap = capacity; }

        /** Places val on the leftmost non-full stack. Time: amortized O(log n). Space: O(1). Invariant: writable covers every non-full stack. */
        void push(int val) {
            int idx = -1;
            // Inspect the smallest entry; discard it when it is stale.
            while (!writable.isEmpty()) {
                int c = writable.first();
                if (c < stacks.size() && stacks.get(c).size() < cap) { idx = c; break; }
                writable.pollFirst();
            }
            // No valid entry means every stack is full, so open a new one.
            if (idx < 0) { idx = stacks.size(); stacks.add(new ArrayDeque<>()); writable.add(idx); }
            stacks.get(idx).push(val);
        }

        /** Pops from the rightmost non-empty stack. Time: amortized O(log n). Space: O(1). Invariant: the last stack is non-empty afterwards. */
        int pop() {
            // Trailing empty stacks are dropped; their set entries become stale and are cleaned by push.
            while (!stacks.isEmpty() && stacks.get(stacks.size() - 1).isEmpty()) stacks.remove(stacks.size() - 1);
            if (stacks.isEmpty()) return -1;
            return popAtStack(stacks.size() - 1);
        }

        /** Pops from a named stack. Time: O(log n). Space: O(1). Invariant: a touched stack is in writable. */
        int popAtStack(int index) {
            // A missing or empty stack gives -1 and changes nothing.
            if (index < 0 || index >= stacks.size() || stacks.get(index).isEmpty()) return -1;
            // The stack now has room, so it must be listed; add is idempotent.
            writable.add(index);
            return stacks.get(index).pop();
        }

        boolean covers() {
            for (int i = 0; i < stacks.size(); i++) if (stacks.get(i).size() < cap && !writable.contains(i)) return false;
            return true;
        }
    }

    /** Brute force: scans stacks from the left for push and from the right for pop. */
    static final class Oracle {
        final int cap; final List<ArrayDeque<Integer>> st = new ArrayList<>();
        Oracle(int cap) { this.cap = cap; }
        void push(int v) {
            for (ArrayDeque<Integer> s : st) if (s.size() < cap) { s.push(v); return; }
            ArrayDeque<Integer> s = new ArrayDeque<>(); s.push(v); st.add(s);
        }
        int pop() {
            for (int i = st.size() - 1; i >= 0; i--) if (!st.get(i).isEmpty()) return st.get(i).pop();
            return -1;
        }
        int popAt(int i) { return i < st.size() && !st.get(i).isEmpty() ? st.get(i).pop() : -1; }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        DinnerPlates d = new DinnerPlates(2);
        for (int v = 1; v <= 5; v++) d.push(v);
        if (d.popAtStack(0) != 2) throw new AssertionError("popAt");
        d.push(6);
        if (d.pop() != 5 || d.pop() != 4) throw new AssertionError("example 1");
        // Example 2 from the exercise.
        DinnerPlates e = new DinnerPlates(1);
        e.push(7); e.push(8);
        if (e.popAtStack(0) != 7 || e.popAtStack(0) != -1) throw new AssertionError("example 2 a");
        e.push(9);
        if (e.pop() != 8) throw new AssertionError("example 2 b");
        // Random comparison with the brute force.
        Random rnd = new Random(3695L);
        for (int t = 0; t < 4000; t++) {
            int cap = 1 + rnd.nextInt(3);
            DinnerPlates x = new DinnerPlates(cap);
            Oracle o = new Oracle(cap);
            for (int step = 0; step < 60; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) { int v = rnd.nextInt(100); x.push(v); o.push(v); }
                else if (op == 1) { if (x.pop() != o.pop()) throw new AssertionError("pop"); }
                else { int i = rnd.nextInt(6); if (x.popAtStack(i) != o.popAt(i)) throw new AssertionError("popAt " + i); }
                if (!x.covers()) throw new AssertionError("writable lost a non-full stack");
            }
        }
    }
}
```
