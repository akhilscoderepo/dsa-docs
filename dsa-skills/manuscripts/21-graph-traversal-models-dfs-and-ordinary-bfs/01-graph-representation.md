<!-- lesson-kind: standard -->
<!-- lesson-id: graph-representation -->
## Graph Representation

<!-- stage: context -->
### Finding One User's Friends

A messaging app stores friendships as pairs of user ids. For six users numbered 0 to 5, the pairs are `[[0,1],[0,2],[1,3],[3,4]]`. User 5 has no friends yet. The profile page of user 3 must show every friend of user 3, and the answer is 1 and 4.

The app asks this question for one user today. The next feature suggests friends of friends. That feature asks the same question for every user it reaches, and it keeps asking until it has covered the whole network. The pairs look like a flat table, but the questions follow relationships from one user to the next. A flat table answers each question slowly. The lesson answers one question: what storage makes "who is connected to this user" fast?

<!-- stage: naive -->
### Scanning All Pairs Each Time

The direct approach keeps the pairs as they arrive. To list the friends of a user, the method reads every pair and checks whether either side is that user. When one side matches, the other side is a friend.

```java
static List<Integer> friendsOf(int[][] pairs, int user) {
    List<Integer> found = new ArrayList<>();
    for (int[] p : pairs) {
        if (p[0] == user) found.add(p[1]);
        else if (p[1] == user) found.add(p[0]);
    }
    return found;
}
```

On the six-user example, `friendsOf(pairs, 3)` returns `[1, 4]`. The method is short and correct. Adding a new friendship costs one array append. The cost appears only when the app asks the question many times.

<!-- stage: bottleneck -->
### Counting Pair Reads Per Search

```predict
A feature visits every user and asks for that user's friends with the scan above. The network has n users and m pairs. How many pair reads does the whole feature perform?

Each question reads all m pairs, and the feature asks n questions. The total is O(n * m) pair reads, which is far larger than the data itself.
```

Each call to `friendsOf` reads all `m` pairs, even for a user with one friend. A feature that asks for every user performs `n * m` reads. With `n = 100000` users and `m = 100000` pairs, that is `10^10` reads, which takes many seconds in Java. The input itself holds only `2 * m` numbers.

The scan repeats the same work. It re-reads pairs that belong to other users. A better layout groups the pairs by user once, so each question reads only the answer. The total cost of asking about every user then drops to O(n + m), because every pair is read a constant number of times.

<!-- stage: insight -->
### Keeping One Friend List Per User

The fix is to restructure the pairs once, into a form that answers "who is connected to this user" by direct lookup. First the lesson needs standard terms for the data.

#### Naming The Parts

A **graph** is a collection of vertices and edges. A **vertex** is one item, here a user, and the chapter numbers vertices from 0 to n-1. An **edge** is one relationship between two vertices, written as a pair `[a, b]`. The **neighbors** of a vertex are the vertices its edges lead to. A vertex with no edges is isolated, and it still exists and still needs an answer.

#### Choosing A Direction

An undirected edge works both ways, so `[a, b]` makes `b` a neighbor of `a` and `a` a neighbor of `b`. A directed edge works one way, so `[a, b]` makes `b` a neighbor of `a` only. A statement must say which kind it uses. Two edges with the same endpoints are parallel edges. A **self-loop** is an edge `[a, a]`. A statement must also say whether the input contains them.

#### Two Storage Layouts

An **adjacency list** is an array `adj` of `n` lists, where `adj[v]` holds the neighbors of `v`. Reading the neighbors of one vertex costs the size of that list. An undirected edge adds two entries, one in each endpoint's list, and a directed edge adds one. The whole structure holds `n` lists and one entry per directed edge, so it takes O(n + m) space.

An **adjacency matrix** is an `n` by `n` grid of booleans, where cell `[a][b]` is true exactly when an edge leads from `a` to `b`. Asking whether one edge exists costs O(1). The grid takes O(n^2) space regardless of how many edges exist.

<!-- names: graph, vertex, edge, neighbor, adjacency list, adjacency matrix -->

<!-- stage: variables -->
### The Names Used In The Code

The conversion uses four names, and the rest of the chapter reuses them.

- **n** is the number of vertices, numbered 0 to n-1.
- **edges** is the `int[][]` input, where each row `[a, b]` is one edge.
- **adj** is the adjacency list, one list of neighbors per vertex.
- **matrix** is the adjacency matrix, a boolean grid of side `n`.

The number of edges is `m`. Later lessons write V for the vertex count `n` and E for the edge count `m`, and each lesson keeps one pair.

<!-- stage: trace -->
### Building The Lists Edge By Edge

#### Undirected Input With Five Vertices

Take `n = 5` and `edges = [[0,1],[0,2],[1,3],[3,4]]`, read as undirected. In the trace below, the pointers `from` and `to` mark the two endpoints of the edge in hand. The method starts with five empty lists.

