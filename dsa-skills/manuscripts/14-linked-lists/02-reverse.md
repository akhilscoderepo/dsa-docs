<!-- lesson-kind: standard -->
<!-- lesson-id: reverse -->
## Reverse A List In One Pass

<!-- stage: context -->
### Why The Reversed List Has One Node

A log viewer stores entries from oldest to newest in a list, and the user asks to see the newest entry first. A developer writes a loop that walks the list and sets each node's `next` to the node before it. The test list has five entries. After the loop the viewer shows one entry and nothing else. The other four entries are still in memory, but no variable leads to them any more.

The loop did the right kind of work in the wrong order. Reversing a list means changing every `next` field, and each change cuts the only link to the rest of the list. The method needs a way to turn every link around while the rest of the list stays in reach.

<!-- stage: naive -->
### Copying The Values Into An Array

The first idea that avoids the problem is to leave the links alone. Copy the values into an array, then walk the list a second time and write the values back from the end of the array to the start.

```java
final class ReverseByCopy {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node reverseValues(Node start) {
        int n = 0;
        for (Node c = start; c != null; c = c.next) n++;          // first walk counts the nodes
        int[] copy = new int[n];
        int i = 0;
        for (Node c = start; c != null; c = c.next) copy[i++] = c.val;   // second walk copies the values
        i = n - 1;
        for (Node c = start; c != null; c = c.next) c.val = copy[i--];   // third walk writes them back reversed
        return start;
    }
}
```

On `1, 2, 3` the method returns the list `3, 2, 1`, and the first node is still the same object. Every link stays in place, so no node can be lost.

<!-- stage: bottleneck -->
### Measuring The Memory And The Meaning

```predict
The copy method visits each node three times. What does it cost in time and in extra memory for a list of n nodes, and what stays wrong for a caller that holds a reference to the node that was last?

Three walks cost O(n) time, and the array costs O(n) extra memory. A caller that holds the last node still finds the old last node at the old end, now holding the first value, so the node did not move.
```

The array doubles the memory for the list, and a list of one million nodes needs a four-megabyte array of `int` values. The second cost is harder to see. The method moves values between nodes and moves no node. Code that keeps a reference to a particular node, such as a cursor or an entry in a map, sees a different value after the call.

When each node carries a large object or a reference that other structures share, copying the values is wrong in both ways. A method that rewires the links keeps each node with its value and needs no array.

<!-- stage: insight -->
### Turning Links Around One By One

The method keeps the list as two parts that together hold every node. One part is the **reversed prefix**, the nodes already turned around. The other part is the **untouched suffix**, the nodes whose links still point forward.

#### Two References Mark The Boundary

The variable `prev` holds the first node of the reversed prefix, or `null` when the prefix is empty. The variable `curr` holds the first node of the untouched suffix, or `null` when the suffix is empty. At the start `prev` is `null` and `curr` is the head. The reversed prefix is empty, and the untouched suffix is the whole list.

<!-- names: reversed prefix, untouched suffix, redirect -->

#### One Step Moves One Node Across

One step moves the first node of the untouched suffix to the front of the reversed prefix. That step has four parts, and their order is fixed. First `saved` copies `curr.next`, so the rest of the suffix stays reachable. Next the **redirect** assigns `curr.next = prev`, which points the node backward at the old prefix. Then `prev` takes the value of `curr`, because the redirected node is the new first node of the prefix. Last `curr` takes the value of `saved`.

#### Why The Loop Ends Cleanly

The loop runs while `curr` is not `null`. When it stops, the untouched suffix is empty, so the reversed prefix holds all `n` nodes, and `prev` is the new head. The old head was the first node moved, and the redirect pointed it at `null`, so it is now the last node and ends the list correctly. The method moves each node once and allocates nothing.

<!-- stage: variables -->
### The Four References In One Step

- **prev** holds the first node of the reversed prefix, or `null` when the prefix is empty.
- **curr** holds the first node of the untouched suffix, or `null` when the suffix is empty.
- **saved** holds `curr.next`, copied before the redirect.
- **head** is the caller's reference, and it still points at the old first node, which is the new last node.

The method returns `prev`, because the caller must replace its stored head with the new first node.

