<!-- lesson-kind: standard -->
<!-- lesson-id: unbounded-coin-change -->
## Unbounded Coin Change

<!-- stage: context -->
### Paying Out Loyalty Points In Tokens

A rewards service pays out loyalty points as tokens worth 1, 3 and 4 points. A customer redeems 6 points, and the service wants to hand out as few tokens as possible. A payout routine that always hands out the largest token that still fits pays 4, then 1, then 1, which is three tokens. Two tokens of value 3 pay the same amount.

Formally, the input is an array `coins` of distinct positive integers and a nonnegative integer `amount`. Every denomination may be used any number of times. The task is to return the smallest number of tokens whose values add up to exactly `amount`, or -1 when no combination reaches it. The method never changes the array.

This lesson asks how to find the smallest token count without testing every combination of tokens.

<!-- stage: naive -->
### Paying With The Largest Token First

The quick idea is greedy. Sort the denominations, then repeatedly hand out as many tokens of the largest denomination as fit, and continue with the next smaller denomination for the rest.

```java
static int greedyCoins(int[] coins, int amount) {
    int[] sorted = coins.clone();
    Arrays.sort(sorted);
    int left = amount;
    int count = 0;
    for (int i = sorted.length - 1; i >= 0; i--) {
        count += left / sorted[i];
        left %= sorted[i];
    }
    return left == 0 ? count : -1;
}
```

The method sorts a copy and then makes one pass, so it runs in O(k log k) time for k denominations. It is fast and it pays correctly for many token sets. The open question is whether the largest token always belongs to a cheapest payout.

```predict
Run greedyCoins with the tokens [1, 3, 4] and the amount 6. What does it return, and what is the true smallest count?

It returns 3, because it pays 4, then 1, then 1. The true smallest count is 2, from the tokens 3 and 3. Taking the biggest token first can leave a remainder that needs many small tokens.
```

<!-- stage: bottleneck -->
### Many Orders Reach The Same Remainder

The greedy method commits to a token before it knows what the remainder costs. A cheaper payout can start with a smaller token, so no ordering of the denominations repairs the method for every token set.

A correct but slow method tries every denomination as the next token and recurses on the remainder. With k denominations and a smallest denomination `m`, the recursion has depth up to `amount / m` and branches k ways at each level. The call count grows like O(k^(amount/m)). For tokens 1, 2 and 5 and the amount 100, the bound 3^100 is far beyond any time budget.

Most of those calls repeat. Paying 1 then 2 and paying 2 then 1 both leave the same remainder, and the remaining cost depends only on that remainder. There are only `amount + 1` distinct remainders. A method that stores one answer per remainder does k steps of work per remainder, which is O(amount * k) time in total. The next section defines that table.

<!-- stage: insight -->
### Build The Table From Small Amounts Up

Imagine the cheapest payout for some amount. Look at one token in it and ask what the rest of the payout must be. The rest pays a smaller amount, and it must itself be cheapest for that smaller amount.

<!-- names: last coin, increasing amounts, unreachable -->

#### One Entry For Each Amount

Let `dp[a]` be the smallest number of tokens that add up to exactly `a`. The final answer is `dp[amount]`. The entry `dp[0]` is 0, because paying nothing needs no tokens. An amount that no combination reaches is **unreachable**, and its entry holds the marker `amount + 1`. That marker is larger than any real answer, because every token is worth at least 1 point and so a payout never needs more than `amount` tokens.

#### The Last Coin Splits Every Payout

Pick any payout for amount `a` and let c be the **last coin** in it, meaning any one token removed from the payout. The remaining tokens pay `a - c` exactly, and they form a cheapest payout for `a - c`, because a cheaper one would also improve the payout for `a`. So `dp[a]` equals 1 plus the smallest `dp[a - c]` over all denominations `c` with `c <= a`. A denomination larger than `a` cannot be the last coin. When every candidate entry holds the marker, `dp[a]` keeps the marker too.

#### Fill In Increasing Amounts

