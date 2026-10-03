<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-size-aggregate-windows -->
## Fixed-Size Aggregate Windows

<!-- stage: context -->
### A Seaside Kiosk Counting Cones

An ice cream kiosk on a seaside pier writes down how many cones it sold on each day of the season. The owner wants a small chalkboard that reports the total for every run of four consecutive days, because her supplier restocks on a four-day cycle and she wants to see which cycle was the busiest. The season has about ninety days, and the numbers can be large on holiday weekends.

She has a notebook with one number per line and a pocket calculator. For the first run she adds the first four numbers. For the second run she is tempted to start over, flip back to the second line, and add four numbers again. It works, but she notices that most of the numbers in the second run are the same ones she added a minute ago.

<!-- stage: naive -->
### Add Four Numbers From Scratch Each Time

The direct plan is to treat every starting day as a fresh job: walk over the next four days and add them up.

```java
static long[] totalsByRecount(int[] sold, int k) {
    long[] totals = new long[sold.length - k + 1];
    for (int start = 0; start + k <= sold.length; start++) {
        long sum = 0;
        for (int day = start; day < start + k; day++) {
            sum += sold[day];
        }
        totals[start] = sum;
    }
    return totals;
}
```

It is easy to trust. It assumes `1 <= k <= sold.length`, and it accumulates in a `long`, so a long season of big numbers cannot wrap around the way an `int` total could.

<!-- stage: bottleneck -->
### Every Total Re-Reads Old Numbers

There are n - k + 1 runs, and each one reads k numbers, so the whole job reads about k times (n - k + 1) numbers. For a block of size k near half of n this is O(n * k), which is quadratic in the worst case. With ninety days and a block of four it feels instant, but with a million sensor readings and a block of a hundred thousand it would not finish.

The waste is easy to see in the notebook. Two neighbouring runs share k - 1 of their k numbers, and the second run differs from the first only at its two ends: one day fell off the left side and one new day appeared on the right. Re-adding the shared middle recomputes something the previous answer already contains. A method that carries the previous total forward and repairs it at the two ends would read each number a constant number of times, which gives O(n) overall regardless of k.

<!-- stage: insight -->
### Carry The Total And Fix Two Ends

Think of the four consecutive days as a frame laid over the notebook, and of moving the frame one day to the right. Each step of that move has exactly two effects on the contents: the **entering value** joins at the right edge, and the **leaving value** is dropped from the left edge. Nothing in the middle changes. So if the total of the old contents is known, the total of the new contents is the old one plus the entering value minus the leaving value, and that costs two reads instead of k.

The state we carry is therefore a **running total**, and the invariant is a precise statement about it: before a result is recorded, the running total equals the sum of the values at positions `left` through `right`, and `right - left + 1` equals k. The loop has three jobs in a fixed order. Add the entering value, subtract the leaving value once the frame has grown past k, and record the total once the frame is exactly k wide.

The same pattern covers any quantity that can be repaired with one add and one remove: a sum, a count of items with some property, a sum of squares. A count is just a sum in which each element contributes zero or one, so the entering and leaving values become small decisions rather than raw numbers. Averages need no new idea either, because every block has the same length k, so comparing averages is the same as comparing sums, and one division at the very end is enough.

<!-- names: entering value, leaving value, running total -->

<!-- stage: variables -->
### Frame Edges And The Total

`right` is the position being added and walks over the whole array once. `left` is `right - k + 1`, the oldest position still inside the frame, and it does not need its own variable in the code, although drawing it helps. `total` is the running total and must be a `long` whenever values or block sizes can push an int past about two billion. `best` is the best total seen so far for the maximum questions, and it must start at the first full block rather than at zero, because a season of losses would otherwise report a zero that no block produced.

<!-- stage: trace -->
### Two Passes With Different Shapes

The first trace uses daily sales 4, 2, -1, 6, 3, 5, 1 and blocks of three days. The first full block is built by adding three values, and from then on every step adds one value and subtracts one. The step to study is the second one, where the day with value 4 leaves and the day with value 6 enters, and the total moves from 5 to 7 without looking at the middle two days.

