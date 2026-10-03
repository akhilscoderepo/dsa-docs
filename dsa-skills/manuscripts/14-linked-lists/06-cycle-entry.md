<!-- lesson-kind: standard -->
<!-- lesson-id: cycle-entry -->
## Cycle Entry

<!-- stage: context -->
### Signposts In The Fog

A mountain trail is marked with signposts, and each signpost shows an arrow to the next one. In clear weather the trail ends at a final post. A storm has damaged one sign, and now the last post of the route points back to an earlier post, so a hiker who follows the arrows blindly walks round and round a loop and never reaches the end. All the posts look alike, and several carry the same number, because the number only tells which section of the trail a post belongs to.

The rescue team wants two answers from a hiker standing at the start with nothing but a notebook: does this trail ever end, and if it loops, which post is the first one that the loop returns to? They cannot mark the posts, and fog keeps them from seeing further than the next sign.

<!-- stage: naive -->
### Write Every Post In The Notebook

The straightforward plan is to record each post visited and to stop when a post is met for the second time. That post is the first one revisited, which is where the loop begins.

```java
final class TrailWithNotebook {
    static final class Post {
        int section;
        Post next;
        Post(int section) { this.section = section; }
    }

    static Post firstRevisited(Post start) {
        java.util.IdentityHashMap<Post, Boolean> seen = new java.util.IdentityHashMap<>();
        for (Post p = start; p != null; p = p.next) {
            if (seen.containsKey(p)) return p;
            seen.put(p, true);
        }
        return null;
    }
}
```

It is correct. It returns null when the trail ends, and otherwise the first post that is reached twice. The notebook is keyed by the post itself, not by its section number, because sections repeat.

<!-- stage: bottleneck -->
### The Notebook Grows With The Trail

The notebook holds one entry for every post before the loop is detected, so it uses O(n) extra memory, and every step pays for a hash lookup and an insertion. On a trail of tens of millions of posts, the notebook costs more than the trail. A shortcut that keeps the section numbers instead of the posts is worse, since equal numbers on different posts would be reported as a loop that does not exist.

The task suggests something smaller. A hiker who walks alone can never tell the difference between a long corridor and a loop, since in both cases the next sign is always there. Two hikers can tell: if they walk at different speeds, the faster one reaches the end on a trail that ends, and on a loop the faster one comes round and catches the slower one. What remains is to prove that the two must meet, and to turn the meeting into the entry of the loop, using nothing but two references and the arithmetic of distances.

<!-- stage: insight -->
### Two Speeds And A Meeting

Start two references at the head. The first, `slow`, advances one node per round, and the second, `fast`, advances two. If `fast` reaches null, the list ends and there is no cycle. Otherwise the **relative speed** of the pair is one node per round: once both are inside the loop, `fast` gains exactly one node on `slow` every round, so the gap, measured around the loop, falls by one each round and reaches zero within the length of the loop. They land on the same node, which is the **collision point**, and that settles the existence question without any memory.

The entry takes one more step of reasoning. Let `a` be the number of nodes from the head to the entry, and `c` the length of the loop. When they meet, `slow` has taken some number of steps, say `s`, and `fast` has taken `2s`. Their difference `s` is a whole number of laps, so `s` is a multiple of `c`. Since `slow` stands `s - a` steps past the entry, taking `a` more steps brings it to `s`, which is a multiple of `c` past the entry, and so back to the entry. This is the **entry reset**: put a second reference at the head, and move it and `slow` one node at a time; they meet at the entry after exactly `a` steps.

<!-- names: relative speed, collision point, entry reset -->

The cost is O(n) time, since `slow` takes fewer than `a + c` rounds to meet, and O(1) space.

<!-- stage: variables -->
### Slow, Fast And The Probe

The references `slow` and `fast` both begin at the head. The condition `fast != null && fast.next != null` guards the double step, because `fast.next.next` would throw `NullPointerException` if either link were null. After a meeting, a third reference `probe` starts at the head, while `slow` stays at the collision point, and both advance one node at a time until they are equal. The loop length is measured by walking from the collision point once around until it is reached again. A list with a single node pointing at itself is a loop of length 1, and a list of two nodes pointing at each other is a loop of length 2.

<!-- stage: trace -->
### A Six-Post Trail And A Two-Post Loop

