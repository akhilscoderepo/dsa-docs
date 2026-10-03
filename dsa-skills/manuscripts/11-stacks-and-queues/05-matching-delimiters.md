<!-- lesson-kind: standard -->
<!-- lesson-id: matching-delimiters -->
## Matching Delimiters

<!-- stage: context -->
### The Proofreader And The Brackets

A publisher's proofreader checks recipe cards before printing. A card may contain notes in round brackets, measurements in square brackets and optional steps in curly braces, and the notes can be nested inside each other, as in an optional step that contains a measurement that contains a note. A card is accepted only if every bracket that opens is closed by the matching kind, and the closings come in the reverse order of the openings, like boxes packed one inside another.

The proofreader is tired of counting. A card can have the same number of openings and closings and still be broken, because a closing round bracket sits where a square bracket should end. She wants a program that reads the card once, from left to right, and says whether it is acceptable.

<!-- stage: naive -->
### Erase Matching Pairs Until Nothing Is Left

The direct method repeatedly deletes every adjacent pair that looks like a matched pair, such as an opening round bracket immediately followed by its closing one. If the text can be erased completely, it was balanced.

```java
static boolean validByErasing(String s) {
    String current = s;
    while (true) {
        String next = current.replace("()", "").replace("[]", "").replace("{}", "");
        if (next.length() == current.length()) break;
        current = next;
    }
    return current.isEmpty();
}
```

It is correct, because an innermost matched pair is always adjacent, and removing it exposes the next level, so a balanced text shrinks to nothing and an unbalanced one gets stuck with a leftover.

<!-- stage: bottleneck -->
### One Layer Of Nesting Per Pass

Each pass walks the whole remaining string and removes only the pairs that are adjacent at that moment, which is the innermost layer. A card with depth d needs about d passes, and when the nesting is deep, such as thirty thousand openings followed by thirty thousand closings, there are thirty thousand passes of up to sixty thousand characters each, which is O(n^2) work. A hundred thousand characters of nested text would need billions of character visits, and each pass allocates a new string.

The passes repeat work because they forget what they have already seen. After the innermost pair is removed, the opening that was just before it is now adjacent to a closing, but the scan has to start from the left again to discover it. A reader who remembers the unmatched openings seen so far in order can pair each closing with the newest of them immediately, and the single left-to-right pass costs O(n).

<!-- stage: insight -->
### Remember What Is Still Open

Walk the text once and keep the **pending openers**, the openings that have not yet been closed, on a stack. Each opening is pushed. A closing symbol looks at the **nearest opener**, the top of the stack: if the stack is empty, or the top is the wrong kind, the text is broken at once, and otherwise the top is removed and the closing is satisfied. The stack is the right structure because a closing must pair with the most recent unresolved opening, which is exactly what the top holds.

The invariant is that the stack contains exactly the openings that have not yet been matched, in the order of their nesting, with the innermost on top. Reading one more character keeps this true: an opening joins the pending set, and a matching closing removes the innermost one. Counting alone cannot maintain such an invariant. The text `)(` has one opening and one closing, and an equal count passes while the order is plainly wrong, because the closing arrived while nothing was open.

The scan has two ways to fail and both must be checked. A closing that finds nothing to match, or the wrong kind on top, fails during the scan. After the last character, the **leftover test** applies: any opening still on the stack was never closed, so the text is broken even though no closing misbehaved. A text is accepted only if no closing failed and the stack is empty at the end.

<!-- names: nearest opener, leftover test, pending openers -->

The idea extends to any number of delimiter kinds without changing the loop, because the only new decision is a lookup that says which closing belongs to which opening.

<!-- stage: variables -->
### Stack Of Openers And A Lookup

The stack holds characters, or positions when an error has to be located, and the helper `partner` returns the opening that belongs to a closing symbol. For one kind of bracket the stack degenerates to a depth counter, and the counter is enough for validity but not for locating the matching opener. Depth is also the quantity needed to find outermost groups, since a group starts when the depth before an opening is zero and ends when the depth after a closing is zero. The loop variable `i` runs over the characters, and `ok` is false as soon as a closing is refused.

<!-- stage: trace -->
### A Clean Nest And A Crossed Pair

The first trace reads `[({})]`. The cells list the characters, with `i` marking the one in hand. The first three characters are pushed, the brace and the round bracket close in the order opposite to their opening, and the square bracket closes last. Look at the closing round bracket: the nearest opener is the round one, so the match succeeds and the stack shrinks to the square bracket.

```trace
{"cells":["[","(","{","}",")","]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[","result":"open"},"note":"The opening [ is pushed, so it becomes the nearest opener."},{"at":{"i":1},"vars":{"stack":"[(","result":"open"},"note":"The opening ( is pushed, so it becomes the nearest opener."},{"at":{"i":2},"vars":{"stack":"[({","result":"open"},"note":"The opening { is pushed, so it becomes the nearest opener."},{"at":{"i":3},"vars":{"stack":"[(","result":"open"},"note":"The closing } matches the nearest opener {, so that opener is removed."},{"at":{"i":4},"vars":{"stack":"[","result":"open"},"note":"The closing ) matches the nearest opener (, so that opener is removed."},{"at":{"i":5},"vars":{"stack":"","result":"empty"},"note":"The closing ] matches the nearest opener [, so that opener is removed."}]}
```

