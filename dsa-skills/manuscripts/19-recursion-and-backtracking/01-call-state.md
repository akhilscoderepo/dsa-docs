<!-- lesson-kind: standard -->
<!-- lesson-id: call-state -->
## Shrink The Problem With Each Call

<!-- stage: context -->
### Why A Sum Method Overflows The Stack

A reporting job adds up the sizes of the files in one list. A developer writes a method that adds the first value to the sum of the rest, and the method calls itself to get the sum of the rest. The first test with three values passes. The next test, with an empty list, crashes with `StackOverflowError`. A third version of the method passes the same position to every call, so it also crashes on the three-value list.

Both crashes have one cause. The call does not say which part of the list it is responsible for, or the part does not get smaller. This lesson asks what a call must receive and promise so that every recursive call works on a strictly smaller task and the chain of calls ends.

<!-- stage: naive -->
### Copying The Rest Of The Array

The direct plan builds the smaller task as a new array. Each call removes the first value, copies the remaining values and passes the copy to the next call.

```java
static long sumByCopy(int[] a) {
    if (a.length == 0) return 0;                                   // an empty array adds up to zero
    int[] rest = Arrays.copyOfRange(a, 1, a.length);               // a new array without the first value
    return a[0] + sumByCopy(rest);                                 // the first value plus the sum of the rest
}
```

The method returns the correct sum for every array. Each call allocates a fresh array one value shorter than its input.

<!-- stage: bottleneck -->
### Counting The Copies And The Calls

```predict
An array holds n = 100,000 values. About how many values do all the copies in one call of sumByCopy move, and how many calls wait on the stack at the deepest point?

The copies move n - 1, then n - 2, then n - 3 values and so on, about n * n / 2 = 5 billion values in total. The calls form one chain of n + 1 calls, and each call waits for the next one, so 100,001 calls wait at the deepest point. A default Java stack holds far fewer frames than that, so the method crashes.
```

The copies make the time O(n^2) for a sum that one loop computes in O(n). The extra arrays also hold O(n^2) values over the whole run, although the garbage collector frees them one by one.

The copies exist only because the method passes the smaller task as data. Two numbers can name the task instead, because they locate it inside the original array. Then no call copies anything, and the cost per call falls to O(1) time and O(1) extra memory. The chain of n + 1 calls still uses O(n) stack memory, and the lesson returns to that cost below.

<!-- stage: insight -->
### Giving Every Call A Contract

A recursive method needs three things, and a missing one produces the crashes from the opening.

#### Fixing What One Call Knows

The values that a call receives are its **call state**. For the sum, the state is the array and one index `i`. The array stays the same in every call, and `i` is the only value that changes. The state must contain enough information that the call needs nothing else.

#### Stating What One Call Promises

The **subproblem contract** says what the call returns when it receives a given state. For the sum, `sum(a, i)` returns the sum of `a[i]` up to the last value, and it returns 0 when `i` equals `a.length`. A caller may trust the contract without reading the code of the callee. This trust lets a reader prove the method one call at a time.

#### Stopping The Chain

The **base case** is a state that the method answers directly, without a recursive call. Every recursive call must move its state closer to a base case. The call `sum(a, i + 1)` moves `i` toward `a.length`, so the chain ends after `a.length - i` calls. A call that passes `i` again, or `i - 1`, never reaches the base case.

<!-- names: call state, subproblem contract, base case -->

<!-- stage: variables -->
### The Pieces Of State

One method holds all state of the sum.

- **Array a** holds the values, and no call changes it.
- **Index i** is the first position that the current call must add.
- **Result** is the value that the call returns, which equals the sum of `a[i..n)`.

Each call increases `i` by one. The call with `i == a.length` returns 0 and starts the return phase. Every call on the stack then adds its own `a[i]` to the value it receives.

<!-- stage: trace -->
### Following The Calls Down And Back

#### Summing A Short Array

The first trace runs `sum(a, 0)` on the array `[4, 1, 3]`. The pointer `i` marks the index of the current call. The variable `phase` says whether the call is still going down or has started to return, and `value` shows what the call returns.

The first three calls each wait for the next call, so they have no value yet. The fourth call has `i == 3`, which equals the array length, so it returns 0. The return phase then runs in reverse order. The call with `i == 2` returns 3 plus 0. The call with `i == 1` returns 1 plus 3. The call with `i == 0` returns 4 plus 4.

#### Halving An Exponent

The second trace computes 2 to the power 10 with a call state that holds one exponent. Each call asks for half of its exponent, so the exponents run 10, 5, 2, 1, 0. The cells show the exponent of each call. The pointer `d` marks the depth of the call. A call with an odd exponent multiplies the squared half result once more by the base.

