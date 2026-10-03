# Lesson spec: Infix And Postfix Evaluation

**Recognition cue.** Operators must be applied either from explicit postfix order or after infix precedence has been made explicit. **Invariant.** In postfix evaluation, the value stack contains completed operands; for a binary operator, pop right before left. **False friend.** Reversing operand order is invisible for addition but breaks subtraction and division.

- **Build - Author exercise: Evaluate One Postfix Operator.** Compute tokens `a b op` with correct operand order.
- **Vary - LC 150 Evaluate Reverse Polish Notation.** Process arbitrary valid postfix tokens with one value stack.
- **Boundary - Author exercise: Non-Commutative Trace.** Test `8 3 -` and integer division with negative values under Java semantics.
- **Recognize - Author exercise: Convert Simple Infix To Postfix.** Use an operator stack for `+`, `-`, `*`, and `/`, then evaluate with the already learned postfix engine.
