<!-- lesson-kind: standard -->
<!-- lesson-id: binary-arithmetic -->
## Binary Arithmetic

<!-- stage: context -->
### Adding Numbers Without A Plus Operator

A hardware simulator models a processor out of logic gates. Its gates compute AND, OR, XOR and shifts, and nothing else. The simulator still has to add two 32-bit integers, and it has no adder to call. Interview questions pose the same puzzle in another form: return the sum of two integers without using the plus or minus operator.

The plus operator is a convenience, because a circuit builds addition from simpler gates, and a program can build it from the same pieces. This lesson asks how bitwise operations alone produce the sum of two integers, negative ones included, and how the computation knows when to stop.

<!-- stage: naive -->
### Counting Up One Step At A Time

The direct idea is to count. Start from `a` and add one, `b` times. Each step moves the total by exactly one, so the loop looks correct.

```java
static int addByCounting(int a, int b) {
    for (int i = 0; i < b; i++) {
        a++;                    // one more unit of b has been added to the total
    }
    return a;
}
```

The loop treats `b` as a number of steps. Each increment is a tiny sum, so the loop also needs an adder under the hood and only moves the problem to a smaller size. The method returns the right answer for small non-negative `b`.

<!-- stage: bottleneck -->
### Counting Takes O(b) Steps And Breaks

```predict
A program adds a = 5 and b = 2,000,000,000 by counting. About how many loop iterations run? What does the loop return for a = 5 and b = -3?

About two billion iterations, because the loop body runs once for every unit of b. For b = -3 the test i < b is false at the start, so the loop never runs and the method returns 5. The correct sum is 2.
```

#### Count The Steps

The loop runs `b` times, so its cost is O(b). A 32-bit `b` reaches 2,147,483,647, which means billions of iterations for one addition. A sum that a processor finishes in one instruction becomes a multi-second loop.

#### Check The Negative Case

A negative `b` makes the loop condition false before the first step. The method then ignores `b` completely and returns `a`. Fixing that needs a second loop that counts down, and the result still costs O(|b|) steps. A correct method must handle all columns of the binary numbers at once and must not depend on how large the value of `b` is.

<!-- stage: insight -->
### Separate The Sum From The Carries

#### Add One Column

A **half adder** is the circuit that adds two single bits. It produces a sum bit and a carry bit. The sum bit is the XOR of the inputs, which is 1 when exactly one input is 1. The carry bit is the AND of the inputs, which is 1 only when both inputs are 1. The case 1 + 1 gives sum bit 0 and carry bit 1, which is the binary number `10`.

<!-- names: half adder, carry word, fixed width -->

#### Add Every Column At Once

An `int` holds 32 columns, and the half adder rule applies to all of them in parallel. The expression `a ^ b` holds the sum bit of every column, and it ignores incoming carries. The expression `(a & b) << 1` is the **carry word**. It holds the carry bit of every column, moved one column to the left, because a carry belongs to the next column. The true total equals `(a ^ b)` plus the carry word. That statement is the same addition problem with different operands. For 3 + 1, the sum word `a ^ b` is `10`, which is 2, and the carry word is also `10`. The two words add up to 4, which is the true total.

#### Repeat Until The Carry Word Is Zero

Compute the new sum word `a ^ b` and the new carry word `(a & b) << 1` from the current `a` and `b`. Then store the sum word in `a` and the carry word in `b`, so the carry word still uses the old `a`. Repeat. The invariant is that `a + b` keeps the same value after each round. When `b` becomes 0, nothing is left to add, and `a` holds the answer.

The loop terminates because every round pushes the carry word upward. Let `p` be the position of the lowest set bit of `b`. The new carry word comes from `a & b`, which has set bits only where `b` has set bits, and the shift moves each one more column left. So the lowest set bit of the new `b` sits at position `p + 1` or higher. After at most 32 rounds the carry word has no bits left.

#### Why Negative Inputs Terminate Too

