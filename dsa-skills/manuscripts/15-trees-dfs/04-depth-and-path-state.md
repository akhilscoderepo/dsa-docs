<!-- lesson-kind: standard -->
<!-- lesson-id: depth-and-path-state -->
## Depth And Path State

<!-- stage: context -->
### The Ranger And The Chalk Sign List

A ranger walks the trails of a hill park that fork again and again. The park office asks two kinds of questions. Some are about distance from the gate: how many forks deep is the farthest spot, and how far is each spot from the entrance. Others are about the route taken to reach a spot: which signposts did a walker pass, and do the distances on the signposts along some route add up to a target number.

The ranger carries a board on which he chalks each signpost as he passes it, so he can report the whole route when he reaches a dead end. He must walk many routes that share their first stretch, and he wonders how to keep the board correct as he turns back from a dead end and takes the next fork.

<!-- stage: naive -->
### Copy The Whole Route At Each Fork

The direct method gives every step its own private copy of the route. At each signpost the ranger copies the board, adds the new signpost to the copy, and hands the copy on to whichever trail he takes next, so routes never disturb one another. A route is reported when it reaches a dead end.

```java
static void collect(Node sign, List<Integer> board, List<List<Integer>> all) {
    if (sign == null) return;
    List<Integer> here = new ArrayList<>(board);
    here.add(sign.val);
    if (sign.left == null && sign.right == null) all.add(here);
    collect(sign.left, here, all);
    collect(sign.right, here, all);
}
```

Each trail has a board of its own, so one route cannot damage the board of another, and every dead end reports a correct route.

<!-- stage: bottleneck -->
### Every Fork Copies A Growing Board

A copy of a board with d signposts costs d steps, and a copy is made at every one of the n signposts. On a trail that is one long line the copies have sizes 1, 2, 3 up to n, so the copying alone costs O(n^2) steps and as much memory is touched. For one hundred thousand signposts that is five billion element copies, though the question may only need one number such as the deepest fork.

Many of the questions need much less than the whole route. The distance from the gate is one number, and the sum of distances along the route is one number, so a whole list is overkill. For the questions that do need the route itself, a single list could serve all walks if the ranger kept it correct himself, by chalking a signpost on the way down and wiping it on the way back. The cost would then be O(1) per step plus the cost of reporting a finished route.

<!-- stage: insight -->
### Extend Down And Summarize Up

Information moves in two directions in a tree walk. **Downward state** is what the parent knows and hands to the child before the call: the number of steps from the root, the remaining target, or the route so far. **Upward summary** is what a finished subtree returns to its parent: the height, or whether a match was found. Every question in this lesson is a choice of what to pass down and what to return up.

A number such as the depth or the remaining target is passed by value, so each call has its own copy and nothing needs undoing. A shared list such as the route is different, because every call sees the same object. The call must add its node before the two child calls, and then perform a **restore step** that removes that node after both child calls return. With that discipline, when a call starts the list holds exactly the path from the root to the parent, and when the call ends the list is back to what it was.

Reporting a route needs a copy of the list taken at that moment, because the list will change as the walk continues. This copy is paid only for routes that match, instead of for every step.

The invariant is that the shared state during a call equals the root-to-node path, and a call leaves it as it found it, so each step costs O(1) apart from reports.

<!-- names: downward state, upward summary, restore step -->

An integer passed down needs no restore, and a list shared across calls always does.

<!-- stage: variables -->
### Depth, Remaining Target And Route

Depth questions need only a return value: a null subtree returns 0 and a node returns one plus the larger child result. A target question passes `remaining` down as an `int`, subtracting the node's value before the calls, and a leaf compares what is left with zero. A route question adds one more variable, the shared `path` list, which is appended to before the child calls and trimmed by `path.remove(path.size() - 1)` after them. The finished-route list stores a copy of `path`, never the list itself.

<!-- stage: trace -->
### Remaining Target And Chalk Board

The first trace carries a remaining target downward through the index 5, 4, 8, 11, null, 13, 4 given in level order, with the target 20. The pointer `node` marks the signpost being entered. The remaining amount goes down at every step by the label of the signpost, and only a dead end is allowed to decide. The walk enters the left branch first, so the route 5, 4, 11 is judged before the other branches are tried.

