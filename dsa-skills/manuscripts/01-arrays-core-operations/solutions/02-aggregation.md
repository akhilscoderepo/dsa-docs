<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Aggregation

#### Solution: [Build] Maximum (Author exercise)
<!-- id: ar-maximum -->

**Approach.** The accumulator `max` holds the largest value in the part of the array already read. It starts as `nums[0]`, so the promise is true for the one-element prefix, and the loop starts at index 1. Each later element replaces `max` only when it is strictly larger. When the loop ends, the prefix is the whole array, so `max` is the answer.

A start value of 0 would fail for an all-negative array, and the harness asserts that failure for `[-9, -4, -7]`. The comparison against the quadratic method from the lesson and against `Arrays.stream` covers random arrays.

**Complexity.**

- **Time** is O(n), as the loop does one comparison for each of the `n - 1` later elements.
- **Space** is O(1), since `max` and the index are the whole state.

```java run
import java.util.Arrays;
import java.util.Random;

public final class Maximum {
    /**
     * Returns the largest value of a non-empty array.
     * Time: O(n), because each element is compared once.
     * Space: O(1), because only max and the index are stored.
     * Invariant: before reading nums[i], max is the largest value in nums[0..i-1].
     */
    static int maximum(int[] nums) {
        // Start from the data so the invariant holds for the one-element prefix.
        int max = nums[0];
        // Begin at index 1 because index 0 is already summarized; the loop gives O(n) time.
        for (int i = 1; i < nums.length; i++) {
            // Replace the accumulator only when the new element is larger, which keeps the invariant.
            if (nums[i] > max) max = nums[i];
        }
        // The prefix is now the whole array, so max is the answer.
        return max;
    }

    /** The quadratic method from the lesson: a value is the maximum when nothing exceeds it. */
    static int maximumByComparison(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            boolean largest = true;
            for (int j = 0; j < nums.length; j++) if (nums[j] > nums[i]) largest = false;
            if (largest) return nums[i];
        }
        throw new IllegalArgumentException("empty array");
    }

    /** The wrong start from the lesson: an accumulator that begins at zero. */
    static int maximumFromZero(int[] nums) {
        int max = 0;
        for (int v : nums) if (v > max) max = v;
        return max;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (maximum(new int[] {-9, -4, -7}) != -4) throw new AssertionError("example 1");
        if (maximum(new int[] {-5}) != -5) throw new AssertionError("example 2");
        // Checks the extreme value Integer.MIN_VALUE as the only element.
        if (maximum(new int[] {Integer.MIN_VALUE}) != Integer.MIN_VALUE) throw new AssertionError("minimum int");
        // Checks the lesson claim: starting at zero returns 0 for an all-negative array.
        if (maximumFromZero(new int[] {-9, -4, -7}) != 0) throw new AssertionError("zero start gives 0");
        // Checks 2,000 random arrays against the quadratic method and the stream library.
        Random rnd = new Random(5);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[1 + rnd.nextInt(8)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(21) - 15;
            int expected = Arrays.stream(x).max().getAsInt();
            if (maximum(x) != expected) throw new AssertionError("mismatch on " + Arrays.toString(x));
            if (maximumByComparison(x) != expected) throw new AssertionError("oracle mismatch on " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Vary] Find Numbers with Even Number of Digits (LeetCode 1295)
<!-- id: ar-even-digit-count -->

**Approach.** The accumulator `count` holds how many elements of the prefix have an even digit count. It starts at 0, because an empty prefix has no matches. For each element, a helper divides the value by 10 until it reaches 0 and counts the divisions, which gives the number of digits. When that number is even, `count` grows by one. The state changed from a value taken from the data to a counter that starts at a constant, and the loop structure stayed the same.

The harness checks the helper against the length of the decimal string for every value from 1 to 100,000, and it checks the count against a string-based oracle on random arrays.

**Complexity.**

- **Time** is O(n), since each element costs at most six divisions, and six is a constant for values up to 10^5.
- **Space** is O(1), as the method keeps `count` and the helper's working value.

```java run
import java.util.Random;

