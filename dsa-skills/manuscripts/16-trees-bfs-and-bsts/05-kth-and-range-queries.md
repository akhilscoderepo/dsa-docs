<!-- lesson-kind: standard -->
<!-- lesson-id: kth-and-range-queries -->
## Answer Rank And Range Questions

<!-- stage: context -->
### Why The Leaderboard Lags

A racing game keeps one million lap times in a binary search tree. The leaderboard shows the third fastest time, and a side panel shows the total of all times between 50 and 80 seconds. The first version builds a full list of every time before it answers either question. The panel takes a full second to refresh, although the third fastest time sits near the left end of the tree and most times fall outside the 50 to 80 window.

Both questions use the sorted order of the keys. One asks for a position in that order. The other asks for the keys in an interval. This lesson asks how a program reads only the part of the tree that the question needs.

<!-- stage: naive -->
### Building The Full Sorted List

The direct plan copies every key into a list in sorted order. The third fastest time is the entry at index 2, and the total sums the entries that fall in the window.

```java
final class QueriesByList {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static void fill(TreeNode node, List<Integer> keys) {
        if (node == null) return;
        fill(node.left, keys);            // everything smaller comes first
        keys.add(node.val);
        fill(node.right, keys);           // everything larger comes last
    }

    static int kth(TreeNode root, int k) {
        List<Integer> keys = new ArrayList<>();
        fill(root, keys);
        return keys.get(k - 1);           // positions count from 1, list indexes from 0
    }

    static int rangeSum(TreeNode root, int low, int high) {
        List<Integer> keys = new ArrayList<>();
        fill(root, keys);
        int sum = 0;
        for (int key : keys) if (key >= low && key <= high) sum += key;   // test every key in the tree
        return sum;
    }
}
```

On the tree with the root 50, the children 30 and 70, and the children 20, 40, 60 and 80 below them, `kth(root, 3)` returns 40, and the sum over 35 to 65 is 150.

<!-- stage: bottleneck -->
### Counting What The Question Needs

```predict
The tree holds one million keys with the smallest possible height, and k is 3. What is the least number of nodes a method must touch to find the third smallest key, and how many does the list method touch?

The third smallest key sits near the left end, so a method that follows the left edge touches about 20 nodes plus a few more. The list method touches all one million nodes.
```

Both list methods cost O(n) time and O(n) space, whatever the question asks. A small `k` needs only the first few keys. A narrow range needs only the keys inside the range. The method should stop reading as soon as the answer is complete. It should also avoid every subtree that cannot hold a useful key, and it should decide that from one comparison.

<!-- stage: insight -->
### Read In Order And Skip Subtrees

An **inorder walk** visits the left subtree, then the node, then the right subtree. In a search tree it visits the keys in sorted order, because everything on the left is smaller than the node and everything on the right is larger. The position of a key in that order is its **rank**, counted from 1 for the smallest. A rank question needs the walk to stop after the kth visit.

#### Stopping After K Visits

A loop with an explicit stack makes the early stop easy. The stack holds the nodes whose left subtree is still being explored. The loop pushes the left spine, which is the chain of left children from a node down to the smallest key below it. It pops one node, counts it as a visit, and then moves to the right child of the popped node and pushes that node's left spine. The kth pop returns the answer. The cost is O(h + k), because the loop pushes at most `h` nodes before the first visit and does constant work per visit afterward.

#### Skipping Subtrees In A Range

A range question gives a low limit and a high limit. A node below the low limit sends the search right, because the node and its whole left subtree are too small. A node above the high limit sends the search left, because the node and its whole right subtree are too large. To **prune** a subtree means to skip it without visiting any node inside. A node inside the range counts, and the search continues on both sides. The nodes the method visits are those inside the range plus the nodes on the paths to its two ends.

<!-- names: inorder walk, rank, prune -->

<!-- stage: variables -->
### The State Of The Two Queries

- **stack** holds the nodes whose own visit is still pending, with the next smallest key on top.
- **node** is the next node whose left spine the loop pushes.
- **visits** counts the keys already read in sorted order, and the loop stops when it equals the requested rank.
- **low** and **high** are the ends of the range, both inclusive.
- **sum** is the total of the keys in the range found so far.

<!-- stage: trace -->
### Stopping Early And Skipping Branches

