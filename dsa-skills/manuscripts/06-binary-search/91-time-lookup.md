<!-- lesson-kind: combination -->
<!-- lesson-id: time-lookup -->
## Look Up Values By Time

<!-- stage: context -->
### What Was The Setting During The Outage

A configuration service records every change of every setting. The setting `timeout` was 30 at time 3 and 45 at time 8, and the setting `retries` was 2 at time 5. During an outage review, an engineer asks what `timeout` was at time 7, and later what `retries` was at time 4. The answers are 30 and nothing, because the first change of `retries` had not happened yet.

The service handles millions of queries over settings that changed thousands of times. A query names a key and a time that rarely matches a change exactly. The question is how to find, quickly, the last change of one key at or before a given time.

<!-- stage: contributions -->
### What The Map And The Search Add

A `HashMap` from key to list answers the first half of every query. It takes the key and returns the list of changes of that key in expected constant time, and it never touches the changes of other keys. The map cannot answer the second half. It stores no order among the times inside one list, and it has no operation that returns the closest earlier entry.

Binary search answers the second half. The changes of one key arrive in increasing time order, so each list is already sorted. The search finds the closest entry at or before the query in logarithmic time, and it does not know which key to open. The two parts are needed together. The map picks the list, and the search picks one entry from it.

<!-- stage: naive -->
### Scanning One Key's Changes

The direct method fetches the list for the key and reads it from the front. It remembers the last entry whose time is not above the query.

```java
final class ScanStore {
    private final java.util.HashMap<String, java.util.ArrayList<Integer>> times = new java.util.HashMap<>();
    private final java.util.HashMap<String, java.util.ArrayList<String>> values = new java.util.HashMap<>();

    void set(String key, String value, int time) {
        times.computeIfAbsent(key, k -> new java.util.ArrayList<>()).add(time);
        values.computeIfAbsent(key, k -> new java.util.ArrayList<>()).add(value);
    }

    String get(String key, int time) {
        var ts = times.get(key);
        String best = "";
        if (ts == null) return best;
        for (int i = 0; i < ts.size(); i++) {
            if (ts.get(i) <= time) best = values.get(key).get(i);
        }
        return best;
    }
}
```

For `timeout` with changes at times 3 and 8, a query at time 7 reads both entries and returns the value stored at time 3.

```predict
A key has changed one million times and a query asks for a time before its first change. How many entries does this scan read, and how many could a method skip, given that the times in the list only increase?

The scan reads all one million entries and returns the empty string. Because the times increase, one comparison with the middle entry already shows that every later entry has a larger time, so a method could skip half of the list at once.
```

<!-- stage: bottleneck -->
### Every Query Reads The Whole List

A query costs O(h) for a list of `h` changes, because the loop never stops early. A service with 10^5 queries per second over a list of 10^6 changes reads 10^11 entries every second.

The map is not the problem. Finding the list is O(1) in expectation. The cost comes from reading an ordered list as if it were unordered. Each comparison with an entry tells the method about a whole side of the list, because the times increase, and the scan uses none of that knowledge. A search that discards half of the list per comparison needs about log2(h) comparisons, which is 20 for a million entries.

<!-- stage: insight -->
### Pick The List, Then Search It

#### One History List Per Key

A **history list** holds every change of one key in the order the changes were made, as a list of times with a parallel list of values. The map from key to history list gives each key its own list. The rule that times only increase makes every list sorted by time without any extra work, because each new change is appended at the end.

<!-- names: history list, floor search, empty answer -->

#### Floor Search On The Times

A **floor search** returns the last position whose time is at most the query. It is the upper bound search from the lower-and-upper-bounds lesson, followed by a step back. The search finds `p`, the first position whose time is greater than the query. The position `p - 1` is the answer, because all positions before `p` have a time at most the query, and `p - 1` is the last of them. The search keeps the interval `[lo, hi)` and discards `mid` when `times[mid] <= query`.

#### The Empty Answer

When `p` is 0, every change is later than the query, so `p - 1` is -1 and no entry applies. The service returns the **empty answer**, the value that the contract names for a query with no applicable entry. An unknown key produces the same answer, because the map returns no list at all. Both cases end in the same result, but they arrive by different paths, and a correct method tests each one.

<!-- stage: variables -->
### The Map, The Lists And The Interval

The method keeps a small set of state and one search interval.

- **times** and **values** are maps from a key to its history list, and they never touch the lists of other keys.
- **history list** of one key is the pair of lists `times.get(key)` and `values.get(key)`, where the times are sorted ascending.
- **lo** and **hi** bound the half-open interval `[lo, hi)` of positions that may hold the first time above the query.
- **p** is the final value of `lo`, the first position with a time above the query.

