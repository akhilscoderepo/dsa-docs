<!-- section: orientation -->
## Orientation

A tic-tac-toe class scans the whole board after every move, and a test with a 3 by 3 board passes. A grader then sends a board of 100 000 by 100 000 cells and the same class runs out of time. The moves are all legal and the answers are all right. The cost per call is the only defect.

This chapter teaches small services whose public calls must stay fast and stay consistent. Each lesson names the authoritative state, the indexes derived from it, and the order in which one call may change them.

### Bounded In-Memory Contract

Every problem here runs in one process with one caller at a time. All data lives in memory, sizes have stated limits, and a call either finishes or reports a failure value. Persistence, networking and several threads are outside the contract.

### Prerequisites

You should know hash maps, tree sets, heaps, tries from earlier chapters and the indexes of chapter 40. An **authoritative state** is the one record that decides what is true. A **derived index** is a structure rebuilt from that record to answer one query fast. A **precondition** is a fact that must hold before a call may change anything.

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

Each lesson opens with a class that passes small tests and breaks under a real workload, and you predict the break before the explanation. Two traces follow, then Java code and a section on false friends. A **false friend** is a design that resembles the pattern and violates one of its conditions. Four exercises follow in the order build, vary, edge case and recognition. The last two lessons combine the earlier ones.

### What You Can Do After This Chapter

You can state which structure is authoritative before you write a method. You can order the checks and writes of a call so that a failure changes nothing. You can pick a trie, a heap or a status table by the query that the class must answer.
