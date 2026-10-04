<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Sorted Deduplication

#### Solution: [Build] Remove Duplicates From Sorted Array (LeetCode 26)
<!-- id: ar-remove-sorted-duplicates -->

**Approach.** The first element of a non-empty array is the representative of the first value run, so the write index starts at 1. The read index then scans from position 1. A value that differs from `nums[write - 1]` begins a new run, so the method copies it to the write index and advances the write index. A value that equals `nums[write - 1]` belongs to a run that already has a representative, so the method skips it.

The invariant is that `nums[0..write-1]` holds one representative of every run started so far, in ascending order. An empty array returns 0 before any index is read. The harness checks the method against a `TreeSet` oracle and also asserts the unsorted false friend.

**Complexity.**

- **Time** is O(n), because the scan makes one comparison and at most one write per position.
- **Space** is O(1), because the method adds two integer variables and no array.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class RemoveSortedDuplicates {
    /**
     * Keeps one representative per run of equal values in a sorted array and returns the count.
     * Time: O(n), because each position is read once.
     * Space: O(1), because only two indexes are stored.
     * Invariant: nums[0..write-1] holds one representative of each run started so far, in ascending order.
     */
    static int removeDuplicates(int[] nums) {
        // An empty array has no first element, so there is nothing to read; return 0 now.
        if (nums.length == 0) return 0;
        // The first element is always a representative, so the prefix already holds one value.
        int write = 1;
        // The read index scans the rest of the array once, which gives the O(n) time.
        for (int read = 1; read < nums.length; read++) {
            // A value different from the last written value starts a new run.
            if (nums[read] != nums[write - 1]) {
                // Copy the new representative to the next free position; write <= read keeps unread values safe.
                nums[write] = nums[read];
                // Extend the prefix by one position.
                write++;
            }
        }
        // The write index equals the number of runs, which is the contract's return value.
        return write;
    }

    public static void main(String[] args) {
        // Checks Example 1: three distinct values remain in ascending order.
        int[] a = {3, 3, 3, 8, 9, 9};
        int k = removeDuplicates(a);
        if (k != 3 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {3, 8, 9})) throw new AssertionError("example 1");
        // Checks Example 2: the empty array and a single element.
        if (removeDuplicates(new int[0]) != 0) throw new AssertionError("empty input");
        int[] one = {-5};
        if (removeDuplicates(one) != 1 || one[0] != -5) throw new AssertionError("single element");
        // Checks the false friend: an unsorted array keeps its repeated value, so the method needs sorted input.
        int[] unsorted = {3, 1, 3};
        if (removeDuplicates(unsorted) != 3) throw new AssertionError("unsorted input keeps the duplicate");
        // Checks the method against a TreeSet oracle on 3,000 random sorted arrays.
        Random rnd = new Random(23);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(6) - 2;
            Arrays.sort(x);
            int[] expected = new TreeSet<>(Arrays.stream(x).boxed().toList()).stream().mapToInt(Integer::intValue).toArray();
            int got = removeDuplicates(x);
            if (!Arrays.equals(Arrays.copyOf(x, got), expected)) throw new AssertionError("mismatch " + Arrays.toString(expected));
        }
    }
}
```

#### Solution: [Vary] Remove Duplicates, Keep Two (LeetCode 80)
<!-- id: ar-keep-two-copies -->

**Approach.** The method generalizes the admission check to a limit of two copies. The first two values are always admitted, because no value can appear three times in a prefix shorter than three. After that, a value is admitted when it differs from `nums[write - 2]`. The array is sorted, so equal values are adjacent, and if the value two positions back in the prefix equals the current value, the prefix already holds two copies of it.

The invariant is that `nums[0..write-1]` holds at most two copies of each value, in ascending order, for every value read so far. The check reads the prefix and not `nums[read - 2]`, because writes may have changed the earlier positions of the array. The harness compares the method with a counting oracle.

**Complexity.**

- **Time** is O(n), because each position costs one comparison and at most one write.
- **Space** is O(1), because only two integer variables are extra.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class KeepTwoCopies {
    /**
     * Keeps at most two copies of each value in a sorted array and returns the prefix length.
     * Time: O(n), because each position is read once.
     * Space: O(1), because only two indexes are stored.
     * Invariant: nums[0..write-1] holds at most two copies of every value read so far, in ascending order.
     */
    static int removeDuplicatesTwo(int[] nums) {
        // The write index is the next free position of the output prefix.
        int write = 0;
        // The read index visits each position once.
        for (int read = 0; read < nums.length; read++) {
            // The first two values are admitted, and later values must differ from the second last written value.
            if (write < 2 || nums[read] != nums[write - 2]) {
                // Copy the admitted value to the free position of the prefix.
                nums[write] = nums[read];
                // Extend the prefix by one position.
                write++;
            }
        }
        // The write index is the length of the result prefix.
        return write;
    }

    /** Reference answer: counts copies per value while building a new list. */
    static List<Integer> oracle(int[] sorted) {
        // The list holds the expected output in order.
        List<Integer> out = new ArrayList<>();
        // Visit every value and admit it only while fewer than two copies of it are in the list.
        for (int v : sorted) {
            int copies = 0;
            for (int w : out) if (w == v) copies++;
            if (copies < 2) out.add(v);
        }
        // Return the expected sequence.
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1: four copies of 4 shrink to two, and three copies of 7 shrink to two.
        int[] a = {4, 4, 4, 4, 6, 7, 7, 7};
        int k = removeDuplicatesTwo(a);
        if (k != 5 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {4, 4, 6, 7, 7})) throw new AssertionError("example 1");
        // Checks Example 2: two copies stay, and a single element stays.
        int[] b = {2, 2};
        if (removeDuplicatesTwo(b) != 2) throw new AssertionError("two copies");
        if (removeDuplicatesTwo(new int[] {9}) != 1) throw new AssertionError("single element");
        if (removeDuplicatesTwo(new int[0]) != 0) throw new AssertionError("empty input");
        // Checks the method against the oracle on 3,000 random sorted arrays.
        Random rnd = new Random(29);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(4);
            Arrays.sort(x);
            List<Integer> expected = oracle(x);
            int got = removeDuplicatesTwo(x);
            if (got != expected.size()) throw new AssertionError("length mismatch");
            for (int i = 0; i < got; i++) if (x[i] != expected.get(i)) throw new AssertionError("prefix mismatch");
        }
    }
}
```

