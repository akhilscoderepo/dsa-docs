<!-- lesson-kind: standard -->
<!-- lesson-id: kth-and-range-queries -->
## Kth And Range Queries

<!-- stage: context -->
### The Orchard Weigh Station

At the orchard weigh station, crates of apples hang on a branching rack. Each crate has a weight painted on it. Lighter crates always hang somewhere to the left below a crate, and heavier ones somewhere to the right. A grocer calls ahead with two kinds of orders. The first reads "send me the third lightest crate", and the second reads "send me every crate weighing between 40 and 70 kilograms, and tell me their total".

The station has about a million crates on the rack, and orders arrive all day. The clerk knows the rack is sorted in the sense of left and right, but he has never worked out how to use that for orders that count from the light end or cover a band of weights.

<!-- stage: naive -->
### Unload The Whole Rack To A Table

The plain method takes every crate off the rack in order of weight and lays the weights out in a long line on a table. The third lightest crate is then the third item on the line, and the band order is answered by walking the line and adding every weight that lies between the two limits.

```java
static int kthByTable(Node rack, int k) {
    List<Integer> table = new ArrayList<>();
    unload(rack, table);
    return table.get(k - 1);
}

static int bandByTable(Node rack, int low, int high) {
    List<Integer> table = new ArrayList<>();
    unload(rack, table);
    int total = 0;
    for (int w : table) if (w >= low && w <= high) total += w;
    return total;
}

static void unload(Node crate, List<Integer> out) {
    if (crate == null) return;
    unload(crate.left, out);
    out.add(crate.val);
    unload(crate.right, out);
}
```

Because the unloading goes left side, then crate, then right side, the table is in weight order, and both orders get correct answers.

<!-- stage: bottleneck -->
### A Million Crates For Three

The table method touches all n crates and stores all n weights, so each order costs O(n) time and O(n) memory. For the third lightest crate on a million-crate rack, 999,997 of the crates handled have nothing to do with the answer. A band order that matches only ten crates still reads every weight to decide that the rest are outside the band.

Both orders can cut the work. Counting from the light end only needs the first k crates of the sorted sequence, and the rack can produce them one at a time, so the walk can stop the moment the kth appears. For a band, whole sides of the rack are decided by a single comparison: if a crate is already lighter than the lower limit, everything on its left is lighter still, and if it is heavier than the upper limit, everything on its right is heavier still. The target is O(h + k) for the count order and O(h + m) for a band that holds m crates.

<!-- stage: insight -->
### Visit In Order And Stop Early

Walking left side, crate, right side produces the weights in increasing order, and this **sorted visit** can be paused. Replace the recursion by an explicit stack: push the crate and keep moving left until there is nothing more on the left, then pop. Each pop is the next heavier crate. A **countdown** starts at k and drops by one with every pop, and the pop that takes it to zero is the answer. The walk then stops, having paid only for the left path and the k crates visited.

A band order uses the same ordering, together with a **pruning rule**. At a crate lighter than the lower limit, the crate and all of its left side are out, so only the right side is worth entering. At a crate heavier than the upper limit, the crate and its right side are out, so only the left side remains. At a crate inside the band, both sides may hold matches, and the crate is added to the total. The walk therefore enters only branches that overlap the band.

The invariant for the count order is that when the countdown is r, the stack plus the unvisited right sides hold exactly the crates heavier than the last pop, so the next pop is the next rank. For the band order, every branch that was skipped lies completely outside the band.

<!-- names: sorted visit, countdown, pruning rule -->

Level order, the walk by depth from the previous lessons, has no connection to weight rank and cannot be used for either order.

<!-- stage: variables -->
### Stack, Countdown And Band Limits

The `stack` is an `ArrayDeque<Node>` holding the crates whose left sides are being worked through, and it grows by the length of a left path and shrinks by one at each pop. The cursor `node` moves left while pushing and then right after each pop. The int `k` is the countdown and is decremented once per pop. For a band, `low` and `high` are fixed inclusive limits and `total` is the running sum, which should be a `long` when the weights are large. A recursive band walk needs no stack, since the call stack plays that part, but its depth equals the height.

<!-- stage: trace -->
### Third Lightest And A Weight Band

