<!-- lesson-kind: standard -->
<!-- lesson-id: integer-answers -->
## Search Whole Number Answers

<!-- stage: context -->
### Choosing A Speed Without Testing Every Speed

A warehouse robot must move four stacks of crates with 5, 9, 14 and 20 crates. It lifts at a fixed speed of `k` crates per hour from one stack at a time, and it finishes a stack before it starts the next. The shift lasts 9 hours. In each hour the robot works on one stack only, so unused lifting capacity in that hour is lost. A lower speed wears the motor less, so the planner wants the smallest whole speed that still finishes in time.

There is no sorted array of answers to look at. The planner could try speed 1, then 2, then 3, and keep going until a speed works. With stacks of millions of crates, that is millions of full simulations. The question is whether the speeds themselves can be searched, even though no array holds them.

<!-- stage: naive -->
### Trying Every Speed In Order

The direct method tries each speed from 1 upward. For each speed it adds up the hours the robot needs for every stack and stops at the first speed whose total fits in the shift.

```java
static int slowestSpeedByScan(int[] stacks, int hours) {
    int speed = 1;
    while (true) {
        long used = 0;
        for (int crates : stacks) {
            used += (crates + speed - 1) / speed;
        }
        if (used <= hours) return speed;
        speed++;
    }
}
```

For `{5, 9, 14, 20}` and 9 hours, speed 6 needs 1 + 2 + 3 + 4 = 10 hours and fails. Speed 7 needs 1 + 2 + 2 + 3 = 8 hours and the method returns 7.

```predict
Speed 7 finishes in time. Without simulating, can speed 8 finish in time, and can speed 6 be proved to fail from the result for speed 7 alone?

Speed 8 finishes in time, because a higher speed never needs more hours for any stack. The result for speed 7 does not decide speed 6 by itself. The successes form one block of higher speeds, so any failures lie below the block.
```

<!-- stage: bottleneck -->
### Each Speed Repeats A Full Simulation

A scan tries up to `m` speeds, where `m` is the largest stack. Each try reads all `n` stacks, so the total cost is O(n * m). For `m` near 10^9 the loop cannot finish.

The prediction shows where the waste lies. After one speed fails, every lower speed also fails, yet the scan simulates each lower speed on its own. After one speed passes, every higher speed also passes. The scan discards one speed per simulation, although each simulation proves a fact about a whole side of the number line.

<!-- stage: insight -->
### Binary Search Over The Answer Range

The answer is a whole number between two limits, so the numbers between the limits form a sorted sequence, even though no array stores them. Each number gets a yes or no verdict from a simulation, and the verdicts never flip back.

<!-- names: feasibility check, answer range, smallest feasible value -->

#### The Feasibility Check

A **feasibility check** is a function that takes one candidate value and answers whether the task succeeds under that value. Here it simulates the shift at speed `k` and compares the hours used with the limit. The check must be monotone. If the candidate `k` passes, every larger candidate passes, and if `k` fails, every smaller candidate fails. This is the false-to-true shape of the first-true lesson, with the candidate value in place of an array index.

#### The Answer Range

The **answer range** is the closed interval `[lo, hi]` of candidates that may still be the answer. Its first value is the lowest speed that could ever work, here 1. Its last value is a candidate that is certain to pass, here the largest stack, because that speed finishes every stack in one hour and uses `n` hours. The number of stacks `n` is at most the hour budget `h`. The search never reads an array of candidates. It computes `mid = lo + (hi - lo) / 2` and calls the check.

#### The Smallest Feasible Value

The search returns the **smallest feasible value**, the lowest candidate whose check passes. When `mid` passes, it may be the answer, so `hi = mid`. When `mid` fails, it cannot be the answer, so `lo = mid + 1`. The loop runs while `lo < hi` and ends with `lo == hi`, which is the smallest passing candidate. The search makes O(log m) checks, and each costs O(n), so the total is O(n log m).

<!-- stage: variables -->
### The Range And The Check

The loop keeps four values: two candidates, a midpoint and a check.

- **lo** is the lowest candidate that may still pass.
- **hi** is a candidate that is known to pass, and it only moves down.
- **mid** is `lo + (hi - lo) / 2`, which stays below `hi` when `lo < hi`.
- **feasible(mid)** is the monotone check, written as a method that reads the input and never changes it.

The two limits are chosen once, before the loop, and the proof that `hi` passes is part of the setup. A wrong `hi` that fails the check makes the loop return a failing value.

<!-- stage: trace -->
### Two Searches Over Answer Ranges

#### Speeds For Four Stacks

