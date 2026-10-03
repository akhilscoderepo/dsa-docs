# Lesson spec: Calculator And String Parsing

**Recognition cue.** Characters form multi-digit numbers and operators whose effect may be delayed by precedence or parentheses. **Invariant.** At each token boundary, the parser has a precise meaning for the accumulated number, pending sign/operator, and saved parent context. **False friend.** Splitting on spaces fails when spaces are optional or parentheses are present.

- **Build - Author exercise: Signed Sum.** Parse multi-digit integers joined by `+` and `-`.
- **Vary - LC 227 Basic Calculator II.** Resolve multiplication and division before committing lower-precedence terms.
- **Boundary - Author exercise: Spaces And Unary Sign.** Distinguish a binary operator from a leading or post-parenthesis unary sign under the chosen grammar.
- **Recognize - LC 224 Basic Calculator.** Save the outer result and sign at `(`, then fold the completed inner expression at `)`.
