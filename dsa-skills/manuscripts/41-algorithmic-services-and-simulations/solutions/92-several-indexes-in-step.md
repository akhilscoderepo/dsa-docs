<!-- solutions-for: 92-several-indexes-in-step -->
### Solutions For Keeping Indexes In Step

#### Solution: [Build] Tic-Tac-Toe With Undo (LeetCode 348)
<!-- id: sv-ix-board-undo -->

**Approach.** The grid of owners is the authoritative state. The derived indexes are four counter families per player: one count per row, one per column, one for the main diagonal and one for the anti-diagonal. A single method, `apply`, takes a cell, a player and a step of +1 or -1. It adds the step to every counter that the cell belongs to, and it writes the grid cell. A move validates first: the cell must be empty and no winner may exist. It then logs the cell, calls `apply` with +1 and checks whether a counter of that player reached `n`.

An undo pops the log and calls `apply` with -1 for the logged cell and player. This restores the grid and every counter in one call, with no special code. A winning move is always the latest accepted move, because later moves are rejected. So an undo that pops the winning move clears the winner, and any other undo leaves the winner at 0.

The invariant says each counter equals the number of marks of its player on its line, and the log holds the accepted moves in order.

**Complexity.**

- **Time** is O(1) per call, because a move touches at most four counters and an undo reverses the same four.
- **Space** is O(n + m), where m is the number of accepted moves held in the log, plus 2 * (2n + 2) counters.

```java run
import java.util.*;

public final class BoardUndoSolution {
    static final class UndoBoard {
        private final int n;
        private final int[][] owner;
        private final int[][] rows, cols;
        private final int[] diag = new int[3], anti = new int[3];
        private final Deque<int[]> log = new ArrayDeque<>();
        private int winner;

        UndoBoard(int n) {
            this.n = n;
            owner = new int[n][n];
            rows = new int[3][n];
            cols = new int[3][n];
        }

        /**
         * The only method that writes the grid and the counters.
         * Time: O(1).
         * Space: O(1) extra.
         * Invariant: each counter equals the marks of its player on its line.
         */
        private void apply(int r, int c, int p, int step) {
            owner[r][c] = step > 0 ? p : 0;
            rows[p][r] += step;
            cols[p][c] += step;
            // The diagonals change only for cells that lie on them.
            if (r == c) diag[p] += step;
            if (r + c == n - 1) anti[p] += step;
        }

        /** Returns 0, the winning player or -1 for a rejected call; O(1) time and space. */
        int move(int r, int c, int p) {
            // Both checks run before the first write.
            if (winner != 0 || owner[r][c] != 0) return -1;
            apply(r, c, p, 1);
            log.push(new int[] {r, c, p});
            boolean won = rows[p][r] == n || cols[p][c] == n
                    || (r == c && diag[p] == n) || (r + c == n - 1 && anti[p] == n);
            if (won) winner = p;
            return won ? p : 0;
        }

        /** Takes back the latest accepted move; O(1) time and space; invariant: the counters return to the earlier state. */
        boolean undo() {
            if (log.isEmpty()) return false;
            int[] m = log.pop();
            apply(m[0], m[1], m[2], -1);
            // A win can only come from the latest move, so any undo clears it.
            winner = 0;
            return true;
        }

        int winner() { return winner; }
    }

    // Brute-force reference: rescans the whole grid after every call.
    static int scanWinner(int[][] g, int n) {
        for (int p = 1; p <= 2; p++) {
            for (int i = 0; i < n; i++) {
                boolean row = true, col = true;
                for (int j = 0; j < n; j++) { row &= g[i][j] == p; col &= g[j][i] == p; }
                if (row || col) return p;
            }
            boolean d = true, a = true;
            for (int i = 0; i < n; i++) { d &= g[i][i] == p; a &= g[i][n - 1 - i] == p; }
            if (d || a) return p;
        }
        return 0;
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        UndoBoard a = new UndoBoard(3);
        int[] got = {a.move(0, 0, 1), a.move(1, 1, 1), a.move(0, 0, 2), a.move(2, 2, 1), a.move(0, 1, 2)};
        if (!Arrays.equals(got, new int[] {0, 0, -1, 1, -1})) throw new AssertionError("e1 moves");
        if (!a.undo() || a.move(0, 1, 2) != 0) throw new AssertionError("e1 undo");
        // Example 2 from the problem text.
        UndoBoard b = new UndoBoard(2);
        if (b.undo() || b.move(0, 0, 2) != 0 || b.move(0, 1, 2) != 2 || b.winner() != 2) throw new AssertionError("e2 win");
        if (!b.undo() || b.winner() != 0) throw new AssertionError("e2 undo");
        // Random calls checked against a full rescan of the grid.
        Random rnd = new Random(9201);
        for (int round = 0; round < 400; round++) {
            int n = 1 + rnd.nextInt(4);
            UndoBoard s = new UndoBoard(n);
            int[][] g = new int[n][n];
            Deque<int[]> hist = new ArrayDeque<>();
            for (int op = 0; op < 60; op++) {
                if (rnd.nextInt(4) == 0) {
                    boolean want = !hist.isEmpty();
                    if (want) { int[] m = hist.pop(); g[m[0]][m[1]] = 0; }
                    if (s.undo() != want) throw new AssertionError("undo");
                } else {
                    int r = rnd.nextInt(n), c = rnd.nextInt(n), p = 1 + rnd.nextInt(2);
                    int want;
                    if (scanWinner(g, n) != 0 || g[r][c] != 0) want = -1;
                    else { g[r][c] = p; hist.push(new int[] {r, c, p}); want = scanWinner(g, n); }
                    if (s.move(r, c, p) != want) throw new AssertionError("move");
                }
                if (s.winner() != scanWinner(g, n)) throw new AssertionError("winner");
            }
        }
    }
}
```

