<!-- solutions-for: 06-transaction-lifecycles -->
### Solutions For Transaction Lifecycles

#### Solution: [Build] Design ATM Machine (LeetCode 2241)
<!-- id: ci40-atm -->

**Approach.** The stock is an array of five `long` counters. A withdraw call builds a plan in a local array. For each value from 500 down to 20, it takes the smaller of the stocked count and the number of whole notes that fit in the remaining amount, then lowers the remaining amount. If the remaining amount is not zero, the call returns `[-1]` without writing the stock. Otherwise it subtracts the plan from the stock and returns the plan.

The invariant is that the stock changes only in the final loop, which runs after every check has passed. A failed call therefore leaves the stock as it was.

**Complexity.**

- **Time** is O(1) per call, because the loops run over five denominations.
- **Space** is O(1), because the stock and the plan hold five numbers each.

```java run
import java.util.*;

public final class AtmSolution {
    static final class Atm {
        private static final int[] VALUE = {20, 50, 100, 200, 500};
        private final long[] stock = new long[5];

        /** Adds banknotes to the stock; O(1) time and space; invariant: every counter stays non-negative. */
        void deposit(int[] counts) {
            for (int i = 0; i < 5; i++) stock[i] += counts[i];
        }

        /**
         * Hands out an amount by the largest-first rule, or changes nothing.
         * Time: O(1).
         * Space: O(1).
         * Invariant: stock changes only after the plan reaches the amount exactly.
         */
        int[] withdraw(int amount) {
            int[] plan = new int[5];
            long left = amount;
            // Phase one reads the stock and writes only the plan.
            for (int i = 4; i >= 0; i--) {
                plan[i] = (int) Math.min(stock[i], left / VALUE[i]);
                left -= (long) plan[i] * VALUE[i];
            }
            // An unpaid remainder means the rule cannot reach the amount.
            if (left != 0) return new int[] {-1};
            // Phase two cannot fail, because each plan count is at most the stock.
            for (int i = 0; i < 5; i++) stock[i] -= plan[i];
            return plan;
        }

        long[] snapshot() { return stock.clone(); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Atm a = new Atm();
        a.deposit(new int[] {3, 2, 0, 1, 0});
        if (!Arrays.equals(a.withdraw(270), new int[] {1, 1, 0, 1, 0})) throw new AssertionError("e1");
        if (!Arrays.equals(a.withdraw(130), new int[] {-1})) throw new AssertionError("e2 failure");
        if (!Arrays.equals(a.snapshot(), new long[] {2, 1, 0, 0, 0})) throw new AssertionError("failure changed the stock");
        if (!Arrays.equals(a.withdraw(90), new int[] {2, 1, 0, 0, 0})) throw new AssertionError("e2 success");
        // Random calls checked against a simulation that copies the stock and discards it on failure.
        Random rnd = new Random(2241);
        int[] val = {20, 50, 100, 200, 500};
        for (int round = 0; round < 300; round++) {
            Atm s = new Atm();
            long[] ref = new long[5];
            for (int op = 0; op < 60; op++) {
                if (rnd.nextInt(3) == 0) {
                    int[] add = new int[5];
                    for (int i = 0; i < 5; i++) { add[i] = rnd.nextInt(4); ref[i] += add[i]; }
                    s.deposit(add);
                } else {
                    int amount = 20 * (1 + rnd.nextInt(40)) + (rnd.nextInt(4) == 0 ? 10 : 0);
                    long[] copy = ref.clone();
                    int[] want = new int[5];
                    int left = amount;
                    for (int i = 4; i >= 0; i--) { want[i] = (int) Math.min(copy[i], left / val[i]); left -= want[i] * val[i]; }
                    int[] got = s.withdraw(amount);
                    if (left != 0) { if (!Arrays.equals(got, new int[] {-1})) throw new AssertionError("expected failure"); }
                    else { for (int i = 0; i < 5; i++) ref[i] -= want[i]; if (!Arrays.equals(got, want)) throw new AssertionError("plan"); }
                    if (!Arrays.equals(s.snapshot(), ref)) throw new AssertionError("stock drift");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Design Order Management System (LeetCode 3822)
<!-- id: ci40-order-management -->

**Approach.** A hash map from order id to an immutable record of customer and state is the source of truth. Two derived views depend on it: a tree set of ids for each state, and a counter for each pair of customer and state. A table lists the legal source states for each move.

A move call first reads the record and checks that the current state is a legal source. If it is not, the call returns `false` and writes nothing. Otherwise one helper removes the id from the old state's set, lowers the old counter, stores the new record, adds the id to the new set and raises the new counter.

The invariant is that every order sits in exactly one state set, and each counter equals the number of the customer's orders in that state. Only the helper writes these three structures.

**Complexity.**

- **Time** is O(log n) per call, because a move does one hash lookup and two tree operations. A list call costs O(k) for k results.
- **Space** is O(n), because each order owns one record, one set slot and a share of a counter.

```java run
import java.util.*;

