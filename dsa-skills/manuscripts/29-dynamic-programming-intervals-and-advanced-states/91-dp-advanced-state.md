<!-- lesson-kind: combination -->
<!-- lesson-id: dp-advanced-state -->
## DP With Advanced State

<!-- stage: context -->
### A Scoring Rule That Defeats Greedy

A list editor deletes entries one at a time. Each deletion earns points equal to the product of the two entries that sit next to the deleted one at that moment. Entries beyond either end count as 1. For the list 4, 9, 3, 1, a developer picks the best-scoring deletion at every step. The program earns 21 points. Another order earns 28.

The greedy program is not buggy in any line. It fails because the best deletion now changes which entries are neighbours later. Deleting the 9 first earns 12 points, but it removes the large neighbour that the other three deletions could have used.

Formally, the input is an `int[] values`. One move deletes an entry and adds the product of its current left and right neighbours to the score. The task is to delete every entry and return the largest possible total.

This lesson asks how to choose the table index so that one stored answer stays valid no matter what happens elsewhere in the list.

<!-- stage: contributions -->
### What Four Earlier Skills Add

#### Interval Tables Add Independent Pieces

The interval lesson showed that `dp[left][right]` can own a contiguous range and read only shorter ranges that are already final. Choosing the last operation inside a range splits it into two parts that no longer affect each other. This lesson reuses that split.

#### Palindrome Tables Add Cheap Validity Checks

The palindrome lesson filled a yes or no table over all substrings and then ran a prefix loop that picks the last piece. The table answers validity in O(1) time. The prefix loop then needs only the lengths of the prefixes, not their contents.

#### Bit Masks Add Sets Of Used Items

The bitmask lesson stored which items are already taken in one integer. Bit `i` is 1 when item `i` is used. The integer is a complete description of a subset, so it works as a table index when the item count is small.

#### Range Tables Add Many Queries

Chapter 28 filled a table over pairs of positions so that every range answer was ready after one pass. That table has one entry per pair of positions, so a single fill answers any range question afterwards. The four skills supply three index choices. A range comes from the interval lesson, a prefix comes from the palindrome lesson and a set comes from the bitmask lesson. Chapter 28 supplies the idea of a range table with one entry per pair of positions.

<!-- stage: naive -->
### Deleting The Best Entry Each Time

The quick idea scores every remaining entry, deletes the highest-scoring one and repeats. The routine below keeps the list in an `ArrayList` with the outside value 1 at both ends.

```java
static int greedyDeletes(int[] values) {
    java.util.List<Integer> cur = new java.util.ArrayList<>();
    cur.add(1);
    for (int v : values) cur.add(v);
    cur.add(1);
    int total = 0;
    while (cur.size() > 2) {
        int bestAt = 1;
        for (int i = 1; i < cur.size() - 1; i++) {
            if (cur.get(i - 1) * cur.get(i + 1) > cur.get(bestAt - 1) * cur.get(bestAt + 1)) bestAt = i;
        }
        total += cur.get(bestAt - 1) * cur.get(bestAt + 1);
        cur.remove(bestAt);
    }
    return total;
}
```

The routine runs in O(n^2) time for n entries, because each of the n rounds scans the list, and uses O(n) memory. Each round makes a final choice using only the score available at that moment.

```predict
Run greedyDeletes on the values [4, 9, 3, 1]. What does it return, and which order of deletions earns more?

It returns 21. It deletes the 9 first for 12 points, then the 3 for 4, then the 1 for 4, then the 4 for 1. Deleting 4, 3 and 1 first, with the 9 still in place, earns 9 each, and the 9 then earns 1, for a total of 28.
```

<!-- stage: bottleneck -->
### A Deletion Changes Every Later Neighbour

Greedy fails because a deletion rewrites the neighbours of two other entries. Any table indexed by a prefix of the original list breaks for the same reason. After the entries 4 and 9 of the running example are deleted, the entry 3 has the outside value 1 as its left neighbour, and the prefix length 2 does not record that.

The correct method tries every order. A list of n entries has n! orders, and each order costs O(n) to score, so the total is O(n! * n). For n = 12 the count of orders is about 479 million, and for n = 20 it exceeds 10^18.

