<!-- lesson-kind: combination -->
<!-- lesson-id: duplicate-with-two-speeds -->
## Find A Duplicate With Two Speeds

<!-- stage: context -->
### Three Fixes And Three Broken Requirements

A code review lists three ways to find the repeated id in a shared table of 100,001 ids, each between 1 and 100,000. The first fix stores every id in a set. The second fix flips the sign of the slot that each id names. The third fix sorts the table. The reviewer rejects each of them for a different reason, and the table must stay unchanged and use almost no extra memory.

All three fixes treat the ids as data. The table also names its own slots, because every id is a legal index. The problem is to see which property of the table makes a fourth fix possible and why that property is not enough alone.

<!-- stage: contributions -->
### What Each Part Adds

The table contributes the links. Because the table has `n + 1` slots and every value lies between 1 and `n`, reading slot `i` gives a legal next slot, and no slot points to slot 0. Following the links from slot 0 is a walk that never leaves the array and never returns to its start. The table does not say where the walk repeats, and it does not say which slot to report.

The two speeds contribute the detection. A pointer that moves one link per round and a pointer that moves two links per round must meet if the walk contains a loop. The two speeds do not tell where the loop begins, and without the bounded table they have no guarantee that a loop exists or that every read is in range. Only the table's bounds create a loop whose first slot is the repeated value, and only the two speeds find that slot without writing.

<!-- stage: naive -->
### Sorting A Copy And Comparing Neighbors

The direct method copies the table, sorts the copy and looks for two equal neighbors. It leaves the original table unchanged.

```java
static int findRepeatSorted(int[] nums) {
    int[] copy = nums.clone();
    Arrays.sort(copy);
    for (int i = 1; i < copy.length; i++) {
        if (copy[i] == copy[i - 1]) return copy[i];
    }
    return -1;
}
```

For `[3, 1, 3, 4, 2]` the sorted copy is `[1, 2, 3, 3, 4]`, and the method returns 3. The method respects the no-write rule for the original table, and it is correct for every legal input.

```predict
The table holds 100,001 ids. How much extra memory does `findRepeatSorted` use compared with the table, and how many comparisons does the sort make?

The copy holds 100,001 ints, as much as the table itself. The sort makes about 100,001 * 17, or 1.7 million comparisons. The method costs O(n log n) time and O(n) extra space, and a method that follows links can do the same work in O(n) time and O(1) space.
```

<!-- stage: bottleneck -->
### The Table Already Holds The Links

The sorted copy answers a question about order, and the problem only asks for a repeated value. The copy costs O(n) memory, which doubles a table that was shared to save memory, and the sort costs O(n log n) time. All of this work serves one comparison of equal neighbors.

The table already encodes a structure that finds the repeat without sorting. Following each value as a link gives a walk that revisits a slot, and the first revisited slot is a slot with two incoming links. The method needs only a way to find that slot with a fixed number of variables, and the two speeds provide it.

<!-- stage: insight -->
### Why The Meeting Leads To The Repeat

#### Why A Loop Exists And Starts At The Repeat

The walk from slot 0 has at most `n + 1` different slots to visit, and it never leaves them, so it must revisit one. Let `t` be the number of slots visited before the loop, and let `c` be the number of slots in the loop. The first slot of the loop is the **entry point**. Two different slots point to it: the last slot before the loop, which is slot 0 when `t = 1`, and the last slot of the loop. Two slots with the same value mean that the entry point is a repeated value.

#### Where The Two Speeds Meet

Let the slow pointer move one link per round and the fast pointer two links per round. After `k` rounds the slow pointer has made `k` links and the fast pointer `2k` links. Once both are in the loop, the fast pointer gains one link per round. They meet at the **meeting point** when the gap `2k - k = k` is a multiple of `c`. The meeting point lies inside the loop, but it is usually not the entry point.

#### Why Restarting Finds The Entry

At the meeting point `k` is a multiple of `c` and `k >= t`. The slow pointer is then `k - t` links inside the loop. A pointer that restarts at slot 0 reaches the entry point after `t` links. Measure positions inside the loop from the entry point, with the entry at position 0. The pointer at the meeting point sits at position `(k - t)` modulo `c`. After `t` more links it sits at position `k` modulo `c`, which is 0 because `k` is a multiple of `c`. Both pointers therefore arrive at the entry point after `t` rounds.

<!-- names: entry point, meeting point -->

#### The Cost

The first phase takes at most `t + c` rounds, and the second takes `t` rounds. The method stores two slot numbers and reads the table without writing, so it costs O(n) time and O(1) space.

