<!-- solutions-for: 05-comparator-contracts -->
### Comparator Contracts

#### Solution: [Build] Safe Integer Comparator (Author exercise)
<!-- id: so-safe-integer-comparator -->

**Approach.** Define the comparator as `(x, y) -> Integer.compare(x, y)`, which returns the sign without computing a difference, and pass it to `List.sort`. The test compares the sorted list with the natural order, and also with a `long`-based oracle that sorts by the exact value `(long) x`, over random lists in which a fifth of the elements are the two extreme values.

**Complexity.** O(n log n) time and O(n) extra space for the list sort.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class SafeIntegerComparator {
    static final Comparator<Integer> ASCENDING = (x, y) -> Integer.compare(x, y);

    static List<Integer> sorted(List<Integer> in) {
        List<Integer> out = new ArrayList<>(in);
        out.sort(ASCENDING);
        return out;
    }
    static List<Integer> oracle(List<Integer> in) {
        List<Integer> out = new ArrayList<>(in);
        out.sort(Comparator.comparingLong(x -> (long) x));
        return out;
    }

    public static void main(String[] args) {
        if (!sorted(List.of(5, -3, 5, 0)).equals(List.of(-3, 0, 5, 5))) throw new AssertionError("example 1");
        if (!sorted(List.of(Integer.MAX_VALUE, Integer.MIN_VALUE, -1)).equals(List.of(Integer.MIN_VALUE, -1, Integer.MAX_VALUE))) throw new AssertionError("example 2");
        if (!sorted(List.of()).isEmpty()) throw new AssertionError("empty list");
        if (ASCENDING.compare(3, 3) != 0) throw new AssertionError("ties return zero");
        Random rnd = new Random(521);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(25);
            List<Integer> in = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(10);
                in.add(pick == 0 ? Integer.MIN_VALUE : pick == 1 ? Integer.MAX_VALUE : rnd.nextInt(21) - 10);
            }
            if (!sorted(in).equals(oracle(in))) throw new AssertionError("differs from the long oracle on " + in);
        }
    }
}
```

#### Solution: [Vary] Chained Keys (Author exercise)
<!-- id: so-chained-keys -->

**Approach.** Build the order as `comparingInt(priority).reversed()` followed by `thenComparingInt(time)`. The `reversed()` call applies only to the priority comparator it follows, so higher priority comes first, and the opening time is consulted only when priorities tie and runs ascending. The test compares with a hand-written nested-conditional oracle on random tickets, and checks that two tickets equal in both keys compare as zero.

**Complexity.** O(n log n) time; the extra space is O(n) for the copy that is sorted.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

public final class ChainedKeys {
    record Ticket(int priority, int time) {}

    static final Comparator<Ticket> ORDER =
        Comparator.comparingInt(Ticket::priority).reversed().thenComparingInt(Ticket::time);

    static Ticket[] arrange(Ticket[] in) {
        Ticket[] out = in.clone();
        Arrays.sort(out, ORDER);
        return out;
    }
    static int handWritten(Ticket a, Ticket b) {
        if (a.priority() != b.priority()) return a.priority() > b.priority() ? -1 : 1;
        return Integer.compare(a.time(), b.time());
    }

    public static void main(String[] args) {
        Ticket[] ex1 = arrange(new Ticket[] {new Ticket(2, 10), new Ticket(5, 30), new Ticket(5, 20)});
        if (!Arrays.equals(ex1, new Ticket[] {new Ticket(5, 20), new Ticket(5, 30), new Ticket(2, 10)})) throw new AssertionError("example 1");
        if (ORDER.compare(new Ticket(3, 7), new Ticket(3, 7)) != 0) throw new AssertionError("example 2: interchangeable tickets tie");
        if (arrange(new Ticket[0]).length != 0) throw new AssertionError("empty input");
        Random rnd = new Random(522);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(15);
            Ticket[] in = new Ticket[n];
            for (int i = 0; i < n; i++) in[i] = new Ticket(1 + rnd.nextInt(5), rnd.nextInt(6));
            Ticket[] got = arrange(in);
            for (int i = 1; i < n; i++) {
                if (handWritten(got[i - 1], got[i]) > 0) throw new AssertionError("out of order at " + i + " in " + Arrays.toString(got));
            }
            Ticket[] expected = in.clone();
            for (int i = 1; i < n; i++) {
                Ticket x = expected[i]; int j = i - 1;
                while (j >= 0 && handWritten(expected[j], x) > 0) { expected[j + 1] = expected[j]; j--; }
                expected[j + 1] = x;
            }
            if (!Arrays.equals(got, expected)) throw new AssertionError("differs from the insertion oracle on " + Arrays.toString(in));
        }
    }
}
```

#### Solution: [Boundary] Equal Keys And Extreme Values (Author exercise)
<!-- id: so-equal-keys-extreme -->

**Approach.** The checker tests, for every pair, that the two signs are opposite, and for every triple that "not after" chains: if `a` is not after `b` and `b` is not after `d`, then `a` is not after `d`. A comparator returning `a < b ? -1 : 1` fails on equal values, since each of two equal elements is reported to come after the other. The subtraction comparator fails because the minimum and maximum disagree about which comes first once the difference wraps. The program asserts that the correct comparator passes the checker and both broken ones fail it, on a sample with the extremes and a repeated value.

