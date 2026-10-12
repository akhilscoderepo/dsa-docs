<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Choosing Graph Methods

#### Solution: [Build] Cheapest Cables For Exactly g Groups (LeetCode 1584)
<!-- id: ga-ch-cable-groups -->

**Approach.**
The method lists the cost of every pair of sites as a triple of cost and two indexes, and it sorts the triples by cost. It then scans them with union-find. A triple whose two sites have equal roots would close a cycle, so the scan skips it. Any other triple merges two groups, adds its cost to a `long` total and lowers the group counter by one. The scan stops as soon as the counter equals `g`.

The invariant is that the accepted cables form a forest, and the forest is a cheapest forest with its current number of groups. Each accepted cable is the lightest one that leaves its group, which is the cut property for the cut between that group and the rest. Stopping at `g` groups means that exactly `n - g` cables are accepted. The total cannot be lower, because every forest with `g` groups has `n - g` cables and the scan took the cheapest safe ones first. The total uses `long`, because an `int` sum wraps past 2147483647.

**Complexity.**
- **Time** is O(n^2 log n), because the list holds n(n - 1) / 2 pairs and the sort dominates the near-constant union-find work.
- **Space** is O(n^2) for the pair list and O(n) for the `parent` array.

```java run
import java.util.*;

public final class ChooseCableGroups {
    /**
     * Returns the least total cost of cables that leave exactly g groups of sites.
     * Time: O(n^2 log n). Space: O(n^2).
     * Invariant: the accepted cables form a cheapest forest for the current group count.
     */
    static long cheapestForGroups(int[][] points, int g) {
        int n = points.length;
        // One triple {cost, i, j} per pair of sites; the list has n(n-1)/2 entries.
        List<int[]> pairs = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int cost = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]);
                pairs.add(new int[] {cost, i, j});
            }
        }
        // Sorting by cost makes the first usable cable of each scan the lightest one.
        pairs.sort((a, b) -> Integer.compare(a[0], b[0]));
        int[] parent = new int[n];
        // Every site starts as the root of its own group.
        for (int i = 0; i < n; i++) parent[i] = i;
        int groups = n;
        long total = 0;
        for (int[] p : pairs) {
            // Reaching g groups ends the scan early, so the later pairs cost nothing.
            if (groups == g) break;
            int a = find(parent, p[1]), b = find(parent, p[2]);
            // Equal roots mean the cable would close a cycle, so it is skipped.
            if (a == b) continue;
            parent[a] = b;
            // The sum is a long because a total of int values can pass the int range.
            total += p[0];
            groups--;
        }
        return total;
    }

    /** Finds the root of x with path halving. Time: near constant per call. Space: O(1). */
    static int find(int[] parent, int x) {
        // The loop climbs until a site is its own parent.
        while (parent[x] != x) {
            // Pointing x at its grandparent shortens later climbs.
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    /** Oracle: tries every subset of cables and keeps the cheapest one with exactly g groups. */
    static long oracle(int[][] points, int g) {
        int n = points.length;
        List<int[]> pairs = new ArrayList<>();
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                pairs.add(new int[] {Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]), i, j});
        long best = Long.MAX_VALUE;
        for (int mask = 0; mask < (1 << pairs.size()); mask++) {
            int[] parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
            int groups = n;
            long cost = 0;
            for (int k = 0; k < pairs.size(); k++) {
                if ((mask >> k & 1) == 0) continue;
                int a = find(parent, pairs.get(k)[1]), b = find(parent, pairs.get(k)[2]);
                if (a != b) {
                    parent[a] = b;
                    groups--;
                }
                cost += pairs.get(k)[0];
            }
            if (groups == g) best = Math.min(best, cost);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] sites = {{1, 1}, {3, 4}, {8, 1}, {6, 6}, {2, 7}};
        if (cheapestForGroups(sites, 2) != 14) throw new AssertionError("example 1");
        if (cheapestForGroups(sites, 5) != 0) throw new AssertionError("example 2");
        // A single site has one group and costs nothing.
        if (cheapestForGroups(new int[][] {{0, 0}}, 1) != 0) throw new AssertionError("single site");
        // The claim about int sums: one more than the largest int wraps to a negative number.
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("int wrap");
        // Random inputs with distinct points are checked against the subset oracle.
        Random rnd = new Random(7);
        for (int iter = 0; iter < 300; iter++) {
            int n = 1 + rnd.nextInt(6);
            Set<Long> seen = new HashSet<>();
            int[][] pts = new int[n][];
            for (int i = 0; i < n; i++) {
                int x, y;
                do {
                    x = rnd.nextInt(11) - 5;
                    y = rnd.nextInt(11) - 5;
                } while (!seen.add(x * 100L + y));
                pts[i] = new int[] {x, y};
            }
            int[][] copy = Arrays.stream(pts).map(int[]::clone).toArray(int[][]::new);
            int g = 1 + rnd.nextInt(n);
            if (cheapestForGroups(pts, g) != oracle(pts, g)) throw new AssertionError("random " + iter);
            // The input array stays unchanged.
            if (!Arrays.deepEquals(pts, copy)) throw new AssertionError("mutated");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Bridges With Large Sides (LeetCode 1192)
<!-- id: ga-ch-bridges-by-size -->

**Approach.**
The method builds an adjacency list in which each entry holds the neighbor and the number of the connection. It runs one depth-first search from server 0. On entry to a server `u`, the search sets `disc[u]` and `low[u]` to the next clock value and starts the size `sz[u]` at 1. It skips the connection that led to `u` by number, so a parent edge never counts as a back edge. A neighbor already reached lowers `low[u]` to the neighbor's discovery time. A new neighbor `v` is visited, and then `low[u]` takes the smaller value, and `sz[u]` grows by `sz[v]`.

The invariant is that `low[v]` is final when `visit(v)` returns, and `sz[v]` is the number of servers in the subtree of `v`. The tree edge from `u` to `v` is a bridge exactly when `low[v] > disc[u]`. Removing it leaves the subtree of `v` with `sz[v]` servers and the rest with `n - sz[v]`. The method keeps the bridge when both numbers reach `s`. It stores the pair as smaller then larger and sorts the final list, because the search order is not the requested order.

**Complexity.**
- **Time** is O(n + m + b log b) for `m` connections and `b` reported bridges. The search reads each connection twice, and the sort handles only the reported pairs.
- **Space** is O(n + m) for the adjacency list and the arrays, plus recursion depth up to n.

```java run
import java.util.*;