Java stores an `int` in a **fixed width** of 32 bits using two's complement, where the top bit has weight -2^31. Addition in this format is addition modulo 2^32. The left shift discards any bit that moves past column 31, and that discarded bit is exactly the overflow that the plus operator also discards. The same loop therefore handles negative inputs with no special case, and it stops after at most 32 rounds for every pair of `int` values.

<!-- stage: variables -->
### Quantities The Loop Keeps

Track these values while the loop runs.

- **a** is the running sum word, which starts as the first input and holds `a ^ b` after each round.
- **b** is the carry word, which starts as the second input and holds `(a & b) << 1` after each round.
- **rounds** counts how many times the loop body ran, and it never exceeds 32 for `int` values.
- **sumBit** is the XOR of two bits in one column, and **carryBit** is their AND.

The loop needs a temporary variable. The right side of the carry assignment must use the old `a`, so the program saves `a & b` before it overwrites `a`. No right shift appears anywhere in the loop, so the difference between `>>` and `>>>` does not matter here. The method reads the 32 bits of each argument as they are, and the result is the same 32 bits that the plus operator would produce.

<!-- stage: trace -->
### Follow One Sum And One String

#### Add 13 And 11 With Words

Take `a = 13` (`1101`) and `b = 11` (`1011`). The cells below hold the value of `a` at the start of each round, and the last cell is the final answer. Round 1 computes the sum word `0110` and the carry word `10010`. Round 2 adds those two words and gets the sum word `10100` and the carry word `00100`. Round 3 gives `10000` and `01000`. Round 4 adds the last pair without any overlapping set bits, so the carry word becomes 0 and the loop stops.

```trace
{"cells":[13,6,20,16,24],"pointers":["round"],"steps":[{"at":{"round":0},"vars":{"a":13,"b":11},"note":"The loop starts with a = 13 (1101) and the second operand b = 11 (1011)."},{"at":{"round":1},"vars":{"a":6,"b":18},"note":"Round 1 gives the sum word 110 and the carry word 10010. The carry word is not 0, so another round follows."},{"at":{"round":2},"vars":{"a":20,"b":4},"note":"Round 2 gives the sum word 10100 and the carry word 100. The carry word is not 0, so another round follows."},{"at":{"round":3},"vars":{"a":16,"b":8},"note":"Round 3 gives the sum word 10000 and the carry word 1000. The carry word is not 0, so another round follows."},{"at":{"round":4},"vars":{"a":24,"b":0},"note":"Round 4 gives the sum word 11000 and the carry word 0. The carry word is 0, so the loop stops."}]}
```

#### Add The Strings 1011 And 110

The same carry idea works on text digits. Align the strings on the right and visit the columns from the last character to the first. Each column adds its two digits and the carry from the previous column. The output digit is the total modulo 2, and the new carry is the total divided by 2. The trace below reads the cells of `1011` from right to left. A final carry of 1 after the last column becomes the leading digit.

```trace
{"cells":[1,0,1,1],"pointers":["i"],"steps":[{"at":{"i":4},"vars":{"carry":0},"note":"No column is read yet, so the carry is 0 and the pointer sits past the last digit."},{"at":{"i":3},"vars":{"xDigit":1,"yDigit":0,"total":1,"carry":0},"note":"Column 1 adds the digits 1 and 0 to the incoming carry 0, which gives 1. The output digit is 1 and the new carry is 0."},{"at":{"i":2},"vars":{"xDigit":1,"yDigit":1,"total":2,"carry":1},"note":"Column 2 adds the digits 1 and 1 to the incoming carry 0, which gives 2. The output digit is 0 and the new carry is 1."},{"at":{"i":1},"vars":{"xDigit":0,"yDigit":1,"total":2,"carry":1},"note":"Column 3 adds the digits 0 and 1 to the incoming carry 1, which gives 2. The output digit is 0 and the new carry is 1."},{"at":{"i":0},"vars":{"xDigit":1,"yDigit":0,"total":2,"carry":1},"note":"Column 4 adds the digits 1 and 0 to the incoming carry 1, which gives 2. The output digit is 0 and the new carry is 1."},{"at":{"i":-1},"vars":{"carry":1},"note":"Every column is read and the carry is still 1, so it becomes the leading digit. The result reads 10001."}]}
```

