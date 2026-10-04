<!-- lesson-kind: standard -->
<!-- lesson-id: sort-and-sweep -->
## Sweep A Sorted Array

<!-- stage: context -->
### Booking Slots That Collide

A booking tool lets customers ask for a slot number. Two customers cannot share a slot, so the tool moves a customer to the next free number when the asked slot is taken, and it reports how many moves it made. A test with a hundred requests runs at once. A batch with 100000 requests for the same slot runs for minutes, although the logic is the same.

The slow batch shows that each new request repeats a search that earlier requests already did. This lesson answers two questions. What must the program remember so that one request needs one decision, and what order of the requests makes that memory enough?

<!-- stage: naive -->
### Probing Upward From The Asked Slot

The direct method keeps the set of taken slots. For each request, it tries the asked slot, then the next number, and so on, until a free slot appears. It counts one move for each number it skips.

```java
static long countMoves(int[] requests) {
    Set<Long> taken = new HashSet<>();
    long moves = 0;
    for (int slot : requests) {
        long candidate = slot;
        while (!taken.add(candidate)) {
            candidate++;
            moves++;
        }
    }
    return moves;
}
```

On the requests `[4, 4, 9]` the first 4 takes slot 4. The second 4 skips to 5 with one move, and 9 takes slot 9. The method returns 1.

<!-- stage: bottleneck -->
### Every Request Walks The Same Chain

```predict
The batch holds 100000 requests for the slot 0. How many moves does the method count in total, and which numbers does the last request test?

The i-th request skips i numbers, so the total is about n * (n - 1) / 2, which is roughly 5 billion and O(n^2). The last request tests every number from 0 up to 99999, all of them already taken.
```

Each request starts at its asked slot and walks over a chain of slots that earlier requests filled. The chain grows with every request, so the work grows with the square of the batch size. The total of 5 billion also exceeds the `int` range, so even the counter needs `long`. The walk answers one question again and again: which is the first free slot at or above the asked slot? If the requests arrive in ascending order, that answer is already known after the previous request.

<!-- stage: insight -->
### Sort Once And Carry A Frontier

When the requests are sorted, the first free slot for a request depends on one number that the previous request leaves behind.

#### What A Sweep Is

A **sweep** is one pass over sorted data in which each item is processed once and in order. A sweep needs a summary of the items before the current one. The summary must be small, and it must contain everything that later items can need.

#### The Frontier Is The Summary

The **frontier** is the smallest slot that no earlier request has taken. Request `i` takes the larger of its asked slot and the frontier. The new frontier is that slot plus one. The cost of the move is the taken slot minus the asked slot, and it is never negative, because the frontier is only used when it exceeds the asked slot.

#### Why Taking The Smallest Slot Is Safe

A **safe move** is a choice that cannot make a later choice worse. Sorted requests make the smallest legal slot a safe move. A later request asks for a slot at least as large as the current request. Any slot below the frontier is taken. Taking a larger slot than necessary can only push the frontier up and add cost later. The invariant after item `i` is that the taken slots are distinct, each is at least its asked slot, and the frontier is one more than the largest taken slot.

<!-- names: sweep, frontier, safe move -->

#### The Cost Of The Sweep

The sort costs O(n log n), and the pass costs O(n). The pass keeps the frontier and the move count, which is O(1) extra space beyond the sorted copy.

<!-- stage: variables -->
### Frontier, Taken Slot And Moves

The pass keeps three values.

- **frontier** is the smallest slot that no earlier request holds, stored as a `long`.
- **taken** is the slot that the current request receives, which is the larger of its asked slot and the frontier.
- **moves** is the sum of `taken - asked` over the requests so far, stored as a `long`.

The frontier and the moves never decrease.

<!-- stage: trace -->
### Two Batches Under The Sweep

#### A Batch With A Collision

Take the requests `[5, 2, 5, 5]`. After sorting they are `2, 5, 5, 5`. The first request takes slot 2, and the frontier becomes 3. The first 5 exceeds the frontier and takes slot 5, so the frontier becomes 6. The second 5 takes slot 6 at a cost of 1, and the third 5 takes slot 7 at a cost of 2. The total is 3.

