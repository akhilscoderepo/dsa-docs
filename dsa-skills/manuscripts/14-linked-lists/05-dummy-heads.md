<!-- lesson-kind: standard -->
<!-- lesson-id: dummy-heads -->
## Use A Dummy Node At The Head

<!-- stage: context -->
### Why The First Item Refuses To Go

A playlist stores songs in a list, and the delete button removes every song with a chosen title. A developer writes a loop that walks the list and unlinks each matching song from the song before it. The delete works on the fifth song, the ninth song and the last song. It does nothing on the first song, because the first song has no song before it, and the playlist variable still points at it. The user clicks the button, and the first song stays.

The developer adds a special branch for the first song, and the next feature, inserting a song at the front, needs the same branch again. Each operation that can change the first node now carries two cases. The goal is to write one rule that works at every position, including the first.

<!-- stage: naive -->
### Handling The First Node Separately

The direct fix moves the head forward while it matches, and then runs the usual loop for the rest of the list.

```java
final class RemoveWithBranch {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node removeAll(Node first, int target) {
        while (first != null && first.val == target) {   // case 1: the first node itself matches
            first = first.next;
        }
        Node before = first;
        while (before != null && before.next != null) {  // case 2: later nodes unlink from the node before them
            if (before.next.val == target) before.next = before.next.next;
            else before = before.next;
        }
        return first;
    }
}
```

On `7, 7, 3, 7, 4` with target 7 the method returns `3, 4`. It is correct, and it needs two loops with two different rules.

<!-- stage: bottleneck -->
### Counting The Cases

```predict
Both loops run in O(n) total time. If a program has k list operations that can change the first node, how many separate cases must a reviewer test, and what grows with k?

Each operation has two cases, a change at the first node and a change later, so a reviewer tests 2k cases. The time stays O(n), and the number of places for a bug to hide grows with k.
```

The cost is not time. The two loops together visit each node once, so the method is O(n). The cost is the number of rules. The first loop changes the variable `first`, and the second loop changes a `next` field. A test suite must cover an empty list, a list whose first node matches, a list where every node matches, and a list where only a later node matches. A missing case returns a wrong head or loses a node.

If the first node had a node before it, one rule would cover every node. The structure has no such node, so the next section adds one.

<!-- stage: insight -->
### Giving The First Node A Predecessor

A **dummy node** is an extra node placed before the real first node. It holds no meaningful value, and the method never reads that value. Its field `next` always points at the current head of the real list. The method builds the dummy once with `new Node(0, head)`.

#### One Rule For Every Node

Every real node now has a **predecessor**, the node whose `next` field points at it. For the first real node, the predecessor is the dummy node. To remove or insert at any position, the method writes the `next` field of the predecessor, and that single write works at the first position too. The branch for the first node disappears.

<!-- names: dummy node, predecessor, tail -->

#### The Returned Head Lives In One Place

After any change, the correct head is `dummy.next`. The method returns that field and never the old `head` variable, because the old head may have been removed. This is the property that makes the dummy node worth its one allocation. A method that builds a result chain keeps a **tail**, the last node of the finished part of the result, and the dummy node is the first tail. Each new node attaches with `tail.next = node`, and the first node needs no extra branch.

#### When A Dummy Node Does Not Help

If the head never changes, the extra node adds nothing. Counting nodes, searching for a value and reading a node's successor all leave the head alone. Use a dummy node when the first node can be inserted, removed or replaced.

<!-- stage: variables -->
### The References With A Dummy Node

- **dummy** holds the extra node placed before the head, and `dummy.next` is always the current head.
- **prev** holds the predecessor of the node under inspection, starting at `dummy`.
- **curr** holds the node under inspection, which is `prev.next`.
- **tail** holds the last node of a result that is being built, starting at `dummy`.
- **return value** is `dummy.next`, which is the head after every change.

<!-- stage: trace -->
### One Rule At Every Position

A pointer drawn outside the cells stands for `null`. In both traces the first cell is the dummy node, and its value 0 is never read.

#### Removing Every 7

Take the list `7, 7, 3, 7, 4` and the target 7. The pointer `prev` marks the predecessor of the node under inspection, and `curr` marks that node. The variable `result` shows the real list, read from `dummy.next`.

