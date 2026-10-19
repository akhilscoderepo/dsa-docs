<!-- lesson-kind: standard -->
<!-- lesson-id: frequency-buckets -->
## Frequency Buckets

<!-- stage: context -->
### Reporting The Most Frequent Word Live

A log analyzer reads search queries as they arrive. A dashboard next to the stream shows the most frequent query and the least frequent query seen so far, and it refreshes after every line. The analyzer keeps a hash map from query text to its count, so each line costs one update. Each refresh scans the whole map to find the largest count. With a million distinct queries, the scan takes longer than the gap between two lines.

The map holds the right counts. It cannot answer "which count is largest" without looking at every count. The same shape appears in rate limiters that report the busiest client, in autocomplete ranking and in cache eviction by use count.

This lesson asks how to arrange the keys so that a count change and a most-frequent query both finish quickly, even when a count goes down.

<!-- stage: naive -->
### Scanning All Counts For The Largest

The direct design keeps one hash map from key to count. An increment adds 1 to the count. The most-frequent query scans every entry and keeps the largest.

```java
final class NaiveCounts {
    private final java.util.Map<String, Integer> count = new java.util.HashMap<>();

    void inc(String key) { count.merge(key, 1, Integer::sum); }

    String mostCommon() {
        String best = "";
        int bestCount = 0;
        for (java.util.Map.Entry<String, Integer> e : count.entrySet()) {
            if (e.getValue() > bestCount) { bestCount = e.getValue(); best = e.getKey(); }
        }
        return best;                                  // scans every entry on every query
    }
}
```

An increment costs O(1), and a query costs O(n) for n distinct keys.

```predict
A million distinct keys have counts between 1 and 5, and one query asks for the largest count after every increment. How many entries does the scan read per query, and how many different counts exist?

The scan reads a million entries per query. Only five different counts exist. The answer depends on five numbers, while the work depends on a million keys.
```

<!-- stage: bottleneck -->
### Many Keys Share Few Counts

The scan costs O(n) per query, because keys with the same count are interchangeable for a max or min question and the scan still reads each one. A count changes by 1 per call. The key that moves leaves one group of equal counts and joins the group of the next count.

The number of distinct counts is small compared with the number of keys, since counts above c need at least c increments each. A structure that groups keys by count can answer a max query by looking at the group with the largest count, and the group changes only at its neighbors.

The grouping brings a new job. When a key moves from count 2 to count 3, the group for count 2 may become empty. An empty group must disappear, or the max and min queries read a group that holds no key.

<!-- stage: insight -->
### Keys Grouped By Exact Count

A **frequency bucket** holds every key whose count equals one number. Every live key sits in exactly one bucket, and the bucket's number equals the key's count.

#### One Step To A Neighbor

An increment moves a key by an **adjacent move**. The key leaves the bucket for count `c` and enters the bucket for count `c + 1`. A decrement moves it from `c` to `c - 1`. No other key changes, and the move touches only two buckets. When the target bucket does not exist yet, the call creates it. When the old bucket becomes empty, the call removes it.

#### Keeping The Buckets In Count Order

The **bucket order** is the sorted order of the bucket numbers. If the buckets form a list in this order, the first bucket holds the minimum count and the last bucket holds the maximum count. A new bucket always appears next to the bucket of the key that moved, because counts differ by 1. So the call splices the new bucket into the list in O(1) without a search.

The invariant has three parts. Every key is in exactly one bucket. The bucket number equals the key's count. No bucket is empty.

<!-- names: frequency bucket, adjacent move, bucket order -->

<!-- stage: variables -->
### What The Class Keeps

The counter keeps three structures.

- **count** maps each key to its current count and changes in every inc call.
- **bucket** maps each count to the sorted set of keys that have it, and it changes in step with count.
- **top** is the largest count that has a bucket, and it changes only when an increment passes it.

The call deletes an empty bucket from `bucket`, so the map holds only counts that some key has.

<!-- stage: trace -->
### Following Keys Between Buckets

#### Moving Keys Up By One

The first trace feeds six increments to the counter. In each step the pointer `call` marks the call just run, and the buckets appear from the smallest count to the largest.

