<!-- lesson-kind: standard -->
<!-- lesson-id: first-and-last -->
## First And Last

<!-- stage: context -->
### A Warehouse Aisle Of Batch Numbers

A warehouse stores crates along one long aisle, in order of batch number. Many crates share a batch, because batches are shipped in lots of fifty or more. An inspector has been told that a defect was traced to batch 17, and she wants to pull every crate of that batch. For that she needs two positions: the first crate marked 17 and the last crate marked 17, so that everything between them can be pulled in one sweep.

She knows that finding some crate marked 17 is quick. She can walk to the middle of the aisle, read a number, and halve the part of the aisle that still matters, again and again. But when she lands on a crate marked 17 she cannot tell, from that crate alone, whether it is the first of its batch, the last, or somewhere in between. A batch of two hundred crates leaves her with a lot of aisle to examine.

<!-- stage: naive -->
### Find Any Crate, Then Walk Outward

The natural plan is to find one crate of the batch quickly, then walk left until the batch changes, and walk right until it changes.

```java
static int[] rangeByWalking(int[] aisle, int batch) {
    int lo = 0, hi = aisle.length - 1, hit = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (aisle[mid] == batch) { hit = mid; break; }
        if (aisle[mid] < batch) lo = mid + 1;
        else hi = mid - 1;
    }
    if (hit == -1) return new int[] {-1, -1};
    int first = hit, last = hit;
    while (first > 0 && aisle[first - 1] == batch) first--;
    while (last + 1 < aisle.length && aisle[last + 1] == batch) last++;
    return new int[] {first, last};
}
```

It gives the correct pair for any aisle, and it returns minus one twice when the batch is not present.

<!-- stage: bottleneck -->
### The Walk Can Cover The Whole Aisle

The search for any crate takes O(log n) readings, but the two walks that follow read one crate at a time. If the whole aisle holds the same batch, the first search lands in the middle and the walks together read all n crates, so the method as a whole is O(n), no better than reading everything. The slow part is repeated reading of crates that the sorted order already told us about.

The aisle is sorted, so the first crate of the batch can be found by the same halving idea, if the search is told what to do on a hit. On landing on the batch, the search should not stop. It should note the position and keep going into the part of the aisle that could still hold something better, which is the left part when the first crate is wanted and the right part when the last crate is wanted. Both answers then cost O(log n).

<!-- stage: insight -->
### A Hit Is Only A Candidate

When the middle value equals the target, the position is a **candidate** for the answer, and nothing more. For the first occurrence, a better answer, if one exists, must be to the left of the candidate, so the search records the candidate and moves the right edge to `mid - 1`. For the last occurrence, it records the candidate and moves the left edge to `mid + 1`. The loop then continues until the interval is empty, and the most recent candidate is the answer.

The two searches differ in one line. The first looks for the **leftmost occurrence**, and a hit pushes the search left. The second looks for the **rightmost occurrence**, and a hit pushes the search right. In both, a middle value smaller than the target moves the left edge up, and a larger one moves the right edge down, exactly as in exact search.

<!-- names: candidate, leftmost occurrence, rightmost occurrence -->

The invariant becomes a statement about two things at once. The recorded candidate is a genuine occurrence, and any occurrence better than it lies inside the current interval. When the interval becomes empty, nothing better remains, so the candidate is the answer, or there never was one. This is why every position the loop discards must be provably no better than the candidate, and why stopping on the first hit would break the guarantee.

The same shape appears in problems with no repeated values at all. A line of software versions is good for a while and bad from some version on. Finding the first bad version is the same as finding the leftmost position of a predicate that is true, which makes each hit a candidate and each miss a proof that everything before it is good.

<!-- stage: variables -->
### Edges, Candidate And Answer Pair

`lo` and `hi` are the edges of the closed interval, as before. `candidate` starts at minus one and is overwritten at every hit, and it is never overwritten by a worse position because a hit always keeps searching toward the better side. The answer for a range query is the pair of the two candidates from the two searches, and when either search never found a hit, both stay at minus one. For versions, the predicate answers whether a given version is bad, and the candidate is the smallest bad version seen so far.

<!-- stage: trace -->
### Searching Left And Then Right

The first trace looks for the first 7 in the array 1, 3, 7, 7, 7, 7, 9, 12. The very first reading lands on position 3, which holds 7. That position is recorded and the right edge moves to 2, because only positions to the left can be better. The step to study is the third, where position 2 is found and recorded, replacing the earlier candidate with a better one.

```trace
{"cells":[1,3,7,7,7,7,9,12],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":7,"mid":3},"vars":{"value":7,"candidate":3},"note":"Read position 3: 7 equals the target. Record 3 as the candidate, and since a smaller index could still hold the target, hi becomes 2."},{"at":{"lo":0,"hi":2,"mid":1},"vars":{"value":3,"candidate":3},"note":"Read position 1: 3 is too small, so lo becomes 2."},{"at":{"lo":2,"hi":2,"mid":2},"vars":{"value":7,"candidate":2},"note":"Read position 2: 7 equals the target. Record 2 as the candidate, and since a smaller index could still hold the target, hi becomes 1."}]}
```

The second trace looks for the last 7 in the same array. Hits push the left edge up instead. The step to study is the last one: position 6 holds 9, which is too large, so the right edge drops to 5, and the most recent candidate, position 5, is the answer.

```trace
{"cells":[1,3,7,7,7,7,9,12],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":7,"mid":3},"vars":{"value":7,"candidate":3},"note":"Read position 3: 7 equals the target. Record 3 as the candidate, and since a larger index could still hold the target, lo becomes 4."},{"at":{"lo":4,"hi":7,"mid":5},"vars":{"value":7,"candidate":5},"note":"Read position 5: 7 equals the target. Record 5 as the candidate, and since a larger index could still hold the target, lo becomes 6."},{"at":{"lo":6,"hi":7,"mid":6},"vars":{"value":9,"candidate":5},"note":"Read position 6: 9 is too large, so hi becomes 5."}]}
```

