<!-- lesson-kind: standard -->
<!-- lesson-id: overflow -->
## Overflow

<!-- stage: context -->
### Why A Correct Total Turns Negative

A billing job adds 100,000 order amounts, each stored as an `int` number of cents. Every single amount is below 2.2 million. The job stores the total in a `long` variable, so the programmer expects room for any realistic sum. In production the report shows a negative revenue figure for one busy day, and no exception appears in the logs.

The program ran without error and still produced a wrong number. Java does not report an arithmetic result that is too large for its type. It silently keeps only the bits that fit. The question for this lesson is where in an expression the type of the result is decided, and how a program protects every step that can exceed it.

<!-- stage: naive -->
### Trusting The Destination Type

The direct approach declares the result as a `long` and assumes that the arithmetic on the right side uses `long` too. The three methods below follow that assumption.

```java
static long sumOfAmounts(int[] amounts) {
    int total = 0;
    for (int amount : amounts) {
        total += amount;                 // the running total is an int
    }
    return total;                        // the int converts to long only here
}

static long pairSum(int a, int b) {
    long result = a + b;                 // the destination is a long
    return result;
}

static int compareByDifference(int a, int b) {
    return a - b;                        // negative means a comes first
}
```

Each method reads naturally. For amounts such as 500 and 700, all three return the expected value. The assumption is that a wide variable on the left makes the work on the right wide as well.

<!-- stage: bottleneck -->
### Result Type Is Set Before Assignment

```predict
A program runs `int x = Integer.MAX_VALUE; long y = x + 1;`. What does y hold?

It holds -2147483648. The sum x + 1 has two int operands, so Java computes it as an int and the result does not fit. The conversion to long happens afterward and only copies the already wrong value.
```

#### Find Where Each Method Fails

The method `sumOfAmounts` costs O(n) and uses constant memory, so its cost is fine. Its flaw is the type of `total`, which is an `int`. Once the running total passes 2,147,483,647, the stored value jumps to a negative number, and the later `return` only converts that wrong value to `long`. The method `pairSum` fails the same way for `a = b = 2,000,000,000`, because the addition finishes as an `int` before the assignment starts. The method `compareByDifference` fails when `a` is large and positive and `b` is large and negative, because the difference exceeds the `int` range and flips its sign.

#### Why Tests Miss It

All three methods pass every small test. They fail only for values near the limits of the type, so a normal test set contains no failing case. A program cannot find these bugs by running more typical inputs. It needs a rule that protects the operation itself, and the rule must apply before the dangerous operation, because an operation that has already overflowed leaves no trace.

<!-- stage: insight -->
### Make The Operation Wide Before It Runs

#### Know What Wraparound Does

Java stores an `int` in 32 bits using two's complement, and it computes `int` arithmetic modulo 2^32. A result above 2,147,483,647 does not raise an error. It **wraps around** to a negative number, and this behavior is called wraparound. The sum `Integer.MAX_VALUE + 1` equals `Integer.MIN_VALUE`. The same happens for `long` at 2^63 - 1. The type of an arithmetic expression comes from its operands. The type of the variable that receives the result plays no role.

<!-- names: widening, wraparound, addExact -->

#### Apply Widening Before The Operation

**Widening** means converting an operand to a larger type, such as `long`, before the operation uses it. The expression `(long) a + b` widens `a`, so Java widens `b` as well and adds as `long`. The expression `(long) (a + b)` adds first as `int` and widens the finished sum, which is too late. A running total declared as `long total` widens every `int` amount at the moment it is added. The invariant of this lesson is that every operation whose true result can leave the range of its operand type must start with operands that are already wide enough.

#### Replace Subtraction With A Named Comparison

A comparator must return the sign of the comparison, not the difference. The call `Integer.compare(a, b)` returns a negative number, 0 or a positive number without subtracting, so it never wraps. The same idea covers negation. The value `-Integer.MIN_VALUE` equals `Integer.MIN_VALUE`, because +2,147,483,648 has no `int` representation. For that reason `Math.abs(Integer.MIN_VALUE)` stays negative. The safe form widens first: `Math.abs((long) x)`.

