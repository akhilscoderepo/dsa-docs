<!-- lesson-kind: standard -->
<!-- lesson-id: merge -->
## Merge

<!-- stage: context -->
### Two Checkout Lanes Become One

A shop has two checkout lanes, and each lane is already in order of arrival, with the customer who came earliest at the front. The manager closes one till and wants the two lanes to become one lane in order of arrival, with nobody moving more than necessary. Each customer holds a numbered ticket, and the customer with the lower ticket must be served first, whichever lane they stand in.

Customers cannot be asked to step away and come back, because each of them is holding a trolley, and the shop has no room for a third lane. The only thing the staff can do is point from one customer to the next. The assistant manager watches the front of each lane and asks a short question each time: who is first, the front of the first lane or the front of the second? The answer decides who is pointed to next.

<!-- stage: naive -->
### Pour Everyone Into A Row And Sort

One idea is to ignore the order that each lane already has: write down every ticket, sort the row, and build a new lane from it.

```java
final class LaneMergeBySort {
    static final class Customer {
        int ticket;
        Customer next;
        Customer(int ticket) { this.ticket = ticket; }
    }

    static Customer merge(Customer a, Customer b) {
        java.util.ArrayList<Integer> tickets = new java.util.ArrayList<>();
        for (Customer c = a; c != null; c = c.next) tickets.add(c.ticket);
        for (Customer c = b; c != null; c = c.next) tickets.add(c.ticket);
        java.util.Collections.sort(tickets);
        Customer head = null, tail = null;
        for (int t : tickets) {
            Customer fresh = new Customer(t);
            if (head == null) head = fresh; else tail.next = fresh;
            tail = fresh;
        }
        return head;
    }
}
```

It is correct on the tickets. For the lanes 2, 5, 9 and 1, 5, 7, 8 it produces 1, 2, 5, 5, 7, 8, 9.

<!-- stage: bottleneck -->
### Sorting Throws Away The Order Already There

The sort treats the customers as if they were in no order at all, so it costs O((n + m) log (n + m)) for lanes of lengths n and m, although both lanes are already sorted and a single pass can do the job in O(n + m). It also needs a row of n + m numbers, and it builds brand new customers, so the people who were standing in the lanes are no longer the ones in the merged lane. Anything that was attached to those customers, such as a trolley number or a reference held by another structure, is lost.

What the two lanes already give is a strong guarantee: the smallest ticket among everyone is at the front of one of the two lanes. Whoever is smaller can be moved to the merged lane at once, and then the same guarantee holds for what remains. The work is one comparison per customer moved. What has to be designed with care is the pointer bookkeeping: where the merged lane's tail is, how the first customer is chosen when the merged lane is still empty, and what happens when one of the lanes runs out.

<!-- stage: insight -->
### Take The Smaller Front Each Time

Keep three references: the head of the first remaining lane, the head of the second remaining lane, and the tail of the merged lane. The merged lane built so far is the **finalized prefix**: it is sorted, it holds only tickets that cannot be beaten by anything still waiting, and it is linked from the first customer through the tail. The two **remaining heads** are the fronts of the two lanes of customers not yet moved, and each of those lanes is still in order. Each step compares the two remaining heads, detaches the smaller one, appends it behind the tail, and advances that lane's head. On a tie the first lane's customer goes first, which keeps the merge stable.

<!-- names: finalized prefix, remaining heads, bulk attach -->

The invariant is that the finalized prefix is sorted and every ticket in it is no larger than any ticket in either remaining lane. A comparison of the two remaining heads preserves it, since the chosen head is the minimum of both lanes. When one lane is exhausted, the other lane is already sorted and every ticket in it is no smaller than the prefix, so a **bulk attach** of the entire remainder, one assignment to the tail's `next`, finishes the job without visiting those customers.

The cost is at most n + m comparisons, so O(n + m) time, and O(1) extra memory, because no node is created.

<!-- stage: variables -->
### Two Heads, A Tail, A First Pick

The references `a` and `b` are the remaining heads and move forward only. The reference `tail` is null while the merged lane is empty, and `head` records the first node picked. When `tail` is null, the picked node becomes `head`, and otherwise it is linked behind `tail`. After the loop, at most one of `a` and `b` is non-null, and that one is attached. If both lists are empty the result is null, and if one is empty the result is the other, handled by the same code without a special case.