<!-- stage: trace -->
### Reversing Three Nodes And Losing Them

#### Turning Links Around In The Right Order

A pointer that sits outside the cells means `null`. Take the list `1, 2, 3`. The pointers `prev` and `curr` mark the boundary between the reversed prefix and the untouched suffix. The variable `prefix` shows the reversed prefix from `prev`, and `suffix` shows the untouched suffix from `curr`.

```trace
{"cells":[1,2,3],"pointers":["prev","curr"],"steps":[{"at":{"prev":-1,"curr":0},"vars":{"prefix":"empty","suffix":"1,2,3"},"note":"Start: the reversed prefix is empty and the untouched suffix is the whole list."},{"at":{"prev":0,"curr":1},"vars":{"prefix":"1","suffix":"2,3"},"note":"saved keeps the rest, then the node 1 is redirected at the old prefix. The prefix now starts at the node 1."},{"at":{"prev":1,"curr":2},"vars":{"prefix":"2,1","suffix":"3"},"note":"saved keeps the rest, then the node 2 is redirected at the old prefix. The prefix now starts at the node 2."},{"at":{"prev":2,"curr":3},"vars":{"prefix":"3,2,1","suffix":"empty"},"note":"saved keeps the rest, then the node 3 is redirected at the old prefix. The prefix now starts at the node 3."}]}
```

The last step shows `prev` on the node 3 and `curr` at the end, so the suffix is empty. Every node moved across exactly once. The node 1, which started as the head, now ends the list.

#### Redirecting Before Saving

Now run the same list with the two statements in the wrong order. The method redirects `curr.next = prev` and then reads `curr.next` for the advance. The variable `reachable` lists the nodes the program can still find.

```trace
{"cells":[1,2,3],"pointers":["prev","curr"],"steps":[{"at":{"prev":-1,"curr":0},"vars":{"reachable":"1,2,3"},"note":"Start: curr is the node 1, and no variable holds saved."},{"at":{"prev":-1,"curr":0},"vars":{"reachable":"1"},"note":"The node 1 is redirected first. Its next is now null, so the nodes 2 and 3 lose their only link."},{"at":{"prev":0,"curr":3},"vars":{"reachable":"1"},"note":"The advance reads the new null, so curr is null and the loop ends. The list is the single node 1."}]}
```

The first redirect changes the node 1 so that it points at `null`. The advance then reads that new `null`, so `curr` becomes `null` and the loop stops after one step. The nodes 2 and 3 have no reference left, which is the failure from the opening example.

<!-- stage: code -->
### Reversing In Code

```java
final class ListReverse {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node reverse(Node head) {
        Node prev = null;                      // the reversed prefix starts empty
        Node curr = head;                      // the untouched suffix starts as the whole list
        while (curr != null) {                 // stop when no node remains in the suffix
            Node saved = curr.next;            // keep the rest of the suffix reachable
            curr.next = prev;                  // redirect this node at the reversed prefix
            prev = curr;                       // this node becomes the first of the prefix
            curr = saved;                      // the suffix now starts at the saved node
        }
        return prev;                           // the new head, or null for the empty list
    }
}
```

The loop body has no branch, so the empty list and the one-node list need no special case. For the empty list the body never runs and the method returns `null`. For a one-node list the body runs once and returns the same node, now redirected to `null`.

- **Time** is O(n), because each node moves across the boundary once.
- **Space** is O(1), because the method stores three references.

<!-- stage: applicability -->
### Using The Boundary Rule

#### Naming The Two Parts Before Coding

Every statement in the loop preserves one fact. The nodes before `curr` form the reversed prefix, and the nodes from `curr` onward form the untouched suffix. This fact is the invariant of the method. Variants such as reversing a range or reversing in blocks keep the same two parts and change only where the loop starts and stops.

#### Spotting The Order Mistake

The statement `curr.next = prev` looks harmless in isolation, and it is the false friend of this lesson. It is correct only after `saved` has taken `curr.next`. A reviewer can check any pointer rewrite with one question: where does the old value of the field go before it is overwritten?

#### Recursion Costs Stack Space

