<!-- lesson-kind: standard -->
<!-- lesson-id: iterator-foundations -->
## Hand Out Tree Keys On Demand

<!-- stage: context -->
### Why The Export Job Crawls

An export job streams five million customer ids to a file in sorted order. The ids live in a binary search tree, and the job asks for the next id whenever the file writer is ready. The first version remembers how many ids it has handed out and, for each request, walks the tree from the root until it reaches that position. The first thousand requests finish at once. By the millionth request every call walks a million nodes, and the job slows down until it appears frozen.

The job needs a program that hands out one key per request and remembers exactly where the last request stopped. This lesson asks what small piece of information is enough to continue from that place without starting over.

<!-- stage: naive -->
### Restarting From The Root On Every Request

The direct plan stores a count of the keys already handed out. A request for the next key walks the whole tree in sorted order, counts the keys it passes, and returns the key at the stored count.

```java
final class NextByRestart {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    private final TreeNode root;
    private int handedOut = 0;                          // how many keys earlier requests already returned
    private int seen;                                   // scratch counter for one walk
    private Integer found;

    NextByRestart(TreeNode root) { this.root = root; }

    private void walk(TreeNode node) {
        if (node == null || found != null) return;      // stop once the wanted position is reached
        walk(node.left);
        if (found == null && seen++ == handedOut) found = node.val;   // the key at the stored position
        walk(node.right);
    }

    int next() {
        seen = 0;
        found = null;
        walk(root);                                     // a full walk from the root for every request
        handedOut++;
        return found;
    }
}
```

On the tree with the root 40, the children 20 and 60, and the children 10, 30, 50 and 70 below them, five calls return `10, 20, 30, 40, 50`. The answers are correct.

<!-- stage: bottleneck -->
### Adding Up The Repeated Walks

```predict
The tree holds n keys, and the job makes n requests. Request number i walks at least i nodes before it can stop. About how many nodes does the job visit in total, and what is the cost in big-O terms?

The total is about 1 + 2 + ... + n, which is n squared over 2. The cost is O(n^2), and five million requests would need about twelve trillion steps.
```

Every request repeats the work of all earlier requests. The walk already did the hard part last time: it found the path from the root to the previous key. The restart throws that path away. The method needs to keep exactly the part of the walk that a later request will use. Anything beyond that part wastes memory, and anything less forces another restart from the root.

<!-- stage: insight -->
### Keep The Unfinished Path On A Stack

An **iterator** is an object that hands out one item per call and remembers where it stopped. For a search tree, the memory is the stack of the stack walk from the earlier lesson on rank questions. At any moment the stack holds the nodes whose own turn has not come yet, with the next key on top. These nodes form a chain from the root downward, and each of them is waiting for its right subtree to be read.

#### Loading The Left Spine

The **left spine** of a node is the chain of left children from that node down to the node with no left child. The constructor pushes the left spine of the root. Its top is the smallest key of the tree, because nothing lies to the left of it.

#### Advancing By One Key

A call to `next` pops the top node and remembers its key. The keys in its right subtree come next in sorted order, and they all lie between this key and the node below it on the stack. So the call pushes the left spine of the right child of the popped node. The new top is the next smallest key. The method `hasNext` asks only whether the stack is empty. A node with no right child pushes nothing, and the stack top is then the parent that was waiting.

#### Counting The Total Work

A single call can push many nodes when the right subtree has a tall left spine. Every node is pushed once and popped once during the whole walk. A full run of `n` calls therefore does at most `2n` pushes and pops, so the **amortized cost** of one call is O(1), meaning the average over a sequence of calls. The worst single call costs O(h). The stack never holds more than one path, so the memory is O(h).

<!-- names: iterator, left spine, amortized cost -->

<!-- stage: variables -->
### The State Between Two Calls

- **stack** holds the nodes still waiting, with the next smallest key on top.
- **top** is the next node `next` returns, and `hasNext` is `true` exactly when the stack is not empty.
- **popped** is the node removed by the current call.
- **work** counts one unit for each push or pop, and its total for a full run is at most `2n`.

