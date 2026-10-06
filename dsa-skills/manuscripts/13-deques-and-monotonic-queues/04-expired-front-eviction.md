<!-- lesson-kind: standard -->
<!-- lesson-id: expired-front-eviction -->
## Remove Old Indices From The Front

<!-- stage: context -->
### A Spike That Never Goes Away

A dashboard reports the highest latency among the last three requests. One request takes 12 milliseconds, and the panel shows 12. Three requests later the spike is old news, yet the panel still shows 12. The code removes entries that a newer, larger value beats. It has no way to remove an entry that has simply become too old.

This lesson answers one question. How does the method find and remove entries that have left the range of recent positions, and why is the front of the deque the only place it needs to look?

<!-- stage: naive -->
### Rescanning The Last k Values

The direct plan finds the maximum of each range by reading every value in it. For a range of length `k` that ends at position `right`, it reads the positions from `right - k + 1` through `right`.

```java
static int[] rescan(int[] a, int k) {
    int[] out = new int[a.length - k + 1];
    for (int right = k - 1; right < a.length; right++) {
        int best = a[right];
        for (int j = right - k + 1; j < right; j++) {
            best = Math.max(best, a[j]);          // read every value in the range
        }
        out[right - k + 1] = best;
    }
    return out;
}
```

For `a = [4, 2, 12, 3, 8, 1]` and `k = 3`, the method returns `12, 12, 12, 8`. Each answer is correct.

<!-- stage: bottleneck -->
### Counting Reads And Spotting Stale Entries

```predict
The deque holds the positions 2 and 4, and the range length is 3. The right end moves to position 5. Is position 2 still a legal entry?

No. The range ending at 5 covers positions 3, 4 and 5, so position 2 has fallen out of it. Its value may still be the largest, but the value no longer counts.
```

The rescan reads about `k` values for each of the `n` ranges, so the total cost is O(n * k). With `n = 1,000,000` and `k = 1,000` that is about one billion reads. Neighbouring ranges share `k - 1` values, so each read repeats an earlier read.

A deque of weaker-value removals avoids those reads, but it brings a new problem. The value order cannot show that an entry is old. The entry for position 2 holds the value 12, which is the largest, so it sits at the front forever unless something checks its position. Age is a property of the position, and the position must be checked on purpose.

<!-- stage: insight -->
### Checking The Age Of The Front Entry

#### Defining An Expired Entry

A range of length `k` that ends at `right` has a **left bound** equal to `right - k + 1`. A stored position is **expired** when it is smaller than the left bound. For a fixed length `k`, this means the position is at most `right - k`. An expired position can never return to the range, because the right end only moves forward.

#### Testing Only The Front

The stored positions increase from the front to the back, because each arrival appends the newest position at the back. The oldest stored position is therefore at the front. If the front is not expired, no later entry is expired either. The **age test** compares the front position with the left bound and removes the front while the test says expired. The test never needs to look past the first legal entry.

#### Using A Loop Instead Of A Single Check

A fixed length removes at most one position per step, so a single `if` is enough in that case. A left bound that jumps can expire several positions at once, so the age test is a loop and not a single `if`. The invariant is that before the method reads the answer for the range ending at `right`, every stored position is at least the left bound. Each position is removed by the age test at most once, so the total cost of all age tests is O(n).

<!-- names: left bound, expired, age test -->

<!-- stage: variables -->
### What Each Step Tracks

Each step reads and updates four pieces of state.

- **right** is the position that arrives now, and it increases by one on each step.
- **k** is the fixed range length, and it never changes during the run.
- **Left bound** is `right - k + 1`, and it is the smallest legal position.
- **Front position** is the oldest stored position, and the age test reads only this entry.

The deque stores positions, so the age test compares positions and never values. The value order from the previous lesson is untouched by this test.

<!-- stage: trace -->
### Following Expiry Through A Run

The first trace follows `a = [4, 2, 12, 3, 8, 1]` with `k = 3`. The value 12 at position 2 removes positions 1 and 0 from the back, so only position 2 is stored. The age test finds nothing on the next two steps, because position 2 stays inside the range. At position 5 the left bound reaches 3, and position 2 is at most `5 - 3`, so the age test removes it from the front. The final deque holds positions 4 and 5.

The second trace isolates expiry. It appends every position and ignores values, and a supplied left bound moves forward by uneven amounts. At position 3 the left bound jumps from 1 to 3, and the age test removes two entries in one step. At position 5 it removes two more. The trace shows why the age test must be a loop.

