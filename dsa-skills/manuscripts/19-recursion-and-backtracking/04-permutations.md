<!-- lesson-kind: standard -->
<!-- lesson-id: permutations -->
## List Every Ordering

<!-- stage: context -->
### Why The Test Never Sees Reversed Input

A test must prove that a sorting method works on every ordering of four distinct values. The developer reuses the subset search from the previous lesson. The search lists `[1, 2, 3, 4]` and its sublists, and it never lists `[4, 3, 2, 1]`, because each choice may only use a later index. The reversed input is the one that exposes the bug, and the test passes without ever running it.

An ordering uses every value once, and any value may come first. This lesson asks how a search fills each position of the output with any value that no earlier position holds, and how it lists every ordering exactly once.

<!-- stage: naive -->
### Building Every Sequence And Rejecting Repeats

The direct plan lets every position take any value from the array. When a sequence reaches full length, the method rejects it if a value appears twice.

```java
static void tryAll(int[] a, List<Integer> path, List<List<Integer>> out) {
    if (path.size() == a.length) {
        if (new HashSet<>(path).size() == path.size()) out.add(new ArrayList<>(path));   // reject a sequence with a repeated value
        return;
    }
    for (int v : a) {                                            // every value may fill this position
        path.add(v);
        tryAll(a, path, out);
        path.remove(path.size() - 1);                            // undo the choice
    }
}
```

The method lists every ordering of distinct values, because each ordering is one of the sequences that it builds. It builds many sequences that it then throws away.

<!-- stage: bottleneck -->
### Counting The Rejected Sequences

```predict
The array holds n = 8 distinct values. How many full-length sequences does the search build, and how many of them are orderings?

The search builds 8^8 = 16,777,216 sequences, because each of the 8 positions has 8 candidates. Only 8! = 40,320 of them hold 8 different values. About 416 sequences are built for each ordering, and each one still costs a set to check.
```

The search costs O(n^n * n) time, and an answer needs only O(n! * n). The ratio n^n / n! grows faster than any fixed power of n, so the waste explodes with the input size.

The rejection happens at the leaf, after the search already placed a repeated value. A repeated value is visible earlier. The search can ask at each position whether a value is already on the path, and it can skip that value at once. The skipped branches then never exist.

<!-- stage: insight -->
### Marking The Values Already Placed

#### Filling One Position Per Call

The depth of a call equals the **output position** that the call fills. The root fills position 0, its children fill position 1, and a call at depth `n` has filled every position. Every call loops over all indices, because any value may fill the position. The loop skips only the indices that earlier positions hold.

#### Remembering Which Indices Are Placed

The **used array** has one boolean for each index of the input. The entry `used[i]` is true while index `i` sits on the current path. A call chooses index `i` only when `used[i]` is false. After the choice it sets `used[i]` to true, adds the value to the path and calls itself. Marking by index and not by value keeps equal values apart.

#### Clearing The Mark On Return

The **mark restoration** has two parts: the call removes the last entry of the path and sets `used[i]` back to false. The two parts must run together. If the path shrinks and the mark stays true, the sibling branches treat index `i` as taken, and the search loses orderings. The invariant is that at depth `d`, the path holds `d` values and the used array has exactly `d` true entries, one for each index on the path.

<!-- names: output position, used array, mark restoration -->

<!-- stage: variables -->
### The Pieces Of State

Four pieces of state describe a call.

- **Depth** is the number of values on the path, and it equals the next output position.
- **Path** is the shared list of values placed so far.
- **Used array** holds one boolean per input index, true when the index is on the path.
- **Index i** is the input index that the loop tries at this depth.

The depth grows by one in each call. The search stores a copy of the path when the depth reaches `n`. The tree has n! leaves and about e * n! calls in total.

<!-- stage: trace -->
### Following The Marks Through Three Values

#### Listing All Six Orderings

The first trace lists the orderings of `[1, 2, 3]`. Each step is one choice. The pointer `i` marks the input index that the choice uses. The variable `path` lists the values placed so far, and `used` shows the three marks as `T` or `F`.

The first branch picks index 0 and then index 1, and then index 2 completes `[1, 2, 3]`. After the return, the mark of index 2 clears, and the loop at depth 2 finds no other free index. The loop at depth 1 then tries index 2, and index 1 is free again, so `[1, 3, 2]` follows. Then the root repeats the same steps for the first values 2 and 3. The trace has 15 choices and ends with `[3, 2, 1]`.

#### Tracing A Mark That Stays

The second trace uses two values and a search that removes the path entry but forgets to clear the mark. The first leaf stores `[1, 2]`. The two returns shrink the path to empty, and both marks stay true. The loop at depth 0 then finds no free index, so the search ends and never stores `[2, 1]`.

#### Stepping Through Both Runs

