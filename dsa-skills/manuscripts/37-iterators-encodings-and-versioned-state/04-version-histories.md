<!-- lesson-kind: standard -->
<!-- lesson-id: version-histories -->
## Version Histories

<!-- stage: context -->
### Asking What A Setting Used To Be

A configuration service holds 100 000 settings. Before every deployment an operator saves a checkpoint, and after an incident the operator asks one question again and again: what was setting 7 at checkpoint 12? The service keeps taking new writes while these questions arrive, so the answer cannot come from the live values. It must come from a record of the past.

Most settings do not change between two checkpoints. A deployment edits a handful of them. The record therefore carries a lot of repeated information if it stores every setting at every checkpoint. The same shape appears in three other systems. A document editor restores an earlier revision. A bank ledger reports a balance as of a given date. A cache answers what a key held at an earlier time.

This lesson asks one question. How does a program answer queries about an earlier version while it still accepts new writes, and without paying for a full copy of the data per version?

<!-- stage: naive -->
### Copying Everything At Every Checkpoint

The direct method copies the whole array at every checkpoint. A query then reads one cell of the stored copy. The class below keeps a list of copies, and `snap` appends a clone of the current values.

```java
final class NaiveSnapshots {
    private final long[] current;
    private final java.util.List<long[]> copies = new java.util.ArrayList<>();

    NaiveSnapshots(int length) { current = new long[length]; }

    void set(int index, long value) { current[index] = value; }

    int snap() {
        copies.add(current.clone());   // copies every cell, changed or not
        return copies.size() - 1;
    }

    long get(int index, int snapId) { return copies.get(snapId)[index]; }
}
```

Every call returns the right answer. With 3 settings and 2 checkpoints, a test reads the stored copies and finds the expected numbers, so the class looks finished.

<!-- stage: bottleneck -->
### Counting The Copied Cells

```predict
The array has 100 000 cells and the program takes 50 000 snapshots. Between two snapshots exactly 3 cells change. How many numbers does the naive class store, and how many of them carry new information?

The naive class stores 100 000 times 50 000, which is 5 billion numbers, and about 40 GB for 8-byte values. Only 3 times 50 000, which is 150 000 numbers, carry new information. The rest repeat a value that an earlier copy already holds.
```

The naive `snap` costs O(n) time and O(n) space for every call, where `n` is the array length. After `s` snapshots the memory is O(n * s). A workload with long arrays and frequent checkpoints exhausts memory long before it exhausts time.

The waste has a precise cause. A cell that did not change between two snapshots appears twice with the same value. The information in the history is only the list of changes, and the number of changes is the number of `set` calls, which is far smaller than `n * s`. A better class must store each change once and rebuild any past value from the changes. The next section shows how to store them so that a query finds the right change quickly.

<!-- stage: insight -->
### Search The Latest Stored Change

#### Keep One Version History Per Cell

A **version history** is the list of changes to one cell, written as pairs of a version number and the value that the cell took at that version. The list follows the order of the versions. A cell that was never written has an empty list. The memory of the whole structure is the total number of changes, so it grows with the number of writes and not with the number of snapshots.

<!-- names: version history, floor search, coalesced write -->

#### Answer A Query With A Floor Search

A query names a version `v`. The correct answer is the value of the latest change whose version is at most `v`, because a change with a larger version had not happened yet. Finding that change is a **floor search**: among sorted keys, find the largest key that is less than or equal to the target. The history is sorted. Binary search therefore finds the change in O(log k) time for `k` changes. Binary search for the first version greater than `v` and step back one position. When that first position is 0, no change is at or before `v`, and the query returns the default value of the contract.

#### Merge Writes That Share A Version

A **coalesced write** replaces the last pair of a history when a new write carries the same version, instead of appending a second pair. Two writes in one snapshot interval are one change as far as any query can tell, because a query can name the version but not the moment inside it. The rule keeps each version at most once per history. Without it, the history would contain two pairs with equal versions, and the floor search would have to decide which one to return.

#### The Invariant That Makes Search Valid

The invariant says that the versions inside each history are strictly increasing. Writes arrive in time order, so the new version is never smaller than the last one. A larger version appends and an equal version replaces. The strict order is exactly what binary search needs, and the query result does not depend on how many writes happened in between.

<!-- stage: variables -->
### What One History Stores

The class keeps one history per cell and one counter for the current version. A query adds a target version.

- **versions** is the sorted array of version numbers in one history, held as `long`.
- **values** is the array of values in the same order, so `values[k]` belongs to `versions[k]`.
- **current** is the version that new writes receive, and for a snapshot array it equals the number of snapshots taken so far.
- **target** is the version named by a query.
- **position** is the first index in `versions` with a version greater than `target`, and `position - 1` is the answer slot.

