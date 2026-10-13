<!-- lesson-kind: standard -->
<!-- lesson-id: submask-aggregation -->
## Submask Aggregation

<!-- stage: context -->
### Trying Every Flag Combination

A configuration service stores the enabled feature flags of one customer as the bits of an `int`. The customer has flags 0, 2 and 3 enabled, so the mask is `1101` in binary, which is 13. A test planner must run the product once for every nonempty combination of those three flags. There are 7 combinations: 13, 12, 9, 8, 5, 4 and 1.

A developer writes the obvious scan. It counts `s` from 1 up to the mask and keeps `s` when `(s & mask) == s`, which means every set bit of `s` is also set in the mask. For the mask 13 the scan makes 13 steps to find 7 combinations, and nobody notices the waste.

The waste appears when the enabled flags sit at high positions. A customer with only flags 0 and 29 enabled has 3 combinations, but the scan counts up to more than half a billion. The same pattern appears in every problem that splits a set of up to about 16 items into two groups.

One such problem is grouping. Four items weigh 4, 3, 3 and 2, and a group may hold items of total weight at most 6. The task is the smallest number of groups. A solution tries every way to cut the item set into two parts, and each part is a subset of the items.

Formally, the input is one non-negative `int` called `mask`. A **subset** of the mask is an `int` whose set bits all lie among the set bits of the mask. The task is to visit every nonempty subset exactly once. This lesson asks how to reach each one in constant work, so the cost depends on the number of enabled flags and not on their positions.

<!-- stage: naive -->
### Counting Up And Filtering

The simple method tries every integer from 1 to `mask` and keeps those that pass the filter. It never looks at which bits the mask contains.

```java
static int countByScan(int mask) {
    int found = 0;
    for (int s = 1; s <= mask; s++) {
        if ((s & mask) == s) {
            found++;
        }
    }
    return found;
}
```

The loop makes `mask` iterations, so the cost is O(mask) time with O(1) memory. A mask is as large as its highest set bit, so the cost grows with the position of the top flag and not with the number of flags. The method is correct. It is slow only because most of the integers it tries fail the filter.

```predict
Call countByScan with mask = (1 << 29) | 1. How many subsets does it find, and how many loop iterations does it make?

It finds 3 subsets: 2^29 + 1, 2^29 and 1. It makes 2^29 + 1 = 536870913 iterations, because the loop runs up to the mask itself. Almost every iteration fails the filter.
```

<!-- stage: bottleneck -->
### The Scan Ignores The Mask Bits

The scan spends one iteration per integer, and a mask with k set bits has only 2^k subsets. The ratio of wasted work to useful work is about mask / 2^k. A mask of 30 bits with 2 set bits wastes about 2^30 iterations to reach 3 results.

The cost grows when a dynamic program needs the subsets of every mask. Such a program loops over all masks from 0 to 2^n - 1 and runs the scan inside each one. The total is the sum of the mask values, which is about 2^n * 2^n / 2, so the cost is O(4^n). For n = 20 that is about 5.5 * 10^11 steps, which no judge accepts.

Most of those steps are wasted. A mask with k set bits has only 2^k subsets, and the sum of 2^k over all masks is 3^n. Each of the n items is in the subset, in the rest of the mask, or outside the mask, which gives 3 choices per item. For n = 20 the number is 3486784401, about 160 times smaller than the 5.5 * 10^11 steps of the scan, yet still too many for a time limit. The next section shows how to step directly from one subset to the next, so the work matches the number of subsets.

<!-- stage: insight -->
### Step Down To The Next Subset

Name the subsets, then find one operation that moves from a subset to the next smaller one. With that operation, a loop visits only real subsets.

<!-- names: submask, descending step, bit layer -->

#### A Submask Is A Subset Of Bits

A **submask** of `mask` is an integer `sub` with `(sub & mask) == sub`. Every submask is at most `mask`, and the mask itself is its largest submask. If the mask has k set bits, it has exactly 2^k submasks, including 0, because each set bit is either kept or dropped.

#### The Descending Step

The **descending step** computes `(sub - 1) & mask` from a submask `sub`. Subtracting 1 clears the lowest set bit of `sub`, call its position p, and sets every bit below p. The AND with `mask` then removes the bits that are not in the mask. The result is `sub` with bit p replaced by all the mask bits below p.

