<!-- lesson-kind: standard -->
<!-- lesson-id: intersection -->
## Find Where Two Lists Meet

<!-- stage: context -->
### Why Equal Messages Pick The Wrong Commit

A version-control tool stores each branch as a list of commits, newest first, and two branches reuse the same older commit objects. A developer needs the newest commit that both branches contain. The first attempt walks both lists and stops at the first pair of commits with equal messages. Two unrelated commits on different branches both carry the message "fix typo", so the tool reports a commit that only one branch contains.

Equal text does not make two commits the same commit. The same commit is one object that both lists reach through their `next` fields. This lesson asks how to find the first object that two lists share, when the lists have different lengths and no index to line them up.

<!-- stage: naive -->
### Comparing Every Pair Of Nodes

The direct plan takes each node of the first list and scans the second list for the same node. The test uses `==`, which compares object identity.

```java
final class MeetByPairs {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node firstShared(Node a, Node b) {
        for (Node x = a; x != null; x = x.next) {         // each node of the first list
            for (Node y = b; y != null; y = y.next) {     // against each node of the second list
                if (x == y) return x;                     // the same object, not merely an equal value
            }
        }
        return null;
    }
}
```

On lists `4, 1, 8, 4, 5` and `5, 6, 1, 8, 4, 5`, whose last three nodes are the same objects, the method returns the node 8. The nodes holding 1 and 5 in the other positions have equal values and are different objects, so the test skips them.

<!-- stage: bottleneck -->
### Counting The Comparisons

```predict
The first list has m nodes and the second has n nodes. In the worst case, how many identity comparisons does the pair method make, and what would a set of first-list nodes cost?

The pair method makes m times n comparisons, which is O(m * n). A set of the first list's nodes brings the time to O(m + n) but needs O(m) extra memory.
```

For two lists of 100,000 nodes with no shared node, the pair method makes ten billion comparisons. A set of nodes fixes the time at the price of memory proportional to the first list. A program that has no memory to spare and a long list needs a method with O(m + n) time and O(1) memory.

Look at what the lists share. Two lists that meet stay together until their ends, because each node has one `next`. The shared part is a common ending, and a common ending has the same length in both lists.

<!-- stage: insight -->
### Lining Up The Shared Ending

Two lists that share a node share everything after it, because a node has exactly one `next`. Call that common ending the **shared tail**. If the first list has `x` nodes before the shared tail and the second has `y` nodes before it, the lists have lengths `x + s` and `y + s`, where `s` is the length of the shared tail.

#### Aligning The Two Lists By Length

The nodes at the same distance from the end are the same object inside the shared tail and different objects outside it. The method therefore wants both references to start at the same distance from the end. The **length difference** `|(x + s) - (y + s)| = |x - y|` says how many nodes the longer list has before that point. The method advances the longer list's reference by the length difference. Then it moves both references one node at a time and compares identity at every step. The first equal pair is the first shared node, and two `null` references mean no shared node.

<!-- names: shared tail, length difference, head switching -->

#### Removing The Length Count With Head Switching

**Head switching** reaches the same alignment without counting. Each reference walks its own list to the end. When it falls off the end, it jumps to the head of the other list and keeps walking. The first reference walks `x + s` nodes and then `y` nodes of the second list, so it has walked `x + y` nodes of unshared prefix before the shared tail begins, plus one step to leave `null`. The second reference walks `y + s` nodes and then `x` nodes of the first list, which is also `x + y` nodes of unshared prefix, plus one step to leave `null`. Both references stand on the first shared node after the same number of steps.

#### Why No Shared Node Still Ends

If the lists share no node, `s` is 0. Each reference walks `m + n` nodes and then falls off the end of the second list. Both references reach `null` after the same number of steps, so they are equal, and the loop stops with the answer `null`.

<!-- stage: variables -->
### The References Of The Meeting Methods

- **a** and **b** hold the heads of the two lists, and the methods never change them.
- **pa** and **pb** hold the two walking references.
- **x** and **y** count the nodes before the shared tail in the first list and the second list.
- **s** counts the nodes in the shared tail, with `s = 0` when no node is shared.
- **diff** is the length difference, used only by the alignment method.

<!-- stage: trace -->
### Two Walkers Meeting At The Shared Tail

On the cells below, a pointer drawn outside them is `null`. The cells list the first list, then the nodes that only the second list holds. The last three cells of the first list are also the last three nodes of the second list.

#### Head Switching With A Shared Tail

Take the first list `4, 1, 8, 4, 5` and the second list `5, 6, 1, 8, 4, 5`. The nodes 8, 4 and 5 are shared. The value 1 appears once in each list, in two different nodes. The pointers `pa` and `pb` mark the two walkers.

