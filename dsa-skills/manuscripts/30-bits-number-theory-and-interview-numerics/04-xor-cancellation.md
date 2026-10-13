<!-- lesson-kind: standard -->
<!-- lesson-id: xor-cancellation -->
## XOR Cancellation

<!-- stage: context -->
### Why One Lost Record Is Hard

A payment service writes one log line when a charge starts and one when it finishes. Both lines carry the same charge id. After a crash, the log holds 2,000,001 lines. Every id appears twice except one, and that id marks the charge that never finished. Support needs that single id, and the log is too large to read by hand.

The ids arrive in no particular order, and a repeated id can sit millions of lines away from its partner. The program must find the id that has no partner without remembering every id it has seen. Lesson 4 asks how a program can match equal values in one pass while using almost no memory.

<!-- stage: naive -->
### Remember Every Id In A Set

The direct approach keeps a set of ids that are still waiting for a partner. A first sighting adds the id, and a second sighting removes it. When the pass ends, the one id left in the set is the answer.

```java
static int singleBySet(int[] ids) {
    java.util.HashSet<Integer> waiting = new java.util.HashSet<>();
    for (int id : ids) {
        if (!waiting.remove(id)) {      // remove returns false when the id was not waiting
            waiting.add(id);            // a first sighting waits for its partner
        }
    }
    return waiting.iterator().next();   // exactly one id has no partner
}
```

The method reads each id once and never sorts. It is correct whenever every id except one appears exactly twice.

```predict
The log holds 2,000,001 lines. In the worst order of lines, how large does the set grow while the pass runs?

The set can grow to about one million ids. If all first sightings come before any second sighting, then each of the 1,000,000 pairs has put its id into the set, and none has been removed yet. The extra memory grows in proportion to the number of lines.
```

<!-- stage: bottleneck -->
### The Set Needs O(n) Extra Memory

#### Count The Memory

In the worst case the set holds half of all ids at once. That is O(n) extra space for `n` lines. Each boxed `Integer` entry in a `HashSet` also costs tens of bytes, so a million waiting ids take tens of megabytes. A service that scans logs on a small machine cannot afford this for every file.

#### Compare The Other Direction

Sorting the ids first needs no set, because equal ids become neighbors. Sorting costs O(n log n) time, and it rewrites the array or needs a copy of it. Both options solve a problem that is smaller than they assume. The program does not need to know which ids it has seen. It only needs a value that forgets an id as soon as the id appears a second time. A single running integer would be enough if combining a value with itself erased it.

<!-- stage: insight -->
### Combine With Exclusive Or To Erase Pairs

#### Define The Operation

The **exclusive or** of two integers, written `a ^ b` in Java, compares them bit by bit. A result bit is 1 when exactly one input bit is 1, and it is 0 when the two input bits are equal. The truth table has four rows: `0^0 = 0`, `0^1 = 1`, `1^0 = 1` and `1^1 = 0`. The operation needs no carry, so every bit position is independent of the others.

#### Use Three Laws

Three laws follow directly from the truth table. The first is `a ^ a = 0`, since every bit is compared with itself. The second is `a ^ 0 = a`, because a 0 bit never changes the other bit. The third is that `^` is commutative and associative, so the order and grouping of a long chain do not matter. Together they say that combining a value with itself **cancels** it, and cancelling a value leaves the rest of the chain untouched.

<!-- names: exclusive or, cancel, split bit -->

#### Fold The Whole Array

Start with `acc = 0` and compute `acc ^= v` for every element `v`. Because order does not matter, the chain equals the pairs combined first and the single value last. Each pair gives 0, and the zeros vanish by the second law. The final `acc` is the single value. The invariant is that `acc` equals the exclusive or of the elements read so far, which is the exclusive or of the single values among them. The memory is one integer.

#### Reuse The Law For Indexes

The same law finds a missing value. Combine every array element with every index that should be present. A value that appears in both groups cancels. The one value that appears in only one group survives. When the unpaired values are `p` and `q`, the fold gives `p ^ q`, which is nonzero because `p` and `q` differ. Any set bit of `p ^ q` is a **split bit**: one of `p` and `q` has it and the other does not. Folding the elements with that bit set, and then the elements without it, recovers `p` and `q` separately.

Take the unpaired values 4 and 9, with the pairs 6 and 2 also in the array. In binary, 4 is `0100` and 9 is `1001`, so `p ^ q` is `1101`, which is 13. The lowest set bit of 13 is bit 0. Of the two unpaired values, only 9 has that bit set. Each pair has two equal values, so both copies fall in the same group and cancel. Folding the elements with bit 0 set gives 9, and `13 ^ 9` gives 4.

<!-- stage: variables -->
### Quantities To Track In The Fold

Track these items while folding.

- **acc** is the running `int` that starts at 0 and absorbs each value with `^=`.
- **v** is the current array element, read once.
- **i** is the zero-based index that the index trick combines with the element.
- **diff** is the exclusive or of the unpaired values `p` and `q`.
- **split** is a value with one bit of `diff` set, taken as `diff & -diff`.

