<!-- lesson-kind: standard -->
<!-- lesson-id: sort-and-deduplicate -->
## Sort And Deduplicate

<!-- stage: context -->
### A Mailing List With Repeated Names

A neighborhood association collects sign-up sheets for its newsletter. Over the years the same households have signed up on several sheets, so the combined list has many repeats, and sending three copies to one house annoys everybody. The secretary wants a clean list with each household once, and, if possible, a count of how many sheets each household appeared on.

She starts by copying names onto a fresh page. Before writing a name she reads down the fresh page to see whether it is already there. It is slow, but she sees no alternative because the sheets are in no order at all. A colleague suggests something else: put the whole stack of names in alphabetical order first. After that, repeats of one household sit side by side, and she would only have to look at the line she just wrote.

<!-- stage: naive -->
### Search The Clean Page For Every Name

In Java the secretary's method keeps a list of names already accepted and searches it for every new name.

```java
static List<Integer> distinctBySearch(int[] values) {
    List<Integer> kept = new ArrayList<>();
    for (int v : values) {
        boolean seen = false;
        for (int k : kept) {
            if (k == v) { seen = true; break; }
        }
        if (!seen) kept.add(v);
    }
    return kept;
}
```

The kept list preserves the order of first appearance, it never contains a repeat, and it handles an empty input without any special case.

<!-- stage: bottleneck -->
### Re-Reading The Clean Page Each Time

If there are n values and most of them are different, the inner loop reads a page that grows to nearly n entries for every new value, so the work is O(n^2). Fifty thousand distinct names mean over a billion comparisons. The repeated work is easy to see: the secretary asks a question about the whole clean page when only one thing could matter, whether the name equals the last one she wrote, if the names had been sorted.

The order of first appearance, which the slow method provides for free, is not something every problem wants. When the output may be in any deterministic order, ascending is as good as any other, and ascending is cheaper. When the problem wants first-appearance order, sorting is the wrong tool, and a hash-based structure from the earlier chapter is the right one. The decision depends on what the output contract says about order.

<!-- stage: insight -->
### Only The Current Run Is Unresolved

Sorting puts equal values next to each other, so each value occupies one contiguous stretch. Walking through the sorted array, the only group that can still grow is the **current run**, the stretch that contains the position being read. Everything before it is finished, and nothing after it has been seen. This is the whole state of the scan: the value of the current run, and, if needed, its length so far.

A new run begins at a **run boundary**, a position where the value differs from the one before it. At a boundary the previous run is complete, and the scan can emit its **representative**, the single value that stands for the run, or its count, or any other summary of the run. The very first position always begins a run, so it needs no comparison with a previous element, and a program that compares it with a made-up starting value will go wrong for inputs that happen to contain that value.

<!-- names: current run, run boundary, representative -->

Several tasks reduce to this walk. Detecting a repeat is asking whether any run has length at least two. Listing the distinct values is emitting one representative per run. Intersecting two collections can be done without comparing them directly: reduce each collection to its distinct values, put the two reduced lists together and sort the result, and a value that appears twice in the combined sorted list must have come from both. The output then comes out in ascending order without any extra step.

The word-building problem uses sorting for a different kind of promise. When words are sorted alphabetically, every word's prefix sorts before it, so by the time a word is read, any shorter word it could have been built from has already been judged. Choosing the first longest word in sorted order also settles ties alphabetically, with no extra comparator.

<!-- stage: variables -->
### Position, Run Value And Run Length

The scan keeps an index `i` over the sorted array, the value that began the current run, and a counter holding how many equal values the run has had so far. At a boundary the counter is reset to one. If the answer is a list of representatives, an output list collects one value per run, appended at the moment a run begins, which avoids a special case for the last run at the end of the array. No other history is kept.

<!-- stage: trace -->
### Runs Closing And Two Lists Merging

The first trace sorts 4, 1, 4, 2, 1, 4 into 1, 1, 2, 4, 4, 4 and reads it left to right, tracking the length of the current run. The step to study is the third one, where the value changes from 1 to 2: the run of 1 values ends with length two, and a new run begins at the 2.

