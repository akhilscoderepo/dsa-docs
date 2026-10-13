<!-- solutions-for: 91-containers-and-api-state -->
### Solutions For Containers And API State

#### Solution: [Build] Bounded Queue Contract (Author exercise)
<!-- id: cs-bounded-queue-contract -->

**Approach.**
The state is three fields: the array `slots`, the index `head` of the oldest element, and the count `size`. The live window is the `size` slots that start at `head` and wrap modulo the capacity. A private method `slot(i)` owns the arithmetic `(head + i) % capacity`, so no other method repeats it. A full `offer` has exactly one extra step compared with a rejecting queue: it reads the oldest value, overwrites that same slot with the new value, and advances `head`. The slot that held the oldest element is the slot one past the newest element when the window is full, so the write lands in the right place.

The invariant is that after every call, `0 <= size <= capacity` and the live window lists the elements from oldest to newest. Each of `offer`, `poll`, `size` and `at` reads `size` before it writes, so no branch leaves the fields half updated.

**Complexity.**
- **Time** is O(1) for every method, because each call performs a fixed number of array reads, one modulo operation and one or two integer updates.
- **Space** is O(capacity) for the array, with no allocation inside any call.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class BoundedQueueContract {
    static final class BoundedQueue {
        private final int[] slots;
        private int head, size;

        BoundedQueue(int capacity) { slots = new int[capacity]; }

        /**
         * Maps a position in the live window to an array index.
         * Time: O(1). Space: O(1).
         * Invariant: the result lies in 0..capacity-1 for 0 <= i <= size.
         */
        private int slot(int i) {
            // head + i is below twice the capacity, so one modulo wraps it.
            return (head + i) % slots.length;
        }

        /**
         * Appends v and evicts the oldest element when the queue is full.
         * Time: O(1), because there is no shifting. Space: O(1).
         * Invariant: size never exceeds the capacity after the call.
         */
        int offer(int v) {
            // A full queue evicts the oldest element, which sits in slot head.
            if (size == slots.length) {
                int evicted = slots[head];
                // The new value reuses the evicted slot, which is one past the newest element.
                slots[head] = v;
                // The oldest element is now the one after the evicted slot.
                head = (head + 1) % slots.length;
                return evicted;
            }
            // A non-full queue writes at the first slot past the live window.
            slots[slot(size)] = v;
            size++;
            // Nothing was evicted.
            return -1;
        }

        /**
         * Removes and returns the oldest element, or -1 when empty.
         * Time: O(1). Space: O(1).
         * Invariant: the removed slot leaves the live window, and size drops by one.
         */
        int poll() {
            // An empty queue has no element and changes nothing.
            if (size == 0) return -1;
            int v = slots[head];
            // The window starts one slot later.
            head = (head + 1) % slots.length;
            size--;
            return v;
        }

        // Number of stored elements.
        int size() { return size; }

        /**
         * Returns the i-th oldest element or -1.
         * Time: O(1). Space: O(1).
         * Invariant: only indexes 0..size-1 read the live window.
         */
        int at(int i) {
            // Positions outside the live window hold stale data and are never read.
            return i < 0 || i >= size ? -1 : slots[slot(i)];
        }
    }

    public static void main(String[] args) {
        // Example 1 of the exercise, in call order.
        BoundedQueue q = new BoundedQueue(3);
        int[] got = {q.offer(4), q.offer(5), q.offer(6), q.offer(7), q.at(0), q.poll(), q.offer(8), q.offer(9)};
        int[] want = {-1, -1, -1, 4, 5, 5, -1, 6};
        for (int i = 0; i < want.length; i++) if (got[i] != want[i]) throw new AssertionError("example 1 call " + i);
        // Example 2: capacity one evicts on every second offer.
        BoundedQueue one = new BoundedQueue(1);
        if (one.offer(2) != -1 || one.offer(3) != 2 || one.poll() != 3 || one.poll() != -1 || one.size() != 0)
            throw new AssertionError("example 2");
        // A query outside the live window returns -1, even right after a poll left stale data.
        if (q.at(-1) != -1 || q.at(3) != -1) throw new AssertionError("at bounds");
        // Random calls checked against an ArrayDeque that follows the same contract.
        Random rnd = new Random(3601L);
        for (int t = 0; t < 3000; t++) {
            int cap = 1 + rnd.nextInt(5);
            BoundedQueue a = new BoundedQueue(cap);
            ArrayDeque<Integer> model = new ArrayDeque<>();
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(4);
                if (op <= 1) {
                    int v = rnd.nextInt(100);
                    int expect = -1;
                    // The model evicts the first element when it already holds cap elements.
                    if (model.size() == cap) expect = model.pollFirst();
                    model.addLast(v);
                    if (a.offer(v) != expect) throw new AssertionError("offer");
                } else if (op == 2) {
                    Integer m = model.pollFirst();
                    if (a.poll() != (m == null ? -1 : m)) throw new AssertionError("poll");
                } else {
                    // Compare the whole live window, not only one element.
                    if (a.size() != model.size()) throw new AssertionError("size");
                    int i = 0;
                    for (int x : model) if (a.at(i++) != x) throw new AssertionError("at");
                    if (a.at(i) != -1) throw new AssertionError("at past end");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Circular Queue With Status Codes (LeetCode 622)
<!-- id: cs-circular-queue-status -->

**Approach.**
The class keeps `slots`, `head` and `size`, and it never stores a tail index. The newest element lives in slot `(head + size - 1) % k`, and the next write goes to `(head + size) % k`. Storing only `size` to separate full from empty means the two states differ even when `head` equals the write position. Each mutating method checks its rejection condition first and returns the code 1 before touching any field, so a rejected call has atomicity. An accepted call writes the slot and then updates `size` or `head`.

The invariant is that the live window of `size` slots from `head` contains the queue from front to back after every call. The method `snapshot` reads exactly that window into a new array, so a caller can compare the whole queue with a model after each step.

**Complexity.**
- **Time** is O(1) for every method except `snapshot`, which takes O(size) because it copies each live slot once.
- **Space** is O(k) for the array, and `snapshot` allocates O(size) for its result.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class CircularQueueStatus {
    static final class StatusQueue {
        private final int[] slots;
        private int head, size;

        StatusQueue(int k) { slots = new int[k]; }

        /**
         * Appends v, or returns 1 and changes nothing when full.
         * Time: O(1). Space: O(1).
         * Invariant: a return of 1 leaves head and size equal to their values on entry.
         */
        int enQueue(int v) {
            // Check first: the rejection path writes nothing.
            if (size == slots.length) return 1;
            // The first free slot is one past the live window.
            slots[(head + size) % slots.length] = v;
            size++;
            return 0;
        }

        /**
         * Removes the front, or returns 1 and changes nothing when empty.
         * Time: O(1). Space: O(1).
         * Invariant: the live window shrinks from the front only.
         */
        int deQueue() {
            // Check first: an empty queue has no front to remove.
            if (size == 0) return 1;
            head = (head + 1) % slots.length;
            size--;
            return 0;
        }

        // Oldest element or -1; the slot at head is read only when size is positive.
        int front() { return size == 0 ? -1 : slots[head]; }

        // Newest element or -1; its slot is computed from head and size, with no stored tail.
        int rear() { return size == 0 ? -1 : slots[(head + size - 1) % slots.length]; }

        boolean isEmpty() { return size == 0; }

        boolean isFull() { return size == slots.length; }

        /**
         * Copies the live window from front to back.
         * Time: O(size), one read per live slot. Space: O(size) for the new array.
         * Invariant: the result has length size and does not alias slots.
         */
        int[] snapshot() {
            int[] out = new int[size];
            // Walk the window in order; the index arithmetic wraps past the array end.
            for (int i = 0; i < size; i++) out[i] = slots[(head + i) % slots.length];
            return out;
        }
    }

    public static void main(String[] args) {
        // Example 1: the fourth enQueue is rejected, and the refill after deQueue wraps around.
        StatusQueue q = new StatusQueue(3);
        int[] codes = {q.enQueue(1), q.enQueue(2), q.enQueue(3), q.enQueue(4)};
        if (!Arrays.equals(codes, new int[] {0, 0, 0, 1})) throw new AssertionError("codes");
        if (q.rear() != 3 || !q.isFull() || q.deQueue() != 0 || q.enQueue(4) != 0) throw new AssertionError("example 1");
        if (!Arrays.equals(q.snapshot(), new int[] {2, 3, 4})) throw new AssertionError("snapshot");
        // Example 2: capacity one.
        StatusQueue one = new StatusQueue(1);
        if (one.deQueue() != 1 || one.enQueue(9) != 0 || one.front() != 9 || one.rear() != 9
                || one.deQueue() != 0 || !one.isEmpty() || one.front() != -1) throw new AssertionError("example 2");
        // Random sequences against an ArrayDeque; every step compares the full snapshot.
        Random rnd = new Random(3602L);
        for (int t = 0; t < 3000; t++) {
            int cap = 1 + rnd.nextInt(6);
            StatusQueue a = new StatusQueue(cap);
            ArrayDeque<Integer> model = new ArrayDeque<>();
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) {
                    int v = rnd.nextInt(1001);
                    int expect = model.size() == cap ? 1 : 0;
                    if (expect == 0) model.addLast(v);
                    if (a.enQueue(v) != expect) throw new AssertionError("enQueue");
                } else if (op == 1) {
                    int expect = model.isEmpty() ? 1 : 0;
                    if (expect == 0) model.pollFirst();
                    if (a.deQueue() != expect) throw new AssertionError("deQueue");
                }
                // After any call, including rejected ones, the representation must match the model.
                int[] snap = a.snapshot();
                if (snap.length != model.size()) throw new AssertionError("length");
                int i = 0;
                for (int x : model) if (snap[i++] != x) throw new AssertionError("content");
                if (a.front() != (model.isEmpty() ? -1 : model.peekFirst())) throw new AssertionError("front");
                if (a.rear() != (model.isEmpty() ? -1 : model.peekLast())) throw new AssertionError("rear");
                if (a.isFull() != (model.size() == cap) || a.isEmpty() != model.isEmpty()) throw new AssertionError("flags");
            }
        }
    }
}
```

#### Solution: [Boundary] Deque Of Capacity One With A Call Log (LeetCode 641)
<!-- id: cs-deque-capacity-one-log -->

**Approach.**
A deque needs both ends to move. The field `head` is the slot of the front element, `insertLast` writes slot `(head + size) % k`, and `insertFront` first moves `head` back to `(head - 1 + k) % k` and then writes there. The addition of `k` keeps the operand non-negative, because Java's `%` returns a negative result for a negative left operand. The rear element sits at `(head + size - 1) % k`. With capacity one, both formulas give slot 0, so the front and the rear are the same slot and no special case is needed.

Each mutating method decides accepted or rejected first, appends `A` or `R` to the log, and writes only on acceptance. The log is a separate field with its own single writer, the private method `record`. The invariant is that the live window is correct after every call and that the log length equals the number of mutating calls so far.

**Complexity.**
- **Time** is O(1) per call for the deque operations, since each uses one modulo and a few updates, and appending to the log costs O(1) amortized.
- **Space** is O(k) for the slots plus O(m) for the log of m mutating calls.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class DequeCapacityOneLog {
    static final class LoggedDeque {
        private final int[] slots;
        private int head, size;
        private final StringBuilder log = new StringBuilder();

        LoggedDeque(int k) { slots = new int[k]; }

        // The only writer of the log: A for accepted, R for rejected.
        private boolean record(boolean accepted) {
            log.append(accepted ? 'A' : 'R');
            return accepted;
        }

        /**
         * Inserts v before the front, or rejects when full.
         * Time: O(1). Space: O(1).
         * Invariant: head moves back by one slot only when the call is accepted.
         */
        boolean insertFront(int v) {
            // Rejection check precedes every write.
            if (size == slots.length) return record(false);
            // Adding the length keeps the operand non-negative before the modulo.
            head = (head - 1 + slots.length) % slots.length;
            slots[head] = v;
            size++;
            return record(true);
        }

        /**
         * Inserts v after the rear, or rejects when full.
         * Time: O(1). Space: O(1).
         * Invariant: the write slot is the first slot past the live window.
         */
        boolean insertLast(int v) {
            if (size == slots.length) return record(false);
            slots[(head + size) % slots.length] = v;
            size++;
            return record(true);
        }

        /**
         * Removes the front, or rejects when empty.
         * Time: O(1). Space: O(1).
         * Invariant: head moves forward by one slot exactly when the call is accepted.
         */
        boolean deleteFront() {
            if (size == 0) return record(false);
            head = (head + 1) % slots.length;
            size--;
            return record(true);
        }

        /**
         * Removes the rear, or rejects when empty.
         * Time: O(1). Space: O(1).
         * Invariant: only size changes, so head still names the front.
         */
        boolean deleteLast() {
            if (size == 0) return record(false);
            size--;
            return record(true);
        }

        // Front element or -1 when empty.
        int getFront() { return size == 0 ? -1 : slots[head]; }

        // Rear element or -1 when empty.
        int getRear() { return size == 0 ? -1 : slots[(head + size - 1) % slots.length]; }

        // Copy of the log, so the caller cannot change it.
        String log() { return log.toString(); }
    }

    public static void main(String[] args) {
        // Example 1: with capacity one, every second mutating call is rejected.
        LoggedDeque d = new LoggedDeque(1);
        if (!d.insertFront(5) || d.insertLast(6) || d.getRear() != 5 || !d.deleteLast() || d.deleteFront()
                || !d.log().equals("ARAR")) throw new AssertionError("example 1");
        // Example 2: capacity two, inserts at both ends, then a wraparound at the rear.
        LoggedDeque e = new LoggedDeque(2);
        if (!e.insertLast(1) || !e.insertFront(2) || e.insertFront(3) || e.getFront() != 2 || e.getRear() != 1
                || !e.deleteLast() || !e.insertLast(4) || e.getRear() != 4 || !e.log().equals("AARAA"))
            throw new AssertionError("example 2");
        // Java's remainder is negative for a negative left operand, which is why the code adds the length.
        if (-1 % 3 != -1) throw new AssertionError("remainder sign");
        // Random sequences against ArrayDeque, with a model log built from the model's accept decisions.
        Random rnd = new Random(3603L);
        for (int t = 0; t < 3000; t++) {
            int cap = 1 + rnd.nextInt(4);
            LoggedDeque a = new LoggedDeque(cap);
            ArrayDeque<Integer> model = new ArrayDeque<>();
            StringBuilder modelLog = new StringBuilder();
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(6);
                int v = rnd.nextInt(1001);
                boolean expect, got;
                switch (op) {
                    case 0 -> { expect = model.size() < cap; if (expect) model.addFirst(v); got = a.insertFront(v); modelLog.append(expect ? 'A' : 'R'); }
                    case 1 -> { expect = model.size() < cap; if (expect) model.addLast(v); got = a.insertLast(v); modelLog.append(expect ? 'A' : 'R'); }
                    case 2 -> { expect = !model.isEmpty(); if (expect) model.pollFirst(); got = a.deleteFront(); modelLog.append(expect ? 'A' : 'R'); }
                    case 3 -> { expect = !model.isEmpty(); if (expect) model.pollLast(); got = a.deleteLast(); modelLog.append(expect ? 'A' : 'R'); }
                    default -> { expect = got = true; }
                }
                if (expect != got) throw new AssertionError("op " + op);
                // Reads must agree and must not change the log.
                if (a.getFront() != (model.isEmpty() ? -1 : model.peekFirst())) throw new AssertionError("front");
                if (a.getRear() != (model.isEmpty() ? -1 : model.peekLast())) throw new AssertionError("rear");
                if (!a.log().equals(modelLog.toString())) throw new AssertionError("log");
            }
        }
    }
}
```

#### Solution: [Recognize] Implement Router (LeetCode 3508)
<!-- id: cs-router-expiry-index -->

**Approach.**
The router has three collections that must describe one packet set. A ring array of records keeps arrival order and evicts the oldest packet. A hash set of records answers the duplicate question. A map from destination to a list of timestamps, with a start offset per destination, answers `getCount`. Timestamps never decrease across additions, so each destination list is sorted, and two binary searches count the entries in a range. The oldest packet overall is also the oldest packet of its own destination, so removing it moves that destination's offset by one and never needs a deletion in the middle of a list.

Inside `addPacket`, the duplicate check runs before the eviction. A rejected duplicate then evicts nothing, and the three collections stay unchanged. Every removal goes through one private method `drop`, which updates the ring, the set and the offset together. The invariant is that the packets in the ring, the records in the set, and the entries from each offset onward in the lists are the same set.

**Complexity.**
- **Time** is O(1) expected for `addPacket` and `forwardPacket`, and O(log n) for `getCount`, where n counts additions to one destination.
- **Space** is O(memoryLimit) for the ring and the set, plus O(a) for the lists, because the lists keep consumed entries and hold every accepted addition a.

```java run
import java.util.*;

public final class RouterExpiryIndex {
    static final class Router {
        record P(int s, int d, int t) {}
        private final P[] ring;
        private int head, size;
        private final Set<P> seen = new HashSet<>();
        private final Map<Integer, List<Integer>> times = new HashMap<>();
        private final Map<Integer, Integer> lo = new HashMap<>();

        Router(int memoryLimit) { ring = new P[memoryLimit]; }

        /**
         * Adds a packet, evicting the oldest when full; rejects exact duplicates first.
         * Time: O(1) expected. Space: O(1) beyond the stored lists.
         * Invariant: a false return changes no collection.
         */
        boolean addPacket(int s, int d, int t) {
            P p = new P(s, d, t);
            // Reject before any eviction, so a rejected call cannot lose a packet.
            if (seen.contains(p)) return false;
            if (size == ring.length) drop();
            ring[(head + size) % ring.length] = p;
            size++;
            seen.add(p);
            times.computeIfAbsent(d, k -> new ArrayList<>()).add(t);
            return true;
        }

        // Removes the oldest packet from the ring, the set and its destination offset together.
        private P drop() {
            P p = ring[head];
            ring[head] = null;
            head = (head + 1) % ring.length;
            size--;
            seen.remove(p);
            lo.merge(p.d(), 1, Integer::sum);
            return p;
        }

        // Forwards the oldest packet, or returns an empty array when there is none.
        int[] forwardPacket() {
            if (size == 0) return new int[0];
            P p = drop();
            return new int[] {p.s(), p.d(), p.t()};
        }

        /**
         * Counts live packets for d with startTime <= timestamp <= endTime.
         * Time: O(log n) for two binary searches. Space: O(1).
         * Invariant: entries before lo[d] are removed packets and are never counted.
         */
        int getCount(int d, int a, int b) {
            List<Integer> l = times.get(d);
            if (l == null) return 0;
            int from = lo.getOrDefault(d, 0);
            return lower(l, b + 1, from) - lower(l, a, from);
        }

        // First index at or after from whose value is at least x.
        private static int lower(List<Integer> l, int x, int from) {
            int lo = from, hi = l.size();
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (l.get(mid) < x) lo = mid + 1; else hi = mid;
            }
            return lo;
        }
    }

    // Brute force: a plain list of live packets scanned on every query.
    static final class Oracle {
        private final int limit;
        private final ArrayList<int[]> live = new ArrayList<>();
        Oracle(int limit) { this.limit = limit; }
        boolean add(int s, int d, int t) {
            for (int[] p : live) if (p[0] == s && p[1] == d && p[2] == t) return false;
            if (live.size() == limit) live.remove(0);
            live.add(new int[] {s, d, t});
            return true;
        }
        int[] forward() { return live.isEmpty() ? new int[0] : live.remove(0); }
        int count(int d, int a, int b) {
            int c = 0;
            for (int[] p : live) if (p[1] == d && p[2] >= a && p[2] <= b) c++;
            return c;
        }
    }

    public static void main(String[] args) {
        // Example 1: duplicate rejected, eviction on the fifth add, then forward and two queries.
        Router r = new Router(3);
        if (!r.addPacket(1, 4, 10) || !r.addPacket(2, 4, 10) || r.addPacket(1, 4, 10) || !r.addPacket(3, 5, 12)
                || !r.addPacket(2, 5, 13)) throw new AssertionError("example 1 adds");
        if (!Arrays.equals(r.forwardPacket(), new int[] {2, 4, 10}) || r.getCount(4, 10, 10) != 0
                || r.getCount(5, 12, 13) != 2) throw new AssertionError("example 1 reads");
        // Example 2: eviction moves the destination offset, so the old timestamp is no longer counted.
        Router q = new Router(2);
        if (!q.addPacket(7, 1, 5) || !q.addPacket(8, 1, 6) || q.getCount(1, 5, 6) != 2 || !q.addPacket(9, 1, 6)
                || q.getCount(1, 5, 6) != 2 || q.getCount(1, 5, 5) != 0) throw new AssertionError("example 2");
        // Random sequences with nondecreasing timestamps, compared with the brute force after every call.
        Random rnd = new Random(3604L);
        for (int t = 0; t < 3000; t++) {
            int limit = 2 + rnd.nextInt(4);
            Router a = new Router(limit);
            Oracle o = new Oracle(limit);
            int ts = 1;
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) {
                    // Small value ranges force duplicates and many equal timestamps.
                    ts += rnd.nextInt(3);
                    int s = 1 + rnd.nextInt(3), d = 1 + rnd.nextInt(3);
                    if (a.addPacket(s, d, ts) != o.add(s, d, ts)) throw new AssertionError("add");
                } else if (op == 1) {
                    if (!Arrays.equals(a.forwardPacket(), o.forward())) throw new AssertionError("forward");
                } else {
                    int d = 1 + rnd.nextInt(3), x = 1 + rnd.nextInt(ts + 1), y = x + rnd.nextInt(5);
                    if (a.getCount(d, x, y) != o.count(d, x, y)) throw new AssertionError("count");
                }
            }
        }
    }
}
```
