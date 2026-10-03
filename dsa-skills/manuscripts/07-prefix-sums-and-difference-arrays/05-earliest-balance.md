<!-- lesson-kind: standard -->
<!-- lesson-id: earliest-balance -->
## Earliest Balance

<!-- stage: context -->
### A Hiker's Trail Log

A hiker wears a small device that records one reading per minute: it writes a plus one when the trail went up during that minute, and a minus one when it went down. Back at the lodge, she wants to know the longest stretch of the walk that began and ended at exactly the same height, so that the morning and the afternoon of that stretch cancelled out. The stretch can be anywhere in the walk, and it must be continuous.

The log has several hours of readings, one per minute, and she has several logs from different trips to compare. She does not need to know where the stretch was, only how many minutes long the longest such stretch lasted.

<!-- stage: naive -->
### Try Every Start And End

The direct approach is to take each starting minute, follow the walk forward minute by minute, and note the length whenever the height comes back to the starting height.

```java
static int longestLevelStretch(int[] steps) {
    int best = 0;
    for (int start = 0; start < steps.length; start++) {
        int height = 0;
        for (int end = start; end < steps.length; end++) {
            height += steps[end];
            if (height == 0) best = Math.max(best, end - start + 1);
        }
    }
    return best;
}
```

It finds the longest stretch for any sequence of steps, because it examines every start and every end.

<!-- stage: bottleneck -->
### Quadratic Work To Compare Heights

The two loops visit about n squared over two pairs of minutes, so the cost is O(n^2), and a log of a hundred thousand minutes means five billion comparisons. The inner loop also recomputes the height from the start for each beginning, although the heights at every minute of the whole walk were already available from one earlier pass.

A stretch is level exactly when the height at its end equals the height at its start. So the longest level stretch is the largest gap between two minutes that share a height. For one end minute, the best partner is the earliest minute with that height, since an earlier start makes a longer stretch. Looking up a height in a table takes O(1) expected time, so one pass with a table can answer for every end minute, in O(n) in total.

<!-- stage: insight -->
### Remember Only The First Time

Walking along the log, keep the running height, which this lesson calls the **balance**. When the balance at some minute matches a balance seen before, everything between the two minutes sums to zero, and the distance between the minutes is the length of a level stretch. To get the longest one for the current minute, the partner has to be the **earliest index** at which this balance occurred. A table that maps each balance to its first occurrence supplies that, and it must never be overwritten: when a balance appears again, the table keeps the old position, and only the distance is computed.

The table needs one entry before the walk begins. A stretch that starts at the very first minute pairs the current balance with the moment before the walk, when the balance was zero, and that moment sits one position before index zero. Call it the **virtual start**: the table is initialized with balance zero mapped to index minus one. Without it, a level stretch that begins at the first minute can never be found, because no recorded position precedes it.

<!-- names: balance, earliest index, virtual start -->

This differs from the counting pattern of the previous lesson in what the table remembers. A count answers how many stretches exist, and needs every occurrence. The longest stretch needs only the first occurrence, and keeping later occurrences would give shorter answers. The invariant is that, for every balance that has appeared, the table holds the smallest index at which it appeared, with the virtual start at minus one for zero.

<!-- stage: variables -->
### Height, First Positions And Best Length

`balance` is the running height after the current minute. `first` is the table from a balance to the earliest index at which it was reached, and it starts as `{0: -1}`. `best` is the longest level stretch found so far, starting at zero. For each index `i`, either the balance is already in `first`, and the candidate length is `i - first.get(balance)`, or it is new and gets recorded at `i`. The length is an index difference, which is why the virtual start sits at minus one: the stretch from index zero to `i` has `i + 1` minutes, which is `i - (-1)`.

<!-- stage: trace -->
### Heights Seen For The First Time

The first trace follows the log 0, 1, 0, 0, 1, 1, 0 for a walk where a zero stands for a descent and a one for a climb, so the steps are minus one, plus one, minus one, minus one, plus one, plus one, minus one. The step to study is the sixth: the height is zero again, the table says zero was first reached before the walk began, at minus one, and the level stretch has length 6, the longest so far.

