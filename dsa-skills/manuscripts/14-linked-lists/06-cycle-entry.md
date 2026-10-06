<!-- lesson-kind: standard -->
<!-- lesson-id: cycle-entry -->
## Find Where A Cycle Starts

<!-- stage: context -->
### Why The Job Chain Never Finishes

A scheduler stores each job's follow-up job in a `next` field and runs jobs by following that field until it reaches `null`. One night a bad update points the follow-up of job 40 back at job 12. The scheduler runs jobs 12 to 40 again and again, and it never reaches `null`. No error appears, and the machine stays busy until someone kills the process.

A traversal of a list assumes that the chain ends. A chain that returns to an earlier node breaks that assumption, and a simple loop cannot tell the two cases apart. This lesson asks how a method can detect the return, and how it can name the node where the return begins, without a large memory cost.

<!-- stage: naive -->
### Remembering Every Visited Node

The direct plan records each node the walk has seen. If the walk reaches a node that is already recorded, the chain has a cycle, and that node is where the cycle starts.

```java
final class CycleBySet {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node firstRepeated(Node start) {
        Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());   // compares nodes by identity
        for (Node c = start; c != null; c = c.next) {
            if (!seen.add(c)) return c;      // add returns false when the node is already recorded
        }
        return null;                         // the walk reached null, so no cycle exists
    }
}
```

On the chain `3, 2, 0, -4`, where the last node points back at the node 2, the method returns the node 2. On a chain that ends in `null`, it returns `null`. The set compares nodes by identity, because two different nodes can hold the same value.

<!-- stage: bottleneck -->
### Measuring The Memory

```predict
The set method visits each node once. What does it cost in time and extra memory for a chain of n nodes, and which of the two costs can a smarter method remove?

The method costs O(n) time and O(n) extra memory, because the set holds every node it has seen. A smarter method can keep the O(n) time and cut the extra memory to O(1).
```

The time is already as good as a walk can be, since any method must visit every node once to see the whole chain. The memory is the problem. A chain of ten million nodes needs a set with ten million entries, and each entry costs far more than one reference. A memory-limited program cannot afford that, and the problem statement often says so.

The method needs a way to notice a repeat without writing down the nodes it has seen. Two walkers on the same chain give such a way, and the next section explains why.

<!-- stage: insight -->
### Two Pointers At Different Speeds

Start two references at the head. The **slow pointer** moves one node per step. The **fast pointer** moves two nodes per step. If the chain ends in `null`, the fast pointer reaches `null` first, and the method answers that no cycle exists. If the chain has a cycle, the fast pointer enters it and stays inside it, and the slow pointer enters it later.

#### Why The Two Pointers Must Meet

Inside the cycle, the fast pointer gains one node on the slow pointer per step, because it moves two nodes while the slow pointer moves one. The gap around the cycle shrinks by exactly 1 each step, so it passes through every value down to 0. The gap cannot jump over 0, and a gap of 0 means both pointers hold the same node. The pointers therefore meet within one cycle length of steps after the slow pointer enters the cycle.

<!-- names: slow pointer, fast pointer, cycle entry -->

#### Finding The Cycle Entry

The **cycle entry** is the first node of the cycle that a walk from the head reaches. Let `a` be the number of nodes before the cycle entry, and let `L` be the number of nodes in the cycle. The slow pointer has moved `t` steps at the meeting, and the fast pointer has moved `2t`. Both are in the cycle, and they differ by whole turns of the cycle, so `2t - t = t` is a multiple of `L`. The slow pointer is therefore `t - a` steps past the cycle entry, and `t` is a multiple of `L`.

Now start a second reference at the head and a third reference at the meeting node. Move both one step at a time. After `a` steps the reference from the head reaches the cycle entry. The reference from the meeting node has moved `a` more steps, so it is `t - a + a = t` steps past the cycle entry. Because `t` is a multiple of `L`, that position is the cycle entry. The two references meet at the cycle entry, and the method returns that node.

#### Measuring The Cycle Length

The length `L` follows from the meeting node alone. Walk one reference around the cycle until it returns to the meeting node, and count the steps. The count is `L`, because the cycle has no branch.

<!-- stage: variables -->
### The References In The Cycle Method

- **slow** holds the node reached by moving 1 node per turn, starting at the head.
- **fast** holds the node reached by moving 2 nodes per turn, starting at the head.
- **meet** holds the node where `slow` and `fast` are equal, which lies inside the cycle.
- **walker** holds a second reference that starts at the head and moves one step per turn in the entry phase.
- **a** is the number of nodes before the cycle entry, and **L** is the number of nodes in the cycle.

