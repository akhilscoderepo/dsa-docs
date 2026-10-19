<!-- solutions-for: 03-resource-allocation -->
### Solutions For Resource Allocation

#### Solution: [Build] Seat Reservation Manager (LeetCode 1845)
<!-- id: ci40-seat-manager -->

**Approach.** A tree set holds every free seat, and the constructor inserts the numbers 1 to `n`. A reserve call removes and returns the first element of the set, which is the smallest free seat. An unreserve call inserts the seat number back.

The invariant is that the set holds exactly the free seats. A reserve call removes the seat before it returns it, and the problem guarantees that an unreserve call names a held seat, so no seat enters the set twice.

**Complexity.**

- **Time** is O(log n) for reserve and unreserve, since a tree set removes its first element and inserts in logarithmic time. The constructor costs O(n log n).
- **Space** is O(n), because the set holds up to n seats.

```java run
import java.util.*;

public final class SeatManagerSolution {
    static final class SeatManager {
        private final TreeSet<Integer> free = new TreeSet<>();      // every seat that no customer holds

        /**
         * Starts with every seat free.
         * Time: O(n log n), because each insertion costs O(log n).
         * Space: O(n).
         * Invariant: free holds 1 through n.
         */
        SeatManager(int n) {
            for (int s = 1; s <= n; s++) free.add(s);
        }

        /** Holds and returns the smallest free seat; O(log n) time, O(1) space; invariant: the seat leaves free before it is returned. */
        int reserve() {
            return free.pollFirst();
        }

        /** Frees a held seat; O(log n) time, O(1) space; invariant: free gains only seats that were held. */
        void unreserve(int seat) {
            free.add(seat);
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        SeatManager a = new SeatManager(3);
        if (a.reserve() != 1 || a.reserve() != 2) throw new AssertionError("e1 first two");
        a.unreserve(1);
        if (a.reserve() != 1) throw new AssertionError("e1 reuse");
        SeatManager b = new SeatManager(2);
        if (b.reserve() != 1 || b.reserve() != 2) throw new AssertionError("e2");
        // Random valid calls checked against a boolean array and a scan.
        Random rnd = new Random(1845);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(12);
            SeatManager s = new SeatManager(n);
            boolean[] held = new boolean[n + 1];
            int heldCount = 0;
            for (int op = 0; op < 80; op++) {
                boolean canReserve = heldCount < n;
                if (canReserve && (heldCount == 0 || rnd.nextBoolean())) {
                    int want = 1;
                    while (held[want]) want++;
                    held[want] = true; heldCount++;
                    if (s.reserve() != want) throw new AssertionError("reserve");
                } else {
                    int seat = 1 + rnd.nextInt(n);
                    while (!held[seat]) seat = seat % n + 1;
                    held[seat] = false; heldCount--;
                    s.unreserve(seat);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Exam Room (LeetCode 855)
<!-- id: ci40-exam-room -->

**Approach.** A tree set holds the occupied seats in order. The first student takes seat 0. For later students, the class lists every candidate seat. The candidates are seat 0 when it is free, the middle of each gap between two neighbors, and seat `n - 1` when it is free.

The distance of seat 0 is the first occupied seat. The distance of the last seat is `n - 1` minus the last occupied seat. A gap between neighbors `a` and `b` offers the seat `a + (b - a) / 2` at distance `(b - a) / 2`. A distance of 0 offers nothing. The scan visits candidates from the lowest seat upward and replaces the best only for a strictly larger distance, so ties keep the smallest seat. A leave call removes the seat from the set.

The invariant is that the set holds exactly the occupied seats, and each candidate is a free seat whose nearest occupied seat is as far away as the candidate's distance.

**Complexity.**

- **Time** is O(k) for a seat call and O(log k) for a leave call, with k occupied seats. The seat call visits each neighboring pair once.
- **Space** is O(k), because the set holds the occupied seats.

```java run
import java.util.*;