The orders share work. Whatever happens to the entries on one side of a chosen survivor does not change the neighbours on the other side. Many orders therefore repeat the same sub-order on a range of the list. The number of distinct ranges is only O(n^2), and a range with fixed ends needs one answer. The next section names the index that makes this sharing exact.

<!-- stage: insight -->
### Pick The Index That Fixes The Outside

A stored answer is reusable only when everything outside it is fixed. The index is the smallest description that fixes that outside. Each earlier skill supplies one kind of index.

<!-- names: interval state, prefix state, mask state -->

#### Interval State For Last Deletions

Let `a` be the list with the outside value 1 added at both ends. Define `dp[l][r]` as the best score from deleting every entry strictly between positions `l` and `r`, while positions `l` and `r` stay in place. This is an **interval state**: the two ends fix the neighbours for the whole sub-problem.

Consider the entry `k` deleted last inside the range. At that moment its neighbours are exactly `a[l]` and `a[r]`, so it earns `a[l] * a[r]`. Before it, the entries between `l` and `k` and the entries between `k` and `r` were deleted with `k` still standing. The two parts do not touch, so `dp[l][r]` is the best `k` of `a[l] * a[r] + dp[l][k] + dp[k][r]`.

#### Prefix State For Cuts

The **prefix state** stores `best[j]` for the first `j` items and tries every earlier cut `i`. It works when the last piece is judged on its own, as with a palindrome whose validity comes from a second table. It fails for deletions, because a prefix has no way to say what stands next to it.

#### Mask State For Sets

The **mask state** stores a subset of items in an integer. It works when the next decision depends on which items remain, and not on their order. In the equal-sum-groups exercise, the entries are split into groups that all have the same target sum, and the open group holds the used items beyond the completed groups. The fill of the open group is the sum of the used items modulo the target, which is a function of the mask alone. The mask therefore replaces a stored fill for every group.

#### The Rule Behind All Three

Choose the index from the question "what must stay fixed for the answer to remain true". The invariant is that every entry read is complete and describes exactly its own index.

<!-- stage: variables -->
### The Table For Deletion Intervals

The list `values` stays unchanged, and these working values describe the table for the running example.

- **a** is an `int[n + 2]` with `a[0] = 1`, `a[n + 1] = 1` and the original entries in between.
- **dp** is an `int[n + 2][n + 2]`; entry `dp[l][r]` is the best score for deleting every entry strictly between `l` and `r`.
- **l** and **r** are the positions of the two ends of the interval; both stay in place.
- **left** and **right** are the stored answers `dp[l][k]` and `dp[k][r]` for the last position `k`.
- **gap** is `r - l`, from 2 up to `n + 1`; a gap of 1 means no entry lies between, and the entry stays 0.
- **last** is the position `k` that the best choice deletes last inside `(l, r)`.
- **pair** is `a[l] * a[r]`, the score for deleting `last` at the very end.

Ranges of a smaller gap come first, so `dp[l][k]` and `dp[k][r]` are final when `(l, r)` reads them. Java fills the new array with zeros, so the gap-1 entries need no extra code.

<!-- stage: trace -->
### Two Runs Of The Interval Table

#### Four Entries With A Clear Winner

The first run uses the values `[4, 9, 3, 1]` from the opening. The array `a` is `[1, 4, 9, 3, 1, 1]`, so the positions run from 0 to 5. The cells below list the intervals with at least one entry inside, in the order the loops visit them: all gap-2 intervals, then gap 3, gap 4 and gap 5. The pointer `cell` marks the interval in progress, and `dp` is the value written.

The gap-2 intervals each hold one entry, so each earns the product of the two ends. The interval `(1,3)` keeps 4 and 3 and earns 12 for the entry 9. Larger intervals combine two smaller answers. The final interval `(0,5)` writes 28, which beats the 21 of the greedy routine.

