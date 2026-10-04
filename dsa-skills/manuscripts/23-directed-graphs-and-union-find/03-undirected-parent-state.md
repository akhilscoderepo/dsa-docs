<!-- lesson-kind: standard -->
<!-- lesson-id: undirected-parent-state -->
## Undirected Parent State

<!-- stage: context -->
### Lanterns Between The Lampposts

Odile looks after Wren Hollow Park, and on the first Saturday of October the town holds its lantern evening. Strings of lights are to be hung from lamppost to lamppost across the lawns. The twelve posts have their numbers painted on the base, 0 to 11, and each string of cable runs between exactly two of them. A single plug at post 0 feeds the whole display.

The town electrician gave her two rules before he would switch anything on. Every post must end up lit, and no cables may form a closed ring anywhere, because a ring means a spare cable that carries nothing new and is one more thing to trip over in the dark. Odile has a clipboard listing the strings already hung, one pair of post numbers per line, and she wants to know whether the park is ready, whether the list as written meets both rules, and she wants a method she can apply to any park and any clipboard.

<!-- stage: naive -->
### Take Each String Down In Turn

The direct way is to test the two rules separately. For the ring rule, imagine unhooking one string at a time and ask whether its two posts can still be reached from each other along the remaining strings. If they can, the string was part of a ring. For the lit rule, search outward from post 0 and see whether every post turns up.

```java
static boolean[] reachFrom(int n, int[][] cables, int skip, int start) {
    List<List<Integer>> next = new ArrayList<>();
    for (int i = 0; i < n; i++) next.add(new ArrayList<>());
    for (int i = 0; i < cables.length; i++) {
        if (i == skip) continue;
        next.get(cables[i][0]).add(cables[i][1]);
        next.get(cables[i][1]).add(cables[i][0]);
    }
    boolean[] lit = new boolean[n];
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    lit[start] = true;
    queue.add(start);
    while (!queue.isEmpty()) {
        int post = queue.poll();
        for (int other : next.get(post)) {
            if (!lit[other]) {
                lit[other] = true;
                queue.add(other);
            }
        }
    }
    return lit;
}

static boolean readyByBruteForce(int n, int[][] cables) {
    for (int i = 0; i < cables.length; i++) {
        if (reachFrom(n, cables, i, cables[i][0])[cables[i][1]]) return false;
    }
    for (boolean on : reachFrom(n, cables, -1, 0)) {
        if (!on) return false;
    }
    return true;
}
```

This is correct. A string that sits on a ring always has a second route between its ends, and a string that sits on no ring never does, so the test finds exactly the ring strings. Each unhooking works on its own fresh arrays, so no earlier attempt can leak into a later one.

<!-- stage: bottleneck -->
### One Search Per String Is Too Many

Every call to the search builds the neighbor lists and walks them, which costs O(n + m) for n posts and m strings. The ring test makes m such calls and the lit test makes one more, so the whole check costs O(m * (n + m)). A district festival with 2,000 posts and 5,000 strings needs about thirty-five million steps, and a city grid with a hundred thousand posts would need ten billion.

Nearly all of those searches rediscover the same thing. Unhooking string 7 and walking the whole park again says almost nothing that unhooking string 8 and walking the whole park again did not already say. The two rules are also being asked as if they were unrelated questions, when a layout in which every post is lit and nothing forms a ring is a very restricted shape. A better method should look at the shape once, and should lean on any simple number that the shape forces, such as how many strings it must contain.

<!-- stage: insight -->
### Counting Strings Settles Half The Question

A layout that lights every post and holds no ring is called a tree. Take n posts. To light them all you need at least n - 1 strings, since each string can bring one new post into the lit group. To avoid a ring you can use at most n - 1, since the n-th string would join two posts that are already joined. So a tree has exactly n - 1 strings, and this gives the **edge count rule**: reject any list whose length is not n - 1, and for a list that does have n - 1 strings, being fully lit and being ring-free are the same thing, so proving one proves the other.

