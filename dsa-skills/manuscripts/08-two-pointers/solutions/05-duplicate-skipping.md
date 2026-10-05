<!-- solutions-for: 08-two-pointers -->
### Solutions For Skipping Repeated Values

#### Solution: [Build] Unique Pairs (Author exercise)
<!-- id: tp-unique-pairs -->

**Approach.**
The pair scan from the opposite ends compares the sum with the target and moves the pointer that cannot help. A match is recorded first. After the recording, `left` moves past every index that holds the recorded left value, and `right` moves past every index that holds the recorded right value. The guard `left < right` keeps the skips from crossing, so `[2, 2, 2]` with target 4 records `[2, 2]` once. The invariant is that each value combination with the target sum is either recorded exactly once or lies between `left` and `right`.

**Complexity.**
- **Time** is O(n), because each pointer moves in one direction and every index is passed at most once, including the skipped ones.
- **Space** is O(1) beyond the output list.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class UniquePairs {
    /**
     * Returns each distinct value pair of a sorted array that sums to target.
     * Time: O(n).
     * Space: O(1) beyond the output.
     * Invariant: every distinct matching pair is recorded once or lies in [left, right].
     */
    static List<List<Integer>> uniquePairs(int[] nums, long target) {
        List<List<Integer>> out = new ArrayList<>();
        int left = 0, right = nums.length - 1;
        // Each pass moves at least one pointer, so the loop makes at most n steps.
        while (left < right) {
            long sum = (long) nums[left] + nums[right];
            // Below the target: the left value cannot reach it with any value in the range.
            if (sum < target) left++;
            // Above the target: the right value cannot reach it with any value in the range.
            else if (sum > target) right--;
            else {
                // Record the representative pair before any skip.
                int a = nums[left], b = nums[right];
                out.add(List.of(a, b));
                // Skip the whole runs of both recorded values.
                while (left < right && nums[left] == a) left++;
                while (left < right && nums[right] == b) right--;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!uniquePairs(new int[] {1, 1, 2, 3, 3, 4, 5}, 6).equals(List.of(List.of(1, 5), List.of(2, 4), List.of(3, 3)))) throw new AssertionError("example 1");
        if (!uniquePairs(new int[] {2, 2, 2}, 4).equals(List.of(List.of(2, 2)))) throw new AssertionError("example 2");
        // The empty array and one value return nothing.
        if (!uniquePairs(new int[0], 0).isEmpty() || !uniquePairs(new int[] {2}, 4).isEmpty()) throw new AssertionError("short");
        // Random sorted arrays against all index pairs collected in a set.
        Random rnd = new Random(51);
        for (int t = 0; t < 4000; t++) {
            int[] a = rnd.ints(rnd.nextInt(10), -4, 5).sorted().toArray();
            long target = rnd.nextInt(11) - 5;
            TreeSet<String> expect = new TreeSet<>();
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) if (a[i] + a[j] == target) expect.add(a[i] + "," + a[j]);
            List<String> got = new ArrayList<>();
            for (List<Integer> p : uniquePairs(a, target)) got.add(p.get(0) + "," + p.get(1));
            // The set holds each combination once, and the scan emits them in increasing order of the first value.
            if (got.size() != expect.size() || !new TreeSet<>(got).equals(expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] 3Sum (LeetCode 15)
<!-- id: tp-three-sum-unique -->

**Approach.**
The method sorts a copy of the input, so the caller's array stays unchanged. The outer loop fixes the first value at index `i`. It skips an `i` whose value equals the previous fixed value, because the previous run was fully processed. For each fixed value the pair scan runs on the indexes after `i` with the target `-nums[i]`. After a recorded triplet, both pointers skip the whole runs of the recorded values. The invariant is that every distinct triplet with a first value before `nums[i]` is already recorded.

**Complexity.**
- **Time** is O(n^2), because the sort costs O(n log n) and each of at most `n` fixed values triggers one O(n) pair scan.
- **Space** is O(n) for the sorted copy, and O(1) beyond it and the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class ThreeSumUnique15 {
    /**
     * Returns the distinct triplets that sum to zero in lexicographic order.
     * Time: O(n^2).
     * Space: O(n) for the sorted copy.
     * Invariant: all distinct triplets whose first value is below nums[i] are recorded.
     */
    static List<List<Integer>> threeSum(int[] input) {
        // The copy keeps the caller's array unchanged.
        int[] nums = input.clone();
        Arrays.sort(nums);
        List<List<Integer>> out = new ArrayList<>();
        for (int i = 0; i < nums.length - 2; i++) {
            // A fixed value that repeats the previous one only repeats finished work.
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            // Once the smallest value is positive, no triplet can sum to zero.
            if (nums[i] > 0) break;
            int left = i + 1, right = nums.length - 1;
            // The pair scan solves the remaining two-sum on the suffix.
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum < 0) left++;
                else if (sum > 0) right--;
                else {
                    // Record the representative before skipping.
                    int a = nums[left], b = nums[right];
                    out.add(List.of(nums[i], a, b));
                    while (left < right && nums[left] == a) left++;
                    while (left < right && nums[right] == b) right--;
                }
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] in = {2, -2, 0, 1, 0, 2, -1, 1};
        int[] copy = in.clone();
        if (!threeSum(in).equals(List.of(List.of(-2, 0, 2), List.of(-2, 1, 1), List.of(-1, 0, 1)))) throw new AssertionError("example 1");
        if (!Arrays.equals(in, copy)) throw new AssertionError("input mutated");
        if (!threeSum(new int[] {3, 3, 3}).isEmpty()) throw new AssertionError("example 2");
        // Random arrays against a brute force over index triples.
        Random rnd = new Random(52);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(10), -4, 5).toArray();
            TreeSet<String> expect = new TreeSet<>();
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) {
                if (a[i] + a[j] + a[k] == 0) {
                    int[] s = {a[i], a[j], a[k]};
                    Arrays.sort(s);
                    expect.add(s[0] + "," + s[1] + "," + s[2]);
                }
            }
            List<String> got = new ArrayList<>();
            for (List<Integer> p : threeSum(a)) got.add(p.get(0) + "," + p.get(1) + "," + p.get(2));
            if (got.size() != expect.size() || !new TreeSet<>(got).equals(expect)) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] All Equal (Author exercise)
<!-- id: tp-all-equal -->

**Approach.**
The method counts instead of listing, and it uses the same skip rules. With `[0, 0, 0, 0]` the fixed value at index 0 is the representative of the run. The pair scan on indexes 1 to 3 finds `0 + 0`, so the triplet is counted once. Both pointers then skip the run and the scan ends. The next fixed index holds the same value as the previous fixed index, so it is skipped. The fixed-value skip compares with the previous slot and never with the next slot, so the first copy is still evaluated. The invariant is that each distinct triplet is counted exactly once.

**Complexity.**
- **Time** is O(n^2), because the sort costs O(n log n) and the scans cost O(n) per distinct fixed value.
- **Space** is O(n) for the sorted copy.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class AllEqual {
    /**
     * Counts the distinct value triplets that sum to zero.
     * Time: O(n^2).
     * Space: O(n) for the sorted copy.
     * Invariant: every distinct triplet with a smaller first value has been counted once.
     */
    static int countTriplets(int[] input) {
        int[] nums = input.clone();
        Arrays.sort(nums);
        int count = 0;
        for (int i = 0; i < nums.length - 2; i++) {
            // The comparison looks backward, so the first copy of a value is still evaluated.
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum < 0) left++;
                else if (sum > 0) right--;
                else {
                    // One distinct triplet found; skip the runs of both recorded values.
                    count++;
                    int a = nums[left], b = nums[right];
                    while (left < right && nums[left] == a) left++;
                    while (left < right && nums[right] == b) right--;
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (countTriplets(new int[] {0, 0, 0, 0}) != 1) throw new AssertionError("example 1");
        if (countTriplets(new int[] {0, 0}) != 0) throw new AssertionError("example 2");
        // Many zeros still give one triplet, and the empty array gives none.
        if (countTriplets(new int[50]) != 1) throw new AssertionError("fifty zeros");
        if (countTriplets(new int[0]) != 0) throw new AssertionError("empty");
        // Random arrays against a set of sorted index triples.
        Random rnd = new Random(53);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(10), -3, 4).toArray();
            Set<String> expect = new HashSet<>();
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) {
                if (a[i] + a[j] + a[k] == 0) {
                    int[] s = {a[i], a[j], a[k]};
                    Arrays.sort(s);
                    expect.add(Arrays.toString(s));
                }
            }
            if (countTriplets(a) != expect.size()) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-unique -->

**Approach.**
The method sorts a copy and fixes two values with two nested loops. Each loop skips a value that equals the previous value at its own depth, because that run was fully processed. The inner pair scan uses the target `target - nums[i] - nums[j]` and the same skip-after-recording rule as before. Every sum is computed in `long`, because four values near 10^9 add to 4 * 10^9. The invariant is that every distinct quadruple whose first two values come before the current fixed pair in sorted order is already recorded.

**Complexity.**
- **Time** is O(n^3), because two fixed loops each take O(n) and the pair scan takes O(n).
- **Space** is O(n) for the sorted copy, and O(1) beyond it and the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class FourSumUnique18 {
    /**
     * Returns the distinct quadruples that sum to target, in lexicographic order.
     * Time: O(n^3).
     * Space: O(n) for the sorted copy.
     * Invariant: every distinct quadruple with an earlier fixed pair is recorded.
     */
    static List<List<Integer>> fourSum(int[] input, long target) {
        int[] nums = input.clone();
        Arrays.sort(nums);
        int n = nums.length;
        List<List<Integer>> out = new ArrayList<>();
        for (int i = 0; i < n - 3; i++) {
            // The first fixed value skips its own repeats.
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            for (int j = i + 1; j < n - 2; j++) {
                // The second fixed value skips repeats inside the same first value.
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;
                int left = j + 1, right = n - 1;
                while (left < right) {
                    // The long cast keeps four values near 10^9 exact.
                    long sum = (long) nums[i] + nums[j] + nums[left] + nums[right];
                    if (sum < target) left++;
                    else if (sum > target) right--;
                    else {
                        int a = nums[left], b = nums[right];
                        out.add(List.of(nums[i], nums[j], a, b));
                        while (left < right && nums[left] == a) left++;
                        while (left < right && nums[right] == b) right--;
                    }
                }
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!fourSum(new int[] {2, 2, 2, 3, 5, 5, 1, 0}, 10).equals(List.of(List.of(0, 2, 3, 5), List.of(1, 2, 2, 5)))) throw new AssertionError("example 1");
        int[] big = {1_000_000_000, 1_000_000_000, 1_000_000_000, 1_000_000_000};
        if (!fourSum(big, 4_000_000_000L).equals(List.of(List.of(1_000_000_000, 1_000_000_000, 1_000_000_000, 1_000_000_000)))) throw new AssertionError("example 2");
        // An int sum wraps for the same values, which is why the sum is a long.
        int wrapped = big[0] + big[1] + big[2] + big[3];
        if (wrapped == 4_000_000_000L) throw new AssertionError("int sum should wrap");
        // Random arrays against a brute force over index quadruples.
        Random rnd = new Random(54);
        for (int t = 0; t < 2000; t++) {
            int[] a = rnd.ints(rnd.nextInt(9), -3, 4).toArray();
            long target = rnd.nextInt(7) - 3;
            TreeSet<String> expect = new TreeSet<>();
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) for (int l = k + 1; l < a.length; l++) {
                if ((long) a[i] + a[j] + a[k] + a[l] == target) {
                    int[] s = {a[i], a[j], a[k], a[l]};
                    Arrays.sort(s);
                    expect.add(Arrays.toString(s));
                }
            }
            TreeSet<String> gotSet = new TreeSet<>();
            for (List<Integer> q : fourSum(a, target)) gotSet.add(Arrays.toString(q.stream().mapToInt(Integer::intValue).toArray()));
            if (fourSum(a, target).size() != expect.size() || !gotSet.equals(expect)) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```
