<!-- lesson-kind: standard -->
<!-- lesson-id: duplicate-control -->
## Skip Equal Values At One Level

<!-- stage: context -->
### Why The Plan Lists A Server Twice

A deployment tester must try every subset of a cluster. The cluster has two identical `web` servers and one `db` server. The tester reuses the subset search and prints `[web]` twice, `[web, db]` twice and `[web, web]` once. Two of the printed plans repeat another plan, so the tester runs the same deployment test twice for each repeated plan.

The two web servers are interchangeable, so a plan that uses the first one equals a plan that uses the second one. This lesson asks how the search recognizes a repeated choice before it explores it, and why it must still allow a plan that uses both web servers.

<!-- stage: naive -->
### Searching Everything And Dropping Equal Lists

The direct plan runs the subset search from the earlier lesson without any change. It stores each finished list, sorted, in a hash set, and the set drops the repeats.

```java
static void collect(int start, int[] a, List<Integer> path, Set<List<Integer>> seen) {
    List<Integer> key = new ArrayList<>(path);
    Collections.sort(key);                                   // equal lists get one sorted form
    seen.add(key);                                           // the set drops lists that appeared before
    for (int i = start; i < a.length; i++) {                 // every later index, equal values included
        path.add(a[i]);
        collect(i + 1, a, path, seen);
        path.remove(path.size() - 1);                        // undo the choice
    }
}
```

The method returns each different list once. It still explores every index choice, including the choices that repeat an earlier subtree.

<!-- stage: bottleneck -->
### Counting The Repeated Subtrees

```predict
The array holds n = 12 equal values. How many calls does the search make, and how many different subsets exist?

The search makes 2^12 = 4,096 calls, because it treats the 12 copies as different indices. Only 13 different subsets exist, one for each count from 0 to 12. About 315 calls serve each result.
```

The search costs O(n * 2^n) time because every index starts a subtree, but the number of different subsets can be as small as n + 1. Each repeated subtree also costs a sort and a hash.

Two equal values at the same position of a loop start two subtrees that list the same subsets. The second subtree adds nothing, so the loop can skip it. The skip must not remove equal values from different depths, because a plan may need both web servers. The difference between the two cases is the depth of the choice.

<!-- stage: insight -->
### Skipping The Second Copy In One Loop

#### Sorting So Equal Values Touch

The **sorted input** puts equal values at neighbouring indices. After the sort, the copies of one value occupy one block of the array. A loop that scans indices from `start` upward meets a block from left to right, so it sees the first copy before any later copy.

#### Comparing With The Left Neighbour

The **equal siblings** of a call are the choices of its loop that hold the same value. Two siblings start two subtrees with the same list of subsets, so only the first one needs a call. The loop skips index `i` when `i > start` and `a[i] == a[i - 1]`. In that case index `i - 1` was also a choice of this loop, and it has already started the same subtree.

#### Keeping The Check In One Level

The **same-level check** compares `i` with `start`, not with 0. When `i == start`, an earlier call chose the left neighbour `a[i - 1]`, so it sits on the path. The current choice is then the next copy of the value. A path may hold several copies of one value, one in each call along the path. The invariant is that no call starts two subtrees with the same value, and a path may still use a value several times.

<!-- names: sorted input, equal siblings, same-level check -->

<!-- stage: variables -->
### The Pieces Of State

Four pieces of state describe a call.

- **Start** is the index where the loop of this call begins.
- **Index i** is the loop variable, and it runs from `start` to `n - 1`.
- **Path** is the shared list of chosen values, in the order of the sorted array.
- **Left neighbour** is the value `a[i - 1]`, which the loop reads only when `i > start`.

The loop skips index `i` when the left neighbour equals `a[i]` and `i > start`. Every other index starts a call with the start `i + 1`.

<!-- stage: trace -->
### Following The Skip Through Three Values

#### Listing The Subsets Of One And Two Twos

The first trace lists the subsets of `[1, 2, 2]`. The pointer `start` shows the start index of the current call, and the variable `path` shows its path. Each step is either the entry of a call or a skip. The variable `stored` counts the lists in the output.

The root stores `[]` and chooses 1, so the call for `[1]` stores its list and chooses the first 2. The call for `[1, 2]` has start 2, so its choice of index 2 has `i == start`. It makes the call that stores `[1, 2, 2]`. Back in the call for `[1]`, the loop reaches index 2 with `i > start` and an equal left neighbour, so it skips. The root then chooses the first 2, stores `[2]` and `[2, 2]`, and skips index 2 at its own loop. The trace stores 6 lists.

#### Tracing A Check That Looks Too Far

