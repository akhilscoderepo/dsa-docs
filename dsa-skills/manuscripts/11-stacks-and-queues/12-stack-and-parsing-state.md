<!-- lesson-kind: combination -->
<!-- lesson-id: stack-and-parsing-state -->
## Stack And Parsing State

<!-- stage: context -->
### The Records Office Terminal

A records office has an old terminal that accepts four kinds of typed text, and a clerk has to answer questions about each one. The first is a price formula in the club's reverse order, where a cost is worked out by numbers followed by the operators that combine them. The second is a compressed storage note such as `3[ab2[c]]d`, which stands for a long run of characters and is never written out in full, because some notes describe more characters than the office could store in a lifetime. The third is a file path typed by hand, full of dots, double dots and doubled slashes. The fourth is a bracketed formula with plus and minus signs, where a minus can sit in front of a whole bracket.

The clerk has learned that each kind of text is read once, from left to right, and that in every kind some half-finished work must be put aside when a new level opens and picked up again when it closes. She is not sure what the four kinds share, or why her helper, who is good at splitting text on separators, keeps getting them wrong.

<!-- stage: contributions -->
### What Reading And Stacking Each Bring

The parser brings meaning. It decides how characters group into tokens, such as a multi-digit number, an operator, a bracket or a path component, and it knows where the reading stands in the grammar: whether a minus is a sign or an operation, whether a digit continues a count or begins one, whether a dot is a name or a command. By itself it holds no memory of what was set aside when a level opened.

The stack brings that memory. It keeps whatever cannot be resolved yet, such as operands waiting for an operator, a repeat count with the text of the level around it, the names of the directories entered so far, or the total and sign that surround a bracket. By itself the stack has no idea what its entries mean or when to push or pop, since that comes from the grammar.

The recognition cue is text read in one pass where some state must be saved at a token that opens a level and restored at the token that closes it.

<!-- stage: naive -->
### Scan Back And Mark Off Entries

The direct way to clean a path is to split it at the slashes, drop the empty and single-dot parts, and, for every double-dot part, walk backwards through the parts to find the nearest directory that has not been cancelled yet and cancel it.

```java
static String simplifyByScanning(String path) {
    String[] parts = path.split("/");
    boolean[] gone = new boolean[parts.length];
    for (int i = 0; i < parts.length; i++) {
        if (parts[i].isEmpty() || parts[i].equals(".")) gone[i] = true;
        else if (parts[i].equals("..")) {
            gone[i] = true;
            for (int j = i - 1; j >= 0; j--) if (!gone[j]) { gone[j] = true; break; }
        }
    }
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < parts.length; i++) if (!gone[i]) sb.append('/').append(parts[i]);
    return sb.length() == 0 ? "/" : sb.toString();
}
```

It is correct, because each double dot cancels the nearest directory still standing, and climbing above the root simply cancels nothing.

<!-- stage: bottleneck -->
### Backward Scans Repeat Themselves

Every double dot restarts a backward walk, and the walk steps over every part that was already cancelled. A path that goes down n directories and then climbs back with n double dots does at least n backward walks, and the later ones pass over a long stretch of cancelled entries, so the work is O(n^2). The same repeated search appears in the other three kinds of text. Finding the matching bracket of a group by walking backwards, or the operands of an operator by scanning for numbers, costs a rescan for every closing token.

The scans repeat because the program forgets what it saw on the way forward. When a part is read, the program already knows that it is the newest directory still open, so there is nothing to search for later if the open directories are kept in order of entry. The newest one is at the end, a double dot removes it, and a name adds a new one. One forward pass, with a stack of what is open, costs O(n).

<!-- stage: insight -->
### Read Meaning, Park What Is Open

Every one of the four texts follows the same loop. The reader works out the **token meaning** of what it has just read, which may need several characters, and then does one stack action chosen by the **grammar position**: push an operand, park a frame when a level opens, pop and combine when it closes, or append a name when a directory is entered. The stack holds the **saved parent state**, the unresolved remainder of every enclosing level, in the order in which the levels were opened.

