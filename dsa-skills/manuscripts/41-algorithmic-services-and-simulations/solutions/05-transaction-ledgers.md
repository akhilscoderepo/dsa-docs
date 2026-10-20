<!-- solutions-for: 05-transaction-ledgers -->
### Solutions For Transaction Ledgers

#### Solution: [Build] Simple Bank System (LeetCode 2043)
<!-- id: sv-bank-transfer -->

**Approach.** A `long` array holds the balances, and account `i` lives at index `i - 1`. A helper tests whether an account number lies in the range 1 to the array length. The transfer call tests both account numbers and then tests that the source balance covers the amount. Only after those tests does it subtract from the source and add to the destination. Deposit and withdraw follow the same shape with one account.

The invariant is that every balance write sits after the last test of its call. A refused call therefore changes no balance, and the sum of all balances changes only through deposit and withdraw.

**Complexity.**

- **Time** is O(1) per call, since a call does a fixed number of array reads and writes.
- **Space** is O(n) for n accounts, because the array holds one balance per account.

```java run
import java.util.*;

public final class BankTransferSolution {
    static final class Bank {
        private final long[] balance;

        Bank(long[] start) { balance = start.clone(); }

        private boolean exists(int account) { return account >= 1 && account <= balance.length; }

        /**
         * Moves money between two accounts, or changes nothing.
         * Time: O(1).
         * Space: O(1).
         * Invariant: both writes run only after every test has passed.
         */
        boolean transfer(int from, int to, long money) {
            // Unknown accounts are refused before any read of a balance.
            if (!exists(from) || !exists(to)) return false;
            // An overdraft is refused before any write.
            if (balance[from - 1] < money) return false;
            // The commit cannot fail; a self transfer nets to zero.
            balance[from - 1] -= money;
            balance[to - 1] += money;
            return true;
        }

        /** Adds money to a known account; O(1) time and space; invariant: unknown accounts stay unwritten. */
        boolean deposit(int account, long money) {
            // The only refusal is an unknown account.
            if (!exists(account)) return false;
            balance[account - 1] += money;
            return true;
        }

        /** Removes money from a known account that covers it; O(1) time and space; invariant: balances never go below zero. */
        boolean withdraw(int account, long money) {
            // Both refusals are tested before the single write.
            if (!exists(account) || balance[account - 1] < money) return false;
            balance[account - 1] -= money;
            return true;
        }

        long balance(int account) { return balance[account - 1]; }
    }

    /** Oracle: applies the call to a copy, and keeps the copy only when no balance went negative. */
    static final class Oracle {
        long[] b;
        Oracle(long[] s) { b = s.clone(); }
        boolean apply(int kind, int x, int y, long m) {
            long[] c = b.clone();
            int n = c.length;
            if (kind == 0) {
                if (x < 1 || x > n || y < 1 || y > n) return false;
                c[x - 1] -= m;
                if (c[x - 1] < 0) return false;
                c[y - 1] += m;
            } else if (kind == 1) {
                if (x < 1 || x > n) return false;
                c[x - 1] += m;
            } else {
                if (x < 1 || x > n) return false;
                c[x - 1] -= m;
            }
            for (long v : c) if (v < 0) return false;
            b = c;
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Bank e = new Bank(new long[] {10, 100, 20, 50, 50});
        if (!e.transfer(5, 1, 20)) throw new AssertionError("e1 a");
        if (e.transfer(3, 4, 25)) throw new AssertionError("e1 b");
        if (!e.withdraw(3, 20)) throw new AssertionError("e1 c");
        if (e.balance(1) != 30 || e.balance(3) != 0) throw new AssertionError("e1 balances");
        Bank f = new Bank(new long[] {10, 100, 20, 50, 50});
        if (f.transfer(2, 6, 5) || f.deposit(0, 5)) throw new AssertionError("e2 refusals");
        if (!f.transfer(2, 2, 100) || f.balance(2) != 100) throw new AssertionError("e2 self transfer");
        // A refused transfer must leave every balance as it was.
        Bank g = new Bank(new long[] {10, 100, 20});
        if (g.transfer(2, 9, 40) || g.balance(2) != 100) throw new AssertionError("refusal changed state");
        // Random calls against the copy-and-discard oracle, with total conservation for transfers.
        Random rnd = new Random(2043);
        for (int round = 0; round < 400; round++) {
            int n = 1 + rnd.nextInt(5);
            long[] start = new long[n];
            for (int i = 0; i < n; i++) start[i] = rnd.nextInt(30);
            Bank s = new Bank(start);
            Oracle o = new Oracle(start);
            for (int op = 0; op < 60; op++) {
                int kind = rnd.nextInt(3);
                int x = rnd.nextInt(n + 3) - 1, y = rnd.nextInt(n + 3) - 1;
                long m = rnd.nextInt(40);
                long before = 0;
                for (int i = 1; i <= n; i++) before += s.balance(i);
                boolean got = kind == 0 ? s.transfer(x, y, m) : kind == 1 ? s.deposit(x, m) : s.withdraw(x, m);
                boolean want = o.apply(kind, x, y, m);
                if (got != want) throw new AssertionError("verdict " + kind);
                long after = 0;
                for (int i = 1; i <= n; i++) {
                    if (s.balance(i) != o.b[i - 1]) throw new AssertionError("balance drift");
                    after += s.balance(i);
                }
                if (kind == 0 && before != after) throw new AssertionError("transfer changed the total");
            }
        }
    }
}
```

