<!-- lesson-kind: standard -->
<!-- lesson-id: exchange-reasoning -->
## Exchange Reasoning

<!-- stage: context -->
### The Whiteboard Round At Marlow Systems

Priya is in the final interview round at Marlow Systems. The problem on the whiteboard is to hold as many meetings as possible in one room. She proposes a rule at once: always take the shortest meeting that still fits. The code is five lines long, it passes the two examples that the interviewer drew, and she smiles.

The interviewer does not nod. She asks a plain question: why is that rule safe for every input, including inputs nobody has drawn yet? Priya realises that she has a rule and some examples but no reason. Her next sentence will decide the round, because an answer that begins with another example is no answer at all.

<!-- stage: naive -->
### Check The Rule On Sample Inputs

The natural first move is to test the rule. Priya writes the rule as code, writes a slow method that is certainly right, and compares the two on a handful of inputs.

```java
static int shortestFirst(int[][] iv) {
    List<int[]> kept = new ArrayList<>();
    List<int[]> pool = new ArrayList<>(Arrays.asList(iv));
    pool.sort(Comparator.comparingInt((int[] a) -> a[1] - a[0]).thenComparingInt(a -> a[0]));
    for (int[] a : pool) {
        boolean clash = false;
        for (int[] k : kept) if (a[0] < k[1] && k[0] < a[1]) clash = true;
        if (!clash) kept.add(a);
    }
    return kept.size();
}

static int bestByBruteForce(int[][] iv, int i, List<int[]> kept) {
    if (i == iv.length) return kept.size();
    int best = bestByBruteForce(iv, i + 1, kept);                 // skip interval i
    boolean fits = true;
    for (int[] k : kept) if (iv[i][0] < k[1] && k[0] < iv[i][1]) fits = false;
    if (fits) {
        kept.add(iv[i]);
        best = Math.max(best, bestByBruteForce(iv, i + 1, kept));
        kept.remove(kept.size() - 1);
    }
    return best;
}

static boolean agreesOn(int[][][] samples) {
    for (int[][] s : samples) if (shortestFirst(s) != bestByBruteForce(s, 0, new ArrayList<>())) return false;
    return true;
}
```

On the two meetings the interviewer drew, and on a dozen more that Priya sketches, `agreesOn` returns true. The rule looks fine, and the checker is a real one, so every sample is judged correctly.

<!-- stage: bottleneck -->
### Samples Cannot Cover Every Input

The set of possible inputs has no end. Even if endpoints are limited to a small range, there are on the order of O(M^(2n)) calendars of n meetings with endpoints up to M, and no hand-written list covers them. A rule can survive every small sample and still fail on a calendar only slightly larger than the ones drawn. The shortest-first rule is a good example, since the calendar on which it breaks has just three meetings.

The failure of sampling is not a failure of effort. A passing test says that no failure was found among the cases tried, while the interviewer asked for a statement about all cases. What is missing is an argument that transforms any best answer into the rule's answer without making it worse. That argument can be checked by reading it, and it covers every input at once.

<!-- stage: insight -->
### Turn Any Best Answer Into The Rule's

A proof that a greedy rule is safe has four parts, and each one answers a question the interviewer is really asking. First, name the choice, which is the single decision the rule makes first. Second, take an arbitrary best solution that does not make that choice and describe an **exchange argument**: a transformation that swaps the choice in and swaps something else out. Third, show **preserved feasibility**, meaning the transformed solution is still legal, and show that its objective is no worse. Fourth, observe that what remains after the choice is the same kind of problem on fewer items, the **reduced subproblem**, so the same reasoning applies again and induction finishes the proof.

<!-- names: exchange argument, preserved feasibility, reduced subproblem -->

Take earliest-finish scheduling as the model. The choice is the meeting that ends first. The swap replaces the first meeting of any best calendar by it. Feasibility holds because every later meeting begins at or after the old end, which is at or after the new end. The calendar has the same size, so it is still best. What remains is a calendar problem for the meetings that begin at or after the chosen end.

The same template also kills a false rule, because a rule that cannot be exchanged into any best solution has a counterexample. A counterexample is a complete disproof, and it is usually small. The search for one is mechanical: list every small input, run the rule and an exact method on each, and report the first where the rule loses. Practising both directions is what makes an answer in an interview sound sure.

<!-- stage: variables -->
### The Best Answer And The Swap

Four things appear in every proof. The solution `opt` is an arbitrary best answer, never one that the proof builds from scratch. The choice `g` is the item the greedy rule picks first. The transformed solution `opt2` is `opt` with `g` swapped in, and the objective `f` is the quantity being optimised, so the claim to check is `f(opt2) >= f(opt)` for a maximum or `<=` for a minimum. The remainder is what is left after `g` is placed. Nothing changes during the proof except which solution is being named.

<!-- stage: trace -->
### A Swap Sequence And A Failing Rule

