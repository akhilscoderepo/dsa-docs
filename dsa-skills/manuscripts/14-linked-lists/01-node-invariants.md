<!-- lesson-kind: standard -->
<!-- lesson-id: node-invariants -->
## Node Invariants

<!-- stage: context -->
### A Scavenger Hunt Of Clue Cards

A school runs a scavenger hunt in which every clue card is hidden in a different place. A card carries a number and one sentence that tells the players where the next card is hidden. The first card is handed over at the start, and the last card says that the hunt is finished. Nobody has a map. The only way to reach the fifth card is to find the first card, follow it to the second, and so on.

The organiser would like to answer questions about the hunt. How many cards are there? What do the numbers add up to? A late idea is a new card squeezed in after the third one, and a worry is a card going missing because the sentence on the previous card was rewritten before the new place was known. The organiser notices that the order of the cards lives entirely in the sentences, and that a careless rewrite can strand every card after it.

<!-- stage: naive -->
### Ask For Card Number Five Each Time

The first idea treats the hunt like a numbered shelf: to work with the card at position `i`, walk from the first card to position `i` every time. A weighted total, where each number is multiplied by its position, shows the cost.

```java
final class ClueHunt {
    static final class Clue {
        int number;
        Clue next;
        Clue(int number) { this.number = number; }
    }

    static Clue clueAt(Clue first, int position) {
        Clue cur = first;
        for (int step = 0; step < position; step++) cur = cur.next;
        return cur;
    }

    static long weightedTotalByPosition(Clue first) {
        int count = 0;
        for (Clue c = first; c != null; c = c.next) count++;
        long total = 0;
        for (int i = 0; i < count; i++) total += (long) i * clueAt(first, i).number;
        return total;
    }
}
```

It is correct. For the numbers 4, 7, 1, 9 it returns 36, since the products are 0, 7, 2 and 27.

<!-- stage: bottleneck -->
### Positions Cost A Walk Each

Reaching position `i` takes `i` steps, because nothing in a chain of references records where position `i` is. The weighted total therefore does 0 + 1 + 2 + ... + (n - 1) steps, which is about n squared over two, or O(n^2). For a hunt of a hundred thousand cards that is five billion steps, where one walk would take a hundred thousand.

The second cost is about mutation. A card that is rewired carelessly takes everything behind it out of reach. If the sentence on card three is overwritten with the new card's place before the old sentence is written down, the old fourth card and all after it are still hidden somewhere, but no one can find them. In an array a store at one index leaves the other indices alone, so this failure has no counterpart there. What is needed is a way to walk once and carry the current card along, and a rule for rewiring that never loses a card.

<!-- stage: insight -->
### Walk Once And Never Lose A Card

A chain of nodes is a **walk**: a reference named `cur` starts at the head and moves with `cur = cur.next` until it is null. Everything that is computed along the way, such as a count, a sum or a weighted total with a running position, is updated in the same step as the move, so no node is revisited. Three ideas keep this safe. The **terminating null** is the only signal that the chain has ended, so every dereference of `cur.next` must be guarded by a test that `cur` itself is not null. The **saved successor** is a local reference to the node that comes after the one being rewired, taken before any link is changed. The **reachability invariant** says that at every moment, each node that has not yet been handled can be reached from some reference the program still holds, whether the head, `cur`, or a saved successor.

<!-- names: terminating null, saved successor, reachability invariant -->

Insertion shows the three working together. To insert a new node after a given node, first save the given node's successor, then point the new node at it, and only then point the given node at the new node. In that order the old successor is held by a local reference until the new node holds it, so the invariant is true after every line. Reversing the order loses the tail.

The cost is one step per node, O(n) for the walk and O(1) for an insertion at a node already in hand, with O(1) extra memory.

<!-- stage: variables -->
### Head, Cursor And Saved Reference

The head is the only entry point to the chain, and the function that changes the first node must return the new head, because the caller's variable is a copy. The cursor `cur` is a local reference that moves forward and never changes the chain unless the code assigns to `cur.next`. The saved reference holds a node that would otherwise become unreachable. When the chain is empty the head is null, and then the cursor is null before the loop starts, so the loop body must not run. A singleton has a head whose `next` is null, which is the other edge case worth naming for every operation.

