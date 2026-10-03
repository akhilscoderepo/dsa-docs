<!-- lesson-kind: standard -->
<!-- lesson-id: minimum-cover-and-deficit-windows -->
## Minimum-Cover And Deficit Windows

<!-- stage: context -->
### A Photographer Along The Parade

A town parade passes a single long barrier, and the floats come by one after another, each painted in one colour. A photographer has been hired to take one picture that shows a red float and a blue float together. The camera can only frame a stretch of consecutive floats, and every extra float in the frame makes the picture busier, so she wants the shortest stretch that still shows both colours. A later request is stricter: the client wants two red floats and a blue one in the same frame.

She has the colour list of the whole parade in front of her, written in order of passing. Pointing to a stretch and checking by eye whether it shows what the client asked for takes a moment, and she wants to avoid doing it for every possible stretch. Stretches that are too short to show everything are useless to her, while stretches that show too much are only wasteful, and she needs a way to find the tightest one.

<!-- stage: naive -->
### Try Every Frame And Tally Colours

The plain plan is to try every first float, extend the frame one float at a time, and after each extension tally every colour in the frame to see whether both are present. The first extension that works gives the shortest frame for that start.

```java
static int shortestFrameByTally(String parade, char want1, char want2) {
    int best = -1;
    for (int first = 0; first < parade.length(); first++) {
        for (int last = first; last < parade.length(); last++) {
            boolean saw1 = false, saw2 = false;
            for (int k = first; k <= last; k++) {
                if (parade.charAt(k) == want1) saw1 = true;
                if (parade.charAt(k) == want2) saw2 = true;
            }
            if (saw1 && saw2) {
                int length = last - first + 1;
                if (best == -1 || length < best) best = length;
                break;
            }
        }
    }
    return best;
}
```

It returns the correct length for any parade, and minus one when one of the colours never appears.

<!-- stage: bottleneck -->
### Tallying Again After Each Extension

There are three nested loops here. The two outer loops pick a first and a last float, which is already quadratic, and the innermost loop reads the whole frame again just to learn one more yes or no. In a parade of n floats where the wanted colours show up only at the very end, the inner tally runs over frames of every length for every start, so the total reading is O(n^3) in the worst case, or O(n^2) if the tally is kept as a running count for each start. Neither is acceptable for a long parade.

The repeated work has two sources. The first is that the tally of a frame differs from the tally of the frame one float longer by exactly one float, so rebuilding it is wasteful. The second is that when a frame from float 10 already works, the frame from float 11 does not need to restart from float 11: the right end of the best frame for float 11 can never lie left of the right end for float 10. A pair of moving edges and a running tally of what is still lacking removes both costs and gives O(n).

<!-- stage: insight -->
### Shrink While The Window Still Works

Write down what the client demands as a table of required copies for each colour. As the window grows to the right, keep a **deficit ledger**: for every required colour, how many more copies are still needed, and as one number, the **missing count**, the total of those shortfalls. Adding a float of a required colour whose shortfall is above zero reduces the missing count by one. Adding a float of any other colour, or a surplus copy of a satisfied colour, changes nothing in the ledger.

<!-- names: deficit ledger, missing count, tightest cover -->

The window is a cover exactly when the missing count is zero. At that moment the loop does the opposite of the previous lesson: it records the window as a candidate, then removes the leftmost float and updates the ledger, and repeats while the window is still a cover. Only when the removal turns the missing count above zero does the loop stop shrinking and let `right` move again. This is how the **tightest cover** for each right end is found. Removing a float of a colour whose count stays at or above the requirement is free, and that is how surplus floats leave the front of the frame.

The invariant is this. The ledger always matches the window exactly, and every start to the left of `left` has already been recorded as covering for some earlier right end or was shown unable to cover anything further. A longer window from the same start cannot beat a recorded shorter one, so nothing better is ever discarded. Note the order: the record comes before the removal, because after the removal the window may no longer be a cover.

<!-- stage: variables -->
### Needs, Missing And Best Pair

`need` holds the required copies per symbol, and a symbol that is not required has need zero. `missing` starts as the sum of all needs, and it is the only value the loop checks. Because a surplus copy must not push the ledger below its true value, the add step decrements `missing` only when the symbol's current need is still positive, and the count in `need` itself may go negative to remember the surplus. `bestStart` and `bestLength` remember the best boundaries, and the length starts as a sentinel larger than any window, so that no cover found means the sentinel is still there.

<!-- stage: trace -->
### Two Frames Of One Parade

The first trace uses the parade q, a, b, x, x, c, b, a, q, z and asks for one each of a, b and c. The missing count drops from three to zero by position 5, where the window q, a, b, x, x, c is first a cover. The step to study is that one: the shrink loop records length 6, removes q for free, records the better length 5, then removes a and breaks the cover, so left stops at 2.

