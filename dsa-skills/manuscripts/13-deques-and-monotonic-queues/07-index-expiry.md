<!-- lesson-kind: standard -->
<!-- lesson-id: index-expiry -->
## Allow Only Recent Positions

<!-- stage: context -->
### A Rule That Looks Back

A fraud rule flags a payment when it is larger than every one of the previous five payments on the same account. The rule never compares a payment with itself, and it ignores payments older than five steps. The first version of the rule looks up the last five payments for every new payment. That lookup is cheap for five payments. A related rule needs the last 50,000 events, and the lookup then dominates the running time.

The earlier lessons answered a question about a range that ends at the current position. This rule asks about the positions before the current one. The order of the steps changes, and this lesson shows how. The question is: when a position may only look back a limited distance, which step runs before the read and which runs after?

<!-- stage: naive -->
### Scanning The Last k Positions

The direct plan keeps the last `k` positions in a queue. For each new position, it scans the queue for the best value, records it, and then adds the new position. When the queue holds more than `k` positions, it drops the oldest one.

```java
static int[] bestOfPrevious(int[] a, int k) {
    Deque<Integer> recent = new ArrayDeque<>();
    int[] out = new int[a.length];
    for (int i = 0; i < a.length; i++) {
        int best = -1;                                  // no earlier position gives -1
        for (int j : recent) best = Math.max(best, a[j]);   // scan every stored position
        out[i] = best;
        recent.addLast(i);
        if (recent.size() > k) recent.pollFirst();
    }
    return out;
}
```

The method is correct when every value is at least zero. For `a = [5, 3, 6, 2]` and `k = 2` it returns `-1, 5, 5, 6`.

<!-- stage: bottleneck -->
### Why Older Positions Never Win Again

```predict
The scores 5 and then 8 arrive, and a position may look back at most 3 positions. Can the score 5 ever be the best of the positions a later query can see?

No. Every later query that can see 5 can also see 8, because 8 arrived after 5 and stays visible longer than 5 does. Since 8 is larger, 5 never wins.
```

Each query scans up to `k` stored positions, so the total cost is O(n * k). For `n = 1,000,000` and `k = 50,000` that is about fifty billion comparisons. The scan reads positions that already lost, and it reads them again for every later query. The repeated work is the comparison against positions that a newer and larger position will outlast.

<!-- stage: insight -->
### Expiring By Position And Reading Before Appending

#### Saying Which Positions Are Eligible

A position `j` is **eligible** for the query at position `i` when `i - k <= j < i`. The upper limit excludes `i` itself. The lower limit moves forward by one for each new `i`. The deque stores positions, because a value alone cannot say when its entry stops being eligible.

#### Keeping The Newer Entry

A newer position can **outlast** an older one, because it stays eligible for more future queries. When the new score is at least as large as an older stored score, the older entry can never win and leaves from the back. The newer entry is the only one that needs to stay.

#### Choosing The Query Order

The **query order** for this lesson differs from the window maximum. The query at `i` must not see `i`, so the steps run in a different order. First, the age test removes the front positions that are smaller than `i - k`. Second, the read takes the front as the answer. Third, the back removes positions that the new score beats. Fourth, the append adds `i`. The read comes before the append, since the append would put `i` into its own query. The invariant is that, at the read, every stored position is eligible and no stored position is beaten by a later eligible one. Each position leaves at most once, so the total cost is O(n).

<!-- names: eligible, outlast, query order -->

<!-- stage: variables -->
### What Changes Between Queries

The method keeps four pieces of state.

- **i** is the current position, and it is the only position that does not appear in its own query.
- **k** is the farthest distance a position can look back, and it does not change.
- **Deque** holds eligible positions with non-increasing scores, and the front is the answer.
- **Answer** is the front score, or the sentinel `-1` when the deque is empty.

The sentinel works only because every score is at least zero. A problem that allows a score of `-1` needs another way to say that no position is eligible.

<!-- stage: trace -->
### Reading Before The Append

The first trace follows `a = [5, 3, 6, 2, 4, 1, 7]` with `k = 3`. At position 0 the deque is empty, so the answer is none, and position 0 is appended. At position 3 the age test removes nothing, because `3 - 3 = 0` and position 0 is still eligible. The read gives 6 from position 2. At position 4 the age test removes position 0, since 0 is smaller than `4 - 3`. The answers are `[-1, 5, 5, 6, 6, 6, 4]`.

The second trace gives each position a score equal to its own value plus the best score among the previous three positions. The array is `[3, -2, 4, -1, 2, -5, 6]`. The start has score 3. Position 2 reads the front, which is position 0 with score 3, so its score is 7. The scores may be negative here, and the front is still the largest eligible score. The last score is 15.