The first trace asks for the third lightest crate on the rack 5, 3, 6, 2, 4, null, null, 1. The marker `node` sits on each popped crate, and `stack` lists what is still waiting, top first. The first pops are the left path crates 1 and 2 and then 3, and the countdown hits zero at 3, so the crates 4, 5 and 6 are never touched.

```trace
{"cells":["5","3","6","2","4","null","null","1"],"pointers":["node"],"steps":[{"at":{"node":7},"vars":{"countdown":2,"stack":"2 3 5"},"note":"The crate 1 is popped as the next heavier crate and the countdown drops to 2."},{"at":{"node":3},"vars":{"countdown":1,"stack":"3 5"},"note":"The crate 2 is popped as the next heavier crate and the countdown drops to 1."},{"at":{"node":1},"vars":{"countdown":0,"stack":"5"},"note":"The crate 3 is popped as the next heavier crate and the countdown drops to 0. The countdown has reached zero, so 3 is the answer and the walk stops."}]}
```

The second trace sums the weights between 5 and 9 on a rack of fifteen crates laid out in a complete shape, 8, 4, 12, 2, 6, 10, 14 and so on. Only visited crates appear. The crate 4 is lighter than the lower limit, so its left side is skipped, and 12 and 10 are heavier than the upper limit, so their right sides are skipped. The crates 2, 14 and the remaining outer ones are never touched at all.

```trace
{"cells":["8","4","12","2","6","10","14","1","3","5","7","9","11","13","15"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"low":5,"high":9,"total":8},"note":"The crate 8 lies inside the band and is added, so the total becomes 8 and both sides are entered."},{"at":{"node":1},"vars":{"low":5,"high":9,"total":8},"note":"The crate 4 is lighter than 5, so it and its left side are out and only the right side is entered."},{"at":{"node":4},"vars":{"low":5,"high":9,"total":14},"note":"The crate 6 lies inside the band and is added, so the total becomes 14 and both sides are entered."},{"at":{"node":9},"vars":{"low":5,"high":9,"total":19},"note":"The crate 5 lies inside the band and is added, so the total becomes 19 and both sides are entered."},{"at":{"node":10},"vars":{"low":5,"high":9,"total":26},"note":"The crate 7 lies inside the band and is added, so the total becomes 26 and both sides are entered."},{"at":{"node":2},"vars":{"low":5,"high":9,"total":26},"note":"The crate 12 is heavier than 9, so it and its right side are out and only the left side is entered."},{"at":{"node":5},"vars":{"low":5,"high":9,"total":26},"note":"The crate 10 is heavier than 9, so it and its right side are out and only the left side is entered."},{"at":{"node":11},"vars":{"low":5,"high":9,"total":35},"note":"The crate 9 lies inside the band and is added, so the total becomes 35 and both sides are entered."}]}
```

<!-- stage: code -->
### Early Stop And Pruned Band

```java
final class OrderedQueries {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int kthSmallest(Node root, int k) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        Node node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = node.left; }
            node = stack.pop();
            if (--k == 0) return node.val;
            node = node.right;
        }
        throw new IllegalArgumentException("k is larger than the tree");
    }

    static long bandSum(Node node, int low, int high) {
        if (node == null) return 0;
        if (node.val < low) return bandSum(node.right, low, high);
        if (node.val > high) return bandSum(node.left, low, high);
        return node.val + bandSum(node.left, low, high) + bandSum(node.right, low, high);
    }
}
```

The count walk costs O(h + k) time and O(h) stack space. The band walk visits the crates inside the band plus at most two boundary paths, so it costs O(h + m) time for m crates in the band, with O(h) recursion.

<!-- stage: applicability -->
### When Order Or A Band Is Requested

Use these walks when a sorted tree answers rank or interval questions: the cheapest k offers in a price index, all events whose timestamps fall inside a window, or a count of users within an age band. The invariant is that the sorted visit yields keys in increasing order and every skipped branch lies entirely outside what the question can accept.

The first false friend is the level-order walk, which has no relationship with key rank: the second item of a level-order list is a child of the root, not the second smallest key. A second false friend is a whole-tree walk that filters, which is correct but gives up the pruning and returns to O(n). A third is repeated rank queries on a changing tree, where each walk costs O(h + k) and a structure that stores subtree sizes would answer faster, which this chapter does not build.

