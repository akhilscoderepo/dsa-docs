<!-- lesson-kind: standard -->
<!-- lesson-id: subsets -->
## Subsets

<!-- stage: context -->
### The Spice Rack Of Quillon Market

A stall at Quillon Market sells spice bundles to order. The jars stand on one rack in a fixed row, and a customer may take any selection of them, from no jar at all up to every jar, with the jars always written on the label in the order they stand on the rack. The stallholder wants a price card that lists every bundle a customer could possibly ask for, once each, so that she never has to work one out while a queue waits.

She tried writing the card by instinct and kept losing track. Bundles with the cumin appeared twice, a bundle that she was sure she had listed was nowhere on the card, and nobody could say how many there should be in all. What she needs is a way to walk the rack that cannot repeat a bundle or skip one.

<!-- stage: naive -->
### Count Through Every Pattern Of Jars

A rack of n jars has 2^n patterns of taken and left jars, and each pattern can be read as a binary number with one bit per jar. The direct method counts from zero up to 2^n - 1 and, for each number, scans its bits from the first jar to the last and writes down the jars whose bit is set.

```java
static List<List<Integer>> bundlesByMask(int[] jars) {
    int n = jars.length;
    List<List<Integer>> card = new ArrayList<>();
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> bundle = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask >> i & 1) == 1) bundle.add(jars[i]);
        }
        card.add(bundle);
    }
    return card;
}
```

It lists every bundle exactly once for any rack that fits in an `int` mask, and it makes a trustworthy oracle for the method that replaces it.

<!-- stage: bottleneck -->
### Each Pattern Is Built From Nothing

Every mask is processed alone, with a scan of all n bits, so the card costs O(n * 2^n) even for the patterns that take no jar at all. That matches the size of the card in the worst case, so the speed is not the real trouble. The trouble is that the loop knows nothing about the decisions inside a mask. Two masks that agree on the first twenty jars repeat that agreement from scratch, and the loop has no way to say that a whole family of bundles is unwanted once their shared start is known to be a bad one.

The mask also welds the method to the width of an integer. A shift of 1 by 32 places gives a nonsense count, so a rack of 32 or more jars cannot be written this way, and the loop gives no place to hang a rule such as "skip bundles that cost too much" or "treat two equal jars as one". A search that decides the jars one at a time, and shares the decisions made so far among all the bundles that start with them, offers that place.

<!-- stage: insight -->
### One Route Per Bundle

Walk the rack from the first jar to the last and settle each jar as taken or left, in that order. At any moment the **decision prefix** is the record of what was settled for all the jars already passed, and the jars after the current index have not been touched. The search state is therefore only the index and the working path of taken jars, and a bundle is the working path when the index runs off the end of the rack.

The same tree can be read in a second way. In the **increasing-start loop**, every node of the search is already a bundle, namely the jars taken so far, and its children are made by taking exactly one later jar, from a starting index just beyond the last jar taken. The loop records the path at every node on arrival, so the bundle with no jars is recorded first, at the root, before any jar is taken. Both readings produce the same family, because a bundle written in rack order can be reached in exactly one way: take its jars in rack order.

That uniqueness is the whole proof that nothing repeats and nothing is missed. A bundle that is missing would need a route the loop does not take, and a bundle that appears twice would need two routes, but jars are only ever added at a start index larger than the previous jar. The **empty subset** is the bundle at the root, and it exists for every rack, including a rack with no jars at all.

The invariant is that at index i the path fixes the fate of exactly the jars before i, and each bundle of jars in rack order has one route from the root.

<!-- names: decision prefix, increasing-start loop, empty subset -->

<!-- stage: variables -->
### Index, Path And Card

In the include or leave view, `index` is the jar being settled, and it grows by one on each call. In the increasing-start view the same role is played by `start`, which is the first jar the loop may still take, and by the loop variable `i`, which is the jar being taken now, so the next call receives `i + 1`. The `path` holds the taken jars in rack order and changes by one jar per move. The `card` is the list of finished bundles, and each entry is a copy made at the moment of recording, since the path keeps changing.

<!-- stage: trace -->
### Eight Bundles From Three Jars

