<!-- lesson-kind: standard -->
<!-- lesson-id: set-sequences -->
## Extend Runs With A Set

<!-- stage: context -->
### The Longest Block Of Ticket Numbers

A support desk receives ticket numbers in the order the tickets close. That order differs from the order of issue. An auditor wants the longest block of consecutive numbers in a batch of up to 100000 tickets, because the gaps between blocks show tickets that are still open. A batch with ten thousand tickets gives an answer at once. A batch with a hundred thousand consecutive numbers, closed in shuffled order, keeps the program busy for minutes.

The program is correct, but it does a large amount of work twice. The question is which part of a block the program measures more than once, and how one test on a single number can tell the program where a block begins.

<!-- stage: naive -->
### Walking Upward From Every Number

The direct method puts all numbers in a set. From each number it walks upward, testing whether the next number is in the set, and it records the longest walk.

```java
static int longestBlock(int[] nums) {
    Set<Integer> all = new HashSet<>();
    for (int x : nums) {
        all.add(x);
    }
    int best = 0;
    for (int x : all) {
        int len = 1;
        while (all.contains(x + len)) {
            len++;
        }
        best = Math.max(best, len);
    }
    return best;
}
```

On `[100, 4, 200, 1, 3, 2]` the walks from 1, 2, 3 and 4 have lengths 4, 3, 2 and 1, and the method returns 4. The loop visits each distinct number once.

<!-- stage: bottleneck -->
### Every Block Member Starts A Walk

```predict
The batch holds the numbers 1 to 100000 in shuffled order. How many membership tests does the method make in total, and which of those tests repeat earlier work?

The walk from the number v tests the 100000 - v numbers above it, so the total is about n * n / 2 = 5 billion tests, which is O(n^2). The walk from 2 repeats the whole walk from 1 except for its first step, and each later number repeats a suffix of the walk before it.
```

A block of length `L` contains `L` numbers, and each of them starts a walk. The walk from the first number visits all `L` numbers. The walk from the second number visits the last `L - 1` of them again, and so on. The work per block grows with `L * L`. Only the walk from the first number of a block matters. The program needs a cheap test that tells whether a number is the first of its block, so that the other numbers of the block skip the walk.

<!-- stage: insight -->
### Walk Only From The First Number

#### Recognize The First Number With One Test

A **run** is a maximal set of consecutive integers `x, x + 1, ..., x + k - 1` that all occur in the input. The number `x` is the **run start** exactly when `x - 1` does not occur in the input. One membership test on `x - 1` therefore decides whether `x` starts a run.

<!-- names: run start, predecessor test, successor walk -->

#### Skip The Numbers That Are Not Starts

The **predecessor test** checks `all.contains(x - 1)`. When it succeeds, the number `x` lies inside a run whose start the loop visits at some point, so the loop skips `x`. When it fails, the loop begins the **successor walk**, which tests `x + 1`, `x + 2` and so on until a test fails. The length of the walk is the length of the run.

#### The Invariant That Bounds The Work

Every run has exactly one start, so the loop walks each run once. Every number of the input belongs to exactly one run. The successor walks therefore visit each distinct number once in total, and the predecessor test visits each distinct number once more. The cost is O(n) on average, which replaces the O(n^2) of the naive version. The loop must iterate over the set and not over the array. A number that occurs three times in the array would start three identical walks, but it occurs once in the set.

#### Choose The Answer Convention

A question about the longest run can return the length, or the start of the longest run, or both. When two runs tie, the contract picks the smaller start or the first found. The loop compares `len > best` for the first found and compares starts too when the contract names the smaller start.

<!-- stage: variables -->
### Set, Start And Walk Length

The loop keeps three pieces of state.

- **all** is the set of distinct input numbers, and it stays fixed once the loop starts.
- **x** is the number the loop currently visits, and it starts a run only if `x - 1` is absent.
- **len** is the length of the successor walk from `x`, and it resets to 1 for every run start.

<!-- stage: trace -->
### Finding Run Starts In Two Sets

#### Two Blocks Of Equal Length

Take `nums = [50, 12, 13, 49, 11, 51, 52, 14]`. The number 50 has 49 in the set, so the loop skips it. The numbers 12 and 13 skip for the same reason. The number 49 has no 48, so it starts a run, and the walk finds 50, 51 and 52, which gives length 4. The number 11 has no 10, so it starts a run with 12, 13 and 14, which also gives length 4. The tie goes to the smaller start 11.

#### Duplicates In The Array