```trace
{"cells":[4,2,-1,6,3,5,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":2},"vars":{"total":5,"best":5},"note":"Build the first block by adding 3 values: the total is 5, and it is the best so far."},{"at":{"left":1,"right":3},"vars":{"total":7,"best":7},"note":"The value 4 leaves and the value 6 enters, so the total becomes 7. The best total so far is 7."},{"at":{"left":2,"right":4},"vars":{"total":8,"best":8},"note":"The value 2 leaves and the value 3 enters, so the total becomes 8. The best total so far is 8."},{"at":{"left":3,"right":5},"vars":{"total":14,"best":14},"note":"The value -1 leaves and the value 5 enters, so the total becomes 14. The best total so far is 14."},{"at":{"left":4,"right":6},"vars":{"total":9,"best":14},"note":"The value 6 leaves and the value 1 enters, so the total becomes 9. The best total so far is 14."}]}
```

The second trace is a count rather than a sum. The letters of "sequoiaxyz" contribute one when they are vowels and zero otherwise, and the block is four letters long. Look closely at the step where the total drops, because a vowel leaves and a consonant enters. Notice that the same bookkeeping holds, only the contribution of each element changed, and that the best block is found at the fourth start with a count of four.

```trace
{"cells":["s","e","q","u","o","i","a","x","y","z"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":3},"vars":{"vowels":2,"best":2},"note":"Count the vowels among the first 4 letters: 2, which is the best so far."},{"at":{"left":1,"right":4},"vars":{"vowels":3,"best":3},"note":"s leaves (a consonant) and o enters (a vowel), so the count is 3. The best count so far is 3."},{"at":{"left":2,"right":5},"vars":{"vowels":3,"best":3},"note":"e leaves (a vowel) and i enters (a vowel), so the count is 3. The best count so far is 3."},{"at":{"left":3,"right":6},"vars":{"vowels":4,"best":4},"note":"q leaves (a consonant) and a enters (a vowel), so the count is 4. The best count so far is 4."},{"at":{"left":4,"right":7},"vars":{"vowels":3,"best":4},"note":"u leaves (a vowel) and x enters (a consonant), so the count is 3. The best count so far is 4."},{"at":{"left":5,"right":8},"vars":{"vowels":2,"best":4},"note":"o leaves (a vowel) and y enters (a consonant), so the count is 2. The best count so far is 4."},{"at":{"left":6,"right":9},"vars":{"vowels":1,"best":4},"note":"i leaves (a vowel) and z enters (a consonant), so the count is 1. The best count so far is 4."}]}
```

<!-- stage: code -->
### Totals, Maximum And Vowel Count

```java
static long[] blockTotals(int[] a, int k) {
    long[] out = new long[a.length - k + 1];
    long total = 0;
    for (int right = 0; right < a.length; right++) {
        total += a[right];
        if (right >= k) total -= a[right - k];
        if (right >= k - 1) out[right - k + 1] = total;
    }
    return out;
}

static double highestAverage(int[] a, int k) {
    long total = 0;
    for (int i = 0; i < k; i++) total += a[i];
    long best = total;
    for (int right = k; right < a.length; right++) {
        total += a[right];
        total -= a[right - k];
        best = Math.max(best, total);
    }
    return (double) best / k;
}

static int mostVowels(String s, int k) {
    int count = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        if ("aeiou".indexOf(s.charAt(right)) >= 0) count++;
        if (right >= k && "aeiou".indexOf(s.charAt(right - k)) >= 0) count--;
        if (right >= k - 1) best = Math.max(best, count);
    }
    return best;
}
```

Every element is read at most twice, once on entry and once on exit, so time is O(n) and extra space is O(1) apart from the output array. `highestAverage` fills the first block in its own loop and divides only after the scan, and it adds and subtracts in two separate statements, because the expression `a[right] - a[right - k]` would be computed in `int` first and could wrap around before it reached the `long` total.

<!-- stage: applicability -->
### When Blocks Have One Fixed Length

Reach for a fixed frame when the question mentions every block of exactly k consecutive items and the answer for a block can be repaired from its neighbour by removing one contribution and adding one. State the invariant out loud before coding: the maintained value equals the contents of positions `left` to `right`, and that range has length k. Every off-by-one in this lesson comes from letting that sentence become untrue for a moment before the result is recorded.

