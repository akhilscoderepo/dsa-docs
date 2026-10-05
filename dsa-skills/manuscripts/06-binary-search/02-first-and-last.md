<!-- lesson-kind: standard -->
<!-- lesson-id: first-and-last -->
## Find The First Or Last Match

<!-- stage: context -->
### A Report That Names The Wrong Row

A monitoring tool keeps error codes in ascending order, one entry per failed request. An engineer asks for the earliest row with code 503, because the first failed request marks the start of an outage. The tool runs a search, finds a row with code 503 and prints "outage began at row 4,812". The engineer opens the log and sees code 503 in rows 4,790 to 4,811 as well.

The search found a correct match, and the report is still wrong. This lesson answers one question. When many entries equal the target, how does a search return a specific one, the earliest or the latest?

<!-- stage: naive -->
### Walking Away From Any Match

A binary search such as `Arrays.binarySearch` returns some matching index. The quick repair is to walk left from that index while the previous entry also equals the target.

```java
static int earliestByWalking(int[] nums, int target) {
    int i = java.util.Arrays.binarySearch(nums, target);
    if (i < 0) return -1;
    while (i > 0 && nums[i - 1] == target) i--;
    return i;
}
```

On `[5, 7, 7, 7, 7, 9]` with target 7, the first match is index 2. The walk then moves to index 1 and stops. The result is correct.

```predict
The array holds 1,000,000 entries that all equal the target. The search returns index 499,999. How many steps does the walk take, and how does that compare with the search itself?

The walk takes 499,999 steps, which is O(n). A search that keeps a candidate and halves the range takes about 20 comparisons, so the walk costs far more than the search it follows.
```

<!-- stage: bottleneck -->
### The Walk Undoes The Savings

The binary search costs O(log n), and the walk costs one step per equal entry. When all `n` entries equal the target, the walk costs about `n / 2` steps. The total is O(n), the same as a plain scan. The method pays for sorted data and then ignores sortedness again in the walk.

The walk also repeats work. The walk reads every equal entry to the left one at a time. The sort order already says that those entries form one unbroken group. A group boundary can be found with the same halving idea, if the search keeps going after it finds a match.

<!-- stage: insight -->
### Treat A Match As A Candidate

A match is only a **candidate**, an index that satisfies the contract so far and may still be improved. The search records it and keeps shrinking the interval toward the side that could hold a better one.

#### Searching For The First Occurrence

For the **first occurrence**, an equal entry at `mid` is a candidate, and any better answer lies to its left. The search stores `candidate = mid` and sets `hi = mid - 1`. A smaller entry moves `lo` to `mid + 1`, and a larger entry moves `hi` to `mid - 1`, as before. The loop ends when the interval is empty. The stored candidate is then the smallest matching index, or `-1` if no entry matched.

<!-- names: candidate, first occurrence, last occurrence -->

#### Searching For The Last Occurrence

For the **last occurrence**, the roles of the sides swap. An equal entry is stored as a candidate, and the search sets `lo = mid + 1`, because a better answer lies to the right. Nothing else changes. The two searches differ in one bound update. Both keep the O(log n) cost, because every step still removes `mid` and at least half of the interval.

#### Why Overwriting The Candidate Is Safe

Each later candidate comes from an interval that lies entirely on the better side of the previous one. The newest candidate is therefore always at least as good as the older ones, so a plain assignment is enough.

<!-- stage: variables -->
### Five Names For Two Searches

The first-occurrence and last-occurrence searches share five names.

- **target** is the value whose boundary the search wants, and it never changes.
- **lo** and **hi** are the closed ends of the search interval.
- **mid** is `lo + (hi - lo) / 2`, recomputed at every step.
- **candidate** is the best matching index found so far, and it starts at `-1`.

The candidate changes only on a match. The returned value is the candidate when the loop ends, so `-1` means that no entry matched.

<!-- stage: trace -->
### Searches That Continue After A Match

