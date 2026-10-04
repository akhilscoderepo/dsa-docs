<!-- lesson-kind: standard -->
<!-- lesson-id: in-place-sign-marking -->
## In-Place Sign Marking

<!-- stage: context -->
### Finding Which Numbers Never Arrived

A monitoring service expects `n` heartbeat messages, numbered from 1 to `n`. A batch arrives as an `int[]` of length `n`, and each element is a message number in that range. Some numbers appear twice, so other numbers must be missing. The operator wants the list of numbers that never arrived. The service runs with a tight memory limit and cannot copy the batch or allocate a table of `n` flags.

The earlier lesson on cyclic placement moves every value to its home cell and then reads the gaps. This question asks for less. It needs only to know whether each number appeared, and it does not need every number to end in a particular cell. Each cell of the input array holds a positive number, and a positive number has an unused property that can carry one yes-or-no answer. This lesson shows how to store that answer inside the input array.

<!-- stage: naive -->
### Recording Arrivals In A Flag Table

The direct method allocates a `boolean` array of size `n + 1`. It sets `arrived[v] = true` for each element `v`, then collects every number from 1 to `n` whose flag is still `false`.

```java
static java.util.List<Integer> missingByFlags(int[] nums) {
    int n = nums.length;
    boolean[] arrived = new boolean[n + 1];
    for (int v : nums) arrived[v] = true;
    java.util.List<Integer> missing = new java.util.ArrayList<>();
    for (int v = 1; v <= n; v++) {
        if (!arrived[v]) missing.add(v);
    }
    return missing;
}
```

This method is correct whenever every element lies in 1 to `n`. It reads the batch once and the table once, so the time is O(n). The table holds `n + 1` booleans, so the extra space is O(n), excluding the result list. That table is the cost that the service cannot pay.

<!-- stage: bottleneck -->
### Paying For A Table Of Flags

```predict
Every element of `nums` is a positive integer from 1 to n. Which part of a cell can hold a yes-or-no answer without destroying the number stored there?

The sign. Flipping a positive number to negative keeps its magnitude, so the program can still read the original number with `Math.abs`, and the sign carries one bit.
```

The flag table stores `n` bits, and the input array already has `n` cells. Each cell stores a number whose magnitude is at most `n`, and that range leaves the sign bit unused, because every number starts positive. The table therefore duplicates storage that the input already contains, and it is the source of the O(n) extra space.

Reusing the sign needs one precaution. A cell that has been flagged now holds a negative number, so reading it as an index would fail. The program must read the magnitude, and it must do that at every read, not only on the first one. The next stage states exactly how the flag and the magnitude work together.

<!-- stage: insight -->
### Flipping The Sign To Record An Arrival

#### Map Each Value To One Cell

Each value `v` from 1 to `n` owns one cell, the index `v - 1`. When the scan reads a value `v`, it makes the number in cell `v - 1` negative. That negative number is a **sign mark**, and it means that the value `v` has been seen. A cell that stays positive after the scan means that its value never appeared. The mark changes only the sign, so the magnitude of every cell still names its original number.

#### Read Every Cell By Its Magnitude

The scan visits cells in order, and an earlier step may already have marked the cell it reads. The value at index `i` is therefore `Math.abs(nums[i])`, the **absolute value**, because a marked cell holds `-v` while its meaning is still `v`. Using the raw negative number as an index would point before the array. The rule is to take the absolute value before every use of a cell as a value, and to negate a target cell only when it is still positive. Negating an already negative cell would erase the mark.

<!-- names: sign mark, absolute value, second visit -->

#### Detect A Value Reaching A Marked Cell

When the target cell is already negative, the value has reached a cell that an earlier occurrence marked. This event is a **second visit**, and it proves that the value occurs at least twice. The same flip therefore answers two questions in one pass. A positive target means the value is new, and a negative target means the value is a duplicate. After the pass, the indices that remain positive name the missing values.

<!-- stage: variables -->
### Meaning Of The Value And The Slot

Each step of the scan uses three quantities, and each has one meaning.

- **`value`** is `Math.abs(nums[i])`, the original number at index `i` even when that cell is marked.
- **`slot`** is `value - 1`, the cell that records whether `value` has been seen.
- **`nums[slot]`** is positive when `value` is new and negative when `value` was seen before.

The negative sign is the only state that the scan adds to the array. The magnitude never changes, so the program can recover the original batch at the end by taking absolute values. If the problem forbids a changed input, the program restores every cell with that one rule.

<!-- stage: trace -->
### Tracing Missing And Duplicate Scans