The first trace works on a minimum, the total of completion times when jobs run one after another. The durations are 5, 2, 8 and 1, run in the order given. The choice is a shortest job, and each step pulls a shortest remaining job to the front of the unresolved part by swapping it with the job standing there. The first step swaps the five with the one, and the total falls from forty-three to thirty-one. The second step finds the two already first and changes nothing. The third swaps the eight with the five, and the total falls to twenty-eight, which is the value of the fully sorted order.

The second trace follows the false rule on meetings 0 to 3, 2 to 4 and 3 to 7, whose lengths are all different, so no tie rule is hiding anything. Shortest-first takes 2 to 4 because it is the shortest, and then both other meetings overlap it, so the rule ends with one meeting. Earliest-finish takes 0 to 3, rejects 2 to 4 and takes 3 to 7, and it holds two meetings. That is the counterexample.

```trace
{"cells":["5","2","8","1"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"order":"1-2-8-5","total":31},"note":"The shortest job in the unresolved part is 1, found at position 3. Swapping it with the job at position 0 moves the total from 43 to 31."},{"at":{"i":1},"vars":{"order":"1-2-8-5","total":31},"note":"The job at position 1 is already a shortest one in the unresolved part, so no swap is needed and the total stays 31."},{"at":{"i":2},"vars":{"order":"1-2-5-8","total":28},"note":"The shortest job in the unresolved part is 5, found at position 3. Swapping it with the job at position 2 moves the total from 31 to 28."},{"at":{"i":3},"vars":{"order":"1-2-5-8","total":28},"note":"The job at position 3 is already a shortest one in the unresolved part, so no swap is needed and the total stays 28."}]}
```

```trace
{"cells":["0-3","2-4","3-7"],"pointers":["i"],"steps":[{"at":{"i":1},"vars":{"rule":"shortest first","taken":1},"note":"Shortest-first examines 2-4, the shortest span left with length 2, and takes it."},{"at":{"i":0},"vars":{"rule":"shortest first","taken":1},"note":"The span 0-3 starts at 0 and ends at 3, so it overlaps the taken 2-4 and is skipped."},{"at":{"i":2},"vars":{"rule":"shortest first","taken":1},"note":"The span 3-7 starts at 3 and ends at 7, so it overlaps the taken 2-4 and is skipped."},{"at":{"i":0},"vars":{"rule":"earliest finish","taken":1},"note":"Earliest-finish sorts by end and takes 0-3 first, since it ends at 3."},{"at":{"i":1},"vars":{"rule":"earliest finish","taken":1},"note":"The span 2-4 starts at 2, before the boundary 3, so it is rejected."},{"at":{"i":2},"vars":{"rule":"earliest finish","taken":2},"note":"The span 3-7 starts at 3, not before the boundary 3, so it is taken. Two spans beat the one that shortest-first found."}]}
```

<!-- stage: code -->
### Executable Swaps And A Search

```java
static long totalCompletion(int[] d, int[] order) {
    long clock = 0, total = 0;
    for (int job : order) { clock += d[job]; total += clock; }   // each job waits for all before it
    return total;
}

static int[] pullShortestToFront(int[] d, int[] order, int from) {
    int[] out = order.clone();
    int best = from;
    for (int k = from + 1; k < out.length; k++) if (d[out[k]] < d[out[best]]) best = k;
    int tmp = out[from]; out[from] = out[best]; out[best] = tmp;
    return out;
}

static int[] exchangeRoom(int[] need, int[] beds, int[] assign, int p, int s) {
    int[] out = assign.clone();
    int old = assign[p];
    if (old == s) return out;
    for (int q = 0; q < out.length; q++) if (out[q] == s) out[q] = old;   // holder takes the old room, or none
    out[p] = s;
    return out;
}
```

A swap changes the cost by an amount that can be written down, namely the difference in durations times the number of places the swap skips, so the first function lets code state and test the claim instead of trusting it. Each method makes one pass over its arrays and runs in O(n). The long accumulators matter, since a total of completion times grows like the square of the length.

<!-- stage: applicability -->
### When A Proof Beats A Test

Reach for exchange reasoning whenever a rule is justified by its examples only, or an interviewer asks why a rule is safe. The invariant is that after each choice some best solution still contains every choice made so far. The proof checks that invariant one choice at a time. Write the four parts in order, and test the transformation in code on random legal solutions when there is any doubt about the arithmetic.

The false friend is the passing example. Examples support intuition, and they can show that a rule is wrong, but they cannot show that it is right for all inputs. A second false friend is a swap that quietly breaks legality. Swapping a long meeting for a short one is attractive, yet if the short one overlaps meetings that the long one did not, the exchanged calendar is not legal and the argument fails. Weighted objectives need extra care, since the swap must also keep the total weight from dropping.

