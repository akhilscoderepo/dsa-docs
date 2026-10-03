<!-- lesson-kind: combination -->
<!-- lesson-id: sorting-and-intervals -->
## Sorting And Intervals

<!-- stage: context -->
### The Coworking Space Calendar

A coworking space rents its meeting rooms by the hour, and the manager keeps a long list of booked sessions, each one a start hour and an end hour. Four jobs land on her desk in the same week. The wall display should show busy blocks, so touching or overlapping sessions must be shown as one bar. A late request arrives, and it must be fitted into the already tidy calendar. The fire marshal wants the fewest sessions cancelled so that the remaining ones never clash in the single large hall. And the front desk wants the fewest loudspeaker announcements, where each announcement reaches every session running at that moment, so that every session hears at least one.

The bookings were typed in by many people, so they sit in no particular order. The manager suspects that the four jobs are cousins, since they all ask about overlap, but she also sees that the answers look very different: one is a union, one is a position, one is a set of survivors, and one is a set of moments.

<!-- stage: contributions -->
### What Sorting And Overlap Each Bring

Sorting brings order. Once the sessions are laid out by one end of the interval, a single scan can carry a small summary of everything already seen, and the decision about the next session needs only that summary. Without the sort, the same decision needs a comparison with every earlier session. Sorting alone, however, does not say what the summary should be or what to do when the next session touches it.

The interval rules bring meaning. They say whether a shared endpoint is an overlap, which end of a block is extended, and which of two clashing sessions is the better one to keep. Those rules turn a sorted list into an answer, and a different rule on the same sorted list gives a different answer.

The recognition cue is a question about overlap among unordered intervals where one value, the furthest end so far or the last kept end, can stand for the whole processed prefix.

<!-- stage: naive -->
### Fuse Any Clashing Pair Until Calm

The direct approach for the display is to search the whole list for any two sessions that clash, fuse them into one, and repeat until a full search finds no clash.

```java
static List<int[]> fuseUntilCalm(int[][] sessions) {
    List<int[]> work = new ArrayList<>();
    for (int[] s : sessions) work.add(s.clone());
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int a = 0; a < work.size() && !changed; a++) {
            for (int b = a + 1; b < work.size() && !changed; b++) {
                int[] x = work.get(a), y = work.get(b);
                if (x[0] <= y[1] && y[0] <= x[1]) {
                    x[0] = Math.min(x[0], y[0]);
                    x[1] = Math.max(x[1], y[1]);
                    work.remove(b);
                    changed = true;
                }
            }
        }
    }
    return work;
}
```

It is correct because it stops only when no two remaining sessions clash, and every fusion keeps all the hours of both sessions.

<!-- stage: bottleneck -->
### Every Fusion Restarts The Search

One fusion removes one session, so a list of n sessions can need n fusions. Each fusion restarts the pair search from the top, and a full search costs O(n^2) comparisons, which makes the whole job O(n^3). A hundred thousand sessions would take about 10^15 comparisons. The same repeated search is the only tool the clumsy method has for the other three jobs too, so none of them is cheaper.

The cost comes from not knowing where to look. After a fusion, the only sessions that can clash with the new block lie next to it on the time line, but an unordered list gives no hint of which those are. If the sessions were arranged by start hour, then a session could clash only with the block that is still open when it begins, and one number, the end of that open block, would answer the question. That brings the merge to O(n log n) for the sort and O(n) for the scan.

<!-- stage: insight -->
### Pick The Order Then Carry One End

The first decision is the **sort key**. Sorting by start hour lays out sessions so that any block already closed is finished for good, which suits unions and insertion. Sorting by end hour makes the session that frees the room soonest come first, which suits keeping the most sessions or placing the fewest announcements. The sort key is chosen from the question and not from habit, and it is the one thing the sorted scan cannot repair later.

