<!-- lesson-kind: combination -->
<!-- lesson-id: prefix-state-and-maps -->
## Prefix State And Maps

<!-- stage: context -->
### An Auditor Reading A Ledger

An auditor receives the ledger of a small bank branch, one line per day, with the net change in the branch's cash: positive when deposits won, negative when withdrawals did, and sometimes zero. She is asked several unrelated questions about it. How many stretches of consecutive days netted exactly a target amount? What was the longest stretch with as many good days as bad ones? How many stretches netted a whole number of bundles of a standard size? Is there any stretch of at least two days that does?

She notices that every question is about a stretch of consecutive days, and that each stretch's net change is the cash level at its end minus the cash level at its start. A pile of daily cash levels is easy to write down. What she lacks is a quick way to ask, for each day, about all the earlier days at once, because a ledger of a hundred thousand days has billions of stretches.

<!-- stage: contributions -->
### What Each Part Brings

The prefix state brings the meaning of a day: the cash level after it, computed in one pass, so that every stretch becomes a difference of two such levels. It can also bring a transformed level, such as a balance that rises on a good day and falls on a bad one, or a level reduced to its remainder when the question is about bundles. The prefix state alone cannot answer a question about all earlier days, because it only offers them one at a time.

The map brings memory with fast lookup: given any value, it says in constant expected time what was recorded for that value, and the map can be asked about a value the current day computed, such as the level it needs an earlier day to have had. The map alone has no meaning for its keys. A table of numbers with nothing to say what each number stands for answers nothing, and the answer to every question below depends on what the key is. The combination is the pairing of a key chosen from the question with a role chosen from the question, and the recognition cue is a question about stretches whose answer can be stated as a relation between two prefix keys.

<!-- stage: naive -->
### Check Every Stretch Directly

The direct approach is to try every first day and every last day, keep the net change of the stretch in a running variable, and test the stretch against the target.

```java
static long countStretches(int[] ledger, long target) {
    long count = 0;
    for (int first = 0; first < ledger.length; first++) {
        long net = 0;
        for (int last = first; last < ledger.length; last++) {
            net += ledger[last];
            if (net == target) count++;
        }
    }
    return count;
}
```

It counts every stretch exactly once, and it uses a `long` net change so large entries do not wrap.

<!-- stage: bottleneck -->
### Billions Of Stretches Visited One By One

A ledger of n days has about n squared over two stretches, and the loop visits every one, so the cost is O(n^2), which is five billion visits for a hundred thousand days. The loop recomputes each net change from scratch for the next first day, even though every net change is a difference of two cash levels that one pass could have produced.

For a fixed last day, the stretches that qualify are those whose start level has a specific value, determined by the question and by the level at the last day. Asking "how many earlier days had that level" or "where was the earliest one" is a lookup in a table filled as the pass moves forward. With O(1) expected work per day, the whole ledger costs O(n), and the only decisions left are what the key is and what the table stores.

<!-- stage: insight -->
### Choose The Key, Then Choose The Role

The **prefix key** is the value of the prefix state that the question compares. For a target sum it is the raw running total, and the earlier key that pairs with the current one is the current total minus the target. For equal numbers of two kinds of day it is a balance that moves up and down by one. For divisibility it is the running total reduced by `Math.floorMod`, and two equal keys pair. The key is the first decision, and the rule that two keys pair is the second.

The map then plays one of two roles. In the **frequency role**, it records how many times each key has occurred, and the answer grows by the count found for the paired key, which is the right role when the question counts stretches. In the **first-index role**, it records only the earliest position at which each key occurred, and a lookup gives the widest stretch ending now, which is the right role for the longest stretch, or for a rule about length. The role is the third decision, and it is a mistake to use one where the other is meant: a frequency table has no positions, and a first-index table has no counts.

<!-- names: prefix key, frequency role, first-index role -->

All four questions of the auditor share one skeleton. Seed the map with the key of the empty prefix before the pass, update the running state with the day, look up the paired key, use the answer, and only then record the current key. Looking up before recording prevents a day from pairing with itself, and the seed lets a stretch begin on the first day. The invariant is that, when day `i` is processed, the map describes exactly the keys of the prefixes that end before day `i`.

<!-- stage: variables -->
### Key, Pair Rule, Table And Answer

`key` is the prefix key of the current day, computed from a running state kept in a `long` unless the bounds make an `int` safe. `pair` is the earlier key that makes a stretch qualify, such as `key - target`, the same key for balance and remainder questions, or a mask. `table` is the map, with entries recorded after each lookup, and its values are counts in the frequency role or indices in the first-index role. The answer is a `long` when counts can pass the range of `int`. One more habit belongs to Java: the key type of the map and the type of the lookup value must be the same boxed type.