```trace
{"cells":[0,7,7,3,7,4],"pointers":["prev","curr"],"steps":[{"at":{"prev":0,"curr":1},"vars":{"result":"7,7,3,7,4"},"note":"Start: prev is the dummy node, and curr is the first real node, 7."},{"at":{"prev":0,"curr":2},"vars":{"result":"7,3,7,4"},"note":"The node 7 matches, so prev.next skips it. prev stays where it is."},{"at":{"prev":0,"curr":3},"vars":{"result":"3,7,4"},"note":"The node 7 matches, so prev.next skips it. prev stays where it is."},{"at":{"prev":3,"curr":4},"vars":{"result":"3,7,4"},"note":"The node 3 does not match, so prev moves onto it."},{"at":{"prev":3,"curr":5},"vars":{"result":"3,4"},"note":"The node 7 matches, so prev.next skips it. prev stays where it is."},{"at":{"prev":5,"curr":-1},"vars":{"result":"3,4"},"note":"The node 4 does not match, so prev moves onto it."}]}
```

The two matching nodes at the front go through the same write as the matching node in the middle. The write is `prev.next = curr.next`, and `prev` stays on the dummy node until a node is kept.

#### Merging Behind A Dummy Tail

Now merge the sorted lists `2, 5` and `1, 6`. The pointers `a` and `b` mark the first unplaced node of each list, and `tail` marks the last node of the result. The variable `result` shows the real result, read from `dummy.next`.

```trace
{"cells":[0,2,5,1,6],"pointers":["a","b","tail"],"steps":[{"at":{"a":1,"b":3,"tail":0},"vars":{"result":"empty"},"note":"Start: tail is the dummy node, and the result is empty."},{"at":{"a":1,"b":4,"tail":3},"vars":{"result":"1"},"note":"The smaller head is the node 1. tail.next attaches it with the same write the first node needed."},{"at":{"a":2,"b":4,"tail":1},"vars":{"result":"1,2"},"note":"The smaller head is the node 2. tail.next attaches it with the same write the first node needed."},{"at":{"a":-1,"b":4,"tail":2},"vars":{"result":"1,2,5"},"note":"The smaller head is the node 5. tail.next attaches it with the same write the first node needed."},{"at":{"a":-1,"b":-1,"tail":2},"vars":{"result":"1,2,5,6"},"note":"One list is empty. One write attaches the leftover 6, and the method returns dummy.next."}]}
```

The first node of the answer attaches exactly like every later node. The method needs no step that chooses the head before the loop.

<!-- stage: code -->
### Using A Dummy Node In Code

```java
final class DummyHead {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node removeAll(Node head, int target) {
        Node dummy = new Node(0, head);          // the value 0 is never read
        Node prev = dummy;                       // the predecessor of the node under inspection
        while (prev.next != null) {
            if (prev.next.val == target) prev.next = prev.next.next;   // unlink the match
            else prev = prev.next;               // keep the node and move on
        }
        return dummy.next;                       // the head, even when the old head was removed
    }

    static Node merge(Node a, Node b) {
        Node dummy = new Node(0, null);
        Node tail = dummy;                       // the finished part of the result starts empty
        while (a != null && b != null) {
            if (b.val < a.val) { tail.next = b; b = b.next; }
            else { tail.next = a; a = a.next; }  // attach the smaller head; ties keep a first
            tail = tail.next;
        }
        tail.next = (a != null) ? a : b;         // one write attaches the leftover nodes
        return dummy.next;
    }
}
```

The dummy node costs one allocation per call. It removes the head branch from `removeAll` and the head choice from `merge`, and the empty-list case needs no extra code.

- **Time** is O(n) for `removeAll` and O(m + n) for `merge`, because each node is handled once.
- **Space** is O(1), because the method allocates one dummy node and no copy of the list.

<!-- stage: applicability -->
### Deciding When A Dummy Node Helps

#### Stating Who Owns The Head

The invariant of this pattern is that `dummy.next` identifies the current head and the variable `prev` or `tail` owns the last finalized link. A method that changes the head can answer, at every statement, which variable holds the head. If the answer is "the dummy", no branch is needed.

#### Skipping The Dummy When The Head Stays

The false friend is the idea that a dummy node is always better. It is not. A method that only reads the list, such as counting or searching, has no first-node problem, and the extra node only adds a line. Check whether the first node can change before adding one.

#### Returning The Right Reference

A common bug is `return head` after the method removed the original head. The old variable still points at the removed node, and the caller gets a list with a node that should be gone. Return `dummy.next`.

