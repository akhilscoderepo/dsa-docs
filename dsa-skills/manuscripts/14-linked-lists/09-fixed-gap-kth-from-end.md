<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-gap-kth-from-end -->
## Fixed-Gap Kth From End

<!-- stage: context -->
### Untying The Fourth Camel From The Rear

A desert caravan has camels tied nose to tail, each camel by a rope to the camel behind it. The guide walks at the front and can reach any camel only by following the ropes one by one. Today a camel that is exactly four places from the back has gone lame, and the guide has to untie it and rejoin the two ropes around it, so that the caravan goes on without it.

The difficulty is that the guide knows where the front of the caravan is and where the back is, but nobody has counted the camels, and the caravan is too long to see from end to end. Counting means walking all the way back and then all the way forward again. The guide would prefer to find the lame camel in a single walk. She also has to take care of the special day when the lame camel turns out to be the leader, because then there is no camel in front to rejoin the rope with.

<!-- stage: naive -->
### Count The Caravan, Then Walk Back In

The direct method counts all camels first, and then walks forward again by the number of camels minus the distance from the end.

```java
final class LameCamelByCount {
    static final class Camel {
        int tag;
        Camel next;
        Camel(int tag) { this.tag = tag; }
    }

    static Camel kthFromRear(Camel leader, int k) {
        int total = 0;
        for (Camel c = leader; c != null; c = c.next) total++;
        Camel cur = leader;
        for (int i = 0; i < total - k; i++) cur = cur.next;
        return cur;
    }
}
```

It is correct when `k` is between 1 and the number of camels. For the tags 4, 8, 6, 3, 2 and `k = 2` it returns the camel with tag 3.

<!-- stage: bottleneck -->
### Two Walks Where One Should Do

The method walks the whole caravan to count it and then walks again almost as far, so it makes about n + (n - k) steps, which is O(n) but with two traversals. When a step is expensive, because nodes are loaded from storage or spread across memory, the second traversal is a real cost. When the chain can be read only once, such as a stream of nodes, the count cannot be followed by a second walk at all.

The position that is wanted is defined relative to the end, and a walker who stands at the front has no way to see the end. A second walker would solve this if it could be placed so that, when it arrives at the end, it is exactly k places behind. Placing it needs only the number k, and no count. If one walker is sent ahead by k camels first, and the second follows, then the distance between the two stays equal to k for as long as they move together, and the moment the first one falls off the end tells the second where it is.

<!-- stage: insight -->
### Keep A Constant Distance

Use two references. The **lead pointer** advances `k` nodes alone, which creates the **fixed gap**: from now on it is exactly `k` nodes ahead of the other one. The **trailing pointer** starts at the head and stays there during that first stretch. Then both advance one node per round. Each round moves them equally, so the gap does not change. The loop ends when the lead pointer has run off the end, which is when it is null, and at that moment the trailing pointer stands on the `k`-th node from the end, since it is `k` nodes behind a position that is one past the last node.

<!-- names: lead pointer, fixed gap, trailing pointer -->

If the task needs the node before the target, as in a deletion, start the trailing pointer on a dummy node before the head and stop the lead on the last node instead, using the test `lead.next != null`. The gap is the same, and the trailing pointer now stands on the predecessor of the target. When `k` equals the length, the lead stops on the last node after exactly `k` advances, and the trailing pointer has not moved from the dummy, so the target is the original head and the same bypass removes it.

The invariant is that the trailing pointer is always `k` nodes behind the lead pointer, counting the dummy as a node. The cost is one traversal, O(n) time, and O(1) extra space. A value of `k` larger than the list must be detected while the lead advances, because the lead becomes null early.

<!-- stage: variables -->
### Lead, Trail And The Gap Of K

The integer `k` is the distance from the end, counted from 1 for the last node. The lead pointer advances `k` steps before the trailing pointer moves, and each of those steps must test that the lead is not null, since a `k` larger than the length ends the advance early and the request cannot be met. The trailing pointer is the answer. With a dummy it starts at the dummy and the lead starts at the dummy too, so that after `k` advances the lead is on the node with index `k - 1`. A list of length one with `k` equal to 1 leaves the lead on that node, with no successor.

<!-- stage: trace -->
### The Second Camel From The Rear

Take the camels `4, 8, 6, 3, 2` and `k = 2`. Both pointers start on the first camel. The lead pointer takes two steps alone and stands on the camel holding 6, with the trailing pointer still on 4. Then both move together. The lead goes to 3 and the trailing pointer to 8, then the lead goes to 2 and the trailing pointer to 6, and finally the lead goes past the last camel and the trailing pointer goes to 3. The gap was 2 throughout, and the trailing pointer stands on the camel that is second from the rear.