A false friend is the prefix sum. If many unrelated range queries arrive after one preparation pass, prefix sums answer each in constant time and a moving frame would redo the work for every query. The frame wins when there is a single left-to-right pass and the blocks are tied to one fixed length. Another false friend is a block length that changes, which breaks the one-in one-out repair and needs the variable-size methods later in this chapter.

In Java, decide what happens when k is zero, negative or larger than the array, because the loops above would allocate a negative array or read out of range. Choose between a clear exception and a documented empty result, and test the choice on `k == n`. Keep totals in `long`, divide for an average once at the end, and use `Math.max` against a `best` seeded from a real block.

<!-- stage: exercises -->
### Exercises

#### [Build] Sums of Every K-Block (Author exercise)
<!-- id: sw-block-sums -->

**Prerequisites.** Prefix sums from an earlier chapter, and the idea of an entering and a leaving value.

**Problem.** Given an int array and a block length `k`, return a `long` array whose entry `i` is the sum of the values at positions `i` through `i + k - 1`. Update one running total as the block moves, and do not mutate the input.

**Constraints.** 1 <= k <= nums.length <= 200000, with any `int` values, so the sums may exceed the int range. Each input element may be read at most twice.

**Example 1.** Input `nums = [3, -1, 4, 1, -5, 9], k = 3`, output `[6, 4, 0, 5]`.

**Example 2.** Input `nums = [7, 7], k = 1`, output `[7, 7]`.

**Hint.** What is the first moment at which the frame is exactly k wide? What should the total hold before that moment, and which position leaves when `right` reaches k?

**Changed decision.** First rung: the total is repaired by one add and one subtract instead of being recomputed.

#### [Vary] Maximum Average Subarray I (LeetCode 643)
<!-- id: sw-max-average -->

**Prerequisites.** The block-sums exercise above.

**Problem.** Find the contiguous subarray of length exactly `k` with the largest average and return that average as a `double`. Track the largest block sum and divide once at the end.

**Constraints.** 1 <= k <= nums.length <= 100000, with values in the full `int` range. Keep the total in a `long`, and seed the best total from the first block.

**Example 1.** Input `nums = [4, -2, 7, 1, -5, 6], k = 3`, output 3.0.

**Example 2.** Input `nums = [-8, -3, -6], k = 2`, output -4.5.

**Hint.** Why is comparing sums equivalent to comparing averages here? What goes wrong if the best total starts at zero for an all-negative array?

**Changed decision.** The output is one extreme over all blocks, not the whole list, and the only division happens after the scan.

#### [Boundary] Whole-Array Window (Author exercise)
<!-- id: sw-whole-array -->

**Prerequisites.** The two exercises above.

**Problem.** Return the start index of the first block of length `k` that has the largest sum, preferring the smaller start on ties. When `k` is smaller than 1 or larger than the array length, throw `IllegalArgumentException` rather than returning a made-up index.

**Constraints.** Any `nums.length` from 0 to 100000, any `int` values and any `int` k. The check on k comes before the first array access.

**Example 1.** Input `nums = [3, 1, 2], k = 3`, output 0.

**Example 2.** Input `nums = [1, 5, 2, 5], k = 2`, output 1.

**Hint.** How many blocks exist when k equals the length? Does the slide loop run at all in that case, and what should an empty array with k = 1 do?

**Changed decision.** The edge is a contract: the smallest legal frame count is one, and illegal widths fail loudly instead of producing a result.

#### [Recognize] Maximum Number of Vowels in a Substring of Given Length (LeetCode 1456)
<!-- id: sw-max-vowels -->

**Prerequisites.** The three exercises above.

**Problem.** For a string of lowercase English letters and a length `k`, return the largest number of vowels (`a`, `e`, `i`, `o`, `u`) found in any substring of length `k`. Each letter contributes one or zero to the maintained count.

**Constraints.** 1 <= k <= s.length() <= 100000, and the characters are `a` to `z` only. Read each character at most twice.

**Example 1.** Input `s = "sequoia", k = 4`, output 4.

**Example 2.** Input `s = "rhythm", k = 2`, output 0.

**Hint.** What replaces the numeric value of an element? Does the count need to be a `long`, and why or why not?

**Changed decision.** The aggregate is a count of elements with a property, so the entering and leaving values are small yes or no contributions.
