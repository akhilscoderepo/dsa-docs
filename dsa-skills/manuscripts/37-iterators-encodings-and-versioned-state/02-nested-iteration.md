<!-- lesson-kind: standard -->
<!-- lesson-id: nested-iteration -->
## Nested Iteration

<!-- stage: context -->
### Why An Export Runs Out Of Memory

A reporting service exports search results that live in pages. Each page is a list of rows, and some pages are empty because a filter removed every row. The export code needs one stream of rows, so a developer writes a wrapper that copies all pages into a single list when the export starts. On a test database the export finishes in a blink. On the production database the pages hold 40 million rows. The copy needs several gigabytes before the first row leaves the server. A client that wants only the first ten rows waits for the whole copy.

A second failure appears in the same service. The page list can contain further lists inside it, to any depth, and the copy uses recursion. One deeply nested input ends the process with a stack overflow. The question of this lesson is how a class presents many sources, some empty and some nested, as one sequence without copying them.

<!-- stage: naive -->
### Copying Everything Into One List

The direct design flattens the input in the constructor and then walks the flat list. For nested input the flattening is a recursive method that descends into every inner list.

```java
final class NaiveFlatten {
    private final java.util.ArrayList<String> flat = new java.util.ArrayList<>();
    private int pos;

    NaiveFlatten(java.util.List<?> items) { collect(items); }

    private void collect(java.util.List<?> items) {
        for (Object o : items) {
            if (o instanceof java.util.List<?> inner) collect(inner);   // descends into every inner list
            else flat.add((String) o);                                  // copies every string
        }
    }

    boolean hasNext() { return pos < flat.size(); }
    String next() { return flat.get(pos++); }
}
```

For the input `["x", [], [["y"], "z"]]` the object returns `x`, `y`, `z` in that order, and `hasNext()` returns `false` afterward. Empty inner lists cost nothing, because the loop over them runs zero times. The class passes every small test.

```predict
A caller builds the object with a list that nests 100000 levels deep and holds one string at the bottom. What happens in the constructor, and what happens when only the first element is needed from a flat input of 40 million strings?

For the deep list, collect calls itself 100000 times, and each call occupies a stack frame, so the thread throws StackOverflowError before any string is read. For the flat input, the constructor copies all 40 million strings before the first call to next, so the caller who needs one element still waits for and stores all of them.
```

<!-- stage: bottleneck -->
### Work Before The First Answer

Let `T` be the total number of strings and `d` the deepest nesting. The constructor costs O(T) time and O(T) memory before it answers any call. The recursion adds O(d) stack frames. The default thread stack holds roughly ten thousand frames of this size, so a nesting depth of 10^5 fails with an error, not with a slow answer.

The copy also freezes the data. When a page changes after the constructor ran, the flat list still shows the old rows. A wrapper that reads the pages on demand shows the rows that exist at the time of the call.

A correct design must meet three requirements. It must do work proportional to the elements the caller actually requests, plus the empty pages it passes. It must use memory proportional to the nesting depth and not to the total size. It must answer `hasNext()` truthfully even when the next several pages are empty, because a `true` answer followed by a failing `next()` breaks the contract.

<!-- stage: insight -->
### Remember Where You Stopped

#### Producing Elements On Demand

A **lazy sequence** is a sequence whose elements are produced only when a caller asks for them. The iterators of this lesson are lazy: the constructor stores references to the sources and does no traversal. Each call to `next()` does the small amount of work needed to find one element, and the work for later elements waits for later calls.

<!-- names: lazy sequence, local cursor, cursor stack -->

#### One Position Inside Each Source

A source is an array, a list, or a nested list. A **local cursor** is the position inside one source that marks its next unread element. For a list of pages, the iterator needs the page index and the column inside that page. Together they identify the next element, and nothing else needs storing. The invariant of this lesson is that the stored position names exactly the next nonempty source and the next unread element in it, or the end of all sources.

