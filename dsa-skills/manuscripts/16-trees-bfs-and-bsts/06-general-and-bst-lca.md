<!-- lesson-kind: standard -->
<!-- lesson-id: general-and-bst-lca -->
## General And BST LCA

<!-- stage: context -->
### Two Campers And A Trail Network

A mountain park has one ranger station, and from it the trails fork again and again, never rejoining. Every junction has at most two trails leading onward. Two campers phone in from different spots on the network and ask for the same thing: to be told the last junction that both of their routes from the station have in common, so they can meet there and walk down together.

The coordinator looks at a map where every junction has a name. On some maps the junction numbers carry no meaning at all. On others, the park has numbered the junctions so that smaller numbers always lie to the left of a junction and larger numbers to the right. The coordinator suspects that the second kind of map should make the question much easier, and that the first kind still has a clean method.

<!-- stage: naive -->
### Ask Every Junction Whether It Holds Both

The direct method visits every junction in turn and asks a yes or no question: does everything beyond this junction contain both campers? Each question is a fresh search of the junction's whole branch. The coordinator keeps the deepest junction that answered yes.

```java
static Node deepestHoldingBoth(Node root, Node p, Node q) {
    if (root == null || !holds(root, p) || !holds(root, q)) return null;
    Node deeper = deepestHoldingBoth(root.left, p, q);
    if (deeper != null) return deeper;
    deeper = deepestHoldingBoth(root.right, p, q);
    return deeper != null ? deeper : root;
}

static boolean holds(Node junction, Node camper) {
    if (junction == null) return false;
    return junction == camper || holds(junction.left, camper) || holds(junction.right, camper);
}
```

The answer is by definition the deepest junction whose branch holds both campers, and the method checks exactly that, so it is correct on any map.

<!-- stage: bottleneck -->
### Every Branch Is Searched Over And Over

The question at a junction searches its whole branch, and the next junction below repeats most of that search. On a trail network shaped like one long line of n junctions with both campers at the far end, each junction searches everything beyond it twice, and the total is about n^2, so the time is O(n^2). With thirty thousand junctions that is nearly two billion visits for a single phone call.

The repetition is avoidable because the information needed at a junction is exactly what its two branches would have computed anyway. If each branch could simply report whether it saw a camper, the junction would learn everything with no new search. A single walk that collects those reports on the way back up the trail should find the answer with O(n) time and O(h) memory. On a map with numbered junctions the walk could be even shorter, since a number can say which way to go.

<!-- stage: insight -->
### Report Upward, Or Steer By Number

On a map with no ordering, let every junction return a **target report** to the junction above: the camper it contains, or nothing. A junction that is itself a camper returns itself at once, without looking further, because if the other camper lies below it, this junction is already the answer, and if not, the report of this junction is still correct. Otherwise it asks both branches and combines their reports. When both branches return something, one camper is on each side, and this junction is the **meeting junction**. When only one branch returns something, that report is passed up unchanged, which carries either a single camper or an already found meeting junction.

The invariant is that a call returns nothing exactly when its branch holds no camper, and returns the meeting junction exactly when its branch holds both, so the report that reaches the root is the answer.

On a numbered map, nothing needs to come back up. At a junction whose number is above both campers' numbers, both are on the left, so move left. When it is below both, move right. As soon as the junction number lies between them, or equals one of them, the routes separate there, and this **split point** is the answer.

<!-- names: target report, meeting junction, split point -->

The numbered shortcut leans on the ordering promise and fails on a map that never made one.

<!-- stage: variables -->
### Camper Targets And Branch Reports

The values `p` and `q` identify the campers and do not change. In the unordered walk, `left` and `right` are the reports returned from the two branches, each either a node or `null`, and the call returns the junction itself when both are non-null, otherwise whichever one is non-null, otherwise `null`. Comparing junctions to campers must use the node identity `==`, or compare `int` values, but never `==` between two boxed `Integer` objects. In the numbered walk the single variable `node` moves down one link per comparison, and the numbers `p` and `q` are compared as plain `int` values.

<!-- stage: trace -->
### Reports, An Ancestor Camper And A Split

The first trace uses the map 1, 2, 3, 4, 5, 6, 7, null, null, 8, 9 with campers at 8 and 7. The marker `node` rests on each junction at the moment it returns its report, in the order the returns happen. The report climbs from 8 through 5 and 2, and the report 7 climbs through 3, so the junction 1 receives two reports and becomes the meeting junction.

