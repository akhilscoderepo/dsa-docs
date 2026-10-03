<!-- lesson-kind: standard -->
<!-- lesson-id: two-way-partition -->
## Two-Way Partition

<!-- stage: context -->
### A Courier Van And House Numbers

A courier loads a van at dawn. The parcels lie in one long row on a conveyor, each stamped with a house number. Houses with even numbers are on the sunny side of the street and are served first, houses with odd numbers are on the shady side and are served afterwards. The driver wants every even-numbered parcel in the front part of the row and every odd-numbered parcel in the back part, so that she can unload the front part on her outward trip and the back part on her return.

Nobody cares which even parcel comes first, and nobody cares about the order inside the back part either. The only promise she needs is that the front part holds only sunny-side parcels and the back part holds only shady-side parcels. The row is long, the conveyor is narrow, and there is no spare table to lay parcels on, so whatever rearranging is done must happen in the row itself.

<!-- stage: naive -->
### Slide Every Parcel Into Place

The tidy-minded plan is to walk the row once. Each time an even-numbered parcel is found behind the front group, lift it, slide every parcel between the front group and its old place one step along, and put it down right after the front group.

```java
static int groupByShifting(int[] row) {
    int front = 0;
    for (int i = 0; i < row.length; i++) {
        if (row[i] % 2 == 0) {
            int carried = row[i];
            for (int k = i; k > front; k--) row[k] = row[k - 1];
            row[front] = carried;
            front++;
        }
    }
    return front;
}
```

It works, and it even keeps the original order inside each group, which is a bonus nobody asked for. It returns how many even parcels there are, which is also the length of the front group.

<!-- stage: bottleneck -->
### The Slides Add Up Quadratically

Take a row that starts with a long run of odd parcels and ends with a long run of even ones. Every even parcel found late in the row drags a slide across the whole run of odd parcels in front of it, one assignment per parcel passed. With n/2 odd parcels followed by n/2 even parcels, each of the n/2 even ones moves across n/2 positions, so the total is about n^2/4 assignments, which is O(n^2). The scan itself was cheap. The cost is in sliding the same odd parcels along again and again.

Sliding was only needed to preserve the order, and the courier never asked for order. Without that promise, an even parcel that is stuck in the back part does not have to be carried to the front group at all. It only has to trade places with an odd parcel that is stuck in the front part, and a single trade fixes both of them at once, so each parcel should need at most one move instead of a slide across the whole row.

<!-- stage: insight -->
### Trade Places Across The Row

Keep one pointer `lo` at the left end and one pointer `hi` at the right end. The left part of the row, before `lo`, is finished and holds only even parcels. The right part, after `hi`, is finished and holds only odd parcels. Between the pointers, inclusive, lies the **unresolved zone**, the parcels nobody has looked at yet. The position where the even region ends and the odd region begins is the **boundary**, and when the unresolved zone becomes empty the boundary is simply `lo`.

Each step looks at the two parcels under the pointers. If the left one is even, it is already in the right region, so `lo` moves right. If the right one is odd, it is already in the right region too, so `hi` moves left. If neither of those holds, then the left parcel is odd and the right parcel is even, and together they are a **misplaced pair**: each is in the other's region. Trading their places swaps both into correct regions, and both pointers advance. Whatever the step, the unresolved zone shrinks by at least one position, so the loop ends after at most n steps.

<!-- names: unresolved zone, boundary, misplaced pair -->

The invariant is a statement about three parts of the row at once. Everything before `lo` is even, everything after `hi` is odd, and nothing has been promised about the zone in between. A trade moves only values inside the zone, so it never breaks that promise, and it fixes two positions with one operation. This is why no value moves more than once and the total number of trades can never exceed half the row length.

The same shape handles any yes or no question about a value, not just parity. Replace "is even" with "is smaller than a pivot" and the loop becomes the splitting step of quicksort, which needs the two regions and does not need the order inside them.

<!-- stage: variables -->
### Two Pointers And The Region Edge

`lo` is the first position that is not yet known to be even, and `hi` is the last position that is not yet known to be odd. The loop runs while `lo <= hi`, so a zone of exactly one parcel is still examined. When the loop ends, `lo` equals `hi + 1`, and it is both the count of even parcels and the index where the odd region starts. The array is rearranged in place, so it is the same object on exit with the same multiset of values, and the method returns `lo` so that the caller learns where the regions meet without scanning again.

<!-- stage: trace -->
### Trades Across The Whole Row

The first trace starts with the row 3, 8, 5, 6, 2, 7, 4, 1. The very first step shows that a pointer can move without any trade, because the right pointer is already on an odd parcel. The step to study is the second one, where the odd 3 on the left and the even 4 on the right form a misplaced pair and are traded in one move.

