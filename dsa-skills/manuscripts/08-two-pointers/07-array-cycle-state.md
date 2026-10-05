<!-- lesson-kind: standard -->
<!-- lesson-id: array-cycle-state -->
## Follow Values As Indexes

<!-- stage: context -->
### A Duplicate In A Read-Only Table

A shared lookup table holds 100,001 slot numbers, and each slot number lies between 1 and 100,000. One number appears more than once, and the table is mapped read-only, so no code may write to it. A checker must report the repeated number. Marking visited slots, as one usually does, writes into the table and fails at once. A copy of the table is possible but doubles the memory of a structure that was shared to save memory.

The table is both data and a set of addresses. The question is how a program can find the repeated number using the values only as places to read, with no writes and a constant number of extra variables.

<!-- stage: naive -->
### Remembering Every Number In A Set

The direct method walks the table and stores each number in a hash set. The first number that is already in the set is the repeat.

```java
static int findRepeatSlow(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int x : nums) {
        if (!seen.add(x)) return x;
    }
    return -1;
}
```

For `[3, 1, 3, 4, 2]` the method returns 3 after it sees the second 3. The method does not write to `nums`, so it respects the read-only table. It pays in memory instead.

```predict
The table holds 100,001 numbers and the repeated number appears last. How many entries does the set hold when the method returns, and how does the memory grow with the table?

The set holds 100,000 entries, one for each distinct number before the repeat. Each boxed `Integer` and each hash entry costs far more than the 4 bytes of an `int` slot. The extra space is O(n), as large as the table itself.
```

<!-- stage: bottleneck -->
### The Table Already Contains A Map

The set stores information that the table already holds. Each value is a legal index, so the table tells the program where to read next from every slot. Following these links needs no memory beyond the current position. The set repeats O(n) memory to remember what the links already encode.

A walk that starts at index 0 and moves to `nums[index]` each time must run out of new slots, because the table has only `n + 1` slots. The walk then comes back to a slot it has seen. The repeat that the program wants is hidden in the shape of that walk.

<!-- stage: insight -->
### Two Speeds Find The Repeated Place

#### Values As Next Indexes

Read `nums[i]` as the **next index** after `i`. The contract makes this safe: the table has `n + 1` slots and every value lies between 1 and `n`, so every value is a legal index, and no value points to index 0. The walk from index 0 is a path of indexes that eventually repeats. After a **tail** of indexes visited once, the walk runs around a **cycle**, a loop of indexes that it visits again and again.

#### The Entry Is The Repeated Value

The first index of the cycle is the **entry**. Two different indexes point to the entry: one on the tail, or index 0, and one on the cycle. Two indexes that hold the same value mean that value is repeated. The entry index equals the repeated value, so finding the entry solves the problem.

#### Floyd's Algorithm In Two Phases

**Floyd's algorithm** uses two pointers that move at different speeds along the walk. In phase one, `slow` advances by one link per round and `fast` advances by two links. They must meet inside the cycle, because the fast pointer gains one step on the slow pointer per round. In phase two, one pointer returns to index 0, and both pointers move one step per round. They meet at the entry. The reason is that the number of steps from the meeting point to the entry, going around the cycle, equals the tail length plus a whole number of laps of the cycle, so the restarted pointer and the other pointer arrive together.

<!-- names: next index, tail, cycle, entry, Floyd's algorithm -->

#### The Cost

Each phase takes O(n) steps and stores two indexes. The method uses O(1) extra space and never writes to the table.

<!-- stage: variables -->
### Two Pointers And Their Phases

The method keeps two indexes, and both change.

- **slow** is the index of the slow pointer, and it follows `slow = nums[slow]` each round.
- **fast** is the index of the fast pointer, and it follows `fast = nums[nums[fast]]` each round.

Phase one starts both at index 0 and ends when they hold the same index. Phase two moves `slow` back to index 0 and moves both pointers one step per round until they meet. The meeting index of phase two is the entry. The table `nums` is read and never written.

<!-- stage: trace -->
### Two Walks Through The Same Rule

#### A Duplicate With A Short Tail

The input is `[3, 1, 3, 4, 2]`. The walk from index 0 reaches index 3 and then runs around the cycle `3, 4, 2`. Phase one ends when the pointers meet at index 2. Phase two starts `slow` at 0, advances both pointers one step per round, and meets at index 3, which is the repeated value.

