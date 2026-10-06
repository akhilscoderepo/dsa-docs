<!-- lesson-kind: standard -->
<!-- lesson-id: infix-and-postfix-evaluation -->
## Evaluate Postfix And Convert Infix

<!-- stage: context -->
### A Formula Engine That Subtracts Backwards

A pricing module stores each formula as space-separated tokens with the operator written last. The text `5 2 +` means 5 plus 2, and `8 3 -` means 8 minus 3. A developer writes the engine in one afternoon. It pushes each number on a stack, and for each operator it pops two values, combines them and pushes the result. The test `5 2 +` returns 7 and passes. Then `8 3 -` returns -5, and `6 2 /` returns 0 instead of 3. Addition hid the fault, because 5 + 2 equals 2 + 5.

The stack itself is correct. The fault lies in which popped value is treated as the first one. A second request follows. Customers type `8 - 3 * 2` in ordinary notation, and the module must turn it into the stored form. The lesson answers two questions. In what order do the two values come off the stack, and how does a stack also convert ordinary notation into the stored form?

<!-- stage: naive -->
### Rescan The Token List For Each Operator

Without the stored form, the engine works directly on the ordinary notation. It scans the token list for the first operator of the highest precedence, replaces the three tokens around it with their result, and starts again from the left.

```java
static int rank(String op) {
    return op.equals("*") || op.equals("/") ? 2 : 1;
}

static int apply(int a, int b, String op) {
    switch (op) {
        case "+": return a + b;
        case "-": return a - b;
        case "*": return a * b;
        default: return a / b;
    }
}

static int evaluateByRescan(List<String> tokens) {
    List<String> t = new ArrayList<>(tokens);
    while (t.size() > 1) {
        int at = 1;
        for (int i = 1; i < t.size(); i += 2) {
            if (rank(t.get(i)) > rank(t.get(at))) at = i;
        }
        int a = Integer.parseInt(t.get(at - 1)), b = Integer.parseInt(t.get(at + 1));
        t.set(at - 1, String.valueOf(apply(a, b, t.get(at))));
        t.remove(at);
        t.remove(at);
    }
    return Integer.parseInt(t.get(0));
}
```

For `8 - 3 * 2` the first pass finds `*` and the list becomes `8 - 6`. The second pass finds `-` and returns 2. The method is correct, and it is the right reference for checking any faster method.

<!-- stage: bottleneck -->
### Counting The Moves After Each Rescan

```predict
An expression has 1000 numbers joined by 999 minus signs. The method finds the first operator and removes two tokens from the front of the list on every pass. Roughly how many element moves does the list shift cause in total?

About two million. Each pass shifts almost the whole remaining list left, and the list shrinks by only two tokens per pass, so the total grows with the square of the number of tokens.
```

Each pass scans the remaining tokens to find the highest precedence, which costs O(n). Each pass also removes two list elements, and `ArrayList.remove` shifts every later element. With `n` numbers there are `n - 1` passes, so the total cost is O(n^2) for both the scans and the shifts. A 1000-number chain of minus signs causes more than 1,900,000 element moves in the shifts alone.

The method also repeats work. It looks at the same low-precedence operators on every pass, although nothing about them changes until the operators around them are done. A method that touches each token once needs a place to keep what it cannot finish yet.

<!-- stage: insight -->
### Write Operators After Their Operands

#### Postfix Order Removes Precedence

In **postfix** notation each operator comes after its two operands, so `8 - 3 * 2` is written `8 3 2 * -`. Precedence and grouping are already encoded in the order. A reader evaluates the tokens from left to right and never needs to look ahead. This is the stored form from the opening, and it is also called reverse Polish notation.

<!-- names: postfix, right operand, operator stack -->

The value stack holds only finished numbers. A number token pushes itself. An operator token pops the two top values, applies the operator and pushes the single result. A valid expression leaves exactly one value on the stack at the end.

#### Pop The Right Operand First

