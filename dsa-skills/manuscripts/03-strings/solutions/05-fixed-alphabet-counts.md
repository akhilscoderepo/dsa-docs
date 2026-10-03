<!-- solutions-for: 05-fixed-alphabet-counts -->
### Fixed Alphabet Counts

#### Solution: [Build] Vowel Counts (Author exercise)
<!-- id: st-vowel-counts -->

**Approach.** Allocate a 26-slot table, which Java fills with zeros, and add one at `c - 'a'` for every character. Then read the five vowel slots in the order `a`, `e`, `i`, `o`, `u`. Each letter picks its own counter, so no search is needed. The assertions compare with a per-vowel scan on random lowercase strings and check that the five counts never exceed the string length.

**Complexity.** O(n) time and O(1) space, with a fixed table of 26 slots.

```java run
import java.util.Arrays;
import java.util.Random;

public final class VowelCounts {
    static int[] vowelCounts(String s) {
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) count[s.charAt(i) - 'a']++;
        String vowels = "aeiou";
        int[] out = new int[5];
        for (int v = 0; v < 5; v++) out[v] = count[vowels.charAt(v) - 'a'];
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(vowelCounts("education"), new int[] {1, 1, 1, 1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(vowelCounts("banana"), new int[] {3, 0, 0, 0, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(vowelCounts(""), new int[5])) throw new AssertionError("empty string");
        Random rnd = new Random(241);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(30);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(26)));
            String s = sb.toString();
            int[] got = vowelCounts(s);
            int total = 0;
            for (int v = 0; v < 5; v++) {
                int expected = 0;
                for (int i = 0; i < s.length(); i++) if (s.charAt(i) == "aeiou".charAt(v)) expected++;
                if (got[v] != expected) throw new AssertionError("vowel " + v + " on " + s);
                total += got[v];
            }
            if (total > s.length()) throw new AssertionError("vowels cannot outnumber characters");
        }
    }
}
```

#### Solution: [Vary] Find the Difference (LeetCode 389)
<!-- id: st-find-difference -->

**Approach.** Share one table between the two strings: add one at each letter's slot for `s` and subtract one for `t`. Every letter that appears equally often in both returns to zero. The extra letter of `t` is left at minus one, so the one nonzero slot names it. The assertions build random pairs by shuffling a string and inserting one extra letter, and check that the method returns that letter, including when the extra letter already occurs in `s`.

**Complexity.** O(n) time and O(1) space.

```java run
import java.util.Random;

public final class FindDifference {
    static char findDifference(String s, String t) {
        int[] net = new int[26];
        for (int i = 0; i < s.length(); i++) net[s.charAt(i) - 'a']++;
        for (int i = 0; i < t.length(); i++) net[t.charAt(i) - 'a']--;
        for (int c = 0; c < 26; c++) if (net[c] != 0) return (char) ('a' + c);
        throw new IllegalStateException("the strings do not differ");
    }

    public static void main(String[] args) {
        if (findDifference("abcd", "dbcea") != 'e') throw new AssertionError("example 1");
        if (findDifference("aab", "abaa") != 'a') throw new AssertionError("example 2");
        if (findDifference("", "z") != 'z') throw new AssertionError("empty first string");
        Random rnd = new Random(242);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(12);
            char[] base = new char[n];
            for (int i = 0; i < n; i++) base[i] = (char) ('a' + rnd.nextInt(4));
            char extra = (char) ('a' + rnd.nextInt(4));
            char[] shuffled = new char[n + 1];
            System.arraycopy(base, 0, shuffled, 0, n);
            shuffled[n] = extra;
            for (int i = n; i > 0; i--) { int j = rnd.nextInt(i + 1); char tmp = shuffled[i]; shuffled[i] = shuffled[j]; shuffled[j] = tmp; }
            if (findDifference(new String(base), new String(shuffled)) != extra) throw new AssertionError("expected " + extra);
        }
    }
}
```

#### Solution: [Boundary] Invalid Alphabet (Author exercise)
<!-- id: st-invalid-alphabet -->

