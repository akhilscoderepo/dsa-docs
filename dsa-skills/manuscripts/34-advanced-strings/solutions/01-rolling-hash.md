<!-- solutions-for: 01-rolling-hash -->
### Solutions For The Rolling Hash Exercises

#### Solution: [Build] Fixed-Window Hash (Author exercise)
<!-- id: as-fixed-window-hash -->

**Approach.**
The method builds the hash of the first window with the multiply-and-add step, which is Horner evaluation of the polynomial. It also computes `power`, the weight `27^(k-1) mod 1,000,000,007` of the leading letter. For every later position it removes the outgoing letter times `power`, multiplies by 27 and adds the incoming letter. The invariant is that after processing index `end`, `hash` equals the polynomial value of the window that ends at `end` under the fixed base, modulus and letter codes. The update stays in `long` arithmetic, because the product of a value below the modulus and 27 exceeds the `int` range, and the code asserts that overflow.

The oracle recomputes the last window from its definition with `BigInteger`, which cannot overflow, and the random tests compare both results.

**Complexity.**
- **Time** is O(n), because the first window costs k steps and each of the n - k later positions costs a constant number of operations; computing `power` adds k - 1 steps.
- **Space** is O(1), because only `hash`, `power` and loop indexes are stored and no substring is created.

```java run
import java.math.BigInteger;
import java.util.Random;

public class FixedWindowHashSolution {
    static final long BASE = 27;
    static final long MOD = 1_000_000_007L;

    /**
     * Returns the hash of the last window of length k, found by sliding from the first window.
     * Time: O(n), because every position triggers one constant-time update.
     * Space: O(1), because only a few longs are kept.
     * Invariant: after index end, hash is the polynomial value of s[end-k+1..end] mod MOD.
     */
    static long lastWindowHash(String s, int k) {
        // power is the weight of the leading letter, BASE^(k-1) mod MOD, built with k-1 multiplications.
        long power = 1;
        for (int j = 1; j < k; j++) power = power * BASE % MOD;
        long hash = 0;
        // One pass over all letters; each iteration costs a constant number of operations.
        for (int end = 0; end < s.length(); end++) {
            // Windows only slide once the first k letters are in, so the outgoing letter exists from end = k.
            if (end >= k) {
                long out = s.charAt(end - k) - 'a' + 1;
                // Remove the leading letter; the reduced term keeps the difference above -MOD, so + MOD restores it.
                hash = (hash - out * power % MOD + MOD) % MOD;
            }
            // Append the incoming letter: shift one base position and add its code.
            hash = (hash * BASE + (s.charAt(end) - 'a' + 1)) % MOD;
        }
        // After the last index the hash describes the last window.
        return hash;
    }

    /** Oracle: sum of code * 27^(k-1-j) evaluated exactly with BigInteger, then reduced once. */
    static long oracle(String s, int k) {
        BigInteger sum = BigInteger.ZERO;
        int from = s.length() - k;
        // Exact evaluation: no overflow, no intermediate reduction.
        for (int j = 0; j < k; j++) {
            BigInteger term = BigInteger.valueOf(s.charAt(from + j) - 'a' + 1).multiply(BigInteger.valueOf(BASE).pow(k - 1 - j));
            sum = sum.add(term);
        }
        return sum.mod(BigInteger.valueOf(MOD)).longValue();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (lastWindowHash("abcab", 3) != 2216) throw new AssertionError("example 1");
        if (lastWindowHash("zzzzzzzzzz", 10) != 130653411L) throw new AssertionError("example 2");
        // A window of one letter is the letter code itself.
        if (lastWindowHash("abcz", 1) != 26) throw new AssertionError("k = 1");
        // Java claim: 1,000,000,006 * 27 overflows int, so the code must multiply in long.
        int wrapped = 1_000_000_006 * 27;
        if ((long) wrapped == 1_000_000_006L * 27) throw new AssertionError("int product should overflow");
        // Random tests against the BigInteger oracle with a seeded generator.
        Random rnd = new Random(34_01);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(60);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(26)));
            int k = 1 + rnd.nextInt(n);
            if (lastWindowHash(sb.toString(), k) != oracle(sb.toString(), k)) throw new AssertionError("mismatch " + sb + " " + k);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Repeated DNA Sequences (LeetCode 187)
<!-- id: as-repeated-dna -->

**Approach.**
The four letters get the 2-bit codes A as 0, C as 1, G as 2 and T as 3, so a window of 10 letters is a 20-bit integer. Appending a letter shifts the key left by 2 bits and adds the code. A mask of 20 one-bits then drops the oldest letter, which replaces the subtraction of the rolling update and removes any need for a modulus or a negative-value fix. The invariant is that after index `end`, `key` holds exactly the 20 bits of the last 10 letters, so two windows are equal exactly when their keys are equal and no collision check is required.

A `byte` array of size 2^20 counts each key up to 2. A key reaches the count 2 on its second occurrence and joins the answer once, so overlapping windows and triple repeats never duplicate an entry. Numeric order of equal-length keys matches alphabetical order under the code order A, C, G, T, so sorting the integer keys sorts the answer, and the strings are built only for the final answer.

**Complexity.**
- **Time** is O(n + R log R), because the scan does constant work per letter and sorting sorts the R repeated keys; R is at most n.
- **Space** is O(2^20 + R), because the count array has a fixed size of about one million bytes and the answer holds R keys.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.TreeMap;

public class RepeatedDnaSolution {
    static final int K = 10;
    static final int MASK = (1 << (2 * K)) - 1;

    /** Maps A, C, G, T to 0, 1, 2, 3; the alphabet is the stated assumption of the contract. */
    static int code(char c) {
        // The switch is exhaustive for the contract alphabet; anything else is a caller error.
        switch (c) {
            case 'A': return 0;
            case 'C': return 1;
            case 'G': return 2;
            case 'T': return 3;
            default: throw new IllegalArgumentException("bad letter " + c);
        }
    }

    /**
     * Returns every 10-letter sequence that occurs at least twice, once each, in ascending order.
     * Time: O(n + R log R), because the scan is linear and the R repeated keys are sorted.
     * Space: O(2^20 + R), because of the fixed count table and the answer keys.
     * Invariant: after index end, key equals the 2-bit digits of s[end-9..end] exactly.
     */
    static List<String> repeated(String s) {
        // The table stores 0, 1 or 2 per key; 2 means the key already joined the answer.
        byte[] seen = new byte[1 << (2 * K)];
        int[] keys = new int[Math.max(s.length(), 1)];
        int count = 0;
        int key = 0;
        // One pass; each iteration does a shift, a mask and a table lookup.
        for (int end = 0; end < s.length(); end++) {
            // Shift the old letters up by 2 bits, add the new code, and drop the oldest letter with the mask.
            key = ((key << 2) | code(s.charAt(end))) & MASK;
            // The first K - 1 iterations only fill the key, so no complete window exists yet.
            if (end < K - 1) continue;
            // The second sighting records the key once; later sightings change nothing.
            if (seen[key] == 1) { seen[key] = 2; keys[count++] = key; }
            else if (seen[key] == 0) seen[key] = 1;
        }
        // Numeric order of equal-length 2-bit keys equals alphabetical order for A < C < G < T.
        Arrays.sort(keys, 0, count);
        List<String> out = new ArrayList<>();
        // Strings are built only for answers, never inside the scan.
        for (int i = 0; i < count; i++) {
            char[] w = new char[K];
            int v = keys[i];
            for (int j = K - 1; j >= 0; j--) { w[j] = "ACGT".charAt(v & 3); v >>= 2; }
            out.add(new String(w));
        }
        return out;
    }

    /** Oracle: count every substring of length 10 in a TreeMap, which also sorts the keys. */
    static List<String> oracle(String s) {
        TreeMap<String, Integer> counts = new TreeMap<>();
        // Direct counting with substring copies; slow but obviously correct.
        for (int i = 0; i + K <= s.length(); i++) counts.merge(s.substring(i, i + K), 1, Integer::sum);
        List<String> out = new ArrayList<>();
        for (var e : counts.entrySet()) if (e.getValue() >= 2) out.add(e.getKey());
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!repeated("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT").equals(List.of("AAAAACCCCC", "CCCCCAAAAA"))) throw new AssertionError("example 1");
        if (!repeated("AAAAAAAAAAAAA").equals(List.of("AAAAAAAAAA"))) throw new AssertionError("overlapping repeats listed once");
        // Inputs shorter than 10 letters, and the empty input, give an empty list.
        if (!repeated("ACGTAC").isEmpty() || !repeated("").isEmpty()) throw new AssertionError("short input");
        // Exactly 10 letters is one window and cannot repeat.
        if (!repeated("ACGTACGTAC").isEmpty()) throw new AssertionError("single window");
        // Ten letters need 20 bits, so the key fits in an int with no modulus.
        if (MASK != 1_048_575) throw new AssertionError("mask size");
        // Random tests over a tiny alphabet slice so repeats are common, against the TreeMap oracle.
        Random rnd = new Random(34_02);
        for (int t = 0; t < 1500; t++) {
            int n = rnd.nextInt(60);
            int letters = 1 + rnd.nextInt(4);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append("ACGT".charAt(rnd.nextInt(letters)));
            if (!repeated(sb.toString()).equals(oracle(sb.toString()))) throw new AssertionError("mismatch " + sb);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Negative Modular Difference (Author exercise)
<!-- id: as-negative-modular-difference -->

**Approach.**
The method computes the first hash with the multiply-and-add step and then slides across the string. At each slide it subtracts the outgoing letter times `power`. The product is reduced by the modulus first, so it lies between 0 and 100, and the difference with the running hash lies between -100 and 100. Java `%` keeps the sign of the left operand, so a negative difference stays negative and would feed a negative number into the next multiplication. Adding the modulus once after the subtraction and reducing again returns the value to the range 0 to 100. The invariant is that `hash` is always in the range 0 to 100 and equals the polynomial value of the current window.

The tests also run the broken variant that skips the addition. It produces a negative value on the first statement example and, after the multiplication, a wrong hash, which shows that the repair is the part that matters. If the subtracted product is not reduced first, the difference can fall far below -101, and one addition of the modulus would not be enough.

**Complexity.**
- **Time** is O(n) for a string of length n, because each slide is a constant number of operations and the first window costs k steps.
- **Space** is O(n - k + 1), because the result holds one hash per window; the working state is O(1).

```java run
import java.util.Arrays;
import java.util.Random;