#### Solution: [Vary] Underground System With Cancel (LeetCode 1396)
<!-- id: sv-ix-underground-slow -->

**Approach.** Two maps hold the authoritative state: open trips by card, and route statistics by route string. A route statistic is an immutable record of route, duration sum and trip count. The derived index is a tree set of those records. It orders by larger mean first and then by smaller route string. The comparison of two means uses cross multiplication of sums and counts, so no rounding enters the order.

A check-in validates that the card has no open trip and stores the station and time. A check-out validates that a trip is open and that the time is not earlier than the check-in time. It then calls the single writer `record`, which removes the old statistic from the map and the set, builds a new statistic with the added duration and inserts it into both. A cancel removes the open trip and touches nothing else, because an open trip is in no sorted index.

The invariant says that every route in the map has exactly one entry in the set with equal sum and count. The largest sum is 10^5 * 10^6 and the largest count is 10^5, so each product stays below 10^16 and fits in a `long`.

**Complexity.**

- **Time** is O(log R) for a check-out, where R is the number of routes, and O(1) for the other calls and for `slowest`, which reads the first set entry.
- **Space** is O(C + R), where C is the number of open trips, because routes keep one record and one set entry.

```java run
import java.util.*;

public final class UndergroundSlowSolution {
    static final class Metro {
        private record Open(String station, int time) {}
        private record Stat(String route, long sum, long count) {}
        // Larger mean first; the route string breaks ties.
        private static final Comparator<Stat> ORDER = (x, y) -> {
            int c = Long.compare(y.sum() * x.count(), x.sum() * y.count());
            return c != 0 ? c : x.route().compareTo(y.route());
        };
        private final Map<Integer, Open> open = new HashMap<>();
        private final Map<String, Stat> stats = new HashMap<>();
        private final TreeSet<Stat> byMean = new TreeSet<>(ORDER);

        boolean checkIn(int card, String station, int t) {
            // A card holds at most one open trip.
            if (open.containsKey(card)) return false;
            open.put(card, new Open(station, t));
            return true;
        }

        /**
         * The only method that writes the statistics and their sorted set.
         * Time: O(log R).
         * Space: O(1) extra.
         * Invariant: the old entry leaves the set before the new entry enters.
         */
        private void record(String route, long duration) {
            Stat old = stats.get(route);
            if (old != null) byMean.remove(old);
            Stat next = old == null ? new Stat(route, duration, 1) : new Stat(route, old.sum() + duration, old.count() + 1);
            stats.put(route, next);
            byMean.add(next);
        }

        boolean checkOut(int card, String station, int t) {
            Open o = open.get(card);
            // Both checks run before the first write.
            if (o == null || t < o.time()) return false;
            open.remove(card);
            record(o.station() + ">" + station, t - o.time());
            return true;
        }

        boolean cancel(int card) { return open.remove(card) != null; }

        /** Returns the mean duration of a route or -1.0; O(1) time and space. */
        double average(String start, String end) {
            Stat s = stats.get(start + ">" + end);
            return s == null ? -1.0 : (double) s.sum() / s.count();
        }

        /** Returns the route with the largest mean, or the empty string; O(1) time and space. */
        String slowest() { return byMean.isEmpty() ? "" : byMean.first().route(); }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Metro a = new Metro();
        boolean ok = a.checkIn(7, "a", 3) && !a.checkIn(7, "b", 4) && a.checkOut(7, "c", 13)
                && a.checkIn(8, "a", 0) && a.checkOut(8, "b", 5);
        if (!ok || !a.slowest().equals("a>c") || a.average("a", "b") != 5.0) throw new AssertionError("e1");
        // Example 2 from the problem text.
        Metro b = new Metro();
        if (!b.checkIn(1, "x", 10) || b.checkOut(1, "y", 9) || !b.cancel(1) || b.cancel(1)) throw new AssertionError("e2 calls");
        if (!b.slowest().isEmpty() || b.average("x", "y") != -1.0) throw new AssertionError("e2 reports");
        // Random calls checked against a rescan of all recorded trips.
        Random rnd = new Random(9202);
        String[] st = {"a", "b", "c"};
        for (int round = 0; round < 400; round++) {
            Metro s = new Metro();
            Map<Integer, Object[]> open = new HashMap<>();
            List<Object[]> done = new ArrayList<>();
            for (int op = 0; op < 60; op++) {
                int card = rnd.nextInt(4), t = rnd.nextInt(20), k = rnd.nextInt(4);
                String station = st[rnd.nextInt(3)];
                if (k == 0) {
                    boolean want = !open.containsKey(card);
                    if (want) open.put(card, new Object[] {station, t});
                    if (s.checkIn(card, station, t) != want) throw new AssertionError("checkIn");
                } else if (k == 1) {
                    Object[] o = open.get(card);
                    boolean want = o != null && t >= (int) o[1];
                    if (want) { open.remove(card); done.add(new Object[] {o[0] + ">" + station, t - (int) o[1]}); }
                    if (s.checkOut(card, station, t) != want) throw new AssertionError("checkOut");
                } else if (k == 2) {
                    if (s.cancel(card) != (open.remove(card) != null)) throw new AssertionError("cancel");
                } else {
                    Map<String, long[]> agg = new TreeMap<>();
                    for (Object[] d : done) { long[] v = agg.computeIfAbsent((String) d[0], x -> new long[2]); v[0] += (int) d[1]; v[1]++; }
                    String best = "";
                    for (Map.Entry<String, long[]> e : agg.entrySet()) {
                        if (best.isEmpty()) { best = e.getKey(); continue; }
                        long[] bv = agg.get(best), ev = e.getValue();
                        // Strictly larger mean wins; the sorted map visits smaller route strings first.
                        if (ev[0] * bv[1] > bv[0] * ev[1]) best = e.getKey();
                    }
                    if (!s.slowest().equals(best)) throw new AssertionError("slowest");
                    String route = st[rnd.nextInt(3)] + ">" + st[rnd.nextInt(3)];
                    long[] v = agg.get(route);
                    double want = v == null ? -1.0 : (double) v[0] / v[1];
                    if (s.average(route.substring(0, 1), route.substring(2)) != want) throw new AssertionError("average");
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Twitter With Mute And Delete (LeetCode 355)
<!-- id: sv-ix-feed-sources -->

**Approach.** The authoritative state is one tree map per author from post time to tweet id, a map from tweet id to its author and time, a follow set per user and a mute set per user. A delete removes the tweet from its author's tree map through the tweet record, so a deleted tweet exists in no list. The single writer for tweets is `remove`, and `post` and `delete` are the only calls that write the author lists.

A feed call collects the visible authors first: the user, plus every followed author who is not muted. Only these authors enter the merge, so a muted author never competes for a place in the result. The merge puts one descending iterator per visible author into a priority queue ordered by the newest unread post time. It then pops until `k` ids are collected or the queue empties, and pushes the next entry of the same author after each pop. Every popped tweet is visible by construction, so the cut at `k` counts only visible tweets. The source count is the size of a set of authors seen in the output.

The invariant says the tweet lists hold exactly the undeleted tweets, and visibility depends only on the follow and mute sets read at the time of the call.

**Complexity.**

- **Time** is O((F + k) log F) per feed call, where F is the number of visible authors. Building the queue costs F log F and each of the k pops costs log F. Other calls cost O(log n).
- **Space** is O(T + U), where T is the number of tweets and U the number of follow and mute pairs. A feed call adds O(F + k).

```java run
import java.util.*;