For a postfix formula the grammar is trivial: a number is pushed, and an operator pops the right operand, then the left, and pushes the result, so the stack height is the number of values waiting. For a compressed note the saved parent state is a pair, the repeat count and the length so far of the enclosing level. For a path it is the list of open directory names, and a double dot pops one unless the stack is empty, which keeps the path from climbing above the root. For a bracketed formula it is the total and the sign in front of the bracket.

The invariant is that the stack contains exactly the unresolved state of the levels opened and not yet closed, innermost on top, and that the current variables describe the innermost level only. A parser without the stack loses the parent when a level opens, and a stack without a parser pushes and pops at the wrong characters.

<!-- names: token meaning, grammar position, saved parent state -->

Counting the stack's height as it grows gives the deepest nesting, and carrying lengths instead of text gives sizes that would never fit in memory as strings.

<!-- stage: variables -->
### Level State And Frames

For a postfix formula the stack `values` holds `long` operands, and `peak` is the largest size it reaches. For a compressed note the current level is a `long` length `cur`, the digits build `count`, and the frames hold a parent length and a count, so no text is built at all. For a path the deque `names` holds directory names, and the output is the names joined with slashes behind a leading slash. For a bracketed formula `result` and `sign` describe the current level, and each frame is a pair of those two numbers, with `deepest` recording the largest frame count. Lengths are capped by a constant, so that a length beyond the cap saturates and never wraps around.

<!-- stage: trace -->
### A Path And A Compressed Note

The first trace cleans the path `/a/./b/../c`, split into the parts a, a single dot, b, a double dot and c. The cells hold the parts, and `p` points at the one being read. The single dot does nothing, and the double dot removes b, the newest open directory, so only a and c remain. Look at the double dot: it works on the end of the stack, with no search at all.

```trace
{"cells":["a",".","b","..","c"],"pointers":["p"],"steps":[{"at":{"p":0},"vars":{"open":"/a"},"note":"The name a is entered, so it is added to the end of the stack."},{"at":{"p":1},"vars":{"open":"/a"},"note":"The single dot is the current directory, so nothing changes."},{"at":{"p":2},"vars":{"open":"/a/b"},"note":"The name b is entered, so it is added to the end of the stack."},{"at":{"p":3},"vars":{"open":"/a"},"note":"The double dot removes b, the newest open directory, from the end of the stack."},{"at":{"p":4},"vars":{"open":"/a/c"},"note":"The name c is entered, so it is added to the end of the stack."}]}
```

The second trace measures the note `3[ab2[c]]d` without building any text. The cells hold the characters, and `i` points at the one being read. At the first closing bracket the inner level has length 1, the repeat count 2 makes 2, and the parent level, which holds the length 2 for `ab`, becomes 4. At the second closing bracket, 4 is repeated three times, so the length is 12, and the final letter makes 13.

```trace
{"cells":["3","[","a","b","2","[","c","]","]","d"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"length":0,"parked":"[]"},"note":"The digit 3 is read, so the count in progress is 3."},{"at":{"i":1},"vars":{"length":0,"parked":"[(0,3)]"},"note":"An opening bracket parks the length 0 and the count 3, then starts a new level at length 0."},{"at":{"i":2},"vars":{"length":1,"parked":"[(0,3)]"},"note":"The letter a adds one to the current length, which is now 1."},{"at":{"i":3},"vars":{"length":2,"parked":"[(0,3)]"},"note":"The letter b adds one to the current length, which is now 2."},{"at":{"i":4},"vars":{"length":2,"parked":"[(0,3)]"},"note":"The digit 2 is read, so the count in progress is 2."},{"at":{"i":5},"vars":{"length":0,"parked":"[(0,3),(2,2)]"},"note":"An opening bracket parks the length 2 and the count 2, then starts a new level at length 0."},{"at":{"i":6},"vars":{"length":1,"parked":"[(0,3),(2,2)]"},"note":"The letter c adds one to the current length, which is now 1."},{"at":{"i":7},"vars":{"length":4,"parked":"[(0,3)]"},"note":"A closing bracket repeats the inner length 1 by 2, and the parent length 2 plus 2 gives 4."},{"at":{"i":8},"vars":{"length":12,"parked":"[]"},"note":"A closing bracket repeats the inner length 4 by 3, and the parent length 0 plus 12 gives 12."},{"at":{"i":9},"vars":{"length":13,"parked":"[]"},"note":"The letter d adds one to the current length, which is now 13."}]}
```

