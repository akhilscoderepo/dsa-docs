<!-- lesson-kind: standard -->
<!-- lesson-id: iterator-protocols -->
## Iterator Protocols

<!-- stage: context -->
### Why A Parser Loses Its Token

A script interpreter reads tokens through a class with one method, `next()`. The parser must decide whether the next token is the word `else` before it picks a branch. It has no way to look, so it calls `next()`, sees `else`, and learns that the token belongs to a different grammar rule. The token is already gone. The next parsing function starts one token late and reports a syntax error on a line that is correct.

A second reader of the same class has the opposite trouble. It calls `next()` after the last token and receives a garbage value, because the class never defined what happens at the end. Both failures come from one gap. The class lets callers take elements. It does not say what a caller may ask without taking anything. It also does not say what the call after the last element returns. This lesson asks how to specify and implement a class so that asking, taking and finishing each have one defined behavior.

<!-- stage: naive -->
### Expanding The Whole Sequence

The direct design reads the entire input into a list in the constructor and then walks the list with an integer. A compressed log stores pairs of a count and a value, such as `3` copies of `8`. The class below expands every pair and offers `next` and a look-ahead called `peek`.

```java
final class NaiveRunReader {
    private final java.util.ArrayList<Integer> items = new java.util.ArrayList<>();
    private int pos;

    NaiveRunReader(int[] counts, int[] values) {
        for (int r = 0; r < counts.length; r++)
            for (int k = 0; k < counts[r]; k++) items.add(values[r]);   // writes every copy
    }

    int next() { return items.get(pos++); }

    int peek() {
        int v = next();    // take the element
        pos--;             // then put it back
        return v;
    }

    boolean hasNext() { return pos < items.size(); }
}
```

With counts `{2, 1}` and values `{8, 5}`, the calls `peek()`, `next()`, `next()`, `next()` return 8, 8, 8 and 5. The answers are correct, and the class looks finished.

```predict
A caller builds the reader with counts {1000000000} and values {7}, and then calls next() once. What happens, and what does the class do when the caller calls next() four times on counts {2} and values {7}?

The constructor tries to store one billion Integer references, so it runs for a long time and then fails with an OutOfMemoryError before next() is ever called. On the short input, the fourth call to next() reaches the end of the list and throws an IndexOutOfBoundsException that names a list index the caller never used. The class never decided what the end looks like, so that message is an accident of the list inside it.
```

<!-- stage: bottleneck -->
### Memory That Depends On The Counts

The constructor writes one list entry for every logical element. If the counts add up to `S`, construction costs O(S) time and O(S) memory. A log with 2000 runs and counts near 10^9 holds about 2 * 10^12 logical elements, which no heap holds. The caller who needs only the first value still pays for all of them.

The constructor is not the only weak point. The look-ahead works by taking an element and putting it back, which is legal only because the data sits in a list that can move backward. A source that reads from a file or a network stream cannot move backward, so the same idea fails there. The class also leaks its internal list in the exception at the end of the data. A caller cannot rely on any documented behavior there.

A correct design therefore needs three properties. It must answer every call in time that does not depend on the counts. It must look at the next element without taking it. It must define the call after the last element in the documentation, not by accident.

<!-- stage: insight -->
### Four Separate Questions

#### One Cursor Marks The Next Element

<!-- names: cursor, observation, consumption, exhaustion -->

A **cursor** is the small group of fields that identifies the next element to hand out and nothing else. For an array it is one integer. For a log of runs it is two numbers: the index of the current run and the count of elements already taken from that run. The iterator never stores the elements that lie ahead of the cursor, so its memory does not depend on how many elements remain.

#### Observation, Availability, Consumption And Exhaustion

An iterator protocol answers four questions, and each question gets its own method with its own effect on the cursor. **Observation** means reading the next element without moving the cursor. `peek()` performs it, and calling it twice returns the same element twice. Availability is the question whether an element exists, and `hasNext()` answers it with no effect on the cursor, however often the caller repeats it. **Consumption** means returning the next element and moving the cursor past it exactly once. `next()` performs it.

**Exhaustion** is the state in which the cursor lies past the last element. This lesson fixes one rule for it. A call to `next()` or `peek()` in that state throws `NoSuchElementException`, the exception that the Java `Iterator` interface documents, and it changes no field. A caller that wants to avoid the exception checks `hasNext()` first.

#### Skipping Without Expanding

