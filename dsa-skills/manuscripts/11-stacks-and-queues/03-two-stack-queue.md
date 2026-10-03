<!-- lesson-kind: standard -->
<!-- lesson-id: two-stack-queue -->
## Two-Stack Queue

<!-- stage: context -->
### Two Trolleys At The Returns Desk

A small library's returns desk has no conveyor belt, only two narrow trolleys, and each trolley is a stack: a book can only be placed on top and only lifted from the top. Readers hand back books all day, and the head librarian insists that books are reshelved in the order they were returned, so the first book handed in must be the first one shelved. The librarian wants to know whether two stacks are enough to behave as a line, and how much walking back and forth between the trolleys that costs.

The desk is busy, so the librarian does not accept a scheme in which every shelving trip means emptying one trolley onto the other and back again. She also wants to know what the scheme does when a reader asks which book will be shelved next while the shelving trolley happens to be empty.

<!-- stage: naive -->
### Pour Everything Across On Every Call

The direct method keeps all books on one trolley. To shelve the oldest book, pour the whole trolley onto the second one, take the top book, and pour everything back.

```java
static int dequeueByPouring(ArrayDeque<Integer> main) {
    ArrayDeque<Integer> spare = new ArrayDeque<>();
    while (!main.isEmpty()) spare.addLast(main.removeLast());
    int oldest = spare.removeLast();
    while (!spare.isEmpty()) main.addLast(spare.removeLast());
    return oldest;
}
```

It is correct, because pouring reverses the order, so the oldest book ends on top of the spare trolley, and pouring back restores the order of the rest.

<!-- stage: bottleneck -->
### Every Shelving Trip Moves Every Book

A trolley holding n books makes each shelving trip move about 2n books, one pour out and one pour back, so a single call costs O(n). A day that returns n books and shelves them all costs O(n^2) in total, which for a hundred thousand books is on the order of ten billion lifts. Almost all of this effort is wasted, because the pour-back undoes the reversal that the pour-out just created, and the next call immediately repeats it.

The reversal is what makes the oldest book reachable, and it is worth keeping. A book that has already been poured onto the second trolley is already in shelving order, so it can stay there. If the second trolley is only refilled when it runs dry, a book is lifted onto it once and lifted off it once, and the cost of the whole day falls to O(n) in total.

<!-- stage: insight -->
### Pour Only When Output Runs Dry

Use two stacks with fixed jobs. All new values go onto the **input stack**, which therefore holds the newest values on top. All removals and peeks read the **output stack**, whose top is always the oldest value available for shelving. When a removal finds the output stack empty, the **transfer rule** applies: move every value from the input stack onto the output stack, one pop and one push each. The move reverses the order, so what was the oldest value at the bottom of the input stack is now on top of the output stack.

The invariant is that the output stack holds a prefix of the queue, oldest on top, and the input stack holds the rest, newest on top, so the whole queue is the output stack read top to bottom followed by the input stack read bottom to top. A new arrival goes on top of the input stack and so sits behind everything already there, which is exactly its place in the queue. Because transfer happens only when the output stack is empty, a value that is waiting in the output stack is never placed behind a newer one.

The accounting is the amortized argument. A value is pushed onto the input stack once, moved to the output stack at most once, and popped from the output stack at most once, so three constant-time operations pay for it in total. A single call can cost O(n) when a transfer is triggered, but any n calls together cost O(n), which is O(1) amortized per call.

<!-- names: input stack, output stack, transfer rule -->

A monotonic queue, which removes dominated values to answer extreme-value questions, is a different structure, and this lesson only emulates the plain first in first out behavior.

<!-- stage: variables -->
### Two Deques, Fixed Jobs

The code holds `in` and `out`, both `ArrayDeque<Integer>` used as stacks with `addLast`, `removeLast` and `peekLast`. The method `shift` moves every value from `in` to `out` and is called only when `out` is empty. Both `peek` and `pop` call it first, because a peek that reads an empty `out` while `in` is full would otherwise report that the queue is empty. The queue is empty only when both stacks are empty. A counter `moves` records how many values `shift` has moved, which the tests use to check the amortized bound.

<!-- stage: trace -->
### Reversal, Then Reuse