```trace
{"cells":[4,2,12,3,8,1],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","expired":0,"dominated":0},"note":"Right edge 0 brings the value 4. The deque is empty, so nothing can be stale. Nothing is removed from the back. Index 0 is appended."},{"at":{"right":1},"vars":{"deque":"[0,1]","expired":0,"dominated":0},"note":"Right edge 1 brings the value 2. The age test finds nothing stale, since the front is above -2. Nothing is removed from the back. Index 1 is appended."},{"at":{"right":2},"vars":{"deque":"[2]","expired":0,"dominated":2},"note":"Right edge 2 brings the value 12. The deque is empty, so nothing can be stale. The value 12 removes index 1, 0 from the back. Index 2 is appended."},{"at":{"right":3},"vars":{"deque":"[2,3]","expired":0,"dominated":0},"note":"Right edge 3 brings the value 3. The age test finds nothing stale, since the front is above 0. Nothing is removed from the back. Index 3 is appended."},{"at":{"right":4},"vars":{"deque":"[2,4]","expired":0,"dominated":1},"note":"Right edge 4 brings the value 8. The age test finds nothing stale, since the front is above 1. The value 8 removes index 3 from the back. Index 4 is appended."},{"at":{"right":5},"vars":{"deque":"[4,5]","expired":1,"dominated":0},"note":"Right edge 5 brings the value 1. The age test removes index 2 from the front, since 5 - 3 = 2 and the index is at most that. Nothing is removed from the back. Index 5 is appended."}]}
```

```trace
{"cells":[0,1,2,3,4,5],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","bound":0,"expired":0},"note":"Right edge 0 appends index 0. The legal left bound is 0, and the front is already legal."},{"at":{"right":1},"vars":{"deque":"[0,1]","bound":0,"expired":0},"note":"Right edge 1 appends index 1. The legal left bound is 0, and the front is already legal."},{"at":{"right":2},"vars":{"deque":"[1,2]","bound":1,"expired":1},"note":"Right edge 2 appends index 2. The legal left bound is 1, so index 0 expire from the front."},{"at":{"right":3},"vars":{"deque":"[3]","bound":3,"expired":2},"note":"Right edge 3 appends index 3. The legal left bound is 3, so index 1, 2 expire from the front."},{"at":{"right":4},"vars":{"deque":"[3,4]","bound":3,"expired":0},"note":"Right edge 4 appends index 4. The legal left bound is 3, and the front is already legal."},{"at":{"right":5},"vars":{"deque":"[5]","bound":5,"expired":2},"note":"Right edge 5 appends index 5. The legal left bound is 5, so index 3, 4 expire from the front."}]}
```

<!-- stage: code -->
### Expiring And Updating In Order

```java
static void expireFront(Deque<Integer> d, int leftBound) {
    while (!d.isEmpty() && d.peekFirst() < leftBound) {   // the front is the oldest position
        d.pollFirst();                                    // each position expires once
    }
}

static void update(int[] a, Deque<Integer> d, int right, int k) {
    expireFront(d, right - k + 1);                        // the age test comes first
    while (!d.isEmpty() && a[d.peekLast()] < a[right]) {  // then the back removes weaker values
        d.pollLast();
    }
    d.addLast(right);                                     // the new position enters last
}
```

The age test runs before any read of the front, because `peekFirst` could otherwise return an expired position. The check `!d.isEmpty()` comes first in the condition, since `peekFirst` returns `null` on an empty deque and the comparison would throw. After `update` finishes, the deque is never empty, because the new position was just appended.

- **Time** is O(1) amortized per update, because the two loops remove positions that earlier updates appended.
- **Space** is O(k), because every stored position lies inside one range of length `k`.

<!-- stage: applicability -->
### Deciding When Expiry Applies

#### Applying The Invariant

Use the age test whenever a stored entry stops counting after some number of positions. The invariant is that every stored position is at least the left bound before any read of the front. Any method that appends positions in increasing order can rely on the front being the oldest entry.

#### Finding The False Friend

The false friend is a value-based test. A method that removes entries whose value looks small, or that trusts the value order, cannot detect age. The entry with the largest value is the one that stays longest, and it is the most likely to be expired. The order of values answers which entry is best, and only the position answers whether the entry is still legal.

#### No-Go Conditions

Do not use a front-only age test when positions are not appended in increasing order, because the oldest entry may then sit in the middle. Do not use it when entries expire by a rule that is not monotone in position, such as a score that decays unevenly. In that case an older entry may outlast a newer one, and the front gives no guarantee.