A recursive reversal also works and reads well, but it uses one stack frame per node. A list of 100,000 nodes can overflow the default Java stack. The loop in this lesson uses constant space and is the safe form for long lists.

<!-- stage: exercises -->
### Exercises

#### [Build] Reverse Three Nodes By Hand (Author exercise)
<!-- id: ll-reverse-three -->

**Prerequisites.** The four-step move from this lesson.

**Problem.** A list contains exactly three nodes `a`, `b` and `c`, in that order, and `head` refers to `a`. Reverse the list by changing `next` fields only, without allocating a node. Perform the four steps by hand for each of the three nodes: copy the successor, redirect the node at the reversed prefix, advance `prev`, and advance `curr`. Return the new head.

**Constraints.** The limits are:
- **Length** is exactly 3 nodes.
- **Values** satisfy `-100 <= val <= 100`.
- **Answer** is a head reference to the old last node.
- **Mutation** changes `next` fields and no value.

**Example 1.** Input `1, 2, 3`, output `3, 2, 1`.

**Example 2.** Input `5, 5, 9`, output `9, 5, 5`, where the two 5 nodes keep their original relative identity.

**Hint.** Which node does `prev` hold after the first step? What does the node 1 point at after that step?

**Changed decision.** Each node turns around once, and the loop is unrolled by hand.

#### [Vary] Reverse Linked List (LeetCode 206)
<!-- id: ll-reverse-list -->

**Prerequisites.** The exercise above.

**Problem.** Given the head of a singly linked list, reverse the list and return the new head. The method reuses the existing nodes. Apply the same step until the untouched suffix is empty.

**Constraints.** The limits are:
- **Length** is between 0 and 5000 nodes.
- **Values** satisfy `-5000 <= val <= 5000`.
- **Answer** is the head of the reversed list, or `null` for an empty list.
- **Mutation** changes `next` fields and allocates no node.

**Example 1.** Input `1, 2, 3, 4, 5`, output `5, 4, 3, 2, 1`.

**Example 2.** Input `1, 2`, output `2, 1`.

**Hint.** The loop from the three-node case now runs until `curr` is `null`. What does the loop condition test?

**Changed decision.** The fixed length of three becomes a loop that ends when the suffix is empty.

#### [Boundary] Empty And One Node (Author exercise)
<!-- id: ll-reverse-boundary -->

**Prerequisites.** The two exercises above.

**Problem.** Reverse a list so that the old head ends as the last node and its `next` is `null`. An empty list returns `null`. A one-node list returns the same node. Write the method so that no `if` statement tests the length.

**Constraints.** The limits are:
- **Length** is between 0 and 10^5 nodes.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Answer** is the new head, which is the same object as the old head when the length is 1.
- **Mutation** changes `next` fields only.

**Example 1.** Input the empty list, output the empty list.

**Example 2.** Input list `8, 9`, output list `9, 8`, and the old head node 8 has `next` equal to `null`.

**Hint.** What does the loop do when `curr` starts as `null`? What does `prev` hold at the end for one node?

**Changed decision.** The boundary needs no special branch, because the starting `prev` is `null`.

#### [Recognize] Reverse Linked List II (LeetCode 92)
<!-- id: ll-reverse-between -->

**Prerequisites.** All three exercises above.

**Problem.** A list starts at `head`, and two 1-based positions `left` and `right` satisfy `left <= right`. Reverse the nodes at positions `left` through `right` inclusive. The nodes before `left` and after `right` stay in place and must stay linked to the reversed block. Return the head of the changed list.

**Constraints.** The limits are:
- **Length** is `n` with `1 <= n <= 500`.
- **Values** satisfy `-500 <= val <= 500`.
- **Positions** satisfy `1 <= left <= right <= n`.
- **Mutation** changes `next` fields only.

**Example 1.** Input list `1, 2, 3, 4, 5` with `left = 2` and `right = 4`, output `1, 4, 3, 2, 5`.

**Example 2.** Input list `3, 5` with `left = 1` and `right = 2`, output `5, 3`.

**Hint.** The block is a smaller list with its own head. Which node before the block must point at the new block head, and where must the old block head point?

**Changed decision.** The loop runs for a fixed number of nodes and reconnects both ends of the block.
