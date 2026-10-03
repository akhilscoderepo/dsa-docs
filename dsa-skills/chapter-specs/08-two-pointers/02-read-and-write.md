# Lesson spec: Read And Write

**Recognition cue.** One pointer reads unresolved input while another marks the next output position or retained boundary. **Invariant.** The written prefix already satisfies the final contract. **False friend.** A sliding window’s left boundary removes state from a range; a write pointer constructs output.

- **Build - LC 27 Remove Element.** Revisit stable compaction as explicit read/write pointer movement.
- **Vary - LC 283 Move Zeroes.** Write stable nonzero values, then repair the suffix.
- **Boundary - LC 26 Remove Duplicates from Sorted Array.** Handle empty input and one-element runs.
- **Recognize - LC 80 Remove Duplicates from Sorted Array II.** The read pointer advances normally; the admission rule consults the kept prefix.