Take six posts with the sections `7, 3, 5, 2, 6, 8`, where the last post points back to the second one. Both hikers start on the first post. After round one, slow is on the post holding 3 and fast on the one holding 5. After round two they are on 5 and 6. After round three, slow is on 2 while fast has gone round the corner and stands on 3. After round four they are on 6 and 2, and after round five both stand on the post holding 8. That is the collision point. The probe is placed on the first post, and one step later both the probe and slow are on the post holding 3, which is the entry of the loop.

A second run uses two posts, `4` and `9`, where the second points back to the first. This is the smallest loop of more than one post: after round one, slow is on 9 and fast is back on 4, and after round two both are on 4, so a loop is found in two rounds without any special treatment.

```trace
{"cells":[7,3,5,2,6,8],"pointers":["slow","fast","probe"],"steps":[{"at":{"slow":0,"fast":0,"probe":-1},"vars":{"phase":"chase"},"note":"Both pointers start at the first signpost, which holds 7."},{"at":{"slow":1,"fast":2,"probe":-1},"vars":{"phase":"chase","round":1},"note":"After round 1 slow stands at the signpost holding 3 and fast at the one holding 5."},{"at":{"slow":2,"fast":4,"probe":-1},"vars":{"phase":"chase","round":2},"note":"After round 2 slow stands at the signpost holding 5 and fast at the one holding 6."},{"at":{"slow":3,"fast":1,"probe":-1},"vars":{"phase":"chase","round":3},"note":"After round 3 slow stands at the signpost holding 2 and fast at the one holding 3."},{"at":{"slow":4,"fast":3,"probe":-1},"vars":{"phase":"chase","round":4},"note":"After round 4 slow stands at the signpost holding 6 and fast at the one holding 2."},{"at":{"slow":5,"fast":5,"probe":-1},"vars":{"phase":"chase","round":5},"note":"After round 5 slow stands at the signpost holding 8 and fast at the one holding 8. They are the same signpost, so a loop exists."},{"at":{"slow":5,"fast":5,"probe":0},"vars":{"phase":"find the entry"},"note":"A third pointer is placed at the first signpost, while slow stays at the meeting point. From now on both move one signpost at a time."},{"at":{"slow":1,"fast":5,"probe":1},"vars":{"phase":"find the entry"},"note":"Both advance one signpost. The probe is at the signpost holding 3 and slow at the one holding 3. They coincide, and this signpost is where the loop begins."}]}
```

```trace
{"cells":[4,9],"pointers":["slow","fast"],"steps":[{"at":{"slow":0,"fast":0},"vars":{"rounds":0},"note":"Both pointers start at the first node, and the second node points back to the first."},{"at":{"slow":1,"fast":0},"vars":{"rounds":1},"note":"Round 1: slow is on the node holding 9 and fast is on the node holding 4. They differ, so the chase continues."},{"at":{"slow":0,"fast":0},"vars":{"rounds":2},"note":"Round 2: slow is on the node holding 4 and fast is on the node holding 4. They are the same node, so there is a cycle."}]}
```

<!-- stage: code -->
### Detect, Measure And Locate

```java
final class CycleCode {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node collision(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return slow;
        }
        return null;
    }

    static int cycleLength(Node head) {
        Node meet = collision(head);
        if (meet == null) return 0;
        int length = 1;
        for (Node cur = meet.next; cur != meet; cur = cur.next) length++;
        return length;
    }

    static Node entry(Node head) {
        Node meet = collision(head);
        if (meet == null) return null;
        Node probe = head;
        while (probe != meet) {
            probe = probe.next;
            meet = meet.next;
        }
        return probe;
    }
}
```

All three methods take O(n) time, since the chase ends within `a + c` rounds, and O(1) space. The comparison is `==` on references, so equal section numbers never cause a false meeting.

<!-- stage: applicability -->
### When A Chain May Loop Back

Think of two speeds when following references might never end: a linked list that could contain a cycle, or any sequence defined by a function that maps each state to a next state, where the question is whether a state repeats and where the repetition begins. The invariant is that, once both references are inside the loop, the gap between them shrinks by one per round, and the node where a reference placed at the head meets the slower one is the entry.

