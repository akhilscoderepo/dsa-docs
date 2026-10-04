<!-- lesson-kind: combination -->
<!-- lesson-id: grid-and-graph-traversal -->
## Grid And Graph Traversal

<!-- stage: context -->
### The Steward Of Kawane Hill

Kawane Hill is cut into rice terraces that circle it like the rings of a cone. Each ring is a row of paddies, and because the ring closes on itself, the last paddy of a row touches the first. The steward keeps a night ledger that lists the crop planted in each paddy as a digit, and a bank of earth separates every pair of neighbours. A blight starts in one paddy and creeps through the banks into any neighbour that grows the same crop. It cannot jump a paddy that grows something else.

Before dawn the steward must answer four questions from the ledger alone. Which paddies fall to a blight that starts here? How many separate patches of one crop are there? How big is the biggest patch? And can the whole map be copied for the valley office without tying the copy to the original?

<!-- stage: contributions -->
### What Each Piece Brings

The grid brings vertices that nobody has to store. A paddy is a pair of row and column, a packed number turns the pair into one index, and a short list of shifts produces the neighbours on demand, so a map of a million paddies costs no edge list. It also brings its own boundary rules, such as the rows that end and the columns that may wrap.

The graph traversal brings ownership of progress. One table says which vertices have been claimed, an outer scan starts a fresh search only at an unclaimed vertex, and a search spends its time only on vertices that nobody owns yet. From the earlier cloning lesson it brings the same idea for objects, where a map keyed by identity plays the part of that table.

The recognition cue is a question about patches, sizes or copies where the neighbours are implied by position or by pointers and no vertex may be worked on twice.

<!-- stage: naive -->
### Start A Fresh Search At Every Paddy

The direct method treats every paddy as a separate question. For each paddy that grows the crop in question, run a brand new search with a private table of marks, and note the smallest position the search reaches. The paddy is the first of its patch exactly when it is that smallest position, so the number of such paddies is the number of patches.

```java
static int patchesByRestart(String[] beds) {
    int rows = beds.length, cols = beds[0].length(), count = 0;
    for (int start = 0; start < rows * cols; start++) {
        if (beds[start / cols].charAt(start % cols) != '1') continue;
        boolean[] mine = new boolean[rows * cols];
        int[] stack = new int[rows * cols];
        int top = 0, smallest = start;
        stack[top++] = start;
        mine[start] = true;
        while (top > 0) {
            int at = stack[--top];
            smallest = Math.min(smallest, at);
            int r = at / cols, c = at % cols;
            int[][] near = {{r - 1, c}, {r + 1, c}, {r, c - 1}, {r, c + 1}};
            for (int[] p : near) {
                if (p[0] < 0 || p[0] >= rows || p[1] < 0 || p[1] >= cols) continue;
                int to = p[0] * cols + p[1];
                if (!mine[to] && beds[p[0]].charAt(p[1]) == '1') { mine[to] = true; stack[top++] = to; }
            }
        }
        if (smallest == start) count++;
    }
    return count;
}
```

The method is correct, since a search that runs to the end of its patch sees every position of that patch, so the smallest of them is the same whichever paddy the search began from.

<!-- stage: bottleneck -->
### Every Search Forgets The Others

A patch of k paddies is searched k times, once from each of its paddies, and each search touches all k of them. For a map of N paddies in a single patch the cost is O(N^2) time, and it also allocates N tables of N marks, so memory churns as well. On a hill of a thousand rings with a thousand paddies each, that is a million searches over up to a million paddies, around a trillion steps, to learn one number. Every search starts from nothing, so the work that one search did for its patch is thrown away the moment the next search begins.

The same waste hides in the other questions. Measuring the biggest patch would repeat every measurement k times, and copying the map by starting a fresh copy from each node would build k copies of the same node. What is needed is a single record of progress that survives from one search to the next, so that a paddy examined once is never examined again, and the total cost is O(N) for the whole map.

<!-- stage: insight -->
### One Table Owns Every Paddy

Give each paddy one **cell id**, `r * cols + c`, and recover the row and column by `id / cols` and `id % cols`. The id is the vertex. A **delta table** of shifts, such as right, down, left and up, then turns an id into its neighbours without any stored edges. A contract that wants diagonals simply uses eight entries instead of four, and a ring that wraps replaces the column test by `(nc + cols) % cols` while keeping the row test. Only the contract changes; the traversal around it is untouched.

