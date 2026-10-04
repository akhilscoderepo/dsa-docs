<!-- lesson-kind: standard -->
<!-- lesson-id: call-state -->
## Call State

<!-- stage: context -->
### The Relay Of The Ferry Ticket Desks

The ferry company of Harrow Bay runs a chain of ticket desks along the quay, and every evening the manager wants one number: how many passengers boarded in total. She does not walk the quay. She phones the last desk and says, "Report the total for the first forty crossings." The clerk there notes down the crossing that is his own, phones the desk before him, and asks the same question about the first thirty-nine. Each clerk adds one figure and passes a shorter question down the line, until a clerk is asked about zero crossings, who answers zero at once without phoning anyone.

The answers then travel back up the quay, each clerk adding the figure he wrote down, and the manager hears the total. The manager notices that the whole system works only because each question is exactly like the one before it, just smaller, and that the line ends because the numbers on the questions get smaller.

<!-- stage: naive -->
### Multiply One Step At A Time

The ferry company also prices its season passes by compounding a fare factor. A pass is repriced by multiplying a starting factor by a growth rate once for every month of the season. The direct method does exactly that, with a loop that multiplies the running result by the rate, one month at a time.

```java
static double repricePass(double rate, int months) {
    double result = 1.0;
    for (int m = 0; m < months; m++) result *= rate;
    return result;
}
```

The loop is plainly correct, it follows the description of the problem, and it is a good oracle for anything cleverer. For a season of twelve months it is all anyone needs.

<!-- stage: bottleneck -->
### Two Billion Months Of Multiplying

The loop performs `months` multiplications, so its cost is O(n) in the exponent, and the exponent of a Java `int` can reach about two billion. A pricing service that repeats the loop for a long horizon spends nearly all of its time re-multiplying the same rate. The work is also wasteful in a structural way: the product for forty months contains the product for twenty months twice over, and the loop computes that twenty-month product from scratch, then forgets it, then builds it again.

The loop cannot see this because it has no notion of a smaller problem of the same kind. It only knows one more multiplication. A method that could ask itself for the twenty-month answer once, and then use it twice, would need only about thirty-one levels of asking for any `int` exponent, which is O(log n) multiplications instead of two billion.

<!-- stage: insight -->
### Describe The Problem By Its Parameters

A recursive method is a promise about a **call state**, which is the small set of parameters that fully identifies one subproblem, here the pair of a rate and an exponent. Two calls with equal parameters ask the same question, and the method's contract says exactly what each call returns: "the rate raised to this exponent". Everything the method needs must travel in that state or be fixed for the whole run, so a call can be understood without looking at who made it.

A call must also have a **base case**, an input so small that the answer is written down directly, such as an exponent of zero returning one. Without it the method has no way to stop asking, and with a wrong base value every answer above it is wrong in a consistent, hard-to-see way.

The third part is a **shrinking measure**: some number built from the call state that is strictly smaller in every recursive call and cannot go below the base case. Halving the exponent works, because an exponent that is cut in half each time reaches zero after about thirty-one calls. The recursive step then uses the answer of the smaller call, and a half-sized answer squared is the full answer, so the smaller call is made once and reused.

The invariant is that every call's contract is the same sentence with different parameters, and each recursive call is strictly closer to a base case than its caller.

<!-- names: call state, base case, shrinking measure -->

<!-- stage: variables -->
### Rate, Exponent And Half Result

The `rate` never changes during a run and is the same in every call. The `exponent` is the number that shrinks, and it is the whole of what makes one call different from another. The value `half` is local to one call: it holds the answer returned by the smaller call, and it exists only after that call comes back. The method's return value is the answer to the call's own contract, and for an odd exponent it is `half * half * rate`, for an even one `half * half`. The stack of waiting calls is the memory of the pending work, with one frame per level of halving.

<!-- stage: trace -->
### Halving An Exponent Down To Zero

The first trace follows the price of a rate of 2 over an exponent of 10. Each cell holds the exponent of the call at that depth, and the pointer `depth` marks which call is running. The calls go down until the exponent reaches zero and then the answers travel back up, each one built from the answer below it.

