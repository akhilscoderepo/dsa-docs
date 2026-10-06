<!-- lesson-kind: standard -->
<!-- lesson-id: sliding-minimum -->
## Find The Minimum Of Every Window

<!-- stage: context -->
### A Copied Method Returns Maxima

A team has a method that reports the highest temperature in every hour-long range of a sensor log. A new feature needs the lowest temperature in every range. A developer copies the method, renames it `lowestPerRange`, and changes nothing else. The only test uses a log where every reading is equal, so the test passes. In production the method returns the highest readings under the name of the lowest ones.

This lesson asks two questions. Which comparisons must change when the answer switches from the largest value to the smallest, and which parts stay as they are? It then asks how a range that shrinks from the left, instead of sliding by a fixed length, uses the same deques.

<!-- stage: naive -->
### Counting Values In A Sorted Map

A sorted map keeps its keys in order and finds its smallest key quickly. The direct plan stores each value in the range with a count, so equal values share one key. A new value increases its count. A value that leaves the range decreases its count, and the key is deleted when the count reaches zero.

```java
static int[] minWithMap(int[] a, int k) {
    TreeMap<Integer, Integer> counts = new TreeMap<>();
    int[] out = new int[a.length - k + 1];
    for (int right = 0; right < a.length; right++) {
        counts.merge(a[right], 1, Integer::sum);                 // the new value enters
        if (right >= k) {
            int old = a[right - k];                              // the value that leaves the range
            if (counts.merge(old, -1, Integer::sum) == 0) counts.remove(old);
        }
        if (right >= k - 1) out[right - k + 1] = counts.firstKey();
    }
    return out;
}
```

The method is correct for every input. For `a = [7, 4, 5, 2, 9]` and `k = 3` it returns `4, 2, 2`.

<!-- stage: bottleneck -->
### Finding Values That Cannot Be The Minimum

```predict
A range holds the values 9, 7, 5, 3 from the oldest to the newest. All four stay in the range for the next step. Which of the four values can still be the minimum of some later range that contains it?

Only 3 can. Every later range that contains 9, 7 or 5 also contains the newer, smaller 3, so none of those three ever wins.
```

The sorted map holds all `k` values of the range, and each update costs O(log k). The total cost is O(n log k). Most of the stored values cannot win. A value that has a newer, smaller value behind it will never be the minimum while it stays in the range, and the map keeps it anyway. The repeated work is the sorting of values that have already lost.

<!-- stage: insight -->
### Mirroring The Back Comparison Only

#### Flipping One Comparison

The method keeps an **increasing deque**, which is a deque of positions whose values never decrease from the front to the back. The front holds the position of the minimum. The back removes a stored position when its value is strictly larger than the new value, because a newer, smaller value outlasts it. This **mirror comparison** is the only change from the maximum method.

#### Leaving The Front Unchanged

The front removes by age, and age does not depend on values. The age test still compares the front position with the left edge of the range. The three steps keep their order: age test, back removal, append, and the answer is read last. Copying the maximum method and keeping the back comparison unchanged breaks the invariant, because the front would then hold the maximum.

#### Moving The Left Edge By A Pointer

A range may shrink from the left in steps instead of sliding by a fixed length. A **left pointer** holds the first position of the range and only moves forward. The age test then compares the front position with the left pointer. For a fixed length the left pointer equals `right - k + 1`, so the fixed method is a special case. A problem that needs both the largest and the smallest value of a range keeps one deque of each kind and applies the same left pointer to both. Each position enters each deque once and leaves it at most once, so both deques together cost O(n).

<!-- names: increasing deque, mirror comparison, left pointer -->

<!-- stage: variables -->
### State For One Or Two Deques

The state differs slightly between the fixed range and the shrinking range.

- **Minimum deque** holds positions with non-decreasing values, and its front is the minimum.
- **Maximum deque** holds positions with non-increasing values, and its front is the maximum, which the shrinking-range problem also needs.
- **Left pointer** is the first position of the range, and it never moves backward.
- **Range spread** is the front value of the maximum deque minus the front value of the minimum deque, and it is zero for a range of one value.

A fixed-range problem uses one deque. A problem that limits the spread uses both, and it moves the left pointer while the spread is too large.

<!-- stage: trace -->
### Reading A Minimum And A Limited Spread

The first trace follows `a = [7, 4, 5, 2, 9, 4, 6]` with `k = 3`. The value 4 at position 1 removes position 0, because 7 is larger. The value 2 at position 3 removes positions 2 and 1 and leaves only position 3. The front then reads 2 for three ranges, until the age test removes position 3 at position 6. The output is `[4, 2, 2, 2, 4]`.

The second trace follows `b = [5, 8, 6, 7, 2, 9, 4]` with a spread limit of 3. Both deques accept each new position. When the spread exceeds the limit, the left pointer moves forward one position at a time, and each deque removes its front if that position falls behind the pointer. At position 4 the value 2 makes the spread six, and the pointer moves to position 4. The longest range that stayed within the limit has length 4.

