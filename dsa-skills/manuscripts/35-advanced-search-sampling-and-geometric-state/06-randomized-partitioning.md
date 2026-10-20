<!-- lesson-kind: standard -->
<!-- lesson-id: randomized-partitioning -->
## Randomized Partitioning

<!-- stage: context -->
### The Median Query That Got Slow

A monitoring job reports the 95th percentile of response times for each hour. It copies the hour's measurements into an array and selects the right value with quickselect, which avoids sorting the whole array. The job runs in milliseconds on live data. One night an engineer replays the logs after a backup step that stores them sorted by value, and the same job takes minutes on the same number of values. The code did not change, only the order of the input.

A method whose speed depends on how the input is ordered is risky, because an attacker or an unlucky export can choose the order. This lesson asks how to select the k-th smallest value so that no input order can make the method slow, while the answer stays exactly correct.

<!-- stage: naive -->
### Always Split On The Last Element

Quickselect finds the k-th smallest value without sorting everything. It picks one value as the pivot, rearranges the array so that smaller values sit before the pivot and larger or equal values after it, and then continues in the one side that contains the wanted position. The direct version always takes the last element of the active range as its pivot.

```java
final class LastPivotSelect {
    static int kthSmallest(int[] a, int k) {
        int lo = 0, hi = a.length - 1, target = k - 1;       // 0-based rank
        while (true) {
            int pv = a[hi], store = lo;                      // the last element is the pivot
            for (int j = lo; j < hi; j++)
                if (a[j] < pv) { int t = a[store]; a[store] = a[j]; a[j] = t; store++; }
            int t = a[store]; a[store] = a[hi]; a[hi] = t;   // the pivot lands at its final index
            if (store == target) return a[store];
            if (target < store) hi = store - 1; else lo = store + 1;
        }
    }
}
```

On shuffled data the method is fast, and tests with random arrays pass. The sorted replay is a different story.

```predict
The array is 1 2 3 4 5 6 7 8, already sorted, and the call asks for the smallest value (k = 1). How many element comparisons `a[j] < pv` does the method make in total? How many would it make for 100000 sorted values?

The pivot is always the largest value of the active range, so every round compares the other elements to it, leaves them all on the left, and removes only the pivot. The rounds compare 7, 6, 5, 4, 3, 2 and 1 elements, which is 28 comparisons for 8 values. For n values the total is n(n - 1) / 2. For 100000 values that is about 5 * 10^9 comparisons, which takes many seconds or minutes.
```

<!-- stage: bottleneck -->
### One Bad Pivot Removes One Value

#### Cost Depends On The Pivot

The method costs O(n) time per round and the number of rounds depends on the pivot. A pivot that splits the range into two nearly equal parts cuts the work in half each round, so the total is about `n + n/2 + n/4 + ...`, which is O(n). A pivot that is the largest or smallest value removes one element per round, so the total is `n + (n - 1) + ...`, which is O(n^2). The worst case needs O(n^2) time and O(1) space.

#### Fixed Rules Can Be Defeated

The pivot rule decides which case occurs, and a fixed rule can be defeated. The last element is the maximum on a sorted ascending array. The first element fails on a sorted descending array. A middle element fails on a specially built array that places extreme values at the middle of every active range. Any rule that reads positions in a fixed way has some input that makes every split unbalanced.

#### Equal Values Break The Split

A second weakness hides in the partition itself. When many values are equal, the test `a[j] < pv` leaves all of the equal values on one side. An array of 10^5 equal values gives the same removal of one element per round, even with a good pivot. The repair has to handle both the choice of the pivot and the equal values.

<!-- stage: insight -->
### Choose The Pivot By Chance

<!-- names: random pivot, three-way partition, expected time -->

#### A Random Pivot Defeats Any Order

A **random pivot** is a position drawn uniformly from the active range `[lo, hi]`, endpoints included. The draw uses `pick.applyAsInt(hi - lo + 1)` and adds `lo`. The input order no longer matters, because the choice does not look at positions in a fixed way. Call a pivot good when its rank lies in the middle half of the active range. A uniform draw is good with probability one half, whatever the input is. A good pivot leaves at most three quarters of the range for the next round. The expected number of rounds until a good pivot appears is 2, so the work shrinks by a constant factor every two rounds on average.

