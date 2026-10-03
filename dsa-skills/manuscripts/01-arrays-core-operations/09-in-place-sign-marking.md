<!-- lesson-kind: standard -->
<!-- lesson-id: in-place-sign-marking -->
## In-Place Sign Marking

<!-- stage: context -->
### Checking Names Off A Printed Roll

A teacher has a printed class roll with the numbers 1 to 30 down the left side. Students line up and each one calls out a number from the roll, though some call the same number twice and some numbers are never called. She wants to know which numbers were never called, and she has no spare paper.

So she does the simplest thing with the roll in front of her. Each time a number is called, she puts a pencil tick beside that number on the roll itself. When the line is finished, every number with no tick is a number nobody called. The roll was already a table with one row per possible number, and the ticks are the record. She added no new sheet of paper.

<!-- stage: naive -->
### Search The Calls For Every Number

The direct method follows the question word for word. For each number on the roll, scan all the calls to see whether it appears.

```java
static List<Integer> disappearedBySearch(int[] calls) {
    List<Integer> missing = new ArrayList<>();
    for (int target = 1; target <= calls.length; target++) {
        boolean seen = false;
        for (int c : calls) {
            if (c == target) { seen = true; break; }
        }
        if (!seen) missing.add(target);
    }
    return missing;
}
```

For `[2, 2, 5, 5, 1]` it checks 1 and 2 and finds them, fails on 3 and 4 and reports both, then finds 5. The result is `[3, 4]`.

<!-- stage: bottleneck -->
### A Fresh Search For Each Number

Each target number triggers a scan of every call, so for `n` calls and `n` numbers the cost is O(n^2). At 100,000 calls that is up to ten billion comparisons. The extra memory is only the output list, so time is the problem. A boolean array of size `n` would fix the time at O(n), but it costs O(n) extra space, which is exactly what the teacher did not have.

The waste is that every scan rediscovers facts the previous scans already knew. The calls never change, but the method forgets what it has seen. The remedy is to record each sighting once, in a place that costs nothing, and that place can be the array itself.

<!-- stage: insight -->
### The Sign Remembers The Visit

When the values lie in `1..n`, slot `v - 1` is the natural place to record whether value `v` has been seen. The array already has `n` slots, and the numbers are the only information in them, so a second bit of information must hide inside each number. The **sign** is that spare bit. Values are positive on input, so making a slot negative cannot be confused with its original content, and its **magnitude** still tells us what number lived there.

A **sign mark** is the act of negating the slot at `v - 1` when value `v` is seen. A slot is a **marked slot** when it is negative. After the pass, the marked slots name the values that appeared, and the slots still positive name the values that never did.

<!-- names: sign mark, marked slot, magnitude -->

The invariant is that slot `v - 1` is negative exactly when value `v` has appeared among the elements read so far. There is one trap built into the technique. The cursor may land on a slot that an earlier step already marked, so the value it reads can be negative. The cursor must therefore read the magnitude, `Math.abs(nums[i])`, before using it as an index. A negative number cannot be an index at all, and a naive `nums[i] - 1` would point before the start of the array.

The same marks answer related questions. If a value arrives and its slot is already marked, that value has been seen before, so it is a duplicate. If a slot is still positive at the end, its value never arrived, so it is missing. Both facts come from the same single pass.

<!-- stage: variables -->
### The Cursor, The Magnitude And The Slot

The cursor `i` visits each position once. The magnitude `v = Math.abs(nums[i])` is the value read at that position, whatever its current sign. The slot is `v - 1`, and its sign is the record. A positive slot means unseen so far, and a negative slot means seen. The marking step must never flip a slot back to positive, so it assigns `-Math.abs(nums[slot])` instead of simply negating. A second scan over the slots reads the finished record.

<!-- stage: trace -->
### Marking And Re-Reading

First roll: `[2, 2, 5, 5, 1]`, five calls and five numbers. The first 2 marks slot 1. The second 2 finds slot 1 already marked, so the mark stays. The 5 marks slot 4, the second 5 changes nothing, and the 1 marks slot 0. Then the collecting scan reads the record: slots 0, 1 and 4 are negative, and slots 2 and 3 are positive. The numbers never called are therefore 3 and 4.

