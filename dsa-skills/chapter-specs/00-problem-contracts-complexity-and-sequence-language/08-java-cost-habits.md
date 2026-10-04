# Lesson spec: Time Complexity Of Common Java Methods

**Recognition cue.** A Java library call appears inside a loop or silently changes representation. **State.** Include the API operation’s actual cost and semantics in the algorithm analysis. **Invariant.** Convenience syntax must not invalidate the target complexity or output contract. **False friend.** Familiar-looking APIs are not automatically constant time, primitive-friendly, or value-based.

- **Build - Author exercise: Front Removal.** Explain why repeatedly calling `ArrayList.remove(0)` over `n` elements performs quadratic shifting. Contrast it with maintaining a read index.
- **Vary - Author exercise: String Construction.** Compare `result = result + ch` in a loop with `StringBuilder.append(ch)`. Explain where repeated copying occurs.
- **Boundary - Author exercise: Primitive Arrays.** Evaluate `Arrays.asList(new int[]{1,2,3})`. State why the result is a one-element `List<int[]>`, not `List<Integer>`.
- **Recognize - Author exercise: Value Equality.** Compare two distinct `String` objects containing the same characters. Explain why `.equals` expresses value equality while `==` tests reference identity.
