<!-- lesson-kind: standard -->
<!-- lesson-id: reverse -->
## Reverse

<!-- stage: context -->
### Turning A Train Around At The Depot

A short freight train is made of wagons, and each wagon is coupled only to the wagon behind it. The locomotive knows the first wagon, and every wagon knows the one behind, but no wagon knows the one in front. The depot has a turntable that sends the train back the way it came, and the yard master has to rebuild the train so that the old last wagon is now the first and every coupling points the other way.

Some wagons carry sealed cargo that is logged against the wagon itself, so unloading and reloading the cargo to swap places is not allowed. The wagons must be recoupled, one coupling at a time. The yard master is a careful person, and she has learned a lesson from a colleague who once uncoupled a wagon from its follower before writing down which wagon the follower was. The rest of the train rolled quietly away down the siding.

<!-- stage: naive -->
### Copy Cargo Into A Row And Back

One way to turn the train is to read every cargo label into a row, then walk the wagons again and write the labels back in the opposite order.

```java
final class TurnByCopy {
    static final class Wagon {
        int label;
        Wagon behind;
        Wagon(int label) { this.label = label; }
    }

    static Wagon turn(Wagon first) {
        int count = 0;
        for (Wagon w = first; w != null; w = w.behind) count++;
        int[] row = new int[count];
        int i = 0;
        for (Wagon w = first; w != null; w = w.behind) row[i++] = w.label;
        i = count - 1;
        for (Wagon w = first; w != null; w = w.behind) w.label = row[i--];
        return first;
    }
}
```

It produces the right order of labels. For wagons 3, 8, 2, 6 it leaves the train reading 6, 2, 8, 3, from the same first wagon.

<!-- stage: bottleneck -->
### Copying Breaks Identity And Costs Memory

The copy needs a row as long as the train, so it uses O(n) extra memory, and it touches every wagon twice. More seriously, it breaks the rule of the depot. The wagon that was first is still first, but it now carries a different label, so anything that was recorded against that wagon, such as a log entry or a reference held by another structure, now points at the wrong cargo. Where a node carries a large payload, moving the payload is also far more expensive than moving a link.

The right move is to change the couplings and leave the wagons alone, which takes one step per wagon and O(1) memory beyond a few references. The difficulty is the one the yard master learned: changing a coupling cuts off access to everything behind that wagon, so the reference to the follower must be recorded first. A rule that is safe at every step, with no wagon ever out of reach, is what turns a clumsy idea into an algorithm.

<!-- stage: insight -->
### Save, Redirect, Advance

The train is split into two parts by two references. The reference `prev` heads the **reversed prefix**, the wagons already turned, with the first wagon of the original order at its far end, and it starts as null. The reference `curr` heads the **untouched suffix**, the wagons not yet visited, and it starts at the head. Each iteration performs the **redirect step** in three moves, always in this order. First, save `curr.next` in a local reference. Second, point `curr.next` at `prev`. Third, advance by setting `prev = curr` and `curr = saved`.

<!-- names: reversed prefix, untouched suffix, redirect step -->

The invariant is that the reversed prefix and the untouched suffix together contain every node exactly once, and that no node is reachable only through a link that was just overwritten. Before the redirect step the only link to the suffix beyond `curr` is `curr.next`, and the saved reference holds a copy of it. After the step, `curr` has become the new head of the reversed prefix and the saved reference is the new head of the suffix. When `curr` is null the suffix is empty, and `prev` is the head of the fully reversed list.

Each link is rewritten once, so the cost is O(n) time and O(1) extra space.

<!-- stage: variables -->
### Prev, Curr And The Saved Link

The three references play separate roles. `prev` is null at the start and is the answer at the end. `curr` is the node being turned, and it becomes null when the suffix has been used up. The local reference `saved` lives for one iteration only. An empty list has a null head, so the loop does not run and `prev` stays null, which is the correct result. A one-node list runs the loop once, redirecting its single node to null, which leaves it unchanged.

<!-- stage: trace -->
### Four Wagons Turn And One Segment Turns

Take the wagons labelled `3, 8, 2, 6`. At the start the reversed prefix is empty and the suffix is the whole train. The first iteration saves the wagon holding 8, points the wagon holding 3 at null, and advances, so the reversed prefix is the single wagon 3. The second iteration saves the wagon holding 2, points the wagon holding 8 at the wagon holding 3, and advances. The third points the wagon holding 2 at the wagon holding 8, and the fourth points the wagon holding 6 at the wagon holding 2. Then `curr` is null and `prev` names the wagon holding 6, so the train reads 6, 2, 8, 3.

