<!-- lesson-kind: standard -->
<!-- lesson-id: increasing-subsequences -->
## Increasing Subsequences

<!-- stage: context -->
### Finding A Rising Trend In Noisy Readings

A monitoring service stores a sensor reading for each minute. The readings for seven minutes are 5, 1, 6, 2, 7, 3 and 8. An engineer wants the longest group of readings that rise from one chosen minute to the next, where the chosen minutes need not touch each other. The readings 1, 2, 3 and 8 form such a group of four, and so do 5, 6, 7 and 8.

A first version scans the data and counts the longest run of neighbouring minutes that rise. On these readings it reports 2, because every rise is cut off by a drop on the next minute. The report misses the trend because the noisy readings in between hide it.

Formally, the input is an `int[] nums`. A subsequence keeps some elements in their original order and may skip any elements between them. It is strictly increasing when each kept element is larger than the one before it. The method returns the length of the longest strictly increasing subsequence. The empty array has length 0, and the method never changes the array.

This lesson asks how to count such a subsequence when the chosen elements are scattered through the array.

<!-- stage: naive -->
### Counting Runs Of Neighbouring Elements

The quick idea scans once and counts how many neighbouring elements in a row increase. It resets the count whenever an element does not exceed the one before it.

```java
static int longestRun(int[] nums) {
    if (nums.length == 0) return 0;
    int best = 1;
    int run = 1;
    for (int i = 1; i < nums.length; i++) {
        run = nums[i] > nums[i - 1] ? run + 1 : 1;
        best = Math.max(best, run);
    }
    return best;
}
```

The method runs in O(n) time and uses O(1) memory. It answers a different question, which is the longest increasing block of adjacent elements. A subsequence may skip elements, so the block answer is never larger than the true answer and is often smaller.

```predict
Run longestRun on 5, 1, 6, 2, 7, 3, 8. What does it return, and what is the true longest strictly increasing subsequence?

It returns 2, because the pairs 1 and 6, 2 and 7, and 3 and 8 are the longest adjacent rises. The true answer is 4, for example 1, 2, 3, 8. The elements 1, 2 and 3 are not adjacent, so the run counter cannot see them.
```

<!-- stage: bottleneck -->
### Too Many Subsequences To List

A correct but slow method lists every subsequence. An array of n elements has 2^n subsequences, and checking one costs O(n), so the work is O(2^n * n). For n = 40 that is more than 4 * 10^13 operations.

A better method uses the structure of the problem. Every increasing subsequence ends at some index, and what comes before that last element is itself an increasing subsequence that ends at a smaller index. This allows a table with one entry per index. Filling the entry for index `i` compares `nums[i]` with every earlier element, so the total work is O(n^2). That is fast enough for n = 2,000, because it needs about four million comparisons.

The quadratic method fails when n reaches 200,000. It needs about 4 * 10^10 comparisons, which takes tens of seconds in Java. The extra cost comes from comparing each new element with all earlier elements, even though most of those comparisons cannot change the answer. The next section builds the table first and then removes the repeated comparisons.

<!-- stage: insight -->
### Keep The Best Ending For Each Length

The goal is to extend a subsequence one element at a time without remembering the subsequence itself. Two summaries are enough, and the second one is a faster version of the first.

<!-- names: smallest tail, lower bound, binary search -->

#### One Length For Every Last Element

Let `dp[i]` be the length of the longest strictly increasing subsequence whose last element is `nums[i]`. Every such subsequence has length 1 when it holds only `nums[i]`. Otherwise its second-to-last element is some `nums[j]` with `j < i` and `nums[j] < nums[i]`, and the part before `nums[i]` is a subsequence that ends at `j`. Therefore `dp[i]` is 1 plus the largest `dp[j]` over all earlier smaller values, or 1 if none exists. The answer is the largest `dp[i]`, because the best subsequence ends at some index.

#### One Smallest Tail For Every Length

The tail of a subsequence is its last element. For each length `L`, keep the **smallest tail** among all increasing subsequences of length `L` that exist in the part of the array read so far. Store these values in an array `tails`, where `tails[L - 1]` belongs to length `L`. A smaller tail is always at least as good, because any later element that can extend a subsequence with a larger tail can also extend one with a smaller tail.

