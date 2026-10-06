<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-size-window -->
## Slide A Window Of Fixed Size

<!-- stage: context -->
### A Monitor That Falls Behind

A monitoring job stores one request count per minute. A dashboard must show the total for every block of 10,000 consecutive minutes, so an operator can spot a slow rise in traffic. The job holds a million counts, and it freezes. The code adds up each block from scratch, and neighbouring blocks share all but two of their minutes. The job repeats almost the same additions again and again.

Many problems ask about every block of exactly `k` consecutive values. They want the highest total, the highest average, or the blocks that hold a certain kind of value. This lesson asks one question. When two neighbouring blocks overlap in all but two positions, how does the answer for the second block reuse the answer for the first?

<!-- stage: naive -->
### Add Up Each Block From Scratch

The direct method treats every block as a new problem. For each start index, it adds the `k` values of that block and stores the total.

```java
static long[] blockSumsFromScratch(int[] nums, int k) {
    long[] out = new long[nums.length - k + 1];
    for (int start = 0; start + k <= nums.length; start++) {
        long total = 0;
        for (int i = start; i < start + k; i++) total += nums[i];
        out[start] = total;
    }
    return out;
}
```

The method is correct and easy to check. Its outer loop visits each start index, and its inner loop reads `k` values for each one.

<!-- stage: bottleneck -->
### Counting The Repeated Additions

```predict
Take the block that starts at index 0 and the block that starts at index 1. How many values differ between the two blocks?

Exactly two values differ. The value at index 0 is in the first block only, and the value at index `k` is in the second block only. The other `k - 1` values appear in both blocks, so the naive method adds them twice.
```

The array has `n - k + 1` blocks, and the naive method adds `k` values for each one. The cost is O(n * k). For `n = 1,000,000` and `k = 10,000`, that is about 9.9 billion additions. For `k = 500,000`, it is about 250 billion.

The largest cost comes from the middle sizes of `k`, where the number of blocks and the size of each block are both large. Almost all of that work is repeated, because each addition recomputes part of the previous block's total. The cost should depend on `n` alone, because each value only needs to enter a total once and leave it once.

<!-- stage: insight -->
### Keep One Sum And Update It

#### The Window Is A Range Of Indexes

A **window** is a contiguous subarray or substring. In an array it is the range `nums[left..right]` with both ends included. A window of fixed size `k` has `right = left + k - 1`, so `left` alone fixes the window. The method needs a stored value that describes the window and survives a move to the next window.

#### The Running Sum Changes By Two Terms

The **running sum** is the total of the values currently inside the window. It lives in one variable. Moving to the next window changes only two members. The value `nums[left]` leaves, and the value `nums[right + 1]` enters. The new running sum is the old sum, minus the leaving value, plus the entering value. That update costs two operations for any `k`.

#### Sliding Fills Once And Then Moves

To **slide** the window means to add one to both `left` and `right`. The method builds the first window by adding `k` values, and then it slides across the rest of the array. The invariant is this: before the method records a result, the running sum equals the sum of `nums[left..right]`. Every index enters the sum once and leaves it at most once, so the whole pass costs O(n).

<!-- names: window, running sum, slide -->

<!-- stage: variables -->
### What The Method Keeps

The method keeps a small set of values, and each has one meaning at every step.

- **nums** is the input array, and the method never changes it.
- **k** is the fixed window size, and it satisfies `1 <= k <= nums.length`.
- **left** is the index of the first value inside the window.
- **right** is the index of the last value inside the window.
- **sum** is the running sum of `nums[left..right]`, held in a `long`.
- **out** holds one total per window, and the entry at index `left` belongs to the window that starts at `left`.

<!-- stage: trace -->
### Tracing Two Passes

#### Sums Of Every Block Of Three

Take `nums = [4, 2, 7, 1, 3, 5]` and `k = 3`. The trace below shows the pointers `left` and `right` and the variable `sum`. The first three steps fill the first window, so the first total, 13, appears when `right` reaches index 2. Each later step moves `right` one place, adds the entering value and subtracts the leaving value.

