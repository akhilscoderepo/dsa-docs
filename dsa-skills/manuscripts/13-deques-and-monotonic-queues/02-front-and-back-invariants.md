<!-- lesson-kind: standard -->
<!-- lesson-id: front-and-back-invariants -->
## Front And Back Invariants

<!-- stage: context -->
### A Shortlist Beside The Stage

A talent show runs for a whole evening. Contestants perform one after another, and a judge scores each act with a number. The stage manager keeps a shortlist on a clipboard at the side of the stage, and her only job is to be able to say at any moment which act on the shortlist is the strongest. When a new act finishes, she compares it with the entries at the bottom of the list. Any earlier act that scored lower is crossed off, because the newcomer is stronger and will still be around when the earlier act has long been forgotten. Then she writes the newcomer at the bottom.

The strongest act is always the one at the top of her clipboard, so a glance answers the question. She never reads from the bottom, since the bottom holds the most recent act and not the best one, and she never writes a new act at the top, since that would put a recent act ahead of stronger ones. Each end of the clipboard has its own job.

<!-- stage: naive -->
### Rescan Every Act For The Best

The direct method keeps every score in a list and, whenever someone asks for the strongest act, scans the whole list.

```java
static int[] bestAfterEachAct(int[] scores) {
    int[] best = new int[scores.length];
    for (int i = 0; i < scores.length; i++) {
        int top = scores[0];
        for (int j = 1; j <= i; j++) top = Math.max(top, scores[j]);
        best[i] = top;
    }
    return best;
}
```

It is correct: for the scores `[3, 1, 4, 1]` it returns `[3, 3, 4, 4]`, since after each act the best of all acts so far is read from the list.

<!-- stage: bottleneck -->
### Past Acts Are Reread Every Time

After `i` acts the scan visits all `i + 1` scores, so the whole show costs about `n * n / 2` comparisons, which is O(n^2). For 100,000 acts that is five billion comparisons just to answer one small question after each act. Most of the scanning is wasted, because a score that is lower than a later score can never be the answer again once the later one has arrived: the later act is stronger and stays on stage at least as long.

So the list is carrying entries that are guaranteed to be useless. What the stage manager needs is a structure that throws such entries away at the moment they become useless, which is when something better arrives behind them, and that keeps the survivors in an order that makes the best one easy to find without a scan.

<!-- stage: insight -->
### One End Reads, The Other End Admits

The shortlist is a deque with one rule for its contents and two jobs for its ends. The **order rule** says that values decrease from front to back, or increase from front to back when minima are wanted. Because of this rule the entry at the front is the strongest survivor, and the answer is always one `peekFirst` away.

The **back admitter** is the end where a new value enters. Before the newcomer is appended, every entry at the back that the newcomer beats is removed, since such an entry is older and weaker and therefore can never be the answer again. Removal stops at the first entry that is at least as strong, which keeps the order rule true, and the newcomer is appended last. The **front reader** is the other end. It only reads the answer and, in later lessons, removes entries that have become too old. Neither end can do the job of the other: reading at the back returns the newest survivor, which is the weakest, and admitting at the front would break the order rule and the chronological order that expiry relies on.

<!-- names: order rule, back admitter, front reader -->

Equal values need a decision. Keeping equal entries preserves older copies, which will expire sooner than the newer copy, and replacing them keeps the deque shorter, because the newer copy is as strong and will outlast the older one. Both policies give the right current maximum. The choice matters only for how long the deque is and for which index a later expiry will remove, so it must be stated and kept.

The total cost is O(n) for `n` values: every value enters the deque a single time and leaves it no more than a single time, although a single arrival may remove many entries.

<!-- stage: variables -->
### The Deque, The Comparison And The Policy

The deque holds the surviving candidates, in the order in which they arrived. The comparison decides which entries a newcomer removes: strictly smaller for a decreasing deque, strictly larger for an increasing one, with equals kept, or smaller-or-equal and larger-or-equal when equals are replaced. The policy for equals is the one decision that is easy to forget, and writing it next to the comparison avoids a mismatch later. Store indices when anything about the entry's age matters, and store values when only the shortlist itself is wanted. The front is the answer, the back is where the next arrival will look first, and the size of the deque is the number of candidates still alive.

<!-- stage: trace -->
### Shortlists For Highest And For Lowest