```trace
{"cells":["5","4","8","11","null","13","4"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"remaining":15},"note":"The signpost 5 is entered with 20 still needed, so its children are given 15."},{"at":{"node":1},"vars":{"remaining":11},"note":"The signpost 4 is entered with 15 still needed, so its children are given 11."},{"at":{"node":3},"vars":{"remaining":0},"note":"The signpost 11 is a dead end and the remaining amount is 0, so this route matches the target."},{"at":{"node":2},"vars":{"remaining":7},"note":"The signpost 8 is entered with 15 still needed, so its children are given 7."},{"at":{"node":5},"vars":{"remaining":-6},"note":"The signpost 13 is a dead end and the remaining amount is -6, which is not zero, so this route does not match."},{"at":{"node":6},"vars":{"remaining":3},"note":"The signpost 4 is a dead end and the remaining amount is 3, which is not zero, so this route does not match."}]}
```

The second trace keeps a shared chalk board on the index 1, 2, 3, 4, 5 for the target 7. A step that chalks a signpost shows the board growing, and a step that wipes one shows it shrinking to what it was before the call. Watch that the board reading `1 2` appears again after the dead end 4 is wiped, which is what allows the next trail to start from the right route.

```trace
{"cells":["1","2","3","4","5"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"board":"1","sum":1},"note":"The signpost 1 is chalked, and the board now holds the route to it with sum 1."},{"at":{"node":1},"vars":{"board":"1 2","sum":3},"note":"The signpost 2 is chalked, and the board now holds the route to it with sum 3."},{"at":{"node":3},"vars":{"board":"1 2 4","sum":7},"note":"The signpost 4 is chalked and is a dead end with sum 7, which equals 7, so the route is copied out."},{"at":{"node":3},"vars":{"board":"1 2","sum":3},"note":"Both trails below the signpost 4 are done, so its chalk mark is wiped and the board returns to its earlier state."},{"at":{"node":4},"vars":{"board":"1 2 5","sum":8},"note":"The signpost 5 is chalked and is a dead end with sum 8, which is not 7, so nothing is reported."},{"at":{"node":4},"vars":{"board":"1 2","sum":3},"note":"Both trails below the signpost 5 are done, so its chalk mark is wiped and the board returns to its earlier state."},{"at":{"node":1},"vars":{"board":"1","sum":1},"note":"Both trails below the signpost 2 are done, so its chalk mark is wiped and the board returns to its earlier state."},{"at":{"node":2},"vars":{"board":"1 3","sum":4},"note":"The signpost 3 is chalked and is a dead end with sum 4, which is not 7, so nothing is reported."},{"at":{"node":2},"vars":{"board":"1","sum":1},"note":"Both trails below the signpost 3 are done, so its chalk mark is wiped and the board returns to its earlier state."},{"at":{"node":0},"vars":{"board":"empty","sum":0},"note":"Both trails below the signpost 1 are done, so its chalk mark is wiped and the board returns to its earlier state."}]}
```

<!-- stage: code -->
### Depth And Path Walks

```java
final class PathWalks {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int maxDepth(Node node) {
        if (node == null) return 0;
        return 1 + Math.max(maxDepth(node.left), maxDepth(node.right));
    }

    static boolean hasPathSum(Node node, int remaining) {
        if (node == null) return false;
        remaining -= node.val;
        if (node.left == null && node.right == null) return remaining == 0;
        return hasPathSum(node.left, remaining) || hasPathSum(node.right, remaining);
    }

    static void routes(Node node, int remaining, List<Integer> path, List<List<Integer>> found) {
        if (node == null) return;
        path.add(node.val);
        remaining -= node.val;
        if (node.left == null && node.right == null && remaining == 0) found.add(new ArrayList<>(path));
        routes(node.left, remaining, path, found);
        routes(node.right, remaining, path, found);
        path.remove(path.size() - 1);
    }
}
```

Every node is entered once with constant work apart from copying a matching route, so the walks take O(n) time plus the length of every reported route. The space is the recursion depth O(h) plus the shared path.

<!-- stage: applicability -->
### When The Answer Depends On The Route

