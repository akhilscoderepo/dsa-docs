<!-- lesson-kind: standard -->
<!-- lesson-id: reusable-candidates -->
## Reusable Candidates

<!-- stage: context -->
### The Coin Jar At Pellam Fair

At the Pellam Fair a ring-toss stall sells its prizes for exact change only. The stallholder keeps a jar with an endless supply of a few coin values, say a two, a three and a five, and a customer must pay the price using any number of each coin. The stallholder wants a laminated card for each prize that shows every different way to pay, so that a customer can pick one and no argument arises.

A way to pay is a handful of coins, and handing over a three and then a two is the same payment as a two and then a three. Her first draft card listed both and made the stall look like it had twice as many options as it did. She wants each handful once, with the coins always shown from the smallest value to the largest.

<!-- stage: naive -->
### Pay With Any Coin At Every Step

The direct method pays one coin at a time. At each step it tries every coin value that still fits the amount left, and when the amount reaches zero it has a finished payment. To avoid showing both orders of the same handful, each finished payment is sorted and put into a set, which keeps one copy.

```java
static Set<List<Integer>> waysByOrder(int[] coins, int price) {
    Set<List<Integer>> ways = new LinkedHashSet<>();
    pay(coins, price, new ArrayList<>(), ways);
    return ways;
}

private static void pay(int[] coins, int left, List<Integer> paid, Set<List<Integer>> ways) {
    if (left == 0) {
        List<Integer> sorted = new ArrayList<>(paid);
        Collections.sort(sorted);
        ways.add(sorted);
        return;
    }
    for (int c : coins) {
        if (c > left) continue;
        paid.add(c);
        pay(coins, left - c, paid, ways);
        paid.remove(paid.size() - 1);
    }
}
```

Each distinct handful is found, since every ordering of it is one of the sequences the loop walks, so the set ends up holding exactly the right cards.

<!-- stage: bottleneck -->
### Every Handful Is Paid In Every Order

A handful of m coins can be paid in up to m! different orders, so h handfuls cost up to O(m! * h) payments, and the search walks all of them. With coin values of one and two and a price of thirty, the number of ordered payments is a Fibonacci number past a million, while the number of different handfuls is only sixteen, one for each count of twos from zero to fifteen. The set hides the damage by merging the repeats afterwards, yet the search has already paid for every one of them, and each costs a sort.

The loop restarts from the first coin after every payment, so it forgets which coin it just used. If a payment only ever moved to the same coin or to a later one, each handful would have one reading order, the nondecreasing one, and would be reached by one route, with no set and no sorting.

<!-- stage: insight -->
### Stay On The Coin Or Move On

Let a call carry a start position in the list of coin values and the amount still to pay. A call has two kinds of moves. It can pay the coin at position i again, which is the **same-index call**: the recursive call receives i and not i + 1, so that coin stays available. Or the loop can move on to a later position, after which the earlier coins are never offered again. Together these generate every handful once, as one **nondecreasing route**, with the coins in list order and a coin repeated by staying on it.

The start position replaces the set. Offering position i only after positions below it have been dropped means that a handful has exactly one spelling, namely its coins sorted by position. A route that paid a later coin and then went back to an earlier one is never produced, so no repeat can appear.

The **remaining target** is the number that shrinks, and it is also what makes the recursion end. Each payment subtracts a positive coin, so the amount strictly decreases and eventually reaches zero, where a payment is recorded, or becomes too small for any coin. The reusable coin makes the depth depend on the price and not on the number of coins, so the guarantee comes entirely from the coins being positive. A coin of zero would produce the same call state again and again, which is the false friend of the first lesson.

The invariant is that a call may pay only the coins at positions from start onward, the remaining target equals the price minus the coins already on the path, and the path is always in list order.

<!-- names: same-index call, nondecreasing route, remaining target -->

<!-- stage: variables -->
### Start, Left And Path