The first trace follows the increasing-start loop over the jars 1, 2 and 3. The pointer `start` marks the first jar a call may take, and the pointer `i` marks the jar the loop is taking, and it reads -1 at the instant a call has just arrived and is recording its path. Watch that every arrival records a bundle, that the removals bring the path back before the loop moves on, and that the order of the card is the order of arrival.

```trace
{"cells":["1","2","3"],"pointers":["start","i"],"steps":[{"at":{"start":0,"i":-1},"vars":{"path":"[]","recorded":1},"note":"The call arrives with start 0 and records a copy of the path [] as bundle 1."},{"at":{"start":0,"i":0},"vars":{"path":"[1]","recorded":1},"note":"The loop takes jar 1, so the path is [1], and the next call may only use jars from index 1."},{"at":{"start":1,"i":-1},"vars":{"path":"[1]","recorded":2},"note":"The call arrives with start 1 and records a copy of the path [1] as bundle 2."},{"at":{"start":1,"i":1},"vars":{"path":"[1, 2]","recorded":2},"note":"The loop takes jar 2, so the path is [1, 2], and the next call may only use jars from index 2."},{"at":{"start":2,"i":-1},"vars":{"path":"[1, 2]","recorded":3},"note":"The call arrives with start 2 and records a copy of the path [1, 2] as bundle 3."},{"at":{"start":2,"i":2},"vars":{"path":"[1, 2, 3]","recorded":3},"note":"The loop takes jar 3, so the path is [1, 2, 3], and the next call may only use jars from index 3."},{"at":{"start":3,"i":-1},"vars":{"path":"[1, 2, 3]","recorded":4},"note":"The call arrives with start 3 and records a copy of the path [1, 2, 3] as bundle 4."},{"at":{"start":2,"i":2},"vars":{"path":"[1, 2]","recorded":4},"note":"Jar 3 is left again, so the path is [1, 2] and the loop moves to the next jar."},{"at":{"start":1,"i":1},"vars":{"path":"[1]","recorded":4},"note":"Jar 2 is left again, so the path is [1] and the loop moves to the next jar."},{"at":{"start":1,"i":2},"vars":{"path":"[1, 3]","recorded":4},"note":"The loop takes jar 3, so the path is [1, 3], and the next call may only use jars from index 3."},{"at":{"start":3,"i":-1},"vars":{"path":"[1, 3]","recorded":5},"note":"The call arrives with start 3 and records a copy of the path [1, 3] as bundle 5."},{"at":{"start":1,"i":2},"vars":{"path":"[1]","recorded":5},"note":"Jar 3 is left again, so the path is [1] and the loop moves to the next jar."},{"at":{"start":0,"i":0},"vars":{"path":"[]","recorded":5},"note":"Jar 1 is left again, so the path is [] and the loop moves to the next jar."},{"at":{"start":0,"i":1},"vars":{"path":"[2]","recorded":5},"note":"The loop takes jar 2, so the path is [2], and the next call may only use jars from index 2."},{"at":{"start":2,"i":-1},"vars":{"path":"[2]","recorded":6},"note":"The call arrives with start 2 and records a copy of the path [2] as bundle 6."},{"at":{"start":2,"i":2},"vars":{"path":"[2, 3]","recorded":6},"note":"The loop takes jar 3, so the path is [2, 3], and the next call may only use jars from index 3."},{"at":{"start":3,"i":-1},"vars":{"path":"[2, 3]","recorded":7},"note":"The call arrives with start 3 and records a copy of the path [2, 3] as bundle 7."},{"at":{"start":2,"i":2},"vars":{"path":"[2]","recorded":7},"note":"Jar 3 is left again, so the path is [2] and the loop moves to the next jar."},{"at":{"start":0,"i":1},"vars":{"path":"[]","recorded":7},"note":"Jar 2 is left again, so the path is [] and the loop moves to the next jar."},{"at":{"start":0,"i":2},"vars":{"path":"[3]","recorded":7},"note":"The loop takes jar 3, so the path is [3], and the next call may only use jars from index 3."},{"at":{"start":3,"i":-1},"vars":{"path":"[3]","recorded":8},"note":"The call arrives with start 3 and records a copy of the path [3] as bundle 8."},{"at":{"start":0,"i":2},"vars":{"path":"[]","recorded":8},"note":"Jar 3 is left again, so the path is [] and the loop moves to the next jar."}]}
```

