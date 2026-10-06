<!-- lesson-kind: standard -->
<!-- lesson-id: increasing-start-combinations -->
## Choose K Values Without Reordering

<!-- stage: context -->
### Why Sixty Review Panels Exist For Ten

A review tool must list every panel of three engineers that it can assign to a change. The company has five engineers. The developer reuses the ordering search from the previous lesson and stops each path at length three. The tool then shows 60 panels, and the reviewers see that `Ana, Ben, Cho` and `Ben, Ana, Cho` name the same panel. Only 10 different panels exist.

A panel is a selection, and the order of its members carries no meaning. This lesson asks how a search lists each selection of `k` values exactly once, and how it avoids calls that cannot reach `k` values.

<!-- stage: naive -->
### Building Every Ordering And Merging Equal Panels

The direct plan runs the ordering search and stops each path at `k` values. It sorts a copy of every full path and keeps one copy of each sorted list in a set.

```java
static void panels(int[] a, int k, boolean[] used, List<Integer> path, Set<List<Integer>> seen) {
    if (path.size() == k) {
        List<Integer> key = new ArrayList<>(path);
        Collections.sort(key);                                 // equal panels get one sorted form
        seen.add(key);                                         // the set drops the repeats
        return;
    }
    for (int i = 0; i < a.length; i++) {
        if (used[i]) continue;                                 // each person serves once per path
        used[i] = true; path.add(a[i]);
        panels(a, k, used, path, seen);
        path.remove(path.size() - 1); used[i] = false;         // undo both pieces of state
    }
}
```

The method finds every panel, because each panel appears in every one of its orders. It builds all of those orders.

<!-- stage: bottleneck -->
### Counting The Repeated Panels

```predict
A company has n = 10 engineers, and each panel holds k = 4 of them. How many ordered paths does the search build, and how many different panels exist? Write C(10, 4) for the number of ways to pick 4 of 10.

The search builds 10 * 9 * 8 * 7 = 5,040 ordered paths. Only C(10, 4) = 210 panels exist. Every panel appears in 4! = 24 orders, so the search does 24 times the necessary work.
```

The search builds n!/(n-k)! paths, which costs O(k * n!/(n-k)!) time with the copies. The count C(n, k) = n!/(k!(n-k)!) would suffice. The waste factor is k!, which reaches 40,320 at k = 8. Each repeated path also costs a sort and a hash.

A panel needs one fixed order, and the input order is the natural choice. A path that lists indices from low to high gives every panel exactly one order. The search only needs to remember where the last choice came from.

<!-- stage: insight -->
### Moving Forward After Every Choice

#### Passing The Next Start

A call that chooses index `i` calls itself with the **next start** `i + 1`. The child loop begins at that index, so every later choice uses a higher index than every earlier choice. The path lists increasing indices, and each selection of indices has one such list.

#### Stopping At The Target Size

The **target size** is the number `k` of values that one result holds. A call stores a copy of its path when the path reaches `k` values, and it makes no further calls. Unlike the subset search, a call with fewer than `k` values stores nothing, because only full-size paths are results.

#### Ending The Loop Early

The **last useful index** at a call is the highest index that can still lead to a result. A path with `s` values needs `k - s` more values, and those values need `k - s` different indices from `i` up to `n - 1`. So the index `i` is useful only when `n - i >= k - s`, which gives `i <= n - (k - s)`. Above that index, every child ends with too few values. Those calls only waste time. The invariant is that every index in a path is higher than the one before it, and the path can still reach `k` values.

<!-- names: next start, target size, last useful index -->

<!-- stage: variables -->
### The Pieces Of State

Four pieces of state describe a call.

- **Start** is the smallest index that the next choice may take.
- **Path** is the shared list of chosen values, in increasing index order.
- **Size** is the number of values on the path, and it grows by one per call.
- **Last** is the highest index that the loop may choose, equal to `n - (k - size)`.

The loop runs from `start` to `last`. A call with a full path stores a copy and returns.

<!-- stage: trace -->
### Following The Start Through Four Values

#### Choosing Two From Four

The first trace lists the pairs of `[1, 2, 3, 4]` with the code of this lesson changed so that `last` is always `n - 1`. The pointer `start` is the start of the call that makes the choice. The variable `path` holds the values chosen so far, and `stored` counts the pairs in the output.

The call with start 0 chooses 1, and the child with start 1 chooses 2, 3 and 4 in turn. Each choice completes a pair, so the child stores three pairs. The root then chooses 2 and 3 in the same way. The last root choice, 4, passes next start 4. The child has no index left, so it returns with a path of one value and stores nothing. The trace shows 10 choices and 6 pairs.

#### Choosing Three With The Last Useful Index

