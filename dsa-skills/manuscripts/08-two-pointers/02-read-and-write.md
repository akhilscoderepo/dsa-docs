<!-- lesson-kind: standard -->
<!-- lesson-id: read-and-write -->
## Read Ahead And Write Behind

<!-- stage: context -->
### Deleting Records From A Big Array

A service holds 100,000 records in an array and must drop every record that a user has deleted. The first version removes one record at a time. After each removal it moves all later records one slot to the left. When half of the records are deleted, the service spends most of its time moving records that it has already moved before.

The cleaned array has a simple shape: the kept records, in their original order, followed by unused slots. The question is how a program can build that array while it touches each record only once.

<!-- stage: naive -->
### Shifting The Tail After Every Removal

The direct method scans the array. When it finds a value equal to `val`, it copies every later value one slot to the left and shortens the logical length by one.

```java
static int removeSlow(int[] nums, int val) {
    int n = nums.length;
    int i = 0;
    while (i < n) {
        if (nums[i] == val) {
            for (int j = i + 1; j < n; j++) nums[j - 1] = nums[j];
            n--;
        } else {
            i++;
        }
    }
    return n;
}
```

For `[1, 2, 2, 3, 2, 4]` and `val = 2`, the method shifts the tail three times. It returns 3 and leaves `[1, 3, 4]` at the front. The loop does not advance `i` after a shift, because a new value has moved into slot `i`.

```predict
The array holds 100,000 copies of `val`. How many single-value copies does `removeSlow` perform?

Each removal copies all later values. The first copies 99,999 values, the next copies 99,998, and so on, which is about 5 billion copies. The total grows with the square of the length, so the method is O(n^2).
```

<!-- stage: bottleneck -->
### Each Kept Value Moves Many Times

A kept value moves left once for every removed value that sits before it. In the worst case a value that is kept moves O(n) times, and the whole method costs O(n^2). The program knows the final position of each kept value in advance, because that position equals the number of kept values before it.

The repeated work comes from fixing the array after every removal. One pass can decide for each value whether it stays and where it goes, so every kept value needs exactly one copy.

<!-- stage: insight -->
### Read Everything And Write Kept Values

#### Two Positions In One Array

Use two indexes that move in the same direction. The **read index** `read` visits each value once, from the first slot to the last. The **write index** `write` marks the next slot of the output. It never passes `read`, because the output cannot hold more values than the input has read so far.

#### The Kept Prefix

The slots from index 0 up to but not including `write` form the **kept prefix**. The kept prefix always equals the final answer for the values read so far. When `nums[read]` passes the test, the scan copies it to `nums[write]` and increases `write`. When it fails the test, the scan does nothing, and only `read` advances. The copy never overwrites an unread value, because `write <= read`.

This scan is a **compaction**, which means a pass that moves the kept values to the front and keeps their relative order. After the loop, `write` equals the number of kept values, so the answer is `write`. Each step costs O(1), the loop runs `n` times, and the method uses O(1) extra space.

<!-- names: read index, write index, kept prefix, compaction -->

#### What The Test Can Consult

The test for a value may look at the value alone, as in "not equal to `val`". It may also look at the kept prefix, as in "different from the last kept value". The pointers do not change in the second case. Only the admission rule changes.

<!-- stage: variables -->
### Three Names And Their Roles

The compaction keeps three pieces of state, and two of them change.

- **read** is the index of the next unread value, and it increases by one per iteration.
- **write** is the index of the next free output slot and the length of the kept prefix, and it never exceeds `read`.
- **nums** is the array, and slots from `write` on may hold stale values that the contract leaves unspecified.

The loop ends when `read` equals `nums.length`. Then `nums[0..write-1]` is the answer.

<!-- stage: trace -->
### Two Compactions With Different Tests

#### Removing One Value

The input is `[1, 2, 2, 3, 2, 4]` and `val` is 2. The read index visits every slot, from the first to the last. The write index advances only when the value differs from 2. The kept prefix therefore grows from empty to `[1, 3, 4]`.

