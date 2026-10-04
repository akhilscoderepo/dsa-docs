<!-- lesson-kind: standard -->
<!-- lesson-id: running-extremum-and-best-gain -->
## Running Extremum And Best Gain

<!-- stage: context -->
### Why Adjacent Days Miss The Best Trade

A price analyst stores daily closing prices of one product in an `int[]` and reports the largest profit from buying on one day and selling on a later day. The first version of the tool compares each day with the next day and reports the biggest jump. For the prices `[4, 2, 6, 5, 9]` it reports 4. A trader who buys at 2 and sells at 9 earns 7, so the tool understates the true answer.

The tool failed because the best buy day and the best sell day are often far apart. Everything between them can go up and down without changing the result. The question is how a single pass can find the best pair while it remembers almost nothing, and what answer the tool must give when every price falls.

<!-- stage: naive -->
### Trying Every Buy Day And Sell Day

The safe reading of the question is a definition. A profit belongs to a pair of days, where the buy day comes first. A method can compute the profit of every such pair and keep the largest.

```java
static int maxProfitPairs(int[] prices) {
    int answer = 0;
    for (int buy = 0; buy < prices.length; buy++) {
        for (int sell = buy + 1; sell < prices.length; sell++) {
            answer = Math.max(answer, prices[sell] - prices[buy]);
        }
    }
    return answer;
}
```

The method is correct, and it starts `answer` at 0 so that a falling market returns 0. It checks every pair, so it also repeats a lot of work.

<!-- stage: bottleneck -->
### Recomputing The Cheapest Earlier Day

```predict
For 100,000 daily prices, about how many pairs does `maxProfitPairs` examine, and what does the inner loop re-learn for each sell day?

About five billion pairs, since the count is n(n - 1) / 2. For a fixed sell day, the inner loop in effect re-searches all earlier days to find the cheapest one, although the previous sell day already searched almost the same days.
```

Fix one sell day. The best buy day for that sell day is the day with the lowest price before it. The brute force finds that day by trying every buy day, and it repeats the search for the next sell day over almost the same set of days. The cost is O(n^2) time.

The set of earlier days grows by exactly one day when the sell day moves forward by one. The cheapest price over a set changes only if the new day is cheaper than the old cheapest price. One remembered number is enough, so the pair search can shrink to O(n) time.

<!-- stage: insight -->
### One Remembered Minimum Gives Every Pair

#### Remember The Lowest Price So Far

The **running minimum** is the smallest value among the positions already read. Before the loop reads `nums[i]`, the running minimum equals the minimum of `nums[0..i-1]`. The method names it `lowestSoFar`. It changes only when the current value is smaller.

#### Score Each Sell Day Against It

For the current position, the best partner on an **earlier position** is the one holding the running minimum. The profit of the best pair that ends at `i` is `nums[i] - lowestSoFar`. The method computes this gain before it updates the minimum, so the current value never pairs with itself.

#### Keep The Best Gain

The **best gain** is the largest profit seen at any position. It starts at 0, because the contract allows no trade and answers 0 when no pair earns a positive profit. After each position the best gain is the largest profit over all pairs inside `nums[0..i]`. Each pair has its sell day at some position, and the scan scores that position against the best buy day, so no pair is missed.

<!-- names: running minimum, earlier position, best gain -->

#### Separate It From A Contiguous Block

The scan pairs two positions and ignores everything between them. A contiguous-block question, such as the best sum of adjacent days, asks about the whole range between the endpoints. That question needs a different state, which a later lesson in this chapter introduces.

<!-- stage: variables -->
### Name The Two State Variables

Write the contract for the answer before choosing the starting values.

- **`lowestSoFar`** is the minimum of `nums[0..i-1]`, and it starts as `nums[0]` with the loop beginning at index 1.
- **`bestGain`** is the largest `nums[j] - nums[k]` over positions `k < j < i`, and it starts at 0 because the contract allows no trade.
- **`gain`** is the profit of selling at `i` against `lowestSoFar`, and it is computed from the old minimum before the update.

The update order is fixed. Compute the gain first, update `bestGain`, and only then update `lowestSoFar`.

<!-- stage: trace -->
### Trace A Rising And A Falling Case

The first trace uses `[9, 4, 6, 3, 8, 5]`. The minimum starts at 9. At `i = 1` the value 4 gives a negative gain, so `bestGain` stays 0, and the minimum drops to 4. At `i = 2` the value 6 gives a gain of 2, so `bestGain` becomes 2. At `i = 3` the value 3 gives a negative gain and becomes the new minimum. At `i = 4` the value 8 gives a gain of 5 against the minimum 3. At `i = 5` the value 5 gives a gain of 2. The final answer is 5, from the minimum 3 paired with the value 8. The values between those two positions do not affect it.

