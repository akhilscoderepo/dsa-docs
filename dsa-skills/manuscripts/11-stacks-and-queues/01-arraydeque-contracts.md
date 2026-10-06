<!-- lesson-kind: standard -->
<!-- lesson-id: arraydeque-contracts -->
## Use ArrayDeque For Stack And Queue

<!-- stage: context -->
### A Marker That Crashes The Search

A breadth-first search over a graph needs to know where one level ends and the next begins. A programmer adds a `null` element to an `ArrayDeque` as the divider. The program throws `NullPointerException` on the first insertion of that divider. The same programmer keeps an undo log in `java.util.Stack`. That code runs, but any caller can also read or insert at an arbitrary index, so the log can stop behaving like a log.

Both failures come from the same gap. The programmer did not know which end of the deque holds which element, and did not know what the deque promises. The lesson answers one question. Which exact calls make `ArrayDeque` behave as a stack or as a queue, and what does each call do when the deque is empty or receives `null`?

<!-- stage: naive -->
### Use The Collection That Comes To Mind

Most programmers reach for `java.util.Stack` for last-in access and for an `ArrayList` for waiting items. The list takes new items at the end and removes the oldest item at index 0.

```java
static int[] reverseWithStack(int[] values) {
    java.util.Stack<Integer> st = new java.util.Stack<>();
    for (int v : values) st.push(v);
    int[] out = new int[values.length];
    for (int i = 0; i < out.length; i++) out[i] = st.pop();
    return out;
}

static int[] drainWithList(int[] values) {
    java.util.List<Integer> waiting = new java.util.ArrayList<>();
    for (int v : values) waiting.add(v);
    int[] out = new int[values.length];
    for (int i = 0; i < out.length; i++) out[i] = waiting.remove(0);
    return out;
}
```

Both methods return correct results. The first reverses the input, and the second keeps the input order.

<!-- stage: bottleneck -->
### Costs Of The Naive Pair

```predict
A list holds 1000 integers. Each `remove(0)` shifts every remaining element one slot to the left. How many element moves does draining the whole list cost?

The first call moves 999 elements, the second moves 998, and the last moves none. The total is 999 + 998 + ... + 0, which equals 499500 moves. The count grows as n squared over 2, so doubling the list quadruples the work.
```

Draining a list of `n` items by `remove(0)` costs O(n^2) in total, because each call shifts the rest of the array. A queue needs O(1) per removal. `Stack` extends `Vector`, so every call also takes a lock that single-threaded code never needs, and `Stack` exposes `get(i)` and `add(i, x)`. Those methods let code read or insert in the middle, and then the structure no longer promises that only one end changes.

The second problem is a missing contract. The code must also say what happens on an empty structure and with `null`. A removal that returns `null` for empty cannot be told apart from a stored `null`. The structure needs one end per meaning and a clear answer for both cases.

<!-- stage: insight -->
### One End Per Meaning

`ArrayDeque` is a resizable circular array that adds and removes at both ends in amortized O(1) time. It has no index access, so the interface offers only end operations. The lesson fixes which end plays which role and keeps that choice for the whole implementation.

#### Choosing A Stack Or A Queue

A stack follows **LIFO**, last in, first out, so the most recently added element leaves first. A queue follows **FIFO**, first in, first out, so the earliest added element leaves first. Both structures add at the last end with `addLast`. A stack removes and reads at the last end with `removeLast` and `peekLast`. A queue removes and reads at the first end with `removeFirst` and `peekFirst`.

#### The Two Ways To Report Empty

Every end operation exists in two forms. `removeFirst`, `removeLast`, `getFirst`, `getLast`, `remove` and `element` throw `NoSuchElementException` when the deque is empty. The forms `pollFirst`, `pollLast`, `peekFirst` and `peekLast` return `null` instead, and the word **poll** names this removal that returns `null` for empty. A `poll` result of `null` is unambiguous only because `ArrayDeque` rejects `null` elements and throws `NullPointerException` on `addLast(null)`.

<!-- names: LIFO, FIFO, poll -->

An invariant holds across the code. One end has one meaning, and no method mixes the two ends. The calls `push`, `pop` and `peek` work on the first end, so mixing them with `peekLast` breaks a stack silently.

<!-- stage: variables -->
### State In A Deque Based Loop

The state is small, and each piece changes at known moments.

