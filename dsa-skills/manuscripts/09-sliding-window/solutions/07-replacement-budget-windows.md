<!-- solutions-for: 09-replacement-budget-windows -->
### Replacement-Budget Windows

#### Solution: [Build] Replacement Cost Of One Window (Author exercise)
<!-- id: sw-window-cost -->

**Approach.** Count the letters of `s[left..right]` in twenty-six counters, keep the largest counter, and return the stretch length minus it. Every letter other than the commonest one has to change, and the commonest one can stay, so nothing smaller is possible. The check compares with an oracle that sorts a copy of the stretch and measures its longest run of equal letters, and confirms that the input string is unchanged after the call.

**Complexity.** One scan of the stretch, so time proportional to its length, and a fixed array of 26 counters as extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class WindowCost {
    static int windowCost(String s, int left, int right) {
        int[] tally = new int[26];
        int top = 0;
        for (int i = left; i <= right; i++) top = Math.max(top, ++tally[s.charAt(i) - 'A']);
        return (right - left + 1) - top;
    }
    static int sortedRunOracle(String s, int left, int right) {
        char[] part = s.substring(left, right + 1).toCharArray();
        Arrays.sort(part);
        int run = 1, longest = 1;
        for (int i = 1; i < part.length; i++) {
            run = part[i] == part[i - 1] ? run + 1 : 1;
            longest = Math.max(longest, run);
        }
        return part.length - longest;
    }

    public static void main(String[] args) {
        if (windowCost("KKLMKLKN", 1, 5) != 3) throw new AssertionError("example 1");
        if (windowCost("ZZZZ", 0, 3) != 0) throw new AssertionError("example 2");
        if (windowCost("Q", 0, 0) != 0) throw new AssertionError("single letter");
        Random rnd = new Random(901);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            int alphabet = 1 + rnd.nextInt(5);
            for (int i = 0; i < n; i++) sb.append((char) ('A' + rnd.nextInt(alphabet)));
            String s = sb.toString();
            String copy = new String(s.toCharArray());
            for (int left = 0; left < n; left++) {
                for (int right = left; right < n; right++) {
                    if (windowCost(s, left, right) != sortedRunOracle(s, left, right)) throw new AssertionError("differs on " + s + " " + left + " " + right);
                }
            }
            if (!s.equals(copy)) throw new AssertionError("string changed");
        }
    }
}
```

#### Solution: [Vary] Longest Binary Uniform Window (Author exercise)
<!-- id: sw-binary-flips -->

**Approach.** Keep two counters, one for zeros and one for ones, and the record of the largest counter value seen. Each new entry raises its counter, and when the window width minus the record exceeds the flip budget, the left edge moves forward by one entry and the window slides at the same width. The answer is the number of entries minus the final left edge. The check compares with a brute force that tries every stretch and takes the smaller of its two counts as the cost, and confirms that the input array is unchanged.

**Complexity.** One pass, so O(n) time with two counters of extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BinaryFlips {
    static int longestFlippable(int[] bits, int flips) {
        int[] seen = new int[2];
        int record = 0, left = 0;
        for (int right = 0; right < bits.length; right++) {
            record = Math.max(record, ++seen[bits[right]]);
            if ((right - left + 1) - record > flips) seen[bits[left++]]--;
        }
        return bits.length - left;
    }
    static int brute(int[] bits, int flips) {
        int best = 0;
        for (int i = 0; i < bits.length; i++) {
            int zeros = 0, ones = 0;
            for (int j = i; j < bits.length; j++) {
                if (bits[j] == 0) zeros++; else ones++;
                if (Math.min(zeros, ones) <= flips) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestFlippable(new int[] {1, 0, 0, 1, 0, 1, 1}, 1) != 4) throw new AssertionError("example 1");
        if (longestFlippable(new int[] {0, 1, 0, 1, 1, 1}, 0) != 3) throw new AssertionError("example 2");
        if (longestFlippable(new int[0], 0) != 0) throw new AssertionError("empty");
        if (longestFlippable(new int[] {1}, 0) != 1) throw new AssertionError("one entry");
        int[] all = new int[40];
        if (longestFlippable(all, 0) != 40) throw new AssertionError("all equal");
        Random rnd = new Random(902);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(16);
            int[] bits = new int[n];
            for (int i = 0; i < n; i++) bits[i] = rnd.nextInt(2);
            int[] copy = Arrays.copyOf(bits, n);
            for (int flips = 0; flips <= n; flips++) {
                if (longestFlippable(bits, flips) != brute(bits, flips)) throw new AssertionError("differs on " + Arrays.toString(bits) + " flips " + flips);
            }
            if (!Arrays.equals(bits, copy)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Boundary] Stale Maximum Trace (Author exercise)
<!-- id: sw-stale-maximum -->

**Approach.** Run the window with a record that is only ever raised. After each step the window width is the right edge minus the left edge plus one, and the true commonest count is recomputed from the counters purely for comparison, so the position is counted whenever the record is strictly larger. The reported length is the final width. The check asserts that the width never decreases, that the left edge moves at most one entry per step, that on every prefix of the string the length equals a brute-force best usable stretch, and that the stale count agrees with an independent recomputation that rescans each window.

**Complexity.** O(n) time for the window itself, plus a fixed 26-counter rescan per step used only for the comparison, so O(26 n) for the full instrumented run.

```java run
import java.util.Random;

