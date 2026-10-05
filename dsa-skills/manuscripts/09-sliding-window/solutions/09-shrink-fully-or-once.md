<!-- solutions-for: 09-sliding-window -->
### Solutions For Choosing The Shrink Policy

#### Solution: [Build] Restore Before Record (Author exercise)
<!-- id: sw-restore-before-record -->

**Approach.**
The window keeps a count per ASCII code. After the entering character raises its count, a `while` loop removes characters from the left until that count is 1 again. Only the entering character can have a count above 1, because the window was valid before it entered. After the loop, the method checks that every count is at most 1 and then measures the window. The method records a window only when its length is strictly larger than the best, so the leftmost start wins ties. The invariant is that every count is at most 1 at the moment of measuring.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once, and the validity check in the assertion is for testing only and is not part of the algorithm.
- **Space** is O(1), because the count array has 128 entries.

```java run
import java.util.Random;

public final class RestoreBeforeRecord {
    /**
     * Returns {start, length} of the leftmost longest substring with no repeated character.
     * Time: O(n), each index enters once and leaves at most once.
     * Space: O(1), a count array of 128 entries.
     * Invariant: at the moment of measuring, every entry of cnt is at most 1.
     */
    static int[] longest(String s) {
        int[] cnt = new int[128];
        int left = 0, bestStart = 0, bestLength = 0;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            cnt[c]++;
            // Restore: runs while the entering character is repeated; each pass removes the value at left.
            while (cnt[c] > 1) {
                cnt[s.charAt(left)]--;
                left++;
            }
            // The assertion states the invariant; it scans 128 entries and belongs to testing only.
            assert valid(cnt) : "window must be valid before measuring";
            // Strict comparison keeps the leftmost start on ties.
            if (right - left + 1 > bestLength) { bestLength = right - left + 1; bestStart = left; }
        }
        // The empty string never enters the loop and returns {0, 0}.
        return new int[] {bestStart, bestLength};
    }

    /** True when every count is at most 1. */
    static boolean valid(int[] cnt) {
        for (int c : cnt) if (c > 1) return false;
        return true;
    }

    /** Oracle: tests every substring in order of start. */
    static int[] oracle(String s) {
        int bs = 0, bl = 0;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            boolean ok = true;
            for (int x = i; x <= j; x++) for (int y = x + 1; y <= j; y++) if (s.charAt(x) == s.charAt(y)) ok = false;
            if (ok && j - i + 1 > bl) { bl = j - i + 1; bs = i; }
        }
        return new int[] {bs, bl};
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement, plus the empty string.
        if (!java.util.Arrays.equals(longest("abcdbea"), new int[] {2, 5})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(longest("bbbbb"), new int[] {0, 1})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(longest(""), new int[] {0, 0})) throw new AssertionError("empty");
        // Random strings agree with the oracle.
        Random rnd = new Random(81);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(14); i < n; i++) sb.append((char) ('a' + rnd.nextInt(5)));
            if (!java.util.Arrays.equals(longest(sb.toString()), oracle(sb.toString()))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] One-Removal Maximum-Length Trace (Author exercise)
<!-- id: sw-one-removal-trace -->

**Approach.**
The method runs the one removal form with `peak`, the largest count seen. After each step it measures the exact dominant count of the current window with a scan of 26 counts, and it counts the steps where the length minus that count exceeds `k`. The scan belongs to the measurement and not to the algorithm under study. The window length never decreases, because each step either grows the window or slides it by one. The final length is `s.length() - left`. The invariant allows an invalid window: after each step, the window length still equals the best valid length of the prefix.

**Complexity.**
- **Time** is O(26 * n) for this exercise, because the measurement scans 26 counts per step; the one removal form alone is O(n).
- **Space** is O(1), because the count array has 26 entries.

```java run
import java.util.Random;

