<!-- lesson-kind: combination -->
<!-- lesson-id: group-nodes-by-depth-with-a-queue -->
## Group Nodes By Depth With A Queue

<!-- stage: context -->
### Why The Org Chart Tool Crashes

A company tool draws an org chart one management layer per row and adds up the salaries of each row. The first version walks the tree with a recursive method that carries the depth as an argument, and it works on every sample chart. Then a customer loads a chart in which each person manages exactly one other person, a reporting chain with half a million links. The tool does not slow down. It dies with a stack overflow error, and the half-drawn chart is lost.

Each row needs the people of one depth together, in order, and the same job must work for managers with any number of reports. This lesson asks how to produce the rows for any tree without a call stack that grows with the height of the tree.

<!-- stage: contributions -->
### What The Tree And Queue Each Add

Two earlier ideas combine here, and each supplies one half of the answer. The tree supplies the children. A node knows its direct reports, and a node reaches no other node except through them. The tree alone gives no order across branches, so a walk that follows one branch to its end leaves the current row before it finishes it.

The queue from the stacks and queues chapter supplies the order. A first-in, first-out queue hands out nodes in the order they arrived, so the children of shallow nodes always leave the queue before the children of deep nodes. The queue alone has no idea where one row ends. The tree and the queue together give rows in order with one pass over the nodes, and a stored count marks each row boundary.

<!-- stage: naive -->
### Carrying The Depth Through A Recursive Walk

The direct plan walks the tree recursively and carries the depth in an argument. The method keeps one running sum for each depth in a list and adds each node's value to the entry at its depth.

```java
final class SumsByRecursion {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static void walk(TreeNode node, int depth, List<Long> sums) {
        if (node == null) return;
        if (depth == sums.size()) sums.add(0L);               // the first node of a new depth opens a new entry
        sums.set(depth, sums.get(depth) + node.val);          // add this value to its row
        walk(node.left, depth + 1, sums);                     // one call frame for each level below
        walk(node.right, depth + 1, sums);
    }

    static List<Long> levelSums(TreeNode root) {
        List<Long> sums = new ArrayList<>();
        walk(root, 0, sums);
        return sums;
    }
}
```

On the tree with the root 5, the children 3 and 8, and the children 1 and 4 under the node 3, the sums are `[5, 11, 5]`. The method is correct on every tree small enough for its call stack.

<!-- stage: bottleneck -->
### Finding The Crash

```predict
The tree is a chain of 500000 nodes, each with one child. What does the recursive method do, and which cost grows with the height of the tree?

The method makes 500000 nested calls, and each call keeps a frame on the call stack, so the program throws a StackOverflowError. The time is O(n), but the call stack grows to O(h), which is 500000 frames here.
```

The failure is a crash, and not a slowdown. A call stack is a small fixed region, and a height of a few thousand to a few tens of thousands of frames fills it. The method also mixes two jobs in one call, because it tracks the depth and the visiting order together, and a node with many children needs a loop over its list in place of two fixed calls.

The program needs a loop in which the waiting nodes live in an ordinary collection that grows on the heap, and in which each row is processed completely before the next one starts.

<!-- stage: insight -->
### One Queue Loop For Every Row

The loop keeps a queue of nodes that are discovered but not yet expanded. Before each row it reads the **level size**, which is the number of nodes in the queue at that moment and exactly the number of nodes in the row. It removes that many nodes, adds each value to the row result, and adds the children of each removed node to the back. The row's nodes are the **frontier**, the set of nodes being expanded. Their children wait behind the frontier and form the next row.

#### Counting Rows With The Loop

The depth is the number of completed passes of the outer loop, so no argument carries it. A row result can be a list, a sum, the last node, or any other aggregate, because the loop hands every node of the row to the same inner step. A limit on the depth is a test on the pass counter before the next pass starts.

#### Expanding Any Number Of Children

The step that adds children is the only part that depends on the shape of the node. A binary node has a left and a right reference, and each is added when it is not null. An N-ary node has a list of children, and **child expansion** is a loop that adds every child in order. The row boundary, the pass counter and the aggregate stay the same. Because the queue lives on the heap, the loop handles a chain of half a million nodes with a queue that never holds more than one node.

<!-- names: level size, frontier, child expansion -->

<!-- stage: variables -->
### The State Of The Row Loop

