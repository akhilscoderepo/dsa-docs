<!-- lesson-kind: combination -->
<!-- lesson-id: greedy-and-ordering -->
## Greedy And Ordering

<!-- stage: context -->
### The Stage Manager Of Fairmoor Festival

Fairmoor Festival runs for one weekend and its stage manager has four jobs that all arrive on the same morning. She must give each helper a pair of gloves, and the gloves come in sizes that only fit a helper whose hands are not larger. She must fill the main stage with as many acts as the schedule allows, given that every act has a start and an end. She must place launch points for the fireworks, where one launch point lights every shell whose burst window contains it. And she must cut the printed programme into sections so that no performer's name appears in two sections.

Her assistant suggests sorting everything first. The stage manager agrees that a sorted list makes each job look easier, but she has seen sorted lists mislead people. Sorting by the wrong thing gave her a half-empty stage last year, and she wants to know what makes one order trustworthy.

<!-- stage: contributions -->
### What Sorting And The Proof Each Bring

Ordering brings visibility. Once the items are arranged by the right key, the choice that looks best sits at the front, so a single walk through the list can find it again and again without searching. Sorting also gives a clean place to apply a rule, such as comparing the next start with the last end.

The greedy proof brings permission. It explains why the front item may be committed without reconsidering the others, because an optimal plan can be changed to contain it without losing anything. An order has no authority by itself, and a proof has no speed by itself. Together they give a fast method that is also correct. The cue for the combination is a problem where some key, a size, an end, or a last position, determines which item to settle first, and the settled item shrinks the problem to the items that remain.

<!-- stage: naive -->
### Quadratic Pairwise Comparison

A method that is certainly correct for the stage and does not depend on any rule about order sorts the acts by end time and then, for each act, looks at every earlier act to see which could precede it. It records the longest chain of acts that fit one after another.

```java
static int longestChain(int[][] acts) {                      // half-open spans
    int[][] s = acts.clone();
    Arrays.sort(s, (a, b) -> Integer.compare(a[1], b[1]));
    int[] best = new int[s.length];
    int answer = 0;
    for (int i = 0; i < s.length; i++) {
        best[i] = 1;
        for (int j = 0; j < i; j++)
            if (s[j][1] <= s[i][0]) best[i] = Math.max(best[i], best[j] + 1);
        answer = Math.max(answer, best[i]);
    }
    return answer;
}
```

The answer is exact for any list of acts, since every pair is checked. It is also an honest baseline for ten thousand acts, though the pair loop is slow.

<!-- stage: bottleneck -->
### Every Pair Is Compared Again

The inner loop examines all earlier acts for every act, so the method does O(n^2) comparisons and keeps an array of n counts. Yet the answer for an act depends on very little. After the sort, the best chain that can precede an act is the best chain among acts that ended by its start, and that quantity can only grow as the ends grow, so a single running figure would do.

The same waste appears in the other jobs. Gloves can be matched by trying every glove for every helper, and the programme can be cut by testing every possible cut position against every performer. Each time, the pairwise check ignores that the sorted order has already arranged the candidates so that the first one that qualifies is the best one that qualifies.

<!-- stage: insight -->
### A Sort Key That Shows Dominance

Choosing the **sort key** is the real decision. The key is right when the item at the front of the order dominates the others for everything that remains. For gloves and helpers, sort both by size. The smallest helper takes the smallest glove that fits, and the exchange argument of Lesson 04 shows that no larger glove is wasted. For acts, sort by end time. The earliest-ending act leaves the stage free soonest, and a second form of proof says the same thing more strongly: the greedy plan **stays ahead**, meaning that after any number of picks its latest end is no later than the latest end of any other plan with that many acts. A plan that stays ahead can never be overtaken, so it ends with the most acts.

<!-- names: sort key, stays ahead, tie rule -->

For the programme, the key is the last position at which each performer appears. A section may close at position i exactly when every performer seen so far has its last appearance at or before i. The greedy plan closes a section the first moment that holds, and that is the earliest legal cut, so it makes the most sections, each as short as possible.

