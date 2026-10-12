<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Every-Edge-Once Routes

#### Solution: [Build] Eulerian Cycle (Author exercise)
<!-- id: ga-hier-euler-cycle -->

**Approach.**
The method counts `out - in` for every vertex and returns an empty array unless all counts are zero. It then keeps an `ArrayDeque` of open vertices, starting with vertex 0. While the top vertex has an unused outgoing link, the method moves that vertex's cursor forward and pushes the target. When the top vertex has none, the method pops it and appends it to the output list. After the stack empties, the output holds `E + 1` vertices exactly when every link was reachable from vertex 0, and the method reverses it.

The invariant is that the output, read backward, is a valid tail of the cycle made only of consumed links. A popped vertex has no unused outgoing link, so nothing can ever be inserted after it. The adjacency lists keep the order of `links`, so the earliest listed unused link is the one at the cursor. A graph with no links pops vertex 0 alone and returns `[0]`. The method never writes to `links`, because it copies the targets into its own lists.

**Complexity.**
- **Time** is O(V + E), because each link is pushed once and popped once, and the degree pass reads each link once.
- **Space** is O(V + E) for the adjacency lists, the cursors, the stack and the output.

```java run
import java.util.*;

public final class HierEulerCycle {
    /**
     * Returns an Eulerian cycle from vertex 0, or an empty array when none exists.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: the output, read backward, is a valid tail of the cycle made of consumed links.
     */
    static int[] cycle(int n, int[][] links) {
        // Adjacency lists keep the order of links, so the earliest listed link comes first.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        int[] balance = new int[n];
        // One pass over the links fills the lists and the degree differences.
        for (int[] e : links) {
            adj.get(e[0]).add(e[1]);
            balance[e[0]]++;
            balance[e[1]]--;
        }
        // A cycle needs every vertex balanced, so any other count ends the search.
        for (int v = 0; v < n; v++) if (balance[v] != 0) return new int[0];
        int[] cursor = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        stack.push(0);
        // Each pass pushes one link or pops one vertex, so the loop runs at most 2E + 1 times.
        while (!stack.isEmpty()) {
            int v = stack.peek();
            if (cursor[v] < adj.get(v).size()) {
                // Advancing the cursor consumes the link, and the target joins the open walk.
                stack.push(adj.get(v).get(cursor[v]++));
            } else {
                // A vertex without unused links is final, so it joins the output.
                out.add(stack.pop());
            }
        }
        // Fewer than E + 1 recorded vertices means some links are unreachable from vertex 0.
        if (out.size() != links.length + 1) return new int[0];
        int[] res = new int[out.size()];
        // Reading the output from the end gives the travel order.
        for (int i = 0; i < res.length; i++) res[i] = out.get(res.length - 1 - i);
        return res;
    }

    /** Recursive reference with the same edge order; it is correct but uses one frame per link. */
    static void rec(int v, List<List<Integer>> adj, int[] cursor, List<Integer> out) {
        // The loop consumes links in listed order and recurses on each target.
        while (cursor[v] < adj.get(v).size()) rec(adj.get(v).get(cursor[v]++), adj, cursor, out);
        // The vertex is recorded after all of its links.
        out.add(v);
    }

    /** Oracle: the recursive version after the same degree test. */
    static int[] recursive(int n, int[][] links) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        int[] bal = new int[n];
        for (int[] e : links) { adj.get(e[0]).add(e[1]); bal[e[0]]++; bal[e[1]]--; }
        for (int b : bal) if (b != 0) return new int[0];
        List<Integer> out = new ArrayList<>();
        rec(0, adj, new int[n], out);
        if (out.size() != links.length + 1) return new int[0];
        int[] res = new int[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(res.length - 1 - i);
        return res;
    }

    /** Brute force: tries every order of the links and reports whether some order forms a cycle from 0. */
    static boolean exists(int[][] links, boolean[] used, int v, int count) {
        // All links used and back at vertex 0 means a cycle exists.
        if (count == links.length) return v == 0;
        for (int i = 0; i < links.length; i++) {
            if (!used[i] && links[i][0] == v) {
                used[i] = true;
                boolean ok = exists(links, used, links[i][1], count + 1);
                used[i] = false;
                if (ok) return true;
            }
        }
        return false;
    }

    /** Checks that a vertex array is a cycle from 0 that uses every link exactly once. */
    static boolean valid(int[][] links, int[] route) {
        if (route.length != links.length + 1 || route[0] != 0 || route[route.length - 1] != 0) return false;
        boolean[] used = new boolean[links.length];
        for (int k = 0; k + 1 < route.length; k++) {
            int found = -1;
            for (int i = 0; i < links.length; i++) {
                if (!used[i] && links[i][0] == route[k] && links[i][1] == route[k + 1]) { found = i; break; }
            }
            if (found < 0) return false;
            used[found] = true;
        }
        return true;
    }

    public static void main(String[] args) throws Exception {
        // The two examples of the exercise.
        int[][] g1 = {{0, 1}, {1, 2}, {2, 0}, {1, 3}, {3, 1}, {1, 4}, {4, 1}};
        if (!Arrays.equals(cycle(5, g1), new int[] {0, 1, 3, 1, 4, 1, 2, 0})) throw new AssertionError("ex1");
        if (cycle(4, new int[][] {{0, 1}, {1, 2}, {2, 0}, {2, 3}}).length != 0) throw new AssertionError("ex2");
        // A graph with no links returns only vertex 0.
        if (!Arrays.equals(cycle(3, new int[0][]), new int[] {0})) throw new AssertionError("empty");
        // Balanced degrees alone do not suffice: the second loop is unreachable from vertex 0.
        if (cycle(4, new int[][] {{0, 1}, {1, 0}, {2, 3}, {3, 2}}).length != 0) throw new AssertionError("split");
        // Java fact: a recursive walk needs one frame per link and overflows a small thread stack.
        int big = 200_000;
        int[][] ring = new int[big][];
        for (int i = 0; i < big; i++) ring[i] = new int[] {i, (i + 1) % big};
        boolean[] overflowed = {false};
        Thread t = new Thread(null, () -> {
            try { recursive(big, ring); } catch (StackOverflowError e) { overflowed[0] = true; }
        }, "small-stack", 256 * 1024);
        t.start();
        t.join();
        if (!overflowed[0]) throw new AssertionError("recursion should overflow");
        // The explicit stack handles the same ring.
        if (cycle(big, ring).length != big + 1) throw new AssertionError("ring");
        // Random graphs, half of them built from closed walks so that cycles are common.
        Random rnd = new Random(2501);
        for (int tr = 0; tr < 3000; tr++) {
            int n = 1 + rnd.nextInt(4);
            List<int[]> list = new ArrayList<>();
            if (rnd.nextBoolean()) {
                int v = 0, len = rnd.nextInt(7);
                for (int s = 0; s < len; s++) { int w = rnd.nextInt(n); list.add(new int[] {v, w}); v = w; }
                if (v != 0) list.add(new int[] {v, 0});
            } else {
                int m = rnd.nextInt(8);
                for (int i = 0; i < m; i++) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n)});
            }
            // The exercise forbids repeats and self loops, so such inputs are skipped.
            boolean ok = true;
            Set<String> seen = new HashSet<>();
            for (int[] e : list) if (e[0] == e[1] || !seen.add(e[0] + "," + e[1])) ok = false;
            if (!ok) continue;
            int[][] links = list.toArray(new int[0][]);
            int[] got = cycle(n, links);
            boolean want = exists(links, new boolean[links.length], 0, 0);
            if ((got.length > 0) != want) throw new AssertionError("existence " + tr);
            if (want && !valid(links, got)) throw new AssertionError("valid " + tr);
            if (!Arrays.equals(got, recursive(n, links))) throw new AssertionError("recursive " + tr);
        }
    }
}
```