#### Passing Empty Sources Before Answering

A page that is empty, or already read to its end, holds no element, so a position that points at it is not a valid answer. The iterator repairs the position before it answers. A private method, here called `settle`, moves the position forward while the current source has no unread element. After `settle`, either the position points at a real element or it lies past the last source. Both `hasNext()` and `next()` call it first. The method `hasNext()` then compares the position with the end, and `next()` reads the element and advances the column by one. Repeated calls to `hasNext()` do not change anything after the first, because a settled position stays settled.

#### One Cursor For Each Open Level

A nested list adds a second dimension, because an element may itself be a source. The iterator then keeps a **cursor stack**: one local cursor for each list that is currently open. The top of the stack is the innermost open list. When the top cursor yields a list, the iterator pushes a cursor for that list. When the top cursor runs out of elements, the iterator pops it and continues in the list below. The stack never holds more entries than the current nesting depth, so memory is O(d). The recursion that overflowed the call stack becomes a loop over an object on the heap.

<!-- stage: variables -->
### Fields For Pages And For Nested Lists

The page iterator and the nested iterator keep these fields.

- **pages** is the list of pages, each a list of strings, and it is never copied.
- **page** is the index of the page that holds the next element, and it equals the page count at the end.
- **col** is the index of the next unread string inside page `page`.
- **stack** holds one iterator for each open list, with the innermost list on top.
- **depth** is the number of iterators on `stack`, and the trace shows it.
- **outer** is the number of items taken from the outermost list, and only the trace shows it.
- **ready** holds the next string once `hasNext()` found it, and it is empty otherwise.

The invariant is that `col` is less than the size of page `page` after `settle`, or `page` equals the page count. For the nested iterator, `ready` is either empty or holds the next string, and the stack contains only lists that may still hold elements.

<!-- stage: trace -->
### Tracing Pages And Nested Lists

#### Passing Empty Pages

The first trace reads four pages, `[a, b]`, `[]`, `[c]` and `[]`, and makes the calls `hasNext()`, `next()`, `next()`, `hasNext()`, `next()` and `hasNext()` in that order. The pointer `page` marks the page that holds the next element, and `col` is the column in that page. The first call, `hasNext()`, finds `a` at column 0 of page 0 and returns `true`. Two calls to `next()` return `a` and `b` and move `col` to 2, which equals the size of page 0. No call has asked for more, so `page` stays at 0 and the position is not settled. The next `hasNext()` call settles it. It passes page 0 because the column reached its size, passes the empty page 1, and stops at page 2 with `col` 0. It returns `true`. One `next()` returns `c`. The last `hasNext()` passes page 2, whose single element is used up, and the empty page 3. It reaches page 4, one past the last page, so it returns `false`.

```trace
{"cells":["[a,b]","[]","[c]","[]"],"pointers":["page"],"steps":[{"at":{"page":0},"vars":{"col":0,"call":"new","result":"none"},"note":"Start: the position is page 0, column 0, and nothing is settled yet."},{"at":{"page":0},"vars":{"col":0,"call":"hasNext()","result":"true"},"note":"hasNext finds a at column 0 of page 0 and returns true."},{"at":{"page":0},"vars":{"col":1,"call":"next()","result":"a"},"note":"next returns a and moves col to 1."},{"at":{"page":0},"vars":{"col":2,"call":"next()","result":"b"},"note":"next returns b and moves col to 2, which equals the size of page 0. The position stays on page 0 until a call needs more."},{"at":{"page":2},"vars":{"col":0,"call":"hasNext()","result":"true"},"note":"hasNext passes page 0 because col equals its size, passes the empty page 1, and stops at page 2 with col 0. It returns true."},{"at":{"page":2},"vars":{"col":1,"call":"next()","result":"c"},"note":"next returns c and moves col to 1."},{"at":{"page":4},"vars":{"col":0,"call":"hasNext()","result":"false"},"note":"hasNext passes page 2 and the empty page 3, reaches page 4 (one past the last page) and returns false."}]}
```

