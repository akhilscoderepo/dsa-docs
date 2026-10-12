<!-- lesson-kind: standard -->
<!-- lesson-id: take-or-skip -->
## Take Or Skip

<!-- stage: context -->
### Picking Hours For A Rate-Limited Job

A reporting service runs an expensive export job. The job is useful in any hour of the day, but a quota rule forbids running it in two consecutive hours. Each hour has a forecast value, such as the number of customers who will download the report. With the forecasts `[5, 8, 5]` for three hours, the operator wants the highest total value. A scheduler that always grabs the best hour first runs hour 1 for a value of 8. Running hours 0 and 2 earns 10, which is better.

Formally, the input is an array `value` of length n. A **selection** is a set of indexes in which no two indexes are adjacent, meaning no two differ by exactly 1. The score of a selection is the sum of `value` over its indexes. The task is to return the highest score. The empty selection is legal and scores 0, and the method never changes the array.

This lesson asks how to find the best selection without testing every set of hours.

<!-- stage: naive -->
### Grabbing The Best Hour First

The quick idea is greedy. Pick the hour with the highest value, block its two neighbours, then pick the best hour that remains, and repeat until no hour is free.

```java
static int greedyBest(int[] value) {
    int n = value.length;
    boolean[] blocked = new boolean[n];
    int total = 0;
    while (true) {
        int pick = -1;
        for (int i = 0; i < n; i++) {
            if (!blocked[i] && (pick == -1 || value[i] > value[pick])) pick = i;
        }
        if (pick == -1) return total;
        total += value[pick];
        blocked[pick] = true;
        if (pick > 0) blocked[pick - 1] = true;
        if (pick + 1 < n) blocked[pick + 1] = true;
    }
}
```

Each round scans the array once and blocks at least one hour, so the method runs in O(n^2) time. It always returns a legal selection, and it is correct on many inputs. The open question is whether the best hour belongs to the best selection.

```predict
Run greedyBest on the forecasts [5, 8, 5]. What does it return, and what is the true highest score?

It returns 8, because it picks the middle hour first and blocks both neighbours. The true highest score is 10, from hours 0 and 2. A locally best pick can block two picks that are better together.
```

<!-- stage: bottleneck -->
### Local Choices Block Better Pairs

The greedy method judges each hour alone, but a pick also removes its neighbours from the future. The cost of a pick is not visible in its own value. Any fix that adjusts the order of picks fails on some input, because the right pick depends on values far away from it.

A correct but slow method tests every set of indexes. An array of n hours has 2^n sets, and checking one set for adjacent indexes costs O(n). For n = 40 that is more than 10^13 operations. Even counting only legal selections, the number grows like 1.6^n, so the legal sets alone are too many to list.

A useful method must compare a pick with what the pick destroys, without listing the sets. The answer for a longer array should reuse the answers for shorter arrays. The next section defines a table over the first i hours so that each entry needs only two earlier entries, giving O(n) time.

<!-- stage: insight -->
### Compare Skipping With Taking

Look at the last hour of an array and ask what a best selection does with it. Either the selection uses that hour or it does not. Each case reduces to a shorter array.

<!-- names: prefix, skip, take -->

#### One Entry For Each Prefix

A **prefix** of length `i` is the first `i` hours, which are the indexes 0 through `i - 1`. Let `best[i]` be the highest score of a legal selection that uses only a prefix of length `i`. The final answer is `best[n]`. The entry `best[0]` is 0, because the empty prefix allows only the empty selection.

#### The Skip Case

To **skip** hour `i - 1` means the selection leaves it out. The remaining indexes all lie in the prefix of length `i - 1`, and any legal selection there stays legal. So the best score in this case is `best[i - 1]`.

#### The Take Case