```trace
{"cells":["q","a","b","x","x","c","b","a","q","z"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"missing":3,"best":0},"note":"Position 0 (q) is added. Missing is 3, so the window is not a cover yet."},{"at":{"left":0,"right":1},"vars":{"missing":2,"best":0},"note":"Position 1 (a) is added. Missing is 2, so the window is not a cover yet."},{"at":{"left":0,"right":2},"vars":{"missing":1,"best":0},"note":"Position 2 (b) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":0,"right":3},"vars":{"missing":1,"best":0},"note":"Position 3 (x) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":0,"right":4},"vars":{"missing":1,"best":0},"note":"Position 4 (x) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":2,"right":5},"vars":{"missing":1,"best":5},"note":"Position 5 (c) completes a cover. The shrink loop records length 5, removes 2 floats, and left becomes 2. Missing is back to 1."},{"at":{"left":2,"right":6},"vars":{"missing":1,"best":5},"note":"Position 6 (b) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":6,"right":7},"vars":{"missing":1,"best":3},"note":"Position 7 (a) completes a cover. The shrink loop records length 3, removes 4 floats, and left becomes 6. Missing is back to 1."},{"at":{"left":6,"right":8},"vars":{"missing":1,"best":3},"note":"Position 8 (q) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":6,"right":9},"vars":{"missing":1,"best":3},"note":"Position 9 (z) is added. Missing is 1, so the window is not a cover yet."}]}
```

The second trace asks for two a and one b on the parade a, b, a, x, b, b, a, x, a, which shows multiplicities. The step to study is the one at position 2: the second a arrives, the ledger reaches zero, the length 3 is recorded as the best, and the shrink loop takes off a and then breaks the cover again. Later windows can tie that length but cannot beat it.

```trace
{"cells":["a","b","a","x","b","b","a","x","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"missing":2,"best":0},"note":"Position 0 (a) is added. Missing is 2, so the window is not a cover yet."},{"at":{"left":0,"right":1},"vars":{"missing":1,"best":0},"note":"Position 1 (b) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":1,"right":2},"vars":{"missing":1,"best":3},"note":"Position 2 (a) completes a cover. The shrink loop records length 3, removes 1 floats, and left becomes 1. Missing is back to 1."},{"at":{"left":1,"right":3},"vars":{"missing":1,"best":3},"note":"Position 3 (x) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":1,"right":4},"vars":{"missing":1,"best":3},"note":"Position 4 (b) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":1,"right":5},"vars":{"missing":1,"best":3},"note":"Position 5 (b) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":3,"right":6},"vars":{"missing":1,"best":3},"note":"Position 6 (a) completes a cover, but length is no better than the best. 2 floats leave and left becomes 3."},{"at":{"left":3,"right":7},"vars":{"missing":1,"best":3},"note":"Position 7 (x) is added. Missing is 1, so the window is not a cover yet."},{"at":{"left":6,"right":8},"vars":{"missing":1,"best":3},"note":"Position 8 (a) completes a cover, but length is no better than the best. 3 floats leave and left becomes 6."}]}
```

<!-- stage: code -->
### Ledger Loop And The Substring Once

```java
static int[] tightestSpan(String parade, int[] need) {
    int[] ledger = need.clone();
    int missing = 0;
    for (int n : ledger) missing += Math.max(n, 0);
    int left = 0, bestStart = -1, bestLength = Integer.MAX_VALUE;
    for (int right = 0; right < parade.length(); right++) {
        int in = parade.charAt(right);
        if (ledger[in]-- > 0) missing--;
        while (missing == 0) {
            if (right - left + 1 < bestLength) {
                bestLength = right - left + 1;
                bestStart = left;
            }
            int out = parade.charAt(left++);
            if (++ledger[out] > 0) missing++;
        }
    }
    return bestStart == -1 ? new int[] {-1, 0} : new int[] {bestStart, bestLength};
}

static String shortestCover(String parade, String wanted) {
    int[] need = new int[128];
    for (char c : wanted.toCharArray()) need[c]++;
    int[] span = tightestSpan(parade, need);
    return span[0] == -1 ? "" : parade.substring(span[0], span[0] + span[1]);
}
```

Each position enters and leaves the window at most once, so the cost is O(n + m) with an extra table of 128 counters, where m is the length of the wanted text. The ledger is allowed to go negative for surplus symbols, and `missing` rises again only when a count climbs back above zero. The substring is built a single time, after the scan, and only when a cover exists.

<!-- stage: applicability -->
### Telling A Cover From A Match

