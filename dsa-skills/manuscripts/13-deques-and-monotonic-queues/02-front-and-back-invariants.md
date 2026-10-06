<!-- lesson-kind: standard -->
<!-- lesson-id: front-and-back-invariants -->
## Give Each End One Job

<!-- stage: context -->
### A Dashboard That Rescans Its Readings

A monitoring dashboard shows the highest latency reading seen so far. Each new reading arrives, and the panel must show the new maximum at once. The first version stores every reading in a list and scans the whole list after each arrival. With a few hundred readings the panel updates instantly. With a million readings the panel lags, because every arrival rescans everything that came before it.

This lesson asks one question. Can a deque hold only the readings that still matter, so that the answer is always at one known end? The answer is yes, and the price is a strict rule about what each end of the deque does.

<!-- stage: naive -->
### Scanning The Whole List Each Time

The direct plan keeps every reading and finds the largest one after each arrival.

```java
static int[] maxAfterEach(int[] readings) {
    List<Integer> seen = new ArrayList<>();
    int[] answers = new int[readings.length];
    for (int i = 0; i < readings.length; i++) {
        seen.add(readings[i]);
        int best = seen.get(0);
        for (int x : seen) best = Math.max(best, x);   // rescan every stored reading
        answers[i] = best;
    }
    return answers;
}
```

The method is correct. For the readings `4, 2, 7, 3` it returns `4, 4, 7, 7`.

<!-- stage: bottleneck -->
### Finding Readings That Cannot Win

```predict
The readings 4, 2 and 7 have arrived. Nothing ever expires. Can 4 or 2 still be the largest reading of any later set of readings?

Neither can. Every later set that contains 4 or 2 also contains the reading 7, which is larger, so 4 and 2 never win again. Only 7 needs to stay.
```

The method scans all `i` stored readings on arrival `i`, so the total cost for `n` readings is O(n^2). A million readings need about 500 billion reads. Most of those reads look at readings that lost long ago. After 7 arrives, the readings 4 and 2 are older and smaller, and they sit in the list for the rest of the run. Each later scan compares against them again and learns nothing. The repeated work is the comparison against readings that can never be the answer.

<!-- stage: insight -->
### Keeping Only Readings That Can Still Win

#### Naming The Readings That Matter

A reading that can still become the answer of some later query is a **candidate**. The method keeps only candidates, and it stores them in a deque so that the best candidate is always at one end. This lesson has no expiry, so a reading stays a candidate until a larger reading arrives after it.

#### Holding The Order Steady

The stored values follow one rule, called **non-increasing order**. Going from the front to the back, each value is equal to or smaller than the one before it. A deque that keeps this rule is a **monotonic deque**. The front is then the largest stored value, so the answer to the query is a read of one end.

#### Giving Each End One Job

Each end of the deque has one job. The back admits a new reading. Before the new reading enters, the method removes every strictly smaller value at the back. Those values can never win again. Then the new reading is appended. The front answers the query, and the method only reads it. The invariant is that the stored values stay in non-increasing order from front to back, and the largest stored value sits at the front. Each reading is appended once and removed at most once, so the total cost is O(n).

<!-- names: candidate, monotonic deque, non-increasing order -->

<!-- stage: variables -->
### What The Deque Holds Between Arrivals

Four pieces of state matter between one arrival and the next.

- **Deque** holds the candidates in non-increasing order, and it changes on every arrival.
- **Incoming value** is the reading being processed, and it is compared with the back only.
- **Front value** is the answer so far, and it changes only when a removal or an append makes a new front.
- **Strictness** decides whether an equal value at the back is removed, and this lesson keeps equal values.

The deque is never empty after the first arrival, because the incoming value is always appended.

<!-- stage: trace -->
### Watching The Order Hold

The first trace follows the readings `4, 2, 7, 3, 3, 1, 6` with the rule that keeps the largest value at the front. The reading 7 arrives third and removes both 2 and 4, so the deque shrinks to a single value. The second 3 does not remove the first 3, because equal values are kept, so the deque holds two copies. The final reading 6 removes the values 1, 3 and 3 and leaves `7, 6`.

The second trace follows `5, 3, 8, 2, 2, 7` with the opposite rule. The values now increase from front to back, so the front holds the smallest value. The comparison flips, and the structure stays the same. The reading 2 clears the whole deque when it arrives, because 2 is smaller than 8, 3 and 5.

