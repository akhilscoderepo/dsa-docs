<!-- lesson-kind: combination -->
<!-- lesson-id: greedy-and-heap -->
## Greedy And Heap

<!-- stage: context -->
### The Road Steward Of Gantry Pass

The road steward of Gantry Pass leads a wagon train from the valley town to the far gate. The road is long and she meets a series of small events. Some are steep ramps where the wagons need either a stack of timber or one of the few winches she carries. Some are fuel depots, each of which offers a certain amount of oil if she stops there. Some are trading contracts that need an up-front deposit and pay a profit afterwards.

At every event she could act at once, but she has noticed that most of the time she does not need to. The ramp may turn out to be cheap, and the depot she skipped may never matter. What she wants is to postpone each decision until the road forces it, and then to look back over everything she has passed and act on the best of it.

<!-- stage: contributions -->
### What Rule And Queue Each Bring

The greedy reasoning brings the rule for hindsight. It says which earlier option should be taken, kept, or given up once a limit is hit: the smallest ramp that holds a winch, the biggest depot already passed, the longest task in the plan, or the most profitable contract that can be afforded. The proof is an exchange argument showing that this particular option is never a mistake.

The heap brings the access. The candidates arrive in the order of the road, and the extreme one must be found again and again as new candidates are added, which a sorted list could not do cheaply. A heap hands over the largest or the smallest in logarithmic time. Neither part works alone: the heap does not know which extreme is the safe one, and the rule has no quick way to find it. The cue for the combination is a limit that gets hit, followed by a need to undo or to select the best of everything seen so far.

<!-- stage: naive -->
### Branch On Every Ramp

The direct method walks along the road and, at each ramp, tries both ways to cross it, with timber and with a winch, as long as the supplies last. It returns the farthest building it can reach by any sequence of choices.

```java
static int furthest(int[] h, int i, long timber, int winches) {
    if (i == h.length - 1) return i;
    int climb = h[i + 1] - h[i];
    if (climb <= 0) return furthest(h, i + 1, timber, winches);       // downhill or level is free
    int best = i;
    if (timber >= climb) best = Math.max(best, furthest(h, i + 1, timber - climb, winches));
    if (winches > 0) best = Math.max(best, furthest(h, i + 1, timber, winches - 1));
    return best;
}
```

The method is exact, because it tries every assignment of supplies to ramps, and it finishes quickly on a short road.

<!-- stage: bottleneck -->
### Two Branches Per Ramp

A road with n ramps has up to O(2^n) assignments, and the failing assignments are explored in full. The cost comes from deciding too early. When the steward reaches a ramp she cannot know whether the winch is better spent here or on a much bigger ramp ahead, so the recursion splits and carries both possibilities.

The deferral idea removes the split. She can put a winch on every ramp as she meets it, as a provisional measure, and change her mind later. The only question when the winches run out is which ramp to take a winch back from, and the answer is the smallest ramp among those that currently hold one. Finding the smallest among a changing collection, again and again, is the job of a heap.

<!-- stage: insight -->
### Decide Late, Retract The Cheapest

A **provisional choice** is a decision taken tentatively that the algorithm is allowed to retract. The steward gives each new ramp a winch. If that uses more winches than she owns, she must retract one, and the **regret move** is to retract the smallest ramp that holds one, paying for it in timber instead. The smallest is correct because every other plan must also pay timber for all but the largest ramps of the road so far, and the heap holds exactly those largest ones. The timber spent is the total of all ramps minus the largest few, which is the least that any plan can spend on this stretch.

The same shape solves the other events. For fuel, the **eligible pool** is the set of depots already passed. She drives until the fuel runs out, and only then retroactively stops at the depot with the most oil in the pool, because any plan that reaches farther with the same number of stops can swap in the larger depot. For tasks with deadlines, the retained task set loses its longest member when a deadline is broken. For contracts, the pool holds those that she can afford, and she takes the most profitable, which raises her capital and widens the pool.

