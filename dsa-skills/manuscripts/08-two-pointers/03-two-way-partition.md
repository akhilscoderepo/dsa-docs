<!-- lesson-kind: standard -->
<!-- lesson-id: two-way-partition -->
## Split An Array In Two

<!-- stage: context -->
### Active Particles Must Come First

A particle system holds five million particles in one array. Each frame, the renderer must see the active particles at the front and the expired particles at the back. Order inside each group does not matter. The first version copies the particles into a second array of the same size, active ones first. That doubles the memory use and adds a large copy to every frame, and the frame rate drops.

The goal is a rearrangement inside the same array. The question is how many moves a program needs when only the two groups matter and the order inside a group does not.

<!-- stage: naive -->
### Copying Into A Second Array

The direct method makes two passes over the input. The first pass copies the values that belong first into a new array. The second pass copies the other values after them.

```java
static int[] splitCopy(int[] nums) {
    int[] out = new int[nums.length];
    int p = 0;
    for (int x : nums) if (x % 2 == 0) out[p++] = x;
    for (int x : nums) if (x % 2 != 0) out[p++] = x;
    return out;
}
```

For `[3, 8, 5, 2, 6, 7]` the method returns `[8, 2, 6, 3, 5, 7]`. It is correct, and every value is written once. The cost is the second array.

```predict
The input holds 5 million values, and 4 of them are in the wrong half, 2 odd values at the front and 2 even values at the back. How many swaps does a rearrangement inside the array need at most, and how many values does `splitCopy` write?

Only the misplaced values must move, so a rearrangement inside the array needs 2 swaps here. The method `splitCopy` writes all 5 million values into a new array and holds 10 million slots at once. The time is O(n) and the extra space is O(n).
```

<!-- stage: bottleneck -->
### Most Values Are Already In Place

The method pays for every value, even for one that already stands in the correct half. A value that is already in the right region needs no write at all. The extra array costs O(n) space, and each frame pays O(n) writes where a few swaps would do.

The copy also hides a second question. A value in the wrong half must go somewhere, and the only slots that are free to receive it are slots that hold a value in the wrong half of the other kind. Two misplaced values of opposite kinds can simply trade places.

<!-- stage: insight -->
### Misplaced Values Trade Places

#### Two Regions And An Open Range

A **partition** of an array puts every value of one category before every value of the other category. Order inside a category is not promised. The scan keeps three ranges. Indexes before `left` hold values of the first category. Indexes after `right` hold values of the second category. The **unresolved range** from `left` to `right` holds values that the scan has not yet classified.

#### Closing The Open Range

The scan looks at `nums[left]`. If it already belongs to the first category, the scan moves `left` forward by one. If `nums[right]` belongs to the second category, the scan moves `right` back by one. Otherwise `nums[left]` is in the wrong region and so is `nums[right]`. The scan performs one **swap**, which exchanges the two values. After the swap, both ends are in valid regions and both pointers move.

Every step shrinks the unresolved range by at least one index. The loop runs at most `n` times and does at most `n / 2` swaps, so the cost is O(n) time and O(1) extra space.

<!-- names: partition, unresolved range, swap -->

#### The Same Idea In One Direction

A second form uses one scan index and one boundary. The boundary `store` marks the first slot of the second category. The scan index `i` moves forward. When `nums[i]` belongs to the first category, the scan swaps it with `nums[store]` and advances `store`. The invariant is the same: values before the boundary satisfy one category, and values after the scan index are unresolved. This form is the right one when a predicate against a pivot value is needed and the first category cannot be known from the ends alone.

<!-- stage: variables -->
### Three Names Mark The Regions

The opposite-end scan keeps three names, and all of them change during the scan: the pointers by moving and `nums` by swaps.

- **left** is the first index of the unresolved range, and indexes before it hold the first category.
- **right** is the last index of the unresolved range, and indexes after it hold the second category.
- **nums** is the array, and each swap exchanges two of its values.

The loop runs while `left < right`. When it stops, the unresolved range holds at most one value, or the pointers have crossed, and in both cases every value is in a valid region.

<!-- stage: trace -->
### Two Partitions On Different Inputs

#### Even Values First

