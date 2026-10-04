<!-- lesson-kind: standard -->
<!-- lesson-id: arrays-sort -->
## Sort A Primitive Array

<!-- stage: context -->
### A Report That Reorders The Readings

A monitoring service stores 100000 temperature readings in arrival order. A report needs the median reading, so a helper sorts the array and picks the middle value. The report is correct. The next screen draws the same array as a time series, and the line now rises smoothly, because the helper reordered the caller's data. Nobody wrote a bug in the sort. Nobody stated who owns the order of the array.

Sorting changes the array it receives. This lesson answers two questions. How does a program sort a primitive array in O(n log n) time, and how does it keep the original order when the caller still needs it?

<!-- stage: naive -->
### Picking The Smallest Value n Times

The direct method scans the unsorted part of the array for its smallest value. It swaps that value to the front of the unsorted part and repeats until one value remains.

```java
static void selectionSort(int[] nums) {
    for (int i = 0; i < nums.length - 1; i++) {
        int smallest = i;
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[j] < nums[smallest]) {
                smallest = j;
            }
        }
        int tmp = nums[i];
        nums[i] = nums[smallest];
        nums[smallest] = tmp;
    }
}
```

On `[9, 2, 7, 2]` the method finds 2 at index 1 and swaps it to index 0. It then finds the second 2 and leaves it in place. The result is `[2, 2, 7, 9]`, and the original order of the array is gone.

<!-- stage: bottleneck -->
### Repeated Scans And A Lost Order

```predict
The array holds 100000 readings. About how many comparisons does the double loop make, and what does the caller see afterward?

The loops make about n * (n - 1) / 2 comparisons, which is roughly 5 billion and O(n^2). The caller sees the sorted array and has no way to recover the arrival order.
```

Each pass over the unsorted part finds one smallest value and learns nothing that the next pass can reuse. The cost is O(n^2), which is too slow for 100000 values. The method also writes into the array it receives, so a second problem exists next to the cost. The library already provides a sort that runs in O(n log n) time. What remains is a decision about ownership: sort the caller's array, or sort a copy of it.

<!-- stage: insight -->
### Call The Library Sort On Your Data

The method should call the library, and it should call the library on an array that it is allowed to change.

#### What The Library Call Guarantees

The call `Arrays.sort(nums)` sorts an `int[]` into ascending order in place. The documentation promises O(n log n) time on every input. After the call, every adjacent pair satisfies `nums[i] <= nums[i + 1]`, and equal values sit next to each other in one contiguous run. Later scans depend on both facts.

#### Sort A Copy To Keep The Original

A **sorted copy** is a new array with the same values in ascending order. The call `Arrays.copyOf(nums, nums.length)` builds the copy in O(n) time and O(n) space. The method then sorts the copy and leaves `nums` as the caller passed it. The caller's array is the single owner of the arrival order, and the copy is the single owner of the sorted order.

#### Sort Only A Range

A **half-open range** `[from, to)` includes index `from` and excludes index `to`. The call `Arrays.sort(nums, from, to)` sorts only that range and never touches other positions. The range has length `to - from`, and the call with `from == to` does nothing. A `from` greater than `to` throws `IllegalArgumentException`. A bound outside `0..nums.length` throws `ArrayIndexOutOfBoundsException`.

<!-- names: Arrays.sort, sorted copy, half-open range -->

<!-- stage: variables -->
### The Array, The Copy And The Bounds

The code needs a few named pieces, and each has one meaning.

- **nums** is the caller's array, and the method never writes to it.
- **copy** is the array that the method sorts and then reads.
- **from** is the first index of a range to sort and is included.
- **to** is the index after the last position of the range and is excluded.

Only `copy` and the range `[from, to)` change during a sort.

<!-- stage: trace -->
### Sorting A Copy And A Range

#### Sorting A Copy And Checking Neighbors

Take `nums = [9, 2, 7, 2]`. The method copies the array and sorts the copy into `[2, 2, 7, 9]`. The array `nums` keeps its order. A scan then compares each value with the one on its left. The pair `2, 2` shows that equal values are adjacent, and every other pair increases.

#### Sorting Only A Range

Now take `[8, 6, 4, 2, 0]` and the call `Arrays.sort(a, 1, 4)`. The range holds the values at indexes 1, 2 and 3, which are `6, 4, 2`. After the call the range holds `2, 4, 6`. The values 8 at index 0 and 0 at index 4 stay where they were.

#### Stepping Through Both Cases

```trace
{"cells":[2,2,7,9],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"nums":"[9, 2, 7, 2]","copy":"[9, 2, 7, 2]"},"note":"The method copies nums. Both arrays hold 9, 2, 7, 2."},{"at":{"i":-1},"vars":{"nums":"[9, 2, 7, 2]","copy":"[2, 2, 7, 9]"},"note":"The library sort orders the copy. The array nums keeps its order."},{"at":{"i":1},"vars":{"left":2,"right":2,"copy":"[2, 2, 7, 9]"},"note":"Compare 2 with 2: the values are equal, so the equal values form one run."},{"at":{"i":2},"vars":{"left":2,"right":7,"copy":"[2, 2, 7, 9]"},"note":"Compare 2 with 7: the left value is smaller, so the order holds."},{"at":{"i":3},"vars":{"left":7,"right":9,"copy":"[2, 2, 7, 9]"},"note":"Compare 7 with 9: the left value is smaller, so the order holds."}]}
```

