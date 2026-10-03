<!-- solutions-for: 07-prefix-xor -->
### Prefix XOR

#### Solution: [Build] XOR Log (LeetCode 1310)
<!-- id: ps-xor-log -->

**Approach.** The log stores, for every appended value, the XOR of everything appended so far, in a growing list that starts with a single zero. An append reads the last stored value, XORs the new value into it and adds the result at the end. A query for positions `left` through `right` reads the stored value at `right + 1` and the stored value at `left` and XORs them, because XOR of a value with itself is zero, so the early values cancel. Nothing is recomputed when a new value arrives. The oracle keeps the raw values and XORs the stretch value by value.

**Complexity.** O(1) amortized for an append, O(1) for a query, and O(n) space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class XorLog {
    static final class Log {
        private final List<Integer> px = new ArrayList<>();
        Log() { px.add(0); }
        void append(int value) { px.add(px.get(px.size() - 1) ^ value); }
        int query(int left, int right) { return px.get(right + 1) ^ px.get(left); }
    }

    public static void main(String[] args) {
        Log log = new Log();
        for (int v : new int[] {6, 2, 7, 4}) log.append(v);
        if (log.query(1, 3) != 1) throw new AssertionError("example 1");
        Log two = new Log();
        two.append(9);
        two.append(9);
        if (two.query(0, 1) != 0) throw new AssertionError("example 2");
        if (log.query(0, 0) != 6) throw new AssertionError("first value alone");
        Random rnd = new Random(7701);
        for (int t = 0; t < 300; t++) {
            Log x = new Log();
            List<Integer> raw = new ArrayList<>();
            for (int step = 0; step < 40; step++) {
                if (raw.isEmpty() || rnd.nextInt(3) != 0) {
                    int v = rnd.nextInt(1000000001);
                    x.append(v);
                    raw.add(v);
                } else {
                    int l = rnd.nextInt(raw.size());
                    int r = l + rnd.nextInt(raw.size() - l);
                    int want = 0;
                    for (int i = l; i <= r; i++) want ^= raw.get(i);
                    if (x.query(l, r) != want) throw new AssertionError("differs for " + l + "," + r);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Count XOR K (Author exercise)
<!-- id: ps-count-xor-k -->

**Approach.** A stretch ending at the current element has XOR `k` exactly when the prefix before its start equals the current prefix XOR `k`, because the early elements cancel. A map counts how often each prefix value has occurred, seeded with zero once for the empty start. At each element the prefix is updated, the complement `current ^ k` is looked up and added to the answer, and then the current prefix is recorded. Looking up before recording keeps a stretch from being empty when `k` is zero. The oracle XORs every stretch.

**Complexity.** One pass, linear expected time, and space proportional to the number of distinct prefixes.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class CountXorK {
    static int countXorK(int[] a, int k) {
        Map<Integer, Integer> seen = new HashMap<>();
        seen.put(0, 1);
        int current = 0, count = 0;
        for (int x : a) {
            current ^= x;
            count += seen.getOrDefault(current ^ k, 0);
            seen.merge(current, 1, Integer::sum);
        }
        return count;
    }
    static int oracle(int[] a, int k) {
        int count = 0;
        for (int i = 0; i < a.length; i++) {
            int x = 0;
            for (int j = i; j < a.length; j++) {
                x ^= a[j];
                if (x == k) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        if (countXorK(new int[] {4, 2, 2, 6, 4}, 6) != 4) throw new AssertionError("example 1");
        if (countXorK(new int[] {0, 0}, 0) != 3) throw new AssertionError("example 2");
        if (countXorK(new int[] {1, 2, 3}, 0) != 1) throw new AssertionError("one stretch cancels");
        Random rnd = new Random(7702);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(8);
            int k = rnd.nextInt(8);
            if (countXorK(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k);
        }
    }
}
```

#### Solution: [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-xor-empty-prefix -->

**Approach.** A stretch that starts at the first element pairs its end with the prefix before the array, whose XOR is zero. The set of seen prefix values therefore has to contain zero from the start, so the check `set.contains(current ^ k)` can find that partner. Each element updates `current`, tests the complement against the set, and then adds `current`. For `arr = [5]` and `k = 5`, the complement of the prefix 5 is zero, which is present only because of the seed. The program shows that the unseeded version answers false for that input, and that the seeded version matches an oracle on random arrays.

**Complexity.** One pass, linear expected time, and a set of at most n + 1 values.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class XorEmptyPrefix {
    static boolean hasStretch(int[] arr, int k) {
        Set<Integer> seen = new HashSet<>();
        seen.add(0);
        int current = 0;
        for (int x : arr) {
            current ^= x;
            if (seen.contains(current ^ k)) return true;
            seen.add(current);
        }
        return false;
    }
    static boolean unseeded(int[] arr, int k) {
        Set<Integer> seen = new HashSet<>();
        int current = 0;
        for (int x : arr) {
            current ^= x;
            if (seen.contains(current ^ k)) return true;
            seen.add(current);
        }
        return false;
    }
    static boolean oracle(int[] arr, int k) {
        for (int i = 0; i < arr.length; i++) {
            int x = 0;
            for (int j = i; j < arr.length; j++) {
                x ^= arr[j];
                if (x == k) return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        if (!hasStretch(new int[] {5}, 5)) throw new AssertionError("example 1");
        if (hasStretch(new int[] {1, 2, 4}, 8)) throw new AssertionError("example 2");
        if (!hasStretch(new int[] {1, 2, 4}, 7)) throw new AssertionError("whole array");
        if (unseeded(new int[] {5}, 5)) throw new AssertionError("the unseeded set should miss the first element");
        Random rnd = new Random(7703);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(16);
            int k = rnd.nextInt(16);
            if (hasStretch(a, k) != oracle(a, k)) throw new AssertionError("seeded differs for k=" + k);
            if (unseeded(a, k) && !oracle(a, k)) throw new AssertionError("unseeded cannot invent a stretch");
        }
    }
}
```

#### Solution: [Recognize] Count Triplets That Can Form Two Arrays of Equal XOR (LeetCode 1442)
<!-- id: ps-equal-xor-triplets -->

**Approach.** If the XOR of the values from `i` to `j - 1` equals the XOR of the values from `j` to `k`, then the XOR of the whole stretch from `i` to `k` is zero, and the converse also holds, so every split point of a zero-XOR stretch gives a valid triple. Write prefix values `px[0..n]`. A zero-XOR stretch from `i` to `k` is a pair of equal prefix values at slots `i` and `k + 1`, and it has `k - i` split points, which is the distance between the two slots minus one. Summing over pairs of equal prefixes gives the answer. A map from a prefix value to a count and a sum of slot positions computes the sum of distances in one pass: for the slot `p`, the contribution is the count times `p - 1` minus the sum of earlier slots. The oracle tries every triple directly.

**Complexity.** The one-pass method is linear in expected time with a map of at most n + 1 entries.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class EqualXorTriplets {
    static long countTriplets(int[] arr) {
        Map<Integer, long[]> seen = new HashMap<>();
        seen.put(0, new long[] {1, 0});
        int current = 0;
        long total = 0;
        for (int p = 1; p <= arr.length; p++) {
            current ^= arr[p - 1];
            long[] slot = seen.computeIfAbsent(current, v -> new long[2]);
            total += slot[0] * (p - 1) - slot[1];
            slot[0]++;
            slot[1] += p;
        }
        return total;
    }
    static long oracle(int[] arr) {
        int n = arr.length;
        long count = 0;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                for (int k = j; k < n; k++) {
                    int x = 0, y = 0;
                    for (int t = i; t < j; t++) x ^= arr[t];
                    for (int t = j; t <= k; t++) y ^= arr[t];
                    if (x == y) count++;
                }
        return count;
    }

    public static void main(String[] args) {
        if (countTriplets(new int[] {2, 3, 1, 6, 7}) != 4) throw new AssertionError("example 1");
        if (countTriplets(new int[] {1, 1, 1, 1, 1}) != 10) throw new AssertionError("example 2");
        if (countTriplets(new int[] {7}) != 0) throw new AssertionError("a single value");
        Random rnd = new Random(7704);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(6);
            if (countTriplets(a) != oracle(a)) throw new AssertionError("differs on " + java.util.Arrays.toString(a));
        }
    }
}
```
