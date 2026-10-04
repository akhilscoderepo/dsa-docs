<!-- lesson-kind: standard -->
<!-- lesson-id: frequency-arrays -->
## Frequency Arrays

<!-- stage: context -->
### Why Counting Readings Becomes Slow

A sensor sends 100,000 integer readings, and each reading is a score from 0 to 100. A dashboard needs to know how many readings hold each score. A later feature asks how many readings fall below a given score. The data arrives in no particular order.

The problem looks like a search problem, because each reading must be compared with something. Yet the scores come from a very small set of possible values. The question is whether that small set gives a cheaper way to count than comparing readings with each other.

<!-- stage: naive -->
### Comparing Each Reading With All Others

The direct approach counts the occurrences of each reading by scanning the whole array again. For every position, it runs a second loop over all positions and counts matches.

```java
static int[] countByComparison(int[] scores) {
    int[] result = new int[scores.length];
    for (int i = 0; i < scores.length; i++) {
        for (int j = 0; j < scores.length; j++) {
            if (scores[j] == scores[i]) result[i]++;
        }
    }
    return result;
}
```

The method returns, for each position, the number of readings equal to the one at that position. It is correct for any integers, and it does not use the small range of the scores.

<!-- stage: bottleneck -->
### Counting The Repeated Comparisons

```predict
The array holds 100,000 readings and every reading is between 0 and 100. About how many comparisons does `countByComparison` make, and how many distinct answers exist?

About ten billion comparisons, since both loops run 100,000 times. Only 101 distinct answers exist, one per score, so the method recomputes the same answer many times.
```

Count the inner comparison. The outer loop runs `n` times and the inner loop runs `n` times for each outer pass. The total is `n * n`, which is O(n^2). For `n = 100,000` that is 10^10 comparisons.

The method also repeats itself. Two readings with the same score receive the same count, and the method computes that count again from scratch. With scores from 0 to 100, there are at most 101 different counts to find. A method that finds each count once, while reading the array once, does about `n` steps and not `n * n`. The next stage shows where to store those counts.

<!-- stage: insight -->
### Use The Value As An Index

#### A Small Range Of Values

A **bounded domain** is a set of possible values whose size is small and known in advance. The scores 0 to 100 form one, with 101 members. A grade, a digit, a die face and a lowercase letter each form one. A bounded domain is a property of the problem statement. The values must be stated to lie in a fixed range, and the range must be small compared with memory.

<!-- names: bounded domain, count array, range check -->

#### Storing Counts At The Value Position

A **count array** has one slot per member of the domain. The slot at position `v` holds the number of occurrences of `v` that the scan has processed. The array starts with every slot at 0. For each reading `x`, the algorithm executes `count[x]++`. No comparison between readings happens. The invariant is that after processing a prefix of the input, `count[v]` equals the number of occurrences of `v` in that prefix, for every `v` in the domain.

#### Checking The Range Before Indexing

A **range check** compares a value with the lower and upper limits of the domain before it indexes the array. Java throws `ArrayIndexOutOfBoundsException` for an index below 0 or at least the array length. A range check turns that crash into a decision, such as skipping the value or reporting invalid input. The count array also supports a second step: a running total over the slots turns counts into the number of values below each `v`, and a walk over the slots in order lists the values in sorted order.

<!-- stage: variables -->
### Track Counts And A Running Total

Four quantities describe the state.

- **Domain size** `D` is the number of possible values, such as 101 for scores 0 to 100.
- **`count`** is an `int[]` of length `D`, where `count[v - low]` stores the occurrences of `v`, and `low` is the smallest value.
- **Input length** `n` is the number of readings processed.
- **Running total** is the sum of `count` over slots below a given value, and it equals the number of smaller readings.

The memory use is `D` integers, and it does not depend on `n`.

<!-- stage: trace -->
### Follow The Counts Through An Array

Take the digits `[3, 1, 3, 0, 3, 1]` with the domain 0 to 4. The count array starts as `[0, 0, 0, 0, 0]`. Reading 3 raises slot 3 to 1, reading 1 raises slot 1 to 1, and the next 3 raises slot 3 to 2. Reading 0 raises slot 0, the third 3 raises slot 3 to 3, and the final 1 raises slot 1 to 2. The final count array is `[1, 2, 0, 3, 0]`. The slots add up to 6, which equals the number of readings. That sum is a quick check that no reading was missed or counted twice. Slot 2 and slot 4 stay at 0, because the input never contains those digits.

