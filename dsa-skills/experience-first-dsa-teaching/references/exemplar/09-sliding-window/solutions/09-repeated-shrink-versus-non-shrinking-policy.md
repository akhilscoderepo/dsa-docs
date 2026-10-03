<!-- solutions-for: 09-repeated-shrink-versus-non-shrinking-policy -->
### Repeated-Shrink Versus Non-Shrinking Policy

#### Solution: [Build] Restore Before Record (Author exercise)
<!-- id: sw-restore-before-record -->

**Approach.** Keep a tally per letter and repair from the left with a `while` loop whenever the arriving letter's count exceeds two. Before measuring, verify that every tally is at most two, and throw if not. Because the loop is a `while`, the check never fires.

**Complexity.** O(n) time and O(1) extra space. The validity check scans 26 slots at each step, which keeps the time at O(26 * n), still linear for a fixed alphabet.

```java run
public final class RestoreBeforeRecord {
    static int longest(String s) {
        int[] count = new int[26];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            count[s.charAt(right) - 'a']++;
            while (count[s.charAt(right) - 'a'] > 2) {
                count[s.charAt(left) - 'a']--;
                left++;
            }
            for (int c : count) {
                if (c > 2) throw new IllegalStateException("window is not valid");
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (longest("aaabbb") != 4) throw new AssertionError("example 1");
        if (longest("abcabc") != 6) throw new AssertionError("example 2");
        if (longest("") != 0) throw new AssertionError("empty");
        if (longest("aaaaa") != 2) throw new AssertionError("single letter");
    }
}
```

#### Solution: [Vary] One-Removal Maximum-Length Trace (Author exercise)
<!-- id: sw-one-removal-trace -->

**Approach.** Keep a tally and a stored `maxFreq` that is raised on arrival. After each arrival, if the stored cost is over the budget, move `left` forward by exactly one. Record the window length for every index. Each entry is the best length proved achievable for the prefix, so the sequence never decreases.

**Complexity.** O(n) time and O(1) extra space beyond the output array.

```java run
import java.util.Arrays;

public final class OneRemovalTrace {
    static int[] lengths(String s, int k) {
        int[] tally = new int[26];
        int[] out = new int[s.length()];
        int left = 0, maxFreq = 0;
        for (int right = 0; right < s.length(); right++) {
            maxFreq = Math.max(maxFreq, ++tally[s.charAt(right) - 'A']);
            if (right - left + 1 - maxFreq > k) {
                tally[s.charAt(left) - 'A']--;
                left++;
            }
            out[right] = right - left + 1;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(lengths("AABABBA", 1), new int[] {1, 2, 3, 4, 4, 4, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(lengths("ABCD", 0), new int[] {1, 1, 1, 1})) throw new AssertionError("example 2");
        int[] t = lengths("AABBBAAB", 2);
        for (int i = 1; i < t.length; i++) if (t[i] < t[i - 1]) throw new AssertionError("must not decrease");
    }
}
```

#### Solution: [Boundary] Multiple Left Removals Needed (Author exercise)
<!-- id: sw-multiple-removals -->

