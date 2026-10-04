<!-- lesson-kind: standard -->
<!-- lesson-id: cyclic-placement -->
## Cyclic Placement

<!-- stage: context -->
### Finding A Gap Without Extra Memory

A collector receives `n` numbered log records and stores their sequence numbers in an `int[]` of length `n`. The records arrive out of order, and some numbers may be missing or repeated. An operator asks which sequence number is the smallest one that never arrived. The collector runs on a device with very little memory, so it cannot allocate a second array of the same size.

The array itself already has `n` cells, and each sequence number between 1 and `n` names exactly one cell, namely the cell at index `number - 1`. If the program could move every number into the cell that its value names, then the first cell holding the wrong number would reveal the gap. This lesson shows how to do that movement inside the input array. The technique is called **cyclic placement**.

<!-- stage: naive -->
### Recording Arrivals In A Second Array

The direct method keeps a `boolean` array of size `n + 2`. It marks `seen[v] = true` for each value `v` from 1 to `n`, then scans `seen` from index 1 and returns the first index that is still `false`.

```java
static int firstMissingBySeen(int[] nums) {
    int n = nums.length;
    boolean[] seen = new boolean[n + 2];
    for (int v : nums) {
        if (v >= 1 && v <= n) seen[v] = true;
    }
    for (int v = 1; v <= n + 1; v++) {
        if (!seen[v]) return v;
    }
    return n + 1;
}
```

This method is correct for every input. It runs two loops of at most `n + 1` steps, so the time is O(n). The `seen` array holds `n + 2` booleans, so the extra space is O(n). The collector cannot afford that array, and sorting a copy needs the same amount of memory.

<!-- stage: bottleneck -->
### Paying For Memory The Input Already Has

```predict
An array holds a permutation of 1 to n, such as `[3, 1, 2]`. What is the largest number of swaps that can put every value at index `value - 1`?

At most `n - 1` swaps. Each swap sends at least one value to the index its number names, and that value never moves again, so the last swap places two values at once.
```

The `seen` array repeats information that the input array already contains. The value `v` in `nums[i]` tells the program directly where `v` belongs, because the home of `v` is index `v - 1`. No search is needed, and no table is needed to remember arrivals. If the program moves each value to its home, the input array itself becomes the table, and the extra space falls from O(n) to O(1).

The remaining question is the cost of the moving. A loop that swaps inside another loop looks quadratic at first sight. The question is whether the total number of swaps stays near `n`. The next stage shows that it does, and it also shows the one input shape that can make the loop run forever.

<!-- stage: insight -->
### Moving Each Value To Its Cell

#### Send A Value To Its Home Cell

For a value `v` between 1 and `n`, the **target slot** is the index `v - 1`. At index `i`, the loop reads `v = nums[i]` and swaps `nums[i]` with `nums[v - 1]`. After the swap, the value `v` sits at its target slot, and the value that came from there now sits at index `i`. The loop does not advance. It reads the new value at `i` and repeats until the value at `i` is already home or has no home.

#### Settled Values Never Move Again

A value that sits at its target slot is **settled**. A swap always produces one more settled value, because it puts `v` into its target slot, and that cell held a value that was not `v`. Nothing in the loop moves a settled value, because the loop only swaps a value out of an index that is not its target slot. The array has `n` cells, so at most `n` swaps happen, and the pointer `i` advances at most `n` times. The two counts add up, so the whole loop is O(n) even though it has a loop inside a loop.

<!-- names: target slot, settled, duplicate guard -->

#### Stop When The Swap Cannot Help

Two cases have no useful swap. A value outside the range 1 to `n` has no target slot, so the loop leaves it where it is and advances. A value whose target slot already holds the same value, which means a copy of it is settled there, is a duplicate. Swapping two equal values changes nothing, and the loop would repeat the same swap forever. The **duplicate guard** is the test `nums[target] != nums[i]` before every swap. When the guard fails, the loop advances. After the loop ends, every index holds either its own number or a value that could not settle, and the first index with the wrong number marks the first missing value.

<!-- stage: variables -->
### Meaning Of The Index And The Target

Three quantities control the loop, and each has one meaning at every step.

- **`i`** is the index under examination, and every index before `i` holds a settled value or a value that cannot settle.
- **`target`** is `nums[i] - 1`, the target slot of the value at `i`, and it is valid only from 0 to `n - 1`.
- **`nums`** is the array that doubles as the record of arrivals, so a swap is the only change to it.

The index `i` advances only when the value at `i` is settled, out of range or a duplicate. After a swap, `i` stays put, because the new value at `i` has not been examined yet. A mistake that moves `i` after every swap skips values and leaves some of them unplaced.

<!-- stage: trace -->
### Tracing A Permutation And A Messy Array

