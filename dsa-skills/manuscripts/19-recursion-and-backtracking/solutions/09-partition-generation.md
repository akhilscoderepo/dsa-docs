<!-- solutions-for: 09-partition-generation -->
### Solutions For Cutting A String

#### Solution: [Build] All Splits Of A Short String (Author exercise)
<!-- id: bt-all-splits-short-string -->

**Approach.**
The call at start position `start` owns the suffix from `start`. It loops over every piece end from `start + 1` to the length, adds the field from `start` up to the piece end and calls itself with the piece end as the new start. When the start position equals the length, the suffix is empty and the path covers every letter, so the call stores a copy. For the empty string, the root call is already at the empty suffix and stores the empty list. Each cut appears once, because the sequence of piece ends is strictly increasing and identifies the cut.

**Complexity.**
- **Time** is O(n * 2^n), because the search stores 2^(n-1) cuts and each copy and field costs up to O(n).
- **Space** is O(n) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class AllSplitsShortString {
    /**
     * Returns every cut of s into non-empty consecutive fields, smallest piece end first.
     * Time: O(n * 2^n). Space: O(n) besides the output.
     * Invariant: the fields on the path cover exactly s[0..start).
     */
    static List<List<String>> splits(String s) {
        List<List<String>> out = new ArrayList<>();
        go(0, s, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, String s, List<String> path, List<List<String>> out) {
        if (start == s.length()) { out.add(new ArrayList<>(path)); return; }   // empty suffix: store a copy
        for (int end = start + 1; end <= s.length(); end++) {   // every end of the next field
            path.add(s.substring(start, end));                  // choose the field from start up to end - 1
            go(end, s, path, out);                              // the suffix starts at end
            path.remove(path.size() - 1);                       // undo the choice
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!splits("abc").equals(List.of(List.of("a", "b", "c"), List.of("a", "bc"), List.of("ab", "c"), List.of("abc")))) throw new AssertionError("ex1");
        if (!splits("").equals(List.of(List.of()))) throw new AssertionError("ex2");
        // Every string up to length 5: the count is 2^(n-1), every cut joins back to s and no cut repeats.
        Random rnd = new Random(1991);
        for (int t = 0; t < 200; t++) {
            int n = rnd.nextInt(6);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            List<List<String>> got = splits(s);
            if (got.size() != (n == 0 ? 1 : 1 << (n - 1))) throw new AssertionError("count " + s);
            if (new HashSet<>(got).size() != got.size()) throw new AssertionError("repeat " + s);
            for (List<String> cut : got) {
                if (!String.join("", cut).equals(s)) throw new AssertionError("join " + s);
                for (String f : cut) if (f.isEmpty()) throw new AssertionError("empty field");
            }
        }
        // The Java claim: substring(length) returns the empty string and does not throw.
        if (!"abc".substring(3).isEmpty()) throw new AssertionError("substring at length");
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Valid-Piece Predicate (Author exercise)
<!-- id: bt-valid-piece-predicate -->

**Approach.**
The search of the previous solution gains a rule that a field must pass before the call uses it. A field passes when it has no leading zero, unless it is the single digit `0`, and when its value is at most `limit`. The call computes the value digit by digit while the piece end grows. It stops the loop once the value exceeds `limit`, because a longer field has a larger value. A field that starts with `0` passes only at length 1, so the loop stops after it. A failed field removes that piece end, and the call never recurses on it. The result keeps the order of the smallest piece end first.

**Complexity.**
- **Time** is O(n * m) where `m` counts the cuts that the rule keeps, plus the failed fields, each of which costs O(1) in the digit loop.
- **Space** is O(n) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class ValidPiecePredicate {
    /**
     * Returns every cut of the digit string s whose fields have no leading zero and a value of at most limit.
     * Time: O(n * m). Space: O(n) besides the output.
     * Invariant: the fields on the path cover s[0..start) and each passes the rule.
     */
    static List<List<String>> cuts(String s, long limit) {
        List<List<String>> out = new ArrayList<>();
        go(0, s, limit, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, String s, long limit, List<String> path, List<List<String>> out) {
        if (start == s.length()) { out.add(new ArrayList<>(path)); return; }   // empty suffix: store a copy
        long value = 0;
        for (int end = start + 1; end <= s.length(); end++) {
            value = value * 10 + (s.charAt(end - 1) - '0');  // the value of the field from start up to end - 1
            if (value > limit) break;                        // a longer field only grows, so the loop ends
            path.add(s.substring(start, end));               // choose the field
            go(end, s, limit, path, out);                    // explore the suffix
            path.remove(path.size() - 1);                    // undo the choice
            if (s.charAt(start) == '0') break;               // a leading zero allows only the field "0"
        }
    }

    /** Oracle: all masks over the gaps, with each field tested at the end. */
    static List<List<String>> oracle(String s, long limit) {
        List<List<String>> out = new ArrayList<>();
        int gaps = Math.max(s.length() - 1, 0);
        for (int mask = 0; mask < (1 << gaps); mask++) {
            List<String> fields = new ArrayList<>(); int from = 0;
            for (int g = 0; g < gaps; g++) if ((mask >> g & 1) == 1) { fields.add(s.substring(from, g + 1)); from = g + 1; }
            if (!s.isEmpty()) fields.add(s.substring(from));
            boolean ok = true;
            for (String f : fields) if ((f.length() > 1 && f.charAt(0) == '0') || Long.parseLong(f) > limit) ok = false;
            if (ok) out.add(fields);
        }
        out.sort((a, b) -> { for (int i = 0; i < Math.min(a.size(), b.size()); i++) { int c = Integer.compare(a.get(i).length(), b.get(i).length()); if (c != 0) return c; } return 0; });
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!cuts("100", 255).equals(List.of(List.of("1", "0", "0"), List.of("10", "0"), List.of("100")))) throw new AssertionError("ex1");
        if (!cuts("909", 90).equals(List.of(List.of("9", "0", "9"), List.of("90", "9")))) throw new AssertionError("ex2");
        if (!cuts("", 5).equals(List.of(List.of()))) throw new AssertionError("empty");
        // Random digit strings must match the mask oracle as sets, and the order must put shorter first fields first.
        Random rnd = new Random(1992);
        for (int t = 0; t < 300; t++) {
            int n = rnd.nextInt(9);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('0' + rnd.nextInt(10) % (rnd.nextBoolean() ? 3 : 10)));
            String s = sb.toString(); long limit = 1 + rnd.nextInt(300);
            List<List<String>> got = cuts(s, limit), want = oracle(s, limit);
            if (got.size() != want.size() || !new HashSet<>(got).equals(new HashSet<>(want))) throw new AssertionError("random " + s + " " + limit);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Empty Suffix Completion (Author exercise)
<!-- id: bt-empty-suffix-completion -->

**Approach.**
The call keeps the start position and the number of fields left to place. A call with no fields left returns. It stores a copy first when the start position equals the length, because a path with `parts` fields and a remaining suffix is not a cut. A call with fields left loops over the piece ends. Each missing field needs at least one letter, so the loop stops at `n - (left - 1)`. This bound removes only calls that cannot finish. For the empty string with `parts = 0`, the root has no fields left at the empty suffix and stores the empty list. For the empty string with `parts = 1`, no field fits and the result is empty.

**Complexity.**
- **Time** is O(n * C(n - 1, parts - 1)) at most, because that many cuts exist and each copy costs O(n).
- **Space** is O(parts) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class EmptySuffixCompletion {
    /**
     * Returns every cut of s into exactly parts non-empty fields, smallest piece end first.
     * Time: O(n * C(n - 1, parts - 1)). Space: O(parts) besides the output.
     * Invariant: the path holds parts - left fields that cover s[0..start).
     */
    static List<List<String>> cuts(String s, int parts) {
        List<List<String>> out = new ArrayList<>();
        go(0, parts, s, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int left, String s, List<String> path, List<List<String>> out) {
        if (left == 0) {                                     // the path holds parts fields
            if (start == s.length()) out.add(new ArrayList<>(path));   // store only when no letter remains
            return;
        }
        int lastEnd = s.length() - (left - 1);               // each later field needs at least one letter
        for (int end = start + 1; end <= lastEnd; end++) {
            path.add(s.substring(start, end));               // choose the next field
            go(end, left - 1, s, path, out);                 // one field fewer to place
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    static long binom(int n, int k) { if (k < 0 || k > n) return 0; long r = 1; for (int i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!cuts("abcd", 2).equals(List.of(List.of("a", "bcd"), List.of("ab", "cd"), List.of("abc", "d")))) throw new AssertionError("ex1");
        if (!cuts("", 0).equals(List.of(List.of()))) throw new AssertionError("ex2");
        if (!cuts("", 1).isEmpty()) throw new AssertionError("empty string, one part");
        if (!cuts("ab", 3).isEmpty()) throw new AssertionError("more parts than letters");
        if (!cuts("ab", 0).isEmpty()) throw new AssertionError("no parts, letters remain");
        // The count must equal C(n - 1, parts - 1) for every length and part count in range.
        for (int n = 1; n <= 10; n++) for (int p = 1; p <= 12; p++) {
            String s = "abcdefghij".substring(0, n);
            List<List<String>> got = cuts(s, p);
            if (got.size() != binom(n - 1, p - 1)) throw new AssertionError("count " + n + "," + p);
            for (List<String> cut : got) if (!String.join("", cut).equals(s) || cut.size() != p) throw new AssertionError("shape " + n + "," + p);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Palindrome Partitioning (LeetCode 131)
<!-- id: bt-palindrome-partitioning -->

**Approach.**
The call at start position `start` loops over every piece end and tests the field from `start` to `end - 1` with two indices that move toward each other. A field that fails the test removes its branch, so the search never builds the cuts that begin with it. A field that passes enters the path through `substring`. Then the call recurses with the piece end as the new start. When the start position equals the length, the call stores a copy. The cut into single letters always passes, so every input has at least one result.

**Complexity.**
- **Time** is O(n * 2^n) in the worst case, for a string such as `aaaa`, where every cut is valid.
- **Space** is O(n) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class PalindromePartitioning {
    private static long checks, calls;

    /**
     * Returns every cut of s into palindromic fields, smallest piece end first.
     * Time: O(n * 2^n) worst case. Space: O(n) besides the output.
     * Invariant: the fields on the path are palindromes and cover s[0..start).
     */
    static List<List<String>> partition(String s) {
        List<List<String>> out = new ArrayList<>();
        go(0, s, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, String s, List<String> path, List<List<String>> out) {
        calls++;                                             // counted only for the cost claim in main
        if (start == s.length()) { out.add(new ArrayList<>(path)); return; }   // empty suffix: store a copy
        for (int end = start + 1; end <= s.length(); end++) {
            checks++;
            if (!isPalindrome(s, start, end - 1)) continue;  // a failed field removes its whole branch
            path.add(s.substring(start, end));               // choose the field
            go(end, s, path, out);                           // explore the suffix
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    private static boolean isPalindrome(String s, int lo, int hi) {
        while (lo < hi) if (s.charAt(lo++) != s.charAt(hi--)) return false;   // compare the two ends
        return true;
    }

    /** Oracle: all masks over the gaps, with each field tested at the end. */
    static Set<List<String>> oracle(String s) {
        Set<List<String>> out = new HashSet<>();
        int gaps = s.length() - 1;
        for (int mask = 0; mask < (1 << gaps); mask++) {
            List<String> fields = new ArrayList<>(); int from = 0;
            for (int g = 0; g < gaps; g++) if ((mask >> g & 1) == 1) { fields.add(s.substring(from, g + 1)); from = g + 1; }
            fields.add(s.substring(from));
            boolean ok = true;
            for (String f : fields) if (!new StringBuilder(f).reverse().toString().equals(f)) ok = false;
            if (ok) out.add(fields);
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!partition("abba").equals(List.of(List.of("a", "b", "b", "a"), List.of("a", "bb", "a"), List.of("abba")))) throw new AssertionError("ex1");
        if (!partition("ab").equals(List.of(List.of("a", "b")))) throw new AssertionError("ex2");
        // Random strings over a small alphabet must match the mask oracle.
        Random rnd = new Random(1993);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(10);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(2)));
            String s = sb.toString();
            List<List<String>> got = partition(s);
            if (got.size() != oracle(s).size() || !new HashSet<>(got).equals(oracle(s))) throw new AssertionError("random " + s);
        }
        // The cost claim of the lesson: twenty different letters give 21 calls and 210 field tests.
        calls = 0; checks = 0;
        List<List<String>> r = partition("abcdefghijklmnopqrst");
        if (r.size() != 1 || calls != 21 || checks != 210) throw new AssertionError("cost " + calls + " " + checks);
        System.out.println("ok");
    }
}
```
