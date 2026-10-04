<!-- solutions-for: 04-find-compression -->
### Find Compression

#### Solution: [Build] Follow Parents To Root (Author exercise)
<!-- id: ug-follow-root -->

**Approach.** Start at `x`, and while the slot at the current member differs from the member itself, step to the slot's value and add one to a counter. The loop reads and never writes, so the argument array is untouched. The oracle works from the other end: it builds a children list for every member, then walks down from each root by breadth, labelling every descendant with its root and its depth, and the two must agree for every member of random forests that are shuffled so that parents are not always smaller. The run also checks the Java claims from the lesson. A recursive `find` that writes `parent[x] = find(parent[x])` overflows the stack on a line of a million cards when the thread has a 512 KB stack, the iterative version answers on the same line, and the second iterative call starts one hop from the top once the line has been compressed. It also asserts the false friend: after compression, the hop count from the bottom of a five-card line falls from 4 to 1, so the original line cannot be read back.

**Complexity.** One call follows at most one link per member on the line, which is O(n) time in the worst case and O(1) extra space; a forest in which all lines are short makes it close to constant.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FollowRootSolution {
    static int[] solve(int[] parent, int x) {
        int hops = 0;
        while (parent[x] != x) {
            x = parent[x];
            hops++;
        }
        return new int[] {x, hops};
    }

    static int[][] oracle(int[] parent) {
        int n = parent.length;
        List<List<Integer>> kids = new ArrayList<>();
        for (int i = 0; i < n; i++) kids.add(new ArrayList<>());
        for (int i = 0; i < n; i++) if (parent[i] != i) kids.get(parent[i]).add(i);
        int[][] out = new int[n][];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            if (parent[i] == i) {
                out[i] = new int[] {i, 0};
                queue.add(i);
            }
        }
        while (!queue.isEmpty()) {
            int v = queue.poll();
            for (int k : kids.get(v)) {
                out[k] = new int[] {out[v][0], out[v][1] + 1};
                queue.add(k);
            }
        }
        return out;
    }

    static int recursiveFind(int[] parent, int x) {
        if (parent[x] != x) parent[x] = recursiveFind(parent, parent[x]);
        return parent[x];
    }

    static int[] chain(int n) {
        int[] p = new int[n];
        for (int i = 1; i < n; i++) p[i] = i - 1;
        return p;
    }

    static int[] hopsAfterOneFind(int[] parent, int x) {
        int root = x;
        while (parent[root] != root) root = parent[root];
        while (parent[x] != root) {
            int next = parent[x];
            parent[x] = root;
            x = next;
        }
        return solve(parent, x);
    }

    public static void main(String[] args) throws Exception {
        if (!Arrays.equals(solve(new int[] {0, 0, 1, 2, 2, 5}, 3), new int[] {0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {0, 0, 2, 2, 3, 3}, 5), new int[] {2, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[] {0}, 0), new int[] {0, 0})) throw new AssertionError("single member");

        Random rnd = new Random(23401);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(30);
            int[] order = new int[n];
            for (int i = 0; i < n; i++) order[i] = i;
            for (int i = n - 1; i > 0; i--) {
                int j = rnd.nextInt(i + 1);
                int tmp = order[i]; order[i] = order[j]; order[j] = tmp;
            }
            int[] parent = new int[n];
            for (int i = 0; i < n; i++) {
                int m = order[i];
                parent[m] = (i == 0 || rnd.nextInt(5) == 0) ? m : order[rnd.nextInt(i)];
            }
            int[] copy = parent.clone();
            int[][] want = oracle(parent);
            for (int x = 0; x < n; x++) {
                if (!Arrays.equals(solve(parent, x), want[x])) throw new AssertionError("random " + t + " member " + x);
            }
            if (!Arrays.equals(copy, parent)) throw new AssertionError("array modified");
        }

        final int big = 1_000_000;
        final boolean[] overflowed = {false};
        final int[] iterativeRoot = {-1};
        final int[] secondHops = {-1};
        Thread worker = new Thread(null, () -> {
            try {
                recursiveFind(chain(big), big - 1);
            } catch (StackOverflowError e) {
                overflowed[0] = true;
            }
            int[] line = chain(big);
            int[] first = solve(line, big - 1);
            iterativeRoot[0] = first[0];
            if (first[1] != big - 1) iterativeRoot[0] = -2;
            int[] again = chain(big);
            secondHops[0] = hopsAfterOneFind(again, big - 1)[1];
        }, "deep-chain", 512 * 1024);
        worker.start();
        worker.join();
        if (!overflowed[0]) throw new AssertionError("recursive find should overflow on a million-card line");
        if (iterativeRoot[0] != 0) throw new AssertionError("iterative walk failed: " + iterativeRoot[0]);
        if (secondHops[0] != 1) throw new AssertionError("second find should be one hop");

        int[] line = chain(5);
        if (solve(line, 4)[1] != 4) throw new AssertionError("line before compression");
        hopsAfterOneFind(line, 4);
        if (solve(line, 4)[1] != 1) throw new AssertionError("false friend: the line must be lost");
    }
}
```

#### Solution: [Vary] Compress A Chain (Author exercise)
<!-- id: ug-compress-chain -->

**Approach.** Clone the array first, then climb from `x` to the root and walk the same line a second time. On that second walk, save the next member, point the current slot at the root, and move on, stopping when a slot already names the root. Members not on the line are never visited, so their slots stay as given. The oracle is a recursive version of the same idea, `parent[x] = find(parent[x])`, run on a clone of every random forest of up to 30 members, which writes in the opposite order but must leave the same array. A second check collects the line as a set with a plain climb and verifies member by member that exactly those on it point at the root and everyone else matches the input. The run also shows that plain assignment `int[] alias = input` shares storage, which is why the clone is needed, and that the argument stays as it was.

**Complexity.** The two walks each read the line once, so the time is O(n) for the clone plus the line length, with O(n) extra space for the returned copy.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class CompressChainSolution {
    static int[] solve(int[] parent, int x) {
        int[] p = parent.clone();
        int root = x;
        while (p[root] != root) root = p[root];
        while (p[x] != root) {
            int next = p[x];
            p[x] = root;
            x = next;
        }
        return p;
    }

    static int oracleFind(int[] p, int x) {
        if (p[x] != x) p[x] = oracleFind(p, p[x]);
        return p[x];
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[] {0, 0, 1, 2, 3}, 4), new int[] {0, 0, 0, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {0, 0, 0, 1, 1, 3, 4}, 6), new int[] {0, 0, 0, 1, 0, 3, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[] {0}, 0), new int[] {0})) throw new AssertionError("lone root");
        if (!Arrays.equals(solve(new int[] {0, 0, 1}, 0), new int[] {0, 0, 1})) throw new AssertionError("root query changes nothing");

        int[] original = {0, 0, 1};
        int[] alias = original;
        alias[2] = 2;
        if (original[2] != 2) throw new AssertionError("an array variable shares storage");
        int[] snapshot = original.clone();
        snapshot[2] = 0;
        if (original[2] != 2) throw new AssertionError("clone must be independent");

        Random rnd = new Random(23402);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(30);
            int[] parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = (i == 0 || rnd.nextInt(6) == 0) ? i : rnd.nextInt(i);
            int x = rnd.nextInt(n);
            int[] copy = parent.clone();
            int[] got = solve(parent, x);
            int[] want = parent.clone();
            oracleFind(want, x);
            if (!Arrays.equals(got, want)) throw new AssertionError("random " + t + " " + Arrays.toString(got));
            Set<Integer> onLine = new HashSet<>();
            int v = x;
            while (parent[v] != v) {
                onLine.add(v);
                v = parent[v];
            }
            for (int i = 0; i < n; i++) {
                int expect = onLine.contains(i) ? v : parent[i];
                if (got[i] != expect) throw new AssertionError("member " + i + " in trial " + t);
            }
            if (!Arrays.equals(copy, parent)) throw new AssertionError("input modified");
        }
    }
}
```

