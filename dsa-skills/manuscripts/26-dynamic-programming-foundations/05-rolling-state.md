<!-- lesson-kind: standard -->
<!-- lesson-id: rolling-state -->
## Rolling State

<!-- stage: context -->
### A Table That Outgrows The Heap

A configuration service stores one on/off setting for each of n feature flags that sit in a row. A safety rule forbids two neighbouring flags from both being on. The service must report how many valid settings exist, modulo 1000000007, for n equal to 100 million flags. The counting method fills a table in which entry `dp[i]` holds the number of valid settings of the first `i` flags. An `int[]` of 100 million entries takes 400 MB. A process with a 512 MB heap limit throws `OutOfMemoryError` before it prints a single number.

The recurrence is the rule that computes one table entry from earlier entries. Here it reads `dp[i] = dp[i - 1] + dp[i - 2]`. The first term covers flag `i` switched off. The second term covers flag `i` switched on, which forces flag `i - 1` off. The program needs only the last entry of the table, so almost all of the 400 MB seems wasted.

This lesson asks which table entries the recurrence still reads, and how a method can discard the rest without changing a single answer. The method never changes its input, because the only input is the integer n.

<!-- stage: naive -->
### Filling The Whole Table

The direct method allocates the table, writes the base entries, and fills the remaining entries from left to right. Each entry takes one addition and one remainder.

```java
static int countSettings(int n) {
    final int MOD = 1_000_000_007;
    int[] dp = new int[n + 1];
    dp[0] = 1;
    if (n >= 1) dp[1] = 2;
    for (int i = 2; i <= n; i++) {
        dp[i] = (dp[i - 1] + dp[i - 2]) % MOD;
    }
    return dp[n];
}
```

The method is correct for every n. Base entry `dp[0]` is 1 because the empty row has exactly one setting. Base entry `dp[1]` is 2 because one flag is either off or on. The sum of two remainders stays below 2 * 10^9 + 12, which fits in an `int`, so the addition cannot overflow.

```predict
While the loop computes dp[1000], which earlier entries does it read, and which entries can the loop never read again?

It reads only dp[999] and dp[998]. The entries dp[0] through dp[997] are never read again, because every later iteration looks back at most two positions. The table holds 1001 entries while the computation needs only 2 of them at any moment.
```

<!-- stage: bottleneck -->
### Memory Grows With The Input

The table has n + 1 entries, so the method uses O(n) memory. The time of O(n) is already the best possible for a loop that visits every index. Only the memory is wasteful. For n equal to 100 million the table takes 400 MB, and the garbage collector cannot reclaim it while `dp` is alive.

The waste comes from a fixed fact about the recurrence. Iteration `i` reads positions `i - 1` and `i - 2` and nothing else. Positions further left were useful once and are dead afterwards. A method that keeps them pays for memory that no instruction will ever read.

Some problems do need the old entries. An answer that reconstructs the chosen items reads the whole table backwards, and a recurrence that reads index `i - k` for a large k needs a long history. The goal is a rule that tells the two cases apart: when the recurrence reads a bounded number of offsets, the memory can drop from O(n) to O(1) while the time stays O(n).

<!-- stage: insight -->
### Keep Only What The Recurrence Reads

A recurrence that looks back by fixed offsets needs only that many past values. Each value moves into a plain variable, and the table disappears.

<!-- names: window, shift, rolling -->

#### Read The Offsets In The Recurrence

List the indices on the right side of the recurrence, written relative to `i`. For `dp[i] = dp[i - 1] + dp[i - 2]`, the offsets are 1 and 2. The largest offset is the size of the **window**, which is the set of most recent entries that later iterations can still read. Here the window holds two entries. A recurrence with offsets 1, 2 and 3 has a window of three entries.

#### One Variable For Each Position

Name one variable for each position in the window. The method calls them `prev2` and `prev1`, where `prev1` holds `dp[i - 1]` and `prev2` holds `dp[i - 2]`. A third variable `cur` holds the new value `dp[i]`. The memory is three `int` values, which is O(1), no matter how large n becomes. This technique is called **rolling state**, because the same few variables keep rolling forward over successive positions of the table.

