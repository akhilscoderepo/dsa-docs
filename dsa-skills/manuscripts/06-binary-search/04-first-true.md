<!-- lesson-kind: standard -->
<!-- lesson-id: first-true -->
## First True

<!-- stage: context -->
### A Bottling Line With A Contamination

A bottling line fills bottles one after another, numbered from zero. Partway along the line a valve got dirty, and from that moment on every bottle was contaminated. Bottles before that moment are fine. The inspector wants to recall only the bad stretch, so she needs the number of the first contaminated bottle, or confirmation that the whole run was clean.

The only way to know whether a bottle is contaminated is a laboratory test, which is slow and expensive, and the lab charges for each bottle tested. There are a hundred thousand bottles in the run. Testing every bottle would take weeks, and the inspector suspects she does not need to. Once she knows that bottle 40,000 is clean, she knows that all earlier bottles are clean too, because contamination never goes away once it has started.

<!-- stage: naive -->
### Test Bottles In Order Until One Fails

The direct plan tests the bottles one at a time from the start of the line.

```java
static int firstContaminatedByTesting(boolean[] contaminated) {
    for (int i = 0; i < contaminated.length; i++) {
        if (contaminated[i]) return i;
    }
    return contaminated.length;
}
```

It returns the number of the first bad bottle, and it returns the run length when every bottle tests clean.

<!-- stage: bottleneck -->
### One Paid Test Per Bottle

The loop pays for a lab test at every bottle up to the first bad one, so it makes O(n) tests, and it makes all n tests when the whole run is clean. The tests are not the cheap array reads of earlier lessons. Each one can cost seconds or money, so the count of tests, and not the count of loop turns, is what the inspector is paying for.

The structure of the data allows far fewer tests. The results along the line are a stretch of clean bottles followed by a stretch of contaminated ones, and a single test at any position tells which stretch that position is in. A clean result removes that position and everything before it, and a contaminated result removes everything after it. Each test can therefore remove half of the remaining candidates, and about seventeen tests would settle a hundred thousand bottles, which is O(log n) tests.

<!-- stage: insight -->
### A Question That Flips Exactly Once

The key property is a **monotone predicate**: a yes-or-no question about a position whose answers, read left to right, are some number of no answers followed only by yes answers. Once the answer is yes it stays yes. The goal is the **first true** position, the earliest one where the answer is yes. Nothing about the data has to be a sorted array of numbers. It only needs the question to flip at most once.

The loop keeps a half-open interval `[lo, hi)`, with `hi` initially `n`. The invariant is that every position before `lo` is known to be false, and `hi` is either a position known to be true or the **sentinel** `n`, the value that means "no position is true". At each step the loop tests `mid`. A true result means the first true position is at `mid` or earlier, so `hi = mid`. A false result means it is after `mid`, so `lo = mid + 1`. When `lo` meets `hi`, that position is the answer, and if it equals `n`, the answer is that no position is true.

<!-- names: monotone predicate, first true, sentinel -->

A predicate can hide inside a problem about numbers. Take a sorted list of positive integers with gaps and ask for the k-th positive integer missing from it. At position `i` the number of missing values before `arr[i]` is `arr[i] - (i + 1)`, because a gap-free list would hold `i + 1` as its value there. That count never decreases as `i` grows, so the question "are at least k values missing before this position" is monotone. The first position where it is true is where the k-th missing value has been passed, and the missing value itself is `k + i`, counting the `i` values that are present and smaller.

A false friend is a predicate that goes true, then false, then true again. A single test then says nothing about either side, so no half can be removed, and the loop would give an arbitrary answer. The monotonic property has to be argued from the problem, not assumed.

<!-- stage: variables -->
### Edges, Test Result And Sentinel

`lo` is the first position that might be the answer and `hi` is the first position that might be true or the sentinel. `mid` lies strictly between them or equals `lo`, and so it is always a valid position, because `mid < hi <= n`. The test result for `mid` is the only input to the update. For the missing-number problem, the stored value is not the predicate itself, but the count `arr[mid] - (mid + 1)` is computed from it on demand and compared with `k`.

<!-- stage: trace -->
### A Flip Found And A Gap Counted

The first trace searches the flags F, F, F, T, T, T, T for the first true. The first test at position 3 is true, so the right edge drops to 3. The step to study is the second: position 1 is false, which proves positions 0 and 1 are false, and the left edge jumps to 2. The edges meet at 3.

```trace
{"cells":["F","F","F","T","T","T","T"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":7,"mid":3},"vars":{"test":"true"},"note":"Test position 3: true, so the first true position is 3 or earlier and hi becomes 3."},{"at":{"lo":0,"hi":3,"mid":1},"vars":{"test":"false"},"note":"Test position 1: false, so positions up to 1 are false and lo becomes 2."},{"at":{"lo":2,"hi":3,"mid":2},"vars":{"test":"false"},"note":"Test position 2: false, so positions up to 2 are false and lo becomes 3."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"answer":3},"note":"The edges meet at 3, the first true position."}]}
```

The second trace finds the fifth missing positive number in 2, 3, 4, 7, 11. The missing counts before each position are 1, 1, 1, 3, 6, and the predicate asks whether the count reaches five. Watch the closing step: the edges meet at position 4, where the count first reaches five, and the answer is 4 plus 5, which is 9.