Each edge adds two entries. The edge `[0,1]` appends 1 to the list of vertex 0 and appends 0 to the list of vertex 1. After the four edges, vertex 3 holds `[1,4]`, which is the answer to the opening question. The total number of entries is 8, twice the number of edges.

#### Directed Input With An Isolated Vertex

Now take `n = 5` and `edges = [[2,3],[0,1],[2,1],[3,2]]`, read as directed. Each edge adds one entry, so the list of vertex 2 holds `[3,1]` and the list of vertex 3 holds `[2]`. Vertex 4 appears in no edge. Its list stays empty, because the method created all five lists before it read any edge.

The two inputs differ in one decision only. The undirected version appends in both directions, and the directed version appends in the stated direction.

#### Stepping Through Both Inputs

The first trace shows the undirected conversion.

```trace
{"cells":[0,1,2,3,4],"pointers":["from","to"],"steps":[{"at":{"from":0,"to":1},"vars":{"edge":"[0,1]","adj":"0:[1] 1:[0] 2:[] 3:[] 4:[]"},"note":"The edge [0,1] adds 1 to the list of vertex 0 and 0 to the list of vertex 1."},{"at":{"from":0,"to":2},"vars":{"edge":"[0,2]","adj":"0:[1,2] 1:[0] 2:[0] 3:[] 4:[]"},"note":"The edge [0,2] gives vertex 0 a second neighbor and gives vertex 2 its first."},{"at":{"from":1,"to":3},"vars":{"edge":"[1,3]","adj":"0:[1,2] 1:[0,3] 2:[0] 3:[1] 4:[]"},"note":"The edge [1,3] extends the list of vertex 1 and starts the list of vertex 3."},{"at":{"from":3,"to":4},"vars":{"edge":"[3,4]","adj":"0:[1,2] 1:[0,3] 2:[0] 3:[1,4] 4:[3]"},"note":"The edge [3,4] makes vertex 3 hold 1 and 4, which answers the opening question."}]}
```

The second trace shows the directed conversion.

```trace
{"cells":[0,1,2,3,4],"pointers":["from","to"],"steps":[{"at":{"from":2,"to":3},"vars":{"edge":"[2,3]","adj":"0:[] 1:[] 2:[3] 3:[] 4:[]"},"note":"The directed edge [2,3] writes 3 into the list of vertex 2 only."},{"at":{"from":0,"to":1},"vars":{"edge":"[0,1]","adj":"0:[1] 1:[] 2:[3] 3:[] 4:[]"},"note":"The directed edge [0,1] writes 1 into the list of vertex 0 and leaves vertex 1 untouched."},{"at":{"from":2,"to":1},"vars":{"edge":"[2,1]","adj":"0:[1] 1:[] 2:[3,1] 3:[] 4:[]"},"note":"The edge [2,1] appends 1 after 3 in the list of vertex 2."},{"at":{"from":3,"to":2},"vars":{"edge":"[3,2]","adj":"0:[1] 1:[] 2:[3,1] 3:[2] 4:[]"},"note":"The edge [3,2] gives vertex 3 a neighbor; vertex 4 still has an empty list because no edge mentions it."}]}
```

<!-- stage: code -->
### Building Lists And A Matrix

#### Two Methods For Lists

The method `undirected` adds both directions for each edge. The method `directed` adds only the stated direction. Both create all `n` lists first.

```java
static List<List<Integer>> undirected(int n, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] e : edges) {
        adj.get(e[0]).add(e[1]);
        adj.get(e[1]).add(e[0]);
    }
    return adj;
}

static List<List<Integer>> directed(int n, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] e : edges) adj.get(e[0]).add(e[1]);
    return adj;
}
```

The loop creates one new list per vertex. A shortcut such as `Collections.nCopies(n, new ArrayList<Integer>())` fills the outer list with `n` references to one single list, so every vertex would share the same neighbors.

#### Matrix Version And Costs

The method `matrixOf` handles undirected edges only, because it sets both cells of each edge. A directed version would set `matrix[e[0]][e[1]]` alone.

```java
static boolean[][] matrixOf(int n, int[][] edges) {
    boolean[][] matrix = new boolean[n][n];
    for (int[] e : edges) {
        matrix[e[0]][e[1]] = true;
        matrix[e[1]][e[0]] = true;
    }
    return matrix;
}
```

- **Lists** build in O(n + m) time and use O(n + m) space; listing the neighbors of `v` costs the size of `adj[v]`.
- **Matrix** builds in O(n^2 + m) time and uses O(n^2) space; testing one edge costs O(1).

<!-- stage: applicability -->
### Choosing A Layout For A Statement

#### Recognizing Relationship Data

Use these structures when relationships are arbitrary pairs and no single parent or next pointer describes them. A tree node has one parent, and a linked list node has one next pointer. Here a vertex has any number of neighbors, so a field per node cannot hold them.

The invariant of the adjacency list is that `adj[v]` holds exactly the neighbors of `v`, no more and no fewer. Every later traversal in the chapter relies on it, because a traversal visits only what the list reports.

#### Checking The Input Contract

