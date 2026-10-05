<!-- solutions-for: 08-two-pointers -->
### Solutions For Checking Strings From Both Ends

#### Solution: [Build] Valid Palindrome (LeetCode 125)
<!-- id: tp-valid-palindrome -->

**Approach.**
One pointer starts at each end of the string. Before a comparison, each pointer moves past characters that are not letters or digits, and the guard `left < right` stops the inner loops at the other pointer. The two counted characters are compared in lowercase, and the first difference returns `false`. When the pointers meet, every counted pair has matched. The invariant is that all counted pairs outside the range from `left` to `right` matched. A string with no counted character never compares a pair and returns `true`.

**Complexity.**
- **Time** is O(n), because each pointer moves in one direction and every character is visited at most once.
- **Space** is O(1), because the scan creates no new string.

```java run
import java.util.Random;

public final class ValidPalindrome125 {
    /**
     * Returns true when the letters and digits of s read the same in both directions, ignoring case.
     * Time: O(n).
     * Space: O(1).
     * Invariant: all counted pairs outside [left, right] matched.
     */
    static boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        // The outer loop ends when the pointers meet, so each pair is compared once.
        while (left < right) {
            // Skip ignored characters on the left; the guard keeps left in range.
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
            // Skip ignored characters on the right.
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
            // Compare the counted pair in lowercase.
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) return false;
            left++;
            right--;
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!isPalindrome("Madam, I'm Adam")) throw new AssertionError("example 1");
        if (isPalindrome("Ab, 9a")) throw new AssertionError("example 2");
        // The underscore is not counted, and a string without counted characters passes.
        if (!isPalindrome("a_a") || !isPalindrome("  ") || !isPalindrome("")) throw new AssertionError("ignored");
        if (Character.isLetterOrDigit('_')) throw new AssertionError("underscore");
        // Random strings against the clean-and-reverse method.
        Random rnd = new Random(91);
        String alphabet = "aAbB1 ,_";
        for (int t = 0; t < 5000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(10);
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            StringBuilder clean = new StringBuilder();
            for (char c : s.toCharArray()) if (Character.isLetterOrDigit(c)) clean.append(Character.toLowerCase(c));
            boolean expect = clean.toString().equals(new StringBuilder(clean).reverse().toString());
            if (isPalindrome(s) != expect) throw new AssertionError("random '" + s + "'");
        }
    }
}
```

#### Solution: [Vary] Reverse String (LeetCode 344)
<!-- id: tp-reverse-chars -->

**Approach.**
A `String` cannot be edited, so the input is a `char[]`. The left pointer starts at the first slot and the right pointer at the last slot, and each round swaps the two characters and moves both pointers inward. The loop stops when `left >= right`, so the middle element of an odd length is never swapped with itself. The invariant is that the slots outside the range from `left` to `right` already hold the reversed pair values.