#### Stepping Through Both Runs

```trace
{"cells":["4","1","3"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"phase":"down","value":"waiting"},"note":"The call for i = 0 must add a[0] = 4 to the sum of the range that starts at 1, so it calls sum with i = 1."},{"at":{"i":1},"vars":{"phase":"down","value":"waiting"},"note":"The call for i = 1 must add a[1] = 1 to the sum of the range that starts at 2, so it calls sum with i = 2."},{"at":{"i":2},"vars":{"phase":"down","value":"waiting"},"note":"The call for i = 2 must add a[2] = 3 to the sum of the range that starts at 3, so it calls sum with i = 3."},{"at":{"i":3},"vars":{"phase":"return","value":0},"note":"The call for i = 3 equals the array length, so it matches the base case and returns 0 without a further call."},{"at":{"i":2},"vars":{"phase":"return","value":3},"note":"The call for i = 2 adds a[2] = 3 to the received value 0 and returns 3."},{"at":{"i":1},"vars":{"phase":"return","value":4},"note":"The call for i = 1 adds a[1] = 1 to the received value 3 and returns 4."},{"at":{"i":0},"vars":{"phase":"return","value":8},"note":"The call for i = 0 adds a[0] = 4 to the received value 4 and returns 8."}]}
```

```trace
{"cells":["10","5","2","1","0"],"pointers":["d"],"steps":[{"at":{"d":0},"vars":{"exponent":10,"value":"waiting"},"note":"The call with exponent 10 is not the base case, so it asks for the power with exponent 5."},{"at":{"d":1},"vars":{"exponent":5,"value":"waiting"},"note":"The call with exponent 5 is not the base case, so it asks for the power with exponent 2."},{"at":{"d":2},"vars":{"exponent":2,"value":"waiting"},"note":"The call with exponent 2 is not the base case, so it asks for the power with exponent 1."},{"at":{"d":3},"vars":{"exponent":1,"value":"waiting"},"note":"The call with exponent 1 is not the base case, so it asks for the power with exponent 0."},{"at":{"d":4},"vars":{"exponent":0,"value":1},"note":"The call with exponent 0 matches the base case and returns 1."},{"at":{"d":3},"vars":{"exponent":1,"value":2},"note":"The call with exponent 1 squares the half result 1 and multiplies by 2 because 1 is odd, so it returns 2."},{"at":{"d":2},"vars":{"exponent":2,"value":4},"note":"The call with exponent 2 squares the half result 2, because 2 is even, so it returns 4."},{"at":{"d":1},"vars":{"exponent":5,"value":32},"note":"The call with exponent 5 squares the half result 4 and multiplies by 2 because 5 is odd, so it returns 32."},{"at":{"d":0},"vars":{"exponent":10,"value":1024},"note":"The call with exponent 10 squares the half result 32, because 10 is even, so it returns 1024."}]}
```

<!-- stage: code -->
### Writing The Methods In Java

#### The Sum With An Index

The method below follows the contract of the lesson. The array never changes, and the call state is the index.

```java
static long sum(int[] a, int i) {
    if (i == a.length) return 0;                    // base case: no value remains
    return a[i] + sum(a, i + 1);                    // the next call owns a strictly shorter range
}
```

#### The Power With A Half Exponent

The second method gives the exponent a call state that halves in each call. The variable `half` holds the contract result for the exponent `n / 2`.

```java
static double power(double x, int n) {              // contract: returns x^n for n >= 0
    if (n == 0) return 1.0;                         // base case: any value to the power 0 is 1
    double half = power(x, n / 2);                  // n / 2 is strictly smaller than n when n > 0
    return n % 2 == 0 ? half * half : half * half * x;   // an odd exponent needs one more factor
}
```

#### Cost Of The Calls

The sum makes n + 1 calls and holds n + 1 frames on the stack at the deepest point, so it costs O(n) time and O(n) stack space. The power halves the exponent and makes about log2(n) + 1 calls, so it costs O(log n) time and O(log n) stack space.

<!-- stage: applicability -->
### Recognizing A Shrinking Subproblem

#### Spotting The Pattern

The cue is a task that splits into a smaller task of the same shape, which a few numbers describe. The invariant is that every call has a stated contract and passes a state that is strictly closer to a base case.

#### Finding The False Friend

The false friend is a call that looks smaller and is not. The call `sum(a, i)` inside `sum(a, i)` never moves, and the call `power(x, n)` inside `power(x, n)` never halves. The stack grows until it overflows, and the failure looks like a deep problem, although the fault is a state that does not change. A second false friend is a copy of the data that stands in for the state, which the naive plan used.

