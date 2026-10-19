<!-- lesson-kind: standard -->
<!-- lesson-id: transaction-ledgers -->
## Apply Transactions Without Partial Changes

<!-- stage: context -->
### A Transfer That Loses Money

A bank service keeps one balance per account. A client asks to move 40 from account 2 to account 9. The code subtracts 40 from account 2 and then looks up account 9. Account 9 does not exist, so the call returns `false`.

The caller sees a refusal and assumes nothing happened. In fact account 2 is now 40 poorer, and no other account is richer. The money has left the system without any record.

Ride systems, order counters and card authorizations show the same failure. Each public call touches several pieces of state, and a refusal that arrives after the first write leaves a mix of old and new values. This lesson asks how to write such a call so that a refused call changes nothing, and so that every counter still agrees with the records it summarizes.

The contract is small and in memory. One object holds all state in hash maps and arrays, one call runs at a time, and nothing is saved to disk.

<!-- stage: naive -->
### Writing While Still Checking

The direct design follows the order of the story. It takes money from the source, then looks for the destination, and it reports a refusal wherever it finds one.

```java
final class NaiveBank {
    private final long[] balance;

    NaiveBank(long[] start) { balance = start.clone(); }

    boolean transfer(int from, int to, long money) {
        if (from < 1 || from > balance.length) return false;
        balance[from - 1] -= money;                 // writes before every check has run
        if (to < 1 || to > balance.length) return false;   // refusal after the write
        if (balance[from - 1] < 0) return false;    // refusal after the write
        balance[to - 1] += money;
        return true;
    }

    long balance(int account) { return balance[account - 1]; }
}
```

The success path is correct. Each refusal after the first write leaves the source account changed.

```predict
The bank has accounts 1 to 3 with balances 10, 100 and 20. The call transfer(2, 9, 40) arrives. What does account 2 hold afterwards, and what should it hold?

The source check passes, so the code subtracts 40 and account 2 holds 60. The destination check then fails and the call returns false. Account 2 should still hold 100, because a refused call must change nothing.
```

<!-- stage: bottleneck -->
### Every Refusal Point After A Write

The cost here is correctness. The code does O(1) work per call, and the damage comes from the order of the steps. The call writes the source balance before it knows that the destination exists and that the source can pay.

Each refusal that follows a write creates one wrong state. A call with three checks and two writes has up to three such states. A real service has more: a trip service updates an active map and a route total, and an order counter updates a count and a price. Each extra write multiplies the mixed states that a failure can leave.

Repairing a mixed state afterwards means remembering every earlier write and undoing it in reverse order. That repair code runs rarely, so it hides its own bugs. The cheaper path is to read first, decide, and write only when every check has passed. A duplicate id, an unknown account and an overdraft are all checks of the same kind, so one early block can handle them together.

<!-- stage: insight -->
### Check Everything, Then Write Everything

Split every public call into two blocks. The first block reads state and tests all **preconditions** of the call. A precondition is a fact that must hold before the call may change anything, such as "the account exists" or "the id is not already active". The block writes nothing except local variables. When a test fails, the call returns its failure value and the object is exactly as it was.

#### The Commit Step

The second block is the **commit**. It applies every change of the call in one run, and it has no failure path. Every test that could fail already ran in the first block. A reader of the object therefore never sees a state that is half old and half new.

#### One Record And Its Summaries

Every service of this kind holds two layers. The **ledger** is the authoritative record of what happened: balances, active trips, open authorizations. Counters such as a route total, a held amount or an order count are derived from the ledger, and they exist only to answer queries in O(1). The commit writes the ledger entry and every derived counter in the same block, so a counter never describes an older ledger.

The invariant is that each accepted call moves the object from one complete state to the next, and each refused call leaves the state unchanged. The target cost is O(1) per call for hash-map state, plus O(log n) when a call also touches an ordered index.

<!-- names: preconditions, commit, ledger -->

<!-- stage: variables -->
### State Read And Written By One Call

Each call involves four kinds of data, and each has a fixed moment of change.

