<!-- solutions-for: 05-validated-priority -->
### Solutions For Validated Priority

#### Solution: [Build] Versioned Heap Entry (Author exercise)
<!-- id: ci40-versioned-heap -->

**Approach.** The record is a hash map from job id to the newest heap entry of that job. A set call builds a new immutable entry, stores it in the record and adds it to the heap. The older entry of the same job stays in the heap. A cancel call removes the job from the record.

A poll call pops entries until one is current. An entry is current when the record holds that very object for its id. The object itself acts as the version, because every set call creates a new object, so no two calls ever share one. The size is the size of the record.

The invariant is that every live job has exactly one current entry in the heap, and a popped entry is returned only if the record still points to it.

**Complexity.**

- **Time** is O(log n) per set call, and a poll call costs O(log n) for each entry it pops. Each entry is popped once, so the cost is O(log n) amortized per call.
- **Space** is O(m), where m is the number of set calls since the heap was last emptied, because stale entries stay until they reach the top.

```java run
import java.util.*;

public final class VersionedHeapSolution {
    static final class JobBoard {
        private record Entry(int priority, int id) {}                       // a fresh object per set call
        private final PriorityQueue<Entry> heap = new PriorityQueue<>((a, b) ->
                a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(a.id(), b.id()));
        private final Map<Integer, Entry> newest = new HashMap<>();         // id -> its current entry, source of truth

        /**
         * Adds a job or changes its priority.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: newest.get(id) is the only current entry of the job.
         */
        void set(int id, int priority) {
            Entry e = new Entry(priority, id);
            newest.put(id, e);
            heap.add(e);
        }

        /** Deletes a live job; O(1) time and space; invariant: its heap entries stop matching the record. */
        void cancel(int id) { newest.remove(id); }

        /**
         * Removes and returns the best live job.
         * Time: O(log n) per popped entry.
         * Space: O(1) extra.
         * Invariant: a popped entry is returned only if the record holds the same object.
         */
        int poll() {
            while (!heap.isEmpty()) {
                Entry e = heap.poll();
                // Identity comparison tells the newest entry from every older one, even with equal fields.
                if (newest.get(e.id()) == e) { newest.remove(e.id()); return e.id(); }
            }
            return -1;
        }

        /** Returns the number of live jobs; O(1) time and space. */
        int size() { return newest.size(); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        JobBoard a = new JobBoard();
        a.set(1, 5); a.set(2, 9); a.set(1, 12);
        if (a.poll() != 1 || a.poll() != 2 || a.poll() != -1) throw new AssertionError("e1");
        JobBoard b = new JobBoard();
        b.set(4, 3); b.cancel(4);
        if (b.size() != 0 || b.poll() != -1) throw new AssertionError("e2");
        // Random calls checked against a scan of a plain map.
        Random rnd = new Random(5001);
        for (int round = 0; round < 300; round++) {
            JobBoard s = new JobBoard();
            Map<Integer, Integer> ref = new HashMap<>();
            for (int op = 0; op < 100; op++) {
                int t = rnd.nextInt(4);
                if (t == 0) { int id = rnd.nextInt(6), p = rnd.nextInt(4); ref.put(id, p); s.set(id, p); }
                else if (t == 1 && !ref.isEmpty()) { int id = new ArrayList<>(ref.keySet()).get(rnd.nextInt(ref.size())); ref.remove(id); s.cancel(id); }
                else if (t == 2) {
                    int best = -1;
                    for (int id : ref.keySet()) if (best == -1 || ref.get(id) > ref.get(best) || (ref.get(id).equals(ref.get(best)) && id < best)) best = id;
                    if (best != -1) ref.remove(best);
                    if (s.poll() != best) throw new AssertionError("poll");
                } else if (s.size() != ref.size()) throw new AssertionError("size");
            }
        }
    }
}
```

#### Solution: [Vary] Design Movie Rental System (LeetCode 1912)
<!-- id: ci40-rental-report -->

**Approach.** A hash map from the copy key to its rent version holds exactly the rented copies, and it is the source of truth. Every rent call increments a counter, stores the new version in the map and adds a heap entry that carries the same version. A drop call removes the copy from the map.

A report call pops entries from the heap and keeps those whose version equals the stored version, until it has five or the heap is empty. Popped stale entries are discarded for good. The call then pushes the kept entries back, so the report does not change the state. A copy rented, dropped and rented again has two entries, and only the newer one matches, so the copy appears once.

The invariant is that each rented copy has exactly one current entry in the heap, and every popped entry that fails the check is dropped.

**Complexity.**

- **Time** is O(log n) per rent call and O((s + 5) log n) per report call, where s counts the stale entries it drops. Each stale entry is dropped once, so the drops add O(log n) amortized per earlier rent call.
- **Space** is O(m), where m is the number of rent calls, because stale entries stay until a report reaches them.