```trace
{"cells":[2,3,4,7,11],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":2},"vars":{"value":4,"missingBefore":1},"note":"Position 2 holds 4 with 1 values missing before it. That is below 5, so lo becomes 3."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"value":11,"missingBefore":6},"note":"Position 4 holds 11 with 6 values missing before it. That reaches 5, so hi becomes 4."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"value":7,"missingBefore":3},"note":"Position 3 holds 7 with 3 values missing before it. That is below 5, so lo becomes 4."},{"at":{"lo":4,"hi":4,"mid":-1},"vars":{"answer":9},"note":"The edges meet at position 4. The answer is 4 + 5 = 9."}]}
```

<!-- stage: code -->
### Flags, Versions And Missing Numbers

```java
static int firstTrue(boolean[] flags) {
    int lo = 0, hi = flags.length;                 // hi == n means "no true value"
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (flags[mid]) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int firstBadVersion(int n, IntPredicate isBad) {
    int lo = 1, hi = n;                            // the contract guarantees version n is bad
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (isBad.test(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int findKthPositive(int[] arr, int k) {
    int lo = 0, hi = arr.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] - (mid + 1) >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo + k;
}
```

Each loop halves the interval, so each makes O(log n) tests of its predicate and uses O(1) extra space. In `findKthPositive`, the final `lo` is the number of values in the array that precede the answer, so adding `k` gives the missing number, even when `lo` equals the array length and the answer lies beyond the largest element.

<!-- stage: applicability -->
### When A Question Flips Only Once

Use first-true search whenever a yes-or-no question about positions or numbers is monotone and the answer is the point where it flips. The invariant to write down is that everything before `lo` is false and `hi` is a possible answer. Before writing the loop, argue why the predicate is monotone, because the search is only correct under that property.

A false friend is a question that is not monotone. "Is this version's test result green" can alternate, so a single reading cannot discard a half. Another false friend is a sorted array searched for a different shape of question: peaks, for example, are not a flip from false to true, and the next lessons treat them with their own rule. A third is a loop that checks the predicate at `hi` itself when `hi` is the sentinel `n`, which reads beyond the array.

In Java, make the sentinel explicit by starting `hi` at `n` and by documenting what the return value `n` means. The midpoint is always below `hi` inside the loop, so reading at `mid` is safe, and the predicate must never be called on `n`. When the predicate is an expensive call, count the calls, and keep the number of calls to at most the number of halvings.

<!-- stage: exercises -->
### Exercises

#### [Build] First True Boolean (Author exercise)
<!-- id: bs-first-true-boolean -->

**Prerequisites.** The lower-and-upper-bounds lesson and its half-open interval.

**Problem.** Given a boolean array that is false for some prefix and true afterwards, return the index of the first true value. State what the method returns when the prefix is the whole array.

**Constraints.** 1 <= flags.length <= 100000. The values are false up to some point and true from then on, with either part possibly empty.

**Example 1.** Input `flags = [false, false, true, true]`, output 2.

**Example 2.** Input `flags = [true]`, output 0.

**Hint.** What does a true value at `mid` prove about the positions after it? What value should `hi` start with, and why?

**Changed decision.** First rung: the array holds the answers of a predicate, so the search is for the flip and not for a value.

#### [Vary] First Bad Version (LeetCode 278)
<!-- id: bs-first-bad-version-halfopen -->

**Prerequisites.** The boolean exercise above, and the earlier version search with a candidate.

**Problem.** Versions 1 to n are released in order and from some version on every version is bad. The predicate call is expensive. Return the first bad version using a half-open interval and no candidate variable, and make at most as many calls as there are halvings of n.

**Constraints.** 1 <= n <= 2000000000, at least one version is bad, and the predicate is monotone. Make at most `ceil(log2 n)` calls.

**Example 1.** Input `n = 100`, first bad version 37, output 37.

**Example 2.** Input `n = 2`, first bad version 2, output 2.

**Hint.** Why can `hi` start at `n` without being tested? What do the edges equal when the loop ends?

**Changed decision.** The stored booleans are replaced by a costly call, and the interval keeps `hi` as a possible answer instead of recording a separate candidate.

#### [Boundary] No True Value (Author exercise)
<!-- id: bs-no-true-value -->

**Prerequisites.** The two exercises above.

**Problem.** Extend the boolean search to arrays that may be entirely false, and return the length of the array in that case. Test the empty array and all-false arrays, and show that the predicate is never read at an index outside the array.

**Constraints.** 0 <= flags.length <= 100000. Any monotone boolean array is allowed, including an entirely false one and an empty one.

**Example 1.** Input `flags = [false, false, false]`, output 3, the sentinel.

**Example 2.** Input `flags = []`, output 0.

**Hint.** When is the position `n` a valid answer? Which positions can `mid` take while `lo < hi`?

**Changed decision.** The contract now allows no true value, so a sentinel answer replaces the guarantee of an answer inside the array.

#### [Recognize] Kth Missing Positive Number (LeetCode 1539)
<!-- id: bs-kth-missing-positive -->

**Prerequisites.** All three exercises above.

**Problem.** A sorted array of distinct positive integers is given. Return the k-th positive integer that does not occur in it. Use the number of missing values before each position as a predicate that can be searched.

**Constraints.** 1 <= arr.length <= 1000, 1 <= arr[i] <= 1000 and strictly increasing, and 1 <= k <= 1000. The answer may lie beyond the largest element.

**Example 1.** Input `arr = [2, 3, 4, 7, 11], k = 5`, output 9.

**Example 2.** Input `arr = [1, 2, 3, 4], k = 2`, output 6.

**Hint.** How many positive integers are missing before position `i`? Why does that count never decrease as `i` grows?

**Changed decision.** The predicate is not stored anywhere; it is derived from the position and the value, and its flip locates a number outside the array.
