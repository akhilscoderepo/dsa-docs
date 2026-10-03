<!-- lesson-kind: standard -->
<!-- lesson-id: middle-nodes -->
## Middle Nodes

<!-- stage: context -->
### A Lantern Midway Along A Cable

A festival hangs its lanterns along one long cable. The lanterns are linked to each other by short ropes, and the only way to get from one lantern to another is to walk along the ropes from the first one. The organisers want to hang a banner on the lantern in the middle of the cable, so that the two halves of the festival are balanced. Nobody knows how many lanterns there are, and the cable is too long to count on a first walk and then walk again.

An electrician stands at the first lantern with a helper. They can walk, they can wave, and they can agree on speeds beforehand, but they cannot ring anybody at the far end to ask. The organisers also ask what to do when the number of lanterns is even, because then there are two lanterns in the middle, and the banner can only go on one of them.

<!-- stage: naive -->
### Copy Lanterns Into A List First

One way is to copy every lantern into an array list as the cable is walked, and then pick the one at position `n / 2`.

```java
final class MiddleByCopy {
    static final class Lantern {
        int id;
        Lantern next;
        Lantern(int id) { this.id = id; }
    }

    static Lantern middle(Lantern first) {
        java.util.ArrayList<Lantern> all = new java.util.ArrayList<>();
        for (Lantern l = first; l != null; l = l.next) all.add(l);
        return all.get(all.size() / 2);
    }
}
```

It is correct. For five lanterns it returns the third, and for six lanterns it returns the fourth, which is the later of the two middle ones.

<!-- stage: bottleneck -->
### One Pass, No Memory Needed

The copy uses O(n) extra memory, an array that holds a reference for every lantern, only to read one of its entries. A version that counts the lanterns first and then walks half of them needs no array, but it walks the cable twice: n steps to count and about n / 2 to reach the middle. When each step is costly, because the nodes are scattered in memory or loaded from storage, two traversals are noticeably slower than one, and when the cable can only be walked once, as with a stream of nodes, counting is not allowed at all.

A single traversal that finds the middle needs the answer to be implied by where the walker stands when the walk ends, without knowing the length ahead. Walkers that move at fixed speeds have exactly that property: if one walker moves twice as fast as another, then by the time the fast one arrives at the end, the slow one has covered half the distance, and no counter is needed. What remains to settle is where precisely the fast walker stops, and what that means for an even number of lanterns.

<!-- stage: insight -->
### Half The Speed Means Half The Distance

Use two references that start at the head. The reference `slow` advances one node per round and `fast` advances two. This **two-to-one ratio** guarantees that after `r` rounds, `slow` is `r` nodes from the head and `fast` is `2r` nodes from the head, so at the moment `fast` can go no further, `slow` is half way. Everything depends on the **stopping test** applied before each round. With the test `fast != null && fast.next != null`, the walk continues as long as `fast` can take two steps, and it stops when `fast` is null or on the last node.

<!-- names: two-to-one ratio, stopping test, middle convention -->

Applied to a list of odd length `2k + 1`, `fast` ends on the last node after `k` rounds, and `slow` is on the node with index `k`, the exact middle. Applied to a list of even length `2k`, `fast` ends as null after `k` rounds, and `slow` is on the node with index `k`, the later of the two middles. This choice is the **middle convention**. A different stopping test, `fast.next != null && fast.next.next != null`, stops one round earlier for even lists and leaves `slow` on the earlier middle, with the same result for odd lists. The convention must be chosen to match what the task asks for, and the test has to be written to match.

The cost is about n / 2 rounds, so O(n) time, and O(1) space.

<!-- stage: variables -->
### Slow, Fast And The Stop

The reference `slow` is the answer when the loop ends. The reference `fast` runs ahead and is allowed to become null. The test must read `fast` before it reads `fast.next`, so that a null `fast` ends the loop and never causes a null dereference. For a list with one node, `fast.next` is null at once, so `slow` stays at the head. For an empty list the head is null and the function returns null. The palindrome check later in the exercises also needs the end of the first half, so some versions keep a reference to the node before `slow`.

