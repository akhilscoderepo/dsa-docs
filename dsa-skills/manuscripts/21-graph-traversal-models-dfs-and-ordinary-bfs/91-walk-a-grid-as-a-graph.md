<!-- lesson-kind: combination -->
<!-- lesson-id: walk-grid-as-graph -->
## Walk A Grid As A Graph

<!-- stage: context -->
### Why A Region Count Runs Too High

A level editor for a game shows a map of land and water cells. The designer asks for two things. The first is the number of separate land regions. The second is a saved copy of one region as a graph of cell objects, so that an undo step can restore it, and the copy must not share cell objects with the live map. The first version of the region counter returned the right count but needed minutes on a large map, because every land cell started its own flood of its region.

The counter is slow because it forgets which cells earlier floods already reached. The copy needs the same kind of memory, here to know which object it has already copied. This lesson asks how one traversal serves a table of cells and a graph of objects, and what changes when the rules of a problem change.

<!-- stage: contributions -->
### What Each Earlier Lesson Adds

Two earlier lessons combine here. The Grid Graphs lesson contributes the way to treat a table as a graph without building one. Each cell is a vertex, and a direction table with a bounds check generates the neighbors of a cell on demand. That lesson also contributes the habit of marking a cell when it enters the frontier.

The Graph Cloning lesson contributes the identity map. It pairs each original object with its copy, and a lookup in that map tells the program whether it has reached an object before. The map therefore plays the part that `visited` plays for cells.

Neither lesson answers the whole editor problem alone. Grid Graphs has no object copies, and Graph Cloning never generates neighbors from coordinates. The combination decides how a changed rule enters the code, which is the subject of the lesson.

<!-- stage: naive -->
### Searching Again From Every Land Cell

The direct plan treats each land cell as a possible start. For each land cell, the plan floods its region with a new `visited` array and finds the smallest cell id in that region. The cell counts as a region start only when its own id is that smallest id.

```java
static int countRegionsSlow(int[][] grid) {
    int rows = grid.length, cols = grid[0].length, count = 0;
    for (int s = 0; s < rows * cols; s++) {
        if (grid[s / cols][s % cols] == 0) continue;
        boolean[] seen = new boolean[rows * cols];       // a fresh array for every start
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        stack.push(s);
        seen[s] = true;
        int smallest = s;
        while (!stack.isEmpty()) {
            int id = stack.pop();
            smallest = Math.min(smallest, id);
            int r = id / cols, c = id % cols;
            int[][] around = {{r + 1, c}, {r - 1, c}, {r, c + 1}, {r, c - 1}};
            for (int[] a : around) {
                if (a[0] < 0 || a[0] >= rows || a[1] < 0 || a[1] >= cols) continue;
                int nid = a[0] * cols + a[1];
                if (grid[a[0]][a[1]] == 1 && !seen[nid]) { seen[nid] = true; stack.push(nid); }
            }
        }
        if (smallest == s) count++;
    }
    return count;
}
```

```predict
A map has 3 rows and 3 columns, and every cell is land. The method returns the right count of 1 region. How many cells does it take off the stack in total?

It takes 81 cells off the stack. Each of the 9 start cells floods the whole map of 9 cells. A single shared search would take each cell off once, which is 9 pops.
```

<!-- stage: bottleneck -->
### Counting Repeated Floods

The method returns correct counts, but it throws away what each flood learned. The method floods a region of `k` cells `k` times, once from each of its cells. Each flood costs O(k), so the region costs O(k^2). On a map of `rows * cols` land cells the total is O((rows * cols)^2). A map of 1,000 by 1,000 cells needs about 10^12 pops.

The allocation adds to the cost. Each start allocates a new array of `rows * cols` flags, so each land start pays O(rows * cols) for its fresh array, whatever the size of its region. The method also hides a second problem. It cannot report a region's size, first cell or copy without running another flood, because the knowledge of which cells belong together dies with each `seen` array.

The editor needs one record of reached cells that lives across all starts. The program then finds each region once, and the same record can carry data about the region.

<!-- stage: insight -->
### One Traversal For Many Rules

#### Separating Neighbors From Traversal

A **neighbor function** takes a vertex and returns the vertices that touch it. For a grid, the function adds each step of the direction table to the cell, applies the bounds check and then applies the eligibility rule of the problem. For an object graph, the function returns the stored list of neighbors. The traversal calls the function and never looks at how the vertices are stored.

