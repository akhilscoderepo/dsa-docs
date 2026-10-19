<!-- solutions-for: 92-availability-priority -->
### Solutions For Free Resource Picks

#### Solution: [Build] Seat Counter With Validation (LeetCode 1845)
<!-- id: ci40-seat-counter -->

**Approach.** The class stores three things: the next seat that was never handed out, a min-heap of returned seats, and a hash set of held seats. A reserve call takes the smaller of the heap top and the counter. Every returned seat is below the counter, so a non-empty heap always wins. The call adds the seat to the held set.

An unreserve call returns `false` unless the held set contains the seat. Otherwise it removes the seat from the held set and adds it to the heap, and it returns `true`. A seat that was never handed out is not in the held set, so the call rejects it. A second release of the same seat is rejected as well, because the first release removed it from the held set.

The invariant is that every seat from 1 up to the counter minus 1 is either in the held set or in the heap, exactly once.

**Complexity.**

- **Time** is O(log k) per call for k returned seats, because heap operations cost logarithmic time and the set operations cost O(1).
- **Space** is O(k + h) for h held seats, and it does not depend on `n`.

```java run
import java.util.*;

public final class SeatCounterSolution {
    static final class SeatCounter {
        private int next = 1;                                         // smallest seat never handed out
        private final PriorityQueue<Integer> released = new PriorityQueue<>();
        private final Set<Integer> held = new HashSet<>();

        /**
         * Holds the smallest free seat.
         * Time: O(log k).
         * Space: O(1) extra.
         * Invariant: seats below next are in held or released, exactly once.
         */
        int reserve() {
            // A returned seat is always smaller than the counter, so it wins when present.
            int seat = released.isEmpty() ? next++ : released.poll();
            held.add(seat);
            return seat;
        }

        /** Frees a held seat or rejects the call; O(log k) time, O(1) space; invariant: only held seats enter the heap. */
        boolean unreserve(int seat) {
            // Removing from the held set both checks and records the release in one step.
            if (!held.remove(seat)) return false;
            released.add(seat);
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text, with a billion seats and no listing.
        SeatCounter a = new SeatCounter();
        if (a.reserve() != 1 || a.reserve() != 2 || !a.unreserve(1) || a.unreserve(1) || a.reserve() != 1 || a.reserve() != 3) throw new AssertionError("e1");
        SeatCounter b = new SeatCounter();
        if (b.unreserve(5) || b.reserve() != 1) throw new AssertionError("e2");
        // Random calls including invalid releases, checked against a boolean array.
        Random rnd = new Random(9201);
        for (int round = 0; round < 300; round++) {
            SeatCounter s = new SeatCounter();
            boolean[] held = new boolean[200];
            for (int op = 0; op < 100; op++) {
                if (rnd.nextBoolean()) {
                    int want = 1;
                    while (held[want]) want++;
                    held[want] = true;
                    if (s.reserve() != want) throw new AssertionError("reserve");
                } else {
                    int seat = rnd.nextInt(45) - 2;
                    boolean want = seat >= 1 && seat < 200 && held[seat];
                    if (want) held[seat] = false;
                    if (s.unreserve(seat) != want) throw new AssertionError("unreserve");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Exam Room With A Gap Heap (LeetCode 855)
<!-- id: ci40-exam-room-heap -->

**Approach.** The occupied seats form a doubly linked list stored in two hash maps, `nextOf` and `prevOf`, plus the first and last occupied seat. A candidate is a pair of two seats where `-1` stands for the left end and `n` for the right end. Its seat is 0 for the left end, `n - 1` for the right end, and `left + (right - left) / 2` otherwise. Its distance is `right` for the left end, `n - 1 - left` for the right end, and `(right - left) / 2` otherwise. The heap orders candidates by larger distance and then smaller seat. A candidate with distance 0 is never added.

A seat call pops candidates until one is current. A candidate with two real seats is current when the successor of its left seat is its right seat. A left-end candidate is current when its right seat is the first occupied seat, and a right-end candidate is current when its left seat is the last occupied seat. The call seats the student at the candidate's seat, rewires the links and adds the two halves of the old gap. A leave call unlinks the seat and adds the merged gap of its two neighbors.

The invariant is that every gap between neighbors has a candidate in the heap, and a popped candidate is used only if its two ends are still neighbors.

**Complexity.**

- **Time** is O(log k) amortized per call, because every candidate is added at most once per call and popped at most once.
- **Space** is O(k + c), where c is the number of calls that left stale candidates behind.

```java run
import java.util.*;