<!-- names: provisional choice, regret move, eligible pool -->

The heap alone proves nothing. A heap of all contracts by profit would pick one she cannot afford, and a heap of ramps by size gives the wrong end if it is a max-heap instead of a min-heap. The proof decides which extreme of which collection is safe, and the heap only makes that extreme cheap to reach.

<!-- stage: variables -->
### The Heap, The Budget And The Reach

For the ramps, `onWinches` is a min-heap holding the climbs that currently use a winch, and `timber` is the supply left after paying for every climb that was retracted. The index `i` is the building being left. For fuel, `reach` is the farthest position the wagons can drive with the oil collected so far, `pool` is a max-heap of the oil at passed depots, and `stops` counts the depots used. For tasks, `kept` is a max-heap of retained durations and `time` is their sum. For contracts, `w` is the current capital, `next` is the first project, in capital order, not yet in the pool, and the pool is a max-heap of profits. Quantities that sum many numbers are `long`.

<!-- stage: trace -->
### Ramps And Depots Traced

The first trace uses buildings of heights 3, 9, 4, 6, 2, 12 and 8, with four units of timber and one winch. Leaving the first building is a climb of six, which takes the winch provisionally. The descents cost nothing. The climb of two from the third building to the fourth needs a winch as well, so the heap holds two climbs and one must be retracted. The smaller one, two, is paid for in timber, leaving two. The climb of ten to the next height adds a third climb and forces another retraction. The smallest is six, which costs six units of timber, but only two remain, so the walk stops at index 4.

The second trace is a fuel run to a target at position 60, starting with ten units. The first depot is at position ten and the fuel is exactly enough, so its thirty units go into the pool. The depot at twenty cannot be reached without help, so the thirty is drawn back and counts as the first stop. The depots at twenty and thirty add ten and twenty-five to the pool, and the depot at fifty is out of reach again, so the twenty-five is drawn as the second stop. After that the target is within reach.

```trace
{"cells":["3","9","4","6","2","12","8"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"timber":4,"onWinches":"6"},"note":"The climb of 6 takes a winch provisionally, and no timber is spent."},{"at":{"i":1},"vars":{"timber":4,"onWinches":"6"},"note":"Moving from height 9 to 4 is level or downhill, so it costs nothing."},{"at":{"i":2},"vars":{"timber":2,"onWinches":"6"},"note":"The climb of 2 is added and the winches are overcommitted, so the smallest climb on a winch, 2, is paid in timber, leaving 2."},{"at":{"i":3},"vars":{"timber":2,"onWinches":"6"},"note":"Moving from height 6 to 2 is level or downhill, so it costs nothing."},{"at":{"i":4},"vars":{"timber":-4,"onWinches":"10"},"note":"The climb of 10 is added and the smallest climb on a winch, 6, must be paid in timber, but the timber would fall to -4, so the walk stops here."}]}
```

```trace
{"cells":["10:30","20:10","30:25","50:20","60:end"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"reach":10,"stops":0,"pool":"30"},"note":"The depot at 10 is within reach, so its 30 units of oil enter the pool."},{"at":{"i":1},"vars":{"reach":40,"stops":1,"pool":"10"},"note":"The reach 10 is short of 20, so the largest oil in the pool, 30, is drawn as stop number 1 and the reach becomes 40. The depot at 20 is within reach, so its 10 units of oil enter the pool."},{"at":{"i":2},"vars":{"reach":40,"stops":1,"pool":"25-10"},"note":"The depot at 30 is within reach, so its 25 units of oil enter the pool."},{"at":{"i":3},"vars":{"reach":65,"stops":2,"pool":"20-10"},"note":"The reach 40 is short of 50, so the largest oil in the pool, 25, is drawn as stop number 2 and the reach becomes 65. The depot at 50 is within reach, so its 20 units of oil enter the pool."},{"at":{"i":4},"vars":{"reach":65,"stops":2,"pool":"20-10"},"note":"The target at 60 is within the reach 65."}]}
```