```trace
{"cells":[7,4,5,2,9,4,6],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","output":"[]"},"note":"Right edge 0 brings 7. Nothing is removed. The first frame is not complete yet."},{"at":{"right":1},"vars":{"deque":"[1]","output":"[]"},"note":"Right edge 1 brings 4. The value 4 removes index 0 from the back because it is smaller. The first frame is not complete yet."},{"at":{"right":2},"vars":{"deque":"[1,2]","output":"[4]"},"note":"Right edge 2 brings 5. Nothing is removed. The front is index 1, so the frame reads 4."},{"at":{"right":3},"vars":{"deque":"[3]","output":"[4,2]"},"note":"Right edge 3 brings 2. The value 2 removes index 2, 1 from the back because it is smaller. The front is index 3, so the frame reads 2."},{"at":{"right":4},"vars":{"deque":"[3,4]","output":"[4,2,2]"},"note":"Right edge 4 brings 9. Nothing is removed. The front is index 3, so the frame reads 2."},{"at":{"right":5},"vars":{"deque":"[3,5]","output":"[4,2,2,2]"},"note":"Right edge 5 brings 4. The value 4 removes index 4 from the back because it is smaller. The front is index 3, so the frame reads 2."},{"at":{"right":6},"vars":{"deque":"[5,6]","output":"[4,2,2,2,4]"},"note":"Right edge 6 brings 6. Index 3 is expired and leaves the front. The front is index 5, so the frame reads 4."}]}
```

```trace
{"cells":[5,8,6,7,2,9,4],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"max_deque":"[0]","min_deque":"[0]","spread":0,"best":1},"note":"Index 0 (value 5) joins both deques. The spread is within the limit, so the left pointer stays. The window covers indices 0 to 0 with range 0, and the best length is 1."},{"at":{"left":0,"right":1},"vars":{"max_deque":"[1]","min_deque":"[0,1]","spread":3,"best":2},"note":"Index 1 (value 8) joins both deques. The spread is within the limit, so the left pointer stays. The window covers indices 0 to 1 with range 3, and the best length is 2."},{"at":{"left":0,"right":2},"vars":{"max_deque":"[1,2]","min_deque":"[0,2]","spread":3,"best":3},"note":"Index 2 (value 6) joins both deques. The spread is within the limit, so the left pointer stays. The window covers indices 0 to 2 with range 3, and the best length is 3."},{"at":{"left":0,"right":3},"vars":{"max_deque":"[1,3]","min_deque":"[0,2,3]","spread":3,"best":4},"note":"Index 3 (value 7) joins both deques. The spread is within the limit, so the left pointer stays. The window covers indices 0 to 3 with range 3, and the best length is 4."},{"at":{"left":4,"right":4},"vars":{"max_deque":"[4]","min_deque":"[4]","spread":0,"best":4},"note":"Index 4 (value 2) joins both deques. The spread was above 3, so the left pointer moves forward 4 step(s) to 4, expiring fronts that fall behind it. The window covers indices 4 to 4 with range 0, and the best length is 4."},{"at":{"left":5,"right":5},"vars":{"max_deque":"[5]","min_deque":"[5]","spread":0,"best":4},"note":"Index 5 (value 9) joins both deques. The spread was above 3, so the left pointer moves forward 1 step(s) to 5, expiring fronts that fall behind it. The window covers indices 5 to 5 with range 0, and the best length is 4."},{"at":{"left":6,"right":6},"vars":{"max_deque":"[6]","min_deque":"[6]","spread":0,"best":4},"note":"Index 6 (value 4) joins both deques. The spread was above 3, so the left pointer moves forward 1 step(s) to 6, expiring fronts that fall behind it. The window covers indices 6 to 6 with range 0, and the best length is 4."}]}
```

<!-- stage: code -->
### The Mirror Method And The Shrinking Range

