<!-- lesson-kind: combination -->
<!-- lesson-id: parse-with-a-stack -->
## Stack And Parsing State

<!-- stage: context -->
### One Stack, Four Different Texts

A developer maintains a small tool that reads four kinds of text. The first is a formula written with the operator last, such as `7 2 - 3 *`. The second is a compressed string such as `2[a3[b]]`. The third is a file path such as `/home/user/../docs/./a.txt`. The fourth is an arithmetic line such as `-(x+4)-y` with named variables. The developer writes one stack loop for the formula, and it works on the valid examples. Testing all four texts with that loop, and copies of it, produces four different bugs. The formula `7 2 ^` is accepted silently. The compressed string loses its repeat count. The path `/..` crashes on an empty stack. The arithmetic line `-(x+4)` returns the wrong sign.

The stack loop was the same each time, so the loop is not what differs. The code stage shows two of the texts, the path and the formula, and the exercises add the compressed string and the line with named variables. The traces follow the path and the compressed string, and the compressed string carries a limit on its decoded length. The task here is to answer one question. For each of the four texts, what must the reading step decide, and what must the stack remember so that the decision can be finished later?

<!-- stage: contributions -->
### What Each Earlier Idea Adds

Two earlier ideas combine in this lesson, and each supplies a different half. The stack lessons supply saved state. When a reader meets a part of the text that cannot be finished yet, it stores what it needs on a stack and continues. The most recent unfinished part is always on top, so the reader finishes parts in the reverse order of starting them. The stack alone does not say what to store.

The reading lessons supply the decision about each piece of text. A reader turns characters into numbers, signs, names and brackets, and it decides whether a piece starts a new level, finishes one or only adds to the current one. Reading alone cannot keep a parent level alive while a child level runs. Each text needs the reading rule to say what the piece means and the stack to hold the unfinished parent.

<!-- stage: naive -->
### Rewrite The Text Until Nothing Changes

Without a stack, the developer rewrites the text in place. For the path, the method splits it into components and then repeatedly looks for a name followed by `..`. It deletes both and starts the scan again from the left.

```java
static String simplifyByRewriting(String path) {
    List<String> parts = new ArrayList<>();
    for (String p : path.split("/")) if (!p.isEmpty() && !p.equals(".")) parts.add(p);
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int i = 0; i < parts.size(); i++) {
            if (!parts.get(i).equals("..")) continue;
            parts.remove(i);
            if (i > 0) parts.remove(i - 1);
            changed = true;
            break;
        }
    }
    return "/" + String.join("/", parts);
}
```

For `/a/./b/../../c/` the parts are `a`, `b`, `..`, `..`, `c`. The first pass removes `b` and `..`, the second removes `a` and `..`, and the result is `/c`. The method is correct. The same idea works for the compressed string by expanding the innermost bracket first, and for the arithmetic line by evaluating the innermost parentheses first.

<!-- stage: bottleneck -->
### Counting The Rescans

```predict
A path has n/2 directory names followed by n/2 `..` components. The method above removes one pair per pass and restarts from index 0. About how many components does it examine in total?

About n squared divided by 8. Each pass walks past all the remaining names before it finds the first `..`, so the examined count shrinks slowly while the pair count grows to n/2.
```

Each pass costs O(n), because the scan restarts at index 0 and walks past every name that is still waiting. Each pass also calls `remove`, which shifts the later elements. There are n/2 passes, so the total is O(n^2). For n equal to 100,000 that is on the order of one billion element visits for a path of one hundred thousand components.

The same shape appears in the other three texts. Expanding the innermost bracket and rescanning the whole string costs O(n) per bracket pair. The method also misses the contract questions. It does not say what happens when `..` has nothing to remove, or when a formula has too few operands. A method that reads each piece once needs a stack to hold the unfinished part.

<!-- stage: insight -->
### Read Once And Save The Unfinished Part

#### The Reading Step Names Each Token

A **token** is the smallest piece of text that has one meaning. In a postfix formula a token is a number or an operator. In a compressed string it is a digit, a letter, an opening bracket or a closing bracket. In a path it is the text between two slashes. In an arithmetic line it is a number, a variable name, a sign or a parenthesis. The reading step assigns a meaning to each token from the token alone and from the position in the text.

