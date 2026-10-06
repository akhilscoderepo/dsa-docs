<!-- lesson-kind: standard -->
<!-- lesson-id: merge -->
## Merge Two Sorted Lists

<!-- stage: context -->
### Why Sorting Again Wastes The Order

Two database shards each return their newest order records as a linked list, sorted by timestamp. A service must combine them into one list sorted by timestamp, and it must reuse the record nodes, because other code holds references to them. The first version copies every timestamp into an array, sorts the array, and writes the values back. The code is short. It also throws away the fact that each shard already sorted its list, and it moves values between records that other code is watching.

Two sorted lists contain a lot of information about the answer. The smallest record of each list is its first node. The question here is how much of that information a method can use while it rewires the existing nodes.

<!-- stage: naive -->
### Collecting And Sorting Every Value

The direct plan ignores the existing order. It reads every value from both lists into one array, sorts the array, and builds a new list from the sorted values.

```java
final class MergeBySorting {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node mergeBySort(Node a, Node b) {
        int n = 0;
        for (Node c = a; c != null; c = c.next) n++;
        for (Node c = b; c != null; c = c.next) n++;       // count both lists
        int[] all = new int[n];
        int i = 0;
        for (Node c = a; c != null; c = c.next) all[i++] = c.val;
        for (Node c = b; c != null; c = c.next) all[i++] = c.val;   // copy every value
        Arrays.sort(all);                                  // sort as if no order existed
        Node head = null;
        for (int j = n - 1; j >= 0; j--) head = new Node(all[j], head);   // allocate n new nodes
        return head;
    }
}
```

On `1, 4, 6` and `2, 3, 7` the method returns `1, 2, 3, 4, 6, 7`. The result is correct, and it shares no node with the inputs.

<!-- stage: bottleneck -->
### Pricing The Ignored Order

```predict
The two lists have m and n nodes, and each list is already sorted. What does the sorting method cost in time and extra memory, and how many comparisons would a method need that uses the existing order?

Sorting m + n values costs O((m + n) log(m + n)) time, and the array and the new nodes cost O(m + n) extra memory. A method that uses the order needs at most m + n - 1 comparisons, so O(m + n) time with no new nodes.
```

For two lists of 500,000 nodes each, the sort compares values about twenty million times. A method that uses the order compares each node about once, so it needs fewer than one million comparisons. The sort also allocates one million new nodes. Code that holds a reference to an old record now points at a node that is no longer in the list.

The order of each input is the resource. The smallest unplaced value of each list is always its first node, so the next node of the answer is one of two candidates.

<!-- stage: insight -->
### Taking The Smaller Head Each Turn

The method builds the answer one node at a time, always at the **result tail**. The result tail is the last node of the **finalized prefix**, the part of the answer that is already sorted and will not change. Everything after the result tail is not yet decided.

#### One Comparison Decides One Node

Each input list is sorted, so its first node is its smallest unplaced node. The **smaller head** of the two first nodes is no larger than any unplaced node, so it is the next node of the answer. The method attaches it with `tail.next = smaller` and advances the list it came from by one node. A tie goes to the first list, so equal values keep the order of the input lists.

<!-- names: result tail, finalized prefix, smaller head -->

#### Attaching The Leftover In One Write

The loop ends when one list runs out. The other list is already sorted, and every node in it is at least as large as every node in the finalized prefix. The method attaches the whole **remainder** with one write, `tail.next = remainder`, and it does not visit those nodes again. A merge that visits every leftover node does extra work and changes nothing.

#### Choosing The First Node

The first node of the answer has no result tail before it. The method picks the smaller of the two heads as the answer's head, then sets the result tail to that node. An empty input list has no head, so the method returns the other list at once.

<!-- stage: variables -->
### The References Of One Merge

- **a** holds the first unplaced node of the first list, or `null` when that list is used up.
- **b** holds the first unplaced node of the second list, or `null` when that list is used up.
- **head** holds the first node of the answer, which is chosen once.
- **tail** holds the result tail, the last node of the finalized prefix.
- **remainder** is whichever of `a` and `b` is not `null` when the loop ends.

<!-- stage: trace -->
### Merging With A Leftover List

In this trace a pointer drawn outside the cells stands for `null`.

#### Merging Two Lists Of Three

Take the lists `1, 4, 6` and `2, 3, 7`. The cells hold the nodes of the first list followed by the nodes of the second list. The pointers `a` and `b` mark the first unplaced node of each list, and `tail` marks the result tail. The variable `merged` shows the finalized prefix.

