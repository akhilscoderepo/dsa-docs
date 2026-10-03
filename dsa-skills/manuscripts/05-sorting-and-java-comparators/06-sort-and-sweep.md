<!-- lesson-kind: standard -->
<!-- lesson-id: sort-and-sweep -->
## Sort And Sweep

<!-- stage: context -->
### Lockers That Can Only Move Upward

A school hands out lockers. Every student writes down the locker number they would like, and many write the same number. The office has one strict rule: nobody may be given a lower number than the one they asked for, and no two students may end up with the same locker. A student who asks for 4 may get 4, 5, 6 or anything higher, and the office wants the total of all those upward moves to be as small as possible.

The clerk starts by simply processing the request slips as they arrive. For each slip she checks whether the number is taken, and if it is, she tries the next number, then the next, until she finds a free one. It works, though she notices that when thirty students all ask for the same number, the last of them takes a very long walk down the corridor, trying thirty taken doors before finding an empty one.

<!-- stage: naive -->
### Bump Upward Until A Free Number Appears

In Java, the clerk's method keeps a set of numbers already handed out. Each request is bumped one step at a time until it no longer collides.

```java
static long totalMovesByBumping(int[] requests) {
    Set<Integer> taken = new HashSet<>();
    long moves = 0;
    for (int want : requests) {
        int got = want;
        while (taken.contains(got)) { got++; moves++; }
        taken.add(got);
    }
    return moves;
}
```

It follows the rules for any arrival order, it never gives a student a lower number, and the total it returns is the number of single steps taken.

<!-- stage: bottleneck -->
### Long Walks Past The Same Taken Numbers

When k students ask for the same number, the i-th of them walks past i taken numbers, so that run alone costs about k squared over two steps, and the whole procedure is O(n^2) in the worst case, even though the answer is only a sum. The set lookups also hide a constant factor, and the result can be much larger than an `int` can hold: a hundred thousand requests for the same locker need almost five billion single steps.

What the clerk is missing is a way to know where the corridor is already full without walking it. After processing students in any order, she needs only one fact to answer whether a number is free: the highest number handed out so far in that stretch. That fact becomes available if the requests are first arranged in increasing order, because then every later request is at least as large as every earlier one.

<!-- stage: insight -->
### After Sorting, One Number Is Enough

Once the requests are in nondecreasing order, a left-to-right **sweep** can decide each student's locker from a single remembered number. That number is the **frontier value**: the largest locker number finalized so far. A new request `x` gets `max(x, frontier + 1)`. If `x` is already above the frontier, nothing collides and the student keeps `x`. Otherwise the student moves up to just past the frontier, which is the smallest number that is both at least `x` and unused. The cost of the move is the new number minus `x`, and the frontier becomes the new number.

The reason this is enough is that everything earlier requests could do to later ones is summarized by the frontier. Earlier students took numbers at or below it, and every later request is at least as large as any earlier request, so no free number below the frontier can ever be useful to a later student. A sweep over a sorted sequence is a loop that carries a small summary, and the summary must **finalize** each processed item, meaning that nothing later can change a decision already made.

<!-- names: sweep, frontier value, finalize -->

The same pattern appears whenever the order makes only the neighborhood of the current item relevant. Squaring a sorted array of mixed signs produces values whose order is no longer sorted, and sorting them again restores an order from which the answer can be read directly. Rebuilding a queue from counts is a sweep over people sorted by height, where the summary is the set of positions that are still empty. In every case the sort supplies the order, and the sweep supplies the decision, one item at a time.

Intervals add a new difficulty, since their endpoints carry semantics beyond a single number, and the next chapters on intervals handle that. Here every item is a single comparable value.

<!-- stage: variables -->
### Frontier, Cost And The Running Total

The frontier is the largest value finalized so far, and before the first item it is smaller than any possible request. The cost of an item is the difference between its final value and its request, and the total is the sum of these costs. The total can exceed the range of an `int` because it can reach about n squared over two, so it lives in a `long`. The frontier, when it is the last finalized value, can also exceed any request by up to n, which fits in an `int` for the sizes here but is safer in a `long`.

<!-- stage: trace -->
### A Frontier Walking Over Sorted Requests

The first trace sorts the requests 3, 2, 1, 2, 1, 7 into 1, 1, 2, 2, 3, 7 and sweeps. The second 1 collides with the frontier, so it moves to 2 at a cost of 1. The next request, 2, is not above the frontier, so it moves to 3, and the one after is bumped to 4. The step to study is the final one: the request 7 is far above the frontier, so it keeps its own value and the frontier jumps to 7.

