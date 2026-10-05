<!-- lesson-kind: combination -->
<!-- lesson-id: sums-in-sorted-arrays -->
## Find Sums In Sorted Arrays

<!-- stage: context -->
### Highlighting The Rows That Match

A ledger screen lists payments in the order they arrived, and the user can ask for two payments that add up to an amount. The screen must highlight the two matching rows. A developer sorts the payments and runs the pair scan, which is fast. The screen then highlights rows 0 and 2, while the matching payments sit in rows 3 and 0 of the table.

The sorted list has the right values at the wrong positions. The scan is correct and the answer is still wrong, because sorting threw away the row numbers. The problem is to keep the speed of the scan and still report the original rows.

<!-- stage: contributions -->
### What Sorting And The Scan Each Add

Sorting puts the values in nondecreasing order. That order gives a relation between the sum of two indexes and the sums of their neighbors, and the relation is what makes elimination safe. Sorting costs O(n log n) comparisons, and it moves every value to a new index. Sorting does not say which pair to test next, and it does not remember where a value came from.

The opposite-end scan supplies the choice of the next pair. It tests one pair of sorted indexes and discards one index, so a pass costs O(n). The scan reports indexes of the array that it reads, so on a sorted copy it reports sorted indexes. Only the combination answers the user's question. Sorting creates the order, the scan uses the order, and an extra piece of state carries the original row through the sort.

<!-- stage: naive -->
### Testing Every Pair Of Rows

The direct method tests every pair of rows in the original order, so the row numbers are correct by construction.

```java
static int[] pairRowsSlow(int[] nums, long target) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if ((long) nums[i] + nums[j] == target) return new int[] {i, j};
        }
    }
    return new int[] {-1, -1};
}
```

For `[8, 3, 12, 5]` and target 13 the method returns rows 0 and 3, which hold 8 and 5. The method needs no sorting, and it costs a double loop.

```predict
The ledger holds 100,000 payments and no pair matches. How many pair sums does `pairRowsSlow` compute, and how many comparisons does a sort of the same 100,000 payments make?

The method computes about 5 billion pair sums. A comparison sort makes about 100,000 * 17, or 1.7 million comparisons. Sorting first and then scanning once costs far less than the double loop.
```

<!-- stage: bottleneck -->
### The Fast Method Loses The Row Numbers

The double loop costs O(n^2) because it tests pairs one by one. The sorted scan costs O(n log n) in total, but its answer names positions in the sorted copy. Mapping those positions back to rows by searching the original array for the two values takes another O(n) step, and it fails when two rows hold the same value. For `[3, 3]` the search for the value 3 finds row 0 twice.

The sort has to carry each row number along with its value. Then the scan can read the row number straight from the sorted copy at the moment of the match.

<!-- stage: insight -->
### Sort The Values Together With Their Rows

#### One Number For Value And Row

A **packed key** is a single `long` that holds the value in its high 32 bits and the row number in its low 32 bits. The expression `((long) value << 32) | row` builds it. Sorting an array of packed keys orders the entries by value first and by row second, because the value occupies the high bits. The row number is never negative, so it never changes the sign of the key. The value comes back with `(int) (key >> 32)` and the row with `(int) key`.

#### The Scan Reads The Row From The Sorted Copy

The **sorted copy** is the array of packed keys after sorting. The pair scan from the first lesson runs on the decoded values of the sorted copy. When the sum matches, the two packed keys name the **original position** of each value, and the method returns those rows in increasing order. The scan never needs the original array again.

<!-- names: packed key, sorted copy, original position -->

#### Fixing More Values

For three values the method fixes one packed key and scans the rest of the sorted copy for a pair. A four-value search fixes two keys. The total cost is O(n log n) for the sort, plus O(n) for one scan, O(n^2) with one fixed key and O(n^3) with two fixed keys. Each added fixed key multiplies the scan cost by `n`, as in the reduction lesson.

<!-- stage: variables -->
### What The Sorted Copy Holds

The method keeps these pieces of state.

- **keys** is the `long[]` of packed keys, sorted, and it replaces the input after the first step.
- **left** and **right** are the scan indexes into `keys`, and they move as in the first lesson.
- **value** at an index is `(int) (keys[index] >> 32)`, and the row is `(int) keys[index]`.
- **nums** is the input array, and the method never changes it.

