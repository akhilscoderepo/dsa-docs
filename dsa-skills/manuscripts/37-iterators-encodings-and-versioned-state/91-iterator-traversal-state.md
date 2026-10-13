<!-- lesson-kind: combination -->
<!-- lesson-id: iterator-traversal-state -->
## Iterator Traversal State

<!-- stage: context -->
### Why Previous Shows A Key Twice

An admin console browses a sorted index of customer keys with two buttons, Next and Previous. The index is a binary search tree, and the console reads it lazily, because the tree holds millions of keys. A developer writes Next with an explicit stack, the standard way to walk a tree in order without recursion. Previous has no counterpart in that design, so the developer saves the last key on screen and returns it. A tester presses Next three times and then Previous twice. The screen shows keys 3, 7, 9, 7 and 7. The last key should be 3, because the user stepped back from 9 to 7 and then to 3. The saved value held only the key before 9, so the second Previous returned it again.

The defect comes from one stored value that tries to stand for a history. The question of this lesson is what an iterator must remember so that any sequence of forward and backward calls returns the right key.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

The lesson Iterator Protocols supplied the four questions of observation, availability, consumption and exhaustion. It also supplied the rule that a cursor holds only what identifies the next element, and that a call after the last element has one documented behavior. This lesson keeps that rule and applies it to the exercises that peek, skip by a count and run backward.

The lesson Nested Iteration supplied the repair method that moves a position past empty sources before an answer, and it supplied the stack of cursors that replaces recursion. A binary search tree traversal is the same shape: the stack holds one cursor for each ancestor whose left subtree was entered.

The new work of this lesson is the memory of what has already been handed out. Peeking needs a small buffer of elements read ahead. A backward step needs the elements read behind. The lesson shows one rule for both. Keep the unread part as a cursor and the handed-out part as a list. Let a single index say where the caller stands.

<!-- stage: naive -->
### Copying The In-Order Sequence

The direct design walks the whole tree once in the constructor and stores every key in a list. A position index then moves left and right over the list, so Previous is as easy as Next.

```java
final class NaiveTreeBrowser {
    static final class Node { int val; Node left, right; }

    private final java.util.ArrayList<Integer> keys = new java.util.ArrayList<>();
    private int pos = -1;    // index of the key on screen, -1 before the first

    NaiveTreeBrowser(Node root) { walk(root); }

    private void walk(Node n) {
        if (n == null) return;
        walk(n.left);          // keys smaller than n
        keys.add(n.val);       // n itself
        walk(n.right);         // keys larger than n
    }

    boolean hasNext() { return pos + 1 < keys.size(); }
    boolean hasPrev() { return pos > 0; }
    int next() { return keys.get(++pos); }
    int prev() { return keys.get(--pos); }
}
```

For the tree with keys 3, 7, 9, 15 and 20, the calls `next()`, `next()`, `prev()`, `next()` return 3, 7, 3 and 7. The class is correct on every small test, and Previous works.

```predict
A tree has 1000000 nodes in a straight left chain, and the caller presses Next twice and then closes the browser. What does the constructor cost, and what happens to the walk method?

The walk method calls itself once for each level of the chain, so a depth of one million exhausts the call stack. The constructor throws StackOverflowError before it stores any key, and the browser never opens. On a balanced tree with the same node count, the recursion succeeds, but the constructor still visits and stores all 1000000 keys before the first call, although the caller reads two.
```

<!-- stage: bottleneck -->
### Work And Memory Before The First Key

If the tree has `n` nodes and height `h`, the constructor costs O(n) time and O(n) memory, and the recursion needs O(h) call-stack frames. A skewed tree has `h = n`, so the recursion fails for a tree of a few tens of thousands of nodes. The caller who reads two keys pays for all of them.

The common repair is a lazy walk with an explicit stack. The constructor pushes the root and every left child below it, down to a leaf, and this chain is the left spine. Each `next` pops the top node, hands out its key and pushes the left spine of its right child. The stack holds O(h) nodes on the heap and produces each key on demand. That walk gives up the reverse direction. When it pops a node and hands out its key, the node leaves the stack, and nothing in the stack describes the keys already handed out. A Previous call has no data to read.

A correct design must therefore meet three requirements. Next must remain lazy, so the work is proportional to the keys that the caller reaches. Previous must return the key before the current one without any traversal. The two directions must agree after any sequence of calls. A Next after a Previous must repeat the key the caller saw before, and it must not read the tree again.

<!-- stage: insight -->
### Unread Keys And Read Keys

#### Two Stores And One Position