public class NegativeModularDifferenceSolution {
    static final long BASE = 27;
    static final long MOD = 101;

    /**
     * Returns the hash of every window of length k, each found by sliding from the previous one.
     * Time: O(n), because every slide is a constant number of operations.
     * Space: O(n - k + 1), because the answer array has one slot per window.
     * Invariant: hash is in [0, MOD - 1] and equals the polynomial value of the current window.
     */
    static int[] windowHashes(String s, int k, boolean normalize) {
        int n = s.length();
        // No window fits, so the answer is empty.
        if (k > n) return new int[0];
        int[] result = new int[n - k + 1];
        long power = 1;
        // power is BASE^(k-1) mod MOD, the weight of the leading letter.
        for (int j = 1; j < k; j++) power = power * BASE % MOD;
        long hash = 0;
        // One pass; every iteration is a constant number of arithmetic operations.
        for (int end = 0; end < n; end++) {
            if (end >= k) {
                long out = s.charAt(end - k) - 'a' + 1;
                // The reduced product lies in [0, 100], so the raw difference lies in [-100, 100].
                long raw = hash - out * power % MOD;
                // The repair adds MOD once and reduces again; skipping it leaves a negative value behind.
                hash = normalize ? (raw + MOD) % MOD : raw;
            }
            // Append the incoming letter; a negative hash from the broken variant propagates here.
            hash = (hash * BASE + (s.charAt(end) - 'a' + 1)) % MOD;
            if (end >= k - 1) result[end - k + 1] = (int) hash;
        }
        return result;
    }

