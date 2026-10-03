<!-- lesson-kind: standard -->
<!-- lesson-id: intersection -->
## Intersection

<!-- stage: context -->
### Two Walking Parties On One Ridge Path

Two hiking parties set out from different mountain huts. Each party follows a chain of waypoint flags, and every flag shows the flag that comes next. After a while both chains join the same ridge path, and from the junction onward the two parties walk over exactly the same flags. One party's path before the junction is two flags long, the other's is three, and nobody has counted the flags after the junction.

The park ranger would like to know which flag is the first one that both parties pass, because that is where a new signpost should go. The flags carry numbers, but the numbers only tell which section of the trail a flag belongs to, so two different flags on the two approaches can show the same number. The ranger cannot mark or move the flags, and walking each party's whole route in advance to count it is possible but annoying.

<!-- stage: naive -->
### Compare Every Flag With Every Flag

The patient approach is to take each flag on the first route and look for it, flag by flag, along the second route.

```java
final class RidgeByComparison {
    static final class Flag {
        int section;
        Flag next;
        Flag(int section) { this.section = section; }
    }

    static Flag firstShared(Flag first, Flag second) {
        for (Flag a = first; a != null; a = a.next) {
            for (Flag b = second; b != null; b = b.next) {
                if (a == b) return a;
            }
        }
        return null;
    }
}
```

It is correct, because it compares flags themselves with `==`, not their numbers. For routes of five and four flags that share their last two it checks each flag of the first route against up to four flags of the second.

<!-- stage: bottleneck -->
### The Pairs Multiply

With routes of lengths n and m the nested loops make up to n times m comparisons, so the cost is O(n * m). Two routes of a hundred thousand flags would need ten billion comparisons. A hash set of the first route's flags brings the time down to O(n + m), but it costs O(n) memory, and the ranger's rule is to use no notebook.

The structure of the problem offers a better handle. After the junction both routes are identical, so the first shared flag is the same distance from the end on both routes. If the two parties were the same distance from the end, they could walk together and stop at the first flag they both reach. What spoils this is the difference in length: the party with the longer route would have to start later. Knowing the lengths means walking each route once, which is acceptable, but a trick that equalises the distances without counting is cleaner, and it relies on a fact about sums: the two routes together have the same total length, whichever is walked first.

<!-- stage: insight -->
### Walk Both Routes In Either Order

Two pointers, `pa` and `pb`, start at the two heads. Each advances one flag per round. When a pointer falls off the end of its own route it does not stop: it jumps to the head of the other route and keeps going. This is the **head switch**. Let `p` and `q` be the lengths of the parts before the junction, and `s` the length of the shared part, which may be zero. Pointer `pa` walks its own route of `p + s` flags, then the other route's own part of `q` flags before it reaches the junction, so it has walked `p + s + q` flags. Pointer `pb` has walked `q + s + p`. The two totals are equal, and this is the **length gap** cancelling out: the longer route's extra flags are absorbed by the other pointer's detour.

<!-- names: head switch, length gap, joint meeting -->

The pointers therefore stand on the same flag at the same round, and the loop condition `pa != pb` ends in a **joint meeting**. If the routes share flags, that meeting is on the first shared flag. If they do not, then after `p + q` flags each pointer has walked both routes and both are null at the same round, and null equals null, so the loop ends without a second condition. A variant that makes the cancellation explicit counts both routes first, advances the pointer on the longer route by the difference, and then moves both pointers together.

The cost is O(n + m) time and O(1) space.

<!-- stage: variables -->
### Two Pointers And A Null That Counts

The pointers `pa` and `pb` start at `headA` and `headB`. Each round moves each one step, and a pointer that is null moves to the other head. Treating the null as a step on the route is what makes both totals equal when the routes do not meet. When the two heads are the same node the loop never runs, and when one list is empty the other pointer walks to the end, and both become null together. The alternative uses `lenA` and `lenB`, an `int` each, and the difference `Math.abs(lenA - lenB)`.

<!-- stage: trace -->
### Two Approaches And A Shared End

Take a first route with flags `4, 1` before the junction and a second with `6, 1, 9`, followed in both cases by the shared flags `8, 2`. The second flag on each approach shows the number 1, but they are different flags. The two pointers start on the two heads. After four rounds `pa` has left the first route and `pb` is on the shared flag holding 2. In round five `pa` stands on the head of the second route, while `pb` has left its route and restarts at the head of the first. Over the next three rounds `pa` walks the flags 6, 1, 9 and `pb` walks 4, 1, and by round eight both stand on the first shared flag, holding 8. The two flags with number 1 were passed by different pointers at different times, and equal numbers never produced a meeting.

