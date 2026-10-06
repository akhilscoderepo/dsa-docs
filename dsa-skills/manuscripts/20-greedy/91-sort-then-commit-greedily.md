<!-- lesson-kind: combination -->
<!-- lesson-id: sort-then-commit -->
## Sort Then Commit Greedily

<!-- stage: context -->
### Why A Log Archiver Cannot Cut Anywhere

A log archiver reads a stream of events. Each event carries a one-letter service code. The archiver cuts the stream into consecutive chunks and ships each chunk to its own archive node. A query about one service must touch only one node, so every service code may appear in exactly one chunk. The operator wants as many chunks as possible, because each chunk is one parallel upload.

One chunk for the whole stream is always legal. Cutting after every event is usually illegal. The archiver needs the cuts that are legal and as many as possible. This lesson asks how a program finds them in one pass, and what the same idea shares with the matching and scheduling problems of the earlier lessons.

<!-- stage: contributions -->
### What Order And Proof Each Add

Two earlier ideas combine in this lesson. Sorting, or reading in a chosen order, makes the next decision visible. After sorting jobs by end time, the next job to consider is the first unread one. After sorting cookies by size, the smallest cookie that matters is at the front. Order alone gives the program a way to read the input, and it says nothing about whether a choice is right.

The exchange argument from the earlier lessons gives the reason a choice is safe. It shows that committing to the front item leaves an optimal completion for everything after it. Neither idea works alone. A proof without an order has no front item to commit to, and an order without a proof is a guess that happens to sort. The combined rule reads: sort by the quantity that the exchange step compares, then commit to each item that fits.

<!-- stage: naive -->
### Trying Every Set Of Cut Positions

The direct plan tries every set of cut positions. For a stream of `n` events there are `n - 1` gaps, and each gap is cut or not. The plan checks that no service code appears in two chunks and keeps the largest legal set.

```java
static int mostChunksByTrying(String log) {
    int n = log.length(), best = 1;
    for (int mask = 0; mask < (1 << (n - 1)); mask++) {          // bit g set means cut after event g
        int[] owner = new int[26];
        Arrays.fill(owner, -1);
        int chunk = 0;
        boolean legal = true;
        for (int i = 0; i < n && legal; i++) {
            int code = log.charAt(i) - 'a';
            if (owner[code] != -1 && owner[code] != chunk) legal = false;   // code seen in an earlier chunk
            owner[code] = chunk;
            if (i < n - 1 && (mask >> i & 1) != 0) chunk++;
        }
        if (legal) best = Math.max(best, chunk + 1);
    }
    return best;
}
```

```predict
How many cut sets does the plan test for a stream of 40 events, and how long does one test take?

It tests 2^39, about 550 billion, cut sets. One test reads the stream once, so the whole plan needs roughly 22 trillion steps. A stream of 40 events is tiny for a real archiver.
```

<!-- stage: bottleneck -->
### Counting The Cut Sets

The plan costs O(2^n * n) time. The count of cut sets doubles with every added event, so the plan is unusable beyond a few dozen events. It also ignores the structure of the legal cuts. A cut after position `i` is legal only when no service code on the left of the cut also appears on the right.

That condition does not depend on the other cuts. A program that could read the stream once and recognize a legal cut position directly would not need the search. The condition needs one number for each service code, the last position where it appears. The same shape appears in every problem of this chapter: one comparable number per item makes the next safe decision visible.

<!-- stage: insight -->
### Reading Items In Order Of One Number

#### Choosing The Sort Key

A **sort key** is the single number of an item that the exchange step compares. For the cookies it is the size. For intervals and balloons it is the end coordinate. For the archive stream it is the **last occurrence** of a service code, the largest index where the code appears. To find the key, ask which attribute of the front item takes room away from the items after it. That attribute is the key, and sorting or scanning by it puts the least costly item first.

#### Cutting At The Earliest Legal Place

For the stream, scan from the left and keep `end`, the largest last occurrence of any code read since the current chunk began. A cut after position `i` is legal exactly when `i == end`, because then every code in the chunk has its last occurrence inside the chunk. The scan cuts at the first such position. This is the **safe commit**. Take any best partition. If its first cut lies after the earliest legal cut, then moving that cut to the earliest legal position keeps all chunks legal and adds a cut, because the part after the new cut can still be cut where the old partition cut it. The partition cannot get worse, so the earliest cut starts some best partition.

#### One Pattern In Four Problems

The same three steps solve the four problems of this lesson. Find the key, order the items by it, and commit to the front item whenever it is legal. For cookies the legal test is that the cookie is large enough. For intervals it is that the start is at least the previous end plus any required gap. For balloons it is that the start does not pass the current arrow. For the stream it is that the scan index equals `end`.

<!-- names: sort key, last occurrence, safe commit -->

<!-- stage: variables -->
### State For The Stream Scan

