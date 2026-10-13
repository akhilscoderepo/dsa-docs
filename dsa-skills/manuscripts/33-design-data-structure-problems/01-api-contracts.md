<!-- lesson-kind: standard -->
<!-- lesson-id: api-contracts -->
## Write The Contract Before The Code

<!-- stage: context -->
### Why A Counter Class Loses Data

A login service counts failed sign-ins per account and locks an account after five failures. A support script calls `all()` on the counter to print the day's totals and then clears the returned map to keep its own output tidy. The next morning the lockout rule sees zero failures for every account, and nobody has touched the counter class in weeks.

No single method in that class is wrong. The class never said what `all()` hands out, so the script assumed it was a private copy. Most problems in this chapter have the same shape. A data-structure problem is a sequence of public calls, and the structure is correct only if every call in every order leaves it usable. This lesson asks what each call must promise before any code exists.

<!-- stage: naive -->
### Writing The Counter Without A Plan

The tempting version starts from the fields. A map from account name to count is the obvious state, so each method does whatever is shortest.

```java
import java.util.HashMap;
import java.util.Map;

final class SloppyCounter {
    private final Map<String, Integer> counts = new HashMap<>();

    int add(String key) {
        Integer old = counts.get(key);
        counts.put(key, old == null ? 1 : old + 1);
        return counts.get(key);
    }

    Integer count(String key) { return counts.get(key); }   // null when the key is absent

    int remove(String key) {
        Integer old = counts.get(key);
        if (old == null) return -1;                          // -1 when the key is absent
        counts.put(key, old - 1);                            // keeps an entry that holds 0
        return old - 1;
    }

    Map<String, Integer> all() { return counts; }            // hands out the real map
}
```

Every method compiles and passes a quick manual test. The trouble appears on the second and third call. One caller reads `count("bob")` for an account that never failed and gets `null`. Another caller removes an absent key and receives `-1`, which looks like a count. A third caller removes the last failure of an account and still finds that account in `all()` with a count of 0.

```predict
A caller runs `int c = counter.count("bob");` for an account that was never added. What happens, and which line of the class is responsible?

The unboxing of `null` into an `int` throws a NullPointerException in the caller's code. The line `return counts.get(key)` is responsible, because it returns `null` as an answer and never says so.
```

<!-- stage: bottleneck -->
### Every Caller Has To Guess

No method here is slow. Each runs in O(1) expected time, so cost is not the problem. The problem is that the class answers four questions differently in each method and states none of them. A caller cannot tell what a method returns, what it changes, what happens when the call is illegal, or what it costs.

Guessing is expensive because the guesses are spread over every caller. One caller treats `null` as zero, another treats `-1` as an error, and a third compares two `Integer` results with `==`. Each guess works on small test data and fails on larger data.

Fixing this by checking inside the class has a price as well. Returning a copy of the map from `all()` costs O(k) time and space for k distinct keys on every call. That price is acceptable only when the specification says callers need a private copy. So the code alone cannot decide, and the decision has to be written down first.

<!-- stage: insight -->
### State Four Facts For Each Operation

#### Listing The Four Facts

An operation is a public method of the structure. Its contract is the promise it makes to every caller, and the contract has four parts. The **output** says what the call returns. The **mutation** says which fields change, and a call that changes nothing says so. The **failure behavior** says what happens when the call is illegal. The **cost** says the time and space, such as O(1) expected time. A structure is correct when every operation keeps its contract after every earlier call, and the invariant is the fact about the state that makes this possible.

#### Choosing How A Call Fails

The **failure contract** of an operation is the part of its contract that covers an illegal call. It has two decisions. The first is how the caller learns about the failure, and there are three standard answers. The operation throws an exception, such as `NoSuchElementException`. It returns a **sentinel**, which is a reserved return value outside the range of real answers, so `-1` works only when real answers are never negative. Or the contract states a precondition that the caller must establish, and the operation promises nothing if the caller breaks it. The second decision is whether a failed call changes the state, and the safest answer is that it never does.

Pick one answer for the whole structure. A stack whose `pop` throws and whose `top` returns `-1` forces every caller to remember both rules.

<!-- names: failure contract, sentinel, defensive copy -->

#### Keeping Internal State Private

An operation must not return a reference to a mutable field. A caller who receives the real map or array can change it without calling any operation, so the invariant no longer holds. A **defensive copy** is a new object that holds the same data, returned in place of the field. The cost of the copy, O(k) for k elements, belongs in the contract of that operation. A read-only view, such as `Collections.unmodifiableMap`, avoids the copy but reflects later changes, so the contract must say which one the caller gets.

