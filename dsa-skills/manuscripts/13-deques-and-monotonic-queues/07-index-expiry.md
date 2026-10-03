<!-- lesson-kind: standard -->
<!-- lesson-id: index-expiry -->
## Index Expiry

<!-- stage: context -->
### Bonuses That Lapse With Age

A delivery company pays its couriers a streak bonus. When a courier finishes a route, the bonus offered for that route is the best rating the courier earned on any of the previous few routes, and a rating older than that cutoff no longer counts, however good it was. A superb rating from long ago is worth nothing today, and a modest rating from yesterday is worth a lot.

The payroll clerk keeps a notebook of the recent ratings. For each new route he scans the notebook for the best rating that has not yet lapsed, and he crosses out nothing, because he worries about a rating that is both old and good. He has also noticed that two routes can have the same rating and yet one of them lapses a day before the other, so the notebook must remember which route a rating came from, not only how large it was.

<!-- stage: naive -->
### Rescan The Recent Routes Each Time

The direct method looks back over the allowed number of earlier positions for every position.

```java
static int[] bonusByLookback(int[] rating, int k) {
    int[] bonus = new int[rating.length];
    for (int i = 0; i < rating.length; i++) {
        int best = -1;
        for (int j = Math.max(0, i - k); j < i; j++) best = Math.max(best, rating[j]);
        bonus[i] = best;
    }
    return bonus;
}
```

It is correct, and for the ratings `[4, 9, 1]` with a lookback of 2 it returns `[-1, 4, 9]`, where `-1` means that no earlier route exists.

<!-- stage: bottleneck -->
### Every Lookback Repeats Old Work

Position `i` and position `i + 1` look back over almost the same stretch, so the scan compares the same ratings again and again. With `n` routes and a lookback of `k` the cost is O(n * k), which approaches O(n^2) once the lookback is a large share of the record. A fleet history of a million routes with a lookback of a hundred thousand would need on the order of a hundred billion comparisons.

What changes between neighbours is small. One rating gains eligibility at the near end, and one rating may lose it at the far end. A rating that is both older and no better than a rating that came after it can never be the best again, because the newer one will outlast it. Only the survivors of that comparison need to be kept, and they must be removed from the far end the moment their age passes the cutoff. A heap would also work, but it leaves lapsed entries inside until they surface, and costs O(n log n) overall.

<!-- stage: insight -->
### Age Decides Who Stays

The structure is a deque of positions, with the oldest at the front and the newest at the back, whose ratings fall from front to back. Three ideas make it correct. The **legal left bound** is the smallest position that may still be used for the current question, and for a lookback of `k` at position `i` it is `i - k`, while for a supplied boundary it is simply the boundary for that question. The **age test** compares the front position with that bound and removes the front while it lies to the left of the bound. The **stored identity** is the position itself, kept instead of the rating, so the age test has something to compare and so two equal ratings that arrived on different days expire on different days.

<!-- names: legal left bound, age test, stored identity -->

The order of work at each position is fixed. Apply the age test first, then read the front as the answer for this position, and only then discard weaker positions from the back and append the current one, because the current position is not eligible for its own question. Since the legal left bound never moves backward, an expired position can never become legal again, and the age test needs only to look at the front.

The cost is O(n) overall, since every position enters once and leaves once, and the deque never holds more positions than the lookback allows.

<!-- stage: variables -->
### Position, Bound And Front

The variable `i` is the current position, the one whose answer is being produced. The bound `low` is the legal left bound for it, either `i - k` or an entry of a boundary array that never decreases. The deque holds positions strictly less than `i`, ordered by age, and `rating[deque.peekFirst()]` is the best eligible rating. When the deque is empty after the age test, there is no eligible position and the answer is a sentinel chosen by the contract. A lookback of `k` means `k` positions are eligible once `i >= k`, so the bound `i - k` itself is legal and anything below it is expired.

<!-- stage: trace -->
### A Lapsed Rating Leaves The Board

Take the ratings `5, 3, 6, 2, 4, 1, 7` with a lookback of 3. At position 0 nothing is eligible, so the answer is none, and position 0 is appended. At position 1 the front is position 0 holding 5, so the bonus is 5, and the 3 is appended behind it. At position 2 the bonus is still 5, and the 6 then removes the 3 and the 5 from the back, leaving only position 2. At position 3 the bonus is 6, and the 2 joins behind it. At position 4 the bound is 1, nothing at the front is below it, the bonus is 6, and the 4 removes the 2. At position 5 the bonus is still 6 and the 1 joins behind the 4. At position 6 the bound is 3, so the age test finds position 2 expired at the front and removes it. The next survivor is position 4 holding 4, so the bonus is 4, and the 7 then clears the whole deque.

A second run applies the same moves to a best-path score, where each position's score is its own value plus the best score among the previous three. The deque holds positions ordered by their computed scores, and the answer read feeds the score that is appended next.