A second run turns only the middle segment of `3, 8, 2, 6, 9, 1`, positions 2 to 4. The wagon holding 3 sits before the segment. The three segment wagons are reversed with the same three moves, and then two couplings are repaired: the wagon before the segment is pointed at the new segment head, and the old segment head, now the segment tail, is pointed at the wagon after it. The result reads 3, 6, 2, 8, 9, 1.

```trace
{"cells":[3,8,2,6],"pointers":["prev","curr"],"steps":[{"at":{"prev":-1,"curr":0},"vars":{"reversed":"empty","untouched":"3>8>2>6"},"note":"The reversed prefix is empty and prev is null. The untouched suffix is the whole list, headed by the node holding 3."},{"at":{"prev":0,"curr":1},"vars":{"reversed":"3","untouched":"8>2>6"},"note":"The old successor (8) was saved, the node holding 3 was pointed at the previous node, and both references moved forward. The reversed prefix now reads 3."},{"at":{"prev":1,"curr":2},"vars":{"reversed":"8>3","untouched":"2>6"},"note":"The old successor (2) was saved, the node holding 8 was pointed at the previous node, and both references moved forward. The reversed prefix now reads 8, 3."},{"at":{"prev":2,"curr":3},"vars":{"reversed":"2>8>3","untouched":"6"},"note":"The old successor (6) was saved, the node holding 2 was pointed at the previous node, and both references moved forward. The reversed prefix now reads 2, 8, 3."},{"at":{"prev":3,"curr":4},"vars":{"reversed":"6>2>8>3","untouched":"empty"},"note":"The old successor (null) was saved, the node holding 6 was pointed at the previous node, and both references moved forward. The reversed prefix now reads 6, 2, 8, 3."}]}
```

```trace
{"cells":[3,8,2,6,9,1],"pointers":["before","prev","curr"],"steps":[{"at":{"before":0,"prev":-1,"curr":1},"vars":{"whole":"3>8>2>6>9>1","segment_tail":"8"},"note":"The node holding 3 sits just before the segment, and the segment starts at the node holding 8. The first node of the segment will become its tail, so it is remembered."},{"at":{"before":0,"prev":1,"curr":2},"vars":{"reversed_part":"8","rest":"2>6>9>1"},"note":"One more segment node is redirected backward. The reversed part reads 8 and the rest starts at the node holding 2."},{"at":{"before":0,"prev":2,"curr":3},"vars":{"reversed_part":"2>8","rest":"6>9>1"},"note":"One more segment node is redirected backward. The reversed part reads 2, 8 and the rest starts at the node holding 6."},{"at":{"before":0,"prev":3,"curr":4},"vars":{"reversed_part":"6>2>8","rest":"9>1"},"note":"One more segment node is redirected backward. The reversed part reads 6, 2, 8 and the rest starts at the node holding 9."},{"at":{"before":0,"prev":3,"curr":4},"vars":{"whole":"3>6>2>8>9>1"},"note":"The node before the segment is pointed at the new segment head, and the old segment head, now its tail, is pointed at the node after the segment. The list reads 3, 6, 2, 8, 9, 1."}]}
```

<!-- stage: code -->
### Reverse A List And A Segment

```java
final class ReverseCode {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node reverse(Node head) {
        Node prev = null, curr = head;
        while (curr != null) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        return prev;
    }

    static Node reverseBetween(Node head, int left, int right) {
        Node before = null, cursor = head;
        for (int i = 1; i < left; i++) { before = cursor; cursor = cursor.next; }
        Node segmentTail = cursor;
        Node prev = null, curr = cursor;
        for (int i = left; i <= right; i++) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        segmentTail.next = curr;
        if (before == null) return prev;
        before.next = prev;
        return head;
    }
}
```

Both methods rewrite each visited link once, so they run in O(n) time and O(1) extra space. The second returns the old head unless the segment starts at position 1, in which case the reversed segment head is the new head.

<!-- stage: applicability -->
### When Every Edge Must Point Backward

