<!-- lesson-kind: standard -->
<!-- lesson-id: merge-counting -->
## Merge Counting

<!-- stage: context -->
### Why Comparing Every Pair Is Too Slow

A search engine ranks 100,000 results for a query. An older ranking of the same results exists, and the team wants one number that says how much the two rankings disagree. The number is the count of result pairs that appear in opposite order in the two rankings. A low count means the new ranking changed little. A high count means it reshuffled the list.

The same question appears in many programs. A fraud check counts how many transactions arrive out of timestamp order. A sync tool counts how many edits were applied out of sequence. In each case the program holds an array and must count the pairs of positions `i < j` where the earlier value is larger than the later value. An array of 100,000 values holds almost five billion such pairs to examine. This lesson answers how to get the total without visiting each pair.

<!-- stage: naive -->
### Checking Every Pair With Two Loops

The direct approach fixes each earlier position and compares it with every later position. The method below counts one pair for each position pair where the earlier value is larger.

```java
static long countPairsSlowly(int[] a) {
    long count = 0;                              // a long holds counts above two billion
    for (int i = 0; i < a.length; i++) {
        for (int j = i + 1; j < a.length; j++) {
            if (a[i] > a[j]) {
                count++;                         // one pair out of order
            }
        }
    }
    return count;
}
```

The outer loop picks the earlier position and the inner loop visits every later position. The method is correct on every input and needs no extra memory. The only question is the number of comparisons.

<!-- stage: bottleneck -->
### Pair Checks Cost O(n^2)

```predict
An array has 100,000 values. How many comparisons does the double loop make, and is that count larger than the biggest `int`?

It makes 4,999,950,000 comparisons, which is n * (n - 1) / 2. The biggest `int` is 2,147,483,647, so the count is more than twice as large. The answer itself can reach the same size, so the counter must be a `long`.
```

#### Count The Comparisons

The pair `(i, j)` is checked once for each `i < j`. That gives n * (n - 1) / 2 comparisons, so the cost is O(n^2). For `n = 100,000` the loops make about five billion comparisons. A typical machine runs a few hundred million simple comparisons per second, so the run takes ten seconds or more. A limit of one or two seconds fails.

#### Find The Wasted Work

The loops treat every pair as unrelated to the others. Suppose the program already knows that `a[5]` is larger than `a[9]` and that `a[9]` is larger than `a[12]`. Then `a[5]` is larger than `a[12]`, and the third comparison adds no information. Sorted order carries exactly this kind of knowledge. If a group of values is sorted, one comparison against that group can settle many pairs at once. The structure we need must put values in sorted order while the program still counts the pairs that sorting would otherwise erase.

<!-- stage: insight -->
### Count Between Halves Before Merging

#### Define The Count

An **inversion** is a pair of positions `i < j` with `a[i] > a[j]`. The goal is to count all inversions of the array. Merge sort splits the array into a left half and a right half, sorts each half recursively, and merges the two sorted halves. Every inversion falls into exactly one of three groups. Both positions are in the left half, both are in the right half, or one is in each half.

#### Split The Pairs

A pair with one position in each half is a **cross pair**. The recursion already counts the other two groups, because each half is a smaller copy of the same problem. Only the cross pairs remain. For a cross pair the left position is always smaller than the right position, so the pair is an inversion exactly when the left value is larger than the right value. The order of values inside each half does not matter for this test. That fact lets the program sort both halves first, and it still counts the same cross pairs.

<!-- names: inversion, cross pair, counting pass -->

#### Count A Whole Suffix At Once

Take two sorted halves. Compare the current left value `a[i]` with the current right value `a[j]`. If `a[i] <= a[j]`, the value `a[i]` is not larger than `a[j]` or any later right value, so it forms no cross pair with the unread right values. The left pointer moves forward. If `a[i] > a[j]`, then `a[i]` and every later left value are also larger than `a[j]`, because the left half is sorted. That is `mid - i` cross pairs found with one comparison. The right pointer moves forward. This is the **counting pass**, and it is the ordinary merge loop with one addition per right value taken.