```trace
{"cells":[5,3,6,2,4,1,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[0]","answers":"[-1]"},"note":"Position 0 holds 5. No earlier position is eligible, so the answer is none. Then position 0 is appended."},{"at":{"i":1},"vars":{"deque":"[0,1]","answers":"[-1,5]"},"note":"Position 1 holds 3. The front gives the answer 5. Then position 1 is appended."},{"at":{"i":2},"vars":{"deque":"[2]","answers":"[-1,5,5]"},"note":"Position 2 holds 6. The front gives the answer 5. Then the value 6 removes position 1, 0 from the back. Then position 2 is appended."},{"at":{"i":3},"vars":{"deque":"[2,3]","answers":"[-1,5,5,6]"},"note":"Position 3 holds 2. The front gives the answer 6. Then position 3 is appended."},{"at":{"i":4},"vars":{"deque":"[2,4]","answers":"[-1,5,5,6,6]"},"note":"Position 4 holds 4. The front gives the answer 6. Then the value 4 removes position 3 from the back. Then position 4 is appended."},{"at":{"i":5},"vars":{"deque":"[2,4,5]","answers":"[-1,5,5,6,6,6]"},"note":"Position 5 holds 1. The front gives the answer 6. Then position 5 is appended."},{"at":{"i":6},"vars":{"deque":"[6]","answers":"[-1,5,5,6,6,6,4]"},"note":"Position 6 holds 7. The age test removes position 2 from the front. The front gives the answer 4. Then the value 7 removes position 5, 4 from the back. Then position 6 is appended."}]}
```

```trace
{"cells":[3,-2,4,-1,2,-5,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"scores":"[3]","deque":"[0]"},"note":"The start is worth 3 and position 0 is stored."},{"at":{"i":1},"vars":{"scores":"[3,1]","deque":"[0,1]"},"note":"Position 1 holds -2. The front is position 0 with score 3, so the score here is 1."},{"at":{"i":2},"vars":{"scores":"[3,1,7]","deque":"[2]"},"note":"Position 2 holds 4. The front is position 0 with score 3, so the score here is 7. The new score removes position 1, 0 from the back."},{"at":{"i":3},"vars":{"scores":"[3,1,7,6]","deque":"[2,3]"},"note":"Position 3 holds -1. The front is position 2 with score 7, so the score here is 6."},{"at":{"i":4},"vars":{"scores":"[3,1,7,6,9]","deque":"[4]"},"note":"Position 4 holds 2. The front is position 2 with score 7, so the score here is 9. The new score removes position 3, 2 from the back."},{"at":{"i":5},"vars":{"scores":"[3,1,7,6,9,4]","deque":"[4,5]"},"note":"Position 5 holds -5. The front is position 4 with score 9, so the score here is 4."},{"at":{"i":6},"vars":{"scores":"[3,1,7,6,9,4,15]","deque":"[6]"},"note":"Position 6 holds 6. The front is position 4 with score 9, so the score here is 15. The new score removes position 5, 4 from the back."}]}
```

<!-- stage: code -->
### Lookback Max With A Bound Array

```java
static int[] bonusOfLastK(int[] rating, int k) {
    int[] bonus = new int[rating.length];
    java.util.ArrayDeque<Integer> deque = new java.util.ArrayDeque<>();
    for (int i = 0; i < rating.length; i++) {
        while (!deque.isEmpty() && deque.peekFirst() < i - k) deque.removeFirst();
        bonus[i] = deque.isEmpty() ? -1 : rating[deque.peekFirst()];
        while (!deque.isEmpty() && rating[deque.peekLast()] < rating[i]) deque.removeLast();
        deque.addLast(i);
    }
    return bonus;
}

static int[] boundedMax(int[] a, int[] low) {
    int[] out = new int[a.length];
    java.util.ArrayDeque<Integer> deque = new java.util.ArrayDeque<>();
    for (int i = 0; i < a.length; i++) {
        while (!deque.isEmpty() && a[deque.peekLast()] < a[i]) deque.removeLast();
        deque.addLast(i);
        while (deque.peekFirst() < low[i]) deque.removeFirst();
        out[i] = a[deque.peekFirst()];
    }
    return out;
}

static long bestJumpScore(int[] nums, int k) {
    long[] score = new long[nums.length];
    java.util.ArrayDeque<Integer> deque = new java.util.ArrayDeque<>();
    score[0] = nums[0];
    deque.addLast(0);
    for (int i = 1; i < nums.length; i++) {
        while (deque.peekFirst() < i - k) deque.removeFirst();
        score[i] = nums[i] + score[deque.peekFirst()];
        while (!deque.isEmpty() && score[deque.peekLast()] <= score[i]) deque.removeLast();
        deque.addLast(i);
    }
    return score[nums.length - 1];
}
```

The first method reads before it appends because a position cannot answer for itself, while the second appends first because its window includes the current position. Both are O(n), since every position is added and removed at most once.

