<!-- lesson-kind: combination -->
<!-- lesson-id: sorting-and-two-pointers -->
## Sorting And Two Pointers

<!-- stage: context -->
### Prize Tokens At The School Fair

At a school fair, one stall hands out a prize to any child who can pull two tokens out of a big basket whose points add up to exactly the number painted on the stall's sign. Each token has a number of points stamped on it, and the tokens were tipped into the basket in whatever order the helpers emptied their pockets. The basket has numbered slots, and the helper who checks the answer wants to know which two slots the winning tokens came from, not just their points. Children are not allowed to rearrange the basket, because the slot numbers must stay the same for the next child.

A patient child can pick up one token, then try it against every other token in the basket, then move to the next. With sixty tokens that is a long afternoon, and when the sign changes to a three-token prize, or to the three tokens that come closest to the sign without reaching it, the same child is nearly in tears. The helpers keep saying that laying the tokens out in a row by points would make it all easier, but nobody can say exactly why.

<!-- stage: contributions -->
### What Each Part Brings

Sorting brings an order that turns a sum into something with a direction. In a row of tokens laid out from the smallest points to the largest, swapping a token for its right-hand neighbour can only raise a sum or leave it the same, and swapping for its left-hand neighbour can only lower it or leave it the same. In a jumbled basket no such statement is true, so a sum that is too big or too small says nothing about which token to change. Sorting alone, however, still leaves a child with all the pairs to try, because a sorted row does not tell the child where in the row a partner is hiding.

Two pointers bring a way to discard candidates in bulk. One pointer stands on the lowest token and one on the highest, and each look at their sum rules out a whole token for good rather than a single pair. The pointers alone are useless on a jumbled basket, because they have a safe-move proof only when moving an end changes the sum in a known direction. Each part supplies what the other one lacks: the order gives meaning to a sum being too big or too small, and the pointers spend that meaning to throw away candidates quickly.

The recognition cue is a question about sums of two or more items that may be rearranged freely for the purposes of the search: an exact target, a count of distinct combinations, or the closest value to a target. The cost of sorting is paid once up front.

<!-- stage: naive -->
### Try Every Pair In The Basket

The direct approach keeps the basket as it is and tries each token against all the tokens that come after it, reporting the two slot numbers when the points add up to the sign.

```java
static int[] pairBySearching(int[] basket, int sign) {
    for (int a = 0; a < basket.length; a++) {
        for (int b = a + 1; b < basket.length; b++) {
            if (basket[a] + basket[b] == sign) return new int[] {a, b};
        }
    }
    return new int[] {-1, -1};
}
```

It never changes the basket, it reports real slot numbers, and it answers minus one twice when no two tokens fit, so it is correct for every basket.

<!-- stage: bottleneck -->
### Every Pair Is Judged On Its Own

A basket of n tokens has n(n - 1)/2 pairs, so the loops read O(n^2) sums in the worst case, which is when no pair fits and every pair is tried. Three tokens at once make the search O(n^3), and four make it O(n^4). The cost comes from judging each pair as if nothing were known about the others. When token 40 plus token 3 is far too big, the loops still go on to try token 40 against every remaining token, although a reader can tell at once that many of those are bound to be too big as well.

That knowledge is only available when the tokens are in order of points. Once they are, a sum that is too big shows that the largest token of the pair cannot work with anything at or below the other one, so the largest token can be set aside for good, and a sum that is too small does the same for the smallest. Sorting the tokens costs O(n log n), and each set-aside costs one step, so a pair search becomes O(n log n) in total. For three tokens, one token is held fixed while a pair search runs on the rest, which gives O(n^2), and for four tokens O(n^3).

<!-- stage: insight -->
### Order First, Then Eliminate From Both Ends

Because the basket must not be rearranged, the order is made on the side. An **index order** is an array of slot numbers arranged so that reading the basket through it gives the points in increasing order. The basket itself is untouched, and every answer is translated back to real slot numbers by reading the index order. When only values matter, as in counting combinations, a plain sorted copy of the values does the same job.

