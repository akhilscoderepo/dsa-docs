<!-- solutions-for: 09-sliding-window -->
### Solutions For Fixed Windows With Counts

#### Solution: [Build] Binary Window Counts (Author exercise)
<!-- id: sw-binary-counts -->

**Approach.**
The count array has two entries, one per possible value. The method adds the first `k` values to the array. Then it moves `right` across the rest of the input, adds the entering value and subtracts the leaving one. The invariant is that, after each update, `cnt[1]` equals the number of ones in `bits[right - k + 1 .. right]`, so the method reads the answer from `cnt[1]`.

**Complexity.**
- **Time** is O(n), because each index enters the count array once and leaves it at most once.
- **Space** is O(1) beyond the output, because the count array has two entries.

```java run
import java.util.Random;

public final class BinaryCounts {
    /**
     * Returns the number of ones in every length-k block of bits.
     * Time: O(n), one fill pass and one slide pass.
     * Space: O(1) beyond the output, a count array of size 2.
     * Invariant: cnt[v] counts the values equal to v in the current window.
     */
    static int[] onesPerBlock(int[] bits, int k) {
        // One entry per possible value; cnt[1] is the answer for a window.
        int[] cnt = new int[2];
        // Fill loop: k increments build the first window.
        for (int i = 0; i < k; i++) cnt[bits[i]]++;
        // One output entry per window start.
        int[] out = new int[bits.length - k + 1];
        out[0] = cnt[1];
        // Slide loop: one entering value and one leaving value per step.
        for (int right = k; right < bits.length; right++) {
            // The value at right enters the window.
            cnt[bits[right]]++;
            // The value at right - k leaves the window.
            cnt[bits[right - k]]--;
            // The window now starts at right - k + 1.
            out[right - k + 1] = cnt[1];
        }
        // Return one count per window.
        return out;
    }

    public static void main(String[] args) {
        // Example 1 and example 2 from the problem statement.
        if (!java.util.Arrays.equals(onesPerBlock(new int[] {1, 0, 1, 1, 0}, 3), new int[] {2, 2, 2})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(onesPerBlock(new int[] {0, 0, 0}, 3), new int[] {0})) throw new AssertionError("example 2");
        // Random binary arrays agree with a direct count per block.
        Random rnd = new Random(11);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(14), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            int[] want = new int[n - k + 1];
            for (int s = 0; s < want.length; s++) for (int i = s; i < s + k; i++) want[s] += a[i];
            if (!java.util.Arrays.equals(onesPerBlock(a, k), want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Find All Anagrams In A String (LeetCode 438)
<!-- id: sw-find-anagrams -->

**Approach.**
The method counts the letters of `p` once in `need`. It slides a window over `s` and keeps `have`, the letter counts of the window. For each `right`, it adds the entering letter and, once `right >= k`, it removes the letter at `right - k`. When the window is full, the method compares `have` with `need`, and equal arrays record the start `right - k + 1`. The invariant is that a full window's array equals the letter counts of `s[left..right]`, so equal arrays mean an anagram. A pattern longer than the text yields an empty list before any loop runs.

**Complexity.**
- **Time** is O(26 * n), which is O(n), because each of the `n` steps updates two entries and runs one 26-entry comparison.
- **Space** is O(1) beyond the output, because the method keeps two arrays of 26 entries.

```java run
import java.util.*;

public final class FindAnagrams {
    /**
     * Returns every start index whose length-|p| substring is an anagram of p.
     * Time: O(26 * n), one constant-size comparison per window.
     * Space: O(1) beyond the output, two arrays of 26 entries.
     * Invariant: for a full window, have equals the letter counts of s[right - k + 1 .. right].
     */
    static List<Integer> anagramStarts(String s, String p) {
        // The result list grows by one entry per hit.
        List<Integer> out = new ArrayList<>();
        int k = p.length();
        // A pattern longer than the text has no window, so the answer is empty.
        if (k > s.length()) return out;
        // need is fixed; have follows the window.
        int[] need = new int[26], have = new int[26];
        // Count the pattern once, k steps.
        for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
        // Each index of s enters the window exactly once.
        for (int right = 0; right < s.length(); right++) {
            // The entering letter raises its count.
            have[s.charAt(right) - 'a']++;
            // Once the window would exceed k letters, the letter at right - k leaves.
            if (right >= k) have[s.charAt(right - k) - 'a']--;
            // Test only full windows; Arrays.equals compares 26 entries, a constant cost.
            if (right >= k - 1 && Arrays.equals(have, need)) out.add(right - k + 1);
        }
        // Starts are added in increasing order because right increases.
        return out;
    }