<!-- stage: exercises -->
### Exercises

#### [Build] Prepend Without A Special Case (Author exercise)
<!-- id: ll-insert-at -->

**Prerequisites.** The dummy node from this lesson.

**Problem.** Given the head of a list, a 0-based position `p` with `0 <= p <= n`, and a value `x`, insert a new node holding `x` so that it becomes the node at position `p`. Position 0 makes it the new head, and position `n` makes it the last node. Use one rule for every position by walking to the predecessor from a dummy node.

**Constraints.** The limits are:
- **Length** is `n` with `0 <= n <= 10^4`.
- **Values** satisfy `-10^4 <= val <= 10^4` and `-10^4 <= x <= 10^4`.
- **Answer** is the head of the changed list.
- **Mutation** changes one `next` field and allocates one node.

**Example 1.** Input list `1, 2`, `p = 0` and `x = 9`, output `9, 1, 2`.

**Example 2.** Input list `1, 2`, `p = 2` and `x = 5`, output `1, 2, 5`.

**Hint.** How many hops from the dummy node reach the predecessor of position `p`? Which statement returns the head?

**Changed decision.** The dummy node makes position 0 follow the same write as every other position.

#### [Vary] Merge Two Sorted Lists (LeetCode 21)
<!-- id: ll-merge-unique -->

**Prerequisites.** The exercise above and the merge from the previous lesson.

**Problem.** Two lists are each sorted in non-decreasing order. Merge them into one sorted list in which each value appears once. The result keeps the first node of each run of equal values, and every other node is dropped. This contract differs from the standard merge, which keeps all nodes. Build the result behind a dummy tail and return its head.

**Constraints.** The limits are:
- **Length** is between 0 and 50 nodes in each list.
- **Values** satisfy `-100 <= val <= 100`.
- **Answer** is the head of the merged list with strictly increasing values.
- **Mutation** changes `next` fields only.

**Example 1.** Input `1, 2, 4` and `1, 3, 4`, output `1, 2, 3, 4`.

**Example 2.** Input `2, 2, 2` and the empty list, output `2`.

**Hint.** When a node is about to attach, what must you compare it with? What is `tail.val` when `tail` is the dummy node?

**Changed decision.** The attach step skips a node when its value equals the last kept value.

#### [Boundary] Remove Linked List Elements (LeetCode 203)
<!-- id: ll-remove-up-to -->

**Prerequisites.** The two exercises above.

**Problem.** Given the head of a list, an integer `target` and a non-negative integer `limit`, remove the first `limit` nodes whose value equals `target`, counting from the head. Every other node stays, including later nodes that match `target`. This contract differs from removing every match. Return the head of the changed list.

**Constraints.** The limits are:
- **Length** is between 0 and 10^4 nodes.
- **Values** satisfy `0 <= val <= 50` and `0 <= target <= 50`.
- **Limit** satisfies `0 <= limit <= 10^4`.
- **Mutation** changes `next` fields only.

**Example 1.** Input list `7, 7, 3, 7`, `target = 7` and `limit = 2`, output `3, 7`.

**Example 2.** Input list `5, 5`, `target = 5` and `limit = 0`, output `5, 5`.

**Hint.** What must the loop count? Which matches are removed when the original first node matches?

**Changed decision.** A removal counter stops the same unlink rule after `limit` writes.

#### [Recognize] Remove Nth Node From End of List (LeetCode 19)
<!-- id: ll-remove-nth-count -->

**Prerequisites.** All three exercises above.

**Problem.** A list starts at `head`, and `n` satisfies `1 <= n <= length`. Remove the `n`th node from the end of the list and return the head. The last node is the first from the end. Count the length with one walk, and then walk to the predecessor of the target. The target can be the original head.

**Constraints.** The limits are:
- **Length** is `L` with `1 <= L <= 30`.
- **Values** satisfy `0 <= val <= 100`.
- **Position** satisfies `1 <= n <= L`.
- **Mutation** changes one `next` field only.

**Example 1.** Input list `1, 2, 3, 4, 5` and `n = 2`, output `1, 2, 3, 5`.

**Example 2.** Input list `1` and `n = 1`, output the empty list.

**Hint.** The target is the node at position `L - n` from the start, counting from 0. How many hops from the dummy node reach its predecessor?

**Changed decision.** The dummy node makes the removal of the original head ordinary.
