<!-- lesson-kind: combination -->
<!-- lesson-id: time-indexed-lookup -->
## Time Indexed Lookup

<!-- stage: context -->
### A Museum With Changing Labels

A museum has many display cases, and the curators change the card in a case several times a day as exhibits are rotated. Every change is written in a logbook as three things: which case, what the new card says, and the time. The logbook is filled in order of time, so the entries for any one case run from the earliest to the latest.

Visitors send questions by email, and each one asks what a particular case said at a particular moment: "What did case B say at 14:20?" The answer is the card from the most recent change at or before 14:20. If the case had not yet been given a card by then, the answer is a blank. A volunteer is asked to answer thousands of such emails a day from the logbook, and the logbook gets longer every day.

<!-- stage: contributions -->
### What Each Part Brings

The hash map brings the choice of case. Given the name of a case, it jumps straight to that case's own list of changes, without looking at any other case's entries. This takes the same time whether the museum has ten cases or ten thousand. The map alone cannot answer the question, because it can only look a name up exactly, and the question asks about a moment that is almost never one of the recorded times.

Binary search brings the choice of moment. Within one case's list the times are in increasing order, so the list is sorted, and a sorted list lets a search discard half of the entries at each step. Binary search alone cannot answer the question either, because there is one logbook for all cases mixed together, and the entries of one case are not contiguous in it. Each part removes exactly the uncertainty that the other one cannot: the map says which list to look in, and the search says where in that list.

The recognition cue is a query that names a key and a time, where the answer is the latest recorded value at or before the time, and the records for each key arrive in order of time.

<!-- stage: naive -->
### Read One Case's Entries From The Start

The direct approach is to keep each case's times and cards in two lists, and to answer a question by reading the case's entries from the first change on, remembering the card of the last change that is not after the requested time.

```java
static String valueByScan(Map<String, List<Integer>> times,
                          Map<String, List<String>> cards, String key, int when) {
    List<Integer> t = times.get(key);
    if (t == null) return "";
    String answer = "";
    for (int i = 0; i < t.size(); i++) {
        if (t.get(i) <= when) answer = cards.get(key).get(i);
    }
    return answer;
}
```

It returns the right card for every question, because the times in a list only increase, so the last entry that is not after `when` is the latest one at or before it, and a blank when there is none.

<!-- stage: bottleneck -->
### Every Question Reads The Whole List

A case that has been changed m times makes the loop read m entries for every question, so q questions about it cost O(q m). A popular case with a hundred thousand changes and a hundred thousand questions means ten billion reads. The loop also reads entries long after the requested time, which cannot matter, since the list is in order of time.

The structure of the list is what the loop ignores. In a list sorted by time, the entries at or before a given moment are a prefix, and the entries after it are a suffix, with one boundary between them. The question asks for the last entry of the prefix. Finding the boundary is the upper-bound search from the earlier lesson, which takes O(log m) steps, so a question costs O(1) expected for the map lookup plus O(log m) for the search.

<!-- stage: insight -->
### Find The Key, Then The Moment

Each key owns a **history list**, a list of its entries kept in the order in which they were recorded, which for this problem is also the order of time. The map's job is to hand over the right **key bucket**, the history list of one key, in constant expected time. After that the problem is only about one sorted list.

Inside the list, the question is a **latest-not-after query**: the entry with the largest time that is at most the requested time. It is solved by finding the first entry whose time is greater than the request, the upper bound, and then stepping one position back. If the upper bound is position `p`, then entries `0` to `p - 1` are not after the request, and the answer is position `p - 1`. If `p` is zero there is no such entry, and the contract's empty answer is returned. The invariant is the one of the bounds lessons: everything below `lo` has time at most the request, and everything from `hi` on has time greater than it.

<!-- names: history list, key bucket, latest-not-after query -->

The same two-step shape appears in other problems. A snapshot array gives every index its own history of changes, tagged with a snapshot number, and a read asks for the latest change at or before that number. An online election keeps one history of leaders by time and asks who led at a given moment. In each case the data arrives in order of the tag, so the list stays sorted without any sorting, and a lookup is a bucket choice followed by a search for the boundary.

<!-- stage: variables -->
### Buckets, Bounds And The Step Back

The map takes a key to its bucket. In the bucket, `lo` and `hi` bound the search over positions, with `hi` starting at the size of the list so that the position one past the end is a legal answer. `mid` is the position under test. When the search ends, `lo` equals the upper bound, and the entry that answers the question is at `lo - 1`. The step back is a place for a bug: when `lo` is zero, position `lo - 1` does not exist, so the empty case must be handled before reading.

<!-- stage: trace -->
### Searching One Key's Timeline