```trace
{"cells":[4,1,8,4,5,5,6,1],"pointers":["pa","pb"],"steps":[{"at":{"pa":0,"pb":5},"vars":{"steps":0},"note":"Start: pa holds the head of the first list and pb holds the head of the second list."},{"at":{"pa":1,"pb":6},"vars":{"steps":1},"note":"Both move one node. pa holds the node 1, and pb holds the node 6."},{"at":{"pa":2,"pb":7},"vars":{"steps":2},"note":"Both move one node. pa holds the node 8, and pb holds the node 1."},{"at":{"pa":3,"pb":2},"vars":{"steps":3},"note":"Both move one node. pa holds the node 4, and pb holds the node 8."},{"at":{"pa":4,"pb":3},"vars":{"steps":4},"note":"Both move one node. pa holds the node 5, and pb holds the node 4."},{"at":{"pa":-1,"pb":4},"vars":{"steps":5},"note":"Both move one node. pa holds null, and pb holds the node 5."},{"at":{"pa":5,"pb":-1},"vars":{"steps":6},"note":"Both move one node. pa holds the node 5 from null to the head of the second list, and pb holds null."},{"at":{"pa":6,"pb":0},"vars":{"steps":7},"note":"Both move one node. pa holds the node 6, and pb holds the node 4 from null to the head of the first list."},{"at":{"pa":7,"pb":1},"vars":{"steps":8},"note":"Both move one node. pa holds the node 1, and pb holds the node 1."},{"at":{"pa":2,"pb":2},"vars":{"steps":9},"note":"Both move one node. pa holds the node 8, and pb holds the node 8. The references are equal, so the walkers stand on the first shared node."}]}
```

After nine steps the walkers hold the same node, the node 8. The first walker passed the five nodes of its list, left through `null` into the second list, and passed three nodes there. The second walker passed the six nodes of its list, left through `null` into the first list, and passed two nodes there. The two equal values of 1 never made the walkers stop.

#### Head Switching Without A Shared Node

Now take the lists `2, 6, 4` and `1, 5`, which share no node.

```trace
{"cells":[2,6,4,1,5],"pointers":["pa","pb"],"steps":[{"at":{"pa":0,"pb":3},"vars":{"steps":0},"note":"Start: pa holds the head of the first list and pb holds the head of the second list."},{"at":{"pa":1,"pb":4},"vars":{"steps":1},"note":"Both move one node. pa holds the node 6, and pb holds the node 5."},{"at":{"pa":2,"pb":-1},"vars":{"steps":2},"note":"Both move one node. pa holds the node 4, and pb holds null."},{"at":{"pa":-1,"pb":0},"vars":{"steps":3},"note":"Both move one node. pa holds null, and pb holds the node 2 from null to the head of the first list."},{"at":{"pa":3,"pb":1},"vars":{"steps":4},"note":"Both move one node. pa holds the node 1 from null to the head of the second list, and pb holds the node 6."},{"at":{"pa":4,"pb":2},"vars":{"steps":5},"note":"Both move one node. pa holds the node 5, and pb holds the node 4."},{"at":{"pa":-1,"pb":-1},"vars":{"steps":6},"note":"Both move one node. pa holds null, and pb holds null. The references are equal, and both are null, so no node is shared."}]}
```

Each walker covers its own list, switches, and covers the other list. The walkers reach `null` together on step six, one step after the last node. Equal references at `null` end the loop with the answer `null`.

<!-- stage: code -->
### Two Ways To Meet In Code

```java
final class ListMeet {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static int length(Node head) {
        int n = 0;
        for (Node c = head; c != null; c = c.next) n++;
        return n;
    }

    static Node alignByLength(Node a, Node b) {
        int la = length(a), lb = length(b);
        Node pa = a, pb = b;
        for (int i = 0; i < la - lb; i++) pa = pa.next;   // the longer first list moves ahead by the difference
        for (int i = 0; i < lb - la; i++) pb = pb.next;   // the longer second list moves ahead by the difference
        while (pa != pb) {                                // identity comparison at equal distance from the end
            pa = pa.next;
            pb = pb.next;
        }
        return pa;                                        // the shared node, or null when both reach the end
    }

    static Node headSwitch(Node a, Node b) {
        Node pa = a, pb = b;
        while (pa != pb) {
            pa = (pa == null) ? b : pa.next;              // after the end of one list, continue on the other
            pb = (pb == null) ? a : pb.next;
        }
        return pa;
    }
}
```

In `alignByLength`, both loops can run, but only one of them runs for any input, because one of `la - lb` and `lb - la` is not positive. In `headSwitch`, a walker that reaches `null` takes one step to leave `null` and move to the other head, and that step counts toward the walk.

- **Time** is O(m + n) for both methods, because each reference makes at most `m + n` steps.
- **Space** is O(1), because both methods store a few references and counters.

<!-- stage: applicability -->
### Using The Equal-Distance Rule

#### Stating The Alignment Fact

