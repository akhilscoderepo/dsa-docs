<!-- solutions-for: 05-binary-tries -->
### Binary Tries

#### Solution: [Build] Insert Fixed-Width Bits (Author exercise)
<!-- id: tn-insert-fixed-bits -->

**Approach.** Each value is written with exactly `w` bits, read from bit `w - 1` down to bit 0 with `(v >>> b) & 1`, and each bit is an edge to a child node that is created only when missing. Every path has length `w`, so leading zeros are real edges, and the leaves are the nodes at depth `w`. The solution counts creations during insertion and counts leaves by one more walk. The oracle builds the set of all bit-string prefixes of every value as text, whose size is the node count, and the set of full strings, whose size is the leaf count. The assertions compare the two on random widths and value lists, including repeated values.

**Complexity.** O(n * w) time and at most n * w nodes.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class InsertFixedBits {
    static final class Node {
        final Node[] kid = new Node[2];
    }

    static int[] solve(int w, int[] values) {
        Node root = new Node();
        int nodes = 0;
        for (int v : values) {
            Node cur = root;
            for (int b = w - 1; b >= 0; b--) {
                int bit = (v >>> b) & 1;
                if (cur.kid[bit] == null) { cur.kid[bit] = new Node(); nodes++; }
                cur = cur.kid[bit];
            }
        }
        int leaves = 0;
        List<Node> level = new ArrayList<>(List.of(root));
        for (int d = 0; d < w; d++) {
            List<Node> down = new ArrayList<>();
            for (Node n : level) for (Node k : n.kid) if (k != null) down.add(k);
            level = down;
        }
        leaves = level.size();
        return new int[] {nodes, leaves};
    }

    static int[] oracle(int w, int[] values) {
        Set<String> prefixes = new HashSet<>(), full = new HashSet<>();
        for (int v : values) {
            StringBuilder sb = new StringBuilder();
            for (int b = w - 1; b >= 0; b--) {
                sb.append((v >> b) & 1);
                prefixes.add(sb.toString());
            }
            full.add(sb.toString());
        }
        return new int[] {prefixes.size(), full.size()};
    }

    static void same(int[] a, int[] b, String what) {
        if (a[0] != b[0] || a[1] != b[1]) throw new AssertionError(what + ": " + a[0] + "," + a[1] + " vs " + b[0] + "," + b[1]);
    }

    public static void main(String[] args) {
        same(solve(3, new int[] {1, 2, 3, 5}), new int[] {9, 4}, "example 1");
        same(solve(4, new int[] {8, 8, 0}), new int[] {8, 2}, "example 2");
        same(solve(5, new int[] {}), new int[] {0, 0}, "no values");
        Random rnd = new Random(18501);
        for (int t = 0; t < 5000; t++) {
            int w = 1 + rnd.nextInt(8);
            int[] values = new int[rnd.nextInt(10)];
            for (int i = 0; i < values.length; i++) values[i] = rnd.nextInt(1 << w);
            same(solve(w, values), oracle(w, values), "random w=" + w);
        }
    }
}
```

#### Solution: [Vary] Best XOR Partner (Author exercise)
<!-- id: tn-best-xor-partner -->

**Approach.** Insert every stored number with bits 30 down to 0. For a query, walk from the top bit and prefer the child whose bit differs from the query bit. When it exists, the result gains that bit and the walk moves into it. Otherwise the walk moves into the only child, which exists because every stored number has a path of full length. The oracle tries every stored number with `^`. The assertions compare the two on random numbers drawn from small ranges, where many numbers share top bits, and from the full range, where they do not.

**Complexity.** O(31) per insertion and per query.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class BestXorPartner {
    static final class Node {
        final Node[] kid = new Node[2];
    }

    static List<Integer> solve(int[] stored, int[] queries) {
        Node root = new Node();
        for (int v : stored) {
            Node cur = root;
            for (int b = 30; b >= 0; b--) {
                int bit = (v >>> b) & 1;
                if (cur.kid[bit] == null) cur.kid[bit] = new Node();
                cur = cur.kid[bit];
            }
        }
        List<Integer> out = new ArrayList<>();
        for (int x : queries) {
            Node cur = root;
            int score = 0;
            for (int b = 30; b >= 0; b--) {
                int want = 1 - ((x >>> b) & 1);
                if (cur.kid[want] != null) { score |= 1 << b; cur = cur.kid[want]; }
                else cur = cur.kid[1 - want];
            }
            out.add(score);
        }
        return out;
    }

    static List<Integer> oracle(int[] stored, int[] queries) {
        List<Integer> out = new ArrayList<>();
        for (int x : queries) {
            int best = 0;
            for (int y : stored) best = Math.max(best, x ^ y);
            out.add(best);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve(new int[] {6, 12, 9, 30, 17}, new int[] {9, 17, 0}).equals(List.of(24, 29, 30))) throw new AssertionError("example 1");
        if (!solve(new int[] {1}, new int[] {1, 0}).equals(List.of(0, 1))) throw new AssertionError("example 2");
        if (!solve(new int[] {Integer.MAX_VALUE}, new int[] {0}).equals(List.of(Integer.MAX_VALUE))) throw new AssertionError("all 31 bits");
        Random rnd = new Random(18502);
        for (int t = 0; t < 5000; t++) {
            int range = rnd.nextBoolean() ? 64 : Integer.MAX_VALUE;
            int[] stored = new int[1 + rnd.nextInt(8)], queries = new int[1 + rnd.nextInt(8)];
            for (int i = 0; i < stored.length; i++) stored[i] = rnd.nextInt(range);
            for (int i = 0; i < queries.length; i++) queries[i] = rnd.nextInt(range);
            if (!solve(stored, queries).equals(oracle(stored, queries))) throw new AssertionError("differs");
        }
    }
}
```