This value is the next smaller submask. Any submask that is smaller than `sub` either differs from `sub` at a bit above p, which makes it smaller than the result, or agrees with `sub` above p and uses only mask bits below p, which makes it at most the result. Starting from `mask`, the loop therefore meets each submask once, in strictly decreasing order, and it reaches 0 last.

#### Stop At Zero On Purpose

The value 0 is a submask, but the standard loop treats it as the end. In Java, `0 - 1` is `-1`, whose bits are all set, so `(0 - 1) & mask` equals `mask`. A loop that continues after 0 returns to the start and never ends. The condition `sub > 0` ends the loop and skips the empty submask. A loop that must include 0 handles it with its own check before it computes the next value.

#### Split A Mask Into Two Parts

A submask `sub` also names a split. The pair `sub` and `mask ^ sub` divides the set bits of `mask` into two disjoint parts. A dynamic program that combines `dp[sub]` with `dp[mask ^ sub]` reads only values with a smaller mask number, so it fills `dp` in increasing mask order. Each mask costs 2^k steps, and the total over all masks is O(3^n).

#### Sum Over Subsets With Bit Layers

Some problems need, for every mask, the sum of `a[sub]` over all of its submasks. This task is called **sum over subsets**, and the exercises abbreviate it as SOS. Enumerating the submasks costs O(3^n). A **bit layer** reduces this to O(n * 2^n). Layer b visits every mask that has bit b set and adds the value of the mask with bit b cleared. After layer b, `f[mask]` holds the sum over the submasks that differ from `mask` only in bits 0 to b. After all n layers, every submask has been counted exactly once.

Take n = 2 and `a = [1, 2, 3, 4]`, indexed by masks 0 to 3. Layer 0 visits masks 1 and 3. It adds `f[0]` to `f[1]`, which gives 3, and adds `f[2]` to `f[3]`, which gives 7. The array is now `[1, 3, 3, 7]`. Layer 1 visits masks 2 and 3. It adds `f[0]` to `f[2]`, which gives 4, and adds `f[1]` to `f[3]`, which gives 7 + 3 = 10. The final array is `[1, 3, 4, 10]`. Mask 3 holds 1 + 2 + 3 + 4, one term for each of its four submasks.

<!-- stage: variables -->
### Masks, Submasks And Tables

These values appear in the loops and tables of this lesson.

- **mask** is the `int` whose set bits form the full set.
- **sub** is the current submask of `mask`, and `(sub & mask) == sub` holds at every step.
- **rest** is `mask ^ sub`, the part of the mask that `sub` leaves out.
- **dp** is an `int[1 << n]`; entry `dp[mask]` is the best answer for the items named by `mask`.
- **f** is a `long[1 << n]` that holds `a` at the start and the sum over submasks at the end.
- **bit** is the index of the current bit layer, from 0 to n - 1.

Java stores an `int` in 32 bits, and `1 << b` has only bit b set. A mask for n items therefore uses bits 0 to n - 1, and the arrays have `1 << n` entries. A sum over up to 2^n values can exceed the `int` range, so `f` uses `long`.

<!-- stage: trace -->
### Two Runs Of Submask Loops

#### Listing The Submasks Of 1101

The first run uses the mask `1101` from the opening. The cells list the 7 nonempty submasks in the order the loop reports them. The pointer `i` marks the submask being processed. At each step the variable `sub-1` shows the result of the subtraction, and `next` shows the value after the AND with the mask.

The first step reports 13. Subtracting 1 gives `1100`, which the mask keeps unchanged, so the next submask is 12. From 12, subtracting 1 gives `1011`, and the AND removes bit 1, which leaves `1001`. The loop skips 11, 10 and every other value that has bit 1 set. The last report is 1, and the next value is 0, so the loop stops. The pointer then moves past the last cell, and the count of 7 equals 2^3 - 1.

