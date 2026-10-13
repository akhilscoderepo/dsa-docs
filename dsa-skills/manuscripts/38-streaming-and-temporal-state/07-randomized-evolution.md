<!-- lesson-kind: standard -->
<!-- lesson-id: randomized-evolution -->
## Randomized Evolution

<!-- stage: context -->
### Why A Fair Shuffle Is Not Fair

A published security analysis of an online poker dealer found that its shuffle gave some deck orders a higher chance than others. The routine walked down the deck and swapped each card with a card at a random position anywhere in the deck. The loop looks balanced and runs in linear time. Players who knew which orders were favored could narrow down the hidden cards. A music player shows a quieter version of the same family of bugs. Its "restore order" button returns the list that the shuffle button already rearranged, because both buttons share one array.

Both failures sit in a collection that changes between calls and then returns random output. This lesson treats the collection as correctable. The set of values never grows and never expires, but every call to shuffle overwrites the arrangement, and a reset call restores the original one. The lesson asks two questions. How does a shuffle give every arrangement the same chance, and which copy of the data must stay untouched so that reset is still possible?

<!-- stage: naive -->
### Swapping With Any Position

The direct design walks the array from left to right and swaps position `i` with a random position from the whole array. A second field keeps the array that reset should return. The class below uses an injected `IntUnaryOperator` called `pick` as its source of randomness, so a test can script the draws. A call `pick.applyAsInt(b)` returns an integer from 0 to `b - 1`.

```java
final class NaiveShuffleBox {
    private final int[] original;
    private final int[] array;
    private final java.util.function.IntUnaryOperator pick;

    NaiveShuffleBox(int[] nums, java.util.function.IntUnaryOperator pick) {
        this.original = nums;      // remembers the input
        this.array = nums;         // shuffles the input
        this.pick = pick;
    }

    int[] shuffle() {
        int n = array.length;
        for (int i = 0; i < n; i++) {
            int j = pick.applyAsInt(n);                 // any position from 0 to n - 1
            int t = array[i]; array[i] = array[j]; array[j] = t;
        }
        return array;
    }

    int[] reset() { return original; }
}
```

On random draws the class returns arrays that look shuffled, and a quick visual check passes. For a different approach, a second design lists all `n!` orders and returns one chosen at random. That design is correct, and it is far too large for any array with more than a dozen elements.

```predict
A caller builds NaiveShuffleBox on {1, 2, 3}, calls shuffle() once, and then calls reset(). What does reset() return? Separately, the loop makes 3 draws from 3 values, so it has 27 equally likely draw sequences. Do the six orders of {1, 2, 3} each receive the same number of those sequences?

reset() returns the shuffled order, because the constructor stores the same array object twice and the shuffle rewrote it. The orders do not share the 27 sequences evenly. Three orders each receive 5 sequences and the other three receive 4, so the original order 1, 2, 3 has probability 4/27 and the order 2, 3, 1 has probability 5/27. Six orders cannot split 27 sequences into equal groups.
```

<!-- stage: bottleneck -->
### Counting Draws Against Orders

The loop makes `n` draws of `n` values each, so it has `n^n` equally likely draw sequences, and each sequence produces exactly one order. A fair shuffle needs every one of the `n!` orders to receive the same number of sequences. That needs `n!` to divide `n^n`. For every `n` of 3 or more it does not. The number `n - 1` is at least 2 and divides `n!`. It shares no prime factor with `n`, so it never divides `n^n`. The bias is therefore a property of the counting, not of the random number generator, and a better generator cannot repair it. For `n = 4` the 256 sequences give some orders 8 sequences and others 15, while a fair split would give each order 10.67.

The enumeration design avoids the bias at a price. It builds `n!` orders, so it costs O(n * n!) time and O(n * n!) space. The swap loop costs only O(n) time and O(1) extra space, which is the budget a correct design should keep.

The second weak point is the shared array. The class holds one object under two names, so no later call can recover the input. A correct design needs two properties. The number of draw sequences must factor as `n * (n - 1) * ... * 1`, and the class must keep an array that no shuffle and no caller can touch.