<!-- stage: trace -->
### Meeting Inside, Then Meeting At The Entry

Here a pointer outside the cells is `null`.

#### Detecting A Cycle On Four Nodes

Take the chain `3, 2, 0, -4`, where the node -4 points back at the node 2. The pointers `slow` and `fast` both start at the node 3. The variable `moved` counts the steps the slow pointer has made.

```trace
{"cells":[3,2,0,-4],"pointers":["slow","fast"],"steps":[{"at":{"slow":0,"fast":0},"vars":{"moved":0},"note":"Start: both pointers hold the node 3."},{"at":{"slow":1,"fast":2},"vars":{"moved":1},"note":"slow moves 1 and fast moves 2. slow holds the node 2 and fast holds the node 0."},{"at":{"slow":2,"fast":1},"vars":{"moved":2},"note":"slow moves 1 and fast moves 2. slow holds the node 0 and fast holds the node 2."},{"at":{"slow":3,"fast":3},"vars":{"moved":3},"note":"slow moves 1 and fast moves 2. Both hold the node -4, so the references are equal and a cycle exists."}]}
```

The pointers meet inside the cycle, at the node reported in the last step. A chain without a cycle never produces equal pointers, because the fast pointer reaches `null` first.

#### Finding The Entry On Six Nodes

Take the chain `1, 2, 3, 4, 5, 6`, where the node 6 points back at the node 3. The cycle holds the four nodes `3, 4, 5, 6`, and two nodes come before it. The pointer `meet` starts at the meeting node found by the first phase. The pointer `walker` starts at the head.

```trace
{"cells":[1,2,3,4,5,6],"pointers":["meet","walker"],"steps":[{"at":{"meet":4,"walker":0},"vars":{"steps":0},"note":"Start: meet holds the node 5, found by the first phase, and walker holds the head, the node 1."},{"at":{"meet":5,"walker":1},"vars":{"steps":1},"note":"Both move one node. walker holds the node 2 and meet holds the node 6."},{"at":{"meet":2,"walker":2},"vars":{"steps":2},"note":"Both move one node. walker holds the node 3 and meet holds the node 3. Both hold the same node, so this node is the cycle entry."}]}
```

Both references move one node per step. After two steps `walker` reaches the node 3, and `meet` reaches the node 3 in the same step. The method returns that node.

<!-- stage: code -->
### Detecting And Locating In Code

```java
final class CycleEntry {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node meetingNode(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {   // test both, because fast.next.next reads one node further
            slow = slow.next;                         // one step
            fast = fast.next.next;                    // two steps
            if (slow == fast) return slow;            // equal references mean a node inside the cycle
        }
        return null;                                  // the fast pointer reached null, so no cycle exists
    }

    static Node cycleEntry(Node head) {
        Node meet = meetingNode(head);
        if (meet == null) return null;
        Node walker = head;
        while (walker != meet) {                      // both references move one step at a time
            walker = walker.next;
            meet = meet.next;
        }
        return walker;                                // the first node of the cycle
    }

    static int cycleLength(Node head) {
        Node meet = meetingNode(head);
        if (meet == null) return 0;
        int length = 1;
        for (Node c = meet.next; c != meet; c = c.next) length++;   // one full turn back to the meeting node
        return length;
    }
}
```

The loop condition tests `fast != null` first and `fast.next != null` second, so `fast.next.next` never dereferences `null`. The comparisons use `==`, which compares node identity, and never use `equals` or the values.

- **Time** is O(n), because the first phase takes at most `a + L` steps and the second takes `a` steps.
- **Space** is O(1), because the walk needs no collection of visited nodes.

<!-- stage: applicability -->
### Using The Two-Speed Rule

#### Stating What The Meeting Proves

The invariant of the first phase is that both pointers stay on the chain until the fast pointer reaches `null` or the pointers are equal. Equal pointers prove a cycle, and a `null` on the fast side proves the chain ends. No other outcome exists.

#### Separating Identity From Value

The false friend here is the node value, which says nothing about identity. A chain such as `1, 2, 1, 2` has repeated values and no cycle. A cycle exists only when a `next` field points back at a node that was already on the walk. Compare references with `==`.

#### Guarding The Pointers