Now take `nums = [3, 3, 2, 1, 1, 9]`. The set holds 3, 2, 1 and 9 in order of first appearance, so the loop visits each number once. The numbers 3 and 2 have predecessors and skip. The number 1 has no 0, so it starts a walk that reaches 2 and 3 and gives length 3. The number 9 has no 8 and starts a walk of length 1.

#### Stepping Through Both Inputs

```trace
{"cells":[50,12,13,49,11,51,52,14],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":50,"start":"no","best":"[0, 0]"},"note":"Value 50: 49 is in the set, so 50 lies inside a run. Skip it."},{"at":{"i":1},"vars":{"value":12,"start":"no","best":"[0, 0]"},"note":"Value 12: 11 is in the set, so 12 lies inside a run. Skip it."},{"at":{"i":2},"vars":{"value":13,"start":"no","best":"[0, 0]"},"note":"Value 13: 12 is in the set, so 13 lies inside a run. Skip it."},{"at":{"i":3},"vars":{"value":49,"start":"yes","best":"[49, 4]"},"note":"Value 49: 48 is missing, so 49 starts a run. The walk upward finds length 4. Best so far: start 49, length 4."},{"at":{"i":4},"vars":{"value":11,"start":"yes","best":"[11, 4]"},"note":"Value 11: 10 is missing, so 11 starts a run. The walk upward finds length 4. Best so far: start 11, length 4."},{"at":{"i":5},"vars":{"value":51,"start":"no","best":"[11, 4]"},"note":"Value 51: 50 is in the set, so 51 lies inside a run. Skip it."},{"at":{"i":6},"vars":{"value":52,"start":"no","best":"[11, 4]"},"note":"Value 52: 51 is in the set, so 52 lies inside a run. Skip it."},{"at":{"i":7},"vars":{"value":14,"start":"no","best":"[11, 4]"},"note":"Value 14: 13 is in the set, so 14 lies inside a run. Skip it."}]}
```

```trace
{"cells":[3,2,1,9],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":3,"start":"no","best":"[0, 0]"},"note":"Value 3: 2 is in the set, so 3 lies inside a run. Skip it."},{"at":{"i":1},"vars":{"value":2,"start":"no","best":"[0, 0]"},"note":"Value 2: 1 is in the set, so 2 lies inside a run. Skip it."},{"at":{"i":2},"vars":{"value":1,"start":"yes","best":"[1, 3]"},"note":"Value 1: 0 is missing, so 1 starts a run. The walk upward finds length 3. Best so far: start 1, length 3."},{"at":{"i":3},"vars":{"value":9,"start":"yes","best":"[1, 3]"},"note":"Value 9: 8 is missing, so 9 starts a run. The walk upward finds length 1. Best so far: start 1, length 3."}]}
```

<!-- stage: code -->
### Predecessor Test And Successor Walk

#### Finding The Longest Run

```java
static int longestRun(int[] nums) {
    Set<Integer> all = new HashSet<>();
    for (int x : nums) {
        all.add(x);
    }
    int best = 0;
    for (int x : all) {
        if (x != Integer.MIN_VALUE && all.contains(x - 1)) {
            continue;
        }
        int len = 1;
        while (x + len != Integer.MIN_VALUE && all.contains(x + len)) {
            len++;
        }
        best = Math.max(best, len);
    }
    return best;
}
```

#### What The Method Costs

Building the set takes n insertions. The loop makes one predecessor test for each distinct number. The walks together make one test for each number that lies in a run plus one failing test for each run. The expected time is O(n). The set holds up to n numbers, so the space is O(n). The two guards on `Integer.MIN_VALUE` stop the arithmetic from wrapping at the ends of the `int` range.

<!-- stage: applicability -->
### When A Set Can Extend A Run

#### Look For A Predecessor And A Successor

Use this method for an unordered sequence of numbers when the question asks about blocks of consecutive values. Each number has one predecessor and one successor, and a membership test reaches either in expected constant time. The invariant is that the set describes the whole input, and the loop starts a walk only at a number whose predecessor is absent. The same idea works for any step of fixed size, such as numbers that differ by 7.

#### Sorting Is A False Friend

A false friend here is sorting the array and scanning for neighbors. Sorting also exposes the runs, but it costs O(n log n) time, and an in-place sort changes the caller's array. The set method needs O(n) expected time and leaves the input unchanged. Sorting remains the better choice when the values are already sorted or when memory for a set is not available.

#### Java Details That Cause Failures

