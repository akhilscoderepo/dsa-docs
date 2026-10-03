<!-- lesson-kind: combination -->
<!-- lesson-id: index-state-and-floyd -->
## Index State And Floyd

<!-- stage: context -->
### A Paper Chase Through The Gym Lockers

A school sports club runs a paper chase through its changing room. There is a row of lockers numbered 1 to n, and the coach's own locker is numbered 0. Every locker holds a folded slip with one locker number written on it, and the slip says where to go next. No slip says 0, so nobody is ever sent back to the coach. The coach has stuffed n + 1 slips into the lockers, and some locker number appears on two different slips, because two lockers send the runner to the same place.

A club member who starts at the coach's locker and keeps obeying the slips will walk for ever, and the coach wants a full report instead of a single number. She wants the shared locker, the number of steps from her own locker before the walk first arrives at it, and the number of lockers in the loop that the walk then circles. The slips are laminated and may not be altered, and the report must come from a walk that carries almost nothing, because the members run the chase with empty pockets.

<!-- stage: contributions -->
### What Each Part Brings

The array representation brings the next-step rule. Because there are n + 1 stored values, each between 1 and n, every cell names a cell that exists, and index 0 can never be named. That promise turns a plain array into a graph where every place has exactly one successor, so a walk from index 0 is always legal and always ends up in a loop. The representation alone says nothing about the loop, it only lets a walk be taken, and a walk that never ends gives no answer by itself.

Floyd's idea brings the loop detection. Two walkers at different speeds meet inside the loop, and a restart from the beginning lands both on the loop's first place, using a handful of integers. Floyd's idea alone needs a successor function to apply, and a bare array does not promise one, since a value of 0 or n + 2 would send a walker out of the array or back to the start. Each part removes the uncertainty that the other cannot: the representation says that a next place always exists, and the two phases say how to find the loop without remembering the path.

The recognition cue is a read-only array whose values are legal indices of itself, with a promise that some value occurs twice.

<!-- stage: naive -->
### Write Down Each First Visit

The straightforward way to produce the full report is to walk from the coach's locker and write the step number on a sheet with one line per locker, the first time each locker is reached. When the walk reaches a locker that already has a number, the loop has closed.

```java
static int[] reportByLog(int[] slips) {
    int[] firstStep = new int[slips.length];
    for (int i = 0; i < firstStep.length; i++) firstStep[i] = -1;
    int locker = 0, step = 0;
    while (firstStep[locker] < 0) {
        firstStep[locker] = step;
        locker = slips[locker];
        step++;
    }
    return new int[] {locker, firstStep[locker], step - firstStep[locker]};
}
```

The locker where the walk stops is the shared one. Its recorded step is the number of moves from locker 0 before the walk first stands on it, and the difference between the current step and that record is the number of lockers in the loop.

<!-- stage: bottleneck -->
### The Sheet Costs One Line Per Locker

The walk makes at most n + 1 moves, so the time is O(n), and that part is already as good as it can be. The sheet is the trouble, because it has a line for every place, so it grows as O(n) and breaks the rule that the members carry almost nothing. Sorting a copy or counting numbers does not help, since both are O(n) extra memory again.

The sheet answers three separate questions at once, and each of them has a cheaper source. The shared locker is where the loop starts. The step count of that first visit is the distance from locker 0 to the loop. The loop size is the distance around once. If two walkers could find a place in the loop without a sheet, then the distance to the loop and the loop size could be counted with two small counters during walks that are needed anyway, which keeps the time at O(n) and the memory at O(1).

<!-- stage: insight -->
### Count Inside Each Phase

The array gives each index one **value link** to the index named by its value, so the walk from index 0 is a tail of `mu` steps followed by a ring of `lambda` places, and the first place on the ring is the shared value. Floyd's walk has two phases, and each of them can carry a counter without changing what it does.

