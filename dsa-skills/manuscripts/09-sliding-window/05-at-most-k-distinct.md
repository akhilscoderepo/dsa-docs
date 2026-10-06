<!-- lesson-kind: standard -->
<!-- lesson-id: at-most-k-distinct -->
## Limit A Window To K Distinct Values

<!-- stage: context -->
### A Cache That Must Not Overflow

A service reads a stream of item ids and keeps recently used items in a small cache that holds `k` different ids. An engineer wants to know the longest run of consecutive requests that the cache serves without ever needing a `k + 1`-th id. The answer tells how large the cache must be to avoid thrashing on a typical burst of traffic. The first version of the analysis starts at each request and collects ids into a set until the set grows too large. On a log of ten million requests, it does not finish.

The earlier windows tracked a sum, a letter count, or a count of bad values. This lesson tracks how many different values the window holds. That number is not stored in one variable that adds and subtracts, and the method needs a way to keep it correct as values leave.

<!-- stage: naive -->
### Collect Ids From Every Start

Each start index begins with an empty set, and each following id joins that set. It stops when the set would hold more than `k` ids, and it records the length of the run.

```java
static int longestFromEveryStart(int[] ids, int k) {
    int best = 0;
    for (int start = 0; start < ids.length; start++) {
        Set<Integer> seen = new HashSet<>();
        int end = start;
        while (end < ids.length && (seen.contains(ids[end]) || seen.size() < k)) {
            seen.add(ids[end]);
            end++;
        }
        best = Math.max(best, end - start);
    }
    return best;
}
```

Each start creates a new set and fills it from scratch.

<!-- stage: bottleneck -->
### Counting The Rereads Once More

```predict
The run from start 0 stops at index 7 because a third id appears. Is the block from index 1 to index 6 valid for a cache of two ids?

Yes. A block inside a valid block holds a subset of its ids, so it holds at most two different ids. The run from start 1 does not need to reread indexes 1 to 6.
```

When the stream uses at most `k` ids, every start reads to the end. The start at index `i` reads `n - i` ids, so the work grows as O(n^2). Each start also allocates a new set and hashes every id again, so the constant is large. For `n = 10,000,000`, the method performs about 50 trillion set operations.

The sets of neighbouring starts differ by one id at most. The cost should depend on `n` alone. The set must change when one id leaves the front. A plain set cannot do that, because a leaving value may still occur later in the block.

<!-- stage: insight -->
### Count Each Value And Remove Empty Keys

#### A Count Map Replaces The Set

A **count map** stores each value in the window with the number of times it occurs there. When a value enters, its count rises by one. When a value leaves, its count drops by one. A plain set cannot answer whether a leaving value is still in the window, and the count can.

#### The Distinct Count Is The Number Of Keys

The **distinct count** is the number of different values in the window. The count map gives it for free, as the number of keys, only if the map holds exactly the values that are in the window. A key with count 0 must therefore leave the map. The invariant is that every key of the count map has a positive count, and the keys are exactly the values of `nums[left..right]`.

#### Removing The Key At Zero

When a leaving value brings its count to 0, the method performs a **key removal**: it deletes the entry from the map. Without the removal, the map keeps a key for a value that is gone, and the key count overstates the distinct count. The window then looks invalid, and the method shrinks too far and returns a length that is too short.

The window is valid when the distinct count is at most `k`. A subset of a valid window is valid, so the shrink loop of the longest-valid lesson applies. When the distinct count exceeds `k`, move `left` forward until it does not. Both indexes move only forward, and the cost is O(n).

<!-- names: count map, distinct count, key removal -->

<!-- stage: variables -->
### What The Method Keeps

The method keeps the two indexes, a map and the best length.

- **counts** is the count map from a value to its number of occurrences in the window.
- **counts.size()** is the distinct count, and it is correct only after every key removal.
- **k** is the limit of the distinct count, and it satisfies `k >= 0`.
- **left** and **right** are the first and last indexes of the window, and `left` may equal `right + 1` when the window is empty.
- **best** is the largest window length recorded after a shrink loop.

<!-- stage: trace -->
### Tracing Two Scans

#### Two Distinct Ids

