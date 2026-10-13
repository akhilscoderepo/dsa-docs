<!-- lesson-kind: standard -->
<!-- lesson-id: iterators -->
## Keep Traversal State Between Calls

<!-- stage: context -->
### Why A Parser Loses Tokens

A SQL parser reads tokens from a tokenizer one call at a time. To decide whether a comma ends the column list, the parser must look at the next token without taking it. The first version of the tokenizer wrapper answered that look by calling the tokenizer's `next()`. After the release, the parser skipped every token it had looked at, and queries with a trailing comma produced wrong syntax errors.

Every bug of this kind has the same cause. A class stands between a caller and a sequence, and it must remember a position across separate public calls. Looking at an element and taking an element are two different promises, and one stored position cannot keep both. This lesson shows what a class must store so that a look leaves the sequence unchanged and a take moves it forward by exactly one step.

<!-- stage: naive -->
### Peeking By Calling next Twice

The tempting wrapper forwards both operations to the source iterator, because that is the only way the source reports an element.

```java
import java.util.Iterator;

final class NaivePeek {
    private final Iterator<Integer> source;

    NaivePeek(Iterator<Integer> source) { this.source = source; }

    // Look at the next element.
    int peek() { return source.next(); }

    // Take the next element.
    int next() { return source.next(); }

    boolean hasNext() { return source.hasNext(); }
}
```

Wrap the sequence `[4, 7, 9]` and call `peek()` and then `next()`. The first call returns 4 and moves the source forward. The second call returns 7. The 4 never reaches the caller as a taken element, and a caller who loops with `hasNext()` ends up one element early.

```predict
A caller wraps the sequence [4, 7, 9] in NaivePeek and calls peek() once, then next() once. What does next() return, and which element can the caller never take afterward?

next() returns 7, because the earlier peek() already moved the source past 4. The element 4 is lost: no later call can return it, since the source never moves backward.
```

<!-- stage: bottleneck -->
### Why Observation Must Not Consume

The naive wrapper runs in O(1) time per call and uses O(1) space, so speed is not the problem. The cost is a wrong sequence. Each `peek()` removes one element from what the caller will later see, so a program that peeks `p` times loses `p` elements from a sequence of `n`, and the loop reads only `n - p` values.

Repeating the peek makes it worse. Two `peek()` calls in a row return two different elements, although nothing was taken between them. A parser that asks the same question twice gets two different answers, and the answer to a question about the next token must not depend on how often the parser asks.

The source iterator offers no way to move backward, and a source such as a network stream or a file reader cannot be restarted at all. The wrapper therefore cannot undo a `source.next()` after it has made one. The only remaining option is to store the pulled element inside the wrapper, which costs O(1) extra space and keeps every call at O(1) time.

<!-- stage: insight -->
### Storing One Pulled Element

#### Adding A Lookahead Slot

Give the wrapper one **lookahead slot** and one flag `filled` that says whether the slot holds an element. The slot holds the single element that the source already gave away but the caller has not yet taken. Two operations then separate cleanly. `peek()` fills the slot when it is empty and returns the slot without clearing it. `next()` fills the slot the same way, returns it, and clears the flag.

The invariant is stated in two cases. When `filled` is false, the source holds every untaken element. When `filled` is true, the slot holds the next element and the source holds all the elements after it. Each operation restores one of those two cases before it returns.

#### Making Repeated Calls Idempotent

An operation is **idempotent** when calling it twice leaves the same state as calling it once. `peek()` becomes idempotent because it pulls from the source only when the flag is false. `hasNext()` becomes idempotent in a stronger way, because it never pulls at all. It answers `filled || source.hasNext()`, and `source.hasNext()` reports availability without consuming.

#### Handling An Exhausted Source

A source is **exhausted** when `hasNext()` returns false and no element remains. A `peek()` or `next()` on an exhausted wrapper must throw `NoSuchElementException`. The check comes before any assignment, so the failed call leaves the slot and the flag as they were. The flag is a separate boolean because the slot value alone cannot say whether it is empty. A sequence of boxed `Integer` values may legitimately contain `null`, and a design that treats `null` as empty would pull a second element.

<!-- names: lookahead slot, idempotent, exhausted -->

<!-- stage: variables -->
### Variables The Wrapper Keeps

Four entities hold the traversal state between calls. The two public reads and the one public take all work on these four.

