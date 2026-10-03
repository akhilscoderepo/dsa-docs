<!-- solutions-for: 09-minimum-cover-and-deficit-windows -->
### Minimum-Cover And Deficit Windows

#### Solution: [Build] Shortest Segment Containing A And B (Author exercise)
<!-- id: sw-shortest-a-and-b -->

**Approach.** Keep a counter for `a` and one for `b` in the window. Add the symbol at `right`, then while both counters are positive, record the length and remove the leftmost symbol, which may drop one counter to zero and end the shrink. The oracle checks every substring on random strings over a small alphabet, and the check counts left moves to confirm the pointer never travels more than n steps.

**Complexity.** The scan is linear in the string length with two counters of extra space, and no substring is built.

```java run
import java.util.Random;

public final class ShortestAandB {
    static int leftMoves;

    static int shortest(String s) {
        int a = 0, b = 0, left = 0, best = -1;
        for (int right = 0; right < s.length(); right++) {
            char in = s.charAt(right);
            if (in == 'a') a++;
            else if (in == 'b') b++;
            while (a > 0 && b > 0) {
                int len = right - left + 1;
                if (best == -1 || len < best) best = len;
                char out = s.charAt(left++);
                leftMoves++;
                if (out == 'a') a--;
                else if (out == 'b') b--;
            }
        }
        return best;
    }
    static int oracle(String s) {
        int best = -1;
        for (int i = 0; i < s.length(); i++) {
            for (int j = i; j < s.length(); j++) {
                String w = s.substring(i, j + 1);
                if (w.indexOf('a') >= 0 && w.indexOf('b') >= 0 && (best == -1 || w.length() < best)) best = w.length();
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (shortest("bxxxaxxb") != 4) throw new AssertionError("example 1");
        if (shortest("cccc") != -1) throw new AssertionError("example 2");
        if (shortest("") != -1) throw new AssertionError("empty");
        if (shortest("a") != -1 || shortest("ab") != 2) throw new AssertionError("tiny");
        if (shortest("aaaa") != -1) throw new AssertionError("only a");
        Random rnd = new Random(911);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append("abc".charAt(rnd.nextInt(3)));
            String s = sb.toString();
            leftMoves = 0;
            if (shortest(s) != oracle(s)) throw new AssertionError("differs on " + s);
            if (leftMoves > n) throw new AssertionError("left moved more than n times");
        }
    }
}
```

#### Solution: [Vary] Required Multiplicities (Author exercise)
<!-- id: sw-required-multiplicities -->

**Approach.** Count the letters in the window and keep `satisfied`, the number of letters whose window count has reached the demand, next to `target`, the number of letters with a positive demand. When the window count of a letter becomes equal to its demand, `satisfied` rises, and when removal makes it one less than the demand, `satisfied` falls. A third copy of a letter leaves the number unchanged, which the check exercises with surplus-heavy strings. The `need` array is copied by reference only for reading, and the check asserts that it is unchanged afterwards.

