<!-- lesson-kind: combination -->
<!-- lesson-id: window-frequency-state -->
## Window Frequency State

<!-- stage: context -->
### Matching A Bead Order To A Strand

A jeweller buys beads on very long strands, and every bead is one of twenty-six colours, written as the letters a to z. A customer brings a small order card that lists some beads, for example two reds and one blue, and asks her to find a stretch of the strand where those beads sit side by side, in any order and with nothing else among them. For a card with m beads she looks at m neighbouring beads at a time and asks whether they are exactly what the card lists.

The strand is thousands of beads long, and the cards are sometimes dozens of beads long, so she cannot afford to recount every colour each time she steps along. She also meets related requests on the same strand. One customer wants the longest stretch in which no colour appears twice. Another allows a few beads to be recoloured. A third gives a card and wants the shortest stretch that contains everything on it.

<!-- stage: contributions -->
### What The Frame And The Tally Bring

The frame brings the question of which beads are under consideration. Two ends move along the strand, and a step of the frame adds one bead at the right and drops one at the left, a constant amount of work whatever the frame's length. The frame alone cannot answer the customer, because it says nothing about the colours inside it. To judge a stretch it would have to look at every bead again.

The tally brings the question of what is inside. A row of twenty-six counters says how many of each colour sit under the frame, and adding or dropping a bead changes one counter. The tally alone cannot answer either, because without ends it has no notion of which bead to drop when the stretch becomes wrong, nor where the stretch starts. Each part settles what the other cannot. The frame says which beads to change the tally for, and the tally says whether the stretch is acceptable.

The recognition cue is a question about a contiguous stretch whose acceptability depends only on how many times each symbol occurs in it, such as a rearrangement of a card, a stretch with no repeats, a repair budget, or a cover of a list.

<!-- stage: naive -->
### Recount Every Stretch From Scratch

The direct method takes each starting bead in turn, counts the colours of the next m beads into a fresh row of counters, builds the counters of the card, and compares the two rows.

```java
static int firstStartByRecount(String strand, String order) {
    int m = order.length();
    for (int start = 0; start + m <= strand.length(); start++) {
        int[] under = new int[26];
        for (int i = start; i < start + m; i++) under[strand.charAt(i) - 'a']++;
        int[] listed = new int[26];
        for (int i = 0; i < m; i++) listed[order.charAt(i) - 'a']++;
        if (Arrays.equals(under, listed)) return start;
    }
    return -1;
}
```

It returns the first start whose beads are a rearrangement of the card, or minus one when there is none, including when the card is longer than the strand.

<!-- stage: bottleneck -->
### Neighbouring Stretches Share Almost Everything

Two neighbouring stretches of m beads share m minus one beads, yet the loop counts all m again, and it also rebuilds the card's counters every time. A strand of n beads costs O(n m) reads, plus twenty-six comparisons per start. With a strand of a million beads and a card of a thousand, that is a billion reads for an answer that one pass could produce.

The first repair is clear: keep one row of counters and update it, adding the bead that enters and removing the bead that leaves, so each step is O(1) reads. That leaves the comparison. Checking whether two rows of twenty-six counters are equal still costs twenty-six reads per step, which is O(26 n) in total and no better in shape. Only a smaller piece of state can make the check constant, so the question is what single number tells us that every colour agrees with the card.

<!-- stage: insight -->
### A Range, A Table And A Counter

Two pieces of state travel together. The **window range** is the pair of indices `left` and `right` that says which positions are active. The **count table** says, for every letter, how many of its occurrences lie inside that range. The combined invariant is a sentence about both: every entry of the table equals the number of times that letter occurs at positions `left` to `right`, and the range is exactly the part of the strand that the table describes. Moving an end without updating the table, or the reverse, breaks it.

For fixed length the table is not compared as a whole. A second table of the card's counts stays frozen, and a **matches counter** records how many of the twenty-six letters currently have the same count in both tables. Before a letter's count changes, if it agreed, the counter drops by one. After the change, if it agrees again, the counter rises by one. A step touches two letters at most, so the update is O(1), and the stretch is a rearrangement of the card exactly when the counter reads twenty-six.

<!-- names: window range, count table, matches counter -->