```trace
{"cells":[3,8,5,6,2,7,4,1],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":7},"vars":{"row":"3,8,5,6,2,7,4,1","evensSoFar":0},"note":"Position 0 holds the odd 3, and position 7 holds 1, which is odd and already in the back region, so hi moves to 6."},{"at":{"lo":0,"hi":6},"vars":{"row":"3,8,5,6,2,7,4,1","evensSoFar":0},"note":"Position 0 holds the odd 3 and position 6 holds the even 4. They form a misplaced pair, so both are exchanged and the pointers move to 1 and 5."},{"at":{"lo":1,"hi":5},"vars":{"row":"4,8,5,6,2,7,3,1","evensSoFar":1},"note":"Position 1 holds 8, which is even and already in the front region, so lo moves to 2."},{"at":{"lo":2,"hi":5},"vars":{"row":"4,8,5,6,2,7,3,1","evensSoFar":2},"note":"Position 2 holds the odd 5, and position 5 holds 7, which is odd and already in the back region, so hi moves to 4."},{"at":{"lo":2,"hi":4},"vars":{"row":"4,8,5,6,2,7,3,1","evensSoFar":2},"note":"Position 2 holds the odd 5 and position 4 holds the even 2. They form a misplaced pair, so both are exchanged and the pointers move to 3 and 3."},{"at":{"lo":3,"hi":3},"vars":{"row":"4,8,2,6,5,7,3,1","evensSoFar":3},"note":"Position 3 holds 6, which is even and already in the front region, so lo moves to 4."},{"at":{"lo":4,"hi":3},"vars":{"row":"4,8,2,6,5,7,3,1","evensSoFar":4},"note":"The pointers have crossed, so no position is unresolved. The first 4 positions are even and the rest are odd."}]}
```

The second trace uses a shorter row with an odd length, 12, 7, 9, 10, 5, and a different ending. Here one parcel is left alone in the zone at the end, with both pointers on the same position. The step to study is the fourth, where `lo` and `hi` coincide on the odd 9, which only needs `hi` to move, and that last move is what makes the pointers cross and the loop stop.

```trace
{"cells":[12,7,9,10,5],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":4},"vars":{"row":"12,7,9,10,5","evensSoFar":0},"note":"Position 0 holds 12, which is even and already in the front region, so lo moves to 1."},{"at":{"lo":1,"hi":4},"vars":{"row":"12,7,9,10,5","evensSoFar":1},"note":"Position 1 holds the odd 7, and position 4 holds 5, which is odd and already in the back region, so hi moves to 3."},{"at":{"lo":1,"hi":3},"vars":{"row":"12,7,9,10,5","evensSoFar":1},"note":"Position 1 holds the odd 7 and position 3 holds the even 10. They form a misplaced pair, so both are exchanged and the pointers move to 2 and 2."},{"at":{"lo":2,"hi":2},"vars":{"row":"12,10,9,7,5","evensSoFar":2},"note":"Both pointers sit on position 2, which holds the odd 9. It is in the back region, so hi moves to 1."},{"at":{"lo":2,"hi":1},"vars":{"row":"12,10,9,7,5","evensSoFar":2},"note":"The pointers have crossed, so no position is unresolved. The first 2 positions are even and the rest are odd."}]}
```

<!-- stage: code -->
### Parity, Pivot And Alternating Slots

```java
static int partitionBy(int[] a, java.util.function.IntPredicate front) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        if (front.test(a[lo])) lo++;
        else if (!front.test(a[hi])) hi--;
        else { int t = a[lo]; a[lo] = a[hi]; a[hi] = t; lo++; hi--; }
    }
    return lo;
}

static int sortByParity(int[] a) { return partitionBy(a, v -> v % 2 == 0); }

static int partitionAroundPivot(int[] a, int pivot) { return partitionBy(a, v -> v < pivot); }

static void placeEvenAtEvenSlots(int[] a) {
    int e = 0, o = 1;
    while (e < a.length && o < a.length) {
        if (a[e] % 2 == 0) e += 2;
        else if (a[o] % 2 != 0) o += 2;
        else { int t = a[e]; a[e] = a[o]; a[o] = t; e += 2; o += 2; }
    }
}
```

The predicate says whether a value belongs to the front region, so one loop serves parity and pivot questions. Each element is read a constant number of times, which gives O(n) time with O(1) extra space. The last method has the same trade, but its pointers step by two because each one walks only over positions of its own parity.

<!-- stage: applicability -->
### Two Regions Without An Order Promise

Reach for this loop when the answer has exactly two regions, the problem says that order inside a region does not matter, and the array may be rearranged. State the invariant out loud before coding it: before `lo` everything belongs in front, after `hi` everything belongs at the back, and the zone between them is untouched. Then decide whether the loop condition is `lo <= hi` or `lo < hi`, and check what the last single position does in each case.

