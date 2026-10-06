<!-- lesson-kind: combination -->
<!-- lesson-id: undo-with-heap -->
## Undo The Worst Choice With A Heap

<!-- stage: context -->
### Why A Runner Spends Passes Early

A database migration runner applies a list of schema steps in order. Each step needs some downtime, measured in minutes. The runner owns a downtime allowance of `b` minutes and `k` skip passes. A skip pass applies one step with no downtime at all. The runner stops at the first step that it cannot pay for, and the operator wants it to get as far as possible.

A runner that spends a skip pass on every step while passes remain wastes them on tiny steps. The first large step then arrives, and nothing is left to cover it. This lesson asks how the runner decides which steps get a skip pass when it cannot see the later steps, and how a heap lets it change an earlier decision.

<!-- stage: contributions -->
### What The Rule And Heap Add

The greedy rule says which earlier decision to take back. Skip passes belong to the largest steps, so when one more step arrives and the passes are over, the smallest step that holds a pass is the one to pay for with downtime instead. The rule says what to undo. It does not say how to find that step quickly.

The heap says how to find it. A min-heap of the steps that hold a pass returns the smallest of them in O(log n) time, and it accepts each new step in the same time. A heap alone proves nothing. It only gives fast access to the smallest or largest value, and a program that popped the wrong end would run fast and return a wrong answer. The pairing works because the rule chooses the end of the heap and the heap makes that choice cheap.

<!-- stage: naive -->
### Spending Passes On The First Steps

The direct plan spends a skip pass on each step while passes remain and pays with downtime afterwards. Heights give the cumulative level, and a step needs downtime equal to the rise from one level to the next. A level that drops or stays equal needs none.

```java
static int reachByFirstPasses(int[] level, int allowance, int passes) {
    for (int i = 1; i < level.length; i++) {
        int rise = level[i] - level[i - 1];
        if (rise <= 0) continue;                 // no downtime needed
        if (passes > 0) passes--;                // spend a pass on the first rises
        else if (allowance >= rise) allowance -= rise;
        else return i - 1;                       // cannot pay: stop before step i
    }
    return level.length - 1;
}
```

```predict
Run the method on `level = [4, 5, 13, 14]` with `allowance = 2` and `passes = 1`. How far does it get, and how far can an ideal plan get?

It stops at index 1. The first rise is 1 and takes the only pass. The second rise is 8, which exceeds the allowance of 2, so the method stops. An ideal plan pays the first rise of 1 with downtime, gives the pass to the rise of 8, and pays the last rise of 1 with downtime. It reaches index 3.
```

<!-- stage: bottleneck -->
### Counting The Ways To Assign Passes

An ideal plan could try every way to give the `k` passes to the `r` rises. That is C(r, k) choices, and the count passes a billion for modest values such as `r = 40` and `k = 20`. Each choice also needs a pass over the steps to check the allowance, so the work is O(C(r, k) * n).

The method above is fast but commits a pass at the first rise and never takes it back. The two extremes suggest a middle plan. Let the runner commit a pass to every rise at first, and let it take one pass back when the passes run out. The open question is which pass to take back, and the answer must keep the best possible plan open.

<!-- stage: insight -->
### Giving A Pass And Taking It Back

#### Committing A Pass Tentatively

A **tentative choice** gives a pass to every rise as it arrives. The runner pushes the rise into a min-heap of the rises that currently hold a pass. As long as the heap holds at most `k` rises, no downtime is paid.

#### Taking Back The Smallest

When the heap holds more than `k` rises, the **ejection step** pops the smallest rise and pays for it with downtime. The smallest rise holds the pass that saves the least downtime. Taking it back costs the least extra allowance, so no other rise is a better one to eject.

An exchange argument supports this. Take a best assignment of passes to the rises read so far. If it covers a rise `x` with downtime while a smaller rise `y` holds a pass, swapping them saves `x - y` minutes and never costs more. A best assignment therefore gives passes to the `k` largest rises.

#### Stopping At The Allowance

The **budget limit** is the allowance `b`. Each ejection subtracts the popped rise from it. When the allowance goes below zero, the runner cannot pay for the current step, so it stops there. The heap keeps the `k` largest rises, and the rest were paid for. The state after step `i` is always the best use of `k` passes for the rises up to `i`.

<!-- names: tentative choice, ejection step, budget limit -->

<!-- stage: variables -->
### State Of The Runner

The runner keeps one heap and two counters. Four items describe the state.

- **covered** is a min-heap that holds the rises that currently have a pass, and its size never stays above `k`.
- **allowance** is the downtime left, and it never passes below zero without stopping the runner.
- **rise** is the positive difference between a level and the previous level.
- **i** is the index of the step under test, and the result is the last index that the runner finishes.