- **queue** holds the nodes discovered and not yet expanded, ordered by depth.
- **size** is the level size read once before the removals of a row.
- **depth** counts the rows already finished, and it is 0 for the root row.
- **row** is the aggregate for the current row, such as a sum or a list.
- **result** is the list of finished rows.

<!-- stage: trace -->
### Wide Rows And A Row Limit

#### Summing The Rows Of A Tree With Many Children

The tree has the root 1 with the children 2, 3 and 4, where 3 has the children 5 and 6 and 4 has the child 7. Each cell is one node, listed in the order the queue finds it. Two pointers track the queue: `removed` is the last node taken out, and `queued` is the last node put in.

```trace
{"cells":[1,2,3,4,5,6,7],"pointers":["removed","queued"],"steps":[{"at":{"removed":-1,"queued":0},"vars":{"depth":0},"note":"Start: the queue holds only the root."},{"at":{"removed":0,"queued":3},"vars":{"size":1,"row sum":1},"note":"Row 0 ends. The loop stored size 1, removed that many nodes and found the sum 1."},{"at":{"removed":3,"queued":6},"vars":{"size":3,"row sum":9},"note":"Row 1 ends. The loop stored size 3, removed that many nodes and found the sum 9."},{"at":{"removed":6,"queued":6},"vars":{"size":3,"row sum":18},"note":"Row 2 ends. The loop stored size 3, removed that many nodes and found the sum 18."}]}
```

Child expansion added three children for the root, and later two and one. The row sums are 1, 9 and 18.

#### Stopping After Three Rows

The tree has the root 1 with the children 2 and 3, the node 4 below the node 2, the node 5 below the node 3, and the node 6 below the node 4. The loop reads the right-side view of only the first three rows.

```trace
{"cells":[1,2,3,4,5,6],"pointers":["removed","queued"],"steps":[{"at":{"removed":-1,"queued":0},"vars":{"depth":0},"note":"Start: the queue holds only the root."},{"at":{"removed":0,"queued":2},"vars":{"depth":1,"view":"[1]"},"note":"Row 0 ends. The last node removed was 1, so it joins the view. The pass counter is now 1."},{"at":{"removed":2,"queued":4},"vars":{"depth":2,"view":"[1, 3]"},"note":"Row 1 ends. The last node removed was 3, so it joins the view. The pass counter is now 2."},{"at":{"removed":4,"queued":5},"vars":{"depth":3,"view":"[1, 3, 5]"},"note":"Row 2 ends. The last node removed was 5, so it joins the view. The pass counter is now 3. The counter equals k, so the loop stops."}]}
```

Here `k` is the number of rows the caller wants, and it is 3. The pass counter reaches 3 and the loop ends. The node 6 was discovered during the last pass but never removed.

<!-- stage: code -->
### The Row Loop For Both Tree Shapes

```java
final class RowLoop {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static final class NaryNode {
        int val;
        List<NaryNode> children = new ArrayList<>();
        NaryNode(int val) { this.val = val; }
    }

    static List<Long> levelSums(TreeNode root) {
        List<Long> result = new ArrayList<>();
        if (root == null) return result;                       // the queue cannot hold null
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();                           // the row boundary
            long row = 0;
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                row += node.val;                               // use a long so large sums stay exact
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            result.add(row);
        }
        return result;
    }

    static List<List<Integer>> narySlices(NaryNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        Deque<NaryNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> row = new ArrayList<>(size);
            for (int i = 0; i < size; i++) {
                NaryNode node = queue.poll();
                row.add(node.val);
                queue.addAll(node.children);                   // child expansion adds every child in order
            }
            result.add(row);
        }
        return result;
    }
}
```

The queue lives on the heap, so a chain of half a million nodes needs no deep call stack.

- **Time** is O(n), because each node is queued once and removed once.
- **Space** is O(w) for the queue, where `w` is the widest row, plus the result.

<!-- stage: applicability -->
### Using The Combined Loop

#### Recognizing The Cue

Use the row loop when the answer is organized by depth: a list per row, an aggregate per row, one chosen node per row, or only the first few rows. Trees with any number of children fit as well, because only child expansion changes.

#### Stating The Invariant

The invariant is that at the top of each pass the queue holds exactly the nodes of one depth, and the pass counter equals that depth. The stored size protects the invariant, since the children added during a pass land behind the row.

#### Avoiding The False Friend