The second trace uses the strictly falling prices `[8, 6, 5, 2]`. Every gain is negative, so `bestGain` never leaves 0, while the minimum follows the falling prices down to 2. The hard step is the last one, because the value 2 produces the lowest price of the array and still no profit. The answer is 0 by contract, and no negative number and no `-1` is returned.

```trace
{"cells":[9,4,6,3,8,5],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"lowestSoFar":9,"bestGain":0},"note":"Start: lowestSoFar is 9, bestGain is 0, and the loop begins at index 1."},{"at":{"i":1},"vars":{"lowestSoFar":4,"bestGain":0},"note":"i = 1: selling at 4 against the old minimum gives -5. bestGain is 0, lowestSoFar is 4."},{"at":{"i":2},"vars":{"lowestSoFar":4,"bestGain":2},"note":"i = 2: selling at 6 against the old minimum gives 2. bestGain is 2, lowestSoFar is 4."},{"at":{"i":3},"vars":{"lowestSoFar":3,"bestGain":2},"note":"i = 3: selling at 3 against the old minimum gives -1. bestGain is 2, lowestSoFar is 3."},{"at":{"i":4},"vars":{"lowestSoFar":3,"bestGain":5},"note":"i = 4: selling at 8 against the old minimum gives 5. bestGain is 5, lowestSoFar is 3."},{"at":{"i":5},"vars":{"lowestSoFar":3,"bestGain":5},"note":"i = 5: selling at 5 against the old minimum gives 2. bestGain is 5, lowestSoFar is 3."},{"at":{"i":6},"vars":{"lowestSoFar":3,"bestGain":5},"note":"The loop ends. The answer is 5."}]}
```

```trace
{"cells":[8,6,5,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"lowestSoFar":8,"bestGain":0},"note":"Start: lowestSoFar is 8, bestGain is 0, and the loop begins at index 1."},{"at":{"i":1},"vars":{"lowestSoFar":6,"bestGain":0},"note":"i = 1: selling at 6 against the old minimum gives -2. bestGain is 0, lowestSoFar is 6."},{"at":{"i":2},"vars":{"lowestSoFar":5,"bestGain":0},"note":"i = 2: selling at 5 against the old minimum gives -1. bestGain is 0, lowestSoFar is 5."},{"at":{"i":3},"vars":{"lowestSoFar":2,"bestGain":0},"note":"i = 3: selling at 2 against the old minimum gives -3. bestGain is 0, lowestSoFar is 2."},{"at":{"i":4},"vars":{"lowestSoFar":2,"bestGain":0},"note":"The loop ends. The answer is 0."}]}
```

<!-- stage: code -->
### Write The Gain Scan And Its Mirror

```java
static int bestGain(int[] nums) {
    if (nums.length == 0) return 0;
    int lowestSoFar = nums[0];
    int bestGain = 0;
    for (int i = 1; i < nums.length; i++) {
        bestGain = Math.max(bestGain, nums[i] - lowestSoFar);
        lowestSoFar = Math.min(lowestSoFar, nums[i]);
    }
    return bestGain;
}

static long bestGainWide(int[] nums) {
    if (nums.length == 0) return 0;
    int lowestSoFar = nums[0];
    long bestGain = 0;
    for (int i = 1; i < nums.length; i++) {
        bestGain = Math.max(bestGain, (long) nums[i] - lowestSoFar);
        lowestSoFar = Math.min(lowestSoFar, nums[i]);
    }
    return bestGain;
}

static int largestDrop(int[] nums) {
    if (nums.length == 0) return 0;
    int highestSoFar = nums[0];
    int bestDrop = 0;
    for (int i = 1; i < nums.length; i++) {
        bestDrop = Math.max(bestDrop, highestSoFar - nums[i]);
        highestSoFar = Math.max(highestSoFar, nums[i]);
    }
    return bestDrop;
}
```

The three methods share one shape. The first line of the loop body scores position `i` against the remembered extremum, and the second line updates the extremum afterwards. `largestDrop` mirrors `bestGain`: the minimum becomes a maximum, and the subtraction swaps its operands. The wide version casts one operand to `long` before subtracting, because the difference of two `int` values can exceed the range of `int`. All three methods run in O(n) time and O(1) space.

<!-- stage: applicability -->
### Check The Pair Contract Before Scanning

#### Recognize A Pair With Fixed Order

Use this scan when the answer is the best difference between two positions, the first of the two must come first, and the positions need not touch. The invariant is that `lowestSoFar` equals the minimum of `nums[0..i-1]` before the loop reads `nums[i]`. A mirror question that wants the largest earlier value minus a later value keeps a running maximum instead.

#### Reject Block And Multi-Trade Questions

Kadane's algorithm, which finds the best contiguous block, looks similar because it also scans once and keeps a running value. It is a false friend here. It sums every element between two endpoints, while this scan uses only the two endpoint values. A question that allows several trades is also outside the pattern. Selling and buying again changes the state, so one remembered minimum no longer describes the optimum. A question that limits the distance between the two days needs a window of recent values, so a single minimum fails there too.