The invariant is `versions[0] < versions[1] < ...` in every history, and a query with `position == 0` returns the default value.

<!-- stage: trace -->
### Tracing A Search And A Snapshot Run

#### A Floor Search In One History

The first trace searches the history of one cell. The versions are 2, 5, 9, 14 and 20, with values 30, 10, 40, 20 and 50. The query asks for version 11. The pointers `lo` and `hi` bound the search window, and `mid` is the index that the step inspects.

The window starts as the whole history, from 0 to 5. The middle index 2 holds version 9, which is not above 11, so the first greater version lies to the right and `lo` moves to 3. The next middle index 4 holds version 20, which is above 11, so `hi` moves to 4. Index 3 holds version 14, which is also above 11, so `hi` moves to 3. The window is now empty. The first greater version sits at index 3, the answer slot is index 2, and the value is 40. The change at version 9 is the latest one that happened by version 11.

```trace
{"cells":["2","5","9","14","20"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"query":11},"note":"Start: the window covers all 5 versions, and the query asks for version 11."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"query":11,"version":9},"note":"Version 9 at index 2 is at most 11, so the first greater version lies to the right and lo becomes 3."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"query":11,"version":20},"note":"Version 20 at index 4 is above 11, so the first greater version is at index 4 or earlier and hi becomes 4."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"query":11,"version":14},"note":"Version 14 at index 3 is above 11, so the first greater version is at index 3 or earlier and hi becomes 3."},{"at":{"lo":3,"hi":3,"mid":3},"vars":{"query":11,"answer":40},"note":"The window is empty. The first greater version is at index 3, so the answer slot is index 2 and the value is 40."}]}
```

#### A Snapshot Array With Pending Writes

The second trace runs a snapshot array of length 3 whose cells start at 0. A write goes to a pending table and a snapshot moves each pending entry into the history of its cell. The pointer `op` marks the operation that just finished.

Two writes to cell 0 leave one pending entry, because the second write replaces the first. The first `snap` returns id 0 and moves the entry into the history of cell 0 as the pair (0, 6). A write to cell 1 and a second `snap` give id 1 and the pair (1, 4) in cell 1. Cell 2 never changes, so its history stays empty and every query on it returns the starting value 0. A query for cell 1 at id 0 searches a history whose first version is 1, finds no version at or before 0 and returns the starting value. The same query at id 1 returns 4.

```trace
{"cells":["set(0,5)","set(0,6)","snap","set(1,4)","snap","get(1,0)","get(1,1)","get(2,1)"],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"pending":"{0:5}","histories":"c0=[];c1=[];c2=[]"},"note":"Write 5 to cell 0. The pending table gets a new entry."},{"at":{"op":1},"vars":{"pending":"{0:6}","histories":"c0=[];c1=[];c2=[]"},"note":"Write 6 to cell 0. The pending table replaces the earlier entry for this cell."},{"at":{"op":2},"vars":{"pending":"{}","histories":"c0=[(0,6)];c1=[];c2=[]"},"note":"Snapshot id 0: each pending entry moves into the history of its cell with version 0."},{"at":{"op":3},"vars":{"pending":"{1:4}","histories":"c0=[(0,6)];c1=[];c2=[]"},"note":"Write 4 to cell 1. The pending table gets a new entry."},{"at":{"op":4},"vars":{"pending":"{}","histories":"c0=[(0,6)];c1=[(1,4)];c2=[]"},"note":"Snapshot id 1: each pending entry moves into the history of its cell with version 1."},{"at":{"op":5},"vars":{"pending":"{}","histories":"c0=[(0,6)];c1=[(1,4)];c2=[]"},"note":"Query cell 1 at snapshot 0: the floor search returns 0, the starting value, because no stored version is at most 0."},{"at":{"op":6},"vars":{"pending":"{}","histories":"c0=[(0,6)];c1=[(1,4)];c2=[]"},"note":"Query cell 1 at snapshot 1: the floor search returns 4."},{"at":{"op":7},"vars":{"pending":"{}","histories":"c0=[(0,6)];c1=[(1,4)];c2=[]"},"note":"Query cell 2 at snapshot 1: the floor search returns 0, the starting value, because no stored version is at most 1."}]}
```

<!-- stage: code -->
### Writing The History And The Array

#### One Cell With A Floor Search

The class below stores one history in two parallel arrays. The method `add` appends a change and the method `valueAt` runs the floor search. The versions are `long`, so a timestamp near 10^15 does not overflow an `int`.

