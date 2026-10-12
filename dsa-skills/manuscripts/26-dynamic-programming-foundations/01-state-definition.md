<!-- lesson-kind: standard -->
<!-- lesson-id: state-definition -->
## Define What Each Table Entry Means

<!-- stage: context -->
### A Counter That Never Finishes

A file-transfer tool sends a payload of `n` bytes as a sequence of chunks, and every chunk carries exactly 2 or 3 bytes. A developer needs to count the distinct chunk sequences for a given `n`, so that a test matrix covers all of them. Two sequences differ when their chunk sizes differ at any position, so 2 then 3 and 3 then 2 are two sequences. She writes a recursive counter that passes a list of the chunks sent so far. It answers `n = 12` at once. At `n = 100` the test run does not finish.

The counter is correct, and the slowness has a specific cause. The method does the same work again and again, because calls that need the same future answer look different to the machine. This lesson asks what a recursive call must remember, what it must forget, and how to write that choice as one sentence. The method reads only the integer `n`.

<!-- stage: naive -->
### Passing The Whole History Down

The direct translation of the task follows the sending process. Each call receives the number of bytes sent so far and the list of chunks chosen so far. It tries a chunk of 2, recurses, removes the chunk, then tries a chunk of 3. A call that has sent exactly `n` bytes counts as one finished sequence. A call that has sent more than `n` bytes counts as none.

```java
static long countWithHistory(int n, int sent, List<Integer> chunks) {
    if (sent == n) return 1;
    if (sent > n) return 0;
    long total = 0;
    for (int size = 2; size <= 3; size++) {
        chunks.add(size);
        total += countWithHistory(n, sent + size, chunks);
        chunks.remove(chunks.size() - 1);
    }
    return total;
}
```

The call `countWithHistory(12, 0, new ArrayList<>())` returns the right count for small `n`. Every finished sequence is built chunk by chunk and counted once.

```predict
Two calls both have sent = 10 bytes. One holds the chunks [2, 2, 3, 3] and the other holds [3, 3, 2, 2]. Do they return the same number, and does the list change that number?

They return the same number, and the list has no effect on it. Both calls count the ways to send the remaining bytes, and that count depends only on how many bytes are left. The list is only a record of the past. The method still recomputes the remaining work once for every history that reaches this point.
```

<!-- stage: bottleneck -->
### Equal Futures Are Computed Many Times

Each call to `countWithHistory` branches into two more calls, and the recursion stops only when `sent` reaches or passes `n`. The number of calls is at least the number of finished sequences. That number grows by a factor of about 1.33 for each added byte. The method therefore runs in O(1.33^n) time, which is exponential. For `n = 100` the answer is about 6.7 * 10^11, so the method makes more than that many calls and runs far longer than a test allows.

The waste does not come from the branching itself. It comes from calls that hold different arguments but need the same answer. The `sent` value tells a call how many bytes remain. The list tells it nothing useful. Because the list differs between histories, any attempt to remember an answer by its arguments would treat equal futures as different questions.

A fix has to answer a precise question first. Which arguments does the answer of a call truly depend on? Only after that choice can repeated work be shared. The next section answers it and shows how to write the choice down.

<!-- stage: insight -->
### One Sentence Defines Every Table Entry

The counter needs a smaller question that has the same form as the original. The answer to that question must not depend on how the call was reached.

<!-- names: subproblem, state, base case -->

#### A Subproblem Has The Same Form

A **subproblem** is a smaller question of the same kind as the original. The original asks for the sequences that fill `n` bytes. A subproblem asks for the sequences that fill `i` bytes, where `i` is at most `n`. The original question is the subproblem with `i = n`, so no extra translation step is needed at the end.

#### The State Holds Only What The Future Needs

The **state** of a subproblem is the smallest set of values that fully determines its answer. Two calls with equal state must return equal answers. For the chunk counter the state is the single number `i`, the byte total that a sequence must add up to. The list of chunks fails this test, because two calls with different lists and equal `i` return equal answers.

#### Write The Definition As A Sentence

Before any formula, write one complete sentence that says what `dp[i]` returns. For this task the sentence reads: `dp[i]` is the number of chunk sequences whose sizes add up to exactly `i` bytes. The sentence names what is counted, names the meaning of `i`, and says exactly and not at most. A vague sentence such as "the ways to get to `i`" hides the choice between exactly and at most, and the later formula inherits the confusion.