Second roll: `[3, 1, 3]`, and the interesting step is the last one. The first 3 marks slot 2, so the array is `[3, 1, -3]`. The 1 marks slot 0, giving `[-3, 1, -3]`. The cursor then reaches index 2, which holds -3, a value that was marked earlier. Reading its magnitude gives 3, and slot 2 is already negative, so 3 is a duplicate. Using -3 directly would have pointed at index -4 and failed.

```trace
{"cells":[2,2,5,5,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"array":"[2,-2,5,5,1]","slot":1},"note":"Read 2. Slot 1 was positive, so it becomes negative."},{"at":{"i":1},"vars":{"array":"[2,-2,5,5,1]","slot":1},"note":"Read 2. Slot 1 is already negative, so nothing changes."},{"at":{"i":2},"vars":{"array":"[2,-2,5,5,-1]","slot":4},"note":"Read 5. Slot 4 was positive, so it becomes negative."},{"at":{"i":3},"vars":{"array":"[2,-2,5,5,-1]","slot":4},"note":"Read 5. Slot 4 is already negative, so nothing changes."},{"at":{"i":4},"vars":{"array":"[-2,-2,5,5,-1]","slot":0},"note":"Read 1. Slot 0 was positive, so it becomes negative."},{"at":{"i":0},"vars":{"array":"[-2,-2,5,5,-1]","missing":"[]"},"note":"Slot 0 is negative, so 1 appeared."},{"at":{"i":1},"vars":{"array":"[-2,-2,5,5,-1]","missing":"[]"},"note":"Slot 1 is negative, so 2 appeared."},{"at":{"i":2},"vars":{"array":"[-2,-2,5,5,-1]","missing":"[3]"},"note":"Slot 2 is still positive, so 3 never appeared."},{"at":{"i":3},"vars":{"array":"[-2,-2,5,5,-1]","missing":"[3,4]"},"note":"Slot 3 is still positive, so 4 never appeared."},{"at":{"i":4},"vars":{"array":"[-2,-2,5,5,-1]","missing":"[3,4]"},"note":"Slot 4 is negative, so 5 appeared."}]}
```

```trace
{"cells":[3,1,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"array":"[3,1,-3]","duplicates":"[]"},"note":"Read 3. Slot 2 was positive, so it becomes negative."},{"at":{"i":1},"vars":{"array":"[-3,1,-3]","duplicates":"[]"},"note":"Read 1. Slot 0 was positive, so it becomes negative."},{"at":{"i":2},"vars":{"array":"[-3,1,-3]","duplicates":"[3]"},"note":"Read the magnitude 3 from -3. Slot 2 is already negative, so 3 is a duplicate."}]}
```

<!-- stage: code -->
### Mark, Then Collect

```java
static List<Integer> disappeared(int[] nums) {          // values in 1..n; mutates the array
    for (int i = 0; i < nums.length; i++) {
        int slot = Math.abs(nums[i]) - 1;
        if (nums[slot] > 0) nums[slot] = -nums[slot];
    }
    List<Integer> missing = new ArrayList<>();
    for (int i = 0; i < nums.length; i++) if (nums[i] > 0) missing.add(i + 1);
    return missing;
}

static List<Integer> duplicates(int[] nums) {           // values in 1..n, each at most twice
    List<Integer> dup = new ArrayList<>();
    for (int i = 0; i < nums.length; i++) {
        int slot = Math.abs(nums[i]) - 1;
        if (nums[slot] < 0) dup.add(slot + 1);
        else nums[slot] = -nums[slot];
    }
    return dup;
}
```

Both read the magnitude before indexing, and both run in linear time with constant extra space apart from the output list. The array is left with negative entries, so a caller that needs the original values must take absolute values of every slot afterwards, or work on a copy. The duplicates method relies on the promise that each value appears at most twice, because a third copy would be reported again.

<!-- stage: applicability -->
### When Slots Can Hold A Sighting

Use sign marking when the values are in `1..n` for an array of length `n`, the array may be modified, and the question asks which values were seen, repeated or missing. The invariant is that slot `v - 1` is negative exactly when `v` was seen, and every read goes through the magnitude. The result needs no extra table.

