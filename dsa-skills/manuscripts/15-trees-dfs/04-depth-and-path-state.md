<!-- lesson-kind: standard -->
<!-- lesson-id: depth-and-path-state -->
## Track Depth And Paths Down A Tree

<!-- stage: context -->
### Paths That Keep Old Folder Names

A directory lister prints the full path of every file under a folder. The developer keeps one `StringBuilder` for the current path. The walk appends a folder name before it enters the folder, and then it prints the path at each file. The first folder prints correctly as `src/docs/intro.txt`. The next folder under `src` prints `src/docs/img/logo.png`, which is wrong, because the name `docs` stayed in the builder after the walk left that folder.

The walk carried a piece of information downward and never took it back. The question is how a recursive walk keeps facts about the route from the root to the current node, and how it keeps facts about a finished subtree.

<!-- stage: naive -->
### Copying The Whole Route At Every Node

The first fix avoids the shared builder. Each call receives its own copy of the route and adds its node to the copy. At a leaf, the method checks whether the values on the route add up to a target.

```java
import java.util.*;

final class RouteCopies {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static boolean hasRouteWithSum(Node node, List<Integer> route, int target) {
        if (node == null) return false;                          // a missing child ends no route
        List<Integer> mine = new ArrayList<>(route);             // a private copy for this call
        mine.add(node.val);                                      // extend the copy with this node
        if (node.left == null && node.right == null) {           // a node without children ends a route
            int sum = 0;
            for (int v : mine) sum += v;                         // add up the whole route again
            return sum == target;
        }
        return hasRouteWithSum(node.left, mine, target) || hasRouteWithSum(node.right, mine, target);
    }
}
```

Take the tree with root 8, right child 10, and left child 3 with children 1 and 6. With an empty list and target 12, the method returns `true`, because route 8, 3, 1 sums to 12. No call can leave leftover names behind, because every call owns its copy.

<!-- stage: bottleneck -->
### Counting The Copies

```predict
The tree is a chain of n nodes, and no route reaches the target. How many values does the method copy in total, and how many values does it add up at the leaf?

The call at depth k copies a list of k - 1 values, so the copies cost 0 + 1 + ... + (n - 1) values in total, which is O(n^2). The leaf adds up all n values once.
```

The time is O(n^2) on a chain, and the extra memory is O(n^2) in total, because every open call keeps its own copy. The method repeats work in two ways. Every call rebuilds a list that its parent already held, and the leaf adds up values that the calls above it had already seen.

Both costs come from the same choice. The method stores the whole route and recomputes facts from it. If each call received the fact it needs, such as how much of the target is still missing, it would need no list at all. If the walk does need the list, as when the answer must print the route, one shared list could be extended and then shortened again.

<!-- stage: insight -->
### Passing Facts Down And Returning Facts Up

A tree walk moves two kinds of information, and keeping them apart removes both costs.

<!-- names: downward state, upward state, backtracking -->

#### Downward State Describes The Route

The **downward state** is information about the route from the root to the current node. Examples are the number of nodes on the route, the amount of the target still missing, and the list of values on the route. The caller computes it before the child call and passes it as an argument. The depth of a node is the number of nodes on the route from the root to it, so the root has depth 1.

#### A Value Passed By Value Needs No Undo

An `int` argument is copied into each call. A call that passes `remaining - node.val` to its children creates a new value and leaves its own `remaining` unchanged. Two sibling calls cannot disturb each other, so nothing needs undoing afterward.

#### A Shared List Needs Backtracking

A `List` argument is different, because every call receives a reference to the same object. A call that adds its node before the child calls changes what its siblings see. **Backtracking** is the step that undoes the last change on the way back: the call removes its node after both child calls return. The list then holds exactly the route to the node that is active, at every moment.

#### Upward State Summarizes A Finished Subtree

The **upward state** is the return value of a call. It describes the whole subtree below the node, such as its height, which is the number of nodes on the longest downward path from that node. The height of the empty tree is 0. A node computes its height as one plus the larger height of its two children, so the parent never needs to look inside the subtree again.

<!-- stage: variables -->
### What Each Call Holds

- **depth** is the number of nodes on the route from the root to the current node, passed down by value.
- **remaining** is the target minus the values on the route, passed down by value.
- **route** is the list of values on the route, one shared object that every call extends and then shortens.
- **height** is the number of nodes on the longest downward path, and it is the value that a call returns.

A node with no children ends a route. A route counts as complete only there, unless the problem says otherwise.

<!-- stage: trace -->
### Following The Route List

#### Extending And Shortening The List

The tree has root 8 and right child 10. The root's left child is 3, which has children 1 and 6. The target is 12. A step shows the node of an active call. The variable `route` lists the values on the route, and `remaining` is 12 minus their sum.