In Java, assert the claims about a swap on random inputs, and accumulate objective values in `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Exchange Two Assignments (Author exercise)
<!-- id: gr-exchange-two-assignments -->

**Prerequisites.** The local-choice lesson of this chapter; arrays of indexes.

**Problem.** Parties with sizes `need` hold rooms with capacities `beds` under a legal assignment `assign`, where `assign[i]` is the room of party `i` or -1, and no room is held twice. Let `p` be the party with the smallest need, taking the lowest index on a tie, and let `s` be the smallest room that fits `p`, taking the lowest index on a tie. If no room fits `p`, return the assignment unchanged. Otherwise return a new legal assignment in which `p` holds `s`, whoever held `s` takes the old room of `p` or none, and every other party is unchanged. The number of housed parties must not drop.

**Constraints.** 0 <= need.length, beds.length <= 10 and sizes are between 1 and 1000. The input arrays must not be modified.

**Example 1.** Input `need = [2, 5]`, `beds = [9, 2, 6]`, `assign = [0, 2]`, output `[1, 2]`.

**Example 2.** Input `need = [3, 4]`, `beds = [4, 3]`, `assign = [0, 1]`, output `[1, 0]`, a true swap, since the old room of party 0 fits party 1.

**Hint.** Who might be holding the smallest fitting room? Why does the old room of `p` fit that holder?

**Changed decision.** First rung: the exchange is a reassignment, and the proof obligation is that the displaced party still fits.

#### [Vary] Swap To Earlier Finish (Author exercise)
<!-- id: gr-swap-to-earlier-finish -->

**Prerequisites.** The exchange exercise above; the interval lesson of this chapter.

**Problem.** Intervals are half-open spans, and `schedule` lists the indexes of a conflict-free subset. Let `g` be the interval that ends earliest among all intervals, taking the lowest index on a tie, and let `f` be the member of the schedule that ends earliest, taking the lowest index on a tie. Return the schedule with `f` replaced by `g`, as indexes sorted by start and then by end. If the schedule is empty, return it unchanged. The result must be conflict-free and have the same size.

**Constraints.** 0 <= intervals.length <= 12, every span has `start < end`, and 0 <= start, end <= 100.

**Example 1.** Input `intervals = [[0, 6], [1, 3], [4, 8], [6, 9]]`, `schedule = [0, 3]`, output `[1, 3]`.

**Example 2.** Input `intervals = [[0, 2], [2, 5], [3, 4]]`, `schedule = [0, 1]`, output `[0, 1]`, since the schedule already starts with the earliest finish.

**Hint.** Which members of the schedule could clash with `g`? How does the end of `f` compare with the start of every other member?

**Changed decision.** The swap now replaces an interval, and legality rests on comparing ends with starts rather than on sizes.

#### [Boundary] Find A Counterexample (Author exercise)
<!-- id: gr-find-counterexample -->

**Prerequisites.** The two exercises above.

**Problem.** The rule shortest-first repeatedly takes the shortest remaining interval that does not overlap any interval already taken. To avoid tie rules, all intervals in a candidate set must have different lengths. Among sets of at most six half-open intervals with integer endpoints from 0 to `maxCoord`, find the first set on which shortest-first takes fewer intervals than the best possible. Order candidates by size, then lexicographically by the sorted list of spans. Return the set, or an empty array if none exists.

**Constraints.** 1 <= maxCoord <= 7. Each span has `start < end`, and a candidate set never repeats a span.

**Example 1.** Input `maxCoord = 7`, output `[[0, 3], [2, 4], [3, 7]]`.

**Example 2.** Input `maxCoord = 6`, output `[]`, since no counterexample with distinct lengths fits in that range.

**Hint.** Which interval must the rule take first, and what must it block? What does the best calendar do with the two long intervals?

**Changed decision.** Instead of proving the rule, the search proves it false, and the counterexample is the smallest object that shows why a swap fails.

#### [Recognize] Present A Greedy Proof (Author exercise)
<!-- id: gr-present-greedy-proof -->

**Prerequisites.** All three exercises above.

**Problem.** Jobs run one after another in a given `order`, and each job's completion time is the sum of the durations up to and including it. The rule to justify is shortest job first for minimising the sum of completion times. Perform one exchange step: find the first position `k` of a job with the smallest duration in `order`, swap it with the job in position 0, and return three `long` values: the total before the swap, the total after, and the total of the remaining jobs (positions 1 and later) taken as a separate sequence.

**Constraints.** 1 <= order.length <= 8, `order` is a permutation of the indexes of `d`, and 1 <= d[i] <= 1000000000.

**Example 1.** Input `d = [5, 2, 8, 1]`, `order = [0, 1, 2, 3]`, output `[43, 31, 27]`.

**Example 2.** Input `d = [3, 3, 3]`, `order = [2, 0, 1]`, output `[18, 18, 9]`, since a tie leaves the first job in place.

**Hint.** By how much does the total change when two jobs trade places, and how many other jobs sit between them? How is the total after the swap related to the first job and the remainder?

**Changed decision.** The proof is presented as numbers: a drop in the objective, an unchanged legality, and a smaller instance of the same problem.