```trace
{"cells":[1,4,6,2,3,7],"pointers":["a","b","tail"],"steps":[{"at":{"a":0,"b":3,"tail":-1},"vars":{"merged":"empty"},"note":"Start: both lists have unplaced nodes, and the finalized prefix is empty."},{"at":{"a":1,"b":3,"tail":0},"vars":{"merged":"1"},"note":"The smaller head is the node 1 of the first list, so it joins the finalized prefix and that list advances."},{"at":{"a":1,"b":4,"tail":3},"vars":{"merged":"1,2"},"note":"The smaller head is the node 2 of the second list, so it joins the finalized prefix and that list advances."},{"at":{"a":1,"b":5,"tail":4},"vars":{"merged":"1,2,3"},"note":"The smaller head is the node 3 of the second list, so it joins the finalized prefix and that list advances."},{"at":{"a":2,"b":5,"tail":1},"vars":{"merged":"1,2,3,4"},"note":"The smaller head is the node 4 of the first list, so it joins the finalized prefix and that list advances."},{"at":{"a":-1,"b":5,"tail":2},"vars":{"merged":"1,2,3,4,6"},"note":"The smaller head is the node 6 of the first list, so it joins the finalized prefix and that list advances."},{"at":{"a":-1,"b":-1,"tail":2},"vars":{"merged":"1,2,3,4,6,7"},"note":"One list is empty. One write attaches the remainder 7, and no comparison is made with it."}]}
```

Each turn places the smaller of the two heads. The last step attaches the leftover node 7 with one write, so the method never compares it with anything.

#### Attaching A Leftover Of Three Nodes

Now take `1, 2` and `5, 6, 7`. Every node of the first list is smaller than every node of the second list.

```trace
{"cells":[1,2,5,6,7],"pointers":["a","b","tail"],"steps":[{"at":{"a":0,"b":2,"tail":-1},"vars":{"merged":"empty"},"note":"Start: both lists have unplaced nodes, and the finalized prefix is empty."},{"at":{"a":1,"b":2,"tail":0},"vars":{"merged":"1"},"note":"The smaller head is the node 1 of the first list, so it joins the finalized prefix and that list advances."},{"at":{"a":-1,"b":2,"tail":1},"vars":{"merged":"1,2"},"note":"The smaller head is the node 2 of the first list, so it joins the finalized prefix and that list advances."},{"at":{"a":-1,"b":-1,"tail":1},"vars":{"merged":"1,2,5,6,7"},"note":"One list is empty. One write attaches the remainder 5,6,7, and no comparison is made with it."}]}
```

The first list runs out after two turns. The three leftover nodes join the answer with one write, and the method makes no comparison with them.

<!-- stage: code -->
### Merging In Code

```java
final class ListMerge {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node merge(Node a, Node b) {
        if (a == null) return b;                      // an empty list leaves the other list as the answer
        if (b == null) return a;
        Node head;
        if (b.val < a.val) { head = b; b = b.next; }  // the smaller head starts the answer; a tie keeps a first
        else { head = a; a = a.next; }
        Node tail = head;                             // the finalized prefix is the single node head
        while (a != null && b != null) {              // both lists still have unplaced nodes
            if (b.val < a.val) { tail.next = b; b = b.next; }
            else { tail.next = a; a = a.next; }       // attach the smaller head and advance its list
            tail = tail.next;                         // the finalized prefix grows by one node
        }
        tail.next = (a != null) ? a : b;              // one write attaches the remainder
        return head;
    }
}
```

The method allocates no node and changes only `next` fields. The strict comparison `b.val < a.val` sends ties to the first list, so the merge is stable.

- **Time** is O(m + n), because each loop turn places one node and the remainder costs one write.
- **Space** is O(1), because the method stores four references.

<!-- stage: applicability -->
### Using The Sorted Prefix Rule

#### Stating What Is Final

The invariant of a merge is that the finalized prefix is sorted, ends at `tail`, and contains no node larger than any unplaced node. Every list that is sorted on a key and must be combined without extra storage has this shape. State what is final before writing the loop.

#### Avoiding Copies That Break Contracts

The false friend of this pattern is the array copy. It is easy to write, and it is correct on the values. It breaks a contract whenever a caller expects the same nodes back, or expects linear time and constant extra memory. Read the statement for words such as "in place", "reuse" and "without extra space" before choosing the copy.

