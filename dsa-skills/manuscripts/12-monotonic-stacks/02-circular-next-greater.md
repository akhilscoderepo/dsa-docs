<!-- lesson-kind: standard -->
<!-- lesson-id: circular-next-greater -->
## Circular Next Greater

<!-- stage: context -->
### Riders On A Ring Road

A small town has a ring road with a lantern at every junction, and the lanterns have different heights. Each night a watchman wants to know, for every lantern, which brighter one he reaches first when he walks along the ring in the usual direction, passing the last lantern and carrying on from the first. A lantern that is the tallest on the ring has no answer, because the walk comes back to it without meeting anything taller.

On a straight road the watchman would simply stop at the end, and some lanterns would have no answer even though a taller one stands behind them. On a ring, those lanterns can still be answered, by the taller ones that were passed at the start of the walk. The watchman wants to do this with one walk, not with a new walk for every lantern, and without drawing a second copy of the ring on paper.

<!-- stage: naive -->
### Walk Around The Ring From Each One

The direct method takes each lantern in turn and walks around the ring, one junction at a time, until it meets a taller lantern or has gone all the way back.

```java
static int[] nextGreaterAround(int[] h) {
    int n = h.length;
    int[] answer = new int[n];
    for (int i = 0; i < n; i++) {
        answer[i] = -1;
        for (int step = 1; step < n; step++) {
            int j = (i + step) % n;
            if (h[j] > h[i]) { answer[i] = h[j]; break; }
        }
    }
    return answer;
}
```

It is correct, since it checks every other lantern in circular order and takes the first taller one. For the ring `[3, 8, 4]` it returns `[8, -1, 8]`: the lantern 4 wraps around past 3 and then meets 8.

<!-- stage: bottleneck -->
### Every Lantern Walks The Full Ring

If the ring holds equal lanterns, or only one tall lantern, then most walks go all the way around without a success. Each of the `n` walks makes up to `n - 1` comparisons, so the cost is about `n * n`, which is O(n^2). A ring of 100,000 lanterns of equal height needs nearly ten billion comparisons to report that nobody has an answer.

The waste is the same as on the straight road. The walks that start at neighbouring lanterns cover almost the same junctions in almost the same order, and each walk rediscovers that the lanterns it passes are not taller. The ring adds one more thing to handle, the wrap from the last junction back to the first, and the temptation is to copy the whole ring into an array twice as long. That does work, but it builds a second array of `2n` cells only to read the first `n` of them twice.

<!-- stage: insight -->
### Walk Twice, Push Once

Run the unresolved stack of the previous lesson over a **virtual lap** structure: let `j` count from 0 to `2n - 1`, and read the value at `a[j % n]`. The first `n` steps are the real walk, and the next `n` steps replay the same values a second time, so no second array is built. In every step, pop each stack top that the current value strictly exceeds and write its answer. The **modulo index** `j % n` turns the virtual position into a real position, and it is also how the answer's position is recovered when it is needed.

Only the first lap pushes. This **first-lap push** rule matters, because every real position must be on the stack exactly once. If the second lap pushed again, a position would appear twice and could be answered twice, with a wrong or redundant result. The second lap exists only to resolve the positions that were left waiting because the greater value stood before them on the ring.

Two laps are enough because the answer for position `i`, if it exists, lies within the next `n - 1` positions in circular order, and these positions all sit among the virtual indices after `i`, up to `i + n - 1`, which is at most `2n - 2`. The order of the stack is the same as before, so after the second lap the positions still waiting are exactly those with no greater value anywhere on the ring. That is always the maximum value or its tied copies, because a strict comparison never lets an equal value resolve another.

<!-- names: virtual lap, modulo index, first-lap push -->

The cost stays O(n) time, because there are `2n` steps and each real position gets one push and at most one pop. The extra space is the stack plus the answer, and there is no copy of the input.

<!-- stage: variables -->
### The Virtual Index And The Real One

The virtual index `j` runs from 0 to `2n - 1` and marks how far the double walk has gone. The real position is `p = j % n`, and the value read is `a[p]`. The stack holds real positions only, pushed when `j < n`, so each of them is on the stack at most once. The answer array is indexed by real position and starts at -1. Java's `%` keeps the sign of the left operand, so `-1 % n` is `-1` and not `n - 1`. A step backward on the ring must therefore be written `(i - 1 + n) % n`, while the forward step `(i + 1) % n` needs no such care because `j` never goes below zero.