<!-- stage: insight -->
### Shrinking The Choice Each Step

#### The Frontier Splits The Array

<!-- names: frontier, snapshot, uniform -->

The **frontier** is an index `i` that splits the working array into two parts. Positions `0` to `i - 1` hold final values that no later step touches. Positions `i` to `n - 1` hold the values still waiting for a place. Fisher-Yates shuffling moves the frontier from left to right. At each step it draws a position `j` from `i` to `n - 1`, swaps `a[i]` with `a[j]`, and moves the frontier one step right. The draw ranges over `n - i` values, so the first draw has `n` options, the second has `n - 1`, and the last useful draw has 2.

#### Why Every Order Is Equally Likely

The product of the draw sizes is `n * (n - 1) * ... * 2`, and it equals `n!`. Different draw sequences produce different orders. Two sequences that differ first at step `i` place different values at position `i`, and no later step changes that position. So the map from draw sequences to orders is one to one, and both sides have `n!` members. Each order therefore has probability `1 / n!`, and the shuffle is **uniform**, which means every order has the same probability. A short form of the argument: each value is equally likely to land at position `i`, whatever the earlier steps chose.

#### The Snapshot Protects Reset

A **snapshot** is a private copy of the input that the class never hands out and never shuffles. The class makes the snapshot in the constructor, so a later change to the caller's array cannot reach it. Reset copies the snapshot into the working array, and every array returned to a caller is a fresh copy, so a caller who writes into a returned array changes nothing inside the class.

The invariant of the design is that the working array always holds a permutation of the snapshot, the positions left of the frontier are final, and the snapshot never changes.

<!-- stage: variables -->
### State And Draw Ranges

The five names below cover the class fields and the loop locals.

- **snapshot** is the private copy of the input array, written once in the constructor.
- **work** is the working array. It always holds the same multiset of values as `snapshot`.
- **pick** is the injected source of randomness. A call with bound `b` returns an integer from 0 to `b - 1`.
- **i** is the frontier, from 0 to `n - 1`. Positions below `i` are final.
- **j** is the position chosen at step `i`. It equals `i + pick.applyAsInt(n - i)`, so it lies in `[i, n - 1]`.

The array may contain equal values. The argument above counts draw sequences, not distinct-looking arrays, so equal values change how arrays look and never change the counting.

<!-- stage: trace -->
### Tracing Shuffles With Scripted Draws

#### One Shuffle Of Four Letters

The first trace shuffles `K L M N` with scripted draws. The pointer `i` marks the frontier and the pointer `j` marks the chosen position. At `i = 0` the draw has bound 4 and returns 2, so `j = 2` and `K` swaps with `M`. The frontier moves right. At `i = 1` the bound is 3 and the draw returns 0, so `j = 1` and the letter `L` stays in place. A draw may choose the frontier position itself, and that choice is required for fairness. At `i = 2` the bound is 2 and the draw returns 1, so `j = 3` and `K` swaps with `N`. The loop stops because the last position has only one value left. The result is `M L N K`.

```trace
{"cells":["K","L","M","N"],"pointers":["i","j"],"steps":[{"at":{"i":-1,"j":-1},"vars":{"bound":"none","draw":"none","array":"K L M N"},"note":"Start: the array is K L M N and no step has run."},{"at":{"i":0,"j":2},"vars":{"bound":4,"draw":2,"array":"M L K N"},"note":"Bound 4, draw 2, so j is 2 and positions 0 and 2 swap."},{"at":{"i":1,"j":1},"vars":{"bound":3,"draw":0,"array":"M L K N"},"note":"Bound 3, draw 0, so j equals i and L stays at position 1."},{"at":{"i":2,"j":3},"vars":{"bound":2,"draw":1,"array":"M L N K"},"note":"Bound 2, draw 1, so j is 3 and positions 2 and 3 swap."},{"at":{"i":3,"j":3},"vars":{"bound":1,"draw":"none","array":"M L N K"},"note":"The frontier reaches position 3. One value is left, so no draw is needed and the result is M L N K."}]}
```

