<!-- lesson-kind: standard -->
<!-- lesson-id: direct-scans -->
## Direct Scans

<!-- stage: context -->
### Why A Lookup Returns The Wrong Index

A monitoring tool stores one day of sensor identifiers in an `int[]`. A support engineer asks where identifier 7 first appears, so the team can open the matching log line. The method answers 1, but the log line at index 1 belongs to identifier 4. Another engineer wants to fix the method by sorting the array first, because sorted data looks easier to search. The answer changes again, and it now points to a position that does not exist in the original log.

Both engineers made the same mistake. They started searching before they wrote down what a correct answer means. An index belongs to the array in its original order. Any step that moves elements also changes every index. This lesson shows how to answer position questions on unsorted data with one pass and a clear statement of what the method returns.

<!-- stage: naive -->
### Sorting The Array Before Searching

The tempting plan copies the array, sorts the copy, and calls the library binary search. Binary search is fast on sorted data, so the plan looks like an upgrade over a loop.

```java
static int firstIndexSorted(int[] nums, int target) {
    int[] sorted = nums.clone();
    Arrays.sort(sorted);
    return Arrays.binarySearch(sorted, target);
}
```

The method compiles and runs. For `nums = [7, 4, 7]` and `target = 7`, the sorted copy is `[4, 7, 7]`. The method then reports a position inside that copy, and not a position inside `nums`.

<!-- stage: bottleneck -->
### Sorting Moves Elements And Adds Cost

```predict
What does `firstIndexSorted` return for `nums = [7, 4, 7]` and `target = 7`, and is that the first index of 7 in `nums`?

It returns 1. The binary search probes the middle of `[4, 7, 7]`, finds 7 there, and stops. The first 7 in `nums` sits at index 0, so the answer is wrong. The method also gives no promise about which of several equal values it finds.
```

Two defects appear at once. The first defect is correctness. Sorting rearranges the elements, so an index in the sorted copy no longer describes `nums`. The question asked for a position in the original data, and the plan answered a different question. Carrying the original positions along would repair this, but that needs a second array of pairs and more code.

The second defect is cost. The sort alone costs O(n log n), and the copy adds O(n) memory. A loop that checks each element once costs O(n) and adds no memory that grows with the input. For `n = 100,000` the loop reads the array one time, while the sort performs well over a million comparisons before the search even starts. The sorted plan is slower, longer, and wrong for this question.

<!-- stage: insight -->
### One Pass With A Stated Result

#### Examine Each Position Once

A **linear scan** visits positions 0, 1, 2 and so on, and examines each element exactly once. Before the loop reads `nums[i]`, it has examined positions 0 to `i - 1`. The state is only the index `i` and the answer so far. Nothing else is needed, because the answer depends on one element at a time.

#### Decide When To Stop

The contract decides when the loop may stop. If the question asks for the first match, the loop may leave the moment it sees a match, because no later element can be earlier. This exit is an **early return**. If the question asks for the last match, a match proves nothing about later positions, so the loop must keep going and overwrite its answer each time it matches.

#### Mark Absence With A Value That Is Not An Index

When the scan reaches the end with no match, it must say so. The method returns -1, which is a **sentinel**: a value outside the set of legal answers. Every legal index is 0 or larger, so -1 cannot be mistaken for a position. Reaching the end of the loop is also the proof of absence, because every position was examined and none matched.

<!-- names: linear scan, early return, sentinel -->

#### Read Directly When The Index Is Given

Some questions hand over an index and ask for the element stored there. No search is involved. Reading `nums[i]` takes O(1) time, so the method reads, transforms, and stores. Choosing between a search and a read is the first decision in this chapter.

<!-- stage: variables -->
### Name The State Of A Scan

A scan needs very little state. Name each piece before writing the loop.

- **`nums`** is the input array, and the method never writes to it.
- **`target`** is the value the contract asks for.
- **`i`** is the next position to examine, from 0 up to `nums.length`.
- **`found`** is the answer so far, which starts at -1 and changes only when `nums[i] == target` and the contract allows it to change.