The same pair works when the length varies. For the longest stretch without repeats, the table says whether the letter that just entered now occurs twice, and the left end moves only while that is true. For a repair budget, the table gives the largest count, and the stretch is acceptable when its length minus that largest count fits in the budget. For a cover of a card with multiplicities, a counter of letters still short of the card says when the stretch is enough, and then the left end moves to make it as small as it can be. Only the question asked of the table changes, and the range moves forward every time.

<!-- stage: variables -->
### Ends, Two Tables And A Counter

`left` and `right` are the ends of the active range, both moving forward. `have` holds the counts of letters in the range, and `want` is the frozen table of the card, both indexed by letter. `matches` is the number of letters for which the two agree, so letters that the card does not mention agree at zero and are counted from the start. For variable length, `shrinkSteps` counts how often the left end moved, and `bestStart` and `bestLen` keep the winning range. In the cover problem `missing` counts the letters still short, and the answer pair is kept as a count and a first start. Nothing is written into the strand, and no piece of it is copied into a substring while the loop runs.

<!-- stage: trace -->
### Sliding A Card Across A Strand

The first trace looks for a rearrangement of the card abc in the strand b, c, x, a, b, d, c, a, b. The range is three beads wide, and the counter starts at twenty-three because every letter except a, b and c agrees with the card at zero. The step to study is the last one, where the b at position 8 enters and the d at position 5 leaves. The enter raises the agreement of b and the leave restores the agreement of d, so the counter goes from twenty-four to twenty-six in one step.

```trace
{"cells":["b","c","x","a","b","d","c","a","b"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"matches":24},"note":"Letter b enters at position 0. The range is still filling, and the counter reads 24."},{"at":{"left":0,"right":1},"vars":{"matches":25},"note":"Letter c enters at position 1. The range is still filling, and the counter reads 25."},{"at":{"left":0,"right":2},"vars":{"matches":24},"note":"Letter x enters at position 2. Matches counter is 24, so it is not a rearrangement."},{"at":{"left":1,"right":3},"vars":{"matches":24},"note":"Letter a enters at position 3. Letter b leaves from position 0. Matches counter is 24, so it is not a rearrangement."},{"at":{"left":2,"right":4},"vars":{"matches":24},"note":"Letter b enters at position 4. Letter c leaves from position 1. Matches counter is 24, so it is not a rearrangement."},{"at":{"left":3,"right":5},"vars":{"matches":24},"note":"Letter d enters at position 5. Letter x leaves from position 2. Matches counter is 24, so it is not a rearrangement."},{"at":{"left":4,"right":6},"vars":{"matches":24},"note":"Letter c enters at position 6. Letter a leaves from position 3. Matches counter is 24, so it is not a rearrangement."},{"at":{"left":5,"right":7},"vars":{"matches":24},"note":"Letter a enters at position 7. Letter b leaves from position 4. Matches counter is 24, so it is not a rearrangement."},{"at":{"left":6,"right":8},"vars":{"matches":26},"note":"Letter b enters at position 8. Letter d leaves from position 5. Matches counter is 26, so this range is a rearrangement and the answer is start 6."}]}
```

The second trace asks for the longest stretch without a repeated bead in the strand t, m, m, z, u, x, t and records the shrink steps. The step to study is the one right after the second m enters, where the left end has to move twice, because the stretch has to drop both the t and the first m before every count is at most one again.

```trace
{"cells":["t","m","m","z","u","x","t"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"shrinkSteps":0,"bestLen":1},"note":"Letter t enters at position 0. Every count is at most one. Width 1 beats the record, so the best range is now 0 to 0."},{"at":{"left":0,"right":1},"vars":{"shrinkSteps":0,"bestLen":2},"note":"Letter m enters at position 1. Every count is at most one. Width 2 beats the record, so the best range is now 0 to 1."},{"at":{"left":0,"right":2},"vars":{"shrinkSteps":0,"bestLen":2},"note":"Letter m enters at position 2. It now occurs twice, so the left end must move."},{"at":{"left":2,"right":2},"vars":{"shrinkSteps":2,"bestLen":2},"note":"The left end moved 2 times and now sits at 2, with all counts at most one."},{"at":{"left":2,"right":3},"vars":{"shrinkSteps":2,"bestLen":2},"note":"Letter z enters at position 3. Every count is at most one."},{"at":{"left":2,"right":4},"vars":{"shrinkSteps":2,"bestLen":3},"note":"Letter u enters at position 4. Every count is at most one. Width 3 beats the record, so the best range is now 2 to 4."},{"at":{"left":2,"right":5},"vars":{"shrinkSteps":2,"bestLen":4},"note":"Letter x enters at position 5. Every count is at most one. Width 4 beats the record, so the best range is now 2 to 5."},{"at":{"left":2,"right":6},"vars":{"shrinkSteps":2,"bestLen":5},"note":"Letter t enters at position 6. Every count is at most one. Width 5 beats the record, so the best range is now 2 to 6."}]}
```