The first trace reads the permutation `[3, 1, 4, 2]`. The first cell holds 3, whose home is the third cell, currently occupied by 4. The swap yields `[4, 1, 3, 2]` and leaves 3 in place for good. Cell 0 now holds 4, whose home is the last cell, so a second swap yields `[2, 1, 3, 4]`. Next, 2 belongs in cell 1, where 1 waits, and the third swap yields `[1, 2, 3, 4]`. Now cell 0 holds 1, which is home, so the loop moves right through three cells that are already correct. Three swaps handled four values. That stays under the `n - 1` bound from the earlier prediction, because the final swap fixed two values together.

```trace
{"cells":[3,1,4,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"target":2,"array":"4,1,3,2"},"note":"Swap: 3 goes to index 2 and 4 comes back to index 0. The new value at 0 is unexamined, so i stays."},{"at":{"i":0},"vars":{"target":3,"array":"2,1,3,4"},"note":"Swap: 4 goes to index 3 and 2 comes back to index 0. The new value at 0 is unexamined, so i stays."},{"at":{"i":0},"vars":{"target":1,"array":"1,2,3,4"},"note":"Swap: 2 goes to index 1 and 1 comes back to index 0. The new value at 0 is unexamined, so i stays."},{"at":{"i":0},"vars":{"target":0,"array":"1,2,3,4"},"note":"1 sits at its own target slot, index 0, so it is settled."},{"at":{"i":1},"vars":{"target":1,"array":"1,2,3,4"},"note":"2 sits at its own target slot, index 1, so it is settled."},{"at":{"i":2},"vars":{"target":2,"array":"1,2,3,4"},"note":"3 sits at its own target slot, index 2, so it is settled."},{"at":{"i":3},"vars":{"target":3,"array":"1,2,3,4"},"note":"4 sits at its own target slot, index 3, so it is settled."},{"at":{"i":4},"vars":{"array":"1,2,3,4"},"note":"Done: i has passed the end and the array reads [1,2,3,4]."}]}
```

The second trace reads `[2, 2, 7, 1]`, an array with a repeated number and an oversized number. Cell 0 holds 2, whose home is cell 1, but cell 1 also holds 2. Swapping equal numbers achieves nothing, so the duplicate guard rejects it and the loop moves on. Cell 1 then holds a 2 that is already home. The 7 cannot fit in four cells, so the loop ignores it. Cell 3 holds 1, whose home is cell 0, where a 2 sits, so a real swap happens and the array becomes `[1, 2, 7, 2]`. The 2 that arrives in cell 3 meets the same guard as before. Scanning for the first wrong cell finds cell 2, so the smallest missing positive is 3. The hardest step is the guard in cell 3, because without it that step would exchange two equal numbers forever.

```trace
{"cells":[2,2,7,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"target":1,"array":"2,2,7,1"},"note":"2 would go to index 1, yet that cell holds 2 already. The duplicate guard refuses the swap."},{"at":{"i":1},"vars":{"target":1,"array":"2,2,7,1"},"note":"2 sits at its own target slot, index 1, so it is settled."},{"at":{"i":2},"vars":{"target":6,"array":"2,2,7,1"},"note":"7 lies outside 1..4, so it has no target slot and the loop passes it."},{"at":{"i":3},"vars":{"target":0,"array":"1,2,7,2"},"note":"Swap: 1 goes to index 0 and 2 comes back to index 3. The new value at 3 is unexamined, so i stays."},{"at":{"i":3},"vars":{"target":1,"array":"1,2,7,2"},"note":"2 would go to index 1, yet that cell holds 2 already. The duplicate guard refuses the swap."},{"at":{"i":4},"vars":{"array":"1,2,7,2"},"note":"Done: i has passed the end and the array reads [1,2,7,2]."}]}
```

<!-- stage: code -->
### Write The Placement Loop

```java
static void placeValues(int[] nums) {
    int i = 0;
    while (i < nums.length) {
        int target = nums[i] - 1;
        boolean hasTarget = target >= 0 && target < nums.length;
        if (hasTarget && nums[target] != nums[i]) {
            int tmp = nums[i];          // swap puts nums[i] into its target slot
            nums[i] = nums[target];
            nums[target] = tmp;
        } else {
            i++;                        // settled, out of range or duplicate
        }
    }
}
```

The loop uses `while` instead of `for`, because `i` stays after a swap. The range test comes first in the condition, so `nums[target]` is read only for a valid index. Each swap settles one value, so the loop performs at most `n` swaps and `n` advances. The time is O(n) and the extra space is O(1). The method changes the order of `nums`, so use it only when the contract allows mutation.

<!-- stage: applicability -->
### Check The Slot Contract Before Moving Values

#### Conditions That Allow Placement

Use placement when each value has one intended index and the input may be reordered.