The first trace answers a question at time 15 for a case whose card changed at times 2, 5, 9, 14, 20 and 27. The cells are those times. The search looks for the first change after time 15. The step to study is the first one: the middle entry has time 14, which is not after 15, so the boundary is to its right and `lo` moves past it.

```trace
{"cells":["2","5","9","14","20","27"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":6,"mid":3},"vars":{"time":14,"query":15},"note":"Time 14 is not after 15, so the boundary is to its right and lo moves to 4."},{"at":{"lo":4,"hi":6,"mid":5},"vars":{"time":27,"query":15},"note":"Time 27 is after 15, so the boundary is here or to the left and hi moves to 5."},{"at":{"lo":4,"hi":5,"mid":4},"vars":{"time":20,"query":15},"note":"Time 20 is after 15, so the boundary is here or to the left and hi moves to 4."},{"at":{"lo":4,"hi":4,"mid":-1},"vars":{"upperBound":4,"answerPosition":3,"answerTime":14},"note":"The upper bound is position 4, so the answer is position 3, the change at time 14."}]}
```

The second trace asks about time 1 for a case whose changes are at times 2, 5 and 9. Every change is after the question, so the upper bound is position zero. The step to study is the closing one, where the step back would read position minus one, so the answer is the blank value instead of an entry.

```trace
{"cells":["2","5","9"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":3,"mid":1},"vars":{"time":5,"query":1},"note":"Time 5 is after 1, so the boundary is here or to the left and hi moves to 1."},{"at":{"lo":0,"hi":1,"mid":0},"vars":{"time":2,"query":1},"note":"Time 2 is after 1, so the boundary is here or to the left and hi moves to 0."},{"at":{"lo":0,"hi":0,"mid":-1},"vars":{"upperBound":0,"answer":"blank"},"note":"The upper bound is position 0, so no change is at or before time 1 and the answer is the blank value."}]}
```

<!-- stage: code -->
### A Bucket Choice And A Boundary Search

```java
final class TimeIndexed {
    static int countNotAfter(List<Integer> times, int when) {
        int lo = 0, hi = times.size();
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (times.get(mid) <= when) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static final class TimeMap {
        private final Map<String, List<Integer>> times = new HashMap<>();
        private final Map<String, List<String>> values = new HashMap<>();

        void set(String key, String value, int time) {
            times.computeIfAbsent(key, k -> new ArrayList<>()).add(time);
            values.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
        }

        String get(String key, int time) {
            List<Integer> t = times.get(key);
            if (t == null) return "";
            int n = countNotAfter(t, time);
            return n == 0 ? "" : values.get(key).get(n - 1);
        }
    }

    static final class SnapshotArray {
        private final List<List<int[]>> changes = new ArrayList<>();
        private int nextId = 0;

        SnapshotArray(int length) {
            for (int i = 0; i < length; i++) changes.add(new ArrayList<>());
        }

        void set(int index, int value) {
            List<int[]> c = changes.get(index);
            if (!c.isEmpty() && c.get(c.size() - 1)[0] == nextId) c.get(c.size() - 1)[1] = value;
            else c.add(new int[] {nextId, value});
        }

        int snap() { return nextId++; }

        int get(int index, int snapId) {
            List<int[]> c = changes.get(index);
            int lo = 0, hi = c.size();
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                if (c.get(mid)[0] <= snapId) lo = mid + 1;
                else hi = mid;
            }
            return lo == 0 ? 0 : c.get(lo - 1)[1];
        }
    }
}
```

Setting a value costs O(1) amortized, and a lookup costs O(1) expected for the map plus O(log m) for the search over the m entries of one bucket. The space is O(total entries). The snapshot array overwrites the last entry when the same index is set twice before a snapshot, so a bucket never holds two entries with the same tag.

<!-- stage: applicability -->
### When Key And Time Both Matter

Use this pair when queries name a key and a point on an ordered scale, each key's records arrive in increasing order of that scale, and the answer is the latest record at or before the point, or the earliest at or after it. State which of the two it is before coding, since they need the upper bound and the lower bound respectively. The invariant is the same as in the bound lessons, applied inside one bucket.

False friends come from the two parts. A map from key to the latest value alone answers only the present, and it loses the past. A single sorted list of all records mixes keys, so the entries of one key are scattered through it. A third false friend is assuming the records arrive in order when the contract does not say so: if timestamps can arrive out of order, the lists need insertion by search or a sorted structure, not appending.

In Java, use `computeIfAbsent` so a missing bucket is created in one step, and test for a missing key before searching, since `get` returns `null` for it. Handle the position before the first entry explicitly, because `lo - 1` is not a valid index there. Choose the empty answer from the contract, which here is an empty string for text and zero for a snapshot array.