#### Descending Into Inner Lists

The second trace reads the nested input `["x", [], [["y"], "z"]]`. The pointer `outer` counts the items taken from the outermost list, and the variable `depth` counts the cursors on the stack, which is the stack size in the code. The first `hasNext()` takes `x` from the outer list, stores it in `ready` and returns `true`, and `next()` hands it out. The second `hasNext()` takes the empty list, pushes a cursor for it, finds nothing, and pops it again. It then takes the list `[["y"], "z"]`, pushes it, takes `["y"]`, pushes that too, and finds `y` at depth 3. The call `next()` returns `y`. The third `hasNext()` pops the exhausted cursor of `["y"]`, finds `z` at depth 2, and `next()` returns it. The last `hasNext()` pops both remaining cursors, reaches depth 0 and returns `false`.

```trace
{"cells":["x","[]","[[y],z]"],"pointers":["outer"],"steps":[{"at":{"outer":0},"vars":{"depth":1,"ready":"none","call":"new","result":"none"},"note":"Start: the stack holds one cursor for the outer list, and nothing is taken."},{"at":{"outer":1},"vars":{"depth":1,"ready":"x","call":"hasNext()","result":"true"},"note":"hasNext takes x from the outer list, stores it in ready and returns true."},{"at":{"outer":1},"vars":{"depth":1,"ready":"none","call":"next()","result":"x"},"note":"next returns x and clears ready."},{"at":{"outer":3},"vars":{"depth":3,"ready":"y","call":"hasNext()","result":"true"},"note":"hasNext opens the empty list and pops it, then opens [[y],z] and [y], and finds y at depth 3. It returns true."},{"at":{"outer":3},"vars":{"depth":3,"ready":"none","call":"next()","result":"y"},"note":"next returns y and clears ready."},{"at":{"outer":3},"vars":{"depth":2,"ready":"z","call":"hasNext()","result":"true"},"note":"hasNext pops the finished cursor of [y] and finds z at depth 2. It returns true."},{"at":{"outer":3},"vars":{"depth":2,"ready":"none","call":"next()","result":"z"},"note":"next returns z and clears ready."},{"at":{"outer":3},"vars":{"depth":0,"ready":"none","call":"hasNext()","result":"false"},"note":"hasNext pops the two remaining cursors, reaches depth 0 and returns false."}]}
```

<!-- stage: code -->
### Lazy Iterators For Both Shapes

#### The Page Iterator

The constructor stores the reference. The method `settle` is the only place where `page` changes.

```java
final class PageIterator {
    private final java.util.List<java.util.List<String>> pages;
    private int page, col;

    PageIterator(java.util.List<java.util.List<String>> pages) { this.pages = pages; }

    private void settle() {
        while (page < pages.size() && col == pages.get(page).size()) { page++; col = 0; }   // passes used-up and empty pages
    }

    boolean hasNext() { settle(); return page < pages.size(); }

    String next() {
        settle();
        if (page == pages.size()) throw new java.util.NoSuchElementException();   // exhausted: the sequence is unchanged
        return pages.get(page).get(col++);                                         // reads one string and advances col
    }
}
```

#### The Nested Iterator

The loop in `hasNext` replaces recursion. It pops exhausted cursors, pushes a cursor for each inner list, and stops at the first string.

```java
final class NestedWords {
    private final java.util.ArrayDeque<java.util.Iterator<?>> stack = new java.util.ArrayDeque<>();
    private String ready;

    NestedWords(java.util.List<?> items) { stack.push(items.iterator()); }

    boolean hasNext() {
        while (ready == null && !stack.isEmpty()) {
            java.util.Iterator<?> top = stack.peek();
            if (!top.hasNext()) { stack.pop(); continue; }           // this level is finished
            Object o = top.next();
            if (o instanceof java.util.List<?> inner) stack.push(inner.iterator());   // open one more level
            else ready = (String) o;                                  // found the next string
        }
        return ready != null;
    }

    String next() {
        if (!hasNext()) throw new java.util.NoSuchElementException();
        String r = ready;
        ready = null;                                                  // the string is consumed
        return r;
    }
}
```

