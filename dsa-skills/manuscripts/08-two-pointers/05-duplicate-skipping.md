<!-- lesson-kind: standard -->
<!-- lesson-id: duplicate-skipping -->
## Skip Repeated Values

<!-- stage: context -->
### The Same Coupon Pair Listed Three Times

A store app lists every pair of coupons whose values add up to the price of a bundle. The coupon values come from a sorted list with many repeats, because several coupons share a value. The screen shows the pair worth 2 and 4 three times in a row, once for each coupon of value 2. The customer sees noise, and the app wastes time producing it.

The program found the same combination of values several times through different indexes. The question is how a scan can report each combination once without remembering what it has already reported.

<!-- stage: naive -->
### Collecting Pairs And Removing Repeats Afterward

The direct method keeps every pair that matches and stores it in a set, so the set drops repeats. A set of lists gives each combination once.

```java
static List<List<Integer>> pairsSlow(int[] nums, int target) {
    Set<List<Integer>> seen = new LinkedHashSet<>();
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] == target) seen.add(List.of(nums[i], nums[j]));
        }
    }
    return new ArrayList<>(seen);
}
```

For `[1, 1, 2, 3, 3, 4, 5]` and target 6, the method returns `[1, 5]`, `[2, 4]` and `[3, 3]`. The method is correct, and the set does the deduplication.

```predict
The input holds 100,000 copies of the value 2 and the target is 4. How many pair sums does `pairsSlow` compute, and how many pairs does the answer hold?

It computes about 5 billion pair sums, and every one of them adds the same pair `[2, 2]` to the set. The answer holds one pair. The time is O(n^2) and the set adds memory that grows with the number of distinct pairs.
```

<!-- stage: bottleneck -->
### Equal Values Repeat Whole Searches

Each copy of a value starts its own search, and each search finds the same partners. In the worst case the method evaluates O(n^2) pairs to report a handful of combinations. The set removes the repeats only after the work is done, so it saves no time.

A sorted array puts equal values next to each other. After one representative of a value has been fully processed, every other copy of that value would repeat the same search. A scan that jumps over those copies avoids the repeated work and needs no set.

<!-- stage: insight -->
### Process One Representative, Then Jump

#### Runs Of Equal Values

In a sorted array each value forms a **run**, a block of adjacent indexes that hold the same value. The scan treats one run as one choice. The first index of a run is its **representative**. The scan fully processes the representative and then **skips** the rest of the run, which means it moves the index past all later copies.

<!-- names: run, representative, skips -->

#### The Skip Comes After The Work

For the pair scan, a match at `left` and `right` is recorded first. Only after the recording does the scan advance `left` past every index with the same value as the recorded `nums[left]`, and move `right` back past every index with the same value as the recorded `nums[right]`. The skip happens after the first pair is evaluated. A skip before the evaluation can discard a valid answer, because the representative itself would be gone.

#### One Policy At Every Depth

When the scan fixes a first value and runs a pair scan on the rest, the fixed value needs the same policy. The loop that fixes a value tests whether it equals the previous fixed value. If it does, the scan skips it, because the previous run was fully processed. The policy applies at each fixed position and at the final pair scan, and the two-pointer scan keeps its O(n) cost per pass.

<!-- stage: variables -->
### Names In The Duplicate Rule

The pair scan with skipping keeps four pieces of state, and three of them change.

- **nums** is the sorted array, and the scan never changes it after the sort.
- **left** is the index of the representative on the low side, and it moves forward.
- **right** is the index of the representative on the high side, and it moves backward.
- **result** is the output list, and it receives each combination once.

After a recorded pair, the scan moves `left` and `right` past the whole runs of the recorded values. It does not compare against the next value alone.

<!-- stage: trace -->
### Two Scans With Skipping

#### Distinct Pairs From A Sorted Array