<!-- stage: trace -->
### Wrapping Over The Ring Twice

Take the ring `3, 8, 4, 1, 2`. In the first lap the 3 is pushed, then the 8 pops it and gives it the answer 8, and the 4 and the 1 are pushed on top of the 8. The 2 beats the 1, which receives the answer 2, but it does not beat the 4, so it is pushed. The first lap ends with positions 1, 2 and 4 waiting, holding the values 8, 4 and 2, which fall from bottom to top. Positions 0 and 3 are already answered.

The second lap begins with the 3 at virtual index 5. It beats the 2, so position 4 wraps around and receives 3, and it does not beat the 4. The 8 at virtual index 6 beats the 4, so position 2 receives 8, and the 8 on the stack is its own earlier copy at position 1, which a strict comparison leaves alone. The values after that resolve nothing, and nothing is pushed. The 8 stays at -1. The step to study is the 3 on the second lap, because it answers a position that stood after it on the straight road.

Now take `5, 1, 5, 3`. The first lap leaves positions 0, 2 and 3 waiting, since the 1 is answered by the second 5. On the second lap, the first 5 beats the 3 and nothing else, because it is equal to the two 5s on the stack, so equal values stay unresolved even across the wrap.

```trace
{"cells":[3,8,4,1,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"j":0,"stack":"[0]","answer":"[-1,-1,-1,-1,-1]"},"note":"Virtual index 0 reads position 0 with value 3 on lap 1. Nothing is waiting to be resolved. Position 0 is pushed."},{"at":{"i":1},"vars":{"j":1,"stack":"[1]","answer":"[8,-1,-1,-1,-1]"},"note":"Virtual index 1 reads position 1 with value 8 on lap 1. It is greater than the waiting value at position 0, so each receives 8. Position 1 is pushed."},{"at":{"i":2},"vars":{"j":2,"stack":"[1,2]","answer":"[8,-1,-1,-1,-1]"},"note":"Virtual index 2 reads position 2 with value 4 on lap 1. It does not exceed the waiting top, so nothing is resolved. Position 2 is pushed."},{"at":{"i":3},"vars":{"j":3,"stack":"[1,2,3]","answer":"[8,-1,-1,-1,-1]"},"note":"Virtual index 3 reads position 3 with value 1 on lap 1. It does not exceed the waiting top, so nothing is resolved. Position 3 is pushed."},{"at":{"i":4},"vars":{"j":4,"stack":"[1,2,4]","answer":"[8,-1,-1,2,-1]"},"note":"Virtual index 4 reads position 4 with value 2 on lap 1. It is greater than the waiting value at position 3, so each receives 2. Position 4 is pushed."},{"at":{"i":0},"vars":{"j":5,"stack":"[1,2]","answer":"[8,-1,-1,2,3]"},"note":"Virtual index 5 reads position 0 with value 3 on lap 2. It is greater than the waiting value at position 4, so each receives 3. Lap two pushes nothing."},{"at":{"i":1},"vars":{"j":6,"stack":"[1]","answer":"[8,-1,8,2,3]"},"note":"Virtual index 6 reads position 1 with value 8 on lap 2. It is greater than the waiting value at position 2, so each receives 8. Lap two pushes nothing."},{"at":{"i":2},"vars":{"j":7,"stack":"[1]","answer":"[8,-1,8,2,3]"},"note":"Virtual index 7 reads position 2 with value 4 on lap 2. It does not exceed the waiting top, so nothing is resolved. Lap two pushes nothing."},{"at":{"i":3},"vars":{"j":8,"stack":"[1]","answer":"[8,-1,8,2,3]"},"note":"Virtual index 8 reads position 3 with value 1 on lap 2. It does not exceed the waiting top, so nothing is resolved. Lap two pushes nothing."},{"at":{"i":4},"vars":{"j":9,"stack":"[1]","answer":"[8,-1,8,2,3]"},"note":"Virtual index 9 reads position 4 with value 2 on lap 2. It does not exceed the waiting top, so nothing is resolved. Lap two pushes nothing."}]}
```

