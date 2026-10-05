<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-counts -->
## Count Subarrays With A Target Sum

<!-- stage: context -->
### Counting Windows That Hit A Quota

A traffic log records the number of requests in each minute of a day. An operations team has a quota of exactly `k` requests. They want to know in how many stretches of consecutive minutes the total equals the quota, because each such stretch is a window where the limiter should have acted.

A day has 1,440 minutes, and the log of a year has half a million. The previous lessons answer one window in constant time, and this question asks about every window. The remaining problem is to count the windows with a given total without looking at every pair of ends.

<!-- stage: naive -->
### Trying Every Start And Every End

A **subarray** is a run of consecutive values, so it is fixed by a start index and an end index. The direct method fixes each start and extends the end one value at a time while it keeps a running sum.

```java
static int countWithSum(int[] nums, int k) {
    int count = 0;
    for (int start = 0; start < nums.length; start++) {
        long sum = 0;
        for (int end = start; end < nums.length; end++) {
            sum += nums[end];
            if (sum == k) count++;
        }
    }
    return count;
}
```

For `[1, 2, 3]` and `k = 3`, the method counts the subarray `[1, 2]` and the subarray `[3]`, so it returns 2.

```predict
The array holds 20,000 values. How many (start, end) pairs does `countWithSum` check?

It checks 20,000 * 20,001 / 2 = 200,010,000 pairs. The number of pairs grows with the square of the length, so the method is O(n^2), even though the running sum makes each check constant.
```

<!-- stage: bottleneck -->
### The Method Visits Every Pair

The running sum removes the cost of adding values, and the loops still visit every pair of ends. The number of pairs is `n * (n + 1) / 2`, which is O(n^2). For 500,000 minutes that is about 1.25 * 10^11 pairs.

Most pairs are not answers, and the method cannot skip them. It has no way to ask, for a fixed end, how many starts give the total `k`. That question depends only on prefix sums. The sum of a subarray equals the difference of two prefix entries, and a program can count matching entries when it sees them.

<!-- stage: insight -->
### Count Earlier Totals That Match

A **boundary** is a position between two values or at either end of the array. The boundaries are numbered 0 to `n`, and boundary `b` has the prefix entry `prefix[b]`. A subarray from boundary `a` to boundary `b` contains the values `nums[a]` through `nums[b - 1]`. Its sum is `prefix[b] - prefix[a]`.

#### Turning The Target Into A Lookup

The sum equals `k` exactly when `prefix[a] = prefix[b] - k`. For the boundary `b`, the answer is the number of earlier boundaries `a < b` whose prefix entry equals `prefix[b] - k`. The program keeps a **frequency map**, which is a hash map from a value to the number of times that value occurred so far. Each prefix entry is a key, and its count is the number of earlier boundaries that have it.

#### The Order Of Lookup And Record

At each position the program reads `cur - k` from the map first, and then it adds `cur` to the map. The order matters. A lookup after the record would match the boundary with itself when `k` is 0, and it would count an empty subarray.

The map starts with one entry, the key 0 with count 1. This **seed** stands for boundary 0, whose prefix is the empty sum. Without it, a subarray that starts at index 0 has no earlier boundary to match, and the program misses it.

<!-- names: frequency map, boundary, seed -->

#### The Cost Of One Pass

The loop runs once per value, and each step makes one lookup and one update in a hash map. The expected time is O(n), and the map holds at most n + 1 keys, so the space is O(n). The running prefix needs a `long` when values are large, and the count needs a `long` when n is large.

<!-- stage: variables -->
### Five Names And Their Roles

The one-pass loop keeps five values.

- **cur** is the prefix sum through the current value and has type `long`.
- **seen** is the frequency map from a prefix value to the count of earlier boundaries with that value.
- **k** is the target sum and never changes.
- **count** is the number of matching subarrays found so far.
- **i** is the index of the value that the loop adds next.

At the start of step `i`, `seen` holds the prefix entries of boundaries 0 through `i`. The lookup reads it before `cur` is stored.

<!-- stage: trace -->
### Two Counts Step By Step

#### An Array With A Mixed Target

The input is `[3, 4, 7, 2, -3, 1, 4, 2]` and `k = 7`. Each step prints the current prefix, the key that is looked up, and the map. The count grows when the looked-up key is present. The method finds 4 subarrays: `[3, 4]`, `[7]`, `[7, 2, -3, 1]` and `[1, 4, 2]`.

