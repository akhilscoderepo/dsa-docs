<!-- lesson-kind: standard -->
<!-- lesson-id: lower-and-upper-bounds -->
## Find Where A Value Belongs

<!-- stage: context -->
### Inserting Into A Sorted List

A leaderboard keeps scores in ascending order. When a player finishes, the program must insert the new score at the position that keeps the list sorted. Players with a tied score expect to rank after the players who reached it first. A version that searches for the exact score fails twice. It returns `-1` for every new score. For a tie, it returns an arbitrary position among equal scores.

The program needs a position and not a yes-or-no answer, and the target need not occur in the list. This lesson answers one question. How does a search return the place where a value belongs, whether or not the list already holds it?

<!-- stage: naive -->
### Scanning For The Insertion Place

The direct method scans from the left and returns the first index whose value is not smaller than the target. If every value is smaller, the place is the end of the array.

```java
static int firstNotSmaller(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] >= target) return i;
    }
    return nums.length;
}
```

On `[1, 3, 5, 5, 8]` with target 5, the method returns 2. With target 9 it returns 5, the length of the array. For target 0 it returns 0.

```predict
The array holds 1,000,000 ascending values and the target is larger than all of them. What does `firstNotSmaller` return, and how many comparisons does it make?

It returns 1,000,000, the array length, after 1,000,000 comparisons. The loop must read every value to learn that none is large enough, which is O(n).
```

<!-- stage: bottleneck -->
### A Position Question Needs Fewer Reads

The scan makes up to `n` comparisons, which is O(n), and each one rules out a single index. The question has the same structure as before. The array is sorted, so the answer position splits it into two parts. The left part holds only values smaller than the target. The right part holds no smaller value.

A comparison at a middle index tells which part that index belongs to. If its value is smaller than the target, the whole left side up to it belongs to the left part. Otherwise it belongs to the right part, and so does everything after it. The scan reads values one at a time and never uses this split.

<!-- stage: insight -->
### Search For The Edge Of A Part

The **lower bound** of a target is the first index whose value is at least the target. The **upper bound** is the first index whose value is greater than the target. Both equal the array length when no such index exists. Inserting at the lower bound puts a new value before its equals, and inserting at the upper bound puts it after them.

<!-- names: lower bound, upper bound, half-open interval -->

#### The Half-Open Interval

Both searches use a **half-open interval** `[lo, hi)`. The index `lo` is included and the index `hi` is excluded. The interval starts as `lo = 0` and `hi = nums.length`, so the answer `nums.length` is already a legal outcome. The loop runs while `lo < hi`, and the interval is empty when `lo == hi`.

#### The Lower Bound Rule

At `mid`, test whether `nums[mid] < target`. If it holds, `mid` and every index before it belong to the left part, so `lo = mid + 1`. If it fails, `mid` could be the answer, so the rule keeps it with `hi = mid`. The bound `hi` never moves past an index that might be the answer. Because `mid < hi`, the interval still shrinks after `hi = mid`.

#### The Upper Bound Rule

The upper bound changes one comparison. The test becomes `nums[mid] <= target`. A value equal to the target now belongs to the left part, so equal entries are skipped. Every other line stays the same. The count of entries equal to a target is then `upper - lower`. The count inside a closed value range `[a, b]` is `upper(b) - lower(a)`.

<!-- stage: variables -->
### What The Interval Guarantees

Three names describe the state, and one fact holds at every step.

- **lo** is the smallest index that can still be the answer, and everything before it is on the left part.
- **hi** is an index that may be the answer, and every index from `hi` on is on the right part or equals the array length.
- **mid** is `lo + (hi - lo) / 2` and always satisfies `lo <= mid < hi`.

The loop ends with `lo == hi`, and that single index is the answer. No separate result variable is needed, because the answer is the final value of `lo`.

<!-- stage: trace -->
### One Lower Bound And One Upper Bound

#### Lower Bound Of 5

The array is `[1, 3, 5, 5, 8]` and the target is 5. The interval starts as `[0, 5)`. The first midpoint is index 2 with value 5, which is not smaller than 5, so `hi` becomes 2. The next midpoint is index 1 with value 3, which is smaller, so `lo` becomes 2. The interval is empty at `lo == hi == 2`, and the lower bound is 2.

```trace
{"cells":[1,3,5,5,8],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"target":"5","interval":"[0, 5)"},"note":"The half-open interval covers indexes 0 to 4 and also allows the answer 5."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"nums[mid]":"5","interval":"[0, 2)"},"note":"The test nums[mid] < 5 fails for 5, so index 2 may be the answer. hi becomes 2."},{"at":{"lo":0,"hi":2,"mid":1},"vars":{"nums[mid]":"3","interval":"[2, 2)"},"note":"The test nums[mid] < 5 holds for 3, so index 1 is on the left part. lo becomes 2."},{"at":{"lo":2,"hi":2,"mid":-1},"vars":{"interval":"[2, 2)"},"note":"The interval is empty, so the answer is index 2."}]}
```

#### Upper Bound Of 4

The array is `[2, 4, 4, 4, 9, 9]` and the target is 4. The first midpoint is index 3 with value 4. The test `<= 4` holds, so `lo` becomes 4. The midpoint at index 5 holds 9, so `hi` becomes 5. The midpoint at index 4 holds 9, so `hi` becomes 4. The interval is empty at 4, which is the index after the last 4.

