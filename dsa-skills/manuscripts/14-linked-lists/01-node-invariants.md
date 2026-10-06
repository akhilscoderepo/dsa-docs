<!-- lesson-kind: standard -->
<!-- lesson-id: node-invariants -->
## Follow References Through A List

<!-- stage: context -->
### Why Inserting One Node Can Lose Three

A text editor stores each line of a file as a node, and each node holds a reference to the next line. A developer adds a line after line 2 and writes two statements. The first points line 2 at the new line. The second points the new line at the line that line 2 pointed to. The editor now shows lines 1, 2 and the new line, and every line after the new line is gone. No error appears, because the program never throws on a lost line. It simply stops being able to find it.

The same silent loss happens when a loop walks a list and changes the references it is about to follow. A list gives no index to fall back on. The question for this lesson is how to follow and change references so that no node disappears.

<!-- stage: naive -->
### Treating The List Like An Array

The quick idea is to reuse array habits. To add up a list of `n` values, ask for the value at position 0, then position 1, and so on. Position `i` is found by starting at the first node and following `next` exactly `i` times.

```java
final class ListWalk {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static int sumByPosition(Node start, int n) {
        int total = 0;
        for (int i = 0; i < n; i++) {
            Node curr = start;                       // every lookup restarts at the first node
            for (int hop = 0; hop < i; hop++) curr = curr.next;
            total += curr.val;
        }
        return total;
    }
}
```

On the list `4, 7, 9` the method returns 20. It is correct and it never changes a reference, so it cannot lose a node. It still misses the point of the structure.

<!-- stage: bottleneck -->
### Counting The Hops

```predict
The method finds position i by following next i times. For a list of n nodes, how many next references does the whole sum follow, and what is that in big-O terms?

Position 0 costs 0 hops, position 1 costs 1 hop, and position n-1 costs n-1 hops. The total is 0 + 1 + ... + (n-1) = n(n-1)/2, which is O(n^2), although one walk from the first node to the last needs only n-1 hops.
```

The cost comes from restarting. For `n = 1,000` the method follows 499,500 references, while a single walk follows 999. For `n = 100,000` the gap is about five billion hops against one hundred thousand.

The array habit also hides a worse problem for any program that edits the list. The method never names which reference to keep before another reference changes. The insertion in this lesson needs a rule about the order of reference changes, and the next section states it.

<!-- stage: insight -->
### Keeping Every Node Reachable

A linked list is a chain of nodes. Each node stores a value and a `next` field, which holds either another node or `null`. A list has no positions of its own. The only thing a program holds on to is one reference to the first node, called the **head**. Every other node is found by following `next` from the head.

#### What Reachable Means

A node is **reachable** when some chain of `next` references, starting from a variable the program still holds, ends at that node. Java reclaims a node that is no longer reachable, so losing the last reference to a node deletes it. Every list operation therefore has one job above all others. After each statement, every node that should stay in the list must still be reachable.

<!-- names: head, reachable, successor -->

#### Saving The Successor Before Changing A Link

The **successor** of a node is the node its `next` field points to. Changing `node.next` overwrites the only stored reference to the successor, unless another variable also holds it. So the safe order has two parts. First copy the successor into a local variable. Then overwrite the field. The editor in the opening story broke this order, and the nodes after the new line lost their last reference.

#### Walking Without Restarting

A walk visits nodes in order with one variable, `curr`, which starts at the head and advances by `curr = curr.next`. The walk ends when `curr` is `null`. Each node costs one hop, so a full walk costs O(n), and the quadratic restart in the naive method disappears.

<!-- stage: variables -->
### The Names Used In Every List Method

The lessons of this chapter use the same small set of names, so each method reads the same way.

- **head** holds the first node, or `null` when the list is empty.
- **curr** holds the node the walk is visiting now.
- **saved** holds a successor copied before a `next` field changes.
- **val** holds the value stored in a node.
- **next** holds the following node, or `null` at the end of the list.

A method that changes the list also states its return value. If the first node can change, the method returns the new head, and the caller must store it.

<!-- stage: trace -->
### Walking And Inserting Step By Step

#### Counting The Nodes Of One List

