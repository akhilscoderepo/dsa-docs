<!-- lesson-kind: standard -->
<!-- lesson-id: farthest-frontier -->
## Farthest Frontier

<!-- stage: context -->
### Why A Relay Chain Stops Short

A signal travels along a line of relay stations, numbered from 0. Each station has a power value. A station with power `p` can forward the signal to any of the next `p` stations, or to any station closer than that. The signal starts at station 0. The operator needs to know whether the signal can ever reach the last station.

A simulator that tries every forwarding choice finishes quickly on a ten-station line. On a line of thirty stations it runs for minutes, and on a hundred stations it never finishes. The question of this lesson is how a program answers the same yes-or-no question with one pass over the stations.

<!-- stage: naive -->
### Trying Every Forwarding Choice

The direct plan is a recursive search. From station `i` it tries each forwarding distance from 1 up to the power of the station. It returns true when any choice leads to the last station.

```java
static boolean canReachBySearch(int[] power, int i) {
    if (i >= power.length - 1) return true;          // the last station is reached
    for (int step = 1; step <= power[i]; step++) {   // try every distance
        if (canReachBySearch(power, i + step)) return true;
    }
    return false;
}
```

```predict
Call the method with `power = [3, 2, 1, 0, 4]` and `i = 0`. How many calls does it make before it returns false? For a line of 30 stations with powers `[28, 27, ..., 1, 0, 1]`, how many calls does it make?

On the first array it makes 8 calls. The count doubles with each station that the powers of the line add, so the line of 30 stations needs 2^28 = 268,435,456 calls. The method revisits the same station over and over through different routes.
```

<!-- stage: bottleneck -->
### Counting The Repeated Routes

The search treats every route as new. A route that reaches station 3 through station 1 and a route that reaches it through station 2 do the same work from station 3 onward. The number of routes grows as O(2^n) for the staircase of powers above, and each route repeats the work of the others.

Memorizing the answer for each station would cut the cost to O(n^2), because each station tries up to `n` distances once. That is still too slow for a line of 100,000 stations. The program needs an observation that avoids tracking individual routes. The yes-or-no answer depends on far less than the set of routes.

<!-- stage: insight -->
### One Number Stands For Every Route

#### Which Stations The Signal Can Reach

Let the **reachable prefix** be the stations from 0 up to some index `k` such that the signal can reach every one of them. The reachable stations always form such a prefix. If the signal can reach station 7, it can reach station 5, because any station that forwards to 7 can also forward to a closer station.

Because the stations form a prefix, one number describes them all. That number is the **farthest index** that any reachable station can forward to. Every index up to it is reachable, and no index beyond it is.

#### Updating The Frontier

Scan the stations from left to right. At station `i` with `i <= farthest`, the station is reachable. It can forward as far as `i + power[i]`, so set `farthest` to the larger of the old value and that sum. The indices that need the same smallest number of jumps form a **jump layer**. The value `farthest` is the right edge of all layers that the scan has seen, and the last exercise counts the layers.

If the scan meets an index `i > farthest`, no reachable station forwards that far, and no later station is reachable either. The answer is false. If `farthest` reaches the last index, the answer is true. The scan makes one decision per station and stores one number, which replaces every route that the search tried.

<!-- names: reachable prefix, farthest index, jump layer -->

<!-- stage: variables -->
### Numbers The Scan Keeps

The scan needs three items.

- **power** is the array of station powers, and `power[i]` is the largest distance station `i` can forward.
- **i** is the index of the station under test.
- **farthest** is the largest index that any scanned reachable station can forward to, and it starts at 0.

The test `i > farthest` is the failure check. The update `farthest = max(farthest, i + power[i])` is the only change of state.

<!-- stage: trace -->
### Two Scans Of The Frontier

#### A Line That Reaches The End

The first trace scans `[2, 1, 1, 2, 4]`. The pointer `i` marks the station under test.

Station 0 has power 2, so `farthest` becomes 2. Stations 1 and 2 add no more than index 3, so the frontier moves to 3. Station 3 has power 2 and forwards to index 5, which passes the last index 4. The scan returns true at station 3 and never reads station 4.

```trace
{"cells":[2,1,1,2,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"farthest":2},"note":"Station 0 has power 2, so it forwards to index 2, and farthest becomes 2."},{"at":{"i":1},"vars":{"farthest":2},"note":"Station 1 has power 1, so it forwards to index 2, and farthest becomes 2."},{"at":{"i":2},"vars":{"farthest":3},"note":"Station 2 has power 1, so it forwards to index 3, and farthest becomes 3."},{"at":{"i":3},"vars":{"farthest":5},"note":"Station 3 has power 2, so it forwards to index 5, and farthest becomes 5. This is the last index, so the answer is true."}]}
```

#### A Line That Stops At A Zero

The second trace scans `[3, 2, 1, 0, 4]`. Station 0 sets `farthest` to 3. Stations 1, 2 and 3 each forward to index 3 at most, so `farthest` stays at 3. Station 3 has power 0 and cannot move the frontier. The scan then reaches index 4, which exceeds `farthest`, and returns false.

```trace
{"cells":[3,2,1,0,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"farthest":3},"note":"Station 0 has power 3, so it forwards to index 3, and farthest becomes 3."},{"at":{"i":1},"vars":{"farthest":3},"note":"Station 1 has power 2, so it forwards to index 3, and farthest becomes 3."},{"at":{"i":2},"vars":{"farthest":3},"note":"Station 2 has power 1, so it forwards to index 3, and farthest becomes 3."},{"at":{"i":3},"vars":{"farthest":3},"note":"Station 3 has power 0, so it forwards to index 3, and farthest becomes 3."},{"at":{"i":4},"vars":{"farthest":3},"note":"Index 4 is beyond farthest = 3, so no scanned station forwards that far. The answer is false."}]}
```