The second decision is the **carried end**: the single number that stands for everything processed so far. For a union it is the furthest end of the open block. For selection it is the end of the last kept session. For announcements it is the coordinate of the last announcement. Each next session is compared with that number and nothing else, so one scan replaces a comparison with every earlier session.

The third decision is the **overlap test** applied against the carried end. A closed contract treats equality as a clash, so the test is start at most the carried end. A half-open contract treats equality as free, so the test is start strictly below it. The same sorted scan then answers a different question simply because the test and the update change.

The invariant is that the carried end summarizes every processed session exactly for the question being asked, so the decision for the next session never needs to look back.

<!-- names: sort key, carried end, overlap test -->

Merging is the false friend for the selection and announcement questions, because fusing sessions destroys the identity of the ones to cancel and the individual sessions that each announcement must reach.

<!-- stage: variables -->
### One Sorted Copy, One Carried End

Every method here works on a sorted copy, `sorted`, so the manager's original list keeps its order and the indices she reports still refer to it. For a union, `blockStart` and `blockEnd` describe the open block and `absorbed` counts the sessions inside it. For selection, `lastEnd` is the end of the last kept session and `kept` collects original indices. For announcements, `shot` is the coordinate of the most recent announcement and the list `shots` collects them. The comparison between a new start and the carried end is written once and chosen from the contract. Values are compared with `Integer.compare`, never by subtraction, and the carried end is held in a `long` so that the starting sentinel cannot collide with a real hour.

<!-- stage: trace -->
### Same Walk, Two Questions

The first trace merges the closed sessions 8 to 10, 1 to 4, 2 to 6, 5 to 7, 15 to 18 and 16 to 17 after sorting by start. The cells show the sorted order, `i` points at the session being read, and `block` points at the session that opened the current block. At the fourth step the session 8 to 10 starts after the carried end 7, so a new block opens and the pointer `block` jumps to it. Notice that the last session 16 to 17 changes nothing, because its end 17 does not pass the carried end 18.

```trace
{"cells":["1-4","2-6","5-7","8-10","15-18","16-17"],"pointers":["i","block"],"steps":[{"at":{"i":0,"block":0},"vars":{"carriedEnd":4,"blocks":1},"note":"The session 1 to 4 is the first one, so the first block opens and the carried end becomes 4."},{"at":{"i":1,"block":0},"vars":{"carriedEnd":6,"blocks":1},"note":"The session 2 to 6 starts at or before the carried end and reaches further, so the carried end grows to 6."},{"at":{"i":2,"block":0},"vars":{"carriedEnd":7,"blocks":1},"note":"The session 5 to 7 starts at or before the carried end and reaches further, so the carried end grows to 7."},{"at":{"i":3,"block":3},"vars":{"carriedEnd":10,"blocks":2},"note":"The session 8 to 10 starts after the carried end, so a new block opens here and the carried end becomes 10."},{"at":{"i":4,"block":4},"vars":{"carriedEnd":18,"blocks":3},"note":"The session 15 to 18 starts after the carried end, so a new block opens here and the carried end becomes 18."},{"at":{"i":5,"block":4},"vars":{"carriedEnd":18,"blocks":3},"note":"The session 16 to 17 starts at or before the carried end and ends inside it, so nothing changes."}]}
```

The second trace places announcements for the closed sessions 3 to 9, 0 to 6, 5 to 10, 11 to 13 and 12 to 15, sorted by end. Now the carried end is the last announcement, and the pointer `shot` marks the session that fixed it. The session 3 to 9 starts at 3, which is not after the announcement at 6, so it already heard it. The session 11 to 13 starts after 6, so a new announcement is made at its end, 13, and the final session 12 to 15 hears that one.