The array `tails` is strictly increasing. If a subsequence of length `L + 1` ends at value `v`, then removing its last element leaves a subsequence of length `L` with a tail below `v`. So the smallest tail for length `L` is below the smallest tail for length `L + 1`.

#### Place Each Value With Binary Search

A new value `x` can extend the longest subsequence only if `x` is larger than every tail. Otherwise it belongs at the first position whose tail is at least `x`. That position is the **lower bound** of `x` in `tails`. Replacing the tail there with `x` keeps the array strictly increasing, and it keeps the smallest tail for that length. Because `tails` is sorted, **binary search** finds the lower bound in O(log n) steps.

Equal values must replace and not extend. If `x` equals a tail, the lower bound points at that tail, and the replacement changes nothing. The length of the answer stays the same, which is correct for a strict comparison.

The array `tails` is not an actual subsequence of the input. It mixes the best tails from different subsequences, and a later tail may come from an earlier position than a smaller one. Only its size is the answer. The invariant is that after each element, `tails[L - 1]` is the smallest possible last element of an increasing subsequence of length `L` in the prefix read so far.

<!-- stage: variables -->
### The Length Table And The Tails Array

The quadratic method keeps these working values, and it leaves the input unchanged.

- **dp** is an `int[]` where `dp[i]` is the longest increasing subsequence that ends at index `i`.
- **i** is the index whose entry the outer loop computes.
- **j** is an earlier index that the inner loop compares with `i`, from 0 up to `i - 1`.
- **best** is the largest entry of `dp` seen so far.

The faster method keeps these values instead.

- **tails** is an `int[]` of capacity `n`, and its first `size` entries are strictly increasing.
- **size** is the number of used entries, which equals the longest length found so far.
- **x** is the element `nums[i]` that the loop places.
- **pos** is the lower bound of `x` among the first `size` entries.

If `pos` equals `size`, the value is larger than every tail, and `size` grows by one. Otherwise the entry at `pos` is overwritten and `size` stays.

<!-- stage: trace -->
### Two Runs Over Small Arrays

#### Quadratic Table On The Opening Readings

The first run fills the length table for the readings 5, 1, 6, 2, 7, 3 and 8. Each cell is one reading. The pointer `i` marks the reading whose entry is being computed, and the pointer `j` marks the earlier reading that it is compared with. The variable `len` is `dp[j]`, and in this trace only, `best` is the current entry for `i`.

Index 2 holds 6 and extends both 5 and 1, so its length is 2. Index 4 holds 7 and extends 6 at length 2, so its length is 3. Index 6 holds 8, which is larger than everything, and it takes the best earlier length 3 plus one. The final length is 4, the same as the subsequence 5, 6, 7, 8 or 1, 2, 3, 8.

