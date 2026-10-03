<!-- lesson-kind: standard -->
<!-- lesson-id: sort-then-scan -->
## Sort Then Scan

<!-- stage: context -->
### A Quiz Night Podium

At the end of a quiz night the host holds a stack of score cards, one per team, and several teams finished with identical scores. She wants to announce the third place, and she has decided that teams with equal scores share a place. If the scores are 95, 95, 80, 70, 70, then 95 is first, 80 is second and 70 is third. When fewer than three different scores exist, she will simply announce the best score instead of leaving the audience waiting.

Her first approach is to hunt through the stack three times. The first time she finds the biggest score. The second time she finds the biggest score smaller than that one. The third time she finds the biggest score smaller than the second. The stack is thick, and each hunt looks at every card, including cards she already knows are out of the running.

<!-- stage: naive -->
### Hunt Below The Previous Pick

In Java, each pass keeps the largest value that is strictly smaller than the previous pick.

```java
static int thirdPlaceByHunting(int[] scores) {
    long limit = Long.MAX_VALUE;
    int best = 0;
    boolean found = false;
    for (int place = 1; place <= 3; place++) {
        found = false;
        for (int s : scores) {
            if (s < limit && (!found || s > best)) { best = s; found = true; }
        }
        if (!found) break;
        limit = best;
        if (place == 3) return best;
    }
    int top = scores[0];
    for (int s : scores) top = Math.max(top, s);
    return top;
}
```

It follows the host's rule exactly, including the case of fewer than three distinct scores, where it announces the best score.

<!-- stage: bottleneck -->
### One Pass Per Place Is Too Many

For the third place there are three passes, which is O(n), and the method looks fine. The trouble is that the pass count equals the place being asked for. If the host wants the k-th place, the cost is O(k n), and for the median place it becomes O(n^2). The method also contains special cases: the limit starts at a huge sentinel, a flag records whether anything was found, and a separate fallback loop finds the maximum. Each is a place for a bug.

Every pass repeats comparisons that earlier passes already made, because nothing from the first pass is remembered except a single number. If the cards were laid out in order of score, then equal scores would be neighbors, the number of different scores so far would be a count of changes, and all the places would be read off in a single walk.

<!-- stage: insight -->
### Sorting Exposes A Simple Neighbor Test

Sorting does not answer the question, it simplifies it. After sorting, two scores are the same place exactly when they are neighbors with equal values, so the **adjacent relation** between a card and the one before it is enough to say whether a new place begins. The scan that follows carries one **candidate**, the best answer found so far under the new order, together with a count of how many places have been passed.

For the podium, sort the scores in descending order, walk from the front, and count a new place each time the value differs from the previous one. When the count reaches the requested place, the current value is the answer. If the walk finishes first, there were fewer places than asked for, and the problem's stated **fallback** applies: here, the largest value. Stating the fallback before writing the loop is the cleanest way to avoid indexing past the number of distinct values.

<!-- names: adjacent relation, candidate, fallback -->

The same two steps solve problems that look different. To report each team's medal while keeping the original card order, sort the positions and not the scores, so that the sorted walk can write its answer back at the original index. To find the one missing number among 0 through n, sort the values and compare each one with its own position: the first position whose value differs from the position number is the answer, and if every position matches, the missing number is n.

Sorting makes these scans easy, but it is not always the cheapest way. Counting and set-based methods can do the same jobs without sorting, at lower cost for some of them, and this lesson chooses the sorted version because it shows how an order turns a global question into a neighbor question.

<!-- stage: variables -->
### Index, Place Count And Answer

The walk keeps an index `i` over the sorted values. The place count begins at one, counting the first value as the start of the first place, and increases at every position whose value differs from its predecessor. The candidate is the value at the position being read, and it becomes the answer only when the count equals the requested place. For the missing number the only state is the index, since the expected value at position `i` is `i` itself. The original positions, when needed, are held in a separate array of indices that is sorted instead of the values.