Take `ids = [1, 2, 1, 3, 3, 2, 2]` and `k = 2`. The trace below shows the distinct count in the variable `distinct` and the best length so far. The id 3 at index 3 raises the distinct count to 3. The shrink loop removes the ids at indexes 0 and 1. The removal at index 1 empties the key 2, so the distinct count falls to 2.

```trace
{"cells":[1,2,1,3,3,2,2],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"distinct":"1","best":"1"},"note":"The id 1 enters, so the distinct count is 1. The window length is 1, and best is 1."},{"at":{"left":0,"right":1},"vars":{"distinct":"2","best":"2"},"note":"The id 2 enters, so the distinct count is 2. The window length is 2, and best is 2."},{"at":{"left":0,"right":2},"vars":{"distinct":"2","best":"3"},"note":"The id 1 enters, so the distinct count is 2. The window length is 3, and best is 3."},{"at":{"left":2,"right":3},"vars":{"distinct":"2","best":"3"},"note":"The id 3 enters, so the distinct count is 3. The id 1 leaves, but it still occurs inside, so the distinct count stays 3. The id 2 leaves and its key is removed, so the distinct count is 2. The window length is 2, and best is 3."},{"at":{"left":2,"right":4},"vars":{"distinct":"2","best":"3"},"note":"The id 3 enters, so the distinct count is 2. The window length is 3, and best is 3."},{"at":{"left":3,"right":5},"vars":{"distinct":"2","best":"3"},"note":"The id 2 enters, so the distinct count is 3. The id 1 leaves and its key is removed, so the distinct count is 2. The window length is 3, and best is 3."},{"at":{"left":3,"right":6},"vars":{"distinct":"2","best":"4"},"note":"The id 2 enters, so the distinct count is 2. The window length is 4, and best is 4."}]}
```

The best length is 4, reached by the block `3, 3, 2, 2`.

#### A Limit Of Zero

When the window is empty, `left` sits one past `right`. Take `ids = [4, 4, 4]` and `k = 0`. No window may hold any value, so the answer is 0. Each entering value raises the distinct count to 1, and the shrink loop removes values until the count is 0 again. The loop removes the entering value itself, so `left` becomes `right + 1` and the window is empty. The method never lets a count drop below 0, and `left` never passes `right + 1`.

```trace
{"cells":[4,4,4],"pointers":["left","right"],"steps":[{"at":{"left":1,"right":0},"vars":{"distinct":"0","best":"0"},"note":"The id 4 enters, so the distinct count is 1. The id 4 leaves and its key is removed, so the distinct count is 0. The window length is 0, and best is 0."},{"at":{"left":2,"right":1},"vars":{"distinct":"0","best":"0"},"note":"The id 4 enters, so the distinct count is 1. The id 4 leaves and its key is removed, so the distinct count is 0. The window length is 0, and best is 0."},{"at":{"left":3,"right":2},"vars":{"distinct":"0","best":"0"},"note":"The id 4 enters, so the distinct count is 1. The id 4 leaves and its key is removed, so the distinct count is 0. The window length is 0, and best is 0."}]}
```

<!-- stage: code -->
### The Count Map Scan In Java

#### One Pass With A Map