The false friend is a recursive walk that passes the depth down as an argument. It gives the same rows on a small tree and crashes on a tall one. A second trap is an aggregate that overflows. A row of many large values can exceed the range of an `int`, so the sum uses a `long`. A third trap is a limit on the depth that is read inside the loop and compared with a changing value. The pass counter is the safe value to compare.

<!-- stage: exercises -->
### Exercises

#### [Build] Level Sums Of A Binary Tree (LeetCode 102)
<!-- id: tbc-level-sums -->

**Prerequisites.** The queue loop and the stored row size from this lesson.

**Problem.** Return the sum of the values at each depth of a binary tree, as a list where entry `d` is the sum of the depth `d` nodes. The root has depth 0. A null root gives an empty list.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^5.
- **Values** satisfy `-10^9 <= val <= 10^9`.
- **Answer** is a list of `long` values, since a row sum can exceed the `int` range.
- **Mutation** does not occur.

**Example 1.** Input root 5 with children 3 and 8, where 3 has children 1 and 4, output `[5, 11, 5]`.

**Example 2.** Input root 1000000000 with two children, each 1000000000, output `[1000000000, 2000000000]`.

**Hint.** What type holds a sum above 2147483647? Where does the row sum reset?

**Changed decision.** Each row produces one number, and the sum needs a wider type.

#### [Vary] Bottom-Up Zigzag Level Order (LeetCode 103)
<!-- id: tbc-bottom-up-zigzag -->

**Prerequisites.** The exercise above.

**Problem.** Return the rows of a binary tree from the deepest row to the root row. Inside the rows of even depth the values read from left to right, and inside the rows of odd depth they read from right to left. The direction depends on the depth of the row and not on its position in the output.

**Constraints.** The limits are:
- **Nodes** number between 0 and 2000.
- **Values** satisfy `-100 <= val <= 100`.
- **Answer** is a list of lists with the deepest row first, and a null root gives an empty list.
- **Mutation** does not occur.

**Example 1.** Input root 3 with children 9 and 20, where 20 has children 15 and 7, output `[[15, 7], [20, 9], [3]]`.

**Example 2.** Input root 1 with children 2 and 3, where 2 has a child 4 and 3 has a child 5, output `[[4, 5], [3, 2], [1]]`.

**Hint.** Which counter tells the direction of a row? Where does the output list receive each finished row?

**Changed decision.** The rows are placed in reverse order, and the direction follows the depth.

#### [Boundary] Right View Of The First K Rows (LeetCode 199)
<!-- id: tbc-right-view-k -->

**Prerequisites.** The two exercises above.

**Problem.** Return the right-side view of a binary tree limited to the first `k` rows: the last node of each of the rows at depths 0 to `k - 1`. If `k` is larger than the height, return the view of every row. If `k` is 0 or the tree is empty, return an empty list. Stop the loop when the pass counter reaches `k`.

**Constraints.** The limits are:
- **Nodes** number between 0 and 100.
- **Values** satisfy `-100 <= val <= 100`.
- **K** satisfies `0 <= k <= 200`.
- **Mutation** does not occur.

**Example 1.** Input root 1 with children 2 and 3, where 2 has a right child 5 and 3 has a right child 4, and `k = 2`, output `[1, 3]`.

**Example 2.** Input the same tree and `k = 0`, output `[]`.

**Hint.** When is the counter compared with `k`? What does `k = 10` give for a tree with three rows?

**Changed decision.** The loop has a second stopping rule, and it reads the pass counter.

#### [Recognize] N-ary Tree Level Order Traversal (LeetCode 429)
<!-- id: tbc-nary-level-order -->

**Prerequisites.** All three exercises above.

**Problem.** Given the root of an N-ary tree, where each node holds a value and a list of children, return the values of the nodes grouped by depth, with the children of each node taken in list order. A null root gives an empty list.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** satisfy `0 <= val <= 10^4`, and values may repeat.
- **Children** of a node may be zero, one or many.
- **Mutation** does not occur.

**Example 1.** Input root 1 with children 3, 2 and 4, where 3 has children 5 and 6, output `[[1], [3, 2, 4], [5, 6]]`.

**Example 2.** Input a single node 7 with no children, output `[[7]]`.

**Hint.** What replaces the two `null` checks for a binary node? What stays the same in the outer loop?

**Changed decision.** Child expansion loops over a list, and the row logic is unchanged.
