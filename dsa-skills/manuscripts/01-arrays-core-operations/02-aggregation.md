<!-- lesson-kind: standard -->
<!-- lesson-id: aggregation -->
## Aggregation

<!-- stage: context -->
### Why The Warmest Night Reads Zero

A weather tool stores the overnight low of each station in an `int[]`, measured in degrees Celsius. On a freezing week every value is below zero. A user asks for the warmest reading, and the tool answers 0. No station recorded 0. The method started its answer at 0 and no reading was ever larger, so the starting guess survived to the end.

The same slip appears in sums that overflow, in counters that never restart, and in averages that include values they should skip. In each case a single number has to stand for everything read so far. This lesson asks what that number must mean, how it starts, and when a single number is not enough.

<!-- stage: naive -->
### Comparing Every Element With Every Other

The direct reading of "the largest value" is a definition: an element is the largest when no element is greater. A method can test that definition for each element in turn.

```java
static int maximumByComparison(int[] nums) {
    for (int i = 0; i < nums.length; i++) {
        boolean largest = true;
        for (int j = 0; j < nums.length; j++) {
            if (nums[j] > nums[i]) largest = false;
        }
        if (largest) return nums[i];
    }
    throw new IllegalArgumentException("empty array");
}
```

The method is correct for every non-empty array. It compares each candidate with the whole array, so it repeats a great deal of work.

<!-- stage: bottleneck -->
### Re-Reading The Array For Every Candidate

```predict
For an array of 100,000 distinct values with the largest one in the last position, about how many comparisons does `maximumByComparison` perform?

About ten billion. Every candidate before the last one runs the inner loop over all 100,000 elements and finds a larger value, so about 100,000 times 100,000 comparisons happen. A single pass needs only 100,000.
```

The inner loop answers the same question again and again. Each time it learns whether some element exceeds `nums[i]`, but it forgets what it learned about the other elements. The cost is O(n^2) comparisons, while one pass over the array can finish in O(n).

The waste comes from keeping no memory between candidates. If the method remembered the largest value seen so far, each new element would need one comparison against that memory. The remaining question is what the memory must contain, and how it starts before any element has been read.

<!-- stage: insight -->
### One Running Value Summarizes The Prefix

#### Keep One Accumulator

An **accumulator** is a variable of fixed size that the loop updates once per element. Its meaning is a promise about the part of the array already read. Before the loop processes `nums[i]`, the accumulator describes exactly `nums[0..i-1]`. Processing `nums[i]` extends that description by one element, so the promise holds again for `nums[0..i]`.

#### Choose The Initial Value From The Contract

The accumulator needs a correct meaning before the first element, so its **initial value** matters as much as its update. A count of matches starts at 0, because zero elements contain zero matches. A sum starts at 0 for the same reason. A maximum has no neutral number, because every `int` can be the answer. The safe choice reads the first element and starts the loop at index 1, which makes the promise true from the beginning.

#### Reset A Run When The Condition Breaks

Some questions ask about a streak of consecutive elements. Two accumulators solve them: the length of the current streak and the best streak completed or in progress. A matching element extends the current streak. An element that breaks the condition causes a **reset** of the current streak to 0, while the best streak keeps its value. The best streak must also update when the streak grows, because a streak that reaches the end of the array never meets a breaking element.

<!-- names: accumulator, initial value, reset -->

#### Combine Several Scalars

A formula may need more than one summary, such as a sum together with a minimum and a maximum. One pass can update all of them, since each needs only the same current element. The cost stays O(n) time and O(1) space.

<!-- stage: variables -->
### Name What Each Accumulator Means

Write the meaning of every accumulator in one sentence before coding. Each definition must stay true after every iteration.

- **`max`** is the largest value in `nums[0..i-1]`, and it starts as `nums[0]`.
- **`count`** is the number of elements in `nums[0..i-1]` that satisfy the condition, and it starts at 0.
- **`sum`** is the total of `nums[0..i-1]`, held in a `long`, and it starts at 0.
- **`current`** is the length of the streak that ends at position `i - 1`, and it drops to 0 when the condition breaks.
- **`best`** is the longest streak found anywhere in `nums[0..i-1]`, and it never decreases.

<!-- stage: trace -->
### Trace A Maximum And A Streak