- **Ledger entry** is the authoritative record, such as a balance or an active trip, and it changes only in the commit.
- **Summary** is a derived counter or total, and it changes in the same commit as its ledger entry.
- **Verdict** is the boolean or failure code that the first block produces before any write.
- **Local values** are the amounts and sums computed during the checks, and they die when the call returns.

<!-- stage: trace -->
### Following Checks And Commits

#### Transfers With Refusals

The first trace runs a bank with three accounts that start at 10, 100 and 20. The pointer `call` marks the latest call, and the balances appear in account order.

```trace
{"cells":["transfer(2,3,40)","transfer(1,4,5)","withdraw(3,50)","deposit(1,15)","transfer(1,2,30)","transfer(2,1,60)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"balances":"10,60,60","result":"true"},"note":"Call 0: the transfer of 40 from account 2 to account 3 passes both tests, so the commit writes both balances."},{"at":{"call":1},"vars":{"balances":"10,60,60","result":"false"},"note":"Call 1: the call names account 4, which does not exist, so the first block refuses it and no balance changes."},{"at":{"call":2},"vars":{"balances":"10,60,10","result":"true"},"note":"Call 2: account 3 holds enough for 50, so the commit lowers its balance."},{"at":{"call":3},"vars":{"balances":"25,60,10","result":"true"},"note":"Call 3: account 1 exists, so the commit adds 15."},{"at":{"call":4},"vars":{"balances":"25,60,10","result":"false"},"note":"Call 4: the call asks for 30 from an account that holds 25, so the first block refuses it and no balance changes."},{"at":{"call":5},"vars":{"balances":"85,0,10","result":"true"},"note":"Call 5: the transfer of 60 from account 2 to account 1 passes both tests, so the commit writes both balances."}]}
```

Call 1 names account 4, which does not exist, so the first block refuses it before any write. Call 4 asks for 30 from an account that holds 25, so the balance is too low and the first block refuses it for the same reason.

#### Trips With A Stale Check-Out

The second trace follows an underground service. A rider id may hold at most one open trip, and each finished trip adds its duration to a route total. The column `stats` lists `route:total/count`.

```trace
{"cells":["checkIn(1,a,3)","checkIn(1,b,5)","checkIn(2,a,4)","checkOut(1,b,10)","checkOut(1,b,11)","checkOut(2,b,12)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"active":"1@a","stats":"-","result":"true"},"note":"Call 0: rider 1 has no open trip, so the commit stores station a and time 3."},{"at":{"call":1},"vars":{"active":"1@a","stats":"-","result":"false"},"note":"Call 1: rider 1 already has an open trip, so the first block refuses the call and nothing changes."},{"at":{"call":2},"vars":{"active":"1@a,2@a","stats":"-","result":"true"},"note":"Call 2: rider 2 has no open trip, so the commit stores station a and time 4."},{"at":{"call":3},"vars":{"active":"2@a","stats":"a>b:7/1","result":"true"},"note":"Call 3: the commit closes the trip of rider 1 and adds 7 to route a>b."},{"at":{"call":4},"vars":{"active":"2@a","stats":"a>b:7/1","result":"false"},"note":"Call 4: rider 1 has no open trip, so the first block refuses the call and the active map and stats stay as they were."},{"at":{"call":5},"vars":{"active":"-","stats":"a>b:15/2","result":"true"},"note":"Call 5: the commit closes the trip of rider 2 and adds 8 to route a>b."}]}
```

Call 1 reuses a rider id that is already inside a trip, so it changes nothing. Call 4 tries to check out a rider whose trip is not open, and it leaves both the active map and the stats untouched.

<!-- stage: code -->
### The Bank With Checks Before Writes

The class runs every test first and writes the two balances only after the last test passes.

```java
final class SafeBank {
    private final long[] balance;

    SafeBank(long[] start) { balance = start.clone(); }

    private boolean exists(int account) { return account >= 1 && account <= balance.length; }

    boolean transfer(int from, int to, long money) {
        if (!exists(from) || !exists(to)) return false;   // block one: reads only
        if (balance[from - 1] < money) return false;      // block one: reads only
        balance[from - 1] -= money;                       // block two: cannot fail
        balance[to - 1] += money;
        return true;
    }

    long balance(int account) { return balance[account - 1]; }
}
```

