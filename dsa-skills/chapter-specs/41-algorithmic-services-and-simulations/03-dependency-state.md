# Lesson spec: Update Values That Depend On Others

**Recognition cue.** Stored values may be literal or derived from other stored values. **Invariant.** Evaluation follows dependency edges and updates cannot leave cached derived state inconsistent.

- **Build - LC 1628 Design an Expression Tree With Evaluate Function.** Separate operator and operand node behavior.
- **Vary - LC 631 Design Excel Sum Formula.** Track cell references and range multiplicity.
- **Boundary - Author exercise: Dependency Cycle Policy.** Reject cycles or state the acyclic guarantee.
- **Recognize - LC 3484 Design Spreadsheet.** Parse formulas and resolve current cell values.