```trace
{"cells":["0","1","0","0","1","1","0"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"balance":-1,"best":0},"note":"The balance -1 is new, so record index 0 as its first position. The best stays 0."},{"at":{"i":1},"vars":{"balance":0,"earliest":-1,"length":2,"best":2},"note":"The balance is 0, first reached at index -1, so the stretch has length 2 and the best is 2."},{"at":{"i":2},"vars":{"balance":-1,"earliest":0,"length":2,"best":2},"note":"The balance is -1, first reached at index 0, so the stretch has length 2 and the best is 2."},{"at":{"i":3},"vars":{"balance":-2,"best":2},"note":"The balance -2 is new, so record index 3 as its first position. The best stays 2."},{"at":{"i":4},"vars":{"balance":-1,"earliest":0,"length":4,"best":4},"note":"The balance is -1, first reached at index 0, so the stretch has length 4 and the best is 4."},{"at":{"i":5},"vars":{"balance":0,"earliest":-1,"length":6,"best":6},"note":"The balance is 0, first reached at index -1, so the stretch has length 6 and the best is 6."},{"at":{"i":6},"vars":{"balance":-1,"earliest":0,"length":6,"best":6},"note":"The balance is -1, first reached at index 0, so the stretch has length 6 and the best is 6."}]}
```

The second trace counts the letters A and B in the text ABxxBAxA, where A adds one, B subtracts one, and any other letter changes nothing. Letters that change nothing repeat the balance, which is allowed, since they sit inside a stretch without changing the totals. The step to study is the fourth: the balance is zero, which is already in the table at minus one, and the stretch of four letters holds one A and one B, with two neutral letters between them.

```trace
{"cells":["A","B","x","x","B","A","x","A"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"balance":1,"best":0},"note":"The balance 1 is new, so record index 0 as its first position. The best stays 0."},{"at":{"i":1},"vars":{"balance":0,"earliest":-1,"length":2,"best":2},"note":"The balance is 0, first reached at index -1, so the stretch has length 2 and the best is 2."},{"at":{"i":2},"vars":{"balance":0,"earliest":-1,"length":3,"best":3},"note":"The balance is 0, first reached at index -1, so the stretch has length 3 and the best is 3."},{"at":{"i":3},"vars":{"balance":0,"earliest":-1,"length":4,"best":4},"note":"The balance is 0, first reached at index -1, so the stretch has length 4 and the best is 4."},{"at":{"i":4},"vars":{"balance":-1,"best":4},"note":"The balance -1 is new, so record index 4 as its first position. The best stays 4."},{"at":{"i":5},"vars":{"balance":0,"earliest":-1,"length":6,"best":6},"note":"The balance is 0, first reached at index -1, so the stretch has length 6 and the best is 6."},{"at":{"i":6},"vars":{"balance":0,"earliest":-1,"length":7,"best":7},"note":"The balance is 0, first reached at index -1, so the stretch has length 7 and the best is 7."},{"at":{"i":7},"vars":{"balance":1,"earliest":0,"length":7,"best":7},"note":"The balance is 1, first reached at index 0, so the stretch has length 7 and the best is 7."}]}
```

<!-- stage: code -->
### One Pass With First Positions

```java
static int findMaxLength(int[] nums) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);
    int balance = 0, best = 0;
    for (int i = 0; i < nums.length; i++) {
        balance += nums[i] == 1 ? 1 : -1;
        Integer earlier = first.get(balance);
        if (earlier == null) first.put(balance, i);
        else best = Math.max(best, i - earlier);
    }
    return best;
}

static int longestEqualAB(String s) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);
    int balance = 0, best = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == 'A') balance++;
        else if (c == 'B') balance--;
        Integer earlier = first.get(balance);
        if (earlier == null) first.put(balance, i);
        else best = Math.max(best, i - earlier);
    }
    return best;
}

static int longestEvenVowels(String s) {
    int[] firstSeen = new int[32];
    java.util.Arrays.fill(firstSeen, -2);
    firstSeen[0] = -1;
    int mask = 0, best = 0;
    for (int i = 0; i < s.length(); i++) {
        int bit = "aeiou".indexOf(s.charAt(i));
        if (bit >= 0) mask ^= 1 << bit;
        if (firstSeen[mask] == -2) firstSeen[mask] = i;
        else best = Math.max(best, i - firstSeen[mask]);
    }
    return best;
}
```

Each function makes one pass with O(1) expected work per element, and its space is proportional to the number of distinct balances, at most 32 masks in the vowel version. The table is read with a nullable `Integer`, so a missing balance is distinguished from index zero.

<!-- stage: applicability -->
### When The Longest Level Stretch Matters

