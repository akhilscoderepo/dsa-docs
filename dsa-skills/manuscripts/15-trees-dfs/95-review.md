<!-- section: review -->
## Review

Come back to this page after the lessons and again a few days later. Each question describes a situation and leaves out the lesson name. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "tr-rev-shared-child", "q": "A tree node object is reached from two different parents. A recursive count of nodes starts at the root. How many times does the count include that node?", "options": ["Once", "Never", "Once per child it has", "Twice"], "answer": 3, "explain": "Each parent makes its own call on the node, and nothing records that the node was seen. The tree contract promises one parent per node, and a shared node breaks that promise."}
```

```quiz
{"id": "tr-rev-delete-order", "q": "A walk deletes a folder node. The operating system refuses to remove a folder that still has entries inside. Where does the delete action sit relative to the calls on the two children?", "options": ["After both calls", "Before both calls", "Between the two calls", "Inside the check for an empty node"], "answer": 0, "explain": "Every entry below the folder must be gone first, so the action runs after both child calls. That position gives postorder."}
```

```quiz
{"id": "tr-rev-push-order", "q": "An iterative preorder walk pushes the left child first and then the right child. For a root 1 with the leaf children 2 and 3, which values does it write?", "options": ["1, 2, 3", "2, 3, 1", "1, 3, 2", "3, 2, 1"], "answer": 2, "explain": "The stack returns the most recent push first, so the right child is popped before the left child. To visit the left child first, push the right child first."}
```

```quiz
{"id": "tr-rev-route-undo", "q": "A walk keeps one shared list of the values on the current route and adds the node before it calls the two children. What must the call do after both child calls return?", "options": ["Nothing, because each call copies the list", "Remove the last entry", "Clear the whole list", "Add the node again"], "answer": 1, "explain": "All calls share one list object. The call must undo its own addition, or the siblings and later nodes see values from routes that they are not on."}
```

```quiz
{"id": "tr-rev-branch-return", "q": "At a node the left subtree has height 3 and the right subtree has height 2, counted in nodes. How many edges does the longest path through this node have, and what does the call return to its parent as a height?", "options": ["5 edges and the height 5", "5 edges and the height 4", "4 edges and the height 5", "4 edges and the height 4"], "answer": 1, "explain": "The path joins both sides, so it has 3 + 2 = 5 edges. The parent can continue only one side, so the call returns one plus the larger height, which is 4."}
```

```quiz
{"id": "tr-rev-marker-clash", "q": "A balance check counts heights in edges, so the empty tree has height -1. The same method uses -1 as the failure marker. What goes wrong?", "options": ["An empty subtree looks like a failure", "Nothing goes wrong", "The root can never fail", "The heights overflow"], "answer": 0, "explain": "A real height of -1 and the failure marker are the same number. The caller cannot tell an empty side from a failed side, so the marker must lie outside the range of real heights."}
```

```quiz
{"id": "tr-rev-left-size", "q": "The preorder list is 1, 2 and the inorder list is 1, 2. For the tree they describe, how many nodes are in the left subtree of the root?", "options": ["Two", "One", "It cannot be told", "Zero"], "answer": 3, "explain": "The root 1 is the first value of the preorder list. It sits at position 0 of the inorder list, so no value lies before it and the left subtree is empty. The node 2 is the right child."}
```

```quiz
{"id": "tr-rev-thread-left", "q": "A walk that borrows empty right references stops after it writes its first k values and does not finish. What does the tree hold afterward?", "options": ["The same references as before", "Values in sorted order", "Some right references that point to ancestors", "Only null left references"], "answer": 2, "explain": "A temporary link is removed only on the second arrival at its node. Stopping early leaves the links in place, and the tree then contains a cycle."}
```

```quiz
{"id": "tr-rev-blank-grid", "q": "A grid of 4 by 4 cells holds the same value in all 16 cells. A quadtree builder tests whether the square is uniform before it cuts. How many nodes does the tree have?", "options": ["21", "5", "1", "16"], "answer": 2, "explain": "The whole square is uniform, so the first call returns one leaf and never cuts. Cutting first would create 1 + 4 + 16 = 21 nodes."}
```

```quiz
{"id": "tr-rev-last-written", "q": "An iterative postorder walk finds a node on top of the stack whose right child is the node it wrote most recently. What does it do with the top node?", "options": ["Writes it and pops it", "Enters the right child again", "Pushes its left spine", "Skips it"], "answer": 0, "explain": "The right side is already written, and the left side was written before it. Both sides are done, so the node is written next."}
```

```quiz
{"id": "tr-rev-fork-return", "q": "A call returns the best path that uses both of its sides to its parent, and not the best single branch. What does the parent do wrong?", "options": ["It reads the wrong child", "It extends a path that already uses both sides", "It counts a leaf twice", "It skips the failure marker"], "answer": 1, "explain": "A path that uses two branches at a node cannot continue upward without forking. The parent would join one more branch to a shape that is no longer a single path."}
```