#### The Base Case Ends Every Chain

The **base case** is a state whose answer is known without any smaller state. The empty sequence adds up to 0 bytes, so `dp[0] = 1`. The sentence also gives the other answers. No sequence adds up to 1 byte, so `dp[1] = 0`. A state with a negative index has no meaning, so every transition must check `i - size >= 0` before it reads `dp[i - size]`.

#### The Formula Follows From The Sentence

Take any sequence that adds up to `i` bytes. Its last chunk has size 2 or 3. Removing that chunk leaves a sequence that adds up to `i - 2` or `i - 3` bytes. The two cases never overlap and together cover every sequence, so `dp[i] = dp[i - 2] + dp[i - 3]`. The sentence produced the formula, and the formula did not need to be guessed.

#### A Rule That Needs Memory Adds A Dimension

Suppose the sender may use at most one chunk of size 3. Two calls with the same `i` now have different futures when one has already used its allowed 3-chunk. The state becomes the pair (`i`, `used`), where `used` counts the 3-chunks already placed. Every value that changes the future belongs in the state, and every value that does not belongs outside it.

<!-- stage: variables -->
### Table, Index, And Chunk Size

The method reads the byte count `n` and two fixed chunk sizes, 2 and 3. It changes no input. It keeps the following working values.

- **dp** is a `long[]` of length `n + 1`; entry `i` holds the number of chunk sequences that add up to exactly `i` bytes.
- **i** is the loop index from 1 to `n`; it names the entry being filled.
- **size** is the chunk size tried for the last chunk; it is 2 or 3.

Each entry reads only entries with a smaller index, which are already final when the loop reaches `i`. The array has length `n + 1` because the indexes 0 through `n` are all valid states.

<!-- stage: trace -->
### Two Runs Of The Table

#### Chunks Of Two Or Three

The first run fills the table for `n = 10`. The pointer `i` marks the entry being filled. The variable `fromTwo` shows the value read from `dp[i - 2]`, and `fromThree` shows the value read from `dp[i - 3]`, with 0 when the index would be negative. The base entries are 1 at index 0 and 0 at index 1. From index 2 on, each entry is the sum of the two reads.

The values grow slowly at first, then faster. Index 5 gets 2 because both 2 then 3 and 3 then 2 add up to 5. The final entry `dp[10]` is 7, and the method never made a call that repeated earlier work.

```trace
{"cells":["0","1","2","3","4","5","6","7","8","9","10"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"fromTwo":0,"fromThree":0},"note":"Index 0 is the base entry. The empty sequence adds up to 0 bytes, so dp[0] is 1."},{"at":{"i":1},"vars":{"fromTwo":0,"fromThree":0},"note":"Index 1 has no valid last chunk, since both sizes are larger than 1, so dp[1] stays 0."},{"at":{"i":2},"vars":{"fromTwo":1,"fromThree":0},"note":"Index 2 adds 1 from dp[0] and has no index for a 3-chunk, so dp[2] is 1."},{"at":{"i":3},"vars":{"fromTwo":0,"fromThree":1},"note":"Index 3 adds 0 from dp[1] and 1 from dp[0], so dp[3] is 1."},{"at":{"i":4},"vars":{"fromTwo":1,"fromThree":0},"note":"Index 4 adds 1 from dp[2] and 0 from dp[1], so dp[4] is 1."},{"at":{"i":5},"vars":{"fromTwo":1,"fromThree":1},"note":"Index 5 adds 1 from dp[3] and 1 from dp[2], so dp[5] is 2."},{"at":{"i":6},"vars":{"fromTwo":1,"fromThree":1},"note":"Index 6 adds 1 from dp[4] and 1 from dp[3], so dp[6] is 2."},{"at":{"i":7},"vars":{"fromTwo":2,"fromThree":1},"note":"Index 7 adds 2 from dp[5] and 1 from dp[4], so dp[7] is 3."},{"at":{"i":8},"vars":{"fromTwo":2,"fromThree":2},"note":"Index 8 adds 2 from dp[6] and 2 from dp[5], so dp[8] is 4."},{"at":{"i":9},"vars":{"fromTwo":3,"fromThree":2},"note":"Index 9 adds 3 from dp[7] and 2 from dp[6], so dp[9] is 5."},{"at":{"i":10},"vars":{"fromTwo":4,"fromThree":3},"note":"Index 10 adds 4 from dp[8] and 3 from dp[7], so dp[10] is 7."}]}
```