Ordering does not settle everything. Equal keys need a **tie rule**, a stated way to break ties, because two items with the same size or the same end can lead to different plans with the same value, and the proof must hold for the rule chosen. For acts, any order among equal ends gives the same count. For gloves, equal sizes can be taken in index order so that the output is determined.

<!-- stage: variables -->
### Pointers, Boundaries And Last Positions

For the assignment, `k` is the next helper in size order who still has no glove, and the loop walks gloves in size order. For the acts, `boundary` is the end of the last accepted act and `kept` counts accepted acts. For the firework points, `at` is the position of the current launch point, which is the earliest end among the group it serves. For the programme, `last[c]` holds the final position of each letter, `end` is the farthest last position among letters seen since `start`, and `start` is the first position of the open section. A section closes when the index equals `end`. Sorting copies the input and never alters it, and ties are broken by input index.

<!-- stage: trace -->
### A Programme Cut And A Glove Match

The first trace cuts the programme `xyxzzwvwvu` into sections. Reading from the left, the letter `x` last appears at position two, so the section cannot close before that. The `y` last appears at position one, which is inside the reach, and the next `x` is the last one, so the index meets the end and the first section closes with three characters. The pair of `z` closes the second section after two characters. Then `w` reaches seven and `v` reaches eight, so the third section runs to eight with four characters. The final `u` is a section of its own.

The second trace matches gloves to helpers. Helpers need sizes 2, 5 and 7, and the gloves come in sizes 1, 3, 5 and 9, listed here in size order. The glove of size one fits nobody, since the smallest helper needs two, so it stays unused. Glove three fits the helper who needs two, glove five fits the helper who needs five, and glove nine fits the helper who needs seven.

```trace
{"cells":["x","y","x","z","z","w","v","w","v","u"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"start":0,"end":2,"sizes":"none"},"note":"Letter 'x' last appears at 2, which pushes the section end from 0 to 2."},{"at":{"i":1},"vars":{"start":0,"end":2,"sizes":"none"},"note":"Letter 'y' last appears at 1, inside the current reach 2, so the section end stays."},{"at":{"i":2},"vars":{"start":3,"end":2,"sizes":"3"},"note":"Letter 'x' has its last occurrence at 2, and the index has reached the section end 2, so the section 0 to 2 closes with 3 characters."},{"at":{"i":3},"vars":{"start":3,"end":4,"sizes":"3"},"note":"Letter 'z' last appears at 4, which pushes the section end from 2 to 4."},{"at":{"i":4},"vars":{"start":5,"end":4,"sizes":"3-2"},"note":"Letter 'z' has its last occurrence at 4, and the index has reached the section end 4, so the section 3 to 4 closes with 2 characters."},{"at":{"i":5},"vars":{"start":5,"end":7,"sizes":"3-2"},"note":"Letter 'w' last appears at 7, which pushes the section end from 4 to 7."},{"at":{"i":6},"vars":{"start":5,"end":8,"sizes":"3-2"},"note":"Letter 'v' last appears at 8, which pushes the section end from 7 to 8."},{"at":{"i":7},"vars":{"start":5,"end":8,"sizes":"3-2"},"note":"Letter 'w' last appears at 7, inside the current reach 8, so the section end stays."},{"at":{"i":8},"vars":{"start":9,"end":8,"sizes":"3-2-4"},"note":"Letter 'v' has its last occurrence at 8, and the index has reached the section end 8, so the section 5 to 8 closes with 4 characters."},{"at":{"i":9},"vars":{"start":10,"end":9,"sizes":"3-2-4-1"},"note":"Letter 'u' has its last occurrence at 9, and the index has reached the section end 9, so the section 9 to 9 closes with 1 character."}]}
```

