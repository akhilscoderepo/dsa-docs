<!-- lesson-kind: standard -->
<!-- lesson-id: parsing-state -->
## Parse One Character At A Time

<!-- stage: context -->
### A Variable Name That Fails To Compile

A configuration tool lets users name their own variables. It copies each name into generated source code. A user names a variable `9lives`. The tool accepts the name, writes the code, and the compiler rejects the whole file with an error that points at generated lines the user never saw.

The check in the tool looked at every character and found nothing wrong. Each of `9`, `l`, `i`, `v`, `e` and `s` is allowed somewhere in a name. The rule depends on position, because a digit is legal in the middle of a name and illegal at the start. The question is how a loop remembers what it has already read, so that the same character gets a different verdict at different places.

<!-- stage: naive -->
### One Test For Every Character

The direct check applies the same test to every character. A name is valid when it is not empty and each character is a letter, a digit or an underscore.

```java
static boolean isIdentifier(String s) {
    if (s.isEmpty()) {
        return false;
    }
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (!(Character.isLetterOrDigit(c) || c == '_')) {
            return false;
        }
    }
    return true;
}
```

The method accepts `"count_2"` and rejects `"my-var"` and `""`, which is correct. It also accepts `"9lives"`, which the compiler rejects. It accepts `"café"` too, because the library call treats the accented letter as a letter.

<!-- stage: bottleneck -->
### The Verdict Depends On Position

```predict
The naive method gives every character the same test. For the input "9lives", what does it return, what does the correct answer say, and what must the loop remember to fix the answer?

It returns true, but the correct answer is false. The first character must be a letter or an underscore, and later characters may also be digits. The loop must remember whether it has consumed the first character yet, which takes one extra variable.
```

The naive loop has no memory between iterations. Each character gets its verdict from the character alone, so it cannot treat index 0 differently from index 5. The fix needs only one extra piece of information: whether the first character is already behind the loop. That piece does not change the cost. The loop still reads each character once in O(n) time and keeps a constant amount of data in O(1) space. The remaining work is a clean way to organize that memory, so that more rules can join it later without turning the loop into a pile of special cases.

<!-- stage: insight -->
### Let A Small Variable Record The Past

A parser reads text from left to right and keeps a variable that summarizes everything it has accepted so far. That variable is the parser **state**. The state does not store the text. It stores only the facts that decide what the next character may be.

#### Name The States Before Writing The Loop

For a variable name, two facts matter. In the state `START` the parser has read nothing, so only a letter or an underscore may come next. In the state `BODY` the parser has read a legal first character, so a letter, an underscore or a digit may come next. The parser starts in `START`.

<!-- names: state, transition, accepting -->

#### Each Character Causes One Transition

A **transition** moves the parser from its current state to the next state, based on the current state and the character at `i`. In `START`, a letter or underscore moves the parser to `BODY`. In `BODY`, a letter, underscore or digit keeps the parser in `BODY`. Every other pair of state and character is an error, and the method returns false at once. The loop never looks backward, because the state already holds everything the past contributes.

#### The End Decides Acceptance

A state is **accepting** when the text may end there and still be valid. For a variable name, only `BODY` is accepting. The empty string leaves the parser in `START`, so the method rejects it with no special case. After the loop, the method returns whether the state is accepting.

<!-- stage: variables -->
### State, Index And Character Class

Three values carry the whole parser, and each one changes at a fixed point.

- **state** holds `START` or `BODY` and changes only when a transition fires.
- **i** points at the character the parser reads next and moves right by one each round.
- **letter and digit tests** classify the character at `i` once per round with ASCII ranges, and the letter test also accepts an underscore.

<!-- stage: trace -->
### Parsing One Valid And One Invalid Name

#### A Valid Name

Take `s = "x_1"`. The parser starts in `START`. At `i = 0` the character `x` is a letter, so the parser moves to `BODY`. At `i = 1` the underscore is legal in `BODY`, so the parser stays there. At `i = 2` the digit `1` is also legal in `BODY`. The loop ends in `BODY`, which is accepting, so the answer is true.

#### An Invalid Name

