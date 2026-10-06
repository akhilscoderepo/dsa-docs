<!-- lesson-kind: standard -->
<!-- lesson-id: calculator-and-string-parsing -->
## Evaluate Expressions Written As Text

<!-- stage: context -->
### A Total Field That Rejects Valid Input

An invoice form lets a clerk type a total as a sum, such as `120 + 35 - 8`. The first version splits the text on spaces and parses each piece with `Integer.parseInt`. It works for that entry. A clerk who types `120+35-8` without spaces gets a `NumberFormatException`, because the whole text is one piece. A clerk who types `7 + 12 * 3` gets 57 when the code applies the operators in the order they appear, although multiplication should come first and the answer is 43.

The characters of the text carry the structure. Digits join into one number, an operator sits between two numbers, and spaces are optional. The lesson answers one question. How does a single left-to-right pass over the characters give every number and every operator the meaning that the arithmetic rules assign?

<!-- stage: naive -->
### Split Into Tokens And Make Several Passes

The direct method first cuts the text into tokens. A token is one number or one operator. Then it makes a pass that evaluates every `*` and `/` inside the token list, and a second pass that adds and subtracts what remains.

```java
static long evalByTokenList(String s) {
    String[] parts = s.replace(" ", "").split("(?<=[-+*/])|(?=[-+*/])");
    List<String> t = new ArrayList<>(Arrays.asList(parts));
    int i = 1;
    while (i < t.size()) {
        String op = t.get(i);
        if (op.equals("*") || op.equals("/")) {
            long a = Long.parseLong(t.get(i - 1)), b = Long.parseLong(t.get(i + 1));
            t.set(i - 1, String.valueOf(op.equals("*") ? a * b : a / b));
            t.remove(i);
            t.remove(i);
        } else {
            i += 2;
        }
    }
    long sum = Long.parseLong(t.get(0));
    for (int k = 1; k < t.size(); k += 2) {
        long b = Long.parseLong(t.get(k + 1));
        sum += t.get(k).equals("+") ? b : -b;
    }
    return sum;
}
```

The method is correct for non-negative numbers when no round brackets appear. For `7+12*3` the first pass replaces `12*3` by `36`, and the second pass adds 7 and 36.

<!-- stage: bottleneck -->
### Removing From The Middle Of A List

```predict
The text is `1*1*1*...*1` with 50,000 multiplications. About how many list elements does the first pass move to the left in total?

About 5 billion. Each multiplication removes two elements near the front of the list, and `ArrayList.remove` shifts every later element one place to the left. The list starts with about 100,000 elements, so each multiplication moves about twice the remaining length.
```

The method costs O(n) to split the text. The first pass costs more. Each `remove(i)` shifts all later tokens, so one multiplication costs O(n). A text with `m` multiplications at the front costs O(m * n), and a text made only of multiplications costs O(n^2). The method also stores every token as a `String` and parses it again, and it has no place for a parenthesis or a sign in front of a number.

The repeated work is the movement of tokens that never change. The pass already knows the one number that every `*` or `/` needs, which is the number right before it. A method that keeps that number at hand can apply the operator the moment the next number is complete, and it never removes anything from the middle.

<!-- stage: insight -->
### Delay Each Operator Until Its Number Ends

A reader that moves left to right sees an operator before the number on its right. The reader cannot apply the operator yet. It must keep what it knows and apply the operator when the right operand is complete.

<!-- names: pending operator, term, parent -->

#### The Pending Operator Waits For A Number

The **pending operator** is the most recent operator character that has not been applied yet. It starts as `+`, which gives the first number a plus sign. Digits change only `num`, using `num = num * 10 + digit`. A number is complete at the next operator character or at the end of the text. At that boundary the reader applies the pending operator to `num`, makes the new operator pending, and resets `num` to 0. Spaces change nothing, which is why `120+35-8` and `120 + 35 - 8` give the same result.