A second run uses routes with no shared flag, `1, 2` and `3`. After a few rounds both pointers are past the end together, so the loop stops without finding a shared flag, and no second termination test was needed.

```trace
{"cells":[4,1,6,1,9,8,2],"pointers":["pa","pb"],"steps":[{"at":{"pa":0,"pb":2},"vars":{"rounds":0},"note":"Pointer pa starts at the head of the first list, holding 4, and pb at the head of the second list, holding 6. They are different nodes."},{"at":{"pa":1,"pb":3},"vars":{"rounds":1},"note":"Round 1: pa is on the node holding 1 and pb is on the node holding 1."},{"at":{"pa":5,"pb":4},"vars":{"rounds":2},"note":"Round 2: pa is on the node holding 8 and pb is on the node holding 9."},{"at":{"pa":6,"pb":5},"vars":{"rounds":3},"note":"Round 3: pa is on the node holding 2 and pb is on the node holding 8."},{"at":{"pa":-1,"pb":6},"vars":{"rounds":4},"note":"Round 4: pa is past the end and pb is on the node holding 2. pa has just left the first list and will restart at the head of the second."},{"at":{"pa":2,"pb":-1},"vars":{"rounds":5},"note":"Round 5: pa is on the node holding 6 and pb is past the end. pb has just left the second list and will restart at the head of the first."},{"at":{"pa":3,"pb":0},"vars":{"rounds":6},"note":"Round 6: pa is on the node holding 1 and pb is on the node holding 4."},{"at":{"pa":4,"pb":1},"vars":{"rounds":7},"note":"Round 7: pa is on the node holding 9 and pb is on the node holding 1."},{"at":{"pa":5,"pb":5},"vars":{"rounds":8},"note":"Round 8: pa is on the node holding 8 and pb is on the node holding 8. They are the same node, so this is the first shared node."}]}
```

```trace
{"cells":[1,2,3],"pointers":["pa","pb"],"steps":[{"at":{"pa":0,"pb":2},"vars":{"rounds":0},"note":"Pointer pa starts on the node holding 1 and pb on the node holding 3."},{"at":{"pa":1,"pb":-1},"vars":{"rounds":1},"note":"Round 1: pa is on the node holding 2 and pb is past the end."},{"at":{"pa":-1,"pb":0},"vars":{"rounds":2},"note":"Round 2: pa is past the end and pb is on the node holding 1."},{"at":{"pa":2,"pb":1},"vars":{"rounds":3},"note":"Round 3: pa is on the node holding 3 and pb is on the node holding 2."},{"at":{"pa":-1,"pb":-1},"vars":{"rounds":4},"note":"Round 4: pa is past the end and pb is past the end. Both are past the end together, so the lists share no node."}]}
```

<!-- stage: code -->
### Head Switching And Length Alignment

```java
final class IntersectionCode {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node bySwitching(Node headA, Node headB) {
        Node pa = headA, pb = headB;
        while (pa != pb) {
            pa = pa == null ? headB : pa.next;
            pb = pb == null ? headA : pb.next;
        }
        return pa;
    }

    static int length(Node head) {
        int n = 0;
        for (Node cur = head; cur != null; cur = cur.next) n++;
        return n;
    }

    static Node byAlignment(Node headA, Node headB) {
        int lenA = length(headA), lenB = length(headB);
        Node a = headA, b = headB;
        for (int i = lenA; i > lenB; i--) a = a.next;
        for (int i = lenB; i > lenA; i--) b = b.next;
        while (a != b) {
            a = a.next;
            b = b.next;
        }
        return a;
    }
}
```

Both methods take O(n + m) time and O(1) space. The switching version needs no lengths, and the alignment version makes the equal-distance idea visible and works on lists that are not allowed to be walked twice in different orders.

<!-- stage: applicability -->
### When Two Chains Share A Tail

Use head switching or length alignment when two acyclic chains might end in the same nodes, and the task is to find where they first coincide. The invariant is that both pointers have walked the same total distance at every round, so the first round at which they are the same node is the first shared node, or the end of both. The check is on node identity, since only a shared node can be reached by both.

The false friend is equality of values. Equal numbers on different flags are common, and a check on values reports a junction that does not exist. A second false friend is the loop `while (pa.next != null)`, which stops one step early and cannot distinguish a shared last node from different last nodes. A third is giving the switch only to one pointer, which leaves the totals unequal and the loop endless on routes that do not meet.