```java
static int[] minOfWindows(int[] a, int k) {
    int[] out = new int[a.length - k + 1];
    Deque<Integer> d = new ArrayDeque<>();                     // positions, values non-decreasing
    for (int right = 0; right < a.length; right++) {
        if (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();     // age test, unchanged
        while (!d.isEmpty() && a[d.peekLast()] > a[right]) d.pollLast();   // mirrored comparison
        d.addLast(right);
        if (right >= k - 1) out[right - k + 1] = a[d.peekFirst()];
    }
    return out;
}

static int longestWithinSpread(int[] a, int limit) {
    Deque<Integer> hi = new ArrayDeque<>();                    // maximum candidates
    Deque<Integer> lo = new ArrayDeque<>();                    // minimum candidates
    int left = 0, best = 0;
    for (int right = 0; right < a.length; right++) {
        while (!hi.isEmpty() && a[hi.peekLast()] < a[right]) hi.pollLast();
        while (!lo.isEmpty() && a[lo.peekLast()] > a[right]) lo.pollLast();
        hi.addLast(right);
        lo.addLast(right);
        while (a[hi.peekFirst()] - a[lo.peekFirst()] > limit) {   // the range spread is too large
            left++;                                             // the range loses its first position
            if (hi.peekFirst() < left) hi.pollFirst();
            if (lo.peekFirst() < left) lo.pollFirst();
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

The inner loop moves the left pointer by one position per pass, so it expires at most one position from each deque per pass, and an `if` is enough. The loop ends before the deques empty, because a range of one value has spread zero and the limit is not negative. The subtraction of two values can overflow `int` when the values are near the type limits, so the exercises keep the values small.

- **Time** is O(n) for both methods. Each deque takes a position once, and the left pointer never moves backward.
- **Space** is O(k) for the first method and O(n) in the worst case for the second.

<!-- stage: applicability -->
### Choosing The Right Deque

#### Applying The Invariant

Choose the deque by the question. A question about the smallest value of a range needs the increasing deque, and a question about the largest value needs the decreasing deque. The invariant is that the front is the extreme value of the range, and the back comparison matches the question. A question that asks for both needs both deques.

#### Finding The False Friend

The false friend is copying the maximum method and changing its name only. The code compiles and runs, and it returns maxima. A copied comparison is correct only after each back comparison is reversed and each answer is checked against a test where the maximum and the minimum differ.

A second false friend is using one deque for both questions. The maximum candidates and the minimum candidates are different positions, so one deque cannot hold both.

#### No-Go Conditions

Do not use a left pointer when the range can also move backward, because the deques cannot restore positions they removed. Do not use the spread method with a negative limit, because the loop would try to empty the deques. When the question asks for the sum or the count of a range, a running total is simpler than any deque.

<!-- stage: exercises -->
### Exercises

#### [Build] Minimum Of Every K-Window (Author exercise)
<!-- id: dq-min-windows -->

**Prerequisites.** The window maximum from the previous lesson; this lesson.

**Problem.** Given an integer array `a` and a range length `k`, consider every range of `k` consecutive values, ordered by its first position. Return the array that holds the minimum value of each range, in the same order. Use a deque of positions whose values never decrease from the front to the back.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Output** has `n - k + 1` entries.

**Example 1.** Input `a = [7, 4, 5, 2, 9]`, `k = 3`, output `[4, 2, 2]`.

**Example 2.** Input `a = [9, 7, 5, 3]`, `k = 2`, output `[7, 5, 3]`.

**Hint.** Reverse the comparison at the back, and keep the age test at the front unchanged. Which comparison removes a larger older value?

**Changed decision.** First exercise of the lesson: the back comparison flips and nothing else changes.

#### [Vary] Window Range (Author exercise)
<!-- id: dq-window-range -->

**Prerequisites.** The minimum exercise above and the window maximum from the previous lesson.

**Problem.** For an integer array `a` and a range length `k`, return one number per range of `k` consecutive values. The number for a range is its maximum value minus its minimum value. Keep one deque for the maximum and one deque for the minimum, and apply the same age test to both.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -1,000,000 and 1,000,000, and the difference fits in `int`.
- **Output** has `n - k + 1` entries, and each entry is not negative.

**Example 1.** Input `a = [7, 4, 5, 2, 9]`, `k = 3`, output `[3, 3, 7]`.

**Example 2.** Input `a = [4, 4, 4]`, `k = 2`, output `[0, 0]`.

**Hint.** The two deques hold different positions. Which fronts give the maximum and the minimum of the current range?

**Changed decision.** The answer needs both extremes, so the method keeps two deques.

#### [Boundary] Duplicate Minima Expire (Author exercise)
<!-- id: dq-duplicate-minima -->

**Prerequisites.** The minimum exercise above and the tie rule from the weaker-value lesson.

**Problem.** For an array `a` and a range length `k`, return one position per range. The position for a range is the largest position that holds the minimum value of that range. A value equal to the back removes that back position, so the newer equal value takes its place.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Ties** return the largest position among equal minima.

**Example 1.** Input `a = [3, 1, 1, 4]`, `k = 2`, output `[1, 2, 2]`.

**Example 2.** Input `a = [2, 2, 2]`, `k = 2`, output `[1, 2]`.

**Hint.** Look at the range that contains both copies of the minimum in Example 1. Which copy leaves the range first, and which one should the deque have kept?

**Changed decision.** The tie rule makes the newest equal value replace the older one, so the older equal copy is never needed, because the newer one outlasts it.

#### [Recognize] LC 1438 Longest Continuous Subarray With Absolute Difference Less Than Or Equal To Limit (LeetCode 1438)
<!-- id: dq-lc1438 -->

**Prerequisites.** Both deque kinds and the left pointer from this lesson.

**Problem.** Given an integer array `nums` and an integer `limit`, find the longest contiguous range in which the difference between the largest and the smallest value is at most `limit`. Return the length of that range.

**Constraints.** The limits are:
- **Length** is between 1 and 100,000.
- **Values** are integers between 1 and 1,000,000,000.
- **Limit** is an integer between 0 and 1,000,000,000.
- **Output** is at least 1, because a range of one value has spread zero.

**Example 1.** Input `nums = [3, 9, 4, 5, 6, 1]`, `limit = 2`, output `3`.

**Example 2.** Input `nums = [1, 5, 9]`, `limit = 0`, output `1`.

**Hint.** When the spread is too large, which position leaves the range? Both deques must drop their fronts that fall behind the left pointer.

**Changed decision.** The range length is no longer fixed, so the left pointer replaces the fixed age rule.
