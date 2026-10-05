<!-- lesson-kind: standard -->
<!-- lesson-id: three-way-partition -->
## Split An Array In Three

<!-- stage: context -->
### Grouping Requests By Priority

A server keeps one million pending requests in an array. Each request carries a priority of 0, 1 or 2. The scheduler wants all requests of priority 0 first, then priority 1, then priority 2. The requests are objects with many other fields, so the program cannot just count the priorities and rewrite them.

The two-way split of the previous lesson separates two groups. A third group breaks it: after one split, the second group still mixes priorities 1 and 2. The question is how one pass can settle all three groups.

<!-- stage: naive -->
### Sorting By Priority

The direct method sorts the array with a comparator on the priority field. The sort handles any number of distinct priorities, so it certainly handles three.

```java
static void groupSlow(int[] priority) {
    Integer[] boxed = new Integer[priority.length];
    for (int i = 0; i < priority.length; i++) boxed[i] = priority[i];
    Arrays.sort(boxed);
    for (int i = 0; i < priority.length; i++) priority[i] = boxed[i];
}
```

For `[2, 0, 2, 1, 1, 0]` the method returns `[0, 0, 1, 1, 2, 2]`. It is correct, and it needs no idea beyond a library call.

```predict
The array holds one million values and each value is 0, 1 or 2. About how many comparisons does a comparison sort make, and how many would a single scan need?

A comparison sort on one million values makes about n log2 n comparisons, which is near 20 million. A single scan reads each value once, so it needs about one million reads. The sort is O(n log n) and the scan is O(n).
```

<!-- stage: bottleneck -->
### A Sort Does More Work Than Needed

A comparison sort establishes the order of every pair, and it pays O(n log n) for that. This problem has only three groups, and values inside one group are equal for the purpose of the task. The sort spends most of its comparisons on pairs that have the same group, where the answer carries no information.

The boxed copy adds O(n) extra memory on top of that. A scan that decides a value's group at the moment it sees the value would need no order inside a group, and it would not need to look at the value twice.

<!-- stage: insight -->
### Four Regions Close Around One Open Range

#### Three Boundaries In One Array

A **three-way partition** puts every value of the first group before every value of the second group, and every value of the second group before every value of the third group. This partition is also called the **Dutch national flag** partition. The scan keeps three indexes `low`, `mid` and `high`. Indexes before `low` hold the first group. Indexes from `low` up to but not including `mid` hold the **middle region**, the second group. Indexes from `mid` to `high` are unresolved, and indexes after `high` hold the third group.

<!-- names: three-way partition, Dutch national flag, middle region -->

#### One Rule For Each Value Seen

The scan looks at `nums[mid]`. A first-group value swaps with `nums[low]`, and then both `low` and `mid` advance. A second-group value is already in the middle region, so only `mid` advances. A third-group value swaps with `nums[high]`, and then `high` moves back by one.

#### Why The Mid Index Waits After A High Swap

The value that arrives at `mid` from `high` has not been inspected. It can belong to any group. The scan must therefore leave `mid` where it is and look at the new value in the next iteration. After a swap with `low`, the arriving value came from the middle region, so it is known to be a second-group value, and `mid` can advance. The loop runs while `mid <= high`, and each iteration shrinks the unresolved range by one, so the scan costs linear time and uses a constant number of extra variables.

<!-- stage: variables -->
### Three Indexes Split The Array

The scan keeps three indexes, and all of them change.

- **low** is the first slot of the middle region, and every slot before it holds the first group.
- **mid** is the slot under inspection, and slots from `low` to `mid - 1` hold the middle region.
- **high** is the last unresolved slot, and every slot after it holds the third group.

The loop continues while `mid` has not passed `high`. It stops when no unresolved slot is left.

<!-- stage: trace -->
### Two Three-Way Scans

#### Grouping Priorities 0, 1 And 2

The input is `[2, 0, 2, 1, 1, 0]`. The first step sees a 2 at `mid` and swaps it with the slot at `high`. The scan does not advance `mid` because the incoming value is unread. The scan ends when `mid` passes `high`.