```trace
{"cells":[13,12,9,8,5,4,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"sub":"1101","sub-1":"1100","next":"1100"},"note":"The submask 1101 is reported. Subtracting 1 gives 1100, and the AND with the mask leaves 1100."},{"at":{"i":1},"vars":{"sub":"1100","sub-1":"1011","next":"1001"},"note":"The submask 1100 is reported. Subtracting 1 gives 1011, and the AND with the mask leaves 1001."},{"at":{"i":2},"vars":{"sub":"1001","sub-1":"1000","next":"1000"},"note":"The submask 1001 is reported. Subtracting 1 gives 1000, and the AND with the mask leaves 1000."},{"at":{"i":3},"vars":{"sub":"1000","sub-1":"0111","next":"0101"},"note":"The submask 1000 is reported. Subtracting 1 gives 0111, and the AND with the mask leaves 0101."},{"at":{"i":4},"vars":{"sub":"0101","sub-1":"0100","next":"0100"},"note":"The submask 0101 is reported. Subtracting 1 gives 0100, and the AND with the mask leaves 0100."},{"at":{"i":5},"vars":{"sub":"0100","sub-1":"0011","next":"0001"},"note":"The submask 0100 is reported. Subtracting 1 gives 0011, and the AND with the mask leaves 0001."},{"at":{"i":6},"vars":{"sub":"0001","sub-1":"0000","next":"0000"},"note":"The submask 0001 is reported. Subtracting 1 gives 0000, and the AND with the mask leaves 0000. This is 0, so the loop stops."},{"at":{"i":7},"vars":{"sub":"0000","count":7},"note":"The loop ends with 7 nonempty submasks, which equals 2^3 - 1."}]}
```

#### Splitting Four Items Into Groups

The second run solves a small grouping problem. Four items weigh 4, 3, 3 and 2, a group may hold at most 6, and the task is the smallest number of groups. The cells show the total weight of each mask from 0 to 15, and the pointer `mask` marks the entry in progress. Bit 0 is the item of weight 4, bit 1 and bit 2 are the two items of weight 3, and bit 3 is the item of weight 2.

A mask whose total fits the capacity needs one group. Any other mask tries every split into `sub` and `mask ^ sub` and keeps the smallest sum of the two stored values. The mask `1111` weighs 12, so it needs a split. The split of items 4 with 2 and items 3 with 3 gives 1 plus 1, and no single group holds all four, so the answer is 2.

```trace
{"cells":[0,4,3,7,3,7,6,10,2,6,5,9,5,9,8,12],"pointers":["mask"],"steps":[{"at":{"mask":0},"vars":{"mask":"0000","sum":0,"dp":0},"note":"The empty mask needs 0 groups, so it is the base value."},{"at":{"mask":1},"vars":{"mask":"0001","sum":4,"dp":1},"note":"The items of 0001 weigh 4, which fits the capacity 6. One group holds them."},{"at":{"mask":2},"vars":{"mask":"0010","sum":3,"dp":1},"note":"The items of 0010 weigh 3, which fits the capacity 6. One group holds them."},{"at":{"mask":3},"vars":{"mask":"0011","sum":7,"split":"0010","dp":2},"note":"The items of 0011 weigh 7, which exceeds 6. The best split is 0010 with 0001, which costs 1 plus 1."},{"at":{"mask":4},"vars":{"mask":"0100","sum":3,"dp":1},"note":"The items of 0100 weigh 3, which fits the capacity 6. One group holds them."},{"at":{"mask":5},"vars":{"mask":"0101","sum":7,"split":"0100","dp":2},"note":"The items of 0101 weigh 7, which exceeds 6. The best split is 0100 with 0001, which costs 1 plus 1."},{"at":{"mask":6},"vars":{"mask":"0110","sum":6,"dp":1},"note":"The items of 0110 weigh 6, which fits the capacity 6. One group holds them."},{"at":{"mask":7},"vars":{"mask":"0111","sum":10,"split":"0110","dp":2},"note":"The items of 0111 weigh 10, which exceeds 6. The best split is 0110 with 0001, which costs 1 plus 1."},{"at":{"mask":8},"vars":{"mask":"1000","sum":2,"dp":1},"note":"The items of 1000 weigh 2, which fits the capacity 6. One group holds them."},{"at":{"mask":9},"vars":{"mask":"1001","sum":6,"dp":1},"note":"The items of 1001 weigh 6, which fits the capacity 6. One group holds them."},{"at":{"mask":10},"vars":{"mask":"1010","sum":5,"dp":1},"note":"The items of 1010 weigh 5, which fits the capacity 6. One group holds them."},{"at":{"mask":11},"vars":{"mask":"1011","sum":9,"split":"1010","dp":2},"note":"The items of 1011 weigh 9, which exceeds 6. The best split is 1010 with 0001, which costs 1 plus 1."},{"at":{"mask":12},"vars":{"mask":"1100","sum":5,"dp":1},"note":"The items of 1100 weigh 5, which fits the capacity 6. One group holds them."},{"at":{"mask":13},"vars":{"mask":"1101","sum":9,"split":"1100","dp":2},"note":"The items of 1101 weigh 9, which exceeds 6. The best split is 1100 with 0001, which costs 1 plus 1."},{"at":{"mask":14},"vars":{"mask":"1110","sum":8,"split":"1100","dp":2},"note":"The items of 1110 weigh 8, which exceeds 6. The best split is 1100 with 0010, which costs 1 plus 1."},{"at":{"mask":15},"vars":{"mask":"1111","sum":12,"split":"1001","dp":2},"note":"The items of 1111 weigh 12, which exceeds 6. The best split is 1001 with 0110, which costs 1 plus 1."}]}
```

