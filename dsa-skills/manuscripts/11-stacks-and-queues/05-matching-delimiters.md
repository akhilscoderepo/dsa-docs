<!-- lesson-kind: standard -->
<!-- lesson-id: matching-delimiters -->
## Check That Brackets Match In Order

<!-- stage: context -->
### A Line With Equal Counts Fails

A JSON parser reads the text `[1, {2]}` and reports an error. A quick count shows one `[`, one `{`, one `]` and one `}`, so every symbol has a partner somewhere. The parser still stops at the `]`, because the opening that is still unfinished at that point is `{`, and a `]` cannot close it. Compilers, linters and formatters make this same check before they read anything else. The check must work in one pass over the text. How does the code remember which opening a closing symbol has to match?

<!-- stage: naive -->
### Delete Matched Pairs Until Nothing Changes

A direct method removes every adjacent matched pair and repeats until the text stops changing. A text is valid when the final text is empty.

```java
static boolean validByDeleting(String s) {
    String t = s;
    while (true) {
        String u = t.replace("()", "").replace("[]", "").replace("{}", "");
        if (u.equals(t)) return t.isEmpty();
        t = u;
    }
}
```

The text `[1, {2]}` without its digits becomes `[{]}`. No adjacent pair exists, so the method returns false. The method is correct for all inputs made of brackets.

<!-- stage: bottleneck -->
### Why Repeated Deletion Slows Down

```predict
Take 50,000 `(` characters followed by 50,000 `)` characters. How many rounds does the deleting method run, and about how many characters does it read in total?

It runs 50,000 rounds, because each round removes only the one pair in the middle. The rounds read about 2.5 billion characters in total. Each round rebuilds a text that is only two characters shorter than the round before.
```

Each round of the method scans and copies the whole remaining text, and a round can remove as little as one pair. A text of `n` characters can need `n / 2` rounds. The total work is therefore O(n^2) time, and each round also allocates a new string of up to `n` characters.

The repeated work is the search for the pair that is ready to delete. After the deleting method removes a pair, the new adjacent pair sits exactly where the removed pair was. The method forgets that position and scans from the left again. A single pass that keeps the unfinished openings in memory never needs a second look at any character.

<!-- stage: insight -->
### Keep The Unfinished Openings In Order

#### What The Scan Must Remember

Read the text from left to right. An opening symbol has no answer yet, so the scan keeps it. A closing symbol has an answer immediately, because it must match the most recent opening that is still unfinished. The scan therefore needs a collection where the last item added is the first item removed.

<!-- names: stack, pending, mismatch -->

#### The Stack Holds The Pending Openings

A **stack** is a collection that adds and removes items at one end, so the last item added leaves first. The scan pushes each opening symbol on the stack. An opening that has been pushed and not yet removed is **pending**. At every position the stack holds exactly the pending openings, with the oldest at the bottom and the newest on top. That sentence is the invariant of the whole method.

#### Three Ways A Text Fails

A closing symbol pops the newest pending opening, and the pair must be compatible. A **mismatch** happens when the popped opening is not the partner of the closing symbol, as with `{` and `]`. The text also fails when a closing symbol finds the stack empty, because no opening is waiting for it. The third failure appears after the last character, when the stack still holds pending openings. The text is valid only when none of the three failures occurs.

<!-- stage: variables -->
### The State Of The Scan

The scan keeps four pieces of state.

- **stack** holds the pending openings. A push adds an opening, and a pop removes the newest one.
- **i** is the index of the character under test. It moves forward by one each step.
- **c** is the character at index `i`. It is either an opening or a closing symbol.
- **partner** is the opening symbol that belongs to a closing symbol. It is fixed by the pairs `()`, `[]` and `{}`.

<!-- stage: trace -->
### Two Texts Through The Stack

#### A Valid Nested Text

The first text is `([]{})`. The cells are its six characters, and the pointer `i` marks the character under test. The scan pushes `(` and then `[`. The `]` pops `[`, which is its partner, so one pending opening leaves. The scan pushes `{`, and `}` pops it. The final `)` pops `(`, and the stack is empty at the end. The text is valid.

```trace
{"cells":["(","[","]","{","}",")"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[(]","char":"("},"note":"( is an opening, so the scan pushes it."},{"at":{"i":1},"vars":{"stack":"[(, []","char":"["},"note":"[ is an opening, so the scan pushes it."},{"at":{"i":2},"vars":{"stack":"[(]","char":"]","popped":"["},"note":"] pops [, which is its partner."},{"at":{"i":3},"vars":{"stack":"[(, {]","char":"{"},"note":"{ is an opening, so the scan pushes it."},{"at":{"i":4},"vars":{"stack":"[(]","char":"}","popped":"{"},"note":"} pops {, which is its partner."},{"at":{"i":5},"vars":{"stack":"[]","char":")","popped":"("},"note":") pops (, which is its partner."},{"at":{"i":6},"vars":{"stack":"[]","result":"true"},"note":"The text ends with an empty stack, so the result is true."}]}
```

#### Equal Counts With The Wrong Order

The second text is `([)]`. It holds two openings and two closings, so a count would accept it. The scan pushes `(` and `[`. The `)` arrives and pops `[`, because `[` is on top. The partner of `)` is `(`, so the scan finds a mismatch at index 2 and stops. The stack still holds the older `(`, and the scan returns false without reading the rest of the text.

```trace
{"cells":["(","[",")","]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[(]","char":"("},"note":"( is an opening, so the scan pushes it."},{"at":{"i":1},"vars":{"stack":"[(, []","char":"["},"note":"[ is an opening, so the scan pushes it."},{"at":{"i":2},"vars":{"stack":"[(]","char":")","popped":"["},"note":") pops [, and the partner of ) is (. This is a mismatch, so the scan stops with false."}]}
```

