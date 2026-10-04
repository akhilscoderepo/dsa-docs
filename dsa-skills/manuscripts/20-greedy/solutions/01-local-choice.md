<!-- solutions-for: 20-greedy -->
### Local Choice

#### Solution: [Build] Smallest Sufficient Match (Author exercise)
<!-- id: gr-smallest-sufficient-match -->

**Approach.** Order the party indexes by need, with the lower index first on a tie, and give each party in that order the smallest unused room that fits, again preferring the lower room index. The rooms are scanned with a flag array, so no room is ever removed from the input. The assertions check both examples, then compare random cases with the exhaustive search from the lesson: the assignment must be legal, with distinct rooms that are large enough, and the number of housed parties must equal the best total over all pairings. The caller's arrays are compared with copies to show that they are untouched.

**Complexity.** Sorting the indexes takes O(n log n), and each party then scans every room, so the whole method is O(n log n + n·m).

```java run
import java.util.Arrays;
import java.util.Random;

public final class SmallestSufficientMatch {
    static int[] assign(int[] need, int[] beds) {
        Integer[] order = new Integer[need.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> need[a] != need[b] ? Integer.compare(need[a], need[b]) : Integer.compare(a, b));
        int[] out = new int[need.length];
        Arrays.fill(out, -1);
        boolean[] used = new boolean[beds.length];
        for (int p : order) {
            int pick = -1;
            for (int r = 0; r < beds.length; r++) {
                if (!used[r] && beds[r] >= need[p] && (pick == -1 || beds[r] < beds[pick])) pick = r;
            }
            if (pick >= 0) { used[pick] = true; out[p] = pick; }
        }
        return out;
    }

    static int bestHoused(int[] need, int[] beds, int g, boolean[] taken) {
        if (g == need.length) return 0;
        int best = bestHoused(need, beds, g + 1, taken);
        for (int r = 0; r < beds.length; r++) {
            if (!taken[r] && beds[r] >= need[g]) {
                taken[r] = true;
                best = Math.max(best, 1 + bestHoused(need, beds, g + 1, taken));
                taken[r] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(assign(new int[]{2, 5, 1}, new int[]{4, 1, 6}), new int[]{0, 2, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(assign(new int[]{3, 3}, new int[]{2, 9}), new int[]{1, -1})) throw new AssertionError("example 2");
        if (assign(new int[0], new int[]{5}).length != 0) throw new AssertionError("no parties");
        if (!Arrays.equals(assign(new int[]{1}, new int[0]), new int[]{-1})) throw new AssertionError("no rooms");
        if (!Arrays.equals(assign(new int[]{2, 2}, new int[]{2, 2}), new int[]{0, 1})) throw new AssertionError("ties take the lower index");

        Random rnd = new Random(2001);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(7), m = rnd.nextInt(7);
            int[] need = new int[n], beds = new int[m];
            for (int i = 0; i < n; i++) need[i] = 1 + rnd.nextInt(8);
            for (int i = 0; i < m; i++) beds[i] = 1 + rnd.nextInt(8);
            int[] needCopy = need.clone(), bedsCopy = beds.clone();
            int[] got = assign(need, beds);
            if (!Arrays.equals(need, needCopy) || !Arrays.equals(beds, bedsCopy)) throw new AssertionError("input was modified");
            boolean[] seen = new boolean[m];
            int housed = 0;
            for (int p = 0; p < n; p++) {
                if (got[p] == -1) continue;
                if (seen[got[p]] || beds[got[p]] < need[p]) throw new AssertionError("illegal assignment for " + Arrays.toString(need) + " " + Arrays.toString(beds));
                seen[got[p]] = true;
                housed++;
            }
            if (housed != bestHoused(need, beds, 0, new boolean[m])) throw new AssertionError("not a best total for " + Arrays.toString(need) + " " + Arrays.toString(beds));
        }
    }
}
```

#### Solution: [Vary] Assign Cookies (LeetCode 455)
<!-- id: gr-assign-cookies -->

**Approach.** Sort clones of both arrays. The cookie cursor moves forward on every step. The child cursor moves only when the current cookie is at least as large as the current child's greed, which both consumes the cookie and satisfies the child. A cookie that is too small for the least greedy waiting child is too small for every later child, so it is dropped. The assertions check the examples, a pair of values at `Integer.MAX_VALUE`, and the exhaustive search on random small cases, and they confirm that the arrays passed in keep their order.