<!-- stage: code -->
### Counter, Repeats, Budget And Cover

```java
static int firstPermutationStart(String strand, String order) {
    int m = order.length(), n = strand.length();
    if (m > n) return -1;
    int[] have = new int[26], want = new int[26];
    for (int i = 0; i < m; i++) want[order.charAt(i) - 'a']++;
    int matches = 0;
    for (int c = 0; c < 26; c++) if (have[c] == want[c]) matches++;
    for (int right = 0; right < n; right++) {
        int in = strand.charAt(right) - 'a';
        if (have[in] == want[in]) matches--;
        have[in]++;
        if (have[in] == want[in]) matches++;
        if (right >= m) {
            int out = strand.charAt(right - m) - 'a';
            if (have[out] == want[out]) matches--;
            have[out]--;
            if (have[out] == want[out]) matches++;
        }
        if (right >= m - 1 && matches == 26) return right - m + 1;
    }
    return -1;
}

static int[] leftmostLongestRepeatFree(String s) {
    int[] have = new int[128];
    int left = 0, shrinks = 0, bestStart = 0, bestLen = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        have[c]++;
        while (have[c] > 1) { have[s.charAt(left++)]--; shrinks++; }
        if (right - left + 1 > bestLen) { bestStart = left; bestLen = right - left + 1; }
    }
    return new int[] {bestStart, bestLen, shrinks};
}

static int[] bestRepaintWindow(String s, int k) {
    int[] have = new int[26];
    int left = 0, bestStart = 0, bestLen = 0;
    for (int right = 0; right < s.length(); right++) {
        have[s.charAt(right) - 'A']++;
        int most = 0;
        for (int v : have) most = Math.max(most, v);
        while (right - left + 1 - most > k) {
            have[s.charAt(left++) - 'A']--;
            most = 0;
            for (int v : have) most = Math.max(most, v);
        }
        if (right - left + 1 > bestLen) { bestStart = left; bestLen = right - left + 1; }
    }
    return new int[] {bestStart, bestLen};
}

static int[] countMinimalCovers(String s, String t) {
    int[] need = new int[128];
    int missing = 0;
    for (char c : t.toCharArray()) { if (need[c]++ == 0) missing++; }
    int[] have = new int[128];
    int left = 0, shortest = Integer.MAX_VALUE, howMany = 0, first = -1;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        have[c]++;
        if (need[c] > 0 && have[c] == need[c]) missing--;
        while (missing == 0) {
            int len = right - left + 1;
            if (len < shortest) { shortest = len; howMany = 1; first = left; }
            else if (len == shortest) howMany++;
            char drop = s.charAt(left++);
            have[drop]--;
            if (need[drop] > 0 && have[drop] < need[drop]) missing++;
        }
    }
    return howMany == 0 ? new int[] {0, -1} : new int[] {howMany, first};
}
```

The first method does a fixed number of table updates per bead, so it runs in O(n) time with 26 counters. The repeat-free and cover methods move each end at most once per bead, which is again linear in n. The repaint method rescans 26 counters per check, so it is O(26 n) rather than O(n), and the cover method may record several covers at one right end, each strictly shorter than the one before, so the strict and the equal comparisons together count every shortest start once.

<!-- stage: applicability -->
### Reading A Stretch Through Its Counts

Whenever a question about a contiguous stretch turns out to depend on how many times each symbol occurs inside it, build the pair of range and table. Write the invariant first, in words, covering both halves: which positions are active, and what each stored number counts. The counter of agreeing or missing letters is then a derived quantity, and it must be updated around every change of a count, before and after, never from a fresh scan.

The nearest false friend is a plain set of seen symbols, which forgets how many times each appeared and so cannot tell a rearrangement from a stretch that merely uses the right letters. Another is the sorted copy of every stretch, which looks like a count comparison and costs a sort per position. A third is the hash map of counts compared with `equals` on every step, correct but linear in the alphabet per step.

