<!-- lesson-kind: combination -->
<!-- lesson-id: randomized-sampling-state -->
## Randomized Sampling State

<!-- stage: context -->
### A Fair Pick From A Moving Pool

A game server awards one random reward to a player. Only some rewards qualify: the player's level must be high enough, the reward must not already be owned, and the season must be active. Each qualifying reward has a drop weight. The first implementation counts all rewards in the catalog, picks a random number below that count, and walks the catalog to the chosen position. When the position falls on a reward that does not qualify, the code gives the next qualifying reward instead. Players with few qualifying rewards notice that one reward appears far more often than the others.

The error is the wrong total. A fair pick is fair among the items that qualify, with chances proportional to their weights, and the code computed its chances against the whole catalog. The lessons before this one taught three separate tools for fair random choice. This lesson asks how to combine them when a data structure decides which items qualify, and how to prove that the final chances are right.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

#### Counting Eligible Items

The lesson Reservoir Sampling supplied the one-pass rule for a stream of unknown length. The item at position `t` replaces the held item with probability `1 / t`, and a counter that counts only eligible items keeps the denominator correct. That lesson also supplied the habit of injecting the source of randomness so that a test can script every draw.

#### Mapping Tickets To Items

The lesson Weighted Selection supplied the ticket view. Each item owns a range of tickets as wide as its weight, and a uniform ticket from 1 to the total makes each item's chance proportional to its weight. It also supplied the rules for `long` totals and for zero weights.

#### Testing Membership In A Shape

The lesson Rejection Sampling supplied a way to sample a shape that has no formula. A uniform draw from a larger region is kept only when it passes a membership test, and the kept draws are uniform over the shape.

#### Combining The Three

The new work is the combination. The data structure, whether an array window, a linked list or a geometric test, decides which items are eligible. The probability rule must then use the total weight of the eligible items as its denominator. The lesson shows how each of the three tools keeps that denominator correct, and which of them applies when eligibility is discovered during a single pass.

<!-- stage: naive -->
### Count Everything, Then Skip

The direct design counts the whole catalog, draws a position below that count, and repairs a bad landing by moving forward to the next qualifying item. Each item is a record with a name, a weight and a flag that says whether it qualifies. Tests script the random draws through a `LongUnaryOperator` parameter. A call with bound `b` returns an integer below `b`.

```java
final class SkipPicker {
    record Item(String name, long weight, boolean qualifies) {}

    static String pick(java.util.List<Item> catalog, java.util.function.LongUnaryOperator pick) {
        int start = (int) pick.applyAsLong(catalog.size());          // position among all items
        for (int step = 0; step < catalog.size(); step++) {
            Item it = catalog.get((start + step) % catalog.size());  // move forward until an item qualifies
            if (it.qualifies()) return it.name();
        }
        return null;                                                  // nothing qualifies
    }
}
```

The code never returns an item that does not qualify, and it ignores the weights entirely. A repair that multiplies the position by the weight would not fix the problem, because the skipping step is what distorts the chances.

```predict
The catalog has five items in this order: A qualifies, B does not, C does not, D qualifies, E does not. The draw is uniform over the five positions and an item that does not qualify passes the pick to the next qualifying item. What is the chance of A and what is the chance of D? Is that fair among the two qualifying items?

Position 0 gives A. Positions 1, 2 and 3 give D, since B and C are skipped forward to D. Position 4 skips E and wraps around to A. So A gets positions 0 and 4, which is 2/5, and D gets positions 1, 2 and 3, which is 3/5. Two qualifying items should each get 1/2, so the pick is unfair.
```

<!-- stage: bottleneck -->
### Skipping Moves Chance To Neighbours

The pick costs O(n) time and O(1) extra space. The cost is acceptable, and the fairness is not. A skipped item passes its whole share of probability to the next qualifying item after it. An item that follows a long run of non-qualifying items collects the shares of all of them. The chance of a qualifying item therefore depends on the length of the gap before it in the catalog, and the gap has nothing to do with the item's weight.

The root cause is the denominator. A fair pick over `k` qualifying items with equal weights needs every item to get chance `1 / k`. A uniform draw over `n` catalog positions gives each position `1 / n`. The two numbers `k` and `n` differ, and no rule that moves probability between neighbours can repair them evenly.

A correct design has two requirements. It must count only eligible items, and the count must be the denominator of every chance. It must also be able to learn eligibility during the pass, because for a linked list or a stream the program cannot count the qualifying items before it starts.

<!-- stage: insight -->
### The Denominator Is The Eligible Total

<!-- names: eligible set, probability invariant, denominator -->

