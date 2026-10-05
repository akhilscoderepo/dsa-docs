<!-- lesson-kind: standard -->
<!-- lesson-id: opposite-ends -->
## Scan From Both Ends

<!-- stage: context -->
### A Gift Card Spent Exactly

A shop app keeps its prices in a sorted list. A customer holds a gift card and wants two items whose prices add up to the card balance exactly. The first version of the feature checks every pair of items. With 200 items nobody notices. With 100,000 items the screen freezes, because the list holds five billion pairs.

The list is sorted, so the order should save work. The question is how a program can use the order of the prices to rule out many pairs with one comparison.

<!-- stage: naive -->
### Checking Every Pair Of Prices

The direct method tries each first index `i` and each later index `j`. It adds the two prices and returns the pair when the sum equals the target.

```java
static int[] findPairSlow(int[] nums, long target) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if ((long) nums[i] + nums[j] == target) return new int[] {i, j};
        }
    }
    return new int[] {-1, -1};
}
```

For `[1, 3, 4, 6, 8, 11]` and target 10, the method tests `1 + 3`, `1 + 4`, and so on, until it reaches `4 + 6`. It ignores the order of the list. A sorted list and a shuffled list cost the same.

```predict
The list holds 100,000 prices and no pair matches the target. How many pair sums does `findPairSlow` compute?

It computes every pair once, which is 100,000 * 99,999 / 2, or about 5 billion sums. The count grows with the square of the length, so the method is O(n^2) in time and O(1) in extra space.
```

<!-- stage: bottleneck -->
### One Sum Rules Out No Pairs

Each pair sum is computed alone. The result of one test never changes the next test. When `1 + 3` is too small, the method still tests `1 + 4`, `1 + 6`, `1 + 8` and `1 + 11` in order. That is the repeated work. The method learns nothing about the pairs it has not tested yet, so it needs O(n^2) sums in the worst case.

The sorted order carries information that the loops ignore. If the first price plus the largest price is already too small, then the first price plus any smaller price is also too small. One test can therefore decide the fate of many pairs at once.

<!-- stage: insight -->
### Each Comparison Removes One Index

#### Two Pointers At The Ends

An **interval** is the range of indexes from `left` to `right` that can still belong to an answer. The **left pointer** `left` starts at index 0, and the **right pointer** `right` starts at index `n - 1`. Every pair of indexes inside the interval is still a candidate. Together the two pointers form a **two pointers** scan, one that moves each pointer in one direction until they meet.

#### The Elimination Argument

Let `s` be `nums[left] + nums[right]`. Suppose `s` is smaller than the target. Every pair that uses index `left` with some index `j` at or before `right` has a sum of at most `s`, because the list is sorted. Each of those sums is smaller than the target, so index `left` belongs to no answer inside the interval. The scan moves `left` one step to the right. This move is an **elimination**, which means that it discards a whole group of pairs with one comparison.

Suppose `s` is larger than the target. Every pair that uses `right` with some index at or after `left` has a sum of at least `s`, and that sum is too large. The scan moves `right` one step to the left. If `s` equals the target, the scan returns the pair.

#### Why The Scan Is Linear

Each step moves one pointer by one position, and the pointers never move back. The interval holds at most `n` indexes, so the loop runs at most `n - 1` times. The method costs O(n) time and O(1) extra space.

<!-- names: interval, left pointer, right pointer, two pointers, elimination -->

<!-- stage: variables -->
### Three Names Define The Scan

The scan keeps three pieces of state, and two of them change.

- **left** is the smallest index that can still belong to an answer, and it only increases.
- **right** is the largest index that can still belong to an answer, and it only decreases.
- **sum** is `nums[left] + nums[right]`, stored in a `long` so that two large `int` values cannot wrap.

The loop condition is `left < right`, because an answer needs two different indexes. When the loop ends without a match, the interval holds fewer than two indexes, so no pair is left.

<!-- stage: trace -->
### Two Scans On Different Inputs