<!-- stage: variables -->
### Names Used In A Counter Contract

A counter that supports duplicates needs a few entities with fixed meanings. The names below are used in every exercise of this lesson.

- **counts** is the map from each key to its number of occurrences, holding only keys whose count is at least 1.
- **total** is the sum of all counts, which `total()` returns in O(1).
- **distinct** is the number of keys with a positive count, which equals `counts.size()`.
- **call** is one public operation invoked on the structure, such as `add("bob")`.
- **state after a call** is the triple of `counts`, `total` and `distinct` that the next call sees.

The invariant ties these together: every stored count is at least 1, and `total` equals the sum of the stored counts.

<!-- stage: trace -->
### Tracing Calls On Two Structures

#### Following The Counter Calls

Start with an empty counter that follows the contract: `add` increments, `remove` decrements and deletes the key at zero, and `remove` on a missing key throws and changes nothing. The calls below arrive in order, and the trace records the state after each one.

The first `add("bob")` creates the key with count 1. The second `add("bob")` raises it to 2, so `total` is 2 while `distinct` stays 1. The call `add("amy")` adds a second key. The call `remove("bob")` lowers bob to 1. The call `remove("amy")` brings amy to 0, so the key disappears and `distinct` drops to 1. The last call, `remove("amy")` again, finds no key and throws, and the state is exactly what it was before the call.

```trace
{"cells":["add(bob)","add(bob)","add(amy)","remove(bob)","remove(amy)","remove(amy)"],"pointers":["call"],"steps":[{"at":{"call":-1},"vars":{"counts":"{}","total":0,"distinct":0,"result":"none"},"note":"Start: the counter is empty, so total and distinct are both 0."},{"at":{"call":0},"vars":{"counts":"{bob:1}","total":1,"distinct":1,"result":"count 1"},"note":"add(bob) raises bob to 1. total is 1 and distinct is 1."},{"at":{"call":1},"vars":{"counts":"{bob:2}","total":2,"distinct":1,"result":"count 2"},"note":"add(bob) raises bob to 2. total is 2 and distinct is 1."},{"at":{"call":2},"vars":{"counts":"{bob:2, amy:1}","total":3,"distinct":2,"result":"count 1"},"note":"add(amy) raises amy to 1. total is 3 and distinct is 2."},{"at":{"call":3},"vars":{"counts":"{bob:1, amy:1}","total":2,"distinct":2,"result":"ok"},"note":"remove(bob) lowers bob to 1. total is 2 and distinct is 2."},{"at":{"call":4},"vars":{"counts":"{bob:1}","total":1,"distinct":1,"result":"ok"},"note":"remove(amy) lowers amy to 0, so the key is deleted. total is 1 and distinct is 1."},{"at":{"call":5},"vars":{"counts":"{bob:1}","total":1,"distinct":1,"result":"throws"},"note":"remove(amy) finds no key and throws NoSuchElementException. counts, total and distinct are unchanged."}]}
```

#### Following The Stack Calls

A stack contract works the same way. It promises that `push` appends, `pop` removes and returns the newest value, `top` returns it without removing, and both `pop` and `top` throw on an empty stack without changing it.

After `push(4)` and `push(9)`, the call `top()` returns 9 and the stack still holds both values. The first `pop()` returns 9 and the second returns 4, which leaves the stack empty. The third `pop()` throws, and the stack stays empty. A later `push(7)` works normally, which proves the failed call did not damage the state. The final `top()` returns 7.

```trace
{"cells":["push(4)","push(9)","top()","pop()","pop()","pop()","push(7)","top()"],"pointers":["call"],"steps":[{"at":{"call":-1},"vars":{"stack":"[]","size":0,"result":"none"},"note":"Start: the stack is empty."},{"at":{"call":0},"vars":{"stack":"[4]","size":1,"result":"ok"},"note":"push(4) appends 4. The stack is [4]."},{"at":{"call":1},"vars":{"stack":"[4,9]","size":2,"result":"ok"},"note":"push(9) appends 9. The stack is [4, 9]."},{"at":{"call":2},"vars":{"stack":"[4,9]","size":2,"result":"9"},"note":"top() returns 9 and removes nothing. The stack is [4, 9]."},{"at":{"call":3},"vars":{"stack":"[4]","size":1,"result":"9"},"note":"pop() removes and returns 9. The stack is [4]."},{"at":{"call":4},"vars":{"stack":"[]","size":0,"result":"4"},"note":"pop() removes and returns 4. The stack is []."},{"at":{"call":5},"vars":{"stack":"[]","size":0,"result":"throws"},"note":"pop() on an empty stack throws NoSuchElementException. The stack is still empty."},{"at":{"call":6},"vars":{"stack":"[7]","size":1,"result":"ok"},"note":"push(7) appends 7. The stack is [7]."},{"at":{"call":7},"vars":{"stack":"[7]","size":1,"result":"7"},"note":"top() returns 7 and removes nothing. The stack is [7]."}]}
```

