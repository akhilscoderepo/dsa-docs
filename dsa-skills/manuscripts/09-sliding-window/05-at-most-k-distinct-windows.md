<!-- lesson-kind: standard -->
<!-- lesson-id: at-most-k-distinct-windows -->
## At-Most-K Distinct Windows

<!-- stage: context -->
### A Librarian And A Display Sign

A school librarian is setting up a display along one long shelf. Every book carries a genre sticker, and the genres repeat all along the shelf. The display sign has room to name only k genres, and a book whose genre is not on the sign cannot be part of the display. She wants the longest stretch of neighbouring books that the sign could cover, which means a stretch whose books come from at most k different genres.

The shelf is catalogued from left to right, so she knows the genre of every position. She can pick a book, walk right while the genres still fit on the sign, and write down how many books she covered. The trouble is that after that, she cannot tell whether the best stretch begins at this book, at the next one, or somewhere much farther along, and she does not want to guess.

<!-- stage: naive -->
### Restart From Every Book

The direct plan is to treat every book as a possible start, walk right from it while the genres still fit on the sign, and remember the longest walk.

```java
static int longestByRestart(int[] shelf, int k) {
    int best = 0;
    for (int start = 0; start < shelf.length; start++) {
        Set<Integer> seen = new HashSet<>();
        int end = start;                       // end is one past the last book covered
        while (end < shelf.length) {
            seen.add(shelf[end]);
            if (seen.size() > k) break;
            end++;
        }
        best = Math.max(best, end - start);
    }
    return best;
}
```

It is correct for every shelf, including a sign with no room at all, where the first book already does not fit and every walk has length zero.

<!-- stage: bottleneck -->
### Every Walk Repeats The Last One

Each start builds a new set and rereads books that the previous start already read. If the whole shelf holds one genre, every walk runs to the end, so the method does about n times n over two book readings, which is O(n^2). Shelves of a hundred thousand books are already out of reach.

The waste is easy to see. Walking from book 5 and walking from book 6 pass over almost exactly the same books, and the second walk learns nothing the first did not already know. What is needed is a way to move from the stretch that begins at 5 to the stretch that begins at 6 by dropping one book from the front, not by walking the whole stretch again. That needs a record of how many books of each genre are currently inside, so that dropping a book can tell us whether a genre just left the sign.

<!-- stage: insight -->
### Count Each Kind And Evict At Zero

Keep a window `[left, right]` and a **tally map** from each value to how many times it occurs inside the window. The invariant has two halves. First, the map holds a positive count for exactly the values in the window, so `map.size()` is the number of different values in it. Second, after each step the window is valid, meaning that size is at most k. The right edge moves one position at a time and adds a value. If the size now exceeds the **distinct budget** k, the left edge moves right, subtracting one from the count of the value it leaves, until the budget is met again.

The reason the left edge never has to move backwards is monotone validity. Removing values from a valid window cannot add a new kind of value, so a valid window stays valid when it shrinks. If the window ending at `right` could not start at `left` because it was over budget, no later window ending further right can start at `left` either, since it would contain everything this one does. That is the argument that lets each position be added once and evicted at most once, so the total work is O(n) map operations.

The step that is easiest to get wrong is **eviction** of a key. When a count drops to zero the key must be removed from the map, not left with a zero. Otherwise `size()` keeps counting genres that are no longer present, the window looks over budget when it is not, and the loop shrinks too far. The invariant is exactly what makes `size()` a trustworthy count of kinds.

<!-- names: tally map, distinct budget, eviction -->

Once the window is valid, its length is a candidate for the best. Because the right edge only grows by one, comparing after the shrink loop, not before, records only valid lengths. The same shape solves any question of the form "longest stretch that uses few kinds", whether the items are numbers, characters, or genre codes.

<!-- stage: variables -->
### Edges, Tally And Best Length

`left` and `right` are the inclusive edges of the window, and `right` is the loop variable. The map `tally` pairs each value with a positive count, and its size is the number of different values inside. The limit k is read, never changed. `best` holds the longest valid window seen so far and starts at zero, which is also the correct answer for an empty input and for k equal to zero. When the window is empty, `left` equals `right + 1`, and its length `right - left + 1` is zero, which is why the arithmetic never needs a special case.

<!-- stage: trace -->
### Evicting Whole Kinds From The Left

The first trace runs on the shelf 1, 2, 1, 3, 3, 2, 1 with a sign for two genres. The window grows freely over the first three books, since only genres 1 and 2 are present. The step to study is the fourth, at position 3, where the new genre 3 pushes the tally to three kinds and the left edge must travel two positions before a key leaves.

