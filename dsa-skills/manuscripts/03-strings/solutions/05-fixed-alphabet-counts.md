<!-- solutions-for: 03-strings -->
### Solutions For Counting Letters

#### Solution: [Build] Vowel Counts (Author exercise)
<!-- id: st-vowel-counts -->

**Approach.**
One pass fills a 26-entry table, where `table[c - 'a']` holds how often the letter `c` occurs. After the pass, a fixed array of the five vowels names the table indexes to read, and the method copies those five entries into the answer. The invariant is that after index `i`, every table entry equals the occurrences of its letter in `s[0..i]`. The harness also asserts the lesson's text about the most frequent letter and the Java behaviors of the table.

**Complexity.**
- **Time** is O(n), because the loop reads each character once and the final copy reads 5 entries.
- **Space** is O(1), because the table holds 26 entries and the answer holds 5, whatever the length of `s`.

```java run
import java.util.Random;

public final class VowelCounts {
    /**
     * Counts a, e, i, o, u in a string of lowercase letters.
     * Time: O(n). Space: O(1), a 26-entry table.
     * Invariant: after index i, table[k] equals the occurrences of letter 'a' + k in s[0..i].
     */
    static int[] vowelCounts(String s) {
        // A new int array starts at 0, so the table needs no initialization loop.
        int[] table = new int[26];
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            // The offset 'a' maps the letters 'a' to 'z' onto the indexes 0 to 25.
            table[s.charAt(i) - 'a']++;
        }
        // The five vowels name the table slots that the answer reads.
        char[] vowels = {'a', 'e', 'i', 'o', 'u'};
        int[] answer = new int[5];
        for (int k = 0; k < 5; k++) {
            // Each answer entry reads one slot, so this loop costs 5 steps.
            answer[k] = table[vowels[k] - 'a'];
        }
        return answer;
    }

    /** Lesson code: the table-based most frequent letter. */
    static char mostFrequent(String s) {
        int[] table = new int[26];
        for (int i = 0; i < s.length(); i++) table[s.charAt(i) - 'a']++;
        int best = 0;
        for (int k = 1; k < 26; k++) if (table[k] > table[best]) best = k;
        return (char) ('a' + best);
    }

    /** Lesson code: the rescanning method, kept as the oracle for the table version. */
    static char naiveMostFrequent(String s) {
        char best = s.charAt(0);
        int bestTimes = 0;
        for (int i = 0; i < s.length(); i++) {
            int times = 0;
            for (int j = 0; j < s.length(); j++) if (s.charAt(j) == s.charAt(i)) times++;
            if (times > bestTimes || (times == bestTimes && s.charAt(i) < best)) { best = s.charAt(i); bestTimes = times; }
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!java.util.Arrays.equals(vowelCounts("mississippi"), new int[] {0, 0, 4, 0, 0})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(vowelCounts(""), new int[5])) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(vowelCounts("aeiouaa"), new int[] {3, 1, 1, 1, 1})) throw new AssertionError("all vowels");
        // Random strings are checked against a character-by-character oracle.
        Random rnd = new Random(51);
        for (int t = 0; t < 400; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(26)));
            String s = sb.toString();
            int[] expect = new int[5];
            for (char c : s.toCharArray()) { int p = "aeiou".indexOf(c); if (p >= 0) expect[p]++; }
            if (!java.util.Arrays.equals(vowelCounts(s), expect)) throw new AssertionError("random " + t);
        }
        // Lesson claim: the examples of the lesson text, including the tie that goes to the smaller letter.
        if (mostFrequent("banana") != 'a' || mostFrequent("cabab") != 'a') throw new AssertionError("lesson examples");
        if (naiveMostFrequent("banana") != 'a' || naiveMostFrequent("cabab") != 'a') throw new AssertionError("naive examples");
        for (int t = 0; t < 400; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(4)));
            if (mostFrequent(sb.toString()) != naiveMostFrequent(sb.toString())) throw new AssertionError("table against rescan " + sb);
        }
        // Lesson claim: the offset maps letters to 0 and 25, and the sums have type int, so a cast is needed.
        if ('a' - 'a' != 0 || 'z' - 'a' != 25 || 'c' - 'a' != 2) throw new AssertionError("offset");
        Object sum = 'a' + 1;
        if (!(sum instanceof Integer)) throw new AssertionError("int sum");
        if ((char) ('a' + 1) != 'b') throw new AssertionError("cast");
        // Lesson claim: a new int[26] is all zeros, and a character below 'a' indexes out of range.
        for (int v : new int[26]) if (v != 0) throw new AssertionError("zero fill");
        boolean threw = false;
        try { int[] probe = new int[26]; probe['A' - 'a']++; } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("out of range index");
    }
}
```