The input is `[1, 1, 2, 3, 3, 4, 5]` and the target is 6. The first sum is 6, so the scan records `[1, 5]` and jumps over the second 1. The next sum is 2 + 4, which also equals 6, so the scan records `[2, 4]`. The last match is `[3, 3]`, after which the pointers meet and the scan stops.

```trace
{"cells":[1,1,2,3,3,4,5],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":6},"vars":{"sum":"6","pairs":"[[1, 5]]"},"note":"The sum 6 equals 6, so the pair [1, 5] is recorded. Then left skips the run of 1 and right skips the run of 5."},{"at":{"left":2,"right":5},"vars":{"sum":"6","pairs":"[[1, 5], [2, 4]]"},"note":"The sum 6 equals 6, so the pair [2, 4] is recorded. Then left skips the run of 2 and right skips the run of 4."},{"at":{"left":3,"right":4},"vars":{"sum":"6","pairs":"[[1, 5], [2, 4], [3, 3]]"},"note":"The sum 6 equals 6, so the pair [3, 3] is recorded. Then left skips the run of 3 and right skips the run of 3."}]}
```

#### Triplets With A Fixed First Value

The input is `[-2, -1, 0, 0, 1, 1, 2, 2]` and the target is 0. The loop fixes each first value once and runs a pair scan on the indexes after it. The trace follows the pair scan for the first value, -2, and shows two skips.

```trace
{"cells":[-2,-1,0,0,1,1,2,2],"pointers":["left","right"],"steps":[{"at":{"left":1,"right":7},"vars":{"sum":"1","fixed":"-2","found":"[]"},"note":"The sum 1 is below 2, so left moves right."},{"at":{"left":2,"right":7},"vars":{"sum":"2","fixed":"-2","found":"[[-2, 0, 2]]"},"note":"With the fixed value -2, the sum 2 matches the pair target 2, so the triplet [-2, 0, 2] is recorded. Both pointers skip their runs."},{"at":{"left":4,"right":5},"vars":{"sum":"2","fixed":"-2","found":"[[-2, 0, 2], [-2, 1, 1]]"},"note":"With the fixed value -2, the sum 2 matches the pair target 2, so the triplet [-2, 1, 1] is recorded. Both pointers skip their runs."}]}
```

<!-- stage: code -->
### Distinct Pairs In Java

```java
static List<int[]> distinctPairs(int[] sorted, long target) {
    List<int[]> out = new ArrayList<>();
    int left = 0, right = sorted.length - 1;
    while (left < right) {
        long sum = (long) sorted[left] + sorted[right];
        if (sum < target) left++;
        else if (sum > target) right--;
        else {
            out.add(new int[] {sorted[left], sorted[right]});
            int a = sorted[left], b = sorted[right];
            while (left < right && sorted[left] == a) left++;
            while (left < right && sorted[right] == b) right--;
        }
    }
    return out;
}
```

The two inner loops run after the pair is recorded. The condition `left < right` stops them from crossing. For the input `[2, 2]` with target 4, the pair is recorded once, and then `left` moves to 1 and the loop ends. An input with no match records nothing, and an input of one value returns an empty list.

<!-- stage: applicability -->
### When Skipping Fits

#### The Invariant

The invariant is that every pair of values that sums to the target has been recorded once or lies in the indexes from `left` to `right`. A recorded pair removes the full runs of both values from the range, so no copy of that combination can be found again. The invariant holds at the start, because nothing is recorded and the range is the whole array.

#### The False Friend

The nearest wrong idea is to skip before the first evaluation, for example by moving `left` while `sorted[left] == sorted[left + 1]` at the top of each iteration. On `[2, 2]` with target 4, that skip moves `left` past the first 2 and then fails to find any pair. The answer pair is lost. The skip must follow the recording of the representative.

#### Conditions That Break The Fit

The method needs a sorted array, because equal values must be adjacent. On an unsorted array a run can split into several blocks, and the skip would miss copies. The method also reports value combinations, so a contract that asks for index combinations needs every copy.

