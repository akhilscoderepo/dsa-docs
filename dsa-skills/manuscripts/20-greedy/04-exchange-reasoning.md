<!-- lesson-kind: standard -->
<!-- lesson-id: exchange-reasoning -->
## Exchange Reasoning

<!-- stage: context -->
### Why Samples Do Not Convince A Reviewer

A candidate in a coding interview proposes a rule for the meeting-room problem: always book the shortest request that still fits. She runs it on three sample inputs, and each answer is correct. The interviewer asks one question: why does this rule give the best answer on every input?

She has no reply. Three correct answers show that the rule can work. They do not show that it always works. This lesson asks what a short argument has to contain so that a reader accepts a rule for all inputs, and how a program can search for the inputs that break a false rule.

<!-- stage: naive -->
### Trusting A Rule After A Few Samples

The candidate's check is a method that compares the rule with the best answer on a list of sample inputs. Each interval is half-open, and the rule accepts the shortest interval that does not overlap an accepted one.

```java
static int shortestFirst(int[][] iv) {
    int[][] order = iv.clone();
    Arrays.sort(order, (a, b) -> Integer.compare(a[1] - a[0], b[1] - b[0]));
    List<int[]> kept = new ArrayList<>();
    for (int[] m : order) {
        boolean clash = false;
        for (int[] k : kept) if (m[0] < k[1] && k[0] < m[1]) clash = true;
        if (!clash) kept.add(m);
    }
    return kept.size();
}

static boolean looksCorrect(int[][][] samples, int[] best) {
    for (int s = 0; s < samples.length; s++) {
        if (shortestFirst(samples[s]) != best[s]) return false;
    }
    return true;                       // the rule matched on every sample
}
```

```predict
The samples are `[[1,2],[3,4]]` with best 2, and `[[1,10],[2,3],[5,6]]` with best 2. Does `looksCorrect` return true? Does the rule also match on `[[0,4],[3,5],[4,8]]`, where the best answer is 2?

It returns true on the two samples. On the third input the rule takes `[3,5]` first, because it is the shortest. That interval overlaps both others, so the rule keeps one interval and the best answer is 2. The samples did not contain such an input.
```

<!-- stage: bottleneck -->
### Counting The Inputs The Samples Miss

A sample list covers a handful of inputs, and the set of legal inputs is far larger. For `n` intervals with endpoints from `V` values, there are about V^(2n) inputs. Checking all of them takes O(V^(2n)) work, which is hopeless for realistic sizes.

Testing has a second weakness. A finite list can only show that a rule is wrong. The one failing input is a proof of failure, and any number of passing inputs is not a proof of success. The interviewer wants the opposite direction. A short written argument has to cover every input at once, so it must talk about an arbitrary input and not about specific numbers.

<!-- stage: insight -->
### Writing A Four-Part Proof

#### Starting From Any Best Answer

A proof for a rule starts with an arbitrary best answer. The argument never builds the answer. It only assumes that some best answer exists and transforms it. The transformation is the **exchange step**. It replaces the first decision of that answer with the decision that the rule makes.

#### The Four Parts Of The Proof

A complete proof states four things in order. First, it names the rule's choice, for example the interval with the earliest end. Second, it describes the exchange step: the best answer began with some other interval `b`, and the proof swaps `b` for the chosen interval `a`. Third, it shows **preserved feasibility**, which means the changed answer is still valid. For the meeting rooms, `a` ends no later than `b`, so every interval that followed `b` still starts after `a` ends. The answer also keeps its size, so it is still a best answer. Fourth, it names the **reduced subproblem**, the input that remains once the choice is made, such as the intervals that start at or after the end of `a`. The same rule applies to that smaller input, so the argument repeats until nothing remains.

#### Why Examples Fall Short

An example fixes numbers, and the proof must hold for all numbers. If any of the four parts fails for one input, that input is a counterexample. For the rule "take the shortest interval", the exchange step fails. A short interval can sit in the middle of two long intervals and overlap both, so swapping it into a best answer can remove two intervals to add one.

<!-- names: exchange step, preserved feasibility, reduced subproblem -->

<!-- stage: variables -->
### Parts Of The Argument

Five items appear in every exchange proof. Each is a named object, and the Build and Vary exercises compute them.

- **rule** is the choice the algorithm commits to, such as the earliest end.
- **choice** is the item that the rule picks from the current input.
- **first** is the first decision of the arbitrary best answer, and it differs from the choice.
- **changed** is the best answer after the exchange step replaces `first` with the choice.
- **remainder** is the input left after the choice, and the same rule applies to it.

The proof is complete when `changed` is valid, is no worse than the original, and starts with the choice.

<!-- stage: trace -->
### Following One Exchange And One Counterexample

#### Swapping The First Interval

The first trace uses the intervals `[1,3)`, `[2,5)`, `[4,7)` and `[6,9)`. The rule picks `[1,3)`, because it ends first. Take the best answer `[2,5)`, `[6,9)`, which begins with a different interval.

