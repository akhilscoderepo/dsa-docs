<!-- lesson-kind: standard -->
<!-- lesson-id: proof-based-pruning -->
## Stop A Branch You Can Prove Fails

<!-- stage: context -->
### Why The Invoice Match Runs For Minutes

A finance tool matches a payment of 50 euros against 30 open invoices. It must find the sets of invoices that add up to exactly 50. Every invoice is at least 10 euros. The tool tries every set of invoices and compares the total at the end. On a laptop it runs for minutes, and most of that time goes to sets that hold twelve invoices and a total of several hundred euros.

A set that already exceeds 50 euros cannot shrink again, because every invoice adds a positive amount. This lesson asks how a search decides that a partial choice is hopeless, and what makes that decision safe instead of a guess.

<!-- stage: naive -->
### Checking The Total At The End

The direct plan runs the subset search and tests the sum of every finished path. It never looks at the sum while the path grows.

```java
static void match(int start, int[] a, List<Integer> path, int target, List<List<Integer>> out) {
    int sum = 0;
    for (int v : path) sum += v;                              // recompute the sum for this path
    if (sum == target) out.add(new ArrayList<>(path));        // test the total of every path
    for (int i = start; i < a.length; i++) {                  // every later invoice, whatever the sum is
        path.add(a[i]);
        match(i + 1, a, path, target, out);
        path.remove(path.size() - 1);                         // undo the choice
    }
}
```

The method finds every matching set, because it visits every set. It spends the same effort on a set that already exceeds the target.

<!-- stage: bottleneck -->
### Counting The Paths That Cannot Recover

```predict
The array holds n = 30 invoices, and each is at least 10. The target is 50. How many paths does the plan above visit, and how many paths have a total of at most 50?

The plan visits 2^30, about 1.07 billion paths. A path with 6 invoices or more totals at least 60, so only paths of 0 to 5 invoices can have a total of at most 50. At most C(30,0) + ... + C(30,5) = 174,437 such paths exist, less than 0.02 percent of the total.
```

The plan costs O(n * 2^n) time, and nearly all of it goes to paths that the target already rules out. A path with a total above 50 stays above 50 after every later choice. Its whole subtree holds no result, and the plan still visits every node of that subtree.

The search can test the total at each call and stop when the total passes the target. This test is safe only because of one fact about the data. The reason must be written down before the code skips anything.

<!-- stage: insight -->
### Skipping Only What A Proof Rules Out

#### Using A Rule That Never Recovers

A **monotone constraint** is a rule that later choices cannot repair. For positive values, the statement "the sum does not exceed the target" is monotone, because every added value raises the sum. Once a path breaks it, every extension of the path breaks it too, so the call may return at once. Sorted values allow a second stop. The loop ends at the first value above the remaining target, because all later values are larger.

#### Bounding What The Rest Can Reach

The **upper bound** of a path is the largest total that any extension can reach, and the **lower bound** is the smallest. For positive values and a fixed start, the upper bound adds every value from the start to the end. If the remaining target lies above that sum, no extension can reach it. The same reasoning with the number of slots left gives the lower and upper bounds for a choice of fixed size.

#### Writing The Proof First

Each skip needs a short sentence that says why no extension can succeed. The sentence names the fact that it needs. That fact is a positive value, a sorted array or a count of slots left. If the sentence needs a fact that the input does not guarantee, the skip is unsafe. The invariant is that every skipped branch contains no result, by a stated rule and not by an impression.

<!-- names: monotone constraint, upper bound, lower bound -->

<!-- stage: variables -->
### The Pieces Of State

Four pieces of state describe a call.

- **Start** is the lowest index that the loop may choose.
- **Remaining target** is the amount that the path still needs to add.
- **Suffix sum** at index `i` is the sum of the values from index `i` to the end, which serves as the upper bound.
- **Slots left** is the number of values that a fixed-size choice still needs.

The loop stops when the current value exceeds the remaining target, and the call returns when the suffix sum from the start is below the remaining target.

<!-- stage: trace -->
### Following The Proofs Through Four Values

#### Matching Ten With Sorted Values

The first trace searches the values `[3, 4, 6, 9]` for a set that adds up to 10. The pointer `start` is the start index of the call that acts, and the variable `remain` shows the remaining target after the choice. The variable `events` counts the choices made so far.