#### Recognizing The No-Go Cases

Plain recursion does not fit when the chain is as long as the input and the input is large. A list of 10^5 values already risks a stack overflow in Java, and one loop avoids that risk. It also does not fit when two different calls reach the same state many times, because the program repeats work. A later chapter handles that case.

<!-- stage: exercises -->
### Exercises

#### [Build] Sum A Prefix (Author exercise)
<!-- id: bt-sum-a-prefix -->

**Prerequisites.** The call state, the subproblem contract and the base case of this lesson.

**Problem.** Given an integer array `a` and an integer `k` with `0 <= k <= a.length`, return the sum of the first `k` values of `a`. Define the method `prefix(a, k)` so that it returns that sum and so that it calls itself with a smaller value of `k`.

**Constraints.** The limits are:
- **Length** is `0 <= a.length <= 5000`.
- **Values** are `-10^6 <= a[i] <= 10^6`.
- **Return** is a `long`.
- **Mutation** does not occur; `a` keeps its contents.

**Example 1.** Input `a = [4, 1, 3, 5]` and `k = 3`, output 8.

**Example 2.** Input `a = [7, -2]` and `k = 0`, output 0.

**Hint.** Which state is the smallest one that has an answer without a recursive call? Which value of `k` does the next call receive?

**Changed decision.** The state is a prefix length, so the base case sits at the start of the array and not at the end.

#### [Vary] Pow(x, n) (LeetCode 50)
<!-- id: bt-pow-halving -->

**Prerequisites.** The previous exercise and the halving trace of this lesson.

**Problem.** Given a real number `x` and an integer `n` with `n >= 0`, return `x` raised to the power `n`. The input never asks for a negative exponent. Use a recursive method whose call state holds only `x` and the current exponent, and make each call use half of the exponent of its caller.

**Constraints.** The limits are:
- **Base** is `-10, 10` as a real number, and `x` may be 0.
- **Exponent** is `0 <= n <= 2^31 - 1`.
- **Result** fits in a `double` for every input of the tests.
- **Zero** to the power 0 equals 1.

**Example 1.** Input `x = 2`, `n = 10`, output 1024.

**Example 2.** Input `x = 0`, `n = 0`, output 1.

**Hint.** How many calls does an exponent of 2^31 - 1 need if each call halves it? Which exponents need an extra factor of `x`?

**Changed decision.** The state shrinks by half and not by one, so the depth falls from n to about log2(n).

#### [Boundary] Zero And Negative Exponents (Author exercise)
<!-- id: bt-negative-exponents -->

**Prerequisites.** The two exercises above.

**Problem.** Given a real number `x` with `x != 0` and any `int` exponent `n`, return `x` raised to the power `n`. A negative exponent means `1 / x^(-n)`. The method must return a correct value for `n = Integer.MIN_VALUE`, whose negation does not fit in an `int`.

**Constraints.** The limits are:
- **Base** is `0.5 <= |x| <= 2`, and `x` is never 0.
- **Exponent** is any `int`, including `Integer.MIN_VALUE`.
- **Result** may underflow to 0 or overflow to infinity, and the method returns that `double` value.
- **Types** use `long` for the exponent inside the method.

**Example 1.** Input `x = 2`, `n = -3`, output 0.125.

**Example 2.** Input `x = 1`, `n = -2147483648`, output 1.

**Hint.** What does `-Integer.MIN_VALUE` evaluate to in `int` arithmetic? Which type holds the exponent before the first negation?

**Changed decision.** The call state now holds a wider exponent type, because one `int` value has no negation of the same type.

#### [Recognize] Recursive String Reversal By Range (Author exercise)
<!-- id: bt-reverse-by-range -->

**Prerequisites.** The previous three exercises.

**Problem.** Given a `char` array `s`, reverse its contents in place with a recursive method `rev(s, lo, hi)`. The contract is that the call reverses the values at positions `lo` through `hi` inclusive. The method may not copy any part of the array and may not create a substring.

**Constraints.** The limits are:
- **Length** is `0 <= s.length <= 5000`.
- **Characters** are any `char` values.
- **Range** starts at `lo = 0` and `hi = s.length - 1`, so an empty array has `hi = -1`.
- **Mutation** changes `s` in place, and the method returns nothing.

**Example 1.** Input `s = ['a','b','c','d']`, output `['d','c','b','a']` as the new contents of `s`.

**Example 2.** Input `s = ['x']`, output `['x']` as the unchanged contents of `s`.

**Hint.** Which two ranges need no work at all? What do the positions `lo + 1` and `hi - 1` describe?

**Changed decision.** Two indices describe one range, and each call shrinks the range from both ends.