The second trace uses the check `i > 0` instead of `i > start`. The call for `[1, 2]` reaches index 2, finds an equal left neighbour and skips. The search never stores `[1, 2, 2]` or `[2, 2]`. The search loses every list that holds two copies of one value.

#### Stepping Through Both Runs

```trace
{"cells":["1","2","2"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"path":"empty","stored":1},"note":"The root call with start 0 stores the empty list."},{"at":{"start":1},"vars":{"path":"1","stored":2},"note":"The call with start 1 stores [1]."},{"at":{"start":2},"vars":{"path":"1,2","stored":3},"note":"The call with start 2 stores [1,2]."},{"at":{"start":3},"vars":{"path":"1,2,2","stored":4},"note":"The call with start 3 stores [1,2,2]."},{"at":{"start":1},"vars":{"path":"1","stored":4},"note":"The loop reaches index 2, where 2 equals its left neighbour and i is above start, so it skips the choice."},{"at":{"start":2},"vars":{"path":"2","stored":5},"note":"The call with start 2 stores [2]."},{"at":{"start":3},"vars":{"path":"2,2","stored":6},"note":"The call with start 3 stores [2,2]."},{"at":{"start":0},"vars":{"path":"empty","stored":6},"note":"The loop reaches index 2, where 2 equals its left neighbour and i is above start, so it skips the choice."}]}
```

```trace
{"cells":["1","2","2"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"path":"empty","stored":1},"note":"The root call with start 0 stores the empty list."},{"at":{"start":1},"vars":{"path":"1","stored":2},"note":"The call with start 1 stores [1]."},{"at":{"start":2},"vars":{"path":"1,2","stored":3},"note":"The call with start 2 stores [1,2]."},{"at":{"start":2},"vars":{"path":"1,2","stored":3},"note":"The loop reaches index 2, where 2 equals its left neighbour and i is above 0, so it skips the choice."},{"at":{"start":1},"vars":{"path":"1","stored":3},"note":"The loop reaches index 2, where 2 equals its left neighbour and i is above 0, so it skips the choice."},{"at":{"start":2},"vars":{"path":"2","stored":4},"note":"The call with start 2 stores [2]."},{"at":{"start":2},"vars":{"path":"2","stored":4},"note":"The loop reaches index 2, where 2 equals its left neighbour and i is above 0, so it skips the choice."},{"at":{"start":0},"vars":{"path":"empty","stored":4},"note":"The loop reaches index 2, where 2 equals its left neighbour and i is above 0, so it skips the choice."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### Subsets With A Same-Level Check

The method sorts a copy of the input, then runs the search of the subset lesson with one added line.

```java
static List<List<Integer>> subsetsWithDup(int[] nums) {
    int[] a = nums.clone();                            // sort a copy, so the caller's array keeps its order
    Arrays.sort(a);
    List<List<Integer>> out = new ArrayList<>();
    go(0, a, new ArrayList<>(), out);
    return out;
}

static void go(int start, int[] a, List<Integer> path, List<List<Integer>> out) {
    out.add(new ArrayList<>(path));                    // record on entry
    for (int i = start; i < a.length; i++) {
        if (i > start && a[i] == a[i - 1]) continue;   // an equal sibling started this subtree already
        path.add(a[i]);                                // choose index i
        go(i + 1, a, path, out);
        path.remove(path.size() - 1);                  // undo the choice
    }
}
```

#### Comparing Boxed Values

The comparison `a[i] == a[i - 1]` is correct because `a` holds `int` values. If the array held `Integer` objects, the operator `==` would compare references. For values outside the range of -128 to 127, two equal `Integer` objects can have different references, so the check would fail without an error. A boxed array needs `equals`.

#### Cost Of The Search

The search makes one call for each different subset and copies a path of up to n values in each call. The time is O(n * m) for m different subsets, plus O(n log n) for the sort. The path and the call stack together hold O(n) values.

<!-- stage: applicability -->
### Recognizing Repeated Sibling Choices

#### Spotting The Pattern

The cue is an input with equal values and an output that must list each different result once. The invariant is that a call never starts two subtrees with the same value, while a path may use the same value at several depths.

#### Finding The False Friend

The false friend is a check that skips every repeated value, written as `i > 0` or as a global set of seen values. It removes the lists that hold two copies of one value, and the program raises no error. A second false friend is a missing sort. Equal values that do not touch cannot be found with the left neighbour.

#### Recognizing The No-Go Cases

The check does not fit when the order of the input carries meaning, because a sort would destroy it. It does not fit when equality depends on a key and not on the value. The neighbour test would then compare the wrong field. A per-call hash set fits both cases at the price of extra memory.

<!-- stage: exercises -->
### Exercises

#### [Build] Equal Sibling Choices (Author exercise)
<!-- id: bt-equal-sibling-choices -->

**Prerequisites.** The same-level check of this lesson and the subset search of the earlier lesson.

**Problem.** The array `nums` holds integers in nondecreasing order. Run the subset search with a start index twice. The first run explores every index choice. The second run skips an index `i` when `i > start` and `nums[i] == nums[i - 1]`. Return an array of two numbers: the number of calls of the first run and the number of calls of the second run. Count the root call.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 12`.
- **Values** satisfy `-5 <= nums[i] <= 5`, and the values never decrease along the array.
- **Return** is an array of two `long` values.
- **Mutation** does not occur; `nums` keeps its contents.