#### Move The Values In Safe Order

After the loop computes `cur`, the window has to **shift** by one position. The old `dp[i - 1]` becomes the new `dp[i - 2]`, and `cur` becomes the new `dp[i - 1]`. The order of the two assignments matters. The assignment `prev2 = prev1` must run first, because it reads `prev1` before `prev1` is overwritten. Running `prev1 = cur` first destroys the only copy of the old `dp[i - 1]`, and both variables then hold the same number. The rule is to write the variable that is oldest first and to read every dependency before it is overwritten.

#### Start From The Base Cases

The loop starts with the window filled from the base entries. Here `prev2` is `dp[0]` and `prev1` is `dp[1]`. When n is smaller than the first computed index, the method returns the right base value and never enters the loop. The invariant is that before the iteration for index `i`, the variables hold `dp[i - 2]` and `dp[i - 1]`, exactly the values the table would hold.

#### When The Table Must Stay

Keep the full table when a later step reads an old entry at an offset that is not bounded, or when the answer needs the path that produced the value. Keep it also when a task asks for every table entry as output. The rolling form answers one final number and nothing else.

<!-- stage: variables -->
### Two Saved Values And One New Value

The method reads the integer `n` and changes nothing outside its own variables. It keeps three working values.

- **prev2** is an `int` that holds `dp[i - 2]` before the iteration for index `i`.
- **prev1** is an `int` that holds `dp[i - 1]` before the iteration for index `i`.
- **cur** is an `int` that holds the new value `dp[i]` computed in the iteration.

Each iteration computes `cur` from the two saved values, copies `prev1` into `prev2`, and copies `cur` into `prev1`. After the last iteration, `prev1` holds `dp[n]`, so the method returns `prev1`.

<!-- stage: trace -->
### Two Runs Of The Same Recurrence

#### The Correct Order For Seven Flags

The first run counts the valid settings for seven flags. The cells are the table entries `dp[0]` through `dp[7]`, which the method never stores. The pointer `i` marks the entry that the current iteration computes. At each step the variables show the window before the shift and the new value `cur`.

The window starts as 1 and 2. Each new value equals the sum of the two saved values, so the sequence reads 3, 5, 8, 13, 21 and 34. After the iteration for `dp[7]`, the variable `prev1` holds 34, which is the answer. The method touched only three variables, although the table it replaced has eight entries.

```trace
{"cells":["dp0","dp1","dp2","dp3","dp4","dp5","dp6","dp7"],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"prev2":1,"prev1":2,"cur":2},"note":"The window starts from the base entries: prev2 holds dp0 = 1 and prev1 holds dp1 = 2."},{"at":{"i":2},"vars":{"prev2":2,"prev1":3,"cur":3},"note":"The sum of 1 and 2 gives cur = 3. The shift moves 2 into prev2 and 3 into prev1."},{"at":{"i":3},"vars":{"prev2":3,"prev1":5,"cur":5},"note":"The sum of 2 and 3 gives cur = 5. The shift moves 3 into prev2 and 5 into prev1."},{"at":{"i":4},"vars":{"prev2":5,"prev1":8,"cur":8},"note":"The sum of 3 and 5 gives cur = 8. The shift moves 5 into prev2 and 8 into prev1."},{"at":{"i":5},"vars":{"prev2":8,"prev1":13,"cur":13},"note":"The sum of 5 and 8 gives cur = 13. The shift moves 8 into prev2 and 13 into prev1."},{"at":{"i":6},"vars":{"prev2":13,"prev1":21,"cur":21},"note":"The sum of 8 and 13 gives cur = 21. The shift moves 13 into prev2 and 21 into prev1."},{"at":{"i":7},"vars":{"prev2":21,"prev1":34,"cur":34},"note":"The sum of 13 and 21 gives cur = 34. The shift moves 21 into prev2 and 34 into prev1."}]}
```

#### The Wrong Order Of The Two Assignments

The second run uses the same recurrence and the same start, but the shift runs in the opposite order. The line `prev1 = cur` comes first, and `prev2 = prev1` comes second. The pointer and the cells have the same meaning as in the first run.

