<!-- lesson-kind: standard -->
<!-- lesson-id: arraydeque-mechanics -->
## Use ArrayDeque From Both Ends

<!-- stage: context -->
### Why A Plain List Slows Down

A log viewer shows the last 1,000 lines of a running service. Each new line arrives at the bottom, and the oldest line falls off the top. The first version stores the lines in an `ArrayList`, and it feels fine in testing. After a busy hour the viewer freezes. The code is correct, so the cause is the cost of one call: dropping the oldest line.

This lesson answers one question. How can a Java program add and remove items at both ends of a sequence, and pay a fixed small cost for each call? The answer is `ArrayDeque`, and the rest of the chapter depends on knowing exactly what each of its calls does.

<!-- stage: naive -->
### Using An ArrayList For Recent Items

The direct plan keeps the lines in an `ArrayList`. A new line goes to the end, and the oldest line sits at index 0.

```java
static void addLine(List<String> lines, String line, int limit) {
    lines.add(line);                 // append at the last index
    if (lines.size() > limit) {
        lines.remove(0);             // drop the oldest line
    }
}
```

The method returns the right result on every input. With a limit of 3, the stream `a, b, c, d` leaves `b, c, d` in the list.

<!-- stage: bottleneck -->
### Counting Moves When The Front Leaves

```predict
An ArrayList holds 100,000 items. How many items does one call to remove(0) move?

It moves 99,999 items, one position each, because every later item shifts left to close the gap. A stream of 100,000 such removals therefore moves about five billion items.
```

An `ArrayList` keeps its items in one array, with no gap at the front. Removing index 0 forces every other item to move one slot left. The cost of one call is O(n) for a list of size n. A viewer that drops one line for every new line pays O(n) on each arrival. A stream of m arrivals costs O(n * m) in total.

The same problem appears at the front on insertion. The call `add(0, x)` shifts every item one slot right. A method that needs the front and the back therefore has one cheap end and one expensive end. The list is O(1) at the back and O(n) at the front. The repeated work is the shifting of items that did not change.

<!-- stage: insight -->
### Letting Both Ends Move Instead

#### Moving A Boundary Instead Of The Items

The fix is to stop moving items. Keep the items where they are and move the marker that says where the sequence starts. Removing the first item then moves one marker by one slot, and no other item moves.

An `ArrayDeque` stores its items in a **circular array**, which is an ordinary array whose last slot is treated as the neighbor of slot 0. Two numbers describe the sequence inside it. The **head index** is the slot of the first item. The **tail index** is the slot where the next appended item will go.

#### Wrapping Past The Edge Of The Array

Adding at the back writes at the tail index and moves the tail index forward by one slot. Removing at the front reads at the head index and moves the head index forward by one slot. Adding at the front moves the head index back by one slot and writes there. When an index passes the edge of the array, it must **wrap around** to the other edge, so slot 0 follows the last slot. Each call touches one slot and one index, so each call costs O(1). When the array is full, the class allocates a larger array and copies the items once. This keeps the average cost of an append at O(1).

<!-- names: circular array, head index, tail index, wrap around -->

<!-- stage: variables -->
### What The Class Keeps Track Of

An `ArrayDeque` keeps four pieces of state. A caller sees only the sequence, but the cost of each call comes from these four.

- **Array** holds the items in slots, and some slots are empty.
- **Head index** is the slot of the first item, and it changes on every front call.
- **Tail index** is the next free slot at the back, and it changes on every back call.
- **Size** is the count of items, and it changes by one on every successful add or remove.

The head index and the tail index are equal when the sequence is empty. A full array would make them equal again, so the class resizes before that can happen.

<!-- stage: trace -->
### Following The Indices Through Wrapping

The two traces use a small array of six slots so every slot is visible. A real `ArrayDeque` starts larger, but the movement of the two indices is the same. The first trace mixes calls at both ends. The slot row shows the array, and the front-to-back row shows the sequence a caller sees.

In the first trace, the call `addFirst(2)` moves the head index from slot 0 back to slot 5. The sequence still reads `2, 4, 7` from front to back. No item moved, because the head index wrapped around the edge.

The second trace keeps the last three items of the stream 5, 6, 7, 8. Each append writes at the tail index. When the size reaches 4, one front removal brings it back to 3. Both indices move forward, and the occupied slots drift around the array. The sequence from front to back stays the three newest items.

