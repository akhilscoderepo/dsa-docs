<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Strings And Maps

#### Solution: [Build] First Unique Character In A String (LeetCode 387)
<!-- id: hm-first-unique-outside -->

**Approach.**
The method counts the letters of `s` in a 26-entry table and marks the letters of `t` in a 26-entry boolean table. A second pass over `s` returns the first index whose count is 1 and whose letter is not marked. The tables replace maps because the contract fixes the alphabet to lowercase letters. The scan reads the string and not the tables, because only the string knows the order. The invariant is that after the counting pass, `count[k]` equals the occurrences of the letter `'a' + k` in `s`, and `inT[k]` records whether `t` holds that letter.

**Complexity.**
- **Time** is O(n + m) for the lengths n of `s` and m of `t`, because each string is read once and each table access takes constant time.
- **Space** is O(1), because the two tables hold 26 entries each.

```java run
import java.util.*;

public final class FirstUniqueOutside {
    /**
     * Returns the first index whose letter occurs once in s and never in t, or -1.
     * Time: O(n + m). Space: O(1).
     * Invariant: after pass one, count[k] is the occurrences of 'a' + k in s and inT[k] says whether t holds it.
     */
    static int firstUniqueOutside(String s, String t) {
        int[] count = new int[26];
        boolean[] inT = new boolean[26];
        // Pass one: count the letters of s.
        for (int i = 0; i < s.length(); i++) count[s.charAt(i) - 'a']++;
        // Mark the letters of t.
        for (int i = 0; i < t.length(); i++) inT[t.charAt(i) - 'a'] = true;
        // Pass two follows the string order and tests both conditions.
        for (int i = 0; i < s.length(); i++) {
            int k = s.charAt(i) - 'a';
            if (count[k] == 1 && !inT[k]) {
                return i;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        // The statement examples and empty inputs.
        if (firstUniqueOutside("abcab", "b") != 2) throw new AssertionError("example 1");
        if (firstUniqueOutside("xyz", "x") != 1) throw new AssertionError("example 2");
        if (firstUniqueOutside("", "abc") != -1 || firstUniqueOutside("aabb", "") != -1) throw new AssertionError("empty and no unique");
        // Random strings are checked against a quadratic oracle.
        Random rnd = new Random(67);
        for (int t = 0; t < 600; t++) {
            String s = rand(rnd, 8), u = rand(rnd, 4);
            int expect = -1;
            for (int i = 0; i < s.length() && expect < 0; i++) {
                int c = 0;
                for (int j = 0; j < s.length(); j++) if (s.charAt(j) == s.charAt(i)) c++;
                if (c == 1 && u.indexOf(s.charAt(i)) < 0) expect = i;
            }
            if (firstUniqueOutside(s, u) != expect) throw new AssertionError(s + " | " + u);
        }
    }

    static String rand(Random r, int max) {
        StringBuilder sb = new StringBuilder();
        int len = r.nextInt(max);
        for (int i = 0; i < len; i++) sb.append((char) ('a' + r.nextInt(5)));
        return sb.toString();
    }
}
```

#### Solution: [Vary] Letter Changes For An Anagram (LeetCode 242)
<!-- id: hm-letter-changes -->

**Approach.**
The strings have equal length, so the surplus of one letter in `s` matches the deficit of another letter. A table holds `count in s - count in t` for each letter. Each letter with a positive difference needs that many replacements in `t`, and one replacement fixes exactly one unit of surplus. The answer is the sum of the positive differences. The sum is 0 exactly when every difference is 0, which is the anagram test. The invariant is that after both passes, `diff[k]` equals the count of `'a' + k` in `s` minus its count in `t`, and the entries sum to 0.

**Complexity.**
- **Time** is O(n), because the passes read each string once and the final sum reads 26 entries.
- **Space** is O(1), because the table has 26 entries.