A second run removes the camel that is fifth from the rear of the same five, which is the leader. A dummy stands before the first camel, and both pointers start on it. The lead takes five steps and stands on the last camel, which has no successor, so the trailing pointer never moves from the dummy. The dummy is pointed past the first camel, and the list reads 8, 6, 3, 2, with no special case for removing the first camel.

```trace
{"cells":[4,8,6,3,2],"pointers":["lead","trail"],"steps":[{"at":{"lead":0,"trail":0},"vars":{"gap":0},"note":"Both pointers start on the first camel, holding 4. The lead pointer will run ahead by exactly 2 camels."},{"at":{"lead":1,"trail":0},"vars":{"gap":1},"note":"The lead pointer takes step 1 of 2 alone and stands on the camel holding 8. The trailing pointer has not moved."},{"at":{"lead":2,"trail":0},"vars":{"gap":2},"note":"The lead pointer takes step 2 of 2 alone and stands on the camel holding 6. The trailing pointer has not moved."},{"at":{"lead":3,"trail":1},"vars":{"gap":2},"note":"Both pointers move one camel. The lead is on the camel holding 3 and the trailing pointer is on the camel holding 8. The gap is still 2."},{"at":{"lead":4,"trail":2},"vars":{"gap":2},"note":"Both pointers move one camel. The lead is on the camel holding 2 and the trailing pointer is on the camel holding 6. The gap is still 2."},{"at":{"lead":5,"trail":3},"vars":{"gap":2},"note":"Both pointers move one camel. The lead is past the last camel and the trailing pointer is on the camel holding 3. The gap is still 2. The lead is past the end, so the trailing pointer stands on the second camel from the end."}]}
```

```trace
{"cells":[4,8,6,3,2],"pointers":["lead","trail"],"steps":[{"at":{"lead":-1,"trail":-1},"vars":{"list":"4>8>6>3>2"},"note":"Both pointers start on the dummy that stands before the first camel."},{"at":{"lead":0,"trail":-1},"vars":{"steps_taken":1},"note":"The lead pointer takes step 1 of 5 and stands on the camel holding 4."},{"at":{"lead":1,"trail":-1},"vars":{"steps_taken":2},"note":"The lead pointer takes step 2 of 5 and stands on the camel holding 8."},{"at":{"lead":2,"trail":-1},"vars":{"steps_taken":3},"note":"The lead pointer takes step 3 of 5 and stands on the camel holding 6."},{"at":{"lead":3,"trail":-1},"vars":{"steps_taken":4},"note":"The lead pointer takes step 4 of 5 and stands on the camel holding 3."},{"at":{"lead":4,"trail":-1},"vars":{"steps_taken":5},"note":"The lead pointer takes step 5 of 5 and stands on the camel holding 2."},{"at":{"lead":4,"trail":-1},"vars":{"list":"4>8>6>3>2"},"note":"The lead is on the last camel, which has no successor, so the trailing pointer never moves. It stays on the dummy, and the camel after the dummy is the one to remove."},{"at":{"lead":4,"trail":-1},"vars":{"list":"8>6>3>2"},"note":"The dummy is pointed past the camel holding 4. The list now reads 8, 6, 3, 2, and the original first camel was removed by the same bypass used anywhere else."}]}
```

<!-- stage: code -->
### Kth From The End, Predecessor And Removal

```java
final class GapCode {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node kthFromEnd(Node head, int k) {
        Node lead = head, trail = head;
        for (int i = 0; i < k; i++) {
            if (lead == null) return null;
            lead = lead.next;
        }
        while (lead != null) {
            lead = lead.next;
            trail = trail.next;
        }
        return trail;
    }

    static Node removeKthFromEnd(Node head, int k) {
        Node dummy = new Node(0);
        dummy.next = head;
        Node lead = dummy, trail = dummy;
        for (int i = 0; i < k; i++) {
            lead = lead.next;
            if (lead == null) return head;
        }
        while (lead.next != null) {
            lead = lead.next;
            trail = trail.next;
        }
        trail.next = trail.next.next;
        return dummy.next;
    }
}
```

Each method makes one pass, so both take O(n) time with O(1) extra space. In the second method the check `lead == null` after the advance catches a `k` larger than the length, and it returns the list unchanged.

<!-- stage: applicability -->
### When Position Is Counted From The End