```trace
{"cells":["inc(a)","inc(b)","inc(b)","inc(c)","inc(b)","inc(a)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"buckets":"1:{a}","top":1},"note":"Call 0: a is new, so it enters bucket 1."},{"at":{"call":1},"vars":{"buckets":"1:{a,b}","top":1},"note":"Call 1: b is new, so it enters bucket 1."},{"at":{"call":2},"vars":{"buckets":"1:{a} 2:{b}","top":2},"note":"Call 2: b moves from count 1 to count 2."},{"at":{"call":3},"vars":{"buckets":"1:{a,c} 2:{b}","top":2},"note":"Call 3: c is new, so it enters bucket 1."},{"at":{"call":4},"vars":{"buckets":"1:{a,c} 3:{b}","top":3},"note":"Call 4: b moves from count 2 to count 3. Bucket 2 is empty now, so the call removes it."},{"at":{"call":5},"vars":{"buckets":"1:{c} 2:{a} 3:{b}","top":3},"note":"Call 5: a moves from count 1 to count 2."}]}
```

The fifth call moves `b` from count 2 to count 3. Bucket 2 held only `b`, so it empties and the call removes it. The list then holds buckets 1 and 3, which are not neighbors in count, and the order of the list still matches the order of the counts.

#### Moving Keys Down By One

The second trace adds decrements. The bucket list must stay free of empty buckets in both directions.

```trace
{"cells":["inc(x)","inc(y)","inc(y)","dec(y)","dec(y)","dec(x)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"buckets":"1:{x}","top":1},"note":"Call 0: x is new, so it enters bucket 1."},{"at":{"call":1},"vars":{"buckets":"1:{x,y}","top":1},"note":"Call 1: y is new, so it enters bucket 1."},{"at":{"call":2},"vars":{"buckets":"1:{x} 2:{y}","top":2},"note":"Call 2: y moves from count 1 to count 2."},{"at":{"call":3},"vars":{"buckets":"1:{x,y}","top":1},"note":"Call 3: y moves from count 2 to count 1. Bucket 2 is empty now, so the call removes it."},{"at":{"call":4},"vars":{"buckets":"1:{x}","top":1},"note":"Call 4: y drops from count 1 to 0, so it leaves the counter."},{"at":{"call":5},"vars":{"buckets":"empty","top":0},"note":"Call 5: x drops from count 1 to 0, so it leaves the counter. Bucket 1 is empty now, so the call removes it."}]}
```

The last call removes `x` from the counter, because its count reaches 0. Bucket 1 empties, and the list holds the remaining buckets only.

<!-- stage: code -->
### An Increment-Only Counter In Java

The class stores buckets in a map from count to sorted keys, and it tracks the largest count.

```java
final class BucketCounter {
    private final java.util.Map<String, Integer> count = new java.util.HashMap<>();
    private final java.util.Map<Integer, java.util.TreeSet<String>> bucket = new java.util.HashMap<>();
    private int top = 0;

    void inc(String key) {
        int c = count.getOrDefault(key, 0);
        if (c > 0) {                                           // leave the old bucket first
            java.util.TreeSet<String> old = bucket.get(c);
            old.remove(key);
            if (old.isEmpty()) bucket.remove(c);               // an empty bucket must disappear
        }
        count.put(key, c + 1);
        bucket.computeIfAbsent(c + 1, k -> new java.util.TreeSet<>()).add(key);
        top = Math.max(top, c + 1);                            // counts only grow, so top never needs a search
    }

    String mostCommon() {
        return top == 0 ? "" : bucket.get(top).first();
    }
}
```

An increment costs O(log n) because of the tree set, and a query costs O(log n). Replacing the tree set with a hash set gives O(1) for both and returns any key of the top bucket. The space is O(n).

<!-- stage: applicability -->
### When Counts Form The Query

#### Recognizing Count Queries

The cue is an update that moves one count by a small step, together with a query for the minimum, the maximum or the most frequent item. State the step size first. The invariant is that each key sits in one bucket that matches its count, and no bucket stays empty.

#### Increments Only Or Both Directions

With increments only, the largest count never drops, so one integer tracks it. With decrements, the largest bucket can empty. Then the next maximum is the previous bucket in the list, and the list must store links in both directions. A heap of counts cannot delete the old count of a key cheaply, so it is not a substitute.

#### False Friends

A sorted map from count to key looks like the same design. It is a false friend when several keys share a count, because the map keeps only one of them. A priority queue holds the largest count at its root, but it gives no way to move a key by one step without a search. Skip buckets when counts jump by large amounts, because a jump creates many new buckets and a sorted structure costs the same.

<!-- stage: exercises -->
### Exercises

#### [Build] Key Frequency Buckets (Author exercise)
<!-- id: ci40-key-buckets -->

**Prerequisites.** Hash maps and tree sets.

