# Lesson spec: Stock Span

**Recognition cue.** For each new value, count the consecutive suffix ending here whose earlier values do not exceed it. **Invariant.** The stack stores decreasing price candidates paired with the span each candidate already summarizes. **False friend.** This asks for the full dominated run, not merely the nearest greater value.

- **Build - Author exercise: Span From Previous-Greater Index.** Compute `i - previousGreaterIndex` for an offline array.
- **Vary - Author exercise: Compressed Price-Span Pairs.** Pop dominated pairs and add their stored spans.
- **Boundary - Author exercise: Equal Prices.** Pop equality because equal earlier days belong to the current `<= price` span.
- **Recognize - LC 901 Online Stock Span.** Maintain the compressed monotonic state across successive API calls.