```trace
{"cells":["-","-","-","-","-","-"],"pointers":["head","tail"],"steps":[{"at":{"head":0,"tail":0},"vars":{"slots":"[-,-,-,-,-,-]","front_to_back":"[]","size":0},"note":"The ring is empty, so head and tail are the same slot, 0."},{"at":{"head":0,"tail":1},"vars":{"slots":"[4,-,-,-,-,-]","front_to_back":"[4]","size":1},"note":"addLast(4) writes 4 in slot 0 and moves the tail to slot 1."},{"at":{"head":0,"tail":2},"vars":{"slots":"[4,7,-,-,-,-]","front_to_back":"[4,7]","size":2},"note":"addLast(7) writes 7 in slot 1 and moves the tail to slot 2."},{"at":{"head":5,"tail":2},"vars":{"slots":"[4,7,-,-,-,2]","front_to_back":"[2,4,7]","size":3},"note":"addFirst(2) moves the head back from slot 0 to slot 5 and writes 2 there. The head wrapped from slot 0 to the last slot, and no item moved."},{"at":{"head":5,"tail":1},"vars":{"slots":"[4,-,-,-,-,2]","front_to_back":"[2,4]","size":2},"note":"removeLast() moves the tail back to slot 1 and takes 7 from it."}]}
```

```trace
{"cells":["-","-","-","-","-","-"],"pointers":["head","tail"],"steps":[{"at":{"head":0,"tail":0},"vars":{"slots":"[-,-,-,-,-,-]","front_to_back":"[]","size":0},"note":"The history is empty."},{"at":{"head":0,"tail":1},"vars":{"slots":"[5,-,-,-,-,-]","front_to_back":"[5]","size":1},"note":"Append 5 at slot 0. The history holds 1 items."},{"at":{"head":0,"tail":2},"vars":{"slots":"[5,6,-,-,-,-]","front_to_back":"[5,6]","size":2},"note":"Append 6 at slot 1. The history holds 2 items."},{"at":{"head":0,"tail":3},"vars":{"slots":"[5,6,7,-,-,-]","front_to_back":"[5,6,7]","size":3},"note":"Append 7 at slot 2. The history holds 3 items."},{"at":{"head":0,"tail":4},"vars":{"slots":"[5,6,7,8,-,-]","front_to_back":"[5,6,7,8]","size":4},"note":"Append 8 at slot 3. The history holds 4 items."},{"at":{"head":1,"tail":4},"vars":{"slots":"[-,6,7,8,-,-]","front_to_back":"[6,7,8]","size":3},"note":"The size 4 is above the capacity 3, so the oldest item 5 is removed from the front."}]}
```

<!-- stage: code -->
### Calling Each End By Name

```java
static List<Integer> lastThree(int[] stream) {
    Deque<Integer> history = new ArrayDeque<>();
    for (int x : stream) {
        history.addLast(x);                   // O(1): write at the tail index
        if (history.size() > 3) {
            history.pollFirst();              // O(1): move the head index forward
        }
    }
    return new ArrayList<>(history);          // iterates from front to back
}
```

The calls come in pairs. Each end has an adding call, a removing call and a reading call.

- **addFirst and addLast** insert at the named end and throw `NullPointerException` for `null`.
- **removeFirst and removeLast** remove from the named end and throw `NoSuchElementException` when the deque is empty.
- **pollFirst and pollLast** remove from the named end and return `null` when the deque is empty.
- **getFirst and getLast** read the named end and throw when the deque is empty.
- **peekFirst and peekLast** read the named end and return `null` when the deque is empty.

The method calls `pollFirst`, because the size test already guarantees an item. Time is O(n) for a stream of n items, since each item is added once and removed at most once. Space is O(1) beyond the output, because the deque never holds more than four items.

<!-- stage: applicability -->
### Deciding When A Deque Fits

#### Applying The Invariant

Use a deque when the method must read or remove at both ends and must never look into the middle. The invariant of the whole chapter starts here. The front and the back keep fixed roles from the first call to the last. A call that says `First` never replaces a call that says `Last`, because the two ends hold different kinds of items.

#### Finding The False Friend

The false friend is `LinkedList`. It also implements `Deque`, and it accepts `null`, but it allocates one node object per item. That cost is a constant factor and not a different growth rate, so `LinkedList` is not wrong. The ordinary choice is `ArrayDeque`, because it uses a plain array and avoids the node objects.

Two other types look close and break the invariant. The `ArrayList` has a cheap back and an expensive front. The `Stack` class works at one end only. The `push` and `pop` calls of a deque also use the front, so a method that pushes and then reads with `peekLast` looks at the wrong end.

#### No-Go Conditions

Do not choose `ArrayDeque` when the method needs an item by position, because the class has no `get(i)`. Do not choose it when the method must store `null`, because every add call rejects it. Do not choose it when the method needs the smallest item at all times, because the order inside a deque follows the calls. The values do not decide it.

<!-- stage: exercises -->
### Exercises

#### [Build] Two-Ended Buffer (Author exercise)
<!-- id: dq-two-ended-buffer -->

**Prerequisites.** The `ArrayDeque` calls in this lesson.

