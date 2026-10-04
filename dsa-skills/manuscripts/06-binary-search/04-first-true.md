<!-- lesson-kind: standard -->
<!-- lesson-id: first-true -->
## Find The First True Value

<!-- stage: context -->
### Which Nightly Run Broke The Test

A team keeps 1,024 nightly builds. A regression test passes on the oldest build and fails on the newest, and it fails on every build after the first failure. Running the test on one build takes ten minutes. Checking the builds one after another costs up to 10,240 minutes, about a week of machine time. The team wants to know which build introduced the failure.

No sorted array is in sight here, and no value is compared with a target. This lesson answers one question. When each position answers a yes-or-no question, and the answers switch only once, how few questions find the position where they switch?

<!-- stage: naive -->
### Asking The Question In Order

The direct method asks the question for build 0, then build 1, and so on, and returns the first build where the answer is yes. If no build says yes, it returns the number of builds.

```java
static int firstFailingBuild(java.util.function.IntPredicate fails, int n) {
    for (int i = 0; i < n; i++) {
        if (fails.test(i)) return i;
    }
    return n;
}
```

For 8 builds where builds 3 to 7 fail, the loop asks four questions and returns 3. The answer is correct. The cost is one question for every build before the failure.

```predict
The failure starts at build 1,000 out of 1,024, and each question costs ten minutes. How many minutes does the loop spend, and which answers did it already know that it could have skipped?

It spends 10,010 minutes on 1,001 questions, which is O(n) in the number of builds. Builds before the failure all answer no, and once a build answers no, every earlier build must answer no too, so most questions repeat known information.
```

<!-- stage: bottleneck -->
### One Answer Settles Many Builds

The loop asks `n` questions in the worst case, which is O(n). Each answer settles only one build. The structure of the data says more. The answers form a run of no answers followed by a run of yes answers, with no switch back.

A yes at build `b` proves yes for every later build. A no at build `b` proves no for every earlier build. One question about a middle build therefore settles half of the remaining builds, in the same way as one comparison in a sorted array. The loop ignores that structure and pays for each build alone.

<!-- stage: insight -->
### Search For The Switch Point

A **predicate** is a yes-or-no function of the position. It is **monotone** when it switches at most once from false to true, so no true answer is followed by a false answer. The goal is the first position where the predicate is true.

<!-- names: predicate, monotone, sentinel -->

#### The Search Rule

The search keeps the half-open interval `[lo, hi)` from the previous lesson, with `hi` starting at the number of positions `n`. At `mid`, call the predicate once. If it is true, `mid` could be the first true position, so the search sets `hi = mid`. If it is false, every position up to `mid` is false, so the search sets `lo = mid + 1`. The loop ends when `lo == hi`.

#### The Sentinel Answer

The position `n` does not exist, but it is a legal answer. A **sentinel** is a value outside the real data that stands for "none". Here `n` means that no position is true. Starting `hi` at `n` makes this outcome appear without extra code, because `lo` reaches `n` when every probed position is false.

#### What The Lower Bound Was

The lower bound is the same search with the predicate `nums[i] >= target`. That predicate is monotone because the array is sorted. The search never looks at an array. It needs only the predicate, so it can run on a build number, a day, a size or any ordered position.

<!-- stage: variables -->
### The State And Its Promise

The search has three names, and the promise about the predicate carries the proof.

- **lo** is the smallest position that can still be the first true one, and every position below it is false.
- **hi** is a position that is true or equals `n`, and the first true position is at most `hi`.
- **mid** is `lo + (hi - lo) / 2`, and the predicate is called once at `mid`.

The loop ends with `lo == hi`. That position is the first true position, or `n` when none exists.

<!-- stage: trace -->
### Two Searches Over Yes And No Answers

#### Eight Builds With A Failure At Build 3

The cells hold 0 for a passing build and 1 for a failing build. The failure starts at build 3. The first midpoint is build 4, which fails, so `hi` becomes 4. The midpoint at build 2 passes, so `lo` becomes 3. The midpoint at build 3 fails, so `hi` becomes 3. The interval is empty and the answer is 3 after three questions.

```trace
{"cells":[0,0,0,1,1,1,1,1],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":8,"mid":-1},"vars":{"interval":"[0, 8)"},"note":"The half-open interval covers builds 0 to 7. The value 8 stands for no failing build."},{"at":{"lo":0,"hi":8,"mid":4},"vars":{"fails":"true","interval":"[0, 4)"},"note":"Build 4 fails, so it may be the first failing build. hi becomes 4."},{"at":{"lo":0,"hi":4,"mid":2},"vars":{"fails":"false","interval":"[3, 4)"},"note":"Build 2 passes, so every earlier build passes too. lo becomes 3."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"fails":"true","interval":"[3, 3)"},"note":"Build 3 fails, so it may be the first failing build. hi becomes 3."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"interval":"[3, 3)"},"note":"The interval is empty, so the search returns 3."}]}
```

#### Five Builds That All Pass

The cells are all 0, so no build fails. The first midpoint is build 2, which passes, so `lo` becomes 3. The midpoint at build 4 passes, so `lo` becomes 5. The interval is empty at 5, which equals the number of builds, so the search returns the sentinel 5.

```trace
{"cells":[0,0,0,0,0],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"interval":"[0, 5)"},"note":"The half-open interval covers builds 0 to 4. The value 5 stands for no failing build."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"fails":"false","interval":"[3, 5)"},"note":"Build 2 passes, so every earlier build passes too. lo becomes 3."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"fails":"false","interval":"[5, 5)"},"note":"Build 4 passes, so every earlier build passes too. lo becomes 5."},{"at":{"lo":5,"hi":5,"mid":-1},"vars":{"interval":"[5, 5)"},"note":"The interval is empty, so the search returns 5. That value equals the number of builds, so no build fails."}]}
```

