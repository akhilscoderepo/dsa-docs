<!-- solutions-for: 09-fixed-size-aggregate-windows -->
### Fixed-Size Aggregate Windows

#### Solution: [Build] Sums of Every K-Block (Author exercise)
<!-- id: sw-block-sums -->

**Approach.** Keep one `long` total. At each position add the entering value, and once the frame has grown beyond k, subtract the value that sits k places behind. From the k-th position onward store the total. Verification uses a from-scratch sum as the oracle on random arrays including extremes, asserts that the input array is unchanged, counts element reads to show that no element is read more than twice, and uses values near the int maximum to show that an int total would have wrapped.

**Complexity.** One pass of n steps with two reads each, so time grows linearly in n; extra space is the output array only.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BlockSums {
    static int reads;

    static long[] blockSums(int[] nums, int k) {
        long[] out = new long[nums.length - k + 1];
        long total = 0;
        for (int right = 0; right < nums.length; right++) {
            total += nums[right];
            reads++;
            if (right >= k) {
                total -= nums[right - k];
                reads++;
            }
            if (right + 1 >= k) out[right + 1 - k] = total;
        }
        return out;
    }

    static long[] oracle(int[] nums, int k) {
        long[] out = new long[nums.length - k + 1];
        for (int s = 0; s < out.length; s++) {
            long sum = 0;
            for (int i = s; i < s + k; i++) sum += nums[i];
            out[s] = sum;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(blockSums(new int[] {3, -1, 4, 1, -5, 9}, 3), new long[] {6, 4, 0, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(blockSums(new int[] {7, 7}, 1), new long[] {7, 7})) throw new AssertionError("example 2");
        int[] big = {Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE, 5};
        long[] got = blockSums(big, 2);
        if (got[0] != 2L * Integer.MAX_VALUE) throw new AssertionError("long total");
        if (Integer.MAX_VALUE + Integer.MAX_VALUE >= 0) throw new AssertionError("an int total would have wrapped");
        Random rnd = new Random(901);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(5);
                a[i] = pick == 0 ? Integer.MAX_VALUE : pick == 1 ? Integer.MIN_VALUE : rnd.nextInt(21) - 10;
            }
            if (t % 7 == 0) Arrays.fill(a, a[0]);
            int[] copy = a.clone();
            int k = 1 + rnd.nextInt(n);
            reads = 0;
            long[] r = blockSums(a, k);
            if (!Arrays.equals(r, oracle(a, k))) throw new AssertionError("differs on " + Arrays.toString(a) + " k " + k);
            if (!Arrays.equals(a, copy)) throw new AssertionError("input was mutated");
            if (reads > 2 * n) throw new AssertionError("too many reads " + reads);
        }
    }
}
```

#### Solution: [Vary] Maximum Average Subarray I (LeetCode 643)
<!-- id: sw-max-average -->

**Approach.** Add the first k values into a `long`, make that the best total, then move the frame while adding and subtracting in separate statements so no step happens in `int` arithmetic. The best total is divided by k once at the end, which is valid because every block has the same length. Seeding the best from the first block, rather than from zero, keeps all-negative inputs correct. Verification recomputes every block average naively, confirms the all-negative example, and shows that `int` subtraction of two extreme values wraps.

**Complexity.** Linear time in the array length and constant extra space.

```java run
import java.util.Random;

public final class MaxAverage {
    static double highestAverage(int[] nums, int k) {
        long total = 0;
        for (int i = 0; i < k; i++) total += nums[i];
        long best = total;
        for (int right = k; right < nums.length; right++) {
            total += nums[right];
            total -= nums[right - k];
            if (total > best) best = total;
        }
        return (double) best / k;
    }

    static double brute(int[] nums, int k) {
        double top = -Double.MAX_VALUE;
        for (int s = 0; s + k <= nums.length; s++) {
            long sum = 0;
            for (int i = s; i < s + k; i++) sum += nums[i];
            top = Math.max(top, (double) sum / k);
        }
        return top;
    }

    public static void main(String[] args) {
        if (highestAverage(new int[] {4, -2, 7, 1, -5, 6}, 3) != 3.0) throw new AssertionError("example 1");
        if (highestAverage(new int[] {-8, -3, -6}, 2) != -4.5) throw new AssertionError("example 2");
        int wrapped = Integer.MAX_VALUE - (-1);
        if (wrapped >= 0) throw new AssertionError("int difference should wrap");
        int[] extremes = {Integer.MAX_VALUE, -1, Integer.MAX_VALUE, -1};
        if (highestAverage(extremes, 2) != brute(extremes, 2)) throw new AssertionError("extremes");
        if (highestAverage(new int[] {-5}, 1) != -5.0) throw new AssertionError("single negative");
        Random rnd = new Random(902);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(6);
                a[i] = pick == 0 ? Integer.MAX_VALUE : pick == 1 ? Integer.MIN_VALUE : rnd.nextInt(41) - 30;
            }
            if (t % 9 == 0) java.util.Arrays.fill(a, a[0]);
            int k = 1 + rnd.nextInt(n);
            if (highestAverage(a, k) != brute(a, k)) throw new AssertionError("differs on " + java.util.Arrays.toString(a) + " k " + k);
        }
    }
}
```

#### Solution: [Boundary] Whole-Array Window (Author exercise)
<!-- id: sw-whole-array -->

**Approach.** Validate k first: anything below 1 or above the array length throws `IllegalArgumentException`, which also covers an empty array, since no k from 1 upward fits. After validation the first block always exists. Compute its sum, then slide and move the best start only on a strictly larger total, which keeps the smallest start on ties. When k equals the length the slide loop body never runs, and the answer is 0. Verification runs a naive scan on random arrays, and asserts the exceptions for k = 0, a negative k, k above the length and an empty array.

**Complexity.** Linear time, constant extra space; the validation is a constant-time comparison.

```java run
import java.util.Random;

