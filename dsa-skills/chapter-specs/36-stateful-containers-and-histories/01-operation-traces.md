# Lesson spec: Trace A Sequence Of Method Calls

**Recognition cue.** The input is a constructor plus a chronological list of method calls. **Invariant.** Each completed call leaves a legal state for every possible next call.

- **Build - Author exercise: Bounded Counter API.** Specify constructor, increment, reset, and query behavior.
- **Vary - LC 1603 Design Parking System.** Keep independent capacity state per car type.
- **Boundary - Author exercise: Rejected Calls.** Prove failed operations leave all fields unchanged.
- **Recognize - LC 1656 Design an Ordered Stream.** Return exactly the newly contiguous suffix released by one insertion.