- **source** is the underlying iterator, which only moves forward and which the wrapper pulls from at most once per element.
- **slot** is the single pulled element that the caller has not taken yet.
- **filled** is the boolean that says whether `slot` holds a real element.
- **advances** counts how many times the wrapper called `source.next()`, which equals the taken count plus one when `filled` is true.

<!-- stage: trace -->
### Tracing Calls On Three Elements

#### Peeking Without Moving

The first trace wraps `[4, 7, 9]`. The pointer `pos` marks how far the source has advanced, which is the index of the next element it would give away.

At the start nothing has been pulled, so `pos` is 0 and the slot is empty. The first `peek()` pulls the 4, moves `pos` to 1 and fills the slot. The second `peek()` finds the slot full, so it returns 4 again and `pos` stays 1. The call `next()` then returns the stored 4 and empties the slot, still without touching the source.

#### Taking And Reaching The End

The next `hasNext()` asks the source and answers true without pulling. The following `next()` pulls the 7, fills the slot and empties it again in one call, so `pos` becomes 2. A `peek()` pulls the 9 and `next()` returns it, and the last `hasNext()` answers false because the slot is empty and the source has nothing left.

```trace
{"cells":[4,7,9],"pointers":["pos"],"steps":[{"at":{"pos":0},"vars":{"slot":"empty","call":"start"},"note":"Start: nothing is pulled, the slot is empty and pos is 0."},{"at":{"pos":1},"vars":{"slot":"4","call":"peek() = 4"},"note":"peek() returns 4; pos is 1 and the slot holds 4."},{"at":{"pos":1},"vars":{"slot":"4","call":"peek() = 4"},"note":"peek() returns 4; pos is 1 and the slot holds 4."},{"at":{"pos":1},"vars":{"slot":"empty","call":"next() = 4"},"note":"next() returns 4; the slot is now empty and pos is 1."},{"at":{"pos":1},"vars":{"slot":"empty","call":"hasNext() = true"},"note":"hasNext() answers true without pulling; pos stays 1."},{"at":{"pos":2},"vars":{"slot":"empty","call":"next() = 7"},"note":"next() returns 7; the slot is now empty and pos is 2."},{"at":{"pos":3},"vars":{"slot":"9","call":"peek() = 9"},"note":"peek() returns 9; pos is 3 and the slot holds 9."},{"at":{"pos":3},"vars":{"slot":"empty","call":"next() = 9"},"note":"next() returns 9; the slot is now empty and pos is 3."},{"at":{"pos":3},"vars":{"slot":"empty","call":"hasNext() = false"},"note":"hasNext() answers false without pulling; pos stays 3."}]}
```

#### Walking A Stack Of Iterators

The second trace follows the nested case, where the sequence is `[[1, [2]], [], 3]`. The pointer `out` counts the integers already taken, and `frames` is the number of unfinished iterators on the stack. Each `next()` first scans forward through the nested lists until it finds an integer. It pushes an iterator when it enters a list and pops one when that list has no element left. The empty list `[]` is entered and popped without producing anything.

```trace
{"cells":[1,2,3],"pointers":["out"],"steps":[{"at":{"out":0},"vars":{"frames":1,"value":"none"},"note":"Start: only the top-level list is on the stack, so frames is 1."},{"at":{"out":1},"vars":{"frames":2,"value":1},"note":"next() enters a list, finds 1 and returns 1; frames is 2."},{"at":{"out":2},"vars":{"frames":3,"value":2},"note":"next() enters a list, finds 2 and returns 2; frames is 3."},{"at":{"out":3},"vars":{"frames":1,"value":3},"note":"next() pops a finished list, pops a finished list, enters an empty list, pops a finished list, finds 3 and returns 3; frames is 1."},{"at":{"out":3},"vars":{"frames":0,"value":"none"},"note":"hasNext() pops a finished list and answers false; frames is 0."}]}
```

<!-- stage: code -->
### Implementing The Lookahead Wrapper

