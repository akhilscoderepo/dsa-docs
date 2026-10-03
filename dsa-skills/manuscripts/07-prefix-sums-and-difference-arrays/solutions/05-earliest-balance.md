<!-- solutions-for: 07-earliest-balance -->
### Earliest Balance

#### Solution: [Build] Contiguous Array (LeetCode 525)
<!-- id: ps-contiguous-array -->

**Approach.** Replace each zero by minus one and keep a running balance. A stretch has equal zeros and ones exactly when the balance at its end equals the balance before its start. The longest such stretch for a given end is the one that starts after the earliest occurrence of that balance, so the table maps each balance to the first index at which it was reached, and a repeated balance is used to measure a length without overwriting the entry. The table starts with balance zero at index minus one, which stands for the moment before the array. The oracle checks every stretch for equal counts.

**Complexity.** One pass, linear expected time, and space proportional to the number of distinct balances.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class ContiguousArray {
    static int findMaxLength(int[] nums) {
        Map<Integer, Integer> first = new HashMap<>();
        first.put(0, -1);
        int balance = 0, best = 0;
        for (int i = 0; i < nums.length; i++) {
            balance += nums[i] == 1 ? 1 : -1;
            Integer earlier = first.get(balance);
            if (earlier == null) first.put(balance, i);
            else best = Math.max(best, i - earlier);
        }
        return best;
    }
    static int oracle(int[] nums) {
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            int ones = 0, zeros = 0;
            for (int j = i; j < nums.length; j++) {
                if (nums[j] == 1) ones++;
                else zeros++;
                if (ones == zeros) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (findMaxLength(new int[] {0, 1, 0, 0, 1, 1, 0}) != 6) throw new AssertionError("example 1");
        if (findMaxLength(new int[] {1, 1, 1, 0}) != 2) throw new AssertionError("example 2");
        if (findMaxLength(new int[] {1, 1, 1}) != 0) throw new AssertionError("no stretch qualifies");
        Random rnd = new Random(7501);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            if (findMaxLength(a) != oracle(a)) throw new AssertionError("differs on " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Equal A And B (Author exercise)
<!-- id: ps-equal-a-and-b -->

**Approach.** The balance rises by one on `A`, falls by one on `B`, and stays the same on any other character. A stretch holds equal numbers of `A` and `B` exactly when the balance at its end equals the balance before its start, and neutral characters do not disturb that. The table keeps the first index of each balance, starting with zero at minus one. A string with no `A` and no `B` has balance zero throughout, so the whole string qualifies, and an empty string gives zero. The oracle counts both letters in every stretch.

**Complexity.** One pass, linear expected time, and space proportional to the number of distinct balances.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class EqualAAndB {
    static int longestEqualAB(String s) {
        Map<Integer, Integer> first = new HashMap<>();
        first.put(0, -1);
        int balance = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == 'A') balance++;
            else if (c == 'B') balance--;
            Integer earlier = first.get(balance);
            if (earlier == null) first.put(balance, i);
            else best = Math.max(best, i - earlier);
        }
        return best;
    }
    static int oracle(String s) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            int a = 0, b = 0;
            for (int j = i; j < s.length(); j++) {
                if (s.charAt(j) == 'A') a++;
                if (s.charAt(j) == 'B') b++;
                if (a == b) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestEqualAB("ABxxBAxA") != 7) throw new AssertionError("example 1");
        if (longestEqualAB("xyz") != 3) throw new AssertionError("example 2");
        if (longestEqualAB("") != 0) throw new AssertionError("empty string");
        if (longestEqualAB("AAA") != 0) throw new AssertionError("only one kind");
        Random rnd = new Random(7502);
        String letters = "ABxy";
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(letters.charAt(rnd.nextInt(4)));
            String s = sb.toString();
            if (longestEqualAB(s) != oracle(s)) throw new AssertionError("differs on " + s);
        }
    }
}
```

#### Solution: [Boundary] Prefix From Zero (Author exercise)
<!-- id: ps-prefix-from-zero -->

**Approach.** A stretch that begins at index zero pairs its end with the moment before the array, when the balance was zero. If the table has no entry for that moment, the pair is never found, and only stretches that start later are examined. Initializing zero at index minus one makes the length `i - (-1) = i + 1` come out right. The program contains both versions: the unseeded one returns 2 on the first example where the true answer is 4, and the seeded one agrees with the oracle on random arrays, including arrays where the longest stretch starts at zero.

**Complexity.** One pass, linear expected time, and space proportional to the number of distinct balances.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class PrefixFromZero {
    static int seeded(int[] nums) {
        Map<Integer, Integer> first = new HashMap<>();
        first.put(0, -1);
        int balance = 0, best = 0;
        for (int i = 0; i < nums.length; i++) {
            balance += nums[i] == 1 ? 1 : -1;
            Integer earlier = first.get(balance);
            if (earlier == null) first.put(balance, i);
            else best = Math.max(best, i - earlier);
        }
        return best;
    }
    static int unseeded(int[] nums) {
        Map<Integer, Integer> first = new HashMap<>();
        int balance = 0, best = 0;
        for (int i = 0; i < nums.length; i++) {
            balance += nums[i] == 1 ? 1 : -1;
            Integer earlier = first.get(balance);
            if (earlier == null) first.put(balance, i);
            else best = Math.max(best, i - earlier);
        }
        return best;
    }
    static int oracle(int[] nums) {
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            int bal = 0;
            for (int j = i; j < nums.length; j++) {
                bal += nums[j] == 1 ? 1 : -1;
                if (bal == 0) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (seeded(new int[] {1, 0, 1, 0, 0, 0}) != 4) throw new AssertionError("example 1");
        if (seeded(new int[] {1, 1, 0, 0}) != 4) throw new AssertionError("example 2");
        if (unseeded(new int[] {1, 0, 1, 0, 0, 0}) == 4) throw new AssertionError("the unseeded table should miss the stretch from zero");
        Random rnd = new Random(7503);
        boolean fromZeroSeen = false;
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            int want = oracle(a);
            if (seeded(a) != want) throw new AssertionError("seeded differs on " + java.util.Arrays.toString(a));
            if (unseeded(a) < want) fromZeroSeen = true;
            if (unseeded(a) > want) throw new AssertionError("an unseeded table cannot exceed the truth");
        }
        if (!fromZeroSeen) throw new AssertionError("random inputs should expose the missing seed");
    }
}
```

