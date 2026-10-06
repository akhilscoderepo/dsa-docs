<!-- lesson-kind: standard -->
<!-- lesson-id: partial-and-k-group-reversal -->
## Reverse Blocks Inside A List

<!-- stage: context -->
### Why The Last Group Comes Back Reversed

A job queue stores tasks in a list. A rule says that every three consecutive tasks run in reverse order, and a final group with fewer than three tasks keeps its order. A developer reverses each group as the loop reaches it. The list has eight tasks, so the last group has two tasks. The loop reverses that short group too, and the output breaks the rule. The developer adds code to reverse the short group back, and the list stays wrong until that repair has run.

A whole-list reversal never faces this problem, because it always touches every node. A reversal of a group touches only some nodes, and it must join the reversed group to the nodes on both sides. This lesson answers one question: how does the method learn that a group is complete before it changes any link?

<!-- stage: naive -->
### Reversing First And Repairing Later

The direct plan reverses each group as the loop reaches it. If the loop runs out of nodes before it has moved `k` of them, it reverses the moved nodes again to restore their order.

```java
final class ReverseThenRepair {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    // Reverses up to k nodes from start. Returns the new first node and writes the moved count to moved[0].
    static Node reverseUpTo(Node start, int k, int[] moved) {
        Node prev = null;
        Node curr = start;
        int count = 0;
        while (curr != null && count < k) {          // stops early when the list ends
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
            count++;
        }
        start.next = curr;                           // the old first node now ends the group
        moved[0] = count;
        return prev;
    }

    static Node reverseGroups(Node head, int k) {
        Node newHead = null;                         // set by the first group
        Node pred = null;                            // last node of the previous group
        Node first = head;                           // first node of the current group
        int[] moved = new int[1];
        while (first != null) {
            Node groupHead = reverseUpTo(first, k, moved);
            boolean tooShort = moved[0] < k;
            if (tooShort) groupHead = reverseUpTo(groupHead, k, moved);   // reverse the moved nodes back
            if (pred == null) newHead = groupHead; else pred.next = groupHead;
            if (tooShort) break;                     // a short group is always the last one
            pred = first;                            // the old first node now ends the group
            first = first.next;                      // the node after the group
        }
        return newHead;
    }
}
```

On `1, 2, 3, 4, 5` with `k = 2` the method reverses `1, 2` and `3, 4`, then reverses the single node 5 twice, so the output is correct. The repair is the part that needs care.

<!-- stage: bottleneck -->
### Counting The Wasted Writes

```predict
A list has n nodes and the last group has m nodes, with m smaller than k. How many extra next writes does the repair cost, and what is wrong with the list while the repair has not run?

The repair costs about m extra writes, which is O(k) in the worst case, so the total stays O(n). Until the repair runs, the short group is in reversed order, and any reader of the list sees a wrong order.
```

The time cost is small. The cost that matters is correctness. The method writes every node of the short group twice, and the list is wrong between the two writes. The repair is also easy to get wrong, because it must restart from the right node after the first reversal changed the links.

The fix does not need the repair at all. A walk that only reads `next` fields can count the group first. A count that reaches `k` proves the group is complete, and a count that stops early proves it is short. The reading walk changes no link, so a short group needs no undo.

<!-- stage: insight -->
### Checking The Group Before Changing It

The safe method splits each group into two parts: a **look-ahead** that only reads, and a reversal that only writes. The look-ahead walks `k` hops from the first node of the group. If the walk reaches `null` before the `k`th hop, the group is short, and the method stops without a single write.

#### Three Anchors Around Every Group

A reversal of a group touches two neighbors. The **predecessor** is the node just before the group, and it must point at the new first node of the group after the reversal. The **group tail** is the group's old first node, which becomes the last node after the reversal. It must point at the first node after the group, which the look-ahead already found.

<!-- names: look-ahead, predecessor, group tail -->

#### One Reversal Reconnects Both Sides

The reversal loop from the previous lesson runs for exactly `k` turns. When it stops, `curr` holds the first node after the group. Two assignments finish the work. The assignment `groupTail.next = curr` joins the reversed group to the rest of the list. The assignment `predecessor.next = prev` joins the node before the group to the new first node. If the group starts at the head, there is no predecessor, and the returned head must change to `prev` instead.

#### Repeating For The Next Group

After a group is reversed, its tail is the predecessor of the next group, and `curr` is the first node of the next group. The method repeats the look-ahead and the reversal until the look-ahead fails or the list ends. Each node is read once by the look-ahead and moved once by the reversal.

<!-- stage: variables -->
### The References Around One Group

- **first** holds the first node of the group before the reversal, which becomes the group tail.
- **probe** holds the node reached by the look-ahead, which is the first node after a complete group.
- **pred** holds the predecessor, the last node of the previous group, or `null` before the first group.
- **newHead** holds the head to return, which is set by the first reversed group.
- **k** is the group size, and every group has exactly `k` nodes or is the final short group.

<!-- stage: trace -->
### Reversing One Group And Then Many

#### Reversing The Middle Three Nodes