<!-- stage: trace -->
### Seven Customers In One Pass

Take the lanes `2, 5, 9` and `1, 5, 7, 8`. The fronts are 2 and 1, so the customer with 1 from the second lane goes first and becomes the head. Then 2 against 5 sends the customer with 2. The fronts are now 5 and 5, a tie, so the first lane's 5 goes before the second lane's, and the 5 from the second lane follows next. Then 9 against 7 sends 7, and 9 against 8 sends 8. The second lane is now exhausted, and the first lane still has one customer holding 9, which is attached to the tail in a single assignment. The merged lane reads 1, 2, 5, 5, 7, 8, 9.

A second run merges `1, 2` with `5, 6`. The first lane's customers win both comparisons, since 1 and 2 are smaller than 5, and then the first lane is exhausted. Both customers in the second lane are attached at once, so only two comparisons were made for four customers.

```trace
{"cells":[2,5,9,1,5,7,8],"pointers":["a","b"],"steps":[{"at":{"a":0,"b":4},"vars":{"result":"[1]"},"note":"The node holding 1 from the second list is attached to the result tail, and that list's head moves forward."},{"at":{"a":1,"b":4},"vars":{"result":"[1,2]"},"note":"The node holding 2 from the first list is attached to the result tail, and that list's head moves forward."},{"at":{"a":2,"b":4},"vars":{"result":"[1,2,5]"},"note":"The node holding 5 from the first list is attached to the result tail, and that list's head moves forward."},{"at":{"a":2,"b":5},"vars":{"result":"[1,2,5,5]"},"note":"The node holding 5 from the second list is attached to the result tail, and that list's head moves forward."},{"at":{"a":2,"b":6},"vars":{"result":"[1,2,5,5,7]"},"note":"The node holding 7 from the second list is attached to the result tail, and that list's head moves forward."},{"at":{"a":2,"b":-1},"vars":{"result":"[1,2,5,5,7,8]"},"note":"The node holding 8 from the second list is attached to the result tail, and that list's head moves forward."},{"at":{"a":2,"b":-1},"vars":{"result":"[1,2,5,5,7,8,9]"},"note":"The second list is exhausted, so the whole remaining first list, a single node holding 9, is attached in one assignment."}]}
```

```trace
{"cells":[1,2,5,6],"pointers":["a","b"],"steps":[{"at":{"a":1,"b":2},"vars":{"result":"[1]","comparisons":1},"note":"The node holding 1 from the first list is attached after one comparison."},{"at":{"a":-1,"b":2},"vars":{"result":"[1,2]","comparisons":2},"note":"The node holding 2 from the first list is attached after one comparison."},{"at":{"a":-1,"b":2},"vars":{"result":"[1,2,5,6]","comparisons":2},"note":"The first list is exhausted after two comparisons, and the second list, still headed by the node holding 5, is attached as a whole without any further comparison."}]}
```

<!-- stage: code -->
### Merge By Relinking And Sort By Merging

```java
final class MergeCode {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node merge(Node a, Node b) {
        Node head = null, tail = null;
        while (a != null && b != null) {
            Node take;
            if (b.value < a.value) { take = b; b = b.next; }
            else { take = a; a = a.next; }
            if (tail == null) head = take; else tail.next = take;
            tail = take;
        }
        Node rest = a != null ? a : b;
        if (tail == null) return rest;
        tail.next = rest;
        return head;
    }

    static Node sortList(Node head) {
        if (head == null || head.next == null) return head;
        int n = 0;
        for (Node cur = head; cur != null; cur = cur.next) n++;
        Node left = head;
        for (int i = 1; i < n / 2; i++) left = left.next;
        Node right = left.next;
        left.next = null;
        return merge(sortList(head), sortList(right));
    }
}
```

The merge makes at most n + m comparisons and creates no nodes, so it is O(n + m) time and O(1) space. The sort splits the list in half by counting, recurses, and merges, so it takes O(n log n) time and uses O(log n) stack frames.

<!-- stage: applicability -->
### When Two Ordered Chains Must Join

Use a merge when two chains are each in order by the same key and the result must be in order too, with the original nodes reused. It is also the building block of a merge sort on a linked list, where the structure suits the algorithm: splitting needs only one cut, and merging needs no extra array. The invariant is that the result tail ends a sorted, finalized prefix, and both remaining heads begin sorted suffixes whose smallest elements are no smaller than anything in the prefix.