On the ordered row, the two pointers stand on the first and the last position. **Pair elimination** is the rule that each sum removes one end for good. If the sum is greater than the target, then the right pointer's token is too big for every partner in the window, since any partner is at least as large as the left pointer's token, and the right pointer moves in. If the sum is less than the target, the left pointer's token is too small for every partner in the window, since any partner is at most as large as the right pointer's token, and the left pointer moves in. An equal sum is an answer.

The invariant is that every valid pair of the whole row lies inside the window between the pointers, inclusive. It holds at the start because the window is the whole row, and each move discards a position that belongs to no valid pair in the window. When the pointers meet, no pair is left, so the answer is that there is none.

For three or more tokens, a **fixed anchor** is a token held still while the rest is searched. The target for the remaining pair becomes the original target minus the anchor, and only the positions after the anchor are searched, so each set of tokens is considered once in position order. When distinct combinations are requested, duplicates are skipped before a pointer moves: an anchor equal to the previous anchor is skipped, and after a hit both pointers step past every copy of their values, so the same combination of values is never counted twice.

<!-- names: index order, pair elimination, fixed anchor -->

<!-- stage: variables -->
### Window Ends, Anchor And Running Sum

`lo` and `hi` are the two ends of the window, in positions of the ordered row, and `lo < hi` is the loop condition so a token is never paired with itself. `sum` is computed fresh from the two values at each step, as a `long` whenever the values or the target may be near the limits of `int`, because two large ints can overflow before the comparison is made. `anchor` is the position of the fixed token for three or four tokens, and it only moves forward. `order` is the index order for the pair problem, holding slot numbers, and `best` is the closest sum found so far for the closest-sum variant, replaced only when a new sum is strictly closer or equally close and smaller. A `moves` counter is added where a test needs to show that the number of pointer moves stays quadratic.

<!-- stage: trace -->
### Two Searches On Ordered Rows

The first trace answers the pair question for a basket holding 8, 3, 11, 5, 2, 9 in slots 0 to 5, with a sign of 17. The cells are the points after ordering, so the row reads 2, 3, 5, 8, 9, 11, and each note also names the original slot of the two tokens in play. The step to study is the fourth: 8 plus 11 is 19, which is too big, so the 11 can pair with nothing at or below the 8, and the right pointer moves in. The last step finds 8 and 9, which sat in slots 0 and 5.

```trace
{"cells":[2,3,5,8,9,11],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":5},"vars":{"sum":13,"slots":"4 and 2"},"note":"2 plus 11 is 13, too small, so 2 fits no partner in the window and lo becomes 1."},{"at":{"lo":1,"hi":5},"vars":{"sum":14,"slots":"1 and 2"},"note":"3 plus 11 is 14, too small, so 3 fits no partner in the window and lo becomes 2."},{"at":{"lo":2,"hi":5},"vars":{"sum":16,"slots":"3 and 2"},"note":"5 plus 11 is 16, too small, so 5 fits no partner in the window and lo becomes 3."},{"at":{"lo":3,"hi":5},"vars":{"sum":19,"slots":"0 and 2"},"note":"8 plus 11 is 19, too big, so 11 fits no partner in the window and hi becomes 4."},{"at":{"lo":3,"hi":4},"vars":{"sum":17,"slots":"0 and 5"},"note":"8 plus 9 is 17, which equals 17. The tokens came from slots 0 and 5."}]}
```

The second trace counts distinct zero-sum triples in the row -2, -2, 0, 1, 1, 2, where an inactive pointer shows as minus one. The first anchor finds two different triples, and the step to study is the third, the second hit, where both pointers cross copies of their values and the window closes at position 4. The next anchor is a copy of the first, so the row skips it without searching, and the counter at the end is 2, showing the duplicate skipping working before any pointer moved.

```trace
{"cells":[-2,-2,0,1,1,2],"pointers":["i","lo","hi"],"steps":[{"at":{"i":0,"lo":1,"hi":5},"vars":{"sum":-2,"count":0},"note":"Sum -2 is below zero, so lo becomes 2."},{"at":{"i":0,"lo":2,"hi":5},"vars":{"sum":0,"count":1},"note":"Sum 0: -2, 0, 2 is counted. Both pointers then step past copies of their values, so lo becomes 3 and hi becomes 4."},{"at":{"i":0,"lo":3,"hi":4},"vars":{"sum":0,"count":2},"note":"Sum 0: -2, 1, 1 is counted. Both pointers then step past copies of their values, so lo becomes 4 and hi becomes 4."},{"at":{"i":1,"lo":-1,"hi":-1},"vars":{"count":2},"note":"Anchor -2 at position 1 equals the previous anchor, so it is skipped before any pointer moves."},{"at":{"i":2,"lo":3,"hi":5},"vars":{"sum":3,"count":2},"note":"Sum 3 is above zero, so hi becomes 4."},{"at":{"i":2,"lo":3,"hi":4},"vars":{"sum":2,"count":2},"note":"Sum 2 is above zero, so hi becomes 3."}]}
```