```java
final class CellHistory {
    private long[] versions = new long[4];
    private long[] values = new long[4];
    private int size;

    void add(long version, long value) {
        if (size > 0 && versions[size - 1] == version) {
            values[size - 1] = value;           // same version: replace the last pair
            return;
        }
        if (size == versions.length) {          // grow by doubling: amortized O(1)
            versions = java.util.Arrays.copyOf(versions, size * 2);
            values = java.util.Arrays.copyOf(values, size * 2);
        }
        versions[size] = version;               // larger version: append
        values[size++] = value;
    }

    long valueAt(long target, long fallback) {
        int lo = 0, hi = size;                  // search for the first version > target
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;          // unsigned shift avoids int overflow
            if (versions[mid] <= target) lo = mid + 1; else hi = mid;
        }
        return lo == 0 ? fallback : values[lo - 1];   // lo == 0 means no change yet
    }
}
```

#### The Snapshot Array

The array class keeps a pending table for the current interval and one history per index that has ever changed. Here each history is a `TreeMap` from snapshot id to value, and its `floorEntry` method is the floor search from the previous section. The table holds at most one entry per index, so `snap` costs time proportional to the number of distinct indices written since the last snapshot.

```java
final class ChangeLogArray {
    private final long start;
    private final java.util.TreeMap<Integer, Long>[] cells;
    private final java.util.HashMap<Integer, Long> pending = new java.util.HashMap<>();
    private int snaps;

    @SuppressWarnings("unchecked")
    ChangeLogArray(int length, long start) {
        this.start = start;
        this.cells = new java.util.TreeMap[length];   // null until the cell first changes
    }

    void set(int index, long value) { pending.put(index, value); }

    int snap() {
        for (var e : pending.entrySet()) {
            int i = e.getKey();
            if (cells[i] == null) cells[i] = new java.util.TreeMap<>();
            cells[i].put(snaps, e.getValue());   // version = id of this snapshot
        }
        pending.clear();
        return snaps++;
    }

    long get(int index, int snapId) {
        if (snapId >= snaps) return -1;          // snapshot not taken yet
        if (cells[index] == null) return start;  // the cell never changed
        var floor = cells[index].floorEntry(snapId);   // latest id at most snapId
        return floor == null ? start : floor.getValue();
    }
}
```

#### Cost

- **add** costs O(1) amortized time and O(1) space per change.
- **valueAt** and the `floorEntry` call cost O(log k) time and O(1) space for a history of `k` changes.
- **snap** costs O(w) time, where `w` is the number of distinct indices written since the previous snapshot.

<!-- stage: applicability -->
### When A Query Names An Earlier Version

#### Recognizing The Pattern

Use this method when updates create versions and a later query names a version or a time. The tell is a pair of operations such as `set` and `get(version)`, or `set` and `get(key, timestamp)`. Check two properties before coding. The versions of one history must arrive in non-decreasing order, which holds for a counter, a clock or a snapshot id. The stored changes must be enough to rebuild every answer, which holds when each change records the new value and not a difference.

#### A False Friend

A full copy per snapshot is a false friend of a correct solution. It returns correct answers on every small test and fails only when the array and the snapshot count both grow. A second false friend is a hash map from version to value. It answers exact versions and returns nothing for a version between two changes, although that query has a well-defined answer. The invariant of strictly increasing versions is what turns the question into a search.

#### Edge Cases To Check Every Time

A query before the first change must return the declared default and must not read index minus one. A query after the last change returns the last value. A query equal to a stored version returns that version's own value, not the previous one. When timestamps or versions can exceed the `int` range, the arrays and the comparisons must use `long`. When two writes can share a version, decide in the contract whether the later write replaces the earlier one, and apply that decision in one place.

<!-- stage: exercises -->
### Exercises

#### [Build] Versioned Integer (Author exercise)
<!-- id: it37-version-histories-versioned-integer -->

**Prerequisites.** The version history and floor search definitions from this lesson.

**Problem.** Design the class `VersionedInt`. The call `set(version, value)` records that the stored integer has `value` from `version` on. The call `get(version)` returns the value of the change with the largest version not above the argument, or -1 when every change has a larger version.

**Constraints.** The limits are:
- **Version** is a `long` with `0 <= version <= 10^15`.
- **Value** is an `int` with `0 <= value <= 10^9`.
- **Order** means the versions of `set` calls are strictly increasing.
- **Calls** number at most 100000, and `get` does not change any field.

**Example 1.** Input calls `["set","set","get","get","get","get","get"]` with arguments `[[3,10],[8,20],[2],[3],[7],[8],[100]]`, output `[null,null,-1,10,10,20,20]`.

**Example 2.** Input calls `["set","get","get"]` with arguments `[[1,7],[0],[1]]`, output `[null,-1,7]`.

**Hint.** Which index does a search for the first version above the query return, and what does that index mean when it is 0?