A call costs O(1) time and the object uses O(n) space for n accounts. A transfer from an account to itself passes both tests and leaves the balance unchanged.

<!-- stage: applicability -->
### Calls That Change Several Values

#### Recognizing The Pattern

The cue is a public call that changes more than one value, or that pairs an opening call with a closing call. List every ledger entry and every summary that the call writes. If a refusal is possible, move all tests before the first write. The invariant to state is that each accepted call produces one complete next state and each refused call produces none.

#### Rejecting Reused Ids

Many services reject a call because an id is already inside a lifecycle, such as a rider already checked in or an authorization still open. The test reads the active map, and it passes again once the lifecycle ends and the entry leaves the map. An id that finished is free to start again.

#### False Friends

A try-catch block around the writes looks like protection. It is a false friend when the catch block cannot restore the old values after some writes already ran. A lock protects against other callers, and it does not make a call all-or-nothing against its own refusal. Skip the two blocks only when a call writes exactly one value, because one write cannot be left half done.

<!-- stage: exercises -->
### Exercises

#### [Build] Simple Bank System (LeetCode 2043)
<!-- id: sv-bank-transfer -->

**Prerequisites.** Arrays and one-based indexing.

**Problem.** Design a class `Bank` built from a `long` array `balance`, where `balance[i - 1]` is the starting balance of account `i`. The call `transfer(from, to, money)` moves `money` from one account to another and returns `true`, or returns `false` and changes nothing. The call `deposit(account, money)` adds `money` and returns `true`, or returns `false` for an unknown account. The call `withdraw(account, money)` subtracts `money` and returns `true`, or returns `false` for an unknown account or a balance below `money`. A transfer fails for an unknown account or when the source balance is below `money`, and a transfer from an account to itself is legal when the balance covers it. The call `balance(account)` is added by this chapter and returns the current balance of a known account.

**Constraints.** The limits are:
- **Accounts** number from 1 to 10^5, and account numbers are integers from 1 to the account count.
- **Balances and money** are integers from 0 to 10^12, and totals fit in a `long`.
- **Calls** number at most 10^5, and a call may name an account outside the valid range.
- **Return** is `boolean` for the three money calls and `long` for `balance`.

**Example 1.** Input balances `[10,100,20,50,50]`, then `transfer(5,1,20)`, `transfer(3,4,25)`, `withdraw(3,20)`, `balance(1)`, `balance(3)`, output `true`, `false`, `true`, 30 and 0.

**Example 2.** Input the same balances, then `transfer(2,6,5)`, `deposit(0,5)`, `transfer(2,2,100)`, `balance(2)`, output `false`, `false`, `true` and 100.

**Hint.** Which two accounts must you look at before any balance changes?

**Changed decision.** Both accounts and the source balance are tested first, so the two balance writes happen only after every refusal has been ruled out.

#### [Vary] Design Underground System (LeetCode 1396)
<!-- id: sv-route-statistics -->

**Prerequisites.** The bank exercise above and hash maps.

**Problem.** This contract is written for this chapter and differs from the usual statement. Design a class `Metro`. The call `checkIn(id, station, t)` opens a trip for rider `id` and returns `true`, or returns `false` if that rider already has an open trip. The call `checkOut(id, station, t)` closes the open trip of the rider and returns `true`. It returns `false` and changes nothing when the rider has no open trip or when `t` is below the check-in time. A closed trip adds `t - checkInTime` to the statistics of the route from the check-in station to the check-out station. The call `getAverage(start, end)` returns the total duration divided by the trip count, rounded down, or -1 if the route has no trip. The call `maxTrip(start, end)` returns the longest duration on the route, or -1 if the route has no trip.

**Constraints.** The limits are:
- **Rider ids** are integers from 1 to 10^6, and **stations** are lowercase strings of length 1 to 10.
- **Times** are integers from 0 to 10^9, and calls need not arrive in time order.
- **Calls** number at most 2 * 10^5.
- **Return** is `boolean` for the two trip calls and `long` for the two route queries.

**Example 1.** Input calls `checkIn(1,a,3)`, `checkIn(1,b,5)`, `checkIn(2,a,4)`, `checkOut(1,b,10)`, `checkOut(2,b,12)`, `getAverage(a,b)`, `maxTrip(a,b)`, output `true`, `false`, `true`, `true`, `true`, 7 and 8.