```java run
import java.util.*;

public final class LetterChanges {
    /**
     * Returns the least number of replacements that make t an anagram of s.
     * Time: O(n). Space: O(1).
     * Invariant: diff[k] is the count of 'a' + k in s minus its count in t, and the entries sum to 0.
     */
    static int minChanges(String s, String t) {
        int[] diff = new int[26];
        // One pass adds the letters of s and subtracts the letters of t.
        for (int i = 0; i < s.length(); i++) {
            diff[s.charAt(i) - 'a']++;
            diff[t.charAt(i) - 'a']--;
        }
        int steps = 0;
        // Each unit of surplus in s needs one replacement in t.
        for (int d : diff) if (d > 0) steps += d;
        return steps;
    }

    public static void main(String[] args) {
        // The statement examples and the empty strings.
        if (minChanges("bab", "aba") != 1) throw new AssertionError("example 1");
        if (minChanges("abc", "cab") != 0) throw new AssertionError("example 2");
        if (minChanges("", "") != 0) throw new AssertionError("empty");
        // A string with no letter in common needs every position changed.
        if (minChanges("aaa", "bbb") != 3) throw new AssertionError("disjoint");
        // Random equal-length strings are checked against a brute force that tries every replacement set.
        Random rnd = new Random(68);
        for (int t = 0; t < 400; t++) {
            int n = rnd.nextInt(6);
            String s = rand(rnd, n), u = rand(rnd, n);
            if (minChanges(s, u) != brute(s, u)) throw new AssertionError(s + " | " + u);
        }
    }

    static String rand(Random r, int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) sb.append((char) ('a' + r.nextInt(3)));
        return sb.toString();
    }

    /** Smallest number of positions of t to rewrite so the multiset equals that of s, by trying all subsets. */
    static int brute(String s, String t) {
        int n = t.length(), best = Integer.MAX_VALUE;
        for (int mask = 0; mask < (1 << n); mask++) {
            // Letters of t that stay.
            int[] need = new int[26];
            for (char c : s.toCharArray()) need[c - 'a']++;
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) {
                if ((mask & (1 << i)) == 0 && --need[t.charAt(i) - 'a'] < 0) ok = false;
            }
            // The rewritten positions can take any letters, so the kept letters only have to fit inside s.
            if (ok) best = Math.min(best, Integer.bitCount(mask));
        }
        return best;
    }
}
```

#### Solution: [Boundary] Isomorphic Strings (LeetCode 205)
<!-- id: hm-isomorphic -->

**Approach.**
The method keeps a forward map from source character to target character and a reverse map from target character to source character. At each position, a stored target that differs from `t[i]` means a source character would split, and a stored source that differs from `s[i]` means two source characters would merge. Either case returns false. Otherwise the method stores the pairing in both maps. The invariant is that after position `i`, the two maps hold the same pairs in opposite directions, and the pairs form a bijection on the characters seen so far. Different lengths return false at once. The harness shows that a forward-only check accepts `"ab"` against `"cc"`.

**Complexity.**
- **Time** is O(n) on average, because each position makes two lookups and two stores of expected constant time.
- **Space** is O(d) for d distinct characters, at most O(n).

```java run
import java.util.*;

public final class IsomorphicStrings {
    /**
     * Reports whether s can be turned into t by a one-to-one replacement of characters.
     * Time: O(n) expected. Space: O(d).
     * Invariant: forward and reverse hold the same pairs in opposite directions, forming a bijection.
     */
    static boolean isomorphic(String s, String t) {
        if (s.length() != t.length()) return false;
        Map<Character, Character> forward = new HashMap<>();
        Map<Character, Character> reverse = new HashMap<>();
        // One iteration per position of both strings.
        for (int i = 0; i < s.length(); i++) {
            char a = s.charAt(i), b = t.charAt(i);
            Character mappedTo = forward.get(a);
            Character mappedFrom = reverse.get(b);
            // A different stored partner in either direction breaks the bijection.
            if ((mappedTo != null && mappedTo != b) || (mappedFrom != null && mappedFrom != a)) {
                return false;
            }
            forward.put(a, b);
            reverse.put(b, a);
        }
        return true;
    }

    /** The mistake: only the forward direction is checked. */
    static boolean forwardOnly(String s, String t) {
        if (s.length() != t.length()) return false;
        Map<Character, Character> forward = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            Character prev = forward.putIfAbsent(s.charAt(i), t.charAt(i));
            if (prev != null && prev != t.charAt(i)) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples and the lesson traces.
        if (!isomorphic("abca", "zbxz")) throw new AssertionError("example 1");
        if (isomorphic("ab", "cc")) throw new AssertionError("example 2");
        if (!isomorphic("egg", "add") || isomorphic("badc", "baba")) throw new AssertionError("lesson traces");
        if (!isomorphic("", "") || isomorphic("a", "")) throw new AssertionError("empty and length");
        // A forward-only check lets the merge through.
        if (!forwardOnly("ab", "cc")) throw new AssertionError("forward-only accepts a merge");
        // Java fact: a Character compared with a char unboxes, so equal letters compare equal.
        Character boxed = 'x';
        if (boxed != 'x') throw new AssertionError("unboxed comparison");
        // Random strings are checked against the quadratic pair test from the lesson.
        Random rnd = new Random(69);
        for (int t = 0; t < 800; t++) {
            int n = rnd.nextInt(7);
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0; i < n; i++) { a.append((char) ('a' + rnd.nextInt(3))); b.append((char) ('x' + rnd.nextInt(3))); }
            boolean expect = true;
            for (int i = 0; i < n; i++)
                for (int j = i + 1; j < n; j++)
                    if ((a.charAt(i) == a.charAt(j)) != (b.charAt(i) == b.charAt(j))) expect = false;
            if (isomorphic(a.toString(), b.toString()) != expect) throw new AssertionError(a + " | " + b);
        }
    }
}
```