#### Cost

- **PageIterator** costs O(1) amortized time per call, because every page boundary is passed once, and O(1) extra space.
- **NestedWords** costs O(1) amortized time per element plus one step for each list it opens, and O(d) space for nesting depth `d`.

<!-- stage: applicability -->
### When To Keep Cursors, Not Copies

#### Recognizing The Pattern

Use this method when a class must show several arrays, lists or nested values as one sequence, and when the total is large or the nesting is deep. Phrases such as "flatten", "skip empty" and "round robin" signal it. Before coding, write down what identifies the next element in one source. Decide how many such identifiers the iterator must hold at once. Name the one method that repairs the position. The invariant to keep is that after the repair the position names the next element or the end.

#### A False Friend

A constructor that flattens the input is a false friend of a lazy iterator. It returns the right order and fails on size, on depth and on sources that change. A second false friend is a `hasNext()` that only checks that the current page exists. It returns `true` for an empty page, and the following `next()` call has nothing to return.

#### When The Method Does Not Apply

When the input is small, fixed and read once, a plain loop with two levels is simpler. When the problem needs random access by index into the flattened sequence, a lazy cursor cannot jump, and a prefix array of source sizes is the better tool.

<!-- stage: exercises -->
### Exercises

#### [Build] Flatten 2D Vector (LeetCode 251)
<!-- id: it37-flatten-2d-vector -->

**Prerequisites.** The Iterator Protocols lesson and the page iterator from this lesson. This exercise changes the contract: rows are `int[]` arrays, the end throws, and `hasNext()` may be repeated without effect.

**Problem.** Design the class `Vector2D` with a constructor that receives an `int[][]` called `vec`. The method `next()` returns the next element when the rows are read in order, and each row is read from left to right. The method `hasNext()` reports whether any element is left to read. A row may be empty. The class does not copy the rows.

**Constraints.** The limits are:
- **Rows** number from 0 to 200, and each row has from 0 to 500 elements.
- **Elements** are `int` values.
- **Calls** number at most 10^5, and `hasNext()` may be called any number of times in a row.
- **Exhaustion** means `next()` throws `NoSuchElementException` and changes no logical state.

**Example 1.** Input calls `["Vector2D","next","next","hasNext","next","hasNext"]` with arguments `[[[1,2],[],[3]],[],[],[],[],[]]`, output `[null,1,2,true,3,false]`.

**Example 2.** Input calls `["Vector2D","hasNext","hasNext","next","hasNext","next"]` with arguments `[[[],[5],[]],[],[],[],[],[]]`, output `[null,true,true,5,false,"NoSuchElementException"]`.

**Hint.** Which method must pass the empty rows, and why must `hasNext()` call it too?

**Changed decision.** Basic case: a position of two integers, repaired by one private method that both public methods call before they answer.

#### [Vary] Zigzag Iterator Over K Lists (LeetCode 281)
<!-- id: it37-zigzag-k-lists -->

**Prerequisites.** The Flatten 2D Vector exercise above. This exercise changes the contract of LeetCode 281: the input is any number of arrays, not two.

**Problem.** Design the class `ZigzagIterator` with a constructor that receives a `List<int[]>` called `lists`. The method `next()` returns elements in rounds. Each round takes the next unread element of every list that still has one, in list order. Lists that have run out take no further turn. The method `hasNext()` returns `true` when any list still has an unread element.

**Constraints.** The limits are:
- **Lists** number from 0 to 500, and each list has from 0 to 100 elements.
- **Elements** are `int` values.
- **Calls** number at most 5 * 10^4.
- **Exhaustion** means `next()` throws `NoSuchElementException` and changes no field.