```trace
{"cells":[3,4,7,2,-3,1,4,2],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"seen":"{0=1}","count":"0"},"note":"The map starts with the seed: prefix 0 occurs once, for boundary 0."},{"at":{"i":0},"vars":{"cur":"3","look up":"-4","seen":"{0=1, 3=1}","count":"0"},"note":"Prefix is 3. The key -4 occurs 0 times before, so the count becomes 0. Then the map records 3."},{"at":{"i":1},"vars":{"cur":"7","look up":"0","seen":"{0=1, 3=1, 7=1}","count":"1"},"note":"Prefix is 7. The key 0 occurs 1 time before, so the count becomes 1. Then the map records 7."},{"at":{"i":2},"vars":{"cur":"14","look up":"7","seen":"{0=1, 3=1, 7=1, 14=1}","count":"2"},"note":"Prefix is 14. The key 7 occurs 1 time before, so the count becomes 2. Then the map records 14."},{"at":{"i":3},"vars":{"cur":"16","look up":"9","seen":"{0=1, 3=1, 7=1, 14=1, 16=1}","count":"2"},"note":"Prefix is 16. The key 9 occurs 0 times before, so the count becomes 2. Then the map records 16."},{"at":{"i":4},"vars":{"cur":"13","look up":"6","seen":"{0=1, 3=1, 7=1, 14=1, 16=1, 13=1}","count":"2"},"note":"Prefix is 13. The key 6 occurs 0 times before, so the count becomes 2. Then the map records 13."},{"at":{"i":5},"vars":{"cur":"14","look up":"7","seen":"{0=1, 3=1, 7=1, 14=2, 16=1, 13=1}","count":"3"},"note":"Prefix is 14. The key 7 occurs 1 time before, so the count becomes 3. Then the map records 14."},{"at":{"i":6},"vars":{"cur":"18","look up":"11","seen":"{0=1, 3=1, 7=1, 14=2, 16=1, 13=1, 18=1}","count":"3"},"note":"Prefix is 18. The key 11 occurs 0 times before, so the count becomes 3. Then the map records 18."},{"at":{"i":7},"vars":{"cur":"20","look up":"13","seen":"{0=1, 3=1, 7=1, 14=2, 16=1, 13=1, 18=1, 20=1}","count":"4"},"note":"Prefix is 20. The key 13 occurs 1 time before, so the count becomes 4. Then the map records 20."}]}
```

#### An Array Of Zeros With Target Zero

The input is `[0, 0, 0]` and `k = 0`. Every prefix is 0, so every step looks up the key 0 and finds all earlier boundaries. The counts are 1, 2 and 3, and the total is 6. A set of seen values would report 1 at each step and miss the multiplicity.

```trace
{"cells":[0,0,0],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"seen":"{0=1}","count":"0"},"note":"The map starts with the seed: prefix 0 occurs once, for boundary 0."},{"at":{"i":0},"vars":{"cur":"0","look up":"0","seen":"{0=2}","count":"1"},"note":"Prefix is 0. The key 0 occurs 1 time before, so the count becomes 1. Then the map records 0."},{"at":{"i":1},"vars":{"cur":"0","look up":"0","seen":"{0=3}","count":"3"},"note":"Prefix is 0. The key 0 occurs 2 times before, so the count becomes 3. Then the map records 0."},{"at":{"i":2},"vars":{"cur":"0","look up":"0","seen":"{0=4}","count":"6"},"note":"Prefix is 0. The key 0 occurs 3 times before, so the count becomes 6. Then the map records 0."}]}
```

<!-- stage: code -->
### The One Pass In Java

```java
static long countWithSum(int[] nums, long k) {
    java.util.HashMap<Long, Integer> seen = new java.util.HashMap<>();
    seen.put(0L, 1);
    long cur = 0;
    long count = 0;
    for (int v : nums) {
        cur += v;
        count += seen.getOrDefault(cur - k, 0);
        seen.merge(cur, 1, Integer::sum);
    }
    return count;
}
```

The keys have type `Long`, because a prefix can exceed the `int` range, and a `Long` key compares by value. The call `getOrDefault` returns 0 for a missing key, so no branch is needed. The method `merge` adds 1 to an existing count or stores 1 for a new key. The lookup runs before the merge, which keeps the empty subarray out of the count.

<!-- stage: applicability -->
### When Counts Replace Pair Checks

#### The Invariant

