<!-- lesson-kind: standard -->
<!-- lesson-id: quadtree-construction -->
## Split A Grid Into Four Parts

<!-- stage: context -->
### Storing A Mostly Blank Map Mask

A mapping tool keeps a land-and-sea mask of 1024 by 1024 cells. Each cell holds 0 for sea or 1 for land. Most of the mask is large open sea or large solid land. The tool stores one entry per cell, so a mask of one million cells needs one million entries. This holds even when an area of 512 by 512 cells has a single value. The developer wants to store such an area once and split an area only when it holds both values.

The idea needs a rule for how to cut a square area into smaller pieces, and a rule for when to stop cutting. This lesson builds a tree from the grid with those two rules.

<!-- stage: naive -->
### Always Cutting Down To Single Cells

The first version cuts every square into four equal squares, and it keeps cutting until each square is one cell. A node at the bottom holds the value of one cell.

```java
final class CutToCells {
    static final class Node {
        int val;                                                 // meaningful only for a single cell
        Node topLeft, topRight, bottomLeft, bottomRight;
    }

    static int nodes;                                            // counts every node that is created

    static Node build(int[][] grid, int r, int c, int size) {
        Node node = new Node();
        nodes++;
        if (size == 1) { node.val = grid[r][c]; return node; }   // one cell is the end of the cutting
        int half = size / 2;                                     // each side is cut in half
        node.topLeft = build(grid, r, c, half);
        node.topRight = build(grid, r, c + half, half);
        node.bottomLeft = build(grid, r + half, c, half);
        node.bottomRight = build(grid, r + half, c + half, half);
        return node;
    }
}
```

For a grid with side 2, the method creates 5 nodes: one for the whole grid and four for its cells. The result is correct, because the cells at the bottom hold every value.

<!-- stage: bottleneck -->
### Counting The Nodes For A Blank Grid

```predict
The grid has side 8, and every cell holds the same value. How many nodes does the method create, and how many would be enough to describe the grid?

The method creates 1 + 4 + 16 + 64 = 85 nodes, one for each square at every level. A single node that stores the value would be enough, because every cell is the same.
```

The tree has one leaf for every cell, so the memory is O(n^2) nodes for a grid of side n, and it adds the nodes above the leaves. The method gives no saving at all. It spends the same time and more memory than the plain array.

The cutting was never needed for a square whose cells are all equal. That square already has an answer. The method needs a test before it cuts. If the square is entirely one value, the call can stop and return one node for the whole square. If the square holds both values, no single node describes it, and the cutting continues.

<!-- stage: insight -->
### Cutting Only When Both Values Appear

The method treats every square area of the grid as a question that can be answered with one node or with four smaller questions.

<!-- names: region, uniform, quadrant -->

#### A Region Is A Square With A Corner And A Side

A **region** is a square block of the grid, written as the row `r` and column `c` of its top-left cell and its side length `size`. The whole grid is the region `(0, 0, n)`. The side length of the whole grid is a power of two, so every cut gives integer sides all the way down to one cell.

#### Uniform Regions Stop The Cutting

A region is **uniform** when every cell in it equals the first cell. A call tests this before it creates any child. If the region is uniform, the call returns one **leaf**, a node that stores the shared value and has no children. A region with one cell is always uniform, so the cutting always ends.

#### Four Quadrants For A Mixed Region

If the region holds both values, the call cuts it into four **quadrants**. Let `half` be `size / 2`. Each quadrant is a square of side `half`. Their top-left cells are `(r, c)`, `(r, c + half)`, `(r + half, c)` and `(r + half, c + half)`. The quadrants do not overlap, and together they cover the region exactly. The call returns an internal node whose four children come from four recursive calls, one per quadrant.

#### What One Call Owns

The invariant is that a call owns exactly one region and returns the node that represents exactly that region. The node is a leaf for a uniform region and has four children otherwise. The test comes before the cut. The tree therefore never holds a node whose four children are equal leaves, because such a node would have been one leaf.

