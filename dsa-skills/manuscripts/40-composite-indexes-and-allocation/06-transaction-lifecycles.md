<!-- lesson-kind: standard -->
<!-- lesson-id: transaction-lifecycles -->
## Transaction Lifecycles

<!-- stage: context -->
### A Withdrawal That Fails After Taking Cash

A cash machine holds five kinds of banknotes. A customer asks for 130, and the machine can reach only 120 with the notes it has. The code takes notes from the inventory one denomination at a time, and it stops with an error when the amount does not come out exact. The error screen appears, and the customer leaves with no cash. The inventory now holds fewer notes than before, because the code had already removed them.

Every later customer sees a machine that holds less cash than its ledger says. Nobody can find the missing notes, because each failed request leaves a small unexplained change behind.

This lesson asks how to run a call that changes several counters and indexes so that a failure leaves everything as it was. The same idea covers calls that move one record through a lifecycle.

<!-- stage: naive -->
### Changing The Inventory While Deciding

The direct design walks through the denominations from the largest to the smallest. It subtracts notes from the inventory as it goes and checks at the end whether the remaining amount is zero.

```java
final class NaiveAtm {
    private static final int[] VALUE = {20, 50, 100, 200, 500};
    private final long[] notes = new long[5];

    void deposit(int[] add) { for (int i = 0; i < 5; i++) notes[i] += add[i]; }

    int[] withdraw(int amount) {
        int[] used = new int[5];
        for (int i = 4; i >= 0; i--) {
            int take = (int) Math.min(notes[i], amount / VALUE[i]);
            notes[i] -= take;                      // writes before the answer is known
            used[i] = take;
            amount -= take * VALUE[i];
        }
        return amount == 0 ? used : new int[] {-1};   // the failure path keeps the writes
    }
}
```

The success path is correct. The failure path returns `{-1}` and leaves the changed inventory.

```predict
The machine holds one 50 note and two 20 notes, and a customer asks for 130. What does the inventory look like after the failed call, and what should it look like?

The loop takes one 50 note and two 20 notes for a total of 90, finds 40 still missing and returns the failure value. The inventory now holds no 50 and no 20 notes. It should still hold one 50 note and two 20 notes, because a failed call must change nothing.
```

<!-- stage: bottleneck -->
### Writes That Happen Before The Verdict

The cost here is correctness, not time. The loop does O(1) work for five denominations, and the damage comes from the order of its steps. The code writes the first result before it knows whether the call succeeds.

A failure can arrive at any point after the first write. The more steps a call has, the more half-finished states exist. A call that touches a map, a sorted index and a counter has at least three places where it can stop in the middle. Each place leaves a different mix of old and new data.

Repairing a half-finished state after the fact is hard. The code would have to remember every earlier write and undo it in reverse order. A simpler path is to avoid the writes until the verdict is known.

<!-- stage: insight -->
### Decide First, Then Change Everything

Split every public call into two phases. The first phase computes a **plan**, which is a description of every change the call would make. It reads state and writes nothing outside local variables. If the plan is impossible, the call returns the failure value and nothing has changed.

#### The Commit Step

The second phase is the **commit**. It applies every change in the plan, and it cannot fail. All checks that could fail belong to the first phase. Because the commit has no failure path, no reader ever sees half of it.

#### When A Failure Cannot Be Avoided

Sometimes a later step can only be checked by running it. Then the call has to undo its earlier writes. A **rollback** restores each changed value in reverse order, using the old values the call saved. A rollback is a fallback. A plan that checks everything first is shorter and has less code to get wrong.

The invariant is that every public call either applies its whole plan or changes nothing, so every counter and every index describes the same state after each call.

<!-- names: plan, commit, rollback -->

<!-- stage: variables -->
### State Touched By One Call

A call of this kind touches four kinds of state, and each kind has a stated moment of change.

- **Record** is the authoritative state of the entity, such as the note counts or an order's current state, and it changes only in the commit.
- **Index** is any derived view, such as a sorted set of orders per state, and it changes in the same commit as the record.
- **Plan** is a local copy of the changes, such as the notes to hand out, and it exists only during the call.
- **Verdict** is the boolean or failure code that the first phase produces before any commit.

<!-- stage: trace -->
### Following Plans And Commits

#### A Machine With A Failing Request

The first trace follows the cash machine. The pointer `call` sits on the latest call, and each step shows the inventory in the order 20, 50, 100, 200, 500.

```trace
{"cells":["deposit","withdraw(600)","withdraw(125)","withdraw(300)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"stock":"0,10,0,3,1","plan":"-"},"note":"Call 0: the deposit adds the counts 0, 10, 0, 3 and 1 to the stock."},{"at":{"call":1},"vars":{"stock":"0,8,0,3,0","plan":"0,2,0,0,1"},"note":"Call 1: the plan 0,2,0,0,1 pays 600 exactly, so the commit subtracts it from the stock."},{"at":{"call":2},"vars":{"stock":"0,8,0,3,0","plan":"fails"},"note":"Call 2: the plan 0,2,0,0,0 leaves 25 unpaid, so the call returns -1 and the stock does not change."},{"at":{"call":3},"vars":{"stock":"0,6,0,2,0","plan":"0,2,0,1,0"},"note":"Call 3: the plan 0,2,0,1,0 pays 300 exactly, so the commit subtracts it from the stock."}]}
```