public final class EvenDigitCount {
    /**
     * Returns the number of decimal digits of a positive value.
     * Time: O(1) for bounded values, because at most six divisions happen below 10^6.
     * Space: O(1), because one working copy is stored.
     */
    static int digits(int value) {
        // Count the digits by removing the last one until nothing is left.
        int d = 0;
        // Each division by 10 removes one digit, so the loop runs once per digit.
        while (value > 0) { d++; value /= 10; }
        // Return how many divisions were needed.
        return d;
    }

    /**
     * Counts elements that have an even number of digits.
     * Time: O(n), because each element needs a bounded number of divisions.
     * Space: O(1), because only count is kept.
     * Invariant: before reading nums[i], count is the number of even-digit values in nums[0..i-1].
     */
    static int countEvenDigits(int[] nums) {
        // An empty prefix has no matches, so the count starts at zero.
        int count = 0;
        // One pass gives O(n) calls to the helper.
        for (int v : nums) {
            // An even digit count adds one to the accumulator.
            if (digits(v) % 2 == 0) count++;
        }
        // The prefix is the whole array.
        return count;
    }

    public static void main(String[] args) {
        // Checks both examples, including the empty array.
        if (countEvenDigits(new int[] {10, 100, 1000, 99999, 100000}) != 3) throw new AssertionError("example 1");
        if (countEvenDigits(new int[] {}) != 0) throw new AssertionError("example 2");
        // Checks the helper against the decimal string length for every allowed value.
        for (int v = 1; v <= 100000; v++) {
            if (digits(v) != String.valueOf(v).length()) throw new AssertionError("digits of " + v);
        }
        // Checks 2,000 random arrays against a string-based oracle.
        Random rnd = new Random(17);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(9)];
            int expected = 0;
            for (int i = 0; i < x.length; i++) {
                x[i] = 1 + rnd.nextInt(100000);
                if (String.valueOf(x[i]).length() % 2 == 0) expected++;
            }
            if (countEvenDigits(x) != expected) throw new AssertionError("count mismatch");
        }
    }
}
```

#### Solution: [Boundary] Max Consecutive Ones (LeetCode 485)
<!-- id: ar-max-consecutive-ones -->

**Approach.** The method keeps two accumulators. The value `current` is the length of the block that ends at the position just read, and `best` is the longest block seen so far. A 1 extends `current` by one. A 0 resets `current` to 0 and leaves `best` untouched. The update `best = max(best, current)` runs after every element, so a block that reaches the end of the array is counted without needing a trailing 0.

The edge cases are the empty array, an all-zero array and a block at the end. The harness checks each one and compares the method with an oracle that splits the bits as a string at every 0.

**Complexity.**

- **Time** is O(n), as every element costs one comparison and one update.
- **Space** is O(1), since `current` and `best` are the only extra variables.

```java run
import java.util.Random;

