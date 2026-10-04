<!-- lesson-kind: standard -->
<!-- lesson-id: k-way-merge -->
## K-Way Merge

<!-- stage: context -->
### One Catalogue From Many Shelves

A regional library network runs an annual book sale, and every branch sends over its list of donated books. Each branch keeps its list in call-number order, because its own shelves are arranged that way, but the lists from different branches are unrelated. The organisers want a single sale catalogue in call-number order, to be printed in one run, and the number of branches has grown from four to several hundred.

A volunteer proposed to pick the next book by standing in front of all the branch lists at once, looking at the first unprinted entry of each, and writing down the smallest. It is a pleasant rule for four lists. For several hundred it means glancing at several hundred entries before writing down a single title, and the catalogue has hundreds of thousands of titles.

<!-- stage: naive -->
### Compare Every Branch's Next Entry

The direct method keeps one cursor per source and, for each output slot, scans all cursors for the smallest current value.

```java
static int[] mergeByScan(int[][] sources) {
    int total = 0;
    for (int[] s : sources) total += s.length;
    int[] cursor = new int[sources.length];
    int[] out = new int[total];
    for (int i = 0; i < total; i++) {
        int pick = -1;
        for (int s = 0; s < sources.length; s++) {
            if (cursor[s] == sources[s].length) continue;
            if (pick < 0 || sources[s][cursor[s]] < sources[pick][cursor[pick]]) pick = s;
        }
        out[i] = sources[pick][cursor[pick]++];
    }
    return out;
}
```

It is correct. For the sources `[[1, 4], [2, 3]]` it returns `[1, 2, 3, 4]`.

<!-- stage: bottleneck -->
### Many Comparisons For Every Slot

With `k` sources and `N` values in total, each of the `N` output slots examines up to `k` cursors, so the cost is O(N * k). For four hundred branches and a million titles that is four hundred million comparisons. The comparisons are also mostly repeated: after one title is written, only one cursor has moved, yet the next slot compares all the cursors again, including the ones that are unchanged and were already known to be larger.

The alternative of pouring every title into one list and sorting it costs O(N log N) and needs room for all `N` values at once, and it ignores the one thing known about the input, namely that every source is already in order. What is needed is a structure that remembers the standing of the current entries, so that when one of them is removed and replaced by its successor, only that single change has to be absorbed, at a logarithmic cost in the number of sources and not in the number of titles.

<!-- stage: insight -->
### Only The Front Of Each Line

The **frontier heap** is a min-heap that holds the current front entry of every source that still has entries, and nothing else. Each entry is a triple: the value, the index of its source, and the position within that source. The root is the smallest of the fronts. Since every source is sorted, that value is also the smallest value that has not yet been written, because anything behind a front entry is at least as large as the front entry.

The loop is the **advance step**. Poll the root and write its value to the output. Then move that source's **source cursor** forward by one, and if the source has another value, offer it as the new front. A source that has run out is simply never offered again, so exhausted sources cost nothing.

<!-- names: frontier heap, advance step, source cursor -->

The frontier never holds more than one entry per source, so its size is at most `k`, and each of the `N` output values costs one poll and at most one offer on a heap of that size. The total is O(N log k) time with O(k) memory for the frontier, apart from the output itself. Comparing the triple by value first and source index second makes the order of equal values deterministic, and it also makes the merge stable with respect to the order of the sources. If the cursor and the position were not stored in the entry, the heap would know the smallest value but not where to continue from.

<!-- stage: variables -->
### Triple, Cursor And Output Slot

Each heap entry is `{value, source, position}`. The value is the comparison key, the source index is the tie-break and also tells the loop which array to read from, and the position tells it which element comes next. Positions only move forward, one step at a time, and each source's position changes only when its own entry is polled. The output index advances once per poll, and the loop runs exactly `N` times, where `N` is the sum of the source lengths, computed before the loop. Sources of length zero never enter the heap, and when only one source remains, the heap holds a single entry and the loop degenerates into a plain copy.

<!-- stage: trace -->
### Three Lines Become One

The first run merges the sources `[1, 4, 7]`, `[2, 4, 9]` and `[3, 8]`. The frontier starts with the three fronts 1, 2 and 3. The 1 is polled, and its successor 4 enters, then the 2 is polled and its successor 4 enters, and the 3 follows with its successor 8. At that point the frontier holds the two 4s and the 8. The two 4s leave one after the other, the first from source 0 because of the tie-break. The 7, the 8 and the 9 follow, and each of them ends its source, so the frontier shrinks as the run finishes. The output is `[1, 2, 3, 4, 4, 7, 8, 9]`.

The second run merges `[1, 2, 3, 4]`, `[10]` and `[5, 6]`. The first source supplies four values in a row, since its fronts stay smaller than the others. The long source then runs out, the frontier shrinks to two entries and then to one, and the 10 waits until the very end. The step to study is the poll of the 4, after which the source is exhausted and nothing is offered.

