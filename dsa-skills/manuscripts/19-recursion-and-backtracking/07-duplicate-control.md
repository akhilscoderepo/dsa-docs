<!-- lesson-kind: standard -->
<!-- lesson-id: duplicate-control -->
## Duplicate Control

<!-- stage: context -->
### The Button Box At Ferrow Mill

The seamstresses of Ferrow Mill keep their spare buttons in a biscuit tin, and the tin holds many buttons that are exactly alike: three brass ones, two of horn, a single pearl. A customer ordering a coat may ask for any selection of buttons from the tin, and the foreman wants a card that lists every different selection once. Two brass buttons are two brass buttons whichever two the seamstress lifts, so a card that lists "the first brass and the second brass" next to "the first brass and the third brass" lists one selection twice.

The foreman cannot tell identical buttons apart and does not want to. He wants a list in which each distinct selection appears once, and he also wants it to include the selection of two brass buttons, because the tin holds three of them.

<!-- stage: naive -->
### List Every Selection And Merge The Twins

The direct way is to treat each button as its own object, list all 2^n selections of the tin with the plain walk of an earlier lesson, order the values of each selection, and keep one copy of each in a set. Identical buttons give identical lists, so the twins merge.

```java
static Set<List<Integer>> selectionsByMerge(int[] buttons) {
    Set<List<Integer>> distinct = new LinkedHashSet<>();
    int n = buttons.length;
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> chosen = new ArrayList<>();
        for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) chosen.add(buttons[i]);
        Collections.sort(chosen);
        distinct.add(chosen);
    }
    return distinct;
}
```

It is easy to believe, since each real selection of buttons is covered and the set removes the twins, and it can serve as an oracle for any smarter search.

<!-- stage: bottleneck -->
### The Tin Of Twenty Identical Buttons

The method builds and sorts every one of the 2^n selections before the set throws most of them away, so it costs O(n * 2^n) however many repeats the tin holds. A tin of twenty identical buttons has twenty-one different selections, one for each count, yet the method builds more than a million lists to find them. The more alike the buttons are, the larger the share of wasted work, and a set that grows large with duplicates before they merge also uses memory in proportion to the waste.

The waste has a clear shape. Picking a brass button first, and then picking any other brass button first, leads to the same family of selections, because the second pick leaves fewer buttons to its right and so offers a smaller family than the first did. A search that could recognise such a choice at the moment it is about to be made, and decline it, would never build the duplicate lists at all.

<!-- stage: insight -->
### Skip The Twin At The Same Depth

Sort a copy of the buttons so that identical ones stand next to each other, and run the increasing-start search. Within one loop, a call is offering a list of **equal siblings** whenever two neighbouring positions hold the same value. Choosing the first of them leaves every later button, equal ones included, still available below it. Choosing the second instead offers only the buttons after it, so everything it can lead to is already reachable below the first. The later sibling is therefore redundant, and the search is told to decline it.

That gives the **same-depth skip**: in the loop that starts at `start`, skip position i when i is greater than `start` and the value at i equals the value at i - 1. The comparison with `start`, and not with zero, is the whole point. At i equal to `start` the previous position is not a sibling in this loop. It was taken higher up the path, so choosing position i adds a second copy of that value, which is a perfectly valid selection such as two brass buttons.

Skipping every repeated value, which a test of i greater than zero would do, forbids exactly those valid selections, so no number of copies above one would ever be chosen. The skip applies only between siblings of one loop, which is why equal values at different depths survive. The **sorted copy** is needed because equal values must be adjacent for the neighbour test to find them, and a copy is used so that the caller's array is not reordered.

The invariant is that two siblings in one loop never hold the same value, while the path may hold any number of equal values taken at different depths.

<!-- names: equal siblings, same-depth skip, sorted copy -->

<!-- stage: variables -->
### Sorted Values, Start And Path

The array `vals` is the sorted copy and never changes during the search. The integer `start` is the first position the loop of this call may take, and it is also the boundary that makes the skip test correct: positions after `start` have siblings to their left in this loop, and the position `start` has none. The `path` holds the values taken, in sorted order. The loop index `i` is the position being taken, and the test `vals[i] == vals[i - 1]` is made only when `i > start`. A copy of the path is stored on arrival at every node.

<!-- stage: trace -->
### Skipping A Twin In One Loop

The first trace runs the search on the sorted values 1, 2, 2. The pointer `start` is the first position the loop may take, and `i` is the position under consideration, with -1 when a call has just arrived and records its path. Look for two events: the second two at depth two is taken, because it equals the value taken above it and sits at `start`, and the second two in the loop at depth one is skipped.

