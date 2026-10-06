<!-- lesson-kind: standard -->
<!-- lesson-id: k-way-merge -->
## Merge Sorted Lists With A Heap

<!-- stage: context -->
### Why The Log Viewer Stalls

A log viewer shows the combined timeline of 200 servers. Each server writes its own log file in time order, so every file is already sorted. The first version of the viewer reads all files into one array, sorts the array and shows the first page. With 10 million events the viewer needs several seconds and gigabytes of memory before it shows anything.

The viewer should show the first page almost at once, and it should not hold every event in memory. This lesson asks how a program merges many sorted files into one sorted stream while it reads only a few values from each file at a time.

<!-- stage: naive -->
### Reading The Next Value Of Each File

The direct plan keeps one read position for each file. To produce the next output value, it scans all positions and picks the file whose next value is smallest.

```java
static int[] mergeByScan(int[][] files) {
    int total = 0;
    for (int[] f : files) total += f.length;
    int[] pos = new int[files.length];                 // next unread position in each file
    int[] out = new int[total];
    for (int w = 0; w < total; w++) {
        int best = -1;                                 // file number holding the smallest next value
        for (int s = 0; s < files.length; s++) {
            if (pos[s] < files[s].length
                    && (best == -1 || files[s][pos[s]] < files[best][pos[best]])) best = s;
        }
        out[w] = files[best][pos[best]++];             // take that value and advance its file
    }
    return out;
}
```

The method is correct, and it reads each file only through its own position.

<!-- stage: bottleneck -->
### Counting Scans Per Output Value

```predict
The viewer merges k = 200 files with N = 10,000,000 events in total. About how many comparisons does the scan method perform?

Each of the N output values scans all k files, so it performs about N * k = 2 * 10^9 comparisons. That is O(N * k), and most of the comparisons repeat work from the previous output value.
```

Each output value costs O(k), so the full merge costs O(N * k). The waste is repeated work. After the program takes one value from file 7, the next values of the other 199 files have not changed. The next scan compares them with each other again and finds the same relative order.

The program needs to remember the order among the other files and update it only for the one file that moved. That is the same job that the first lesson of this chapter solved for a changing set of numbers.

<!-- stage: insight -->
### Keeping One Value Per File

The program keeps a `PriorityQueue` that holds the next unread value of each file. That set of values is the **frontier**. Each file has at most one entry in the frontier, so the queue never holds more than `k` entries.

#### Choosing The Next Output Value

Every file is sorted, so the smallest unread value of a file is its next unread value. The smallest unread value over all files is therefore the smallest entry in the frontier. `poll` returns that entry, and the program appends its value to the output.

#### Refilling The Frontier

The entry that just left belongs to one file, so the program needs to know which file and which position. Each entry stores three numbers: the value, the **source index** of its file, and the position in that file. After `poll`, the program reads the **successor**, which is the next value in the same file. It offers the successor when the file has one and does nothing otherwise.

#### Keeping The Cost Low

Each output value costs one `poll` and at most one `offer` on a queue of at most `k` entries, which is O(log k). The merge costs O(N log k) time. The extra memory is O(k) for the frontier, and the output needs O(N) only when the program stores it.

<!-- names: frontier, source index, successor -->

<!-- stage: variables -->
### Three Numbers In Every Entry

The queue stores small arrays, and each array has three fields that change at different times.

- **Value** is the number that the queue orders by, and it never changes after the entry is created.
- **Source index** says which input file the value came from, and it stays fixed for the life of the entry.
- **Position** says where the value sits in its file, and the successor entry uses position plus one.
- **Output count** counts values written so far, and the merge stops when it equals the total length.

The queue holds exactly one entry for each file that still has unread values.

<!-- stage: trace -->
### Merging Files Step By Step

#### Merging Three Files

Take the files `[1, 4, 7]`, `[2, 5]` and `[3, 6, 9]`. In the first trace the pointer `out` marks the output position just written. The variable `frontier` lists the entries as `value from source index`.

The frontier starts with 1, 2 and 3, one entry per file. The first poll returns 1 from file 0, and file 0 offers its successor 4. The next polls return 2 and 3 and refill the frontier with 5 and 6. The frontier always holds three entries until file 1 runs out after its value 5. From then on it holds two entries and then one, and the output ends as 1, 2, 3, 4, 5, 6, 7, 9.

#### Merging With An Empty File And Equal Values