**Complexity.** The checker is O(m^3) for a sample of m elements, which is acceptable as a test tool for m up to about a dozen.

```java run
import java.util.Comparator;
import java.util.List;

public final class EqualKeysExtreme {
    static <T> boolean obeysLaws(Comparator<T> c, List<T> sample) {
        for (T a : sample) {
            for (T b : sample) {
                if (Integer.signum(c.compare(a, b)) != -Integer.signum(c.compare(b, a))) return false;
                for (T d : sample) {
                    if (c.compare(a, b) <= 0 && c.compare(b, d) <= 0 && c.compare(a, d) > 0) return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        List<Integer> sample = List.of(Integer.MIN_VALUE, -1, 0, 0, 7, Integer.MAX_VALUE, 7);
        Comparator<Integer> good = Integer::compare;
        Comparator<Integer> neverZero = (a, b) -> a < b ? -1 : 1;
        Comparator<Integer> subtraction = (a, b) -> a - b;
        if (!obeysLaws(good, sample)) throw new AssertionError("example 1: the library comparator is lawful");
        if (obeysLaws(neverZero, sample)) throw new AssertionError("example 2: a comparator that never returns zero fails on ties");
        if (obeysLaws(subtraction, sample)) throw new AssertionError("subtraction breaks at the extremes");
        if (obeysLaws(neverZero, List.of(1, 2, 3))) throw new AssertionError("even without ties, an element compared with itself must give zero");
        if (neverZero.compare(4, 4) != 1) throw new AssertionError("tied elements are each reported as after the other");
        if (good.compare(0, 0) != 0) throw new AssertionError("a tie returns zero");
        if (!obeysLaws(good, List.<Integer>of())) throw new AssertionError("empty sample is vacuously lawful");
    }
}
```

#### Solution: [Recognize] Largest Number (LeetCode 179)
<!-- id: so-largest-number-laws -->

**Approach.** Name the comparator `GLUE`, defined as `(y + x).compareTo(x + y)`, so that the piece whose concatenation comes out larger goes first and a tie in both orders returns zero. Sort the strings with it, then collapse a leading `"0"` to `"0"`. To see why it is a valid order, run the law checker on the pieces: the program does that on every input. The oracle is a bitmask recursion that builds the best string by trying each unused piece as the next one, which does not use sorting at all.

**Complexity.** O(n log n) comparisons for the sort, each costing a bounded number of characters; the law check is O(n^3) and only appears in tests.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class LargestNumberLaws {
    static final Comparator<String> GLUE = (x, y) -> (y + x).compareTo(x + y);

    static String largest(int[] nums) {
        String[] p = new String[nums.length];
        for (int i = 0; i < p.length; i++) p[i] = String.valueOf(nums[i]);
        Arrays.sort(p, GLUE);
        return p[0].equals("0") ? "0" : String.join("", p);
    }
    static boolean obeysLaws(Comparator<String> c, List<String> sample) {
        for (String a : sample) for (String b : sample) {
            if (Integer.signum(c.compare(a, b)) != -Integer.signum(c.compare(b, a))) return false;
            for (String d : sample)
                if (c.compare(a, b) <= 0 && c.compare(b, d) <= 0 && c.compare(a, d) > 0) return false;
        }
        return true;
    }
    static String bestJoin(String[] p, int used) {
        if (used == (1 << p.length) - 1) return "";
        String best = null;
        for (int i = 0; i < p.length; i++) {
            if ((used & (1 << i)) != 0) continue;
            String cand = p[i] + bestJoin(p, used | (1 << i));
            if (best == null || cand.compareTo(best) > 0) best = cand;
        }
        return best;
    }

    public static void main(String[] args) {
        if (!largest(new int[] {12, 121}).equals("12121")) throw new AssertionError("example 1");
        if (!largest(new int[] {2, 22, 222}).equals("222222")) throw new AssertionError("example 2");
        if (GLUE.compare("2", "22") != 0) throw new AssertionError("tied pieces return zero");
        if (!largest(new int[] {0, 0}).equals("0")) throw new AssertionError("all zeros");
        Random rnd = new Random(523);
        int[] pool = {0, 1, 2, 22, 222, 3, 30, 34, 12, 121, 9, 90, 909, 100000};
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(6);
            int[] a = new int[n];
            String[] p = new String[n];
            for (int i = 0; i < n; i++) { a[i] = pool[rnd.nextInt(pool.length)]; p[i] = String.valueOf(a[i]); }
            if (!obeysLaws(GLUE, Arrays.asList(p))) throw new AssertionError("glue order broke a law on " + Arrays.toString(p));
            String expected = bestJoin(p, 0);
            if (expected.charAt(0) == '0') expected = "0";
            if (!largest(a).equals(expected)) throw new AssertionError("differs from the recursion oracle on " + Arrays.toString(a));
        }
        Comparator<String> broken = (x, y) -> y.length() != x.length() ? Integer.compare(y.length(), x.length()) : y.compareTo(x) >= 0 ? 1 : -1;
        if (obeysLaws(broken, List.of("5", "5"))) throw new AssertionError("a never-zero comparator fails on equal pieces");
    }
}
```
