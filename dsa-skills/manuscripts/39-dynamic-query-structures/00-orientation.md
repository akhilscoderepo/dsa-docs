<!-- section: orientation -->
## Orientation

A leaderboard service precomputes prefix sums so that any range total costs one subtraction. The first score correction arrives, and every stored prefix after that position is wrong. Rebuilding all of them on each correction turns a fast service into a slow one. This chapter teaches classes whose updates and queries share one object. Each lesson asks which summary the object keeps, which call repairs it, and how many calls the workload makes of each kind.

### Prerequisites

You should know prefix sums, Fenwick and segment trees, ordered maps, intervals, binary lifting, union-find and shortest paths. Four ideas appear without a full teaching pass. The lessons introduce a **modular inverse** (the number that undoes a multiplication modulo a prime), **lazy propagation** (a node stores a pending change for its whole range and applies it to children only when a call needs them) and **skip lists** (sorted linked lists stacked in levels). They expect you to recall **Kruskal's algorithm**, which builds a minimum spanning forest by adding the cheapest edge that joins two components, and the **Boyer-Moore majority vote**, which finds a candidate that may hold more than half the votes. A **mutation** is a call that changes stored state. A **query** is a call that reads an answer from that state. The **update-to-query ratio** is how many mutations the workload makes for each query. Every exercise states that ratio and says whether the calls are known before the first one runs, because both facts decide the design.

### What Each Lesson Protects

Each lesson names one fact that every public call must leave true.

- **Mutable Range Queries** keeps every tree entry equal to the sum of the range it owns.
- **Interval Unions** keeps stored ranges disjoint, ordered and written with one endpoint rule.
- **Ordered Structures** keeps keys sorted and every higher-level node also present on level 0.
- **Deferred Transforms** keeps pending operations composed in call order.
- **Query Planning** keeps a summary that answers every query without rereading the original data.
- **Dynamic Graph Queries** keeps every returned distance consistent with all accepted edges.
- **Ordered Interval State** joins sorted search with coverage counting over very large coordinate ranges.
- **Preprocessed Query APIs** joins ancestor, position and path indexes under a stated workload.

### Reading Order

Every lesson opens with a class that passes small tests and then fails on a realistic workload. You predict the failure before the reasoning appears. Two traces follow the state call by call, then Java code and the limits of the idea. The four exercises climb from a basic build to a variation, an edge case and a recognition problem. A **false friend** is a design that looks like the pattern but breaks its precondition. Solutions check each class against a slow, obviously correct **oracle** on random inputs.

### What You Can Do After This Chapter

You can pick a structure for a class from its call mix instead of from habit. You can state the endpoint rule of an interval API before writing a comparison. You can say when a precomputed index must be rebuilt and when an incremental repair is cheaper. The base trees belong to chapter 31, and the ordered sets belong to chapter 32.
