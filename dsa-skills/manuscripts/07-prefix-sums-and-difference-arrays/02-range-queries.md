<!-- lesson-kind: standard -->
<!-- lesson-id: range-queries -->
## Answer Range Sum Queries

<!-- stage: context -->
### A Chart That Freezes While You Drag

A monitoring page charts the requests per minute for the last 100,000 minutes, about 70 days. The user drags two handles to choose a window of minutes, and the page shows the total number of requests inside it. Short windows respond at once. A window that covers most of the chart freezes the page, because every drag event adds up tens of thousands of numbers.

The data does not change while the user drags. Only the window changes. This lesson answers one question. How does a program answer a sum over any window of unchanging data in constant time?

<!-- stage: naive -->
### Adding The Window Values Each Time

The direct method answers each query with a loop from `left` to `right`. A query is a pair of indexes, and both ends belong to the window.

```java
static long[] answerEach(int[] nums, int[][] queries) {
    long[] out = new long[queries.length];
    for (int q = 0; q < queries.length; q++) {
        long sum = 0;
        for (int i = queries[q][0]; i <= queries[q][1]; i++) sum += nums[i];
        out[q] = sum;
    }
    return out;
}
```

For `nums = [2, 4, 1, 5, 3, 6]` and the query `[1, 3]`, the loop adds 4, 1 and 5 and returns 10.

```predict
The array holds 100,000 values, and 100,000 queries each ask for the whole array. How many additions does `answerEach` perform?

It performs 100,000 times 100,000 additions, which is 10,000,000,000. Each query costs the window length, so the cost is O(n) per query and O(n * q) for q queries.
```

<!-- stage: bottleneck -->
### Every Query Repeats Earlier Additions

A query over a window of length `w` costs `w` additions, which is O(n) in the worst case. Two queries over overlapping windows add the same values twice. With `q` queries the method costs O(n * q), and both factors reach 10^5 in the example above.

The array never changes between queries. The method pays for the same sums again and again, although the answer to every window depends only on the data. Any work that depends only on the data can run once, before the first query.

<!-- stage: insight -->
### Subtract Two Stored Totals

**Preprocessing** is work that runs once before the first query, so that each query costs less afterwards. Here it builds the prefix array of the previous lesson, with the sentinel `prefix[0] = 0` and `prefix[i + 1] = prefix[i] + nums[i]`.

#### A Window As A Difference

An **inclusive range** `[left, right]` contains both end indexes. The entry `prefix[right + 1]` is the sum of `nums[0]` through `nums[right]`. The entry `prefix[left]` is the sum of `nums[0]` through `nums[left - 1]`. Both sums contain the values before `left`.

**Cancellation** removes that shared part. The subtraction `prefix[right + 1] - prefix[left]` leaves exactly the values from `left` through `right`. The formula is the whole algorithm, and the sentinel makes it hold when `left` is 0.

#### The Cost Of Many Queries

Preprocessing costs O(n) time and O(n) space, once. Each query reads two entries and subtracts, which costs O(1). For `q` queries the total is O(n + q), and the example with 10^5 values and 10^5 queries costs about 2 * 10^5 operations and not 10^10.

<!-- names: inclusive range, preprocessing, cancellation -->

<!-- stage: variables -->
### Five Names And Their Roles

The query code uses five names. Only `left` and `right` change from one query to the next.

- **prefix** is the `long` array of length `n + 1` from the previous lesson, built once and never changed.
- **left** is the first index inside the window.
- **right** is the last index inside the window.
- **right + 1** is the prefix index that includes `nums[right]`.
- **answer** is `prefix[right + 1] - prefix[left]` and has type `long`.

Both reads use valid indexes when `0 <= left <= right < n`. The largest read is `prefix[n]`, and the smallest is `prefix[0]`.

<!-- stage: trace -->
### Two Queries On One Array

#### A Window In The Middle

