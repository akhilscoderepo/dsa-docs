<!-- section: orientation -->
## Orientation

A formula engine returns -5 for `8 3 -` and passes every test that uses a plus sign. A job runner starts the newest job first, so the oldest job waits forever. A JSON checker accepts `[1, {2]}` because every symbol has a partner somewhere. All three programs hold unfinished work in a container, and each one takes that work out in the wrong order. This chapter answers one question: which end of a container should a program use, so that unfinished work comes back when the rules say it should?

### Prerequisites

You should know arrays, `String` and `char`, loops, and the cost words from Chapter 00. A few lessons use `int[]` and simple grid or graph neighbors. Each lesson defines its own terms the first time they matter, including stack, queue and frame.

### The Eleven Lessons

Each lesson fixes one rule about which item leaves the container next.

- **Use ArrayDeque For Stack And Queue** lists the exact calls for each end and what they do on an empty deque.
- **Process Items In Arrival Order** runs a queue until every task finishes, including tasks that return for another turn.
- **Build A Queue From Two Stacks** moves items between two stacks and counts the cost of each call.
- **Find Shortest Steps With A Queue** explores a search level by level so the first hit is the cheapest.
- **Check That Brackets Match In Order** stores each open bracket until its partner arrives.
- **Save State For Each Nesting Level** stores a partial result when a group opens and restores it when the group closes.
- **Track The Minimum In A Stack** stores one extra answer next to each value.
- **Group Queue Items By Level** counts the items in the queue before each pass, so one loop stops at each level.
- **Decode Nested Repeat Groups** keeps the text and the count that belong outside the open group.
- **Evaluate Expressions Written As Text** delays each operator until its number is complete.
- **Evaluate Postfix And Convert Infix** pops operands in the right order and moves operators between two stacks.

### The Combination Lesson

One lesson joins the stack lessons with the reading lessons.

- **Stack And Parsing State** shows what the reading step decides and what the stack holds for four different texts.

### How To Work Through Each Lesson

Each lesson starts with a program that fails on a real input and then shows a simple version that works but costs too much. A prediction question follows, and you answer it before the explanation appears. Two traces show the container after each step. Four exercises close the lesson, from a direct build to a problem you must recognize from its wording. Write the removal order you expect before you open a hint.

### What You Can Do After This Chapter

You can name the end of a deque that each call touches and say what it returns on an empty deque. You can choose a stack when the newest unfinished item must finish first, and a queue when the oldest must go first. You can say what one stack entry stores, and you can write the check that rejects bad input before any state changes.
