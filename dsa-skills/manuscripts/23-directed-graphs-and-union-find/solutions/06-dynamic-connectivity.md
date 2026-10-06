<!-- solutions-for: 23-directed-graphs-and-union-find -->
### Solutions For Dynamic Connectivity

#### Solution: [Build] Online Connect And Query (Author exercise)
<!-- id: dg-online-connect-query -->

**Approach.**
The method keeps `parent` and `size` for the items and reads the events once, in order. For every event it first finds the representatives of both items. A question event appends whether the two representatives are equal. A link event returns early when they are equal. Otherwise it makes the smaller tree a child of the larger tree and adds the count.

The invariant is that before each event, two items share a representative exactly when a chain of earlier link events joins them. A question reads this state and never changes it, and a link changes it only by merging the two groups of its endpoints. An item is joined to itself, because `find(a) == find(a)`, which covers a question with `a == b`. The oracle answers each question with a fresh breadth-first search over the links that arrived before it.

**Complexity.**
- **Time** is O(e log n) for e events, because each event performs two finds of at most log2(n) steps.
- **Space** is O(n) for `parent` and `size`, plus one entry per question in the result.

```java run
import java.util.*;

public final class OnlineConnectQuery {
    /**
     * Answers each question event with the connectivity at that moment.
     * Time: O(e log n). Space: O(n).
     * Invariant: equal representatives mean a chain of earlier links exists.
     */
    static boolean[] answers(int n, int[][] events) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        List<Boolean> out = new ArrayList<>();
        // One pass over the events keeps the answers in input order.
        for (int[] ev : events) {
            int x = find(parent, ev[1]);
            int y = find(parent, ev[2]);
            // A question only reads the two representatives.
            if (ev[0] == 1) { out.add(x == y); continue; }
            // A link between items of one group changes nothing.
            if (x == y) continue;
            // The smaller tree goes under the larger tree.
            if (size[x] < size[y]) { int t = x; x = y; y = t; }
            parent[y] = x;
            size[x] += size[y];
        }
        boolean[] res = new boolean[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    static int find(int[] parent, int x) {
        // Walk up until an item is its own parent.
        while (parent[x] != x) x = parent[x];
        return x;
    }

    /** Oracle: for each question, a breadth-first search over all links seen so far. */
    static boolean[] oracle(int n, int[][] events) {
        List<int[]> links = new ArrayList<>();
        List<Boolean> out = new ArrayList<>();
        for (int[] ev : events) {
            if (ev[0] == 0) { links.add(ev); continue; }
            boolean[] seen = new boolean[n];
            ArrayDeque<Integer> queue = new ArrayDeque<>();
            queue.add(ev[1]);
            seen[ev[1]] = true;
            while (!queue.isEmpty()) {
                int v = queue.poll();
                for (int[] l : links) {
                    int w = l[1] == v ? l[2] : l[2] == v ? l[1] : -1;
                    if (w >= 0 && !seen[w]) { seen[w] = true; queue.add(w); }
                }
            }
            out.add(seen[ev[2]]);
        }
        boolean[] res = new boolean[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(answers(5, new int[][] {{1, 0, 1}, {0, 0, 1}, {0, 1, 2}, {1, 0, 2}, {1, 3, 4}}), new boolean[] {false, true, false})) throw new AssertionError("ex1");
        if (!Arrays.equals(answers(4, new int[][] {{0, 3, 2}, {1, 2, 3}, {1, 0, 0}, {0, 0, 3}, {1, 2, 0}}), new boolean[] {true, true, true})) throw new AssertionError("ex2");
        // An empty event list gives an empty answer array.
        if (answers(1, new int[0][]).length != 0) throw new AssertionError("empty");
        // Random event streams must match the search oracle.
        Random rnd = new Random(2309);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(9);
            int m = rnd.nextInt(25);
            int[][] ev = new int[m][];
            for (int k = 0; k < m; k++) ev[k] = new int[] {rnd.nextInt(2), rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(answers(n, ev), oracle(n, ev))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Provinces After Each Edge (LeetCode 547)
<!-- id: dg-provinces-per-edge -->

**Approach.**
The usual solution of this problem reads a matrix and returns one number at the end. This version keeps a running count `provinces` that starts at n and records it after every link. For each link the method finds both representatives. Equal representatives, including the case `a == b`, leave the count unchanged. Different representatives merge the two trees and lower the count by one. The method stores the count in the answer array at the position of the link.

The invariant is that after k links, `provinces` equals n minus the number of merges. That value is the number of connected sets of cities in the first k links. A link can lower the count by at most one, because it joins at most two sets. The oracle recounts the sets after every prefix with a depth-first search, which shares no state with the incremental method.

**Complexity.**
- **Time** is O(m log n) for m links, because each link costs two finds of at most log2(n) steps.
- **Space** is O(n) for the arrays, plus O(m) for the result.

```java run
import java.util.*;

