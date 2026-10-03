<!-- lesson-kind: standard -->
<!-- lesson-id: partial-and-k-group-reversal -->
## Partial And K-Group Reversal

<!-- stage: context -->
### Flipping Full Boxes On A Conveyor

A packing line sends parcels down a conveyor in a single file. At the end a worker flips the parcels in boxes of three: the first three parcels are reversed within their box, then the next three, and so on. A final box with fewer than three parcels is not a full box, and the supervisor's rule is that such a box goes out exactly as it arrived. Parcels cannot be unwrapped, so the parcels must be moved with their couplings, which are the only record of the order.

The worker already knows how to turn one box around. What bothers her is the bookkeeping between boxes. After a box is flipped, its old first parcel is at the back and must be linked to the next box, and the parcel before the box must be linked to the new front. Boxes after the first are also reached only by following couplings from the belt's start.

<!-- stage: naive -->
### Reuse The Segment Turn From The Start

One idea is to call the segment reversal from the previous lesson once for every full box, giving it the start and end positions of that box counted from the head of the belt.

```java
final class BoxFlipByRestart {
    static final class Parcel {
        int tag;
        Parcel next;
        Parcel(int tag) { this.tag = tag; }
    }

    static Parcel reverseBetween(Parcel head, int left, int right) {
        Parcel before = null, cursor = head;
        for (int i = 1; i < left; i++) { before = cursor; cursor = cursor.next; }
        Parcel segmentTail = cursor, prev = null, curr = cursor;
        for (int i = left; i <= right; i++) {
            Parcel saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        segmentTail.next = curr;
        if (before == null) return prev;
        before.next = prev;
        return head;
    }

    static Parcel flipBoxes(Parcel head, int k) {
        int n = 0;
        for (Parcel p = head; p != null; p = p.next) n++;
        for (int left = 1; left + k - 1 <= n; left += k) head = reverseBetween(head, left, left + k - 1);
        return head;
    }
}
```

It is correct. For the tags 9, 4, 7, 2, 8, 5, 3 with boxes of three it returns 7, 4, 9, 5, 8, 2, 3.

<!-- stage: bottleneck -->
### Every Box Walks From The Start Again

Each call to the segment reversal walks from the head to its first position. The box that starts at position `left` therefore costs about `left` steps before any flipping, and the sum over all boxes is about n / k boxes times an average of n / 2 steps, which is O(n^2 / k). For boxes of three on a belt of a hundred thousand parcels, that is more than a billion steps, where flipping every parcel once costs a hundred thousand.

The waste is the walk back to the start. After a box is flipped, the program already holds a reference to the parcel that now ends that box, which is exactly the parcel before the next box. Nothing needs to be rediscovered. A second issue is the decision of whether a box is full. The naive code counts all parcels once, which is fine, but a version that flips first and checks later would have to undo a partial flip. The check must come before any link is changed, and it must be made by looking ahead from the box start without altering anything.

<!-- stage: insight -->
### Look Ahead, Then Flip, Then Carry On

Process the belt box by box, carrying three references. The **group predecessor** is the last node of the box that was just finished, or null before the first box, and it is the node whose `next` must be redirected to the new front of the box that comes next. The **start** of the current box is the node the look-ahead begins at. The **full-block look-ahead** walks a probe forward up to `k` nodes without changing any link, counting the nodes. If fewer than `k` are found, the loop stops and the remaining nodes stay as they are. If `k` are found, the probe rests on the node after the box.

<!-- names: group predecessor, full-block look-ahead, reconnection pair -->

The flip itself is the standard reversal over `k` nodes, with one change: the reversed prefix starts as the probe node and not null, so that the box's old first node is already linked to the first node after the box when the flip ends. The **reconnection pair** is then handled in two assignments: the group predecessor is pointed at the new front of the box, or the head is updated when there is no predecessor, and the old first node of the box becomes the new group predecessor. The start moves to the probe.

The invariant is that everything before the start is final and correctly linked, everything from the start onward is untouched, and the look-ahead never modifies anything. Each node is visited a constant number of times, so the cost is O(n) time and O(1) extra space.

<!-- stage: variables -->
### Predecessor, Start, Probe And Count

The reference `before` is null until the first box is done. The reference `start` names the first node of the next box. The probe walks forward from `start`, and the counter `c` reaches `k` exactly when a full box exists. After the flip, `prev` heads the reversed box, and `start`, which has not changed, is its last node. When `k` is 1 each box is one node, so the list is unchanged. When `k` is larger than the list, the first look-ahead finds fewer than `k` nodes and nothing happens. The head changes only when the first box is flipped.