```trace
{"cells":[3,1,3,4,2],"pointers":["slow","fast"],"steps":[{"at":{"slow":3,"fast":4},"vars":{"phase":"1","round":"1"},"note":"Phase one, round 1: slow moves one step to index 3 and fast moves two steps to index 4."},{"at":{"slow":4,"fast":3},"vars":{"phase":"1","round":"2"},"note":"Phase one, round 2: slow moves one step to index 4 and fast moves two steps to index 3."},{"at":{"slow":2,"fast":2},"vars":{"phase":"1","round":"3"},"note":"Phase one, round 3: slow moves one step to index 2 and fast moves two steps to index 2. The pointers meet."},{"at":{"slow":0,"fast":2},"vars":{"phase":"2","round":"0"},"note":"Phase two starts: slow returns to index 0 and fast stays at the meeting index 2."},{"at":{"slow":3,"fast":3},"vars":{"phase":"2","round":"1"},"note":"Phase two, round 1: both pointers move one step, slow to index 3 and fast to index 3. They meet at index 3, the repeated value."}]}
```

#### A Duplicate With A Longer Tail

The input is `[1, 3, 4, 2, 2]`. The walk visits `0, 1, 3, 2, 4` and then returns to 2, so the tail has three indexes and the cycle has two. The two phases use the same rules, and phase two ends at index 2.

```trace
{"cells":[1,3,4,2,2],"pointers":["slow","fast"],"steps":[{"at":{"slow":1,"fast":3},"vars":{"phase":"1","round":"1"},"note":"Phase one, round 1: slow moves one step to index 1 and fast moves two steps to index 3."},{"at":{"slow":3,"fast":4},"vars":{"phase":"1","round":"2"},"note":"Phase one, round 2: slow moves one step to index 3 and fast moves two steps to index 4."},{"at":{"slow":2,"fast":4},"vars":{"phase":"1","round":"3"},"note":"Phase one, round 3: slow moves one step to index 2 and fast moves two steps to index 4."},{"at":{"slow":4,"fast":4},"vars":{"phase":"1","round":"4"},"note":"Phase one, round 4: slow moves one step to index 4 and fast moves two steps to index 4. The pointers meet."},{"at":{"slow":0,"fast":4},"vars":{"phase":"2","round":"0"},"note":"Phase two starts: slow returns to index 0 and fast stays at the meeting index 4."},{"at":{"slow":1,"fast":2},"vars":{"phase":"2","round":"1"},"note":"Phase two, round 1: both pointers move one step, slow to index 1 and fast to index 2."},{"at":{"slow":3,"fast":4},"vars":{"phase":"2","round":"2"},"note":"Phase two, round 2: both pointers move one step, slow to index 3 and fast to index 4."},{"at":{"slow":2,"fast":2},"vars":{"phase":"2","round":"3"},"note":"Phase two, round 3: both pointers move one step, slow to index 2 and fast to index 2. They meet at index 2, the repeated value."}]}
```

<!-- stage: code -->
### Floyd's Algorithm In Java

```java
static int findDuplicate(int[] nums) {
    int slow = 0, fast = 0;
    do {
        slow = nums[slow];
        fast = nums[nums[fast]];
    } while (slow != fast);
    slow = 0;
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    return slow;
}
```

Phase one uses a `do while` loop, because both pointers start equal at index 0 and a plain `while` would stop before the first step. Every dereference stays in range, because every value lies between 1 and `n` and the table has `n + 1` slots. The method never writes to `nums`. The smallest legal input `[1, 1]` meets at index 1 in phase one and returns 1.

<!-- stage: applicability -->
### When Following Values Fits

#### The Invariant

The invariant of phase one is that both pointers are on the walk, and the distance between them grows by one per round once both are on the cycle. The invariant of phase two is that each pointer is the same number of steps from the entry, so equal speed makes them meet there. The contract supplies the guarantee that makes the entry exist: more slots than distinct values.

#### The False Friend

The nearest wrong idea is to mark visited slots by negating them, or to place each value at its own index by swapping. Both methods run in O(n) time and O(1) space, and both write to the table. They fail on a read-only table and change the caller's data. A second false friend is the linked list version of this algorithm, where nodes are objects. Here the links are array values, and the method depends on the bound that every value is a legal index.

