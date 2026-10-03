<!-- lesson-kind: standard -->
<!-- lesson-id: opposite-ends -->
## Opposite Ends

<!-- stage: context -->
### A Gift Card At A Craft Stall

At a village craft fair, a visitor holds a gift card worth exactly 50 coins, and she wants to hand it over in one go for two small presents. The stall keeps everything on a single long shelf, cheapest item at the left end and dearest at the right end, each with a little price tag. She needs two different items whose tags add up to exactly 50. The stall owner, who knows the stock well, promises that this evening there is exactly one such pair.

The shelf holds thousands of items, and she has no wish to spend the afternoon holding one item in each hand and adding tags in her head. She wonders whether the fact that the shelf is in price order can save her from trying every pairing.

<!-- stage: naive -->
### Try Every Pair Of Items

The direct plan is to take each item in turn and test it against every item that comes after it on the shelf, stopping when two tags hit the card value.

```java
static int[] pairByTrying(int[] tags, int card) {
    for (int a = 0; a < tags.length; a++) {
        for (int b = a + 1; b < tags.length; b++) {
            if (tags[a] + tags[b] == card) {
                return new int[] {a + 1, b + 1};   // shelf positions counted from 1
            }
        }
    }
    return new int[] {-1, -1};
}
```

It is correct on any shelf, sorted or not, and it never pairs an item with itself because the second index always starts after the first.

<!-- stage: bottleneck -->
### Every Pair Is Added Again

With n items there are about n * (n - 1) / 2 pairs, so the double loop does O(n^2) additions in the worst case. For ten thousand items that is around fifty million sums, to find one pair. The wasted effort is that each sum is looked at alone. When the visitor finds that a cheap item plus a middling item falls short of 50, that result says something about many other pairs too, but the loops ignore it and go on to test the same cheap item against the next item, and the next.

The sorted shelf is the missing piece of information. If the cheapest remaining item plus the dearest remaining item is already short of the card, then the cheapest item is short with every other remaining partner as well, since no partner is dearer than the dearest one. One comparison can therefore settle a whole row of pairs at once, and a method that exploits this does a constant amount of work per item removed, which is O(n) in total.

<!-- stage: insight -->
### One Sum Rules Out A Whole Row

Stand at both ends of the shelf, with `left` at the cheapest item and `right` at the dearest, and look at the sum of those two tags. The three outcomes each carry a proof. If the sum is smaller than the card, then `left` cannot belong to the answer inside the current range, because even its best possible partner, the item at `right`, leaves it short, and every other partner is no dearer. If the sum is larger, then `right` is too dear for every partner at or after `left`, and it can be dropped. If the sum is equal, the pair is found.

Each of the first two cases is an **elimination**: a single comparison discards one endpoint together with every pair that used it, and nothing that could still win is lost. The region that has not been discarded is the **live interval**, the positions from `left` to `right`, inclusive. It shrinks by exactly one position per step, so the loop ends after at most n - 1 steps with either the answer or `left == right`, which means no pair exists.

This is only valid because prices are ordered. The property that makes an elimination safe is that the sum is **monotone** in each endpoint: moving `left` up never makes the sum smaller, and moving `right` down never makes it larger. The invariant is that every valid pair not yet ruled out has both of its positions inside the live interval. It holds at the start because the interval is the whole shelf, each step keeps it true by discarding only positions that appear in no valid pair, and when the interval is down to one position, no pair of two different positions remains.

<!-- names: elimination, live interval, monotone -->

<!-- stage: variables -->
### Two Positions And Their Sum

`left` starts at 0 and `right` at `n - 1`, so the pair of positions is always two distinct places with `left < right`. The loop runs while `left < right`, and that condition is what stops an item from being paired with itself. `sum` is recomputed at each step from the two tags, and it must be a `long` when tags can be near the `int` limits, because adding two large `int` values wraps around to a negative number. For the closest-pair variant, `bestGap` holds the smallest distance to the target seen so far, and for the container problem, `best` holds the largest area seen so far.

<!-- stage: trace -->
### Narrowing From Both Shelf Ends