<!-- stage: trace -->
### Counting Places And Spotting A Gap

The first trace finds the third place among 2, 2, 3, 1, 5, 5, using the values sorted from largest to smallest: 5, 5, 3, 2, 2, 1. The place count goes up each time the value changes. The step to study is the fourth, where the value falls from 3 to 2 and the count reaches three, which ends the walk with the answer 2.

```trace
{"cells":[5,5,3,2,2,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":5,"place":1},"note":"5 is the first value, so it begins the first place."},{"at":{"i":1},"vars":{"value":5,"place":1},"note":"5 equals the previous value, so it shares place 1."},{"at":{"i":2},"vars":{"value":3,"place":2},"note":"The value falls from 5 to 3, so place 2 begins."},{"at":{"i":3},"vars":{"value":2,"place":3},"note":"The value falls from 3 to 2, so place 3 begins. Place three has been reached, so the answer is 2."}]}
```

The second trace finds the missing number in 3, 0, 1, 4, whose sorted form is 0, 1, 3, 4. Each position is compared with the value it holds. The first two match. At the third position the value is 3 instead of 2, so the expected number 2 is the one that is missing, and the scan can stop without reading the last position.

```trace
{"cells":[0,1,3,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"expected":0,"value":0},"note":"Position 0 holds 0, which equals its index, so nothing is missing so far."},{"at":{"i":1},"vars":{"expected":1,"value":1},"note":"Position 1 holds 1, which equals its index, so nothing is missing so far."},{"at":{"i":2},"vars":{"expected":2,"value":3,"answer":2},"note":"Position 2 holds 3 but should hold 2. The number 2 is missing, so the scan returns 2."}]}
```

<!-- stage: code -->
### Place Counting, Indexed Ranks And Gaps

```java
static int kthDistinctOrBest(int[] nums, int k) {
    int[] a = nums.clone();
    Arrays.sort(a);
    int place = 1;
    for (int i = a.length - 1; i >= 0; i--) {
        if (i < a.length - 1 && a[i] != a[i + 1]) place++;
        if (place == k) return a[i];
    }
    return a[a.length - 1];                 // fewer than k distinct values
}

static String[] relativeRanks(int[] score) {
    Integer[] by = new Integer[score.length];
    for (int i = 0; i < by.length; i++) by[i] = i;
    Arrays.sort(by, (i, j) -> Integer.compare(score[j], score[i]));
    String[] medal = {"Gold Medal", "Silver Medal", "Bronze Medal"};
    String[] out = new String[score.length];
    for (int rank = 0; rank < by.length; rank++) {
        out[by[rank]] = rank < 3 ? medal[rank] : String.valueOf(rank + 1);
    }
    return out;
}

static int missingFromZeroToN(int[] nums) {
    int[] a = nums.clone();
    Arrays.sort(a);
    for (int i = 0; i < a.length; i++) {
        if (a[i] != i) return i;
    }
    return a.length;
}
```

All three methods cost O(n log n) for the sort and O(n) for the scan. The rank method boxes the positions, which costs O(n) extra space, and its comparator uses `Integer.compare` on scores so that extreme values cannot overflow. In `kthDistinctOrBest` the loop returns inside, so the final return is reached only when there are fewer than k distinct values.

<!-- stage: applicability -->
### When Sorted Order Simplifies The Question

Use sort-then-scan when a question about the whole collection becomes a question about neighbors once the values are in order: distinct places, gaps, closest pairs, runs, ranks. The invariant is the meaning of the candidate: after reading position `i`, the candidate is the best answer among positions up to `i` under the new order. Decide the fallback in advance, for the cases where the scan finishes without the sought pattern.

A false friend is binary search. Sorted input alone does not make binary search legal, since it needs a monotone yes-or-no question over the positions: all the answers on one side of some boundary must be no, and all on the other must be yes. Another false friend is a sort used on data whose original positions matter, with the positions then lost. Carry indices in that case.