#### Multiplication Changes The Last Term

A **term** is a chain of numbers joined by `*` and `/`, between two `+` or `-` signs or the ends of the text. The text `7 + 12*3 - 20/4` has the three terms 7, 36 and 5. The value of the whole text is the sum of its terms with their signs. The reader keeps the finished terms on a stack. A pending `+` pushes `num`, and a pending `-` pushes `-num`. A pending `*` or `/` pops the top term, applies the operator with `num`, and pushes the result. The invariant is that, at every boundary, the stack holds the signed value of each finished term and the top term can still change.

#### Parentheses Save The Parent Expression

The **parent** of a parenthesized group is the group that directly contains it, and the text outside every group has no parent. At a `(` the reader has a running result and the sign in front of the group. It saves both on a stack and starts a fresh result of 0 with sign 1 for the inside. At the matching `)` it finishes the inner number, multiplies the inner result by the saved sign, and adds the saved result. The invariant is that the running result belongs to the innermost open group, and the saved pairs belong to the parents. This lesson keeps the two tools in separate grammars: terms for `*` and `/`, and saved parents for parentheses.

<!-- stage: variables -->
### What The Reader Keeps

The reader keeps up to six pieces of state, depending on the grammar.

- **num** is the number built from the digits since the last boundary, and it resets to 0 at each boundary.
- **op** is the pending operator, and it changes only at a boundary.
- **terms** is the stack of signed finished terms, and its top changes at each `*` or `/`.
- **result** is the running sum of the innermost open group.
- **sign** is the sign that the next number gets, either 1 or -1.
- **saved** holds one pair of result and sign for each open parenthesis.

<!-- stage: trace -->
### Reading Two Expressions Character By Character

#### Terms On A Stack

The first trace reads `7 + 12*3 - 20/4`. The cells are the characters, and the pointer `i` marks the character just read. The vars show `num`, the pending operator `op` and the stack `terms`. The last step has the pointer past the final cell, because the end of the text is also a boundary.

The number 7 stays in `num` until the first operator. At that boundary the pending operator is the initial `+`, so 7 goes on the stack. The `*` between 12 and 3 acts when 3 is complete, so it multiplies the top term by 3 and replaces 12 by 36. At the end, the sum of the stack is 7 + 36 - 5 = 38.

```trace
{"cells":["7"," ","+"," ","1","2","*","3"," ","-"," ","2","0","/","4"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"num":7,"op":"+","terms":"[]"},"note":"The digit 7 makes num 7."},{"at":{"i":1},"vars":{"num":7,"op":"+","terms":"[]"},"note":"The space changes nothing."},{"at":{"i":2},"vars":{"num":0,"op":"+","terms":"[7]"},"note":"+ ends the number 7. The pending operator + pushes 7. Now + is pending."},{"at":{"i":3},"vars":{"num":0,"op":"+","terms":"[7]"},"note":"The space changes nothing."},{"at":{"i":4},"vars":{"num":1,"op":"+","terms":"[7]"},"note":"The digit 1 makes num 1."},{"at":{"i":5},"vars":{"num":12,"op":"+","terms":"[7]"},"note":"The digit 2 makes num 12."},{"at":{"i":6},"vars":{"num":0,"op":"*","terms":"[7, 12]"},"note":"* ends the number 12. The pending operator + pushes 12. Now * is pending."},{"at":{"i":7},"vars":{"num":3,"op":"*","terms":"[7, 12]"},"note":"The digit 3 makes num 3."},{"at":{"i":8},"vars":{"num":3,"op":"*","terms":"[7, 12]"},"note":"The space changes nothing."},{"at":{"i":9},"vars":{"num":0,"op":"-","terms":"[7, 36]"},"note":"- ends the number 3. The pending operator * multiplies the top term 12 by 3. Now - is pending."},{"at":{"i":10},"vars":{"num":0,"op":"-","terms":"[7, 36]"},"note":"The space changes nothing."},{"at":{"i":11},"vars":{"num":2,"op":"-","terms":"[7, 36]"},"note":"The digit 2 makes num 2."},{"at":{"i":12},"vars":{"num":20,"op":"-","terms":"[7, 36]"},"note":"The digit 0 makes num 20."},{"at":{"i":13},"vars":{"num":0,"op":"/","terms":"[7, 36, -20]"},"note":"/ ends the number 20. The pending operator - pushes -20. Now / is pending."},{"at":{"i":14},"vars":{"num":4,"op":"/","terms":"[7, 36, -20]"},"note":"The digit 4 makes num 4."},{"at":{"i":15},"vars":{"num":0,"op":"+","terms":"[7, 36, -5]"},"note":"The end of the text ends the number 4. The pending operator / divides the top term -20 by 4."}]}
```