public final class ChooseBridgesBySize {
    /**
     * Returns the bridges whose two sides each hold at least s servers, as sorted [smaller, larger] pairs.
     * Time: O(n + m + b log b). Space: O(n + m).
     * Invariant: low[v] and sz[v] are final when the visit of v returns.
     */
    static List<List<Integer>> bridgesBySize(int n, int[][] connections, int s) {
        // Each adjacency entry holds {neighbor, connection number}.
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int id = 0; id < connections.length; id++) {
            adj.get(connections[id][0]).add(new int[] {connections[id][1], id});
            adj.get(connections[id][1]).add(new int[] {connections[id][0], id});
        }
        int[] disc = new int[n], low = new int[n], sz = new int[n];
        int[] clock = {0};
        List<List<Integer>> out = new ArrayList<>();
        // The network is connected, so one search from server 0 reaches everything.
        visit(0, -1, n, s, adj, disc, low, sz, clock, out);
        // Pairs are compared by the first entry and then by the second entry.
        out.sort((a, b) -> a.get(0).equals(b.get(0)) ? Integer.compare(a.get(1), b.get(1)) : Integer.compare(a.get(0), b.get(0)));
        return out;
    }

    /** Depth-first visit that fills disc, low and sz. Time: O(deg(u)) per call. Space: O(1) per frame. */
    static void visit(int u, int viaId, int n, int s, List<List<int[]>> adj, int[] disc, int[] low, int[] sz,
                      int[] clock, List<List<Integer>> out) {
        // The first discovery sets both numbers; 0 stays the marker of an unreached server.
        disc[u] = low[u] = ++clock[0];
        sz[u] = 1;
        for (int[] e : adj.get(u)) {
            // The entering connection is skipped by number, so it never acts as a back edge.
            if (e[1] == viaId) continue;
            int v = e[0];
            if (disc[v] == 0) {
                visit(v, e[1], n, s, adj, disc, low, sz, clock, out);
                // The child's low link may reach above u, and its size joins the subtree of u.
                low[u] = Math.min(low[u], low[v]);
                sz[u] += sz[v];
                // No edge climbs above u from the subtree of v, so the tree edge is a bridge.
                if (low[v] > disc[u] && sz[v] >= s && n - sz[v] >= s) {
                    out.add(List.of(Math.min(u, v), Math.max(u, v)));
                }
            } else {
                // A back edge to an earlier server lowers the low link of u.
                low[u] = Math.min(low[u], disc[v]);
            }
        }
    }

    /** Oracle: removes each connection and counts the servers reachable from one endpoint. */
    static List<List<Integer>> oracle(int n, int[][] connections, int s) {
        List<List<Integer>> out = new ArrayList<>();
        for (int skip = 0; skip < connections.length; skip++) {
            boolean[] seen = new boolean[n];
            Deque<Integer> stack = new ArrayDeque<>();
            seen[connections[skip][0]] = true;
            stack.push(connections[skip][0]);
            int count = 1;
            while (!stack.isEmpty()) {
                int u = stack.pop();
                for (int id = 0; id < connections.length; id++) {
                    if (id == skip) continue;
                    int other = connections[id][0] == u ? connections[id][1] : connections[id][1] == u ? connections[id][0] : -1;
                    if (other >= 0 && !seen[other]) {
                        seen[other] = true;
                        count++;
                        stack.push(other);
                    }
                }
            }
            int a = connections[skip][0], b = connections[skip][1];
            if (!seen[b] && count >= s && n - count >= s) out.add(List.of(Math.min(a, b), Math.max(a, b)));
        }
        out.sort((x, y) -> x.get(0).equals(y.get(0)) ? Integer.compare(x.get(1), y.get(1)) : Integer.compare(x.get(0), y.get(0)));
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] c1 = {{0, 1}, {1, 2}, {2, 0}, {1, 3}, {3, 4}, {4, 5}, {5, 3}, {3, 6}, {6, 7}};
        if (!bridgesBySize(8, c1, 2).toString().equals("[[1, 3], [3, 6]]")) throw new AssertionError("example 1");
        int[][] c2 = {{0, 1}, {1, 2}, {2, 3}};
        if (!bridgesBySize(4, c2, 2).toString().equals("[[1, 2]]")) throw new AssertionError("example 2");
        // Boundary: a size bound above half of n leaves no bridge.
        if (!bridgesBySize(4, c2, 3).isEmpty()) throw new AssertionError("large bound");
        // Random connected simple graphs are checked against the removal oracle.
        Random rnd = new Random(11);
        for (int iter = 0; iter < 400; iter++) {
            int n = 2 + rnd.nextInt(8);
            List<int[]> edges = new ArrayList<>();
            Set<Integer> used = new HashSet<>();
            // A random tree makes the graph connected.
            for (int v = 1; v < n; v++) {
                int u = rnd.nextInt(v);
                edges.add(new int[] {u, v});
                used.add(u * 100 + v);
            }
            // Extra connections, without repeats or self loops, create cycles.
            for (int extra = rnd.nextInt(6); extra > 0; extra--) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a == b || !used.add(Math.min(a, b) * 100 + Math.max(a, b))) continue;
                edges.add(new int[] {a, b});
            }
            Collections.shuffle(edges, rnd);
            int[][] conn = edges.toArray(new int[0][]);
            int s = 1 + rnd.nextInt(n);
            if (!bridgesBySize(n, conn, s).equals(oracle(n, conn, s))) throw new AssertionError("random " + iter);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] City With Fewest Strictly Near Cities (LeetCode 1334)