#### Solution: [Boundary] Keep One Per Run (Author exercise)
<!-- id: ar-keep-one-per-run -->

**Approach.** The loop is the one-representative loop with attention on its extremes. When all values are equal, every read after the first is skipped, so the write index stays at 1. When all values are distinct, every read is admitted, so the write index reaches `n` and the array is unchanged. The comparison uses `!=` and never subtracts, because the difference of `Integer.MAX_VALUE` and `Integer.MIN_VALUE` overflows `int` and could give a wrong sign.

The invariant is that `nums[0..write-1]` holds one representative per run started so far. The harness asserts the overflow fact that justifies the comparison, then checks both extremes and random arrays that include the two extreme values.

**Complexity.**

- **Time** is O(n), because the scan does constant work per position.
- **Space** is O(1), because no array is allocated.

```java run
import java.util.Arrays;
import java.util.Random;

public final class KeepOnePerRun {
    /**
     * Keeps one value per run of equal values in a sorted array and returns the number of runs.
     * Time: O(n), because each position is read once.
     * Space: O(1), because only two indexes are stored.
     * Invariant: nums[0..write-1] holds one representative of each run started so far.
     */
    static int keepOnePerRun(int[] nums) {
        // Guard the empty array first, because nums[write - 1] needs a first element.
        if (nums.length == 0) return 0;
        // The first value is the representative of the first run.
        int write = 1;
        // The read index scans the remaining positions once.
        for (int read = 1; read < nums.length; read++) {
            // Compare with !=; a subtraction test could overflow on extreme values.
            if (nums[read] != nums[write - 1]) {
                // A new run starts, so its first value moves to the free position.
                nums[write] = nums[read];
                // Extend the prefix by one position.
                write++;
            }
        }
        // The write index equals the number of runs.
        return write;
    }

    public static void main(String[] args) {
        // Checks the overflow fact: the difference of the two extreme values wraps around to 1, which has the wrong sign.
        if (Integer.MIN_VALUE - Integer.MAX_VALUE != 1) throw new AssertionError("subtraction wraps");
        // Checks Example 1: an all-equal array collapses to one value.
        int[] a = {5, 5, 5};
        if (keepOnePerRun(a) != 1 || a[0] != 5) throw new AssertionError("all equal");
        // Checks Example 2: an already distinct array is unchanged, including the extreme values.
        int[] b = {1, 2, 3};
        if (keepOnePerRun(b) != 3 || !Arrays.equals(b, new int[] {1, 2, 3})) throw new AssertionError("all distinct");
        int[] c = {Integer.MIN_VALUE, Integer.MAX_VALUE};
        if (keepOnePerRun(c) != 2) throw new AssertionError("extreme values");
        if (keepOnePerRun(new int[0]) != 0) throw new AssertionError("empty input");
        // Checks the method against a run counter on 3,000 random sorted arrays with extreme values.
        Random rnd = new Random(31);
        int[] pool = {Integer.MIN_VALUE, -1, 0, 7, Integer.MAX_VALUE};
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = pool[rnd.nextInt(pool.length)];
            Arrays.sort(x);
            int runs = 0;
            for (int i = 0; i < x.length; i++) if (i == 0 || x[i] != x[i - 1]) runs++;
            if (keepOnePerRun(x) != runs) throw new AssertionError("run count mismatch");
        }
    }
}
```