To **take** hour `i - 1` means the selection includes it. Hour `i - 2` is then forbidden, so the rest of the selection lies in the prefix of length `i - 2`. That prefix has no index adjacent to `i - 1`, so every legal selection there combines safely with the new hour. The best score in this case is `value[i - 1] + best[i - 2]`. For `i = 1` there is no hour `i - 2`, so the rest is empty and contributes 0.

#### The Entry Is The Larger Case

Every legal selection falls into exactly one of the two cases, so `best[i] = max(best[i - 1], value[i - 1] + best[i - 2])`. The invariant is that `best[i]` is the highest score of any legal selection within the first `i` hours, and every earlier entry is final when the loop reaches `i`. The empty choice is built in, because `best[0]` is 0 and `max` never returns less than an earlier entry.

<!-- stage: variables -->
### The Prefix Table And Two Candidates

The method reads the array `value` and changes nothing. It keeps three working values.

- **best** is an `int[]` of length `n + 1`; entry `i` is the highest score within the first `i` hours.
- **skip** is `best[i - 1]`, which is the score when the last hour of the prefix stays out.
- **take** is `value[i - 1]` plus the entry two prefixes back, or plus 0 when `i` is 1.

The loop index `i` is a prefix length from 1 to `n`, so the hour it examines is `value[i - 1]`. The table stores prefix lengths and never overwrites `value`. Updating `value` in place would change the caller's data and would also read a number that has already been replaced.

<!-- stage: trace -->
### Two Runs Over Small Forecasts

#### Taking Wins At Most Hours

The first run uses the forecasts `[5, 8, 5, 3, 9, 4]`. Each cell is one hour, and the pointer `i` marks the hour that the loop examines, which is the prefix length minus 1. At each hour the trace shows `skip`, which is the previous best, and `take`, which is the hour's value plus the best from two prefixes back. The variable `best` is the larger of the two. The first step, with the pointer at -1, shows the empty prefix.

At hour 1, taking 8 beats the earlier 5. At hour 2, taking 5 on top of the 5 from hour 0 gives 10 and beats 8. At hour 3, taking 3 on top of 8 gives 11. At hour 4, taking 9 on top of 10 gives 19. Hour 5 offers 4, and taking it gives only 15, so skipping keeps the best at 19.

```trace
{"cells":[5,8,5,3,9,4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"skip":0,"take":0,"best":0},"note":"The empty prefix has the best score 0, so nothing is chosen yet."},{"at":{"i":0},"vars":{"skip":0,"take":5,"best":5},"note":"Hour 0 has value 5. Skipping keeps 0, taking gives 5, so taking wins and best becomes 5."},{"at":{"i":1},"vars":{"skip":5,"take":8,"best":8},"note":"Hour 1 has value 8. Skipping keeps 5, taking gives 8, so taking wins and best becomes 8."},{"at":{"i":2},"vars":{"skip":8,"take":10,"best":10},"note":"Hour 2 has value 5. Skipping keeps 8, taking gives 10, so taking wins and best becomes 10."},{"at":{"i":3},"vars":{"skip":10,"take":11,"best":11},"note":"Hour 3 has value 3. Skipping keeps 10, taking gives 11, so taking wins and best becomes 11."},{"at":{"i":4},"vars":{"skip":11,"take":19,"best":19},"note":"Hour 4 has value 9. Skipping keeps 11, taking gives 19, so taking wins and best becomes 19."},{"at":{"i":5},"vars":{"skip":19,"take":15,"best":19},"note":"Hour 5 has value 4. Skipping keeps 19, taking gives 15, so skipping wins and best becomes 19."}]}
```

#### Skipping Wins At Weak Hours

The second run uses `[2, 10, 3, 3, 12, 2, 9]`. Weak hours show the skip case. At hour 2, the value 3 added to the best from two prefixes back gives only 5, so skipping keeps 10. At hour 5, the value 2 gives 15, so skipping keeps 22.

Hours 1, 4 and 6 give 10 + 12 + 9 = 31, which is the final entry. Each hour compared both cases against exact earlier scores, so no hour needed a guess about its neighbours.

