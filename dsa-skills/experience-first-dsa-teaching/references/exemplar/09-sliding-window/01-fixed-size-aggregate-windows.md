<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-size-aggregate-windows -->
## Fixed-Size Aggregate Windows

<!-- stage: context -->
### The Rolling Total

A web server logs how many requests arrived in each second. The on-call engineer does not care about any single second, which is mostly noise. She cares about the busiest three-second stretch, because that is what the autoscaler reacts to. Her dashboard therefore plots, for every second, the total of that second and the two before it.

The question has a rigid shape. Every candidate is a block of exactly the same length, the blocks sit side by side and overlap, and each block is summarized by one number. The same shape appears in a moving average of stock prices, in the best week of sales within a quarter, and in the number of vowels in every ten-letter stretch of a string.

<!-- stage: naive -->
### Add Up Every Block

The first idea is to take each starting position in turn and add up the `k` values that follow it, writing each total into the answer.

```java
static int[] blockSumsBruteForce(int[] nums, int k) {
    int[] out = new int[nums.length - k + 1];
    for (int start = 0; start + k <= nums.length; start++) {
        int total = 0;
        for (int i = start; i < start + k; i++) {
            total += nums[i];
        }
        out[start] = total;
    }
    return out;
}
```

This is correct, and it reads exactly like the problem statement.

<!-- stage: bottleneck -->
### Re-Reading the Overlap

Look at two neighboring blocks in `[4, 2, 1, 7, 8]` with `k = 3`. The first block is 4, 2, 1 and the second is 2, 1, 7. The values 2 and 1 appear in both, and the method adds them twice. When `k` is large the waste grows, because neighboring blocks share all but one of their values and the method still re-reads every one.

Count the work. There are `n - k + 1` blocks and each costs `k` additions, so the total is `k * (n - k + 1)`. The product is largest when `k` is around half of `n`, where it is about `n^2 / 4`. With `n = 100,000` and `k = 50,000` that is roughly 2.5 billion additions to produce a list of numbers that differ from their neighbors by one value in and one value out. The method uses O(1) extra space beyond the output, and the time is the part that hurts.

<!-- stage: insight -->
### One In, One Out

The block that starts at index 1 is the block that starts at index 0, minus the value at index 0, plus the value at index `k`. Nothing else changed. So the total for the new block is the old total, minus the value that left, plus the value that arrived. That is two operations, whatever the size of `k`.

Think of a train window with a fixed number of seats. Each time the train moves one stop, one passenger gets off at the back and one gets on at the front, and the conductor updates the headcount without recounting the seats. A range that moves one step at a time while keeping its length is called a **fixed-size window**, and the single number we keep up to date for it is its **running aggregate**. Here the aggregate is a sum, but it could be any quantity that can be updated by adding the arrival and undoing the departure.

<!-- names: fixed-size window, running aggregate -->

The idea works because the aggregate has an inverse. A sum can be undone by subtraction, and a count can be undone by decrementing it. A maximum cannot be undone, because once the largest value leaves we do not know the next largest without looking at the others. That limit is why this lesson stays with sums and counts, and why windows that need a maximum belong to a later chapter on deques.

<!-- stage: variables -->
### Three Variables

The index `right` is the position of the newest value in the window. The window covers `right - k + 1` through `right`, so no separate left variable is needed, because its distance from `right` never changes. The variable `total` is the running aggregate and always equals the sum of the values currently in the window. The answer array receives one entry each time the window is full. Until `right` reaches `k - 1` the window has not reached its full size, so nothing is recorded.

<!-- stage: trace -->
### One Run Through

Take `[4, 2, 1, 7, 8, 1, 2, 8, 1, 0]` with `k = 3`. The first three readings, 4, 2 and 1, simply fill the window. The total grows to 7, and since the window now holds three values, 7 is the first entry of the answer.

Now the window slides. Reading 7 arrives while 4 leaves, so the total moves from 7 to 10, because 7 minus 4 is a gain of 3. Reading 8 arrives while 2 leaves, so the total becomes 16. Reading 1 arrives while 1 leaves, and the total stays at 16 because the two values are equal. Notice that the total can stay flat even though the window contents changed.

The rest of the run follows the same pattern. The windows end with totals 11, 11, 11 and 9, and the answer is `[7, 10, 16, 16, 11, 11, 11, 9]`. Eight windows came out of ten values, which matches `n - k + 1`. Each value was added once and subtracted once, and no value was ever summed again from scratch.