```trace
{"cells":[1,1,2,2,3,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"request":1,"placed":1,"frontier":1,"totalMoves":0},"note":"Request 1. It is the first request, so it keeps its value. The frontier is 1 and the total moves so far are 0."},{"at":{"i":1},"vars":{"request":1,"placed":2,"frontier":2,"totalMoves":1},"note":"Request 1. It is not above the previous frontier, so it moves up to 2. The frontier is 2 and the total moves so far are 1."},{"at":{"i":2},"vars":{"request":2,"placed":3,"frontier":3,"totalMoves":2},"note":"Request 2. It is not above the previous frontier, so it moves up to 3. The frontier is 3 and the total moves so far are 2."},{"at":{"i":3},"vars":{"request":2,"placed":4,"frontier":4,"totalMoves":4},"note":"Request 2. It is not above the previous frontier, so it moves up to 4. The frontier is 4 and the total moves so far are 4."},{"at":{"i":4},"vars":{"request":3,"placed":5,"frontier":5,"totalMoves":6},"note":"Request 3. It is not above the previous frontier, so it moves up to 5. The frontier is 5 and the total moves so far are 6."},{"at":{"i":5},"vars":{"request":7,"placed":7,"frontier":7,"totalMoves":6},"note":"Request 7. It is above the previous frontier, so it keeps 7. The frontier is 7 and the total moves so far are 6."}]}
```

The second trace rebuilds a queue with the free-slot method. People are processed from the shortest to the tallest, and among equal heights the larger count first. Each person takes the empty position that has exactly their count of empty positions before it, since all positions still empty will be taken by people at least as tall. The step to study is the person 3 over 0, who is processed after 3 over 2, and still takes the first empty position.

```trace
{"cells":["2/4","3/2","3/0","4/2","5/0","6/0"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"person":"2/4","slot":4,"line":"_ _ _ _ 2/4 _"},"note":"Place 2/4 in the empty position that has 4 empty positions before it, which is position 4. The line is now _ _ _ _ 2/4 _."},{"at":{"i":1},"vars":{"person":"3/2","slot":2,"line":"_ _ 3/2 _ 2/4 _"},"note":"Place 3/2 in the empty position that has 2 empty positions before it, which is position 2. The line is now _ _ 3/2 _ 2/4 _."},{"at":{"i":2},"vars":{"person":"3/0","slot":0,"line":"3/0 _ 3/2 _ 2/4 _"},"note":"Place 3/0 in the empty position that has 0 empty positions before it, which is position 0. The line is now 3/0 _ 3/2 _ 2/4 _."},{"at":{"i":3},"vars":{"person":"4/2","slot":5,"line":"3/0 _ 3/2 _ 2/4 4/2"},"note":"Place 4/2 in the empty position that has 2 empty positions before it, which is position 5. The line is now 3/0 _ 3/2 _ 2/4 4/2."},{"at":{"i":4},"vars":{"person":"5/0","slot":1,"line":"3/0 5/0 3/2 _ 2/4 4/2"},"note":"Place 5/0 in the empty position that has 0 empty positions before it, which is position 1. The line is now 3/0 5/0 3/2 _ 2/4 4/2."},{"at":{"i":5},"vars":{"person":"6/0","slot":3,"line":"3/0 5/0 3/2 6/0 2/4 4/2"},"note":"Place 6/0 in the empty position that has 0 empty positions before it, which is position 3. The line is now 3/0 5/0 3/2 6/0 2/4 4/2."}]}
```

<!-- stage: code -->
### Squares, Frontier And Free Slots

```java
static int[] sortedSquares(int[] nums) {
    int[] out = new int[nums.length];
    for (int i = 0; i < nums.length; i++) out[i] = nums[i] * nums[i];
    Arrays.sort(out);
    return out;
}

static long minIncrementForUnique(int[] nums) {
    int[] a = nums.clone();
    Arrays.sort(a);
    long cost = 0, frontier = Long.MIN_VALUE;
    for (int x : a) {
        long placed = Math.max(x, frontier + 1);
        cost += placed - x;
        frontier = placed;
    }
    return cost;
}

static int[][] rebuildBySlots(int[][] people) {
    int[][] order = people.clone();
    Arrays.sort(order, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(q[1], p[1]));
    int[][] line = new int[order.length][];
    for (int[] p : order) {
        int empty = -1, at = 0;
        while (true) {
            if (line[at] == null && ++empty == p[1]) break;
            at++;
        }
        line[at] = p;
    }
    return line;
}
```

The squares method is O(n log n), because the squares must be sorted. The increment sweep is O(n log n) for the sort plus O(n) for the loop. The free-slot rebuild scans for the empty position once per person, so it is O(n^2) in the worst case, which is acceptable for the limits of the exercise.

<!-- stage: applicability -->
### When Decisions Only Look Back