A run of count zero, or a run that the cursor has fully used, holds no element. The cursor moves past such runs lazily, inside the call that needs the next element. The move is a loop over run boundaries, so it costs time proportional to the runs it skips and never to the counts. Counts are stored as `long` values, because a count near 10^9 is legal and a sum of counts exceeds `int`.

The invariant of the protocol is that observation never moves the cursor, consumption moves it exactly once, and the cursor never points past the end of the data.

<!-- stage: variables -->
### Cursor Fields In Both Classes

The lesson uses two small classes, and the trace follows the first fields of each.

- **tokens** is the array of strings that the token reader serves.
- **pos** is the index of the next unread token, from 0 to `tokens.length`.
- **counts** is the `long` array with the length of each run.
- **run** is the index of the run that holds the next element, and it equals the number of runs when the sequence is exhausted.
- **used** is the number of elements already taken from run `run`.

The invariant is `0 <= pos <= tokens.length` for the reader, and `0 <= used <= counts[run]` for the run reader whenever `run` is a valid index.

<!-- stage: trace -->
### Tracing Calls On Both Cursors

#### The Token Reader With Look-Ahead

The pointer `pos` marks the next unread token. The first call, `peek()`, returns `let` and leaves `pos` at 0, and a second `peek()` returns `let` again. The call `next()` returns `let` and moves `pos` to 1. The calls `next()` for `x`, `=` and `5` move `pos` to 4, which equals the number of tokens. At that point `hasNext()` returns `false`. The last call, `next()`, finds the cursor past the end, throws `NoSuchElementException` and leaves `pos` at 4. The trace shows that only `next` ever changes `pos`.

```trace
{"cells":["let","x","=","5"],"pointers":["pos"],"steps":[{"at":{"pos":0},"vars":{"call":"new","result":"none"},"note":"Start: pos is 0, so the first token is next."},{"at":{"pos":0},"vars":{"call":"peek()","result":"let"},"note":"peek returns let and leaves pos at 0."},{"at":{"pos":0},"vars":{"call":"peek()","result":"let"},"note":"A second peek returns let again, because observation does not move pos."},{"at":{"pos":1},"vars":{"call":"next()","result":"let"},"note":"next returns let and moves pos to 1."},{"at":{"pos":2},"vars":{"call":"next()","result":"x"},"note":"next returns x and moves pos to 2."},{"at":{"pos":3},"vars":{"call":"next()","result":"="},"note":"next returns = and moves pos to 3."},{"at":{"pos":4},"vars":{"call":"next()","result":"5"},"note":"next returns 5 and moves pos to 4."},{"at":{"pos":4},"vars":{"call":"hasNext()","result":"false"},"note":"pos equals the number of tokens, so hasNext returns false and changes nothing."},{"at":{"pos":4},"vars":{"call":"next()","result":"throws"},"note":"The cursor lies past the last token, so next throws NoSuchElementException and pos stays at 4."}]}
```

#### The Run Reader Skips Empty Runs

The second trace follows a run reader with runs `a` twice, `b` zero times and `c` once. The pointer `run` marks the run that holds the next element. The first `next()` returns `a` and raises `used` to 1. The second `next()` returns `a` and raises `used` to 2, which equals the count of run 0. The reader does not move to run 1 yet, because no caller has asked for another element. The third `next()` finds run 0 used up, passes run 1 because its count is zero, lands on run 2 and returns `c`. The last `hasNext()` passes run 2 and reaches run 3, one past the last run, so it returns `false`. Every move across a run boundary happens inside a call that needs it.

```trace
{"cells":["a x2","b x0","c x1"],"pointers":["run"],"steps":[{"at":{"run":0},"vars":{"used":0,"call":"new","result":"none"},"note":"Start: run 0 holds the next element and nothing is used."},{"at":{"run":0},"vars":{"used":1,"call":"next()","result":"a"},"note":"next returns a and raises used to 1."},{"at":{"run":0},"vars":{"used":2,"call":"next()","result":"a"},"note":"next returns a and raises used to 2. Run 0 is now used up, but no call has asked for more yet, so run stays 0."},{"at":{"run":2},"vars":{"used":1,"call":"next()","result":"c"},"note":"next passes the used-up run 0 and the empty run 1, lands on run 2 and returns c with used 1."},{"at":{"run":3},"vars":{"used":0,"call":"hasNext()","result":"false"},"note":"hasNext passes the used-up run 2 and reaches run 3, one past the last run, so it returns false."}]}
```