<!-- stage: code -->
### Index Order, Triple Count And Closest Sum

```java
static int[] pairByOriginalIndex(int[] nums, int target) {
    Integer[] order = new Integer[nums.length];
    for (int k = 0; k < order.length; k++) order[k] = k;
    Arrays.sort(order, (x, y) -> Integer.compare(nums[x], nums[y]));   // nums stays as given
    int lo = 0, hi = order.length - 1;
    while (lo < hi) {
        long sum = (long) nums[order[lo]] + nums[order[hi]];
        if (sum == target) {
            int p = order[lo], q = order[hi];
            return new int[] {Math.min(p, q), Math.max(p, q)};
        }
        if (sum < target) lo++; else hi--;
    }
    return new int[] {-1, -1};
}

static int countZeroTriples(int[] nums) {
    int[] a = nums.clone();
    Arrays.sort(a);
    int count = 0;
    for (int anchor = 0; anchor + 2 < a.length && a[anchor] <= 0; anchor++) {
        if (anchor > 0 && a[anchor] == a[anchor - 1]) continue;
        int lo = anchor + 1, hi = a.length - 1;
        while (lo < hi) {
            long sum = (long) a[anchor] + a[lo] + a[hi];
            if (sum < 0) lo++;
            else if (sum > 0) hi--;
            else {
                count++;
                int left = a[lo], right = a[hi];
                while (lo < hi && a[lo] == left) lo++;
                while (lo < hi && a[hi] == right) hi--;
            }
        }
    }
    return count;
}

static long closestSum(int[] nums, long target) {
    int[] a = nums.clone();
    Arrays.sort(a);
    long best = (long) a[0] + a[1] + a[2];
    for (int anchor = 0; anchor + 2 < a.length; anchor++) {
        int lo = anchor + 1, hi = a.length - 1;
        while (lo < hi) {
            long sum = (long) a[anchor] + a[lo] + a[hi];
            long gap = Math.abs(sum - target), bestGap = Math.abs(best - target);
            if (gap < bestGap || (gap == bestGap && sum < best)) best = sum;
            if (sum < target) lo++; else hi--;
        }
    }
    return best;
}
```

Sorting is O(n log n), the pair search is O(n) afterwards, so the pair method is O(n log n) with O(n) extra memory for the index order, while the triple methods are O(n^2) overall with O(n) for the copy. The pair method sorts boxed `Integer` slot numbers because a comparator needs objects, which is the price of leaving `nums` alone. The anchor loop in the count stops at the first positive anchor, since three positive values cannot sum to zero.

<!-- stage: applicability -->
### Reading A Sum Question Before Coding

Reach for this pair of tools when the question is about a sum of two or more items, the items may be arranged for the search, and the answer is an exact hit, a count of distinct combinations, or the nearest value. Before writing code, settle three contract points: whether the original positions are needed, which means an index order and not a sort in place, whether the input may be changed, and whether duplicates count once or many times. Then state the invariant aloud: every candidate not yet ruled out lies inside the window.

The nearest false friend is the pointers without the sort. On a jumbled row, a sum that is too big does not justify moving the right end, since a smaller partner may sit anywhere, so the loop returns wrong answers that look plausible. A second false friend is sorting and then still testing all the pairs, which is correct but keeps O(n^2). A third is a hash lookup for the complement, which is a fine answer for the pair, but does not extend to distinct triples without extra duplicate bookkeeping, and cannot answer the closest-sum question at all.

In Java, sorting an `int[]` mutates it, so copy first when the contract promises an unchanged input, and use `Integer[]` with a comparator when original positions matter. Compare with `Integer.compare` instead of subtracting, and widen to `long` before adding.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Sum II (LeetCode 167)
<!-- id: tp-pair-original-indices -->