<!-- stage: variables -->
### The Quantities In The Argument

The argument uses the following quantities, and the last three change while the method runs.

- **t** is the number of slots visited once before the loop, and it is fixed by the table.
- **c** is the number of slots in the loop, and it is fixed by the table.
- **k** is the number of rounds of phase one, and it grows by one per round.
- **slow** and **fast** are the two slot numbers, and each round updates them.

The program never computes `t` or `c`. The proof uses them to show that the second phase ends at the entry point.

<!-- stage: trace -->
### The Arithmetic Of The Two Phases

#### Phase One Closes The Gap

The table is `[1, 3, 4, 2, 2]`, and the walk is `0, 1, 3, 2, 4, 2, 4, ...`. So `t = 3` and `c = 2`. The trace tracks the number of links each pointer has made. The gap between them grows by one per round. The pointers can meet only after both are inside the loop and the gap is a multiple of the loop length 2. That happens in round 4, and the trace lists the number of links of each pointer in every round.

```trace
{"cells":[1,3,4,2,2],"pointers":["slow","fast"],"steps":[{"at":{"slow":1,"fast":3},"vars":{"links slow":"1","links fast":"2","gap":"1"},"note":"After round 1, slow made 1 links and fast made 2 links. The gap is 1."},{"at":{"slow":3,"fast":4},"vars":{"links slow":"2","links fast":"4","gap":"2"},"note":"After round 2, slow made 2 links and fast made 4 links. The gap is 2."},{"at":{"slow":2,"fast":4},"vars":{"links slow":"3","links fast":"6","gap":"3"},"note":"After round 3, slow made 3 links and fast made 6 links. The gap is 3."},{"at":{"slow":4,"fast":4},"vars":{"links slow":"4","links fast":"8","gap":"4"},"note":"After round 4, slow made 4 links and fast made 8 links. The gap is 4. The pointers meet because the gap 4 is a multiple of the loop length 2."}]}
```

#### Phase Two Reaches The Entry

After phase one, `slow` restarts at slot 0 and `fast` stays at the meeting point. Each round moves both pointers by one link. After `t = 3` rounds both stand on slot 2, which is the repeated value. The trace lists the rounds one by one, so that the equal distances from the entry point are visible.

```trace
{"cells":[1,3,4,2,2],"pointers":["slow","fast"],"steps":[{"at":{"slow":0,"fast":4},"vars":{"rounds":"0"},"note":"Phase two starts. slow restarts at slot 0 and fast stays at the meeting point, slot 4."},{"at":{"slow":1,"fast":2},"vars":{"rounds":"1"},"note":"Round 1: both pointers move one link, to slots 1 and 2."},{"at":{"slow":3,"fast":4},"vars":{"rounds":"2"},"note":"Round 2: both pointers move one link, to slots 3 and 4."},{"at":{"slow":2,"fast":2},"vars":{"rounds":"3"},"note":"Round 3: both pointers move one link, to slots 2 and 2. They meet at slot 2, the repeated value."}]}
```

<!-- stage: code -->
### The Method With A Read-Only View

```java
static int repeatedValue(IntUnaryOperator view) {
    int slow = 0, fast = 0;
    do {
        slow = view.applyAsInt(slow);
        fast = view.applyAsInt(view.applyAsInt(fast));
    } while (slow != fast);
    slow = 0;
    while (slow != fast) {
        slow = view.applyAsInt(slow);
        fast = view.applyAsInt(fast);
    }
    return slow;
}
```

The parameter is an `IntUnaryOperator`, a function from a slot number to a value. It offers no way to write, so the type itself forbids the sign marking and the cyclic placement of the alternative fixes. Calling `view.applyAsInt(i)` returns `nums[i]`, and a caller can pass `i -> nums[i]`. The method needs the contract that every value lies between 1 and `n` for a table of `n + 1` slots, or a read may leave the array.

<!-- stage: applicability -->
### Choosing Among The Fixes

#### The Invariant

The invariant of phase two is that the two pointers are the same number of links from the entry point. It holds right after phase one, because the meeting point is `k` links from slot 0 with `k` a multiple of the loop length. The contract supplies the guarantee that makes the entry point equal a repeated value: the table has more slots than distinct values.

#### The False Friend

The nearest wrong idea is to pick a fix by speed alone. Sign marking and cyclic placement run in O(n) time and O(1) space, and both write to the table. A set reads only and costs O(n) space. Sorting costs O(n log n) and needs a copy. Each of these fixes breaks one requirement. The two speeds are the only choice that is read-only with O(1) space, which is why the contract decides the method.