public final class StaleMaximum {
    static boolean widthDropped;
    static boolean movedTwice;

    static int[] runWindow(String s, int k) {
        int[] tally = new int[26];
        int record = 0, left = 0, stale = 0, lastWidth = 0;
        for (int right = 0; right < s.length(); right++) {
            record = Math.max(record, ++tally[s.charAt(right) - 'A']);
            int before = left;
            if ((right - left + 1) - record > k) { tally[s.charAt(left) - 'A']--; left++; }
            if (left - before > 1) movedTwice = true;
            int width = right - left + 1;
            if (width < lastWidth) widthDropped = true;
            lastWidth = width;
            int truth = 0;
            for (int c : tally) truth = Math.max(truth, c);
            if (record > truth) stale++;
        }
        return new int[] {s.length() - left, stale};
    }
    static int bestStretch(String s, int k) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            for (int j = i; j < s.length(); j++) {
                int top = 0;
                for (int c = 'A'; c <= 'Z'; c++) {
                    int count = 0;
                    for (int x = i; x <= j; x++) if (s.charAt(x) == c) count++;
                    top = Math.max(top, count);
                }
                if ((j - i + 1) - top <= k) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }
    static int slowStale(String s, int k) {
        // independent replay: window edges recomputed from the rule, maximum recomputed from the record's definition
        int left = 0, record = 0, stale = 0;
        for (int right = 0; right < s.length(); right++) {
            int inWindow = 0;
            for (int x = left; x <= right; x++) if (s.charAt(x) == s.charAt(right)) inWindow++;
            record = Math.max(record, inWindow);
            if ((right - left + 1) - record > k) left++;
            int truth = 0;
            for (int x = left; x <= right; x++) {
                int count = 0;
                for (int y = left; y <= right; y++) if (s.charAt(y) == s.charAt(x)) count++;
                truth = Math.max(truth, count);
            }
            if (record > truth) stale++;
        }
        return stale;
    }

