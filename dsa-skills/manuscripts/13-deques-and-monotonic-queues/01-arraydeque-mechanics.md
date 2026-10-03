<!-- lesson-kind: standard -->
<!-- lesson-id: arraydeque-mechanics -->
## ArrayDeque Mechanics

<!-- stage: context -->
### A Train With Two Doors

A small shunting yard keeps a train of freight wagons on a single track. A wagon can be coupled on at the front or at the back, and the yard master can uncouple the wagon at either end. Wagons in the middle are out of reach, because the train is too heavy to open up. Over a shift the yard master adds a wagon at the back for ordinary cargo, puts an urgent wagon at the front, and removes a wagon from whichever end the schedule names.

The yard master never walks along the train to find a wagon. She only ever looks at the first wagon or the last wagon, and every coupling or uncoupling takes the same short time however long the train has grown. A shift of ten thousand changes should therefore cost ten thousand short jobs. She also keeps a rule that every wagon must have a real load, and an empty flatbed with nothing on it is refused at the gate.

<!-- stage: naive -->
### Keep The Train In An Ordinary List

The direct way to represent a line of items with two usable ends is an `ArrayList`. Adding at the back is `add(x)`, adding at the front is `add(0, x)`, and removing from the front is `remove(0)`.

```java
static java.util.ArrayList<Integer> train = new java.util.ArrayList<>();

static void addBack(int load)  { train.add(load); }
static void addFront(int load) { train.add(0, load); }
static int removeFront()       { return train.remove(0); }
static int removeBack()        { return train.remove(train.size() - 1); }
```

It works. After `addBack(4)`, `addFront(7)` and `addBack(9)` the list holds `[7, 4, 9]`, and `removeFront()` returns 7 and leaves `[4, 9]`.

<!-- stage: bottleneck -->
### Every Front Job Shifts The Whole Line

An `ArrayList` keeps its items in one block of memory, in order. Inserting or removing at index 0 moves every other item one place over, so the job costs time proportional to the current length. A train of 100,000 wagons that gets 100,000 front changes performs about five billion item moves, which is O(n^2) for `n` front jobs, whereas the jobs at the back cost O(1) each. A sliding structure that evicts the oldest entry every step would pay that shifting cost every step.

The shifting is wasted because the yard master never asks for a wagon in the middle. The structure promises positions that she does not need, and she pays for the promise at every front job. What the problem needs is a structure that gives up access to the middle and in exchange makes both ends cheap.

<!-- stage: insight -->
### Two Ends, One Circle, No Middle

Java's `ArrayDeque` stores its items in an array treated as a **circular buffer**. It keeps a `head` index that marks the first item and a `tail` index that marks the next free slot after the last item. Adding at the front moves `head` one step backward, wrapping from slot 0 to the last slot, and adding at the back writes at `tail` and moves it one step forward. Removing moves the same indices the other way. No item is ever shifted, so each of `addFirst`, `addLast`, `pollFirst`, `pollLast`, `peekFirst` and `peekLast` takes constant time, apart from the occasional doubling of the array when the circle is full, which averages out to constant.

The price is that the middle can't be indexed. In return the structure gives **end roles**: the algorithm decides, once, what the front means and what the back means, and then each method call is one of four moves, `addFirst`, `addLast`, `removeFirst` or `removeLast`, plus the two peeks. Mixing the stack-style names `push` and `pop`, which act on the front, with the queue-style names that act on the back is how the roles get confused, so a method that uses a deque should pick one vocabulary and stay with it.

The third piece is the **empty contract**. Some methods throw when the deque is empty: `removeFirst`, `removeLast`, `getFirst`, `getLast`. Others return `null` instead: `pollFirst`, `pollLast`, `peekFirst`, `peekLast`. Because the deque does not accept `null` items, a `null` result is an unambiguous sign of emptiness, and that is why the null ban exists. The decision between the two families is made on purpose, by asking whether an empty deque is a bug in the caller or a normal state.

<!-- names: circular buffer, end roles, empty contract -->

Each operation is O(1) amortized, and the structure uses O(n) memory for `n` stored items.

<!-- stage: variables -->
### Head, Tail And End Roles

In the circular buffer the `head` is the slot of the first item and the `tail` is the slot just past the last item, and an empty deque is the state in which both are equal. The count of items is `tail - head`, taken modulo the buffer length. In an algorithm built on a deque the more important variables are the roles: which end holds the oldest item, which end receives new items, and which end is read for the answer. Fix these three decisions before writing code, and let the method names carry them: new items go in with `addLast`, the oldest leave with `pollFirst`, and the item that is read for the answer is `peekFirst`. When an empty deque is possible, use the peek and poll family, whose `null` result is tested explicitly, and unbox the result into an `int` only after that test.

<!-- stage: trace -->
### A Small Ring Fills And Wraps

