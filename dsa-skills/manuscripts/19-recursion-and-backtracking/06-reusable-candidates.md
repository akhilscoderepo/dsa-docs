<!-- lesson-kind: standard -->
<!-- lesson-id: reusable-candidates -->
## Reuse A Value In A Sum

<!-- stage: context -->
### Why Ten Cents Gives Hundreds Of Payments

A payment tester must list every way to pay exactly 10 cents with coins of 1, 2 and 3 cents. A coin may appear any number of times. The developer writes a search that tries all three coins at every step and stops when the sum reaches 10. The tester prints 274 payments. It lists `3, 3, 2, 2` and `2, 2, 3, 3` on separate lines, although a customer who hands over those coins makes the same payment.

Only 14 different payments exist. This lesson asks how a search lets a coin repeat and still lists each payment once.

<!-- stage: naive -->
### Trying Every Coin At Every Step

The direct plan loops over all coins at each call and passes the smaller target. It sorts each finished payment and keeps one copy of each in a set.

```java
static void pay(int[] coins, int remain, List<Integer> path, Set<List<Integer>> seen) {
    if (remain == 0) {
        List<Integer> key = new ArrayList<>(path);
        Collections.sort(key);                                  // equal payments get one sorted form
        seen.add(key);                                          // the set drops the repeats
        return;
    }
    if (remain < 0) return;                                     // the coins overshoot the target
    for (int c : coins) {                                       // every coin again, from the first one
        path.add(c);
        pay(coins, remain - c, path, seen);
        path.remove(path.size() - 1);                           // undo the choice
    }
}
```

The method finds every payment, because each payment appears in at least one order of its coins. It builds every order.

<!-- stage: bottleneck -->
### Counting The Orders Of One Payment

```predict
The target is 10 and the coins are 1, 2 and 3. The search stores one path for every ordered list of coins that adds up to 10. About how many paths does it store, and how many different payments exist?

The search stores 274 ordered lists, and only 14 different payments exist, so the search stores about 20 lists for each payment. It makes 979 calls in total, while a search that avoids the repeats makes 94.
```

The search costs O(c^(t/m)) time in the worst case, where `c` is the number of coins, `t` is the target and `m` is the smallest coin. A payment with `j` coins appears in up to j! orders, so the waste grows with the length of the payment.

The loop restarts at the first coin at every call. A payment only needs one order, such as coins from small to large. If each call may use its own coin or a later coin, but never an earlier one, then every payment appears in the order of the coin list, once.

<!-- stage: insight -->
### Staying On The Same Coin

#### Reusing Through The Same Start

A call with start `s` loops over the coins from index `s`. When it chooses coin `i`, it passes the **same start** `i` to the child, and not `i + 1`. The child may choose coin `i` again, or any later coin. A coin appears as often as the sum allows, and no child ever chooses a coin below `i`.

#### Tracking The Remaining Target

The **remaining target** is the part of the target that the path has not yet reached. It starts at the target and falls by each chosen coin. A call with remaining target 0 stores a copy of its path. A call with a negative remaining target has overshot and returns at once. Every coin is positive, so the remaining target only falls.

#### Keeping A Nondecreasing Path

The path lists coin indices that never decrease, so it is a **nondecreasing path**. Each payment has exactly one nondecreasing list of indices, and the search visits that list once. The invariant is that every choice uses an index at or above the index of the last choice. The remaining target equals the target minus the sum of the path.

<!-- names: same start, remaining target, nondecreasing path -->

<!-- stage: variables -->
### The Pieces Of State

Four pieces of state describe a call.

- **Start** is the lowest coin index that the loop may choose.
- **Remaining target** is the target minus the sum of the path.
- **Path** is the shared list of chosen coins in nondecreasing index order.
- **Index i** is the coin index that the loop tries.

A choice passes `i` as the next start and lowers the remaining target by `coins[i]`. A call stores a copy of the path when the remaining target is 0.