#### Solution: [Vary] Design Underground System (LeetCode 1396)
<!-- id: sv-route-statistics -->

**Approach.** A hash map from rider id to an immutable open-trip record holds the authoritative active state. A second hash map from route to an immutable statistics record holds the derived totals: duration sum, trip count and maximum. A route key is a record of the two station names, so two routes never collide.

Check-in tests that the id is absent from the active map and then stores the trip. Check-out reads the open trip first and refuses when it is missing or when the time is earlier than the check-in time. Only then does it remove the trip and replace the route statistics with a merged record. A refused check-out leaves the trip open, so the rider can check out again with a valid time.

The invariant is that the statistics of each route equal the sum over all closed trips of that route, and each rider id appears in the active map at most once. Both facts hold because one block removes the open trip and updates the statistics together.

**Complexity.**

- **Time** is O(1) expected per call, because each call does a fixed number of hash-map operations.
- **Space** is O(a + r), where a is the number of open trips and r is the number of routes with at least one closed trip.

```java run
import java.util.*;

public final class RouteStatisticsSolution {
    static final class Metro {
        private record Open(String station, long time) {}
        private record Route(String from, String to) {}
        private record Stat(long total, long count, long max) {}
        private final Map<Integer, Open> active = new HashMap<>();   // authoritative open trips
        private final Map<Route, Stat> stats = new HashMap<>();      // derived route totals

        /**
         * Opens a trip unless the rider already has one.
         * Time: O(1) expected.
         * Space: O(1) per open trip.
         * Invariant: a rider id appears in the active map at most once.
         */
        boolean checkIn(int id, String station, long t) {
            // An id that is already open is refused before any write.
            if (active.containsKey(id)) return false;
            active.put(id, new Open(station, t));
            return true;
        }

        /**
         * Closes the open trip of a rider and merges its duration into the route.
         * Time: O(1) expected.
         * Space: O(1) per route.
         * Invariant: the trip leaves the active map in the same block that updates the route.
         */
        boolean checkOut(int id, String station, long t) {
            Open trip = active.get(id);
            // A missing trip and an earlier time are both refused before any write.
            if (trip == null || t < trip.time()) return false;
            long d = t - trip.time();
            // The commit removes the trip and replaces the immutable statistics record.
            active.remove(id);
            stats.merge(new Route(trip.station(), station), new Stat(d, 1, d),
                (a, b) -> new Stat(a.total() + b.total(), a.count() + b.count(), Math.max(a.max(), b.max())));
            return true;
        }

        /** Returns the rounded-down average duration of a route, or -1; O(1) expected time and space. */
        long getAverage(String start, String end) {
            Stat s = stats.get(new Route(start, end));
            // An unknown route has no trips, so it reports -1.
            return s == null ? -1 : s.total() / s.count();
        }

        /** Returns the longest duration of a route, or -1; O(1) expected time and space. */
        long maxTrip(String start, String end) {
            Stat s = stats.get(new Route(start, end));
            return s == null ? -1 : s.max();
        }
    }

    /** Oracle: keeps every closed trip in a list and scans the list for each query. */
    static final class Oracle {
        final List<int[]> open = new ArrayList<>();            // {id, stationIndex, time}
        final List<long[]> done = new ArrayList<>();           // {from, to, duration}
        boolean in(int id, int st, long t) {
            for (int[] o : open) if (o[0] == id) return false;
            open.add(new int[] {id, st, (int) t});
            return true;
        }
        boolean out(int id, int st, long t) {
            for (int i = 0; i < open.size(); i++) {
                int[] o = open.get(i);
                if (o[0] != id) continue;
                if (t < o[2]) return false;
                done.add(new long[] {o[1], st, t - o[2]});
                open.remove(i);
                return true;
            }
            return false;
        }
        long avg(int a, int b) {
            long sum = 0, cnt = 0;
            for (long[] d : done) if (d[0] == a && d[1] == b) { sum += d[2]; cnt++; }
            return cnt == 0 ? -1 : sum / cnt;
        }
        long max(int a, int b) {
            long best = -1;
            for (long[] d : done) if (d[0] == a && d[1] == b) best = Math.max(best, d[2]);
            return best;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Metro m = new Metro();
        boolean[] r1 = {m.checkIn(1, "a", 3), m.checkIn(1, "b", 5), m.checkIn(2, "a", 4), m.checkOut(1, "b", 10), m.checkOut(2, "b", 12)};
        if (!Arrays.equals(r1, new boolean[] {true, false, true, true, true})) throw new AssertionError("e1 verdicts");
        if (m.getAverage("a", "b") != 7 || m.maxTrip("a", "b") != 8) throw new AssertionError("e1 stats");
        // Example 2 from the problem text.
        Metro n = new Metro();
        boolean[] r2 = {n.checkIn(4, "c", 10), n.checkOut(4, "a", 9), n.checkOut(4, "a", 15), n.checkOut(4, "a", 16)};
        if (!Arrays.equals(r2, new boolean[] {true, false, true, false})) throw new AssertionError("e2 verdicts");
        if (n.getAverage("c", "a") != 5 || n.getAverage("a", "c") != -1) throw new AssertionError("e2 stats");
        // A refused check-out keeps the trip open, so a later valid check-out succeeds.
        Metro k = new Metro();
        k.checkIn(1, "x", 10);
        if (k.checkOut(1, "y", 5) || !k.checkOut(1, "y", 12) || k.getAverage("x", "y") != 2) throw new AssertionError("open trip lost");
        // Random calls against the list-scanning oracle, including early check-outs and repeated ids.
        Random rnd = new Random(1396);
        String[] names = {"a", "b", "c"};
        for (int round = 0; round < 400; round++) {
            Metro s = new Metro();
            Oracle o = new Oracle();
            for (int op = 0; op < 80; op++) {
                int id = 1 + rnd.nextInt(4), st = rnd.nextInt(3);
                long t = rnd.nextInt(30);
                int kind = rnd.nextInt(4);
                if (kind == 0) { if (s.checkIn(id, names[st], t) != o.in(id, st, t)) throw new AssertionError("checkIn"); }
                else if (kind == 1) { if (s.checkOut(id, names[st], t) != o.out(id, st, t)) throw new AssertionError("checkOut"); }
                else {
                    int a = rnd.nextInt(3), b = rnd.nextInt(3);
                    if (s.getAverage(names[a], names[b]) != o.avg(a, b)) throw new AssertionError("average");
                    if (s.maxTrip(names[a], names[b]) != o.max(a, b)) throw new AssertionError("max");
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Duplicate Active Transaction (Author exercise)
<!-- id: sv-duplicate-active -->

**Approach.** The balance array and a hash map from transaction id to an immutable reservation hold the authoritative state. A second `long` array stores the held total per account as a derived summary, so `available` is a subtraction. Authorize tests the id against the active map first, then the account range, then the available amount. Only then does it store the reservation and raise the held total.

Settle and release read the reservation first and refuse an id that is not active. Settle lowers the balance and the held total by the amount, and release lowers only the held total. Both remove the map entry in the same block. Because the entry leaves the map, the same id can start again later. While the entry stays in the map, even a request for a different account is refused.

The invariant is that the held total of each account equals the sum of its active reservations, and available never goes below zero.

**Complexity.**

- **Time** is O(1) expected per call, because each call does a fixed number of hash-map and array operations.
- **Space** is O(n + a) for n accounts and a active reservations.

```java run
import java.util.*;