#### Saved Parents In Parentheses

The second trace reads `20-(4-(3+2))+1`. The vars show `num`, `sign`, `result` and the stack `saved`, where each pair is the saved result and the saved sign. The first `(` saves the result 20 and the sign -1 that stands in front of the group. The second `(` saves the result 4 and the sign -1 again.

At the innermost `)` the inner result 5 is multiplied by the saved sign -1 and added to the saved 4, which gives -1. At the next `)` the value -1 is multiplied by -1 and added to 20, which gives 21. The final `+1` brings the answer to 22.

```trace
{"cells":["2","0","-","(","4","-","(","3","+","2",")",")","+","1"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"num":2,"sign":1,"result":0,"saved":"[]"},"note":"The digit 2 makes num 2."},{"at":{"i":1},"vars":{"num":20,"sign":1,"result":0,"saved":"[]"},"note":"The digit 0 makes num 20."},{"at":{"i":2},"vars":{"num":0,"sign":-1,"result":20,"saved":"[]"},"note":"- adds 20 to result, which is now 20."},{"at":{"i":3},"vars":{"num":0,"sign":1,"result":0,"saved":"[(20, -1)]"},"note":"( saves result 20 and sign -1, then starts a fresh group."},{"at":{"i":4},"vars":{"num":4,"sign":1,"result":0,"saved":"[(20, -1)]"},"note":"The digit 4 makes num 4."},{"at":{"i":5},"vars":{"num":0,"sign":-1,"result":4,"saved":"[(20, -1)]"},"note":"- adds 4 to result, which is now 4."},{"at":{"i":6},"vars":{"num":0,"sign":1,"result":0,"saved":"[(20, -1), (4, -1)]"},"note":"( saves result 4 and sign -1, then starts a fresh group."},{"at":{"i":7},"vars":{"num":3,"sign":1,"result":0,"saved":"[(20, -1), (4, -1)]"},"note":"The digit 3 makes num 3."},{"at":{"i":8},"vars":{"num":0,"sign":1,"result":3,"saved":"[(20, -1), (4, -1)]"},"note":"+ adds 3 to result, which is now 3."},{"at":{"i":9},"vars":{"num":2,"sign":1,"result":3,"saved":"[(20, -1), (4, -1)]"},"note":"The digit 2 makes num 2."},{"at":{"i":10},"vars":{"num":0,"sign":1,"result":-1,"saved":"[(20, -1)]"},"note":") finishes the inner result 5, multiplies it by the saved sign -1 and adds the saved result 4, so result is -1."},{"at":{"i":11},"vars":{"num":0,"sign":1,"result":21,"saved":"[]"},"note":") finishes the inner result -1, multiplies it by the saved sign -1 and adds the saved result 20, so result is 21."},{"at":{"i":12},"vars":{"num":0,"sign":1,"result":21,"saved":"[]"},"note":"+ adds 0 to result, which is now 21."},{"at":{"i":13},"vars":{"num":1,"sign":1,"result":21,"saved":"[]"},"note":"The digit 1 makes num 1."},{"at":{"i":14},"vars":{"num":0,"sign":1,"result":22,"saved":"[]"},"note":"The end of the text adds the last number, so the answer is 22."}]}
```

