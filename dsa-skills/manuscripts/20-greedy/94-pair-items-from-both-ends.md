<!-- lesson-kind: combination -->
<!-- lesson-id: pair-from-both-ends -->
## Pair Items From Both Ends

<!-- stage: context -->
### Why A Packer Uses Extra Machines

A job packer assigns jobs to worker machines. Each job needs some memory. A machine has a memory limit and runs at most two jobs at once, so a machine holds one job or two jobs whose memory adds up to at most the limit. The operator wants to use as few machines as possible, because each machine costs money by the hour.

A packer that pairs each job with the next job in the queue wastes machines whenever two large jobs sit next to each other. This lesson asks how a program chooses the partner of each job so that the machine count is as small as possible, and how it does so without trying every pairing.

<!-- stage: contributions -->
### What Sorting, Pointers And Proof Each Add

Three earlier ideas combine here. Sorting by memory puts the lightest job at one end of the array and the heaviest at the other. Two pointers, one at each end, give the program the two candidates it cares about in constant time and let it advance either pointer after a decision. The exchange argument gives the reason a decision is safe.

None of them is enough alone. Sorting and pointers without a proof produce a loop that moves pointers by guesswork. A proof without the order has no lightest or heaviest job to talk about. Together, the proof says which pointer may move, the sorted order says what each pointer holds, and the pointers make each step O(1).

<!-- stage: naive -->
### Pairing Neighboring Jobs In Queue Order

The direct plan walks the queue in order. It takes the current job and puts the next job on the same machine when the two fit. Otherwise it runs the current job alone.

```java
static int machinesByNeighbors(int[] memory, int limit) {
    int machines = 0, i = 0;
    while (i < memory.length) {
        if (i + 1 < memory.length && memory[i] + memory[i + 1] <= limit) i += 2;   // pair with the next job
        else i += 1;                                                                // run alone
        machines++;
    }
    return machines;
}
```

```predict
Run the method on `memory = [4, 4, 2, 2]` with `limit = 6`. How many machines does it use, and how few are possible?

It uses 3 machines. The first two jobs of 4 do not fit together, so the first job runs alone. The second job of 4 pairs with the first job of 2, and the last job of 2 runs alone. The best plan pairs each job of 4 with a job of 2 and uses 2 machines.
```

<!-- stage: bottleneck -->
### Counting The Pairings

The neighbor method runs in O(n) time. It is wrong because the neighbor of a job has no special meaning. The partner of a job can be any other job in the queue.

Trying every pairing of `n` jobs takes O(n!) time in the worst case, since each job has many possible partners. A program must decide on a partner without searching. The decision should depend on the memory values alone, and it should hold for every input. Sorting the jobs is cheap, so the open question is which end of the sorted array settles a decision first.

<!-- stage: insight -->
### Settling The Heaviest Job First

#### Why The Heaviest Job Decides First

In sorted order, the heaviest job is the hardest to place. It fits with a partner only if the partner is light enough. The lightest job is the easiest partner for any job. If the heaviest job cannot share a machine with the lightest job, it cannot share with any job, so it runs alone.

#### The Feasible Pair Test

A **feasible pair** is two jobs whose memory adds up to at most the limit. The test compares the heaviest remaining job with the lightest remaining job. If the pair is feasible, the program puts them on one machine and moves both pointers inward. If it is not feasible, the heaviest job runs alone, and only the right pointer moves.

#### Why The Commitment Is Safe

The **endpoint commitment** says that the heaviest job takes the lightest job as a partner whenever the pair is feasible. Take a best plan, and let `h` be the heaviest job and `l` the lightest, with `h + l` at most the limit. In the plan, `h` shares a machine with a job `p` or runs alone, and `l` shares a machine with a job `q` or runs alone. If `h` and `l` already share a machine, nothing changes.

Otherwise, regroup the two machines. Put `h` and `l` on one machine, which is feasible by assumption. Put `p` and `q`, where they exist, on the other machine. That machine is feasible, because `q` is at most `h`, so `p + q` is at most `p + h`, which fits the limit. The plan uses no more machines than before. The **two-end scan** applies the commitment again to the jobs that remain.

<!-- names: feasible pair, endpoint commitment, two-end scan -->

<!-- stage: variables -->
### Pointers For The Two-End Scan

The scan sorts a copy of the array and keeps two pointers and a count. Four items describe the state.

