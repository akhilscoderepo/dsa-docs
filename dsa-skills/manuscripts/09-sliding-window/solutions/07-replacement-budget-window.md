<!-- solutions-for: 09-sliding-window -->
### Solutions For Replacement Budget Windows

#### Solution: [Build] Replacement Cost Of One Window (Author exercise)
<!-- id: sw-window-cost -->

**Approach.**
The window `s[l..r]` has fixed boundaries, so the method counts its letters in one pass and reads the largest count. The replacement cost is the length minus that count. Keeping the most frequent letter and overwriting every other character is the cheapest way to make the window uniform, because each overwritten character costs one. The invariant is that, after the pass, `cnt` holds the letter counts of exactly `s[l..r]`.

**Complexity.**
- **Time** is O(r - l + 26), because one pass counts the window and one scan reads the 26 counts.
- **Space** is O(1), because the count array has 26 entries.

```java run
import java.util.Random;

public final class WindowCost {
    /**
     * Returns the replacement cost of s[l..r]: its length minus its dominant count.
     * Time: O(r - l + 26), one counting pass and one scan of the counts.
     * Space: O(1), a count array of 26 entries.
     * Invariant: cnt holds the letter counts of s[l..r] after the loop.
     */
    static int cost(String s, int l, int r) {
        int[] cnt = new int[26];
        // The loop reads each index of the window once.
        for (int i = l; i <= r; i++) cnt[s.charAt(i) - 'a']++;
        // The dominant count is the largest entry.
        int top = 0;
        for (int c : cnt) top = Math.max(top, c);
        // Overwrite every other character, so the cost is length minus the dominant count.
        return (r - l + 1) - top;
    }

    /** Oracle: tries each target letter and counts mismatches. */
    static int oracle(String s, int l, int r) {
        int best = Integer.MAX_VALUE;
        for (char t = 'a'; t <= 'z'; t++) {
            int mismatches = 0;
            for (int i = l; i <= r; i++) if (s.charAt(i) != t) mismatches++;
            best = Math.min(best, mismatches);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (cost("aabbbcc", 1, 5) != 2) throw new AssertionError("example 1");
        if (cost("aabbbcc", 2, 4) != 0) throw new AssertionError("example 2");
        // Random strings and windows agree with the oracle.
        Random rnd = new Random(61);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(12); i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            String s = sb.toString();
            int l = rnd.nextInt(s.length()), r = l + rnd.nextInt(s.length() - l);
            if (cost(s, l, r) != oracle(s, l, r)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Longest Binary Uniform Window (Author exercise)
<!-- id: sw-binary-uniform -->

**Approach.**
The alphabet has two values, so the window keeps two counts. The dominant count is the larger of the two, and the cost is the length minus that larger count. The shrink loop runs while the cost exceeds `k`, and the method records the length afterwards. Flipping the minority value to the majority value costs one flip per minority value, so the cost is the number of flips. The invariant: once the loop ends, the window needs at most `k` flips to become uniform.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once, and the dominant count costs O(1).
- **Space** is O(1), because the method keeps two counts and three integers.

```java run
import java.util.Random;