```trace
{"cells":[3,1,3,0,3,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"count":"[0, 0, 0, 1, 0]"},"note":"Read 3 at index 0. Slot 3 rises to 1. The counts are now [0, 0, 0, 1, 0]."},{"at":{"i":1},"vars":{"count":"[0, 1, 0, 1, 0]"},"note":"Read 1 at index 1. Slot 1 rises to 1. The counts are now [0, 1, 0, 1, 0]."},{"at":{"i":2},"vars":{"count":"[0, 1, 0, 2, 0]"},"note":"Read 3 at index 2. Slot 3 rises to 2. The counts are now [0, 1, 0, 2, 0]."},{"at":{"i":3},"vars":{"count":"[1, 1, 0, 2, 0]"},"note":"Read 0 at index 3. Slot 0 rises to 1. The counts are now [1, 1, 0, 2, 0]."},{"at":{"i":4},"vars":{"count":"[1, 1, 0, 3, 0]"},"note":"Read 3 at index 4. Slot 3 rises to 3. The counts are now [1, 1, 0, 3, 0]."},{"at":{"i":5},"vars":{"count":"[1, 2, 0, 3, 0]"},"note":"Read 1 at index 5. Slot 1 rises to 2. The counts are now [1, 2, 0, 3, 0]."}]}
```

The second trace turns the counts into running totals. Take the same counts `[1, 2, 0, 3, 0]`. A running total before slot `v` is the number of readings smaller than `v`. Slot 0 has total 0, slot 1 has total 1, slot 2 has total 3, slot 3 has total 3, and slot 4 has total 6. The hardest step is slot 3, because slot 2 holds no readings, so the total stays 3 instead of growing. Each total at a slot equals the total at the previous slot plus the previous slot's count, so an empty slot adds nothing. The last total, 6, equals the full input length because slot 4 is past every reading. Reading the table gives each query its answer without another scan of the input.

```trace
{"cells":[1,2,0,3,0],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"count":"[1, 2, 0, 3, 0]","before":"[0]"},"note":"Slot 0 holds 1 readings. The number of readings below 0 is 0, so the total is stored for slot 0. The running total becomes 1."},{"at":{"i":1},"vars":{"count":"[1, 2, 0, 3, 0]","before":"[0, 1]"},"note":"Slot 1 holds 2 readings. The number of readings below 1 is 1, so the total is stored for slot 1. The running total becomes 3."},{"at":{"i":2},"vars":{"count":"[1, 2, 0, 3, 0]","before":"[0, 1, 3]"},"note":"Slot 2 holds 0 readings. The number of readings below 2 is 3, so the total is stored for slot 2. The running total becomes 3."},{"at":{"i":3},"vars":{"count":"[1, 2, 0, 3, 0]","before":"[0, 1, 3, 3]"},"note":"Slot 3 holds 3 readings. The number of readings below 3 is 3, so the total is stored for slot 3. The running total becomes 6."},{"at":{"i":4},"vars":{"count":"[1, 2, 0, 3, 0]","before":"[0, 1, 3, 3, 6]"},"note":"Slot 4 holds 0 readings. The number of readings below 4 is 6, so the total is stored for slot 4. The running total becomes 6."}]}
```

<!-- stage: code -->
### Write The Counting Loop

```java
static int[] countDigits(int[] digits) {
    int[] count = new int[10];
    for (int x : digits) {
        count[x]++;
    }
    return count;
}

static int[] smallerBefore(int[] count) {
    int[] before = new int[count.length];
    int running = 0;
    for (int v = 0; v < count.length; v++) {
        before[v] = running;
        running += count[v];
    }
    return before;
}
```

The first method reads each value once, so it takes O(n) time. It allocates an array of 10 integers, so its space does not depend on `n`. The second method walks the `D` slots once, so it takes O(D) time. Java fills a new `int[]` with zeros, so the counts start correct without a reset loop. Each counter is an `int`, which holds counts up to about two billion.

<!-- stage: applicability -->
### Recognize Small Domains And Their Limits

#### Recognize The Pattern

Use a count array when the statement gives an explicit small integer range and asks about frequencies, ranks or sorted order. Constraints such as "each value is between 0 and 100" or "lowercase letters" are the signal. The invariant is that every slot counts the matching values in the processed prefix. Each correct solution preserves that statement after every read. A counting pass followed by a walk over the slots sorts the values in O(n + D) time, which beats comparison sorting when `D` is small.

#### Check The False Friend

