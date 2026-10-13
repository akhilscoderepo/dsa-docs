<!-- solutions-for: 03-circular-buffers -->
### Solutions For Circular Buffers

#### Solution: [Build] Ring Buffer (Author exercise)
<!-- id: sc-ring-buffer -->

**Approach.**
The buffer owns one array and two ints, `head` and `size`. The oldest value sits at `slots[head]`, and the next write position is `(head + size) % capacity`, computed when needed and never stored. An add on a full buffer returns `false` before it touches any field, which keeps a rejected call from changing state. A removal reads `slots[head]`, advances `head` by one with wraparound and lowers `size`. A private helper `at(i)` owns the modular formula, so no other method repeats it.

The invariant is that the live values occupy `at(0)` through `at(size - 1)`, and these positions differ because `size <= capacity`. Equal indices are never used to detect fullness, so a full buffer and an empty buffer are told apart by `size` alone.

**Complexity.**
- **Time** is O(1) per call, because each method reads or writes one slot and updates at most two ints.
- **Space** is O(capacity) for the array, with O(1) extra fields.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class RingBufferBuild {
    /** Fixed-capacity FIFO of ints. Time: O(1) per call. Space: O(capacity). Invariant: live values are at(0)..at(size - 1). */
    static final class RingBuffer {
        // Storage allocated once; its length never changes.
        private final int[] slots;
        // Array index of the oldest value, always in [0, capacity).
        private int head;
        // Number of live values, always in [0, capacity].
        private int count;

        RingBuffer(int capacity) { slots = new int[capacity]; }

        // The only place that applies wraparound: the array index of the i-th oldest live value.
        private int at(int i) { return (head + i) % slots.length; }

        /** Appends v, or returns false and changes nothing when full. Time: O(1). Space: O(1). */
        boolean offer(int v) {
            // A full buffer rejects before any field changes.
            if (count == slots.length) return false;
            // The write position is the index just after the newest value.
            slots[at(count)] = v;
            // The new value becomes live.
            count++;
            return true;
        }

        /** Removes and returns the oldest value, or -1 when empty. Time: O(1). Space: O(1). */
        int poll() {
            // An empty buffer has no oldest value.
            if (count == 0) return -1;
            // Read the oldest value before the index moves.
            int v = slots[head];
            // Advance head with wraparound; no value is copied.
            head = (head + 1) % slots.length;
            // One fewer live value.
            count--;
            return v;
        }

        /** Returns the oldest value without removing it, or -1 when empty. Time: O(1). Space: O(1). */
        int peek() { return count == 0 ? -1 : slots[head]; }

        /** Returns the number of live values. Time: O(1). Space: O(1). */
        int size() { return count; }
    }

    /** Oracle: a bounded FIFO on java.util.ArrayDeque. Time: O(1) per call. Space: O(capacity). Invariant: the deque holds the live values in order. */
    static final class Oracle {
        private final ArrayDeque<Integer> d = new ArrayDeque<>();
        private final int cap;
        Oracle(int cap) { this.cap = cap; }
        boolean offer(int v) { if (d.size() == cap) return false; d.addLast(v); return true; }
        int poll() { return d.isEmpty() ? -1 : d.pollFirst(); }
        int peek() { return d.isEmpty() ? -1 : d.peekFirst(); }
        int size() { return d.size(); }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise: capacity 2 with a wrapped write.
        RingBuffer r = new RingBuffer(2);
        boolean[] adds = {r.offer(5), r.offer(6), r.offer(7)};
        if (!adds[0] || !adds[1] || adds[2]) throw new AssertionError("e1 adds");
        if (r.poll() != 5 || !r.offer(7) || r.poll() != 6 || r.poll() != 7 || r.poll() != -1) throw new AssertionError("e1 rest");
        // Example 2: capacity 3, then peek and size after two removals and two adds.
        r = new RingBuffer(3);
        r.offer(1); r.offer(2); r.offer(3);
        if (r.poll() != 1 || r.poll() != 2 || !r.offer(4) || !r.offer(5) || r.peek() != 3 || r.size() != 3) throw new AssertionError("e2");
        // Capacity one: every index stays 0, and the buffer alternates between full and empty.
        r = new RingBuffer(1);
        if (!r.offer(9) || r.offer(8) || r.poll() != 9 || r.poll() != -1 || !r.offer(8) || r.peek() != 8) throw new AssertionError("cap 1");
        // The claim in the lesson: an int remainder with divisor 0 throws, so capacity 0 is outside the contract.
        int zero = args.length;
        try { int ignored = 5 % zero; throw new AssertionError("no exception " + ignored); } catch (ArithmeticException expected) { }
        // The claim in the lesson: ArrayDeque has no capacity limit and accepts every add.
        ArrayDeque<Integer> unbounded = new ArrayDeque<>();
        for (int i = 0; i < 10_000; i++) if (!unbounded.offerLast(i)) throw new AssertionError("ArrayDeque rejected");
        // Random operation sequences compared with the oracle, including long runs that wrap many times.
        Random rnd = new Random(3601L);
        for (int t = 0; t < 2000; t++) {
            int cap = 1 + rnd.nextInt(6);
            RingBuffer a = new RingBuffer(cap);
            Oracle b = new Oracle(cap);
            for (int op = 0; op < 60; op++) {
                int k = rnd.nextInt(4), v = rnd.nextInt(1000);
                boolean ok = switch (k) {
                    case 0, 1 -> a.offer(v) == b.offer(v);
                    case 2 -> a.poll() == b.poll();
                    default -> a.peek() == b.peek();
                };
                if (!ok || a.size() != b.size()) throw new AssertionError("mismatch cap=" + cap + " op=" + op);
            }
        }
    }
}
```

#### Solution: [Vary] Design Circular Queue (LeetCode 622)
<!-- id: sc-circular-queue -->

**Approach.**
The queue keeps `data`, `head` and `size`, and every query follows from them. `Front` reads `data[head]`. `Rear` reads the position `(head + size - 1) % k`, which exists only when the queue is non-empty, so the method checks `size` first and returns -1 otherwise. The methods `isEmpty` and `isFull` compare `size` with 0 and with `k`, and no method compares two indices. That choice removes the case in which equal head and tail mean either state.

Mutation order matters in `deQueue`. The method reads nothing it needs after `head` moves, so it advances `head` and lowers `size` together, and a rejected call returns before either update. The invariant is the lesson's: the live values sit at `(head + i) % k` for `i < size`.

**Complexity.**
- **Time** is O(1) per call, because each method uses constant arithmetic on three fields.
- **Space** is O(k) for the array and O(1) for the fields.

```java run
import java.util.LinkedList;
import java.util.Random;