```trace
{"cells":[5,3,6,2,4,1,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[0]","answers":"[-1]"},"note":"Position 0 holds 5. No earlier position is eligible, so the answer is none. Then position 0 is appended."},{"at":{"i":1},"vars":{"deque":"[0,1]","answers":"[-1,5]"},"note":"Position 1 holds 3. The front gives the answer 5. Then position 1 is appended."},{"at":{"i":2},"vars":{"deque":"[2]","answers":"[-1,5,5]"},"note":"Position 2 holds 6. The front gives the answer 5. Then the value 6 removes position 1, 0 from the back. Then position 2 is appended."},{"at":{"i":3},"vars":{"deque":"[2,3]","answers":"[-1,5,5,6]"},"note":"Position 3 holds 2. The front gives the answer 6. Then position 3 is appended."},{"at":{"i":4},"vars":{"deque":"[2,4]","answers":"[-1,5,5,6,6]"},"note":"Position 4 holds 4. The front gives the answer 6. Then the value 4 removes position 3 from the back. Then position 4 is appended."},{"at":{"i":5},"vars":{"deque":"[2,4,5]","answers":"[-1,5,5,6,6,6]"},"note":"Position 5 holds 1. The front gives the answer 6. Then position 5 is appended."},{"at":{"i":6},"vars":{"deque":"[6]","answers":"[-1,5,5,6,6,6,4]"},"note":"Position 6 holds 7. The age test removes position 2 from the front. The front gives the answer 4. Then the value 7 removes position 5, 4 from the back. Then position 6 is appended."}]}
```

```trace
{"cells":[3,-2,4,-1,2,-5,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"scores":"[3]","deque":"[0]"},"note":"The start is worth 3 and position 0 is stored."},{"at":{"i":1},"vars":{"scores":"[3,1]","deque":"[0,1]"},"note":"Position 1 holds -2. The front is position 0 with score 3, so the score here is 1."},{"at":{"i":2},"vars":{"scores":"[3,1,7]","deque":"[2]"},"note":"Position 2 holds 4. The front is position 0 with score 3, so the score here is 7. The new score removes position 1, 0 from the back."},{"at":{"i":3},"vars":{"scores":"[3,1,7,6]","deque":"[2,3]"},"note":"Position 3 holds -1. The front is position 2 with score 7, so the score here is 6."},{"at":{"i":4},"vars":{"scores":"[3,1,7,6,9]","deque":"[4]"},"note":"Position 4 holds 2. The front is position 2 with score 7, so the score here is 9. The new score removes position 3, 2 from the back."},{"at":{"i":5},"vars":{"scores":"[3,1,7,6,9,4]","deque":"[4,5]"},"note":"Position 5 holds -5. The front is position 4 with score 9, so the score here is 4."},{"at":{"i":6},"vars":{"scores":"[3,1,7,6,9,4,15]","deque":"[6]"},"note":"Position 6 holds 6. The front is position 4 with score 9, so the score here is 15. The new score removes position 5, 4 from the back."}]}
```

<!-- stage: code -->
### Expire, Read, Remove, Append

```java
static int[] bestOfPrevious(int[] a, int k) {
    int[] out = new int[a.length];
    Deque<Integer> d = new ArrayDeque<>();                   // eligible positions, scores non-increasing
    for (int i = 0; i < a.length; i++) {
        while (!d.isEmpty() && d.peekFirst() < i - k) d.pollFirst();   // 1: age test
        out[i] = d.isEmpty() ? -1 : a[d.peekFirst()];                  // 2: read before the append
        while (!d.isEmpty() && a[d.peekLast()] < a[i]) d.pollLast();   // 3: weaker scores leave
        d.addLast(i);                                                  // 4: append
    }
    return out;
}

static int bestPathScore(int[] nums, int k) {
    int n = nums.length;
    int[] score = new int[n];
    score[0] = nums[0];
    Deque<Integer> d = new ArrayDeque<>();
    d.addLast(0);
    for (int i = 1; i < n; i++) {
        while (d.peekFirst() < i - k) d.pollFirst();                   // the deque is never empty here
        score[i] = nums[i] + score[d.peekFirst()];                     // best earlier score plus own value
        while (!d.isEmpty() && score[d.peekLast()] <= score[i]) d.pollLast();
        d.addLast(i);
    }
    return score[n - 1];
}
```

The second method keeps a score for every position. The score of position `i` is its own value plus the best score among the previous `k` positions. The deque in `bestPathScore` is never empty at the read, because position `i - 1` was appended last and is always eligible.

- **Time** is O(n) for both methods, because each position is appended once and each age test removes a position only once.
- **Space** is O(k) for the deque in the first method, and O(n) for the score array in the second.

<!-- stage: applicability -->
### Checking The Distance Rule

#### Applying The Invariant

Use the pattern when each position may use only positions within a fixed distance behind it, and the question asks for the best of them. The invariant is that every stored position is eligible and no stored position has a newer eligible position with an equal or better score. The age test uses a strict comparison with `i - k`, so check the boundary on a case with `k = 1`.

#### Finding The False Friend

The false friend is a deque that stores values instead of positions. A value hides how old its entry is. When two equal values arrive at different positions, they expire at different times, and a value-only deque cannot tell which copy to remove. Storing positions keeps the age and still gives the value through the array.