The step that removes the waste is **shared visited**: one boolean array, allocated once, that every search of the run reads and writes. A search claims a cell by marking it at the moment the cell is pushed, and it never pushes a cell that is already marked. When the first search ends, every cell of its patch is marked, so a later search that stumbles onto that patch can only find walls. The outer scan then walks the ids in order and starts a search only at an eligible cell that is still unmarked. That single rule counts patches, since each start is a new patch. It measures them, since each search returns the number of cells it claimed. And it recolours them, since the marked cells are exactly the reached cells.

The same table moves from coordinates to objects. When the vertices are node objects with no coordinates at all, the marks live in a map keyed by object identity, and its value can be the copy of that node. The map is then both the visited table and the wiring list. Equal digits on two paddies, or equal values on two nodes, never merge them, because the key is the vertex itself.

The invariant is that a cell is marked exactly when some search has already claimed it, so each cell is claimed once and belongs to exactly one patch.

<!-- names: cell id, delta table, shared visited -->

<!-- stage: variables -->
### Ids, Shifts And The Marks

The integer `id` is the paddy being expanded, with `r` and `c` decoded from it, and `nr` and `nc` are the shifted position for move `d`. The table `owned` has one boolean per cell for the whole run, and the array `stack` holds ids waiting to be expanded, never more than the cell count because of the mark at push. The integer `moves` says how many entries of the shift tables are active, four or eight. The value `claimed` counts what the current search took, `count` counts searches started by the outer scan, and `largest` keeps the best claimed value so far.

<!-- stage: trace -->
### A Ring Fill And A Diagonal Scan

The first trace spreads a colour across a ring of three rows and four columns, stored flat in reading order, so the pointer `cur` is a cell id. The fill starts at id 0, which grows crop 1. Its left neighbour is not outside the map, because the ring wraps to id 3, and from there the fill runs down the last column and wraps again to the first column of the bottom row. The vars show how many cells are claimed and how many ids are waiting on the stack. All six cells of crop 1 end up claimed, and no cell of another crop is ever pushed.

```trace
{"cells":[1,0,0,1,0,0,0,1,1,1,0,1],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"claimed":1,"waiting":1},"note":"Cell 0 at row 0, column 0 is claimed and it pushes 1 new cells (3), one of them through the wrap of the ring."},{"at":{"cur":3},"vars":{"claimed":2,"waiting":1},"note":"Cell 3 at row 0, column 3 is claimed and it pushes 1 new cells (7)."},{"at":{"cur":7},"vars":{"claimed":3,"waiting":1},"note":"Cell 7 at row 1, column 3 is claimed and it pushes 1 new cells (11)."},{"at":{"cur":11},"vars":{"claimed":4,"waiting":1},"note":"Cell 11 at row 2, column 3 is claimed and it pushes 1 new cells (8), one of them through the wrap of the ring."},{"at":{"cur":8},"vars":{"claimed":5,"waiting":1},"note":"Cell 8 at row 2, column 0 is claimed and it pushes 1 new cells (9)."},{"at":{"cur":9},"vars":{"claimed":6,"waiting":0},"note":"Cell 9 at row 2, column 1 is claimed and it pushes nothing new."}]}
```

The second trace is the outer scan on a flat map of three rows and four columns where land is the character one and the contract lets diagonal neighbours join an island. The pointer `scan` walks the twelve ids. A search starts only at unowned land, and the vars report how many searches have started and how many cells the latest one claimed. With the diagonal flag the land at ids 0, 5 and 10 forms one chain, which is one island, and the land at id 3 is a second. The last note states how many islands the four-way contract would find on the same map.

```trace
{"cells":["1","0","0","1","0","1","0","0","0","0","1","0"],"pointers":["scan"],"steps":[{"at":{"scan":0},"vars":{"islands":1,"last_size":3},"note":"Id 0 is unowned land, so search 1 starts and claims 3 cells."},{"at":{"scan":3},"vars":{"islands":2,"last_size":1},"note":"Id 3 is unowned land, so search 2 starts and claims 1 cell."},{"at":{"scan":5},"vars":{"islands":2,"last_size":1},"note":"Id 5 is land that is already owned, so no new search starts."},{"at":{"scan":10},"vars":{"islands":2,"last_size":1},"note":"Id 10 is land that is already owned, so no new search starts."},{"at":{"scan":12},"vars":{"islands":2,"last_size":1},"note":"The scan has passed all twelve ids and the diagonal contract gives 2 islands, where the four-way contract would give 4."}]}
```

<!-- stage: code -->
### One Walk For Fill, Count And Copy

