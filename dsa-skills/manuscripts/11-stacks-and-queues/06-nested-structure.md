<!-- lesson-kind: standard -->
<!-- lesson-id: nested-structure -->
## Nested Structure

<!-- stage: context -->
### The Assembly Parts Catalogue

A bicycle maker keeps a parts catalogue written as one long line of text. A group in round brackets is an assembly, and an assembly can contain loose parts and smaller assemblies, which can contain smaller ones in turn. The wheel assembly holds a rim, spokes and a hub assembly, and the hub assembly holds bearings. The catalogue writer uses the brackets to show what belongs inside what.

The workshop manager wants numbers from this line: how deep the deepest assembly is, and a total cost where each part inside an assembly is charged a handling fee that doubles for every level of assembly around it. She also cares that the answer does not fall apart on a catalogue that nests a hundred thousand assemblies one inside another, which is a stress test the supplier once sent as a joke.

<!-- stage: naive -->
### Recurse On Each Group With A Rescan

The direct method is a recursive descent. To score a stretch of the line, scan it to split it into its top-level groups, and for each group recurse on the text between its brackets.

```java
static long scoreByRecursion(String s, int lo, int hi) {
    long total = 0;
    int i = lo;
    while (i < hi) {
        int depth = 0, j = i;
        do {
            depth += s.charAt(j) == '(' ? 1 : -1;
            j++;
        } while (depth > 0);
        long inner = scoreByRecursion(s, i + 1, j - 1);
        total += inner == 0 ? 1 : 2 * inner;
        i = j;
    }
    return total;
}
```

It is correct, since each group is found by counting to its closing bracket, and the value of a group depends only on the text inside it.

<!-- stage: bottleneck -->
### Every Level Rescans Its Whole Range

Each recursive call scans its own range to find where the groups end, and the next call scans the range inside, so a line of n characters that nests k levels deep scans about n, n minus 2, n minus 4 and so on, which is O(n^2) in the worst case. The recursion also uses one call frame per level, so a nesting of a hundred thousand levels needs a hundred thousand frames, and Java's call stack is not that deep. The supplier's joke catalogue ends the program with a `StackOverflowError` before it produces any answer.

The repeated scanning is avoidable because the characters are read in order and the inner groups finish before the groups that contain them. All the method needs while it reads is the unfinished state of each enclosing assembly. Keeping those states in an explicit stack, one entry per open level, makes a single pass enough, costs O(n) time, and moves the depth from the call stack to the heap, where it can be as large as memory allows.

<!-- stage: insight -->
### One Frame For Each Open Level

Give every open group a **level frame**: a small record of the unfinished state of that level, such as the running total of what has been seen inside it so far. A stack of such frames mirrors the nesting. Reading an opening bracket pushes a new empty frame, because a new level has begun and nothing is known about it yet. Reading a loose part updates the top frame only, since the part belongs to the innermost open assembly.

The decision that makes the method work is the **closing fold**. When a closing bracket arrives, the top frame is complete: nothing more can ever be added to it. Remove it, compute the value that the finished group is worth to its parent, which might be double its total, or a fixed one for an empty group, and add that value to the frame underneath. The **parent restore** is implicit in the stack: the frame below was untouched during the whole time the inner group was open, so after the pop it is exactly what it was when the inner group began, and the folded value is the only thing that changes it.

The invariant is that each frame on the stack holds the unresolved state of exactly one open level, with the innermost on top, and that frames below the top have not changed since their child level opened. A single global accumulator breaks this: when an inner group opens, the outer total is mixed with the inner one, and when the inner group closes, nothing remembers how much of the total belonged to the outer level.

<!-- names: level frame, closing fold, parent restore -->

When only the number of open levels is needed, such as the deepest nesting, the frames carry no data and the stack collapses to a counter of its height.

<!-- stage: variables -->
### A Stack Of Totals And A Counter

The stack `frames` holds one `long` total for each open level, with the bottom entry standing for the top level of the whole line, so it is created before any character is read. The variable `depth` equals the number of open groups, and `deepest` records the largest value of `depth` seen. An opening bracket pushes a zero, a closing bracket pops the top, converts it to the group's value, and adds that value to the new top, and a digit adds to the top. An unbalanced line is detected when a closing bracket would pop the bottom entry or when more than one entry remains at the end.

