<!-- lesson-kind: standard -->
<!-- lesson-id: sort-then-scan -->
## Scan The Sorted Array

<!-- stage: context -->
### A Scoreboard That Repeats One Score

A game site shows the third-highest score on its front page. The first version sorts the scores and reads the third value from the end. On most days it works. On a day when two players tie for first place, the page shows the second-highest score as if it were the third. On a day with only two scores, the page crashes.

Sorting arranged the scores, and the code still answered the wrong question. The third position in an array and the third distinct score are different things. This lesson answers one question. After a sort, which small piece of state must a scan carry so that the answer counts the right thing and survives short inputs?

<!-- stage: naive -->
### Reading The Third Position From The End

The direct method sorts a copy of the scores in ascending order and returns the element that sits third from the end.

```java
static int thirdHighest(int[] scores) {
    int[] sorted = Arrays.copyOf(scores, scores.length);
    Arrays.sort(sorted);
    return sorted[sorted.length - 3];
}
```

On `[2, 9, 4, 7]` the sorted copy is `[2, 4, 7, 9]`, and the method returns 4, the third-highest score. The method looks correct on data without ties and with at least three scores.

<!-- stage: bottleneck -->
### Positions Count Copies, Not Scores

```predict
The scores are `[2, 9, 9, 4, 7]`. What does the method return, what should the third-highest distinct score be, and what happens for the input `[8, 8]`?

The sorted copy is `[2, 4, 7, 9, 9]`, and the method returns 7. The distinct scores in descending order are 9, 7 and 4, so the answer should be 4. For `[8, 8]` the index `2 - 3` is negative, and the method throws `ArrayIndexOutOfBoundsException`.
```

The sort costs O(n log n) and orders the scores, which is only the first half of the work. The question asks for the third distinct value, and an index counts positions, so every repeated score shifts the answer. The method has no place to record how many different values it has passed. It also has no rule for inputs with fewer than three distinct scores. The decision that the sort enables is local: two neighbors are equal or different, and a counter of different neighbors answers the question.

<!-- stage: insight -->
### Count Changes Between Neighbors

After the sort, equal scores are adjacent, so a scan can find each new distinct score by comparing two neighbors.

#### Compare Each Value With Its Neighbor

An **adjacent comparison** tests whether `sorted[i]` equals the value next to it in the scan direction. A change between neighbors marks the start of a new distinct value. The scan reads each pair once, so it costs O(n) after the sort.

#### Count Distinct Values From The Top

The **distinct rank** of a value is its position in the list of distinct values, with the largest value at rank 1. The scan starts at the last index with rank 1. It moves left one index at a time and adds 1 to the rank whenever the value differs from its right neighbor. The scan returns the value at the moment the rank equals 3. The invariant after reading index `i` is that the rank equals the number of distinct values in `sorted[i..n - 1]`.

#### Decide The Fallback First

A **fallback** is the answer that the problem names when the scan ends before the rank reaches 3. Here the fallback is the largest value, which sits at rank 1. The scan ends without reaching rank 3 exactly when the array has fewer than three distinct values. Writing the fallback in the problem statement and in the code removes the crash.

<!-- names: adjacent comparison, distinct rank, fallback -->

#### What The Scan Costs

Sorting takes O(n log n) time. The scan then reads each neighbor pair once, which adds at most O(n). The method keeps the rank and one index, so the scan needs O(1) space beyond the sorted copy.

<!-- stage: variables -->
### Index, Rank And Previous Value

The scan keeps these values.

- **i** is the index being read, and it moves from the last position toward 0.
- **rank** is the number of distinct values from `i` to the end of the sorted array.
- **sorted** is the sorted copy, which the scan never changes.

The rank only increases, and it increases only when the value at `i` differs from the value at `i + 1`.

<!-- stage: trace -->
### Two Scoreboards Under The Scan

#### Scores With A Tie

Take `[2, 9, 9, 4, 7]`, which sorts to `[2, 4, 7, 9, 9]`. The scan starts at index 4 with the value 9 and rank 1. At index 3 the value is again 9, so the rank stays at 1. At index 2 the value 7 differs from 9, so the rank becomes 2. At index 1 the value 4 differs from 7, so the rank becomes 3, and the scan returns 4.

#### Scores With Fewer Than Three Values

Now take `[8, 8]`. The scan starts at index 1 with rank 1. At index 0 the value equals its neighbor, so the rank stays at 1. The loop ends before the rank reaches 3, so the method returns the fallback, which is the largest value 8.

#### Stepping Through Both Scoreboards

```trace
{"cells":[2,4,7,9,9],"pointers":["i"],"steps":[{"at":{"i":4},"vars":{"value":9,"rank":1},"note":"Start at the last index. The value 9 is the largest, so the rank is 1."},{"at":{"i":3},"vars":{"value":9,"rank":1},"note":"The value 9 equals its right neighbor, so the rank stays 1."},{"at":{"i":2},"vars":{"value":7,"rank":2},"note":"The value 7 differs from its right neighbor 9, so the rank becomes 2."},{"at":{"i":1},"vars":{"value":4,"rank":3},"note":"The value 4 differs from its right neighbor 7, so the rank becomes 3. The rank is 3, so the scan returns this value."}]}
```

```trace
{"cells":[8,8],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"value":8,"rank":1},"note":"Start at the last index. The value 8 is the largest, so the rank is 1."},{"at":{"i":0},"vars":{"value":8,"rank":1},"note":"The value 8 equals its right neighbor, so the rank stays 1."},{"at":{"i":-1},"vars":{"rank":1},"note":"The loop ends with rank 1, below 3, so the method returns the fallback, the largest value 8."}]}
```

