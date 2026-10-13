<!-- lesson-kind: standard -->
<!-- lesson-id: operation-traces -->
## Trace A Sequence Of Method Calls

<!-- stage: context -->
### Why A Passing Class Still Fails

A web service caps simultaneous exports at three per account. A class named `ExportLimiter` counts the running exports. Its `start()` method returns `false` at the cap. Every unit test passes, because each test creates a fresh object and calls one method. In production the counter drifts. After a burst of five start requests, the two refused calls have each added one to the counter, so it reads 5 while only three exports run. When those three finish, the counter reads 2, the limiter believes two exports still run, and it permits only one new export.

No single method is wrong on a fresh object. The failure appears only in a sequence of calls on one object, because an earlier call changed a field that a later call reads. The lesson asks one question. How does a programmer specify and check a class so that every sequence of calls stays correct?

<!-- stage: naive -->
### Testing Each Method On A Fresh Object

The direct method writes one small test per method. Each test creates a new object, calls the method once and compares the result with the expected value. For a counter with a limit, the class below looks natural, and `increment` counts first and then reports whether the count still fits.

```java
final class NaiveCounter {
    private final int limit;
    private int count;

    NaiveCounter(int limit) { this.limit = limit; }

    boolean increment() {
        count++;                 // counts first
        return count <= limit;   // then reports whether it fit
    }
    void reset() { count = 0; }
    int value() { return count; }
}
```

With limit 2, the first `increment` on a fresh object returns `true`, `value` on a fresh object returns 0, and `reset` followed by `value` returns 0. All three tests pass, so the class looks finished.

<!-- stage: bottleneck -->
### Counting The Call Sequences

```predict
A counter has limit 2. A caller invokes increment three times and then value. What does the naive class return from value, and which call first leaves the object in a condition that no later call can describe correctly?

The value call returns 3, although the counter should stop at 2. The third increment correctly returns false, yet it also raised count from 2 to 3. The single-call tests never reach that third increment, so they cannot see the problem.
```

A fresh-object test reaches only the states that the constructor produces. A real caller reaches many more. With `m` methods and traces of length `L`, a caller can issue `m^L` different sequences, ignoring the arguments. A counter with three methods has 59 049 sequences of length 10 and about 3.5 billion of length 20. Checking every sequence costs O(m^L), which no test suite can afford.

The bug also does not live in any method body. The third `increment` returns the right answer and still damages a field. The damage matters only because later calls read that field. A check must therefore look at the fields left behind by each call, not only at the value that the call returns. The next section names the property to check and shows why a short check per method covers every long sequence.

<!-- stage: insight -->
### Keep The Object Legal After Each Call

#### What An Operation Trace Records

An **operation trace** is a constructor call followed by a chronological list of method calls, each paired with the value it must return. The trace `new BoundedCounter(2)`, `increment() = true`, `increment() = true`, `increment() = false`, `value() = 2` specifies the class on one history. A class is correct when it reproduces the expected return value of every call in every trace that its documentation allows.

<!-- names: operation trace, legal state, rejected call -->

#### Legal State And The Invariant

The fields of an object together hold its state. A **legal state** is an assignment of values to all fields that the class documentation permits. For the bounded counter, a legal state satisfies `0 <= count <= limit`. The invariant of this lesson says that each completed call leaves a legal state for every possible next call. Any method may read any field, so one illegal field value can change the result of a call that comes much later.

#### A Rejected Call Changes Nothing

A **rejected call** is a call whose precondition fails, such as `increment` when `count` already equals `limit`. It returns the failure value, here `false`. It must also leave every field with the value it had before the call. The naive class breaks this rule, because it raises `count` before it decides to refuse. The repair tests the condition first and changes fields only on the accepting path.

#### Why One Check Per Method Suffices

The constructor must produce a legal state. Every other method must satisfy a second promise: when it starts in any legal state, it returns the right value and ends in a legal state. Then induction on the length of the trace proves that every trace is safe. The first call starts in the constructor's legal state, and each later call starts in the legal state that its predecessor left. The proof needs only `m + 1` checks, one for the constructor and one per method, instead of `m^L` sequences. For a rejected call the check is even simpler, because the final state must equal the initial state.