In Java, use `int[26]` or `int[128]` only when the problem promises that alphabet, and `HashMap` otherwise. Compare two counts with `==` on primitives, and watch the boxed `Integer` trap if a map is used. Build answers from indices and print a substring once at the end, never inside the loop. For several matching windows decide whether ties go to the leftmost start, and make the strict inequality in the update say so.

<!-- stage: exercises -->
### Exercises

#### [Build] Permutation in String (LeetCode 567)
<!-- id: sw-permutation-start-index -->

**Prerequisites.** Sliding windows from this chapter, and frequency counts from Chapter 04.

**Problem.** Given a text and an order of lowercase letters, return the starting index of the first window of the text that is a rearrangement of the order, or minus one if there is none. Keep one table of counts and a counter of letters whose counts agree, so every slide does a fixed amount of work. Do not build substrings and do not modify the inputs.

**Constraints.** 1 <= order.length() <= 100000, 0 <= text.length() <= 100000, lowercase letters only. When the order is longer than the text, the answer is minus one, and each slide may touch only two letters.

**Example 1.** Input `text = "bcxabdcab", order = "abc"`, output 6.

**Example 2.** Input `text = "ab", order = "abc"`, output -1.

**Hint.** What changes in the agreement count when a letter is added, and what when one is removed? Why is it enough to look at those two letters?

**Changed decision.** The classic question asks only whether a match exists. Here the first index is returned, and the counter replaces the comparison of whole tables, with the constant work per slide checked.

#### [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-longest-leftmost-repeat-free -->

**Prerequisites.** The exercise above.

**Problem.** For a string of ASCII characters, return `[start, length, shrinkSteps]` for the leftmost longest stretch in which no character occurs twice, where `shrinkSteps` is the total number of times the left end moved. Use counts and shrink while the entering character occurs more than once.

**Constraints.** 0 <= s.length() <= 100000, characters with codes 0 to 127. The empty string gives `[0, 0, 0]`, and the left end never moves backwards.

**Example 1.** Input `s = "tmmzuxt"`, output `[2, 5, 2]`.

**Example 2.** Input `s = "aaaa"`, output `[0, 1, 3]`.

**Hint.** When two stretches of the same length are found, which one should replace the record? Does the shrink count depend on which one wins?

**Changed decision.** The length alone is no longer enough. The answer names where the stretch starts, ties keep the earlier one, and the number of left moves is reported as evidence of linear work.

#### [Boundary] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-exact-max-repaint-window -->

**Prerequisites.** The two exercises above.

**Problem.** For a string of capital letters and a budget k, return `[start, length]` of the leftmost longest stretch that can be made into one letter with at most k replacements. Recompute the largest count exactly over all 26 counters whenever it is needed, and shrink until the stretch fits the budget.

**Constraints.** 0 <= s.length() <= 100000, letters A to Z only, 0 <= k <= 100000. The budget may be larger than the string, and the stretch must be valid whenever it is recorded.

**Example 1.** Input `s = "ABBBACDDE", k = 1`, output `[0, 4]`.

**Example 2.** Input `s = "XYZ", k = 0`, output `[0, 1]`.

**Hint.** Why is it safe to call the stretch valid only after the shrink loop? What does the largest count have to be taken over?

**Changed decision.** The earlier versions of this problem report one length. This one returns a stretch, so the largest count must describe the current range exactly at every step.

#### [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-count-minimal-covers -->

**Prerequisites.** All three exercises above.

**Problem.** Given a string s and a string t of ASCII characters, where t may repeat characters, return `[howMany, firstStart]`, where howMany is the number of different start positions of covering stretches of the shortest possible length and firstStart is the smallest such start. A stretch covers t when it holds each character at least as often as t does. Return `[0, -1]` if none exists. Never construct a substring.

**Constraints.** 0 <= s.length() <= 100000, 1 <= t.length() <= 100000, characters 0 to 127. When t is longer than s, the answer is `[0, -1]`.

**Example 1.** Input `s = "xabxbaxab", t = "ab"`, output `[3, 1]`.

**Example 2.** Input `s = "zzz", t = "zz"`, output `[2, 0]`.

**Hint.** After the shrink loop stops, which stretch ending at the current right end is the shortest cover? How can two covers of the shortest length share a start?

**Changed decision.** The classic answer is one string. Here the answer counts distinct shortest starts and reports the leftmost, so every cover found by the loop must be compared with the best length without being copied.