<!-- stage: trace -->
### One Walk And One Careful Insertion

Take the numbers `4, 7, 1, 9` and walk them. The cursor names the node holding 4, which is counted and added, and then it follows the reference to the node holding 7. The same happens for 1 and 9, so the count reaches 4 and the sum reaches 21. When the cursor leaves the last node it becomes null, the loop ends, and the walk has touched each node exactly once. Nothing has been changed, and the head still names the first node.

The second run inserts a new node holding 5 after the node holding 7. At the start the new node exists but nothing points to it. The old successor, the node holding 1, is saved. The new node is pointed at it, so the new node now leads to 1 and 9. Only then is the node holding 7 pointed at the new node, and the chain reads 4, 7, 5, 1, 9. The step to study is the third one, where the new node takes over the tail before anything points to the new node.

```trace
{"cells":[4,7,1,9],"pointers":["head","cur"],"steps":[{"at":{"head":0,"cur":0},"vars":{"count":0,"sum":0},"note":"The reference cur names the node holding 4, which has not been counted yet. It is counted, then cur follows its next reference."},{"at":{"head":0,"cur":1},"vars":{"count":1,"sum":4},"note":"The reference cur names the node holding 7, which has not been counted yet. It is counted, then cur follows its next reference."},{"at":{"head":0,"cur":2},"vars":{"count":2,"sum":11},"note":"The reference cur names the node holding 1, which has not been counted yet. It is counted, then cur follows its next reference."},{"at":{"head":0,"cur":3},"vars":{"count":3,"sum":12},"note":"The reference cur names the node holding 9, which has not been counted yet. It is counted, then cur follows its next reference."},{"at":{"head":0,"cur":4},"vars":{"count":4,"sum":21},"note":"The reference cur is null, so the loop ends. The list was only read, and the head still names the first node."}]}
```

```trace
{"cells":[4,7,1,9,5],"pointers":["node","fresh"],"steps":[{"at":{"node":1,"fresh":4},"vars":{"main_chain":"4>7>1>9","fresh_chain":"5"},"note":"A new node holding 5 exists but nothing points to it, and its next reference is null. The chain still reads 4, 7, 1, 9."},{"at":{"node":1,"fresh":4},"vars":{"saved":"1","main_chain":"4>7>1>9","fresh_chain":"5"},"note":"The old successor of the node holding 7, which holds 1, is saved in a local reference before any link changes."},{"at":{"node":1,"fresh":4},"vars":{"saved":"1","main_chain":"4>7>1>9","fresh_chain":"5>1>9"},"note":"The new node now points to the saved successor, so it can reach 1 and 9 without help from the main chain."},{"at":{"node":1,"fresh":4},"vars":{"saved":"1","main_chain":"4>7>5>1>9","fresh_chain":"5>1>9"},"note":"The node holding 7 now points to the new node. The chain reads 4, 7, 5, 1, 9 and every node is still reachable from the head."}]}
```

<!-- stage: code -->
### Walk And Insert After A Node

```java
final class NodeWalk {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static long[] countAndSum(Node head) {
        long count = 0, sum = 0;
        for (Node cur = head; cur != null; cur = cur.next) {
            count++;
            sum += cur.value;
        }
        return new long[]{count, sum};
    }

    static void insertAfter(Node node, int value) {
        Node fresh = new Node(value);
        Node saved = node.next;
        fresh.next = saved;
        node.next = fresh;
    }
}
```

The walk is O(n) time and O(1) space. The insertion is O(1) once the node is in hand, and the local `saved` can be inlined, but writing it out makes the order of the three assignments visible. Swapping the last two lines would leave `fresh.next` null and lose every node after `node`.

<!-- stage: applicability -->
### When References Define The Order