Imagine a ring of six slots, numbered 0 to 5, that is allowed to hold at most five items, which keeps one slot free so that an empty ring and a full ring can be told apart. The ring starts empty with `head = 0` and `tail = 0`. Calling `addLast(4)` writes 4 in slot 0 and moves the tail to 1. Calling `addLast(7)` writes in slot 1. Calling `addFirst(2)` moves the head back from 0, which wraps around to slot 5, and writes 2 there, so the line from front to back is 2, 4, 7 and it occupies slots 5, 0 and 1. Calling `removeLast()` takes 7 from slot 1 and moves the tail back to 1. The step to study is `addFirst(2)`, because the head wraps around the end of the array and no item moves.

A second ring shows a bounded history of capacity three. The values 5, 6 and 7 are appended at the back. When 8 arrives the size would become four, so the oldest item, at the front, is removed first, and 5 leaves while 8 joins.

```trace
{"cells":["-","-","-","-","-","-"],"pointers":["head","tail"],"steps":[{"at":{"head":0,"tail":0},"vars":{"slots":"[-,-,-,-,-,-]","front_to_back":"[]","size":0},"note":"The ring is empty, so head and tail are the same slot, 0."},{"at":{"head":0,"tail":1},"vars":{"slots":"[4,-,-,-,-,-]","front_to_back":"[4]","size":1},"note":"addLast(4) writes 4 in slot 0 and moves the tail to slot 1."},{"at":{"head":0,"tail":2},"vars":{"slots":"[4,7,-,-,-,-]","front_to_back":"[4,7]","size":2},"note":"addLast(7) writes 7 in slot 1 and moves the tail to slot 2."},{"at":{"head":5,"tail":2},"vars":{"slots":"[4,7,-,-,-,2]","front_to_back":"[2,4,7]","size":3},"note":"addFirst(2) moves the head back from slot 0 to slot 5 and writes 2 there. The head wrapped from slot 0 to the last slot, and no item moved."},{"at":{"head":5,"tail":1},"vars":{"slots":"[4,-,-,-,-,2]","front_to_back":"[2,4]","size":2},"note":"removeLast() moves the tail back to slot 1 and takes 7 from it."}]}
```

```trace
{"cells":["-","-","-","-","-","-"],"pointers":["head","tail"],"steps":[{"at":{"head":0,"tail":0},"vars":{"slots":"[-,-,-,-,-,-]","front_to_back":"[]","size":0},"note":"The history is empty."},{"at":{"head":0,"tail":1},"vars":{"slots":"[5,-,-,-,-,-]","front_to_back":"[5]","size":1},"note":"Append 5 at slot 0. The history holds 1 items."},{"at":{"head":0,"tail":2},"vars":{"slots":"[5,6,-,-,-,-]","front_to_back":"[5,6]","size":2},"note":"Append 6 at slot 1. The history holds 2 items."},{"at":{"head":0,"tail":3},"vars":{"slots":"[5,6,7,-,-,-]","front_to_back":"[5,6,7]","size":3},"note":"Append 7 at slot 2. The history holds 3 items."},{"at":{"head":0,"tail":4},"vars":{"slots":"[5,6,7,8,-,-]","front_to_back":"[5,6,7,8]","size":4},"note":"Append 8 at slot 3. The history holds 4 items."},{"at":{"head":1,"tail":4},"vars":{"slots":"[-,6,7,8,-,-]","front_to_back":"[6,7,8]","size":3},"note":"The size 4 is above the capacity 3, so the oldest item 5 is removed from the front."}]}
```

<!-- stage: code -->
### Both Ends And Both Families

```java
static int[] demonstrateEnds() {
    java.util.ArrayDeque<Integer> d = new java.util.ArrayDeque<>();
    d.addLast(4);
    d.addFirst(7);
    d.addLast(9);                                  // front to back: 7, 4, 9
    int first = d.removeFirst();                   // 7
    int last = d.peekLast();                       // 9, the item stays
    Integer none = new java.util.ArrayDeque<Integer>().pollFirst();   // null: the safe family
    return new int[]{first, last, d.size(), none == null ? 1 : 0};
}

static java.util.ArrayDeque<Integer> bounded(int[] stream, int capacity) {
    java.util.ArrayDeque<Integer> history = new java.util.ArrayDeque<>();
    for (int x : stream) {
        history.addLast(x);
        if (history.size() > capacity) history.removeFirst();   // evict the oldest
    }
    return history;
}
```

Every call is O(1) amortized, so `bounded` runs in O(n) for `n` values with O(capacity) memory. The methods `removeFirst` and `peekLast` are called on a deque that is known to be non-empty, and the safe family appears where emptiness is possible. The `null` that `pollFirst` returns is held in an `Integer`, since assigning it to an `int` would throw a `NullPointerException` while unboxing.

<!-- stage: applicability -->
### When Both Ends Are Needed

Use a deque when the algorithm only ever touches the two ends, adding or removing at each in constant time, and has no use for items in the middle. The invariant is that the front and back keep the roles they were given at the start, so every method call can be read as a statement about one end. Write the roles in a comment above the loop when the deque is used for anything beyond a plain queue.

The false friend is `LinkedList`, which also offers every deque method. It allocates a node for each item, so it uses more memory and is usually slower in practice, and it allows `null` items, which makes an empty result ambiguous. `ArrayDeque` is the ordinary choice unless a program needs `null` items or an index, and then a deque is probably the wrong structure anyway. A second false friend is the legacy `Stack` class, and a third is `ArrayList` with `remove(0)`, whose front jobs are linear.