The scan over the stream needs an array and three numbers. Five items describe the state.

- **last** is an array of 26 entries, and `last[c]` is the largest index of code `c` in the stream.
- **start** is the index where the current chunk began.
- **end** is the largest `last` value among the codes read since `start`.
- **i** is the index of the event under test.
- **sizes** is the list of finished chunk lengths, and the scan adds `i - start + 1` when `i == end`.

The array `last` is the only structure built before the scan. It replaces the search over cut sets.

<!-- stage: trace -->
### Two Scans With A Committed Rule

#### Cutting The Stream

The first trace scans `abacbdeffed`. The array `last` holds a at 2, b at 4, c at 3, d at 10, e at 9 and f at 8. The pointer `i` marks the event under test.

The scan raises `end` to 2 at `a`, then to 4 at `b`. It reaches `i = 4`, which equals `end`, and cuts a chunk of length 5. The next chunk starts at `d`, which raises `end` to 10. The scan reaches index 10 and cuts a chunk of length 6.

```trace
{"cells":["a","b","a","c","b","d","e","f","f","e","d"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"end":2,"cuts":0},"note":"The letter a ends at 2, so end is 2."},{"at":{"i":1},"vars":{"end":4,"cuts":0},"note":"The letter b ends at 4, so end is 4."},{"at":{"i":2},"vars":{"end":4,"cuts":0},"note":"The letter a ends at 2, so end is 4."},{"at":{"i":3},"vars":{"end":4,"cuts":0},"note":"The letter c ends at 3, so end is 4."},{"at":{"i":4},"vars":{"end":4,"cuts":1},"note":"The letter b ends at 4, so end is 4. The index equals end, so the scan cuts a part of length 5."},{"at":{"i":5},"vars":{"end":10,"cuts":1},"note":"The letter d ends at 10, so end is 10."},{"at":{"i":6},"vars":{"end":10,"cuts":1},"note":"The letter e ends at 9, so end is 10."},{"at":{"i":7},"vars":{"end":10,"cuts":1},"note":"The letter f ends at 8, so end is 10."},{"at":{"i":8},"vars":{"end":10,"cuts":1},"note":"The letter f ends at 8, so end is 10."},{"at":{"i":9},"vars":{"end":10,"cuts":1},"note":"The letter e ends at 9, so end is 10."},{"at":{"i":10},"vars":{"end":10,"cuts":2},"note":"The letter d ends at 10, so end is 10. The index equals end, so the scan cuts a part of length 6."}]}
```

#### Scheduling With A Required Gap

The second trace uses intervals ordered by end: `[1,3)`, `[2,4)`, `[4,6)`, `[5,8)` and `[7,9)`, with a required gap of 1 between kept intervals. The scan accepts an interval when its start is at least the previous end plus 1. It accepts three intervals and removes two.

```trace
{"cells":["1-3","2-4","4-6","5-8","7-9"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"kept":1,"removed":0},"note":"The start 1 is at least the needed bound, so the scan keeps [1,3) and sets lastEnd to 3."},{"at":{"i":1},"vars":{"kept":1,"removed":1},"note":"The start 2 is below lastEnd + 1 = 4, so the scan removes [2,4)."},{"at":{"i":2},"vars":{"kept":2,"removed":1},"note":"The start 4 is at least the needed bound, so the scan keeps [4,6) and sets lastEnd to 6."},{"at":{"i":3},"vars":{"kept":2,"removed":2},"note":"The start 5 is below lastEnd + 1 = 7, so the scan removes [5,8)."},{"at":{"i":4},"vars":{"kept":3,"removed":2},"note":"The start 7 is at least the needed bound, so the scan keeps [7,9) and sets lastEnd to 9."}]}
```

<!-- stage: code -->
### Reading The Stream With Last Positions

```java
static List<Integer> cutSizes(String log) {
    int[] last = new int[26];
    for (int i = 0; i < log.length(); i++) last[log.charAt(i) - 'a'] = i;
    List<Integer> sizes = new ArrayList<>();
    int start = 0, end = 0;
    for (int i = 0; i < log.length(); i++) {
        end = Math.max(end, last[log.charAt(i) - 'a']);
        if (i == end) {
            sizes.add(i - start + 1);
            start = i + 1;
        }
    }
    return sizes;
}
```

The first loop overwrites `last` as it goes, so the final value of each code is its last position. The second loop is one pass and cuts as soon as every code in the chunk has ended. The sizes always sum to the length of the stream, because every position belongs to exactly one chunk.

- **Time** is O(n) for two passes over the stream, with a constant 26 for the array.
- **Space** is O(1) for the array, plus O(k) for the `k` chunk sizes returned.

<!-- stage: applicability -->
### Telling A Proven Order From A Guess

#### Applying The Invariant