A step with a rise of zero or less does not touch the heap.

<!-- stage: trace -->
### Two Runs With A Heap

#### Giving Passes To The Largest Rises

The first trace uses `level = [4, 5, 13, 14]`, `allowance = 2` and `passes = 1`. The pointer `i` marks the step under test.

The rise at index 1 is 1, so the runner pushes it, and the heap holds one rise. At index 2 the rise is 8. The heap holds two rises, which is more than one pass, so the runner pops the smallest, 1, and pays 1 from the allowance. At index 3 the rise is 1. The runner pushes it, pops it at once and pays 1 more. The allowance is 0, and the runner finishes index 3.

```trace
{"cells":[4,5,13,14],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"heap":1,"allowance":2},"note":"The rise at index 1 is 1, so the runner pushes it into the heap. The heap still fits the passes, so nothing is paid."},{"at":{"i":2},"vars":{"heap":1,"allowance":1},"note":"The rise at index 2 is 8, so the runner pushes it into the heap. The heap holds more than 1 rise, so the runner pops the smallest, 1, and pays it from the allowance."},{"at":{"i":3},"vars":{"heap":1,"allowance":0},"note":"The rise at index 3 is 1, so the runner pushes it into the heap. The heap holds more than 1 rise, so the runner pops the smallest, 1, and pays it from the allowance."}]}
```

#### Refueling With The Largest Passed Station

A second problem has the same shape. A vehicle has fuel and drives to a target. Each station along the road holds some fuel and can be used once. The vehicle does not stop until it cannot reach the next stop. The heap then holds the fuel of the stations already passed, and the rule takes the largest. The trace uses a start fuel of 10 and stations at positions 5, 11 and 20 with fuel 2, 10 and 5, and a target at 25.

```trace
{"cells":["5:2","11:10","20:5","25:end"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"fuel":10,"stops":0},"note":"The next stop is at 5 and needs fuel 5 in total. The vehicle reaches it and adds its fuel 2 to the heap."},{"at":{"i":1},"vars":{"fuel":12,"stops":1},"note":"The next stop is at 11 and needs fuel 11 in total. The fuel 10 is short, so the vehicle takes the largest passed station, 2, and the fuel becomes 12. The vehicle reaches it and adds its fuel 10 to the heap."},{"at":{"i":2},"vars":{"fuel":22,"stops":2},"note":"The next stop is at 20 and needs fuel 20 in total. The fuel 12 is short, so the vehicle takes the largest passed station, 10, and the fuel becomes 22. The vehicle reaches it and adds its fuel 5 to the heap."},{"at":{"i":3},"vars":{"fuel":27,"stops":3},"note":"The next stop is at 25 and needs fuel 25 in total. The fuel 22 is short, so the vehicle takes the largest passed station, 5, and the fuel becomes 27. The vehicle reaches the target."}]}
```

<!-- stage: code -->
### Keeping The Covered Rises In A Heap

```java
static int furthest(int[] level, int allowance, int passes) {
    PriorityQueue<Integer> covered = new PriorityQueue<>();
    for (int i = 1; i < level.length; i++) {
        int rise = level[i] - level[i - 1];
        if (rise <= 0) continue;
        covered.add(rise);                          // tentatively cover this rise
        if (covered.size() > passes) allowance -= covered.poll();   // pay for the smallest
        if (allowance < 0) return i - 1;
    }
    return level.length - 1;
}
```

The heap is a min-heap, so `poll` returns the smallest rise. The method adds before it tests the size, so the new rise competes with the older ones. The difference of two levels fits in `int` for the limits of the exercises, and the allowance changes only by subtraction of a positive rise.

- **Time** is O(n log k), because each step costs at most one push and one pop on a heap of at most `k + 1` entries.
- **Space** is O(k) for the heap.

<!-- stage: applicability -->
### When A Heap Carries The Undo

#### Applying The Invariant

Use this pairing when each new item can be accepted tentatively, a limited resource may run out, and the best earlier choice to withdraw is the smallest or largest accepted value. The invariant is that after each step, the heap holds exactly the choices that an optimal plan for the steps read so far would keep. State which end of the heap the rule pops and why.

#### Finding Cases That Break The Precondition

A false friend is a heap used only as a sorted container. If the rule does not name which choice to withdraw, the heap gives speed and no correctness. A second false friend is a withdrawal that is not free, such as a choice that changes the cost of later choices. Then the exchange step fails, and the problem needs state comparison from the dynamic programming chapters.

#### Avoiding Java Pitfalls