#### Finding The First 7

The array is `[5, 7, 7, 7, 7, 9]` and the target is 7. The first midpoint is index 2, which holds a 7. The search stores candidate 2 and moves `hi` to 1. The next midpoint is index 0 with value 5, which is smaller, so `lo` becomes 1. The midpoint at index 1 holds another 7, so the candidate improves to 1. Then `hi` becomes 0, the interval is empty, and the answer is 1.

```trace
{"cells":[5,7,7,7,7,9],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"target":"7","candidate":"-1"},"note":"Start with the whole array as the search interval. No candidate exists yet."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"nums[mid]":"7","candidate":"2"},"note":"The value 7 equals the target. Store candidate 2 and keep only the left side, so hi becomes 1."},{"at":{"lo":0,"hi":1,"mid":0},"vars":{"nums[mid]":"5","candidate":"2"},"note":"The value 5 is smaller than 7, so lo becomes 1."},{"at":{"lo":1,"hi":1,"mid":1},"vars":{"nums[mid]":"7","candidate":"1"},"note":"The value 7 equals the target. Store candidate 1 and keep only the left side, so hi becomes 0."},{"at":{"lo":1,"hi":0,"mid":-1},"vars":{"candidate":"1"},"note":"The interval is empty, so the search returns candidate 1."}]}
```

#### Finding The Last 7

The array is `[4, 7, 7, 7, 9, 9, 9]` and the target is 7. The first midpoint is index 3, a match, so the candidate is 3 and `lo` moves to 4. The midpoint at index 5 holds 9, which is larger, so `hi` becomes 4. Index 4 holds 9 as well, so `hi` becomes 3 and the interval is empty. The answer is 3, the candidate stored on the first step.

```trace
{"cells":[4,7,7,7,9,9,9],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":-1},"vars":{"target":"7","candidate":"-1"},"note":"Start with the whole array as the search interval. No candidate exists yet."},{"at":{"lo":0,"hi":6,"mid":3},"vars":{"nums[mid]":"7","candidate":"3"},"note":"The value 7 equals the target. Store candidate 3 and keep only the right side, so lo becomes 4."},{"at":{"lo":4,"hi":6,"mid":5},"vars":{"nums[mid]":"9","candidate":"3"},"note":"The value 9 is larger than 7, so hi becomes 4."},{"at":{"lo":4,"hi":4,"mid":4},"vars":{"nums[mid]":"9","candidate":"3"},"note":"The value 9 is larger than 7, so hi becomes 3."},{"at":{"lo":4,"hi":3,"mid":-1},"vars":{"candidate":"3"},"note":"The interval is empty, so the search returns candidate 3."}]}
```

<!-- stage: code -->
### Two Methods With One Difference

```java
static int firstOccurrence(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1, candidate = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) { candidate = mid; hi = mid - 1; }
        else if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return candidate;
}

static int lastOccurrence(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1, candidate = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) { candidate = mid; lo = mid + 1; }
        else if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return candidate;
}
```

In both methods the match branch still removes `mid` from the interval, so the loop ends. An absent target never changes the candidate, and an empty array returns `-1`. For an array of identical values the loop still takes about `log2(n) + 1` steps.

<!-- stage: applicability -->
### When The Boundary Is The Answer

#### The Invariant

The invariant is that the best matching index, if one exists, lies inside `[lo, hi]` or equals `candidate`. A match at `mid` can give up the right half, because the first occurrence cannot lie there. It cannot give up `mid` itself, which is why the code stores it before moving the bound. The final interval is empty, so nothing better remains.

#### The False Friend

Stopping at the first match is the false friend. It looks like exact search and it is correct when values are distinct. With duplicates the returned index is unspecified, and the library method `Arrays.binarySearch` has the same behavior. Any statement that says "first", "last", "leftmost" or "earliest" needs the candidate rule.

#### Reading A Group Boundary As A Count