The cells follow the tree from the top row to the bottom row with one key per node. The pointer `node` marks the node the loop handles in each step.

#### Reading The Third Smallest Key

The tree has the root 50, the children 30 and 70, and the children 20, 40, 60 and 80 below them. The loop looks for the third smallest key.

```trace
{"cells":[50,30,70,20,40,60,80],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"stack":"[50]","visits":0},"note":"The loop pushes 50 onto the stack and moves to its left child."},{"at":{"node":1},"vars":{"stack":"[50, 30]","visits":0},"note":"The loop pushes 30 onto the stack and moves to its left child."},{"at":{"node":3},"vars":{"stack":"[50, 30, 20]","visits":0},"note":"The loop pushes 20 onto the stack and moves to its left child."},{"at":{"node":3},"vars":{"stack":"[50, 30]","visits":1},"note":"The loop pops 20 as visit 1 and then moves to its right child."},{"at":{"node":1},"vars":{"stack":"[50]","visits":2},"note":"The loop pops 30 as visit 2 and then moves to its right child."},{"at":{"node":4},"vars":{"stack":"[50, 40]","visits":2},"note":"The loop pushes 40 onto the stack and moves to its left child."},{"at":{"node":4},"vars":{"stack":"[50]","visits":3},"note":"The loop pops 40 as visit 3. The count equals k, so 40 is the answer."}]}
```

The loop reads 20, 30 and 40 and stops. The nodes 60, 70 and 80 are never touched.

#### Summing Keys From 35 To 65

The same tree gives the sum of the keys between 35 and 65, both included.

```trace
{"cells":[50,30,70,20,40,60,80],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"sum":50},"note":"50 lies in the range, so it joins the sum and the walk continues on both sides."},{"at":{"node":1},"vars":{"sum":50},"note":"30 is below 35, so it and its left subtree are skipped and the walk goes right."},{"at":{"node":4},"vars":{"sum":90},"note":"40 lies in the range, so it joins the sum and the walk continues on both sides."},{"at":{"node":2},"vars":{"sum":90},"note":"70 is above 65, so it and its right subtree are skipped and the walk goes left."},{"at":{"node":5},"vars":{"sum":150},"note":"60 lies in the range, so it joins the sum and the walk continues on both sides."}]}
```

The walk never visits the node 20, because 30 is below the low limit. It never visits the node 80, because 70 is above the high limit. Three nodes are added, and the total is 150.

<!-- stage: code -->
### The Two Queries In Code

```java
final class RankAndRange {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static int kthSmallest(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = node.left; }   // push the left spine
            node = stack.pop();                                            // the smallest unread key
            if (--k == 0) return node.val;                                 // the kth visit ends the walk
            node = node.right;                                             // then read the right subtree
        }
        throw new IllegalArgumentException("k is larger than the tree");
    }

    static int rangeSum(TreeNode node, int low, int high) {
        if (node == null) return 0;                                        // an empty subtree adds nothing
        if (node.val < low) return rangeSum(node.right, low, high);        // node and its left side are too small
        if (node.val > high) return rangeSum(node.left, low, high);        // node and its right side are too large
        return node.val + rangeSum(node.left, low, high) + rangeSum(node.right, low, high);
    }
}
```

The `ArrayDeque` works as a stack through `push` and `pop`, and it never holds `null`, because the loop pushes only non-null nodes.

- **Time** of `kthSmallest` is O(h + k), and the time of `rangeSum` is O(h + m), where `m` is the number of keys inside the range.
- **Space** is O(h) for the stack or the recursion.

<!-- stage: applicability -->
### Using The Order And The Range

#### Recognizing The Cue

Use the inorder walk when the answer depends on the sorted position: the kth smallest, the median, the first k keys. Use pruning when the answer depends on an interval of values: a sum, a count, or a list of keys between two limits. Both need a valid search tree.

#### Stating The Invariant

The invariant of the inorder loop is that the stack top holds the smallest key not yet read, and everything smaller has been counted. The invariant of the range walk is that a skipped subtree holds no key inside the range. Each skip follows from one comparison with the node key.

#### Avoiding The False Friend

The false friend is the level order of the previous lessons. A queue reads nodes by depth, and depth has no relationship to size, so the kth node read is not the kth smallest. A second trap is a rank that is out of bounds. A rank of 0 or one larger than the node count has no answer, and the contract of the problem must say which values of `k` are allowed.