The stacks are `{5, 9, 14, 20}` and the shift is 9 hours. The cells below are the candidate speeds 1 to 20, so index `i` holds the speed `i + 1`. The first midpoint is speed 10, which needs 1 + 1 + 2 + 2 = 6 hours and passes, so `hi` becomes speed 10. The next midpoint is speed 5, which needs 1 + 2 + 3 + 4 = 10 hours and fails, so `lo` becomes speed 6. Speed 8 passes, speed 7 passes and speed 6 fails, and the range closes on speed 7.

```trace
{"cells":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":19,"mid":-1},"vars":{},"note":"Start with every candidate, speeds 1 to 20."},{"at":{"lo":0,"hi":19,"mid":9},"vars":{"candidate":"10","passes":"yes"},"note":"Speed 10 needs 6 hours and passes, so hi moves to 10."},{"at":{"lo":0,"hi":9,"mid":4},"vars":{"candidate":"5","passes":"no"},"note":"Speed 5 needs 10 hours and fails, so lo moves to 6."},{"at":{"lo":5,"hi":9,"mid":7},"vars":{"candidate":"8","passes":"yes"},"note":"Speed 8 needs 8 hours and passes, so hi moves to 8."},{"at":{"lo":5,"hi":7,"mid":6},"vars":{"candidate":"7","passes":"yes"},"note":"Speed 7 needs 8 hours and passes, so hi moves to 7."},{"at":{"lo":5,"hi":6,"mid":5},"vars":{"candidate":"6","passes":"no"},"note":"Speed 6 needs 10 hours and fails, so lo moves to 7."},{"at":{"lo":6,"hi":6,"mid":6},"vars":{"answer":"7"},"note":"The range holds one candidate, 7, so the search returns it."}]}
```

#### Capacities For Six Packages

The package weights are `{4, 2, 7, 1, 5, 3}` and the limit is 3 loading days, with packages loaded in order. The cells are the capacities 7 to 26, because a capacity below the heaviest package 7 cannot carry it, and a capacity of 22 carries all packages in one day. Capacity 16 needs 2 days and passes, and capacities 11, 9 and 8 each need 3 days and pass. Capacity 7 needs 4 days and fails, so the range closes on capacity 8.

```trace
{"cells":[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":19,"mid":-1},"vars":{},"note":"Start with every candidate, capacities 7 to 26."},{"at":{"lo":0,"hi":19,"mid":9},"vars":{"candidate":"16","passes":"yes"},"note":"Capacity 16 needs 2 days and passes, so hi moves to 16."},{"at":{"lo":0,"hi":9,"mid":4},"vars":{"candidate":"11","passes":"yes"},"note":"Capacity 11 needs 3 days and passes, so hi moves to 11."},{"at":{"lo":0,"hi":4,"mid":2},"vars":{"candidate":"9","passes":"yes"},"note":"Capacity 9 needs 3 days and passes, so hi moves to 9."},{"at":{"lo":0,"hi":2,"mid":1},"vars":{"candidate":"8","passes":"yes"},"note":"Capacity 8 needs 3 days and passes, so hi moves to 8."},{"at":{"lo":0,"hi":1,"mid":0},"vars":{"candidate":"7","passes":"no"},"note":"Capacity 7 needs 4 days and fails, so lo moves to 8."},{"at":{"lo":1,"hi":1,"mid":1},"vars":{"answer":"8"},"note":"The range holds one candidate, 8, so the search returns it."}]}
```

<!-- stage: code -->
### The Search Over Candidates In Java

```java
static int slowestSpeed(int[] stacks, int hours) {
    int lo = 1, hi = 0;
    for (int crates : stacks) hi = Math.max(hi, crates);
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (hoursNeeded(stacks, mid) <= hours) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static long hoursNeeded(int[] stacks, int speed) {
    long used = 0;
    for (int crates : stacks) used += (crates + speed - 1) / speed;
    return used;
}
```

The method `hoursNeeded` returns a `long`, because the sum of many large stacks divided by a small speed can exceed the range of an `int`. The expression `(crates + speed - 1) / speed` rounds up, and it can overflow when `crates` is near `Integer.MAX_VALUE`, so inputs in the exercises stay below 10^9.

<!-- stage: applicability -->
### When To Search The Answer

#### The Invariant

The invariant is that `hi` always passes the check and every candidate below `lo` fails it. Setup establishes it, because `hi` is the largest stack and no candidate lies below 1, so the claim is true at the start. Each update keeps it, because a passing `mid` becomes the new `hi` and a failing `mid` raises `lo` past a candidate that fails. When `lo == hi`, one candidate is both the lowest possible and a passing one.

#### The False Friend

Binary search applies to the ordered answer range, and the input array has nothing to do with it. The stacks are not sorted, and sorting them would change nothing. A reader who looks for sorted input will not see the search. The reliable cue is a question of the form "the smallest `x` such that a task succeeds", paired with a task whose success never reverses when `x` grows.

