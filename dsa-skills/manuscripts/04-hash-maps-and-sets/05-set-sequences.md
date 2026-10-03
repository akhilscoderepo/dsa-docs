<!-- lesson-kind: standard -->
<!-- lesson-id: set-sequences -->
## Set Sequences

<!-- stage: context -->
### Chains Of Numbered Cards

A teacher hands numbered cards to a class, in no particular order, and some students end up holding the same number. She asks for the longest chain of consecutive numbers that the class can form, such as 11, 12, 13 and 14, with every student in the chain holding the next number up. Students may stand anywhere in the room.

A sharp student has a better idea than comparing cards in pairs. Everyone looks around the room for the number just below their own. If someone holds it, they are in the middle of a chain and sit down. Only the students whose lower neighbour is missing stay standing, and each of those walks up the chain by asking whether the next number is in the room. Each chain is then counted once, from its bottom, and no student is asked twice.

<!-- stage: naive -->
### Count Upward From Every Card

A direct version lets every student start counting. Each one asks whether the next number exists, then the one after that, until a number is missing.

```java
static int longestChainFromEveryCard(int[] cards) {
    Set<Integer> room = new HashSet<>();
    for (int c : cards) room.add(c);
    int best = 0;
    for (int c : room) {
        int len = 1;
        while (room.contains(c + len)) len++;
        best = Math.max(best, len);
    }
    return best;
}
```

For the cards `[5, 6, 7, 20]` it returns 3, from the chain 5, 6, 7. The membership tests are cheap, and the answer is correct.

<!-- stage: bottleneck -->
### Every Card Walks Its Own Chain

The set makes each question cheap, but the number of questions is the issue. In a chain of length `L`, the card at the bottom walks `L` steps, the next card walks `L - 1` steps, and so on, because each of them restarts the climb. For one chain of `n` consecutive numbers that is about `n * n / 2` membership tests, so the total is O(n * n), and with 100,000 cards in one chain it is about five billion tests.

Nearly all of that work is repeated. A card in the middle of a chain re-counts what the card below it has already counted, and it can never produce a longer chain than the card below it would. The only card whose count matters for a chain is the lowest one, and the lowest one can be recognised by a single membership test, the one for the number just below it.

<!-- stage: insight -->
### Start At The Bottom Only

Load the complete input into a set first, so that every neighbour question has a reliable answer. A **sequence start** is a value `x` for which `x - 1` is not in the set. Every maximal chain of consecutive integers has exactly one start, its smallest value, and every other value in the chain has its predecessor present. The **predecessor test** is the single membership question that classifies a value as a start or as a middle element.

Once a start is found, the **run walk** moves upward one membership test at a time, asking for `x + 1`, `x + 2` and so on until a number is missing, and the number of steps is the length of the chain. The invariant is that the set describes the whole input, so a missing neighbour truly means the chain ended there. Because only starts walk, each value in the set is visited by exactly one walk, the walk of the chain it belongs to, so the total number of membership tests over all walks is at most the number of distinct values plus the number of starts.

<!-- names: sequence start, predecessor test, run walk -->

That gives expected O(n) time, which beats sorting at O(n log n), and it does not reorder or copy the input array. Sorting is a genuine alternative when the memory for a set is a concern, but it changes the cost and, if done in place, the data. The set also removes duplicates by construction, which matters for the boundary case: inserting duplicates first means a repeated start is still one start.

<!-- stage: variables -->
### A Set Of Everything And A Cursor

The set `all` holds every distinct input value and is complete before any walk begins, which is why a missing neighbour is trustworthy. The loop variable is a candidate value, taken from the set so that duplicates cannot appear twice. For a start, the cursor `x + len` moves upward and `len` counts the chain. The best chain is kept as a length, or as a start and a length when the chain itself is needed. For questions across two collections, the set is built from one and read while scanning the other, and a value can be removed from the set once reported so that it cannot be reported again.

<!-- stage: trace -->
### Walking Chains And Reporting Once

