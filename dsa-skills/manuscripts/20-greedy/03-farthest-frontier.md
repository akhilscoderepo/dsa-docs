<!-- lesson-kind: standard -->
<!-- lesson-id: farthest-frontier -->
## Farthest Frontier

<!-- stage: context -->
### The Relay Towers Of Kestrel Pass

Along Kestrel Pass stand a row of signal towers, numbered from the foot of the mountain to the summit. A message begins at tower zero. Each tower has a lamp of its own strength, and a tower with strength three can pass the message on to any one of the next three towers. A tower with strength zero can receive a message but cannot forward it.

The watch captain wants to know two things. Can a message that starts at the foot ever reach the summit tower? And if it can, what is the fewest number of relays that does it? She has the strengths written in a ledger, and she knows that some towers further up the pass are dead, with strength zero, which makes her nervous about the gaps.

<!-- stage: naive -->
### Follow Every Possible Relay

The first method follows the message. From tower `i` it tries every tower it could be passed to, from the next one up to the farthest the lamp allows, and asks recursively whether the summit can be reached from there.

```java
static boolean canReach(int[] strength, int i) {
    int last = strength.length - 1;
    if (i >= last) return true;
    for (int step = 1; step <= strength[i]; step++) {
        if (canReach(strength, i + step)) return true;
    }
    return false;
}
```

For the minimum number of relays the same recursion keeps the smallest count among the branches that succeed. Either way, every possible chain of relays is examined, so the answers are right. On a ledger of eight towers it answers immediately.

<!-- stage: bottleneck -->
### The Same Towers Are Visited Again

A tower with strength s opens s branches, and a tower reached by many different earlier relays is explored again each time. On a ledger of n towers whose strengths are all large, the number of relay chains grows like O(2^n), and the failing case is the worst, because the recursion must exhaust every chain before it may say no.

Yet most of that exploring is pointless. If a message can reach tower seven by one chain, it does not matter how the message got there, because the same towers lie above it. And when tower seven can be reached, so can every tower below seven and above the one that sent the message, since the sender's lamp covers the whole stretch in between. The recursion treats those towers as separate discoveries, when they all belong to one single block of the pass.

<!-- stage: insight -->
### Track How Far The Message Goes

Every tower that a message can reach lies in a **reachable prefix** of the pass, an unbroken run of towers starting at tower zero. The reason is simple. A tower j is reached by a jump from some earlier reachable tower i, and that jump covers every tower between i and j, so those are reachable as well. Reachability never leaves a hole, which means the whole set can be described by one number.

That number is the **farthest frontier**, the highest tower index that some reachable tower can pass to. Scan the towers from the foot. A tower at index i inside the prefix extends the frontier to the larger of the old frontier and `i + strength[i]`. A tower beyond the frontier proves that the message can never get there, since nothing reachable can jump that far, and every tower above it is cut off as well. The scan then stops with a definite no.

<!-- names: reachable prefix, farthest frontier, jump layer -->

The fewest relays comes from the same picture drawn in bands. The towers reachable with exactly one relay form the first band, the towers reachable with two form the next band just above it, and so on. Each band is called a **jump layer**, and it is an unbroken stretch because the reachable set always is. While the scan walks across one layer, it records the highest tower that any member of that layer could pass to. When the scan reaches the end of the layer, that record is the end of the next layer, and one more relay has been counted. If the record equals the current end, no tower in the layer can forward the message, and the summit is out of reach.

<!-- stage: variables -->
### The Frontier And The Layer Edge

The cursor `i` is the tower being read. For reachability, `far` is the highest index that any tower already scanned could pass to, held as a `long` because `i + strength[i]` can exceed the range of an int. Everything up to `far` is reachable, and the test `i > far` is the failure signal. For the minimum count, `curEnd` is the last tower of the layer being walked, `far` keeps its meaning as the best reach seen from the layer so far, and `jumps` counts layers completed. Only at `i == curEnd` do `jumps` and `curEnd` change. The array itself is never altered.

<!-- stage: trace -->
### Scans That Succeed, Fail And Count

The first trace reads strengths 3, 1, 0, 2, 0, 5 from the foot. Tower zero is inside the prefix and extends the frontier to three. Tower one has strength one and reaches only two, so the frontier stays. Tower two is a dead tower, harmless because the frontier already lies beyond it. Tower three is still inside, and its strength of two lifts the frontier to five. Tower four is dead again, and tower five is the summit and lies inside the frontier, so the message arrives.