The fold has no conditions on sign. An `int` is a 32-bit pattern, and the operator `^` acts on all 32 bits, including the sign bit. A negative value cancels with itself exactly as a positive one does. The value 0 is a valid single value, and the fold returns 0 for it just as it returns any other result.

<!-- stage: trace -->
### Follow The Fold And The Index Trick

#### Fold Five Ids

Take the ids `4, 1, 2, 1, 2`. The accumulator starts at 0. After the first id it holds 4, which is `100` in binary. The second id 1 sets bit 0 and gives 5. The third id 2 sets bit 1 and gives 7. The fourth id 1 clears bit 0 again, so `acc` becomes 6. The fifth id 2 clears bit 1, so `acc` is 4. The ids 1 and 2 each appeared twice and are gone. Only the id 4 remains.

```trace
{"cells":[4,1,2,1,2],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"acc":0},"note":"The accumulator starts at 0, the identity for the exclusive or."},{"at":{"i":0},"vars":{"acc":4,"binary":"100"},"note":"The id 4 is read for the first time, so it enters the accumulator. The accumulator is 4."},{"at":{"i":1},"vars":{"acc":5,"binary":"101"},"note":"The id 1 is read for the first time, so it enters the accumulator. The accumulator is 5."},{"at":{"i":2},"vars":{"acc":7,"binary":"111"},"note":"The id 2 is read for the first time, so it enters the accumulator. The accumulator is 7."},{"at":{"i":3},"vars":{"acc":6,"binary":"110"},"note":"The id 1 is read a second time, so it cancels its first copy. The accumulator is 6."},{"at":{"i":4},"vars":{"acc":4,"binary":"100"},"note":"The id 2 is read a second time, so it cancels its first copy. The accumulator is 4."}]}
```

#### Find The Missing Value In 0 To 4

The array `3, 0, 4, 1` holds four of the five numbers from 0 to 4. The accumulator starts at `n = 4`, the one number that has no index. At each position `i` the loop combines the index and the element. By the end, each of the numbers 0, 1, 3 and 4 has entered twice and the number 2 has entered once.

```trace
{"cells":[3,0,4,1],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"acc":4},"note":"The accumulator starts at n = 4, the number that has no index."},{"at":{"i":0},"vars":{"acc":7},"note":"The step combines the index 0 and the element 3. The accumulator is 7."},{"at":{"i":1},"vars":{"acc":6},"note":"The step combines the index 1 and the element 0. The accumulator is 6."},{"at":{"i":2},"vars":{"acc":0},"note":"The step combines the index 2 and the element 4. The accumulator is 0."},{"at":{"i":3},"vars":{"acc":2},"note":"The step combines the index 3 and the element 1. The accumulator is 2. The loop ends with the missing number 2."}]}
```

The hardest step is the third one. Before it, `acc` is 6, which equals `4 ^ 3 ^ 1`. The step combines the index 2 and the element 4. The element 4 removes the 4 that `acc` already holds, and the index 2 adds a 2. What remains is `3 ^ 1 ^ 2`, which is 0. That zero comes from the particular values, because `3 ^ 1` happens to equal 2. It does not show that the answer is found. The last step combines the index 3 and the element 1, which removes the 3 and the 1 and leaves 2. The number 2 is not an element, so it is the only number left in the accumulator.

<!-- stage: code -->
### Implement The Fold And Split

```java
static int singleNumber(int[] nums) {
    int acc = 0;                          // 0 is the identity, so the first value passes through
    for (int v : nums) {
        acc ^= v;                         // a value that repeats erases itself from acc
    }
    return acc;                           // only the unpaired value survives
}

static int missingWithOffset(int[] a, int lo) {
    int acc = lo + a.length;              // the top of the range has no matching index
    for (int i = 0; i < a.length; i++) {
        acc ^= (lo + i) ^ a[i];           // index value and element value cancel when both exist
    }
    return acc;
}

static int[] twoSingles(int[] nums) {
    int diff = 0;
    for (int v : nums) diff ^= v;         // diff equals p ^ q, which is nonzero
    int split = diff & -diff;             // one bit where p and q differ
    int p = 0;
    for (int v : nums) {
        if ((v & split) != 0) p ^= v;     // the group with the split bit set holds p only
    }
    int q = diff ^ p;                     // q is the exclusive or of diff and p
    return new int[]{Math.min(p, q), Math.max(p, q)}; // the smaller value comes first
}
```

The first method does one pass and keeps one integer. The second method needs the range start `lo` because the index values must match the element values. The third method makes two passes. The parentheses in `(v & split) != 0` make the AND run before the comparison.

<!-- stage: applicability -->
### When Exclusive Or Applies

#### Recognize The Cue

Use this method when equal values pair off and one or two of them do not, or when two collections should hold the same values except for one difference. The invariant to check is that every value outside the answer reaches the accumulator an even number of times. The method also works for any odd count in place of one, because an odd number of copies leaves one copy. Parity is the whole story, and the exact count never matters.