<!-- names: pending stack, visited list, history position -->

The iterator keeps the unread keys in a **pending stack**: the stack of tree nodes that the lazy in-order walk has entered and not yet handed out. Its top is the smallest unread key. It keeps the keys already handed out in a **visited list**, in the order they were handed out, which is ascending order. A **history position** is one integer that names the key on screen, as an index into the visited list. It starts at -1, before the first key.

The two stores and the position describe one sequence. The visited list holds the prefix of the in-order sequence that the iterator has reached so far. The pending stack describes the rest of the sequence, from the smallest unread key onward. The history position says where inside the prefix the caller stands.

#### Next Replays Or Extends

A call to `next` first looks at the history position. When a visited key lies after it, the iterator adds 1 to the position and returns that key from the list, and it does not touch the tree. This replay is what makes Next after Previous correct. When the position is already at the last visited key, the iterator extends the history. It pops the top node of the pending stack and pushes the left spine of that node's right child. It then appends the key to the visited list and adds 1 to the position. When the stack is also empty, the sequence is exhausted, and the call throws `NoSuchElementException`.

#### Previous Moves Only The Position

A call to `prev` needs no tree access. If the position is above 0, the iterator subtracts 1 and returns the key at the new position. Otherwise no key lies before the current one, and the call throws `NoSuchElementException` without changing the position. The visited list is never shortened, because the caller may press Next again, and the replay path returns those keys from memory.

<!-- stage: variables -->
### Fields Of The Tree Browser

The lesson's browser stores two stores and one position besides the tree. Each lookahead or skipping exercise keeps the matching small cursor.

- **pending** is the stack of nodes entered by the walk and not yet handed out, with the smallest unread key on top.
- **visited** is the list of keys handed out so far, in ascending order, and it never shrinks.
- **pos** is the history position, the index in `visited` of the key on screen, from -1 to `visited.size() - 1`.

The invariant is that `visited` is a prefix of the in-order sequence and `pending` produces exactly the keys after that prefix, in order.

<!-- stage: trace -->
### Tracing Forward And Backward Calls

#### Extending And Then Replaying

The tree has root 7, left child 3, right child 15, and 15 has children 9 and 20. Its in-order keys are 3, 7, 9, 15 and 20. The pointer `pos` marks the history position over those five keys, and the variable `pending` lists the stack from the top. The constructor pushes the left spine 7 and 3, so 3 is on top. The first `next` pops 3, finds no right child, appends 3 and moves `pos` to 0. The second `next` pops 7 and pushes the left spine of 15, which is 15 and 9. It appends 7 and moves `pos` to 1. The third `next` pops 9 and appends it. Then `prev` moves `pos` from 2 to 1 and returns 7, and a second `prev` returns 3. The following `next` returns 7 and the one after it returns 9, both from the visited list, so `pending` does not change. The call after that extends the history again with 15.

```trace
{"cells":["3","7","9","15","20"],"pointers":["pos"],"steps":[{"at":{"pos":-1},"vars":{"call":"new","result":"none","visited":"[]","pending":"[3,7]"},"note":"Start: the constructor pushed the left spine, so the smallest key is on top of pending, and pos is -1."},{"at":{"pos":0},"vars":{"call":"next()","result":3,"visited":"[3]","pending":"[7]"},"note":"next pops 3, which has no right child, appends 3 and moves pos to 0."},{"at":{"pos":1},"vars":{"call":"next()","result":7,"visited":"[3,7]","pending":"[9,15]"},"note":"next pops 7 and pushes the left spine of 15, which is 15 and 9. It appends 7 and moves pos to 1."},{"at":{"pos":2},"vars":{"call":"next()","result":9,"visited":"[3,7,9]","pending":"[15]"},"note":"next pops 9, appends it and moves pos to 2."},{"at":{"pos":1},"vars":{"call":"prev()","result":7,"visited":"[3,7,9]","pending":"[15]"},"note":"prev moves pos from 2 to 1 and returns 7 from visited. The tree is not read."},{"at":{"pos":0},"vars":{"call":"prev()","result":3,"visited":"[3,7,9]","pending":"[15]"},"note":"prev moves pos to 0 and returns 3 from visited."},{"at":{"pos":1},"vars":{"call":"next()","result":7,"visited":"[3,7,9]","pending":"[15]"},"note":"next replays 7 from visited. pending is unchanged."},{"at":{"pos":2},"vars":{"call":"next()","result":9,"visited":"[3,7,9]","pending":"[15]"},"note":"next replays 9 from visited. pending is unchanged."},{"at":{"pos":3},"vars":{"call":"next()","result":15,"visited":"[3,7,9,15]","pending":"[20]"},"note":"pos is at the last visited key, so next extends the history. It pops 15, pushes the left spine of 20, appends 15 and moves pos to 3."}]}
```