```trace
{"cells":["1","2","3"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"path":"1","used":"TFF"},"note":"The call at depth 0 chooses index 0, so the path becomes [1]."},{"at":{"i":1},"vars":{"path":"1,2","used":"TTF"},"note":"The call at depth 1 chooses index 1, so the path becomes [1,2]."},{"at":{"i":2},"vars":{"path":"1,2,3","used":"TTT"},"note":"The call at depth 2 chooses index 2, so the path becomes [1,2,3]. The path is full, so the leaf stores a copy."},{"at":{"i":2},"vars":{"path":"1,3","used":"TFT"},"note":"The call at depth 1 chooses index 2, so the path becomes [1,3]."},{"at":{"i":1},"vars":{"path":"1,3,2","used":"TTT"},"note":"The call at depth 2 chooses index 1, so the path becomes [1,3,2]. The path is full, so the leaf stores a copy."},{"at":{"i":1},"vars":{"path":"2","used":"FTF"},"note":"The call at depth 0 chooses index 1, so the path becomes [2]."},{"at":{"i":0},"vars":{"path":"2,1","used":"TTF"},"note":"The call at depth 1 chooses index 0, so the path becomes [2,1]."},{"at":{"i":2},"vars":{"path":"2,1,3","used":"TTT"},"note":"The call at depth 2 chooses index 2, so the path becomes [2,1,3]. The path is full, so the leaf stores a copy."},{"at":{"i":2},"vars":{"path":"2,3","used":"FTT"},"note":"The call at depth 1 chooses index 2, so the path becomes [2,3]."},{"at":{"i":0},"vars":{"path":"2,3,1","used":"TTT"},"note":"The call at depth 2 chooses index 0, so the path becomes [2,3,1]. The path is full, so the leaf stores a copy."},{"at":{"i":2},"vars":{"path":"3","used":"FFT"},"note":"The call at depth 0 chooses index 2, so the path becomes [3]."},{"at":{"i":0},"vars":{"path":"3,1","used":"TFT"},"note":"The call at depth 1 chooses index 0, so the path becomes [3,1]."},{"at":{"i":1},"vars":{"path":"3,1,2","used":"TTT"},"note":"The call at depth 2 chooses index 1, so the path becomes [3,1,2]. The path is full, so the leaf stores a copy."},{"at":{"i":1},"vars":{"path":"3,2","used":"FTT"},"note":"The call at depth 1 chooses index 1, so the path becomes [3,2]."},{"at":{"i":0},"vars":{"path":"3,2,1","used":"TTT"},"note":"The call at depth 2 chooses index 0, so the path becomes [3,2,1]. The path is full, so the leaf stores a copy."}]}
```

