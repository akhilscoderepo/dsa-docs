<!-- lesson-kind: standard -->
<!-- lesson-id: array-cycle-state -->
## Array Cycle State

<!-- stage: context -->
### A Trail Of Painted Stones

A mountain trail is marked by stone cairns numbered 1 to n, with a base camp numbered 0 at the foot. On top of every cairn, and on the doorstep of the base camp, lies a flat stone with one number painted on it. The number tells a hiker which cairn to walk to next. No stone is ever painted with 0, so once a hiker leaves the base camp nobody is sent back to it. There are n + 1 stones for n cairns, and a ranger has noticed that some cairn is named on two different stones, which means two different paths of the trail run into the same cairn.

The ranger wants the number of that shared cairn. The stones are old and must not be repainted, turned over or moved, and the ranger carries no notebook and no list of ticks. The hut warden says that a hiker who simply keeps following the stones will learn the answer, but nobody has said how to read it off a walk that never seems to end.

<!-- stage: naive -->
### Tick Every Cairn On The Way

The first idea is to walk the trail from the base camp and keep a tick list with one box per cairn. A hiker ticks the box of every place visited, and the first cairn whose box is already ticked when the hiker arrives is the shared one.

```java
static int duplicateByTicks(int[] stones) {
    boolean[] ticked = new boolean[stones.length];
    int cairn = 0;
    while (!ticked[cairn]) {
        ticked[cairn] = true;
        cairn = stones[cairn];
    }
    return cairn;
}
```

The walk must end, because there are only n + 1 places and each step goes to a place, so some place is eventually reached twice. The first place reached twice is a cairn with two incoming stones, and the contract says that exactly one number is painted more than once, so it is the answer.

<!-- stage: bottleneck -->
### The Tick List Is The Forbidden Notebook

The walk reads at most n + 1 stones, so the time is O(n), which is fine. The cost is the tick list. It has one box for every place, so the memory grows as O(n), and the ranger was told to carry no notebook at all. Replacing the tick list with a sorted copy of the stones or with a count of each number only moves the same O(n) memory somewhere else, and comparing every pair of stones needs O(n^2) time.

What the tick list really records is whether the hiker has been here before, and that is information that the walk itself contains. A hiker who has walked long enough must be going around a loop, and after that the path repeats forever. If the hiker could notice, with a constant number of markers, that the walk has started to repeat, and then find where the loop begins, no list would be needed at all. The place where the loop begins is exactly the cairn with two incoming stones.

<!-- stage: insight -->
### Two Walkers On One Trail

Treat the array as a set of arrows from every index to the index named by its value. Starting at index 0 the walk goes forever along a **tail** of distinct places that leads into a loop, and the loop is a ring that is traversed again and again. Let the tail have `mu` steps from index 0 to the first place on the ring, and let the ring have `lambda` places. The first place on the ring is the **cycle entry**, and it is the duplicate, because it is reached from the last tail place and also from the last ring place, which are two different indices holding the same value.

Release a **slow pointer** that moves one step at a time and a **fast pointer** that moves two steps at a time, both starting at index 0. Once both are on the ring, the fast one gains one place on the slow one at every round, so the gap between them, measured around the ring, shrinks by one each round until it is zero, and the two stand on the same index. At that moment the slow one has taken `t` steps and the fast one `2t`, and they differ by `t` steps, which is a whole number of laps, so `t` is a multiple of `lambda`. The slow one is then `t - mu` places past the entry, so the number of steps still needed to reach the entry is `lambda - (t - mu)` taken modulo `lambda`, which equals `mu` modulo `lambda`.

<!-- names: slow pointer, fast pointer, cycle entry -->

That is the second phase. Put the slow pointer where it is, move the fast pointer back to index 0 and make it slow down to one step at a time. The pointer from index 0 needs exactly `mu` steps to reach the entry. The pointer in the ring needs `mu` steps plus some whole laps to land on the entry, so after `mu` rounds both are on the entry. They cannot meet earlier, because until round `mu` the one from index 0 is still on the tail, which the ring never touches. A small picture helps. Imagine a tail of three steps and a ring of six places. After six rounds the quicker walker has made twelve moves, six more than the other one, which is exactly one lap of the ring, so they share a stone three places past the entry. Three more steps ahead of that stone lies the entry again, and three steps is also the length of the tail, which is why the same count serves both walkers. The invariant of phase one is that the fast pointer is always twice as far along the path as the slow one. The invariant of phase two is that both pointers are the same number of steps away from the entry modulo `lambda`.

<!-- stage: variables -->
### Slow, Fast And The Restarted Walker

`nums` is the read-only array of n + 1 values, each between 1 and n, so every value is a legal index and no read can go out of range. `slow` and `fast` start at 0, and each round `slow` becomes `nums[slow]` while `fast` becomes `nums[nums[fast]]`. The loop is a do-while, because the two start equal and the test is meaningful only after one round. After the meeting, a third variable called `finder` starts at 0, and `finder` and `slow` each move one step per round until they are equal. That shared index is the duplicate, and no cell of `nums` is ever written.