Read the contract before writing any code. Does an edge work in both directions, or only one? Can the input repeat an edge or contain a self-loop? Are all vertices numbered, including those that appear in no edge? A conversion that answers one of these questions wrongly produces lists that look right on a small example and fail elsewhere.

#### Matrix As False Friend

The matrix looks simpler, because one lookup answers an edge question. It is a false friend for sparse data. A network of 100000 users takes `10^10` cells in a matrix, even if each user has three friends. The adjacency list uses memory in proportion to the data. Choose the matrix only when `n` is small or when the statement asks many direct edge questions on a dense graph.

<!-- stage: exercises -->
### Exercises

#### [Build] Undirected Adjacency Lists (Author exercise)
<!-- id: gt-undirected-adjacency -->

**Prerequisites.** The adjacency list of this lesson.

**Problem.** Given an integer `n` and an array `edges` of undirected edges, return the adjacency list as `List<List<Integer>>`. Vertices are numbered 0 to n-1. For each row `[a, b]` of `edges` in input order, append `b` to the list of `a` and then append `a` to the list of `b`. The list of an isolated vertex is empty.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** are integers in the range 0 to n-1.
- **Edge list** has no repeated edge and no self-loop.
- **Input** is not modified, so `edges` keeps its contents.

**Example 1.** Input `n = 4` and `edges = [[0,1],[0,2],[2,3]]`, output `[[1,2],[0],[0,3],[2]]`.

**Example 2.** Input `n = 3` and `edges = [[1,2],[0,1]]`, output `[[1],[2,0],[1]]`.

**Hint.** How many entries does one edge add in total?

**Changed decision.** Each edge is written in both directions.

#### [Vary] Directed Adjacency Lists (Author exercise)
<!-- id: gt-directed-adjacency -->

**Prerequisites.** The previous exercise.

**Problem.** Given an integer `n` and an array `edges` of directed edges, return the adjacency list as `List<List<Integer>>`. A row `[a, b]` is an edge from `a` to `b`, so only `adj[a]` receives `b`. Rows are read in input order. Every vertex from 0 to n-1 has a list, including vertices that no edge mentions.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** are integers in the range 0 to n-1.
- **Edge list** has no repeated pair `[a, b]`, and `a != b`.
- **Reverse pairs** may occur; `[a, b]` and `[b, a]` are two different edges.

**Example 1.** Input `n = 4` and `edges = [[2,0],[0,1],[2,1]]`, output `[[1],[],[0,1],[]]`.

**Example 2.** Input `n = 2` and `edges = [[1,0]]`, output `[[],[0]]`.

**Hint.** Which of the two appends from the undirected exercise remains?

**Changed decision.** Each edge is written in the stated direction only, and isolated vertices keep empty lists.

#### [Boundary] Parallel And Self Edges (Author exercise)
<!-- id: gt-parallel-self-edges -->

**Prerequisites.** The undirected exercise.

**Problem.** Given an integer `n` and an array `edges` of undirected edges, return `List<List<Integer>>` where entry `v` lists the distinct neighbors of `v` in ascending order. The input may contain the same edge several times, in either order of endpoints, and may contain self-loops `[v, v]`. A vertex is never its own neighbor in the output, and a repeated edge counts once.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** are integers in the range 0 to n-1.
- **Repeats** are allowed; `[a, b]` and `[b, a]` name the same undirected edge.
- **Self-loops** are allowed and are ignored.

**Example 1.** Input `n = 3` and `edges = [[0,1],[1,0],[1,1],[1,2]]`, output `[[1],[0,2],[1]]`.

**Example 2.** Input `n = 2` and `edges = [[0,0],[1,1]]`, output `[[],[]]`.

**Hint.** For the input `[[0,1],[1,0]]`, does vertex 0 list vertex 1 once or twice, and which sentence of the contract decides it?

**Changed decision.** The contract now permits repeats and self-loops, so the method deduplicates and skips them.

#### [Recognize] Find Center of Star Graph (LeetCode 1791)
<!-- id: gt-star-center -->

**Prerequisites.** The edge and neighbor terms of this lesson.

**Problem.** A star graph is an undirected graph with `n - 1` edges on vertices labeled 0 to n-1, where one vertex, the center, shares an edge with every other vertex, and no other edges exist. Given `edges`, return the center. This version numbers vertices from 0, not from 1.

**Constraints.** The limits are:
- **Vertices** number `n = edges.length + 1`, and `n` is not part of the input.
- **Edges** satisfy `2 <= edges.length <= 10^5 - 1`, and each row has two distinct endpoints.
- **Shape** is guaranteed to be a valid star graph, so the center is unique.
- **Input** is not modified, so `edges` keeps its contents.

**Example 1.** Input `edges = [[0,1],[2,0],[0,3]]`, output 0.

**Example 2.** Input `edges = [[3,1],[3,0],[2,3],[3,4]]`, output 3.

**Hint.** Which vertex must appear in every edge, and how few edges show it?

**Changed decision.** No lists are built. The first two edges share exactly one endpoint, and that endpoint is the center.