<!-- stage: variables -->
### Fields And The Trace Row

The bounded counter keeps two fields, `limit` and `count`. A trace table adds two columns, `call` and `result`, that the reader tracks after every call.

- **limit** is the capacity, fixed by the constructor and never changed afterward.
- **count** is the number of accepted increments since the last reset.
- **call** is the index of the current entry in the operation trace, where entry 0 is the constructor.
- **result** is the value the current call returns, written `true`, `false`, an integer, or `null` for a method that returns nothing.

The invariant is `0 <= count <= limit` after the constructor and after every call, whether the call succeeds or fails.

<!-- stage: trace -->
### Tracing Calls On A Counter

#### A Correct Counter With Limit 2

The first trace follows a correct counter through the constructor and seven calls. The pointer `call` marks the call that just finished, and the variable `count` shows the field after that call.

The constructor sets `count` to 0. The first two increments succeed and raise `count` to 2. The third increment arrives when `count` equals `limit`, so the counter rejects it, returns `false` and keeps `count` at 2. The `value` call then returns 2, which matches the specification. A `reset` sets `count` to 0, and the next increment succeeds again. The rejected call is the only entry where the return value says `false`, and it is also the only increment after which `count` stays the same. The two facts always appear together in a correct class.

```trace
{"cells":["new(2)","inc","inc","inc","value","reset","inc","value"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"count":0,"result":"null"},"note":"Call 0: the constructor sets limit to 2 and count to 0, which is a legal state."},{"at":{"call":1},"vars":{"count":1,"result":"true"},"note":"Call 1: count 0 is below limit 2, so the counter accepts the call, raises count to 1 and returns true."},{"at":{"call":2},"vars":{"count":2,"result":"true"},"note":"Call 2: count 1 is below limit 2, so the counter accepts the call, raises count to 2 and returns true."},{"at":{"call":3},"vars":{"count":2,"result":"false"},"note":"Call 3: count equals limit 2, so the counter rejects the call, returns false and leaves count at 2. The state is identical to the state before the call."},{"at":{"call":4},"vars":{"count":2,"result":"2"},"note":"Call 4: value returns 2. This matches the specification."},{"at":{"call":5},"vars":{"count":0,"result":"null"},"note":"Call 5: reset sets count to 0, which is legal for every limit."},{"at":{"call":6},"vars":{"count":1,"result":"true"},"note":"Call 6: count 0 is below limit 2, so the counter accepts the call, raises count to 1 and returns true."},{"at":{"call":7},"vars":{"count":1,"result":"1"},"note":"Call 7: value returns 1. This matches the specification."}]}
```

#### The Naive Counter On The First Calls

The second trace replays the first four calls on the naive class from the earlier stage. The first two increments behave exactly as before. The third increment returns `false`, so a test that checks only the return value still passes. The field tells a different story, because `count` now equals 3 while `limit` equals 2. That assignment violates `0 <= count <= limit`, so the object has left every legal state. The following `value` call returns 3, and the trace expects 2. The error shows up one call after the damage, which is why a check of the return value alone cannot locate it.

```trace
{"cells":["new(2)","inc","inc","inc","value"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"count":0,"result":"null"},"note":"Call 0: the constructor sets limit to 2 and count to 0, which is a legal state."},{"at":{"call":1},"vars":{"count":1,"result":"true"},"note":"Call 1: count counts first, goes from 0 to 1, and the call returns true. The state satisfies 0 <= count <= 2."},{"at":{"call":2},"vars":{"count":2,"result":"true"},"note":"Call 2: count counts first, goes from 1 to 2, and the call returns true. The state satisfies 0 <= count <= 2."},{"at":{"call":3},"vars":{"count":3,"result":"false"},"note":"Call 3: count goes from 2 to 3 before the check, and the call returns false. The return value is right, but count 3 exceeds limit 2, so the state is illegal."},{"at":{"call":4},"vars":{"count":3,"result":"3"},"note":"Call 4: value returns 3. The specification expects 2, so the earlier damage becomes visible here."}]}
```