<!-- stage: trace -->
### Meeting Inside The Ring

The first trace uses the array 4, 6, 2, 1, 2, 5, 3. The path from index 0 is 0, 4, 2, 2, 2 and so on, so the tail has two steps and the ring is the single index 2, which points to itself. The step to study is the second one, where the fast pointer arrives on index 2 and the slow pointer arrives there too, so the first phase ends on the ring after only two rounds.

```trace
{"cells":[4,6,2,1,2,5,3],"pointers":["slow","fast","finder"],"steps":[{"at":{"slow":4,"fast":2,"finder":-1},"vars":{"phase":1,"round":1},"note":"Round 1: slow moves to index 4 and fast moves two steps to index 2. They differ, so another round follows."},{"at":{"slow":2,"fast":2,"finder":-1},"vars":{"phase":1,"round":2},"note":"Round 2: slow reads index 2, fast reads two cells and also lands on index 2. They are equal, so phase one ends inside the ring."},{"at":{"slow":2,"fast":-1,"finder":0},"vars":{"phase":2,"round":0},"note":"Phase two starts. slow stays on index 2, and a new walker called finder starts at index 0. Both will now move one step per round."},{"at":{"slow":2,"fast":-1,"finder":4},"vars":{"phase":2,"round":1},"note":"Round 1: finder moves to index 4 and slow moves to index 2. They differ."},{"at":{"slow":2,"fast":-1,"finder":2},"vars":{"phase":2,"round":2},"note":"Round 2: finder and slow both land on index 2. That index is the duplicate."}]}
```

The second trace uses a longer ring. The array 5, 8, 3, 1, 7, 2, 3, 6, 4 sends the walk through 0, 5, 2, 3 and then around the ring 3, 1, 8, 4, 7, 6 back to 3. Phase one needs six rounds and stops on index 4. The step to study is the restart that follows, where the walker started from index 0 and the slow pointer left on index 4 stand far apart, and both then move one step at a time until they land together on index 3, which is the duplicate and not the place where phase one stopped.

```trace
{"cells":[5,8,3,1,7,2,3,6,4],"pointers":["slow","fast","finder"],"steps":[{"at":{"slow":5,"fast":2,"finder":-1},"vars":{"phase":1,"round":1},"note":"Round 1: slow moves to index 5 and fast moves two steps to index 2. They differ, so another round follows."},{"at":{"slow":2,"fast":1,"finder":-1},"vars":{"phase":1,"round":2},"note":"Round 2: slow moves to index 2 and fast moves two steps to index 1. They differ, so another round follows."},{"at":{"slow":3,"fast":4,"finder":-1},"vars":{"phase":1,"round":3},"note":"Round 3: slow moves to index 3 and fast moves two steps to index 4. They differ, so another round follows."},{"at":{"slow":1,"fast":6,"finder":-1},"vars":{"phase":1,"round":4},"note":"Round 4: slow moves to index 1 and fast moves two steps to index 6. They differ, so another round follows."},{"at":{"slow":8,"fast":1,"finder":-1},"vars":{"phase":1,"round":5},"note":"Round 5: slow moves to index 8 and fast moves two steps to index 1. They differ, so another round follows."},{"at":{"slow":4,"fast":4,"finder":-1},"vars":{"phase":1,"round":6},"note":"Round 6: slow reads index 4, fast reads two cells and also lands on index 4. They are equal, so phase one ends inside the ring."},{"at":{"slow":4,"fast":-1,"finder":0},"vars":{"phase":2,"round":0},"note":"Phase two starts. slow stays on index 4, and a new walker called finder starts at index 0. Both will now move one step per round."},{"at":{"slow":7,"fast":-1,"finder":5},"vars":{"phase":2,"round":1},"note":"Round 1: finder moves to index 5 and slow moves to index 7. They differ."},{"at":{"slow":6,"fast":-1,"finder":2},"vars":{"phase":2,"round":2},"note":"Round 2: finder moves to index 2 and slow moves to index 6. They differ."},{"at":{"slow":3,"fast":-1,"finder":3},"vars":{"phase":2,"round":3},"note":"Round 3: finder and slow both land on index 3. That index is the duplicate."}]}
```

<!-- stage: code -->
### Two Phases, No Writes

```java
static int findDuplicate(int[] nums) {
    int slow = 0, fast = 0;
    do {
        slow = nums[slow];
        fast = nums[nums[fast]];
    } while (slow != fast);
    int finder = 0;
    while (finder != slow) {
        finder = nums[finder];
        slow = nums[slow];
    }
    return slow;
}

static int stepsUntilRepeat(int[] nums) {
    boolean[] seen = new boolean[nums.length];
    int index = 0, moves = 0;
    while (!seen[index]) {
        seen[index] = true;
        index = nums[index];
        moves++;
    }
    return moves;
}
```

The first method reads each cell a bounded number of times per round and holds three integers, so the running time grows linearly with n while memory stays constant, and it never assigns to the array. The second one is the walk itself written with a memory, which is the tool for the exercises that ask for the length of a walk.