    /** Oracle: Horner evaluation of every window from scratch, reduced at each step. */
    static int[] oracle(String s, int k) {
        if (k > s.length()) return new int[0];
        int[] result = new int[s.length() - k + 1];
        // Each window is evaluated independently, so there is no sliding state to get wrong.
        for (int i = 0; i < result.length; i++) {
            long h = 0;
            for (int j = 0; j < k; j++) h = (h * BASE + (s.charAt(i + j) - 'a' + 1)) % MOD;
            result[i] = (int) h;
        }
        return result;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(windowHashes("abcab", 3, true), new int[] {79, 25, 95})) throw new AssertionError("example 1");
        if (!Arrays.equals(windowHashes("zyxzy", 3, true), new int[] {59, 12, 43})) throw new AssertionError("example 2");
        // Empty input and a window longer than the string both give an empty answer.
        if (windowHashes("", 3, true).length != 0 || windowHashes("ab", 3, true).length != 0) throw new AssertionError("empty");
        // Java claims: % keeps the sign of the left operand, and floorMod does not.
        if (-19 % 101 != -19) throw new AssertionError("remainder keeps sign");
        if (Math.floorMod(-19, 101) != 82) throw new AssertionError("floorMod is non-negative");
        // The unreduced difference of example 2 is -513, and one addition of 101 stays negative.
        long power = 27L * 27 % MOD;
        if (59 - 26 * power != -513 || -513 + 101 >= 0) throw new AssertionError("raw difference");
        // The reduced product used by the method keeps the difference above -101.
        if (59 - 26 * power % MOD != -8) throw new AssertionError("reduced difference");
        // Without the repair the second slide of example 1 holds -19 and the hashes go wrong.
        if (Arrays.equals(windowHashes("abcab", 3, false), new int[] {79, 25, 95})) throw new AssertionError("broken variant should differ");
        // Random tests against the from-scratch oracle, including windows longer than the string.
        Random rnd = new Random(34_03);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(40);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(26)));
            int k = 1 + rnd.nextInt(n + 2);
            if (!Arrays.equals(windowHashes(sb.toString(), k, true), oracle(sb.toString(), k))) throw new AssertionError("mismatch " + sb + " " + k);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Longest Duplicate Substring (LeetCode 1044)