```trace
{"cells":[2,4,4,4,9,9],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":-1},"vars":{"target":"4","interval":"[0, 6)"},"note":"The half-open interval covers indexes 0 to 5 and also allows the answer 6."},{"at":{"lo":0,"hi":6,"mid":3},"vars":{"nums[mid]":"4","interval":"[4, 6)"},"note":"The test nums[mid] <= 4 holds for 4, so index 3 is on the left part. lo becomes 4."},{"at":{"lo":4,"hi":6,"mid":5},"vars":{"nums[mid]":"9","interval":"[4, 5)"},"note":"The test nums[mid] <= 4 fails for 9, so index 5 may be the answer. hi becomes 5."},{"at":{"lo":4,"hi":5,"mid":4},"vars":{"nums[mid]":"9","interval":"[4, 4)"},"note":"The test nums[mid] <= 4 fails for 9, so index 4 may be the answer. hi becomes 4."},{"at":{"lo":4,"hi":4,"mid":-1},"vars":{"interval":"[4, 4)"},"note":"The interval is empty, so the answer is index 4."}]}
```

<!-- stage: code -->
### Two Searches With One Changed Test

```java
static int lowerBound(int[] nums, int target) {
    int lo = 0, hi = nums.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static int upperBound(int[] nums, int target) {
    int lo = 0, hi = nums.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

The results lie in `0` to `nums.length`, and both methods return 0 for an empty array. A target below every value gives 0, and a target above every value gives `nums.length`. The closed-interval style of the earlier lessons cannot use `hi = mid`, because the loop then never ends. The half-open form and its loop test `lo < hi` belong together.

<!-- stage: applicability -->
### When The Edge Is The Answer

#### The Invariant

The invariant is that every index below `lo` fails the keep test and every index from `hi` on passes it. Initially both sets are empty. Each step moves one bound across `mid` after the test classifies it, so the invariant holds. When the interval is empty, `lo` is the first index that passes.

#### The False Friend

Exact search is the false friend. It may stop on equality, and the position it returns among equal entries is arbitrary. Bounds must not stop. A match at `mid` tells nothing about the edge, so the search keeps `hi = mid` and continues. Code that returns `mid` on equality gives an answer that is wrong whenever equal entries repeat.

#### Reading Bounds In Practice

Search Insert Position, counts of a value, and ranges of values all read bounds. Some problems add a rule at the end of the array, such as a wraparound to the first entry when no larger entry exists. The check `lo == nums.length` is the place for such a rule. The library method `Arrays.binarySearch` does not return a bound for duplicates, so code that needs a bound writes this loop.

<!-- stage: exercises -->
### Exercises

#### [Build] Search Insert Position (LeetCode 35)
<!-- id: bs-insert-35 -->

**Prerequisites.** The half-open interval and the lower bound rule of this lesson.

**Problem.** Given an array `nums` of distinct integers in ascending order and an integer `target`, return the index of `target` when it occurs. Otherwise return the index where `target` would be inserted to keep the array sorted.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`; the empty array is valid.
- **Values** are distinct `int` values in ascending order.
- **Target** is any `int`.
- **Answer** lies in `0` to `nums.length`.

**Example 1.** Input `nums = [2,4,7,10]` and `target = 7`, output 2.

**Example 2.** Input `nums = [2,4,7,10]` and `target = 5`, output 2.

**Hint.** Which index is the first one whose value is not smaller than the target? Return that index.

**Changed decision.** The search returns a position for a missing target and does not stop on equality.

#### [Vary] Upper Bound (Author exercise)
<!-- id: bs-upper-bound -->

**Prerequisites.** The first exercise above.

**Problem.** Given an array `nums` sorted in non-decreasing order and an integer `target`, return the first index whose value is strictly greater than `target`. Return `nums.length` when no such index exists.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values in non-decreasing order, with duplicates.
- **Target** is any `int`.
- **Answer** lies in `0` to `nums.length`.

**Example 1.** Input `nums = [2,4,4,4,9,9]` and `target = 4`, output 4.

**Example 2.** Input `nums = [1,2,3]` and `target = 3`, output 3.

**Hint.** Which comparison puts an entry equal to the target on the left part?

**Changed decision.** One comparison changes from `<` to `<=`, and equal entries move to the left part.

#### [Boundary] Outside Range (Author exercise)
<!-- id: bs-outside-range -->

**Prerequisites.** Both exercises above.

**Problem.** Given an array `nums` sorted in non-decreasing order and an integer `target`, return the pair `[lower, upper]` of the lower bound and the upper bound of `target`. The pair must be correct for targets below every value and above every value.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values in non-decreasing order.
- **Target** is any `int`, including values outside the range of `nums`.
- **Answer** satisfies `0 <= lower <= upper <= nums.length`.

**Example 1.** Input `nums = [2,4,4,7]` and `target = 1`, output `[0,0]`.

**Example 2.** Input `nums = [2,4,4,7]` and `target = 9`, output `[4,4]`.

**Hint.** What does each search return when the keep test passes at index 0, and what when it fails at every index?

**Changed decision.** The outputs sit at the ends of the legal range, so the sentinel `nums.length` must be reachable.

#### [Recognize] Smallest Letter Greater Than Target (LeetCode 744)
<!-- id: bs-next-letter-744 -->

**Prerequisites.** All exercises above.

**Problem.** Given an array `letters` of lowercase letters sorted in non-decreasing order and a letter `target`, return the smallest letter in `letters` that is strictly greater than `target`. If no such letter exists, return the first letter of `letters`.

**Constraints.** The limits are:
- **Length** is `1 <= letters.length <= 10^4`.
- **Values** are lowercase letters in non-decreasing order, and `letters` has at least two distinct letters.
- **Target** is a lowercase letter.
- **Answer** is one letter taken from `letters`.

**Example 1.** Input `letters = [d,f,f,k]` and `target = f`, output `k`.

**Example 2.** Input `letters = [d,f,f,k]` and `target = k`, output `d`.

**Hint.** Compute the upper bound of the target. What index must the answer use when the bound equals the array length?

**Changed decision.** The upper bound answers the question, and a wraparound rule handles the index `letters.length`.