```java
final class Terraces {
    private static final int[] DR = {0, 1, 0, -1, 1, 1, -1, -1};
    private static final int[] DC = {1, 0, -1, 0, 1, -1, -1, 1};

    private static int claim(int start, int rows, int cols, boolean[] owned,
                             IntPredicate eligible, int moves, boolean wrap) {
        int[] stack = new int[rows * cols];
        int top = 0, claimed = 0;
        stack[top++] = start;
        owned[start] = true;
        while (top > 0) {
            int id = stack[--top];
            claimed++;
            int r = id / cols, c = id % cols;
            for (int d = 0; d < moves; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows) continue;
                if (wrap) nc = (nc + cols) % cols;
                else if (nc < 0 || nc >= cols) continue;
                int next = nr * cols + nc;
                if (owned[next] || !eligible.test(next)) continue;
                owned[next] = true;
                stack[top++] = next;
            }
        }
        return claimed;
    }

    static int ringFill(int[][] img, int sr, int sc, int color) {
        int rows = img.length, cols = img[0].length, tone = img[sr][sc];
        if (tone == color) return 0;
        boolean[] owned = new boolean[rows * cols];
        int n = claim(sr * cols + sc, rows, cols, owned, id -> img[id / cols][id % cols] == tone, 4, true);
        for (int id = 0; id < owned.length; id++) if (owned[id]) img[id / cols][id % cols] = color;
        return n;
    }

    static int[] patchReport(String[] beds, boolean diagonal) {
        int rows = beds.length, cols = beds[0].length();
        boolean[] owned = new boolean[rows * cols];
        int count = 0, largest = 0;
        for (int id = 0; id < owned.length; id++) {
            if (owned[id] || beds[id / cols].charAt(id % cols) != '1') continue;
            count++;
            largest = Math.max(largest, claim(id, rows, cols, owned,
                    k -> beds[k / cols].charAt(k % cols) == '1', diagonal ? 8 : 4, false));
        }
        return new int[]{count, largest};
    }

    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    static Node cloneFrom(Node start) {
        Map<Node, Node> twin = new IdentityHashMap<>();
        Deque<Node> stack = new ArrayDeque<>();
        twin.put(start, new Node(start.val));
        stack.push(start);
        while (!stack.isEmpty()) {
            Node cur = stack.pop();
            Node t = twin.get(cur);
            for (Node nb : cur.neighbors) {
                Node tn = twin.get(nb);
                if (tn == null) {
                    tn = new Node(nb.val);
                    twin.put(nb, tn);
                    stack.push(nb);
                }
                t.neighbors.add(tn);
            }
        }
        return twin.get(start);
    }
}
```

The first eight entries of the tables hold the four straight moves before the four diagonal ones, so a count of four or eight selects the contract. Each id is pushed at most once and expanded once, which gives O(R * C * moves) time for any number of searches together, with O(R * C) memory for the marks and the stack. The clone walk is the same loop with the map as the marks, taking O(V + E) time and O(V) space.

<!-- stage: applicability -->
### Maps, Patches And Object Webs

Reach for this combination when a rectangular map or a web of linked objects must be cut into regions and each region reported: spreading dye through pixels, counting stands of one tree on a satellite tile, finding the biggest room on a floor plan, or duplicating a configuration whose parts point at each other. The invariant to defend is that the single table of marks holds a vertex if and only if some search has claimed it, so no vertex is worked on twice and no region is split between two searches.

The first false friend is to read equal values as the same vertex. Two paddies that both grow crop 1, or two nodes that both carry the value 7, are different vertices, and a table keyed by value would fuse them. The second false friend is to believe that a grid brings diagonal neighbours along. The shift table decides, and a contract that says nothing about diagonals means four moves, while the flag must be stated and tested when eight are wanted.

Do not use this combination when moves have different costs, or when many starting points must spread together, or when two searches must meet in the middle. Those need the frontier layers and termination proofs of Chapter 22. In Java, the remainder operator keeps the sign of its left side, so `(c - 1) % cols` is `-1` for column 0, and a ring that wraps must add `cols` before taking the remainder.

<!-- stage: exercises -->
### Exercises

#### [Build] Flood Fill On A Ring (LeetCode 733)
<!-- id: gg-ring-flood-fill -->

**Prerequisites.** The shared visited table and the delta table of this lesson, and the three-gate neighbour test of the grid lesson.

**Problem.** The `image` is a rectangular grid of colour numbers whose columns wrap around, so column 0 is next to the last column in the same row, while rows do not wrap. Starting at `(sr, sc)`, recolour that cell and every cell reachable through up, down, left and right steps over cells of the starting colour, so that all of them become `color`. The `image` is changed in place, and the method returns the number of cells whose colour was changed. If `color` equals the starting colour, nothing changes and the answer is 0.

