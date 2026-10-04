<!-- lesson-kind: standard -->
<!-- lesson-id: sort-and-deduplicate -->
## Remove Duplicates After Sorting

<!-- stage: context -->
### An Order Report That Lists Numbers Twice

A shop exports a daily report of order numbers. Customers resubmit forms, so the same number can appear many times in the raw feed. The report must list each number once, in ascending order, and show how many times it appeared. A first version collects the numbers in a hash set. It drops the counts, and it prints the numbers in an order that looks random. A second version keeps a list of the numbers it has seen so far, and it takes minutes on a feed of 200000 rows.

Both versions answer a different question than the report asks. The report needs one entry per distinct number and one count, in a fixed order. This lesson answers one question. What order of the feed makes equal numbers easy to find, so that one pass produces the whole report?

<!-- stage: naive -->
### Searching The List Of Seen Numbers

The direct method keeps a list of pairs, each with a number and its count. For every row of the feed, it searches the list for the number and adds 1 to the count, or it appends a new pair.

```java
static List<int[]> countRuns(int[] feed) {
    List<int[]> report = new ArrayList<>();
    for (int x : feed) {
        boolean found = false;
        for (int[] entry : report) {
            if (entry[0] == x) {
                entry[1]++;
                found = true;
                break;
            }
        }
        if (!found) {
            report.add(new int[] {x, 1});
        }
    }
    return report;
}
```

On the feed `[4, 7, 4, 9]` the method returns the pairs `(4, 2)`, `(7, 1)` and `(9, 1)`. The pairs appear in the order of first appearance.

<!-- stage: bottleneck -->
### Every Row Searches The Whole List

```predict
The feed holds 200000 distinct numbers. About how many entry comparisons does the method make, and is its output ascending?

Each row compares with every entry added so far, so the total is about n * (n - 1) / 2, which is roughly 20 billion and O(n^2). The output follows the order of first appearance, so it is ascending only when the feed happens to be ascending.
```

The search for a number repeats work for every row, and the list holds up to n entries. The method also fixes the output order by accident, since it lists numbers by first appearance. A report with a required order would need a second sort of the pairs. If equal numbers were next to each other in the feed, no search would be needed. The row after a number would either match it or start a new number.

<!-- stage: insight -->
### Sort The Feed And Read Groups

Sorting the feed puts equal numbers next to each other and puts the numbers themselves in the order that the report needs.

#### Equal Values Form One Run

A **run** is a maximal block of adjacent positions that hold the same value. After the sort, each distinct value owns exactly one run, because a value cannot reappear after a larger value begins. The runs also appear in ascending order of their values.

#### One Entry Per Run

The **run length** is the number of positions in a run, and it equals the count of the value in the feed. The program starts a run at index `i`, moves a second index `j` to the end of the run, and emits the pair `(value, j - i)`. It then continues at `j`. Each index of the array is read once, so the scan costs O(n).

#### Keep One Representative

A **representative** is the single value that stands for a whole run. The program emits `sorted[i]` and ignores the other positions of the run. The invariant at the start of each outer step is that every run to the left of `i` has been emitted exactly once, and no run to the right has been touched.

<!-- names: run, run length, representative -->

#### What The Pass Costs

The sort costs O(n log n) and the scan costs O(n), so sorting dominates. The pass needs only the two indexes and the output list. The copy for sorting adds O(n) space when the caller's feed must stay unchanged.

<!-- stage: variables -->
### Start, End And The Report

The scan uses a few pieces of state.

- **sorted** is the sorted copy of the feed.
- **i** is the first index of the current run.
- **j** is the first index after the current run, and it moves right while the value stays equal.
- **report** is the list of emitted pairs of value and count.

Only the current run is unresolved at any time, and `i` jumps to `j` when the run ends.

<!-- stage: trace -->
### Two Feeds Read In Groups

#### A Feed With Three Distinct Numbers

