<!-- solutions-for: 09-window-frequency-state -->
### Window Frequency State

#### Solution: [Build] Permutation in String (LeetCode 567)
<!-- id: sw-permutation-start-index -->

**Approach.** Freeze a table of the order's counts and keep a second table for the letters inside the current range, together with `agree`, the number of the 26 letters whose two counts are equal. Letters that the order does not use agree at zero from the start. For each step, a letter that enters or leaves is handled by the same three moves: lower `agree` if the letter agreed, change its count, raise `agree` if it agrees now. When the range is as wide as the order and `agree` is 26, the start is returned. The check counts every table write and asserts at most two per slide, compares with a sort-and-compare oracle, and shows two facts used in the lesson: a set of letters cannot tell a rearrangement from a stretch with the same letters in other multiplicities, and boxed integers must not be compared with `==`.

**Complexity.** Two table writes per character, so O(n) time for a text of n characters, plus O(m) to build the order's table, and O(1) extra space for the two 26-entry tables.

```java run
import java.util.*;

public final class PermutationStartIndex {
    static int writes;

    static int firstStart(String text, String order) {
        int m = order.length(), n = text.length();
        if (m > n) return -1;
        int[] listed = new int[26], inside = new int[26];
        for (int i = 0; i < m; i++) listed[order.charAt(i) - 'a']++;
        int agree = 0;
        for (int c = 0; c < 26; c++) if (listed[c] == inside[c]) agree++;
        for (int hi = 0; hi < n; hi++) {
            int add = text.charAt(hi) - 'a';
            if (inside[add] == listed[add]) agree--;
            inside[add]++;
            writes++;
            if (inside[add] == listed[add]) agree++;
            if (hi >= m) {
                int drop = text.charAt(hi - m) - 'a';
                if (inside[drop] == listed[drop]) agree--;
                inside[drop]--;
                writes++;
                if (inside[drop] == listed[drop]) agree++;
            }
            if (hi >= m - 1 && agree == 26) return hi - m + 1;
        }
        return -1;
    }

    static int oracle(String text, String order) {
        char[] want = order.toCharArray();
        Arrays.sort(want);
        for (int s = 0; s + want.length <= text.length(); s++) {
            char[] part = text.substring(s, s + want.length).toCharArray();
            Arrays.sort(part);
            if (Arrays.equals(part, want)) return s;
        }
        return -1;
    }

    static String random(Random rnd, int len, int alphabet) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(alphabet)));
        return sb.toString();
    }

    public static void main(String[] args) {
        if (firstStart("bcxabdcab", "abc") != 6) throw new AssertionError("example 1");
        if (firstStart("ab", "abc") != -1) throw new AssertionError("example 2");
        if (firstStart("", "a") != -1) throw new AssertionError("empty text");
        if (firstStart("z", "z") != 0) throw new AssertionError("single");
        if (firstStart("aaaa", "aa") != 0) throw new AssertionError("all equal");
        if (firstStart("aab", "ab") != 1) throw new AssertionError("set is not enough");
        Set<Character> s1 = new HashSet<>(), s2 = new HashSet<>();
        for (char c : "aab".toCharArray()) s1.add(c);
        for (char c : "ab".toCharArray()) s2.add(c);
        if (!s1.equals(s2)) throw new AssertionError("sets should be equal");
        Integer big1 = 1000, big2 = 1000;
        if (big1 == big2) throw new AssertionError("boxed values above the cache are different objects");
        if (!big1.equals(big2)) throw new AssertionError("boxed values are equal by value");
        String longText = random(new Random(5), 100000, 3);
        writes = 0;
        firstStart(longText + "zzzzzz", "zzzzzzz");
        if (writes > 2 * (longText.length() + 6)) throw new AssertionError("more than two writes per slide: " + writes);
        Random rnd = new Random(1001);
        for (int t = 0; t < 3000; t++) {
            int alphabet = 1 + rnd.nextInt(4);
            String text = random(rnd, rnd.nextInt(14), alphabet);
            String order = random(rnd, 1 + rnd.nextInt(5), alphabet);
            if (firstStart(text, order) != oracle(text, order))
                throw new AssertionError("differs on " + text + " / " + order);
        }
    }
}
```

#### Solution: [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-longest-leftmost-repeat-free -->

**Approach.** Keep counts per character code in a 128-entry table. After a character enters, the only count that can exceed one is its own, so a `while` loop moves `left` forward, lowering counts, until that count is one again. Every move of `left` is a shrink step. A range replaces the record only when it is strictly longer, which keeps the leftmost of equally long ranges. Since `left` moves only by shrinking, the shrink total equals its final value, and the check compares that with the start of the longest repeat-free range that ends at the last character, found by brute force. The leftmost longest range is also found by brute force over all ranges.

**Complexity.** The left end moves at most n times and the right end n times, so the time is O(n), with a fixed table of 128 counters as space.