#### Conditions That Break The Fit

The method needs every value to be a legal slot and no value to equal 0. It needs a repeated value to exist, so a table of `n + 1` slots with `n` distinct values is required. A table that may be modified allows the simpler cyclic placement, and a table that may use O(n) space allows a set. When two or more different values repeat, the method returns one of them and does not choose the smallest.

<!-- stage: exercises -->
### Exercises

#### [Build] Value-As-Next-Index (Author exercise)
<!-- id: tp-contract-check -->

**Prerequisites.** The bounded table of the contribution stage.

**Problem.** Take an integer array `nums` with at least two slots. Let `n = nums.length - 1`. Return the smallest index whose value is not between 1 and `n` inclusive. Return `-1` when every value is legal. A legal table is one in which following values as links never leaves the array and never returns to slot 0.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 10^5`.
- **Values** are any `int` values.
- **Legal values** are the integers from 1 to `nums.length - 1`.
- **Mutation** of the input does not occur.

**Example 1.** Input `nums = [3,1,3,4,2]`, output `-1`.

**Example 2.** Input `nums = [1,3,2]`, output 1, because the length is 3, so `n = 2` and the value 3 at index 1 is not legal.

**Hint.** Which two values break the walk: one that leaves the array and one that returns to the start?

**Changed decision.** The check protects the pointer walk, because a value of 0 or a value above `n` breaks the argument or the array bounds.

#### [Vary] Find the Duplicate Number (LeetCode 287)
<!-- id: tp-duplicate-count -->

**Prerequisites.** The first exercise above and the proof of this lesson.

**Problem.** Take an integer array `nums` with `n + 1` slots and values between 1 and `n`, in which exactly one value repeats. Return `{d, c}`, where `d` is the repeated value and `c` is the number of slots that hold `d`. The array must not change. The original problem returns only the value, and this version also counts its slots.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 10^5`.
- **Values** are `int` values from 1 to `nums.length - 1`.
- **Repeat** is exactly one value, which can appear many times.
- **Mutation** is forbidden, and the extra space is O(1).

**Example 1.** Input `nums = [3,1,3,4,2]`, output `{3,2}`.

**Example 2.** Input `nums = [2,2,2,2,2]`, output `{2,5}`.

**Hint.** Find `d` with the two phases first. How can one more pass over the table produce the count?

**Changed decision.** The answer adds a count, so a second pass is needed after the two phases.

#### [Boundary] Duplicate Near Start (Author exercise)
<!-- id: tp-duplicate-near-start -->

**Prerequisites.** The second exercise above.

**Problem.** An array `nums` follows the table contract of the previous exercise. Return `{i, j}` with `i < j`, the two smallest indexes whose value is the repeated value. The array must not change.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 10^5`.
- **Values** are `int` values from 1 to `nums.length - 1`, with exactly one repeated value.
- **Result** names the first two slots that hold the repeated value.
- **Mutation** is forbidden.

**Example 1.** Input `nums = [1,1]`, output `{0,1}`.

**Example 2.** Input `nums = [1,3,4,2,2]`, output `{3,4}`.

**Hint.** The repeated value is the entry point. Which scan finds its first two positions, and does the scan need the walk?

**Changed decision.** The answer is a pair of positions, and a duplicate at the very start leaves a tail of length one.

#### [Recognize] Compare Alternatives (Author exercise)
<!-- id: tp-read-only-view -->

**Prerequisites.** All exercises above and the false friend of this lesson.

**Problem.** A table of `n + 1` slots with values between 1 and `n` hides exactly one repeated value. The method receives the number `n` and an `IntUnaryOperator` named `view`, where `view.applyAsInt(i)` returns the value in slot `i`. The operator offers no way to write. Return the repeated value.

**Constraints.** The limits are:
- **n** is `1 <= n <= 10^5`.
- **Slots** are numbered from 0 to `n`.
- **Values** are from 1 to `n`, with exactly one repeated value.
- **Access** is by `view.applyAsInt(i)` only.

**Example 1.** Input `n = 4` and a table `[3,1,3,4,2]`, output 3.

**Example 2.** Input `n = 1` and a table `[1,1]`, output 1.

**Hint.** A method that has no write access cannot mark or place values. Which alternative remains that uses constant extra space?

**Changed decision.** The type of the input rules out the fixes that write to the table, so the method must be the one that only reads.
