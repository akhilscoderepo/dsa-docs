<!-- lesson-kind: standard -->
<!-- lesson-id: iterator-foundations -->
## Iterator Foundations

<!-- stage: context -->
### The Reading Room Attendant

A reading room keeps its catalogue cards on branching shelves, with earlier titles on the left of each card and later titles on the right. Patrons come one at a time and each of them says only "next, please". They may ask three times and walk away, or they may ask until the shelves are empty, and the attendant never knows which. After each request he must hand over the next card in alphabetical order, and he must also be able to answer the question "is there another card?" at any moment.

The attendant has a small trolley, big enough for a handful of cards at a time, and the room has a rule that the shelves may not be rearranged. A request must be quick, because patrons dislike waiting, and the trolley is the only extra space he has.

<!-- stage: naive -->
### Copy Every Card Onto A Table

The straightforward plan is to prepare for the patron before the first request. The attendant walks all the shelves in alphabetical order and lays every card on a long table. A request then hands over the card at the current place on the table and moves the place forward, and "is there another card" asks whether the place is still on the table.

```java
final class FlatReader {
    private final List<Integer> table = new ArrayList<>();
    private int place = 0;

    FlatReader(Node root) { lay(root); }

    private void lay(Node card) {
        if (card == null) return;
        lay(card.left);
        table.add(card.val);
        lay(card.right);
    }

    boolean hasNext() { return place < table.size(); }
    int next() { return table.get(place++); }
}
```

Each request after the setup is a single step, and every request returns the right card because the table holds the whole sorted sequence.

<!-- stage: bottleneck -->
### The Table Holds Everything Nobody Asked For

The setup costs O(n) time before the first patron has received a single card, and the table needs O(n) space. A shelf with a million cards pays a million steps and a million table places for a patron who asks three times. The trolley rule makes this plan unworkable, since the table is exactly as large as the whole catalogue.

The opposite shortcut, finding the next card by starting from the top shelf every time, is no better. Locating the card after a given one by searching from the root costs O(h), and a patron who goes through all n cards pays O(n h), which is quadratic for a long chain. The need is a method that starts instantly, remembers only a short path, and spends a small constant amount per request when averaged over a whole reading, so that n requests cost O(n) in total with only O(h) memory.

<!-- stage: insight -->
### Keep Only The Path Ahead

The next card in order is always at the end of a path that begins at the unvisited top of the structure: from any shelf go left as far as possible. So the attendant keeps a stack holding this **left spine**, the chain of shelves from the current starting shelf down to its leftmost card. The card on top of the stack is the smallest card not yet handed out, and the cards beneath it are its **unvisited ancestors**, which are waiting for their turn after everything on their left has been consumed.

A request pops the top card. Its left side is already finished, so the only remaining cards in its subtree are on its right. The attendant then refills the stack with the left spine of that right child, which makes the next smallest card the new top. This is a **lazy refill**: the spine of a right side is loaded only at the moment it becomes relevant, not at the start. If there is no right child, the refill adds nothing, and the new top is the next unvisited ancestor.

The invariant is that the stack always holds the unvisited ancestors of the next card in order, with the next card on top, so that the stack is empty exactly when every card has been handed out.

<!-- names: left spine, unvisited ancestors, lazy refill -->

A single request may push as many as h cards, but each card is pushed once and popped once in the entire reading, so n requests cost O(n) together.

<!-- stage: variables -->
### Stack, Top And Refill Cursor

The `stack` is an `ArrayDeque<Node>` that holds the left spine of everything unvisited, with the smallest unvisited node on top. It is filled by the helper `pushLeft(node)`, which follows `left` links and pushes every node it passes. The method `hasNext()` is simply `!stack.isEmpty()`, which means nothing is stored separately to say whether the iteration is over. The method `next()` pops `top`, calls `pushLeft(top.right)`, and returns `top.val`. Calling `next()` when the stack is empty is a contract violation, and `ArrayDeque.pop()` throws `NoSuchElementException` in that case.

<!-- stage: trace -->
### Three Requests And A Long Right Chain