<!-- stage: trace -->
### Three Calls And The Total Work

Each cell is one key of the tree listed row by row from the root, and the pointer `node` marks the node a call returns.

#### Following The First Three Calls

The tree has the root 40, the children 20 and 60, and the children 10, 30, 50 and 70 below them. The constructor loads the left spine, which holds 40, 20 and 10.

```trace
{"cells":[40,20,60,10,30,50,70],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"stack":"[40, 20]"},"note":"Call 1 pops 10 and returns it. The stack now holds [40, 20]."},{"at":{"node":1},"vars":{"stack":"[40, 30]"},"note":"Call 2 pops 20 and returns it. The stack now holds [40, 30]."},{"at":{"node":4},"vars":{"stack":"[40]"},"note":"Call 3 pops 30 and returns it. The stack now holds [40]."}]}
```

After the third call the stack holds only the root 40. The fourth call pops 40 and pushes 60 and 50, the left spine of its right child.

#### Counting Pushes And Pops Over All Seven Calls

The same tree is read to the end, and the column `total` adds the pushes and pops of every call, including the loading in the constructor.

```trace
{"cells":[40,20,60,10,30,50,70],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"call work":1,"total":4},"note":"Call 1 returns 10 and spends 1 unit(s) on its pop and pushes."},{"at":{"node":1},"vars":{"call work":2,"total":6},"note":"Call 2 returns 20 and spends 2 unit(s) on its pop and pushes."},{"at":{"node":4},"vars":{"call work":1,"total":7},"note":"Call 3 returns 30 and spends 1 unit(s) on its pop and pushes."},{"at":{"node":0},"vars":{"call work":3,"total":10},"note":"Call 4 returns 40 and spends 3 unit(s) on its pop and pushes."},{"at":{"node":5},"vars":{"call work":1,"total":11},"note":"Call 5 returns 50 and spends 1 unit(s) on its pop and pushes."},{"at":{"node":2},"vars":{"call work":2,"total":13},"note":"Call 6 returns 60 and spends 2 unit(s) on its pop and pushes."},{"at":{"node":6},"vars":{"call work":1,"total":14},"note":"Call 7 returns 70 and spends 1 unit(s) on its pop and pushes."}]}
```

The total after the last call is 14, which is twice the number of nodes. Single calls cost between 1 and 3 units, and no call repeated an earlier node.

<!-- stage: code -->
### The Iterator In Code

```java
final class KeyIterator {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    private final Deque<TreeNode> stack = new ArrayDeque<>();

    KeyIterator(TreeNode root) { pushLeftSpine(root); }               // the smallest key ends on top

    private void pushLeftSpine(TreeNode node) {
        while (node != null) { stack.push(node); node = node.left; }  // push every node down the left edge
    }

    boolean hasNext() { return !stack.isEmpty(); }                    // a waiting node means a key remains

    int next() {
        TreeNode popped = stack.pop();                                // pop throws when no key remains
        pushLeftSpine(popped.right);                                  // keys of the right subtree come next
        return popped.val;
    }
}
```

The call `pop` on an empty `ArrayDeque` throws a `NoSuchElementException`, so a caller that ignores `hasNext` gets an error and not a wrong key. The stack never holds `null`, because `pushLeftSpine` stops at the first missing child.

- **Time** is O(1) amortized per call and O(h) for one call in the worst case.
- **Space** is O(h), because the stack holds one root-to-node path.

<!-- stage: applicability -->
### Using The Stored Path

#### Recognizing The Cue

Use an iterator when a client needs the next key on demand, such as paging through results, merging two trees, or comparing two trees key by key. The client may stop at any time, so the program must not build the whole sorted list first.

#### Stating The Invariant

The invariant is that the stack holds the nodes still waiting, and its top is the smallest key not yet returned. A pop followed by loading the left spine of the right child restores it. Everything below the top is larger than every key in the subtree that was just loaded.

#### Avoiding The False Friend

