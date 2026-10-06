<!-- lesson-kind: standard -->
<!-- lesson-id: subsets -->
## List Every Subset

<!-- stage: context -->
### Why The Role Test Lists Duplicates

A permissions screen offers three roles: `admin`, `editor` and `viewer`. A test must try every set of roles that one user can hold. The developer writes a search that tries any role at any step. The test report then lists `editor, admin` and `admin, editor` as two plans, although both give the user the same roles.

A user holds a set of roles, so the order of the roles carries no meaning. This lesson asks how a search lists each set exactly once, and why such a search can record a result at every call and not only at the end.

<!-- stage: naive -->
### Trying Every Order And Removing Repeats

The direct plan lets each step pick any role that the path has not used. At every call it sorts a copy of the path and stores the copy in a hash set, which removes the repeated sets.

```java
static void collect(int[] a, boolean[] used, List<Integer> path, Set<List<Integer>> seen) {
    List<Integer> key = new ArrayList<>(path);
    Collections.sort(key);                                   // equal sets get one sorted form
    seen.add(key);                                           // the set drops repeats
    for (int i = 0; i < a.length; i++) {
        if (used[i]) continue;                               // each index serves at most once per path
        used[i] = true; path.add(a[i]);                      // choose any unused index
        collect(a, used, path, seen);
        path.remove(path.size() - 1); used[i] = false;       // undo both pieces of state
    }
}
```

The method finds every set, because every set appears in at least one order. It also visits every order of every set.

<!-- stage: bottleneck -->
### Counting The Calls For Ten Roles

```predict
The array holds n = 10 values. The search makes one call for every ordered list of distinct values, including the empty list. About how many calls does it make, and how many sets exist?

The count is 10!/10! + 10!/9! + ... + 10!/0!, which is about 9.9 million calls. Only 2^10 = 1,024 sets exist, so about 9,600 calls belong to each set. Each call also sorts a copy of its path.
```

The search makes about e * n! calls, and each call adds a sort of O(n log n) time. The extra calls repeat orders, and the search finishes the work before the hash set discards them.

A set has one canonical order, which is the order of the indices in the input. A search that only builds paths in that order never builds a repeated set, so it needs no sort and no hash set. The question is how to make the path follow the input order.

<!-- stage: insight -->
### Choosing Only Later Indices

#### Moving The Start Forward

Each call receives a **start index**, the smallest index that the next choice may use. The root call has start 0. After a call chooses index `i`, it calls itself with start `i + 1`. Every path is then a strictly increasing list of indices, so a set can appear in one order only.

#### Counting Skipped Indices

The values at indices between the old start and the chosen index are the **skipped indices**. The call that chooses index `i` decides that those values stay out of the set, and no later call may add them. This is the same decision as the exclusion branch of the include-or-exclude search from the previous lesson. The invariant is that at start `s`, the path fixes the decision for every index below `s`, and indices from `s` on stay undecided.

#### Recording On Entry

Every path of increasing indices is already a complete subset, so no call needs to wait for a leaf. A call stores a copy of its path at **record on entry**, before its loop starts. The root stores the empty subset. The search stores each path once. The tree has exactly one node for each of the 2^n subsets, because a sorted list of indices names one subset.

<!-- names: start index, skipped indices, record on entry -->

<!-- stage: variables -->
### The Pieces Of State

A call and the search hold four pieces of state.

- **Start** is the first index that the loop of the call may choose.
- **Index i** is the index that the loop tries, with `start <= i < n`.
- **Path** is the shared list of the chosen values in increasing index order.
- **Output** is the list of snapshots that each call stores on entry.

Choosing index `i` raises the start of the child call to `i + 1`. The loop in a call with start `n` has no iteration, so that call only records its path and returns.

<!-- stage: trace -->
### Following The Start Index

#### Listing Every Subset Of Three Values

The first trace lists the subsets of `[1, 2, 3]`. The pointer `start` marks the start index of the current call, and the variable `path` shows the path. Each step is one entry into a call. The variable `stored` counts the snapshots that exist after the step.