    /** Oracle: sorts every substring and compares with the sorted pattern. */
    static List<Integer> oracle(String s, String p) {
        List<Integer> out = new ArrayList<>();
        char[] want = p.toCharArray();
        Arrays.sort(want);
        for (int st = 0; st + p.length() <= s.length(); st++) {
            char[] b = s.substring(st, st + p.length()).toCharArray();
            Arrays.sort(b);
            if (Arrays.equals(b, want)) out.add(st);
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: windows bac and cab are anagrams of abc.
        if (!anagramStarts("bacdcab", "abc").equals(List.of(0, 4))) throw new AssertionError("example 1");
        // Example 2: a pattern longer than the text returns an empty list.
        if (!anagramStarts("ab", "abc").isEmpty()) throw new AssertionError("example 2");
        // Random strings over a small alphabet agree with the sorting oracle.
        Random rnd = new Random(12);
        for (int t = 0; t < 3000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(14); i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0, m = 1 + rnd.nextInt(5); i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (!anagramStarts(a.toString(), b.toString()).equals(oracle(a.toString(), b.toString()))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Repeated Required Character (Author exercise)
<!-- id: sw-repeated-required -->

**Approach.**
The method uses the same two count arrays and stops at the first full window with equal arrays. The count of `a` in `need` is 2 for the pattern `aab`, so a window with a single `a` has a different array and fails the test. A test of membership, which records only whether each pattern letter occurs, would accept such a window. The method returns -1 when the loop ends without a hit. The invariant is the same as for the previous exercise.

**Complexity.**
- **Time** is O(26 * n), because each step makes a constant number of updates and one 26-entry comparison.
- **Space** is O(1), because the method keeps two arrays of 26 entries.

```java run
import java.util.*;

public final class RepeatedRequired {
    /**
     * Returns the smallest start of a window with the same letter counts as p, or -1.
     * Time: O(26 * n), one constant comparison per window.
     * Space: O(1), two arrays of 26 entries.
     * Invariant: for a full window, have equals the counts of s[right - k + 1 .. right].
     */
    static int firstStart(String s, String p) {
        int k = p.length();
        // No window exists when the pattern is longer than the text.
        if (k > s.length()) return -1;
        int[] need = new int[26], have = new int[26];
        // need records multiplicity, so the pattern aab gives need[a] = 2.
        for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
        // Slide loop: one entering letter per step.
        for (int right = 0; right < s.length(); right++) {
            have[s.charAt(right) - 'a']++;
            // The leaving letter appears once the window passes length k.
            if (right >= k) have[s.charAt(right - k) - 'a']--;
            // The first full window with equal counts is the smallest start.
            if (right >= k - 1 && Arrays.equals(have, need)) return right - k + 1;
        }
        // The loop finished without a hit.
        return -1;
    }

    /** Wrong test: only checks that each pattern letter occurs in the window. */
    static boolean membershipOnly(String window, String p) {
        for (char c : p.toCharArray()) if (window.indexOf(c) < 0) return false;
        return true;
    }

    /** Oracle: sorts every substring. */
    static int oracle(String s, String p) {
        char[] want = p.toCharArray();
        Arrays.sort(want);
        for (int st = 0; st + p.length() <= s.length(); st++) {
            char[] b = s.substring(st, st + p.length()).toCharArray();
            Arrays.sort(b);
            if (Arrays.equals(b, want)) return st;
        }
        return -1;
    }

    public static void main(String[] args) {
        // Example 1 and example 2 from the problem statement.
        if (firstStart("cabxaab", "aab") != 4) throw new AssertionError("example 1");
        if (firstStart("abcb", "aab") != -1) throw new AssertionError("example 2");
        // The membership test accepts the window "abc" for the pattern "aab", and the count test does not.
        if (!membershipOnly("abc", "aab")) throw new AssertionError("membership accepts abc");
        if (firstStart("abc", "aab") != -1) throw new AssertionError("counts reject abc");
        // Random strings agree with the oracle.
        Random rnd = new Random(13);
        for (int t = 0; t < 3000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(14); i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0, m = 1 + rnd.nextInt(5); i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (firstStart(a.toString(), b.toString()) != oracle(a.toString(), b.toString())) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Permutation In String (LeetCode 567)
<!-- id: sw-permutation-in-string -->

**Approach.**
The question asks whether any full window has the letter counts of the pattern. The method keeps the two count arrays of the previous exercises and returns `true` at the first full window whose arrays are equal. It returns `false` when the loop ends. The invariant is that a full window's array equals the counts of the window's letters, so one equal pair of arrays proves that a permutation exists.

**Complexity.**
- **Time** is O(26 * n), because each step updates two entries and compares 26 entries.
- **Space** is O(1), because the method keeps two arrays of 26 entries.

```java run
import java.util.*;

public final class PermutationInString {
    /**
     * Returns true when some substring of s is a permutation of p.
     * Time: O(26 * n), one constant comparison per full window.
     * Space: O(1), two arrays of 26 entries.
     * Invariant: for a full window, have holds the letter counts of the window.
     */
    static boolean containsPermutation(String p, String s) {
        int k = p.length();
        // A pattern longer than the text cannot fit in any window.
        if (k > s.length()) return false;
        int[] need = new int[26], have = new int[26];
        // Build the pattern counts once.
        for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
        // Slide loop over the entering index.
        for (int right = 0; right < s.length(); right++) {
            // Entering letter.
            have[s.charAt(right) - 'a']++;
            // Leaving letter, once the window is longer than k.
            if (right >= k) have[s.charAt(right - k) - 'a']--;
            // The first equal pair of arrays answers the question, so the method stops here.
            if (right >= k - 1 && Arrays.equals(have, need)) return true;
        }
        // No window matched.
        return false;
    }

    /** Oracle: sorts every substring. */
    static boolean oracle(String p, String s) {
        char[] want = p.toCharArray();
        Arrays.sort(want);
        for (int st = 0; st + p.length() <= s.length(); st++) {
            char[] b = s.substring(st, st + p.length()).toCharArray();
            Arrays.sort(b);
            if (Arrays.equals(b, want)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // Example 1: the substring "ba" is a permutation of "ab".
        if (!containsPermutation("ab", "xbax")) throw new AssertionError("example 1");
        // Example 2: no length-3 substring of "abba" has two a and one b.
        if (containsPermutation("aab", "abba")) throw new AssertionError("example 2");
        // Random strings agree with the oracle.
        Random rnd = new Random(14);
        for (int t = 0; t < 3000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(14); i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0, m = 1 + rnd.nextInt(5); i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (containsPermutation(b.toString(), a.toString()) != oracle(b.toString(), a.toString())) throw new AssertionError("random " + t);
        }
    }
}
```