<!-- stage: trace -->
### Folding Groups Into Their Parents

The first trace scores the line `(()(()))` under the rule that an empty pair is worth one, two groups side by side add up, and a group around other groups is worth double their sum. Each cell is one character, and `i` shows where the reading stands. Two pairs complete inside the outer group, one directly and one inside another group, and the stack shows the totals of the open levels from the outside in. At the final bracket the outer frame holds three, and it is folded into the bottom entry as six.

```trace
{"cells":["(","(",")","(","(",")",")",")"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"saved":"[0]","current":0},"note":"An opening bracket saves the current total and starts a new level with zero."},{"at":{"i":1},"vars":{"saved":"[0,0]","current":0},"note":"An opening bracket saves the current total and starts a new level with zero."},{"at":{"i":2},"vars":{"saved":"[0]","current":1},"note":"A closing bracket finishes a group with inner total 0, which is worth 1, and the parent total becomes 1."},{"at":{"i":3},"vars":{"saved":"[0,1]","current":0},"note":"An opening bracket saves the current total and starts a new level with zero."},{"at":{"i":4},"vars":{"saved":"[0,1,0]","current":0},"note":"An opening bracket saves the current total and starts a new level with zero."},{"at":{"i":5},"vars":{"saved":"[0,1]","current":1},"note":"A closing bracket finishes a group with inner total 0, which is worth 1, and the parent total becomes 1."},{"at":{"i":6},"vars":{"saved":"[0]","current":3},"note":"A closing bracket finishes a group with inner total 1, which is worth 2, and the parent total becomes 3."},{"at":{"i":7},"vars":{"saved":"[]","current":6},"note":"A closing bracket finishes a group with inner total 3, which is worth 6, and the parent total becomes 6."}]}
```

The second trace reads the catalogue `1(2(3))4`, where each part is charged its own cost times two for every enclosing level. Look at the first closing bracket: the group holding 3 is complete, so the frame below it, which had collected only 2, receives twice 3, and the next closing bracket then folds that total into the frame holding 1.

```trace
{"cells":["1","(","2","(","3",")",")","4"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"saved":"[]","current":1},"note":"The part 1 is added to the innermost open level, so the current total becomes 1."},{"at":{"i":1},"vars":{"saved":"[1]","current":0},"note":"An opening bracket saves the total so far and starts a new level with zero."},{"at":{"i":2},"vars":{"saved":"[1]","current":2},"note":"The part 2 is added to the innermost open level, so the current total becomes 2."},{"at":{"i":3},"vars":{"saved":"[1,2]","current":0},"note":"An opening bracket saves the total so far and starts a new level with zero."},{"at":{"i":4},"vars":{"saved":"[1,2]","current":3},"note":"The part 3 is added to the innermost open level, so the current total becomes 3."},{"at":{"i":5},"vars":{"saved":"[1]","current":8},"note":"A closing bracket finishes a group worth 3, so the saved total receives twice that and the current total becomes 8."},{"at":{"i":6},"vars":{"saved":"[]","current":17},"note":"A closing bracket finishes a group worth 8, so the saved total receives twice that and the current total becomes 17."},{"at":{"i":7},"vars":{"saved":"[]","current":21},"note":"The part 4 is added to the innermost open level, so the current total becomes 21."}]}
```

<!-- stage: code -->
### Depth, Fee Total And Score

```java
static int deepestNesting(String s) {
    int depth = 0, deepest = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(') { depth++; deepest = Math.max(deepest, depth); }
        else if (c == ')') depth--;
    }
    return deepest;
}

static long feeTotal(String s) {
    ArrayDeque<Long> frames = new ArrayDeque<>();
    long acc = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(') { frames.addLast(acc); acc = 0; }
        else if (c == ')') acc = frames.removeLast() + 2 * acc;
        else acc += c - '0';
    }
    return acc;
}

static long scoreOfParentheses(String s) {
    ArrayDeque<Long> frames = new ArrayDeque<>();
    long top = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == '(') { frames.addLast(top); top = 0; }
        else top = frames.removeLast() + Math.max(2 * top, 1);
    }
    return top;
}
```

Every character causes one push, one pop or one addition, so the three methods run in O(n) time, and the two stack methods use O(depth) extra space, which is at most O(n) and lives on the heap and not on the call stack.

