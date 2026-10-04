<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Tie Order

#### Solution: [Build] Stable Score Sort (Author exercise)
<!-- id: so-stable-tickets -->

**Approach.**
The method builds one `Ticket` record per id and sorts the tickets with a comparator that reads only the priority. `Arrays.sort` on an object array is stable, so tickets with equal priority keep the order of the input. When the sort finishes, adjacent tickets have a smaller priority on the left, or an equal priority and an earlier input position. The harness compares the answer with a bucket oracle that groups ids by priority in input order. It also asserts the two reversal facts from the lesson.

**Complexity.**
- **Time** is O(n log n), because the library sort makes that many comparisons of two integers.
- **Space** is O(n) for the records, the answer and the sort buffer.

```java run
import java.util.*;

public final class StableTickets {
    record Ticket(String id, int priority) {}

    /**
     * Returns the ids ordered by priority, with equal priorities in input order.
     * Time: O(n log n). Space: O(n).
     * Invariant: adjacent tickets are ordered by priority, and ties follow the input order.
     */
    static String[] order(String[] ids, int[] priorities) {
        Ticket[] tickets = new Ticket[ids.length];
        for (int i = 0; i < ids.length; i++) tickets[i] = new Ticket(ids[i], priorities[i]);
        // The object sort is stable, so the comparator needs only the key.
        Arrays.sort(tickets, Comparator.comparingInt(Ticket::priority));
        String[] out = new String[tickets.length];
        for (int i = 0; i < out.length; i++) out[i] = tickets[i].id();
        return out;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!Arrays.equals(order(new String[] {"A", "B", "C"}, new int[] {2, 2, 1}), new String[] {"C", "A", "B"})) throw new AssertionError("example 1");
        if (!Arrays.equals(order(new String[] {"x", "y", "z", "w"}, new int[] {5, 1, 5, 1}), new String[] {"y", "w", "x", "z"})) throw new AssertionError("example 2");
        if (order(new String[0], new int[0]).length != 0) throw new AssertionError("empty");
        // Java facts from the lesson: reversing the comparator keeps ties in input order, reversing the array flips them.
        Ticket[] a = {new Ticket("A", 1), new Ticket("B", 1), new Ticket("C", 2)};
        Ticket[] byComparator = a.clone();
        Arrays.sort(byComparator, Comparator.comparingInt(Ticket::priority).reversed());
        if (!byComparator[1].id().equals("A") || !byComparator[2].id().equals("B")) throw new AssertionError("comparator reversal");
        Ticket[] byArray = a.clone();
        Arrays.sort(byArray, Comparator.comparingInt(Ticket::priority));
        Collections.reverse(Arrays.asList(byArray));
        if (!byArray[1].id().equals("B") || !byArray[2].id().equals("A")) throw new AssertionError("array reversal");
        // Random inputs are checked against a bucket oracle.
        Random rnd = new Random(91);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(10);
            String[] ids = new String[n];
            int[] pr = new int[n];
            for (int k = 0; k < n; k++) { ids[k] = "t" + k; pr[k] = rnd.nextInt(4) - 1; }
            List<String> expect = new ArrayList<>();
            for (int p = -1; p <= 2; p++) for (int k = 0; k < n; k++) if (pr[k] == p) expect.add(ids[k]);
            if (!Arrays.equals(order(ids, pr), expect.toArray(new String[0]))) throw new AssertionError(Arrays.toString(pr));
        }
    }
}
```

#### Solution: [Vary] Explicit Index Tie (Author exercise)
<!-- id: so-index-tie -->

**Approach.**
The method sorts an `Integer[]` of the indexes `0` to `n - 1`. The comparator looks up the two keys and compares them with `Integer.compare`. When the keys are equal, it compares the indexes themselves. No two positions tie, because indexes are distinct, so the output is the same for every correct sort and the comparator does not depend on stability. At the end of the sort, adjacent indexes have smaller keys, or equal keys and a smaller index on the left.

**Complexity.**
- **Time** is O(n log n), because each comparison reads two keys and two indexes.
- **Space** is O(n), because of the boxed indexes and the answer.