The first trace builds an iterator on the shelves 10, 5, 15, 3, 7, 12, 20, 2, null, 6. The marker `node` sits on the card that sits on top of the stack, and `stack` lists the stack from the top down. Loading the spine puts 10, 5, 3 and 2 on the stack with 2 on top, so the first request returns 2 at once. The request that returns 5 is the interesting one: after popping 5 the attendant pushes the spine of 7, which is 7 and then 6, so 6 is the next card.

```trace
{"cells":["10","5","15","3","7","12","20","2","null","6"],"pointers":["node"],"steps":[{"at":{"node":7},"vars":{"returned":"none","stack":"2 3 5 10"},"note":"The constructor loads the left spine, so the stack holds 2 3 5 10 from the top down and the smallest card 2 is on top."},{"at":{"node":3},"vars":{"returned":2,"stack":"3 5 10"},"note":"The request pops 2 and returns it. It has no right child, so nothing is pushed. The next card is 3."},{"at":{"node":1},"vars":{"returned":3,"stack":"5 10"},"note":"The request pops 3 and returns it. It has no right child, so nothing is pushed. The next card is 5."},{"at":{"node":9},"vars":{"returned":5,"stack":"6 7 10"},"note":"The request pops 5 and returns it. Its right child starts a new spine, so 7 6 is pushed. The next card is 6."},{"at":{"node":4},"vars":{"returned":6,"stack":"7 10"},"note":"The request pops 6 and returns it. It has no right child, so nothing is pushed. The next card is 7."},{"at":{"node":0},"vars":{"returned":7,"stack":"10"},"note":"The request pops 7 and returns it. It has no right child, so nothing is pushed. The next card is 10."}]}
```

The second trace uses the shelf plan 1, null, 2, null, 3, a chain that leans right. Only one card is on the stack at any moment, since each card has no left side. Every request pops the single card, pushes its right child, and the stack stays at one card until the last request leaves it empty, after which `hasNext` would answer false.

```trace
{"cells":["1","null","2","null","3"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"returned":"none","stack":"1"},"note":"The constructor loads the left spine, so the stack holds 1 from the top down and the smallest card 1 is on top."},{"at":{"node":2},"vars":{"returned":1,"stack":"2"},"note":"The request pops 1 and returns it. Its right child starts a new spine, so 2 is pushed. The next card is 2."},{"at":{"node":4},"vars":{"returned":2,"stack":"3"},"note":"The request pops 2 and returns it. Its right child starts a new spine, so 3 is pushed. The next card is 3."},{"at":{"node":-1},"vars":{"returned":3,"stack":"empty"},"note":"The request pops 3 and returns it. It has no right child, so nothing is pushed. The stack is empty, so no card is left."}]}
```

<!-- stage: code -->
### An Iterator On A Short Stack

```java
final class BstIterator {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    private final ArrayDeque<Node> stack = new ArrayDeque<>();

    BstIterator(Node root) { pushLeft(root); }

    private void pushLeft(Node node) {
        while (node != null) {
            stack.push(node);
            node = node.left;
        }
    }

    boolean hasNext() { return !stack.isEmpty(); }

    int next() {
        Node top = stack.pop();
        pushLeft(top.right);
        return top.val;
    }
}
```

The constructor costs O(h), a single `next` costs O(h) in the worst case and O(1) on average, since each node is pushed once and popped once. The stack never holds more than h nodes, so the extra space is O(h).

<!-- stage: applicability -->
### When Keys Are Pulled One By One

Use this iterator when a consumer walks a sorted structure step by step and may stop early: merging two sorted trees one key at a time, paging through an ordered index, or a loop that needs the next key to decide whether to continue. The invariant is that the stack holds the unvisited ancestors of the next key in order, so reading the top is always enough to answer.

The first false friend is the root-traversal restart, where each `next` call runs an inorder walk from the top and counts to the position after the previous one. It is correct and quadratic over a full reading. A second false friend is the up-front flattening, which makes every request O(1) but pays O(n) in time and memory before the first one, and it also goes stale if the tree changes between requests. A third is believing the worst-case O(h) request makes the whole reading cost O(n h); the amortised cost of a full reading is O(n).

In Java, `ArrayDeque.pop()` throws on an empty stack, so guard `next()` with the `hasNext()` contract, and never test emptiness by catching that exception. Use `ArrayDeque` and not `Stack`, which is synchronized and legacy.