The third call plans to take two 50 notes and then finds 25 left over. The plan is impossible, so the call returns `-1` and the inventory stays as it was.

#### An Order Moving Between States

The second trace follows orders through the states created, paid and shipped, and the state cancelled. A legal move changes the record and the state index together. An illegal move changes neither.

```trace
{"cells":["create(1)","create(2)","pay(1)","ship(1)","cancel(1)","cancel(2)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"indexes":"CRE:{1}","result":"true"},"note":"Call 0: order 1 enters the CREATED index."},{"at":{"call":1},"vars":{"indexes":"CRE:{1,2}","result":"true"},"note":"Call 1: order 2 enters the CREATED index."},{"at":{"call":2},"vars":{"indexes":"CRE:{2} PAI:{1}","result":"true"},"note":"Call 2: order 1 is CREATED, so it leaves that index and enters PAID."},{"at":{"call":3},"vars":{"indexes":"CRE:{2} SHI:{1}","result":"true"},"note":"Call 3: order 1 is PAID, so it leaves that index and enters SHIPPED."},{"at":{"call":4},"vars":{"indexes":"CRE:{2} SHI:{1}","result":"false"},"note":"Call 4: order 1 is SHIPPED, which cannot be cancelled, so the call returns false and no index changes."},{"at":{"call":5},"vars":{"indexes":"SHI:{1} CAN:{2}","result":"true"},"note":"Call 5: order 2 is CREATED, so it leaves that index and enters CANCELLED."}]}
```

The fifth call asks to cancel an order that already shipped. The check reads the record and rejects the move before any write.

<!-- stage: code -->
### The Machine With Plan Then Commit

The class computes the plan in a local array and commits it only when the remaining amount is zero.

```java
final class SafeAtm {
    private static final int[] VALUE = {20, 50, 100, 200, 500};
    private final long[] notes = new long[5];

    void deposit(int[] add) { for (int i = 0; i < 5; i++) notes[i] += add[i]; }

    int[] withdraw(int amount) {
        int[] plan = new int[5];
        int left = amount;
        for (int i = 4; i >= 0; i--) {                       // phase one reads notes and writes only plan
            plan[i] = (int) Math.min(notes[i], left / VALUE[i]);
            left -= plan[i] * VALUE[i];
        }
        if (left != 0) return new int[] {-1};                // failure: nothing was written
        for (int i = 0; i < 5; i++) notes[i] -= plan[i];     // phase two cannot fail
        return plan;
    }
}
```

A call costs O(1) for a fixed number of denominations. The space is O(1) beyond the five counters.

<!-- stage: applicability -->
### Calls That Move Several Pieces Of State

#### Recognizing The Pattern

The cue is one public call that changes more than one value, or that moves an entity from one state to the next. Write down every value and index the call changes. The invariant is that each call applies its whole plan or none of it.

#### Lifecycle Rules

A lifecycle is a graph of legal moves, such as created to paid to shipped. Store the legal moves as data and check the current state against them in the first phase. A move that the graph does not allow returns `false` and leaves every index untouched.

#### False Friends

A try-catch block around the writes looks like a safe design. It is a false friend when the catch block cannot restore the old values, because the exception arrives after some writes. Locks and synchronized methods protect against other threads, and they do not make a call all-or-nothing against its own failure. Skip the two phases when the call changes exactly one value, because a single write cannot be left half done.

<!-- stage: exercises -->
### Exercises

#### [Build] Design ATM Machine (LeetCode 2241)
<!-- id: ci40-atm -->

**Prerequisites.** Arrays and greedy choice.

**Problem.** Design a class `Atm` that stores counts of banknotes of values 20, 50, 100, 200 and 500, all starting at 0. The call `deposit(counts)` adds the five counts in that order. The call `withdraw(amount)` hands out the amount by taking as many notes as possible of the largest value, then the next largest, and so on, with no later correction. It returns the five counts it hands out and removes them from the stock. If the amount cannot be reached exactly by this rule, it returns `[-1]` and changes nothing.

**Constraints.** The limits are:
- **Counts** are integers from 0 to 10^9 per call, and totals fit in a `long`.
- **Amount** satisfies `1 <= amount <= 10^9`.
- **Calls** number at most 5000.
- **Return** is an array of length 5, or `[-1]`.

**Example 1.** Input calls `deposit([3,2,0,1,0])`, `withdraw(270)`, output `[1,1,0,1,0]`.

**Example 2.** Input the same deposit and withdraw, then `withdraw(130)`, `withdraw(90)`, output `[-1]` and then `[2,1,0,0,0]`.

**Hint.** Which array holds the notes you would take, and when may the stock array change?

**Changed decision.** The result is known only after all five denominations are checked, so the stock changes after the last check.

#### [Vary] Design Order Management System (LeetCode 3822)
<!-- id: ci40-order-management -->