The exchange step replaces `[2,5)` with `[1,3)`. The interval `[1,3)` ends at 3, before 5, so `[6,9)` still starts after it. The changed answer has the same size and begins with the choice of the rule.

```trace
{"cells":["2-5","6-9"],"pointers":["k"],"steps":[{"at":{"k":0},"vars":{"answer":"2-5, 6-9","size":2},"note":"The best answer begins with [2,5), which is not the choice of the rule. The rule picks [1,3), the interval with the earliest end."},{"at":{"k":0},"vars":{"answer":"1-3, 6-9","size":2},"note":"The exchange step replaces [2,5) with [1,3). The new interval ends at 3, before 5, so it ends no later than the interval it replaces."},{"at":{"k":1},"vars":{"answer":"1-3, 6-9","size":2},"note":"The interval [6,9) starts at 6, after 3, so it does not overlap the choice. The changed answer is valid, has size 2 and begins with the choice."}]}
```

#### Breaking The Shortest-First Rule

The second trace feeds `[0,4)`, `[3,5)` and `[4,8)` to the shortest-first rule. The pointer `i` marks the interval in length order. The interval `[3,5)` has length 2 and goes first. Both other intervals overlap it, so the rule keeps one interval. The best answer keeps `[0,4)` and `[4,8)`, which is two. The input is a counterexample.

```trace
{"cells":["3-5","0-4","4-8"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"accepted":1},"note":"The interval [3,5) has length 2 and overlaps no accepted interval, so the rule accepts it."},{"at":{"i":1},"vars":{"accepted":1},"note":"The interval [0,4) overlaps the accepted interval, so the rule rejects it."},{"at":{"i":2},"vars":{"accepted":1},"note":"The interval [4,8) overlaps the accepted interval, so the rule rejects it."}]}
```

<!-- stage: code -->
### Checking A Swap And Searching For Failures

```java
static int[][] swapFirst(int[][] schedule, int[] chosen) {
    if (schedule.length == 0 || chosen[1] > schedule[0][1]) return null;   // chosen must end no later
    int[][] changed = schedule.clone();
    changed[0] = chosen;
    for (int k = 1; k < changed.length; k++) {
        if (changed[k][0] < changed[k - 1][1]) return null;                // an overlap breaks feasibility
    }
    return changed;
}

static int[][] findCounterexample(int values, int n) {
    int per = values * values;                                   // pairs (start, end) per interval
    int total = (int) Math.pow(per, n);
    for (int code = 0; code < total; code++) {
        int[][] iv = new int[n][];
        int c = code;
        for (int k = 0; k < n; k++) {
            int pair = c % per; c /= per;
            int s = pair / values, e = pair % values;
            if (s >= e) { iv = null; break; }                    // half-open needs start < end
            iv[k] = new int[] {s, e};
        }
        if (iv != null && shortestCount(iv) < maxCompatible(iv)) return iv;
    }
    return null;                                                 // no failure of this size
}

static int shortestCount(int[][] iv) {
    int[][] order = iv.clone();
    Arrays.sort(order, Comparator.comparingInt((int[] a) -> a[1] - a[0]).thenComparingInt(a -> a[0]));
    int[][] kept = new int[order.length][];
    int n = 0;
    for (int[] m : order) {
        boolean clash = false;
        for (int k = 0; k < n; k++) if (m[0] < kept[k][1] && kept[k][0] < m[1]) clash = true;
        if (!clash) kept[n++] = m;
    }
    return n;
}

static int maxCompatible(int[][] iv) {
    int[][] byEnd = iv.clone();
    Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));
    int count = 0, lastEnd = Integer.MIN_VALUE;
    for (int[] m : byEnd) if (m[0] >= lastEnd) { count++; lastEnd = m[1]; }
    return count;
}
```

The method `swapFirst` replays the exchange step on a schedule sorted by start. It returns the changed schedule, or `null` when the swap would break feasibility. The method `findCounterexample` enumerates every small input, and it compares `shortestCount`, the rule with its tie order, with `maxCompatible`, the end-order scan of lesson 02. A returned input is a proof of failure. A `null` result proves nothing about larger inputs.

- **Time** of `swapFirst` is O(n), because it checks each neighboring pair once.
- **Space** of `swapFirst` is O(n) for the copy, and the search takes O(per^n * n^2) time.

<!-- stage: applicability -->
### Using Proofs In Interviews

#### Applying The Invariant

When an interviewer asks why a rule is safe, answer with the four parts and one concrete input. The invariant of the argument is that an arbitrary best answer can be changed to start with the choice without becoming worse. Say the sentence first, then show the swap.

#### Finding Cases That Break The Precondition

A false friend is a worked example presented as a proof. A table of passing inputs convinces nobody who can find one failing input. A second false friend is an exchange that preserves the objective but breaks feasibility, so check the validity of the changed answer before you claim the step works.

#### Avoiding Java Pitfalls