<!-- id: ga-ch-city-strict -->

**Approach.**
The cue is a question about distances between all pairs on a map with at most 100 cities. The method fills a `long[][]` table with `Long.MAX_VALUE` as the no-route sentinel and 0 on the diagonal. Each undirected road writes its length into both directions and keeps the smaller value if a pair repeats. Three loops then run with the intermediate city `k` as the outermost loop. Before any addition, the method tests that both parts differ from the sentinel, because the sum of two copies of `Long.MAX_VALUE` wraps to a negative number.

The invariant is that after the round for `k`, each entry is the best distance whose intermediates all have an index of at most `k`. After the last round the table holds the shortest distances. A final scan counts, for each city, the other cities whose distance is strictly below `limit`. The sentinel never counts, because it exceeds every limit. The scan uses `<=` when it compares counts, so a later city with an equal count replaces the earlier one, and the greatest index wins. Counting with `<=` against the limit instead of `<` would put a city at distance exactly `limit` into the count, which is the boundary error.

**Complexity.**
- **Time** is O(n^3) for the three loops, plus O(n^2) for the final scan.
- **Space** is O(n^2) for the distance table.

```java run
import java.util.*;

public final class ChooseCityStrict {
    /**
     * Returns the city with the fewest cities strictly closer than limit, preferring the greatest index.
     * Time: O(n^3). Space: O(n^2).
     * Invariant: after the round for k, dist[i][j] is the best distance with intermediates 0..k.
     */
    static int fewestNearCity(int n, int[][] roads, int limit) {
        long[][] dist = new long[n][n];
        // Long.MAX_VALUE marks a pair with no known route.
        for (long[] row : dist) Arrays.fill(row, Long.MAX_VALUE);
        for (int i = 0; i < n; i++) dist[i][i] = 0;
        for (int[] r : roads) {
            // A road runs both ways, and the smaller length wins if a pair repeats.
            dist[r[0]][r[1]] = Math.min(dist[r[0]][r[1]], r[2]);
            dist[r[1]][r[0]] = Math.min(dist[r[1]][r[0]], r[2]);
        }
        // The intermediate city is the outermost loop, which the recurrence requires.
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                // Skipping an unreachable first half saves work and avoids sentinel arithmetic.
                if (dist[i][k] == Long.MAX_VALUE) continue;
                for (int j = 0; j < n; j++) {
                    if (dist[k][j] == Long.MAX_VALUE) continue;
                    long through = dist[i][k] + dist[k][j];
                    if (through < dist[i][j]) dist[i][j] = through;
                }
            }
        }
        int bestCity = -1, bestCount = Integer.MAX_VALUE;
        for (int i = 0; i < n; i++) {
            int near = 0;
            for (int j = 0; j < n; j++) {
                // Strictly below the limit counts as near, and the sentinel is never below it.
                if (i != j && dist[i][j] < limit) near++;
            }
            // A later city with an equal count replaces the earlier one, so the greatest index wins.
            if (near <= bestCount) {
                bestCount = near;
                bestCity = i;
            }
        }
        return bestCity;
    }

    /** Oracle: Bellman-Ford style passes from every source instead of the table. */
    static int oracle(int n, int[][] roads, int limit) {
        int bestCity = -1, bestCount = Integer.MAX_VALUE;
        for (int s = 0; s < n; s++) {
            long[] d = new long[n];
            Arrays.fill(d, Long.MAX_VALUE);
            d[s] = 0;
            for (int pass = 0; pass < n; pass++) {
                for (int[] r : roads) {
                    if (d[r[0]] != Long.MAX_VALUE && d[r[0]] + r[2] < d[r[1]]) d[r[1]] = d[r[0]] + r[2];
                    if (d[r[1]] != Long.MAX_VALUE && d[r[1]] + r[2] < d[r[0]]) d[r[0]] = d[r[1]] + r[2];
                }
            }
            int near = 0;
            for (int v = 0; v < n; v++) if (v != s && d[v] != Long.MAX_VALUE && d[v] < limit) near++;
            if (near <= bestCount) {
                bestCount = near;
                bestCity = s;
            }
        }
        return bestCity;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] roads = {{0, 1, 3}, {1, 2, 1}, {1, 3, 4}, {2, 3, 1}};
        if (fewestNearCity(4, roads, 5) != 3) throw new AssertionError("example 1");
        if (fewestNearCity(4, roads, 3) != 0) throw new AssertionError("example 2");
        // Limit 1 makes every count 0 because lengths are at least 1, so the greatest index wins.
        if (fewestNearCity(4, roads, 1) != 3) throw new AssertionError("limit one");
        // The sentinel claim: adding two copies of Long.MAX_VALUE wraps to a negative number.
        if (Long.MAX_VALUE + Long.MAX_VALUE >= 0) throw new AssertionError("long wrap");
        // Disconnected map: the isolated city has no near city and the greatest index among ties.
        if (fewestNearCity(3, new int[][] {{0, 1, 2}}, 10) != 2) throw new AssertionError("isolated");
        // Random maps are checked against the per-source oracle.
        Random rnd = new Random(23);
        for (int iter = 0; iter < 500; iter++) {
            int n = 2 + rnd.nextInt(7);
            List<int[]> list = new ArrayList<>();
            for (int a = 0; a < n; a++)
                for (int b = a + 1; b < n; b++)
                    if (rnd.nextInt(3) == 0) list.add(new int[] {a, b, 1 + rnd.nextInt(9)});
            if (list.isEmpty()) list.add(new int[] {0, 1, 1 + rnd.nextInt(9)});
            int[][] rd = list.toArray(new int[0][]);
            int limit = 1 + rnd.nextInt(12);
            if (fewestNearCity(n, rd, limit) != oracle(n, rd, limit)) throw new AssertionError("random " + iter);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Reconstruct Itinerary (LeetCode 332)
<!-- id: ga-ch-itinerary-smallest -->

**Approach.**
The cue is the demand to use every ticket exactly once, which makes each ticket an edge that the walk consumes. The method maps each airport to a `PriorityQueue<String>` of destinations, so polling returns the smallest unused destination. It keeps a stack that starts with `JFK`. While the stack is not empty, it looks at the top airport. When that airport has an unused ticket, the method polls the smallest destination and pushes it. Otherwise the airport is a dead end, and the method moves it from the stack to the front of the answer list.

The invariant is that the answer list holds a valid tail of the trip, written in order, and every ticket in it is consumed. An airport enters the list only when no unused ticket leaves it, which is the postorder write. Taking the smallest destination first makes the first complete walk the smallest one in dictionary order. A dead end that is smaller than a longer route still comes out last, so the trip with all tickets wins. Strings compare with `compareTo`, and the queue orders three-letter codes in that order.

**Complexity.**
- **Time** is O(m log m) for `m` tickets, because each ticket enters and leaves a queue once.
- **Space** is O(m) for the queues, the stack and the answer list.

```java run
import java.util.*;