```java run
import java.util.*;

public final class IndexTie {
    /**
     * Returns the indexes of keys ordered by key, with ties by smaller index.
     * Time: O(n log n). Space: O(n).
     * Invariant: adjacent indexes are ordered by (key, index).
     */
    static int[] orderByValue(int[] keys) {
        Integer[] positions = new Integer[keys.length];
        // Each position starts as its own index.
        for (int i = 0; i < keys.length; i++) positions[i] = i;
        // The index is the last key, so no two positions compare as zero.
        Arrays.sort(positions, (a, b) -> keys[a] != keys[b] ? Integer.compare(keys[a], keys[b]) : Integer.compare(a, b));
        int[] out = new int[keys.length];
        for (int i = 0; i < out.length; i++) out[i] = positions[i];
        return out;
    }

    public static void main(String[] args) {
        // The statement examples, the empty input and the extreme keys.
        if (!Arrays.equals(orderByValue(new int[] {30, 10, 30, 20}), new int[] {1, 3, 0, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(orderByValue(new int[] {4, 4, 4}), new int[] {0, 1, 2})) throw new AssertionError("example 2");
        if (orderByValue(new int[0]).length != 0) throw new AssertionError("empty");
        if (!Arrays.equals(orderByValue(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE}), new int[] {1, 0})) throw new AssertionError("extremes");
        // Random inputs are checked against a pairwise rank oracle: the rank counts positions that must come earlier.
        Random rnd = new Random(92);
        for (int t = 0; t < 500; t++) {
            int[] keys = new int[rnd.nextInt(10)];
            for (int k = 0; k < keys.length; k++) keys[k] = rnd.nextInt(5) == 0 ? Integer.MIN_VALUE : rnd.nextInt(4);
            int[] expect = new int[keys.length];
            for (int i = 0; i < keys.length; i++) {
                int rank = 0;
                for (int j = 0; j < keys.length; j++) if (keys[j] < keys[i] || (keys[j] == keys[i] && j < i)) rank++;
                expect[rank] = i;
            }
            if (!Arrays.equals(orderByValue(keys), expect)) throw new AssertionError(Arrays.toString(keys));
        }
    }
}
```

#### Solution: [Boundary] Comparator Equality (Author exercise)
<!-- id: so-case-ties -->

**Approach.**
The comparator applies `String.CASE_INSENSITIVE_ORDER` first. When that result is zero, it compares the two words with `compareTo` and swaps the arguments, so the word that is greater under `compareTo` comes first. For ASCII letters, a lowercase letter has a larger code than its uppercase form, so lowercase comes first. The second key returns zero only for identical strings, which are interchangeable. The harness asserts that the first key alone returns zero for `"a"` and `"A"`, which shows why the second key is needed.

**Complexity.**
- **Time** is O(n log n * m), where m is the longest word, because each comparison reads at most m characters.
- **Space** is O(n) for the copy and the sort buffer.

