<!-- solutions-for: 08-strings-and-maps -->
### Strings And Maps

#### Solution: [Build] First Unique Character in a String (LeetCode 387)
<!-- id: hm-first-unique-letter -->

**Approach.** Count each character in a `LinkedHashMap`, which remembers the order in which keys were first inserted and keeps that order when a later count is updated. Then iterate over the entries and return the first key whose count is 1, or the underscore if none exists. The order of the answer comes from the map and not from a second pass over the string. The oracle recounts each character by a nested loop and takes the first one with a count of one, and the assertions compare on random strings, plus a check that updating a count does not move the key.

**Complexity.** Expected O(n) time and O(k) extra space for `k` distinct characters.

```java run
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Random;

public final class FirstUniqueLetter {
    static char firstUniqueChar(String s) {
        Map<Character, Integer> count = new LinkedHashMap<>();
        for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
        for (Map.Entry<Character, Integer> e : count.entrySet()) {
            if (e.getValue() == 1) return e.getKey();
        }
        return '_';
    }
    static char oracle(String s) {
        for (int i = 0; i < s.length(); i++) {
            int times = 0;
            for (int j = 0; j < s.length(); j++) if (s.charAt(j) == s.charAt(i)) times++;
            if (times == 1) return s.charAt(i);
        }
        return '_';
    }

    public static void main(String[] args) {
        if (firstUniqueChar("level") != 'v') throw new AssertionError("example 1");
        if (firstUniqueChar("noon") != '_') throw new AssertionError("example 2");
        if (firstUniqueChar("") != '_') throw new AssertionError("empty string");
        Map<Character, Integer> m = new LinkedHashMap<>();
        m.put('z', 1); m.put('a', 1); m.merge('z', 1, Integer::sum);
        if (m.keySet().iterator().next() != 'z') throw new AssertionError("updating a count keeps the first-seen order");
        Random rnd = new Random(111);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(12);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(5)));
            String s = sb.toString();
            if (firstUniqueChar(s) != oracle(s)) throw new AssertionError("disagrees with the recount on " + s);
        }
    }
}
```

#### Solution: [Vary] Valid Anagram (LeetCode 242)
<!-- id: hm-anagram-ledger -->

**Approach.** Walk both strings together. For each position add one to the first character's entry and subtract one from the second character's entry, removing an entry whenever its count reaches zero. After the walk, every character has matched in both strings exactly when no entry is left, so the map is empty. If zero-count entries were kept, the map would not be empty even for true anagrams, and the assertions show that. Different lengths are rejected first. The oracle sorts both strings and compares them, and the assertions agree on random strings over a small alphabet.

**Complexity.** Expected O(n) time and O(k) extra space.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class AnagramLedger {
    static void bump(Map<Character, Integer> ledger, char c, int delta) {
        int now = ledger.getOrDefault(c, 0) + delta;
        if (now == 0) ledger.remove(c); else ledger.put(c, now);
    }
    static boolean sameLetters(String a, String b) {
        if (a.length() != b.length()) return false;
        Map<Character, Integer> ledger = new HashMap<>();
        for (int i = 0; i < a.length(); i++) {
            bump(ledger, a.charAt(i), 1);
            bump(ledger, b.charAt(i), -1);
        }
        return ledger.isEmpty();
    }
    static boolean keepsZeros(String a, String b) {
        Map<Character, Integer> ledger = new HashMap<>();
        for (int i = 0; i < a.length(); i++) {
            ledger.merge(a.charAt(i), 1, Integer::sum);
            ledger.merge(b.charAt(i), -1, Integer::sum);
        }
        return ledger.isEmpty();
    }
    static boolean oracle(String a, String b) {
        char[] x = a.toCharArray(), y = b.toCharArray();
        Arrays.sort(x);
        Arrays.sort(y);
        return Arrays.equals(x, y);
    }

    public static void main(String[] args) {
        if (!sameLetters("dusty", "study")) throw new AssertionError("example 1");
        if (sameLetters("abca", "abcc")) throw new AssertionError("example 2");
        if (keepsZeros("dusty", "study")) throw new AssertionError("a ledger that keeps zero entries is never empty for true anagrams");
        if (!sameLetters("", "")) throw new AssertionError("empty strings");
        Random rnd = new Random(112);
        for (int t = 0; t < 4000; t++) {
            StringBuilder x = new StringBuilder(), y = new StringBuilder();
            int n = rnd.nextInt(8);
            for (int i = 0; i < n; i++) x.append((char) ('a' + rnd.nextInt(3)));
            int m = rnd.nextInt(4) == 0 ? rnd.nextInt(8) : n;
            for (int i = 0; i < m; i++) y.append((char) ('a' + rnd.nextInt(3)));
            if (sameLetters(x.toString(), y.toString()) != oracle(x.toString(), y.toString())) throw new AssertionError("disagrees with the sort oracle");
        }
    }
}
```

#### Solution: [Boundary] Isomorphic Strings (LeetCode 205)
<!-- id: hm-isomorphic-strings -->

**Approach.** Keep a forward map from characters of the first string to characters of the second and a backward map in the other direction. At each position, an existing forward entry must equal the second character and an existing backward entry must equal the first character. If both checks pass, both entries are written. A forward map alone would accept `ab` against `cc`, because `a` and `b` each map consistently to `c`, and the assertions show that. The oracle tests every pair of positions for agreement in both strings, and the assertions compare the two on random strings.

**Complexity.** Expected O(n) time and O(k) extra space.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class IsomorphicStrings {
    static boolean isIsomorphic(String s, String t) {
        if (s.length() != t.length()) return false;
        Map<Character, Character> forward = new HashMap<>(), backward = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            char a = s.charAt(i), b = t.charAt(i);
            Character f = forward.get(a), g = backward.get(b);
            if (f != null && f != b) return false;
            if (g != null && g != a) return false;
            forward.put(a, b);
            backward.put(b, a);
        }
        return true;
    }
    static boolean forwardOnly(String s, String t) {
        Map<Character, Character> forward = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            Character f = forward.get(s.charAt(i));
            if (f != null && f != t.charAt(i)) return false;
            forward.put(s.charAt(i), t.charAt(i));
        }
        return true;
    }
    static boolean oracle(String s, String t) {
        if (s.length() != t.length()) return false;
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 1; j < s.length(); j++)
                if ((s.charAt(i) == s.charAt(j)) != (t.charAt(i) == t.charAt(j))) return false;
        return true;
    }

    public static void main(String[] args) {
        if (!isIsomorphic("gaga", "xyxy")) throw new AssertionError("example 1");
        if (isIsomorphic("ab", "cc")) throw new AssertionError("example 2");
        if (!forwardOnly("ab", "cc")) throw new AssertionError("a forward map alone accepts two characters sharing one replacement");
        if (isIsomorphic("ab", "c")) throw new AssertionError("different lengths");
        Random rnd = new Random(113);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(8);
            StringBuilder x = new StringBuilder(), y = new StringBuilder();
            for (int i = 0; i < n; i++) { x.append((char) ('a' + rnd.nextInt(3))); y.append((char) ('p' + rnd.nextInt(3))); }
            if (isIsomorphic(x.toString(), y.toString()) != oracle(x.toString(), y.toString())) throw new AssertionError("disagrees with the pair check");
        }
    }
}
```