**Prerequisites.** Opposite-end pointers on a sorted row from the first lesson of this chapter, and sorting a boxed index array with a comparator.

**Problem.** The numbers are NOT in sorted order this time. Given `nums` and a `target`, return the zero-based positions `{p, q}` with `p < q` of two different entries whose values add up to the target, or `{-1, -1}` if no such pair exists. Sort an index order, not the array: `nums` must be unchanged on return.

**Constraints.** 0 <= nums.length <= 50000, values and target are any `int`, and sums must be computed without overflow. If several pairs fit, any one of them is accepted.

**Example 1.** Input `nums = [8, 3, 11, 5, 2, 9], target = 17`, output `[0, 5]`.

**Example 2.** Input `nums = [4, 4, 9], target = 8`, output `[0, 1]`.

**Hint.** What must the index order be sorted by? After the pointers meet on a hit, which array do you read to produce the answer?

**Changed decision.** The classic version promises a sorted array with a one-based answer; here the data is jumbled, positions must be the original ones, and the array may not be touched.

#### [Vary] 3Sum (LeetCode 15)
<!-- id: tp-count-zero-triplets -->

**Prerequisites.** The Build exercise above, and skipping equal values before moving a pointer.

**Problem.** Given `nums`, return the number of distinct value triplets, each from three different positions, that add up to zero. Two triplets are the same if they hold the same values. Do not return the triplets themselves, and do not change `nums`. Also record how many times a pointer moves, and show that it never exceeds `n * n`.

**Constraints.** 0 <= nums.length <= 3000 and values in the range -100000 to 100000.

**Example 1.** Input `nums = [-2, 0, 1, 1, 2, -2]`, output 2.

**Example 2.** Input `nums = [0, 0, 0, 0]`, output 1.

**Hint.** What is the order of the two skipping loops after a hit, and what stops the first one from running past the second pointer?

**Changed decision.** The answer is a count of distinct value triplets over an unsorted input that must survive intact, so the sort is done on a copy and duplicates are skipped without ever building the list.

#### [Boundary] 3Sum Closest (LeetCode 16)
<!-- id: tp-closest-sum-tie-smaller -->

**Prerequisites.** The 3Sum exercise above.

**Problem.** Given `nums` with at least three entries and a `target`, return the sum of three different entries that is closest to the target. When two sums are equally close, return the smaller sum. A row of exactly three entries has only one candidate, and the answer may exceed the range of `int`, so return a `long`.

**Constraints.** 3 <= nums.length <= 1000, values are any `int`, and the target is any `long` within plus or minus 10000000000.

**Example 1.** Input `nums = [2000000000, 2000000000, 2000000000], target = 0`, output 6000000000.

**Example 2.** Input `nums = [1, 2, 4, 8], target = 9`, output 7.

**Hint.** Where do you store the best sum, and what must be compared on equal gaps? Which type does the gap itself need?

**Changed decision.** No exact hit exists in general, so the loop must keep a best-so-far through every step instead of returning at equality, and the tie rule is part of the contract.

#### [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-quads-pruned -->

**Prerequisites.** The three exercises above.

**Problem.** Return every distinct quadruplet of values, as sorted lists in lexicographic order, whose four entries come from different positions and add up to `target`. Use two fixed anchors and one pointer pair, add the cheap tests on the smallest and largest possible sums so whole branches are skipped, and make sure the pruned result equals the unpruned one. The input must not be modified.

**Constraints.** 0 <= nums.length <= 200, values and target are `int`, and the sums need `long`.

**Example 1.** Input `nums = [3, 0, 1, 2, 1, 2, 0], target = 6`, output `[[0, 1, 2, 3], [1, 1, 2, 2]]`.
**Example 2.** Input `nums = [1000000000, 1000000000, 1000000000, 1000000000], target = -294967296`, output `[]`.

**Hint.** What is the smallest sum an anchor can still reach, and what does it say about every later anchor when it is already too big?

**Changed decision.** A second fixed anchor and cheap bounds are added, so the duplicate policy must hold at every depth, and pruning may only discard branches that cannot hold a hit.
