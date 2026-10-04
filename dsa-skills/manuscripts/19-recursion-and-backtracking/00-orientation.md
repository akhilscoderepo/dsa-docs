<!-- section: orientation -->
## Orientation

A large family of problems asks for every answer and not just one: all the subsets of a list, all the orders of some tasks, all the ways to cut a word into parts, all the placements of queens that do not threaten one another. The method for them is to build an answer one decision at a time on a single shared path, to look at what that path allows, and then to undo the decision exactly so that the next alternative starts from the same place. This chapter teaches that method from its smallest piece, a call that knows what it is asked, up to searches over boards, and ends by joining it with the trie of the previous chapter.

### What To Bring

Everything here is recursion over a few numbers, so you should be at ease with a method that calls itself and with reading the depth of a call as a measure of progress. The input and output contracts of Chapter 00 apply to every exercise, and each problem states whether the input may be changed. Lists and arrays from Chapter 01, string indexing from Chapter 03 and the habit of copying before storing come with you. The recursion over trees in Chapter 15 gave you the idea of a return value built from smaller calls, and the trie of Chapter 18 is needed in the last lesson only.

### The Eleven Lessons

The first lesson defines what one call promises and why every call has to get closer to a stopping point. The second adds the shared path with its place, explore and undo moves. The third generates every subset, the fourth every arrangement, and the fifth every selection of a fixed size in which order does not matter. The sixth lets an item be used any number of times, the seventh handles equal values in the input, and the eighth shows when a branch may be abandoned and when it may not. The ninth cuts a whole sequence into pieces, the tenth searches grids and boards with markers, and the eleventh uses a trie to search a board for many words together.

### How To Work Through A Lesson

Each lesson begins with a short scene and a plain method that is correct but wasteful, and it helps to name the wasted work yourself before the insight arrives. When you follow a trace, say aloud what the shared path holds at that step and what each marker says. For every exercise decide first what the call state is, then what makes the recursion stop, and then what must be undone on the way back. Every solution file runs the clever method against a slower one on random inputs, so an answer that surprises you deserves a hand trace.

### Leaving The Chapter

You should be able to say what a call's state is and what shrinks in it, and to explain why a path must be copied when it is stored and restored when a call returns. You should be able to choose between a start index, a table of used marks, a same-index call and a loop over endings by looking at what the output is. You should be able to say what proof backs each pruned branch, and why a skip rule compares neighbours in one loop and not along the whole path. The review questions are scenarios, and they repay a second attempt after a few days.