<!-- stage: applicability -->
### When Inner Work Must Finish First

Use a stack of frames when inner structures must be resolved before the structures around them, as in nested groups, assemblies, scopes and expressions. The invariant is that every frame holds the unresolved state of one open level, and the frames below the top are exactly as they were when the child level opened.

A false friend is one running total, which cannot tell the outer share from the inner share once a group has opened. A second false friend is a depth counter used where data must be carried, which is right for the deepest nesting and wrong for any value that must be restored at a closing bracket. A third is recursion on the nesting itself, which is clear and fails for deeply nested input.

In Java, push the saved total before resetting the working total, and pop in the reverse order, so that the pair of statements at `(` mirrors the pair at `)`. Use `long` for totals that can double at every level. Decide from the contract what an unbalanced line means before the first character is read, and reject it when a closing bracket arrives at the bottom frame or when frames remain at the end.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Parenthesis Depth (Author exercise)
<!-- id: sq-max-parenthesis-depth -->

**Prerequisites.** The Matching Delimiters lesson.

**Problem.** Given a balanced string of round brackets, return the largest number of groups that are open at the same time. Track the opened but unresolved levels as the string is read.

**Constraints.** 0 <= s.length <= 100000, and `s` is balanced and contains only round brackets.

**Example 1.** Input `s = "(()(()))"`, output `3`.

**Example 2.** Input `s = "()()"`, output `1`.

**Hint.** How many levels are open after each character? When does that number reach its largest value?

**Changed decision.** First rung: only the number of open levels is needed, so the stack is represented by its height.

#### [Vary] Sum Values By Nested Group (Author exercise)
<!-- id: sq-sum-by-nested-group -->

**Prerequisites.** The Maximum Parenthesis Depth rung.

**Problem.** The input is a string of single digits and round brackets. A group is worth the sum of the digits directly inside it plus twice the sum of the values of the groups directly inside it. The whole string counts as the outermost group, so its digits count once and every bracketed group inside it is doubled. Return the value of the whole string.

**Constraints.** 0 <= s.length <= 1000, the nesting depth is at most 20, `s` is balanced, and every other character is a digit.

**Example 1.** Input `s = "1(2)3"`, output `8`.

**Example 2.** Input `s = "(1(2))"`, output `10`.

**Hint.** What must be saved when a group opens, and how is it combined with the finished group when the group closes?

**Changed decision.** The parent total is saved at an opening bracket and restored at the closing bracket, where it absorbs the doubled value of the finished child.

#### [Boundary] Deep Single Chain (Author exercise)
<!-- id: sq-deep-single-chain -->

**Prerequisites.** The Sum Values By Nested Group rung.

**Problem.** Given a string of round brackets, return `[deepest, groups]`, the largest number of simultaneously open groups and the total number of groups. If the string is not balanced, because a closing bracket has nothing to close or some opening bracket is never closed, return `[-1, -1]`. The string may nest a hundred thousand levels deep, so the method must not recurse on the nesting.

**Constraints.** 0 <= s.length <= 200000 and every character is a round bracket.

**Example 1.** Input `s = "((()))"`, output `[3, 3]`.

**Example 2.** Input `s = "(()"`, output `[-1, -1]`.

**Hint.** Which two checks reject an unbalanced string? What happens to a call stack when recursion follows a chain of a hundred thousand levels?

**Changed decision.** The nesting is iterative, with explicit state, so the depth is limited by memory and not by the call stack, and both failure modes are rejected.

#### [Recognize] Score of Parentheses (LeetCode 856)
<!-- id: sq-score-of-parentheses -->

**Prerequisites.** The Deep Single Chain rung.

**Problem.** A balanced string of round brackets is scored by three rules: `()` is worth 1, the concatenation of two balanced strings is worth the sum of their scores, and `(A)` is worth twice the score of the balanced string `A`. Return the score of the whole string.

**Constraints.** 2 <= s.length <= 50 and `s` is a balanced string of round brackets.

**Example 1.** Input `s = "(()(()))"`, output `6`.

**Example 2.** Input `s = "()()"`, output `2`.

**Hint.** What does a finished group contribute to the group around it? What is the value of an empty group?

**Changed decision.** A completed group is resolved into the value its parent expects, which is one for an empty group and twice its content otherwise.
