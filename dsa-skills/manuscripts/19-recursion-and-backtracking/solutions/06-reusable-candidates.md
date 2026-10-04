<!-- solutions-for: 06-reusable-candidates -->
### Reusable Candidates

#### Solution: [Build] Sum With Repeated Coins (Author exercise)
<!-- id: bt-coin-ways -->

**Approach.** A call at position `start` with `left` still owed returns one when `left` is zero, and otherwise adds up the answers of paying each coin at a position from `start` onward that fits, passing the same position down. Because no path is stored, the call state is just the pair of numbers. The oracle is the classic table over amounts, which processes one coin value at a time and adds the ways of the amount less that coin, so it shares no search with the recursion. Random coin sets are compared for every price from 0 to 30, and a price of zero must give one handful.

**Complexity.** The number of calls is bounded by the number of handfuls times their length, and the stack is at most price divided by the smallest coin deep.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class CoinWays {
    static long count(int[] coins, int start, int left) {
        if (left == 0) return 1;
        long total = 0;
        for (int i = start; i < coins.length; i++) {
            if (coins[i] <= left) total += count(coins, i, left - coins[i]);
        }
        return total;
    }

    static long oracle(int[] coins, int price) {
        long[] ways = new long[price + 1];
        ways[0] = 1;
        for (int c : coins) for (int a = c; a <= price; a++) ways[a] += ways[a - c];
        return ways[price];
    }

    public static void main(String[] args) {
        if (count(new int[] {1, 2}, 0, 4) != 3) throw new AssertionError("example 1");
        if (count(new int[] {3}, 0, 7) != 0) throw new AssertionError("example 2");
        if (count(new int[] {3, 5}, 0, 0) != 1) throw new AssertionError("price zero");
        Random rnd = new Random(19601);
        for (int t = 0; t < 2000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(5);
            while (set.size() < n) set.add(1 + rnd.nextInt(20));
            int[] coins = set.stream().mapToInt(Integer::intValue).toArray();
            int price = rnd.nextInt(31);
            if (count(coins, 0, price) != oracle(coins, price)) throw new AssertionError("differs at price " + price);
        }
    }
}
```

#### Solution: [Vary] Combination Sum (LeetCode 39)
<!-- id: bt-combination-sum -->

**Approach.** The loop runs over positions from `start`, skips a candidate that exceeds `left`, appends it, recurses with the same position and removes it. A copy of the path is stored when `left` hits zero. No sort is needed, because the order of a combination is the order of positions, which the start position enforces, so the unsorted second example comes out as `[3, 2, 2]`. The oracle writes each combination as a vector of counts per candidate with an odometer, keeps those with the right sum, and sorts them by their position sequences, which is the order of the search because a finished path is never the prefix of another. The harness also runs the same code with a zero candidate and asserts that it overflows the stack, as the lesson says.

**Complexity.** The work is proportional to the number of search nodes, which is bounded by the handfuls and their lengths, and the stack depth is at most target divided by the smallest candidate.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class CombinationSum {
    static void pay(int[] c, int start, int left, List<Integer> path, List<List<Integer>> out) {
        if (left == 0) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < c.length; i++) {
            if (c[i] > left) continue;
            path.add(c[i]);
            pay(c, i, left - c[i], path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> solve(int[] c, int target) {
        List<List<Integer>> out = new ArrayList<>();
        pay(c, 0, target, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int[] c, int target) {
        int n = c.length;
        int[] maxUse = new int[n];
        for (int i = 0; i < n; i++) maxUse[i] = target / c[i];
        int[] use = new int[n];
        List<List<Integer>> positions = new ArrayList<>();
        while (true) {
            int sum = 0;
            for (int i = 0; i < n; i++) sum += use[i] * c[i];
            if (sum == target) {
                List<Integer> seq = new ArrayList<>();
                for (int i = 0; i < n; i++) for (int u = 0; u < use[i]; u++) seq.add(i);
                positions.add(seq);
            }
            int d = n - 1;
            while (d >= 0 && use[d] == maxUse[d]) use[d--] = 0;
            if (d < 0) break;
            use[d]++;
        }
        positions.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        List<List<Integer>> out = new ArrayList<>();
        for (List<Integer> seq : positions) {
            List<Integer> vals = new ArrayList<>();
            for (int p : seq) vals.add(c[p]);
            out.add(vals);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve(new int[] {2, 3, 6, 7}, 7).equals(List.of(List.of(2, 2, 3), List.of(7)))) throw new AssertionError("example 1");
        if (!solve(new int[] {3, 2}, 7).equals(List.of(List.of(3, 2, 2)))) throw new AssertionError("example 2");
        Random rnd = new Random(19602);
        for (int t = 0; t < 1500; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(5);
            while (set.size() < n) set.add(2 + rnd.nextInt(11));
            List<Integer> shuffled = new ArrayList<>(set);
            java.util.Collections.shuffle(shuffled, rnd);
            int[] c = shuffled.stream().mapToInt(Integer::intValue).toArray();
            int target = 1 + rnd.nextInt(24);
            if (!solve(c, target).equals(oracle(c, target))) throw new AssertionError("differs for target " + target);
        }
        boolean overflowed = false;
        try {
            solve(new int[] {0, 3}, 5);
        } catch (StackOverflowError e) {
            overflowed = true;
        }
        if (!overflowed) throw new AssertionError("a zero candidate never shrinks the target, so the stack must overflow");
    }
}
```

