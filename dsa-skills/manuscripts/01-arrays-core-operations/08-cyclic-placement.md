<!-- lesson-kind: standard -->
<!-- lesson-id: cyclic-placement -->
## Cyclic Placement

<!-- stage: context -->
### Coats With Numbered Tags

A theatre coat check has a rail of numbered hooks, and every coat arrives with a paper tag. Tag 1 belongs on hook 1, tag 2 on hook 2, and so on. During the interval the coats are piled onto the rail in whatever order the guests handed them in, and the attendant has ten minutes to restore order before the doors open.

She does not take every coat down and sort the pile on a table. She looks at the coat on hook one, reads its tag, and swaps it with whatever hangs on the hook named by that tag. She keeps doing that until the coat in her hands belongs where she stands, and then she moves to the next hook. Nothing is carried away from the rail, and no second rail is needed.

<!-- stage: naive -->
### Look For Each Number By Scanning

Suppose the question is the first positive number missing from an array. The direct method tries 1, then 2, then 3, and searches the whole array for each candidate.

```java
static int firstMissingByScanning(int[] nums) {
    for (int candidate = 1; candidate <= nums.length + 1; candidate++) {
        boolean found = false;
        for (int v : nums) {
            if (v == candidate) { found = true; break; }
        }
        if (!found) return candidate;
    }
    return nums.length + 1;
}
```

It is short and obviously right, because it asks the question in the same words as the problem. For `[7, 5, 1, 2, -4]` it checks 1 and 2, fails to find 3, and returns it.

<!-- stage: bottleneck -->
### One Full Search For Every Candidate

Each candidate triggers a scan of the whole array, and there can be about `n` candidates, so the cost is O(n^2). With 100,000 values that is up to ten billion comparisons. The extra space is O(1), so memory is fine, and the repeated searching is the waste. Every scan answers a membership question about one number, and the array never gets any easier to search.

A hash set from a later chapter turns each membership check into a lookup, and a sort puts neighbors together, but each costs either O(n) memory or O(n log n) time. There is a cheaper route when the values are close to the indices. A number between 1 and `n` already has an obvious address in an array of length `n`, which means the array itself can serve as the table.

<!-- stage: insight -->
### Every Value Has A Home Slot

Within an array of length `n`, a value `v` between 1 and `n` has a **home slot**: index `v - 1`. If every value sat in its home slot, the array would read `1, 2, 3, ...`, and the first position holding the wrong number would immediately name the first missing value. The work is to move values into their home slots using nothing but swaps inside the array.

Standing at index `i`, read `v = nums[i]`. If `v` is outside `1..n`, it has no home in this array and is left alone. If the home slot `v - 1` already holds `v`, the value is settled, and a second copy has nowhere to go. Otherwise swap `nums[i]` with `nums[v - 1]`, which puts `v` in its home slot for good, and then look again at the value that arrived at index `i`. This repeated swapping is **cyclic placement**, and the sequence of swaps from one starting index is a **swap chain**. The chain ends when the arriving value is out of range or already settled.

<!-- names: home slot, cyclic placement, swap chain -->

The invariant is that every swap permanently settles one value, so a slot that holds its own value is never disturbed again. Each swap settles one value, and at most `n` values can be settled, so the total number of swaps is at most `n`. The nested loop looks quadratic, but the swaps are paid for once each, and the total work is O(n). The stopping test on the home slot also protects against duplicates. If two copies of `3` exist, swapping them with each other would never change anything, so the test compares the two values and not just the index.

<!-- stage: variables -->
### The Cursor And The Arriving Value

The cursor `i` moves forward over the array exactly once. At each position the value `v = nums[i]` is the current coat in hand. The home slot is `v - 1`, and the test that decides whether to swap compares `nums[v - 1]` with `v`. The array holds the evidence of progress, since a slot holding `index + 1` is settled. After the pass, one more scan looks for the first slot that does not hold its own number, and that scan is the answer.

<!-- stage: trace -->
### Two Rails, Two Kinds Of Chain

First rail: `[3, 1, 2]`. At index 0 the value 3 belongs on slot 2, so swap, which brings 2 to index 0. The 2 belongs on slot 1, so swap again, which brings 1 to index 0. The 1 belongs on slot 0 and is settled, so the chain ends. Indices 1 and 2 were settled by that one chain, so the rest of the pass finds nothing to do.