**Prerequisites.** The ATM exercise above and tree sets.

**Problem.** The rules below are this chapter's own wording and may differ in detail from LeetCode. Design a class `Orders`. The call `create(orderId, customerId)` adds an order in state `CREATED` and returns `true`, or returns `false` if the id exists. The call `pay(orderId)` moves `CREATED` to `PAID`. The call `ship(orderId)` moves `PAID` to `SHIPPED`. The call `deliver(orderId)` moves `SHIPPED` to `DELIVERED`. The call `cancel(orderId)` moves `CREATED` or `PAID` to `CANCELLED`. Each move returns `true` when legal and `false` otherwise, and an illegal move changes nothing. The call `listByState(state)` returns the order ids in that state in increasing order. The call `countByCustomer(customerId, state)` returns how many of that customer's orders are in that state.

**Constraints.** The limits are:
- **Ids** are integers from 1 to 10^5, and customers are integers from 1 to 10^4.
- **States** are the strings `CREATED`, `PAID`, `SHIPPED`, `DELIVERED` and `CANCELLED`.
- **Calls** number at most `10^5`, and a move may name an unknown order, which is illegal.
- **Return** of `listByState` is a list, and `countByCustomer` returns an `int`.

**Example 1.** Input calls `create(1,7)`, `create(2,7)`, `pay(1)`, `ship(1)`, `cancel(1)`, `listByState(SHIPPED)`, output `true`, `true`, `true`, `true`, `false` and the list 1.

**Example 2.** Input calls `create(3,8)`, `cancel(3)`, `pay(3)`, `countByCustomer(8,CANCELLED)`, output `true`, `true`, `false` and 1.

**Hint.** Which two indexes change when an order moves from one state to the next?

**Changed decision.** Each move changes the record and two indexes, so a helper moves all three in one step after the legality check.

#### [Boundary] Failed Transition Rollback (Author exercise)
<!-- id: ci40-failed-rollback -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `Warehouse` built from arrays `items` and `quantities` that give the starting stock of each item. The call `checkout(customer, items, quantities)` reserves several lines for a customer at once. It returns `true` and applies every line when the stock covers the total demand of each item. The same item may appear in several lines, and its demands add up. Otherwise it returns `false` and changes nothing. The call `stock(item)` returns the stock. The call `held(customer, item)` returns the quantity that the customer holds. The call `holders(item)` returns the customers who hold the item in increasing order.

**Constraints.** The limits are:
- **Items** are lowercase strings, and **customers** are integers from 1 to 10^4.
- **Quantities** are integers from 1 to 10^6 per line, and totals fit in a `long`.
- **Lines** number from 1 to 100 per checkout, and **calls** number at most `10^4`.
- **Holders** lists a customer only while the customer holds at least one unit of the item.

**Example 1.** Input stock `a` 3 and `b` 2, then `checkout(1,[a,b],[2,1])`, `checkout(2,[a,a],[1,1])`, `stock(a)`, `holders(a)`, output `true`, `false`, 1 and the list 1.

**Example 2.** Input the same calls, then `checkout(2,[b,a],[1,1])`, `holders(a)`, output `true` and the list 1, 2.

**Hint.** Which total must each item's stock cover when two lines name the same item?

**Changed decision.** Lines add up per item before any check, so the plan holds one total per item and the commit writes all three structures.

#### [Recognize] Design Event Manager (LeetCode 3885)
<!-- id: ci40-event-manager -->

**Prerequisites.** All three exercises above.

**Problem.** This contract is written for the chapter, so the LeetCode statement may differ in detail. Design a class `Events`. The call `create(eventId, time)` adds an event in state `SCHEDULED` and returns `true`, or returns `false` if the id exists. The call `reschedule(eventId, newTime)` changes the time of a `SCHEDULED` event and returns `true`, or returns `false` for any other state. The call `cancel(eventId)` moves a `SCHEDULED` event to `CANCELLED` and returns `true`, or returns `false` otherwise. The call `runNext()` takes the `SCHEDULED` event with the earliest time, breaking ties by the smaller id, marks it `DONE` and returns its id, or returns -1 if none exists. The call `count(state)` returns the number of events in that state.

**Constraints.** The limits are:
- **Ids** are integers from 1 to 10^5, and times satisfy `0 <= time <= 10^9`.
- **States** are the strings `SCHEDULED`, `CANCELLED` and `DONE`.
- **Calls** number at most `2 * 10^5`.
- **Return** types are `boolean`, `int` or `int` as named above.

**Example 1.** Input calls `create(1,50)`, `create(2,30)`, `create(3,30)`, `runNext()`, `reschedule(3,60)`, `runNext()`, output 2 for the first `runNext`, `true` for `reschedule`, then 1.

**Example 2.** Input calls `create(5,10)`, `cancel(5)`, `reschedule(5,20)`, `runNext()`, `count(CANCELLED)`, output `true` for `cancel`, `false` for `reschedule`, then -1 and 1.

**Hint.** Which of the three views holds only scheduled events, and which call removes an event from it?

**Changed decision.** Only scheduled events live in the time index, so every move out of that state removes the event from the index.