The false friend is cyclic placement from the previous lesson. Both treat the array as a table with one slot per value, but placement moves values into their final locations, while sign marking records membership only, so the array order is lost. If the answer depends on where values end up, use placement. Another false friend is data with zeros or negatives in the input, since the sign bit is then already in use, and the method silently reads wrong slots. A shift by a constant fixes small ranges, but arbitrary integers call for a set.

In Java, `Math.abs(Integer.MIN_VALUE)` is still negative, which is irrelevant inside the promised range but a reminder that the range promise is doing real work. Restore the signs before returning the array if the caller will see it again.

<!-- stage: exercises -->
### Exercises

#### [Build] Find All Numbers Disappeared in an Array (LeetCode 448)
<!-- id: ar-disappeared-numbers -->

**Prerequisites.** The home-slot idea from cyclic placement; this lesson.

**Problem.** Given an array of `n` integers, each in `1..n`, return all integers in that range that do not appear in the array. Use the array itself to record sightings.

**Constraints.** 1 <= n <= 10^5 and 1 <= nums[i] <= n. The array may be modified, and the output list does not count as extra space.

**Example 1.** Input `nums = [2, 2, 5, 5, 1]`, output `[3, 4]`.

**Example 2.** Input `nums = [1, 2, 3]`, output `[]`, since every number of the range appears.

**Hint.** Which slot corresponds to a value? Which change to that slot can be undone later and cannot be confused with the original content?

**Changed decision.** First rung: the sign of a slot stores one bit per value, so no second table is needed.

#### [Vary] Find All Duplicates in an Array (LeetCode 442)
<!-- id: ar-find-duplicates -->

**Prerequisites.** The disappeared-numbers exercise above.

**Problem.** Given an array of `n` integers in `1..n` in which each value appears once or twice, return all values that appear twice, using the array for bookkeeping.

**Constraints.** 1 <= n <= 10^5, 1 <= nums[i] <= n, and no value appears more than twice. The array may be modified.

**Example 1.** Input `nums = [3, 1, 3, 2, 5, 5]`, output `[3, 5]`.

**Example 2.** Input `nums = [1, 2, 3]`, output `[]`, because every value is unique.

**Hint.** When a value arrives and its slot is already marked, what have you learned? What should you do when it is not marked?

**Changed decision.** The question moves from reading the marks at the end to testing the mark at the moment of arrival.

#### [Boundary] Re-read a Marked Value (Author exercise)
<!-- id: ar-reread-marked-value -->

**Prerequisites.** The two exercises above.

**Problem.** After some slots are marked, the cursor can land on a negative number. Show why using that value directly as an index is invalid, and show that taking its magnitude repairs the read. Mark every value of an array and then restore all original values.

**Constraints.** 1 <= n <= 10^5 and 1 <= nums[i] <= n. A marked slot must never be flipped back to positive during the pass.

**Example 1.** Input `nums = [3, 1, 3]`, output a duplicate report of 3, and the read at index 2 meets the marked value -3.

**Example 2.** Input `nums = [2, 1]`, output the array `[-2, -1]` after marking and `[2, 1]` after restoring.

**Hint.** What index would -3 minus one point at? How does taking the magnitude recover the original value, and what must the marking step assign so a second visit does not undo the first?

**Changed decision.** The tests target the reading step and show why every read must pass through the magnitude.

#### [Recognize] Set Mismatch (LeetCode 645)
<!-- id: ar-set-mismatch -->

**Prerequisites.** All three exercises above.

**Problem.** An array should contain each of `1..n` once, but one value was copied over another, so one value appears twice and one value is missing. Return the repeated value and the missing value in that order.

**Constraints.** 2 <= n <= 10^4 and 1 <= nums[i] <= n, with exactly one repeated and one missing value. The array may be modified.

**Example 1.** Input `nums = [3, 1, 3, 4]`, output `[3, 2]`.

**Example 2.** Input `nums = [2, 2]`, output `[2, 1]`.

**Hint.** Which of the two answers appears at the moment a slot is found already marked? Which appears only after the pass, as a slot still positive?

**Changed decision.** One pass produces both answers, one from the arrival test and one from the final scan.