<!-- names: neighbor function, start loop, discovery rule -->

#### Running The Start Loop

The **start loop** scans every vertex in a fixed order. An eligible vertex that no search has reached starts a new search. The loop then records what the problem asks for, such as a count, an area or the first vertex of the region. Every search shares one `visited` array, so a region is found once, from its first vertex in scan order. The shared array turns O((rows * cols)^2) work into O(rows * cols).

#### Applying One Discovery Rule

The **discovery rule** marks a vertex at the moment the search first finds it, before the vertex enters the frontier. For cells, the mark is a flag in `visited`. For objects, the mark is an entry in the identity map from original to copy, and the entry also stores the copy.

Each changed contract touches exactly one of the three parts. Diagonal contact adds four steps to the direction table inside the neighbor function. A protected color changes the eligibility test in the neighbor function. A smallest-island request changes what the start loop records. A graph of objects changes what the discovery rule stores. The traversal itself stays the same.

<!-- stage: variables -->
### What One Walk Keeps

One walk keeps the following values. The names match the trace and the code below.

- **dirs** holds one row and column step per allowed direction.
- **visited** is a boolean array indexed by the cell id `r * cols + c`.
- **frontier** is an `ArrayDeque` of ids or objects waiting for expansion.
- **scan** is the index that the start loop has reached.
- **cur** is the vertex that just left the frontier.
- **count** is the number of searches the start loop has begun.
- **copies** is the identity map from each original object to its copy.

<!-- stage: trace -->
### Walking Two Different Inputs

#### Counting Regions With Diagonal Contact

The first trace counts regions on a table with three rows and four columns, flattened into twelve cells. Diagonal contact joins cells, so the direction table has eight steps. The pointer `scan` marks the start loop, and the pointer `cur` marks the cell that left the frontier. Water cells pass the scan with no step in the trace.

The first land cell, cell 0, starts region 1. The search walks the diagonal through cells 5 and 10 and then reaches cell 11. Cell 3 sits in the top right corner and touches none of them, so the scan reaches it next and starts region 2. The scan also meets cells 5, 10 and 11 again, and each time it skips them, because `visited` already holds them.

```trace
{"cells":[1,0,0,1,0,1,0,0,0,0,1,1],"pointers":["scan","cur"],"steps":[{"at":{"scan":0,"cur":-1},"vars":{"count":"1","frontier":"[0]"},"note":"Cell 0 is land and no search has reached it. It begins region 1 and enters the frontier."},{"at":{"scan":0,"cur":0},"vars":{"count":"1","frontier":"[5]"},"note":"Cell 0 leaves the frontier. Of its eight candidates, only cell 5 joins the frontier, by corner contact."},{"at":{"scan":0,"cur":5},"vars":{"count":"1","frontier":"[10]"},"note":"The search expands cell 5. Of its eight candidates, only cell 10 joins the frontier, by corner contact."},{"at":{"scan":0,"cur":10},"vars":{"count":"1","frontier":"[11]"},"note":"Next the search takes cell 10. Of its eight candidates, only cell 11 joins the frontier."},{"at":{"scan":0,"cur":11},"vars":{"count":"1","frontier":"[]"},"note":"Cell 11 leaves the frontier. Of its eight candidates, no new cell qualifies."},{"at":{"scan":3,"cur":-1},"vars":{"count":"2","frontier":"[3]"},"note":"Cell 3 is land and no search has reached it. It begins region 2 and enters the frontier."},{"at":{"scan":3,"cur":3},"vars":{"count":"2","frontier":"[]"},"note":"Cell 3 leaves the frontier. Of its eight candidates, no new cell qualifies."},{"at":{"scan":5,"cur":-1},"vars":{"count":"2","frontier":"[]"},"note":"The scan reaches cell 5. It holds land, but visited already marks it, so no new search starts."},{"at":{"scan":10,"cur":-1},"vars":{"count":"2","frontier":"[]"},"note":"The scan reaches cell 10. It holds land, but visited already marks it, so no new search starts."},{"at":{"scan":11,"cur":-1},"vars":{"count":"2","frontier":"[]"},"note":"The scan reaches cell 11. It holds land, but visited already marks it, so no new search starts."},{"at":{"scan":12,"cur":-1},"vars":{"count":"2","frontier":"[]"},"note":"The scan passes the last cell. The map holds 2 regions."}]}
```