public final class DuplicateActiveSolution {
    static final class Holds {
        private record Hold(int account, long amount) {}
        private final long[] balance;                          // authoritative balances
        private final long[] held;                             // derived total of active holds per account
        private final Map<Integer, Hold> active = new HashMap<>();   // authoritative active reservations

        Holds(long[] start) {
            balance = start.clone();
            held = new long[start.length];
        }

        /**
         * Reserves an amount unless the id is active, the account is unknown or funds are short.
         * Time: O(1) expected.
         * Space: O(1) per reservation.
         * Invariant: held[a] equals the sum of the active holds of account a.
         */
        boolean authorize(int txId, int account, long amount) {
            // A reused active id is refused first, whatever its account.
            if (active.containsKey(txId)) return false;
            // An unknown account is refused before any array read.
            if (account < 1 || account > balance.length) return false;
            // An amount above the available funds is refused before any write.
            if (balance[account - 1] - held[account - 1] < amount) return false;
            // The commit writes the entry and the summary together.
            active.put(txId, new Hold(account, amount));
            held[account - 1] += amount;
            return true;
        }

        /** Finalizes a reservation and lowers the balance; O(1) expected time and space; invariant: entry, hold and balance move together. */
        boolean settle(int txId) {
            Hold h = active.get(txId);
            // An id that is not active is refused.
            if (h == null) return false;
            active.remove(txId);
            held[h.account() - 1] -= h.amount();
            balance[h.account() - 1] -= h.amount();
            return true;
        }