#### Watch The Starting Values

Java adds a hazard when the code starts `lowestSoFar` at `Integer.MAX_VALUE`. Subtracting that constant from a negative value can wrap around and produce a large positive gain. Starting from `nums[0]` avoids the problem. A difference between two `int` values can also exceed `int` range, so wide inputs need a `long` difference.

The contract decides the empty case and the falling case. State both before writing the initial value of `bestGain`. This lesson returns 0 for an empty array, for one price, and for prices that never rise.

<!-- stage: exercises -->
### Exercises

#### [Build] Best Time to Buy and Sell Stock (LeetCode 121)
<!-- id: ar-best-time-buy-sell -->

**Prerequisites.** The maximum scan from the previous lesson.

**Problem.** Given an integer array `prices`, where `prices[i]` is the price on day `i`, choose one buy day and one later sell day. Return the largest possible profit, which is the sell price minus the buy price. If no trade earns a positive profit, return 0.

**Constraints.** The limits are:
- **`prices`** is an `int[]` with `1 <= prices.length <= 10^5`.
- **Values** satisfy `0 <= prices[i] <= 10^4`.
- **Order** requires the sell day to be later than the buy day.
- **Return value** is an `int` that is never negative.

**Example 1.** Input `prices = [9, 4, 6, 3, 8, 5]`, output 5, which buys at 3 and sells at 8.

**Example 2.** Input `prices = [5]`, output 0, because one day has no later day to sell on.

**Hint.** For a fixed sell day, which single earlier price gives the best profit? What can you remember so that you do not search for it?

**Changed decision.** Baseline case: one remembered minimum replaces the inner loop over all earlier days.

#### [Vary] Largest Drop (Author exercise)
<!-- id: ar-largest-drop -->

**Prerequisites.** The best-time-to-buy exercise above.

**Problem.** Take an integer array `nums` and every pair of positions `i < j`. Return the maximum of `nums[i] - nums[j]` over those pairs, or 0 if no pair has a positive difference.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `0 <= nums.length <= 10^5`.
- **Values** satisfy `-10^4 <= nums[i] <= 10^4`.
- **Order** requires `i < j`, so the larger term comes from the earlier position.
- **Return value** is an `int` that is never negative.

**Example 1.** Input `nums = [3, 9, 4, 1, 6]`, output 8, because 9 comes before 1.

**Example 2.** Input `nums = [1, 2, 3]`, output 0, because every earlier value is smaller than every later value.

**Hint.** Which remembered value makes `nums[i] - nums[j]` as large as possible for a fixed `j`? Does the update order stay the same?

**Changed decision.** The remembered extremum becomes a running maximum, and the subtraction swaps its operands.

#### [Boundary] No Profitable Pair (Author exercise)
<!-- id: ar-no-profitable-pair -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `values`, return the largest value of `values[j] - values[i]` over pairs with `i < j`, as a `long`. The contract says to return 0 when every such difference is zero or negative, and when the array has fewer than two elements. A falling array therefore returns 0, and it does not return a negative number or -1.

**Constraints.** The limits are:
- **`values`** is an `int[]` with `0 <= values.length <= 10^5`.
- **Values** can be any `int`, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Return value** is a `long` that is never negative.
- **Ties** between equal values give a difference of 0.

**Example 1.** Input `values = [9, 7, 4, 3]`, output 0, because every pair loses value.

**Example 2.** Input `values = [-2000000000, 2000000000]`, output 4000000000, which exceeds the range of `int`.

**Hint.** What does the answer mean when nothing improves, and which value of `bestGain` encodes it? In which type should the subtraction happen?

**Changed decision.** The scan states its empty and falling answers before it starts, and the difference widens to `long`.

#### [Recognize] Best Time to Buy and Sell Stock II (LeetCode 122)
<!-- id: ar-buy-sell-many -->

**Prerequisites.** The three exercises above.

**Problem.** Given an integer array `prices`, where `prices[i]` is the price on day `i`, you may buy and sell any number of times. You hold at most one share at a time, and you may sell and buy again on the same day. Return the largest total profit.

**Constraints.** The limits are:
- **`prices`** is an `int[]` with `1 <= prices.length <= 10^5`.
- **Values** satisfy `0 <= prices[i] <= 10^4`.
- **Holding** allows at most one share at any time.
- **Return value** is an `int` that is never negative, and 0 means no trade helps.

**Example 1.** Input `prices = [4, 1, 3, 2, 6, 5]`, output 6, from buying at 1 and selling at 3, then buying at 2 and selling at 6.

**Example 2.** Input `prices = [9, 6, 3]`, output 0, because the price never rises.

**Hint.** With many trades allowed, does a single remembered minimum still describe the best plan? What does each rise between two neighboring days contribute?

**Changed decision.** The state changes from a running minimum to day-to-day differences, so this problem is a false friend of the lesson's own pattern.
