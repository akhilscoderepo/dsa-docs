<!-- lesson-kind: standard -->
<!-- lesson-id: parsing-state -->
## Parsing State

<!-- stage: context -->
### A Clerk Checking Handwritten Amounts

A clerk reads amounts from handwritten forms, one mark at a time, and decides whether each entry is a number the accounting system can accept. Some entries are plain, like 42. Some carry a sign, like -17, or a decimal point, like 3.5, or a power of ten, like 2e10. Others are nonsense, like 4..2, 1e, or a lone dot. She reads from left to right and she does not look back.

After every mark she asks herself one question: given what I have read so far, is this still a legal beginning of a number, and if the entry ended here, would it be a complete one? A minus sign is fine at the start and wrong anywhere else. A dot is fine once. A letter `e` is fine only after some digits, and it demands more digits afterwards. She is not storing the whole entry. She remembers a few facts about it.

<!-- stage: naive -->
### Hand The Whole Entry To The Library

In Java the first idea is to let the library decide, and treat an exception as the answer no.

```java
static boolean validNumberByParsing(String s) {
    try {
        Double.parseDouble(s);
        return true;
    } catch (NumberFormatException e) {
        return false;
    }
}
```

On `"42"`, `"-17"`, `"3.5"` and `"2e10"` it says yes, and on `"4..2"` and `"abc"` it says no. It is three lines long and needs no thinking about states.

<!-- stage: bottleneck -->
### The Library Answers A Different Question

The call reads the string once, so it is O(n) in time, and cost is not the complaint. The complaint is that `Double.parseDouble` accepts more than the clerk's rules do. It accepts the words `NaN` and `Infinity`, a trailing type letter as in `1d` or `2f`, hexadecimal floating-point text, and surrounding spaces. A form containing `Infinity` would be accepted as a number. Failure is reported by throwing an exception, which builds a stack trace for every bad entry and is slow when most entries are bad.

The fix is not a faster library call. The contract is a particular small set of legal strings, and the code has to state that set. Describing it as a handful of facts about what has been read so far turns the contract into a loop with a few branches that run in O(n) and are easy to test one by one.

<!-- stage: insight -->
### A Few Facts About What Was Read

A **parser state** is a small summary of the characters consumed so far, just enough to decide what may come next. For a number the summary can be a few booleans: whether any digit has been seen, whether a decimal point has been seen, whether an exponent mark has been seen, and whether a digit has followed that exponent mark. Each new character either keeps the state legal, by moving to a new state, or breaks the rules, and the parse fails at once.

The characters consumed so far form a **legal prefix**, a string that could still be extended into a valid token. The invariant is that after every character, the state describes a legal prefix and nothing else has been remembered. At the end of the input, the token is valid only if the state is an **accepting state**, one in which the prefix is already a complete token. The digit `1` leaves the state accepting. The text `1e` is a legal prefix but not an accepting state, because an exponent needs digits after it.

<!-- names: parser state, legal prefix, accepting state -->

Many contracts need an extra decision about overflow. When a number is built digit by digit as `value * 10 + digit`, the multiplication can exceed the type before the loop ends. The safe rule checks before multiplying: if `value` is already larger than `(MAX - digit) / 10`, the next step would overflow, so stop and return the clamped limit. Checking afterwards is too late, because the wrapped value looks like a legitimate small number.

Parsing does not always produce a single number. Two version strings such as `1.02.0` and `1.2` are compared component by component. Each component is a run of digits, read between dots. Comparing components as digit strings, after dropping leading zeros, works even if a component is longer than any integer type, which converting the whole version to one number could never do.

<!-- stage: variables -->
### The Index, The Flags And The Value

The index `i` is the next unread character, and everything before it has been consumed under the rules. The flags record the state: `seenDigit`, `seenDot`, `seenExp`, and `digitAfterExp`, which starts true and turns false when an exponent mark appears, then true again at the next digit. A sign is legal only at the start or directly after an exponent mark, which is checked against the previous character. For integer parsing the state also holds `sign` and `value`. The characters read are never stored, only their effect on the state.

<!-- stage: trace -->
### One Legal Entry And One That Fails

Take `1.5e-3`. The first character, `1`, is a digit, so `seenDigit` becomes true. The `.` is allowed because no dot and no exponent has appeared, so `seenDot` becomes true. The `5` is another digit. The `e` is allowed because a digit has been seen and no exponent yet, so `seenExp` becomes true and `digitAfterExp` becomes false. The `-` is a sign directly after the exponent mark, so it is allowed. The last digit `3` sets `digitAfterExp` to true. The input ends with a digit seen and a digit after the exponent, so the state is accepting.