```trace
{"cells":["8","3","10","1","6"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"route":"8","remaining":4},"note":"The call on the node 8 adds its value to the list. The remaining amount is 4, and the call continues to its children."},{"at":{"node":1},"vars":{"route":"8 3","remaining":1},"note":"The call on the node 3 adds its value to the list. The remaining amount is 1, and the call continues to its children."},{"at":{"node":3},"vars":{"route":"8 3 1","remaining":0},"note":"The call on the leaf 1 adds its value. The remaining amount is 0, so this route matches."},{"at":{"node":3},"vars":{"route":"8 3","remaining":1},"note":"Both children of the node 1 are done, so the call removes its value from the list."},{"at":{"node":4},"vars":{"route":"8 3 6","remaining":-5},"note":"The call on the leaf 6 adds its value. The remaining amount is -5, so this route does not match."},{"at":{"node":4},"vars":{"route":"8 3","remaining":1},"note":"Both children of the node 6 are done, so the call removes its value from the list."},{"at":{"node":1},"vars":{"route":"8","remaining":4},"note":"Both children of the node 3 are done, so the call removes its value from the list."},{"at":{"node":2},"vars":{"route":"8 10","remaining":-6},"note":"The call on the leaf 10 adds its value. The remaining amount is -6, so this route does not match."},{"at":{"node":2},"vars":{"route":"8","remaining":4},"note":"Both children of the node 10 are done, so the call removes its value from the list."},{"at":{"node":0},"vars":{"route":"empty","remaining":12},"note":"Both children of the node 8 are done, so the call removes its value from the list."}]}
```

The route 8, 3, 1 ends at a leaf with remaining 0, so it matches. After each call returns, its value leaves the list, so the call on node 6 starts from the route 8, 3.

#### Forgetting To Shorten The List

The second run uses the same tree and skips the removal step. The list keeps every value that was ever added.

```trace
{"cells":["8","3","10","1","6"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"route":"8","remaining":4},"note":"The call on the node 8 adds its value to the list. The remaining amount is 4, and the call continues to its children."},{"at":{"node":1},"vars":{"route":"8 3","remaining":1},"note":"The call on the node 3 adds its value to the list. The remaining amount is 1, and the call continues to its children."},{"at":{"node":3},"vars":{"route":"8 3 1","remaining":0},"note":"The call on the leaf 1 adds its value. The remaining amount is 0, so this route matches."},{"at":{"node":4},"vars":{"route":"8 3 1 6","remaining":-6},"note":"The call on the leaf 6 adds its value to a list that still holds 1. The remaining amount shows -6, but the route to this node is 8, 3, 6 with remaining -5."},{"at":{"node":2},"vars":{"route":"8 3 1 6 10","remaining":-16},"note":"The call on the leaf 10 adds its value. The remaining amount is -16, so this route does not match."}]}
```

At the leaf 6 the list holds 8, 3, 1, 6 and the remaining amount is negative. The route to node 6 is 8, 3, 6, so the real remaining amount is -5. The leftover value 1 gives a wrong answer for every later leaf.

<!-- stage: code -->
### Three Walks That Carry State

```java
import java.util.*;

final class PathState {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static int height(Node node) {
        if (node == null) return 0;                              // the empty tree has height 0
        int l = height(node.left);                               // the finished left subtree reports its height
        int r = height(node.right);                              // the finished right subtree reports its height
        return 1 + Math.max(l, r);                               // one more node than the taller side
    }

    static int countAtDepth(Node node, int depth, int wanted) {
        if (node == null) return 0;
        if (depth == wanted) return 1;                           // deeper nodes cannot have this depth
        return countAtDepth(node.left, depth + 1, wanted)        // depth + 1 is a new value for each child
             + countAtDepth(node.right, depth + 1, wanted);
    }

    static void routes(Node node, List<Integer> route, List<String> out) {
        if (node == null) return;
        route.add(node.val);                                     // extend the shared list before the child calls
        if (node.left == null && node.right == null) out.add(route.toString());   // a leaf ends a route
        routes(node.left, route, out);
        routes(node.right, route, out);
        route.remove(route.size() - 1);                          // backtrack after both child calls
    }
}
```

The `int` parameters need no cleanup. The shared list needs the last statement of `routes`. The method removes by index. A call such as `route.remove(Integer.valueOf(v))` deletes the first equal value, which can be an earlier entry of the route.

- **Time** is O(n) for `height` and `countAtDepth`, because each node receives one call. `routes` costs O(n) plus the length of each stored route string.
- **Space** is O(h) in the stack of pending calls and the shared list, because only one route is live at a time.

<!-- stage: applicability -->
### Choosing What To Pass Or Return