<!-- stage: trace -->
### Two Roles On Two Ledgers

The first trace counts the stretches netting exactly 1000000000 in the ledger 1000000000, 1000000000, -1000000000, using the frequency role with long keys. See the third day: the running total returns to 1000000000, the paired key is zero, and the seed contributes one, so the whole ledger from the first day counts as a stretch.

```trace
{"cells":["1000000000","1000000000","-1000000000"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":1000000000,"pairKey":0,"found":1,"count":1},"note":"The running total is 1000000000 and the paired key is 0. The table holds it 1 times, so the count is 1."},{"at":{"i":1},"vars":{"total":2000000000,"pairKey":1000000000,"found":1,"count":2},"note":"The running total is 2000000000 and the paired key is 1000000000. The table holds it 1 times, so the count is 2."},{"at":{"i":2},"vars":{"total":1000000000,"pairKey":0,"found":1,"count":3},"note":"The running total is 1000000000 and the paired key is 0. The table holds it 1 times, so the count is 3."}]}
```

The second trace uses the first-index role to find the stretch of at least two days whose total is a multiple of 6 and whose last day is earliest, in the ledger 23, 2, 4, 6, 7. The key is the running total reduced by 6. Consider the third day: the key 5 was first seen on the first day, the gap is two days, and the stretch from index 1 to index 2 is reported.

```trace
{"cells":["23","2","4","6","7"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":23,"key":5},"note":"The total is 23 and the key is 5, which is new, so record index 0 as its first position."},{"at":{"i":1},"vars":{"total":25,"key":1},"note":"The total is 25 and the key is 1, which is new, so record index 1 as its first position."},{"at":{"i":2},"vars":{"total":29,"key":5,"firstIndex":0,"start":1,"end":2},"note":"The key 5 was first seen at index 0, the gap is 2, so the stretch from 1 to 2 qualifies and the scan stops."}]}
```

<!-- stage: code -->
### One Skeleton, Three Keys

```java
static long subarraySumLong(int[] nums, long k) {
    Map<Long, Integer> seen = new HashMap<>();
    seen.put(0L, 1);
    long balance = 0, count = 0;
    for (int x : nums) {
        balance += x;
        count += seen.getOrDefault(balance - k, 0);
        seen.merge(balance, 1, Integer::sum);
    }
    return count;
}

static int[] longestBalancedSpan(int[] nums) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);
    int balance = 0, bestLen = 0, bestStart = -1, bestEnd = -1;
    for (int i = 0; i < nums.length; i++) {
        balance += nums[i] == 1 ? 1 : -1;
        Integer earlier = first.get(balance);
        if (earlier == null) first.put(balance, i);
        else if (i - earlier > bestLen) {
            bestLen = i - earlier;
            bestStart = earlier + 1;
            bestEnd = i;
        }
    }
    return new int[] {bestStart, bestEnd};
}

static long divisibleStretches(int[] nums, int k) {
    Map<Integer, Integer> seen = new HashMap<>();
    seen.put(0, 1);
    long total = 0, count = 0;
    for (int x : nums) {
        total += x;
        int cls = (int) Math.floorMod(total, (long) k);
        count += seen.getOrDefault(cls, 0);
        seen.merge(cls, 1, Integer::sum);
    }
    return count;
}

static int[] earliestGoodPair(int[] nums, int k) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);
    long total = 0;
    for (int i = 0; i < nums.length; i++) {
        total += nums[i];
        int cls = (int) Math.floorMod(total, (long) k);
        Integer earlier = first.get(cls);
        if (earlier == null) first.put(cls, i);
        else if (i - earlier >= 2) return new int[] {earlier + 1, i};
    }
    return new int[] {-1, -1};
}
```

Each function does one pass with O(1) expected work per day, and the table holds at most one entry per distinct key. The first function seeds with `0L`, so that its key has the same boxed type as every later key.

<!-- stage: applicability -->
### When Stretches Hide A Key Match

Use this pairing when a question about contiguous stretches can be restated as a relation between the prefix keys at the stretch's two ends, and the number of keys is manageable. The invariant is the one of the skeleton: the table describes the keys of prefixes that end before the current day, the lookup precedes the record, and the table was seeded with the empty prefix.

A false friend is the table whose keys have no stated meaning, built by copying an earlier solution without asking what is being compared. Another is the wrong role: counting with an index table or measuring with a count table. A third is the key reduced in the wrong way, such as `%` on a negative total. A fourth is a sliding window, which is a different tool and fails when values can be negative.