```java
// Contract: hasNext() never consumes; peek() pulls at most once per element; next() advances exactly once.
// remove() is deliberately not overridden, so the interface default throws UnsupportedOperationException.
final class PeekIterator implements Iterator<Integer> {
    private final Iterator<Integer> source;
    private int lookahead;
    private boolean filled;

    PeekIterator(Iterator<Integer> source) { this.source = source; }

    // Reports availability only; the source is asked but never advanced.
    @Override public boolean hasNext() { return filled || source.hasNext(); }

    // Pulls from the source only when the slot is empty, so repeated peeks cost one advance.
    int peek() {
        if (!filled) {
            lookahead = source.next();   // throws NoSuchElementException before any field changes
            filled = true;
        }
        return lookahead;
    }

    // Returns the same element peek() showed, then empties the slot.
    @Override public Integer next() {
        int value = peek();
        filled = false;
        return value;
    }
}
```

Every operation runs in O(1) time and the wrapper adds O(1) space. A caller who only calls `next()` pays for the slot with one boolean test. The class inherits `remove()` from the interface and does not override it, so the hazards listed in the last stage stay visible.

<!-- stage: applicability -->
### Checking The Next Element Invariant

#### Recognizing An Incremental Sequence

Use this design when a class must expose one logical sequence a piece at a time, and a caller may ask a question about the next element before taking it. Tree iterators, nested list flatteners, merging several streams and token readers all have this shape.

The **invariant** is a fact that every public operation must restore before it returns. Here it says that the slot and the source together hold exactly the untaken elements, in order, with at most one element in the slot. If you can state that sentence for a new class, you can check each operation against it.

#### Spotting The False Friend

A **false friend** is a design that looks like the right tool and fails on a boundary case. The nearest false friend is copying the whole sequence into a list and walking an index. It is correct for an array, but it costs O(n) space and time at construction, and it breaks for a source that is large, lazy or one-shot. It also reads a list snapshot, so later changes to the source are invisible.

#### Avoiding Three Java Hazards

The interface method `Iterator.remove()` has a default body that throws `UnsupportedOperationException`. A wrapper with a filled slot must not forward `remove()` to the source, because the source would remove the cached element and not the last one returned. A `java.util.ArrayList` iterator counts structural changes in `modCount`, and the check happens in `next()`, not in `hasNext()`. A cached element therefore hides a list change until the next pull, and the `ConcurrentModificationException` appears one call late. Last, an `Iterator<Integer>` may yield `null`. Unboxing it into an `int` throws `NullPointerException`, and a `null` sentinel for an empty slot cannot tell a missing element from a null one, so use a separate boolean.

<!-- stage: exercises -->
### Exercises

#### [Build] Array Peeking Iterator (Author exercise)
<!-- id: ds-array-peeking-iterator -->

**Prerequisites.** The lookahead wrapper in this lesson.

**Problem.** Implement a class `ArrayPeekingIterator` over an `int[] data`. The constructor stores the array without copying it. Operation `hasNext()` returns true when an element has not been taken. Operation `peek()` returns the next element without taking it. Operation `next()` returns the next element and takes it. The class keeps a cursor `pos` that counts how many elements it has read from `data`, and it stores at most one read element that the caller has not taken. Operation `advances()` returns `pos`. Both `peek()` and `next()` throw `NoSuchElementException` when every element has been taken.

**Constraints.** The limits are:
- **Length** is `0 <= data.length <= 10^5`.
- **Values** are `int`, and ties are allowed.
- **Mutation** of `data` is not allowed, and the caller does not change it during use.
- **Cost** of every operation is O(1).
- **Failure** is `NoSuchElementException` and leaves all state unchanged.

**Example 1.** Input `data = [4,7,9]` and the calls `peek()`, `peek()`, `next()`, `next()`, output `4, 4, 4, 7` and `advances() = 2`.

**Example 2.** Input `data = [5]` and the calls `peek()`, `next()`, `hasNext()`, output `5, 5, false`, and a further `peek()` throws with `advances() = 1`.

**Hint.** Which call reads from `data`, and what must the other calls do when the cached element exists?

**Changed decision.** First exercise in the sequence: it separates reading from the array from handing the element to the caller.

#### [Vary] Peeking Iterator (LeetCode 284)
<!-- id: ds-peeking-iterator-contract -->

**Prerequisites.** The array peeking exercise above.

**Problem.** Implement `PeekingCountdown` over an `Iterator<Integer> source` and an integer `size` equal to the number of elements the source will give. Operations `hasNext()`, `peek()` and `next()` behave as in the previous exercise. The changed contract has two parts. Operation `peek()` on an exhausted wrapper throws `NoSuchElementException`, and the throw leaves every field and `remaining()` as they were. Operation `remaining()` returns `size` minus the number of elements `next()` has returned, and a `peek()` never changes it.