The root call has start 0 and stores the empty subset. It chooses index 0, and the call with start 1 stores `[1]`. That call chooses index 1 and then index 2, which stores `[1, 2]` and `[1, 2, 3]`. The path `[1, 3]` appears next, because the call for `[1]` also tries index 2. The root then tries index 1 and index 2, and the trace ends with `[2]`, `[2, 3]` and `[3]`. The trace stores 8 subsets, which equals 2^3.

#### Counting Calls Without A Start Index

The second trace runs the plan that lets every step pick any unused index on the array `[1, 2]`. It makes 5 calls and stores the sorted path in each. The sets `[1, 2]` appear twice, once from each order, so the hash set holds only 4 sets from 5 calls.

#### Stepping Through Both Runs

```trace
{"cells":["1","2","3"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"path":"empty","stored":1},"note":"The root call with start 0 stores the empty subset."},{"at":{"start":1},"vars":{"path":"1","stored":2},"note":"The call with start 1 stores the subset [1]."},{"at":{"start":2},"vars":{"path":"1,2","stored":3},"note":"The call with start 2 stores the subset [1,2]."},{"at":{"start":3},"vars":{"path":"1,2,3","stored":4},"note":"The call with start 3 stores the subset [1,2,3]."},{"at":{"start":3},"vars":{"path":"1,3","stored":5},"note":"The call with start 3 stores the subset [1,3]."},{"at":{"start":2},"vars":{"path":"2","stored":6},"note":"The call with start 2 stores the subset [2]."},{"at":{"start":3},"vars":{"path":"2,3","stored":7},"note":"The call with start 3 stores the subset [2,3]."},{"at":{"start":3},"vars":{"path":"3","stored":8},"note":"The call with start 3 stores the subset [3]."}]}
```

```trace
{"cells":["1","2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"path":"empty","set size":1},"note":"Call 1 holds the path [empty], and its sorted form is new, so the hash set grows."},{"at":{"i":1},"vars":{"path":"1","set size":2},"note":"Call 2 holds the path [1], and its sorted form is new, so the hash set grows."},{"at":{"i":2},"vars":{"path":"1,2","set size":3},"note":"Call 3 holds the path [1,2], and its sorted form is new, so the hash set grows."},{"at":{"i":1},"vars":{"path":"2","set size":4},"note":"Call 4 holds the path [2], and its sorted form is new, so the hash set grows."},{"at":{"i":2},"vars":{"path":"2,1","set size":4},"note":"Call 5 holds the path [2,1], and its sorted form is already in the hash set, so the call was wasted."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### Subsets With A Start Index

The method stores the path on entry, then tries each later index. Its undo step is the same removal as in the previous lesson.

```java
static List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    go(0, nums, new ArrayList<>(), out);
    return out;
}

static void go(int start, int[] nums, List<Integer> path, List<List<Integer>> out) {
    out.add(new ArrayList<>(path));                    // record on entry: the path is a complete subset
    for (int i = start; i < nums.length; i++) {        // only indices at or after start
        path.add(nums[i]);                             // choose index i
        go(i + 1, nums, path, out);                    // the next start skips every index up to i
        path.remove(path.size() - 1);                  // undo the choice
    }
}
```

#### Cost Of The Search

The search makes 2^n calls, one for each subset, and each call copies a path of up to n values. The time is O(n * 2^n), and the output needs O(n * 2^n) values. The path and the stack use O(n) memory. The plan with every order costs O(n! * n log n) time, which is far larger.

<!-- stage: applicability -->
### Recognizing A Set Of Choices

#### Spotting The Pattern

The cue is a question about every selection of elements where the order inside a selection carries no meaning. The invariant is that every path is an increasing list of indices, so each selection has exactly one path.

#### Finding The False Friend

The false friend is the state of the next lesson. A search that marks used indices and picks any unused one at each step builds ordered lists, so it produces `[1, 2]` and `[2, 1]` as two results. A fixed order is the property that separates a set from an arrangement.

#### Recognizing The No-Go Cases

The search does not fit when the output is too large to list, because 2^n subsets reach millions at n = 25. It does not fit when a direct formula gives the one subset that the question needs. A question about a count of subsets with a given sum usually needs a different method.

<!-- stage: exercises -->
### Exercises

#### [Build] Subsets Of Two Values (Author exercise)
<!-- id: bt-subsets-of-two-values -->

**Prerequisites.** The start index and the record on entry of this lesson.

**Problem.** Given an array `nums` of at most two distinct integers, return every subset of `nums`. Use a recursive method that receives a start index and stores a copy of the path when a call begins. The result lists the subsets in the order in which the calls begin. Each subset keeps the order of `nums`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 2`.
- **Values** are distinct integers with `-100 <= nums[i] <= 100`.
- **Count** of subsets is exactly `2^nums.length`.
- **Empty input** returns one subset.

