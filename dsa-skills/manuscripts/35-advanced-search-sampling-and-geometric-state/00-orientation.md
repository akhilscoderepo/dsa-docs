<!-- section: orientation -->
## Orientation

A coupon tool must pick the best subset of 40 items for a budget, and a loop over every subset never finishes. A promotion engine must choose one winner at random, and its winners cluster at the start of the list. A map app must find a route fast, and its shortcut sometimes returns a slower road. Each problem has a correct method that is neither the first idea nor an exotic one. This chapter teaches six such methods for search that must split its work, and for random choices that must stay fair.

### Prerequisites

You should know binary search, sorting, heaps, shortest paths with a priority queue, and the Fenwick tree from the range-query chapter. A **uniform** choice gives every allowed outcome the same chance. A **distribution** states the chance of each outcome. An **expected** cost is the average cost over the random draws for a fixed input. Every lesson passes the source of randomness into the method as a parameter, so tests can script each draw and check each probability by counting.

### What Each Lesson Protects

Each lesson names one fact that stays true for the whole run.

- **Meet In Middle** keeps a one-to-one map between full choices and pairs of half choices.
- **A Star Search** keeps the priority of every queued entry at or below the cost of the best route.
- **Reservoir Sampling** keeps every item seen so far equally likely to be held.
- **Weighted Selection** keeps one owner for every ticket from 1 to the total weight.
- **Rejection Sampling** keeps every draw uniform over the larger region and the test independent of the draw.
- **Randomized Partitioning** keeps the wanted rank inside the active range after every round.
- **Randomized Sampling State** keeps the chance of each eligible item equal to its weight over the eligible total.
- **A-Star Heuristics** keeps the guess below the true remaining cost and handles a negative reduced weight by reopening.

### Reading Order

Every lesson opens with a program that passes short tests and fails on larger inputs or on a statistical check. You predict the failure before the reasoning appears. Two traces follow the variables step by step, then Java code and the limits of the idea. The four exercises climb from a basic build to a variation, an edge case and a recognition problem. A **false friend** is a method that looks like the pattern but breaks its precondition. Solutions check each class against an **oracle**, a slow but obviously correct version, and count outcomes over every possible draw sequence where the sizes are small.

### What You Can Do After This Chapter

You can tell from a limit of 40 that two half enumerations are the intended method. You can attach a guess to a shortest-path search and test it before trusting it. You can write the chance of one item as a fraction before you code a random pick, and you can name the denominator. Randomized state that changes between calls, such as shuffles, belongs to the streaming chapter that precedes this one.