#### Solution: [Vary] Eulerian Path (Author exercise)
<!-- id: ga-hier-euler-path -->

**Approach.**
The method first counts `out - in` for each vertex. Any count outside minus one to one rejects the graph, and so does a second vertex with count one. The start is the vertex with count one when it exists. Otherwise the start is the smallest vertex with an outgoing link, and a graph with no links returns `[0]`. The method stores the links in a head and next array pair, which are linked lists kept in plain arrays, and it fills them from the last link to the first so that the earliest link is read first. The walk then pops and pushes with an `int[]` stack.

The invariant is that the output, read backward, is a valid tail of the path made of consumed links. A vertex enters the output only after its links are gone. The start rule matters: when the graph is balanced, every vertex with a link lies on one cycle if the walk reaches all links, so the smallest such vertex is a safe start. The final length test rejects graphs whose links the walk cannot reach.

**Complexity.**
- **Time** is O(V + E), because the degree pass, the array fill and the walk each touch every link a constant number of times.
- **Space** is O(V + E) for the head, next and target arrays, the stack and the output.

```java run
import java.util.*;

public final class HierEulerPath {
    /**
     * Returns an Eulerian path whose start follows the degree rule, or an empty array.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: the output, read backward, is a valid tail of the path made of consumed links.
     */
    static int[] path(int n, int[][] links) {
        int m = links.length;
        // A graph with no links is the single vertex 0 by the exercise rule.
        if (m == 0) return new int[] {0};
        int[] balance = new int[n];
        for (int[] e : links) { balance[e[0]]++; balance[e[1]]--; }
        int start = -1;
        int plus = 0;
        // One pass rejects bad degrees and finds the vertex with one extra outgoing link.
        for (int v = 0; v < n; v++) {
            if (balance[v] > 1 || balance[v] < -1) return new int[0];
            if (balance[v] == 1) { plus++; start = v; }
        }
        if (plus > 1) return new int[0];
        // With all vertices balanced, the smallest vertex that has an outgoing link starts the path.
        if (start == -1) {
            start = n;
            for (int[] e : links) start = Math.min(start, e[0]);
        }
        // head[v] is the first link of v, next[i] is the following link, filled from the back to keep the order.
        int[] head = new int[n];
        Arrays.fill(head, -1);
        int[] next = new int[m];
        for (int i = m - 1; i >= 0; i--) {
            next[i] = head[links[i][0]];
            head[links[i][0]] = i;
        }
        int[] stack = new int[m + 1];
        int[] out = new int[m + 1];
        int top = 0, size = 0;
        stack[top++] = start;
        // Each pass consumes one link or records one vertex.
        while (top > 0) {
            int v = stack[top - 1];
            if (head[v] != -1) {
                // Taking the link and moving the head forward consumes it.
                int i = head[v];
                head[v] = next[i];
                stack[top++] = links[i][1];
            } else {
                // A vertex with no link left is recorded and removed.
                out[size++] = v;
                top--;
            }
        }
        if (size != m + 1) return new int[0];
        int[] res = new int[size];
        // The reversed output is the path in travel order.
        for (int i = 0; i < size; i++) res[i] = out[size - 1 - i];
        return res;
    }

    /** Brute force: reports whether some order of the links forms a path from the given start. */
    static boolean exists(int[][] links, boolean[] used, int v, int count) {
        if (count == links.length) return true;
        for (int i = 0; i < links.length; i++) {
            if (!used[i] && links[i][0] == v) {
                used[i] = true;
                boolean ok = exists(links, used, links[i][1], count + 1);
                used[i] = false;
                if (ok) return true;
            }
        }
        return false;
    }

    /** Checks that the route starts at the given vertex and uses every link exactly once. */
    static boolean valid(int[][] links, int[] route, int start) {
        if (route.length != links.length + 1 || route[0] != start) return false;
        boolean[] used = new boolean[links.length];
        for (int k = 0; k + 1 < route.length; k++) {
            int found = -1;
            for (int i = 0; i < links.length; i++) {
                if (!used[i] && links[i][0] == route[k] && links[i][1] == route[k + 1]) { found = i; break; }
            }
            if (found < 0) return false;
            used[found] = true;
        }
        return true;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(path(5, new int[][] {{2, 0}, {0, 1}, {1, 2}, {2, 3}, {3, 4}}), new int[] {2, 0, 1, 2, 3, 4})) throw new AssertionError("ex1");
        if (path(4, new int[][] {{1, 2}, {2, 3}, {1, 3}}).length != 0) throw new AssertionError("ex2");
        // A balanced graph starts at the smallest vertex with an outgoing link.
        if (!Arrays.equals(path(4, new int[][] {{3, 1}, {1, 3}}), new int[] {1, 3, 1})) throw new AssertionError("balanced");
        if (!Arrays.equals(path(3, new int[0][]), new int[] {0})) throw new AssertionError("empty");
        // Random graphs, half of them cut from a real walk so that a path usually exists.
        Random rnd = new Random(2502);
        for (int tr = 0; tr < 3000; tr++) {
            int n = 1 + rnd.nextInt(5);
            List<int[]> list = new ArrayList<>();
            if (rnd.nextBoolean()) {
                int v = rnd.nextInt(n), len = rnd.nextInt(7);
                for (int s = 0; s < len; s++) { int w = rnd.nextInt(n); list.add(new int[] {v, w}); v = w; }
                Collections.shuffle(list, rnd);
            } else {
                int m = rnd.nextInt(8);
                for (int i = 0; i < m; i++) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n)});
            }
            // The exercise forbids repeats and self loops, so such inputs are skipped.
            boolean ok = true;
            Set<String> seen = new HashSet<>();
            for (int[] e : list) if (e[0] == e[1] || !seen.add(e[0] + "," + e[1])) ok = false;
            if (!ok || list.isEmpty()) continue;
            int[][] links = list.toArray(new int[0][]);
            int[] got = path(n, links);
            // The oracle tries every vertex as a start, because the degree rule names only one of them.
            boolean want = false;
            for (int s = 0; s < n && !want; s++) want = exists(links, new boolean[links.length], s, 0);
            if ((got.length > 0) != want) throw new AssertionError("existence " + tr);
            if (want) {
                int[] bal = new int[n];
                for (int[] e : links) { bal[e[0]]++; bal[e[1]]--; }
                int start = -1;
                for (int v = 0; v < n; v++) if (bal[v] == 1) start = v;
                if (start == -1) { start = n; for (int[] e : links) start = Math.min(start, e[0]); }
                if (!valid(links, got, start)) throw new AssertionError("valid " + tr);
            }
        }
    }
}
```