#### A Batch With A Long Run

Take the requests `[0, 0, 0, 0, 10]`. The four zeros take slots 0, 1, 2 and 3 at costs 0, 1, 2 and 3. The request 10 exceeds the frontier 4 and takes slot 10 at no cost. The total is 6. The frontier never moves backward, and each request makes one decision.

#### Stepping Through Both Batches

```trace
{"cells":[2,5,5,5],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"frontier":"none","moves":0},"note":"Start: no slot is taken, so the frontier is below every request."},{"at":{"i":0},"vars":{"asked":2,"taken":2,"frontier":3,"moves":0},"note":"The frontier is not above the request, so the request keeps its slot. The frontier becomes 3."},{"at":{"i":1},"vars":{"asked":5,"taken":5,"frontier":6,"moves":0},"note":"The frontier is not above the request, so the request keeps its slot. The frontier becomes 6."},{"at":{"i":2},"vars":{"asked":5,"taken":6,"frontier":7,"moves":1},"note":"The frontier is above the request, so the request moves up to the frontier. The frontier becomes 7."},{"at":{"i":3},"vars":{"asked":5,"taken":7,"frontier":8,"moves":3},"note":"The frontier is above the request, so the request moves up to the frontier. The frontier becomes 8."},{"at":{"i":4},"vars":{"frontier":8,"moves":3},"note":"The pass ends with 3 moves in total."}]}
```

```trace
{"cells":[0,0,0,0,10],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"frontier":"none","moves":0},"note":"Start: no slot is taken, so the frontier is below every request."},{"at":{"i":0},"vars":{"asked":0,"taken":0,"frontier":1,"moves":0},"note":"The frontier is not above the request, so the request keeps its slot. The frontier becomes 1."},{"at":{"i":1},"vars":{"asked":0,"taken":1,"frontier":2,"moves":1},"note":"The frontier is above the request, so the request moves up to the frontier. The frontier becomes 2."},{"at":{"i":2},"vars":{"asked":0,"taken":2,"frontier":3,"moves":3},"note":"The frontier is above the request, so the request moves up to the frontier. The frontier becomes 3."},{"at":{"i":3},"vars":{"asked":0,"taken":3,"frontier":4,"moves":6},"note":"The frontier is above the request, so the request moves up to the frontier. The frontier becomes 4."},{"at":{"i":4},"vars":{"asked":10,"taken":10,"frontier":11,"moves":6},"note":"The frontier is not above the request, so the request keeps its slot. The frontier becomes 11."},{"at":{"i":5},"vars":{"frontier":11,"moves":6},"note":"The pass ends with 6 moves in total."}]}
```

<!-- stage: code -->
### Sort Then One Pass

#### Counting The Moves

```java
static long countMoves(int[] requests) {
    int[] sorted = Arrays.copyOf(requests, requests.length);
    Arrays.sort(sorted);
    long frontier = Long.MIN_VALUE;
    long moves = 0;
    for (int asked : sorted) {
        long taken = Math.max(asked, frontier);
        moves += taken - asked;
        frontier = taken + 1;
    }
    return moves;
}
```

#### What The Method Costs

The sort takes O(n log n) time and the loop takes O(n) time. The copy uses O(n) space. Both `frontier` and `moves` are `long`, because a run of 100000 equal values needs about 5 billion moves.

<!-- stage: applicability -->
### When A Frontier Is Enough

#### Look For Neighbors That Decide Everything

Use a sort and a sweep when, in sorted order, each item depends only on the item before it or on one running summary. The invariant is that the summary holds everything that later items can need. Write the summary in one sentence before writing code, and check that one number or one small record states it.

#### Where The Sweep Does Not Apply

A false friend is an item that depends on items far away in sorted order. A problem that asks for two values that add to a target needs a different tool, because the frontier cannot represent all values seen before. Ranges that overlap are also not covered here, because they need rules for endpoints that have their own chapter. Sorting also fails when the problem fixes the input order, such as a time series.