<!-- stage: variables -->
### The Values A Call Holds

- **r** and **c** are the row and the column of the top-left cell of the region.
- **size** is the side length of the region, always a power of two.
- **half** is `size / 2`, the side length of each quadrant.
- **first** is the value of the cell at `(r, c)`, which every other cell must equal for the region to be uniform.

The four child regions use the offsets `0` and `half` for the row and for the column. A leaf stores `first` and no children. An internal node stores no value that the tree uses.

<!-- stage: trace -->
### Cutting A Four By Four Grid

#### One Cut Is Enough

The grid has four rows: `1 1 0 0`, `1 1 0 0`, `1 1 1 1` and `1 1 1 1`. The cells list the grid row by row, so the cell at row `i` and column `j` has index `4i + j`. The pointers `start` and `end` mark the top-left and bottom-right cells of the region that a call owns.

```trace
{"cells":["1","1","0","0","1","1","0","0","1","1","1","1","1","1","1","1"],"pointers":["start","end"],"steps":[{"at":{"start":0,"end":15},"vars":{"region":"row 0, column 0, side 4","result":"cut"},"note":"The whole grid holds 1 and also a different value at row 0, column 2, so the call cuts it into four quadrants."},{"at":{"start":0,"end":5},"vars":{"region":"row 0, column 0, side 2","result":"leaf 1"},"note":"The top-left quadrant has every cell equal to 1, so the call returns one leaf with the value 1."},{"at":{"start":2,"end":7},"vars":{"region":"row 0, column 2, side 2","result":"leaf 0"},"note":"The top-right quadrant has every cell equal to 0, so the call returns one leaf with the value 0."},{"at":{"start":8,"end":13},"vars":{"region":"row 2, column 0, side 2","result":"leaf 1"},"note":"The bottom-left quadrant has every cell equal to 1, so the call returns one leaf with the value 1."},{"at":{"start":10,"end":15},"vars":{"region":"row 2, column 2, side 2","result":"leaf 1"},"note":"The bottom-right quadrant has every cell equal to 1, so the call returns one leaf with the value 1."}]}
```

The whole grid mixes both values, so it is cut once. The four quadrants are all uniform, and each returns a leaf. The tree has five nodes instead of 21.

#### One Quadrant Needs A Second Cut

The second grid has the rows `0 0 1 1`, `0 0 1 0`, `1 1 1 1` and `1 1 1 1`. The top-right quadrant mixes both values.

```trace
{"cells":["0","0","1","1","0","0","1","0","1","1","1","1","1","1","1","1"],"pointers":["start","end"],"steps":[{"at":{"start":0,"end":15},"vars":{"region":"row 0, column 0, side 4","result":"cut"},"note":"The whole grid holds 0 and also a different value at row 0, column 2, so the call cuts it into four quadrants."},{"at":{"start":0,"end":5},"vars":{"region":"row 0, column 0, side 2","result":"leaf 0"},"note":"The top-left quadrant has every cell equal to 0, so the call returns one leaf with the value 0."},{"at":{"start":2,"end":7},"vars":{"region":"row 0, column 2, side 2","result":"cut"},"note":"The top-right quadrant holds 1 and also a different value at row 1, column 3, so the call cuts it into four quadrants."},{"at":{"start":2,"end":2},"vars":{"region":"row 0, column 2, side 1","result":"leaf 1"},"note":"The top-left quadrant has every cell equal to 1, so the call returns one leaf with the value 1."},{"at":{"start":3,"end":3},"vars":{"region":"row 0, column 3, side 1","result":"leaf 1"},"note":"The top-right quadrant has every cell equal to 1, so the call returns one leaf with the value 1."},{"at":{"start":6,"end":6},"vars":{"region":"row 1, column 2, side 1","result":"leaf 1"},"note":"The bottom-left quadrant has every cell equal to 1, so the call returns one leaf with the value 1."},{"at":{"start":7,"end":7},"vars":{"region":"row 1, column 3, side 1","result":"leaf 0"},"note":"The bottom-right quadrant has every cell equal to 0, so the call returns one leaf with the value 0."},{"at":{"start":8,"end":13},"vars":{"region":"row 2, column 0, side 2","result":"leaf 1"},"note":"The bottom-left quadrant has every cell equal to 1, so the call returns one leaf with the value 1."},{"at":{"start":10,"end":15},"vars":{"region":"row 2, column 2, side 2","result":"leaf 1"},"note":"The bottom-right quadrant has every cell equal to 1, so the call returns one leaf with the value 1."}]}
```