<!-- stage: code -->
### Two Iterators With Defined Ends

#### The Token Reader

The reader stores the array and one index. Both `peek` and `next` share one guard that throws at the end, so the exhausted behavior is written once.

```java
final class TokenReader {
    private final String[] tokens;
    private int pos;

    TokenReader(String[] tokens) { this.tokens = tokens; }

    boolean hasNext() { return pos < tokens.length; }          // availability, no side effect

    String peek() {
        if (pos == tokens.length) throw new java.util.NoSuchElementException();   // exhausted
        return tokens[pos];                                    // observation, pos unchanged
    }

    String next() {
        String t = peek();      // same guard, same element
        pos++;                  // consumption moves the cursor once
        return t;
    }
}
```

#### The Run Reader

The run reader keeps the pair `run` and `used`. The private method `settle` moves past runs that hold no element, and every public method calls it first.

```java
final class RunReader {
    private final char[] symbols;
    private final long[] counts;
    private int run;
    private long used;

    RunReader(char[] symbols, long[] counts) { this.symbols = symbols; this.counts = counts; }

    private void settle() {
        while (run < counts.length && used == counts[run]) { run++; used = 0; }   // skips used-up and empty runs
    }

    boolean hasNext() { settle(); return run < counts.length; }

    char next() {
        settle();
        if (run == counts.length) throw new java.util.NoSuchElementException();   // exhausted
        used++;                                                                  // one element taken from this run
        return symbols[run];
    }
}
```

#### Cost

- **TokenReader** costs O(1) time per call and O(1) extra space.
- **RunReader** costs O(1) amortized time per call, because each run boundary is passed once, and O(1) extra space.

<!-- stage: applicability -->
### When To Define A Cursor

#### Recognizing The Pattern

Use this method when a class hands out one logical sequence over many calls and the sequence is large, compressed or produced on demand. The words `hasNext`, `next` and `peek` in a problem statement signal it. Before coding, write down the cursor fields, say which method moves them, and decide what the call after the last element does. The invariant to keep is that only the consuming method moves the cursor, and it moves it once.

#### A False Friend

Copying everything into a list is a false friend of an iterator. The copy passes small tests, and it fails when the counts are large or when the source cannot be rewound. A second false friend is a look-ahead that takes an element and puts it back. It works on a list and breaks on a stream.

#### When The Method Does Not Apply

If the caller always reads the whole sequence once and the sequence fits in memory, a plain loop over an array needs no iterator class. If several threads call the iterator at once, one cursor is not enough, and this lesson assumes a single caller.

<!-- stage: exercises -->
### Exercises

#### [Build] Array Iterator (Author exercise)
<!-- id: it37-array-iterator -->

**Prerequisites.** The cursor, availability, consumption and exhaustion definitions from this lesson.

**Problem.** Design the class `ArrayIterator` with a constructor that receives an `int[]`. The method `hasNext()` returns `true` when an element remains. The method `next()` returns the next element and moves past it. The method `remaining()` returns the number of elements not yet returned. The class keeps one cursor and never copies the array.

**Constraints.** The limits are:
- **Length** of the array is from 0 to 10^5, and elements are `int` values.
- **Calls** number at most 10^5 per object.
- **Exhaustion** means `next()` throws `NoSuchElementException` and changes no field.
- **Mutation** of the array by the caller after construction does not happen.

**Example 1.** Input calls `["ArrayIterator","hasNext","next","next","hasNext","next"]` with arguments `[[[4,7]],[],[],[],[],[]]`, output `[null,true,4,7,false,"NoSuchElementException"]`.

**Example 2.** Input calls `["ArrayIterator","hasNext","remaining","hasNext"]` with arguments `[[[]],[],[],[]]`, output `[null,false,0,false]`.

**Hint.** Which single integer identifies the next element, and which method is allowed to change it?

**Changed decision.** Basic case: one cursor, `hasNext` and `remaining` only read it, and `next` checks for exhaustion before it moves.

#### [Vary] Peeking Iterator (LeetCode 284)
<!-- id: it37-peeking-iterator -->

**Prerequisites.** The Array Iterator exercise above. This exercise changes the source: the class wraps any `java.util.Iterator<Integer>`, which cannot move backward.