```trace
{"cells":["(0,2)","(1,3)","(2,4)","(3,5)","(0,3)","(1,4)","(2,5)","(0,4)","(1,5)","(0,5)"],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"a":"[1, 4, 9, 3, 1, 1]"},"note":"Positions 0 and 5 hold the outside value 1. Every interval with no item strictly inside starts at 0."},{"at":{"cell":0},"vars":{"l":0,"r":2,"last":1,"pair":9,"left":0,"right":0,"dp":9},"note":"Interval (0,2) keeps the values 1 and 9 until the end. The best last removal is position 1, so the entry is 9 plus 0 plus 0, which is 9."},{"at":{"cell":1},"vars":{"l":1,"r":3,"last":2,"pair":12,"left":0,"right":0,"dp":12},"note":"Interval (1,3) keeps the values 4 and 3 until the end. The best last removal is position 2, so the entry is 12 plus 0 plus 0, which is 12."},{"at":{"cell":2},"vars":{"l":2,"r":4,"last":3,"pair":9,"left":0,"right":0,"dp":9},"note":"Interval (2,4) keeps the values 9 and 1 until the end. The best last removal is position 3, so the entry is 9 plus 0 plus 0, which is 9."},{"at":{"cell":3},"vars":{"l":3,"r":5,"last":4,"pair":3,"left":0,"right":0,"dp":3},"note":"Interval (3,5) keeps the values 3 and 1 until the end. The best last removal is position 4, so the entry is 3 plus 0 plus 0, which is 3."},{"at":{"cell":4},"vars":{"l":0,"r":3,"last":1,"pair":3,"left":0,"right":12,"dp":15},"note":"Interval (0,3) keeps the values 1 and 3 until the end. The best last removal is position 1, so the entry is 3 plus 0 plus 12, which is 15."},{"at":{"cell":5},"vars":{"l":1,"r":4,"last":3,"pair":4,"left":12,"right":0,"dp":16},"note":"Interval (1,4) keeps the values 4 and 1 until the end. The best last removal is position 3, so the entry is 4 plus 12 plus 0, which is 16."},{"at":{"cell":6},"vars":{"l":2,"r":5,"last":4,"pair":9,"left":9,"right":0,"dp":18},"note":"Interval (2,5) keeps the values 9 and 1 until the end. The best last removal is position 4, so the entry is 9 plus 9 plus 0, which is 18."},{"at":{"cell":7},"vars":{"l":0,"r":4,"last":2,"pair":1,"left":9,"right":9,"dp":19},"note":"Interval (0,4) keeps the values 1 and 1 until the end. The best last removal is position 2, so the entry is 1 plus 9 plus 9, which is 19."},{"at":{"cell":8},"vars":{"l":1,"r":5,"last":2,"pair":4,"left":0,"right":18,"dp":22},"note":"Interval (1,5) keeps the values 4 and 1 until the end. The best last removal is position 2, so the entry is 4 plus 0 plus 18, which is 22."},{"at":{"cell":9},"vars":{"l":0,"r":5,"last":2,"pair":1,"left":9,"right":18,"dp":28},"note":"Interval (0,5) keeps the values 1 and 1 until the end. The best last removal is position 2, so the entry is 1 plus 9 plus 18, which is 28."}]}
```

#### Three Entries With A Dominant Middle

The second run uses `[6, 2, 5]`. The best total is 37. The interval `(1,3)` keeps 6 and 5 for the entry 2 and earns 30, which becomes the heavy part of the answer. The longer intervals add the small scores of the end entries around it, and the final interval writes 37.

```trace
{"cells":["(0,2)","(1,3)","(2,4)","(0,3)","(1,4)","(0,4)"],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"a":"[1, 6, 2, 5, 1]"},"note":"Positions 0 and 4 hold the outside value 1. Every interval with no item strictly inside starts at 0."},{"at":{"cell":0},"vars":{"l":0,"r":2,"last":1,"pair":2,"left":0,"right":0,"dp":2},"note":"Interval (0,2) keeps the values 1 and 2 until the end. The best last removal is position 1, so the entry is 2 plus 0 plus 0, which is 2."},{"at":{"cell":1},"vars":{"l":1,"r":3,"last":2,"pair":30,"left":0,"right":0,"dp":30},"note":"Interval (1,3) keeps the values 6 and 5 until the end. The best last removal is position 2, so the entry is 30 plus 0 plus 0, which is 30."},{"at":{"cell":2},"vars":{"l":2,"r":4,"last":3,"pair":2,"left":0,"right":0,"dp":2},"note":"Interval (2,4) keeps the values 2 and 1 until the end. The best last removal is position 3, so the entry is 2 plus 0 plus 0, which is 2."},{"at":{"cell":3},"vars":{"l":0,"r":3,"last":1,"pair":5,"left":0,"right":30,"dp":35},"note":"Interval (0,3) keeps the values 1 and 5 until the end. The best last removal is position 1, so the entry is 5 plus 0 plus 30, which is 35."},{"at":{"cell":4},"vars":{"l":1,"r":4,"last":3,"pair":6,"left":30,"right":0,"dp":36},"note":"Interval (1,4) keeps the values 6 and 1 until the end. The best last removal is position 3, so the entry is 6 plus 30 plus 0, which is 36."},{"at":{"cell":5},"vars":{"l":0,"r":4,"last":1,"pair":1,"left":0,"right":36,"dp":37},"note":"Interval (0,4) keeps the values 1 and 1 until the end. The best last removal is position 1, so the entry is 1 plus 0 plus 36, which is 37."}]}
```