```trace
{"cells":[1,1,2,4,4,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":1,"runLength":1,"representatives":"1"},"note":"The first position begins a run. Representatives so far: 1."},{"at":{"i":1},"vars":{"value":1,"runLength":2,"representatives":"1"},"note":"1 equals the previous value, so the current run has length 2. Representatives so far: 1."},{"at":{"i":2},"vars":{"value":2,"runLength":1,"representatives":"1,2"},"note":"The value changes from 1 to 2, so the run of 1 ends with length 2 and a new run begins. Representatives so far: 1, 2."},{"at":{"i":3},"vars":{"value":4,"runLength":1,"representatives":"1,2,4"},"note":"The value changes from 2 to 4, so the run of 2 ends with length 1 and a new run begins. Representatives so far: 1, 2, 4."},{"at":{"i":4},"vars":{"value":4,"runLength":2,"representatives":"1,2,4"},"note":"4 equals the previous value, so the current run has length 2. Representatives so far: 1, 2, 4."},{"at":{"i":5},"vars":{"value":4,"runLength":3,"representatives":"1,2,4"},"note":"4 equals the previous value, so the current run has length 3. Representatives so far: 1, 2, 4."}]}
```

The second trace intersects 4, 9, 5, 9 with 9, 4, 9, 8, 4. Each side is reduced to distinct values, giving 4, 5, 9 and 4, 8, 9. The two lists are joined and sorted into 4, 4, 5, 8, 9, 9, and the scan looks for adjacent equal pairs. The step to study is the final one, where the second 9 matches the first, since that is a value present in both original lists.

```trace
{"cells":[4,4,5,8,9,9],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"previous":4,"current":4,"common":"4"},"note":"Position 1 holds 4 and position 0 holds 4. The value came from both arrays, so report 4."},{"at":{"i":2},"vars":{"previous":4,"current":5,"common":"4"},"note":"Position 2 holds 5 and position 1 holds 4. They differ, so nothing is reported."},{"at":{"i":3},"vars":{"previous":5,"current":8,"common":"4"},"note":"Position 3 holds 8 and position 2 holds 5. They differ, so nothing is reported."},{"at":{"i":4},"vars":{"previous":8,"current":9,"common":"4"},"note":"Position 4 holds 9 and position 3 holds 8. They differ, so nothing is reported."},{"at":{"i":5},"vars":{"previous":9,"current":9,"common":"4,9"},"note":"Position 5 holds 9 and position 4 holds 9. The value came from both arrays, so report 9."}]}
```

<!-- stage: code -->
### Representatives, Run Counts And Common Values

```java
static int[] distinctSorted(int[] values) {
    int[] a = values.clone();
    Arrays.sort(a);
    int[] out = new int[a.length];
    int size = 0;
    for (int i = 0; i < a.length; i++) {
        if (i == 0 || a[i] != a[i - 1]) out[size++] = a[i];   // a run begins here
    }
    return Arrays.copyOf(out, size);
}

static boolean hasRunOfTwo(int[] values) {
    int[] a = values.clone();
    Arrays.sort(a);
    int runLength = 0;
    for (int i = 0; i < a.length; i++) {
        runLength = (i > 0 && a[i] == a[i - 1]) ? runLength + 1 : 1;
        if (runLength >= 2) return true;
    }
    return false;
}

static int[] commonValues(int[] x, int[] y) {
    int[] ux = distinctSorted(x), uy = distinctSorted(y);
    int[] both = new int[ux.length + uy.length];
    System.arraycopy(ux, 0, both, 0, ux.length);
    System.arraycopy(uy, 0, both, ux.length, uy.length);
    Arrays.sort(both);
    int[] out = new int[Math.min(ux.length, uy.length)];
    int size = 0;
    for (int i = 1; i < both.length; i++) if (both[i] == both[i - 1]) out[size++] = both[i];
    return Arrays.copyOf(out, size);
}
```

Each function sorts, so the cost is O(n log n) time and O(n) extra space, followed by a linear scan. A value appears at most once in each distinct list, so it can appear at most twice in the combined one, which is what makes the adjacent test correct.

<!-- stage: applicability -->
### When Order Of Output Is Free

Use sort-and-deduplicate when the output may be in ascending order, or in no promised order at all, and when the question is about the groups of equal values: one per group, how many in each, whether any group has more than one member. The invariant is that all earlier runs are complete and the current run is the only group that may still grow. State the first-element rule explicitly, because the first position starts a run without a previous element.

