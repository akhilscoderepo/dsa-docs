<!-- lesson-kind: standard -->
<!-- lesson-id: ordered-maps-and-sets -->
## Ordered Maps And Sets

<!-- stage: context -->
### Why Nearest Lookups Slow Down

A booking service stores the start time of every reservation. A new request asks for a start time, and the service must find the reservation that begins just before it and the one that begins just after it. Those two neighbors decide whether the request overlaps. Requests arrive all day, and each accepted request adds a new start time to the data.

A hash set answers "is this exact time stored?" in constant time, but it cannot answer "which stored time is the closest one below this value?". A hash set keeps no order, so that question forces a scan of every entry. A plain sorted array answers the nearest question quickly, yet it struggles when new entries keep arriving. This lesson asks how a program can keep keys in order, find their neighbors quickly and still accept new keys.

<!-- stage: naive -->
### Keeping A Sorted List By Hand

The direct approach stores the start times in a sorted `ArrayList`. A binary search finds where a new value belongs, and the list inserts it at that position. The same search also finds the neighbors of any query value.

```java
static void insert(java.util.ArrayList<Integer> sorted, int x) {
    int at = java.util.Collections.binarySearch(sorted, x);   // index of x, or -(insertion point) - 1
    if (at < 0) {
        at = -at - 1;                                         // convert to the insertion point
    }
    sorted.add(at, x);                                        // shifts every later element one slot right
}

static Integer lowerNeighbor(java.util.ArrayList<Integer> sorted, int q) {
    int at = java.util.Collections.binarySearch(sorted, q);
    int point = at >= 0 ? at : -at - 1;                       // first index whose value is >= q
    return point == 0 ? null : sorted.get(point - 1);         // the entry just before that index
}
```

The search costs O(log n) comparisons, so each neighbor query is fast. The insertion is different. The call `sorted.add(at, x)` moves every element after `at` one slot to the right, which is up to `n` moves.

<!-- stage: bottleneck -->
### Insertions Cost O(n) Each

```predict
A sorted list starts empty. A program inserts 100,000 distinct values in random order, one at a time. About how many element moves do all the insertions cost together?

About 2.5 billion moves. The list holds k elements before the k-th insertion, and a random position shifts about half of them. Summing k / 2 for k up to 100,000 gives about n squared divided by 4.
```

#### Count The Moves

One insertion into a list of size `k` moves about `k / 2` elements on average, so it costs O(k). Summed over `n` insertions, the cost is O(n^2) in total. For `n = 100,000` that is about 2.5 * 10^9 element moves, which takes seconds. Removing a value has the same cost, because every later element shifts one slot left.

#### Compare The Other Extreme

An unsorted list makes each insertion O(1), because the new value goes at the end. But a neighbor query then scans all entries and costs O(n). One layout makes queries cheap and updates expensive, and the other does the reverse. The structure we need must keep keys in order, find a neighbor in O(log n) and also add or remove a key in O(log n). That requires storing the keys as linked nodes that never shift, arranged so that every search path stays short.

<!-- stage: insight -->
### Keep Keys In A Balanced Search Tree

#### Store Keys In A Balanced Tree

A **binary search tree** stores one key per node. Every key in the left subtree of a node is smaller than the node's key, and every key in the right subtree is larger. A search starts at the root and moves left or right, so it follows one path from the root downward. A **balanced** tree keeps its height at O(log n) by restructuring itself after each insertion or removal. Java's **`TreeMap`** is a balanced tree of this kind, a red-black tree, and `TreeSet` is a thin wrapper around a `TreeMap`. Because nodes link to each other, an insertion adds one node and relinks a few pointers, and no element moves.

<!-- names: TreeMap, floor, ceiling, comparator -->

#### Answer Neighbor Queries By Descending

The method `floor(x)` returns the greatest key that is less than or equal to `x`, and `ceiling(x)` returns the smallest key that is greater than or equal to `x`. Their strict versions are `lower(x)` and `higher(x)`. All four run the same descent. At each node the search compares `x` with the node key. When the node key qualifies as an answer, the search remembers it as the best candidate and moves toward the side that could hold a better one. When the node key does not qualify, the search moves toward the side that holds qualifying keys. The descent ends at a missing child, and the remembered candidate is the answer, or `null` when no key ever qualified. The path has the height of the tree, so each query costs O(log n).