<!-- stage: trace -->
### Following Two Coins Through A Target

#### Paying Seven With Three Coins

The first trace uses the coins `[2, 3, 7]` and the target 7. The pointer `start` shows the lowest coin index that the choosing call may use. The variable `remain` shows the remaining target after the choice, and `stored` counts the payments in the output.

The root chooses 2, and its child keeps start 0, so it chooses 2 again and then a third 2. The remaining target is 1, so the next choices of 2, 3 and 7 all overshoot. The call after the second 2 has the remaining target 3. It chooses 3, reaches 0 and stores `[2, 2, 3]`. The call after the first 2 then chooses 3 and has start 1, so it never tries the coin 2 again. The root next chooses 3 and finds no payment, and its last choice, 7, stores `[7]`. The trace shows 18 choices and 2 payments.

#### Seeing The Order Repeat

The second trace uses the coins `[1, 2]` and the target 3 with a loop that restarts at the first coin. It stores `[1, 1, 1]`, then `[1, 2]`, then `[2, 1]`. The last two lists hold the same coins in a different order, so the search counts one payment twice.

#### Stepping Through Both Runs

```trace
{"cells":["2","3","7"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"remain":5,"stored":0},"note":"The call with start 0 chooses 2, and the remaining target becomes 5."},{"at":{"start":0},"vars":{"remain":3,"stored":0},"note":"The call with start 0 chooses 2, and the remaining target becomes 3."},{"at":{"start":0},"vars":{"remain":1,"stored":0},"note":"The call with start 0 chooses 2, and the remaining target becomes 1."},{"at":{"start":0},"vars":{"remain":-1,"stored":0},"note":"The call with start 0 chooses 2, and the remaining target becomes -1. The path overshoots, so the child returns at once."},{"at":{"start":0},"vars":{"remain":-2,"stored":0},"note":"The call with start 0 chooses 3, and the remaining target becomes -2. The path overshoots, so the child returns at once."},{"at":{"start":0},"vars":{"remain":-6,"stored":0},"note":"The call with start 0 chooses 7, and the remaining target becomes -6. The path overshoots, so the child returns at once."},{"at":{"start":0},"vars":{"remain":0,"stored":1},"note":"The call with start 0 chooses 3, and the remaining target becomes 0. The child stores [2,2,3]."},{"at":{"start":0},"vars":{"remain":-4,"stored":1},"note":"The call with start 0 chooses 7, and the remaining target becomes -4. The path overshoots, so the child returns at once."},{"at":{"start":0},"vars":{"remain":2,"stored":1},"note":"The call with start 0 chooses 3, and the remaining target becomes 2."},{"at":{"start":1},"vars":{"remain":-1,"stored":1},"note":"The call with start 1 chooses 3, and the remaining target becomes -1. The path overshoots, so the child returns at once."},{"at":{"start":1},"vars":{"remain":-5,"stored":1},"note":"The call with start 1 chooses 7, and the remaining target becomes -5. The path overshoots, so the child returns at once."},{"at":{"start":0},"vars":{"remain":-2,"stored":1},"note":"The call with start 0 chooses 7, and the remaining target becomes -2. The path overshoots, so the child returns at once."},{"at":{"start":0},"vars":{"remain":4,"stored":1},"note":"The call with start 0 chooses 3, and the remaining target becomes 4."},{"at":{"start":1},"vars":{"remain":1,"stored":1},"note":"The call with start 1 chooses 3, and the remaining target becomes 1."},{"at":{"start":1},"vars":{"remain":-2,"stored":1},"note":"The call with start 1 chooses 3, and the remaining target becomes -2. The path overshoots, so the child returns at once."},{"at":{"start":1},"vars":{"remain":-6,"stored":1},"note":"The call with start 1 chooses 7, and the remaining target becomes -6. The path overshoots, so the child returns at once."},{"at":{"start":1},"vars":{"remain":-3,"stored":1},"note":"The call with start 1 chooses 7, and the remaining target becomes -3. The path overshoots, so the child returns at once."},{"at":{"start":0},"vars":{"remain":0,"stored":2},"note":"The call with start 0 chooses 7, and the remaining target becomes 0. The child stores [7]."}]}
```

