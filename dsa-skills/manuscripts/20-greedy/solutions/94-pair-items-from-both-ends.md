<!-- solutions-for: 94-pair-items-from-both-ends -->
### Solutions For Pairing From Both Ends

#### Solution: [Build] Assign Cookies (LeetCode 455)
<!-- id: gr-cookies-with-slack -->

**Approach.**
The method sorts both arrays and moves one pointer into each. When the cookie is smaller than the child's minimum, the cookie is too small for every remaining child, because the minimums only grow, so the method skips the cookie. When the cookie lies inside the child's range, the method matches them and moves both pointers. When the cookie exceeds the range, the cookie is too large for this child, and every later cookie is at least as large, so the child cannot be served and the method skips the child. Each of the three moves discards an item that no remaining partner can use, so no match is lost. The upper bound uses `long`, because `g + slack` can pass the `int` range.

After each step, the matched pairs are valid, and every skipped child and cookie has no partner among the unread items.

**Complexity.**
- **Time** is O(n log n + m log m) for the sorts, and the scan adds O(n + m).
- **Space** is O(1) extra beyond the sorts.

```java run
import java.util.*;

public final class CookiesWithSlack {
    /**
     * Returns the largest number of children served by a cookie in [g, g + slack].
     * Time: O(n log n + m log m). Space: O(1) extra.
     * Invariant: matched pairs are valid, and each skipped item has no partner among the unread items.
     */
    static int serve(int[] g, int[] s, int slack) {
        int[] kids = g.clone(), cookies = s.clone();                   // keep the caller's order
        Arrays.sort(kids);
        Arrays.sort(cookies);
        int i = 0, j = 0, served = 0;
        while (i < kids.length && j < cookies.length) {                // one pointer moves each round
            if (cookies[j] < kids[i]) j++;                             // too small for this and every later child
            else if (cookies[j] <= (long) kids[i] + slack) { served++; i++; j++; } // inside the range
            else i++;                                                  // too large: no later cookie fits this child
        }
        return served;
    }

    static int brute(int[] g, int[] s, int slack, int gi, boolean[] used) {
        if (gi == g.length) return 0;
        int best = brute(g, s, slack, gi + 1, used);
        for (int k = 0; k < s.length; k++) {
            if (!used[k] && s[k] >= g[gi] && s[k] <= (long) g[gi] + slack) {
                used[k] = true;
                best = Math.max(best, 1 + brute(g, s, slack, gi + 1, used));
                used[k] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (serve(new int[] {1, 2, 3}, new int[] {3, 1}, 0) != 2) throw new AssertionError("ex1");
        if (serve(new int[] {2, 5}, new int[] {3, 4, 9}, 2) != 1) throw new AssertionError("ex2");
        // The upper bound passes the int range and stays correct.
        if (serve(new int[] {Integer.MAX_VALUE}, new int[] {Integer.MAX_VALUE}, Integer.MAX_VALUE) != 1) throw new AssertionError("overflow");
        if (serve(new int[0], new int[] {1}, 3) != 0) throw new AssertionError("empty");
        // Random inputs must match exhaustive matching.
        Random rnd = new Random(2101);
        for (int t = 0; t < 600; t++) {
            int[] g = new int[rnd.nextInt(6)], s = new int[rnd.nextInt(6)];
            for (int k = 0; k < g.length; k++) g[k] = 1 + rnd.nextInt(8);
            for (int k = 0; k < s.length; k++) s[k] = 1 + rnd.nextInt(10);
            int slack = rnd.nextInt(4);
            if (serve(g, s, slack) != brute(g, s, slack, 0, new boolean[s.length])) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Boats to Save People (LeetCode 881)
<!-- id: gr-boats-to-save-people -->

**Approach.**
The method sorts the weights and runs the two-end scan. The heaviest remaining person rides in every round. The lightest remaining person joins that boat when their weights fit the limit, and otherwise the heaviest person rides alone. If the heaviest cannot share with the lightest, no one is light enough, so riding alone is forced. If the pair fits, the regrouping argument of the lesson shows that pairing with the lightest never needs more boats.

After each round, every person outside the pointers is placed, and the people between the pointers need as few boats as any plan allows.

**Complexity.**
- **Time** is O(n log n), because the sort costs that much and the scan is linear.
- **Space** is O(1) extra beyond the sort, since the method sorts the input array.

```java run
import java.util.*;