<!-- stage: code -->
### Filling Intervals By Gap Size

The method returns the largest score for deleting every entry. It copies the input into an array with the outside value 1 added at both ends and fills intervals in order of increasing gap.

```java
static int bestDeletionScore(int[] values) {
    int n = values.length;
    int[] a = new int[n + 2];
    a[0] = 1;
    a[n + 1] = 1;
    for (int i = 0; i < n; i++) a[i + 1] = values[i];
    int[][] dp = new int[n + 2][n + 2];
    for (int gap = 2; gap <= n + 1; gap++) {
        for (int l = 0; l + gap <= n + 1; l++) {
            int r = l + gap;
            for (int k = l + 1; k < r; k++) {
                int total = a[l] * a[r] + dp[l][k] + dp[k][r];
                if (total > dp[l][r]) dp[l][r] = total;
            }
        }
    }
    return dp[0][n + 1];
}
```

Time grows as O(n^3), because O(n^2) intervals each try up to n choices. Memory is O(n^2) for the table. An empty array gives `n = 0`, the gap loop starts at 2 and never runs, and the method returns 0. The product of two ends can reach large values, so a very large input needs `long` instead of `int`.

<!-- stage: applicability -->
### Matching The Index To The Problem

#### Reading The Cue

Ask what must stay fixed when two choices lead to the same remaining work. If the last operation inside a contiguous range splits it into independent parts, use a range index. If the last piece of a prefix is judged alone, use a prefix index with a validity table. If the future depends on a small set of used items and not on their order, use a mask. If many range questions are asked on one text, fill the whole range table once.

#### Checking The Invariant

The invariant says that each entry is final before any entry reads it and that it describes exactly its own index. Test the empty input, a single item, two equal items and a case where the greedy choice and the best choice differ. Compare against a brute-force search on inputs small enough to enumerate. A table that returns a value above the brute force has read an entry that was not yet final.

#### Spotting The False Friend

The false friend is a prefix table used for a problem where choices change the neighbours of other items. It passes tests where the best order happens to run left to right. The second false friend is the greedy rule above, which passes whenever the best immediate choice is also globally best. A third false friend is a table that records the fill of every group separately: it stores a group order that the problem does not care about.

#### Knowing When Not To Use It

Do not use a mask when the item count exceeds about 20, because 2^n entries no longer fit in memory. Do not use an O(n^3) interval table when n is in the thousands. Both cases call for a different formulation.

<!-- stage: exercises -->
### Exercises

#### [Build] Palindromic Subsequence In Query Ranges (LeetCode 516)
<!-- id: dp29-range-palindrome-queries -->

**Prerequisites.** The interval table from this lesson and the range table from chapter 28, which stores one answer for every pair of positions. This exercise uses only the range index.