#### Finding A Pair That Sums To Ten

The input is `[1, 3, 4, 6, 8, 11]` and the target is 10. The first sum is 12, which is too large, so `right` moves left. The next sum is 9, which is too small, so `left` moves right. The scan alternates in this way until `4 + 6` matches at indexes 2 and 3.

```trace
{"cells":[1,3,4,6,8,11],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":5},"vars":{"sum":"12"},"note":"The sum 12 is above 10, so index 5 cannot help and right moves left."},{"at":{"left":0,"right":4},"vars":{"sum":"9"},"note":"The sum 9 is below 10, so index 0 cannot help and left moves right."},{"at":{"left":1,"right":4},"vars":{"sum":"11"},"note":"The sum 11 is above 10, so index 4 cannot help and right moves left."},{"at":{"left":1,"right":3},"vars":{"sum":"9"},"note":"The sum 9 is below 10, so index 1 cannot help and left moves right."},{"at":{"left":2,"right":3},"vars":{"sum":"10"},"note":"The sum 10 equals the target 10, so the pair at indexes 2 and 3 is the answer."}]}
```

#### Choosing The Shorter Wall

The input is a list of wall heights `[4, 2, 5, 3, 6, 1]`. The area of a pair is the smaller height times the distance between the indexes. After each area, the scan moves the pointer at the shorter wall, because a wider pair with the same shorter wall cannot be taller than that wall.

```trace
{"cells":[4,2,5,3,6,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":5},"vars":{"area":"5","best":"5"},"note":"The area is min(4, 1) * 5 = 5. The wall at index 5 is shorter, so right moves left."},{"at":{"left":0,"right":4},"vars":{"area":"16","best":"16"},"note":"The area is min(4, 6) * 4 = 16. The wall at index 0 is not taller, so left moves right."},{"at":{"left":1,"right":4},"vars":{"area":"6","best":"16"},"note":"The area is min(2, 6) * 3 = 6. The wall at index 1 is not taller, so left moves right."},{"at":{"left":2,"right":4},"vars":{"area":"10","best":"16"},"note":"The area is min(5, 6) * 2 = 10. The wall at index 2 is not taller, so left moves right."},{"at":{"left":3,"right":4},"vars":{"area":"3","best":"16"},"note":"The area is min(3, 6) * 1 = 3. The wall at index 3 is not taller, so left moves right."}]}
```

<!-- stage: code -->
### The Scan In Java

```java
static int[] findPair(int[] nums, long target) {
    int left = 0;
    int right = nums.length - 1;
    while (left < right) {
        long sum = (long) nums[left] + nums[right];
        if (sum == target) return new int[] {left, right};
        if (sum < target) left++;
        else right--;
    }
    return new int[] {-1, -1};
}
```

The cast `(long) nums[left]` widens before the addition, so the sum of two values near 2 * 10^9 stays exact. An empty array and a one-element array give `right <= left`, so the loop body never runs and the method returns `{-1, -1}`. The method reads the array and never writes to it.

<!-- stage: applicability -->
### When The Scan Fits

#### The Invariant

The invariant is that every pair with a sum equal to the target has both indexes in the closed range from `left` to `right`. It holds at the start, because the range is the whole array. Each move discards one index that no matching pair can use, so the invariant still holds after the move. When the loop ends, the range holds fewer than two indexes, and no pair is left.

#### The False Friend

The nearest wrong idea is to run the same scan on an unsorted array. The moves rest on the claim that a smaller left value gives smaller sums, and that claim fails without order. On `[5, 1, 4, 2]` with target 6, the scan adds `5 + 2 = 7`, moves `right`, and then adds `5 + 4 = 9`. It never reaches the pair `(1, 5)`. A sort first costs O(n log n) and moves the indexes, which matters when the answer must name original positions.

#### Conditions That Break The Fit