        /** Cancels a reservation and keeps the balance; O(1) expected time and space; invariant: entry and hold leave together. */
        boolean release(int txId) {
            Hold h = active.get(txId);
            if (h == null) return false;
            active.remove(txId);
            held[h.account() - 1] -= h.amount();
            return true;
        }

        long available(int account) { return balance[account - 1] - held[account - 1]; }
    }

    /** Oracle: stores reservations in a list and recomputes the available amount by scanning it. */
    static final class Oracle {
        final long[] bal;
        final List<long[]> list = new ArrayList<>();   // {txId, account, amount}
        Oracle(long[] s) { bal = s.clone(); }
        long avail(int a) {
            long v = bal[a - 1];
            for (long[] h : list) if (h[1] == a) v -= h[2];
            return v;
        }
        boolean authorize(int tx, int a, long amt) {
            for (long[] h : list) if (h[0] == tx) return false;
            if (a < 1 || a > bal.length) return false;
            if (avail(a) < amt) return false;
            list.add(new long[] {tx, a, amt});
            return true;
        }
        boolean end(int tx, boolean pay) {
            for (int i = 0; i < list.size(); i++) {
                if (list.get(i)[0] != tx) continue;
                long[] h = list.remove(i);
                if (pay) bal[(int) h[1] - 1] -= h[2];
                return true;
            }
            return false;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Holds h = new Holds(new long[] {100, 50});
        boolean[] r1 = {h.authorize(7, 1, 60), h.authorize(7, 2, 10), h.authorize(8, 1, 50)};
        if (!Arrays.equals(r1, new boolean[] {true, false, false}) || h.available(1) != 40) throw new AssertionError("e1 first part");
        if (!h.settle(7) || !h.authorize(7, 2, 10) || h.available(2) != 40) throw new AssertionError("e1 reuse after settle");
        // Example 2 from the problem text.
        Holds g = new Holds(new long[] {100, 50});
        if (!g.authorize(1, 2, 50) || !g.release(1) || g.release(1)) throw new AssertionError("e2 release");
        if (g.available(2) != 50 || g.authorize(1, 3, 5)) throw new AssertionError("e2 tail");
        // A refused duplicate leaves the first reservation in place.
        Holds d = new Holds(new long[] {100});
        d.authorize(5, 1, 30);
        if (d.authorize(5, 1, 10) || d.available(1) != 70) throw new AssertionError("duplicate changed state");
        // Random calls against the list-scanning oracle.
        Random rnd = new Random(7043);
        for (int round = 0; round < 400; round++) {
            int n = 1 + rnd.nextInt(3);
            long[] start = new long[n];
            for (int i = 0; i < n; i++) start[i] = rnd.nextInt(60);
            Holds s = new Holds(start);
            Oracle o = new Oracle(start);
            for (int op = 0; op < 70; op++) {
                int kind = rnd.nextInt(3), tx = 1 + rnd.nextInt(5);
                boolean got, want;
                if (kind == 0) {
                    int a = rnd.nextInt(n + 2);
                    long amt = 1 + rnd.nextInt(40);
                    got = s.authorize(tx, a, amt);
                    want = o.authorize(tx, a, amt);
                } else {
                    got = kind == 1 ? s.settle(tx) : s.release(tx);
                    want = o.end(tx, kind == 1);
                }
                if (got != want) throw new AssertionError("verdict " + kind);
                for (int a = 1; a <= n; a++) if (s.available(a) != o.avail(a)) throw new AssertionError("available drift");
            }
        }
    }
}
```

#### Solution: [Recognize] Apply Discount Every n Orders (LeetCode 1357)
<!-- id: sv-cashier-discount -->

**Approach.** A hash map from product id to price is the catalog, and one integer counts the orders served so far. The bill call walks the lines and adds `price * amount` into a local `long`. An id missing from the catalog ends the call with -1 before the counter moves. After the loop the counter increases by one, and when it is a multiple of n the local total is replaced by the discounted total in integer arithmetic.

Invariant: the counter equals the number of calls that returned a bill, so a refused order cannot move the position of the discount. The counter is the only state a call writes, and the write sits after the last test.

**Complexity.**

- **Time** is O(L) per call for an order of L lines, because each line costs one hash lookup.
- **Space** is O(P) for P catalog products, plus O(1) for the counter.

```java run
import java.math.BigInteger;
import java.util.*;

public final class CashierDiscountSolution {
    static final class Cashier {
        private final int n, discount;
        private final Map<Integer, Integer> price = new HashMap<>();   // authoritative catalog
        private int served;                                            // derived count of billed orders