Do not use these methods if either chain may contain a cycle, since both pointers can circle forever. Detect and handle a cycle first, as in the previous lesson. In Java, compare references with `==`, and take care that `pa.next` is never evaluated on a null pointer, which the conditional expression above avoids.

<!-- stage: exercises -->
### Exercises

#### [Build] Compare Node Identity (Author exercise)
<!-- id: ll-compare-identity -->

**Prerequisites.** The cycle entry lesson of this chapter, where `==` on references decided everything.

**Problem.** Two lists are described by three arrays: `a` and `b` are the values of the nodes before the junction in each list, and `shared` holds the values of the nodes that both lists share by reference. The first list is `a` followed by `shared`, and the second is `b` followed by `shared`. Return `[identityMatches, valueMatches]`: the number of nodes of the first list that also appear in the second by identity, and the number of nodes of the first list whose value equals the value of at least one node of the second list.

**Constraints.** 0 <= a.length, b.length, shared.length <= 10^3 and -10^9 <= value <= 10^9.

**Example 1.** Input `a = [1, 2]`, `b = [1, 5]`, `shared = [8, 9]`, output `[2, 3]`.

**Example 2.** Input `a = [3]`, `b = [3]`, `shared = []`, output `[0, 1]`.

**Hint.** Two nodes can hold the same value without being the same node. Which of the two counts is the one a junction is made of?

**Changed decision.** First rung: identity is compared with `==` on references, and values are compared separately to show that they are a different question.

#### [Vary] Align By Length (Author exercise)
<!-- id: ll-align-by-length -->

**Prerequisites.** The Compare Node Identity exercise above.

**Problem.** For the same description by `a`, `b` and `shared`, count both lists, advance the pointer of the longer list by the difference, and then move both pointers together until they are the same node. Return `[lengthA, lengthB, value]`, where `value` is the value of the first shared node, or -1 if the lists share no node.

**Constraints.** 0 <= a.length, b.length, shared.length <= 10^5 and 0 <= value <= 10^9, so -1 is never a real value.

**Example 1.** Input `a = [4, 1]`, `b = [5, 6, 1]`, `shared = [8, 4, 5]`, output `[5, 6, 8]`.

**Example 2.** Input `a = [1]`, `b = [2, 3]`, `shared = []`, output `[1, 2, -1]`.

**Hint.** After the longer list is advanced, how many nodes remain in each list before the junction? What are both pointers when the lists do not meet?

**Changed decision.** The distances are equalised by counting, and the longer list's pointer is advanced by the exact difference before the joint walk.

#### [Boundary] No Intersection And Shared Head (Author exercise)
<!-- id: ll-switch-rounds -->

**Prerequisites.** The two exercises above.

**Problem.** For the same description, run the head-switching walk, in which a pointer that is null moves to the other list's head, and return `[met, rounds]`: `met` is 1 if the walk stops on a real node and 0 if it stops with both pointers null, and `rounds` is the number of rounds in which pointers were moved.

**Constraints.** 0 <= a.length, b.length, shared.length <= 10^5 and -10^9 <= value <= 10^9. When both lists are empty, they have no nodes, and the answer is `[0, 0]`.

**Example 1.** Input `a = [1, 2]`, `b = [3]`, `shared = []`, output `[0, 4]`.

**Example 2.** Input `a = []`, `b = []`, `shared = [7, 2]`, output `[1, 0]`.

**Hint.** If both heads are the same node, does the loop body ever run? If there is no shared node, at which round are both pointers null?

**Changed decision.** A null pointer counts as a step on its route, so two lists with no shared node end together in null and the walk needs no second stopping test.

#### [Recognize] Intersection of Two Linked Lists (LeetCode 160)
<!-- id: ll-intersection-lists -->

**Prerequisites.** All three exercises above.

**Problem.** The head of each of two singly linked lists is given, and the lists may share nodes from some node onward. Return the first shared node, described here by its value, or -1 if the lists do not intersect. The lists must keep their original structure and the solution must use constant extra space.

**Constraints.** 0 <= lengths <= 3 * 10^4 and 1 <= value <= 10^5. Neither list contains a cycle. Different nodes can hold equal values.

**Example 1.** Input `a = [4, 1, 3]`, `b = [6, 5]`, `shared = [8, 4, 5]`, output `8`.

**Example 2.** Input `a = [2, 6, 4]`, `b = [1, 5]`, `shared = []`, output `-1`.

**Hint.** Why do the two pointers have the same total distance after switching heads once? What equality ends the loop, and what is the value when both are null?

**Changed decision.** Each pointer continues into the other list after its own ends, which equalises the walks without counting any length.