Take the list `1, 2, 3, 4, 5` and reverse the three nodes `2, 3, 4`. The pointer `pred` marks the node before the group. The pointer `prev` marks the first node of the reversed part, and `curr` marks the first node not yet moved. The variable `chain` shows the list read from the head. While the reversal runs, the chain is cut short, because `pred` still points at the old group head, and the first move already changed that node's `next`.

```trace
{"cells":[1,2,3,4,5],"pointers":["pred","prev","curr"],"steps":[{"at":{"pred":0,"prev":-1,"curr":1},"vars":{"chain":"1,2,3,4,5"},"note":"Start: pred is the node 1, and the group is the nodes 2, 3 and 4. The look-ahead found three nodes, so the reversal may begin."},{"at":{"pred":0,"prev":1,"curr":2},"vars":{"chain":"1,2"},"note":"The node 2 moves across: saved keeps the rest, the node is redirected at the reversed part, and prev takes the node 2."},{"at":{"pred":0,"prev":2,"curr":3},"vars":{"chain":"1,2"},"note":"The node 3 moves across: saved keeps the rest, the node is redirected at the reversed part, and prev takes the node 3."},{"at":{"pred":0,"prev":3,"curr":4},"vars":{"chain":"1,2"},"note":"The node 4 moves across: saved keeps the rest, the node is redirected at the reversed part, and prev takes the node 4."},{"at":{"pred":0,"prev":3,"curr":4},"vars":{"chain":"1,2,5"},"note":"first.next = curr links the old group head, the node 2, to the node 5."},{"at":{"pred":0,"prev":3,"curr":4},"vars":{"chain":"1,4,3,2,5"},"note":"pred.next = prev links the node 1 to the node 4. The list reads 1,4,3,2,5."}]}
```

After three moves, `curr` holds the node 5. The assignment `first.next = curr` links the old group head, the node 2, to the node 5, and the assignment `pred.next = prev` links the node 1 to the node 4. Both writes use references that the walk kept.

#### Reversing Groups Of Two With A Short Rest

Now take the same list with `k = 2`. The pointer `pred` marks the tail of the previous group, and `first` marks the first node of the next group. Here the chain is whole after every group.

```trace
{"cells":[1,2,3,4,5],"pointers":["pred","first"],"steps":[{"at":{"pred":-1,"first":0},"vars":{"chain":"1,2,3,4,5"},"note":"Start: no group is reversed yet, and the first group begins at the node 1. The look-ahead reads two nodes, so the group is complete."},{"at":{"pred":0,"first":2},"vars":{"chain":"2,1,3,4,5"},"note":"The group 1,2 is reversed and its tail is the node 1. The next group starts at the node 3. The look-ahead from there finds two nodes."},{"at":{"pred":2,"first":4},"vars":{"chain":"2,1,4,3,5"},"note":"The group 3,4 is reversed and its tail is the node 3. The next group starts at the node 5. The look-ahead from there reads the node 5 and then reaches the end."},{"at":{"pred":2,"first":4},"vars":{"chain":"2,1,4,3,5"},"note":"The look-ahead counted one node, which is fewer than k, so the method stops with no write. The node 5 stays in place."}]}
```

Each of the first two groups is complete, so the method reverses it. The third group holds only the node 5, and the look-ahead fails, so the method stops. The node 5 keeps its place, and no write undoes anything.

<!-- stage: code -->
### Reversing Groups In Code

```java
final class GroupReverse {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node reverseFirst(Node start, int k) {
        Node prev = null;
        Node curr = start;
        for (int i = 0; i < k; i++) {          // exactly k nodes cross the boundary
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        start.next = curr;                     // the group tail links to the node after the group
        return prev;                           // the new first node of the group
    }

    static Node reverseKGroup(Node head, int k) {
        Node newHead = null;                   // set by the first reversed group
        Node pred = null;                      // last node of the previous group
        Node first = head;                     // first node of the current group
        while (true) {
            Node probe = first;
            int seen = 0;
            while (probe != null && seen < k) {    // look-ahead: read only, no writes
                probe = probe.next;
                seen++;
            }
            if (seen < k) break;               // a short group stays as it is
            Node groupHead = reverseFirst(first, k);
            if (pred == null) newHead = groupHead;     // the first group sets the returned head
            else pred.next = groupHead;                // later groups join the previous group
            pred = first;                      // the old first node is now the group tail
            first = probe;                     // the next group starts after this one
        }
        return newHead == null ? head : newHead;
    }
}
```

The look-ahead leaves `first` untouched, so a failed look-ahead needs no cleanup. After the last full group, the previous group's tail already points at `first` because `reverseFirst` wrote that link.

- **Time** is O(n), because the look-ahead reads each node once and the reversal moves each node once.
- **Space** is O(1), because the code stores a few references and no copy.

<!-- stage: applicability -->
### Using The Check-Then-Reverse Rule

#### Stating What Must Be Known First

The invariant of this pattern is that the method knows the predecessor, the first node, the node after the group and whether a full group exists before it writes any link. A list problem that mentions a "block", a "range" or "every k nodes" has this shape. Write down the four items before coding.

