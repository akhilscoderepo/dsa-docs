<!-- lesson-kind: standard -->
<!-- lesson-id: earliest-balance -->
## Find The Longest Balanced Span

<!-- stage: context -->
### Builds With Equal Passes And Failures

A build server records every build of a month as a pass or a fail. A reliability engineer asks for the longest stretch of consecutive builds that holds the same number of passes and failures. That stretch marks the longest period where the pipeline was neither mostly green nor mostly red.

A month holds tens of thousands of builds. The engineer needs the length of the stretch and not the number of stretches. The task is to find the longest such span in a single pass, even though no rule says where a span starts.

<!-- stage: naive -->
### Counting Passes And Failures For Every Pair

The direct method tries every start index. For each start it extends the end and keeps one counter that adds 1 for a pass (the value 1) and subtracts 1 for a fail (the value 0). A counter of 0 means equal numbers, and the method records the length.

```java
static int longestEqual(int[] nums) {
    int best = 0;
    for (int start = 0; start < nums.length; start++) {
        int diff = 0;
        for (int end = start; end < nums.length; end++) {
            diff += nums[end] == 1 ? 1 : -1;
            if (diff == 0) best = Math.max(best, end - start + 1);
        }
    }
    return best;
}
```

For `[0, 0, 1, 0, 0, 0, 1, 1]` the method returns 6. The span from index 2 to index 7 holds three ones and three zeros.

```predict
The array holds 50,000 builds. How many (start, end) pairs does `longestEqual` examine?

It examines 50,000 * 50,001 / 2 = 1,250,025,000 pairs. The loops visit every pair of ends, so the cost is O(n^2).
```

<!-- stage: bottleneck -->
### The Method Cannot Skip Starts

Each start gets its own inner loop, and the loops together visit every pair. The cost is O(n^2), which is more than a billion steps for 50,000 builds. The method also looks for a zero counter from each start, and it does not use what earlier starts already computed.

A frequency map, as in the lesson on counting sums, counts matching pairs. This question asks for the longest span and not the number of spans, so a count of pairs does not answer it. The answer needs the position of the best start for each end, and a position is a different thing to store than a count.

<!-- stage: insight -->
### Remember Where Each Balance First Appeared

A **balance** is a running number that adds 1 for each value 1 and subtracts 1 for each value 0. After `i` values, the balance equals the number of ones minus the number of zeros among them. The balance at the start, before any value, is 0.

#### Equal Balance Means Equal Counts

Two boundaries with an **equal balance** enclose a span with equal counts. If the balance is `x` at boundary `a` and again at boundary `b`, the values between add up to `x - x = 0`. Ones and zeros then cancel, so their counts match. The length of that span is `b - a`.

#### The Earliest Index Gives The Longest Span

For a fixed end, the longest valid span starts at the **earliest index** where the same balance occurred. A later start gives a shorter span, so the program stores only the first index for each balance. It never overwrites an entry, because the first occurrence is the best start for every later end.

The map starts with the balance 0 at index -1. Index -1 stands for the position before the first value. With it, a span that starts at index 0 has a start to match, and its length is `i - (-1) = i + 1`.

<!-- names: balance, equal balance, earliest index -->

#### What The Map Answers

A frequency map answers how many spans exist. The earliest-index map answers how long the longest span is, because each entry is a position and not a count. The loop runs once, with one lookup per value, so the time is O(n) expected and the space is O(n).

<!-- stage: variables -->
### Five Names And Their Roles

The one-pass loop keeps five values.

- **bal** is the running balance after the current value.
- **first** is the map from a balance to the earliest index where it appeared.
- **best** is the length of the longest span found so far.
- **i** is the index of the current value.
- **seen** is `first.get(bal)`, the earliest index with the same balance. The span begins right after that index.

Before the first step, `first` holds only the pair balance 0 at index -1. A lookup that finds a balance gives a span of length `i - first.get(bal)`. A lookup that misses stores the pair `bal` at `i`.

<!-- stage: trace -->
### Two Searches Step By Step

#### A Span In The Middle Of The Array

