<!-- lesson-kind: standard -->
<!-- lesson-id: graph-cloning -->
## Graph Cloning

<!-- stage: context -->
### Duplicating Linked Shapes

A diagram editor lets the user select a group of connected shapes and duplicate it. Each shape holds a number label and a list of references to the shapes it connects to. Three shapes labeled 0, 1 and 2 form a loop, which is a chain of references that returns to its first shape: shape 0 refers to shape 1, shape 1 refers to shape 2, and shape 2 refers back to shape 0.

The duplicate must hold three new shapes with the same labels. Each new shape must refer only to other new shapes. If one new shape still referred to an original shape, then moving the original would move part of the duplicate. A loop of references also means the editor cannot simply follow references until it reaches the end, because no end exists. The lesson answers one question: how does a program copy a structure of linked objects when references can loop and can point to the same object from several places?

<!-- stage: naive -->
### Copying Each Reference Recursively

Each shape is a `Node` object, and from here the lesson calls it a node. A node has an `int val` and a list `neighbors` of references to other `Node` objects. The direct approach copies a node by creating a new object with the same value. It then copies every node in `neighbors` the same way and adds the results to the new list.

```java
static Node copy(Node n) {
    Node result = new Node(n.val);
    for (Node next : n.neighbors) result.neighbors.add(copy(next));
    return result;
}
```

On a chain of nodes with no loops and no shared references, this method works. Every node is copied once, and the references of the new nodes point to new nodes. The method fails when the structure has a loop or a shared reference.

<!-- stage: bottleneck -->
### Counting Calls On Shared References

```predict
Node 0 refers to node 1, node 1 to node 2, and node 2 back to node 0. What does copy(node 0) do?

The call copies node 0, then copies node 1, then node 2, then node 0 again, and the chain of calls never ends. The method stops only when the call stack overflows with a StackOverflowError.
```

A loop is one failure. Shared references are a second failure, and it affects even structures without loops. Suppose node `i` refers to nodes `i + 1` and `i + 2`. Node 3 is then reachable from node 1 and from node 2. The method copies node 3 once for each way of reaching it, so it creates several different copies of one original node.

The number of copies grows exponentially in the number of nodes, which is O(2^n) in the worst case. For 40 nodes the method creates more than 10^8 copies, although the structure holds only 40 nodes. The result is also wrong, because the duplicate has many nodes where the original has one.

The method needs to remember which original node it has already copied. It must find that earlier copy again instead of making a new one.

<!-- stage: insight -->
### Keeping One Clone Per Original

The fix is a lookup table from each original node to the new node made for it. With it, every original is copied exactly once, and every reference to that original is rewired to the same copy. A copy built this way is a **deep copy**: it duplicates every node reachable from the start, so no node of the copy is also a node of the original.

#### Naming The Parts

A **node** is the object that stands for one vertex, and its `neighbors` list holds the neighbors of that vertex. A **clone** is the new node created for one original node. The **identity map** is a `HashMap<Node, Node>` named `clones`, which stores one entry per original node, with the original as the key and its clone as the value. The map compares keys by object identity and not by label, because `Node` does not override `equals`. A node is **discovered** the moment the method adds it to the map as a key.

<!-- names: clone, identity map, discovered -->

#### Why The Entry Comes First

For each original node, the method creates the clone and stores the entry before it looks at any neighbor. When a neighbor is already discovered, the method does not copy it again. It reads the existing clone from the map and adds that clone to the new list. This order is what ends a loop, because the second arrival at node 0 finds its entry already present. Storing the entry after the loop would repeat the endless chain of the naive method.

#### What The Map Guarantees

After each step, the map holds exactly one clone for each discovered original node, and no original node has two. This is the invariant of the lesson. It handles a shared reference as well as a loop, because a node reached by two paths is discovered by the first path and found in the map by the second.

<!-- stage: variables -->
### Four Names In The Copy

The copy uses four names.

- **start** is the original node that the caller passes, and it may be `null` for an empty structure.
- **clones** is the map from each discovered original node to its clone.
- **original** is the node being processed in the current call.
- **clone** is the new node created for `original`, and its `neighbors` list is filled during the call.

<!-- stage: trace -->
### Copying Two Small Graphs

#### A Loop With A Branch

Take four nodes with directed references: node 0 refers to 1, node 1 refers to 2, node 2 refers to 0 and 3, and node 3 refers to nothing. The pointer `cur` in each trace marks the original in hand, and `next` marks the neighbor under inspection. In the code below, `cur` is the variable `original`, `next` is the variable `next`, `clones` lists the keys of the map `clones`, and `count` equals `clones.size()`.

The method enters node 0, stores its clone, then follows the reference to node 1 and then to node 2. The first neighbor of node 2 is node 0, which is already in the map. The method reuses the existing clone of node 0, and the loop closes without a new call. The second neighbor, node 3, is new, so the method enters it and stores a fourth entry.

