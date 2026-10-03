<!-- section: orientation -->
## Orientation

A linked list stores order in references instead of positions, and that single fact changes how every operation is judged. There is no index to jump to, so a position costs a walk. There is also no neighbour to protect a node from a careless edit, so a single wrong assignment can leave the rest of the list unreachable. This chapter treats the chain as a set of moves that are safe because of an invariant: before each link is overwritten, the node it led to is held by another reference. From that one idea come reversal, merging, cycle detection, shared tails, midpoints, and gaps measured from the end.

### What To Bring

You should be comfortable with loops and references in Java, with the idea of identity versus equality from the earlier chapters on strings and hash maps, and with sorting and merging from the chapter on comparators. Two pointers from Chapter 08 supply the habit of moving more than one reference in a single pass. The monotonic structures of Chapters 12 and 13 are not needed. Doubly linked caches, which pair a chain with a map, are named at the end of this chapter as a later topic.

### The Eleven Lessons

The first lesson sets out what a node is and why reachability is the property to protect. The second reverses a chain, and the third reverses only a stretch of it or every full block of a given size. The fourth merges two ordered chains, and the fifth shows how a dummy node removes the special case of the first node. The sixth detects a loop and finds where it starts, and the seventh finds where two chains join. The eighth finds the middle with two speeds, the ninth finds a node at a fixed distance from the end with two pointers kept apart, and the tenth flattens chains hidden inside other chains. The eleventh lesson combines the chain with a hash map to duplicate a structure whose nodes point at each other arbitrarily.

### How To Work Through A Lesson

Each lesson begins with a short scene and a plain method that works but costs too much. Read the bottleneck and try to say what is thrown away, then read the insight. The traces show the references after every step, and the text names the single step to study twice. Try each exercise on paper first. Before using a hint, write down which references you hold, which link you are about to overwrite, and which node would become unreachable if you did it now. Every solution is compiled and run, and compared with a slower method.

### Leaving The Chapter

You should be able to explain in one sentence why each link edit is ordered as it is, why a dummy node is worth its allocation, and why two pointers at different speeds can decide questions that no single pointer can. You should also be able to say when identity, and not value, is the right comparison. The review at the end poses short scenarios, and it is worth repeating after a few days.