<!-- stage: code -->
### Two Searches And A Version Hunt

```java
static int firstOccurrence(int[] a, int target) {
    int lo = 0, hi = a.length - 1, candidate = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else if (a[mid] > target) hi = mid - 1;
        else { candidate = mid; hi = mid - 1; }     // better answer must be on the left
    }
    return candidate;
}

static int lastOccurrence(int[] a, int target) {
    int lo = 0, hi = a.length - 1, candidate = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else if (a[mid] > target) hi = mid - 1;
        else { candidate = mid; lo = mid + 1; }     // better answer must be on the right
    }
    return candidate;
}

static int firstBadVersion(int n, IntPredicate isBad) {
    int lo = 1, hi = n, candidate = n;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (isBad.test(mid)) { candidate = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return candidate;
}
```

Each search halves the interval, so each takes logarithmic time with constant memory, O(log n) and O(1), and a range query that runs both is also O(log n). In `firstBadVersion` the predicate replaces the comparison, and the candidate starts at `n` because the contract promises that some version is bad.

<!-- stage: applicability -->
### When The Answer Is An Extreme Occurrence

Use this shape when values repeat and the question asks for the first, the last, or the count of occurrences, where the count is the last position minus the first plus one. State the invariant before coding: the candidate is a real occurrence and no better one lies outside the interval. Decide which edge moves on a hit before writing anything else, and keep that line separate from the two comparison lines.

A false friend is exact search from the previous lesson. It is allowed to stop on equality, and used here it would return an arbitrary occurrence. Another is the walk outward from a hit, which looks cheap but degrades to O(n) when the repeated run is long. A third is a problem that has repeated values but asks only for existence, where the plain version is enough.

In Java, initialize the candidate to the value the problem wants for "absent", usually minus one, and do not return from inside the loop. For the version problem the predicate may be an expensive call, so count how many times it is called, and note that the candidate-keeping loop makes at most one call per halving. Use `lo + (hi - lo) / 2` in every variant.

<!-- stage: exercises -->
### Exercises

#### [Build] First Occurrence (Author exercise)
<!-- id: bs-first-occurrence -->

**Prerequisites.** The exact-search lesson, and the idea of a candidate answer.

**Problem.** Given an array sorted in nondecreasing order, possibly with repeats, return the smallest index whose value equals the target, or minus one if the target is absent. Do not walk outward from a hit.

**Constraints.** 0 <= nums.length <= 100000 and any `int` values. The method must make O(log n) readings even when every value is equal.

**Example 1.** Input `nums = [2, 2, 5, 5, 5, 9], target = 5`, output 2.

**Example 2.** Input `nums = [1, 3], target = 4`, output -1.

**Hint.** When the middle value equals the target, which side could hold a smaller index? What should you do with the position you just found?

**Changed decision.** First rung: equality no longer ends the search, it only records a candidate and moves the right edge.

#### [Vary] Last Occurrence (Author exercise)
<!-- id: bs-last-occurrence -->

**Prerequisites.** The first-occurrence exercise above.

**Problem.** Given the same kind of array, return the largest index whose value equals the target, or minus one if absent. Preserve a candidate at each hit and continue to the right.

**Constraints.** 0 <= nums.length <= 100000 and any `int` values, with repeats allowed. Use O(log n) readings.

**Example 1.** Input `nums = [2, 2, 5, 5, 5, 9], target = 5`, output 4.

**Example 2.** Input `nums = [6, 6, 6], target = 6`, output 2.

**Hint.** Which edge moves on a hit this time? How does the final answer relate to the last recorded candidate?

**Changed decision.** The direction after a hit flips, so the left edge moves up and the candidate marches toward the end of the run.

#### [Boundary] Find First and Last Position of Element in Sorted Array (LeetCode 34)
<!-- id: bs-search-range -->

**Prerequisites.** The two exercises above.

**Problem.** Return the pair of the first and last index of the target in a sorted array with repeats, or the pair minus one and minus one when it is absent. Include arrays in which every element is equal to the target.

**Constraints.** 0 <= nums.length <= 100000 and any `int` values. Run in O(log n), and do not scan the array.

**Example 1.** Input `nums = [3, 3, 3, 3], target = 3`, output `[0, 3]`.

**Example 2.** Input `nums = [1, 2, 4], target = 3`, output `[-1, -1]`.

**Hint.** If the first search returns minus one, what does that say about the second search? How many readings does an array of identical values need?

**Changed decision.** The edge cases are the whole-array run and the absent target, where a walk outward would be linear or a pair would be inconsistent.

#### [Recognize] First Bad Version (LeetCode 278)
<!-- id: bs-first-bad-version -->

**Prerequisites.** All three exercises above.

**Problem.** Versions 1 to n were released in order, and from some version on every version is bad. A call to the predicate tells whether one version is bad. Return the first bad version, with the fewest calls you can manage.

**Constraints.** 1 <= n <= 2000000000, at least one version is bad, and the predicate is monotone: once bad, always bad. Use a closed interval and keep a candidate.

**Example 1.** Input `n = 10`, first bad version 4, output 4.

**Example 2.** Input `n = 1`, first bad version 1, output 1.

**Hint.** What does a bad version tell you about every version after it? What does a good version tell you about every version before it?

**Changed decision.** There are no repeated values and no array; the predicate replaces the comparison, and the candidate is the smallest bad version seen so far.
