<!-- solutions-for: 03-longest-valid-windows -->
### Longest-Valid Windows

#### Solution: [Build] Longest Binary Run With One Zero (Author exercise)
<!-- id: sw-run-one-zero -->

**Approach.** Keep a window from `left` to `right` and a counter of zeros inside it. Take in each new reading, and while the counter exceeds one, remove readings from the left until it does not. Measure the window after that repair.

**Complexity.** O(n) time, because each index enters and leaves the window at most once, and O(1) extra space.

```java run
public final class LongestBinaryRun {
    static int longestRun(int[] bits) {
        int left = 0, zeros = 0, best = 0;
        for (int right = 0; right < bits.length; right++) {
            if (bits[right] == 0) zeros++;
            while (zeros > 1) {
                if (bits[left] == 0) zeros--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestRun(new int[] {1, 1, 0, 1, 1, 1, 0, 1}) != 6) throw new AssertionError("example 1");
        if (longestRun(new int[] {0, 0, 0}) != 1) throw new AssertionError("example 2");
    }
}
```

#### Solution: [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-distinct-substring -->

**Approach.** The violation is now a repeated character, so the counter becomes a table of counts. Only the character that just arrived can be the duplicate, because the window was valid before it came in. Remove characters from the left until the count of the incoming character is back to one.

**Complexity.** O(n) time and O(1) space, since the table has a fixed size. The table covers ASCII only, which the constraints guarantee. For arbitrary UTF-16 text, use a `HashMap<Character, Integer>` instead.

```java run
public final class DistinctWindow {
    static int lengthOfLongestSubstring(String s) {
        int[] count = new int[128];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            char incoming = s.charAt(right);
            count[incoming]++;
            while (count[incoming] > 1) {
                count[s.charAt(left)]--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (lengthOfLongestSubstring("dvdfkd") != 4) throw new AssertionError("example 1");
        if (lengthOfLongestSubstring("tmmzuxt") != 5) throw new AssertionError("example 2");
        if (lengthOfLongestSubstring("") != 0) throw new AssertionError("empty string");
    }
}
```

#### Solution: [Boundary] Violation At Both Ends (Author exercise)
<!-- id: sw-left-boundaries -->

**Approach.** Reuse the repair loop unchanged and record `left` once the loop finishes for each `right`. The output shows the repair loop removing several elements in one step, as in the last entry of the first example.

**Complexity.** O(n) time and O(n) space for the returned array.

```java run
import java.util.Arrays;

public final class LeftBoundaries {
    static int[] leftAfterEachStep(int[] bits) {
        int[] leftAt = new int[bits.length];
        int left = 0, zeros = 0;
        for (int right = 0; right < bits.length; right++) {
            if (bits[right] == 0) zeros++;
            while (zeros > 1) {
                if (bits[left] == 0) zeros--;
                left++;
            }
            leftAt[right] = left;
        }
        return leftAt;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(leftAfterEachStep(new int[] {1, 1, 1, 0, 1, 0}), new int[] {0, 0, 0, 0, 0, 4}))
            throw new AssertionError("example 1");
        if (!Arrays.equals(leftAfterEachStep(new int[] {0, 0, 0}), new int[] {0, 1, 2}))
            throw new AssertionError("example 2");
    }
}
```

#### Solution: [Recognize] Max Consecutive Ones III (LeetCode 1004)
<!-- id: sw-flip-k-zeros -->

**Approach.** Flipping at most k zeros means the final run contains at most k zeros, so the problem asks for the longest window whose zero count is at most k. The limit is now a parameter. When k is 0, the repair loop can remove the whole window, and the measured length is correctly 0.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class FlipWindow {
    static int longestOnes(int[] nums, int k) {
        int left = 0, zeros = 0, best = 0;
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == 0) zeros++;
            while (zeros > k) {
                if (nums[left] == 0) zeros--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestOnes(new int[] {1, 0, 1, 0, 0, 1, 1}, 2) != 5) throw new AssertionError("example 1");
        if (longestOnes(new int[] {0, 0, 0}, 0) != 0) throw new AssertionError("example 2");
    }
}
```