Now take `s = "ab-c"`. The first two letters move the parser to `BODY` and keep it there. At `i = 2` the hyphen is neither a letter, an underscore nor a digit, so no transition exists. The method returns false at that index and never reads the final letter. The trace labels this outcome `REJECT`, which only marks that the method returned false. A digit at `i = 0` would fail in the same way, because `START` accepts no digit.

#### Stepping Through Both Names

```trace
{"cells":["x","_","1"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"state":"START"},"note":"Start: the parser has read nothing, so the state is START."},{"at":{"i":0},"vars":{"state":"BODY"},"note":"Index 0 holds 'x', a legal first character, so the state becomes BODY."},{"at":{"i":1},"vars":{"state":"BODY"},"note":"Index 1 holds '_', which is legal in BODY, so the state stays BODY."},{"at":{"i":2},"vars":{"state":"BODY"},"note":"Index 2 holds '1', which is legal in BODY, so the state stays BODY."},{"at":{"i":3},"vars":{"state":"BODY"},"note":"The index equals the length and the state is BODY, which is accepting, so the answer is true."}]}
```

```trace
{"cells":["a","b","-","c"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"state":"START"},"note":"Start: the parser has read nothing, so the state is START."},{"at":{"i":0},"vars":{"state":"BODY"},"note":"Index 0 holds 'a', a legal first character, so the state becomes BODY."},{"at":{"i":1},"vars":{"state":"BODY"},"note":"Index 1 holds 'b', which is legal in BODY, so the state stays BODY."},{"at":{"i":2},"vars":{"state":"REJECT"},"note":"Index 2 holds '-', which no transition allows in BODY, so the method returns false."}]}
```

<!-- stage: code -->
### A Loop With A State Variable

#### Checking A Variable Name

```java
static boolean isIdentifier(String s) {
    final int START = 0, BODY = 1;
    int state = START;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        boolean letter = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
        boolean digit = c >= '0' && c <= '9';
        if (state == START && letter) {
            state = BODY;
        } else if (state == BODY && (letter || digit)) {
            state = BODY;
        } else {
            return false;
        }
    }
    return state == BODY;
}
```

#### What The Loop Costs

The loop reads each character once and does a fixed number of comparisons per character, so it runs in O(n) time. It keeps a constant number of integers and booleans, so it uses O(1) space. The explicit ranges `'a'` to `'z'` and `'A'` to `'Z'` keep the test to ASCII, which fits the rule that a name uses only ASCII letters.

<!-- stage: applicability -->
### When A Small State Is Enough

#### Look For A Fixed List Of Situations

Use a state variable when the text follows a grammar with a fixed number of situations, such as before the sign, inside the digits, or after the decimal point. Signed numbers, version strings, simple tokens and fixed formats all fit. The invariant of the parser is that the state always summarizes the accepted prefix, so the next decision needs only the state and the current character. Write the states and the legal transitions on paper before writing the loop.

#### Nested Scopes Are A False Friend

A false friend in this lesson is a check that resembles a parsing loop and breaks its rule. Checking that every opening bracket has a matching closing bracket looks like a short loop with a counter or two. Brackets can nest to any depth, and the kinds must match in the right order, so a fixed number of states cannot record the open brackets. Such tasks need a stack, which a later chapter teaches.

#### Java Details That Cause Failures

The call `Character.isLetterOrDigit(c)` accepts letters and digits from other scripts, so ASCII rules need explicit range tests. The call `Integer.parseInt` accepts a leading `+`, rejects a leading space, and also accepts non-ASCII digits, so it cannot validate a token for a stated format. The call throws `NumberFormatException` on bad input. Integer arithmetic wraps silently, because `Integer.MAX_VALUE + 1` equals `Integer.MIN_VALUE`. A parser must test for overflow before it multiplies, and it must never test afterwards.

<!-- stage: exercises -->
### Exercises

#### [Build] Parse A Signed Integer Token (Author exercise)
<!-- id: st-signed-token -->

**Prerequisites.** The states, transitions and accepting states from this lesson.