<!-- stage: exercises -->
### Exercises

#### [Build] Expire One Window (Author exercise)
<!-- id: dq-expire-one -->

**Prerequisites.** Storing positions in a deque from the previous lesson; this lesson.

**Problem.** A deque holds positions in strictly increasing order from the front to the back. A left bound `L` is an integer. A position is expired when it is smaller than `L`. Remove expired positions from the front until the front is at least `L` or the deque is empty. Return the remaining positions from the front to the back.

**Constraints.** The limits are:
- **Positions** number between 0 and 100,000 and strictly increase.
- **Values** of positions are between 0 and 1,000,000.
- **Bound** `L` is an integer between 0 and 1,000,000.
- **Output** is an `int[]`, empty when every position expires.

**Example 1.** Input positions `[2, 4]` with `L = 3`, output `[4]`.

**Example 2.** Input positions `[3, 4, 5]` with `L = 3`, output `[3, 4, 5]`, because the front is already legal.

**Hint.** Which end holds the smallest position? Where does the first legal position stop the removal?

**Changed decision.** First exercise of the lesson: the age test looks at the front only.

#### [Vary] Jumping Boundary (Author exercise)
<!-- id: dq-jumping-boundary -->

**Prerequisites.** The expire exercise above.

**Problem.** An array `bound` has one left bound per step, and `bound[r] <= r` for every `r`. The array never decreases. On step `r`, append position `r` to an initially empty deque. Then remove from the front every position smaller than `bound[r]`. Record the front position after the removals. Return the array of recorded fronts.

**Constraints.** The limits are:
- **Length** is between 0 and 100,000.
- **Bounds** satisfy `0 <= bound[r] <= r` and never decrease.
- **Removals** per step can be zero, one or many.
- **Output** has the same length as `bound`.

**Example 1.** Input `[0, 0, 1, 3, 3, 5]`, output `[0, 0, 1, 3, 3, 5]`.

**Example 2.** Input `[0, 0, 0]`, output `[0, 0, 0]`.

**Hint.** One step can expire several positions. Does a single `if` or a loop handle the jump from 1 to 3?

**Changed decision.** The left bound moves by uneven amounts, so the age test becomes a loop.

#### [Boundary] Exact Expiry Point (Author exercise)
<!-- id: dq-exact-expiry -->

**Prerequisites.** The jumping boundary exercise above.

**Problem.** A range has length `k` and ends at position `right`. It holds the positions `right - k + 1` through `right`, and it holds fewer when `right - k + 1` is negative. Given the number of positions `n` and the length `k`, append positions `0` through `n - 1` one at a time to an initially empty deque. After each append, remove expired positions from the front. Return, for each step, the front position after the removals.

**Constraints.** The limits are:
- **Count** `n` is between 0 and 100,000.
- **Length** `k` is between 1 and 100,000.
- **Range** includes both of its end positions.
- **Output** has length `n`.

**Example 1.** Input `n = 5`, `k = 3`, output `[0, 0, 0, 1, 2]`.

**Example 2.** Input `n = 3`, `k = 1`, output `[0, 1, 2]`.

**Hint.** For `k = 3` and `right = 3`, which position is the first one outside the range? Compare it with `right - k`.

**Changed decision.** The task is the exact comparison that separates the last legal position from the first expired one.

#### [Recognize] Chronological Candidate Queue (Author exercise)
<!-- id: dq-chronological-queue -->

**Prerequisites.** The weaker-value removal and the age test.

**Problem.** An integer array `a` has a range of length `k` that ends at position `right`. A list `stored` claims to be the state of a deque of positions for that range under the maximum rule. The state is legal when three facts hold. Reading from the front, the positions strictly increase. Every position lies from `right - k + 1` through `right`. The values `a[stored[i]]` never increase from the front to the back. Return `true` when the state is legal and `false` otherwise.

**Constraints.** The limits are:
- **Array** `a` has between 1 and 100,000 values.
- **Length** `k` is between 1 and the length of `a`.
- **Right** is between 0 and the length of `a` minus 1.
- **Stored** has between 0 and `k` entries, each between 0 and the length of `a` minus 1.

**Example 1.** Input `a = [4, 2, 12, 3, 8, 1]`, `k = 3`, `right = 4`, `stored = [2, 4]`, output `true`.

**Example 2.** Input the same array with `stored = [1, 2]`, output `false`, because the values 2 and 12 rise.

**Hint.** Check the three facts in turn. Which one catches a position that left the range?

**Changed decision.** The exercise reads a finished state and judges it, instead of building it.