The input is `[3, 8, 5, 2, 6, 7]`. The first category is the even values. The scan moves `left` over evens and `right` over odds. When `left` stands on an odd value and `right` stands on an even value, it swaps them. The scan ends when the two pointers meet or cross, and then no unresolved value is left.

```trace
{"cells":[3,8,5,2,6,7],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":5},"vars":{"array":"[3, 8, 5, 2, 6, 7]"},"note":"The value 7 at right is odd, so right moves left."},{"at":{"left":0,"right":4},"vars":{"array":"[6, 8, 5, 2, 3, 7]"},"note":"The values 3 and 6 are both misplaced, so the scan swaps them and moves both pointers."},{"at":{"left":1,"right":3},"vars":{"array":"[6, 8, 5, 2, 3, 7]"},"note":"The value 8 at left is even, so left moves right."},{"at":{"left":2,"right":3},"vars":{"array":"[6, 8, 2, 5, 3, 7]"},"note":"The values 5 and 2 are both misplaced, so the scan swaps them and moves both pointers."},{"at":{"left":3,"right":2},"vars":{"array":"[6, 8, 2, 5, 3, 7]"},"note":"The pointers have crossed. Every even value stands before every odd value."}]}
```

#### Values Below A Pivot First

The input is `[7, 2, 9, 3, 5, 1]` and the pivot is 5. The first category is values below 5. The scan index `i` visits each slot, and `store` marks where the next small value goes. A small value swaps into `store`, and then `store` advances. A value that is not small stays where it is, so the slots between `store` and `i` hold only values that are not small.

```trace
{"cells":[7,2,9,3,5,1],"pointers":["i","store"],"steps":[{"at":{"i":0,"store":0},"vars":{"array":"[7, 2, 9, 3, 5, 1]"},"note":"The value 7 is not below 5, so only i moves."},{"at":{"i":1,"store":0},"vars":{"array":"[2, 7, 9, 3, 5, 1]"},"note":"The value 2 is below 5, so it swaps with 7 at store and store advances."},{"at":{"i":2,"store":1},"vars":{"array":"[2, 7, 9, 3, 5, 1]"},"note":"The value 9 is not below 5, so only i moves."},{"at":{"i":3,"store":1},"vars":{"array":"[2, 3, 9, 7, 5, 1]"},"note":"The value 3 is below 5, so it swaps with 7 at store and store advances."},{"at":{"i":4,"store":2},"vars":{"array":"[2, 3, 9, 7, 5, 1]"},"note":"The value 5 is not below 5, so only i moves."},{"at":{"i":5,"store":2},"vars":{"array":"[2, 3, 1, 7, 5, 9]"},"note":"The value 1 is below 5, so it swaps with 9 at store and store advances."},{"at":{"i":6,"store":3},"vars":{"array":"[2, 3, 1, 7, 5, 9]"},"note":"The scan ends with store = 3. The first 3 slots hold the values below 5."}]}
```

<!-- stage: code -->
### The Opposite-End Scan In Java

```java
static void evenFirst(int[] nums) {
    int left = 0, right = nums.length - 1;
    while (left < right) {
        if (nums[left] % 2 == 0) left++;
        else if (nums[right] % 2 != 0) right--;
        else {
            int tmp = nums[left];
            nums[left] = nums[right];
            nums[right] = tmp;
            left++;
            right--;
        }
    }
}
```

The test for an even value is `x % 2 == 0`. The test `x % 2 == 1` fails for negative values, because Java gives `-3 % 2 == -1`. An empty or one-element array skips the loop. An array of all even values only moves `left`, and an array of all odd values only moves `right`, so both cases perform no swap.

<!-- stage: applicability -->
### When Splitting Fits

#### The Invariant

The invariant is that every index before `left` holds a first-category value and every index after `right` holds a second-category value. It holds at the start, because both ranges are empty. A move of `left` extends the first region with a value that belongs there. A move of `right` does the same for the second region. A swap places one value in each region.

#### The False Friend

The nearest wrong idea is stable compaction from the previous lesson. Compaction keeps the order of the kept values and may write many values. A partition promises only the two regions, and it writes at most two values per swap. Using a partition where the problem needs the original order gives a wrong answer. The values `[5, 2, 8, 3]` come back as `[8, 2, 5, 3]`, which is a valid partition, while a stable method returns `[2, 8, 5, 3]`.