Take the scores `4, 2, 7, 3, 3, 1, 6` and keep a decreasing shortlist, removing only strictly smaller entries. The 4 enters an empty list. The 2 is not larger than the 4, so it is appended behind it. The 7 beats both, so the 2 and then the 4 are removed from the back, and the list is just the 7. The 3 is appended, and the second 3 is not strictly larger than the first, so both stay. The 1 is appended. The 6 removes the 1 and the two 3s and stops at the 7. The final list reads 7, 6 and its front is the strongest score. The step to study is the arrival of the 7, which empties the list at the back and leaves the front changed.

Now keep an increasing shortlist for the lowest score over `5, 3, 8, 2, 2, 7`. The 3 removes the 5, the 8 is appended, the first 2 removes the 8 and the 3, and the second 2 is kept next to it. The 7 is appended and the front stays 2.

```trace
{"cells":[4,2,7,3,3,1,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[4]","front":4},"note":"The back is not strictly smaller than 4, or the deque is empty, so nothing is removed and 4 is appended."},{"at":{"i":1},"vars":{"deque":"[4,2]","front":4},"note":"The back is not strictly smaller than 2, or the deque is empty, so nothing is removed and 2 is appended."},{"at":{"i":2},"vars":{"deque":"[7]","front":7},"note":"The value 7 removes 2, 4 from the back, because they are strictly smaller. Then 7 is appended."},{"at":{"i":3},"vars":{"deque":"[7,3]","front":7},"note":"The back is not strictly smaller than 3, or the deque is empty, so nothing is removed and 3 is appended."},{"at":{"i":4},"vars":{"deque":"[7,3,3]","front":7},"note":"The back is not strictly smaller than 3, or the deque is empty, so nothing is removed and 3 is appended."},{"at":{"i":5},"vars":{"deque":"[7,3,3,1]","front":7},"note":"The back is not strictly smaller than 1, or the deque is empty, so nothing is removed and 1 is appended."},{"at":{"i":6},"vars":{"deque":"[7,6]","front":7},"note":"The value 6 removes 1, 3, 3 from the back, because they are strictly smaller. Then 6 is appended."}]}
```

```trace
{"cells":[5,3,8,2,2,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"deque":"[5]","front":5},"note":"The back is not strictly larger than 5, or the deque is empty, so nothing is removed and 5 is appended."},{"at":{"i":1},"vars":{"deque":"[3]","front":3},"note":"The value 3 removes 5 from the back, because they are strictly larger. Then 3 is appended."},{"at":{"i":2},"vars":{"deque":"[3,8]","front":3},"note":"The back is not strictly larger than 8, or the deque is empty, so nothing is removed and 8 is appended."},{"at":{"i":3},"vars":{"deque":"[2]","front":2},"note":"The value 2 removes 8, 3 from the back, because they are strictly larger. Then 2 is appended."},{"at":{"i":4},"vars":{"deque":"[2,2]","front":2},"note":"The back is not strictly larger than 2, or the deque is empty, so nothing is removed and 2 is appended."},{"at":{"i":5},"vars":{"deque":"[2,2,7]","front":2},"note":"The back is not strictly larger than 7, or the deque is empty, so nothing is removed and 7 is appended."}]}
```

<!-- stage: code -->
### A Shortlist With A Direction

```java
static java.util.ArrayDeque<Integer> shortlist(int[] values, boolean forMaximum) {
    java.util.ArrayDeque<Integer> d = new java.util.ArrayDeque<>();
    for (int v : values) {
        // the back admitter: drop every entry the newcomer strictly beats, then append
        while (!d.isEmpty() && (forMaximum ? d.peekLast() < v : d.peekLast() > v)) {
            d.removeLast();
        }
        d.addLast(v);
    }
    return d;                       // the front reader: d.peekFirst() is the best survivor
}
```

Every value enters the deque a single time and leaves it no more than a single time, so the time is O(n) and the memory is O(n) in the worst case, for example for scores that never beat one another. The comparison uses the unboxed values, since `d.peekLast() < v` unboxes automatically. A test for equality between two `Integer` objects with `==` compares references and not numbers, and it is only accidentally right for small values, so equality of boxed values should be written with `equals` or after unboxing.

<!-- stage: applicability -->
### When The Ends Have Different Jobs

Use a monotonic deque when the question is the extreme value of a moving collection, one end of the collection answers and the other end admits new items and prunes weaker ones. The invariant is the order rule plus the roles: the front is the best survivor, entries toward the back follow the stated order, and a value is only ever appended at the back. State the direction, the comparison and the equal policy before writing the loop.

The false friend is treating the two ends as interchangeable. A program that sometimes reads the back for the answer and sometimes admits at the front may pass small tests, because a deque of one or two entries looks the same from either end, and then fail on a longer input. A second false friend is a sorted list, which also keeps the best at one end but costs logarithmic or linear time to insert, while the deque only ever appends.