Now take `1e5.2`. The `1` is a digit and the `e` starts an exponent. The `5` is an exponent digit. The `.` arrives after an exponent mark, where a decimal point is illegal, so the parse fails at that character without reading the rest. The step to study is the failure: the string could not become valid by any later characters, so the scan stops immediately.

```trace
{"cells":["1",".","5","e","-","3"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"seenDigit":true,"seenDot":false,"seenExp":false,"digitAfterExp":true},"note":"Read '1', a digit. A digit has now been seen."},{"at":{"i":1},"vars":{"seenDigit":true,"seenDot":true,"seenExp":false,"digitAfterExp":true},"note":"Read '.', the first decimal point, which is legal."},{"at":{"i":2},"vars":{"seenDigit":true,"seenDot":true,"seenExp":false,"digitAfterExp":true},"note":"Read '5', a digit. A digit has now been seen."},{"at":{"i":3},"vars":{"seenDigit":true,"seenDot":true,"seenExp":true,"digitAfterExp":false},"note":"Read 'e'. The exponent now needs at least one digit after it."},{"at":{"i":4},"vars":{"seenDigit":true,"seenDot":true,"seenExp":true,"digitAfterExp":false},"note":"Read '-', a sign directly after an exponent mark, which is legal."},{"at":{"i":5},"vars":{"seenDigit":true,"seenDot":true,"seenExp":true,"digitAfterExp":true},"note":"Read '3', a digit. A digit has now been seen. The exponent has its digit."}]}
```

```trace
{"cells":["1","e","5",".","2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"seenDigit":true,"seenDot":false,"seenExp":false,"digitAfterExp":true},"note":"Read '1', a digit. A digit has now been seen."},{"at":{"i":1},"vars":{"seenDigit":true,"seenDot":false,"seenExp":true,"digitAfterExp":false},"note":"Read 'e'. The exponent now needs at least one digit after it."},{"at":{"i":2},"vars":{"seenDigit":true,"seenDot":false,"seenExp":true,"digitAfterExp":true},"note":"Read '5', a digit. A digit has now been seen. The exponent has its digit."},{"at":{"i":3},"vars":{"seenDigit":true,"seenDot":false,"seenExp":true,"verdict":"reject"},"note":"Read '.'. A decimal point after another point or after an exponent mark is illegal. The parse fails here."}]}
```

<!-- stage: code -->
### Flags, Clamp And Component Compare

```java
static boolean isNumber(String s) {
    boolean seenDigit = false, seenDot = false, seenExp = false, digitAfterExp = true;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') { seenDigit = true; digitAfterExp = true; }
        else if (c == '+' || c == '-') { if (i != 0 && s.charAt(i - 1) != 'e' && s.charAt(i - 1) != 'E') return false; }
        else if (c == '.') { if (seenDot || seenExp) return false; seenDot = true; }
        else if (c == 'e' || c == 'E') { if (seenExp || !seenDigit) return false; seenExp = true; digitAfterExp = false; }
        else return false;
    }
    return seenDigit && digitAfterExp;
}

static int atoi(String s) {
    int i = 0, n = s.length(), sign = 1, value = 0;
    while (i < n && s.charAt(i) == ' ') i++;
    if (i < n && (s.charAt(i) == '+' || s.charAt(i) == '-')) { if (s.charAt(i) == '-') sign = -1; i++; }
    while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
        int d = s.charAt(i) - '0';
        if (value > (Integer.MAX_VALUE - d) / 10) return sign == 1 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
        value = value * 10 + d;
        i++;
    }
    return sign * value;
}

static int compareVersions(String a, String b) {
    int i = 0, j = 0;
    while (i < a.length() || j < b.length()) {
        int si = i, sj = j;
        while (i < a.length() && a.charAt(i) != '.') i++;
        while (j < b.length() && b.charAt(j) != '.') j++;
        while (si < i && a.charAt(si) == '0') si++;           // drop leading zeros
        while (sj < j && b.charAt(sj) == '0') sj++;
        if (i - si != j - sj) return i - si < j - sj ? -1 : 1;
        for (; si < i; si++, sj++) if (a.charAt(si) != b.charAt(sj)) return a.charAt(si) < b.charAt(sj) ? -1 : 1;
        i++; j++;
    }
    return 0;
}
```

Each method reads every character a fixed number of times, for O(n) time and O(1) extra space. In `atoi` the overflow test happens before the multiplication, and the clamp value is the same for an exact result at the limit and for anything beyond it. A missing component in `compareVersions` is an empty digit run, which compares as zero after the leading-zero step, so `1.0` equals `1.0.0`.