The false friend is the restart from the root. It looks simple and returns correct keys, but the total cost grows with the square of the key count. A second trap is a copy of all keys into a list in the constructor. It gives O(1) calls, but it costs O(n) memory and O(n) time before the first key appears. The stack keeps both costs proportional to the height.

<!-- stage: exercises -->
### Exercises

#### [Build] Push Left Spine (Author exercise)
<!-- id: tb-iter-left-spine -->

**Prerequisites.** The left spine and the stack from this lesson.

**Problem.** Take the root of a binary search tree, push its left spine onto a stack, and return the keys on the stack, listed from the bottom of the stack to the top. A null root gives an empty list. The top of the stack holds the smallest key of the tree.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and all keys are distinct.
- **Values** satisfy `-10^9 <= val <= 10^9`.
- **Answer** is a list whose last entry is the smallest key.
- **Mutation** does not occur.

**Example 1.** Input root 40 with children 20 and 60, where 20 has children 10 and 30 and 60 has children 50 and 70, output `[40, 20, 10]`.

**Example 2.** Input root 5 with only a right child 8, output `[5]`.

**Hint.** Which child does the loop follow? What ends the loop?

**Changed decision.** The loop follows left links only and keeps every node it passes.

#### [Vary] Advance One Inorder Step (Author exercise)
<!-- id: tb-iter-advance -->

**Prerequisites.** The exercise above.

**Problem.** A search tree and an integer `j` are supplied. Create the stack with the left spine of the root and then perform `j` pops. After each pop, push the left spine of the right child of the popped node. Return the keys on the stack after the jth pop, from the bottom of the stack to the top.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4, and all keys are distinct.
- **J** satisfies `1 <= j <= n`.
- **Answer** is a list of keys, possibly empty.
- **Mutation** does not occur.

**Example 1.** Input the tree above and `j = 1`, output `[40, 20]`.

**Example 2.** Input the same tree and `j = 2`, output `[40, 30]`.

**Hint.** Which node does a pop remove? Whose left spine joins the stack afterward?

**Changed decision.** A pop adds the left spine of the right child, and only then does the next call begin.

#### [Boundary] Empty Iterator And Right Chain (Author exercise)
<!-- id: tb-iter-edges -->

**Prerequisites.** The two exercises above.

**Problem.** For a search tree, create the stack as before and call a pop while the stack is not empty, which is the test `hasNext`. Return a two-element array holding the number of keys returned and the largest size the stack reached. A null root gives zero keys and a largest size of zero.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and all keys are distinct.
- **Shapes** include the empty tree, a single node, and a chain where every node has only a right child.
- **Answer** is an `int[]` of length 2.
- **Mutation** does not occur.

**Example 1.** Input a null root, output `[0, 0]`.

**Example 2.** Input a chain of three nodes 1, 2, 3 where each node is the right child of the previous one, output `[3, 1]`.

**Hint.** What does the stack hold for a chain that has no left children? What does `hasNext` return before the first pop?

**Changed decision.** The loop condition is the emptiness of the stack, and a chain keeps the stack at size 1.

#### [Recognize] Binary Search Tree Iterator (LeetCode 173)
<!-- id: tb-bst-iterator -->

**Prerequisites.** All three exercises above.

**Problem.** Implement a class `BSTIterator` built from the root of a binary search tree. The method `next` returns the next smallest key and moves the pointer forward, and the method `hasNext` returns `true` if a key remains. The class must support `next` in amortized O(1) time and use O(h) memory.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^5, and all keys are distinct.
- **Values** satisfy `0 <= val <= 10^6`.
- **Calls** to `next` happen only when `hasNext` is `true`, and the total number of calls is at most 10^5.
- **Mutation** does not occur.

**Example 1.** Input root 7 with children 3 and 15, where 15 has children 9 and 20, and the calls `next, next, hasNext, next, hasNext`, output `3, 7, true, 9, true`.

**Example 2.** Input the same tree and the calls `next` five times followed by `hasNext`, output `3, 7, 9, 15, 20, false`.

**Hint.** What does the constructor load? Which spine does `next` load after a pop?

**Changed decision.** The stack persists between calls, and each call advances it by one key.