In the **meeting phase** a walker moves one link per round and a runner moves two, both from index 0, until they stand on the same index. If `t` is the number of rounds, the walker has moved `t` links and the runner `2t`, and both are on the ring, so `t` is a multiple of `lambda`. It is also at least `mu`, since the walker must reach the ring before they can coincide, and it is the smallest multiple of `lambda` that is at least `mu`. The number of rounds therefore does not by itself say how long the tail is, because several tails give the same `t`, but it gives a free check on the other two answers.

In the **entry phase** the runner goes back to index 0, and the walker stays where the meeting happened. Now both move one link per round until they are equal. They land together on the first ring place after exactly `mu` rounds, so the number of rounds of this phase is the tail length, and the index where they land is the shared value. The ring size comes from one more short walk, started from the entry, that counts links until it is back on the entry, which takes `lambda` rounds.

<!-- names: value link, meeting phase, entry phase -->

The three numbers are tied together by the first phase. The invariant of the meeting phase is that the runner is always twice as far along the path as the walker. The invariant of the entry phase is that both walkers are the same number of links away from the ring's first place, modulo `lambda`, and the one from index 0 is still on the tail until round `mu`. The array is only read during all three walks, so a method that marks cells or swaps values would have given the same duplicate and would have broken the contract.

<!-- stage: variables -->
### Walker, Runner, Returner And Counters

`nums` is the read-only array, and every cell is checked, or promised, to hold a value from 1 to n. `walker` and `runner` start at 0 and move one and two links per round, and `meetRounds` counts the rounds of the meeting phase. `returner` starts at 0 for the entry phase, and `tail` counts its rounds, which ends equal to `mu`. `cycle` counts the links of the final lap, starting from the entry. The answer is the triple of the entry index, `tail` and `cycle`, and none of the counters changes what any pointer does.

<!-- stage: trace -->
### Three Walks And Their Counters

The first trace uses the array 2, 5, 1, 1, 4, 3. The walk from index 0 goes 0, 2, 1, 5, 3 and then back to 1, so the tail is two steps and the ring has the three places 1, 5 and 3. The step to study is the third round of the meeting phase, where the walker and the runner finally stand on the same index, after a number of rounds that is the smallest multiple of 3 that is at least 2, which is 3.

```trace
{"cells":[2,5,1,1,4,3],"pointers":["walker","runner","returner"],"steps":[{"at":{"walker":2,"runner":1,"returner":-1},"vars":{"phase":"meeting","rounds":1},"note":"Meeting round 1: the walker moves to index 2 and the runner moves two links to index 1. They are apart."},{"at":{"walker":1,"runner":3,"returner":-1},"vars":{"phase":"meeting","rounds":2},"note":"Meeting round 2: the walker moves to index 1 and the runner moves two links to index 3. They are apart."},{"at":{"walker":5,"runner":5,"returner":-1},"vars":{"phase":"meeting","rounds":3},"note":"Meeting round 3: the walker is on index 5 and the runner, after two links, is on index 5. They coincide, so the meeting phase ends after 3 rounds."},{"at":{"walker":5,"runner":-1,"returner":0},"vars":{"phase":"entry","tail":0},"note":"The entry phase starts. The walker stays on index 5, and the returner starts at index 0. Both will move one link per round."},{"at":{"walker":3,"runner":-1,"returner":2},"vars":{"phase":"entry","tail":1},"note":"Entry round 1: the returner moves to index 2 and the walker to index 3. They are apart."},{"at":{"walker":1,"runner":-1,"returner":1},"vars":{"phase":"entry","tail":2},"note":"Entry round 2: both land on index 1. This is the shared value, and the tail is 2."},{"at":{"walker":1,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":0},"note":"The lap starts on the entry, index 1. The walker will count links until it is back here."},{"at":{"walker":5,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":1},"note":"Lap link 1: the walker reaches index 5."},{"at":{"walker":3,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":2},"note":"Lap link 2: the walker reaches index 3."},{"at":{"walker":1,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":3},"note":"Lap link 3: the walker reaches index 1. That is the entry again, so the ring size is 3."}]}
```