#### Both Ends Of The Sequence

The second tree has root 2 with children 1 and 3. The first three `next` calls append 1, 2 and 3 and leave `pending` empty. The call `hasNext` then returns `false`, because no visited key lies after `pos` and the stack is empty. A fourth `next` throws `NoSuchElementException` and changes nothing. Two `prev` calls move back to 1. At that point `pos` is 0, so `hasPrev` returns `false`, and a third `prev` throws. A `next` call afterward returns 2 from the visited list. The trace shows that the throwing calls leave `pos` and `visited` unchanged.

```trace
{"cells":["1","2","3"],"pointers":["pos"],"steps":[{"at":{"pos":-1},"vars":{"call":"new","result":"none","visited":"[]","pending":"[1,2]"},"note":"Start: the constructor pushed the left spine, so the smallest key is on top of pending, and pos is -1."},{"at":{"pos":0},"vars":{"call":"next()","result":1,"visited":"[1]","pending":"[2]"},"note":"next pops 1 and appends it. pos is 0."},{"at":{"pos":1},"vars":{"call":"next()","result":2,"visited":"[1,2]","pending":"[3]"},"note":"next pops 2, pushes the left spine of 3 and appends 2. pos is 1."},{"at":{"pos":2},"vars":{"call":"next()","result":3,"visited":"[1,2,3]","pending":"[]"},"note":"next pops 3 and appends it. pending is now empty and pos is 2."},{"at":{"pos":2},"vars":{"call":"hasNext()","result":"false","visited":"[1,2,3]","pending":"[]"},"note":"No visited key lies after pos, and pending is empty, so hasNext returns false."},{"at":{"pos":2},"vars":{"call":"next()","result":"throws","visited":"[1,2,3]","pending":"[]"},"note":"next finds nothing to replay or extend, throws NoSuchElementException and changes no field."},{"at":{"pos":1},"vars":{"call":"prev()","result":2,"visited":"[1,2,3]","pending":"[]"},"note":"prev moves pos to 1 and returns 2."},{"at":{"pos":0},"vars":{"call":"prev()","result":1,"visited":"[1,2,3]","pending":"[]"},"note":"prev moves pos to 0 and returns 1."},{"at":{"pos":0},"vars":{"call":"hasPrev()","result":"false","visited":"[1,2,3]","pending":"[]"},"note":"pos is 0, so no key lies before the current one and hasPrev returns false."},{"at":{"pos":0},"vars":{"call":"prev()","result":"throws","visited":"[1,2,3]","pending":"[]"},"note":"prev throws NoSuchElementException and leaves pos at 0."},{"at":{"pos":1},"vars":{"call":"next()","result":2,"visited":"[1,2,3]","pending":"[]"},"note":"next replays 2 from visited and moves pos to 1."}]}
```

<!-- stage: code -->
### The Reversible Tree Iterator

#### The Class

The class below needs the tree node type, so the node is a nested class. The method `hasNext` asks for a key after the position in the visited list, or a node in the pending stack. The method `next` replays when it can and extends only when it must.

```java
final class TreeBrowser {
    static final class Node { int val; Node left, right; }

    private final java.util.ArrayDeque<Node> pending = new java.util.ArrayDeque<>();
    private final java.util.ArrayList<Integer> visited = new java.util.ArrayList<>();
    private int pos = -1;

    TreeBrowser(Node root) { spine(root); }

    private void spine(Node n) {
        for (; n != null; n = n.left) pending.push(n);          // enters every left child down to a leaf
    }

    boolean hasNext() { return pos + 1 < visited.size() || !pending.isEmpty(); }
    boolean hasPrev() { return pos > 0; }

    int next() {
        if (!hasNext()) throw new java.util.NoSuchElementException();   // exhausted: no field changes
        if (pos + 1 == visited.size()) {                                // the history ends here, so extend it
            Node n = pending.pop();
            spine(n.right);
            visited.add(n.val);
        }
        return visited.get(++pos);                                      // replay or fresh key, one step right
    }

    int prev() {
        if (!hasPrev()) throw new java.util.NoSuchElementException();   // nothing before the current key
        return visited.get(--pos);                                      // only the position moves
    }
}
```

#### One Rule For All Four Iterators