#### Sorting The Facts By Direction

Ask of each fact whether it describes the route above the node or the subtree below it. Route facts such as depth and remaining target travel down as arguments. Subtree facts such as height travel up as return values. The invariant is that a downward fact is extended before the child call and restored afterward, and an upward fact is complete when the call returns.

#### Finding The False Friend

An integer passed by value and a list passed by reference both look like arguments, and that is the false friend. The integer needs no undo, and the list needs backtracking. A route stored in a shared list also needs a copy when it is saved, such as `new ArrayList<>(route)`. Saving the shared list itself stores a reference, and later calls change it.

#### No-Go Conditions

If the answer needs the route to be reversible at no cost, a persistent structure is needed, which this chapter does not cover. Some questions compare nodes on different branches, such as the longest path between any two nodes. A single downward fact is not enough there, and the next lesson adds a second kind of return value.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Depth Of Binary Tree (LeetCode 104)
<!-- id: dp-height -->

**Prerequisites.** The upward state and the height from this lesson.

**Problem.** A binary tree has a root. The depth of the tree is the number of nodes on the longest path from the root down to a leaf. Return the depth. An empty tree has depth 0.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers that the answer does not use.
- **Answer** is an integer between 0 and 10^4.
- **Mutation** is not allowed.

**Example 1.** Input root 9 with left child 4 and right child 7, output 4. Node 4 has a left child 2, and node 7 has a right child 8 that has a right child 1.

**Example 2.** Input root 3 with a left child 1 and no right child, output 2.

**Hint.** What does a call return for `null`? How does a node combine the two numbers that its children return?

**Changed decision.** The return value of each call replaces any stored route.

#### [Vary] Path Sum (LeetCode 112)
<!-- id: dp-path-sum -->

**Prerequisites.** The exercise above and the remaining amount from this lesson.

**Problem.** Given a binary tree and an integer `target`, return `true` if some path from the root to a leaf has values that add up to `target`. A leaf is a node with no children. An empty tree has no path.

**Constraints.** The limits are:
- **Nodes** number between 0 and 5000.
- **Values** are integers between -1000 and 1000.
- **Target** is an integer between -5000 and 5000.
- **Answer** is a `boolean`, and the method never changes the tree.

**Example 1.** Input root 8 with left child 3 and right child 10, where node 3 has children 1 and 6, and `target = 12`, output `true`.

**Example 2.** Input the same tree and `target = 11`, output `false`, because the sum 11 ends at the node 3, which has children.

**Hint.** What do you pass to each child so that no list is needed? What must a call check before it compares the amount with zero?

**Changed decision.** The route is replaced by one integer that is passed by value.

#### [Boundary] Leaf Versus Internal Match (Author exercise)
<!-- id: dp-leaf-count -->

**Prerequisites.** The two exercises above.

**Problem.** Given a binary tree and an integer `target`, return the number of paths from the root to a leaf whose values add up to `target`. A path that reaches the sum at a node with children does not count. Count every matching leaf, and do not stop at the first one.

**Constraints.** The limits are:
- **Nodes** number between 0 and 5000.
- **Values** are integers between -1000 and 1000.
- **Target** is an integer between -5000 and 5000.
- **Answer** is an integer between 0 and the number of leaves.

**Example 1.** Input root 5 with only a left child 3, and `target = 5`, output 0. The sum 5 is reached at the root, which is not a leaf.

**Example 2.** Input root 2 with left child 3 and right child 3, and `target = 5`, output 2.

**Hint.** What does a call on `null` return, and what does a call on a node with only one child return when its single child call fails?

**Changed decision.** The method counts and never returns early, and the leaf test decides every match.

#### [Recognize] Path Sum II (LeetCode 113)
<!-- id: dp-path-list -->

**Prerequisites.** All three exercises above.

**Problem.** Given a binary tree and an integer `target`, return every root-to-leaf path whose values add up to `target`. Each path is a list of node values from the root down. The order of the paths follows the left-before-right walk.

**Constraints.** The limits are:
- **Nodes** number between 0 and 5000.
- **Values** are integers between -1000 and 1000.
- **Target** is an integer between -5000 and 5000.
- **Answer** is a list of lists, empty when no path matches.

**Example 1.** Input root 8 with left child 3 and right child 10, where node 3 has children 1 and 6, and `target = 17`, output `[8, 3, 6]`.

**Example 2.** Input root 1 with left child 2 and right child 2, and `target = 3`, output `[1, 2]` and `[1, 2]`. The two lists come from different leaves.

**Hint.** One list holds the current route. When is a copy needed, and when does a value leave the list?

**Changed decision.** A shared list needs backtracking after both child calls, and a copy is taken at each match.
