<!-- lesson-kind: standard -->
<!-- lesson-id: balanced-tree-concepts -->
## Keep A Search Tree Short

<!-- stage: context -->
### Why Lookups Slow Down Every Week

A monitoring service stores events in a binary search tree keyed by timestamp. Events arrive in time order, so every new key is larger than all earlier keys. In the first week the dashboard answers instantly. After a month a lookup takes a noticeable pause, and after a year the dashboard times out. Nothing in the code changed, and each lookup still compares the key with one node per level.

Every lookup, insert and delete in a search tree costs one step per level. The tree in this service has quietly turned into a long chain, and a chain has as many levels as it has nodes. This lesson asks what shape keeps the number of levels small, and what a program can do to keep that shape.

<!-- stage: naive -->
### Inserting Keys In Arrival Order

The direct plan uses the plain insert from the lesson on one path. Each new key walks down from the root and attaches as a new leaf, and nothing else ever moves.

```java
final class PlainTree {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static TreeNode insert(TreeNode node, int key) {
        if (node == null) return new TreeNode(key);          // the empty slot receives the new leaf
        if (key < node.val) node.left = insert(node.left, key);
        else node.right = insert(node.right, key);           // larger keys go right
        return node;
    }

    static int height(TreeNode node) {
        if (node == null) return 0;                          // an empty tree has no level
        return 1 + Math.max(height(node.left), height(node.right));   // levels below plus this one
    }
}
```

Inserting the keys `4, 2, 6, 1, 3, 5, 7` gives a tree with 3 levels. Inserting `1, 2, 3, 4, 5, 6, 7` gives a tree with 7 levels, where every node has only a right child.

<!-- stage: bottleneck -->
### Measuring The Slowdown

```predict
A hundred thousand keys arrive in increasing order. How many levels does the plain tree have, and about how many comparisons do all the inserts need together?

The tree has one hundred thousand levels, because each key becomes the right child of the previous one. The inserts need about 1 + 2 + ... + 100000 comparisons, which is about five billion, so the cost is O(n^2) for n keys.
```

The shape depends on the arrival order, and the program does not control that order. A sorted, reversed or nearly sorted stream is common in real data, such as timestamps and counters. The cost of one operation is O(h) for height `h`, and `h` ranges from about log n for a compact tree to n for a chain.

The tree needs a repair step that keeps `h` near log n whatever order the keys arrive in, and the repair must not break the order of the keys.

<!-- stage: insight -->
### Rearrange Nodes Without Changing The Order

#### Keeping Both Sides About Equal

A tree is **height-balanced** when, at every node, the heights of the left and right subtrees differ by at most 1. A height-balanced tree with `n` nodes has height O(log n). The reason is a count of the smallest tree for each height: a tree of height `h` needs at least a smallest tree of height `h - 1` on one side and a smallest tree of height `h - 2` on the other. That count grows like the Fibonacci numbers, so a tree of height `h` has exponentially many nodes, and a tree of `n` nodes has only logarithmic height.

Balanced does not mean complete or symmetric. A node may have a left subtree of height 3 and a right subtree of height 2. The rule only limits the difference.

#### Rotating One Link At A Time

A **rotation** lifts one node above its parent and moves one subtree to keep the order. In a right rotation at a node `z` with a left child `y`, the node `y` becomes the top, the node `z` becomes the right child of `y`, and the old right subtree of `y` becomes the left subtree of `z`. That subtree held keys larger than `y` and smaller than `z`, so it fits the new slot exactly. The sorted order of all keys stays the same, and only the heights change. A left rotation is the mirror.

A chain of three nodes that leans left, such as 3, 2, 1, is cured by one right rotation at the top node. A chain that leans right is cured by one left rotation. A zigzag needs two rotations.

#### Letting The Library Do The Work

A **self-balancing** tree applies the rotations after each insert and delete, along the path that was just changed, so the height rule always holds. Java's `TreeMap` and `TreeSet` are self-balancing trees with O(log n) operations in the worst case. They also give the neighbors from the lesson on the next key: `higherKey` is the successor and `lowerKey` is the predecessor. Writing and debugging a self-balancing tree by hand is rarely worth the effort for an interview or a job.

<!-- names: height-balanced, rotation, self-balancing -->

<!-- stage: variables -->
### The Quantities Behind Balance

- **height** is the number of levels on the longest path from a node down, with 0 for an empty subtree.
- **difference** is the height of the left subtree minus the height of the right subtree, and the rule allows -1, 0 and 1.
- **z** is the node where a rotation happens, and **y** is the child that moves above it.
- **inorder** is the list of keys in sorted order, which every rotation leaves unchanged.