```java
static int longestAtMostK(int[] nums, int k) {
    Map<Integer, Integer> counts = new HashMap<>();
    int left = 0, best = 0;
    for (int right = 0; right < nums.length; right++) {
        counts.merge(nums[right], 1, Integer::sum);
        while (counts.size() > k) {
            int gone = nums[left];
            int c = counts.get(gone) - 1;
            if (c == 0) counts.remove(gone);
            else counts.put(gone, c);
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

The `merge` call adds the entering value with count 1 or raises its count. The leaving value is read from the array before `left` moves. When the count reaches 0, the method removes the key, and `counts.size()` is correct again.

#### Cost Of The Scan

Each index enters the map once and leaves it at most once, and each map operation costs O(1) on average. The time is O(n). The map holds at most `k + 1` keys, so the extra memory is O(min(n, k)).

<!-- stage: applicability -->
### When The Count Map Applies

#### Spotting An At-Most-K Request

Look for a request for the longest block with at most `k` different values. Typical wording is "at most two kinds of fruit" or "at most `k` distinct characters". The condition is monotone under removal. A shorter block never holds more different values than a longer block that contains it.

#### The Invariant To State

The map holds only positive counts, and its keys are exactly the values of the window. Every statement about `size()` depends on this. State it before the loop, because a stale zero entry causes a bug that small samples hide.

#### A Stale Zero Entry Is A False Friend

A key with count 0 left in the map looks harmless, because its count is correct. The key count is not. The expression `counts.size()` stops measuring distinct values, and the window shrinks more than it must. A second false friend is the "sum of counts" of the map, which equals the window length and says nothing about distinct values.

#### Java Habits For This Pattern

Use `merge` for the entering value and `remove` when a count reaches 0. For a small known alphabet, use an `int[]` and a separate distinct counter, which avoids boxing. Do not call `size()` on a map that keeps zero entries. Read `nums[left]` before incrementing `left`.

<!-- stage: exercises -->
### Exercises

#### [Build] Longest Segment With One Distinct Value (Author exercise)
<!-- id: sw-one-distinct -->

**Prerequisites.** The count map and the key removal of this lesson.

**Problem.** Given an integer array `nums`, return the length of the longest contiguous block in which all values are equal. The method keeps one active value and its count. When a different value enters, the shrink loop removes the block's values until the count is 0.

**Constraints.**
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are `int` values.
- **Return** type is `int`, and an empty array gives 0.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [5,5,2,2,2,7]`. Output `3`.

**Example 2.** Input `nums = [9]`. Output `1`.

**Hint.** When a different value enters, how many values must leave before the window holds one distinct value again?

**Changed decision.** The limit is one distinct value, and the map shrinks to a single key and its count.

#### [Vary] Fruit Into Baskets (LeetCode 904)
<!-- id: sw-fruit-baskets -->

**Prerequisites.** The one-value exercise above.

**Problem.** Given an integer array `fruits`, where `fruits[i]` is the type of fruit on tree `i`, return the length of the longest contiguous block that contains at most two different types.

**Constraints.**
- **Length** satisfies `1 <= fruits.length <= 10^5`.
- **Values** satisfy `0 <= fruits[i] < fruits.length`.
- **Return** type is `int`.
- **Mutation** does not occur; `fruits` is unchanged.

**Example 1.** Input `fruits = [1,2,1,3,3,2,2]`. Output `4`.

**Example 2.** Input `fruits = [4,4,4]`. Output `3`.

**Hint.** When a leaving type has count 0, what must the method do with its key?

**Changed decision.** The limit of distinct types is two, and the map can hold three keys for a moment.

#### [Boundary] K Is Zero (Author exercise)
<!-- id: sw-k-zero -->

**Prerequisites.** The two exercises above.

**Problem.** The input is an integer array `nums` and a limit `k >= 0`. Return the length of the longest contiguous block with at most `k` different values. For `k = 0`, no non-empty block qualifies, and the answer is 0. The method must not read a count below 0 or move `left` beyond `right + 1`.

**Constraints.**
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Limit** satisfies `0 <= k <= 10^5`.
- **Values** are `int` values.
- **Return** type is `int`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [4,4]`, `k = 0`. Output `0`.

**Example 2.** Input `nums = [1,2,2]`, `k = 1`. Output `2`.

**Hint.** With `k = 0`, which value does the shrink loop remove when the first value enters?

**Changed decision.** The window may shrink to empty, and `left` may equal `right + 1`.

#### [Recognize] Longest Substring With At Most K Distinct Characters (Author exercise)
<!-- id: sw-at-most-k-chars -->

**Prerequisites.** All three exercises above.

**Problem.** Given a string `s` and an integer `k` with `k >= 0`, return the length of the longest substring that contains at most `k` different characters.

**Constraints.**
- **Length** satisfies `0 <= s.length <= 10^5`.
- **Characters** are any ASCII characters, codes 0 to 127.
- **Limit** satisfies `0 <= k <= 128`.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "eceba"`, `k = 2`. Output `3`, from `ece`.

**Example 2.** Input `s = "aaabbb"`, `k = 1`. Output `3`.

**Hint.** Which exercise above has the same loop? What replaces the integer key?

**Changed decision.** The values are characters, and a count array of 128 entries can replace the map.