In Java, keep the countdown as a local `int` that is decremented once per pop, rather than a static field that survives from a previous query, and sum into a `long` when a band may hold many large values. Use `ArrayDeque` for the stack, since the legacy `Stack` class synchronizes every call.

<!-- stage: exercises -->
### Exercises

#### [Build] First K Inorder Values (Author exercise)
<!-- id: tb-first-k-inorder -->

**Prerequisites.** The BST invariant lesson and the explicit stack of Chapter 11.

**Problem.** The crates form a search tree of distinct weights, stored by levels, with `null` at each missing child. Given k, return the k lightest weights in increasing order, and stop the walk as soon as the kth has been produced.

**Constraints.** 1 <= k <= values.length <= 5000 and weights are integers between 1 and 100000.

**Example 1.** Input `values = [5, 3, 6, 2, 4, null, null, 1]`, `k = 3`, output `[1, 2, 3]`.

**Example 2.** Input `values = [3, null, 4, null, 5]`, `k = 2`, output `[3, 4]`.

**Hint.** After a pop, which crate comes next in weight order, and when can the loop end?

**Changed decision.** The loop is a stack walk that ends the moment the output holds k values, so crates beyond the kth are never taken from the rack.

#### [Vary] Kth Smallest Element in a BST (LeetCode 230)
<!-- id: tb-kth-smallest -->

**Prerequisites.** The First K Inorder Values rung.

**Problem.** Given a search tree of distinct keys in level order and an integer k between 1 and the number of nodes, return the kth smallest key. The walk should use a countdown that is decreased on each pop and return on the pop that reaches zero.

**Constraints.** 1 <= k <= values.length <= 10000 and keys are distinct integers between 0 and 100000.

**Example 1.** Input `values = [3, 1, 4, null, 2]`, `k = 1`, output `1`.

**Example 2.** Input `values = [5, 3, 6, 2, 4, null, null, 1]`, `k = 3`, output `3`.

**Hint.** What does the first pop of a stack walk return, and what does the stack hold afterwards?

**Changed decision.** The output list is replaced by a single countdown, and the walk returns from the middle of the loop on the pop that brings it to zero.

#### [Boundary] K At Either End (Author exercise)
<!-- id: tb-k-at-either-end -->

**Prerequisites.** The Kth Smallest rung and the mirror image of a walk.

**Problem.** For a non-empty search tree of distinct keys in level order and a rank k within range, return `[kthSmallest, kthLargest]`. The rank k = 1 gives the minimum and the maximum, and the rank k equal to the number of nodes swaps them, so the same k counted from the two ends must be checked at both extremes.

**Constraints.** 1 <= k <= values.length <= 5000 and keys are distinct integers between -100000 and 100000.

**Example 1.** Input `values = [2, 1, 3]`, `k = 1`, output `[1, 3]`.

**Example 2.** Input `values = [2, 1, 3]`, `k = 3`, output `[3, 1]`.

**Hint.** To count from the heavy end, which side is explored first, and which side is pushed on the stack?

**Changed decision.** The second walk swaps left and right everywhere, which yields descending order and leaves the countdown logic unchanged.

#### [Recognize] Range Sum of BST (LeetCode 938)
<!-- id: tb-range-sum-bst -->

**Prerequisites.** The K At Either End rung and the pruning comparison.

**Problem.** Given a search tree of distinct keys in level order and two limits `low` and `high` with low <= high, return the sum of every key that lies between them, both limits included. Branches that cannot contain a key inside the band must not be entered.

**Constraints.** 1 <= values.length <= 20000, keys are distinct integers between 1 and 100000, and 1 <= low <= high <= 100000.

**Example 1.** Input `values = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]`, `low = 5`, `high = 9`, output `35`.

**Example 2.** Input `values = [10, 5, 15, 3, 7, null, 18]`, `low = 8`, `high = 9`, output `0`.

**Hint.** If the current key is below `low`, which side of it can still hold a key in the band?

**Changed decision.** A key outside the band does not end the walk but sends it to only one side, and a key inside the band sends it to both.