**Constraints.** The limits are:
- **Size** is `0 <= size <= 10^5`, and it equals the true length of the source.
- **Values** are `int` and fit in a boxed `Integer` with no `null`.
- **Source** moves forward only and cannot be restarted.
- **Cost** of every operation is O(1).
- **Failure** is `NoSuchElementException` on `peek()` or `next()` when nothing remains.

**Example 1.** Input a source `[3,8,1]` and `size = 3`, with the calls `peek()`, `remaining()`, `next()`, `remaining()`, `next()`, `next()`, `remaining()`, output `3, 3, 3, 2, 8, 1, 0`.

**Example 2.** Input an empty source and `size = 0`, output that `hasNext()` is false, `remaining()` is 0, and two `peek()` calls in a row both throw while `remaining()` stays 0.

**Hint.** Where in `peek()` must the check for an empty source sit so that nothing has changed when the exception leaves?

**Changed decision.** The contract now adds a counted view of the sequence and a failure that must leave state untouched.

#### [Boundary] Repeated hasNext And Peek (Author exercise)
<!-- id: ds-repeated-has-next-peek -->

**Prerequisites.** The two exercises above.

**Problem.** Implement a generic class `Lookahead<T>` that implements `Iterator<T>` over a source iterator. Operations `hasNext()` and `peek()` must be idempotent, so calling either one any number of times in a row changes nothing after the first call. Count the underlying advances, which are the calls the wrapper makes to `source.next()`. Show that after any call sequence the count equals the number of taken elements plus one when an element is cached, and no more.

**Constraints.** The limits are:
- **Elements** are of type `T`, and `null` is allowed as an element.
- **Sequence** length is at most `10^5`, and it may be empty.
- **Count** is observed through a source wrapper that increments a counter on every successful `next()`.
- **hasNext()** is not allowed to call `source.next()`.
- **Remove** is not supported and throws `UnsupportedOperationException`.

**Example 1.** Input a source `[6,2,9]` and the calls `hasNext()` three times, `peek()` three times, output `true` three times, then `6` three times, with 1 advance. Then `next()`, `hasNext()`, `peek()` output `6, true, 2` and 2 advances.

**Example 2.** Input a source `[5]` and the calls `peek()`, `next()`, `hasNext()`, `peek()`, output `5, 5, false` and then a `NoSuchElementException`, with exactly 1 advance.

**Hint.** If `hasNext()` asked the source to produce an element, how many elements would ten calls consume?

**Changed decision.** The edge case is repetition: the same read-only call repeated must not change the number of advances.

#### [Recognize] Flatten Nested List Iterator (LeetCode 341)
<!-- id: ds-nested-item-flatten -->

**Prerequisites.** All three exercises above.

**Problem.** A nested item implements the interface `NestedItem` with the operations `boolean isInt()`, `int value()` and `List<NestedItem> children()`. The operation `value()` is defined only when `isInt()` is true, and `children()` only when it is false. Implement `NestedFlattener` over a top-level `List<NestedItem>`. Operation `hasNext()` returns true when an integer has not been returned, `next()` returns the integers in left-to-right order, and `liveFrames()` returns the number of iterators currently on the stack. Skip empty lists. Return only integers.

**Constraints.** The limits are:
- **Total** number of items across all lists is at most `10^5`.
- **Depth** of list nesting is at most 1000.
- **Values** are `int`.
- **Empty** lists are allowed at any depth, including the top level.
- **Frames** counted by `liveFrames()` include the top-level list, and a frame is removed only when `hasNext()` finds it empty.
- **Failure** is `NoSuchElementException` from `next()` when no integer remains.

**Example 1.** Input `[[1,[2]],[],3]`, output `1, 2, 3`, and `liveFrames()` reads `2, 3, 1` right after each `next()`.

**Example 2.** Input `[[[]],[[]]]`, output that `hasNext()` is false, and `liveFrames()` reads 1 before the first call and 0 after it.

**Hint.** A list that you enter is a new iterator on top of the stack. When is it safe to remove it?

**Changed decision.** The sequence is now nested, so one saved cursor becomes a stack of unfinished cursors, and the lookahead slot holds the next integer found by a scan.
