<!-- lesson-kind: standard -->
<!-- lesson-id: quadtree-construction -->
## Quadtree Construction

<!-- stage: context -->
### The Mosaic Restorer's Ledger

A restorer is cataloguing a square mosaic floor made of black and white tiles, laid out in a grid whose side is a power of two. Her ledger has room for only a few lines, so she cannot list every tile. She notices that large stretches of the floor are a single colour, and she decides to record such a stretch as one entry. A stretch that has both colours is cut into four equal quarters, top left, top right, bottom left and bottom right, and each quarter is recorded in the same way.

She wants to know how to decide quickly what a stretch is, and how to be sure that the quarters she cuts are exactly the right size, never overlapping and never leaving a tile out. She also wants the ledger to stay short when the floor is mostly one colour.

<!-- stage: naive -->
### Cut Everything Down To Single Tiles

The direct method skips the decision. She cuts every stretch into four quarters, and those into four more, until every stretch is one tile, and writes an entry for each tile. Afterwards she goes back and merges any four neighbouring entries that show the same colour.

```java
static String full(int[][] floor, int top, int left, int side) {
    if (side == 1) return String.valueOf(floor[top][left]);
    int half = side / 2;
    String a = full(floor, top, left, half);
    String b = full(floor, top, left + half, half);
    String c = full(floor, top + half, left, half);
    String d = full(floor, top + half, left + half, half);
    if (a.length() == 1 && a.equals(b) && a.equals(c) && a.equals(d)) return a;
    return "(" + a + b + c + d + ")";
}
```

After merging, a stretch is a single entry exactly when its four quarters were single entries of one colour, so the result is correct.

<!-- stage: bottleneck -->
### Every Tile Gets An Entry First

The cutting creates one entry for every tile before any merging starts. For a floor with N tiles that is N entries and about N / 3 more for the stretches above them, so the memory is proportional to N whatever the answer looks like. A floor of sixteen million tiles that is all one colour still needs sixteen million entries, which are merged into one and thrown away.

The decision can be made before the cutting. If the stretch is already one colour, one entry is written and no quarters are made. Only a stretch with two colours is cut, so the number of entries made is the size of the answer. Checking a stretch costs a look at its tiles, and a stretch that is not one colour usually shows its second colour early. The checking at one level of cutting touches each tile at most once, so with about log n levels the worst case is O(N log n) steps, in return for allocating only what the answer needs.

<!-- stage: insight -->
### Decide Before You Divide

Let every call own one square block of the grid, described by its top row, its left column and its side length. These **region bounds** are the whole state, and the call returns the node that stands for exactly that block. The call first runs the **uniform test**: compare every cell of the block with its first cell. If all match, return a leaf holding that value and make no other call. Only a block that fails the test is divided.

Division follows a fixed rule. With half equal to the side divided by two, the four **quadrants** start at the top-left corner of the block, half columns to the right, half rows down, and half rows down and half columns to the right, and each has side half. These four squares do not overlap and together cover the block exactly, since each tile belongs to the one whose row range and column range contain it. A block of side one is always uniform, so division never reaches a side of zero.

The invariant is that every call owns a precise block and returns the node for exactly that block, and the children of any internal node cover its block with no gap. A leaf is made for a uniform block, so no internal node has four equal leaf children.

<!-- names: region bounds, uniform test, quadrants -->

Making four children first and testing afterwards builds structure that is thrown away.

<!-- stage: variables -->
### Bounds, First Cell And Half

A call carries `top`, `left` and `side`. The uniform test reads `grid[top][left]` as the first value and loops over rows `top` to `top + side - 1` and columns `left` to `left + side - 1`, stopping at the first difference. The variable `half` is `side / 2`, which is exact because the side is a power of two and is at least 2 whenever a block is divided. The four child calls differ only in whether `half` is added to the row, the column, both or neither.

<!-- stage: trace -->
### Only Mixed Blocks Are Cut

The first trace builds the ledger for a four by four floor whose rows are 1 1 0 0, 1 1 0 0, 1 0 1 1 and 1 0 1 1, with the cells listed row by row. The pointer `cell` marks the top-left tile of the block under examination, and `side` shows its size. The whole floor has both colours and is cut, three of the four quarters are single-colour and recorded at once, and one quarter is mixed and is cut down to its tiles.

