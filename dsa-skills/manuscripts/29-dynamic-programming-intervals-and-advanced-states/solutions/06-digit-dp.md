<!-- solutions-for: 29-dynamic-programming-intervals-and-advanced-states -->
### Solutions For Digit DP

#### Solution: [Build] Count Fixed-Length Digit Strings (Author exercise)
<!-- id: dp29-fixed-length-strings -->

**Approach.**
Let `ways[p]` be the number of valid strings of length `p`. The empty string is valid, so `ways[0]` is 1. Each position accepts every character of `allowed`, whatever came before, so `ways[p + 1]` equals `ways[p]` times the size of `allowed`. No flag is needed here, because no position depends on an earlier choice.

The invariant is that `ways[p]` counts distinct strings of length `p` over `allowed`, and each string of length `p + 1` is one string of length `p` followed by one allowed character. The answer is `ways[len]`.

**Complexity.**
- **Time** is O(len), because the loop makes one multiplication for each position.
- **Space** is O(len) for the array, and a single running product would reduce it to O(1).

```java run
import java.util.*;

public final class Dp29FixedLengthStrings {
    /**
     * Counts strings of length len whose characters all come from allowed.
     * Time: O(len). Space: O(len).
     * Invariant: ways[p] counts the distinct valid strings of length p.
     */
    static long count(int len, String allowed) {
        // One slot per length from 0 to len; Java fills the new array with zeros.
        long[] ways = new long[len + 1];
        // The empty string is the single valid string of length 0.
        ways[0] = 1;
        // Each loop pass extends every string of length p by one allowed character.
        for (int p = 0; p < len; p++) {
            // Every position offers allowed.length() choices, so the count multiplies by that size.
            ways[p + 1] = ways[p] * allowed.length();
        }
        // The last slot holds the strings of the requested length.
        return ways[len];
    }

    /** Oracle: builds every string over the allowed characters and counts them. */
    static long oracle(int len, String allowed) {
        List<String> cur = new ArrayList<>();
        cur.add("");
        for (int p = 0; p < len; p++) {
            List<String> nxt = new ArrayList<>();
            for (String s : cur) for (char c : allowed.toCharArray()) nxt.add(s + c);
            cur = nxt;
        }
        return cur.size();
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (count(4, "024") != 81) throw new AssertionError("ex1");
        if (count(3, "1357") != 64) throw new AssertionError("ex2");
        // Length 0 gives one empty string, and the largest case stays inside a long.
        if (count(0, "5") != 1) throw new AssertionError("len 0");
        if (count(15, "0123456789") != 1_000_000_000_000_000L) throw new AssertionError("max");
        // Java behavior: a new long array holds zeros, and an int times a long widens to long.
        long[] fresh = new long[3];
        if (fresh[2] != 0L) throw new AssertionError("zero fill");
        if (((long) 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10 * 10) != 1_000_000_000_000_000L) throw new AssertionError("widen");
        // Random inputs against the oracle.
        Random rnd = new Random(2906);
        for (int t = 0; t < 300; t++) {
            int len = rnd.nextInt(6);
            StringBuilder sb = new StringBuilder();
            for (char c = '0'; c <= '9'; c++) if (rnd.nextInt(4) == 0) sb.append(c);
            if (sb.length() == 0) sb.append('7');
            if (count(len, sb.toString()) != oracle(len, sb.toString())) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Add Tight State (Author exercise)
<!-- id: dp29-add-tight-state -->

**Approach.**
The method writes `n` as `d` digits and walks the positions from left to right. It keeps `tight`, the count of prefixes equal to the leading digits of `n`, and `loose`, the count of prefixes already smaller. A tight prefix may place an allowed digit from 0 up to the digit of `n` at that position. A loose prefix may place any allowed digit.

When a tight prefix places the digit of `n` itself, it stays tight. Every smaller allowed digit moves it to the loose count. The invariant is that after `p` positions, `tight` is 1 if the first `p` digits of `n` all belong to `allowed` and 0 otherwise, and `loose` counts every allowed prefix that is smaller. The answer is `tight + loose`, because a tight string equals `n` and still counts.

**Complexity.**
- **Time** is O(d * 10), because each position tries at most ten digits for two counts.
- **Space** is O(d) for the digit array, plus constant space for the two counts.

```java run
import java.util.*;

public final class Dp29AddTightState {
    /**
     * Counts d-digit strings, leading zeros allowed, with value at most n and characters from allowed.
     * Time: O(d * 10). Space: O(d).
     * Invariant: tight is 1 only while the prefix equals the leading digits of n.
     */
    static long count(long n, String allowed) {
        // Mark each allowed digit once so each test costs O(1).
        boolean[] ok = new boolean[10];
        for (char c : allowed.toCharArray()) ok[c - '0'] = true;
        // Digits of n from the leading digit down to the last digit.
        String text = Long.toString(n);
        long tight = 1;
        long loose = 0;
        // Each pass handles one position of the d positions.
        for (int p = 0; p < text.length(); p++) {
            int limit = text.charAt(p) - '0';
            // Loose prefixes keep their count for every allowed digit, any of ten digits.
            long nextLoose = 0;
            int allowedCount = 0;
            for (int dig = 0; dig <= 9; dig++) if (ok[dig]) allowedCount++;
            nextLoose += loose * allowedCount;
            // A tight prefix places digits up to the limit, and smaller digits turn loose.
            long nextTight = 0;
            if (tight == 1) {
                for (int dig = 0; dig < limit; dig++) if (ok[dig]) nextLoose++;
                // The limit digit keeps the prefix tight only when it is allowed.
                if (ok[limit]) nextTight = 1;
            }
            tight = nextTight;
            loose = nextLoose;
        }
        // A tight string equals n, so it counts with the smaller strings.
        return tight + loose;
    }

