<!-- lesson-kind: standard -->
<!-- lesson-id: local-choice -->
## Local Choice

<!-- stage: context -->
### Why Placement Wastes Large Servers

A batch service places jobs onto servers. Each job needs a known amount of memory, and each server has a known amount of free memory. A server runs at most one job. The service must place as many jobs as it can.

The first version walks the jobs in arrival order. Each job takes the first server with enough memory. On one afternoon a small job arrives first and takes the largest server. A large job arrives second and finds no server that fits, so the service places one job when it could have placed two. This lesson asks how a program decides each placement once and never revisits it.

<!-- stage: naive -->
### Placing Jobs In Arrival Order

The direct plan handles the jobs in the order they arrive. For each job it scans the servers from the start and takes the first unused server that has enough memory.

```java
static int placeInArrivalOrder(int[] jobs, int[] servers) {
    boolean[] used = new boolean[servers.length];
    int placed = 0;
    for (int job : jobs) {
        for (int s = 0; s < servers.length; s++) {
            if (!used[s] && servers[s] >= job) {   // first fit
                used[s] = true;
                placed++;
                break;
            }
        }
    }
    return placed;
}
```

```predict
Run the method on `jobs = [3, 8]` and `servers = [9, 4]`. What does it return, and is that the largest possible number of placements?

It returns 1. The job of size 3 takes the server of size 9, because that server comes first. The job of size 8 then finds only the server of size 4, which is too small. The better plan puts the job of size 3 on the server of size 4 and the job of size 8 on the server of size 9, which places 2.
```

<!-- stage: bottleneck -->
### Counting The Cost And The Wrong Answers

The method fails in two ways. The first failure is cost. Each job scans up to `m` servers, so the work grows as O(n * m) for `n` jobs and `m` servers. At `n = m = 100,000` that is ten billion steps.

The second failure is correctness, and it matters more. The method commits each placement without asking what the placement costs later. A fast method with the same rule would still return 1 on the example. A rewrite that only speeds up the scan does not repair the answer. The program needs a rule that makes each commitment safe, so that no later job suffers because of an earlier choice.

<!-- stage: insight -->
### Committing To A Choice That Cannot Hurt

#### Defining The Greedy Choice

A **greedy choice** is a decision that the algorithm commits to at once and never reverses. The algorithm then solves only the smaller problem that remains. Committing early is cheap, because the program never stores alternatives. It is correct only when the choice is proven safe.

#### Proving The Choice Safe

An **exchange argument** proves a choice safe. Take any best answer, and change it step by step so that it contains the chosen move, without making it worse. If that change always works, a best answer that contains the move exists.

For the placement problem, sort the jobs and the servers in increasing order. Let `d` be the smallest remaining job and `r` the smallest remaining server with `r >= d`. The greedy choice places `d` on `r`.

Take a best answer. If it places `d` on some server `r2`, then `r2 >= r`. If `r` serves another job `e`, then `e >= d` and `e <= r <= r2`, so the answer can swap the two and stay valid. If `r` serves no job, the answer can move `d` onto `r`. If `d` is unplaced, the answer can place `d` on `r`, or drop `e` and place `d`. In each case the count does not fall.

#### Dominance Behind The Swap

The swap works because of **dominance**. One option dominates another when it can do everything the other can do. Here the server `r2` dominates `r`, because every job that fits on `r` also fits on `r2`. Spending the smaller server first keeps the dominating one for later.

<!-- names: greedy choice, exchange argument, dominance -->

<!-- stage: variables -->
### Pointers And Counts For One Pass

After both arrays are sorted, the algorithm needs only two positions and a count. Four items describe the state.

- **jobs** is the array of memory demands, sorted in increasing order.
- **servers** is the array of free memory sizes, sorted in increasing order.
- **i** is the index of the smallest job that is not yet placed.
- **j** is the index of the smallest server that the algorithm has not yet used or discarded.
- **placed** is the number of jobs placed so far, and it equals `i`.