**Constraints.** 1 <= rows <= 40, 1 <= cols <= 40, colours are numbers from 0 to 99, and the start lies inside the grid. A ring of one or two columns is allowed.

**Example 1.** Input `image = [[3,3,1,3],[1,2,1,1],[3,1,1,3]], sr = 0, sc = 0, color = 7`, output `3` and `image` becomes `[[7,7,1,7],[1,2,1,1],[3,1,1,3]]`.

**Example 2.** Input `image = [[4,0,4],[0,0,0]], sr = 0, sc = 0, color = 9`, output `2` and `image` becomes `[[9,0,9],[0,0,0]]`.

**Hint.** Which of the two coordinates may be wrapped with a remainder, and what is `-1 % cols` in Java?

**Changed decision.** The column step wraps around the ring while the row step does not, and the result is a count of changed cells instead of the picture alone.

#### [Vary] Islands With A Diagonal Flag (LeetCode 200)
<!-- id: gg-island-count-flag -->

**Prerequisites.** The Build rung and the outer scan that starts a search at each unowned land cell.

**Problem.** The `grid` is an array of equal-length strings of `'1'` (land) and `'0'` (water), and `diagonal` is a flag. An island is a maximal group of land cells joined by up, down, left and right steps, and when `diagonal` is true the four corner steps join cells as well. Return the number of islands. The grid is not modified.

**Constraints.** 1 <= rows <= 40, 1 <= cols <= 40, and every character is `'1'` or `'0'`.

**Example 1.** Input `grid = ["10010","01100","00001","10010"], diagonal = true`, output `3`.

**Example 2.** Input `grid = ["0110","1001","0110"], diagonal = false`, output `4`.

**Hint.** Which part of the traversal depends on the flag, and which part is the same for both contracts?

**Changed decision.** The number of neighbour moves depends on the flag, so the same scan gives different counts on the same grid.

#### [Boundary] Report On The Largest Island (LeetCode 695)
<!-- id: gg-largest-island-report -->

**Prerequisites.** The Vary rung and the claimed-count that each search returns.

**Problem.** The `grid` is an array of equal-length strings of `'1'` (land) and `'0'` (water), with up, down, left and right connections. Number the cells in reading order from 0. Return `[area, ties, firstId]`, where `area` is the size of the largest island, `ties` is how many islands have exactly that size, and `firstId` is the smallest cell number inside the first largest island found by a reading-order scan. When there is no land at all, return `[0, 0, -1]`.

**Constraints.** 1 <= rows <= 40, 1 <= cols <= 40, and every character is `'1'` or `'0'`.

**Example 1.** Input `grid = ["1100","0011","1001"]`, output `[3, 1, 6]`.

**Example 2.** Input `grid = ["1011","0010","1001","1100"]`, output `[3, 2, 2]`.

**Hint.** What must happen to the tie count when a strictly larger island appears, and when an equal one appears?

**Changed decision.** The answer carries three numbers, so the running best is reset on a larger island and counted on an equal one, instead of being a single maximum.

#### [Recognize] Clone A Patch Of Nodes (LeetCode 133)
<!-- id: gg-clone-cell-graph -->

**Prerequisites.** The Boundary rung and the idea that an identity map takes the place of the marks.

**Problem.** The `grid` holds digits, where 0 is empty and any other digit is a node object whose `val` is that digit, so several nodes may share a value. Two nodes are linked when their cells are next to each other by a step up, right, down or left, and each node stores its neighbours in that order. Copy the nodes reachable from the node at `(sr, sc)`, using only the node objects and never the grid, and report `[nodes, entries, v1, v2, ...]`, where `nodes` is the number of copied nodes, `entries` is the total length of all copied neighbour lists, and the remaining numbers are the `val` of each neighbour of the copy of the start node, in stored order. The start cell is not 0.

**Constraints.** 1 <= rows <= 12, 1 <= cols <= 12, every entry is a digit from 0 to 9, and the start cell is not 0.

**Example 1.** Input `grid = [[2,2,0],[0,2,5],[7,0,2]], sr = 0, sc = 1`, output `[5, 8, 2, 2]`.

**Example 2.** Input `grid = [[4,4],[4,4]], sr = 0, sc = 0`, output `[4, 8, 4, 4]`.

**Hint.** What plays the part of the marks when the vertices are objects, and could a value be the key?

**Changed decision.** The marks are keyed by the node object itself, since many nodes share a value and no coordinates are available during the copy.