A false friend is stable compaction, which keeps relative order and therefore may need many more writes, as the sliding method shows. Another false friend is a loop that moves `lo` with an inner `while` and forgets to test `lo <= hi`, which walks off the end of an array whose values are all in the front category. A third is a problem that does promise order or forbids changing the input, where trading values breaks the contract and a copy or a stable method is needed.

In Java, test evenness with `v % 2 == 0` and oddness with `v % 2 != 0`, never `v % 2 == 1`, because the remainder of a negative odd number is minus one. When the category is a comparison with a pivot, use `<` directly and do not subtract the values, because a difference can overflow.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort Array By Parity (LeetCode 905)
<!-- id: tp-parity-split -->

**Prerequisites.** Two pointers on opposite ends of an array, and the remainder operator on negative numbers.

**Problem.** Rearrange an integer array in place so that every even value comes before every odd value, with no promise about order inside either group, and return the number of even values. Negative values are allowed, and the method must not allocate a second array.

**Constraints.** 0 <= nums.length <= 5000 and values in the full `int` range. At most nums.length / 2 trades are allowed.

**Example 1.** Input `nums = [3, 1, 4, 6, 7, 2]`. Output 3, with the array left as `[2, 6, 4, 1, 7, 3]`, though any arrangement with the evens first is accepted.

**Example 2.** Input `nums = [1, 1, 2]`, output 1, with the array left as `[2, 1, 1]`.

**Hint.** What can you say about a position that holds an even value when the left pointer stands on it? What do you do when the left value is odd and the right value is even?

**Changed decision.** First rung: the output is rearranged in place and the return value is the length of the front region, so the pointers are judged by where they meet and not by an order.

#### [Vary] Partition Around Pivot (Author exercise)
<!-- id: tp-around-pivot -->

**Prerequisites.** The parity exercise above, and the idea that a predicate defines the front region.

**Problem.** Given an integer array and a pivot value, rearrange the array in place so that every value strictly smaller than the pivot comes before every value that is greater than or equal to it, and return the count of smaller values. Do not promise any order inside either region, and do not sort.

**Constraints.** 0 <= nums.length <= 5000, values and pivot anywhere in the `int` range, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`. The comparison must not use subtraction.

**Example 1.** Input `nums = [9, 2, 7, 4, 5, 1], pivot = 5`. Output 3, with the array left as `[1, 2, 4, 7, 5, 9]`.

**Example 2.** Input `nums = [4, 6, 5], pivot = 4`. Output 0, with the array left unchanged.

**Hint.** Which region does a value equal to the pivot belong to? What changes in the code compared with the parity version, and what stays the same?

**Changed decision.** The category is a comparison with a given value instead of a property of the value alone, and equal values go to the back region.

#### [Boundary] One Empty Region (Author exercise)
<!-- id: tp-one-empty-region -->

**Prerequisites.** Both exercises above.

**Problem.** Partition an integer array by parity in place and return two numbers: the boundary index and the number of trades made. Make sure that arrays whose values are all even, all odd, empty, or one element long work without reading outside the array.

**Constraints.** 0 <= nums.length <= 5000 and values in the full `int` range. An array that is already partitioned must cost zero trades.

**Example 1.** Input `nums = [2, 4, 6, 8]`, output `[4, 0]`, and the array is unchanged.

**Example 2.** Input `nums = [7, 5, 3]`, output `[0, 0]`, and the array is unchanged.

**Hint.** When every value is even, what is the only thing that can stop the left pointer? When every value is odd, which pointer travels all the way across?

**Changed decision.** The edge cases are the extreme splits, where one region is empty and one pointer must be stopped by the other, not by an element.

#### [Recognize] Sort Array By Parity II (LeetCode 922)
<!-- id: tp-alternating-parity -->

**Prerequisites.** All three exercises above.

**Problem.** An integer array has exactly as many even values as odd values. Rearrange it in place so that every even index holds an even value and every odd index holds an odd value, using one pointer for each class of index and no extra array. Return nothing, and any valid arrangement is accepted.

**Constraints.** The length is even, 0 <= nums.length <= 5000, with equal counts of even and odd values in the full `int` range. Each pointer moves only in steps of two.

**Example 1.** Input `nums = [4, 2, 5, 7]`, output nothing, with the array left as `[4, 5, 2, 7]`.

**Example 2.** Input `nums = [3, 0, 1, 6]`, output nothing, with the array left as `[0, 3, 6, 1]`.

**Hint.** The two pointers no longer start at the two ends. What does each pointer's position tell you about the value that belongs there?

**Changed decision.** The regions are interleaved instead of contiguous, so the pointers start at the front, advance by two, and each one stands for a destination class and not for an end of the array.
