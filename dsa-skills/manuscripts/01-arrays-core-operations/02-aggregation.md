<!-- lesson-kind: standard -->
<!-- lesson-id: aggregation -->
## Aggregation

<!-- stage: context -->
### The Overnight Peak Display

A cold-storage warehouse has a wall display that shows, after every temperature reading, the warmest reading so far tonight. The readings arrive every minute from midnight, and by morning there are hundreds of them. The facilities manager glances at the display at any hour and wants the number to be right.

Think about what the display's program must remember. It cannot need the whole night's readings to answer, or it would grow all night. One number should be enough, and each new reading should change that number at most once. Plenty of array questions have this flavor, where a summary small enough to fit in a variable can absorb elements one at a time.

<!-- stage: naive -->
### Recompute From The Start Each Time

The direct way to keep the display right is to rescan everything after each new reading and pick the largest.

```java
static int[] runningMaxRescan(int[] readings) {
    int[] shown = new int[readings.length];
    for (int i = 0; i < readings.length; i++) {
        int best = readings[0];
        for (int j = 1; j <= i; j++) {
            best = Math.max(best, readings[j]);
        }
        shown[i] = best;
    }
    return shown;
}
```

It is correct, since every shown value is the true maximum of the readings so far. It is also exactly what the problem says, restated as code, so it needs no cleverness to write.

<!-- stage: bottleneck -->
### Reading The Past Again And Again

After the `i`-th reading the inner loop looks at `i + 1` values, so the work is 1 + 2 + ... + n, which is `n * (n + 1) / 2` and O(n^2) overall. A night of 600 readings costs about 180,000 looks, which is harmless. A sensor sampling every millisecond for a day produces 86.4 million readings, and the rescanning needs about 3.7 * 10^15 looks, which no machine finishes.

The waste is plain to see. The maximum of the first 500 readings was computed a moment ago, and the new reading does not change anything about those 500 values. Yet the method throws that answer away and recomputes it. Space is not the issue, because the extra memory is O(1) beyond the output. The inefficiency is repeated work on data that has not changed.

<!-- stage: insight -->
### Keep A Summary That Absorbs One Element

The previous maximum already contains everything the old readings can say about the maximum. When a new reading arrives, the new maximum is the larger of the old maximum and the new reading. Nothing else is needed, and nothing is looked at twice.

A variable that carries what has been learned from the prefix is an **accumulator**. The invariant that makes the technique work is that before processing `nums[i]`, the accumulator describes exactly `nums[0..i-1]`, no more and no less. Processing the element extends the description by one position, and the loop repeats. The accumulator can be a sum, a count, a maximum, a minimum, or several of these held together.

<!-- names: accumulator, fixed-size summary -->

The technique applies when the question can be answered from a **fixed-size summary**, a handful of scalars whose size does not grow with the input. Some summaries can absorb an element and need nothing else. The sum plus the new value is the new sum, the larger of two maxima is the new maximum, and a count plus one is the new count. Other questions refuse to fit. Asking for the best pair, or the best block of consecutive values, needs information about relationships between positions that one scalar cannot hold, which is why those questions get their own lessons.

Initialization follows from the invariant. Before any element has been processed, the accumulator must describe the empty prefix. A sum starts at zero because an empty sum is zero, and a count starts at zero for the same reason. A maximum has no empty-prefix value, so it starts from the first real element and the loop begins at index 1.

<!-- stage: variables -->
### What Each Accumulator Means

Name the accumulator by what it summarizes, such as `maxSoFar`, `total` or `evenCount`, and write its meaning beside the declaration. The loop index `i` marks the next element to absorb. For a problem that needs several summaries at once, declare them all before the loop and update each exactly once per element, so that at every point all of them describe the same prefix.

<!-- stage: trace -->
### Three Summaries Over Three Readings

Take the readings `[-3, 8, 1]` and keep a sum, a maximum and a minimum together. Before anything is read, the sum is 0 and the maximum and minimum have not been set. Reading the first value, -3, sets the maximum and minimum to -3, since the prefix holds a single value, and the sum becomes -3.

Reading 8 raises the sum to 5 and the maximum to 8, and leaves the minimum at -3. Reading 1 raises the sum to 6 and changes neither extreme. The final answers are a sum of 6, a maximum of 8 and a minimum of -3. The step that students underrate is the first one. A maximum started at 0 would stay 0 for an all-negative input, which is why the first real element, and never an arbitrary constant, must seed it.

```trace
{"cells":[-3,8,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"sum":-3,"max":-3,"min":-3},"note":"Read -3. The prefix holds one value, so max and min are both seeded with -3, and the sum is -3."},{"at":{"i":1},"vars":{"sum":5,"max":8,"min":-3},"note":"Read 8. The sum becomes 5 and the maximum rises to 8. The minimum stays -3."},{"at":{"i":2},"vars":{"sum":6,"max":8,"min":-3},"note":"Read 1. The sum becomes 6. Neither extreme changes, because 1 is between them."}]}
```

<!-- stage: code -->
### Single-Pass Summaries

