<!-- solutions-for: 05-binary-tries -->
### Solutions For Picking The Best XOR Partner

#### Solution: [Build] Insert Fixed-Width Bits (Author exercise)
<!-- id: tr-insert-fixed-width-bits -->

**Approach.**
The method inserts every value as a path of exactly `width` bits, from bit `width - 1` down to bit 0. Each node has two links. A missing link creates a node and increments the count. A value shorter than the width still walks all levels, because its leading bits are zeros. A repeated value finds every link present and creates nothing. The count therefore equals the number of distinct nonempty bit prefixes of the stored values.

Before each insert the tree holds one node per distinct bit prefix of the earlier values.

**Complexity.**
- **Time** is O(n * width), because each value takes `width` steps.
- **Space** is O(n * width) in the worst case, because each value adds at most `width` nodes.

```java run
import java.util.*;

public final class InsertFixedWidthBits {
    private static final class Node { final Node[] next = new Node[2]; }

    /**
     * Returns the number of nodes below the root after inserting all values as width-bit paths.
     * Time: O(n * width). Space: O(n * width).
     * Invariant: the tree holds one node per distinct bit prefix of the values inserted so far.
     */
    static int countNodes(int[] values, int width) {
        Node root = new Node();
        int created = 0;
        for (int v : values) {
            Node cur = root;
            for (int b = width - 1; b >= 0; b--) {                 // highest bit first, always width steps
                int bit = (v >> b) & 1;
                if (cur.next[bit] == null) { cur.next[bit] = new Node(); created++; }   // a missing link costs one node
                cur = cur.next[bit];
            }
        }
        return created;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countNodes(new int[] {1, 2, 3}, 3) != 6) throw new AssertionError("ex1");
        if (countNodes(new int[] {5, 5}, 3) != 3) throw new AssertionError("ex2");
        // An empty array creates nothing, and one value creates exactly width nodes.
        if (countNodes(new int[0], 4) != 0 || countNodes(new int[] {0}, 31) != 31) throw new AssertionError("edges");
        // Random inputs must match a set of distinct bit-prefix strings.
        Random rnd = new Random(1851);
        for (int t = 0; t < 400; t++) {
            int width = 1 + rnd.nextInt(6);
            int[] v = new int[rnd.nextInt(8)];
            Set<String> prefixes = new HashSet<>();
            for (int i = 0; i < v.length; i++) {
                v[i] = rnd.nextInt(1 << width);
                StringBuilder sb = new StringBuilder();
                for (int b = width - 1; b >= 0; b--) { sb.append((v[i] >> b) & 1); prefixes.add(sb.toString()); }
            }
            if (countNodes(v, width) != prefixes.size()) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Best XOR Partner (Author exercise)
<!-- id: tr-best-xor-partner -->

**Approach.**
The method inserts every stored value as a 31-bit path. For a query `x` the walk reads the bits of `x` from bit 30 down to bit 0. At each bit it takes the child with the opposite bit when that child exists, and it sets the same bit in the result. When the opposite child is missing, the walk takes the child with the same bit and leaves the result bit at 0. The greedy choice is correct because one bit of the result at a higher position is worth more than all lower bits together. Because a stored value exists, one of the two children always exists.

After the bits above position `b` the walk stands on the path of a stored value that maximizes the result bits above `b`.

**Complexity.**
- **Time** is O((n + q) * 31) for `n` stored values and `q` queries.
- **Space** is O(n * 31) for the nodes.

```java run
import java.util.*;

public final class BestXorPartner {
    private static final class Node { final Node[] next = new Node[2]; }