#### Expected Time

The **expected time** is the average over the random draws, with the input fixed. A round on a range of length `m` costs O(m). With a good pivot every other round on average, the expected total is at most a geometric sum with ratio 3/4 and a constant factor, which is O(n). A bad run is possible, but its probability falls quickly. The worst case stays O(n^2), and the guarantee is about the average over draws, never about a single run.

#### Equal Values Need Three Regions

A **three-way partition** splits the active range into three parts: values below the pivot value, values equal to it, and values above it. Three indices keep the boundaries: `lt` for the first equal position, `gt` for the last equal position, and `i` for the next position to examine. If the wanted rank lies in the equal band, the pivot value is the answer, and the method returns without further work. Otherwise the method keeps only the below part or the above part, which excludes the whole equal band. An array of equal values then finishes in one round.

The invariant is that the wanted rank always lies inside the active range, and every value outside the active range is correctly placed relative to it.

<!-- stage: variables -->
### Range, Pivot And Three Bands

The loop keeps nine names.

- **lo** and **hi** are the ends of the active range, inclusive. Both change only when a side is dropped.
- **target** is the 0-based rank of the wanted value in sorted order. It equals `k - 1` for the k-th smallest.
- **p** is the pivot position, drawn as `lo + pick.applyAsInt(hi - lo + 1)`.
- **pv** is the pivot value `a[p]`, read before any swap.
- **lt** is the first position of the equal band. Positions `lo` to `lt - 1` hold values below `pv`.
- **gt** is the last position of the equal band. Positions `gt + 1` to `hi` hold values above `pv`.
- **i** is the next position to examine. Positions `lt` to `i - 1` hold values equal to `pv`.
- **rounds** counts the loop passes, which a test can read.

The scan ends when `i` passes `gt`. At that moment the three bands cover the whole active range.

<!-- stage: trace -->
### Tracing Two Selections

#### A Selection With Two Rounds

The first trace selects the 4th smallest value (rank 3) of `9 4 7 4 1 8`. The pointers `lo` and `hi` mark the active range and `p` marks the pivot. The first draw returns offset 0, so the pivot is 9, the largest value. Everything else is smaller, so the band of values below 9 covers positions 0 to 4 and the band above 9 is empty. The rank 3 is below the equal band at position 5, so the range shrinks to positions 0 to 4. The second draw returns offset 1, so the pivot is 7, the value at position 1 of the rearranged range `4 7 4 1 8`. The partition puts three values below 7, one value equal to 7 and one value above. The equal band covers position 3 only, and the rank 3 lies inside it. The method returns 7 after two rounds.

```trace
{"cells":[9,4,7,4,1,8],"pointers":["lo","hi","p"],"steps":[{"at":{"lo":0,"hi":5,"p":-1},"vars":{"target":3,"array":"9 4 7 4 1 8"},"note":"Start: the active range is the whole array and the wanted rank is 3."},{"at":{"lo":0,"hi":5,"p":0},"vars":{"draw":0,"pivot":9,"array":"4 7 4 1 8 9"},"note":"Draw offset 0 picks position 0 with pivot value 9. The pivot value is read before any swap."},{"at":{"lo":0,"hi":5,"p":0},"vars":{"lt":5,"gt":5,"array":"4 7 4 1 8 9"},"note":"The three-way scan ends. The equal band covers positions 5 to 5. The rank 3 is below the equal band, so the range becomes 0 to 4."},{"at":{"lo":0,"hi":4,"p":1},"vars":{"draw":1,"pivot":7,"array":"4 4 1 7 8 9"},"note":"Draw offset 1 picks position 1 with pivot value 7. The pivot value is read before any swap."},{"at":{"lo":0,"hi":4,"p":1},"vars":{"lt":3,"gt":3,"array":"4 4 1 7 8 9"},"note":"The three-way scan ends. The equal band covers positions 3 to 3. The rank 3 is inside the equal band, so the method returns 7."}]}
```

#### Many Equal Values

The second trace selects rank 3 of `5 5 5 2 5 9 5`. The draw returns offset 2, so the pivot value is 5. The three-way partition puts the value 2 below, five copies of 5 in the middle, and the value 9 above. The equal band covers positions 1 to 5. The rank 3 lies inside it, so the method returns 5 after one round, without looking at the other values again. A two-way partition would have kept the five copies together on one side and needed more rounds.