<!-- stage: code -->
### Writing The Counter As A Class

#### The Class

The correct class tests the limit first and changes `count` only when the call succeeds. The constructor, `increment`, `reset` and `value` each run in constant time. The fields are private, so these four members are the only code that can change `count`, and checking them covers every trace.

```java
final class BoundedCounter {
    private final int limit;
    private int count;

    BoundedCounter(int limit) {
        this.limit = limit;   // a legal state needs limit >= 0
        this.count = 0;       // 0 <= 0 <= limit holds
    }

    boolean increment() {
        if (count == limit) return false;   // rejected: no field changes
        count++;                            // accepted: count stays <= limit
        return true;
    }

    void reset() { count = 0; }             // 0 is legal for every limit

    int value() { return count; }           // reads only, changes nothing
}
```

#### Cost

- **increment** costs O(1) time and O(1) space.
- **reset** and **value** cost O(1) time and O(1) space.

<!-- stage: applicability -->
### When To Reason About Call Sequences

#### Recognizing The Pattern

Use this method when the input is a class name, a constructor with arguments and a chronological list of method calls with their expected outputs. Design problems on contest sites use exactly this shape. Before writing code, list the fields, state the invariant over those fields, and write down for each method which fields change on the accepting path. For every method that can refuse, write down that no field changes on the refusing path. The code then follows from the list.

#### A False Friend

Correct methods on a fresh object are a false friend of a correct API. A method can return the right value for every fresh object and still leave a field in a state that breaks the next call. The naive counter shows this. The question to ask is not whether the method returns the expected value. The question is whether the object is legal when the method returns.

#### When The Method Does Not Apply

A class with no fields, such as a set of pure helper functions, has no state to keep legal. A class that several threads call at once breaks the assumption of one chronological order, so this chapter always assumes a single caller. A call that must succeed partly and fail partly needs its documentation to say which fields change, because the rule that a rejected call changes nothing no longer describes it.

<!-- stage: exercises -->
### Exercises

#### [Build] Bounded Counter API (Author exercise)
<!-- id: sc-operation-traces-bounded-counter -->

**Prerequisites.** The operation trace, legal state and rejected call definitions from this lesson.

**Problem.** Design the class `BoundedCounter` with an integer `limit` fixed by the constructor. It supports three methods. `increment()` returns `true` and adds 1 to the count when the count is less than `limit`, and otherwise returns `false`. `reset()` sets the count to 0 and returns nothing. `value()` returns the current count. The count starts at 0 and never exceeds `limit`.

**Constraints.** The limits are:
- **Limit** is an integer with `0 <= limit <= 10^9`.
- **Calls** number at most 1000 per object.
- **Rejected increment** returns `false` and changes no field.
- **Mutation** happens only inside the three methods.

**Example 1.** Input calls `["BoundedCounter","increment","increment","increment","value"]` with arguments `[[2],[],[],[],[]]`, output `[null,true,true,false,2]`.

**Example 2.** Input calls `["BoundedCounter","increment","reset","increment","increment","value"]` with arguments `[[1],[],[],[],[],[]]`, output `[null,true,null,true,false,1]`.

**Hint.** Which comparison must run before `count` changes, and what does `reset` need to keep the invariant when `limit` is 0?

**Changed decision.** Basic case: the method tests the precondition first and writes the field only on the accepting path.

#### [Vary] Design Parking System (LeetCode 1603)
<!-- id: sc-operation-traces-parking-system -->

**Prerequisites.** The Bounded Counter API exercise above.

**Problem.** Design the class `ParkingSystem` with three car types, numbered 1 for big, 2 for medium and 3 for small. The constructor receives the number of free spaces for each type in that order. `addCar(carType)` returns `true` and uses one space of that type when a space is free, and otherwise returns `false`. A space is never freed.

