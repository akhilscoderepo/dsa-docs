<!-- lesson-kind: standard -->
<!-- lesson-id: stable-compaction -->
## Stable Compaction

<!-- stage: context -->
### Pulling Defects Off The Line

Parts roll along a conveyor belt in a fixed order, and an inspector must remove every defective part without disturbing the order of the good ones. The belt has no spare lane, so good parts can only slide forward into the gaps the defects leave. When she is done, the good parts must sit at the start of the belt in their original sequence, and she must call out how many there are.

Nothing about the belt can be lengthened or shortened, and the parts that fall off the end are simply no longer counted. This is the situation behind a whole family of array problems where you must filter an array using the array itself as the workspace, and the order of what survives still matters.

<!-- stage: naive -->
### Close The Gap After Every Removal

The literal way to remove a part is to slide everything after it one place forward, then continue from the same position.

```java
static int removeByShifting(int[] nums, int bad) {
    int length = nums.length;
    int i = 0;
    while (i < length) {
        if (nums[i] == bad) {
            for (int j = i + 1; j < length; j++) nums[j - 1] = nums[j];
            length--;
        } else {
            i++;
        }
    }
    return length;
}
```

This is correct and keeps the order. For `[5, 1, 5, 5, 2]` with the bad value 5 it returns 2 and the first two slots hold `[1, 2]`.

<!-- stage: bottleneck -->
### Every Removal Moves The Whole Tail

Each removal shifts all the elements after it, so the cost of one removal is up to `n`. When many elements are bad the total grows as O(n^2). If every one of 100,000 elements is bad, the first removal shifts 99,999 elements, the next shifts 99,998, and so on, for about five billion moves in total.

The work is almost all wasted. A good element after a removed one is moved forward by one slot, and if more bad elements follow, it is moved again, and again. Each good element may be shuffled many times before it settles, even though its final position was determined by a single fact: how many good elements precede it. The extra space is O(1), which is the only thing the method does well.

<!-- stage: insight -->
### One Index Reads, One Writes

The final position of a good element is the number of good elements that came before it. Keep that count as a position, and each good element can be copied straight to its final slot the moment it is seen. Nothing needs to be moved twice.

This is **stable compaction**. The scan uses a read index that visits every slot, and a **write index** that marks the next slot to receive a good element. For each element, if it is kept, copy it to the write index and advance the write index. If it is discarded, do nothing. The invariant is that `nums[0..write-1]` holds exactly the accepted values among the elements already read, in their original order. Because the write index can never run ahead of the read index, a write only lands on a slot that has already been read, so no unread value is ever destroyed.

<!-- names: stable compaction, write index, stable -->

The word **stable** means that kept elements keep their relative order, which is the promise the invariant makes. The result is the count `write`. Everything from `write` onward is leftover data and carries no meaning. The method does not shorten the array and must not claim to, because a Java array has a fixed length. This connects directly to the mutation-contract habit from Chapter 00, where the boundary `k` names the meaningful prefix.

Stability is not free. If order did not matter, a faster-looking variant overwrites a removed element with the last element and shrinks the count, which scrambles the order. That variant answers a different question, and this lesson is about the one that preserves order.

<!-- stage: variables -->
### The Read And Write Pair

The read index `read` runs from 0 to the end and examines each element once. The write index `write` starts at 0 and counts the accepted elements, which is also the next free slot. At every moment `write <= read`, so the region between them contains values that were read and either accepted earlier, and moved, or rejected. The filter test is the only part that changes between problems, so keep it as a clearly named condition and leave the two indices alone.

<!-- stage: trace -->
### Removing The Fives

Take `[5, 1, 5, 5, 2]` and remove every 5. At read 0 the value is 5, which is rejected, so the write index stays at 0. At read 1 the value 1 is accepted and copied to slot 0, which turns the array into `[1, 1, 5, 5, 2]`, and the write index moves to 1. At read 2 and read 3 the values are 5, both rejected, and nothing changes.

At read 4 the value 2 is accepted and copied to slot 1, giving `[1, 2, 5, 5, 2]`, and the write index becomes 2. The loop ends with `write = 2`, so the answer is the prefix `[1, 2]`. The last three slots still hold `5, 5, 2`, which are leftovers, and the final 2 appears twice, once as the answer and once as stale data. The step that deserves attention is read 4, where a value moves a long distance in one copy, from slot 4 to slot 1, instead of being nudged forward several times.

```trace
{"cells":[5,1,5,5,2],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"kept":0,"array":"[5,1,5,5,2]"},"note":"Read 0: the value is 5, so it is rejected. Nothing is written and write stays at 0."},{"at":{"read":1,"write":1},"vars":{"kept":1,"array":"[1,1,5,5,2]"},"note":"Read 1: 1 is kept and copied to slot 0. The array reads [1, 1, 5, 5, 2]; write moves to 1."},{"at":{"read":2,"write":1},"vars":{"kept":1,"array":"[1,1,5,5,2]"},"note":"Read 2: the value is 5, so it is rejected. Nothing is written and write stays at 1."},{"at":{"read":3,"write":1},"vars":{"kept":1,"array":"[1,1,5,5,2]"},"note":"Read 3: the value is 5, so it is rejected. Nothing is written and write stays at 1."},{"at":{"read":4,"write":2},"vars":{"kept":2,"array":"[1,2,5,5,2]"},"note":"Read 4: 2 is kept and copied to slot 1. The array reads [1, 2, 5, 5, 2]; write moves to 2."},{"at":{"read":5,"write":2},"vars":{"kept":2,"array":"[1,2,5,5,2]"},"note":"Done. k = 2, so the answer is the prefix [1,2]. The last three slots are stale leftovers."}]}
```