<!-- stage: code -->
### Writing The Two Readers

#### Terms With A Stack

The method treats the end of the text as a final boundary by reading a `+` there. The `/` operator applies Java integer division, which truncates toward zero.

```java
static int calculate(String s) {
    ArrayDeque<Integer> terms = new ArrayDeque<>();
    int num = 0;
    char op = '+';
    for (int i = 0; i <= s.length(); i++) {
        char c = i < s.length() ? s.charAt(i) : '+';
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
        } else if (c != ' ') {
            if (op == '+') terms.push(num);
            else if (op == '-') terms.push(-num);
            else if (op == '*') terms.push(terms.pop() * num);
            else terms.push(terms.pop() / num);
            op = c;
            num = 0;
        }
    }
    int sum = 0;
    for (int term : terms) sum += term;
    return sum;
}
```

#### Parentheses With Saved Pairs

This method has only `+`, `-` and parentheses. It keeps the saved results and the saved signs on two stacks of equal size.

```java
static int calculateGroups(String s) {
    ArrayDeque<Integer> results = new ArrayDeque<>();
    ArrayDeque<Integer> signs = new ArrayDeque<>();
    int result = 0, sign = 1, num = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
        } else if (c == '+' || c == '-') {
            result += sign * num;
            num = 0;
            sign = c == '+' ? 1 : -1;
        } else if (c == '(') {
            results.push(result);
            signs.push(sign);
            result = 0;
            sign = 1;
        } else if (c == ')') {
            result += sign * num;
            num = 0;
            result = result * signs.pop() + results.pop();
        }
    }
    return result + sign * num;
}
```

Both methods read each character once. They run in O(n) time. The first uses O(t) space for `t` terms, and the second uses O(d) space for nesting depth `d`.

<!-- stage: applicability -->
### Telling When Delayed Meaning Applies

#### Recognize The Cue

Use a pending operator when numbers and operators arrive as characters and the meaning of an operator depends on a number that comes later. The invariant of this lesson is that, at each boundary, `num`, the pending operator and the saved context have one exact meaning. Spreadsheet formulas, discount rules typed by hand and filter expressions in a search box have this shape.

#### Splitting On Spaces Is A False Friend

A method that splits on spaces looks simple. It is a false friend, because spaces are optional, and `120+35-8` is one piece. Evaluating left to right is also a false friend when `*` and `/` appear, since `7+12*3` gives 57 and not 43. A third false friend is the unary minus. In `-4+1` and in `(-4+1)` the `-` has no left operand, so the reader must not treat it as a binary operator that applies to an earlier number. The method `calculateGroups` above handles a unary minus only at the start of the text or right after `(`.

#### A Sign After Another Sign

In `5 - -3` the second `-` follows a sign and not a number. The rule is that a sign with no number since the last sign flips the sign. Here the second `-` flips the pending sign from -1 to 1, so the text means 5 + 3. The code above does not apply this rule, because it overwrites the pending sign instead of flipping it. The Boundary exercise below uses the rule.

#### When Not To Use This Reader

The code in this lesson evaluates `+` and `-` with parentheses, or `+`, `-`, `*` and `/` without parentheses. It handles a unary minus only at the start of the text or after `(`, and it does not handle a sign that follows another sign. A text that has both parentheses and `*` or `/` needs the terms stack and the saved parents together. That combination is its own problem. An exponent operator or a function call needs a rule for which operator binds first, and a stack of numbers alone cannot encode it.

<!-- stage: exercises -->
### Exercises

#### [Build] Signed Sum (Author exercise)
<!-- id: sq-signed-sum -->

**Prerequisites.** The pending operator and `num` of this lesson.

