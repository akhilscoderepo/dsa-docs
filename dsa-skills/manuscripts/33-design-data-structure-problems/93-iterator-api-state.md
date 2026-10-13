<!-- lesson-kind: combination -->
<!-- lesson-id: iterator-api-state -->
## Traversal State Across Public Calls

<!-- stage: context -->
### A Parser That Loses One Token

A JSON parser reads tokens from a lexer through a small interface with `hasNext()` and `next()`. The parser must look at the upcoming token before it decides which rule to apply. A developer writes `hasNext()` so that it reads one token from the lexer and returns true when the read succeeds. The parser calls `hasNext()` once in a loop condition and `next()` once in the body. Every second token disappears, and the parser reports an error on valid input.

The lexer, the parser and the loop are each correct on their own. The failure sits between them, in the promise that a question about the upcoming element must not remove that element. Earlier chapters walked a tree or a nested structure inside one function, where the walk ran from start to finish without interruption. Here the caller controls the pace and the order of calls. This lesson asks what state a class must keep so that every public operation leaves the traversal ready for the next one.

<!-- stage: contributions -->
### What Traversal And Class Each Add

The traversal supplies the order and the position. A stack of unvisited tree nodes, or a stack of nested-list cursors, already knows which element comes next and how to find the one after it. Used inside one function, that knowledge lives in local variables and disappears when the function returns.

The class supplies the contract. It moves the position into fields, so the position survives between calls. It also fixes which operations may change the position, how often a caller may repeat an operation, and what a call on an exhausted structure must do. A caller may ask `hasNext()` five times in a row or call `peek()` before every `next()`. The traversal alone gives no answer to those calls, because it assumes one pass. The combination answers a single question: which fields must the class keep so that any legal sequence of calls returns the right elements in the right order.

<!-- stage: naive -->
### Copying The Whole Traversal Into A List

The direct design runs the whole traversal once, stores every value in a list and then serves calls from the list. The class below does that for a binary search tree. The constructor performs an in-order walk, and `next()` returns the values one at a time.

```java
import java.util.ArrayList;
import java.util.List;

final class EagerTreeIterator {
    record TreeNode(int val, TreeNode left, TreeNode right) {}

    private final List<Integer> values = new ArrayList<>();
    private int position = 0;

    EagerTreeIterator(TreeNode root) {
        collect(root);
    }

    private void collect(TreeNode node) {
        if (node == null) return;
        collect(node.left());
        values.add(node.val());
        collect(node.right());
    }

    boolean hasNext() {
        return position < values.size();
    }

    int next() {
        return values.get(position++);
    }
}
```

For a tree holding 2, 5 and 9, the constructor stores `[2, 5, 9]`, and three calls to `next()` return those values in order. Repeated calls to `hasNext()` change nothing, so the class behaves correctly on small trees.

<!-- stage: bottleneck -->
### The Constructor Pays For Every Node

```predict
A tree holds 1,000,000 nodes, and a caller reads only the first value and then stops. How much time and memory does the constructor spend, and how much did the caller need?

The constructor spends O(n) time and O(n) memory, about a million list entries, before the first call returns. The caller needed one value, which a walk down the leftmost path of O(h) nodes can find, where h is the height.
```

The constructor takes O(n) time and the list takes O(n) space before the caller asks for anything. A caller that stops after one value still pays for all of it. A query engine that scans an index range and stops at the first matching row shows the cost clearly. The recursive walk also uses O(h) call frames, so a tree that leans to one side with a million nodes overflows the Java call stack inside the constructor.

The list is also a snapshot. If another part of the program inserts a node after construction, the iterator keeps returning the old values. The goal is a class that holds O(h) state, starts in O(h) time and produces each value on demand. That goal needs a state smaller than the full answer, and it adds a new requirement: the state must stay consistent after every call, in any order.

<!-- stage: insight -->
### Keep Only What The Next Call Needs

#### Hold The Unvisited Ancestors

The **spine stack** is a stack of tree nodes whose values are not yet returned. After construction and after every call, it holds the path from the root to the next node to return, restricted to nodes that are not yet returned. Its top is the next element. The constructor pushes the root and then every left child below it. A call to `next()` pops the top, pushes the left spine of that node's right child, and returns the popped value. Each node is pushed once and popped once, so `next()` costs O(1) amortized and O(h) in the worst case, and the stack uses O(h) space.