The false friend is comparing values. Two different nodes can hold the same value, so a check on values reports loops that do not exist and misses the first repeated node. A second false friend is a fast pointer that is advanced without checking `fast.next`, which crashes on lists of odd length. A third is stopping at the meeting point and reporting it as the entry, since the collision point is somewhere inside the loop and only by chance the entry.

Do not use it when memory is free and clarity matters more than the space, since the notebook version is shorter to explain. Do not use it on structures that are not single-successor chains, such as graphs with branching. In Java, the comparison must be `==` on node references, and a self-loop must be handled by the same code, which it is, since the first round already puts both references on the node.

<!-- stage: exercises -->
### Exercises

#### [Build] Linked List Cycle (LeetCode 141)
<!-- id: ll-detect-cycle -->

**Prerequisites.** The reverse and merge lessons of this chapter.

**Problem.** The list is encoded by its values and an integer `pos`. If `pos` is -1 the last node points to null, and otherwise the last node points to the node at index `pos`. Return whether the list contains a cycle, using only constant extra memory.

**Constraints.** 0 <= n <= 10^4, -10^5 <= value <= 10^5, and -1 <= pos < n. Repeated values are allowed and say nothing about cycles.

**Example 1.** Input `values = [8, 1, 6, 4, 9]`, `pos = 2`, output `true`.

**Example 2.** Input `values = [5, 7]`, `pos = -1`, output `false`.

**Hint.** What does the fast pointer reach on a list that ends? Which test protects the double step?

**Changed decision.** First rung: a chase at two speeds replaces the notebook, and equality is tested on node references.

#### [Vary] Measure Cycle Length (Author exercise)
<!-- id: ll-cycle-length -->

**Prerequisites.** The Linked List Cycle exercise above.

**Problem.** For the same encoding of a list by `values` and `pos`, return the number of nodes in the cycle, or 0 if the list has no cycle.

**Constraints.** 0 <= n <= 10^5, -10^9 <= value <= 10^9 and -1 <= pos < n.

**Example 1.** Input `values = [8, 1, 6, 4, 9]`, `pos = 2`, output `3`.

**Example 2.** Input `values = [5, 7]`, `pos = -1`, output `0`.

**Hint.** The collision point is inside the loop. How can one walk from it to count the loop without any further comparison against values?

**Changed decision.** After the collision, one pointer walks once around the loop until it returns to the collision point, and the number of steps is the answer.

#### [Boundary] Self-Loop And Two-Node Cycle (Author exercise)
<!-- id: ll-cycle-rounds -->

**Prerequisites.** The two exercises above.

**Problem.** Run the chase with `slow` moving one node and `fast` moving two nodes per round, and return the pair `[hasCycle, rounds]`, where `rounds` is the number of rounds started before the loop ended, by a meeting or by `fast` reaching the end. `hasCycle` is 1 or 0. A round counts if its moves were made.

**Constraints.** 1 <= n <= 10^5, -10^9 <= value <= 10^9 and -1 <= pos < n.

**Example 1.** Input `values = [4]`, `pos = 0`, output `[1, 1]`.

**Example 2.** Input `values = [4, 9]`, `pos = -1`, output `[0, 1]`.

**Hint.** Which nodes do both pointers stand on after the first round for a single node pointing at itself? For the acyclic pair, what does `fast` become in the first round?

**Changed decision.** The guard `fast != null && fast.next != null` is checked before every double step, so lists with one or two nodes need no special case.

#### [Recognize] Linked List Cycle II (LeetCode 142)
<!-- id: ll-cycle-entry -->

**Prerequisites.** All three exercises above.

**Problem.** For the same encoding, return the index of the node where the cycle begins, which is the node the last node points to, or -1 if there is no cycle. Do not modify the list and use constant extra memory.

**Constraints.** 0 <= n <= 10^4, -10^5 <= value <= 10^5 and -1 <= pos < n. Values may repeat.

**Example 1.** Input `values = [7, 3, 5, 2, 6, 8]`, `pos = 1`, output `1`.

**Example 2.** Input `values = [4, 4, 4]`, `pos = 2`, output `2`.

**Hint.** After the collision, where must the second pointer be placed, and how many steps does each take until they meet? Why does the second example prove that values cannot decide?

**Changed decision.** A second pointer is reset to the head while the slow one stays at the collision point, and equal-speed movement locates the entry.