```trace
{"cells":["1","2","3","4","5","6","7","null","null","8","9"],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"report":"none"},"note":"Neither branch of the junction 4 holds a camper, so it reports nothing."},{"at":{"node":9},"vars":{"report":8},"note":"The junction 8 is a camper, so it reports itself at once without looking further."},{"at":{"node":10},"vars":{"report":"none"},"note":"Neither branch of the junction 9 holds a camper, so it reports nothing."},{"at":{"node":4},"vars":{"report":8},"note":"Only one branch of the junction 5 reported, so it passes the report 8 upward unchanged."},{"at":{"node":1},"vars":{"report":8},"note":"Only one branch of the junction 2 reported, so it passes the report 8 upward unchanged."},{"at":{"node":5},"vars":{"report":"none"},"note":"Neither branch of the junction 6 holds a camper, so it reports nothing."},{"at":{"node":6},"vars":{"report":7},"note":"The junction 7 is a camper, so it reports itself at once without looking further."},{"at":{"node":2},"vars":{"report":7},"note":"Only one branch of the junction 3 reported, so it passes the report 7 upward unchanged."},{"at":{"node":0},"vars":{"report":1},"note":"The branches of the junction 1 reported 8 and 7, one camper on each side, so 1 is the meeting junction and reports itself."}]}
```

The second trace keeps the same map but moves the campers to 2 and 9. The junction 2 is itself a camper, so it reports itself immediately and its branch, which holds the other camper at 9, is never visited. The right side of the station produces no report, and the station passes up the single report from the left, which is the correct answer 2.

```trace
{"cells":["1","2","3","4","5","6","7","null","null","8","9"],"pointers":["node"],"steps":[{"at":{"node":1},"vars":{"report":2},"note":"The junction 2 is a camper, so it reports itself at once without looking further."},{"at":{"node":5},"vars":{"report":"none"},"note":"Neither branch of the junction 6 holds a camper, so it reports nothing."},{"at":{"node":6},"vars":{"report":"none"},"note":"Neither branch of the junction 7 holds a camper, so it reports nothing."},{"at":{"node":2},"vars":{"report":"none"},"note":"Neither branch of the junction 3 holds a camper, so it reports nothing."},{"at":{"node":0},"vars":{"report":2},"note":"Only one branch of the junction 1 reported, so it passes the report 2 upward unchanged."}]}
```

The third trace works on a numbered map, 20, 10, 30, 5, 15, 25, 35, null, null, 12, 18, with campers at 12 and 18. At 20 both numbers are smaller, so the route goes left. At 10 both are larger, so it goes right. At 15 the number lies between them, so the walk stops with 15.

```trace
{"cells":["20","10","30","5","15","25","35","null","null","12","18"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"p":12,"q":18},"note":"Both 12 and 18 are smaller than the junction 20, so the walk goes left."},{"at":{"node":1},"vars":{"p":12,"q":18},"note":"Both 12 and 18 are larger than the junction 10, so the walk goes right."},{"at":{"node":4},"vars":{"p":12,"q":18},"note":"The junction 15 is not above both numbers nor below both, so the routes separate here and 15 is the answer."}]}
```

<!-- stage: code -->
### Two Walks For Two Kinds Of Map

```java
final class MeetingPoints {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node meeting(Node node, Node p, Node q) {
        if (node == null || node == p || node == q) return node;
        Node left = meeting(node.left, p, q);
        Node right = meeting(node.right, p, q);
        if (left != null && right != null) return node;
        return left != null ? left : right;
    }

    static Node splitPoint(Node root, int p, int q) {
        Node node = root;
        while (node != null) {
            if (p < node.val && q < node.val) node = node.left;
            else if (p > node.val && q > node.val) node = node.right;
            else return node;
        }
        return null;
    }
}
```

The unordered walk visits each junction once, so it takes O(n) time with O(h) recursion. The numbered walk follows one path, so it takes O(h) time and O(1) space.

<!-- stage: applicability -->
### When Two Routes Must Meet

Use the report walk for any question about the lowest shared point of two items in a hierarchy: the nearest common manager of two employees, the closest shared folder of two files, or the earliest merge point of two version branches. The invariant is that a call returns nothing for a branch without targets and returns the meeting junction for a branch with both. Use the split-point walk when the hierarchy is a search tree and the question concerns two keys.

The first false friend is the numbered shortcut applied to an unordered tree. It compares numbers that carry no meaning about position, so it can walk away from both campers and return a junction that does not contain them. A second false friend is the depth-first path comparison that records both routes and compares them from the top, which is correct but copies routes, and costs more memory than the report walk. A third is the case where one camper stands above the other, which the early return at a camper handles correctly only because both are guaranteed to exist.

