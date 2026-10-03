<!-- lesson-kind: standard -->
<!-- lesson-id: expired-front-eviction -->
## Expired-Front Eviction

<!-- stage: context -->
### A Wallet Of Coupons With Dates

A shopper keeps a small wallet of discount coupons. Each coupon has a percentage printed on it and the day it was handed out, and every coupon is valid for exactly three days, counting the day it was issued. At the till the cashier wants to apply the best coupon that is still valid today. The wallet is kept in the order in which coupons were received, so the oldest one is always on the top of the pile.

On some days the best coupon in the wallet turns out to be too old. It has the highest percentage, but its three days are over, and the cashier must put it aside and look at the next. Sometimes a whole stretch of the oldest coupons has gone stale at once, for example after a long weekend. The percentage printed on a coupon can say how good it is, but it can never say whether it is still valid, and only the issue date can.

<!-- stage: naive -->
### Check Every Coupon Each Day

The direct method looks at every coupon of the last three days afresh, and takes the best.

```java
static int[] bestValidCoupon(int[] percent, int days) {
    int[] best = new int[percent.length];
    for (int today = 0; today < percent.length; today++) {
        int top = Integer.MIN_VALUE;
        for (int issued = Math.max(0, today - days + 1); issued <= today; issued++) {
            top = Math.max(top, percent[issued]);
        }
        best[today] = top;
    }
    return best;
}
```

It is correct, and it treats age properly: for `[10, 30, 20, 5]` with `days = 2` it returns `[10, 30, 30, 20]`, since by day 3 the 30 issued on day 1 is no longer valid.

<!-- stage: bottleneck -->
### The Same Valid Coupons Are Reread

Each day the loop revisits all the valid coupons, so with `n` days and a validity of `d` days the cost is about `n * d`, which is O(n * d) and approaches O(n^2) when the validity is long. A year of daily coupons that stay valid for 200 days costs about 50,000 comparisons for the year, and a long ledger with a long validity is much worse.

The rereading ignores what the previous day already learned. Almost the same coupons were valid yesterday, with one coupon too old and one new, and the dominated ones had already been dismissed. A wallet that keeps only the coupons that can still be best, in order of issue, needs one thing more: a quick way to find out when its oldest coupon has gone stale, so that it can be put aside before the cashier reads the top of the pile.

<!-- stage: insight -->
### Put Aside The Stale Front

Candidates enter the deque at the back in order of index, so the front is always the oldest candidate. An **age test** compares the index at the front with the **legal left bound** of the current window. For a window of length `k` whose right edge is `right`, the legal indices are `right - k + 1` through `right`, so an index `<= right - k` is expired. The **front expiry** loop removes the front while its index is expired: `while (!deque.isEmpty() && deque.peekFirst() <= right - k) deque.removeFirst();`.

It is enough to test the front because indices increase from front to back. If the oldest candidate is legal, every candidate behind it is newer and legal as well, so the loop can stop at the first legal front. It has to be a loop and not an `if`, because the left bound can move by more than one index at a time, and a single arrival can leave several candidates stale.

<!-- names: age test, legal left bound, front expiry -->

The invariant, before the answer for the window ending at `right` is read, is that every stored index is greater than `right - k`. Value order cannot establish it. A value can be the largest in the deque and also be expired, and only the index can tell. Each index goes in a single time and comes out no more than a single time from the front, so the total cost of all expiry work is O(n).

<!-- stage: variables -->
### The Edge, The Bound, The Front

The right edge is the index of the newest value in the current window, `k` is its length, and `right - k` is the last index that has just become illegal. The front of the deque is the oldest candidate, compared against that last illegal index. The deque is read for the answer only after the expiry loop has finished, because before it the front might be stale. A variable bound, such as an array `left[right]` that records where the legal part begins, replaces `right - k + 1` and uses the same loop, with the test `deque.peekFirst() < left[right]`. If the window is empty, which is possible only when the bound can pass the right edge, the deque is empty after expiry and there is no answer.

<!-- stage: trace -->
### Candidates Aging Out

Take the values `4, 2, 12, 3, 8, 1` with windows of length 3, keeping the largest candidates. At right edge 2 the 12 arrives and removes the 2 and the 4 from the back, so the deque holds index 2. At right edge 3 the 3 is appended, and index 2 is still legal since `3 - 3 = 0` and 2 is greater than 0. At right edge 4 the 8 removes the 3 and the deque holds indices 2 and 4. At right edge 5 the age test finds that `5 - 3 = 2`, so index 2, which holds the largest value 12, is expired, and it is removed from the front. Then the 1 is appended, and the deque holds indices 4 and 5. The step to study is right edge 5, where the largest value is removed by age and not by a larger value.