public final class BinaryUniform {
    /**
     * Returns the longest block that becomes uniform after at most k flips.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), two counters.
     * Invariant: after the shrink loop, the window length minus max(zeros, ones) is at most k.
     */
    static int longest(int[] bits, int k) {
        // cnt[0] counts zeros and cnt[1] counts ones inside the window.
        int[] cnt = new int[2];
        int left = 0, best = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < bits.length; right++) {
            cnt[bits[right]]++;
            // Shrink: runs while the flips needed exceed k; each pass removes one index.
            while (right - left + 1 - Math.max(cnt[0], cnt[1]) > k) {
                cnt[bits[left]]--;
                left++;
            }
            // The window is valid, so its length is a candidate.
            best = Math.max(best, right - left + 1);
        }
        // The longest valid length.
        return best;
    }

    /** Oracle: tests every block with both targets. */
    static int oracle(int[] a, int k) {
        int best = 0;
        for (int i = 0; i < a.length; i++) for (int j = i; j < a.length; j++) {
            int ones = 0;
            for (int x = i; x <= j; x++) ones += a[x];
            int zeros = j - i + 1 - ones;
            if (Math.min(ones, zeros) <= k) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (longest(new int[] {1, 1, 0, 0, 1, 0, 0, 0, 1, 0}, 2) != 8) throw new AssertionError("example 1");
        if (longest(new int[] {1, 0, 1, 0}, 1) != 3) throw new AssertionError("example 2");
        // Random arrays and budgets agree with the oracle.
        Random rnd = new Random(62);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(2);
            int k = rnd.nextInt(a.length + 1);
            if (longest(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Stale Maximum Trace (Author exercise)
<!-- id: sw-stale-maximum -->

**Approach.**
The method runs the exact scan of the lesson. After the shrink loop at each `r`, it computes `exact` by scanning the 26 counts and keeps `seen`, the largest `exact` so far. It counts the indexes where `seen > exact`. Such indexes exist, because the dominant character can leave the window while the shrink loop repairs a violation. At those indexes, a program that remembered `seen` would use a value larger than the truth for the current window. The invariant is that `seen` is the maximum of the exact dominant counts after the loops of all earlier indexes.

**Complexity.**
- **Time** is O(26 * n), because each index enters once, leaves at most once, and each loop test scans 26 counts.
- **Space** is O(1), because the count array has 26 entries.

```java run
import java.util.Random;

public final class StaleMaximum {
    /** Dominant count by scanning all 26 entries. */
    static int dominant(int[] cnt) {
        int top = 0;
        for (int c : cnt) top = Math.max(top, c);
        return top;
    }

    /**
     * Returns the number of indexes where the historical maximum exceeds the exact dominant count.
     * Time: O(26 * n), a scan of 26 counts per loop test.
     * Space: O(1), a count array of 26 entries.
     * Invariant: seen is the largest exact dominant count recorded after any earlier shrink loop.
     */
    static int staleIndexes(String s, int k) {
        int[] cnt = new int[26];
        int left = 0, seen = 0, stale = 0;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            cnt[s.charAt(right) - 'a']++;
            // Shrink: runs while the replacement cost exceeds k.
            while (right - left + 1 - dominant(cnt) > k) {
                cnt[s.charAt(left) - 'a']--;
                left++;
            }
            // The exact dominant count of the repaired window.
            int exact = dominant(cnt);
            // The historical maximum never decreases.
            seen = Math.max(seen, exact);
            // Count the indexes where the historical value overstates the window.
            if (seen > exact) stale++;
        }
        // The number of stale indexes.
        return stale;
    }

    /** Oracle: recomputes each window from its boundaries by brute force. */
    static int oracle(String s, int k) {
        int left = 0, seen = 0, stale = 0;
        for (int right = 0; right < s.length(); right++) {
            while (cost(s, left, right) > k) left++;
            int exact = (right - left + 1) - cost(s, left, right);
            seen = Math.max(seen, exact);
            if (seen > exact) stale++;
        }
        return stale;
    }

    static int cost(String s, int l, int r) {
        int top = 0;
        for (int i = l; i <= r; i++) {
            int c = 0;
            for (int j = l; j <= r; j++) if (s.charAt(j) == s.charAt(i)) c++;
            top = Math.max(top, c);
        }
        return (r - l + 1) - top;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (staleIndexes("aababba", 1) != 2) throw new AssertionError("example 1");
        if (staleIndexes("abc", 0) != 0) throw new AssertionError("example 2");
        // Random strings and budgets agree with the oracle.
        Random rnd = new Random(63);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(13); i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            int k = rnd.nextInt(4);
            if (staleIndexes(sb.toString(), k) != oracle(sb.toString(), k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-char-replacement -->

**Approach.**
The cost of a window is its length minus its dominant count, and a window is valid when the cost is at most `k`. The method expands `right`, adds the entering letter to a count array of 26 entries, and runs a shrink loop while the cost exceeds `k`. The dominant count comes from a fresh scan of the counts, so it is exact after every removal. The method records the length after the loop. The invariant: once the loop ends, the window needs at most `k` replacements, and every start before `left` is unusable.

**Complexity.**
- **Time** is O(26 * n), because each index enters once and leaves at most once, and each loop test scans 26 counts.
- **Space** is O(1), because the count array has 26 entries.

```java run
import java.util.Random;

public final class CharReplacement {
    /**
     * Returns the longest substring that becomes one repeated letter after at most k replacements.
     * Time: O(26 * n), each index enters once and leaves at most once.
     * Space: O(1), a count array of 26 entries.
     * Invariant: after the shrink loop, length minus the dominant count is at most k.
     */
    static int characterReplacement(String s, int k) {
        int[] cnt = new int[26];
        int left = 0, best = 0;
        // Expand: the letter at right enters.
        for (int right = 0; right < s.length(); right++) {
            cnt[s.charAt(right) - 'A']++;
            // Shrink: runs while the replacement cost exceeds k; the scan below finds the exact dominant count.
            while (true) {
                int top = 0;
                for (int c : cnt) top = Math.max(top, c);
                if (right - left + 1 - top <= k) break;
                // The letter at left leaves the window.
                cnt[s.charAt(left) - 'A']--;
                left++;
            }
            // The window is valid, so its length is a candidate.
            best = Math.max(best, right - left + 1);
        }
        // The longest valid length.
        return best;
    }

    /** Oracle: tries every substring and every target letter. */
    static int oracle(String s, int k) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            int minMismatch = Integer.MAX_VALUE;
            for (char t = 'A'; t <= 'Z'; t++) {
                int mm = 0;
                for (int x = i; x <= j; x++) if (s.charAt(x) != t) mm++;
                minMismatch = Math.min(minMismatch, mm);
            }
            if (minMismatch <= k) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (characterReplacement("AABABBA", 1) != 4) throw new AssertionError("example 1");
        if (characterReplacement("ABAB", 2) != 4) throw new AssertionError("example 2");
        // Random strings and budgets agree with the oracle.
        Random rnd = new Random(64);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(13); i < n; i++) sb.append((char) ('A' + rnd.nextInt(3)));
            int k = rnd.nextInt(sb.length() + 1);
            if (characterReplacement(sb.toString(), k) != oracle(sb.toString(), k)) throw new AssertionError("random " + t);
        }
    }
}
```