Use this when a question asks for the longest or the shortest stretch in which two quantities are equal, or in which a signed total returns to a value it had before. Translate the equality into a balance by adding one for the first quantity, subtracting one for the second, and adding nothing for anything else. The invariant is that each balance is stored once, at its first index, and that the table starts with zero at minus one.

A false friend is the frequency table from the last lesson, which counts stretches and has no use for lengths. Another is the table that is overwritten on every visit, which stores the latest index and produces the shortest stretch for each balance instead of the longest. A third is a table with no entry for the start: the first minutes of the walk are then excluded from every answer.

In Java, store indices in a `Map<Integer, Integer>` and read with `get` into an `Integer`, or use `containsKey`, so that a missing entry is not confused with index zero, and so that the stored minus one is not mistaken for a missing entry. When the state is a small set of switches, a bitmask in a short array is both simpler and faster than a map. Use `Math.max` for the longest and `Math.min` for the shortest.

<!-- stage: exercises -->
### Exercises

#### [Build] Contiguous Array (LeetCode 525)
<!-- id: ps-contiguous-array -->

**Prerequisites.** The prefix counts lesson, and the balance idea from this lesson.

**Problem.** Given an array of zeros and ones, return the length of the longest contiguous stretch that contains the same number of zeros and ones. Treat each zero as minus one, keep a table of the earliest index of each balance, and return zero if no stretch qualifies.

**Constraints.** 1 <= nums.length <= 100000 and each `nums[i]` is 0 or 1.

**Example 1.** Input `nums = [0, 1, 0, 0, 1, 1, 0]`, output 6.

**Example 2.** Input `nums = [1, 1, 1, 0]`, output 2.

**Hint.** What is the balance after a stretch with equal zeros and ones? Which earlier occurrence of a balance gives the longest stretch?

**Changed decision.** First rung: the table keeps the first index of a balance, and a repeat is used to measure a length, not stored.

#### [Vary] Equal A And B (Author exercise)
<!-- id: ps-equal-a-and-b -->

**Prerequisites.** The Contiguous Array exercise above.

**Problem.** Given a string, return the length of the longest contiguous stretch with the same number of letters `A` and letters `B`, where all other characters are allowed anywhere in the stretch. Add one for `A`, subtract one for `B`, and add nothing for other characters.

**Constraints.** 0 <= s.length() <= 100000 and the characters are any ASCII letters.

**Example 1.** Input `s = "ABxxBAxA"`, output 7.

**Example 2.** Input `s = "xyz"`, output 3.

**Hint.** What happens to the balance on a neutral character? What does an empty stretch of letters mean for the answer?

**Changed decision.** A third kind of step, a neutral one, leaves the balance unchanged, so repeated balances now occur on consecutive indices.

#### [Boundary] Prefix From Zero (Author exercise)
<!-- id: ps-prefix-from-zero -->

**Prerequisites.** The two exercises above.

**Problem.** Solve the zeros-and-ones problem again, concentrating on stretches that begin at index zero. Show that a table without the virtual start gives a wrong answer for such inputs, and that initializing balance zero at index minus one fixes it.

**Constraints.** 1 <= nums.length <= 100000 and each `nums[i]` is 0 or 1.

**Example 1.** Input `nums = [1, 0, 1, 0, 0, 0]`, output 4.

**Example 2.** Input `nums = [1, 1, 0, 0]`, output 4.

**Hint.** Which index should stand for the moment before the first value? What does the unseeded version return for the first example?

**Changed decision.** The virtual start is the point of the exercise, so the table begins with zero mapped to minus one.

#### [Recognize] Find the Longest Substring Containing Vowels in Even Counts (LeetCode 1371)
<!-- id: ps-even-vowels -->

**Prerequisites.** All three exercises above, and bit operations from Chapter 00.

**Problem.** Given a string of lowercase letters, return the length of the longest substring in which each of the vowels a, e, i, o and u appears an even number of times, possibly zero. The state that repeats is not a number but a mask of five parity bits, one per vowel, and two equal masks enclose a stretch of even counts.

**Constraints.** 1 <= s.length() <= 100000 and the string uses lowercase letters only.

**Example 1.** Input `s = "eleetminicoworoep"`, output 13.

**Example 2.** Input `s = "aeiou"`, output 0.

**Hint.** What does flipping a bit do each time a vowel appears? What must be equal at the two ends of a valid substring?

**Changed decision.** The balance is a five-bit parity mask, so the table maps a mask to its first index, and the repeat rule is unchanged.