```trace
{"cells":["1","2","2"],"pointers":["start","i"],"steps":[{"at":{"start":0,"i":-1},"vars":{"path":"[]","recorded":1},"note":"The call arrives with start 0 and records a copy of [] as selection 1."},{"at":{"start":0,"i":0},"vars":{"path":"[1]","recorded":1},"note":"Position 0 holds 1 and is taken, so the path is [1]."},{"at":{"start":1,"i":-1},"vars":{"path":"[1]","recorded":2},"note":"The call arrives with start 1 and records a copy of [1] as selection 2."},{"at":{"start":1,"i":1},"vars":{"path":"[1, 2]","recorded":2},"note":"Position 1 holds 2 and is taken, so the path is [1, 2]."},{"at":{"start":2,"i":-1},"vars":{"path":"[1, 2]","recorded":3},"note":"The call arrives with start 2 and records a copy of [1, 2] as selection 3."},{"at":{"start":2,"i":2},"vars":{"path":"[1, 2, 2]","recorded":3},"note":"Position 2 holds 2, equal to the value just taken above, but it is the first position of this loop, so it is a second copy and is taken: the path is [1, 2, 2]."},{"at":{"start":3,"i":-1},"vars":{"path":"[1, 2, 2]","recorded":4},"note":"The call arrives with start 3 and records a copy of [1, 2, 2] as selection 4."},{"at":{"start":2,"i":2},"vars":{"path":"[1, 2]","recorded":4},"note":"The value 2 is removed, so the path is [1, 2]."},{"at":{"start":1,"i":1},"vars":{"path":"[1]","recorded":4},"note":"The value 2 is removed, so the path is [1]."},{"at":{"start":1,"i":2},"vars":{"path":"[1]","recorded":4},"note":"Position 2 holds 2, the same as position 1 in this same loop, so it is an equal sibling and is skipped."},{"at":{"start":0,"i":0},"vars":{"path":"empty","recorded":4},"note":"The value 1 is removed, so the path is empty."},{"at":{"start":0,"i":1},"vars":{"path":"[2]","recorded":4},"note":"Position 1 holds 2 and is taken, so the path is [2]."},{"at":{"start":2,"i":-1},"vars":{"path":"[2]","recorded":5},"note":"The call arrives with start 2 and records a copy of [2] as selection 5."},{"at":{"start":2,"i":2},"vars":{"path":"[2, 2]","recorded":5},"note":"Position 2 holds 2, equal to the value just taken above, but it is the first position of this loop, so it is a second copy and is taken: the path is [2, 2]."},{"at":{"start":3,"i":-1},"vars":{"path":"[2, 2]","recorded":6},"note":"The call arrives with start 3 and records a copy of [2, 2] as selection 6."},{"at":{"start":2,"i":2},"vars":{"path":"[2]","recorded":6},"note":"The value 2 is removed, so the path is [2]."},{"at":{"start":0,"i":1},"vars":{"path":"empty","recorded":6},"note":"The value 2 is removed, so the path is empty."},{"at":{"start":0,"i":2},"vars":{"path":"[]","recorded":6},"note":"Position 2 holds 2, the same as position 1 in this same loop, so it is an equal sibling and is skipped."}]}
```

The second trace is the false friend, run on the values 2, 2 with a skip test of `i > 0` instead of `i > start`. The variable `lost` becomes yes at the moment a valid selection is cut off, which here is the pair of twos.

```trace
{"cells":["2","2"],"pointers":["start","i"],"steps":[{"at":{"start":0,"i":-1},"vars":{"path":"[]","lost":"no"},"note":"The call arrives with start 0 and records a copy of []."},{"at":{"start":0,"i":0},"vars":{"path":"[2]","lost":"no"},"note":"Position 0 is taken, so the path is [2]."},{"at":{"start":1,"i":-1},"vars":{"path":"[2]","lost":"no"},"note":"The call arrives with start 1 and records a copy of [2]."},{"at":{"start":1,"i":1},"vars":{"path":"[2]","lost":"yes"},"note":"Position 1 equals position 0, and the test i > 0 skips it, although this is the first position of the loop, so the valid pair [2, 2] is cut off."},{"at":{"start":0,"i":0},"vars":{"path":"empty","lost":"no"},"note":"The value is removed, so the path is empty."},{"at":{"start":0,"i":1},"vars":{"path":"[]","lost":"no"},"note":"Position 1 equals position 0 in this loop, so skipping it is right."}]}
```

<!-- stage: code -->
### The Test Against Start

```java
static List<List<Integer>> distinctSubsets(int[] nums) {
    int[] vals = nums.clone();
    Arrays.sort(vals);                              // sort a copy
    List<List<Integer>> out = new ArrayList<>();
    walk(vals, 0, new ArrayList<>(), out);
    return out;
}

private static void walk(int[] vals, int start, List<Integer> path, List<List<Integer>> out) {
    out.add(new ArrayList<>(path));
    for (int i = start; i < vals.length; i++) {
        if (i > start && vals[i] == vals[i - 1]) continue;   // equal sibling
        path.add(vals[i]);
        walk(vals, i + 1, path, out);
        path.remove(path.size() - 1);
    }
}
```

The array holds `int` values, so `==` compares numbers. If the same test were written for a `List<Integer>`, then `==` would compare references, and for values beyond 127 two equal numbers can be different objects, so the skip would silently fail. The search visits one node per distinct selection, so its time is proportional to the number of distinct selections times their length, after an O(n log n) sort.

<!-- stage: applicability -->
### Equal Values In The Input