#### Java Details That Cause Failures

A running total of moves can exceed `int`, so declare it as `long`. Initialize the frontier with a value that is below every legal item, such as `Long.MIN_VALUE`, and not with 0, which fails for negative items. Adding 1 to a frontier of `Integer.MAX_VALUE` overflows `int`, so keep the frontier in `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Squares Of A Sorted Array (LeetCode 977)
<!-- id: so-sorted-squares -->

**Prerequisites.** The sort of a primitive array from the earlier lessons.

**Problem.** Let `nums` be an array sorted in nondecreasing order. Return an array of the squares of its values, also in nondecreasing order. This exercise uses a sort of the squares, and a later chapter shows a method that needs no sort.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^4`.
- **Values** satisfy `-10^4 <= nums[i] <= 10^4`, so each square fits in `int`.
- **Input order** is nondecreasing, and duplicates may occur.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [-6, -2, 0, 3]`, output `[0, 4, 9, 36]`.

**Example 2.** Input `nums = [-5, -5, 1]`, output `[1, 25, 25]`.

**Hint.** Squaring changes the order of negative values. Which step puts the squares back in order?

**Changed decision.** Basic case: a sort restores the order that squaring breaks.

#### [Vary] Queue Reconstruction By Height (LeetCode 406)
<!-- id: so-queue-or-none -->

**Prerequisites.** Queue Reconstruction By Height from the lesson on sorting objects, and the sweep from this lesson.

**Problem.** Let `people` be an array of pairs `[h, k]`, where `k` is the number of people in front of this person with height at least `h`. Return a queue in which every `k` is correct. Unlike the earlier exercise, the input may have no valid queue. Return an empty array in that case.

**Constraints.** The limits are:
- **Length** satisfies `0 <= people.length <= 1000`.
- **Heights** satisfy `0 <= h <= 10^6`.
- **Counts** satisfy `0 <= k <= 10^6`, so a count can exceed every possible position.
- **Mutation** of `people` is not allowed.

**Example 1.** Input `people = [[5, 1], [9, 0], [5, 0]]`, output `[[5, 0], [5, 1], [9, 0]]`.

**Example 2.** Input `people = [[4, 0], [4, 0]]`, output `[]`.

**Hint.** After the insertions, what must be checked before the answer is returned, and which count exceeds the list size at insertion time?

**Changed decision.** The sweep must reject invalid input, so the method verifies its partial output instead of trusting the input.

#### [Boundary] A Long Run Of Equal Values (Author exercise)
<!-- id: so-frontier-max -->

**Prerequisites.** The two exercises above and the frontier from this lesson.

**Problem.** Given the integer array `nums`, raise values by whole numbers, never lowering any value, until all values are distinct, using the fewest total increments. Return the largest value of the final array as a `long`. Return 0 for the empty array.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers, including `Integer.MAX_VALUE`.
- **Final values** can exceed the `int` range.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [7, 7, 1]`, output 8.

**Example 2.** Input `nums = [2147483647, 2147483647, 2147483647]`, output 2147483649.

**Hint.** Which variable of the sweep holds the largest taken slot, and in which type must the frontier be stored?

**Changed decision.** The answer is the frontier of the sweep and not its cost, and the frontier passes the `int` range.

#### [Recognize] Minimum Increment To Make Array Unique (LeetCode 945)
<!-- id: so-min-increment -->

**Prerequisites.** All three exercises above.

**Problem.** Take `nums`, an array whose values are non-negative. In one move, add 1 to one value. Return the minimum number of moves that make all values distinct.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** satisfy `0 <= nums[i] <= 10^9`.
- **Answer** can exceed the `int` range and is returned as a `long`.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [5, 2, 5, 5]`, output 3.

**Example 2.** Input `nums = [0, 0, 0, 0, 10]`, output 6.

**Hint.** After sorting, what is the smallest value that the current item can take, given everything before it?

**Changed decision.** The sweep adds up the cost of each decision, and the sort makes each decision depend on the frontier alone.
