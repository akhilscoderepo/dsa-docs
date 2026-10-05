<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-construction -->
## Build Running Totals

<!-- stage: context -->
### A Report That Recounts Every Day

A sales report lists 100,000 daily revenue figures. Beside each day it prints the revenue earned from the first day up to that day. The report job works for a small shop with 365 days. For ten years of data from a large store, it runs for minutes, because every row adds up all earlier days again.

Row 50,000 repeats the work of row 49,999 and adds one number. The question is how a program can store the sum of everything before a position, so that the next position costs a single addition.

<!-- stage: naive -->
### Adding The Days Again For Every Row

The direct method starts a new inner loop for every position. It adds the values from index 0 through index `i` and stores that total in `out[i]`.

```java
static long[] totalsThrough(int[] nums) {
    long[] out = new long[nums.length];
    for (int i = 0; i < nums.length; i++) {
        long sum = 0;
        for (int j = 0; j <= i; j++) sum += nums[j];
        out[i] = sum;
    }
    return out;
}
```

For `[3, 1, 4, 1, 5]` the method returns `[3, 4, 8, 9, 14]`. Position 4 adds five numbers, and position 3 added four of those five numbers a moment earlier.

```predict
The array holds 100,000 values. How many additions does `totalsThrough` perform in total?

It performs 1 + 2 + ... + 100,000 additions, which is 5,000,050,000. Position `i` costs `i + 1` additions, and the sum of those costs grows with the square of the length, so the method is O(n^2).
```

<!-- stage: bottleneck -->
### Every Total Contains The Previous Total

The total through index `i` equals the total through index `i - 1` plus `nums[i]`. The inner loop ignores that relation and rebuilds the earlier total from the first value. Position `i` performs `i + 1` additions, so the whole method performs about `n^2 / 2` additions, which is O(n^2).

The earlier total is already known when the loop reaches position `i`. The program computed it one step ago and then threw it away. For 100,000 days the method performs five billion additions, where 100,000 would give the same answers.

<!-- stage: insight -->
### Store The Total Before Each Position

A **prefix array** is an array `prefix` of length `n + 1` where `prefix[i]` is the sum of the first `i` values of `nums`. The value `prefix[i]` covers the indexes `0` to `i - 1`. It leaves out `nums[i]`.

#### The Entry For No Values

The first entry is `prefix[0] = 0`. It is the sum of zero values. This entry is a **sentinel**, which means a stored value that exists so the formulas need no special case for the first position. With it, every position follows the same rule, and the first position needs no `if`.

#### One Addition Per Position

The **recurrence** is `prefix[i + 1] = prefix[i] + nums[i]`. It defines each entry from the previous entry and one input value. The loop runs once per value, performs one addition per step, and costs O(n) time with O(n) extra space. The total through index `i` is then `prefix[i + 1]`, and the total before index `i` is `prefix[i]`.

<!-- names: prefix array, sentinel, recurrence -->

#### The Type Of Each Entry

Each entry is a sum of up to `n` values. With 100,000 values near 10^9, the sum reaches 10^14, which exceeds the `int` maximum of about 2.1 * 10^9. The array therefore has type `long[]`, and the addition widens each `int` before it adds.

<!-- stage: variables -->
### Four Names And Their Roles

The construction uses four names, and three of them change.

- **nums** is the input array and is never modified.
- **prefix** is the `long` array of length `n + 1`, and entry `i` holds the sum of the first `i` values.
- **i** is the position of the value that the loop adds next.
- **n** is `nums.length`, and it fixes the length of `prefix`.

The loop body reads `prefix[i]` and `nums[i]` and writes `prefix[i + 1]`. When the loop ends, every entry from `0` to `n` holds its final value.

<!-- stage: trace -->
### Two Uses Of The Same Array

#### Building The Array For Five Values

The input is `[3, 1, 4, 1, 5]`. The pointer `i` marks the value that the loop adds. Each step copies the previous entry and adds `nums[i]`. The array ends as `[0, 3, 4, 8, 9, 14]`, and its last entry is the sum of all five values.

```trace
{"cells":[3,1,4,1,5],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"prefix":"[0]"},"note":"Start with the sentinel entry prefix[0] = 0, the sum of zero values."},{"at":{"i":0},"vars":{"nums[i]":"3","prefix":"[0, 3]"},"note":"Add 3 to 0 and store 3 as prefix[1]."},{"at":{"i":1},"vars":{"nums[i]":"1","prefix":"[0, 3, 4]"},"note":"Add 1 to 3 and store 4 as prefix[2]."},{"at":{"i":2},"vars":{"nums[i]":"4","prefix":"[0, 3, 4, 8]"},"note":"Add 4 to 4 and store 8 as prefix[3]."},{"at":{"i":3},"vars":{"nums[i]":"1","prefix":"[0, 3, 4, 8, 9]"},"note":"Add 1 to 8 and store 9 as prefix[4]."},{"at":{"i":4},"vars":{"nums[i]":"5","prefix":"[0, 3, 4, 8, 9, 14]"},"note":"Add 5 to 9 and store 14 as prefix[5]."}]}
```

#### Finding The Position With Equal Sides

The input is `[1, 7, 3, 6, 5, 6]` and the total is 28. For each `i`, the left side is `prefix[i]`, and the right side is the total minus `prefix[i + 1]`. The loop stops at the first `i` where the two sides match. That is index 3, where each side sums to 11.