```trace
{"cells":[1,2,2,3,2,4],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"value":"1","kept":"[1]"},"note":"The value 1 differs from 2, so it is copied to slot 0 and write advances."},{"at":{"read":1,"write":1},"vars":{"value":"2","kept":"[1]"},"note":"The value 2 equals 2, so only read advances."},{"at":{"read":2,"write":1},"vars":{"value":"2","kept":"[1]"},"note":"The value 2 equals 2, so only read advances."},{"at":{"read":3,"write":1},"vars":{"value":"3","kept":"[1, 3]"},"note":"The value 3 differs from 2, so it is copied to slot 1 and write advances."},{"at":{"read":4,"write":2},"vars":{"value":"2","kept":"[1, 3]"},"note":"The value 2 equals 2, so only read advances."},{"at":{"read":5,"write":2},"vars":{"value":"4","kept":"[1, 3, 4]"},"note":"The value 4 differs from 2, so it is copied to slot 2 and write advances."},{"at":{"read":6,"write":3},"vars":{"kept":"[1, 3, 4]"},"note":"The scan ends. The kept prefix [1, 3, 4] holds three values, so the method returns 3."}]}
```

#### Keeping At Most Two Copies

The input is the sorted array `[1, 1, 1, 2, 2, 3]`. A value enters the kept prefix when fewer than two slots are written, or when it differs from the value two slots behind `write`. The test reads the kept prefix, and `read` still moves by one. The scan skips the third copy of 1 and keeps both copies of 2.

```trace
{"cells":[1,1,1,2,2,3],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"value":"1","kept":"[1]"},"note":"The value 1 is admitted because fewer than two values are written."},{"at":{"read":1,"write":1},"vars":{"value":"1","kept":"[1, 1]"},"note":"The value 1 is admitted because fewer than two values are written."},{"at":{"read":2,"write":2},"vars":{"value":"1","kept":"[1, 1]"},"note":"The value 1 equals the value 1 two slots behind write, so it is skipped."},{"at":{"read":3,"write":2},"vars":{"value":"2","kept":"[1, 1, 2]"},"note":"The value 2 is admitted because it differs from the value 1 two slots behind write."},{"at":{"read":4,"write":3},"vars":{"value":"2","kept":"[1, 1, 2, 2]"},"note":"The value 2 is admitted because it differs from the value 1 two slots behind write."},{"at":{"read":5,"write":4},"vars":{"value":"3","kept":"[1, 1, 2, 2, 3]"},"note":"The value 3 is admitted because it differs from the value 2 two slots behind write."},{"at":{"read":6,"write":5},"vars":{"kept":"[1, 1, 2, 2, 3]"},"note":"The scan ends with five kept values, so the method returns 5."}]}
```

<!-- stage: code -->
### The Compaction In Java

```java
static int removeValue(int[] nums, int val) {
    int write = 0;
    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != val) {
            nums[write] = nums[read];
            write++;
        }
    }
    return write;
}
```

An empty array skips the loop and returns 0. When every value equals `val`, `write` stays 0. When no value equals `val`, each value copies onto itself, which is harmless and keeps the code free of a special case. The method mutates the array in place and returns the length of the kept prefix. Slots at index `write` and above hold stale values, so the caller must read only the prefix.

<!-- stage: applicability -->
### When Read And Write Fit

#### The Invariant

The invariant is that `nums[0..write-1]` holds exactly the admitted values among `nums[0..read-1]`, in their original order. It holds at the start with `read = write = 0`. Each iteration either appends one admitted value and advances both indexes, or discards one value and advances only `read`. The invariant gives the answer when `read` reaches the end.

#### The False Friend

The nearest wrong idea is a sliding window. A window has a left boundary that removes state from a range. The write index removes nothing. It marks where the next output value goes, and the values behind it are final. Code that shrinks `write` to undo an earlier choice has left this pattern.

#### Conditions That Break The Fit