#### Let The Comparator Decide Equality

A **comparator** is the rule that orders two keys and returns a negative number, zero or a positive number. A `TreeMap` never calls `equals` or `hashCode`. It treats two keys as the same key exactly when the comparator returns 0 for them. The invariant is that the tree stays ordered under one fixed comparator, and every search and insertion relies on it. If the comparator gives inconsistent answers, or if a stored key changes in a way that alters its comparison result, the invariant breaks and later searches walk the wrong way.

<!-- stage: variables -->
### Quantities To Track In The Tree

Track these items while using an ordered map or set.

- **map** is a `TreeMap<K, V>` that stores each key once under its comparator.
- **x** is the query value that a navigation call compares with the stored keys.
- **best** is the remembered candidate while the descent runs.
- **node** is the tree node that the descent currently compares with `x`.
- **result** is the key that a call returns, or `null` when no key qualifies.

The four navigation calls differ only in which comparison results qualify a node. The call `floor` accepts a key when it is at most `x`, and `lower` accepts it only when it is smaller than `x`. The call `ceiling` accepts a key at least `x`, and `higher` accepts it only when it is larger. The methods `firstKey` and `lastKey` give the minimum and maximum keys. They throw `NoSuchElementException` on an empty map, while `firstEntry` and `lastEntry` return `null` instead.

<!-- stage: trace -->
### Follow Two Descents

The trace draws the keys in sorted order and picks the node to compare with a midpoint rule, so the picture shows a balanced tree. The real `TreeMap` may have a different shape, but its descent follows the same comparison rule and its height stays O(log n). Each step shows the node being compared and the best candidate so far. The pointer value -1 means that no node is selected or no candidate exists.

#### Find The Ceiling Of 14

The keys are `3, 8, 12, 17, 21, 25, 30`, and the call is `ceiling(14)`. The root is the middle key 17. Since 17 is at least 14, it qualifies, so the search remembers 17 and goes left for a smaller qualifying key. The left subtree holds `3, 8, 12`, and its root is 8. Since 8 is below 14, it does not qualify, so the search goes right. The next node is 12, which is also below 14, so the search goes right again and finds no child. The remembered candidate 17 is the answer.

```trace
{"cells":[3,8,12,17,21,25,30],"pointers":["node","best"],"steps":[{"at":{"node":-1,"best":-1},"vars":{"x":14},"note":"The call ceiling(14) starts at the root with no candidate."},{"at":{"node":3,"best":3},"vars":{"x":14,"key":17,"candidate":17},"note":"17 is at least 14, so it qualifies and becomes the candidate. The search goes left for a better key."},{"at":{"node":1,"best":3},"vars":{"x":14,"key":8,"candidate":17},"note":"8 is below 14, so it does not qualify. The search goes right."},{"at":{"node":2,"best":3},"vars":{"x":14,"key":12,"candidate":17},"note":"12 is below 14, so it does not qualify. The search goes right."},{"at":{"node":-1,"best":3},"vars":{"x":14,"result":17},"note":"The search reaches a missing child, so it stops. The answer is 17."}]}
```

#### Find The Floor Of 25

The keys are `2, 7, 11, 16, 22, 27, 31, 40, 44`, and the call is `floor(25)`. The root is 22, which is at most 25, so it qualifies and the search goes right for a larger qualifying key. The right subtree holds `27, 31, 40, 44`, and its first compared key is 31, which is above 25, so the search goes left. The next key is 27, which is also above 25, and it has no left child. The answer is the remembered 22.

```trace
{"cells":[2,7,11,16,22,27,31,40,44],"pointers":["node","best"],"steps":[{"at":{"node":-1,"best":-1},"vars":{"x":25},"note":"The call floor(25) starts at the root with no candidate."},{"at":{"node":4,"best":4},"vars":{"x":25,"key":22,"candidate":22},"note":"22 is at most 25, so it qualifies and becomes the candidate. The search goes right for a better key."},{"at":{"node":6,"best":4},"vars":{"x":25,"key":31,"candidate":22},"note":"31 is above 25, so it does not qualify. The search goes left."},{"at":{"node":5,"best":4},"vars":{"x":25,"key":27,"candidate":22},"note":"27 is above 25, so it does not qualify. The search goes left."},{"at":{"node":-1,"best":4},"vars":{"x":25,"result":22},"note":"The search reaches a missing child, so it stops. The answer is 22."}]}
```

