<!-- section: orientation -->
## Orientation

A tree is data that contains smaller copies of itself. Each node owns a whole subtree, no subtree has two owners, and a missing branch is a perfectly good, empty subtree. Once that is accepted, a large group of questions turns into one habit: write the answer for the empty case, assume both branches have already answered, and say how the node combines the two answers. This chapter follows that habit through traversal order, explicit stacks, depth and path state, subtree summaries, failure marks, reconstruction from two sequences, a traversal that borrows null links, and a tree built over a grid.

### What To Bring

You should be at ease with recursion on arrays, with classes that hold references to other objects, and with the idea of an invariant from the linked list chapter. The explicit stack of Chapter 11 returns here in a new role. Maps from the hash chapter are used for the reconstruction lesson, and two-dimensional indexing from the matrix chapter is needed for the last lesson. Breadth-first walks over levels are not assumed, because they open the next chapter.

### The Ten Lessons

The first lesson fixes what a node and an empty subtree mean for binary and general trees. The second shows that preorder, inorder and postorder are one walk with the same action placed at three different moments. The third replaces the call stack with a stack that the program controls, and the fourth separates state that travels down from summaries that travel up. The fifth returns one branch while scoring two, the sixth carries a failure mark through a height, and the seventh rebuilds a tree from two sequences. The eighth walks in constant extra space by borrowing empty links, and the ninth compresses a square grid into a tree of uniform blocks. The tenth lesson combines the tree with depth-first return values to answer four questions in one pass each.

### How To Work Through A Lesson

Every lesson opens with a short scene and a plain method that is right but wasteful. Try to name the wasted work before reading the insight. Then follow each trace one step at a time, and say aloud which values go down and which come up. For each exercise, first decide what a call on an empty subtree returns and what each call hands to its parent, and only then write code. Every solution file is compiled and run against a slower method, so a surprising answer is worth tracing by hand.

### Leaving The Chapter

You should be able to say, for any tree question, what is passed down, what is returned up, and what is kept aside as a running result. You should be able to justify the position of a node action among its child calls, and you should recognise the cases that overflow a call stack. The review section asks short scenario questions, and it repays a second attempt after a few days.