The first trace enqueues 1, 2 and 3, and then removes twice. The cells hold the script. After the three arrivals the input stack reads 1, 2, 3 from bottom to top and the output stack is empty. The first removal finds the output empty, so all three values move over and read 3, 2, 1 from bottom to top, with the oldest value 1 now on top and ready. The second removal needs no transfer at all.

```trace
{"cells":["enq 1","enq 2","enq 3","deq","deq"],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"input":"[1]","output":"[]"},"note":"The value 1 goes on top of the input stack, behind everything already in the queue."},{"at":{"op":1},"vars":{"input":"[1,2]","output":"[]"},"note":"The value 2 goes on top of the input stack, behind everything already in the queue."},{"at":{"op":2},"vars":{"input":"[1,2,3]","output":"[]"},"note":"The value 3 goes on top of the input stack, behind everything already in the queue."},{"at":{"op":3},"vars":{"input":"[]","output":"[3,2]"},"note":"The output stack was empty, so the transfer rule moves all 3 value(s) over, and the removal returns 1, the oldest."},{"at":{"op":4},"vars":{"input":"[]","output":"[3]"},"note":"The output stack is not empty, so no transfer happens and the removal returns 2."}]}
```

The second trace interleaves calls. Look at the step where 7 and 8 arrive while the output stack still holds 6: they go onto the input stack and wait behind 6, so the older value keeps its place. The transfer happens only after 6 has left and the output stack runs dry.

```trace
{"cells":["enq 5","enq 6","deq","enq 7","enq 8","deq","deq"],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"input":"[5]","output":"[]"},"note":"The value 5 goes on top of the input stack, behind everything already in the queue."},{"at":{"op":1},"vars":{"input":"[5,6]","output":"[]"},"note":"The value 6 goes on top of the input stack, behind everything already in the queue."},{"at":{"op":2},"vars":{"input":"[]","output":"[6]"},"note":"The output stack was empty, so the transfer rule moves all 2 value(s) over, and the removal returns 5, the oldest."},{"at":{"op":3},"vars":{"input":"[7]","output":"[6]"},"note":"The value 7 goes on top of the input stack, behind everything already in the queue."},{"at":{"op":4},"vars":{"input":"[7,8]","output":"[6]"},"note":"The value 8 goes on top of the input stack, behind everything already in the queue."},{"at":{"op":5},"vars":{"input":"[7,8]","output":"[]"},"note":"The output stack is not empty, so no transfer happens and the removal returns 6."},{"at":{"op":6},"vars":{"input":"[]","output":"[8]"},"note":"The output stack was empty, so the transfer rule moves all 2 value(s) over, and the removal returns 7, the oldest."}]}
```

<!-- stage: code -->
### Enqueue, Shift, Peek And Pop

```java
static final class TwoStackQueue {
    private final ArrayDeque<Integer> in = new ArrayDeque<>();
    private final ArrayDeque<Integer> out = new ArrayDeque<>();
    int moves;

    void push(int x) { in.addLast(x); }

    private void shift() {
        if (!out.isEmpty()) return;
        while (!in.isEmpty()) { out.addLast(in.removeLast()); moves++; }
    }

    int peek() { shift(); return out.peekLast(); }

    int pop() { shift(); return out.removeLast(); }

    boolean isEmpty() { return in.isEmpty() && out.isEmpty(); }
}
```

A call to `push` is O(1), and a call to `peek` or `pop` is O(n) in the worst case when a transfer happens, but each value is moved at most once, so any sequence of m calls costs O(m) and the space is O(n).

<!-- stage: applicability -->
### When Only Stacks Are Allowed

Use this when the available container is last in first out and the public behavior has to be first in first out, as in interview prompts that forbid a queue class, or in systems where one stack is cheap to undo. The invariant is that the output stack holds the oldest values with the oldest on top and the input stack holds the newest values, and a transfer is done only when the output stack is empty.

A false friend is to move everything on every operation, which is correct and costs linear time per call. A second false friend is to move on every dequeue only when the input stack is larger, which breaks the order as soon as an older value is stranded under a newer one. A third is to read the empty flag of the output stack alone, which reports an empty queue while the input stack still holds values.

