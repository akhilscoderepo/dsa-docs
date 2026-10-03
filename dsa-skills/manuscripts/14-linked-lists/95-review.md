<!-- section: review -->
## Review

Return to this section after the lessons and again after a few days. The scenarios avoid naming the method, so decide which references you hold, which link you are about to change, and which node would be lost, before you read the options. These questions test prediction and recognition, which guided exercises cannot.

### Recognition Questions

```quiz
{"id":"ll-rev-lost-tail","q":"To insert a new node after a given node, which order of assignments keeps the old successor reachable?","options":["Point the given node at the new node, then the new node at the old successor.","Save the old successor, point the new node at it, then point the given node at the new node.","Point the new node at null first.","Either order works."],"answer":1,"explain":"The old successor must be held by a reference at every moment, and only the saved copy or the new node's link can hold it once the given node is rewired."}
```

```quiz
{"id":"ll-rev-reverse-save","q":"In the reversal loop, why is the successor of the current node saved before its link is redirected?","options":["To make the loop shorter.","The redirect overwrites the only link to the rest of the list.","To count the nodes.","The successor is needed for the return value."],"answer":1,"explain":"After the redirect, the current node no longer leads to the untouched suffix, so a saved reference is the only way to continue."}
```

```quiz
{"id":"ll-rev-lookahead","q":"Why does a k-group reversal look ahead k nodes before changing any link?","options":["To find the middle.","So a short final group is detected while the list is still untouched.","To reverse faster.","To allocate a dummy."],"answer":1,"explain":"Flipping first and discovering a short group later would require flipping it back, and a look-ahead avoids that without changing any link."}
```

```quiz
{"id":"ll-rev-merge-tail","q":"When one of two sorted lists runs out during a merge, what finishes the job?","options":["A comparison for each remaining node.","One assignment that attaches the whole remaining list.","Sorting the remaining nodes.","Copying the values into an array."],"answer":1,"explain":"The remaining list is already sorted and no smaller than anything placed, so it can be attached as it is."}
```

```quiz
{"id":"ll-rev-dummy","q":"What does a dummy head remove from list code?","options":["The need for a tail.","The special case of changing the first real node.","The need to return a value.","Null checks on every node."],"answer":1,"explain":"With a dummy, the first real node has a predecessor like every other node, so inserting or removing it uses the same line as elsewhere."}
```

```quiz
{"id":"ll-rev-cycle-values","q":"Two nodes of a list hold the same value. What does that say about a cycle?","options":["There is a cycle.","Nothing, because a cycle is about node identity.","There is no cycle.","The list is a palindrome."],"answer":1,"explain":"A cycle means that following references returns to the same node object, and equal values on different nodes do not."}
```

```quiz
{"id":"ll-rev-entry","q":"After the slow and fast pointers meet inside a cycle, how is the start of the cycle found?","options":["Stop at the meeting point.","Place a pointer at the head and move it and the slow pointer one step at a time until they meet.","Move fast one more lap.","Reverse the list."],"answer":1,"explain":"The distance from the head to the entry equals the distance from the meeting point to the entry, going forward around the cycle, up to whole laps."}
```

```quiz
{"id":"ll-rev-head-switch","q":"Why do the two pointers of the head-switching walk meet at the first shared node?","options":["They walk at different speeds.","Each walks the same total distance, its own list plus the other list's private part.","They compare values.","They start at the tails."],"answer":1,"explain":"The totals p + s + q and q + s + p are equal, so the pointers stand on the same node in the same round."}
```

```quiz
{"id":"ll-rev-middle-even","q":"For a list of even length, which middle does the loop 'while fast and fast.next are non-null' return?","options":["The first middle.","The second middle.","The head.","The tail."],"answer":1,"explain":"Fast becomes null after k rounds on a list of 2k nodes, and slow is then on the node with index k, which is the later middle."}
```

```quiz
{"id":"ll-rev-gap","q":"A lead pointer advances k nodes, then both pointers move together. What does the trailing pointer hold when the lead becomes null?","options":["The middle node.","The k-th node from the end.","The head.","The predecessor of the head."],"answer":1,"explain":"The gap stays k, and the lead is one past the last node, so the trailing pointer is k nodes before that position."}
```

```quiz
{"id":"ll-rev-flatten-links","q":"Why must a flatten of a multilevel doubly linked list repair prev links as well as next links?","options":["Because next links are optional.","A list with only next links repaired plays correctly forward and breaks when walked backward.","Because prev links are faster.","Because the child pointer needs it."],"answer":1,"explain":"The structure is only valid when each pair of neighbours agrees in both directions, and a one-directional test cannot reveal the break."}
```

```quiz
{"id":"ll-rev-clone-first","q":"In a deep copy with random pointers, why are all clones created before any link is written?","options":["To save memory.","So that every lookup finds a clone, whatever the position of the target.","To avoid null checks.","Because clones cannot have links."],"answer":1,"explain":"A random target may come later in the list, and its clone must already exist when the link is written."}
```

```quiz
{"id":"ll-rev-map-key","q":"Why is the identity map keyed by the node object and not by the node's value?","options":["Objects hash faster.","Different nodes can hold equal values, and a value key would merge their entries.","Values cannot be keys.","The values are always distinct."],"answer":1,"explain":"Equal values on different nodes collapse into one key and send links to the wrong clone."}
```