In Java, sort positions through a boxed `Integer[]` when the comparator needs the original index, and use `Integer.compare` for comparing values. For the k-th distinct value never index at `length - k` directly, because duplicates make that position the wrong one. Count the changes of value while scanning, and fall back as the problem says.

<!-- stage: exercises -->
### Exercises

#### [Build] Third Maximum Number (LeetCode 414)
<!-- id: so-third-maximum -->

**Prerequisites.** The sort-and-deduplicate lesson, and the idea of a run of equal values.

**Problem.** Return the third largest distinct value in the array. If fewer than three distinct values exist, return the largest value. Sort a copy and count how many distinct values you have passed while walking from the large end.

**Constraints.** 1 <= nums.length <= 10000 and any `int` values, including `Integer.MIN_VALUE`. Do not use a sentinel value that could itself appear in the input.

**Example 1.** Input `nums = [2, 2, 3, 1, 5, 5]`, output 2.

**Example 2.** Input `nums = [8, 8, 4]`, output 8, since only two distinct values exist.

**Hint.** When does a new place begin while walking the sorted array? What should the method return if the walk ends before the third place?

**Changed decision.** First rung: the duplicate rule is part of the scan, so places are counted by changes of value and not by positions.

#### [Vary] Relative Ranks (LeetCode 506)
<!-- id: so-relative-ranks -->

**Prerequisites.** The third-maximum exercise above.

**Problem.** Each athlete has a distinct score. Return an array in the original athlete order in which the best score holds `"Gold Medal"`, the second `"Silver Medal"`, the third `"Bronze Medal"`, and every other athlete holds their place number as a string.

**Constraints.** 1 <= score.length <= 10000 and 0 <= score[i] <= 1000000, all scores distinct. Sort positions, not the scores themselves.

**Example 1.** Input `score = [40, 90, 70, 55]`, output `["4", "Gold Medal", "Silver Medal", "Bronze Medal"]`.

**Example 2.** Input `score = [10]`, output `["Gold Medal"]`.

**Hint.** What must you remember about each sorted score to put its answer back in the right place? Which array should the comparator read?

**Changed decision.** The sort is over indices, so the original positions survive and the answers are written back by index.

#### [Boundary] Fewer Than k Distinct Values (Author exercise)
<!-- id: so-fewer-than-k-distinct -->

**Prerequisites.** The two exercises above.

**Problem.** Return the k-th largest distinct value, or the largest value when fewer than k distinct values exist. Test k larger than the number of distinct values, k equal to one, and an array whose entries are all equal.

**Constraints.** 1 <= nums.length <= 1000, 1 <= k <= 1000, and any `int` values. The method must never read outside the array.

**Example 1.** Input `nums = [4, 4, 4], k = 2`, output 4, the fallback.

**Example 2.** Input `nums = [7, 1, 9, 9], k = 3`, output 1.

**Hint.** What goes wrong if you index the sorted array at `length - k`? How can the scan tell that it ran out of places?

**Changed decision.** The requested place may not exist, so the fallback is a defined outcome and not an index error.

#### [Recognize] Missing Number (LeetCode 268)
<!-- id: so-missing-number-sorted -->

**Prerequisites.** All three exercises above.

**Problem.** An array holds n distinct numbers taken from 0 through n, so exactly one number in that range is absent. Sort a copy, return the first index whose value differs from the index, and return n if every earlier position matches.

**Constraints.** 1 <= nums.length <= 10000 and the values are distinct and lie in the range 0 to n. The argument must not be modified.

**Example 1.** Input `nums = [3, 0, 1, 4]`, output 2.

**Example 2.** Input `nums = [0, 1, 2]`, output 3.

**Hint.** What value should sit at position `i` if nothing is missing before it? What is the answer when no position disagrees?

**Changed decision.** The sorted order lets each value be compared with its own index, so the first disagreement is the gap.