#### Avoiding The Repair Trap

The false friend is to reverse first and decide later. It looks shorter, but the undo needs references that the reversal has overwritten. A read-only look-ahead costs one extra pass over the group, and it removes the undo.

#### Covering The Head And Short Lists

The first group has no predecessor, so the returned head changes. A list shorter than `k` returns the original head with no write. A value of `k = 1` makes every group trivially complete, and the reversal changes nothing. State these three cases in a comment before the loop.

<!-- stage: exercises -->
### Exercises

#### [Build] Reverse Exactly Two Nodes (Author exercise)
<!-- id: ll-two-nodes -->

**Prerequisites.** The reversal loop from the previous lesson and the three anchors of this lesson.

**Problem.** A node `pred` is followed by two nodes `a` and `b`, and then by a node `after` or by `null`. Swap `a` and `b` by changing `next` fields so that the chain reads `pred`, `b`, `a`, `after`. Do not change any value and do not allocate a node.

**Constraints.** The limits are:
- **Length** is at least 3 nodes, so `pred.next` and `pred.next.next` are not `null`.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Answer** is the changed list, read from the head.
- **Mutation** changes `next` fields of `pred`, `a` and `b`.

**Example 1.** Input list `1, 2, 3, 4` with `pred` at the node 1, output `1, 3, 2, 4`.

**Example 2.** Input list `7, 8, 9` with `pred` at the node 7, output `7, 9, 8`.

**Hint.** Which three `next` fields change? Which node must `a.next` point at, and where is it before the first write?

**Changed decision.** The group size is two, and the code reconnects a supplied predecessor and successor.

#### [Vary] Reverse Linked List II (LeetCode 92)
<!-- id: ll-reverse-range-clamped -->

**Prerequisites.** The exercise above and the reversal loop of the previous lesson.

**Problem.** A list starts at `head`, and `from` and `to` are 0-based positions. Reverse the nodes at positions `from` through `min(to, n - 1)` inclusive, where `n` is the length. This contract differs from the 1-based form: `to` may exceed the last position and is then clamped, and a range that is empty after clamping leaves the list unchanged. Return the head.

**Constraints.** The limits are:
- **Length** is `n` with `0 <= n <= 500`.
- **Values** satisfy `-500 <= val <= 500`.
- **Positions** satisfy `0 <= from` and `from <= to <= 10^4`.
- **Mutation** changes `next` fields only.

**Example 1.** Input list `1, 2, 3, 4, 5`, `from = 1` and `to = 3`, output `1, 4, 3, 2, 5`.

**Example 2.** Input list `1, 2, 3`, `from = 1` and `to = 9`, output `1, 3, 2`.

**Hint.** How many nodes does the block hold after clamping? What does the node before the block need to point at when `from` is 0?

**Changed decision.** The end position is clamped to the list, so the block length depends on `n`.

#### [Boundary] Incomplete Final Group (Author exercise)
<!-- id: ll-incomplete-group -->

**Prerequisites.** The two exercises above.

**Problem.** Reverse the first `k` nodes of the list that starts at `head`, if and only if the list has at least `k` nodes. Otherwise return the original head and write no `next` field at all. Return the head of the resulting list.

**Constraints.** The limits are:
- **Length** is between 0 and 10^4 nodes.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Group size** satisfies `1 <= k <= 10^4`.
- **Mutation** changes `next` fields only when the first `k` nodes all exist.

**Example 1.** Input list `1, 2, 3` and `k = 3`, output `3, 2, 1`.

**Example 2.** Input list `1, 2` and `k = 3`, output `1, 2`, and no `next` field changes.

**Hint.** What walk can prove that `k` nodes exist without writing? What does that walk return when the list ends early?

**Changed decision.** A read-only look-ahead decides whether any write is allowed.

#### [Recognize] Reverse Nodes in k-Group (LeetCode 25)
<!-- id: ll-reverse-k-group -->

**Prerequisites.** All three exercises above.

**Problem.** Reverse the list that starts at `head` in groups of `k` nodes, where `k` is an integer, and return the head of the changed list. Nodes in a complete group of `k` consecutive nodes appear in reverse order. If the number of nodes is not a multiple of `k`, the final group of fewer than `k` nodes keeps its original order. Change `next` fields only, and do not change any value.

**Constraints.** The limits are:
- **Length** is `n` with `1 <= n <= 5000`.
- **Values** satisfy `0 <= val <= 1000`.
- **Group size** satisfies `1 <= k <= n`.
- **Mutation** changes `next` fields only.

**Example 1.** Input list `1, 2, 3, 4, 5` and `k = 2`, output `2, 1, 4, 3, 5`.

**Example 2.** Input list `1, 2, 3, 4, 5` and `k = 3`, output `3, 2, 1, 4, 5`.

**Hint.** After a group is reversed, which node is the predecessor of the next group? Which node does the look-ahead leave you at?

**Changed decision.** The bounded reversal repeats while a complete group remains.