```java
static int maximum(int[] nums) {            // contract: nums is non-empty
    int best = nums[0];                     // describes the prefix nums[0..0]
    for (int i = 1; i < nums.length; i++) {
        best = Math.max(best, nums[i]);     // best now describes nums[0..i]
    }
    return best;
}

static int countAbove(int[] nums, int threshold) {
    int count = 0;                          // the empty prefix has count 0
    for (int v : nums) {
        if (v > threshold) count++;
    }
    return count;
}
```

Both methods make one pass and keep O(1) extra space, so they run in O(n) time. `maximum` starts from `nums[0]` because the contract promises a non-empty array, in line with the guarantee habit from Chapter 00. `countAbove` starts at 0 because an empty prefix has no matches, and it needs no guard, since an empty array simply returns 0. For sums, declare the accumulator `long` whenever the values and the length together can exceed the `int` range.

<!-- stage: applicability -->
### When One Scalar Is Enough

Use aggregation when the answer is determined by a few numbers that summarize the elements read so far. The invariant to state is that before processing `nums[i]`, the accumulator describes exactly `nums[0..i-1]`, and the update after processing extends it to `nums[0..i]`. If you can say what the summary of the empty prefix is, initialization is settled.

The false friend is a question about pairs or blocks that looks like an aggregate. The best difference between two positions, or the best sum over a stretch of consecutive values, cannot be maintained by a single maximum or a single sum, because the right choice depends on relationships between elements. The next lessons introduce the extra state those questions need. Treating them as plain aggregates produces code that passes the first sample and fails the second.

Java hazards are mostly numeric. A sum of many `int` values can overflow, so use `long`. Dividing two integers truncates, so an average needs a cast before the division. `Integer.MIN_VALUE` as the starting maximum is correct only if no legal value can fall below it, and starting from the first element avoids the question.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum (Author exercise)
<!-- id: ar-maximum -->

**Prerequisites.** The accumulator invariant from this lesson; Chapter 00 input guarantees.

**Problem.** Given a non-empty integer array `nums`, return its largest value. Initialize the accumulator from the input and not from zero, and do not modify the array.

**Constraints.** 1 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. Aim for a single pass with a few scalars.

**Example 1.** Input `nums = [-3, 8, 1]`, output 8.

**Example 2.** Input `nums = [-5]`, output -5, so a single negative value is still the maximum.

**Hint.** Which element is guaranteed to exist before the loop starts? What would a starting value of zero do to an all-negative array?

**Changed decision.** First rung: the accumulator is seeded from the data and absorbs one element per step.

#### [Vary] Find Numbers with Even Number of Digits (LeetCode 1295)
<!-- id: ar-even-digit-count -->

**Prerequisites.** The maximum exercise above.

**Problem.** Given an array of positive integers, return how many of them have an even number of decimal digits. The accumulator is now a count, and each element is classified by its digit count.

**Constraints.** 0 <= nums.length <= 500 and 1 <= nums[i] <= 10^5. Do not convert numbers to strings if a loop over digits is simple enough.

**Example 1.** Input `nums = [100, 7, 22, 3000, 55555]`, output 2, from 22 and 3000.

**Example 2.** Input `nums = []`, output 0, because an empty prefix has a count of zero.

**Hint.** How can you count the digits of a number by repeated division by ten? Which value does a count accumulator start from?

**Changed decision.** The state changes from an extremum to a count, and the update depends on a property of each element.

#### [Boundary] Max Consecutive Ones (LeetCode 485)
<!-- id: ar-max-consecutive-ones -->

**Prerequisites.** The two exercises above.

**Problem.** Given a binary array of zeros and ones, return the length of the longest run of consecutive ones. Reset the current run at every zero while preserving the best completed run, and handle an array that ends in the middle of a run.

**Constraints.** 1 <= nums.length <= 10^5 and each `nums[i]` is 0 or 1. Use one pass and no auxiliary array.

**Example 1.** Input `nums = [1, 0, 1, 1, 0, 1]`, output 2.

**Example 2.** Input `nums = [0, 0]`, output 0, since there is no one at all.

**Hint.** Do you need to remember every run, or only the current one and the best so far? When should the best be updated, only at a zero or at every step?

**Changed decision.** Two accumulators now cooperate, one that resets and one that never decreases.

#### [Recognize] Average Salary Excluding the Minimum and Maximum Salary (LeetCode 1491)
<!-- id: ar-average-salary -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array of distinct salaries, return the average salary after excluding the single minimum and the single maximum. One pass should keep the sum, the minimum and the maximum together, and the answer is computed from those three values at the end.

**Constraints.** 3 <= salary.length <= 100, 1000 <= salary[i] <= 10^6 and all values are distinct. An answer within 10^-5 of the true value is accepted.

**Example 1.** Input `salary = [1900, 2500, 2200, 1700]`, output 2050.0, from the middle values 1900 and 2200.

**Example 2.** Input `salary = [1000, 2000, 3000]`, output 2000.0, since only 2000 remains after the extremes are removed.

**Hint.** Which three scalars does the final formula need? Why must the division be done in floating point?

**Changed decision.** The summary grows to three scalars that are updated together and combined only at the end.