public final class FeedSourcesSolution {
    record Feed(List<Integer> ids, int sources) {}

    static final class FeedDesk {
        private int clock;
        private final Map<Integer, TreeMap<Integer, Integer>> byAuthor = new HashMap<>();
        private final Map<Integer, int[]> tweetInfo = new HashMap<>();
        private final Map<Integer, Set<Integer>> follows = new HashMap<>();
        private final Map<Integer, Set<Integer>> muted = new HashMap<>();

        void post(int user, int tweet) {
            int time = clock++;
            byAuthor.computeIfAbsent(user, k -> new TreeMap<>()).put(time, tweet);
            tweetInfo.put(tweet, new int[] {user, time});
        }

        void follow(int a, int b) { if (a != b) follows.computeIfAbsent(a, k -> new HashSet<>()).add(b); }

        void unfollow(int a, int b) { if (follows.containsKey(a)) follows.get(a).remove(b); }

        void mute(int v, int author) { if (v != author) muted.computeIfAbsent(v, k -> new HashSet<>()).add(author); }

        void unmute(int v, int author) { if (muted.containsKey(v)) muted.get(v).remove(author); }

        /** Removes a tweet from its author's list; O(log n) time, O(1) space; invariant: no deleted tweet stays in a list. */
        boolean delete(int tweet) {
            int[] info = tweetInfo.remove(tweet);
            if (info == null) return false;
            byAuthor.get(info[0]).remove(info[1]);
            return true;
        }