In Java, keep the key type of the map identical to the type used in lookups: `Map<Long, Integer>` is searched with a `long`, since `get(0)` boxes an `Integer` and never matches a stored `Long`. Choose `long` for running totals and counts when the bounds allow large values. Normalize remainders with `Math.floorMod`, and remember that a first-index table must be read with a nullable `Integer` so that index zero is not mistaken for a missing entry.

<!-- stage: exercises -->
### Exercises

#### [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: ps-combo-subarray-sum-long -->

**Prerequisites.** The prefix counts lesson, and boxing rules for `Map<Long, Integer>`.

**Problem.** Count the non-empty contiguous stretches of an integer array that sum to `k`, where entries are as large as a billion and `k` may be a `long`. Use a map keyed by `Long`, seeded with the key `0L`, and show that a lookup made with an `int` key silently finds nothing.

**Constraints.** 1 <= nums.length <= 100000, -1000000000 <= nums[i] <= 1000000000, and -100000000000000 <= k <= 100000000000000. The running total needs `long`.

**Example 1.** Input `nums = [1000000000, 1000000000, -1000000000], k = 1000000000`, output 3.

**Example 2.** Input `nums = [5, -5, 5], k = 0`, output 2.

**Hint.** What is the type of the running total? What does `seen.get(0)` look up in a `Map<Long, Integer>`?

**Changed decision.** The key type widens to `long`, so the seed and every lookup must use the same boxed type as the stored keys.

#### [Vary] Contiguous Array (LeetCode 525)
<!-- id: ps-combo-contiguous-array-span -->

**Prerequisites.** The Subarray Sum Equals K exercise above, and the earliest balance lesson.

**Problem.** For an array of zeros and ones, return the first and last indices of the longest stretch with equal numbers of zeros and ones, as `[start, end]`, and return `[-1, -1]` if there is none. If several stretches share the longest length, return the one with the smallest start. Keep the first index of each balance and update the best stretch only on a strictly longer length.

**Constraints.** 1 <= nums.length <= 100000 and each `nums[i]` is 0 or 1.

**Example 1.** Input `nums = [0, 1, 0, 0, 1, 1, 0]`, output `[0, 5]`.

**Example 2.** Input `nums = [1, 1, 1]`, output `[-1, -1]`.

**Hint.** Which index is the first position of the stretch when a balance repeats? Which comparison keeps the earliest of equal-length stretches?

**Changed decision.** The answer is the stretch itself and not its length, so both ends are recorded and ties are broken by strict comparison.

#### [Boundary] Subarray Sums Divisible by K (LeetCode 974)
<!-- id: ps-combo-divisible-large-k -->

**Prerequisites.** The two exercises above, and the remainder classes lesson.

**Problem.** Count the non-empty stretches whose sum is divisible by `k`, where `k` can be as large as a billion, so an array of `k` counters is not possible, and where the count can pass the range of `int`. Use a map from the normalized remainder to a count, and a `long` answer.

**Constraints.** 1 <= nums.length <= 100000, -1000000000 <= nums[i] <= 1000000000, and 1 <= k <= 1000000000.

**Example 1.** Input `nums = [4, 5, 0, -2, -3, 1], k = 5`, output 7.

**Example 2.** Input 100000 zeros and `k = 1000000000`, output 5000050000.

**Hint.** How many pairs of equal keys are there when all keys are zero? What type holds that count?

**Changed decision.** The class space is too large for an array, so a map replaces it, and the answer widens to `long`.

#### [Recognize] Continuous Subarray Sum (LeetCode 523)
<!-- id: ps-combo-continuous-pair -->

**Prerequisites.** All three exercises above.

**Problem.** Find the stretch of at least two numbers, with a sum that is a multiple of `k`, whose last index is the smallest possible, and among those the smallest start. Return it as `[start, end]`, or `[-1, -1]` if there is none. Keep the first index of each remainder, and stop at the first pair that is far enough apart.

**Constraints.** 1 <= nums.length <= 100000, 0 <= nums[i] <= 1000000000, and 1 <= k <= 2147483647.

**Example 1.** Input `nums = [23, 2, 4, 6, 7], k = 6`, output `[1, 2]`.

**Example 2.** Input `nums = [23, 2, 6, 4, 7], k = 13`, output `[-1, -1]`.

**Hint.** Why does the first stored index of a remainder give the smallest start for a given end? Why can the loop stop at the first valid pair?

**Changed decision.** The answer is the earliest-ending stretch, so the scan stops at the first valid pair and reports the indices.
