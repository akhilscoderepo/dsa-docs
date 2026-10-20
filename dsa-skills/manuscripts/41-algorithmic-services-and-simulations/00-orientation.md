<!-- section: orientation -->
## Orientation

A tic-tac-toe class rereads the whole board after every move, and a test with a 3 by 3 board passes. A server then hosts a 1000 by 1000 board. Each move checks every one of the million cells four times, which is about four million reads, so 100 000 moves make about four hundred billion reads, and the class runs out of time. The moves are all legal and the answers are all right. The cost per call is the only defect.

This chapter teaches small services whose public calls must stay fast and stay consistent. Each lesson names the authoritative state, the indexes derived from it, and the order in which one call may change them.

### Keep All State In Memory

Every problem here runs in one process with one caller at a time. All data lives in memory, sizes have stated limits, and a call either finishes or reports a failure value. Persistence, networking and several threads are outside the contract. Some contracts here are the chapter's own, so they may differ from the LeetCode statement of the same name.

### Prerequisites

You should know hash maps, tree sets, heaps, tries from earlier chapters and the multi-index records of chapter 40, where one record feeds several lookup structures. An **authoritative state** is the one record that decides what is true. A **derived index** is a structure rebuilt from that record to answer one query fast. A **precondition** is a fact that must hold before a call may change anything.

### What Each Lesson Protects

- **Move Pieces On A Board** keeps the position, the occupancy and the counters in agreement after every accepted move.
- **Resolve Paths In A Tree** gives every reachable node one parent and one normalized path.
- **Update Values That Depend On Others** keeps cached values equal to a fresh evaluation.
- **Merge Feeds From Many Sources** applies visibility before the output limit.
- **Apply Transactions Without Partial Changes** leaves the object unchanged when any check fails.
- **Answer Prefix Queries With A Trie** keeps a number on every prefix of every stored key.
- **Track Status And Pick The Next Task** lets the status table overrule every queue entry.
- **Rank Words By Prefix** keeps a short ranked list at every prefix node.
- **Keep Several Indexes In Step** sends every change through a single writer.

### Reading Order

Each lesson opens with a problem you recognize, then shows a simple class that passes small tests, and you predict where it breaks before the explanation. The explanation names the bottleneck and the insight that removes it, then lists the state that each call reads and writes. Two traces follow, then Java code, then a section on when the pattern applies. That section ends with false friends. A **false friend** is a design that resembles the pattern and violates one of its conditions. Four exercises close the lesson in the order build, vary, edge case and recognition. The last two lessons combine the earlier ones, and each adds a section after its opening that says what the earlier lessons contribute.

### What You Can Do After This Chapter

You can state which structure is authoritative before you write a method. You can order the checks and writes of a call so that a failure changes nothing. You can pick a trie, a heap or a status table by the query that the class must answer.