- **deque** is the `ArrayDeque<Integer>` that holds the waiting elements; it starts empty and changes only at its two ends.
- **last end** receives every `addLast` call and, for a stack, also supplies every removal.
- **first end** supplies every removal for a queue and is never written by a stack.
- **size** is `deque.size()`, and it decides whether a removal is legal when the code chose the throwing form.

<!-- stage: trace -->
### Same Input, Two Removal Orders

Both traces use the input values 4, 7 and 9. The cells are the input, and the pointer `in` marks the next input index. The variable `deque` shows the contents from first end to last end, and `out` shows the values removed so far.

The stack trace adds all three values at the last end. It then removes three times at the last end, so the output is 9, 7, 4. The deque never holds an element between the two ends that is out of place, because only one end changes after the additions.

```trace
{"cells":[4,7,9],"pointers":["in"],"steps":[{"at":{"in":0},"vars":{"deque":"[4]","out":"[]"},"note":"addLast(4) puts 4 at the last end."},{"at":{"in":1},"vars":{"deque":"[4, 7]","out":"[]"},"note":"addLast(7) puts 7 at the last end."},{"at":{"in":2},"vars":{"deque":"[4, 7, 9]","out":"[]"},"note":"addLast(9) puts 9 at the last end."},{"at":{"in":3},"vars":{"deque":"[4, 7]","out":"[9]"},"note":"removeLast() returns 9."},{"at":{"in":3},"vars":{"deque":"[4]","out":"[9, 7]"},"note":"removeLast() returns 7."},{"at":{"in":3},"vars":{"deque":"[]","out":"[9, 7, 4]"},"note":"removeLast() returns 4."}]}
```

The queue trace adds the same values at the last end in the same order. It removes at the first end, so the output is 4, 7, 9. The only change from the first trace is which end supplies removals, and that one change turns reversal into preserved order.

```trace
{"cells":[4,7,9],"pointers":["in"],"steps":[{"at":{"in":0},"vars":{"deque":"[4]","out":"[]"},"note":"addLast(4) puts 4 at the last end."},{"at":{"in":1},"vars":{"deque":"[4, 7]","out":"[]"},"note":"addLast(7) puts 7 at the last end."},{"at":{"in":2},"vars":{"deque":"[4, 7, 9]","out":"[]"},"note":"addLast(9) puts 9 at the last end."},{"at":{"in":3},"vars":{"deque":"[7, 9]","out":"[4]"},"note":"removeFirst() returns 4."},{"at":{"in":3},"vars":{"deque":"[9]","out":"[4, 7]"},"note":"removeFirst() returns 7."},{"at":{"in":3},"vars":{"deque":"[]","out":"[4, 7, 9]"},"note":"removeFirst() returns 9."}]}
```

<!-- stage: code -->
### Stack And Queue Methods

#### Methods With Fixed Ends

The first method uses the last end for both adding and removing. The second uses the last end for adding and the first end for removing.

```java
static int[] asStack(int[] values) {
    java.util.ArrayDeque<Integer> dq = new java.util.ArrayDeque<>();
    for (int v : values) dq.addLast(v);
    int[] out = new int[values.length];
    for (int i = 0; i < out.length; i++) out[i] = dq.removeLast();
    return out;
}

static int[] asQueue(int[] values) {
    java.util.ArrayDeque<Integer> dq = new java.util.ArrayDeque<>();
    for (int v : values) dq.addLast(v);
    int[] out = new int[values.length];
    for (int i = 0; i < out.length; i++) out[i] = dq.removeFirst();
    return out;
}
```

#### Removal That Reports Empty

When emptiness is a legal case, use the `poll` form and test the result. When the algorithm proves the deque is non-empty, use the throwing form so a broken proof fails loudly.

```java
static int takeOrDefault(java.util.ArrayDeque<Integer> dq, int fallback) {
    Integer head = dq.pollFirst();
    return head == null ? fallback : head;
}
```

Each method runs in O(n) time for `n` values and uses O(n) space for the deque. A single end operation runs in amortized O(1) time.

<!-- stage: applicability -->
### Checking The Contract Before Choosing

#### Recognizing The Access Pattern

Use `ArrayDeque` when the algorithm needs only last-in access or arrival-order access, with no search by position. The invariant is that each end keeps one meaning for the entire program. Undo logs, call-order tracking and request buffers fit this shape.

#### Legacy Stack Is A False Friend

`java.util.Stack` looks like the natural name for a stack, and its `push` and `pop` work. That is the false friend. It stays correct for simple use, but its index methods break the one-end rule and its synchronized methods add cost. Prefer `ArrayDeque` for ordinary stacks.