#### Cloning One Region

The second trace copies the region of the first land cell in a table with three rows and three columns, flattened into nine cells. The graph has a vertex for each land cell and an edge for each pair of land cells that share a side. The pointer `cur` marks the original cell under expansion. The trace variable `copies` shows `copies.size()`, the number of entries of the identity map named `copies` in the code, and `cur` keeps its name there.

Cell 0 starts the walk and receives its copy first. Cell 1 then links back to the copy of cell 0, and the walk does not create a second copy. Cells 6 and 8 never appear, because they belong to other regions.

```trace
{"cells":[1,1,0,0,1,0,1,0,1],"pointers":["cur"],"steps":[{"at":{"cur":-1},"vars":{"copies":"1","frontier":"[0]"},"note":"The first land cell is 0. Its copy is created at once and the cell enters the frontier."},{"at":{"cur":0},"vars":{"copies":"2","frontier":"[1]"},"note":"Cell 0 leaves the frontier. Its copy now lists [1], and cell 1 gets a new copy and enters the frontier."},{"at":{"cur":1},"vars":{"copies":"3","frontier":"[4]"},"note":"The walk expands cell 1. Its copy now lists [0, 4]. Cell 4 gets a new copy and enters the frontier, and the copy of cell 0 exists already, so the walk only links to it."},{"at":{"cur":4},"vars":{"copies":"3","frontier":"[]"},"note":"Cell 4 leaves the frontier. Its copy now lists [1]. The copy of cell 1 exists already, so the walk only links to it."}]}
```

<!-- stage: code -->
### One Walk In Two Forms

#### Counting Regions With A Chosen Direction Table

The method below takes the direction table as a parameter. A caller passes four steps or eight and gets the matching regions. The outer loop is the start loop, the loop over `dirs` with its two tests is the neighbor function written inline, and the lines that set `visited` apply the discovery rule.

```java
static int regionCount(int[][] grid, int[][] dirs) {
    int rows = grid.length, cols = grid[0].length, count = 0;
    boolean[] visited = new boolean[rows * cols];          // one array shared by every search
    for (int scan = 0; scan < rows * cols; scan++) {       // the start loop
        if (grid[scan / cols][scan % cols] != 1 || visited[scan]) continue;
        count++;                                           // an unreached land cell begins a region
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        visited[scan] = true;
        frontier.add(scan);
        while (!frontier.isEmpty()) {
            int cur = frontier.poll();
            for (int[] d : dirs) {                         // the neighbor function, written inline
                int nr = cur / cols + d[0], nc = cur % cols + d[1];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int id = nr * cols + nc;
                if (grid[nr][nc] == 1 && !visited[id]) { visited[id] = true; frontier.add(id); }
            }
        }
    }
    return count;
}
```

#### Copying Objects With An Identity Map

The second method copies a graph of objects. The class wraps the node type and both methods so that the block compiles on its own. The method `buildNodes` makes one `Node` for each land cell and lists the neighbors in the order up, left, right, down.

```java
final class RegionCopy {
    static final class Node {
        final int id;
        final List<Node> neighbors = new ArrayList<>();
        Node(int id) { this.id = id; }
    }

    static Node copyRegion(Node first) {
        HashMap<Node, Node> copies = new HashMap<>();             // original to copy
        ArrayDeque<Node> frontier = new ArrayDeque<>();
        copies.put(first, new Node(first.id));                    // mark when found
        frontier.add(first);
        while (!frontier.isEmpty()) {
            Node cur = frontier.poll();
            for (Node nb : cur.neighbors) {
                if (!copies.containsKey(nb)) {                    // not found before
                    copies.put(nb, new Node(nb.id));
                    frontier.add(nb);
                }
                copies.get(cur).neighbors.add(copies.get(nb));    // link copy to copy
            }
        }
        return copies.get(first);
    }

    static Node[] buildNodes(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        Node[] nodes = new Node[rows * cols];                     // null marks a water cell
        for (int id = 0; id < rows * cols; id++) {
            if (grid[id / cols][id % cols] == 1) nodes[id] = new Node(id);
        }
        int[][] order = {{-1, 0}, {0, -1}, {0, 1}, {1, 0}};       // up, left, right, down
        for (int id = 0; id < rows * cols; id++) {
            if (nodes[id] == null) continue;
            for (int[] d : order) {
                int nr = id / cols + d[0], nc = id % cols + d[1];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (nodes[nr * cols + nc] != null) nodes[id].neighbors.add(nodes[nr * cols + nc]);
            }
        }
        return nodes;
    }
}
```