The stack is last in, first out. The most recently pushed value is the **right operand**, and the value under it is the left operand. In `8 3 -` the value 3 was pushed last, so the first pop returns 3. The method must compute `left - right` with left equal to 8. Popping in the other order computes 3 - 8 for subtraction, and for `6 2 /` it computes 2 / 6, which is 0. Addition and multiplication give the same answer in both orders, so only a test with `-` or `/` can find the mistake. Java integer division truncates toward zero, so `-7 / 2` equals -3.

#### An Operator Stack Converts Infix

Ordinary notation, called **infix**, writes each operator between its operands. To convert it, keep an **operator stack** of operators that wait for their right side. A number goes straight to the output. When an operator arrives, every waiting operator on top with precedence at least as high as the new one is popped to the output first, because it must run before the new one. Then the new operator waits on the stack. At the end of the text, the remaining operators leave in stack order. Using at least as high, not strictly higher, makes equal operators run left to right, so `6 - 2 - 3` means `(6 - 2) - 3`.

<!-- stage: variables -->
### State For Evaluation And Conversion

Evaluation needs one stack, and conversion needs one stack and one output list.

- **values** is a stack of integers that are already computed, and its top is the most recent result.
- **right** is the first value an operator pops, and it is the operand written last.
- **left** is the second value an operator pops, and it is the operand written first.
- **ops** is a stack of operators that wait for their right side, with the highest precedence nearest the top.
- **output** is the list of postfix tokens built so far, which only grows.

The stack `values` changes at every token, while `ops` changes only at operators and at the end of the text.

<!-- stage: trace -->
### Walking One Evaluation And One Conversion

#### Evaluate A Subtraction And A Division

The tokens are `20 4 - 3 2 / *`. The cells are the tokens and the pointer `i` marks the token in use. The variable `values` lists the stack with the top on the right. After `20` and `4` the stack holds both, and `-` pops 4 first, then 20, so it computes 20 - 4 = 16. Next `3` and `2` are pushed and `/` computes 3 / 2 = 1. The final `*` multiplies 16 by 1.

```trace
{"cells":["20","4","-","3","2","/","*"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"values":"[20]"},"note":"The number 20 goes on the stack."},{"at":{"i":1},"vars":{"values":"[20, 4]"},"note":"The number 4 goes on the stack."},{"at":{"i":2},"vars":{"values":"[16]"},"note":"- pops the right operand 4, then the left operand 20, and pushes 20 - 4 = 16."},{"at":{"i":3},"vars":{"values":"[16, 3]"},"note":"The number 3 goes on the stack."},{"at":{"i":4},"vars":{"values":"[16, 3, 2]"},"note":"The number 2 goes on the stack."},{"at":{"i":5},"vars":{"values":"[16, 1]"},"note":"/ pops the right operand 2, then the left operand 3, and pushes 3 / 2 = 1."},{"at":{"i":6},"vars":{"values":"[16]"},"note":"* pops the right operand 1, then the left operand 16, and pushes 16 * 1 = 16."}]}
```

#### Convert An Expression With Three Operators

The tokens are `8 - 3 * 2 + 1`. Numbers go straight to `output`. The `-` waits on `ops`. The `*` has higher precedence than the waiting `-`, so nothing is popped and `*` waits above it. The `+` has precedence equal to `-` and lower than `*`, so it pops `*` and then `-` before it waits. The end of the text pops the last operator.