For a variable bound take the legal left bounds `0, 0, 1, 3, 3, 5` over six right edges. At right edge 3 the bound jumps from 1 to 3, so two candidates, indices 1 and 2, expire together, which a single `if` would miss.

```trace
{"cells":[4,2,12,3,8,1],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","expired":0,"dominated":0},"note":"Right edge 0 brings the value 4. The deque is empty, so nothing can be stale. Nothing is removed from the back. Index 0 is appended."},{"at":{"right":1},"vars":{"deque":"[0,1]","expired":0,"dominated":0},"note":"Right edge 1 brings the value 2. The age test finds nothing stale, since the front is above -2. Nothing is removed from the back. Index 1 is appended."},{"at":{"right":2},"vars":{"deque":"[2]","expired":0,"dominated":2},"note":"Right edge 2 brings the value 12. The deque is empty, so nothing can be stale. The value 12 removes index 1, 0 from the back. Index 2 is appended."},{"at":{"right":3},"vars":{"deque":"[2,3]","expired":0,"dominated":0},"note":"Right edge 3 brings the value 3. The age test finds nothing stale, since the front is above 0. Nothing is removed from the back. Index 3 is appended."},{"at":{"right":4},"vars":{"deque":"[2,4]","expired":0,"dominated":1},"note":"Right edge 4 brings the value 8. The age test finds nothing stale, since the front is above 1. The value 8 removes index 3 from the back. Index 4 is appended."},{"at":{"right":5},"vars":{"deque":"[4,5]","expired":1,"dominated":0},"note":"Right edge 5 brings the value 1. The age test removes index 2 from the front, since 5 - 3 = 2 and the index is at most that. Nothing is removed from the back. Index 5 is appended."}]}
```

```trace
{"cells":[0,1,2,3,4,5],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","bound":0,"expired":0},"note":"Right edge 0 appends index 0. The legal left bound is 0, and the front is already legal."},{"at":{"right":1},"vars":{"deque":"[0,1]","bound":0,"expired":0},"note":"Right edge 1 appends index 1. The legal left bound is 0, and the front is already legal."},{"at":{"right":2},"vars":{"deque":"[1,2]","bound":1,"expired":1},"note":"Right edge 2 appends index 2. The legal left bound is 1, so index 0 expire from the front."},{"at":{"right":3},"vars":{"deque":"[3]","bound":3,"expired":2},"note":"Right edge 3 appends index 3. The legal left bound is 3, so index 1, 2 expire from the front."},{"at":{"right":4},"vars":{"deque":"[3,4]","bound":3,"expired":0},"note":"Right edge 4 appends index 4. The legal left bound is 3, and the front is already legal."},{"at":{"right":5},"vars":{"deque":"[5]","bound":5,"expired":2},"note":"Right edge 5 appends index 5. The legal left bound is 5, so index 3, 4 expire from the front."}]}
```

<!-- stage: code -->
### The Expiry Loop

```java
static void expire(java.util.ArrayDeque<Integer> deque, int right, int k) {
    while (!deque.isEmpty() && deque.peekFirst() <= right - k) {
        deque.removeFirst();                      // the oldest candidate has left the window
    }
}

static void expireBelow(java.util.ArrayDeque<Integer> deque, int legalLeft) {
    while (!deque.isEmpty() && deque.peekFirst() < legalLeft) {
        deque.removeFirst();                      // a supplied bound may jump past several indices
    }
}
```

Each expiry removes a distinct index from the front, so over a whole run the removals add up to at most `n`, giving O(n) total work, and the extra memory is O(1). The two methods express the same rule. The first uses the last illegal index `right - k` with `<=`, and the second uses the first legal index with `<`, and mixing the two tests, for instance `<` with `right - k`, leaves one stale index in a window of length `k`.

<!-- stage: applicability -->
### When Stale Candidates Linger

Use front expiry when each candidate has a position or timestamp and the question is about the candidates in a moving range. The invariant is that before any answer is read, every stored index lies in the legal range, and the front is the oldest stored index, so the age test only ever looks at the front. Write the boundary as an explicit inequality, `index <= right - k` for expiry, and check it on a window of length 1 and a window equal to the whole array.

The false friend is value order. The front of a monotonic deque is the best value among the survivors, and that is a different thing from being the best valid value, so reading the answer before expiry returns a stale maximum. A second false friend is using `if` in place of `while`, which works when the bound moves one step per arrival and fails when it jumps. A third is removing expired entries from the back, which would be right only if entries were stored in reverse order.