The first trace changes the candidate once, at the root, then moves left once, and then moves right twice. The second trace keeps the root as its candidate while the later nodes fail. Each descent compares only three keys, although the maps hold seven and nine.

<!-- stage: code -->
### Use Navigation Calls For Neighbors

```java
final class OrderedCounts {
    private final java.util.TreeMap<Integer, Integer> counts = new java.util.TreeMap<>();

    void add(int key) {
        counts.merge(key, 1, Integer::sum);          // one tree search; creates the entry or raises its count
    }

    boolean removeOne(int key) {
        Integer c = counts.get(key);                 // one tree search for the exact key
        if (c == null) return false;                 // absent key: nothing to remove
        if (c == 1) counts.remove(key);              // a zero count must delete the entry, or the key stays visible
        else counts.put(key, c - 1);
        return true;
    }

    Integer nearestAtMost(int x) {
        return counts.floorKey(x);                   // greatest key <= x, or null when none exists
    }

    Integer nearestAbove(int x) {
        return counts.higherKey(x);                  // smallest key > x, or null when none exists
    }

    java.util.Map<Integer, Integer> keysBetween(int lo, int hi) {
        return counts.subMap(lo, true, hi, true);    // a live view of keys lo..hi, not a copy
    }
}
```

Every call above runs one descent and costs O(log n). The method `keysBetween` creates the view in O(1), because it only records two bounds. The first step of iterating the view runs one descent, so iteration costs O(log n + m) for `m` keys in range. A view is **live**, which means it reads the original map each time. A later change to the map shows through the view, and a `put` through the view with a key outside its bounds throws `IllegalArgumentException`. The `descendingMap` and `headMap` calls follow the same rule.

<!-- stage: applicability -->
### When An Ordered Map Applies

#### Recognize The Pattern

Use `TreeMap` or `TreeSet` when a program needs the predecessor or successor of a value, the minimum or maximum, or iteration in key order, while keys are added and removed. Typical cases are interval booking, the closest value to a target, and counts that must print in sorted order. Each insert, removal and lookup costs O(log n), and the invariant to protect is that every stored key keeps a stable position under the comparator.

#### Watch For The Nearest False Friend

A `HashMap` is a false friend. It looks like the right tool because it also stores keys and values, and its operations cost O(1) on average, but it has no order and no neighbor query. A `PriorityQueue` is a second false friend. It gives the minimum quickly, yet it cannot find the key just below a given value and cannot remove an arbitrary key cheaply. If the data never changes after loading, a sorted array with binary search is simpler and faster in practice.

#### Avoid The Java Comparator Traps

The comparator replaces `equals`. A case-insensitive comparator makes `"Apple"` and `"apple"` the same key, so the second `add` is ignored, even though `"Apple".equals("apple")` is false. The class `BigDecimal` shows the reverse case. `new BigDecimal("1.0")` and `new BigDecimal("1.00")` are not equal under `equals`, but `compareTo` returns 0, so a `TreeSet` keeps one of them and a `HashSet` keeps both. A comparator should be consistent with `equals` unless the program wants that merging.

Never change a stored key in a way that alters its order. The tree does not notice the change, so it stays arranged by the old order. A later search for the key can end at the wrong node and report it missing. Also remember that `null` is a normal result of `floor` and its relatives, while `put(null, v)` on a natural-order `TreeMap` throws `NullPointerException`.

<!-- stage: exercises -->
### Exercises

#### [Build] Floor And Ceiling (Author exercise)
<!-- id: ord-floor-ceiling -->

**Prerequisites.** The navigation calls and the `null` result from this lesson.

**Problem.** Given a set of distinct integer keys and a list of query integers, return for each query `q` two values. The first value is the greatest key that is less than or equal to `q`. The second value is the smallest key that is greater than or equal to `q`. If no such key exists, that value is -1.