When you search for counterexamples, keep the input space small and enumerate it fully, so a failure is reproducible. Print the failing input, not only a boolean. Fix the tie rule of the rule under test, because a rule with undefined ties gives different results between runs of `Arrays.sort` with different comparators.

<!-- stage: exercises -->
### Exercises

#### [Build] Exchange Two Assignments (Author exercise)
<!-- id: gr-exchange-two-assignments -->

**Prerequisites.** The exchange step of this lesson and lesson 01.

**Problem.** Arrays `demands` and `supplies` are sorted in non-decreasing order, and `demands` is not empty. Array `plan` has one entry per demand. Entry `plan[k]` is the index of the supply that serves demand `k`, or -1 when demand `k` is unserved. The plan is valid, so each supply serves at most one demand and always meets its demand. Let `r` be the smallest index with `supplies[r] >= demands[0]`. Apply one exchange step so that demand 0 uses supply `r`. If another demand `e` uses `r`, give `e` the supply that demand 0 used before, which may be -1. Return the changed plan, or the unchanged plan when no supply `r` exists.

**Constraints.** The limits are:
- **Count** is `1 <= demands.length <= 1000` and `0 <= supplies.length <= 1000`.
- **Values** are integers in `1 <= value <= 10^6`.
- **Plan** is valid and has the length of `demands`.
- **Mutation** of the plan is allowed.

**Example 1.** Input `demands = [3,5]`, `supplies = [4,6,9]` and `plan = [2,1]`, output `[0,1]`.

**Example 2.** Input `demands = [3,5]`, `supplies = [4,6]` and `plan = [-1,0]`, output `[0,-1]`.

**Hint.** What happens when the supply `r` is already in use, and what does demand 0 hold before the swap?

**Changed decision.** The method rewrites one plan and does not search for a plan.

#### [Vary] Swap To Earlier Finish (Author exercise)
<!-- id: gr-swap-to-earlier-finish -->

**Prerequisites.** The previous exercise.

**Problem.** Array `schedule` holds half-open intervals sorted by start, and no two overlap. Interval `chosen` is a half-open interval. Replace the first interval of the schedule with `chosen` when `chosen` ends no later than the first interval and the changed schedule has no overlap. Return the changed schedule, or the original schedule when the replacement is not allowed.

**Constraints.** The limits are:
- **Count** is `1 <= schedule.length <= 10^4`.
- **Values** are integers in `-10^9 <= start < end <= 10^9`.
- **Equal ends** are allowed, and the swap is then permitted.
- **Mutation** does not occur; return a new array when a swap happens.

**Example 1.** Input `schedule = [[2,5],[6,9]]` and `chosen = [1,3]`, output `[[1,3],[6,9]]`.

**Example 2.** Input `schedule = [[2,5],[6,9]]` and `chosen = [1,7]`, output `[[2,5],[6,9]]`.

**Hint.** After the swap, which neighbors of the first position still need a check?

**Changed decision.** The method tests a swap and does not build a schedule.

#### [Boundary] Find A Counterexample (Author exercise)
<!-- id: gr-find-a-counterexample -->

**Prerequisites.** The shortest-first rule of the naive stage.

**Problem.** The rule shortest-first sorts half-open intervals by length, breaks ties by smaller start, and accepts an interval when it overlaps no accepted interval. Return true when the rule accepts fewer intervals than the largest set of intervals that no two overlap, and false otherwise.

**Constraints.** The limits are:
- **Count** is `0 <= intervals.length <= 12`.
- **Values** are integers in `0 <= start < end <= 50`.
- **Duplicates** may appear and count as separate intervals.
- **Return** is a boolean.

**Example 1.** Input `intervals = [[0,4],[3,5],[4,8]]`, output true.

**Example 2.** Input `intervals = [[1,2],[3,4]]`, output false.

**Hint.** What is the shortest interval doing to its two neighbors?

**Changed decision.** The method detects a failing input and does not solve the scheduling task.

#### [Recognize] Present A Greedy Proof (Author exercise)
<!-- id: gr-present-a-greedy-proof -->

**Prerequisites.** All four parts of the proof in this lesson.

**Problem.** Intervals are half-open. Rule 1 picks the interval with the smallest end. Rule 2 picks the interval with the smallest start. Rule 3 picks the shortest interval. Each rule breaks ties by smaller start, then by smaller input position. Given `intervals` and a rule number, return true when the interval picked by the rule belongs to at least one largest set of intervals that no two overlap.

**Constraints.** The limits are:
- **Count** is `1 <= intervals.length <= 12`.
- **Values** are integers in `0 <= start < end <= 50`.
- **Rule** is 1, 2 or 3.
- **Duplicates** may appear and count as separate intervals.

**Example 1.** Input `intervals = [[0,4],[3,5],[4,8]]` and `rule = 1`, output true.

**Example 2.** Input `intervals = [[0,4],[3,5],[4,8]]` and `rule = 3`, output false.

**Hint.** For which rule can you swap the pick into any best set without breaking it?

**Changed decision.** The method tests a rule's first pick on one input.