**Complexity.**
- **Time** is O(n), because the loop makes `n / 2` swaps.
- **Space** is O(1), because the swap uses one temporary variable.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ReverseChars344 {
    /**
     * Reverses chars in place.
     * Time: O(n).
     * Space: O(1).
     * Invariant: slots outside [left, right] hold their final values.
     */
    static void reverse(char[] chars) {
        int left = 0, right = chars.length - 1;
        // Each round settles two slots, so the loop runs n / 2 times.
        while (left < right) {
            char tmp = chars[left];
            chars[left] = chars[right];
            chars[right] = tmp;
            left++;
            right--;
        }
    }

    public static void main(String[] args) {
        // The statement examples.
        char[] a = {'d', 'o', 'g', 's'};
        reverse(a);
        if (!Arrays.equals(a, new char[] {'s', 'g', 'o', 'd'})) throw new AssertionError("example 1");
        char[] b = {'x'};
        reverse(b);
        if (!Arrays.equals(b, new char[] {'x'})) throw new AssertionError("example 2");
        // The empty array.
        char[] e = new char[0];
        reverse(e);
        // Random arrays against StringBuilder.reverse for characters in the Basic Multilingual Plane.
        Random rnd = new Random(92);
        for (int t = 0; t < 4000; t++) {
            char[] x = new char[rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = (char) ('a' + rnd.nextInt(26));
            char[] y = x.clone();
            reverse(y);
            if (!new String(y).equals(new StringBuilder(new String(x)).reverse().toString())) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Valid Palindrome II (LeetCode 680)
<!-- id: tp-palindrome-one-delete -->

**Approach.**
The scan compares symmetric pairs from the two ends. At the first mismatch it has used up the single deletion, so it tests two cases. In the first case the left character is removed, which means the range from `left + 1` to `right` must be a palindrome. In the second case the right character is removed, so the range from `left` to `right - 1` must be a palindrome. Each test is a plain two-pointer check. Only the first mismatch needs the repair, because any later mismatch would need a second deletion. The invariant is that all pairs outside the range matched without a deletion.

**Complexity.**
- **Time** is O(n), because the main scan is linear and the two checks scan at most `n` characters in total.
- **Space** is O(1), because the checks use indexes on the original string.

```java run
import java.util.Random;

public final class PalindromeOneDelete680 {
    /**
     * Returns true when s is a palindrome after deleting at most one character.
     * Time: O(n).
     * Space: O(1).
     * Invariant: all pairs outside [left, right] matched without a deletion.
     */
    static boolean validAfterOneDelete(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            // At the first mismatch the single deletion is spent on one of the two ends.
            if (s.charAt(left) != s.charAt(right)) {
                return isPalin(s, left + 1, right) || isPalin(s, left, right - 1);
            }
            left++;
            right--;
        }
        return true;
    }

    /** Plain palindrome check on the inclusive range [i, j]. */
    static boolean isPalin(String s, int i, int j) {
        while (i < j) {
            if (s.charAt(i) != s.charAt(j)) return false;
            i++;
            j--;
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!validAfterOneDelete("abcddcbea")) throw new AssertionError("example 1");
        if (validAfterOneDelete("abc")) throw new AssertionError("example 2");
        // Short strings: one letter, two letters.
        if (!validAfterOneDelete("a") || !validAfterOneDelete("ab")) throw new AssertionError("short");
        // Random strings against trying every single deletion.
        Random rnd = new Random(93);
        for (int t = 0; t < 5000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(9);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            boolean expect = s.equals(new StringBuilder(s).reverse().toString());
            for (int i = 0; i < n && !expect; i++) {
                String d = s.substring(0, i) + s.substring(i + 1);
                if (d.equals(new StringBuilder(d).reverse().toString())) expect = true;
            }
            if (validAfterOneDelete(s) != expect) throw new AssertionError("random " + s);
        }
    }
}
```

#### Solution: [Recognize] Is Subsequence (LeetCode 392)
<!-- id: tp-is-subsequence -->

**Approach.**
The pointer `i` walks through `t` and moves every round. The pointer `j` points into `s` and moves only when `t.charAt(i)` equals `s.charAt(j)`. Both pointers move to the right, and no pair of mirrored positions is compared. The greedy match is safe because taking the earliest matching character of `t` leaves the longest remaining part of `t` for the rest of `s`. When `j` reaches the length of `s`, every character of `s` found a match in order. The invariant is that `s[0..j-1]` is a subsequence of `t[0..i-1]` and `j` is as large as possible.

**Complexity.**
- **Time** is O(|t|), because `i` visits each character of `t` once.
- **Space** is O(1), because the method keeps two indexes.

```java run
import java.util.Random;

public final class IsSubsequence392 {
    /**
     * Returns true when s is a subsequence of t.
     * Time: O(|t|).
     * Space: O(1).
     * Invariant: s[0..j-1] is the longest prefix of s that is a subsequence of t[0..i-1].
     */
    static boolean isSubsequence(String s, String t) {
        int j = 0;
        // i moves every round, so the loop costs |t| steps.
        for (int i = 0; i < t.length() && j < s.length(); i++) {
            // j moves only on a match, so unmatched characters of t are skipped.
            if (t.charAt(i) == s.charAt(j)) j++;
        }
        return j == s.length();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!isSubsequence("ace", "abcde")) throw new AssertionError("example 1");
        if (isSubsequence("aec", "abcde")) throw new AssertionError("example 2");
        // The empty pattern matches every text, and a nonempty pattern fails on the empty text.
        if (!isSubsequence("", "xyz") || !isSubsequence("", "") || isSubsequence("a", "")) throw new AssertionError("empty");
        // Random strings against a check over every subset of positions of t.
        Random rnd = new Random(94);
        for (int t = 0; t < 4000; t++) {
            int m = rnd.nextInt(4), n = rnd.nextInt(9);
            StringBuilder sb = new StringBuilder(), tb = new StringBuilder();
            for (int i = 0; i < m; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0; i < n; i++) tb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString(), tt = tb.toString();
            boolean expect = false;
            for (int mask = 0; mask < (1 << n) && !expect; mask++) {
                StringBuilder pick = new StringBuilder();
                for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) pick.append(tt.charAt(i));
                if (pick.toString().equals(s)) expect = true;
            }
            if (isSubsequence(s, tt) != expect) throw new AssertionError("random " + s + " " + tt);
        }
    }
}
```