The two boundaries give the size of a group. The count of entries equal to the target is `last - first + 1`, computed in O(log n). When the first boundary is `-1`, the count is zero, so test for `-1` before the subtraction. The same shape reappears when a yes-or-no question replaces the equality test, which the lesson on the first true value covers.

<!-- stage: exercises -->
### Exercises

#### [Build] First Occurrence (Author exercise)
<!-- id: bs-first-occurrence -->

**Prerequisites.** The search interval of the previous lesson and the candidate rule above.

**Problem.** Given an array `nums` sorted in non-decreasing order and an integer `target`, return the smallest index `i` with `nums[i] == target`. Return `-1` when no entry equals `target`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`; the empty array is valid.
- **Values** are `int` values in non-decreasing order, and duplicates are allowed.
- **Target** is any `int`.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [5,7,7,7,7,9]` and `target = 7`, output 1.

**Example 2.** Input `nums = [2,2,2,2]` and `target = 3`, output -1.

**Hint.** When `nums[mid]` equals the target, can an index to the right of `mid` be the smallest match? Which bound should move?

**Changed decision.** A match no longer ends the search; it becomes a candidate and the interval moves to the left.

#### [Vary] Last Occurrence (Author exercise)
<!-- id: bs-last-occurrence -->

**Prerequisites.** The first exercise above.

**Problem.** Given an array `nums` sorted in non-decreasing order and an integer `target`, return the largest index `i` with `nums[i] == target`. Return `-1` when no entry equals `target`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values in non-decreasing order, with duplicates.
- **Target** is any `int`.
- **Mutation** does not occur; `nums` does not change.

**Example 1.** Input `nums = [4,7,7,7,9,9,9]` and `target = 7`, output 3.

**Example 2.** Input `nums = [1,1,1,1]` and `target = 1`, output 3.

**Hint.** Reuse the first-occurrence method and decide which side a match should discard.

**Changed decision.** The match sends the interval to the right, so one bound update flips.

#### [Boundary] First And Last Position (LeetCode 34)
<!-- id: bs-range-34 -->

**Prerequisites.** Both exercises above.

**Problem.** Given an array `nums` sorted in non-decreasing order and an integer `target`, return `[first, last]`, the smallest and the largest index of `target`. Return `[-1,-1]` when `target` does not occur.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values in non-decreasing order, and the array may hold one repeated value only.
- **Target** is any `int`.
- **Answer** has `first <= last` when the target occurs, and both entries are `-1` otherwise.

**Example 1.** Input `nums = [3,3,3,3]` and `target = 3`, output `[0,3]`.

**Example 2.** Input `nums = [1,4,4,6]` and `target = 5`, output `[-1,-1]`.

**Hint.** Run the two searches separately. If the first search returns `-1`, what must the second return?

**Changed decision.** The output is a pair, and an absent target must not leave a half-filled pair.

#### [Recognize] First Bad Version (LeetCode 278)
<!-- id: bs-first-bad -->

**Prerequisites.** All exercises above.

**Problem.** Versions `1` to `n` were released in order. A function `isBad(v)` returns `true` for version `v` when it contains the defect. Once a version is bad, every later version is bad. At least one version is bad. Return the smallest bad version while calling `isBad` as few times as the search allows.

**Constraints.** The limits are:
- **Count** is `1 <= n <= 2^31 - 1`.
- **Oracle** `isBad(v)` is monotone: `false` for versions below the first bad one and `true` from there on.
- **Guarantee** the first bad version lies in `1` to `n`.
- **Answer** is one `int`, and `isBad` is called at most `32` times.

**Example 1.** Input `n = 9` and first bad version 6, output 6.

**Example 2.** Input `n = 1` and first bad version 1, output 1.

**Hint.** A bad version at `mid` is a candidate, and a good version rules out everything up to `mid`. Which midpoint form avoids overflow when `n` is near `2^31 - 1`?

**Changed decision.** The data is an oracle and not an array, but the boundary shape is the same candidate rule.
