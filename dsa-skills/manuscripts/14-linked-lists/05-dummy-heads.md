<!-- lesson-kind: standard -->
<!-- lesson-id: dummy-heads -->
## Dummy Heads

<!-- stage: context -->
### A Divider Card Before The First Recipe

A recipe society keeps its cards in a long box, in a chain: each card has a note saying which card comes next, and the box has a sticker saying which card is first. Cards are added and withdrawn all the time, and a withdrawal of a card in the middle is easy, since the card before it just gets a new note. The first card is the awkward one. It has no card before it, so withdrawing it means changing the sticker on the box instead of a note on a card, and inserting a new first card needs the sticker changed too.

The secretary has had enough of writing every instruction twice, once for the first card and once for the others. She also dislikes the day when three withdrawals in a row hit the first card, because then the sticker has to be changed three times. She wonders whether the box could be arranged so that every card, including the first real one, has a card before it.

<!-- stage: naive -->
### Two Code Paths For The First Card

The usual response is to handle the first card in a separate loop and then handle the rest in a second loop. A withdrawal of every card whose number is in a blocked list shows the shape.

```java
final class FileBoxWithBranches {
    static final class Card {
        int number;
        Card next;
        Card(int number) { this.number = number; }
    }

    static Card withdraw(Card first, java.util.Set<Integer> blocked) {
        while (first != null && blocked.contains(first.number)) first = first.next;
        Card cur = first;
        while (cur != null && cur.next != null) {
            if (blocked.contains(cur.next.number)) cur.next = cur.next.next;
            else cur = cur.next;
        }
        return first;
    }
}
```

It is correct. For the cards 5, 2, 5, 7, 2, 9 with the numbers 2 and 5 blocked, it returns 7, 9.

<!-- stage: bottleneck -->
### Duplicated Logic Is The Cost

The work is O(n) either way, so the cost here is not time. It is the shape of the code. The same decision, whether a card should be withdrawn, appears in two loops that rewire in two different ways: one moves the sticker, and the other changes a note. Each loop has its own null guards and its own end condition, and a mistake in one of them is invisible to tests that never put a blocked card at the front, or never put two blocked cards side by side.

The pattern repeats in other operations. Inserting a card at position `p` needs a branch when `p` is zero. Building a merged chain needs a branch for the first card chosen. Every operation that might change the first card grows an `if` that looks very similar, and a real chain implementation ends up with dozens of them. The fix is to remove the cause rather than to handle it more neatly: give the first real card a predecessor so that it is no longer special.

<!-- stage: insight -->
### Give The Front A Permanent Predecessor

Create one extra node, the **dummy head**, whose value is never read, and point it at the real first node. From then on every real node has a predecessor, so an operation that changes the real front is just an operation on `dummy.next`. The caller's answer is whatever `dummy.next` holds when the work is done. The **owner reference** is the node whose `next` field is about to be written: during a removal it is the last node kept, and during a build it is the last node attached. The **stable entry** is `dummy` itself, which never moves, so the code that returns the result does not have to remember which node was first.

<!-- names: dummy head, owner reference, stable entry -->

The invariant is that `dummy.next` always names the head of the chain of kept nodes, the owner reference names the last kept node, and everything from the owner reference's successor on is untouched. A removal then reads the same for the first card and for any other: if the owner's successor is blocked, point the owner past it and stay, and otherwise move the owner forward. A build appends behind the owner and moves it. No branch asks whether the node is the first.

The dummy costs one allocation, so the time stays O(n) and the extra space O(1).

<!-- stage: variables -->
### Dummy, Owner And Candidate

The reference `dummy` is created once and its `next` initially names the head of the input, or null for an empty input. The reference `owner` starts at `dummy`, and the candidate is `owner.next`, the node that is examined next. In a build, the owner is the tail of the chain under construction, and `dummy.next` is set by the first attach through the same assignment as every other. The function returns `dummy.next`. The dummy's own value is irrelevant, so any `int` will do, but a build that must compare against the tail's value has to check for the owner being the dummy before reading it.

<!-- stage: trace -->
### Three Front Withdrawals And A Merge

Take the cards `5, 2, 5, 7, 2, 9` with the numbers 2 and 5 blocked. The owner is the dummy, and the candidate holds 5, which is blocked, so the dummy is pointed past it. The candidate now holds 2, which is blocked as well, and the dummy is pointed past it again, and then past the next 5. All three of these steps are the same line, and none of them is a special case. The candidate holding 7 is allowed, so the owner moves onto it. The candidate holding 2 is blocked, so the owner is pointed past it, and the last candidate, holding 9, is allowed. The chain reads 7, 9.

A second run merges the sorted lists `1, 3, 3, 6` and `2, 3, 6, 8` into one list in which every value appears once. The owner is the tail of the result. A node whose value equals the tail's value is skipped and the others are attached, and the first attach goes through the dummy like all the rest. The result reads 1, 2, 3, 6, 8.