The first iteration is still correct, because it computes `cur` before any assignment. The damage appears after the shift. Both variables now hold the same number, so every later sum doubles that number. The values 3, 6, 12 and 24 appear in place of 3, 5, 8 and 13, and each is double its predecessor. The final result of 96 differs from the correct 34. The method runs without any error, which is why the hazard needs a deliberate check.

```trace
{"cells":["dp0","dp1","dp2","dp3","dp4","dp5","dp6","dp7"],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"prev2":1,"prev1":2,"cur":2},"note":"The window starts from the base entries: prev2 holds dp0 = 1 and prev1 holds dp1 = 2."},{"at":{"i":2},"vars":{"prev2":3,"prev1":3,"cur":3},"note":"The sum of 1 and 2 gives cur = 3. The wrong shift sets prev1 to 3 first, so prev2 also becomes 3."},{"at":{"i":3},"vars":{"prev2":6,"prev1":6,"cur":6},"note":"The sum of 3 and 3 gives cur = 6. The wrong shift sets prev1 to 6 first, so prev2 also becomes 6."},{"at":{"i":4},"vars":{"prev2":12,"prev1":12,"cur":12},"note":"The sum of 6 and 6 gives cur = 12. The wrong shift sets prev1 to 12 first, so prev2 also becomes 12."},{"at":{"i":5},"vars":{"prev2":24,"prev1":24,"cur":24},"note":"The sum of 12 and 12 gives cur = 24. The wrong shift sets prev1 to 24 first, so prev2 also becomes 24."},{"at":{"i":6},"vars":{"prev2":48,"prev1":48,"cur":48},"note":"The sum of 24 and 24 gives cur = 48. The wrong shift sets prev1 to 48 first, so prev2 also becomes 48."},{"at":{"i":7},"vars":{"prev2":96,"prev1":96,"cur":96},"note":"The sum of 48 and 48 gives cur = 96. The wrong shift sets prev1 to 96 first, so prev2 also becomes 96."}]}
```

<!-- stage: code -->
### Counting Settings With Three Variables

The method returns the same answer as the table version while it keeps three `int` values. The remainder inside the loop keeps every stored value below the modulus, so `prev1 + prev2` always fits in an `int`.