```trace
{"cells":["1","1","0","0","1","1","0","0","1","0","1","1","1","0","1","1"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"side":4},"note":"The block of side 4 at row 0, column 0 holds both values, so it is cut into four blocks of side 2."},{"at":{"cell":0},"vars":{"side":2},"note":"The block of side 2 at row 0, column 0 holds only 1, so it is written as one leaf."},{"at":{"cell":2},"vars":{"side":2},"note":"The block of side 2 at row 0, column 2 holds only 0, so it is written as one leaf."},{"at":{"cell":8},"vars":{"side":2},"note":"The block of side 2 at row 2, column 0 holds both values, so it is cut into four blocks of side 1."},{"at":{"cell":8},"vars":{"side":1},"note":"The block of side 1 at row 2, column 0 holds only 1, so it is written as one leaf."},{"at":{"cell":9},"vars":{"side":1},"note":"The block of side 1 at row 2, column 1 holds only 0, so it is written as one leaf."},{"at":{"cell":12},"vars":{"side":1},"note":"The block of side 1 at row 3, column 0 holds only 1, so it is written as one leaf."},{"at":{"cell":13},"vars":{"side":1},"note":"The block of side 1 at row 3, column 1 holds only 0, so it is written as one leaf."},{"at":{"cell":10},"vars":{"side":2},"note":"The block of side 2 at row 2, column 2 holds only 1, so it is written as one leaf."}]}
```

The second trace uses a floor that is all 0 except for the last tile, which is 1. Only the blocks that contain the odd tile are cut, and the other three quarters of each cut are written down as single entries without being examined further. The chain of cuts follows the odd tile down to its own cell.

```trace
{"cells":["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"side":4},"note":"The block of side 4 at row 0, column 0 holds both values, so it is cut into four blocks of side 2."},{"at":{"cell":0},"vars":{"side":2},"note":"The block of side 2 at row 0, column 0 holds only 0, so it is written as one leaf."},{"at":{"cell":2},"vars":{"side":2},"note":"The block of side 2 at row 0, column 2 holds only 0, so it is written as one leaf."},{"at":{"cell":8},"vars":{"side":2},"note":"The block of side 2 at row 2, column 0 holds only 0, so it is written as one leaf."},{"at":{"cell":10},"vars":{"side":2},"note":"The block of side 2 at row 2, column 2 holds both values, so it is cut into four blocks of side 1."},{"at":{"cell":10},"vars":{"side":1},"note":"The block of side 1 at row 2, column 2 holds only 0, so it is written as one leaf."},{"at":{"cell":11},"vars":{"side":1},"note":"The block of side 1 at row 2, column 3 holds only 0, so it is written as one leaf."},{"at":{"cell":14},"vars":{"side":1},"note":"The block of side 1 at row 3, column 2 holds only 0, so it is written as one leaf."},{"at":{"cell":15},"vars":{"side":1},"note":"The block of side 1 at row 3, column 3 holds only 1, so it is written as one leaf."}]}
```

<!-- stage: code -->
### Compress Uniform Blocks Into Leaves

```java
final class QuadBuilder {
    static boolean uniform(int[][] grid, int top, int left, int side) {
        int first = grid[top][left];
        for (int r = top; r < top + side; r++)
            for (int c = left; c < left + side; c++)
                if (grid[r][c] != first) return false;
        return true;
    }

    static String build(int[][] grid, int top, int left, int side) {
        if (uniform(grid, top, left, side)) return String.valueOf(grid[top][left]);
        int half = side / 2;
        return "(" + build(grid, top, left, half)
                + build(grid, top, left + half, half)
                + build(grid, top + half, left, half)
                + build(grid, top + half, left + half, half) + ")";
    }
}
```

Each level of division touches each tile at most once in the uniform tests, and a floor of side n has about log n levels, so the time is O(N log n) for N = n squared tiles in the worst case. The recursion depth is only log n, and the memory is proportional to the size of the answer.

<!-- stage: applicability -->
### When A Grid Splits Into Four