The second trace uses the array 3, 1, 3, 2, a very short case. The walk goes 0, 3, 2 and back to 3, so the tail is one step and the ring has two places. The step to study is the restart of the entry phase, where the returner stands on index 0 and the walker stands on the meeting place, and a single round puts them both on index 3. The final lap then counts two links, so the triple is 3, 1, 2.

```trace
{"cells":[3,1,3,2],"pointers":["walker","runner","returner"],"steps":[{"at":{"walker":3,"runner":2,"returner":-1},"vars":{"phase":"meeting","rounds":1},"note":"Meeting round 1: the walker moves to index 3 and the runner moves two links to index 2. They are apart."},{"at":{"walker":2,"runner":2,"returner":-1},"vars":{"phase":"meeting","rounds":2},"note":"Meeting round 2: the walker is on index 2 and the runner, after two links, is on index 2. They coincide, so the meeting phase ends after 2 rounds."},{"at":{"walker":2,"runner":-1,"returner":0},"vars":{"phase":"entry","tail":0},"note":"The entry phase starts. The walker stays on index 2, and the returner starts at index 0. Both will move one link per round."},{"at":{"walker":3,"runner":-1,"returner":3},"vars":{"phase":"entry","tail":1},"note":"Entry round 1: both land on index 3. This is the shared value, and the tail is 1."},{"at":{"walker":3,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":0},"note":"The lap starts on the entry, index 3. The walker will count links until it is back here."},{"at":{"walker":2,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":1},"note":"Lap link 1: the walker reaches index 2."},{"at":{"walker":3,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":2},"note":"Lap link 2: the walker reaches index 3. That is the entry again, so the ring size is 2."}]}
```

<!-- stage: code -->
### One Pass Through All Three Walks

```java
static int[] duplicateReport(int[] nums) {
    int walker = 0, runner = 0;
    do {
        walker = nums[walker];
        runner = nums[nums[runner]];
    } while (walker != runner);

    int returner = 0, tail = 0;
    while (returner != walker) {
        returner = nums[returner];
        walker = nums[walker];
        tail++;
    }

    int entry = walker, cycle = 1;
    for (int probe = nums[entry]; probe != entry; probe = nums[probe]) cycle++;
    return new int[] {entry, tail, cycle};
}

static boolean isValueLinkArray(int[] nums) {
    if (nums.length < 2) return false;
    for (int v : nums) if (v < 1 || v > nums.length - 1) return false;
    return true;
}
```

Each of the three loops runs at most n + 1 rounds and the code keeps a fixed number of integers, so the total is O(n) time and O(1) extra space, and nothing is ever assigned into the array. The second method is the validity test that the first exercise needs, and it reads each value once.

<!-- stage: applicability -->
### Reading Three Numbers From A Walk

A good moment for this combination is a read-only array whose values are legal indices, when the question asks for more than the repeated value: how far the walk is from the loop, how big the loop is, or whether the answer changes when the array is edited. Put the invariant in one sentence before writing code: the runner travels twice as far as the walker, and after the restart both are equally far from the first ring place. Then decide which counter belongs to which loop so that none of them is touched in another.

A false friend is the plain duplicate method that only returns the entry. It hides the tail and the ring size, and some people read the number of meeting rounds as the tail length, which is wrong whenever the ring is longer than the tail. Another false friend is cyclic placement or sign marking. They produce the duplicate in O(n) time, yet they write into the array, so they break a read-only promise, and they cannot report the tail or the ring size without extra work.

In Java, check the representation before walking when the input is not promised to be legal, because a stray 0 in the array sends the walk back to the start and a value past the end throws an exception. Use a do-while for the meeting phase, since both walkers start equal, and compare the array to a saved copy in tests to prove that nothing was written. Keep the three counters as separate `int` variables so a reader can tell which phase made each one.

<!-- stage: exercises -->
### Exercises

#### [Build] Value-As-Next-Index (Author exercise)
<!-- id: tp-value-as-next-index -->

**Prerequisites.** Index-as-storage from the arrays chapter, the Floyd lesson of this chapter (array cycle state), and reading an array without modifying it.