```trace
{"cells":[8,6,4,2,0],"pointers":["lo","hi"],"steps":[{"at":{"lo":1,"hi":4},"vars":{"array":"[8, 6, 4, 2, 0]"},"note":"The call covers indexes 1, 2 and 3. Index 4 is the excluded end."},{"at":{"lo":1,"hi":4},"vars":{"range":"[6, 4, 2]","array":"[8, 6, 4, 2, 0]"},"note":"The range holds 6, 4, 2 before the sort."},{"at":{"lo":1,"hi":4},"vars":{"range":"[2, 4, 6]","array":"[8, 2, 4, 6, 0]"},"note":"The range holds 2, 4, 6 after the sort. The values 8 and 0 stay in place."}]}
```

<!-- stage: code -->
### Copy First And Then Sort

#### Sorted Copy And Range Sort

```java
static int[] sortedCopy(int[] nums) {
    int[] copy = Arrays.copyOf(nums, nums.length);
    Arrays.sort(copy);
    return copy;
}

static void sortRange(int[] nums, int from, int to) {
    Arrays.sort(nums, from, to);
}
```

#### What The Methods Cost

Both methods run in O(n log n) time for a range or an array of n values. The copy costs O(n) extra space. The range sort adds no copy, and its extra space is that of the library sort. The comparison between values uses the operators on `int`, so no subtraction appears anywhere.

<!-- stage: applicability -->
### When The Library Sort Fits

#### Check The Order Contract First

Use `Arrays.sort` on a primitive array when the natural ascending order of the values is the order that the decision needs, and the caller allows a change or a copy. The invariant is that after the call every adjacent pair is nondecreasing and equal values form one run. A problem that says only "return the answer" gives no right to reorder its input, so the safe default is a copy.

#### Where A Primitive Sort Falls Short

A false friend is the idea that the same call can order by any rule. The call `Arrays.sort(int[])` accepts no comparator, so descending order or a custom rule does not fit on `int[]`. Reversing the sorted array afterward costs O(n) and works for descending order, but a rule that depends on several fields needs objects, which later lessons cover. Another false friend is a sort of values that the problem wants in arrival order, such as a time series.

#### Java Details That Cause Failures

The method `Arrays.sort(int[])` returns `void`, so code such as `return Arrays.sort(a)` does not compile. Code that stores the result of `Arrays.copyOf` in a new variable and sorts the original array still changes the caller's data, so check which variable the call receives. Calculations on sorted values, such as a gap between neighbors, can overflow `int` when the values span the full range, so use `long` for the difference.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort A Primitive Copy (Author exercise)
<!-- id: so-sorted-copy -->

**Prerequisites.** The sorted copy and the library call from this lesson.

**Problem.** Let `nums` be an array of integers. Return a new array that holds the values of `nums` in ascending order. The array `nums` must keep its original contents and order.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`; the empty array is legal.
- **Values** are 32-bit integers.
- **Mutation** of `nums` is not allowed.
- **Answer** is a new `int[]`, and it is not the same object as `nums`.

**Example 1.** Input `nums = [9, 2, 7, 2]`, output `[2, 2, 7, 9]`, and `nums` is still `[9, 2, 7, 2]`.

**Example 2.** Input `nums = []`, output `[]`.

**Hint.** Which call makes an independent array, and which array does the sort receive?

**Changed decision.** Basic case: the method owns the sorted order, and the caller keeps the arrival order.

#### [Vary] Sort A Subrange (Author exercise)
<!-- id: so-sort-subrange -->

**Prerequisites.** Sort A Primitive Copy above.

**Problem.** Let `nums` be an array and let `from` and `to` be integers. Sort the positions `from` up to but not including `to` into ascending order, in place. Leave every other position unchanged.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Bounds** satisfy `0 <= from <= to <= nums.length`.
- **Empty range** occurs when `from == to` and changes nothing.
- **Invalid bounds** may be passed, and the method reports them with the exception that the Java library throws.

**Example 1.** Input `nums = [8, 6, 4, 2, 0]`, `from = 1`, `to = 4`, output `[8, 2, 4, 6, 0]`.

**Example 2.** Input `nums = [5, 1]`, `from = 2`, `to = 1`, output: the method throws `IllegalArgumentException`.

**Hint.** Is the index `to` part of the range, and which library overload takes two bounds?

**Changed decision.** The sort covers a range, so the end index is excluded and positions outside stay fixed.

#### [Boundary] Empty, Singleton, And Extreme Values (Author exercise)
<!-- id: so-sorted-gap -->

**Prerequisites.** The two exercises above.

**Problem.** Take an integer array `nums`. Sort a copy of `nums`. Return the largest difference between two adjacent values of the sorted copy as a `long`. Return 0 when the array has fewer than two values.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Difference** is exact and can reach `2^32 - 1`.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [3, 9, 4]`, output 5, because the sorted values `3, 4, 9` have gaps 1 and 5.

**Example 2.** Input `nums = [-2147483648, 2147483647]`, output 4294967295.

**Hint.** Which type must hold the subtraction of two neighbors, and where must the cast happen?

**Changed decision.** The adjacent difference of extreme values leaves the `int` range, so the arithmetic moves to `long`.

#### [Recognize] Smallest Repeated Value (LeetCode 217)
<!-- id: so-smallest-repeat -->

**Prerequisites.** All three exercises above.

**Problem.** Consider an integer array `nums`. Return the smallest value that occurs at least twice in `nums`, or `null` when all values are distinct. This version changes the contract of the original Contains Duplicate problem, which returns only true or false.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers, and negative values are legal.
- **Mutation** of `nums` is not allowed.
- **Answer** is an `Integer` or `null`.

**Example 1.** Input `nums = [7, 3, 7, 3, 9]`, output 3.

**Example 2.** Input `nums = [4, -4, 0]`, output `null`.

**Hint.** After sorting, where does the first pair of equal neighbors sit relative to the smallest repeated value?

**Changed decision.** The answer depends on the sorted order, because the first equal pair of the sorted copy is the smallest repeated value.