The second trace reads `([)]`, which has two openings and two closings of the right kinds in a wrong order. When the round closing arrives, the nearest opener is the square bracket, not the round one, so the match fails at once, and the scan stops without reading the rest.

```trace
{"cells":["(","[",")","]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"(","result":"open"},"note":"The opening ( is pushed, so it becomes the nearest opener."},{"at":{"i":1},"vars":{"stack":"([","result":"open"},"note":"The opening [ is pushed, so it becomes the nearest opener."},{"at":{"i":2},"vars":{"stack":"([","result":"broken"},"note":"The closing ) meets the nearest opener [, which is the wrong kind, so the text is broken."}]}
```

<!-- stage: code -->
### Match Kinds, Report The Position

```java
static boolean isBalanced(String s) {
    ArrayDeque<Character> open = new ArrayDeque<>();
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(' || c == '[' || c == '{') {
            open.addLast(c);
        } else {
            if (open.isEmpty() || open.removeLast() != partner(c)) return false;
        }
    }
    return open.isEmpty();
}

static char partner(char closing) {
    return closing == ')' ? '(' : closing == ']' ? '[' : '{';
}

static String removeOutermost(String s) {
    StringBuilder out = new StringBuilder();
    int depth = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == ')') depth--;
        if (depth > 0) out.append(c);
        if (c == '(') depth++;
    }
    return out.toString();
}
```

Each character is handled once with constant work, so both methods run in O(n) time, with O(n) extra space for the stack in the first and O(1) beyond the output in the second.

<!-- stage: applicability -->
### When The Newest Opening Closes First

Use a stack when every closing must match the most recent unresolved compatible opening, as in brackets, markup tags and nested quotations. The invariant is that the stack stores exactly the unmatched openings in nesting order, so that the top is always the one a closing must meet.

A false friend is the count of openings and closings, which accepts `)(` and `([)]`. A second false friend is a separate counter for each kind, which accepts the crossed pair `([)]` as well. A third is the erase-and-repeat method, which is correct but quadratic and allocates a string per pass.

In Java, guard every removal with an emptiness test, since `removeLast` on an empty deque throws `NoSuchElementException`. Store positions when the answer must name where the text broke, and do the leftover test after the loop. Compare characters with `==` on `char` values, and avoid comparing boxed `Character` objects by identity.

<!-- stage: exercises -->
### Exercises

#### [Build] One Bracket Type (Author exercise)
<!-- id: sq-one-bracket-type -->

**Prerequisites.** The BFS Queue State lesson.

**Problem.** Given a string of round brackets only, return whether every closing bracket matches an earlier opening bracket and none is left open. Push each opening and resolve each closing against the stack.

**Constraints.** 0 <= s.length <= 100000 and every character is `(` or `)`.

**Example 1.** Input `s = "(()())"`, output `true`.

**Example 2.** Input `s = "())("`, output `false`.

**Hint.** What does the stack hold after each character? What should happen when a closing finds the stack empty?

**Changed decision.** First rung: a single kind of bracket needs no kind lookup, and the stack records only that something is open.

#### [Vary] Valid Parentheses (LeetCode 20)
<!-- id: sq-valid-parentheses -->

**Prerequisites.** The One Bracket Type rung.

**Problem.** Given a string made of the six characters `(`, `)`, `[`, `]`, `{` and `}`, return whether every bracket is closed by the same kind of bracket and in the correct nesting order.

**Constraints.** 1 <= s.length <= 100000 and every character is a bracket.

**Example 1.** Input `s = "{[()]}"`, output `true`.

**Example 2.** Input `s = "([)]"`, output `false`.

**Hint.** Which opening belongs to a given closing? What makes the pair of the wrong kind?

**Changed decision.** The closing symbol must match the kind of the top of the stack, so the loop needs a lookup from closing to opening.

#### [Boundary] Premature Close And Leftover Open (Author exercise)
<!-- id: sq-premature-close-leftover -->

**Prerequisites.** The Valid Parentheses rung.

**Problem.** Given a string of the three bracket kinds, return -1 if it is balanced. Otherwise return the index of the first closing symbol that finds an empty stack or the wrong kind on top. If no closing fails but openings remain, return the index of the earliest opening that was never closed.

**Constraints.** 0 <= s.length <= 100000 and every character is a bracket.

**Example 1.** Input `s = "())"`, output `2`.

**Example 2.** Input `s = "(([]"`, output `0`.

**Hint.** What must the stack store so that the position of an opening can be reported? Which opening is the earliest leftover?

**Changed decision.** The stack stores positions, and the answer covers both failure modes: a failure during the scan and a leftover after it.

#### [Recognize] Remove Outermost Parentheses (LeetCode 1021)
<!-- id: sq-remove-outermost -->

**Prerequisites.** The Premature Close And Leftover Open rung.

**Problem.** A valid parentheses string is split into primitive groups, each of which is a valid string that cannot be split further. Remove the first opening and the last closing of every primitive group and return the resulting string.

**Constraints.** 2 <= s.length <= 100000, `s` consists of `(` and `)` only, and `s` is a valid parentheses string.

**Example 1.** Input `s = "(()())(())"`, output `"()()()"`.

**Example 2.** Input `s = "()()"`, output `""`.

**Hint.** What is the nesting depth just before a group opens and just after it closes? Which characters are at depth zero?

**Changed decision.** Only the depth of the stack matters, so the stack collapses to a counter that identifies where each group begins and ends.