The input is `[0, 0, 1, 0, 0, 0, 1, 1]`. The balance first reaches -2 at index 1 and returns to -2 at index 3 and at index 7. Each repeat proposes a span. The repeat at index 7 gives the longest proposal, 6, from index 2 through index 7.

```trace
{"cells":[0,0,1,0,0,0,1,1],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"first":"{0@-1}","best":"0"},"note":"The map starts with balance 0 at index -1, the position before the first value."},{"at":{"i":0},"vars":{"bal":"-1","first":"{0@-1, -1@0}","best":"0"},"note":"Balance -1 is new, so the map stores it at index 0."},{"at":{"i":1},"vars":{"bal":"-2","first":"{0@-1, -1@0, -2@1}","best":"0"},"note":"Balance -2 is new, so the map stores it at index 1."},{"at":{"i":2},"vars":{"bal":"-1","first":"{0@-1, -1@0, -2@1}","best":"2"},"note":"Balance -1 appeared at index 0, so the span has length 2-(0) = 2. The best length is 2."},{"at":{"i":3},"vars":{"bal":"-2","first":"{0@-1, -1@0, -2@1}","best":"2"},"note":"Balance -2 appeared at index 1, so the span has length 3-(1) = 2. The best length is 2."},{"at":{"i":4},"vars":{"bal":"-3","first":"{0@-1, -1@0, -2@1, -3@4}","best":"2"},"note":"Balance -3 is new, so the map stores it at index 4."},{"at":{"i":5},"vars":{"bal":"-4","first":"{0@-1, -1@0, -2@1, -3@4, -4@5}","best":"2"},"note":"Balance -4 is new, so the map stores it at index 5."},{"at":{"i":6},"vars":{"bal":"-3","first":"{0@-1, -1@0, -2@1, -3@4, -4@5}","best":"2"},"note":"Balance -3 appeared at index 4, so the span has length 6-(4) = 2. The best length is 2."},{"at":{"i":7},"vars":{"bal":"-2","first":"{0@-1, -1@0, -2@1, -3@4, -4@5}","best":"6"},"note":"Balance -2 appeared at index 1, so the span has length 7-(1) = 6. The best length is 6."}]}
```

#### A Span That Starts At Index Zero

The input is `[1, 0]`, and the map starts as before. After index 0 the balance is 1, which is new. After index 1 the balance is 0, and the map holds 0 at index -1. The span length is `1 - (-1) = 2`, so the whole array qualifies. The check needs the entry at index -1, because no other index holds balance 0.

```trace
{"cells":[1,0],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"first":"{0@-1}","best":"0"},"note":"The map starts with balance 0 at index -1, the position before the first value."},{"at":{"i":0},"vars":{"bal":"1","first":"{0@-1, 1@0}","best":"0"},"note":"Balance 1 is new, so the map stores it at index 0."},{"at":{"i":1},"vars":{"bal":"0","first":"{0@-1, 1@0}","best":"2"},"note":"Balance 0 appeared at index -1, so the span has length 1-(-1) = 2. The best length is 2."}]}
```

<!-- stage: code -->
### The One Pass In Java

```java
static int longestEqual(int[] nums) {
    java.util.HashMap<Integer, Integer> first = new java.util.HashMap<>();
    first.put(0, -1);
    int bal = 0;
    int best = 0;
    for (int i = 0; i < nums.length; i++) {
        bal += nums[i] == 1 ? 1 : -1;
        Integer seen = first.get(bal);
        if (seen == null) first.put(bal, i);
        else best = Math.max(best, i - seen);
    }
    return best;
}
```

The method returns 0 when no span exists, because `best` starts at 0. The balance stays between `-n` and `n`, so an `int` is enough. The `put` runs only for a new balance, so the stored index is always the earliest.

The type of `seen` is `Integer` and not `int`, because `get` returns `null` for a missing key. An unboxing of `null` would throw a `NullPointerException`.

<!-- stage: applicability -->
### When The First Position Is Enough

#### The Invariant

The invariant is that for every balance in the map, the stored index is the smallest index where that balance occurred. At each boundary the loop either stores a new balance or measures against the stored one. The best span ending here is therefore found, and `best` holds the maximum over all ends.

#### The False Friend