<!-- stage: trace -->
### Comparing Two Shapes And One Rotation

#### Searching For The Largest Key In Two Shapes

The cells hold the keys 1 to 7 in sorted order. One tree is the chain built from the arrival order 1 to 7, and the other tree is the compact shape built from the order 4, 2, 6, 1, 3, 5, 7. The pointers `chain` and `compact` mark the key each tree compares at each step, and -1 means that tree has finished.

```trace
{"cells":[1,2,3,4,5,6,7],"pointers":["chain","compact"],"steps":[{"at":{"chain":0,"compact":3},"vars":{"step":1},"note":"The chain compares 7 with 1 and goes right. The compact tree compares 7 with 4."},{"at":{"chain":1,"compact":5},"vars":{"step":2},"note":"The chain compares 7 with 2 and goes right. The compact tree compares 7 with 6."},{"at":{"chain":2,"compact":6},"vars":{"step":3},"note":"The chain compares 7 with 3 and goes right. The compact tree compares 7 with 7 and stops with a match."},{"at":{"chain":3,"compact":-1},"vars":{"step":4},"note":"The chain compares 7 with 4 and goes right. The compact tree is finished."},{"at":{"chain":4,"compact":-1},"vars":{"step":5},"note":"The chain compares 7 with 5 and goes right. The compact tree is finished."},{"at":{"chain":5,"compact":-1},"vars":{"step":6},"note":"The chain compares 7 with 6 and goes right. The compact tree is finished."},{"at":{"chain":6,"compact":-1},"vars":{"step":7},"note":"The chain compares 7 with 7 and stops with a match. The compact tree is finished."}]}
```

The compact tree finds 7 in 3 comparisons, and the chain needs 7.

#### Rotating A Left-Leaning Chain

The cells hold the keys 1, 2 and 3 in sorted order. The tree starts as the chain with 3 on top, 2 below it and 1 at the bottom. The pointer `top` marks the key at the top of the tree.

```trace
{"cells":[1,2,3],"pointers":["top"],"steps":[{"at":{"top":2},"vars":{"height":3},"note":"Start: the tree is the left chain 3, 2, 1. The top key is 3 and the height is 3."},{"at":{"top":2},"vars":{"height":3},"note":"The method takes y = 2, the left child of 3. The right subtree of 2 is empty, so it becomes the new left subtree of 3."},{"at":{"top":1},"vars":{"height":2},"note":"The method makes 3 the right child of 2 and returns 2 as the new top. The height is 2, and the sorted order is still 1, 2, 3."}]}
```

The sorted order of the cells never changes. Only the top key and the height change.

<!-- stage: code -->
### Height And Rotation In Code

```java
final class Rotations {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static int height(TreeNode node) {
        return node == null ? 0 : 1 + Math.max(height(node.left), height(node.right));
    }

    static TreeNode rotateRight(TreeNode z) {
        TreeNode y = z.left;                 // y rises above z
        z.left = y.right;                    // keys between y and z move under z
        y.right = z;                         // z drops to the right of y
        return y;                            // y is the new top of this subtree
    }

    static TreeNode rotateLeft(TreeNode z) {
        TreeNode y = z.right;                // the mirror image of rotateRight
        z.right = y.left;
        y.left = z;
        return y;
    }
}
```

The caller must store the returned node in the slot that held `z`, because the top of the subtree changed. A library map hides all of this.

```java
final class LibraryMap {
    static Integer successorOf(TreeMap<Integer, String> map, int key) {
        return map.higherKey(key);            // the smallest key above the given key, or null
    }

    static Integer predecessorOf(TreeMap<Integer, String> map, int key) {
        return map.lowerKey(key);             // the largest key below the given key, or null
    }
}
```

- **Time** of a rotation is O(1), because it rewrites three references.
- **Space** is O(1), because no node is created.

<!-- stage: applicability -->
### Choosing A Tree Or A Library

#### Recognizing The Cue

Think about balance whenever keys may arrive in sorted or nearly sorted order, or when the problem needs O(log n) in the worst case, not on average. A phrase such as "operations on a stream of sorted values" points to it. A problem with random keys or a fixed small input does not need it.

#### Stating The Invariant

The invariant of a height-balanced tree is that every node has subtree heights differing by at most 1, and every rotation preserves the sorted order of the keys. Repairs happen along the path of the last change, since only those nodes can break the rule.

#### Avoiding The False Friend