**Example 1.** Input `nums = [5, 7]`, output `[[],[5],[5,7],[7]]`.

**Example 2.** Input `nums = [9]`, output `[[],[9]]`.

**Hint.** How many calls does the search make for two values? Which start does the call for `[5]` receive?

**Changed decision.** Every call stores a result, and the loop over later indices replaces the include-or-exclude branch.

#### [Vary] Subsets (LeetCode 78)
<!-- id: bt-subsets-start-index -->

**Prerequisites.** The previous exercise.

**Problem.** Given an array `nums` of distinct integers, return every subset of `nums`. Search with a start index and store a copy of the path at the beginning of every call. The result lists the subsets in the order in which the calls begin, which differs from the order of the include-or-exclude search of the previous lesson.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10`.
- **Values** are distinct integers with `-10 <= nums[i] <= 10`.
- **Count** of subsets is exactly `2^nums.length`.
- **Mutation** does not occur; `nums` keeps its order.

**Example 1.** Input `nums = [1,2,3]`, output `[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]`.

**Example 2.** Input `nums = [4,0]`, output `[[],[4],[4,0],[0]]`.

**Hint.** Which subsets does the call for `[1]` store, and in which order? What start does the root pass to its first child?

**Changed decision.** The search stores a result at every call, and the output order follows entry order, not leaf order.

#### [Boundary] Empty Input (Author exercise)
<!-- id: bt-subsets-empty-input -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums` that may be empty and an integer `target`, return every subset of `nums` whose values add up to `target`. The empty subset adds up to 0. The result lists the subsets in the order in which a search with a start index begins its calls. The values may be negative, so the search does not stop early.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 12`.
- **Values** are distinct integers with `-20 <= nums[i] <= 20`.
- **Target** is `-100 <= target <= 100`.
- **Empty result** is an empty list when no subset reaches `target`.

**Example 1.** Input `nums = []`, `target = 0`, output `[[]]`.

**Example 2.** Input `nums = [1,2,3]`, `target = 3`, output `[[1,2],[3]]`.

**Hint.** What does the root call store when `nums` is empty? Which result differs between target 0 and target 1?

**Changed decision.** The check against `target` runs at every call, and the empty path is a valid candidate.

#### [Recognize] Subsets II Count (LeetCode 90)
<!-- id: bt-subsets-distinct-count -->

**Prerequisites.** The previous three exercises.

**Problem.** Given an integer array `nums` that may hold equal values, return the number of different subsets. Two subsets are the same when they hold the same values with the same multiplicities, whatever the indices are. The empty subset counts once. The method may sort `nums` first.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 12`.
- **Values** are integers with `-10 <= nums[i] <= 10`.
- **Return** is an `int`.
- **Mutation** may reorder a copy of `nums`, and the caller's array keeps its order.

**Example 1.** Input `nums = [1,2,2]`, output 6.

**Example 2.** Input `nums = [3,3,3]`, output 4.

**Hint.** After sorting, equal values sit next to each other. What do two equal subsets look like as sorted lists, and which data structure removes copies of equal lists?

**Changed decision.** Equal values create repeated subsets, so the program counts distinct sorted lists. A later lesson shows how to skip the repeats during the search.