The second trace lists the triples of `[1, 2, 3, 4]` with the early end. The root loop stops at index 1, because a triple that starts at index 2 would need three indices from a range of two. The trace makes 9 choices and stores 4 triples, and no choice leads to a call with too few indices.

#### Stepping Through Both Runs

```trace
{"cells":["1","2","3","4"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"path":"1","stored":0},"note":"The call with start 0 chooses 1, so the path becomes [1]."},{"at":{"start":1},"vars":{"path":"1,2","stored":1},"note":"The call with start 1 chooses 2, so the path becomes [1,2]. The path has the target size, so the call stores a copy."},{"at":{"start":1},"vars":{"path":"1,3","stored":2},"note":"The call with start 1 chooses 3, so the path becomes [1,3]. The path has the target size, so the call stores a copy."},{"at":{"start":1},"vars":{"path":"1,4","stored":3},"note":"The call with start 1 chooses 4, so the path becomes [1,4]. The path has the target size, so the call stores a copy."},{"at":{"start":0},"vars":{"path":"2","stored":3},"note":"The call with start 0 chooses 2, so the path becomes [2]."},{"at":{"start":2},"vars":{"path":"2,3","stored":4},"note":"The call with start 2 chooses 3, so the path becomes [2,3]. The path has the target size, so the call stores a copy."},{"at":{"start":2},"vars":{"path":"2,4","stored":5},"note":"The call with start 2 chooses 4, so the path becomes [2,4]. The path has the target size, so the call stores a copy."},{"at":{"start":0},"vars":{"path":"3","stored":5},"note":"The call with start 0 chooses 3, so the path becomes [3]."},{"at":{"start":3},"vars":{"path":"3,4","stored":6},"note":"The call with start 3 chooses 4, so the path becomes [3,4]. The path has the target size, so the call stores a copy."},{"at":{"start":0},"vars":{"path":"4","stored":6},"note":"The call with start 0 chooses 4, so the path becomes [4]. The next start is 4, so the child has no index left and stores nothing."}]}
```