The second trace is the include or leave reading on two jars, with leave tried first. The pointer `index` is the jar being settled, and a bundle is recorded at the leaf, when the index is one past the last jar. Compare the order of this card with the first one, since the two readings reach the same four bundles by different routes.

```trace
{"cells":["4","7"],"pointers":["index"],"steps":[{"at":{"index":0},"vars":{"path":"[]","recorded":0},"note":"Jar 4 is left out first, so the path stays []."},{"at":{"index":1},"vars":{"path":"[]","recorded":0},"note":"Jar 7 is left out first, so the path stays []."},{"at":{"index":2},"vars":{"path":"[]","recorded":1},"note":"Both jars are settled, so a copy of the path [] is recorded as bundle 1."},{"at":{"index":1},"vars":{"path":"[7]","recorded":1},"note":"Jar 7 is now taken, so the path is [7]."},{"at":{"index":2},"vars":{"path":"[7]","recorded":2},"note":"Both jars are settled, so a copy of the path [7] is recorded as bundle 2."},{"at":{"index":1},"vars":{"path":"[]","recorded":2},"note":"Both choices for jar 7 are done, so it is removed and the path reads []."},{"at":{"index":0},"vars":{"path":"[4]","recorded":2},"note":"Jar 4 is now taken, so the path is [4]."},{"at":{"index":1},"vars":{"path":"[4]","recorded":2},"note":"Jar 7 is left out first, so the path stays [4]."},{"at":{"index":2},"vars":{"path":"[4]","recorded":3},"note":"Both jars are settled, so a copy of the path [4] is recorded as bundle 3."},{"at":{"index":1},"vars":{"path":"[4, 7]","recorded":3},"note":"Jar 7 is now taken, so the path is [4, 7]."},{"at":{"index":2},"vars":{"path":"[4, 7]","recorded":4},"note":"Both jars are settled, so a copy of the path [4, 7] is recorded as bundle 4."},{"at":{"index":1},"vars":{"path":"[4]","recorded":4},"note":"Both choices for jar 7 are done, so it is removed and the path reads [4]."},{"at":{"index":0},"vars":{"path":"[]","recorded":4},"note":"Both choices for jar 4 are done, so it is removed and the path reads []."}]}
```

<!-- stage: code -->
### Record At Every Arrival

```java
static List<List<Integer>> allBundles(int[] jars) {
    List<List<Integer>> card = new ArrayList<>();
    collect(jars, 0, new ArrayList<>(), card);
    return card;
}

private static void collect(int[] jars, int start, List<Integer> path, List<List<Integer>> card) {
    card.add(new ArrayList<>(path));                 // every arrival is a bundle
    for (int i = start; i < jars.length; i++) {
        path.add(jars[i]);                           // take one later jar
        collect(jars, i + 1, path, card);            // only later jars remain
        path.remove(path.size() - 1);                // leave it again
    }
}
```

An empty array records the root and then the loop body never runs, so the result is a list holding one empty list. The tree has 2^n nodes, each costing O(1) beyond its copy, so the whole card takes O(n * 2^n) time, and the stack is n frames deep.

<!-- stage: applicability -->
### Every Element Optional

Use the walk when each item may be present or absent, the order inside a result follows the input, and the answers are the whole family or those members that pass a test. Selections of features, collections of coins and subsets that must satisfy a condition all share the shape. The invariant to keep in mind is that the path fixes the fate of every element before the index, so a pruning rule can look only at the path and at what remains.

The nearest false friend is the arrangement search of the next lesson. There the state marks which elements are used and a call decides which element fills a position, so two orders of the same elements are two different answers. Here a bundle has no positions, and taking the cumin before the pepper is not a separate bundle, so reusing the used-array idea would produce too many results, in the wrong shape. A second false friend is an input with equal values, which makes some bundles appear more than once, and that is repaired by sorting and skipping, which is the subject of a later lesson.

