<!-- lesson-kind: standard -->
<!-- lesson-id: middle-nodes -->
## Find The Middle Node

<!-- stage: context -->
### Why Counting First Doubles The Disk Reads

A log archive stores a long sequence of records as a linked list, and each `next` call reads one page from disk. A worker must split the list into two halves so that two threads can process them. The first version counts the records with one walk, then walks half of the count to find the split point. The archive has two million records, and the disk reads show that the worker touches 3 million pages before it starts any real work.

The worker reads the first half of the list twice. A walk that could stop after one pass would save a third of the reads. This lesson asks how to find the split point of a list in a single pass, when no length is known in advance.

<!-- stage: naive -->
### Counting The Nodes Before Splitting

The direct plan walks the whole list to count the nodes, then walks again for half of the count.

```java
final class SplitByCount {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node halfWayNode(Node head) {
        int n = 0;
        for (Node c = head; c != null; c = c.next) n++;    // first walk: n hops
        Node c = head;
        for (int i = 0; i < n / 2; i++) c = c.next;        // second walk: n / 2 hops
        return c;
    }
}
```

On `1, 2, 3, 4, 5` the method counts 5 and then takes 2 hops, so it returns the node 3. On `1, 2, 3, 4` it counts 4 and takes 2 hops, so it returns the node 3, the second of the two central nodes.

<!-- stage: bottleneck -->
### Counting The Hops

```predict
For a list of n nodes, how many next hops does the count-then-walk method follow in total, and how many hops would a method need that finds the split point while it walks the list once?

The method follows n hops to count and about n / 2 hops to walk, so about 3n / 2 hops in total, which is still O(n). A single pass that stops at the end needs only n hops.
```

The big-O class does not change, and the constant does. When each hop is a disk read or a network call, the extra half is half a pass of real cost. The method also needs a second traversal that starts from the head, which a read-once source cannot offer.

The method needs a position that moves half as far as the end of the list, without knowing where the end is. Two references that move at different speeds provide that.

<!-- stage: insight -->
### Moving Two References At Different Speeds

Start two references at the head. The **slow** reference moves one node per step, and the **fast** reference moves two nodes per step. The fast reference reaches the end when the slow reference has moved half as far, so the slow reference stands on the center of the list when the loop stops.

#### Where The References Stand After k Steps

After `k` steps the slow reference is at index `k` and the fast reference is at index `2k`, counting the head as index 0, as long as the fast reference has not fallen off the end. The loop stops when the fast reference cannot take another double step. For a list of `n` nodes that happens at `k = n / 2` when `n` is even, and at `k = (n - 1) / 2` when `n` is odd. In both cases the slow reference is at index `n / 2` using integer division.

<!-- names: first middle, second middle, middle node -->

#### One Middle Node Or Two

A list with an odd number of nodes has one **middle node**, the node with the same number of nodes on each side. A list with an even number of nodes has two central nodes. The **first middle** is the one at index `n / 2 - 1`, and the **second middle** is the one at index `n / 2`. The statement of a problem must say which one it wants.

#### Choosing The Loop Test

The loop test `fast != null && fast.next != null` lets the fast reference take a double step only if both nodes exist. It stops with the fast reference past the end for an even `n`, so the slow reference is at the second middle. The test `fast.next != null && fast.next.next != null` stops one step earlier for an even `n`, so the slow reference stays on the first middle. For an odd `n`, both tests leave the slow reference on the single middle node.

<!-- stage: variables -->
### The References In The Middle Search

- **slow** holds the node at index `k` after `k` steps, starting at the head.
- **fast** holds the node at index `2k` after `k` steps, starting at the head.
- **n** is the number of nodes in the list, and the methods never compute it.
- **k** is the number of steps taken, which ends at `n / 2` or `(n - 1) / 2`.

<!-- stage: trace -->
### Reading The Center In One Pass

Below, `null` appears as a pointer that is not above any cell.