<!-- stage: code -->
### Scanning With One Number

```java
static boolean canReach(int[] power) {
    int farthest = 0;
    for (int i = 0; i < power.length; i++) {
        if (i > farthest) return false;               // no station reaches index i
        farthest = Math.max(farthest, i + power[i]);
        if (farthest >= power.length - 1) return true;
    }
    return true;
}
```

The early exit at the last index is optional, but it saves work on long lines. The sum `i + power[i]` stays inside `int` for the limits of this lesson. A line whose powers reach `Integer.MAX_VALUE` needs `long` for the sum.

- **Time** is O(n), because each station is tested once.
- **Space** is O(1), because the scan keeps one integer.

<!-- stage: applicability -->
### Recognizing A Single Frontier

#### Applying The Invariant

Use a frontier when positions lie on a line and a position can reach everything between itself and some far limit. The invariant is that every index up to `farthest` is reachable, and meeting an index beyond it proves failure. Check the invariant by asking whether "can reach 5" always implies "can reach 3".

#### Finding Cases That Break The Precondition

A false friend is a line where a station forwards to exactly one distance, such as a board with fixed jump lengths. Then reaching station 7 does not imply reaching station 5, and the prefix property fails. Backtracking with a memo table is a second false friend for this problem, because it does the right work with much more machinery than the single number needs.

#### Avoiding Java Pitfalls

Compare `i > farthest` before the update, not after, or a station that is not reachable can still extend the frontier. Use `long` when the powers can be large. Test the one-station line, where the answer is true without any jump.

<!-- stage: exercises -->
### Exercises

#### [Build] Update Reachable Prefix (Author exercise)
<!-- id: gr-update-reachable-prefix -->

**Prerequisites.** The frontier scan of this lesson.

**Problem.** Array `power` has at least one entry. From index `i` a jump moves to any index from `i` to `min(i + power[i], n - 1)`, where `n` is the length. Return the largest index that can be reached from index 0.

**Constraints.** The limits are:
- **Count** is `1 <= power.length <= 10^5`.
- **Values** are integers in `0 <= power[i] <= 10^5`.
- **Return** is an index in `0..n-1`.
- **Mutation** does not occur.

**Example 1.** Input `power = [2,3,1,1,4]`, output 4.

**Example 2.** Input `power = [3,2,1,0,4]`, output 3.

**Hint.** At which index should the scan stop reading stations?

**Changed decision.** The method returns the frontier and not a yes-or-no answer.

#### [Vary] Jump Game (LeetCode 55)
<!-- id: gr-jump-game -->

**Prerequisites.** The previous exercise.

**Problem.** Array `nums` has at least one entry. From index `i` a jump moves forward by any distance from 1 to `nums[i]`. Return true when the last index can be reached from index 0, and false otherwise.

**Constraints.** The limits are:
- **Count** is `1 <= nums.length <= 10^4`.
- **Values** are integers in `0 <= nums[i] <= 10^5`.
- **Start** is index 0, and a one-entry array returns true.
- **Mutation** does not occur.

**Example 1.** Input `nums = [2,3,1,1,4]`, output true.

**Example 2.** Input `nums = [3,2,1,0,4]`, output false.

**Hint.** Compare the frontier with the last index after each update.

**Changed decision.** The method answers a yes-or-no question about the last index.

#### [Boundary] Zero Before The Frontier (Author exercise)
<!-- id: gr-zero-before-the-frontier -->

**Prerequisites.** The first exercise.

**Problem.** Array `power` has at least one entry. A zero at index `i` with `i < n - 1` blocks the signal when `i` is reachable and no earlier station forwards beyond `i`. Return the smallest index of a blocking zero, or -1 when no zero blocks.

**Constraints.** The limits are:
- **Count** is `1 <= power.length <= 10^5`.
- **Values** are integers in `0 <= power[i] <= 10^5`.
- **Last index** is never blocking, even when its value is zero.
- **Unreachable zeros** past a block do not count.

**Example 1.** Input `power = [3,2,1,0,4]`, output 3.

**Example 2.** Input `power = [2,0,2,0,4]`, output -1.

**Hint.** What is the value of `farthest` when the scan reaches a harmless zero?

**Changed decision.** The method reports where the frontier stops.

#### [Recognize] Jump Game II (LeetCode 45)
<!-- id: gr-jump-game-ii -->

**Prerequisites.** The frontier scan and the first three exercises.

**Problem.** Array `nums` has at least one entry, and a jump from index `i` may cover any distance from 1 to `nums[i]`. The last index can always be reached. Return the smallest number of jumps that reach the last index from index 0.

**Constraints.** The limits are:
- **Count** is `1 <= nums.length <= 10^4`.
- **Values** are integers in `0 <= nums[i] <= 1000`.
- **Guarantee** is that the last index is reachable.
- **One entry** needs 0 jumps.

**Example 1.** Input `nums = [2,3,1,1,4]`, output 2.

**Example 2.** Input `nums = [1,2,0,1]`, output 2.

**Hint.** Which indices can be reached with exactly `k` jumps, and where does the next group begin?

**Changed decision.** The frontier is split into groups, one group for each jump.