```trace
{"cells":[5,1,5,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"j":0,"stack":"[0]","answer":"[-1,-1,-1,-1]"},"note":"Virtual index 0 reads position 0 with value 5 on lap 1. Nothing is waiting to be resolved. Position 0 is pushed."},{"at":{"i":1},"vars":{"j":1,"stack":"[0,1]","answer":"[-1,-1,-1,-1]"},"note":"Virtual index 1 reads position 1 with value 1 on lap 1. It does not exceed the waiting top, so nothing is resolved. Position 1 is pushed."},{"at":{"i":2},"vars":{"j":2,"stack":"[0,2]","answer":"[-1,5,-1,-1]"},"note":"Virtual index 2 reads position 2 with value 5 on lap 1. It is greater than the waiting value at position 1, so each receives 5. Position 2 is pushed."},{"at":{"i":3},"vars":{"j":3,"stack":"[0,2,3]","answer":"[-1,5,-1,-1]"},"note":"Virtual index 3 reads position 3 with value 3 on lap 1. It does not exceed the waiting top, so nothing is resolved. Position 3 is pushed."},{"at":{"i":0},"vars":{"j":4,"stack":"[0,2]","answer":"[-1,5,-1,5]"},"note":"Virtual index 4 reads position 0 with value 5 on lap 2. It is greater than the waiting value at position 3, so each receives 5. Lap two pushes nothing."},{"at":{"i":1},"vars":{"j":5,"stack":"[0,2]","answer":"[-1,5,-1,5]"},"note":"Virtual index 5 reads position 1 with value 1 on lap 2. It does not exceed the waiting top, so nothing is resolved. Lap two pushes nothing."},{"at":{"i":2},"vars":{"j":6,"stack":"[0,2]","answer":"[-1,5,-1,5]"},"note":"Virtual index 6 reads position 2 with value 5 on lap 2. It does not exceed the waiting top, so nothing is resolved. Lap two pushes nothing."},{"at":{"i":3},"vars":{"j":7,"stack":"[0,2]","answer":"[-1,5,-1,5]"},"note":"Virtual index 7 reads position 3 with value 3 on lap 2. It does not exceed the waiting top, so nothing is resolved. Lap two pushes nothing."}]}
```

<!-- stage: code -->
### Double Walk Without A Copy

```java
static int[] nextGreaterCircular(int[] a) {
    int n = a.length;
    int[] answer = new int[n];
    java.util.Arrays.fill(answer, -1);
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j < 2 * n; j++) {
        int p = j % n;
        while (!stack.isEmpty() && a[p] > a[stack.peekLast()]) {
            answer[stack.removeLast()] = a[p];
        }
        if (j < n) stack.addLast(p);      // the second lap resolves, and never pushes
    }
    return answer;
}

static int[] successors(int n, int start) {
    int[] order = new int[n - 1];
    for (int step = 1; step < n; step++) order[step - 1] = (start + step) % n;
    return order;
}
```

The loop makes `2n` iterations with constant extra work each, plus pops that total at most `n`, so the time is O(n) and the extra space is O(n). The condition `j < n` is the whole difference from the straight scan, and removing it makes some positions appear twice on the stack. The helper `successors` lists the circular order for one start, which is the order that the naive method walks and that the double lap reproduces in the aggregate.

<!-- stage: applicability -->
### When A Ring Needs Two Laps

Use two laps when successors wrap from the end to the beginning, and each position still needs the first greater value in circular order. The invariant is that, after the first lap, the stack holds exactly the positions that have no greater value to their right, and during the second lap each of them can only be resolved by a value that stood to its left on the straight road.

The false friend is the physical copy, `concat(a, a)`, which gives the same answers but spends O(n) more memory and invites a push of the second half, which then yields duplicated positions. A second false friend is the one-lap shortcut. It happens to be right when the largest value stands last, since every other position is then answered before the walk ends, and it is wrong for `[3, 8, 4, 1, 2]`, where the 4 and the 2 need the wrap.

Do not stretch the pattern to rings where the walk can pass a position more than once for a different reason, such as a graph with branches, since a stack scan assumes one linear order of visits. For plain arrays with no wrap, a single lap is enough and the second lap would do nothing. Also remember to treat a ring of one value: the position is never resolved, and the answer stays at the default.