```trace
{"cells":["1","3","5","9"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"served":0,"nextNeed":2},"note":"The glove of size 1 is smaller than the 2 that the next helper needs, so it fits nobody and stays unused."},{"at":{"i":1},"vars":{"served":1,"nextNeed":5},"note":"The glove of size 3 fits the helper who needs 2, who is next in size order, so it is given to them."},{"at":{"i":2},"vars":{"served":2,"nextNeed":7},"note":"The glove of size 5 fits the helper who needs 5, who is next in size order, so it is given to them."},{"at":{"i":3},"vars":{"served":3,"nextNeed":"none"},"note":"The glove of size 9 fits the helper who needs 7, who is next in size order, so it is given to them."}]}
```

<!-- stage: code -->
### Four Sorted Sweeps

```java
static int[] gloveOwners(int[] need, int[] glove) {              // glove -> helper index, or -1
    Integer[] helpers = new Integer[need.length], gloves = new Integer[glove.length];
    for (int i = 0; i < helpers.length; i++) helpers[i] = i;
    for (int i = 0; i < gloves.length; i++) gloves[i] = i;
    Arrays.sort(helpers, (a, b) -> need[a] != need[b] ? Integer.compare(need[a], need[b]) : Integer.compare(a, b));
    Arrays.sort(gloves, (a, b) -> glove[a] != glove[b] ? Integer.compare(glove[a], glove[b]) : Integer.compare(a, b));
    int[] owner = new int[glove.length];
    Arrays.fill(owner, -1);
    int k = 0;
    for (int g : gloves) if (k < helpers.length && glove[g] >= need[helpers[k]]) owner[g] = helpers[k++];
    return owner;
}

static long[] removalsAndBoundary(int[][] acts) {                // {removed, last end}
    int[][] s = acts.clone();
    Arrays.sort(s, (a, b) -> Integer.compare(a[1], b[1]));
    int kept = 0;
    long boundary = -1;
    for (int[] r : s) if (r[0] >= boundary) { kept++; boundary = r[1]; }
    return new long[]{acts.length - kept, boundary};
}

static long[] launchPoints(long[][] shells) {                     // {centre, radius} -> {points, last point}
    long[][] w = new long[shells.length][];
    for (int i = 0; i < w.length; i++) w[i] = new long[]{shells[i][0] - shells[i][1], shells[i][0] + shells[i][1]};
    Arrays.sort(w, (a, b) -> Long.compare(a[1], b[1]));
    long points = 0, at = 0;
    for (long[] x : w) if (points == 0 || x[0] > at) { points++; at = x[1]; }
    return new long[]{points, at};
}

static List<Integer> sectionSizes(String s) {
    int[] last = new int[26];
    for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;
    List<Integer> out = new ArrayList<>();
    int start = 0, end = 0;
    for (int i = 0; i < s.length(); i++) {
        end = Math.max(end, last[s.charAt(i) - 'a']);
        if (i == end) { out.add(i - start + 1); start = i + 1; }
    }
    return out;
}
```

Each sweep is linear after its sort, so the acts and launch points cost O(n log n), the gloves cost O(n log n + m log m), and the programme needs only one pass over the text. The window ends are formed in `long` before comparing, because a centre and a radius near the `int` limits add to more than an `int` holds. The comparators avoid subtraction.

<!-- stage: applicability -->
### When The Order Is Also Proven

Use this combination when a sort key makes the settled item obvious and an exchange or stays-ahead argument shows that settling it loses nothing. The invariant is that after each settled item an optimal completion of the remaining items still exists, and the sorted order guarantees that the next candidate is the dominant one. Write the key, the tie rule and the proof sentence before coding.

The false friend is sorting without the proof. Sorting acts by start is natural for merging and leads straight to a wrong greedy for selection, and sorting helpers by name or arrival says nothing about fit. A rule that merely looks tidy after sorting is only a heuristic. The combination also stops applying when the objective carries weights, or when the settled item changes what the others cost, since a heavy long act may beat several light short ones.

In Java, sort index arrays when the answer is reported by original position, use `Integer.compare` and `Long.compare` in comparators, and widen sums of endpoints to `long` before comparing.

<!-- stage: exercises -->
### Exercises

#### [Build] Assign Cookies (LeetCode 455)
<!-- id: gc-cookie-owners -->