The root chooses 3, and the remaining target is 7. The call with start 1 chooses 4, and the remaining target is 3. The next value is 6, which exceeds 3, so the loop stops. Back at start 1, the loop chooses 6 and leaves the remaining target 1. The next call meets the value 9, which exceeds 1, so it stops. The loop at start 1 then meets 9 above its own remaining target 7 and stops too. The root chooses 4 and reaches the remaining target 6, and the value 6 completes the set `[4, 6]`.

#### Seeing A Negative Value Recover

The second trace uses the values `[5, -3]` and the target 2. The root first checks that the target lies inside the range of reachable totals. The choice of 5 then gives the remaining target minus 3, which a positive rule would call an overshoot. The next value is minus 3, which brings the remaining target to 0. The set `[5, -3]` adds up to 2. A skip after the first choice would have lost it.

#### Stepping Through Both Runs

```trace
{"cells":["3","4","6","9"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"remain":7,"events":1},"note":"The call with start 0 chooses 3, so the remaining target becomes 7."},{"at":{"start":1},"vars":{"remain":3,"events":2},"note":"The call with start 1 chooses 4, so the remaining target becomes 3."},{"at":{"start":2},"vars":{"remain":3,"events":2},"note":"The value 6 exceeds the remaining target 3, so the loop stops. Every later value is larger still."},{"at":{"start":1},"vars":{"remain":1,"events":3},"note":"The call with start 1 chooses 6, so the remaining target becomes 1."},{"at":{"start":3},"vars":{"remain":1,"events":3},"note":"The value 9 exceeds the remaining target 1, so the loop stops. Every later value is larger still."},{"at":{"start":1},"vars":{"remain":7,"events":3},"note":"The value 9 exceeds the remaining target 7, so the loop stops. Every later value is larger still."},{"at":{"start":0},"vars":{"remain":6,"events":4},"note":"The call with start 0 chooses 4, so the remaining target becomes 6."},{"at":{"start":2},"vars":{"remain":0,"events":5},"note":"The call with start 2 chooses 6, so the remaining target becomes 0. The path [4,6] adds up to 10, so the search returns true."}]}
```

```trace
{"cells":["5","-3"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"remain":2,"events":0},"note":"The root call needs 2 and its values can reach totals from -3 to 5, so the target lies inside that range and the search continues."},{"at":{"start":0},"vars":{"remain":-3,"events":1},"note":"The call chooses 5, so the remaining target becomes -3. A positive-value rule would stop here, but the next value may be negative."},{"at":{"start":1},"vars":{"remain":0,"events":2},"note":"The call with start 1 chooses -3, so the remaining target becomes 0. The set [5,-3] adds up to 2, and the search returns true."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### Existence With Two Proofs

The method answers whether some set of sorted positive values adds up to the target. It uses two skips, and each has a comment that names its proof.

```java
static boolean canReach(int start, int remain, int[] a, int[] suffix) {
    if (remain == 0) return true;                          // the path is a result
    for (int i = start; i < a.length; i++) {
        if (a[i] > remain) break;                          // monotone: sorted positives make later values larger still
        if (suffix[i] < remain) break;                     // upper bound: even all values from i cannot reach remain
        if (canReach(i + 1, remain - a[i], a, suffix)) return true;   // a result ends the whole search
    }
    return false;
}
```

#### Building The Suffix Sums

The array `suffix` has length `n + 1`, and `suffix[i]` holds the sum of `a[i]` to `a[n - 1]`. The loop `for (int i = n - 1; i >= 0; i--) suffix[i] = suffix[i + 1] + a[i];` builds it in O(n). The call needs no change for a larger array.

#### Cost Of The Search

The worst case still costs O(2^n), because a target near half of the total keeps many paths alive. The skips remove every path whose total or whose reachable range rules it out, which cuts the number of calls by large factors on typical inputs. The stack uses O(n) memory.

<!-- stage: applicability -->
### Recognizing A Provable Prune

#### Spotting The Pattern

The cue is a partial choice that no extension can turn into a result, and a short argument that shows it. The invariant is that every skip follows from a stated fact about the input, such as positive values, a sorted order or a count of slots.

#### Finding The False Friend

The false friend is a skip that rests on a hunch, such as dropping a branch because its sum looks large. A hunch removes results without any error. A second false friend is a correct rule applied to the wrong data, such as the overshoot rule on values that may be negative.

#### Recognizing The No-Go Cases

The skip does not fit when the input may hold negative values and no other bound holds. It does not fit when the search needs every path, such as a listing of all subsets. For an optimization, a bound against the best result so far also needs a proof that the bound is valid.

<!-- stage: exercises -->
### Exercises

#### [Build] Positive Remaining Sum (Author exercise)
<!-- id: bt-positive-remaining-sum -->

**Prerequisites.** The monotone constraint and the two skips of this lesson.

**Problem.** The array `values` holds positive integers in nondecreasing order, and `target` is a non-negative integer. Return true when some subset of `values`, possibly empty, adds up to `target`, and false otherwise. Each index serves at most once. The search stops at the first value that exceeds the remaining target and returns true as soon as it finds a subset.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 20`.
- **Values** satisfy `1 <= values[i] <= 50`, and they never decrease along the array.
- **Target** is `0 <= target <= 200`.
- **Mutation** does not occur; `values` keeps its contents.