<!-- stage: code -->
### Three Loops Over Submasks

The first method returns all nonempty submasks of a mask in decreasing order. The second method fills the grouping table from the trace. The third method sums over all submasks with one pass per bit.

```java
static int[] listSubmasks(int mask) {
    int[] out = new int[(1 << Integer.bitCount(mask)) - 1];
    int w = 0;
    for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
        out[w++] = sub;
    }
    return out;
}

static int minGroups(int[] weight, int cap) {
    int n = weight.length;
    int[] total = new int[1 << n];
    int[] dp = new int[1 << n];
    for (int mask = 1; mask < (1 << n); mask++) {
        int low = Integer.numberOfTrailingZeros(mask);
        total[mask] = total[mask & (mask - 1)] + weight[low];
        dp[mask] = total[mask] <= cap ? 1 : Integer.MAX_VALUE;
        for (int sub = (mask - 1) & mask; sub > 0; sub = (sub - 1) & mask) {
            dp[mask] = Math.min(dp[mask], dp[sub] + dp[mask ^ sub]);
        }
    }
    return dp[(1 << n) - 1];
}

static long[] sumOverSubmasks(long[] a, int n) {
    long[] f = a.clone();
    for (int bit = 0; bit < n; bit++) {
        for (int mask = 0; mask < (1 << n); mask++) {
            if ((mask >> bit & 1) == 1) {
                f[mask] += f[mask ^ (1 << bit)];
            }
        }
    }
    return f;
}
```

The first method runs in O(2^k) time for a mask with k set bits. The second runs in O(3^n) time and O(2^n) memory, and it assumes every weight is at most `cap`. The third runs in O(n * 2^n) time. In the second method, `mask & (mask - 1)` clears the lowest set bit, which lets each total reuse a smaller one. The inner loop starts at `(mask - 1) & mask`, which skips `mask` itself, and it stops at 0, which skips the empty part.

<!-- stage: applicability -->
### Recognizing Subset Splits

#### Reading The Cue

Use this method when a transition or a query ranges over every subset of a mask. Phrases such as "split the set into two groups", "for every subset of the chosen items" and "sum over all subsets" point here. The bit count n must stay small, because 3^n is the cost of full enumeration. That is feasible up to about n = 15 or 16, where 3^16 is about 43 million. The bit-layer sum costs only n * 2^n, so it reaches n = 20.

#### Checking The Invariant

The invariant of the descending step is that every submask below the current one is still ahead, and none has been skipped or repeated. Check it on a mask with one bit, which must report that bit only. Check it on a mask with spread bits, such as `100001`, which must report 3 values. Check that a mask of 0 reports nothing. For the table, the invariant is that both `dp[sub]` and `dp[mask ^ sub]` are final when `dp[mask]` reads them, because both have smaller mask numbers.

#### Avoiding The False Friend

The first false friend is the counting scan from the opening, which gives correct output at a cost that depends on the highest bit. The second is a loop written `sub >= 0`, which never ends, because `-1 & mask` equals `mask`. The third is a split that visits both `sub` and `mask ^ sub` as separate cases and counts every pair twice. When the pair is unordered, the loop can fix the lowest bit of `mask` inside `sub`.