The array is `[2, 4, 1, 5, 3, 6]` and its prefix array is `[0, 2, 6, 7, 12, 15, 21]`. The query is `[1, 3]`. The pointer `left` marks `prefix[left]`, and the pointer `end` marks `prefix[right + 1]`. The first read gives 12, the second gives 2, and the difference is 10.

```trace
{"cells":[0,2,6,7,12,15,21],"pointers":["left","end"],"steps":[{"at":{"left":-1,"end":-1},"vars":{"query":"[1, 3]"},"note":"The prefix array is ready. The query is [1, 3], so the two reads are prefix[4] and prefix[1]."},{"at":{"left":-1,"end":4},"vars":{"prefix[end]":"12"},"note":"Read prefix[4] = 12, the sum of the first 4 values."},{"at":{"left":1,"end":4},"vars":{"prefix[end]":"12","prefix[left]":"2"},"note":"Read prefix[1] = 2, the sum of the first 1 values."},{"at":{"left":1,"end":4},"vars":{"answer":"12 - 2 = 10"},"note":"The shared first 1 values cancel, so the answer is 10."}]}
```

#### A Window That Starts At Index Zero

The query is `[0, 5]`, the whole array, and its prefix array is the same as before. The pointer `left` is 0, so the second read is the sentinel. The sentinel is 0, so the answer equals `prefix[6]`, which is 21. The query reads no index before the start of the array, and the first read is the last entry of `prefix`.

```trace
{"cells":[0,2,6,7,12,15,21],"pointers":["left","end"],"steps":[{"at":{"left":-1,"end":-1},"vars":{"query":"[0, 5]"},"note":"The prefix array is ready. The query is [0, 5], so the two reads are prefix[6] and prefix[0]."},{"at":{"left":-1,"end":6},"vars":{"prefix[end]":"21"},"note":"Read prefix[6] = 21, the sum of the first 6 values."},{"at":{"left":0,"end":6},"vars":{"prefix[end]":"21","prefix[left]":"0"},"note":"Read prefix[0] = 0, the sum of the first 0 values."},{"at":{"left":0,"end":6},"vars":{"answer":"21 - 0 = 21"},"note":"The shared first 0 values cancel, so the answer is 21."}]}
```

<!-- stage: code -->
### Preprocessing And Queries In Java

```java
static long[] buildPrefix(int[] nums) {
    long[] prefix = new long[nums.length + 1];
    for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
    return prefix;
}

static long rangeSum(long[] prefix, int left, int right) {
    return prefix[right + 1] - prefix[left];
}
```

The first method runs once. The second method runs once per query and does not loop. It never reads `prefix[left - 1]`, so `left = 0` is safe.

The method assumes `0 <= left <= right < n`. A caller with a bad index gets either a wrong sum or an `ArrayIndexOutOfBoundsException`, so a program that takes user input checks the bounds before the call.

<!-- stage: applicability -->
### When Stored Totals Beat Loops

#### The Invariant

The invariant is that for every pair `0 <= a <= b <= n`, `prefix[b] - prefix[a]` equals the sum of `nums[a]` through `nums[b - 1]`. Each entry is a sum of a leading part of the array. The difference of two leading parts is the part between them, and this holds for every pair at once.

#### The False Friend

A sliding window is the false friend. It answers a family of windows that move in one direction, and it keeps one running total while the ends advance. It cannot answer an arbitrary window in constant time, because the window must travel there first. Queries in any order need the stored totals.

#### Conditions That Break The Fit

The array must stay unchanged. One update to `nums[i]` changes every entry after it, so interleaved updates and queries need a tree structure from a later chapter. The method also fits only operations that can be undone. Subtraction undoes addition, so sums work. A maximum has no inverse, so the same formula does not answer a range maximum.

<!-- stage: exercises -->
### Exercises

#### [Build] Range Sum Query Immutable (LeetCode 303)
<!-- id: ps-range-sum-303 -->

