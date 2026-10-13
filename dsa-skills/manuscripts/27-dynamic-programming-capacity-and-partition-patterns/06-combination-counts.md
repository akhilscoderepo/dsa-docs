<!-- lesson-kind: standard -->
<!-- lesson-id: combination-counts -->
## Combination Counts

<!-- stage: context -->
### Listing Change Breakdowns For A Cashier

A cashier app shows every distinct way to pay 5 units with coins of 1, 2 and 5. Cashiers read the list to pick a breakdown that matches the coins in the drawer. The correct list has four entries: 5, then 2 + 2 + 1, then 2 + 1 + 1 + 1, then five coins of 1. The app shows nine entries, because it lists 1 + 2 + 2, 2 + 1 + 2 and 2 + 2 + 1 as three different breakdowns. A cashier cannot tell which entries are duplicates.

The inputs are an array `coins` of distinct positive integers and a nonnegative integer `amount`. A **combination** is a choice of how many times each denomination is used, and the order of the coins does not matter. Two combinations are equal when every denomination is used the same number of times. The task is to count the combinations whose values add up to `amount`. A combination with no coins adds up to 0, so amount 0 has exactly one combination. The method never changes the array.

This lesson asks how to count each combination once without listing them.

<!-- stage: naive -->
### Extending The Fewest-Coins Loop

The quick idea reuses the loop from the first lesson of this chapter. The outer loop walks the amounts upward, and the inner loop tries each denomination as the last coin. The table adds the counts instead of taking the minimum.

```java
static long countByAmounts(int[] coins, int amount) {
    long[] ways = new long[amount + 1];
    ways[0] = 1;
    for (int a = 1; a <= amount; a++) {
        for (int coin : coins) {
            if (coin <= a) ways[a] += ways[a - coin];
        }
    }
    return ways[amount];
}
```

The method runs in O(amount * k) time for k denominations and uses O(amount) memory. The structure matches a correct table for the fewest coins. The open question is whether adding counts in this loop order counts each breakdown once.

```predict
Run countByAmounts on the coins [1, 2, 5] with amount 5. What does it return, and how many distinct combinations exist?

It returns 9, and only 4 combinations exist. The method counts 1 + 2 + 2, 2 + 1 + 2 and 2 + 2 + 1 as three separate entries, because each order reaches amount 5 through a different last coin. A count that depends on the order of the coins is a count of sequences.
```

<!-- stage: bottleneck -->
### The Last Coin Fixes The Order

The entry for amount `a` adds `ways[a - coin]` for every denomination. The breakdown with the coins 1, 2 and 2 can be laid down in three orders, and the table follows a separate path for each order, so it adds 3 to the count. The table does not remember which coins came before the last one, so it cannot merge those paths.

A correct but slow method lists the combinations by choosing a count for each denomination. With k denominations and amount `A`, the number of count vectors grows like A^k divided by k! and by the product of the denominations, so it is O(A^k) in the worst case. For the denominations 1 through 8 and amount 600, there are about 1.7 * 10^11 combinations, so listing them one by one is too slow.

The fix is to lay down the coins in a fixed order so that each combination has exactly one path through the table. If all uses of the first denomination come before all uses of the second, no reordering is possible. A table that processes one denomination at a time follows this rule and needs O(amount * k) time. The next section shows how.

<!-- stage: insight -->
### Count Coins In One Fixed Order

Every combination can be written down in many orders, and only one of them matters for counting. Choose a single writing order and count writings in that order only.

<!-- names: canonical order, one coin at a time, empty combination -->

#### Write Each Combination In Canonical Order

Number the denominations by their position in the array. The **canonical order** of a combination lists all copies of denomination 0 first, then all copies of denomination 1, and so on. Every combination has exactly one canonical writing, and two different combinations have different writings. So the number of combinations equals the number of canonical writings, and a table that follows the canonical order counts each combination once.

#### Add One Coin At A Time