An array indexed by arbitrary ids is a false friend. Customer ids up to 10^9 would need an array of a billion integers, which is about four gigabytes, even when only five customers exist. The array size must follow the stated range and not the largest value in sight. General keys belong to hash maps, which chapter 04 teaches.

#### Check The Java Hazards

Java throws on an index outside the array, so values that can leave the range need a range check first. A domain that starts above 0, such as heights from 1 to 100, needs an offset: use `count[v - low]`. A counter that can exceed the `int` range needs `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Digit Counts (Author exercise)
<!-- id: ar-digit-counts -->

**Prerequisites.** The count array and the domain from this lesson.

**Problem.** Given an integer array `digits` in which every value lies in `0..9`, return an `int[]` of length 10. The entry at position `d` is the number of times `d` appears in `digits`.

**Constraints.** The limits are:
- **`digits`** is an `int[]` with `0 <= digits.length <= 10^5`.
- **Values** are integers from 0 to 9, so no range check is needed.
- **Return value** is a new `int[10]`, and the input is not modified.
- **Extra space** is the output array only.

**Example 1.** Input `[2, 0, 2]`. Output `[1, 0, 2, 0, 0, 0, 0, 0, 0, 0]`.

**Example 2.** Input `[]`. Output ten zeros. The input `[9, 9, 9, 9]` returns zeros except for 4 at position 9.

**Hint.** What does slot `d` hold before the scan begins, and what changes it?

**Changed decision.** Baseline case: one slot per member of the domain, incremented once per reading.

#### [Vary] Smaller Than Current Number (LeetCode 1365)
<!-- id: ar-smaller-than-current -->

**Prerequisites.** The digit-counts exercise above.

**Problem.** Given an integer array `nums` with values in `0..100`, return an array `answer` of the same length. For each index `i`, `answer[i]` is the number of positions `j` with `nums[j] < nums[i]`.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 10^5`.
- **Values** are integers from 0 to 100.
- **Return value** is a new `int[]` of length `nums.length`, and the input is not modified.
- **Ties** do not count, because the comparison is strict.

**Example 1.** Input `[5, 0, 5, 2, 9]`. Output `[2, 0, 2, 1, 4]`.

**Example 2.** Input `[7, 7, 7]`. Output `[0, 0, 0]`, because no value is smaller than 7.

**Hint.** If you know how many readings equal each value, how do you combine those counts to get the number of readings below `v`?

**Changed decision.** The counts are no longer the answer. They feed a running total, and each query reads that total at the slot of its value.

#### [Boundary] Dice Validation (Author exercise)
<!-- id: ar-dice-validation -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `rolls`, return an `int[6]` where position `f - 1` holds the number of rolls equal to face `f`, for faces 1 to 6. If any roll lies outside `1..6`, return `null` and stop. Check the input `[1, 6, 0]`, which must return `null`.

**Constraints.** The limits are:
- **`rolls`** is an `int[]` with `0 <= rolls.length <= 10^5`.
- **Values** are any `int` values, including negative values and values above 6.
- **Return value** is a new `int[6]`, or `null` when any value is invalid.
- **Offset** is 1, because face 1 is stored at position 0.

**Example 1.** Input `[1, 6, 6]`. Output `[1, 0, 0, 0, 0, 2]`.

**Example 2.** Input `[1, 6, 0]`. Output `null`, because 0 is not a face. An empty input returns six zeros.

**Hint.** Which comparison must run before `count[roll - 1]++`, and what does Java do if the index is wrong?

**Changed decision.** The values may leave the domain, so a range check precedes every index operation.

#### [Recognize] Height Checker (LeetCode 1051)
<!-- id: ar-height-checker -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `heights` with values in `1..100`, let `expected` be the same values sorted in non-decreasing order. Return the number of indices `i` with `heights[i] != expected[i]`. The input array is not modified.

**Constraints.** The limits are:
- **`heights`** is an `int[]` with `1 <= heights.length <= 10^5`.
- **Values** are integers from 1 to 100.
- **Return value** is an `int` between 0 and `heights.length`.
- **Sorting** must not use a comparison sort.

**Example 1.** Input `[3, 1, 2, 2, 3]`. Output 3, since `expected` is `[1, 2, 2, 3, 3]` and positions 0, 1 and 3 differ.

**Example 2.** Input `[4, 4, 9]`. Output 0, because the array is already in order.

**Hint.** The sorted order is a walk over the slots from low to high. How do you compare each slot's values with the original positions?

**Changed decision.** The count array replaces a comparison sort, and the sorted sequence is never stored.
