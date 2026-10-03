<!-- lesson-kind: standard -->
<!-- lesson-id: infix-and-postfix-evaluation -->
## Infix And Postfix Evaluation

<!-- stage: context -->
### The Reverse Calculator Club

A club of retired engineers swears by calculators that have no equals key. To compute three plus four times two, a member types three, then four, then two, then the times key, then the plus key. Each operator key acts on the most recent numbers on the display stack and replaces them with one result. The club likes this style because nothing is ever ambiguous: the order of the keys is the order of the work, and brackets are never needed.

A newcomer wants to write a small program that runs a key sequence and prints the answer. She also wants to be able to type ordinary school arithmetic such as `3+2*4-6/2` and have the program turn it into the club's key order first. The club president warns her that the order of the two numbers under a minus key matters, and that she should test a subtraction and a division before trusting anything.

<!-- stage: naive -->
### Find An Operator Ready To Act

The direct method keeps the key sequence as a list. It scans from the left for the first operator that has two numbers just before it, replaces those three entries by the result, and repeats until one number is left.

```java
static long evaluateByRewriting(List<String> tokens) {
    List<String> t = new ArrayList<>(tokens);
    while (t.size() > 1) {
        for (int i = 2; i < t.size(); i++) {
            String op = t.get(i);
            if (op.length() == 1 && "+-*/".contains(op)) {
                long left = Long.parseLong(t.get(i - 2)), right = Long.parseLong(t.get(i - 1));
                long value = op.equals("+") ? left + right : op.equals("-") ? left - right
                        : op.equals("*") ? left * right : left / right;
                t.set(i - 2, String.valueOf(value));
                t.remove(i);
                t.remove(i - 1);
                break;
            }
        }
    }
    return Long.parseLong(t.get(0));
}
```

It is correct, because an operator with two numbers immediately before it is ready to act, and replacing the three entries by one preserves the meaning of the rest of the sequence.

<!-- stage: bottleneck -->
### Every Step Restarts The Scan

Each rewrite starts again from the left and removes two entries from the middle of the list, which shifts all later entries. With n tokens there are about n over two operators to apply, and each costs a scan of O(n) plus a shift of O(n), so the total is O(n^2). A sequence of a hundred thousand tokens would need billions of steps, and every step converts numbers to text and back again.

The restarts are wasted because the operator that becomes ready next is always right next to the one just applied, or later in the sequence. A reader who walks the tokens once and remembers the numbers still waiting needs no restart: when an operator key is met, the two numbers it needs are exactly the two most recent waiting numbers. A stack holds them, and the whole sequence is run in O(n).

<!-- stage: insight -->
### Waiting Numbers Live On A Stack

Walk the key sequence once. A number is pushed onto the **value stack**. An operator key pops two numbers, applies itself, and pushes the single result, so the stack always holds the completed operands that are still waiting for a partner. At the end, one number remains, and it is the answer.

The one decision that is easy to get wrong is **operand order**. The first number pop gives the right operand of the operator, because the right operand was pushed later. The second pop gives the left operand. For plus and times the order cannot matter, which is how a swapped version can pass the first tests. For minus and divide it does matter, so the code must pop the right operand first, then the left, and compute `left op right`. The key sequence `8 3 -` means eight minus three, which is five, and not three minus eight.

To accept ordinary school arithmetic, convert it to key order first with a second stack, the **operator stack**. Numbers go straight to the output. An operator waits on the operator stack, but before it waits it must let out any operator already waiting that binds at least as tightly, because that operator's right operand is now complete. Times and divide bind tighter than plus and minus, and equal precedence is released too, which makes the operators left associative, so `8-3-2` is `(8-3)-2`.

<!-- names: value stack, operand order, operator stack -->

The invariant for evaluation is that the value stack holds exactly the completed operands in the order they were produced, and the invariant for conversion is that the operator stack holds operators in strictly increasing precedence from bottom to top.

<!-- stage: variables -->
### Values, Operators And Tokens

The array `tokens` holds the key sequence as strings, and an operator is recognized as a token of length one that is one of the four symbols, because the token `-11` is a negative number and not an operator. The stack `values` holds `long` numbers and `ops` holds operator characters. A helper `prec` returns two for times and divide, one for plus and minus. The output of the conversion is a list of strings, built from numbers read digit by digit from the input text, so that a number such as 30 is a single token.

<!-- stage: trace -->
### Running Keys, Then Converting

The first trace runs the key sequence `2 3 4 * - 5 +`. The cells hold the tokens, and `t` points at the one being read. After three numbers are pushed, the times key pops 4 and then 3, and pushes 12. The minus key then pops 12 first as the right operand, and 2 second as the left operand, so the result is two minus twelve, which is minus ten.