public final class ChooseItinerarySmallest {
    /**
     * Returns the smallest trip from JFK that uses every ticket once.
     * Time: O(m log m). Space: O(m).
     * Invariant: the answer list is a valid tail of the trip made of consumed tickets only.
     */
    static List<String> smallestItinerary(List<List<String>> tickets) {
        // Each airport owns a queue that returns its smallest unused destination first.
        Map<String, PriorityQueue<String>> unused = new HashMap<>();
        for (List<String> t : tickets) {
            unused.computeIfAbsent(t.get(0), k -> new PriorityQueue<>()).add(t.get(1));
        }
        Deque<String> stack = new ArrayDeque<>();
        LinkedList<String> trip = new LinkedList<>();
        stack.push("JFK");
        // Every turn either consumes one ticket or moves one airport to the answer.
        while (!stack.isEmpty()) {
            PriorityQueue<String> q = unused.get(stack.peek());
            if (q == null || q.isEmpty()) {
                // Dead end: no unused ticket leaves the airport, so it is written to the front.
                trip.addFirst(stack.pop());
            } else {
                // Consume the smallest unused ticket and walk to its destination.
                stack.push(q.poll());
            }
        }
        return trip;
    }

    /** Oracle: tries every order of tickets and keeps the smallest valid trip. */
    static List<String> oracle(List<List<String>> tickets) {
        // The recursion explores each unused ticket that leaves the current airport.
        return search("JFK", new ArrayList<>(List.of("JFK")), new boolean[tickets.size()], tickets, null);
    }