#### One Rule For Three Tools

The **eligible set** is the set of items that qualify at the moment of the pick, as decided by the data structure: a window of an array, the nodes of a list, or the points of a shape. The weight of the eligible set is the sum of the weights of its members. The **denominator** of the pick is that sum. The **probability invariant** says that every eligible item `e` has chance `weight(e) / denominator`, and no ineligible item has any chance.

Each earlier tool keeps the invariant in its own way. The reservoir keeps a running denominator, which is the total weight of the eligible items seen so far. The ticket method computes the denominator once, as the last prefix total. Rejection never computes it, and it lets the uniform draw over the larger region and the membership test produce chances that are proportional to the area of the eligible part.

#### A Weighted Reservoir

The reservoir rule extends to integer weights without a table. Let `W` be the total weight of the eligible items read so far, including the current item `e` with weight `w`. The method draws an integer from 0 to `W - 1` and replaces the held item with `e` when the draw is below `w`. The chance of replacement is `w / W`. The proof is by induction. After the first eligible item the invariant holds, since it is the only one. Suppose item `j` is held with chance `w_j / W_before`. After item `e` arrives, `j` stays with chance `(W_before / W) * (w_j / W_before) = w_j / W`. Item `e` is held with chance `w / W`. Every eligible item has chance proportional to its weight.

#### Choosing The Tool

The reservoir fits when eligibility is found while reading and the total is unknown. The ticket method fits when the items sit in memory, the weights are fixed, and many picks follow. Rejection fits when membership is a cheap test and the shape fills a large share of a simple region. The invariant is checked the same way for all three: write down the chance of one eligible item, divided by the eligible total.

<!-- stage: variables -->
### Eligible Total, Draw And Held Item

The weighted reservoir keeps five names.

- **held** is the name or index of the item currently in the sample.
- **total** is the sum of the weights of all eligible items read so far. It is a `long`, because a long stream of large weights overflows an `int`.
- **w** is the weight of the item being read. Only eligible items change `total`.
- **draw** is the result of `pick.applyAsLong(total)`, an integer from 0 to `total - 1`.
- **eligible** is the flag from the data structure. An ineligible item neither changes `total` nor makes a draw.

The first eligible item always becomes `held`. Its draw would always be below its own weight, so the code skips the draw and keeps the count of calls equal to the number of eligible items after the first.

<!-- stage: trace -->
### Tracing A Pool And A Ring

#### A Weighted Pass Over A Stream

The first trace reads five records in order, each written as a name and a weight. The records `A:3`, `C:1`, `D:4` and `E:2` are eligible, and `B:2` is not. The pointer `t` marks the record being read. Record `A` becomes the held item and sets `total` to 3. Record `B` does not qualify, so nothing changes. Record `C` brings `total` to 4 and draws from bound 4, getting 3, which is not below its weight 1, so `A` stays. Record `D` brings `total` to 8 and draws from bound 8, getting 2, which is below 4, so `D` replaces `A`. Record `E` brings `total` to 10 and draws from bound 10, getting 7, which is not below 2, so `D` stays. The final sample is `D`.

```trace
{"cells":["A:3","B:2","C:1","D:4","E:2"],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"total":3,"held":"A","draw":"none"},"note":"Record A is the first eligible record. It becomes the held item without a draw, and total is 3."},{"at":{"t":1},"vars":{"total":3,"held":"A","draw":"none"},"note":"Record B does not qualify, so total and the held item stay as they are."},{"at":{"t":2},"vars":{"total":4,"held":"A","draw":3},"note":"Total becomes 4. The draw from bound 4 is 3, which is not below the weight 1, so the held item stays."},{"at":{"t":3},"vars":{"total":8,"held":"D","draw":2},"note":"Total becomes 8. The draw from bound 8 is 2, which is below the weight 4, so D replaces the held item."},{"at":{"t":4},"vars":{"total":10,"held":"D","draw":7},"note":"Total becomes 10. The draw from bound 10 is 7, which is not below the weight 2, so the held item stays."}]}
```

#### Rejection On A Ring

The second trace samples a point in a ring with inner radius 1 and outer radius 2. The square around the outer circle gives unit coordinates from -1 to 1. A point is accepted when its squared distance from the center is between `0.25` and `1`, because the inner radius is half the outer radius. The pointer `trial` marks the trial. The first pair of draws lies inside the hole and is rejected. The second pair lies outside the outer circle and is rejected. The third pair lies in the ring and is accepted, and the result is scaled by the outer radius.