public final class BoatsToSavePeople {
    /**
     * Returns the smallest number of boats for up to two people each.
     * Time: O(n log n). Space: O(1) extra.
     * Invariant: people outside lo..hi are placed, and a best plan exists for the people inside.
     */
    static int boats(int[] people, int limit) {
        Arrays.sort(people);                                           // lightest to heaviest
        int lo = 0, hi = people.length - 1, boats = 0;
        while (lo <= hi) {                                             // one boat per round
            if (lo < hi && (long) people[lo] + people[hi] <= limit) lo++; // the lightest joins the heaviest
            hi--;                                                      // the heaviest is placed either way
            boats++;
        }
        return boats;
    }

    static int brute(int[] p, int limit, boolean[] used) {
        int first = -1;
        for (int i = 0; i < p.length; i++) if (!used[i]) { first = i; break; }
        if (first < 0) return 0;
        used[first] = true;
        int best = 1 + brute(p, limit, used);                          // first person alone
        for (int j = first + 1; j < p.length; j++) {                   // first person with another
            if (!used[j] && p[first] + p[j] <= limit) {
                used[j] = true;
                best = Math.min(best, 1 + brute(p, limit, used));
                used[j] = false;
            }
        }
        used[first] = false;
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (boats(new int[] {4, 4, 2, 2}, 6) != 2) throw new AssertionError("ex1");
        if (boats(new int[] {3, 5, 3, 4}, 5) != 4) throw new AssertionError("ex2");
        if (boats(new int[0], 5) != 0 || boats(new int[] {5}, 5) != 1) throw new AssertionError("edge");
        // Random inputs must match an exhaustive search over pairings.
        Random rnd = new Random(2102);
        for (int t = 0; t < 600; t++) {
            int limit = 3 + rnd.nextInt(8);
            int[] p = new int[rnd.nextInt(8)];
            for (int k = 0; k < p.length; k++) p[k] = 1 + rnd.nextInt(limit);
            int expect = brute(p, limit, new boolean[p.length]);
            if (boats(p.clone(), limit) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Exact Capacity And One Remaining Person (Author exercise)
<!-- id: gr-exact-capacity-single -->

**Approach.**
The method runs the same scan and also counts the boats that carry one person. A pair is feasible when the sum is at most the limit, so a sum equal to the limit is allowed. The sum uses `long`, because two weights up to 2^30 add up to 2^31, which overflows `int`. A boat is single when the pair test fails, and also when `lo == hi`, because one person remains and no partner exists. That last person counts once, since the pointer `hi` moves left and ends the loop.

After each round, `boats` counts the boats opened, and `singles` counts those with one person.

**Complexity.**
- **Time** is O(n log n), where the sort dominates one linear scan.
- **Space** is O(1) extra beyond the sort.

```java run
import java.util.*;

public final class ExactCapacitySingle {
    /**
     * Returns {boats, singles} for the two-end scan.
     * Time: O(n log n). Space: O(1) extra.
     * Invariant: boats and singles count the rounds done, and people outside lo..hi are placed.
     */
    static int[] plan(int[] people, int limit) {
        int[] w = people.clone();
        Arrays.sort(w);
        int lo = 0, hi = w.length - 1, boats = 0, singles = 0;
        while (lo <= hi) {                                             // one boat per round
            if (lo < hi && (long) w[lo] + w[hi] <= limit) lo++;        // equality is feasible
            else singles++;                                            // the heaviest rides alone, or only one remains
            hi--;
            boats++;
        }
        return new int[] {boats, singles};
    }

    static int bruteBoats(int[] p, int limit, boolean[] used) {
        int first = -1;
        for (int i = 0; i < p.length; i++) if (!used[i]) { first = i; break; }
        if (first < 0) return 0;
        used[first] = true;
        int best = 1 + bruteBoats(p, limit, used);
        for (int j = first + 1; j < p.length; j++) {
            if (!used[j] && (long) p[first] + p[j] <= limit) {
                used[j] = true;
                best = Math.min(best, 1 + bruteBoats(p, limit, used));
                used[j] = false;
            }
        }
        used[first] = false;
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(plan(new int[] {2, 2, 3, 5, 5}, 6), new int[] {4, 3})) throw new AssertionError("ex1");
        if (!Arrays.equals(plan(new int[] {3, 3}, 6), new int[] {1, 0})) throw new AssertionError("ex2");
        // Empty input, and weights near 2^30 whose sum passes the int range.
        if (!Arrays.equals(plan(new int[0], 5), new int[] {0, 0})) throw new AssertionError("empty");
        int big = 1 << 30;
        if (!Arrays.equals(plan(new int[] {big, big}, big), new int[] {2, 2}) || !Arrays.equals(plan(new int[] {big - 1, 1}, big), new int[] {1, 0})) throw new AssertionError("big");
        // Random inputs: the boat count must be the optimum, and singles must equal boats minus pairs.
        Random rnd = new Random(2103);
        for (int t = 0; t < 600; t++) {
            int limit = 3 + rnd.nextInt(8);
            int[] p = new int[rnd.nextInt(8)];
            for (int k = 0; k < p.length; k++) p[k] = 1 + rnd.nextInt(limit);
            int[] r = plan(p, limit);
            if (r[0] != bruteBoats(p, limit, new boolean[p.length])) throw new AssertionError("boats " + t);
            if (r[0] * 2 - r[1] != p.length) throw new AssertionError("singles " + t);
        }
    }
}
```

#### Solution: [Recognize] Bag of Tokens (LeetCode 948)
<!-- id: gr-bag-of-tokens -->

**Approach.**
The method sorts the tokens and keeps two pointers. While the cheapest remaining token is affordable, it plays that token face up for one point. When it is not affordable and the score is positive, the method plays the dearest remaining token face down, which costs one point and adds the most power. When neither move works, the method stops. The method tracks the best score seen, because the score drops after a face-down play. Spending the cheapest token gains a point at the least power cost, and selling the dearest token gains the most power for one point, so each move is the best of its kind.

After each move, `best` is the largest score reached so far, and the tokens outside the pointers are played.

**Complexity.**
- **Time** is O(n log n) for sorting, followed by one O(n) pass.
- **Space** is O(1) extra beyond the sort.

```java run
import java.util.*;

public final class BagOfTokens {
    /**
     * Returns the largest score over all play orders.
     * Time: O(n log n). Space: O(1) extra.
     * Invariant: tokens outside lo..hi are played, and best is the largest score reached.
     */
    static int bagOfTokensScore(int[] tokens, int power) {
        int[] t = tokens.clone();
        Arrays.sort(t);
        int lo = 0, hi = t.length - 1, score = 0, best = 0;
        while (lo <= hi) {                                             // one play per round
            if (power >= t[lo]) { power -= t[lo++]; score++; best = Math.max(best, score); } // spend the cheapest
            else if (score > 0) { power += t[hi--]; score--; }         // sell the dearest
            else break;                                                // no move is possible
        }
        return best;
    }

    static int brute(int[] t, int power, int score, boolean[] used) {
        int best = score;
        for (int i = 0; i < t.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            if (power >= t[i]) best = Math.max(best, brute(t, power - t[i], score + 1, used));
            if (score >= 1) best = Math.max(best, brute(t, power + t[i], score - 1, used));
            used[i] = false;
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (bagOfTokensScore(new int[] {40, 60, 90, 150, 400}, 100) != 3) throw new AssertionError("ex1");
        if (bagOfTokensScore(new int[] {200, 300}, 100) != 0) throw new AssertionError("ex2");
        if (bagOfTokensScore(new int[0], 5) != 0 || bagOfTokensScore(new int[] {0}, 0) != 1) throw new AssertionError("edge");
        // Random inputs must match an exhaustive search over play orders.
        Random rnd = new Random(2104);
        for (int t = 0; t < 400; t++) {
            int[] tok = new int[rnd.nextInt(6)];
            for (int k = 0; k < tok.length; k++) tok[k] = rnd.nextInt(9);
            int power = rnd.nextInt(9);
            if (bagOfTokensScore(tok, power) != brute(tok, power, 0, new boolean[tok.length])) throw new AssertionError("random " + t);
        }
    }
}
```