The first trace finds the maximum of `[-6, -2, -9, -2, -4]`. The accumulator `max` starts as -6, which is the first element. At `i = 1` the value -2 is larger, so `max` becomes -2. At `i = 2` the value -9 is smaller and `max` stays. At `i = 3` the value -2 equals `max`, so nothing changes. The final value is -2, and a starting value of 0 would have produced the wrong answer 0 here.

The second trace finds the longest run of ones in `[1, 1, 0, 1, 1, 1]`. The streak `current` grows to 2, resets to 0 at the zero, and then grows to 3. The value `best` follows the growth, so it reads 2 after the first run and 3 at the end. The last step matters most. The array ends inside a run, so no zero arrives to trigger a final update, and `best` must already hold 3.

```trace
{"cells":[-6,-2,-9,-2,-4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"max":-6},"note":"max starts as the first element, -6. The loop begins at index 1."},{"at":{"i":1},"vars":{"max":-2},"note":"i = 1: -2 is larger than the old max, so max becomes -2."},{"at":{"i":2},"vars":{"max":-2},"note":"i = 2: -9 is not larger than -2, so max stays -2."},{"at":{"i":3},"vars":{"max":-2},"note":"i = 3: -2 is not larger than -2, so max stays -2."},{"at":{"i":4},"vars":{"max":-2},"note":"i = 4: -4 is not larger than -2, so max stays -2."},{"at":{"i":5},"vars":{"max":-2},"note":"The loop ends. max is -2."}]}
```

```trace
{"cells":[1,1,0,1,1,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"current":1,"best":1},"note":"i = 0: the value is 1, so current grows to 1. best is 1."},{"at":{"i":1},"vars":{"current":2,"best":2},"note":"i = 1: the value is 1, so current grows to 2. best is 2."},{"at":{"i":2},"vars":{"current":0,"best":2},"note":"i = 2: the value is 0, so current resets to 0 and best keeps its value. best is 2."},{"at":{"i":3},"vars":{"current":1,"best":2},"note":"i = 3: the value is 1, so current grows to 1. best is 2."},{"at":{"i":4},"vars":{"current":2,"best":2},"note":"i = 4: the value is 1, so current grows to 2. best is 2."},{"at":{"i":5},"vars":{"current":3,"best":3},"note":"i = 5: the value is 1, so current grows to 3. best is 3."},{"at":{"i":6},"vars":{"current":3,"best":3},"note":"The array ends inside a run. No zero follows, and best already holds 3."}]}
```

<!-- stage: code -->
### Write Maximum, Count And Streak Scans

```java
static int maximum(int[] nums) {
    int max = nums[0];
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] > max) max = nums[i];
    }
    return max;
}

static long total(int[] nums) {
    long sum = 0;
    for (int v : nums) sum += v;
    return sum;
}

static int longestRun(int[] bits) {
    int current = 0, best = 0;
    for (int b : bits) {
        if (b == 1) current++;
        else current = 0;
        best = Math.max(best, current);
    }
    return best;
}
```

Each method makes one pass, so each costs O(n) time and O(1) space. The `maximum` method assumes a non-empty array, because it reads `nums[0]` before the loop. The `total` method declares `sum` as a `long`, so adding many large `int` values cannot wrap around. In `longestRun`, the update of `best` sits outside the branch, so it runs after every element and covers a run that touches the end.

<!-- stage: applicability -->
### Check The Summary Before Folding

#### Recognize A Foldable Question

Use an accumulator when a fixed-size value can describe the prefix completely. The invariant is that the accumulator equals the answer for `nums[0..i-1]` before each step. Counts, sums, minimums, maximums and streak lengths all satisfy it. A good test is to ask whether the answer for the first `i + 1` elements follows from the answer for the first `i` elements and `nums[i]` alone.

#### Reject Pair And Subarray Questions

Questions about pairs or subarrays are a false friend of this pattern. Counting pairs of equal values, or finding the longest subarray with a given sum, looks like a running count. A single scalar cannot answer them, because the new element must be compared with earlier elements and not only with a summary. Such questions need more state, for example a table of values seen so far, which later chapters introduce.

#### Watch Overflow And Integer Division

Java adds two hazards. First, `int` arithmetic wraps around silently. Adding 1 to `Integer.MAX_VALUE` gives `Integer.MIN_VALUE`, so a sum of `int` values needs a `long` accumulator. Second, dividing two integers discards the fraction. An average of `int` values needs one operand converted to `double` before the division.

