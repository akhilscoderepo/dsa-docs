<!-- lesson-kind: standard -->
<!-- lesson-id: memo-and-table -->
## Cache Results Or Fill A Table

<!-- stage: context -->
### A Test That Runs For Minutes

A developer writes a unit test for a sequence generator. The generator defines `F(0) = 0`, `F(1) = 1`, and `F(n) = F(n - 1) + F(n - 2)` for larger `n`. The recurrence is clear, and the recursive method that mirrors it is three lines long. The test checks `F(10)` and passes in a blink. A second test checks `F(50)`, and the test runner kills it after ten minutes without a result.

Nothing in the method is wrong, so the reader needs to ask what the machine is doing for those ten minutes. The same value is computed many times, and nothing keeps the earlier results. This lesson asks how to compute each value once, and it compares two ways to do that: remembering answers during the recursion, and filling an array in a planned order. Both methods read an integer `n`, return a `long`, and change no input.

<!-- stage: naive -->
### Recursing Straight From The Formula

The most direct code copies the formula. The method returns `n` when `n` is 0 or 1. Otherwise it adds the results of two recursive calls.

```java
static long fibPlain(int n) {
    if (n < 2) return n;
    return fibPlain(n - 1) + fibPlain(n - 2);
}
```

The code is correct for every `n` whose result fits in a `long`. It is also a faithful picture of the recurrence, which makes it a good first draft.

```predict
How many calls to fibPlain does the single call fibPlain(5) make in total, counting the first call?

It makes 15 calls. The call for 5 makes calls for 4 and 3. The call for 4 makes calls for 3 and 2, so the value for 3 is computed twice. Each smaller value is recomputed again and again, and the count of calls roughly grows by a factor of 1.6 for each increase of n by one.
```

<!-- stage: bottleneck -->
### The Call Count Grows Exponentially

Let `C(n)` be the number of calls made by `fibPlain(n)`. A call with `n < 2` is a single call, and any other call adds the calls of its two children plus itself. So `C(n) = C(n - 1) + C(n - 2) + 1`, which gives 15 calls for `n = 5`. The count is larger than `F(n)` itself, and `F(n)` grows by the factor 1.618 per step. The method therefore runs in O(1.618^n) time, which is exponential.

For `n = 50` the method makes about 40 billion calls. At one billion simple calls per second that is still around 40 seconds of pure call overhead, and each call costs more than a simple operation. The test with `n = 50` cannot pass in a reasonable time, and `n = 90` would take well over a century.

The tree of calls shows where the time goes. The value for 3 appears under both children of the call for 5, and each copy repeats its whole subtree. There are only `n + 1` distinct arguments, and the method computes a single answer for each argument many times. A fix has to compute each argument once and reuse the result. Two orderings achieve this, and the next section develops both.

<!-- stage: insight -->
### Compute Each Argument Only Once

The goal is to reduce the work to one computation per distinct argument. That brings the cost from exponential to O(n), since there are `n + 1` arguments and each does a constant amount of work.

<!-- names: memoization, tabulation, dependency order -->

#### Memoization Stores Finished Answers

**Memoization** keeps the recursive method and adds a cache, an array indexed by the argument. The method first checks the cache for its argument. When an answer exists, the method returns it without recursing. Otherwise it computes the answer from smaller arguments, stores it in the cache, and returns it. The cache holds only completed answers. A value is written after its computation ends and never before, so a later call never reads a half-built result.

#### Mark Empty Slots With A Value That Is Not An Answer

A new `long[]` starts with every entry 0. The value `F(0)` is 0 as well, so the entry 0 cannot mean "not computed yet". A method that tests `memo[n] != 0` would recompute `F(0)` every time, and in other problems it would return wrong answers. The cache needs a marker that no real answer can equal, such as `-1` here, set for every entry with `Arrays.fill`.

#### Tabulation Fills An Array In A Fixed Order

**Tabulation** removes the recursion. The entries `0` to `n` are computed in increasing order of index with a plain loop. An entry reads only entries with smaller indexes, and the loop has already finished those. The array is the cache, and the loop order guarantees that every read finds a final value. Memoization lets the recursion discover the order, and tabulation sets the order in advance.