Sorting the arrays needs a stated order. This lesson sorts in increasing order with the natural order of `int`.

<!-- stage: trace -->
### Two Passes Over Sorted Arrays

#### A Pass With No Waste

The first trace uses `jobs = [3, 8, 5]` and `servers = [9, 4, 6]`. After sorting, the jobs are 3, 5 and 8, and the servers are 4, 6 and 9. The cells are the servers, and the pointer `j` marks the current server.

At `j = 0` the job of size 3 fits on the server of size 4, so the pass places it. At `j = 1` the job of size 5 fits on the server of size 6. At `j = 2` the job of size 8 fits on the server of size 9. The pass places all three jobs.

```trace
{"cells":[4,6,9],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"i":1,"placed":1},"note":"The server of size 4 fits the job of size 3, so the pass places the job and moves to the next job."},{"at":{"j":1},"vars":{"i":2,"placed":2},"note":"The server of size 6 fits the job of size 5, so the pass places the job and moves to the next job."},{"at":{"j":2},"vars":{"i":3,"placed":3},"note":"The server of size 9 fits the job of size 8, so the pass places the job and moves to the next job."}]}
```

#### A Pass That Discards Servers

The second trace uses `jobs = [5, 6]` and `servers = [1, 2, 5, 7]`. The servers of size 1 and 2 are smaller than the smallest remaining job. No later job is smaller, so each of them is useless forever. The pass discards them and moves `j` forward without placing a job.

```trace
{"cells":[1,2,5,7],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"i":0,"placed":0},"note":"The server of size 1 is smaller than the job of size 5, so the pass discards it and moves on."},{"at":{"j":1},"vars":{"i":0,"placed":0},"note":"The server of size 2 is smaller than the job of size 5, so the pass discards it and moves on."},{"at":{"j":2},"vars":{"i":1,"placed":1},"note":"The server of size 5 fits the job of size 5, so the pass places the job and moves to the next job."},{"at":{"j":3},"vars":{"i":2,"placed":2},"note":"The server of size 7 fits the job of size 6, so the pass places the job and moves to the next job."}]}
```

<!-- stage: code -->
### Matching Sorted Jobs To Sorted Servers

```java
static int placeSmallestFirst(int[] jobs, int[] servers) {
    int[] jobsSorted = jobs.clone();
    int[] serversSorted = servers.clone();
    Arrays.sort(jobsSorted);
    Arrays.sort(serversSorted);
    int i = 0;
    for (int j = 0; j < serversSorted.length && i < jobsSorted.length; j++) {
        if (serversSorted[j] >= jobsSorted[i]) i++;   // place job i on server j
    }
    return i;
}
```

The method clones both arrays before it sorts, so the caller keeps its original order. The loop advances `j` on every step and advances `i` only on a placement. A discarded server therefore costs one step and no job.

- **Time** is O(n log n + m log m), because the sorts dominate the single pass of O(n + m).
- **Space** is O(n + m) for the two copies, or O(1) extra when the caller allows in-place sorting.

<!-- stage: applicability -->
### Checking That A Choice Is Safe

#### Applying The Invariant

Use a greedy choice when one decision must be final and a smaller version of the same problem remains. The invariant of this lesson is that after every commitment a best completion of the remaining jobs and servers still exists. State it in one sentence before you code. If you cannot argue that sentence with a swap, the choice is only a guess.

#### Finding Cases That Break The Precondition

A false friend of this method is picking the largest immediate reward. A job that earns more money does not dominate a job that is smaller, so the largest reward can block several smaller ones. The first-fit method above is also a false friend, because first in arrival order is not an order that dominates.

#### Avoiding Java Pitfalls

Sort a copy when the caller expects the input order to stay. Use `Integer.compare` in comparators and never subtract values, because subtraction overflows for large `int` values. Use `long` for a total that can pass 2,147,483,647.

<!-- stage: exercises -->
### Exercises

