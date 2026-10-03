<!-- lesson-kind: standard -->
<!-- lesson-id: arraydeque-contracts -->
## ArrayDeque Contracts

<!-- stage: context -->
### Trays And Ticket Lines

A bakery keeps two small pieces of furniture behind the counter. The first is a spring-loaded stack of clean trays: the baker always takes the tray on top, and a washed tray is always put back on top. The second is a ticket line at the pickup window, where customers are served strictly in the order they joined. The shop is moving its bookkeeping to a small program, and the owner wants both pieces of furniture modelled with the same Java container, so that the program does not need two different data structures for what are, physically, two rules about which end to use.

The programmer's first worry is not speed but meaning. If the same container is used with one end for trays and the other end for tickets, a careless method call can quietly turn the tray stack into a line. She also hears that Java's container refuses some values, and she wants to know what happens when the baker reaches for a tray that is not there.

<!-- stage: naive -->
### Use A List With Index Arithmetic

The first idea is a plain `ArrayList`. The tray stack uses the last position, and the ticket line takes from position zero.

```java
static int servedInOrder(int[] arrivals) {
    List<Integer> line = new ArrayList<>();
    for (int ticket : arrivals) line.add(ticket);
    int checksum = 0;
    while (!line.isEmpty()) {
        int next = line.remove(0);
        checksum = checksum * 31 + next;
    }
    return checksum;
}

static int trayOnTop(List<Integer> trays) {
    return trays.get(trays.size() - 1);
}
```

It is correct, because `remove(0)` really does hand back the oldest ticket and `get(size - 1)` really is the newest tray, so both rules are followed.

<!-- stage: bottleneck -->
### Removing From Position Zero Shifts Everything

An `ArrayList` keeps its elements packed in one array, so removing at position zero moves every remaining element one place to the left. For a line of n tickets the first removal moves n minus one elements, the next moves n minus two, and so on, which is O(n^2) work to serve the whole line. A day with a hundred thousand tickets means about five billion element moves, all of them spent keeping the array packed and none of them serving a customer.

The cost has nothing to do with the rule being implemented. A line only ever touches its two ends, yet the list is built to support removal anywhere, and it pays for that freedom on every call. A container that records where the front and the back currently sit, and moves those markers instead of the data, can add and remove at either end in constant time, which makes the whole line cost O(n).

<!-- stage: insight -->
### Pick The Ends Once And Keep Them

`ArrayDeque` is that container. It is a double-ended queue, so it can add and remove at both of its ends in constant time, and the important decision is which end plays which role. The rule that keeps programs honest is to give each end exactly one meaning for the whole program. For a stack, choose a single **stack end** and use `addLast`, `removeLast` and `peekLast` on it. For a line, add at the back and remove from the **queue front** with `addLast`, `removeFirst` and `peekFirst`. Because the same two ends serve both, the choice shows up in the method names, and a reader can audit it at a glance.

The invariant is that every element enters at the end the structure names for arrivals and leaves from the end it names for departures, and nothing else touches the other end. If one method pushes with `push`, which is `addFirst`, and another reads with `peekLast`, the container still runs but the two methods disagree about which end is the top, and the bug is silent.

Two contracts decide what happens at the edges. Methods in the throwing family, `removeFirst`, `removeLast`, `getFirst` and `getLast`, raise `NoSuchElementException` on an empty container. Methods in the polling family, `pollFirst`, `pollLast`, `peekFirst` and `peekLast`, return `null` instead. That return value is only unambiguous because `ArrayDeque` enforces a **null ban**: adding `null` throws `NullPointerException`, so a returned `null` always means empty and never means a stored value.

<!-- names: stack end, queue front, null ban -->

Java's old `Stack` class works, but it extends `Vector`, which synchronizes every call and exposes index-based methods that break the stack discipline, so `ArrayDeque` is the preferred choice for ordinary stacks.

<!-- stage: variables -->
### One Deque, Two Named Ends

The code needs a single variable, `deque`, declared as `ArrayDeque<Integer>`, and each program fixes in a comment which end is the arrival end and which end is the departure end. For the stack the arrival end and the departure end are the same, the last position. For the line they differ: arrivals go to the last position and departures leave from the first. A result array `out` collects removed values in the order they leave. When a removal might hit an empty container, the code checks `isEmpty()` or uses the polling method, so the decision between an exception and `null` is made in the open.