#### Building Then Copying One Region

Take the map `[[1,1],[0,1]]`. The cells 0, 1 and 3 are land, and cell 2 is water. The method `buildNodes` gives node 0 the list `[1]`, because its cell has water below it. Node 1 receives `[0, 3]`, and node 3 receives `[1]`. The call `copyRegion(nodes[0])` then copies node 0, finds node 1 through it and copies node 1, and finds node 3 through node 1. Each copy lists the same values as its original, and no copy is an original. The Recognize exercise changes the Clone Graph contract in exactly this way. The objects come from coordinates first, and the copy step stays the same.

#### Cost Of Both Forms

- **Time** is O(rows * cols * |dirs|) for the first method, because each cell enters the frontier once and tests every step.
- **Time** is O(V + E) for the second method, because each object is copied once and each edge is linked once.
- **Space** is O(rows * cols) for the first method and O(V) for the second, because each stores one mark per vertex.

<!-- stage: applicability -->
### Telling Which Part A Contract Changes

#### Mapping A Changed Rule To One Part

Read a changed contract and ask which of the three parts it touches. A new set of moves or a new eligibility rule belongs to the neighbor function, and the moves sit in its direction table. A new quantity to report belongs to the start loop. A new kind of vertex belongs to the discovery rule. Changing one part leaves the other two unchanged.

#### Keeping The Invariant Across Contracts

The invariant of the whole lesson is that every vertex enters the frontier once, and the program marks it before it enters. This holds for cells, for objects and for every changed contract in the exercises. A rule that unmarks a vertex, or that marks it only on removal from the frontier, breaks the invariant.

#### Avoiding Familiar Code On New Rules

The original problem is a false friend of the changed one. A solution copied from the four-direction version passes every sample that has no diagonal contact. A fill that tests the old color instead of the protected color passes samples with a single color. In Java, `HashMap` compares objects with `equals`, and a `Node` class without its own `equals` compares by identity. That default is what the copy relies on, and a class that defines value equality would merge distinct objects.

<!-- stage: exercises -->
### Exercises

#### [Build] Protected Fill With A Count (LeetCode 733)
<!-- id: gt-fill-protected -->

**Prerequisites.** The Grid Graphs lesson and its Flood Fill exercise.

**Problem.** This changes the Flood Fill contract in two ways. First, the patch is not a set of same-colored pixels. The patch is every pixel reachable from `(sr, sc)` through side neighbors whose color is not `protect`. Second, the method returns a count. An image is a rectangular array of integer colors. If `image[sr][sc] == protect`, the patch is empty. Otherwise, set every patch pixel to `color`, and return the number of patch pixels whose color changed.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 50`, and every row has the same length.
- **Colors** satisfy `0 <= image[r][c], color, protect < 1000`.
- **Protect** differs from `color`, so a recolored pixel stays part of the patch.
- **Count** is the number of pixels whose value changed, so a patch pixel already holding `color` adds nothing.
- **Mutation** is expected; the method changes `image` in place and returns the count.

**Example 1.** Input `image = [[1,7,5],[2,5,1],[1,2,2]]`, `sr = 0`, `sc = 0`, `color = 7`, `protect = 5`, output 6, and the image becomes `[[7,7,5],[7,5,7],[7,7,7]]`.

**Example 2.** Input `image = [[4,5],[5,4]]`, `sr = 0`, `sc = 1`, `color = 6`, `protect = 5`, output 0, and the image stays unchanged because the source holds the protected color.

**Hint.** Which test decides whether a candidate neighbor joins the patch, and which comparison decides whether the count grows?

**Changed decision.** The eligibility test moves from equality with the old color to inequality with the protected color, and the count differs from the patch size.

#### [Vary] Islands With Diagonal Contact (LeetCode 200)
<!-- id: gt-island-diagonal -->

**Prerequisites.** The Number Of Islands exercise of the Grid Graphs lesson.

**Problem.** This changes the Number Of Islands contract in two ways. First, two land cells are neighbors when they share a side or a corner, so each cell has up to eight neighbors. Second, the map is an `int` array and not a `char` array. A cell holds 1 for land and 0 for water. An island is a maximal set of land cells connected through these eight-direction neighbors. Return the number of islands.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 100`, and every row has the same length.
- **Cells** are the `int` values 0 and 1 only.
- **Neighbors** are the eight cells that share a side or a corner.
- **Answer** is an `int`, and it is 0 when the map has no land.
- **Mutation** does not occur; the method leaves `grid` unchanged.