```trace
{"cells":[2,0,2,1,1,0],"pointers":["low","mid","high"],"steps":[{"at":{"low":0,"mid":0,"high":5},"vars":{"array":"[0, 0, 2, 1, 1, 2]"},"note":"The value 2 belongs to the third group, so it swaps with the slot at high and high moves back. The value now at mid is unread, so mid stays."},{"at":{"low":0,"mid":0,"high":4},"vars":{"array":"[0, 0, 2, 1, 1, 2]"},"note":"The value 0 belongs to the first group, so it swaps with the slot at low, and low and mid both advance."},{"at":{"low":1,"mid":1,"high":4},"vars":{"array":"[0, 0, 2, 1, 1, 2]"},"note":"The value 0 belongs to the first group, so it swaps with the slot at low, and low and mid both advance."},{"at":{"low":2,"mid":2,"high":4},"vars":{"array":"[0, 0, 1, 1, 2, 2]"},"note":"The value 2 belongs to the third group, so it swaps with the slot at high and high moves back. The value now at mid is unread, so mid stays."},{"at":{"low":2,"mid":2,"high":3},"vars":{"array":"[0, 0, 1, 1, 2, 2]"},"note":"The value 1 belongs to the middle region, so only mid advances."},{"at":{"low":2,"mid":3,"high":3},"vars":{"array":"[0, 0, 1, 1, 2, 2]"},"note":"The value 1 belongs to the middle region, so only mid advances."},{"at":{"low":2,"mid":4,"high":3},"vars":{"array":"[0, 0, 1, 1, 2, 2]"},"note":"The pointer mid has passed high, so no slot is unresolved."}]}
```

#### Grouping Around A Pivot Value

The input is `[7, 5, 2, 9, 5, 1]` and the pivot is 5. The first group is values below 5, the second is values equal to 5, and the third is values above 5. The scan uses the same rules, and a comparison with the pivot replaces the group number. The pivot value 5 appears twice, and both copies end next to each other.

```trace
{"cells":[7,5,2,9,5,1],"pointers":["low","mid","high"],"steps":[{"at":{"low":0,"mid":0,"high":5},"vars":{"array":"[1, 5, 2, 9, 5, 7]"},"note":"The value 7 belongs to the values above the pivot, so it swaps with the slot at high and high moves back. The value now at mid is unread, so mid stays."},{"at":{"low":0,"mid":0,"high":4},"vars":{"array":"[1, 5, 2, 9, 5, 7]"},"note":"The value 1 belongs to the values below the pivot, so it swaps with the slot at low, and low and mid both advance."},{"at":{"low":1,"mid":1,"high":4},"vars":{"array":"[1, 5, 2, 9, 5, 7]"},"note":"The value 5 belongs to the values equal to the pivot, so only mid advances."},{"at":{"low":1,"mid":2,"high":4},"vars":{"array":"[1, 2, 5, 9, 5, 7]"},"note":"The value 2 belongs to the values below the pivot, so it swaps with the slot at low, and low and mid both advance."},{"at":{"low":2,"mid":3,"high":4},"vars":{"array":"[1, 2, 5, 5, 9, 7]"},"note":"The value 9 belongs to the values above the pivot, so it swaps with the slot at high and high moves back. The value now at mid is unread, so mid stays."},{"at":{"low":2,"mid":3,"high":3},"vars":{"array":"[1, 2, 5, 5, 9, 7]"},"note":"The value 5 belongs to the values equal to the pivot, so only mid advances."},{"at":{"low":2,"mid":4,"high":3},"vars":{"array":"[1, 2, 5, 5, 9, 7]"},"note":"The pointer mid has passed high, so no slot is unresolved."}]}
```

<!-- stage: code -->
### The Three-Way Scan In Java

```java
static void groupByThree(int[] nums) {
    int low = 0, mid = 0, high = nums.length - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            swap(nums, low++, mid++);
        } else if (nums[mid] == 1) {
            mid++;
        } else {
            swap(nums, mid, high--);
        }
    }
}

static void swap(int[] a, int i, int j) {
    int t = a[i]; a[i] = a[j]; a[j] = t;
}
```

The loop condition is `mid <= high`, not `mid < high`. With `<` the slot at `high` is never inspected when `mid == high`, and one value stays in the wrong group. An empty array has `high = -1`, so the loop never runs. An array of one group only moves `mid`, or only `high`, and the other regions stay empty.

<!-- stage: applicability -->
### When Three Regions Fit

#### The Invariant

The invariant is that `nums[0..low-1]` holds the first group, `nums[low..mid-1]` holds the middle region, and `nums[high+1..n-1]` holds the third group. The slots `nums[mid..high]` are unresolved. At the start the three known regions are empty. Each of the three cases keeps the invariant true while it shrinks the unresolved range by one slot.