Do not use a deque when the algorithm must look at items in the middle, search for a value, or remove an item that is not at an end, since a deque offers no such method that is fast. A heap or a tree set is the right structure for removing the smallest item, and a deque is not. Also remember the contract of the null ban: storing a missing value by `null` fails at once with a `NullPointerException`, so a marker value such as -1 must be chosen instead when a missing item has to be stored.

<!-- stage: exercises -->
### Exercises

#### [Build] Two-Ended Buffer (Author exercise)
<!-- id: dq-two-ended-buffer -->

**Prerequisites.** Stacks and queues from Chapter 11, and `ArrayDeque` method names.

**Problem.** A deque of integers starts empty. Process an array of commands in order. A command is one of `addFirst x`, `addLast x`, `removeFirst`, `removeLast`, `peekFirst`, `peekLast`. For every `removeFirst`, `removeLast`, `peekFirst` and `peekLast`, append the integer it produces to the result. Commands that remove or peek are only issued when the deque is not empty.

**Constraints.** 1 <= commands.length <= 10^5 and 0 <= x <= 10^9. Each command must cost O(1) amortized.

**Example 1.** Input `commands = ["addLast 4", "addFirst 7", "addLast 9", "removeFirst", "peekLast", "removeLast"]`, output `[7, 9, 9]`.

**Example 2.** Input `commands = ["addFirst 1", "addFirst 2", "peekFirst", "peekLast"]`, output `[2, 1]`, since the second `addFirst` goes in front of the first.

**Hint.** Which of the six commands change the deque and which only read it? What does `addFirst` do to the order that `addLast` does not?

**Changed decision.** First rung: each command maps to exactly one `First` or `Last` method, so the end is named in every call.

#### [Vary] Bounded Recent History (Author exercise)
<!-- id: dq-bounded-recent-history -->

**Prerequisites.** The Two-Ended Buffer exercise above.

**Problem.** A history keeps at most `capacity` items. Each value of `stream` is appended at the back, and if the history then holds more than `capacity` items, the oldest item, which is at the front, is evicted. Return the evicted values in the order they were evicted.

**Constraints.** 1 <= capacity <= 10^5, 0 <= stream.length <= 10^5 and 0 <= stream[i] <= 10^9.

**Example 1.** Input `stream = [5, 6, 7, 8, 9]`, `capacity = 3`, output `[5, 6]`.

**Example 2.** Input `stream = [1, 2]`, `capacity = 5`, output `[]`, since the history never overflows.

**Hint.** Should the eviction happen before or after the append? What would the history hold at the moment of the check if you evicted first?

**Changed decision.** A size check follows every append, so the front is removed only when the back has just pushed the history over its limit.

#### [Boundary] Empty Deque Contract (Author exercise)
<!-- id: dq-empty-deque-contract -->

**Prerequisites.** The two exercises above.

**Problem.** A deque of non-negative integers starts empty and processes a script of the commands `addLast x`, `pollFirst`, `pollLast`, `peekFirst` and `peekLast`. Unlike the earlier exercise, the poll and peek commands may be issued when the deque is empty. For every poll or peek, append the produced integer to the result, or -1 if the deque was empty. The program must not throw.

**Constraints.** 1 <= script.length <= 10^5 and 0 <= x <= 10^9, so -1 never appears as a real item.

**Example 1.** Input `script = ["pollFirst", "addLast 3", "pollFirst", "pollFirst"]`, output `[-1, 3, -1]`.

**Example 2.** Input `script = ["peekLast", "peekFirst"]`, output `[-1, -1]`.

**Hint.** What does `pollFirst` return on an empty deque, and why can that value never be a real item? Which type should hold the result before it is converted?

**Changed decision.** The safe methods are chosen on purpose, because emptiness is a normal state here and not a bug, and the result is tested before unboxing.

#### [Recognize] Candidate Deque API (Author exercise)
<!-- id: dq-candidate-deque-api -->

**Prerequisites.** All three exercises above.

**Problem.** A window algorithm keeps candidates in a deque whose front is the oldest candidate and whose back is the newest. Its steps are written as letters: `S` looks at the oldest candidate, `E` removes the oldest candidate, `N` looks at the newest candidate, `D` removes the newest candidate and `A` adds a new candidate as the newest. Given a string of such letters, return the `ArrayDeque` method names that perform the steps in order.

**Constraints.** 1 <= steps.length() <= 10^4 and every character is one of `S`, `E`, `N`, `D`, `A`. Use `peekFirst`, `removeFirst`, `peekLast`, `removeLast` and `addLast`.

**Example 1.** Input `steps = "SEA"`, output `["peekFirst", "removeFirst", "addLast"]`.

**Example 2.** Input `steps = "NDNA"`, output `["peekLast", "removeLast", "peekLast", "addLast"]`.

**Hint.** Which end is the oldest candidate? Which of the five steps read without changing the deque, and which change it?

**Changed decision.** No algorithm is written yet. The task is to see that expiry works on the front, domination works on the back, and appending is only ever at the back.