    /** Extends the path by every unused ticket from at and returns the smallest complete trip found. */
    static List<String> search(String at, List<String> path, boolean[] used, List<List<String>> tickets, List<String> best) {
        if (path.size() == tickets.size() + 1) {
            // A complete trip replaces the best one when it is smaller position by position.
            if (best == null || compare(path, best) < 0) return new ArrayList<>(path);
            return best;
        }
        for (int k = 0; k < tickets.size(); k++) {
            if (used[k] || !tickets.get(k).get(0).equals(at)) continue;
            used[k] = true;
            path.add(tickets.get(k).get(1));
            best = search(tickets.get(k).get(1), path, used, tickets, best);
            path.remove(path.size() - 1);
            used[k] = false;
        }
        return best;
    }

    /** Compares two trips of equal length position by position. */
    static int compare(List<String> a, List<String> b) {
        for (int i = 0; i < a.size(); i++) {
            int c = a.get(i).compareTo(b.get(i));
            if (c != 0) return c;
        }
        return 0;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        List<List<String>> t1 = List.of(List.of("JFK", "SFO"), List.of("JFK", "ATL"), List.of("SFO", "ATL"),
                List.of("ATL", "JFK"), List.of("ATL", "SFO"));
        if (!smallestItinerary(t1).toString().equals("[JFK, ATL, JFK, SFO, ATL, SFO]")) throw new AssertionError("example 1");
        List<List<String>> t2 = List.of(List.of("JFK", "AAA"), List.of("AAA", "JFK"), List.of("JFK", "AAA"), List.of("AAA", "BBB"));
        if (!smallestItinerary(t2).toString().equals("[JFK, AAA, JFK, AAA, BBB]")) throw new AssertionError("example 2");
        // Strings compare by dictionary order, which the queue relies on.
        if ("ATL".compareTo("JFK") >= 0) throw new AssertionError("string order");
        // The input list stays unchanged because the method only reads it.
        List<List<String>> before = new ArrayList<>(t1);
        smallestItinerary(t1);
        if (!before.equals(t1)) throw new AssertionError("mutated");
        // Random valid inputs come from random walks that start at JFK.
        String[] names = {"JFK", "ATL", "SFO", "LAX"};
        Random rnd = new Random(5);
        for (int iter = 0; iter < 400; iter++) {
            int steps = 1 + rnd.nextInt(7);
            List<List<String>> tickets = new ArrayList<>();
            String cur = "JFK";
            for (int i = 0; i < steps; i++) {
                String nxt = names[rnd.nextInt(names.length)];
                tickets.add(List.of(cur, nxt));
                cur = nxt;
            }
            Collections.shuffle(tickets, rnd);
            if (!smallestItinerary(tickets).equals(oracle(tickets))) throw new AssertionError("random " + iter);
        }
        System.out.println("ok");
    }
}
```