```trace
{"cells":[2,10,3,3,12,2,9],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"skip":0,"take":0,"best":0},"note":"The empty prefix has the best score 0, so nothing is chosen yet."},{"at":{"i":0},"vars":{"skip":0,"take":2,"best":2},"note":"Hour 0 has value 2. Skipping keeps 0, taking gives 2, so taking wins and best becomes 2."},{"at":{"i":1},"vars":{"skip":2,"take":10,"best":10},"note":"Hour 1 has value 10. Skipping keeps 2, taking gives 10, so taking wins and best becomes 10."},{"at":{"i":2},"vars":{"skip":10,"take":5,"best":10},"note":"Hour 2 has value 3. Skipping keeps 10, taking gives 5, so skipping wins and best becomes 10."},{"at":{"i":3},"vars":{"skip":10,"take":13,"best":13},"note":"Hour 3 has value 3. Skipping keeps 10, taking gives 13, so taking wins and best becomes 13."},{"at":{"i":4},"vars":{"skip":13,"take":22,"best":22},"note":"Hour 4 has value 12. Skipping keeps 13, taking gives 22, so taking wins and best becomes 22."},{"at":{"i":5},"vars":{"skip":22,"take":15,"best":22},"note":"Hour 5 has value 2. Skipping keeps 22, taking gives 15, so skipping wins and best becomes 22."},{"at":{"i":6},"vars":{"skip":22,"take":31,"best":31},"note":"Hour 6 has value 9. Skipping keeps 22, taking gives 31, so taking wins and best becomes 31."}]}
```

<!-- stage: code -->
### One Table, One Maximum Per Hour

The method returns the highest score of a legal selection and returns 0 for an empty array. It allocates the table once and fills it from small prefixes to large ones.

```java
static int nonAdjacentBest(int[] value) {
    int n = value.length;
    int[] best = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        int skip = best[i - 1];
        int take = value[i - 1] + (i >= 2 ? best[i - 2] : 0);
        best[i] = Math.max(skip, take);
    }
    return best[n];
}
```

The conditional covers the first prefix, where no earlier entry exists to add. A table of length `n + 1` keeps `best[0]` at 0 without an assignment, because Java zero-fills new arrays. The method runs in O(n) time and uses O(n) memory. For `n` equal to 0, the loop does not run and the method returns `best[0]`, which is 0.

<!-- stage: applicability -->
### Recognizing Choices That Block Neighbours

#### Reading The Cue

Use this method when each position can be used or left out and using one position forbids a nearby position. Typical wording says that no two chosen items may be adjacent, or that a chosen item blocks the next one. The answer is a total over the chosen items, such as the maximum value, and the table indexes prefixes of the input.

#### Checking The Invariant

An **invariant** is a statement that stays true before and after each loop step. Here it says that `best[i]` equals the highest score within the first `i` positions, and every legal selection in a prefix is counted by one of the two cases. Test the empty array, which must return 0 without touching an index. Test one element, where the take case has no earlier entry. Test values of 0 and negative values, where leaving everything out must stay available.

#### Avoiding The False Friend

A **false friend** is a method that passes simple samples yet returns a wrong total on other inputs. Here the false friend is the greedy pick from the naive section, and the next one is picking every other element. For `[9, 1, 1, 9]` the alternating choice of indexes 0 and 2 gives 10, while indexes 0 and 3 give 18. A third false friend is the maximum of the sum of even indexes and the sum of odd indexes, which fails for the same input. Last, an in-place update of the input array would erase values the later comparison still needs.

<!-- stage: exercises -->
### Exercises

#### [Build] Nonadjacent Sum (Author exercise)
<!-- id: dp-takeskip-nonadjacent-sum -->

**Prerequisites.** The prefix table and the maximum of two cases from this lesson.

**Problem.** An array `value` holds a nonnegative integer for each position. A selection is a set of positions in which no two positions are adjacent. Return the largest sum of `value` over any selection. The empty selection is allowed.