The second trace merges `[2, 2]`, an empty file and `[2, 3]`. The empty file adds no entry to the frontier at the start. Two equal values 2 sit in the frontier at the start. The comparator breaks the tie by source index, so file 0 leaves first, and its successor 2 leaves next for the same reason. The output is 2, 2, 2, 3.

#### Stepping Through Both Merges

```trace
{"cells":[1,2,3,4,5,6,7,9],"pointers":["out"],"steps":[{"at":{"out":-1},"vars":{"frontier":"[1 from 0, 2 from 1, 3 from 2]"},"note":"The frontier starts with the first value of each non-empty file: [1 from 0, 2 from 1, 3 from 2]."},{"at":{"out":0},"vars":{"frontier":"[2 from 1, 3 from 2, 4 from 0]"},"note":"The poll returns 1 from file 0. File 0 offers its successor 4."},{"at":{"out":1},"vars":{"frontier":"[3 from 2, 4 from 0, 5 from 1]"},"note":"The poll returns 2 from file 1. File 1 offers its successor 5."},{"at":{"out":2},"vars":{"frontier":"[4 from 0, 5 from 1, 6 from 2]"},"note":"The poll returns 3 from file 2. File 2 offers its successor 6."},{"at":{"out":3},"vars":{"frontier":"[5 from 1, 6 from 2, 7 from 0]"},"note":"The poll returns 4 from file 0. File 0 offers its successor 7."},{"at":{"out":4},"vars":{"frontier":"[6 from 2, 7 from 0]"},"note":"The poll returns 5 from file 1. File 1 has no successor, so the frontier shrinks."},{"at":{"out":5},"vars":{"frontier":"[7 from 0, 9 from 2]"},"note":"The poll returns 6 from file 2. File 2 offers its successor 9."},{"at":{"out":6},"vars":{"frontier":"[9 from 2]"},"note":"The poll returns 7 from file 0. File 0 has no successor, so the frontier shrinks."},{"at":{"out":7},"vars":{"frontier":"[]"},"note":"The poll returns 9 from file 2. File 2 has no successor, so the frontier shrinks."}]}
```

```trace
{"cells":[2,2,2,3],"pointers":["out"],"steps":[{"at":{"out":-1},"vars":{"frontier":"[2 from 0, 2 from 2]"},"note":"The frontier starts with the first value of each non-empty file: [2 from 0, 2 from 2]."},{"at":{"out":0},"vars":{"frontier":"[2 from 0, 2 from 2]"},"note":"The poll returns 2 from file 0. File 0 offers its successor 2."},{"at":{"out":1},"vars":{"frontier":"[2 from 2]"},"note":"The poll returns 2 from file 0. File 0 has no successor, so the frontier shrinks."},{"at":{"out":2},"vars":{"frontier":"[3 from 2]"},"note":"The poll returns 2 from file 2. File 2 offers its successor 3."},{"at":{"out":3},"vars":{"frontier":"[]"},"note":"The poll returns 3 from file 2. File 2 has no successor, so the frontier shrinks."}]}
```

<!-- stage: code -->
### Merging Sorted Arrays In Java

#### The Merge Method

Each entry is an `int[]` with the value, the source index and the position. The comparator reads the value first and breaks ties with the source index.

```java
static int[] merge(int[][] sources) {
    PriorityQueue<int[]> frontier = new PriorityQueue<>((a, b) ->
        a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
    int total = 0;
    for (int s = 0; s < sources.length; s++) {
        total += sources[s].length;
        if (sources[s].length > 0) frontier.offer(new int[] {sources[s][0], s, 0});   // the first value of each non-empty file
    }
    int[] out = new int[total];
    int w = 0;
    while (!frontier.isEmpty()) {
        int[] top = frontier.poll();                    // the smallest unread value over all files
        out[w++] = top[0];
        int next = top[2] + 1;                          // position of the successor in the same file
        if (next < sources[top[1]].length) {
            frontier.offer(new int[] {sources[top[1]][next], top[1], next});
        }
    }
    return out;
}
```

#### Costs Of The Merge

The merge makes N polls and at most N offers on a queue of size `k` or less. Time is O(N log k) and the frontier needs O(k) memory. For `k = 1` the loop reduces to copying the single file.

<!-- stage: applicability -->
### Recognizing A Many Streams Question

#### Spotting The Pattern

The cue is several inputs that are each sorted, and a question that asks for the next global value again and again. The invariant is that the frontier holds exactly one entry for each file that still has unread values, so its root is the next global value.

#### Finding The False Friend

The false friend is inserting every value from every file into one queue. That queue also returns the correct order. It holds N entries, so it loses the O(k) memory bound and spends O(N) before the first output value appears.

