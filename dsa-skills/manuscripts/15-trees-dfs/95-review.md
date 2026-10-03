<!-- section: review -->
## Review

Come back to this section when the lessons are finished and again after a few days. The scenarios do not name the technique, so decide what each call receives and what it hands back before you look at the options. These questions test prediction and recognition, which the guided exercises do not.

### Recognition Questions

```quiz
{"id": "tr-rev-null-subtree", "q": "A recursive method receives a null child. What is the safest design?", "options": ["Check for null before every recursive call and skip it.", "Let the base case answer for null, so every other call can assume its node exists.", "Catch the NullPointerException.", "Store a placeholder node with value zero."], "answer": 1, "explain": "Treating null as a valid empty subtree with a defined answer removes all other null checks from the recursive step."}
```

```quiz
{"id": "tr-rev-position", "q": "Where must the append sit among the two child calls to get the sorted order of a binary search tree?", "options": ["Before both calls.", "Between the two calls.", "After both calls.", "The position does not matter."], "answer": 1, "explain": "Appending between the calls writes the whole left block, then the node, then the whole right block."}
```

```quiz
{"id": "tr-rev-push-order", "q": "A stack walk must visit the left subtree first. In what order are the children pushed?", "options": ["Left child, then right child.", "Right child, then left child.", "Either order, since both get visited.", "Neither, because the root is pushed last."], "answer": 1, "explain": "The last child pushed is the first one popped, so the left child has to be pushed last."}
```

```quiz
{"id": "tr-rev-overflow", "q": "A tree with one hundred thousand nodes is a single chain. Which walk is at risk of StackOverflowError?", "options": ["A walk driven by an explicit ArrayDeque.", "A recursive walk.", "A loop over the level-order array.", "Neither one."], "answer": 1, "explain": "Recursion depth equals the height, which is the full length of the chain here."}
```

```quiz
{"id": "tr-rev-restore", "q": "A shared route list is extended before the two child calls. What must the call do before it returns?", "options": ["Clear the whole list.", "Remove its own entry, so the list is back as it was found.", "Copy the list.", "Nothing, since the parent will clean up."], "answer": 1, "explain": "The call leaves shared state exactly as it found it, which keeps every route correct for the calls that follow."}
```

```quiz
{"id": "tr-rev-return-branch", "q": "In a longest-path question, why does a node return only one branch height to its parent?", "options": ["To save memory.", "The parent can only continue a path through one of the branches.", "Two branches are larger.", "The other branch is always shorter."], "answer": 1, "explain": "A path that already uses both branches of a node cannot be extended by the parent without visiting the node twice."}
```

```quiz
{"id": "tr-rev-sentinel", "q": "Heights are counted in edges, so an empty subtree has height -1. Which failure value stays safe?", "options": ["-1.", "0.", "-2.", "1."], "answer": 2, "explain": "The failure value must lie outside every valid result, and -1 is already a valid height of an empty subtree."}
```

```quiz
{"id": "tr-rev-two-orders", "q": "Which pair of sequences identifies a binary tree with distinct labels?", "options": ["Preorder alone.", "Preorder and postorder.", "Preorder and inorder.", "Inorder alone."], "answer": 2, "explain": "Preorder names each root, and the root's position in inorder splits the labels into the left and right subtrees."}
```

```quiz
{"id": "tr-rev-morris", "q": "In a Morris walk, what does the predecessor's right link equal on the second arrival at a node?", "options": ["Null.", "The node itself.", "The left child.", "The parent's right child."], "answer": 1, "explain": "The link was set to the current node on the first arrival, which is how the second arrival is recognised before the link is cut."}
```

```quiz
{"id": "tr-rev-quad", "q": "When does a quadtree builder create an internal node?", "options": ["For every block of side greater than one.", "Only for a block whose cells are not all equal.", "For every block that has four neighbours.", "Never, since leaves are enough."], "answer": 1, "explain": "A uniform block of any size is a single leaf, so division happens only when the cells disagree."}
```

```quiz
{"id": "tr-rev-state-answer", "q": "A walk returns a local result that uses both branches as its state instead of one branch. What goes wrong?", "options": ["The time becomes quadratic.", "A parent extends a result that already forks, so the answer describes no real path.", "The recursion never ends.", "Nothing, the answers agree."], "answer": 1, "explain": "The return state must be something a parent can extend, and a two-branch chain cannot be extended."}
```
