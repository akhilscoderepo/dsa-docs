<!-- solutions-for: 01-local-choice -->
### Solutions For Local Choice

#### Solution: [Build] Smallest Sufficient Match (Author exercise)
<!-- id: gr-smallest-sufficient-match -->

**Approach.**
The method walks the supplies once with the pointer `j` and keeps a pointer `i` to the smallest unserved demand. A supply that meets the demand serves it, and `i` advances. A smaller supply is useless for this demand and for every later demand, so the walk discards it. The swap argument of the lesson shows that serving the smallest demand with the smallest sufficient supply never lowers the best count.

After each step, `i` demands are served and a best completion exists for the rest.

**Complexity.**
- **Time** is O(n + m), because each step advances `j` once and `i` at most once.
- **Space** is O(1), because the method keeps two integers.

```java run
import java.util.*;

public final class SmallestSufficientMatch {
    /**
     * Returns the largest number of served demands for sorted inputs.
     * Time: O(n + m). Space: O(1).
     * Invariant: the first i demands are served by supplies before index j, and a best completion exists.
     */
    static int serve(int[] demands, int[] supplies) {
        int i = 0;                                                  // smallest demand not yet served
        for (int j = 0; j < supplies.length && i < demands.length; j++) { // one step per supply
            if (supplies[j] >= demands[i]) i++;                     // sufficient supply serves the demand
        }
        return i;                                                   // number of served demands
    }

    static int brute(int[] d, int[] s, int di, boolean[] used) {
        if (di == d.length) return 0;
        int best = brute(d, s, di + 1, used);                       // skip this demand
        for (int k = 0; k < s.length; k++) {
            if (!used[k] && s[k] >= d[di]) {
                used[k] = true;
                best = Math.max(best, 1 + brute(d, s, di + 1, used));
                used[k] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (serve(new int[] {3, 8}, new int[] {4, 9}) != 2) throw new AssertionError("ex1");
        if (serve(new int[] {5, 6}, new int[] {1, 2, 5, 7}) != 2) throw new AssertionError("ex2");
        // Empty sides serve nothing.
        if (serve(new int[0], new int[] {1}) != 0 || serve(new int[] {1}, new int[0]) != 0) throw new AssertionError("empty");
        // Random sorted inputs must match exhaustive assignment.
        Random rnd = new Random(2001);
        for (int t = 0; t < 400; t++) {
            int[] d = new int[rnd.nextInt(6)], s = new int[rnd.nextInt(6)];
            for (int k = 0; k < d.length; k++) d[k] = 1 + rnd.nextInt(8);
            for (int k = 0; k < s.length; k++) s[k] = 1 + rnd.nextInt(8);
            Arrays.sort(d); Arrays.sort(s);
            if (serve(d, s) != brute(d, s, 0, new boolean[s.length])) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Assign Cookies (LeetCode 455)
<!-- id: gr-assign-cookies -->

**Approach.**
The method sorts both arrays in increasing order and then repeats the smallest-first pass. Sorting is the only new step, and it makes the smallest remaining child and the smallest remaining cookie visible at the front. The exchange argument needs that order, because it compares the chosen cookie with every larger one. The method sorts the arrays in place, which the constraints allow.

Before each step, the children before `i` hold the cookies before `j`, and no better split exists.

**Complexity.**
- **Time** is O(n log n + m log m) for the sorts, plus O(n + m) for the pass.
- **Space** is O(1) extra besides the sort buffer of `Arrays.sort`.

```java run
import java.util.*;

public final class AssignCookies {
    /**
     * Returns the largest number of satisfied children.
     * Time: O(n log n + m log m). Space: O(1) extra beyond the sort.
     * Invariant: children before i are satisfied by cookies before j, and a best completion exists.
     */
    static int findContentChildren(int[] g, int[] s) {
        Arrays.sort(g);                                             // smallest greed first
        Arrays.sort(s);                                             // smallest cookie first
        int i = 0;                                                  // smallest unsatisfied child
        for (int j = 0; j < s.length && i < g.length; j++) {        // one step per cookie
            if (s[j] >= g[i]) i++;                                  // cookie satisfies child i
        }
        return i;                                                   // satisfied children
    }

