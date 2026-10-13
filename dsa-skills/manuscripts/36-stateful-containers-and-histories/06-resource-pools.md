<!-- lesson-kind: standard -->
<!-- lesson-id: resource-pools -->
## Reuse Freed Identifiers From A Pool

<!-- stage: context -->
### Why Two Clients Share One Session Number

A chat server gives every connected client a session number between 0 and 9 999. When a client disconnects, its cleanup code hands the number back so that a later client can use it. One day a network error runs the cleanup code twice for the same client. Minutes later, two new clients both receive session number 4, and each one starts reading messages meant for the other.

The same failure appears in file descriptor tables, database connection slots, order numbers and block numbers in a memory manager. In each case a fixed set of numbers moves between two states, free and in use. The lesson asks one question. How must the pool store those states so that no number is ever free and in use at once, and so that the next number handed out follows a promised order?

<!-- stage: naive -->
### Keeping A List Of Free Numbers

The direct design keeps a list of the free numbers. Allocation finds the smallest number in the list and removes it. Release appends the returned number to the list.

```java
static final java.util.ArrayList<Integer> free = new java.util.ArrayList<>();

static void start(int n) {
    for (int id = 0; id < n; id++) free.add(id);
}

static int allocate() {
    if (free.isEmpty()) return -1;
    int best = 0;
    for (int i = 1; i < free.size(); i++) if (free.get(i) < free.get(best)) best = i;
    return free.remove(best);
}

static void release(int id) {
    free.add(id);
}
```

With ten numbers, the calls allocate, allocate, release(0), allocate return 0, 1 and then 0 again. The list design is short, it uses memory only for the free numbers, and it gives the right answer when every client releases a number exactly once.

<!-- stage: bottleneck -->
### Counting Duplicates And Scans

```predict
A client calls release(4) twice for the same session number, and then two new clients call allocate. What do the two clients receive, and what does the list look like?

Both clients receive 4 if 4 is the smallest number in the list. The second release appended a second copy of 4, and allocate removes only one copy per call. The list holds a number that is free twice, which contradicts the rule that each number has exactly one state.
```

The list cannot detect the second release, because the only way to learn whether a number is already present is to scan the whole list. Adding that scan makes release cost O(n) in the list length. The allocation scan also costs O(n) per call.

For a pool of 100 000 numbers, allocating every one of them reads 100 000, then 99 999, then 99 998 list entries, and so on. That sum is about 5 billion comparisons, which is O(n^2) over n calls. The cost comes from searching a list for two facts, whether a number is present and which number is smallest.

The deeper problem is that the list answers a question about states only by searching. A state lookup for one specific number should cost O(1). The next section stores the state of each number at the position that the number itself names.

<!-- stage: insight -->
### Storing One State Per Number

#### One Free Flag For Each Number

Store a boolean array `free` of length `n`. The entry `free[id]` is true exactly when `id` is available, so each number has one **free flag** and therefore exactly one state. A number cannot be free twice, because a flag holds a single value.

<!-- names: free flag, scan start, idempotent release -->

#### Release That Ignores A Second Call

A release is **idempotent release** when repeating the same call leaves the pool unchanged. The method reads `free[id]` first. When the flag is already true, or when `id` lies outside 0 to n - 1, the method changes nothing and returns false. Only a number whose flag is false becomes free, and the method returns true. The duplicate cleanup call from the opening therefore has no effect.

#### A Scan Start For The Smallest Free Number

Allocation must return the smallest free number. A field `low` stores the **scan start**: every number below `low` is known to be in use, so allocation begins its scan at `low` and never reads those entries. When allocation finds the free number `id`, it sets the flag to false and moves `low` to `id + 1`. When release frees a number smaller than `low`, it moves `low` back to that number, because a free number now exists below the old scan start.

The scan start keeps allocation fast when releases are rare, since the scan reads only entries that were not yet visited. The worst case stays O(n) per call, for example when a client repeatedly frees the last number and the first number. That cost is acceptable here, and the Vary exercise below removes it with an increasing frontier and a sorted set.

<!-- stage: variables -->
### State Kept Between Calls

The pool stores two fields, `free` and `low`, that together describe one logical state.

- **n** is the number of identifiers, equal to `free.length`, so it is not a separate field.
- **free** is the boolean array where `free[id]` is true when `id` is available.
- **low** is the scan start, the smallest index that may hold a true flag.

