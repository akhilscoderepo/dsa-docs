<!-- lesson-kind: standard -->
<!-- lesson-id: validate-search-and-insert -->
## Validate Search And Insert

<!-- stage: context -->
### The Cloakroom With Branching Racks

A theatre cloakroom hangs its coats on racks that branch. Each rack holds one coat with a numbered ticket, and two more racks hang below it: coats with smaller tickets are always somewhere on the left side below, coats with larger tickets somewhere on the right side. The attendant hands over a ticket stub and expects her coat back within seconds, even on a night when thousands of coats are hanging.

Three jobs arrive all evening. A guest shows a stub and the attendant must find the coat, or say it is not there. A new coat comes in and must be hung in the one place where the order still holds. And sometimes a coat must be taken off a rack in the middle of the structure without leaving the others in a muddle.

<!-- stage: naive -->
### Look At Every Rack

The plain method ignores the order and treats the racks as an unsorted pile. To find a coat the attendant visits every rack in turn and compares each ticket with the stub. To add a coat she lists all tickets in order, inserts the new one in its place in the list, and then hangs the whole list on racks again from scratch.

```java
static Node findByEverything(Node rack, int stub) {
    if (rack == null) return null;
    if (rack.val == stub) return rack;
    Node inLeft = findByEverything(rack.left, stub);
    return inLeft != null ? inLeft : findByEverything(rack.right, stub);
}

static Node rehangAll(Node rack, int ticket) {
    List<Integer> all = new ArrayList<>();
    collect(rack, all);
    all.add(ticket);
    Collections.sort(all);
    return hang(all, 0, all.size() - 1);
}

static void collect(Node rack, List<Integer> out) {
    if (rack == null) return;
    collect(rack.left, out);
    out.add(rack.val);
    collect(rack.right, out);
}

static Node hang(List<Integer> sorted, int lo, int hi) {
    if (lo > hi) return null;
    int mid = (lo + hi) / 2;
    Node rack = new Node(sorted.get(mid));
    rack.left = hang(sorted, lo, mid - 1);
    rack.right = hang(sorted, mid + 1, hi);
    return rack;
}
```

The helper `collect` lists every ticket and `hang` builds a rack tree from a sorted list. Both jobs are done correctly, because the order of the tickets never matters for finding and the rebuild restores the rule.

<!-- stage: bottleneck -->
### The Order Is Never Used

A failed search has to visit all n racks before it can say the coat is missing, so each search costs O(n). Inserting by rebuilding costs O(n log n) for the sort alone and replaces every rack, which is absurd for adding a single coat. With a hundred thousand coats and a hundred thousand guests, the search work alone approaches ten billion comparisons.

All of this effort ignores a rule that was paid for when the racks were built. At any rack, one comparison between the stub and the rack's ticket already tells the attendant which entire side cannot hold the coat. Half the structure, or more, can be dropped with a single comparison, and the same comparison tells a new coat where to hang. If the tree is reasonably short, each job should cost the height h rather than n, and removing a coat should only disturb the racks right around it.

<!-- stage: insight -->
### One Comparison Drops A Whole Side

Compare the stub with the ticket on the current rack. If the stub is smaller, the coat can only be on the left, so the entire right side is thrown away unseen. If it is larger, the left side is thrown away. This is the **discard rule**, and it keeps the invariant that if the coat exists, it hangs somewhere below the current rack. A search is therefore one downward path of at most h racks, and when the path runs off the tree, the coat is not there.

That same path serves insertion. The route a missing stub would take ends at an empty place where a rack could hang, the **null slot**, and attaching the new coat there keeps the rule, because every comparison on the way down was already consistent with it. A recursive version returns the possibly new top of each branch so that the parent can re-attach it.

Removal has three cases. A coat on a leaf rack is simply dropped. A rack with one branch is replaced by that branch. A rack with two branches cannot be dropped, so the attendant takes the smallest ticket of its right side, the next ticket in order, writes it onto this rack, and then removes that smallest rack from the right side, where it has at most one branch. This is the **successor splice**.

<!-- names: discard rule, null slot, successor splice -->

The ticket moved up in a splice is larger than everything on the left and no larger than anything left on the right, so the order survives.

<!-- stage: variables -->
### Stub, Current Rack And Returned Branch