```trace
{"cells":[5,2,5,7,2,9],"pointers":["owner","cand"],"steps":[{"at":{"owner":-1,"cand":0},"vars":{"list":"2>5>7>2>9"},"note":"The candidate holds 5, which is blocked, so the owner's next reference is pointed past it and the owner stays where it is. The list now reads 2, 5, 7, 2, 9."},{"at":{"owner":-1,"cand":1},"vars":{"list":"5>7>2>9"},"note":"The candidate holds 2, which is blocked, so the owner's next reference is pointed past it and the owner stays where it is. The list now reads 5, 7, 2, 9."},{"at":{"owner":-1,"cand":2},"vars":{"list":"7>2>9"},"note":"The candidate holds 5, which is blocked, so the owner's next reference is pointed past it and the owner stays where it is. The list now reads 7, 2, 9."},{"at":{"owner":-1,"cand":3},"vars":{"list":"7>2>9"},"note":"The candidate holds 7, which is allowed, so the owner moves onto it."},{"at":{"owner":3,"cand":4},"vars":{"list":"7>9"},"note":"The candidate holds 2, which is blocked, so the owner's next reference is pointed past it and the owner stays where it is. The list now reads 7, 9."},{"at":{"owner":3,"cand":5},"vars":{"list":"7>9"},"note":"The candidate holds 9, which is allowed, so the owner moves onto it."}]}
```

```trace
{"cells":[1,3,3,6,2,3,6,8],"pointers":["a","b"],"steps":[{"at":{"a":1,"b":4},"vars":{"result":"[1]"},"note":"The next node in merged order holds 1 from the first list and is attached behind the tail."},{"at":{"a":1,"b":5},"vars":{"result":"[1,2]"},"note":"The next node in merged order holds 2 from the second list and is attached behind the tail."},{"at":{"a":2,"b":5},"vars":{"result":"[1,2,3]"},"note":"The next node in merged order holds 3 from the first list and is attached behind the tail."},{"at":{"a":3,"b":5},"vars":{"result":"[1,2,3]"},"note":"The next node in merged order holds 3 from the first list and is skipped, because the tail already holds that value."},{"at":{"a":3,"b":6},"vars":{"result":"[1,2,3]"},"note":"The next node in merged order holds 3 from the second list and is skipped, because the tail already holds that value."},{"at":{"a":-1,"b":6},"vars":{"result":"[1,2,3,6]"},"note":"The next node in merged order holds 6 from the first list and is attached behind the tail."},{"at":{"a":-1,"b":7},"vars":{"result":"[1,2,3,6]"},"note":"The next node in merged order holds 6 from the second list and is skipped, because the tail already holds that value."},{"at":{"a":-1,"b":-1},"vars":{"result":"[1,2,3,6,8]"},"note":"The next node in merged order holds 8 from the second list and is attached behind the tail."}]}
```

<!-- stage: code -->
### Four Operations Behind One Dummy

```java
final class DummyCode {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node insertAt(Node head, int p, int x) {
        Node dummy = new Node(0);
        dummy.next = head;
        Node owner = dummy;
        for (int i = 0; i < p; i++) owner = owner.next;
        Node fresh = new Node(x);
        fresh.next = owner.next;
        owner.next = fresh;
        return dummy.next;
    }

    static Node mergeDistinct(Node a, Node b) {
        Node dummy = new Node(0), tail = dummy;
        while (a != null || b != null) {
            Node take;
            if (b == null || (a != null && a.value <= b.value)) { take = a; a = a.next; }
            else { take = b; b = b.next; }
            if (tail == dummy || tail.value != take.value) { tail.next = take; tail = take; }
        }
        tail.next = null;
        return dummy.next;
    }

    static Node withdraw(Node head, java.util.Set<Integer> blocked) {
        Node dummy = new Node(0);
        dummy.next = head;
        Node owner = dummy;
        while (owner.next != null) {
            if (blocked.contains(owner.next.value)) owner.next = owner.next.next;
            else owner = owner.next;
        }
        return dummy.next;
    }

    static Node removeFromEnd(Node head, int n) {
        int length = 0;
        for (Node cur = head; cur != null; cur = cur.next) length++;
        Node dummy = new Node(0);
        dummy.next = head;
        Node owner = dummy;
        for (int i = 0; i < length - n; i++) owner = owner.next;
        owner.next = owner.next.next;
        return dummy.next;
    }
}
```

Each method makes one pass, apart from `removeFromEnd`, which makes two, so all are O(n) time and O(1) extra space. In `mergeDistinct` the final `tail.next = null` cuts the last attached node away from whatever followed it in its original list.

<!-- stage: applicability -->
### When The Front May Change

