<!-- lesson-kind: standard -->
<!-- lesson-id: product-state -->
## Product State

<!-- stage: context -->
### Finding The Best Run Of Growth Factors

A pricing service stores a growth factor for each day. A factor of 3 triples a value, a factor of -2 flips its sign and doubles its size, and a factor of 0 wipes it out. An analyst asks for the contiguous run of days with the largest product of factors. The run must contain at least one day.

For the array `[2, 3, -2, 4]` the answer is 6, from the run `2, 3`. The sum version of this question has a short one-pass solution, so an engineer tries to reuse it. The reused solution returns a wrong answer on `[-2, 3, -4]`, where the right answer is 24. The question for this lesson is why the sum method breaks and what extra memory repairs it.

<!-- stage: naive -->
### Multiplying Every Subarray With A Running Product

The direct method tries every start index. For each start it extends the end index one step at a time and keeps a running product. It records the largest product it sees.

```java
static int bruteMaxProduct(int[] nums) {
    int best = nums[0];
    for (int start = 0; start < nums.length; start++) {
        int product = 1;
        for (int end = start; end < nums.length; end++) {
            product *= nums[end];
            best = Math.max(best, product);
        }
    }
    return best;
}
```

This method is correct for every sign pattern, because it checks every subarray. It starts `best` at the first element, so an array such as `[-4]` still returns a real product. It takes O(n^2) time and O(1) extra space, which is too slow for an array of 20,000 values.

<!-- stage: bottleneck -->
### Why One Ending Value Is Not Enough

```predict
Apply the sum recurrence to products on `[-2, 3, -4]`: keep one value, the best product of a subarray ending at the current index, and update it with `max(x, previous * x)`. What does it return, and what is the true answer?

It returns 3. The ending value is -2 at index 0, then 3 at index 1, then max(-4, 3 * -4) = -4 at index 2, and the best seen is 3. The true answer is 24, from the whole array, because -2 * 3 * -4 = 24. The single value threw away -6, and -6 times -4 is the largest product.
```

The method above takes O(n^2) time, and the one-value shortcut takes O(n) time but returns wrong answers. The shortcut fails because multiplication by a negative number reverses the order of values. The smallest product ending at an index, such as -6, becomes the largest product after one more negative value. The sum recurrence never has this problem, because adding a number keeps the order of the old sums.

The wrong result comes from a discarded value, not from a missing loop. A correct method must keep the smallest ending product too, because that value can become the largest on the next negative. Keeping both values makes each step O(1), and the whole pass stays O(n).

<!-- stage: insight -->
### Keeping Both Ending Products

#### State At Each Index

The scan keeps three values. The value `maxEndingHere` is the largest product of a non-empty subarray that ends at the current index. The value `minEndingHere` is the smallest product of a non-empty subarray that ends at the current index. The value `bestOverall` is the largest `maxEndingHere` seen so far, and it is the answer after the last index.

<!-- names: maxEndingHere, minEndingHere, bestOverall -->

#### Recurrence For Both Products

A subarray that ends at index `i` is either the single value `x = nums[i]`, or a longer subarray that ends at `i - 1` multiplied by `x`. A longer subarray has the largest product `maxEndingHere * x` or the smallest product `minEndingHere * x` as its extreme, because the extreme of `x` times a set of values sits at one end of that set. A positive `x` keeps the order, so the largest product extends the largest. A negative `x` reverses the order, so the smallest product extends into the new largest, and the roles of the two values swap. A zero makes every candidate 0, so both values become 0, and the next index can start a fresh subarray.

The update takes three candidates, `x`, `maxEndingHere * x` and `minEndingHere * x`. The new `maxEndingHere` is the largest candidate, and the new `minEndingHere` is the smallest candidate. Both new values read the old values, so the update must not overwrite one before the other uses it.

#### Why The Invariant Holds

After every index, the two values equal the true largest and smallest products of subarrays ending there. The candidate list contains every possible shape of an ending subarray, and taking the extreme of the extremes gives the extreme of all of them. `bestOverall` takes the maximum across all ending indices, so it equals the answer.

<!-- stage: variables -->
### Meaning And Update Time Of Each Variable

The scan keeps three variables, and a loop index `i` moves from left to right.