```trace
{"cells":[5,5,5,2,5,9,5],"pointers":["lo","hi","p"],"steps":[{"at":{"lo":0,"hi":6,"p":-1},"vars":{"target":3,"array":"5 5 5 2 5 9 5"},"note":"Start: the active range is the whole array and the wanted rank is 3."},{"at":{"lo":0,"hi":6,"p":2},"vars":{"draw":2,"pivot":5,"array":"2 5 5 5 5 5 9"},"note":"Draw offset 2 picks position 2 with pivot value 5. The pivot value is read before any swap."},{"at":{"lo":0,"hi":6,"p":2},"vars":{"lt":1,"gt":5,"array":"2 5 5 5 5 5 9"},"note":"The three-way scan ends. The equal band covers positions 1 to 5. The rank 3 is inside the equal band, so the method returns 5."}]}
```

<!-- stage: code -->
### Quickselect With Random Pivots

#### The Loop

The method keeps the loop shape of the naive version and replaces the pivot rule and the partition. It rearranges the array in place.

```java
final class RandomizedSelect {
    static int kthSmallest(int[] a, int k, java.util.function.IntUnaryOperator pick) {
        int lo = 0, hi = a.length - 1, target = k - 1;
        while (true) {
            int p = lo + pick.applyAsInt(hi - lo + 1);       // uniform position in [lo, hi]
            int pv = a[p];
            int lt = lo, i = lo, gt = hi;                    // below: [lo, lt), equal: [lt, i), unknown: [i, gt], above: (gt, hi]
            while (i <= gt) {
                if (a[i] < pv) { int t = a[lt]; a[lt] = a[i]; a[i] = t; lt++; i++; }
                else if (a[i] > pv) { int t = a[i]; a[i] = a[gt]; a[gt] = t; gt--; }
                else i++;
            }
            if (target < lt) hi = lt - 1;                    // keep the below band
            else if (target > gt) lo = gt + 1;               // keep the above band
            else return pv;                                  // the rank is in the equal band
        }
    }
}
```

#### Cost

- **Time** is O(n) expected for any input order, and O(n^2) in the worst case.
- **Space** is O(1), because the method works in place and keeps a few indices.
- **Mutation** rearranges the input array, so a caller who needs the original order passes a copy.

<!-- stage: applicability -->
### When Random Pivots Apply

#### Recognizing The Pattern

Use this method when the task needs the k-th smallest value, a median or a percentile. Check two conditions: only one rank is wanted, and the input order is not under your control. Before coding, decide whether equal values are common and whether the input array may be rearranged. The invariant to keep is that the wanted rank lies in the active range after every round.

#### False Friends

Sorting is a false friend when only one rank is needed, since it costs O(n log n) where selection costs O(n) on average. A heap of size `k` is a second false friend: it gives O(n log k) time and is better when `k` is small or the data arrive as a stream. A median of three fixed positions looks like a defence, but an adversarial order still defeats it.

#### When The Method Does Not Apply

If a hard worst-case bound is required, as in a real-time controller, the expected bound is not enough, and a deterministic median-of-medians selection or a heap is the right choice. If the input must keep its order, the method needs a copy. If the randomness source is predictable, an adversary can learn the pivots and rebuild the bad case.

<!-- stage: exercises -->
### Exercises

#### [Build] Uniform Pivot Index (Author exercise)
<!-- id: rp35-uniform-pivot-index -->

**Prerequisites.** The random pivot and the inclusive active range from this lesson.

**Problem.** Write `int pivotIndex(int lo, int hi, IntUnaryOperator pick)`. The method calls `pick.applyAsInt(hi - lo + 1)` exactly once and treats the result `d` as an offset. It returns `lo + d`. If `lo > hi`, it throws `IllegalArgumentException` before calling `pick`. If `d` is outside 0 to `hi - lo`, it throws `IllegalStateException`.

**Constraints.** The limits are:
- **Bounds** satisfy `0 <= lo` and `hi <= 10^9`, so `hi - lo + 1` fits in an `int`.
- **Range** is inclusive on both ends.
- **Draw** result lies from 0 to the bound minus 1 when the source is correct.
- **Calls** to `pick` number exactly one per valid call.