<!-- stage: code -->
### Four Heaps, Four Hindsight Rules

```java
static int furthestBuilding(int[] h, long timber, int winches) {
    PriorityQueue<Integer> onWinches = new PriorityQueue<>();            // smallest climb on top
    for (int i = 0; i + 1 < h.length; i++) {
        int climb = h[i + 1] - h[i];
        if (climb <= 0) continue;
        onWinches.add(climb);
        if (onWinches.size() > winches) timber -= onWinches.poll();      // retract the smallest
        if (timber < 0) return i;
    }
    return h.length - 1;
}

static int refuelStops(long target, long startFuel, long[][] depots) {  // depots[i] = {position, oil}
    PriorityQueue<Long> pool = new PriorityQueue<>(Comparator.reverseOrder());
    long reach = startFuel;
    int stops = 0;
    for (int i = 0; i <= depots.length; i++) {
        long position = i < depots.length ? depots[i][0] : target;
        while (reach < position) {
            if (pool.isEmpty()) return -1;
            reach += pool.poll();
            stops++;
        }
        if (i < depots.length) pool.add(depots[i][1]);
    }
    return stops;
}

static long[] bestPlan(int[][] tasks) {                                   // tasks[i] = {hours, deadline}
    int[][] order = tasks.clone();
    Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));
    PriorityQueue<Integer> kept = new PriorityQueue<>(Comparator.reverseOrder());
    long time = 0;
    for (int[] t : order) {
        kept.add(t[0]);
        time += t[0];
        if (time > t[1]) time -= kept.poll();
    }
    return new long[]{kept.size(), time};
}

static long ipo(int k, long w, int[] profit, int[] capital) {
    Integer[] byCapital = new Integer[profit.length];
    for (int i = 0; i < byCapital.length; i++) byCapital[i] = i;
    Arrays.sort(byCapital, (a, b) -> Integer.compare(capital[a], capital[b]));
    PriorityQueue<Integer> pool = new PriorityQueue<>(Comparator.reverseOrder());
    int next = 0;
    for (int round = 0; round < k; round++) {
        while (next < byCapital.length && capital[byCapital[next]] <= w) pool.add(profit[byCapital[next++]]);
        if (pool.isEmpty()) break;
        w += pool.poll();
    }
    return w;
}
```

Every item enters a heap at most once and leaves at most once, so each method costs O(n log n) in the number of items, with the sort of the contracts and tasks included. The supplies and capital are `long`, because the sum of many climbs or profits can exceed the `int` range even when each term fits.

<!-- stage: applicability -->
### When Hindsight Needs A Heap

Use the pair when a limit eventually forces a choice, when the best option is the extreme of everything seen so far, and when the extreme changes as new items arrive. The invariant is that the heap holds exactly the items still eligible for the regret move, and that the move takes the extreme the exchange argument names. State both the heap's direction and the proof sentence before coding.

The false friend is the heap without the proof. A max-heap of profits that ignores affordability picks contracts that cannot be taken, and a min-heap over the wrong quantity retracts the wrong ramp. Another false friend is a plain sort for a problem that needs undoing, such as the task plan from Lesson 05, where accepting whatever fits in deadline order fails. The pattern also stops applying when a retracted choice cannot really be changed later, for example when a depot must be used before the wagon passes it.

In Java, use `Comparator.reverseOrder()` for a max-heap and never negate or subtract to simulate one. Keep totals in `long`, and make sure every poll is guarded by an emptiness check where the contract allows an empty heap.

<!-- stage: exercises -->
### Exercises

#### [Build] Furthest Building You Can Reach (LeetCode 1642)
<!-- id: gc-furthest-building -->

**Prerequisites.** The heap lessons of Chapter 17; the local-choice and exchange lessons of this chapter.

**Problem.** You stand on building 0 and move to the next building each step. If the next building is not taller, the move is free. If it is taller by `d`, you pay `d` units of timber or use one winch. Return the index of the furthest building you can reach.

