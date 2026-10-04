<!-- section: review -->
## Review

Return to this section after the lessons and again after a few days. The scenarios do not name the technique, so decide what the queue, stack or interval holds before looking at the options. These questions test prediction, which the guided exercises do not.

### Recognition Questions

```quiz
{"id": "tb-rev-queue-size", "q": "A level walk reads queue.size() once before each wave. What goes wrong if the loop condition reads it afresh at every step?", "options": ["Nothing, the loop ends at the same place.", "Children added during the wave are counted, so waves run together.", "The queue becomes empty too early.", "The tree is visited in postorder."], "answer": 1, "explain": "The live size grows whenever a child is added, so the loop never stops at the end of the wave and the groups are no longer separated by depth."}
```

```quiz
{"id": "tb-rev-local-check", "q": "Every node of a tree is correctly ordered against its own parent. What can still be wrong?", "options": ["Nothing, the tree is a search tree.", "A node may break the order of an ancestor higher up.", "The tree may contain null children.", "The root may have a duplicate."], "answer": 1, "explain": "A search tree orders each node against every ancestor, so a node in the right side of the root must exceed the root even if it fits its parent."}
```

```quiz
{"id": "tb-rev-insert-place", "q": "Where does a new key attach in a plain search tree that rejects duplicates?", "options": ["At the root, pushing the old root down.", "As a new leaf at the empty place where the search for the key ends.", "In the middle of the tree, at the median.", "At the deepest node on the left."], "answer": 1, "explain": "The failed search path ends at an empty child link, and attaching a leaf there keeps every comparison on the path consistent."}
```

```quiz
{"id": "tb-rev-successor", "q": "A node has no right subtree and is the right child of its parent. Where is its inorder successor?", "options": ["Its parent.", "Its left child.", "The nearest ancestor reached by turning left on the way down.", "The smallest key in the tree."], "answer": 2, "explain": "Ancestors on whose right the node lies are smaller, so the answer is the lowest ancestor whose left side contains the node, if there is one."}
```

```quiz
{"id": "tb-rev-band-prune", "q": "While summing keys between low and high, the walk reaches a key smaller than low. Which side can still hold keys in the band?", "options": ["Only the left side.", "Only the right side.", "Both sides.", "Neither side."], "answer": 1, "explain": "Everything on the left of a key is smaller still, so only the right side can reach the band."}
```

```quiz
{"id": "tb-rev-lca-order", "q": "Which statement about the lowest common ancestor shortcut that steers by key is true?", "options": ["It works on any binary tree.", "It works only when the tree promises the left-smaller, right-larger order.", "It works only on complete trees.", "It needs parent links."], "answer": 1, "explain": "Comparing numbers says which way both targets lie only when the numbers carry positional meaning, as in a search tree."}
```

```quiz
{"id": "tb-rev-iterator-cost", "q": "A search tree iterator keeps a stack of the left spine. What is the cost of n calls to next over the whole tree?", "options": ["O(n) in total, since each node is pushed and popped once.", "O(n h) in total.", "O(n log n) in total.", "O(h) in total."], "answer": 0, "explain": "A single call may push a whole spine, but every node enters and leaves the stack once, so the total is linear and the average per call is constant."}
```

```quiz
{"id": "tb-rev-null-markers", "q": "Why does a preorder text of a tree need markers for empty children?", "options": ["To make the text shorter.", "Different shapes can have the same list of values, and markers record where each branch ends.", "To sort the values.", "Because Java cannot split text otherwise."], "answer": 1, "explain": "Without markers the reader cannot tell which values belong to the left side, so the shape is lost."}
```

```quiz
{"id": "tb-rev-rotation", "q": "What does a rotation leave unchanged?", "options": ["The height of every subtree.", "The inorder listing of the keys.", "The root of the tree.", "The number of leaves."], "answer": 1, "explain": "A rotation rewrites three links and moves one subtree between the two nodes, and the left-to-right order of the keys is untouched."}
```

```quiz
{"id": "tb-rev-direction-rule", "q": "To read every other wave right to left, what must stay unchanged?", "options": ["The order in which children are queued.", "The size snapshot.", "The list type.", "Nothing needs to stay."], "answer": 0, "explain": "Children must still be queued left to right, or the next wave would be discovered in the wrong order. Only the placement within the wave's own list changes."}
```

```quiz
{"id": "tb-rev-neighbours", "q": "A search for a key that is not in the tree stops at an empty place. What are the interval ends the walk carried?", "options": ["The smallest and largest keys in the tree.", "The next lower and next higher keys in sorted order.", "The root and the last node visited.", "Always null and null."], "answer": 1, "explain": "No key can lie inside the final interval, so its ends are the keys adjacent to the missing key in sorted order."}
```