That makes a single walk enough. A layout with no ring but possibly several separate pieces is a **forest**, and a forest with c pieces has exactly n - c strings. When the list has n - 1 strings and the walk from post 0 reaches all n posts, there is one piece, so no ring can exist. When the walk falls short, there is a ring somewhere hiding behind the shortfall, even though the walk never touches it.

Sometimes you still need to find the ring itself. A walk meets each string from both of its ends, so on arriving at a post it must ignore the **parent vertex**, the post it just came from. Any other neighbor that has already been reached closes a ring. This check is blind in two places. It says nothing at all about posts the walk never reached, and it knows only post numbers, so a doubled string between the same two posts is noticed only if the neighbor lists keep both copies.

<!-- names: edge count rule, forest, parent vertex -->

<!-- stage: variables -->
### Posts, Strings And The Walk

The integer `n` is the number of posts and `cables` is the list of strings, each a pair of post numbers. The array `adj` holds, for every post, the list of posts it shares a string with, and each string is written into two lists. The boolean array `seen` marks posts the walk has reached, and `reached` counts them. During the ring walk, `v` is the post being expanded, `w` is a neighbor under test, and `parent` is the post the walk came from, with -1 standing for a starting post that has none.

<!-- stage: trace -->
### One Clean Tree And One Hidden Ring

The first trace walks a six-post park whose strings are 0-1, 0-2, 1-3, 1-4 and 2-5, using the parent rule and visiting neighbors in the order they were hung. The pointer `cur` is the post being expanded. Each post except the first skips the one string back to the post it came from, so no ring is reported, and the final step compares the number of posts reached with n.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"parent":-1,"reached":1},"note":"Post 0 is entered as the start."},{"at":{"cur":1},"vars":{"parent":0,"reached":2},"note":"Post 1 is entered from post 0."},{"at":{"cur":1},"vars":{"parent":0,"reached":2},"note":"Post 0 is the parent vertex of post 1, so that string is skipped."},{"at":{"cur":3},"vars":{"parent":1,"reached":3},"note":"Post 3 is entered from post 1."},{"at":{"cur":3},"vars":{"parent":1,"reached":3},"note":"Post 1 is the parent vertex of post 3, so that string is skipped."},{"at":{"cur":1},"vars":{"parent":0,"reached":3},"note":"The walk returns to post 1 with 3 posts reached so far."},{"at":{"cur":4},"vars":{"parent":1,"reached":4},"note":"Post 4 is entered from post 1."},{"at":{"cur":4},"vars":{"parent":1,"reached":4},"note":"Post 1 is the parent vertex of post 4, so that string is skipped."},{"at":{"cur":1},"vars":{"parent":0,"reached":4},"note":"The walk returns to post 1 with 4 posts reached so far."},{"at":{"cur":0},"vars":{"parent":-1,"reached":4},"note":"The walk returns to post 0 with 4 posts reached so far."},{"at":{"cur":2},"vars":{"parent":0,"reached":5},"note":"Post 2 is entered from post 0."},{"at":{"cur":2},"vars":{"parent":0,"reached":5},"note":"Post 0 is the parent vertex of post 2, so that string is skipped."},{"at":{"cur":5},"vars":{"parent":2,"reached":6},"note":"Post 5 is entered from post 2."},{"at":{"cur":5},"vars":{"parent":2,"reached":6},"note":"Post 2 is the parent vertex of post 5, so that string is skipped."},{"at":{"cur":2},"vars":{"parent":0,"reached":6},"note":"The walk returns to post 2 with 6 posts reached so far."},{"at":{"cur":0},"vars":{"parent":-1,"reached":6},"note":"The walk returns to post 0 with 6 posts reached so far."},{"at":{"cur":0},"vars":{"parent":-1,"reached":6},"note":"No ring was found and 6 posts were reached, which equals n = 6, so the layout is a tree."}]}
```

The second trace is a five-post park with strings 0-1, 1-2, 2-0 and 3-4. It has n - 1 = 4 strings, so the count rule lets it through, and the plain walk from post 0 then only marks posts as reached with no parent logic at all. It circles the triangle once, stops adding posts, and never meets posts 3 and 4. The shortfall of two posts is how the hidden ring gets caught.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"strings":4,"reached":1},"note":"The list holds 4 strings and n - 1 is 4, so the count rule passes. Post 0 is marked as reached."},{"at":{"cur":0},"vars":{"strings":4,"reached":3},"note":"Post 0 is expanded and marks posts 1, 2."},{"at":{"cur":2},"vars":{"strings":4,"reached":3},"note":"Post 2 is expanded; every neighbor is already marked."},{"at":{"cur":1},"vars":{"strings":4,"reached":3},"note":"Post 1 is expanded; every neighbor is already marked."},{"at":{"cur":0},"vars":{"strings":4,"reached":3},"note":"The walk is finished with 3 posts reached out of 5, so posts 3 and 4 are cut off and the answer is false."}]}
```