#### A Shared Target

Now take node 0 referring to 1 and 2, node 1 referring to 3, node 2 referring to 3, and node 3 referring to nothing. Node 3 can be reached by two paths. The method discovers it from node 1. When node 2 later lists node 3, the map already holds its clone, so the method reuses that clone. The result has four clones, one for each original node.

The two inputs show the same rule in two forms. A reference to a discovered node is always wired to the stored clone and never starts a new copy.

#### Stepping Through Both Graphs

The first trace follows the loop with a branch.

```trace
{"cells":[0,1,2,3],"pointers":["cur","next"],"steps":[{"at":{"cur":0,"next":-1},"vars":{"clones":"0","count":1},"note":"Node 0 enters the map with a new clone, and the walk follows its only reference."},{"at":{"cur":1,"next":-1},"vars":{"clones":"0,1","count":2},"note":"Node 1 gets its clone, and its reference leads to node 2."},{"at":{"cur":2,"next":-1},"vars":{"clones":"0,1,2","count":3},"note":"Node 2 gets its clone and lists nodes 0 and 3."},{"at":{"cur":2,"next":0},"vars":{"clones":"0,1,2","count":3},"note":"Node 0 already has a clone, so node 2 points its clone at it and the walk goes no deeper."},{"at":{"cur":3,"next":-1},"vars":{"clones":"0,1,2,3","count":4},"note":"Node 3 is new, so it gets the fourth clone and has no references to follow."}]}
```

The second trace follows the shared target.

```trace
{"cells":[0,1,2,3],"pointers":["cur","next"],"steps":[{"at":{"cur":0,"next":-1},"vars":{"clones":"0","count":1},"note":"Node 0 enters the map first and lists nodes 1 and 2."},{"at":{"cur":1,"next":-1},"vars":{"clones":"0,1","count":2},"note":"Node 1 gets a clone and lists node 3."},{"at":{"cur":3,"next":-1},"vars":{"clones":"0,1,3","count":3},"note":"Node 3 is discovered through node 1 and stored with its clone."},{"at":{"cur":2,"next":-1},"vars":{"clones":"0,1,3,2","count":4},"note":"Node 2 gets a clone after the branch through node 1 is finished."},{"at":{"cur":2,"next":3},"vars":{"clones":"0,1,3,2","count":4},"note":"Node 2 lists node 3, which the map already holds, so the existing clone is reused and no fifth clone appears."}]}
```

<!-- stage: code -->
### Copying With A HashMap

#### The Copy Method

The method `cloneGraph` guards against `null`, creates the map and starts the recursive helper. The helper stores the entry before the loop over the neighbors.

```java
final class CloneCode {
    static final class Node {
        int val;
        List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    static Node cloneGraph(Node start) {
        if (start == null) return null;
        return dfs(start, new HashMap<>());
    }

    static Node dfs(Node original, Map<Node, Node> clones) {
        Node clone = new Node(original.val);
        clones.put(original, clone);
        for (Node next : original.neighbors) {
            Node known = clones.get(next);
            clone.neighbors.add(known != null ? known : dfs(next, clones));
        }
        return clone;
    }
}
```

#### Cost Of The Copy

- **Time** is O(n + m), because each node is entered once and each reference is read once, with O(1) map work per step.
- **Space** is O(n) of auxiliary memory, because the map holds one entry per node and the recursion stack holds at most n calls. The returned clones are output and occupy O(n + m) in total.

The recursion depth can reach `n` on a long chain, so the method suits graphs of moderate size.

<!-- stage: applicability -->
### Recognizing Copy Problems

#### Spotting Reachable Object Graphs

Use this method when a statement asks for a copy of objects that refer to each other, and the copy must keep the sharing and the loops of the original. The cue is a reachable object structure that is not a tree. The method copies only what the start node can reach. Nodes that no path from `start` reaches are never discovered, so they never appear in the copy.

#### Keeping The Invariant

The invariant ties the map to the discovery order: one clone per discovered original, none twice. Every wiring step reads from the map and never creates a second clone. A wiring step that reads a node not yet discovered must enter it first.

#### Value Keys As False Friend

A map keyed by label is a false friend of the identity map. It looks like the same table, but two different nodes can carry equal labels. A value key merges those nodes into one clone and silently removes a node from the copy. The key must be the original node itself. In Java, a `Node` class without `equals` and `hashCode` gives that behavior by default, and a class that overrides both by label breaks it.

#### Empty Input And Self-Loops

A `null` start means an empty structure, and the answer is `null`. A node that lists itself as a neighbor is a one-node loop, and the same map rule handles it.

<!-- stage: exercises -->
### Exercises

#### [Build] Clone One Edge (Author exercise)
<!-- id: gt-clone-one-edge -->