**Problem.** This is a variant of LeetCode 516 that adds range queries. A string `s` and a list of queries are given. Each query is a pair `(l, r)` of indexes with `l <= r`. For every query, return the length of the longest palindromic subsequence of the substring `s[l..r]`. A palindromic subsequence keeps characters in order, may skip characters and reads the same in both directions. Return the answers in query order.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 300`.
- **Queries** number at most 2000, and `0 <= l <= r < s.length()`.
- **Characters** are lowercase English letters.
- **Result** is an `int[]` with one entry per query.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `s = "xabcbayz"`, `queries = [[0,7],[1,5],[2,2],[6,7]]`, output `[5, 5, 1, 1]`.

**Example 2.** Input `s = "cbbdcb"`, `queries = [[0,5],[1,4]]`, output `[4, 2]`.

**Hint.** What does a range with equal end characters read, and what does a range with different end characters read? What value does an empty inner range have?

**Changed decision.** One table answers every query after it is filled once. The table keeps all ranges, because a query may ask for any of them.

#### [Vary] Palindrome Cuts With Minimum Piece Length (LeetCode 132)
<!-- id: dp29-cuts-min-piece-length -->

**Prerequisites.** The exercise above and the palindrome table lesson. This exercise uses the prefix index with a palindrome table.

**Problem.** This is a variant of LeetCode 132 that adds a minimum piece length and an impossible result. A string `s` and an integer `minLen` are given. A cut splits `s` between two neighbouring characters. Choose cuts so that every piece is a palindrome with at least `minLen` characters. Return the smallest number of cuts, or -1 if no choice of cuts works.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 1000`.
- **Minimum length** satisfies `1 <= minLen <= s.length()`.
- **Characters** are lowercase English letters.
- **Result** is an `int`, with -1 when impossible.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `s = "aaacbcaa"`, `minLen = 2`, output `2`. With `minLen = 1` the same string needs only 1 cut.

**Example 2.** Input `s = "abacabb"`, `minLen = 2`, output `-1`.

**Hint.** Which earlier prefixes may end just before the last piece, and what must be true about the last piece itself? What marks a prefix that has no valid split?

**Changed decision.** A prefix may be unreachable. The prefix table needs a marker for that state, and the length floor removes some cuts that a palindrome table alone would accept.

#### [Boundary] Burst Balloons With Given Outer Values (LeetCode 312)
<!-- id: dp29-burst-outer-values -->

**Prerequisites.** The two exercises above and the interval table from this lesson. This exercise uses only the range index.

**Problem.** This is a variant of LeetCode 312 that replaces the fixed outer 1s with given edge values. An array `nums` and two integers `leftEdge` and `rightEdge` are given. Bursting the balloon at index `i` earns `left * nums[i] * right`, where `left` and `right` are the nearest balloons that have not burst yet. If no balloon remains on a side, that side uses `leftEdge` or `rightEdge`. Burst every balloon in some order. Return the largest total.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 300`, and the array may be empty.
- **Values** satisfy `0 <= nums[i] <= 100`.
- **Edges** satisfy `0 <= leftEdge, rightEdge <= 100`.
- **Result** is an `int`, and 0 is returned for an empty array.
- **Mutation** is not allowed; the method copies the array before it adds the edges.

**Example 1.** Input `nums = [2,4,3]`, `leftEdge = 5`, `rightEdge = 2`, output `130`.

**Example 2.** Input `nums = [2,4,3]`, `leftEdge = 0`, `rightEdge = 0`, output `24`.

**Hint.** If a balloon is the last one burst inside an interval, which two values are its neighbours, and where do the edges enter the table?

**Changed decision.** The two outside values are inputs, not fixed to 1. The self term changes the recurrence. The last balloon `k` in `(l, r)` earns `a[l] * nums[k] * a[r]`, which includes the value of `k` itself, whereas the deletion game earns only `a[l] * a[r]`. A value of 0 at an edge makes some choices worth nothing, so the table cannot rely on ones as defaults.

#### [Recognize] Largest Number Of Equal Sum Groups (LeetCode 698)
<!-- id: dp29-equal-sum-groups -->

**Prerequisites.** All three exercises above and the bitmask lesson. This exercise uses the mask index.

**Problem.** This is a variant of LeetCode 698 that asks for the largest group count and not a yes or no for a given count. An array `nums` of positive integers is given. Split all entries into `k` non-empty groups so that every group has the same sum. Every entry belongs to exactly one group. Return the largest `k` for which such a split exists.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 16`.
- **Values** satisfy `1 <= nums[i] <= 10000`.
- **Result** is an `int`, and `k = 1` always works.
- **Mutation** is not allowed.

**Example 1.** Input `nums = [1,2,3,4,5,6]`, output `3`.

**Example 2.** Input `nums = [7,7,2,2,3,3]`, output `2`.

**Hint.** For a fixed group count, what sum must each group have? Does the fill of the group in progress depend on the order the used items were added, or only on which items are used?

**Changed decision.** The method tries each possible `k` and runs a mask search for each. The fill of the open group follows from the mask alone, so the search does not track which group is which.