#### Solution: [Recognize] Find the Longest Substring Containing Vowels in Even Counts (LeetCode 1371)
<!-- id: ps-even-vowels -->

**Approach.** Each vowel flips one bit of a five-bit mask, so the mask records which vowels have appeared an odd number of times so far. A substring has every vowel an even number of times exactly when the mask at its end equals the mask before its start, because the flips between the two cancel in pairs. As in the balance problems, the longest substring for an end is the one starting after the earliest occurrence of its mask, so a table of 32 entries stores the first index of each mask, with mask zero at index minus one. The oracle counts each vowel in every substring.

**Complexity.** One pass, linear time, and a table of 32 slots.

```java run
import java.util.Arrays;
import java.util.Random;

public final class EvenVowels {
    static int findTheLongestSubstring(String s) {
        int[] firstSeen = new int[32];
        Arrays.fill(firstSeen, -2);
        firstSeen[0] = -1;
        int mask = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            int bit = "aeiou".indexOf(s.charAt(i));
            if (bit >= 0) mask ^= 1 << bit;
            if (firstSeen[mask] == -2) firstSeen[mask] = i;
            else best = Math.max(best, i - firstSeen[mask]);
        }
        return best;
    }
    static int oracle(String s) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            int[] c = new int[5];
            for (int j = i; j < s.length(); j++) {
                int v = "aeiou".indexOf(s.charAt(j));
                if (v >= 0) c[v]++;
                boolean ok = true;
                for (int x : c) if (x % 2 != 0) ok = false;
                if (ok) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (findTheLongestSubstring("eleetminicoworoep") != 13) throw new AssertionError("example 1");
        if (findTheLongestSubstring("aeiou") != 0) throw new AssertionError("example 2");
        if (findTheLongestSubstring("bcbcbc") != 6) throw new AssertionError("no vowels at all");
        Random rnd = new Random(7504);
        String letters = "aeioubcd";
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(letters.charAt(rnd.nextInt(letters.length())));
            String s = sb.toString();
            if (findTheLongestSubstring(s) != oracle(s)) throw new AssertionError("differs on " + s);
        }
    }
}
```