public final class OneRemovalTrace {
    /**
     * Returns {final window length, number of steps after which the window is invalid}.
     * Time: O(26 * n), a constant-size scan per step for the measurement.
     * Space: O(1), a count array of 26 entries.
     * Invariant: after each step, the window length equals the best valid length of the prefix.
     */
    static int[] run(String s, int k) {
        int[] cnt = new int[26];
        int left = 0, peak = 0, invalid = 0;
        // Expand: the letter at right enters.
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'A';
            cnt[c]++;
            // peak only rises, so it can be larger than the exact dominant count of the window.
            peak = Math.max(peak, cnt[c]);
            // One removal: at most one value leaves per step, so the length never shrinks.
            if (right - left + 1 - peak > k) {
                cnt[s.charAt(left) - 'A']--;
                left++;
            }
            // Measurement only: the exact dominant count of the current window.
            int exact = 0;
            for (int x : cnt) exact = Math.max(exact, x);
            // A window whose exact cost exceeds k is invalid, although its length is a correct candidate.
            if (right - left + 1 - exact > k) invalid++;
        }
        // The window length at the end equals the answer.
        return new int[] {s.length() - left, invalid};
    }

    /** Oracle: full shrink with an exact dominant count, returning the answer only. */
    static int answer(String s, int k) {
        int[] cnt = new int[26];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            cnt[s.charAt(right) - 'A']++;
            while (true) {
                int top = 0;
                for (int x : cnt) top = Math.max(top, x);
                if (right - left + 1 - top <= k) break;
                cnt[s.charAt(left) - 'A']--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (!java.util.Arrays.equals(run("AAABCD", 1), new int[] {4, 2})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(run("ABAB", 2), new int[] {4, 0})) throw new AssertionError("example 2");
        // The final length equals the full-shrink answer on random strings, so the one removal form is safe here.
        Random rnd = new Random(82);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(14); i < n; i++) sb.append((char) ('A' + rnd.nextInt(3)));
            int k = rnd.nextInt(sb.length() + 1);
            if (run(sb.toString(), k)[0] != answer(sb.toString(), k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Multiple Left Removals Needed (Author exercise)
<!-- id: sw-multiple-removals -->

**Approach.**
The faulty scan removes one character per `right` when the entering character is repeated. In `abcdbea`, the second `b` enters while the window is `abcd`. One removal drops `a`, and the window `bcdb` still holds both copies of `b`. The scan has not restored validity, and it records the length of an invalid window. The method returns that recorded length, which is larger than the true answer on this input. The true scan needs two removals at that step, so a `while` loop is required. The invariant of the faulty scan is broken, because its window is not duplicate-free.

**Complexity.**
- **Time** is O(n), because each step does a constant amount of work.
- **Space** is O(1), because the count array has 26 entries.

```java run
import java.util.Random;

public final class MultipleRemovals {
    /**
     * Returns the best length that the one-removal duplicate-free scan reports.
     * Time: O(n), constant work per step.
     * Space: O(1), a count array of 26 entries.
     * Invariant: none; the window may keep a repeated character, which is the defect under study.
     */
    static int faulty(String s) {
        int[] cnt = new int[26];
        int left = 0, best = 0;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'a';
            cnt[c]++;
            // One removal: an if repairs at most one repeat position.
            if (cnt[c] > 1) {
                cnt[s.charAt(left) - 'a']--;
                left++;
            }
            // The scan records the length even when a repeat remains inside.
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    /** The correct scan with a while loop. */
    static int correct(String s) {
        int[] cnt = new int[26];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'a';
            cnt[c]++;
            // Full shrink: removes values until the entering character is unique.
            while (cnt[c] > 1) { cnt[s.charAt(left) - 'a']--; left++; }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: the faulty scan reports 6, the correct answer is 5.
        if (faulty("abcdbea") != 6 || correct("abcdbea") != 5) throw new AssertionError("example 1");
        // Example 2: both scans agree on abcabc, where one removal suffices at every step.
        if (faulty("abcabc") != 3 || correct("abcabc") != 3) throw new AssertionError("example 2");
        // The faulty scan never reports less than the correct one, and it differs on some inputs.
        Random rnd = new Random(83);
        boolean differs = false;
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(14); i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            int f = faulty(sb.toString()), c = correct(sb.toString());
            if (f < c) throw new AssertionError("faulty below correct at " + t);
            if (f != c) differs = true;
        }
        if (!differs) throw new AssertionError("no input exposed the defect");
    }
}
```

#### Solution: [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-wide-replacement -->

**Approach.**
The alphabet has 65,536 symbols, so a scan of the counts costs too much. The method keeps `peak`, the largest count seen in any step, and slides without shrinking fully. When the length minus `peak` exceeds `k`, one character leaves and `left` moves by one. The window length never decreases. A longer answer needs a count above the old `peak`, and `peak` rises only when the entering character really reaches that count in the current window, so the length never exceeds a valid length. The method returns `s.length() - left`. The invariant stays the same as in the previous exercise, with the window length equal to the best valid length of the prefix.

**Complexity.**
- **Time** is O(n), because each step does a constant amount of work and the loop has no scan.
- **Space** is O(1), because the count array has 65,536 entries regardless of `n`.

```java run
import java.util.Random;

public final class WideReplacement {
    /**
     * Returns the longest substring that becomes one repeated character after at most k replacements.
     * Time: O(n), constant work per step and no scan of the counts.
     * Space: O(1), a count array of 65,536 entries.
     * Invariant: after each step, the window length equals the best valid length of the prefix.
     */
    static int characterReplacement(String s, int k) {
        // One counter per 16-bit character code.
        int[] cnt = new int[65536];
        int left = 0, peak = 0;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            cnt[c]++;
            // peak is the largest count seen; it may be stale after removals, and that is safe here.
            peak = Math.max(peak, cnt[c]);
            // One removal: slide by one when the length would exceed peak + k.
            if (right - left + 1 - peak > k) {
                cnt[s.charAt(left)]--;
                left++;
            }
        }
        // The window length never decreased, so the final length is the answer.
        return s.length() - left;
    }

    /** Oracle: full shrink with an exact dominant count over a small alphabet. */
    static int oracle(String s, int k) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            int top = 0;
            for (int x = i; x <= j; x++) {
                int c = 0;
                for (int y = i; y <= j; y++) if (s.charAt(y) == s.charAt(x)) c++;
                top = Math.max(top, c);
            }
            if (j - i + 1 - top <= k) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (characterReplacement("AABABBA", 1) != 4) throw new AssertionError("example 1");
        if (characterReplacement("ABCDE", 0) != 1) throw new AssertionError("example 2");
        // A string with wide characters works with the same code.
        if (characterReplacement("中文中", 1) != 3) throw new AssertionError("wide characters");
        // Random strings over a mixed alphabet agree with the oracle.
        Random rnd = new Random(84);
        String alpha = "ab中￿";
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(13); i < n; i++) sb.append(alpha.charAt(rnd.nextInt(alpha.length())));
            int k = rnd.nextInt(sb.length() + 1);
            if (characterReplacement(sb.toString(), k) != oracle(sb.toString(), k)) throw new AssertionError("random " + t);
        }
    }
}
```