#### Solution: [Boundary] Parallel Edges (Author exercise)
<!-- id: ga-hier-parallel-edges -->

**Approach.**
The method copies `count` into a working matrix `left`, because the input must stay unchanged. It checks that each row sum equals the matching column sum. Then it runs the stack walk. For the top vertex `v`, a pointer `col[v]` moves right past entries of `left[v]` that are zero. When the pointer stays inside the row, the method subtracts one from `left[v][col[v]]` and pushes that column. The pointer does not advance, because the same target may still hold more parallel links. When the pointer leaves the row, the method pops `v` and records it.

The invariant is that `left[u][v]` counts the links from `u` to `v` that are still unused, and the output, read backward, is a valid tail of the cycle. A yes or no entry for each pair would treat two parallel links as one, and the cycle would stop short. A self loop is a link from a vertex to itself, so the walk pushes the same vertex again and the row sum equals the column sum at that vertex. Taking the smallest column first makes the cycle the smallest in lexical order, which the oracle confirms.

**Complexity.**
- **Time** is O(n^2 + E), because copying and summing the matrix costs O(n^2), the pointers move at most n steps per row, and every link is pushed once.
- **Space** is O(n^2 + E) for the working matrix, the stack and the output.

```java run
import java.util.*;

public final class HierParallelEdges {
    /**
     * Returns the lexically smallest Eulerian cycle from vertex 0, or an empty array.
     * Time: O(n^2 + E). Space: O(n^2 + E).
     * Invariant: left[u][v] counts unused links, and the output, read backward, is a valid cycle tail.
     */
    static int[] cycle(int[][] count) {
        int n = count.length;
        // The working copy keeps the input unchanged.
        int[][] left = new int[n][];
        long total = 0;
        for (int u = 0; u < n; u++) left[u] = count[u].clone();
        // Row sums are out-degrees and column sums are in-degrees; they must match for every vertex.
        for (int u = 0; u < n; u++) {
            long out = 0, in = 0;
            for (int v = 0; v < n; v++) { out += count[u][v]; in += count[v][u]; }
            if (out != in) return new int[0];
            total += out;
        }
        int[] col = new int[n];
        int[] stack = new int[(int) total + 1];
        int[] rec = new int[(int) total + 1];
        int top = 0, size = 0;
        stack[top++] = 0;
        // Each pass pushes one link or records one vertex.
        while (top > 0) {
            int v = stack[top - 1];
            // Skip targets whose links are all used; the pointer only moves right.
            while (col[v] < n && left[v][col[v]] == 0) col[v]++;
            if (col[v] < n) {
                // One parallel link is consumed, and the pointer stays for the remaining copies.
                left[v][col[v]]--;
                stack[top++] = col[v];
            } else {
                // The row is empty, so the vertex is final.
                rec[size++] = v;
                top--;
            }
        }
        // A short record means some links are unreachable from vertex 0.
        if (size != total + 1) return new int[0];
        int[] res = new int[size];
        for (int i = 0; i < size; i++) res[i] = rec[size - 1 - i];
        return res;
    }

    /** Brute force: the first complete route found with the smallest target tried first is the smallest cycle. */
    static int[] brute(int[][] left, int v, int remaining, List<Integer> path) {
        // All links are used; the route must end at vertex 0.
        if (remaining == 0) return v == 0 ? path.stream().mapToInt(Integer::intValue).toArray() : null;
        for (int w = 0; w < left.length; w++) {
            if (left[v][w] > 0) {
                left[v][w]--;
                path.add(w);
                int[] r = brute(left, w, remaining - 1, path);
                path.remove(path.size() - 1);
                left[v][w]++;
                if (r != null) return r;
            }
        }
        return null;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(cycle(new int[][] {{1, 2}, {2, 0}}), new int[] {0, 0, 1, 0, 1, 0})) throw new AssertionError("ex1");
        if (cycle(new int[][] {{1, 0, 0}, {0, 0, 1}, {0, 1, 0}}).length != 0) throw new AssertionError("ex2");
        // The input matrix is not changed.
        int[][] keep = {{1, 2}, {2, 0}};
        cycle(keep);
        if (!Arrays.deepEquals(keep, new int[][] {{1, 2}, {2, 0}})) throw new AssertionError("mutated");
        // A graph with no links returns only vertex 0.
        if (!Arrays.equals(cycle(new int[][] {{0, 0}, {0, 0}}), new int[] {0})) throw new AssertionError("empty");
        // Random matrices built from closed walks plus noise, so both outcomes occur.
        Random rnd = new Random(2503);
        for (int tr = 0; tr < 3000; tr++) {
            int n = 1 + rnd.nextInt(4);
            int[][] c = new int[n][n];
            int walks = rnd.nextInt(3);
            for (int w = 0; w < walks; w++) {
                int v = 0, len = rnd.nextInt(4);
                for (int s = 0; s < len; s++) { int x = rnd.nextInt(n); c[v][x]++; v = x; }
                c[v][0]++;
            }
            if (rnd.nextInt(4) == 0) c[rnd.nextInt(n)][rnd.nextInt(n)]++;
            int total = 0;
            for (int[] row : c) for (int x : row) total += x;
            if (total > 9) continue;
            int[][] copy = new int[n][];
            for (int i = 0; i < n; i++) copy[i] = c[i].clone();
            int[] got = cycle(c);
            int[] want = total == 0 ? new int[] {0} : brute(copy, 0, total, new ArrayList<>(List.of(0)));
            if (want == null) want = new int[0];
            if (!Arrays.equals(got, want)) throw new AssertionError("random " + tr + " " + Arrays.toString(got) + " " + Arrays.toString(want));
        }
    }
}
```