```trace
{"cells":[5,1,6,2,7,3,8],"pointers":["i","j"],"steps":[{"at":{"i":-1,"j":-1},"vars":{"best":0,"len":0},"note":"Every index starts with length 1, because the element alone is a subsequence."},{"at":{"i":0,"j":0},"vars":{"best":1,"len":1},"note":"Index 0 is finished with length 1, the longest strictly increasing subsequence that ends at value 5."},{"at":{"i":1,"j":0},"vars":{"best":1,"len":1},"note":"Index 1 holds 1 and index 0 holds 5. The earlier value is not smaller, so it cannot extend and the length stays 1."},{"at":{"i":1,"j":1},"vars":{"best":1,"len":1},"note":"Index 1 is finished with length 1, the longest strictly increasing subsequence that ends at value 1."},{"at":{"i":2,"j":0},"vars":{"best":2,"len":1},"note":"Index 2 holds 6 and index 0 holds 5. The smaller earlier value extends length 1, so the length at index 2 is 2."},{"at":{"i":2,"j":1},"vars":{"best":2,"len":1},"note":"Index 2 holds 6 and index 1 holds 1. The extension gives 2, which does not beat 2, so the length stays 2."},{"at":{"i":2,"j":2},"vars":{"best":2,"len":2},"note":"Index 2 is finished with length 2, the longest strictly increasing subsequence that ends at value 6."},{"at":{"i":3,"j":0},"vars":{"best":1,"len":1},"note":"Index 3 holds 2 and index 0 holds 5. The earlier value is not smaller, so it cannot extend and the length stays 1."},{"at":{"i":3,"j":1},"vars":{"best":2,"len":1},"note":"Index 3 holds 2 and index 1 holds 1. The smaller earlier value extends length 1, so the length at index 3 is 2."},{"at":{"i":3,"j":2},"vars":{"best":2,"len":2},"note":"Index 3 holds 2 and index 2 holds 6. The earlier value is not smaller, so it cannot extend and the length stays 2."},{"at":{"i":3,"j":3},"vars":{"best":2,"len":2},"note":"Index 3 is finished with length 2, the longest strictly increasing subsequence that ends at value 2."},{"at":{"i":4,"j":0},"vars":{"best":2,"len":1},"note":"Index 4 holds 7 and index 0 holds 5. The smaller earlier value extends length 1, so the length at index 4 is 2."},{"at":{"i":4,"j":1},"vars":{"best":2,"len":1},"note":"Index 4 holds 7 and index 1 holds 1. The extension gives 2, which does not beat 2, so the length stays 2."},{"at":{"i":4,"j":2},"vars":{"best":3,"len":2},"note":"Index 4 holds 7 and index 2 holds 6. The smaller earlier value extends length 2, so the length at index 4 is 3."},{"at":{"i":4,"j":3},"vars":{"best":3,"len":2},"note":"Index 4 holds 7 and index 3 holds 2. The extension gives 3, which does not beat 3, so the length stays 3."},{"at":{"i":4,"j":4},"vars":{"best":3,"len":3},"note":"Index 4 is finished with length 3, the longest strictly increasing subsequence that ends at value 7."},{"at":{"i":5,"j":0},"vars":{"best":1,"len":1},"note":"Index 5 holds 3 and index 0 holds 5. The earlier value is not smaller, so it cannot extend and the length stays 1."},{"at":{"i":5,"j":1},"vars":{"best":2,"len":1},"note":"Index 5 holds 3 and index 1 holds 1. The smaller earlier value extends length 1, so the length at index 5 is 2."},{"at":{"i":5,"j":2},"vars":{"best":2,"len":2},"note":"Index 5 holds 3 and index 2 holds 6. The earlier value is not smaller, so it cannot extend and the length stays 2."},{"at":{"i":5,"j":3},"vars":{"best":3,"len":2},"note":"Index 5 holds 3 and index 3 holds 2. The smaller earlier value extends length 2, so the length at index 5 is 3."},{"at":{"i":5,"j":4},"vars":{"best":3,"len":3},"note":"Index 5 holds 3 and index 4 holds 7. The earlier value is not smaller, so it cannot extend and the length stays 3."},{"at":{"i":5,"j":5},"vars":{"best":3,"len":3},"note":"Index 5 is finished with length 3, the longest strictly increasing subsequence that ends at value 3."},{"at":{"i":6,"j":0},"vars":{"best":2,"len":1},"note":"Index 6 holds 8 and index 0 holds 5. The smaller earlier value extends length 1, so the length at index 6 is 2."},{"at":{"i":6,"j":1},"vars":{"best":2,"len":1},"note":"Index 6 holds 8 and index 1 holds 1. The extension gives 2, which does not beat 2, so the length stays 2."},{"at":{"i":6,"j":2},"vars":{"best":3,"len":2},"note":"Index 6 holds 8 and index 2 holds 6. The smaller earlier value extends length 2, so the length at index 6 is 3."},{"at":{"i":6,"j":3},"vars":{"best":3,"len":2},"note":"Index 6 holds 8 and index 3 holds 2. The extension gives 3, which does not beat 3, so the length stays 3."},{"at":{"i":6,"j":4},"vars":{"best":4,"len":3},"note":"Index 6 holds 8 and index 4 holds 7. The smaller earlier value extends length 3, so the length at index 6 is 4."},{"at":{"i":6,"j":5},"vars":{"best":4,"len":3},"note":"Index 6 holds 8 and index 5 holds 3. The extension gives 4, which does not beat 4, so the length stays 4."},{"at":{"i":6,"j":6},"vars":{"best":4,"len":4},"note":"Index 6 is finished with length 4, the longest strictly increasing subsequence that ends at value 8."}]}
```

#### Tails On An Array With Equal Values