#### Test Before The Operation When No Wider Type Exists

A `long` sum of two `long` values can wrap as well, and no larger primitive type exists. The method `Math.addExact(a, b)` throws an `ArithmeticException` when the result does not fit, and it has partners for subtraction, multiplication and negation. When the program must return a defined value instead, it tests the condition before it computes. To append a digit `d` to a non-negative `int` value `r`, the product `r * 10 + d` fits exactly when `r < Integer.MAX_VALUE / 10`, or `r` equals `Integer.MAX_VALUE / 10` and `d` is at most 7.

<!-- stage: variables -->
### Quantities To Track In Each Operation

Track these items for every arithmetic step that might overflow.

- **operand type** is the declared type of each input, which sets the width of the operation.
- **true result** is the mathematical value, ignoring any limit.
- **limit** is the largest value of the operand type, for example `Integer.MAX_VALUE`.
- **widened operand** is an input that was converted to the larger type before the operation.

For the reverse-digits example in the trace, two more items matter. The variable `rev` holds the digits collected so far, and `digit` holds the next digit taken from the end of the input. The constant `Integer.MAX_VALUE / 10` is 214,748,364, and the largest last digit that still fits is 7. The check compares `rev` with that constant before any multiplication, so the check never needs a value that has already overflowed.

<!-- stage: trace -->
### Follow One Sum And One Digit Check

The first trace adds three `int` values with an `int` accumulator and a `long` accumulator side by side. The second trace reverses the digits of an `int` and stops at the step where the next multiplication would overflow.

#### Add Three Large Values

The values are 1,500,000,000, 1,500,000,000 and 100. The `long` accumulator tracks the true total. The `int` accumulator keeps only the low 32 bits of each result, so it shows what the naive method computes. After the second value the true total is 3,000,000,000, and the `int` accumulator holds a negative number, because 3,000,000,000 minus 2^32 is negative.

```trace
{"cells":[1500000000,1500000000,100],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"intSum":0,"longSum":0},"note":"Both accumulators start at 0."},{"at":{"i":0},"vars":{"intSum":1500000000,"longSum":1500000000},"note":"The value 1500000000 is added. The long accumulator holds the true total 1500000000. The int accumulator still agrees at 1500000000."},{"at":{"i":1},"vars":{"intSum":-1294967296,"longSum":3000000000},"note":"The value 1500000000 is added. The long accumulator holds the true total 3000000000. The int accumulator kept only the low 32 bits, so it holds -1294967296, which is wrong."},{"at":{"i":2},"vars":{"intSum":-1294967196,"longSum":3000000100},"note":"The value 100 is added. The long accumulator holds the true total 3000000100. The int accumulator kept only the low 32 bits, so it holds -1294967196, which is wrong."}]}
```

#### Reverse A Number And Stop At The Limit

The input is 1463847413, and the loop takes its digits from the end. Before each step the program compares `rev` with 214,748,364. For the first nine digits, `rev` stays at or below that limit, so the update `rev * 10 + digit` is safe. At the tenth digit, `rev` is 314,748,364, which exceeds the limit, so the method returns 0 without multiplying.

```trace
{"cells":[3,1,4,7,4,8,3,6,4,1],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"rev":0,"limit":214748364},"note":"No digit is taken yet. The check compares rev with 214748364 before every multiplication."},{"at":{"i":0},"vars":{"rev":3,"digit":3},"note":"The check passes. The update gives rev = 3."},{"at":{"i":1},"vars":{"rev":31,"digit":1},"note":"The check passes. The update gives rev = 31."},{"at":{"i":2},"vars":{"rev":314,"digit":4},"note":"The check passes. The update gives rev = 314."},{"at":{"i":3},"vars":{"rev":3147,"digit":7},"note":"The check passes. The update gives rev = 3147."},{"at":{"i":4},"vars":{"rev":31474,"digit":4},"note":"The check passes. The update gives rev = 31474."},{"at":{"i":5},"vars":{"rev":314748,"digit":8},"note":"The check passes. The update gives rev = 314748."},{"at":{"i":6},"vars":{"rev":3147483,"digit":3},"note":"The check passes. The update gives rev = 3147483."},{"at":{"i":7},"vars":{"rev":31474836,"digit":6},"note":"The check passes. The update gives rev = 31474836."},{"at":{"i":8},"vars":{"rev":314748364,"digit":4},"note":"The check passes. The update gives rev = 314748364. This is the ninth digit, so the next step is the decisive one."},{"at":{"i":9},"vars":{"rev":314748364,"digit":1},"note":"The value rev is 314748364, which is above 214748364. Multiplying by 10 would leave the int range, so the method returns 0."}]}
```