Take the list `4, 7, 9`. The pointer `head` stays on the first node, the pointer `curr` marks the node being visited, and the value `n` counts the nodes seen so far. The walk starts at the head, adds one to `n` at every node, and stops when `curr` falls off the end of the list.

```trace
{"cells":[4,7,9],"pointers":["head","curr"],"steps":[{"at":{"head":0,"curr":0},"vars":{"n":0},"note":"curr starts at the head, the node 4. The count is 0."},{"at":{"head":0,"curr":1},"vars":{"n":1},"note":"The walk counts the node 4, so n becomes 1. Then curr moves to the node 7."},{"at":{"head":0,"curr":2},"vars":{"n":2},"note":"The walk counts the node 7, so n becomes 2. Then curr moves to the node 9."},{"at":{"head":0,"curr":3},"vars":{"n":3},"note":"The walk counts the node 9, so n becomes 3. Then curr moves to null, which ends the loop."}]}
```

The last step shows `curr` past the final node, which is the `null` the loop condition tests. The count is 3, so the walk follows 3 hops from the head to the end and visits each node once.

#### Inserting 5 After The Node 7

Now insert a new node holding 5 after the node 7. The cells list the nodes in creation order, so the new node is the last cell. The pointer `node` marks the node 7, and `new` marks the new node. The variable `chain` shows what the list holds when read from the head.

```trace
{"cells":[4,7,9,5],"pointers":["node","new"],"steps":[{"at":{"node":1,"new":-1},"vars":{"chain":"4,7,9","saved":"-"},"note":"Start: the list reads 4,7,9. The pointer node marks the node 7, and no new node exists yet."},{"at":{"node":1,"new":-1},"vars":{"chain":"4,7,9","saved":9},"note":"saved copies node.next, which is the node 9. The node 9 now has two references, node.next and saved."},{"at":{"node":1,"new":3},"vars":{"chain":"4,7,9","saved":9},"note":"The new node 5 is built with its next field set to saved. The list still reads 4,7,9 from the head, and the node 5 is not linked yet."},{"at":{"node":1,"new":3},"vars":{"chain":"4,7,5,9","saved":9},"note":"node.next now points to the new node. The list reads 4,7,5,9, and every old node is still reachable."}]}
```

The trace shows why the order matters. After `saved` copies the old successor, the node 9 has two references, one from `node.next` and one from `saved`. Only then does `node.next` change, and the final step links the new node to `saved`, so no node is lost.

<!-- stage: code -->
### Walking And Inserting In Code

```java
final class ListOps {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static int count(Node head) {
        int n = 0;
        for (Node curr = head; curr != null; curr = curr.next) {   // one hop per node
            n++;
        }
        return n;
    }

    static void insertAfter(Node node, int val) {
        Node saved = node.next;                    // keep the successor reachable first
        node.next = new Node(val, saved);          // the new node links to the saved successor
    }
}
```

The method `count` never writes a field, so it cannot change the list. The method `insertAfter` makes the two writes in the only safe order. Its statement `new Node(val, saved)` fills `next` while the constructor runs, so the new node never points at itself.

- **Time** of `count` is O(n), because the loop visits each node once.
- **Time** of `insertAfter` is O(1), because it follows no reference except the one it already holds.
- **Space** of both is O(1), because they store a few references and no copy of the list.

<!-- stage: applicability -->
### Using The Reachability Rule

#### Stating The Invariant Before Coding

The rule that every kept node stays reachable after each statement is the invariant of every linked list method. Before writing a list method, name the references the method must hold at each step. A mutation that does not name them is a guess.

#### Separating Lists From Arrays

Arrays and lists look alike on paper. A false friend is a feature that looks the same in two structures and behaves differently, and each feature of one has such a partner in the other. An array answers "what is at index `i`" in O(1). A list answers it in O(i), because the answer needs `i` hops. The false friend here is index access. A statement that asks for the position `i` of a list does not get the array's speed.

#### Watching For Null

A node's `next` is `null` at the end of the list, and `head` is `null` for an empty list. A method that reads `curr.next` when `curr` is `null` throws a `NullPointerException`. Each exercise below states which references may be `null` before it changes any reference.

<!-- stage: exercises -->
### Exercises

#### [Build] Traverse And Count (Author exercise)
<!-- id: ll-traverse-count -->

**Prerequisites.** The walk with one `curr` variable from this lesson.

