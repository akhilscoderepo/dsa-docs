<!-- lesson-kind: standard -->
<!-- lesson-id: calculator-and-string-parsing -->
## Calculator And String Parsing

<!-- stage: context -->
### The Market Stall Running Total

A market trader keeps her takings as one long line of text on a paper tape, written quickly in the order things happened: a sale is a number, a refund is a minus sign and a number, and a bundle price is written as a product, such as three items at four coins each. The tape has irregular spaces, because some days she types fast, and now and then a group of sales is wrapped in round brackets because she settled it with a customer separately and wants it kept together.

Each evening her nephew types the tape into a program that has to say what the day's total is. The program must respect that multiplication binds tighter than adding, that a number can have several digits, that a minus can mean a refund or can sit in front of a bracket, and that spaces carry no meaning and may be missing entirely.

<!-- stage: naive -->
### Split Into Words And Rewrite The List

The direct method splits the tape on spaces into tokens, makes a first pass that replaces every multiplication or division by its result, and makes a second pass that adds and subtracts what is left.

```java
static long evaluateSpaced(String s) {
    List<String> t = new ArrayList<>(Arrays.asList(s.trim().split(" +")));
    int i = 1;
    while (i < t.size()) {
        String op = t.get(i);
        if (op.equals("*") || op.equals("/")) {
            long a = Long.parseLong(t.get(i - 1)), b = Long.parseLong(t.get(i + 1));
            t.set(i - 1, String.valueOf(op.equals("*") ? a * b : a / b));
            t.remove(i);
            t.remove(i);
        } else i += 2;
    }
    long total = Long.parseLong(t.get(0));
    for (int k = 1; k < t.size(); k += 2) {
        long v = Long.parseLong(t.get(k + 1));
        total += t.get(k).equals("+") ? v : -v;
    }
    return total;
}
```

It is correct for tapes where every number and every operator is separated by spaces, since the first pass applies the tighter operators before the second pass runs.

<!-- stage: bottleneck -->
### It Needs Spaces And Shifts The List

The method fails outright on a tape written as `3+2*4`, because splitting on spaces produces one token, and it has no answer at all for brackets. Even when the spacing is perfect, each product removes two entries from the middle of an `ArrayList`, which shifts every later entry, so a tape with n entries and about n over four products costs O(n^2) in shifting alone. A tape with a hundred thousand terms makes billions of shifts, and every step also converts numbers to text and back.

The root cause is that the method waits to see the whole tape before it acts, and then rewrites the list again and again. A reader scans the tape once, and for each number the only question is what to do with it now. The sum so far does not need the number if the number is going to be multiplied by the next one, so the program has to remember the most recent term separately from the finished total. That memory is one number, and the scan costs O(n).

<!-- stage: insight -->
### Keep The Open Term And Operator

Scan the characters left to right, building each number digit by digit with `value = value * 10 + digit`, and skip spaces without any other effect. A number is not used when its last digit is read, because the next character might extend it. Instead it is used when the next operator, or the end of the tape, arrives, together with the **pending operator** that came before the number. The pending operator says how the number joins the terms: a plus pushes it as a new term, a minus pushes its negation, and a times or divide replaces the most recent term by the product or quotient of that term and the number.

The stack of terms is the memory that makes precedence automatic. Addition and subtraction only ever push finished terms, while multiplication and division reach back into the top term and change it, so by the time the tape ends, every product has already been folded into its term, and the answer is the sum of the stack. The **term accumulator** is the stack's top: the one value that is still allowed to change.

Round brackets add a second kind of unresolved state. When an opening bracket arrives, the result so far and the sign in front of the bracket must be set aside, and the inside starts from zero. When the closing bracket arrives, the inside result is multiplied by the saved sign and added to the saved result. These two numbers are the **saved context**, one pair for each open bracket.

<!-- names: pending operator, term accumulator, saved context -->

The invariant is that at every token boundary the accumulated number, the pending operator and the saved contexts together give an exact meaning to the part of the tape that has been read.

<!-- stage: variables -->
### Number, Operator, Terms, Contexts

The variable `num` accumulates the digits of the number being read, `op` holds the pending operator, which starts as plus, and `terms` is a stack of finished and still-open terms. For the bracketed version, `result` is the running total of the current level, `sign` is the sign that will apply to the next number, and `saved` is a stack that receives `result` and `sign` at an opening bracket. All sums are held in `long`, because a tape of large numbers can exceed the range of `int`. Division is integer division, which in Java truncates toward zero for negative operands.

<!-- stage: trace -->
### One Pass Over The Tape

The first trace evaluates `3+2*4-6/2` with the stack of terms. The characters fill the cells, and `i` is the index in hand. Each operator commits the number before it using the operator that came before that number. Look at the multiplication: the term 2 is on top of the stack, and the product with 4 replaces it, so the later minus sees a finished eight.