```trace
{"cells":[4,2,7,1,3,5],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"sum":"4"},"note":"The value 4 enters, so the sum is 4."},{"at":{"left":0,"right":1},"vars":{"sum":"6"},"note":"The value 2 enters, so the sum is 6."},{"at":{"left":0,"right":2},"vars":{"sum":"13"},"note":"The value 7 enters, so the sum is 13. The window is full and the first total is 13."},{"at":{"left":1,"right":3},"vars":{"sum":"10"},"note":"The value 1 enters and the value 4 leaves, so the sum becomes 10."},{"at":{"left":2,"right":4},"vars":{"sum":"11"},"note":"The value 3 enters and the value 2 leaves, so the sum becomes 11."},{"at":{"left":3,"right":5},"vars":{"sum":"9"},"note":"The value 5 enters and the value 7 leaves, so the sum becomes 9."}]}
```

At every step after the fill, only two values change the sum. The method never reads the values in the middle of the window again.

#### A Maximum With Negative Values

Take `nums = [-9, -1, -6, -2, -3]` and `k = 2`, and track the largest window total in the variable `best`. Every total is negative here, so the correct answer is also negative. The best total, -5, appears at the last window. A starting value of 0 for `best` returns 0, which is the sum of no window at all. The method sets `best` to the first window's total, and then compares each later total with it.

```trace
{"cells":[-9,-1,-6,-2,-3],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":1},"vars":{"sum":"-10","best":"-10"},"note":"The first window gives -10, and best starts at -10, not at 0."},{"at":{"left":1,"right":2},"vars":{"sum":"-7","best":"-7"},"note":"The value -6 enters and the value -9 leaves, so the sum is -7. The sum beats -10, so best becomes -7."},{"at":{"left":2,"right":3},"vars":{"sum":"-8","best":"-7"},"note":"The value -2 enters and the value -1 leaves, so the sum is -8. The sum does not beat -7, so best stays."},{"at":{"left":3,"right":4},"vars":{"sum":"-5","best":"-5"},"note":"The value -3 enters and the value -6 leaves, so the sum is -5. The sum beats -7, so best becomes -5."}]}
```

<!-- stage: code -->
### Sliding The Window In Java

#### One Pass With A Running Sum

```java
static long[] windowSums(int[] nums, int k) {
    long sum = 0;
    for (int right = 0; right < k; right++) sum += nums[right];
    long[] out = new long[nums.length - k + 1];
    out[0] = sum;
    for (int right = k; right < nums.length; right++) {
        sum += nums[right];
        sum -= nums[right - k];
        out[right - k + 1] = sum;
    }
    return out;
}
```

The first loop fills the window, and the second loop slides it. The leaving index is `right - k`, because the window before the slide covers `right - k .. right - 1`. The sum has type `long`, so a large `k` times large values cannot overflow it.

#### Cost Of The Pass

The method reads each index once in the fill loop or once in the slide loop, so the time is O(n). The extra memory is O(1) beyond the output array. The method never copies a subarray, so no step costs O(k).

<!-- stage: applicability -->
### When The Window Applies

#### Spotting A Fixed-Size Window

Look for a request about every contiguous block of exactly `k` elements. The answer for one block must update when one value leaves and one enters. The aggregate must support removal. A sum, a count and a product of non-zero values support removal. A plain maximum does not, because the leaving value might be the maximum, and a later chapter on deques handles that case.

#### The Invariant To State

Before the method uses the aggregate, the aggregate describes exactly `nums[left..right]` and the length is `k`. A reader who states this invariant before writing the loop avoids the usual off-by-one error in the leaving index.

#### When A Prefix Sum Fits Better

A prefix sum array stores, at each index, the sum of all values before it, so the sum of any range is one subtraction of two stored values, in O(1) after an O(n) build. A prefix sum is the better tool when many unrelated range queries follow. A window is the natural tool for one left-to-right pass, and it needs no extra array. A prefix sum is a false friend here, because it looks like the right tool and wastes memory. The false friend shows up when the problem names no ranges beyond the fixed size, and the prefix array then costs memory without any benefit.