**Prerequisites.** The identity map of this lesson.

**Problem.** Two `Node` objects `a` and `b` are joined by one undirected edge, so `a.neighbors` is `[b]` and `b.neighbors` is `[a]`. Given `a`, return a clone of `a`. The clone of `a` has the same `val` and one neighbor, a clone of `b` with the same `val`, whose only neighbor is the clone of `a`. No object of the result is an object of the input.

**Constraints.** The limits are:
- **Nodes** are exactly two, with distinct `int` values in the range 0 to 1.
- **Input** is the node `a`, which is never `null`.
- **Neighbors** of each node are exactly the other node.
- **Mutation** does not occur; the input nodes do not change.

**Example 1.** Input `a` with `val = 0` and `b` with `val = 1`, output a clone of `a` with `val = 0` whose neighbor has `val = 1` and refers back to the clone of `a`.

**Example 2.** Input `a` with `val = 1` and `b` with `val = 0`, output a clone of `a` with `val = 1` whose neighbor has `val = 0` and refers back to the clone of `a`.

**Hint.** What must exist before the clone of `a` can list the clone of `b`?

**Changed decision.** Both clones are created before the copied edge is wired.

#### [Vary] Clone A Cycle (Author exercise)
<!-- id: gt-clone-cycle -->

**Prerequisites.** The previous exercise.

**Problem.** A directed cycle has `k` nodes with values 0 to k-1, where node `i` has exactly one neighbor, node `(i + 1) % k`. Given the node with value `s`, return its clone. In the result, following `neighbors.get(0)` from the clone of `s` exactly `k` times returns to the clone of `s`. The result shares no node with the input.

**Constraints.** The limits are:
- **Length** satisfies `2 <= k <= 100`.
- **Start** satisfies `0 <= s < k`.
- **Neighbors** of each node hold exactly one node.
- **Mutation** does not occur; the input nodes do not change.

**Example 1.** Input `k = 3` and `s = 0`, output a clone cycle whose values along the neighbors are `[0,1,2,0]`.

**Example 2.** Input `k = 4` and `s = 2`, output a clone cycle whose values along the neighbors are `[2,3,0,1,2]`.

**Hint.** When does the method meet the start node a second time, and what does the map hold at that moment?

**Changed decision.** The entry is stored before the neighbors are traversed, so the last node reuses the first clone.

#### [Boundary] Null And Self-Loop (Author exercise)
<!-- id: gt-null-self-loop -->

**Prerequisites.** The two exercises above.

**Problem.** Given `start`, the node of a directed graph, return its clone. If `start` is `null`, return `null`. A node may list itself as a neighbor, and the clone of such a node must list its own clone and never the original. The clone must keep the neighbor order of every reachable original node.

**Constraints.** The limits are:
- **Nodes** reachable from `start` number at most 100, with distinct `int` values.
- **Start** may be `null`.
- **Self-loops** are allowed; a node may appear once in its own `neighbors`.
- **Repeats** do not occur; no node appears twice in one `neighbors` list.
- **Mutation** does not occur; the input nodes do not change.

**Example 1.** Input `start = null`, output `null`.

**Example 2.** Input one node with `val = 0` and neighbors `[itself]`, output a node with `val = 0` whose single neighbor is itself, and which is not the input node.

**Hint.** What does the map hold when the method reads the neighbor list of a node that lists itself?

**Changed decision.** Absence returns `null`, and a reference back to the same node is wired to the clone it already has.

#### [Recognize] Clone Graph (LeetCode 133)
<!-- id: gt-clone-graph -->

**Prerequisites.** The three exercises above.

**Problem.** A directed graph has `n` nodes with distinct values 0 to n-1. The input is the array `adjList` and the start value `s`, and the node objects are built from `adjList`, where node `i` has the neighbors listed in `adjList[i]`. Undirected edges appear in both lists. Return a deep copy of the part of the graph reachable from the node with value `s`. This version differs from the LeetCode problem in two ways. The start value is arbitrary, and nodes that the start cannot reach are not copied.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 100`.
- **Values** are distinct and equal to the index of the node.
- **Lists** hold values in the range 0 to n-1, with no repeats inside one list and no self-loops.
- **Start** satisfies `0 <= s < n`.
- **Mutation** does not occur; the input nodes do not change.

**Example 1.** Input `adjList = [[1,2],[0,2],[0,1,3],[2]]` and `s = 0`, output a clone with neighbor lists `[[1,2],[0,2],[0,1,3],[2]]` for the values 0 to 3.

**Example 2.** Input `adjList = [[1],[0],[3],[2]]` and `s = 2`, output a clone with neighbor lists `[[3],[2]]` for the values 2 and 3 only.

**Hint.** Which nodes does a traversal from the start node ever discover?

**Changed decision.** The start is any node, and the copy contains exactly the reachable nodes.