public final class CircularQueue622 {
    /** Bounded queue answering six queries. Time: O(1) per call. Space: O(k). Invariant: live values sit at (head + i) % k for i < size. */
    static final class MyCircularQueue {
        private final int[] data;
        private int head;
        private int size;

        MyCircularQueue(int k) { data = new int[k]; }

        boolean enQueue(int value) {
            // Full queues reject without touching any field.
            if (isFull()) return false;
            // The slot after the newest value is free because size < k.
            data[(head + size) % data.length] = value;
            // The value is now live.
            size++;
            return true;
        }

        boolean deQueue() {
            // An empty queue has nothing to remove.
            if (isEmpty()) return false;
            // Moving head past the front value retires it; the stale number stays in the array but no live index reaches it.
            head = (head + 1) % data.length;
            // The count and the index change together in this one method.
            size--;
            return true;
        }

        // Front value, or -1 when empty.
        int Front() { return isEmpty() ? -1 : data[head]; }

        // Newest value, or -1 when empty; the position is computed from head and size.
        int Rear() { return isEmpty() ? -1 : data[(head + size - 1) % data.length]; }

        // Empty exactly when no value is live.
        boolean isEmpty() { return size == 0; }

        // Full exactly when every slot is live.
        boolean isFull() { return size == data.length; }
    }