For a first-match method, `found` never needs to exist, because the method returns at once. For a last-match method, `found` changes on every match and is returned after the loop.

<!-- stage: trace -->
### Trace Scans That Stop And Finish

The first trace searches `[5, 2, 7, 9, 9, 4]` for the first index of 9. At `i = 0`, `i = 1` and `i = 2` the elements are 5, 2 and 7, which all differ from 9, so the scan moves on each time. At `i = 3` the element is 9. The scan returns 3 and never reads the second 9, because a first-match contract needs nothing more.

The second trace searches `[3, 8, 1, 6]` for 5. The scan compares 5 with each of the four elements and finds no match. When `i` reaches 4, the index equals `nums.length`, so no position is left. The method returns -1. The hard step is the last one, because no element triggers it. The loop condition ends the scan, and the end itself carries the proof that 5 does not occur.

```trace
{"cells":[5,2,7,9,9,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"target":9,"result":-1},"note":"i = 0: 5 differs from 9, so the scan moves on."},{"at":{"i":1},"vars":{"target":9,"result":-1},"note":"i = 1: 2 differs from 9, so the scan moves on."},{"at":{"i":2},"vars":{"target":9,"result":-1},"note":"i = 2: 7 differs from 9, so the scan moves on."},{"at":{"i":3},"vars":{"target":9,"result":3},"note":"i = 3: 9 equals 9, so the scan returns 3 and never reads the later 9."}]}
```

```trace
{"cells":[3,8,1,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"target":5,"result":-1},"note":"i = 0: 3 differs from 5, so the scan moves on."},{"at":{"i":1},"vars":{"target":5,"result":-1},"note":"i = 1: 8 differs from 5, so the scan moves on."},{"at":{"i":2},"vars":{"target":5,"result":-1},"note":"i = 2: 1 differs from 5, so the scan moves on."},{"at":{"i":3},"vars":{"target":5,"result":-1},"note":"i = 3: 6 differs from 5, so the scan moves on."},{"at":{"i":4},"vars":{"target":5,"result":-1},"note":"i = 4 equals nums.length, so every position was examined. The method returns -1."}]}
```

<!-- stage: code -->
### Write First And Last Match Scans

```java
static int firstIndex(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] == target) return i;
    }
    return -1;
}

static int lastIndex(int[] nums, int target) {
    int found = -1;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] == target) found = i;
    }
    return found;
}

static int[] readThrough(int[] nums) {
    int[] ans = new int[nums.length];
    for (int i = 0; i < nums.length; i++) ans[i] = nums[nums[i]];
    return ans;
}
```

`firstIndex` leaves the loop on the first match, so its cost is at most `n` comparisons. `lastIndex` always runs all `n` comparisons, since a later match could still replace `found`. `readThrough` is not a search at all. It reads `nums[i]`, uses that value as a second index, and writes into a new array. The new array matters, because writing into `nums` while reading it would change values that later iterations still need.

<!-- stage: applicability -->
### Check The Contract Before Scanning

#### Recognize A Direct Scan

Use a scan when the data is unsorted, any element can change the answer, and the answer comes from looking at one element at a time. The invariant is simple to state. Before the loop reads `nums[i]`, the answer is correct for the elements at positions 0 to `i - 1`. A scan also fits when the contract asks for an index, because the loop keeps the original positions intact.

#### Reject Sorting Before A Single Query

Sorting before one position query is a false friend of a scan. It looks like a way to make searching easy, yet it breaks the index meaning and costs O(n log n) against O(n). Sorting pays off only when many queries share one sorted array and the contract does not need the original positions. Chapter 04 covers the hash map answer to repeated lookups.

#### Watch Java Equality And Empty Input

Java adds two hazards. The first is equality on boxed values. For an `Integer[]`, the operator `==` compares object references, so two equal values can compare as different. Use `equals` for boxed values. For `int[]`, `==` compares numbers and works as expected.