Think of the redirect step whenever the task needs the order of a chain flipped, or a stretch of it flipped, and nodes must keep their identity. The same shape appears in palindrome checks, in reordering a list, and in reversing groups. The invariant is that `prev` heads the fully reversed prefix and `curr` heads the untouched suffix, so that every node is in exactly one of the two parts and none is reachable only through an overwritten link.

The false friend is the natural-looking order of assignments: point `curr.next` at `prev` first, and then try to advance with `curr = curr.next`. That moves `curr` to `prev`, and the loop either stops at once or circles back. A second false friend is copying values, which gives the right output on a plain test and breaks any other reference to a node. A third is forgetting to reconnect both ends of a segment, which leaves a list that is cut or looped.

Do not reverse when only the order of reading is needed and not the structure, since a recursive or stack-based read gives it without rewiring. Reversal also changes the list for every other holder of the head, so it must be stated in the contract. In Java, a recursive reversal uses one stack frame per node and overflows on long lists, so the loop form is the safe one.

<!-- stage: exercises -->
### Exercises

#### [Build] Reverse Three Nodes By Hand (Author exercise)
<!-- id: ll-reverse-three-by-hand -->

**Prerequisites.** The node invariants lesson of this chapter.

**Problem.** A linked list has exactly three nodes, given by their values from head to tail. Reverse it by performing the save, redirect and advance moves three times by hand, and return the values of the result from head to tail.

**Constraints.** The list has exactly three nodes, and -10^9 <= value <= 10^9. The nodes must be reused, not replaced.

**Example 1.** Input `values = [1, 2, 3]`, output `[3, 2, 1]`.

**Example 2.** Input `values = [5, 5, 9]`, output `[9, 5, 5]`.

**Hint.** Write down the three references before the first move and after each move. After the third move which of them is null, and which one is the new head?

**Changed decision.** First rung: the three moves are done in the stated order, and the old successor is saved before any link is rewritten.

#### [Vary] Reverse Linked List (LeetCode 206)
<!-- id: ll-reverse-list -->

**Prerequisites.** The Reverse Three Nodes By Hand exercise above.

**Problem.** Given the head of a singly linked list, reverse the list and return the new head.

**Constraints.** 0 <= n <= 5000 and -5000 <= value <= 5000.

**Example 1.** Input `values = [7, 1, 4, 9, 2]`, output `[2, 9, 4, 1, 7]`.

**Example 2.** Input `values = [6, 6]`, output `[6, 6]`.

**Hint.** What condition ends the loop, and what do the two references hold at that moment? Which of them is returned?

**Changed decision.** The loop runs until the untouched suffix is empty, so the number of nodes does not need to be known beforehand.

#### [Boundary] Empty And One Node (Author exercise)
<!-- id: ll-reverse-empty-one -->

**Prerequisites.** The two exercises above.

**Problem.** Reverse a list that may have zero or one node, and report whether the original head object is the head of the result. Return the values of the result followed by `1` if the result head is the same node object as the original head, and `0` otherwise.

**Constraints.** 0 <= n <= 100 and -100 <= value <= 100. For n = 0 the head is null, and the flag is `1` because null is the same as null.

**Example 1.** Input `values = []`, output `[1]`.

**Example 2.** Input `values = [8]`, output `[8, 1]`.

**Hint.** What does the loop do for a null head? For one node, what does the redirect step assign to that node's `next`, and which node is `prev` at the end?

**Changed decision.** No branch for small lists is allowed; the same loop must return the right head for zero, one, and many nodes.

#### [Recognize] Reverse Linked List II (LeetCode 92)
<!-- id: ll-reverse-between -->

**Prerequisites.** All three exercises above.

**Problem.** Given the head of a singly linked list and two positions `left` and `right` with `1 <= left <= right <= n`, counted from 1, reverse the nodes from position `left` to position `right` and return the head of the list.

**Constraints.** 1 <= n <= 500 and -500 <= value <= 500. One pass over the list.

**Example 1.** Input `values = [3, 8, 2, 6, 9, 1]`, `left = 2`, `right = 4`, output `[3, 6, 2, 8, 9, 1]`.

**Example 2.** Input `values = [5, 6]`, `left = 1`, `right = 2`, output `[6, 5]`.

**Hint.** Which node must be remembered before the segment starts, and which node becomes the segment's tail? What changes when `left` is 1?

**Changed decision.** Only a stretch is reversed, so both boundaries are reconnected after the loop, and the head changes only when the stretch starts at position 1.