<!-- stage: exercises -->
### Exercises

#### [Build] Unique Pairs (Author exercise)
<!-- id: tp-unique-pairs -->

**Prerequisites.** The pair scan with skipping from this lesson.

**Problem.** Take a nondecreasing integer array `nums` and an integer `target`. Return every pair `[a, b]` with `a <= b` that has a distinct value combination and a sum equal to `target`. A pair `[a, b]` is valid when the array holds an index pair `i < j` with `nums[i] = a` and `nums[j] = b`. List the pairs in increasing order of `a`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`; the empty array is valid.
- **Values** are `int` values, sorted in nondecreasing order.
- **Target** is a `long`.
- **Result** holds each value combination once.

**Example 1.** Input `nums = [1,1,2,3,3,4,5]` and `target = 6`, output `[[1,5],[2,4],[3,3]]`.

**Example 2.** Input `nums = [2,2,2]` and `target = 4`, output `[[2,2]]`.

**Hint.** After you record a pair, which two indexes must move past their whole runs?

**Changed decision.** Basic case: the scan skips whole runs after recording a pair, so each combination appears once.

#### [Vary] 3Sum (LeetCode 15)
<!-- id: tp-three-sum-unique -->

**Prerequisites.** The first exercise above.

**Problem.** Given an integer array `nums` that is not sorted, return all triplets `[a, b, c]` with `a <= b <= c` and `a + b + c = 0`, where each distinct value combination appears once. List the triplets in increasing lexicographic order. The input array must not change.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 3000`.
- **Values** are `int` values with `|nums[i]| <= 10^5`.
- **Mutation** of the input does not occur, so the method sorts a copy.
- **Result** holds each distinct triplet once.

**Example 1.** Input `nums = [2,-2,0,1,0,2,-1,1]`, output `[[-2,0,2],[-2,1,1],[-1,0,1]]`.

**Example 2.** Input `nums = [3,3,3]`, output `[]`.

**Hint.** Skip a fixed first value that equals the previous fixed value, and skip repeated values inside the pair scan only after you record a triplet.

**Changed decision.** The duplicate policy now covers two places: the fixed first value and the pair scan.

#### [Boundary] All Equal (Author exercise)
<!-- id: tp-all-equal -->

**Prerequisites.** The false friend of this lesson.

**Problem.** Given an integer array `nums`, return the number of distinct value triplets `a <= b <= c` with `a + b + c = 0`. The input may hold many equal values.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 3000`; the empty array is valid.
- **Values** are `int` values with `|nums[i]| <= 10^5`.
- **Mutation** of the input does not occur.
- **Return type** is `int`.

**Example 1.** Input `nums = [0,0,0,0]`, output 1.

**Example 2.** Input `nums = [0,0]`, output 0.

**Hint.** With four equal zeros, which fixed value is the representative, and which skip must not run before it is evaluated?

**Changed decision.** A single run supplies all three values, so the pair scan must still find the triplet after the fixed value.

#### [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-unique -->

**Prerequisites.** All exercises above.

**Problem.** Given an integer array `nums` and a `long` target, return all distinct value quadruples `[a, b, c, d]` with `a <= b <= c <= d` and `a + b + c + d = target`. List them in increasing lexicographic order. The input must not change.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 200`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Target** is a `long` with `|target| <= 4 * 10^9`.
- **Sums** can exceed the `int` range, so the method adds in `long`.

**Example 1.** Input `nums = [2,2,2,3,5,5,1,0]` and `target = 10`, output `[[0,2,3,5],[1,2,2,5]]`.

**Example 2.** Input `nums = [1000000000,1000000000,1000000000,1000000000]` and `target = 4000000000`, output `[[1000000000,1000000000,1000000000,1000000000]]`.

**Hint.** The duplicate policy applies at each fixed position and at the final pair scan. How many fixed positions does this problem have?

**Changed decision.** A second fixed position adds one more skip rule, and the pair scan stays unchanged.
