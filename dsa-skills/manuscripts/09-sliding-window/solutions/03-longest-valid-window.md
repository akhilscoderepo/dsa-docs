<!-- solutions-for: 09-sliding-window -->
### Solutions For Longest Valid Windows

#### Solution: [Build] Longest Binary Run With One Zero (Author exercise)
<!-- id: sw-one-zero -->

**Approach.**
The method expands `right` one index at a time and counts the zeros inside the window. When the count reaches two, a `while` loop moves `left` forward and subtracts one each time `left` passes a zero. The loop stops when one zero remains. After the loop the window is valid, so the method compares its length with `best`. The invariant is that, after the loop, `zeros` equals the number of zeros in `bits[left..right]` and is at most one.

**Complexity.**
- **Time** is O(n), because `right` advances `n` times and `left` advances at most `n` times in total.
- **Space** is O(1), because the method keeps three integers.

```java run
import java.util.Random;

public final class OneZeroRun {
    /**
     * Returns the longest block with at most one zero.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), three integers.
     * Invariant: after the shrink loop, zeros equals the zero count of bits[left..right] and is at most 1.
     */
    static int longest(int[] bits) {
        // left starts at 0 and only increases.
        int left = 0, zeros = 0, best = 0;
        // Expand: one new value enters per iteration, so the loop runs n times.
        for (int right = 0; right < bits.length; right++) {
            // A zero entering raises the violation count.
            if (bits[right] == 0) zeros++;
            // Shrink: runs while the window holds two zeros; total work over the call is at most n steps.
            while (zeros > 1) {
                // A zero leaving lowers the violation count.
                if (bits[left] == 0) zeros--;
                // Moving left removes bits[left] from the window.
                left++;
            }
            // The window is valid here, so its length is a legal candidate.
            best = Math.max(best, right - left + 1);
        }
        // An empty array never enters the loop, so best stays 0.
        return best;
    }

    /** Oracle: tests every block directly. */
    static int oracle(int[] a) {
        int best = 0;
        for (int i = 0; i < a.length; i++) for (int j = i; j < a.length; j++) {
            int z = 0;
            for (int x = i; x <= j; x++) if (a[x] == 0) z++;
            if (z <= 1) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2, plus the empty array.
        if (longest(new int[] {1, 1, 0, 1, 0, 1, 1}) != 4) throw new AssertionError("example 1");
        if (longest(new int[] {0, 0, 0}) != 1) throw new AssertionError("example 2");
        if (longest(new int[0]) != 0) throw new AssertionError("empty");
        // Random binary arrays agree with the oracle.
        Random rnd = new Random(21);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(2);
            if (longest(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-longest-no-repeat -->

**Approach.**
The state is a count per character inside the window. The entering character raises its count. While that count exceeds one, the method removes `s.charAt(left)` from the counts and moves `left` forward. The loop can run several times for one `right`, because the repeated character can sit deep inside the window. After the loop every count is at most one, so the window has no repeated character, and the method records its length. The invariant is that, after the loop, every entry of `cnt` for a character in the window is exactly one, and the other entries are zero.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1) for the ASCII table of 128 entries, and O(min(n, alphabet)) for a map over a larger alphabet.

```java run
import java.util.Random;

public final class LongestNoRepeat {
    /**
     * Returns the length of the longest substring with no repeated character (ASCII input).
     * Time: O(n), each index enters once and leaves at most once.
     * Space: O(1), a count table of 128 entries.
     * Invariant: after the shrink loop, no entry of cnt exceeds 1.
     */
    static int longest(String s) {
        // One counter per ASCII code.
        int[] cnt = new int[128];
        int left = 0, best = 0;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            // The entering character raises its own count.
            cnt[c]++;
            // Shrink: runs while the entering character appears twice; each pass removes the leftmost character.
            while (cnt[c] > 1) {
                // The leaving character lowers its count before left moves.
                cnt[s.charAt(left)]--;
                left++;
            }
            // The window has no repeats, so its length is a candidate.
            best = Math.max(best, right - left + 1);
        }
        // The longest valid length seen over all right ends.
        return best;
    }

    /** Oracle: tests every substring with a set. */
    static int oracle(String s) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            java.util.Set<Character> seen = new java.util.HashSet<>();
            for (int j = i; j < s.length() && seen.add(s.charAt(j)); j++) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement, plus the empty string.
        if (longest("abcdbea") != 5) throw new AssertionError("example 1");
        if (longest("aaaa") != 1) throw new AssertionError("example 2");
        if (longest("") != 0) throw new AssertionError("empty");
        // Random strings over a small alphabet agree with the oracle.
        Random rnd = new Random(22);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(15); i < n; i++) sb.append((char) ('a' + rnd.nextInt(5)));
            if (longest(sb.toString()) != oracle(sb.toString())) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Violation At Both Ends (Author exercise)
<!-- id: sw-many-removals -->