```trace
{"cells":["2","3","4","*","-","5","+"],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"values":"[2]"},"note":"The number 2 is pushed onto the value stack."},{"at":{"t":1},"vars":{"values":"[2,3]"},"note":"The number 3 is pushed onto the value stack."},{"at":{"t":2},"vars":{"values":"[2,3,4]"},"note":"The number 4 is pushed onto the value stack."},{"at":{"t":3},"vars":{"values":"[2,12]"},"note":"The key * pops 4 first as the right operand and 3 second as the left operand, then pushes 3 * 4 = 12."},{"at":{"t":4},"vars":{"values":"[-10]"},"note":"The key - pops 12 first as the right operand and 2 second as the left operand, then pushes 2 - 12 = -10."},{"at":{"t":5},"vars":{"values":"[-10,5]"},"note":"The number 5 is pushed onto the value stack."},{"at":{"t":6},"vars":{"values":"[-5]"},"note":"The key + pops 5 first as the right operand and -10 second as the left operand, then pushes -10 + 5 = -5."}]}
```

The second trace converts `3+2*4-6/2`. The cells hold the tokens of the input. Look at the minus: the stack holds a plus below a times, so the times is released first because it binds tighter, and then the plus is released because it binds equally, which is the left associative rule at work.

```trace
{"cells":["3","+","2","*","4","-","6","/","2"],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"output":"3","waiting":""},"note":"The number 3 goes straight to the output."},{"at":{"t":1},"vars":{"output":"3","waiting":"+"},"note":"The operator + binds tighter than the waiting operator or finds none, so it waits on the operator stack."},{"at":{"t":2},"vars":{"output":"3 2","waiting":"+"},"note":"The number 2 goes straight to the output."},{"at":{"t":3},"vars":{"output":"3 2","waiting":"+*"},"note":"The operator * binds tighter than the waiting operator or finds none, so it waits on the operator stack."},{"at":{"t":4},"vars":{"output":"3 2 4","waiting":"+*"},"note":"The number 4 goes straight to the output."},{"at":{"t":5},"vars":{"output":"3 2 4 * +","waiting":"-"},"note":"The operator - first releases *+ to the output because it binds at least as tightly, and then waits on the operator stack."},{"at":{"t":6},"vars":{"output":"3 2 4 * + 6","waiting":"-"},"note":"The number 6 goes straight to the output."},{"at":{"t":7},"vars":{"output":"3 2 4 * + 6","waiting":"-/"},"note":"The operator / binds tighter than the waiting operator or finds none, so it waits on the operator stack."},{"at":{"t":8},"vars":{"output":"3 2 4 * + 6 2","waiting":"-/"},"note":"The number 2 goes straight to the output. At the end the waiting operators leave in reverse order, so the output is 3 2 4 * + 6 2 / -."}]}
```

<!-- stage: code -->
### Evaluate Postfix, Convert Infix

```java
static long evaluatePostfix(String[] tokens) {
    ArrayDeque<Long> values = new ArrayDeque<>();
    for (String tok : tokens) {
        if (tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0) {
            long right = values.removeLast();
            long left = values.removeLast();
            switch (tok.charAt(0)) {
                case '+': values.addLast(left + right); break;
                case '-': values.addLast(left - right); break;
                case '*': values.addLast(left * right); break;
                default: values.addLast(left / right);
            }
        } else {
            values.addLast(Long.parseLong(tok));
        }
    }
    return values.removeLast();
}

static List<String> toPostfix(String expr) {
    List<String> out = new ArrayList<>();
    ArrayDeque<Character> ops = new ArrayDeque<>();
    int i = 0;
    while (i < expr.length()) {
        char c = expr.charAt(i);
        if (c >= '0' && c <= '9') {
            int j = i;
            while (j < expr.length() && Character.isDigit(expr.charAt(j))) j++;
            out.add(expr.substring(i, j));
            i = j;
            continue;
        }
        while (!ops.isEmpty() && prec(ops.peekLast()) >= prec(c)) out.add(String.valueOf(ops.removeLast()));
        ops.addLast(c);
        i++;
    }
    while (!ops.isEmpty()) out.add(String.valueOf(ops.removeLast()));
    return out;
}

static int prec(char op) { return op == '*' || op == '/' ? 2 : 1; }
```

Each token is pushed once and popped once, so both methods run in O(n) time and O(n) space. The evaluator needs no precedence table at all, since the order of the tokens already carries it, and the converter holds the whole precedence rule in the single helper `prec`.

<!-- stage: applicability -->
### When Operators Wait For Operands