Use this for square grids whose uniform parts can be summarised: map tiles, image compression, collision regions, and any grid where large stretches are alike. The invariant is that each call owns exactly one square block, and returns the node for that block alone.

A false friend is making four children first and checking afterwards, which allocates the full tree in a place where the answer may be one leaf. A second false friend is the cut into four that is slightly off. A quadrant that starts one row too early overlaps its neighbour, and a block of odd side divided by two leaves a tile uncovered. A third is reading the grid as `grid[column][row]`, which silently swaps two quadrants of a non-symmetric floor.

In Java, build a string or a node only after the uniform test fails, and take care with the order of the four child calls, because the serialisation depends on it. Check the side before dividing, since `1 / 2` is 0 in integer arithmetic.

<!-- stage: exercises -->
### Exercises

#### [Build] Uniform Region Test (Author exercise)
<!-- id: tr-uniform-region -->

**Prerequisites.** The recursion lessons of this chapter and two-dimensional array indexing.

**Problem.** A square grid of 0 and 1 values is given with a region described by `top`, `left` and `side`. Return whether every cell of that region equals the first cell of the region.

**Constraints.** The grid side is a power of two between 1 and 64, and the region lies inside the grid.

**Example 1.** Input `grid = [[1, 1], [1, 0]]`, `top = 0, left = 0, side = 1`, output `true`.

**Example 2.** Input `grid = [[1, 1], [1, 0]]`, `top = 0, left = 0, side = 2`, output `false`.

**Hint.** Which cell do the others have to match, and when can the scan stop?

**Changed decision.** The test belongs before any division, so a matching region becomes one leaf with no further calls.

#### [Vary] Split Four Quadrants (Author exercise)
<!-- id: tr-split-quadrants -->

**Prerequisites.** The Uniform Region Test rung and the bounds of a region.

**Problem.** Given a region by `top`, `left` and `side`, with an even side, return its four quadrants as `[top, left, side]` triples in the order top-left, top-right, bottom-left, bottom-right. The quadrants must not overlap and must cover the region exactly.

**Constraints.** 2 <= side <= 64, side is a power of two, and 0 <= top, left <= 1000.

**Example 1.** Input `top = 0, left = 0, side = 4`, output `[[0, 0, 2], [0, 2, 2], [2, 0, 2], [2, 2, 2]]`.

**Example 2.** Input `top = 2, left = 4, side = 2`, output `[[2, 4, 1], [2, 5, 1], [3, 4, 1], [3, 5, 1]]`.

**Hint.** What is added to the row, and what to the column, for each of the four?

**Changed decision.** A child's bounds are the parent's bounds shifted by half the side in the row, the column, both, or neither.

#### [Boundary] One Cell (Author exercise)
<!-- id: tr-one-cell -->

**Prerequisites.** The Split Four Quadrants rung and the base case of side one.

**Problem.** Build the compressed quadtree of a square grid of 0 and 1 values and return the number of nodes in it, leaves and internal nodes together. A region of side one is always a leaf and is never divided.

**Constraints.** The grid side is a power of two between 1 and 64.

**Example 1.** Input `grid = [[1]]`, output `1`.

**Example 2.** Input `grid = [[1, 0], [0, 1]]`, output `5`.

**Hint.** When does a call return without making any child call, and what does a side of one guarantee?

**Changed decision.** A single cell is uniform by itself, so the base case needs no extra rule and division stops at side one.

#### [Recognize] Construct Quad Tree (LeetCode 427)
<!-- id: tr-construct-quad-tree -->

**Prerequisites.** The One Cell rung and the uniform test.

**Problem.** Compress a square grid of 0 and 1 values into a quadtree and return it as a string in preorder. A leaf is written as its value, `0` or `1`, and an internal node is written as an opening parenthesis, the strings of its top-left, top-right, bottom-left and bottom-right children in that order, and a closing parenthesis.

**Constraints.** The grid side is a power of two between 1 and 64.

**Example 1.** Input `grid = [[1, 1], [1, 1]]`, output `1`.

**Example 2.** Input `grid = [[1, 0], [1, 1]]`, output `(1011)`.

**Hint.** Which blocks become leaves, and what happens in a block that does not?

**Changed decision.** Internal nodes are made only for mixed blocks, and a uniform block of any size is one leaf.