```trace
{"cells":["10","5","2","1","0"],"pointers":["depth"],"steps":[{"at":{"depth":0},"vars":{"exponent":10,"answer":"waiting"},"note":"The call for exponent 10 is not a base case, so it asks the same question for exponent 5 and waits."},{"at":{"depth":1},"vars":{"exponent":5,"answer":"waiting"},"note":"The call for exponent 5 is not a base case, so it asks the same question for exponent 2 and waits."},{"at":{"depth":2},"vars":{"exponent":2,"answer":"waiting"},"note":"The call for exponent 2 is not a base case, so it asks the same question for exponent 1 and waits."},{"at":{"depth":3},"vars":{"exponent":1,"answer":"waiting"},"note":"The call for exponent 1 is not a base case, so it asks the same question for exponent 0 and waits."},{"at":{"depth":4},"vars":{"exponent":0,"answer":1},"note":"The exponent is zero, which is the base case, so the call answers 1 without asking anything."},{"at":{"depth":3},"vars":{"exponent":1,"answer":2},"note":"The half result is back, so the call for exponent 1 squares it and multiplies by the rate once more, answering 2."},{"at":{"depth":2},"vars":{"exponent":2,"answer":4},"note":"The half result is back, so the call for exponent 2 squares it, answering 4."},{"at":{"depth":1},"vars":{"exponent":5,"answer":32},"note":"The half result is back, so the call for exponent 5 squares it and multiplies by the rate once more, answering 32."},{"at":{"depth":0},"vars":{"exponent":10,"answer":1024},"note":"The half result is back, so the call for exponent 10 squares it, answering 1024."}]}
```

The second trace is a different kind of shrinking. A method totals the first `k` figures of an array by taking the last of them and asking for the total of the first `k - 1`. The pointer `k` is the call state, and the base case is the call with `k` equal to zero, which returns zero without looking at the array.

```trace
{"cells":["3","1","4","1"],"pointers":["k"],"steps":[{"at":{"k":4},"vars":{"returned":"waiting"},"note":"The call for k = 4 must add a[3] = 1 to the total of the first 3 figures, so it asks for that total."},{"at":{"k":3},"vars":{"returned":"waiting"},"note":"The call for k = 3 must add a[2] = 4 to the total of the first 2 figures, so it asks for that total."},{"at":{"k":2},"vars":{"returned":"waiting"},"note":"The call for k = 2 must add a[1] = 1 to the total of the first 1 figures, so it asks for that total."},{"at":{"k":1},"vars":{"returned":"waiting"},"note":"The call for k = 1 must add a[0] = 3 to the total of the first 0 figures, so it asks for that total."},{"at":{"k":0},"vars":{"returned":0},"note":"The count is zero, which is the base case, so the call returns 0 without reading the array."},{"at":{"k":1},"vars":{"returned":3},"note":"The smaller total is back, so the call for k = 1 returns 0 + 3 = 3."},{"at":{"k":2},"vars":{"returned":4},"note":"The smaller total is back, so the call for k = 2 returns 3 + 1 = 4."},{"at":{"k":3},"vars":{"returned":8},"note":"The smaller total is back, so the call for k = 3 returns 4 + 4 = 8."},{"at":{"k":4},"vars":{"returned":9},"note":"The smaller total is back, so the call for k = 4 returns 8 + 1 = 9."}]}
```

<!-- stage: code -->
### Power By Halving

```java
static double power(double rate, int exponent) {
    if (exponent == 0) return 1.0;          // base case, written down directly
    double half = power(rate, exponent / 2); // smaller call, made once
    return (exponent % 2 == 0) ? half * half : half * half * rate;
}

static double prefixTotal(int[] a, int k) {
    if (k == 0) return 0;                    // empty prefix has no figures
    return prefixTotal(a, k - 1) + a[k - 1];
}
```

Both methods are written for a nonnegative second parameter, and each rests on the shrinking measure. The first runs in O(log n) time with a stack of the same depth, and the second takes a linear number of calls and a linear stack for a prefix of length k.

<!-- stage: applicability -->
### When The Problem Contains Itself

Look for recursion when the problem can be restated about a smaller version of itself, and when the number of parameters needed to describe a version is small enough to write in a signature. Totals over prefixes, powers, nested structures that are defined in terms of smaller copies of themselves, and every method in the rest of this chapter share that shape. The invariant to keep in mind is that each call's contract is the same sentence and each call moves toward a base case.