**Constraints.** The limits are:
- **Keys** number between 0 and 10^5, are distinct, and satisfy `0 <= key <= 10^9`.
- **Queries** number at most 10^5 and satisfy `0 <= q <= 10^9`.
- **Return** is an `int[][]` with one pair per query.
- **Mutation** of the inputs is not allowed.

**Example 1.** Input keys `10, 20, 30, 40` and queries `25, 20, 5, 45`, output `(20, 30), (20, 20), (-1, 10), (40, -1)`.

**Example 2.** Input keys `7` and queries `7, 8`, output `(7, 7), (7, -1)`.

**Hint.** Which two navigation calls match the two bounds, and what do they return when nothing qualifies?

**Changed decision.** Baseline case: one pair of nearest keys per query.

#### [Vary] Ordered Frequency Map (Author exercise)
<!-- id: ord-frequency-map -->

**Prerequisites.** The floor and ceiling exercise above.

**Problem.** Start with an empty multiset of integers. Process a list of operations. The operation `(1, x)` adds one copy of `x`. The operation `(2, x)` removes one copy of `x`, and it does nothing when `x` is absent. Return the final contents as pairs `(value, count)` in increasing order of value, listing only values with a positive count.

**Constraints.** The limits are:
- **Operations** number at most 10^5.
- **Values** are `int` values with `-10^9 <= x <= 10^9`.
- **Type** is 1 for add and 2 for remove.
- **Return** is an `int[][]` of pairs, and empty contents return an empty array.

**Example 1.** Input `(1,5), (1,3), (1,5), (1,9), (2,3), (2,5)`, output `(5, 1), (9, 1)`.

**Example 2.** Input `(1,4), (2,7), (1,4), (2,4), (2,4), (2,4)`, output the empty array.

**Hint.** What must happen to an entry when its count drops to 0, so that the ordered output stays correct?

**Changed decision.** The map now stores a count per key, and a removal must delete the key at count 0.

#### [Boundary] Missing Neighbor And Comparator Equality (Author exercise)
<!-- id: ord-comparator-equality -->

**Prerequisites.** The two exercises above.

**Problem.** Words are compared by letters only, ignoring the case of ASCII letters. Two words are the same key when they differ only in case. Insert the given words in order into an ordered set, and keep the first spelling of each key. For each query word, return the stored word with the greatest key that is strictly smaller than the query under the same comparison, or the text `none` if no stored key is smaller.

**Constraints.** The limits are:
- **Words** number between 0 and 10^4, with length 1 to 10, ASCII letters only.
- **Queries** number at most 10^4, with the same length and alphabet.
- **Order** compares words letter by letter after converting every letter to lower case.
- **Return** is a `String[]` with one answer per query.

**Example 1.** Input words `Pear, apple, APPLE, banana` and queries `BANANA, Apple, zebra`, output `apple, none, Pear`.

**Example 2.** Input words `b, B, a` and queries `B, A, c`, output `a, none, b`.

**Hint.** Which comparator makes two spellings one key, and which call returns the strictly smaller neighbor?

**Changed decision.** Key identity comes from the comparator and not from `equals`, and a missing neighbor must map to a text result.

#### [Recognize] My Calendar I (LeetCode 729)
<!-- id: ord-calendar-booking -->

**Prerequisites.** All three exercises above.

**Problem.** Design a calendar class. The call `book(start, end)` represents the half-open time range from `start` up to but not including `end`. If the range shares at least one time with an accepted booking, return false and store nothing. Otherwise store it and return true.

**Constraints.** The limits are:
- **Times** are `int` values with `0 <= start < end <= 10^9`.
- **Calls** number at most 1000.
- **Touching** ranges, where one `end` equals another `start`, do not overlap.
- **Return** is a `boolean` for each call.

**Example 1.** Input the calls `book(10, 20)`, `book(15, 25)`, `book(20, 30)`, output true, false, true.

**Example 2.** Input the calls `book(5, 10)`, `book(0, 5)`, `book(0, 6)`, `book(10, 11)`, output true, true, false, true.

**Hint.** Among accepted starts, which two neighbors of the new `start` are the only ones that can overlap it?

**Changed decision.** The query is an overlap test against stored neighbors, and the stored data changes after every accepted call.