The false friend is the word "balanced" read as "perfectly symmetric". A balanced tree can have different shapes on the two sides and still keep logarithmic height. A second trap is the average case. A plain search tree is fast on random keys and slow on sorted keys, and a statement about the average says nothing about the worst input. Prefer `TreeMap` or `TreeSet` when the worst case matters, and write a hand-built tree only when the problem asks for the structure itself.

<!-- stage: exercises -->
### Exercises

#### [Build] Compare Search Heights (Author exercise)
<!-- id: tb-bal-heights -->

**Prerequisites.** The height of a tree from this lesson.

**Problem.** Given an array of distinct keys, insert the keys one at a time into an initially empty plain binary search tree in array order, with no rebalancing. Return the height of the tree, which counts the nodes on the longest root-to-leaf path. An empty array gives height 0.

**Constraints.** The limits are:
- **Length** is between 0 and 1000.
- **Values** are distinct `int` values.
- **Answer** is an `int` between 0 and the length.
- **Mutation** does not occur to the input array.

**Example 1.** Input `[1, 2, 3]`, output 3, because each key becomes the right child of the previous key.

**Example 2.** Input `[2, 1, 3]`, output 2.

**Hint.** Where does each new key attach? How does the height of a node relate to the heights of its children?

**Changed decision.** The arrival order, and not the key set, decides the height.

#### [Vary] Identify One Rotation (Author exercise)
<!-- id: tb-bal-rotation-type -->

**Prerequisites.** The exercise above.

**Problem.** Three distinct keys are inserted in the given order into an empty plain binary search tree. Return `"RIGHT_ROTATION"` if the tree is a chain that leans left, `"LEFT_ROTATION"` if it is a chain that leans right, `"NONE"` if the tree has height 2, and `"DOUBLE"` if the tree is a chain with a zigzag.

**Constraints.** The limits are:
- **Input** is exactly three distinct `int` keys.
- **Values** may be negative.
- **Answer** is one of the four strings.
- **Mutation** does not occur.

**Example 1.** Input `[3, 2, 1]`, output `"RIGHT_ROTATION"`.

**Example 2.** Input `[1, 3, 2]`, output `"DOUBLE"`.

**Hint.** Which keys become the root and its children for each insertion order? Which shapes have height 3?

**Changed decision.** The method names the repair for a shape and does not measure a height.

#### [Boundary] Preserve Inorder Through Rotation (Author exercise)
<!-- id: tb-bal-inorder -->

**Prerequisites.** The two exercises above.

**Problem.** A search tree and the key of one of its nodes are supplied, and that node has a left child. Rotate that node to the right as described in this lesson, and return the keys of the whole tree in sorted order after the rotation. The result must equal the sorted order before the rotation.

**Constraints.** The limits are:
- **Nodes** number between 2 and 10^4, and all keys are distinct.
- **Key** is the key of a node that has a left child.
- **Answer** is a list in increasing order with one entry for each node.
- **Mutation** rewrites three child references.

**Example 1.** Input root 3 with a left child 2 that has a left child 1, and key 3, output `[1, 2, 3]`.

**Example 2.** Input root 5 with children 3 and 8, where 3 has children 2 and 4, and key 5, output `[2, 3, 4, 5, 8]`.

**Hint.** Which subtree changes its parent during the rotation? Does any key change its place in sorted order?

**Changed decision.** The method changes the shape and must leave the sorted order untouched.

#### [Recognize] Explain Library Choice (Author exercise)
<!-- id: tb-bal-library-choice -->

**Prerequisites.** All three exercises above.

**Problem.** Keys arrive in a given order, and the program may store them in a hand-built plain search tree or in a library self-balancing map. Return `true` if the hand-built tree, built by inserting the keys in arrival order, would have a height greater than twice the smallest height a tree of that many nodes can have, and so the library map is the safer choice. Otherwise return `false`. The smallest height of a tree with `n` nodes is the number of bits of `n`.

**Constraints.** The limits are:
- **Length** is between 1 and 1000.
- **Values** are distinct `int` values.
- **Answer** is a `boolean`.
- **Mutation** does not occur.

**Example 1.** Input `[1, 2, 3, 4, 5, 6, 7]`, output `true`, because the height is 7, which is greater than 2 * 3.

**Example 2.** Input `[4, 2, 6, 1, 3, 5, 7]`, output `false`, because the height is 3.

**Hint.** How many levels does the plain tree have for this order? How many bits does 7 have?

**Changed decision.** The method decides which structure to use from the shape that an input order produces.