<!-- stage: trace -->
### Five Lanterns And Six Lanterns

Take five lanterns with the numbers `4, 8, 6, 3, 2`. Both walkers begin at the lantern holding 4. In round one, slow moves to 8 and fast moves to 6. In round two, slow moves to 6 and fast moves to 2, which is the last lantern. Fast has no successor, so the loop stops with slow on the lantern holding 6, exactly in the middle.

Now take six lanterns `3, 5, 2, 8, 1, 6`. After round one slow is on 5 and fast on 2, and after round two slow is on 2 and fast on 1. In round three slow moves to 8 and fast steps off the end and becomes null. The loop stops with slow on the lantern holding 8, the later of the two middle lanterns, 2 and 8. With the other stopping test, the loop would have stopped after round two, leaving slow on the earlier middle, 2.

```trace
{"cells":[4,8,6,3,2],"pointers":["slow","fast"],"steps":[{"at":{"slow":0,"fast":0},"vars":{"rounds":0},"note":"Both pointers start on the first lantern, holding 4."},{"at":{"slow":1,"fast":2},"vars":{"rounds":1},"note":"Round 1: slow steps once to the lantern holding 8, and fast steps twice and is on the lantern holding 6."},{"at":{"slow":2,"fast":4},"vars":{"rounds":2},"note":"Round 2: slow steps once to the lantern holding 6, and fast steps twice and is on the lantern holding 2. The loop stops because fast has no successor."}]}
```

```trace
{"cells":[3,5,2,8,1,6],"pointers":["slow","fast"],"steps":[{"at":{"slow":0,"fast":0},"vars":{"rounds":0},"note":"Both pointers start on the first lantern, holding 3."},{"at":{"slow":1,"fast":2},"vars":{"rounds":1},"note":"Round 1: slow steps once to the lantern holding 5, and fast steps twice and is on the lantern holding 2."},{"at":{"slow":2,"fast":4},"vars":{"rounds":2},"note":"Round 2: slow steps once to the lantern holding 2, and fast steps twice and is on the lantern holding 1."},{"at":{"slow":3,"fast":-1},"vars":{"rounds":3},"note":"Round 3: slow steps once to the lantern holding 8, and fast steps twice and is past the end. The loop stops because fast is null. Slow holds the second of the two middle lanterns."}]}
```

<!-- stage: code -->
### Two Conventions And A Palindrome Check

```java
final class MiddleCode {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node secondMiddle(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    static Node firstMiddle(Node head) {
        if (head == null) return null;
        Node slow = head, fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    static boolean isPalindrome(Node head) {
        Node firstHalfEnd = firstMiddle(head);
        if (firstHalfEnd == null) return true;
        Node prev = null, curr = firstHalfEnd.next;
        while (curr != null) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        boolean same = true;
        Node a = head, b = prev;
        while (b != null) {
            if (a.value != b.value) { same = false; break; }
            a = a.next;
            b = b.next;
        }
        curr = prev;
        prev = null;
        while (curr != null) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        firstHalfEnd.next = prev;
        return same;
    }
}
```

The loops each touch about half the nodes or less, so the whole check is O(n) time with O(1) extra space. The second half is reversed for comparison and restored afterwards, so the list leaves in its original state.

<!-- stage: applicability -->
### When The Length Is Not Known

Use two speeds when the middle, or any fixed fraction of the way along, is needed in one traversal. It appears in merge sort on lists, where a list is split at its middle, in palindrome checks, where the second half is compared with the first, and in reordering tasks that interleave the two halves. The invariant is that `fast` is always twice as far from the head as `slow`, so when `fast` can no longer take two steps, `slow` has crossed half of the nodes.