**Problem.** A deque is a sequence that supports insertion and removal at both ends. Start with an empty deque of `int`. Given an array of commands, apply them in order. Each command is one of `addFirst x`, `addLast x`, `removeFirst` or `removeLast`. Return the final contents of the deque from the front to the back. Every `remove` command applies to a deque that holds at least one item.

**Constraints.** The limits are:
- **Commands** number between 0 and 1,000.
- **Values** `x` are integers between -1,000 and 1,000.
- **Validity** means no remove command meets an empty deque.
- **Output** is an `int[]`, empty when the deque ends empty.

**Example 1.** Input `["addLast 4", "addLast 7", "addFirst 2", "removeLast"]`, output `[2, 4]`.

**Example 2.** Input `["addFirst 1", "addFirst 2", "addFirst 3", "removeFirst", "addLast 9"]`, output `[2, 1, 9]`.

**Hint.** Each command names its end, so each maps to the call with the same name. Where does `addFirst 3` place the item relative to `addFirst 2`?

**Changed decision.** First exercise of the lesson: every call names its end explicitly.

#### [Vary] Bounded Recent History (Author exercise)
<!-- id: dq-bounded-history -->

**Prerequisites.** The two-ended buffer exercise above.

**Problem.** A history of capacity `c` holds the most recent items of a stream. Given an integer array `stream` and a capacity `c`, append each item at the back of the history. After an append, if the history holds more than `c` items, remove the oldest item from the front. Return the final history from oldest to newest.

**Constraints.** The limits are:
- **Capacity** `c` is between 1 and 1,000.
- **Stream length** is between 0 and 100,000.
- **Values** are 32-bit integers.
- **Output** has `min(c, stream length)` items.

**Example 1.** Input `stream = [5, 6, 7, 8]`, `c = 3`, output `[6, 7, 8]`.

**Example 2.** Input `stream = [9, 9]`, `c = 5`, output `[9, 9]`, because the history never fills.

**Hint.** The size test runs after the append, so the history briefly holds `c + 1` items. Which end loses an item?

**Changed decision.** The removal is conditional on the size, and it always takes the front.

#### [Boundary] Empty Deque Contract (Author exercise)
<!-- id: dq-empty-contract -->

**Prerequisites.** The five call pairs listed in the code stage.

**Problem.** Every access call has two forms. The throwing form fails on an empty deque. The returning form gives `null` on an empty deque. Given an array of commands for an empty `Deque<Integer>`, return one result string per command. The commands are `addLast x`, `pollFirst`, `peekLast`, `removeFirst` and `getLast`. An add command gives `"ok"`. A command that returns an item gives its decimal text. A returning command on an empty deque gives `"null"`. A throwing command on an empty deque gives `"NoSuchElementException"`.

**Constraints.** The limits are:
- **Commands** number between 0 and 1,000.
- **Values** `x` are integers between -1,000 and 1,000.
- **State** starts empty and carries across commands.
- **Output** has exactly one string per command.

**Example 1.** Input `["pollFirst", "addLast 3", "peekLast"]`, output `["null", "ok", "3"]`.

**Example 2.** Input `["removeFirst", "addLast 8", "getLast", "removeFirst", "getLast"]`, output `["NoSuchElementException", "ok", "8", "8", "NoSuchElementException"]`.

**Hint.** Which of the five commands can fail, and which of those four return `null` instead of failing? A `peekLast` does not remove anything.

**Changed decision.** The empty case becomes part of the contract, and the choice of call decides the result.

#### [Recognize] Candidate Deque API (Author exercise)
<!-- id: dq-candidate-api -->

**Prerequisites.** All calls in this lesson.

**Problem.** A later method stores candidates in a deque. For each new item it performs five steps in this order. Step 1 reads the oldest candidate. Step 2 discards the oldest candidate. Step 3 reads the newest candidate. Step 4 discards the newest candidate. Step 5 stores the new item as the newest candidate. Return an array of five strings, where entry `i` names the one `Deque` method that performs step `i + 1`. Use the form that returns `null` on empty, and use the `First` or `Last` call that matches the end.

**Constraints.** The limits are:
- **Methods** come from `peekFirst`, `pollFirst`, `peekLast`, `pollLast` and `addLast`.
- **Steps** each use exactly one method.
- **Types** are `ArrayDeque`, not `LinkedList`.
- **Output** is a `String[]` of length 5.

**Example 1.** Input step 1, which reads the oldest candidate, gives the output entry `peekFirst`.

**Example 2.** Input step 5, which stores at the newest end, gives the output entry `addLast`.

**Hint.** Decide which end holds the oldest candidate. Then match each step to reading or removing at that end.

**Changed decision.** No algorithm is written; the only decision is which end each step touches.
