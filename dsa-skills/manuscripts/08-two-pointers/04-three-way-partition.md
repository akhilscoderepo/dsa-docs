<!-- lesson-kind: standard -->
<!-- lesson-id: three-way-partition -->
## Three-Way Partition

<!-- stage: context -->
### A Laundry Cart Of Towels

A hotel laundry room receives one big cart of towels, all mixed together. Each towel carries a small tag that a handheld scanner can read, and the tag says one of three things: it is bleached white, it is a pale color, or it is dark. The washing machines are loaded in that order, whites first, pale colors second, darks last, so the cart has to be rearranged into three stretches along a long rail: whites at the start, darks at the end, and the pale ones in between.

The rail has no spare hooks, so the towels must be rearranged on the hooks it already has. Scanning is slow because the attendant has to hold each towel under the scanner, so she would like to scan each towel as few times as possible. Moving a towel from one hook to another is easy, and the order of towels inside one stretch does not matter at all.

<!-- stage: naive -->
### Two Sweeps Along The Rail

The attendant can use the plan that worked for two groups, twice. The first sweep gathers all the white towels at the start of the rail. The second sweep starts after the whites and gathers the pale towels right behind them. Whatever is left must be dark.

```java
static void twoSweeps(int[] rail) {
    int placed = 0;
    for (int i = 0; i < rail.length; i++) {
        if (rail[i] == 0) {
            int t = rail[i]; rail[i] = rail[placed]; rail[placed] = t;
            placed++;
        }
    }
    for (int i = placed; i < rail.length; i++) {
        if (rail[i] == 1) {
            int t = rail[i]; rail[i] = rail[placed]; rail[placed] = t;
            placed++;
        }
    }
}
```

The codes are 0 for white, 1 for pale and 2 for dark. The result is correct for any rail made of those three codes, and it uses no extra hooks.

<!-- stage: bottleneck -->
### Every Sweep Scans Towels Again

The first sweep scans all n towels, and the second scans nearly all of them again, because the second sweep still has to look at every towel that is not white. Each sweep is O(n), so two sweeps are O(n) overall, but the constant matters when each scan is slow, and the pattern grows worse with more groups: k groups need k minus one sweeps, which is O(k * n) scans. Many of those scans are repeats. A dark towel is looked at in the first sweep and is looked at again in the second sweep, and the second look learns nothing new about it.

What the attendant needs is a way to scan each towel once and decide its destination immediately. That is possible if the rail is described by regions that grow as scanning continues, so that every scanned towel is already in the right stretch or at least adjacent to it. One pass with a few markers should replace the sweeps, and each position should be read a constant number of times.

<!-- stage: insight -->
### Four Regions And One Open Zone

Place three markers, `low`, `mid` and `high`, along the rail. They cut the rail into **four regions**. Positions before `low` hold only whites. Positions from `low` up to but not including `mid` hold only pale towels. Positions from `mid` through `high`, inclusive, are not yet scanned, and positions after `high` hold only darks. The scanning marker is `mid`, and it always stands on the first position nobody has looked at.

Each step reads the towel at `mid` exactly once and chooses among three moves. A white towel trades places with the towel at `low`, which is a pale one or `mid` itself, and then both `low` and `mid` advance. A pale towel is already in the middle stretch, so only `mid` advances. A dark towel trades places with the towel at `high` and `high` retreats. In that third case `mid` must stay where it is, because the **incoming value** that arrived from the far end has never been scanned. The loop must **reinspect** the same position. The asymmetry is deliberate. After a trade with `low`, the arriving towel is known to be pale, since everything between `low` and `mid` was scanned and was pale, so `mid` can move on safely.

<!-- names: four regions, incoming value, reinspect -->

The invariant is exactly that division of the rail: before `low` is white, from `low` to before `mid` is pale, after `high` is dark, and the stretch in between is open. Each step shrinks the open stretch by one position, and the loop ends when `mid` passes `high`, at which time nothing is left open. The three outcomes change one or two positions and always preserve the division, so the correctness argument is a short case check and not an argument about the whole rail.

The same machinery sorts any list into below, equal and above relative to a chosen value, which is how quicksort stays fast when many equal values exist.

<!-- stage: variables -->
### Three Markers And Their Meanings

`low` is the first position of the pale stretch, and everything before it is white. `mid` is the next position to scan, and it is also the end of the pale stretch. `high` is the last position that is not yet known to be dark. At the start `low` and `mid` are both 0 and `high` is the last index, so every region except the open one is empty. When the loop ends, `low` is the number of whites, `mid` equals `high + 1`, and `mid` is also the first dark position, so the two returned boundaries are `low` and `mid`.

<!-- stage: trace -->
### Whites Forward And Darks Backward

The first trace starts with the rail 2, 0, 2, 1, 1, 0, which opens with a dark towel. The first step shows the rule that matters most: the dark towel trades with the last position, `high` retreats, and `mid` does not move. The step to study is the fourth, where another dark towel at position 2 trades with position 4 and the value that arrives is a pale one, scanned in the next step.

