<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-gap-kth-from-end -->
## Find The Kth Node From The End

<!-- stage: context -->
### Why The Third Newest Alert Is Wrong

An alert feed stores alerts from oldest to newest in a list, and the dashboard must show the third alert from the end. The first version counts the alerts, then walks `n - 3` hops from the head. It works on a feed of ten alerts. A feed with exactly three alerts needs zero hops and works too. A feed with two alerts makes `n - 3` negative, the loop never runs, and the dashboard shows the oldest alert as if it were the third from the end. A nearby bug shows the fourth from the end instead, because the developer counted from 0 and forgot that the last alert is the first from the end.

Positions counted from the end disagree with positions counted from the head by one, and the head gives no hint about how far the end is. The goal is a rule that finds a node by its distance from the end, with boundaries that a reader can check.

<!-- stage: naive -->
### Counting, Then Walking Forward

The direct plan counts the nodes, then converts the distance from the end into a distance from the head.

```java
final class KthByCount {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node kthFromEnd(Node head, int k) {
        int n = 0;
        for (Node c = head; c != null; c = c.next) n++;    // first walk counts the nodes
        if (k < 1 || k > n) return null;                   // reject positions that do not exist
        Node c = head;
        for (int i = 0; i < n - k; i++) c = c.next;        // second walk: n - k hops from the head
        return c;
    }
}
```

On `1, 2, 3, 4, 5` with `k = 2` the method counts 5, takes 3 hops, and returns the node 4. With `k = 1` it takes 4 hops and returns the node 5.

<!-- stage: bottleneck -->
### Counting The Hops And The Conversions

```predict
For a list of n nodes, how many hops does the method follow when k is 1, and how many when k equals n? Which formula does a reader have to check by hand?

For k = 1 the method follows n hops to count and n - 1 hops to walk, so 2n - 1 hops. For k = n it follows n hops to count and 0 hops to walk, so n hops. The reader must trust the formula n - k at both ends, and the method is O(n) in both cases.
```

The method is linear, so speed is not the main problem. The method traverses twice, and it converts one coordinate system into another with the formula `n - k`. An off-by-one error in that formula returns the wrong node at the two ends of the range. The length also has to be known before the answer can start, which a method working on a stream cannot do.

The method needs a rule that never mentions `n`. A distance from the end is a distance between two references, and two references can keep one distance while they move.

<!-- stage: insight -->
### Keeping A Fixed Gap Between Two References

Place two references at the head. Move the **leading reference** forward by `k` nodes, so that the **trailing reference** stays behind it. The two references now stand `k` nodes apart. This distance is the **fixed gap**.

#### Moving Both References Together

Move both references one node per step. The gap stays `k`, because each step moves both by one. The leading reference falls off the end of the list after `n - k` more steps. At that moment the trailing reference stands at index `n - k`, which is the `k`th node from the end, because `k` nodes lie between it and the end. The method never uses `n`.

<!-- names: leading reference, trailing reference, fixed gap -->

#### Stopping Before The Target

Some tasks need the node before the target, for example to delete the target. Start the trailing reference at a dummy node placed before the head, and keep the leading reference at the head. Advance the leading reference `k` nodes, and then move both until the leading reference is `null`. The trailing reference now stands one node before the `k`th node from the end. If the target is the original head, the trailing reference is the dummy node, and the same write removes it.

#### Checking That k Is Valid

The advance loop can run out of nodes. If the leading reference becomes `null` before it has moved `k` nodes, the list has fewer than `k` nodes, and no `k`th node from the end exists. The method then reports that no answer exists. If the leading reference becomes `null` exactly after `k` moves, then `k` equals the length, and the trailing reference stays at the head, which is the `k`th node from the end.

<!-- stage: variables -->
### The References With A Fixed Gap

- **lead** holds the leading reference, which moves `k` nodes first and then moves with `trail`.
- **trail** holds the trailing reference, which starts at the head, or at the dummy node when the predecessor is needed.
- **k** is the gap in nodes between `trail` and `lead` and counts from 1, so the last node is the first from the end.
- **dummy** holds the extra node before the head, used when the target may be the head.
- **n** is the list length, which the methods never compute.

<!-- stage: trace -->
### Moving A Gap To The End

Below, a pointer at the left of the cells or past their right end is not on a node, and it stands for `null` or for the dummy node as the text says.

#### Finding The Second Node From The End

