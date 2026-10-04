# Lesson spec: Parse One Character At A Time

**Recognition cue.** Characters change a small parser state: digit, sign, decimal point, token boundary, or error. **State.** State variables record what has already been legally consumed. **False friend.** Nested scopes require a stack and arrive in Chapter 11.

- **Build - Author exercise: Parse a Signed Integer Token.** Consume an optional sign followed by one or more digits, and reject the token if any other character appears.
- **Vary - LC 8 String to Integer (atoi).** Consume optional sign and digits under explicit overflow rules.
- **Boundary - LC 65 Valid Number.** A decimal point and exponent each have placement rules; test `"."` and `"2e10"`.
- **Recognize - LC 165 Compare Version Numbers.** Parse components without converting an unbounded version to one integer.