#### Store One Element Of Lookahead

A source that cannot restart, such as a network stream or a file reader, cannot give back an element once it has returned it. To let a caller look without consuming, the wrapper keeps a **cached head**. This is one slot that holds an element already pulled from the source but not yet returned to the caller. A call to `peek()` fills the slot if it is empty and returns it. A call to `next()` returns the slot and empties it, or pulls directly when the slot is empty. The slot is the only place where an element is both pulled and unreturned.

#### State The Rule Every Operation Restores

The **next-element invariant** says that between any two calls, the fields alone determine the next element to return, and they record exactly the elements not yet returned. A call to `next()` removes one element from that record. A call to `hasNext()` or `peek()` removes none. These two operations may move internal position, for example by skipping empty nested lists or by filling the cached head, but they return the same answer when repeated, and they never lose an element. The invariant is the condition that every public operation must restore before it returns.

<!-- names: spine stack, cached head, next-element invariant -->

<!-- stage: variables -->
### Fields That Hold The Position

Each iterator in this lesson keeps a small set of fields, and every operation reads or writes only these.

- **stack** holds the tree nodes or nested-list cursors that still have elements to give.
- **head** is the one element already pulled from the source and not yet returned, valid only when `hasHead` is true.
- **hasHead** tells whether `head` holds an element, so a legitimate value of zero is never confused with an empty slot.
- **source** is the structure that supplies elements and cannot be restarted.

The size of `stack` equals the number of unfinished ancestors, so it never exceeds the height of the tree or the nesting depth of the list.

<!-- stage: trace -->
### Tracing The Stack And The Slot

#### A Search Tree Read In Order

Take the tree with root 6, left child 2, right child 9, and the values 1 and 4 below 2, with 3 below 4 on the left, and 8 below 9 on the left. The in-order values are 1, 2, 3, 4, 6, 8, 9. The constructor pushes 6, 2 and 1, so the stack holds three nodes and its top is 1. A call to `next()` pops 1 and finds no right child, so the stack shrinks to 6 and 2.

The next call pops 2 and pushes the left spine of its right child 4, which is 4 and 3. The stack grows to 6, 4 and 3, and its top is 3. The remaining calls pop 3, 4 and 6, and the pop of 6 pushes 9 and 8. The stack reaches depth zero after 9 is returned.

```trace
{"cells":[1,2,3,4,6,8,9],"pointers":["next"],"steps":[{"at":{"next":0},"vars":{"stack":"[6, 2, 1]","depth":3},"note":"The constructor pushes the left spine. The stack holds [6, 2, 1] and the top, 1, is the next value."},{"at":{"next":1},"vars":{"returned":1,"stack":"[6, 2]","depth":2},"note":"next() pops 1 and pushes the left spine of its right child. Returned so far: [1]."},{"at":{"next":2},"vars":{"returned":2,"stack":"[6, 4, 3]","depth":3},"note":"next() pops 2 and pushes the left spine of its right child. Returned so far: [1, 2]."},{"at":{"next":3},"vars":{"returned":3,"stack":"[6, 4]","depth":2},"note":"next() pops 3 and pushes the left spine of its right child. Returned so far: [1, 2, 3]."},{"at":{"next":4},"vars":{"returned":4,"stack":"[6]","depth":1},"note":"next() pops 4 and pushes the left spine of its right child. Returned so far: [1, 2, 3, 4]."},{"at":{"next":5},"vars":{"returned":6,"stack":"[9, 8]","depth":2},"note":"next() pops 6 and pushes the left spine of its right child. Returned so far: [1, 2, 3, 4, 6]."},{"at":{"next":6},"vars":{"returned":8,"stack":"[9]","depth":1},"note":"next() pops 8 and pushes the left spine of its right child. Returned so far: [1, 2, 3, 4, 6, 8]."},{"at":{"next":-1},"vars":{"returned":9,"stack":"[]","depth":0},"note":"next() pops 9 and pushes the left spine of its right child. Returned so far: [1, 2, 3, 4, 6, 8, 9]."}]}
```