Use the list `1, 2, 3, 4, 5` and `k = 2`. The pointer `lead` first moves two nodes from the head, and then both pointers move together. The variable `gap` shows the number of nodes between `trail` and `lead`.

```trace
{"cells":[1,2,3,4,5],"pointers":["lead","trail"],"steps":[{"at":{"lead":0,"trail":0},"vars":{"gap":0},"note":"Start: lead and trail both hold the node 1, so the gap is 0."},{"at":{"lead":1,"trail":0},"vars":{"gap":1},"note":"Only lead moves, to the node 2. The gap is 1."},{"at":{"lead":2,"trail":0},"vars":{"gap":2},"note":"Only lead moves, to the node 3. The gap is 2."},{"at":{"lead":3,"trail":1},"vars":{"gap":2},"note":"Both move one node. lead holds the node 4, and trail holds the node 2. The gap is still 2."},{"at":{"lead":4,"trail":2},"vars":{"gap":2},"note":"Both move one node. lead holds the node 5, and trail holds the node 3. The gap is still 2."},{"at":{"lead":-1,"trail":3},"vars":{"gap":2},"note":"Both move one node. lead holds null, and trail holds the node 4. The gap is still 2."}]}
```

When `lead` falls off the end, `trail` is on the node 4. Two nodes, 4 and 5, sit from `trail` to the end, so the node 4 is the second from the end.

#### Removing The Head When k Equals The Length

Now take the list `1, 2, 3` and `k = 3`, with a dummy node before the head. The first cell is the dummy node. The variable `gap` counts positions from `trail` to `lead`, so the dummy node makes it one larger than `k`.

```trace
{"cells":[0,1,2,3],"pointers":["lead","trail"],"steps":[{"at":{"lead":1,"trail":0},"vars":{"gap":1},"note":"Start: trail holds the dummy node and lead holds the head, the node 1."},{"at":{"lead":2,"trail":0},"vars":{"gap":2},"note":"Only lead moves, to the node 2."},{"at":{"lead":3,"trail":0},"vars":{"gap":3},"note":"Only lead moves, to the node 3."},{"at":{"lead":-1,"trail":0},"vars":{"gap":4},"note":"Only lead moves, to null."},{"at":{"lead":-1,"trail":0},"vars":{"gap":4},"note":"lead is null, so the second loop makes no move. trail still holds the dummy node, the predecessor of the head."}]}
```

The leading reference falls off the end after exactly three moves, so the loop that moves both references never runs. The trailing reference stays on the dummy node, which is the predecessor of the original head.

<!-- stage: code -->
### Two Methods With A Fixed Gap

```java
final class FixedGap {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node kthFromEnd(Node head, int k) {
        Node lead = head, trail = head;
        for (int i = 0; i < k; i++) {
            if (lead == null) return null;     // the list has fewer than k nodes
            lead = lead.next;                  // open a gap of k nodes
        }
        while (lead != null) {                 // move both until the leading reference leaves the list
            lead = lead.next;
            trail = trail.next;
        }
        return trail;                          // k nodes from trail to the end of the list
    }

    static Node removeKthFromEnd(Node head, int k) {
        Node dummy = new Node(0, head);
        Node lead = head, trail = dummy;
        for (int i = 0; i < k; i++) {
            if (lead == null) return head;     // k is too large, so nothing changes
            lead = lead.next;
        }
        while (lead != null) { lead = lead.next; trail = trail.next; }
        trail.next = trail.next.next;          // trail is the predecessor of the target
        return dummy.next;
    }
}
```

In `kthFromEnd`, a list with exactly `k` nodes leaves `lead` at `null` after the advance loop, and `trail` stays on the head. The loop condition `lead != null` is then false at once.

- **Time** is O(n), because `lead` makes at most `n` hops and `trail` makes at most `n - k` hops.
- **Space** is O(1), because the methods store three references.

<!-- stage: applicability -->
### Choosing A Gap Over A Ratio

#### Stating The Gap As The Invariant

The invariant of the method is that the number of nodes between the trailing reference and the leading reference stays `k` after every move of both references. State the number, and the stopping position follows. When the leading reference is `null`, the trailing reference has `k` nodes from itself to the end.

#### Separating A Gap From A Ratio

The false friend is the fast and slow pair from the previous lesson. That pair keeps a ratio of speeds, and it finds a fraction of the list such as the middle. A fixed gap keeps a difference of positions, and it finds an offset from the end. If the statement says "the `k`th from the end", use a gap. If it says "the middle", use a ratio.