<!-- stage: trace -->
### Two Full Boxes And A Short Tail

Take the tags `9, 4, 7, 2, 8, 5, 3` with boxes of three. The first look-ahead starts at 9, walks over 9, 4 and 7, and rests on the node holding 2, so a full box exists. The box is reversed with the probe as the first link target, which makes the node holding 9 point at 2. There is no predecessor, so the head becomes the node holding 7, and the list reads 7, 4, 9, 2, 8, 5, 3. The node holding 9 becomes the predecessor and the start moves to 2. The second look-ahead covers 2, 8 and 5 and rests on 3. After the flip that box reads 5, 8, 2, and the predecessor, the node holding 9, is pointed at the node holding 5. The third look-ahead starts at 3 and finds only one node, so the loop stops, and the list reads 7, 4, 9, 5, 8, 2, 3.

A second run swaps exactly two nodes, the ones holding 7 and 1 in `4, 7, 1, 9`. The first node of the pair is pointed at the node after the pair, the second node is pointed at the first, and finally the node before the pair is pointed at the second. Until that last assignment the list from the head still skips the second node.

```trace
{"cells":[9,4,7,2,8,5,3],"pointers":["before","group"],"steps":[{"at":{"before":-1,"group":0},"vars":{"list":"7>4>9>2>8>5>3","found":3},"note":"The look-ahead finds 3 nodes after the group starting at the node holding 9, so the group is reversed with its tail pointed at the following node. The list now reads 7, 4, 9, 2, 8, 5, 3."},{"at":{"before":0,"group":3},"vars":{"list":"7>4>9>5>8>2>3","found":3},"note":"The look-ahead finds 3 nodes after the group starting at the node holding 2, so the group is reversed with its tail pointed at the following node. The list now reads 7, 4, 9, 5, 8, 2, 3."},{"at":{"before":3,"group":6},"vars":{"list":"7>4>9>5>8>2>3","found":1},"note":"The look-ahead from the node holding 3 finds only 1 node(s), fewer than 3, so the short suffix is left exactly as it is and the loop stops."}]}
```

```trace
{"cells":[4,7,1,9],"pointers":["before","first","second","after"],"steps":[{"at":{"before":0,"first":1,"second":2,"after":3},"vars":{"list":"4>7>1>9"},"note":"The pair to swap is the nodes holding 7 and 1. The node holding 4 stands before it and the node holding 9 comes after it."},{"at":{"before":0,"first":1,"second":2,"after":3},"vars":{"list":"4>7>9","second_chain":"1>9"},"note":"The first node of the pair is pointed at the node after the pair, so it no longer depends on the second node for the tail."},{"at":{"before":0,"first":1,"second":2,"after":3},"vars":{"second_chain":"1>7>9"},"note":"The second node is pointed at the first, so from the second node the order reads 1, 7, 9. The list from the head is still 4, 7, 9 because the node before has not been rewired."},{"at":{"before":0,"first":1,"second":2,"after":3},"vars":{"list":"4>1>7>9"},"note":"The node before the pair is pointed at the second node. The list now reads 4, 1, 7, 9 and all four nodes are reachable."}]}
```

<!-- stage: code -->
### Reverse A Range And Reverse Full Groups

```java
final class GroupReverse {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node swapPairAfter(Node head, int p) {
        Node before = null, first = head;
        for (int i = 0; i < p; i++) { before = first; first = first.next; }
        Node second = first.next;
        first.next = second.next;
        second.next = first;
        if (before == null) return second;
        before.next = second;
        return head;
    }

    static Node reverseGroups(Node head, int k) {
        Node before = null, start = head;
        while (true) {
            Node probe = start;
            int c = 0;
            while (probe != null && c < k) { probe = probe.next; c++; }
            if (c < k) break;
            Node prev = probe, curr = start;
            for (int i = 0; i < k; i++) {
                Node saved = curr.next;
                curr.next = prev;
                prev = curr;
                curr = saved;
            }
            if (before == null) head = prev; else before.next = prev;
            before = start;
            start = probe;
        }
        return head;
    }
}
```

The look-ahead and the flip each touch a box once, so the total is O(n) time and O(1) space. Seeding `prev` with the probe saves a separate line that would link the old first node to the rest.

<!-- stage: applicability -->
### Bounded Reversal Inside A Chain

Think of this pattern when only part of a chain must be reversed, either one stretch or every full block of a given size, and the pieces on both sides must remain attached. The invariant is that the nodes before the current start are final and linked, the nodes from the start on are untouched, and a flip happens only after a look-ahead has proved that a full block exists. Each block then needs the same three moves as a single reversal and two reconnections.