Use sort and sweep when, after sorting, a decision about an item depends only on the previous finalized items through a small summary, such as the last value, a running maximum or a count. The invariant to state is what the summary promises: that every item before the current one is final and that the summary captures everything from them that later items could care about. If you cannot say what the summary is in one sentence, the sweep is not ready.

A false friend is a problem where the interval between items matters, such as merging overlapping ranges. A single number cannot say which of two earlier ranges still reaches the current one, so the summary needs more structure, and the dedicated interval chapter gives it. Another false friend is sorting when the original order is part of the answer, as in "return the original index of each result", which needs the index carried along. When the input is already sorted, as in the squares problem with its negative side, a later chapter shows that two pointers give an O(n) answer, so sorting is the simple but not the optimal tool.

In Java, accumulate costs in a `long`, keep `Integer.MIN_VALUE` out of the initial frontier by starting from a `long` sentinel, and do not subtract values that can span the whole `int` range. If a problem allows values as large as the type's limit, `frontier + 1` can overflow an `int`.

<!-- stage: exercises -->
### Exercises

#### [Build] Squares of a Sorted Array (LeetCode 977)
<!-- id: so-sorted-squares -->

**Prerequisites.** The arrays-sort lesson; the idea that sorting supplies an order.

**Problem.** Given an array sorted in nondecreasing order that may hold negative numbers, return a new array of the squares of each number, also in nondecreasing order. Use sorting after squaring, so that the order is supplied by the sort.

**Constraints.** 1 <= nums.length <= 10000 and -10000 <= nums[i] <= 10000, sorted in nondecreasing order. A later chapter gives an O(n) method for this exact input.

**Example 1.** Input `nums = [-6, -2, 1, 5]`, output `[1, 4, 25, 36]`.

**Example 2.** Input `nums = [-3, -3, 0]`, output `[0, 9, 9]`.

**Hint.** Why is the array of squares not sorted even though the input is? Which call restores the order?

**Changed decision.** First rung: the sort is used to restore an order that the transformation destroyed.

#### [Vary] Queue Reconstruction by Height (LeetCode 406)
<!-- id: so-queue-free-slots -->

**Prerequisites.** The sort-and-sweep insight above, and the earlier queue-reconstruction exercise.

**Problem.** Rebuild the same kind of queue as before, from height and count of taller-or-equal people in front, with a different invariant: sort from the shortest to the tallest, with larger counts first among equal heights, and place each person into the empty position that has exactly their count of empty positions before it.

**Constraints.** 1 <= people.length <= 2000 and the input describes at least one valid queue. Use a fixed-size output array with empty slots, and no list insertion.

**Example 1.** Input `[[2,4],[6,0],[3,2],[3,0],[4,2],[5,0]]`, output `[[3,0],[5,0],[3,2],[6,0],[2,4],[4,2]]`.

**Example 2.** Input `[[9,0],[4,1],[9,1]]`, output `[[9,0],[4,1],[9,1]]`.

**Hint.** When a person is placed, which people are still to come, and are they taller or shorter? What do the empty positions before the chosen one represent?

**Changed decision.** The sort direction is reversed, so the summary is the set of empty positions and not a growing list.

#### [Boundary] A Long Run of Equal Values (Author exercise)
<!-- id: so-long-equal-run -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array of non-negative integers, return the smallest total increase that makes every value distinct, when each value may only be raised. Test a run of one hundred thousand equal values, show that the answer exceeds the `int` range, and keep the accumulated cost in a `long`.

**Constraints.** 0 <= nums.length <= 100000 and 0 <= nums[i] <= 100000. The returned total is a `long`.

**Example 1.** Input `nums = [5, 5, 5, 5]`, output 6, since the values become 5, 6, 7, 8.

**Example 2.** Input a hundred thousand zeros, output 4999950000, which is larger than `Integer.MAX_VALUE`.

**Hint.** How large can the total be for a run of k equal values? Where would an `int` accumulator wrap?

**Changed decision.** The data is chosen so the answer leaves the range of `int`, making the accumulator type part of the solution.

#### [Recognize] Minimum Increment to Make Array Unique (LeetCode 945)
<!-- id: so-minimum-increment-unique -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array where one move raises a single element by one, return the minimum number of moves needed to make every element distinct. Sort first, then raise each element to at least one more than the previous finalized value.

**Constraints.** 1 <= nums.length <= 100000 and 0 <= nums[i] <= 100000. Return a `long`, and do not simulate moves one at a time.

**Example 1.** Input `nums = [3, 2, 1, 2, 1, 7]`, output 6.

**Example 2.** Input `nums = [4, 9, 20]`, output 0, since the values are already distinct.

**Hint.** After sorting, what single number tells you the smallest value the current element may take? When is the element already fine?

**Changed decision.** A single remembered number, the frontier, replaces the set of taken values used by the slow method.