Each trace below prints the whole array after every step, so the sign changes stay visible. The first trace reads `[2, 4, 2, 6, 1, 1]`, where the numbers are expected from 1 to 6. The leading 2 flips the entry at index 1 from 4 to -4. Index 1 then yields -4, so the scan converts it to the magnitude 4 and flips index 3. The 2 at index 2 meets an entry that is already negative, which proves that 2 appeared earlier. Index 3 holds -6, so the scan works with 6 and flips index 5. The 1 at index 4 flips index 0. Index 5 now holds -1, since the 6 flipped it, so the scan works with 1 and sees that index 0 is negative already. Indices 2 and 4 never turned negative. Therefore 3 and 5 are the numbers that never arrived.

```trace
{"cells":[2,4,2,6,1,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":2,"slot":1,"array":"2,-4,2,6,1,1"},"note":"Value 2 marks cell 1, which turns negative."},{"at":{"i":1},"vars":{"value":4,"slot":3,"array":"2,-4,2,-6,1,1"},"note":"Value 4 marks cell 3, which turns negative."},{"at":{"i":2},"vars":{"value":2,"slot":1,"array":"2,-4,2,-6,1,1"},"note":"Cell 1 is already negative, so 2 has a second visit."},{"at":{"i":3},"vars":{"value":6,"slot":5,"array":"2,-4,2,-6,1,-1"},"note":"Value 6 marks cell 5, which turns negative."},{"at":{"i":4},"vars":{"value":1,"slot":0,"array":"-2,-4,2,-6,1,-1"},"note":"Value 1 marks cell 0, which turns negative."},{"at":{"i":5},"vars":{"value":1,"slot":0,"array":"-2,-4,2,-6,1,-1"},"note":"Cell 0 is already negative, so 1 has a second visit."},{"at":{"i":6},"vars":{"array":"-2,-4,2,-6,1,-1"},"note":"Cells 2 and 4 are still positive, so 3 and 5 never appeared."}]}
```

The second trace reads `[5, 3, 5, 1, 3]` and looks for repeated numbers. The 5 flips index 4, and the 3 flips index 2. At index 2 the stored entry is -5, because the 3 changed it, so the scan recovers 5 and sees that index 4 is negative. That is a second visit, so 5 goes into the result. The 1 flips index 0. At index 4 the stored entry is -3, because the first 5 changed it, so the scan recovers 3 and sees that index 2 is negative, and 3 joins the result. The hardest step is that last one. The report is right only because the program applies the absolute value before using the entry as a number, and never indexes with -3.

```trace
{"cells":[5,3,5,1,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":5,"slot":4,"array":"5,3,5,1,-3"},"note":"Value 5 marks cell 4, which turns negative."},{"at":{"i":1},"vars":{"value":3,"slot":2,"array":"5,3,-5,1,-3"},"note":"Value 3 marks cell 2, which turns negative."},{"at":{"i":2},"vars":{"value":5,"slot":4,"array":"5,3,-5,1,-3"},"note":"Cell 4 is already negative, so 5 has a second visit. Report 5."},{"at":{"i":3},"vars":{"value":1,"slot":0,"array":"-5,3,-5,1,-3"},"note":"Value 1 marks cell 0, which turns negative."},{"at":{"i":4},"vars":{"value":3,"slot":2,"array":"-5,3,-5,1,-3"},"note":"Cell 2 is already negative, so 3 has a second visit. Report 3."},{"at":{"i":5},"vars":{"array":"-5,3,-5,1,-3"},"note":"The scan ends with the repeated values 5 and 3 reported."}]}
```

Compare this run with the flag table from the naive stage. That table would reserve six booleans for the first input, whereas the marking pass reserves nothing beyond a few integer variables, yet both reach identical answers. Every step touches a single entry in constant time, so the full scan costs time proportional to the array length. A final sweep that replaces each entry by its absolute value would restore the original batch whenever the caller requires it.

<!-- stage: code -->
### Write The Marking Pass

```java
static java.util.List<Integer> missingNumbers(int[] nums) {
    for (int i = 0; i < nums.length; i++) {
        int slot = Math.abs(nums[i]) - 1;     // magnitude is the original number
        if (nums[slot] > 0) nums[slot] = -nums[slot];   // mark once, never unmark
    }
    java.util.List<Integer> missing = new java.util.ArrayList<>();
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] > 0) missing.add(i + 1);  // never marked, so i + 1 never appeared
    }
    return missing;
}
```

The first loop marks one cell for each element and reads every element through `Math.abs`. The test `nums[slot] > 0` prevents a second negation from removing a mark. The second loop collects the cells that stayed positive. The time is O(n), and the extra space is O(1) apart from the result list. The method changes the signs in `nums`, so it fits only when the contract allows mutation or when a final pass restores the signs.

<!-- stage: applicability -->
### Check The Range And Mutation Contract

#### Conditions That Allow Sign Marking

