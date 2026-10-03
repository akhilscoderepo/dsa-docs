<!-- lesson-kind: standard -->
<!-- lesson-id: diameter-and-subtree-returns -->
## Diameter And Subtree Returns

<!-- stage: context -->
### The Longest Ride On The Lift Network

A mountain resort has a network of chairlifts that branches like a tree. One station at the top feeds two lifts below it, each of those feeds up to two more, and so on, and there is exactly one way between any two stations. The manager wants the longest journey a guest can take between two stations, where the guest may ride down one branch and up another, counting the number of lift segments.

Every station sends a short radio report to the station above it, and the manager wonders what that report should say. A station knows what hangs below it, but the station above can only continue a journey through one of the stations below, since a guest cannot be on two lifts at once. The longest journey might not even touch the top station.

<!-- stage: naive -->
### Ask For Heights At Every Station

The direct method treats each station as a possible peak of the journey. For every station it asks how tall the left side is and how tall the right side is, adds the two heights, and keeps the best sum found over all stations. The heights come from a separate helper that measures a side from scratch.

```java
static int height(Node node) {
    if (node == null) return 0;
    return 1 + Math.max(height(node.left), height(node.right));
}

static int diameter(Node node) {
    if (node == null) return 0;
    int through = height(node.left) + height(node.right);
    return Math.max(through, Math.max(diameter(node.left), diameter(node.right)));
}
```

A longest journey bends at exactly one station, its highest point, so checking every station as that point finds the best one.

<!-- stage: bottleneck -->
### Heights Are Measured Again And Again

The helper walks the whole side below a station every time it is called, and it is called at every station. On a network that is one long line, the top station measures n - 1 stations below it, the next one n - 2, and so on, so the heights alone cost O(n^2). For a hundred thousand stations that is about five billion steps, though each station is already measured once by the recursion that visits it.

The waste is that the height of a side is exactly what the recursion into that side computes on the way. A station visited after its two sides could take their heights as return values, add them for its own candidate, and pass up its own height for the station above. Each station would then be visited once, with O(1) work, for O(n) in total, and the radio report from a station would be one number.

<!-- stage: insight -->
### Report One Branch Answer Another

The walk returns, from every station, the length of its **upward branch**, the longest downward ride that starts at that station and goes through only one of the sides. That is the one fact the station above can use, because its own journey may continue through a single side only. In a postorder call, both sides have already reported, so the station knows the two branch lengths left and right.

The station is also a possible **turning node**, the highest point of a journey that rides down the left side and down the right side. The best journey that turns here has length left plus right. This sum is an answer and not a report: it is compared with the **running best**, a variable outside the recursion, and then it is dropped. What goes up to the parent is only the larger of the two sides plus one for the segment to the parent, or the height.

The invariant is that the returned number is always a single downward branch, while the running best holds the best complete journey over all stations finished so far. Every journey has one highest station, and that station considers it when it is finished, so the final running best is the answer. Each station is visited once, so the work is O(n).

<!-- names: upward branch, turning node, running best -->

A report that included both sides would describe a fork, which no guest can ride as one journey.

<!-- stage: variables -->
### Return Value And Running Best

The helper has a return value and a side effect, and they must not be mixed. The return value is the height `1 + max(left, right)`, with 0 for a null side. The side effect is the update `best = Math.max(best, left + right)`, which counts segments when heights are measured in nodes. The running best lives in a field or a one-element array that outlives every call and is reset before each fresh walk, and it starts at 0 for lengths, which cannot be negative. The same pattern for sums needs a different starting value, since sums can be negative.

<!-- stage: trace -->
### Height Goes Up While Best Stays

The first trace walks the lift network 1, 2, 3, 4, 5 in level-order form for the longest journey in segments. The pointer `node` marks the station that has just heard both of its sides. Its columns are the branch it reports to its parent and the best complete journey seen so far. The station 2 sees two leaves below it, so it reports a branch of 2 upward, while it counts a journey of 2 turning at itself, and the top station finds a longer one.

```trace
{"cells":["1","2","3","4","5"],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"reports":1,"best":0},"note":"The station 4 has branches 0 and 0 below it, so a journey turning here has 0 segments, and it reports a branch of 1 upward."},{"at":{"node":4},"vars":{"reports":1,"best":0},"note":"The station 5 has branches 0 and 0 below it, so a journey turning here has 0 segments, and it reports a branch of 1 upward."},{"at":{"node":1},"vars":{"reports":2,"best":2},"note":"The station 2 has branches 1 and 1 below it, so a journey turning here has 2 segments, and it reports a branch of 2 upward."},{"at":{"node":2},"vars":{"reports":1,"best":2},"note":"The station 3 has branches 0 and 0 below it, so a journey turning here has 0 segments, and it reports a branch of 1 upward."},{"at":{"node":0},"vars":{"reports":3,"best":3},"note":"The station 1 has branches 2 and 1 below it, so a journey turning here has 3 segments, and it reports a branch of 3 upward."}]}
```

The second trace uses a variant with labels that may be negative, on the index -10, 9, 20, null, null, 15, 7, where each station adds its own number to its branch and the journey value is the best sum along a bent route. A branch with a negative total is not worth continuing, so it is reported as 0. Observe that the best journey is settled at the station 20 and that the root cannot improve on it, though the root reports a branch upward.