The invariant holds before and after every public call: for every `id` below `low`, `free[id]` is false. An allocation that returns `id` leaves `free[id]` false. A release that returns true leaves `free[id]` true and `low <= id`. A call that returns false changes neither field. A call that returns -1 leaves every flag unchanged and only moves `low` to `free.length`, which the invariant allows because every flag is already false.

<!-- stage: trace -->
### Tracing Allocations And Releases

#### A Pool Of Five Numbers

The first trace uses a pool with `n = 5`. The pointer `id` marks the number a call returns or touches, and the pointer `low` marks the scan start. The variable `free` lists the numbers whose flag is true after the call.

Three allocations return 0, 1 and 2, and each one moves `low` just past the number it returns. The call release(1) sets the flag of 1 to true and moves `low` back from 3 to 1. The next allocation scans from 1, finds it free at once and returns 1. Two more allocations return 3 and 4. The final allocation scans from 5 and reads nothing, so it returns -1 and the pool is exhausted without any state change.

```trace
{"cells":["0","1","2","3","4"],"pointers":["id","low"],"steps":[{"at":{"id":0,"low":1},"vars":{"free":"1,2,3,4","result":"0"},"note":"allocate scans from low and returns 0. The flag of 0 becomes false and low moves to 1."},{"at":{"id":1,"low":2},"vars":{"free":"2,3,4","result":"1"},"note":"allocate scans from low and returns 1. The flag of 1 becomes false and low moves to 2."},{"at":{"id":2,"low":3},"vars":{"free":"3,4","result":"2"},"note":"allocate scans from low and returns 2. The flag of 2 becomes false and low moves to 3."},{"at":{"id":1,"low":1},"vars":{"free":"1,3,4","result":"true"},"note":"release(1) finds the flag false, sets it true and returns true. low becomes min(3, 1) = 1."},{"at":{"id":1,"low":2},"vars":{"free":"3,4","result":"1"},"note":"allocate scans from low and returns 1. The flag of 1 becomes false and low moves to 2."},{"at":{"id":3,"low":4},"vars":{"free":"4","result":"3"},"note":"allocate scans from low and returns 3. The flag of 3 becomes false and low moves to 4."},{"at":{"id":4,"low":5},"vars":{"free":"none","result":"4"},"note":"allocate scans from low and returns 4. The flag of 4 becomes false and low moves to 5."},{"at":{"id":5,"low":5},"vars":{"free":"none","result":"-1"},"note":"allocate scans from low and reads no true flag, so it returns -1 and leaves every flag unchanged."}]}
```

#### A Duplicate Release In A Pool Of Four

The second trace uses a pool with `n = 4` and repeats the failure from the opening. After allocations of 0 and 1, the call release(1) returns true and moves `low` back to 1. The second release(1) finds the flag already true, so it returns false and changes nothing. The call release(7) names a number outside the pool and also returns false.

The following allocations return 1, 2 and 3, each exactly once, and the last allocation returns -1. In the list design two of those results would have been the same number. The flag array makes that outcome impossible, because every returned number needed a true flag at the moment of allocation.

```trace
{"cells":["0","1","2","3"],"pointers":["id","low"],"steps":[{"at":{"id":0,"low":1},"vars":{"free":"1,2,3","result":"0"},"note":"allocate scans from low and returns 0. The flag of 0 becomes false and low moves to 1."},{"at":{"id":1,"low":2},"vars":{"free":"2,3","result":"1"},"note":"allocate scans from low and returns 1. The flag of 1 becomes false and low moves to 2."},{"at":{"id":1,"low":1},"vars":{"free":"1,2,3","result":"true"},"note":"release(1) finds the flag false, sets it true and returns true. low becomes min(2, 1) = 1."},{"at":{"id":1,"low":1},"vars":{"free":"1,2,3","result":"false"},"note":"release(1) is already free, so it returns false and changes nothing."},{"at":{"id":4,"low":1},"vars":{"free":"1,2,3","result":"false"},"note":"release(7) is outside the pool, so the pointer rests past the last cell, and the call returns false and changes nothing."},{"at":{"id":1,"low":2},"vars":{"free":"2,3","result":"1"},"note":"allocate scans from low and returns 1. The flag of 1 becomes false and low moves to 2."},{"at":{"id":2,"low":3},"vars":{"free":"3","result":"2"},"note":"allocate scans from low and returns 2. The flag of 2 becomes false and low moves to 3."},{"at":{"id":3,"low":4},"vars":{"free":"none","result":"3"},"note":"allocate scans from low and returns 3. The flag of 3 becomes false and low moves to 4."},{"at":{"id":4,"low":4},"vars":{"free":"none","result":"-1"},"note":"allocate scans from low and reads no true flag, so it returns -1 and leaves every flag unchanged."}]}
```