#### Dependency Order Decides The Loop

The **dependency order** of a recurrence says which entries must be final before another entry can be computed. For `F(i)` the entries `i - 1` and `i - 2` come first, so the loop runs upward. A recurrence that reads larger indexes needs a loop that runs downward. Writing the loop in the wrong direction reads entries that still hold their default value, and the result is silently wrong with no exception.

#### Sizing The Array And Its Two Base Entries

The table needs the indexes 0 through `n`, so it has `n + 1` entries. The base entries `F(0)` and `F(1)` are set before the loop. For `n = 0` the array would have a single entry, and writing entry 1 would throw `ArrayIndexOutOfBoundsException`. The size `Math.max(2, n + 1)` or a guard on `n` protects the base entries.

#### Comparing Memory And Reach

Both forms take O(n) time and O(n) memory for the cache. Memoization also holds up to `n` active calls on the call stack, and a deep chain can throw `StackOverflowError` at a depth of some thousands. Tabulation uses no recursion. Memoization computes only the arguments that the answer needs, which helps when many arguments are never reached.

<!-- stage: variables -->
### Cache Array, Marker, And Loop Index

Both methods read the integer `n`, which is at least 0, and change nothing outside their own arrays. The working values are listed below.

- **memo** is a `long[]` of length `n + 1`; entry `k` holds `F(k)` when it is final and `-1` otherwise.
- **table** is a `long[]` of length at least 2; the tabulated method fills entry `i` from entries `i - 1` and `i - 2`.
- **i** is the loop index of the tabulated method; it runs from 2 to `n` in increasing order.
- **depth** is the number of active calls of the memoized method; it reaches `n` before the first answer is stored.

The marker `-1` is safe because every Fibonacci number is at least 0. Each entry changes from the marker to its final value exactly once.

<!-- stage: trace -->
### Two Runs Of The Fibonacci Table

#### Memoized Calls For Six

The first run follows the memoized method for `F(6)`. The pointer `call` marks the argument of the call that just finished. The variable `depth` is the number of active calls when it finished, `filled` is the number of cache entries that hold a final value, and `calls` counts the finished calls so far. The note says whether the call computed its value or found it in the cache.

The method first descends through the arguments 5, 4, 3 and 2 to the base calls for 1 and 0. Then each call for 2, 3, 4, 5 and 6 stores a value, so five cache entries become final. Three calls find a cache hit, for the arguments 2, 3 and 4. The second call for 1, made by the call for 3, is a base case, so it needs no cache. The method makes 11 calls, instead of the 25 calls that the plain recursion makes for `n = 6`.

```trace
{"cells":["0","1","2","3","4","5","6"],"pointers":["call"],"steps":[{"at":{"call":1},"vars":{"depth":6,"filled":0,"calls":1},"note":"The call for 1 is a base case and returns 1 without touching the cache."},{"at":{"call":0},"vars":{"depth":6,"filled":0,"calls":2},"note":"The call for 0 is a base case and returns 0 without touching the cache."},{"at":{"call":2},"vars":{"depth":5,"filled":1,"calls":3},"note":"The call for 2 adds its two smaller answers and stores 1."},{"at":{"call":1},"vars":{"depth":5,"filled":1,"calls":4},"note":"The call for 1 is a base case and returns 1 without touching the cache."},{"at":{"call":3},"vars":{"depth":4,"filled":2,"calls":5},"note":"The call for 3 adds its two smaller answers and stores 2."},{"at":{"call":2},"vars":{"depth":4,"filled":2,"calls":6},"note":"The call for 2 finds its answer in the cache and returns at once."},{"at":{"call":4},"vars":{"depth":3,"filled":3,"calls":7},"note":"The call for 4 adds its two smaller answers and stores 3."},{"at":{"call":3},"vars":{"depth":3,"filled":3,"calls":8},"note":"The call for 3 finds its answer in the cache and returns at once."},{"at":{"call":5},"vars":{"depth":2,"filled":4,"calls":9},"note":"The call for 5 adds its two smaller answers and stores 5."},{"at":{"call":4},"vars":{"depth":2,"filled":4,"calls":10},"note":"The call for 4 finds its answer in the cache and returns at once."},{"at":{"call":6},"vars":{"depth":1,"filled":5,"calls":11},"note":"The call for 6 adds its two smaller answers and stores 8."}]}
```