#### Solution: [Recognize] Word Pattern (LeetCode 290)
<!-- id: hm-word-pattern -->

**Approach.**
The method splits `text` at single spaces into words. If the number of words differs from the length of `pattern`, the answer is false. The rest is the bijection check of the lesson, with words in place of the target characters. A map sends each pattern letter to its word, and a second map sends each word back to its letter. A conflict in either map returns false. The invariant is that after position `i`, the two maps hold the same pairs in opposite directions for the first `i + 1` letters and words. The words are `String` values, so the comparison uses `equals`, not `==`.

**Complexity.**
- **Time** is O(L) on average for a text of L characters. The split reads the text once, and each position makes map operations whose cost follows the word length.
- **Space** is O(L) for the words and the two maps.

```java run
import java.util.*;

public final class WordPattern {
    /**
     * Reports whether the words of text follow the letter pattern one to one.
     * Time: O(L) expected for L characters of text. Space: O(L).
     * Invariant: toWord and toLetter hold the same pairs in opposite directions for the processed prefix.
     */
    static boolean wordPattern(String pattern, String text) {
        String[] words = text.split(" ");
        // The counts must agree, or some letter has no word.
        if (words.length != pattern.length()) return false;
        Map<Character, String> toWord = new HashMap<>();
        Map<String, Character> toLetter = new HashMap<>();
        // One iteration per pattern letter and its word.
        for (int i = 0; i < words.length; i++) {
            char c = pattern.charAt(i);
            String w = words[i];
            String boundWord = toWord.get(c);
            Character boundLetter = toLetter.get(w);
            // equals compares the words by content, which == would not guarantee.
            if ((boundWord != null && !boundWord.equals(w)) || (boundLetter != null && boundLetter != c)) {
                return false;
            }
            toWord.put(c, w);
            toLetter.put(w, c);
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples and the length mismatch.
        if (!wordPattern("xyx", "red blue red")) throw new AssertionError("example 1");
        if (wordPattern("ab", "go go")) throw new AssertionError("example 2");
        if (wordPattern("aa", "go")) throw new AssertionError("fewer words than letters");
        if (!wordPattern("a", "go")) throw new AssertionError("single");
        // Two words with equal content built at run time still compare by equals.
        String built = new StringBuilder("g").append("o").toString();
        if (!wordPattern("aa", "go " + built)) throw new AssertionError("content equality");
        // Random inputs are checked against the quadratic pair test.
        Random rnd = new Random(70);
        String[] vocab = {"go", "no", "red", "blue"};
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(5);
            StringBuilder p = new StringBuilder(), tx = new StringBuilder();
            String[] ws = new String[n];
            for (int i = 0; i < n; i++) {
                p.append((char) ('a' + rnd.nextInt(3)));
                ws[i] = vocab[rnd.nextInt(vocab.length)];
                tx.append(i > 0 ? " " : "").append(ws[i]);
            }
            boolean expect = true;
            for (int i = 0; i < n; i++)
                for (int j = i + 1; j < n; j++)
                    if ((p.charAt(i) == p.charAt(j)) != ws[i].equals(ws[j])) expect = false;
            if (wordPattern(p.toString(), tx.toString()) != expect) throw new AssertionError(p + " | " + tx);
        }
    }
}
```