**Prerequisites.** The prefix array and the cancellation formula of this lesson.

**Problem.** Given an integer array `nums` and a list of queries `[left, right]`, return for each query the sum of `nums[left]` through `nums[right]`. Every query satisfies `0 <= left <= right < nums.length`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^4`.
- **Values** are `int` values with `|nums[i]| <= 10^5`.
- **Queries** number at most `10^4`.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [-2,0,3,-5,2,-1]` and queries `[[0,2],[2,5],[0,5]]`, output `[1,-1,-3]`.

**Example 2.** Input `nums = [7]` and queries `[[0,0]]`, output `[7]`.

**Hint.** Build one array before the first query. Which two entries bound the window `[left, right]`?

**Changed decision.** Basic case: the cost moves from each query to a single preparation step.

#### [Vary] Half-Open Query (Author exercise)
<!-- id: ps-half-open-query -->

**Prerequisites.** The first exercise above.

**Problem.** Given an integer array `nums` and a list of queries, where each query is a pair `[start, end]` with `0 <= start <= end <= nums.length`, return for each query the sum of `nums[start]` through `nums[end - 1]`. The query leaves out the end index, so a query with `start == end` has sum 0.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^4`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Queries** number at most `10^4`.
- **Return type** is `long[]`.

**Example 1.** Input `nums = [3,1,4,1,5]` and queries `[[1,4],[0,5]]`, output `[6,14]`.

**Example 2.** Input `nums = [3,1,4]` and queries `[[2,2],[3,3]]`, output `[0,0]`.

**Hint.** The sentinel convention already excludes the end index. Which entries do `start` and `end` name directly?

**Changed decision.** The end index excludes its value, so the formula loses its `+ 1`.

#### [Boundary] Whole Array (Author exercise)
<!-- id: ps-whole-array -->

**Prerequisites.** The first exercise and the second trace of this lesson.

**Problem.** Given a non-empty integer array `nums`, return the array `[all, first, last]`. The value `all` is the sum of all values. The value `first` is the sum of the window `[0, 0]`. The value `last` is the sum of the window `[n - 1, n - 1]`. Answer each one with the cancellation formula and no read before index 0.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^4`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Return type** is `long[]` of length 3.
- **Single value** gives three equal answers.

**Example 1.** Input `nums = [4,-2,7]`, output `[9,4,7]`.

**Example 2.** Input `nums = [5]`, output `[5,5,5]`.

**Hint.** A window that starts at 0 subtracts `prefix[0]`. Does that entry exist, and what is its value?

**Changed decision.** The two single-value windows touch both ends, so they test the sentinel and the largest index.

#### [Recognize] XOR Queries Of A Subarray (LeetCode 1310)
<!-- id: ps-xor-queries -->

**Prerequisites.** All exercises above. The operator `^` combines two integers bit by bit, and `x ^ x` equals 0 for every `x`.

**Problem.** Given an integer array `arr` and a list of queries `[left, right]`, return for each query the XOR of `arr[left]` through `arr[right]`. Subtraction cannot undo XOR, but XOR undoes itself, so a stored prefix state answers each query.

**Constraints.** The limits are:
- **Length** is `1 <= arr.length <= 3 * 10^4`.
- **Values** are `int` values with `1 <= arr[i] <= 10^9`.
- **Queries** satisfy `0 <= left <= right < arr.length`.
- **Return type** is `int[]`.

**Example 1.** Input `arr = [1,3,4,8]` and queries `[[0,1],[1,2],[0,3],[3,3]]`, output `[2,7,14,8]`.

**Example 2.** Input `arr = [4,8,2,10]` and queries `[[2,3],[1,3],[0,0],[0,3]]`, output `[8,0,4,4]`.

**Hint.** Replace the addition in the recurrence with `^` and the subtraction in the query with `^`. Why does the shared part vanish?

**Changed decision.** The operation changes while the structure stays: cancellation works because XOR is its own inverse.