Let `ways[a]` be the number of combinations that add up to `a` using only the denominations processed so far. The method processes **one coin at a time**, in array order. When it adds denomination `c`, a combination for amount `a` either uses no copy of `c`, which the old `ways[a]` already counts, or uses at least one. Remove the last copy of `c` from the canonical writing. What remains is a combination for `a - c` that uses denominations up to and including `c`, so its count is `ways[a - c]` after `c` has already updated that smaller amount. So the update is `ways[a] += ways[a - c]`, with `a` increasing from `c` to `amount`.

#### Seed The Table With The Empty Combination

The **empty combination** uses no coins and adds up to 0. It is the one combination for amount 0, so `ways[0]` is 1 before any denomination is processed. Every other combination grows from it by appending copies of a denomination. Without this seed, every entry stays 0. The invariant is that after denomination `c` finishes, `ways[a]` counts the combinations of `a` that use only the denominations processed so far. The answer is `ways[amount]`.

<!-- stage: variables -->
### Counts For Each Amount

The inputs `coins` and `amount` stay unchanged, and the method keeps these values.

- **ways** is a `long[]` of length `amount + 1`; entry `a` counts the combinations that add up to `a`.
- **coin** is the denomination that the outer loop adds.
- **a** is the amount that the inner loop updates, from `coin` up to `amount`.
- **ways[0]** is the seed 1 for the empty combination.

The counts are `long` values, because the number of combinations grows quickly with the amount. For the denominations 1 through 8 and amount 600, the count passes the `int` range. The denominations must be distinct. A repeated value would act as two denominations and count its combinations twice.

<!-- stage: trace -->
### Two Runs With The Same Coins

#### Coins In The Outer Loop

The first run uses the coins 1, 2 and 5 and amount 5. Each cell is an amount from 0 to 5, and the pointer `a` marks the entry that changes. The variable `coin` is the denomination being added, `add` is the amount added to the entry, and `ways` is the entry after the update. The first step shows the seed.