The first trace looks for 26 on a shelf of seven tags, with the pair present. The step to study is the second, where the sum 28 overshoots the card, so the dear end is dropped and `right` moves in, while a later step shows `left` moving because the sum is short. The pair is found when the tags are 11 and 15.

```trace
{"cells":[2,5,8,11,15,19,23],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":6},"vars":{"sum":25},"note":"Sum 25 is below 26, so tag 2 is short even with the dearest partner and left moves to 1."},{"at":{"left":1,"right":6},"vars":{"sum":28},"note":"Sum 28 is above 26, so tag 23 is too dear even with the cheapest partner and right moves to 5."},{"at":{"left":1,"right":5},"vars":{"sum":24},"note":"Sum 24 is below 26, so tag 5 is short even with the dearest partner and left moves to 2."},{"at":{"left":2,"right":5},"vars":{"sum":27},"note":"Sum 27 is above 26, so tag 19 is too dear even with the cheapest partner and right moves to 4."},{"at":{"left":2,"right":4},"vars":{"sum":23},"note":"Sum 23 is below 26, so tag 8 is short even with the dearest partner and left moves to 3."},{"at":{"left":3,"right":4},"vars":{"sum":26},"note":"Tags 11 and 15 add up to 26, which equals the card, so the pair is found."}]}
```

The second trace uses a different shelf of six tags with repeated prices, and a card of 20 that no pair can reach. The step to study is the last one, where `left` and `right` meet on the same position and the loop stops. The two copies of 9 are tried together before that, which shows that equal values need no special treatment.

```trace
{"cells":[3,3,4,9,9,14],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":5},"vars":{"sum":17},"note":"Sum 17 is below 20, so tag 3 is short even with the dearest partner and left moves to 1."},{"at":{"left":1,"right":5},"vars":{"sum":17},"note":"Sum 17 is below 20, so tag 3 is short even with the dearest partner and left moves to 2."},{"at":{"left":2,"right":5},"vars":{"sum":18},"note":"Sum 18 is below 20, so tag 4 is short even with the dearest partner and left moves to 3."},{"at":{"left":3,"right":5},"vars":{"sum":23},"note":"Sum 23 is above 20, so tag 14 is too dear even with the cheapest partner and right moves to 4."},{"at":{"left":3,"right":4},"vars":{"sum":18},"note":"Sum 18 is below 20, so tag 9 is short even with the dearest partner and left moves to 4."},{"at":{"left":4,"right":4},"vars":{"sum":18},"note":"The two pointers meet on one position, so the live interval holds no pair and the answer is none."}]}
```

<!-- stage: code -->
### Pair Scan And Closest Gap

```java
static int[] pairInSorted(int[] tags, long card) {
    int left = 0, right = tags.length - 1;
    while (left < right) {
        long sum = (long) tags[left] + tags[right];
        if (sum == card) return new int[] {left + 1, right + 1};
        if (sum < card) left++;          // left is short even with the dearest partner
        else right--;                    // right is too dear even with the cheapest partner
    }
    return new int[] {-1, -1};
}

static long closestGap(int[] tags, long card) {
    int left = 0, right = tags.length - 1;
    long bestGap = Long.MAX_VALUE;
    while (left < right) {
        long sum = (long) tags[left] + tags[right];
        bestGap = Math.min(bestGap, Math.abs(sum - card));
        if (sum == card) return 0;
        if (sum < card) left++; else right--;
    }
    return bestGap;
}
```

Every iteration moves one pointer and reads two tags, so the loops take linear time and constant extra memory, with no more than n - 1 iterations. The cast to `long` happens before the addition, since casting the finished `int` sum would be too late.

<!-- stage: applicability -->
### Recognizing The Two Ends Scan

Reach for this scan when the data is ordered, or has some other monotone quantity, and the question is about a pair of positions with a combined score that must hit, approach, or beat a target. A good sign is that you can say what a single comparison proves about an entire endpoint. State the invariant before writing the loop, namely that every pair still possible lies between the two pointers, and choose which pointer moves by asking which endpoint the comparison has just proven useless.