```trace
{"cells":[50,12,13,49,11,51,52,14],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":50,"start":"no","best":"[0, 0]"},"note":"Value 50: 49 is in the set, so 50 is inside a chain. Skip it."},{"at":{"i":1},"vars":{"value":12,"start":"no","best":"[0, 0]"},"note":"Value 12: 11 is in the set, so 12 is inside a chain. Skip it."},{"at":{"i":2},"vars":{"value":13,"start":"no","best":"[0, 0]"},"note":"Value 13: 12 is in the set, so 13 is inside a chain. Skip it."},{"at":{"i":3},"vars":{"value":49,"start":"yes","best":"[49, 4]"},"note":"Value 49: 48 is missing, so 49 starts a chain. Walking upward finds length 4. Best so far: start 49, length 4."},{"at":{"i":4},"vars":{"value":11,"start":"yes","best":"[11, 4]"},"note":"Value 11: 10 is missing, so 11 starts a chain. Walking upward finds length 4. Best so far: start 11, length 4."},{"at":{"i":5},"vars":{"value":51,"start":"no","best":"[11, 4]"},"note":"Value 51: 50 is in the set, so 51 is inside a chain. Skip it."},{"at":{"i":6},"vars":{"value":52,"start":"no","best":"[11, 4]"},"note":"Value 52: 51 is in the set, so 52 is inside a chain. Skip it."},{"at":{"i":7},"vars":{"value":14,"start":"no","best":"[11, 4]"},"note":"Value 14: 13 is in the set, so 14 is inside a chain. Skip it."}]}
```

Take the cards `[50, 12, 13, 49, 11, 51, 52, 14]`. The 50 has a predecessor, 49, so it is skipped. The 12 and the 13 have predecessors and are skipped. The 49 has no 48, so it is a start and the walk finds 50, 51 and 52, a chain of length 4. The 11 is also a start with no 10, and its walk finds 12, 13 and 14, another chain of length 4. The later cards are all middles or ends and are skipped, so each chain was walked exactly once.

```trace
{"cells":[7,3,3,5,1,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":7,"pending":"{1, 3}","output":"[7]"},"note":"Value 7 is in the set, so report it and remove it. Output: [7]."},{"at":{"i":1},"vars":{"value":3,"pending":"{1}","output":"[7, 3]"},"note":"Value 3 is in the set, so report it and remove it. Output: [7, 3]."},{"at":{"i":2},"vars":{"value":3,"pending":"{1}","output":"[7, 3]"},"note":"Value 3 is not in the set, so skip it. Output: [7, 3]."},{"at":{"i":3},"vars":{"value":5,"pending":"{1}","output":"[7, 3]"},"note":"Value 5 is not in the set, so skip it. Output: [7, 3]."},{"at":{"i":4},"vars":{"value":1,"pending":"{}","output":"[7, 3, 1]"},"note":"Value 1 is in the set, so report it and remove it. Output: [7, 3, 1]."},{"at":{"i":5},"vars":{"value":7,"pending":"{}","output":"[7, 3, 1]"},"note":"Value 7 is not in the set, so skip it. Output: [7, 3, 1]."}]}
```

The second trace shows a value being reported once. The set holds `{1, 3, 7}` from the first collection, and the second collection is `[7, 3, 3, 5, 1, 7]`. The first 7 is in the set, so it is reported and removed. The 3 is reported and removed, and the next 3 is no longer in the set, so it is skipped. The 5 was never there, the 1 is reported, and the final 7 was already removed, so the output is `[7, 3, 1]`.

<!-- stage: code -->
### Spans, Shared Values, Starts And Steps

```java
static int[] longestRunSpan(int[] nums) {
    Set<Integer> all = new HashSet<>();
    for (int x : nums) all.add(x);
    int bestStart = 0, bestLen = 0;
    for (int x : all) {
        if (all.contains(x - 1)) continue;             // predecessor test: a middle element
        int len = 1;
        while (all.contains(x + len)) len++;           // run walk from the start
        if (len > bestLen || (len == bestLen && x < bestStart)) { bestLen = len; bestStart = x; }
    }
    return new int[] {bestStart, bestLen};
}

static List<Integer> sharedOnce(int[] a, int[] b) {
    Set<Integer> pending = new HashSet<>();
    for (int x : a) pending.add(x);
    List<Integer> out = new ArrayList<>();
    for (int y : b) if (pending.remove(y)) out.add(y);   // remove returns true only the first time
    return out;
}

static int countRuns(int[] nums) {
    Set<Integer> all = new HashSet<>();
    for (int x : nums) all.add(x);
    int starts = 0;
    for (int x : all) if (!all.contains(x - 1)) starts++;
    return starts;
}

static int happySteps(int n) {
    Set<Integer> states = new HashSet<>();
    int steps = 0;
    while (n != 1) {
        if (!states.add(n)) return -1;
        int next = 0;
        for (int m = n; m > 0; m /= 10) next += (m % 10) * (m % 10);
        n = next;
        steps++;
    }
    return steps;
}
```

The sequence methods are expected O(n) because each walk is paid for by a distinct start. `longestRunSpan` iterates over the set, not the array, so a repeated value cannot be tried twice. Ties in length are broken toward the smaller start, because the iteration order of a `HashSet` is unspecified and would otherwise make the answer unstable. `pending.remove(y)` returns true only the first time a value is removed, which both tests membership and marks the value as reported.

<!-- stage: applicability -->
### When Neighbours Are Tested By Value