The answer position is `p - 1`, and it is -1 when `p` is 0. The search never reads `times[hi]`, because `hi` starts at the list size.

<!-- stage: trace -->
### Two Queries On One History List

#### A Query Between Two Changes

The times of one key are `[2, 5, 9, 14, 20]`, and the query is 12. The search starts with `lo = 0` and `hi = 5`. The first midpoint is position 2 with time 9, which is not above 12, so `lo` becomes 3. The next midpoint is position 4 with time 20, which is above 12, so `hi` becomes 4. The midpoint at position 3 has time 14, which is above 12, so `hi` becomes 3. The interval is empty with `p = 3`, and the answer is position 2, the entry at time 9.

```trace
{"cells":[2,5,9,14,20],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"query":"12"},"note":"Start with the whole list. The query is 12."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"time[mid]":"9"},"note":"Time 9 is not above 12, so lo becomes 3."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"time[mid]":"20"},"note":"Time 20 is above 12, so hi becomes 4."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"time[mid]":"14"},"note":"Time 14 is above 12, so hi becomes 3."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"p":"3","answer":"2"},"note":"The interval is empty with p = 3, so the answer is position 2, the entry at time 9."}]}
```

#### A Query Before Every Change

The same list is searched with the query 1. The first midpoint is position 2 with time 9, which is above 1, so `hi` becomes 2. The midpoint at position 1 has time 5, which is above 1, so `hi` becomes 1. The midpoint at position 0 has time 2, which is above 1, so `hi` becomes 0. The interval is empty with `p = 0`, and the answer is position -1, so the lookup returns the empty answer.

```trace
{"cells":[2,5,9,14,20],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"query":"1"},"note":"Start with the whole list. The query is 1."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"time[mid]":"9"},"note":"Time 9 is above 1, so hi becomes 2."},{"at":{"lo":0,"hi":2,"mid":1},"vars":{"time[mid]":"5"},"note":"Time 5 is above 1, so hi becomes 1."},{"at":{"lo":0,"hi":1,"mid":0},"vars":{"time[mid]":"2"},"note":"Time 2 is above 1, so hi becomes 0."},{"at":{"lo":0,"hi":0,"mid":-1},"vars":{"p":"0","answer":"-1"},"note":"The interval is empty with p = 0, so no entry applies and the lookup returns the empty answer."}]}
```

<!-- stage: code -->
### The Store In Java

```java
final class TimeStore {
    private final java.util.HashMap<String, java.util.ArrayList<Integer>> times = new java.util.HashMap<>();
    private final java.util.HashMap<String, java.util.ArrayList<String>> values = new java.util.HashMap<>();

    void set(String key, String value, int time) {
        times.computeIfAbsent(key, k -> new java.util.ArrayList<>()).add(time);
        values.computeIfAbsent(key, k -> new java.util.ArrayList<>()).add(value);
    }

    String get(String key, int time) {
        var ts = times.get(key);
        if (ts == null) return "";
        int lo = 0, hi = ts.size();
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (ts.get(mid) <= time) lo = mid + 1;
            else hi = mid;
        }
        return lo == 0 ? "" : values.get(key).get(lo - 1);
    }
}
```

Each `set` appends in O(1) amortized time, and each `get` costs O(1) for the map plus O(log h) for the search. The list holds `Integer` objects, and `ts.get(mid) <= time` unboxes the stored value before comparing.

<!-- stage: applicability -->
### When The Map Alone Is Not Enough

#### The Invariant

The invariant of the search is that every position below `lo` has a time at most the query and every position at or above `hi` has a time above it. The map adds a second invariant for the whole store: the list of a key contains exactly the changes of that key, in increasing time order. The search is only valid while the second invariant holds, so a `set` with an earlier time than the last one would break every later query.

#### The False Friend

A plain `HashMap<String, String>` that stores only the latest value is the false friend. It answers queries for the present and loses every earlier value, so a query about the past reads the wrong entry. The reliable cue is the phrase "as of time t" in the contract.

#### Where Each Key Owns A Timeline

The same two-level shape appears whenever each key owns an ordered history. Snapshot versions of an array element, price changes of one product and sessions of one user all use a map to the history and a floor search inside it. Check that times only grow before relying on the order.

<!-- stage: exercises -->
### Exercises

#### [Build] One Key History (Author exercise)
<!-- id: bs-time-one-key -->

**Prerequisites.** The lesson Find Where A Value Belongs and the floor search of this lesson.

