<!-- lesson-kind: standard -->
<!-- lesson-id: integer-answers -->
## Integer Answers

<!-- stage: context -->
### A Print Shop Renting A Press

A print shop has a stack of jobs to finish before it closes in nine hours. The press can be rented at any whole number of pages per hour, and a faster press costs more, so the owner wants the slowest speed that still gets everything done. There is a catch in how the press works: during one hour it works on a single job only. If a job has fewer pages left than the press can print in an hour, the rest of that hour is wasted, and the next job starts at the next hour.

The owner has no formula for the best speed. She can, however, take any proposed speed and work out by hand how many hours the whole stack would need: for each job, divide its pages by the speed and round up, then add the results. If the total is within nine hours the speed is good enough, and if not, it is too slow. Checking one speed takes one pass over the jobs.

<!-- stage: naive -->
### Try Each Speed From The Slowest Up

The direct approach is to try the speeds one after another, starting at one page an hour, until a speed finishes in time.

```java
static int slowestSpeedByTrying(int[] jobs, int hours) {
    int fastest = 0;
    for (int pages : jobs) fastest = Math.max(fastest, pages);
    for (int speed = 1; speed <= fastest; speed++) {
        long needed = 0;
        for (int pages : jobs) needed += (pages + speed - 1) / speed;
        if (needed <= hours) return speed;
    }
    return fastest;
}
```

It returns the smallest speed that works for any jobs, because it checks the speeds in increasing order.

<!-- stage: bottleneck -->
### One Full Pass For Every Speed

For each candidate speed the loop makes a pass over all the jobs, so the cost is the number of candidate speeds times the number of jobs, O(S n), where S is the largest job size. With jobs of up to a billion pages, S is a billion, and even a handful of jobs takes far too long. Most of that work is wasted, because the answer to each check carries information about all the other speeds.

A speed that works lets every faster speed work too, since a faster press never needs more hours. A speed that fails means every slower speed fails. The speeds therefore split into a slow stretch where the check fails and a fast stretch where it passes, with a single boundary between them. The boundary can be found with O(log S) checks, each costing O(n), so O(n log S) in total.

<!-- stage: insight -->
### Search The Space Of Answers

The array being searched is not an array of data. It is the **answer space**, the range of whole numbers that might be the answer, here the speeds from 1 up to the largest job. What makes binary search legal is not the input but the **feasibility check**: a function that takes a candidate answer and says whether it works. If feasibility is monotone, so that a feasible candidate stays feasible for every larger one, the candidates form a stretch of failures followed by a stretch of successes, and the answer is the first success.

The result is the **minimum feasible** value, found with the half-open pattern of the first-true lesson. The interval is `[lo, hi]` with `lo` the smallest candidate and `hi` a value known to be feasible. At each step test `mid`. If it is feasible, the answer is `mid` or smaller, so `hi = mid`. If it is not, the answer is larger, so `lo = mid + 1`. The loop runs while `lo < hi`. The invariant is that every candidate below `lo` is proved infeasible and `hi` is feasible, so the answer is in `[lo, hi]`.

<!-- names: answer space, feasibility check, minimum feasible -->

The work of a problem like this is in two places. The first is choosing the bounds, because the loop needs a value that is certainly feasible at the top and a value that cannot be too large at the bottom. The second is writing the check so that its cost is one pass and its arithmetic cannot overflow: the sum of hours can exceed `int`, so it is held in a `long`.

The same pattern covers several problems with different checks. Shipping packages in order within a number of days asks for the smallest capacity, and the check is a greedy loading that starts a new day whenever the next package does not fit. Making bouquets needs the earliest day on which enough adjacent flowers have bloomed, and the check counts runs. Splitting an array into parts with the smallest possible largest sum asks for the smallest allowed part sum, and the check greedily cuts a new part whenever the running sum would pass the limit.

<!-- stage: variables -->
### Bounds, Candidate And Count

`lo` and `hi` are the smallest and largest candidates still possible. `mid` is the candidate under test, and it is always a whole number between them. The feasibility check receives `mid` and returns a boolean, and while it runs it keeps a counter, hours or days or parts, in a `long`. The bounds come from the problem: for speeds the lowest is one and the highest is the largest job, and for capacities the lowest is the heaviest package and the highest is the sum of all packages. Anything that makes the demand impossible must be detected before the loop.

<!-- stage: trace -->
### Testing Speeds Until The Boundary