<!-- stage: exercises -->
### Exercises

#### [Build] One Key History (Author exercise)
<!-- id: bs-one-key-history -->

**Prerequisites.** The lower and upper bounds lesson, and maps of lists from Chapter 04.

**Problem.** Given the strictly increasing times of the changes of one key and a query time, return the position of the latest change at or before the query, or minus one if every change is later. Use a search for the upper bound and step back once.

**Constraints.** 0 <= times.length <= 100000, strictly increasing integers, and any integer query.

**Example 1.** Input `times = [2, 5, 9, 14], query = 10`, output 2.

**Example 2.** Input `times = [2, 5, 9, 14], query = 14`, output 3.

**Hint.** Which position does the upper bound give? What is the answer when that position is zero?

**Changed decision.** First rung: the sorted list is a history, and the answer is one position before the first time that is greater than the query.

#### [Vary] Time Based Key-Value Store (LeetCode 981)
<!-- id: bs-time-map -->

**Prerequisites.** The One Key History exercise above.

**Problem.** Design a store with `set(key, value, timestamp)` and `get(key, timestamp)`. A `get` returns the value of the set call for that key with the largest timestamp not after the query, or an empty string if there is none. Timestamps passed to `set` for one key are strictly increasing.

**Constraints.** 1 <= key.length, value.length <= 100, up to 200000 calls in total, and 1 <= timestamp <= 10000000.

**Example 1.** Input `set("foo", "bar", 1)` then `get("foo", 3)`, output `"bar"`.

**Example 2.** Input `set("foo", "bar", 1)`, `set("foo", "bar2", 4)` then `get("foo", 4)`, output `"bar2"`.

**Hint.** What keeps the entries of each key apart? Does a list of values need its own binary search, or can it share the position found in the list of times?

**Changed decision.** Many keys share the store, so a map picks the history list, and only then does the search start.

#### [Boundary] Time Based Key-Value Store Early Query (LeetCode 981)
<!-- id: bs-time-map-early -->

**Prerequisites.** The two exercises above.

**Problem.** Keep the store of the previous exercise and answer the cases around its edges: a key that was never set, a query before the first timestamp of a key, a query exactly at the first timestamp, and a query after the last. The empty string is the contract for the first two cases, and reading position minus one must never happen.

**Constraints.** The same limits as the previous exercise, with queries that may be smaller than every stored timestamp.

**Example 1.** Input `set("a", "x", 5)` then `get("a", 4)`, output the empty string.

**Example 2.** Input `get("b", 100)` when `"b"` was never set, output the empty string.

**Hint.** What does the search return for a query smaller than every time? Which line must come before the read?

**Changed decision.** The empty answer is part of the contract, so the step back is guarded and a missing key is checked before any search.

#### [Recognize] Snapshot Array (LeetCode 1146)
<!-- id: bs-snapshot-array -->

**Prerequisites.** All three exercises above.

**Problem.** Design an array of a given length, with every element starting at zero, and the operations `set(index, val)`, `snap()` which returns the number of the snapshot just taken starting from zero, and `get(index, snap_id)` which returns the element's value when that snapshot was taken. Give each index its own list of changes tagged by snapshot number.

**Constraints.** 1 <= length <= 50000, at most 50000 calls in total, and 0 <= val <= 1000000000.

**Example 1.** Input length 3, `set(0, 5)`, `snap()`, `set(0, 6)` then `get(0, 0)`, output 5.

**Example 2.** Input the same calls followed by a second `snap()` and `get(2, 1)`, output 0.

**Hint.** Why must a snapshot not copy the array? What should happen when the same index is set twice before a snapshot?

**Changed decision.** The key is an index and the time is the snapshot number, and an index without changes answers zero.

#### [Extend] Online Election (LeetCode 911)
<!-- id: bs-online-election -->

**Prerequisites.** The Snapshot Array exercise above.

**Problem.** Votes arrive as person and time pairs in increasing order of time. A query `q(t)` returns the person who was leading at time `t`, and when two people have the same count the one who received a vote most recently wins. Precompute the leader after each vote, then answer a query by searching the times.

**Constraints.** 1 <= persons.length == times.length <= 5000, times strictly increasing, and queries at or after the first time.

**Example 1.** Input `persons = [0, 1, 1, 0, 0, 1, 0]`, `times = [0, 5, 10, 15, 20, 25, 30]` and `q(12)`, output 1.

**Example 2.** Input the same election and `q(25)`, output 1, since the tie at time 25 goes to the most recent vote.

**Hint.** What single value must be remembered for each vote time? How does the tie rule change the comparison of counts?

**Changed decision.** The stored value is a derived leader, built in one pass, and the query is the same latest-not-after search.