Use a fixed gap when a node is named by its distance from the end, or when a window of fixed width must trail a pointer that scans, and one traversal is wanted. The invariant is that, after the lead has advanced `k` nodes, the trailing pointer stays exactly `k` nodes behind it, so that when the lead reaches the end the trailing pointer is at the required offset.

The false friend is the speed ratio of the previous lesson. Two speeds find a fraction of the way along, such as the middle, and a fixed gap finds an offset from the end, and the two are easy to confuse because both use two pointers. A second false friend is advancing the lead without a null check, which throws when `k` exceeds the length. A third is stopping the lead at null when the task needs the predecessor, which leaves the trailing pointer one node too far.

Do not use a gap when the offset is from the front, where a plain walk suffices, and do not rely on it when the chain can be changed between the two pointers' moves by other code. In Java, name the two references by role, check `lead` before each dereference in the first stretch, and when deleting use a dummy so that removing the head needs no branch.

<!-- stage: exercises -->
### Exercises

#### [Build] Kth Node From End (Author exercise)
<!-- id: ll-kth-from-end -->

**Prerequisites.** The dummy heads and middle nodes lessons of this chapter.

**Problem.** A linked list is given by its values, together with an integer `k` with `1 <= k <= n`. Return the value of the `k`-th node from the end, where `k = 1` is the last node. Create a gap of `k` nodes and then move both pointers together.

**Constraints.** 1 <= k <= n <= 10^5 and -10^9 <= value <= 10^9.

**Example 1.** Input `values = [4, 8, 6, 3, 2]`, `k = 2`, output `3`.

**Example 2.** Input `values = [5]`, `k = 1`, output `5`.

**Hint.** How far ahead must the lead pointer be, and where is it when the trailing pointer is on the answer?

**Changed decision.** First rung: the lead pointer runs `k` steps alone, and the walk ends when the lead is null.

#### [Vary] Predecessor Of Kth From End (Author exercise)
<!-- id: ll-predecessor-kth -->

**Prerequisites.** The Kth Node From End exercise above.

**Problem.** For the same input, return the value of the node that comes immediately before the `k`-th node from the end, or -1 if the `k`-th node from the end is the first node of the list.

**Constraints.** 1 <= k <= n <= 10^5 and 0 <= value <= 10^9, so -1 is never a real value.

**Example 1.** Input `values = [4, 8, 6, 3, 2]`, `k = 2`, output `6`.

**Example 2.** Input `values = [5, 9]`, `k = 2`, output `-1`.

**Hint.** Where must the trailing pointer start so that it ends one node earlier? How is a result for the first node represented?

**Changed decision.** The trailing pointer starts on a dummy before the head, and the lead stops on the last node, so the trailing pointer ends on the predecessor.

#### [Boundary] K Equals Length (Author exercise)
<!-- id: ll-k-too-large -->

**Prerequisites.** The two exercises above.

**Problem.** Given a list by its values and an integer `k >= 1`, remove the `k`-th node from the end in one pass and return the values of the resulting list. If `k` is larger than the length of the list, return the list unchanged. When `k` equals the length, the first node is removed.

**Constraints.** 0 <= n <= 10^5, 1 <= k <= 2 * 10^5 and -10^9 <= value <= 10^9. The length may not be counted.

**Example 1.** Input `values = [4, 8, 6]`, `k = 3`, output `[8, 6]`.

**Example 2.** Input `values = [4, 8]`, `k = 5`, output `[4, 8]`.

**Hint.** What does the lead pointer become when `k` is larger than the length, and what must the code do then? What does the trailing pointer hold when `k` equals the length?

**Changed decision.** The null check inside the first stretch detects an oversized `k`, and a dummy makes the removal of the first node an ordinary bypass.

#### [Recognize] Remove Nth Node From End of List (LeetCode 19)
<!-- id: ll-remove-nth-gap -->

**Prerequisites.** All three exercises above, and the dummy heads lesson.

**Problem.** Remove the `n`-th node from the end of a linked list in a single pass, and return a pair: the value that was removed, or -1 if `n` is larger than the length and nothing was removed, and the values of the resulting list.

**Constraints.** 1 <= length <= 30, 1 <= n <= 60 and 0 <= value <= 100.

**Example 1.** Input `values = [9, 1, 7, 2]`, `n = 3`, output `[1, [9, 7, 2]]`.

**Example 2.** Input `values = [5, 6]`, `n = 3`, output `[-1, [5, 6]]`.

**Hint.** After the removal, which node still holds the removed value so that it can be reported? Where in the code is the oversized `n` detected?

**Changed decision.** The removal is done in one pass with a fixed gap, and the contract reports the removed value and tolerates an `n` larger than the list.