**Changed decision.** Basic case: a sorted history of changes plus one floor search replaces any scan of the past.

#### [Vary] Snapshot Array (LeetCode 1146)
<!-- id: it37-version-histories-snapshot-array -->

**Prerequisites.** The Versioned Integer exercise above.

**Problem.** Design the class `SnapshotArray` with a length and a starting value shared by all cells. The call `set(index, val)` changes one cell. The call `snap()` saves the state and returns its identifier, counting from 0. The call `get(index, snapId)` returns the cell value that snapshot `snapId` saved, or -1 when the program has not yet taken that snapshot.

**Constraints.** The limits are:
- **Length** is `1 <= length <= 50000`, and calls number at most 100000.
- **Values** are `long` numbers with `0 <= val, start <= 10^12`.
- **Index** is a valid cell number in every call.
- **Memory** must stay proportional to the number of `set` calls.

**Example 1.** Input `length = 3`, `start = 7`, then `set(0,5)`, `snap()`, `set(0,6)`, `set(0,9)`, `get(0,0)`, `snap()`, `set(1,4)`, `get(1,0)`, `get(1,1)`, `get(0,1)`, `get(2,1)`, `get(0,2)`, `snap()`, `get(1,2)`, output `[0,5,1,7,7,9,7,-1,2,4]` for the `snap` and `get` calls in order.

**Example 2.** Input `length = 1`, `start = 0`, then `get(0,0)`, `snap()`, `get(0,0)`, output `[-1,0,0]`.

**Hint.** What does a snapshot store for a cell that was not written since the last snapshot, and where does the starting value come from?

**Changed decision.** Each cell owns a history, and the version of a saved write is the id of the snapshot that saves it.

#### [Boundary] Repeated Writes Before Snap (Author exercise)
<!-- id: it37-version-histories-repeated-writes -->

**Prerequisites.** The Versioned Integer and Snapshot Array exercises above.

**Problem.** Design the class `CoalescedInt`. The call `set(version, value)` returns `true` and stores the pair when `version` is at least the largest version stored so far. A `set` with a version equal to the largest stored version replaces that pair's value. A `set` with a smaller version returns `false` and changes nothing. The call `get(version)` returns the value of the pair with the largest version at most the argument, or -1 when none exists. The call `size()` returns the number of stored pairs.

**Constraints.** The limits are:
- **Version** is a `long` with `0 <= version <= 10^15`.
- **Value** is an `int` with `0 <= value <= 10^9`.
- **Calls** number at most 100000.
- **Rejected set** leaves every field unchanged, including `size()`.

**Example 1.** Input calls `["set","set","set","set","size","get","get","get"]` with arguments `[[4,1],[4,2],[6,3],[5,9],[],[4],[5],[3]]`, output `[true,true,true,false,2,2,2,-1]`.

**Example 2.** Input calls `["set","set","get","size"]` with arguments `[[0,5],[0,6],[0],[]]`, output `[true,true,6,1]`.

**Hint.** Which comparison between the new version and the last stored version separates append, replace and reject?

**Changed decision.** The boundary is the equal version. The new value replaces the last pair in place, and the pair count stays the same.

#### [Recognize] Fresh Time Based Store (LeetCode 981)
<!-- id: it37-version-histories-fresh-store -->

**Prerequisites.** All exercises above.

**Problem.** Design the class `FreshStore` with a freshness limit `ttl` given to the constructor. The call `set(key, value, ts)` stores `value` for `key` from time `ts` on. The call `get(key, ts)` finds the stored pair of `key` with the largest time `t <= ts`. It returns that pair's value when `ts - t <= ttl`, and otherwise the empty string. It also returns the empty string when `key` has no pair at or before `ts`.

**Constraints.** The limits are:
- **Time** values are `long` numbers with `1 <= ts <= 10^15`, and `ttl` is a `long` with `0 <= ttl <= 10^15`.
- **Order** means the times of `set` calls for one key are strictly increasing.
- **Strings** are non-empty lowercase words of at most 10 letters.
- **Calls** number at most 100000 across all keys.

**Example 1.** Input `ttl = 5`, then `set(a,x,3)`, `set(a,y,10)`, `get(a,2)`, `get(a,3)`, `get(a,8)`, `get(a,9)`, `get(a,10)`, `get(a,15)`, `get(a,16)`, `get(b,1)`, output `["","x","x","","y","y","",""]`.

**Example 2.** Input `ttl = 0`, then `set(k,v,4)`, `get(k,4)`, `get(k,5)`, output `["v",""]`.

**Hint.** Which pair does the floor search return, and which subtraction decides whether it is still fresh?

**Changed decision.** The floor search is the same, but the answer gains a second test on the distance to the found pair, and the subtraction must use `long`.