public final class ExamRoomHeapSolution {
    static final class GapRoom {
        private record Gap(int left, int right) {}                      // -1 and n stand for the two ends
        private final int n;
        private final Map<Integer, Integer> nextOf = new HashMap<>();   // occupied seat -> next occupied seat, or n
        private final Map<Integer, Integer> prevOf = new HashMap<>();   // occupied seat -> previous occupied seat, or -1
        private int first = -1, last = -1;                              // first and last occupied seats, -1 when empty
        private final PriorityQueue<Gap> heap;

        GapRoom(int n) {
            this.n = n;
            heap = new PriorityQueue<>((a, b) -> {
                int c = Integer.compare(dist(b), dist(a));
                return c != 0 ? c : Integer.compare(pick(a), pick(b));
            });
        }

        private int pick(Gap g) { return g.left() == -1 ? 0 : g.right() == n ? n - 1 : g.left() + (g.right() - g.left()) / 2; }

        private int dist(Gap g) { return g.left() == -1 ? g.right() : g.right() == n ? n - 1 - g.left() : (g.right() - g.left()) / 2; }

        private void offer(Gap g) { if (dist(g) > 0) heap.add(g); }

        // True when the two ends are still neighbors; O(1) time and space.
        private boolean current(Gap g) {
            if (g.left() == -1) return first == g.right();
            if (g.right() == n) return last == g.left();
            Integer succ = nextOf.get(g.left());
            return succ != null && succ == g.right();
        }

        /**
         * Seats a student at the best free seat.
         * Time: O(log k) amortized.
         * Space: O(1) extra.
         * Invariant: only a candidate whose ends are neighbors is used.
         */
        int seat() {
            if (first == -1) {
                first = last = 0;
                nextOf.put(0, n); prevOf.put(0, -1);
                offer(new Gap(0, n));
                return 0;
            }
            Gap g = heap.poll();
            // Drop candidates whose two ends stopped being neighbors.
            while (!current(g)) g = heap.poll();
            int p = pick(g), l = g.left(), r = g.right();
            nextOf.put(p, r); prevOf.put(p, l);
            if (l == -1) first = p; else nextOf.put(l, p);
            if (r == n) last = p; else prevOf.put(r, p);
            offer(new Gap(l, p));
            offer(new Gap(p, r));
            return p;
        }