The nearest false friend is a method that calls itself with unchanged or growing parameters. It looks recursive and has a base case written in the code, but the measure never shrinks, so the base case is never reached and the loop has simply moved to the call stack, where it ends in an error instead of a hang. A second false friend is recursion used where a plain loop is clearer, such as walking an array one element at a time in a long input. Java does not remove the frames of waiting calls, so a prefix method over a million elements can run out of stack, and an explicit loop is the better tool there.

Do not use recursion when the depth of the calls grows with the input and the input may be large, unless the depth is bounded by a logarithm as it is for the power method. Also check what the narrowest value of the parameter does before negating or halving it, because a negative exponent or the most negative `int` changes the arithmetic of the shrinking step.

<!-- stage: exercises -->
### Exercises

#### [Build] Sum A Prefix (Author exercise)
<!-- id: bt-sum-prefix -->

**Prerequisites.** The idea of a subproblem with a base case and a shrinking number.

**Problem.** Given an array `a` of integers and a count `k`, return the total of the first `k` elements, using a method that calls itself with `k - 1` and never uses a loop. A `k` of zero gives zero.

**Constraints.** 0 <= k <= a.length <= 2000, and each value is between -10^6 and 10^6.

**Example 1.** Input `a = [3, 1, 4, 1, 5]`, `k = 3`, output `8`.

**Example 2.** Input `a = [7, 2]`, `k = 0`, output `0`.

**Hint.** What is the smallest prefix whose total needs no array access, and what does the call for `k` hand to the call for `k - 1`?

**Changed decision.** The answer of the smaller call is built on, and the base case supplies a value that does not depend on the array at all.

#### [Vary] Power By Halving (LeetCode 50)
<!-- id: bt-power-halving -->

**Prerequisites.** The Sum A Prefix rung, and the idea that a half-sized answer can be reused.

**Problem.** Given a real number `x` and a nonnegative integer `n`, return a pair: `x` raised to `n`, and the number of calls the method made, counting the first one. The method may call itself once per level, with the exponent `n / 2`, and must reuse the result of that call.

**Constraints.** 0 <= n <= 2^31 - 1, and x is between -3.0 and 3.0.

**Example 1.** Input `x = 2.0`, `n = 10`, output `[1024.0, 5]`.

**Example 2.** Input `x = 3.0`, `n = 0`, output `[1.0, 1]`.

**Hint.** If the half-sized call is made twice instead of once, how many calls does an exponent of 2^30 cost?

**Changed decision.** The shrink steps from one less to one half, so the count of calls drops from linear to logarithmic.

#### [Boundary] Zero And Negative Exponents (Author exercise)
<!-- id: bt-negative-exponent -->

**Prerequisites.** The Power By Halving rung.

**Problem.** Given a nonzero real number `x` and any `int` exponent `n`, return `x` raised to `n`. A negative exponent means the reciprocal of the positive power. The most negative `int` must work, and `x = 0` is never given.

**Constraints.** -2^31 <= n <= 2^31 - 1, and x is a nonzero real number between -2.0 and 2.0. Results that are too small to represent are returned as 0.0.

**Example 1.** Input `x = 2.0`, `n = -2`, output `0.25`.

**Example 2.** Input `x = -1.0`, `n = -2147483648`, output `1.0`.

**Hint.** What does `-n` produce when `n` is the most negative `int`, and where should the conversion to a wider type happen?

**Changed decision.** The exponent is widened to a `long` before it is negated, so the shrinking measure stays nonnegative for every input.

#### [Recognize] Recursive String Reversal By Range (Author exercise)
<!-- id: bt-reverse-range -->

**Prerequisites.** The Zero And Negative Exponents rung and the habit of naming the shrinking measure.

**Problem.** Given a string `s` and two indexes `lo` and `hi`, return `s` with the characters from `lo` to `hi` inclusive in reverse order. Work on a single character array with a method that swaps the two ends and calls itself on the interval strictly inside them, and never builds substrings. If `lo >= hi` the string is returned unchanged.

**Constraints.** 0 <= lo, hi < s.length() <= 5000, and s has lowercase letters only.

**Example 1.** Input `s = "abcde"`, `lo = 0`, `hi = 4`, output `"edcba"`.

**Example 2.** Input `s = "river"`, `lo = 3`, `hi = 1`, output `"river"`.

**Hint.** Which number gets smaller on every call, and what two shapes of interval stop the recursion, one of even length and one of odd length?

**Changed decision.** The state is an interval of two indexes rather than a single count, and the base case is any interval with fewer than two characters.
