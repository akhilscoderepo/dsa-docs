<!-- lesson-kind: standard -->
<!-- lesson-id: successor-and-predecessor -->
## Successor And Predecessor

<!-- stage: context -->
### The Bell Ringer On The Frame

A small chapel keeps its bells on a wooden frame that branches like a tree. Each bell has its own pitch. Lower pitches always hang somewhere on the left side below a bell, and higher pitches somewhere on the right side. The ringer plays a tune that climbs the whole scale: after striking one bell he must strike the bell with the next higher pitch, and before long he is standing at some bell with no memory of the others.

On a good day he can walk the frame in his head, but the frame has no ropes leading back up, so once he steps down a branch he cannot step back. He needs a rule that tells him which bell comes next from where he stands, and a similar rule for the bell just below, for the downward run at the end of the tune.

<!-- stage: naive -->
### Write Out The Whole Scale First

The plain method writes the pitches of every bell in order into a list, finds the one he just rang in that list, and reads the neighbour. Nothing about the frame's shape needs to be understood, because a sorted list answers both questions.

```java
static Integer nextBySorting(Node root, int pitch) {
    List<Integer> scale = new ArrayList<>();
    collect(root, scale);
    for (int i = 0; i < scale.size(); i++) {
        if (scale.get(i) > pitch) return scale.get(i);
    }
    return null;
}

static void collect(Node bell, List<Integer> out) {
    if (bell == null) return;
    collect(bell.left, out);
    out.add(bell.val);
    collect(bell.right, out);
}
```

The list is complete and in order, so the first pitch above the one just rung is the right answer, and null is returned when the ringer is on the highest bell.

<!-- stage: bottleneck -->
### The Whole Frame For One Neighbour

Writing the scale costs O(n) time and O(n) memory, and it is paid again for every question. A tune that asks for the next bell a hundred thousand times on a frame of a hundred thousand bells spends ten billion steps, nearly all of them on bells nowhere near the answer. The neighbour in pitch order is also usually physically close, either just below the current bell or a short way up the path from the root.

The frame has already done the sorting. Everything smaller than a bell is on its left and everything larger is on its right, so the next pitch above must come from a place that can be reached by following a single path, never by touching unrelated branches. If the path from the root to the bell is at most h long, a question should cost O(h) with O(1) extra memory, even though the list-making method costs O(n) every time.

<!-- stage: insight -->
### The Next Bell Is On One Path

Look first at what is below the current bell. If its right side is not empty, the next higher pitch is the smallest pitch on that side, which is reached from the right child by following left links until none remain. That is the **inside case**.

If the right side is empty, nothing below is higher, so the answer must be above: it is the nearest ancestor whose left side contains the current bell, that is, the last bell where the path from the root turned left. A bell where the path turned right is smaller than the target and cannot be the answer. This is the **ancestor case**, and it explains why the parent is not always the successor: a bell that is a right child with nothing below it has a parent that is lower, and the answer lies higher up.

Both cases come out of one downward walk from the root that never needs parent links. Keep a candidate, the smallest pitch seen so far that is higher than the target. At each bell above the target, save it as the candidate and go left, and at any other bell go right. When the walk ends, the candidate is the answer, or none.

The invariant is that the candidate is always the smallest pitch above the target among the bells already visited, and the answer lies in the subtree still ahead or is the candidate itself.

<!-- names: inside case, ancestor case, mirror rule -->

For the next lower pitch, apply the **mirror rule**: swap every left and right, so the inside case uses the largest pitch of the left side and the walk saves a bell whenever it goes right.

<!-- stage: variables -->
### Candidate, Current Bell And Target

The variable `target` is the pitch just rung and does not change. The variable `node` is the current bell and moves down one link per step until it becomes null. The variable `best` is an `Integer`, not an `int`, because it must be able to hold the answer null for "no bell above". It is overwritten each time the walk meets a bell higher than the target, and it is never overwritten with a larger value, since each such bell lies in the subtree of the previous one. The helper `leftmost(node)` follows left links to find the smallest pitch of a subtree for the inside case.