<!-- stage: code -->
### Implement The Safe Forms

```java
final class SafeNumerics {
    static long sumOfAmounts(int[] amounts) {
        long total = 0;                         // a long accumulator widens each amount as it is added
        for (int amount : amounts) {
            total += amount;                    // long plus int is computed as long
        }
        return total;
    }

    static int compareSafely(int a, int b) {
        return Integer.compare(a, b);           // returns the sign without subtracting
    }

    static long absoluteValue(int x) {
        return Math.abs((long) x);              // widen first, so MIN_VALUE has a positive form
    }

    static int reverseDigits(int x) {
        int rev = 0;
        while (x != 0) {
            int digit = x % 10;                 // the remainder keeps the sign of x
            x /= 10;
            if (rev > Integer.MAX_VALUE / 10 || (rev == Integer.MAX_VALUE / 10 && digit > 7)
                    || rev < Integer.MIN_VALUE / 10 || (rev == Integer.MIN_VALUE / 10 && digit < -8)) {
                return 0;                       // multiplying by 10 and adding the digit would leave the int range
            }
            rev = rev * 10 + digit;             // the multiplication is now safe
        }
        return rev;
    }
}
```

The method `reverseDigits` handles negative inputs without a branch, because `x % 10` and `x /= 10` keep the sign of `x`. Its check has four parts. Two parts cover a value that is already past the limit of `rev * 10`, and two parts cover a value exactly at that limit, where the last digit decides. The limit digits are 7 for the positive side and -8 for the negative side. The sum method costs O(n) time, and the digit loop costs O(log x) time. Every method uses O(1) extra memory.

<!-- stage: applicability -->
### When Overflow Needs Care

#### Recognize The Pattern

Check every arithmetic step whose inputs can reach about half the range of the type. Common cases are sums over many values, products of two sizes, midpoints of two large indexes, differences used as comparator results and negation of a value that can be the minimum. The invariant to state before coding is that the operation starts with operands wide enough to hold the true result, or the program has proven that the result fits. A check after the operation proves nothing, because the wrapped value looks like any other number.

Constraints in a problem statement decide the question. A bound such as 10^5 values below 10^9 gives a sum up to 10^14, which needs `long`. Two values up to 10^9 multiply to 10^18, which still fits in a `long` but not in an `int`.

#### Watch For The Nearest False Friend

The assignment `long y = a * b` is the false friend. It looks safe because the variable is wide, yet the multiplication already finished as an `int`. A second false friend is the compound assignment `int s += someLong`, which compiles without a warning because Java inserts a narrowing cast. Use `BigInteger` only when no primitive width is enough, since it costs far more per operation than `long`.

#### Avoid The Java Rounding And Cast Traps

A cast applies to the nearest operand only. In `(long) a * b` the cast binds to `a`, and in `(long) (a * b)` it binds to the finished product. The `char` and `short` types widen to `int` in arithmetic, so a sum of two `short` values never wraps at 16 bits, and a store back into a `short` truncates silently. Integer division and remainder truncate toward zero, so `-7 / 2` is -3 and `-7 % 2` is -1. For the midpoint of two indexes, write `low + (high - low) / 2`, which stays inside the range when both indexes are non-negative.

<!-- stage: exercises -->
### Exercises