Take the feed `[4, 7, 4, 9, 7, 4]`. After sorting it is `4, 4, 4, 7, 7, 9`. The first run starts at index 0 and stops before index 3, so it has length 3. The second run covers indexes 3 and 4 with length 2. The last run holds the 9 at index 5 with length 1.

#### A Feed Where Every Number Is Equal

Now take `[4, 4, 4]`. There is one run, and the second index moves to the end of the array before the pair is emitted. The scan emits `(4, 3)`. A method that emits a pair only when the next value differs would miss this pair, because no later value exists. The loop above never has that problem, since the end of the array also ends a run.

#### Stepping Through Both Feeds

```trace
{"cells":[4,4,4,7,7,9],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":0},"vars":{"report":"[]"},"note":"Start: the first run begins at index 0."},{"at":{"i":0,"j":3},"vars":{"value":4,"report":"[(4, 3)]"},"note":"The run of 4 spans indexes 0 to 2, so the length is 3. Emit (4, 3) and continue at index 3."},{"at":{"i":3,"j":5},"vars":{"value":7,"report":"[(4, 3), (7, 2)]"},"note":"The run of 7 spans indexes 3 to 4, so the length is 2. Emit (7, 2) and continue at index 5."},{"at":{"i":5,"j":6},"vars":{"value":9,"report":"[(4, 3), (7, 2), (9, 1)]"},"note":"The run of 9 spans indexes 5 to 5, so the length is 1. Emit (9, 1) and continue at index 6."},{"at":{"i":6,"j":6},"vars":{"report":"[(4, 3), (7, 2), (9, 1)]"},"note":"The loop ends because i reaches the array length. The report holds three pairs."}]}
```

```trace
{"cells":[4,4,4],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":0},"vars":{"report":"[]"},"note":"Start: the first run begins at index 0."},{"at":{"i":0,"j":1},"vars":{"value":4,"report":"[]"},"note":"Index 0 holds 4, so the run extends. The end index moves to 1."},{"at":{"i":0,"j":2},"vars":{"value":4,"report":"[]"},"note":"Index 1 holds 4, so the run extends. The end index moves to 2."},{"at":{"i":0,"j":3},"vars":{"value":4,"report":"[]"},"note":"Index 2 holds 4, so the run extends. The end index moves to 3."},{"at":{"i":0,"j":3},"vars":{"value":4,"report":"[(4, 3)]"},"note":"The run of 4 spans indexes 0 to 2, so the length is 3. Emit (4, 3) and continue at index 3."},{"at":{"i":3,"j":3},"vars":{"report":"[(4, 3)]"},"note":"The loop ends because i reaches the array length. The single run was emitted without a later value."}]}
```

<!-- stage: code -->
### Find The End Of Each Run

#### Counting Runs

```java
static List<int[]> countRuns(int[] feed) {
    int[] sorted = Arrays.copyOf(feed, feed.length);
    Arrays.sort(sorted);
    List<int[]> report = new ArrayList<>();
    int i = 0;
    while (i < sorted.length) {
        int j = i;
        while (j < sorted.length && sorted[j] == sorted[i]) {
            j++;
        }
        report.add(new int[] {sorted[i], j - i});
        i = j;
    }
    return report;
}
```

#### What The Method Costs

The sort takes O(n log n) time. The loops together visit each index once, so the scan takes O(n) time. The copy and the report take O(n) space in the worst case of all distinct values.

<!-- stage: applicability -->
### When Sorting Groups The Duplicates

#### Look For One Answer Per Value

Use sort and scan when the answer needs one item or one count for each distinct value, and the order of the answer is ascending or can be chosen. The invariant is that the current run is the only unresolved group. The method fits when memory for a hash set is unwanted, or when a canonical order is part of the output.

#### Where Sorting Is Not The Tool

A false friend is a method that assumes the input is already sorted. Such a method gives wrong counts on unsorted input, so the sort must come first. Another false friend is a problem that needs only existence, such as whether any duplicate exists. A hash set answers that question in O(n) expected time without an order, so a sort costs more than the question needs. If the answer must follow the order of first appearance, sorting destroys the information, unless the program stores indexes first.

