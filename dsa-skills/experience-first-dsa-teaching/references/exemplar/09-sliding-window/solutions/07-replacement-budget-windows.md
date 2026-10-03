<!-- solutions-for: 07-replacement-budget-windows -->
### Replacement-Budget Windows

#### Solution: [Build] Replacement Cost Of One Window (Author exercise)
<!-- id: sw-replacement-cost -->

**Approach.** Count the letters inside `left..right`, find the largest count, and return the length of the range minus that count. The largest count is the number of letters that can stay unchanged.

**Complexity.** O(right - left + 26) time and O(1) extra space.

```java run
public final class ReplacementCost {
    static int cost(String s, int left, int right) {
        int[] tally = new int[26];
        int most = 0;
        for (int i = left; i <= right; i++) {
            most = Math.max(most, ++tally[s.charAt(i) - 'A']);
        }
        return right - left + 1 - most;
    }

    public static void main(String[] args) {
        if (cost("AABAB", 0, 4) != 2) throw new AssertionError("example 1");
        if (cost("ZZZ", 0, 2) != 0) throw new AssertionError("example 2");
        if (cost("ABC", 1, 1) != 0) throw new AssertionError("single tile");
        if (cost("ABCD", 0, 3) != 3) throw new AssertionError("all different");
    }
}
```

#### Solution: [Vary] Longest Binary Uniform Window (Author exercise)
<!-- id: sw-binary-uniform -->

**Approach.** Keep two counters, one per symbol, for the current window. The cost of making the window uniform is its length minus the larger counter, and since there are only two counters the larger one can be read exactly at every step. Shrink from the left while the cost exceeds `k`.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class BinaryUniform {
    static int longestUniform(int[] bits, int k) {
        int[] count = new int[2];
        int left = 0, best = 0;
        for (int right = 0; right < bits.length; right++) {
            count[bits[right]]++;
            while (right - left + 1 - Math.max(count[0], count[1]) > k) {
                count[bits[left]]--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestUniform(new int[] {1, 0, 1, 1, 0, 0, 1}, 1) != 4) throw new AssertionError("example 1");
        if (longestUniform(new int[] {0, 1, 0, 1}, 0) != 1) throw new AssertionError("example 2");
        if (longestUniform(new int[] {1, 0, 1, 0}, 4) != 4) throw new AssertionError("large budget");
        if (longestUniform(new int[] {0}, 0) != 1) throw new AssertionError("single value");
    }
}
```

#### Solution: [Boundary] Stale Maximum Trace (Author exercise)
<!-- id: sw-stale-maximum -->

**Approach.** Run the algorithm with a stored `maxFreq` raised on arrival and never lowered. After the shrink loop for each `right`, scan the 26 tallies for the true maximum of the current stretch and count the positions where the stored value is strictly larger. The scan is read-only, so it does not disturb the algorithm being observed.

**Complexity.** O(26 * n) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class StaleMaximum {
    static int[] observe(String s, int k) {
        int[] tally = new int[26];
        int left = 0, maxFreq = 0, best = 0, stale = 0;
        for (int right = 0; right < s.length(); right++) {
            maxFreq = Math.max(maxFreq, ++tally[s.charAt(right) - 'A']);
            while (right - left + 1 - maxFreq > k) {
                tally[s.charAt(left) - 'A']--;
                left++;
            }
            best = Math.max(best, right - left + 1);
            int truth = 0;
            for (int c : tally) truth = Math.max(truth, c);
            if (maxFreq > truth) stale++;
        }
        return new int[] {best, stale};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(observe("AABABBA", 1), new int[] {4, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(observe("AAAA", 0), new int[] {4, 0})) throw new AssertionError("example 2");
        if (observe("ABCDE", 0)[0] != 1) throw new AssertionError("no repeats");
    }
}
```

#### Solution: [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-character-replacement -->

**Approach.** Keep a tally of the stretch and a stored `maxFreq` that is raised on arrival and never lowered. Shrink from the left while length minus `maxFreq` exceeds `k`. The reported length is always achievable by some real stretch, because a length of `maxFreq + k` is reached only after a real stretch had that dominant count.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class CharacterReplacement {
    static int characterReplacement(String s, int k) {
        int[] tally = new int[26];
        int left = 0, maxFreq = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            maxFreq = Math.max(maxFreq, ++tally[s.charAt(right) - 'A']);
            while (right - left + 1 - maxFreq > k) {
                tally[s.charAt(left) - 'A']--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (characterReplacement("BBABCBB", 1) != 4) throw new AssertionError("example 1");
        if (characterReplacement("QQRQQ", 0) != 2) throw new AssertionError("example 2");
        if (characterReplacement("AABABBA", 1) != 4) throw new AssertionError("lesson trace");
        if (characterReplacement("A", 0) != 1) throw new AssertionError("single");
        if (characterReplacement("ABCDE", 4) != 5) throw new AssertionError("budget covers all");
    }
}
```
