<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Earliest Balance

#### Solution: [Build] Contiguous Array (LeetCode 525)
<!-- id: ps-contiguous-array-525 -->

**Approach.**
Each 0 counts as -1 and each 1 as +1, so a span has equal counts exactly when its two boundaries have the same balance. For a fixed end, the longest span starts at the earliest boundary with that balance. The map stores the first index of every balance and is never overwritten. It starts with balance 0 at index -1, so a span that begins at index 0 has a start to match. The invariant is that every stored index is the smallest index with that balance.

**Complexity.**
- **Time** is O(n) expected, because each value costs one hash lookup and at most one insert.
- **Space** is O(n), because the map holds at most n + 1 balances.

```java run
import java.util.HashMap;
import java.util.Random;

public final class ContiguousArray525 {
    /**
     * Returns the length of the longest subarray with equal numbers of 0 and 1.
     * Time: O(n) expected, one hash operation per value.
     * Space: O(n) for the map of earliest indexes.
     * Invariant: first.get(b) is the smallest index at which the balance was b.
     */
    static int longest(int[] nums) {
        HashMap<Integer, Integer> first = new HashMap<>();
        // Index -1 stands for the position before the first value.
        first.put(0, -1);
        int bal = 0, best = 0;
        for (int i = 0; i < nums.length; i++) {
            // A one adds 1 and a zero subtracts 1.
            bal += nums[i] == 1 ? 1 : -1;
            Integer seen = first.get(bal);
            // A new balance records its earliest index, and a repeat measures the span.
            if (seen == null) first.put(bal, i);
            else best = Math.max(best, i - seen);
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (longest(new int[] {0, 0, 1, 0, 0, 0, 1, 1}) != 6) throw new AssertionError("example 1");
        if (longest(new int[] {1, 1, 1}) != 0) throw new AssertionError("example 2");
        // A span from index 0 needs the entry at index -1.
        if (longest(new int[] {1, 0}) != 2) throw new AssertionError("from zero");
        // Random binary arrays against the double loop.
        Random rnd = new Random(17);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(14), 0, 2).toArray();
            int expect = 0;
            for (int i = 0; i < a.length; i++) {
                int d = 0;
                for (int j = i; j < a.length; j++) { d += a[j] == 1 ? 1 : -1; if (d == 0) expect = Math.max(expect, j - i + 1); }
            }
            if (longest(a) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Equal A And B (Author exercise)
<!-- id: ps-equal-a-and-b -->

**Approach.**
The step is +1 for `A`, -1 for `B` and 0 for every other letter. Equal balances at two boundaries enclose a substring with as many `A` as `B`. A letter with step 0 repeats the previous balance, so the map already holds that balance at an earlier index, and the span grows by one for free. The map keeps only the earliest index, so a run of other letters extends the best span instead of resetting it.

**Complexity.**
- **Time** is O(n) expected, because each character costs one hash operation.
- **Space** is O(n), because the map holds at most n + 1 balances.

```java run
import java.util.HashMap;
import java.util.Random;