#### A Peek That Pulls Once

Wrap a source that holds 4, 7 and 9. The first `peek()` finds the slot empty and pulls 4, so the source has now been called once. The second `peek()` finds the slot full and returns 4 without calling the source. A call to `next()` returns 4 and empties the slot. A call to `hasNext()` asks the source whether more elements exist and does not pull. The next `next()` pulls 7 directly, because the slot is empty. A later `peek()` pulls 9 once.

```trace
{"cells":[4,7,9],"pointers":["pulled"],"steps":[{"at":{"pulled":-1},"vars":{"head":"empty","calls":0},"note":"Start: the slot is empty and the source has not been called."},{"at":{"pulled":0},"vars":{"op":"peek()","result":4,"head":4,"calls":1},"note":"peek() finds the slot empty and pulls 4. The source call count is 1."},{"at":{"pulled":0},"vars":{"op":"peek()","result":4,"head":4,"calls":1},"note":"peek() finds the slot full and returns 4 with no source call. The count stays 1."},{"at":{"pulled":0},"vars":{"op":"next()","result":4,"head":"empty","calls":1},"note":"next() returns the cached 4 and empties the slot. The count stays 1."},{"at":{"pulled":0},"vars":{"op":"hasNext()","result":"true","head":"empty","calls":1},"note":"hasNext() answers true from the slot and the source, with no pull. The count stays 1."},{"at":{"pulled":1},"vars":{"op":"next()","result":7,"head":"empty","calls":2},"note":"next() finds the slot empty and pulls 7 directly. The count is 2."},{"at":{"pulled":2},"vars":{"op":"peek()","result":9,"head":9,"calls":3},"note":"peek() finds the slot empty and pulls 9. The source call count is 3."},{"at":{"pulled":2},"vars":{"op":"next()","result":9,"head":"empty","calls":3},"note":"next() returns the cached 9 and empties the slot. The count stays 3."},{"at":{"pulled":2},"vars":{"op":"hasNext()","result":"false","head":"empty","calls":3},"note":"hasNext() answers false from the slot and the source, with no pull. The count stays 3."}]}
```

<!-- stage: code -->
### Two Iterators That Keep The Invariant

#### A Tree Iterator On Node Objects

```java
final class IteratorState {
    record TreeNode(int val, TreeNode left, TreeNode right) {}

    static final class SpineIterator {
        private final java.util.ArrayDeque<TreeNode> stack = new java.util.ArrayDeque<>();

        SpineIterator(TreeNode root) { pushLeft(root); }

        private void pushLeft(TreeNode node) {
            for (; node != null; node = node.left()) stack.push(node); // each node enters the stack once
        }

        boolean hasNext() { return !stack.isEmpty(); } // reads state only, removes nothing

        int next() {
            if (stack.isEmpty()) throw new java.util.NoSuchElementException();
            TreeNode top = stack.pop();                // the top is the next element
            pushLeft(top.right());                     // restore the invariant for the following call
            return top.val();
        }
    }
}
```

#### A Wrapper That Can Look Ahead

```java
final class PeekState {
    static final class Peeker {
        private final java.util.Iterator<Integer> source;
        private int head;
        private boolean hasHead;

        Peeker(java.util.Iterator<Integer> source) { this.source = source; }

        int peek() {
            if (!hasHead) { head = source.next(); hasHead = true; } // at most one pull per cached element
            return head;
        }

        boolean hasNext() { return hasHead || source.hasNext(); }   // never pulls

        int next() {
            if (hasHead) { hasHead = false; return head; }          // hand over the cached element
            return source.next();
        }
    }
}
```

Both classes check the invariant at the end of each operation. `SpineIterator` costs O(h) space and O(1) amortized time for `next()`. `Peeker` uses O(1) extra space and makes one source call for each element, no matter how often the caller peeks.

<!-- stage: applicability -->
### When A Class Must Resume Traversal

#### Recognize The Call-By-Call Pattern