#### [Build] Int Sum Into Long (Author exercise)
<!-- id: bt06-sum-into-long -->

**Prerequisites.** The result type rule and the long accumulator from this lesson.

**Problem.** Given an array `a` of `int` values, return the exact mathematical sum of all elements. The empty array has sum 0.

**Constraints.** The limits are:
- **Length** of `a` is an `int` with `0 <= n <= 10^5`.
- **Values** are any `int` values, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Return** is a `long`.
- **Mutation** of `a` is not allowed.

**Example 1.** Input `a = [2147483647,2147483647,5]`, output 4294967299, while an `int` accumulator would end at 3.

**Example 2.** Input `a = [-2147483648,-2147483648]`, output -4294967296, which is far below the `int` range.

**Hint.** Which type must the running total have, so that adding an `int` never wraps?

**Changed decision.** Baseline case: the accumulator is declared wide, so each addition happens in `long`.

#### [Vary] Safe Comparator (Author exercise)
<!-- id: bt06-safe-comparator -->

**Prerequisites.** The previous exercise and the comparison rule from this lesson.

**Problem.** Given an array of integer pairs, sort it by the first number in ascending order. Pairs with equal first numbers go by the second number in descending order. Return the sorted array.

**Constraints.** The limits are:
- **Pairs** number at most 10^4.
- **Numbers** are any `int` values, including the extreme values of the type.
- **Ties** in both numbers keep any order.
- **Return** is the sorted `int[][]`, and the input array may be sorted in place.

**Example 1.** Input `[[2147483647,1],[-2147483648,5],[2147483647,9],[0,3]]`, output `[[-2147483648,5],[0,3],[2147483647,9],[2147483647,1]]`. A subtraction comparator mis-orders `2147483647` and `-2147483648`.

**Example 2.** Input `[[5,2],[5,7],[-1,0]]`, output `[[-1,0],[5,7],[5,2]]`, because the two pairs with first number 5 go by second number 7 and then 2.

**Hint.** What does a comparator return, and why can a plain subtraction give the wrong sign?

**Changed decision.** The operation changes from adding to comparing, so the safe form replaces subtraction with `Integer.compare`.

#### [Boundary] MIN_VALUE Negation (Author exercise)
<!-- id: bt06-min-value-negation -->

**Prerequisites.** The two exercises above.

**Problem.** Given an `int` value `x`, return its absolute value `|x|` as a `long`. The result for `x = Integer.MIN_VALUE` must be the positive number 2,147,483,648.

**Constraints.** The limits are:
- **`x`** is any `int` value.
- **Return** is a `long` that is never negative.

**Example 1.** Input `x = -2147483648`, output 2147483648, since negating in `int` would return the same negative value.

**Example 2.** Input `x = -7`, output 7.

**Hint.** What does negating the smallest `int` return, and where should the conversion to `long` happen?

**Changed decision.** The boundary case is the one value whose negation has no `int` form, so the widening must come first.

#### [Recognize] Reverse Digits Of An Integer (LeetCode 7)
<!-- id: bt06-reverse-digits -->

**Prerequisites.** All three exercises above.

**Problem.** Given a signed 32-bit integer `x`, return the integer whose decimal digits are those of `x` in reverse order, with the sign of `x` kept. If the result lies outside the 32-bit signed range, return 0. The solution uses only `int` variables and no `long`, so each step must test the range before it multiplies.

**Constraints.** The limits are:
- **`x`** is an `int` with `-2^31 <= x <= 2^31 - 1`.
- **Trailing zeros** of `x` vanish in the result.
- **Return** is an `int`.
- **Types** allowed for variables are `int` only.

**Example 1.** Input `x = 1463847412`, output 2147483641, which sits just below the limit because the last digit 1 is at most 7.

**Example 2.** Input `x = 2046384125`, output 0, because the reversed number 5214836402 is above 2147483647.

**Hint.** Which test on the digits collected so far tells whether the next multiplication and addition still fit?

**Changed decision.** The input has no wider type to fall back on, so the check moves before the multiplication.
