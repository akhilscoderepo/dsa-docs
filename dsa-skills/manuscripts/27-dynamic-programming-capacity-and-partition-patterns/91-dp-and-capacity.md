<!-- lesson-kind: combination -->
<!-- lesson-id: dp-and-capacity -->
## DP And Capacity

<!-- stage: context -->
### One Routine For Three Billing Screens

A billing service sells prepaid credit packs of 1, 2 and 3 units and shows three counts for an invoice of 4 units. The first screen counts bundles, where a bundle is a set of packs and the same pack type can be bought many times. The second counts purchase orders, where buying a 1-pack and then a 3-pack differs from buying them in the other order. The third counts one-time promo vouchers of 1, 2 and 3 units, where each voucher can be redeemed only once.

A developer writes one table routine and reuses it for all three screens. The screens show plausible numbers, and at least two of them do not match the product team's hand count. The correct counts are 4 bundles, 7 purchase orders and 1 voucher set, and the routine gets at least two of them wrong.

This lesson asks which choices in a capacity table decide the meaning of the count, and how to set them for each question.

<!-- stage: contributions -->
### What Two Earlier Skills Add

#### What Dynamic Programming Supplies

The foundations chapter gave every table entry a one-sentence meaning and a combine rule. The entry for a total says how many ways, how few items, or whether the total is reachable. The base entry is the empty choice. The update reads smaller entries that are already final, so the loop order is part of the definition.

#### What Capacity Supplies

The capacity lessons added two choices about the loops. The direction of the inner loop decides whether an item can be used again: upward lets it repeat, and downward allows one use. The loop that stays on the outside decides whether order matters: items outside count combinations, and totals outside count sequences.

#### What Both Add Together

Neither skill settles the loops alone. A table meaning without the loop choices can describe a question that the loops do not answer, and loop choices without a table meaning produce numbers with no question behind them. Together they give a short procedure. State the meaning of an entry, decide whether items repeat and whether order counts, and then pick the loop structure that implements exactly that pair of answers.

<!-- stage: naive -->
### Copying One Loop For Every Question

The quick idea picks the loop structure from the first problem and keeps it. The routine below puts the items on the outside and walks the totals upward, which is the structure of the fewest-coins and bundle-count tables. It adds counts and is called with a flag for each screen.

```java
static long copiedRoutine(int[] packs, int target) {
    long[] ways = new long[target + 1];
    ways[0] = 1;
    for (int pack : packs) {
        for (int total = pack; total <= target; total++) ways[total] += ways[total - pack];
    }
    return ways[target];
}
```

The routine runs in O(target * k) time for k pack sizes and uses O(target) memory. It gives the correct bundle count for repeatable packs. The open question is what it returns for the other two screens.

```predict
Run copiedRoutine on the packs [1, 2, 3] with target 4. Which of the three screens does the result match, and what are the other two answers?

It returns 4, which matches the bundle count. The purchase-order screen needs 7, and the voucher screen needs 1. The routine lets every pack repeat and ignores order, so it cannot produce the other two numbers.
```

<!-- stage: bottleneck -->
### Wrong Switches Give Plausible Numbers

The routine has the right cost for all three screens, since each valid structure runs in O(target * k). The defect is not speed. A wrong choice of loop direction or of loop owner keeps the code short and the output a plain integer, so nothing signals the mistake. A count of 4 for the voucher screen looks as believable as the correct 1.

Testing each variant against hand counts does not scale. The structure has two independent choices, and a third choice for the objective, so a team that copies code between screens can pair the wrong choices without noticing. Counting every pairing by exhaustive search is not an option for large targets, because the number of sequences grows exponentially.

A reliable method must tie the loop choices to the two questions in the problem statement. Asking whether an item can repeat fixes the inner direction, and asking whether order counts fixes the outer loop. The next section states that rule and the cases it excludes.

<!-- stage: insight -->
### Two Questions Fix The Loop Structure

Each question about the problem statement maps to one choice in the code. Ask them in order, and the structure follows.

<!-- names: loop direction, loop owner, combine rule -->

#### Direction Decides Reuse