**Example 2.** Input calls `checkIn(4,c,10)`, `checkOut(4,a,9)`, `checkOut(4,a,15)`, `checkOut(4,a,16)`, `getAverage(c,a)`, `getAverage(a,c)`, output `true`, `false`, `true`, `false`, 5 and -1.

**Hint.** What must be true about the rider before the check-out may touch the route totals?

**Changed decision.** A check-out is refused before any write when the trip is missing or the time is earlier, and a refused check-out keeps the rider's trip open. The route also keeps a maximum, and the average rounds down.

#### [Boundary] Duplicate Active Transaction (Author exercise)
<!-- id: sv-duplicate-active -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `Holds` built from a `long` array `balance`, where `balance[i - 1]` is the balance of account `i`. The call `authorize(txId, account, amount)` reserves `amount` on an account and returns `true`. It returns `false` and changes nothing if `txId` is already active, the account is unknown, or `amount` exceeds the available amount of the account. The available amount is the balance minus the sum of the account's active reservations. The call `settle(txId)` removes the reservation and lowers the balance by its amount. The call `release(txId)` removes the reservation and leaves the balance unchanged. Both calls return `true`, or return `false` for an id that is not active. The call `available(account)` returns the available amount of a known account.

**Constraints.** The limits are:
- **Accounts** number from 1 to 10^4, and balances are integers from 0 to 10^12.
- **Transaction ids** are integers from 1 to 10^9, and amounts are integers from 1 to 10^12.
- **Calls** number at most 10^5, and an id may start again after it was settled or released.
- **Return** is `boolean` for the three transaction calls and `long` for `available`.

**Example 1.** Input balances `[100,50]`, then `authorize(7,1,60)`, `authorize(7,2,10)`, `authorize(8,1,50)`, `available(1)`, `settle(7)`, `authorize(7,2,10)`, `available(2)`, output `true`, `false`, `false`, 40, `true`, `true` and 40.

**Example 2.** Input the same balances, then `authorize(1,2,50)`, `release(1)`, `release(1)`, `available(2)`, `authorize(1,3,5)`, output `true`, `true`, `false`, 50 and `false`.

**Hint.** Which map answers whether an id is active, and when does an entry leave it?

**Changed decision.** The same id is refused while it is active, even for a different account, and accepted again after it ends. Both ends of the lifecycle update the reservation map and the sum of active reservations together.

#### [Recognize] Apply Discount Every n Orders (LeetCode 1357)
<!-- id: sv-cashier-discount -->

**Prerequisites.** All three exercises above.

**Problem.** The rules below are this chapter's own wording and may differ from LeetCode in detail. Design a class `Cashier` built from `n`, a percentage `discount`, an array `products` of distinct ids and an array `prices` of integer prices. The call `getBill(product, amount)` receives parallel arrays of order lines and returns the bill as a `long`. The bill is the sum of `price * amount` over the lines. If any product id is not in the catalog, the call returns -1 and the order does not count. Every n-th counted order is paid at `total * (100 - discount) / 100`, rounded down. Orders that return -1 are not counted.

**Constraints.** The limits are:
- **Catalog** holds 1 to 200 products with ids from 1 to 200 and prices from 1 to 1000.
- **Parameters** satisfy `1 <= n <= 10^4` and `0 <= discount <= 100`.
- **Orders** have 1 to 200 lines with amounts from 1 to 1000, and an id may repeat inside an order.
- **Calls** number at most 10^4.

**Example 1.** Input `Cashier(3,50,[1,2,3],[100,200,300])`, then `getBill([1,2],[1,1])`, `getBill([3],[1])`, `getBill([1,1],[1,2])`, output 300, 300 and 150.

**Example 2.** Input `Cashier(2,10,[1],[100])`, then `getBill([1],[1])`, `getBill([5],[1])`, `getBill([1],[3])`, output 100, -1 and 270.

**Hint.** When does the order counter change, and what must be known by then?

**Changed decision.** The counter and the discount depend on the whole order being valid, so every line is priced into a local total before the counter moves.