#### Solution: [Boundary] Singleton Components (Author exercise)
<!-- id: ug-singletons -->

**Approach.** Every member begins as its own root. For each pair, find both roots and link one to the other when they differ, so a pair naming one member twice, or a pair repeated, finds equal roots and does nothing. Afterwards, find the root of every member and tally how many members each root has. The members that are alone are the roots whose tally is exactly 1. The oracle never builds a forest: it marks a member as joined when some pair names it together with a different member, and counts the unmarked ones. Both are checked on random inputs with plenty of self pairs and repeats, plus fixed cases for one member, no pairs at all, and a pair of the same member twice. The run also shows the trap behind the stated contract: counting roots instead of groups of size one gives a different answer whenever any group has two or more members.

**Complexity.** With E pairs and n members the finds stay short because of the rewriting, giving close to O(n + E) time, though the rigorous bound is slightly larger, and the space is two `int[]` of size n.

```java run
import java.util.Random;

public final class SingletonsSolution {
    static int find(int[] parent, int x) {
        int root = x;
        while (parent[root] != root) root = parent[root];
        while (parent[x] != root) {
            int next = parent[x];
            parent[x] = root;
            x = next;
        }
        return root;
    }

    static int solve(int n, int[][] edges) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int[] e : edges) {
            int a = find(parent, e[0]), b = find(parent, e[1]);
            if (a != b) parent[a] = b;
        }
        int[] tally = new int[n];
        for (int i = 0; i < n; i++) tally[find(parent, i)]++;
        int alone = 0;
        for (int i = 0; i < n; i++) if (tally[i] == 1) alone++;
        return alone;
    }

    static int countRoots(int n, int[][] edges) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int[] e : edges) {
            int a = find(parent, e[0]), b = find(parent, e[1]);
            if (a != b) parent[a] = b;
        }
        int roots = 0;
        for (int i = 0; i < n; i++) if (parent[i] == i) roots++;
        return roots;
    }

    static int oracle(int n, int[][] edges) {
        boolean[] joined = new boolean[n];
        for (int[] e : edges) {
            if (e[0] != e[1]) {
                joined[e[0]] = true;
                joined[e[1]] = true;
            }
        }
        int alone = 0;
        for (boolean j : joined) if (!j) alone++;
        return alone;
    }

    public static void main(String[] args) {
        if (solve(5, new int[][] {{0, 1}, {2, 2}}) != 3) throw new AssertionError("example 1");
        if (solve(4, new int[][] {{1, 2}, {2, 1}, {3, 3}}) != 2) throw new AssertionError("example 2");
        if (solve(1, new int[][] {}) != 1) throw new AssertionError("one member");
        if (solve(6, new int[][] {}) != 6) throw new AssertionError("no pairs");
        if (solve(2, new int[][] {{0, 1}, {1, 0}, {0, 1}}) != 0) throw new AssertionError("repeated pair");
        if (countRoots(5, new int[][] {{0, 1}, {2, 2}}) == 3) throw new AssertionError("false friend: roots are not singletons");

        Random rnd = new Random(23403);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(12);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = edges[i].clone();
            int got = solve(n, edges), want = oracle(n, edges);
            if (got != want) throw new AssertionError("random " + t + ": " + got + " vs " + want);
            if (!java.util.Arrays.deepEquals(copy, edges)) throw new AssertionError("edges modified");
        }
    }
}
```