The same split appears in every exercise below. A lookahead iterator keeps the read-ahead elements in a small buffer and pulls from the source only when the buffer is too short. A run skipper keeps a cursor of run index and used count and jumps by subtraction. A nested iterator keeps a stack of open lists. A bounded tree iterator keeps the pending stack and the visited list. The invariant is that the stored history and the stored cursor always describe one position in one sequence, and extending the history never skips or repeats a key.

#### Cost

- **Constructor** costs O(h) time and O(h) space for tree height `h`.
- **next** costs O(1) amortized time, because each node enters and leaves the stack once, and a replayed call is O(1).
- **prev** costs O(1) time, and the visited list adds O(k) memory for the `k` keys reached so far.

<!-- stage: applicability -->
### When History And Cursor Share State

#### Recognizing The Pattern

Use this method when one class must answer calls in two directions, or look ahead, or skip by a count, over a sequence that is too large to copy. The words `prev`, `peek` and `skip` signal it. Before coding, separate the sequence into the part already handed out and the part still unread. Decide which structure holds each part, and let one integer or one cursor say where the caller stands. The invariant to keep is that the two parts always describe a single sequence with no gap and no overlap.

#### A False Friend

A single saved value is a false friend of a history. It answers Previous once, and a second Previous has nothing to return. A second false friend is a forward stack that pops nodes and assumes the caller never returns. It works for forward-only traversal and loses every key it popped.

#### When The Method Does Not Apply

If the caller only moves forward, the visited list is wasted memory, and the stack and a cursor are enough. If the caller needs arbitrary jumps to the k-th key, an order-statistic structure, such as a balanced tree with subtree sizes, answers faster than replaying a history.

<!-- stage: exercises -->
### Exercises

#### [Build] Peeking Iterator With Lookahead Offset (LeetCode 284)
<!-- id: it37-lookahead-peeking -->

**Prerequisites.** The lesson Iterator Protocols and its Peeking Iterator exercise. This exercise changes the contract of LeetCode 284: a peek may look several elements ahead.

**Problem.** Design the class `LookaheadIterator` with a constructor that receives an `Iterator<Integer>` called the source. The method `peek(offset)` returns the element that lies `offset` positions after the next element, so `peek(0)` returns the next element, and it consumes nothing. The method `next()` returns and consumes the next element. The method `hasNext()` reports whether an element remains. The class pulls from the source only the elements that a call needs.

**Constraints.** The limits are:
- **Elements** are `Integer` values from -10^9 to 10^9.
- **Offset** is an `int` from -5 to 100, and calls number at most 1000.
- **Invalid offset** means a negative offset throws `IllegalArgumentException`, and an offset past the end throws `NoSuchElementException`.
- **Failing calls** change no element, so the next successful call sees the same sequence.

**Example 1.** Input calls `["LookaheadIterator","peek","peek","next","peek","peek","hasNext"]` with arguments `[[[10,20,30,40]],[2],[0],[],[2],[3],[]]`, output `[null,30,10,10,40,"NoSuchElementException",true]`.

**Example 2.** Input calls `["LookaheadIterator","hasNext","peek","peek"]` with arguments `[[[]],[],[0],[-1]]`, output `[null,false,"NoSuchElementException","IllegalArgumentException"]`.

**Hint.** Which collection holds the elements pulled from the source but not yet consumed, and when must a peek that runs past the end leave them in place?

**Changed decision.** The single cached element becomes a buffer of read-ahead elements. A peek past the end still keeps what it pulled, so the sequence stays intact for later calls.

#### [Vary] Run Skipper (LeetCode 900)
<!-- id: it37-run-skipper -->

**Prerequisites.** The lesson Iterator Protocols and its RLE Iterator exercise. This exercise changes the contract of LeetCode 900: counts are `long`, a skip may consume fewer elements than requested, and exhaustion throws.

**Problem.** Design the class `RunSkipper` with a constructor that receives a `long[]` called `counts` and an `int[]` called `values` of the same length. Run `i` repeats `values[i]` exactly `counts[i]` times, and the runs form one sequence in index order. The method `skip(n)` consumes up to `n` elements and returns the number actually consumed. The method `peek()` returns the next element without consuming it. The method `next()` consumes and returns the next element. The method `hasNext()` reports whether an element remains.

**Constraints.** The limits are:
- **Runs** number from 0 to 1000.
- **Counts** are `long` values from 0 to 10^18, and the sum of all counts can exceed `Long.MAX_VALUE`.
- **Argument** `n` is a `long` from 0 to 10^18, and calls number at most 1000.
- **Exhaustion** means `peek()` and `next()` throw `NoSuchElementException`, and `skip` returns 0.