The **loop direction** is the order in which the inner loop visits totals. An upward loop reads `ways[t - v]` after the same item `v` has already updated it, so the item can appear again. A downward loop reads `ways[t - v]` before the item updates it, so the item contributes at most once. Reuse questions say "any number of times", and single-use questions say "each at most once".

#### Ownership Decides Order

The **loop owner** is the loop that stays on the outside. If the items own the outside, each combination is written once in the order of the item array, and the table counts combinations. If the totals own the outside, every item can be the last element of any prefix, and the table counts sequences. Order matters only when the statement says that different orders are different outcomes.

#### The Rule Decides The Question

The **combine rule** says how two entries merge: addition counts ways, taking the smaller value minimizes the item count, and a logical or tests reachability. The rule does not interact with the other two choices, so the same loop structure serves all three questions. The last row of the table below is excluded from this chapter. Sequences of single-use items need to know which items were used, which a table indexed by total cannot record, so this chapter excludes it.

| Items repeat | Order counts | Outer loop | Inner loop |
| --- | --- | --- | --- |
| yes | no | items | upward |
| yes | yes | totals | items tried as last element |
| no | no | items | downward |
| no | yes | not a table over totals | needs a set of used items |

The invariant is that after each outer step, every entry is exact for the question the two answers define.

<!-- stage: variables -->
### Switches And One Count Table

The routine reads the item array and the target, and it changes neither. It keeps these values.

- **ways** is a `long[]` of length `target + 1`; entry `t` counts the outcomes that add up to `t`.
- **reusable** is a `boolean` that is true when an item may be used again.
- **ordered** is a `boolean` that is true when different orders are different outcomes.
- **t** is the total that a loop updates.
- **v** is the item value that a loop adds or tries as the last element.

The routine rejects the pair `ordered` true and `reusable` false, because the table cannot count that case. The counts are `long` values. Every item value must be positive, since a value of 0 would read an entry that is not final.

<!-- stage: trace -->
### Two Runs On Three Pack Sizes

#### One Use Per Pack

The first run applies the downward loop to the packs 1, 2 and 3 with target 4. The cells are the totals 0 through 4, and the pointer `t` points at the entry that changes. The variable `v` is the pack being added, `add` is the amount it contributes, and `ways` is the entry after the contribution. The first step shows the seed.

The pack 1 reaches total 1. The pack 2 then reaches totals 3 and 2, in that order, because the downward loop visits 4, 3 and 2. Total 3 reads the entry for total 1, which holds only the pack 1, so the pack 2 is never counted twice. The pack 3 reaches total 4 from total 1 and total 3 from the seed. The final entry for total 4 is 1, from the packs 1 and 3.

```trace
{"cells":[0,1,2,3,4],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"v":0,"add":0,"ways":1},"note":"The seed is the empty choice, so the count for total 0 is 1."},{"at":{"t":1},"vars":{"v":1,"add":1,"ways":1},"note":"Pack 1 at total 1 gains 1 from total 0, which was read before pack 1 changed it, so the count becomes 1."},{"at":{"t":3},"vars":{"v":2,"add":1,"ways":1},"note":"Pack 2 at total 3 gains 1 from total 1, which was read before pack 2 changed it, so the count becomes 1."},{"at":{"t":2},"vars":{"v":2,"add":1,"ways":1},"note":"Pack 2 at total 2 gains 1 from total 0, which was read before pack 2 changed it, so the count becomes 1."},{"at":{"t":4},"vars":{"v":3,"add":1,"ways":1},"note":"Pack 3 at total 4 gains 1 from total 1, which was read before pack 3 changed it, so the count becomes 1."},{"at":{"t":3},"vars":{"v":3,"add":1,"ways":2},"note":"Pack 3 at total 3 gains 1 from total 0, which was read before pack 3 changed it, so the count becomes 2."}]}
```

#### Order Counts

The second run uses the same packs and target with the totals on the outside. Each total sums, over every pack v, the entry v below it. Total 2 holds 2 and total 3 holds 4. Total 4 receives 4 from the last element 1, 2 from the last element 2, and 1 from the last element 3. The result is 7, which matches the purchase-order screen.