A third rule concerns empty input. Counts and sums handle an empty array and return 0. A maximum has no valid answer for an empty array, so the contract must say what the method returns or forbid empty input.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum (Author exercise)
<!-- id: ar-maximum -->

**Prerequisites.** Writing a `for` loop and comparing two `int` values.

**Problem.** Given a non-empty integer array `nums`, return the largest value stored in it. The method returns a value from the array, and not an index.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 10^5`.
- **Values** are any `int`, including negative numbers and `Integer.MIN_VALUE`.
- **Return value** is an `int` that equals some element of `nums`.
- **Mutation** is not allowed.

**Example 1.** Input `nums = [-9, -4, -7]`, output -4, since every value is negative and the largest is the one closest to zero.

**Example 2.** Input `nums = [-5]`, output -5, because a single element is its own maximum.

**Hint.** What must the accumulator hold before the loop reads `nums[1]`? Why does starting at 0 fail for negative values?

**Changed decision.** Baseline case: the accumulator starts from the data and not from a constant.

#### [Vary] Find Numbers with Even Number of Digits (LeetCode 1295)
<!-- id: ar-even-digit-count -->

**Prerequisites.** The maximum exercise above.

**Problem.** Given an integer array `nums` of positive values, return how many elements have an even number of decimal digits. The digit count of a value is the length of its decimal representation without leading zeros.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `0 <= nums.length <= 500`.
- **Values** satisfy `1 <= nums[i] <= 10^5`.
- **Return value** is an `int` between 0 and `nums.length`.
- **Empty input** returns 0.

**Example 1.** Input `nums = [10, 100, 1000, 99999, 100000]`, output 3, because 10, 1000 and 100000 have 2, 4 and 6 digits.

**Example 2.** Input `nums = []`, output 0, because no element satisfies the condition.

**Hint.** The condition applies to each element alone. How many times can you divide a value by 10 before it reaches 0?

**Changed decision.** The accumulator changes from an extremum to a count, and it starts at 0 because an empty prefix has no matches.

#### [Boundary] Max Consecutive Ones (LeetCode 485)
<!-- id: ar-max-consecutive-ones -->

**Prerequisites.** The two exercises above.

**Problem.** Given a binary array `bits`, whose values are 0 or 1, return the length of the longest block of consecutive 1 values. A block is a range of adjacent positions in which every value is 1.

**Constraints.** The limits are:
- **`bits`** is an `int[]` with `0 <= bits.length <= 10^5`.
- **Values** are 0 or 1 only.
- **Return value** is an `int`, and 0 means that no 1 occurs.
- **Mutation** is not allowed.

**Example 1.** Input `bits = [1, 0, 1, 1, 1, 0, 1]`, output 3.

**Example 2.** Input `bits = [0, 1, 1]`, output 2, because the longest block touches the end and no zero follows it.

**Hint.** What happens to the current block at a 0? Where in the loop must the best length update so a block at the end is counted?

**Changed decision.** A second accumulator appears: the current block resets at a 0 while the best length keeps its value.

#### [Recognize] Average Salary Excluding the Minimum and Maximum Salary (LeetCode 1491)
<!-- id: ar-trimmed-average -->

**Prerequisites.** The three exercises above.

**Problem.** Given an integer array `salary` with unique values, return the average of the values after one minimum value and one maximum value are removed. Return a `double`. An answer within 10^-5 of the exact value is accepted.

**Constraints.** The limits are:
- **`salary`** is an `int[]` with `3 <= salary.length <= 100`.
- **Values** are unique, with `1000 <= salary[i] <= 10^6`.
- **Return value** is a `double`.
- **Mutation** is not allowed, and the array is not sorted.

**Example 1.** Input `salary = [5000, 1500, 3500, 2500, 9000]`, output about 3666.66667, because 1500 and 9000 are removed and the average of the other three is 11000 divided by 3.

**Example 2.** Input `salary = [7000, 4000, 1000]`, output 4000.0, because only 4000 remains.

**Hint.** Which three scalars does the final formula need? Is sorting required to find them?

**Changed decision.** Three accumulators update together in one pass, so a single scan replaces sorting.