The hardest step is the third column of the string trace. The two digits plus the incoming carry give 2, so the output digit is 0 and the carry stays 1. The word loop meets the same case whenever a carry meets a 1 in the other word. That column's sum bit becomes 0, and a new carry moves one column left.

<!-- stage: code -->
### Implement The Loop And The String Sum

```java
final class BinaryArithmetic {
    static int add(int a, int b) {
        while (b != 0) {
            int carryWord = (a & b) << 1;    // parentheses keep the shift on the AND result
            a = a ^ b;                       // sum bits of every column without carries
            b = carryWord;                   // the carries become the next operand
        }
        return a;                            // no carries remain, so a is the total
    }

    static String addBinary(String x, String y) {
        StringBuilder out = new StringBuilder();
        int i = x.length() - 1;
        int j = y.length() - 1;
        int carry = 0;
        while (i >= 0 || j >= 0 || carry != 0) {
            int total = carry;                           // start with the incoming carry
            if (i >= 0) total += x.charAt(i--) - '0';    // read one digit of x
            if (j >= 0) total += y.charAt(j--) - '0';    // read one digit of y
            out.append((char) ('0' + (total & 1)));      // the low bit of the total is the digit
            carry = total >> 1;                          // the high bit is the next carry
        }
        int k = 0;
        String sum = out.reverse().toString();           // digits were appended from the right
        while (k < sum.length() - 1 && sum.charAt(k) == '0') k++;   // skip leading zeros, keep one digit
        return sum.substring(k);
    }
}
```

The word loop saves the carry word first because the next line overwrites `a`. The string loop runs while any input digit or a carry remains, so one extra pass appends the leading 1 for a sum such as `1` plus `1`. Inputs with leading zeros, such as `0` plus `000`, produce extra zeros at the front, so the last lines skip them and keep one digit. Both methods give the same result as the plus operator for the stated inputs. The string method reads one character per column, so it costs O(max(x, y)) time. The word method runs at most 32 rounds, which makes it O(1) for an `int`.

<!-- stage: applicability -->
### When To Use Bitwise Addition

#### Recognize The Pattern

Look for a requirement to build addition or a larger sum from gate-level operations, or for digit strings that exceed any machine word. The cue is that two operands combine into a sum and a leftover that moves one place to the left. The invariant to check before coding is that the running sum plus the carry word stays equal to the original total after every round, and that the loop ends only when the carry word is zero.

#### Watch For The Nearest False Friend

XOR alone is a false friend. The expression `a ^ b` equals `a + b` only when no column has two set bits, and it silently drops every carry otherwise. The case `3 ^ 1` gives 2, while `3 + 1` is 4. The OR operator fails in the same way. In production code, the plus operator or `Math.addExact` is the right tool, and the bitwise loop belongs to simulations, interviews and arbitrary-length digit strings.

#### Avoid The Java Shift Trap

Precedence causes the most common bug. The expression `a & b << 1` parses as `a & (b << 1)`, because the shift binds tighter than AND, so always write `(a & b) << 1`. Keep the arguments as `int`. If a caller widens them to `long`, the loop sums in 64 bits and a wraparound at 32 bits no longer happens. For digit strings, convert a character to its value with `c - '0'` and never test equality against a number.

<!-- stage: exercises -->
### Exercises

#### [Build] One-Bit Half Adder (Author exercise)
<!-- id: bt07-half-adder -->

**Prerequisites.** The sum bit and the carry bit from this lesson.

**Problem.** Given two bits `a` and `b`, each equal to 0 or 1, return an array of two ints. The first element is the sum bit, which is 1 when exactly one input bit is 1. The second element is the carry bit, which is 1 when both input bits are 1. Use only bitwise operators.