#### The Null Hazard And Its Fix

The Java hazard is that `ArrayDeque` throws on `null`. A level divider must therefore be a real value. Use a sentinel value that the data cannot contain, such as `-1` for non-negative data, or count the elements per level and keep the count in an `int`. Do not use a deque when the algorithm must read the middle element, because no deque operation does that.

<!-- stage: exercises -->
### Exercises

#### [Build] Deque As Stack (Author exercise)
<!-- id: sq-deque-as-stack -->

**Prerequisites.** The stack calls in this lesson.

**Problem.** Given an integer array `values`, insert its elements into one `ArrayDeque<Integer>` in index order, then remove every element and return the removed values in removal order. Use only the last end of the deque for both insertion and removal.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 10^5`.
- **Values** are any `int` values.
- **Return** is a new `int[]` of the same length; the input does not change.

**Example 1.** Input `[4,7,9]`, output `[9,7,4]`.

**Example 2.** Input `[2,2,5,1]`, output `[1,5,2,2]`.

**Hint.** The element added last must leave first. Which end do both calls need?

**Changed decision.** Basic case: one end holds the whole meaning, so the output is the reversed input.

#### [Vary] Deque As Queue (Author exercise)
<!-- id: sq-deque-as-queue -->

**Prerequisites.** The exercise above.

**Problem.** Take an integer array `values` and an empty `ArrayDeque<Integer>`. Add the elements in index order, then remove them all and return the removed values in removal order. Add at the last end and remove at the first end.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 10^5`.
- **Values** are any `int` values, including duplicates.
- **Return** is a new `int[]` of the same length; the input does not change.

**Example 1.** Input `[4,7,9]`, output `[4,7,9]`.

**Example 2.** Input `[5,5,2]`, output `[5,5,2]`.

**Hint.** Only the end used for removal differs from the previous exercise.

**Changed decision.** Removal moves to the first end, so the output keeps arrival order.

#### [Boundary] Empty Access Contract (Author exercise)
<!-- id: sq-empty-access-contract -->

**Prerequisites.** The two exercises above and the two forms of each end operation.

**Problem.** An `ArrayDeque<Integer>` starts empty. Each command is one of `"add v"` with an integer `v`, `"poll"`, `"remove"`, `"peek"` or `"element"`. `add` inserts at the last end. The other four read the first end, and `poll` and `remove` also delete that element. Return one string per command: `"ok"` for `add`, the element as text on success, `"null"` when `poll` or `peek` meets an empty deque, and `"NoSuchElementException"` when `remove` or `element` meets an empty deque.

**Constraints.** The limits are:
- **Length** is `0 <= commands.length <= 10^4`.
- **Values** are `int` values in `add`, and the code never stores `null`.
- **Return** is a `String[]` with one entry per command.

**Example 1.** Input `["poll","add 3","peek","remove","remove"]`, output `["null","ok","3","3","NoSuchElementException"]`.

**Example 2.** Input `["element","add 8","element","poll","peek"]`, output `["NoSuchElementException","ok","8","8","null"]`.

**Hint.** Which two forms throw and which two return `null`? Catch only the exception that the contract names.

**Changed decision.** Empty is a legal state, so each command needs its own empty answer.

#### [Recognize] Choose The Ends (Author exercise)
<!-- id: sq-choose-the-ends -->

**Prerequisites.** All three exercises above.

**Problem.** A program records events and takes them back out. A positive integer in `events` records that event. The value `0` takes one recorded event back. When `mode` is `"undo"`, a take returns the most recently recorded event, as an editor undo log does. When `mode` is `"buffer"`, a take returns the earliest recorded event, as a request buffer does. Return the taken values in order, with `-1` for a take on nothing recorded. Use one `ArrayDeque<Integer>` and the exact end operations of the mode.

**Constraints.** The limits are:
- **Length** is `0 <= events.length <= 10^5`.
- **Values** are `0` or positive `int` values.
- **Mode** is exactly `"undo"` or `"buffer"`.
- **Return** is an `int[]` with one entry per `0` in `events`.

**Example 1.** Input `[3,8,0,5,0,0,0]` with `"undo"`, output `[8,5,3,-1]`.

**Example 2.** Input `[3,8,0,5,0,0,0]` with `"buffer"`, output `[3,8,5,-1]`.

**Hint.** The recording call is identical for both modes. Which end should supply the take, and which form returns `null` when nothing is recorded?

**Changed decision.** The mode chooses the end, and a take on an empty deque returns `-1` and does not throw.
