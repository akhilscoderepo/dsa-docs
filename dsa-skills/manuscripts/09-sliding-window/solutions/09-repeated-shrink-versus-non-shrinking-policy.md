<!-- solutions-for: 09-repeated-shrink-versus-non-shrinking-policy -->
### Repeated-Shrink Versus Non-Shrinking Policy

#### Solution: [Build] Restore Before Record (Author exercise)
<!-- id: sw-restore-before-record -->

**Approach.** Keep a map from value to its count inside the window. After adding the entry at `right`, remove entries from `left` in a `while` loop until the new value occurs once, then measure the width. The code re-checks the whole window by brute force right after the loop to assert that it is valid before it is measured, and it counts every move of each edge to show that each index enters once and leaves at most once. The array is copied before the call and compared afterwards to show that it was not modified. The oracle tries every subarray with a set.

**Complexity.** Each edge moves forward at most n times, so the loop makes at most 2n moves, giving O(n) expected time with a hash map and O(n) space for the map.

```java run
import java.util.*;

public final class RestoreBeforeRecord {
    static int moves;

    static boolean distinct(int[] a, int from, int to) {
        Set<Integer> s = new HashSet<>();
        for (int i = from; i <= to; i++) if (!s.add(a[i])) return false;
        return true;
    }

    static int longestDistinctRun(int[] nums) {
        Map<Integer, Integer> inside = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < nums.length; right++) {
            inside.merge(nums[right], 1, Integer::sum);
            moves++;
            while (inside.get(nums[right]) > 1) {
                inside.merge(nums[left++], -1, Integer::sum);
                moves++;
            }
            if (!distinct(nums, left, right)) throw new AssertionError("recorded an invalid window");
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int oracle(int[] a) {
        int best = 0;
        for (int i = 0; i < a.length; i++)
            for (int j = i; j < a.length; j++)
                if (distinct(a, i, j)) best = Math.max(best, j - i + 1);
        return best;
    }

    public static void main(String[] args) {
        if (longestDistinctRun(new int[] {4, 7, 4, 9, 7, 1}) != 4) throw new AssertionError("example 1");
        if (longestDistinctRun(new int[] {5, 5, 5}) != 1) throw new AssertionError("example 2");
        if (longestDistinctRun(new int[0]) != 0) throw new AssertionError("empty");
        if (longestDistinctRun(new int[] {Integer.MIN_VALUE}) != 1) throw new AssertionError("single");
        if (longestDistinctRun(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, Integer.MAX_VALUE}) != 2)
            throw new AssertionError("extremes");
        int[] big = new int[100000];
        for (int i = 0; i < big.length; i++) big[i] = i % 7;
        moves = 0;
        if (longestDistinctRun(big) != 7) throw new AssertionError("periodic");
        if (moves > 2 * big.length) throw new AssertionError("more than 2n moves: " + moves);
        Random rnd = new Random(901);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(8);
                a[i] = pick == 6 ? Integer.MAX_VALUE : pick == 7 ? Integer.MIN_VALUE : pick;
            }
            int[] copy = a.clone();
            int got = longestDistinctRun(a);
            if (!Arrays.equals(a, copy)) throw new AssertionError("input was modified");
            if (got != oracle(a)) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] One-Removal Maximum-Length Trace (Author exercise)
<!-- id: sw-one-removal-trace -->

**Approach.** Update the count of the new letter, raise `tracked` if that count is a record, and if `width - tracked` exceeds k remove exactly one letter at the left. Record the width after every character. The width after step i equals the best fixable run within the prefix read so far, which the check compares with a brute-force search over that prefix for every i. The width is therefore a length bound, not a description of the final window, and the check shows a case where the final window needs more than k repaints when its counts are examined exactly. The width sequence never decreases.

**Complexity.** Constant work per character, so O(n) time, plus O(n) for the returned array and O(1) for the counts.

```java run
import java.util.*;

public final class OneRemovalTrace {
    static int removals;

    static int[] widths(String s, int k) {
        int[] seen = new int[26];
        int[] out = new int[s.length()];
        int left = 0, tracked = 0;
        for (int right = 0; right < s.length(); right++) {
            tracked = Math.max(tracked, ++seen[s.charAt(right) - 'A']);
            if (right - left + 1 - tracked > k) {
                seen[s.charAt(left++) - 'A']--;
                removals++;
            }
            out[right] = right - left + 1;
        }
        return out;
    }