The invariant is that on arrival at boundary `b`, the map holds the frequency of each of `prefix[0]` through `prefix[b - 1]`. The lookup then counts exactly the earlier boundaries with `prefix[a] = prefix[b] - k`. Each valid pair `(a, b)` is counted once, at its later boundary.

#### The False Friend

A set is the false friend. It answers whether some earlier boundary matches, and it hides how many. Repeated prefixes mean several valid starts for one end, so a set undercounts. The map keeps the multiplicity that the answer needs.

#### Conditions That Break The Fit

The relation must be a difference of two stored values, so a target on a product or a maximum does not reduce to a lookup. The values may be negative, and this method still works. A window method that moves two ends depends on non-negative values and fails on negatives. The method needs extra space proportional to the number of distinct prefixes.

<!-- stage: exercises -->
### Exercises

#### [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: ps-subarray-sum-560 -->

**Prerequisites.** The frequency map and the seed of this lesson.

**Problem.** Given an integer array `nums` and an integer `k`, return the number of non-empty contiguous subarrays whose sum equals `k`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 2 * 10^4`.
- **Values** are `int` values with `-1000 <= nums[i] <= 1000`.
- **Target** satisfies `-10^7 <= k <= 10^7`.
- **Order** matters; the subarrays are contiguous and keep the input order.

**Example 1.** Input `nums = [3,4,7,2,-3,1,4,2]` and `k = 7`, output 4.

**Example 2.** Input `nums = [1,2,3]` and `k = 3`, output 2.

**Hint.** For the current prefix `cur`, which earlier prefix value gives a subarray of sum `k`? Read the map before you store `cur`.

**Changed decision.** Basic case: the answer counts earlier boundaries, so the program stores frequencies and not positions.

#### [Vary] Binary Subarrays With Sum (LeetCode 930)
<!-- id: ps-binary-subarrays-930 -->

**Prerequisites.** The first exercise above.

**Problem.** Given a binary array `nums`, where every value is 0 or 1, and an integer `goal`, return the number of non-empty contiguous subarrays whose sum equals `goal`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 3 * 10^4`.
- **Values** are 0 or 1.
- **Goal** satisfies `0 <= goal <= nums.length`.
- **Zeros** create many equal prefix values.

**Example 1.** Input `nums = [0,1,1,0,1]` and `goal = 2`, output 5.

**Example 2.** Input `nums = [0,0,1,0,0]` and `goal = 1`, output 9.

**Hint.** Equal prefixes appear after each run of zeros. How many earlier boundaries share the key `cur - goal`?

**Changed decision.** The value domain shrinks to 0 and 1, so the prefix values form a non-decreasing sequence with long runs of repeats.

#### [Boundary] Zero Target (Author exercise)
<!-- id: ps-zero-target -->

**Prerequisites.** The first exercise and the second trace of this lesson.

**Problem.** Given an integer array `nums`, return the number of non-empty contiguous subarrays whose sum is 0. The count can exceed the `int` range, so the return type is `long`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Return type** is `long`.
- **Empty subarray** is not counted.

**Example 1.** Input `nums = [1,-1,1,-1]`, output 4.

**Example 2.** Input `nums = [2,3]`, output 0.

**Hint.** A zero sum means two equal prefix values. If a prefix value occurred `m` times before, how many subarrays end at the current boundary?

**Changed decision.** The target is 0, so the lookup key equals the current prefix, and the order of lookup and record decides whether the empty subarray is counted.

#### [Recognize] Count Number Of Nice Subarrays (LeetCode 1248)
<!-- id: ps-nice-subarrays-1248 -->

**Prerequisites.** All exercises above. A value `v` is odd when `v % 2 != 0`.

**Problem.** Given an integer array `nums` with non-negative values and an integer `k`, return the number of contiguous subarrays that contain exactly `k` odd values.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 5 * 10^4`.
- **Values** are `int` values with `1 <= nums[i] <= 10^5`.
- **Target** satisfies `1 <= k <= nums.length`.
- **Return type** is `long`.

**Example 1.** Input `nums = [2,1,2,2,1,2,1]` and `k = 2`, output 7.

**Example 2.** Input `nums = [1,3,5]` and `k = 2`, output 2.

**Hint.** Replace each value by 1 when it is odd and by 0 otherwise. What does the sum of a subarray of the new values count?

**Changed decision.** The array is not a sum yet. A conversion step maps each value to 0 or 1, and then the previous exercise applies.