```trace
{"cells":[1,4,7,2,4,9,3,8],"pointers":["polled"],"steps":[{"at":{"polled":0},"vars":{"frontier":"[(2,s1),(3,s2),(4,s0)]","output":"[1]"},"note":"The front 1 of source 0 is polled and written. Its successor 4 enters the frontier."},{"at":{"polled":3},"vars":{"frontier":"[(3,s2),(4,s0),(4,s1)]","output":"[1,2]"},"note":"The front 2 of source 1 is polled and written. Its successor 4 enters the frontier."},{"at":{"polled":6},"vars":{"frontier":"[(4,s0),(4,s1),(8,s2)]","output":"[1,2,3]"},"note":"The front 3 of source 2 is polled and written. Its successor 8 enters the frontier."},{"at":{"polled":1},"vars":{"frontier":"[(4,s1),(7,s0),(8,s2)]","output":"[1,2,3,4]"},"note":"The front 4 of source 0 is polled and written. Its successor 7 enters the frontier."},{"at":{"polled":4},"vars":{"frontier":"[(7,s0),(8,s2),(9,s1)]","output":"[1,2,3,4,4]"},"note":"The front 4 of source 1 is polled and written. Its successor 9 enters the frontier."},{"at":{"polled":2},"vars":{"frontier":"[(8,s2),(9,s1)]","output":"[1,2,3,4,4,7]"},"note":"The front 7 of source 0 is polled and written. Source 0 is exhausted, so nothing is offered."},{"at":{"polled":7},"vars":{"frontier":"[(9,s1)]","output":"[1,2,3,4,4,7,8]"},"note":"The front 8 of source 2 is polled and written. Source 2 is exhausted, so nothing is offered."},{"at":{"polled":5},"vars":{"frontier":"[]","output":"[1,2,3,4,4,7,8,9]"},"note":"The front 9 of source 1 is polled and written. Source 1 is exhausted, so nothing is offered."}]}
```

```trace
{"cells":[1,2,3,4,10,5,6],"pointers":["polled"],"steps":[{"at":{"polled":0},"vars":{"frontier":"[(2,s0),(5,s2),(10,s1)]","output":"[1]"},"note":"The front 1 of source 0 is polled and written. Its successor 2 enters the frontier."},{"at":{"polled":1},"vars":{"frontier":"[(3,s0),(5,s2),(10,s1)]","output":"[1,2]"},"note":"The front 2 of source 0 is polled and written. Its successor 3 enters the frontier."},{"at":{"polled":2},"vars":{"frontier":"[(4,s0),(5,s2),(10,s1)]","output":"[1,2,3]"},"note":"The front 3 of source 0 is polled and written. Its successor 4 enters the frontier."},{"at":{"polled":3},"vars":{"frontier":"[(5,s2),(10,s1)]","output":"[1,2,3,4]"},"note":"The front 4 of source 0 is polled and written. Source 0 is exhausted, so nothing is offered."},{"at":{"polled":5},"vars":{"frontier":"[(6,s2),(10,s1)]","output":"[1,2,3,4,5]"},"note":"The front 5 of source 2 is polled and written. Its successor 6 enters the frontier."},{"at":{"polled":6},"vars":{"frontier":"[(10,s1)]","output":"[1,2,3,4,5,6]"},"note":"The front 6 of source 2 is polled and written. Source 2 is exhausted, so nothing is offered."},{"at":{"polled":4},"vars":{"frontier":"[]","output":"[1,2,3,4,5,6,10]"},"note":"The front 10 of source 1 is polled and written. Source 1 is exhausted, so nothing is offered."}]}
```

<!-- stage: code -->
### Merging With A Frontier Heap

```java
static int[] mergeSorted(int[][] sources) {
    java.util.PriorityQueue<int[]> frontier = new java.util.PriorityQueue<>(
        java.util.Comparator.<int[]>comparingInt(e -> e[0]).thenComparingInt(e -> e[1]));
    int total = 0;
    for (int s = 0; s < sources.length; s++) {
        total += sources[s].length;
        if (sources[s].length > 0) frontier.offer(new int[]{sources[s][0], s, 0});
    }
    int[] out = new int[total];
    for (int i = 0; i < total; i++) {
        int[] head = frontier.poll();                    // smallest front
        out[i] = head[0];
        int next = head[2] + 1;
        if (next < sources[head[1]].length) {
            frontier.offer(new int[]{sources[head[1]][next], head[1], next});
        }
    }
    return out;
}
```

The first loop costs O(k log k), and the second performs N polls and at most N offers on a heap of at most `k` entries, so the whole method is O(k log k + N log k). The frontier is the only structure beyond the output, with at most `k` entries. The poll in the second loop never returns `null`, because the loop runs exactly `total` times and each poll is followed by an offer of that source's successor while one exists, so the frontier is non-empty whenever unwritten values remain.