#### Tabulated Entries For Eight

The second run fills a table for `n = 8` with a loop. The pointer `i` marks the entry being filled. The variables `left` and `right` hold the values read from entries `i - 2` and `i - 1`. The two base entries 0 and 1 are set before the loop starts.

Each step reads two final entries and writes one. Because the loop runs upward, no read ever lands on an unfilled entry. The loop performs 7 additions, from index 2 to index 8, and the last entry is 21.

```trace
{"cells":["0","1","2","3","4","5","6","7","8"],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"left":0,"right":0},"note":"Before the loop, the base entries are set: entry 0 is 0 and entry 1 is 1."},{"at":{"i":2},"vars":{"left":0,"right":1},"note":"Entry 2 adds 0 and 1, and stores 1."},{"at":{"i":3},"vars":{"left":1,"right":1},"note":"Entry 3 adds 1 and 1, and stores 2."},{"at":{"i":4},"vars":{"left":1,"right":2},"note":"Entry 4 adds 1 and 2, and stores 3."},{"at":{"i":5},"vars":{"left":2,"right":3},"note":"Entry 5 adds 2 and 3, and stores 5."},{"at":{"i":6},"vars":{"left":3,"right":5},"note":"Entry 6 adds 3 and 5, and stores 8."},{"at":{"i":7},"vars":{"left":5,"right":8},"note":"Entry 7 adds 5 and 8, and stores 13."},{"at":{"i":8},"vars":{"left":8,"right":13},"note":"Entry 8 adds 8 and 13, and stores 21."}]}
```

<!-- stage: code -->
### Memoized And Tabulated Forms

The first method keeps the recursion and adds the cache. The second method replaces the recursion with a loop. Both return a `long`.

```java
static long fibMemo(int n) {
    long[] memo = new long[n + 1];
    Arrays.fill(memo, -1);
    return fibFrom(n, memo);
}

static long fibFrom(int k, long[] memo) {
    if (k < 2) return k;
    if (memo[k] != -1) return memo[k];
    memo[k] = fibFrom(k - 1, memo) + fibFrom(k - 2, memo);
    return memo[k];
}

static long fibTable(int n) {
    long[] table = new long[Math.max(2, n + 1)];
    table[1] = 1;
    for (int i = 2; i <= n; i++) table[i] = table[i - 1] + table[i - 2];
    return table[n];
}
```

The base case in `fibFrom` returns before the cache is read, so the array never needs entries below 2 for the recursion. The sum is a `long`, and `F(92)` is the last Fibonacci number that fits, because `F(93)` wraps around to a negative value without any error. Both methods run in O(n) time. Memoization uses O(n) memory for the cache and O(n) for the call stack. Tabulation uses O(n) memory for the table.

<!-- stage: applicability -->
### Choosing Between The Two Forms

#### Reading The Cue

Use this lesson when a recurrence is clear and a direct recursion repeats arguments. A recursive method whose arguments come from a small range is the typical sign. Count the distinct arguments. When that count is small and each argument needs constant work, caching reduces the cost to the product of the two numbers.

#### Checking The Invariant

An **invariant** is a condition that stays true while the loop or recursion runs. For memoization the invariant is that every cache entry is either the marker or the final answer for its argument. For tabulation it is that every entry the loop reads has already been finalized. Test the smallest inputs, `n = 0` and `n = 1`, where the array size and base entries decide whether the code runs. Test a mid-size value against a hand calculation, and test the largest value that fits.

#### Avoiding The False Friend

A **false friend** is a habit that works on easy cases and breaks on others. One is a cache marker of 0 for a problem whose answers can be 0. Another is a cache keyed by only some of the arguments, which returns an answer computed for a different call. The third is a table loop in the wrong direction, which reads default values and gives wrong results silently. Caching also does not help when every call has a distinct argument, because then nothing repeats.

<!-- stage: exercises -->
### Exercises

#### [Build] Memoized Fibonacci (Author exercise)
<!-- id: dp-memo-fib-cache -->