    /**
     * Returns the largest query ^ stored value for each query.
     * Time: O((n + q) * 31). Space: O(31 * n).
     * Invariant: after the bits above b the walk stands on a stored value that maximizes those result bits.
     */
    static int[] best(int[] stored, int[] queries) {
        Node root = new Node();
        for (int v : stored) {
            Node cur = root;
            for (int b = 30; b >= 0; b--) {
                int bit = (v >> b) & 1;
                if (cur.next[bit] == null) cur.next[bit] = new Node();
                cur = cur.next[bit];
            }
        }
        int[] out = new int[queries.length];
        for (int j = 0; j < queries.length; j++) {
            Node cur = root;
            int res = 0;
            for (int b = 30; b >= 0; b--) {                        // decide the result bits from the highest
                int bit = (queries[j] >> b) & 1;
                if (cur.next[1 - bit] != null) { res |= 1 << b; cur = cur.next[1 - bit]; }   // opposite child puts a 1 in the result
                else cur = cur.next[bit];                          // only the same child exists, so this result bit is 0
            }
            out[j] = res;
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(best(new int[] {3, 10, 5, 25, 2, 8}, new int[] {5, 2}), new int[] {28, 27})) throw new AssertionError("ex1");
        if (!Arrays.equals(best(new int[] {7}, new int[] {0, 7}), new int[] {7, 0})) throw new AssertionError("ex2");
        // The largest int value works with the 31-bit width.
        if (best(new int[] {0}, new int[] {Integer.MAX_VALUE})[0] != Integer.MAX_VALUE) throw new AssertionError("max int");
        // Random inputs must match the pair loop.
        Random rnd = new Random(1852);
        for (int t = 0; t < 400; t++) {
            int[] s = new int[1 + rnd.nextInt(6)];
            int[] q = new int[rnd.nextInt(6)];
            for (int i = 0; i < s.length; i++) s[i] = rnd.nextInt(t % 2 == 0 ? 16 : Integer.MAX_VALUE);
            for (int i = 0; i < q.length; i++) q[i] = rnd.nextInt(t % 2 == 0 ? 16 : Integer.MAX_VALUE);
            int[] expect = new int[q.length];
            for (int j = 0; j < q.length; j++) for (int x : s) expect[j] = Math.max(expect[j], q[j] ^ x);
            if (!Arrays.equals(best(s, q), expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Equal Values And Sign Policy (Author exercise)
<!-- id: tr-equal-values-sign-policy -->

**Approach.**
The contract allows only nonnegative ints, so bit 31 is always 0 and 31 bits per path are enough. The method scans the array once. For position `i` it queries the tree, which holds the values at positions below `i`, and it then inserts `values[i]`. The query comes first, so a value never pairs with itself, and an equal value at an earlier position still forms a valid pair with XOR 0. An array with fewer than two values returns -1 because no pair exists. For the first position the tree is empty, so the method skips the query.

At position `i` the tree holds exactly the values at positions `0..i-1`, so every pair `(j, i)` with `j < i` is considered once.

**Complexity.**
- **Time** is O(n * 31), because each position costs one query and one insert of 31 steps.
- **Space** is O(n * 31) for the nodes.

```java run
import java.util.*;

public final class EqualValuesSignPolicy {
    private static final class Node { final Node[] next = new Node[2]; }

    /**
     * Returns the largest values[i] ^ values[j] for i < j, or -1 when no pair exists.
     * Time: O(31 n). Space: O(31 n).
     * Invariant: at position i the tree holds the values at positions below i.
     */
    static int maxPair(int[] values) {
        if (values.length < 2) return -1;                          // no pair of different positions
        Node root = new Node();
        int best = -1;
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {                                           // the tree is empty before the first insert
                Node cur = root;
                int res = 0;
                for (int b = 30; b >= 0; b--) {
                    int bit = (values[i] >> b) & 1;
                    if (cur.next[1 - bit] != null) { res |= 1 << b; cur = cur.next[1 - bit]; }
                    else cur = cur.next[bit];
                }
                best = Math.max(best, res);
            }
            Node cur = root;                                       // insert after the query, so no self pair
            for (int b = 30; b >= 0; b--) {
                int bit = (values[i] >> b) & 1;
                if (cur.next[bit] == null) cur.next[bit] = new Node();
                cur = cur.next[bit];
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (maxPair(new int[] {6, 6, 6}) != 0) throw new AssertionError("ex1");
        if (maxPair(new int[] {Integer.MAX_VALUE, 0}) != Integer.MAX_VALUE) throw new AssertionError("ex2");
        // Fewer than two values give -1.
        if (maxPair(new int[0]) != -1 || maxPair(new int[] {5}) != -1) throw new AssertionError("short");
        // Random inputs must match the pair loop over i < j.
        Random rnd = new Random(1853);
        for (int t = 0; t < 400; t++) {
            int[] v = new int[rnd.nextInt(8)];
            for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(t % 3 == 0 ? 4 : Integer.MAX_VALUE);
            int expect = -1;
            for (int i = 0; i < v.length; i++) for (int j = i + 1; j < v.length; j++) expect = Math.max(expect, v[i] ^ v[j]);
            if (maxPair(v) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Maximum XOR of Two Numbers in an Array (LeetCode 421)
<!-- id: tr-maximum-xor-pair -->

**Approach.**
The problem asks for the largest XOR, so the highest differing bit decides which partner is best. The method inserts all numbers into a tree of 31-bit paths. It then queries each number against the whole tree. A query takes the opposite child when it exists, and the result then gains that bit. A number may pair with itself, which gives 0, so the whole tree is a valid partner set and the answer is never negative. The maximum over all queries is the answer.

For each number the walk returns the largest XOR with any number in the array, so the maximum over all numbers is the maximum over all pairs.

**Complexity.**
- **Time** is O(31 n), because each number costs one insert and one query of 31 steps.
- **Space** is O(31 n) for the nodes.

```java run
import java.util.*;

public final class MaximumXorPair {
    private static final class Node { final Node[] next = new Node[2]; }

    /**
     * Returns the maximum nums[i] ^ nums[j] over i <= j.
     * Time: O(31 n). Space: O(31 n).
     * Invariant: query(x) returns the largest x ^ y over all y stored in the tree.
     */
    static int findMaximumXOR(int[] nums) {
        Node root = new Node();
        for (int v : nums) {                                       // build the whole tree first
            Node cur = root;
            for (int b = 30; b >= 0; b--) {
                int bit = (v >> b) & 1;
                if (cur.next[bit] == null) cur.next[bit] = new Node();
                cur = cur.next[bit];
            }
        }
        int best = 0;
        for (int x : nums) {                                       // then query every number against all numbers
            Node cur = root;
            int res = 0;
            for (int b = 30; b >= 0; b--) {
                int bit = (x >> b) & 1;
                if (cur.next[1 - bit] != null) { res |= 1 << b; cur = cur.next[1 - bit]; }   // prefer the opposite branch
                else cur = cur.next[bit];
            }
            best = Math.max(best, res);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (findMaximumXOR(new int[] {3, 10, 5, 25, 2, 8}) != 28) throw new AssertionError("ex1");
        if (findMaximumXOR(new int[] {14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70}) != 127) throw new AssertionError("ex2");
        // One element pairs with itself, so the answer is 0.
        if (findMaximumXOR(new int[] {9}) != 0) throw new AssertionError("single");
        // Random inputs must match the pair loop over i <= j.
        Random rnd = new Random(1854);
        for (int t = 0; t < 400; t++) {
            int[] v = new int[1 + rnd.nextInt(8)];
            for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(t % 2 == 0 ? 32 : Integer.MAX_VALUE);
            int expect = 0;
            for (int i = 0; i < v.length; i++) for (int j = i; j < v.length; j++) expect = Math.max(expect, v[i] ^ v[j]);
            if (findMaximumXOR(v) != expect) throw new AssertionError("random " + t);
        }
    }
}
```