<!-- stage: code -->
### Four Texts, One Loop Shape

```java
static long[] rpnWithPeak(String[] tokens) {
    ArrayDeque<Long> values = new ArrayDeque<>();
    int peak = 0;
    for (String tok : tokens) {
        if (tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0) {
            long right = values.removeLast(), left = values.removeLast();
            values.addLast(tok.equals("+") ? left + right : tok.equals("-") ? left - right
                    : tok.equals("*") ? left * right : left / right);
        } else values.addLast(Long.parseLong(tok));
        peak = Math.max(peak, values.size());
    }
    return new long[] {values.removeLast(), peak};
}

static long decodedLength(String s, long cap) {
    ArrayDeque<long[]> frames = new ArrayDeque<>();
    long cur = 0, count = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') count = count * 10 + (c - '0');
        else if (c == '[') { frames.addLast(new long[] {cur, count}); cur = 0; count = 0; }
        else if (c == ']') {
            long[] f = frames.removeLast();
            long repeated = (f[1] == 0 || cur == 0) ? 0 : (cur > (cap + 1) / f[1] ? cap + 1 : f[1] * cur);
            cur = Math.min(f[0] + repeated, cap + 1);
        } else cur = Math.min(cur + 1, cap + 1);
    }
    return cur > cap ? -1 : cur;
}

static String simplifyPath(String path) {
    ArrayDeque<String> names = new ArrayDeque<>();
    for (String part : path.split("/")) {
        if (part.isEmpty() || part.equals(".")) continue;
        if (part.equals("..")) { if (!names.isEmpty()) names.removeLast(); }
        else names.addLast(part);
    }
    StringBuilder sb = new StringBuilder();
    for (String n : names) sb.append('/').append(n);
    return sb.length() == 0 ? "/" : sb.toString();
}

static long[] calculateWithDepth(String s) {
    ArrayDeque<long[]> saved = new ArrayDeque<>();
    long result = 0, num = 0;
    int sign = 1, deepest = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') num = num * 10 + (c - '0');
        else if (c == '+' || c == '-') { result += sign * num; num = 0; sign = c == '+' ? 1 : -1; }
        else if (c == '(') { saved.addLast(new long[] {result, sign}); deepest = Math.max(deepest, saved.size()); result = 0; sign = 1; }
        else if (c == ')') {
            result += sign * num; num = 0;
            long[] outer = saved.removeLast();
            result = outer[0] + outer[1] * result;
        }
    }
    return new long[] {result + sign * num, deepest};
}
```

Each loop reads every token once and pushes or pops at most once for it, so all four run in O(n) time, and the space is O(depth) for the three that save levels and O(n) for the path names.

<!-- stage: applicability -->
### Spotting A Parser With Memory

Reach for the pair when text is read in one pass and some state has to be set aside when a level opens and restored when it closes: nested groups, brackets, repeat notation, paths and formulas whose operators arrive after their operands. The invariant is that the stack holds exactly the unresolved state of the levels that are open, innermost on top, and the current variables describe the innermost level only.

A false friend is splitting the text on its separators, which cannot represent nesting and breaks as soon as a token is more than one character wide. A second false friend is a stack with no grammar, which pops at the wrong characters because it never decided what a token means. A third is rebuilding text at every level, when only a length or a count of levels was asked for.

In Java, check emptiness before every pop, since a malformed or boundary input such as a leading double dot reaches the empty stack, and decide in the contract whether that is an error or a no-op. Hold sums and lengths in `long`, saturate against an explicit cap when a size can explode, and compare tokens by exact text so that a name such as `...` is not mistaken for a command.

