# Lesson spec: Apply Transactions Without Partial Changes

**Recognition cue.** Calls create check-in state, balances, purchases, or inventory transitions. **Invariant.** Each accepted transaction has one complete before/after state and failed validation causes no partial mutation.

- **Build - LC 2043 Simple Bank System.** Validate accounts and balances before transfer.
- **Vary - LC 1396 Design Underground System.** Pair check-in/check-out state and aggregate route statistics.
- **Boundary - Author exercise: Duplicate Active Transaction.** Reject an entity already inside a lifecycle.
- **Recognize - LC 1357 Apply Discount Every n Orders.** Combine catalog lookup, order counting, and price calculation.