#### Solution: [Vary] Find The Difference (LeetCode 389)
<!-- id: st-find-difference -->

**Approach.**
One table serves both strings. The first pass increments the entry of each letter of `s`, and the second pass decrements the entry of each letter of `t`. A letter that appears the same number of times in both strings ends at 0. The extra letter of `t` ends at -1, because `t` has one more occurrence than `s`. A final scan over the 26 entries returns the letter whose entry is negative. The invariant is that after both passes, each entry equals the occurrences in `s` minus the occurrences in `t`.

**Complexity.**
- **Time** is O(n), because the passes read n and n + 1 characters and the scan reads 26 entries.
- **Space** is O(1), because the table has 26 entries.

```java run
import java.util.Random;

public final class FindDifference {
    /**
     * Returns the one letter that t holds more often than s.
     * Time: O(n). Space: O(1).
     * Invariant: after both passes, table[k] equals the count of letter k in s minus its count in t.
     */
    static char findDifference(String s, String t) {
        int[] table = new int[26];
        // The first pass adds the supply of every letter of s, which costs n steps.
        for (int i = 0; i < s.length(); i++) table[s.charAt(i) - 'a']++;
        // The second pass removes every letter of t, which costs n + 1 steps.
        for (int i = 0; i < t.length(); i++) table[t.charAt(i) - 'a']--;
        // Exactly one entry is -1, because t holds one extra occurrence of one letter.
        for (int k = 0; k < 26; k++) {
            if (table[k] < 0) return (char) ('a' + k);
        }
        // The contract guarantees an extra letter, so this line is unreachable for valid input.
        throw new IllegalArgumentException("no extra letter");
    }

    public static void main(String[] args) {
        // The statement examples.
        if (findDifference("xyz", "zqyx") != 'q') throw new AssertionError("example 1");
        if (findDifference("", "m") != 'm') throw new AssertionError("example 2");
        // The extra letter may repeat a letter of s.
        if (findDifference("aab", "baaa") != 'a') throw new AssertionError("repeated letter");
        // Random inputs are built by shuffling s and inserting a known extra letter.
        Random rnd = new Random(52);
        for (int tcase = 0; tcase < 600; tcase++) {
            int len = rnd.nextInt(8);
            StringBuilder sb = new StringBuilder();
            for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(5)));
            String s = sb.toString();
            char extra = (char) ('a' + rnd.nextInt(5));
            java.util.List<Character> chars = new java.util.ArrayList<>();
            for (char c : s.toCharArray()) chars.add(c);
            chars.add(rnd.nextInt(chars.size() + 1), extra);
            java.util.Collections.shuffle(chars, rnd);
            StringBuilder tb = new StringBuilder();
            for (char c : chars) tb.append(c);
            if (findDifference(s, tb.toString()) != extra) throw new AssertionError("random " + tcase);
        }
    }
}
```

#### Solution: [Boundary] Invalid Alphabet (Author exercise)
<!-- id: st-invalid-alphabet -->

**Approach.**
The loop checks each character against the range `'a'` to `'z'` before it computes the table index. A character outside the range returns `-1` at once, so no index outside 0 to 25 is ever formed. A valid character raises its entry, and the first time an entry becomes 1, a distinct counter grows by one. The empty string never enters the loop and returns 0. The invariant is that before each index, every earlier character is a lowercase letter and `distinct` equals the number of entries that are not zero.

**Complexity.**
- **Time** is O(n), because each character costs one range test and at most one table update.
- **Space** is O(1), because the table has 26 entries.