**Approach.** Compute the correct answer with a `while` repair loop. Compute the variant with an `if`, keeping the largest window length it measures. The variant diverges exactly when one arrival requires more than one removal, because after a single removal the window still holds a repeat and the incoming letter's own count no longer signals it.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class MultipleRemovals {
    static int correct(String s) {
        int[] count = new int[26];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'a';
            count[c]++;
            while (count[c] > 1) {
                count[s.charAt(left) - 'a']--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int oneRemoval(String s) {
        int[] count = new int[26];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'a';
            count[c]++;
            if (count[c] > 1) {
                count[s.charAt(left) - 'a']--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int[] both(String s) {
        return new int[] {correct(s), oneRemoval(s)};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(both("abba"), new int[] {2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(both("abcabc"), new int[] {3, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(both(""), new int[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(both("aabba"), new int[] {2, 3})) throw new AssertionError("longer failure");
        if (!Arrays.equals(both("qrrstq"), new int[] {4, 5})) throw new AssertionError("extend example");
        if (!Arrays.equals(both("dvdfkd"), new int[] {4, 4})) throw new AssertionError("single removals suffice");
    }
}
```

#### Solution: [Recognize] Longest Repeating Character Replacement, Both Policies (LeetCode 424)
<!-- id: sw-replacement-both-policies -->

**Approach.** The repeated-shrink version promises a valid-by-stored-maximum window after the loop and records the best length. The non-shrinking version moves `left` at most once and returns the final length, which is the candidate length. Both rely on a stored `maxFreq` that is raised on arrival and never lowered. The two are compared and a mismatch throws.

**Complexity.** O(n) time and O(1) extra space for each version.

```java run
public final class ReplacementBothPolicies {
    static int shrink(String s, int k) {
        int[] tally = new int[26];
        int left = 0, maxFreq = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            maxFreq = Math.max(maxFreq, ++tally[s.charAt(right) - 'A']);
            while (right - left + 1 - maxFreq > k) {
                tally[s.charAt(left) - 'A']--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int slide(String s, int k) {
        int[] tally = new int[26];
        int left = 0, maxFreq = 0;
        for (int right = 0; right < s.length(); right++) {
            maxFreq = Math.max(maxFreq, ++tally[s.charAt(right) - 'A']);
            if (right - left + 1 - maxFreq > k) {
                tally[s.charAt(left) - 'A']--;
                left++;
            }
        }
        return s.length() - left;
    }

    static int characterReplacement(String s, int k) {
        int a = shrink(s, k), b = slide(s, k);
        if (a != b) throw new IllegalStateException("policies disagree: " + a + " vs " + b);
        return a;
    }

    public static void main(String[] args) {
        if (characterReplacement("XYXXY", 1) != 4) throw new AssertionError("example 1");
        if (characterReplacement("BBABCBB", 1) != 4) throw new AssertionError("example 2");
        java.util.Random rnd = new java.util.Random(7);
        for (int trial = 0; trial < 2000; trial++) {
            int n = 1 + rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('A' + rnd.nextInt(3)));
            characterReplacement(sb.toString(), rnd.nextInt(n + 1));
        }
    }
}
```

#### Solution: [Extend] Non-Shrinking Without Repeats (Author exercise)
<!-- id: sw-unique-non-shrinking -->

**Approach.** Keep a counter `repeats` of letters whose count is above one. It rises when a count goes from one to two on arrival and falls when a count goes from two to one on departure. After each arrival, if `repeats` is above zero the whole window is invalid, so the left edge moves one step. Because the test is exact and validity is monotone, the window length never drops below the best valid length, and the final length is the answer.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class UniqueNonShrinking {
    static int slide(String s) {
        int[] count = new int[26];
        int repeats = 0, left = 0;
        for (int right = 0; right < s.length(); right++) {
            if (++count[s.charAt(right) - 'a'] == 2) repeats++;
            if (repeats > 0) {
                if (--count[s.charAt(left) - 'a'] == 1) repeats--;
                left++;
            }
        }
        return s.length() - left;
    }

    static int shrink(String s) {
        int[] count = new int[26];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'a';
            count[c]++;
            while (count[c] > 1) {
                count[s.charAt(left) - 'a']--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (slide("abba") != 2) throw new AssertionError("example 1");
        if (slide("qrrstq") != 4) throw new AssertionError("example 2");
        if (slide("") != 0) throw new AssertionError("empty");
        java.util.Random rnd = new java.util.Random(11);
        for (int trial = 0; trial < 3000; trial++) {
            int n = rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            String s = sb.toString();
            if (slide(s) != shrink(s)) throw new AssertionError("policies disagree on " + s);
        }
    }
}
```