```java run
import java.util.*;

public final class RentalReportSolution {
    static final class RentalReport {
        private record Item(int price, int shop, int movie, int version) {}
        private final Map<Long, Integer> price = new HashMap<>();             // pair key -> fixed price
        private final Map<Long, Integer> rentedVersion = new HashMap<>();     // rented pair key -> newest version
        private final PriorityQueue<Item> heap = new PriorityQueue<>((a, b) -> {
            int c = Integer.compare(a.price(), b.price());
            if (c != 0) return c;
            c = Integer.compare(a.shop(), b.shop());
            return c != 0 ? c : Integer.compare(a.movie(), b.movie());
        });
        private int clock = 0;

        private static long key(int shop, int movie) { return ((long) shop << 32) | movie; }

        RentalReport(int[][] entries) {
            for (int[] e : entries) price.put(key(e[0], e[1]), e[2]);
        }

        /** Marks a copy rented and adds one candidate; O(log n) time, O(1) space; invariant: the record holds the newest version. */
        void rent(int shop, int movie) {
            int v = ++clock;
            rentedVersion.put(key(shop, movie), v);
            heap.add(new Item(price.get(key(shop, movie)), shop, movie, v));
        }

        /** Marks a copy unrented; O(1) time and space; invariant: its candidates stop matching the record. */
        void drop(int shop, int movie) { rentedVersion.remove(key(shop, movie)); }

        /**
         * Lists up to 5 cheapest rented copies without changing the state.
         * Time: O((s + 5) log n) for s stale entries dropped.
         * Space: O(1) extra.
         * Invariant: the kept entries return to the heap, so a second report gives the same answer.
         */
        List<int[]> report() {
            List<Item> kept = new ArrayList<>();
            while (kept.size() < 5 && !heap.isEmpty()) {
                Item it = heap.poll();
                Integer v = rentedVersion.get(key(it.shop(), it.movie()));
                // Keep only the newest candidate of a rented copy; drop the rest for good.
                if (v != null && v == it.version()) kept.add(it);
            }
            List<int[]> out = new ArrayList<>();
            for (Item it : kept) { out.add(new int[] {it.shop(), it.movie()}); heap.add(it); }
            return out;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        int[][] entries = {{0, 1, 5}, {0, 2, 6}, {1, 1, 4}};
        RentalReport a = new RentalReport(entries);
        a.rent(0, 1); a.rent(1, 1);
        List<int[]> r1 = a.report();
        if (r1.size() != 2 || r1.get(0)[0] != 1 || r1.get(0)[1] != 1 || r1.get(1)[0] != 0 || r1.get(1)[1] != 1) throw new AssertionError("e1");
        RentalReport b = new RentalReport(entries);
        b.rent(1, 1); b.drop(1, 1); b.rent(1, 1); b.rent(0, 2);
        List<int[]> r2 = b.report();
        if (r2.size() != 2 || r2.get(0)[0] != 1 || r2.get(1)[1] != 2) throw new AssertionError("e2");
        // Random calls checked against a sort of the rented copies, including repeated reports.
        Random rnd = new Random(5002);
        for (int round = 0; round < 200; round++) {
            List<int[]> list = new ArrayList<>();
            for (int s = 0; s < 4; s++) for (int v = 0; v < 3; v++) if (rnd.nextInt(3) > 0) list.add(new int[] {s, v, 1 + rnd.nextInt(5)});
            int[][] es = list.toArray(new int[0][]);
            RentalReport sut = new RentalReport(es);
            boolean[] out = new boolean[es.length];
            for (int op = 0; op < 100; op++) {
                int k = rnd.nextInt(es.length), t = rnd.nextInt(3);
                if (t == 0 && !out[k]) { out[k] = true; sut.rent(es[k][0], es[k][1]); }
                else if (t == 1 && out[k]) { out[k] = false; sut.drop(es[k][0], es[k][1]); }
                else if (t == 2) {
                    List<int[]> want = new ArrayList<>();
                    for (int i = 0; i < es.length; i++) if (out[i]) want.add(es[i]);
                    want.sort((x, y) -> x[2] != y[2] ? Integer.compare(x[2], y[2]) : x[0] != y[0] ? Integer.compare(x[0], y[0]) : Integer.compare(x[1], y[1]));
                    for (int pass = 0; pass < 2; pass++) {
                        List<int[]> got = sut.report();
                        if (got.size() != Math.min(5, want.size())) throw new AssertionError("size");
                        for (int i = 0; i < got.size(); i++) if (got.get(i)[0] != want.get(i)[0] || got.get(i)[1] != want.get(i)[1]) throw new AssertionError("order");
                    }
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Repeated Corrections (Author exercise)
<!-- id: ci40-repeated-corrections -->

**Approach.** The record maps each live id to its priority and newest version, and the heap holds candidates stamped with versions. A set call adds a candidate. A peek call drops stale candidates from the top until the top matches the record, and it leaves that live candidate in place. A poll call runs the same loop and then removes the live top.

Because peek removes only entries that fail the version check, it never changes an answer. Thousands of corrections to one id would still grow the heap. Every mutating call therefore compares the heap size with twice the live count plus 16. When the heap is larger, the call rebuilds the heap from the record, which holds exactly one candidate per live job.

The invariant is that the record decides every answer, and after every call the heap holds at most `2 * live + 16` entries.

**Complexity.**

- **Time** is O(log n) amortized per call. A rebuild costs O(n) and runs only after the heap has grown by at least `live + 16` entries, which pays for it.
- **Space** is O(live) after every call, because the rebuild rule bounds the heap.

```java run
import java.util.*;