```trace
{"cells":["3","+","2","*","4","-","6","/","2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"terms":"[]","op":"+","num":3},"note":"The digit 3 is read, so the number in progress is 3."},{"at":{"i":1},"vars":{"terms":"[3]","op":"+","num":0},"note":"The character + commits the number 3: the pending plus pushes the term 3."},{"at":{"i":2},"vars":{"terms":"[3]","op":"+","num":2},"note":"The digit 2 is read, so the number in progress is 2."},{"at":{"i":3},"vars":{"terms":"[3,2]","op":"*","num":0},"note":"The character * commits the number 2: the pending plus pushes the term 2."},{"at":{"i":4},"vars":{"terms":"[3,2]","op":"*","num":4},"note":"The digit 4 is read, so the number in progress is 4."},{"at":{"i":5},"vars":{"terms":"[3,8]","op":"-","num":0},"note":"The character - commits the number 4: the pending times replaces the top term 2 by 8."},{"at":{"i":6},"vars":{"terms":"[3,8]","op":"-","num":6},"note":"The digit 6 is read, so the number in progress is 6."},{"at":{"i":7},"vars":{"terms":"[3,8,-6]","op":"/","num":0},"note":"The character / commits the number 6: the pending minus pushes the term -6."},{"at":{"i":8},"vars":{"terms":"[3,8,-3]","op":"/","num":2},"note":"The digit 2 is read, so the number in progress is 2, and the end of the tape commits it: the pending divide replaces the top term -6 by -3, and the terms 3, 8 and -3 sum to 8."}]}
```

The second trace evaluates `1-(4+(2-3))` with saved contexts. The minus before the first bracket becomes the saved sign, and the inside restarts at zero. When the innermost bracket closes with the value minus one, it is added to the saved result of the level around it, and that level's total of three is then subtracted from the saved one.

```trace
{"cells":["1","-","(","4","+","(","2","-","3",")",")"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"result":0,"sign":1,"saved":"[]"},"note":"The digit 1 is read, so the number in progress is 1."},{"at":{"i":1},"vars":{"result":1,"sign":-1,"saved":"[]"},"note":"The - commits the number 1 with its sign, so the level total is 1, and the next sign is -."},{"at":{"i":2},"vars":{"result":0,"sign":1,"saved":"[(1,-1)]"},"note":"An opening bracket saves the total 1 and the sign -, then the inside restarts at zero."},{"at":{"i":3},"vars":{"result":0,"sign":1,"saved":"[(1,-1)]"},"note":"The digit 4 is read, so the number in progress is 4."},{"at":{"i":4},"vars":{"result":4,"sign":1,"saved":"[(1,-1)]"},"note":"The + commits the number 4 with its sign, so the level total is 4, and the next sign is +."},{"at":{"i":5},"vars":{"result":0,"sign":1,"saved":"[(1,-1),(4,1)]"},"note":"An opening bracket saves the total 4 and the sign +, then the inside restarts at zero."},{"at":{"i":6},"vars":{"result":0,"sign":1,"saved":"[(1,-1),(4,1)]"},"note":"The digit 2 is read, so the number in progress is 2."},{"at":{"i":7},"vars":{"result":2,"sign":-1,"saved":"[(1,-1),(4,1)]"},"note":"The - commits the number 2 with its sign, so the level total is 2, and the next sign is -."},{"at":{"i":8},"vars":{"result":2,"sign":-1,"saved":"[(1,-1),(4,1)]"},"note":"The digit 3 is read, so the number in progress is 3."},{"at":{"i":9},"vars":{"result":3,"sign":-1,"saved":"[(1,-1)]"},"note":"A closing bracket finishes the inside with value -1, and the saved total plus the saved sign times that value gives 3."},{"at":{"i":10},"vars":{"result":-2,"sign":-1,"saved":"[]"},"note":"A closing bracket finishes the inside with value 3, and the saved total plus the saved sign times that value gives -2."}]}
```

<!-- stage: code -->
### Terms Stack And Bracket Contexts

```java
static long calculate(String s) {
    ArrayDeque<Long> terms = new ArrayDeque<>();
    long num = 0;
    char op = '+';
    for (int i = 0; i <= s.length(); i++) {
        char c = i < s.length() ? s.charAt(i) : '+';
        if (c >= '0' && c <= '9') { num = num * 10 + (c - '0'); continue; }
        if (c == ' ') continue;
        if (op == '+') terms.addLast(num);
        else if (op == '-') terms.addLast(-num);
        else if (op == '*') terms.addLast(terms.removeLast() * num);
        else terms.addLast(terms.removeLast() / num);
        op = c;
        num = 0;
    }
    long total = 0;
    for (long t : terms) total += t;
    return total;
}

static long calculateBrackets(String s) {
    ArrayDeque<long[]> saved = new ArrayDeque<>();
    long result = 0, num = 0;
    int sign = 1;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') num = num * 10 + (c - '0');
        else if (c == '+' || c == '-') { result += sign * num; num = 0; sign = c == '+' ? 1 : -1; }
        else if (c == '(') { saved.addLast(new long[] {result, sign}); result = 0; sign = 1; }
        else if (c == ')') {
            result += sign * num; num = 0;
            long[] outer = saved.removeLast();
            result = outer[0] + outer[1] * result;
        }
    }
    return result + sign * num;
}
```