- **weights** is the sorted copy of the memory values.
- **lo** is the index of the lightest job that is not placed.
- **hi** is the index of the heaviest job that is not placed.
- **machines** is the number of machines opened so far.

The loop runs while `lo <= hi`. When `lo == hi`, one job remains, and it runs alone.

<!-- stage: trace -->
### Two Scans From Both Ends

#### Pairing And Running Alone

The first trace sorts the memory values to `[2, 2, 3, 5, 5]` with `limit = 6`. The pointers are `lo` and `hi`.

The heaviest job is 5 and the lightest is 2. The sum 7 passes the limit, so the job 5 runs alone, and `hi` moves left. The same test fails again for the second 5. The jobs 3 and 2 fit together, so one machine holds both and both pointers move. One job of 2 remains with `lo == hi`, and it runs alone. The scan opens four machines.

```trace
{"cells":[2,2,3,5,5],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":4},"vars":{"machines":1},"note":"The sum 2 + 5 is 7, which passes the limit, so the job 5 runs alone and hi moves left."},{"at":{"lo":0,"hi":3},"vars":{"machines":2},"note":"The sum 2 + 5 is 7, which passes the limit, so the job 5 runs alone and hi moves left."},{"at":{"lo":0,"hi":2},"vars":{"machines":3},"note":"The sum 2 + 3 is 5, which fits the limit, so one machine takes both jobs and both pointers move."},{"at":{"lo":1,"hi":1},"vars":{"machines":4},"note":"Only the job 2 remains, so it runs alone."}]}
```

#### Spending Power For Score

A second problem uses the same two ends. A player has some power and a list of tokens. Playing the cheapest token face up costs its value in power and adds one point. Playing the dearest token face down costs one point and adds its value in power. The trace uses the tokens 40, 60, 90, 150 and 400 with power 100.

```trace
{"cells":[40,60,90,150,400],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":4},"vars":{"power":60,"score":1},"note":"The power covers the token 40, so the player plays it face up, and the score becomes 1."},{"at":{"lo":1,"hi":4},"vars":{"power":0,"score":2},"note":"The power covers the token 60, so the player plays it face up, and the score becomes 2."},{"at":{"lo":2,"hi":4},"vars":{"power":400,"score":1},"note":"The token 90 costs too much, so the player plays the token 400 face down. The power becomes 400 and the score drops to 1."},{"at":{"lo":2,"hi":3},"vars":{"power":310,"score":2},"note":"The power covers the token 90, so the player plays it face up, and the score becomes 2."},{"at":{"lo":3,"hi":3},"vars":{"power":160,"score":3},"note":"The power covers the token 150, so the player plays it face up, and the score becomes 3."}]}
```

<!-- stage: code -->
### Scanning From Both Ends

```java
static int machines(int[] memory, int limit) {
    int[] w = memory.clone();
    Arrays.sort(w);
    int lo = 0, hi = w.length - 1, machines = 0;
    while (lo <= hi) {
        if (lo < hi && w[lo] + w[hi] <= limit) lo++;   // the lightest job joins the heaviest job
        hi--;                                           // the heaviest job is placed either way
        machines++;
    }
    return machines;
}
```

The loop places the heaviest job in every round, and it also places the lightest job when the pair is feasible. The condition `lo < hi` stops the method from pairing a job with itself. The sum of two values can pass the `int` range for large weights, so use `(long) w[lo] + w[hi]` when the limits allow values near 2^31.

- **Time** is O(n log n) for the sort, plus O(n) for the scan itself.
- **Space** is O(n) for the sorted copy, or O(1) when the caller allows an in-place sort.

<!-- stage: applicability -->
### When Both Ends Settle The Choice

#### Applying The Invariant

Use this pairing when sorted values let the two ends decide each step, as with pairing under a sum limit, or spending the cheapest and selling the dearest. The invariant is that every item outside the pointers is placed, and a best plan for the items between the pointers still exists. Say which end decides first and why before you move a pointer.

#### Finding Cases That Break The Precondition

A false friend is a two-pointer scan that moves a pointer without a proof. The pointers look the same as in the pair-sum scan of Chapter 08, but a pair-sum scan looks for one pair, and this scan must place every item. A second false friend is a machine that holds three or more items. Then the heaviest item may need two partners, and the two-end argument does not cover it.

#### Avoiding Java Pitfalls

Use `<=` when the sum can equal the limit. Use `(long)` on the sum when values can be large. Keep `lo < hi` in the pairing test, so an item is never paired with itself. Sort a copy when the caller expects its order to stay.