Use sign marking when the question asks which values appeared and the data fits the index range.

- **Invariant** is that cell `v - 1` is negative exactly when the value `v` has been read, and no step changes a magnitude.
- **Range** is 1 to `n`, so every value maps to a valid cell and every number starts positive.
- **Mutation** of the input is allowed, or a final pass restores the signs.
- **Question** concerns membership, such as missing, repeated or present values.

#### False Friends And No-Go Cases

Cyclic placement is a false friend for this question, because it also reuses the input array but moves values with swaps to restore locations. It is the right tool when the answer depends on where a value ends up. Sign marking only records membership and cannot answer a question about final locations. A frequency array also looks similar, but it needs its own memory, so it is not constant space.

Do not use sign marking when values can be zero or negative, because the sign already carries meaning. Do not use it when values can exceed `n`, because the target index would fall outside the array. Do not use it when the input must stay unchanged and cannot be restored.

<!-- stage: exercises -->
### Exercises

#### [Build] Find Disappeared Numbers (LeetCode 448)
<!-- id: ar-disappeared-numbers -->

**Prerequisites.** The marking pass with `value` and `slot` from this lesson.

**Problem.** Given an integer array `nums` of length `n` whose elements lie in the range `1` to `n`, return the list of integers in that range that do not appear in `nums`, in ascending order.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 10^5`.
- **Values** are integers in the range `1` to `n`, and repeats are allowed.
- **Mutation** of `nums` is allowed.
- **Extra space** is O(1) apart from the result list.

**Example 1.** Input `[5, 1, 5, 2, 2]`, output `[3, 4]`.

**Example 2.** Input `[1]`, output `[]`, because the only number in the range 1 to 1 appears.

**Hint.** Which cells stay positive after the pass, and what does the index of such a cell tell you?

**Changed decision.** Baseline case: the input array replaces the flag table, and the sign carries one bit per cell.

#### [Vary] Find All Duplicates (LeetCode 442)
<!-- id: ar-find-duplicates -->

**Prerequisites.** The Find Disappeared Numbers exercise above.

**Problem.** Given an integer array `nums` of length `n` whose elements lie in the range `1` to `n`, where each value appears once or twice, return every value that appears twice. List the values in the order of their second occurrences.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 10^5`.
- **Values** are integers in the range `1` to `n`, and each appears at most twice.
- **Mutation** of `nums` is allowed.
- **Extra space** is O(1) apart from the result list.

**Example 1.** Input `[3, 1, 3, 2, 1]`, output `[3, 1]`, because the second 3 comes before the second 1.

**Example 2.** Input `[1, 2, 3]`, output `[]`, because every value appears once.

**Hint.** What does a negative target cell tell you at the moment the scan reaches it?

**Changed decision.** The output changes from cells that stay positive to the moment a value meets a cell that is already marked.

#### [Boundary] Re-read A Marked Value (Author exercise)
<!-- id: ar-reread-marked-value -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums` of length `n` whose elements lie in the range `1` to `n`, return the number of distinct values in `nums`. Use sign marking, and restore `nums` to its original contents before the method returns.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 10^5`.
- **Values** are integers in the range `1` to `n`, and repeats are allowed.
- **Mutation** is allowed during the call, but `nums` must hold its original values at return.
- **Extra space** is O(1).

**Example 1.** Input `[2, 2, 2]`, output 1, and `nums` is still `[2, 2, 2]` afterward.

**Example 2.** Input `[1, 2, 3]`, output 3, and `nums` is unchanged.

**Hint.** What happens when the program uses a value that has already been marked as an index, and how can one rule at every read prevent it?

**Changed decision.** The scan must read cells that earlier steps have marked, and it must undo every mark before it returns.

#### [Recognize] Set Mismatch (LeetCode 645)
<!-- id: ar-set-mismatch -->

**Prerequisites.** The Re-read A Marked Value exercise above.

**Problem.** An array `nums` of length `n` started as the numbers `1` to `n`. One error changed it, so one number now appears twice and one number is absent. Return an `int[]` of length two that holds the repeated number first and the absent number second.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `2 <= n <= 10^4`.
- **Values** are integers in the range `1` to `n`.
- **Error** is exactly one repeated number and one absent number.
- **Mutation** of `nums` is allowed.
- **Extra space** is O(1).

**Example 1.** Input `[2, 3, 3, 4, 5]`, output `[3, 1]`, because 3 repeats and 1 is absent.

**Example 2.** Input `[2, 2]`, output `[2, 1]`, because 2 repeats and 1 is absent.

**Hint.** Which event during the pass reveals the repeated number, and which cell stays positive afterward?

**Changed decision.** One pass must answer two questions: a marked target reveals the repeated number, and the cell that stays positive reveals the absent one.