    /** Oracle on a linked list with the same contract. Time: O(1) per call. Space: O(k). Invariant: the list holds live values in order. */
    static final class Oracle {
        private final LinkedList<Integer> l = new LinkedList<>();
        private final int k;
        Oracle(int k) { this.k = k; }
        boolean enQueue(int v) { if (l.size() == k) return false; l.addLast(v); return true; }
        boolean deQueue() { if (l.isEmpty()) return false; l.removeFirst(); return true; }
        int Front() { return l.isEmpty() ? -1 : l.getFirst(); }
        int Rear() { return l.isEmpty() ? -1 : l.getLast(); }
        boolean isEmpty() { return l.isEmpty(); }
        boolean isFull() { return l.size() == k; }
    }

    public static void main(String[] args) {
        // Example 1: removal until empty, then the empty reads.
        MyCircularQueue q = new MyCircularQueue(3);
        if (!q.enQueue(7) || !q.enQueue(8) || q.Front() != 7 || q.Rear() != 8) throw new AssertionError("e1 a");
        if (!q.deQueue() || !q.deQueue() || q.deQueue() || q.Front() != -1 || q.Rear() != -1 || !q.isEmpty()) throw new AssertionError("e1 b");
        // Example 2: capacity 2 wraps the second add of 1 into slot 0.
        q = new MyCircularQueue(2);
        if (!q.enQueue(4) || !q.enQueue(9) || q.enQueue(1) || !q.deQueue() || !q.enQueue(1)) throw new AssertionError("e2 a");
        if (q.Front() != 9 || q.Rear() != 1 || !q.isFull()) throw new AssertionError("e2 b");
        // A full and an empty queue are distinguished even though head and the write position coincide in both.
        q = new MyCircularQueue(1);
        if (!q.isEmpty() || q.isFull() || !q.enQueue(3) || q.isEmpty() || !q.isFull()) throw new AssertionError("cap 1");
        // Random sequences compared with the oracle on all six queries.
        Random rnd = new Random(3602L);
        for (int t = 0; t < 2000; t++) {
            int k = 1 + rnd.nextInt(5);
            MyCircularQueue a = new MyCircularQueue(k);
            Oracle b = new Oracle(k);
            for (int op = 0; op < 60; op++) {
                int v = rnd.nextInt(1001);
                boolean ok = switch (rnd.nextInt(6)) {
                    case 0, 1 -> a.enQueue(v) == b.enQueue(v);
                    case 2 -> a.deQueue() == b.deQueue();
                    case 3 -> a.Front() == b.Front() && a.Rear() == b.Rear();
                    case 4 -> a.isEmpty() == b.isEmpty();
                    default -> a.isFull() == b.isFull();
                };
                if (!ok) throw new AssertionError("mismatch k=" + k + " op=" + op);
            }
        }
    }
}
```

#### Solution: [Boundary] Design Circular Deque (LeetCode 641)
<!-- id: sc-circular-deque -->

**Approach.**
The deque uses the same three fields and adds one rule for each end. Insertion at the back writes `(head + size) % k`. Insertion at the front first moves `head` to `(head - 1 + k) % k` and then writes there. Deletion at the front moves `head` forward, and deletion at the back only lowers `size`, because the back position is derived from `head` and `size`. The reads return `data[head]` and `data[(head + size - 1) % k]`.

The term `+ k` is required because Java's remainder keeps the sign of the left operand, so `-1 % 3` is `-1` and would be an invalid index. With capacity one, every modular expression evaluates to 0, so the same code works with no special case: the front insertion moves `head` from 0 to `(0 - 1 + 1) % 1 = 0`. The invariant is the one for the queue, and each method restores it before it returns.

**Complexity.**
- **Time** is O(1) per call, because every method is a fixed number of arithmetic steps.
- **Space** is O(k) for the array, with three ints of extra state.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class CircularDeque641 {
    /** Bounded deque. Time: O(1) per call. Space: O(k). Invariant: live values sit at (head + i) % k for i < size. */
    static final class MyCircularDeque {
        private final int[] data;
        private int head;
        private int size;

        MyCircularDeque(int k) { data = new int[k]; }

        boolean insertFront(int value) {
            // Full deques reject before head moves.
            if (isFull()) return false;
            // Step back one slot; adding the length keeps the left operand non-negative.
            head = (head - 1 + data.length) % data.length;
            // The new front value goes into the slot head now names.
            data[head] = value;
            size++;
            return true;
        }

        boolean insertLast(int value) {
            if (isFull()) return false;
            // The slot after the newest value is free because size < k.
            data[(head + size) % data.length] = value;
            size++;
            return true;
        }

        boolean deleteFront() {
            if (isEmpty()) return false;
            // Retire the front value by moving head forward.
            head = (head + 1) % data.length;
            size--;
            return true;
        }

        boolean deleteLast() {
            if (isEmpty()) return false;
            // The back position is derived from head and size, so lowering size retires it.
            size--;
            return true;
        }

        int getFront() { return isEmpty() ? -1 : data[head]; }

        int getRear() { return isEmpty() ? -1 : data[(head + size - 1) % data.length]; }

        boolean isEmpty() { return size == 0; }

        boolean isFull() { return size == data.length; }
    }

    /** Oracle on java.util.ArrayDeque with an explicit limit. Time: O(1) per call. Space: O(k). Invariant: the deque holds live values in order. */
    static final class Oracle {
        private final ArrayDeque<Integer> d = new ArrayDeque<>();
        private final int k;
        Oracle(int k) { this.k = k; }
        boolean insertFront(int v) { if (d.size() == k) return false; d.addFirst(v); return true; }
        boolean insertLast(int v) { if (d.size() == k) return false; d.addLast(v); return true; }
        boolean deleteFront() { if (d.isEmpty()) return false; d.removeFirst(); return true; }
        boolean deleteLast() { if (d.isEmpty()) return false; d.removeLast(); return true; }
        int getFront() { return d.isEmpty() ? -1 : d.peekFirst(); }
        int getRear() { return d.isEmpty() ? -1 : d.peekLast(); }
        boolean isEmpty() { return d.isEmpty(); }
        boolean isFull() { return d.size() == k; }
    }

    public static void main(String[] args) {
        // The claim in the explanation: Java's remainder keeps the sign of the left operand.
        int minusOne = -1 - args.length;
        if (minusOne % 3 != -1 || (minusOne + 3) % 3 != 2) throw new AssertionError("remainder sign");
        // Example 1: capacity one, every end operation targets slot 0.
        MyCircularDeque d = new MyCircularDeque(1);
        if (!d.insertFront(5) || d.insertLast(6) || d.getFront() != 5 || d.getRear() != 5 || !d.isFull()) throw new AssertionError("e1 a");
        if (!d.deleteLast() || !d.isEmpty() || !d.insertLast(6) || d.getFront() != 6 || !d.deleteFront() || d.deleteFront()) throw new AssertionError("e1 b");
        // Example 2: front insertions wrap head backwards, and a back deletion then back insertion reuses the slot.
        d = new MyCircularDeque(3);
        if (!d.insertLast(1) || !d.insertFront(2) || !d.insertFront(3) || d.insertLast(4)) throw new AssertionError("e2 a");
        if (d.getFront() != 3 || d.getRear() != 1 || !d.deleteLast() || !d.insertLast(9) || d.getRear() != 9 || d.getFront() != 3) throw new AssertionError("e2 b");
        // Random sequences compared with the oracle, with small capacities that include one.
        Random rnd = new Random(3603L);
        for (int t = 0; t < 3000; t++) {
            int k = 1 + rnd.nextInt(4);
            MyCircularDeque a = new MyCircularDeque(k);
            Oracle b = new Oracle(k);
            for (int op = 0; op < 60; op++) {
                int v = rnd.nextInt(1001);
                boolean ok = switch (rnd.nextInt(8)) {
                    case 0 -> a.insertFront(v) == b.insertFront(v);
                    case 1 -> a.insertLast(v) == b.insertLast(v);
                    case 2 -> a.deleteFront() == b.deleteFront();
                    case 3 -> a.deleteLast() == b.deleteLast();
                    case 4 -> a.getFront() == b.getFront();
                    case 5 -> a.getRear() == b.getRear();
                    case 6 -> a.isEmpty() == b.isEmpty();
                    default -> a.isFull() == b.isFull();
                };
                if (!ok) throw new AssertionError("mismatch k=" + k + " op=" + op);
            }
        }
    }
}
```