```java run
import java.util.*;

public final class LeftmostRepeatFree {
    static int[] solve(String s) {
        int[] seen = new int[128];
        int left = 0, shrinkSteps = 0, bestStart = 0, bestLen = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            seen[c]++;
            while (seen[c] > 1) {
                seen[s.charAt(left)]--;
                left++;
                shrinkSteps++;
            }
            if (right - left + 1 > bestLen) {
                bestStart = left;
                bestLen = right - left + 1;
            }
        }
        if (shrinkSteps > s.length()) throw new AssertionError("more than n left moves");
        return new int[] {bestStart, bestLen, shrinkSteps};
    }

    static boolean repeatFree(String s, int from, int to) {
        boolean[] used = new boolean[128];
        for (int i = from; i <= to; i++) {
            if (used[s.charAt(i)]) return false;
            used[s.charAt(i)] = true;
        }
        return true;
    }

    static int[] oracle(String s) {
        int n = s.length(), bestStart = 0, bestLen = 0;
        for (int i = 0; i < n; i++)
            for (int j = i; j < n; j++)
                if (repeatFree(s, i, j) && j - i + 1 > bestLen) { bestStart = i; bestLen = j - i + 1; }
        int lastStart = n;
        while (lastStart > 0 && repeatFree(s, lastStart - 1, n - 1)) lastStart--;
        return new int[] {bestStart, bestLen, n == 0 ? 0 : lastStart};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve("tmmzuxt"), new int[] {2, 5, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve("aaaa"), new int[] {0, 1, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(""), new int[] {0, 0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(solve("q"), new int[] {0, 1, 0})) throw new AssertionError("single");
        if (!Arrays.equals(solve("abab"), new int[] {0, 2, 2})) throw new AssertionError("tie keeps leftmost");
        Random rnd = new Random(1002);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            int alphabet = 1 + rnd.nextInt(6);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(alphabet);
                sb.append((char) (pick == 0 ? 0 : pick == 1 ? 127 : 'a' + pick));
            }
            String s = sb.toString();
            if (!Arrays.equals(solve(s), oracle(s))) throw new AssertionError("differs on " + s.length() + " chars: " + Arrays.toString(solve(s)) + " vs " + Arrays.toString(oracle(s)));
        }
    }
}
```

#### Solution: [Boundary] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-exact-max-repaint-window -->

**Approach.** Keep 26 counters for the letters in the range. After a letter enters, take the exact largest counter and shrink with a `while` loop, taking the exact largest counter again after each removal, until the length minus that largest count is at most k. The range is valid at the moment it is compared with the record, and it replaces the record only if strictly longer, so the leftmost of equal ranges stays. A budget of k at least the string length keeps the whole string. The check verifies validity of the recorded range by brute force, counts the scans of the 26 counters, and compares with a search over every range.

**Complexity.** The counters are scanned at most twice per character, so about 52 n reads in the worst case, written as O(n) for a fixed alphabet, with O(1) extra space.

```java run
import java.util.*;

public final class ExactMaxRepaint {
    static int scans;

    static int largest(int[] counts) {
        scans++;
        int m = 0;
        for (int v : counts) m = Math.max(m, v);
        return m;
    }

    static int[] bestRange(String s, int k) {
        int[] counts = new int[26];
        int left = 0, bestStart = 0, bestLen = 0;
        for (int right = 0; right < s.length(); right++) {
            counts[s.charAt(right) - 'A']++;
            int most = largest(counts);
            while (right - left + 1 - most > k) {
                counts[s.charAt(left++) - 'A']--;
                most = largest(counts);
            }
            if (right - left + 1 - most > k) throw new AssertionError("recorded an invalid range");
            if (right - left + 1 > bestLen) { bestStart = left; bestLen = right - left + 1; }
        }
        return new int[] {bestStart, bestLen};
    }

    static boolean fits(String s, int from, int to, int k) {
        int[] c = new int[26];
        int most = 0;
        for (int i = from; i <= to; i++) most = Math.max(most, ++c[s.charAt(i) - 'A']);
        return to - from + 1 - most <= k;
    }

    static int[] oracle(String s, int k) {
        int bestStart = 0, bestLen = 0;
        for (int i = 0; i < s.length(); i++)
            for (int j = i; j < s.length(); j++)
                if (fits(s, i, j, k) && j - i + 1 > bestLen) { bestStart = i; bestLen = j - i + 1; }
        return new int[] {bestStart, bestLen};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(bestRange("ABBBACDDE", 1), new int[] {0, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(bestRange("XYZ", 0), new int[] {0, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(bestRange("", 3), new int[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(bestRange("ABCDE", 9), new int[] {0, 5})) throw new AssertionError("budget above length");
        if (!Arrays.equals(bestRange("KKKK", 0), new int[] {0, 4})) throw new AssertionError("all equal");
        Random rnd = new Random(1003);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(15);
            int alphabet = rnd.nextBoolean() ? 3 : 26;
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('A' + rnd.nextInt(alphabet)));
            String s = sb.toString();
            int k = rnd.nextInt(n + 2);
            scans = 0;
            int[] got = bestRange(s, k);
            if (scans > 2 * n) throw new AssertionError("more than two scans per character");
            if (!Arrays.equals(got, oracle(s, k))) throw new AssertionError("differs on " + s + " k " + k);
        }
    }
}
```