#### Solution: [Boundary] Candidate Larger Than Remainder (Author exercise)
<!-- id: bt-larger-than-remainder -->

**Approach.** With candidates in strictly ascending order, the first candidate that exceeds `left` is followed only by larger ones, so leaving the loop at that point loses nothing, and the count of comparisons falls. The harness also runs the version that skips with `continue` and asserts that it finds the same combinations with at least as many looks, and with strictly more on the first example, where the counts are 16 and 27. The oracle is an iterative search with an explicit stack of frames, which counts a look each time it advances a frame's position, and shares no recursion with the solution. An unsorted array is also tried, to show that leaving early then loses a combination, which is why the problem fixes the order.

**Complexity.** Fewer looks than a full scan of the candidates at every node, with the same asymptotic bound as the search without the early exit.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class LargerThanRemainder {
    static long looks;

    static int pay(int[] c, int start, int left, boolean leave) {
        if (left == 0) return 1;
        int found = 0;
        for (int i = start; i < c.length; i++) {
            looks++;
            if (c[i] > left) {
                if (leave) break;
                continue;
            }
            found += pay(c, i, left - c[i], leave);
        }
        return found;
    }

    static long[] run(int[] c, int target, boolean leave) {
        looks = 0;
        int found = pay(c, 0, target, leave);
        return new long[] {found, looks};
    }

    static long[] oracle(int[] c, int target) {
        long found = 0, seen = 0;
        Deque<int[]> stack = new ArrayDeque<>();
        stack.push(new int[] {0, target, 0});
        while (!stack.isEmpty()) {
            int[] f = stack.peek();
            if (f[1] == 0) { found++; stack.pop(); continue; }
            int i = f[0] + f[2];
            if (i >= c.length) { stack.pop(); continue; }
            seen++;
            if (c[i] > f[1]) { stack.pop(); continue; }
            f[2]++;
            stack.push(new int[] {i, f[1] - c[i], 0});
        }
        return new long[] {found, seen};
    }

    public static void main(String[] args) {
        long[] one = run(new int[] {2, 3, 6, 7}, 7, true);
        if (one[0] != 2 || one[1] != 16) throw new AssertionError("example 1: " + one[0] + "," + one[1]);
        long[] two = run(new int[] {5, 8}, 4, true);
        if (two[0] != 0 || two[1] != 1) throw new AssertionError("example 2");
        if (run(new int[] {2, 3, 6, 7}, 7, false)[1] != 27) throw new AssertionError("continue version makes 27 looks");
        int[] unsorted = {7, 2};
        if (run(unsorted, 9, true)[0] >= run(unsorted, 9, false)[0]) throw new AssertionError("leaving early on unsorted input loses a combination");
        Random rnd = new Random(19603);
        for (int t = 0; t < 2000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(6);
            while (set.size() < n) set.add(1 + rnd.nextInt(12));
            int[] c = set.stream().mapToInt(Integer::intValue).toArray();
            int target = 1 + rnd.nextInt(24);
            long[] a = run(c, target, true), b = run(c, target, false), o = oracle(c, target);
            if (a[0] != o[0] || a[1] != o[1]) throw new AssertionError("differs for target " + target);
            if (b[0] != a[0] || b[1] < a[1]) throw new AssertionError("continue version: same answers, no fewer looks");
        }
    }
}
```

#### Solution: [Recognize] Fixed-Length Reusable Sum (Author exercise)
<!-- id: bt-fixed-length-reuse -->

**Approach.** The call state gains `picks`, the number of values still to place, next to `left`. A combination is recorded only when both are zero, a call with `picks` at zero and `left` above zero returns at once, and the loop keeps the same-index call. Combinations of size zero with target zero give one empty list. The oracle runs an odometer over all sequences of k positions, keeps the nondecreasing ones that sum to the target, and so lists them in the order of the search. The harness compares both over random candidate sets, with k from 0 to 6 and targets up to 30.

**Complexity.** The depth is at most k, so at most n^k nodes in the worst case, which is well under fifty thousand for these limits.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class FixedLengthReuse {
    static void pick(int[] c, int start, int picks, int left, List<Integer> path, List<List<Integer>> out) {
        if (picks == 0) {
            if (left == 0) out.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < c.length; i++) {
            if (c[i] > left) continue;
            path.add(c[i]);
            pick(c, i, picks - 1, left - c[i], path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> solve(int[] c, int k, int target) {
        List<List<Integer>> out = new ArrayList<>();
        pick(c, 0, k, target, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int[] c, int k, int target) {
        int n = c.length;
        List<List<Integer>> out = new ArrayList<>();
        int[] seq = new int[k];
        while (true) {
            boolean up = true;
            int sum = 0;
            for (int j = 0; j < k; j++) {
                sum += c[seq[j]];
                if (j > 0 && seq[j] < seq[j - 1]) up = false;
            }
            if (up && sum == target) {
                List<Integer> vals = new ArrayList<>();
                for (int j = 0; j < k; j++) vals.add(c[seq[j]]);
                out.add(vals);
            }
            int d = k - 1;
            while (d >= 0 && seq[d] == n - 1) seq[d--] = 0;
            if (d < 0) break;
            seq[d]++;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve(new int[] {1, 2, 3}, 3, 6).equals(List.of(List.of(1, 2, 3), List.of(2, 2, 2)))) throw new AssertionError("example 1");
        if (!solve(new int[] {4, 6}, 2, 9).isEmpty()) throw new AssertionError("example 2");
        List<List<Integer>> zero = solve(new int[] {5}, 0, 0);
        if (zero.size() != 1 || !zero.get(0).isEmpty()) throw new AssertionError("k = 0 and target 0");
        if (!solve(new int[] {5}, 0, 3).isEmpty()) throw new AssertionError("k = 0 and target 3");
        Random rnd = new Random(19604);
        for (int t = 0; t < 2000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(5);
            while (set.size() < n) set.add(1 + rnd.nextInt(10));
            int[] c = set.stream().mapToInt(Integer::intValue).toArray();
            int k = rnd.nextInt(6);
            int target = rnd.nextInt(31);
            if (!solve(c, k, target).equals(oracle(c, k, target))) throw new AssertionError("differs for k=" + k + ", target=" + target);
        }
    }
}
```
