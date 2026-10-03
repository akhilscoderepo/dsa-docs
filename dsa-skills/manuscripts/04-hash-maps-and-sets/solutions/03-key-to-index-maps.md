<!-- solutions-for: 03-key-to-index-maps -->
### Key To Index Maps

#### Solution: [Build] Two Sum (LeetCode 1)
<!-- id: hm-two-sum -->

**Approach.** For each position, ask the map for the complement `target - nums[i]`. A hit returns the stored position and the current one. A miss stores the current value with its position and moves on. The lookup happens before the store, so a value can never pair with itself, and a duplicate such as `[4, 4]` is found when the second copy arrives. The assertions check every random answer by adding the two chosen values and requiring distinct indices in increasing order, and they check that an answer exists exactly when the all-pairs oracle finds one.

**Complexity.** Expected O(n) time and O(n) extra space.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class TwoSum {
    static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> at = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            Integer j = at.get(target - nums[i]);
            if (j != null) return new int[] {j, i};
            at.put(nums[i], i);
        }
        return new int[] {};
    }
    static boolean exists(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (nums[i] + nums[j] == target) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(twoSum(new int[] {8, 2, 11, 3}, 14), new int[] {2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(twoSum(new int[] {4, 4}, 8), new int[] {0, 1})) throw new AssertionError("example 2");
        if (twoSum(new int[] {3, 7, 3}, 6).length != 2) throw new AssertionError("second 3 finds the first");
        if (twoSum(new int[] {3}, 6).length != 0) throw new AssertionError("a value must not pair with itself");
        Random rnd = new Random(51);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[2 + rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(14) - 5;
            int target = rnd.nextInt(20) - 6;
            int[] got = twoSum(x, target);
            if (exists(x, target)) {
                if (got.length != 2 || got[0] >= got[1] || x[got[0]] + x[got[1]] != target) throw new AssertionError("invalid pair");
            } else if (got.length != 0) throw new AssertionError("no pair exists");
        }
    }
}
```

#### Solution: [Vary] Contains Duplicate II (LeetCode 219)
<!-- id: hm-contains-duplicate-two -->

**Approach.** Store the latest position of every value. For each position, look up the previous position of the same value. If it exists and the gap is at most `k`, return true. Then overwrite the entry with the current position, since the latest copy is always the closest one for later positions. Keeping the first position would compare against copies that are farther away than necessary and could miss a valid pair, as the third and fourth 5 of `[5, 1, 5, 5]` show with `k = 1`. The oracle checks all pairs, and the assertions include that case and random arrays with random `k`.

**Complexity.** Expected O(n) time and O(n) extra space.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class ContainsDuplicateTwo {
    static boolean nearbyDuplicate(int[] nums, int k) {
        Map<Integer, Integer> last = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            Integer j = last.get(nums[i]);
            if (j != null && i - j <= k) return true;
            last.put(nums[i], i);
        }
        return false;
    }
    static boolean keepsFirst(int[] nums, int k) {
        Map<Integer, Integer> first = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            Integer j = first.get(nums[i]);
            if (j != null && i - j <= k) return true;
            first.putIfAbsent(nums[i], i);
        }
        return false;
    }
    static boolean oracle(int[] nums, int k) {
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length && j - i <= k; j++)
                if (nums[i] == nums[j]) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!nearbyDuplicate(new int[] {6, 2, 6}, 2)) throw new AssertionError("example 1");
        if (nearbyDuplicate(new int[] {6, 2, 3, 6}, 2)) throw new AssertionError("example 2");
        if (!nearbyDuplicate(new int[] {5, 1, 5, 5}, 1)) throw new AssertionError("latest copy is within range");
        if (keepsFirst(new int[] {5, 1, 5, 5}, 1)) throw new AssertionError("keeping the first copy misses the close pair");
        if (nearbyDuplicate(new int[] {}, 3)) throw new AssertionError("empty array");
        Random rnd = new Random(52);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(6);
            int k = rnd.nextInt(6);
            if (nearbyDuplicate(x, k) != oracle(x, k)) throw new AssertionError("disagrees with the pair check");
        }
    }
}
```