<!-- stage: applicability -->
### When Sorted Streams Must Interleave

Use a frontier heap when several inputs are each sorted by the same key, and the output, or the first few outputs, must be one sequence ordered by that key. The invariant is that the heap holds exactly one front entry for each non-exhausted source, and that its root is the smallest value that has not been written. The same shape handles sorted lists, sorted rows of a matrix, and files read in blocks, as long as the next entry of a source can be reached from the previous one.

The false friend is a heap that is loaded with every value at the start. It produces the same output, but it needs O(N) memory instead of O(k), it spends a logarithm of `N` and not of `k` on each value, and it can never be used on a source that is read as a stream. Another false friend is a repeated two-way merge from left to right, which looks like a divide-and-conquer but gives O(N * k) when the accumulated result keeps growing, unless the merges are arranged in a balanced tree.

Do not use it when the sources are not sorted by the key in use, or when `k` is two, where two cursors on two arrays are simpler and constant in memory. In Java, a heap of linked-list nodes needs an explicit comparator on the node value, because the node class has no natural order and the queue would throw a `ClassCastException` on the second offer.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Three Sorted Arrays (Author exercise)
<!-- id: hp-merge-three-arrays -->

**Prerequisites.** The frontier heap, the advance step and the source cursor of this lesson.

**Problem.** Given three sorted integer arrays `a`, `b` and `c`, return one sorted array with all of their values. Keep one front entry per array in a `PriorityQueue`, each entry holding the value, the array number and the position.

**Constraints.** 1 <= a.length + b.length + c.length <= 10^5, each array is in nondecreasing order, and values are between -10^9 and 10^9.

**Example 1.** Input `a = [1, 5, 9]`, `b = [2, 6]`, `c = [0, 3, 10]`, output `[0, 1, 2, 3, 5, 6, 9, 10]`.

**Example 2.** Input `a = [4]`, `b = [4]`, `c = [4, 4]`, output `[4, 4, 4, 4]`.

**Hint.** What does the entry need to carry so that the next front of the same array can be found? How many entries can the queue hold at once?

**Changed decision.** First rung: three fixed sources, the triple entry, and the advance step, without any lists, empty cases or tie rules to think about.

#### [Vary] Merge k Sorted Lists (LeetCode 23)
<!-- id: hp-merge-k-lists -->

**Prerequisites.** Merge Three Sorted Arrays above.

**Problem.** Given an array of `k` singly linked lists, each sorted in ascending order, merge them into one sorted linked list and return its head. The input lists are encoded as arrays of values, and the merged list must reuse the original nodes.

**Constraints.** 0 <= k <= 10^4, the total number of nodes is at most 10^4, and node values are between -10^4 and 10^4.

**Example 1.** Input `lists = [[2, 5], [1, 6, 8], [3]]`, output `[1, 2, 3, 5, 6, 8]`.

**Example 2.** Input `lists = [[]]`, output `[]`.

**Hint.** What does a node already know about the position of the next entry of its list? What must the heap's comparator read, given that nodes are not comparable?

**Changed decision.** The entries are list nodes, so the successor is `node.next` and no position is stored, and the comparator must be supplied for the node type.

#### [Boundary] Empty Sources And Equal Heads (Author exercise)
<!-- id: hp-empty-sources-equal-heads -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `sources` of sorted integer arrays, some of which may be empty, return the source indices in the order in which their values are written by the merge, where equal values leave the lower source index first.

**Constraints.** 1 <= sources.length <= 1000, the total number of values is at most 10^5, and each source is in nondecreasing order. Some sources may have length 0.

**Example 1.** Input `sources = [[], [5, 5], [5], []]`, output `[1, 1, 2]`.

**Example 2.** Input `sources = [[2], [1, 2], [2]]`, output `[1, 0, 1, 2]`.

**Hint.** Which sources are allowed to enter the queue at the start? Which field of the entry settles a tie between equal values?

**Changed decision.** Sources may be empty and heads may be equal, so the entry rule and the comparator's second field now decide the answer.

#### [Recognize] Kth Smallest Element in a Sorted Matrix (LeetCode 378)
<!-- id: hp-kth-smallest-matrix -->

**Prerequisites.** All three exercises above.

**Problem.** Given an `n x n` matrix in which every row and every column is sorted in nondecreasing order, return the k-th smallest value of the whole matrix, counting duplicates separately.

**Constraints.** 1 <= n <= 300, 1 <= k <= n * n, and values are between -10^9 and 10^9.

**Example 1.** Input `matrix = [[1, 4, 8], [2, 5, 9], [3, 6, 12]]`, `k = 5`, output 5.

**Example 2.** Input `matrix = [[2, 2], [2, 3]]`, `k = 3`, output 2.

**Hint.** Each row is a sorted source. How many entries does the frontier need at the start, and how many polls do you make before the answer appears?

**Changed decision.** The sources are rows of a grid, and the loop stops after `k` polls instead of exhausting the sources.