#### Solution: [Boundary] Equal Values And Sign Policy (Author exercise)
<!-- id: tn-equal-and-sign -->

**Approach.** The policy is stated first: width 32, bits 31 down to 0, and the result read as an unsigned number held in a `long`. Each value is queried against the trie of the values before it and then inserted, so a value never pairs with itself, while an equal value at another position still forms a pair and gives 0. A list with fewer than two entries returns -1. The first query of a trie is skipped because it is empty, which also avoids following a missing child. The result is built in a `long` with `1L << b`, so bit 31 does not become negative. The oracle takes the exclusive or of every pair of positions and masks it to 32 bits. The assertions check the Java facts the lesson relies on: `1 << 31` is negative, `-1 >>> 31` is 1 while `-1 >> 31` is -1, and querying an empty trie fails.

**Complexity.** O(n * 32) time and space.

```java run
import java.util.Random;

public final class EqualAndSign {
    static final class Node {
        final Node[] kid = new Node[2];
    }

    static long solve(int[] values) {
        if (values.length < 2) return -1;
        Node root = new Node();
        long best = 0;
        for (int i = 0; i < values.length; i++) {
            int x = values[i];
            if (i > 0) {
                Node cur = root;
                long score = 0;
                for (int b = 31; b >= 0; b--) {
                    int want = 1 - ((x >>> b) & 1);
                    if (cur.kid[want] != null) { score |= 1L << b; cur = cur.kid[want]; }
                    else cur = cur.kid[1 - want];
                }
                best = Math.max(best, score);
            }
            Node cur = root;
            for (int b = 31; b >= 0; b--) {
                int bit = (x >>> b) & 1;
                if (cur.kid[bit] == null) cur.kid[bit] = new Node();
                cur = cur.kid[bit];
            }
        }
        return best;
    }

    static long oracle(int[] values) {
        if (values.length < 2) return -1;
        long best = 0;
        for (int i = 0; i < values.length; i++)
            for (int j = i + 1; j < values.length; j++) best = Math.max(best, (values[i] ^ values[j]) & 0xFFFFFFFFL);
        return best;
    }

    public static void main(String[] args) {
        if (solve(new int[] {5, -5}) != 4294967294L) throw new AssertionError("example 1");
        if (solve(new int[] {7, 7, 7}) != 0) throw new AssertionError("example 2");
        if (solve(new int[] {3}) != -1 || solve(new int[] {}) != -1) throw new AssertionError("fewer than two");
        if ((1 << 31) >= 0) throw new AssertionError("1 << 31 is the sign bit");
        if ((-1 >>> 31) != 1 || (-1 >> 31) != -1) throw new AssertionError("unsigned shift does not smear the sign");
        boolean failed = false;
        try {
            Node empty = new Node();
            Node cur = empty;
            for (int b = 31; b >= 0; b--) cur = cur.kid[1 - ((5 >>> b) & 1)].kid[0];
        } catch (NullPointerException e) { failed = true; }
        if (!failed) throw new AssertionError("a query on an empty trie must fail");
        Random rnd = new Random(18503);
        for (int t = 0; t < 5000; t++) {
            int[] values = new int[rnd.nextInt(9)];
            int mode = rnd.nextInt(3);
            for (int i = 0; i < values.length; i++) values[i] = mode == 0 ? rnd.nextInt() : mode == 1 ? rnd.nextInt(5) - 2 : rnd.nextInt(4) * Integer.MIN_VALUE;
            if (solve(values) != oracle(values)) throw new AssertionError("differs");
        }
    }
}
```