Do not use the shortlist when a removed entry might become useful again, which happens when the collection can lose its newest entries as well as its oldest, or when the query asks for something other than an extreme value, such as the median. A heap or a balanced structure is needed there. In Java, also remember that `ArrayDeque` rejects `null`, so the shortlist cannot hold a missing score without a marker.

<!-- stage: exercises -->
### Exercises

#### [Build] Decreasing Candidate Values (Author exercise)
<!-- id: dq-decreasing-candidate-values -->

**Prerequisites.** The previous lesson on `ArrayDeque` mechanics.

**Problem.** Process the integers of `stream` in order. Before appending a value at the back of a deque, remove from the back every value that is strictly smaller than it. Equal values are kept. Return the contents of the deque from front to back after the last value.

**Constraints.** 0 <= stream.length <= 10^5 and -10^9 <= stream[i] <= 10^9. Linear time.

**Example 1.** Input `stream = [4, 2, 7, 3, 3, 1, 6]`, output `[7, 6]`.

**Example 2.** Input `stream = [5, 5, 5]`, output `[5, 5, 5]`, since equal values are never removed.

**Hint.** Which end does the removal test look at, and when does the loop stop? What does the deque look like after every step if you never pop an equal value?

**Changed decision.** First rung: the back admits, and the values decrease from front to back, with the front as the best.

#### [Vary] Increasing Candidate Values (Author exercise)
<!-- id: dq-increasing-candidate-values -->

**Prerequisites.** The Decreasing Candidate Values exercise above.

**Problem.** Process the integers of `stream` in order. Before appending a value at the back of a deque, remove from the back every value that is strictly larger than it. Equal values are kept. Report the deque's contents, front to back, once the stream has ended.

**Constraints.** 0 <= stream.length <= 10^5 and -10^9 <= stream[i] <= 10^9. Linear time.

**Example 1.** Input `stream = [4, 2, 7, 3, 3, 1, 6]`, output `[1, 6]`.

**Example 2.** Input `stream = [9, 8, 7]`, output `[7]`, because each new value removes the one before it.

**Hint.** Which single comparison has to be reversed? Why is the front now the smallest value?

**Changed decision.** The comparison is reversed, so the deque supports minima and the values increase from front to back.

#### [Boundary] Equal Candidate Policy (Author exercise)
<!-- id: dq-equal-candidate-policy -->

**Prerequisites.** The two exercises above.

**Problem.** Process `stream` with a decreasing deque of indices under two policies. Under *keep equals* a newcomer removes only back entries with strictly smaller values. Under *replace equals* it removes back entries with smaller or equal values. Return an array of two lists: the indices in the deque from front to back at the end under keep equals, and then under replace equals.

**Constraints.** 1 <= stream.length <= 10^5 and -10^9 <= stream[i] <= 10^9.

**Example 1.** Input `stream = [2, 2, 1, 2]`, output `[[0, 1, 3], [3]]`.

**Example 2.** Input `stream = [5]`, output `[[0], [0]]`, since a single value is its own answer under both policies.

**Hint.** Why do both policies give the same front value at every step? What changes about which index sits at the front?

**Changed decision.** The comparison changes at equality only, and indices are stored so the effect on age can be seen.

#### [Recognize] Name Each End (Author exercise)
<!-- id: dq-name-each-end -->

**Prerequisites.** All three exercises above.

**Problem.** A sliding-window maximum with window length `k` has been run and its removals logged in order. Each log entry is a string `"<side> <index> <right>"`, where `side` is `F` for the front or `B` for the back, `index` is the removed index, and `right` is the window's right edge at that moment. Label each entry: `expired` if `index <= right - k`, which must happen at the front, `dominated` if `index > right - k`, which must happen at the back, and `invalid` if the side does not match the reason.

**Constraints.** 1 <= k <= 10^5 and 0 <= log.length <= 10^5, with 0 <= index <= right <= 10^9.

**Example 1.** Input `k = 3`, `log = ["B 0 1", "F 1 4", "B 3 4", "B 2 4"]`, output `["dominated", "expired", "dominated", "dominated"]`.

**Example 2.** Input `k = 3`, `log = ["F 2 3"]`, output `["invalid"]`, since index 2 is still inside the window when the right edge is 3.

**Hint.** Which comparison separates an old index from a recent one? Which end may a removal for each reason use?

**Changed decision.** Each removal is explained by its reason, expiration at the front or domination at the back, and a mismatch is a bug in the log.