public final class WholeArray {
    static int bestStart(int[] nums, int k) {
        if (k < 1 || k > nums.length) throw new IllegalArgumentException("k out of range: " + k);
        long total = 0;
        for (int i = 0; i < k; i++) total += nums[i];
        long top = total;
        int start = 0;
        for (int left = 1; left + k <= nums.length; left++) {
            total += nums[left + k - 1];
            total -= nums[left - 1];
            if (total > top) {
                top = total;
                start = left;
            }
        }
        return start;
    }

    static int brute(int[] nums, int k) {
        int start = 0;
        long top = Long.MIN_VALUE;
        for (int s = 0; s + k <= nums.length; s++) {
            long sum = 0;
            for (int i = s; i < s + k; i++) sum += nums[i];
            if (sum > top) {
                top = sum;
                start = s;
            }
        }
        return start;
    }

    static boolean throwsFor(int[] nums, int k) {
        try {
            bestStart(nums, k);
            return false;
        } catch (IllegalArgumentException e) {
            return true;
        }
    }

    public static void main(String[] args) {
        if (bestStart(new int[] {3, 1, 2}, 3) != 0) throw new AssertionError("example 1");
        if (bestStart(new int[] {1, 5, 2, 5}, 2) != 1) throw new AssertionError("example 2");
        if (!throwsFor(new int[] {1, 2, 3}, 0)) throw new AssertionError("k = 0");
        if (!throwsFor(new int[] {1, 2, 3}, -4)) throw new AssertionError("negative k");
        if (!throwsFor(new int[] {1, 2, 3}, 4)) throw new AssertionError("k above length");
        if (!throwsFor(new int[0], 1)) throw new AssertionError("empty array");
        if (bestStart(new int[] {9}, 1) != 0) throw new AssertionError("single element");
        if (bestStart(new int[] {4, 4, 4, 4}, 2) != 0) throw new AssertionError("all equal keeps the smallest start");
        Random rnd = new Random(903);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            for (int k = 1; k <= n; k++) {
                if (bestStart(a, k) != brute(a, k)) throw new AssertionError("differs on " + java.util.Arrays.toString(a) + " k " + k);
            }
        }
    }
}
```

#### Solution: [Recognize] Maximum Number of Vowels in a Substring of Given Length (LeetCode 1456)
<!-- id: sw-max-vowels -->

**Approach.** The aggregate is the number of vowels among the letters currently inside the frame. Entering a vowel adds one and leaving a vowel removes one, and consonants change nothing. Track the best count once the frame has k letters. The count never exceeds k, so an `int` is plenty, which the check confirms by comparing the best count with k on a string of only vowels. The oracle is a naive substring count over random strings over a small alphabet, including a string that is all vowels and one that has none.

**Complexity.** One pass with at most two character reads per position: linear time, constant space.

```java run
import java.util.Random;

public final class MaxVowels {
    static int reads;

    static boolean vowel(char c) {
        reads++;
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    }

    static int maxVowels(String s, int k) {
        int inside = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            if (vowel(s.charAt(right))) inside++;
            if (right >= k && vowel(s.charAt(right - k))) inside--;
            if (right + 1 >= k && inside > best) best = inside;
        }
        return best;
    }

    static int brute(String s, int k) {
        int best = 0;
        for (int st = 0; st + k <= s.length(); st++) {
            int c = 0;
            for (char ch : s.substring(st, st + k).toCharArray()) if ("aeiou".indexOf(ch) >= 0) c++;
            best = Math.max(best, c);
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxVowels("sequoia", 4) != 4) throw new AssertionError("example 1");
        if (maxVowels("rhythm", 2) != 0) throw new AssertionError("example 2");
        if (maxVowels("aeiouaeiou", 7) != 7) throw new AssertionError("all vowels equals k");
        if (maxVowels("bcdfg", 3) != 0) throw new AssertionError("no vowels");
        if (maxVowels("e", 1) != 1) throw new AssertionError("single letter");
        Random rnd = new Random(904);
        String alphabet = "abcdeiz";
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            int k = 1 + rnd.nextInt(n);
            reads = 0;
            int got = maxVowels(s, k);
            if (got != brute(s, k)) throw new AssertionError("differs on " + s + " k " + k);
            if (reads > 2 * n) throw new AssertionError("too many character reads");
        }
    }
}
```