```trace
{"cells":["8","-","3","*","2","+","1"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"output":"8","ops":"[]"},"note":"The number 8 goes straight to the output."},{"at":{"i":1},"vars":{"output":"8","ops":"[-]"},"note":"- finds no waiting operator, so it waits."},{"at":{"i":2},"vars":{"output":"8 3","ops":"[-]"},"note":"The number 3 goes straight to the output."},{"at":{"i":3},"vars":{"output":"8 3","ops":"[-, *]"},"note":"* binds tighter than the waiting -, so it pops nothing and waits above it."},{"at":{"i":4},"vars":{"output":"8 3 2","ops":"[-, *]"},"note":"The number 2 goes straight to the output."},{"at":{"i":5},"vars":{"output":"8 3 2 * -","ops":"[+]"},"note":"+ pops * and - to the output, because they bind at least as tightly, and then waits."},{"at":{"i":6},"vars":{"output":"8 3 2 * - 1","ops":"[+]"},"note":"The number 1 goes straight to the output."},{"at":{"i":7},"vars":{"output":"8 3 2 * - 1 +","ops":"[]"},"note":"The end of the text pops the waiting + to the output."}]}
```

<!-- stage: code -->
### Writing Evaluation And Conversion In Java

#### Evaluate A Postfix Token Array

The method pops the right operand first. A token is an operator when it is one character long and one of the four signs, so the token `-7` stays a number.

```java
static boolean isOperator(String tok) {
    return tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0;
}

static int evalPostfix(String[] tokens) {
    Deque<Integer> values = new ArrayDeque<>();
    for (String tok : tokens) {
        if (!isOperator(tok)) { values.addLast(Integer.parseInt(tok)); continue; }
        int right = values.removeLast();
        int left = values.removeLast();
        switch (tok.charAt(0)) {
            case '+' -> values.addLast(left + right);
            case '-' -> values.addLast(left - right);
            case '*' -> values.addLast(left * right);
            default -> values.addLast(left / right);
        }
    }
    return values.removeLast();
}
```

#### Convert Infix Tokens To Postfix

The method treats a token of precedence 0 as a number, and it pops the waiting operator when precedences are equal.

```java
static int prec(String tok) {
    switch (tok) {
        case "+": case "-": return 1;
        case "*": case "/": return 2;
        default: return 0;
    }
}

static List<String> toPostfix(String[] infix) {
    List<String> output = new ArrayList<>();
    Deque<String> ops = new ArrayDeque<>();
    for (String tok : infix) {
        if (prec(tok) == 0) { output.add(tok); continue; }
        while (!ops.isEmpty() && prec(ops.peekLast()) >= prec(tok)) output.add(ops.removeLast());
        ops.addLast(tok);
    }
    while (!ops.isEmpty()) output.add(ops.removeLast());
    return output;
}
```

Both methods run in O(n) time and use O(n) space, because each token is pushed once and popped at most once.

<!-- stage: applicability -->
### When The Two Stacks Apply

#### Postfix Input Is Safe To Trust

The invariant for evaluation is that the stack holds only finished values, and each operator replaces its two top values with one. Use this method when the input is already operator-last and valid. Then the stack never has fewer than two values at an operator, and it ends with one value.

#### Operand Order Is The False Friend

Swapping the two popped values is a false friend. It passes every test that uses only `+` and `*`, and it fails at the first `-` or `/`. Always include `8 3 -` and a division with a negative left value in a test.

#### Cases That Need More

The conversion above has no parentheses, no unary minus and no right-associative operators. Parentheses need a marker on `ops` that stops popping. A right-associative operator such as exponentiation pops only strictly higher precedence. Division by zero is the caller's contract and is not repaired by either method. For plain infix text that has no parentheses, a single scan with a saved term is shorter, as the calculator lesson showed.

<!-- stage: exercises -->
### Exercises

#### [Build] Evaluate One Postfix Operator (Author exercise)
<!-- id: sq-eval-one-operator -->

**Prerequisites.** The value stack and the pop order from this lesson.

**Problem.** Given exactly three tokens `a b op`, where `a` and `b` are decimal integers and `op` is one of `+`, `-`, `*` or `/`, return the value of the postfix expression. The result is `a op b` in Java `int` arithmetic, where `/` truncates toward zero.

**Constraints.** The limits are:
- **Values** are `int` values written in decimal, and a negative value has a leading minus sign.
- **Divisor** `b` is not zero when `op` is `/`.
- **Results** fit in an `int`.
- **Mutation** is not allowed; the token array does not change.