#### Solution: [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-count-minimal-covers -->

**Approach.** Store the required count of each character and the number of characters whose requirement is not yet met, `short`. When a character enters and its count reaches the requirement, `short` drops. While `short` is zero, the current range covers t: compare its length with the shortest so far, replacing the record and resetting the tally on a strictly shorter range, adding one to the tally on an equal one, then drop the left character and raise `short` if its requirement is no longer met. Several covers can be seen at one right end, but their lengths strictly decrease, so each shortest start is counted once. The oracle finds, for every start, the first end that covers, takes the minimum length, and counts the starts that reach it. The check also counts the moves of both ends.

**Complexity.** Each end moves forward at most n times, so the time is O(n + m) with m the length of t, and the space is two tables of 128 counters.

```java run
import java.util.*;

public final class MinimalCoverCount {
    static int moves;

    static int[] countCovers(String s, String t) {
        int[] required = new int[128], inside = new int[128];
        int lacking = 0;
        for (int i = 0; i < t.length(); i++) if (required[t.charAt(i)]++ == 0) lacking++;
        int left = 0, shortest = Integer.MAX_VALUE, tally = 0, firstStart = -1;
        for (int right = 0; right < s.length(); right++) {
            char in = s.charAt(right);
            moves++;
            inside[in]++;
            if (required[in] > 0 && inside[in] == required[in]) lacking--;
            while (lacking == 0) {
                int len = right - left + 1;
                if (len < shortest) { shortest = len; tally = 1; firstStart = left; }
                else if (len == shortest) tally++;
                char out = s.charAt(left++);
                moves++;
                inside[out]--;
                if (required[out] > 0 && inside[out] < required[out]) lacking++;
            }
        }
        return tally == 0 ? new int[] {0, -1} : new int[] {tally, firstStart};
    }

    static boolean covers(String s, int from, int to, String t) {
        int[] c = new int[128];
        for (int i = from; i <= to; i++) c[s.charAt(i)]++;
        int[] need = new int[128];
        for (int i = 0; i < t.length(); i++) need[t.charAt(i)]++;
        for (int ch = 0; ch < 128; ch++) if (c[ch] < need[ch]) return false;
        return true;
    }

    static int[] oracle(String s, String t) {
        int best = Integer.MAX_VALUE;
        int[] lengthFrom = new int[s.length()];
        for (int i = 0; i < s.length(); i++) {
            lengthFrom[i] = -1;
            for (int j = i; j < s.length(); j++)
                if (covers(s, i, j, t)) { lengthFrom[i] = j - i + 1; break; }
            if (lengthFrom[i] != -1) best = Math.min(best, lengthFrom[i]);
        }
        int count = 0, first = -1;
        for (int i = 0; i < s.length(); i++)
            if (lengthFrom[i] == best) { if (count == 0) first = i; count++; }
        return count == 0 ? new int[] {0, -1} : new int[] {count, first};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(countCovers("xabxbaxab", "ab"), new int[] {3, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(countCovers("zzz", "zz"), new int[] {2, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(countCovers("abc", "d"), new int[] {0, -1})) throw new AssertionError("absent");
        if (!Arrays.equals(countCovers("ab", "abc"), new int[] {0, -1})) throw new AssertionError("t longer");
        if (!Arrays.equals(countCovers("", "a"), new int[] {0, -1})) throw new AssertionError("empty s");
        if (!Arrays.equals(countCovers("k", "k"), new int[] {1, 0})) throw new AssertionError("single");
        Random rnd = new Random(1004);
        for (int t = 0; t < 3000; t++) {
            int alphabet = 1 + rnd.nextInt(4);
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            int n = rnd.nextInt(14), m = 1 + rnd.nextInt(4);
            for (int i = 0; i < n; i++) a.append((char) (rnd.nextInt(alphabet) == 0 ? 0 : 'a' + rnd.nextInt(alphabet)));
            for (int i = 0; i < m; i++) b.append((char) (rnd.nextInt(alphabet) == 0 ? 0 : 'a' + rnd.nextInt(alphabet)));
            String s = a.toString(), pat = b.toString();
            moves = 0;
            int[] got = countCovers(s, pat);
            if (moves > 2 * n) throw new AssertionError("more than 2n moves");
            if (!Arrays.equals(got, oracle(s, pat))) throw new AssertionError("differs on n=" + n + " m=" + m + " " + Arrays.toString(got) + " vs " + Arrays.toString(oracle(s, pat)));
        }
    }
}
```