#### Odd Length With Five Nodes

Take the list `10, 20, 30, 40, 50`. The pointers `slow` and `fast` start at the node 10. The variable `steps` counts the loop turns.

```trace
{"cells":[10,20,30,40,50],"pointers":["slow","fast"],"steps":[{"at":{"slow":0,"fast":0},"vars":{"steps":0},"note":"Start: slow and fast both hold the node 10."},{"at":{"slow":1,"fast":2},"vars":{"steps":1},"note":"slow moves 1 and fast moves 2. slow holds the node 20, and fast holds the node 30."},{"at":{"slow":2,"fast":4},"vars":{"steps":2},"note":"slow moves 1 and fast moves 2. slow holds the node 30, and fast holds the node 50."},{"at":{"slow":2,"fast":4},"vars":{"steps":2},"note":"The loop test fails, so the loop stops. slow holds the node 30."}]}
```

After two turns the fast reference is on the last node, and the next double step is impossible. The slow reference is on the node 30, which has two nodes on each side.

#### Even Length With Six Nodes

Now take the list `1, 2, 3, 4, 5, 6` and the loop test that allows a double step when the fast reference and its successor exist.

```trace
{"cells":[1,2,3,4,5,6],"pointers":["slow","fast"],"steps":[{"at":{"slow":0,"fast":0},"vars":{"steps":0},"note":"Start: slow and fast both hold the node 1."},{"at":{"slow":1,"fast":2},"vars":{"steps":1},"note":"slow moves 1 and fast moves 2. slow holds the node 2, and fast holds the node 3."},{"at":{"slow":2,"fast":4},"vars":{"steps":2},"note":"slow moves 1 and fast moves 2. slow holds the node 3, and fast holds the node 5."},{"at":{"slow":3,"fast":-1},"vars":{"steps":3},"note":"slow moves 1 and fast moves 2. slow holds the node 4, and fast holds null."},{"at":{"slow":3,"fast":-1},"vars":{"steps":3},"note":"The loop test fails, so the loop stops. slow holds the node 4."}]}
```

After three turns the fast reference has fallen off the end, and the slow reference is on the node 4. That node is the second middle, because three nodes come before it and two come after it.

<!-- stage: code -->
### Two Loop Tests In Code

```java
final class MiddleNodes {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node secondMiddle(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {   // a double step needs both nodes
            slow = slow.next;                         // one step
            fast = fast.next.next;                    // two steps
        }
        return slow;                                  // the middle, or the second of two middles
    }

    static Node firstMiddle(Node head) {
        Node slow = head, fast = head;                // head must not be null
        while (fast.next != null && fast.next.next != null) {   // stop one step earlier for even lengths
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;                                  // the middle, or the first of two middles
    }
}
```

The method `secondMiddle` accepts an empty list and returns `null`. The method `firstMiddle` reads `fast.next` immediately, so it needs a non-empty list, and a caller with an empty list must test `head` first. In both methods the order of the two tests matters, because `&&` stops at the first false test and never evaluates the second.

- **Time** is O(n), because the fast reference makes at most `n` hops and the slow reference makes at most `n / 2`.
- **Space** is O(1), because the methods store two references.

<!-- stage: applicability -->
### Matching The Contract To The Loop

#### Stating What The Gap Means

The invariant of the search is that the fast reference has moved twice as many nodes as the slow reference. When the fast reference stops at the end, the slow reference has crossed half of the nodes. State this in a comment, and then write down which middle the problem wants.

#### Choosing Between Two Middles

The false friend of this pattern is an even-length list. The odd case has one answer, and an even case has two, so a loop that is right for one contract is wrong for the other by one node. A problem statement says "the second middle" or "the first middle" in a sentence, and the loop test follows from that sentence.

#### Using The Middle As A Split Point

A palindrome check, a merge sort and a balanced tree built from a sorted list all split a list at its center. Each needs the node before the split point or the node at it, and the choice of middle decides which half is longer.