<!-- stage: code -->
### Count First, Then Walk Once

```java
final class LightLayout {
    static boolean isTree(int n, int[][] cables) {
        if (cables.length != n - 1) return false;
        List<List<Integer>> adj = build(n, cables);
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        seen[0] = true;
        stack.push(0);
        int reached = 1;
        while (!stack.isEmpty()) {
            int v = stack.pop();
            for (int w : adj.get(v)) {
                if (!seen[w]) {
                    seen[w] = true;
                    reached++;
                    stack.push(w);
                }
            }
        }
        return reached == n;
    }

    static boolean ringByParent(int n, int[][] cables) {
        List<List<Integer>> adj = build(n, cables);
        boolean[] seen = new boolean[n];
        for (int s = 0; s < n; s++) {
            if (!seen[s] && walk(adj, seen, s, -1)) return true;
        }
        return false;
    }

    private static boolean walk(List<List<Integer>> adj, boolean[] seen, int v, int parent) {
        seen[v] = true;
        for (int w : adj.get(v)) {
            if (w == parent) continue;
            if (seen[w] || walk(adj, seen, w, v)) return true;
        }
        return false;
    }

    private static List<List<Integer>> build(int n, int[][] cables) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] c : cables) {
            adj.get(c[0]).add(c[1]);
            adj.get(c[1]).add(c[0]);
        }
        return adj;
    }
}
```

The tree test needs no parent at all, because the count has already ruled out every layout where a ring and a missing piece could cancel out. Both routines run in O(n + m) time and use O(n + m) space for the lists, and the recursive one also needs stack depth up to n.

<!-- stage: applicability -->
### When Strings Must Form One Tree

Reach for this when a question says "connected with no cycle", "exactly one route between any two", "n nodes and n - 1 links", or asks whether a pile of undirected links forms a tree: cable layouts, pipe networks, a family of folders under one root, a spanning structure for a network. The invariant to defend is that a post seen again is a ring only if it is not the post you just came from, and that a ring-free answer covers only the posts the walk actually reached.

The false friend is borrowed machinery. Directed three-color marking is unnecessary for undirected rings, since every link is two-way and a finished post can still be a neighbor of a later one without any harm. The parent check has a second weakness of its own: it accepts a layout with two disconnected pieces, because a forest has no ring.

Do not use the parent rule when the input may hold parallel strings that count as a ring and the neighbors are kept in a set. A set stores each neighbor once, so a doubled cable collapses into a single one and slips through, and you need lists that keep repeats or a comparison of counts instead. In Java, `Collections.nCopies(n, new ArrayList<Integer>())` fills the list with one shared list, so every post would share the same neighbors. Build a fresh list per post in a loop. Deep chains of posts also make the recursive walk risky for very large n, and the stack version avoids that.

<!-- stage: exercises -->
### Exercises

#### [Build] DFS With Parent (Author exercise)
<!-- id: ug-dfs-parent -->

**Prerequisites.** The parent vertex rule from this lesson, and the cycle vocabulary of the previous chapter's cycle detection lesson.

**Problem.** The graph has `n` vertices numbered 0 to n - 1 and the undirected edges `edges`, where each `edges[i] = [a, b]`. Return `true` if the graph contains a cycle in any of its pieces, and `false` otherwise. Write a depth-first walk that passes the vertex it came from into every call and ignores that one neighbor. The graph is simple: no self-loops and no pair of vertices joined by two edges. The input is not modified.