A self-loop is a single node whose `next` is that same node, and a two-node cycle has two nodes pointing at each other. Both cycles are caught by the same loop, as the exercises show. Each read of `fast.next.next` needs `fast` and `fast.next` to be non-null, and the loop condition checks them in that order.

<!-- stage: exercises -->
### Exercises

#### [Build] Linked List Cycle (LeetCode 141)
<!-- id: ll-cycle-detect -->

**Prerequisites.** The slow pointer and the fast pointer from this lesson.

**Problem.** A linked list has a cycle if some node can be reached again by following `next` references from the head. Given the head of a list, return `true` if the list has a cycle and `false` otherwise. Use one step for the slow pointer and two steps for the fast pointer, and use no extra collection.

**Constraints.** The limits are:
- **Length** is between 0 and 10^4 nodes.
- **Values** satisfy `-10^5 <= val <= 10^5`, and values may repeat.
- **Answer** is a `boolean`.
- **Mutation** does not occur; no field changes.

**Example 1.** Input `3, 2, 0, -4` with the last node pointing at the node 2, output `true`.

**Example 2.** Input `1, 2, 1, 2` ending in `null`, output `false`, because repeated values are not repeated nodes.

**Hint.** What does the fast pointer hold when the chain ends? What must be non-null before the fast pointer moves twice?

**Changed decision.** Two speeds replace a set of visited nodes.

#### [Vary] Measure Cycle Length (Author exercise)
<!-- id: ll-cycle-length -->

**Prerequisites.** The exercise above.

**Problem.** Given the head of a list, return the number of nodes in its cycle, or 0 if the list has no cycle. The nodes before the cycle entry do not count. First find a node inside the cycle with the two-speed walk. Then walk once around the cycle and count the nodes.

**Constraints.** The limits are:
- **Length** is between 0 and 10^4 nodes.
- **Values** satisfy `-10^5 <= val <= 10^5`.
- **Answer** is an `int` between 0 and the number of nodes.
- **Mutation** does not occur.

**Example 1.** Input `1, 2, 3, 4, 5, 6` with the node 6 pointing at the node 3, output 4.

**Example 2.** Input `7, 8, 9` ending in `null`, output 0.

**Hint.** Where does the loop start counting? When does the count stop?

**Changed decision.** The meeting node starts a count of one full turn.

#### [Boundary] Self-Loop And Two-Node Cycle (Author exercise)
<!-- id: ll-cycle-small -->

**Prerequisites.** The two exercises above.

**Problem.** Given the head of a list, return the number of steps the slow pointer makes before the slow pointer and the fast pointer first hold the same node, or -1 if they never meet. The slow pointer moves one node per step, and the fast pointer moves two nodes per step. The list may be empty, may hold one node, or may be a cycle of one or two nodes.

**Constraints.** The limits are:
- **Length** is between 0 and 100 nodes.
- **Cycle** is absent or enters the list at any node, including a node that points at itself.
- **Answer** is an `int`, either -1 or a positive step count.
- **Mutation** does not occur.

**Example 1.** Input a single node whose `next` is itself, output 1.

**Example 2.** Input two nodes `A` and `B` with `A.next = B` and `B.next = A`, output 2.

**Hint.** Which reads happen in each step? Which of them would throw on a single node with `next` equal to `null`?

**Changed decision.** The guard must protect two reads of `next` per step.

#### [Recognize] Linked List Cycle II (LeetCode 142)
<!-- id: ll-cycle-entry -->

**Prerequisites.** All three exercises above.

**Problem.** Given the head of a list, return the node where the cycle begins, or `null` if the list has no cycle. The cycle begins at the first node that a walk from the head reaches and that lies on the cycle. After the pointers meet, move one reference back to the head and move both references one step at a time until they are equal. Use constant extra memory.

**Constraints.** The limits are:
- **Length** is between 0 and 10^4 nodes.
- **Values** satisfy `-10^5 <= val <= 10^5`, and values may repeat.
- **Answer** is a node reference or `null`.
- **Mutation** does not occur.

**Example 1.** Input `3, 2, 0, -4` with the last node pointing at the node 2, output the node 2.

**Example 2.** Input `1, 2` with the node 2 pointing at the node 1, output the node 1.

**Hint.** If `a` nodes come before the cycle entry, where is the meeting node relative to the entry? What does moving `a` more steps do to it?

**Changed decision.** A reset to the head turns a meeting node into the entry.