```trace
{"cells":["1","2"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"remain":2,"stored":0},"note":"The loop restarts at coin 1, and it chooses 1, so the path becomes [1] with the remaining target 2."},{"at":{"start":0},"vars":{"remain":1,"stored":0},"note":"The loop restarts at coin 1, and it chooses 1, so the path becomes [1,1] with the remaining target 1."},{"at":{"start":0},"vars":{"remain":0,"stored":1},"note":"The loop restarts at coin 1, and it chooses 1, so the path becomes [1,1,1] with the remaining target 0. The path adds up to 3, so the search stores [1,1,1]."},{"at":{"start":0},"vars":{"remain":0,"stored":2},"note":"The loop restarts at coin 1, and it chooses 2, so the path becomes [1,2] with the remaining target 0. The path adds up to 3, so the search stores [1,2]."},{"at":{"start":0},"vars":{"remain":1,"stored":2},"note":"The loop restarts at coin 1, and it chooses 2, so the path becomes [2] with the remaining target 1."},{"at":{"start":0},"vars":{"remain":0,"stored":3},"note":"The loop restarts at coin 1, and it chooses 1, so the path becomes [2,1] with the remaining target 0. The path adds up to 3, so the search stores [2,1]."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### Combination Sum With Reuse

The method passes `i` and not `i + 1` to the child, which allows a coin to repeat.

```java
static void go(int start, int remain, int[] coins, List<Integer> path, List<List<Integer>> out) {
    if (remain < 0) return;                            // the path overshoots the target
    if (remain == 0) {                                 // the path adds up to the target
        out.add(new ArrayList<>(path));                // store a copy
        return;
    }
    for (int i = start; i < coins.length; i++) {       // the same coin or a later coin
        path.add(coins[i]);                            // choose coin i
        go(i, remain - coins[i], coins, path, out);    // same start: coin i may repeat
        path.remove(path.size() - 1);                  // undo the choice
    }
}
```

#### Cost Of The Search

The depth of the recursion is at most `t / m` for the target `t` and the smallest coin `m`, so the stack uses O(t / m) memory. The number of calls grows exponentially in that depth in the worst case. For small targets, the nondecreasing path keeps the number of calls close to the number of payments.

<!-- stage: applicability -->
### Recognizing A Reusable Choice

#### Spotting The Pattern

The cue is a sum or a count that a value may reach several times, and the order of the values carries no meaning. The invariant is that every call passes the start of its own choice to the child, so a path is nondecreasing and every payment has one path.

#### Finding The False Friend

The false friend is a loop that restarts at index 0 after every choice. It builds each payment in every order. A second false friend is a child start of `i + 1`, which looks like the combination search of the previous lesson. It allows each coin only once, so it misses `[2, 2, 3]`.

#### Recognizing The No-Go Cases

The search does not fit when the question asks for a count or a minimum and not for the lists, because a table over amounts answers it faster. It does not fit when the target is large and the coins are small, since the output grows too large to list. A later chapter treats those questions.

<!-- stage: exercises -->
### Exercises

#### [Build] Sum With Repeated Coins (Author exercise)
<!-- id: bt-sum-with-repeated-coins -->

**Prerequisites.** The same start and the remaining target of this lesson.

**Problem.** Given a positive integer array `coins` with distinct values and a non-negative integer `target`, return every nondecreasing list of coins that adds up to `target`. A coin may appear several times in one list. A list that adds up to 0 is the empty list. The result keeps the order of the search.

**Constraints.** The limits are:
- **Coins** satisfy `1 <= coins.length <= 5` and `1 <= coins[i] <= 10`, and the coins are distinct.
- **Order** of `coins` may be any order, and the search follows the input order.
- **Target** is `0 <= target <= 15`.
- **Empty result** is an empty list when no payment reaches `target`.

**Example 1.** Input `coins = [1,2]`, `target = 3`, output `[[1,1,1],[1,2]]`.

**Example 2.** Input `coins = [5]`, `target = 0`, output `[[]]`.

**Hint.** Which start does the child of coin `i` receive? What does a call with remaining target 0 store?

**Changed decision.** The child receives the same start and not the next one, so the chosen coin stays available.

#### [Vary] Combination Sum (LeetCode 39)
<!-- id: bt-combination-sum -->

**Prerequisites.** The previous exercise.

**Problem.** The array `candidates` holds distinct positive integers, and `target` is a positive integer. Return every list of candidates that adds up to `target`, where a candidate may appear any number of times. Lists with the same candidates and the same counts count as one list. The values in a list follow the order of `candidates`.

**Constraints.** The limits are:
- **Candidates** satisfy `1 <= candidates.length <= 8` and `2 <= candidates[i] <= 40`, and they are distinct.
- **Target** is `1 <= target <= 40`.
- **Order** of the result follows the search order.
- **Mutation** does not occur; `candidates` keeps its order.

**Example 1.** Input `candidates = [2,3,6,7]`, `target = 7`, output `[[2,2,3],[7]]`.

**Example 2.** Input `candidates = [3,5]`, `target = 2`, output `[]`.

**Hint.** Why does a search with `i + 1` miss the list `[2, 2, 3]`? How deep can the recursion go for the smallest candidate?

**Changed decision.** The candidates arrive in any order, so the search follows the input order.

#### [Boundary] Candidate Larger Than Remainder (Author exercise)
<!-- id: bt-candidate-larger-than-remainder -->

**Prerequisites.** The two exercises above.

**Problem.** The array `candidates` holds distinct positive integers in increasing order, and `target` is a non-negative integer. Return the number of calls that the reuse search makes. Each loop stops at the first candidate that is larger than the remaining target, because all later candidates are larger still. Count the root call and every call that the loop makes.

**Constraints.** The limits are:
- **Candidates** satisfy `1 <= candidates.length <= 8` and `1 <= candidates[i] <= 30`, in strictly increasing order.
- **Target** is `0 <= target <= 30`.
- **Return** is a `long`.
- **Empty case** target 0 makes the root call only.

**Example 1.** Input `candidates = [2,3,6,7]`, `target = 7`, output 10.

**Example 2.** Input `candidates = [4]`, `target = 3`, output 1.

**Hint.** Which loop iterations does the stop rule remove? What happens to the call that has remaining target 0?

**Changed decision.** The loop stops at the first candidate above the remaining target, and the argument needs both sorted order and positive values.

#### [Recognize] Fixed-Length Reusable Sum (Author exercise)
<!-- id: bt-fixed-length-reusable-sum -->

**Prerequisites.** The previous three exercises.

**Problem.** The array `candidates` holds distinct positive integers, `target` is a positive integer and `k` is a positive integer. Return every nondecreasing list of exactly `k` candidates that adds up to `target`. A candidate may appear several times in one list. The values follow the order of `candidates`.

**Constraints.** The limits are:
- **Candidates** satisfy `1 <= candidates.length <= 6` and `1 <= candidates[i] <= 20`, and they are distinct.
- **Length** is `1 <= k <= 8`.
- **Target** is `1 <= target <= 40`.
- **Empty result** is an empty list when no list matches.

**Example 1.** Input `candidates = [1,2,3]`, `target = 5`, `k = 3`, output `[[1,1,3],[1,2,2]]`.

**Example 2.** Input `candidates = [4,6]`, `target = 10`, `k = 3`, output `[]`.

**Hint.** Which second counter limits the depth? When is a path with the remaining target 0 still not a result?

**Changed decision.** The search adds a count of remaining choices and keeps the same start for reuse.