**Problem.** An array `times` is sorted in strictly increasing order, and an integer `q` is a query time. Return the largest element of `times` that is at most `q`, or `-1` when no element is at most `q`.

**Constraints.** The limits are:
- **Length** is `1 <= times.length <= 100000`.
- **Values** satisfy `0 <= times[i] <= 10^9`, strictly increasing.
- **Query** satisfies `0 <= q <= 10^9`.
- **Mutation** does not occur; `times` does not change.

**Example 1.** Input `times = [2,5,9,14,20]` and `q = 12`, output 9.

**Example 2.** Input `times = [2,5,9,14,20]` and `q = 1`, output -1.

**Hint.** Find the first position with a time above `q`. Which position holds the answer?

**Changed decision.** Basic case: the search finds the first time above the query and steps back one position.

#### [Vary] Time Based Key-Value Store (LeetCode 981)
<!-- id: bs-time-key-value-store -->

**Prerequisites.** The previous exercise.

**Problem.** Process a list of operations on a store. The operation `set(key, value, time)` records that `key` has `value` from `time` on. The operation `get(key, time)` returns the value recorded for `key` at the largest recorded time that is at most `time`, or the empty string when no such record exists. Return the results of all `get` operations in order.

**Constraints.** The limits are:
- **Operations** number `1 <= n <= 100000`.
- **Time** values satisfy `1 <= time <= 10^7`, strictly increasing among the `set` calls of one key.
- **Keys and values** are non-empty lowercase strings of at most 10 letters.
- **Result** for an unknown key is the empty string.

**Example 1.** Input `set(a,x,3)`, `set(a,y,8)`, `set(b,z,5)`, `get(a,2)`, `get(a,3)`, `get(a,7)`, `get(a,9)`, `get(b,5)`, `get(c,5)`, output `["", "x", "x", "y", "z", ""]`.

**Example 2.** Input `set(k,v,1)`, `get(k,1000)`, output `["v"]`.

**Hint.** Which structure picks the list of one key? Which operation then picks one entry inside it?

**Changed decision.** The data splits by key, so a map chooses the history list and the search runs inside that list only.

#### [Boundary] Early Query (Author exercise)
<!-- id: bs-time-early-query -->

**Prerequisites.** Both exercises above.

**Problem.** Given a strictly increasing array `times` and an integer query time `q`, return the position of the largest element at most `q`, or `-1` when `q` is smaller than every element. A query equal to an element returns that element's position.

**Constraints.** The limits are:
- **Length** is `1 <= times.length <= 100000`.
- **Values** satisfy `0 <= times[i] <= 10^9`, strictly increasing.
- **Query** satisfies `0 <= q <= 10^9`, and it may fall before the first, on any, or after the last element.
- **Answer** is a position in `0..times.length - 1` or `-1`.

**Example 1.** Input `times = [4,7,10]` and `q = 3`, output -1.

**Example 2.** Input `times = [4,7,10]` and `q = 10`, output 2.

**Hint.** What does the search return when every time is above `q`? Test a query equal to the first element.

**Changed decision.** The answer position can be -1, so the final step back from `p` must not read the list at an invalid position.

#### [Recognize] Snapshot Array (LeetCode 1146)
<!-- id: bs-time-snapshot-array -->

**Prerequisites.** All exercises above.

**Problem.** Process operations on an integer array of a given length with all elements 0. The operation `set(index, val)` changes one element. The operation `snap()` saves the current state and returns its identifier, which counts from 0. The operation `get(index, snapId)` returns the element at `index` as it was when snapshot `snapId` was taken. Return the results of all `snap` and `get` operations in order.

**Constraints.** The limits are:
- **Length** is `1 <= length <= 50000`, and operations number at most `50000`.
- **Values** satisfy `0 <= val <= 10^9`.
- **Identifiers** passed to `get` name an existing snapshot.
- **Memory** must stay proportional to the number of `set` calls, not to length times snapshots.

**Example 1.** Input `length = 3`, `set(0,5)`, `snap()`, `set(0,6)`, `get(0,0)`, `snap()`, `set(1,4)`, `get(1,0)`, `get(1,1)`, `get(0,1)`, output `[0, 5, 1, 0, 0, 6]`.

**Example 2.** Input `length = 1`, `snap()`, `get(0,0)`, output `[0, 0]`.

**Hint.** Give every index its own history list of snapshot identifiers and values. A later `set` in the same snapshot replaces the last entry.

**Changed decision.** The time axis is the snapshot identifier, so each index owns a history list and a floor search finds the identifier.