<!-- stage: trace -->
### Three Pushes And Two Removals

The first trace uses the values 4, 7 and 1 as a stack with `addLast` and `removeLast`. The cells hold the script of operations, and `op` points at the one being run. After the three arrivals the deque holds 4, 7, 1 from the first position to the last, and the first removal returns 1, the value that arrived last. The second removal returns 7, so the values come out in reverse arrival order.

```trace
{"cells":["addLast 4","addLast 7","addLast 1","removeLast","removeLast"],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"deque":"[4]","out":"[]"},"note":"The value 4 goes to the last position, so it becomes the top of the stack."},{"at":{"op":1},"vars":{"deque":"[4,7]","out":"[]"},"note":"The value 7 goes to the last position, so it becomes the top of the stack."},{"at":{"op":2},"vars":{"deque":"[4,7,1]","out":"[]"},"note":"The value 1 goes to the last position, so it becomes the top of the stack."},{"at":{"op":3},"vars":{"deque":"[4,7]","out":"[1]"},"note":"The removal takes from the last position and returns 1, the value that arrived most recently."},{"at":{"op":4},"vars":{"deque":"[4]","out":"[1,7]"},"note":"The removal takes from the last position and returns 7, the value that arrived most recently."}]}
```

The second trace asks what each method does on an empty deque. The polling methods return `null` and the throwing ones raise an exception, and adding `null` is refused even when the deque is not empty. Notice the last two steps: both of them fail for different reasons, one because nothing is stored and the other because the value itself is forbidden.

```trace
{"cells":["pollFirst","peekFirst","removeFirst","addLast null","addLast 5","addLast null"],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"result":"null","deque":"[]"},"note":"The deque is empty, so pollFirst returns null instead of throwing."},{"at":{"op":1},"vars":{"result":"null","deque":"[]"},"note":"The deque is empty, so peekFirst returns null too, and the null can only mean empty."},{"at":{"op":2},"vars":{"result":"NoSuchElementException","deque":"[]"},"note":"The deque is still empty, but removeFirst belongs to the throwing family, so it raises NoSuchElementException."},{"at":{"op":3},"vars":{"result":"NullPointerException","deque":"[]"},"note":"Adding null is refused with NullPointerException even though the deque is empty, so nothing is stored."},{"at":{"op":4},"vars":{"result":"stored 5","deque":"[5]"},"note":"The value 5 is added at the last position, and the deque now holds one element."},{"at":{"op":5},"vars":{"result":"NullPointerException","deque":"[5]"},"note":"Adding null is refused again, and the deque still holds only 5."}]}
```

<!-- stage: code -->
### Stack, Line, And Safe Access

```java
static int[] reverseWithStack(int[] values) {
    ArrayDeque<Integer> stack = new ArrayDeque<>();
    for (int v : values) stack.addLast(v);
    int[] out = new int[values.length];
    for (int i = 0; i < out.length; i++) out[i] = stack.removeLast();
    return out;
}

static int[] keepWithLine(int[] values) {
    ArrayDeque<Integer> line = new ArrayDeque<>();
    for (int v : values) line.addLast(v);
    int[] out = new int[values.length];
    for (int i = 0; i < out.length; i++) out[i] = line.removeFirst();
    return out;
}

static int frontOrDefault(ArrayDeque<Integer> deque, int fallback) {
    Integer head = deque.peekFirst();
    return head == null ? fallback : head;
}
```

Each loop performs one constant-time add and one constant-time removal per value, so the time is O(n) and the extra space is O(n) for the deque and the output array. The last method is O(1), and it is safe because a null result can only mean empty.

<!-- stage: applicability -->
### When A Deque Is The Right Box

Reach for `ArrayDeque` whenever the algorithm only touches the ends of a sequence: undo logs, request buffers, pending work and anything described as last in first out or first in first out. The invariant is that each end has one fixed meaning and every method in the program uses the ends consistently.

A false friend is the legacy `Stack`, which behaves correctly for simple use but carries synchronization and index methods that a stack never needs. A second false friend is `LinkedList`, which also accepts `null`, so a null result from `poll` can no longer be told apart from a stored value. A third is `ArrayList.remove(0)`, which is correct and quietly quadratic.