- **`maxEndingHere`** holds the largest product ending at `i`, and it changes at every index.
- **`minEndingHere`** holds the smallest product ending at `i`, and it changes at every index.
- **`bestOverall`** holds the largest `maxEndingHere` seen so far, and it changes only when a new value beats it.
- **Candidate trio** is `x`, `maxEndingHere * x` and `minEndingHere * x`, computed from the old values before either variable changes.

All three variables start at `nums[0]`, because the first index has only one subarray.

<!-- stage: trace -->
### Tracing Sign Changes And A Swap

The first trace follows `[2, 3, -2, 4]`. At index 0 all values equal 2. At index 1 the value is 3, so the candidates are 3, 6 and 6, and both ending products become 6 and 3 in the right order: the largest is 6 and the smallest is 3. At index 2 the value is -2 and the candidates are -2, -12 and -6, so the largest ending product drops to -2 and the smallest falls to -12. The negative value swapped the roles, and the old largest value became the new smallest. At index 3 the value is 4 and the candidates are 4, -8 and -48. The largest is 4 and the smallest is -48. `bestOverall` stays at 6 through the whole pass.

```trace
{"cells":[2,3,-2,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"maxEndingHere":2,"minEndingHere":2,"bestOverall":2},"note":"Index 0 holds 2. All three values start at 2."},{"at":{"i":1},"vars":{"maxEndingHere":6,"minEndingHere":3,"bestOverall":6},"note":"Index 1 holds 3. The candidates are 3, 6 and 6. The largest is 6 and the smallest is 3. bestOverall is 6."},{"at":{"i":2},"vars":{"maxEndingHere":-2,"minEndingHere":-12,"bestOverall":6},"note":"Index 2 holds -2. The candidates are -2, -12 and -6. The largest is -2 and the smallest is -12. The negative value reverses the order, so the old smallest product feeds the new largest. bestOverall is 6."},{"at":{"i":3},"vars":{"maxEndingHere":4,"minEndingHere":-48,"bestOverall":6},"note":"Index 3 holds 4. The candidates are 4, -8 and -48. The largest is 4 and the smallest is -48. bestOverall is 6."}]}
```

The second trace follows `[-2, 3, -4]`, the array that breaks the one-value shortcut. The smallest ending product -6 at index 1 becomes the largest ending product 24 at index 2 after the negative value. The answer is 24.

```trace
{"cells":[-2,3,-4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"maxEndingHere":-2,"minEndingHere":-2,"bestOverall":-2},"note":"Index 0 holds -2. All three values start at -2."},{"at":{"i":1},"vars":{"maxEndingHere":3,"minEndingHere":-6,"bestOverall":3},"note":"Index 1 holds 3. The candidates are 3, -6 and -6. The largest is 3 and the smallest is -6. bestOverall is 3."},{"at":{"i":2},"vars":{"maxEndingHere":24,"minEndingHere":-12,"bestOverall":24},"note":"Index 2 holds -4. The candidates are -4, -12 and 24. The largest is 24 and the smallest is -12. The negative value reverses the order, so the old smallest product feeds the new largest. bestOverall is 24."}]}
```

<!-- stage: code -->
### Writing The Two-State Pass In Java

```java
static int maxProduct(int[] nums) {
    int maxEndingHere = nums[0];
    int minEndingHere = nums[0];
    int bestOverall = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        int fromMax = maxEndingHere * x;
        int fromMin = minEndingHere * x;
        maxEndingHere = Math.max(x, Math.max(fromMax, fromMin));
        minEndingHere = Math.min(x, Math.min(fromMax, fromMin));
        bestOverall = Math.max(bestOverall, maxEndingHere);
    }
    return bestOverall;
}
```

The two local variables `fromMax` and `fromMin` hold the old products, so the second assignment does not read an already changed `maxEndingHere`. The method takes O(n) time and O(1) extra space. The Java hazard is overflow. The product of many values outgrows `int` quickly, so the method relies on the guarantee that every subarray product fits in a 32-bit integer. Without that guarantee, use `long` and check the limits.

<!-- stage: applicability -->
### Checking Whether Two States Are Needed

#### Conditions For Using Product State