A frequency map is the false friend. It looks alike, because both structures use prefix states as keys. The count says how many starts exist and says nothing about which start is the earliest. An exercise that asks for the longest span needs the position, and an exercise that asks for the number of spans needs the count.

#### Conditions That Break The Fit

The condition for a span must reduce to an equal state at two boundaries. A requirement that the ones outnumber the zeros by a margin does not reduce to equality, and it needs another method. The values must also map to a fixed step, such as +1, -1 or 0. A step that depends on the span itself breaks the idea.

<!-- stage: exercises -->
### Exercises

#### [Build] Contiguous Array (LeetCode 525)
<!-- id: ps-contiguous-array-525 -->

**Prerequisites.** The balance and the earliest-index map of this lesson.

**Problem.** Given a binary array `nums`, return the length of the longest contiguous subarray that contains the same number of 0 and 1. Return 0 when no such subarray exists.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are 0 or 1.
- **Empty answer** is 0 when no balanced subarray exists.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [0,0,1,0,0,0,1,1]`, output 6.

**Example 2.** Input `nums = [1,1,1]`, output 0.

**Hint.** Treat each 0 as -1. Which index should the map keep for a balance that appears again?

**Changed decision.** Basic case: the map stores positions and never overwrites, so the answer is a length and not a count.

#### [Vary] Equal A And B (Author exercise)
<!-- id: ps-equal-a-and-b -->

**Prerequisites.** The first exercise above.

**Problem.** Given a string `s` of uppercase letters, return the length of the longest substring in which the letter `A` occurs as many times as the letter `B`. Other letters do not count, and a substring without `A` and `B` is valid.

**Constraints.** The limits are:
- **Length** is `1 <= s.length() <= 10^5`.
- **Characters** are uppercase letters `A` to `Z`.
- **Step** is +1 for `A`, -1 for `B` and 0 for every other letter.
- **Answer** is 0 when no valid substring exists, for example when the string is `"A"`.

**Example 1.** Input `s = "AXBBA"`, output 5.

**Example 2.** Input `s = "AAB"`, output 2.

**Hint.** Letters with step 0 leave the balance unchanged. What happens to the map entry when the balance repeats at the next index?

**Changed decision.** The step has three values, so some positions repeat the previous balance and extend a span for free.

#### [Boundary] Balanced Span With Start (Author exercise)
<!-- id: ps-balanced-start -->

**Prerequisites.** The first exercise and the second trace of this lesson.

**Problem.** Given a binary array `nums`, return the pair `[start, length]` of the longest contiguous subarray with the same number of 0 and 1. When two spans have the same length, return the one with the smaller start. Return `[-1, 0]` when no such subarray exists.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are 0 or 1.
- **Tie** between equal lengths resolves to the smaller start index.
- **Return type** is an `int` array of length 2.

**Example 1.** Input `nums = [1,0,1,1,1]`, output `[0,2]`.

**Example 2.** Input `nums = [1,1,1]`, output `[-1,0]`.

**Hint.** The map holds the balance 0 at index -1. Which expression turns a stored index into the start of the span?

**Changed decision.** The answer reports a position, so the index shift between the stored index and the start decides correctness.

#### [Recognize] Longest Substring With Even Vowel Counts (LeetCode 1371)
<!-- id: ps-even-vowels-1371 -->

**Prerequisites.** All exercises above. The expression `mask ^= 1 << j` flips bit `j` of the integer `mask`, and flipping twice restores the bit.

**Problem.** Given a lowercase string `s`, return the length of the longest substring in which each of the vowels `a`, `e`, `i`, `o` and `u` occurs an even number of times. Zero is even.

**Constraints.** The limits are:
- **Length** is `1 <= s.length() <= 5 * 10^5`.
- **Characters** are lowercase letters `a` to `z`.
- **State** is a 5 bit mask, so there are 32 possible states.
- **Return value** is the length, and a substring without vowels is valid.

**Example 1.** Input `s = "leetcodes"`, output 5.

**Example 2.** Input `s = "xyz"`, output 3.

**Hint.** Let bit `j` record whether vowel `j` has appeared an odd number of times. When do two boundaries have equal masks?

**Changed decision.** The repeated state is a parity mask and not one integer balance, so the map key changes while the earliest-index idea stays.