public final class ExamRoomSolution {
    static final class ExamRoom {
        private final int n;
        private final TreeSet<Integer> occupied = new TreeSet<>();

        ExamRoom(int n) { this.n = n; }

        /**
         * Seats a student at the best free seat.
         * Time: O(k) for k occupied seats, because the scan visits each gap once.
         * Space: O(1) extra.
         * Invariant: bestDist is the largest distance among the candidates visited so far.
         */
        int seat() {
            if (occupied.isEmpty()) { occupied.add(0); return 0; }
            int bestSeat = 0, bestDist = occupied.first();              // seat 0, distance to the first student
            int prev = occupied.first();
            // Visit each pair of neighbors in increasing seat order.
            for (int cur : occupied.tailSet(prev, false)) {
                int d = (cur - prev) / 2;
                // Strictly greater keeps the smaller seat on ties.
                if (d > bestDist) { bestDist = d; bestSeat = prev + d; }
                prev = cur;
            }
            // The last seat competes with the right end of the row.
            if (n - 1 - prev > bestDist) bestSeat = n - 1;
            occupied.add(bestSeat);
            return bestSeat;
        }

        /** Frees seat p; O(log k) time, O(1) space; invariant: occupied loses exactly p. */
        void leave(int p) { occupied.remove(p); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        ExamRoom r = new ExamRoom(10);
        int[] first = {r.seat(), r.seat(), r.seat(), r.seat()};
        if (first[0] != 0 || first[1] != 9 || first[2] != 4 || first[3] != 2) throw new AssertionError("e1");
        r.leave(4);
        if (r.seat() != 5) throw new AssertionError("e2");
        // Random calls checked against a scan of every free seat.
        Random rnd = new Random(855);
        for (int round = 0; round < 300; round++) {
            int n = 2 + rnd.nextInt(14);
            ExamRoom s = new ExamRoom(n);
            boolean[] occ = new boolean[n];
            int count = 0;
            for (int op = 0; op < 60; op++) {
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

#### Solution: [Boundary] Duplicate Release (Author exercise)
<!-- id: ci40-duplicate-release -->

**Approach.** The free set is a tree set of seat numbers, and the taken record is a boolean array. A reserve call polls the first free seat, marks it taken and returns it, or returns -1 when the set is empty. A release call returns `false` when the number is outside 1 to `n` or when the taken flag is false. Otherwise it clears the flag, inserts the seat into the free set and returns `true`. The count of free seats is the size of the set.

The invariant is that a seat is in the free set exactly when its taken flag is false. The release check reads the flag before it touches the set, so a rejected call changes neither structure.

**Complexity.**

- **Time** is O(log n) per call. The tree set polls and inserts in logarithmic time, and the flag check adds O(1).
- **Space** is O(n), because the set and the array each hold up to n entries.

```java run
import java.util.*;

public final class DuplicateReleaseSolution {
    static final class SeatBook {
        private final TreeSet<Integer> free = new TreeSet<>();
        private final boolean[] taken;                              // taken[s] is true while s is held

        /** Starts with every seat free; O(n log n) time, O(n) space; invariant: free and taken partition 1..n. */
        SeatBook(int n) {
            taken = new boolean[n + 1];
            for (int s = 1; s <= n; s++) free.add(s);
        }

        /** Holds the smallest free seat or returns -1; O(log n) time, O(1) space; invariant: the seat moves from free to taken. */
        int reserve() {
            if (free.isEmpty()) return -1;
            int s = free.pollFirst();
            taken[s] = true;
            return s;
        }

        /**
         * Frees a held seat and rejects everything else.
         * Time: O(log n).
         * Space: O(1).
         * Invariant: the check reads taken first, so a rejected call changes nothing.
         */
        boolean release(int seat) {
            // Out-of-range numbers and free seats are rejected before any write.
            if (seat < 1 || seat >= taken.length || !taken[seat]) return false;
            taken[seat] = false;
            free.add(seat);
            return true;
        }

        /** Returns the number of free seats; O(1) time and space; invariant: it equals the size of free. */
        int available() { return free.size(); }
    }

    public static void main(String[] args) {
        // Example 1: the second release of seat 2 is rejected, and seat 2 comes back once.
        SeatBook a = new SeatBook(2);
        if (a.reserve() != 1 || a.reserve() != 2 || !a.release(2) || a.release(2) || a.reserve() != 2) throw new AssertionError("e1");
        // Example 2: out-of-range releases change nothing.
        SeatBook b = new SeatBook(3);
        if (b.release(0) || b.release(3) || b.available() != 3) throw new AssertionError("e2");
        if (b.release(Integer.MIN_VALUE) || b.release(Integer.MAX_VALUE)) throw new AssertionError("extreme ints");
        // Random calls including invalid releases, checked against a boolean array.
        Random rnd = new Random(41);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(8);
            SeatBook s = new SeatBook(n);
            boolean[] held = new boolean[n + 2];
            for (int op = 0; op < 80; op++) {
                if (rnd.nextBoolean()) {
                    int want = -1;
                    for (int i = 1; i <= n && want == -1; i++) if (!held[i]) want = i;
                    if (want != -1) held[want] = true;
                    if (s.reserve() != want) throw new AssertionError("reserve");
                } else {
                    int seat = rnd.nextInt(n + 3) - 1;
                    boolean want = seat >= 1 && seat <= n && held[seat];
                    if (want) held[seat] = false;
                    if (s.release(seat) != want) throw new AssertionError("release");
                }
                int free = 0;
                for (int i = 1; i <= n; i++) if (!held[i]) free++;
                if (s.available() != free) throw new AssertionError("available");
            }
        }
    }
}
```

#### Solution: [Recognize] Booking Concert Tickets In Groups (LeetCode 2286)
<!-- id: ci40-concert-tickets -->

**Approach.** Row `r` has `free[r]` free seats, and its held seats are the leftmost ones. A segment tree over the rows stores, for each node, the maximum and the sum of `free` over its rows.

A gather call descends from the root toward the leftmost row whose free count is at least `k`. At each node it goes left when the left child's maximum is at least `k`, and right otherwise. If that row is beyond `maxRow`, or no row qualifies, the call returns an empty array. Otherwise the first seat is `m - free[r]`, and the call lowers `free[r]` by `k` with a point update. A scatter call sums the free seats of rows 0 to `maxRow`. It returns `false` when the sum is below `k`. Otherwise it takes seats from the first non-full row, then the next, until `k` seats are placed. The pointer to the first non-full row only moves forward, because rows only fill in this exercise.

The invariant is that every node holds the maximum and sum of its rows' `free` values, and each point update repairs the nodes on the path to the root.

**Complexity.**

- **Time** is O(log n) per gather call and O((rows touched + 1) log n) per scatter call. Each touched row needs one point update, and scatter calls touch at most n rows in total.
- **Space** is O(n), because the tree has about 4n nodes.

```java run
import java.util.*;

public final class ConcertTicketsSolution {
    static final class Hall {
        private final int n;
        private final long m;
        private final long[] free;                               // free[r] = free seats in row r
        private final long[] mx, sm;                             // segment tree: maximum and sum of free
        private int firstOpen = 0;                               // first row that may still have free seats

        /**
         * Builds the tree with every row empty.
         * Time: O(n).
         * Space: O(n).
         * Invariant: each node covers a row range and holds the max and sum of free there.
         */
        Hall(int n, int m) {
            this.n = n; this.m = m;
            free = new long[n];
            Arrays.fill(free, m);
            mx = new long[4 * n]; sm = new long[4 * n];
            build(1, 0, n - 1);
        }

        private void build(int node, int l, int r) {
            if (l == r) { mx[node] = sm[node] = m; return; }
            int mid = (l + r) / 2;
            build(2 * node, l, mid); build(2 * node + 1, mid + 1, r);
            pull(node);
        }

        // Recomputes one node from its two children in O(1).
        private void pull(int node) {
            mx[node] = Math.max(mx[2 * node], mx[2 * node + 1]);
            sm[node] = sm[2 * node] + sm[2 * node + 1];
        }

        private void set(int node, int l, int r, int pos, long v) {
            if (l == r) { mx[node] = sm[node] = v; return; }
            int mid = (l + r) / 2;
            if (pos <= mid) set(2 * node, l, mid, pos, v); else set(2 * node + 1, mid + 1, r, pos, v);
            pull(node);
        }

        // Sums free over rows [0, hi] in O(log n).
        private long sum(int node, int l, int r, int hi) {
            if (l > hi) return 0;
            if (r <= hi) return sm[node];
            int mid = (l + r) / 2;
            return sum(2 * node, l, mid, hi) + sum(2 * node + 1, mid + 1, r, hi);
        }

        /** Returns {row, firstSeat} or an empty array; O(log n) time, O(1) space; invariant: the row is the leftmost with at least k free. */
        int[] gather(int k, int maxRow) {
            if (mx[1] < k) return new int[0];
            // Descend to the leftmost row whose free count is at least k.
            int node = 1, l = 0, r = n - 1;
            while (l < r) {
                int mid = (l + r) / 2;
                if (mx[2 * node] >= k) { node = 2 * node; r = mid; } else { node = 2 * node + 1; l = mid + 1; }
            }
            if (l > maxRow) return new int[0];
            int seat = (int) (m - free[l]);
            free[l] -= k;
            set(1, 0, n - 1, l, free[l]);
            return new int[] {l, seat};
        }

        /** Holds k seats in the lowest rows up to maxRow or changes nothing; O((rows + 1) log n) time, O(1) space; invariant: the prefix sum check precedes every write. */
        boolean scatter(int k, int maxRow) {
            if (sum(1, 0, n - 1, maxRow) < k) return false;
            long need = k;
            while (need > 0) {
                // Skip rows that are already full; the pointer never moves backward.
                while (free[firstOpen] == 0) firstOpen++;
                long take = Math.min(free[firstOpen], need);
                free[firstOpen] -= take;
                set(1, 0, n - 1, firstOpen, free[firstOpen]);
                need -= take;
            }
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Hall h = new Hall(2, 5);
        int[] g = h.gather(4, 0);
        if (g.length != 2 || g[0] != 0 || g[1] != 0 || h.gather(2, 0).length != 0) throw new AssertionError("e1");
        Hall h2 = new Hall(2, 5);
        int[] g2;
        if (!h2.scatter(5, 1) || (g2 = h2.gather(5, 1)).length != 2 || g2[0] != 1 || g2[1] != 0) throw new AssertionError("e2");
        // Random calls checked against a plain array of free counts.
        Random rnd = new Random(2286);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(6), m = 1 + rnd.nextInt(6);
            Hall s = new Hall(n, m);
            int[] free = new int[n];
            Arrays.fill(free, m);
            for (int op = 0; op < 40; op++) {
                int k = 1 + rnd.nextInt(m), maxRow = rnd.nextInt(n);
                if (rnd.nextBoolean()) {
                    int row = -1;
                    for (int r = 0; r < n && row == -1; r++) if (free[r] >= k) row = r;
                    int[] got = s.gather(k, maxRow);
                    if (row == -1 || row > maxRow) { if (got.length != 0) throw new AssertionError("gather none"); }
                    else {
                        if (got.length != 2 || got[0] != row || got[1] != m - free[row]) throw new AssertionError("gather row");
                        free[row] -= k;
                    }
                } else {
                    int total = 0;
                    for (int r = 0; r <= maxRow; r++) total += free[r];
                    boolean want = total >= k;
                    if (want) { int need = k; for (int r = 0; r <= maxRow && need > 0; r++) { int t = Math.min(free[r], need); free[r] -= t; need -= t; } }
                    if (s.scatter(k, maxRow) != want) throw new AssertionError("scatter");
                }
            }
        }
    }
}
```