The false friend is the loop condition. A condition that checks only `fast.next != null` throws `NullPointerException` on even-length lists, where `fast` becomes null, and a condition that checks only `fast != null` throws when `fast` is the last node. A second false friend is ignoring the even case, since odd-length tests pass with either convention and the error appears only on the first even example. A third is assuming that the middle is where the data is balanced, when the nodes' values say nothing about position.

Do not use it to find the node at an arbitrary index or a quarter of the way along without adapting the speeds, and do not use it when the chain may loop, since fast would never reach null. In Java, the test order matters because the `&&` operator short-circuits, which is what protects the dereference.

<!-- stage: exercises -->
### Exercises

#### [Build] Odd-Length Middle (Author exercise)
<!-- id: ll-odd-middle -->

**Prerequisites.** The cycle entry lesson of this chapter, which introduced the two speeds.

**Problem.** A linked list of odd length is given by its values. Move `slow` one node and `fast` two nodes per round while `fast` has a successor, and return `[middleValue, rounds]`, where `middleValue` is the value at `slow` at the end and `rounds` is the number of rounds made.

**Constraints.** n is odd, 1 <= n <= 10^5 and -10^9 <= value <= 10^9.

**Example 1.** Input `values = [4, 8, 6, 3, 2]`, output `[6, 2]`.

**Example 2.** Input `values = [7]`, output `[7, 0]`.

**Hint.** Where is `fast` after `r` rounds, and on which node does it stand when the loop ends for an odd length?

**Changed decision.** First rung: the loop ends when `fast` is on the last node, and the number of rounds is half the distance to the end.

#### [Vary] Middle of the Linked List (LeetCode 876)
<!-- id: ll-middle-second -->

**Prerequisites.** The Odd-Length Middle exercise above.

**Problem.** Given the head of a singly linked list, return the middle node, and if there are two middle nodes, return the second one. Report the answer as the values from the returned node to the end of the list.

**Constraints.** 1 <= n <= 100 and 1 <= value <= 100.

**Example 1.** Input `values = [3, 5, 2, 8, 1, 6]`, output `[8, 1, 6]`.

**Example 2.** Input `values = [9, 4, 7]`, output `[4, 7]`.

**Hint.** With the stopping test `fast != null && fast.next != null`, what is `fast` when the loop ends on an even-length list?

**Changed decision.** For an even number of nodes the later middle is returned, so the loop continues while `fast` can still take two steps.

#### [Boundary] First Middle Contract (Author exercise)
<!-- id: ll-first-middle -->

**Prerequisites.** The two exercises above.

**Problem.** A list is given by its values. Return the value of the first of the two middle nodes when the length is even, and of the single middle node when it is odd. If the list is empty, return -1.

**Constraints.** 0 <= n <= 10^5 and 0 <= value <= 10^9, so -1 is never a real value.

**Example 1.** Input `values = [3, 5, 2, 8, 1, 6]`, output `2`.

**Example 2.** Input `values = [1]`, output `1`.

**Hint.** Which stopping test makes `fast` stop one round earlier on an even list? What does the test do on a list with one node?

**Changed decision.** The stopping test reads `fast.next` and `fast.next.next` before moving, which changes the answer only for even lengths.

#### [Recognize] Palindrome Linked List (LeetCode 234)
<!-- id: ll-palindrome-list -->

**Prerequisites.** All three exercises above, and the reverse lesson.

**Problem.** Given the head of a singly linked list, return whether the values of the list read the same from the front and from the back. Use O(n) time and O(1) extra space, and leave the list as it was found.

**Constraints.** 1 <= n <= 10^5 and 0 <= value <= 9.

**Example 1.** Input `values = [2, 7, 1, 7, 2]`, output `true`.

**Example 2.** Input `values = [4, 5, 5, 3]`, output `false`.

**Hint.** Which middle ends the first half, and what is reversed? What has to happen after the comparison so that the caller's list is unchanged?

**Changed decision.** The middle is found first, the second half is reversed for the comparison and restored afterwards, so that no extra array is used and the input is preserved.