**Complexity.** Each index is added once and removed at most once, so the time is linear, with a 26-slot table.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RequiredMultiplicities {
    static int shortest(String s, int[] need) {
        int[] have = new int[26];
        int target = 0;
        for (int n : need) if (n > 0) target++;
        int satisfied = 0, left = 0, best = -1;
        for (int right = 0; right < s.length(); right++) {
            int in = s.charAt(right) - 'a';
            have[in]++;
            if (need[in] > 0 && have[in] == need[in]) satisfied++;
            while (satisfied == target) {
                int len = right - left + 1;
                if (best == -1 || len < best) best = len;
                int out = s.charAt(left++) - 'a';
                if (need[out] > 0 && have[out] == need[out]) satisfied--;
                have[out]--;
            }
        }
        return best;
    }
    static int oracle(String s, int[] need) {
        int best = -1;
        for (int i = 0; i < s.length(); i++) {
            for (int j = i; j < s.length(); j++) {
                int[] c = new int[26];
                for (int x = i; x <= j; x++) c[s.charAt(x) - 'a']++;
                boolean ok = true;
                for (int k = 0; k < 26; k++) if (c[k] < need[k]) ok = false;
                if (ok && (best == -1 || j - i + 1 < best)) best = j - i + 1;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        int[] n1 = new int[26];
        n1[0] = 2;
        n1[1] = 1;
        if (shortest("abaxbbaxa", n1) != 3) throw new AssertionError("example 1");
        if (shortest("xaybxa", n1) != 5) throw new AssertionError("example 2");
        int[] untouched = n1.clone();
        if (!Arrays.equals(n1, untouched)) throw new AssertionError("need was modified");
        if (shortest("", n1) != -1) throw new AssertionError("empty string");
        int[] one = new int[26];
        one[2] = 1;
        if (shortest("c", one) != 1) throw new AssertionError("single letter");
        int[] many = new int[26];
        many[0] = 5;
        if (shortest("aaaa", many) != -1 || shortest("aaaaaa", many) != 5) throw new AssertionError("all equal");
        Random rnd = new Random(912);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            String s = sb.toString();
            int[] need = new int[26];
            do {
                Arrays.fill(need, 0);
                for (int k = 0; k < 4; k++) need[k] = rnd.nextInt(3);
            } while (Arrays.stream(need).sum() == 0);
            int[] copy = need.clone();
            if (shortest(s, need) != oracle(s, need)) throw new AssertionError("differs on " + s + " " + Arrays.toString(need));
            if (!Arrays.equals(need, copy)) throw new AssertionError("need was modified");
        }
    }
}
```

#### Solution: [Boundary] No Cover Exists (Author exercise)
<!-- id: sw-no-cover-exists -->

**Approach.** Build a ledger of required counts from `t` and the number still missing, which starts at the length of `t`. Scan with the add, record and remove moves and keep `bestStart` and `bestLength`, with the start set to minus one until a window is recorded. A `t` longer than `s`, or a letter that is absent from `s`, never lets `missing` reach zero, so the sentinel pair `[-1, 0]` is returned with no special loop. Because only indices are returned, nothing is cut out of `s`. The oracle is a quadratic scan that picks the leftmost shortest window by sorted-letter comparison, and the check covers both examples and the unreachable cases.

**Complexity.** O(|s| + |t|) time and a 26-slot table; the pair needs two integers.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NoCoverExists {
    static int[] cover(String s, String t) {
        int[] ledger = new int[26];
        for (int i = 0; i < t.length(); i++) ledger[t.charAt(i) - 'a']++;
        int missing = t.length();
        int left = 0, bestStart = -1, bestLength = 0;
        for (int right = 0; right < s.length(); right++) {
            if (ledger[s.charAt(right) - 'a']-- > 0) missing--;
            while (missing == 0) {
                int len = right - left + 1;
                if (bestStart == -1 || len < bestLength) {
                    bestStart = left;
                    bestLength = len;
                }
                if (++ledger[s.charAt(left++) - 'a'] > 0) missing++;
            }
        }
        return new int[] {bestStart, bestLength};
    }
    static int[] oracle(String s, String t) {
        char[] want = t.toCharArray();
        Arrays.sort(want);
        int[] best = {-1, 0};
        for (int i = 0; i < s.length(); i++) {
            for (int j = i; j < s.length(); j++) {
                int len = j - i + 1;
                if (best[0] != -1 && len >= best[1]) break;
                int[] c = new int[26];
                for (int x = i; x <= j; x++) c[s.charAt(x) - 'a']++;
                int[] w = new int[26];
                for (char ch : want) w[ch - 'a']++;
                boolean ok = true;
                for (int k = 0; k < 26; k++) if (c[k] < w[k]) ok = false;
                if (ok) {
                    best[0] = i;
                    best[1] = len;
                    break;
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(cover("qq", "qqq"), new int[] {-1, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(cover("zxyzyx", "xyz"), new int[] {0, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(cover("", "a"), new int[] {-1, 0})) throw new AssertionError("empty s");
        if (!Arrays.equals(cover("abc", "d"), new int[] {-1, 0})) throw new AssertionError("absent letter");
        if (!Arrays.equals(cover("a", "a"), new int[] {0, 1})) throw new AssertionError("single");
        if (!Arrays.equals(cover("bbbb", "bb"), new int[] {0, 2})) throw new AssertionError("all equal");
        Random rnd = new Random(913);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            int m = 1 + rnd.nextInt(5);
            StringBuilder tb = new StringBuilder();
            for (int i = 0; i < m; i++) tb.append((char) ('a' + rnd.nextInt(5)));
            String s = sb.toString(), pat = tb.toString();
            if (!Arrays.equals(cover(s, pat), oracle(s, pat))) throw new AssertionError("differs on " + s + " / " + pat);
        }
    }
}
```

#### Solution: [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-min-window-substring -->

**Approach.** Fill a 128-slot ledger from `t`, then scan `s` with the same three moves: add the new character and lower `missing` only if its ledger entry was positive, record boundaries while `missing` is zero, and remove from the left. The ledger may go negative for surplus characters, and an entry that climbs back above zero raises `missing`. The scan keeps only the best start and length. The substring is made once after the scan, which the check proves with a counter on the extraction helper, and neither input is changed.

**Complexity.** The scan adds each position once and removes it at most once, so the time is O(|s| + |t|) and the table has constant size.

```java run
import java.util.Random;

public final class MinWindowSubstring {
    static int builds;

    static String extract(String s, int start, int length) {
        builds++;
        return s.substring(start, start + length);
    }
    static String minWindow(String s, String t) {
        int[] ledger = new int[128];
        for (int i = 0; i < t.length(); i++) ledger[t.charAt(i)]++;
        int missing = t.length();
        int left = 0, bestStart = 0, bestLength = Integer.MAX_VALUE;
        for (int right = 0; right < s.length(); right++) {
            if (ledger[s.charAt(right)]-- > 0) missing--;
            while (missing == 0) {
                if (right - left + 1 < bestLength) {
                    bestLength = right - left + 1;
                    bestStart = left;
                }
                if (++ledger[s.charAt(left++)] > 0) missing++;
            }
        }
        return bestLength == Integer.MAX_VALUE ? "" : extract(s, bestStart, bestLength);
    }
    static String oracle(String s, String t) {
        String best = "";
        for (int i = 0; i < s.length(); i++) {
            for (int j = i + 1; j <= s.length(); j++) {
                String w = s.substring(i, j);
                if (!best.isEmpty() && w.length() >= best.length()) break;
                int[] c = new int[128];
                for (char ch : w.toCharArray()) c[ch]++;
                int[] need = new int[128];
                for (char ch : t.toCharArray()) need[ch]++;
                boolean ok = true;
                for (int k = 0; k < 128; k++) if (c[k] < need[k]) ok = false;
                if (ok) {
                    best = w;
                    break;
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (!minWindow("kxyzxkzyxk", "xxkz").equals("kxyzx")) throw new AssertionError("example 1");
        if (!minWindow("abc", "abcc").isEmpty()) throw new AssertionError("example 2");
        builds = 0;
        if (!minWindow("abc", "d").isEmpty() || builds != 0) throw new AssertionError("no cover builds nothing");
        if (!minWindow("a", "a").equals("a")) throw new AssertionError("single");
        if (!minWindow("bbbb", "bb").equals("bb")) throw new AssertionError("all equal");
        if (!minWindow("Aa", "aA").equals("Aa")) throw new AssertionError("case sensitive");
        Random rnd = new Random(914);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append("abAB".charAt(rnd.nextInt(4)));
            int m = 1 + rnd.nextInt(4);
            StringBuilder tb = new StringBuilder();
            for (int i = 0; i < m; i++) tb.append("abABc".charAt(rnd.nextInt(5)));
            String s = sb.toString(), pat = tb.toString();
            builds = 0;
            String got = minWindow(s, pat);
            if (!got.equals(oracle(s, pat))) throw new AssertionError("differs on " + s + " / " + pat);
            if (builds > 1) throw new AssertionError("substring built more than once");
        }
    }
}
```