```trace
{"cells":[1,2,1,3,3,2,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"tally":"1x1","best":1},"note":"Position 0 holds 1, so its count becomes 1. The tally holds 1 value, within the limit of 2. Window length 1, best so far 1."},{"at":{"left":0,"right":1},"vars":{"tally":"1x1 2x1","best":2},"note":"Position 1 holds 2, so its count becomes 1. The tally holds 2 values, within the limit of 2. Window length 2, best so far 2."},{"at":{"left":0,"right":2},"vars":{"tally":"1x2 2x1","best":3},"note":"Position 2 holds 1, so its count becomes 2. The tally holds 2 values, within the limit of 2. Window length 3, best so far 3."},{"at":{"left":2,"right":3},"vars":{"tally":"1x1 3x1","best":3},"note":"Position 3 holds 3, so its count becomes 1. The tally would be over the limit of 2, so the left edge drops 2 positions (1, 2) until a key disappears, and left becomes 2. Window length 2, best so far 3."},{"at":{"left":2,"right":4},"vars":{"tally":"1x1 3x2","best":3},"note":"Position 4 holds 3, so its count becomes 2. The tally holds 2 values, within the limit of 2. Window length 3, best so far 3."},{"at":{"left":3,"right":5},"vars":{"tally":"3x2 2x1","best":3},"note":"Position 5 holds 2, so its count becomes 1. The tally would be over the limit of 2, so the left edge drops 1 position (1) until a key disappears, and left becomes 3. Window length 3, best so far 3."},{"at":{"left":5,"right":6},"vars":{"tally":"2x1 1x1","best":3},"note":"Position 6 holds 1, so its count becomes 1. The tally would be over the limit of 2, so the left edge drops 2 positions (3, 3) until a key disappears, and left becomes 5. Window length 2, best so far 3."}]}
```

The second trace uses letters and a sign for three genres, on the shelf x, y, x, z, z, w, x, y. Here the best window is reached early, at length five, and later steps shrink the window without ever beating it. The step to study is the last one, where a single new letter evicts three positions because the letter z had a count of two and both copies had to leave before the key vanished.

```trace
{"cells":["x","y","x","z","z","w","x","y"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"tally":"xx1","best":1},"note":"Position 0 holds x, so its count becomes 1. The tally holds 1 value, within the limit of 3. Window length 1, best so far 1."},{"at":{"left":0,"right":1},"vars":{"tally":"xx1 yx1","best":2},"note":"Position 1 holds y, so its count becomes 1. The tally holds 2 values, within the limit of 3. Window length 2, best so far 2."},{"at":{"left":0,"right":2},"vars":{"tally":"xx2 yx1","best":3},"note":"Position 2 holds x, so its count becomes 2. The tally holds 2 values, within the limit of 3. Window length 3, best so far 3."},{"at":{"left":0,"right":3},"vars":{"tally":"xx2 yx1 zx1","best":4},"note":"Position 3 holds z, so its count becomes 1. The tally holds 3 values, within the limit of 3. Window length 4, best so far 4."},{"at":{"left":0,"right":4},"vars":{"tally":"xx2 yx1 zx2","best":5},"note":"Position 4 holds z, so its count becomes 2. The tally holds 3 values, within the limit of 3. Window length 5, best so far 5."},{"at":{"left":2,"right":5},"vars":{"tally":"xx1 zx2 wx1","best":5},"note":"Position 5 holds w, so its count becomes 1. The tally would be over the limit of 3, so the left edge drops 2 positions (x, y) until a key disappears, and left becomes 2. Window length 4, best so far 5."},{"at":{"left":2,"right":6},"vars":{"tally":"xx2 zx2 wx1","best":5},"note":"Position 6 holds x, so its count becomes 2. The tally holds 3 values, within the limit of 3. Window length 5, best so far 5."},{"at":{"left":5,"right":7},"vars":{"tally":"xx1 wx1 yx1","best":5},"note":"Position 7 holds y, so its count becomes 1. The tally would be over the limit of 3, so the left edge drops 3 positions (x, z, z) until a key disappears, and left becomes 5. Window length 3, best so far 5."}]}
```

<!-- stage: code -->
### One Loop Three Shapes