Second rail: `[7, 5, 1, 2, -4]`, where some values do not belong. The 7 is larger than the array length, so it is skipped. The 5 swaps with the last slot, and the -4 that arrives is out of range and stops the chain. The 1 swaps to slot 0 and drops the 7 onto index 2, where it is skipped again. The 2 swaps to slot 1. The final scan finds the first slot that does not hold its own number, and index 2 holds 7, so the answer is 3.

```trace
{"cells":[3,1,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"array":"[2,1,3]","settled":1},"note":"Swap 3 into slot 2; index 0 now holds 2."},{"at":{"i":0},"vars":{"array":"[1,2,3]","settled":3},"note":"Swap 2 into slot 1; index 0 now holds 1."},{"at":{"i":0},"vars":{"array":"[1,2,3]","settled":3},"note":"Index 0 holds 1 and slot 0 already holds 1, so the chain stops."},{"at":{"i":1},"vars":{"array":"[1,2,3]","settled":3},"note":"Index 1 holds 2 and slot 1 already holds 2, so the chain stops."},{"at":{"i":2},"vars":{"array":"[1,2,3]","settled":3},"note":"Index 2 holds 3 and slot 2 already holds 3, so the chain stops."}]}
```

```trace
{"cells":[7,5,1,2,-4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"array":"[7,5,1,2,-4]","settled":0},"note":"Index 0 holds 7, which has no home slot here, so the chain stops."},{"at":{"i":1},"vars":{"array":"[7,-4,1,2,5]","settled":1},"note":"Swap 5 into slot 4; index 1 now holds -4."},{"at":{"i":1},"vars":{"array":"[7,-4,1,2,5]","settled":1},"note":"Index 1 holds -4, which has no home slot here, so the chain stops."},{"at":{"i":2},"vars":{"array":"[1,-4,7,2,5]","settled":2},"note":"Swap 1 into slot 0; index 2 now holds 7."},{"at":{"i":2},"vars":{"array":"[1,-4,7,2,5]","settled":2},"note":"Index 2 holds 7, which has no home slot here, so the chain stops."},{"at":{"i":3},"vars":{"array":"[1,2,7,-4,5]","settled":3},"note":"Swap 2 into slot 1; index 3 now holds -4."},{"at":{"i":3},"vars":{"array":"[1,2,7,-4,5]","settled":3},"note":"Index 3 holds -4, which has no home slot here, so the chain stops."},{"at":{"i":4},"vars":{"array":"[1,2,7,-4,5]","settled":3},"note":"Index 4 holds 5 and slot 4 already holds 5, so the chain stops."}]}
```

<!-- stage: code -->
### Swap Until The Slot Is Settled

```java
static void placeAll(int[] nums) {                    // contract: a permutation of 1..n
    for (int i = 0; i < nums.length; i++) {
        while (nums[i] != i + 1) {
            int home = nums[i] - 1;
            int tmp = nums[home]; nums[home] = nums[i]; nums[i] = tmp;
        }
    }
}

static int firstMissingPositive(int[] nums) {         // any ints; mutates the array
    int n = nums.length;
    for (int i = 0; i < n; i++) {
        while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
            int home = nums[i] - 1;
            int tmp = nums[home]; nums[home] = nums[i]; nums[i] = tmp;
        }
    }
    for (int i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;
    return n + 1;
}
```

The first method relies on its contract and needs no range test. The second guards against out-of-range values and duplicates before every swap, then scans for the first unsettled slot. Both run in linear time because each swap settles one value, and both use constant extra space, but both rewrite the input array. Copy it first if the caller still needs the original order.

<!-- stage: applicability -->
### When Values Name Their Own Index

Use cyclic placement when the values are, or can be filtered to, integers in a range the size of the array, and the question is about which values are missing, repeated, or misplaced. The invariant is that a settled slot holds its own number and is never touched again. Mutation of the input must be acceptable, since the array is rearranged.