The loop visits **increasing amounts** from 1 to `amount`. When it reaches `a`, every entry below `a` is final. The entry `dp[a - c]` may already count the same denomination `c` once or several times. The loop therefore allows every denomination to appear again in any payout, which is exactly what the problem permits. The invariant, a condition that stays true at every loop step, is that `dp[a]` is correct for every amount the loop has passed, and the order of the amounts is what grants repeated use.

<!-- stage: variables -->
### The Table And The Candidate Coin

The method reads `coins` and `amount` and changes nothing. It keeps these working values.

- **dp** is an `int[]` of length `amount + 1`; entry `a` is the smallest token count that adds up to `a`.
- **a** is the amount that the outer loop fills, from 1 to `amount`.
- **coin** is the denomination that the inner loop tries as the last coin.
- **marker** is the value `amount + 1`, which stands for an unreachable amount.

The marker is not `Integer.MAX_VALUE`. Adding 1 to that value overflows to a negative number and makes the unreachable entry look like the best one. With the marker `amount + 1`, the sum `dp[a - coin] + 1` never exceeds `amount + 2`, so it fits in an `int`.

<!-- stage: trace -->
### Two Runs Over Small Amounts

#### A Smaller Token Beats The Largest

The first run uses the tokens 1, 3 and 4 and the amount 6. Each cell is an amount from 0 to 6, and the pointer `a` marks the amount that the loop fills. The variable `dp` is the filled entry and `coin` is the denomination that gave it. The first step, with the pointer at -1, shows the base entry.

At amount 3, the token 3 pays it alone. At amount 5, the last coin 1 leaves amount 4, which costs one token, so the payout costs two. At amount 6, the last coin 3 leaves amount 3, which costs one token. That gives 2 tokens, and the largest-token-first payout of 3 tokens is beaten.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["a"],"steps":[{"at":{"a":-1},"vars":{"dp":0,"coin":0},"note":"The base entry for amount 0 is 0, because paying nothing needs no tokens."},{"at":{"a":1},"vars":{"dp":1,"coin":1},"note":"Amount 1 takes the last coin 1, which leaves amount 0 with 0 tokens, so the entry becomes 1."},{"at":{"a":2},"vars":{"dp":2,"coin":1},"note":"Amount 2 takes the last coin 1, which leaves amount 1 with 1 token, so the entry becomes 2."},{"at":{"a":3},"vars":{"dp":1,"coin":3},"note":"Amount 3 takes the last coin 3, which leaves amount 0 with 0 tokens, so the entry becomes 1."},{"at":{"a":4},"vars":{"dp":1,"coin":4},"note":"Amount 4 takes the last coin 4, which leaves amount 0 with 0 tokens, so the entry becomes 1."},{"at":{"a":5},"vars":{"dp":2,"coin":1},"note":"Amount 5 takes the last coin 1, which leaves amount 4 with 1 token, so the entry becomes 2."},{"at":{"a":6},"vars":{"dp":2,"coin":3},"note":"Amount 6 takes the last coin 3, which leaves amount 3 with 1 token, so the entry becomes 2."}]}
```

#### Unreachable Amounts Stay Marked

The second run uses the tokens 5 and 7 and the amount 14. The marker is 15, so a `dp` value of 15 means that no combination reaches the amount. Amounts 1 to 4, 6, 8, 9, 11 and 13 keep the marker. Amount 14 becomes 2, because the last coin 7 leaves amount 7, which one token of 7 pays. The payout uses the denomination 7 twice, and the table allows that because `dp[7]` is final when amount 14 is filled.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],"pointers":["a"],"steps":[{"at":{"a":-1},"vars":{"dp":0,"coin":0},"note":"The base entry for amount 0 is 0, and the marker 15 stands for unreachable amounts."},{"at":{"a":1},"vars":{"dp":15,"coin":0},"note":"Amount 1 has no denomination that leaves a reachable amount, so the entry keeps the marker 15."},{"at":{"a":2},"vars":{"dp":15,"coin":0},"note":"Amount 2 is below or between the useful sums, so no last coin leaves a reachable amount and the entry keeps the marker 15."},{"at":{"a":3},"vars":{"dp":15,"coin":0},"note":"Amount 3 is below or between the useful sums, so no last coin leaves a reachable amount and the entry keeps the marker 15."},{"at":{"a":4},"vars":{"dp":15,"coin":0},"note":"Amount 4 is below or between the useful sums, so no last coin leaves a reachable amount and the entry keeps the marker 15."},{"at":{"a":5},"vars":{"dp":1,"coin":5},"note":"Amount 5 takes the last coin 5, which leaves amount 0 with 0 tokens, so the entry becomes 1."},{"at":{"a":6},"vars":{"dp":15,"coin":0},"note":"Amount 6 is below or between the useful sums, so no last coin leaves a reachable amount and the entry keeps the marker 15."},{"at":{"a":7},"vars":{"dp":1,"coin":7},"note":"Amount 7 takes the last coin 7, which leaves amount 0 with 0 tokens, so the entry becomes 1."},{"at":{"a":8},"vars":{"dp":15,"coin":0},"note":"Amount 8 is below or between the useful sums, so no last coin leaves a reachable amount and the entry keeps the marker 15."},{"at":{"a":9},"vars":{"dp":15,"coin":0},"note":"Amount 9 is below or between the useful sums, so no last coin leaves a reachable amount and the entry keeps the marker 15."},{"at":{"a":10},"vars":{"dp":2,"coin":5},"note":"Amount 10 takes the last coin 5, which leaves amount 5 with 1 token, so the entry becomes 2."},{"at":{"a":11},"vars":{"dp":15,"coin":0},"note":"Amount 11 is below or between the useful sums, so no last coin leaves a reachable amount and the entry keeps the marker 15."},{"at":{"a":12},"vars":{"dp":2,"coin":5},"note":"Amount 12 takes the last coin 5, which leaves amount 7 with 1 token, so the entry becomes 2."},{"at":{"a":13},"vars":{"dp":15,"coin":0},"note":"Amount 13 is below or between the useful sums, so no last coin leaves a reachable amount and the entry keeps the marker 15."},{"at":{"a":14},"vars":{"dp":2,"coin":7},"note":"Amount 14 takes the last coin 7, which leaves amount 7 with 1 token, so the entry becomes 2."}]}
```