        /**
         * Returns the k newest visible tweets and the number of authors among them.
         * Time: O((F + k) log F).
         * Space: O(F + k).
         * Invariant: only visible authors enter the queue, so the cut at k counts visible tweets.
         */
        Feed feed(int user, int k) {
            List<Integer> authors = new ArrayList<>();
            authors.add(user);
            for (int f : follows.getOrDefault(user, Set.of())) {
                // Muted authors leave before the merge starts.
                if (!muted.getOrDefault(user, Set.of()).contains(f)) authors.add(f);
            }
            record Cursor(int author, Iterator<Map.Entry<Integer, Integer>> it, Map.Entry<Integer, Integer> cur) {}
            PriorityQueue<Cursor> pq = new PriorityQueue<>((x, y) -> Integer.compare(y.cur().getKey(), x.cur().getKey()));
            for (int au : authors) {
                TreeMap<Integer, Integer> m = byAuthor.get(au);
                if (m == null || m.isEmpty()) continue;
                Iterator<Map.Entry<Integer, Integer>> it = m.descendingMap().entrySet().iterator();
                pq.add(new Cursor(au, it, it.next()));
            }
            List<Integer> ids = new ArrayList<>();
            Set<Integer> seen = new HashSet<>();
            while (ids.size() < k && !pq.isEmpty()) {
                Cursor c = pq.poll();
                ids.add(c.cur().getValue());
                seen.add(c.author());
                if (c.it().hasNext()) pq.add(new Cursor(c.author(), c.it(), c.it().next()));
            }
            return new Feed(ids, seen.size());
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        FeedDesk a = new FeedDesk();
        a.post(1, 10); a.post(2, 20); a.post(2, 21); a.post(3, 30);
        a.follow(1, 2); a.follow(1, 3);
        if (!a.feed(1, 3).equals(new Feed(List.of(30, 21, 20), 2))) throw new AssertionError("e1 first");
        a.mute(1, 3);
        if (!a.feed(1, 3).equals(new Feed(List.of(21, 20, 10), 2))) throw new AssertionError("e1 mute");
        if (!a.delete(21) || !a.feed(1, 3).equals(new Feed(List.of(20, 10), 2))) throw new AssertionError("e1 delete");
        // Example 2 from the problem text.
        FeedDesk b = new FeedDesk();
        b.post(5, 50); b.follow(4, 5); b.unfollow(4, 5);
        if (!b.feed(4, 2).equals(new Feed(List.of(), 0))) throw new AssertionError("e2 empty");
        b.follow(4, 4); b.post(4, 40);
        if (!b.feed(4, 2).equals(new Feed(List.of(40), 1)) || b.delete(99)) throw new AssertionError("e2 self");
        // Random calls checked against a filter of the full tweet list, then a cut.
        Random rnd = new Random(9203);
        for (int round = 0; round < 400; round++) {
            FeedDesk s = new FeedDesk();
            List<int[]> all = new ArrayList<>();
            boolean[][] fol = new boolean[4][4], mut = new boolean[4][4];
            Set<Integer> dead = new HashSet<>();
            int nextId = 100;
            for (int op = 0; op < 60; op++) {
                int u = rnd.nextInt(4), v = rnd.nextInt(4), t = rnd.nextInt(7);
                if (t == 0) { all.add(new int[] {u, nextId}); s.post(u, nextId++); }
                else if (t == 1) { if (u != v) fol[u][v] = true; s.follow(u, v); }
                else if (t == 2) { fol[u][v] = false; s.unfollow(u, v); }
                else if (t == 3) { if (u != v) mut[u][v] = true; s.mute(u, v); }
                else if (t == 4) { mut[u][v] = false; s.unmute(u, v); }
                else if (t == 5) {
                    int id = 100 + rnd.nextInt(nextId - 99);
                    boolean want = id < nextId && dead.add(id);
                    if (s.delete(id) != want) throw new AssertionError("delete");
                } else {
                    int k = 1 + rnd.nextInt(5);
                    List<Integer> ids = new ArrayList<>();
                    Set<Integer> src = new HashSet<>();
                    // Newest first: walk the post list from the end and filter before counting.
                    for (int i = all.size() - 1; i >= 0 && ids.size() < k; i--) {
                        int au = all.get(i)[0], id = all.get(i)[1];
                        boolean vis = au == u || (fol[u][au] && !mut[u][au]);
                        if (vis && !dead.contains(id)) { ids.add(id); src.add(au); }
                    }
                    if (!s.feed(u, k).equals(new Feed(ids, src.size()))) throw new AssertionError("feed");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Ride Sharing With Nearest Driver (LeetCode 3829)
<!-- id: sv-ix-ride-match -->

**Approach.** The authoritative state is two maps: one from driver id to a driver record with position and status, and one from rider id to a rider record with position, destination, status and driver. A status is free, riding, offline, waiting, done or cancelled. The two derived indexes are a linked hash set of waiting rider ids in arrival order, and a tree set of free spots, where a spot is an immutable pair of position and driver id. Spots are never changed while they sit in the set. A driver who moves gets a new spot.

Two writer helpers keep the indexes in step. `markFree` puts a driver at a position with status free and inserts the spot. `takeSpot` removes the spot of a free driver. Every call validates its status precondition first and then uses the helpers. A match finds the first waiting rider, then the nearest free spot. The nearest spot is the better of two candidates. The right candidate is the ceiling of the rider's position with the smallest id. The left candidate is the smallest-id spot at the largest position below the rider, found by one `lower` call and one `ceiling` call. A distance tie goes to the smaller id.

The invariant says that a driver has a spot exactly when the driver is free, and a rider is in the waiting set exactly when the rider is waiting. Both sides of a match are validated before either is written.

**Complexity.**

- **Time** is O(log n) per call, because each call runs a constant number of hash, set and tree operations.
- **Space** is O(n), since each driver and rider holds one record and at most one index entry.

```java run
import java.util.*;

public final class RideMatchSolution {
    static final class RideDesk {
        private static final int FREE = 0, RIDING = 1, OFFLINE = 2, WAITING = 3, DONE = 4, CANCELLED = 5;
        private static final class Driver { int pos, status; }
        private static final class Rider { int pos, dest, status, driver; }
        private record Spot(int pos, int id) {}
        private static final Comparator<Spot> ORDER = (a, b) ->
                a.pos() != b.pos() ? Integer.compare(a.pos(), b.pos()) : Integer.compare(a.id(), b.id());
        private final Map<Integer, Driver> drivers = new HashMap<>();
        private final Map<Integer, Rider> riders = new HashMap<>();
        private final Set<Integer> waiting = new LinkedHashSet<>();
        private final TreeSet<Spot> free = new TreeSet<>(ORDER);

        // Puts a driver at a position and into the free index; O(log n) time, O(1) space.
        private void markFree(int id, Driver d, int pos) {
            d.pos = pos;
            d.status = FREE;
            free.add(new Spot(pos, id));
        }

        // Removes the exact spot of a free driver; O(log n) time, O(1) space.
        private void takeSpot(int id, Driver d) { free.remove(new Spot(d.pos, id)); }

        boolean addDriver(int id, int pos) {
            if (drivers.containsKey(id)) return false;
            Driver d = new Driver();
            drivers.put(id, d);
            markFree(id, d, pos);
            return true;
        }

        boolean goOffline(int id) {
            Driver d = drivers.get(id);
            if (d == null || d.status != FREE) return false;
            takeSpot(id, d);
            d.status = OFFLINE;
            return true;
        }

        boolean request(int id, int pos, int dest) {
            if (riders.containsKey(id)) return false;
            Rider r = new Rider();
            r.pos = pos; r.dest = dest; r.status = WAITING;
            riders.put(id, r);
            waiting.add(id);
            return true;
        }

        boolean cancel(int id) {
            Rider r = riders.get(id);
            if (r == null || r.status != WAITING) return false;
            waiting.remove(id);
            r.status = CANCELLED;
            return true;
        }

        // Returns the nearest free spot, the smaller id on a tie, or null; O(log n) time, O(1) space.
        private Spot nearest(int pos) {
            Spot right = free.ceiling(new Spot(pos, Integer.MIN_VALUE));
            Spot edge = free.lower(new Spot(pos, Integer.MIN_VALUE));
            // The lower call returns the largest id at the left position, so one more call finds the smallest id there.
            Spot left = edge == null ? null : free.ceiling(new Spot(edge.pos(), Integer.MIN_VALUE));
            if (left == null) return right;
            if (right == null) return left;
            long dl = (long) pos - left.pos(), dr = (long) right.pos() - pos;
            if (dl != dr) return dl < dr ? left : right;
            return left.id() <= right.id() ? left : right;
        }

        /**
         * Pairs the longest-waiting rider with the nearest free driver.
         * Time: O(log n).
         * Space: O(1).
         * Invariant: both sides are found before the first write.
         */
        int[] match() {
            if (waiting.isEmpty() || free.isEmpty()) return new int[0];
            int rid = waiting.iterator().next();
            Rider r = riders.get(rid);
            Spot s = nearest(r.pos);
            Driver d = drivers.get(s.id());
            waiting.remove(rid);
            takeSpot(s.id(), d);
            r.status = RIDING; r.driver = s.id();
            d.status = RIDING;
            return new int[] {rid, s.id()};
        }

        boolean finish(int id) {
            Rider r = riders.get(id);
            if (r == null || r.status != RIDING) return false;
            r.status = DONE;
            markFree(r.driver, drivers.get(r.driver), r.dest);
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        RideDesk a = new RideDesk();
        boolean ok = a.addDriver(1, 10) && a.addDriver(2, 20) && a.request(100, 15, 40) && a.request(101, 30, 5);
        if (!ok) throw new AssertionError("e1 setup");
        if (!Arrays.equals(a.match(), new int[] {100, 1}) || !Arrays.equals(a.match(), new int[] {101, 2})) throw new AssertionError("e1 match");
        if (a.match().length != 0 || !a.finish(100)) throw new AssertionError("e1 finish");
        // Example 2 from the problem text.
        RideDesk b = new RideDesk();
        if (!b.request(7, 5, 9) || b.match().length != 0 || !b.addDriver(3, 100)) throw new AssertionError("e2 setup");
        if (!b.cancel(7) || b.cancel(7) || b.match().length != 0 || b.finish(7)) throw new AssertionError("e2 calls");
        // Random calls checked against linear scans of plain arrays.
        Random rnd = new Random(9204);
        for (int round = 0; round < 500; round++) {
            RideDesk s = new RideDesk();
            int D = 5, R = 6;
            int[] dpos = new int[D], dst = new int[D];          // dst: -1 unused, 0 free, 1 riding, 2 offline
            Arrays.fill(dst, -1);
            int[] rpos = new int[R], rdest = new int[R], rst = new int[R], rdrv = new int[R];
            Arrays.fill(rst, -1);                                // -1 unused, 0 waiting, 1 riding, 2 done, 3 cancelled
            List<Integer> order = new ArrayList<>();
            for (int op = 0; op < 60; op++) {
                int t = rnd.nextInt(6), id = rnd.nextInt(6);
                if (t == 0) {
                    int i = id % D, p = rnd.nextInt(10);
                    boolean want = dst[i] == -1;
                    if (want) { dst[i] = 0; dpos[i] = p; }
                    if (s.addDriver(i, p) != want) throw new AssertionError("addDriver");
                } else if (t == 1) {
                    int i = id % D;
                    boolean want = dst[i] == 0;
                    if (want) dst[i] = 2;
                    if (s.goOffline(i) != want) throw new AssertionError("goOffline");
                } else if (t == 2) {
                    int p = rnd.nextInt(10), d = rnd.nextInt(10);
                    boolean want = rst[id] == -1;
                    if (want) { rst[id] = 0; rpos[id] = p; rdest[id] = d; order.add(id); }
                    if (s.request(id, p, d) != want) throw new AssertionError("request");
                } else if (t == 3) {
                    boolean want = rst[id] == 0;
                    if (want) { rst[id] = 3; order.remove((Integer) id); }
                    if (s.cancel(id) != want) throw new AssertionError("cancel");
                } else if (t == 4) {
                    int[] want = new int[0];
                    int bestD = -1;
                    if (!order.isEmpty()) {
                        int rid = order.get(0);
                        for (int i = 0; i < D; i++) {
                            if (dst[i] != 0) continue;
                            if (bestD == -1 || Math.abs(dpos[i] - rpos[rid]) < Math.abs(dpos[bestD] - rpos[rid])) bestD = i;
                        }
                        if (bestD != -1) {
                            want = new int[] {rid, bestD};
                            order.remove(0); rst[rid] = 1; rdrv[rid] = bestD; dst[bestD] = 1;
                        }
                    }
                    if (!Arrays.equals(s.match(), want)) throw new AssertionError("match");
                } else {
                    boolean want = rst[id] == 1;
                    if (want) { rst[id] = 2; dst[rdrv[id]] = 0; dpos[rdrv[id]] = rdest[id]; }
                    if (s.finish(id) != want) throw new AssertionError("finish");
                }
            }
        }
    }
}
```