Use two ending states when the objective is a contiguous product and the values can be negative. The invariant is that the two values bracket every product of an ending subarray, from the smallest to the largest. A negative value swaps their roles. A zero resets both. The idea also carries to other objectives where a negative reverses the useful order, such as the longest run with a positive product, where the stored state becomes a length for each sign.

#### False Friend And No-Go Conditions

The sum version of this problem is a false friend. It looks identical, since both ask for the best contiguous run, but addition does not reverse order, so one ending state is enough. Copying that code into a product problem returns wrong answers whenever two negatives appear.

Do not keep two states when all values are positive, because the largest product is the product of the whole array and one value suffices. Do not use this recurrence when the product can overflow and the problem gives no bound, because the intermediate values then need `long` or big integers.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Product Subarray (LeetCode 152)
<!-- id: ar-max-product -->

**Prerequisites.** The two-state recurrence from this lesson.

**Problem.** Given an integer array `nums`, return the largest product over all non-empty contiguous subarrays of `nums`.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 2 * 10^4`.
- **Values** satisfy `-10 <= nums[i] <= 10`.
- **Overflow** is excluded, because every subarray product fits in a 32-bit signed integer.
- **Subarray** is non-empty, so a single element qualifies.

**Example 1.** Input `[3, -1, 4, -2, -5]`, output 40, from the run `4, -2, -5`.

**Example 2.** Input `[-4, 0, -1]`, output 0, from the single value 0, since every longer run is negative or includes 0.

**Hint.** Which earlier product could become the largest after a negative value?

**Changed decision.** Baseline case: the single ending state of the sum problem becomes two, because a negative reverses the order of products.

#### [Vary] Product Ending Here (Author exercise)
<!-- id: ar-product-ending-here -->

**Prerequisites.** The maximum product exercise above.

**Problem.** Given an integer array `nums`, return the largest product over all non-empty subarrays that end at the last index of `nums`.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 2 * 10^4`.
- **Values** satisfy `-10 <= nums[i] <= 10`.
- **Overflow** is excluded, because every subarray product fits in a 32-bit signed integer.
- **Required end** is the last index, so the subarray must include the final item.

**Example 1.** Input `[1, -2, -3, 4]`, output 24, from the whole array.

**Example 2.** Input `[-3, 0, -5]`, output 0, from the run `0, -5`.

**Hint.** Do you still need to remember the best product seen at earlier indices, or only the two ending values?

**Changed decision.** The global best disappears, but both ending values remain, since the last index still depends on the smallest product before it.

#### [Boundary] Zero And Negative Trace (Author exercise)
<!-- id: ar-product-zero-negative-trace -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums`, return a table with one row per index. Row `i` holds the pair of `maxEndingHere` and `minEndingHere` after index `i`. State the maximum product as the largest first entry in the table.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 100`.
- **Values** satisfy `-10 <= nums[i] <= 10` and may include zero.
- **Return value** is an `int[n][2]` table with the maximum first and the minimum second.

**Example 1.** Input `[-2, 3, -4]`, output rows `[-2, -2]`, `[3, -6]`, `[24, -12]`, so the maximum product is 24.

**Example 2.** Input `[0, -2]`, output rows `[0, 0]`, `[0, -2]`, so the maximum product is 0.

**Hint.** What do the three candidates equal when the new value is zero?

**Changed decision.** The dry run exposes the two special values: a zero resets both states, and a negative swaps their roles.

#### [Recognize] Longest Positive Product Run (LeetCode 1567)
<!-- id: ar-positive-product-length -->

**Prerequisites.** The zero and negative dry run above.

**Problem.** Given an integer array `nums`, return the length of the longest subarray whose product is positive. Return 0 when no such subarray exists.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 10^5`.
- **Values** satisfy `-10^9 <= nums[i] <= 10^9`.
- **Product** is never computed, so overflow cannot occur.
- **Return value** is a length, which is 0 when every candidate fails.

**Example 1.** Input `[-1, -2, -3, 0, 2]`, output 2, from the run `-1, -2`.

**Example 2.** Input `[2, -2, -3, 0, 5]`, output 3, from the run `2, -2, -3`.

**Hint.** Store the length of the longest run that ends here with a positive product and the longest with a negative product.

**Changed decision.** The stored state changes from products to lengths per sign, but a negative value still swaps the two histories.