The coin 1 gives every amount one combination. The coin 2 then raises the counts for amounts 2 to 5 to 2, 2, 3 and 3. The coin 5 adds one combination for amount 5, which makes the final count 4. The combinations are 5, 2 + 2 + 1, 2 + 1 + 1 + 1 and 1 + 1 + 1 + 1 + 1.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["a"],"steps":[{"at":{"a":0},"vars":{"coin":0,"add":0,"ways":1},"note":"The seed is the empty combination, so the count for amount 0 is 1."},{"at":{"a":1},"vars":{"coin":1,"add":1,"ways":1},"note":"Adding the coin 1, amount 1 gains 1 from amount 0, so its count becomes 1."},{"at":{"a":2},"vars":{"coin":1,"add":1,"ways":1},"note":"Adding the coin 1, amount 2 gains 1 from amount 1, so its count becomes 1."},{"at":{"a":3},"vars":{"coin":1,"add":1,"ways":1},"note":"Adding the coin 1, amount 3 gains 1 from amount 2, so its count becomes 1."},{"at":{"a":4},"vars":{"coin":1,"add":1,"ways":1},"note":"Adding the coin 1, amount 4 gains 1 from amount 3, so its count becomes 1."},{"at":{"a":5},"vars":{"coin":1,"add":1,"ways":1},"note":"Adding the coin 1, amount 5 gains 1 from amount 4, so its count becomes 1."},{"at":{"a":2},"vars":{"coin":2,"add":1,"ways":2},"note":"Adding the coin 2, amount 2 gains 1 from amount 0, so its count becomes 2."},{"at":{"a":3},"vars":{"coin":2,"add":1,"ways":2},"note":"Adding the coin 2, amount 3 gains 1 from amount 1, so its count becomes 2."},{"at":{"a":4},"vars":{"coin":2,"add":2,"ways":3},"note":"Adding the coin 2, amount 4 gains 2 from amount 2, so its count becomes 3."},{"at":{"a":5},"vars":{"coin":2,"add":2,"ways":3},"note":"Adding the coin 2, amount 5 gains 2 from amount 3, so its count becomes 3."},{"at":{"a":5},"vars":{"coin":5,"add":1,"ways":4},"note":"Adding the coin 5, amount 5 gains 1 from amount 0, so its count becomes 4."}]}
```

#### Amounts In The Outer Loop

The second run uses the same coins and the loop order of the naive section. For each amount it adds the entries one coin below, for every coin that fits. The entry for amount 3 becomes 3, because it adds the entries for amounts 2 and 1. The entry for amount 5 adds the entries for amounts 4, 3 and 0, which gives 5 + 3 + 1 = 9. That is the count of sequences, and it matches the nine entries in the cashier list.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["a"],"steps":[{"at":{"a":0},"vars":{"coin":0,"add":0,"ways":1},"note":"The seed is the empty combination, so the count for amount 0 is 1."},{"at":{"a":1},"vars":{"coin":1,"add":1,"ways":1},"note":"With the last coin 1, amount 1 gains 1 from amount 0, so its count becomes 1."},{"at":{"a":2},"vars":{"coin":1,"add":1,"ways":1},"note":"With the last coin 1, amount 2 gains 1 from amount 1, so its count becomes 1."},{"at":{"a":2},"vars":{"coin":2,"add":1,"ways":2},"note":"With the last coin 2, amount 2 gains 1 from amount 0, so its count becomes 2."},{"at":{"a":3},"vars":{"coin":1,"add":2,"ways":2},"note":"With the last coin 1, amount 3 gains 2 from amount 2, so its count becomes 2."},{"at":{"a":3},"vars":{"coin":2,"add":1,"ways":3},"note":"With the last coin 2, amount 3 gains 1 from amount 1, so its count becomes 3."},{"at":{"a":4},"vars":{"coin":1,"add":3,"ways":3},"note":"With the last coin 1, amount 4 gains 3 from amount 3, so its count becomes 3."},{"at":{"a":4},"vars":{"coin":2,"add":2,"ways":5},"note":"With the last coin 2, amount 4 gains 2 from amount 2, so its count becomes 5."},{"at":{"a":5},"vars":{"coin":1,"add":5,"ways":5},"note":"With the last coin 1, amount 5 gains 5 from amount 4, so its count becomes 5."},{"at":{"a":5},"vars":{"coin":2,"add":3,"ways":8},"note":"With the last coin 2, amount 5 gains 3 from amount 3, so its count becomes 8."},{"at":{"a":5},"vars":{"coin":5,"add":1,"ways":9},"note":"With the last coin 5, amount 5 gains 1 from amount 0, so its count becomes 9."}]}
```

<!-- stage: code -->
### Coins Outside And Amounts Inside

The method returns the number of combinations. It processes one denomination per outer iteration and updates the table in increasing order of amount.

```java
static long countCombinations(int[] coins, int amount) {
    long[] ways = new long[amount + 1];
    ways[0] = 1;
    for (int coin : coins) {
        for (int a = coin; a <= amount; a++) ways[a] += ways[a - coin];
    }
    return ways[amount];
}
```

The only difference from the naive method is the order of the two loops. The cost is O(amount * k) time and O(amount) memory. A denomination larger than `amount` never enters the inner loop, and an empty `coins` array returns `ways[amount]`, which is 1 only for amount 0.

<!-- stage: applicability -->
### Recognizing Counts That Ignore Order

#### Reading The Cue

Use this method when the question counts ways to reach an exact sum with reusable values and says that the order does not matter. Words such as "combinations", "number of ways to make change" and "distinct multisets" point here. The table indexes the sum, and the outer loop walks the values.

#### Checking The Invariant

The invariant says that after each denomination, every entry counts the combinations that use only the denominations seen so far. Test amount 0, which must return 1 even for an empty array. Test a positive amount with an empty array, which must return 0. Test a denomination above the amount, which must change nothing.

#### Avoiding The False Friend

The false friend is the fewest-coins loop with the order of the loops swapped, which counts sequences and returns 9 for the cashier example. A descending inner loop is another, and it counts selections that use each denomination at most once. Duplicate denominations in the array are a third, since they count the same combination twice. A final one is an `int` count, which overflows long before the amount gets large.

<!-- stage: exercises -->
### Exercises

#### [Build] Count With One Coin (Author exercise)
<!-- id: cap-cmb-one-coin -->