A false friend is the in-place removal of duplicates that was taught for sorted input in the arrays chapter. That technique assumes the input was already sorted, and it is wrong for an unsorted array. Sorting first and then applying it changes the order of the survivors, which is wrong whenever the problem asks for first-appearance order, and a linked hash set is the right tool there.

In Java, do not initialize a "previous value" to a fixed number such as 0, because an input of zeros will be wrongly treated as already seen. Use the index test `i == 0` instead. Sort a clone unless the contract says the argument may change, and remember that a `char` or a string can serve as a run value just as an `int` does.

<!-- stage: exercises -->
### Exercises

#### [Build] Contains Duplicate (LeetCode 217)
<!-- id: so-contains-duplicate-runs -->

**Prerequisites.** The arrays-sort lesson and its in-place variant of this problem.

**Problem.** Return true if some value occurs at least twice, under a different contract from before: the caller's array is read-only, so work on a sorted copy, and decide by measuring the length of each run of equal values.

**Constraints.** 1 <= nums.length <= 100000 and any `int` values. The argument must be unchanged when the method returns.

**Example 1.** Input `nums = [12, 5, 12]`, output true.

**Example 2.** Input `nums = [8, 1, 6, 3]`, output false.

**Hint.** What is the length of the current run when a value repeats? Why must the run counter restart at one and not at zero at a boundary?

**Changed decision.** The argument may not change, so a copy is sorted, and the test becomes a run length reaching two.

#### [Vary] Intersection of Two Arrays (LeetCode 349)
<!-- id: so-intersection-sorted-runs -->

**Prerequisites.** The contains-duplicate exercise above.

**Problem.** Return the values that occur in both arrays, each value once, in ascending order. Reduce each array to its distinct sorted values, join the two reduced lists, sort them, and report each value that occurs twice.

**Constraints.** 1 <= a.length, b.length <= 1000 and 0 <= values <= 1000. Do not use a hash-based set.

**Example 1.** Input `a = [4, 9, 5, 9], b = [9, 4, 9, 8, 4]`, output `[4, 9]`.

**Example 2.** Input `a = [1, 2], b = [3, 4]`, output `[]`.

**Hint.** Why can a value appear at most twice after the two lists are reduced to distinct values? What does a second copy tell you?

**Changed decision.** The question moves from one array to two, and the answer is read from the pairs in a combined sorted list.

#### [Boundary] All Equal (Author exercise)
<!-- id: so-all-equal -->

**Prerequisites.** The two exercises above.

**Problem.** Write the distinct-values routine so that `[4, 4, 4]` returns exactly `[4]`, and show that a version that starts with a made-up previous value of 0 returns an empty result for `[0, 0, 0]`. Test arrays of one value repeated 1 to 20 times.

**Constraints.** 0 <= length <= 100 and any `int` values, including 0 and the extremes. The first element must be emitted without a comparison to a previous element.

**Example 1.** Input `[4, 4, 4]`, output `[4]`.

**Example 2.** Input `[0, 0, 0]`, output `[0]`, where the faulty sentinel version returns `[]`.

**Hint.** What does the first position of the sorted array have to compare with? Which inputs can fool a fixed starting value?

**Changed decision.** The data is one long run, so the start of the scan has to be handled without a made-up predecessor.

#### [Recognize] Longest Word in Dictionary (LeetCode 720)
<!-- id: so-longest-buildable-word -->

**Prerequisites.** All three exercises above.

**Problem.** Given a list of lowercase words, return the longest word that can be built one letter at a time, where every shorter prefix of it, down to a single letter, is also in the list. If several words have the longest length, return the alphabetically smallest, and if none can be built, return the empty string.

**Constraints.** 1 <= words.length <= 1000 and 1 <= each length <= 30. Words may repeat. Sort the words and decide ties by position in the sorted order.

**Example 1.** Input `words = ["cat", "c", "ca", "dog", "do", "d", "dot"]`, output `"cat"`.

**Example 2.** Input `words = ["xy", "xyz"]`, output `""`, since neither word has a one-letter start in the list.

**Hint.** When a word is read in sorted order, has its prefix already been decided? Which of two equally long candidates is met first?

**Changed decision.** The sorted order is chosen so that earlier decisions are final, and the tie rule comes from the order and not from a comparator.