```trace
{"cells":["1","2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"path":"1","used":"TF"},"note":"The call at depth 0 chooses index 0, so the path becomes [1]."},{"at":{"i":1},"vars":{"path":"1,2","used":"TT"},"note":"The call at depth 1 chooses index 1, so the path becomes [1,2]. The path is full, so the leaf stores a copy."},{"at":{"i":1},"vars":{"path":"1","used":"TT"},"note":"The undo step removes the value of index 1 from the path but leaves its mark true."},{"at":{"i":0},"vars":{"path":"empty","used":"TT"},"note":"The undo step removes the value of index 0 from the path but leaves its mark true."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### The Search With A Used Array

The method fills one position per call and restores both pieces of state after each branch.

```java
static void go(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> out) {
    if (path.size() == nums.length) {                  // every output position is filled
        out.add(new ArrayList<>(path));                // store a copy of the full ordering
        return;
    }
    for (int i = 0; i < nums.length; i++) {            // any index may fill this position
        if (used[i]) continue;                         // skip indices that earlier positions hold
        used[i] = true; path.add(nums[i]);             // choose: mark the index and add its value
        go(nums, used, path, out);                     // explore the remaining positions
        path.remove(path.size() - 1); used[i] = false; // restore both pieces of state
    }
}
```

#### Swapping Values In Place

The same search can reorder the input array itself. At depth `d`, the loop swaps `nums[d]` with `nums[i]` for each `i` from `d` to the end, recurses with depth `d + 1` and swaps back. The prefix `nums[0..d)` plays the role of the path, and the suffix plays the role of the free indices. This version needs no used array and no path list, and it lists the orderings in a different order.

```java
static void swapGo(int[] a, int d, List<List<Integer>> out) {
    if (d == a.length) {                                 // the whole array is one ordering
        List<Integer> copy = new ArrayList<>();
        for (int v : a) copy.add(v);
        out.add(copy);
        return;
    }
    for (int i = d; i < a.length; i++) {
        int t = a[d]; a[d] = a[i]; a[i] = t;             // place a[i] at position d
        swapGo(a, d + 1, out);
        t = a[d]; a[d] = a[i]; a[i] = t;                 // swap back to restore the array
    }
}
```

#### Cost Of The Search

The search makes about e * n! calls, and each leaf copies n values. The time is O(n * n!). The used array, the path and the stack use O(n) memory besides the output.

<!-- stage: applicability -->
### Recognizing An Ordering Problem

#### Spotting The Pattern

The cue is an output that uses every element once and counts different positions as different results. The invariant is that the depth equals the number of filled positions and that the used array marks exactly the indices on the path.

#### Finding The False Friend

The false friend is the start index of the previous lesson. It keeps every path in increasing index order, so it lists combinations and never lists `[2, 1]`. A second false friend is the mark that stays after a return, which removes whole families of orderings and does not raise an error.

#### Recognizing The No-Go Cases

The search does not fit when the question wants one ordering, such as the next one in dictionary order. A direct algorithm finds that ordering in O(n). It does not fit when n exceeds 10 or 11, since n! passes tens of millions. An optimization over orderings needs a method that does not list them.

<!-- stage: exercises -->
### Exercises

#### [Build] Permute Three Distinct Values (Author exercise)
<!-- id: bt-permute-three -->

**Prerequisites.** The used array and the mark restoration of this lesson.

**Problem.** Given an array `nums` of exactly three distinct integers, return all six orderings of its values. The search fills one position per call. At each position it tries the indices from 0 to 2 and skips indices that an earlier position holds. The result keeps the order of the search.

**Constraints.** The limits are:
- **Length** is exactly 3.
- **Values** are distinct integers with `-100 <= nums[i] <= 100`.
- **Count** of orderings is exactly 6.
- **Mutation** does not occur; `nums` keeps its order.

**Example 1.** Input `nums = [1,2,3]`, output `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`.

**Example 2.** Input `nums = [7,-1,4]`, output `[[7,-1,4],[7,4,-1],[-1,7,4],[-1,4,7],[4,7,-1],[4,-1,7]]`.

**Hint.** How many marks are true when the call at depth 2 begins? Which index does the call at depth 2 choose in the first branch?

**Changed decision.** Any index may fill a position, and a boolean mark per index replaces the start index.

#### [Vary] Permutations (LeetCode 46)
<!-- id: bt-permutations-used-array -->

**Prerequisites.** The previous exercise.

**Problem.** The array `nums` holds distinct integers. Return all orderings of its values. Search with a used array and a shared path. The result lists the orderings in the order in which a search that tries indices from low to high reaches them. An empty array has one ordering, the empty list.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 8`.
- **Values** are distinct integers with `-10 <= nums[i] <= 10`.
- **Count** of orderings is exactly `nums.length` factorial.
- **Mutation** does not occur; `nums` keeps its order.

**Example 1.** Input `nums = [0,1]`, output `[[0,1],[1,0]]`.

**Example 2.** Input `nums = []`, output `[[]]`.

**Hint.** Which loop bounds does each call use? What does the call at depth `n` store?

**Changed decision.** The method accepts any length, and the empty input produces one result.

#### [Boundary] Restore Used State (Author exercise)
<!-- id: bt-restore-used-state -->

**Prerequisites.** The two exercises above.

**Problem.** The array `nums` holds distinct integers, and `k` is an integer. Return every list of exactly `k` values taken from different indices of `nums`. Two lists with the same values in a different order are different. The search stops at depth `k`, so it stores a path while some index is still free. The result lists the lists in the order of a search that tries indices from low to high.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 7`.
- **Values** are distinct integers with `-10 <= nums[i] <= 10`.
- **Size** is `0 <= k <= 9`, and a `k` above the length gives an empty result.
- **Empty list** is the only result when `k = 0`.

**Example 1.** Input `nums = [1,2,3]`, `k = 2`, output `[[1,2],[1,3],[2,1],[2,3],[3,1],[3,2]]`.

**Example 2.** Input `nums = [5]`, `k = 0`, output `[[]]`.

**Hint.** When the search stops at depth `k`, how many marks are true? Which mark must the call clear after it returns from the branch of index `i`?

**Changed decision.** The leaf appears before the path uses every index, so a missing restoration of one mark changes the result.

#### [Recognize] Permutations II (LeetCode 47)
<!-- id: bt-permutations-equal-values -->

**Prerequisites.** The previous three exercises.

**Problem.** Given an array `nums` that may hold equal values, return every different ordering of its values. Two orderings are the same when they hold the same value at every position. The result lists each ordering once, in the order in which a search that tries indices from low to high first reaches it.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 8`.
- **Values** are integers with `-5 <= nums[i] <= 5`, and equal values may repeat.
- **Count** of orderings is the factorial of the length divided by the factorials of the value counts.
- **Mutation** does not occur; `nums` keeps its order.

**Example 1.** Input `nums = [1,1,2]`, output `[[1,1,2],[1,2,1],[2,1,1]]`.

**Example 2.** Input `nums = [2,2]`, output `[[2,2]]`.

**Hint.** At one depth, two equal values build the same subtree twice. Which small set, local to one call, records the values that this call already tried?

**Changed decision.** Equal values may repeat in the output but may not repeat as sibling choices of one call.