**Constraints.** 1 <= n <= 200, 0 <= edges.length <= 400, and each pair of distinct vertices appears at most once.

**Example 1.** Input `n = 5, edges = [[0,1],[1,2],[2,0],[3,4]]`, output `true`.

**Example 2.** Input `n = 6, edges = [[0,1],[1,2],[1,3],[4,5]]`, output `false`.

**Hint.** What does a vertex see when it looks back along the very edge it was entered by, and which single neighbor must it therefore pass over?

**Changed decision.** Every call receives the vertex it was entered from, so an already seen neighbor counts as a cycle only when it is a different vertex.

#### [Vary] Detect A Triangle (Author exercise)
<!-- id: ug-triangle -->

**Prerequisites.** The DFS With Parent rung.

**Problem.** The graph is simple and undirected, with vertices 0 to n - 1. Return the three vertices of a triangle, meaning three vertices that are pairwise joined by edges, as an `int[]` of length 3 in increasing order. If several triangles exist, return the one that is smallest when compared first vertex, then second, then third. If there is none, return an empty array. The input is not modified.

**Constraints.** 1 <= n <= 60, 0 <= edges.length <= 300, and each pair of distinct vertices appears at most once.

**Example 1.** Input `n = 6, edges = [[0,1],[1,2],[2,3],[3,1],[3,4],[4,5]]`, output `[1,2,3]`.

**Example 2.** Input `n = 4, edges = [[0,1],[1,2],[2,3],[3,0]]`, output `[]`.

**Hint.** After stepping from a vertex p to a neighbor v, which neighbors of v should be tested against p's own neighbors?

**Changed decision.** The seen neighbor of interest must also be adjacent to the parent, which turns a general ring test into a test for rings of length exactly three.

#### [Boundary] Single Edge And Parallel Edges (Author exercise)
<!-- id: ug-parallel-edges -->

**Prerequisites.** The Detect A Triangle rung, and the forest idea that a ring-free piece with k vertices has k - 1 edges.

**Problem.** The graph has vertices 0 to n - 1 and an `edges` list that may repeat a pair or hold a self-loop `[v, v]`. Each entry is a separate cable. The contract is exact: two entries joining the same pair form a cycle, a self-loop is a cycle, and one lone entry is not. Return `true` if some cycle exists, otherwise `false`. The input is not modified.

**Constraints.** 1 <= n <= 100, 0 <= edges.length <= 300, and each entry holds two vertices in the range 0 to n - 1.

**Example 1.** Input `n = 4, edges = [[0,1],[1,2],[2,1]]`, output `true`.

**Example 2.** Input `n = 3, edges = [[0,1]]`, output `false`.

**Hint.** If you compare each piece's vertex count with its number of edges, what do two copies of the same pair do to that comparison?

**Changed decision.** The walk is replaced by edge counting per piece, so a doubled edge is judged by the rules of the contract and not by whether a neighbor looks like the parent.

#### [Recognize] Graph Valid Tree (LeetCode 261)
<!-- id: ug-valid-tree -->

**Prerequisites.** The Single Edge And Parallel Edges rung and the edge count rule from the insight stage.

**Problem.** The input is an integer `n` and an array `edges` of undirected edges, where `edges[i] = [a, b]` joins vertices a and b out of 0 to n - 1. Return `true` if the edges make the graph a valid tree, meaning it is connected and has no cycle, and `false` otherwise. The input is not modified.

**Constraints.** 1 <= n <= 2000, 0 <= edges.length <= 5000, no self-loops, and no pair of vertices repeats.

**Example 1.** Input `n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]`, output `true`.

**Example 2.** Input `n = 6, edges = [[0,1],[1,2],[2,0],[3,4],[4,5]]`, output `false`.

**Hint.** The second example has exactly n - 1 edges. What does one walk from vertex 0 find missing?

**Changed decision.** The answer needs a connectivity test as well as a cycle test, and the edge count lets one reach count replace both.