    public static void main(String[] args) {
        int[] one = runWindow("MMMNOPQ", 1);
        if (one[0] != 4 || one[1] != 3) throw new AssertionError("example 1 " + one[0] + " " + one[1]);
        int[] two = runWindow("ABCD", 0);
        if (two[0] != 1 || two[1] != 0) throw new AssertionError("example 2");
        int[] none = runWindow("", 0);
        if (none[0] != 0 || none[1] != 0) throw new AssertionError("empty");
        Random rnd = new Random(903);
        boolean sawStale = false;
        for (int t = 0; t < 2500; t++) {
            int n = rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            int alphabet = 1 + rnd.nextInt(4);
            for (int i = 0; i < n; i++) sb.append((char) ('A' + rnd.nextInt(alphabet)));
            String s = sb.toString();
            int k = rnd.nextInt(n + 1);
            widthDropped = false;
            movedTwice = false;
            int[] got = runWindow(s, k);
            if (widthDropped) throw new AssertionError("width shrank on " + s);
            if (movedTwice) throw new AssertionError("left moved twice on " + s);
            if (got[0] != bestStretch(s, k)) throw new AssertionError("length differs on " + s + " k " + k);
            for (int cut = 0; cut <= n; cut++) {
                String prefix = s.substring(0, cut);
                if (runWindow(prefix, k)[0] != bestStretch(prefix, k)) throw new AssertionError("prefix differs on " + prefix);
            }
            if (got[1] != slowStale(s, k)) throw new AssertionError("stale count differs on " + s);
            if (got[1] > 0) sawStale = true;
        }
        if (!sawStale) throw new AssertionError("never saw a stale record");
    }
}
```

#### Solution: [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-char-replacement -->

**Approach.** A window is usable when its width minus its commonest letter count is at most `k`. Slide a window along the string with the record of the largest count seen, never lowering it, and use an `if` so that an unusable window slides at the same width instead of shrinking. The answer is the number of characters minus the final left edge. The check compares with a shrinking version that keeps the exact maximum, with a brute force over all stretches, counts the tally updates to show that each character is added once and removed at most once, and confirms that the index arithmetic `ch - 'A'` produces an `int`.

**Complexity.** O(n) time for the window, with 26 counters of extra space. The test asserts at most 2n counter updates in total.

```java run
import java.util.Random;

public final class CharReplacement {
    static int updates;

    static int slidingFixed(String s, int k) {
        int[] tally = new int[26];
        int record = 0, left = 0;
        for (int right = 0; right < s.length(); right++) {
            updates++;
            int now = ++tally[s.charAt(right) - 'A'];
            record = Math.max(record, now);
            if ((right - left + 1) - record > k) {
                updates++;
                tally[s.charAt(left) - 'A']--;
                left++;
            }
        }
        return s.length() - left;
    }
    static int shrinkingExact(String s, int k) {
        int[] tally = new int[26];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            tally[s.charAt(right) - 'A']++;
            while (true) {
                int top = 0;
                for (int c : tally) top = Math.max(top, c);
                if ((right - left + 1) - top <= k) break;
                tally[s.charAt(left) - 'A']--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }
    static int brute(String s, int k) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            for (int j = i; j < s.length(); j++) {
                int top = 0;
                for (int x = i; x <= j; x++) {
                    int count = 0;
                    for (int y = i; y <= j; y++) if (s.charAt(y) == s.charAt(x)) count++;
                    top = Math.max(top, count);
                }
                if ((j - i + 1) - top <= k) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (slidingFixed("PQQPRPPS", 2) != 5) throw new AssertionError("example 1");
        if (slidingFixed("XYZ", 0) != 1) throw new AssertionError("example 2");
        if (slidingFixed("", 3) != 0) throw new AssertionError("empty");
        if (slidingFixed("W", 0) != 1) throw new AssertionError("one letter");
        if (slidingFixed("RRRRR", 0) != 5) throw new AssertionError("all equal");
        if (slidingFixed("ABCDE", 5) != 5) throw new AssertionError("budget covers all");
        Object index = 'B' - 'A';
        if (!(index instanceof Integer)) throw new AssertionError("char arithmetic is not int");
        Random rnd = new Random(904);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            StringBuilder sb = new StringBuilder();
            int alphabet = 1 + rnd.nextInt(4);
            for (int i = 0; i < n; i++) sb.append((char) ('A' + rnd.nextInt(alphabet)));
            String s = sb.toString();
            for (int k = 0; k <= n; k++) {
                updates = 0;
                int fixed = slidingFixed(s, k);
                if (updates > 2 * n) throw new AssertionError("too many updates " + updates);
                if (fixed != shrinkingExact(s, k)) throw new AssertionError("shrinking form differs on " + s + " k " + k);
                if (fixed != brute(s, k)) throw new AssertionError("brute force differs on " + s + " k " + k);
            }
        }
    }
}
```