<!-- stage: trace -->
### Next Pitch After Seven And After Three

Both traces use the frame 8, 3, 10, 1, 6, null, 14, null, null, 4, 7, 13, written in level order. The first asks for the pitch after 7. The marker `node` rests on the bell being compared, and `best` shows the saved candidate. At the bell 8 the walk saves 8 and goes left, and then it goes right at 3 and 6 because those pitches are not higher than 7, so nothing lower replaces the candidate. The walk ends below 7 with 8 saved, which is the ancestor case.

```trace
{"cells":["8","3","10","1","6","null","14","null","null","4","7","13"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"target":7,"best":8},"note":"The bell 8 is higher than 7, so it is saved as the candidate and the walk goes left."},{"at":{"node":1},"vars":{"target":7,"best":8},"note":"The bell 3 is not higher than 7, so the candidate stays and the walk goes right."},{"at":{"node":4},"vars":{"target":7,"best":8},"note":"The bell 6 is not higher than 7, so the candidate stays and the walk goes right."},{"at":{"node":10},"vars":{"target":7,"best":8},"note":"The bell 7 is not higher than 7, so the candidate stays and the walk goes right. There is nothing on that side, so the walk ends with 8 as the answer."}]}
```

The second trace asks for the pitch after 3, a bell that does have a right side. The bell 8 is saved and left, then 3 itself is not higher than the target so the walk turns right to 6, saves it and turns left to 4, saves it, and turns left into nothing. The candidate has crept down the right side of 3 to its smallest pitch, which is the inside case reached without any special code.

```trace
{"cells":["8","3","10","1","6","null","14","null","null","4","7","13"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"target":3,"best":8},"note":"The bell 8 is higher than 3, so it is saved as the candidate and the walk goes left."},{"at":{"node":1},"vars":{"target":3,"best":8},"note":"The bell 3 is not higher than 3, so the candidate stays and the walk goes right."},{"at":{"node":4},"vars":{"target":3,"best":6},"note":"The bell 6 is higher than 3, so it is saved as the candidate and the walk goes left."},{"at":{"node":9},"vars":{"target":3,"best":4},"note":"The bell 4 is higher than 3, so it is saved as the candidate and the walk goes left. There is nothing on that side, so the walk ends with 4 as the answer."}]}
```

<!-- stage: code -->
### One Walk For Both Neighbours

```java
final class NextInOrder {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Integer successor(Node root, int target) {
        Integer best = null;
        Node node = root;
        while (node != null) {
            if (node.val > target) { best = node.val; node = node.left; }
            else node = node.right;
        }
        return best;
    }

    static Integer predecessor(Node root, int target) {
        Integer best = null;
        Node node = root;
        while (node != null) {
            if (node.val < target) { best = node.val; node = node.right; }
            else node = node.left;
        }
        return best;
    }

    static Node leftmost(Node node) {
        while (node.left != null) node = node.left;
        return node;
    }
}
```

Each loop follows one path and does constant work per step, so the time is O(h) and the extra space is O(1). The height h is n for a chain and about log n for a balanced tree.

<!-- stage: applicability -->
### When The Next Key Is Asked For

Use the one-path walk when a sorted structure must report the key just above or just below a given one: the next free appointment time, the nearest higher price tier, or the next entry in a sorted index when scanning one step at a time. The invariant is that the saved candidate is the smallest key above the target among the nodes already passed, so the walk never needs to look at a branch it has dropped.

The first false friend is the parent. The parent is the successor only when the node is a left child with no right side, and when it is a right child the answer is higher. A second false friend is the inorder list, correct but O(n) per question, which pays for everything when one path would do. A third is the plain ceiling query that treats equal keys as acceptable, because a successor must be strictly higher than the target.

In Java, return an `Integer` so that "no neighbour" can be null, and never unbox that result into an `int` before testing it, since that throws a `NullPointerException` on the last key of the tree.

<!-- stage: exercises -->
### Exercises