**Example 1.** Input `grid = [[1,0,0,1],[0,1,0,0],[0,0,1,1]]`, output 2, where the four cells on the diagonal chain form one island.

**Example 2.** Input `grid = [[1,1,0],[0,0,1],[1,0,0]]`, output 2, where the first three cells form one island and the cell in the bottom left corner forms the other.

**Hint.** Which of the three parts of the walk holds the list of moves? Does the start loop need any change?

**Changed decision.** The direction table grows from four steps to eight, and nothing else in the walk changes.

#### [Boundary] Smallest Island And Its First Cell (LeetCode 695)
<!-- id: gt-smallest-island -->

**Prerequisites.** The Max Area Of Island exercise of the Grid Graphs lesson.

**Problem.** This changes the Max Area Of Island contract. The map is an `int` array with 1 for land and 0 for water, and neighbors share a side. The area of an island counts the cells that it holds. Return the smallest area and the first cell of the island that has it. The first cell of an island is the cell with the smallest row, and then the smallest column, among the island's cells. When several islands share the smallest area, choose the one whose first cell comes first in row-major order. Return `{area, row, col}`, or `{0, -1, -1}` when the map has no land.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 50`, and every row has the same length.
- **Cells** are the `int` values 0 and 1 only.
- **Neighbors** use the four side directions only.
- **Ties** go to the island whose first cell has the smaller row, then the smaller column.
- **Mutation** does not occur; the method leaves `grid` unchanged.

**Example 1.** Input `grid = [[1,1,0,0],[1,0,0,1],[0,0,0,0],[1,0,1,1]]`, output `{1, 1, 3}`.

**Example 2.** Input `grid = [[1,0,1],[1,0,1],[1,0,1]]`, output `{3, 0, 0}`, because both islands have area 3 and the left one comes first.

**Hint.** The start loop reaches the first cell of every island before any other cell of it. When should the best answer be replaced, and when should a tie leave it alone?

**Changed decision.** The method keeps a smaller area and the cell that starts the search, and not the largest area.

#### [Recognize] Clone A Graph Built From Land (LeetCode 133)
<!-- id: gt-clone-land -->

**Prerequisites.** The Graph Cloning lesson and the three exercises above.

**Problem.** This changes the Clone Graph contract. The input is a map `grid` of 0 and 1, and the graph does not arrive as objects. Build the graph first. It has one `Node` for each land cell, with `val = r * cols + c`. Two nodes are neighbors when their cells share a side, and each node lists its neighbors in the order up, left, right, down. Then return a deep copy of the component that holds the first land cell in row-major order. The copy shares no `Node` with the original graph and keeps the same neighbor order. Return `null` when the map has no land. Cells of other islands do not appear in the copy.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 30`, and every row has the same length.
- **Cells** are the `int` values 0 and 1 only.
- **Node** has an `int val` and a `List<Node> neighbors`.
- **Neighbors** use the four side directions only, in the order up, left, right, down.
- **Copy** shares no node with the original graph and contains only one island.

**Example 1.** Input `grid = [[1,1,0],[0,1,0],[1,0,1]]`, output a copy that lists the pairs `0:[1]`, `1:[0,4]` and `4:[1]` as `val:[neighbor vals]`. Cells 6 and 8 are land of other islands.

**Example 2.** Input `grid = [[1,1],[1,1]]`, output a copy that lists `0:[1,2]`, `1:[0,3]`, `2:[0,3]` and `3:[1,2]`.

**Hint.** What plays the role of `visited` when the vertices are objects? What must the program store along with the mark?

**Changed decision.** The graph appears from coordinates and then needs copying, so the identity map replaces `visited` and only one component is copied.