The method needs a test that decides a value from that value and the kept prefix alone. A test that needs values after `read` cannot run in one pass. The method also mutates the input, so a contract that forbids writing to the array needs a new array. Finally, the order is stable only when each kept value is copied in read order.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Element (LeetCode 27)
<!-- id: tp-remove-element -->

**Prerequisites.** The compaction of this lesson.

**Problem.** Given an integer array `nums` and an integer `val`, remove every occurrence of `val` in place. Return `k`, the number of values not equal to `val`. The first `k` slots of `nums` must hold those values in their original order. Slots from index `k` on may hold any value.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 100`; the empty array is valid.
- **Values** are `int` values from 0 to 50, and `val` is an `int` from 0 to 100.
- **Order** of the kept values equals their order in the input.
- **Extra space** is O(1).

**Example 1.** Input `nums = [4,1,4,2,4,3]` and `val = 4`, output `k = 3` with prefix `[1,2,3]`.

**Example 2.** Input `nums = [7,7]` and `val = 7`, output `k = 0`.

**Hint.** Copy a value only when it passes the test. What does `write` count at every moment?

**Changed decision.** Basic case: one pass that keeps the original order of the values that stay.

#### [Vary] Move Zeroes (LeetCode 283)
<!-- id: tp-move-zeroes -->

**Prerequisites.** The first exercise above.

**Problem.** Given an integer array `nums`, move every `0` to the end in place. The nonzero values keep their relative order, and the array length does not change.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^4`.
- **Values** are `int` values; negative values are allowed.
- **Mutation** is required, and the method returns nothing.
- **Writes** should be few: a value that is already in place may be left untouched.

**Example 1.** Input `nums = [0,3,0,-2,5]`, output `[3,-2,5,0,0]`.

**Example 2.** Input `nums = [1,2]`, output `[1,2]`.

**Hint.** After the compaction, which slots hold stale values, and what should they hold?

**Changed decision.** The array keeps its length, so the stale suffix must be repaired with zeros.

#### [Boundary] Remove Duplicates From Sorted Array (LeetCode 26)
<!-- id: tp-dedup-sorted -->

**Prerequisites.** The first exercise and the kept prefix of this lesson.

**Problem.** Given an integer array `nums` sorted in nondecreasing order, keep one copy of each distinct value in place. Return `k`, the number of distinct values. The first `k` slots hold them in sorted order.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 3 * 10^4`; the empty array is valid.
- **Values** are `int` values, sorted in nondecreasing order.
- **Runs** may have length 1, so a value with no neighbor must stay.
- **Extra space** is O(1).

**Example 1.** Input `nums = [2,2,5,7,7,7,9]`, output `k = 4` with prefix `[2,5,7,9]`.

**Example 2.** Input `nums = []`, output `k = 0`.

**Hint.** The first value is always admitted. Which earlier value does each later value compare with?

**Changed decision.** The test looks at the kept prefix, and the empty input needs a guard before the first admission.

#### [Recognize] Remove Duplicates From Sorted Array II (LeetCode 80)
<!-- id: tp-dedup-twice -->

**Prerequisites.** The second trace of this lesson.

**Problem.** Given an integer array `nums` sorted in nondecreasing order, keep at most two copies of each value in place. Return `k`, the length of the result. The first `k` slots hold the result in sorted order.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 3 * 10^4`.
- **Values** are `int` values, sorted in nondecreasing order.
- **Copies** per value in the output are at most two.
- **Extra space** is O(1).

**Example 1.** Input `nums = [3,3,3,3,4,4,4]`, output `k = 4` with prefix `[3,3,4,4]`.

**Example 2.** Input `nums = [1,2,2,2,5]`, output `k = 4` with prefix `[1,2,2,5]`.

**Hint.** Compare the candidate with the value two slots behind `write`, and never with the value at `read - 2`. Why?

**Changed decision.** The admission rule reads the kept prefix at distance two, while `read` still advances by one.