<!-- stage: exercises -->
### Exercises

#### [Build] Evaluate Reverse Polish With Peak (LeetCode 150)
<!-- id: sq-sp-rpn-with-peak -->

**Prerequisites.** The Infix And Postfix Evaluation lesson.

**Problem.** Given a valid postfix token array of integers and the four operators, return `[value, peak]`, where `value` is the result of the expression and `peak` is the largest number of values that were on the stack at the same time, measured after each token is processed. Division truncates toward zero.

**Constraints.** 1 <= tokens.length <= 10000, every integer token is between -1000 and 1000, and the expression is valid with no division by zero.

**Example 1.** Input `tokens = ["6", "2", "/", "4", "3", "-", "*"]`, output `[3, 3]`.

**Example 2.** Input `tokens = ["5"]`, output `[5, 1]`.

**Hint.** When does the stack grow, and when does it shrink? At which moment should its size be recorded?

**Changed decision.** The answer has a second component, so the stack height is measured while the sequence runs, and the operand order still comes from popping the right operand first.

#### [Vary] Decoded Length Without Building (LeetCode 394)
<!-- id: sq-sp-decoded-length -->

**Prerequisites.** The Evaluate Reverse Polish With Peak rung.

**Problem.** Given an encoded string of letters, counts and brackets, as in `k[encoded_string]`, return the length of the decoded string without building it. If the length is larger than 10^18, return -1. Counts may have several digits, and a count of zero makes its group empty even when the group inside is huge.

**Constraints.** 1 <= s.length <= 1000, every count is between 0 and 1000000000, and the string is well formed.

**Example 1.** Input `s = "3[ab2[c]]d"`, output `13`.

**Example 2.** Input `s = "1000000000[1000000000[1000000000[a]]]"`, output `-1`.

**Hint.** Which two numbers must a frame remember? What should happen to a length that passes the cap, and what if its count is zero?

**Changed decision.** Each frame stores a length and a count and no text, and lengths saturate at the cap instead of wrapping around in a `long`.

#### [Boundary] Simplify Path (LeetCode 71)
<!-- id: sq-sp-simplify-path -->

**Prerequisites.** The Decoded Length Without Building rung.

**Problem.** Given an absolute Unix-style path, return its canonical form. A single dot means the current directory, a double dot means the parent directory and cannot move above the root, several slashes count as one, and the result starts with one slash and has no trailing slash. A name made of three or more dots is an ordinary name.

**Constraints.** 1 <= path.length <= 3000, the path begins with `/`, and it consists of letters, digits, dots, underscores and slashes.

**Example 1.** Input `path = "/a/./b/../../c/"`, output `"/c"`.

**Example 2.** Input `path = "/../"`, output `"/"`.

**Hint.** What should a double dot do when no directory is open? How is a part equal to three dots recognized?

**Changed decision.** A double dot on the empty stack is ignored, so the path cannot climb above the root, and tokens are compared by exact text.

#### [Recognize] Basic Calculator With Depth (LeetCode 224)
<!-- id: sq-sp-calculator-depth -->

**Prerequisites.** The Simplify Path rung.

**Problem.** Given an expression of digits, `+`, `-`, round brackets and spaces, return `[value, deepest]`, where `value` is the result and `deepest` is the largest number of brackets open at once. A minus may precede a bracket or start a bracket's contents. Numbers can be as large as 10^12, so the value is a `long`.

**Constraints.** 1 <= s.length <= 100000, the expression is valid, every number is at most 1000000000000, and every intermediate value fits in a `long`.

**Example 1.** Input `s = "2-(5-(6+1))+(10-3)"`, output `[11, 2]`.

**Example 2.** Input `s = "-(-3+10)"`, output `[-7, 1]`.

**Hint.** What is saved when a bracket opens? Where is the count of open brackets taken?

**Changed decision.** The values are `long` and the answer carries the depth, which is the largest size of the saved-context stack.