```trace
{"cells":["1","2","3","4"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"path":"1","stored":0},"note":"The call with start 0 chooses 1, so the path becomes [1]."},{"at":{"start":1},"vars":{"path":"1,2","stored":0},"note":"The call with start 1 chooses 2, so the path becomes [1,2]."},{"at":{"start":2},"vars":{"path":"1,2,3","stored":1},"note":"The call with start 2 chooses 3, so the path becomes [1,2,3]. The path has the target size, so the call stores a copy."},{"at":{"start":2},"vars":{"path":"1,2,4","stored":2},"note":"The call with start 2 chooses 4, so the path becomes [1,2,4]. The path has the target size, so the call stores a copy."},{"at":{"start":1},"vars":{"path":"1,3","stored":2},"note":"The call with start 1 chooses 3, so the path becomes [1,3]."},{"at":{"start":3},"vars":{"path":"1,3,4","stored":3},"note":"The call with start 3 chooses 4, so the path becomes [1,3,4]. The path has the target size, so the call stores a copy."},{"at":{"start":0},"vars":{"path":"2","stored":3},"note":"The call with start 0 chooses 2, so the path becomes [2]."},{"at":{"start":2},"vars":{"path":"2,3","stored":3},"note":"The call with start 2 chooses 3, so the path becomes [2,3]."},{"at":{"start":3},"vars":{"path":"2,3,4","stored":4},"note":"The call with start 3 chooses 4, so the path becomes [2,3,4]. The path has the target size, so the call stores a copy."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### Combinations With An Early End

The method below stops each loop at the last useful index, which the call computes from the size of the path.

```java
static void go(int start, int k, int[] nums, List<Integer> path, List<List<Integer>> out) {
    if (path.size() == k) {                              // the target size is reached
        out.add(new ArrayList<>(path));                  // store a copy and make no more calls
        return;
    }
    int last = nums.length - (k - path.size());          // highest index that can still finish
    for (int i = start; i <= last; i++) {                // later indices cannot reach k values
        path.add(nums[i]);                               // choose index i
        go(i + 1, k, nums, path, out);                   // the next start is one past this index
        path.remove(path.size() - 1);                    // undo the choice
    }
}
```

#### Cost Of The Search

The search stores C(n, k) results, and each copy costs O(k), so the time is O(k * C(n, k)). With the early end, every call extends to at least one result, so the number of calls stays within a factor of k of the number of results. The path and the stack use O(k) memory.

<!-- stage: applicability -->
### Recognizing A Selection Problem

#### Spotting The Pattern

The cue is a request for `k` values from a collection with no meaning attached to their order. The invariant is that every path lists strictly increasing indices, so each selection has one path, and the path can still grow to `k` values.

#### Finding The False Friend

The false friend is a used array. It lets any later call pick an index below an earlier choice, so the search lists `[1, 2]` and `[2, 1]` as two results. A second false friend is a loop that ends at the last index of the input, which is correct but builds many calls that end with too few values.

#### Recognizing The No-Go Cases

The search does not fit when the input has equal values and the output must hold each selection once, because equal values produce repeated paths. It does not fit when the question asks only for the number of selections. The formula C(n, k) answers that question directly. A large `k` near `n` is better handled by choosing the values to leave out.

<!-- stage: exercises -->
### Exercises

#### [Build] Choose Two From Four (Author exercise)
<!-- id: bt-choose-two-from-four -->

**Prerequisites.** The next start and the target size of this lesson.

**Problem.** Given an array `nums` of exactly four distinct integers, return every list of two of its values. A list keeps the order of `nums`, and each pair of indices produces one list. Search with a start index and stop each path at two values. The result lists the pairs in the order in which the search reaches them.

**Constraints.** The limits are:
- **Length** is exactly 4.
- **Values** are distinct integers with `-100 <= nums[i] <= 100`.
- **Count** of lists is exactly 6.
- **Mutation** does not occur; `nums` keeps its order.

**Example 1.** Input `nums = [1,2,3,4]`, output `[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]`.

**Example 2.** Input `nums = [9,0,5,2]`, output `[[9,0],[9,5],[9,2],[0,5],[0,2],[5,2]]`.

**Hint.** Which start does the child of the choice at index 1 receive? Which pairs does a root choice at index 3 produce?

**Changed decision.** A path stops at a fixed size, and the next start is one past the chosen index.

#### [Vary] Combinations (LeetCode 77)
<!-- id: bt-combinations-n-choose-k -->

**Prerequisites.** The previous exercise.

**Problem.** Given integers `n` and `k`, return every list of `k` different numbers chosen from `1` to `n`. Each list is in increasing order. The result lists the lists in the order in which a search with a start index reaches them. The size `k` is a parameter, so the same method serves every size from 0 to `n`.

**Constraints.** The limits are:
- **Range** is `1 <= n <= 12`.
- **Size** is `0 <= k <= n`.
- **Count** of lists is the binomial coefficient of `n` and `k`.
- **Empty list** is the only result when `k = 0`.

**Example 1.** Input `n = 4`, `k = 3`, output `[[1,2,3],[1,2,4],[1,3,4],[2,3,4]]`.

**Example 2.** Input `n = 3`, `k = 0`, output `[[]]`.

**Hint.** What does a call do when the path already holds `k` values? Which numbers does the call at start `s` try?

**Changed decision.** The target size is a parameter, and the values come from a numeric range and not from an array.

#### [Boundary] Insufficient Remaining Values (Author exercise)
<!-- id: bt-insufficient-remaining -->

**Prerequisites.** The two exercises above.

**Problem.** Run the combination search on the numbers `1` to `n` with target size `k`. Each loop stops at the last useful index. Return the number of calls that the search makes, and count the root call. A call that stores a result and a call that has no loop iteration are both calls.

**Constraints.** The limits are:
- **Range** is `0 <= n <= 20`.
- **Size** is `0 <= k <= 25`, and `k` may exceed `n`.
- **Return** is a `long`.
- **Empty case** `n = 0` still makes the root call.

**Example 1.** Input `n = 4`, `k = 2`, output 10.

**Example 2.** Input `n = 3`, `k = 5`, output 1.

**Hint.** What is the last useful index at the root when `k > n`? Which calls does the early end remove from the search of `n = 4`, `k = 2`?

**Changed decision.** The method counts calls, so the loop bound is the only thing that changes the answer.

#### [Recognize] Combination Sum III (LeetCode 216)
<!-- id: bt-combination-sum-three -->

**Prerequisites.** The previous three exercises.

**Problem.** Given integers `k` and `n`, return every list of exactly `k` different digits from `1` to `9` that adds up to `n`. A digit appears at most once in a list, and each list is increasing. The order of the result follows the order of the search.

**Constraints.** The limits are:
- **Size** is `1 <= k <= 9`.
- **Sum** is `1 <= n <= 60`.
- **Digits** are `1` to `9`, and no digit repeats in one list.
- **Empty result** is an empty list when no list adds up to `n`.

**Example 1.** Input `k = 2`, `n = 5`, output `[[1,4],[2,3]]`.

**Example 2.** Input `k = 4`, `n = 1`, output `[]`.

**Hint.** Which value tells the call how much sum is still needed? When does a full path fail?

**Changed decision.** The search keeps a remaining sum next to the start. The search stores a full path only when that sum is 0.