The second trace reads 2, 1, 0, 0, 3. The frontier reaches two from tower zero and stays at two, since tower one adds only up to two and tower two adds nothing. Tower three lies beyond the frontier, so the scan stops with a no. The third trace counts relays on 4, 1, 1, 3, 1, 1, 1. The first layer is tower zero alone with record four. Walking towers one to four raises the record to six at tower three, and at tower four the layer ends, so the second relay is counted and the summit lies inside.

```trace
{"cells":["3","1","0","2","0","5"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"far":3},"note":"Tower 0 with strength 3 reaches 3, so the frontier grows from 0 to 3."},{"at":{"i":1},"vars":{"far":3},"note":"Tower 1 with strength 1 reaches only 2, which does not beat the frontier 3, so it stays."},{"at":{"i":2},"vars":{"far":3},"note":"Tower 2 is dead with strength 0, and the frontier 3 already lies beyond it, so nothing changes."},{"at":{"i":3},"vars":{"far":5},"note":"Tower 3 with strength 2 reaches 5, so the frontier grows from 3 to 5."},{"at":{"i":4},"vars":{"far":5},"note":"Tower 4 is dead with strength 0, and the frontier 5 already lies beyond it, so nothing changes."},{"at":{"i":5},"vars":{"far":10},"note":"Tower 5 is the summit and lies inside the frontier 10, so the message arrives."}]}
```

```trace
{"cells":["2","1","0","0","3"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"far":2},"note":"Tower 0 with strength 2 reaches 2, so the frontier grows from 0 to 2."},{"at":{"i":1},"vars":{"far":2},"note":"Tower 1 with strength 1 reaches only 2, which does not beat the frontier 2, so it stays."},{"at":{"i":2},"vars":{"far":2},"note":"Tower 2 is dead with strength 0 and sits exactly on the frontier 2, so the frontier cannot grow."},{"at":{"i":3},"vars":{"far":2,"verdict":"cut off"},"note":"Tower 3 lies beyond the frontier 2, so no reachable tower can pass a message this far and the scan stops with a no."}]}
```

```trace
{"cells":["4","1","1","3","1","1","1"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"far":4,"curEnd":4,"jumps":1},"note":"Tower 0 is the first layer on its own, with record 4, so relay number 1 is counted and the next layer ends at 4."},{"at":{"i":1},"vars":{"far":4,"curEnd":4,"jumps":1},"note":"Tower 1 has strength 1 and reaches 2, so the record is 4. The layer continues."},{"at":{"i":2},"vars":{"far":4,"curEnd":4,"jumps":1},"note":"Tower 2 has strength 1 and reaches 3, so the record is 4. The layer continues."},{"at":{"i":3},"vars":{"far":6,"curEnd":4,"jumps":1},"note":"Tower 3 has strength 3 and reaches 6, so the record is 6. The layer continues."},{"at":{"i":4},"vars":{"far":6,"curEnd":6,"jumps":2},"note":"Tower 4 ends the layer. The record is 6, so relay number 2 is counted and the next layer ends at 6."}]}
```

<!-- stage: code -->
### One Scan For Each Question

```java
static boolean canReach(int[] strength) {
    long far = 0;
    for (int i = 0; i < strength.length; i++) {
        if (i > far) return false;                    // cut off: nothing reachable jumps this far
        far = Math.max(far, (long) i + strength[i]);
    }
    return true;
}

static int fewestRelays(int[] strength) {
    int n = strength.length;
    int jumps = 0;
    long curEnd = 0, far = 0;
    for (int i = 0; i < n - 1; i++) {
        far = Math.max(far, (long) i + strength[i]);
        if (i == curEnd) {                            // the layer is finished
            if (far == curEnd) return -1;             // nobody in the layer can forward
            jumps++;
            curEnd = far;
            if (curEnd >= n - 1) break;
        }
    }
    return jumps;
}
```

Each loop visits every tower once and keeps three numbers, so both methods run in O(n) time with O(1) extra memory. The cast to `long` happens before the addition, and the layer loop stops at the second to last tower because the summit needs no further relay. A one-tower ledger needs zero relays, and the loop body never runs.

<!-- stage: applicability -->
### When A Single Reach Number Suffices