The top-right quadrant is cut again into four single cells, and each cell is a leaf. The other three quadrants are uniform at once. The tree has nine nodes, and the extra cutting happens only where both values appear.

<!-- stage: code -->
### The Construction In Code

```java
final class QuadTree {
    static final class Node {
        boolean val;                                             // the shared value of a leaf
        boolean isLeaf;
        Node topLeft, topRight, bottomLeft, bottomRight;
        Node(boolean val, boolean isLeaf) { this.val = val; this.isLeaf = isLeaf; }
    }

    static Node build(int[][] grid) {
        return build(grid, 0, 0, grid.length);                   // the whole grid is the first region
    }

    private static Node build(int[][] grid, int r, int c, int size) {
        int first = grid[r][c];
        boolean uniform = true;
        for (int i = r; i < r + size && uniform; i++) {          // scan the rows of the region
            for (int j = c; j < c + size; j++) {                 // scan the cells of one row
                if (grid[i][j] != first) { uniform = false; break; }   // a different cell ends the scan
            }
        }
        if (uniform) return new Node(first == 1, true);          // one leaf describes the whole region
        int half = size / 2;                                     // the side of each quadrant
        Node node = new Node(true, false);                       // an internal node stores no meaningful value
        node.topLeft = build(grid, r, c, half);
        node.topRight = build(grid, r, c + half, half);
        node.bottomLeft = build(grid, r + half, c, half);
        node.bottomRight = build(grid, r + half, c + half, half);
        return node;
    }
}
```

The method relies on integer division being exact. For a side that is not a power of two, such as 3, `half` is 1, and the four quadrants cover only 4 of the 9 cells.

- **Time** is O(n^2 log n) for a grid of side n. The regions on one level do not overlap, so one level reads at most n^2 cells, and there are about log n levels.
- **Space** is O(log n) for the stack, plus the nodes of the tree, whose number is at most about the number of cells.

<!-- stage: applicability -->
### Testing Before Splitting

#### Stating What A Call Returns

The invariant is simple. A call owns one region and returns a node for exactly that region. The node is a leaf when all cells agree, and it has four quadrant children otherwise. Write the region as three numbers before you write the recursion. A call that receives a region of the wrong shape gives a tree that covers the wrong cells.

#### Finding The False Friend

Creating the four children first and testing afterward looks natural, because the structure of the tree is symmetric. It is the false friend of this topic. The tree then has a node for every cell of the grid and no saving. The test also must scan the region and not just compare the four corners, because two cells can agree while a cell between them differs.

#### No-Go Conditions

The method needs a square grid whose side is a power of two. For a rectangle or an odd side, the quadrants do not tile the region, and the cut rule needs a different shape. If most regions are mixed, such as a noisy image, the tree is as large as the grid and saves nothing.

<!-- stage: exercises -->
### Exercises

#### [Build] Uniform Region Test (Author exercise)
<!-- id: qt-uniform -->

**Prerequisites.** The region and the uniform test from this lesson.

**Problem.** A square grid of 0 and 1 values is given. A region has its top-left cell at row `r` and column `c`, and a side length `size`. Return `true` if every cell of the region equals the cell at `(r, c)`.

**Constraints.** The limits are:
- **Grid** has `n` rows and `n` columns with `n` a power of two up to 64.
- **Cells** hold 0 or 1.
- **Region** satisfies `r + size <= n` and `c + size <= n`, with `size >= 1`.
- **Answer** is a `boolean`, and a region of size 1 gives `true`.