#### Java Details That Cause Failures

Compare array values with `==` on primitives, and use `equals` on boxed values, because `==` on two `Integer` objects compares references. The inner loop must test `j < sorted.length` before it reads `sorted[j]`. Emit the last run after the loop, or let the inner loop end at the array boundary as the code above does.

<!-- stage: exercises -->
### Exercises

#### [Build] Contains Duplicate (LeetCode 217)
<!-- id: so-extra-copies -->

**Prerequisites.** Runs and run lengths from this lesson.

**Problem.** Suppose `nums` holds integers. Return the number of positions that must be deleted so that no value occurs twice. This version counts the extra copies, and it changes the contract of the original problem, which returns only whether a duplicate exists.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers, and negative values are legal.
- **Answer** is 0 when all values are distinct.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [6, 2, 6, 6, 2, 9]`, output 3, because 6 occurs three times and 2 occurs twice.

**Example 2.** Input `nums = [5, -5, 0]`, output 0.

**Hint.** What does each run contribute beyond its first position?

**Changed decision.** Basic case: the answer sums the run lengths minus one, so a boolean becomes a count.

#### [Vary] Intersection Of Two Arrays (LeetCode 349)
<!-- id: so-common-values -->

**Prerequisites.** Contains Duplicate above.

**Problem.** Let `a` and `b` be integer arrays. Return an `int[]` that holds each value present in both arrays exactly once, in ascending order. This version returns the values in sorted order, and it must find them without a hash set.

**Constraints.** The limits are:
- **Length** satisfies `0 <= a.length, b.length <= 10^4`.
- **Values** are 32-bit integers, including negative values.
- **Duplicates** may occur inside either array.
- **Mutation** of `a` and `b` is not allowed.

**Example 1.** Input `a = [8, 3, 8, -1]`, `b = [3, 8, 8, 0]`, output `[3, 8]`.

**Example 2.** Input `a = [-2, -2]`, `b = [-2, 5]`, output `[-2]`.

**Hint.** If both arrays go into one sorted sequence with a tag for the source, what must a run contain to prove that a value is common?

**Changed decision.** A run must hold both sources, so the scan reads a tag next to each value.

#### [Boundary] All Equal (Author exercise)
<!-- id: so-distinct-ascending -->

**Prerequisites.** The two exercises above.

**Problem.** Starting from the integer array `nums`, return the distinct values of `nums` in ascending order, each once. The input may be empty, may hold one value, or may hold the same value many times.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Answer** has one entry for each distinct value.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [4, 4, 4]`, output `[4]`.

**Example 2.** Input `nums = [2147483647, -2147483648, 2147483647]`, output `[-2147483648, 2147483647]`.

**Hint.** Where does the last run end, and which loop condition stops the inner scan at the array boundary?

**Changed decision.** The last run has no following value to mark its end, so the end of the array must end it.

#### [Recognize] Longest Word In Dictionary (LeetCode 720)
<!-- id: so-buildable-word -->

**Prerequisites.** All three exercises above.

**Problem.** Let `words` be an array of lowercase strings. A word is buildable when every prefix of it with length from 1 up to its length minus one is also in `words`. Return the longest buildable word. Among words of the same length, return the one that comes first alphabetically. Return the empty string when `words` is empty.

**Constraints.** The limits are:
- **Length** satisfies `0 <= words.length <= 1000`.
- **Words** are non-empty strings of lowercase letters with length at most 30, and the same word can repeat.
- **Single letters** are buildable.
- **Mutation** of `words` is not allowed.

**Example 1.** Input `words = ["t", "ta", "tan", "tank", "tab", "x", "xyz"]`, output `"tank"`.

**Example 2.** Input `words = ["m", "mo", "ma", "mop"]`, output `"mop"`.

**Hint.** In sorted order, where does a word appear compared with its prefixes, which set of buildable words does the scan keep, and which buildable word does the scan see first among equal lengths?

**Changed decision.** Sorted order places every prefix before its words and makes the tie choice deterministic.