**Example 1.** Input calls `["RunSkipper","skip","peek","next","skip","peek","hasNext"]` with arguments `[[[4,2,1000000000000000000],[1,2,3]],[5],[],[],[7],[],[]]`, output `[null,5,2,2,7,3,true]`.

**Example 2.** Input calls `["RunSkipper","skip","hasNext","skip","peek"]` with arguments `[[[2,1],[6,7]],[5],[],[1],[]]`, output `[null,3,false,0,"NoSuchElementException"]`.

**Hint.** Why must the class never compute the sum of the counts, and what quantity does each loop round subtract instead?

**Changed decision.** Consumption by a count may stop early, so the return value is a consumed count and not a value. The loop works with differences, because a total could overflow `long`.

#### [Boundary] Depth-Weighted Nested Iterator (LeetCode 341)
<!-- id: it37-depth-weighted-nested -->

**Prerequisites.** The lesson Nested Iteration and its Flatten Nested List Iterator exercise. This exercise changes the contract of LeetCode 341: each integer comes back multiplied by its depth.

**Problem.** A `NestedInteger` is either one integer, or a list of `NestedInteger` values, with the methods `isInteger()`, `getInteger()` and `getList()`. The input is the top-level list, which has depth 1. A list inside a list of depth `d` has depth `d + 1`, and an integer has the depth of the list that directly contains it. Design the class `DepthWeightedIterator` whose `next()` returns the integers in reading order, each multiplied by its depth, as a `long`. The method `hasNext()` reports whether an integer remains.

**Constraints.** The limits are:
- **Integers** are `int` values from -10^9 to 10^9, and the structure holds at most 10^5 of them.
- **Depth** is up to 10^5, and lists may be empty at any level.
- **Result** is a `long`, because a product can reach 10^14.
- **Exhaustion** means `next()` throws `NoSuchElementException`.

**Example 1.** Input calls `["DepthWeightedIterator","next","next","next","hasNext"]` with arguments `[[[1,[2]],[],3],[],[],[],[]]`, output `[null,2,6,3,false]`.

**Example 2.** Input calls `["DepthWeightedIterator","next","hasNext"]` with arguments `[[[],[[-4]]],[],[]]`, output `[null,-12,false]`.

**Hint.** At the moment the iterator finds an integer, which structure already knows the depth, and what type must hold the product?

**Changed decision.** The depth is not stored separately. The size of the stack of open lists at the moment of discovery is the depth, and the result type widens from `int` to `long`.

#### [Recognize] Range-Bounded BST Iterator (LeetCode 1586)
<!-- id: it37-bst-iterator-range -->

**Prerequisites.** The lesson text above and the Flatten Nested List Iterator exercise of the lesson Nested Iteration. This exercise changes the contract of LeetCode 1586: only keys inside a closed range take part.

**Problem.** Design the class `RangeBstIterator` with a constructor that receives the root of a binary search tree with distinct keys and two integers `lo` and `hi`. The sequence is the keys `k` with `lo <= k <= hi` in ascending order. The current position starts before the first key. The method `next()` moves the current position one key to the right and returns that key. The method `prev()` moves it one key to the left and returns that key. The methods `hasNext()` and `hasPrev()` report whether a key exists to the right of the current position, or to the left of the current key.

**Constraints.** The limits are:
- **Nodes** number from 0 to 10^5, and keys are distinct `int` values from 0 to 10^6.
- **Range** satisfies `0 <= lo <= hi <= 10^6`.
- **Height** may reach 10^5, so recursion over the tree is not allowed.
- **Failing calls** `next()` or `prev()` with no key in that direction throw `NoSuchElementException` and change no field.

**Example 1.** Input calls `["RangeBstIterator","next","next","prev","hasPrev","hasNext","next","next","hasNext"]` with arguments `[[7,3,15,null,null,9,20],5,16]` for the constructor and empty arguments for the calls, output `[null,7,9,7,false,true,9,15,false]`.

**Example 2.** Input calls `["RangeBstIterator","hasNext","hasPrev","next"]` with arguments `[[2,1,3],4,9]` for the constructor and empty arguments for the calls, output `[null,false,false,"NoSuchElementException"]`.

**Hint.** Which nodes may the left-spine push skip because their key is below `lo`, and how does the iterator know that a stack top above `hi` ends the sequence?

**Changed decision.** The range bounds the walk on both sides. The push skips nodes below `lo` by moving right, and a top node above `hi` ends the sequence for every node under it, because the stack is ascending.