```trace
{"cells":[2,0,2,1,1,0],"pointers":["low","mid","high"],"steps":[{"at":{"low":0,"mid":0,"high":5},"vars":{"row":"2,0,2,1,1,0","value":2},"note":"Position 0 holds 2. It trades with position 5, high becomes 4, and mid stays at 0 because the value that arrived from position 5 has not been looked at yet."},{"at":{"low":0,"mid":0,"high":4},"vars":{"row":"0,0,2,1,1,2","value":0},"note":"Position 0 holds 0 and the middle region is empty, so it trades with itself. Both low and mid move on to 1."},{"at":{"low":1,"mid":1,"high":4},"vars":{"row":"0,0,2,1,1,2","value":0},"note":"Position 1 holds 0 and the middle region is empty, so it trades with itself. Both low and mid move on to 2."},{"at":{"low":2,"mid":2,"high":4},"vars":{"row":"0,0,2,1,1,2","value":2},"note":"Position 2 holds 2. It trades with position 4, high becomes 3, and mid stays at 2 because the value that arrived from position 4 has not been looked at yet."},{"at":{"low":2,"mid":2,"high":3},"vars":{"row":"0,0,1,1,2,2","value":1},"note":"Position 2 holds 1, which already belongs in the middle region, so mid moves to 3."},{"at":{"low":2,"mid":3,"high":3},"vars":{"row":"0,0,1,1,2,2","value":1},"note":"Position 3 holds 1, which already belongs in the middle region, so mid moves to 4."},{"at":{"low":2,"mid":4,"high":3},"vars":{"row":"0,0,1,1,2,2","value":"none"},"note":"The unresolved region is empty. Zeros fill the first 2 positions, ones fill the next 2, and twos fill the last 2."}]}
```

The second trace uses the shorter rail 1, 0, 2, 1, 0. Here the first step is a pale towel that costs only a move of `mid`, and then a white towel has to trade with a pale one at `low`. The step to study is the fourth. The white towel that arrived from the far end now sits under `mid`, and it is placed in the first region by a trade with position 1, which holds a pale towel.

```trace
{"cells":[1,0,2,1,0],"pointers":["low","mid","high"],"steps":[{"at":{"low":0,"mid":0,"high":4},"vars":{"row":"1,0,2,1,0","value":1},"note":"Position 0 holds 1, which already belongs in the middle region, so mid moves to 1."},{"at":{"low":0,"mid":1,"high":4},"vars":{"row":"1,0,2,1,0","value":0},"note":"Position 1 holds 0. It trades with position 0, which holds a 1 from the middle region, so low becomes 1 and mid becomes 2."},{"at":{"low":1,"mid":2,"high":4},"vars":{"row":"0,1,2,1,0","value":2},"note":"Position 2 holds 2. It trades with position 4, high becomes 3, and mid stays at 2 because the value that arrived from position 4 has not been looked at yet."},{"at":{"low":1,"mid":2,"high":3},"vars":{"row":"0,1,0,1,2","value":0},"note":"Position 2 holds 0. It trades with position 1, which holds a 1 from the middle region, so low becomes 2 and mid becomes 3."},{"at":{"low":2,"mid":3,"high":3},"vars":{"row":"0,0,1,1,2","value":1},"note":"Position 3 holds 1, which already belongs in the middle region, so mid moves to 4."},{"at":{"low":2,"mid":4,"high":3},"vars":{"row":"0,0,1,1,2","value":"none"},"note":"The unresolved region is empty. Zeros fill the first 2 positions, ones fill the next 2, and twos fill the last 1."}]}
```

<!-- stage: code -->
### Flag Sort And Pivot Split

```java
static int[] flagSort(int[] rail) {
    int low = 0, mid = 0, high = rail.length - 1;
    while (mid <= high) {
        int code = rail[mid];
        if (code == 0) { rail[mid] = rail[low]; rail[low] = 0; low++; mid++; }
        else if (code == 1) mid++;
        else { rail[mid] = rail[high]; rail[high] = 2; high--; }   // do not advance mid
    }
    return new int[] {low, mid};
}

static int[] splitAroundPivot(int[] a, int pivot) {
    int lt = 0, i = 0, gt = a.length - 1;
    while (i <= gt) {
        int c = Integer.compare(a[i], pivot);
        if (c < 0) { int t = a[lt]; a[lt] = a[i]; a[i] = t; lt++; i++; }
        else if (c > 0) { int t = a[gt]; a[gt] = a[i]; a[i] = t; gt--; }
        else i++;
    }
    return new int[] {lt, gt + 1};
}
```

Every iteration moves `mid` forward or `high` backward, so the loop runs at most n times and makes O(n) reads with O(1) extra space. The second method uses a comparison result so that the three categories come from one read of each value, and it does not subtract the values.

<!-- stage: applicability -->
### When Three Categories Share One Pass

Choose this partition when every element falls into exactly one of three ordered categories, such as low, middle and high, and the array may be rearranged. Before writing the loop, say the invariant aloud as four ranges, name which of them each marker bounds, and decide the two return values. A good test for the rule on the far side is to hand the loop an array that begins with a high value and check that it is read again after the trade.