Use set-based sequence reasoning when a numeric sequence can be extended by asking whether the successor or predecessor value exists, and the order of the input is irrelevant. The invariant is that the set describes the complete input, and only a sequence start may begin a walk. Without the start rule the method is correct but quadratic.

The false friend is sorting. Sorting also exposes runs, since neighbours in value become neighbours in position, and it needs no extra structure beyond the sorted copy, but it costs O(n log n) and either mutates the input or copies it. Another false friend is a value range that is not integer, such as strings or doubles, where "next value" has no definition.

In Java, iterate over the set and not over the original array when duplicates may exist. Do not rely on the iteration order of a `HashSet` for tie-breaking, and state the rule in the code. Be careful with `x + len` and `x - 1` near `Integer.MIN_VALUE` and `Integer.MAX_VALUE`, where the arithmetic wraps around, and widen to `long` if the constraints reach the limits of `int`. The constraints in the exercises stay well inside that range.

<!-- stage: exercises -->
### Exercises

#### [Build] Longest Consecutive Sequence (LeetCode 128)
<!-- id: hm-longest-span -->

**Prerequisites.** Membership sets lesson; the sequence start in this lesson. This is a deliberate revisit with a richer answer, reporting where the chain begins as well as how long it is.

**Problem.** Given an unsorted integer array, return the start value and the length of the longest chain of consecutive integers as a two-element array. If several chains share the longest length, return the one with the smaller start. For an empty array return `[0, 0]`.

**Constraints.** 0 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. Walk only from starts, and report the same answer on every run.

**Example 1.** Input `nums = [50, 12, 13, 49, 11, 51, 52, 14]`, output `[11, 4]`, with the tie at length 4 going to the smaller start.

**Example 2.** Input `nums = [-3, -2, -2]`, output `[-3, 2]`, since the repeated value adds nothing.

**Hint.** Which single membership test separates a start from a middle element? Which collection should the loop run over when duplicates exist?

**Changed decision.** The walk now has to remember where the best chain began, so the start is a result and not just a gate.

#### [Vary] Intersection of Two Arrays (LeetCode 349)
<!-- id: hm-shared-in-order -->

**Prerequisites.** The build exercise above; the intersection from the membership lesson.

**Problem.** Given two integer arrays, return the values that occur in both, each once, in the order in which each value first appears in the second array. Mark a value as reported by removing it from the set.

**Constraints.** 0 <= nums1.length, nums2.length <= 10^4, and values lie in -10^6..10^6. Both arrays may repeat values.

**Example 1.** Input `nums1 = [1, 3, 3, 7]`, `nums2 = [7, 3, 3, 5, 1, 7]`, output `[7, 3, 1]`.

**Example 2.** Input `nums1 = [2, 2]`, `nums2 = [2, 2, 2]`, output `[2]`.

**Hint.** What does `Set.remove` return, and how can that one call both test membership and prevent a repeat?

**Changed decision.** The output order follows the second array, and the set is consumed as values are reported.

#### [Boundary] Duplicate Starts (Author exercise)
<!-- id: hm-duplicate-starts -->

**Prerequisites.** The two exercises above.

**Problem.** Return the number of maximal runs of consecutive integers in the array, which equals the number of sequence starts. Insert all values, duplicates included, into the set before counting, and show that a repeated start is counted once.

**Constraints.** 0 <= nums.length <= 10^5. The array may hold many copies of the same value. Count starts over the set, not over the array.

**Example 1.** Input `nums = [4, 4, 5, 9, 9, 9, 2]`, output 3, from the runs `{2}`, `{4, 5}` and `{9}`.

**Example 2.** Input `nums = []`, output 0.

**Hint.** If you counted starts while looping over the array, how many times would the start 9 be counted in the first example?

**Changed decision.** The question is the number of runs, so the guard against counting a start twice is the entire answer.

#### [Recognize] Happy Number (LeetCode 202)
<!-- id: hm-happy-steps -->

**Prerequisites.** All three exercises above; the happy number from the membership lesson.

**Problem.** Replace a positive integer by the sum of the squares of its digits repeatedly. Return the number of replacements needed to reach 1, or -1 if the sequence enters a loop first. Stop as soon as a state repeats.

**Constraints.** 1 <= n <= 2^31 - 1. Store the states already visited in a set. The input 1 needs zero replacements.

**Example 1.** Input `n = 13`, output 2, through 10 and then 1.

**Example 2.** Input `n = 20`, output -1, since 20 leads to 4 and then around the loop 4, 16, 37, 58, 89, 145, 42, 20.

**Hint.** What is the first state that proves a loop, and how does a failed `add` reveal it? Where does the counter increase?

**Changed decision.** The method now reports how long the process took, so the set is a guard and the step counter is the result.