A second false friend is a method that appends before it reads. That method includes position `i` in its own query, and it returns the wrong answer whenever position `i` holds the best score.

#### No-Go Conditions

Do not use this pattern when the best earlier value depends on more than a distance. An example is a position that may use only entries of a certain type. The age test then removes the wrong entries. Do not use it when the distance limit differs for every query in a way that is not monotone, because the front would not be the oldest legal entry.

<!-- stage: exercises -->
### Exercises

#### [Build] Best Of Last K Scores (Author exercise)
<!-- id: dq-best-of-last-k -->

**Prerequisites.** The window maximum and the age test from earlier lessons; this lesson.

**Problem.** An array `scores` holds non-negative integers, and `k` is a distance. For each position `i`, the eligible positions are those from `max(0, i - k)` through `i - 1`. Return an array whose entry `i` is the largest score among the eligible positions, or `-1` when `i` has no eligible position. Use a deque of positions and read before you append.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Distance** `k` is between 1 and 100,000.
- **Scores** are integers between 0 and 1,000,000.
- **Output** has `n` entries, and the entry at position 0 is `-1`.

**Example 1.** Input `scores = [5, 3, 6, 2, 4, 1, 7]`, `k = 3`, output `[-1, 5, 5, 6, 6, 6, 4]`.

**Example 2.** Input `scores = [9, 1, 1]`, `k = 1`, output `[-1, 9, 1]`.

**Hint.** The query at `i` must not see position `i`. Which step runs between the age test and the append?

**Changed decision.** First exercise of the lesson: the read moves before the append.

#### [Vary] Variable Legal Left Bound (Author exercise)
<!-- id: dq-variable-bound -->

**Prerequisites.** The first exercise above.

**Problem.** An array `scores` holds non-negative integers, and an array `bound` gives a legal left bound for each position. The bound never decreases, and `bound[i] <= i`. For each position `i`, the eligible positions are those from `bound[i]` through `i - 1`. Return an array whose entry `i` is the largest eligible score, or `-1` when no position is eligible.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000, and both arrays have length `n`.
- **Bounds** satisfy `0 <= bound[i] <= i` and never decrease.
- **Scores** are integers between 0 and 1,000,000.
- **Output** has `n` entries.

**Example 1.** Input `scores = [4, 8, 2, 6]`, `bound = [0, 0, 1, 2]`, output `[-1, 4, 8, 2]`.

**Example 2.** Input `scores = [3, 3, 3]`, `bound = [0, 0, 1]`, output `[-1, 3, 3]`.

**Hint.** A bound that jumps can expire several positions at once. Does a single `if` or a loop remove them?

**Changed decision.** The age test compares with a supplied bound instead of `i - k`.

#### [Boundary] Duplicate Values, Different Ages (Author exercise)
<!-- id: dq-duplicate-ages -->

**Prerequisites.** The second exercise above and the tie rule from the weaker-value lesson.

**Problem.** Take the same eligible positions as in the first exercise, with non-negative integer `scores` and a distance `k`. Return an array whose entry `i` is the position of the largest eligible score. If several eligible positions hold that score, return the largest of those positions. Return `-1` when no position is eligible.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Distance** `k` is between 1 and 100,000.
- **Scores** are integers between 0 and 1,000,000, and many may be equal.
- **Output** has `n` entries of positions or `-1`.

**Example 1.** Input `scores = [4, 4, 1, 1]`, `k = 2`, output `[-1, 0, 1, 1]`.

**Example 2.** Input `scores = [2, 2, 2]`, `k = 1`, output `[-1, 0, 1]`.

**Hint.** A value alone cannot say which copy to return. Which tie rule keeps the newest copy of the best score?

**Changed decision.** The answer is a position, so the deque must keep each entry's identity and its age.

#### [Recognize] LC 1696 Jump Game VI (LeetCode 1696)
<!-- id: dq-lc1696 -->

**Prerequisites.** All earlier exercises in this lesson.

**Problem.** An integer array `nums` and an integer `k` describe a walk that starts at position 0. From position `i` the walk may jump to any position from `i + 1` through `min(i + k, n - 1)`. The score of a walk is the sum of `nums` at every position it visits, including the first and the last. Return the largest score of a walk that ends at position `n - 1`.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Distance** `k` is between 1 and `n`.
- **Values** are integers between -10,000 and 10,000, and the answer fits in `int`.
- **Walk** must end at the last position and may not move left.

**Example 1.** Input `nums = [3, -2, 4, -1, 2, -5, 6]`, `k = 3`, output `15`.

**Example 2.** Input `nums = [-5, -3, -1]`, `k = 1`, output `-9`.

**Hint.** The best score of a walk that ends at `i` is `nums[i]` plus the best score among positions `i - k` through `i - 1`. Which structure answers that in constant time?

**Changed decision.** The scores are computed as the loop runs, and the deque stores positions ordered by those scores.