public final class MaxConsecutiveOnes {
    /**
     * Returns the length of the longest block of consecutive ones.
     * Time: O(n), because each element is read once.
     * Space: O(1), because only current and best are stored.
     * Invariant: before reading bits[i], current is the length of the block ending at i-1 and best is the longest block in bits[0..i-1].
     */
    static int longestRun(int[] bits) {
        // Both accumulators describe the empty prefix, where no block exists.
        int current = 0, best = 0;
        // One pass over all elements gives O(n) time.
        for (int b : bits) {
            // A one extends the block that ends at the previous position.
            if (b == 1) current++;
            // A zero breaks the block, so the current length restarts; best keeps its value.
            else current = 0;
            // Update after every element so a block that touches the end is counted.
            best = Math.max(best, current);
        }
        // Every element was read, so best covers the whole array.
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples; the second one ends inside a block.
        if (longestRun(new int[] {1, 0, 1, 1, 1, 0, 1}) != 3) throw new AssertionError("example 1");
        if (longestRun(new int[] {0, 1, 1}) != 2) throw new AssertionError("example 2");
        // Checks the empty array and an all-zero array.
        if (longestRun(new int[] {}) != 0) throw new AssertionError("empty");
        if (longestRun(new int[] {0, 0}) != 0) throw new AssertionError("all zeros");
        // Checks an all-ones array, where no zero ever arrives.
        if (longestRun(new int[] {1, 1, 1, 1}) != 4) throw new AssertionError("all ones");
        // Checks 2,000 random binary arrays against an oracle that splits the text at each zero.
        Random rnd = new Random(29);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < x.length; i++) { x[i] = rnd.nextInt(2); sb.append(x[i]); }
            int expected = 0;
            for (String block : sb.toString().split("0")) expected = Math.max(expected, block.length());
            if (longestRun(x) != expected) throw new AssertionError("mismatch on " + sb);
        }
    }
}
```

#### Solution: [Recognize] Average Salary Excluding the Minimum and Maximum Salary (LeetCode 1491)
<!-- id: ar-trimmed-average -->

**Approach.** The final formula is the total minus the smallest value minus the largest value, divided by `n - 2`. Three scalars supply it: `sum`, `min` and `max`. One pass updates all three, because each needs only the current element. The sum is a `long`, so large totals cannot wrap, and the division converts to `double` before dividing, so the fraction survives. Sorting is not needed, since the formula never uses the order of the values.

The harness shows both Java hazards from the lesson: an `int` sum wraps at `Integer.MAX_VALUE`, and integer division drops the fraction. It then compares the method with a sort-based oracle on random arrays of distinct values.

**Complexity.**

- **Time** is O(n), because one pass updates the three scalars for each element.
- **Space** is O(1), because `sum`, `min`, `max` and the index are the whole state. A sort-based method would take O(n log n) time instead.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class TrimmedAverage {
    /**
     * Returns the average after removing one minimum and one maximum value.
     * Time: O(n), because one pass updates three scalars.
     * Space: O(1), because only sum, min, max and the index are stored.
     * Invariant: before reading salary[i], sum, min and max describe salary[0..i-1].
     */
    static double trimmedAverage(int[] salary) {
        // Start min and max from the first element and sum from zero; sum is a long to avoid wrap-around.
        long sum = 0;
        int min = salary[0], max = salary[0];
        // One pass over all elements gives O(n) time.
        for (int v : salary) {
            // Add the element to the total of the prefix.
            sum += v;
            // Keep the smallest value seen so far.
            if (v < min) min = v;
            // Keep the largest value seen so far.
            if (v > max) max = v;
        }
        // Remove one minimum and one maximum, then divide as double so the fraction is kept.
        return (double) (sum - min - max) / (salary.length - 2);
    }

    public static void main(String[] args) {
        // Checks both examples within the allowed error of 1e-5.
        if (Math.abs(trimmedAverage(new int[] {5000, 1500, 3500, 2500, 9000}) - 11000.0 / 3) > 1e-9) throw new AssertionError("example 1");
        if (trimmedAverage(new int[] {7000, 4000, 1000}) != 4000.0) throw new AssertionError("example 2");
        // Checks the lesson claim: int addition wraps around at Integer.MAX_VALUE.
        int wrapped = Integer.MAX_VALUE + 1;
        if (wrapped != Integer.MIN_VALUE) throw new AssertionError("int sum wraps");
        // Checks the lesson claim: integer division drops the fraction, while a double division keeps it.
        if (11000 / 3 != 3666) throw new AssertionError("integer division truncates");
        if (!((double) 11000 / 3 > 3666.6)) throw new AssertionError("double division keeps the fraction");
        // Checks 2,000 random arrays of distinct values against a sort-based oracle.
        Random rnd = new Random(37);
        for (int t = 0; t < 2000; t++) {
            int n = 3 + rnd.nextInt(6);
            List<Integer> pool = new ArrayList<>();
            for (int v = 0; v < 40; v++) pool.add(1000 + 23 * v);
            Collections.shuffle(pool, rnd);
            int[] x = new int[n];
            for (int i = 0; i < n; i++) x[i] = pool.get(i);
            int[] sorted = x.clone();
            Arrays.sort(sorted);
            double total = 0;
            for (int i = 1; i < n - 1; i++) total += sorted[i];
            if (Math.abs(trimmedAverage(x) - total / (n - 2)) > 1e-6) throw new AssertionError("mismatch on " + Arrays.toString(x));
        }
    }
}
```
