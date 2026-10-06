<!-- section: review -->
## Review

Come back to this page after the lessons and again a few days later. Each question describes a situation and leaves out the lesson name. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "tb-rev-size-inside", "q": "A row loop uses `for (int i = 0; i < queue.size(); i++)` and adds the children of each removed node to the same queue. A root has two children. What does the first pass do?", "options": ["It removes only the root", "It removes the root and then both children", "It removes the root and one child", "It throws an exception"], "answer": 1, "explain": "A removal shrinks the queue by one and two additions grow it by two, so the test reads 2 after the first removal. The loop removes both children, and the first row mixes two depths."}
```

```quiz
{"id": "tb-rev-null-child", "q": "A row loop adds both children of every node to an `ArrayDeque` and skips the null check. What happens at the first leaf?", "options": ["The leaf is skipped", "A NullPointerException is thrown", "The loop ends quietly", "A null entry is stored and later ignored"], "answer": 1, "explain": "ArrayDeque rejects null elements, so the add call for a missing child throws. Each child needs a null check before it enters the queue."}
```

```quiz
{"id": "tb-rev-deep-violation", "q": "Every node of a tree is larger than its left child and smaller than its right child. Can the tree still fail to be a search tree?", "options": ["No, the two comparisons prove it", "Yes, a deep node can break a limit set by a distant ancestor", "Only if keys repeat", "Only if the tree is empty"], "answer": 1, "explain": "A node must respect every ancestor, not only its parent. A small key under the right child of the root violates the root even when it is smaller than its own parent."}
```

```quiz
{"id": "tb-rev-int-limit", "q": "A validity check starts with the limits `Integer.MIN_VALUE` and `Integer.MAX_VALUE` as `int` values and uses strict comparisons. Which tree does it wrongly reject?", "options": ["A tree whose root key is Integer.MAX_VALUE", "A tree with three nodes", "A tree with negative keys", "An empty tree"], "answer": 0, "explain": "A strict comparison with an upper limit equal to the key rejects it. Limits stored as long lie outside the int range, so every int key passes the first test."}
```

```quiz
{"id": "tb-rev-search-branch", "q": "A search for the key 12 reaches a node with the key 20. What may the search ignore?", "options": ["The left subtree of the node", "The right subtree of the node", "The parent of the node", "Nothing, because both sides may hold 12"], "answer": 1, "explain": "The key 12 is smaller than 20, and every key in the right subtree is larger than 20. The right subtree cannot hold 12."}
```

```quiz
{"id": "tb-rev-parent-successor", "q": "The key 7 is a leaf and its parent holds 6. What is the successor of 7 in the tree?", "options": ["6, the parent", "The nearest ancestor from which the path turned left", "The root", "There is none"], "answer": 1, "explain": "The parent holds a smaller key, so it cannot be the successor. The successor is the nearest ancestor that is larger than 7, which is the last node where the path turned left."}
```

```quiz
{"id": "tb-rev-range-prune", "q": "A range sum with limits 35 and 65 reaches a node with the key 30. Which subtree can the walk skip?", "options": ["The right subtree", "The left subtree", "Both subtrees", "Neither subtree"], "answer": 1, "explain": "The key 30 is below the low limit, so every key in its left subtree is smaller still. The walk skips that side and continues to the right child."}
```

```quiz
{"id": "tb-rev-bst-lca-shortcut", "q": "Which tree makes the key-comparison shortcut for the lowest common ancestor give a wrong answer?", "options": ["A search tree with distinct keys", "A binary tree whose keys are in no particular order", "A tree with one node", "A tree that is a chain with increasing keys"], "answer": 1, "explain": "The shortcut relies on the ordering to say which side holds both targets. In an unordered tree a comparison of keys says nothing about the side."}
```

```quiz
{"id": "tb-rev-iterator-cost", "q": "An iterator pushes the left spine of a right child after each pop. What is the cost of one call to next, averaged over all calls of a full run?", "options": ["O(n)", "O(h)", "O(1)", "O(log n) in every case"], "answer": 2, "explain": "Each node is pushed once and popped once during the run, so the total work is at most twice the node count. The average per call is a constant, although a single call can cost O(h)."}
```

```quiz
{"id": "tb-rev-marker-count", "q": "A binary tree has 6 nodes. How many tokens does the preorder text with null markers hold?", "options": ["6", "7", "12", "13"], "answer": 3, "explain": "A tree with n nodes has n + 1 empty slots, and each node and each empty slot writes one token. For n = 6 that gives 6 + 7 = 13 tokens."}
```

```quiz
{"id": "tb-rev-rotation-order", "q": "A right rotation lifts the left child of a node above that node. What happens to the sorted order of all keys?", "options": ["It reverses", "It stays the same", "The lifted key moves to the front", "It changes only for the lifted subtree"], "answer": 1, "explain": "The subtree that changes its parent still lies between the same two keys. Only the shape and heights change, and the sorted order stays the same."}
```

```quiz
{"id": "tb-rev-balanced-meaning", "q": "A height-balanced tree is the same thing as which kind of tree?", "options": ["A complete tree", "A perfectly symmetric tree", "Neither, because it only limits the height difference at each node", "A tree with equal numbers of left and right nodes"], "answer": 2, "explain": "The rule only keeps the heights of two subtrees within 1 of each other. A balanced tree can have different shapes on its two sides."}
```

```quiz
{"id": "tb-rev-depth-recursion", "q": "A row printer passes the depth down a recursive walk. It works on every sample and then crashes on one input. Which input is most likely?", "options": ["A tree with duplicate values", "A very tall chain of nodes", "A tree with negative values", "A tree with a single node"], "answer": 1, "explain": "Each level of the walk keeps a frame on the call stack. A chain with hundreds of thousands of levels fills the stack and throws a StackOverflowError, while a queue loop keeps its nodes on the heap."}
```

```quiz
{"id": "tb-rev-slot-interval", "q": "A key lies outside the open interval of the slot where its node hangs. What does a lookup for that key from the root do?", "options": ["It finds the node", "It ends at a different place and never reaches that node", "It loops forever", "It finds the node but takes longer"], "answer": 1, "explain": "The comparisons of a lookup lead to the slot whose interval contains the key. A node outside its own interval sits in the wrong slot, so the lookup ends somewhere else."}
```