    static int brute(int[] g, int[] s, int gi, boolean[] used) {
        if (gi == g.length) return 0;
        int best = brute(g, s, gi + 1, used);
        for (int k = 0; k < s.length; k++) {
            if (!used[k] && s[k] >= g[gi]) {
                used[k] = true;
                best = Math.max(best, 1 + brute(g, s, gi + 1, used));
                used[k] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (findContentChildren(new int[] {1, 2, 3}, new int[] {1, 1}) != 1) throw new AssertionError("ex1");
        if (findContentChildren(new int[] {10, 9, 8, 7}, new int[] {5, 6, 7, 8}) != 2) throw new AssertionError("ex2");
        // Values at the int maximum compare without overflow.
        if (findContentChildren(new int[] {Integer.MAX_VALUE}, new int[] {Integer.MAX_VALUE}) != 1) throw new AssertionError("max");
        // Random unsorted inputs must match exhaustive assignment.
        Random rnd = new Random(2002);
        for (int t = 0; t < 400; t++) {
            int[] g = new int[rnd.nextInt(6)], s = new int[rnd.nextInt(6)];
            for (int k = 0; k < g.length; k++) g[k] = 1 + rnd.nextInt(8);
            for (int k = 0; k < s.length; k++) s[k] = 1 + rnd.nextInt(8);
            int expect = brute(g, s, 0, new boolean[s.length]);
            if (findContentChildren(g, s) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Unusable Resources (Author exercise)
<!-- id: gr-unusable-resources -->

**Approach.**
The method runs the same pointer pass and counts a discard whenever the current supply is smaller than the smallest remaining demand. A discarded supply is smaller than every remaining demand, because the demands are sorted, so the discard is final. The pass stops when the demands run out or the supplies run out. Supplies that the pass never reads are not counted, which is the boundary case: with a single demand that no supply meets, every supply is read and discarded.

After each step, `discarded` equals the number of supplies before `j` that served no demand.

**Complexity.**
- **Time** is O(n + m), because each step advances `j` once.
- **Space** is O(1), because the method keeps three integers.

```java run
import java.util.*;

public final class UnusableResources {
    /**
     * Returns the number of supplies the smallest-first pass discards.
     * Time: O(n + m). Space: O(1).
     * Invariant: discarded counts supplies before j that are smaller than the demand at i at the time of reading.
     */
    static int discarded(int[] demands, int[] supplies) {
        int i = 0, discarded = 0;                                   // served demands and discards
        for (int j = 0; j < supplies.length && i < demands.length; j++) { // stop when demands run out
            if (supplies[j] >= demands[i]) i++;                     // supply serves the demand
            else discarded++;                                       // supply is too small for every remaining demand
        }
        return discarded;                                           // unread supplies are not counted
    }

    static int model(int[] d, int[] s) {
        int served = 0, count = 0, j = 0;
        while (served < d.length && j < s.length) {
            while (j < s.length && s[j] < d[served]) { count++; j++; }
            if (j < s.length) { served++; j++; }
        }
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (discarded(new int[] {5, 6}, new int[] {1, 2, 5, 7}) != 2) throw new AssertionError("ex1");
        if (discarded(new int[] {4}, new int[] {1, 2, 3}) != 3) throw new AssertionError("ex2");
        // Empty inputs return 0, and unread supplies are not counted.
        if (discarded(new int[0], new int[] {1}) != 0 || discarded(new int[] {1}, new int[] {1, 0}) != 0) throw new AssertionError("empty");
        // Random sorted inputs must match a nested-loop model.
        Random rnd = new Random(2003);
        for (int t = 0; t < 400; t++) {
            int[] d = new int[rnd.nextInt(6)], s = new int[rnd.nextInt(7)];
            for (int k = 0; k < d.length; k++) d[k] = 1 + rnd.nextInt(8);
            for (int k = 0; k < s.length; k++) s[k] = 1 + rnd.nextInt(8);
            Arrays.sort(d); Arrays.sort(s);
            if (discarded(d, s) != model(d, s)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Lemonade Change (LeetCode 860)
<!-- id: gr-lemonade-change -->

**Approach.**
The method counts the 5 bills and the 10 bills in hand. A 5 needs no change. A 10 needs one 5. A 20 needs 15, which the stand pays with a 10 and a 5 when it has both, and with three 5 bills otherwise. A 10 can pay only a 20, and a 5 can pay a 10 or a 20, so the 10 is the less flexible bill. Spending the 10 first keeps the more flexible 5 bills. An exchange argument confirms this: any plan that spends three 5 bills while a 10 is available can swap one 10 and one 5 for them and keep more 5 bills.

After each customer, the counts of 5 and 10 bills match a plan that keeps a best completion.

**Complexity.**
- **Time** is O(n), because each payment takes constant work.
- **Space** is O(1), because the method keeps two counters.

```java run
import java.util.*;

public final class LemonadeChange {
    /**
     * Returns true when every customer receives exact change.
     * Time: O(n). Space: O(1).
     * Invariant: fives and tens hold the bills in hand, and tens are spent before fives.
     */
    static boolean lemonadeChange(int[] bills) {
        int fives = 0, tens = 0;                                    // bills in hand
        for (int b : bills) {                                       // one customer per step
            if (b == 5) fives++;                                    // no change needed
            else if (b == 10) {                                     // change is one five
                if (fives == 0) return false;
                fives--; tens++;
            } else {                                                // change is 15
                if (tens > 0 && fives > 0) { tens--; fives--; }     // spend the less flexible ten first
                else if (fives >= 3) fives -= 3;                    // otherwise three fives
                else return false;
            }
        }
        return true;                                                // every customer was paid correctly
    }

    static boolean brute(int[] bills, int i, int fives, int tens) {
        if (i == bills.length) return true;
        int b = bills[i];
        if (b == 5) return brute(bills, i + 1, fives + 1, tens);
        if (b == 10) return fives > 0 && brute(bills, i + 1, fives - 1, tens + 1);
        if (tens > 0 && fives > 0 && brute(bills, i + 1, fives - 1, tens - 1)) return true;
        return fives >= 3 && brute(bills, i + 1, fives - 3, tens);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!lemonadeChange(new int[] {5, 5, 5, 10, 20})) throw new AssertionError("ex1");
        if (lemonadeChange(new int[] {10, 10})) throw new AssertionError("ex2");
        // The hostile case: the ten must go first.
        if (!lemonadeChange(new int[] {5, 5, 10, 5, 20})) throw new AssertionError("ten first");
        if (!lemonadeChange(new int[0])) throw new AssertionError("empty");
        // Random sequences must match exhaustive choice of change.
        Random rnd = new Random(2004);
        int[] kinds = {5, 10, 20};
        for (int t = 0; t < 600; t++) {
            int[] b = new int[rnd.nextInt(9)];
            for (int k = 0; k < b.length; k++) b[k] = kinds[rnd.nextInt(3)];
            if (lemonadeChange(b) != brute(b, 0, 0, 0)) throw new AssertionError("random " + t);
        }
    }
}
```