**Example 1.** Input `["8","3","-"]`, output 5.

**Example 2.** Input `["-7","2","/"]`, output -3.

**Hint.** Push both numbers, then pop twice. Which pop returns the value written last?

**Changed decision.** The first value popped is the right operand, and the second value popped is the left operand.

#### [Vary] Evaluate Reverse Polish Notation (LeetCode 150)
<!-- id: sq-leetcode-rpn -->

**Prerequisites.** The exercise above.

**Problem.** An array of tokens is a valid postfix expression. Each token is an operator from `+`, `-`, `*`, `/` or a decimal integer. Evaluate the expression and return the result. Division truncates toward zero.

**Constraints.** The limits are:
- **Length** is `1 <= tokens.length <= 10^4`.
- **Tokens** are an operator or an `int` in decimal, and a negative number keeps its minus sign.
- **Validity** means the expression is well formed and never divides by zero.
- **Results** and all intermediate values fit in a 32-bit `int`.

**Example 1.** Input `["6","-4","/","5","+"]`, output 4, because 6 / -4 is -1 and -1 + 5 is 4.

**Example 2.** Input `["9","3","4","-","*","2","/"]`, output -4, because 3 - 4 is -1, 9 * -1 is -9, and -9 / 2 is -4.

**Hint.** One stack holds the finished values. When a token is exactly one operator character, pop the right operand and then the left operand.

**Changed decision.** The expression has any length and any nesting, so one value stack replaces the single operator of the previous exercise.

#### [Boundary] Non-Commutative Trace (Author exercise)
<!-- id: sq-operator-results -->

**Prerequisites.** The two exercises above.

**Problem.** Given a valid postfix token array, return the result of each operator in the order the operators are applied. The result of the first applied operator is the first element, and the result of the last applied operator is the last element.

**Constraints.** The limits are:
- **Length** is `1 <= tokens.length <= 10^4`.
- **Tokens** are an operator from `+`, `-`, `*`, `/` or a decimal `int`, and `-7` is a number while `-` alone is an operator.
- **Arithmetic** is Java `int` arithmetic, and division truncates toward zero, not toward negative infinity.
- **Return** is an `int[]`, empty when the array holds one number.
- **Validity** means the expression is well formed, the divisor is never zero, and every intermediate value fits in an `int`.

**Example 1.** Input `["8","3","-"]`, output `[5]`.

**Example 2.** Input `["-7","2","/","-3","*"]`, output `[-3,9]`.

**Hint.** Add each computed value to the result list before it goes back on the stack. How does the code tell `-7` from `-`?

**Changed decision.** The answer is the sequence of intermediate values, so truncation and operand order both show in the output.

#### [Recognize] Convert Simple Infix To Postfix (Author exercise)
<!-- id: sq-infix-to-postfix -->

**Prerequisites.** All three exercises above.

**Problem.** Given infix tokens that alternate between integers and operators from `+`, `-`, `*`, `/`, return the value of the expression. Multiplication and division bind tighter than addition and subtraction. Operators of equal precedence apply from left to right. Division truncates toward zero.

**Constraints.** The limits are:
- **Length** is an odd number from 1 to 999 tokens.
- **Numbers** are non-zero decimal `int` values, and a negative number keeps its minus sign.
- **Parentheses** do not appear.
- **Results** and all intermediate values fit in an `int`.

**Example 1.** Input `["9","/","2","*","4","-","7"]`, output 9, because 9 / 2 is 4, then 4 * 4 is 16, then 16 - 7 is 9.

**Example 2.** Input `["6","-","2","-","3"]`, output 1.

**Hint.** Convert to postfix first, then reuse the value stack. When a new operator arrives, which waiting operators must leave first?

**Changed decision.** The input has precedence and no stored order, so an operator stack decides when each operator moves to the output.