<!-- stage: code -->
### Implementing The Counter Contract

The contract goes into the Javadoc first, one line per fact, and the code follows it. This version keeps the invariant and throws on an illegal removal.

```java
import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;

final class AccountCounter {
    private final Map<String, Integer> counts = new HashMap<>();
    private int total;

    /** Output: new count of key. Mutation: count + 1, total + 1. Failure: none. Cost: O(1) expected. */
    int add(String key) {
        total++;
        return counts.merge(key, 1, Integer::sum);
    }

    /** Output: none. Mutation: count - 1, key deleted at 0. Failure: NoSuchElementException, state unchanged. Cost: O(1) expected. */
    void remove(String key) {
        Integer c = counts.get(key);
        if (c == null) throw new NoSuchElementException(key);   // checked before any write
        if (c == 1) counts.remove(key); else counts.put(key, c - 1);
        total--;
    }

    /** Output: count of key, 0 when absent. Mutation: none. Failure: none. Cost: O(1) expected. */
    int count(String key) { return counts.getOrDefault(key, 0); }

    /** Output: independent copy of the counts. Mutation: none. Cost: O(k) time and space. */
    Map<String, Integer> snapshot() { return new HashMap<>(counts); }
}
```

The method `count` returns 0 for an absent key, so absence is not a failure and callers never meet `null`. The method `remove` runs its check before any write, so a failed call leaves `counts` and `total` as they were. The method `snapshot` returns a copy, so a caller who clears the result cannot reach the field.

<!-- stage: applicability -->
### Checking The Contract Before Coding

#### Using Invariants And Calls Together

Reach for this lesson whenever a problem says "design a class" and lists methods. Correctness then lives in the order of calls, and no single call proves it. An invariant is a condition on the fields that each operation may rely on at entry and must restore before it returns. Write the invariant first, then check each operation against it, including the failing path.

#### Spotting A False Friend

A false friend is code that passes its first test call and then fails on a later call. The usual false friend here is the getter. Returning the internal array or list looks like a harmless read, yet the caller now owns a live handle to the state. The same trap appears when a constructor stores the caller's array without copying it.

#### Three Java Hazards In Contracts

Returning `null` for an empty result moves the failure into the caller, where it appears as a NullPointerException far from its cause. A method that returns `Integer` invites `==` comparison, which compares references, so two equal counts above 127 can compare as different. Declare `int` returns where absence is not a legal answer, and use `equals` when you must compare boxed values.

The next lesson in this chapter shows how each operation keeps the invariant when several fields change together.

<!-- stage: exercises -->
### Exercises

#### [Build] Specify A Counter API (Author exercise)
<!-- id: ds-specify-counter-api -->

**Prerequisites.** The counter contract in this lesson.

**Problem.** Design a class `EventCounter` that counts occurrences of string keys. It has operations `add(key)`, `remove(key)`, `count(key)`, `distinct()`, `total()` and `snapshot()`. For each operation, write its output, mutation, failure behavior and cost. Then implement the class. The operation `add` returns the new count of `key`. The operation `remove` lowers the count of `key` by one and deletes the key at zero. The operation `snapshot` returns a map that the caller may change without affecting the counter.

**Constraints.** The limits are:
- **Keys** are non-null strings, and a null key throws `NullPointerException`.
- **Removal** of a key whose count is 0 throws `NoSuchElementException` and changes no state.
- **Absent key** gives `count(key) = 0` and is not a failure.
- **Calls** number at most 10^5, and each of `add`, `remove`, `count`, `distinct`, `total` costs O(1) expected time.
- **Snapshot** costs O(k) for k distinct keys.

**Example 1.** Input `add("a")`, `add("b")`, `add("a")`, `remove("a")`, output `count("a") = 1`, `distinct() = 2`, `total() = 2`.

**Example 2.** Input a caller that clears the map returned by `snapshot()`, output that `count("a")` and `total()` are unchanged, and `remove("zzz")` throws.