The variable `key` is the stub or the new ticket and never changes. An iterative search uses `node`, which moves down one link per comparison and becomes `null` when the stub is not present. A recursive insertion or removal returns the root of the branch it was given, and the caller stores that return value in `node.left` or `node.right`, which is how a new leaf or a spliced branch gets attached. For the removal case with two branches, `succ` is the leftmost node of the right branch, found by following `left` links until there are none. The duplicate policy is a fixed decision made before any code is written, such as rejecting an equal key.

<!-- stage: trace -->
### Finding And Hanging A Coat

The first trace searches for the stub 6 in the racks 8, 3, 10, 1, 6, null, 14 given in level order. The marker `node` sits on the rack being compared. At the rack 8 the stub is smaller so the right side with 10 and 14 is dropped without a visit, and at 3 the stub is larger so the left side with 1 is dropped. The next rack is 6, which is the coat.

```trace
{"cells":["8","3","10","1","6","null","14"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"stub":6,"rack":8},"note":"The stub 6 is smaller than the rack 8, so the right side is dropped and the walk goes left."},{"at":{"node":1},"vars":{"stub":6,"rack":3},"note":"The stub 6 is larger than the rack 3, so the left side is dropped and the walk goes right."},{"at":{"node":4},"vars":{"stub":6,"rack":6},"note":"The rack 6 equals the stub 6, so the coat is found."}]}
```

The second trace hangs the new ticket 5 on the same racks. The cells are written in complete-tree positions, so the empty places below 1 and 6 appear as extra cells at the end, and the pointer `node` can rest on an empty place. The path is the same as the search for a missing stub: 8, then 3, then 6, and then the empty place to the left of 6, which is where the new coat is attached.

```trace
{"cells":["8","3","10","1","6","null","14","null","null","null","null"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"stub":5,"rack":8},"note":"The stub 5 is smaller than the rack 8, so the right side is dropped and the walk goes left."},{"at":{"node":1},"vars":{"stub":5,"rack":3},"note":"The stub 5 is larger than the rack 3, so the left side is dropped and the walk goes right."},{"at":{"node":4},"vars":{"stub":5,"rack":6},"note":"The stub 5 is smaller than the rack 6, so the right side is dropped and the walk goes left."},{"at":{"node":9},"vars":{"stub":5,"rack":"empty"},"note":"The place to the left of 6 is empty, so the new coat 5 is attached here and nothing else moves."}]}
```

<!-- stage: code -->
### Search, Insert And Remove

```java
final class RackOps {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node search(Node root, int key) {
        Node node = root;
        while (node != null && node.val != key) {
            node = key < node.val ? node.left : node.right;
        }
        return node;
    }

    static Node insert(Node node, int key) {
        if (node == null) return new Node(key);
        if (key < node.val) node.left = insert(node.left, key);
        else if (key > node.val) node.right = insert(node.right, key);
        return node;
    }

    static Node remove(Node node, int key) {
        if (node == null) return null;
        if (key < node.val) { node.left = remove(node.left, key); return node; }
        if (key > node.val) { node.right = remove(node.right, key); return node; }
        if (node.left == null) return node.right;
        if (node.right == null) return node.left;
        Node succ = node.right;
        while (succ.left != null) succ = succ.left;
        node.val = succ.val;
        node.right = remove(node.right, succ.val);
        return node;
    }
}
```

Each operation follows one downward path and does constant work per rack, so the time is O(h), which is O(n) for a chain and O(log n) for a well-shaped tree. The recursive forms use O(h) stack and the search uses O(1).

<!-- stage: applicability -->
### When The Key Decides The Direction

Use a single path whenever the structure is ordered and the question is about one key: a lookup in an index of customer numbers, adding a record to a sorted tree, or deleting a retired id. The invariant is that if the key is present under the stated contract, it lies in the one subtree that the last comparison selected.

The first false friend is validation, which looks like a search but needs a different state. A search can trust the ordering and follow one path, while validation must test an ordering nobody has verified, so it needs bounds and has to visit every node. A second false friend is assuming that the search path is short. The path is bounded by the height, and a tree built from sorted keys is a chain on which every job costs O(n). A third is forgetting to store the return value of the recursive calls, which silently loses an inserted leaf or a spliced branch.

In Java, state the policy for equal keys before coding. With the policy to reject duplicates, equality falls through every comparison and returns the node unchanged, but a policy that counts or places equals needs an explicit branch for equality.