**Problem.** An expression is a sequence of non-negative decimal integers separated by the operators `+` and `-`, with no spaces and no sign before the first integer. Given a well-formed expression, return its value, where operators apply from left to right.

**Constraints.** The limits are:
- **Length** is 1 to 100000 characters.
- **Integers** are from 0 to 1000000, written without leading plus signs.
- **Return** is a `long`.
- **Mutation** is not allowed; the input is read once.

**Example 1.** Input `120+35-8`, output 147.

**Example 2.** Input `10-4-3-2`, output 1.

**Hint.** The operator before a number applies when the number is complete. What must the reader do at the end of the text, where no operator follows?

**Changed decision.** Basic case: a number is complete only at the next operator or the end, so `num = num * 10 + digit`.

#### [Vary] Basic Calculator II (LeetCode 227)
<!-- id: sq-leetcode-calculator-two -->

**Prerequisites.** The exercise above and the term stack of this lesson.

**Problem.** An expression has non-negative integers and the operators `+`, `-`, `*` and `/`, with optional spaces. Multiplication and division bind tighter than addition and subtraction, and operators of equal rank apply left to right. Division is integer division that truncates toward zero. Return the value of a well-formed expression.

**Constraints.** The limits are:
- **Length** is 1 to 100000 characters.
- **Integers** are from 0 to 1000000, and every intermediate value fits in `int`.
- **Division** never has a zero divisor.
- **Spaces** can appear anywhere except inside a number.

**Example 1.** Input `8 - 3*4 + 10/3`, output -1.

**Example 2.** Input ` 100/7/2`, output 7.

**Hint.** Which value must change when `*` or `/` arrives, a finished term or the running sum? What does the stack hold after `8 - 3`?

**Changed decision.** Multiplication and division change the top term, while addition and subtraction push a new signed term.

#### [Boundary] Spaces And Unary Sign (Author exercise)
<!-- id: sq-spaces-and-unary-sign -->

**Prerequisites.** The two exercises above.

**Problem.** An expression has non-negative integers, the operators `+` and `-`, and optional spaces. A sign is unary when it is the first character or follows another sign, and a unary sign applies to the number or sign after it. A sign is binary when it follows a number. Return the value of a well-formed expression.

**Constraints.** The limits are:
- **Length** is 1 to 100000 characters.
- **Integers** are from 0 to 1000, and the value fits in `long`.
- **Signs** can repeat, so `- - 3` is legal and equals 3.
- **Spaces** can appear anywhere except inside a number.

**Example 1.** Input ` - 4 +10 - -3`, output 9.

**Example 2.** Input `5 - - - 2`, output 3.

**Hint.** What distinguishes a sign that follows a number from a sign that follows another sign? Which variable can record whether a number was read since the last sign?

**Changed decision.** A sign with no number since the previous sign flips the pending sign, while a sign after a number applies the number first.

#### [Recognize] Basic Calculator (LeetCode 224)
<!-- id: sq-leetcode-basic-calculator -->

**Prerequisites.** All exercises above, and the saved parents of this lesson.

**Problem.** An expression has non-negative integers, the operators `+` and `-`, parentheses and optional spaces. A `-` is unary when it is the first character of the expression or follows `(`, and then it negates the value that comes next. Return the value of a well-formed expression.

**Constraints.** The limits are:
- **Length** is 1 to 100000 characters.
- **Integers** are from 0 to 1000000, and every intermediate value fits in `int`.
- **Nesting** is at most 20000 levels deep.
- **Spaces** can appear anywhere except inside a number.

**Example 1.** Input `(1+(4-12))-(3-5)`, output -5.

**Example 2.** Input `-(2+3)-(-4)`, output -1.

**Hint.** What must be saved at `(` so that the inner result can join its parent later? Which sign multiplies the inner result?

**Changed decision.** A `(` saves the running result and the sign in front of it, and a `)` folds the finished inner result into the saved parent.