```trace
{"cells":[1,7,3,6,5,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"left":"0","right":"27"},"note":"Left side 0 differs from right side 27, so the loop moves on."},{"at":{"i":1},"vars":{"left":"1","right":"20"},"note":"Left side 1 differs from right side 20, so the loop moves on."},{"at":{"i":2},"vars":{"left":"8","right":"17"},"note":"Left side 8 differs from right side 17, so the loop moves on."},{"at":{"i":3},"vars":{"left":"11","right":"11"},"note":"Left side 11 equals right side 11, so index 3 is the pivot."}]}
```

<!-- stage: code -->
### The Construction In Java

```java
static long[] buildPrefix(int[] nums) {
    long[] prefix = new long[nums.length + 1];
    for (int i = 0; i < nums.length; i++) {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    return prefix;
}
```

Java fills a new `long[]` with zeros, so `prefix[0]` is already the sentinel. The expression `prefix[i] + nums[i]` adds a `long` and an `int`, and Java widens the `int` first. The method reads `nums` and never writes to it, so the caller keeps the original array.

An empty array gives `prefix` of length 1 with the single entry 0, and the loop body never runs.

<!-- stage: applicability -->
### When A Prefix Array Fits

#### The Invariant

The invariant is that after the step for index `i`, the entries `prefix[0]` through `prefix[i + 1]` hold the sums of the first 0 through `i + 1` values. The recurrence keeps it true, because one new value extends the previous sum by exactly that value. The sentinel makes the invariant hold before the first step.

#### The False Friend

The false friend is the index shift between the two arrays. The value `prefix[i]` excludes `nums[i]`, while a loop that stores totals in a same-length array makes entry `i` include it. Mixing the two conventions moves every answer by one position. The sentinel convention keeps one rule everywhere, and `prefix[i + 1]` is the total through index `i`.

#### Conditions That Break The Fit

An `int` accumulator fails when the sum can pass 2,147,483,647, and it wraps without an error. The array also assumes the values stay fixed. A single changed value in `nums` changes every later entry, so frequent updates need a different structure from a later chapter.

<!-- stage: exercises -->
### Exercises

#### [Build] Running Sum Of 1d Array (LeetCode 1480)
<!-- id: ps-running-sum -->

**Prerequisites.** The recurrence of this lesson.

**Problem.** Given an integer array `nums`, return an array `out` of the same length where `out[i]` is the sum of `nums[0]` through `nums[i]`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`; the empty array is valid.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Return type** is `long[]`, because a sum can exceed the `int` range.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [1,2,3,4]`, output `[1,3,6,10]`.

**Example 2.** Input `nums = [1000000000,1000000000,1000000000]`, output `[1000000000,2000000000,3000000000]`.

**Hint.** Each output equals the previous output plus one value. What type holds 3,000,000,000?

**Changed decision.** Basic case: one addition per position, with a `long` accumulator.

#### [Vary] Find Pivot Index (LeetCode 724)
<!-- id: ps-pivot-index -->

**Prerequisites.** The first exercise and the second trace of this lesson.

**Problem.** Given an integer array `nums`, return the smallest index `p` where the sum of the values left of `p` equals the sum of the values right of `p`. Return `-1` when no index qualifies. An empty side has sum 0.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values with `|nums[i]| <= 10^4`.
- **Tie** between several pivots returns the smallest index.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [1,7,3,6,5,6]`, output 3.

**Example 2.** Input `nums = [2,1,-1]`, output 0.

**Hint.** The right side equals the total minus the left side minus `nums[p]`. Which prefix entry gives the left side?

**Changed decision.** Every index compares two totals, so the question changes from one total to a relation between two totals.

#### [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-empty-prefix -->

**Prerequisites.** The sentinel entry of this lesson.

**Problem.** Given an integer array `nums` and an integer `c` with `0 <= c <= nums.length`, return the sum of the first `c` values of `nums`. The sum of zero values is 0. Build the array of this lesson and read one entry.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 1000`; the empty array is valid.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Count** `c` is between 0 and `nums.length` inclusive.
- **Return type** is `long`.

**Example 1.** Input `nums = [4,-2,7]` and `c = 0`, output 0.

**Example 2.** Input `nums = []` and `c = 0`, output 0.

**Hint.** Which entry of the array holds the sum of zero values, and does it exist when `nums` is empty?

**Changed decision.** The query reads the sentinel, so the answer for zero values needs no branch.

#### [Recognize] Prefix Averages (Author exercise)
<!-- id: ps-prefix-averages -->

**Prerequisites.** All exercises above. Java integer division.

**Problem.** Given an integer array `nums`, return an array `avg` where `avg[i]` is the sum of `nums[0]` through `nums[i]` divided by `i + 1`. Use Java integer division, which truncates toward zero.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Division** truncates toward zero, as the Java operator `/` does on `long` values.
- **Return type** is `long[]`.

**Example 1.** Input `nums = [4,6,5]`, output `[4,5,5]`.

**Example 2.** Input `nums = [-3,0,0]`, output `[-3,-1,-1]`.

**Hint.** The divisor for index `i` is the count `i + 1`, which equals the prefix index of the same total.

**Changed decision.** The stored total feeds a division, so the count of values must match the total's range.