<!-- stage: code -->
### Filtering In Place

```java
static int removeElement(int[] nums, int val) {
    int kept = 0;                                   // nums[0..kept-1] holds the survivors read so far
    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != val) nums[kept++] = nums[read];
    }
    return kept;                                    // slots from kept onward are unspecified
}

static void moveZeroes(int[] nums) {
    int kept = 0;
    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != 0) nums[kept++] = nums[read];
    }
    for (int i = kept; i < nums.length; i++) nums[i] = 0;   // the contract here asks for zeroes at the end
}
```

`removeElement` returns the count and leaves the suffix alone, because its contract says the suffix is unspecified. `moveZeroes` has a different contract, because the whole array must end up as survivors followed by zeroes, so it needs a second loop to fill the suffix. Both run in O(n) time and O(1) extra space, and each element is read once and written at most once. Reading the contract decides whether the second loop is required.

<!-- stage: applicability -->
### When Order Must Survive

Use stable compaction when you must keep selected values in their original order and reuse the input array. The invariant to state is that `nums[0..write-1]` contains exactly the accepted values already read, in order. Return `write` as the result, and treat everything beyond it as meaningless unless the contract says to fill it.

The false friend is the swap-with-last shortcut. It is O(n) as well and needs no second loop, but it reorders the survivors, so it is correct only when the problem explicitly says order does not matter. Another is building a new list, which is simpler and correct whenever extra space is allowed. This lesson is for the case where the space contract forbids it.

Java adds a few traps. The array never shrinks, so loops that run to `nums.length` after compaction will read stale slots. Testing evenness with `v % 2 == 1` misses negative odd numbers, because `-3 % 2` is `-1`, so test `v % 2 != 0` for odd and `v % 2 == 0` for even. And a filter that depends on neighbors must be checked for whether reading `nums[read - 1]` sees an original value or an overwritten one.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Element (LeetCode 27)
<!-- id: ar-remove-element -->

**Prerequisites.** The read and write indices in this lesson; Chapter 00 mutation contracts.

**Problem.** Given an integer array `nums` and a value `val`, remove every occurrence of `val` in place and return the number `k` of elements that remain. The first `k` slots must hold the remaining elements, and what follows them is irrelevant.

**Constraints.** 0 <= nums.length <= 100 and 0 <= nums[i], val <= 100. Use O(1) extra space and keep the order of the survivors.

**Example 1.** Input `nums = [5, 1, 5, 5, 2]`, `val = 5`, output `k = 2` with `nums[0..1] = [1, 2]`.

**Example 2.** Input `nums = [4]`, `val = 4`, output `k = 0`, so no slot holds meaningful data afterward.

**Hint.** Which index counts the elements you have decided to keep? When can a write overwrite a slot you have not read yet?

**Changed decision.** First rung: introduces the read and write indices and the meaning of the returned count.

#### [Vary] Move Zeroes (LeetCode 283)
<!-- id: ar-move-zeroes -->

**Prerequisites.** The remove-element exercise above.

**Problem.** Given an integer array, move all zeroes to the end while keeping the relative order of the non-zero values, modifying the array in place. Unlike the previous exercise, the entire array must reflect the result.

**Constraints.** 1 <= nums.length <= 10^4 and -2^31 <= nums[i] <= 2^31 - 1. Do not allocate a second array.

**Example 1.** Input `nums = [0, 0, 4, 0, 9, 2]`, output `[4, 9, 2, 0, 0, 0]`.

**Example 2.** Input `nums = [0]`, output `[0]`, since a single zero is already in place.

**Hint.** After copying the non-zero values forward, what must you do with the slots from `kept` to the end? Why was this not needed before?

**Changed decision.** The contract changes from an unspecified suffix to a fully specified array, so a fill step is added.

#### [Boundary] Keep Evens (Author exercise)
<!-- id: ar-keep-evens -->

**Prerequisites.** The two exercises above.

**Problem.** Given `nums`, overwrite its prefix with its even values in their original order and return the count `k`. Negative numbers must be classified correctly, so choose the parity test with care.

**Constraints.** 0 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. Use O(1) extra space.

**Example 1.** Input `nums = [-2, 3, 4]`, output `k = 2` with prefix `[-2, 4]`.

**Example 2.** Input `nums = [1, 3]`, output `k = 0`, because there is no even value.

**Hint.** What does `-3 % 2` evaluate to in Java? Which test, `== 1` or `!= 0`, treats negative odd numbers correctly?

**Changed decision.** The filter condition changes to a parity test, and the hazard moves from indexing to the sign of the remainder.

#### [Recognize] Filter Positives (Author exercise)
<!-- id: ar-filter-positives -->

**Prerequisites.** All three exercises above.

**Problem.** Given `nums`, overwrite its prefix with the strictly positive values in their original order and return the count `k`. The filter changes again, but the invariant on the read and write indices must stay the same.

**Constraints.** 0 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. Zero is not positive.

**Example 1.** Input `nums = [3, -1, 0, 5, -7, 2]`, output `k = 3` with prefix `[3, 5, 2]`.

**Example 2.** Input `nums = [-1, 0]`, output `k = 0`, since neither value is strictly positive.

**Hint.** Which part of your code is the test and which part is the bookkeeping? What stays identical when only the test changes?

**Changed decision.** Only the acceptance test changes, which shows the pattern is the two-index bookkeeping and not the specific filter.
