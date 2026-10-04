<!-- section: orientation -->
## Orientation

A game board is stored as an `int[][]`. A function that counts the mines next to a cell reports one too many for the top-right corner, because it reads a cell outside the board. A second function that clears every row and column holding a zero wipes half the board, because it reads zeros that it wrote a moment earlier. Both bugs come from treating a grid as a pile of cells and not as rows, columns and a shape with rules. This chapter answers one question: what must a method know about a matrix before it reads or writes a cell?

### Prerequisites

You should know Java arrays, nested `for` loops and the cost vocabulary of Chapter 00. The array patterns of Chapter 01 help, especially the read index and the write index. The chapter needs no other data structure.

### What The Seven Lessons Cover

Each lesson adds one habit for working with a grid, together with the invariant that keeps it correct.

- **Rectangular And Ragged Arrays** reads the width of each row from that row and not from the first one.
- **Walking Rows, Columns And Diagonals** names a region by a rule on the row and column indexes.
- **Moving With A Direction** keeps one cursor and a direction that turns clockwise.
- **Checking The Neighbors Of A Cell** lists nearby cells from a table of offsets and one range test.
- **Rotating A Square In Place** composes a transpose and a row reversal.
- **Marking Rows Before Clearing Them** records which lines to change before any cell changes.
- **Walking A Matrix In Spiral Order** keeps four edges around the cells not yet visited.

### How To Work Through Each Lesson

Every part of a lesson carries a label, so you always see where you are. A lesson opens with a failing case, and then a prediction prompt asks you to name the cause before the answer appears. A trace lets you step through the loop and watch the indexes change. Each lesson closes with four exercises, each with a hidden hint and a hidden solution. Write your own attempt before you open either one.

### What You Can Do After This Chapter

You can read the shape of a matrix from the statement and from the data, and you can state which cells a loop may read after it has written. You can choose between a visited table, a direction cursor and four edges for a walk, and you can say what breaks each choice. You can also name the inputs that break matrix code, such as an empty row, a single row, a single column, a corner cell and an odd side length.
