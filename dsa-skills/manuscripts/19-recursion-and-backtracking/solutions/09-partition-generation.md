<!-- solutions-for: 09-partition-generation -->
### Partition Generation

#### Solution: [Build] All Splits Of A Short String (Author exercise)
<!-- id: bt-short-splits -->

**Approach.** A call at `start` loops the ending from `start + 1` to the length, adds the piece from `start` to that ending, recurses from the ending and removes the piece, and it records a copy of the path when `start` equals the length. The order of results is the order of the sequences of ending positions, shortest ending first. The oracle goes through every pattern of cuts at the gaps, converts each to its list of endings, sorts those lists, and cuts the string by them. The harness compares both for random strings of one to eight letters and asserts that the number of partitions is 2^(n - 1), which is the number of patterns.

**Complexity.** There are 2^(n - 1) partitions, each costing an O(n) copy, and the stack holds at most n pieces.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ShortSplits {
    static void cut(String s, int start, List<String> path, List<List<String>> out) {
        if (start == s.length()) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int end = start + 1; end <= s.length(); end++) {
            path.add(s.substring(start, end));
            cut(s, end, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<String>> splits(String s) {
        List<List<String>> out = new ArrayList<>();
        cut(s, 0, new ArrayList<>(), out);
        return out;
    }

    static List<List<String>> oracle(String s) {
        int n = s.length();
        List<List<Integer>> ends = new ArrayList<>();
        for (int m = 0; m < (1 << (n - 1)); m++) {
            List<Integer> e = new ArrayList<>();
            for (int gap = 0; gap < n - 1; gap++) if ((m >> gap & 1) == 1) e.add(gap + 1);
            e.add(n);
            ends.add(e);
        }
        ends.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        List<List<String>> out = new ArrayList<>();
        for (List<Integer> e : ends) {
            List<String> pieces = new ArrayList<>();
            int from = 0;
            for (int x : e) { pieces.add(s.substring(from, x)); from = x; }
            out.add(pieces);
        }
        return out;
    }

    public static void main(String[] args) {
        List<List<String>> one = List.of(List.of("a", "b", "c"), List.of("a", "bc"), List.of("ab", "c"), List.of("abc"));
        if (!splits("abc").equals(one)) throw new AssertionError("example 1");
        if (!splits("a").equals(List.of(List.of("a")))) throw new AssertionError("example 2");
        Random rnd = new Random(19901);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            List<List<String>> got = splits(s);
            if (!got.equals(oracle(s))) throw new AssertionError("differs on " + s);
            if (got.size() != (1 << (n - 1))) throw new AssertionError("count on " + s);
        }
    }
}
```

#### Solution: [Vary] Valid-Piece Predicate (Author exercise)
<!-- id: bt-valid-pieces -->

**Approach.** The search is the same as in the previous rung with a test on each piece before recursion. A piece passes when it is the single digit zero or begins with a nonzero digit, and when its value is within the cap. A failing piece is skipped with `continue` and not `break`, since a longer piece from the same start can still pass when it fails only by a leading zero, and the cap is the only reason a longer piece could never pass. The harness compares the search with an oracle that builds every pattern of cuts and filters by the same rule, using values parsed as `long`. Both examples are asserted literally.

**Complexity.** Each accepted piece leads to a call, so the work follows the accepted prefixes and is at most O(n * 2^n), usually far below that.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ValidPieces {
    static boolean ok(String piece, int cap) {
        if (piece.length() > 1 && piece.charAt(0) == '0') return false;
        return Long.parseLong(piece) <= cap;
    }

    static void cut(String s, int start, int cap, List<String> path, List<List<String>> out) {
        if (start == s.length()) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int end = start + 1; end <= s.length(); end++) {
            String piece = s.substring(start, end);
            if (!ok(piece, cap)) continue;
            path.add(piece);
            cut(s, end, cap, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<String>> solve(String s, int cap) {
        List<List<String>> out = new ArrayList<>();
        cut(s, 0, cap, new ArrayList<>(), out);
        return out;
    }

    static List<List<String>> oracle(String s, int cap) {
        int n = s.length();
        List<List<Integer>> ends = new ArrayList<>();
        for (int m = 0; m < (1 << (n - 1)); m++) {
            List<Integer> e = new ArrayList<>();
            for (int gap = 0; gap < n - 1; gap++) if ((m >> gap & 1) == 1) e.add(gap + 1);
            e.add(n);
            ends.add(e);
        }
        ends.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        List<List<String>> out = new ArrayList<>();
        for (List<Integer> e : ends) {
            List<String> pieces = new ArrayList<>();
            int from = 0;
            boolean good = true;
            for (int x : e) {
                String p = s.substring(from, x);
                from = x;
                if ((p.length() > 1 && p.charAt(0) == '0') || Long.parseLong(p) > cap) good = false;
                pieces.add(p);
            }
            if (good) out.add(pieces);
        }
        return out;
    }

    public static void main(String[] args) {
        List<List<String>> one = List.of(List.of("1", "2", "3", "4"), List.of("1", "2", "34"), List.of("1", "23", "4"), List.of("12", "3", "4"), List.of("12", "34"));
        if (!solve("1234", 34).equals(one)) throw new AssertionError("example 1");
        List<List<String>> two = List.of(List.of("1", "0", "0", "1"), List.of("10", "0", "1"), List.of("100", "1"));
        if (!solve("1001", 100).equals(two)) throw new AssertionError("example 2");
        Random rnd = new Random(19902);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('0' + rnd.nextInt(10)));
            String s = sb.toString();
            int cap = rnd.nextInt(1001);
            if (!solve(s, cap).equals(oracle(s, cap))) throw new AssertionError("differs on " + s + " cap " + cap);
        }
    }
}
```

#### Solution: [Boundary] Empty Suffix Completion (Author exercise)
<!-- id: bt-empty-suffix -->

**Approach.** The call records only when `start` equals the length of the string, and its loop offers a piece of two letters or three only when that many letters remain, which keeps `substring` inside the string. A string of length zero is complete at the first call and records one empty partition, and a string of length one reaches the end of every route without recording. The harness runs a careless version that records any path that cannot be extended, and asserts that on `abcde` it lists the incomplete path `ab`, `cd`, which is the error this rung is about. It also asserts that an out-of-range `substring` throws. The oracle checks every pattern of cuts and keeps those whose pieces all have two or three letters.

**Complexity.** The routes follow acceptable prefixes, and the number of partitions grows like a Fibonacci-style sequence in the length, with a copy for each.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class EmptySuffix {
    static void cut(String s, int start, boolean careless, List<String> path, List<List<String>> out) {
        if (start == s.length()) {
            out.add(new ArrayList<>(path));
            return;
        }
        boolean extended = false;
        for (int len = 2; len <= 3; len++) {
            if (start + len > s.length()) break;
            extended = true;
            path.add(s.substring(start, start + len));
            cut(s, start + len, careless, path, out);
            path.remove(path.size() - 1);
        }
        if (careless && !extended) out.add(new ArrayList<>(path));
    }

    static List<List<String>> solve(String s, boolean careless) {
        List<List<String>> out = new ArrayList<>();
        cut(s, 0, careless, new ArrayList<>(), out);
        return out;
    }

    static List<List<String>> oracle(String s) {
        int n = s.length();
        List<List<String>> out = new ArrayList<>();
        if (n == 0) {
            out.add(new ArrayList<>());
            return out;
        }
        List<List<Integer>> ends = new ArrayList<>();
        for (int m = 0; m < (1 << (n - 1)); m++) {
            List<Integer> e = new ArrayList<>();
            for (int gap = 0; gap < n - 1; gap++) if ((m >> gap & 1) == 1) e.add(gap + 1);
            e.add(n);
            ends.add(e);
        }
        ends.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        for (List<Integer> e : ends) {
            List<String> pieces = new ArrayList<>();
            int from = 0;
            boolean good = true;
            for (int x : e) {
                if (x - from < 2 || x - from > 3) good = false;
                pieces.add(s.substring(from, x));
                from = x;
            }
            if (good) out.add(pieces);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve("abcde", false).equals(List.of(List.of("ab", "cde"), List.of("abc", "de")))) throw new AssertionError("example 1");
        if (!solve("a", false).isEmpty()) throw new AssertionError("example 2");
        List<List<String>> empty = solve("", false);
        if (empty.size() != 1 || !empty.get(0).isEmpty()) throw new AssertionError("empty string has one empty partition");
        if (!solve("abcde", true).contains(List.of("ab", "cd"))) throw new AssertionError("the careless version records the incomplete path");
        boolean threw = false;
        try {
            "abc".substring(2, 4);
        } catch (StringIndexOutOfBoundsException e) {
            threw = true;
        }
        if (!threw) throw new AssertionError("substring past the end must throw");
        Random rnd = new Random(19903);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(13);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(26)));
            String s = sb.toString();
            if (!solve(s, false).equals(oracle(s))) throw new AssertionError("differs on length " + n);
        }
    }
}
```

#### Solution: [Recognize] Palindrome Partitioning (LeetCode 131)
<!-- id: bt-palindrome-partition -->

**Approach.** The structure is that of the predicate rung with the rule replaced by a palindrome test on the piece, found by comparing characters from both ends inward. A piece of one letter always passes, so every string has at least one partition, and a failing piece is skipped without ending the loop, since a longer piece from the same start can still read the same in both directions. The oracle builds every pattern of cuts and tests each piece against its reverse. The harness also asserts that a string of equal letters has 2^(n - 1) partitions, as every piece of it is a palindrome, and that the first partition always cuts into single letters.

**Complexity.** Up to 2^(n - 1) partitions, each an O(n) copy, plus O(n) per palindrome test, and a stack of n frames.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class PalindromePartition {
    static boolean palindrome(String s, int lo, int hi) {
        while (lo < hi) if (s.charAt(lo++) != s.charAt(hi--)) return false;
        return true;
    }

    static void cut(String s, int start, List<String> path, List<List<String>> out) {
        if (start == s.length()) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int end = start + 1; end <= s.length(); end++) {
            if (!palindrome(s, start, end - 1)) continue;
            path.add(s.substring(start, end));
            cut(s, end, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<String>> partition(String s) {
        List<List<String>> out = new ArrayList<>();
        cut(s, 0, new ArrayList<>(), out);
        return out;
    }

    static List<List<String>> oracle(String s) {
        int n = s.length();
        List<List<Integer>> ends = new ArrayList<>();
        for (int m = 0; m < (1 << (n - 1)); m++) {
            List<Integer> e = new ArrayList<>();
            for (int gap = 0; gap < n - 1; gap++) if ((m >> gap & 1) == 1) e.add(gap + 1);
            e.add(n);
            ends.add(e);
        }
        ends.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        List<List<String>> out = new ArrayList<>();
        for (List<Integer> e : ends) {
            List<String> pieces = new ArrayList<>();
            int from = 0;
            boolean good = true;
            for (int x : e) {
                String p = s.substring(from, x);
                if (!p.equals(new StringBuilder(p).reverse().toString())) good = false;
                pieces.add(p);
                from = x;
            }
            if (good) out.add(pieces);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!partition("aab").equals(List.of(List.of("a", "a", "b"), List.of("aa", "b")))) throw new AssertionError("example 1");
        List<List<String>> two = List.of(List.of("a", "b", "b", "a"), List.of("a", "bb", "a"), List.of("abba"));
        if (!partition("abba").equals(two)) throw new AssertionError("example 2");
        for (int n = 1; n <= 12; n++) {
            String same = "a".repeat(n);
            if (partition(same).size() != (1 << (n - 1))) throw new AssertionError("equal letters, n=" + n);
        }
        Random rnd = new Random(19904);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(2)));
            String s = sb.toString();
            List<List<String>> got = partition(s);
            if (!got.equals(oracle(s))) throw new AssertionError("differs on " + s);
            if (got.get(0).size() != n) throw new AssertionError("the first partition is single letters");
        }
    }
}
```