#### Conditions That Break The Fit

The method needs a test that puts each value into one of two categories without looking at the others. It also mutates the array. A contract that asks for sorted order inside each category needs a sort after the partition. A test that depends on a neighbor, such as "greater than the previous value", does not describe two regions.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort Array By Parity (LeetCode 905)
<!-- id: tp-sort-by-parity -->

**Prerequisites.** The opposite-end scan of this lesson.

**Problem.** Given an integer array `nums`, rearrange it so that every even value comes before every odd value. Return the array. Any arrangement that satisfies the rule is accepted.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 5000`; the empty array is valid.
- **Values** are `int` values; negative values are allowed.
- **Parity** of a negative value follows `x % 2 == 0` for even and `x % 2 != 0` for odd.
- **Extra space** is O(1).

**Example 1.** Input `nums = [5,2,8,3]`, one valid output is `[8,2,5,3]`.

**Example 2.** Input `nums = [-1,-4]`, one valid output is `[-4,-1]`.

**Hint.** When the left value is odd and the right value is even, both are misplaced. What can you do with them together?

**Changed decision.** Basic case: swap two misplaced values instead of shifting a tail.

#### [Vary] Partition Around Pivot (Author exercise)
<!-- id: tp-partition-pivot -->

**Prerequisites.** The one-direction form in the insight of this lesson.

**Problem.** Given an integer array `nums` and an integer `pivot`, rearrange `nums` in place so that every value less than `pivot` comes before every value greater than or equal to `pivot`. Return `k`, the number of values less than `pivot`. The order inside each region is not specified.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values, and `pivot` is an `int`.
- **Return value** `k` is the index of the first value that is not less than `pivot`.
- **Extra space** is O(1).

**Example 1.** Input `nums = [7,2,9,3,5,1]` and `pivot = 5`, output `k = 3` and the first three slots hold `2`, `3` and `1` in some order.

**Example 2.** Input `nums = [6,6]` and `pivot = 6`, output `k = 0`.

**Hint.** The category depends on a comparison with `pivot`, so the boundary and the scan index move in the same direction.

**Changed decision.** The category comes from a comparison with a parameter, and the answer reports the size of the first region.

#### [Boundary] One Empty Region (Author exercise)
<!-- id: tp-one-empty-region -->

**Prerequisites.** The first exercise and the code stage of this lesson.

**Problem.** Partition an integer array so that even values come first, using the opposite-end scan of this lesson. Return the number of swaps that the scan performs.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 1000`; the empty array is valid.
- **Values** are `int` values; negative values are allowed.
- **Scan** is the opposite-end scan, and a swap happens only when both ends are misplaced.
- **Return type** is `int`.

**Example 1.** Input `nums = [2,4,6]`, output 0.

**Example 2.** Input `nums = [1,3]`, output 0.

**Hint.** What does the scan do when every value is even, and what does it do when every value is odd?

**Changed decision.** One region is empty, so the scan moves one pointer across the whole array and never swaps.

#### [Recognize] Sort Array By Parity II (LeetCode 922)
<!-- id: tp-parity-two -->

**Prerequisites.** All exercises above.

**Problem.** Given an integer array `nums` that holds as many even values as odd values, rearrange it in place so that `nums[i]` is even when `i` is even and `nums[i]` is odd when `i` is odd. Return the array. Any valid arrangement is accepted.

**Constraints.** The limits are:
- **Length** is an even number with `2 <= nums.length <= 2 * 10^4`.
- **Values** are `int` values from 0 to 1000, with exactly half of them even.
- **Destination** of each value depends on the parity of its index.
- **Extra space** is O(1).

**Example 1.** Input `nums = [4,1,2,3]`, one valid output is `[4,1,2,3]`.

**Example 2.** Input `nums = [3,2,1,4]`, one valid output is `[2,3,4,1]`.

**Hint.** Use one pointer on the even slots and one on the odd slots. Each pointer jumps by two.

**Changed decision.** The two regions interleave, so each pointer steps by two instead of one.