<!-- stage: applicability -->
### When Age Limits The Candidates

Reach for index expiry when a query is a best-of over a stretch whose left edge only moves rightward, and when every candidate carries a position that can be compared with that edge. Typical forms are a lookback of fixed length, a boundary array supplied with the problem, and a recurrence in which each state depends on the best of the last few states. The invariant is that the deque holds only positions at or above the legal left bound, in age order, with ratings that fall toward the back, so the front is both the oldest survivor and the best one.

The false friend is a deque that stores ratings. It looks fine until two equal ratings come from different days, and then removing the value removes the wrong day's entry, or leaves a lapsed entry behind. A second false friend is checking the age test after reading the front, which reads one lapsed value. A third is a boundary that can move left, since a discarded position cannot be brought back.

Do not use it when the left bound can move backward, when every candidate must be summed rather than compared, or when the question is about the k-th best rather than the best. In Java, `Deque<Integer>` holds boxed positions, so comparing two of them with `==` is unsafe once they exceed 127. The code above compares with `<` and an `int` bound, which unboxes.

<!-- stage: exercises -->
### Exercises

#### [Build] Best Of Last K Scores (Author exercise)
<!-- id: dq-best-of-last-k -->

**Prerequisites.** The sliding maximum and sliding minimum lessons of this chapter.

**Problem.** Given a non-negative integer array `score` and a lookback `k`, return an array where entry `i` is the largest score at positions `i-k` through `i-1`, ignoring positions below 0. If there is no such position, the entry is -1.

**Constraints.** 1 <= k <= score.length <= 10^5 and 0 <= score[i] <= 10^9. Linear time.

**Example 1.** Input `score = [5, 3, 6, 2, 4, 1, 7]`, `k = 3`, output `[-1, 5, 5, 6, 6, 6, 4]`.

**Example 2.** Input `score = [2, 2, 2]`, `k = 1`, output `[-1, 2, 2]`.

**Hint.** The current position is not allowed to answer for itself. Should it be appended before or after the front is read?

**Changed decision.** First rung: the answer is read before the current position is appended, and the age test uses the bound `i - k`.

#### [Vary] Variable Legal Left Bound (Author exercise)
<!-- id: dq-variable-left-bound -->

**Prerequisites.** The Best Of Last K Scores exercise above.

**Problem.** Given an integer array `a` and an array `low` of the same length with `low[i] <= i` and `low[i] <= low[i+1]`, return an array whose entry `i` is the largest value among positions `low[i]` through `i`, both ends included.

**Constraints.** 1 <= a.length <= 10^5, -10^9 <= a[i] <= 10^9, and `low` never decreases. Linear time.

**Example 1.** Input `a = [6, 2, 8, 3, 5, 4]`, `low = [0, 0, 1, 2, 2, 4]`, output `[6, 6, 8, 8, 8, 5]`.

**Example 2.** Input `a = [7, 7, 7]`, `low = [0, 1, 2]`, output `[7, 7, 7]`.

**Hint.** What replaces the constant `k` in the age test? What would break if one entry of `low` were smaller than the one before it?

**Changed decision.** The expiry bound is read from a supplied array for each position, and the current position is included in its own window.

#### [Boundary] Duplicate Values, Different Ages (Author exercise)
<!-- id: dq-duplicate-ages -->

**Prerequisites.** The two exercises above.

**Problem.** For every window of `k` consecutive positions, return the position of the oldest occurrence of the largest value in that window, as an index into `a`.

**Constraints.** 1 <= k <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Equal values are allowed.

**Example 1.** Input `a = [4, 4, 2, 4]`, `k = 2`, output `[0, 1, 3]`.

**Example 2.** Input `a = [3, 3, 3]`, `k = 2`, output `[0, 1]`.

**Hint.** If equal values may stay behind a newcomer in the deque, which of them will be at the front, and which one expires first?

**Changed decision.** Back removal is strict, so equal values are kept, and the front supplies the oldest of the tied positions.

#### [Recognize] Jump Game VI (LeetCode 1696)
<!-- id: dq-jump-game-six -->

**Prerequisites.** All three exercises above.

**Problem.** Start at index 0 of an integer array `nums` and reach the last index. From index `i` you may jump to any index from `i+1` to `i+k`, and the score is the sum of the values at every index visited, including the first and the last. Return the maximum score.

**Constraints.** 1 <= nums.length <= 10^5, -10^4 <= nums[i] <= 10^4 and 1 <= k <= nums.length. Linear time.

**Example 1.** Input `nums = [3, -2, 4, -1, 2, -5, 6]`, `k = 3`, output 15.

**Example 2.** Input `nums = [-4, -3, -5]`, `k = 1`, output -12.

**Hint.** The best score at an index depends on the best among the previous `k` best scores. What does the deque store, and what is compared in the back loop?

**Changed decision.** The deque holds positions ordered by computed best scores, not by input values, so the recurrence reads its previous best from the front.