The first trace finds the slowest press speed for jobs of 3, 6, 7 and 11 pages with a limit of eight hours. The candidates are the speeds one to eleven. The first test of speed 6 needs six hours, which is within the limit, so the upper edge comes down to 6. The step to study is the second: speed 3 needs ten hours and fails, so every speed up to 3 fails, and the lower edge jumps to 4.

```trace
{"cells":["1","2","3","4","5","6","7","8","9","10","11"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":10,"mid":5},"vars":{"speed":6,"hours":6},"note":"Try speed 6. The jobs need 6 hours, within the limit of 8, so the answer is 6 or slower and hi comes down to speed 6."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"speed":3,"hours":10},"note":"Try speed 3. The jobs need 10 hours, over the limit of 8, so every speed up to 3 fails and lo moves to speed 4."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"speed":5,"hours":8},"note":"Try speed 5. The jobs need 8 hours, within the limit of 8, so the answer is 5 or slower and hi comes down to speed 5."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"speed":4,"hours":8},"note":"Try speed 4. The jobs need 8 hours, within the limit of 8, so the answer is 4 or slower and hi comes down to speed 4."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"answer":4},"note":"The edges meet at speed 4, the slowest speed that finishes in time."}]}
```

The second trace splits 7, 2, 5, 10, 8 into two parts and searches for the smallest allowed part sum, between the largest element 10 and the total 32. Each test cuts greedily and counts parts. The step to study is the closing one: the edges meet at the smallest sum for which two parts are enough.

```trace
{"cells":["10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":22,"mid":11},"vars":{"limit":21,"parts":2},"note":"Try a limit of 21. Greedy cutting needs 2 parts, which is at most 2, so hi comes down to 21."},{"at":{"lo":0,"hi":11,"mid":5},"vars":{"limit":15,"parts":3},"note":"Try a limit of 15. Greedy cutting needs 3 parts, more than 2, so lo moves to 16."},{"at":{"lo":6,"hi":11,"mid":8},"vars":{"limit":18,"parts":2},"note":"Try a limit of 18. Greedy cutting needs 2 parts, which is at most 2, so hi comes down to 18."},{"at":{"lo":6,"hi":8,"mid":7},"vars":{"limit":17,"parts":3},"note":"Try a limit of 17. Greedy cutting needs 3 parts, more than 2, so lo moves to 18."},{"at":{"lo":8,"hi":8,"mid":-1},"vars":{"answer":18},"note":"The edges meet at 18, the smallest limit that needs at most 2 parts."}]}
```

<!-- stage: code -->
### Four Checks Over One Search