        Cashier(int n, int discount, int[] products, int[] prices) {
            this.n = n;
            this.discount = discount;
            for (int i = 0; i < products.length; i++) price.put(products[i], prices[i]);
        }

        /**
         * Prices one order and applies the discount on every n-th billed order.
         * Time: O(L) for L lines.
         * Space: O(1) beyond the catalog.
         * Invariant: served counts only the orders that returned a bill.
         */
        long getBill(int[] product, int[] amount) {
            long total = 0;
            for (int i = 0; i < product.length; i++) {
                Integer p = price.get(product[i]);
                // An unknown product ends the call before the counter moves.
                if (p == null) return -1;
                total += (long) p * amount[i];
            }
            // The counter moves only for a fully priced order.
            served++;
            // Every n-th billed order is paid at the discounted total, rounded down.
            if (served % n == 0) total = total * (100 - discount) / 100;
            return total;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Cashier a = new Cashier(3, 50, new int[] {1, 2, 3}, new int[] {100, 200, 300});
        long[] r1 = {a.getBill(new int[] {1, 2}, new int[] {1, 1}), a.getBill(new int[] {3}, new int[] {1}), a.getBill(new int[] {1, 1}, new int[] {1, 2})};
        if (!Arrays.equals(r1, new long[] {300, 300, 150})) throw new AssertionError("e1 " + Arrays.toString(r1));
        // Example 2 from the problem text: the refused order is not counted.
        Cashier b = new Cashier(2, 10, new int[] {1}, new int[] {100});
        long[] r2 = {b.getBill(new int[] {1}, new int[] {1}), b.getBill(new int[] {5}, new int[] {1}), b.getBill(new int[] {1}, new int[] {3})};
        if (!Arrays.equals(r2, new long[] {100, -1, 270})) throw new AssertionError("e2 " + Arrays.toString(r2));
        // Random orders against a linear-scan oracle that uses BigInteger and its own counter list.
        Random rnd = new Random(1357);
        for (int round = 0; round < 300; round++) {
            int p = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(4), disc = rnd.nextInt(101);
            int[] ids = new int[p], prices = new int[p];
            for (int i = 0; i < p; i++) { ids[i] = i * 2 + 1; prices[i] = 1 + rnd.nextInt(1000); }
            Cashier s = new Cashier(n, disc, ids, prices);
            List<Long> billed = new ArrayList<>();
            for (int op = 0; op < 40; op++) {
                int lines = 1 + rnd.nextInt(5);
                int[] prod = new int[lines], amt = new int[lines];
                BigInteger sum = BigInteger.ZERO;
                boolean bad = false;
                for (int i = 0; i < lines; i++) {
                    prod[i] = rnd.nextInt(2 * p + 1);
                    amt[i] = 1 + rnd.nextInt(1000);
                    int found = -1;
                    for (int j = 0; j < p; j++) if (ids[j] == prod[i]) found = prices[j];
                    if (found < 0) bad = true; else sum = sum.add(BigInteger.valueOf((long) found * amt[i]));
                }
                long want;
                if (bad) want = -1;
                else {
                    billed.add(0L);
                    want = (billed.size() % n == 0) ? sum.multiply(BigInteger.valueOf(100 - disc)).divide(BigInteger.valueOf(100)).longValueExact() : sum.longValueExact();
                }
                if (s.getBill(prod, amt) != want) throw new AssertionError("bill");
            }
        }
    }
}
```