**Example 1.** Input the grid with rows `1 1 0 0`, `1 1 0 0`, `1 1 1 1`, `1 1 1 1`, and the region `r = 0, c = 0, size = 2`. Output `true`.

**Example 2.** Input the grid with rows `0 0 1 1`, `0 0 1 0`, `1 1 1 1`, `1 1 1 1`, and the region `r = 0, c = 2, size = 2`. Output `false`.

**Hint.** Which value does every other cell compare with? When can the scan stop?

**Changed decision.** The scan stops at the first cell that differs.

#### [Vary] Split Four Quadrants (Author exercise)
<!-- id: qt-split -->

**Prerequisites.** The exercise above and the quadrants from this lesson.

**Problem.** A region is given by the row `r` and column `c` of its top-left cell and an even side length `size`. Return the four quadrants as triples `[row, column, side]`, in the order top-left, top-right, bottom-left, bottom-right. The quadrants do not overlap and cover the region.

**Constraints.** The limits are:
- **Row and column** are integers between 0 and 1023.
- **Side** is an even integer between 2 and 1024.
- **Answer** has four triples, each with side `size / 2`.
- **Mutation** does not apply, because the method reads three integers.

**Example 1.** Input `r = 0, c = 0, size = 4`, output `[0,0,2]`, `[0,2,2]`, `[2,0,2]`, `[2,2,2]`.

**Example 2.** Input `r = 4, c = 2, size = 2`, output `[4,2,1]`, `[4,3,1]`, `[5,2,1]`, `[5,3,1]`.

**Hint.** Which offset moves the column, and which moves the row? What is added to each coordinate?

**Changed decision.** The method computes bounds only and does not read the grid.

#### [Boundary] One Cell (Author exercise)
<!-- id: qt-leaf-count -->

**Prerequisites.** The two exercises above.

**Problem.** Given a square grid of 0 and 1 values with a side that is a power of two, return the number of leaves in its quadtree. A region that is uniform becomes one leaf. A grid with a single cell has one leaf, and the method must not cut it further.

**Constraints.** The limits are:
- **Grid** has side `n`, a power of two with `1 <= n <= 64`.
- **Cells** hold 0 or 1.
- **Answer** is an integer between 1 and `n * n`.
- **Mutation** is not allowed.

**Example 1.** Input the grid `[[1]]`, output 1.

**Example 2.** Input the grid with rows `0 1` and `1 0`, output 4.

**Hint.** What does a region of side 1 return? Which test comes before the cut?

**Changed decision.** The test comes first, so a single cell is a leaf and is never cut.

#### [Recognize] Construct Quad Tree (LeetCode 427)
<!-- id: qt-construct -->

**Prerequisites.** All three exercises above.

**Problem.** Given a square grid of 0 and 1 values with a side that is a power of two, build its quadtree and return the root. A leaf stores `isLeaf = true` and the shared value. An internal node stores `isLeaf = false`, four children in the order top-left, top-right, bottom-left, bottom-right, and any value. A uniform region must be one leaf, and no internal node may have four equal leaf children.

**Constraints.** The limits are:
- **Grid** has side `n`, a power of two with `1 <= n <= 64`.
- **Cells** hold 0 or 1.
- **Answer** is the root of the tree.
- **Mutation** is not allowed.

**Example 1.** Input the grid with rows `0 0 1 1`, `0 0 1 0`, `1 1 1 1`, `1 1 1 1`, output an internal root. Its top-left child is a leaf 0, and its top-right child is internal with leaves 1, 1, 1, 0. Its bottom children are leaves 1 and 1.

**Example 2.** Input the grid `[[0, 0], [0, 0]]`, output a single leaf 0.

**Hint.** Which check comes first in each call? How do you find the four child corners?

**Changed decision.** An internal node is built only after the uniform test fails.