**Prerequisites.** The memoization sections of this lesson.

**Problem.** The sequence `F` satisfies `F(0) = 0`, `F(1) = 1`, and `F(n) = F(n - 1) + F(n - 2)` for `n >= 2`. Write a recursive method that returns `F(n)` as a `long`. The method keeps a cache of completed answers and computes each value of `F(k)` for `k <= n` at most once.

**Constraints.** The limits are:
- **Index** satisfies `0 <= n <= 90`.
- **Result** fits in a `long`.
- **Cache** uses a marker that no Fibonacci number equals.

**Example 1.** Input `n = 50`, output `12586269025`.

**Example 2.** Input `n = 0`, output `0`.

**Hint.** If the cache marker were 0, which call would never be remembered, and what would that cost?

**Changed decision.** The method returns a cached value before it recurses, and it stores a value only after both recursive calls have returned.

#### [Vary] Bottom-Up Fibonacci (Author exercise)
<!-- id: dp-memo-fib-table -->

**Prerequisites.** The exercise above, and the section on tabulation.

**Problem.** Let `F` be the sequence from the exercise above. Given `n` and a modulus `m`, return a `long[]` of length `n + 1` whose entry `i` equals `F(i)` modulo `m`. Fill the array with a loop and no recursion.

**Constraints.** The limits are:
- **Index** satisfies `0 <= n <= 1000`.
- **Modulus** satisfies `1 <= m <= 2000000000`.
- **Sums** may reach `4 * 10^9`, so they must be computed as `long`.

**Example 1.** Input `n = 6`, `m = 10`, output `[0,1,1,2,3,5,8]`.

**Example 2.** Input `n = 10`, `m = 7`, output `[0,1,1,2,3,5,1,6,0,6,6]`.

**Hint.** Which entries does index `i` read, and in which direction must the loop run so that both are final?

**Changed decision.** The loop replaces the recursion and every entry is reduced modulo `m` as it is stored. For `m = 1` every entry is 0, including the base entries.

#### [Boundary] Zero And One (Author exercise)
<!-- id: dp-memo-zero-one -->

**Prerequisites.** The two exercises above.

**Problem.** The Lucas sequence `L` satisfies `L(0) = 2`, `L(1) = 1`, and `L(n) = L(n - 1) + L(n - 2)` for `n >= 2`. Return `L(n)` as a `long`, using a table that is filled in increasing index order.

**Constraints.** The limits are:
- **Index** satisfies `0 <= n <= 80`.
- **Result** fits in a `long`.
- **Table** must have a valid entry for each base index even when `n` is 0.

**Example 1.** Input `n = 0`, output `2`.

**Example 2.** Input `n = 5`, output `11`.

**Hint.** What is the length of the array for `n = 0`, and which line writes to index 1?

**Changed decision.** Both base entries are non-zero or distinct from the Fibonacci pair, so a table that assumes `table[0] = 0` fails. The array length is the larger of 2 and `n + 1`.

#### [Recognize] Stairs With Broken Steps (LeetCode 70)
<!-- id: dp-memo-stairs-broken -->

**Prerequisites.** All three exercises above.

**Problem.** A staircase has steps numbered 0 to `n`. A climber starts on step 0 and each move climbs 1 or 2 steps. The array `broken` lists steps on which the climber must never land. Step 0 is never broken. Return the number of different move sequences that land exactly on step `n`, as a `long`. Implement the memoized form and the tabulated form, and use the same answer from both.

**Constraints.** The limits are:
- **Steps** satisfy `0 <= n <= 60`.
- **Broken** has distinct values in `1..n`, listed in increasing order, and may be empty.
- **Result** fits in a `long`, and it is 0 when step `n` is broken.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `n = 5`, `broken = [3]`, output `2`.

**Example 2.** Input `n = 3`, `broken = [3]`, output `0`.

**Hint.** What should the entry of a broken step hold, and how many calls are active at once in the memoized form when `broken` is empty?

**Changed decision.** A broken step stores 0 instead of the sum of its two predecessors, so ways never pass through it. The table needs O(n) memory, and the memoized form needs O(n) more for its call stack.