The false friend is the same two-pointer loop on data that is not in order. Without order, a short sum says nothing about the other partners of `left`, so moving an endpoint is a guess that can skip the answer. Sort a copy first if the original order must survive, and remember that the answer then names positions in the sorted copy. Another false friend is a problem that wants every pair, or a count of all pairs, where discarding an endpoint would discard answers you still need to report.

In Java, keep the loop condition as `left < right` so that an item is never paired with itself, and widen sums to `long`. When the task asks for original positions, decide the indexing base before coding, because the classic problem counts from 1 while arrays count from 0.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Sum II Input Array Is Sorted (LeetCode 167)
<!-- id: tp-two-sum-sorted -->

**Prerequisites.** The elimination argument in this lesson, and the contract that values arrive in nondecreasing order.

**Problem.** Given an array sorted in nondecreasing order and a target, return the 1-indexed positions of the two entries that add up to the target, smaller position first. Exactly one valid pair exists, and an entry may not be used twice.

**Constraints.** 2 <= numbers.length <= 30000, every value and the target fit in `int`, and the sorted-order promise holds. Use constant extra space and do not modify the array.

**Example 1.** Input `numbers = [2, 7, 11, 15], target = 18`, output `[2, 3]`.

**Example 2.** Input `numbers = [-3, 0, 4, 4, 9], target = 8`, output `[3, 4]`.

**Hint.** If the two ends add up to less than the target, which end can never be part of the answer? What does a sum that is too large rule out?

**Changed decision.** First rung: the pair of ends is compared with the target, and the comparison decides which end is discarded.

#### [Vary] Closest Pair Sum (Author exercise)
<!-- id: tp-closest-pair-sum -->

**Prerequisites.** The two-sum exercise above.

**Problem.** Given a sorted array and a target, return the smallest possible value of `|numbers[i] + numbers[j] - target|` over all pairs of different positions `i < j`. A pair that hits the target exactly gives 0.

**Constraints.** 2 <= numbers.length <= 100000, any `int` values, any `int` target, sorted nondecreasing. Sums can leave the `int` range, so compute in `long`.

**Example 1.** Input `numbers = [1, 4, 9, 16], target = 12`, output 1.

**Example 2.** Input `numbers = [-5, -1, 5], target = 0`, output 0.

**Hint.** The same discard rule still applies after a sum that misses the target. What do you need to remember before you discard an end?

**Changed decision.** There is no guarantee of an exact pair, so the scan keeps the best distance seen and runs until the pointers meet.

#### [Boundary] Two Values (Author exercise)
<!-- id: tp-two-values -->

**Prerequisites.** The two exercises above.

**Problem.** Given a sorted array and a target, report whether two different positions hold values summing to the target. Equal values at different positions count as a pair, one position never pairs with itself, and the answer may be no.

**Constraints.** 0 <= numbers.length <= 100000, any `int` values, and a `long` target. Sorted nondecreasing. The extremes `Integer.MAX_VALUE` and `Integer.MIN_VALUE` may appear.

**Example 1.** Input `numbers = [5, 5], target = 10`, output `true`.

**Example 2.** Input `numbers = [7], target = 14`, output `false`.

**Hint.** What does the loop condition do for an empty or one-element array? What goes wrong when two huge positive values are added as `int`?

**Changed decision.** Existence replaces the position pair, and the boundary cases are equal neighbours, a single value that must not pair with itself, and sums beyond the `int` range.

#### [Recognize] Container With Most Water (LeetCode 11)
<!-- id: tp-container-water -->

**Prerequisites.** All three exercises above.

**Problem.** Vertical walls stand at positions 0 to n - 1 with the given nonnegative heights. Choose two walls, and the water they hold is the distance between them times the shorter height. Return the largest amount of water.

**Constraints.** 2 <= height.length <= 100000 and 0 <= height[i] <= 1000000000. The array is not sorted, so the area must be returned as a `long`.

**Example 1.** Input `height = [3, 9, 2, 6, 4]`, output 12.

**Example 2.** Input `height = [5, 5, 5]`, output 10.

**Hint.** Compare the walls at the two ends. Which wall limits the area, and can any narrower pair that keeps it do better?

**Changed decision.** The data is not sorted, but a different monotone fact replaces order: for a fixed shorter wall, moving inward only reduces the width, so that wall is discarded.