The second run uses the readings 4, 8, 4, 9, 2, 3, 5, 5 and 6. The pointer `i` marks the reading being placed. The variable `x` is that reading, `pos` is its lower bound among the tails, and `size` is the length found so far.

The first two readings grow the list to 4 and 8, and 9 grows it to length 3. The second 4 finds the tail 4 already at position 0, so it replaces that tail with an equal value and the length stays. The reading 2 then replaces 4, which makes the list 2, 8, 9. That list is not a subsequence of the input, since 2 comes after 8 and 9. The readings 3 and 5 replace 8 and 9, and the second 5 changes nothing. The reading 6 grows the list to length 4. The tails 2, 3, 5 and 6 happen to form a subsequence here, yet the method never relies on that.

```trace
{"cells":[4,8,4,9,2,3,5,5,6],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"x":0,"pos":0,"size":0},"note":"The tails list starts empty, so the length is 0."},{"at":{"i":0},"vars":{"x":4,"pos":0,"size":1},"note":"Value 4. No tail is at least 4, so it goes at position 0 and the length grows to 1. Tails are now [4]."},{"at":{"i":1},"vars":{"x":8,"pos":1,"size":2},"note":"Value 8. No tail is at least 8, so it goes at position 1 and the length grows to 2. Tails are now [4, 8]."},{"at":{"i":2},"vars":{"x":4,"pos":0,"size":2},"note":"Value 4. The first tail that is at least 4 is 4 at position 0, so 4 replaces it and the length stays 2. Tails are now [4, 8]."},{"at":{"i":3},"vars":{"x":9,"pos":2,"size":3},"note":"Value 9. No tail is at least 9, so it goes at position 2 and the length grows to 3. Tails are now [4, 8, 9]."},{"at":{"i":4},"vars":{"x":2,"pos":0,"size":3},"note":"Value 2. The first tail that is at least 2 is 4 at position 0, so 2 replaces it and the length stays 3. Tails are now [2, 8, 9]."},{"at":{"i":5},"vars":{"x":3,"pos":1,"size":3},"note":"Value 3. The first tail that is at least 3 is 8 at position 1, so 3 replaces it and the length stays 3. Tails are now [2, 3, 9]."},{"at":{"i":6},"vars":{"x":5,"pos":2,"size":3},"note":"Value 5. The first tail that is at least 5 is 9 at position 2, so 5 replaces it and the length stays 3. Tails are now [2, 3, 5]."},{"at":{"i":7},"vars":{"x":5,"pos":2,"size":3},"note":"Value 5. The first tail that is at least 5 is 5 at position 2, so 5 replaces it and the length stays 3. Tails are now [2, 3, 5]."},{"at":{"i":8},"vars":{"x":6,"pos":3,"size":4},"note":"Value 6. No tail is at least 6, so it goes at position 3 and the length grows to 4. Tails are now [2, 3, 5, 6]."}]}
```

<!-- stage: code -->
### Two Methods For The Same Length

The first method fills the table of lengths. The second keeps the sorted tails and searches for each position.

```java
static int lisQuadratic(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    int best = 0;
    for (int i = 0; i < n; i++) {
        dp[i] = 1;
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i] && dp[j] + 1 > dp[i]) dp[i] = dp[j] + 1;
        }
        best = Math.max(best, dp[i]);
    }
    return best;
}

static int lisTails(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;
    for (int x : nums) {
        int lo = 0;
        int hi = size;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (tails[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        tails[lo] = x;
        if (lo == size) size++;
    }
    return size;
}
```

The first method costs O(n^2) time and O(n) memory. The second costs O(n log n) time, because each element needs one binary search over at most n entries, and it uses O(n) memory. Both return 0 for an empty array, since the loops never run. The search keeps `tails[mid] < x` as the move-right test, which makes it a lower bound and handles equal values. The exercises below build the table first, then change the question, then the comparison, then the input size.

<!-- stage: applicability -->
### Recognizing Rising Subsequences

#### Reading The Cue

Use this method when the answer is a longest chain of elements that keep their order, the elements need not be adjacent, and each chosen element must be larger than the previous one. Words such as "not necessarily contiguous" and "strictly increasing" point here. The quadratic table fits small inputs and also fits questions that need a value for each ending index. The sorted tails fit large inputs where only the length matters.

#### Checking The Invariant