#### Name The False Friend

Addition is a false friend for the missing-value task. The sum of `0..n` minus the sum of the array also gives the missing value. Java `int` arithmetic wraps around modulo 2^32, so the difference is still the right missing value even when the sums overflow. The real differences are elsewhere. The exclusive or needs no wide type and no reasoning about overflow, because each bit stays in its own position. A sum also fails for the task with two unpaired values, because one total cannot recover two unknown numbers. Addition is the right choice when the task needs a total and not a cancellation.

#### Check The Preconditions

The fold gives a wrong answer when the input breaks its promise. If two values are unpaired, the fold returns their combination and not either value. If a value appears three times in a list that also pairs others, the extra copy survives, which is correct for odd counts and wrong for a "pairs only" promise. Confirm the pairing guarantee before relying on the result.

<!-- stage: exercises -->
### Exercises

#### [Build] Single Number (LeetCode 136)
<!-- id: bt04-single-number -->

**Prerequisites.** The fold with `^` from this lesson.

**Problem.** Given a non-empty array `nums` of integers, every element appears exactly twice except for one element that appears exactly once. Return the element that appears once.

**Constraints.** The limits are:
- **Length** of `nums` is an `int` with `1 <= n <= 3 * 10^4`, and `n` is odd.
- **Values** are `int` values, and negative values are allowed.
- **Guarantee** is that exactly one value appears once.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [9,-3,7,9,7]`, output -3, because the pairs of 9 and of 7 cancel.

**Example 2.** Input `nums = [42]`, output 42, since a single element has no pair to cancel.

**Hint.** What is `v ^ v`, and what is `v ^ 0`?

**Changed decision.** Baseline case: every pair cancels, and one value remains.

#### [Vary] Missing Value By XOR (Author exercise)
<!-- id: bt04-missing-offset -->

**Prerequisites.** The first exercise above.

**Problem.** Given an integer `lo` and an array `a` of `n` distinct integers that all lie in the range `lo` to `lo + n`, both included, return the one number in that range that does not appear in `a`. Combine values and indexes with the exclusive or.

**Constraints.** The limits are:
- **`n`** is an `int` with `0 <= n <= 10^5`.
- **`lo`** is an `int` with `-10^9 <= lo <= 10^9`.
- **Values** in `a` are distinct and lie in `lo` to `lo + n`.
- **Return** is an `int`, and the order of `a` is arbitrary.

**Example 1.** Input `lo = 5` and `a = [7,5,8,6]`, output 9, because the range 5 to 9 lacks its top value.

**Example 2.** Input `lo = -2` and `a = [-2,0,2,1]`, output -1, because the range -2 to 2 lacks a negative value in the middle.

**Hint.** Which number in the range has no index of its own, and what do you combine with each element?

**Changed decision.** The range starts at `lo`, so the index values are `lo + i` and not `i`.

#### [Boundary] Zero And Negative Values (Author exercise)
<!-- id: bt04-odd-count-signed -->

**Prerequisites.** The first two exercises above.

**Problem.** Given a non-empty array `nums` of integers, exactly one value appears an odd number of times, and every other value appears an even number of times. Return that value.

**Constraints.** The limits are:
- **Length** of `nums` is an `int` with `1 <= n <= 10^5`.
- **Values** are any `int`, including 0, negative numbers and `Integer.MIN_VALUE`.
- **Guarantee** is that exactly one value has an odd count.
- **Return** is an `int`, and 0 is a possible answer.

**Example 1.** Input `nums = [0,0,0]`, output 0, because 0 has an odd count of 3 and is a valid answer.

**Example 2.** Input `nums = [-5,3,-5,3,-5]`, output -5, because -5 appears three times and 3 appears twice.

**Hint.** Does the sign bit behave differently from the other 31 bits under `^`?

**Changed decision.** The odd count may be 3 or more, and the answer may be 0 or negative.

#### [Recognize] Single Number III (LeetCode 260)
<!-- id: bt04-two-singles -->

**Prerequisites.** The first three exercises above.

**Problem.** Given an array `nums` of integers in which exactly two distinct integers `p` and `q` appear once and every other integer appears exactly twice, return `p` and `q` as an array of length 2. The smaller value comes first in the result.

**Constraints.** The limits are:
- **Length** of `nums` is an `int` with `2 <= n <= 3 * 10^4`.
- **Values** are `int` values, and negative values are allowed.
- **Guarantee** is that `p` and `q` differ and appear once.
- **Return** is an `int[]` of length 2, in ascending order.

**Example 1.** Input `nums = [6,2,9,6,4,2]`, output [4,9], because 4 and 9 appear once and the pairs 6 and 2 cancel.

**Example 2.** Input `nums = [-1,5,-1,0]`, output [0,5], because the single values are 0 and 5 and the pair -1 cancels.

**Hint.** The fold gives `p ^ q`. Which bit tells `p` from `q`?

**Changed decision.** Two unpaired integers survive, so one fold is not enough and the array is split by one bit.