Do not generate the whole family when only a count or a best value is asked for and the input is large, since 2^n grows quickly. Handle the empty input as one bundle and not as no answer, and in Java sort a copy when the algorithm needs order, because sorting the caller's array silently changes what the caller sees.

<!-- stage: exercises -->
### Exercises

#### [Build] Subsets Of Two Values (Author exercise)
<!-- id: bt-two-values -->

**Prerequisites.** The idea of a decision prefix, and the working path with its undo step.

**Problem.** Given an array of exactly two distinct integers, return all four subsets by settling the first value and then the second, trying to leave each value out before taking it. Each subset is written in the original order of the array.

**Constraints.** The array has length 2, and the values are distinct integers between -100 and 100.

**Example 1.** Input `nums = [4, 7]`, output `[[], [7], [4], [4, 7]]`.

**Example 2.** Input `nums = [-1, 0]`, output `[[], [0], [-1], [-1, 0]]`.

**Hint.** How many leaves does a tree of two binary decisions have, and in what order are they reached if the left branch always means leaving the value out?

**Changed decision.** The leave branch comes first at each level, and a value of zero is still a taken value and not an absent one.

#### [Vary] Subsets In Arrival Order (LeetCode 78)
<!-- id: bt-preorder-subsets -->

**Prerequisites.** The Subsets Of Two Values rung, and the starting index of the increasing-start loop.

**Problem.** Given an array of distinct integers, return every subset in the order the increasing-start loop arrives at them: record the current path on arrival, then for each index from the start onward take that element and recurse from the next index.

**Constraints.** 0 <= nums.length <= 10, and the values are distinct integers between -10 and 10.

**Example 1.** Input `nums = [1, 2, 3]`, output `[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]`.

**Example 2.** Input `nums = [4, 9]`, output `[[], [4], [4, 9], [9]]`.

**Hint.** What does the first recorded path look like, and which index does the call for a taken element receive as its start?

**Changed decision.** A subset is recorded at every node of the tree, not only at the leaves, and the next start moves just beyond the element taken.

#### [Boundary] Empty Input (Author exercise)
<!-- id: bt-empty-input -->

**Prerequisites.** The Subsets In Arrival Order rung.

**Problem.** In this version of the rack problem, given an array of distinct integers, possibly empty, and a target `t`, return every subset whose elements sum to `t`, in arrival order. The empty subset has sum zero, so an empty array with target zero has exactly one answer, and an empty array with any other target has none.

**Constraints.** 0 <= nums.length <= 12, the values are distinct integers between -20 and 20, and t is between -50 and 50.

**Example 1.** Input `nums = []`, `t = 0`, output `[[]]`.

**Example 2.** Input `nums = [3, -3, 5]`, `t = 0`, output `[[], [3, -3]]`.

**Hint.** What should the result be for an empty array and a target of 5, and why must a negative value stop you from abandoning a path whose sum is already above the target?

**Changed decision.** The result is a list holding one empty list, not an empty list, when the empty subset itself satisfies the condition.

#### [Recognize] Subsets With Equal Values (LeetCode 90)
<!-- id: bt-subsets-with-equals -->

**Prerequisites.** The Empty Input Subset Sums rung. The skip rule used here is only previewed, and the Duplicate Control lesson explains why it is safe.

**Problem.** Given an array of integers that may contain equal values, return every distinct subset, each in nondecreasing order, with no subset listed twice. Sort a copy of the array, then use the increasing-start loop and skip an element that equals the previous element of the same loop.

**Constraints.** 0 <= nums.length <= 10, and the values are integers between -10 and 10.

**Example 1.** Input `nums = [1, 2, 2]`, output `[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]`.

**Example 2.** Input `nums = [4, 1, 4, 4]`, output `[[], [1], [1, 4], [1, 4, 4], [1, 4, 4, 4], [4], [4, 4], [4, 4, 4]]`.

**Hint.** Why does taking the second of two equal values at the same loop give a bundle that the first already produced?

**Changed decision.** Equal elements at one loop are tried only once, after the input is sorted so that equal values sit side by side.