<!-- names: token, frame, clamp -->

#### The Stack Holds One Frame Per Open Level

A **frame** is what the reader pushes when a level opens, and it holds what the reader needs to continue after that level closes. The group that directly contains a given group is its **parent**. A compressed string pushes a pair of the text before the bracket and the repeat count. A path pushes one name for each open directory. An arithmetic line pushes a pair of the result before the parenthesis and the sign in front of it. A postfix formula opens no levels, so its stack holds finished values and no frames. When a level closes, the reader pops one frame and combines it with the finished level.

#### The Contract Decides Empty And Bad Cases

The contract says what happens when a pop finds nothing. In a path, `..` at the top level must **clamp**, so it does nothing, because the root has no parent. In a postfix formula an operator with fewer than two values is an error. In a compressed string a closing bracket without a frame is an error. The contract also says what an unknown token means. In a compressed string the contract can also set a **limit** on the decoded length, so an oversized expansion becomes a rejection. Each rule is a decision of the reading step, and the stack only stores what the decision needs.

#### Validate Before Any Push Or Pop

The reader inspects each token and the stack depth before any change. A closing bracket needs a waiting frame, an operator needs two operands on hand, and a repeat needs a projected length within the limit. When an inspection fails, the reader reports a malformed input, and the stored contents stay as they were.

<!-- stage: variables -->
### What The Reader And The Stack Carry

The reader and the stack share these pieces of state.

- **stack** is the last-in, first-out store of frames, and its top is the innermost unfinished level.
- **token** is the current piece of text, and the reader classifies it before any stack operation.
- **frame** is the unit pushed at a level start and popped at the level end.
- **current** is the value of the level being read, such as the running result or the running text.
- **limit or error flag** is the contract's rejection state, and it stops the reader at the first bad token.

The stack changes at level boundaries, while `current` changes at every token.

<!-- stage: trace -->
### Walking A Path And A Compressed String

#### A Path With Two Parent Moves

The path is `/a/./b/../../c/`. After the slashes are removed, the components are `a`, `.`, `b`, `..`, `..` and `c`. The pointer `i` marks the component in use, and `stack` lists the open names from the root outward. The component `.` changes nothing. Each `..` pops one name. A name pushes itself. The final stack gives the path.

```trace
{"cells":["a",".","b","..","..","c"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[a]"},"note":"The name a goes on the stack."},{"at":{"i":1},"vars":{"stack":"[a]"},"note":"The component . names the current directory, so the stack stays the same."},{"at":{"i":2},"vars":{"stack":"[a, b]"},"note":"The name b goes on the stack."},{"at":{"i":3},"vars":{"stack":"[a]"},"note":"The component .. pops b, so the path moves to its parent."},{"at":{"i":4},"vars":{"stack":"[]"},"note":"The component .. pops a, so the path moves to its parent."},{"at":{"i":5},"vars":{"stack":"[c]"},"note":"The name c goes on the stack."}]}
```

#### A Bounded Compressed String

The text is `2[a3[b]]` and the limit on the decoded length is 10. The variable `cur` is the text of the level being read, `num` is the repeat count being read, and `frames` holds the saved pairs, each written as the parent text in quotes and the repeat count. A closing bracket checks the new length against the limit before it builds the text.

```trace
{"cells":["2","[","a","3","[","b","]","]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"cur":"\"\"","num":2,"frames":"[]"},"note":"The digit 2 makes num 2."},{"at":{"i":1},"vars":{"cur":"\"\"","num":0,"frames":"[(\"\", 2)]"},"note":"[ saves the parent text \"\" and the count 2, then starts an empty level."},{"at":{"i":2},"vars":{"cur":"\"a\"","num":0,"frames":"[(\"\", 2)]"},"note":"The letter a extends cur to \"a\"."},{"at":{"i":3},"vars":{"cur":"\"a\"","num":3,"frames":"[(\"\", 2)]"},"note":"The digit 3 makes num 3."},{"at":{"i":4},"vars":{"cur":"\"\"","num":0,"frames":"[(\"\", 2), (\"a\", 3)]"},"note":"[ saves the parent text \"a\" and the count 3, then starts an empty level."},{"at":{"i":5},"vars":{"cur":"\"b\"","num":0,"frames":"[(\"\", 2), (\"a\", 3)]"},"note":"The letter b extends cur to \"b\"."},{"at":{"i":6},"vars":{"cur":"\"abbb\"","num":0,"frames":"[(\"\", 2)]"},"note":"] computes the length 1 + 3 * 1 = 4, which is within the limit 10, then builds the text."},{"at":{"i":7},"vars":{"cur":"\"abbbabbb\"","num":0,"frames":"[]"},"note":"] computes the length 0 + 2 * 4 = 8, which is within the limit 10, then builds the text."}]}
```