<!-- stage: code -->
### Allocating And Releasing With Flags

#### The Pool Class

The class below follows the two fields from the variables stage. The loop in `allocate` starts at `low`, and the guard in `release` implements the idempotent rule.

```java
final class IdPool {
    private final boolean[] free;
    private int low;

    IdPool(int n) {
        free = new boolean[n];
        java.util.Arrays.fill(free, true);
        low = 0;
    }

    int allocate() {
        for (int id = low; id < free.length; id++) {
            if (free[id]) {
                free[id] = false;
                low = id + 1;
                return id;
            }
        }
        low = free.length;
        return -1;
    }

    boolean release(int id) {
        if (id < 0 || id >= free.length || free[id]) return false;
        free[id] = true;
        low = Math.min(low, id);
        return true;
    }
}
```

#### Cost And Java Details

- **allocate** costs O(n) time in the worst case and O(1) when `low` points at a free number.
- **release** costs O(1) time, because it reads and writes one array entry.
- **Memory** is O(n), with one byte-sized flag per number in the usual JVM layout.

The bounds check comes before the array read, because `free[-1]` or `free[7]` on a pool of four would throw an `ArrayIndexOutOfBoundsException`. The `||` operator skips the right side once the left side is true, so the order of the three tests matters.

<!-- stage: applicability -->
### When A Pool Of Flags Applies

#### Recognizing The Pattern

Use this design when a fixed set of identifiers moves between free and in use, when release can arrive twice or arrive for a number that was never issued, and when the statement names the order in which freed numbers return. Phrases such as the smallest available number, release a number only once or reject an unknown number point here.

State the invariant before coding: every identifier is in exactly one state, and every helper that changes one field changes the others in the same call. Check that each public method leaves the invariant true on its failure paths as well as its success path.

#### Two False Friends

A list or queue of free numbers is the first false friend. It supplies an order and a cheap removal, but it cannot reject a duplicate, because it holds no per-number state. A priority queue has the same gap: it returns the smallest entry, yet two equal entries are both legal inside it. A flag array supplies the state check, while the order structure supplies the choice, and a pool that needs fast ordered choice keeps both and keeps them consistent.

A counter that only counts how many numbers are free is the second false friend. It cannot tell which numbers are free, so a second release of the same number raises the count above the real total.

#### When Not To Use It

Do not allocate a flag array when the identifier range is huge and few numbers are ever issued, such as ranges up to 10^9. Store an increasing frontier plus a sorted set of returned values instead. Do not use it when the freed units must form contiguous runs, as in a memory allocator, because a single flag cannot tell whether a block of the needed length is free.

<!-- stage: exercises -->
### Exercises

#### [Build] Reusable ID Pool (Author exercise)
<!-- id: sc-pool-id-pool -->

**Prerequisites.** The free flag, the scan start and the idempotent release rule from this lesson.

**Problem.** Design a class `IdPool` for identifiers `0` to `n - 1`. The constructor `IdPool(int n)` marks every identifier free. The method `allocate()` marks the smallest free identifier in use and returns it, or returns `-1` when none is free. The method `release(int id)` returns `true` and marks `id` free when `id` is in use. It returns `false` and changes nothing when `id` is free or outside `0` to `n - 1`.

**Constraints.** The limits are:
- **Pool size** is `1 <= n <= 10^5`.
- **Calls** number at most `10^5` per pool.
- **Identifiers** passed to `release` are any `int` value.
- **Return** is `-1` for an exhausted pool and a boolean for release.

**Example 1.** Input constructor argument `n = 3` and the calls allocate, allocate, release(0), allocate, allocate, allocate, output `0, 1, true, 0, 2, -1`.

**Example 2.** Input constructor argument `n = 2` and the calls release(1), allocate, release(0), release(0), release(5), release(-1), allocate, output `false, 0, true, false, false, false, 0`.

**Hint.** Which single array entry answers whether a release is a duplicate, and which field tells allocation where to start reading?

**Changed decision.** Basic case: the pool stores one state per identifier in an array and rejects a release by reading that entry.