<!-- stage: exercises -->
### Exercises

#### [Build] First K Inorder Values (Author exercise)
<!-- id: tb-kth-first-k -->

**Prerequisites.** The stack loop from this lesson.

**Problem.** Given the root of a binary search tree and an integer `k`, return the first `k` keys in sorted order. If the tree holds fewer than `k` keys, return all of them. Stop reading the tree as soon as `k` keys are collected.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and all keys are distinct.
- **K** satisfies `0 <= k <= 10^4`.
- **Answer** is a list in increasing order with at most `k` entries.
- **Mutation** does not occur.

**Example 1.** Input root 5 with children 3 and 6, where 3 has children 2 and 4, and `k = 3`, output `[2, 3, 4]`.

**Example 2.** Input the same tree and `k = 0`, output `[]`.

**Hint.** What does the loop do after the kth key is added? Which key does the first pop return?

**Changed decision.** The loop collects keys and stops at a count.

#### [Vary] Kth Smallest Element in a BST (LeetCode 230)
<!-- id: tb-kth-smallest -->

**Prerequisites.** The exercise above.

**Problem.** Given the root of a binary search tree and an integer `k`, return the kth smallest key, where the smallest key has rank 1. Use an iterative inorder walk and return the key of the kth popped node.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4, and `1 <= k <= n`.
- **Values** satisfy `0 <= val <= 10^4`, and all keys are distinct.
- **Answer** is an `int`.
- **Mutation** does not occur.

**Example 1.** Input root 3 with children 1 and 4, where 1 has a right child 2, and `k = 1`, output 1.

**Example 2.** Input root 5 with children 3 and 6, where 3 has children 2 and 4 and 2 has a left child 1, and `k = 3`, output 3.

**Hint.** Which node is on top of the stack when the first key is read? When does the counter reach zero?

**Changed decision.** The method returns a single key and does not collect a list.

#### [Boundary] K At Either End (Author exercise)
<!-- id: tb-kth-both-ends -->

**Prerequisites.** The two exercises above.

**Problem.** Given the root of a binary search tree with `n` keys and an integer `k`, return a two-element array. The first entry is the kth smallest key and the second entry is the kth largest key. The kth largest key has rank 1 for the largest key. Use the smallest valid rank 1 and the largest valid rank `n` as test cases.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4, and all keys are distinct.
- **K** satisfies `1 <= k <= n`.
- **Answer** is an `int[]` of length 2.
- **Mutation** does not occur.

**Example 1.** Input root 5 with children 3 and 6, where 3 has children 2 and 4, and `k = 1`, output `[2, 6]`.

**Example 2.** Input the same tree and `k = 5`, output `[6, 2]`.

**Hint.** Which child does the mirrored walk visit first? What does rank `n` from the left equal from the right?

**Changed decision.** A second walk mirrors the first, and both extreme ranks must work.

#### [Recognize] Range Sum of BST (LeetCode 938)
<!-- id: tb-range-sum -->

**Prerequisites.** All three exercises above.

**Problem.** Given the root of a binary search tree and two integers `low` and `high`, return the sum of the keys that lie in the closed range from `low` to `high`. Skip a subtree whenever one comparison shows that it cannot hold a key in the range.

**Constraints.** The limits are:
- **Nodes** number between 1 and 2 * 10^4, and all keys are distinct.
- **Values** satisfy `1 <= val <= 10^5`, and `1 <= low <= high <= 10^5`.
- **Answer** is an `int`, because the sum of at most 2 * 10^4 keys of at most 10^5 each stays below 2.1 * 10^9.
- **Mutation** does not occur.

**Example 1.** Input root 10 with children 5 and 15, where 5 has children 3 and 7 and 15 has a right child 18, with `low = 7` and `high = 15`, output 32.

**Example 2.** Input root 10 with children 5 and 15, where 5 has children 3 and 7, 15 has a right child 18, and 3 has a left child 1 and 7 has a left child 6, with `low = 6` and `high = 10`, output 23.

**Hint.** What does a node below `low` tell you about its left subtree? What does a node above `high` tell you about its right subtree?

**Changed decision.** A comparison with a range limit removes a whole subtree.