In Java, compare nodes with `==` and numbers as `int`. Two `Integer` objects holding the same large value are different objects, so `==` between them can be false even though `equals` is true.

<!-- stage: exercises -->
### Exercises

#### [Build] General-Tree Ancestor Return (Author exercise)
<!-- id: tb-meeting-junction -->

**Prerequisites.** The tree DFS chapter's return values and the postorder moment.

**Problem.** Trails form a binary tree with distinct labels, listed in level order with `null` at each missing child. Two labels `p` and `q` are present, and neither one is an ancestor of the other. Return `[label, depth]` for the lowest junction above both, where depth counts edges down from the root.

**Constraints.** 3 <= values.length <= 3000, labels are distinct integers between 0 and 100000, and the two labels sit in different branches of some junction.

**Example 1.** Input `values = [1, 2, 3, 4, 5, 6, 7, null, null, 8, 9]`, `p = 8`, `q = 7`, output `[1, 0]`.

**Example 2.** Input `values = [1, 2, 3, 4, 5, 6, 7, null, null, 8, 9]`, `p = 8`, `q = 9`, output `[5, 2]`.

**Hint.** What must the two branches of the answer's junction report, and what does every junction above it report?

**Changed decision.** A junction is the answer when both of its branches return a camper, and the depth is carried down so it can be read at that moment.

#### [Vary] Lowest Common Ancestor of a Binary Tree (LeetCode 236)
<!-- id: tb-lca-binary-tree -->

**Prerequisites.** The General-Tree Ancestor Return rung.

**Problem.** For a binary tree with distinct labels in level order and two labels `p` and `q` that are both present, return the label of their lowest common ancestor. A node counts as an ancestor of itself, so when one label lies below the other the upper one is the answer.

**Constraints.** 2 <= values.length <= 10000, labels are distinct integers between -100000 and 100000, and `p` differs from `q`.

**Example 1.** Input `values = [1, 2, 3, 4, 5, 6, 7, null, null, 8, 9]`, `p = 4`, `q = 9`, output `2`.

**Example 2.** Input `values = [1, 2, 3, 4, 5, 6, 7, null, null, 8, 9]`, `p = 2`, `q = 9`, output `2`.

**Hint.** What should a call return when it meets one of the two labels, and does it matter whether the other label lies beneath?

**Changed decision.** A junction that is itself one of the labels returns at once, which lets a label stand for the answer when the other is below it.

#### [Boundary] One Target Is Ancestor (Author exercise)
<!-- id: tb-target-is-ancestor -->

**Prerequisites.** The Binary Tree LCA rung and its early return.

**Problem.** For a binary tree with distinct labels in level order and two present labels `p` and `q`, which may be equal, return `[lca, distance]`, where `distance` is the number of edges on the route from `p` to `q` through their lowest common ancestor. When one label is above the other, the lca is the upper one, and when the labels are equal, the distance is zero.

**Constraints.** 1 <= values.length <= 3000, labels are distinct integers between 0 and 100000, and `p` and `q` are labels in the tree and may be the same label.

**Example 1.** Input `values = [1, 2, 3, 4, 5, 6, 7, null, null, 8, 9]`, `p = 2`, `q = 9`, output `[2, 2]`.

**Example 2.** Input `values = [1, 2, 3, 4, 5, 6, 7, null, null, 8, 9]`, `p = 5`, `q = 5`, output `[5, 0]`.

**Hint.** If the depths of the three nodes are known, how many edges lie between each label and the lowest common ancestor?

**Changed decision.** The depth is recorded for the labels and the answer junction, and the distance is computed from the three depths with no second search.

#### [Recognize] Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)
<!-- id: tb-lca-bst -->

**Prerequisites.** The One Target Is Ancestor rung and the ordering promise of a search tree.

**Problem.** Given a search tree of distinct keys in level order and two keys `p` and `q` that are in it, return their lowest common ancestor, where a key counts as its own ancestor. Use the ordering to decide the direction at each node and avoid visiting both sides.

**Constraints.** 2 <= values.length <= 10000, keys are distinct integers between 0 and 100000, and `p` differs from `q`.

**Example 1.** Input `values = [20, 10, 30, 5, 15, 25, 35, null, null, 12, 18]`, `p = 12`, `q = 18`, output `15`.

**Example 2.** Input `values = [20, 10, 30, 5, 15, 25, 35, null, null, 12, 18]`, `p = 10`, `q = 12`, output `10`.

**Hint.** When both keys are smaller than the current key, which subtree holds both of them?

**Changed decision.** No reports travel upward; the walk goes down one side while both keys lie on that side and stops at the first node that separates them or equals one.