The false friend is sign marking, the next lesson. Both use the array as a table of size `n`, but sign marking only records that a value was seen, while placement actually restores locations, which is needed when the answer depends on where things ended up. Another false friend is any array with values far outside `1..n`, such as ids up to a billion. Those values have no home slot, and ignoring them is only safe when the question is about the smaller range. If the input must stay unchanged, copy it first or use a different method.

In Java the swap needs a temporary variable, and the stopping test must come before the swap. Writing `nums[nums[i] - 1]` before checking the range throws an `ArrayIndexOutOfBoundsException` for a value like 0 or 9. Use `while` and not `if`, because after a swap the arriving value also needs a home.

<!-- stage: exercises -->
### Exercises

#### [Build] Place 1..n (Author exercise)
<!-- id: ar-place-one-to-n -->

**Prerequisites.** Swap on arrays from Chapter 00; the home slot idea in this lesson.

**Problem.** Given an array that is a permutation of `1..n`, rearrange it in place so that value `v` sits at index `v - 1`. Use only swaps within the array.

**Constraints.** 1 <= n <= 10^5, and the input contains each of `1..n` exactly once. Use no second array.

**Example 1.** Input `nums = [3, 1, 2]`, output `[1, 2, 3]`.

**Example 2.** Input `nums = [4, 3, 2, 1]`, output `[1, 2, 3, 4]`.

**Hint.** Where must the value at the cursor end up? What do you do with the value that the swap brings to the cursor?

**Changed decision.** First rung: the value chooses its own destination, so no searching or sorting is needed.

#### [Vary] Missing Number (LeetCode 268)
<!-- id: ar-missing-number -->

**Prerequisites.** The place-1..n exercise above.

**Problem.** An array of length `n` holds distinct numbers drawn from the range `0..n`, so exactly one number of that range is absent. Return the absent number using cyclic placement and a final scan.

**Constraints.** 1 <= n <= 10^4 and every value is distinct and within `0..n`. The array may be modified.

**Example 1.** Input `nums = [4, 0, 2, 1]`, output 3.

**Example 2.** Input `nums = [0, 1]`, output 2, because every slot is settled and the missing number is `n`.

**Hint.** The range now starts at 0, so what is the home slot of a value? Which value has no slot at all?

**Changed decision.** The home slot becomes `v` instead of `v - 1`, and the value `n` has no slot and is left alone.

#### [Boundary] Duplicate Slot (Author exercise)
<!-- id: ar-duplicate-slot -->

**Prerequisites.** The two exercises above.

**Problem.** Now an array of length `n` holds values in `1..n`, and some values repeat. Run the placement with the rule that you stop swapping when `nums[i] == nums[nums[i] - 1]`. Return the array after placement, and explain what happens without that rule on `[2, 2]`.

**Constraints.** 1 <= n <= 10^5 and 1 <= nums[i] <= n. The array may be modified.

**Example 1.** Input `nums = [3, 1, 3]`, output `[1, 3, 3]`, where index 1 is the only slot not holding its own number.

**Example 2.** Input `nums = [2, 2]`, output `[2, 2]`, where index 0 is unsettled. Without the stopping rule, swapping the two 2s would repeat forever.

**Hint.** What if the home slot already holds the same value as the cursor? Would a swap change anything at all?

**Changed decision.** The stopping test compares values and not indices, which turns a possible infinite loop into a clean stop.

#### [Recognize] First Missing Positive (LeetCode 41)
<!-- id: ar-first-missing-positive -->

**Prerequisites.** All three exercises above.

**Problem.** Given an unsorted integer array, return the smallest positive integer that does not appear. Values that are zero, negative, or larger than the array length may be present and must not break the method. Use linear time and constant extra space.

**Constraints.** 1 <= nums.length <= 10^5 and -2^31 <= nums[i] <= 2^31 - 1. The array may be modified, and no hash set is allowed.

**Example 1.** Input `nums = [7, 5, 1, 2, -4]`, output 3.

**Example 2.** Input `nums = [1, 2, 3, 4]`, output 5, because every slot is settled.

**Hint.** What is the biggest the answer can be for an array of length `n`? Which values can therefore be ignored?

**Changed decision.** The answer is at most `n + 1`, so out-of-range values are skipped and the first unsettled slot names the answer.