#### At Most One Three-Byte Chunk

The second run adds the rule from the insight section on a rule that needs memory. The state is now the pair (`i`, `used`), where `used` is 0 or 1. The variable `zero` holds the count for sequences with no 3-chunk, and `one` holds the count for sequences with exactly one. The pointer `i` runs to 7 bytes.

A sequence with no 3-chunk reads only `zero[i - 2]`. A sequence with one reads `one[i - 2]` and `zero[i - 3]`, because adding the single allowed 3-chunk moves the pair from used = 0 to used = 1. At index 7 the answer is `zero + one`, which is 3, because the single 3-chunk has three possible positions among two 2-chunks. With a single index the two columns would merge and the rule could not be enforced.

```trace
{"cells":["0","1","2","3","4","5","6","7"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"zero":1,"one":0},"note":"Index 0 holds the empty sequence, which has no 3-chunk, so zero is 1 and one is 0."},{"at":{"i":1},"vars":{"zero":0,"one":0},"note":"Index 1 gives zero = 0 and one = 0, so the total for 1 byte is 0."},{"at":{"i":2},"vars":{"zero":1,"one":0},"note":"Index 2 gives zero = 1 and one = 0, so the total for 2 bytes is 1."},{"at":{"i":3},"vars":{"zero":0,"one":1},"note":"Index 3 gives zero = 0 and one = 1, so the total for 3 bytes is 1."},{"at":{"i":4},"vars":{"zero":1,"one":0},"note":"Index 4 gives zero = 1 and one = 0, so the total for 4 bytes is 1."},{"at":{"i":5},"vars":{"zero":0,"one":2},"note":"Index 5 gives zero = 0 and one = 2, so the total for 5 bytes is 2."},{"at":{"i":6},"vars":{"zero":1,"one":0},"note":"Index 6 gives zero = 1 and one = 0, so the total for 6 bytes is 1."},{"at":{"i":7},"vars":{"zero":0,"one":3},"note":"Index 7 gives zero = 0 and one = 3, so the total for 7 bytes is 3."}]}
```

<!-- stage: code -->
### Filling The Table From The Base

The method returns the count as a `long`. It fills the array in increasing order of `i`, so the entries it reads always hold final values.

```java
static long countChunkSequences(int n) {
    long[] dp = new long[n + 1];
    dp[0] = 1;
    for (int i = 1; i <= n; i++) {
        for (int size = 2; size <= 3; size++) {
            if (i - size >= 0) dp[i] += dp[i - size];
        }
    }
    return dp[n];
}
```

The guard `i - size >= 0` is required because index `-1` throws `ArrayIndexOutOfBoundsException` in Java. Time is O(n), since each of the `n` entries does two reads. Space is O(n) for the array. The result fits in a `long` for every `n` up to about 150, and beyond that the sum wraps around silently without any error.

<!-- stage: applicability -->
### Writing The Definition Before The Formula

#### Reading The Cue

Use this lesson when a recursive method repeats work and the answer to a call depends on a small set of its arguments. Counting problems that ask for the number of ways to build a total are typical. The first step is always the sentence, written before any code. If the sentence is not clear, the formula built on it will not be clear either.

#### Checking The Invariant

An **invariant** is a fact about the table that remains true after each step. Here the invariant is that `dp[i]` equals exactly what its sentence says for every `i` the loop has finished. Test it on the smallest inputs. Check `n = 0`, which must give 1, and `n = 1`, which must give 0. Then check that every read index is at least 0. If a hand count of a small case disagrees with the table, the sentence and the formula disagree, and the sentence is the one to fix first.

#### Avoiding The False Friend

A **false friend** is a familiar shortcut that passes simple tests and fails on other inputs. Here the shortcut is a state that is too small. A table indexed only by `i` looks natural, but it merges calls whose futures differ whenever a rule remembers something else, such as a cap on one chunk size. The opposite mistake is a state that is too large, as in the history list of the first method. A too-large state is correct and slow, and a too-small state is fast and wrong.