#### Reset, Then Shuffle Again

The second trace uses a class built on `7 2 9 2` with a repeated value. The first shuffle runs three steps with scripted draws and leaves the working array in a new order, while the snapshot stays `7 2 9 2`. The reset step copies the snapshot back into the working array. A second shuffle with different draws then gives a different order. The variables column shows the snapshot, and it has the same value in every step. The pointer `j` equals `i` in the steps where the draw keeps the frontier value in place.

```trace
{"cells":["7","2","9","2"],"pointers":["i","j"],"steps":[{"at":{"i":-1,"j":-1},"vars":{"snapshot":"7 2 9 2","array":"7 2 9 2","call":"new"},"note":"The constructor copies the input twice. Snapshot and working array both read 7 2 9 2."},{"at":{"i":0,"j":2},"vars":{"snapshot":"7 2 9 2","array":"9 2 7 2","call":"shuffle()"},"note":"Draw 2 from bound 4 gives j = 2, so positions 0 and 2 swap."},{"at":{"i":1,"j":1},"vars":{"snapshot":"7 2 9 2","array":"9 2 7 2","call":"shuffle()"},"note":"Draw 0 from bound 3 gives j = 1, so the value stays at position 1."},{"at":{"i":2,"j":3},"vars":{"snapshot":"7 2 9 2","array":"9 2 2 7","call":"shuffle()"},"note":"Draw 1 from bound 2 gives j = 3, so positions 2 and 3 swap."},{"at":{"i":-1,"j":-1},"vars":{"snapshot":"7 2 9 2","array":"7 2 9 2","call":"reset()"},"note":"reset copies the snapshot into the working array. The snapshot never changed, so the array reads 7 2 9 2 again."},{"at":{"i":0,"j":3},"vars":{"snapshot":"7 2 9 2","array":"2 2 9 7","call":"shuffle()"},"note":"Draw 3 from bound 4 gives j = 3, so positions 0 and 3 swap."},{"at":{"i":1,"j":3},"vars":{"snapshot":"7 2 9 2","array":"2 7 9 2","call":"shuffle()"},"note":"Draw 2 from bound 3 gives j = 3, so positions 1 and 3 swap."},{"at":{"i":2,"j":2},"vars":{"snapshot":"7 2 9 2","array":"2 7 9 2","call":"shuffle()"},"note":"Draw 0 from bound 2 gives j = 2, so the value stays at position 2."}]}
```

<!-- stage: code -->
### Shuffler With Private Snapshot

#### The Class

The class copies the input twice in its constructor, once for the snapshot and once for the working array. The method `permute` is the Fisher-Yates loop. The public methods return copies.

```java
final class Shuffler {
    private final int[] snapshot;
    private final int[] work;
    private final java.util.function.IntUnaryOperator pick;

    Shuffler(int[] nums, java.util.function.IntUnaryOperator pick) {
        this.snapshot = nums.clone();   // private copy: the caller's later writes cannot reach it
        this.work = nums.clone();       // second copy: shuffles never touch the snapshot
        this.pick = pick;
    }

    private void permute() {
        int n = work.length;
        for (int i = 0; i + 1 < n; i++) {          // frontier i: the last position needs no draw
            int j = i + pick.applyAsInt(n - i);    // uniform position in [i, n - 1]
            int t = work[i]; work[i] = work[j]; work[j] = t;
        }
    }

    int[] shuffle() { permute(); return work.clone(); }              // fresh copy for the caller

    int[] reset() {
        System.arraycopy(snapshot, 0, work, 0, work.length);        // restore without sharing
        return work.clone();
    }
}
```

#### Production Use

In production code the caller passes a `java.util.Random` method reference, for example `new Shuffler(nums, new java.util.Random()::nextInt)`. The call `nextInt(bound)` returns a value from 0 to `bound - 1` without the bias of a remainder operation. Tests pass a scripted source, so a test can drive the loop through every draw sequence.