The `start` is the first position the call may use, and it equals the position of the last coin paid, so it changes only when the loop moves on. The `left` value is the remaining target and drops by the value of each coin paid. The `path` holds the coins paid so far in list order, with repeats. The loop variable `i` is the position being paid now, and it passes `i` itself, not `i + 1`, to the next call. The `ways` list gets a copy of the path whenever `left` is exactly zero.

<!-- stage: trace -->
### Paying Six With Twos And Threes

The first trace pays six using the coins 2 and 3. The pointer `i` marks the coin being paid, and the variable `left` is the amount still owed. Notice that after a two is paid the loop may pay a two or a three, but after a three has been paid it may only pay a three, since the coin before it is gone.

```trace
{"cells":["2","3"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"path":"[2]","left":4},"note":"The coin 2 is paid, so 4 is left, and the next call may use positions from 0 onward, which keeps 2 available."},{"at":{"i":0},"vars":{"path":"[2, 2]","left":2},"note":"The coin 2 is paid, so 2 is left, and the next call may use positions from 0 onward, which keeps 2 available."},{"at":{"i":0},"vars":{"path":"[2, 2, 2]","left":0},"note":"The coin 2 is paid, so 0 is left, and the next call may use positions from 0 onward, which keeps 2 available."},{"at":{"i":0},"vars":{"path":"[2, 2, 2]","left":0},"note":"The amount left is zero, so a copy of [2, 2, 2] is recorded as handful 1."},{"at":{"i":0},"vars":{"path":"[2, 2]","left":2},"note":"The coin 2 is taken back, so the path is [2, 2] and 2 is owed again."},{"at":{"i":1},"vars":{"path":"[2, 2]","left":2},"note":"The coin 3 is larger than the 2 still owed, so it is skipped."},{"at":{"i":0},"vars":{"path":"[2]","left":4},"note":"The coin 2 is taken back, so the path is [2] and 4 is owed again."},{"at":{"i":1},"vars":{"path":"[2, 3]","left":1},"note":"The coin 3 is paid, so 1 is left, and the next call may use positions from 1 onward, which keeps 3 available."},{"at":{"i":1},"vars":{"path":"[2, 3]","left":1},"note":"The coin 3 is larger than the 1 still owed, so it is skipped."},{"at":{"i":1},"vars":{"path":"[2]","left":4},"note":"The coin 3 is taken back, so the path is [2] and 4 is owed again."},{"at":{"i":0},"vars":{"path":"empty","left":6},"note":"The coin 2 is taken back, so the path is empty and 6 is owed again."},{"at":{"i":1},"vars":{"path":"[3]","left":3},"note":"The coin 3 is paid, so 3 is left, and the next call may use positions from 1 onward, which keeps 3 available."},{"at":{"i":1},"vars":{"path":"[3, 3]","left":0},"note":"The coin 3 is paid, so 0 is left, and the next call may use positions from 1 onward, which keeps 3 available."},{"at":{"i":1},"vars":{"path":"[3, 3]","left":0},"note":"The amount left is zero, so a copy of [3, 3] is recorded as handful 2."},{"at":{"i":1},"vars":{"path":"[3]","left":3},"note":"The coin 3 is taken back, so the path is [3] and 3 is owed again."},{"at":{"i":1},"vars":{"path":"empty","left":6},"note":"The coin 3 is taken back, so the path is empty and 6 is owed again."}]}
```

The second trace is the false friend. It pays three with the coins 1 and 2, and each call restarts from the first coin. The variable `again` tells whether the sorted handful was already found. The route 1 then 2 and the route 2 then 1 spell the same handful, so one of them is a repeat.