#### Conditions That Break The Fit

The method needs every value to be a legal index and a repeat to exist. A value of 0 would send the walk back to index 0 and put index 0 inside the cycle, and then the entry no longer equals a repeated value. A value outside the range reads outside the array and throws an exception. A table with several repeated values still returns one of them, and the method does not say which one is first.

<!-- stage: exercises -->
### Exercises

#### [Build] Follow Links (Author exercise)
<!-- id: tp-follow-links -->

**Prerequisites.** The value-as-next-index reading of this lesson.

**Problem.** Take an integer array `nums` of length `n >= 1` in which every value is a legal index from 0 to `n - 1`. Start at index 0 and move to `nums[index]` repeatedly. Return the number of distinct indexes visited before the walk first returns to an index it has already visited.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values from 0 to `nums.length - 1`.
- **Walk** starts at index 0 and ends at the first repeated index.
- **Mutation** of the input does not occur.

**Example 1.** Input `nums = [1,2,0]`, output 3.

**Example 2.** Input `nums = [0]`, output 1.

**Hint.** Every value is a legal index, so no step reads outside the array. How can you remember which indexes you have visited?

**Changed decision.** Basic case: only the walk is new, and a visited array is allowed.

#### [Vary] Find the Duplicate Number (LeetCode 287)
<!-- id: tp-find-duplicate -->

**Prerequisites.** The first exercise and Floyd's algorithm from this lesson.

**Problem.** Take an integer array `nums` of length `n + 1` whose values lie between 1 and `n`. At least one value repeats. Return a value that appears more than once. Do not modify the array and use O(1) extra space.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 10^5`, so `n >= 1`.
- **Values** are `int` values from 1 to `n`.
- **Repeat** may appear more than twice.
- **Mutation** is forbidden, and the extra space is O(1).

**Example 1.** Input `nums = [3,1,3,4,2]`, output 3.

**Example 2.** Input `nums = [2,2,2,2,2]`, output 2.

**Hint.** Read `nums[i]` as the next index after `i`. Which index do two different slots point to?

**Changed decision.** The walk is the same, and phase two turns the meeting point into the entry.

#### [Boundary] Immediate Cycle (Author exercise)
<!-- id: tp-immediate-cycle -->

**Prerequisites.** The code stage of this lesson.

**Problem.** Take an integer array `nums` that satisfies the contract of the previous exercise. Run the two phases of Floyd's algorithm and return `{m, e}`, where `m` is the index at which the two pointers meet in phase one and `e` is the index at which they meet in phase two.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 10^5`.
- **Values** are `int` values from 1 to `nums.length - 1`.
- **Phase one** starts both pointers at index 0 and moves `slow` one link and `fast` two links per round.
- **Mutation** of the input does not occur.

**Example 1.** Input `nums = [1,1]`, output `{1,1}`.

**Example 2.** Input `nums = [1,3,4,2,2]`, output `{4,2}`.

**Hint.** For `[1,1]`, what do `slow` and `fast` hold after the first round, and does any read leave the array?

**Changed decision.** The smallest input meets at once, and the answer shows that every read stays in range.

#### [Recognize] Tail And Cycle Lengths (Author exercise)
<!-- id: tp-tail-cycle-lengths -->

**Prerequisites.** All exercises above.

**Problem.** Take an integer array `nums` that satisfies the contract of the second exercise. Walk from index 0. Return `{t, c}`, where `t` is the number of indexes visited once before the cycle begins, and `c` is the number of indexes in the cycle.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 10^5`.
- **Values** are `int` values from 1 to `nums.length - 1`.
- **Tail** counts the indexes before the entry, including index 0, so `t >= 1`.
- **Mutation** of the input does not occur, and the extra space is O(1).

**Example 1.** Input `nums = [3,1,3,4,2]`, output `{1,3}`.

**Example 2.** Input `nums = [1,1]`, output `{1,1}`.

**Hint.** After phase one the pointers hold one index of the cycle. How can you count the cycle length, and how far does `slow` travel in phase two?

**Changed decision.** The answer asks for the two lengths, and the proof of phase two shows that the tail length equals the number of steps in phase two.