#### Cost

- **shuffle** costs O(n) time for the loop and O(n) space for the returned copy.
- **reset** costs O(n) time and O(n) space for the same reasons.
- **Constructor** costs O(n) time and O(n) space for the two copies.

<!-- stage: applicability -->
### When Fair Shuffling Applies

#### Recognizing The Pattern

Use this method when public calls change a collection and later return random output. The words "shuffle", "random order" and "reset" in a statement signal it. Before coding, decide which copy must stay fixed and what the draw ranges are at each step. The invariant to keep is that each valid arrangement has probability `1 / n!` under the current state, the snapshot never changes, and every returned array is a copy.

#### False Friends

A swap with a random position from the whole array is a false friend of Fisher-Yates, because the two loops differ by a single bound, `n` versus `n - i`, and only one is fair. A sort with a random comparator is a second false friend. Its result depends on the sorting algorithm, and a comparator that contradicts itself breaks the sort contract. For sampling a single item from a stream whose length is unknown, shuffling is also the wrong tool. Chapter 35 covers reservoir sampling, which keeps one item and proves that each of `t` items seen so far is held with probability `1 / t`.

#### When The Method Does Not Apply

If the output must resist an adversary, as in a card game with money at stake, `java.util.Random` is a no-go. Its internal state has only 48 bits, and an observer who sees a few outputs can predict the rest. Use `java.security.SecureRandom` as the source. If the requested distribution is not uniform, for example weighted choices without repeats, the counting argument above no longer holds and the method needs a different proof.

<!-- stage: exercises -->
### Exercises

#### [Build] Fisher-Yates One Step (Author exercise)
<!-- id: st38-fisher-yates-step -->

**Prerequisites.** The frontier and the draw range from this lesson.

**Problem.** Write the method `int step(int[] a, int i, IntUnaryOperator pick)`. The method performs one Fisher-Yates step at frontier `i`. It calls `pick.applyAsInt(a.length - i)` exactly once and treats the result `k` as an offset. It swaps `a[i]` with `a[i + k]` in place and returns the value now stored at `a[i]`.

**Constraints.** The limits are:
- **Length** of `a` is from 1 to 10^5, and elements are `int` values.
- **Frontier** `i` satisfies `0 <= i < a.length`.
- **Draw** `k` lies from 0 to `a.length - i - 1`, and a draw outside that range throws `IllegalStateException` before any write.
- **Mutation** touches only positions `i` and `i + k`.

**Example 1.** Input `a = [4, 7, 9]`, `i = 1`, draw bound 2 with scripted result 1, output `9`, and `a` becomes `[4, 9, 7]`.

**Example 2.** Input `a = [5, 5, 2]`, `i = 0`, draw bound 3 with scripted result 2, output `2`, and `a` becomes `[2, 5, 5]`.

**Hint.** What must the argument to `pick` be so that the chosen position can equal `i` itself?

**Changed decision.** Basic case: the draw range shrinks to the unplaced suffix, and the position under the frontier may swap with itself.

#### [Vary] Shuffle An Array (LeetCode 384)
<!-- id: st38-shuffle-array -->

**Prerequisites.** The Fisher-Yates One Step exercise above. This exercise repeats the step over the whole array and adds a restore call.

**Problem.** Design the class `ShuffleBox` with a constructor that receives an `int[] nums` and an `IntUnaryOperator pick`. The method `shuffle()` returns a new array that holds the elements of `nums` in an order chosen so that every arrangement of the elements has the same probability. The method `reset()` returns a new array equal to `nums` as it was at construction time.

**Constraints.** The limits are:
- **Length** of `nums` is from 0 to 50, and elements are `int` values that may repeat.
- **Calls** number at most 10^4 per object.
- **Draws** come only from `pick`, and one `shuffle()` calls it once per frontier from 0 to `n - 2`.
- **Isolation** means a write into a returned array never changes later results.

**Example 1.** Input `nums = [3, 1, 2]` with scripted draws `2, 0` for `shuffle()`, output `[2, 1, 3]`, and then `reset()` outputs `[3, 1, 2]`.