In Java, give each stack a fixed role and name it after its role. Have `peek` shift exactly as `pop` does. State what happens on an empty call: either the contract forbids it, or the method returns a documented value, and in both cases check `isEmpty()` through both stacks before the call.

<!-- stage: exercises -->
### Exercises

#### [Build] Enqueue And One Dequeue (Author exercise)
<!-- id: sq-enqueue-one-dequeue -->

**Prerequisites.** The FIFO Simulation lesson.

**Problem.** Enqueue all the given values into a two-stack queue, then dequeue exactly once. Return the dequeued value followed by the contents of the output stack from bottom to top after that dequeue.

**Constraints.** 1 <= values.length <= 100000 and -1000000000 <= values[i] <= 1000000000.

**Example 1.** Input `values = [4, 5, 6]`, output `[4, 6, 5]`.

**Example 2.** Input `values = [9]`, output `[9]`.

**Hint.** In which order do the values sit on the output stack after the transfer? Which one is on top?

**Changed decision.** First rung: a transfer reverses the input stack, so the output stack from bottom to top lists the remaining values in reverse arrival order.

#### [Vary] Interleaved Queue Calls (Author exercise)
<!-- id: sq-interleaved-queue-calls -->

**Prerequisites.** The Enqueue And One Dequeue rung.

**Problem.** A script is an array of integers: a nonnegative value enqueues it, -1 dequeues, and -2 peeks at the oldest value without removing it. Return the results of every -1 and -2 command in order. Every -1 and -2 finds a nonempty queue.

**Constraints.** 0 <= script.length <= 100000 and each script value is -2, -1, or between 0 and 1000000000.

**Example 1.** Input `script = [5, 6, -1, 7, 8, -2, -1, -1]`, output `[5, 6, 6, 7]`.

**Example 2.** Input `script = [3, -2, -2, -1]`, output `[3, 3, 3]`.

**Hint.** When 7 and 8 arrive while the output stack is not empty, where do they go? Does a peek need the transfer rule too?

**Changed decision.** New values arrive while the output stack is nonempty, so older values must stay in front of them, and a peek triggers the same transfer as a removal.

#### [Boundary] Empty Queue API (Author exercise)
<!-- id: sq-empty-queue-api -->

**Prerequisites.** The Interleaved Queue Calls rung.

**Problem.** Run the same script, but now a -1 or -2 command may find the queue empty. In that case it returns -1, which is no valid stored value, and changes nothing. Return the result of every -1 and -2 command in order. Be careful when the output stack is empty but the input stack is not.

**Constraints.** 0 <= script.length <= 100000 and each script value is -2, -1, or between 0 and 1000000000.

**Example 1.** Input `script = [-2, 4, -2, -1, -1]`, output `[-1, 4, 4, -1]`.

**Example 2.** Input `script = [1, 2, -1, 3, -1, -1, -1]`, output `[1, 2, 3, -1]`.

**Hint.** When is the queue truly empty? What is wrong with testing only the output stack?

**Changed decision.** Emptiness is decided from both stacks together, and an empty call returns the documented value instead of throwing.

#### [Recognize] Implement Queue using Stacks (LeetCode 232)
<!-- id: sq-implement-queue-stacks -->

**Prerequisites.** The Empty Queue API rung.

**Problem.** Implement a queue with `push`, `pop`, `peek` and `empty` using only stack operations. The input is a list of command strings, and the output holds one string per command: a dash for `push x`, the value for `pop` and `peek`, and `true` or `false` for `empty`. Every `pop` and `peek` finds a nonempty queue. Each value must move between the stacks at most once.

**Constraints.** 1 <= commands.length <= 100000 and every pushed value is between 0 and 1000000000.

**Example 1.** Input `commands = ["push 1", "push 2", "peek", "pop", "empty"]`, output `["-", "-", "1", "1", "false"]`.

**Example 2.** Input `commands = ["push 7", "pop", "empty"]`, output `["-", "7", "true"]`.

**Hint.** Which stack is read by `pop`, and when is it refilled? How many times can one value be moved?

**Changed decision.** The full interface is built on the transfer rule, so the amortized bound of one move per value must hold across every call.