<!-- stage: exercises -->
### Exercises

#### [Build] Push Left Spine (Author exercise)
<!-- id: tb-push-left-spine -->

**Prerequisites.** The BST invariant lesson and the explicit stack of Chapter 11.

**Problem.** A search tree is stored in level order with `null` at each missing child. Load the stack by pushing the root and then every node reached by repeated left links, and return the stack contents as a list of keys from the top of the stack down. An empty tree gives an empty list.

**Constraints.** 0 <= values.length <= 3000 and keys are distinct integers between 0 and 100000.

**Example 1.** Input `values = [10, 5, 15, 3, 7, 12, 20, 2, null, 6]`, output `[2, 3, 5, 10]`.

**Example 2.** Input `values = [4, null, 6]`, output `[4]`.

**Hint.** Which node is pushed first, and which node ends up on top?

**Changed decision.** The loop follows only left links and pushes every node it passes, so the top of the stack is the smallest key in the tree.

#### [Vary] Advance One Inorder Step (Author exercise)
<!-- id: tb-advance-one-step -->

**Prerequisites.** The Push Left Spine rung.

**Problem.** After loading the spine, perform exactly `m` calls of the pop-and-refill step: pop the top, push the left spine of its right child, and remember the popped key. Return the key popped by the last call followed by the stack contents from the top down.

**Constraints.** 1 <= m <= values.length <= 3000, keys are distinct integers between 0 and 100000, and the tree is a search tree.

**Example 1.** Input `values = [10, 5, 15, 3, 7, 12, 20, 2, null, 6]`, `m = 3`, output `[5, 6, 7, 10]`.

**Example 2.** Input `values = [4, null, 6]`, `m = 1`, output `[4, 6]`.

**Hint.** After popping a node whose right child exists, which chain of nodes goes on the stack?

**Changed decision.** A step pops one node and then loads the left spine of its right child, so the stack changes only by the nodes that have just become relevant.

#### [Boundary] Empty Iterator And Right Chain (Author exercise)
<!-- id: tb-empty-and-right-chain -->

**Prerequisites.** The Advance One Inorder Step rung and the guard on an empty stack.

**Problem.** Build the iterator for the tree and run a list of operations, each either `hasNext` or `next`. Report one result per operation: `true` or `false` for `hasNext`, the key for `next`, and the word `none` for a `next` that is requested when no key is left. The tree may be empty or may lean entirely to the right.

**Constraints.** 0 <= values.length <= 2000 with distinct integer keys between 0 and 100000, and 1 <= operations.length <= 4000.

**Example 1.** Input `values = []`, `operations = [hasNext, next]`, output `[false, none]`.

**Example 2.** Input `values = [1, null, 2, null, 3]`, `operations = [next, next, hasNext, next, hasNext]`, output `[1, 2, true, 3, false]`.

**Hint.** What does `hasNext` look at, and what should `next` check before it pops?

**Changed decision.** `hasNext` is defined as a non-empty stack, and `next` checks it first, so an empty tree and an exhausted iterator both answer without an exception.

#### [Recognize] Binary Search Tree Iterator (LeetCode 173)
<!-- id: tb-bst-iterator -->

**Prerequisites.** The Empty Iterator And Right Chain rung and the lazy refill.

**Problem.** Implement an iterator over a search tree given in level order, where `next` returns the next smallest key and `hasNext` tells whether any key remains. Operations arrive as a string of letters, `N` for `next` and `H` for `hasNext`, and a `next` is only requested when a key remains. Return the answers in order, with `true` or `false` for each `H`. Amortised O(1) per call and O(h) space are expected.

**Constraints.** 1 <= values.length <= 10000, keys are distinct integers between 0 and 100000, and the operation string has between 1 and 20000 letters.

**Example 1.** Input `values = [6, 2, 9, 1, 4, 8, 11]`, `ops = "NNHNNNNH"`, output `[1, 2, true, 4, 6, 8, 9, true]`.

**Example 2.** Input `values = [5]`, `ops = "NH"`, output `[5, false]`.

**Hint.** Which nodes must be on the stack so that its top is always the smallest unvisited key?

**Changed decision.** Nothing is flattened at the start; only a single left spine is stored, and each pop loads the spine of one right child.