```trace
{"cells":[4,2,7,3,3,1,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[4]","front":4},"note":"The back is not strictly smaller than 4, or the deque is empty, so nothing is removed and 4 is appended."},{"at":{"i":1},"vars":{"deque":"[4,2]","front":4},"note":"The back is not strictly smaller than 2, or the deque is empty, so nothing is removed and 2 is appended."},{"at":{"i":2},"vars":{"deque":"[7]","front":7},"note":"The value 7 removes 2, 4 from the back, because they are strictly smaller. Then 7 is appended."},{"at":{"i":3},"vars":{"deque":"[7,3]","front":7},"note":"The back is not strictly smaller than 3, or the deque is empty, so nothing is removed and 3 is appended."},{"at":{"i":4},"vars":{"deque":"[7,3,3]","front":7},"note":"The back is not strictly smaller than 3, or the deque is empty, so nothing is removed and 3 is appended."},{"at":{"i":5},"vars":{"deque":"[7,3,3,1]","front":7},"note":"The back is not strictly smaller than 1, or the deque is empty, so nothing is removed and 1 is appended."},{"at":{"i":6},"vars":{"deque":"[7,6]","front":7},"note":"The value 6 removes 1, 3, 3 from the back, because they are strictly smaller. Then 6 is appended."}]}
```

```trace
{"cells":[5,3,8,2,2,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[5]","front":5},"note":"The back is not strictly larger than 5, or the deque is empty, so nothing is removed and 5 is appended."},{"at":{"i":1},"vars":{"deque":"[3]","front":3},"note":"The value 3 removes 5 from the back, because they are strictly larger. Then 3 is appended."},{"at":{"i":2},"vars":{"deque":"[3,8]","front":3},"note":"The back is not strictly larger than 8, or the deque is empty, so nothing is removed and 8 is appended."},{"at":{"i":3},"vars":{"deque":"[2]","front":2},"note":"The value 2 removes 8, 3 from the back, because they are strictly larger. Then 2 is appended."},{"at":{"i":4},"vars":{"deque":"[2,2]","front":2},"note":"The back is not strictly larger than 2, or the deque is empty, so nothing is removed and 2 is appended."},{"at":{"i":5},"vars":{"deque":"[2,2,7]","front":2},"note":"The back is not strictly larger than 7, or the deque is empty, so nothing is removed and 7 is appended."}]}
```

<!-- stage: code -->
### Appending At The Back, Reading The Front

```java
static void pushMax(Deque<Integer> d, int x) {
    while (!d.isEmpty() && d.peekLast() < x) {   // strictly smaller values lose to x
        d.pollLast();                            // each value is removed at most once
    }
    d.addLast(x);                                // x enters at the back
}

static void pushMin(Deque<Integer> d, int x) {
    while (!d.isEmpty() && d.peekLast() > x) {   // strictly larger values lose to x
        d.pollLast();
    }
    d.addLast(x);
}

static int answer(Deque<Integer> d) {
    return d.peekFirst();                        // the front is the maximum, or the minimum for pushMin
}
```

The two push methods differ in one comparison. The method `pushMax` removes strictly smaller values, and `pushMin` removes strictly larger values. The method `answer` only reads. It must run after at least one push, because `peekFirst` returns `null` on an empty deque and the unboxing would fail.

- **Time** is O(1) amortized per push, since the loop removes values that earlier pushes added, and each value is added once.
- **Space** is O(n) in the worst case, which happens when the readings strictly decrease.

<!-- stage: applicability -->
### Deciding When Two Ends Suffice

#### Applying The Invariant

Use this structure when each query asks for the largest or smallest value among the readings kept so far. The invariant is that the values stay in non-increasing order, or in non-decreasing order for the minimum, and the front holds the answer. Every method that touches the deque must keep that order.

#### Finding The False Friend

The false friend is a deque whose two ends are interchangeable. A method that sometimes removes at the front to make room and sometimes removes at the back breaks the order proof. The back removes values that lost to a newer value. The front, in a later lesson, removes values that grew too old. Mixing the two reasons at one end removes values that may still win.

A sorted `TreeMap` also answers the maximum, but each update costs O(log n), and it keeps losers that the deque discards.

#### No-Go Conditions