<!-- stage: applicability -->
### Values That Are Also Positions

Reach for this method when every stored value is itself a legal position in the same array, so that the array describes a next-step rule, and when the contract promises that some place is entered twice. Say the invariant aloud before coding: after phase one the two pointers stand on the ring, and after phase two they stand on the entry. Check the range promise first, since a value outside the array would make the walk read a cell that does not exist.

A false friend is any method that marks, swaps or negates cells to remember a visit. Sign marking and cyclic placement find the same answer in O(n) time, but they write into the array, so they are wrong when the statement says the input is read-only. Another false friend is a two-pointer scan on a sorted array, where the pointers move toward each other by comparing values. Here the pointers never compare values at all, they only compare positions, and the array does not need to be sorted.

In Java, remember that `nums[nums[fast]]` reads two cells in one expression, so a step of the fast pointer is two reads. If the exercise asks for a count of reads, count them where they happen. Use the plain `int` type, because every index stays between 0 and n, and do not try to stop early inside phase one, since the meeting place is only somewhere on the ring.

<!-- stage: exercises -->
### Exercises

#### [Build] Follow Links (Author exercise)
<!-- id: tp-follow-links -->

**Prerequisites.** Reading an array cell by index, and the idea that a value can name another cell.

**Problem.** Given `nums` of length n + 1 whose values all lie between 1 and n, start at index 0 and repeat `index = nums[index]`. Count the moves made until the walk steps onto an index that it has already stood on, counting the start as stood on. Every index that you read must be between 0 and n, and you must be able to say why.

**Constraints.** 1 <= n <= 5000, and the array may be reused afterwards without change. Use a boolean array to remember visits for this exercise.

**Example 1.** Input `nums = [2, 3, 1, 3]`, output 4.

**Example 2.** Input `nums = [1, 1]`, output 2.

**Hint.** Where can the walk be after k moves, and how many different places exist in all? Why does no read ever hit a value of 0?

**Changed decision.** First rung: the array is read as a rule that says where to go next, and the work is to follow it, not to scan it from left to right.

#### [Vary] Find the Duplicate Number (LeetCode 287)
<!-- id: tp-find-duplicate-read-only -->

**Prerequisites.** The follow-links exercise above.

**Problem.** An array `nums` has n + 1 integers, each between 1 and n, and exactly one value occurs more than once, possibly many times. Return that value, without writing into the array and with constant extra memory.

**Constraints.** 1 <= n <= 100000, the array is read-only, and only a few integer variables are allowed. A sorted copy, a count table and sign marking are all ruled out.

**Example 1.** Input `nums = [4, 2, 5, 3, 2, 1]`, output 2.

**Example 2.** Input `nums = [3, 3, 3, 3]`, output 3.

**Hint.** Which place has two incoming arrows, and how can two walkers of different speeds find the ring without remembering where they have been?

**Changed decision.** The tick list from the follow-links exercise is replaced by two moving positions, and the answer is the entry of the ring and not the length of the walk.

#### [Boundary] Immediate Cycle (Author exercise)
<!-- id: tp-immediate-cycle -->

**Prerequisites.** The two exercises above.

**Problem.** Solve the duplicate problem for the smallest legal inputs, n = 1 and n = 2, by the same two-phase method. Read the array only through a checked reader that throws an exception when asked for an index below 0 or above n, and show that no legal array ever triggers it.

**Constraints.** n is 1 or 2, so the array has 2 or 3 cells. Every legal array of those sizes must be answered with zero out-of-range requests and no write.

**Example 1.** Input `nums = [1, 1]`, output 1.

**Example 2.** Input `nums = [2, 2, 1]`, output 2.

**Hint.** In `[1, 1]` where do the slow and the fast pointer stand after one round? Can the walk from index 0 ever return to index 0?

**Changed decision.** The ring may be a single place that points to itself, and the tail may be as short as one step, so the equality test of phase one must be checked after a move and not before it.

#### [Recognize] Phase Two Proof (LeetCode 287)
<!-- id: tp-phase-two-proof -->

**Prerequisites.** All three exercises above.

**Problem.** For the same kind of array, return a pair: the index where phase one stops, and the duplicate that phase two finds. Then decide, from what the pair shows, why restarting one walker at index 0 is needed and why the meeting place of phase one cannot be returned as the answer.

**Constraints.** 1 <= n <= 20000, a read-only array with exactly one repeated value. Phase two must move both pointers one step per round, and the array must be unchanged at the end.

**Example 1.** Input `nums = [4, 2, 5, 3, 2, 1]`, output `[5, 2]`.

**Example 2.** Input `nums = [3, 3, 3, 3]`, output `[3, 3]`.

**Hint.** In the first example, how far is the stopping index from the duplicate along the ring? How many steps does the walker from index 0 need to reach the duplicate?

**Changed decision.** The earlier exercise returned only the duplicate, and this one also reports where phase one stops, which shows that the two places are different in general.