The false friend is the plan of flipping first and checking later. A short final block that has been flipped must be flipped back, and the code that does so has to find the block's start again. A second false friend is restarting from the head for every block, which looks harmless and costs a factor of n over k. A third is forgetting the head update when the first block is flipped, so the caller keeps a reference to a node that is now in the middle.

Do not use block reversal when the block boundaries depend on values and not counts, or when the structure is doubly linked and the back links need their own repair. In Java, count with an `int`, and note that for `k` larger than the list the look-ahead stops cleanly, while a missing guard on the probe would throw `NullPointerException`.

<!-- stage: exercises -->
### Exercises

#### [Build] Reverse Exactly Two Nodes (Author exercise)
<!-- id: ll-swap-pair -->

**Prerequisites.** The reverse lesson of this chapter.

**Problem.** A linked list is given by its values, together with a position `p`. Swap the node at position `p` with the node at position `p + 1`, counting from 0, by changing links and not values, and return the values of the resulting list.

**Constraints.** 2 <= n <= 10^5 and 0 <= p <= n - 2. Value copying is not allowed.

**Example 1.** Input `values = [4, 7, 1, 9]`, `p = 1`, output `[4, 1, 7, 9]`.

**Example 2.** Input `values = [2, 3]`, `p = 0`, output `[3, 2]`.

**Hint.** In what order must the three links be written so that the second node is not lost? What changes when there is no node before the pair?

**Changed decision.** First rung: the node before the pair is pointed at the new front last, and the head changes when the pair starts at position 0.

#### [Vary] Reverse A Half-Open Range (LeetCode 92)
<!-- id: ll-reverse-half-open -->

**Prerequisites.** The Reverse Exactly Two Nodes exercise above, and the reverse lesson.

**Problem.** Given a linked list and two integers `from` and `to`, reverse the nodes at positions `from` up to but not including `to`, counted from 0. If `to` is larger than the length, treat it as the length. If the range holds fewer than two nodes, leave the list unchanged. Return the values of the result.

**Constraints.** 0 <= n <= 10^5, 0 <= from <= to <= 10^9 and -10^9 <= value <= 10^9.

**Example 1.** Input `values = [5, 1, 7, 3, 8]`, `from = 1`, `to = 99`, output `[5, 8, 3, 7, 1]`.

**Example 2.** Input `values = [4, 6, 2]`, `from = 2`, `to = 2`, output `[4, 6, 2]`.

**Hint.** How many nodes are in the range after the clamp, and what does the segment tail point at when the range runs to the end of the list?

**Changed decision.** The positions are 0-based and half-open, and the upper end is clamped, so the length of the range is computed before the reversal starts.

#### [Boundary] Incomplete Final Group (Author exercise)
<!-- id: ll-first-full-group -->

**Prerequisites.** The two exercises above.

**Problem.** Given a linked list and a group size `k`, reverse only the first group of `k` nodes if the list contains at least `k` nodes, and otherwise leave the list unchanged. Return the values of the result.

**Constraints.** 0 <= n <= 10^5, 1 <= k <= 10^5 and -10^9 <= value <= 10^9. No link may be changed before it is certain that a full group exists.

**Example 1.** Input `values = [1, 2, 3, 4, 5]`, `k = 3`, output `[3, 2, 1, 4, 5]`.

**Example 2.** Input `values = [1, 2]`, `k = 3`, output `[1, 2]`.

**Hint.** What does the probe hold when it stops early? How is the list guaranteed untouched in that case?

**Changed decision.** A look-ahead runs before any link changes, so a short group is detected without needing to undo a flip.

#### [Recognize] Reverse Nodes in k-Group (LeetCode 25)
<!-- id: ll-reverse-k-group -->

**Prerequisites.** All three exercises above.

**Problem.** You receive the head of a linked list and an integer `k`; reverse the nodes of the list `k` at a time and return the modified list. Nodes left over at the end, fewer than `k`, stay as they are. Only the links may change, not the values.

**Constraints.** 1 <= k <= n <= 5000 and 0 <= value <= 1000.

**Example 1.** Input `values = [2, 4, 6, 8, 10, 12]`, `k = 4`, output `[8, 6, 4, 2, 10, 12]`.

**Example 2.** Input `values = [9, 4, 7, 2, 8, 5, 3]`, `k = 3`, output `[7, 4, 9, 5, 8, 2, 3]`.

**Hint.** What does the last node of a flipped group point at afterwards, and which node becomes the group predecessor for the next group?

**Changed decision.** The bounded reversal is repeated while full groups remain, and each group is linked to both neighbours before the next look-ahead begins.