Use this pattern when items compete for a limited resource and one comparable number tells which item costs the least. The invariant is that after each commitment, a best completion still exists for the items not yet read. Name the sort key and say in one sentence why the exchange step keeps the invariant. If you cannot say it, you have only a heuristic that sorts.

#### Finding Cases That Break The Precondition

A false friend is sorting by a number that only looks natural. Start time suits merging and fails for the largest compatible set. Shortest length fails the same problem. A second false friend is a sort that helps but never gets a proof, as with sorting a weighted scheduling problem by weight alone. Weighted choices need the state comparison of the dynamic programming chapters.

#### Avoiding Java Pitfalls

Index the 26-entry array with `ch - 'a'` and state that the input holds lowercase letters only. Compare keys with `Integer.compare`. When items keep their original positions in the result, sort an array of positions and not the items themselves. Fix the tie rule before you sort, because equal keys can change which positions an answer lists.

<!-- stage: exercises -->
### Exercises

#### [Build] Assign Cookies (LeetCode 455)
<!-- id: gr-sort-satisfied-children -->

**Prerequisites.** Lesson 01 and the sort key of this lesson.

**Problem.** Array `g` holds the least cookie size that each child accepts, and array `s` holds the cookie sizes. A cookie of size `x` satisfies child `i` when `x >= g[i]`. Each cookie and each child is used at most once. Order the children by `g`, breaking ties by smaller position. Scan the sorted cookies and give each cookie to the first unsatisfied child in that order when it fits. Return the positions of the satisfied children in increasing order.

**Constraints.** The limits are:
- **Count** is `0 <= g.length, s.length <= 3 * 10^4`.
- **Values** are integers in `1 <= value <= 2^31 - 1`.
- **Positions** start at 0 in the order of `g`.
- **Mutation** of the input arrays does not occur.

**Example 1.** Input `g = [3,1,2]` and `s = [2,3]`, output `[1,2]`.

**Example 2.** Input `g = [2,2,2]` and `s = [1,2]`, output `[0]`.

**Hint.** Sort positions by greed, not the values themselves.

**Changed decision.** The method lists which children are satisfied and not how many.

#### [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: gr-intervals-with-gap -->

**Prerequisites.** Lesson 02 and the sort key of this lesson.

**Problem.** Each interval is half-open, `[start, end)`. A required gap `gap` separates two kept intervals: the start of a kept interval must be at least the end of the previous kept interval plus `gap`. Return the smallest number of intervals to remove so that all kept intervals satisfy the gap rule.

**Constraints.** The limits are:
- **Count** is `0 <= intervals.length <= 10^5`.
- **Values** are integers in `0 <= start < end <= 10^9`.
- **Gap** is an integer in `0 <= gap <= 10^9`.
- **Sum** of `end + gap` can pass the `int` range.

**Example 1.** Input `intervals = [[1,3],[2,4],[4,6],[5,8],[7,9]]` and `gap = 1`, output 2.

**Example 2.** Input `intervals = [[1,3],[3,5],[5,7]]` and `gap = 1`, output 1.

**Hint.** Which number does the exchange step compare, and what does the gap add to it?

**Changed decision.** The compatibility test adds a gap to the previous end.

#### [Boundary] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: gr-half-open-balloons -->

**Prerequisites.** Lesson 02 and the sort key of this lesson.

**Problem.** Each balloon spans the half-open range `[start, end)` of integer coordinates. An arrow at an integer `x` bursts every balloon with `start <= x < end`. A balloon whose `end` equals the start of another does not share a coordinate with it. Return the smallest number of arrows that burst all balloons.

**Constraints.** The limits are:
- **Count** is `0 <= balloons.length <= 10^5`.
- **Values** are integers in `-2^31 <= start < end <= 2^31 - 1`.
- **Touching** ranges need separate arrows.
- **Overflow** can occur if the method computes `end - 1` or `end - start` in `int`.

**Example 1.** Input `balloons = [[1,3],[3,5],[2,4]]`, output 2.

**Example 2.** Input `balloons = [[1,4],[2,5],[3,6]]`, output 1.

**Hint.** An arrow at the last integer inside the first range ends at which coordinate?

**Changed decision.** The shared-endpoint rule is half-open, not closed.

#### [Recognize] Partition Labels (LeetCode 763)
<!-- id: gr-partition-labels -->

**Prerequisites.** The stream scan of this lesson.

**Problem.** String `s` holds lowercase English letters. Cut `s` into consecutive nonempty parts so that each letter appears in at most one part. Among all such cuts, choose one with the largest number of parts. Return the lengths of the parts in order.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters.
- **Return** is an empty list for the empty string.
- **Mutation** does not occur.

**Example 1.** Input `s = "abacbdeffed"`, output `[5,6]`.

**Example 2.** Input `s = "aabbcc"`, output `[2,2,2]`.

**Hint.** At which index may the current part close, and why?

**Changed decision.** The sort key is the last position of a letter.