**Problem.** Design a class `KeyBuckets`. The call `inc(key)` raises the count of a string key by 1, starting from 0. The call `mostCommon()` returns the key with the largest count, and the smallest key in lexicographic order among keys with equal counts. It returns an empty string when no key exists. The call `keysAt(c)` returns the keys with count exactly `c` in lexicographic order.

**Constraints.** The limits are:
- **Keys** are lowercase strings of length 1 to 10.
- **Calls** number at most `10^5`.
- **Count** `c` in `keysAt` satisfies `c >= 1`.
- **Return** of `keysAt` is an empty list when no key has count `c`.

**Example 1.** Input calls `inc(a)`, `inc(b)`, `inc(b)`, `mostCommon()`, output `b`.

**Example 2.** Input calls `inc(y)`, `inc(x)`, `mostCommon()`, `keysAt(1)`, output `x` and the list `x`, `y`.

**Hint.** Which two buckets does one increment touch, and which integer tracks the top?

**Changed decision.** A key moves between adjacent buckets, so the call removes the old bucket once it empties and before the query reads the top.

#### [Vary] All O`one Data Structure (LeetCode 432)
<!-- id: ci40-all-oone -->

**Prerequisites.** The key buckets exercise above.

**Problem.** Design a class `AllOne`. The call `inc(key)` raises the count of a key by 1, starting from 0. The call `dec(key)` lowers the count by 1 and removes the key when the count reaches 0. The call `getMaxKey()` returns any key with the largest count, and `getMinKey()` returns any key with the smallest count. Both return an empty string when no key exists. Every call must run in O(1) time on average.

**Constraints.** The limits are:
- **Keys** are lowercase strings of length 1 to 10.
- **Calls** number at most `5 * 10^4`.
- **Dec** is called only for keys that exist.
- **Return** of `getMaxKey` and `getMinKey` is any key that meets the rule.

**Example 1.** Input calls `inc(a)`, `inc(b)`, `inc(b)`, `getMaxKey()`, `getMinKey()`, output `b` and `a`.

**Example 2.** Input calls `inc(a)`, `dec(a)`, `getMaxKey()`, output an empty string.

**Hint.** Why must the buckets form a linked list in count order, and which neighbor does a decrement read?

**Changed decision.** A decrement can empty the minimum bucket, so the min pointer moves to a neighbor and needs no search.

#### [Boundary] Empty Bucket Removal (Author exercise)
<!-- id: ci40-empty-bucket -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `CountLedger` with the calls `inc(key)`, `dec(key)` and `getMaxKey()` of the previous exercise, and a call `bucketCount()` that returns the number of distinct positive counts held by live keys. The call `getMaxKey()` returns the smallest key among those with the largest count, or an empty string when no key exists. The structure must keep no empty bucket after any call.

**Constraints.** The limits are:
- **Keys** are lowercase strings of length 1 to 10.
- **Calls** number at most `10^5`, and `dec` names a live key.
- **Dec** removes the key when its count reaches 0.
- **bucketCount** returns an `int` and equals 0 when no key exists.

**Example 1.** Input calls `inc(a)`, `inc(b)`, `inc(b)`, `bucketCount()`, `dec(a)`, `bucketCount()`, output 2 and then 1.

**Example 2.** Input calls `inc(x)`, `inc(y)`, `inc(x)`, `inc(y)`, `bucketCount()`, `dec(y)`, `bucketCount()`, output 1 and then 2.

**Hint.** What does the structure hold for count 3 right after the last key with count 3 moves down?

**Changed decision.** The check for an empty bucket moves into every call that removes a key from a bucket.

#### [Recognize] Maximum Frequency Stack (LeetCode 895)
<!-- id: ci40-freq-stack -->

**Prerequisites.** All three exercises above.

**Problem.** Design a class `FreqStack`. The call `push(val)` pushes an integer. The call `pop()` removes and returns the value with the highest number of occurrences currently in the stack. When several values tie, it removes the occurrence of the value whose latest remaining occurrence is closest to the top.

**Constraints.** The limits are:
- **Values** satisfy `0 <= val <= 10^9`.
- **Calls** number at most `2 * 10^4`.
- **Pop** is called only on a non-empty stack.
- **Return** of `pop` is an `int`.

**Example 1.** Input pushes of 5, 7, 5, 7, 4, 5 and then four `pop()` calls, output 5, 7, 5, 4.

**Example 2.** Input pushes of 1, 1, 2 and then two `pop()` calls, output 1 and then 2.

**Hint.** Keep one stack for each frequency. Which stack does a push join, and which stack does a pop read?

**Changed decision.** Ties break by recency, so each bucket stores values in push order and a pop reads the top of the highest bucket.