#### Solution: [Recognize] Implement Router (LeetCode 3508)
<!-- id: sc-implement-router -->

**Approach.**
A ring of `memoryLimit` packets, stored as three parallel int arrays, decides order and eviction. Three indexes mirror it. A hash set of packet identity records answers the duplicate check. A map from destination to a timestamp list answers counts. A start offset in each list marks the entries that are still in the router. Timestamps never decrease across adds, and the oldest packet of one destination is also the oldest in the ring, so each list stays sorted and its evicted entries form a prefix.

One private method `removeOldest` owns every cross-field change. It reads the ring front, removes the key from the set, advances that destination's start offset and moves `head`. Both `forwardPacket` and a full `addPacket` call it, so the three structures cannot disagree. A count is two binary searches inside the live part of the list.

**Complexity.**
- **Time** is O(1) expected for `addPacket` and `forwardPacket`, and O(log n) for `getCount`, where n counts packets ever added to one destination.
- **Space** is O(memoryLimit) for the ring and the set, plus O(total adds) for the lists, which keep retired entries behind the start offset.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class RouterQueries {
    /** Bounded packet router. Invariant: ring, key set and destination lists describe the same packets. */
    static final class Router {
        private static final class Dest { final ArrayList<Integer> times = new ArrayList<>(); int from; }

        private final int[] src, dst, ts;
        private int head, size;
        private final Set<Key> keys = new HashSet<>();
        private final Map<Integer, Dest> byDest = new HashMap<>();

        Router(int memoryLimit) { src = new int[memoryLimit]; dst = new int[memoryLimit]; ts = new int[memoryLimit]; }

        // The identity of a packet; a record supplies equals and hashCode over all three fields.
        private record Key(int source, int destination, int timestamp) { }

        private static Key key(int s, int d, int t) { return new Key(s, d, t); }

        // Removes the oldest packet from the ring, the key set and the destination list together.
        private int[] removeOldest() {
            int[] p = {src[head], dst[head], ts[head]};
            keys.remove(key(p[0], p[1], p[2]));
            byDest.get(p[1]).from++;
            head = (head + 1) % src.length;
            size--;
            return p;
        }

        boolean addPacket(int source, int destination, int timestamp) {
            // A stored identical packet rejects the call before anything changes.
            if (!keys.add(key(source, destination, timestamp))) return false;
            // A full router drops its oldest packet first; the new key is already in the set but differs from it.
            if (size == src.length) removeOldest();
            int at = (head + size) % src.length;
            src[at] = source; dst[at] = destination; ts[at] = timestamp;
            size++;
            byDest.computeIfAbsent(destination, x -> new Dest()).times.add(timestamp);
            return true;
        }

        int[] forwardPacket() { return size == 0 ? new int[0] : removeOldest(); }

        int getCount(int destination, int startTime, int endTime) {
            Dest d = byDest.get(destination);
            if (d == null) return 0;
            // Live entries are d.times[from..end); both bounds are binary searches on the sorted part.
            return lowerBound(d.times, d.from, endTime + 1) - lowerBound(d.times, d.from, startTime);
        }

        // First index in [lo, list.size()) whose value is at least x.
        private static int lowerBound(List<Integer> list, int lo, int x) {
            int hi = list.size();
            while (lo < hi) { int mid = (lo + hi) >>> 1; if (list.get(mid) < x) lo = mid + 1; else hi = mid; }
            return lo;
        }
    }

    /** Oracle: a list of packets scanned linearly. Time: O(n) per call. Space: O(n). */
    static final class Oracle {
        private final ArrayList<int[]> l = new ArrayList<>();
        private final int limit;
        Oracle(int limit) { this.limit = limit; }
        boolean addPacket(int s, int d, int t) {
            for (int[] p : l) if (p[0] == s && p[1] == d && p[2] == t) return false;
            if (l.size() == limit) l.remove(0);
            l.add(new int[] {s, d, t});
            return true;
        }
        int[] forwardPacket() { return l.isEmpty() ? new int[0] : l.remove(0); }
        int getCount(int d, int a, int b) { int c = 0; for (int[] p : l) if (p[1] == d && p[2] >= a && p[2] <= b) c++; return c; }
    }

    public static void main(String[] args) {
        // Example 1: duplicate rejection, eviction at the limit, a count and four forwards.
        Router r = new Router(3);
        if (!r.addPacket(1, 4, 10) || !r.addPacket(2, 4, 11) || r.addPacket(1, 4, 10) || !r.addPacket(3, 5, 12) || !r.addPacket(4, 4, 13)) throw new AssertionError("e1 adds");
        if (r.getCount(4, 10, 13) != 2) throw new AssertionError("e1 count");
        if (!java.util.Arrays.equals(r.forwardPacket(), new int[] {2, 4, 11}) || !java.util.Arrays.equals(r.forwardPacket(), new int[] {3, 5, 12})
            || !java.util.Arrays.equals(r.forwardPacket(), new int[] {4, 4, 13}) || r.forwardPacket().length != 0) throw new AssertionError("e1 forwards");
        // Example 2: an evicted packet can be added again.
        r = new Router(2);
        if (!r.addPacket(1, 1, 5) || !r.addPacket(2, 1, 5) || !r.addPacket(3, 2, 5) || !r.addPacket(1, 1, 5) || r.getCount(1, 5, 5) != 1) throw new AssertionError("e2");
        // Largest legal field values: the identity must stay exact at the limits.
        r = new Router(2);
        if (!r.addPacket(200_000, 200_000, 1_000_000_000) || r.addPacket(200_000, 200_000, 1_000_000_000) || r.getCount(200_000, 1, 1_000_000_000) != 1) throw new AssertionError("large");
        // Random sequences with nondecreasing timestamps compared with the oracle.
        Random rnd = new Random(3604L);
        for (int t = 0; t < 2000; t++) {
            int limit = 2 + rnd.nextInt(4);
            Router a = new Router(limit);
            Oracle b = new Oracle(limit);
            int time = 1;
            for (int op = 0; op < 50; op++) {
                int k = rnd.nextInt(5);
                if (k <= 2) {
                    time += rnd.nextInt(2);
                    int s = 1 + rnd.nextInt(3), d = 1 + rnd.nextInt(3);
                    if (a.addPacket(s, d, time) != b.addPacket(s, d, time)) throw new AssertionError("add");
                } else if (k == 3) {
                    if (!java.util.Arrays.equals(a.forwardPacket(), b.forwardPacket())) throw new AssertionError("forward");
                } else {
                    int d = 1 + rnd.nextInt(3), lo = 1 + rnd.nextInt(time), hi = lo + rnd.nextInt(3);
                    if (a.getCount(d, lo, hi) != b.getCount(d, lo, hi)) throw new AssertionError("count");
                }
            }
        }
    }
}
```