Use this design when a class exposes `hasNext()`, `next()` or a similar pair, the data is large or cannot restart, and callers repeat or interleave operations. An invariant is a fact about the fields that every public operation must restore before it returns. Here the fact is the next-element invariant. Write it down first, then check each operation against it, including the operation on an exhausted structure, which must throw `NoSuchElementException` and leave the fields unchanged.

#### Beware The Plausible Shortcuts

A false friend is a technique that fits the problem on the first example and breaks a condition of the contract. Eager flattening is one. It returns correct values on a static tree, and it costs O(n) before the first call and goes stale when the tree changes. A `hasNext()` that pulls an element and forgets it is another. It passes a test that calls `hasNext()` and `next()` in strict alternation, and it loses data when the caller calls `hasNext()` twice.

#### Java Details That Cause Failures

Use `ArrayDeque` for the stack, because `Stack` is a legacy synchronized class. Keep a `hasHead` flag, because an `Integer head` set to `null` hides a real value and a plain `int` has no empty state. Document what happens when the underlying structure changes after construction, since a stack of nodes reflects the tree at the time of the last `next()` and not later inserts.

<!-- stage: exercises -->
### Exercises

#### [Build] Tree Iterator Over A Node Pool (LeetCode 173)
<!-- id: ds-pool-tree-iterator -->

**Prerequisites.** The spine stack in this lesson and the lesson Keep Traversal State Between Calls.

**Problem.** This variation of Binary Search Tree Iterator stores the tree in three parallel arrays, the node pool. Node `i` has the value `val[i]`, the left child `left[i]` and the right child `right[i]`, and the index -1 means no child. Implement a class `PoolTreeIterator(int[] left, int[] right, int[] val, int root)` with the operations `hasNext()`, `next()` and `peekDepth()`. The tree is a binary search tree, and `next()` returns the values in increasing order. Keep the unvisited left spine in an int stack. The operation `peekDepth()` returns the current size of that stack. The operation `next()` on an exhausted iterator throws `NoSuchElementException`.

**Constraints.** The limits are:
- **Nodes** number `0 <= n <= 10^5`, and `n` equals the length of each array.
- **Values** are distinct `int` numbers.
- **Root** is a valid index, or -1 for an empty tree.
- **Nodes** outside the tree rooted at `root` may exist in the pool and are never visited.
- **Cost** of `next()` is O(1) amortized, and extra space is O(h).

**Example 1.** Input: a pool with `val = [8,3,10,1,6,14,4]`, `left = [1,3,-1,-1,6,-1,-1]`, `right = [2,4,5,-1,-1,-1,-1]` and `root = 0`. Output: the depths from `peekDepth()` are 3 after construction, then 2, 3, 2, 1, 1, 1, 0 after each of seven calls to `next()`, and the values returned are 1, 3, 4, 6, 8, 10, 14.

**Example 2.** Input: `val = [5,6,7]`, `left = [-1,-1,-1]`, `right = [1,2,-1]` and `root = 0`, a chain that leans right. Output: the depths are 1 after construction and 1, 1, 0 after the three calls, and the values are 5, 6, 7.

**Hint.** After a call to `next()`, which nodes must enter the stack, and where does the walk stop?

**Changed decision.** The tree lives in index arrays and not in node objects, and a new operation exposes the stack size, so the stack must hold indexes and its size must stay exact.

#### [Vary] Peeking Over A Source That Cannot Restart (LeetCode 284)
<!-- id: ds-counting-peeker -->

**Prerequisites.** The cached head in this lesson and the tree exercise above.

**Problem.** This variation of Peeking Iterator wraps an `IntSource` with the operations `hasNext()` and `next()`. The source cannot restart, and a public counter `calls` records how many times `next()` ran on it. Implement `CountingPeeker(IntSource source)` with the operations `peek()`, `hasNext()` and `next()`. Each operation must cause at most one call to `source.next()` each time an element becomes cached. A repeated `peek()` and any `hasNext()` cause none. When the source holds no more elements, `peek()` and `next()` throw `NoSuchElementException`.

**Constraints.** The limits are:
- **Source length** is `0 <= m <= 10^5` values of type `int`.
- **Counter** `calls` is read-only for the wrapper and starts at 0.
- **Operations** are called in any order, with any number of repeats.
- **Cost** is O(1) time and O(1) extra space for every operation.