public final class EqualAAndB {
    /**
     * Returns the length of the longest substring with as many 'A' as 'B'.
     * Time: O(n) expected, one hash operation per character.
     * Space: O(n) for the map of earliest indexes.
     * Invariant: first.get(b) is the smallest index at which the balance was b.
     */
    static int longest(String s) {
        HashMap<Integer, Integer> first = new HashMap<>();
        // Index -1 stands for the position before the first character.
        first.put(0, -1);
        int bal = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            // Three step values: +1, -1 and 0 for the other letters.
            if (c == 'A') bal++;
            else if (c == 'B') bal--;
            Integer seen = first.get(bal);
            // The earliest index stays, and a repeat extends the best span.
            if (seen == null) first.put(bal, i);
            else best = Math.max(best, i - seen);
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (longest("AXBBA") != 5) throw new AssertionError("example 1");
        if (longest("AAB") != 2) throw new AssertionError("example 2");
        // A single A has no valid substring.
        if (longest("A") != 0) throw new AssertionError("single A");
        // Random strings over A, B and X against the double loop.
        Random rnd = new Random(18);
        String alphabet = "ABX";
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 1 + rnd.nextInt(14); i > 0; i--) sb.append(alphabet.charAt(rnd.nextInt(3)));
            String s = sb.toString();
            int expect = 0;
            for (int i = 0; i < s.length(); i++) {
                int d = 0;
                for (int j = i; j < s.length(); j++) {
                    d += (s.charAt(j) == 'A' ? 1 : 0) - (s.charAt(j) == 'B' ? 1 : 0);
                    if (d == 0) expect = Math.max(expect, j - i + 1);
                }
            }
            if (longest(s) != expect) throw new AssertionError("random " + s);
        }
    }
}
```

#### Solution: [Boundary] Prefix From Zero (Author exercise)
<!-- id: ps-balanced-start -->

**Approach.**
The map stores balance 0 at index -1, so a span that begins at index 0 can match. A repeat at index `i` with stored index `p` is a span that covers indexes `p + 1` through `i`. Its start is `p + 1`, and its length is `i - p`. The method replaces the best pair only when the new length is strictly larger. Among spans of equal length, the one with the smaller start also has the smaller end, so the loop meets it first and keeps it. Without any repeat, the answer stays `[-1, 0]`.

**Complexity.**
- **Time** is O(n) expected, because each value costs one hash operation.
- **Space** is O(n) for the map of earliest indexes.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;

public final class BalancedStart {
    /**
     * Returns {start, length} of the longest balanced subarray, smaller start on ties, or {-1, 0}.
     * Time: O(n) expected, one hash operation per value.
     * Space: O(n) for the map of earliest indexes.
     * Invariant: first.get(b) is the smallest index at which the balance was b.
     */
    static int[] longest(int[] nums) {
        HashMap<Integer, Integer> first = new HashMap<>();
        first.put(0, -1);
        int bal = 0;
        int[] best = {-1, 0};
        for (int i = 0; i < nums.length; i++) {
            bal += nums[i] == 1 ? 1 : -1;
            Integer p = first.get(bal);
            if (p == null) {
                first.put(bal, i);
            } else if (i - p > best[1]) {
                // The span covers p + 1 through i, and a strict comparison keeps the smaller start on ties.
                best[0] = p + 1;
                best[1] = i - p;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(longest(new int[] {1, 0, 1, 1, 1}), new int[] {0, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(longest(new int[] {1, 1, 1}), new int[] {-1, 0})) throw new AssertionError("example 2");
        // Random binary arrays against the double loop with the same tie rule.
        Random rnd = new Random(19);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(14), 0, 2).toArray();
            int[] expect = {-1, 0};
            for (int i = 0; i < a.length; i++) {
                int d = 0;
                for (int j = i; j < a.length; j++) {
                    d += a[j] == 1 ? 1 : -1;
                    if (d == 0 && j - i + 1 > expect[1]) { expect[0] = i; expect[1] = j - i + 1; }
                }
            }
            if (!Arrays.equals(longest(a), expect)) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Longest Substring With Even Vowel Counts (LeetCode 1371)
<!-- id: ps-even-vowels-1371 -->

**Approach.**
The state is a 5 bit mask where bit `j` is 1 when vowel `j` has appeared an odd number of times. Reading a vowel flips its bit with `^`, and a consonant leaves the mask unchanged. Two boundaries with equal masks enclose a substring where every vowel flipped an even number of times. The mask takes only 32 values, so an array of 32 earliest indexes replaces the hash map. It starts with -2 as a marker for unseen states, and the mask 0 holds -1 for the position before the first character.

**Complexity.**
- **Time** is O(n), because each character costs a constant number of operations.
- **Space** is O(1), because the array has 32 entries whatever the length of `s`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class EvenVowels1371 {
    /**
     * Returns the length of the longest substring with an even count of each vowel.
     * Time: O(n), constant work per character.
     * Space: O(1), an array of 32 earliest indexes.
     * Invariant: first[m] is the smallest index with parity mask m, or -2 when unseen.
     */
    static int longest(String s) {
        // The value -2 marks an unseen mask, because -1 is a valid index for the empty prefix.
        int[] first = new int[32];
        Arrays.fill(first, -2);
        first[0] = -1;
        int mask = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            // The index of the vowel in "aeiou" selects the bit to flip.
            int j = "aeiou".indexOf(s.charAt(i));
            if (j >= 0) mask ^= 1 << j;
            // An unseen mask records its earliest index, and a repeat measures the span.
            if (first[mask] == -2) first[mask] = i;
            else best = Math.max(best, i - first[mask]);
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (longest("leetcodes") != 5) throw new AssertionError("example 1");
        if (longest("xyz") != 3) throw new AssertionError("example 2");
        // Random strings over a small alphabet against the double loop.
        Random rnd = new Random(20);
        String alphabet = "aeioubc";
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 1 + rnd.nextInt(14); i > 0; i--) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            int expect = 0;
            for (int i = 0; i < s.length(); i++) {
                for (int j = i; j < s.length(); j++) {
                    boolean ok = true;
                    for (char v : "aeiou".toCharArray()) {
                        int c = 0;
                        for (int k = i; k <= j; k++) if (s.charAt(k) == v) c++;
                        if (c % 2 != 0) ok = false;
                    }
                    if (ok) expect = Math.max(expect, j - i + 1);
                }
            }
            if (longest(s) != expect) throw new AssertionError("random " + s);
        }
    }
}
```