The split loop does not apply when n is above about 16, because 3^n is too large. The bit-layer sum does not apply above about 20. Neither applies when the groups are not drawn from one shared set of items. In those cases a different state or a greedy argument is needed.

<!-- stage: exercises -->
### Exercises

#### [Build] Enumerate Submasks (Author exercise)
<!-- id: dp29-enumerate-submasks -->

**Prerequisites.** Setting, testing and counting bits from the previous lesson.

**Problem.** An integer `mask` is given. Return all nonempty submasks of `mask` in decreasing order. A submask is an integer `sub` with `(sub & mask) == sub`.

**Constraints.** The limits are:
- **Value** satisfies `0 <= mask < 2^20`, and `mask` may be 0.
- **Result** is an `int[]` of length `2^k - 1`, where k is the number of set bits.
- **Order** is strictly decreasing.
- **Mutation** is not applicable, because the input is a single integer.

**Example 1.** Input `mask = 13`, output `[13, 12, 9, 8, 5, 4, 1]`.

**Example 2.** Input `mask = 6`, output `[6, 4, 2]`.

**Hint.** Which value comes after `sub`, and where does the loop stop?

**Changed decision.** The loop jumps from one submask to the next in place of counting through all integers, so the cost follows the number of results.

#### [Vary] Partition A Mask (Author exercise)
<!-- id: dp29-partition-mask -->

**Prerequisites.** The exercise above.

**Problem.** An array `weight` of `n` positive integers and an integer `cap` are given. Split the items into groups so that the weights in each group sum to at most `cap`. Return the smallest possible number of groups.

**Constraints.** The limits are:
- **Items** satisfy `1 <= n <= 12`.
- **Weights** satisfy `1 <= weight[i] <= cap`.
- **Capacity** satisfies `1 <= cap <= 10^6`.
- **Result** is an `int`, and the array stays unchanged.

**Example 1.** Input `weight = [4, 3, 3, 2]`, `cap = 6`, output `2`.

**Example 2.** Input `weight = [5, 5, 5]`, `cap = 9`, output `3`.

**Hint.** Which two table entries does a split of a mask into `sub` and `mask ^ sub` read?

**Changed decision.** The loop now combines two stored answers for each split in place of listing the parts, so each mask uses its proper submasks.

#### [Boundary] Include Empty Submask Deliberately (Author exercise)
<!-- id: dp29-include-empty -->

**Prerequisites.** The two exercises above.

**Problem.** An integer `mask` is given. Return all submasks of `mask`, including 0, in decreasing order.

**Constraints.** The limits are:
- **Value** satisfies `0 <= mask < 2^20`, and `mask` may be 0.
- **Result** is an `int[]` of length `2^k`, where k is the number of set bits, and its last entry is 0.
- **Order** is strictly decreasing.
- **Termination** is required for every allowed `mask`, including 0.

**Example 1.** Input `mask = 5`, output `[5, 4, 1, 0]`.

**Example 2.** Input `mask = 0`, output `[0]`.

**Hint.** What does `(0 - 1) & mask` equal in Java, and where must the check for 0 sit?

**Changed decision.** The loop reports the empty submask, so it must test for 0 before it computes the next value.

#### [Recognize] SOS Subset Sums (Author exercise)
<!-- id: dp29-sos-subset-sums -->

**Prerequisites.** All three exercises above.

**Problem.** An integer `n` and an array `a` of length `2^n` are given. Return an array `f` of length `2^n` where `f[mask]` is the sum of `a[sub]` over all submasks `sub` of `mask`, including 0 and `mask`.

**Constraints.** The limits are:
- **Size** satisfies `0 <= n <= 16`.
- **Values** satisfy `0 <= a[i] <= 10^6`.
- **Result** is a `long[]`, because a sum can exceed the `int` range.
- **Mutation** is not allowed, so the input array stays unchanged.

**Example 1.** Input `n = 2`, `a = [1, 2, 3, 4]`, output `[1, 3, 4, 10]`.

**Example 2.** Input `n = 3`, `a = [3, 1, 4, 1, 5, 9, 2, 6]`, output `[3, 4, 7, 9, 8, 18, 14, 31]`.

**Hint.** Add the values one bit at a time, so that after layer b the sums cover only changes in bits 0 to b.

**Changed decision.** The query covers every mask at once, so the method adds one bit layer at a time in place of listing submasks for each mask.