In Java, remember that `push` and `pop` work on the front while `add` and `offer` work on the back, so mixing the two families flips the structure by accident. Choose the throwing methods when an empty access is a bug that should stop the program, and the polling methods when empty is a normal state. Never try to store `null`, and use a small marker object or a level-size count when a separator is needed.

<!-- stage: exercises -->
### Exercises

#### [Build] Deque As Stack (Author exercise)
<!-- id: sq-deque-as-stack -->

**Prerequisites.** Arrays and loops, and the idea of last in first out.

**Problem.** Given an array of integers, push the values onto an `ArrayDeque` in order and return the values in the order they are popped. Use one end for both pushing and popping.

**Constraints.** 0 <= values.length <= 100000 and -1000000000 <= values[i] <= 1000000000.

**Example 1.** Input `values = [3, 1, 4]`, output `[4, 1, 3]`.

**Example 2.** Input `values = []`, output `[]`.

**Hint.** Which end receives each value, and which end must the pops use to give the newest first?

**Changed decision.** First rung: both pushing and popping share one end, so the output is the input reversed.

#### [Vary] Deque As Queue (Author exercise)
<!-- id: sq-deque-as-queue -->

**Prerequisites.** Deque As Stack.

**Problem.** A script is an array of integers. A nonnegative value enqueues that value, and the value -1 dequeues one value. Return the dequeued values in the order they leave. Every -1 in the script is guaranteed to find a nonempty queue.

**Constraints.** 0 <= script.length <= 100000, every script value is -1 or between 0 and 1000000000, and the number of -1 values never exceeds the number of enqueues before it.

**Example 1.** Input `script = [5, 8, -1, 2, -1, -1]`, output `[5, 8, 2]`.

**Example 2.** Input `script = [7, -1, 9, -1]`, output `[7, 9]`.

**Hint.** Which end takes arrivals and which end gives departures, if the oldest value must leave first?

**Changed decision.** The departure end moves to the opposite side from the arrival end, so values leave in arrival order.

#### [Boundary] Empty Access Contract (Author exercise)
<!-- id: sq-empty-access-contract -->

**Prerequisites.** Deque As Queue.

**Problem.** Run a script of commands on an `ArrayDeque<Integer>`. The commands are `add x` for `addLast`, `poll` for `pollFirst`, `remove` for `removeFirst`, `peek` for `peekFirst`, `element` for `getFirst`, and `addnull` for `addLast(null)`. For each command return the printed result: the value, the word `null`, or the name of the exception class that Java throws, such as `NoSuchElementException`. A command that throws changes nothing.

**Constraints.** 0 <= commands.length <= 1000 and every `x` is between -1000 and 1000.

**Example 1.** Input `commands = ["poll", "add 4", "peek", "remove", "remove"]`, output `["null", "-", "4", "4", "NoSuchElementException"]`.

**Example 2.** Input `commands = ["addnull", "add 1", "element", "poll"]`, output `["NullPointerException", "-", "1", "1"]`.

**Hint.** Which commands return `null`, which throw, and which return nothing at all? What does `add` print?

**Changed decision.** The empty and null edges are chosen by method family, so a command's printed result depends on the contract of the method called.

#### [Recognize] Choose The Ends (Author exercise)
<!-- id: sq-choose-the-ends -->

**Prerequisites.** Empty Access Contract.

**Problem.** A hidden container receives a script: a positive number inserts that number, and 0 removes one value. The array `seen` lists the removed values in order. Return `"STACK"` if only last-in-first-out explains `seen`, `"QUEUE"` if only first-in-first-out explains it, `"BOTH"` if either does, and `"NEITHER"` otherwise.

**Constraints.** 0 <= script.length <= 1000, every positive insert is at most 1000000, and each removal in the script finds a nonempty container.

**Example 1.** Input `script = [1, 2, 3, 0, 0], seen = [3, 2]`, output `"STACK"`.

**Example 2.** Input `script = [1, 0, 2, 0], seen = [1, 2]`, output `"BOTH"`.

**Hint.** Replay the script on a stack and on a queue, and compare each replay with `seen`.

**Changed decision.** The container's rule is unknown, so the code recognizes it by replaying both rules on the same script.