**Constraints.** The limits are:
- **Spaces** satisfy `0 <= big, medium, small <= 1000`.
- **Car type** is 1, 2 or 3.
- **Calls** number at most 1000 per object.
- **Rejected call** returns `false` and changes no field, including the counts of the other two types.

**Example 1.** Input calls `["ParkingSystem","addCar","addCar","addCar","addCar"]` with arguments `[[1,1,0],[1],[2],[3],[1]]`, output `[null,true,true,false,false]`.

**Example 2.** Input calls `["ParkingSystem","addCar","addCar","addCar","addCar","addCar","addCar"]` with arguments `[[2,0,1],[3],[3],[2],[1],[1],[1]]`, output `[null,true,false,false,true,true,false]`.

**Hint.** The single count of the previous exercise becomes several counts. Which argument selects the count, and may one type's refusal change another type's count?

**Changed decision.** One counter becomes an array of independent counters, and the call argument selects which counter the invariant check applies to.

#### [Boundary] Rejected Calls (Author exercise)
<!-- id: sc-operation-traces-rejected-calls -->

**Prerequisites.** The Bounded Counter API and Design Parking System exercises above.

**Problem.** Design the class `Quota` with a capacity fixed by the constructor. `reserve(n)` returns `true` and adds `n` to the used amount when the used amount plus `n` does not exceed the capacity, and otherwise returns `false`. `cancel(n)` returns `true` and subtracts `n` from the used amount when `n` does not exceed the used amount, and otherwise returns `false`. `used()` returns the used amount. A call that returns `false` must leave every field exactly as it was.

**Constraints.** The limits are:
- **Capacity** is an `int` with `0 <= capacity <= 2^31 - 1`.
- **Amount** `n` is an `int` with `1 <= n <= 2^31 - 1`.
- **All or nothing** means a reservation never takes part of `n`.
- **Overflow** must not change an answer, even when the capacity equals `2^31 - 1`.

**Example 1.** Input calls `["Quota","reserve","reserve","cancel","cancel","used"]` with arguments `[[5],[3],[3],[4],[2],[]]`, output `[null,true,false,false,true,1]`.

**Example 2.** Input calls `["Quota","reserve","cancel","used"]` with arguments `[[0],[1],[1],[]]`, output `[null,false,false,0]`.

**Hint.** Which comparison avoids computing the sum of two large `int` values?

**Changed decision.** The focus moves from the accepting path to the refusing path: the precondition test must finish before the first field write, and it must not overflow.

#### [Recognize] Design an Ordered Stream (LeetCode 1656)
<!-- id: sc-operation-traces-ordered-stream -->

**Prerequisites.** The Rejected Calls exercise above.

**Problem.** Design the class `OrderedStream` for keys `1` to `n`. The constructor receives `n`. The call `insert(idKey, value)` stores the value for the key. That key has no value yet. It then returns the list of values for the longest run of consecutive keys that starts at the smallest key not yet returned and whose values are all stored. The list is empty when that smallest key has no stored value. The call returns every value exactly once.

**Constraints.** The limits are:
- **Count** `n` satisfies `1 <= n <= 1000`.
- **Key** satisfies `1 <= idKey <= n`, and each key is inserted at most once.
- **Value** is a string of 1 to 5 lowercase letters.
- **Order** of the returned list is increasing key order.

**Example 1.** Input calls `["OrderedStream","insert","insert","insert","insert"]` with arguments `[[4],[2,"b"],[1,"a"],[4,"d"],[3,"c"]]`, output `[null,[],["a","b"],[],["c","d"]]`.

**Example 2.** Input calls `["OrderedStream","insert","insert","insert"]` with arguments `[[3],[1,"x"],[3,"z"],[2,"y"]]`, output `[null,["x"],[],["y","z"]]`.

**Hint.** Which single index records the smallest key not yet returned, and where must it stop after one insertion?

**Changed decision.** The state is no longer a count. It is a stored array plus a pointer, and one insertion releases a whole contiguous suffix, not a single value.