```java run
import java.util.Random;

public final class InvalidAlphabet {
    /**
     * Returns the number of distinct letters, or -1 when a character lies outside 'a' to 'z'.
     * Time: O(n). Space: O(1).
     * Invariant: before index i, all earlier characters are lowercase letters and distinct counts the nonzero entries.
     */
    static int distinctLetters(String s) {
        int[] table = new int[26];
        int distinct = 0;
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            // The range test runs before the subtraction, so the table index is always legal.
            if (c < 'a' || c > 'z') return -1;
            // A letter seen for the first time adds one to the distinct count.
            if (table[c - 'a'] == 0) distinct++;
            // The entry records that the letter has now occurred.
            table[c - 'a']++;
        }
        // Reaching the end proves that every character was a lowercase letter.
        return distinct;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (distinctLetters("abca") != 3) throw new AssertionError("example 1");
        if (distinctLetters("ab1") != -1) throw new AssertionError("example 2");
        // Empty input, the two characters just outside the range, and a bad character at the end.
        if (distinctLetters("") != 0) throw new AssertionError("empty");
        if (distinctLetters("`") != -1 || distinctLetters("{") != -1) throw new AssertionError("neighbors of the range");
        if (distinctLetters("abcdefghijklmnopqrstuvwxyz") != 26) throw new AssertionError("full alphabet");
        // The digit '1' maps to an index of -48, which is why the range test runs first.
        if ('1' - 'a' != -48) throw new AssertionError("digit index");
        // Random strings are checked against a set-based oracle.
        Random rnd = new Random(53);
        String pool = "abcz1A{`";
        for (int t = 0; t < 800; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(8);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            int expect = s.matches("[a-z]*") ? (int) s.chars().distinct().count() : -1;
            if (distinctLetters(s) != expect) throw new AssertionError("random " + t + " " + s);
        }
    }
}
```

#### Solution: [Recognize] Ransom Note (LeetCode 383)
<!-- id: st-ransom-note -->

**Approach.**
The first pass counts every letter of the magazine, so the table holds the supply of each letter. The second pass reads the note and consumes one unit of supply per letter. When an entry drops below 0, the note needs more of that letter than the magazine holds, and the method returns false at once. When the second pass ends without a negative entry, every letter of the note found its own position, so the method returns true. The invariant is that after index `i` of the note, each entry equals the magazine supply of its letter minus its use by `note[0..i]`.

**Complexity.**
- **Time** is O(m + n), where m and n are the magazine and note lengths, because each string is read once.
- **Space** is O(1), because the table has 26 entries.

```java run
import java.util.Random;

public final class RansomNote {
    /**
     * Returns true when every letter of note has its own position in magazine.
     * Time: O(m + n). Space: O(1).
     * Invariant: after note[0..i], table[k] equals the magazine supply of letter k minus its use so far.
     */
    static boolean canConstruct(String note, String magazine) {
        int[] table = new int[26];
        // The first pass records the supply of each letter, which costs m steps.
        for (int i = 0; i < magazine.length(); i++) table[magazine.charAt(i) - 'a']++;
        // The second pass consumes supply for each note letter, which costs at most n steps.
        for (int i = 0; i < note.length(); i++) {
            // A negative entry means the note needs a letter that the magazine ran out of.
            if (--table[note.charAt(i) - 'a'] < 0) return false;
        }
        // Every note letter found its own magazine position.
        return true;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!canConstruct("deed", "eddxe")) throw new AssertionError("example 1");
        if (canConstruct("noon", "onn")) throw new AssertionError("example 2");
        // Empty note, empty magazine and an exact match.
        if (!canConstruct("", "") || !canConstruct("", "abc")) throw new AssertionError("empty note");
        if (canConstruct("a", "")) throw new AssertionError("empty magazine");
        if (!canConstruct("abc", "cba")) throw new AssertionError("exact rearrangement");
        // Random pairs are checked against an oracle that removes one matching position at a time.
        Random rnd = new Random(54);
        for (int t = 0; t < 1000; t++) {
            String note = random(rnd), magazine = random(rnd);
            StringBuilder rest = new StringBuilder(magazine);
            boolean expect = true;
            for (char c : note.toCharArray()) {
                int p = rest.indexOf(String.valueOf(c));
                if (p < 0) { expect = false; break; }
                rest.deleteCharAt(p);
            }
            if (canConstruct(note, magazine) != expect) throw new AssertionError("random " + note + " " + magazine);
        }
    }

    static String random(Random r) {
        StringBuilder sb = new StringBuilder();
        int len = r.nextInt(7);
        for (int k = 0; k < len; k++) sb.append((char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```