All sums use `long`, because two decoded values can add to more than the `int` range.

<!-- stage: trace -->
### Two Searches That Report Original Rows

#### Two Rows From An Unsorted Table

The input is `[8, 3, 12, 5]` and the target is 13. After sorting, the values are `3, 5, 8, 12` and their rows are `1, 3, 0, 2`. The first sum is 15, which is above the target, so the right pointer moves. The scan then reads the sum of the decoded values at each step and, at the match, reports the rows of the two keys.

```trace
{"cells":[3,5,8,12],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":3},"vars":{"sum":"15","rows":"1 and 2"},"note":"The sum 15 is above 13, so right moves left."},{"at":{"left":0,"right":2},"vars":{"sum":"11","rows":"1 and 0"},"note":"The sum 11 is below 13, so left moves right."},{"at":{"left":1,"right":2},"vars":{"sum":"13","rows":"3 and 0"},"note":"The sum 13 equals 13. The keys hold the original rows 3 and 0, so the answer is [0, 3]."}]}
```

#### Three Rows With One Fixed Value

The input is `[9, 2, -5, 3, 1]` and the target is 0. The sorted values are `-5, 1, 2, 3, 9` with rows `2, 4, 1, 3, 0`. The scan fixes the first sorted value and searches the later indexes for a pair that reaches the remaining target.

```trace
{"cells":[-5,1,2,3,9],"pointers":["i","left","right"],"steps":[{"at":{"i":0,"left":1,"right":4},"vars":{"remaining":"5","sum":"10"},"note":"The pair sum 10 is above the remaining target 5, so right moves left."},{"at":{"i":0,"left":1,"right":3},"vars":{"remaining":"5","sum":"4"},"note":"The pair sum 4 is below the remaining target 5, so left moves right."},{"at":{"i":0,"left":2,"right":3},"vars":{"remaining":"5","sum":"5"},"note":"The pair sum 5 equals the remaining target 5. The three keys hold the original rows [1, 2, 3]."}]}
```

<!-- stage: code -->
### Two Rows With Their Positions In Java

```java
static int[] pairRows(int[] nums, long target) {
    long[] keys = new long[nums.length];
    for (int i = 0; i < nums.length; i++) keys[i] = ((long) nums[i] << 32) | i;
    Arrays.sort(keys);
    int left = 0, right = keys.length - 1;
    while (left < right) {
        long sum = (long) (int) (keys[left] >> 32) + (int) (keys[right] >> 32);
        if (sum == target) {
            int a = (int) keys[left], b = (int) keys[right];
            return new int[] {Math.min(a, b), Math.max(a, b)};
        }
        if (sum < target) left++;
        else right--;
    }
    return new int[] {-1, -1};
}
```

The sort uses `Arrays.sort(long[])`, which needs no comparator and no boxing. The cast `(int) keys[left]` keeps only the low 32 bits, which hold the row. An empty array and one row skip the loop and return `{-1, -1}`. The method never writes to `nums`.

<!-- stage: applicability -->
### When Sorting Plus The Scan Fits

#### The Invariant

The invariant is that every pair of rows that sums to the target has both packed keys inside the range from `left` to `right` of the sorted copy. The sort establishes the order that the elimination needs, and each pointer move removes a key that no matching pair can use. The row travels inside the key, so the final answer needs no lookup.

#### The False Friend

The nearest wrong idea is to scan the unsorted array with two pointers. On `[12, 3, 5, 8]` with target 13 the scan adds `12 + 8`, `12 + 5` and `12 + 3`, finds every sum too large, and reports no pair, although `5 + 8` matches. Another false friend is to sort the values alone and report sorted positions. The sums are right and the rows are wrong.

#### Conditions That Break The Fit

The method pays O(n log n) for the sort, so a single query on a small array may be cheaper with the double loop. A hash map can answer the pair question in O(n) expected time when the table is queried once and without ordering. The sorted copy pays off when the same sorted order serves several targets or several fixed values, as in the three-value and four-value problems.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Sum II With Original Positions (LeetCode 167)
<!-- id: tp-sorted-rows-pair -->