<!-- stage: exercises -->
### Exercises

#### [Build] Name The Subproblem (Author exercise)
<!-- id: dp-state-name-subproblem -->

**Prerequisites.** The sentence, base case and formula steps of this lesson.

**Problem.** A message of `n` bytes is sent as an ordered sequence of chunks, and every chunk has size 2 or 5. Two sequences are different when they differ in length or in any chunk size. Return the number of such sequences whose sizes add up to exactly `n`, as a `long`. The empty sequence adds up to 0 and counts as one sequence.

**Constraints.** The limits are:
- **Length** satisfies `0 <= n <= 60`.
- **Result** fits in a `long`.
- **Mutation** is not relevant, because the method receives one integer.

**Example 1.** Input `n = 12`, output `4`.

**Example 2.** Input `n = 1`, output `0`.

**Hint.** Write the sentence for `dp[i]` first, and check it on `i = 0` and `i = 1` before writing any formula.

**Changed decision.** The chunk sizes are 2 and 5 and not 2 and 3, so the formula reads two different earlier entries. The sentence is the same, with only the sizes replaced.

#### [Vary] Add One Necessary Dimension (Author exercise)
<!-- id: dp-state-add-dimension -->

**Prerequisites.** The exercise above, and the section on a rule that needs memory.

**Problem.** A message of `n` bytes is sent as an ordered sequence of chunks of size 2 or 5. The sequence may contain at most `k` chunks of size 5. Count the sequences that fill exactly `n` bytes and return that count as a `long`. For `n = 0` the only sequence is the empty one.

**Constraints.** The limits are:
- **Length** satisfies `0 <= n <= 60`.
- **Cap** satisfies `0 <= k <= 12`.
- **Result** fits in a `long`.

**Example 1.** Input `n = 12`, `k = 2`, output `4`.

**Example 2.** Input `n = 7`, `k = 0`, output `0`.

**Hint.** Two calls have the same remaining byte count and different numbers of 5-chunks left. Do they return the same number?

**Changed decision.** The table gains a second index for the number of 5-chunks used, so the state is a pair. A single index would merge calls with different futures.

#### [Boundary] Base-State Contract (Author exercise)
<!-- id: dp-state-base-contract -->

**Prerequisites.** The two exercises above.

**Problem.** A track has `n` cells numbered 0 to `n - 1`. The array `jump` has length `n`. From cell `i` a move goes forward by any whole number of cells from 1 to `jump[i]`. A move that would pass cell `n - 1` is not allowed. Return the number of different move sequences that start at cell 0 and end at cell `n - 1`, as a `long`. A track with one cell has one empty sequence.

**Constraints.** The limits are:
- **Length** satisfies `1 <= n <= 30`.
- **Jump** values satisfy `1 <= jump[i] <= 3`.
- **Result** fits in a `long`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `jump = [2,1,3,1,1]`, output `4`.

**Example 2.** Input `jump = [3]`, output `1`.

**Hint.** What does `dp[n - 1]` have to be, and what answer does a move past the last cell contribute?

**Changed decision.** The sentence describes routes that leave cell `i` and not routes that reach it, so the table fills from the last cell backward. Moves past the end must contribute 0.

#### [Recognize] Climbing With Steps Of One Or Three (LeetCode 70)
<!-- id: dp-state-stairs-one-three -->

**Prerequisites.** All three exercises above.

**Problem.** A staircase has `n` steps. Each move climbs exactly 1 step or exactly 3 steps. Two ways differ when their sequences of move sizes differ. Return the number of ways to climb from the ground to step `n`, landing exactly on step `n`, as a `long`. Climbing zero steps has one way, which is to make no move.

**Constraints.** The limits are:
- **Steps** satisfy `0 <= n <= 60`.
- **Result** fits in a `long`.

**Example 1.** Input `n = 6`, output `6`.

**Example 2.** Input `n = 2`, output `1`.

**Hint.** Is `dp[i]` the number of ways to reach step `i` or to leave it, and does the answer sit at index 0 or at index `n`?

**Changed decision.** The allowed moves are 1 and 3 and not 1 and 2, so a step 2 has only one way and the usual recurrence over the two previous entries does not apply.