```trace
{"cells":[0,1,2,3,4],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"v":0,"add":0,"ways":1},"note":"The seed is the empty sequence, so the count for total 0 is 1."},{"at":{"t":1},"vars":{"v":1,"add":1,"ways":1},"note":"Total 1 with the last element 1 gains 1 from total 0, so its count becomes 1."},{"at":{"t":2},"vars":{"v":1,"add":1,"ways":1},"note":"Total 2 with the last element 1 gains 1 from total 1, so its count becomes 1."},{"at":{"t":2},"vars":{"v":2,"add":1,"ways":2},"note":"Total 2 with the last element 2 gains 1 from total 0, so its count becomes 2."},{"at":{"t":3},"vars":{"v":1,"add":2,"ways":2},"note":"Total 3 with the last element 1 gains 2 from total 2, so its count becomes 2."},{"at":{"t":3},"vars":{"v":2,"add":1,"ways":3},"note":"Total 3 with the last element 2 gains 1 from total 1, so its count becomes 3."},{"at":{"t":3},"vars":{"v":3,"add":1,"ways":4},"note":"Total 3 with the last element 3 gains 1 from total 0, so its count becomes 4."},{"at":{"t":4},"vars":{"v":1,"add":4,"ways":4},"note":"Total 4 with the last element 1 gains 4 from total 3, so its count becomes 4."},{"at":{"t":4},"vars":{"v":2,"add":2,"ways":6},"note":"Total 4 with the last element 2 gains 2 from total 2, so its count becomes 6."},{"at":{"t":4},"vars":{"v":3,"add":1,"ways":7},"note":"Total 4 with the last element 3 gains 1 from total 1, so its count becomes 7."}]}
```

<!-- stage: code -->
### One Routine With Two Switches

The method sets the loops from the two answers. It throws for the one pair that a table over totals cannot count.

```java
static long countWays(int[] items, int target, boolean reusable, boolean ordered) {
    if (ordered && !reusable) throw new IllegalArgumentException("order with single use needs a set of used items");
    long[] ways = new long[target + 1];
    ways[0] = 1;
    if (ordered) {
        for (int t = 1; t <= target; t++)
            for (int v : items) if (v <= t) ways[t] += ways[t - v];
    } else if (reusable) {
        for (int v : items)
            for (int t = v; t <= target; t++) ways[t] += ways[t - v];
    } else {
        for (int v : items)
            for (int t = target; t >= v; t--) ways[t] += ways[t - v];
    }
    return ways[target];
}
```

All three branches cost O(target * k) time and O(target) memory. The first branch implements the totals-outside loop, the second the items-outside upward loop, and the third the items-outside downward loop. The packs 1, 2 and 3 with target 4 return 7, 4 and 1 in that order.

<!-- stage: applicability -->
### Choosing The Loop Structure

#### Reading The Cue

Use this lesson when a statement mentions a limit or a sum, a pool of items, and a count or a best value. Read the statement for two phrases. "Any number of times" or "unlimited supply" sets the direction upward, and "each at most once" sets it downward. "Different orders are different" or "sequences" puts the totals outside, and "combinations" or "sets" puts the items outside.

#### Checking The Invariant

The invariant says that every entry is exact for the question defined by the two answers, once the outer step that finishes it is done. Test the same small input under all three structures and compare against the hand counts. Test target 0, which must return 1 in every structure. Test an item above the target, which must change nothing.

#### Avoiding The False Friend

The false friend is a copied loop that answers a neighboring question and returns a plausible number. A downward loop used for a reuse question undercounts, and an upward loop used for a single-use question overcounts. A totals-outside loop used for combinations overcounts, and an items-outside loop used for sequences undercounts. A fourth false friend is an `int` count, which overflows once sequences grow.

<!-- stage: exercises -->
### Exercises

#### [Build] Coin Change (LeetCode 322)
<!-- id: cap-dpc-coin-change-flag -->

**Prerequisites.** The loop direction rule from this lesson and the fewest-coins table from the first lesson of the chapter.