<!-- stage: applicability -->
### When A Few Facts Decide Validity

Use parsing state when characters change a small summary, such as signs, digits, a dot, a boundary between tokens, or an error, and the contract names exactly which strings are legal. The invariant is that after every character, the state describes a legal prefix. Decide the accepting states before coding, and test them with the shortest inputs: the empty string, a lone sign, a lone dot.

The false friend is a library parser. `Double.parseDouble` and `Integer.parseInt` are convenient but follow their own grammar, which can be wider or narrower than the contract, and they report errors by exceptions. Another false friend is nested structure. Balanced parentheses or nested brackets need a record of what is still open, which grows with the depth, and that is a stack, taught in Chapter 11. A few flags cannot count nesting.

In Java, compare `char` values with ranges rather than `Character.isDigit` when the contract says ASCII digits. Check overflow before multiplying. Avoid `String.split` for tokens that can be large, since it allocates and a regular expression adds cost. For versions, compare components as digit strings if the contract does not bound their size.

<!-- stage: exercises -->
### Exercises

#### [Build] Parse a Signed Integer Token (Author exercise)
<!-- id: st-parse-signed-integer -->

**Prerequisites.** The indexed-scan lesson; the character test from Chapter 00.

**Problem.** A token is valid if it is an optional `'+'` or `'-'` followed by one or more digits, and nothing else. Return the integer value of a valid token, or report that the token is invalid.

**Constraints.** 0 <= token.length() <= 19 and a valid token has at most 18 digits, so the value fits in a `long`. Do not use a library parser.

**Example 1.** Input `token = "-205"`, output -205.

**Example 2.** Input `token = "12a"`, output invalid, since the letter breaks the token.

**Hint.** What must be true before any digit is read, and what must be true when the input ends? Which character is allowed only at index 0?

**Changed decision.** First rung: a few facts about what has been consumed replace the call to a library parser.

#### [Vary] String to Integer (atoi) (LeetCode 8)
<!-- id: st-atoi -->

**Prerequisites.** The signed-integer exercise above.

**Problem.** Implement an `atoi` that skips leading spaces, reads an optional sign, then reads digits until the first non-digit, and returns the value clamped to the 32-bit signed range. If no digits are read, return 0.

**Constraints.** 0 <= s.length() <= 200. Check overflow before multiplying, and do not use a library parser.

**Example 1.** Input `s = "   -42abc"`, output -42.

**Example 2.** Input `s = "99999999999"`, output 2147483647, the largest 32-bit value.

**Hint.** What happens to `value * 10 + digit` for a large value, and where must the test happen to catch it? What is the answer when the first character after the spaces is a letter?

**Changed decision.** The contract now stops at the first non-digit and clamps, so the overflow rule joins the state.

#### [Boundary] Valid Number (LeetCode 65)
<!-- id: st-valid-number -->

**Prerequisites.** The two exercises above.

**Problem.** Decide whether a string is a valid decimal number: an optional sign, digits with at most one decimal point and at least one digit, and an optional exponent `e` or `E` followed by an optional sign and at least one digit. Test the strings `"."` and `"2e10"` and show that a library parser accepts some strings this contract rejects.

**Constraints.** 1 <= s.length() <= 20 and `s` consists of digits, signs, dots and letters. Use a few flags and no regular expression.

**Example 1.** Input `s = "."`, output false, since no digit appears.

**Example 2.** Input `s = "2e10"`, output true.

**Hint.** Which flags must be set before an `e` is allowed? Where is a sign allowed, and where is a dot forbidden?

**Changed decision.** The tests target the placement rules for the point and the exponent, where each character is legal only in certain states.

#### [Recognize] Compare Version Numbers (LeetCode 165)
<!-- id: st-compare-versions -->

**Prerequisites.** All three exercises above.

**Problem.** Compare two version strings made of numeric components separated by dots. Components may have leading zeros, and a missing component counts as zero. Return -1 if the first is smaller, 1 if it is larger and 0 if they are equal. Components may be too long for any integer type.

**Constraints.** 1 <= each string length <= 500. Compare components as digit strings and do not convert a whole version to one integer.

**Example 1.** Input `a = "3.07.1", b = "3.7"`, output 1.

**Example 2.** Input `a = "0.9.9", b = "0.10"`, output -1.

**Hint.** How do you compare two digit runs without converting them? What does a run that does not exist mean for the comparison?

**Changed decision.** The state is two cursors, one per string, each reading a component at a time, with leading zeros skipped.