**Constraints.** 1 <= heights.length <= 100000, 1 <= heights[i] <= 1000000000, 0 <= timber <= 1000000000000000 and 0 <= winches <= heights.length.

**Example 1.** Input `heights = [3, 9, 4, 6, 2, 12, 8]`, `timber = 4`, `winches = 1`, output 4.

**Example 2.** Input `heights = [1, 1000000000, 1, 1000000000]`, `timber = 1999999998`, `winches = 0`, output 3.

**Hint.** Which climbs should end up on winches once the road is fully known? How can a heap maintain that set as the road is read?

**Changed decision.** Every climb takes a winch provisionally, and the smallest climb on a winch is retracted whenever the winches run out.

#### [Vary] Minimum Number of Refueling Stops (LeetCode 871)
<!-- id: gc-refuel-stops -->

**Prerequisites.** The furthest-building exercise above.

**Problem.** A vehicle starts at position 0 with `startFuel` units, burning one unit per unit of distance, and must reach `target`. Each depot `[position, oil]` lies at a position before the target, in increasing order, and adds its oil if the vehicle stops there. The tank has no capacity limit. Return the smallest number of stops, or -1 if the target cannot be reached.

**Constraints.** 0 <= depots.length <= 100000, 1 <= target, startFuel, position, oil <= 1000000000 and each position is smaller than the target.

**Example 1.** Input `target = 60`, `startFuel = 10`, `depots = [[10, 30], [20, 10], [30, 25], [50, 20]]`, output 2.

**Example 2.** Input `target = 100`, `startFuel = 1`, `depots = [[10, 100]]`, output -1.

**Hint.** When must a stop be made, and which depot among those already passed is best to have stopped at? Why can the stop be decided after passing it?

**Changed decision.** Depots enter a pool as they are passed, and the largest is used only when the fuel runs out.

#### [Boundary] Course Schedule III (LeetCode 630)
<!-- id: gc-course-plan-total -->

**Prerequisites.** The two exercises above and the task-selection lesson of this chapter.

**Problem.** Each course is `[duration, lastDay]`, courses are taken one after another from day 0, and a course must end by its last day. Return two values: the largest number of courses that can be taken, and the smallest total duration among all choices of that many courses. The total can pass the `int` range.

**Constraints.** 0 <= courses.length <= 100000 and 1 <= duration, lastDay <= 2147483647.

**Example 1.** Input `courses = [[7, 7], [3, 8], [2, 9], [4, 13], [5, 13]]`, output `[3, 9]`.

**Example 2.** Input `courses = [[2000000000, 2000000000], [2000000000, 2147483647]]`, output `[1, 2000000000]`.

**Hint.** Whenever a last day is broken, which kept course is the best to give up, and what does giving it up do to the total? What happens when the newcomer is itself the longest?

**Changed decision.** The retracted course is the longest retained one, and the final heap contents also give the smallest possible total for that count.

#### [Recognize] IPO (LeetCode 502)
<!-- id: gc-ipo-capital -->

**Prerequisites.** All three exercises above.

**Problem.** You may start at most `k` distinct projects. Project `i` needs capital `capital[i]` to start and adds `profit[i]` to your capital when finished, immediately. You begin with capital `w`. Return the largest capital you can hold after at most `k` projects.

**Constraints.** 0 <= k <= 100000, 0 <= w <= 1000000000, 0 <= profit[i], capital[i] <= 1000000000 and the two arrays have the same length. The answer can pass the `int` range.

**Example 1.** Input `k = 3`, `w = 2`, `profit = [5, 1, 4, 9, 2]`, `capital = [3, 0, 2, 8, 2]`, output 20.

**Example 2.** Input `k = 2`, `w = 0`, `profit = [7, 3]`, `capital = [1, 1]`, output 0, since neither project is affordable.

**Hint.** Which projects can be started right now, and which of them is best? What happens to the set of affordable projects after a project finishes?

**Changed decision.** The pool grows as the capital grows, and the most profitable affordable project is taken each round.