#### [Build] Smallest Sufficient Match (Author exercise)
<!-- id: gr-smallest-sufficient-match -->

**Prerequisites.** The pointer pass of this lesson.

**Problem.** Arrays `demands` and `supplies` are both sorted in non-decreasing order. A supply of size `s` can serve a demand of size `d` when `s >= d`. Each supply serves at most one demand, and each demand receives at most one supply. Return the largest number of demands that can be served.

**Constraints.** The limits are:
- **Count** is `0 <= demands.length, supplies.length <= 10^5`.
- **Values** are integers in `1 <= value <= 10^9`.
- **Order** is non-decreasing for both arrays.
- **Mutation** does not occur.

**Example 1.** Input `demands = [3,8]` and `supplies = [4,9]`, output 2.

**Example 2.** Input `demands = [5,6]` and `supplies = [1,2,5,7]`, output 2.

**Hint.** Which supply is safe to give to the smallest remaining demand?

**Changed decision.** The arrays arrive sorted, so the method needs no sort.

#### [Vary] Assign Cookies (LeetCode 455)
<!-- id: gr-assign-cookies -->

**Prerequisites.** The previous exercise and sorting from Chapter 05.

**Problem.** Array `g` holds the minimum size each child accepts. Array `s` holds the sizes of the cookies. A cookie of size `x` satisfies a child `i` when `x >= g[i]`. Each child receives at most one cookie, and each cookie goes to at most one child. Return the largest number of satisfied children.

**Constraints.** The limits are:
- **Count** is `0 <= g.length, s.length <= 3 * 10^4`.
- **Values** are integers in `1 <= value <= 2^31 - 1`.
- **Order** is arbitrary.
- **Mutation** of the input arrays is allowed.

**Example 1.** Input `g = [1,2,3]` and `s = [1,1]`, output 1.

**Example 2.** Input `g = [10,9,8,7]` and `s = [5,6,7,8]`, output 2.

**Hint.** What must be true about both arrays before a single pass works?

**Changed decision.** Neither array arrives sorted, so the method sorts first.

#### [Boundary] Unusable Resources (Author exercise)
<!-- id: gr-unusable-resources -->

**Prerequisites.** The first exercise.

**Problem.** The arrays `demands` and `supplies` arrive sorted in non-decreasing order. Run the smallest-first pass: for the smallest remaining demand, discard every supply that is smaller than it, then pair the next supply with it. Return the number of supplies that the pass discards before the pass ends. A supply that stays unread after the last demand is served is not discarded.

**Constraints.** The limits are:
- **Count** is `0 <= demands.length, supplies.length <= 10^5`.
- **Values** are integers in `1 <= value <= 10^9`.
- **Order** is non-decreasing for both arrays.
- **Empty** inputs are allowed and return 0.

**Example 1.** Input `demands = [5,6]` and `supplies = [1,2,5,7]`, output 2.

**Example 2.** Input `demands = [4]` and `supplies = [1,2,3]`, output 3.

**Hint.** When the supplies run out first, which supplies were discarded?

**Changed decision.** The method counts discarded supplies and not served demands.

#### [Recognize] Lemonade Change (LeetCode 860)
<!-- id: gr-lemonade-change -->

**Prerequisites.** The exchange argument of this lesson.

**Problem.** A stand sells items for 5. Array `bills` lists the payments in order, and each payment is 5, 10 or 20. The stand starts with no bills and must give back the exact difference. Return true if every customer receives the correct change, and false otherwise.

**Constraints.** The limits are:
- **Count** is `0 <= bills.length <= 10^5`.
- **Values** are 5, 10 or 20.
- **Order** is the order of arrival and cannot change.
- **Return** is a boolean.

**Example 1.** Input `bills = [5,5,5,10,20]`, output true.

**Example 2.** Input `bills = [10,10]`, output false.

**Hint.** When a 20 arrives, which bills could pay the 15, and which bill is more useful later?

**Changed decision.** The order is fixed, so the choice is which bills to hand back.