<!-- stage: exercises -->
### Exercises

#### [Build] Assign Cookies (LeetCode 455)
<!-- id: gr-cookies-with-slack -->

**Prerequisites.** Lesson 01 and the pointer scan of this lesson.

**Problem.** Array `g` lists the smallest cookie size that each child accepts, and array `s` lists the cookie sizes. A child also refuses a cookie that is too large. A cookie of size `x` satisfies child `i` when `g[i] <= x <= g[i] + slack`. No child takes two cookies, and no cookie goes to two children. Return the largest number of satisfied children.

**Constraints.** The limits are:
- **Count** is `0 <= g.length, s.length <= 3 * 10^4`.
- **Values** are integers in `1 <= value <= 2^31 - 1`.
- **Slack** is an integer in `0 <= slack <= 2^31 - 1`.
- **Sum** of `g[i] + slack` can pass the `int` range.

**Example 1.** Input `g = [1,2,3]`, `s = [3,1]` and `slack = 0`, output 2.

**Example 2.** Input `g = [2,5]`, `s = [3,4,9]` and `slack = 2`, output 1.

**Hint.** When the cookie is too large for the smallest remaining child, which pointer moves?

**Changed decision.** A child can also reject a cookie that is too large.

#### [Vary] Boats to Save People (LeetCode 881)
<!-- id: gr-boats-to-save-people -->

**Prerequisites.** The previous exercise.

**Problem.** Array `people` holds the weight of each person. A boat carries at most two people, and their weights add up to at most `limit`. Every person weighs at most `limit`. Return the smallest number of boats that carry everyone.

**Constraints.** The limits are:
- **Count** is `0 <= people.length <= 5 * 10^4`.
- **Values** are integers in `1 <= people[i] <= limit <= 3 * 10^4`.
- **Capacity** of a boat is two people.
- **Mutation** of the array is allowed.

**Example 1.** Input `people = [4,4,2,2]` and `limit = 6`, output 2.

**Example 2.** Input `people = [3,5,3,4]` and `limit = 5`, output 4.

**Hint.** Which person can the heaviest remaining person share with, if anyone?

**Changed decision.** The scan pairs the heaviest person with the lightest person only when it fits.

#### [Boundary] Exact Capacity And One Remaining Person (Author exercise)
<!-- id: gr-exact-capacity-single -->

**Prerequisites.** The previous exercise.

**Problem.** The setting is the boat problem. A pair is allowed when the weights add up to at most `limit`, so a sum equal to `limit` is allowed. Return an array `[boats, singles]`. The value `boats` is the smallest number of boats. The value `singles` is the number of boats that carry one person in the plan of the two-end scan. A person left alone when the pointers meet counts once.

**Constraints.** The limits are:
- **Count** is `0 <= people.length <= 5 * 10^4`.
- **Values** are integers in `1 <= people[i] <= limit <= 2^30`.
- **Sum** of two weights can pass the `int` range for the largest limit.
- **Empty** input returns `[0,0]`.

**Example 1.** Input `people = [2,2,3,5,5]` and `limit = 6`, output `[4,3]`.

**Example 2.** Input `people = [3,3]` and `limit = 6`, output `[1,0]`.

**Hint.** What does the scan do when `lo == hi`?

**Changed decision.** Equality is feasible, and the final person is counted once.

#### [Recognize] Bag of Tokens (LeetCode 948)
<!-- id: gr-bag-of-tokens -->

**Prerequisites.** The two-end scan of this lesson.

**Problem.** Array `tokens` holds token values, and `power` is the starting power. The score starts at 0. Playing a token face up needs `power >= token`, costs `token` power and adds 1 score. Playing a token face down needs score at least 1, costs 1 score and adds `token` power. Each token is played at most once. Return the largest score that any play order can reach.

**Constraints.** The limits are:
- **Count** is `0 <= tokens.length <= 1000`.
- **Values** are integers in `0 <= tokens[i], power <= 10^4`.
- **Order** of play is free.
- **Return** is 0 when no token can be played.

**Example 1.** Input `tokens = [40,60,90,150,400]` and `power = 100`, output 3.

**Example 2.** Input `tokens = [200,300]` and `power = 100`, output 0.

**Hint.** Which token should the player spend first, and which should the player sell?

**Changed decision.** The two ends play opposite roles: the cheapest is spent and the dearest is sold.