<!-- stage: code -->
### Writing A Path Reader And Checked Pop

#### Path Components On A Stack

As in the first lesson, the code uses the last end of the deque, with `addLast` to push and `removeLast` to pop. The method clamps `..` at the root by testing for an empty stack before it pops.

```java
static String simplifyPath(String path) {
    Deque<String> open = new ArrayDeque<>();
    for (String part : path.split("/")) {
        if (part.isEmpty() || part.equals(".")) continue;
        if (part.equals("..")) { if (!open.isEmpty()) open.removeLast(); }
        else open.addLast(part);
    }
    if (open.isEmpty()) return "/";
    StringBuilder sb = new StringBuilder();
    for (String name : open) sb.append('/').append(name);
    return sb.toString();
}
```

#### A Pop That Reports An Empty Stack

A checked operator step tests the stack size before it pops. It returns false when fewer than two values wait, so the caller can reject the text with an error code and not throw. A postfix reader calls it as `if (!applyOperator(values, tok.charAt(0))) return "ERR";`. This short version handles three operators, and division adds the zero-divisor test of the exercise.

```java
static boolean applyOperator(Deque<Long> values, char op) {
    if (values.size() < 2) return false;
    long right = values.removeLast();
    long left = values.removeLast();
    values.addLast(op == '+' ? left + right : op == '-' ? left - right : left * right);
    return true;
}
```

Both methods run in O(n) time and use O(n) space, because each token is pushed at most once and popped at most once.

<!-- stage: applicability -->
### Choosing The Frame For A New Text

#### Ask What Cannot Finish Yet

The invariant of this lesson says that each unfinished level has exactly one frame on the stack, with the innermost level on top. To choose the frame for a new text, ask which information is still needed after the current level closes. If the answer is a value, store the value. If the answer is a count and a prefix, store both. If the answer is a sign and a running result, store both.

#### A Stack Alone Is A False Friend

A stack of plain values is a false friend for nested text. It fits a postfix formula, and it fails for `2[a3[b]]`, because a value stack loses the repeat count and the text before the bracket. A stack also does not define the grammar. The text `a b` and the text `ab` differ in the reading step, not in the stack. The contract decides the empty case, the unknown token and the limit.

#### When A Stack Does Not Fit

A text that needs a lookup of an earlier unmatched piece by value asks for another structure. A stack that drops entries by comparison is taught in a later chapter. A text whose parts may end in any order, not the reverse of starting order, also does not fit one stack.

<!-- stage: exercises -->
### Exercises

#### [Build] Postfix With Error Codes (LeetCode 150)
<!-- id: sq-rpn-checked -->

**Prerequisites.** The postfix evaluation from the previous lesson.

**Problem.** This contract differs from the earlier evaluation of postfix text. A token array is meant to be a postfix expression. A token is a number when it is an optional minus sign followed by digits and it fits in an `int`. A token is an operator when it is exactly `+`, `-`, `*` or `/`. Any other token is unknown. Return the decimal value of the expression as a `String`. Return `"ERR"` instead when the token array has an unknown token, when an operator has fewer than two values, when more than one value remains at the end, when a division has a zero divisor, or when any intermediate value leaves the `int` range. Division truncates toward zero.

**Constraints.** The limits are:
- **Length** is `0 <= tokens.length <= 10^4`.
- **Tokens** are non-empty strings of at most 12 characters.
- **Empty array** is an error and returns `"ERR"`.
- **Return** is `"ERR"` or the decimal value of the final result.

**Example 1.** Input `["7","2","-","3","*"]`, output `"15"`.

**Example 2.** Input `["6","3","%"]`, output `"ERR"`, because `%` is an unknown token.

