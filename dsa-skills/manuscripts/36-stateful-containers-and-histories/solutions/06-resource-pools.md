<!-- solutions-for: 06-resource-pools -->
### Solutions For Resource Pools

#### Solution: [Build] Reusable ID Pool (Author exercise)
<!-- id: sc-pool-id-pool -->

**Approach.**
The pool keeps one boolean per identifier, so every identifier has exactly one state. A second field `low` records a scan start: every index below it holds a false flag. Allocation reads flags from `low` upward, takes the first true flag, clears it and moves `low` past it. When the scan reaches the end, it sets `low` to `n` and returns -1, so the next failed call starts at the end and reads nothing.

Release first checks the range and then the flag. A number outside the pool or already free returns false before any write, which makes the call idempotent. A valid release sets the flag and lowers `low` to the released number when that number is smaller, which restores the invariant that no true flag sits below `low`.

**Complexity.**
- **Time** is O(n) per allocate in the worst case, because a scan may cross many in-use entries, and O(1) per release, because it touches one entry.
- **Space** is O(n), because the array holds one flag per identifier and the other fields are single ints.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class ReusableIdPool {
    private final boolean[] free;
    private int low;

    /**
     * Creates a pool of identifiers 0 to n - 1, all free.
     * Time: O(n), because every flag is written once.
     * Space: O(n), because one flag exists per identifier.
     * Invariant: no flag below low is true.
     */
    ReusableIdPool(int n) {
        // One flag per identifier; the allocation of the array costs O(n) space.
        free = new boolean[n];
        // Every identifier starts free, written in one pass of n steps.
        java.util.Arrays.fill(free, true);
        // The scan start is 0 because index 0 may be free.
        low = 0;
    }

    /**
     * Returns the smallest free identifier and marks it in use, or -1 when none is free.
     * Time: O(n) worst case, because the scan can cross every in-use entry.
     * Space: O(1), because only an index is stored.
     * Invariant: after the call, no flag below low is true.
     */
    int allocate() {
        // The loop starts at low, so entries known to be in use are never read again.
        for (int id = low; id < free.length; id++) {
            // The first true flag is the smallest free identifier, because smaller entries are false.
            if (free[id]) {
                // Mark the identifier in use so that a later call cannot return it.
                free[id] = false;
                // Everything up to id is now in use, so the next scan begins just after it.
                low = id + 1;
                // The caller receives the identifier exactly once.
                return id;
            }
        }
        // The scan found nothing; moving low to n makes the next failure cost nothing.
        low = free.length;
        // The pool is exhausted and no field except low changed.
        return -1;
    }

    /**
     * Returns true and frees id when id is in use; returns false and changes nothing otherwise.
     * Time: O(1), because one entry is read and at most one is written.
     * Space: O(1), because no structure grows.
     * Invariant: a repeated call with the same id returns false the second time.
     */
    boolean release(int id) {
        // The range test runs first, so the array is never read at an invalid index; a free flag means a duplicate.
        if (id < 0 || id >= free.length || free[id]) return false;
        // The identifier becomes available again.
        free[id] = true;
        // A free entry now exists at id, so the scan start cannot stay above it.
        low = Math.min(low, id);
        // The caller learns that the release took effect.
        return true;
    }

    /**
     * Oracle with a set of identifiers in use and a full scan from 0.
     * Time: O(n) per allocate, because the scan always starts at 0.
     * Space: O(n), because the set can hold every identifier.
     * Invariant: an identifier is free exactly when the set does not contain it.
     */
    static final class Oracle {
        private final int n;
        private final Set<Integer> used = new HashSet<>();
        Oracle(int n) { this.n = n; }
        int allocate() {
            // Try every identifier in increasing order; the first one not in use is the smallest free.
            for (int id = 0; id < n; id++) if (used.add(id)) return id;
            return -1;
        }
        boolean release(int id) {
            // Removing from the set reports whether the identifier was in use; an invalid id was never added.
            return used.remove(id);
        }
    }

    public static void main(String[] args) {
        // The first worked example: reuse of 0 after release, then exhaustion.
        ReusableIdPool a = new ReusableIdPool(3);
        if (a.allocate() != 0 || a.allocate() != 1 || !a.release(0) || a.allocate() != 0 || a.allocate() != 2 || a.allocate() != -1)
            throw new AssertionError("example 1");
        // The second worked example: release before allocation, duplicate release and out-of-range release.
        ReusableIdPool b = new ReusableIdPool(2);
        if (b.release(1) || b.allocate() != 0 || !b.release(0) || b.release(0) || b.release(5) || b.release(-1) || b.allocate() != 0)
            throw new AssertionError("example 2");
        // Release order does not matter: the smallest free identifier always comes first.
        ReusableIdPool c = new ReusableIdPool(4);
        for (int i = 0; i < 4; i++) c.allocate();
        c.release(3);
        c.release(1);
        if (c.allocate() != 1 || c.allocate() != 3 || c.allocate() != -1) throw new AssertionError("order");
        // A failed allocation leaves the pool usable.
        c.release(2);
        if (c.allocate() != 2) throw new AssertionError("after exhaustion");
        // Random operation sequences compared with the oracle, including invalid and duplicate releases.
        Random rnd = new Random(3601L);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            ReusableIdPool p = new ReusableIdPool(n);
            Oracle o = new Oracle(n);
            for (int step = 0; step < 40; step++) {
                // Half of the calls allocate and half release a number that may be invalid.
                if (rnd.nextBoolean()) {
                    if (p.allocate() != o.allocate()) throw new AssertionError("allocate mismatch");
                } else {
                    int id = rnd.nextInt(n + 4) - 2;
                    if (p.release(id) != o.release(id)) throw new AssertionError("release mismatch");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Smallest Number in Infinite Set (LeetCode 2336)
<!-- id: sc-pool-infinite-set -->

**Approach.**
Every integer at or above the integer `frontier` was never removed, so the set stores nothing for them. Every integer below `frontier` is either still removed or has been added back, and a `TreeSet` named `returned` holds exactly the added-back ones. The method `popSmallest` takes the smallest element of `returned` when that set is not empty, because every value in it is smaller than `frontier`. Otherwise it returns `frontier` and increments it.

The method `addBack` inserts `num` only when `num < frontier`, because a larger value is already in the set implicitly. The `TreeSet` ignores a second insertion of the same value, so a duplicate addBack changes nothing. The invariant is that the set equals the union of `returned` and all integers from `frontier` upward, with `returned` holding only values below `frontier`.

**Complexity.**
- **Time** is O(log k) per call, where k is the size of `returned`, because the tree set orders its entries.
- **Space** is O(k), because only the added-back values below the frontier are stored.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class InfiniteSetFrontier {
    private int frontier = 1;
    private final TreeSet<Integer> returned = new TreeSet<>();

    /**
     * Removes and returns the smallest integer in the set.
     * Time: O(log k), because pollFirst on a tree set is logarithmic.
     * Space: O(1) extra, because at most one element leaves or the frontier moves by one.
     * Invariant: every element of returned is below frontier.
     */
    int popSmallest() {
        // A returned value is always smaller than the frontier, so it wins when one exists.
        if (!returned.isEmpty()) return returned.pollFirst();
        // Otherwise the frontier is the smallest present integer; the post-increment advances it past the removed one.
        return frontier++;
    }

    /**
     * Inserts num into the set when it is absent.
     * Time: O(log k), because a tree set insertion is logarithmic.
     * Space: O(1) extra, because at most one element is added.
     * Invariant: returned never holds a value at or above frontier, and never holds a value twice.
     */
    void addBack(int num) {
        // A value at or above the frontier is still in the set, so nothing needs storing.
        if (num < frontier) returned.add(num);
    }

    /** Oracle: a flag array that marks removed integers and scans from 1. Time: O(limit) per pop. Space: O(limit). */
    static final class Oracle {
        private final boolean[] removed = new boolean[5000];
        int popSmallest() {
            // The first integer not removed is the smallest present one.
            int x = 1;
            while (removed[x]) x++;
            removed[x] = true;
            return x;
        }
        void addBack(int num) { removed[num] = false; }
    }

    public static void main(String[] args) {
        // First worked example: pop three, add back 1, pop twice.
        InfiniteSetFrontier s = new InfiniteSetFrontier();
        if (s.popSmallest() != 1 || s.popSmallest() != 2 || s.popSmallest() != 3) throw new AssertionError("pops");
        s.addBack(1);
        if (s.popSmallest() != 1 || s.popSmallest() != 4) throw new AssertionError("after addBack");
        // Second worked example: addBack above the frontier does nothing, and a duplicate addBack stores one copy.
        InfiniteSetFrontier u = new InfiniteSetFrontier();
        u.addBack(7);
        if (u.popSmallest() != 1 || u.popSmallest() != 2) throw new AssertionError("ignored addBack");
        u.addBack(2);
        u.addBack(2);
        if (u.popSmallest() != 2 || u.popSmallest() != 3) throw new AssertionError("duplicate addBack");
        // Random sequences within the statement limits, compared with the oracle.
        Random rnd = new Random(3602L);
        for (int t = 0; t < 3000; t++) {
            InfiniteSetFrontier f = new InfiniteSetFrontier();
            Oracle o = new Oracle();
            for (int step = 0; step < 60; step++) {
                if (rnd.nextInt(3) > 0) {
                    if (f.popSmallest() != o.popSmallest()) throw new AssertionError("pop mismatch");
                } else {
                    int num = 1 + rnd.nextInt(12);
                    f.addBack(num);
                    o.addBack(num);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Design Phone Directory (LeetCode 379)
<!-- id: sc-pool-phone-directory -->

**Approach.**
The directory keeps two structures that must agree. A queue `waiting` holds the available numbers in the order in which they became available, and a boolean array `assigned` holds the state of each number. The method `get` polls the queue, marks the number assigned and returns it, or returns -1 on an empty queue. The method `check` reads the flag only.

The method `release` reads the flag first. When the number is not assigned, the call returns without touching the queue, because appending it again would put one number in the queue twice and a later pair of get calls would return it twice. When the number is assigned, the flag is cleared and the number joins the end of the queue. The invariant is that a number is in `waiting` exactly once when its flag is false, and not at all when its flag is true.

**Complexity.**
- **Time** is O(1) per call, because the queue and the array both support constant-time operations at the points used.
- **Space** is O(maxNumbers), because the queue and the array each hold at most one entry per number.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class PhoneDirectoryQueue {
    private final ArrayDeque<Integer> waiting = new ArrayDeque<>();
    private final boolean[] assigned;

    /**
     * Creates a directory in which every number is available, oldest first.
     * Time: O(maxNumbers), because every number is queued once.
     * Space: O(maxNumbers), because the queue and the array hold one entry per number.
     * Invariant: waiting holds the numbers whose assigned flag is false, each exactly once.
     */
    PhoneDirectoryQueue(int maxNumbers) {
        // One flag per number, all false at the start.
        assigned = new boolean[maxNumbers];
        // Queue the numbers in increasing order so that 0 has been available longest.
        for (int i = 0; i < maxNumbers; i++) waiting.add(i);
    }

    /**
     * Assigns and returns the number that has been available longest, or -1.
     * Time: O(1), because polling the head of an ArrayDeque is constant.
     * Space: O(1), because nothing grows.
     * Invariant: the returned number leaves the queue and its flag becomes true in the same call.
     */
    int get() {
        // An empty queue means the directory is exhausted.
        if (waiting.isEmpty()) return -1;
        // The head is the longest-waiting available number.
        int number = waiting.poll();
        // The flag and the queue change together, so the two structures agree.
        assigned[number] = true;
        return number;
    }

    /** Returns true when number is available. Time: O(1). Space: O(1). Invariant: reads the flag only. */
    boolean check(int number) {
        // Available means not assigned.
        return !assigned[number];
    }

    /**
     * Makes number available again unless it already is.
     * Time: O(1), because one flag is read and the queue gains at most one entry.
     * Space: O(1), because at most one entry is added.
     * Invariant: a number is queued only when its flag changes from true to false.
     */
    void release(int number) {
        // A number that is not assigned is already queued, so a second append would duplicate it.
        if (!assigned[number]) return;
        // The flag changes first so a repeated call finds it false.
        assigned[number] = false;
        // The number joins the end of the waiting order.
        waiting.add(number);
    }

    /**
     * Oracle with a plain list that searches for duplicates before adding.
     * Time: O(maxNumbers) per call, because contains scans the list.
     * Space: O(maxNumbers), because the list holds each available number once.
     * Invariant: the list order is the order in which numbers became available.
     */
    static final class Oracle {
        private final List<Integer> order = new ArrayList<>();
        private final int max;
        Oracle(int max) {
            this.max = max;
            for (int i = 0; i < max; i++) order.add(i);
        }
        int get() { return order.isEmpty() ? -1 : order.remove(0); }
        boolean check(int number) { return order.contains(number); }
        void release(int number) {
            // Append only when the number is absent from the available list.
            if (number >= 0 && number < max && !order.contains(number)) order.add(number);
        }
    }

    public static void main(String[] args) {
        // First worked example, including a repeated release that must be ignored.
        PhoneDirectoryQueue d = new PhoneDirectoryQueue(3);
        if (d.get() != 0 || d.get() != 1 || d.check(0)) throw new AssertionError("start");
        d.release(0);
        if (!d.check(0)) throw new AssertionError("check after release");
        d.release(0);
        if (d.get() != 2 || d.get() != 0 || d.get() != -1) throw new AssertionError("order after release");
        // Second worked example: releasing a number that was never assigned changes nothing.
        PhoneDirectoryQueue e = new PhoneDirectoryQueue(2);
        if (e.get() != 0) throw new AssertionError("e0");
        e.release(1);
        if (e.get() != 1) throw new AssertionError("e1");
        e.release(1);
        e.release(0);
        if (e.get() != 1 || e.get() != 0) throw new AssertionError("fifo");
        // Random sequences with many duplicate releases, compared with the oracle.
        Random rnd = new Random(3603L);
        for (int t = 0; t < 4000; t++) {
            int max = 1 + rnd.nextInt(6);
            PhoneDirectoryQueue p = new PhoneDirectoryQueue(max);
            Oracle o = new Oracle(max);
            for (int step = 0; step < 40; step++) {
                int kind = rnd.nextInt(3), number = rnd.nextInt(max);
                if (kind == 0) {
                    if (p.get() != o.get()) throw new AssertionError("get mismatch");
                } else if (kind == 1) {
                    if (p.check(number) != o.check(number)) throw new AssertionError("check mismatch");
                } else {
                    p.release(number);
                    o.release(number);
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Design Memory Allocator (LeetCode 2502)
<!-- id: sc-pool-memory-allocator -->

**Approach.**
This is a transfer problem. Each unit stores the owner id, with 0 meaning free, because ids start at 1. Allocation scans left to right and counts the current run of free units. When the count reaches `size`, the run ends at the current index, so the start is the index minus `size - 1`, and the method writes the owner into that run. Because the scan runs left to right, the first completed run has the lowest start. Freeing reads every unit once, clears those that match the owner and counts them. A single flag per unit would not work, because the free call must find all blocks of one owner.

The invariant is that every unit has exactly one value, which is free or one owner, and a run found by allocation is entirely free before the write.

**Complexity.**
- **Time** is O(n) per call, because each call scans the array once and writes at most `size` units.
- **Space** is O(n), because the owner array has one int per unit.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.TreeSet;

public final class MemoryAllocatorRuns {
    private final int[] owner;

    /** Creates n free units. Time: O(n). Space: O(n). Invariant: owner[i] is 0 for a free unit. */
    MemoryAllocatorRuns(int n) { owner = new int[n]; }

    /**
     * Allocates the lowest run of size free units to mID, or returns -1.
     * Time: O(n), because one left-to-right scan counts runs.
     * Space: O(1), because only counters are stored.
     * Invariant: run counts consecutive free units ending at the current index.
     */
    int allocate(int size, int mID) {
        // run counts consecutive free units ending at i; it resets at every owned unit.
        int run = 0;
        for (int i = 0; i < owner.length; i++) {
            // A free unit extends the run; an owned unit breaks it.
            run = owner[i] == 0 ? run + 1 : 0;
            // The first index where the run reaches size gives the lowest start.
            if (run == size) {
                int start = i - size + 1;
                // Write the owner into the whole run; this is the only write path.
                for (int j = start; j <= i; j++) owner[j] = mID;
                return start;
            }
        }
        // No run was long enough, including a size larger than n.
        return -1;
    }

    /**
     * Frees every unit owned by mID and returns how many were freed.
     * Time: O(n), because every unit is read once.
     * Space: O(1), because only a counter is stored.
     * Invariant: no unit holds mID after the call.
     */
    int freeMemory(int mID) {
        int freed = 0;
        for (int i = 0; i < owner.length; i++) {
            // Clear only the units owned by mID and count them.
            if (owner[i] == mID) { owner[i] = 0; freed++; }
        }
        return freed;
    }

    /** Oracle: a set of units in use per owner, with a start-by-start test. Time: O(n * size) per allocate. Space: O(n). */
    static final class Oracle {
        private final int n;
        private final Map<Integer, TreeSet<Integer>> units = new HashMap<>();
        Oracle(int n) { this.n = n; }
        private boolean used(int u) {
            for (TreeSet<Integer> s : units.values()) if (s.contains(u)) return true;
            return false;
        }
        int allocate(int size, int mID) {
            for (int s = 0; s + size <= n; s++) {
                boolean ok = true;
                // Every unit of the candidate run must be unowned.
                for (int j = s; j < s + size && ok; j++) ok = !used(j);
                if (ok) {
                    TreeSet<Integer> set = units.computeIfAbsent(mID, k -> new TreeSet<>());
                    for (int j = s; j < s + size; j++) set.add(j);
                    return s;
                }
            }
            return -1;
        }
        int freeMemory(int mID) {
            TreeSet<Integer> set = units.remove(mID);
            return set == null ? 0 : set.size();
        }
    }

    public static void main(String[] args) {
        // First worked example: freed units are reused and a request larger than any run fails.
        MemoryAllocatorRuns a = new MemoryAllocatorRuns(10);
        int[] got = {a.allocate(1, 1), a.allocate(1, 2), a.allocate(1, 3), a.freeMemory(2), a.allocate(3, 4),
            a.allocate(1, 1), a.allocate(1, 1), a.freeMemory(1), a.allocate(4, 2), a.allocate(8, 5)};
        int[] want = {0, 1, 2, 1, 3, 1, 6, 3, 6, -1};
        if (!java.util.Arrays.equals(got, want)) throw new AssertionError("example 1");
        // Second worked example: an owner without units frees nothing.
        MemoryAllocatorRuns b = new MemoryAllocatorRuns(6);
        int[] got2 = {b.allocate(2, 7), b.allocate(2, 7), b.allocate(2, 8), b.freeMemory(7), b.allocate(3, 9),
            b.freeMemory(7), b.allocate(3, 9)};
        if (!java.util.Arrays.equals(got2, new int[] {0, 2, 4, 4, 0, 0, -1})) throw new AssertionError("example 2");
        // Random sequences compared with the oracle.
        Random rnd = new Random(3604L);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            MemoryAllocatorRuns p = new MemoryAllocatorRuns(n);
            Oracle o = new Oracle(n);
            for (int step = 0; step < 30; step++) {
                int id = 1 + rnd.nextInt(4);
                if (rnd.nextBoolean()) {
                    int size = 1 + rnd.nextInt(n + 1);
                    if (p.allocate(size, id) != o.allocate(size, id)) throw new AssertionError("allocate mismatch");
                } else if (p.freeMemory(id) != o.freeMemory(id)) throw new AssertionError("free mismatch");
            }
        }
    }
}
```