```trace
{"cells":["0-6","3-9","5-10","11-13","12-15"],"pointers":["i","shot"],"steps":[{"at":{"i":0,"shot":0},"vars":{"lastShot":6,"announcements":1},"note":"The session 0 to 6 has not heard an announcement, so one is made at its end, 6."},{"at":{"i":1,"shot":0},"vars":{"lastShot":6,"announcements":1},"note":"The session 3 to 9 starts at 3, which is not after the announcement at 6, so it already heard it."},{"at":{"i":2,"shot":0},"vars":{"lastShot":6,"announcements":1},"note":"The session 5 to 10 starts at 5, which is not after the announcement at 6, so it already heard it."},{"at":{"i":3,"shot":3},"vars":{"lastShot":13,"announcements":2},"note":"The session 11 to 13 has not heard an announcement, so one is made at its end, 13."},{"at":{"i":4,"shot":3},"vars":{"lastShot":13,"announcements":2},"note":"The session 12 to 15 starts at 12, which is not after the announcement at 13, so it already heard it."}]}
```

<!-- stage: code -->
### Four Questions, One Sorted Scan

```java
static int[][] mergeWithCounts(int[][] sessions) {
    int[][] sorted = copyAndSort(sessions, 0);
    List<int[]> blocks = new ArrayList<>();
    for (int[] s : sorted) {
        int[] last = blocks.isEmpty() ? null : blocks.get(blocks.size() - 1);
        if (last != null && s[0] <= last[1]) {
            last[1] = Math.max(last[1], s[1]);
            last[2]++;
        } else {
            blocks.add(new int[] {s[0], s[1], 1});
        }
    }
    return blocks.toArray(new int[0][]);
}

static int[] keptIndices(int[][] sessions) {
    Integer[] order = new Integer[sessions.length];
    for (int i = 0; i < order.length; i++) order[i] = i;
    Arrays.sort(order, (x, y) -> sessions[x][1] != sessions[y][1]
            ? Integer.compare(sessions[x][1], sessions[y][1]) : Integer.compare(x, y));
    List<Integer> kept = new ArrayList<>();
    long lastEnd = Long.MIN_VALUE;
    for (int idx : order) {
        if (sessions[idx][0] >= lastEnd) { kept.add(idx); lastEnd = sessions[idx][1]; }
    }
    Collections.sort(kept);
    return kept.stream().mapToInt(Integer::intValue).toArray();
}

static int[] announcementPoints(int[][] sessions) {
    int[][] sorted = copyAndSort(sessions, 1);
    List<Integer> shots = new ArrayList<>();
    long shot = Long.MIN_VALUE;
    for (int[] s : sorted) {
        if (shots.isEmpty() || s[0] > shot) { shot = s[1]; shots.add(s[1]); }
    }
    return shots.stream().mapToInt(Integer::intValue).toArray();
}

static int[][] copyAndSort(int[][] src, int key) {
    int[][] copy = new int[src.length][];
    for (int i = 0; i < copy.length; i++) copy[i] = src[i].clone();
    Arrays.sort(copy, (a, b) -> Integer.compare(a[key], b[key]));
    return copy;
}
```

Every method pays for one sort and then one linear scan, so the time is O(n log n) and the space is O(n) for the copies and the answers.

<!-- stage: applicability -->
### Choosing The Order And The Carried End

Reach for a sorted scan when many unordered intervals are asked an overlap question and one value can summarize the processed prefix. The invariant is that the carried end stands for every processed interval exactly as far as the question needs, so each decision looks at the new interval and that one number only.

A false friend is assuming that sorting alone fixes the answer, since the same sorted list yields a union, a survivor set, or a set of points depending on the key and the update. A second false friend is merging first and then counting, which loses the identity of the original intervals that selection and announcement questions must report. A third is sorting an insertion problem that already arrives sorted and disjoint, which wastes a log factor and can reorder the answer.

In Java, sort a clone or an index array so that the caller's list and indices survive, compare with `Integer.compare`, and choose between `<` and `<=` from the stated contract. When ties are possible in the sort key, state the secondary key, since the reported set depends on it.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge With Counts (LeetCode 56)
<!-- id: iv-sorting-merge-counts -->

**Prerequisites.** Merge And Insert, and the endpoint contract lessons.