A false friend is the two-way partition from the previous lesson. It finishes with two regions, so a third category forces a second sweep and the repeated scans described earlier. Another false friend is a counting rewrite that tallies the codes and overwrites the array with zeros, ones and twos. It is correct for bare integers, but it destroys objects that merely carry a category, and it needs two passes. A third is a problem that wants stability among equal elements, where trading values will break the promised order.

In Java, compare with `Integer.compare` or direct `<` and `>` tests, and never with subtraction, which can overflow for values near the ends of the `int` range. Keep the three branches in the order low, middle, high so that the dangerous branch, the one that does not advance `mid`, is easy to spot and to test.

<!-- stage: exercises -->
### Exercises

#### [Build] Partition 0,1,2 (Author exercise)
<!-- id: tp-flag-012 -->

**Prerequisites.** The two-way partition lesson, and the idea of an open region between two finished regions.

**Problem.** An integer array contains only the values 0, 1 and 2. Rearrange it in place in a single pass so that the zeros come first, then the ones, then the twos, and return the pair of start indexes of the ones and of the twos. Do not call a library sort and do not count values.

**Constraints.** 0 <= nums.length <= 3000 and every value is 0, 1 or 2. Each loop step must retire at least one position.

**Example 1.** Input `nums = [2, 1, 0, 1, 2, 0]`, output `[2, 4]`, with the array left as `[0, 0, 1, 1, 2, 2]`.

**Example 2.** Input `nums = [1, 1, 1]`, output `[0, 3]`, with the array left unchanged.

**Hint.** Which region does each marker end? What must be true of the position under `mid` before you decide what to do with it?

**Changed decision.** First rung: the invariant has four regions and one scanning marker, so the answer is read from where the markers end.

#### [Vary] Sort Colors (LeetCode 75)
<!-- id: tp-sort-colors -->

**Prerequisites.** The exercise above.

**Problem.** An array holds the codes 0 for red, 1 for white and 2 for blue. Sort it in place so that the reds come first, then the whites, then the blues. Return nothing. Use one pass, make no more than nums.length loop iterations, and do not call a library sort.

**Constraints.** 0 <= nums.length <= 3000 and every value is 0, 1 or 2. The array object must be the same object on return, and extra memory must not depend on the length.

**Example 1.** Input `nums = [2, 0, 2, 1, 1, 0]`, output nothing, with the array left as `[0, 0, 1, 1, 2, 2]`.

**Example 2.** Input `nums = [1, 0]`, output nothing, with the array left as `[0, 1]`.

**Hint.** The category meanings are unchanged. What changes is the contract: nothing is returned and the bound on loop iterations is part of the promise.

**Changed decision.** The same invariant is applied to the formal problem, so the work is to meet the contract exactly: the sorted array is the only result, and the loop-iteration bound is checked.

#### [Boundary] Reinspect Swapped High (Author exercise)
<!-- id: tp-reinspect-high -->

**Prerequisites.** Both exercises above.

**Problem.** Run the one-pass sort on an array of the codes 0, 1 and 2, and return the sorted array together with the number of loop steps that left the scanning marker in place after a trade with the high end. Explain in the solution why a version that advances `mid` after such a trade is wrong.

**Constraints.** 0 <= nums.length <= 3000 and every value is 0, 1 or 2. The array must be sorted correctly, and the count must come from the loop itself.

**Example 1.** Input `nums = [2, 0, 1]`, output sorted array `[0, 1, 2]` and count 1.

**Example 2.** Input `nums = [2, 2, 0]`, output sorted array `[0, 2, 2]` and count 2.

**Hint.** Which value sits under `mid` right after the trade with the high end? Compare the count with the number of twos in the input.

**Changed decision.** The edge case is the single branch that does not advance `mid`, and the exercise makes its effect countable and testable.

#### [Recognize] Three-Way Pivot Partition (Author exercise)
<!-- id: tp-pivot-three-way -->

**Prerequisites.** The three exercises above.

**Problem.** Given an integer array and a pivot value, rearrange the array in place so that values smaller than the pivot come first, values equal to the pivot come next, and values greater than the pivot come last. Return the pair holding the index where the equal region starts and the index where the greater region starts. Values may be anywhere in the `int` range.

**Constraints.** 0 <= nums.length <= 3000, with values and pivot anywhere in the `int` range, including both extremes. Compare values directly or with `Integer.compare`, and never by subtraction.

**Example 1.** Input `nums = [5, 9, 5, 1, 7, 5, 2], pivot = 5`, output `[2, 5]`, with the array left as `[2, 1, 5, 5, 5, 7, 9]`.

**Example 2.** Input `nums = [3, 3, 3], pivot = 8`, output `[3, 3]`, with the array left unchanged.

**Hint.** The three category tests come from one comparison result. Which of the old codes does each outcome of the comparison play the part of?

**Changed decision.** The codes 0, 1 and 2 are replaced by the outcomes of a comparison with a pivot, so the loop reads a value and compares it, with the equal region taking the place of the pale stretch.