**Constraints.** Limits:
- **`a` and `b`** are `int` values that equal 0 or 1.
- **Return** is an `int[]` of length 2 in the order sum bit, carry bit.
- **Operators** allowed are `&`, `|`, `^` and `<<`.

**Example 1.** Input `a = 1` and `b = 1`, output `[0, 1]`, because 1 + 1 is binary `10`, which has sum bit 0 and carry bit 1.

**Example 2.** Input `a = 1` and `b = 0`, output `[1, 0]`, because only one input bit is set and no carry forms.

**Hint.** Which gate returns 1 for different inputs, and which gate returns 1 only when both inputs are 1?

**Changed decision.** Baseline case: separates the sum bit from the carry bit.

#### [Vary] Sum With Round Count (LeetCode 371)
<!-- id: bt07-sum-rounds -->

**Prerequisites.** The half adder exercise above and the loop from this lesson.

**Problem.** Given two non-negative integers `a` and `b`, add them without the plus or minus operator. Return an array of two ints. The first element is the sum, and the second element is the number of loop rounds that ran until the carry word became 0. This version differs from LeetCode 371, which returns only the sum and allows negative inputs.

**Constraints.** Limits:
- **`a` and `b`** are `int` values with `0 <= a, b <= 10^9`.
- **Sum** fits in an `int`.
- **Return** is an `int[]` of length 2, with the round count at least 0.
- **Operators** plus and minus are not allowed.

**Example 1.** Input `a = 13` and `b = 11`, output `[24, 4]`, because the carry word lasts four rounds, as the trace shows.

**Example 2.** Input `a = 999999999` and `b = 1`, output `[1000000000, 10]`, because the carry travels up a run of nine set bits and needs ten rounds.

**Hint.** What does the loop do when `b` is 0 at the start, and which expression is the new `b`?

**Changed decision.** The output grows from the sum alone to the sum plus the number of rounds.

#### [Boundary] Negative Inputs (Author exercise)
<!-- id: bt07-negative-inputs -->

**Prerequisites.** The two exercises above.

**Problem.** Given two 32-bit signed integers `a` and `b`, return their sum as the plus operator would compute it in Java, including wraparound on overflow. Use only bitwise operators and a loop.

**Constraints.** Limits:
- **`a` and `b`** are `int` values over the full range -2^31 to 2^31 - 1.
- **Overflow** wraps modulo 2^32, with no exception.
- **Return** is an `int`.
- **Operators** plus and minus are not allowed.

**Example 1.** Input `a = -5` and `b = 3`, output -2, because the carry word becomes 0 after two rounds.

**Example 2.** Input `a = -2147483648` and `b = -1`, output 2147483647, because the sum wraps modulo 2^32 and the carry out of column 31 is discarded.

**Hint.** What happens to a carry bit that moves past column 31, and how many rounds can the loop take at most?

**Changed decision.** The inputs include negative values, so termination relies on the fixed 32-bit width.

#### [Recognize] Binary String Addition (Author exercise)
<!-- id: bt07-binary-string-sum -->

**Prerequisites.** All three exercises above.

**Problem.** Given two strings `x` and `y` made of the characters `0` and `1`, return their sum as a binary string. The result has no leading zeros, except that the sum zero is the string `0`.

**Constraints.** Limits:
- **Length** of each string is an `int` with `1 <= length <= 10^4`.
- **Characters** are only `0` and `1`.
- **Leading zeros** may appear in the inputs.
- **Return** is a `String`, and the inputs are not mutated.

**Example 1.** Input `x = "111"` and `y = "1"`, output `"1000"`, because the carry runs through all three columns and adds a leading digit.

**Example 2.** Input `x = "0"` and `y = "000"`, output `"0"`, because leading zeros in the inputs are dropped and the zero sum keeps one digit.

**Hint.** Which value from the previous column joins the two digits of the current column?

**Changed decision.** The operands are character digits of unbounded length, so a fixed 32-bit word cannot hold them.
