<!-- solutions-for: 02-aggregation -->
### Aggregation

#### Solution: [Build] Maximum (Author exercise)
<!-- id: ar-maximum -->

**Approach.** Seed the accumulator with `nums[0]`, which the contract guarantees exists, then absorb each remaining element with `Math.max`. After processing index `i` the accumulator is the maximum of `nums[0..i]`. Starting from zero would return 0 for an all-negative array, and the assertions include exactly that case. The rescanning version from the lesson serves as an oracle for a randomized comparison.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class Maximum {
    static int maximum(int[] nums) {
        int best = nums[0];
        for (int i = 1; i < nums.length; i++) best = Math.max(best, nums[i]);
        return best;
    }
    static int maxFromZero(int[] nums) {
        int best = 0;
        for (int v : nums) best = Math.max(best, v);
        return best;
    }
    static int oracle(int[] nums) {
        int best = Integer.MIN_VALUE;
        for (int i = 0; i < nums.length; i++) for (int j = 0; j <= i; j++) best = Math.max(best, nums[j]);
        return best;
    }

    public static void main(String[] args) {
        if (maximum(new int[] {-3, 8, 1}) != 8) throw new AssertionError("example 1");
        if (maximum(new int[] {-5}) != -5) throw new AssertionError("example 2");
        if (maxFromZero(new int[] {-5}) != 0) throw new AssertionError("a zero seed is wrong for negatives");
        Random rnd = new Random(3);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(41) - 20;
            if (maximum(a) != oracle(a)) throw new AssertionError("disagrees with the oracle");
        }
    }
}
```

#### Solution: [Vary] Find Numbers with Even Number of Digits (LeetCode 1295)
<!-- id: ar-even-digit-count -->

**Approach.** Keep a count that starts at zero. For each value, count its digits by dividing by ten until it reaches zero, and increment the count when that number is even. The loop over digits runs at most six times for values up to 10^5, so it is a constant amount of work per element. Converting to a string gives the same answer and allocates an object per element, which the digit loop avoids, and the assertions check that both agree.

**Complexity.** O(n) time, since the digit loop is bounded by a constant, and O(1) extra space.

```java run
public final class EvenDigitCount {
    static int digits(int v) { int d = 0; while (v > 0) { d++; v /= 10; } return d; }
    static int countEven(int[] nums) {
        int count = 0;
        for (int v : nums) if (digits(v) % 2 == 0) count++;
        return count;
    }
    static int countEvenViaString(int[] nums) {
        int count = 0;
        for (int v : nums) if (String.valueOf(v).length() % 2 == 0) count++;
        return count;
    }

    public static void main(String[] args) {
        if (countEven(new int[] {100, 7, 22, 3000, 55555}) != 2) throw new AssertionError("example 1");
        if (countEven(new int[] {}) != 0) throw new AssertionError("example 2");
        if (digits(100000) != 6 || digits(9) != 1 || digits(10) != 2) throw new AssertionError("digit counts");
        for (int v = 1; v <= 100_000; v++) {
            if (countEven(new int[] {v}) != countEvenViaString(new int[] {v})) throw new AssertionError("digit loop disagrees at " + v);
        }
    }
}
```

#### Solution: [Boundary] Max Consecutive Ones (LeetCode 485)
<!-- id: ar-max-consecutive-ones -->

**Approach.** Keep `current`, the length of the run of ones ending at the element just read, and `best`, the longest run seen. On a one, extend `current`. On a zero, set `current` to zero. Update `best` after every element, not only at a zero, because the array may end in the middle of a run and the last run would otherwise never be recorded. This is the same bug the hostile-dry-runs lesson showed, and `[1, 1]` is the test that exposes it.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class MaxConsecutiveOnes {
    static int longestRun(int[] nums) {
        int best = 0, current = 0;
        for (int v : nums) {
            current = v == 1 ? current + 1 : 0;
            best = Math.max(best, current);
        }
        return best;
    }
    static int updateOnlyAtZero(int[] nums) {
        int best = 0, current = 0;
        for (int v : nums) {
            if (v == 1) current++; else { best = Math.max(best, current); current = 0; }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestRun(new int[] {1, 0, 1, 1, 0, 1}) != 2) throw new AssertionError("example 1");
        if (longestRun(new int[] {0, 0}) != 0) throw new AssertionError("example 2");
        if (longestRun(new int[] {1, 1}) != 2) throw new AssertionError("array ends inside a run");
        if (updateOnlyAtZero(new int[] {1, 1}) != 0) throw new AssertionError("updating only at a zero misses the last run");
        for (int mask = 0; mask < 1 << 10; mask++) {
            int[] a = new int[10];
            for (int i = 0; i < 10; i++) a[i] = mask >> i & 1;
            int expected = 0;
            for (int s = 0; s < 10; s++) { int e = s; while (e < 10 && a[e] == 1) e++; expected = Math.max(expected, e - s); }
            if (longestRun(a) != expected) throw new AssertionError("mask " + mask);
        }
    }
}
```

#### Solution: [Recognize] Average Salary Excluding the Minimum and Maximum Salary (LeetCode 1491)
<!-- id: ar-average-salary -->

**Approach.** One pass keeps `sum`, `min` and `max`, seeded from the first element for the two extremes. After the loop the answer is `(sum - min - max) / (n - 2)`, computed in floating point so the division does not truncate. Using `long` for the sum is not needed at these limits, since 100 salaries of 10^6 total 10^8, which fits in an `int`, but it costs nothing and removes the question. The check compares against sorting the array and averaging the middle.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class AverageSalary {
    static double average(int[] salary) {
        long sum = salary[0];
        int min = salary[0], max = salary[0];
        for (int i = 1; i < salary.length; i++) {
            sum += salary[i];
            min = Math.min(min, salary[i]);
            max = Math.max(max, salary[i]);
        }
        return (double) (sum - min - max) / (salary.length - 2);
    }
    static double oracle(int[] salary) {
        int[] s = salary.clone();
        Arrays.sort(s);
        double total = 0;
        for (int i = 1; i < s.length - 1; i++) total += s[i];
        return total / (s.length - 2);
    }

    public static void main(String[] args) {
        if (Math.abs(average(new int[] {1900, 2500, 2200, 1700}) - 2050.0) > 1e-9) throw new AssertionError("example 1");
        if (Math.abs(average(new int[] {1000, 2000, 3000}) - 2000.0) > 1e-9) throw new AssertionError("example 2");
        if (Math.abs(average(new int[] {1000, 2000, 2500, 4000}) - 2250.0) > 1e-9) throw new AssertionError("even number of values left");
        Random rnd = new Random(5);
        for (int t = 0; t < 2000; t++) {
            int n = 3 + rnd.nextInt(8);
            java.util.Set<Integer> seen = new java.util.HashSet<>();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) { int v; do { v = 1000 + rnd.nextInt(5000); } while (!seen.add(v)); a[i] = v; }
            if (Math.abs(average(a) - oracle(a)) > 1e-9) throw new AssertionError("disagrees with the sorting oracle");
        }
        if ((5 - 0) / 2 != 2 || (double) (5 - 0) / 2 != 2.5) throw new AssertionError("integer division truncates");
    }
}
```