#### Solution: [Recognize] Maximum XOR of Two Numbers in an Array (LeetCode 421)
<!-- id: tn-max-xor-pair -->

**Approach.** Store all numbers in a binary trie of 31 levels, then take the best partner of each number and keep the largest score. A number may pair with itself, which scores 0, and that never beats a real pair, so storing everything first is safe and the answer is never negative. The trie is kept in two parallel integer arrays instead of node objects, which saves memory for two hundred thousand numbers: `child[2 * id + bit]` is the id of a child or 0 when missing, with id 0 reserved for the root. The oracle checks every pair, including a number with itself. The assertions compare the two on random arrays, and check a large array of 200000 numbers against a second method, the standard shrinking-mask method with a hash set, which agrees on the answer.

**Complexity.** O(31 * n) time, and O(31 * n) space for the child arrays.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class MaxXorPair {
    static int solve(int[] nums) {
        int[] child = new int[2 * (31 * nums.length + 1)];
        int size = 1;
        for (int v : nums) {
            int cur = 0;
            for (int b = 30; b >= 0; b--) {
                int slot = 2 * cur + ((v >>> b) & 1);
                if (child[slot] == 0) child[slot] = size++;
                cur = child[slot];
            }
        }
        int best = 0;
        for (int x : nums) {
            int cur = 0, score = 0;
            for (int b = 30; b >= 0; b--) {
                int bit = (x >>> b) & 1;
                if (child[2 * cur + 1 - bit] != 0) { score |= 1 << b; cur = child[2 * cur + 1 - bit]; }
                else cur = child[2 * cur + bit];
            }
            best = Math.max(best, score);
        }
        return best;
    }

    static int oracle(int[] nums) {
        int best = 0;
        for (int a : nums) for (int b : nums) best = Math.max(best, a ^ b);
        return best;
    }

    static int byMasks(int[] nums) {
        int best = 0, mask = 0;
        for (int b = 30; b >= 0; b--) {
            mask |= 1 << b;
            Set<Integer> heads = new HashSet<>();
            for (int v : nums) heads.add(v & mask);
            int attempt = best | (1 << b);
            for (int h : heads) if (heads.contains(h ^ attempt)) { best = attempt; break; }
        }
        return best;
    }

    public static void main(String[] args) {
        if (solve(new int[] {14, 11, 7, 2}) != 12) throw new AssertionError("example 1");
        if (solve(new int[] {4096, 4095}) != 8191) throw new AssertionError("example 2");
        if (solve(new int[] {0}) != 0 || solve(new int[] {9}) != 0) throw new AssertionError("single number pairs with itself");
        Random rnd = new Random(18504);
        for (int t = 0; t < 5000; t++) {
            int range = rnd.nextBoolean() ? 32 : Integer.MAX_VALUE;
            int[] nums = new int[1 + rnd.nextInt(9)];
            for (int i = 0; i < nums.length; i++) nums[i] = rnd.nextInt(range);
            if (solve(nums) != oracle(nums)) throw new AssertionError("differs");
        }
        int[] big = new int[200000];
        for (int i = 0; i < big.length; i++) big[i] = rnd.nextInt(Integer.MAX_VALUE);
        if (solve(big) != byMasks(big)) throw new AssertionError("large array disagrees with the mask method");
    }
}
```
