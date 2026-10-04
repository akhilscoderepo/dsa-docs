<!-- section: orientation -->
## Orientation

A greedy method makes a decision, keeps it, and never looks back. That sounds reckless, and in most problems it is. The subject of this chapter is the small family of problems in which it is not reckless, because a short argument shows that the decision just taken still leaves an optimal answer reachable. The skill being trained is therefore twofold. You learn to write the fast loop, and you learn to say why it is right, or to find the input that proves it wrong.

### What To Bring

Sorting with comparators from Chapter 05 is used in every lesson, and the interval vocabulary of Chapter 10 returns in the second one. The combination lessons draw on three further tools that were taught earlier: the priority queue of Chapter 17, the monotonic stack of Chapter 12, and the two-pointer motion of Chapter 08. Dynamic programming is not assumed. It belongs to Chapters 26 to 29, and the chapter says plainly where a problem that looks greedy has to be handed over to it.

### Nine Lessons In Two Groups

Five lessons teach the micro-patterns. The first treats a local choice with rooms and parties, and says what has to be true for the cheapest option to be safe. The second picks the largest set of events that do not overlap and counts the fewest arrows that touch every balloon. The third keeps a single reach number along a line of jumps, first for yes or no and then for the fewest jumps. The fourth is about the proof itself, and every exercise in it is an exercise in reasoning, with a swap to perform, a counterexample to find, and a proof to present. The fifth selects tasks under a capacity or a deadline and introduces retraction.

Four combination lessons follow. Ordering joins sorted keys to the proof, the heap lesson adds a priority queue for hindsight, the stack lesson adds a budget of permitted removals, and the pointer lesson settles one end of a sorted range at a time.

### Reading The Lessons

Each lesson starts with a short scene and a method that is correct but slow. Before reading the insight, name the repeated work in that slow method and guess which choice could be made once. When a trace is shown, say what the state means before reading the note beside it. When you reach an exercise, write the choice and the proof sentence first, and only then the code. The solution files run each method against an exhaustive or independent method on many small inputs, so a disagreement between your answer and a solution is worth tracing step by step.

### Where The Chapter Ends Up

You should be able to state, for any greedy rule, what the choice is, how a best answer is exchanged into it, why the exchanged answer stays legal, and what smaller problem remains. You should be able to build a small counterexample for a rule that fails, and to explain why the shortest-first rule does. You should know why a reach number describes everything that can be reached on a line, why retraction needs a heap, when a stack may pop, and why a pointer move discards an item rather than guessing. The review section poses scenarios, and a second attempt after some days is the best test.