public final class RepeatedCorrectionsSolution {
    static final class Desk {
        private record Entry(int priority, int id, int version) {}
        private final PriorityQueue<Entry> heap = new PriorityQueue<>((a, b) ->
                a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(a.id(), b.id()));
        private final Map<Integer, int[]> record = new HashMap<>();           // id -> {priority, version}
        private int clock = 0;

        // Rebuilds the heap from the record when stale entries dominate; O(n) time, O(n) space.
        private void compact() {
            if (heap.size() <= 2 * record.size() + 16) return;
            heap.clear();
            for (Map.Entry<Integer, int[]> e : record.entrySet()) heap.add(new Entry(e.getValue()[0], e.getKey(), e.getValue()[1]));
        }

        /** Adds a job or changes its priority; O(log n) amortized time, O(1) extra space; invariant: the record holds the newest version. */
        void set(int id, int priority) {
            record.put(id, new int[] {priority, ++clock});
            heap.add(new Entry(priority, id, clock));
            compact();
        }

        /** Deletes a live job; O(1) amortized time, O(1) space; invariant: its entries stop matching the record. */
        void cancel(int id) { record.remove(id); compact(); }

        // Drops stale entries from the top until the top matches the record or the heap is empty.
        private Entry liveTop() {
            while (!heap.isEmpty()) {
                Entry e = heap.peek();
                int[] r = record.get(e.id());
                if (r != null && r[1] == e.version()) return e;
                heap.poll();
            }
            return null;
        }

        /** Returns the best live id without removing it; O(log n) amortized time, O(1) space; invariant: only stale entries leave the heap. */
        int peek() {
            Entry e = liveTop();
            return e == null ? -1 : e.id();
        }

        /** Removes and returns the best live id; O(log n) amortized time, O(1) space; invariant: the record and the heap lose the same job. */
        int poll() {
            Entry e = liveTop();
            if (e == null) return -1;
            heap.poll();
            record.remove(e.id());
            compact();
            return e.id();
        }

        int size() { return record.size(); }
        int heapSize() { return heap.size(); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Desk a = new Desk();
        a.set(1, 5); a.set(1, 9); a.set(1, 5);
        if (a.peek() != 1 || a.poll() != 1 || a.peek() != -1) throw new AssertionError("e1");
        Desk b = new Desk();
        b.set(2, 4); b.set(3, 4); b.cancel(2); b.set(2, 4);
        if (b.peek() != 2 || b.poll() != 2 || b.poll() != 3) throw new AssertionError("e2");
        // Heavy corrections of one id keep the heap bounded and the answers unchanged.
        Desk c = new Desk();
        for (int i = 0; i < 10_000; i++) c.set(7, i % 3);
        if (c.heapSize() > 2 * c.size() + 16 || c.peek() != 7 || c.peek() != 7) throw new AssertionError("heavy corrections");
        // Random calls with many peeks, checked against a scan of a plain map.
        Random rnd = new Random(5003);
        for (int round = 0; round < 300; round++) {
            Desk s = new Desk();
            Map<Integer, Integer> ref = new HashMap<>();
            for (int op = 0; op < 150; op++) {
                int t = rnd.nextInt(5);
                if (t <= 1) { int id = rnd.nextInt(5), p = rnd.nextInt(3); ref.put(id, p); s.set(id, p); }
                else if (t == 2 && !ref.isEmpty()) { int id = new ArrayList<>(ref.keySet()).get(rnd.nextInt(ref.size())); ref.remove(id); s.cancel(id); }
                else {
                    int best = -1;
                    for (int id : ref.keySet()) if (best == -1 || ref.get(id) > ref.get(best) || (ref.get(id).equals(ref.get(best)) && id < best)) best = id;
                    if (s.peek() != best || s.peek() != best) throw new AssertionError("peek");
                    if (t == 4) { if (best != -1) ref.remove(best); if (s.poll() != best) throw new AssertionError("poll"); }
                }
                if (s.size() != ref.size() || s.heapSize() > 2 * s.size() + 16) throw new AssertionError("size or bound");
            }
        }
    }
}
```

#### Solution: [Recognize] Design Auction System (LeetCode 3815)
<!-- id: ci40-auction -->

**Approach.** A hash map from the pair of user and item to the current bid and its version is the source of truth. Each item owns a heap of bid candidates, ordered by higher amount first and then by larger user id. Each add call increments a counter, stores the amount and version in the map and adds a candidate to the item's heap. A remove call deletes the pair from the map.

A highest-bidder query looks at the top of the item's heap. If the pair is missing from the map, or its stored version differs from the candidate's version, the candidate is stale and the query pops it. The query stops at the first current candidate and leaves it in place. A user who bids twice has two candidates, and only the newer one matches.

The invariant is that every current bid has exactly one current candidate in its item's heap, and the query exposes a candidate only after the version check.

**Complexity.**

- **Time** is O(log n) per add call and O(log n) amortized per query, because each stale candidate is popped once.
- **Space** is O(b), where b is the number of add calls, because stale candidates stay until a query reaches them.

```java run
import java.util.*;

public final class AuctionSolution {
    static final class Auction {
        private record Bid(int amount, int user, int version) {}
        private final Map<Long, int[]> current = new HashMap<>();                       // (user,item) -> {amount, version}
        private final Map<Integer, PriorityQueue<Bid>> heapOf = new HashMap<>();          // item -> candidates
        private int clock = 0;