**Problem.** Given closed intervals in any order, merge every group that overlaps or touches, and return each block as `[start, end, count]`, where `count` is the number of original intervals inside the block. Blocks are returned in increasing start order.

**Constraints.** 1 <= intervals.length <= 50000 and -1000000000 <= start <= end <= 1000000000.

**Example 1.** Input `intervals = [[15, 18], [1, 3], [8, 10], [2, 6]]`, output `[[1, 6, 2], [8, 10, 1], [15, 18, 1]]`.

**Example 2.** Input `intervals = [[4, 5], [1, 4]]`, output `[[1, 5, 2]]`.

**Hint.** Which key puts a closed block's members next to each other? What must happen to the counter when a block opens?

**Changed decision.** The sorted scan carries a count beside the furthest end, so each block reports how many originals it swallowed.

#### [Vary] Insert Position And Absorbed Count (LeetCode 57)
<!-- id: iv-sorting-insert-position -->

**Prerequisites.** Merge With Counts.

**Problem.** Given a sorted list of disjoint half-open intervals and a new half-open interval, report `[position, absorbed]`. The new interval absorbs every list interval that shares at least one point with it, and touching alone does not absorb. The position is the index that the grown interval takes in the resulting list, and `absorbed` is the number of list intervals it swallows. Do not sort.

**Constraints.** 0 <= list.length <= 100000, 0 <= start < end <= 1000000000 for every interval.

**Example 1.** Input `list = [[1, 3], [6, 9]], extra = [2, 5]`, output `[0, 1]`.

**Example 2.** Input `list = [[1, 2], [3, 4]], extra = [2, 3]`, output `[1, 0]`.

**Hint.** How many list intervals end at or before the new start? Which ones start strictly before the new end and end strictly after the new start?

**Changed decision.** The list is already ordered, so three regions are counted in one pass and the half-open test keeps touching intervals out of the absorbed region.

#### [Boundary] Kept Indices With A Tie Rule (LeetCode 435)
<!-- id: iv-sorting-kept-indices -->

**Prerequisites.** Insert Position And Absorbed Count, and Overlap And Coverage.

**Problem.** Given half-open intervals, return the original indices of the intervals kept by this rule: order the indices by end, breaking equal ends by the smaller index, and keep an index when its interval starts at or after the end of the last kept interval. Return the kept indices in increasing order.

**Constraints.** 1 <= intervals.length <= 100000 and -2147483648 <= start < end <= 2147483647.

**Example 1.** Input `intervals = [[2, 5], [0, 3], [3, 6], [1, 4], [6, 9]]`, output `[1, 2, 4]`.

**Example 2.** Input `intervals = [[1, 2], [1, 2]]`, output `[0]`.

**Hint.** What must the sort carry besides the interval so the report can name an original position? Why must the equal-end rule be written down?

**Changed decision.** The sort is over indices and not over copies of the intervals, so the answer can name the originals and the tie rule decides which duplicate survives.

#### [Recognize] Announcement Coordinates (LeetCode 452)
<!-- id: iv-sorting-arrow-positions -->

**Prerequisites.** Kept Indices With A Tie Rule.

**Problem.** Each session is a closed span, and an announcement at a coordinate reaches every session whose span contains it. Return the coordinates of the announcements chosen by shooting at the end of the first session that has not yet heard one, in increasing order. The list must be as short as possible.

**Constraints.** 1 <= points.length <= 100000 and -2147483648 <= start <= end <= 2147483647.

**Example 1.** Input `points = [[4, 12], [1, 5], [6, 8], [2, 4], [9, 14]]`, output `[4, 8, 14]`.

**Example 2.** Input `points = [[1, 1]]`, output `[1]`.

**Hint.** Which coordinate reaches the first session and still covers as many later sessions as possible? When does a session need a new announcement?

**Changed decision.** The scan reports the coordinates themselves and not their count, so the carried end is stored as a list entry whenever it moves.