#### Keep The Counts Correct

Each cross pair is counted exactly once, at the moment its right value is taken by the pointer `j`. The invariant is that the count so far equals the number of cross pairs whose right value lies before the pointer `j`. The merge then writes the halves into one sorted run, so the parent level sees a sorted half. The recursion has O(log n) levels, and each level does O(n) work in total. The whole count costs O(n log n).

<!-- stage: variables -->
### Quantities To Track While Merging

Track these items for one call on the range from `lo` up to but not including `hi`.

- **lo** is the first index of the range, included.
- **hi** is the end of the range, excluded, so the range holds `hi - lo` values.
- **mid** is the start of the right half, and the left half is `lo` up to `mid`.
- **i** is the left pointer, which moves from `lo` toward `mid`.
- **j** is the right pointer, which moves from `mid` toward `hi`.
- **count** is a `long` with the number of inversions found in the range.
- **buffer** is a shared `int[]` of the full length that holds the merged values before they are copied back.

The range is half open so that `hi - lo` is its length and an empty range needs no special case. The method passes only these bounds and one shared buffer. It never copies a subarray to pass the state into a recursive call. The unread left values at the moment of a count are the indexes `i` up to `mid`, and their number is `mid - i`.

<!-- stage: trace -->
### Follow Two Merges

Both traces show the counting pass on two sorted halves. The array cells are the left half followed by the right half. The pointer `i` walks the left half and the pointer `j` walks the right half.

#### Count With Distinct Values

The left half is `3, 6, 9` and the right half is `1, 7, 8`. At the start, `a[i] = 3` is larger than `a[j] = 1`, and all three left values are larger than 1. The count jumps by 3 with a single comparison. After that the left values 3 and 6 are not larger than 7, so `i` moves past them. The value 9 is larger than 7 and larger than 8, and each time only one left value is unread, so the count grows by 1 twice. The final count is 5.

```trace
{"cells":[3,6,9,1,7,8],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":3},"vars":{"count":0},"note":"The left half [3, 6, 9] and the right half [1, 7, 8] are both sorted. The count starts at 0."},{"at":{"i":0,"j":3},"vars":{"count":3},"note":"The left value 3 is greater than the right value 1, and so are all 3 unread left values. The count grows by 3 and becomes 3. The right pointer moves on."},{"at":{"i":0,"j":4},"vars":{"count":3},"note":"The left value 3 is at most the right value 7, so it forms no pair with any right value still unread. The left pointer moves on."},{"at":{"i":1,"j":4},"vars":{"count":3},"note":"The left value 6 is at most the right value 7, so it forms no pair with any right value still unread. The left pointer moves on."},{"at":{"i":2,"j":4},"vars":{"count":4},"note":"The left value 9 is greater than the right value 7, and so are all 1 unread left values. The count grows by 1 and becomes 4. The right pointer moves on."},{"at":{"i":2,"j":5},"vars":{"count":5},"note":"The left value 9 is greater than the right value 8, and so are all 1 unread left values. The count grows by 1 and becomes 5. The right pointer moves on."},{"at":{"i":2,"j":6},"vars":{"count":5},"note":"One half is used up, so no further pair can form. The answer for this merge is 5."}]}
```

#### Count With Equal Values

The left half is `2, 4, 4, 8` and the right half is `4, 4, 6`. The equal values 4 are the hard step. The test is `a[i] <= a[j]`, so an equal left value moves on without counting. The pointer `i` passes 2 and both left 4s, and none of them is a cross pair with the right 4s, because equal values are not inversions. Only 8 is larger than the right values 4, 4 and 6, and one unread left value remains each time. The final count is 3.

