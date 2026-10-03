<!-- section: orientation -->
## Orientation

Stacks and queues are the two simplest ways to remember work that has not been finished. A stack hands back the newest unfinished item first, which suits anything nested: brackets, undo steps, a calculation that has been interrupted by a smaller calculation. A queue hands back the oldest unfinished item first, which suits fairness, waiting lines and exploring outward in rounds. This chapter shows how little machinery each one needs in Java, and then spends most of its time on the questions that decide whether the code is right: which end does what, what happens when the container is empty, and what exactly is stored.

### Before You Begin

You should be comfortable with arrays, strings and loops, with the way Java sorts and compares values from the earlier chapters, and with the habit of stating a problem's input and output guarantees before writing code. No graph or tree knowledge is needed. The queue lessons only use lists of successors that are supplied, and the full treatment of graphs and trees comes in later chapters.

### The Twelve Lessons

The first lesson covers `ArrayDeque`, the one class used for both structures, with its two families of methods and its refusal to hold `null`. The second runs a first-in-first-out simulation and recognizes when a line is stuck. The third builds a queue from two stacks and explains why the work is shared out evenly. The fourth lets a queue explore states by the number of moves from a start. The fifth and sixth turn to stacks: matching brackets of several kinds and keeping one frame of state for every open level. The seventh makes a stack that always knows its minimum. The eighth returns to queues and processes work in rounds by capturing the size of the queue before draining it. The ninth decodes nested repeat notation, the tenth reads calculator input with precedence and brackets, and the eleventh evaluates postfix formulas and converts ordinary arithmetic into them. The twelfth combines a parser with a stack in four small tasks.

### How To Work Through A Lesson

Each lesson begins with a small situation and a method that works but repeats effort. Before reading the insight, say what a stack or a queue would have to remember. The traces print the contents of the container after every step, so predict the next line before you reveal it. Try every exercise before opening its hint, and write down three facts first: what is stored, what happens at the open end, and what happens when the container is empty. The Java in every solution is compiled and run against a slower method that tries everything.

### Leaving The Chapter

You should be able to say why `push` and `addLast` must never be mixed, why the queue size is read once before a round is drained, and why a postfix evaluator pops the right operand first. You should also be able to explain why a stack of totals replaces recursion on deeply nested input, and why a comparison with equality keeps duplicate minimums alive. The review that follows poses short scenarios, and it is worth returning to after a few days.