```java
static int longestAtMostK(int[] a, int k) {
    Map<Integer, Integer> tally = new HashMap<>();
    int left = 0, best = 0;
    for (int right = 0; right < a.length; right++) {
        tally.merge(a[right], 1, Integer::sum);
        while (tally.size() > k) {
            int out = a[left++];
            if (tally.merge(out, -1, Integer::sum) == 0) tally.remove(out);   // evict at zero
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

static int longestSingleKind(int[] a) {
    int best = 0, run = 0, key = 0;
    for (int i = 0; i < a.length; i++) {
        if (run > 0 && a[i] == key) run++;
        else { key = a[i]; run = 1; }
        best = Math.max(best, run);
    }
    return best;
}

static int longestLetters(String s, int k) {
    int[] seen = new int[128];
    int kinds = 0, left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        if (seen[s.charAt(right)]++ == 0) kinds++;
        while (kinds > k) {
            if (--seen[s.charAt(left++)] == 0) kinds--;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

The general version makes at most two map operations per position, one when `right` adds it and one when `left` removes it, so it runs in expected linear time and holds at most k plus one keys. `Map.merge` returns the new value, which lets the same call decrement and decide about eviction. The single-kind version keeps just a key and a count, since with a budget of one the whole map collapses into those two variables. The letter version swaps the map for an array and a separate `kinds` counter, so the counter must be adjusted exactly when a count crosses zero in either direction.

<!-- stage: applicability -->
### Spotting A Few-Kinds Budget

Reach for this window when the question asks for the longest or shortest stretch that uses no more than k different kinds, and when throwing items away from a valid stretch can only keep it valid. Before writing anything, state the invariant aloud: the map holds a positive count for exactly the values inside. If you cannot say that sentence, the eviction line will be wrong.

A false friend is the fixed-size window, because here the length is the thing being maximised and it changes at every step. Another is the "exactly k kinds" question, which looks identical but is not monotone, since removing a value from a window with exactly k kinds can drop it to k minus one. A third is a hand-rolled distinct counter that is not updated when a count crosses zero in both directions.

In Java, remember that `map.size()` counts keys, so a leftover zero entry silently breaks every later comparison. Handle k equal to zero deliberately: the window becomes empty after each addition, and the answer stays zero. Use `Integer::sum` through `merge` for counters, and prefer an array when the alphabet is small and known.

<!-- stage: exercises -->
### Exercises

#### [Build] Longest Segment With One Distinct Value (Author exercise)
<!-- id: sw-one-kind-run -->

**Prerequisites.** The fixed-size window lesson, and the idea of an invariant that a single count can carry.

**Problem.** Given an array of integers, return the length of the longest run of consecutive positions that all hold the same value. Keep only the current key and how many times it has been seen in a row, not a map.

**Constraints.** 0 <= nums.length <= 200000 and any `int` values. Use one pass and constant extra space.

**Example 1.** Input `nums = [4, 4, 9, 9, 9, 4]`, output 3.

**Example 2.** Input `nums = []`, output 0.

**Hint.** What does the map degenerate to when only one kind is allowed? What should happen to the count when the next value differs from the key?

**Changed decision.** First rung: the budget is one, so the whole tally collapses into a single key and a counter, and eviction means starting over.

#### [Vary] Fruit Into Baskets (LeetCode 904)
<!-- id: sw-fruit-baskets -->

**Prerequisites.** The one-kind exercise above.

**Problem.** Trees stand in a row and each tree bears one type of fruit, given as an integer. You carry two baskets and each basket holds only one type, without a size limit. Starting at any tree, you pick one fruit from every tree moving right and must stop before a tree whose fruit fits neither basket. Return the most trees you can pick from.

**Constraints.** 1 <= fruits.length <= 100000 and 0 <= fruits[i] < 100000. Run in expected linear time.

**Example 1.** Input `fruits = [5, 8, 5, 8, 3, 3, 8]`, output 4.

**Example 2.** Input `fruits = [2, 2, 2]`, output 3.

**Hint.** How many kinds may the window hold? When the third kind arrives, which positions must leave before the map is back within budget?

**Changed decision.** The budget is a story constant of two, and the answer is the window length, so nothing changes except the story that hides the invariant.

#### [Boundary] K Is Zero (Author exercise)
<!-- id: sw-k-zero -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array and an integer `k` that may be zero, return the length of the longest window holding at most `k` different values. When `k` is zero, the answer is zero for every array. Make sure no count goes negative and that `left` never passes `right + 1`.

**Constraints.** 0 <= nums.length <= 50000, 0 <= k <= 100000 and any `int` values. Single pass, expected linear time.

**Example 1.** Input `nums = [3, 1, 3], k = 0`, output 0.

**Example 2.** Input `nums = [3, 1, 3], k = 5`, output 3.

**Hint.** What does the shrink loop do right after the first addition when the budget is zero? Where does `left` end up, and what is the window length then?

**Changed decision.** The budget is so small that every addition is immediately evicted, so the loop must reach an empty window without underflow.

#### [Recognize] Longest Substring With At Most K Distinct Characters (Author exercise)
<!-- id: sw-k-distinct-chars -->

**Prerequisites.** The three exercises above.

**Problem.** Given a string of lowercase letters and an integer `k`, return the length of the longest substring that contains at most `k` different letters. The problem looks like a string task, so decide which structure carries the counts.

**Constraints.** 0 <= s.length() <= 100000, 0 <= k <= 26, and only `a` to `z` appear. Aim for a single pass with a fixed-size count array.

**Example 1.** Input `s = "aabbcbbd", k = 2`, output 5.

**Example 2.** Input `s = "zzzz", k = 1`, output 4.

**Hint.** Which counter tells you how many kinds are inside? At what two moments does it change?

**Changed decision.** The items are characters, so a count array replaces the map, and a separate counter replaces `size()`.