#### Handling The Head Specially

The first node has no result tail to attach to, so this version handles it before the loop. The next lesson shows how a helper node removes that special case. Until then, check the two empty-list returns and the head choice in every merge you write.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Two One-Node Lists (Author exercise)
<!-- id: ll-merge-one-node -->

**Prerequisites.** The smaller-head rule from this lesson.

**Problem.** A list `a` holds one node and a list `b` holds one node, and each node's `next` is `null`. Return one list that holds both nodes in non-decreasing order of value. If the two values are equal, the node of `a` comes first. Attach the smaller node first and then attach the other node, with no allocation.

**Constraints.** The limits are:
- **Length** is exactly 1 node in each list.
- **Values** satisfy `-100 <= val <= 100`.
- **Answer** is the head of a two-node list.
- **Mutation** changes the `next` field of one node.

**Example 1.** Input `5` and `3`, output `3, 5`.

**Example 2.** Input `4` and `4`, output the node of `a` followed by the node of `b`.

**Hint.** Which node is the head? What does the head's `next` point at after the single write?

**Changed decision.** The loop is unrolled to one comparison and one remainder write.

#### [Vary] Merge Two Sorted Lists (LeetCode 21)
<!-- id: ll-merge-two-sorted -->

**Prerequisites.** The exercise above.

**Problem.** Two singly linked lists are each sorted in non-decreasing order. Merge them into one sorted list by reusing the existing nodes, and return its head. Consume the smaller current node at each turn, and send ties to the first list.

**Constraints.** The limits are:
- **Length** is between 0 and 50 nodes in each list.
- **Values** satisfy `-100 <= val <= 100`.
- **Answer** is the head of the merged list, or `null` when both lists are empty.
- **Mutation** changes `next` fields and allocates no node.

**Example 1.** Input `1, 2, 4` and `1, 3, 4`, output `1, 1, 2, 3, 4, 4`.

**Example 2.** Input the empty list and `0`, output `0`.

**Hint.** The one-node case becomes a loop. What condition keeps the loop running, and what does the loop attach at the end?

**Changed decision.** The method repeats the smaller-head step until one list is empty.

#### [Boundary] One Empty Or Exhausted List (Author exercise)
<!-- id: ll-merge-exhausted -->

**Prerequisites.** The two exercises above.

**Problem.** Merge two sorted lists as in the previous exercise, and also return the number of value comparisons the method makes. A comparison is one evaluation of a test that reads the values of two nodes. When one list runs out, the method attaches the other list's remaining nodes with one write and makes no further comparison.

**Constraints.** The limits are:
- **Length** is between 0 and 1000 nodes in each list.
- **Values** satisfy `-10^4 <= val <= 10^4`, and each list is sorted in non-decreasing order.
- **Answer** is the merged head and a comparison count.
- **Mutation** changes `next` fields only.

**Example 1.** Input `1, 2, 3` and `7, 8`, output `1, 2, 3, 7, 8` and 3 comparisons.

**Example 2.** Input the empty list and `4`, output `4` and 0 comparisons.

**Hint.** How many nodes does the loop place before one list is empty? Which nodes does the final write attach?

**Changed decision.** The exhausted list ends the loop, and the leftover needs no comparison.

#### [Recognize] Sort List (LeetCode 148)
<!-- id: ll-sort-list -->

**Prerequisites.** All three exercises above.

**Problem.** Given the head of a linked list, return the list sorted in non-decreasing order of value. Reuse the existing nodes. Split the list into two halves, sort each half recursively, and combine the sorted halves with the merge from this lesson. A list of length 0 or 1 is already sorted. The split may count the nodes first and then walk half of them.

**Constraints.** The limits are:
- **Length** is between 0 and 5 * 10^4 nodes.
- **Values** satisfy `-10^5 <= val <= 10^5`, and duplicates are allowed.
- **Answer** is the head of the sorted list, or `null` for an empty list.
- **Mutation** changes `next` fields and allocates no node.

**Example 1.** Input `4, 2, 1, 3`, output `1, 2, 3, 4`.

**Example 2.** Input `-1, 5, 3, 4, 0`, output `-1, 0, 3, 4, 5`.

**Hint.** After the split, where must the first half end so the two halves share no node? Which loop already combines two sorted lists?

**Changed decision.** The merge becomes the combine step of a divide-and-conquer sort.