**Problem.** Given an array `nums`, decide whether it is a legal value-as-next-index array, which means that its length n + 1 is at least 2 and every value lies between 1 and n. If it is not legal, return an empty array. If it is legal, return the distinct indices visited by the walk that starts at index 0 and follows `index = nums[index]`, in visiting order, stopping before the first index would be visited a second time.

**Constraints.** 0 <= nums.length <= 3000, with arbitrary `int` values including negative ones. Do not modify the array and do not read an index before the values have been validated.

**Example 1.** Input `nums = [3, 1, 4, 2, 1]`, output `[0, 3, 2, 4, 1]`.

**Example 2.** Input `nums = [2, 0, 1]`, output `[]`.

**Hint.** Which values would make the walk leave the array or return to index 0? Why does the path never have more than n + 1 entries?

**Changed decision.** First rung: the work is to check that the representation holds and to record the path, with no interest yet in the loop.

#### [Vary] Find the Duplicate Number (LeetCode 287)
<!-- id: tp-duplicate-triple -->

**Prerequisites.** The value-as-next-index exercise above, and the single-answer Floyd method for this representation.

**Problem.** For a legal array with exactly one repeated value, return the triple `[duplicate, tail, cycle]`, where `tail` is the number of steps from index 0 to the first index of the loop and `cycle` is the number of indices in the loop. Count inside the phases of Floyd's method, and do not use extra memory proportional to n.

**Constraints.** 1 <= n <= 100000, a legal read-only array, and a constant number of extra integers. The array must be equal to its saved copy after the call.

**Example 1.** Input `nums = [2, 4, 3, 1, 2]`, output `[2, 1, 4]`.

**Example 2.** Input `nums = [5, 2, 6, 1, 3, 4, 2]`, output `[2, 5, 2]`.

**Hint.** What does the number of rounds in the entry phase measure? How can one extra lap, started from the entry, measure the ring?

**Changed decision.** The earlier lesson returned a single value, and now the output carries two distances, so each phase must carry its own counter.

#### [Boundary] Duplicate Near Start (Author exercise)
<!-- id: tp-duplicate-near-start -->

**Prerequisites.** The triple exercise above.

**Problem.** For a legal array whose first value `nums[0]` is itself the repeated value, so that the tail is as short as it can be, return the same triple `[duplicate, tail, cycle]`. Explain why the tail can never be 0 for a legal array, and check that the array is untouched.

**Constraints.** 1 <= n <= 50000, `nums[0]` is the repeated value, and no write to the array is allowed, not even one that is undone before returning.

**Example 1.** Input `nums = [1, 1]`, output `[1, 1, 1]`.

**Example 2.** Input `nums = [2, 3, 1, 2]`, output `[2, 1, 3]`.

**Hint.** What is the first place after index 0? Could index 0 itself be on the ring, and what would that need from the values?

**Changed decision.** The tail is pinned at its minimum, so the entry phase must run exactly one round and the answer must still come out through the same code path as for long tails.

#### [Recognize] Compare Alternatives (Author exercise)
<!-- id: tp-compare-alternatives -->

**Prerequisites.** All three exercises above, plus cyclic placement and sign marking from the arrays chapter.

**Problem.** For a legal array, run three duplicate finders directly on the given array object: Floyd's two walks, cyclic placement that swaps a value into the cell of its own number, and sign marking that negates the cell named by each absolute value. All three must return the same duplicate. Return `[a, b, c]`, where each entry is the number of cells whose value differs after the finder returns from what it was before. Say which finder you would pick when the array is read-only.

**Constraints.** 1 <= n <= 20000, a legal array with one repeated value, and each finder runs on a fresh copy of the input array so that the three counts do not influence one another.

**Example 1.** Input `nums = [3, 1, 4, 2, 1]`, output `[0, 4, 4]`.

**Example 2.** Input `nums = [1, 1]`, output `[0, 0, 1]`.

**Hint.** Which of the three finders writes to the array, and in which input does a writing finder happen to stop before it has written anything?

**Changed decision.** The question is no longer how to find the duplicate but which method may be used, and the answer depends on whether the contract allows writes.
