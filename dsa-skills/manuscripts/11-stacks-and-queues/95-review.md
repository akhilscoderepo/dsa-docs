<!-- section: review -->
## Review

Return to this section after the lessons and again after a few days. The scenarios do not name a structure, so decide what is stored and which end acts before you open the options. These questions test recall and recognition, which guided exercises cannot.

### Recognition Questions

```quiz
{"id":"sq-rev-deque-ends","q":"A program uses addLast to insert and removeLast to remove. What structure is it?","options":["A queue.","A stack.","A sorted list.","A set."],"answer":1,"explain":"Insertion and removal share one end, so the newest element leaves first, which is last in first out."}
```

```quiz
{"id":"sq-rev-null","q":"Why can an ArrayDeque not use null to separate batches?","options":["It would be slow.","ArrayDeque throws NullPointerException on null elements.","null is converted to zero.","The batch would be skipped."],"answer":1,"explain":"The class refuses null so that a null result from a polling method can only mean empty, which also rules out a null marker."}
```

```quiz
{"id":"sq-rev-poll-remove","q":"On an empty ArrayDeque, which pair of calls returns null and throws, in that order?","options":["removeFirst and pollFirst","pollFirst and removeFirst","peekFirst and pollFirst","getFirst and removeFirst"],"answer":1,"explain":"The polling family returns null on empty, while the throwing family raises NoSuchElementException."}
```

```quiz
{"id":"sq-rev-stuck-line","q":"In a queue where the front item is moved to the back when it cannot be served, how do you know the line is stuck?","options":["The queue is empty.","Every waiting item has been rejected once in a row.","The first item was rejected.","The queue size is odd."],"answer":1,"explain":"A full rotation of rejections, as many as there are waiting items, means the next pass would repeat the same rejections forever."}
```

```quiz
{"id":"sq-rev-two-stack","q":"When may the input stack of a two-stack queue be moved onto the output stack?","options":["On every removal.","Only when the output stack is empty.","Only when the input stack is full.","Never; both stacks stay separate."],"answer":1,"explain":"Moving while the output stack still holds older values would put newer values in front of them, so a transfer is allowed only when the output stack is empty."}
```

```quiz
{"id":"sq-rev-mark-enqueue","q":"In a queue-driven search, when should a state be marked as discovered?","options":["When it is removed from the queue.","When it is added to the queue.","When its neighbours are listed.","After the search ends."],"answer":1,"explain":"Marking at insertion guarantees that a state with several incoming transitions enters the queue once, which keeps the work linear."}
```

```quiz
{"id":"sq-rev-count-order","q":"Why is ([)] rejected even though it has two openings and two closings of matching kinds?","options":["It is too short.","The closing round bracket meets a square bracket as the nearest opener.","Counts of each kind differ.","It begins with a round bracket."],"answer":1,"explain":"Each closing must match the most recent unresolved opening, and here the nearest opener is the wrong kind."}
```

```quiz
{"id":"sq-rev-frame","q":"In a nested structure with values, what does a frame on the stack hold?","options":["The final answer.","The unresolved state of one enclosing level.","The deepest nesting seen.","A copy of the whole input."],"answer":1,"explain":"Each frame saves what must be restored when its inner level closes, such as a running total or a repeat count."}
```

```quiz
{"id":"sq-rev-min-equal","q":"In a two-stack minimum, why is a value recorded when it is equal to the current minimum?","options":["To save space.","So that popping one of two equal minimums still leaves a record of the other.","To keep the stacks the same size.","Because equal values sort last."],"answer":1,"explain":"Each standing copy of the minimum needs its own record, otherwise one pop would erase the only record of a value that is still on the stack."}
```

```quiz
{"id":"sq-rev-level-size","q":"When must the queue size be read in a batch loop?","options":["At every step of the inner loop.","Once, before the inner loop starts.","After the inner loop ends.","Never; the loop uses isEmpty."],"answer":1,"explain":"The live size grows as children are appended, so only the size taken before the loop identifies the items of the current round."}
```

```quiz
{"id":"sq-rev-digits","q":"What turns the digits 1 and 2 into the count 12 while reading text?","options":["count = count + digit","count = count * 10 + digit","count = digit","count = count * 2 + digit"],"answer":1,"explain":"Each new digit shifts the earlier digits one decimal place to the left before it is added."}
```

```quiz
{"id":"sq-rev-postfix-order","q":"For the postfix sequence 8 3 -, which value is popped first and what is it called?","options":["8, the left operand.","3, the right operand.","3, the left operand.","8, the right operand."],"answer":1,"explain":"The last pushed value is on top and is the right operand, so the result is the left value minus the right value, which is five."}
```