Use the frontier when positions lie on a line, each position offers a range of moves forward, and the question is whether an end can be reached or in how many steps. The invariant is that every index up to `far` is reachable and that finding an index beyond it proves failure. For the layered count, the added invariant is that the indices of one layer form a contiguous block ending at `curEnd`.

The false friend is the backtracking search, which explores exponentially many chains that the frontier dominates. A closer false friend is a move rule that is not a range. If each tower must pass the message exactly `strength[i]` steps and no fewer, the reachable set is no longer a prefix, and a single number cannot describe it. The same applies when moves have costs, where the shortest total cost needs shortest-path methods from Chapter 24 or dynamic programming from Chapter 26.

In Java, add in `long` before comparing, because `i + strength[i]` can wrap past `Integer.MAX_VALUE`. Zeros are harmless inside the frontier and fatal only at its edge, so test `i > far` before reading the tower.

<!-- stage: exercises -->
### Exercises

#### [Build] Update Reachable Prefix (Author exercise)
<!-- id: gr-update-reachable-prefix -->

**Prerequisites.** The indexed scan from Chapter 01; the idea that a variable can summarise a prefix.

**Problem.** Tower `i` can pass a message to any of the next `strength[i]` towers. A message starts at tower zero. Return the highest tower index that the message can reach, never more than the last index. Scan only towers that lie inside the current frontier.

**Constraints.** 1 <= strength.length <= 100000 and 0 <= strength[i] <= 2147483647. Sums of an index and a strength must not overflow.

**Example 1.** Input `strength = [3, 1, 0, 2, 0, 5]`, output 5.

**Example 2.** Input `strength = [1, 0, 9, 9]`, output 1, since tower one is dead and the towers beyond it cannot be reached.

**Hint.** Which towers is it safe to read? What single number is enough to describe all of them?

**Changed decision.** First rung: the reachable towers are summarised by one frontier index, and only towers inside it extend it.

#### [Vary] Jump Game (LeetCode 55)
<!-- id: gr-jump-game-reach -->

**Prerequisites.** The reachable-prefix exercise above.

**Problem.** Starting at index 0 of an array of non-negative integers, you may move from index `i` to any index from `i + 1` to `i + nums[i]`. Return whether the last index can be reached.

**Constraints.** 1 <= nums.length <= 10000 and 0 <= nums[i] <= 100000.

**Example 1.** Input `nums = [2, 0, 0, 1]`, output false.

**Example 2.** Input `nums = [1, 1, 1, 0]`, output true, since a zero at the last index is not read as a move.

**Hint.** What does it mean when the scan reaches an index larger than the frontier? What does the answer depend on at the final index?

**Changed decision.** The return value changes from a number to a verdict, and the failure test `i > far` becomes the exit.

#### [Boundary] Zero Before The Frontier (Author exercise)
<!-- id: gr-zero-before-frontier -->

**Prerequisites.** The two exercises above.

**Problem.** Return the smallest index that no message starting at index 0 can reach, or -1 if every index is reachable. A zero is harmless when an earlier index already jumps beyond it.

**Constraints.** 1 <= nums.length <= 100000 and 0 <= nums[i] <= 2147483647.

**Example 1.** Input `nums = [3, 0, 0, 0, 1]`, output 4, since the frontier stops at 3.

**Example 2.** Input `nums = [4, 0, 0, 0, 0]`, output -1, since the first jump crosses every zero.

**Hint.** At which index does the scan first see `i > far`? What does a very large strength do to `i + nums[i]` in 32-bit arithmetic?

**Changed decision.** The answer is the position where the invariant breaks, and zeros matter only at the edge of the frontier.

#### [Recognize] Jump Game II (LeetCode 45)
<!-- id: gr-jump-layers -->

**Prerequisites.** All three exercises above.

**Problem.** Using the same moves as the reachability exercise, return the fewest moves that take index 0 to the last index. Return -1 if the last index cannot be reached, and 0 if the array has a single element.

**Constraints.** 1 <= nums.length <= 100000 and 0 <= nums[i] <= 1000000.

**Example 1.** Input `nums = [4, 1, 1, 3, 1, 1, 1]`, output 2.

**Example 2.** Input `nums = [2, 0, 0, 5]`, output -1.

**Hint.** Where does one move's worth of indices end? What is the best record of reach seen from inside it?

**Changed decision.** The frontier is now read in layers, with a counter that grows at each layer boundary and a stuck test at that boundary.