**Example 1.** Input `lo = 3`, `hi = 7`, scripted draw `4` for the bound 5, output `7`.

**Example 2.** Input `lo = 5`, `hi = 5`, scripted draw `0` for the bound 1, output `5`.

**Hint.** How many positions does an inclusive range from `lo` to `hi` contain?

**Changed decision.** Basic case: only the draw of the pivot position, with the upper end included.

#### [Vary] Randomized Quickselect (Author exercise)
<!-- id: rp35-randomized-quickselect -->

**Prerequisites.** The Uniform Pivot Index exercise above. This exercise adds the partition and keeps one side.

**Problem.** Write `int kthSmallest(int[] a, int k, IntUnaryOperator pick)`. Each round draws a pivot position with the previous exercise, swaps the pivot to the end of the active range, and partitions with the rule `a[j] < pv` so that smaller values come first. The pivot ends at its final index `s`. If `s` equals `k - 1`, the method returns the pivot. Otherwise it continues in the part of the range that contains `k - 1`. The method may rearrange `a`.

**Constraints.** The limits are:
- **Length** of `a` is from 1 to 10^5.
- **Rank** `k` is from 1 to the length.
- **Values** are `int` values that may repeat.
- **Draws** use the bound `hi - lo + 1` once per round.

**Example 1.** Input `a = [7, 2, 9, 4, 1]`, `k = 2`, scripted draws `0, 1`, output `2`.

**Example 2.** Input `a = [9, 4, 7, 4, 1, 8]`, `k = 3`, scripted draws `0, 1, 1`, output `4`.

**Hint.** After the partition, which side can be dropped when the wanted rank is below the pivot's final index?

**Changed decision.** The method keeps only the side that holds the wanted rank, and the input order no longer decides the pivot.

#### [Boundary] Equal Values (Author exercise)
<!-- id: rp35-equal-values -->

**Prerequisites.** The Randomized Quickselect exercise above. This exercise changes the partition from two parts to three.

**Problem.** Write `int[] kthSmallestThreeWay(int[] a, int k, IntUnaryOperator pick)`. Each round draws a pivot value `pv = a[lo + draw]` and splits the active range into values below `pv`, values equal to `pv` and values above `pv`. If the wanted rank lies in the equal band, the method stops. Otherwise it continues in the below part or the above part. Return `{value, rounds}`, where `rounds` is the number of loop passes that drew a pivot.

**Constraints.** The limits are:
- **Length** of `a` is from 1 to 10^5.
- **Rank** `k` is from 1 to the length.
- **Values** are `int` values, and many may be equal.
- **Rounds** count the draws, so an array of equal values gives `rounds == 1`.

**Example 1.** Input `a = [3, 1, 3, 2, 3]`, `k = 4`, scripted draws `1, 0`, output `{3, 2}`.

**Example 2.** Input `a = [4, 4, 4, 4, 4]`, `k = 3`, scripted draw `0`, output `{4, 1}`.

**Hint.** Where does the equal band sit after one pass, and what happens if the rank is inside it?

**Changed decision.** Equal values form their own band, and the method drops the whole band at once.

#### [Recognize] Kth Largest Element In An Array (LeetCode 215)
<!-- id: rp35-kth-largest -->

**Prerequisites.** The Equal Values exercise above. This exercise asks for the k-th largest value and for the cost argument.

**Problem.** Write `int findKthLargest(int[] nums, int k, IntUnaryOperator pick)`. Return the value that is the k-th largest in sorted descending order, where equal values count separately. Use randomized selection with a three-way partition, so the expected time is O(n) and the worst-case time is O(n^2).

**Constraints.** The limits are:
- **Length** of `nums` is from 1 to 10^5.
- **Rank** `k` is from 1 to the length.
- **Values** are `int` values from -10^9 to 10^9.
- **Mutation** is allowed, and the method rearranges `nums`.

**Example 1.** Input `nums = [9, 4, 7, 4, 1, 8]`, `k = 3`, scripted draws `0, 1`, output `7`.

**Example 2.** Input `nums = [6, 6, 2, 6, 3]`, `k = 2`, scripted draws `2, 0`, output `6`.

**Hint.** Which 0-based rank in ascending order matches the k-th largest?

**Changed decision.** The wanted rank counts from the top, so the target becomes `n - k` in ascending order.