```trace
{"cells":["(0.1, -0.1)","(-0.9, 0.9)","(0.8, 0.0)"],"pointers":["trial"],"steps":[{"at":{"trial":0},"vars":{"x":0.1,"y":-0.1,"r2":0.02,"verdict":"reject"},"note":"Draws 0.55 and 0.45 give the unit point (0.1, -0.1) with squared distance 0.02. It lies inside the hole, below 0.25, so it is rejected."},{"at":{"trial":1},"vars":{"x":-0.9,"y":0.9,"r2":1.62,"verdict":"reject"},"note":"Draws 0.05 and 0.95 give the unit point (-0.9, 0.9) with squared distance 1.62. It lies outside the outer circle, above 1, so it is rejected."},{"at":{"trial":2},"vars":{"x":0.8,"y":0.0,"r2":0.64,"verdict":"accept"},"note":"Draws 0.9 and 0.5 give the unit point (0.8, 0.0) with squared distance 0.64. It is accepted and returned after scaling by 2."}]}
```

<!-- stage: code -->
### One Pass With Weights And Eligibility

#### The Weighted Reservoir

The method reads records once. A record carries a flag from the data structure, and the method ignores records that do not qualify. The first eligible record is kept without a draw.

```java
final class WeightedReservoir {
    record Item(String name, long weight, boolean qualifies) {}

    static String pick(java.util.List<Item> items, java.util.function.LongUnaryOperator pick) {
        String held = null;
        long total = 0;                                       // weight of the eligible items read so far
        for (Item it : items) {
            if (!it.qualifies() || it.weight() == 0) continue;   // ineligible items change nothing
            total += it.weight();
            if (held == null) { held = it.name(); continue; }    // the first eligible item needs no draw
            if (pick.applyAsLong(total) < it.weight()) held = it.name();   // replace with chance w / total
        }
        return held;                                          // null when nothing qualifies
    }
}
```

#### Cost

- **Time** is O(n) for one pass with one draw per eligible item after the first.
- **Space** is O(1), because the method keeps the held name and the total.
- **Rejection** costs O(1) expected per sample when the eligible region fills a good share of the simple region.

<!-- stage: applicability -->
### When The Eligible Total Matters

#### Recognizing The Pattern

Use this combination when a statement asks for a random pick among items that satisfy a condition. A data structure decides the condition, for example a window, a list traversal, a set or a geometric test. Before coding, name the eligible set, name its total weight and write the chance of one eligible item as a fraction. The invariant to protect is that every eligible item has chance `weight / denominator` and nothing else has any chance.

#### False Friends

Skipping to the next qualifying item is a false friend, as the predict question showed. Picking a position among all items and retrying until it qualifies is exact but is rejection in disguise, and its speed depends on the share of qualifying items. A shuffle of the whole catalog followed by a scan is exact and costs more than needed. Picking uniformly among qualifying items and then adjusting by weight does not give proportional chances.

#### When The Method Does Not Apply

If the weights change between picks, a Fenwick tree keeps the totals current. If the eligible set is empty, the pick has no valid answer, and the contract must say what the method returns. If the weights are real numbers, integer tickets are unavailable, and the boundary comparisons need a stated tolerance.

<!-- stage: exercises -->
### Exercises

#### [Build] Random Pick Index (LeetCode 398)
<!-- id: rss35-random-pick-window -->

**Prerequisites.** The weighted reservoir idea from this lesson and the Reservoir Sampling lesson. This exercise limits the eligible positions to a window.

**Problem.** Write `int pickInWindow(int[] nums, int target, int from, int to, LongUnaryOperator pick)`. A position `i` is eligible when `from <= i <= to` and `nums[i] == target`. Return one eligible position, chosen so that every eligible position has the same probability. The first eligible position needs no draw. For the `m`-th eligible position, call `pick.applyAsLong(m)` once and take the new position when the result is 0. Return -1 and make no draw when no position is eligible.

**Constraints.** The limits are:
- **Length** of `nums` is from 1 to 2 * 10^4.
- **Window** satisfies `0 <= from <= to < nums.length`.
- **Values** are `int` values, and `target` may be absent from the window.
- **Memory** is O(1) beyond the input.

**Example 1.** Input `nums = [2, 7, 2, 2, 9, 2]`, `target = 2`, `from = 1`, `to = 5`, scripted draws `0, 2` for the bounds 2 and 3, output `3`.

**Example 2.** Input `nums = [4, 5]`, `target = 9`, `from = 0`, `to = 1`, no draws, output `-1`.

**Hint.** Which count is the denominator when matches outside the window do not exist for this call?

**Changed decision.** The eligible set is a window of the array, and the answer may be empty.