Use `Collections.reverseOrder()` for a max-heap and never subtract values in a comparator. Use `long` for a sum of allowances or fuel that can pass 2,147,483,647. Equal values leave the heap in no promised order, so a result must not depend on it.

<!-- stage: exercises -->
### Exercises

#### [Build] Furthest Building You Can Reach (LeetCode 1642)
<!-- id: gr-furthest-building -->

**Prerequisites.** The heap and the ejection step of this lesson.

**Problem.** Array `heights` holds building heights. Moving from building `i` to building `i + 1` costs nothing when the next height is no larger. When the next height is larger, the move needs either one ladder or as many bricks as the height difference. There are `bricks` bricks and `ladders` ladders. Return the index of the furthest building that the climber reaches, starting at index 0.

**Constraints.** The limits are:
- **Count** is `1 <= heights.length <= 10^5`.
- **Values** are integers in `1 <= heights[i] <= 10^6`.
- **Resources** are `0 <= bricks <= 10^9` and `0 <= ladders <= heights.length`.
- **Mutation** does not occur.

**Example 1.** Input `heights = [4,5,13,14]`, `bricks = 2` and `ladders = 1`, output 3.

**Example 2.** Input `heights = [1,5,1,9,2]`, `bricks = 3` and `ladders = 1`, output 2.

**Hint.** Which climb should a ladder replace when the ladders run out?

**Changed decision.** The method may take a ladder back from an earlier climb.

#### [Vary] Minimum Number of Refueling Stops (LeetCode 871)
<!-- id: gr-refueling-stops -->

**Prerequisites.** The previous exercise.

**Problem.** A vehicle starts at position 0 with `startFuel` units of fuel and uses one unit per position. Array `stations` holds pairs `{position, fuel}`, sorted by position. Stopping at a station adds its fuel at once, and each station can be used one time. Return the smallest number of stops needed to reach `target`, or -1 when it is not possible.

**Constraints.** The limits are:
- **Count** is `0 <= stations.length <= 500`.
- **Values** are integers in `1 <= target, startFuel, position, fuel <= 10^9` with positions below `target`.
- **Sum** of fuel can pass the `int` range.
- **Order** of the stations is increasing position.

**Example 1.** Input `target = 25`, `startFuel = 10` and `stations = [[5,2],[11,10],[20,5]]`, output 3.

**Example 2.** Input `target = 15`, `startFuel = 3` and `stations = [[2,4]]`, output -1.

**Hint.** When the next position is out of reach, which passed station gives the most fuel?

**Changed decision.** The method refuels from the largest passed station and counts stops.

#### [Boundary] Course Schedule III (LeetCode 630)
<!-- id: gr-courses-count-and-total -->

**Prerequisites.** Lesson 05 and the heap of this lesson.

**Problem.** Array `courses` holds pairs `{duration, lastDay}`. A student takes one course at a time from day 1, and a course counts only if it finishes by its last day. Return an array `[count, total]`, where `count` is the largest number of courses that can finish on time, and `total` is the smallest sum of durations among the sets of that size.

**Constraints.** The limits are:
- **Count** is `0 <= courses.length <= 10^4`.
- **Values** are integers in `1 <= duration, lastDay <= 10^9`.
- **Total** can pass the `int` range, so it needs `long`.
- **Empty** input returns `[0,0]`.

**Example 1.** Input `courses = [[5,5],[2,6],[2,6]]`, output `[2,4]`.

**Example 2.** Input `courses = [[3,3],[4,3]]`, output `[1,3]`.

**Hint.** What does the total of the heap equal after the last course?

**Changed decision.** The method also reports the smallest total, and the sums need `long`.

#### [Recognize] IPO (LeetCode 502)
<!-- id: gr-project-capital -->

**Prerequisites.** The previous exercises.

**Problem.** Arrays `profits` and `capital` describe projects. A project can start when the current capital is at least its `capital` value, and finishing it adds its profit to the capital. The student starts with `w` capital and finishes at most `k` projects, one at a time. Return the largest final capital.

**Constraints.** The limits are:
- **Count** is `0 <= profits.length == capital.length <= 10^5`.
- **Values** are integers in `0 <= profits[i], capital[i] <= 10^9`, and `0 <= w <= 10^9`.
- **Limit** is `0 <= k <= 10^5`.
- **Final** capital can pass the `int` range, so it needs `long`.

**Example 1.** Input `k = 2`, `w = 0`, `profits = [1,2,3]` and `capital = [0,1,1]`, output 4.

**Example 2.** Input `k = 3`, `w = 5`, `profits = [4,1]` and `capital = [9,0]`, output 6.

**Hint.** Which projects does the current capital unlock, and which unlocked project pays most?

**Changed decision.** The heap holds the unlocked projects and the rule takes the largest profit.