Reach for the same-depth skip whenever the input holds equal values and the answers should not repeat: distinct subsets, distinct combinations that sum to a target, and distinct arrangements, as in the second form of the permutation lesson. The invariant to guard is that siblings in a single loop have distinct values, and the test must reference the start of the loop and not the start of the array.

The nearest false friend is deduplication by a set after the fact, which is correct but pays for every repeat before it is thrown away, and in the worst case turns a linear number of answers into an exponential amount of work. A second false friend is skipping any value that was seen before anywhere on the path, which looks like the same idea and removes valid answers that use a value twice. The test is never about the whole path. It compares only neighbours within one loop.

Do not use the rule on unsorted input, since equal values are then not adjacent and some twins slip through. Do not sort the caller's array in place unless the contract allows it. In Java compare `int` values or call `equals` on boxed values, and remember that the skip rule removes only repeated branches, never the repeated values inside one selection.

<!-- stage: exercises -->
### Exercises

#### [Build] Equal Sibling Choices (Author exercise)
<!-- id: bt-equal-siblings -->

**Prerequisites.** The increasing-start search for subsets, and the idea of a subtree of calls.

**Problem.** Take the subset search with no skip rule on a sorted array. The root has one child for each first pick. For a position `p` with `nums[p] == nums[p - 1]`, return a pair `[a, b]`: `a` is the number of subsets recorded in the subtree of the child at `p`, and `b` is how many of those value lists also occur in the subtree of the child at `p - 1`.

**Constraints.** The array is sorted ascending with 2 to 8 values between -9 and 9, and `p` is a position with 1 <= p < nums.length and `nums[p] == nums[p - 1]`.

**Example 1.** Input `nums = [1, 2, 2]`, `p = 2`, output `[1, 1]`.

**Example 2.** Input `nums = [3, 3, 3, 5]`, `p = 1`, output `[4, 4]`.

**Hint.** Which values stay available below the child at `p - 1` that are also available below the child at `p`?

**Changed decision.** The question is asked of a single loop's neighbours, so the answer is always that the later sibling adds nothing new.

#### [Vary] Fixed-Size Distinct Subsets (LeetCode 90)
<!-- id: bt-distinct-size-k -->

**Prerequisites.** The Equal Sibling Choices rung.

**Problem.** Given an unsorted array that may contain equal values and a size `k`, return every distinct subset with exactly `k` values, each in nondecreasing order, in the order the search finds them. A size larger than the array has no answers.

**Constraints.** 0 <= nums.length <= 9, 0 <= k <= 10, and the values are integers between -5 and 5.

**Example 1.** Input `nums = [1, 2, 2]`, `k = 2`, output `[[1, 2], [2, 2]]`.

**Example 2.** Input `nums = [4, 4, 4]`, `k = 2`, output `[[4, 4]]`.

**Hint.** At which size does a call record, and does the skip rule care how many values are already on the path?

**Changed decision.** A size target replaces recording at every node, so a path is stored only at length k, and the same-depth skip is unchanged.

#### [Boundary] Equal Values At Different Depths (Author exercise)
<!-- id: bt-equal-depths -->

**Prerequisites.** The Fixed-Size Distinct Subsets rung.

**Problem.** Given an unsorted array, return every distinct subset in which some value appears at least twice, each in nondecreasing order and in the order found. A value taken once and a value taken twice are both ordinary paths, and only the skip within one loop may be used to avoid repeats.

**Constraints.** 0 <= nums.length <= 9, and the values are integers between 1 and 1000.

**Example 1.** Input `nums = [1, 2, 2]`, output `[[1, 2, 2], [2, 2]]`.

**Example 2.** Input `nums = [5, 5, 5]`, output `[[5, 5], [5, 5, 5]]`.

**Hint.** Where does the second copy of a value sit in the search, in the same loop as the first copy or in the call below it?

**Changed decision.** The answers are exactly the ones that a skip applied to every repeated value would forbid, so the test must compare against the loop start.

#### [Recognize] Combination Sum II (LeetCode 40)
<!-- id: bt-combination-sum-two -->

**Prerequisites.** The Equal Values At Different Depths rung, and the remaining-target state of the reusable candidates lesson.

**Problem.** Given candidates that may repeat and a target, return every distinct combination that sums to the target, where each candidate occurrence is used at most once. Each combination is nondecreasing and combinations come in the order found. Sort a copy, skip equal siblings, and leave the loop at the first candidate that is too large.

**Constraints.** 1 <= candidates.length <= 10, each candidate is between 1 and 12, and 1 <= target <= 30.

**Example 1.** Input `candidates = [3, 1, 2, 3, 1, 4]`, `target = 6`, output `[[1, 1, 4], [1, 2, 3], [2, 4], [3, 3]]`.

**Example 2.** Input `candidates = [2, 2, 2]`, `target = 4`, output `[[2, 2]]`.

**Hint.** After sorting, which occurrence of an equal run is offered at a loop, and how many occurrences can still be used one level deeper?

**Changed decision.** Candidates are used once, so the next start is i + 1, and the equal-sibling skip joins the target-based exit from the loop.