Add a dummy head when the real first node may be inserted before, removed, or replaced, so that every case becomes an operation on a predecessor's `next`. The invariant is that `dummy.next` always identifies the current result head, while the owner reference names the last finalized link, so that a single line of code serves the first node and every other node.

The false friend is a dummy added by habit. When the head never changes, for example when the task only reads the list or only changes values, the dummy buys nothing, and it clutters the code with an extra node that must be skipped when the list is printed. A second false friend is forgetting to return `dummy.next`, which returns the dummy itself and puts a spurious node at the front. A third is a build that attaches nodes without cutting the last node's old `next`, which leaves a tail that still points into an input list.

Do not rely on a dummy to hide a cycle or a shared tail, since it only manages the front. In Java, allocate the dummy with any value, never compare against its value, and remember that on very long lists one extra object is cheap while an unnoticed branch can be expensive to debug.

<!-- stage: exercises -->
### Exercises

#### [Build] Prepend Without A Special Case (Author exercise)
<!-- id: ll-insert-at-position -->

**Prerequisites.** The node invariants and merge lessons of this chapter.

**Problem.** The input is a list described by its values, a position `p` and a value `x`, where `0 <= p <= n`. Insert a new node holding `x` so that it becomes the node at position `p`, counting from 0, and return the values of the result. Position 0 is the front and position `n` is the end. Use a dummy head so that no branch tests whether `p` is zero.

**Constraints.** 0 <= n <= 10^5, 0 <= p <= n and -10^9 <= x <= 10^9.

**Example 1.** Input `values = [3, 4]`, `p = 0`, `x = 9`, output `[9, 3, 4]`.

**Example 2.** Input `values = [3, 4]`, `p = 2`, `x = 7`, output `[3, 4, 7]`.

**Hint.** Which node is the owner after `p` steps from the dummy? Does the same code serve an empty list?

**Changed decision.** First rung: the front is reached through `dummy.next`, so position 0 and every other position use the same three lines.

#### [Vary] Merge Two Sorted Lists, Each Value Once (LeetCode 21)
<!-- id: ll-merge-distinct -->

**Prerequisites.** The Prepend Without A Special Case exercise above, and the merge lesson.

**Problem.** Given the heads of two sorted linked lists, merge them into one sorted list in which every value appears at most once, using the original nodes, and return the head. Of several equal nodes, the first one in merged order is kept.

**Constraints.** 0 <= n, m <= 10^5 and -10^9 <= value <= 10^9. Both lists are sorted in non-decreasing order, and either may contain repeated values.

**Example 1.** Input `a = [1, 3, 3, 6]`, `b = [2, 3, 6, 8]`, output `[1, 2, 3, 6, 8]`.

**Example 2.** Input `a = [4, 4]`, `b = []`, output `[4]`.

**Hint.** What does the tail compare against while the result is still empty? What must the last attached node's `next` be, and why?

**Changed decision.** A node is attached only when its value differs from the tail's, so some nodes are dropped, and the last attached node's `next` must be cleared.

#### [Boundary] Remove Blocked Values (LeetCode 203)
<!-- id: ll-remove-blocked -->

**Prerequisites.** The two exercises above.

**Problem.** You receive the head of a linked list and an array `blocked` of integers, remove every node whose value appears in `blocked`, and return the new head. One or many of the original first nodes may be blocked.

**Constraints.** 0 <= n <= 10^5, 0 <= blocked.length <= 100 and -10^9 <= value <= 10^9.

**Example 1.** Input `values = [5, 2, 5, 7, 2, 9]`, `blocked = [2, 5]`, output `[7, 9]`.

**Example 2.** Input `values = [1, 1]`, `blocked = [1]`, output `[]`.

**Hint.** When the first three nodes are all blocked, how many times does the head change, and which assignment changes it each time?

**Changed decision.** The match test is membership in a set and not equality with one value, and the owner stays put after a bypass because the next candidate has not been examined.

#### [Recognize] Remove Nth Node From End of List (LeetCode 19)
<!-- id: ll-remove-nth-dummy -->

**Prerequisites.** All three exercises above.

**Problem.** You receive the head of a linked list and an integer `n`; remove the `n`-th node from the end of the list and return the head. Count the length first, then walk from a dummy head.

**Constraints.** 1 <= length <= 30, 1 <= n <= length and 0 <= value <= 100.

**Example 1.** Input `values = [4, 8, 6, 3, 2]`, `n = 2`, output `[4, 8, 6, 2]`.

**Example 2.** Input `values = [7]`, `n = 1`, output `[]`.

**Hint.** Which node must the owner stop at so that deleting the target is a bypass? What does the owner hold when the target is the original first node?

**Changed decision.** A dummy predecessor makes deleting the original head an ordinary bypass, so no branch is needed for `n` equal to the length.