    static int bestInPrefix(String s, int end, int k) {
        int best = 0;
        for (int i = 0; i <= end; i++) {
            int[] c = new int[26];
            int most = 0;
            for (int j = i; j <= end; j++) {
                most = Math.max(most, ++c[s.charAt(j) - 'A']);
                if (j - i + 1 - most <= k) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    static int exactNeed(String s, int from, int to) {
        int[] c = new int[26];
        int most = 0;
        for (int j = from; j <= to; j++) most = Math.max(most, ++c[s.charAt(j) - 'A']);
        return to - from + 1 - most;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(widths("QQQRSTQ", 2), new int[] {1, 2, 3, 4, 5, 5, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(widths("ABAB", 0), new int[] {1, 1, 1, 1})) throw new AssertionError("example 2");
        if (widths("", 0).length != 0) throw new AssertionError("empty");
        if (!Arrays.equals(widths("Z", 0), new int[] {1})) throw new AssertionError("single");
        if (!Arrays.equals(widths("KKKK", 0), new int[] {1, 2, 3, 4})) throw new AssertionError("all equal");
        String hostile = "AAAABCDE";
        int[] w = widths(hostile, 1);
        int finalWidth = w[w.length - 1];
        if (exactNeed(hostile, hostile.length() - finalWidth, hostile.length() - 1) <= 1)
            throw new AssertionError("expected an unfixable final window");
        if (finalWidth != bestInPrefix(hostile, hostile.length() - 1, 1)) throw new AssertionError("width is the best length");
        Random rnd = new Random(902);
        for (int t = 0; t < 2500; t++) {
            int n = rnd.nextInt(13);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('A' + rnd.nextInt(rnd.nextBoolean() ? 3 : 26)));
            String s = sb.toString();
            int k = rnd.nextInt(n + 1);
            removals = 0;
            int[] got = widths(s, k);
            if (removals > n) throw new AssertionError("too many removals");
            for (int i = 0; i < n; i++) {
                if (got[i] != bestInPrefix(s, i, k)) throw new AssertionError("prefix " + i + " of " + s + " k " + k);
                if (i > 0 && got[i] < got[i - 1]) throw new AssertionError("width decreased");
            }
        }
    }
}
```

#### Solution: [Boundary] Multiple Left Removals Needed (Author exercise)
<!-- id: sw-multiple-left-removals -->

**Approach.** Count the values inside the window. After adding the entry at `right`, run a `while` loop that removes entries at `left` until no value exceeds c; since only the new value can exceed c, the loop stops as soon as one copy of it has left. Count the removals made in each step and keep the largest. The always-correct start is the smallest `left` for which the run is valid, which the oracle finds by brute force for each `right`; the burst of that step is the change of that start. A second routine replaces `while` by `if` and the check shows that on the first example it ends with a window that still breaks the limit. The input is not modified.

**Complexity.** Each index enters and leaves at most once, so the loop is O(n) expected time with O(n) space for the counts, and the removals over all steps sum to less than n.

```java run
import java.util.*;

public final class MultipleRemovals {
    static int[] longestWithLimit(int[] nums, int c) {
        Map<Integer, Integer> inside = new HashMap<>();
        int left = 0, best = 0, burst = 0, totalRemoved = 0;
        for (int right = 0; right < nums.length; right++) {
            inside.merge(nums[right], 1, Integer::sum);
            int removed = 0;
            while (inside.get(nums[right]) > c) {
                inside.merge(nums[left++], -1, Integer::sum);
                removed++;
            }
            totalRemoved += removed;
            burst = Math.max(burst, removed);
            best = Math.max(best, right - left + 1);
        }
        if (totalRemoved >= Math.max(1, nums.length)) throw new AssertionError("removals exceed length");
        return new int[] {best, burst};
    }

    static boolean valid(int[] a, int from, int to, int c) {
        Map<Integer, Integer> m = new HashMap<>();
        for (int i = from; i <= to; i++) if (m.merge(a[i], 1, Integer::sum) > c) return false;
        return true;
    }

    static int[] oracle(int[] a, int c) {
        int best = 0, burst = 0, prevStart = 0;
        for (int r = 0; r < a.length; r++) {
            int start = r;
            while (start > 0 && valid(a, start - 1, r, c)) start--;
            burst = Math.max(burst, start - prevStart);
            prevStart = start;
            best = Math.max(best, r - start + 1);
        }
        return new int[] {best, burst};
    }

    static boolean ifVariantEndsValid(int[] nums, int c) {
        Map<Integer, Integer> inside = new HashMap<>();
        int left = 0;
        for (int right = 0; right < nums.length; right++) {
            inside.merge(nums[right], 1, Integer::sum);
            if (inside.get(nums[right]) > c) inside.merge(nums[left++], -1, Integer::sum);
        }
        return valid(nums, left, nums.length - 1, c);
    }

    public static void main(String[] args) {
        int[] ex1 = {9, 8, 7, 1, 1, 2, 1};
        if (!Arrays.equals(longestWithLimit(ex1, 2), new int[] {6, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(longestWithLimit(new int[] {3, 3, 3, 3}, 1), new int[] {1, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(longestWithLimit(new int[0], 1), new int[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(longestWithLimit(new int[] {Integer.MIN_VALUE}, 1), new int[] {1, 0})) throw new AssertionError("single");
        if (!Arrays.equals(longestWithLimit(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE}, 5), new int[] {2, 0}))
            throw new AssertionError("limit above counts");
        if (ifVariantEndsValid(ex1, 2)) throw new AssertionError("if variant should end with a broken window");
        Random rnd = new Random(903);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(5);
                a[i] = pick == 3 ? Integer.MIN_VALUE : pick == 4 ? Integer.MAX_VALUE : pick;
            }
            int c = 1 + rnd.nextInt(3);
            int[] copy = a.clone();
            int[] got = longestWithLimit(a, c);
            if (!Arrays.equals(a, copy)) throw new AssertionError("input was modified");
            if (!Arrays.equals(got, oracle(a, c))) throw new AssertionError("differs on " + Arrays.toString(a) + " c " + c);
        }
    }
}
```

#### Solution: [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-replacement-both-forms -->

**Approach.** The always-valid form takes the exact largest count by scanning the 26 counts and shrinks with a `while` until `width - exact` is at most k. The non-shrinking form keeps `tracked` as a maximum that never falls, removes one letter when `width - tracked` exceeds k, and returns the number of letters minus `left`. The two forms agree because the width of the second grows only through a record count that sits under the current window. At the end the tracked value can exceed the exact largest count of the final window, which the check demonstrates on the first example and counts over random strings. Both lengths are compared with a brute force over all substrings, the string is only read, and the first form's condition is evaluated fewer than twice per letter.

**Complexity.** The always-valid form is O(26 n) time, the non-shrinking form is O(n) time, and both use O(1) extra space for the 26 counts.

```java run
import java.util.*;

public final class RepeatedShrinkForms {
    static int checks;

    static int exactMax(int[] seen) {
        int m = 0;
        for (int v : seen) m = Math.max(m, v);
        return m;
    }

    static int alwaysValid(String s, int k) {
        int[] seen = new int[26];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            seen[s.charAt(right) - 'A']++;
            while (true) {
                checks++;
                if (right - left + 1 - exactMax(seen) <= k) break;
                seen[s.charAt(left++) - 'A']--;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int[] report(String s, int k) {
        int[] seen = new int[26];
        int left = 0, tracked = 0;
        for (int right = 0; right < s.length(); right++) {
            tracked = Math.max(tracked, ++seen[s.charAt(right) - 'A']);
            if (right - left + 1 - tracked > k) seen[s.charAt(left++) - 'A']--;
        }
        return new int[] {alwaysValid(s, k), s.length() - left, tracked, exactMax(seen)};
    }

    static int oracle(String s, int k) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            int[] c = new int[26];
            for (int j = i; j < s.length(); j++) {
                c[s.charAt(j) - 'A']++;
                if (j - i + 1 - exactMax(c) <= k) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(report("AAAABCDE", 1), new int[] {5, 5, 4, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(report("ABAB", 2), new int[] {4, 4, 2, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(report("", 0), new int[] {0, 0, 0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(report("Z", 0), new int[] {1, 1, 1, 1})) throw new AssertionError("single");
        if (!Arrays.equals(report("MMMM", 0), new int[] {4, 4, 4, 4})) throw new AssertionError("all equal");
        Random rnd = new Random(904);
        int stale = 0;
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(15);
            StringBuilder sb = new StringBuilder();
            int alphabet = rnd.nextBoolean() ? 3 : 26;
            for (int i = 0; i < n; i++) sb.append((char) ('A' + rnd.nextInt(alphabet)));
            String s = sb.toString();
            int k = rnd.nextInt(n + 2);
            checks = 0;
            int[] r = report(s, k);
            if (checks >= 2 * Math.max(1, n) + 1) throw new AssertionError("too many checks: " + checks);
            int truth = oracle(s, k);
            if (r[0] != truth || r[1] != truth) throw new AssertionError("differs on " + s + " k " + k);
            if (r[2] < r[3]) throw new AssertionError("tracked below exact");
            if (r[2] > r[3]) stale++;
        }
        if (stale == 0) throw new AssertionError("no case with a stale maximum");
    }
}
```