**Example 1.** Input calls `["ZigzagIterator","next","next","next","next","next","next","hasNext"]` with arguments `[[[1,2,3],[4],[5,6]],[],[],[],[],[],[],[]]`, output `[null,1,4,5,2,6,3,false]`.

**Example 2.** Input calls `["ZigzagIterator","next","next","hasNext"]` with arguments `[[[],[7,8],[]],[],[],[]]`, output `[null,7,8,false]`.

**Hint.** Which collection holds exactly the lists that still have elements, and in what order does it hold them?

**Changed decision.** The iterator keeps a queue of local cursors, one for each list that still has an element. A list that finishes leaves the queue and takes no more turns.

#### [Boundary] Flatten Nested List Iterator (LeetCode 341)
<!-- id: it37-nested-list-iterator -->

**Prerequisites.** The Zigzag Iterator exercise above and the nested iterator from this lesson.

**Problem.** A `NestedInteger` is either one integer, or a list of `NestedInteger` values. It offers `isInteger()`, `getInteger()` and `getList()`. Design the class `NestedIterator` with a constructor that receives a list of `NestedInteger` values. The method `next()` returns the integers in the order that they appear when the structure is read left to right and inner lists are read in place. The method `hasNext()` returns `true` when an integer remains. The class does not build the flat list.

**Constraints.** The limits are:
- **Integers** are `int` values, and the structure holds at most 10^5 of them.
- **Nesting depth** is up to 10^5, and lists may be empty at any level.
- **Calls** number at most 2 * 10^5.
- **Exhaustion** means `next()` throws `NoSuchElementException`.

**Example 1.** Input calls `["NestedIterator","next","next","next","hasNext"]` with arguments `[[[1,[2]],[],3],[],[],[],[]]`, output `[null,1,2,3,false]`.

**Example 2.** Input calls `["NestedIterator","hasNext","next","hasNext"]` with arguments `[[[[]],[4,[]],[]],[],[],[]]`, output `[null,true,4,false]`.

**Hint.** Where does the iterator record that it found an integer but has not handed it out yet?

**Changed decision.** Empty lists can nest without limit, so `hasNext()` must loop until it finds an integer or empties the stack. It cannot assume that the next item is usable.

#### [Recognize] Iterator For Combination (LeetCode 1286)
<!-- id: it37-combination-iterator -->

**Prerequisites.** The Flatten Nested List Iterator exercise above. This exercise has no nested input. The unfinished state is a small array of indexes into the character string.

**Problem.** Design the class `CombinationIterator` with a constructor that receives a string `characters` of distinct lowercase letters in increasing order and an integer `combinationLength` called `k`. A combination is a string of `k` letters taken from `characters` in their original order. The method `next()` returns the next combination in lexicographic order, starting with the first `k` letters. The method `hasNext()` returns `true` when a combination remains. The class does not store the list of all combinations.

**Constraints.** The limits are:
- **Characters** have length `n` from 1 to 15, and `1 <= k <= n`.
- **Calls** number at most 10^4.
- **Memory** must not depend on the number of combinations, which is the binomial coefficient of `n` and `k`.
- **Exhaustion** means `next()` throws `NoSuchElementException` and changes no field.

**Example 1.** Input calls `["CombinationIterator","next","hasNext","next","next","hasNext"]` with arguments `[["abc",2],[],[],[],[],[]]`, output `[null,"ab",true,"ac","bc",false]`.

**Example 2.** Input calls `["CombinationIterator","hasNext","next","hasNext","next"]` with arguments `[["xyz",3],[],[],[],[]]`, output `[null,true,"xyz",false,"NoSuchElementException"]`.

**Hint.** Which index must move first after a combination is returned, and what must the indexes to its right become?

**Changed decision.** The stored state is not a pointer into a source. It is the current combination as `k` indexes, and `next()` computes the successor from those indexes in place.