```trace
{"cells":[2,4,4,8,4,4,6],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":4},"vars":{"count":0},"note":"The left half [2, 4, 4, 8] and the right half [4, 4, 6] are both sorted. The count starts at 0."},{"at":{"i":0,"j":4},"vars":{"count":0},"note":"The left value 2 is at most the right value 4, so it forms no pair with any right value still unread. The left pointer moves on."},{"at":{"i":1,"j":4},"vars":{"count":0},"note":"The left value 4 is at most the right value 4, so it forms no pair with any right value still unread. The left pointer moves on."},{"at":{"i":2,"j":4},"vars":{"count":0},"note":"The left value 4 is at most the right value 4, so it forms no pair with any right value still unread. The left pointer moves on."},{"at":{"i":3,"j":4},"vars":{"count":1},"note":"The left value 8 is greater than the right value 4, and so are all 1 unread left values. The count grows by 1 and becomes 1. The right pointer moves on."},{"at":{"i":3,"j":5},"vars":{"count":2},"note":"The left value 8 is greater than the right value 4, and so are all 1 unread left values. The count grows by 1 and becomes 2. The right pointer moves on."},{"at":{"i":3,"j":6},"vars":{"count":3},"note":"The left value 8 is greater than the right value 6, and so are all 1 unread left values. The count grows by 1 and becomes 3. The right pointer moves on."},{"at":{"i":3,"j":7},"vars":{"count":3},"note":"One half is used up, so no further pair can form. The answer for this merge is 3."}]}
```

The first trace shows a count larger than 1 from one comparison, which is the saving over the double loop. The second trace shows that the sign of the comparison decides which ties count.

<!-- stage: code -->
### Implement Counting During The Merge

```java
final class MergeCount {
    static long countInversions(int[] a) {
        int[] work = a.clone();                       // the caller's array stays unchanged
        return sortAndCount(work, 0, work.length, new int[work.length]);
    }

    private static long sortAndCount(int[] a, int lo, int hi, int[] buffer) {
        if (hi - lo < 2) {
            return 0;                                 // zero or one value has no pair
        }
        int mid = lo + (hi - lo) / 2;                 // right half starts here
        long count = sortAndCount(a, lo, mid, buffer)
                   + sortAndCount(a, mid, hi, buffer); // pairs inside each half
        int i = lo, j = mid, k = lo;
        while (i < mid || j < hi) {
            if (j == hi || (i < mid && a[i] <= a[j])) {
                buffer[k++] = a[i++];                 // equal values stay on the left, so ties never count
            } else {
                count += mid - i;                     // all unread left values exceed a[j]
                buffer[k++] = a[j++];
            }
        }
        System.arraycopy(buffer, lo, a, lo, hi - lo); // the range is sorted for the parent
        return count;
    }
}
```

The recursion passes index bounds and one shared buffer, so no call copies a subarray. The only copy is the single `clone` at the start, which keeps the caller's array unchanged. When the left half is used up, the `else` branch adds `mid - i`, which is 0. The count is a `long`, because the total can reach about five billion.

<!-- stage: applicability -->
### When Merge Counting Applies

#### Recognize The Pattern

Use merge counting when the task counts pairs of positions `i < j` whose values satisfy an order relation, such as `a[i] > a[j]`, and the program only needs the total or one count per position. The relation must be monotone over sorted values: if a left value satisfies it for some right value, every larger left value does too. That property lets one pointer count a whole suffix of the sorted left half.

The invariant to check is that both halves are sorted before the cross pairs are counted, and that the count so far covers exactly the right values already passed. When a condition is more complex than a comparison, such as `a[i] > 2 * a[j]`, the pointer needs its own counting pass before the merge, because the merge order and the counting order differ.

#### Watch For The Nearest False Friend

Plain sorting is a false friend. Sorting the array gives the right order, but it destroys the original positions, and an inversion depends on those positions. Sorting first and counting afterward answers a different question. A second false friend is a stack or heap pass that works for the next larger value. It finds one neighbor for each position and does not count all larger values.

#### Avoid The Java Traps

Keep the count in a `long`, because an array of 100,000 reversed values holds almost five billion inversions. Choose `<=` or `<` on purpose, since the choice decides whether equal values count as inversions. Compute the midpoint as `lo + (hi - lo) / 2` so the sum of two large bounds cannot overflow. Pass index bounds and one shared buffer, and do not copy subarrays at each level.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Inversions (Author exercise)
<!-- id: mrg-count-inversions -->