Use these walks when a result depends on how far a node is from the root, how tall a subtree is, or what lies along the way from the root. Examples are file path lengths, cumulative prices through a menu tree, and decision paths. The invariant is that the shared state during a call equals the path to its node and a call hands the state back as it found it.

A false friend is the integer that looks like the list. An integer passed down is copied, so nothing needs to be undone, while a list is shared and must be trimmed after the calls, and forgetting that leaves stale entries in every later route. A second false friend is a leaf test that is skipped: a target met at an internal node does not end a root-to-leaf path. A third is copying the path at every step, which is correct but quadratic.

In Java, record a route with `new ArrayList<>(path)`, since adding `path` itself stores a reference that later changes. Remove the last element by index, because `remove(Integer)` on a `List<Integer>` removes by value.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Depth of Binary Tree (LeetCode 104)
<!-- id: tr-depth-of-tree -->

**Prerequisites.** The tree representation and recursive traversal lessons.

**Problem.** A binary tree is given as a level-order array in which `null` marks a missing child and children of missing nodes are not listed. Report how many nodes lie on the longest downward route that starts at the root.

**Constraints.** 0 <= values.length <= 10000 and every value is an integer between -100 and 100.

**Example 1.** Input `values = [3, 9, 20, null, null, 15, 7]`, output `3`.

**Example 2.** Input `values = [1, null, 2]`, output `2`.

**Hint.** What is the depth of a null subtree, and how does a node use the depths of its two sides?

**Changed decision.** The answer travels upward as a return value, one plus the larger child result, with no state passed down.

#### [Vary] Path Sum (LeetCode 112)
<!-- id: tr-path-sum-exists -->

**Prerequisites.** The Maximum Depth rung and the passing of values down.

**Problem.** For the same level-order input and an integer `target`, return whether some path from the root down to a leaf has labels adding up to the target.

**Constraints.** 0 <= values.length <= 5000 and values and target are integers between -1000 and 1000.

**Example 1.** Input `values = [5, 4, 8, 11, null, 13, 4, 7, 2]`, `target = 22`, output `true`.

**Example 2.** Input `values = [1, 2, 3]`, `target = 5`, output `false`.

**Hint.** What number should be handed to a child, and where in the walk is it compared?

**Changed decision.** The remaining target goes down as an integer, so the state is copied for free and nothing is undone afterwards.

#### [Boundary] Leaf Versus Internal Match (Author exercise)
<!-- id: tr-leaf-versus-internal -->

**Prerequisites.** The Path Sum rung and its leaf test.

**Problem.** For a level-order tree and an integer `target`, return `[leafMatches, anyMatches]`, where `leafMatches` counts leaves whose root-to-node sum equals the target and `anyMatches` counts all nodes, leaf or not, with that sum. The empty tree gives `[0, 0]`.

**Constraints.** 0 <= values.length <= 5000 and values and target are integers between -1000 and 1000.

**Example 1.** Input `values = [1, 2]`, `target = 1`, output `[0, 1]`.

**Example 2.** Input `values = [3, 0, -3]`, `target = 3`, output `[1, 2]`.

**Hint.** Which nodes may end a counted path in each of the two numbers, and can the sum come back to the target after passing it?

**Changed decision.** A match is accepted at a leaf for the first count and at any node for the second, so the leaf test is the only line that separates them.

#### [Recognize] Path Sum II (LeetCode 113)
<!-- id: tr-path-sum-routes -->

**Prerequisites.** The Leaf Versus Internal Match rung and the shared list discipline.

**Problem.** For a level-order tree and an integer `target`, return every root-to-leaf path whose labels add up to the target, each as a list of values, with paths ordered by visiting the left subtree before the right.

**Constraints.** 0 <= values.length <= 2000 and values and target are integers between -1000 and 1000.

**Example 1.** Input `values = [5, 4, 8, 11, null, 13, 4, 7, 2, null, null, 5, 1]`, `target = 22`, output `[[5, 4, 11, 2], [5, 8, 4, 5]]`.

**Example 2.** Input `values = [1, 2]`, `target = 0`, output `[]`.

**Hint.** What is on the shared list when a call starts, and what must be true when it returns?

**Changed decision.** One list is extended before the child calls and trimmed after them, and a copy is stored only for a path that matches.