<!-- id: as-longest-duplicate-substring -->

**Approach.**
A duplicate of length L implies a duplicate of every shorter length, because removing the last letter from both occurrences leaves two equal shorter substrings. The property is monotone, so a binary search over lengths from 1 to n - 1 finds the largest length for which a duplicate exists. Each probe slides a rolling hash across the string with base 27 and letter codes 1 to 26 and keeps a table from each hash value to the starts that produced it. When a window hash is already in the table, the code compares the new window with every stored start through `regionMatches`, which reads both windows in place and creates no substring. Only an exact match counts as a duplicate. The invariant of a probe is that `hash` equals the polynomial value of the current window and that the table holds every earlier start, so no true duplicate is missed and no false one is accepted.

Because every match is verified, a collision costs time but never changes the answer. The harness proves that by running the same code with a modulus of 13, which forces many collisions, and by counting that false matches did occur and were rejected. The result is the substring of the best start, which is copied once at the end.

**Complexity.**
- **Time** is O(n log n) expected with a large modulus, because the binary search makes about log n probes and each probe is one linear pass with rare verification; a probe degrades toward O(n * L) if many windows collide.
- **Space** is O(n), because one probe stores at most n - L + 1 starts in the table and no window text.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public class LongestDuplicateSubstringSolution {
    static final long BASE = 27;
    static final long BIG_MOD = 1_000_000_007L;
    /** Counts matches of equal hash with different text; used only by the harness. */
    static long falseMatches = 0;

    /**
     * Returns the start of a window of length len that equals an earlier window, or -1.
     * Time: O(n) expected per probe, because each window is hashed in constant time and verified only on a hash match.
     * Space: O(n), because the table holds up to n - len + 1 start indexes.
     * Invariant: hash is the polynomial value of s[end-len+1..end] mod mod, and the table holds all earlier starts.
     */
    static int findDuplicate(String s, int len, long mod) {
        int n = s.length();
        // power is BASE^(len-1) mod mod, the weight of the leading letter.
        long power = 1;
        for (int j = 1; j < len; j++) power = power * BASE % mod;
        HashMap<Long, ArrayList<Integer>> table = new HashMap<>();
        long hash = 0;
        // One pass over the string; every window costs a constant number of operations to hash.
        for (int end = 0; end < n; end++) {
            // The outgoing letter exists once the window has been full for a step.
            if (end >= len) {
                long out = s.charAt(end - len) - 'a' + 1;
                // Reduce the product first, then add mod once, so the value stays in [0, mod - 1].
                hash = (hash - out * power % mod + mod) % mod;
            }
            // Append the incoming letter.
            hash = (hash * BASE + (s.charAt(end) - 'a' + 1)) % mod;
            // Windows are complete only from index len - 1 onward.
            if (end < len - 1) continue;
            int start = end - len + 1;
            ArrayList<Integer> earlier = table.computeIfAbsent(hash, h -> new ArrayList<>());
            // Verified comparison: regionMatches reads both windows in place and allocates no substring.
            for (int other : earlier) {
                if (s.regionMatches(other, s, start, len)) return start;
                falseMatches++;
            }
            earlier.add(start);
        }
        return -1;
    }

    /**
     * Returns a longest substring that occurs at least twice, or the empty string.
     * Time: O(n log n) expected, because about log n probes each cost O(n) expected.
     * Space: O(n), because of the probe table.
     * Invariant: lo is a length with a known duplicate (or 0) and hi + 1 is a length with none.
     */
    static String longestDuplicate(String s, long mod) {
        int lo = 0, hi = s.length() - 1, bestStart = 0;
        // Binary search on the length; the search is valid because a duplicate of length L implies one of length L - 1.
        while (lo < hi) {
            int mid = (lo + hi + 1) >>> 1;
            int start = findDuplicate(s, mid, mod);
            // A duplicate of length mid exists, so the answer is at least mid; remember where it starts.
            if (start >= 0) { lo = mid; bestStart = start; }
            // No duplicate of length mid exists, so the answer is shorter.
            else hi = mid - 1;
        }
        // The only substring copy in the whole method happens here, once.
        return s.substring(bestStart, bestStart + lo);
    }

    /** Oracle: try lengths from longest down, using a HashSet of substring copies. */
    static int oracleLength(String s) {
        // Slow and exact: every length gets a full set of copied windows.
        for (int len = s.length() - 1; len >= 1; len--) {
            java.util.HashSet<String> seen = new java.util.HashSet<>();
            for (int i = 0; i + len <= s.length(); i++) if (!seen.add(s.substring(i, i + len))) return len;
        }
        return 0;
    }

    /** Counts occurrences of t in s, overlapping allowed. */
    static int occurrences(String s, String t) {
        int c = 0;
        for (int i = s.indexOf(t); i >= 0; i = s.indexOf(t, i + 1)) c++;
        return c;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!longestDuplicate("banana", BIG_MOD).equals("ana")) throw new AssertionError("example 1");
        if (!longestDuplicate("aaaaa", BIG_MOD).equals("aaaa")) throw new AssertionError("overlap");
        if (!longestDuplicate("abcd", BIG_MOD).isEmpty()) throw new AssertionError("no duplicate");
        // Empty and one-letter inputs have no duplicate.
        if (!longestDuplicate("", BIG_MOD).isEmpty() || !longestDuplicate("z", BIG_MOD).isEmpty()) throw new AssertionError("tiny");
        // Java claims: regionMatches compares in place with offsets, and a partial substring is a new object.
        String t = "banana";
        if (!t.regionMatches(1, t, 3, 3) || t.regionMatches(0, t, 2, 3)) throw new AssertionError("regionMatches");
        if (t.substring(1, 4) == t || t.substring(0, t.length()) != t) throw new AssertionError("substring identity");
        // Random tests with the large modulus and with a tiny modulus that forces collisions.
        Random rnd = new Random(34_04);
        for (int trial = 0; trial < 2500; trial++) {
            int n = rnd.nextInt(40);
            int letters = 1 + rnd.nextInt(3);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(letters)));
            String s = sb.toString();
            int expected = oracleLength(s);
            for (long mod : new long[] {BIG_MOD, 13}) {
                String got = longestDuplicate(s, mod);
                // The length must equal the oracle length, and the text must really occur twice.
                if (got.length() != expected) throw new AssertionError("length " + s + " mod " + mod);
                if (expected > 0 && occurrences(s, got) < 2) throw new AssertionError("not a duplicate " + s);
            }
        }
        // The tiny modulus produced hash matches between different windows, and verification rejected each one.
        if (falseMatches == 0) throw new AssertionError("collisions should have occurred");
        System.out.println("ok");
    }
}
```