<!-- stage: code -->
### One Loop For Every Predicate

```java
static int firstTrue(int n, java.util.function.IntPredicate test) {
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (test.test(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

The method calls `test` at most `floor(log2(n)) + 1` times. For 1,024 builds that is at most 11 calls, which is 110 minutes and not 10,240. The lower bound of the previous lesson is `firstTrue(n, i -> nums[i] >= target)`. An empty range, `n == 0`, returns 0 without any call.

<!-- stage: applicability -->
### When The Switch Is Single

#### The Invariant

The invariant is that every position below `lo` is false and the position `hi` is true or equals `n`. A false answer at `mid` moves `lo` past it, and a true answer moves `hi` onto it. Both moves keep the invariant, and an empty interval leaves only one candidate.

#### The False Friend

A predicate that is not monotone is the false friend. Take the answers false, true, false, true over four positions. The first midpoint is position 2, which is false, so the search moves `lo` to 3. It then finds position 3 true and returns 3, although position 1 is the first true one. Discarding half the data is justified only by monotonicity, and no comparison of neighbors can repair it.

#### Checking The Switch Before Searching

Before writing the loop, state the predicate in one line and say why a true at `p` forces a true at every later `p`. If that sentence cannot be written, the search does not apply. Problems that count something up to each index often pass this test, because a running count never decreases.

<!-- stage: exercises -->
### Exercises

#### [Build] First True Boolean (Author exercise)
<!-- id: bs-first-true-array -->

**Prerequisites.** The search rule and the sentinel answer of this lesson.

**Problem.** Given a boolean array `flags` that holds some number of `false` values followed by `true` values, return the index of the first `true`. Return `flags.length` when the array holds no `true`.

**Constraints.** The limits are:
- **Length** is `0 <= flags.length <= 10^5`.
- **Shape** is `false` values first and then `true` values, and either part may be empty.
- **Answer** lies in `0` to `flags.length`.
- **Mutation** does not occur; `flags` does not change.

**Example 1.** Input `flags = [false,false,true,true]`, output 2.

**Example 2.** Input `flags = [false,false,false]`, output 3.

**Hint.** If `flags[mid]` is true, can the first true lie after `mid`? If it is false, can it lie at or before `mid`?

**Changed decision.** Basic case: the loop tests a stored boolean instead of comparing two numbers.

#### [Vary] First Bad Build Between Two Known Builds (LeetCode 278)
<!-- id: bs-bad-between -->

**Prerequisites.** The first exercise above.

**Problem.** Builds are numbered with integers. Build `good` is known to pass and build `bad` is known to fail, with `good < bad`. The oracle `fails(b)` is monotone: it returns `false` up to some build and `true` from the next build on. Return the first failing build, and never call `fails` on `good` or `bad`.

**Constraints.** The limits are:
- **Range** is `0 <= good < bad <= 2^31 - 1`.
- **Oracle** is monotone, and the first failing build lies in `good + 1` to `bad`.
- **Calls** to `fails` number at most `31`.
- **Answer** is one `int`.

**Example 1.** Input `good = 10`, `bad = 20` and first failing build 17, output 17.

**Example 2.** Input `good = 0`, `bad = 1`, output 1, with no call to `fails`.

**Hint.** The interval of possible answers is `good + 1` to `bad`, and `bad` is already known to fail. Where should `hi` start?

**Changed decision.** Two builds are known in advance, so the interval starts smaller and the endpoints cost no calls.

#### [Boundary] No True Value (Author exercise)
<!-- id: bs-no-true -->

**Prerequisites.** Both exercises above.

**Problem.** Given an integer `n` and a monotone oracle `isTrue(i)` for positions `0` to `n - 1`, return the first position where it is true. Return `n` when the oracle is false everywhere. Report also the number of oracle calls as the second entry of a pair `[position, calls]`.

**Constraints.** The limits are:
- **Count** is `0 <= n <= 10^9`; zero positions is valid.
- **Oracle** is monotone: false for a prefix and true afterward.
- **Calls** number at most `floor(log2(n)) + 1`, and zero when `n == 0`.
- **Answer** is `[position, calls]` with both values as `int`.

**Example 1.** Input `n = 5` with every position false, output `[5,2]`.

**Example 2.** Input `n = 0`, output `[0,0]`.

**Hint.** What value does `lo` reach when every probed position is false? Which loop condition prevents any call when `n == 0`?

**Changed decision.** The sentinel `n` is a valid result, and the empty range must make no call.

#### [Recognize] Kth Missing Positive Number (LeetCode 1539)
<!-- id: bs-kth-missing -->

**Prerequisites.** All exercises above.

**Problem.** An array `arr` holds distinct positive integers in ascending order. The positive integers that do not occur in `arr` are called missing, listed in ascending order. Given `arr` and a positive integer `k`, return the `k`-th missing positive integer.

**Constraints.** The limits are:
- **Length** is `1 <= arr.length <= 1000`.
- **Values** satisfy `1 <= arr[i] <= 1000`, distinct and ascending.
- **Rank** satisfies `1 <= k <= 1000`.
- **Answer** may exceed `arr[arr.length - 1]`.

**Example 1.** Input `arr = [2,3,4,7,11]` and `k = 5`, output 9.

**Example 2.** Input `arr = [4,5,6]` and `k = 2`, output 2.

**Hint.** The count of missing numbers below `arr[i]` is `arr[i] - (i + 1)`. Does that count ever decrease as `i` grows? Find the first `i` where it reaches `k`.

**Changed decision.** The predicate is a count compared with `k`, and the answer is computed from the final index and not read from the array.
