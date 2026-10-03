<!-- solutions-for: 09-fixed-frequency-windows -->
### Fixed Frequency Windows

#### Solution: [Build] Binary Window Counts (Author exercise)
<!-- id: sw-binary-counts -->

**Approach.** The tally for a single color is one counter. Before the frame is full, only additions happen. From position k onward each step removes the bit that sits k places behind, and from position k - 1 onward the counter is copied into the answer. Zeros add and subtract nothing, so they cost no special handling. The check compares with a from-scratch count on random bit arrays, includes all zeros and all ones, confirms that the input is unchanged, and counts reads to stay within two per element.

**Complexity.** Each position is touched a bounded number of times, so the running time is linear in the array length; the output array is the only extra storage.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BinaryCounts {
    static int touches;

    static int[] onesPerBlock(int[] bits, int k) {
        int[] answer = new int[bits.length - k + 1];
        int ones = 0;
        for (int i = 0; i < bits.length; i++) {
            ones += bits[i];
            touches++;
            if (i - k >= 0) {
                ones -= bits[i - k];
                touches++;
            }
            if (i - k + 1 >= 0) answer[i - k + 1] = ones;
        }
        return answer;
    }

    static int[] oracle(int[] bits, int k) {
        int[] answer = new int[bits.length - k + 1];
        for (int s = 0; s < answer.length; s++) {
            for (int j = s; j < s + k; j++) if (bits[j] == 1) answer[s]++;
        }
        return answer;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(onesPerBlock(new int[] {1, 0, 1, 1, 0, 0, 1}, 4), new int[] {3, 2, 2, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(onesPerBlock(new int[] {0, 0, 0}, 3), new int[] {0})) throw new AssertionError("example 2");
        Random rnd = new Random(921);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] bits = new int[n];
            int mode = rnd.nextInt(4);
            for (int i = 0; i < n; i++) bits[i] = mode == 0 ? 0 : mode == 1 ? 1 : rnd.nextInt(2);
            int[] copy = bits.clone();
            int k = 1 + rnd.nextInt(n);
            touches = 0;
            int[] got = onesPerBlock(bits, k);
            if (!Arrays.equals(got, oracle(bits, k))) throw new AssertionError("differs on " + Arrays.toString(bits) + " k " + k);
            if (!Arrays.equals(bits, copy)) throw new AssertionError("input was mutated");
            if (touches > 2 * n) throw new AssertionError("more than two reads per element");
        }
    }
}
```

#### Solution: [Vary] Find All Anagrams in a String (LeetCode 438)
<!-- id: sw-find-anagrams -->

**Approach.** Build the card's tally once. Walk over the text, adding the entering letter, removing the letter that is m places behind, and comparing the two 26-slot arrays with `Arrays.equals` whenever the frame holds m letters. A pattern longer than the text returns an empty list before any array is touched. The check compares with a sort-based oracle over a three-letter alphabet, which forces many matches and near misses. It also shows that `==` on two equal arrays is false while `Arrays.equals` is true, and that a capital letter breaks the 26-slot assumption with an exception.

**Complexity.** Two array updates and one comparison of 26 slots per position, which is linear in the text length for this fixed alphabet; extra space is two small arrays plus the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FindAnagrams {
    static List<Integer> findAnagrams(String text, String pattern) {
        List<Integer> hits = new ArrayList<>();
        int m = pattern.length();
        if (m > text.length()) return hits;
        int[] target = new int[26];
        int[] current = new int[26];
        for (char ch : pattern.toCharArray()) target[ch - 'a']++;
        for (int right = 0; right < text.length(); right++) {
            current[text.charAt(right) - 'a']++;
            int left = right - m + 1;
            if (left > 0) current[text.charAt(left - 1) - 'a']--;
            if (left >= 0 && Arrays.equals(target, current)) hits.add(left);
        }
        return hits;
    }

    static List<Integer> oracle(String text, String pattern) {
        List<Integer> hits = new ArrayList<>();
        char[] want = pattern.toCharArray();
        Arrays.sort(want);
        for (int s = 0; s + want.length <= text.length(); s++) {
            char[] piece = text.substring(s, s + want.length).toCharArray();
            Arrays.sort(piece);
            if (Arrays.equals(piece, want)) hits.add(s);
        }
        return hits;
    }

    public static void main(String[] args) {
        if (!findAnagrams("abcbacab", "abc").equals(List.of(0, 2, 3, 5))) throw new AssertionError("example 1");
        if (!findAnagrams("aaaa", "aa").equals(List.of(0, 1, 2))) throw new AssertionError("example 2");
        if (!findAnagrams("ab", "abc").isEmpty()) throw new AssertionError("pattern longer than text");
        if (!findAnagrams("", "a").isEmpty()) throw new AssertionError("empty text");
        int[] first = new int[26];
        int[] second = new int[26];
        if (first == second) throw new AssertionError("distinct arrays are distinct objects");
        if (!Arrays.equals(first, second)) throw new AssertionError("equal contents");
        boolean failed = false;
        try {
            findAnagrams("abC", "a");
        } catch (ArrayIndexOutOfBoundsException e) {
            failed = true;
        }
        if (!failed) throw new AssertionError("a capital letter must leave the 26-slot domain");
        Random rnd = new Random(922);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            int m = 1 + rnd.nextInt(5);
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0; i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0; i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (t % 11 == 0) {
                a = new StringBuilder("a".repeat(n));
                b = new StringBuilder("a".repeat(m));
            }
            if (!findAnagrams(a.toString(), b.toString()).equals(oracle(a.toString(), b.toString()))) throw new AssertionError("differs on " + a + " " + b);
        }
    }
}
```