```java
static int countSettingsRolling(int n) {
    final int MOD = 1_000_000_007;
    if (n == 0) return 1;
    int prev2 = 1;
    int prev1 = 2;
    for (int i = 2; i <= n; i++) {
        int cur = (prev1 + prev2) % MOD;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

The early return handles n equal to 0, which has no loop iteration and no `dp[1]` to read. For n equal to 1, the loop body never runs and the method returns `prev1`, which holds 2. The method runs in O(n) time and uses O(1) memory.

<!-- stage: applicability -->
### Recognizing A Fixed Look Back

#### Reading The Cue

Use rolling state when every transition reads values at a fixed number of positions to the left, and the problem asks for one final number. Counting ways, maximum totals and minimum costs along a row all fit. If the statement asks only for the value at index n and never for the chosen items, the table is an implementation choice and not a requirement.

#### Checking The Invariant

An **invariant** is a condition on the variables that is true at the start of every loop iteration. Here, before the iteration for index `i`, the saved variables equal the entries `dp[i - 1]` and so on up to the window size. The shift order protects this statement. Test n equal to 0 and 1, where the loop does not run. Test the largest n against a table, because a wrong shift is silent. Test a sequence whose values hit the modulus, because the sum of two values must not overflow.

#### Avoiding The False Friend

A **false friend** is a shortcut that passes small examples and breaks on others. The first false friend is reusing the table as a single variable, which loses the second saved value. The second is shrinking a table to the last two rows or entries when the recurrence reads offset three or a whole column, which gives wrong answers without an error. The third is rolling the state when the output requires the path, because the dropped entries are the only record of the choices.

<!-- stage: exercises -->
### Exercises

#### [Build] Two-State Fibonacci (Author exercise)
<!-- id: dp-roll-two-state-fib -->

**Prerequisites.** The rolling state and the base entries of this lesson.

**Problem.** A sequence has `f(0) = a` and `f(1) = b`. For every `i >= 2`, the value is `f(i) = (f(i - 1) + f(i - 2)) mod 1000000007`. Given `a`, `b` and `n`, return `f(n)` as an `int`. The method uses a constant number of variables.

**Constraints.** The limits are:
- **Seeds** satisfy `0 <= a, b <= 1000000006`.
- **Index** satisfies `0 <= n <= 100000000`.
- **Result** is returned in the range `0..1000000006`.

**Example 1.** Input `a = 0`, `b = 1`, `n = 10`, output `55`.

**Example 2.** Input `a = 1000000006`, `b = 1000000006`, `n = 2`, output `1000000005`.

**Hint.** Which two values does the iteration for index 2 read, and what does the method return when n is 0?

**Changed decision.** The method keeps two variables and a new value instead of a table. It returns the seed `a` directly for n equal to 0, because that index is never computed.

#### [Vary] House Robber (LeetCode 198)
<!-- id: dp-roll-robber-negative -->

**Prerequisites.** The exercise above.

**Problem.** An array `nums` holds one integer for each house along a street. A selection is a set of indices in which no two indices are adjacent, and the empty set is allowed. The total of a selection is the sum of its values. Return the largest total over all selections. The values may be negative.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 100000`.
- **Values** satisfy `-10000 <= nums[i] <= 10000`.
- **Result** is at least 0, because the empty selection is allowed.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [3,-2,7,5]`, output `10`.

**Example 2.** Input `nums = [-4,-1,-6]`, output `0`.

**Hint.** What does the best total over the first i houses equal when house i is skipped, and when it is taken?

**Changed decision.** The method may skip a negative house, and the empty selection stays valid. So the two saved values start at 0, and each step takes the larger of skipping and taking.

#### [Boundary] Update Order (Author exercise)
<!-- id: dp-roll-update-order -->

**Prerequisites.** The two exercises above.

**Problem.** A sequence has three seeds `t(0) = a`, `t(1) = b` and `t(2) = c`. For every `i >= 3`, the value is `t(i) = (t(i - 1) + t(i - 2) + t(i - 3)) mod 1000000007`. Return `t(n)` as an `int`. The method keeps three saved values and reads each one before it overwrites it.

**Constraints.** The limits are:
- **Seeds** satisfy `0 <= a, b, c <= 1000000006`.
- **Index** satisfies `0 <= n <= 50000000`.
- **Sum** of three seeds can exceed the range of `int`, so the method adds in `long`.

**Example 1.** Input `a = 1`, `b = 2`, `c = 3`, `n = 6`, output `37`.

**Example 2.** Input `a = 1000000006`, `b = 1000000006`, `c = 1000000006`, `n = 3`, output `1000000004`.

**Hint.** Which of the three variables must move first when the window shifts, and what does n = 0, 1 or 2 return?

**Changed decision.** The window has three positions instead of two, so the shift has three assignments. The oldest variable is overwritten first, and the sum is computed in `long` before the remainder.

#### [Recognize] Min Cost Climbing Stairs (LeetCode 746)
<!-- id: dp-roll-min-cost-stairs -->

**Prerequisites.** All three exercises above.

**Problem.** An array `cost` gives a price for each step, where `cost[i]` is paid when a climber leaves step `i`. The climber starts on step 0 or on step 1. From step `i`, one move goes to step `i + 1` or to step `i + 2`. The top is the position `cost.length`. Return the lowest total price to reach the top.

**Constraints.** The limits are:
- **Length** satisfies `2 <= cost.length <= 100000`.
- **Prices** satisfy `0 <= cost[i] <= 999`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `cost = [4,1,9,2,8,3]`, output `6`.

**Example 2.** Input `cost = [5,0,0,5,0]`, output `0`.

**Hint.** What does the lowest price to stand on step i read from, and how many earlier values does that need?

**Changed decision.** The state is the lowest price to stand on a position, and the top is one more position than the last step. The method keeps two saved prices instead of an array of `cost.length + 1` entries.