public final class OrderManagementSolution {
    static final class Orders {
        private enum State { CREATED, PAID, SHIPPED, DELIVERED, CANCELLED }
        private record Order(int customer, State state) {}
        private final Map<Integer, Order> orderOf = new HashMap<>();                              // id -> record, source of truth
        private final EnumMap<State, TreeSet<Integer>> byState = new EnumMap<>(State.class);
        private final Map<Long, Integer> counter = new HashMap<>();                               // (customer, state) -> count

        Orders() { for (State s : State.values()) byState.put(s, new TreeSet<>()); }

        private static long key(int customer, State s) { return ((long) customer << 8) | s.ordinal(); }

        /**
         * Moves one order between states and repairs every view.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: the id leaves the old set before it enters the new one.
         */
        private void move(int id, Order old, State to) {
            byState.get(old.state()).remove(id);
            counter.merge(key(old.customer(), old.state()), -1, Integer::sum);
            orderOf.put(id, new Order(old.customer(), to));
            byState.get(to).add(id);
            counter.merge(key(old.customer(), to), 1, Integer::sum);
        }

        // Checks legality first and calls move only for a legal source state; O(log n) time, O(1) space.
        private boolean transition(int id, State to, State... allowedFrom) {
            Order o = orderOf.get(id);
            if (o == null) return false;
            boolean legal = false;
            for (State s : allowedFrom) if (o.state() == s) legal = true;
            if (!legal) return false;
            move(id, o, to);
            return true;
        }

        boolean create(int id, int customer) {
            if (orderOf.containsKey(id)) return false;
            orderOf.put(id, new Order(customer, State.CREATED));
            byState.get(State.CREATED).add(id);
            counter.merge(key(customer, State.CREATED), 1, Integer::sum);
            return true;
        }

        boolean pay(int id) { return transition(id, State.PAID, State.CREATED); }
        boolean ship(int id) { return transition(id, State.SHIPPED, State.PAID); }
        boolean deliver(int id) { return transition(id, State.DELIVERED, State.SHIPPED); }
        boolean cancel(int id) { return transition(id, State.CANCELLED, State.CREATED, State.PAID); }

        /** Lists the ids in one state in order; O(k) time and space for k results. */
        List<Integer> listByState(String state) { return new ArrayList<>(byState.get(State.valueOf(state))); }