Do not use this structure when a query asks for the second largest value, a median or a rank. The deque has thrown away exactly the values those queries need. Do not use it when a value must leave from the middle on demand, because only the two ends are cheap.

<!-- stage: exercises -->
### Exercises

#### [Build] Decreasing Candidate Values (Author exercise)
<!-- id: dq-decreasing-values -->

**Prerequisites.** The `ArrayDeque` calls from the previous lesson; this lesson.

**Problem.** A non-increasing deque has values that never grow from its front to its back. Start with an empty deque of `int`. Take the values of the input array in order. For each value `x`, remove every strictly smaller value from the back. Then append `x` at the back. When the input ends, report the values the deque holds, front first.

**Constraints.** The limits are:
- **Length** is between 0 and 100,000.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Ties** stay in the deque, because only strictly smaller values leave.
- **Output** is an `int[]`, empty for empty input.

**Example 1.** Input `[4, 2, 7, 3]`, output `[7, 3]`.

**Example 2.** Input `[5, 5, 5]`, output `[5, 5, 5]`, because equal values never remove each other.

**Hint.** Compare the incoming value with the back only. Which value at the back does the new value remove first?

**Changed decision.** First exercise of the lesson: the back removes losers and then admits the newcomer.

#### [Vary] Increasing Candidate Values (Author exercise)
<!-- id: dq-increasing-values -->

**Prerequisites.** The decreasing exercise above.

**Problem.** A non-decreasing deque has values that never shrink from its front to its back. Given an integer array, process the values in order. For each value `x`, remove from the back every value strictly larger than `x`, append `x`, and record the value at the front. Return the array of recorded front values.

**Constraints.** The limits are:
- **Length** is between 0 and 100,000.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Output** has the same length as the input.
- **Ties** stay in the deque, because only strictly larger values leave.

**Example 1.** Input `[5, 3, 8, 2]`, output `[5, 3, 3, 2]`.

**Example 2.** Input `[1, 2, 3]`, output `[1, 1, 1]`, because no value ever removes the front.

**Hint.** Only the comparison changes. Which value is at the front of a non-decreasing deque?

**Changed decision.** The comparison flips, so the front holds the smallest value instead of the largest.

#### [Boundary] Equal Candidate Policy (Author exercise)
<!-- id: dq-equal-policy -->

**Prerequisites.** Both exercises above.

**Problem.** Two policies handle a value equal to the back. The keep policy leaves the equal back value in place and appends the new value. The replace policy removes the equal back value and then appends the new value. Given an integer array and a boolean `keepEqual`, build a deque of maxima, with larger values nearer the front, under the chosen policy. Return the final deque from the front to the back.

**Constraints.** The limits are:
- **Length** is between 0 and 100,000.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Flag** `keepEqual` chooses the policy once for the whole run.
- **Output** is an `int[]`, empty for empty input.

**Example 1.** Input `[4, 4, 2]` with `keepEqual = true`, output `[4, 4, 2]`.

**Example 2.** Input `[4, 4, 2]` with `keepEqual = false`, output `[4, 2]`.

**Hint.** The policies differ in one comparison, strictly smaller or smaller-or-equal. Does either policy change the value at the front?

**Changed decision.** The tie rule becomes an explicit choice, and both choices keep the same answer at the front.

#### [Recognize] Name Each End (Author exercise)
<!-- id: dq-name-each-end -->

**Prerequisites.** The roles of the two ends from this lesson.

**Problem.** A trace lists the removals of a deque of candidates. Each record is a pair of strings. The first string is the end that lost an item, `front` or `back`. The second string is the cause, `age` when the item became too old, or `value` when a newer and better item arrived. An age removal must use the front, and a value removal must use the back. Return the position of the first record whose end does not match its cause, or `-1` when every record matches.

**Constraints.** The limits are:
- **Records** number between 0 and 100,000.
- **Ends** are exactly `front` or `back`.
- **Causes** are exactly `age` or `value`.
- **Output** is a zero-based position, or `-1`.

**Example 1.** Input `[["front", "age"], ["back", "value"]]`, output `-1`.

**Example 2.** Input `[["back", "age"]]`, output `0`, because a back removal cannot be an age removal.

**Hint.** Which end holds the oldest item, and which end holds the weakest newest item?

**Changed decision.** The task reads a trace and judges each removal by its end and its cause.