        /** Frees seat p and offers the merged gap; O(log k) time, O(1) extra space; invariant: the links skip p. */
        void leave(int p) {
            int l = prevOf.remove(p), r = nextOf.remove(p);
            if (l != -1) nextOf.put(l, r); else first = r == n ? -1 : r;
            if (r != n) prevOf.put(r, l); else last = l;
            if (first != -1) offer(new Gap(l, r));
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        GapRoom r = new GapRoom(8);
        int[] got = {r.seat(), r.seat(), r.seat(), r.seat()};
        if (got[0] != 0 || got[1] != 7 || got[2] != 3 || got[3] != 5) throw new AssertionError("e1");
        r.leave(3);
        if (r.seat() != 2) throw new AssertionError("e2");
        // A huge row works because only seated students are stored.
        GapRoom big = new GapRoom(1_000_000_000);
        if (big.seat() != 0 || big.seat() != 999_999_999 || big.seat() != 499_999_999) throw new AssertionError("big row");
        // Random calls checked against a scan of every free seat.
        Random rnd = new Random(855);
        for (int round = 0; round < 400; round++) {
            int n = 2 + rnd.nextInt(14);
            GapRoom s = new GapRoom(n);
            boolean[] occ = new boolean[n];
            int count = 0;
            for (int op = 0; op < 80; op++) {
                if (count < n && (count == 0 || rnd.nextInt(3) > 0)) {
                    int want = 0, wantD = -1;
                    for (int c = 0; c < n; c++) {
                        if (occ[c]) continue;
                        int d = count == 0 ? n : Integer.MAX_VALUE;
                        for (int q = 0; q < n; q++) if (occ[q]) d = Math.min(d, Math.abs(q - c));
                        if (d > wantD) { wantD = d; want = c; }
                    }
                    occ[want] = true; count++;
                    if (s.seat() != want) throw new AssertionError("seat");
                } else {
                    int p = rnd.nextInt(n);
                    while (!occ[p]) p = (p + 1) % n;
                    occ[p] = false; count--;
                    s.leave(p);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Stale Gap Candidate (Author exercise)
<!-- id: ci40-stale-gap -->

**Approach.** A tree set holds the occupied positions. A heap holds candidate pairs ordered by larger difference and then smaller left position. An occupy call finds the lower and higher neighbors of the new position before it inserts the position. It then adds a candidate for each existing neighbor pair that touches the new position. A vacate call finds the same two neighbors after the removal and adds the merged pair when both neighbors exist.

A widest-gap call looks at the heap top. A candidate is current only when both positions are occupied and the occupied position directly above the left one is the right one. A candidate that fails the test is popped and dropped. The first current candidate is returned and stays in the heap.

Checking only the left position is not enough. If position 9 is vacated, the pair (4, 9) keeps its left end occupied and fails only on the right end. If a new position is occupied between 4 and 9, both ends stay occupied and the pair fails only on the adjacency test.

The invariant is that every pair of consecutive occupied positions has a candidate in the heap, and a candidate is returned only after the three-part test passes.

**Complexity.**

- **Time** is O(log k) amortized per call, because each candidate is added once and dropped at most once.
- **Space** is O(k + c) for k occupied positions and c candidates that went stale.

```java run
import java.util.*;

public final class StaleGapSolution {
    static final class GapBook {
        private record Gap(int left, int right) {}
        private final TreeSet<Integer> occupied = new TreeSet<>();
        private final PriorityQueue<Gap> heap = new PriorityQueue<>((a, b) -> {
            int c = Integer.compare(b.right() - b.left(), a.right() - a.left());
            return c != 0 ? c : Integer.compare(a.left(), b.left());
        });

        /** Marks a free position occupied and offers the two new gaps; O(log k) time, O(1) space; invariant: both new pairs enter the heap. */
        void occupy(int seat) {
            Integer lo = occupied.lower(seat), hi = occupied.higher(seat);
            occupied.add(seat);
            if (lo != null) heap.add(new Gap(lo, seat));
            if (hi != null) heap.add(new Gap(seat, hi));
        }

        /** Frees an occupied position and offers the merged gap; O(log k) time, O(1) space; invariant: the merged pair enters the heap. */
        void vacate(int seat) {
            occupied.remove(seat);
            Integer lo = occupied.lower(seat), hi = occupied.higher(seat);
            if (lo != null && hi != null) heap.add(new Gap(lo, hi));
        }

        // The three-part test: both ends occupied and no occupied position between them; O(log k) time.
        private boolean current(Gap g) {
            if (!occupied.contains(g.left()) || !occupied.contains(g.right())) return false;
            Integer above = occupied.higher(g.left());
            return above != null && above == g.right();
        }

        /**
         * Returns the widest pair of consecutive occupied positions.
         * Time: O(log k) amortized.
         * Space: O(1) extra.
         * Invariant: only candidates that fail the test leave the heap.
         */
        int[] widestGap() {
            while (!heap.isEmpty()) {
                Gap g = heap.peek();
                if (current(g)) return new int[] {g.left(), g.right()};
                heap.poll();
            }
            return new int[0];
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        GapBook a = new GapBook();
        a.occupy(2); a.occupy(10); a.occupy(6);
        if (!Arrays.equals(a.widestGap(), new int[] {2, 6})) throw new AssertionError("e1 first");
        a.vacate(6);
        if (!Arrays.equals(a.widestGap(), new int[] {2, 10})) throw new AssertionError("e1 second");
        GapBook b = new GapBook();
        b.occupy(1);
        if (b.widestGap().length != 0) throw new AssertionError("e2 empty");
        b.occupy(9); b.occupy(4);
        if (!Arrays.equals(b.widestGap(), new int[] {4, 9})) throw new AssertionError("e2 middle");
        b.vacate(9);
        if (!Arrays.equals(b.widestGap(), new int[] {1, 4})) throw new AssertionError("e2 vacate");
        // Random calls checked against a scan of the sorted occupied positions.
        Random rnd = new Random(9203);
        for (int round = 0; round < 400; round++) {
            GapBook s = new GapBook();
            boolean[] occ = new boolean[15];
            for (int op = 0; op < 100; op++) {
                int p = rnd.nextInt(15);
                if (occ[p]) { occ[p] = false; s.vacate(p); } else { occ[p] = true; s.occupy(p); }
                int[] want = new int[0];
                int prev = -1;
                for (int x = 0; x < 15; x++) {
                    if (!occ[x]) continue;
                    if (prev != -1 && (want.length == 0 || x - prev > want[1] - want[0])) want = new int[] {prev, x};
                    prev = x;
                }
                if (!Arrays.equals(s.widestGap(), want) || !Arrays.equals(s.widestGap(), want)) throw new AssertionError("widestGap");
            }
        }
    }
}
```

#### Solution: [Recognize] Booking Hall With Cancellations (LeetCode 2286)
<!-- id: ci40-hall-cancel -->

**Approach.** Each row stores its free seat count, and the booked seats are the leftmost ones. An iterative segment tree over the rows keeps the maximum and the sum of the free counts, padded with empty rows up to a power of two.

A gather call descends from the root to the leftmost row whose free count is at least `k`. It returns an empty array when that row is past `maxRow`. Otherwise the first seat is `m` minus the free count, and a point update lowers the count by `k`. A scatter call checks the sum of rows 0 to `maxRow` against `k`. It then repeats the same descent with a demand of 1 to find the lowest row that still has a free seat, takes as many seats as that row offers, and updates it. A cancel call checks that the row holds at least `k` bookings, raises the free count and updates the tree.

The descent replaces the forward-moving pointer of the version without cancellations, because a cancel call can reopen a row below the pointer.

The invariant is that each tree node holds the maximum and the sum of the free counts of its rows after every call.

**Complexity.**

- **Time** is O(log n) per gather and cancel call, and O((rows touched + 1) log n) per scatter call.
- **Space** is O(n), because the tree holds about 2n numbers.

```java run
import java.util.*;

public final class HallCancelSolution {
    static final class CancelHall {
        private final int n, size;
        private final long m;
        private final long[] free, mx, sm;

        /** Builds the tree with every row empty; O(n) time, O(n) space; invariant: each node summarizes its rows. */
        CancelHall(int n, int m) {
            this.n = n; this.m = m;
            int sz = 1;
            while (sz < n) sz <<= 1;
            size = sz;
            free = new long[n];
            mx = new long[2 * sz]; sm = new long[2 * sz];
            for (int r = 0; r < n; r++) { free[r] = m; mx[sz + r] = sm[sz + r] = m; }
            for (int i = sz - 1; i >= 1; i--) pull(i);
        }

        private void pull(int i) {
            mx[i] = Math.max(mx[2 * i], mx[2 * i + 1]);
            sm[i] = sm[2 * i] + sm[2 * i + 1];
        }

        // Writes one row and repairs its ancestors in O(log n).
        private void setRow(int r, long value) {
            free[r] = value;
            int i = size + r;
            mx[i] = sm[i] = value;
            for (i >>= 1; i >= 1; i >>= 1) pull(i);
        }

        // Sums rows [0, hi] with a bottom-up walk in O(log n).
        private long prefix(int hi) {
            long total = 0;
            for (int l = size, r = size + hi + 1; l < r; l >>= 1, r >>= 1) {
                if ((l & 1) == 1) total += sm[l++];
                if ((r & 1) == 1) total += sm[--r];
            }
            return total;
        }

        // Returns the leftmost row with at least k free seats, or -1, in O(log n).
        private int leftmost(long k) {
            if (mx[1] < k) return -1;
            int i = 1;
            while (i < size) i = mx[2 * i] >= k ? 2 * i : 2 * i + 1;
            return i - size;
        }

        /** Books k seats in the first row with room; O(log n) time, O(1) space; invariant: the row is the leftmost with k free. */
        int[] gather(int k, int maxRow) {
            int r = leftmost(k);
            if (r == -1 || r > maxRow) return new int[0];
            int seat = (int) (m - free[r]);
            setRow(r, free[r] - k);
            return new int[] {r, seat};
        }

        /** Books k seats over the lowest rows or changes nothing; O((rows + 1) log n) time, O(1) space; invariant: the sum check precedes every write. */
        boolean scatter(int k, int maxRow) {
            if (prefix(maxRow) < k) return false;
            long need = k;
            while (need > 0) {
                int r = leftmost(1);
                long take = Math.min(free[r], need);
                setRow(r, free[r] - take);
                need -= take;
            }
            return true;
        }

        /** Frees the last k bookings of a row; O(log n) time, O(1) space; invariant: free stays between 0 and m. */
        boolean cancel(int row, int k) {
            if (m - free[row] < k) return false;
            setRow(row, free[row] + k);
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        CancelHall a = new CancelHall(3, 4);
        int[] g;
        if (!a.scatter(5, 2) || !a.cancel(0, 2) || (g = a.gather(2, 0)).length != 2 || g[0] != 0 || g[1] != 2) throw new AssertionError("e1");
        CancelHall b = new CancelHall(3, 4);
        if (!b.scatter(5, 2) || b.cancel(2, 1) || (g = b.gather(4, 2)).length != 2 || g[0] != 2 || g[1] != 0) throw new AssertionError("e2");
        // Random calls checked against a plain array of free counts.
        Random rnd = new Random(9204);
        for (int round = 0; round < 400; round++) {
            int n = 1 + rnd.nextInt(6), m = 1 + rnd.nextInt(6);
            CancelHall s = new CancelHall(n, m);
            int[] free = new int[n];
            Arrays.fill(free, m);
            for (int op = 0; op < 60; op++) {
                int t = rnd.nextInt(3), k = 1 + rnd.nextInt(m), maxRow = rnd.nextInt(n);
                if (t == 0) {
                    int row = -1;
                    for (int r = 0; r < n && row == -1; r++) if (free[r] >= k) row = r;
                    int[] got = s.gather(k, maxRow);
                    if (row == -1 || row > maxRow) { if (got.length != 0) throw new AssertionError("gather none"); }
                    else { if (got.length != 2 || got[0] != row || got[1] != m - free[row]) throw new AssertionError("gather row"); free[row] -= k; }
                } else if (t == 1) {
                    int total = 0;
                    for (int r = 0; r <= maxRow; r++) total += free[r];
                    boolean want = total >= k;
                    if (want) { int need = k; for (int r = 0; need > 0; r++) { int take = Math.min(free[r], need); free[r] -= take; need -= take; } }
                    if (s.scatter(k, maxRow) != want) throw new AssertionError("scatter");
                } else {
                    int row = rnd.nextInt(n);
                    boolean want = m - free[row] >= k;
                    if (want) free[row] += k;
                    if (s.cancel(row, k) != want) throw new AssertionError("cancel");
                }
            }
        }
    }
}
```