The call `set.contains(x + 1L)` boxes a `Long`, and a `Set<Integer>` never holds a `Long`, so the call returns false without any warning. Keep the arithmetic in `int` and guard the ends of the range. The expression `x - 1` wraps to `Integer.MAX_VALUE` when `x` is `Integer.MIN_VALUE`, which would make the predecessor test read the wrong number.

<!-- stage: exercises -->
### Exercises

#### [Build] Start Of The Longest Run (LeetCode 128)
<!-- id: hm-longest-run-start -->

**Prerequisites.** The predecessor test and the successor walk from this lesson.

**Problem.** This variation of Longest Consecutive Sequence asks for the start of the run and not only its length. Let `nums` be an integer array. A run is a maximal block of consecutive integers that all occur in `nums`. Return an `int[]` with two entries: the start of a longest run and its length. When several runs share the longest length, return the one with the smallest start. For the empty array, return `[0, 0]`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers, and duplicates may occur.
- **Answer** has exactly two entries.
- **Ties** go to the smaller start.

**Example 1.** Input `nums = [20, 5, 21, 6, 22, 7, 8]`, output `[5, 4]`.

**Example 2.** Input `nums = [9, 2, 3, 10]`, output `[2, 2]`, because the runs 2..3 and 9..10 tie and 2 is smaller.

**Hint.** Which number in each run does the loop use to start the walk, and what does the loop remember about the best run so far?

**Changed decision.** Basic case: the answer reports the start of the run, and a tie compares starts.

#### [Vary] Shared By Three Arrays (LeetCode 349)
<!-- id: hm-shared-by-three -->

**Prerequisites.** Start Of The Longest Run above and the intersection exercise from the first lesson.

**Problem.** This variation of Intersection Of Two Arrays uses three arrays. Let `a`, `b` and `c` be integer arrays. Return an `int[]` of the values that occur in all three arrays. Report each value once, in the order of its first occurrence in `a`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= a.length, b.length, c.length <= 10^4`.
- **Values** are 32-bit integers, and duplicates may occur.
- **Answer** may be empty and holds no repeated value.
- **Method** builds sets of `b` and `c` and scans `a` once.

**Example 1.** Input `a = [5, 1, 5, 2, 9]`, `b = [2, 5, 7, 5]`, `c = [5, 2, 2]`, output `[5, 2]`.

**Example 2.** Input `a = [1, 2]`, `b = [3]`, `c = [1]`, output `[]`.

**Hint.** How many membership tests does one value of `a` need, and which set stops the answer from repeating a value?

**Changed decision.** Three collections take part, so a value needs two tests, and one more set keeps the answer free of repeats.

#### [Boundary] Duplicate Starts (Author exercise)
<!-- id: hm-duplicate-starts -->

**Prerequisites.** The two exercises above.

**Problem.** Let `nums` be an integer array that may hold repeated values. Return the number of runs, where a run is a maximal block of consecutive integers that all occur in `nums`. A value that occurs many times counts once.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers.
- **Answer** is an `int` from 0 to `nums.length`.
- **Duplicates** insert into the set first, so one value never starts two runs.

**Example 1.** Input `nums = [1, 1, 2, 5, 5, 5, 9]`, output 3, for the runs `{1, 2}`, `{5}` and `{9}`.

**Example 2.** Input `nums = []`, output 0.

**Hint.** If the program counted starts while reading the array, what would happen to a repeated start?

**Changed decision.** The program counts run starts over the set of distinct values and never walks the successors.

#### [Recognize] Generator Period (LeetCode 202)
<!-- id: hm-generator-period -->

**Prerequisites.** All three exercises above and the happy number exercise from the first lesson.

**Problem.** This variation of Happy Number counts the states of a generator in place of testing for the value 1. A pseudo-random generator keeps a state `s` from 0 to 9999. Its next state is `(s * s / 100) % 10000`, using integer division. Starting from `seed`, return the number of distinct states the generator visits, counting the seed. The generator stops counting at the first state that repeats.

**Constraints.** The limits are:
- **Seed** satisfies `0 <= seed <= 9999`.
- **Arithmetic** fits in `int`, because `9999 * 9999` is below `2^31`.
- **Termination** relies on detecting a repeated state.
- **Answer** is an `int` from 1 to 10000.

**Example 1.** Input `seed = 0`, output 1, because the next state of 0 is 0.

**Example 2.** Input `seed = 1234`, output 57.

**Hint.** What must the program remember about each state, and what ends the loop?

**Changed decision.** A set holds visited states of a process, and the first repeated state ends the count.