<!-- stage: code -->
### One Backward Scan

#### Third Highest With A Fallback

```java
static int thirdHighest(int[] scores) {
    int[] sorted = Arrays.copyOf(scores, scores.length);
    Arrays.sort(sorted);
    int rank = 1;
    for (int i = sorted.length - 2; i >= 0; i--) {
        if (sorted[i] != sorted[i + 1]) {
            rank++;
            if (rank == 3) {
                return sorted[i];
            }
        }
    }
    return sorted[sorted.length - 1];
}
```

#### What The Method Costs

The sort takes O(n log n) time, and the loop makes at most n - 1 steps. The copy takes O(n) space. The method assumes at least one score, because the fallback reads the last index.

<!-- stage: applicability -->
### When A Scan Finishes The Job

#### Look For An Answer Between Neighbors

Use sort and scan when, in sorted order, the answer depends on whether neighbors are equal, adjacent, or differ by a known amount. The invariant is that a small piece of state, such as a rank or a previous value, summarizes everything the scan has read. Write the fallback for short or degenerate inputs before writing the loop.

#### Where Sorted Input Is Not Enough

A false friend is binary search, which also needs sorted input. Binary search needs a yes-or-no question whose answers change only once along the array, and sorted order alone does not give that. Another false friend is a problem whose answer does not depend on neighbors, such as the sum of all values, where a sort adds cost and no help. When the answer needs only the largest or smallest few values, a single pass without a sort already works in O(n).

#### Java Details That Cause Failures

Do not start a scan from `Integer.MIN_VALUE` as an "empty" marker, because the input can contain that value. Keep a count or a boolean instead, or read the first element and start from it. An index such as `length - 3` throws when the array is short, so guard it or use the rank as in the code above. Declare accumulators as `long` when the scan adds values.

<!-- stage: exercises -->
### Exercises

#### [Build] Third Maximum Number (LeetCode 414)
<!-- id: so-third-maximum -->

**Prerequisites.** The adjacent comparison and the fallback from this lesson.

**Problem.** Let `nums` be a nonempty array of integers. Return the third largest distinct value. When `nums` has fewer than three distinct values, return the largest value.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 10^4`.
- **Values** are 32-bit integers, including `Integer.MIN_VALUE`.
- **Distinct** means different as numbers, so equal values count once.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [10, -3, 10, 7, 7, 1]`, output 1.

**Example 2.** Input `nums = [1, 2, -2147483648]`, output -2147483648.

**Hint.** What does the scan return when the rank reaches 3, and what must it return when the loop ends first?

**Changed decision.** Basic case: a rank counter replaces the position count, and a fallback replaces the crash.

#### [Vary] Relative Ranks (LeetCode 506)
<!-- id: so-relative-ranks -->

**Prerequisites.** Third Maximum Number above, and the sort of indexes from the lesson on stability.

**Problem.** Let `scores` be an array of distinct non-negative integers. Return an array `ranks` of strings with `ranks[i]` for `scores[i]`. The highest score gets `"Gold Medal"`, the second highest gets `"Silver Medal"`, and the third highest gets `"Bronze Medal"`. Every other score gets its position in descending order as a decimal string, starting from `"4"`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= scores.length <= 10^4`.
- **Scores** satisfy `0 <= scores[i] <= 10^6` and are pairwise distinct.
- **Answer** keeps the original positions of the scores.
- **Mutation** of `scores` is not allowed.

**Example 1.** Input `scores = [40, 90, 10, 75]`, output `["Bronze Medal", "Gold Medal", "4", "Silver Medal"]`.

**Example 2.** Input `scores = [7]`, output `["Gold Medal"]`.

**Hint.** If the program sorts indexes and not scores, how does it write each answer back to the right position?

**Changed decision.** The scan walks the sorted order, but the answer goes to the original positions.

#### [Boundary] Fewer Than k Distinct Values (Author exercise)
<!-- id: so-kth-distinct -->

**Prerequisites.** The two exercises above.

**Problem.** Let `nums` be a nonempty array of integers and let `k` be a positive integer. Return the `k`-th smallest distinct value of `nums`. When `nums` has fewer than `k` distinct values, return the largest value of `nums`.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **k** satisfies `1 <= k <= 10^9`.
- **Values** are 32-bit integers, and values may repeat.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [5, 1, 5, 3]`, `k = 2`, output 3.

**Example 2.** Input `nums = [4, 4]`, `k = 3`, output 4.

**Hint.** What does the loop do when `k` is larger than the number of distinct values, and where does the fallback sit in the sorted array?

**Changed decision.** The rank target is an input, so the scan can end before it reaches the target and must return the stated fallback.

#### [Recognize] Missing Number (LeetCode 268)
<!-- id: so-missing-number -->

**Prerequisites.** All three exercises above.

**Problem.** Let `nums` be an array of `n` distinct integers from the range 0 to `n` inclusive. Exactly one value of that range is absent. Return the absent value.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^4`.
- **Values** are distinct and satisfy `0 <= nums[i] <= nums.length`.
- **Absent value** is unique, and the empty array returns 0.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [5, 2, 0, 1, 4]`, output 3.

**Example 2.** Input `nums = [0, 1, 2]`, output 3.

**Hint.** In the sorted array, what value should sit at each index, and what is the answer if every index matches?

**Changed decision.** The adjacent relation is the gap between an index and its value, and the fallback is `n`.
