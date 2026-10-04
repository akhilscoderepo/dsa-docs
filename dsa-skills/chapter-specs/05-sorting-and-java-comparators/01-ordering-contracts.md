# Lesson spec: Compare Two Values Safely

**Recognition cue.** A problem asks for a deterministic order before any scan can make a local decision. **Java hazard.** Use `Integer.compare(a, b)` or `Long.compare(a, b)`; subtraction can overflow. **False friend.** Sorting primitive values cannot preserve custom-object tie behavior by accident.

- **Build - LC 912 Sort an Array.** Sort integers; state the required output order.
- **Vary - Author exercise: Sort Boxed Integers in Descending Order.** Sort an `Integer[]` with a safe reverse comparator, and explain why the same comparator overload does not accept `int[]`.
- **Boundary - Author exercise: Extreme Comparator.** Order `Integer.MIN_VALUE`, `0`, and `Integer.MAX_VALUE` without subtraction.
- **Recognize - LC 179 Largest Number.** The decisive comparator is concatenation order, not numeric order.
