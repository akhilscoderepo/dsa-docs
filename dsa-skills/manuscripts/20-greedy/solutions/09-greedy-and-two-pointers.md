<!-- solutions-for: 20-greedy -->
### Greedy And Two Pointers

#### Solution: [Build] Assign Cookies (LeetCode 455)
<!-- id: gc-cookies-with-tolerance -->

**Approach.** Sort clones of both arrays and keep a cursor `i` over children and `j` over cookies. If the current cookie is smaller than the current child's greed, it is too small for this child and for every later one, so `j` advances. If it is larger than `greed + tol`, computed in `long`, it is too big for this child, and since later cookies are no smaller the child can never be served, so `i` advances. Otherwise the pair is made and both advance. The assertions check both examples, a window that reaches past `Integer.MAX_VALUE`, and random small inputs against an exhaustive matching in which each child may take any unused cookie inside its window.

**Complexity.** The sorts cost O(n log n + m log m) and each loop step moves at least one cursor, so the pass takes at most n + m steps.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CookiesWithTolerance {
    static int satisfied(int[] greed, int[] sizes, int tol) {
        int[] g = greed.clone(), s = sizes.clone();
        Arrays.sort(g);
        Arrays.sort(s);
        int i = 0, j = 0, matched = 0;
        while (i < g.length && j < s.length) {
            if (s[j] < g[i]) j++;
            else if ((long) s[j] > (long) g[i] + tol) i++;
            else { matched++; i++; j++; }
        }
        return matched;
    }

    static int oracle(int[] g, int[] s, int tol, int idx, boolean[] taken) {
        if (idx == g.length) return 0;
        int best = oracle(g, s, tol, idx + 1, taken);
        for (int c = 0; c < s.length; c++) {
            if (!taken[c] && s[c] >= g[idx] && (long) s[c] <= (long) g[idx] + tol) {
                taken[c] = true;
                best = Math.max(best, 1 + oracle(g, s, tol, idx + 1, taken));
                taken[c] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (satisfied(new int[]{1, 4, 9}, new int[]{2, 3, 10, 7}, 2) != 2) throw new AssertionError("example 1");
        if (satisfied(new int[]{3, 3, 5}, new int[]{3, 5, 5, 6}, 0) != 2) throw new AssertionError("example 2");
        if (satisfied(new int[0], new int[]{4}, 3) != 0) throw new AssertionError("no children");
        if (satisfied(new int[]{4}, new int[0], 3) != 0) throw new AssertionError("no cookies");
        int top = Integer.MAX_VALUE;
        if (satisfied(new int[]{top - 1}, new int[]{top}, top) != 1) throw new AssertionError("window past the int range");
        if (top - 1 + top >= 0) throw new AssertionError("the int sum greed + tol must wrap negative");
        int[] g = {9, 1}, s = {5, 1};
        satisfied(g, s, 0);
        if (g[0] != 9 || s[0] != 5) throw new AssertionError("inputs were reordered");

        Random rnd = new Random(2901);
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(7), m = rnd.nextInt(7);
            int[] gr = new int[n], sz = new int[m];
            for (int i = 0; i < n; i++) gr[i] = 1 + rnd.nextInt(10);
            for (int i = 0; i < m; i++) sz[i] = 1 + rnd.nextInt(12);
            int tol = rnd.nextInt(4);
            if (satisfied(gr, sz, tol) != oracle(gr, sz, tol, 0, new boolean[m])) throw new AssertionError("disagrees with the exhaustive matching");
        }
    }
}
```

#### Solution: [Vary] Boats to Save People (LeetCode 881)
<!-- id: gc-boats-limit -->

**Approach.** Sort a clone and place a pointer at each end. The heaviest person always departs in this boat. The lightest joins when the two are different people and their combined weight, summed in `long`, is at most the limit. If the lightest cannot fit with the heaviest, nobody can, so the heaviest rides alone. The swap argument shows that pairing the heaviest with the lightest never costs a boat. The assertions check both examples, show that the int sum of the two largest weights wraps below the limit, and compare random cases with the exhaustive pairing search.

**Complexity.** The sort costs O(n log n) and the two pointers make n steps in total, with O(n) memory for the clone.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BoatsLimit {
    static int boats(int[] people, int limit) {
        int[] p = people.clone();
        Arrays.sort(p);
        int lo = 0, hi = p.length - 1, count = 0;
        while (lo <= hi) {
            if (lo < hi && (long) p[lo] + p[hi] <= limit) lo++;
            hi--;
            count++;
        }
        return count;
    }

    static int oracle(long[] w, boolean[] used, long limit) {
        int i = 0;
        while (i < w.length && used[i]) i++;
        if (i == w.length) return 0;
        used[i] = true;
        int best = 1 + oracle(w, used, limit);
        for (int j = i + 1; j < w.length; j++) {
            if (!used[j] && w[i] + w[j] <= limit) {
                used[j] = true;
                best = Math.min(best, 1 + oracle(w, used, limit));
                used[j] = false;
            }
        }
        used[i] = false;
        return best;
    }

    public static void main(String[] args) {
        if (boats(new int[]{7, 2, 5, 3, 4}, 9) != 3) throw new AssertionError("example 1");
        if (boats(new int[]{Integer.MAX_VALUE, Integer.MAX_VALUE}, Integer.MAX_VALUE) != 2) throw new AssertionError("example 2");
        int wrapped = Integer.MAX_VALUE + Integer.MAX_VALUE;
        if (wrapped > Integer.MAX_VALUE || wrapped >= 0) throw new AssertionError("the int sum must wrap negative, which would wrongly pass a limit test");
        if (boats(new int[0], 5) != 0) throw new AssertionError("nobody waiting");
        if (boats(new int[]{4}, 4) != 1) throw new AssertionError("one person");
        if (boats(new int[]{5, 5, 5, 5}, 10) != 2) throw new AssertionError("exact fits");
        if (boats(new int[]{6, 6, 6}, 10) != 3) throw new AssertionError("nobody can share");

        Random rnd = new Random(2902);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(9);
            int limit = 1 + rnd.nextInt(12);
            int[] people = new int[n];
            long[] w = new long[n];
            for (int i = 0; i < n; i++) { people[i] = 1 + rnd.nextInt(limit); w[i] = people[i]; }
            if (boats(people, limit) != oracle(w, new boolean[n], limit)) throw new AssertionError("disagrees with the pairing search on " + Arrays.toString(people) + " limit " + limit);
        }
    }
}
```

#### Solution: [Boundary] Exact Capacity And One Remaining Person (Author exercise)
<!-- id: gc-exact-capacity-last-person -->

**Approach.** Use the same two pointers, with the pairing test `p[lo] + p[hi] <= limit` in `long` so that equality is allowed, and with the extra condition `lo < hi` so that a person is never paired with themselves. Every iteration is one boat, and an iteration that advances `lo` is a boat with two people. When the pointers land on the same person the test `lo < hi` fails, the person departs alone, and the loop ends, so the last singleton is counted once. The oracle simulates the same rule with a deque of sorted weights, and a separate exhaustive search confirms the boat count. The assertions check both examples and random inputs.

**Complexity.** One sort and one pass give O(n log n) time with O(n) memory for the clone.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class ExactCapacityLastPerson {
    static int[] run(int[] people, int limit) {
        int[] p = people.clone();
        Arrays.sort(p);
        int lo = 0, hi = p.length - 1, boats = 0, pairs = 0;
        while (lo <= hi) {
            if (lo < hi && (long) p[lo] + p[hi] <= limit) { lo++; pairs++; }
            hi--;
            boats++;
        }
        return new int[]{boats, pairs};
    }

    static int[] deque(int[] people, int limit) {
        int[] p = people.clone();
        Arrays.sort(p);
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        for (int v : p) dq.addLast(v);
        int boats = 0, pairs = 0;
        while (!dq.isEmpty()) {
            int heavy = dq.pollLast();
            boats++;
            if (!dq.isEmpty() && (long) dq.peekFirst() + heavy <= limit) { dq.pollFirst(); pairs++; }
        }
        return new int[]{boats, pairs};
    }

    static int bruteBoats(int[] w, boolean[] used, int limit) {
        int i = 0;
        while (i < w.length && used[i]) i++;
        if (i == w.length) return 0;
        used[i] = true;
        int best = 1 + bruteBoats(w, used, limit);
        for (int j = i + 1; j < w.length; j++) {
            if (!used[j] && (long) w[i] + w[j] <= limit) {
                used[j] = true;
                best = Math.min(best, 1 + bruteBoats(w, used, limit));
                used[j] = false;
            }
        }
        used[i] = false;
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[]{3, 3, 3}, 6), new int[]{2, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[]{5}, 5), new int[]{1, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(run(new int[0], 5), new int[]{0, 0})) throw new AssertionError("nobody waiting");
        if (!Arrays.equals(run(new int[]{2, 2, 2, 2}, 4), new int[]{2, 2})) throw new AssertionError("all exact pairs");
        if (!Arrays.equals(run(new int[]{1, 9, 9, 9}, 10), new int[]{3, 1})) throw new AssertionError("only one pair fits");

        Random rnd = new Random(2903);
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(9);
            int limit = 1 + rnd.nextInt(10);
            int[] people = new int[n];
            for (int i = 0; i < n; i++) people[i] = 1 + rnd.nextInt(limit);
            int[] got = run(people, limit);
            if (!Arrays.equals(got, deque(people, limit))) throw new AssertionError("differs from the deque simulation");
            if (got[0] != bruteBoats(people, new boolean[n], limit)) throw new AssertionError("not the fewest boats");
            if (got[0] - got[1] + got[1] * 2 != n) throw new AssertionError("every person must ride exactly once");
        }
    }
}
```

#### Solution: [Recognize] Bag of Tokens (LeetCode 948)
<!-- id: gc-bag-of-tokens -->

**Approach.** Sort a clone. While the pointers have not crossed, play the cheapest remaining token face up if the energy allows, which gains a point and updates the best score. If it is too dear and a point is in hand, play the dearest remaining token face down, which returns the most energy for one point. If neither is possible, stop. The energy is a `long`, because selling large tokens can push it past the `int` range, as the second example shows. The oracle explores every order of face-up and face-down plays and takes the highest score ever held. The assertions check both examples and random small inputs.

**Complexity.** The sort costs O(n log n) and the pointer loop makes at most n steps.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BagOfTokens {
    static int bestScore(int[] tokens, long power) {
        int[] t = tokens.clone();
        Arrays.sort(t);
        int lo = 0, hi = t.length - 1, score = 0, best = 0;
        while (lo <= hi) {
            if (power >= t[lo]) { power -= t[lo++]; score++; best = Math.max(best, score); }
            else if (score > 0) { power += t[hi--]; score--; }
            else break;
        }
        return best;
    }

    static int oracle(int[] t, int mask, long power, int score) {
        int best = score;
        for (int i = 0; i < t.length; i++) {
            if ((mask >> i & 1) == 1) continue;
            if (power >= t[i]) best = Math.max(best, oracle(t, mask | 1 << i, power - t[i], score + 1));
            if (score > 0) best = Math.max(best, oracle(t, mask | 1 << i, power + t[i], score - 1));
        }
        return best;
    }

    public static void main(String[] args) {
        if (bestScore(new int[]{60, 20, 90, 30, 10}, 45) != 3) throw new AssertionError("example 1");
        if (bestScore(new int[]{Integer.MAX_VALUE, 1, Integer.MAX_VALUE}, Integer.MAX_VALUE) != 1) throw new AssertionError("example 2");
        long afterSale = (long) (Integer.MAX_VALUE - 1) + Integer.MAX_VALUE;
        if (afterSale <= Integer.MAX_VALUE) throw new AssertionError("the energy in example 2 passes the int range");
        if (bestScore(new int[0], 5) != 0) throw new AssertionError("no tokens");
        if (bestScore(new int[]{50}, 50) != 1) throw new AssertionError("exactly enough energy");
        if (bestScore(new int[]{51}, 50) != 0) throw new AssertionError("one short");
        if (bestScore(new int[]{100, 200}, 150) != 1) throw new AssertionError("selling does not beat holding a point");
        if (bestScore(new int[]{100}, 4000000000L) != 1) throw new AssertionError("energy above the int range");

        Random rnd = new Random(2904);
        for (int t = 0; t < 700; t++) {
            int n = rnd.nextInt(7);
            int[] tokens = new int[n];
            for (int i = 0; i < n; i++) tokens[i] = 1 + rnd.nextInt(12);
            long power = rnd.nextInt(15);
            if (bestScore(tokens, power) != oracle(tokens, 0, power, 0)) throw new AssertionError("disagrees with the exhaustive play on " + Arrays.toString(tokens) + " power " + power);
        }
    }
}
```