**Problem.** An array `coins` of positive integers, a nonnegative integer `amount` and a boolean `reusable` are given. When `reusable` is true, each denomination may be used any number of times. When it is false, each array position may be used at most once, and equal values at different positions count as different coins. Return the fewest coins whose values sum to `amount`, or -1 if no choice does.

**Constraints.** The limits are:
- **Length** satisfies `0 <= coins.length <= 15`.
- **Value** satisfies `1 <= coins[i] <= 1000`, and equal values are allowed.
- **Amount** satisfies `0 <= amount <= 5000`, and amount 0 returns 0.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = [1,3,4]`, `amount = 6`, `reusable = true`, output `2`.

**Example 2.** Input `coins = [1,3,4]`, `amount = 6`, `reusable = false`, output `-1`.

**Hint.** Which inner direction lets a coin be read after it has already updated a smaller amount, and which direction does not?

**Changed decision.** The flag chooses the direction of the inner loop. The table, the marker and the minimum rule stay the same in both cases.

#### [Vary] Coin Change II (LeetCode 518)
<!-- id: cap-dpc-coin-change-two-ordered -->

**Prerequisites.** The exercise above and the two count lessons of this chapter.

**Problem.** The inputs are `coins` with distinct positive denominations, a nonnegative `amount` and a boolean `ordered`. Each denomination may be used any number of times. When `ordered` is false, return the number of combinations that add up to `amount`. When it is true, return the number of sequences that add up to `amount`.

**Constraints.** The limits are:
- **Length** satisfies `1 <= coins.length <= 10`.
- **Denomination** satisfies `1 <= coins[i] <= 100`, and values are distinct.
- **Amount** satisfies `0 <= amount <= 300`.
- **Result** is a `long`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = [2,4,5]`, `amount = 9`, `ordered = false`, output `2`.

**Example 2.** Input `coins = [2,4,5]`, `amount = 9`, `ordered = true`, output `5`.

**Hint.** The same update serves both answers. Which loop must be on the outside for each answer?

**Changed decision.** The flag chooses the loop owner. The seed, the update and the table type stay the same in both cases.

#### [Boundary] Partition Equal Subset Sum (LeetCode 416)
<!-- id: cap-dpc-partition-nonempty -->

**Prerequisites.** The two exercises above and the target-sum lesson.

**Problem.** An array `nums` of nonnegative integers is given. Split the indexes into two groups so that both groups are nonempty and have the same sum. The answer is `true` when a legal split exists.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 40`, and a single element cannot be split.
- **Value** satisfies `0 <= nums[i] <= 100`, and zeros may fill the array.
- **Groups** must both be nonempty, and each index belongs to exactly one group.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [0,0]`, output `true`.

**Example 2.** Input `nums = [0]`, output `false`.

**Hint.** The empty subset and the full set may both sum to half. How can a count of subsets tell the legal splits from those two?

**Changed decision.** The table counts subsets in place of testing reachability, with the descending loop. The method subtracts the empty subset and the full set when they reach half.

#### [Recognize] Target Sum (LeetCode 494)
<!-- id: cap-dpc-signed-range -->

**Prerequisites.** All three exercises above.

**Problem.** An array `nums` of nonnegative integers and two integers `lo` and `hi` with `lo <= hi` are given. Every element receives a plus or a minus sign. Return the number of sign assignments whose signed sum `s` satisfies `lo <= s <= hi`.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 20`.
- **Value** satisfies `0 <= nums[i] <= 50`, and the total is at most 1000.
- **Range** satisfies `-1000 <= lo <= hi <= 1000`.
- **Result** is a `long`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [1,2,3]`, `lo = 0`, `hi = 2`, output `3`.

**Example 2.** Input `nums = [4,1,3,2]`, `lo = -2`, `hi = 3`, output `6`.

**Hint.** A signed sum of `s` means the plus group sums to `(total + s) / 2`. Which plus-group sums stay inside the range?

**Changed decision.** One table of subset counts answers the whole range. The method adds up the entries whose plus-group sum falls between the two bounds.