```java
static int minEatingSpeed(int[] piles, int h) {
    int lo = 1, hi = 0;
    for (int p : piles) hi = Math.max(hi, p);
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        long hours = 0;
        for (int p : piles) hours += (p + mid - 1) / mid;
        if (hours <= h) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int shipWithinDays(int[] weights, int days) {
    int lo = 0, hi = 0;
    for (int w : weights) { lo = Math.max(lo, w); hi += w; }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int used = 1, load = 0;
        for (int w : weights) {
            if (load + w > mid) { used++; load = 0; }
            load += w;
        }
        if (used <= days) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int minDays(int[] bloomDay, int m, int k) {
    if ((long) m * k > bloomDay.length) return -1;
    int lo = Integer.MAX_VALUE, hi = 0;
    for (int d : bloomDay) { lo = Math.min(lo, d); hi = Math.max(hi, d); }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int bouquets = 0, run = 0;
        for (int d : bloomDay) {
            if (d <= mid) { if (++run == k) { bouquets++; run = 0; } }
            else run = 0;
        }
        if (bouquets >= m) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int splitArray(int[] nums, int parts) {
    int lo = 0, hi = 0;
    for (int x : nums) { lo = Math.max(lo, x); hi += x; }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int used = 1, sum = 0;
        for (int x : nums) {
            if (sum + x > mid) { used++; sum = 0; }
            sum += x;
        }
        if (used <= parts) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

Each search runs O(log R) turns, where R is the size of the answer space, and each turn is one O(n) pass, so the cost is O(n log R) time with O(1) extra space. The impossible case for bouquets is rejected up front with a `long` product, since the loop would otherwise return a day that does not satisfy the demand.

<!-- stage: applicability -->
### When Answers Can Be Tested

Use search over the answer space when the answer is a whole number in a known range, a candidate can be tested in one pass, and feasibility is monotone: larger is easier, or smaller is easier, consistently. The invariant is the pair of facts about the edges: everything below `lo` has been proved infeasible, and `hi` is feasible. State why the check is monotone before coding, since that proof is the whole reason the search is legal.

A false friend is the thought that binary search needs a sorted array. Here the input array may be in any order, and what is searched is the range of candidate answers. Another false friend is a check that is not monotone: asking for an answer that makes some count equal to a value, instead of at most or at least, breaks the property. A third is searching without first checking that some answer exists, which returns a bound that is not an answer.

In Java, keep counters in a `long` when the sum of per-item costs can pass the range of `int`. Start the lower bound at the smallest value that could possibly work, not at zero, when zero would divide by zero or be meaningless. Return the lower edge at the end, and test the impossible case before the loop, not after it.

<!-- stage: exercises -->
### Exercises

#### [Build] Koko Eating Bananas (LeetCode 875)
<!-- id: bs-koko-speed -->

**Prerequisites.** The first-true lesson, and ceiling division by integers.

**Problem.** There are piles of bananas and a limit of `h` hours. Each hour Koko picks one pile and eats up to `k` bananas from it, wasting any leftover time in that hour. Return the smallest whole `k` that finishes all piles within `h` hours.

**Constraints.** 1 <= piles.length <= 10000, piles.length <= h <= 1000000000, and 1 <= piles[i] <= 1000000000. Hours needed may exceed the `int` range.

**Example 1.** Input `piles = [5, 9, 14, 20], h = 9`, output 7.

**Example 2.** Input `piles = [4, 4, 4], h = 3`, output 4.

**Hint.** If a speed finishes in time, what can you say about any faster speed? What are the smallest and largest speeds worth trying?

**Changed decision.** First rung: the searched array is the range of speeds, and a pass over the piles is the test.

#### [Vary] Capacity To Ship Packages Within D Days (LeetCode 1011)
<!-- id: bs-ship-capacity -->

**Prerequisites.** The Koko exercise above.

**Problem.** Packages must be shipped in the given order, and each day the ship carries a prefix of the remaining packages up to its capacity. Return the smallest capacity that ships all packages within `days` days.

**Constraints.** 1 <= days <= weights.length <= 50000 and 1 <= weights[i] <= 500. The ship cannot split a package, so the capacity is at least the heaviest package.

**Example 1.** Input `weights = [4, 8, 3, 9, 6, 5], days = 3`, output 12.

**Example 2.** Input `weights = [2, 2, 2], days = 3`, output 2.

**Hint.** What are the smallest and largest capacities that could be the answer? How does a greedy loading decide when to start a new day?

**Changed decision.** The test changes from a sum of ceilings to a greedy loading, while the search for the minimum feasible value stays the same.

#### [Boundary] Minimum Number of Days to Make m Bouquets (LeetCode 1482)
<!-- id: bs-bouquet-days -->

**Prerequisites.** The two exercises above.

**Problem.** Flower `i` blooms on day `bloomDay[i]`. A bouquet needs `k` adjacent flowers that have all bloomed, and each flower is used in at most one bouquet. Return the earliest day on which `m` bouquets can be made, or minus one if that is impossible. Detect the impossible demand before searching.

**Constraints.** 1 <= bloomDay.length <= 100000, 1 <= bloomDay[i] <= 1000000000, and 1 <= m, k <= 1000000. The product m times k can exceed the `int` range.

**Example 1.** Input `bloomDay = [4, 9, 2, 9, 9, 3, 9], m = 2, k = 2`, output 9.

**Example 2.** Input `bloomDay = [4, 9, 2, 9, 9, 3, 9], m = 3, k = 3`, output -1.

**Hint.** How many flowers do `m` bouquets need in total? What does the check count, and what resets a run of bloomed flowers?

**Changed decision.** The demand may be impossible regardless of the day, so a guard before the search is part of the contract.

#### [Recognize] Split Array Largest Sum (LeetCode 410)
<!-- id: bs-split-array-largest-sum -->

**Prerequisites.** All three exercises above.

**Problem.** Split an array of non-negative integers into `k` non-empty contiguous parts so that the largest part sum is as small as possible, and return that sum. Search the allowed part sum and count the parts a greedy cutting needs.

**Constraints.** 1 <= nums.length <= 1000, 0 <= nums[i] <= 1000000, and 1 <= k <= nums.length. The sum of all elements fits in an `int` for these limits.

**Example 1.** Input `nums = [3, 9, 1, 4, 6, 2], k = 3`, output 12.

**Example 2.** Input `nums = [5, 5], k = 1`, output 10.

**Hint.** What are the smallest and largest possible values of the answer? Why does a greedy cut count the fewest parts for a given limit?

**Changed decision.** The unknown is a maximum allowed part sum, so the test is a greedy partition count compared with `k`.