**Approach.**
The method runs the longest-substring scan and tracks `left` after the shrink loop for each `right`. After the loop, `left` equals `first(r)`, the smallest valid start for that `r`. The jump at `r` is the new `left` minus the previous `left`, and the method keeps the largest jump. Because the jump can exceed one, the shrink step must be a `while` loop. An `if` removes one character per `right`, leaves a repeat in the window, and reports a smaller jump. The invariant is that `left` equals `first(r)` after each loop.

**Complexity.**
- **Time** is O(n), because `left` moves forward at most `n` times in total.
- **Space** is O(1), because the method keeps a table of 26 entries and a few integers.

```java run
import java.util.Random;

public final class ManyRemovals {
    /**
     * Returns the largest forward jump of left at a single right index.
     * Time: O(n), left only moves forward.
     * Space: O(1), a table of 26 counters.
     * Invariant: after the shrink loop, left equals the smallest valid start for right.
     */
    static int largestJump(String s) {
        int[] cnt = new int[26];
        int left = 0, bestJump = 0;
        // Expand: one character enters per iteration.
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            cnt[c - 'a']++;
            // Remember where left was before restoring validity.
            int before = left;
            // Shrink: the loop may run several times for one right.
            while (cnt[c - 'a'] > 1) {
                cnt[s.charAt(left) - 'a']--;
                left++;
            }
            // The jump is the number of removals made for this right.
            bestJump = Math.max(bestJump, left - before);
        }
        // For an empty string the loop does not run and the answer is 0.
        return bestJump;
    }

    /** Wrong variant: a single removal with if, to show the difference. */
    static int largestJumpWithIf(String s) {
        int[] cnt = new int[26];
        int left = 0, bestJump = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            cnt[c - 'a']++;
            int before = left;
            if (cnt[c - 'a'] > 1) { cnt[s.charAt(left) - 'a']--; left++; }
            bestJump = Math.max(bestJump, left - before);
        }
        return bestJump;
    }

    /** Oracle: finds first(r) by testing every start. */
    static int oracle(String s) {
        int prev = 0, best = 0;
        for (int r = 0; r < s.length(); r++) {
            int l = 0;
            while (true) {
                boolean dup = false;
                for (int i = l; i <= r; i++) for (int j = i + 1; j <= r; j++) if (s.charAt(i) == s.charAt(j)) dup = true;
                if (!dup) break;
                l++;
            }
            best = Math.max(best, l - prev);
            prev = l;
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2.
        if (largestJump("abcdbea") != 2) throw new AssertionError("example 1");
        if (largestJump("abc") != 0) throw new AssertionError("example 2");
        // The if variant reports a smaller jump on example 1, so a while loop is needed.
        if (largestJumpWithIf("abcdbea") != 1) throw new AssertionError("if variant");
        // Random strings agree with the oracle.
        Random rnd = new Random(23);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(14); i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            if (largestJump(sb.toString()) != oracle(sb.toString())) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Max Consecutive Ones III (LeetCode 1004)
<!-- id: sw-max-ones-k -->

**Approach.**
The window may hold at most `k` zeros, so the shrink loop runs while the zero count exceeds `k`. When `k` is 0 the loop removes every zero that enters, and the window collapses to empty at each zero. The method records the length after the loop. The invariant is that, after the loop, the window holds at most `k` zeros, and every start before `left` is unusable for this and later `right` values.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1), because the method keeps three integers.

```java run
import java.util.Random;

public final class MaxOnesK {
    /**
     * Returns the longest block with at most k zeros.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), three integers.
     * Invariant: after the shrink loop, zeros <= k and zeros counts nums[left..right].
     */
    static int longestOnes(int[] nums, int k) {
        int left = 0, zeros = 0, best = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < nums.length; right++) {
            // A zero raises the violation count.
            if (nums[right] == 0) zeros++;
            // Shrink: runs while the window holds more than k zeros; with k = 0 it empties the window at each zero.
            while (zeros > k) {
                // Leaving a zero lowers the violation count.
                if (nums[left] == 0) zeros--;
                left++;
            }
            // The window is valid; an empty window gives length 0.
            best = Math.max(best, right - left + 1);
        }
        // Return the longest valid length.
        return best;
    }

    /** Oracle: tests every block. */
    static int oracle(int[] a, int k) {
        int best = 0;
        for (int i = 0; i < a.length; i++) for (int j = i; j < a.length; j++) {
            int z = 0;
            for (int x = i; x <= j; x++) if (a[x] == 0) z++;
            if (z <= k) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (longestOnes(new int[] {1, 0, 0, 1, 1, 0, 1}, 2) != 5) throw new AssertionError("example 1");
        if (longestOnes(new int[] {0, 0, 0}, 0) != 0) throw new AssertionError("example 2");
        // Random arrays and limits agree with the oracle.
        Random rnd = new Random(24);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(2);
            int k = rnd.nextInt(a.length + 1);
            if (longestOnes(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```