<!-- stage: code -->
### Two Loops Over Amounts And Coins

The method returns the smallest token count, or -1 when the amount is unreachable. It fills the table once, from small amounts to large ones.

```java
static int minCoins(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int coin : coins) {
            if (coin <= a && dp[a - coin] + 1 < dp[a]) dp[a] = dp[a - coin] + 1;
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

The test `coin <= a` keeps the index `a - coin` inside the table. The final comparison turns the marker into -1. The method runs in O(amount * k) time and uses O(amount) memory. For `amount` equal to 0 the loops do not run, and the method returns `dp[0]`, which is 0.

<!-- stage: applicability -->
### Recognizing Repeatable Items With A Count Goal

#### Reading The Cue

Use this method when a positive-valued item can be used any number of times, the items must add up to an exact target, and the goal is the smallest number of items. Wording such as "any number of each kind" and "fewest" points here. The table indexes the target value, and each entry depends on entries with smaller targets.

#### Checking The Invariant

An **invariant** is a statement that stays true before and after each loop step. Here it says that `dp[a]` is the fewest tokens for amount `a` for every amount the loop has passed. Test amount 0, which must return 0 even with no denominations. Test an amount below every denomination, which must return -1. Test one denomination that does not divide the amount.

#### Avoiding The False Friend

A **false friend** is a method that passes simple samples yet returns a wrong result on other inputs. The greedy payout is the false friend here, and it is correct only for token sets with a special structure. A second false friend is a table that holds `Integer.MAX_VALUE` as the marker and then adds 1 to it. A third is a loop over amounts that runs downward, which reads entries that are not final yet and gives wrong totals.

<!-- stage: exercises -->
### Exercises

#### [Build] One Denomination (Author exercise)
<!-- id: cap-coin-one-denomination -->

**Prerequisites.** The table of fewest tokens per amount from this lesson.

**Problem.** A single positive integer `coin` is the only denomination, and it may be used any number of times. Return the smallest number of tokens that add up to exactly `amount`, or -1 when no number of tokens does.

**Constraints.** The limits are:
- **Coin** satisfies `1 <= coin <= 1000`.
- **Amount** satisfies `0 <= amount <= 10000`, and amount 0 needs 0 tokens.
- **Result** is an `int`, and -1 marks an unreachable amount.

**Example 1.** Input `coin = 4`, `amount = 12`, output `3`.

**Example 2.** Input `coin = 4`, `amount = 10`, output `-1`.

**Hint.** With one denomination, which single earlier entry can the entry for amount `a` read, and what does it hold when that entry is unreachable?

**Changed decision.** The inner loop over denominations has one candidate, so the minimum is a single read. Amounts that are not multiples of the coin keep the marker.

#### [Vary] Coin Change (LeetCode 322)
<!-- id: cap-coin-fewest-coins -->

**Prerequisites.** The exercise above.

**Problem.** An array `coins` holds distinct positive denominations, and each may be used any number of times. Return the smallest number of coins that add up to exactly `amount`, or -1 when no combination does.

**Constraints.** The limits are:
- **Length** satisfies `1 <= coins.length <= 12`.
- **Denomination** satisfies `1 <= coins[i] <= 10000`, and values are distinct.
- **Amount** satisfies `0 <= amount <= 10000`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = [3,7,10]`, `amount = 14`, output `2`.