**Prerequisites.** The seed `ways[0] = 1` and the increasing update from this lesson.

**Problem.** Only one denomination exists, a positive integer `coin`, and it can be used repeatedly. Return the number of combinations of coins that add up to exactly `amount`.

**Constraints.** The limits are:
- **Coin** satisfies `1 <= coin <= 1000`.
- **Amount** satisfies `0 <= amount <= 10000`, and amount 0 has one combination.
- **Result** is a `long`, and it is always 0 or 1.

**Example 1.** Input `coin = 3`, `amount = 12`, output `1`.

**Example 2.** Input `coin = 5`, `amount = 12`, output `0`.

**Hint.** With one denomination, which single earlier entry feeds each entry, and what does the seed contribute?

**Changed decision.** The table holds counts, not minimums, and its seed is 1. With one denomination the counts never exceed 1, so the table agrees with a divisibility test.

#### [Vary] Coin Change II (LeetCode 518)
<!-- id: cap-cmb-coin-change-two -->

**Prerequisites.** The exercise above.

**Problem.** The array `coins` lists distinct positive denominations, each usable repeatedly. Return the number of combinations whose values add up to exactly `amount`. Combinations that differ only in the order of the coins are the same combination.

**Constraints.** The limits are:
- **Length** satisfies `1 <= coins.length <= 12`.
- **Denomination** satisfies `1 <= coins[i] <= 5000`, and values are distinct.
- **Amount** satisfies `0 <= amount <= 5000`.
- **Result** is a `long`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = [2,3,7]`, `amount = 12`, output `4`.

**Example 2.** Input `coins = [4]`, `amount = 10`, output `0`.

**Hint.** Which loop must be on the outside so that every combination is written in one fixed order of denominations?

**Changed decision.** The method adds ways coin by coin. Each coin extends the table with the combinations that use it at least once.

#### [Boundary] Empty Combination (Author exercise)
<!-- id: cap-cmb-empty-combination -->

**Prerequisites.** The two exercises above.

**Problem.** The inputs are distinct positive denominations in `coins`, possibly none, and a nonnegative `amount`. Count the combinations that add up to exactly `amount`, where the array may be empty. The empty combination counts as one combination for amount 0.

**Constraints.** The limits are:
- **Length** satisfies `0 <= coins.length <= 8`.
- **Denomination** satisfies `1 <= coins[i] <= 8`, and values are distinct.
- **Amount** satisfies `0 <= amount <= 600`.
- **Result** is a `long`, and the answer can exceed the `int` range.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = []`, `amount = 0`, output `1`.

**Example 2.** Input `coins = [7,9]`, `amount = 5`, output `0`.

**Hint.** Which entry must be set before any loop runs, and what happens to the answer for a positive amount when no denomination exists?

**Changed decision.** The seed is set before the loops, so an empty array still answers 1 for amount 0. The table type is `long`, because the count for the denominations 1 through 8 passes the `int` range.

#### [Recognize] Explain Loop Order (Author exercise)
<!-- id: cap-cmb-explain-loop-order -->

**Prerequisites.** All three exercises above.

**Problem.** Given distinct positive denominations `coins` and a nonnegative `amount`, return a `long[]` of length 2. Entry 0 is the number of combinations that add up to `amount`, where order does not matter. Entry 1 is the number of coin sequences that add up to `amount`, where two sequences with different orders are different.

**Constraints.** The limits are:
- **Length** satisfies `1 <= coins.length <= 8`.
- **Denomination** satisfies `1 <= coins[i] <= 30`, and values are distinct.
- **Amount** satisfies `0 <= amount <= 60`, and amount 0 has one combination and one empty sequence.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = [1,2]`, `amount = 4`, output `[3,5]`.

**Example 2.** Input `coins = [3,4]`, `amount = 7`, output `[1,2]`.

**Hint.** The two counts use the same update with the two loops in opposite order. Which loop order gives which count?

**Changed decision.** The method fills two tables with the same update and swapped loops. Entry 0 uses coins in the outer loop, and entry 1 uses amounts in the outer loop.