**Example 1.** Input `values = [3,4,6,9]`, `target = 10`, output true.

**Example 2.** Input `values = [5,7]`, `target = 6`, output false.

**Hint.** Which fact about the values makes the stop safe? What does the empty subset give for target 0?

**Changed decision.** The search asks whether a result exists, so it returns at the first success and stops a loop with the monotone constraint.

#### [Vary] Remaining-Slots Bound (Author exercise)
<!-- id: bt-remaining-slots-bound -->

**Prerequisites.** The previous exercise and the choice of `k` values from an earlier lesson.

**Problem.** The array `values` holds positive integers in nondecreasing order, `k` is a positive integer and `target` is a non-negative integer. Return the number of subsets of exactly `k` indices whose values add up to `target`. Stop a branch when fewer than the needed number of indices remain, when the smallest possible completion exceeds the remaining target, or when the largest possible completion falls below it.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 20`.
- **Values** satisfy `1 <= values[i] <= 50`, and they never decrease along the array.
- **Size** is `1 <= k <= 20`, and `k` may exceed the length.
- **Return** is an `int`.

**Example 1.** Input `values = [1,2,3,4,5]`, `k = 2`, `target = 6`, output 2.

**Example 2.** Input `values = [4,9]`, `k = 3`, `target = 13`, output 0.

**Hint.** Which sum is the smallest that `s` more values can reach from index `i` in a sorted array? Which sum is the largest?

**Changed decision.** Two bounds join the slot count, and each bound needs the sorted order and the positive values to be correct.

#### [Boundary] Negative Values Break Sum Pruning (Author exercise)
<!-- id: bt-negative-values-break-pruning -->

**Prerequisites.** The two exercises above.

**Problem.** The array `values` holds integers of any sign in any order, and `target` is an integer. Return true when some subset of `values`, possibly empty, adds up to `target`. A path whose sum passes the target may still recover through a later negative value, so the search may not stop on an overshoot. It may stop when the remaining target lies outside the range that the later values can add up to.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 18`.
- **Values** satisfy `-20 <= values[i] <= 20`.
- **Target** is `-100 <= target <= 100`.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [5,-3]`, `target = 2`, output true.

**Example 2.** Input `values = [6,-6,1]`, `target = 7`, output true.

**Hint.** Which sum is the largest that the values from index `i` can add up to? Which is the smallest? Why does the overshoot rule fail on `[5, -3]`?

**Changed decision.** The monotone constraint no longer holds, so the skip rests on the range of totals that the later values can reach.

#### [Recognize] N-Queens Count (LeetCode 51)
<!-- id: bt-n-queens-count -->

**Prerequisites.** The previous three exercises.

**Problem.** Place `n` queens on an `n` by `n` board, one in each row, so that no two queens share a column or a diagonal. Return the number of different placements. The search fills one row per call and rejects a cell at once when its column or one of its two diagonals already holds a queen. Rows are numbered from 0.

**Constraints.** The limits are:
- **Size** is `1 <= n <= 9`.
- **Return** is an `int`.
- **Placements** are different when some row has its queen in a different column.
- **Boards** with no valid placement give 0.

**Example 1.** Input `n = 4`, output 2.

**Example 2.** Input `n = 3`, output 0.

**Hint.** Which value is equal for all cells on one diagonal, and which is equal on the other diagonal? How many queens does a row hold in a valid placement?

**Changed decision.** The search counts placements and rejects a cell by a proven rule, which is the same column or the same diagonal sum or difference.