#### [Vary] Linked List Random Node (LeetCode 382)
<!-- id: rss35-weighted-list-node -->

**Prerequisites.** The Random Pick Index exercise above. This exercise changes the denominator from a count of nodes to a sum of node weights.

**Problem.** A node holds an `int val`, a `long count` of at least 1 and a reference `next`. A node stands for `count` equal copies of `val` in an expanded sequence. Write `int weightedNode(RunNode head, LongUnaryOperator pick)`. The method walks the list once and returns a value chosen so that every element of the expanded sequence has the same probability. The first node needs no draw. For every later node, the method adds its `count` to the running total, calls `pick.applyAsLong(total)` once, and takes the node's value when the result is below its `count`.

**Constraints.** The limits are:
- **Nodes** number from 1 to 10^5.
- **Counts** are `long` values from 1 to 10^12, and the total fits in a `long`.
- **Walk** reads each node once and does not change the list.
- **Memory** is O(1) beyond the list.

**Example 1.** Input list of three nodes `(5, x2)`, `(8, x1)` and `(3, x3)` in this order, with scripted draws `0, 4` for the bounds 3 and 6, output `8`.

**Example 2.** Input list `(7, x4)`, no draws, output `7`.

**Hint.** What is the chance that a node with count `c` replaces the held value when the running total is `T`?

**Changed decision.** Each node carries a weight, so the replacement chance is `count / total` and not `1 / nodes`.

#### [Boundary] Random Pick With Weight (LeetCode 528)
<!-- id: rss35-wide-ticket-picker -->

**Prerequisites.** The Linked List Random Node exercise above and the Weighted Selection lesson. This exercise uses zero-based tickets and weights that need the full `long` range.

**Problem.** Design the class `WidePicker` with a constructor that receives `long[] w` and a `LongUnaryOperator pick`. The constructor builds prefix totals with `Math.addExact`. It throws `IllegalArgumentException` when the array is empty, when any weight is negative, or when the total is zero, and `ArithmeticException` when the total exceeds `Long.MAX_VALUE`. The method `pickIndex()` takes the ticket `pick.applyAsLong(total)`, which lies from 0 to `total - 1`, and returns the first index whose prefix total is strictly greater than the ticket.

**Constraints.** The limits are:
- **Length** of `w` is from 0 to 10^5.
- **Weights** are `long` values, and only values from 0 up are legal.
- **Tickets** are zero-based, so index `i` owns the tickets from `P[i-1]` to `P[i] - 1`.
- **Zero weights** are legal and never chosen.

**Example 1.** Input `w = [3, 0, 2]` with scripted draws `2, 3`, outputs `0, 2`.

**Example 2.** Input `w = [9223372036854775807, 1]` throws `ArithmeticException`, and `w = [4000000000000000000, 4000000000000000000]` with scripted draw `7999999999999999999` outputs `1`.

**Hint.** Which search finds the first prefix total that is strictly above a zero-based ticket?

**Changed decision.** Tickets start at 0, so the comparison flips from "at least" to "strictly above", and the sums must be checked for overflow.

#### [Recognize] Generate Random Point In A Circle (LeetCode 478)
<!-- id: rss35-random-point-ring -->

**Prerequisites.** The Boundary exercise above and the Rejection Sampling lesson. This exercise removes an inner disc from the eligible region.

**Problem.** Write `double[] ringPoint(double inner, double outer, DoubleSupplier rand)`. The eligible region is the set of points whose distance from the origin is at least `inner` and at most `outer`. Each trial draws `u` and then `v` from `rand`, forms `ux = 2u - 1` and `uy = 2v - 1`, and accepts the pair when `(inner / outer)^2 <= ux^2 + uy^2 <= 1`. The method returns `{outer * ux, outer * uy}` for the first accepted pair.

**Constraints.** The limits are:
- **Radii** satisfy `0 <= inner < outer <= 10^8`.
- **Draws** are doubles from 0 (included) to 1 (excluded).
- **Test** runs in unit coordinates before scaling, and both edges are inside.
- **Acceptance** probability is `(pi - pi * (inner / outer)^2) / 4`.

**Example 1.** Input `inner = 1`, `outer = 2`, draws `0.5, 0.5, 0.9, 0.5`, output `[1.6, 0.0]`.

**Example 2.** Input `inner = 0`, `outer = 3`, draws `0.5, 0.5`, output `[0.0, 0.0]`.

**Hint.** What fraction of the unit square is accepted when the inner disc has half the outer radius?

**Changed decision.** The eligible region is a ring, so the membership test has a lower bound as well as an upper bound.