Each character is read once and each term is pushed and popped at most once, so both methods run in O(n) time, with O(n) extra space for the stack of terms or contexts.

<!-- stage: applicability -->
### When Meaning Waits For The Next Token

Use a single left-to-right parse with saved state when numbers span several characters and the effect of an operator is delayed by precedence or by brackets. The invariant is that at each token boundary the number, the pending operator and the saved contexts give an exact meaning to the text read so far.

A false friend is splitting on spaces, which fails when spaces are optional and cannot represent brackets. A second false friend is applying each operator the moment it is read, which ignores precedence and gives `3+2*4` the value 20. A third is parsing numbers with `Integer.parseInt` on a substring without first deciding where the number ends, which breaks on a sign, a space or a bracket.

In Java, accumulate digits with `c - '0'` in a `long`, flush the last number at the end of the input by treating the end like one more operator, and remember that integer division truncates toward zero, so `-7 / 2` is `-3` and not `-4`. Decide in the grammar whether a minus after an operator or an opening bracket is a unary sign, and handle it where the sign is read.

<!-- stage: exercises -->
### Exercises

#### [Build] Signed Sum (Author exercise)
<!-- id: sq-signed-sum -->

**Prerequisites.** The Nested Decoding lesson.

**Problem.** The input is non-negative integers joined by `+` and `-`, with no spaces and no brackets. Return the value of the expression, reading multi-digit numbers whole.

**Constraints.** 1 <= s.length <= 100000, the expression starts with a digit, and every number is at most 1000000000.

**Example 1.** Input `s = "12+30-5"`, output `37`.

**Example 2.** Input `s = "100"`, output `100`.

**Hint.** When is a number complete? What must be done with the last number at the end of the text?

**Changed decision.** First rung: a number is committed when the next operator or the end arrives, and only plus and minus exist, so the sign is the whole pending state.

#### [Vary] Basic Calculator II (LeetCode 227)
<!-- id: sq-basic-calculator-two -->

**Prerequisites.** The Signed Sum rung.

**Problem.** The input is non-negative integers and the operators `+`, `-`, `*` and `/`, with optional spaces and no brackets. Evaluate it with the usual precedence. Division truncates toward zero. Every intermediate value fits in a signed 32-bit integer.

**Constraints.** 1 <= s.length <= 300000, every number is a non-negative integer, and the expression is valid and has no division by zero.

**Example 1.** Input `s = "10-8/3*2"`, output `6`.

**Example 2.** Input `s = " 7*3/4+1"`, output `6`.

**Hint.** Which operators may change a term that is already on the stack? When may a term be considered final?

**Changed decision.** Multiplication and division fold into the top term before lower-precedence terms are committed, so precedence is handled by what the stack allows to change.

#### [Boundary] Spaces And Unary Sign (Author exercise)
<!-- id: sq-spaces-unary-sign -->

**Prerequisites.** The Basic Calculator II rung.

**Problem.** The input uses `+`, `-`, integers and arbitrary spaces. A `+` or `-` is a unary sign when it is the first non-space character or comes immediately after another operator, ignoring spaces. Otherwise it is a binary operator. Return the value of the expression as a `long`.

**Constraints.** 1 <= s.length <= 100000, the expression is valid, and every number is at most 1000000000.

**Example 1.** Input `s = " -12 + 5 - -3 "`, output `-4`.

**Example 2.** Input `s = "7- +2"`, output `5`.

**Hint.** What was the last non-space character before this sign? What does an operator followed by a sign mean?

**Changed decision.** A sign that follows an operator or starts the text belongs to the next number, so the parser has to know whether it is between two operands before it gives the sign a meaning.

#### [Recognize] Basic Calculator (LeetCode 224)
<!-- id: sq-basic-calculator -->

**Prerequisites.** The Spaces And Unary Sign rung.

**Problem.** The input contains digits, `+`, `-`, round brackets and spaces. Evaluate the expression. A `-` may appear before a bracket and may also be unary at the start of a bracket's contents, as in `(-3+1)`. There is no multiplication or division.

**Constraints.** 1 <= s.length <= 300000, the expression is valid, and every intermediate value fits in a signed 32-bit integer.

**Example 1.** Input `s = "1 - (4 + (2 - 3))"`, output `-2`.

**Example 2.** Input `s = "-(2 + 3) + 10"`, output `5`.

**Hint.** What must be saved when a bracket opens, and how is the inside folded into the outside when it closes?

**Changed decision.** The result and the sign in front of the bracket are saved at an opening bracket, and the inside is folded in at the closing bracket.