Use a value stack when operators arrive after their operands, as in postfix sequences, expression trees read bottom up, and calculators with no equals key. Use an operator stack to bring infix text into that order. The invariant is that the value stack holds completed operands in production order, and the operator stack holds waiting operators in increasing precedence.

A false friend is swapping the two popped operands, which is invisible for plus and times and wrong for minus and divide. A second false friend is releasing waiting operators only when they bind strictly tighter, which makes equal operators right associative, so that `8-3-2` is computed as `8-(3-2)`. A third is treating every token that starts with a minus as an operator, which turns the number `-11` into a broken key.

In Java, pop the right operand first and compute `left op right`. Recognize operators by exact one-character tokens, and parse everything else with `Long.parseLong`. Integer division truncates toward zero, so `-7 / 2` is `-3`, and a divide by zero throws `ArithmeticException` for integers, so the problem contract must exclude it.

<!-- stage: exercises -->
### Exercises

#### [Build] Evaluate One Postfix Operator (Author exercise)
<!-- id: sq-one-postfix-operator -->

**Prerequisites.** The Calculator And String Parsing lesson.

**Problem.** Given three tokens `a`, `b` and `op`, where `a` and `b` are integers and `op` is one of `+`, `-`, `*` and `/`, return the result of the postfix sequence `a b op`. Push both numbers, pop the right operand and then the left, and apply the operator.

**Constraints.** -1000000000 <= a, b <= 1000000000 and `b` is not zero when `op` is `/`.

**Example 1.** Input `tokens = ["8", "3", "-"]`, output `5`.

**Example 2.** Input `tokens = ["7", "2", "/"]`, output `3`.

**Hint.** Which of the two popped numbers was pushed first? Which one is the left operand?

**Changed decision.** First rung: the operand order is fixed by the pops, with the right operand coming off the stack first.

#### [Vary] Evaluate Reverse Polish Notation (LeetCode 150)
<!-- id: sq-evaluate-rpn -->

**Prerequisites.** The Evaluate One Postfix Operator rung.

**Problem.** Given an array of tokens that is a valid postfix expression, return its value. The tokens are integers and the four operators. Division truncates toward zero. All intermediate values fit in a signed 32-bit integer.

**Constraints.** 1 <= tokens.length <= 10000, every token is an operator or an integer between -200 and 200, and the expression is valid with no division by zero.

**Example 1.** Input `tokens = ["9", "3", "/", "2", "*"]`, output `6`.

**Example 2.** Input `tokens = ["2", "3", "4", "*", "-", "5", "+"]`, output `-5`.

**Hint.** How do you tell the token `-` from the token `-11`? How many values are on the stack when the sequence is finished?

**Changed decision.** Arbitrary valid sequences are run with a single value stack, and operators are recognized by exact token text.

#### [Boundary] Non-Commutative Trace (Author exercise)
<!-- id: sq-non-commutative-trace -->

**Prerequisites.** The Evaluate Reverse Polish Notation rung.

**Problem.** Given a valid postfix token array, return the result of every operator in the order the operators are applied, as an array. Negative operands and integer division under Java's rules must be handled exactly. The expression contains at least one operator.

**Constraints.** 3 <= tokens.length <= 10000, every token is an operator or an integer between -1000 and 1000, and no divisor is zero.

**Example 1.** Input `tokens = ["8", "3", "-", "2", "/"]`, output `[5, 2]`.

**Example 2.** Input `tokens = ["-7", "2", "/", "7", "-2", "/", "-"]`, output `[-3, -3, 0]`.

**Hint.** What is `-7 / 2` in Java? What would a floor division give instead?

**Changed decision.** Every intermediate result is reported, so a swapped operand order or a rounding rule that differs from Java's shows up at once.

#### [Recognize] Convert Simple Infix To Postfix (Author exercise)
<!-- id: sq-infix-to-postfix -->

**Prerequisites.** The Non-Commutative Trace rung.

**Problem.** Given an infix expression of non-negative integers and the operators `+`, `-`, `*` and `/`, with no spaces and no brackets, return the postfix tokens as an array of strings. Operators of equal precedence are left associative, and numbers may have several digits.

**Constraints.** 1 <= s.length <= 10000, the expression is valid and begins and ends with a digit, and every number is at most 1000000.

**Example 1.** Input `s = "3+2*4-6/2"`, output `["3", "2", "4", "*", "+", "6", "2", "/", "-"]`.

**Example 2.** Input `s = "8-3-2"`, output `["8", "3", "-", "2", "-"]`.

**Hint.** When a new operator arrives, which waiting operators must leave first? What happens when two operators have equal precedence?

**Changed decision.** An operator stack releases waiting operators of equal or higher precedence before a new operator waits, which gives the expected grouping and left associativity.