**Prerequisites.** The counting pass and the merge from this lesson.

**Problem.** Given an integer array `a`, return the number of pairs of positions `(i, j)` with `i < j` and `a[i] > a[j]`.

**Constraints.** The limits are:
- **Length** `n` is an `int` with `0 <= n <= 10^5`.
- **Values** are `int` values over the full `int` range, and may repeat.
- **Return** is a `long`, and an empty array or a single value returns 0.
- **Mutation** of `a` is not allowed.

**Example 1.** Input `a = [2, 4, 1, 3, 5]`, output 3, from the pairs `(2, 1)`, `(4, 1)` and `(4, 3)`.

**Example 2.** Input a strictly decreasing array of 100,000 values, output 4,999,950,000, which does not fit in an `int`.

**Hint.** After both halves are sorted, how many left values are larger than the right value you take?

**Changed decision.** Baseline case: the merge gains one addition when it takes a right value.

#### [Vary] Count of Smaller Numbers After Self (LeetCode 315)
<!-- id: mrg-greater-before -->

**Prerequisites.** Count Inversions above.

**Problem.** Given an integer array `a`, return an array `result` of the same length. The entry `result[j]` is the number of positions `i < j` with `a[i] > a[j]`.

**Constraints.** The limits are:
- **Length** `n` is an `int` with `0 <= n <= 10^5`.
- **Values** are `int` values over the full `int` range, and may repeat.
- **Return** is an `int[]` of length `n`, indexed by original position.
- **Mutation** of `a` is not allowed.

**Example 1.** Input `a = [5, 2, 6, 1]`, output `[0, 1, 0, 3]`.

**Example 2.** Input `a = [4, 4, 4]`, output `[0, 0, 0]`, since equal values are not larger.

**Hint.** The merge reorders values, so which array can still tell you the original position of the value you take?

**Changed decision.** The output changes from one total to one count per original position, so the merge must carry indexes.

#### [Boundary] Equal Values (Author exercise)
<!-- id: mrg-equal-values -->

**Prerequisites.** Both exercises above.

**Problem.** Count the position pairs `(i, j)` of an integer array `a` that satisfy `i < j` and `a[i] >= a[j]`. Equal values count as pairs. Return that count.

**Constraints.** The limits are:
- **Length** `n` is an `int` with `0 <= n <= 10^5`.
- **Values** are `int` values over the full `int` range, and many may be equal.
- **Return** is a `long`.
- **Mutation** of `a` is not allowed.

**Example 1.** Input `a = [1, 2, 2, 1]`, output 4, from the pairs at positions `(0, 3)`, `(1, 2)`, `(1, 3)` and `(2, 3)`.

**Example 2.** Input `a = [7, 7, 7, 7]`, output 6, since every pair counts. The strict version of the count returns 0 here.

**Hint.** On a tie, which pointer must move so that the left value is counted against the equal right value?

**Changed decision.** The relation changes from strictly larger to larger or equal, so the tie rule in the merge flips.

#### [Recognize] Reverse Pairs (LeetCode 493)
<!-- id: mrg-large-drop -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `a` and a non-negative integer `d`, return the number of pairs of positions `(i, j)` with `i < j` and `a[i] - a[j] > d`.

**Constraints.** The limits are:
- **Length** `n` is an `int` with `0 <= n <= 10^5`.
- **Values** are `int` values over the full `int` range.
- **Threshold** `d` is a `long` with `0 <= d <= 4 * 10^9`.
- **Return** is a `long`.
- **Mutation** of `a` is not allowed.

**Example 1.** Input `a = [7, 1, 5, 2]` and `d = 3`, output 2, from the pairs `(7, 1)` and `(7, 2)`.

**Example 2.** Input `a = [2000000000, -2000000000]` and `d = 3999999999`, output 1. The difference is 4,000,000,000, which does not fit in an `int`.

**Hint.** The test no longer matches the merge order. Which loop can move one pointer forward over the left half before the merge starts?

**Changed decision.** The condition becomes a difference test, so the program counts in a separate pass with `long` arithmetic and then merges.