**Constraints.** The limits are:
- **Length** satisfies `0 <= value.length <= 1000`, and an empty array returns 0.
- **Value** satisfies `0 <= value[i] <= 1000`.
- **Mutation** is not allowed, because the input array stays unchanged.
- **Result** is an `int`.

**Example 1.** Input `value = [5,8,5]`, output `10`.

**Example 2.** Input `value = [3,2,7,10]`, output `13`.

**Hint.** For the last position, what is the best score if the selection leaves it out, and what is it if the selection uses it?

**Changed decision.** The method writes `max(skip, take)` for every prefix. The take case adds the position's value to the entry two prefixes back, not to the entry one prefix back.

#### [Vary] House Robber With Minimum Spacing (LeetCode 198)
<!-- id: dp-takeskip-spaced-houses -->

**Prerequisites.** The exercise above.

**Problem.** An array `value` holds the money in each house along a street, and an integer `gap` sets the minimum distance between robbed houses. A selection is a set of houses in which every two indexes differ by at least `gap`. Return the greatest total money over all selections, where the empty selection scores 0.

**Constraints.** The limits are:
- **Length** satisfies `0 <= value.length <= 1000`.
- **Value** satisfies `0 <= value[i] <= 1000`.
- **Gap** satisfies `1 <= gap <= 2000`, and a gap of 1 allows adjacent positions.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `value = [6,1,5,7,2]`, `gap = 3`, output `13`.

**Example 2.** Input `value = [3,8,1]`, `gap = 5`, output `8`.

**Hint.** Using position `i - 1` forbids the positions closer than `gap`. Which prefix length still holds only compatible positions, and what if that length is negative?

**Changed decision.** The take case jumps back `gap` prefixes in place of 2. When `gap` exceeds the prefix length, the jump lands before the empty prefix and the rest contributes 0.

#### [Boundary] All Zero And Singleton (Author exercise)
<!-- id: dp-takeskip-zero-singleton -->

**Prerequisites.** The two exercises above.

**Problem.** An array `value` holds an integer for each position, and values may be negative. A selection is a set of positions in which no two positions are adjacent, and the empty selection is allowed. Return an `int[]` of length 2. Entry 0 is the largest sum over all selections. Entry 1 is the smallest number of positions among the selections that reach that sum.

**Constraints.** The limits are:
- **Length** satisfies `0 <= value.length <= 1000`.
- **Value** satisfies `-1000 <= value[i] <= 1000`, and zeros may occur.
- **Empty choice** is legal, so the sum is never below 0.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `value = [0,0,0]`, output `[0,0]`.

**Example 2.** Input `value = [2,0,-4,2,0]`, output `[4,2]`.

**Hint.** If every value is zero or negative, which selection wins, and why must a zero not be counted as a pick?

**Changed decision.** Each table entry stores a pair of sum and count. The take case is allowed to lose, and a tie in sum goes to the smaller count, so zeros are never selected.

#### [Recognize] House Robber II (LeetCode 213)
<!-- id: dp-takeskip-circular-houses -->

**Prerequisites.** All three exercises above.

**Problem.** Houses stand in a circle, and `nums[i]` is the money in house `i`. House `n - 1` is adjacent to house 0, and house `i` is adjacent to house `i + 1`. A selection is a set of houses with no two adjacent. Return the largest total money over any selection.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 100`.
- **Money** satisfies `0 <= nums[i] <= 1000`.
- **Circle** means house 0 and house `n - 1` are adjacent only when `n >= 2`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [4,9,4]`, output `9`.

**Example 2.** Input `nums = [5,1,1,5]`, output `6`.

**Hint.** Houses 0 and `n - 1` cannot both be used. Which two straight-line arrays together cover every legal selection?

**Changed decision.** The method calls the straight-line table twice, once without house 0 and once without house `n - 1`. A single house is answered before any split, because both ranges would be empty.