#### [Vary] Smallest Number in Infinite Set (LeetCode 2336)
<!-- id: sc-pool-infinite-set -->

**Prerequisites.** The Reusable ID Pool exercise above.

**Problem.** Design a class `SmallestInfiniteSet` that holds every positive integer at first. The method `popSmallest()` removes the smallest integer in the set and returns it. The method `addBack(int num)` inserts `num` into the set when the set does not hold it, and does nothing otherwise.

**Constraints.** The limits are:
- **Value** `num` satisfies `1 <= num <= 1000`.
- **Calls** number at most `1000` per set.
- **Duplicates** in `addBack` leave the set unchanged.
- **Return** of `popSmallest` is always an existing positive integer.

**Example 1.** Input the calls popSmallest, popSmallest, popSmallest, addBack(1), popSmallest, popSmallest, output `1, 2, 3, null, 1, 4`.

**Example 2.** Input the calls addBack(7), popSmallest, popSmallest, addBack(2), addBack(2), popSmallest, popSmallest, output `null, 1, 2, null, null, 2, 3`.

**Hint.** Every integer at or above some frontier value was never removed. Which removed integers are smaller than that frontier, and which structure returns the smallest of them?

**Changed decision.** The range changes from a fixed array to an unbounded frontier, so only values below the frontier need stored state.

#### [Boundary] Design Phone Directory (LeetCode 379)
<!-- id: sc-pool-phone-directory -->

**Prerequisites.** The Reusable ID Pool exercise above.

**Problem.** Design a class `PhoneDirectory` for numbers `0` to `maxNumbers - 1`. The method `get()` returns the available number that has been available longest, assigns it, and returns `-1` when none is available. The method `check(int number)` returns `true` when `number` is available. The method `release(int number)` makes an assigned number available again at the end of the waiting order, and does nothing when `number` is already available.

**Constraints.** The limits are:
- **Size** is `1 <= maxNumbers <= 10^4`.
- **Numbers** passed to `check` and `release` satisfy `0 <= number < maxNumbers`.
- **Calls** number at most `2 * 10^4` per directory.
- **Initial order** is increasing: `0` is available longest, then `1`, and so on.

**Example 1.** Input constructor argument `maxNumbers = 3` and the calls get, get, check(0), release(0), check(0), release(0), get, get, get, output `0, 1, false, null, true, null, 2, 0, -1`.

**Example 2.** Input constructor argument `maxNumbers = 2` and the calls get, release(1), get, release(1), release(0), get, get, output `0, null, 1, null, null, 1, 0`.

**Hint.** If release only appends to the waiting order, a second release of the same number appends it twice. What must release read first?

**Changed decision.** The order structure becomes a queue with first-in, first-out reuse, and release must read a separate state array before it touches the queue.

#### [Recognize] Design Memory Allocator (LeetCode 2502)
<!-- id: sc-pool-memory-allocator -->

**Prerequisites.** The three exercises above.

**Problem.** Design a class `Allocator` for a memory array of `n` units, all free at first. The method `allocate(int size, int mID)` finds the lowest start index of a run of `size` consecutive free units, marks the run as owned by `mID`, and returns the start, or returns `-1` when no run exists. The method `freeMemory(int mID)` frees every unit owned by `mID`, including units from several allocations, and returns the number of units freed.

**Constraints.** The limits are:
- **Memory size** is `1 <= n <= 1000`.
- **Request size** satisfies `1 <= size <= 1000`.
- **Owner** satisfies `1 <= mID <= 1000`.
- **Calls** number at most `1000` per allocator.

**Example 1.** Input constructor argument `n = 10` and the calls allocate(1,1), allocate(1,2), allocate(1,3), freeMemory(2), allocate(3,4), allocate(1,1), allocate(1,1), freeMemory(1), allocate(4,2), allocate(8,5), output `0, 1, 2, 1, 3, 1, 6, 3, 6, -1`.

**Example 2.** Input constructor argument `n = 6` and the calls allocate(2,7), allocate(2,7), allocate(2,8), freeMemory(7), allocate(3,9), freeMemory(7), allocate(3,9), output `0, 2, 4, 4, 0, 0, -1`.

**Hint.** A single free flag per unit cannot name the owner. Which per-unit value records both the free state and the owner, and how does a scan count a run?

**Changed decision.** The state per unit changes from a boolean to an owner label, and allocation searches for a run of free units and not for a single one.