#### Java Hazards

Check the contract for `k` before the first loop. A value `k = 0` gives a wrong output length, and `k > nums.length` reads past the array. Divide a sum into an average once at the end, and cast one operand to `double` before the division.

<!-- stage: exercises -->
### Exercises

#### [Build] Sums Of Every K-Block (Author exercise)
<!-- id: sw-block-sums -->

**Prerequisites.** The running sum and the invariant of this lesson.

**Problem.** Given an integer array `nums` and an integer `k`, return an array `out` of length `nums.length - k + 1`. For each `i` from 0 to `nums.length - k`, `out[i]` is the sum of `nums[i..i + k - 1]`.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Window size** satisfies `1 <= k <= nums.length`.
- **Values** satisfy `-10^4 <= nums[i] <= 10^4`.
- **Return** type is `long[]`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [4,2,7,1,3,5]`, `k = 3`. Output `[13,10,11,9]`.

**Example 2.** Input `nums = [-5,5]`, `k = 1`. Output `[-5,5]`.

**Hint.** After the first sum, which two values change when the window moves by one index?

**Changed decision.** Basic case: one entering value and one leaving value replace a sum of `k` values.

#### [Vary] Maximum Average Subarray I (LeetCode 643)
<!-- id: sw-max-average -->

**Prerequisites.** The block sums exercise above.

**Problem.** Among the contiguous subarrays of `nums` with length exactly `k`, find the one with the largest average value. Return that average as a `double`. The average of a block is its sum divided by `k`.

**Constraints.**
- **Length** satisfies `1 <= k <= nums.length <= 10^5`.
- **Values** satisfy `-10^4 <= nums[i] <= 10^4`.
- **Tolerance** allows an absolute error of `10^-5`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [3,-1,4,-2,6]`, `k = 2`. Output `2.0`, from the block `[-2,6]`.

**Example 2.** Input `nums = [-3,-8,-5]`, `k = 2`. Output `-5.5`, from the block `[-3,-8]`.

**Hint.** Compare window sums as integers, and divide once after the loop. Which starting value for the best sum survives a case where every sum is negative?

**Changed decision.** The method keeps a maximum over the totals and defers the division to the end.

#### [Boundary] Whole-Array Window (Author exercise)
<!-- id: sw-whole-array -->

**Prerequisites.** The two exercises above.

**Problem.** The input is an integer array `nums` and an integer `k`. Return the largest sum over all contiguous blocks of length exactly `k`. If `k` is not in the range `1` to `nums.length`, throw an `IllegalArgumentException`. The method must give the correct answer when `k == nums.length`, which has exactly one block.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Window size** is any `int`, and the method validates it.
- **Values** satisfy `-10^4 <= nums[i] <= 10^4`.
- **Return** type is `long`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [2,-7,4]`, `k = 3`. Output `-1`, the sum of the whole array.

**Example 2.** Input `nums = [2,-7,4]`, `k = 4`. Output: the method throws `IllegalArgumentException`.

**Hint.** How many times does the slide loop run when `k == nums.length`? What does the single `long` result hold?

**Changed decision.** A contract check replaces a silent guess for an illegal `k`.

#### [Recognize] Maximum Number Of Vowels In A Substring Of Given Length (LeetCode 1456)
<!-- id: sw-max-vowels -->

**Prerequisites.** All three exercises above.

**Problem.** Given a string `s` of lowercase English letters and an integer `k`, return the largest number of vowels in any substring of length exactly `k`. The vowels are `a`, `e`, `i`, `o` and `u`.

**Constraints.**
- **Length** satisfies `1 <= k <= s.length <= 10^5`.
- **Characters** are lowercase English letters `a` to `z`.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is unchanged.

**Example 1.** Input `s = "abciiidef"`, `k = 3`. Output `3`, from the substring `iii`.

**Example 2.** Input `s = "rhythm"`, `k = 2`. Output `0`, because no vowel occurs.

**Hint.** Which value does each character add to the window, and which value does it remove when it leaves?

**Changed decision.** Each character contributes 0 or 1 to a count, in place of an integer value.