**Prerequisites.** The local-choice lesson of this chapter; sorting index arrays from Chapter 05.

**Problem.** Child `i` is content with any cookie of size at least `greed[i]`, and each cookie goes to at most one child. Return an array with one entry per cookie, holding the index of the child that cookie satisfies or -1 if the cookie is not used. Serve children from the least greedy upwards, breaking ties by the lower child index, and offer cookies from the smallest upwards, breaking ties by the lower cookie index. The number of children served must be as large as possible.

**Constraints.** 0 <= greed.length, sizes.length <= 100000 and every value is between 1 and 2147483647.

**Example 1.** Input `greed = [7, 2, 5]`, `sizes = [5, 1, 3, 9]`, output `[2, -1, 1, 0]`.

**Example 2.** Input `greed = [2, 2]`, `sizes = [2, 2, 2]`, output `[0, 1, -1]`, since the last cookie is left over.

**Hint.** What must the sort carry along so that the answer can be reported by original position? Which child is waiting when a cookie is too small?

**Changed decision.** Positions, not values, are the output, so the sorted orders are orders of indexes with explicit tie rules.

#### [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: gc-removals-and-boundary -->

**Prerequisites.** The interval-scheduling lesson of this chapter.

**Problem.** Given half-open spans, return two values: the smallest number of spans to remove so that none of the rest overlap, and the end of the last span that remains, or -1 if no span remains. Spans that touch do not overlap.

**Constraints.** 0 <= acts.length <= 100000 and 0 <= start < end <= 1000000000.

**Example 1.** Input `acts = [[1, 4], [2, 3], [3, 6], [5, 7], [4, 5]]`, output `[2, 7]`.

**Example 2.** Input `acts = [[0, 5], [0, 5], [5, 10]]`, output `[1, 10]`.

**Hint.** What does the second value say about how far ahead the greedy plan is, compared with any other plan of the same size? Does it depend on how equal ends are ordered?

**Changed decision.** Besides the count, the free boundary after the last pick is reported, which makes the stays-ahead claim concrete.

#### [Boundary] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: gc-launch-points -->

**Prerequisites.** The two exercises above.

**Problem.** Each balloon is described by a centre `c` and a radius `r >= 0`, and it covers the closed span from `c - r` to `c + r`. A shot at a point bursts every balloon whose span contains the point, and balloons that touch at a single point are both burst by a shot there. Return the fewest shots and the position of the last shot, placing each shot at the earliest end of the group it serves. If there are no balloons, return `[0, 0]`.

**Constraints.** 0 <= balloons.length <= 100000, 0 <= r <= 2147483647 and `c` is any `int`. The span ends can fall outside the `int` range.

**Example 1.** Input `balloons = [[5, 3], [1, 1], [9, 2], [12, 0]]`, output `[3, 12]`.

**Example 2.** Input `balloons = [[2147483647, 2147483647], [0, 0]]`, output `[1, 0]`.

**Hint.** What does `c + r` do in 32-bit arithmetic? Is a balloon that begins exactly at the last shot already burst?

**Changed decision.** The endpoint test is the closed one, and the ends themselves are computed in a wider type before any comparison.

#### [Recognize] Partition Labels (LeetCode 763)
<!-- id: gc-section-sizes -->

**Prerequisites.** All three exercises above.

**Problem.** Cut a lowercase string into as many pieces as possible so that each letter appears in at most one piece. Return the lengths of the pieces in order.

**Constraints.** 0 <= s.length() <= 100000 and `s` has only the letters `a` to `z`.

**Example 1.** Input `s = "xyxzzwvwvu"`, output `[3, 2, 4, 1]`.

**Example 2.** Input `s = "mnopqmrst"`, output `[6, 1, 1, 1]`.

**Hint.** Where is the earliest position at which a cut is legal after a piece has started? What must be true of every letter seen since the piece began?

**Changed decision.** The order is the order of last occurrences, and a piece is closed only when the scan reaches the farthest last occurrence of its own letters.