**Example 1.** Input: a source holding 4, 7, 9 and the calls peek, peek, hasNext, next, next, peek, next, hasNext. Output: the results are 4, 4, true, 4, 7, 9, 9, false, and `calls` is 1 after the first two operations and 3 at the end.

**Example 2.** Input: a source holding 5 and the calls hasNext three times, then next. Output: the results are true, true, true, 5, and `calls` is 0 before the call to `next()` and 1 after it.

**Hint.** Which operation is allowed to touch the source, and what must stay true about the slot afterward?

**Changed decision.** The source cannot restart and reports its own call count, so the proof of correctness shifts from the returned values to the number of pulls.

#### [Boundary] Flatten With Empty Lists And A Depth Limit (LeetCode 341)
<!-- id: ds-bounded-flatten -->

**Prerequisites.** The next-element invariant in this lesson and the peeking exercise above.

**Problem.** This variation of Flatten Nested List Iterator uses a class `Nest` that holds either one integer or a list of `Nest` values, and a list may be empty. Implement `FlatIterator(List<Nest> top, int maxDepth)` with the operations `hasNext()` and `next()` that return the integers in left-to-right order. The top-level list has depth 1, and each list nested inside a list has one more than its parent. The constructor does not scan the input. The first call to `hasNext()` or `next()` that would enter a list with a depth greater than `maxDepth` throws `IllegalArgumentException`, and every later call throws it again. Calls before that point behave normally. Empty lists at the start, at the end and between integers produce no values.

**Constraints.** The limits are:
- **Total size** counting integers and lists is at most `10^5`.
- **Limit** satisfies `1 <= maxDepth <= 1000`.
- **Integers** are `int` values.
- **Repeated** `hasNext()` calls return the same answer and consume nothing.
- **Exhausted** `next()` throws `NoSuchElementException`.
- **Too deep** is reported by `IllegalArgumentException` from `hasNext()` or `next()`, never by the constructor.

**Example 1.** Input: `[[], 1, [[], 2, []], [], 3, []]` with `maxDepth = 3`. Output: 1, 2, 3.

**Example 2.** Input: the same list with `maxDepth = 2`. Output: the first `next()` returns 1, and the following `hasNext()` throws `IllegalArgumentException`, because the empty list inside `[[], 2, []]` sits at depth 3.

**Hint.** When is it safe for `hasNext()` to move past an empty list, and what must it store when it reaches an integer?

**Changed decision.** Empty lists make the next element unknown without a search, and the depth limit is a failure that appears at the call that reaches the deep list, so the constructor stays cheap.

#### [Recognize] Zigzag Over K Sources With Rotation Count (LeetCode 281)
<!-- id: ds-zigzag-rotations -->

**Prerequisites.** All three exercises above.

**Problem.** This variation of Zigzag Iterator reads `k` int arrays in turns. Implement `Zigzag(int[][] sources)` with the operations `hasNext()`, `next()` and `rotations()`. The cursor names the source that supplies the next value. Right after each call to `next()`, if values remain, the cursor moves forward one source at a time, wrapping from the last source to the first, until it reaches a source with a value left. The operation `skipExhausted` is this movement, and each single step counts as one rotation. The constructor also moves the cursor from source 0 to the first non-empty source, and those steps count. The operation `rotations()` returns the total so far.

**Constraints.** The limits are:
- **Sources** number `1 <= k <= 1000`, and any source may be empty.
- **Values** total at most `10^5`.
- **No step** is taken when no values remain.
- **Exhausted** `next()` throws `NoSuchElementException`.

**Example 1.** Input: `[[1,2,3],[],[4],[5,6]]`. Output: the values come out as 1, 4, 5, 2, 6, 3, and `rotations()` is 8 after the last call.

**Example 2.** Input: `[[7,8]]`. Output: the values are 7 and 8, and `rotations()` is 1, because the cursor wraps once after 7 and stops after 8. The input `[[],[]]` has no values and `rotations()` is 0.

**Hint.** Which source must the cursor name between two calls, and when does the cursor stop moving?

**Changed decision.** The class keeps a cursor over many sources and counts its own movement, so the invariant becomes "the cursor names a source with a value left".