**Prerequisites.** The packed key of this lesson and the first lesson of the chapter.

**Problem.** Take an unsorted integer array `nums` and a `long` target. Return `{i, j}` with `i < j` and `nums[i] + nums[j] = target`, where `i` and `j` are positions in the original array. When no pair matches, return `{-1, -1}`. This exercise adapts the sorted-array problem of the first lesson to an unsorted array, so the positions must survive the sort.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`; the empty array is valid.
- **Values** are `int` values over the full `int` range.
- **Target** is a `long`.
- **Mutation** of the input does not occur, and any matching pair is accepted.

**Example 1.** Input `nums = [8,3,12,5]` and `target = 13`, output `{0,3}`.

**Example 2.** Input `nums = [3,3]` and `target = 6`, output `{0,1}`.

**Hint.** Pack each value with its position before the sort. How do you read the position at the match?

**Changed decision.** Basic case: the sort must carry the position, because the scan alone reports sorted positions.

#### [Vary] 3Sum With Original Positions (LeetCode 15)
<!-- id: tp-sorted-rows-triple -->

**Prerequisites.** The first exercise above and the reduction lesson of this chapter.

**Problem.** Search an unsorted integer array `nums` for three values. Return `{i, j, k}` with `i < j < k` and `nums[i] + nums[j] + nums[k] = target`, using positions of the original array. Return an empty array when no triple matches. Any matching triple is accepted. The original three-sum problem lists distinct value triplets, and this version reports one triple of positions.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 3000`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Target** is a `long`.
- **Mutation** of the input does not occur.

**Example 1.** Input `nums = [9,2,-5,3,1]` and `target = 0`, output `{1,2,3}`.

**Example 2.** Input `nums = [4,1,5]` and `target = 20`, output `{}`.

**Hint.** Fix one packed key and scan the keys after it for a pair that reaches the remaining target.

**Changed decision.** The answer is a set of positions, so the scan stops at the first match and sorts the three positions.

#### [Boundary] 3Sum Closest With Original Positions (LeetCode 16)
<!-- id: tp-sorted-rows-closest -->

**Prerequisites.** The second exercise above.

**Problem.** Take an integer array `nums` with at least three values, and a `long` target. Return `{i, j, k}` with `i < j < k`, using positions of the original array, so that the sum of the three values is closest to `target`. When two sums are equally close, prefer the smaller sum. Any triple that reaches the best sum is accepted. The original closest-sum problem returns the sum, and this version returns positions.

**Constraints.** The limits are:
- **Length** is `3 <= nums.length <= 1000`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Target** is a `long`.
- **Mutation** of the input does not occur.

**Example 1.** Input `nums = [10,2,7,4,15]` and `target = 20`, output `{0,1,2}`, whose sum 19 is closest.

**Example 2.** Input `nums = [1,1,1,1]` and `target = 5`, output any triple, for example `{0,1,2}`.

**Hint.** No exact match is guaranteed. Which packed keys do you save when a sum is the closest so far?

**Changed decision.** The scan keeps the three keys of the best candidate instead of stopping at an exact match.

#### [Recognize] 4Sum Not Above A Target (LeetCode 18)
<!-- id: tp-sorted-rows-four -->

**Prerequisites.** All exercises above.

**Problem.** Take an integer array `nums` of positive values and a `long` target. Among all choices of four different indexes, return the largest sum that does not exceed `target`. Return `-1` when every four-value sum exceeds `target`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 200`; an array shorter than four gives `-1`.
- **Values** are `int` values from 1 to `10^9`.
- **Target** is a `long` up to `4 * 10^9`.
- **Return type** is `long`.

**Example 1.** Input `nums = [7,3,2,9,4]` and `target = 20`, output 18.

**Example 2.** Input `nums = [5,5,5,5]` and `target = 19`, output `-1`.

**Hint.** Fix two values, then scan a pair. When a pair sum fits under the remaining target, which pointer should move to look for a larger sum?

**Changed decision.** The goal is a one-sided bound, so a sum that fits is a candidate and the scan keeps looking for a larger one.