The elimination needs a monotone relation: a pointer move must change the quantity in one known direction. Order gives that for sums. For a quantity that is not monotone in the pointers, such as a sum of three values with both ends free, one pointer pair is not enough.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Sum II, Input Array Is Sorted (LeetCode 167)
<!-- id: tp-two-sum-sorted -->

**Prerequisites.** The scan of this lesson.

**Problem.** Take an integer array `numbers` in nondecreasing order and an integer `target`. Return the 1-based indexes `[i, j]` with `i < j` and `numbers[i] + numbers[j] == target`. The input has exactly one such pair.

**Constraints.** The limits are:
- **Length** is `2 <= numbers.length <= 3 * 10^4`.
- **Values** are `int` values from `-1000` to `1000`, sorted in nondecreasing order.
- **Pair** is unique, and the two indexes differ.
- **Mutation** does not occur, and the extra space is O(1).

**Example 1.** Input `numbers = [2,5,9,12,20]` and `target = 21`, output `[3,4]`.

**Example 2.** Input `numbers = [-4,-1,0,3]` and `target = -4`, output `[1,3]`.

**Hint.** If the current sum is below the target, which index can no longer help?

**Changed decision.** Basic case: the scan stops at the first match, and the answer uses 1-based indexes.

#### [Vary] Closest Pair Sum (Author exercise)
<!-- id: tp-closest-pair-sum -->

**Prerequisites.** The first exercise above.

**Problem.** Take an integer array `nums` in nondecreasing order and an integer `target`. Return the sum of the pair `i < j` whose sum has the smallest absolute difference from `target`. Break a tie between two equally close sums by returning the smaller one.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 10^5`.
- **Values** are `int` values with `|nums[i]| <= 10^9`, sorted in nondecreasing order.
- **Target** is an `int`.
- **Return type** is `long`, because a pair sum can exceed the `int` range.

**Example 1.** Input `nums = [1,4,9,16]` and `target = 12`, output 13.

**Example 2.** Input `nums = [1,5,7]` and `target = 7`, output 6, because the sums 6 and 8 are equally close.

**Hint.** A match no longer ends the scan. Which sum do you save at each step, and which pointer moves after a tie?

**Changed decision.** The scan keeps the best sum seen so far, and it continues after a sum that is not exact.

#### [Boundary] Two Values (Author exercise)
<!-- id: tp-two-values -->

**Prerequisites.** The first exercise and the false friend of this lesson.

**Problem.** Take a sorted integer array `nums` and a `target`. Return `true` when two different indexes hold values that sum to `target`. Two indexes may hold equal values, and a single value never pairs with itself.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`; the empty array is valid.
- **Values** are `int` values, sorted in nondecreasing order.
- **Target** is a `long`.
- **Mutation** does not occur.

**Example 1.** Input `nums = [3,3]` and `target = 6`, output `true`.

**Example 2.** Input `nums = [3,5,8]` and `target = 6`, output `false`.

**Hint.** Why does the loop condition `left < right` make `[3]` with target 6 return `false`?

**Changed decision.** The scan must stop when the pointers meet, so a value is never paired with itself.

#### [Recognize] Container With Most Water (LeetCode 11)
<!-- id: tp-container-water -->

**Prerequisites.** The second trace of this lesson.

**Problem.** Given an integer array `height` of wall heights, choose two indexes `i < j`. The area of the pair is `min(height[i], height[j]) * (j - i)`. Return the largest area over all pairs.

**Constraints.** The limits are:
- **Length** is `2 <= height.length <= 10^5`.
- **Values** are `int` values from 0 to `10^4`; the array is not sorted.
- **Return type** is `long`.
- **Mutation** does not occur.

**Example 1.** Input `height = [3,9,2,8,1]`, output 16.

**Example 2.** Input `height = [5,5]`, output 5.

**Hint.** The array is not sorted. Which quantity is monotone when you move the pointer at the taller wall?

**Changed decision.** The monotone quantity is the area bound by the shorter wall, not the sum of two values.