#### [Build] Minimum Of Right Subtree (Author exercise)
<!-- id: tb-right-subtree-minimum -->

**Prerequisites.** The BST invariant lesson and the search path.

**Problem.** The bell frame is a binary search tree with distinct keys, given in level order with `null` for absent children. For a given key that is present and has a non-empty right side, return the smallest key on that right side.

**Constraints.** 2 <= values.length <= 2000, the keys are distinct integers between 1 and 100000, and the given key always has a right child.

**Example 1.** Input `values = [8, 3, 10, 1, 6, null, 14, null, null, 4, 7, 13]`, `key = 3`, output `4`.

**Example 2.** Input `values = [8, 3, 10, 1, 6, null, 14, null, null, 4, 7, 13]`, `key = 8`, output `10`.

**Hint.** After stepping to the right child once, which direction leads to smaller keys, and when do you stop?

**Changed decision.** Exactly one right step is taken, after which only left links are followed until the next left link is null.

#### [Vary] Successor Without Parent Links (Author exercise)
<!-- id: tb-successor-no-parents -->

**Prerequisites.** The Minimum Of Right Subtree rung and the candidate idea.

**Problem.** Given a binary search tree with distinct keys in level order and an integer `target` that may or may not be in the tree, return the smallest key strictly greater than `target`, or `null` if there is none. Nodes carry no link to their parent.

**Constraints.** 0 <= values.length <= 5000, the keys are distinct integers between -100000 and 100000, and the target is an integer in the same range.

**Example 1.** Input `values = [5, 3, 6, 2, 4]`, `target = 4`, output `5`.

**Example 2.** Input `values = [5, 3, 6, 2, 4]`, `target = 6`, output `null`.

**Hint.** When the walk goes left from a node, what is the one thing worth remembering about that node?

**Changed decision.** No search for the target node is needed; the candidate is saved at each node that is higher than the target, and the walk continues left from there.

#### [Boundary] Maximum And Minimum Keys (Author exercise)
<!-- id: tb-extreme-keys -->

**Prerequisites.** The Successor Without Parent Links rung and its mirror.

**Problem.** For a binary search tree with distinct keys in level order and a key that is present, return `[predecessor, successor]`, the next lower and the next higher key, writing `null` for a side that has none. The largest key has no successor and the smallest has no predecessor, and a lone node has neither.

**Constraints.** 1 <= values.length <= 3000, keys are distinct integers between -100000 and 100000, and the key is present.

**Example 1.** Input `values = [7]`, `key = 7`, output `[null, null]`.

**Example 2.** Input `values = [2, 1, 3]`, `key = 3`, output `[2, null]`.

**Hint.** If the candidate is only set when a bell is on the correct side of the key, what is left in it at the extremes?

**Changed decision.** Both neighbours start as null and are never defaulted to a sentinel number, so the extremes report null instead of an out-of-range key.

#### [Recognize] Inorder Successor in BST (LeetCode 285)
<!-- id: tb-inorder-successor -->

**Prerequisites.** The Maximum And Minimum Keys rung and both cases of the successor.

**Problem.** Given a binary search tree with distinct keys in level order and the key `p` of a node known to be in the tree, return the key of its successor in sorted order, or `null` if `p` is the largest key. A node with a right side answers from inside it, and a node without one answers from an ancestor.

**Constraints.** 1 <= values.length <= 10000, the keys are distinct integers between 0 and 100000, and `p` is a key in the tree.

**Example 1.** Input `values = [20, 9, 25, 5, 12, null, null, null, null, 11, 14]`, `p = 12`, output `14`.

**Example 2.** Input `values = [20, 9, 25, 5, 12, null, null, null, null, 11, 14]`, `p = 14`, output `20`.

**Hint.** In the second example, which of the ancestors 12, 9 and 20 lies above 14 in sorted order, and which is the nearest?

**Changed decision.** The answer comes from the minimum of the right side when there is one, and otherwise from the last ancestor at which the route to the node turned left.