**Example 2.** Input `coins = [5,9]`, `amount = 8`, output `-1`.

**Hint.** For one amount, which denominations can be the last coin, and which entry does each of them read?

**Changed decision.** Every denomination that fits is tried as the last coin, and the entry keeps the smallest result. One denomination is no longer enough to decide the entry.

#### [Boundary] Amount Zero And Impossible Target (Author exercise)
<!-- id: cap-coin-zero-and-impossible -->

**Prerequisites.** The two exercises above.

**Problem.** An array `coins` of distinct positive denominations, a nonnegative `amount` and an integer `failure` are given. Return the smallest number of coins that add up to exactly `amount`, or return `failure` when no combination does.

**Constraints.** The limits are:
- **Length** satisfies `0 <= coins.length <= 12`, and the array may be empty.
- **Amount** satisfies `0 <= amount <= 10000`, and amount 0 returns 0 even with no coins.
- **Failure** satisfies `-1000 <= failure <= 1000`, and it may equal a valid count such as 0 or 2.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = []`, `amount = 0`, `failure = -7`, output `0`.

**Example 2.** Input `coins = [6,10]`, `amount = 9`, `failure = 2`, output `2`.

**Hint.** The table needs a marker that is never a real answer. Why must the marker not be the same value as `failure`?

**Changed decision.** The table keeps its own marker `amount + 1` and the method converts it to `failure` only at the return. A caller value such as 0 or 2 cannot be confused with a real count inside the table.

#### [Recognize] Reconstruct One Minimum Set (Author exercise)
<!-- id: cap-coin-reconstruct -->

**Prerequisites.** All three exercises above.

**Problem.** An array `coins` holds distinct positive denominations, each usable any number of times. Return an `int[]` of coins that add up to exactly `amount` and whose length is the smallest possible, listed from largest to smallest. Return `null` when no combination reaches `amount`. Any smallest set is accepted.

**Constraints.** The limits are:
- **Length** satisfies `1 <= coins.length <= 12`.
- **Denomination** satisfies `1 <= coins[i] <= 1000`, and values are distinct.
- **Amount** satisfies `0 <= amount <= 5000`, and amount 0 returns an empty array.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = [1,3,4]`, `amount = 6`, output `[3,3]`.

**Example 2.** Input `coins = [2,5]`, `amount = 3`, output `null`.

**Hint.** The table only stores counts. What second value, saved when an entry improves, lets the method walk back from `amount` to 0?

**Changed decision.** Each improvement also stores the last coin in a parallel array `choice`. The method then follows `amount - choice[amount]` until it reaches 0.