        /** Counts one customer's orders in a state; O(1) time and space. */
        int countByCustomer(int customer, String state) { return counter.getOrDefault(key(customer, State.valueOf(state)), 0); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Orders a = new Orders();
        boolean[] r = {a.create(1, 7), a.create(2, 7), a.pay(1), a.ship(1), a.cancel(1)};
        if (!r[0] || !r[1] || !r[2] || !r[3] || r[4] || !a.listByState("SHIPPED").equals(List.of(1))) throw new AssertionError("e1");
        Orders b = new Orders();
        if (!b.create(3, 8) || !b.cancel(3) || b.pay(3) || b.countByCustomer(8, "CANCELLED") != 1) throw new AssertionError("e2");
        // Random calls checked against a plain map of states.
        Random rnd = new Random(3822);
        String[] names = {"CREATED", "PAID", "SHIPPED", "DELIVERED", "CANCELLED"};
        for (int round = 0; round < 300; round++) {
            Orders s = new Orders();
            Map<Integer, String> st = new HashMap<>();
            Map<Integer, Integer> cust = new HashMap<>();
            for (int op = 0; op < 100; op++) {
                int id = rnd.nextInt(6), t = rnd.nextInt(6);
                if (t == 0) {
                    int c = rnd.nextInt(3);
                    boolean want = !st.containsKey(id);
                    if (want) { st.put(id, "CREATED"); cust.put(id, c); }
                    if (s.create(id, c) != want) throw new AssertionError("create");
                } else {
                    String from1 = t == 1 ? "CREATED" : t == 2 ? "PAID" : t == 3 ? "SHIPPED" : "CREATED";
                    String from2 = t >= 4 ? "PAID" : from1;
                    String to = t == 1 ? "PAID" : t == 2 ? "SHIPPED" : t == 3 ? "DELIVERED" : "CANCELLED";
                    boolean want = st.containsKey(id) && (st.get(id).equals(from1) || st.get(id).equals(from2));
                    if (want) st.put(id, to);
                    boolean got = t == 1 ? s.pay(id) : t == 2 ? s.ship(id) : t == 3 ? s.deliver(id) : s.cancel(id);
                    if (got != want) throw new AssertionError("move " + t);
                }
                for (String name : names) {
                    List<Integer> want = new ArrayList<>();
                    for (int i = 0; i < 6; i++) if (name.equals(st.get(i))) want.add(i);
                    if (!s.listByState(name).equals(want)) throw new AssertionError("list");
                    for (int c = 0; c < 3; c++) {
                        int n = 0;
                        for (int i : want) if (cust.get(i) == c) n++;
                        if (s.countByCustomer(c, name) != n) throw new AssertionError("count");
                    }
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Failed Transition Rollback (Author exercise)
<!-- id: ci40-failed-rollback -->

**Approach.** Three structures hold the state: a map from item to stock, a map from customer to held quantities, and a map from item to the sorted set of customers who hold it. A checkout call first adds the quantities of every line into a local map of totals per item. It then checks each total against the stock and returns `false` if any total is too large. No structure has been written at that point.

When every check passes, the commit loops over the totals once. For each item it lowers the stock, raises the customer's held quantity and inserts the customer into the item's holder set. A check line by line would accept two lines of 1 unit against a stock of 1, so the plan must hold totals per item.

The invariant is that the stock plus all held quantities of an item stays equal to the starting stock, and an item's holder set holds exactly the customers with a positive held quantity.

**Complexity.**

- **Time** is O(L log n) per checkout call, where L is the number of lines, because the plan and the commit each visit every item once and the set insertion costs O(log n).
- **Space** is O(n + h), where h is the number of pairs of customer and item that hold stock, because the plan adds O(L) temporary entries.

```java run
import java.util.*;

public final class FailedRollbackSolution {
    static final class Warehouse {
        private final Map<String, Long> stock = new HashMap<>();
        private final Map<Integer, Map<String, Long>> held = new HashMap<>();       // customer -> item -> quantity
        private final Map<String, TreeSet<Integer>> holdersOf = new HashMap<>();     // item -> customers with a positive quantity

        Warehouse(String[] items, int[] quantities) {
            for (int i = 0; i < items.length; i++) stock.merge(items[i], (long) quantities[i], Long::sum);
        }

        /**
         * Reserves all lines or none.
         * Time: O(L log n) for L lines.
         * Space: O(L) for the plan.
         * Invariant: no structure changes before every total passes its check.
         */
        boolean checkout(int customer, String[] items, int[] quantities) {
            // The plan sums the demand per item, because two lines can name one item.
            Map<String, Long> plan = new HashMap<>();
            for (int i = 0; i < items.length; i++) plan.merge(items[i], (long) quantities[i], Long::sum);
            for (Map.Entry<String, Long> e : plan.entrySet()) {
                // One failed check ends the call before any write.
                if (stock.getOrDefault(e.getKey(), 0L) < e.getValue()) return false;
            }
            // The commit cannot fail, because every total already fits.
            for (Map.Entry<String, Long> e : plan.entrySet()) {
                stock.merge(e.getKey(), -e.getValue(), Long::sum);
                held.computeIfAbsent(customer, k -> new HashMap<>()).merge(e.getKey(), e.getValue(), Long::sum);
                holdersOf.computeIfAbsent(e.getKey(), k -> new TreeSet<>()).add(customer);
            }
            return true;
        }

        long stock(String item) { return stock.getOrDefault(item, 0L); }

        long held(int customer, String item) { return held.getOrDefault(customer, Map.of()).getOrDefault(item, 0L); }

        List<Integer> holders(String item) { return new ArrayList<>(holdersOf.getOrDefault(item, new TreeSet<>())); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Warehouse w = new Warehouse(new String[] {"a", "b"}, new int[] {3, 2});
        if (!w.checkout(1, new String[] {"a", "b"}, new int[] {2, 1})) throw new AssertionError("e1 first");
        if (w.checkout(2, new String[] {"a", "a"}, new int[] {1, 1})) throw new AssertionError("e1 duplicate lines");
        if (w.stock("a") != 1 || !w.holders("a").equals(List.of(1)) || w.held(2, "a") != 0) throw new AssertionError("failed call changed state");
        if (!w.checkout(2, new String[] {"b", "a"}, new int[] {1, 1}) || !w.holders("a").equals(List.of(1, 2))) throw new AssertionError("e2");
        // Random calls checked against a simulation on copies.
        Random rnd = new Random(42);
        String[] names = {"a", "b", "c"};
        for (int round = 0; round < 300; round++) {
            int[] start = {rnd.nextInt(6), rnd.nextInt(6), rnd.nextInt(6)};
            Warehouse s = new Warehouse(names, start);
            long[] stk = {start[0], start[1], start[2]};
            long[][] hold = new long[4][3];
            for (int op = 0; op < 40; op++) {
                int c = 1 + rnd.nextInt(3), lines = 1 + rnd.nextInt(4);
                String[] it = new String[lines];
                int[] q = new int[lines];
                long[] need = new long[3];
                for (int i = 0; i < lines; i++) { int k = rnd.nextInt(3); it[i] = names[k]; q[i] = 1 + rnd.nextInt(3); need[k] += q[i]; }
                boolean want = true;
                for (int k = 0; k < 3; k++) if (need[k] > stk[k]) want = false;
                if (want) for (int k = 0; k < 3; k++) { stk[k] -= need[k]; hold[c][k] += need[k]; }
                if (s.checkout(c, it, q) != want) throw new AssertionError("verdict");
                for (int k = 0; k < 3; k++) {
                    if (s.stock(names[k]) != stk[k]) throw new AssertionError("stock");
                    List<Integer> hs = new ArrayList<>();
                    for (int x = 1; x <= 3; x++) { if (s.held(x, names[k]) != hold[x][k]) throw new AssertionError("held"); if (hold[x][k] > 0) hs.add(x); }
                    if (!s.holders(names[k]).equals(hs)) throw new AssertionError("holders");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Design Event Manager (LeetCode 3885)
<!-- id: ci40-event-manager -->

**Approach.** A hash map from event id to an immutable record of time and state is the source of truth. Two derived views follow it: a tree set of scheduled events ordered by time and then id, and a counter for each state. Only `SCHEDULED` events appear in the tree set.

Reschedule and cancel first read the record and return `false` unless the state is `SCHEDULED`. Reschedule then removes the event with the old time from the tree set, stores the new record and inserts the event with the new time. Cancel removes the event from the tree set and moves one unit between the counters. A run call polls the first event of the tree set, stores the record in state `DONE` and moves one unit between the counters.

The invariant is that the tree set holds exactly the scheduled events with their current times, and each counter equals the number of records in that state.

**Complexity.**

- **Time** is O(log n) per call, because each call does one hash lookup and at most two tree operations.
- **Space** is O(n), because each event owns one record and at most one tree entry.

```java run
import java.util.*;

public final class EventManagerSolution {
    static final class Events {
        private enum State { SCHEDULED, CANCELLED, DONE }
        private record Event(int time, int id) {}
        private record Rec(int time, State state) {}
        private final Map<Integer, Rec> recOf = new HashMap<>();                        // id -> record, source of truth
        private final TreeSet<Event> scheduled = new TreeSet<>((a, b) ->
                a.time() != b.time() ? Integer.compare(a.time(), b.time()) : Integer.compare(a.id(), b.id()));
        private final int[] counts = new int[3];                                        // number of events per state

        /** Adds a scheduled event; O(log n) time, O(1) space; invariant: the record, the tree and the counter agree. */
        boolean create(int id, int time) {
            if (recOf.containsKey(id)) return false;
            recOf.put(id, new Rec(time, State.SCHEDULED));
            scheduled.add(new Event(time, id));
            counts[State.SCHEDULED.ordinal()]++;
            return true;
        }

        /** Moves a scheduled event to a new time; O(log n) time, O(1) space; invariant: the old tree entry leaves first. */
        boolean reschedule(int id, int newTime) {
            Rec r = recOf.get(id);
            if (r == null || r.state() != State.SCHEDULED) return false;
            scheduled.remove(new Event(r.time(), id));
            recOf.put(id, new Rec(newTime, State.SCHEDULED));
            scheduled.add(new Event(newTime, id));
            return true;
        }

        /** Cancels a scheduled event; O(log n) time, O(1) space; invariant: only scheduled events sit in the tree. */
        boolean cancel(int id) {
            Rec r = recOf.get(id);
            if (r == null || r.state() != State.SCHEDULED) return false;
            scheduled.remove(new Event(r.time(), id));
            recOf.put(id, new Rec(r.time(), State.CANCELLED));
            counts[State.SCHEDULED.ordinal()]--;
            counts[State.CANCELLED.ordinal()]++;
            return true;
        }

        /** Runs the earliest scheduled event or returns -1; O(log n) time, O(1) space; invariant: the polled event leaves the tree. */
        int runNext() {
            Event e = scheduled.pollFirst();
            if (e == null) return -1;
            recOf.put(e.id(), new Rec(e.time(), State.DONE));
            counts[State.SCHEDULED.ordinal()]--;
            counts[State.DONE.ordinal()]++;
            return e.id();
        }

        /** Returns the number of events in a state; O(1) time and space. */
        int count(String state) { return counts[State.valueOf(state).ordinal()]; }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Events a = new Events();
        a.create(1, 50); a.create(2, 30); a.create(3, 30);
        if (a.runNext() != 2 || !a.reschedule(3, 60) || a.runNext() != 1) throw new AssertionError("e1");
        Events b = new Events();
        b.create(5, 10);
        if (!b.cancel(5) || b.reschedule(5, 20) || b.runNext() != -1 || b.count("CANCELLED") != 1) throw new AssertionError("e2");
        // Random calls checked against a scan of a plain map.
        Random rnd = new Random(3885);
        String[] names = {"SCHEDULED", "CANCELLED", "DONE"};
        for (int round = 0; round < 300; round++) {
            Events s = new Events();
            Map<Integer, int[]> ref = new HashMap<>();                                   // id -> {time, state}
            for (int op = 0; op < 100; op++) {
                int id = rnd.nextInt(6), t = rnd.nextInt(4);
                if (t == 0) {
                    int time = rnd.nextInt(4);
                    boolean want = !ref.containsKey(id);
                    if (want) ref.put(id, new int[] {time, 0});
                    if (s.create(id, time) != want) throw new AssertionError("create");
                } else if (t == 1) {
                    int time = rnd.nextInt(4);
                    boolean want = ref.containsKey(id) && ref.get(id)[1] == 0;
                    if (want) ref.get(id)[0] = time;
                    if (s.reschedule(id, time) != want) throw new AssertionError("reschedule");
                } else if (t == 2) {
                    boolean want = ref.containsKey(id) && ref.get(id)[1] == 0;
                    if (want) ref.get(id)[1] = 1;
                    if (s.cancel(id) != want) throw new AssertionError("cancel");
                } else {
                    int best = -1;
                    for (int i : ref.keySet()) if (ref.get(i)[1] == 0 && (best == -1 || ref.get(i)[0] < ref.get(best)[0] || (ref.get(i)[0] == ref.get(best)[0] && i < best))) best = i;
                    if (best != -1) ref.get(best)[1] = 2;
                    if (s.runNext() != best) throw new AssertionError("runNext");
                }
                for (int k = 0; k < 3; k++) {
                    int n = 0;
                    for (int[] v : ref.values()) if (v[1] == k) n++;
                    if (s.count(names[k]) != n) throw new AssertionError("count");
                }
            }
        }
    }
}
```