The false friend is copying values into an array and sorting, which is correct on values and breaks the contract on nodes, memory and time. A second false friend is the loop that stops when either chain is empty and forgets the other chain's remainder, which silently drops customers. A third is comparing with `<=` on the second chain's value, which makes ties favour the second chain and breaks stability.

Do not merge this way when the chains are not sorted by the same key, or when a priority structure over many chains is needed, since pairwise merging of many lists repeats work. In Java, keep the comparison on `int` values simple, and use `Integer.compare` when subtraction might overflow.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Two One-Node Lists (Author exercise)
<!-- id: ll-merge-one-node -->

**Prerequisites.** The node invariants and reverse lessons of this chapter.

**Problem.** Two linked lists each hold exactly one node, with values `x` and `y`. Merge them into one sorted list by relinking the nodes, and return the values of the result. If `x` equals `y`, the node from the first list must come first, and the result also reports whether it did.

**Constraints.** -10^9 <= x, y <= 10^9. The nodes must be reused. Return `[first, second, firstWasFromFirstList]` where the last entry is 1 if the first value in the result came from the first list and 0 otherwise.

**Example 1.** Input `x = 7`, `y = 3`, output `[3, 7, 0]`.

**Example 2.** Input `x = 4`, `y = 4`, output `[4, 4, 1]`.

**Hint.** Which node is attached first, and what is the other node attached to? Which comparison keeps ties in favour of the first list?

**Changed decision.** First rung: attach the smaller head, then attach the leftover node as the remainder, with ties going to the first list.

#### [Vary] Merge Two Sorted Lists (LeetCode 21)
<!-- id: ll-merge-two-sorted -->

**Prerequisites.** The Merge Two One-Node Lists exercise above.

**Problem.** Given the heads of two sorted linked lists, merge them into one sorted list made of the nodes of the two lists, and return the head of the merged list.

**Constraints.** 0 <= n, m <= 50 and -100 <= value <= 100. Both lists are sorted in non-decreasing order.

**Example 1.** Input `a = [2, 5, 9]`, `b = [1, 5, 7, 8]`, output `[1, 2, 5, 5, 7, 8, 9]`.

**Example 2.** Input `a = []`, `b = []`, output `[]`.

**Hint.** What is the tail while the result is empty? How do both lists being empty and one list being empty fall out of the same code?

**Changed decision.** The loop continues while both lists have nodes, the smaller front is attached each time, and the remainder is attached as a whole.

#### [Boundary] One Empty Or Exhausted List (Author exercise)
<!-- id: ll-merge-exhausted -->

**Prerequisites.** The two exercises above.

**Problem.** Merge two sorted lists given by their values, and report the number of value comparisons the merge performed. Return the pair of the merged values and the comparison count.

**Constraints.** 0 <= n, m <= 10^5 and -10^9 <= value <= 10^9. When one list runs out, the remaining nodes of the other must be attached with one assignment and no more comparisons.

**Example 1.** Input `a = [1, 2]`, `b = [5, 6]`, output `[[1, 2, 5, 6], 2]`.

**Example 2.** Input `a = [4, 8, 9]`, `b = []`, output `[[4, 8, 9], 0]`.

**Hint.** How many comparisons are needed once one list is empty? What is attached after the loop, and how is a null tail handled?

**Changed decision.** The tail of a non-empty merge is linked straight to the surviving list, so a whole suffix joins at the cost of one assignment.

#### [Recognize] Sort List (LeetCode 148)
<!-- id: ll-sort-list -->

**Prerequisites.** All three exercises above.

**Problem.** Take the head of a linked list and return the list sorted in ascending order using a merge sort that reuses the nodes. Split the list into two halves, sort each half recursively, and merge them.

**Constraints.** 0 <= n <= 5 * 10^4 and -10^5 <= value <= 10^5.

**Example 1.** Input `values = [5, 2, 9, 2, 7, 1]`, output `[1, 2, 2, 5, 7, 9]`.

**Example 2.** Input `values = []`, output `[]`.

**Hint.** How is the list cut into two halves with only one assignment after the cut point is found? What are the base cases of the recursion?

**Changed decision.** The merge invariant is reused inside a recursion, and the two halves are produced by cutting a single link after counting the nodes.