<!-- stage: exercises -->
### Exercises

#### [Build] Odd-Length Middle (Author exercise)
<!-- id: ll-odd-middle -->

**Prerequisites.** The slow and fast references from this lesson.

**Problem.** A list has an odd number of nodes. Run the slow and fast references from the head, as described in this lesson, and return two results: the value of the middle node and the number of loop turns that ran. The loop stops when the fast reference or its successor is `null`.

**Constraints.** The limits are:
- **Length** is an odd number `n` with `1 <= n <= 10^5`.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Answer** is two `int` results.
- **Mutation** does not occur.

**Example 1.** Input `1, 2, 3, 4, 5`, output the value 3 after 2 turns.

**Example 2.** Input `7`, output the value 7 after 0 turns.

**Hint.** What does the fast reference hold when the loop stops? How does the number of turns relate to the index of the middle node?

**Changed decision.** Two references of different speeds replace a count and a second walk.

#### [Vary] Middle of the Linked List (LeetCode 876)
<!-- id: ll-second-middle -->

**Prerequisites.** The exercise above.

**Problem.** Given the head of a non-empty list, return the middle node of the list. If the list has two middle nodes, return the second one. The returned node is the head of the list that starts at the middle, so the caller reads the rest of the list from it.

**Constraints.** The limits are:
- **Length** is between 1 and 100 nodes.
- **Values** satisfy `1 <= val <= 100`.
- **Answer** is a node reference that is never `null`.
- **Mutation** does not occur.

**Example 1.** Input `1, 2, 3, 4, 5`, output the node 3 with the list `3, 4, 5`.

**Example 2.** Input `1, 2, 3, 4, 5, 6`, output the node 4 with the list `4, 5, 6`.

**Hint.** In an even-length list, where is the fast reference when the loop stops? Which loop test makes the slow reference land on the second middle?

**Changed decision.** The even-length case returns the second of the two middle nodes.

#### [Boundary] First Middle Contract (Author exercise)
<!-- id: ll-first-middle -->

**Prerequisites.** The two exercises above.

**Problem.** Given the head of a non-empty list, return the middle node. If the list has two middle nodes, return the first one. The loop must make the same number of turns as the previous exercise's loop for odd lengths and one fewer turn for even lengths. Change only the loop test.

**Constraints.** The limits are:
- **Length** is between 1 and 10^5 nodes.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Answer** is a node reference that is never `null`.
- **Mutation** does not occur.

**Example 1.** Input `1, 2, 3, 4`, output the node 2.

**Example 2.** Input `9`, output the node 9.

**Hint.** The fast reference should stop one double step earlier for even lengths. What two nodes must exist for a double step to be allowed?

**Changed decision.** The stopping condition changes so the slow reference stops one node earlier for even lengths.

#### [Recognize] Palindrome Linked List (LeetCode 234)
<!-- id: ll-palindrome -->

**Prerequisites.** All three exercises above and the reversal from the previous chapter lessons.

**Problem.** Given the head of a list, return `true` if the sequence of values reads the same from the front and from the back, and `false` otherwise. Use constant extra memory. Find the first middle, reverse the second half in place, compare the two halves, and then reverse the second half again. The list must have its original order when the method returns.

**Constraints.** The limits are:
- **Length** is between 1 and 10^5 nodes.
- **Values** satisfy `0 <= val <= 9`.
- **Answer** is a `boolean`.
- **Mutation** is allowed during the call, and the list must have its original order afterward.

**Example 1.** Input `1, 2, 2, 1`, output `true`.

**Example 2.** Input `1, 2, 3, 2`, output `false`, and the list still reads `1, 2, 3, 2`.

**Hint.** Which node ends the first half in an odd-length list? Which node starts the second half?

**Changed decision.** The middle node becomes the split point of a reverse-and-compare.