```trace
{"cells":["1","2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"path":"[1]","again":"no"},"note":"The coin 1 is paid from the whole list, because the loop restarts at the first coin, so the path is [1]."},{"at":{"i":0},"vars":{"path":"[1, 1]","again":"no"},"note":"The coin 1 is paid from the whole list, because the loop restarts at the first coin, so the path is [1, 1]."},{"at":{"i":0},"vars":{"path":"[1, 1, 1]","again":"no"},"note":"The coin 1 is paid from the whole list, because the loop restarts at the first coin, so the path is [1, 1, 1]."},{"at":{"i":0},"vars":{"path":"[1, 1, 1]","again":"no"},"note":"The amount left is zero, so [1, 1, 1] is complete as the handful [1, 1, 1], which is new."},{"at":{"i":0},"vars":{"path":"[1, 1]","again":"no"},"note":"The coin 1 is taken back, so the path is [1, 1]."},{"at":{"i":0},"vars":{"path":"[1]","again":"no"},"note":"The coin 1 is taken back, so the path is [1]."},{"at":{"i":1},"vars":{"path":"[1, 2]","again":"no"},"note":"The coin 2 is paid from the whole list, because the loop restarts at the first coin, so the path is [1, 2]."},{"at":{"i":1},"vars":{"path":"[1, 2]","again":"no"},"note":"The amount left is zero, so [1, 2] is complete as the handful [1, 2], which is new."},{"at":{"i":1},"vars":{"path":"[1]","again":"no"},"note":"The coin 2 is taken back, so the path is [1]."},{"at":{"i":0},"vars":{"path":"empty","again":"no"},"note":"The coin 1 is taken back, so the path is empty."},{"at":{"i":1},"vars":{"path":"[2]","again":"no"},"note":"The coin 2 is paid from the whole list, because the loop restarts at the first coin, so the path is [2]."},{"at":{"i":0},"vars":{"path":"[2, 1]","again":"no"},"note":"The coin 1 is paid from the whole list, because the loop restarts at the first coin, so the path is [2, 1]."},{"at":{"i":0},"vars":{"path":"[2, 1]","again":"yes"},"note":"The amount left is zero, so [2, 1] is complete as the handful [1, 2], which was found before, so it is a repeat."},{"at":{"i":0},"vars":{"path":"[2]","again":"no"},"note":"The coin 1 is taken back, so the path is [2]."},{"at":{"i":1},"vars":{"path":"empty","again":"no"},"note":"The coin 2 is taken back, so the path is empty."}]}
```

<!-- stage: code -->
### The Loop Passes The Same Position

```java
static List<List<Integer>> ways(int[] coins, int price) {
    List<List<Integer>> ways = new ArrayList<>();
    pay(coins, 0, price, new ArrayList<>(), ways);
    return ways;
}

private static void pay(int[] coins, int start, int left, List<Integer> path, List<List<Integer>> ways) {
    if (left == 0) {
        ways.add(new ArrayList<>(path));
        return;
    }
    for (int i = start; i < coins.length; i++) {
        if (coins[i] > left) continue;               // does not fit
        path.add(coins[i]);
        pay(coins, i, left - coins[i], path, ways);  // same position again
        path.remove(path.size() - 1);
    }
}
```

All coins must be positive. With a coin of zero the call state never changes and the recursion runs until the stack is exhausted, which ends in a `StackOverflowError`. The number of calls depends on the price and the coin values, and the stack can be as deep as the price divided by the smallest coin.

<!-- stage: applicability -->
### One Item, Any Number Of Times

Use the same-index search when an item may be used any number of times and the result is a collection without order: ways to pay an amount, ways to build a total from reusable parts, and counts of unordered selections with repetition. The invariant that carries the proof is that the path is in list order and the remaining target equals the price minus the path, so the whole record of a call sits in two numbers.

The nearest false friend is the search that starts the loop at zero after every payment. It looks equally natural and is correct when order matters, as in counting the ordered ways to climb stairs, but for unordered handfuls it reports every reordering, and the cost grows with the factorial of the handful size. A second false friend is the one-use version of the previous lesson, which passes `i + 1`, and so can never pay a coin twice. The single character that separates the two lessons is that choice of argument.

Do not use it when a coin may be zero or negative, because the remaining target no longer shrinks and the depth is unbounded. Do not list the ways when only their number is needed for a large price, because the listing grows without limit. In Java, keep the coin array out of the mutation path and copy the path when recording, and expect a deep stack when the smallest coin is tiny compared with the price.

<!-- stage: exercises -->
### Exercises