#### Solution: [Recognize] Word Pattern (LeetCode 290)
<!-- id: hm-word-pattern -->

**Approach.** Split the sentence into words and require the same count as the pattern letters. Then run the two-map pairing check with letters as the first key type and words as the second, comparing words with `equals`. Equal letters must map to equal words, and different letters to different words. The oracle turns both the pattern and the word list into sequences of first-occurrence numbers, so that `xyx` and `up down up` both become `0 1 0`, and compares those sequences. The assertions agree on random patterns and sentences built from a small vocabulary.

**Complexity.** Expected O(n + L) time for the pattern length `n` and the total sentence length `L`, and O(n) extra space.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class WordPattern {
    static boolean wordPattern(String pattern, String sentence) {
        String[] words = sentence.split(" ");
        if (pattern.length() != words.length) return false;
        Map<Character, String> forward = new HashMap<>();
        Map<String, Character> backward = new HashMap<>();
        for (int i = 0; i < words.length; i++) {
            char p = pattern.charAt(i);
            String w = words[i];
            String f = forward.get(p);
            Character g = backward.get(w);
            if (f != null && !f.equals(w)) return false;
            if (g != null && g != p) return false;
            forward.put(p, w);
            backward.put(w, p);
        }
        return true;
    }
    static <T> List<Integer> shape(List<T> items) {
        Map<T, Integer> first = new HashMap<>();
        List<Integer> out = new ArrayList<>();
        for (T item : items) {
            first.putIfAbsent(item, first.size());
            out.add(first.get(item));
        }
        return out;
    }
    static boolean oracle(String pattern, String sentence) {
        List<Character> letters = new ArrayList<>();
        for (char c : pattern.toCharArray()) letters.add(c);
        List<String> words = List.of(sentence.split(" "));
        return letters.size() == words.size() && shape(letters).equals(shape(words));
    }

    public static void main(String[] args) {
        if (!wordPattern("xyx", "up down up")) throw new AssertionError("example 1");
        if (wordPattern("ab", "hot hot")) throw new AssertionError("example 2");
        if (wordPattern("ab", "hot")) throw new AssertionError("different counts");
        if (wordPattern("aa", "hot cold")) throw new AssertionError("one letter, two words");
        String[] vocab = {"up", "down", "left", "right"};
        Random rnd = new Random(114);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(6);
            StringBuilder p = new StringBuilder(), s = new StringBuilder();
            for (int i = 0; i < n; i++) {
                p.append((char) ('a' + rnd.nextInt(3)));
                if (i > 0) s.append(' ');
                s.append(vocab[rnd.nextInt(vocab.length)]);
            }
            if (wordPattern(p.toString(), s.toString()) != oracle(p.toString(), s.toString())) throw new AssertionError("disagrees with the shape oracle");
        }
    }
}
```