The second hazard is the empty array. The loop body never runs, so the method falls through to the sentinel, which is the correct answer for a search. Reading `nums[0]` before the loop would throw an exception instead. A scan that starts from the data, such as a maximum, needs a different rule, which the next lesson covers.

<!-- stage: exercises -->
### Exercises

#### [Build] First Match (Author exercise)
<!-- id: ar-first-match -->

**Prerequisites.** Reading an array by index and writing a `for` loop.

**Problem.** Given an integer array `nums` and an integer `target`, return the smallest index `i` such that `nums[i]` equals `target`. If no such index exists, return -1.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `0 <= nums.length <= 10^5` and any `int` values.
- **`target`** is any `int` value.
- **Return value** is an `int`, and -1 means that `target` does not occur.
- **Mutation** is not allowed, so `nums` keeps its order and contents.

**Example 1.** Input `nums = [6, 2, 8, 2]`, `target = 2`, output 1.

**Example 2.** Input `nums = []`, `target = 3`, output -1, because no position exists to examine.

**Hint.** What does reaching the end of the loop prove about every position? Which line may return before the end?

**Changed decision.** Baseline case: the first match ends the scan, and the end of the loop is the only way to answer absent.

#### [Vary] Last Match (Author exercise)
<!-- id: ar-last-match -->

**Prerequisites.** The first-match exercise above.

**Problem.** Given an integer array `nums` and an integer `target`, return the largest index `i` such that `nums[i]` equals `target`. If no such index exists, return -1.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `0 <= nums.length <= 10^5` and any `int` values.
- **`target`** is any `int` value.
- **Return value** is an `int`, and -1 means that `target` does not occur.
- **Mutation** is not allowed.

**Example 1.** Input `nums = [5, 1, 5, 5, 2]`, `target = 5`, output 3.

**Example 2.** Input `nums = [4]`, `target = 9`, output -1.

**Hint.** After a match at index 1, can you already tell whether index 3 also matches? What must the variable `found` do on each match?

**Changed decision.** A match no longer permits leaving the loop, so the method keeps the latest match and returns after the full scan.

#### [Boundary] Target Absent (Author exercise)
<!-- id: ar-target-absent -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums` and an integer `target`, return the first index of `target` in `nums`, or -1 when `target` does not occur. The array may contain -1 as a value, and `target` may equal -1. A returned -1 must still mean absent, and a returned index must still be a real position.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `0 <= nums.length <= 10^5`, and values can be negative.
- **`target`** is any `int`, including -1.
- **Order** is arbitrary, and the array is not sorted.
- **Return value** is an `int` that is -1 or a valid index.

**Example 1.** Input `nums = [3, 2, 2, 3]`, `target = 5`, output -1.

**Example 2.** Input `nums = [4, -1, 9]`, `target = -1`, output 1, because the value -1 sits at index 1 and the sentinel appears only when the loop ends.

**Hint.** The loop returns an index, never a value. Why can the returned index 1 not be confused with the sentinel?

**Changed decision.** The scan must finish before it may answer absent, and the sentinel must never come from the array contents.

#### [Recognize] Build Array from Permutation (LeetCode 1920)
<!-- id: ar-build-permutation -->

**Prerequisites.** The three exercises above.

**Problem.** A permutation of length `n` contains each integer from 0 to `n - 1` exactly once. Given a permutation `nums`, return a new array `ans` of length `n` where `ans[i] = nums[nums[i]]` for every index `i`.

**Constraints.** The limits are:
- **`nums`** is an `int[]` that is a permutation, with `1 <= nums.length <= 1000`.
- **Indexes** stay valid, because every value lies in 0 to `n - 1`.
- **Mutation** is not allowed, and the method returns a new array.

**Example 1.** Input `nums = [3, 0, 2, 1]`, output `[1, 3, 2, 0]`.

**Example 2.** Input `nums = [1, 2, 0]`, output `[2, 0, 1]`.

**Hint.** Does any position need a search? What would happen to later reads if you wrote into `nums` while looping?

**Changed decision.** The contract gives every index, so each answer is a direct read and no search happens at all.