**Example 2.** Input `nums = [8, 8, 5, 0]` with scripted draws `1, 2, 0` for `shuffle()`, output `[8, 0, 5, 8]`, and then `reset()` outputs `[8, 8, 5, 0]`.

**Hint.** Which array does each call start from, and which of the arrays that the class holds may the call write into?

**Changed decision.** The single step becomes a loop over a moving frontier. The class also keeps a private snapshot, so no shuffle writes into it and reset can run at any time.

#### [Boundary] Repeated Reset And Shuffle (Author exercise)
<!-- id: st38-reset-shuffle-cycles -->

**Prerequisites.** The Shuffle An Array exercise above. This exercise changes one decision: the class adds `current()` and copies on every read and write, so callers never touch the working array.

**Problem.** Design the class `Deck` with a constructor that receives an `int[] initial` and an `IntUnaryOperator pick`. The method `shuffle()` applies one Fisher-Yates pass to the current order and returns a copy of the new order. The method `current()` returns a copy of the current order. The method `reset()` sets the current order to the initial order and returns a copy of it. The initial order is the content of `initial` at construction time.

**Constraints.** The limits are:
- **Length** of `initial` is from 0 to 1000, and elements are `int` values that may repeat.
- **Calls** number at most 10^4 per object.
- **Aliasing** means a write by the caller into `initial` after construction, or into any returned array, never changes the object.
- **Draws** use `pick` once per frontier from 0 to `n - 2`, so lengths 0 and 1 use none.

**Example 1.** Input `initial = [1, 2, 3]`. The call `shuffle()` with draws `1, 1` outputs `[2, 3, 1]`. The caller writes 99 into that array, and `current()` outputs `[2, 3, 1]`. Then `reset()` outputs `[1, 2, 3]`, and `shuffle()` with draws `2, 1` outputs `[3, 1, 2]`.

**Example 2.** Input `initial = [4, 4]`. The caller sets `initial[0] = 9` after construction, and `reset()` outputs `[4, 4]`. For `initial = [6]`, `shuffle()` outputs `[6]` and calls `pick` zero times.

**Hint.** How many separate arrays does the class need, and which of them does the caller ever receive?

**Changed decision.** The new decision is `current()` plus copy-on-read, which means copy in and copy out. The class copies `initial` at construction and copies every array it returns. It keeps the initial order apart from the working order.

#### [Recognize] Streaming Sample Review (Author exercise)
<!-- id: st38-streaming-sample-review -->

**Prerequisites.** The Repeated Reset And Shuffle exercise above. This exercise changes the kind of state: values arrive one at a time and the set grows, so there is no array to shuffle.

**Problem.** Design the class `StreamPicker` with a constructor that receives a `LongUnaryOperator pick`. The method `add(int value)` records the next value of the stream. The method `pick()` returns one of the values added so far, chosen so that each added value has the same probability. The class stores a constant number of values and never keeps the whole stream. Each call to `add` calls `pick.applyAsLong(t)` once, where `t` is the number of values added so far including the new one, and a result of 0 replaces the stored value with the new value.

**Constraints.** The limits are:
- **Stream** length is from 0 to 10^12 values, so the counter and the draw bound use `long`.
- **Values** are `int` values that may repeat.
- **Empty** stream means `pick()` throws `NoSuchElementException`.
- **Memory** is O(1) and does not depend on the number of values added.

**Example 1.** Input calls `add(5)`, `add(8)`, `add(3)`, `pick()` with scripted draws `0, 1, 0` for the three `add` calls, output `3`.

**Example 2.** Input calls `pick()` on a new object, output `NoSuchElementException`. Then `add(7)` with scripted draw `0` and `pick()` output `7`.

**Hint.** What is the probability that the newest of `t` values replaces the stored one, and what must it be for the newest value to be held with probability `1 / t`?

**Changed decision.** The represented set grows instead of being rearranged. The class keeps one held value and a count, and the draw bound grows with the count.