**Problem.** A node holds an `int` value `val` and a reference `next` to another node or `null`. A list is the chain of nodes reachable from a reference `head` by following `next`. Given `head`, return the number of nodes in the list and the sum of their values. The method follows `next` references and never assigns to any field.

**Constraints.** The limits are:
- **Length** is between 0 and 10^5 nodes; `head` is `null` for the empty list.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Answer** is two `int` results, the count and the sum.
- **Mutation** does not occur; no field changes.

**Example 1.** Input `4, 7, 9`, output count 3 and sum 20.

**Example 2.** Input the empty list, output count 0 and sum 0.

**Hint.** Start `curr` at `head`. What condition ends the walk, and what does `curr` hold when the list is empty?

**Changed decision.** A single walk replaces one lookup per position.

#### [Vary] Insert After A Node (Author exercise)
<!-- id: ll-insert-after -->

**Prerequisites.** The traversal exercise above and the saved successor rule.

**Problem.** Given a reference `node` to a node of a list and an integer `x`, insert a new node holding `x` immediately after `node`. Every node that followed `node` before the call must follow the new node after it, in the same order. Return nothing; the caller still holds `head`.

**Constraints.** The limits are:
- **Length** is between 1 and 10^5 nodes, because `node` is not `null`.
- **Values** satisfy `-10^4 <= val <= 10^4` and `-10^4 <= x <= 10^4`.
- **Answer** is the changed list, read from `head`.
- **Mutation** changes `node.next` and the new node only.

**Example 1.** Input list `4, 7, 9`, `node` is the node 7 and `x = 5`, output `4, 7, 5, 9`.

**Example 2.** Input list `4, 7, 9`, `node` is the node 9 and `x = 1`, output `4, 7, 9, 1`.

**Hint.** What does `node.next` hold before the write? Where does the old value go if no variable keeps it?

**Changed decision.** The list changes at a given node, so the order of two writes matters.

#### [Boundary] Empty And Singleton Lists (Author exercise)
<!-- id: ll-empty-singleton -->

**Prerequisites.** The two exercises above.

**Problem.** Write the method `secondValue(head)`. It returns the value of the second node of the list, or `-1` when the list has fewer than two nodes. Then write `appendValue(head, x)`, which appends a node holding `x` after the last node and returns the head of the changed list. Both methods must work when `head` is `null` and when the list has one node.

**Constraints.** The limits are:
- **Length** is between 0 and 10^5 nodes.
- **Values** satisfy `0 <= val <= 10^4` and `0 <= x <= 10^4`, so `-1` is never a value.
- **Answer** is an `int` for `secondValue` and a head reference for `appendValue`.
- **Mutation** is allowed in `appendValue` only, and only on the last node.

**Example 1.** Input the empty list and `x = 6`, output -1 from `secondValue` and the list `6` from `appendValue`.

**Example 2.** Input list `3` and `x = 6`, output -1 from `secondValue` and the list `3, 6` from `appendValue`.

**Hint.** Which of `head`, `head.next` and `curr.next` may be `null` at each read? Which of them must you test first?

**Changed decision.** The empty list needs a new head, so the returned head replaces the argument.

#### [Recognize] Remove Linked List Elements (LeetCode 203)
<!-- id: ll-remove-elements -->

**Prerequisites.** All three exercises above.

**Problem.** Given the head of a list and an integer `target`, remove every node whose value equals `target`. The remaining nodes keep their original order. Return the head of the changed list. The method may reuse the retained nodes and does not copy them.

**Constraints.** The limits are:
- **Length** is between 0 and 10^4 nodes.
- **Values** satisfy `1 <= val <= 50` and `0 <= target <= 50`.
- **Answer** is the head of the retained chain, or `null` when no node remains.
- **Mutation** is allowed on `next` fields of retained nodes.

**Example 1.** Input list `1, 2, 6, 3, 4, 5, 6` and `target = 6`, output `1, 2, 3, 4, 5`.

**Example 2.** Input list `7, 7, 7, 7` and `target = 7`, output the empty list.

**Hint.** To delete a node, which retained node must change its `next`? What changes when the first node itself must go?

**Changed decision.** Deletion rewrites the link of the node before the removed node, and the head may change.