```trace
{"cells":[4,2,1,7,8,1,2,8,1,0],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"sum":4,"recorded":0},"note":"Take in index 0 (value 4). The window is not full yet."},{"at":{"left":0,"right":1},"vars":{"sum":6,"recorded":0},"note":"Take in index 1 (value 2). The window is not full yet."},{"at":{"left":0,"right":2},"vars":{"sum":7,"recorded":0},"note":"Take in index 2 (value 1). The window is not full yet."},{"at":{"left":0,"right":2},"vars":{"sum":7,"recorded":1},"note":"The window holds 3 values, so record its sum, 7."},{"at":{"left":1,"right":3},"vars":{"sum":10,"recorded":2},"note":"Add index 3 (value 7), remove index 0 (value 4); the sum becomes 10 and is recorded."},{"at":{"left":2,"right":4},"vars":{"sum":16,"recorded":3},"note":"Add index 4 (value 8), remove index 1 (value 2); the sum becomes 16 and is recorded."},{"at":{"left":3,"right":5},"vars":{"sum":16,"recorded":4},"note":"Add index 5 (value 1), remove index 2 (value 1); the sum becomes 16 and is recorded."},{"at":{"left":4,"right":6},"vars":{"sum":11,"recorded":5},"note":"Add index 6 (value 2), remove index 3 (value 7); the sum becomes 11 and is recorded."},{"at":{"left":5,"right":7},"vars":{"sum":11,"recorded":6},"note":"Add index 7 (value 8), remove index 4 (value 8); the sum becomes 11 and is recorded."},{"at":{"left":6,"right":8},"vars":{"sum":11,"recorded":7},"note":"Add index 8 (value 1), remove index 5 (value 1); the sum becomes 11 and is recorded."},{"at":{"left":7,"right":9},"vars":{"sum":9,"recorded":8},"note":"Add index 9 (value 0), remove index 6 (value 2); the sum becomes 9 and is recorded."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static int[] blockSums(int[] nums, int k) {
    int[] out = new int[nums.length - k + 1];
    int total = 0;
    for (int right = 0; right < nums.length; right++) {
        total += nums[right];                  // the newest value enters
        if (right >= k) total -= nums[right - k];   // the oldest value leaves
        if (right >= k - 1) out[right - k + 1] = total;   // record only when the window is full
    }
    return out;
}
```

The two guards use different thresholds, and the difference matters. The subtraction starts at index `k`, because that is the first moment a value falls out of the window. The recording starts at index `k - 1`, because that is the first moment the window is full. Swapping them gives an answer that is wrong at the start and does not crash, so check both against the trace above.

Every index is added once and subtracted at most once, so the time is O(n) and the extra space is O(1) beyond the output array. The brute force spent `k` operations per window and this spends two, which is the whole improvement.

<!-- stage: applicability -->
### When It Applies

Reach for a fixed-size window when the problem names a block length up front, the candidates are all the blocks of that length, and the summary of a block can be updated by one addition and one undo. The invariant to say out loud is this: before recording, the aggregate equals the summary of exactly the `k` values from `right - k + 1` through `right`.

The false friend is prefix sums. If the problem asks for many independent range queries, where every query has its own endpoints, a prefix table answers each in constant time and a moving window does not help. A window is the natural tool when one pass visits every block of one fixed length. Prefix sums are taught in Chapter 07, and the choice between them is about whether the question is one sweep or many separate lookups.

Java adds one hazard. Sums of many `int` values can overflow, and the standard remedy is to widen the accumulator to `long` when the constraints allow large values or large `k`. Also decide up front what happens when `k` is zero, negative or larger than the array. The loop above would index a negative-length array, so the contract has to say what to return, and an exercise below asks you to state it.

<!-- stage: exercises -->
### Exercises

#### [Build] Sums of Every K-Block (Author exercise)
<!-- id: sw-block-sums -->

**Prerequisites.** Chapter 01 array traversal; this lesson.

**Problem.** Given an integer array `nums` and an integer `k`, return an array whose entry `i` is the sum of the `k` values starting at index `i`. The input must not be modified.

**Constraints.** 1 <= k <= nums.length <= 10^5 and -10^4 <= nums[i] <= 10^4. Target O(n) time and O(1) extra space beyond the returned array.

**Example 1.** Input `nums = [4, 2, 1, 7, 8]`, `k = 3`, output `[7, 10, 16]`.

**Example 2.** Input `nums = [5]`, `k = 1`, output `[5]`, because a single value is one block of size one.

**Hint.** When `right` moves one step, which single value enters and which single value must be taken back out, and at which index does the first removal happen?