Choose this method when the question demands that a stretch contain certain symbols, perhaps with required counts, and the target is the shortest such stretch. Before coding, say the invariant in one sentence: the ledger describes the window exactly, and the record is taken while the window is still a cover. Then decide the three moves, namely the add that lowers `missing`, the record, and the removal that may raise it again.

The false friend is a fixed signature. The previous lessons asked whether a window holds exactly the same letters as a pattern, and for that the window has a fixed length. A cover may hold any amount of surplus, so its length is not known in advance, and a table equality check would reject covers that contain extra letters. A second false friend is the longest-valid shape from the last lesson, which records after repair; copying that order here records windows that are no longer covers.

In Java, keep the table of needs separate from the table that moves, or clone it as the code does, because the needs are consulted by later queries. Let counts go negative rather than clamping them, since clamping destroys the surplus bookkeeping. Return the best boundaries, not the substring, until the end, so that a missing cover costs no string at all.

<!-- stage: exercises -->
### Exercises

#### [Build] Shortest Segment Containing A And B (Author exercise)
<!-- id: sw-shortest-a-and-b -->

**Prerequisites.** The longest-valid exercises of the previous lesson, and a counter for two symbols.

**Problem.** Given a string of lowercase letters, return the length of the shortest substring that contains at least one `a` and at least one `b`, or minus one when no such substring exists. Expand until both appear, then shrink away surplus symbols from the left.

**Constraints.** 0 <= s.length() <= 100000 and lowercase letters only. Linear time, with two counters and no string building.

**Example 1.** Input `s = "bxxxaxxb"`, output 4.

**Example 2.** Input `s = "cccc"`, output -1.

**Hint.** When both counters are positive, is the window a candidate? What happens to the answer if you remove the leftmost symbol and the window still shows both?

**Changed decision.** First rung: the window is recorded while valid and then shrunk, the reverse of the longest-valid order of repair first and record second.

#### [Vary] Required Multiplicities (Author exercise)
<!-- id: sw-required-multiplicities -->

**Prerequisites.** The shortest-segment exercise above.

**Problem.** Given a lowercase string and an array `need` of 26 counts, return the length of the shortest substring that has at least `need[c]` copies of every letter `c`, or minus one when none exists. At least one count is positive. Track how many letters have reached their required count, instead of asking whether a letter is present.

**Constraints.** 1 <= s.length() <= 100000, each `need[c]` is between 0 and 100000, and the array `need` must be left unchanged.

**Example 1.** Input `s = "abaxbbaxa", need[a] = 2, need[b] = 1`, output 3.

**Example 2.** Input `s = "xaybxa", need[a] = 2, need[b] = 1`, output 5.

**Hint.** Which event makes a letter newly satisfied, and which makes it unsatisfied again? Does a third copy of a letter change the number of satisfied letters?

**Changed decision.** Presence is replaced by a count requirement, so the check moves from "is it there" to "has its count reached the demand", and the number of satisfied letters is the ledger.

#### [Boundary] No Cover Exists (Author exercise)
<!-- id: sw-no-cover-exists -->

**Prerequisites.** The two exercises above.

**Problem.** Given strings `s` and `t` of lowercase letters, find the leftmost shortest window of `s` that contains every letter of `t` with its multiplicity. Return the pair `[start, length]`, or `[-1, 0]` when no window covers. Return the pair, never a substring, so a failed search builds nothing.

**Constraints.** 1 <= t.length() <= 10000 and 0 <= s.length() <= 100000. Cover `t` longer than `s` and letters absent from `s` without special loops.

**Example 1.** Input `s = "qq", t = "qqq"`, output `[-1, 0]`.

**Example 2.** Input `s = "zxyzyx", t = "xyz"`, output `[0, 3]`.

**Hint.** If the ledger never reaches zero, what does the record still hold? Which single value distinguishes no cover from a cover of length zero?

**Changed decision.** The empty answer is a first-class result: the best pair keeps its sentinel when no window ever reaches missing zero, and nothing needs to be cut out of `s`.

#### [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-min-window-substring -->

**Prerequisites.** All three exercises above.

**Problem.** Given strings `s` and `t`, return the shortest substring of `s` that contains every character of `t`, counting duplicates, or the empty string if none exists. Remember the best boundaries during the scan and create the substring a single time at the end.

**Constraints.** 1 <= s.length(), t.length() <= 100000, characters have codes below 128, and an answer of equal length is the leftmost. Both inputs are read-only.

**Example 1.** Input `s = "kxyzxkzyxk", t = "xxkz"`, output `"kxyzx"`.

**Example 2.** Input `s = "abc", t = "abcc"`, output `""`.

**Hint.** What are the three moves of the ledger, and in which order do the record and the removal happen? When is the substring call made?

**Changed decision.** The tables hold arbitrary characters with duplicates in `t`, and the output form is a string that is built once, not an index pair.