**Example 1.** Input `nums = [1,2,2]`, output `[8,6]`.

**Example 2.** Input `nums = [3,3,3,3]`, output `[16,5]`.

**Hint.** What does the second run do at the second copy of a value in one loop? How many different subsets does a block of equal values give?

**Changed decision.** The search counts calls, and the second run adds one skip rule to the first.

#### [Vary] Subsets II (LeetCode 90)
<!-- id: bt-subsets-two-skip -->

**Prerequisites.** The previous exercise.

**Problem.** The array `nums` may hold equal values in any order. Return every different subset, where two subsets are different when their sorted lists differ. Sort a copy of `nums`, then search with a start index and the same-level check. Each list follows the order of the sorted copy, and the output order follows the order of the calls.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 12`.
- **Values** satisfy `-10 <= nums[i] <= 10`, and equal values may repeat.
- **Count** of lists equals the product of one plus the count of each value.
- **Mutation** does not occur; `nums` keeps its order.

**Example 1.** Input `nums = [4,4,1,4]`, output `[[],[1],[1,4],[1,4,4],[1,4,4,4],[4],[4,4],[4,4,4]]`.

**Example 2.** Input `nums = [0]`, output `[[],[0]]`.

**Hint.** Which array does the search read, the input or its sorted copy? Which index comparison tells the loop that two siblings are equal?

**Changed decision.** The search returns the lists, and the earlier count of different subsets now comes from the skip rule and not from a hash set.

#### [Boundary] Equal Values At Different Depths (Author exercise)
<!-- id: bt-equal-values-different-depths -->

**Prerequisites.** The two exercises above.

**Problem.** The array `nums` holds integers in nondecreasing order, `v` is an integer and `m` is a non-negative integer. Return every different subset of `nums` that holds the value `v` exactly `m` times. A subset may hold several copies of `v` only when `nums` holds that many copies. The output order follows the order of the calls.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 12`.
- **Values** satisfy `-5 <= nums[i] <= 5`, and the values never decrease along the array.
- **Count** is `0 <= m <= 12`, and `v` may be absent from `nums`.
- **Empty result** is an empty list when no subset has exactly `m` copies of `v`.

**Example 1.** Input `nums = [2,2,3]`, `v = 2`, `m = 2`, output `[[2,2],[2,2,3]]`.

**Example 2.** Input `nums = [1,1]`, `v = 1`, `m = 0`, output `[[]]`.

**Hint.** Which comparison keeps `[2, 2]` reachable? What does the check `i > 0` remove from the output?

**Changed decision.** A filter on the count of one value makes a wrong skip rule visible, because every result with two copies depends on equal values at different depths.

#### [Recognize] Combination Sum II (LeetCode 40)
<!-- id: bt-combination-sum-two -->

**Prerequisites.** The previous three exercises.

**Problem.** The array `candidates` holds positive integers that may repeat, and `target` is a positive integer. Return every different list of candidates that adds up to `target`. Each index serves at most once, so a list may hold a value only as often as `candidates` does. Two lists are different when their sorted lists differ. Each list follows the sorted order, and the result keeps the search order.

**Constraints.** The limits are:
- **Length** is `1 <= candidates.length <= 14`.
- **Values** satisfy `1 <= candidates[i] <= 12`, and equal values may repeat.
- **Target** is `1 <= target <= 40`.
- **Mutation** does not occur; `candidates` keeps its order.

**Example 1.** Input `candidates = [3,1,3,2,2]`, `target = 5`, output `[[1,2,2],[2,3]]`.

**Example 2.** Input `candidates = [2,2,2]`, `target = 4`, output `[[2,2]]`.

**Hint.** Which two checks does a call need, one for the remaining target and one for equal siblings? Why can the loop stop at a candidate above the remaining target?

**Changed decision.** The search keeps the remaining target and the same-level check, and every index serves at most once.