Do not use front expiry when entries can leave in an order other than age, for instance when a coupon can be redeemed and discarded from the middle. Expiry also needs candidates stored in index order, which holds when each new index is only appended at the back. Remember that expiry uses indices, so storing values alone would make equal values from different days impossible to tell apart.

<!-- stage: exercises -->
### Exercises

#### [Build] Expire One Window (Author exercise)
<!-- id: dq-expire-one-window -->

**Prerequisites.** The previous three lessons of this chapter.

**Problem.** Indices `0, 1, ..., n - 1` arrive one at a time and are appended to the back of a deque, with nothing ever removed by value. The window has length `k`. After each arrival at right edge `r`, remove the front index if it is at most `r - k`, using an `if`, since at most one index can expire per arrival. Return the front index after each step.

**Constraints.** 1 <= n <= 10^5 and 1 <= k <= 10^5.

**Example 1.** Input `n = 6`, `k = 3`, output `[0, 0, 0, 1, 2, 3]`.

**Example 2.** Input `n = 2`, `k = 5`, output `[0, 0]`, since nothing is old enough to expire.

**Hint.** Which index has just become illegal at right edge `r`? Why is one removal per step enough here and not in general?

**Changed decision.** First rung: the front is tested against the last illegal index and removed once per arrival.

#### [Vary] Jumping Boundary (Author exercise)
<!-- id: dq-jumping-boundary -->

**Prerequisites.** The Expire One Window exercise above.

**Problem.** Indices `0, 1, ..., n - 1` arrive one at a time and are appended to a deque, with nothing removed by value. An array `legalLeft` of length `n` is non-decreasing, with `legalLeft[r] <= r`. After the arrival at right edge `r`, remove from the front every index smaller than `legalLeft[r]`. Return, for each `r`, the number of indices removed at that step.

**Constraints.** 1 <= n <= 10^5 and 0 <= legalLeft[r] <= r with `legalLeft` non-decreasing.

**Example 1.** Input `legalLeft = [0, 0, 1, 3, 3, 5]`, output `[0, 0, 1, 2, 0, 2]`.

**Example 2.** Input `legalLeft = [0, 1, 2, 3]`, output `[0, 1, 1, 1]`, so a bound that moves one step at a time removes one index per step.

**Hint.** Why is a loop needed here when an `if` was enough in the first rung? What stops the loop?

**Changed decision.** The boundary comes from an array and may jump, so the expiry becomes a loop that continues while the front is illegal.

#### [Boundary] Exact Expiry Point (Author exercise)
<!-- id: dq-exact-expiry-point -->

**Prerequisites.** The two exercises above.

**Problem.** Indices `0, 1, ..., n - 1` arrive and are appended to a deque. The window has length `k`. After each arrival at right edge `r`, remove from the front every index that is at most `r - k`. Return the size of the deque after each step, which must equal the number of indices actually inside the window.

**Constraints.** 1 <= n <= 10^5 and 1 <= k <= 10^5.

**Example 1.** Input `n = 5`, `k = 3`, output `[1, 2, 3, 3, 3]`.

**Example 2.** Input `n = 4`, `k = 1`, output `[1, 1, 1, 1]`, because with a window of length one every earlier index expires.

**Hint.** Which comparison, `<` or `<=`, against `r - k` leaves exactly `k` indices? What does the wrong one return for `k = 1`?

**Changed decision.** The comparison is the whole point: `<=` against `right - k` means the index exactly `k` steps back is already outside the window.

#### [Recognize] Chronological Candidate Queue (Author exercise)
<!-- id: dq-chronological-candidate-queue -->

**Prerequisites.** All three exercises above, and the dominated-back lesson.

**Problem.** Process the array `a` with windows of length `k`. At each right edge, first expire stale indices from the front, then remove from the back every index whose value is strictly smaller than the new value, then append the new index. Return the indices left in the deque after the last step, front to back.

**Constraints.** 1 <= a.length <= 10^5, 1 <= k <= a.length and -10^9 <= a[i] <= 10^9.

**Example 1.** Input `a = [4, 2, 12, 3, 8, 1]`, `k = 3`, output `[4, 5]`.

**Example 2.** Input `a = [5, 4, 3, 2, 1]`, `k = 2`, output `[3, 4]`.

**Hint.** The indices in the deque should always be increasing and the values non-increasing. Which of the two orders does expiry rely on, and which one does the answer rely on?

**Changed decision.** Expiry and domination are combined for the first time, so each arrival makes three ordered moves: expire at the front, dominate at the back, then append.