<!-- stage: code -->
### Writing The Scan In Java

#### The Scan Method

The method uses `ArrayDeque<Character>` as the stack. It checks `isEmpty()` before each `pop()`, because `pop()` on an empty deque throws `NoSuchElementException`. It compares `char` values and not `Character` objects, so the `!=` test compares values.

```java
static boolean isBalanced(String s) {
    ArrayDeque<Character> stack = new ArrayDeque<>();
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(' || c == '[' || c == '{') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) return false;
            char open = stack.pop();
            if (open != partnerOf(c)) return false;
        }
    }
    return stack.isEmpty();
}

static char partnerOf(char close) {
    if (close == ')') return '(';
    if (close == ']') return '[';
    return '{';
}
```

#### Cost Of The Scan

Each character causes at most one push or one pop, and each of those takes O(1) time. The scan runs in O(n) time. The stack holds at most `n` characters, so it needs O(n) space in the worst case, for example in a text made only of openings.

<!-- stage: applicability -->
### When The Stack Is The Right Tool

#### Recognize The Cue

Use a stack when each closing symbol must pair with the most recent unfinished opening. The invariant is that the stack holds the pending openings in nesting order. HTML tags, JSON braces, function-call frames and undo steps all follow this shape. The cue is a rule that an inner item must finish before the item that contains it.

#### Equal Counts Are A False Friend

A count of openings and closings per type looks like a complete check, and it is a false friend. It accepts `([)]` and `)(`, because counts carry no order. A single running depth number is a related false friend for texts with several bracket types. The number says how many openings are pending and does not say which types they are.

#### When A Counter Is Enough

A text with one bracket type needs no stack. A depth counter that goes up on `(` and down on `)` holds the same information as the stack size. The method must reject a depth below zero and a final depth above zero. Do not use a stack for a problem where closings may match any earlier opening, because the rule above then no longer holds.

<!-- stage: exercises -->
### Exercises

#### [Build] One Bracket Type (Author exercise)
<!-- id: sq-one-bracket-type -->

**Prerequisites.** The scan with an `ArrayDeque` in this lesson.

**Problem.** A string made of `(` and `)` is balanced when repeated removal of an adjacent `()` pair reduces it to the empty string. Given such a string `s`, return true if it is balanced and false otherwise.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are only `(` and `)`.
- **Return** is a `boolean`, and the empty string is balanced.
- **Mutation** is not allowed; the string does not change.

**Example 1.** Input `(()())`, output true.

**Example 2.** Input `)(`, output false, although the string has one opening and one closing.

**Hint.** Push each `(`. What must the stack contain when a `)` arrives, and what must it contain after the last character?

**Changed decision.** Basic case: one bracket type, so each closing symbol needs only a nonempty stack.

#### [Vary] Three Delimiter Types (LeetCode 20)
<!-- id: sq-three-delimiter-types -->

**Prerequisites.** The exercise above.

**Problem.** A string made of `(`, `)`, `[`, `]`, `{` and `}` is valid when every opening has a closing of the same type, and the pairs close in the reverse order of their openings. Given a string `s`, return true if it is valid.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are only the six bracket characters.
- **Return** is a `boolean`, and the empty string is valid.
- **Mutation** is not allowed; the string does not change.

**Example 1.** Input `{[()]}[]`, output true.

**Example 2.** Input `{[}]`, output false, because the `}` meets `[` as the newest pending opening.

**Hint.** Store the opening symbols. Which opening must the popped item equal for each closing symbol?

**Changed decision.** The stack top must be compared with the partner of the closing symbol, and not only popped.

#### [Boundary] Premature Close And Leftover Open (Author exercise)
<!-- id: sq-premature-close-leftover -->

**Prerequisites.** The two exercises above.

**Problem.** Given a string `s` of bracket characters, return -1 when `s` is valid. Otherwise return the index of the first closing symbol that cannot be matched, either because the stack is empty or because its partner differs from the newest opening. When no such closing symbol exists and openings are still pending after the scan, return the index of the newest pending opening.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are only the six bracket characters `()[]{}`.
- **Return** is an `int` index, or -1 for a valid string.
- **Mutation** is not allowed; the string does not change.

**Example 1.** Input `())(`, output 2, because the second `)` finds an empty stack.

**Example 2.** Input `[(()`, output 1, because the `(` at index 1 is the newest opening still pending at the end.

**Hint.** Push the index of each opening, and not only the character. What does the stack hold when the scan ends without an early failure?

**Changed decision.** Both failure kinds must return a position, so the stack stores indices.

#### [Recognize] Remove Outermost Parentheses (LeetCode 1021)
<!-- id: sq-remove-outermost -->

**Prerequisites.** The one-type scan and the depth counter remark in this lesson.

**Problem.** A balanced string is primitive when it is nonempty and cannot be split into two nonempty balanced strings. Every balanced string is a concatenation of primitive strings. Given a balanced string `s`, remove the first `(` and the last `)` of every primitive piece and return the concatenation of the results.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are only `(` and `)`, and `s` is balanced.
- **Return** is a `String`, empty when every piece has length 2.
- **Mutation** is not allowed; the string does not change.

**Example 1.** Input `((()))()(())`, output `(())()`, because the three pieces keep only their inner parts.

**Example 2.** Input `()()`, output the empty string, because both pieces have length 2.

**Hint.** The depth of a character is the number of pending openings before it. Which `(` has depth 0 before it, and which `)` has depth 0 after it?

**Changed decision.** The stack content is not needed, only its size, so a depth counter replaces the stack.