A second false friend is a merge of exactly two sorted arrays. Two pointers do that job with no queue and O(N) time.

#### Recognizing The No-Go Cases

The method needs every input sorted by the same order. Unsorted inputs break the claim that a file's next value is its smallest, and the frontier then returns a wrong order. For a very large `k` with small files, sorting all values once can be simpler.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Three Sorted Arrays (Author exercise)
<!-- id: hp-merge-three -->

**Prerequisites.** The frontier entry with value, source index and position.

**Problem.** Given three arrays `a`, `b` and `c`, each sorted in nondecreasing order, return one array that holds all their values in nondecreasing order. Use a `PriorityQueue` that holds at most one entry for each array, and store the value, the array number and the position in each entry.

**Constraints.** The limits are:
- **Lengths** satisfy `0 <= a.length, b.length, c.length <= 10^5`.
- **Values** are `int` values, and duplicates are allowed.
- **Mutation** does not occur; the three inputs keep their contents.

**Example 1.** Input `a = [1,4,9]`, `b = [2,3]` and `c = [0,8]`, output `[0,1,2,3,4,8,9]`.

**Example 2.** Input `a = [5]`, `b = [5]` and `c = [5]`, output `[5,5,5]`.

**Hint.** Which entry must the program offer after it polls an entry from array `b`? What does the position field tell it?

**Changed decision.** The queue refills from the array of the polled entry, so it holds three entries at most.

#### [Vary] Merge k Sorted Lists (LeetCode 23)
<!-- id: hp-merge-k-lists -->

**Prerequisites.** The previous exercise and the linked list node from Chapter 14.

**Problem.** Given an array `lists` of `k` heads of singly linked lists, each sorted in nondecreasing order by `val`, return the head of one sorted list. Reuse the existing nodes by relinking `next`, and create no new list nodes. A null head means an empty list. Poll one node and offer its `next` node.

**Constraints.** The limits are:
- **k** satisfies `0 <= k <= 10^4`, and any head can be null.
- **Total nodes** number at most `10^5`, and values are `int` values.
- **Return** is the head of the merged list, or null when there are no nodes.
- **Mutation** is allowed on `next` fields only.

**Example 1.** Input `lists = [[2,5,8],[1,5],[3]]`, output `[1,2,3,5,5,8]`.

**Example 2.** Input `lists = []`, output `[]`.

**Hint.** What replaces the position field when each entry is a node? Which entry does the program offer after a poll?

**Changed decision.** The queue stores nodes, and the successor is the node's own `next` reference.

#### [Boundary] Empty Sources And Equal Heads (Author exercise)
<!-- id: hp-empty-equal-heads -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `sources` of sorted `int` arrays, some of them empty, merge them. Return the source index of each output value in output order. When two sources show equal values at the same time, the source with the smaller index goes first.

**Constraints.** The limits are:
- **Sources** number `0 <= sources.length <= 10^3`, and each source holds `0` to `10^3` values.
- **Values** are `int` values, and each source is sorted in nondecreasing order.
- **Ties** between equal values always resolve by the smaller source index.
- **Answer** is an `int[]` with one source index for each output value.

**Example 1.** Input `sources = [[1,3],[],[1,2]]`, output `[0,2,2,0]`.

**Example 2.** Input `sources = [[],[]]`, output `[]`.

**Hint.** Which sources get an entry at the start? Which field of the comparator breaks the tie?

**Changed decision.** Empty sources add no entry, and the comparator reads the source index on equal values.

#### [Recognize] Kth Smallest Element in a Sorted Matrix (LeetCode 378)
<!-- id: hp-kth-smallest-matrix -->

**Prerequisites.** All three exercises above.

**Problem.** Given an `n x n` matrix `matrix` and an integer `k`, return the kth smallest of all `n * n` values, counting duplicates. Every row and every column is sorted in nondecreasing order. Treat each row as a sorted file and stop after `k` polls.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 300`.
- **Values** are `int` values, and duplicates are allowed.
- **k** satisfies `1 <= k <= n * n`.
- **Mutation** does not occur; `matrix` keeps its contents.

**Example 1.** Input `matrix = [[2,3,7],[4,6,8],[5,9,10]]` and `k = 5`, output 6.

**Example 2.** Input `matrix = [[4]]` and `k = 1`, output 4.

**Hint.** Which entries must the queue hold at the start? Does the program need to read past the kth poll?

**Changed decision.** The merge stops after `k` polls and returns the last polled value.