Think in nodes when the data is a chain of references, when elements are inserted or removed at known positions, or when the order lives in the links and not in indices. The invariant is that every node not yet handled stays reachable from a held reference, and the head always names the start of the intended chain. Each operation is then judged by what it does to reachability, not only by what it does to values.

The false friend is the array habit of asking for position `i`. It works, so tests pass, and the cost is quadratic without any visible error. A second false friend is rewiring in the order that reads naturally, which loses the tail. A third is returning nothing from a function that may replace the head, which leaves the caller holding the old first node.

Do not use a chain when the program needs fast access by position or a binary search, since a walk is the only way to reach a node. In Java, `==` on node references tests identity and not equal values, and a null head must be handled before the first dereference, since `head.next` on a null head throws `NullPointerException`.

<!-- stage: exercises -->
### Exercises

#### [Build] Traverse And Count (Author exercise)
<!-- id: ll-traverse-and-count -->

**Prerequisites.** The chapter on arrays and the idea of a reference from Chapter 00.

**Problem.** A linked list is given by its values from head to tail. Walk it once, without changing it, and return the pair `[count, sum]` of the number of nodes and the sum of their values.

**Constraints.** 0 <= n <= 10^5 and -10^9 <= value <= 10^9. The sum can exceed the range of `int`, so return `long` values.

**Example 1.** Input `values = [4, 7, 1, 9]`, output `[4, 21]`.

**Example 2.** Input `values = []`, output `[0, 0]`.

**Hint.** What is the head of an empty list? Which test makes the loop body skip it without a special case?

**Changed decision.** First rung: a single walk that reads each node once and never assigns to a `next` field.

#### [Vary] Insert After A Node (Author exercise)
<!-- id: ll-insert-after-node -->

**Prerequisites.** The Traverse And Count exercise above.

**Problem.** A linked list is given by its values, together with a position `p` and a value `x`. Insert a new node holding `x` immediately after the node at position `p`, counting from 0, and return the values of the resulting list from head to tail.

**Constraints.** 1 <= n <= 10^5, 0 <= p < n and -10^9 <= x <= 10^9.

**Example 1.** Input `values = [4, 7, 1, 9]`, `p = 1`, `x = 5`, output `[4, 7, 5, 1, 9]`.

**Example 2.** Input `values = [3]`, `p = 0`, `x = 8`, output `[3, 8]`.

**Hint.** Which of the three assignments may come first without losing the old successor? What happens if `p` names the last node?

**Changed decision.** The list changes, so the successor is saved before the first link is rewritten.

#### [Boundary] Empty And Singleton Lists (Author exercise)
<!-- id: ll-empty-and-singleton -->

**Prerequisites.** The two exercises above.

**Problem.** A linked list is given by its values. Delete its last node and return the values of the resulting list. An empty list stays empty.

**Constraints.** 0 <= n <= 10^5 and -10^9 <= value <= 10^9. The solution may not copy values into an array to find the last node.

**Example 1.** Input `values = [6]`, output `[]`.

**Example 2.** Input `values = []`, output `[]`.

**Hint.** Deleting a node needs a reference to the node before it. What does the walk hold when the list has one node, and who owns the head afterward?

**Changed decision.** The head itself may be deleted, so the function returns the head, and the walk stops one node early using a lookahead on `next.next`.

#### [Recognize] Remove Linked List Elements (LeetCode 203)
<!-- id: ll-remove-elements -->

**Prerequisites.** All three exercises above.

**Problem.** Given the head of a linked list of integers and an integer `val`, remove every node whose value equals `val` and return the new head.

**Constraints.** 0 <= n <= 10^4, 1 <= value <= 50 and 0 <= val <= 50.

**Example 1.** Input `values = [4, 4, 1, 4, 2, 4]`, `val = 4`, output `[1, 2]`.

**Example 2.** Input `values = [5, 5]`, `val = 5`, output `[]`.

**Hint.** The first node may need to be removed several times in a row. How is the head advanced before the main walk starts, and which node's `next` is rewritten in the walk?

**Changed decision.** More than one node can match, and the head may match too, so the head is advanced first and then each matching successor is bypassed through its predecessor.