```java run
import java.util.*;

public final class CaseTies {
    /**
     * Returns the words sorted ignoring case, with lowercase before uppercase on a case-only tie.
     * Time: O(n log n * m). Space: O(n).
     * Invariant: the comparator returns zero only for identical strings.
     */
    static String[] sortWords(String[] words) {
        String[] copy = words.clone();
        // The swapped compareTo puts the greater string, which has the lowercase letter, first.
        Arrays.sort(copy, String.CASE_INSENSITIVE_ORDER.thenComparing((a, b) -> b.compareTo(a)));
        return copy;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!Arrays.equals(sortWords(new String[] {"bee", "Ant", "ant", "Bee"}), new String[] {"ant", "Ant", "bee", "Bee"})) throw new AssertionError("example 1");
        if (!Arrays.equals(sortWords(new String[] {"a", "A", "a"}), new String[] {"a", "a", "A"})) throw new AssertionError("example 2");
        if (sortWords(new String[0]).length != 0) throw new AssertionError("empty");
        // Java facts from the lesson: the first key ties for case-only differences, and a lowercase letter has the larger code.
        if (String.CASE_INSENSITIVE_ORDER.compare("a", "A") != 0) throw new AssertionError("first key ties");
        if ("a".compareTo("A") <= 0) throw new AssertionError("code order");
        // Random inputs are checked against an oracle that orders by a lowercase key and then by an inverted-case key.
        Random rnd = new Random(93);
        for (int t = 0; t < 500; t++) {
            String[] w = new String[rnd.nextInt(8)];
            for (int k = 0; k < w.length; k++) {
                StringBuilder sb = new StringBuilder();
                for (int len = rnd.nextInt(4); len > 0; len--) sb.append(rnd.nextBoolean() ? (char) ('a' + rnd.nextInt(2)) : (char) ('A' + rnd.nextInt(2)));
                w[k] = sb.toString();
            }
            String[] expect = w.clone();
            // The inverted-case key maps lowercase to uppercase, so a plain ascending sort puts the original lowercase first.
            Arrays.sort(expect, Comparator.comparing((String s) -> s.toLowerCase())
                    .thenComparing(s -> s.chars().mapToObj(c -> String.valueOf(Character.isLowerCase(c) ? Character.toUpperCase((char) c) : Character.toLowerCase((char) c))).reduce("", String::concat)));
            if (!Arrays.equals(sortWords(w), expect)) throw new AssertionError(Arrays.toString(w));
        }
    }
}
```

#### Solution: [Recognize] Sort Integers By The Number Of 1 Bits (LeetCode 1356)
<!-- id: so-bit-count -->

**Approach.**
The method boxes the values and sorts them with a comparator that reads `Integer.bitCount` first and the value second. Both keys use `Integer.compare` through `comparingInt` and `naturalOrder`, so nothing overflows. The second key makes the order independent of the input order, because two equal values are interchangeable and two different values with the same bit count differ in value. Afterward, adjacent integers are ordered by the pair (bit count, value).

**Complexity.**
- **Time** is O(n log n), because each comparison counts the bits of two 32-bit values in constant time.
- **Space** is O(n) for the boxed array.

```java run
import java.util.*;

public final class BitCountSort {
    /**
     * Returns arr ordered by bit count and then by value.
     * Time: O(n log n). Space: O(n).
     * Invariant: adjacent values are ordered by (bit count, value).
     */
    static int[] sortByBits(int[] arr) {
        Integer[] boxed = new Integer[arr.length];
        for (int i = 0; i < arr.length; i++) boxed[i] = arr[i];
        // The value is the tie key, so the order does not depend on the input order.
        Arrays.sort(boxed, Comparator.comparingInt(Integer::bitCount).thenComparing(Comparator.naturalOrder()));
        int[] out = new int[arr.length];
        for (int i = 0; i < out.length; i++) out[i] = boxed[i];
        return out;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!Arrays.equals(sortByBits(new int[] {1024, 3, Integer.MAX_VALUE, 6}), new int[] {1024, 3, 6, Integer.MAX_VALUE})) throw new AssertionError("example 1");
        if (!Arrays.equals(sortByBits(new int[] {5, 5, 0}), new int[] {0, 5, 5})) throw new AssertionError("example 2");
        if (sortByBits(new int[0]).length != 0) throw new AssertionError("empty");
        // Random inputs, shuffled in several orders, must give the same answer, and must match a pairwise rank oracle.
        Random rnd = new Random(94);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(5) == 0 ? Integer.MAX_VALUE : rnd.nextInt(20);
            int[] b = a.clone();
            for (int k = b.length - 1; k > 0; k--) { int j = rnd.nextInt(k + 1); int tmp = b[k]; b[k] = b[j]; b[j] = tmp; }
            int[] r = sortByBits(a);
            if (!Arrays.equals(r, sortByBits(b))) throw new AssertionError("depends on input order");
            for (int k = 1; k < r.length; k++) {
                int c1 = Integer.bitCount(r[k - 1]), c2 = Integer.bitCount(r[k]);
                if (c1 > c2 || (c1 == c2 && r[k - 1] > r[k])) throw new AssertionError(Arrays.toString(r));
            }
        }
    }
}
```
