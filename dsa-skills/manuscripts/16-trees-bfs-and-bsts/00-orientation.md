<!-- section: orientation -->
## Orientation

The previous chapter treated a tree as something to be walked in depth. This chapter adds two new ways of looking at the same structure. The first is by distance from the top, where a queue hands out the nodes wave by wave and a single captured number marks the end of each wave. The second is by order of the keys, where a promise stored in the tree, smaller on the left and larger on the right, lets one comparison discard a whole branch. Most of the lessons are one of these two ideas applied to a different question.

### What To Bring

You should be comfortable with the recursive walks of Chapter 15, with the first-in, first-out queue of Chapter 11, and with the way an explicit stack can replace recursion. The binary search chapter helps, since a search tree is the same halving idea written in links. Heaps and priority queues are not needed and arrive in the next chapter. Trees are given as level-order arrays with `null` for each missing child, and the solutions always build real nodes before working with them.

### The Eleven Lessons

The first lesson groups nodes by depth and then reorders or selects them. The second shows why a search tree must be checked with an interval that is handed down, and the third uses the same ordering to search, insert and remove. The fourth finds the key just above or just below another, and the fifth answers rank and band questions by stopping early or skipping branches. The sixth finds where two routes meet, first in any tree and then in a search tree. The seventh turns the sorted walk into an iterator that holds only a short path. The eighth writes a tree as text and reads it back, the ninth explains why shape matters and what a rotation is, and the last two lessons combine the queue with the tree and the carried interval with the search tree.

### How To Work Through A Lesson

Each lesson opens with a short scene and a plain method that is correct and wasteful. Try to name the repeated work before reading the insight. Follow every trace one step at a time and say what the queue, the stack or the interval holds before reading the note. For an exercise, first write down the contract for an empty tree and for a tree with one child. Solutions are compiled and run against a slower oracle, so a surprising answer deserves a hand trace.

### Leaving The Chapter

You should be able to say, for a question about a tree, whether it is read by depth, by key order, or by a route between two nodes. You should be able to state what a search tree promises and what a walk must carry to test it. You should recognise when a plain search tree is a risk because input arrives sorted. The review questions ask for predictions, and they repay a second attempt after a few days.