public final class ProvincesPerEdge {
    /**
     * Returns the number of provinces after each prefix of the link list.
     * Time: O(m log n). Space: O(n + m).
     * Invariant: provinces = n minus the merges done so far.
     */
    static int[] counts(int n, int[][] links) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        int provinces = n;
        int[] out = new int[links.length];
        // The loop index doubles as the position in the answer.
        for (int k = 0; k < links.length; k++) {
            int x = find(parent, links[k][0]);
            int y = find(parent, links[k][1]);
            // Different representatives mean the link joins two provinces.
            if (x != y) {
                if (size[x] < size[y]) { int t = x; x = y; y = t; }
                parent[y] = x;
                size[x] += size[y];
                provinces--;
            }
            // The count is recorded after every link, merged or not.
            out[k] = provinces;
        }
        return out;
    }

    static int find(int[] parent, int x) {
        // Climb to the representative.
        while (parent[x] != x) x = parent[x];
        return x;
    }

    /** Oracle: recount connected sets from scratch for every prefix. */
    static int[] oracle(int n, int[][] links) {
        int[] out = new int[links.length];
        for (int k = 0; k < links.length; k++) {
            boolean[][] adj = new boolean[n][n];
            for (int j = 0; j <= k; j++) { adj[links[j][0]][links[j][1]] = true; adj[links[j][1]][links[j][0]] = true; }
            boolean[] seen = new boolean[n];
            int c = 0;
            for (int s = 0; s < n; s++) {
                if (seen[s]) continue;
                c++;
                Deque<Integer> stack = new ArrayDeque<>();
                stack.push(s);
                seen[s] = true;
                while (!stack.isEmpty()) {
                    int v = stack.pop();
                    for (int w = 0; w < n; w++) if (adj[v][w] && !seen[w]) { seen[w] = true; stack.push(w); }
                }
            }
            out[k] = c;
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(counts(4, new int[][] {{0, 1}, {2, 3}, {1, 0}, {1, 2}}), new int[] {3, 2, 2, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(counts(3, new int[][] {{0, 0}, {1, 2}}), new int[] {3, 2})) throw new AssertionError("ex2");
        // Random link lists must match the recount oracle.
        Random rnd = new Random(2310);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(9);
            int m = rnd.nextInt(15);
            int[][] links = new int[m][];
            for (int k = 0; k < m; k++) links[k] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(counts(n, links), oracle(n, links))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Duplicate Union (Author exercise)
<!-- id: dg-duplicate-union -->

**Approach.**
The method keeps `groups`, which starts at n, and `effective`, which starts at 0. For each pair it finds both representatives. When they are equal, the pair is a repeat, a reversal, a cycle edge or a pair with `a == b`. The method skips it without a write. When they differ, the method merges the trees, lowers `groups` and raises `effective` by one.

The invariant is that `groups + effective == n` after every pair. Both counters change only in the merge branch, and each merge moves one unit from one counter to the other. The skip branch touches neither, so a duplicate cannot disturb the sum. The code asserts this sum on random input. The oracle labels the items and relabels one whole group for every merge, so it shares no code with the tree walk.

**Complexity.**
- **Time** is O(m log n), because each pair costs two finds of at most log2(n) steps.
- **Space** is O(n) for `parent` and `size`.

```java run
import java.util.*;

public final class DuplicateUnion {
    /**
     * Returns {final group count, number of effective links}.
     * Time: O(m log n). Space: O(n).
     * Invariant: groups + effective equals n after every pair.
     */
    static int[] summary(int n, int[][] pairs) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        int groups = n, effective = 0;
        for (int[] p : pairs) {
            int x = find(parent, p[0]);
            int y = find(parent, p[1]);
            // A second arrival of a pair finds equal representatives and stops here.
            if (x == y) continue;
            if (size[x] < size[y]) { int t = x; x = y; y = t; }
            parent[y] = x;
            size[x] += size[y];
            // One merge moves one unit between the two counters.
            groups--;
            effective++;
        }
        return new int[] {groups, effective};
    }

    static int find(int[] parent, int x) {
        // Climb to the representative.
        while (parent[x] != x) x = parent[x];
        return x;
    }

    /** Oracle: relabels every member of one group on each effective link. */
    static int[] oracle(int n, int[][] pairs) {
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        int effective = 0;
        for (int[] p : pairs) {
            int la = label[p[0]], lb = label[p[1]];
            if (la == lb) continue;
            effective++;
            for (int v = 0; v < n; v++) if (label[v] == lb) label[v] = la;
        }
        return new int[] {new HashSet<>(Arrays.stream(label).boxed().toList()).size(), effective};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(summary(5, new int[][] {{0, 1}, {1, 0}, {0, 1}, {3, 3}, {3, 4}}), new int[] {3, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(summary(3, new int[][] {{2, 1}, {1, 2}, {0, 2}, {2, 0}, {0, 1}}), new int[] {1, 2})) throw new AssertionError("ex2");
        // Random pairs with many repeats must match the relabeling oracle, and the sum must equal n.
        Random rnd = new Random(2311);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(25);
            int[][] pairs = new int[m][];
            for (int k = 0; k < m; k++) pairs[k] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[] got = summary(n, pairs);
            if (!Arrays.equals(got, oracle(n, pairs))) throw new AssertionError("random " + t);
            if (got[0] + got[1] != n) throw new AssertionError("sum " + t);
        }
    }
}
```

#### Solution: [Recognize] Accounts Merge (LeetCode 721)
<!-- id: dg-accounts-merge -->

**Approach.**
The method treats each account as an item and keeps a union by size structure over the account indices. A map `owner` stores, for each email, the first account that listed it. When a later account lists an email that already has an owner, the method merges the two account indices. A shared email proves that both accounts belong to one person. Otherwise it records the current account as the owner.

After all accounts are read, the method computes `find(i)` for every account. This representative is the group key. It adds the emails of account i to a sorted set that belongs to that key. Finally, each set becomes one result list that starts with the name of the representative account, followed by the emails in ascending order.

The invariant is that two accounts share a representative exactly when a chain of shared emails joins them. A name never merges accounts, so two people called Kim stay separate unless an email links them. The oracle builds an explicit graph that joins every pair of accounts with a common email and collects connected sets with a depth-first search.

**Complexity.**
- **Time** is O(L log n + L log L) for L emails in total, because each email costs one map access and at most one union. The sorted sets add the L log L term.
- **Space** is O(L) for the map, the sets and the result.

```java run
import java.util.*;

public final class AccountsMerge {
    /**
     * Returns merged accounts: name followed by sorted distinct emails.
     * Time: O(L log L). Space: O(L).
     * Invariant: equal representatives mean a chain of shared emails exists.
     */
    static List<List<String>> merge(List<List<String>> accounts) {
        int n = accounts.size();
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        // owner remembers the first account that listed each email.
        Map<String, Integer> owner = new HashMap<>();
        for (int i = 0; i < n; i++) {
            for (int e = 1; e < accounts.get(i).size(); e++) {
                String email = accounts.get(i).get(e);
                Integer first = owner.putIfAbsent(email, i);
                // A repeated email proves both accounts belong to one person.
                if (first != null) union(parent, size, i, first);
            }
        }
        // Group the emails under the final representative of their account.
        Map<Integer, TreeSet<String>> byKey = new HashMap<>();
        for (int i = 0; i < n; i++) {
            TreeSet<String> set = byKey.computeIfAbsent(find(parent, i), k -> new TreeSet<>());
            set.addAll(accounts.get(i).subList(1, accounts.get(i).size()));
        }
        List<List<String>> result = new ArrayList<>();
        // Each group becomes one list that starts with the name.
        for (Map.Entry<Integer, TreeSet<String>> g : byKey.entrySet()) {
            List<String> row = new ArrayList<>();
            row.add(accounts.get(g.getKey()).get(0));
            row.addAll(g.getValue());
            result.add(row);
        }
        return result;
    }

    static int find(int[] parent, int x) {
        // Climb to the representative.
        while (parent[x] != x) x = parent[x];
        return x;
    }

    static void union(int[] parent, int[] size, int a, int b) {
        int x = find(parent, a), y = find(parent, b);
        if (x == y) return;
        if (size[x] < size[y]) { int t = x; x = y; y = t; }
        parent[y] = x;
        size[x] += size[y];
    }

    /** Oracle: join every pair of accounts with a common email, then depth-first search. */
    static List<List<String>> oracle(List<List<String>> accounts) {
        int n = accounts.size();
        boolean[][] adj = new boolean[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                for (String e : accounts.get(i).subList(1, accounts.get(i).size()))
                    if (accounts.get(j).subList(1, accounts.get(j).size()).contains(e)) adj[i][j] = true;
        boolean[] seen = new boolean[n];
        List<List<String>> out = new ArrayList<>();
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            TreeSet<String> emails = new TreeSet<>();
            Deque<Integer> stack = new ArrayDeque<>();
            stack.push(s);
            seen[s] = true;
            while (!stack.isEmpty()) {
                int v = stack.pop();
                emails.addAll(accounts.get(v).subList(1, accounts.get(v).size()));
                for (int w = 0; w < n; w++) if (adj[v][w] && !seen[w]) { seen[w] = true; stack.push(w); }
            }
            List<String> row = new ArrayList<>();
            row.add(accounts.get(s).get(0));
            row.addAll(emails);
            out.add(row);
        }
        return out;
    }

    /** Sorts the result lists so that two results compare equal in any order. */
    static List<String> normalize(List<List<String>> lists) {
        List<String> keys = new ArrayList<>();
        for (List<String> l : lists) keys.add(String.join(",", l));
        Collections.sort(keys);
        return keys;
    }

    static List<List<String>> acc(String[]... rows) {
        List<List<String>> out = new ArrayList<>();
        for (String[] r : rows) out.add(new ArrayList<>(Arrays.asList(r)));
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        List<List<String>> in1 = acc(new String[] {"Ana", "a@x.com", "b@x.com"}, new String[] {"Ben", "c@x.com"},
            new String[] {"Ana", "b@x.com", "d@x.com"}, new String[] {"Ana", "e@x.com"});
        List<List<String>> out1 = acc(new String[] {"Ana", "a@x.com", "b@x.com", "d@x.com"}, new String[] {"Ben", "c@x.com"}, new String[] {"Ana", "e@x.com"});
        if (!normalize(merge(in1)).equals(normalize(out1))) throw new AssertionError("ex1");
        List<List<String>> in2 = acc(new String[] {"Kim", "k1@m.com", "k2@m.com"}, new String[] {"Kim", "k3@m.com"},
            new String[] {"Kim", "k4@m.com", "k3@m.com"}, new String[] {"Kim", "k2@m.com", "k4@m.com"}, new String[] {"Kim", "z@m.com"});
        List<List<String>> out2 = acc(new String[] {"Kim", "k1@m.com", "k2@m.com", "k3@m.com", "k4@m.com"}, new String[] {"Kim", "z@m.com"});
        if (!normalize(merge(in2)).equals(normalize(out2))) throw new AssertionError("ex2");
        // The input lists stay unchanged.
        if (in2.get(0).size() != 3 || in2.size() != 5) throw new AssertionError("input changed");
        // Random accounts: each name owns a pool of four emails, so one email has one name.
        Random rnd = new Random(2312);
        String[] names = {"A", "B", "C"};
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(8);
            List<List<String>> accounts = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                int p = rnd.nextInt(3);
                List<String> row = new ArrayList<>();
                row.add(names[p]);
                int k = 1 + rnd.nextInt(3);
                for (int j = 0; j < k; j++) row.add(names[p].toLowerCase() + rnd.nextInt(4) + "@m.com");
                accounts.add(row);
            }
            if (!normalize(merge(accounts)).equals(normalize(oracle(accounts)))) throw new AssertionError("random " + t);
        }
    }
}
```