    /** Oracle: pads every value from 0 to n to d digits and tests each character. */
    static long oracle(long n, String allowed) {
        int d = Long.toString(n).length();
        long total = 0;
        for (long x = 0; x <= n; x++) {
            StringBuilder s = new StringBuilder(Long.toString(x));
            while (s.length() < d) s.insert(0, '0');
            boolean good = true;
            for (int i = 0; i < s.length(); i++) if (allowed.indexOf(s.charAt(i)) < 0) good = false;
            if (good) total++;
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (count(3047, "0123") != 208) throw new AssertionError("ex1");
        if (count(58, "2468") != 8) throw new AssertionError("ex2");
        // Bound 0 has one digit; the string "0" counts only when 0 is allowed.
        if (count(0, "0") != 1) throw new AssertionError("zero allowed");
        if (count(0, "5") != 0) throw new AssertionError("zero not allowed");
        // Java behavior: subtracting '0' from a digit character gives its int value.
        if ("7".charAt(0) - '0' != 7) throw new AssertionError("digit value");
        // Random bounds against the oracle.
        Random rnd = new Random(2907);
        for (int t = 0; t < 400; t++) {
            long n = rnd.nextInt(3000);
            StringBuilder sb = new StringBuilder();
            for (char c = '0'; c <= '9'; c++) if (rnd.nextInt(2) == 0) sb.append(c);
            if (sb.length() == 0) sb.append('3');
            if (count(n, sb.toString()) != oracle(n, sb.toString())) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Leading Zero And Number Zero (Author exercise)
<!-- id: dp29-leading-zero-and-zero -->

**Approach.**
The state is the position, the tight flag, the started flag and the number of real zero digits placed so far. A map from zero count to ways would also work, and a `long[2][2][k + 2]` array is simpler. Zeros placed before the first nonzero digit are padding, so they leave the zero count at its value. Zeros placed after the number started add 1. Counts above `k` are dropped, since zero counts never decrease.

The integer 0 never starts, so the final tally of a state that is not started needs a rule. That state stands for the single integer 0, whose one digit is a zero. The method adds its count to the answer only when `k` equals 1. The invariant is that the zero count of a state equals the number of zero digits in the number's real representation so far.

**Complexity.**
- **Time** is O(d * 4 * k * 10), because each position, flag pair and zero count tries ten digits.
- **Space** is O(k) for the two layers of counts, plus O(d) for the digits.

```java run
import java.util.*;

public final class Dp29LeadingZeroAndZero {
    /**
     * Counts integers x in [0, n] whose decimal form has exactly k zero digits.
     * Time: O(d * k * 10). Space: O(d + k).
     * Invariant: zeros counts only digits placed after the number has started.
     */
    static long count(long n, int k) {
        // Digits of n from the leading digit down.
        String text = Long.toString(n);
        // cur[t][s][z] counts prefixes with tight flag t, started flag s and z real zeros.
        long[][][] cur = new long[2][2][k + 2];
        // The empty prefix is tight and not started, with no zeros.
        cur[1][0][0] = 1;
        // Each pass handles one position of the digits of n.
        for (int p = 0; p < text.length(); p++) {
            long[][][] nxt = new long[2][2][k + 2];
            int d = text.charAt(p) - '0';
            for (int t = 0; t < 2; t++) {
                for (int s = 0; s < 2; s++) {
                    for (int z = 0; z <= k; z++) {
                        long c = cur[t][s][z];
                        if (c == 0) continue;
                        // A tight prefix is capped by the digit of n; a loose one accepts 0 to 9.
                        int limit = t == 1 ? d : 9;
                        for (int dig = 0; dig <= limit; dig++) {
                            int nt = (t == 1 && dig == limit) ? 1 : 0;
                            int ns = (s == 1 || dig != 0) ? 1 : 0;
                            // A zero counts only after the number has started.
                            int nz = z + ((s == 1 && dig == 0) ? 1 : 0);
                            if (nz > k) continue;
                            nxt[nt][ns][nz] += c;
                        }
                    }
                }
            }
            cur = nxt;
        }
        // Started prefixes are real integers from 1 to n, so those with k zeros count.
        long total = cur[0][1][k] + cur[1][1][k];
        // The unstarted prefix is the integer 0, which has exactly one zero digit.
        if (k == 1) total += cur[0][0][0] + cur[1][0][0];
        return total;
    }

    /** Oracle: writes every integer from 0 to n and counts the character '0'. */
    static long oracle(long n, int k) {
        long total = 0;
        for (long x = 0; x <= n; x++) {
            String s = Long.toString(x);
            int zeros = 0;
            for (int i = 0; i < s.length(); i++) if (s.charAt(i) == '0') zeros++;
            if (zeros == k) total++;
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (count(100, 2) != 1) throw new AssertionError("ex1");
        if (count(0, 1) != 1) throw new AssertionError("ex2");
        // The integer 0 has one zero digit and none for k = 0; a one-digit bound has no zeros.
        if (count(0, 0) != 0) throw new AssertionError("zero k0");
        if (count(9, 0) != 9) throw new AssertionError("nine");
        // Java behavior: Long.toString writes 0 as the single character "0" and adds no leading zeros.
        if (!Long.toString(0).equals("0")) throw new AssertionError("toString zero");
        if (!Long.toString(105).equals("105")) throw new AssertionError("toString 105");
        // Random bounds and zero counts against the oracle.
        Random rnd = new Random(2908);
        for (int t = 0; t < 500; t++) {
            long n = rnd.nextInt(4000);
            int k = rnd.nextInt(4);
            if (count(n, k) != oracle(n, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Numbers At Most N Given Digit Set (LeetCode 902)
<!-- id: dp29-digit-set-at-most-n -->

**Approach.**
The method counts positive integers at most `n` with every digit in the set, and it uses the same two flags as the lesson. At each position a prefix places a digit from the set that does not pass the limit. Because the set has no 0, a started number never places a padding zero. Padding zeros may still appear while the number has not started, and they leave the started flag at 0.

The state tracks tight and started flags, and the invariant is the one from the lesson: each count covers every distinct prefix with those flags. The answer adds the two started counts, which excludes the empty number. The alternative of adding the count of every shorter length separately gives the same total, and the started flag removes that special case.

**Complexity.**
- **Time** is O(d * 9), because each position tries at most nine set digits for four states.
- **Space** is O(d) for the digit array, plus constant space for the counts.

```java run
import java.util.*;

public final class Dp29DigitSetAtMostN {
    /**
     * Counts positive integers at most n whose digits all come from the given set.
     * Time: O(d * 9). Space: O(d).
     * Invariant: ways[t][s] counts distinct prefixes with tight flag t and started flag s.
     */
    static long count(String digits, long n) {
        // Mark each digit of the set so the membership test costs O(1).
        boolean[] inSet = new boolean[10];
        for (char c : digits.toCharArray()) inSet[c - '0'] = true;
        String text = Long.toString(n);
        long[][] ways = new long[2][2];
        // The empty prefix is tight and not started.
        ways[1][0] = 1;
        // Each pass fixes one position of the digits of n.
        for (int p = 0; p < text.length(); p++) {
            long[][] next = new long[2][2];
            int d = text.charAt(p) - '0';
            for (int t = 0; t < 2; t++) {
                for (int s = 0; s < 2; s++) {
                    long c = ways[t][s];
                    if (c == 0) continue;
                    // A tight prefix may not pass the digit of n.
                    int limit = t == 1 ? d : 9;
                    // Digit 0 is padding for an unstarted prefix; any other digit must belong to the set.
                    for (int dig = 0; dig <= limit; dig++) {
                        if (dig == 0 ? s == 1 : !inSet[dig]) continue;
                        int nt = (t == 1 && dig == limit) ? 1 : 0;
                        int ns = dig == 0 ? 0 : 1;
                        next[nt][ns] += c;
                    }
                }
            }
            ways = next;
        }
        // Started prefixes are the positive integers that fit the set and the bound.
        return ways[0][1] + ways[1][1];
    }

    /** Oracle: tests every integer from 1 to n against the set. */
    static long oracle(String digits, long n) {
        long total = 0;
        for (long x = 1; x <= n; x++) {
            String s = Long.toString(x);
            boolean good = true;
            for (int i = 0; i < s.length(); i++) if (digits.indexOf(s.charAt(i)) < 0) good = false;
            if (good) total++;
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (count("249", 500) != 30) throw new AssertionError("ex1");
        if (count("1357", 1000) != 84) throw new AssertionError("ex2");
        // A single digit set and a bound that equals the set digit.
        if (count("5", 5) != 1) throw new AssertionError("single");
        if (count("5", 4) != 0) throw new AssertionError("below");
        // Java behavior: String.indexOf returns -1 when a character is absent.
        if ("249".indexOf('7') != -1) throw new AssertionError("indexOf");
        // Random sets and bounds against the oracle.
        Random rnd = new Random(2909);
        for (int t = 0; t < 500; t++) {
            long n = 1 + rnd.nextInt(5000);
            StringBuilder sb = new StringBuilder();
            for (char c = '1'; c <= '9'; c++) if (rnd.nextInt(3) == 0) sb.append(c);
            if (sb.length() == 0) sb.append('6');
            if (count(sb.toString(), n) != oracle(sb.toString(), n)) throw new AssertionError("random " + t);
        }
    }
}
```