<!-- stage: exercises -->
### Exercises

#### [Build] Search in a Binary Search Tree (LeetCode 700)
<!-- id: tb-bst-search -->

**Prerequisites.** The BST invariant and bounds lesson.

**Problem.** The racks form a search tree of distinct keys, listed in level order with `null` for absent children. Given a `key`, find the node holding it and return the subtree rooted there as a level-order array, or an empty array when no node holds the key.

**Constraints.** 0 <= values.length <= 5000 and the keys, including the stub, are distinct integers between 1 and 10000.

**Example 1.** Input `values = [4, 2, 7, 1, 3]`, `key = 2`, output `[2, 1, 3]`.

**Example 2.** Input `values = [4, 2, 7, 1, 3]`, `key = 5`, output `[]`.

**Hint.** After one comparison with the current key, which side can no longer contain the stub?

**Changed decision.** The walk follows exactly one child per comparison and stops at a match or at null, with no visit to the discarded side.

#### [Vary] Insert into a Binary Search Tree (LeetCode 701)
<!-- id: tb-bst-insert -->

**Prerequisites.** The Search rung and the downward path.

**Problem.** Given a binary search tree with distinct keys in level order and a `key` that is not yet present, attach the key as a new leaf at the empty place where its search path ends. Return the level-order array of the resulting tree, with trailing `null` entries removed.

**Constraints.** 0 <= values.length <= 5000, keys are distinct integers between -100000 and 100000, and the new key differs from all of them.

**Example 1.** Input `values = [4, 2, 7, 1, 3]`, `key = 5`, output `[4, 2, 7, 1, 3, 5]`.

**Example 2.** Input `values = [3, null, 5]`, `key = 4`, output `[3, null, 5, 4]`.

**Hint.** When the walk reaches a null child, what should the caller store in its link?

**Changed decision.** The walk is the same as in the search, but it ends by returning a new node to be stored in the parent's link, so existing nodes are never moved.

#### [Boundary] Duplicate-Key Policy (Author exercise)
<!-- id: tb-duplicate-key-policy -->

**Prerequisites.** The Insert rung and the equality branch of a comparison.

**Problem.** Insert the given `keys` one by one into an empty tree under a named policy. Under `reject` an equal key is ignored, under `count` an equal key adds one to a counter stored on the existing node, and under `right` an equal key becomes a new node on the right side of the equal node. Return `[nodes, height, sortedKeys]`, where height counts nodes along the longest downward route and `sortedKeys` lists every stored key in order, repeated by its counter.

**Constraints.** 0 <= keys.length <= 300, keys are integers between 0 and 20, and the policy is one of the three words.

**Example 1.** Input `keys = [5, 3, 5, 8]`, `policy = count`, output `[3, 2, [3, 5, 5, 8]]`.

**Example 2.** Input `keys = [2, 2, 2]`, `policy = right`, output `[3, 3, [2, 2, 2]]`.

**Hint.** What does the comparison do when the two keys are equal, and does that branch need to exist for every policy?

**Changed decision.** Equality gets its own branch whose action depends on the policy, and the choice changes the node count and the height even when the sorted keys agree.

#### [Recognize] Delete Node in a BST (LeetCode 450)
<!-- id: tb-delete-node -->

**Prerequisites.** The Duplicate-Key Policy rung and the three removal cases.

**Problem.** Given a binary search tree with distinct keys in level order and a `key`, remove the node holding that key if there is one. A node with two children takes the value of the smallest node on its right side, which is then removed from there. Return the level-order array of the result, with trailing `null` entries removed.

**Constraints.** 0 <= values.length <= 5000 and keys, including the target, are distinct integers between -100000 and 100000.

**Example 1.** Input `values = [5, 3, 6, 2, 4, null, 7]`, `key = 3`, output `[5, 4, 6, 2, null, null, 7]`.

**Example 2.** Input `values = [5, 3, 6, 2, 4, null, 7]`, `key = 5`, output `[6, 3, 7, 2, 4]`.

**Hint.** Which node on the right side can take the removed key's place without breaking order, and what does removing it from there cost?

**Changed decision.** A node with two children is not removed but overwritten by its successor, and the removal is then repeated for the successor's old node, which has at most one child.