#### Solution: [Recognize] Number Of Provinces (LeetCode 547)
<!-- id: ug-provinces -->

**Approach.** Give every city its own root, then read the upper triangle of the matrix and, for each 1 off the diagonal, link the two roots when they differ. At the end, find every city's root and tally members per root: the number of roots with a nonzero tally is the number of provinces and the largest tally is the size of the biggest. Always ask `find` for a city's group; a slot read directly can be stale after later links. The oracle is a Floyd-Warshall style closure on a copy of the matrix: for every middle city, any pair that reaches the middle becomes reachable, and the groups are then read from the rows. The run compares both answers on random symmetric matrices of one to eight cities and also demonstrates the false friend, counting distinct values in the raw array, which reports two provinces for a three-city line that is one.

**Complexity.** Reading the matrix is O(n^2) and dominates, since each of the O(n^2) links costs a nearly constant find, and the extra space is the two `int[]` of size n; the closure oracle needs O(n^3).

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class ProvincesSolution {
    static int find(int[] parent, int x) {
        int root = x;
        while (parent[root] != root) root = parent[root];
        while (parent[x] != root) {
            int next = parent[x];
            parent[x] = root;
            x = next;
        }
        return root;
    }

    static int[] solve(int[][] isConnected) {
        int n = isConnected.length;
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (isConnected[i][j] == 1) {
                    int a = find(parent, i), b = find(parent, j);
                    if (a != b) parent[a] = b;
                }
            }
        }
        int[] tally = new int[n];
        for (int i = 0; i < n; i++) tally[find(parent, i)]++;
        int count = 0, largest = 0;
        for (int t : tally) {
            if (t > 0) count++;
            largest = Math.max(largest, t);
        }
        return new int[] {count, largest};
    }

    static int[] oracle(int[][] m) {
        int n = m.length;
        boolean[][] reach = new boolean[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++) reach[i][j] = i == j || m[i][j] == 1;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        Set<String> groups = new HashSet<>();
        int largest = 0;
        for (int i = 0; i < n; i++) {
            groups.add(Arrays.toString(reach[i]));
            int size = 0;
            for (int j = 0; j < n; j++) if (reach[i][j]) size++;
            largest = Math.max(largest, size);
        }
        return new int[] {groups.size(), largest};
    }

    static int distinctRawSlots(int[][] isConnected) {
        int n = isConnected.length;
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                if (isConnected[i][j] == 1) {
                    int a = find(parent, i), b = find(parent, j);
                    if (a != b) parent[a] = b;
                }
        Set<Integer> values = new HashSet<>();
        for (int p : parent) values.add(p);
        return values.size();
    }

    public static void main(String[] args) {
        int[][] e1 = {{1, 1, 0}, {1, 1, 0}, {0, 0, 1}};
        int[][] e2 = {{1, 0, 0, 1, 0}, {0, 1, 1, 0, 0}, {0, 1, 1, 1, 0}, {1, 0, 1, 1, 0}, {0, 0, 0, 0, 1}};
        if (!Arrays.equals(solve(e1), new int[] {2, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(e2), new int[] {2, 4})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[][] {{1}}), new int[] {1, 1})) throw new AssertionError("one city");
        if (!Arrays.equals(solve(new int[][] {{1, 0}, {0, 1}}), new int[] {2, 1})) throw new AssertionError("two lonely cities");
        int[][] line = {{1, 1, 0}, {1, 1, 1}, {0, 1, 1}};
        if (!Arrays.equals(solve(line), new int[] {1, 3})) throw new AssertionError("three-city line");
        if (distinctRawSlots(line) == 1) throw new AssertionError("false friend: raw slots must overcount");

        Random rnd = new Random(23404);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] m = new int[n][n];
            int percent = 5 + rnd.nextInt(40);
            for (int i = 0; i < n; i++) {
                m[i][i] = 1;
                for (int j = i + 1; j < n; j++) m[i][j] = m[j][i] = rnd.nextInt(100) < percent ? 1 : 0;
            }
            int[][] copy = new int[n][];
            for (int i = 0; i < n; i++) copy[i] = m[i].clone();
            int[] got = solve(m), want = oracle(m);
            if (!Arrays.equals(got, want)) throw new AssertionError("random " + t + Arrays.toString(got) + Arrays.toString(want));
            if (!Arrays.deepEquals(copy, m)) throw new AssertionError("matrix modified");
        }
    }
}
```