#### The False Friend

The nearest wrong idea is to advance `mid` after every swap, as the two-way scan advances both pointers. After a swap with `high`, the value at `mid` is unread. Moving on leaves a value of any group in the middle region. The input `[1, 2, 0]` shows the failure. The scan swaps the 2 with the 0 to give `[1, 0, 2]`, then moves past the 0 without reading it, and the array stays unsorted.

#### Conditions That Break The Fit

The method needs a test that places each value into exactly one of three ordered groups. More than three groups need a different method, such as counting by group or sorting. The method mutates the array, and it does not keep the original order inside a group.

<!-- stage: exercises -->
### Exercises

#### [Build] Partition 0,1,2 (Author exercise)
<!-- id: tp-partition-012 -->

**Prerequisites.** The four-region invariant of this lesson.

**Problem.** Given an integer array `nums` whose values are only 0, 1 and 2, rearrange it in place so that all 0 values come first, then all 1 values, then all 2 values. Return an array `{c0, c1, c2}` with the number of 0, 1 and 2 values. Use one scan and no counting array.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^4`; the empty array is valid.
- **Values** are only 0, 1 and 2.
- **Scan** is the three-way scan of this lesson, and the method makes no sort call.
- **Extra space** is O(1).

**Example 1.** Input `nums = [1,2,0,1]`, the array becomes `[0,1,1,2]` and the output is `[1,2,1]`.

**Example 2.** Input `nums = []`, output `[0,0,0]`.

**Hint.** After the scan, `low` and `mid` and `high` sit at the region boundaries. Which index differences give the counts?

**Changed decision.** Basic case: the scan reports the boundaries as counts after it finishes the four regions.

#### [Vary] Sort Colors (LeetCode 75)
<!-- id: tp-sort-colors -->

**Prerequisites.** The first exercise above.

**Problem.** Given an array `nums` with `n` objects colored red, white or blue, represented by 0, 1 and 2, sort the array in place so that the colors appear in the order red, white, blue. Do not call a library sort.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 300`.
- **Values** are only 0, 1 and 2.
- **Mutation** is required, and the method returns nothing.
- **Passes** over the array: one, with O(1) extra space.

**Example 1.** Input `nums = [2,1,0,2,1]`, output `[0,1,1,2,2]`.

**Example 2.** Input `nums = [1]`, output `[1]`.

**Hint.** The colors keep the same meaning as the groups of this lesson, and the formal problem adds no new rule.

**Changed decision.** The formal statement replaces group names with colors and drops the count output.

#### [Boundary] Reinspect Swapped High (Author exercise)
<!-- id: tp-reinspect-high -->

**Prerequisites.** The false friend of this lesson.

**Problem.** Run the three-way scan on an array of 0, 1 and 2. Return the number of iterations of the loop, where each iteration inspects `nums[mid]` once. A swap with `high` does not advance `mid`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 1000`.
- **Values** are only 0, 1 and 2.
- **Loop** runs while `mid <= high`.
- **Return type** is `int`, the count of loop iterations.

**Example 1.** Input `nums = [2,0]`, output 2.

**Example 2.** Input `nums = [1,2,0]`, output 3.

**Hint.** After the first swap in `[2,0]`, which value sits at `mid`, and has the scan read it yet?

**Changed decision.** The count equals the array length, because every slot, including a value that arrives from `high`, is inspected once.

#### [Recognize] Three-Way Pivot Partition (Author exercise)
<!-- id: tp-three-way-pivot -->

**Prerequisites.** All exercises above and the second trace of this lesson.

**Problem.** Given an integer array `nums` and an integer `pivot`, rearrange `nums` in place so that values less than `pivot` come first, then values equal to `pivot`, then values greater than `pivot`. Return `{a, b}`, where `a` is the index of the first value equal to `pivot` and `b` is the index of the first value greater than `pivot`. When no value equals `pivot`, `a` equals `b`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values, and `pivot` is an `int`.
- **Order** inside each region is not specified.
- **Extra space** is O(1).

**Example 1.** Input `nums = [7,5,2,9,5,1]` and `pivot = 5`, output `{2,4}`.

**Example 2.** Input `nums = [4,8]` and `pivot = 6`, output `{1,1}`.

**Hint.** Compare `nums[mid]` with `pivot` to choose among the three rules. Which boundary values are the answer?

**Changed decision.** The groups come from comparisons with a parameter, so the answer reports region starts.
