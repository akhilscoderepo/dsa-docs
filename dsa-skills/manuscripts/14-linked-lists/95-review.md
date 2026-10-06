<!-- section: review -->
## Review

Come back to this page after the lessons and again a few days later. Each question describes a situation and leaves out the lesson name. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "ll-rev-self-link", "q": "A method runs `node.next = newNode;` and then `newNode.next = node.next;`. What does `newNode.next` hold afterwards?", "options": ["The old successor of node", "newNode itself", "null", "node"], "answer": 1, "explain": "The first statement already replaced node.next with newNode, so the second statement copies newNode into newNode.next. The old successor lost its only link."}
```

```quiz
{"id": "ll-rev-save-first", "q": "In the loop that reverses a list, which statement must run before `curr.next = prev`?", "options": ["prev = curr", "saved = curr.next", "curr = saved", "return prev"], "answer": 1, "explain": "The assignment curr.next = prev overwrites the only link to the rest of the list. The copy in saved keeps the rest reachable."}
```

```quiz
{"id": "ll-rev-short-group", "q": "A list has 7 nodes, and it is reversed in groups of 3 with a short final group left alone. What happens to the 7th node?", "options": ["It stays in place", "It joins the second group", "It moves to the front", "It is removed"], "answer": 0, "explain": "The groups are nodes 1 to 3 and nodes 4 to 6. The look-ahead from node 7 finds one node, which is fewer than 3, so no write happens."}
```

```quiz
{"id": "ll-rev-tie-merge", "q": "Two sorted lists start with equal values. The merge takes the node of the second list only when `b.val < a.val`. Which node goes first?", "options": ["The node of the second list", "The node of the first list", "Whichever has the longer list", "Neither, because they are equal"], "answer": 1, "explain": "For equal values the test b.val < a.val is false, so the merge takes the node of the first list. That keeps equal values in input order."}
```

```quiz
{"id": "ll-rev-return-head", "q": "A method removes matching nodes behind a dummy node but returns `head` instead of `dummy.next`. When does the caller get a wrong list?", "options": ["When the first node is removed", "When the last node is removed", "When no node matches", "When the list is long"], "answer": 0, "explain": "The variable head still points at the removed node, so the caller receives a list that starts with a node that should be gone. dummy.next is always the current head."}
```

```quiz
{"id": "ll-rev-equal-values", "q": "A list holds the values 5, 5, 5 and its last node points at null. Does the list have a cycle?", "options": ["Yes, because the values repeat", "No, because a cycle needs a node that is reached twice", "Yes, because slow and fast hold equal values", "Only when the length is odd"], "answer": 1, "explain": "A cycle is a repeated node, not a repeated value. The fast reference reaches null, so the loop ends with no cycle."}
```

```quiz
{"id": "ll-rev-length-difference", "q": "Two lists have 5 and 3 nodes and share their last 2 nodes. By how many nodes must the longer list's reference start ahead in the length method?", "options": ["1", "2", "3", "5"], "answer": 1, "explain": "The difference of the lengths is 5 - 3 = 2. After that advance both references are the same distance from the end, so the first equal pair is the first shared node."}
```

```quiz
{"id": "ll-rev-middle-index", "q": "A list has 6 nodes, and the loop runs while `fast != null && fast.next != null`. On which index does `slow` stop?", "options": ["Index 2", "Index 3", "Index 4", "Index 5"], "answer": 1, "explain": "The loop makes 3 turns, so slow is at index 3, the second of the two middle nodes."}
```

```quiz
{"id": "ll-rev-gap-moves", "q": "The leading reference moves k = 3 nodes from the head of a list that has exactly 3 nodes. How many moves does the second loop make?", "options": ["0", "1", "2", "3"], "answer": 0, "explain": "After 3 moves the leading reference is null, so the second loop never runs. The trailing reference stays on the head, which is the 3rd node from the end."}
```

```quiz
{"id": "ll-rev-up-arrow", "q": "After a splice, a list reads correctly from the head along `next`, and walking backward from the last node skips a whole child chain. Which writes were probably missing?", "options": ["The prev writes at the two boundaries", "The writes that clear the child field", "The walk to the child tail", "The copy of the values"], "answer": 0, "explain": "Each boundary needs a next write and a prev write. A list with correct next links and stale prev links works in one direction only."}
```

```quiz
{"id": "ll-rev-two-passes", "q": "Why does the copy method create every new node in a first pass before it sets any random link?", "options": ["A random link can point at a node that has no copy yet", "The map needs the nodes sorted", "The next links need two reads", "A single pass cannot read null"], "answer": 0, "explain": "A random link may point forward. If the copies were created while wiring, a lookup of a later node would find nothing."}
```

### Recall Exercises

Close this page and answer from memory, then check against the lessons. Write the four statements of one reversal turn in order, and say which one protects the rest of the list. Explain in two sentences why a dummy node makes the removal of the first node follow the same rule as every other node. State what the slow and fast references hold when a list of 6 nodes ends the middle search, and say which loop test gives the first middle. Describe the four writes of one child-chain splice, and name the one write that is skipped when the parent is the last node.