**Problem.** Design the class `PeekingIterator` with a constructor that receives an `Iterator<Integer>` called the source. The method `peek()` returns the next element and leaves it unread. The method `next()` returns the next element and consumes it. The method `hasNext()` reports whether any element is left. The class calls the source's `next()` only to fill one cached element and never calls it twice for the same element.

**Constraints.** The limits are:
- **Elements** are `Integer` values from -10^9 to 10^9, and 0 is an ordinary value.
- **Calls** number at most 1000 per object.
- **Exhaustion** means `peek()` and `next()` throw `NoSuchElementException` and change no field.
- **Source** may be any iterator, and the class does not read ahead of one element.

**Example 1.** Input calls `["PeekingIterator","next","peek","next","peek","next","hasNext"]` with arguments `[[[1,2,3]],[],[],[],[],[],[]]`, output `[null,1,2,2,3,3,false]`.

**Example 2.** Input calls `["PeekingIterator","peek","peek","next","peek","next","peek"]` with arguments `[[[5,0]],[],[],[],[],[],[]]`, output `[null,5,5,5,0,0,"NoSuchElementException"]`.

**Hint.** Is an `Integer` value of 0 enough to mean that the cache is empty, or does the class need a separate flag?

**Changed decision.** The look-ahead is no longer "take and put back". The class stores one cached element and a flag, and `next()` hands out the cache before it asks the source again.

#### [Boundary] Compressed String Iterator (LeetCode 604)
<!-- id: it37-compressed-string-iterator -->

**Prerequisites.** The Peeking Iterator exercise above. This exercise changes two decisions of LeetCode 604: counts may be zero, and a call after the end throws.

**Problem.** Design the class `StringIterator` with a constructor that receives a compressed string. The string is a sequence of groups, and each group is one letter followed by a decimal count. The logical sequence repeats each letter as many times as its count, in order. The method `next()` returns the next letter. The method `hasNext()` returns `true` when a letter remains. The class never builds the expanded string.

**Constraints.** The limits are:
- **Length** of the compressed string is from 2 to 1000 characters.
- **Letters** are lowercase English letters, and each is followed by 1 to 15 decimal digits.
- **Counts** may be 0 and may exceed `Integer.MAX_VALUE`.
- **Exhaustion** means `next()` throws `NoSuchElementException` and changes no field.

**Example 1.** Input calls `["StringIterator","next","next","next","hasNext"]` with arguments `[["a2b0c13"],[],[],[],[]]`, output `[null,"a","a","c",true]`.

**Example 2.** Input calls `["StringIterator","hasNext","next","hasNext","next"]` with arguments `[["p0q1"],[],[],[],[]]`, output `[null,true,"q",false,"NoSuchElementException"]`.

**Hint.** What type holds a count with 15 digits, and which loop passes a group whose count is 0?

**Changed decision.** Multi-digit and zero counts make a group possibly empty, so the iterator must skip groups lazily inside the call that needs a letter, and `long` replaces `int`.

#### [Recognize] RLE Iterator (LeetCode 900)
<!-- id: it37-rle-iterator -->

**Prerequisites.** The Compressed String Iterator exercise above.

**Problem.** Design the class `RLEIterator` with a constructor that receives an `int[]` called `encoding` of even length. For every even index `i`, `encoding[i]` is a count and `encoding[i + 1]` is the value that repeats that many times. The method `exhaust(n)` consumes the next `n` logical elements and returns the last one consumed. When fewer than `n` elements remain, it consumes all of them and returns -1.

**Constraints.** The limits are:
- **Length** of `encoding` is even and from 2 to 1000.
- **Counts and values** are `int` values from 0 to 10^9.
- **Argument** `n` satisfies `1 <= n <= 10^9`, and calls number at most 1000.
- **Memory** must not depend on the sum of counts, which can reach 5 * 10^11.

**Example 1.** Input calls `["RLEIterator","exhaust","exhaust","exhaust","exhaust"]` with arguments `[[[3,8,0,9,2,5]],[2],[1],[1],[2]]`, output `[null,8,8,5,-1]`.

**Example 2.** Input calls `["RLEIterator","exhaust","exhaust","exhaust"]` with arguments `[[[1,4,2,6]],[1],[2],[1]]`, output `[null,4,6,-1]`.

**Hint.** Which loop moves from run to run, and why can a single call to `exhaust` finish after looking at only some of the runs?

**Changed decision.** Consumption now advances the cursor by a count in one call. The cursor jumps over whole runs by subtraction, and only the run that contains the target element is entered.