#### Solution: [Boundary] Repeated Required Character (Author exercise)
<!-- id: sw-repeated-required -->

**Approach.** Store how many of each letter the pattern requires, and keep `missing`, the number of required letters not yet covered, which starts at the pattern length. When a letter enters while its tally is still below its requirement, `missing` drops by one; when a letter leaves and its tally falls below the requirement, `missing` rises by one. A block counts exactly when `missing` is zero, so no scan of 26 slots is needed. Verification tallies every block from scratch as the oracle, counts the slot updates, and shows that a plain set-of-letters test accepts a block that the second example proves invalid.

**Complexity.** Two tally updates per position and a constant amount of other work, so linear time and constant extra space.

```java run
import java.util.Random;

public final class RepeatedRequired {
    static int updates;

    static int countCovering(String text, String pattern, int k) {
        int[] need = new int[26];
        int[] have = new int[26];
        for (char ch : pattern.toCharArray()) need[ch - 'a']++;
        int missing = pattern.length();
        int good = 0;
        for (int right = 0; right < text.length(); right++) {
            int in = text.charAt(right) - 'a';
            if (have[in] < need[in]) missing--;
            have[in]++;
            updates++;
            if (right >= k) {
                int out = text.charAt(right - k) - 'a';
                have[out]--;
                if (have[out] < need[out]) missing++;
                updates++;
            }
            if (right >= k - 1 && missing == 0) good++;
        }
        return good;
    }

    static int brute(String text, String pattern, int k) {
        int good = 0;
        for (int s = 0; s + k <= text.length(); s++) {
            int[] have = new int[26];
            for (int i = s; i < s + k; i++) have[text.charAt(i) - 'a']++;
            int[] need = new int[26];
            for (char ch : pattern.toCharArray()) need[ch - 'a']++;
            boolean ok = true;
            for (int c = 0; c < 26; c++) if (have[c] < need[c]) ok = false;
            if (ok) good++;
        }
        return good;
    }

    static int bySetOfLetters(String text, String pattern, int k) {
        int good = 0;
        for (int s = 0; s + k <= text.length(); s++) {
            boolean ok = true;
            for (char ch : pattern.toCharArray()) if (text.substring(s, s + k).indexOf(ch) < 0) ok = false;
            if (ok) good++;
        }
        return good;
    }

    public static void main(String[] args) {
        if (countCovering("abacaab", "aab", 4) != 3) throw new AssertionError("example 1");
        if (countCovering("abxcb", "aab", 3) != 0) throw new AssertionError("example 2");
        if (bySetOfLetters("abxcb", "aab", 3) != 1) throw new AssertionError("a set accepts the block abx");
        if (countCovering("aab", "aab", 3) != 1) throw new AssertionError("whole text equals pattern");
        if (countCovering("a", "a", 1) != 1) throw new AssertionError("single letter");
        Random rnd = new Random(923);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int m = 1 + rnd.nextInt(Math.min(n, 4));
            int k = m + rnd.nextInt(n - m + 1);
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0; i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0; i < m; i++) b.append((char) ('a' + rnd.nextInt(2)));
            if (t % 13 == 0) a = new StringBuilder("a".repeat(n));
            updates = 0;
            int got = countCovering(a.toString(), b.toString(), k);
            if (got != brute(a.toString(), b.toString(), k)) throw new AssertionError("differs on " + a + " " + b + " " + k);
            if (updates > 2 * n) throw new AssertionError("more than two updates per position");
        }
    }
}
```