#### Solution: [Recognize] Reconstruct Itinerary (LeetCode 332)
<!-- id: ga-hier-itinerary -->

**Approach.**
The method maps each airport to a `PriorityQueue` that orders its destinations from largest to smallest. Equal tickets enter the queue as separate entries, so repeats are consumed one by one. It counts `out - in` for each airport, and it returns an empty list when a count leaves the range minus one to one or when an airport with count one is not `JFK`. It then runs the stack walk from `JFK`, polling the largest destination of the top airport, and it records an airport when its queue is empty. A recorded list shorter than `tickets.length + 1` means some tickets are unreachable, so the method returns an empty list.

The invariant is that the recorded list, read backward, is a valid tail of the itinerary. Taking the largest destination first gives the largest itinerary for the same reason that the smallest first gives the smallest: the first dead end is the airport where the trip must end, and it is recorded first. The degree rule matters because a graph with a wrong start can still produce `E + 1` recorded airports that do not form a trip. The method reads `tickets` and never modifies it.

**Complexity.**
- **Time** is O(E log E), because each ticket enters and leaves a priority queue once.
- **Space** is O(V + E) for the queues, the stack and the recorded list.

```java run
import java.util.*;

public final class HierItinerary {
    /**
     * Returns the lexically largest itinerary from JFK that uses every ticket, or an empty list.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: the recorded list, read backward, is a valid tail of the itinerary.
     */
    static List<String> largest(String[][] tickets) {
        Map<String, PriorityQueue<String>> dest = new HashMap<>();
        Map<String, Integer> balance = new HashMap<>();
        // Every ticket joins the queue of its origin and shifts the degree difference.
        for (String[] t : tickets) {
            dest.computeIfAbsent(t[0], k -> new PriorityQueue<>(Comparator.reverseOrder())).add(t[1]);
            balance.merge(t[0], 1, Integer::sum);
            balance.merge(t[1], -1, Integer::sum);
        }
        // Only JFK may have one extra departure, and no airport may differ by more than one.
        for (Map.Entry<String, Integer> e : balance.entrySet()) {
            if (Math.abs(e.getValue()) > 1) return new ArrayList<>();
            if (e.getValue() == 1 && !e.getKey().equals("JFK")) return new ArrayList<>();
        }
        Deque<String> stack = new ArrayDeque<>();
        List<String> out = new ArrayList<>();
        stack.push("JFK");
        // Each pass takes one ticket or records one airport.
        while (!stack.isEmpty()) {
            PriorityQueue<String> q = dest.get(stack.peek());
            if (q != null && !q.isEmpty()) {
                // Polling consumes the largest remaining destination.
                stack.push(q.poll());
            } else {
                // An airport without tickets is final and joins the record.
                out.add(stack.pop());
            }
        }
        // A short record means some tickets are unreachable from JFK.
        if (out.size() != tickets.length + 1) return new ArrayList<>();
        Collections.reverse(out);
        return out;
    }

    /** Brute force: tries the largest destination first, so the first complete itinerary is the largest. */
    static List<String> brute(String[][] tickets, boolean[] used, String at, List<String> path) {
        if (path.size() == tickets.length + 1) return new ArrayList<>(path);
        String[] order = new String[tickets.length];
        int k = 0;
        for (int i = 0; i < tickets.length; i++) if (!used[i] && tickets[i][0].equals(at)) order[k++] = tickets[i][1];
        Arrays.sort(order, 0, k, Comparator.reverseOrder());
        for (int j = 0; j < k; j++) {
            if (j > 0 && order[j].equals(order[j - 1])) continue;
            int pick = -1;
            for (int i = 0; i < tickets.length; i++) {
                if (!used[i] && tickets[i][0].equals(at) && tickets[i][1].equals(order[j])) { pick = i; break; }
            }
            used[pick] = true;
            path.add(order[j]);
            List<String> r = brute(tickets, used, order[j], path);
            path.remove(path.size() - 1);
            used[pick] = false;
            if (r != null) return r;
        }
        return null;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        String[][] a = {{"JFK", "SFO"}, {"JFK", "ATL"}, {"SFO", "ATL"}, {"ATL", "JFK"}, {"ATL", "SFO"}};
        if (!largest(a).equals(List.of("JFK", "SFO", "ATL", "JFK", "ATL", "SFO"))) throw new AssertionError("ex1");
        if (!largest(new String[][] {{"JFK", "ATL"}, {"JFK", "SFO"}}).isEmpty()) throw new AssertionError("ex2");
        // The input is not changed.
        if (!a[0][1].equals("SFO") || a.length != 5) throw new AssertionError("mutated");
        // Equal tickets are consumed one at a time.
        if (!largest(new String[][] {{"JFK", "LAX"}, {"LAX", "JFK"}, {"JFK", "LAX"}, {"LAX", "JFK"}}).equals(List.of("JFK", "LAX", "JFK", "LAX", "JFK"))) throw new AssertionError("repeats");
        // Random tickets over a small airport set, half built from a real trip.
        String[] names = {"JFK", "ATL", "SFO", "LAX"};
        Random rnd = new Random(2504);
        for (int tr = 0; tr < 3000; tr++) {
            List<String[]> list = new ArrayList<>();
            if (rnd.nextBoolean()) {
                String v = "JFK";
                int len = 1 + rnd.nextInt(7);
                for (int s = 0; s < len; s++) { String w = names[rnd.nextInt(names.length)]; list.add(new String[] {v, w}); v = w; }
                Collections.shuffle(list, rnd);
            } else {
                int m = 1 + rnd.nextInt(7);
                for (int i = 0; i < m; i++) list.add(new String[] {names[rnd.nextInt(names.length)], names[rnd.nextInt(names.length)]});
            }
            String[][] tickets = list.toArray(new String[0][]);
            List<String> got = largest(tickets);
            List<String> want = brute(tickets, new boolean[tickets.length], "JFK", new ArrayList<>(List.of("JFK")));
            if (want == null) want = new ArrayList<>();
            if (!got.equals(want)) throw new AssertionError("random " + tr + " " + got + " " + want);
        }
    }
}
```