        private static long key(int user, int item) { return ((long) user << 32) | item; }

        /**
         * Records a bid and replaces the user's earlier bid on the item.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: the stored version belongs to the newest candidate.
         */
        void addBid(int user, int item, int amount) {
            int v = ++clock;
            current.put(key(user, item), new int[] {amount, v});
            heapOf.computeIfAbsent(item, k -> new PriorityQueue<>((a, b) ->
                    a.amount() != b.amount() ? Integer.compare(b.amount(), a.amount()) : Integer.compare(b.user(), a.user()))).add(new Bid(amount, user, v));
        }

        /** Withdraws a bid; O(1) time and space; invariant: the candidates of the pair stop matching the record. */
        void removeBid(int user, int item) { current.remove(key(user, item)); }

        /**
         * Returns the leading bidder or -1.
         * Time: O(log n) amortized.
         * Space: O(1) extra.
         * Invariant: only stale candidates leave the heap.
         */
        int getHighestBidder(int item) {
            PriorityQueue<Bid> heap = heapOf.get(item);
            if (heap == null) return -1;
            while (!heap.isEmpty()) {
                Bid b = heap.peek();
                int[] cur = current.get(key(b.user(), item));
                // A candidate is current only when the record holds its version.
                if (cur != null && cur[1] == b.version()) return b.user();
                heap.poll();
            }
            return -1;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Auction a = new Auction();
        a.addBid(1, 10, 50); a.addBid(2, 10, 70); a.addBid(1, 10, 80);
        if (a.getHighestBidder(10) != 1) throw new AssertionError("e1");
        Auction b = new Auction();
        b.addBid(1, 10, 50); b.addBid(2, 10, 50);
        if (b.getHighestBidder(10) != 2) throw new AssertionError("e2 tie");
        b.removeBid(2, 10);
        if (b.getHighestBidder(10) != 1 || b.getHighestBidder(99) != -1) throw new AssertionError("e2 after");
        // Random calls checked against a scan of all current bids.
        Random rnd = new Random(3815);
        for (int round = 0; round < 300; round++) {
            Auction s = new Auction();
            Map<Long, Integer> ref = new HashMap<>();
            for (int op = 0; op < 120; op++) {
                int u = rnd.nextInt(4), item = rnd.nextInt(3), t = rnd.nextInt(3);
                long k = ((long) u << 32) | item;
                if (t == 0) { int amt = 1 + rnd.nextInt(4); ref.put(k, amt); s.addBid(u, item, amt); }
                else if (t == 1 && ref.containsKey(k)) { ref.remove(k); s.removeBid(u, item); }
                else {
                    int best = -1, bestAmt = 0;
                    for (int x = 0; x < 4; x++) {
                        Integer amt = ref.get(((long) x << 32) | item);
                        if (amt != null && (amt > bestAmt || (amt == bestAmt && x > best))) { best = x; bestAmt = amt; }
                    }
                    if (s.getHighestBidder(item) != best) throw new AssertionError("highest");
                }
            }
        }
    }
}
```