- **Invariant** is that every swap puts one value in its target slot, and no loop step moves a settled value.
- **Mapping** from value to index is a fixed formula such as `v - 1`, or `v` when the range starts at 0.
- **Mutation** of the input is allowed, and the original order is not needed afterward.
- **Duplicates** are allowed only with the duplicate guard in place.

#### False Friends And No-Go Cases

Sign marking looks like a close relative, because it also uses the input array as the record. It is a false friend for this task, because it only records which values were seen and does not move any value to a final location. It cannot answer a question about where a value ends up. Sorting looks like another route to the same result, but it costs O(n log n) time and does not exploit a known mapping.

Do not use placement when the input must stay unchanged, because the loop destroys the original order. Do not use it when values have no fixed target index, such as arbitrary large integers or strings, because there is no cell for them to settle in.

<!-- stage: exercises -->
### Exercises

#### [Build] Place 1..n (Author exercise)
<!-- id: ar-place-one-to-n -->

**Prerequisites.** The placement loop with `i` and `target` from this lesson.

**Problem.** Given an integer array `nums` that is a permutation of the values `1` to `n`, where `n = nums.length`, reorder `nums` in place so that `nums[i] == i + 1` for every index `i`. Return nothing.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 10^5`.
- **Values** are distinct and cover `1` to `n` exactly once.
- **Mutation** of `nums` is required, and no second array of size `n` is allowed.
- **Extra space** is O(1).

**Example 1.** Input `[3, 1, 4, 2]`, output: nothing is returned, and `nums` becomes `[1, 2, 3, 4]`.

**Example 2.** Input `[2, 1]`, output: nothing is returned, and `nums` becomes `[1, 2]` after one swap.

**Hint.** After a swap at index `i`, which value sits at `i`, and has it been examined yet?

**Changed decision.** Baseline case: the loop keeps `i` still after a swap and advances only when the value at `i` is settled.

#### [Vary] Missing Number (LeetCode 268)
<!-- id: ar-missing-number -->

**Prerequisites.** The Place 1..n exercise above.

**Problem.** Given an integer array `nums` of length `n` that holds distinct values from the range `0` to `n`, return the one value in that range that is absent. The array may be reordered during the call.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 10^4`.
- **Values** are distinct integers in the range `0` to `n`.
- **Mutation** of `nums` is allowed.
- **Extra space** is O(1).

**Example 1.** Input `[1, 4, 0, 2]`, output 3, because the range is 0 to 4 and 3 is absent.

**Example 2.** Input `[0, 1, 2]`, output 3, because every index holds its own number and the absent value is `n`.

**Hint.** The value `n` has no cell at index `n`. What should the loop do with it, and what does the first index holding the wrong number tell you?

**Changed decision.** The range now starts at 0, so the target slot of `v` is `v` itself, and the value `n` has no target slot.

#### [Boundary] Duplicate Slot (Author exercise)
<!-- id: ar-duplicate-slot -->

**Prerequisites.** The Missing Number exercise above.

**Problem.** Given an integer array `nums` of length `n` whose values lie in the range `1` to `n` and may repeat, run the placement loop with the duplicate guard. Then return the number of indices `i` where `nums[i] != i + 1`.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 10^4`.
- **Values** are integers in the range `1` to `n`, and repeats are allowed.
- **Mutation** of `nums` is allowed, and the loop must stop on every input.
- **Return value** is an `int` from `0` to `n - 1`.

**Example 1.** Input `[3, 1, 3, 4, 2]`, output 1, because the array ends as `[1, 2, 3, 4, 3]` and only index 4 holds the wrong number.

**Example 2.** Input `[2, 2, 2]`, output 2, because the value 2 settles at index 1 and indices 0 and 2 stay wrong.

**Hint.** When the target slot already holds the same value as index `i`, what does another swap change?

**Changed decision.** The input is no longer a permutation, so the loop needs the duplicate guard to avoid repeating the same swap forever.

#### [Recognize] First Missing Positive (LeetCode 41)
<!-- id: ar-first-missing-positive -->

**Prerequisites.** The Duplicate Slot exercise above.

**Problem.** Given an unsorted integer array `nums`, return the smallest positive integer that does not appear in it. The array may be reordered during the call.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 10^5`.
- **Values** are any `int` values, including zero, negatives, duplicates and values above `n`.
- **Mutation** of `nums` is allowed.
- **Extra space** is O(1).

**Example 1.** Input `[2, 5, -3, 1, 0]`, output 3, because 1 and 2 appear and 3 does not.

**Example 2.** Input `[6, 6, 1, 1, 1]`, output 2, because duplicates and values above `n` do not hide the gap at 2.

**Hint.** The answer lies between 1 and `n + 1`. Which values can the loop ignore, and what does the first index with the wrong number mean?

**Changed decision.** Values outside `1` to `n` and duplicates now appear together, so the loop ignores out-of-range values and the answer comes from the first index whose number is wrong.