#### Covering The Edge Values Of k

A value `k = 1` leaves the trailing reference on the last node. A value `k = n` leaves it on the head. A value `k > n` runs the advance loop past the end, so the method must test `lead` inside that loop. State the contract for `k > n` before coding, because the statement may promise it away or ask for a result.

<!-- stage: exercises -->
### Exercises

#### [Build] Kth Node From End (Author exercise)
<!-- id: ll-kth-from-end -->

**Prerequisites.** The fixed gap from this lesson.

**Problem.** Given the head of a list and an integer `k` with `1 <= k <= n`, return the value of the `k`th node from the end, where the last node is the first from the end. Open a gap of `k` nodes between two references, then move both references until the leading reference leaves the list. Return the value at the trailing reference.

**Constraints.** The limits are:
- **Length** is `n` with `1 <= n <= 10^5`.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Position** satisfies `1 <= k <= n`.
- **Mutation** does not occur.

**Example 1.** Input `1, 2, 3, 4, 5` and `k = 2`, output 4.

**Example 2.** Input `1, 2, 3, 4, 5` and `k = 1`, output 5.

**Hint.** How many nodes does the leading reference move before the trailing reference starts? What does the leading reference hold at the end?

**Changed decision.** A gap between two references replaces the count of nodes.

#### [Vary] Predecessor Of Kth From End (Author exercise)
<!-- id: ll-kth-predecessor -->

**Prerequisites.** The exercise above.

**Problem.** Given the head of a list and an integer `k` with `1 <= k <= n`, return the value of the node that comes just before the `k`th node from the end, or -1 if the `k`th node from the end is the head. Place a dummy node before the head, start the trailing reference there, and keep the leading reference at the head.

**Constraints.** The limits are:
- **Length** is `n` with `1 <= n <= 10^5`.
- **Values** satisfy `0 <= val <= 10^4`, so -1 is never a value.
- **Position** satisfies `1 <= k <= n`.
- **Mutation** does not occur.

**Example 1.** Input `1, 2, 3, 4, 5` and `k = 2`, output 3.

**Example 2.** Input `1, 2, 3, 4, 5` and `k = 5`, output -1.

**Hint.** Where does the trailing reference stop when it starts one node earlier? What does it hold when the target is the head?

**Changed decision.** The trailing reference starts one node earlier, so it stops before the target.

#### [Boundary] K Equals Length (Author exercise)
<!-- id: ll-kth-boundary -->

**Prerequisites.** The two exercises above.

**Problem.** Given the head of a list and an integer `k >= 1`, return the 0-based index from the head of the `k`th node from the end, or -1 if the list has fewer than `k` nodes. Find the index with a fixed gap, and count the trailing reference's hops to produce it. State what the method returns when `k` equals the length and when `k` is larger.

**Constraints.** The limits are:
- **Length** is between 0 and 10^5 nodes.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Position** satisfies `1 <= k <= 10^6`.
- **Mutation** does not occur.

**Example 1.** Input `1, 2, 3` and `k = 3`, output 0, because the target is the head.

**Example 2.** Input `1, 2, 3` and `k = 4`, output -1.

**Hint.** What does the leading reference hold after exactly `k` moves on a list of `k` nodes? Where must the check for a short list happen?

**Changed decision.** The advance loop validates `k`, and the result is an index instead of a node.

#### [Recognize] Remove Nth Node From End of List (LeetCode 19)
<!-- id: ll-remove-nth-gap -->

**Prerequisites.** All three exercises above.

**Problem.** Given the head of a list and an integer `n`, remove the `n`th node from the end and return the head, using one pass and no length count. This contract differs from the two-pass form: `n` may exceed the length of the list, and then the list stays unchanged. The target may be the original head.

**Constraints.** The limits are:
- **Length** is between 0 and 30 nodes.
- **Values** satisfy `0 <= val <= 100`.
- **Position** satisfies `1 <= n <= 100`.
- **Mutation** changes at most one `next` field.

**Example 1.** Input `1, 2, 3, 4, 5` and `n = 2`, output `1, 2, 3, 5`.

**Example 2.** Input `1, 2` and `n = 3`, output `1, 2`, and input `1` with `n = 1` gives the empty list.

**Hint.** Which reference must stop on the predecessor of the target? What happens to the advance loop when the list is shorter than `n`?

**Changed decision.** One pass with a gap replaces the length count, and a short list leaves the list unchanged.