**Complexity.** Two sorts dominate, so the time is O(n log n + m log m), plus a pass of n + m steps; the clones cost O(n + m) memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class AssignCookies {
    static int findContentChildren(int[] greed, int[] sizes) {
        int[] g = greed.clone(), s = sizes.clone();
        Arrays.sort(g);
        Arrays.sort(s);
        int child = 0;
        for (int cookie = 0; cookie < s.length && child < g.length; cookie++) {
            if (s[cookie] >= g[child]) child++;
        }
        return child;
    }

    static int oracle(int[] g, int[] s, int idx, boolean[] taken) {
        if (idx == g.length) return 0;
        int best = oracle(g, s, idx + 1, taken);
        for (int c = 0; c < s.length; c++) {
            if (!taken[c] && s[c] >= g[idx]) {
                taken[c] = true;
                best = Math.max(best, 1 + oracle(g, s, idx + 1, taken));
                taken[c] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (findContentChildren(new int[]{2, 5, 1, 9}, new int[]{3, 1, 6}) != 3) throw new AssertionError("example 1");
        if (findContentChildren(new int[]{3, 3, 3}, new int[]{3, 9}) != 2) throw new AssertionError("example 2");
        if (findContentChildren(new int[0], new int[]{4}) != 0) throw new AssertionError("no children");
        if (findContentChildren(new int[]{4}, new int[0]) != 0) throw new AssertionError("no cookies");
        int top = Integer.MAX_VALUE;
        if (findContentChildren(new int[]{top, top}, new int[]{top, top - 1}) != 1) throw new AssertionError("values at the int limit");

        int[] greed = {9, 1, 5};
        int[] sizes = {6, 2, 8};
        findContentChildren(greed, sizes);
        if (!Arrays.equals(greed, new int[]{9, 1, 5}) || !Arrays.equals(sizes, new int[]{6, 2, 8})) throw new AssertionError("caller arrays were reordered");

        Random rnd = new Random(2002);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(8), m = rnd.nextInt(8);
            int[] g = new int[n], s = new int[m];
            for (int i = 0; i < n; i++) g[i] = 1 + rnd.nextInt(7);
            for (int i = 0; i < m; i++) s[i] = 1 + rnd.nextInt(7);
            if (findContentChildren(g, s) != oracle(g, s, 0, new boolean[m])) throw new AssertionError("disagrees on " + Arrays.toString(g) + " " + Arrays.toString(s));
        }
    }
}
```

#### Solution: [Boundary] Unusable Resources (Author exercise)
<!-- id: gr-unusable-resources -->

**Approach.** Run the same two cursors and add one counter. When the current room is at least as large as the waiting party, both cursors move. When it is smaller, only the room cursor moves and the discard counter grows. The loop ends when the parties run out or the rooms run out, so rooms left unexamined are never counted. The assertions check both examples, a case with no waiting parties where nothing is discarded, and random inputs, comparing the served count with the exhaustive best and the discard count with a queue-based replay of the same rule.

**Complexity.** The pass itself is linear in n + m after two sorts, giving O(n log n + m log m) overall.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class UnusableResources {
    static int[] run(int[] need, int[] beds) {
        int[] g = need.clone(), r = beds.clone();
        Arrays.sort(g);
        Arrays.sort(r);
        int served = 0, discarded = 0, room = 0;
        while (room < r.length && served < g.length) {
            if (r[room] >= g[served]) served++;
            else discarded++;
            room++;
        }
        return new int[]{served, discarded};
    }

    static int[] replay(int[] need, int[] beds) {
        int[] g = need.clone(), r = beds.clone();
        Arrays.sort(g);
        Arrays.sort(r);
        ArrayDeque<Integer> waiting = new ArrayDeque<>();
        for (int v : g) waiting.addLast(v);
        int discarded = 0, served = 0;
        for (int cap : r) {
            if (waiting.isEmpty()) break;
            if (cap >= waiting.peekFirst()) { waiting.pollFirst(); served++; }
            else discarded++;
        }
        return new int[]{served, discarded};
    }

    static int bestHoused(int[] need, int[] beds, int g, boolean[] taken) {
        if (g == need.length) return 0;
        int best = bestHoused(need, beds, g + 1, taken);
        for (int r = 0; r < beds.length; r++) {
            if (!taken[r] && beds[r] >= need[g]) {
                taken[r] = true;
                best = Math.max(best, 1 + bestHoused(need, beds, g + 1, taken));
                taken[r] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[]{4, 4}, new int[]{1, 2, 3}), new int[]{0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[]{2, 6}, new int[]{Integer.MAX_VALUE, 2, 1}), new int[]{2, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(run(new int[0], new int[]{1, 2}), new int[]{0, 0})) throw new AssertionError("no waiting parties");
        if (!Arrays.equals(run(new int[]{3}, new int[]{1, 1, 1, 5, 9, 9}), new int[]{1, 3})) throw new AssertionError("later rooms are not examined");

        Random rnd = new Random(2003);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(7), m = rnd.nextInt(8);
            int[] need = new int[n], beds = new int[m];
            for (int i = 0; i < n; i++) need[i] = 1 + rnd.nextInt(6);
            for (int i = 0; i < m; i++) beds[i] = 1 + rnd.nextInt(6);
            int[] got = run(need, beds);
            if (got[0] != bestHoused(need, beds, 0, new boolean[m])) throw new AssertionError("served count wrong on " + Arrays.toString(need) + " " + Arrays.toString(beds));
            if (!Arrays.equals(got, replay(need, beds))) throw new AssertionError("discard count differs from the replay");
        }
    }
}
```

#### Solution: [Recognize] Lemonade Change (LeetCode 860)
<!-- id: gr-lemonade-change -->

**Approach.** Keep a count of fives and a count of tens. A five is simply kept. A ten needs one five. A twenty needs fifteen, and the only ways are a ten with a five or three fives. Prefer the ten, because a ten is useful only for twenties while a five is useful for every later customer, so the choice that keeps more fives dominates. The assertions check both examples, then compare with a depth-first search that tries both ways to change a twenty on random queues. They also find a queue where the fives-first variant fails and the ten-first rule succeeds, which shows that the preference is not a matter of taste.

**Complexity.** One pass with constant work per customer gives O(n) time and O(1) memory, while the oracle is exponential in the number of twenties.

```java run
import java.util.Random;

public final class LemonadeChange {
    static boolean tenFirst(int[] bills) {
        int fives = 0, tens = 0;
        for (int bill : bills) {
            if (bill == 5) fives++;
            else if (bill == 10) { if (fives == 0) return false; fives--; tens++; }
            else if (tens > 0 && fives > 0) { tens--; fives--; }
            else if (fives >= 3) fives -= 3;
            else return false;
        }
        return true;
    }

    static boolean fivesFirst(int[] bills) {
        int fives = 0, tens = 0;
        for (int bill : bills) {
            if (bill == 5) fives++;
            else if (bill == 10) { if (fives == 0) return false; fives--; tens++; }
            else if (fives >= 3) fives -= 3;
            else if (tens > 0 && fives > 0) { tens--; fives--; }
            else return false;
        }
        return true;
    }

    static boolean search(int[] bills, int i, int fives, int tens) {
        if (i == bills.length) return true;
        int b = bills[i];
        if (b == 5) return search(bills, i + 1, fives + 1, tens);
        if (b == 10) return fives > 0 && search(bills, i + 1, fives - 1, tens + 1);
        if (tens > 0 && fives > 0 && search(bills, i + 1, fives - 1, tens - 1)) return true;
        return fives >= 3 && search(bills, i + 1, fives - 3, tens);
    }

    public static void main(String[] args) {
        if (!tenFirst(new int[]{5, 5, 10, 5, 20, 10, 5, 20})) throw new AssertionError("example 1");
        if (tenFirst(new int[]{5, 10, 10, 20})) throw new AssertionError("example 2");
        if (!tenFirst(new int[0])) throw new AssertionError("an empty queue is served");
        if (tenFirst(new int[]{10})) throw new AssertionError("a first ten has no change");
        if (tenFirst(new int[]{5, 5, 20})) throw new AssertionError("two fives are not fifteen");

        Random rnd = new Random(2004);
        int[] kinds = {5, 10, 20};
        boolean separated = false;
        for (int t = 0; t < 20000; t++) {
            int n = rnd.nextInt(13);
            int[] bills = new int[n];
            for (int i = 0; i < n; i++) bills[i] = (rnd.nextInt(10) < 5) ? 5 : kinds[rnd.nextInt(3)];
            boolean expected = search(bills, 0, 0, 0);
            if (tenFirst(bills) != expected) throw new AssertionError("ten-first disagrees with the search");
            if (fivesFirst(bills) && !expected) throw new AssertionError("fives-first accepted an impossible queue");
            if (expected && !fivesFirst(bills)) separated = true;
        }
        if (!separated) throw new AssertionError("expected a queue that only the ten-first rule serves");
    }
}
```