#### When The Check Is Not Monotone

If a larger candidate can fail after a smaller one passes, the search discards a side that holds the answer. Check monotonicity before writing the loop. State the reason in one sentence, such as "more capacity never needs more days". If no such sentence holds, the pattern does not apply.

<!-- stage: exercises -->
### Exercises

#### [Build] Eating Speed For All Piles (LeetCode 875)
<!-- id: bs-int-eating-speed -->

**Prerequisites.** The lesson Find The First True Value and the answer range of this lesson.

**Problem.** An array `piles` holds the number of items in each pile, and an integer `h` is the number of available hours. In each hour, a worker chooses one pile and removes `min(k, remaining)` items from it, where `k` is a fixed integer speed. Return the smallest integer `k` such that all piles are emptied within `h` hours.

**Constraints.** The limits are:
- **Length** is `1 <= piles.length <= 10000`.
- **Pile size** is `1 <= piles[i] <= 10^9`.
- **Hours** satisfy `piles.length <= h <= 10^9`.
- **Mutation** does not occur; `piles` does not change.

**Example 1.** Input `piles = [5,9,14,20]` and `h = 9`, output 7.

**Example 2.** Input `piles = [4,4,4]` and `h = 3`, output 4.

**Hint.** What speed is certain to work? Which direction does a failing speed point?

**Changed decision.** Basic case: the search runs over speeds, and the feasibility check sums rounded-up hours.

#### [Vary] Capacity For Shipping In Order (LeetCode 1011)
<!-- id: bs-int-ship-capacity -->

**Prerequisites.** The previous exercise.

**Problem.** An array `weights` lists packages in the order they must be shipped, and an integer `days` is the deadline. Each day the ship loads consecutive packages whose total weight does not exceed the ship capacity `c`. Return the smallest integer `c` such that all packages ship within `days` days.

**Constraints.** The limits are:
- **Length** is `1 <= weights.length <= 50000`.
- **Weight** is `1 <= weights[i] <= 500`.
- **Days** satisfy `1 <= days <= weights.length`.
- **Order** of the packages is fixed and cannot change.

**Example 1.** Input `weights = [4,2,7,1,5,3]` and `days = 3`, output 8.

**Example 2.** Input `weights = [4,2,7,1,5,3]` and `days = 1`, output 22.

**Hint.** The lower limit is the heaviest package, and the upper limit is the total weight. A greedy pass counts days for a given capacity.

**Changed decision.** The check is a greedy pass that counts days, and the lower limit of the range is no longer 1.

#### [Boundary] Days To Make Bouquets (LeetCode 1482)
<!-- id: bs-int-bouquets -->

**Prerequisites.** The previous exercises.

**Problem.** An array `bloomDay` gives the day on which each flower in a row blooms. A bouquet takes `k` adjacent flowers that have all bloomed, and each flower serves in at most one bouquet. Return the smallest day by which `m` bouquets can be made, or `-1` when no day suffices.

**Constraints.** The limits are:
- **Length** is `1 <= bloomDay.length <= 100000`.
- **Day** values satisfy `1 <= bloomDay[i] <= 10^9`.
- **Demand** satisfies `1 <= m` and `1 <= k`, and `m * k` may exceed the `int` range.
- **Answer** is a day number or `-1`.

**Example 1.** Input `bloomDay = [7,3,9,3,7,8,3]`, `m = 2` and `k = 3`, output 9.

**Example 2.** Input `bloomDay = [7,3,9,3,7]`, `m = 2` and `k = 3`, output -1.

**Hint.** Compare `m * k` with the number of flowers using `long` before any search starts. What range of days do the candidates cover?

**Changed decision.** Some inputs have no feasible candidate at all, so a test of total demand comes before the search.

#### [Recognize] Split Into Smallest Largest Sum (LeetCode 410)
<!-- id: bs-int-split-array -->

**Prerequisites.** All exercises above.

**Problem.** Given an array `nums` of non-negative integers and an integer `k`, split `nums` into `k` non-empty contiguous parts. Return the smallest possible value of the largest part sum over all such splits.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 1000`.
- **Values** satisfy `0 <= nums[i] <= 10^6`.
- **Parts** satisfy `1 <= k <= nums.length`.
- **Answer** fits in an `int`.

**Example 1.** Input `nums = [4,9,3,8,6]` and `k = 3`, output 13.

**Example 2.** Input `nums = [4,9,3,8,6]` and `k = 5`, output 9.

**Hint.** Fix a limit on the part sum and count how few parts a greedy pass needs. Fewer than `k` parts can always be split further.

**Changed decision.** The candidate is a ceiling on part sums, and the check counts parts, which only has to be at most `k`.