The invariant of the table says that `dp[i]` is final before any later index reads it. The invariant of the tails says that the list is strictly increasing and holds the smallest possible tail for each length. Test an array in strictly decreasing order, which must give 1. Test an array of equal values, which must also give 1 for a strict rule. Test an empty array and a single element.

#### Avoiding The False Friend

The first false friend is the longest increasing block of adjacent elements, which passes sorted inputs and fails the opening readings. The second is reading the tails list as the answer subsequence, which fails whenever a small value arrives late. The third is an upper bound search, which lets equal values extend the list and so solves the non-decreasing question. This method does not apply when the chosen elements must be adjacent, or when the answer needs a weighted sum in place of a count, because the tails list stores no weights.

<!-- stage: exercises -->
### Exercises

#### [Build] LIS Ending At I (Author exercise)
<!-- id: is-ending-at-i -->

**Prerequisites.** The length table from this lesson.

**Problem.** An array `nums` of integers is given. For each index `i`, return the length of the longest strictly increasing subsequence whose last element is `nums[i]`. Return an `int[]` of the same length as `nums`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 2000`.
- **Value** satisfies `-10^9 <= nums[i] <= 10^9`.
- **Result** has the same length as `nums`, and an empty input gives an empty array.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [3,1,4,1,5,9,2,6]`, output `[1,1,2,1,3,4,2,4]`.

**Example 2.** Input `nums = [4,4,4]`, output `[1,1,1]`.

**Hint.** Which earlier entries may extend index `i`, and what does every entry start as?

**Changed decision.** The method returns the whole table in place of its largest entry. Each entry depends only on earlier entries that hold smaller values.

#### [Vary] Longest Increasing Subsequence (LeetCode 300)
<!-- id: is-quadratic-length -->

**Prerequisites.** The exercise above.

**Problem.** An array `nums` of integers is given. Return the length of the longest strictly increasing subsequence of `nums`, using the quadratic table.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 2500`.
- **Value** satisfies `-10^4 <= nums[i] <= 10^4`.
- **Result** is an `int`, and an empty input gives 0.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [0,8,4,12,2,10,6,14]`, output `4`.

**Example 2.** Input `nums = [7,7,7,7]`, output `1`.

**Hint.** The answer is not the last entry of the table. Where can the best subsequence end?

**Changed decision.** The method takes the maximum over all entries of the table from the previous exercise. The best subsequence may end at any index.

#### [Boundary] Duplicates (Author exercise)
<!-- id: is-duplicates -->

**Prerequisites.** The two exercises above and the tails list from this lesson.

**Problem.** An array `nums` of integers may contain equal values. Return an `int[]` of length 2. Entry 0 is the length of the longest strictly increasing subsequence. Entry 1 is the length of the longest non-decreasing subsequence, where each kept element is at least the one before it.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 100000`.
- **Value** satisfies `-10^9 <= nums[i] <= 10^9`, and equal values are common.
- **Result** has length 2, and an empty input gives `[0,0]`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [2,2,3,3,1,3]`, output `[2,5]`.

**Example 2.** Input `nums = [5,4,3]`, output `[1,1]`.

**Hint.** Which search position, the first tail at least `x` or the first tail larger than `x`, lets an equal value extend the list?

**Changed decision.** The strict count places each value at the lower bound, and the non-decreasing count places it at the first tail larger than the value. Only the comparison in the search differs.

#### [Recognize] Prefix Lengths In O(n log n) (LeetCode 300)
<!-- id: is-prefix-lengths -->

**Prerequisites.** All three exercises above.

**Problem.** An array `nums` of integers is given. For each `k` from 1 to `nums.length`, return the length of the longest strictly increasing subsequence of the first `k` elements. The result `int[]` holds one entry per prefix.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 200000`.
- **Value** satisfies `-10^9 <= nums[i] <= 10^9`.
- **Result** has the same length as `nums`, and an empty input gives an empty array.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [3,1,2,1,5,4,6]`, output `[1,1,2,2,3,3,4]`.

**Example 2.** Input `nums = [5,4,3,2]`, output `[1,1,1,1]`.

**Hint.** After the tails list absorbs the first `k` elements, which number already equals the answer for that prefix?

**Changed decision.** The method records the size of the tails list after every element in place of reading it once at the end. The input size rules out the quadratic table.