**Changed decision.** First rung of the ladder: introduces the running aggregate and the two different start thresholds.

#### [Vary] Maximum Average Subarray I (LeetCode 643)
<!-- id: sw-max-average -->

**Prerequisites.** The block-sum exercise above.

**Problem.** Among all contiguous blocks of exactly `k` readings in `nums`, find the block with the highest mean and return that mean as a `double`.

**Constraints.** n == nums.length, 1 <= k <= n <= 10^5, -10^4 <= nums[i] <= 10^4. An answer within 10^-5 of the true value is accepted.

**Example 1.** Input `nums = [3, -1, 4, 1, 5]`, `k = 2`, output `3.0`, from the block `[1, 5]`.

**Example 2.** Input `nums = [-8, -3, -6]`, `k = 2`, output `-4.5`. Every block sum is negative, so a starting `best` of zero would be wrong.

**Hint.** Do you need to keep the average of every block, or only one number per block? Which value must `best` start from so negative sums still work?

**Changed decision.** The output changes from a list of every sum to one best value, and the division moves out of the loop to a single use at the end.

#### [Boundary] Whole-Array Window (Author exercise)
<!-- id: sw-whole-array-window -->

**Prerequisites.** The two exercises above.

**Problem.** Write the block-sum method with an explicit contract for bad input. If `k` is less than 1 or greater than `nums.length`, return an empty array. Otherwise return the sum of every block of size `k`.

**Constraints.** 0 <= nums.length <= 10^5, -10^9 <= nums[i] <= 10^9, and `k` is any int. Sums can exceed the range of `int`, so the result type is `long[]`. Target O(n) time.

**Example 1.** Input `nums = [3, 1, 4]`, `k = 3`, output `[8]`. The window is the whole array and is recorded exactly once.

**Example 2.** Input `nums = [3, 1, 4]`, `k = 4`, output `[]`. The block is longer than the array, so no window exists.

**Hint.** Where should the check for a bad `k` sit relative to the allocation of the output array, and which type must the running total have when values reach 10^9?

**Changed decision.** The window may consume the entire input, and the contract for impossible sizes is stated instead of left to a crash.

#### [Recognize] Maximum Number of Vowels in a Substring of Given Length (LeetCode 1456)
<!-- id: sw-max-vowels -->

**Prerequisites.** The three exercises above.

**Problem.** Look at every window of `k` consecutive letters in the string `s` and count the vowels (`a`, `e`, `i`, `o`, `u`) in it. Return the largest count over all windows.

**Constraints.** 1 <= s.length <= 10^5, `s` consists of lowercase English letters, and 1 <= k <= s.length. Target O(n) time and O(1) extra space.

**Example 1.** Input `s = "queueing"`, `k = 3`, output `3`, from the window `"ueu"`.

**Example 2.** Input `s = "rhythms"`, `k = 4`, output `0`. No window contains a vowel, so the answer must not be reported as `k`.

**Hint.** What does each character contribute to the aggregate when it enters and when it leaves, and can you answer that without building any substring?

**Changed decision.** The aggregate changes from a numeric sum to a Boolean contribution per character, so one helper decides what each entering and leaving letter adds.

#### [Extend] Grumpy Bookstore Owner (LeetCode 1052)
<!-- id: sw-grumpy-owner -->

**Prerequisites.** The four exercises above.

**Problem.** In minute `i`, `customers[i]` people walk into a shop. When `grumpy[i]` is 1 the owner turns them all away, and when it is 0 they are served. Once during the day the owner can stay calm for exactly `minutes` consecutive minutes and serve everyone who arrives in them. Return the largest number of customers that can be served.

**Constraints.** n == customers.length == grumpy.length, 1 <= minutes <= n <= 2 * 10^4, 0 <= customers[i] <= 1000, and grumpy[i] is 0 or 1.

**Example 1.** Input `customers = [2, 3, 1, 4, 2]`, `grumpy = [1, 0, 1, 1, 0]`, `minutes = 2`, output `10`. Five customers are served anyway, and calming minutes 2 and 3 adds five more.

**Example 2.** Input `customers = [5, 1]`, `grumpy = [1, 1]`, `minutes = 1`, output `5`. The owner is grumpy throughout, so the calm minute should go to the larger crowd.

**Hint.** Some customers are satisfied no matter what you do. Which extra customers does a calm window gain, and how can you keep that gain as the running aggregate of a fixed window?

**Changed decision.** The aggregate is a gain that counts only the grumpy minutes inside the window, added to a baseline that never changes.