**Hint.** For each operation, finish the sentence "if the caller breaks the rules, then" before you write the body. Which field would a returned reference expose?

**Changed decision.** First exercise in the sequence: moves the focus from writing methods to writing what each method promises.

#### [Vary] Empty Removal Policy (Author exercise)
<!-- id: ds-empty-removal-policy -->

**Prerequisites.** The specify-counter exercise above.

**Problem.** An `IntStack` has operations `push(v)`, `pop()`, `top()` and `isEmpty()`. Implement three versions that differ only in how `pop` and `top` treat an empty stack. The throwing version throws `NoSuchElementException` and keeps its state. The sentinel version returns `-1` and keeps its state, which requires that every pushed value is at least 0. The precondition version promises nothing for an empty stack, and callers must test `isEmpty()` first. Each version applies its rule to both `pop` and `top`.

**Constraints.** The limits are:
- **Values** pushed to the sentinel version are in the range 0 to 10^9, and a negative value throws `IllegalArgumentException`.
- **Operations** number at most 10^5, and each costs O(1) amortized.
- **Failed call** in the throwing and sentinel versions leaves size and contents unchanged.
- **Precondition version** has no behavior to test for an empty stack except that callers avoid it.

**Example 1.** Input `push(5)`, `pop()`, `pop()`, output 5 and then an exception for the throwing version, 5 and then -1 for the sentinel version.

**Example 2.** Input `push(-1)` on the sentinel version, output an `IllegalArgumentException`, because a stored -1 would be impossible to tell from "empty".

**Hint.** Where would a caller of each version have to write an extra check? Which version needs a restriction on the values?

**Changed decision.** The failure behavior changes while the output and mutation of legal calls stay the same.

#### [Boundary] Repeated Calls (Author exercise)
<!-- id: ds-repeated-calls -->

**Prerequisites.** The two exercises above.

**Problem.** A counter follows the contract of `EventCounter`. Given a list of calls of the form `add k` or `remove k`, report the state after each call. The state is written `distinct/total`. A call that succeeds is reported as `ok d/t`. A call that throws is reported as `err d/t`, and the numbers show the unchanged state. Return the list of reports in call order.

**Constraints.** The limits are:
- **Calls** number between 1 and 1000, and keys are lowercase letters.
- **Duplicates** are allowed, so the same key may be added many times.
- **Removal** of a key with count 0 is reported as `err` and changes no state.
- **Distinct** drops only when a key's count reaches 0.

**Example 1.** Input `add a`, `add a`, `remove a`, output `ok 1/1`, `ok 1/2`, `ok 1/1`.

**Example 2.** Input `add x`, `add x`, `add y`, `remove x`, `remove x`, `remove x`, `add x`, output `ok 1/1`, `ok 1/2`, `ok 2/3`, `ok 2/2`, `ok 1/1`, `err 1/1`, `ok 2/2`.

**Hint.** What happens to `distinct` on the first removal of a key that was added twice? Which numbers must a failed call leave alone?

**Changed decision.** Calls repeat on the same key, so the invariant that every stored count is at least 1 now matters on every call.

#### [Recognize] Min Stack (LeetCode 155)
<!-- id: ds-min-stack-contract -->

**Prerequisites.** All three exercises above.

**Problem.** Design a stack `MinStack` of `int` values with operations `push(v)`, `pop()`, `top()` and `getMin()`. Before any code, write the contract of each operation: output, mutation, failure behavior and cost. The operation `pop` returns the removed value. The operation `getMin` returns the smallest value currently stored. On an empty stack, `pop`, `top` and `getMin` each throw `NoSuchElementException` and leave the stack unchanged. Then implement the stack.

**Constraints.** The limits are:
- **Values** are any `int`, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Operations** number at most 10^5.
- **Cost** is O(1) for `pop`, `top` and `getMin`, and O(1) amortized for `push`.
- **Empty stack** is a failure for `pop`, `top` and `getMin`, and never returns a placeholder value.

**Example 1.** Input `push(6)`, `push(2)`, `push(9)`, `push(2)`, `getMin()`, `pop()`, `getMin()`, `pop()`, `pop()`, `getMin()`, output 2, 2, 2, 9, 2, 6 as the results of the six calls that return a value, in order.

**Example 2.** Input `pop()` on an empty stack and then `push(3)` and `getMin()`, output an exception and then 3.

**Hint.** Which value is the minimum after each push, and does it depend only on the values below it? What must `getMin` do on an empty stack?

**Changed decision.** The original problem assumes legal calls. Here the failure behavior of every operation is part of the stated contract.