**Approach.** Check that each character lies between `'a'` and `'z'` before it is used as an index. The method rejects a bad character by throwing an `IllegalArgumentException` whose message names the character and its index, and it validates before updating, so no count is half-written. The documented contract is that input outside the declared alphabet is rejected. The unchecked version fails differently for each bad character: `'B'` gives the index -31, `'{'` gives 26, one past the end, and `'é'` gives a large index, and each is an out-of-bounds exception that does not name the real problem. The assertions exercise all of these.

**Complexity.** O(n) time and O(1) space.

```java run
import java.util.Arrays;

public final class InvalidAlphabet {
    static int[] letterCounts(String s) {
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c < 'a' || c > 'z') throw new IllegalArgumentException("character '" + c + "' at index " + i + " is outside a-z");
            count[c - 'a']++;
        }
        return count;
    }
    static int[] unchecked(String s) {
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) count[s.charAt(i) - 'a']++;
        return count;
    }

    public static void main(String[] args) {
        int[] ok = letterCounts("ab");
        if (ok[0] != 1 || ok[1] != 1 || Arrays.stream(ok).sum() != 2) throw new AssertionError("example 1");
        try {
            letterCounts("aB");
            throw new AssertionError("example 2 must be rejected");
        } catch (IllegalArgumentException e) {
            if (!e.getMessage().contains("'B'") || !e.getMessage().contains("index 1")) throw new AssertionError("the message must name the character and index: " + e.getMessage());
        }
        if ('B' - 'a' != -31) throw new AssertionError("'B' maps to -31");
        if ('{' - 'a' != 26) throw new AssertionError("'{' maps to 26, one past the table");
        for (String bad : new String[] {"B", "{", "é"}) {
            boolean threw = false;
            try { unchecked(bad); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
            if (!threw) throw new AssertionError("the unchecked version must fail on " + bad);
        }
        if (Arrays.stream(letterCounts("")).sum() != 0) throw new AssertionError("empty input");
    }
}
```

#### Solution: [Recognize] Ransom Note (LeetCode 383)
<!-- id: st-ransom-note -->

**Approach.** Count the magazine in a 26-slot table, then walk the note and subtract one from the slot of each letter. If a slot becomes negative, the magazine has run out of that letter, so return false at once, since no later letter can restore the count. If the note finishes, return true. The assertions compare with the tile-hunting search from the lesson on random strings over a small alphabet, where shortages are common.

**Complexity.** O(n + m) time and O(1) space.

```java run
import java.util.Random;

public final class RansomNote {
    static boolean canConstruct(String note, String magazine) {
        int[] count = new int[26];
        for (int i = 0; i < magazine.length(); i++) count[magazine.charAt(i) - 'a']++;
        for (int i = 0; i < note.length(); i++) if (--count[note.charAt(i) - 'a'] < 0) return false;
        return true;
    }
    static boolean oracle(String note, String magazine) {
        char[] tiles = magazine.toCharArray();
        for (int i = 0; i < note.length(); i++) {
            boolean found = false;
            for (int j = 0; j < tiles.length; j++) if (tiles[j] == note.charAt(i)) { tiles[j] = '#'; found = true; break; }
            if (!found) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        if (!canConstruct("aabc", "cbaaaz")) throw new AssertionError("example 1");
        if (canConstruct("xyy", "yxz")) throw new AssertionError("example 2");
        if (canConstruct("a", "b")) throw new AssertionError("missing letter");
        Random rnd = new Random(243);
        int yes = 0, no = 0;
        for (int t = 0; t < 6000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            int n = 1 + rnd.nextInt(6), m = 1 + rnd.nextInt(10);
            for (int i = 0; i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0; i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            boolean got = canConstruct(a.toString(), b.toString());
            if (got != oracle(a.toString(), b.toString())) throw new AssertionError("disagrees on " + a + " from " + b);
            if (got) yes++; else no++;
        }
        if (yes == 0 || no == 0) throw new AssertionError("random inputs must cover both outcomes");
    }
}
```