**Problem.** Let `s` be a string. The string is a signed integer token when it has an optional sign `'+'` or `'-'` followed by one or more decimal digits and no other character. Return the value of the token as a `long`. Return `Long.MIN_VALUE` when `s` is not a signed integer token.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 18`.
- **Characters** are any Java `char` values; digits mean `'0'` through `'9'` only.
- **Value** fits in a `long`, because a token has at most 18 digits.
- **Rejection** returns `Long.MIN_VALUE`, and no valid token has that value.

**Example 1.** Input `s = "-408"`, output -408.

**Example 2.** Input `s = "+"`, output `Long.MIN_VALUE`, because a sign alone has no digit.

**Hint.** Which states does the parser need between the sign and the first digit, and which state accepts?

**Changed decision.** Basic case: the parser needs three states, and the sign leads to a state that is not accepting.

#### [Vary] String To Integer (LeetCode 8)
<!-- id: st-atoi -->

**Prerequisites.** The token parser above.

**Problem.** Let `s` be a string. Skip leading space characters. Then read an optional sign `'+'` or `'-'`. Then read the longest run of decimal digits, and stop at the first other character. Return the integer that the digits form, negated when the sign is `'-'`. Return 0 when no digit is read. When the value lies outside the range of a 32-bit signed integer, return the nearest bound of that range.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 200`.
- **Characters** are English letters, digits, `' '`, `'+'`, `'-'` and `'.'`.
- **Range** of the answer is `-2^31` to `2^31 - 1`.
- **Overflow** needs a check before the accumulator can exceed its type.

**Example 1.** Input `s = "   +17 apples"`, output 17.

**Example 2.** Input `s = "-2147483649x"`, output -2147483648, because the value is below the lower bound.

**Hint.** When must the loop stop reading digits, and which type can hold the accumulator until that moment?

**Changed decision.** The parser tolerates trailing text and clamps the value instead of rejecting it.

#### [Boundary] Valid Number (LeetCode 65)
<!-- id: st-valid-number -->

**Prerequisites.** The two parsers above.

**Problem.** Let `s` be a string. Return true when `s` is a valid decimal number. A valid number has an optional sign, then a mantissa, then an optional exponent. The mantissa is one or more digits with an optional single `'.'` anywhere among them, and it holds at least one digit. The exponent is `'e'` or `'E'`, then an optional sign, then one or more digits.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 20`.
- **Characters** are English letters, digits, `'+'`, `'-'` and `'.'`.
- **Exponent** holds an integer only, so no `'.'` follows an `'e'`.
- **Spaces** do not occur.

**Example 1.** Input `s = "-.5e+3"`, output true.

**Example 2.** Input `s = "."`, output false, because the mantissa has no digit.

**Hint.** Keep four yes-or-no facts: a digit was seen, a dot was seen, an exponent mark was seen, and a digit followed that mark. When is a sign legal, and which of the four facts decide acceptance at the end?

**Changed decision.** The parser tracks several independent facts, and acceptance depends on two of them at the end.

#### [Recognize] Compare Version Numbers (LeetCode 165)
<!-- id: st-compare-versions -->

**Prerequisites.** All three exercises above.

**Problem.** Let `v1` and `v2` be version strings. Each string holds integer components separated by single dots. Compare the components from left to right as integers, where leading zeros do not matter and a missing component counts as 0. Return -1 when `v1` is smaller, 1 when `v1` is larger and 0 when the versions are equal.

**Constraints.** The limits are:
- **Length** satisfies `1 <= v1.length(), v2.length() <= 500`.
- **Characters** are digits and `'.'` only, with no empty component.
- **Components** lie in `0` to `2^31 - 1` and may have leading zeros.
- **Method** parses each component directly from the string and never converts a whole version to one number.

**Example 1.** Input `v1 = "2.04.0"`, `v2 = "2.4"`, output 0.

**Example 2.** Input `v1 = "1.9"`, `v2 = "1.10"`, output -1.

**Hint.** What value does the parser return for a string that already ended, and how does each string keep its own index?

**Changed decision.** Two parsers run side by side, and each end of input behaves like the component 0.