```trace
{"cells":["-10","9","20","null","null","15","7"],"pointers":["node"],"steps":[{"at":{"node":1},"vars":{"reports":9,"best":9},"note":"The station 9 adds its label to the branches 0 and 0, giving 9 for a journey turning here, and it reports 9 upward."},{"at":{"node":5},"vars":{"reports":15,"best":15},"note":"The station 15 adds its label to the branches 0 and 0, giving 15 for a journey turning here, and it reports 15 upward."},{"at":{"node":6},"vars":{"reports":7,"best":15},"note":"The station 7 adds its label to the branches 0 and 0, giving 7 for a journey turning here, and it reports 7 upward."},{"at":{"node":2},"vars":{"reports":35,"best":42},"note":"The station 20 adds its label to the branches 15 and 7, giving 42 for a journey turning here, and it reports 35 upward."},{"at":{"node":0},"vars":{"reports":25,"best":42},"note":"The station -10 adds its label to the branches 9 and 35, giving 34 for a journey turning here, and it reports 25 upward."}]}
```

<!-- stage: code -->
### One Pass With A Side Effect

```java
final class DiameterWalk {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int best;

    static int branch(Node node) {
        if (node == null) return 0;
        int left = branch(node.left);
        int right = branch(node.right);
        best = Math.max(best, left + right);
        return 1 + Math.max(left, right);
    }

    static int diameter(Node root) {
        best = 0;
        branch(root);
        return best;
    }
}
```

Each node is entered once and does constant work, so the time is O(n), and the stack is O(h). The value `left + right` counts edges because the heights are counted in nodes.

<!-- stage: applicability -->
### When The Best Path May Turn

This pattern fits any question about a best path in a tree that may bend at one node: longest path, heaviest path, longest run of equal labels, or most expensive route between two nodes. The invariant is that each call returns the best single branch from its node and updates a separate running best with the best bent path through it.

A false friend is returning the two-sided value, which seems natural because it is the larger number, but a parent adding it to its own side would build a path that visits the same node twice. A second false friend is the diameter that must pass through the root, which is the weaker question, since the best journey may lie entirely in one side. A third is mixing units, so that a height counted in nodes is read as edges.

In Java, keep the running best where every call can reach it and reset it at the start of each walk, because a static field left over from the previous tree silently corrupts the next answer. Choose its starting value to suit the question.

<!-- stage: exercises -->
### Exercises

#### [Build] Return Subtree Height (Author exercise)
<!-- id: tr-subtree-height -->

**Prerequisites.** The Depth And Path State lesson and the idea of returned values.

**Problem.** Given a level-order tree, return `[height, uneven]`, where height counts nodes on the longest downward route from the root and `uneven` counts the nodes whose left and right subtree heights differ. Both heights of a node must be known before its own result is formed. The empty tree gives `[0, 0]`.

**Constraints.** 0 <= values.length <= 5000 and values are integers between -100 and 100.

**Example 1.** Input `values = [1, 2, 3]`, output `[2, 0]`.

**Example 2.** Input `values = [1, 2, null, 3]`, output `[3, 2]`.

**Hint.** When can a node compare its two sides, and what does it hand upward?

**Changed decision.** The node waits for both child heights, uses them to update a counter, and then returns only its own height.

#### [Vary] Diameter of Binary Tree (LeetCode 543)
<!-- id: tr-diameter-of-tree -->

**Prerequisites.** The Return Subtree Height rung.

**Problem.** For a level-order tree, return the number of edges on the longest path between any two nodes. The path need not pass through the root.

**Constraints.** 0 <= values.length <= 5000 and values are integers between -100 and 100.

**Example 1.** Input `values = [1, 2, 3, 4, 5]`, output `3`.

**Example 2.** Input `values = [1, 2]`, output `1`.

**Hint.** What is the best journey that turns at a node, and what may the parent receive?

**Changed decision.** A running best takes the sum of the two heights at every node, while the return value stays a single height.

#### [Boundary] Nodes Versus Edges (Author exercise)
<!-- id: tr-nodes-versus-edges -->

**Prerequisites.** The Diameter rung and its height convention.

**Problem.** For a level-order tree, return `[edges, nodes]`, the longest path between two nodes measured in edges and in nodes. A single node gives `[0, 1]` and the empty tree gives `[0, 0]`. State which unit your returned height uses and keep it consistent.

**Constraints.** 0 <= values.length <= 5000 and values are integers between -100 and 100.

**Example 1.** Input `values = [7]`, output `[0, 1]`.

**Example 2.** Input `values = [1, 2, 3, 4, 5]`, output `[3, 4]`.

**Hint.** If heights count nodes, what does the sum of two heights count? What changes for the other unit?

**Changed decision.** Heights count nodes, so the sum of two heights gives edges, and one more node is added only when a path exists at all.

#### [Recognize] Binary Tree Maximum Path Sum (LeetCode 124)
<!-- id: tr-max-path-sum -->

**Prerequisites.** The Nodes Versus Edges rung and the idea of discarding a bad branch.

**Problem.** For a level-order tree, return the largest sum of node values over any non-empty path that follows parent-child links, visits each node at most once, and need not use the root. Values may be negative.

**Constraints.** 1 <= values.length <= 3000 and values are integers between -1000 and 1000.

**Example 1.** Input `values = [2, -1, 3, null, 4]`, output `8`.

**Example 2.** Input `values = [-4]`, output `-4`.

**Hint.** When is a branch worth continuing, and what must the running best start at?

**Changed decision.** A branch reported upward is cut off at zero when it would only lower the total, while the complete answer at a node may use both sides.