#### Solution: [Recognize] String Compression (LeetCode 443)
<!-- id: ar-string-compression -->

**Approach.** The method treats each maximal run of one character as a unit. A read index finds the end of the run, so the run length is known when the run finishes. The write index then writes the character and, when the length exceeds 1, the decimal digits of the length.

The write index never passes the read index. A run of length 1 writes one position for one read position. A run of length `L` greater than 1 writes `1 + d` positions, where `d` is the digit count of `L`, and `1 + d <= L` for every `L >= 2`. So the output never overtakes unread input. Digits are written without a temporary string. The method counts the digits first and then fills them from the last digit backward. The harness compares the method with a `StringBuilder` oracle on random arrays.

**Complexity.**

- **Time** is O(n), because the read index moves forward past each position once, and digit writing costs O(log L) per run, which sums to at most O(n).
- **Space** is O(1), because digits are written directly into the array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class StringCompression {
    /**
     * Compresses runs of equal characters in place and returns the new length.
     * Time: O(n), because the read index passes each position once and digit writing sums to at most n.
     * Space: O(1), because digits go straight into the array.
     * Invariant: chars[0..write-1] is the compressed form of every run finished so far.
     */
    static int compress(char[] chars) {
        // The write index is the next free position of the compressed prefix.
        int write = 0;
        // The read index marks the start of the current run.
        int read = 0;
        // Each outer pass handles exactly one run, so the loop ends after all runs are handled.
        while (read < chars.length) {
            // Remember the run's character, because writes may overwrite its first position.
            char ch = chars[read];
            // Advance the end marker to the first position after the run; the whole loop advances read once per position.
            int end = read;
            while (end < chars.length && chars[end] == ch) end++;
            // The run length is the distance between the start and the end marker.
            int length = end - read;
            // Write the character once for the run.
            chars[write++] = ch;
            // A length of 1 has no digits; a longer run writes its length.
            if (length > 1) {
                // Count the digits of the length so that the fill can start at the last digit.
                int digits = 0;
                for (int v = length; v > 0; v /= 10) digits++;
                // Fill the digits backward from the last position of the digit block.
                for (int pos = write + digits - 1, v = length; pos >= write; pos--, v /= 10) chars[pos] = (char) ('0' + v % 10);
                // Move the write index past the digit block.
                write += digits;
            }
            // Continue with the next run, which starts at the end marker.
            read = end;
        }
        // The write index is the compressed length.
        return write;
    }

    /** Reference answer built with a StringBuilder. */
    static String oracle(char[] chars) {
        // The builder holds the expected compressed text.
        StringBuilder sb = new StringBuilder();
        // Walk the runs and append the character and the length when it exceeds 1.
        for (int i = 0; i < chars.length; ) {
            int j = i;
            while (j < chars.length && chars[j] == chars[i]) j++;
            sb.append(chars[i]);
            if (j - i > 1) sb.append(j - i);
            i = j;
        }
        // Return the expected text.
        return sb.toString();
    }

    public static void main(String[] args) {
        // Checks Example 1: one x, twelve y, one z compress to "xy12z".
        char[] a = ("x" + "y".repeat(12) + "z").toCharArray();
        int k = compress(a);
        if (k != 5 || !new String(a, 0, k).equals("xy12z")) throw new AssertionError("example 1");
        // Checks Example 2: a run of 100 gives "q100", and a single character stays.
        char[] b = "q".repeat(100).toCharArray();
        k = compress(b);
        if (k != 4 || !new String(b, 0, k).equals("q100")) throw new AssertionError("run of 100");
        char[] c = {'a'};
        if (compress(c) != 1 || c[0] != 'a') throw new AssertionError("single character");
        // Checks the method against the oracle on 3,000 random arrays with long runs possible.
        Random rnd = new Random(37);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            int groups = 1 + rnd.nextInt(4);
            for (int g = 0; g < groups; g++) sb.append(String.valueOf((char) ('a' + rnd.nextInt(3))).repeat(1 + rnd.nextInt(14)));
            char[] x = sb.toString().toCharArray();
            String expected = oracle(x);
            int got = compress(x);
            if (!new String(x, 0, got).equals(expected)) throw new AssertionError("mismatch " + expected);
        }
    }
}
```