#### [Build] Sum With Repeated Coins (Author exercise)
<!-- id: bt-coin-ways -->

**Prerequisites.** The increasing-start loop, and the idea of a shrinking amount as the guarantee of termination.

**Problem.** Given distinct positive coin values and a price, return the number of handfuls of coins that add up to exactly the price, where a coin value may be used any number of times and the order of the coins inside a handful does not matter. A price of zero has exactly one handful, the empty one.

**Constraints.** 1 <= coins.length <= 5, each coin is between 1 and 20, and 0 <= price <= 30.

**Example 1.** Input `coins = [1, 2]`, `price = 4`, output `3`.

**Example 2.** Input `coins = [3]`, `price = 7`, output `0`.

**Hint.** After paying the coin at position i, which positions may the next payment use, and what does it mean if no coin fits?

**Changed decision.** The call passes the same position back in after paying a coin, so a coin stays available, while the answer is a count and no path needs to be stored.

#### [Vary] Combination Sum (LeetCode 39)
<!-- id: bt-combination-sum -->

**Prerequisites.** The Sum With Repeated Coins rung.

**Problem.** Given distinct positive integers `candidates` and a `target`, return every combination of candidates that sums to the target, with a candidate usable any number of times. Each combination lists its values in the order of their positions in the array, and combinations are returned in the order the search finds them.

**Constraints.** 1 <= candidates.length <= 6, each candidate is between 2 and 12, and 1 <= target <= 24.

**Example 1.** Input `candidates = [2, 3, 6, 7]`, `target = 7`, output `[[2, 2, 3], [7]]`.

**Example 2.** Input `candidates = [3, 2]`, `target = 7`, output `[[3, 2, 2]]`.

**Hint.** If the array is not sorted, in what order do the values of a combination appear, and does the search need to sort anything?

**Changed decision.** Instead of counting, each hit stores a copy of the path, and the order of the answers follows array positions, not numeric size.

#### [Boundary] Candidate Larger Than Remainder (Author exercise)
<!-- id: bt-larger-than-remainder -->

**Prerequisites.** The Combination Sum rung.

**Problem.** Given positive candidates in strictly ascending order and a target, return a pair `[combinations, looks]`. The value `looks` is the number of times the loop compares a candidate with the amount left, and the loop must leave as soon as one candidate is too large, since all later ones are larger still. A target smaller than every candidate must produce no combination.

**Constraints.** 1 <= candidates.length <= 6, the candidates are positive, strictly ascending and at most 12, and 1 <= target <= 24.

**Example 1.** Input `candidates = [2, 3, 6, 7]`, `target = 7`, output `[2, 16]`.

**Example 2.** Input `candidates = [5, 8]`, `target = 4`, output `[0, 1]`.

**Hint.** What must be true about the order of the candidates for leaving the loop early to be as safe as skipping one candidate?

**Changed decision.** The loop stops at the first candidate that does not fit, instead of skipping it, which is valid only under the ascending order.

#### [Recognize] Fixed-Length Reusable Sum (Author exercise)
<!-- id: bt-fixed-length-reuse -->

**Prerequisites.** The Candidate Larger Than Remainder rung.

**Problem.** Given distinct positive integers `candidates`, a count `k` and a target, return every combination of exactly `k` values, repeats allowed, that sums to the target. Values appear in array order and combinations in the order found. A `k` of zero with a target of zero gives one empty combination.

**Constraints.** 1 <= candidates.length <= 6, each candidate is between 1 and 10, 0 <= k <= 6, and 0 <= target <= 30.

**Example 1.** Input `candidates = [1, 2, 3]`, `k = 3`, `target = 6`, output `[[1, 2, 3], [2, 2, 2]]`.

**Example 2.** Input `candidates = [4, 6]`, `k = 2`, `target = 9`, output `[]`.

**Hint.** Which new number joins the call state, and at what moment must both numbers be exact for a combination to be recorded?

**Changed decision.** A count of remaining picks joins the remaining target, and a path is recorded only when both reach zero, while the same-index call is unchanged.