#### Solution: [Boundary] First Index Wins (Author exercise)
<!-- id: hm-first-index-wins -->

**Approach.** Use `putIfAbsent` so a value keeps the position of its first sighting, then read the stored position for every element. Overwriting with `put` while reading the previous entry would report the preceding copy, so `[5, 5, 5]` would give `[0, 0, 1]` and never the required `[0, 0, 0]`. The assertions show both the correct result and the overwriting variant's result on the examples, and compare the correct method with a linear search for the first equal value on random arrays.

**Complexity.** Expected O(n) time and O(n) extra space.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class FirstIndexWins {
    static int[] firstOccurrence(int[] nums) {
        Map<Integer, Integer> first = new HashMap<>();
        int[] out = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            first.putIfAbsent(nums[i], i);
            out[i] = first.get(nums[i]);
        }
        return out;
    }
    static int[] overwritingPrevious(int[] nums) {
        Map<Integer, Integer> last = new HashMap<>();
        int[] out = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            Integer prev = last.get(nums[i]);
            out[i] = prev == null ? i : prev;
            last.put(nums[i], i);
        }
        return out;
    }
    static int[] oracle(int[] nums) {
        int[] out = new int[nums.length];
        for (int j = 0; j < nums.length; j++) {
            int i = 0;
            while (nums[i] != nums[j]) i++;
            out[j] = i;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(firstOccurrence(new int[] {7, 3, 7, 7}), new int[] {0, 1, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(firstOccurrence(new int[] {5, 5, 5}), new int[] {0, 0, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(overwritingPrevious(new int[] {5, 5, 5}), new int[] {0, 0, 1})) throw new AssertionError("the overwriting variant reports the previous copy");
        if (firstOccurrence(new int[] {}).length != 0) throw new AssertionError("empty array");
        Random rnd = new Random(53);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(5);
            if (!Arrays.equals(firstOccurrence(x), oracle(x))) throw new AssertionError("disagrees with the linear search");
        }
    }
}
```

#### Solution: [Recognize] Widest Equal-Value Pair (Author exercise)
<!-- id: hm-widest-equal-pair -->

**Approach.** For each position, the widest pair ending there uses the earliest copy of the same value, so store each value's first position and compute `i - first` for every later sighting, tracking the maximum. A value seen for the first time contributes 0. Overwriting the stored position would measure distance to the nearest copy and could understate the answer, as `[4, 1, 9, 4, 2, 4]` shows: the nearest copy gives at most 3, while the first gives 5. The oracle tries all pairs, and the assertions run both on random arrays and require the same maximum.

**Complexity.** Expected O(n) time and O(n) extra space.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class WidestEqualPair {
    static int widest(int[] nums) {
        Map<Integer, Integer> first = new HashMap<>();
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            Integer f = first.putIfAbsent(nums[i], i);
            if (f != null) best = Math.max(best, i - f);
        }
        return best;
    }
    static int nearestOnly(int[] nums) {
        Map<Integer, Integer> last = new HashMap<>();
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            Integer j = last.put(nums[i], i);
            if (j != null) best = Math.max(best, i - j);
        }
        return best;
    }
    static int oracle(int[] nums) {
        int best = 0;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (nums[i] == nums[j]) best = Math.max(best, j - i);
        return best;
    }

    public static void main(String[] args) {
        if (widest(new int[] {4, 1, 9, 4, 2, 4}) != 5) throw new AssertionError("example 1");
        if (widest(new int[] {1, 2, 3}) != 0) throw new AssertionError("example 2");
        if (nearestOnly(new int[] {4, 1, 9, 4, 2, 4}) != 3) throw new AssertionError("the nearest copy understates the answer");
        if (widest(new int[] {}) != 0) throw new AssertionError("empty array");
        Random rnd = new Random(54);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(14)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(6);
            if (widest(x) != oracle(x)) throw new AssertionError("disagrees with the pair check");
        }
    }
}
```