<!-- stage: exercises -->
### Exercises

#### [Build] Circular Successor Indices (Author exercise)
<!-- id: ms-circular-successors -->

**Prerequisites.** The previous lesson, and remainders with `%`.

**Problem.** Given the length `n` of a ring of positions numbered `0` to `n - 1` and a starting position `start`, list the other positions in the order in which a walker visits them when leaving `start` in the forward direction and passing the last position into position 0. The list holds `n - 1` positions and never includes `start`.

**Constraints.** 1 <= n <= 10^5 and 0 <= start < n. Do not build an array of length `2n`.

**Example 1.** Input `n = 5`, `start = 3`, output `[4, 0, 1, 2]`.

**Example 2.** Input `n = 1`, `start = 0`, output `[]`, since a ring of one position has no other position.

**Hint.** Which expression turns `start + step` into a valid position? What would `-1 % n` give if you tried to walk backward?

**Changed decision.** First rung: a position is read as a remainder of a virtual index, which later becomes the double lap.

#### [Vary] Virtual Double Scan (Author exercise)
<!-- id: ms-virtual-double-scan -->

**Prerequisites.** The Circular Successor Indices exercise above.

**Problem.** Given an integer array `a`, treat it as a ring read twice, with virtual indices `0` to `2n - 1` where virtual index `j` holds `a[j % n]`. For each real position `i`, return the smallest virtual index `j > i` whose value is strictly greater than `a[i]`, or -1 if no virtual index up to `2n - 1` qualifies. The virtual index may be at least `n`.

**Constraints.** 1 <= a.length <= 10^5 and 0 <= a[i] <= 10^9. Do not allocate a doubled array.

**Example 1.** Input `a = [3, 8, 4, 1, 2]`, output `[1, -1, 6, 4, 5]`.

**Example 2.** Input `a = [2, 1]`, output `[-1, 2]`, so the value 1 is answered by virtual index 2, the first value of the second lap.

**Hint.** What is pushed during the first lap and what is only read during the second? What must the answer store when it is a virtual index?

**Changed decision.** The scan reads `a[j % n]` for two laps and reports the virtual position, not the value, so the wrap becomes visible in the output.

#### [Boundary] All Equal Circular Array (Author exercise)
<!-- id: ms-all-equal-circular -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `a` read as a ring, return for each position the first strictly greater value in circular order, or -1 if none exists. Make sure that arrays whose values are all equal, including a ring of one value, produce -1 everywhere and that the second lap pushes nothing.

**Constraints.** 1 <= a.length <= 10^5 and 0 <= a[i] <= 10^9, so -1 is never a real value. Use no more than `2n` steps and no copy of the array.

**Example 1.** Input `a = [7, 7, 7, 7]`, output `[-1, -1, -1, -1]`.

**Example 2.** Input `a = [5]`, output `[-1]`, because the walk returns to the same position immediately.

**Hint.** Which comparison would wrongly resolve a position by an equal copy of itself on the second lap? How many positions stay on the stack when all values are equal?

**Changed decision.** The comparison is strict through both laps, so equal values never answer each other, even when they meet across the wrap.

#### [Recognize] Next Greater Element II (LeetCode 503)
<!-- id: ms-next-greater-element-ii -->

**Prerequisites.** All three exercises above.

**Problem.** Given a circular integer array `nums`, return an array where entry `i` is the first strictly greater value that you meet when you move forward from position `i`, wrapping from the last element to the first. If there is none, the entry is -1.

**Constraints.** 1 <= nums.length <= 10^4 and -10^9 <= nums[i] <= 10^9. Linear time is expected.

**Example 1.** Input `nums = [1, 2, 1]`, output `[2, -1, 2]`.

**Example 2.** Input `nums = [5, 4, 3, 2, 1]`, output `[-1, 5, 5, 5, 5]`, so every position after the maximum is answered by the wrap.

**Hint.** Combine the virtual double lap with the stack of unresolved positions from the previous lesson. In which lap may a position be pushed?

**Changed decision.** The unresolved stack is run over two virtual laps, with pushes only in the first.