#### Solution: [Recognize] Permutation in String (LeetCode 567)
<!-- id: sw-permutation-in-string -->

**Approach.** Use one balance array that starts as the pattern's counts. Each entering letter subtracts one from its slot and each leaving letter adds one back, so the array is all zeros exactly when the stretch is a permutation of the pattern. Test for zeros only once the frame holds m letters, and return true at the first success. A pattern longer than the text answers false immediately. The check compares with a sort-based oracle on random lowercase strings, confirms both examples, and counts slot visits to show the bound of 26 per full-length stretch.

**Complexity.** Two updates and at most 26 comparisons per position, which is linear in the text length for the fixed alphabet; extra space is one 26-slot array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PermutationInString {
    static int slotVisits;

    static boolean contains(String pattern, String text) {
        int m = pattern.length();
        if (m > text.length()) return false;
        int[] balance = new int[26];
        for (int i = 0; i < m; i++) balance[pattern.charAt(i) - 'a']++;
        for (int pos = 0; pos < text.length(); pos++) {
            balance[text.charAt(pos) - 'a']--;
            if (pos >= m) balance[text.charAt(pos - m) - 'a']++;
            if (pos + 1 < m) continue;
            int slot = 0;
            while (slot < 26) {
                slotVisits++;
                if (balance[slot] != 0) break;
                slot++;
            }
            if (slot == 26) return true;
        }
        return false;
    }

    static boolean oracle(String pattern, String text) {
        char[] want = pattern.toCharArray();
        Arrays.sort(want);
        for (int s = 0; s + want.length <= text.length(); s++) {
            char[] piece = text.substring(s, s + want.length).toCharArray();
            Arrays.sort(piece);
            if (Arrays.equals(piece, want)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        if (!contains("abbc", "cbxabcb")) throw new AssertionError("example 1");
        if (contains("aab", "abxbaxa")) throw new AssertionError("example 2");
        if (contains("abc", "ab")) throw new AssertionError("pattern longer than text");
        if (!contains("z", "z")) throw new AssertionError("single letter");
        if (contains("a", "")) throw new AssertionError("empty text");
        Random rnd = new Random(924);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            int m = 1 + rnd.nextInt(5);
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0; i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0; i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (t % 17 == 0) {
                a = new StringBuilder("c".repeat(n));
                b = new StringBuilder("c".repeat(m));
            }
            slotVisits = 0;
            boolean got = contains(b.toString(), a.toString());
            if (got != oracle(b.toString(), a.toString())) throw new AssertionError("differs on " + a + " " + b);
            int fullStretches = Math.max(0, n - m + 1);
            if (slotVisits > 26 * fullStretches) throw new AssertionError("more than 26 visits per stretch");
        }
    }
}
```