**Hint.** Keep the values as `long`, so a product of two `int` values cannot overflow before the range test. When does the final stack size prove that the expression is complete?

**Changed decision.** The reader rejects bad input at the first bad token and does not assume a valid expression.

#### [Vary] Decode With A Length Limit (LeetCode 394)
<!-- id: sq-decode-bounded -->

**Prerequisites.** The first exercise and the saved parent text of a nested group.

**Problem.** This contract differs from the earlier decoding of nested groups. An encoded string is built from lowercase letters and groups of the form `k[text]`. The decoded group is `text` repeated `k` times. Given the encoded string and an integer `limit`, return the decoded string, or return `null` when the decoded string would be longer than `limit`. The method must reject an oversized result before it builds any text longer than `limit`.

**Constraints.** The limits are:
- **Encoded length** is `1 <= s.length() <= 100`.
- **Counts** satisfy `1 <= k <= 300`, and the text inside brackets is not empty.
- **Limit** satisfies `1 <= limit <= 10^6`.
- **Input** is a valid encoding, with balanced brackets and a count before every opening bracket.
- **Return** is the decoded `String` or `null`.

**Example 1.** Input `s = "2[a3[b]]c"` with `limit = 20`, output `"abbbabbbc"`.

**Example 2.** Input `s = "2[3[abc]]"` with `limit = 10`, output `null`, because the decoded length is 18.

**Hint.** Before a closing bracket builds the repeated text, compute the new length as the parent length plus the count times the inner length. Which numeric type holds the product safely?

**Changed decision.** The closing bracket checks the length first, so a hostile input such as five nested counts of 300 returns `null` at once and does not allocate.

#### [Boundary] Simplify A Unix Path (LeetCode 71)
<!-- id: sq-simplify-path -->

**Prerequisites.** The two exercises above.

**Problem.** Given an absolute Unix-style path, return its canonical form. A single period `.` means the current directory and is dropped. A double period `..` means the parent directory and removes the previous name when one exists. Repeated slashes count as one slash. The canonical path starts with one slash, separates names with one slash, and has no trailing slash unless the path is the root alone. A component with three or more periods is an ordinary name.

**Constraints.** The limits are:
- **Length** is `1 <= path.length() <= 3000`.
- **Characters** are letters, digits, periods, underscores and slashes.
- **Start** of the path is always a slash.
- **Root** has no parent, so `..` at the root leaves the root unchanged.

**Example 1.** Input `"/a/./b/../../c/"`, output `"/c"`.

**Example 2.** Input `"/../...//x/"`, output `"/.../x"`, because `..` at the root changes nothing and `...` is a name.

**Hint.** Keep the names in a `String` array and an `int` count of how many are open. Empty text and `.` change nothing. What must the code check before it lowers the count for `..`?

**Changed decision.** The stack is an array with a top count and no deque, so a parent move at the root is the test that the count is above 0.

#### [Recognize] Calculator With Named Variables (LeetCode 224)
<!-- id: sq-calc-variables -->

**Prerequisites.** All three exercises above.

**Problem.** This contract differs from the earlier calculator with parentheses. The expression contains lowercase variable names, non-negative integers, the signs `+` and `-`, parentheses and spaces. A minus sign may also be a unary minus when it is the first sign of the expression or comes right after an opening parenthesis. A unary minus applies to the number, variable or parenthesized group that follows it. Parallel arrays `names` and `values` give the value of each variable. Return the value of the expression, or `null` when it uses a variable that `names` does not contain.

**Constraints.** The limits are:
- **Length** is `1 <= s.length() <= 10^5`.
- **Names** are non-empty lowercase strings, and the array `names` holds no duplicates.
- **Numbers** are digit sequences that fit in an `int`.
- **Validity** means the expression is well formed, and all values and results fit in an `int`.
- **Return** is an `Integer`, which is `null` for an undefined variable.

**Example 1.** Input `s = "-(x+4)-y"` with `x = 3` and `y = 5`, output -12.

**Example 2.** Input `s = "7-(k-(2+1))"` with only `k = 10`, output 0; with no variables defined, output `null`.

**Hint.** Read a name as a token like a number, then look it up. When the reader meets an opening parenthesis, which two values must it save?

**Changed decision.** The reading step now has a third kind of token, and an unresolved name rejects the whole expression.