The invariant of both methods is that the two references are the same distance from the end of their lists whenever they are compared, so the first equal pair is the first shared node. State the distance rule before coding. For head switching, say that both references take the same number of steps, counting the one step that leaves `null`.

#### Keeping Identity Apart From Value

The false friend is the equal value. A node value is data, and a shared node is an object. Two lists may hold many equal values and no shared node, and the commit example shows how a value test returns a wrong answer. Compare references with `==` and never compare `val`.

#### Covering Empty Lists And Shared Heads

An empty list has no node to share, and both methods return `null` when either list is empty. When both lists start at the same node, the references are equal at the first test, and the methods return the head without a step. The exercises cover these cases.

<!-- stage: exercises -->
### Exercises

#### [Build] Compare Node Identity (Author exercise)
<!-- id: ll-node-identity -->

**Prerequisites.** The shared tail idea from this lesson.

**Problem.** Two lists `a` and `b` have the same length `n`. For each position `i` from 0 to `n - 1`, compare the `i`th node of `a` with the `i`th node of `b`. Return two counts: the number of positions where the two values are equal, and the number of positions where the two nodes are the same object.

**Constraints.** The limits are:
- **Length** is `n` with `0 <= n <= 10^4` for both lists.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Answer** is two `int` counts.
- **Mutation** does not occur.

**Example 1.** Input two separate lists `1, 2, 3` and `1, 2, 3`, output 3 equal values and 0 same nodes.

**Example 2.** Input `1, 2, 3` and `9, 2, 3` where the second and third nodes are shared, output 2 equal values and 2 same nodes.

**Hint.** Which operator compares object identity? Which field compares values?

**Changed decision.** Identity replaces value as the test for a shared node.

#### [Vary] Align By Length (Author exercise)
<!-- id: ll-align-by-length -->

**Prerequisites.** The exercise above.

**Problem.** Given the heads of two lists, return the first node that both lists contain as the same object, or `null` if they share no node. Count the length of each list, advance the reference of the longer list by the length difference, and then move both references one node at a time until they are the same node or both are `null`.

**Constraints.** The limits are:
- **Length** is between 0 and 3 * 10^4 nodes in each list.
- **Values** satisfy `-10^5 <= val <= 10^5`, and values may repeat.
- **Answer** is a node reference or `null`.
- **Mutation** does not occur; both lists must be unchanged after the call.

**Example 1.** Input `4, 1, 8, 4, 5` and `5, 6, 1, 8, 4, 5` sharing the last three nodes, output the node 8.

**Example 2.** Input `1, 9` and `2, 3` sharing no node, output `null`.

**Hint.** If the first list is longer by `d`, how many nodes of it come before the first node that could be shared? What do the two references hold if no node is shared?

**Changed decision.** A length count replaces the nested comparison.

#### [Boundary] No Intersection And Shared Head (Author exercise)
<!-- id: ll-meet-boundary -->

**Prerequisites.** The two exercises above.

**Problem.** Use head switching on two lists and return the number of loop turns that run before the two references are equal. A turn moves both references once. The count is 0 when the references are equal before the first turn, and a turn that moves a reference off the end counts like any other turn. Report the count for lists that share no node, lists that start at the same node, and lists where one or both are empty.

**Constraints.** The limits are:
- **Length** is between 0 and 3 * 10^4 nodes in each list.
- **Values** satisfy `-10^5 <= val <= 10^5`.
- **Answer** is an `int` count of turns.
- **Mutation** does not occur.

**Example 1.** Input `1, 2` and `3` sharing no node, output 4, because the references reach `null` on different turns, switch lists, and are both `null` on turn 4.

**Example 2.** Input the same head for both lists, output 0.

**Hint.** What do both references hold after `m + n` steps when no node is shared? What does an empty list do to the loop?

**Changed decision.** The stopping point is a pair of `null` references, and a shared head stops the loop at once.

#### [Recognize] Intersection of Two Linked Lists (LeetCode 160)
<!-- id: ll-intersection-switch -->

**Prerequisites.** All three exercises above.

**Problem.** Given the heads `headA` and `headB` of two singly linked lists, return the node where the two lists intersect, or `null` if they do not intersect. The lists are acyclic. Use constant extra memory and no length count. When a reference reaches the end of its list, move it to the head of the other list.

**Constraints.** The limits are:
- **Length** is between 1 and 3 * 10^4 nodes in each list.
- **Values** satisfy `1 <= val <= 10^5`, and values may repeat.
- **Answer** is a node reference or `null`.
- **Mutation** does not occur; both lists keep their original structure.

**Example 1.** Input `4, 1, 8, 4, 5` and `5, 6, 1, 8, 4, 5` sharing the last three nodes, output the node 8.

**Example 2.** Input `2, 6, 4` and `1, 5` sharing no node, output `null`.

**Hint.** After the first reference walks its list and then the front of the other list, how many nodes has it walked before the shared tail? How many has the second reference walked?

**Changed decision.** Head switching replaces the length count.
